"""
SERP Thumbnail Study — auto-fetch + VLM-tag a topic's live thumbnail shelf.

Pipeline:
  1. SERP search (scrapetube, quota-free) -> top-N ranking videos for the query
  2. Download their thumbnails (reuses thumbnail_image_audit._download_serp)
  3. Tag EACH thumbnail with Gemini Flash vision into a strict schema
     (operation / face / overlay text + word count / framing / colors / subject / map)
  4. Aggregate into a "shelf study": which conventions dominate, which
     operations are ABSENT (the whitespace a replacement thumb should attack)

This is the classification/study layer the static outlier corpus can't do
per-topic and CLIP cosine can't do at all (CLIP measures distance, not taxonomy).
CLIP differentiation still lives in thumbnail_image_audit.py — different job.

Usage:
    python -m tools.preflight.serp_thumb_study --slug south-china-sea \
        --query "south china sea dispute explained" --query "nine dash line" --top 8

    # Skip search, tag an explicit ID set:
    python -m tools.preflight.serp_thumb_study --slug gibraltar \
        --ids LMTJW_eEYDs,zvyWCP2x1GU,y4ztC1BuDgI --top 8

Output: channel-data/serp-studies/<slug>-<date>.md (+ .json sidecar)
Requires: scrapetube, Pillow, and the `gemini` CLI on PATH (Flash vision).
"""

import argparse
import json
import re
import subprocess
import sys
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Dict, List, Optional

from tools.logging_config import get_logger, setup_logging
from tools.preflight.thumbnail_image_audit import _download_serp

logger = get_logger(__name__)

GEMINI_MODEL = "gemini-2.5-flash"

# HvH operation taxonomy (from THUMBNAIL-RECOMMEND-PROTOCOL.md) — given to the
# VLM so classification is consistent with the rest of the packaging stack.
OPERATIONS = [
    "COMPRESSION", "TITLE_REPETITION", "MECHANISM_REFRAME", "VISUAL_ANSWER",
    "NO_OVERLAY", "LOCATION_PROOF", "AESTHETIC_HOOK",
]

TAG_INSTRUCTIONS = f"""You are classifying ONE YouTube thumbnail for a packaging study.
Return ONLY a single JSON object, no prose, no markdown fences. Schema:

{{
  "overlay_text": "<verbatim text burned into the thumbnail, or empty string>",
  "overlay_words": <integer word count of overlay_text>,
  "framing": "<one of: declarative | question | label | none>",
  "face": <true if a human face is a prominent element, else false>,
  "map": <true if a geographic map is a prominent element, else false>,
  "dominant_colors": ["<color>", "<color>"],
  "subject": "<<=8 word description of the main visual>",
  "operation": "<best-fit ONE of: {', '.join(OPERATIONS)}>"
}}

Operation definitions:
- COMPRESSION: one number/word/phrase slammed large as the hero.
- TITLE_REPETITION: overlay just restates the video title.
- MECHANISM_REFRAME: overlay reframes the topic to a mechanism/cause.
- VISUAL_ANSWER: the image itself answers the question (data, proof, contrast).
- NO_OVERLAY: no meaningful text overlay at all.
- LOCATION_PROOF: a specific place/document shown as evidence.
- AESTHETIC_HOOK: mood/cinematic styling carries it, text secondary.
Pick the single closest fit. Output the JSON object only."""


def search_serp(queries: List[str], top_n: int) -> List[Dict]:
    """Dedup union of SERP results across queries, sorted by view count desc."""
    import scrapetube

    def views_of(v: Dict) -> int:
        try:
            txt = v["viewCountText"]["simpleText"]
            return int("".join(c for c in txt if c.isdigit()) or 0)
        except (KeyError, TypeError, ValueError):
            return 0

    seen: Dict[str, Dict] = {}
    for q in queries:
        try:
            for v in scrapetube.get_search(q, limit=12):
                vid = v["videoId"]
                if vid in seen:
                    continue
                title = "".join(
                    r.get("text", "") for r in v.get("title", {}).get("runs", [])
                )
                channel = ""
                try:
                    channel = v["ownerText"]["runs"][0]["text"]
                except (KeyError, IndexError, TypeError):
                    pass
                seen[vid] = {"id": vid, "title": title, "channel": channel,
                             "views": views_of(v)}
        except Exception as e:  # scrapetube schema drift / network
            logger.warning("search '%s' failed: %s", q, e)
    ranked = sorted(seen.values(), key=lambda x: -x["views"])
    return ranked[:top_n]


