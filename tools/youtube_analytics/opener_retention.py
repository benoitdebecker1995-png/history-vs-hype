"""
Opener ↔ retention link (the /opener diagnostic source).

Backfills the `opener_retention` table: for every published long-form video we
can match to an SRT, store the verbatim 0:00-0:30 narration, its classified hook
archetype, and the audience retention at ~30 seconds. The /opener skill queries
this — DIAGNOSTICALLY ONLY — to warn when an archetype has historically bled in
our own first 30 seconds. Per memory/feedback-channel-data-too-small.md, per-
archetype n is small, so this NEVER ranks hook types; niche-wide data does that.

Reuses (no new plumbing):
    - retention_analysis.build_srt_mapping / parse_srt   → video_id ↔ opener text
    - AnalyticsStore.retention_curve                      → bucketed retention
    - retention_by_topic.classify_topic                  → topic_type
    - hook_scorer._detect_hook_style                     → hook archetype

Usage:
    python -m tools.youtube_analytics.opener_retention            # backfill + summary
    python -m tools.youtube_analytics.opener_retention --show     # also print aggregates

    from tools.youtube_analytics.opener_retention import get_opener_diagnostic
    diag = get_opener_diagnostic(topic_type='territorial', hook_archetype='cold_fact')
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from tools.logging_config import get_logger
from tools.youtube_analytics.store import AnalyticsStore, ANALYTICS_DB
from tools.youtube_analytics.retention_analysis import build_srt_mapping, parse_srt
from tools.youtube_analytics.retention_by_topic import classify_topic

logger = get_logger(__name__)

OPENER_WINDOW_SECONDS = 30.0


# ---------------------------------------------------------------------------
# Curve math
# ---------------------------------------------------------------------------

def _retention_at_ratio(points: List[Dict[str, Any]], target_ratio: float) -> Optional[float]:
    """Linear-interpolate audience_watch_ratio at `target_ratio`.

    `points` must be sorted by elapsed_ratio ascending. Clamps to the curve
    endpoints when target falls outside the sampled range.
    """
    if not points:
        return None
    if target_ratio <= points[0]["elapsed_ratio"]:
        return points[0]["audience_watch_ratio"]
    if target_ratio >= points[-1]["elapsed_ratio"]:
        return points[-1]["audience_watch_ratio"]
    for i in range(1, len(points)):
        x1, x2 = points[i - 1]["elapsed_ratio"], points[i]["elapsed_ratio"]
        if x1 <= target_ratio <= x2:
            y1, y2 = points[i - 1]["audience_watch_ratio"], points[i]["audience_watch_ratio"]
            if x2 == x1:
                return y2
            frac = (target_ratio - x1) / (x2 - x1)
            return y1 + frac * (y2 - y1)
    return points[-1]["audience_watch_ratio"]


def _extract_opener_text(srt_path: Path, window: float = OPENER_WINDOW_SECONDS) -> str:
    """Return the verbatim narration spoken in the first `window` seconds."""
    segments = parse_srt(srt_path)
    texts = [s["text"] for s in segments if s["start_seconds"] < window]
    merged = " ".join(t.strip() for t in texts if t.strip())
    merged = " ".join(merged.split())  # collapse whitespace/newlines
    return merged[:1500]


def _classify_archetype(opener_text: str) -> str:
    """Classify the opener into a hook archetype (reuses hook_scorer)."""
    if not opener_text:
        return "unknown"
    from tools.research.hook_scorer import _detect_hook_style, _load_pattern_library
    return _detect_hook_style(opener_text, _load_pattern_library())


# ---------------------------------------------------------------------------
# Backfill
# ---------------------------------------------------------------------------

def backfill(db_path: Path = ANALYTICS_DB) -> Dict[str, int]:
    """(Re)build the opener_retention table from SRT + retention curves.

    Idempotent: upserts by video_id. Returns a small stats dict.
    """
    # Ensure the v3 table exists before the read-only store opens.
    from tools.youtube_analytics.growth_data import ensure_schema, _get_db
    conn = _get_db(db_path)
    ensure_schema(conn)
    conn.close()

    srt_mapping = build_srt_mapping()
    now = datetime.now(timezone.utc).isoformat()
    stats = {"written": 0, "no_srt": 0, "no_curve": 0, "no_duration": 0}

    with AnalyticsStore.open(db_path) as store:
        videos = store.videos(min_duration_seconds=121)
        for v in videos:
            vid = v["video_id"]
            duration = v.get("duration_seconds") or 0
            if duration <= 0:
                stats["no_duration"] += 1
                continue
            srt_path = srt_mapping.get(vid)
            if srt_path is None:
                stats["no_srt"] += 1
                continue
            points = store.retention_curve(vid)
            if len(points) < 2:
                stats["no_curve"] += 1
                continue

            opener_text = _extract_opener_text(srt_path)
            archetype = _classify_archetype(opener_text)
            topic = classify_topic(v["title"], v.get("topic_type") or "general")

            start_ret = points[0]["audience_watch_ratio"]
            ret_30 = _retention_at_ratio(points, OPENER_WINDOW_SECONDS / duration)
            intro_drop = (
                (start_ret - ret_30) / start_ret
                if (start_ret and ret_30 is not None and start_ret > 0)
                else None
            )

            store.upsert_opener_retention(
                video_id=vid,
                opener_text=opener_text,
                hook_archetype=archetype,
                first_30s_retention=ret_30,
                intro_drop_30s=intro_drop,
                topic_type=topic,
                published_at=v.get("published_at"),
                fetched_at=now,
            )
            stats["written"] += 1
        store.commit()

    logger.info("opener_retention backfill: %s", stats)
    return stats


# ---------------------------------------------------------------------------
# Diagnostic reader (called by /opener)
# ---------------------------------------------------------------------------

def get_opener_diagnostic(
    topic_type: Optional[str] = None,
    hook_archetype: Optional[str] = None,
    db_path: Path = ANALYTICS_DB,
) -> Dict[str, Any]:
    """Aggregate first-30s retention for a topic/archetype slice.

    Returns {n, avg_first_30s_retention, avg_intro_drop_30s, best, worst, rows}.
    DIAGNOSTIC ONLY — surfaces where our own openers bled; does not rank archetypes.
    """
    with AnalyticsStore.open(db_path) as store:
        rows = store.opener_rows(topic_type=topic_type, hook_archetype=hook_archetype)

    rets = [r["first_30s_retention"] for r in rows if r["first_30s_retention"] is not None]
    drops = [r["intro_drop_30s"] for r in rows if r["intro_drop_30s"] is not None]
    by_drop = sorted([r for r in rows if r["intro_drop_30s"] is not None],
                     key=lambda r: r["intro_drop_30s"])
    return {
        "n": len(rows),
        "avg_first_30s_retention": (sum(rets) / len(rets)) if rets else None,
        "avg_intro_drop_30s": (sum(drops) / len(drops)) if drops else None,
        "best": by_drop[:2],            # smallest drop first
        "worst": list(reversed(by_drop))[:2],
        "rows": rows,
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _print_summary(db_path: Path) -> None:
    with AnalyticsStore.open(db_path) as store:
        rows = store.opener_rows()
    by_type: Dict[str, List[float]] = {}
    by_arch: Dict[str, List[float]] = {}
    for r in rows:
        d = r["intro_drop_30s"]
        if d is None:
            continue
        by_type.setdefault(r["topic_type"] or "?", []).append(d)
        by_arch.setdefault(r["hook_archetype"] or "?", []).append(d)

    def _fmt(group: Dict[str, List[float]], label: str) -> None:
        print(f"\n  Avg first-30s intro-drop by {label} (lower = better):")
        for k, vals in sorted(group.items(), key=lambda kv: sum(kv[1]) / len(kv[1])):
            print(f"    {k:<14} n={len(vals):<3} drop={sum(vals)/len(vals):.1%}")

    print(f"\nopener_retention rows: {len(rows)}")
    _fmt(by_type, "topic_type")
    _fmt(by_arch, "hook_archetype")


def main() -> None:
    parser = argparse.ArgumentParser(description="Backfill opener_retention and show diagnostics.")
    parser.add_argument("--show", action="store_true", help="Print aggregate diagnostics after backfill.")
    parser.add_argument("--db", default=str(ANALYTICS_DB), help="Path to analytics.db")
    args = parser.parse_args()

    db_path = Path(args.db)
    stats = backfill(db_path)
    print(f"Backfill complete: {stats}")
    if args.show:
        _print_summary(db_path)


if __name__ == "__main__":
    main()
