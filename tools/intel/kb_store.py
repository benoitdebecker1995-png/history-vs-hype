"""
kb_store.py — SQLite storage layer for the YouTube Intelligence Engine

Manages tools/intel/intel.db with 5 tables:
    algo_snapshots      — Algorithm knowledge snapshots per refresh
    competitor_channels — Channel registry (config)
    competitor_videos   — Competitor video data (rolling window)
    niche_snapshots     — Niche format/hook pattern snapshots
    kb_meta             — Staleness tracking / last refresh timestamp

All public methods follow the error-dict pattern: return {'error': msg}
on failure; never raise. JSON columns use json.dumps/json.loads.
Schema auto-creates on first connection (keywords.db pattern).
Schema versioning via PRAGMA user_version (DB-01, DB-03).
"""

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from tools.logging_config import get_logger

logger = get_logger(__name__)

# Database lives alongside this file
DB_PATH = Path(__file__).parent / "intel.db"

# Current schema version — increment when adding new migrations below
CURRENT_SCHEMA_VERSION = 2

_SCHEMA_SQL = """
-- Algorithm knowledge: one snapshot per refresh
CREATE TABLE IF NOT EXISTS algo_snapshots (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    refreshed_at    TEXT    NOT NULL,
    source_names    TEXT    NOT NULL,   -- JSON array of source names used
    algorithm_model TEXT    NOT NULL,   -- JSON blob: full algorithm model
    signal_weights  TEXT,               -- JSON: {ctr, avd, satisfaction, ...}
    longform_insights TEXT,             -- JSON: insights specific to longform
    confidence      TEXT    DEFAULT 'medium'
);

-- Competitor channel registry (config, not rolled over)
CREATE TABLE IF NOT EXISTS competitor_channels (
    channel_id      TEXT PRIMARY KEY,
    channel_name    TEXT NOT NULL,
    channel_url     TEXT,
    subscriber_count INTEGER,
    niche_category  TEXT,               -- 'style-match', 'broad-history', 'geopolitics'
    track_active    INTEGER DEFAULT 1,
    added_at        TEXT NOT NULL
);

-- Competitor video store (rolling window — purge on refresh)
CREATE TABLE IF NOT EXISTS competitor_videos (
    video_id        TEXT PRIMARY KEY,
    channel_id      TEXT REFERENCES competitor_channels(channel_id),
    title           TEXT NOT NULL,
    published_at    TEXT NOT NULL,
    views           INTEGER,
    likes           INTEGER,
    duration_seconds INTEGER,
    description     TEXT,
    is_outlier      INTEGER DEFAULT 0,
    outlier_reason  TEXT,
    fetched_at      TEXT NOT NULL
);

-- Niche pattern snapshots
CREATE TABLE IF NOT EXISTS niche_snapshots (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    refreshed_at    TEXT NOT NULL,
    format_patterns TEXT,              -- JSON: {top_formats, avg_length_min, ...}
    hook_patterns   TEXT,             -- JSON: {common_hooks, title_formulas, ...}
    trending_topics TEXT              -- JSON: [{topic, channel, views, published_at}, ...]
);

-- Metadata / staleness tracking
CREATE TABLE IF NOT EXISTS kb_meta (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    last_refresh TEXT,
    last_export  TEXT,
    version      INTEGER DEFAULT 1
);

-- Indexes for common query patterns
CREATE INDEX IF NOT EXISTS idx_competitor_videos_channel   ON competitor_videos(channel_id);
CREATE INDEX IF NOT EXISTS idx_competitor_videos_outlier   ON competitor_videos(is_outlier);
CREATE INDEX IF NOT EXISTS idx_competitor_videos_published ON competitor_videos(published_at);
"""


