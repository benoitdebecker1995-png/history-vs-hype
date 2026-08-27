"""AnalyticsStore — single seam over analytics.db (videos, traffic_sources, daily_channel).

Peer to tools.discovery.keyword_store.KeywordStore. Hides connection lifecycle,
schema, and SQL from analysis scripts.

Reads are the primary surface. Writes grew in incrementally — see ADR-0004
stages 3–4. Currently exposed: upsert_video (with VideoRow dataclass),
upsert_traffic_source, upsert_daily_metric. All growth_data.py writers now
route through the store; ensure_schema() is the only remaining raw-conn
caller, which is appropriate (schema migration ≠ domain writes).

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
from dataclasses import astuple, dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

from tools.logging_config import get_logger
from tools.sqlite_access import connect_readonly

logger = get_logger(__name__)

ANALYTICS_DB = Path(__file__).parent / "analytics.db"


@dataclass(frozen=True)
class VideoRow:
    """Immutable contract for videos table upsert operations.

    Required fields match the schema's NOT NULL columns. Defaults match the
    schema defaults so a caller only needs to override the columns they
    actually have data for.

    Field order matches the INSERT column order in upsert_video — do NOT
    reorder without updating that SQL.
    """
    video_id: str
    title: str
    published_at: str
    duration_seconds: int
    fetched_at: str
    tags: Optional[str] = None  # JSON-encoded array string
    # Analytics-API metrics. None = "not fetched this refresh" (upsert COALESCEs
    # to keep last-known-good); a real 0 still lands. See upsert_video + ADR-0004.
    views: Optional[int] = 0
    watch_time_minutes: Optional[float] = 0.0
    avg_view_duration_seconds: Optional[int] = 0
    avg_view_percentage: Optional[float] = 0.0
    likes: Optional[int] = 0
    comments: Optional[int] = 0
    shares: Optional[int] = 0
    subscribers_gained: Optional[int] = 0
    subscribers_lost: int = 0
    impressions: Optional[int] = None
    ctr_percent: Optional[float] = None
    topic_type: str = "general"
    angles: Optional[str] = None  # JSON-encoded array string
    metrics_fetched_at: Optional[str] = None
    ctr_as_of: Optional[str] = None  # snapshot_date the CTR came from (freshness stamp)


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

    @classmethod
    def open_readonly(cls, db_path: Path = ANALYTICS_DB) -> "AnalyticsStore":
        """Open analytics.db without migrations, WAL changes, or write capability."""
        return cls(connect_readonly(Path(db_path)))

    def close(self) -> None:
        if self._conn is not None:
            self._conn.close()
            self._conn = None  # type: ignore[assignment]

    def __enter__(self) -> "AnalyticsStore":
        return self

    def __exit__(self, *_exc: Any) -> None:
        self.close()

    def commit(self) -> None:
        self._conn.commit()

    # ── studio CTR imports ────────────────────────────────────────────────────

    def studio_import_exists(self, source_sha256: str) -> bool:
        """True if a CSV with this content hash was already imported (idempotency)."""
        row = self._conn.execute(
            "SELECT 1 FROM studio_ctr_imports WHERE source_sha256 = ?", (source_sha256,)
        ).fetchone()
        return row is not None

    def insert_studio_import(self, *, source_sha256: str, source_filename: str,
                             exported_at: str, imported_at: str, window_kind: str,
                             period_start: Optional[str], period_end: Optional[str],
                             surface: str, rows: List[Dict[str, Any]],
                             unmatched_count: int) -> int:
        """Insert one import header + its rows in a single transaction. Returns import_id.

        Does NOT commit. Caller commits. Idempotency is the caller's job via
        studio_import_exists — the UNIQUE hash also hard-stops a double insert.
        """
        cur = self._conn.execute(
            "INSERT INTO studio_ctr_imports "
            "(source_sha256, source_filename, exported_at, imported_at, window_kind, "
            " period_start, period_end, surface, row_count, unmatched_count) "
            "VALUES (?,?,?,?,?,?,?,?,?,?)",
            (source_sha256, source_filename, exported_at, imported_at, window_kind,
             period_start, period_end, surface, len(rows), unmatched_count),
        )
        import_id = cur.lastrowid
        self._conn.executemany(
            "INSERT INTO studio_ctr_rows (import_id, video_id, video_title, impressions, ctr_percent) "
            "VALUES (?,?,?,?,?)",
            [(import_id, r["video_id"], r.get("video_title"), r.get("impressions"),
              r.get("ctr_percent")) for r in rows],
        )
        return import_id

    def latest_studio_lifetime(self) -> tuple:
        """Return ({video_id: {impressions, ctr_percent}}, exported_at) for the most
        recent LIFETIME import, or ({}, None) if none. Used by the CTR validator."""
        hdr = self._conn.execute(
            "SELECT id, exported_at FROM studio_ctr_imports "
            "WHERE window_kind = 'lifetime' ORDER BY exported_at DESC, id DESC LIMIT 1"
        ).fetchone()
        if hdr is None:
            return {}, None
        rows = self._conn.execute(
            "SELECT video_id, impressions, ctr_percent FROM studio_ctr_rows WHERE import_id = ?",
            (hdr["id"],),
        ).fetchall()
        out = {r["video_id"]: {"impressions": r["impressions"], "ctr_percent": r["ctr_percent"]}
               for r in rows}
        return out, hdr["exported_at"]

    def lifetime_ctr_by_video(self) -> Dict[str, Dict[str, Any]]:
        """LIFETIME impressions/CTR per video, each row carrying its own as-of.

        THE canonical read for "how did this video actually do". Peer to
        ``tools.discovery.ctr_reads.latest_valid_ctr_by_video`` (ADR-0017), which
        does the same job for keywords.db.

        Returns ``{video_id: {impressions, ctr_percent, as_of, grain, source_table}}``.
        Empty dict when no lifetime import exists.

        ⚠ Do NOT substitute ``videos()[...]["impressions"]`` for this. Those columns
        are a TRAILING SNAPSHOT stamped with ``ctr_as_of`` — on 2026-08-03 they held
        a single collection date for 57 of 58 rows, and reading them as lifetime gave
        a median of 56 impressions against a true lifetime median of 2,923. See the
        ADR that records that incident.
        """
        lifetime, exported_at = self.latest_studio_lifetime()
        return {
            vid: {
                "impressions": rec.get("impressions"),
                "ctr_percent": rec.get("ctr_percent"),
                "as_of": exported_at,
                "grain": "lifetime",
                "source_table": "studio_ctr_rows",
            }
            for vid, rec in lifetime.items()
        }

    def snapshot_ctr_by_video(self) -> Dict[str, Dict[str, Any]]:
        """TRAILING-WINDOW impressions/CTR per video, each row carrying its as-of.

        The ``videos.impressions`` / ``videos.ctr_percent`` pair, returned only ever
        alongside ``videos.ctr_as_of`` so the grain cannot be lost in transit. Use
        when you specifically want the recent window; use
        :meth:`lifetime_ctr_by_video` for how a video actually did.
        """
        try:
            rows = self._conn.execute(
                "SELECT video_id, impressions, ctr_percent, ctr_as_of FROM videos "
                "WHERE impressions IS NOT NULL"
            ).fetchall()
        except sqlite3.Error as e:
            logger.debug("snapshot_ctr_by_video failed: %s", e)
            return {}
        return {
            r["video_id"]: {
                "impressions": r["impressions"],
                "ctr_percent": r["ctr_percent"],
                "as_of": r["ctr_as_of"],
                "grain": "snapshot",
                "source_table": "videos",
            }
            for r in rows
        }

    # ── videos ────────────────────────────────────────────────────────────────

    _VIDEO_COLUMNS = (
        "video_id, title, published_at, duration_seconds, tags, "
        "views, watch_time_minutes, avg_view_duration_seconds, "
        "avg_view_percentage, likes, comments, shares, "
        "subscribers_gained, subscribers_lost, "
        "impressions, ctr_percent, topic_type, angles, "
        "fetched_at, metrics_fetched_at, ctr_as_of"
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

        ⚠ The ``impressions`` / ``ctr_percent`` columns in these rows are a
        **TRAILING SNAPSHOT**, not lifetime, and are only meaningful next to the
        ``ctr_as_of`` value returned in the same row. For "how did this video
        actually do", call :meth:`lifetime_ctr_by_video` instead — reading these as
        lifetime is a recorded incident, not a hypothetical.
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
        """Aggregate traffic across all videos in the canonical videos table.

        Inner-joins traffic_sources to videos so orphan rows (Shorts, deleted
        videos, stale backfill remnants) don't pollute the channel-wide
        long-form aggregate. The videos table is long-form only; traffic_sources
        can accumulate rows for videos no longer fetched.

        Each row: {source_type, total_views, total_watch_time_minutes}.
        """
        rows = self._conn.execute(
            "SELECT t.source_type, "
            "SUM(t.views) AS total_views, "
            "SUM(t.watch_time_minutes) AS total_watch_time_minutes "
            "FROM traffic_sources t "
            "INNER JOIN videos v ON t.video_id = v.video_id "
            "GROUP BY t.source_type "
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

    # ── retention_curves ──────────────────────────────────────────────────────

    def retention_curve(self, video_id: str) -> List[Dict[str, Any]]:
        """Return the full retention curve for one video, ordered by position."""
        rows = self._conn.execute(
            "SELECT video_id, elapsed_ratio, audience_watch_ratio, "
            "relative_performance, fetched_at "
            "FROM retention_curves WHERE video_id = ? ORDER BY elapsed_ratio ASC",
            (video_id,),
        ).fetchall()
        return [dict(r) for r in rows]

    def retention_summary_by_video(self) -> List[Dict[str, Any]]:
        """Return per-video retention summary joined to videos table.

        Each row: {video_id, title, views, point_count, avg_retention,
                   final_retention, min_retention, min_position}.

        min_position is the elapsed_ratio at which retention bottoms out — the
        clearest "cliff" indicator. final_retention compared to avg_retention
        flags whether viewers are leaving steadily or in a late drop.
        """
        rows = self._conn.execute(
            """
            WITH per_video AS (
                SELECT
                    rc.video_id,
                    COUNT(*) AS point_count,
                    AVG(rc.audience_watch_ratio) AS avg_retention,
                    MIN(rc.audience_watch_ratio) AS min_retention
                FROM retention_curves rc
                GROUP BY rc.video_id
            ),
            final_pt AS (
                SELECT video_id, audience_watch_ratio AS final_retention
                FROM retention_curves rc1
                WHERE elapsed_ratio = (
                    SELECT MAX(elapsed_ratio) FROM retention_curves rc2
                    WHERE rc2.video_id = rc1.video_id
                )
            ),
            min_pt AS (
                SELECT video_id, elapsed_ratio AS min_position
                FROM retention_curves rc1
                WHERE audience_watch_ratio = (
                    SELECT MIN(audience_watch_ratio) FROM retention_curves rc2
                    WHERE rc2.video_id = rc1.video_id
                )
                GROUP BY video_id  -- one row even if multiple minima tie
            )
            SELECT
                v.video_id,
                v.title,
                v.views,
                pv.point_count,
                pv.avg_retention,
                fp.final_retention,
                pv.min_retention,
                mp.min_position
            FROM videos v
            INNER JOIN per_video pv ON pv.video_id = v.video_id
            LEFT JOIN final_pt fp ON fp.video_id = v.video_id
            LEFT JOIN min_pt mp ON mp.video_id = v.video_id
            ORDER BY v.views DESC
            """
        ).fetchall()
        return [dict(r) for r in rows]

    def retention_cliffs(self, *, max_ratio: float = 0.80) -> List[Dict[str, Any]]:
        """Per-video retention minimum restricted to elapsed_ratio < max_ratio.

        The natural end-of-video falloff dominates a raw MIN(retention) — most
        videos hit their lowest point in the last bucket because viewers who
        watched 99% but skipped the outro count as drop. Restricting to the
        first 80% (default) isolates true mid-video cliffs — the bits worth
        editing differently next time.

        Returns: [{video_id, title, views, cliff_retention, cliff_position}]
        ordered by cliff_retention ASC (steepest first). Only videos with at
        least one retention point inside the window appear.
        """
        rows = self._conn.execute(
            """
            WITH cliffs AS (
                SELECT
                    rc.video_id,
                    MIN(rc.audience_watch_ratio) AS cliff_retention
                FROM retention_curves rc
                WHERE rc.elapsed_ratio < ?
                GROUP BY rc.video_id
            ),
            cliff_pos AS (
                SELECT rc.video_id, rc.elapsed_ratio AS cliff_position
                FROM retention_curves rc
                INNER JOIN cliffs c
                    ON c.video_id = rc.video_id
                   AND c.cliff_retention = rc.audience_watch_ratio
                WHERE rc.elapsed_ratio < ?
                GROUP BY rc.video_id  -- collapse ties to one position per video
            )
            SELECT
                v.video_id, v.title, v.views,
                c.cliff_retention, cp.cliff_position
            FROM videos v
            INNER JOIN cliffs c    ON c.video_id  = v.video_id
            INNER JOIN cliff_pos cp ON cp.video_id = v.video_id
            ORDER BY c.cliff_retention ASC
            """,
            (max_ratio, max_ratio),
        ).fetchall()
        return [dict(r) for r in rows]

    # ── opener_retention ──────────────────────────────────────────────────────

    def opener_rows(
        self,
        *,
        topic_type: Optional[str] = None,
        hook_archetype: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Return opener_retention rows, optionally filtered by topic / archetype.

        Each row: {video_id, opener_text, hook_archetype, first_30s_retention,
                   intro_drop_30s, topic_type, published_at, fetched_at}.
        DIAGNOSTIC ONLY — per-archetype n is small; never rank hook types on this.
        """
        where: List[str] = []
        params: List[Any] = []
        if topic_type is not None:
            where.append("topic_type = ?")
            params.append(topic_type)
        if hook_archetype is not None:
            where.append("hook_archetype = ?")
            params.append(hook_archetype)
        clause = f"WHERE {' AND '.join(where)}" if where else ""
        sql = (
            "SELECT video_id, opener_text, hook_archetype, first_30s_retention, "
            "intro_drop_30s, topic_type, published_at, fetched_at "
            f"FROM opener_retention {clause} ORDER BY intro_drop_30s DESC"
        )
        return [dict(r) for r in self._conn.execute(sql, params).fetchall()]

    def upsert_opener_retention(
        self,
        *,
        video_id: str,
        opener_text: Optional[str],
        hook_archetype: Optional[str],
        first_30s_retention: Optional[float],
        intro_drop_30s: Optional[float],
        topic_type: Optional[str],
        published_at: Optional[str],
        fetched_at: str,
    ) -> None:
        """Insert or update one row in opener_retention (video_id PRIMARY KEY).

        Does NOT commit. Caller calls store.commit() after batching writes.
        """
        self._conn.execute(
            "INSERT INTO opener_retention "
            "(video_id, opener_text, hook_archetype, first_30s_retention, "
            " intro_drop_30s, topic_type, published_at, fetched_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?) "
            "ON CONFLICT(video_id) DO UPDATE SET "
            "opener_text = excluded.opener_text, "
            "hook_archetype = excluded.hook_archetype, "
            "first_30s_retention = excluded.first_30s_retention, "
            "intro_drop_30s = excluded.intro_drop_30s, "
            "topic_type = excluded.topic_type, "
            "published_at = excluded.published_at, "
            "fetched_at = excluded.fetched_at",
            (video_id, opener_text, hook_archetype, first_30s_retention,
             intro_drop_30s, topic_type, published_at, fetched_at),
        )

    # ── search_terms ──────────────────────────────────────────────────────────

    def search_terms(
        self,
        *,
        video_id: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """Return search term rows. If `video_id` given, only that video's terms."""
        if video_id is not None:
            sql = (
                "SELECT video_id, term, views, watch_time_minutes, fetched_at "
                "FROM search_terms WHERE video_id = ? ORDER BY views DESC"
            )
            params: Sequence[Any] = (video_id,)
        else:
            sql = (
                "SELECT video_id, term, views, watch_time_minutes, fetched_at "
                "FROM search_terms ORDER BY views DESC"
            )
            params = ()
        if limit is not None:
            sql += f" LIMIT {int(limit)}"
        return [dict(r) for r in self._conn.execute(sql, params).fetchall()]

    def top_search_terms(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Aggregate search terms across all long-form videos.

        Returns: [{term, total_views, total_watch_time_minutes, video_count}]
        ordered by total_views DESC. Inner-joins videos so orphans are excluded.
        """
        rows = self._conn.execute(
            """
            SELECT
                s.term,
                SUM(s.views) AS total_views,
                SUM(s.watch_time_minutes) AS total_watch_time_minutes,
                COUNT(DISTINCT s.video_id) AS video_count
            FROM search_terms s
            INNER JOIN videos v ON v.video_id = s.video_id
            GROUP BY s.term
            ORDER BY total_views DESC
            LIMIT ?
            """,
            (int(limit),),
        ).fetchall()
        return [dict(r) for r in rows]

    def videos_missing_search_traffic(self) -> List[Dict[str, Any]]:
        """Long-form videos with zero rows in search_terms.

        These are videos the algorithm/index never surfaced via search —
        either a packaging miss (no head-term anchor) or a distribution miss
        (suggested-only). Returns: [{video_id, title, views, published_at}].
        """
        rows = self._conn.execute(
            """
            SELECT v.video_id, v.title, v.views, v.published_at
            FROM videos v
            LEFT JOIN search_terms s ON s.video_id = v.video_id
            WHERE s.video_id IS NULL
            ORDER BY v.views DESC
            """
        ).fetchall()
        return [dict(r) for r in rows]

    # ── subscribed_status ─────────────────────────────────────────────────────

    def subscribed_status(self, *, video_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Return subscribed_status rows. If video_id given, only that video."""
        if video_id is not None:
            rows = self._conn.execute(
                "SELECT video_id, status, views, watch_time_minutes, "
                "avg_view_percentage, fetched_at "
                "FROM subscribed_status WHERE video_id = ?",
                (video_id,),
            ).fetchall()
        else:
            rows = self._conn.execute(
                "SELECT video_id, status, views, watch_time_minutes, "
                "avg_view_percentage, fetched_at FROM subscribed_status"
            ).fetchall()
        return [dict(r) for r in rows]

    def subscribed_status_by_video(self) -> List[Dict[str, Any]]:
        """Pivoted sub/non-sub split per video, joined to videos.

        Each row: {video_id, title, views, sub_views, nonsub_views, nonsub_pct,
                   sub_avg_pct, nonsub_avg_pct}.

        nonsub_pct = share of views from non-subscribers (algorithm reach signal).
        Videos with high nonsub_pct AND high views = the algorithm pushed them
        beyond the existing audience.
        """
        rows = self._conn.execute(
            """
            SELECT
                v.video_id,
                v.title,
                v.views,
                COALESCE(SUM(CASE WHEN s.status = 'SUBSCRIBED'   THEN s.views END), 0) AS sub_views,
                COALESCE(SUM(CASE WHEN s.status = 'UNSUBSCRIBED' THEN s.views END), 0) AS nonsub_views,
                AVG(CASE WHEN s.status = 'SUBSCRIBED'   THEN s.avg_view_percentage END) AS sub_avg_pct,
                AVG(CASE WHEN s.status = 'UNSUBSCRIBED' THEN s.avg_view_percentage END) AS nonsub_avg_pct
            FROM videos v
            INNER JOIN subscribed_status s ON s.video_id = v.video_id
            GROUP BY v.video_id, v.title, v.views
            ORDER BY v.views DESC
            """
        ).fetchall()
        out = []
        for r in rows:
            d = dict(r)
            total = (d['sub_views'] or 0) + (d['nonsub_views'] or 0)
            d['nonsub_pct'] = (d['nonsub_views'] / total * 100) if total > 0 else 0.0
            out.append(d)
        return out

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

    def upsert_video(self, row: VideoRow) -> None:
        """Insert or update one row in the videos table (video_id PRIMARY KEY).

        Does NOT commit. Caller calls store.commit() after batching writes.

        Update semantics: COALESCE-guarded (a NULL in the new row keeps the prior
        value) for every metric that can be transiently unavailable — the CTR
        trio (impressions, ctr_percent, ctr_as_of) from the flaky keywords.db
        bridge, AND the Analytics-API metrics (views, watch_time, retention,
        subscribers_gained, …). `fetch_video_metrics_bulk` OMITS a video whose
        per-video query fails or returns no rows, so store_videos passes None for
        those fields; without the COALESCE a single failed video — or a broad API
        outage — would overwrite last-known-good metrics with 0. A genuine 0 is
        passed as 0 (not None) and still lands. Only metadata (title, tags, …) and
        subscribers_lost (never fetched per-video) stay full-replace.

        The VideoRow dataclass's field order matches the INSERT column
        order — astuple() produces a tuple compatible with the SQL below.
        """
        self._conn.execute(
            "INSERT INTO videos "
            "(video_id, title, published_at, duration_seconds, fetched_at, "
            " tags, views, watch_time_minutes, avg_view_duration_seconds, "
            " avg_view_percentage, likes, comments, shares, "
            " subscribers_gained, subscribers_lost, "
            " impressions, ctr_percent, topic_type, angles, metrics_fetched_at, "
            " ctr_as_of) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) "
            "ON CONFLICT(video_id) DO UPDATE SET "
            "title = excluded.title, "
            "published_at = excluded.published_at, "
            "duration_seconds = excluded.duration_seconds, "
            "fetched_at = excluded.fetched_at, "
            "tags = excluded.tags, "
            # Analytics-API metrics: COALESCE so an omitted-from-fetch video
            # (NULL) keeps its last-known-good value; a genuine 0 still lands.
            "views = COALESCE(excluded.views, videos.views), "
            "watch_time_minutes = COALESCE(excluded.watch_time_minutes, videos.watch_time_minutes), "
            "avg_view_duration_seconds = COALESCE(excluded.avg_view_duration_seconds, videos.avg_view_duration_seconds), "
            "avg_view_percentage = COALESCE(excluded.avg_view_percentage, videos.avg_view_percentage), "
            "likes = COALESCE(excluded.likes, videos.likes), "
            "comments = COALESCE(excluded.comments, videos.comments), "
            "shares = COALESCE(excluded.shares, videos.shares), "
            "subscribers_gained = COALESCE(excluded.subscribers_gained, videos.subscribers_gained), "
            "subscribers_lost = excluded.subscribers_lost, "
            # CTR/impressions/stamp are COALESCE-guarded: a refresh where the CTR
            # source is transiently empty (keywords.db missing/locked, tracker
            # failed) passes NULL, and without this guard the upsert would wipe
            # last-known-good CTR to NULL. Keep the old value when the new is NULL.
            "impressions = COALESCE(excluded.impressions, videos.impressions), "
            "ctr_percent = COALESCE(excluded.ctr_percent, videos.ctr_percent), "
            "topic_type = excluded.topic_type, "
            "angles = excluded.angles, "
            "metrics_fetched_at = excluded.metrics_fetched_at, "
            "ctr_as_of = COALESCE(excluded.ctr_as_of, videos.ctr_as_of)",
            astuple(row),
        )

    def upsert_daily_metric(
        self,
        *,
        day: str,
        views: int,
        watch_time_minutes: float,
        avg_view_duration_seconds: int,
        subscribers_gained: int,
        subscribers_lost: int,
        likes: int,
        fetched_at: str,
    ) -> None:
        """Insert or update one row in daily_channel (day is PRIMARY KEY).

        Does NOT commit. Caller calls store.commit() after batching writes.
        """
        self._conn.execute(
            "INSERT INTO daily_channel "
            "(day, views, watch_time_minutes, avg_view_duration_seconds, "
            " subscribers_gained, subscribers_lost, likes, fetched_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?) "
            "ON CONFLICT(day) DO UPDATE SET "
            "views = excluded.views, "
            "watch_time_minutes = excluded.watch_time_minutes, "
            "avg_view_duration_seconds = excluded.avg_view_duration_seconds, "
            "subscribers_gained = excluded.subscribers_gained, "
            "subscribers_lost = excluded.subscribers_lost, "
            "likes = excluded.likes, "
            "fetched_at = excluded.fetched_at",
            (day, views, watch_time_minutes, avg_view_duration_seconds,
             subscribers_gained, subscribers_lost, likes, fetched_at),
        )

    def upsert_retention_point(
        self,
        *,
        video_id: str,
        elapsed_ratio: float,
        audience_watch_ratio: float,
        relative_performance: Optional[float],
        fetched_at: str,
    ) -> None:
        """Insert or update one (video_id, elapsed_ratio) row in retention_curves.

        A full retention curve = ~100 rows per video. Caller batches all points
        then commits once.
        """
        self._conn.execute(
            "INSERT INTO retention_curves "
            "(video_id, elapsed_ratio, audience_watch_ratio, relative_performance, fetched_at) "
            "VALUES (?, ?, ?, ?, ?) "
            "ON CONFLICT(video_id, elapsed_ratio) DO UPDATE SET "
            "audience_watch_ratio = excluded.audience_watch_ratio, "
            "relative_performance = excluded.relative_performance, "
            "fetched_at = excluded.fetched_at",
            (video_id, elapsed_ratio, audience_watch_ratio, relative_performance, fetched_at),
        )

    def upsert_search_term(
        self,
        *,
        video_id: str,
        term: str,
        views: int,
        watch_time_minutes: float,
        fetched_at: str,
    ) -> None:
        """Insert or update one (video_id, term) row in search_terms."""
        self._conn.execute(
            "INSERT INTO search_terms "
            "(video_id, term, views, watch_time_minutes, fetched_at) "
            "VALUES (?, ?, ?, ?, ?) "
            "ON CONFLICT(video_id, term) DO UPDATE SET "
            "views = excluded.views, "
            "watch_time_minutes = excluded.watch_time_minutes, "
            "fetched_at = excluded.fetched_at",
            (video_id, term, views, watch_time_minutes, fetched_at),
        )

    def upsert_subscribed_status(
        self,
        *,
        video_id: str,
        status: str,
        views: int,
        watch_time_minutes: float,
        avg_view_percentage: float,
        fetched_at: str,
    ) -> None:
        """Insert or update one (video_id, status) row in subscribed_status.

        `status` is 'SUBSCRIBED' or 'UNSUBSCRIBED' (the YT Analytics API values).
        """
        self._conn.execute(
            "INSERT INTO subscribed_status "
            "(video_id, status, views, watch_time_minutes, avg_view_percentage, fetched_at) "
            "VALUES (?, ?, ?, ?, ?, ?) "
            "ON CONFLICT(video_id, status) DO UPDATE SET "
            "views = excluded.views, "
            "watch_time_minutes = excluded.watch_time_minutes, "
            "avg_view_percentage = excluded.avg_view_percentage, "
            "fetched_at = excluded.fetched_at",
            (video_id, status, views, watch_time_minutes, avg_view_percentage, fetched_at),
        )

    def commit(self) -> None:
        """Commit pending writes. Pair with the upsert_* methods."""
        self._conn.commit()
