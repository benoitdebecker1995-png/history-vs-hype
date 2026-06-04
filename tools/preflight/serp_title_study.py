"""
SERP Title Study — classify a topic's live ranking *titles* and find the whitespace.

The text analog of serp_thumb_study.py. Reuses that module's quota-free scrapetube
fetch (which already returns title text we were throwing away) and title_scorer.py's
existing structural detectors. NO Gemini (titles are plain text) and NO scoring of
competitor titles on OUR CTR model (that would be the channel-authority confound —
a Vox title ranking high says nothing about whether its wording converts for us).

What it answers that title_scorer can't: title_scorer grades ONE candidate against a
frozen own-CTR snapshot + static niche aggregate. This shows what the ACTUAL ranking
shelf for THIS query looks like right now — which framings/keywords saturate it, and
which channel-winning patterns (the two-sentence "Claim. Evidence." formula, evidence
promises) are ABSENT, i.e. the positioning whitespace a new title should occupy.

Usage:
    python -m tools.preflight.serp_title_study --slug south-china-sea \
        --query "south china sea dispute" --query "nine dash line" --top 12

    # Reuse a prior thumb study's fetch instead of re-searching (if it was --query based):
    python -m tools.preflight.serp_title_study --slug gibraltar \
        --from-study channel-data/serp-studies/gibraltar-2026-06-03.json

Output: channel-data/serp-studies/titles/<slug>-<date>.md (+ .json)
"""

import argparse
import json
import re
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Dict, List, Optional

from tools.logging_config import get_logger, setup_logging
from tools.preflight.serp_thumb_study import search_serp
from tools.title_scorer import (
    detect_pattern, has_year, has_specific_number, has_evidence_promise,
    has_named_entity, has_controversy_frame,
)

logger = get_logger(__name__)

# the channel's top-retention formula: "[Claim sentence]. [Evidence sentence]."
TWO_SENTENCE = re.compile(r"(?<=[a-z]{3})\.\s+[A-Z]")

_STOP = {
    "the", "a", "an", "and", "or", "of", "to", "in", "on", "for", "is", "are",
    "was", "were", "why", "how", "what", "who", "this", "that", "its", "it",
    "with", "from", "by", "as", "at", "be", "explained", "documentary", "full",
    "history", "vs", "vs.", "part", "you", "your", "about", "into", "over",
}


def _classify(title: str) -> Dict:
    t = title.strip()
    return {
        "title": t,
        "len": len(t),
        "pattern": detect_pattern(t),
        "question": t.endswith("?"),
        "year": has_year(t),
        "colon": ":" in t,
        "number": has_specific_number(t),
        "evidence_promise": has_evidence_promise(t),
        "named_entity": has_named_entity(t),
        "controversy": has_controversy_frame(t),
        "two_sentence": bool(TWO_SENTENCE.search(t)),
    }


def _keywords(titles: List[str], query_terms: set, top: int = 12) -> List[tuple]:
    c = Counter()
    for t in titles:
        for w in re.findall(r"[a-z']+", t.lower()):
            if len(w) > 2 and w not in _STOP:
                c[w] += 1
    # query terms saturate trivially; keep them but mark separately downstream
    return c.most_common(top), query_terms


def _pct(n: int, total: int) -> str:
    return f"{(100 * n / total):.0f}%" if total else "0%"


