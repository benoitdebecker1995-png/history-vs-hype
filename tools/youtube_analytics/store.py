"""AnalyticsStore — single seam over analytics.db (videos, traffic_sources, daily_channel).

Peer to tools.discovery.keyword_store.KeywordStore. Hides connection lifecycle,
schema, and SQL from analysis scripts.

Reads are the primary surface. Writes have been growing in incrementally —
see ADR-0004 stage 3. Currently exposed: upsert_traffic_source(). Video and
daily-channel writers (growth_data.py:store_videos / store_daily_metrics)
still keep their own connections until their dataclass shapes are designed.

Usage:
    from tools.youtube_analytics.store import AnalyticsStore

    # one-shot scripts (the common case)
    with AnalyticsStore.open() as store:
        videos = store.videos(min_duration_seconds=60)

    # writes — caller commits explicitly
    with AnalyticsStore.open() as store:
        for v, s in traffic_rows:
            store.upsert_traffic_source(video_id=v, source_type=s, ...)
        store.commit()

    # tests
    store = AnalyticsStore(sqlite3.connect(":memory:"))

See ADR-0004 (docs/adr/0004-two-store-split-analytics-vs-keywords.md) for why
this lives alongside KeywordStore rather than merging.
"""
from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

from tools.logging_config import get_logger

logger = get_logger(__name__)

ANALYTICS_DB = Path(__file__).parent / "analytics.db"


def _open_conn(db_path: Path) -> sqlite3.Connection:
    """Open analytics.db with the project's standard pragmas + row_factory."""
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


