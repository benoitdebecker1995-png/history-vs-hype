"""
Demand Checker — validates topic search demand before project creation.

Prevents producing videos on topics with zero search audience by checking
keyword search volume and comparable video performance from the database.

Usage:
    python -m tools.preflight.demand_checker "berlin conference africa"
    python -m tools.preflight.demand_checker "treaty of tordesillas"
    python -m tools.preflight.demand_checker "bermeja island mexico"
"""

import argparse
import sqlite3
import sys
from pathlib import Path
from typing import Dict, List, Tuple

from tools.logging_config import get_logger, setup_logging

logger = get_logger(__name__)

DB_PATH = str(Path(__file__).resolve().parent.parent / "discovery" / "keywords.db")

# Thresholds
GO_VOLUME = 1000
GO_VIEWS = 500
CAUTION_VOLUME = 200
STOP_VIEWS = 200
SIMILARITY_THRESHOLD = 0.4  # 40% word overlap


def _normalize(text: str) -> set:
    """Split text into lowercase word tokens, stripping short noise words."""
    stop = {"the", "of", "a", "an", "in", "on", "and", "is", "to", "for", "by"}
    return {w for w in text.lower().split() if len(w) > 1 and w not in stop}


def _word_overlap(tokens_a: set, tokens_b: set) -> float:
    """Return Jaccard-like overlap: intersection / min(len_a, len_b)."""
    if not tokens_a or not tokens_b:
        return 0.0
    intersection = tokens_a & tokens_b
    return len(intersection) / min(len(tokens_a), len(tokens_b))


def search_keywords(conn: sqlite3.Connection, query_tokens: set) -> List[Dict]:
    """Find keywords table rows matching any query token."""
    if not query_tokens:
        return []
    cur = conn.cursor()
    matches = []
    for token in query_tokens:
        cur.execute(
            "SELECT keyword, search_volume, competition_score "
            "FROM keywords WHERE LOWER(keyword) LIKE ?",
            (f"%{token}%",),
        )
        for row in cur.fetchall():
            kw_tokens = _normalize(row[0])
            overlap = _word_overlap(query_tokens, kw_tokens)
            if overlap >= SIMILARITY_THRESHOLD:
                matches.append({
                    "keyword": row[0],
                    "search_volume": row[1],
                    "competition": row[2],
                    "overlap": round(overlap, 2),
                })
    # Deduplicate by keyword
    seen = set()
    unique = []
    for m in matches:
        if m["keyword"] not in seen:
            seen.add(m["keyword"])
            unique.append(m)
    return sorted(unique, key=lambda x: x["search_volume"] or 0, reverse=True)


def search_comparable_videos(
    conn: sqlite3.Connection, query_tokens: set
) -> List[Dict]:
    """Find video_performance rows with similar titles."""
    cur = conn.cursor()
    try:
        cur.execute("""SELECT title, views, topic_type FROM video_performance
            WHERE title NOT LIKE '%#%'
            AND COALESCE(avg_view_duration_seconds, 999) >= 60""")
    except sqlite3.OperationalError:
        logger.warning("video_performance table not found")
        return []

    matches = []
    for row in cur.fetchall():
        title = row[0] or ""
        title_tokens = _normalize(title)
        overlap = _word_overlap(query_tokens, title_tokens)
        if overlap >= SIMILARITY_THRESHOLD:
            matches.append({
                "title": title,
                "views": row[1] or 0,
                "topic_type": row[2],
                "overlap": round(overlap, 2),
            })
    return sorted(matches, key=lambda x: x["views"], reverse=True)