def build_title_study(slug: str, records: List[Dict], query_terms: set) -> str:
    rows = [{**r, "tags": _classify(r["title"])} for r in records if r.get("title")]
    n = len(rows)
    if not n:
        return f"# SERP Title Study — {slug}\n\nNo titles found (the source fetch had empty titles — use --query)."

    def share(key):
        return sum(1 for r in rows if r["tags"].get(key)), n

    patterns = Counter(r["tags"]["pattern"] for r in rows)
    q, _ = share("question"); yr, _ = share("year"); col, _ = share("colon")
    num, _ = share("number"); ev, _ = share("evidence_promise")
    ne, _ = share("named_entity"); ctr, _ = share("controversy")
    two, _ = share("two_sentence")
    avg_len = sum(r["tags"]["len"] for r in rows) / n
    kw, _ = _keywords([r["title"] for r in rows], query_terms)

    # Whitespace / positioning levers: channel-winning patterns that are RARE on the
    # shelf (occupy them) and shelf saturations a new title should break.
    levers = []
    if two / n < 0.20:
        levers.append(f"**Two-sentence \"Claim. Evidence.\" is rare ({_pct(two,n)})** — the channel's top-retention formula is open whitespace here. Lead with it.")
    if ev / n < 0.20:
        levers.append(f"**Evidence-promise rare ({_pct(ev,n)})** — 'the documents / a court / the receipt' is a brand-differentiated lever the shelf isn't using.")
    if q / n >= 0.40:
        levers.append(f"**Shelf is question-heavy ({_pct(q,n)})** — a declarative title breaks the pattern (and questions cost the channel ~-36% CTR).")
    if yr / n >= 0.40:
        levers.append(f"**Years saturate the shelf ({_pct(yr,n)})** — a yearless title stands out (and dodges the -46% year penalty).")
    if ne / n >= 0.70:
        levers.append(f"**Named entities everywhere ({_pct(ne,n)})** — entity alone won't differentiate; carry the mechanism/consequence instead.")
    if not levers:
        levers.append("No strong structural whitespace — differentiate on the specific claim/keyword angle, not title structure.")

    lines = [
        f"# SERP Title Study — {slug}",
        "",
        f"**Generated:** {date.today().isoformat()}  ",
        f"**Method:** scrapetube SERP → top {n} by views → title_scorer structural detectors (no Gemini, no CTR scoring of competitors)",
        "",
        "## Shelf structure",
        "",
        f"- **Patterns:** " + ", ".join(f"{k} {v}" for k, v in patterns.most_common()),
        f"- **Question-framed:** {q}/{n} ({_pct(q,n)})",
        f"- **Has year:** {yr}/{n} ({_pct(yr,n)}) · **Has colon:** {col}/{n} ({_pct(col,n)}) · **Has number:** {num}/{n} ({_pct(num,n)})",
        f"- **Evidence-promise:** {ev}/{n} ({_pct(ev,n)}) · **Two-sentence Claim.Evidence.:** {two}/{n} ({_pct(two,n)})",
        f"- **Named entity:** {ne}/{n} ({_pct(ne,n)}) · **Controversy frame:** {ctr}/{n} ({_pct(ctr,n)})",
        f"- **Avg length:** {avg_len:.0f} chars",
        f"- **Saturated keywords:** " + ", ".join(f"{w}({c})" for w, c in kw),
        "",
        "## Positioning whitespace (where a new title should aim)",
        "",
    ]
    lines += [f"- {x}" for x in levers]
    lines += [
        "",
        "## Per-title classification",
        "",
        "| Views | Channel | Pattern | Q | Yr | Evid | 2-sent | Title |",
        "|------:|---------|---------|:-:|:--:|:----:|:------:|-------|",
    ]
    for r in rows:
        tg = r["tags"]
        lines.append(
            f"| {r['views']:,} | {r['channel'][:16]} | {tg['pattern']} | "
            f"{'Y' if tg['question'] else '·'} | {'Y' if tg['year'] else '·'} | "
            f"{'Y' if tg['evidence_promise'] else '·'} | {'Y' if tg['two_sentence'] else '·'} | "
            f"{r['title'][:52]} |"
        )
    lines += ["", "## Video IDs", "`" + ",".join(r["id"] for r in records) + "`", ""]
    return "\n".join(lines)


def run(slug: str, queries: List[str], from_study: Optional[str], top_n: int,
        out: Optional[str]) -> str:
    if from_study:
        records = json.loads(Path(from_study).read_text(encoding="utf-8"))[:top_n]
        if not any(r.get("title") for r in records):
            raise SystemExit(f"{from_study} has no title text (was it an --ids thumb study?). Use --query.")
        query_terms = set()
    else:
        records = search_serp(queries, top_n)
        query_terms = {w for q in queries for w in re.findall(r"[a-z']+", q.lower())}
    if not records:
        raise SystemExit("No SERP results — check the query or scrapetube install.")

    md = build_title_study(slug, records, query_terms)
    out_path = Path(out) if out else Path("channel-data/serp-studies/titles") / f"{slug}-{date.today().isoformat()}.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(md, encoding="utf-8")
    out_path.with_suffix(".json").write_text(
        json.dumps([{**r, "tags": _classify(r["title"])} for r in records if r.get("title")],
                   indent=1, ensure_ascii=False), encoding="utf-8")
    return str(out_path)


def main():
    setup_logging()
    ap = argparse.ArgumentParser(description="SERP title study (structural classification of the ranking shelf).")
    ap.add_argument("--slug", required=True, help="short topic slug for filenames")
    ap.add_argument("--query", action="append", default=[], help="search query (repeatable)")
    ap.add_argument("--from-study", help="reuse a prior thumb-study JSON's fetch (skip re-search)")
    ap.add_argument("--top", type=int, default=12, help="titles to study (default 12)")
    ap.add_argument("--out", help="output .md path (default channel-data/serp-studies/titles/)")
    args = ap.parse_args()
    if not args.query and not args.from_study:
        ap.error("provide at least one --query or --from-study")
    path = run(args.slug, args.query, args.from_study, args.top, args.out)
    print(f"\nTitle study written: {path}")


if __name__ == "__main__":
    main()
