"""Cross-store views — composing analytics.db video + traffic data.

The two stores stay separate (see ADR-0004). CTR/impressions now live in
analytics.db.videos, populated from keywords.db.ctr_snapshots by the growth_data
bridge (deterministic, genuine-zero-preserving, freshness-stamped). This module
merges that cached CTR with search-traffic share computed from traffic_sources.

⚠ Historical note (2026-07-22): this module used to RE-READ keywords.db at read
time via `_apply_latest_ctr` and overwrite the CTR here. That override had two
bugs — `WHERE ctr_percent > 0` dropped genuine-zero-CTR videos, and
`GROUP BY … HAVING MAX(snapshot_date)` returned an arbitrary row's ctr/impressions
under SQLite's bare-column rule. It was retired: the bridge now writes the correct
value into `videos.ctr_percent`/`impressions`/`ctr_as_of`, so every consumer reads
one source. Do NOT reinstate a keywords.db read here.

This module is the *one* place the traffic merge lives. Callers
(title_intelligence, traffic_analysis, ctr_by_source_analysis) consume the merged
view and don't touch either store directly.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

from tools.logging_config import get_logger

from tools.youtube_analytics.store import ANALYTICS_DB, AnalyticsStore

logger = get_logger(__name__)


def videos_with_ctr_and_traffic(
    *,
    min_views: int = 11,
    analytics_db: Path = ANALYTICS_DB,
) -> List[Dict[str, Any]]:
    """Return videos enriched with cached CTR and search-traffic share.

    Each row carries the full analytics.db video columns (including the cached
    ctr_percent/impressions/ctr_as_of written by the growth_data bridge) plus:
      - search_views: views attributed to YT_SEARCH (int, 0 if none)
      - total_traffic_views: sum of all traffic_sources views (int, 0 if none)
      - search_traffic_pct: search_views / total_traffic_views * 100, rounded to 0.1

    CTR is NOT re-overlaid from keywords.db (see module docstring) — it is the
    value analytics.db holds, which is the corrected bridge output.

    Args:
        min_views: lower bound on `videos.views` (inclusive). Default 11
            preserves the old `WHERE views > 10` filter byte-for-byte.
        analytics_db: override for tests.
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

    result: List[Dict[str, Any]] = []
    for v in videos.values():
        total = v.get("total_traffic_views", 0) or 0
        search = v.get("search_views", 0) or 0
        v["search_traffic_pct"] = round((search / total * 100) if total > 0 else 0, 1)
        result.append(v)
    return result