def _extract_json(raw: str) -> Optional[Dict]:
    """Pull the first {...} JSON object out of a noisy Gemini stdout."""
    start, end = raw.find("{"), raw.rfind("}")
    if start == -1 or end == -1 or end <= start:
        return None
    try:
        return json.loads(raw[start:end + 1])
    except json.JSONDecodeError:
        return None


def tag_thumbnail(img: Path, retries: int = 1) -> Optional[Dict]:
    """Tag one thumbnail via Gemini Flash vision. Returns parsed dict or None."""
    img_posix = img.as_posix()
    # Invoke through bash so `gemini` resolves the same way the /gemini command
    # proves it does on this machine; instructions on stdin, image ref in -p.
    cmd = f'gemini -m {GEMINI_MODEL} -p "@{img_posix}" --yolo -o text'
    for attempt in range(retries + 1):
        try:
            proc = subprocess.run(
                ["bash", "-lc", cmd],
                input=TAG_INSTRUCTIONS,
                capture_output=True, text=True, timeout=150,
            )
        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            logger.warning("gemini call failed for %s: %s", img.name, e)
            continue
        parsed = _extract_json(proc.stdout)
        if parsed:
            return parsed
        logger.warning("unparseable tag for %s (attempt %d): %s",
                       img.name, attempt + 1, proc.stdout[:160])
    return None


def _pct(n: int, total: int) -> str:
    return f"{(100 * n / total):.0f}%" if total else "0%"


def _aggregate(records: List[Dict]) -> Dict:
    """Shelf composition stats from a study's tagged records (shared by study + synthesize)."""
    tagged = [r for r in records if r.get("tags")]
    n = len(tagged)
    ops = Counter(r["tags"].get("operation", "?") for r in tagged)
    return {
        "n": n,
        "faces": sum(1 for r in tagged if r["tags"].get("face")),
        "maps": sum(1 for r in tagged if r["tags"].get("map")),
        "framings": Counter(r["tags"].get("framing", "none") for r in tagged),
        "ops": ops,
        "colors": Counter(
            c.lower() for r in tagged for c in (r["tags"].get("dominant_colors") or [])
        ),
        "avg_words": (sum(r["tags"].get("overlay_words", 0) for r in tagged) / n) if n else 0,
        "absent_ops": [op for op in OPERATIONS if op not in ops],
    }


def build_study(slug: str, records: List[Dict]) -> str:
    """records: each has id/title/channel/views + 'tags' dict (or None)."""
    a = _aggregate(records)
    n = a["n"]
    faces, maps = a["faces"], a["maps"]
    framings, ops, colors = a["framings"], a["ops"], a["colors"]
    avg_words, absent_ops = a["avg_words"], a["absent_ops"]

    lines = [
        f"# SERP Thumbnail Study — {slug}",
        "",
        f"**Generated:** {date.today().isoformat()}  ",
        f"**Method:** scrapetube SERP → top {len(records)} by views → Gemini Flash vision tags  ",
        f"**Tagged:** {n}/{len(records)}",
        "",
        "## Shelf composition",
        "",
        f"- **Face present:** {faces}/{n} ({_pct(faces, n)})",
        f"- **Map present:** {maps}/{n} ({_pct(maps, n)})",
        f"- **Framing:** " + ", ".join(f"{k} {v}" for k, v in framings.most_common()),
        f"- **Operations:** " + ", ".join(f"{k} {v}" for k, v in ops.most_common()),
        f"- **Avg overlay words:** {avg_words:.1f}",
        f"- **Color palette:** " + ", ".join(f"{k}({v})" for k, v in colors.most_common(6)),
        "",
        "## Whitespace (operations ABSENT from this shelf — attack here)",
        "",
        ("- " + ", ".join(absent_ops)) if absent_ops else "- none — shelf covers every operation; differentiate on subject/color instead.",
        "",
        "## Per-thumbnail tags",
        "",
        "| Views | Channel | Op | Face | Map | Framing | Words | Overlay text | Subject |",
        "|------:|---------|----|:----:|:---:|---------|------:|--------------|---------|",
    ]
    for r in records:
        t = r.get("tags")
        if not t:
            lines.append(f"| {r['views']:,} | {r['channel'][:18]} | — | — | — | — | — | (tag failed) | — |")
            continue
        lines.append(
            f"| {r['views']:,} | {r['channel'][:18]} | {t.get('operation','?')} | "
            f"{'Y' if t.get('face') else '·'} | {'Y' if t.get('map') else '·'} | "
            f"{t.get('framing','?')} | {t.get('overlay_words',0)} | "
            f"{(t.get('overlay_text') or '')[:40]} | {(t.get('subject') or '')[:34]} |"
        )
    lines += ["", "## Video IDs", "`" + ",".join(r["id"] for r in records) + "`", ""]
    return "\n".join(lines)