class AnalyticsStore:
    """Read-only accessor for analytics.db.

    Caller chooses lifecycle:
      - `AnalyticsStore.open()` as a context manager (one-shot scripts)
      - `AnalyticsStore(conn)` for DI in tests or long-lived workflows
    """

    def __init__(self, conn: sqlite3.Connection) -> None:
        self._conn = conn
        # Ensure dict-style access even if caller forgot to set row_factory.
        if self._conn.row_factory is not sqlite3.Row:
            self._conn.row_factory = sqlite3.Row

    @classmethod
    def open(cls, db_path: Path = ANALYTICS_DB) -> "AnalyticsStore":
        if not Path(db_path).exists():
            raise FileNotFoundError(f"analytics.db not found at {db_path}")
        return cls(_open_conn(Path(db_path)))

    def close(self) -> None:
        if self._conn is not None:
            self._conn.close()
            self._conn = None  # type: ignore[assignment]

    def __enter__(self) -> "AnalyticsStore":
        return self

    def __exit__(self, *_exc: Any) -> None:
        self.close()

    # ── videos ────────────────────────────────────────────────────────────────

    _VIDEO_COLUMNS = (
        "video_id, title, published_at, duration_seconds, tags, "
        "views, watch_time_minutes, avg_view_duration_seconds, "
        "avg_view_percentage, likes, comments, shares, "
        "subscribers_gained, subscribers_lost, "
        "impressions, ctr_percent, topic_type, angles, "
        "fetched_at, metrics_fetched_at"
    )

    def videos(
        self,
        *,
        min_duration_seconds: Optional[int] = None,
        min_views: Optional[int] = None,
        topic_type: Optional[str] = None,
        published_after: Optional[str] = None,
        order_by: str = "published_at",
        descending: bool = True,
    ) -> List[Dict[str, Any]]:
        """Return videos matching the given filters, ordered by `order_by`.

        Whitelist for `order_by`: video_id, title, published_at, duration_seconds,
        views, watch_time_minutes, avg_view_percentage, subscribers_gained,
        impressions, ctr_percent. Unknown values fall back to published_at.
        """
        order_col = self._safe_order_col(order_by)
        direction = "DESC" if descending else "ASC"

        where: List[str] = []
        params: List[Any] = []
        if min_duration_seconds is not None:
            where.append("duration_seconds >= ?")
            params.append(min_duration_seconds)
        if min_views is not None:
            where.append("views >= ?")
            params.append(min_views)
        if topic_type is not None:
            where.append("topic_type = ?")
            params.append(topic_type)
        if published_after is not None:
            where.append("published_at >= ?")
            params.append(published_after)

        clause = f"WHERE {' AND '.join(where)}" if where else ""
        sql = f"SELECT {self._VIDEO_COLUMNS} FROM videos {clause} ORDER BY {order_col} {direction}"
        return [dict(r) for r in self._conn.execute(sql, params).fetchall()]

    def video(self, video_id: str) -> Optional[Dict[str, Any]]:
        """Return one video by ID, or None."""
        row = self._conn.execute(
            f"SELECT {self._VIDEO_COLUMNS} FROM videos WHERE video_id = ?",
            (video_id,),
        ).fetchone()
        return dict(row) if row else None

    def videos_by_id(self, video_ids: Sequence[str]) -> Dict[str, Dict[str, Any]]:
        """Return a {video_id: row} mapping for the given IDs (missing IDs omitted)."""
        ids = list(video_ids)
        if not ids:
            return {}
        placeholders = ",".join("?" for _ in ids)
        sql = f"SELECT {self._VIDEO_COLUMNS} FROM videos WHERE video_id IN ({placeholders})"
        return {r["video_id"]: dict(r) for r in self._conn.execute(sql, ids).fetchall()}

    @staticmethod
    def _safe_order_col(name: str) -> str:
        allowed = {
            "video_id", "title", "published_at", "duration_seconds",
            "views", "watch_time_minutes", "avg_view_percentage",
            "subscribers_gained", "impressions", "ctr_percent",
        }
        return name if name in allowed else "published_at"

    # ── traffic_sources ───────────────────────────────────────────────────────

    def traffic_sources(
        self,
        *,
        video_id: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Return traffic rows. If `video_id` given, only that video's rows.

        Each row: {video_id, source_type, views, watch_time_minutes}.
        """
        if video_id is not None:
            rows = self._conn.execute(
                "SELECT video_id, source_type, views, watch_time_minutes "
                "FROM traffic_sources WHERE video_id = ? ORDER BY views DESC",
                (video_id,),
            ).fetchall()
        else:
            rows = self._conn.execute(
                "SELECT video_id, source_type, views, watch_time_minutes "
                "FROM traffic_sources"
            ).fetchall()
        return [dict(r) for r in rows]

    def traffic_totals_by_source(self) -> List[Dict[str, Any]]:
        """Aggregate traffic across all videos, grouped by source_type.

        Each row: {source_type, total_views, total_watch_time_minutes}.
        """
        rows = self._conn.execute(
            "SELECT source_type, "
            "SUM(views) AS total_views, "
            "SUM(watch_time_minutes) AS total_watch_time_minutes "
            "FROM traffic_sources GROUP BY source_type "
            "ORDER BY total_views DESC"
        ).fetchall()
        return [dict(r) for r in rows]

    # ── daily_channel ─────────────────────────────────────────────────────────

    def daily_channel(self, *, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Return daily channel rows ordered by day ascending.

        If `limit` is given, returns the *most recent* `limit` days (still
        ordered ascending in the result).
        """
        if limit is None:
            rows = self._conn.execute(
                "SELECT day, views, watch_time_minutes, avg_view_duration_seconds, "
                "subscribers_gained, subscribers_lost, likes, fetched_at "
                "FROM daily_channel ORDER BY day ASC"
            ).fetchall()
        else:
            rows = self._conn.execute(
                "SELECT day, views, watch_time_minutes, avg_view_duration_seconds, "
                "subscribers_gained, subscribers_lost, likes, fetched_at "
                "FROM daily_channel ORDER BY day DESC LIMIT ?",
                (limit,),
            ).fetchall()
            rows = list(reversed(rows))
        return [dict(r) for r in rows]

    # ── escape hatch ──────────────────────────────────────────────────────────

    def execute(self, sql: str, params: Sequence[Any] = ()) -> List[Dict[str, Any]]:
        """Run an ad-hoc read query. Use this only when no method fits.

        Aggregations with single callers (e.g. packaging_autopilot's threshold
        counts) belong here rather than as named methods.
        """
        return [dict(r) for r in self._conn.execute(sql, tuple(params)).fetchall()]

    # ── writes ────────────────────────────────────────────────────────────────

    def upsert_traffic_source(
        self,
        *,
        video_id: str,
        source_type: str,
        views: int,
        watch_time_minutes: float,
        fetched_at: str,
    ) -> None:
        """Insert or update one (video_id, source_type) row in traffic_sources.

        Does NOT commit. Caller calls store.commit() after batching writes.
        """
        self._conn.execute(
            "INSERT INTO traffic_sources "
            "(video_id, source_type, views, watch_time_minutes, fetched_at) "
            "VALUES (?, ?, ?, ?, ?) "
            "ON CONFLICT(video_id, source_type) DO UPDATE SET "
            "views = excluded.views, "
            "watch_time_minutes = excluded.watch_time_minutes, "
            "fetched_at = excluded.fetched_at",
            (video_id, source_type, views, watch_time_minutes, fetched_at),
        )

    def commit(self) -> None:
        """Commit pending writes. Pair with the upsert_* methods."""
        self._conn.commit()
