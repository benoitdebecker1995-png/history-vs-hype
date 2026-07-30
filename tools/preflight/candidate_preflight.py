"""Candidate pre-flight — have we already done this?

WHY THIS EXISTS
---------------
`.claude/PROMPTS/blind-next-video-discovery.md` has mandated a collision check against published
titles and project folders since it was written. On 2026-07-30 that mandate was ignored twice in
one session: a "NATO promised not to expand" video was proposed and screened at length before the
owner pointed out he had **already published it** (`499YLd1BHZ4`, 2025-09-10), and earlier the same
session a candidate was pushed without checking `_BACKLOG/`.

A rule that must bind goes in code, not prose (ADR-0012). Prose in a brief is a rule that binds
only when the reader happens to remember it.

WHAT IT CHECKS
--------------
  PUBLISHED      analytics.db video titles        -> HARD collision, exit non-zero
  IN_PRODUCTION  video-projects/_IN_PRODUCTION/   -> FLAG (eligible on merit, but say so loudly)
  READY_TO_FILM  video-projects/_READY_TO_FILM/   -> FLAG
  BACKLOG        video-projects/_BACKLOG/         -> FLAG
  ARCHIVED       video-projects/_ARCHIVED/        -> FLAG

Per the discovery brief, an existing project is a FLAG, not a kill — banked work lowers cost. A
published title is a hard stop unless deliberately overridden.

Read-side: never raises. Returns {'error': ...} on failure.
"""

from __future__ import annotations

import argparse
import re
import sqlite3
import sys
from pathlib import Path
from typing import Dict, List, Optional

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from tools.logging_config import get_logger, setup_logging  # noqa: E402

logger = get_logger(__name__)

REPO = Path(__file__).resolve().parents[2]
ANALYTICS_DB = REPO / "tools" / "youtube_analytics" / "analytics.db"
PROJECTS = REPO / "video-projects"

LIFECYCLE = {
    "_IN_PRODUCTION": "IN_PRODUCTION",
    "_READY_TO_FILM": "READY_TO_FILM",
    "_BACKLOG": "BACKLOG",
    "_ARCHIVED": "ARCHIVED",
}

_STOP = {
    "the", "a", "an", "of", "and", "or", "in", "on", "to", "for", "is", "was", "did",
    "why", "how", "what", "who", "that", "this", "it", "its", "at", "by", "with",
    "not", "but", "from", "as", "are", "were", "be", "been", "his", "her", "their",
}


def _terms(topic: str) -> List[str]:
    """Content words from a topic string, lowercased, stopwords dropped."""
    words = re.findall(r"[a-z0-9']+", topic.lower())
    return [w for w in words if w not in _STOP and len(w) > 2]


def _match(terms: List[str], haystack: str) -> List[str]:
    h = haystack.lower()
    return [t for t in terms if t in h]


def check(topic: str, min_terms: int = 2, db_path: Optional[str] = None) -> Dict:
    """Check a candidate topic for prior art. Never raises.

    min_terms: how many content words must co-occur to count as a collision.
    """
    terms = _terms(topic)
    if not terms:
        return {"error": f"no usable search terms in topic: {topic!r}"}
    need = min(min_terms, len(terms))

    collisions: List[Dict] = []

    # --- published titles -------------------------------------------------
    db = Path(db_path) if db_path else ANALYTICS_DB
    if not db.exists():
        collisions.append(
            {"kind": "WARN", "where": "analytics.db", "detail": f"missing at {db}"}
        )
    else:
        try:
            conn = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
            try:
                rows = conn.execute(
                    "SELECT video_id, title, published_at FROM videos WHERE title IS NOT NULL"
                ).fetchall()
            finally:
                conn.close()
            for vid, title, pub in rows:
                hits = _match(terms, title or "")
                if len(hits) >= need:
                    collisions.append(
                        {
                            "kind": "PUBLISHED",
                            "where": vid,
                            "detail": f"{title}  ({(pub or '?')[:10]})",
                            "matched": hits,
                        }
                    )
        except sqlite3.Error as exc:
            collisions.append(
                {"kind": "WARN", "where": "analytics.db", "detail": f"query failed: {exc}"}
            )

    # --- project folders --------------------------------------------------
    for folder, kind in LIFECYCLE.items():
        base = PROJECTS / folder
        if not base.exists():
            continue
        for p in sorted(base.rglob("*")):
            if not p.is_dir():
                continue
            # only look at project-level dirs (direct children, plus _ARCHIVED/published/*)
            if p.parent != base and p.parent.name not in ("published",):
                continue
            hits = _match(terms, p.name)
            if len(hits) >= need:
                collisions.append(
                    {"kind": kind, "where": str(p.relative_to(REPO)), "detail": p.name,
                     "matched": hits}
                )

    hard = [c for c in collisions if c["kind"] == "PUBLISHED"]
    flags = [c for c in collisions if c["kind"] not in ("PUBLISHED", "WARN")]
    warns = [c for c in collisions if c["kind"] == "WARN"]

    return {
        "topic": topic,
        "terms": terms,
        "min_terms": need,
        "collisions": collisions,
        "verdict": "COLLISION" if hard else ("FLAG" if flags else "CLEAR"),
        "hard": len(hard),
        "flags": len(flags),
        "warnings": len(warns),
    }


def format_report(res: Dict) -> str:
    if "error" in res:
        return f"ERROR: {res['error']}"
    out = [
        "=" * 72,
        "  CANDIDATE PRE-FLIGHT  (have we already done this?)",
        "=" * 72,
        f"  topic: {res['topic']}",
        f"  terms: {', '.join(res['terms'])}  (>= {res['min_terms']} must co-occur)",
    ]
    if not res["collisions"]:
        out.append("\n  no prior art found")
    else:
        out.append("")
        for c in res["collisions"]:
            mark = "!!" if c["kind"] == "PUBLISHED" else ("??" if c["kind"] == "WARN" else " *")
            out.append(f"  {mark} [{c['kind']}] {c['detail']}")
            out.append(f"       {c['where']}")
    out.append(f"\n  VERDICT: {res['verdict']}")
    if res["verdict"] == "COLLISION":
        out.append("  -> ALREADY PUBLISHED. Do not propose without an explicit override.")
    elif res["verdict"] == "FLAG":
        out.append("  -> existing project(s). Eligible on merit, but SAY SO when proposing.")
    out.append("=" * 72)
    return "\n".join(out)


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(
        description="Candidate pre-flight — collision check before proposing a video (ADR-0021)",
        epilog=(
            "Examples:\n"
            '  python -m tools.preflight.candidate_preflight "NATO promised not to expand"\n'
            '  python -m tools.preflight.candidate_preflight "Bengal famine Churchill" --min-terms 2\n'
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("topic", help="candidate topic or working title")
    ap.add_argument("--min-terms", type=int, default=2, help="content words that must co-occur")
    ap.add_argument("--db", help="override analytics.db path")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("-v", "--verbose", action="store_true")
    g.add_argument("-q", "--quiet", action="store_true")
    args = ap.parse_args(argv)
    setup_logging(args.verbose, args.quiet)

    res = check(args.topic, min_terms=args.min_terms, db_path=args.db)
    print(format_report(res))
    if "error" in res:
        return 2
    return 1 if res["verdict"] == "COLLISION" else 0


if __name__ == "__main__":
    raise SystemExit(main())