def synthesize(studies_dir: Path) -> str:
    """Read all study JSONs, detect DURABLE cross-topic patterns, write an approval
    proposal. Never writes the notebook — that stays a gated Claude action.

    A pattern is 'durable' only if it recurs across >= half the studies (min 2).
    Per-topic snapshots are deliberately NOT promoted (staleness + channel-authority
    confound); only patterns that hold across many shelves are candidates."""
    import glob
    from math import ceil

    files = sorted(glob.glob(str(studies_dir / "*.json")))
    studies = []
    for f in files:
        try:
            records = json.loads(Path(f).read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as e:
            logger.warning("skip %s: %s", f, e)
            continue
        slug = Path(f).stem.rsplit("-", 3)[0]  # strip trailing -YYYY-MM-DD
        agg = _aggregate(records)
        if agg["n"]:
            studies.append((slug, agg))
    N = len(studies)
    if N == 0:
        raise SystemExit(f"No study JSONs in {studies_dir} — run some --query studies first.")

    threshold = max(2, ceil(N / 2))
    conf = "LOW (thin sample)" if N < 3 else ("MEDIUM" if N < 6 else "HIGH")
    candidates: List[Dict] = []

    def add(pattern: str, hits: List[str], note: str):
        candidates.append({"pattern": pattern, "hits": hits, "note": note})

    # 1. Face-heavy shelves -> no-face is a durable break (matches HvH 0%-face niche)
    face_hits = [f"{s} {_pct(a['faces'], a['n'])}" for s, a in studies if a["faces"] / a["n"] >= 0.40]
    if len(face_hits) >= threshold:
        add("Shelves are face-heavy → NO-FACE is a durable break.",
            face_hits, "Reinforces the channel's existing 0%-face niche rule. Strong, low-risk.")

    # 2. Question-framing shelves -> declarative is a durable break
    q_hits = [f"{s} {_pct(a['framings'].get('question', 0), a['n'])}" for s, a in studies
              if a["framings"].get("question", 0) / a["n"] >= 0.35]
    if len(q_hits) >= threshold:
        add("Shelves skew question-framed → DECLARATIVE overlay is a durable break.",
            q_hits, "Matches channel data: question titles -36% CTR. Cross-validates the rule from the visual side.")

    # 3. Chronically-absent operations -> durable whitespace
    absent_counter = Counter()
    for s, a in studies:
        for op in a["absent_ops"]:
            absent_counter[op] += 1
    for op, c in absent_counter.most_common():
        if c >= threshold:
            hits = [s for s, a in studies if op in a["absent_ops"]]
            add(f"Operation {op} is chronically absent ({c}/{N} shelves) → durable whitespace.",
                hits, "An operation almost no competitor uses across topics — a repeatable differentiation lever, not a one-off.")

    # 4. Recurring dominant color -> off-palette is a durable break
    color_studies = Counter()
    for s, a in studies:
        for col, _ in a["colors"].most_common(2):
            color_studies[col] += 1
    for col, c in color_studies.most_common(3):
        if c >= threshold:
            add(f"'{col}' dominates {c}/{N} shelves → an off-palette (high-contrast non-{col}) thumb is a durable break.",
                [s for s, a in studies if col in dict(a["colors"].most_common(2))],
                "Color is a fast pre-attentive differentiator; consistent skew = reliable lever.")

    today = date.today().isoformat()
    lines = [
        f"# SERP Shelf Meta-Patterns — Synthesis Proposal ({today})",
        "",
        f"**Studies analyzed:** {N} ({', '.join(s for s, _ in studies)})  ",
        f"**Recurrence threshold:** pattern must hold in ≥ {threshold}/{N} shelves  ",
        f"**Confidence ceiling:** {conf}",
        "",
        "> These are DURABLE cross-topic candidates only. Per-topic snapshots were excluded by design",
        "> (staleness + SERP-ranking is confounded by channel authority, so it is NOT a 'what wins' signal).",
        "> **Nothing here is written to the notebook automatically.** Approve below, then Claude patches",
        "> the Packaging Intelligence notebook via `note_create`.",
        "",
        "## Candidate durable patterns",
        "",
    ]
    if not candidates:
        lines.append(f"_None cleared the ≥{threshold}/{N} recurrence bar. Add more studies and re-run._")
    for i, c in enumerate(candidates, 1):
        lines += [
            f"### {i}. {c['pattern']}",
            f"- **Evidence:** {', '.join(c['hits'])}",
            f"- **Why durable:** {c['note']}",
            "",
        ]
    lines += [
        "---",
        "## Notebook patch (GATED — do after user approval)",
        "",
        "Notebook: `Packaging Intelligence — History vs Hype` (id `98973069-020b-41f4-b3cd-795864b5cada`).",
        "On approval, Claude creates ONE dated note titled "
        f"`SERP shelf meta-patterns (synth {today})` containing only the APPROVED patterns above.",
        "Do NOT add per-topic study files as sources. Do NOT overwrite prior synthesis notes — append a new dated note.",
        "",
    ]
    proposal = studies_dir / f"_SYNTHESIS-PROPOSAL-{today}.md"
    proposal.write_text("\n".join(lines), encoding="utf-8")
    return str(proposal)


def run(slug: str, queries: List[str], ids: Optional[str], top_n: int,
        out: Optional[str]) -> str:
    if ids:
        records = [{"id": i.strip(), "title": "", "channel": "(supplied)", "views": 0}
                   for i in ids.split(",") if i.strip()][:top_n]
    else:
        records = search_serp(queries, top_n)
    if not records:
        raise SystemExit("No SERP results — check the query or scrapetube install.")

    paths = _download_serp([r["id"] for r in records])
    by_id = {p.stem: p for p in paths}
    for r in records:
        img = by_id.get(r["id"])
        r["tags"] = tag_thumbnail(img) if img else None
        status = "ok" if r["tags"] else "FAIL"
        logger.info("tagged %s (%s) -> %s", r["id"], r["channel"][:18], status)

    md = build_study(slug, records)
    out_path = Path(out) if out else Path("channel-data/serp-studies") / f"{slug}-{date.today().isoformat()}.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(md, encoding="utf-8")
    out_path.with_suffix(".json").write_text(
        json.dumps(records, indent=1, ensure_ascii=False), encoding="utf-8")
    return str(out_path)


def main():
    setup_logging()
    ap = argparse.ArgumentParser(description="SERP thumbnail study (auto-fetch + VLM-tag).")
    ap.add_argument("--slug", help="short topic slug for filenames (required unless --synthesize)")
    ap.add_argument("--query", action="append", default=[],
                    help="search query (repeatable). Omit if using --ids.")
    ap.add_argument("--ids", help="comma-separated video IDs (skip search)")
    ap.add_argument("--top", type=int, default=8, help="thumbnails to study (default 8)")
    ap.add_argument("--out", help="output .md path (default channel-data/serp-studies/)")
    ap.add_argument("--synthesize", action="store_true",
                    help="skip search; distill durable cross-topic patterns from all existing "
                         "studies into a gated notebook-patch proposal")
    ap.add_argument("--studies-dir", default="channel-data/serp-studies",
                    help="where study JSONs live (for --synthesize)")
    args = ap.parse_args()

    if args.synthesize:
        path = synthesize(Path(args.studies_dir))
        print(f"\nSynthesis proposal written: {path}")
        print("Review it, then have Claude patch the notebook (note_create) ONLY for approved patterns.")
        return

    if not args.query and not args.ids:
        ap.error("provide at least one --query or --ids (or use --synthesize)")
    if not args.slug:
        ap.error("--slug is required for a study run")
    path = run(args.slug, args.query, args.ids, args.top, args.out)
    print(f"\nStudy written: {path}")


if __name__ == "__main__":
    main()