class KBStore:
    """
    SQLite knowledge-base store for the YouTube Intelligence Engine.

    Usage:
        store = KBStore()                    # uses default DB_PATH
        store = KBStore('/custom/path.db')   # custom path
    """

    def __init__(self, db_path: str | Path | None = None):
        self.db_path = Path(db_path) if db_path else DB_PATH
        self._migrate_schema()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _connect(self) -> sqlite3.Connection:
        """Open connection with row_factory for dict-like access."""
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        return conn

    def _get_schema_version(self) -> int:
        """Read PRAGMA user_version from the database. Returns 0 if never set or on error."""
        try:
            conn = self._connect()
            version = conn.execute("PRAGMA user_version").fetchone()[0]
            conn.close()
            logger.debug("intel.db schema version: %d", version)
            return version
        except sqlite3.Error:
            return 0

    def _set_schema_version(self, version: int) -> None:
        """Write PRAGMA user_version to the database."""
        conn = self._connect()
        conn.execute(f"PRAGMA user_version = {version}")
        conn.commit()
        conn.close()
        logger.debug("intel.db schema version set to %d", version)

    def _migrate_schema(self) -> None:
        """
        Run all pending schema migrations in version order.

        Version gates are idempotent — each gate only runs when the current
        version is below the target. Version is stamped AFTER the DDL block
        succeeds, so a failed migration reruns on next startup.

        All DDL inside each gate is wrapped in `with conn:` for atomic rollback.
        Note: executescript() is NOT used inside `with conn:` blocks because it
        issues an implicit COMMIT that defeats rollback. Individual conn.execute()
        calls are used instead.
        """
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        version = self._get_schema_version()

        # ----------------------------------------------------------------
        # Version 1: initial schema (5 tables + 3 indexes)
        # ----------------------------------------------------------------
        if version < 1:
            conn = self._connect()
            try:
                has_tables = conn.execute(
                    "SELECT name FROM sqlite_master WHERE type='table' AND name='algo_snapshots'"
                ).fetchone() is not None

                if not has_tables:
                    # Fresh database — create all tables and indexes atomically.
                    # Split _SCHEMA_SQL into individual statements and execute
                    # each separately so `with conn:` rollback actually works.
                    # Note: executescript() is NOT used here because it issues an
                    # implicit COMMIT that defeats the `with conn:` rollback.
                    logger.info("intel.db: creating initial schema (version 1)")
                    try:
                        with conn:
                            for stmt in _SCHEMA_SQL.strip().split(";\n"):
                                # Strip leading comment lines, keep the SQL part
                                sql_lines = [
                                    line for line in stmt.splitlines()
                                    if line.strip() and not line.strip().startswith("--")
                                ]
                                sql = "\n".join(sql_lines).strip()
                                if sql:
                                    conn.execute(sql)
                    except Exception as exc:
                        conn.close()
                        raise RuntimeError(f"KBStore schema init failed: {exc}") from exc
                else:
                    # Pre-versioning database — tables already exist, skip DDL
                    logger.info("intel.db: existing pre-v1 database detected, bootstrapping to version 1")

                conn.close()
            except RuntimeError:
                raise
            except Exception as exc:
                conn.close()
                raise RuntimeError(f"KBStore schema init failed: {exc}") from exc

            self._set_schema_version(1)
            version = 1

        # ----------------------------------------------------------------
        # Version 2: add topic_cluster + outlier_ratio columns
        # ----------------------------------------------------------------
        if version < 2:
            logger.info("intel.db: migrating to version 2 (adding topic_cluster, outlier_ratio columns)")
            conn = self._connect()
            try:
                cols = [r[1] for r in conn.execute("PRAGMA table_info(competitor_videos)").fetchall()]
                with conn:
                    if "topic_cluster" not in cols:
                        conn.execute("ALTER TABLE competitor_videos ADD COLUMN topic_cluster TEXT")
                    if "outlier_ratio" not in cols:
                        conn.execute("ALTER TABLE competitor_videos ADD COLUMN outlier_ratio REAL")
            except Exception as exc:
                conn.close()
                raise RuntimeError(f"KBStore migration to v2 failed: {exc}") from exc
            conn.close()
            self._set_schema_version(2)
            logger.info("intel.db: migration to version 2 complete")

    @staticmethod
    def _now() -> str:
        """Return current UTC time as ISO 8601 string."""
        return datetime.now(timezone.utc).isoformat()

    # ------------------------------------------------------------------
    # Algorithm snapshots
    # ------------------------------------------------------------------

    def save_algo_snapshot(
        self,
        source_names: list,
        algorithm_model: dict,
        signal_weights: dict | None = None,
        longform_insights: list | None = None,
        confidence: str = "medium",
    ) -> dict:
        """
        Insert a new algorithm knowledge snapshot.

        Args:
            source_names:      List of source names used (e.g. ['vidIQ', 'Creator Insider'])
            algorithm_model:   Full algorithm model blob as dict
            signal_weights:    Dict mapping signal names to weight strings
            longform_insights: List of longform-specific insight strings
            confidence:        'high' | 'medium' | 'low'

        Returns:
            {'id': int, 'refreshed_at': str} or {'error': str}
        """
        try:
            conn = self._connect()
            now = self._now()
            cursor = conn.execute(
                """INSERT INTO algo_snapshots
                   (refreshed_at, source_names, algorithm_model, signal_weights, longform_insights, confidence)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (
                    now,
                    json.dumps(source_names),
                    json.dumps(algorithm_model),
                    json.dumps(signal_weights) if signal_weights is not None else None,
                    json.dumps(longform_insights) if longform_insights is not None else None,
                    confidence,
                ),
            )
            conn.commit()
            row_id = cursor.lastrowid
            conn.close()
            return {"id": row_id, "refreshed_at": now}
        except Exception as exc:
            return {"error": f"save_algo_snapshot failed: {exc}"}

    def get_latest_algo_snapshot(self) -> dict | None:
        """
        Return the most recent algorithm snapshot, or None if empty.

        Returns:
            dict with all fields (JSON columns decoded) or None
        """
        try:
            conn = self._connect()
            row = conn.execute(
                "SELECT * FROM algo_snapshots ORDER BY id DESC LIMIT 1"
            ).fetchone()
            conn.close()
            if row is None:
                return None
            result = dict(row)
            for col in ("source_names", "algorithm_model", "signal_weights", "longform_insights"):
                if result.get(col) is not None:
                    result[col] = json.loads(result[col])
            return result
        except Exception as exc:
            return {"error": f"get_latest_algo_snapshot failed: {exc}"}

    # ------------------------------------------------------------------
    # Competitor channels
    # ------------------------------------------------------------------

    def save_competitor_channel(
        self,
        channel_id: str,
        channel_name: str,
        channel_url: str | None = None,
        subscriber_count: int | None = None,
        niche_category: str | None = None,
    ) -> dict:
        """
        Upsert a competitor channel into the registry.

        Returns:
            {'channel_id': str} or {'error': str}
        """
        try:
            conn = self._connect()
            conn.execute(
                """INSERT INTO competitor_channels
                   (channel_id, channel_name, channel_url, subscriber_count, niche_category, added_at)
                   VALUES (?, ?, ?, ?, ?, ?)
                   ON CONFLICT(channel_id) DO UPDATE SET
                       channel_name = excluded.channel_name,
                       channel_url  = excluded.channel_url,
                       subscriber_count = excluded.subscriber_count,
                       niche_category = excluded.niche_category""",
                (channel_id, channel_name, channel_url, subscriber_count, niche_category, self._now()),
            )
            conn.commit()
            conn.close()
            return {"channel_id": channel_id}
        except Exception as exc:
            return {"error": f"save_competitor_channel failed: {exc}"}

    def get_active_channels(self) -> list[dict]:
        """
        Return all channels with track_active = 1.

        Returns:
            List of channel dicts or {'error': str}
        """
        try:
            conn = self._connect()
            rows = conn.execute(
                "SELECT * FROM competitor_channels WHERE track_active = 1"
            ).fetchall()
            conn.close()
            return [dict(r) for r in rows]
        except Exception as exc:
            return {"error": f"get_active_channels failed: {exc}"}

    # ------------------------------------------------------------------
    # Competitor videos
    # ------------------------------------------------------------------

    def save_competitor_videos(self, videos: list[dict]) -> dict:
        """
        Bulk insert or update competitor videos.

        Each video dict should contain:
            video_id, channel_id, title, published_at, views, likes,
            duration_seconds, description, is_outlier, outlier_reason

        Returns:
            {'saved': int} or {'error': str}
        """
        if not videos:
            return {"saved": 0}
        try:
            conn = self._connect()
            now = self._now()
            saved = 0
            for video in videos:
                conn.execute(
                    """INSERT INTO competitor_videos
                       (video_id, channel_id, title, published_at, views, likes,
                        duration_seconds, description, is_outlier, outlier_reason, fetched_at)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                       ON CONFLICT(video_id) DO UPDATE SET
                           views            = excluded.views,
                           likes            = excluded.likes,
                           duration_seconds = excluded.duration_seconds,
                           is_outlier       = excluded.is_outlier,
                           outlier_reason   = excluded.outlier_reason,
                           fetched_at       = excluded.fetched_at""",
                    (
                        video.get("video_id"),
                        video.get("channel_id"),
                        video.get("title"),
                        video.get("published_at"),
                        video.get("views"),
                        video.get("likes"),
                        video.get("duration_seconds"),
                        video.get("description"),
                        int(bool(video.get("is_outlier", False))),
                        video.get("outlier_reason"),
                        now,
                    ),
                )
                saved += 1
            conn.commit()
            conn.close()
            return {"saved": saved}
        except Exception as exc:
            return {"error": f"save_competitor_videos failed: {exc}"}

    def get_competitor_videos(
        self,
        channel_id: str | None = None,
        outliers_only: bool = False,
        limit: int = 50,
    ) -> list[dict]:
        """
        Fetch competitor videos with optional filters.

        Args:
            channel_id:    Filter by channel (None = all channels)
            outliers_only: Only return is_outlier = 1 videos
            limit:         Max rows to return

        Returns:
            List of video dicts or {'error': str}
        """
        try:
            conn = self._connect()
            where_clauses = []
            params: list = []

            if channel_id is not None:
                where_clauses.append("channel_id = ?")
                params.append(channel_id)
            if outliers_only:
                where_clauses.append("is_outlier = 1")

            where_sql = "WHERE " + " AND ".join(where_clauses) if where_clauses else ""
            params.append(limit)

            rows = conn.execute(
                f"SELECT * FROM competitor_videos {where_sql} ORDER BY published_at DESC LIMIT ?",
                params,
            ).fetchall()
            conn.close()
            return [dict(r) for r in rows]
        except Exception as exc:
            return {"error": f"get_competitor_videos failed: {exc}"}

    def purge_competitor_videos(self) -> dict:
        """
        Delete all competitor videos (used before a full refresh).

        Returns:
            {'deleted': int} or {'error': str}
        """
        try:
            conn = self._connect()
            cursor = conn.execute("DELETE FROM competitor_videos")
            deleted = cursor.rowcount
            conn.commit()
            conn.close()
            return {"deleted": deleted}
        except Exception as exc:
            return {"error": f"purge_competitor_videos failed: {exc}"}

    # ------------------------------------------------------------------
    # Niche snapshots
    # ------------------------------------------------------------------

    def save_niche_snapshot(
        self,
        format_patterns: dict | None = None,
        hook_patterns: dict | None = None,
        trending_topics: list | None = None,
    ) -> dict:
        """
        Insert a niche pattern snapshot.

        Returns:
            {'id': int, 'refreshed_at': str} or {'error': str}
        """
        try:
            conn = self._connect()
            now = self._now()
            cursor = conn.execute(
                """INSERT INTO niche_snapshots
                   (refreshed_at, format_patterns, hook_patterns, trending_topics)
                   VALUES (?, ?, ?, ?)""",
                (
                    now,
                    json.dumps(format_patterns) if format_patterns is not None else None,
                    json.dumps(hook_patterns) if hook_patterns is not None else None,
                    json.dumps(trending_topics) if trending_topics is not None else None,
                ),
            )
            conn.commit()
            row_id = cursor.lastrowid
            conn.close()
            return {"id": row_id, "refreshed_at": now}
        except Exception as exc:
            return {"error": f"save_niche_snapshot failed: {exc}"}

    def get_latest_niche_snapshot(self) -> dict | None:
        """
        Return the most recent niche snapshot, or None if empty.

        Returns:
            dict with JSON columns decoded, or None
        """
        try:
            conn = self._connect()
            row = conn.execute(
                "SELECT * FROM niche_snapshots ORDER BY id DESC LIMIT 1"
            ).fetchone()
            conn.close()
            if row is None:
                return None
            result = dict(row)
            for col in ("format_patterns", "hook_patterns", "trending_topics"):
                if result.get(col) is not None:
                    result[col] = json.loads(result[col])
            return result
        except Exception as exc:
            return {"error": f"get_latest_niche_snapshot failed: {exc}"}

    # ------------------------------------------------------------------
    # Staleness / refresh tracking
    # ------------------------------------------------------------------

    def get_last_refresh(self) -> str | None:
        """
        Return ISO timestamp of the last refresh, or None if never refreshed.
        """
        try:
            conn = self._connect()
            row = conn.execute(
                "SELECT last_refresh FROM kb_meta ORDER BY id DESC LIMIT 1"
            ).fetchone()
            conn.close()
            if row is None:
                return None
            return row["last_refresh"]
        except Exception as exc:
            return {"error": f"get_last_refresh failed: {exc}"}

    def set_last_refresh(self) -> dict:
        """
        Update kb_meta.last_refresh to the current UTC time.

        Inserts a new row if kb_meta is empty; otherwise updates the latest.

        Returns:
            {'last_refresh': str} or {'error': str}
        """
        try:
            conn = self._connect()
            now = self._now()
            row = conn.execute("SELECT id FROM kb_meta ORDER BY id DESC LIMIT 1").fetchone()
            if row is None:
                conn.execute(
                    "INSERT INTO kb_meta (last_refresh) VALUES (?)", (now,)
                )
            else:
                conn.execute(
                    "UPDATE kb_meta SET last_refresh = ? WHERE id = ?",
                    (now, row["id"]),
                )
            conn.commit()
            conn.close()
            return {"last_refresh": now}
        except Exception as exc:
            return {"error": f"set_last_refresh failed: {exc}"}

    def update_video_topic(self, video_id: str, topic_cluster_json: str) -> dict:
        """
        Update the topic_cluster column for a single competitor video.

        Args:
            video_id:            YouTube video ID
            topic_cluster_json:  JSON string of topic clusters (e.g. '["territorial","legal"]')

        Returns:
            {'updated': True} or {'error': str}
        """
        try:
            conn = self._connect()
            conn.execute(
                "UPDATE competitor_videos SET topic_cluster = ? WHERE video_id = ?",
                (topic_cluster_json, video_id),
            )
            conn.commit()
            conn.close()
            return {"updated": True}
        except Exception as exc:
            return {"error": f"update_video_topic failed: {exc}"}

    def update_video_outlier_ratio(self, video_id: str, ratio: float) -> dict:
        """
        Update the outlier_ratio column for a single competitor video.

        Args:
            video_id: YouTube video ID
            ratio:    Outlier ratio (views / channel median)

        Returns:
            {'updated': True} or {'error': str}
        """
        try:
            conn = self._connect()
            conn.execute(
                "UPDATE competitor_videos SET outlier_ratio = ? WHERE video_id = ?",
                (ratio, video_id),
            )
            conn.commit()
            conn.close()
            return {"updated": True}
        except Exception as exc:
            return {"error": f"update_video_outlier_ratio failed: {exc}"}

    def is_stale(self, max_age_days: int = 7) -> bool:
        """
        Return True if the knowledge base needs a refresh.

        A fresh DB (no refresh ever recorded) is always stale.

        Args:
            max_age_days: Number of days before data is considered stale

        Returns:
            True if stale (refresh needed), False if current
        """
        try:
            last = self.get_last_refresh()
            if last is None or isinstance(last, dict):
                # None = never refreshed; dict = error
                return True
            last_dt = datetime.fromisoformat(last)
            now = datetime.now(timezone.utc)
            # Make last_dt timezone-aware if needed
            if last_dt.tzinfo is None:
                last_dt = last_dt.replace(tzinfo=timezone.utc)
            age_days = (now - last_dt).days
            return age_days >= max_age_days
        except (ValueError, TypeError, sqlite3.Error):
            # Conservative: if we can't determine staleness, assume stale
            return True
