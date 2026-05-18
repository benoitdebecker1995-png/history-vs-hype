"""Cross-store views — composing analytics.db and keywords.db.

The two stores stay separate (see ADR-0004), but many analyses need them
merged: video metadata from analytics.db, latest CTR snapshot from
keywords.db, and search-traffic share computed from traffic_sources.

This module is the *one* place that merge lives. Callers (title_intelligence,
traffic_analysis, ctr_by_source_analysis) consume the merged view and don't
touch either store directly.
"""
from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional

from tools.logging_config import get_logger

from tools.youtube_analytics.store import ANALYTICS_DB, AnalyticsStore

logger = get_logger(__name__)

_REPO_ROOT = Path(__file__).resolve().parents[2]
KEYWORDS_DB = _REPO_ROOT / "tools" / "discovery" / "keywords.db"


def videos_with_ctr_and_traffic(
    *,
    min_views: int = 11,
    analytics_db: Path = ANALYTICS_DB,
    keywords_db: Path = KEYWORDS_DB,
) -> List[Dict[str, Any]]:
    """Return videos enriched with latest CTR snapshot and search-traffic share.

    Each row carries the full analytics.db video columns plus:
      - search_views: views attributed to YT_SEARCH (int, 0 if none)
      - total_traffic_views: sum of all traffic_sources views (int, 0 if none)
      - search_traffic_pct: search_views / total_traffic_views * 100, rounded to 0.1
      - ctr_percent: overwritten with latest snapshot from keywords.db when available
      - impressions: overwritten with snapshot impressions when CTR is taken from keywords.db

    If keywords.db is unreadable, the function still returns a result — videos
    keep whatever ctr_percent/impressions analytics.db has.

    Args:
        min_views: lower bound on `videos.views` (inclusive). Default 11
            preserves the old `WHERE views > 10` filter byte-for-byte.
        analytics_db: override for tests.
        keywords_db: override for tests.
    """
    with AnalyticsStore.open(analytics_db) as store:
        videos: Dict[str, Dict[str, Any]] = {}
        for v in store.videos(min_views=min_views, order_by="views"):
            v["search_views"] = 0
            v["total_traffic_views"] = 0
            videos[v["video_id"]] = v

        for row in store.traffic_sources():
            vid = row["video_id"]
            if vid not in videos:
                continue
            videos[vid]["total_traffic_views"] += row["views"] or 0
            if row["source_type"] == "YT_SEARCH":
                videos[vid]["search_views"] = row["views"] or 0

    _apply_latest_ctr(videos, keywords_db)

    result: List[Dict[str, Any]] = []
    for v in videos.values():
        total = v.get("total_traffic_views", 0) or 0
        search = v.get("search_views", 0) or 0
        v["search_traffic_pct"] = round((search / total * 100) if total > 0 else 0, 1)
        result.append(v)
    return result


def _apply_latest_ctr(videos: Dict[str, Dict[str, Any]], keywords_db: Path) -> None:
    """Mutate `videos` in place with the latest ctr_snapshot per video.

    Silently degrades if keywords.db is missing or unreadable — callers still
    get analytics.db CTR values.
    """
    if not Path(keywords_db).exists():
        logger.warning("keywords.db not found at %s; skipping CTR merge", keywords_db)
        return

    try:
        conn = sqlite3.connect(str(keywords_db))
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            """
            SELECT video_id, ctr_percent, impression_count
            FROM ctr_snapshots
            WHERE ctr_percent > 0
            GROUP BY video_id
            HAVING snapshot_date = MAX(snapshot_date)
            """
        ).fetchall()
        conn.close()
    except sqlite3.Error as e:
        logger.warning("Could not read keywords.db CTR data: %s", e)
        return

    for row in rows:
        vid = row["video_id"]
        if vid in videos:
            videos[vid]["ctr_percent"] = row["ctr_percent"]
            videos[vid]["impressions"] = row["impression_count"]