def evaluate(
    keyword_matches: List[Dict], video_matches: List[Dict]
) -> Tuple[str, List[str]]:
    """Return (verdict, reasons) based on demand data.

    Verdicts: GO, CAUTION, STOP.
    """
    reasons: List[str] = []

    # Best search volume from keyword matches
    best_volume = 0
    best_kw = None
    for m in keyword_matches:
        vol = m["search_volume"] or 0
        if vol > best_volume:
            best_volume = vol
            best_kw = m

    # Best views from comparable videos
    best_views = 0
    best_video = None
    for v in video_matches:
        if v["views"] > best_views:
            best_views = v["views"]
            best_video = v

    # Decision logic
    if best_volume >= GO_VOLUME:
        reasons.append(
            f"Keyword '{best_kw['keyword']}' has {best_volume:,}/month search volume"
        )
        verdict = "GO"
    elif best_views >= GO_VIEWS:
        reasons.append(
            f"Similar video '{best_video['title']}' got {best_views:,} views"
        )
        verdict = "GO"
    elif best_volume >= CAUTION_VOLUME:
        reasons.append(
            f"Keyword '{best_kw['keyword']}' has moderate volume ({best_volume:,}/month)"
        )
        verdict = "CAUTION"
    elif not keyword_matches and not video_matches:
        reasons.append("No matching keywords or comparable videos found in database")
        verdict = "CAUTION"
    elif best_views >= STOP_VIEWS:
        reasons.append(
            f"Similar video '{best_video['title']}' got {best_views:,} views (marginal)"
        )
        verdict = "CAUTION"
    else:
        if best_volume > 0:
            reasons.append(
                f"Best keyword volume is only {best_volume:,}/month (threshold: {CAUTION_VOLUME:,})"
            )
        else:
            reasons.append("No keyword search volume data found")
        if best_views > 0:
            reasons.append(
                f"Best comparable video got only {best_views:,} views (threshold: {STOP_VIEWS:,})"
            )
        else:
            reasons.append("No comparable video performance data")
        verdict = "STOP"

    return verdict, reasons


def _verdict_decoration(verdict: str) -> str:
    colors = {"GO": "\033[32m", "CAUTION": "\033[33m", "STOP": "\033[31m"}
    reset = "\033[0m"
    if sys.stderr.isatty():
        return f"{colors.get(verdict, '')}{verdict}{reset}"
    return verdict


def run(topic: str) -> Dict:
    """Run demand check and return structured result."""
    query_tokens = _normalize(topic)
    logger.debug("Query tokens: %s", query_tokens)

    if not Path(DB_PATH).exists():
        return {"error": f"Database not found: {DB_PATH}"}

    conn = sqlite3.connect(DB_PATH)
    try:
        keyword_matches = search_keywords(conn, query_tokens)
        video_matches = search_comparable_videos(conn, query_tokens)
        verdict, reasons = evaluate(keyword_matches, video_matches)
    finally:
        conn.close()

    return {
        "topic": topic,
        "verdict": verdict,
        "reasons": reasons,
        "keyword_matches": keyword_matches[:10],
        "video_matches": video_matches[:10],
    }


def print_report(result: Dict) -> None:
    """Print human-readable demand report to stdout."""
    if "error" in result:
        print(f"ERROR: {result['error']}")
        return

    verdict = result["verdict"]
    print(f"\n{'=' * 60}")
    print(f"  DEMAND CHECK: {result['topic']}")
    print(f"{'=' * 60}")
    print(f"\n  Verdict: {_verdict_decoration(verdict)}")

    print(f"\n  Reasoning:")
    for r in result["reasons"]:
        print(f"    - {r}")

    if result["keyword_matches"]:
        print(f"\n  Keyword Matches ({len(result['keyword_matches'])}):")
        for m in result["keyword_matches"][:5]:
            vol = f"{m['search_volume']:,}/mo" if m["search_volume"] else "N/A"
            comp = f"{m['competition']:.0f}" if m["competition"] else "N/A"
            print(f"    {m['keyword']:40s}  vol={vol:>10s}  comp={comp:>4s}  overlap={m['overlap']}")

    if result["video_matches"]:
        print(f"\n  Comparable Videos ({len(result['video_matches'])}):")
        for v in result["video_matches"][:5]:
            print(f"    {v['title'][:50]:50s}  views={v['views']:>7,}  type={v['topic_type'] or '?'}")

    if not result["keyword_matches"] and not result["video_matches"]:
        print("\n  No data found. Consider running keyword discovery first.")

    print(f"\n{'=' * 60}\n")


def main():
    parser = argparse.ArgumentParser(
        description="Check topic search demand before creating a video project"
    )
    parser.add_argument("topic", help="Topic name or keywords to check")
    parser.add_argument("-v", "--verbose", action="store_true", help="Debug logging")
    parser.add_argument("-q", "--quiet", action="store_true", help="Errors only")
    args = parser.parse_args()

    setup_logging(args.verbose, args.quiet)
    result = run(args.topic)
    print_report(result)

    # Exit code: 0=GO, 1=CAUTION, 2=STOP
    exit_codes = {"GO": 0, "CAUTION": 1, "STOP": 2}
    sys.exit(exit_codes.get(result.get("verdict", "STOP"), 2))


if __name__ == "__main__":
    main()
