"""
Performance Tracker Module

Extracted from database.py (Phase H4 refactor). Owns all 21 methods related to
video performance, CTR variant tracking, and post-publish feedback loops.

Usage:
    from tools.discovery.performance_tracker import PerformanceTracker

    tracker = PerformanceTracker.connect()
    tracker.add_video_performance('abc123', title='Why Borders Matter', views=15000)
    tracker.close()
"""

import sqlite3
import json
from datetime import datetime, timezone
from typing import Optional, Dict, List, Any

from tools.discovery.ctr_reads import latest_valid_ctr_by_video
from tools.logging_config import get_logger

logger = get_logger(__name__)


class PerformanceTracker:
    """
    Video performance tracking and CTR variant analysis.

    Wraps an injected sqlite3.Connection. Use connect() to construct from a
    full KeywordDB path, or pass a connection directly for testing.
    """

    def __init__(self, conn: sqlite3.Connection) -> None:
        self._conn = conn

    @classmethod
    def connect(cls, db_path: Optional[str] = None) -> 'PerformanceTracker':
        from tools.discovery.database import KeywordDB  # deferred — avoids circular import
        kdb = KeywordDB(db_path)
        return cls(kdb._conn)

    def close(self) -> None:
        if self._conn:
            self._conn.close()
            self._conn = None

    # -------------------------------------------------------------------------
    # Internal helpers
    # -------------------------------------------------------------------------

    @staticmethod
    def _err(operation: str, message: str, exc: Optional[BaseException] = None, **extras) -> Dict[str, Any]:
        result: Dict[str, Any] = {
            'error': message,
            'module': __name__,
            'operation': operation,
            'details': str(exc) if exc is not None else '',
        }
        result.update(extras)
        return result

    def _ensure_performance_table(self):
        """Safely create video_performance table if it doesn't exist."""
        try:
            cursor = self._conn.cursor()
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='video_performance'"
            )
            if cursor.fetchone() is not None:
                return
            with self._conn:
                self._conn.execute(
                    """
                    CREATE TABLE IF NOT EXISTS video_performance (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        video_id TEXT UNIQUE NOT NULL,
                        title TEXT,
                        views INTEGER,
                        subscribers_gained INTEGER,
                        subscribers_lost INTEGER,
                        conversion_rate REAL,
                        watch_time_minutes REAL,
                        avg_view_duration_seconds INTEGER,
                        likes INTEGER,
                        comments INTEGER,
                        shares INTEGER,
                        topic_type TEXT,
                        angles TEXT,
                        published_at DATE,
                        fetched_at DATE NOT NULL,
                        classified_at DATE
                    )
                    """
                )
                self._conn.execute(
                    "CREATE INDEX IF NOT EXISTS idx_performance_conversion ON video_performance(conversion_rate DESC)"
                )
                self._conn.execute(
                    "CREATE INDEX IF NOT EXISTS idx_performance_topic ON video_performance(topic_type)"
                )
                self._conn.execute(
                    "CREATE INDEX IF NOT EXISTS idx_performance_fetched ON video_performance(fetched_at DESC)"
                )
        except sqlite3.Error:
            pass

    # =========================================================================
    # VIDEO PERFORMANCE METHODS (Phase 19)
    # =========================================================================

    def add_video_performance(
        self,
        video_id: str,
        title: Optional[str] = None,
        views: Optional[int] = None,
        subscribers_gained: Optional[int] = None,
        subscribers_lost: Optional[int] = None,
        conversion_rate: Optional[float] = None,
        watch_time_minutes: Optional[float] = None,
        avg_view_duration_seconds: Optional[int] = None,
        likes: Optional[int] = None,
        comments: Optional[int] = None,
        shares: Optional[int] = None,
        topic_type: Optional[str] = None,
        angles: Optional[List[str]] = None,
        published_at: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Add or update video performance data.

        Uses INSERT OR REPLACE to update existing records.

        Args:
            video_id: YouTube video ID (required, unique)
            title: Video title
            views: Total views
            subscribers_gained: Subscribers gained from this video
            subscribers_lost: Subscribers lost from this video
            conversion_rate: (subs_gained / views) * 100
            watch_time_minutes: Total watch time in minutes
            avg_view_duration_seconds: Average view duration
            likes: Like count
            comments: Comment count
            shares: Share count
            topic_type: Primary topic classification
            angles: List of content angles (stored as JSON)
            published_at: Video publish date (ISO format)

        Returns:
            {'status': 'inserted'|'updated', 'video_id': str} on success
            {'error': msg} on failure

        Example:
            db.add_video_performance(
                video_id='abc123',
                title='Why Borders Matter',
                views=15000,
                subscribers_gained=25,
                subscribers_lost=2,
                conversion_rate=0.167,
                topic_type='territorial',
                angles=['legal', 'historical']
            )
        """
        try:
            self._ensure_performance_table()

            cursor = self._conn.cursor()
            now = datetime.now(timezone.utc).date().isoformat()

            angles_json = json.dumps(angles) if angles else None

            cursor.execute(
                "SELECT id FROM video_performance WHERE video_id = ?",
                (video_id,)
            )
            existing = cursor.fetchone()

            if existing:
                cursor.execute(
                    """
                    UPDATE video_performance
                    SET title = COALESCE(?, title),
                        views = COALESCE(?, views),
                        subscribers_gained = COALESCE(?, subscribers_gained),
                        subscribers_lost = COALESCE(?, subscribers_lost),
                        conversion_rate = COALESCE(?, conversion_rate),
                        watch_time_minutes = COALESCE(?, watch_time_minutes),
                        avg_view_duration_seconds = COALESCE(?, avg_view_duration_seconds),
                        likes = COALESCE(?, likes),
                        comments = COALESCE(?, comments),
                        shares = COALESCE(?, shares),
                        topic_type = COALESCE(?, topic_type),
                        angles = COALESCE(?, angles),
                        published_at = COALESCE(?, published_at),
                        fetched_at = ?,
                        classified_at = CASE WHEN ? IS NOT NULL THEN ? ELSE classified_at END
                    WHERE video_id = ?
                    """,
                    (title, views, subscribers_gained, subscribers_lost, conversion_rate,
                     watch_time_minutes, avg_view_duration_seconds, likes, comments, shares,
                     topic_type, angles_json, published_at, now, now, now, video_id)
                )
                action = 'updated'
            else:
                cursor.execute(
                    """
                    INSERT INTO video_performance
                        (video_id, title, views, subscribers_gained, subscribers_lost,
                         conversion_rate, watch_time_minutes, avg_view_duration_seconds,
                         likes, comments, shares, topic_type, angles, published_at,
                         fetched_at, classified_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (video_id, title, views, subscribers_gained, subscribers_lost,
                     conversion_rate, watch_time_minutes, avg_view_duration_seconds,
                     likes, comments, shares, topic_type, angles_json, published_at,
                     now, now if (topic_type or angles) else None)
                )
                action = 'inserted'

            self._conn.commit()

            return {
                'status': action,
                'video_id': video_id
            }

        except sqlite3.Error as e:
            return self._err('add_video_performance', 'Database operation failed', e)

    def get_video_performance(self, video_id: str) -> Dict[str, Any]:
        """
        Retrieve performance data for a single video.

        Args:
            video_id: YouTube video ID

        Returns:
            Video performance dict with angles parsed from JSON
            {'error': 'not found'} if video not in database

        Example:
            perf = db.get_video_performance('abc123')
            if 'error' not in perf:
                print(f"Conversion rate: {perf['conversion_rate']}%")
        """
        try:
            self._ensure_performance_table()

            cursor = self._conn.cursor()
            cursor.execute(
                "SELECT * FROM video_performance WHERE video_id = ?",
                (video_id,)
            )

            row = cursor.fetchone()

            if row is None:
                return self._err('get_video_performance', 'not found', video_id=video_id)

            result = dict(row)

            if result.get('angles'):
                try:
                    result['angles'] = json.loads(result['angles'])
                except (json.JSONDecodeError, TypeError):
                    result['angles'] = []

            return result

        except sqlite3.Error as e:
            return self._err('get_video_performance', 'Database operation failed', e)

    def search_video_performance_by_title(self, title_prefix: str) -> Optional[str]:
        """Look up video_id by title prefix using case-insensitive LIKE match."""
        if not title_prefix:
            return None
        try:
            self._ensure_performance_table()
            prefix = title_prefix[:40]
            cursor = self._conn.cursor()
            cursor.execute(
                "SELECT video_id FROM video_performance "
                "WHERE title LIKE ? COLLATE NOCASE LIMIT 1",
                (f"%{prefix}%",),
            )
            row = cursor.fetchone()
            return row[0] if row else None
        except Exception as exc:
            logger.warning("DB lookup error for '%s': %s", title_prefix, exc)
            return None

    def get_all_video_performance(self, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Retrieve all video performance records.

        Args:
            limit: Maximum records to return (default 100)

        Returns:
            List of video performance dicts, sorted by fetched_at DESC

        Example:
            all_videos = db.get_all_video_performance(limit=50)
            for v in all_videos:
                print(f"{v['title']}: {v['conversion_rate']}% conversion")
        """
        try:
            self._ensure_performance_table()

            cursor = self._conn.cursor()
            cursor.execute(
                """
                SELECT * FROM video_performance
                ORDER BY fetched_at DESC
                LIMIT ?
                """,
                (limit,)
            )

            results = []
            for row in cursor.fetchall():
                video_dict = dict(row)

                if video_dict.get('angles'):
                    try:
                        video_dict['angles'] = json.loads(video_dict['angles'])
                    except (json.JSONDecodeError, TypeError):
                        video_dict['angles'] = []

                results.append(video_dict)

            return results

        except sqlite3.Error:
            return []

    def get_performance_by_topic(self, topic_type: str, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Get video performance filtered by topic type.

        Args:
            topic_type: Topic to filter by (e.g., 'territorial', 'ideological')
            limit: Maximum records to return

        Returns:
            List of video performance dicts with matching topic_type

        Example:
            territorial = db.get_performance_by_topic('territorial')
            avg_conversion = sum(v['conversion_rate'] for v in territorial) / len(territorial)
        """
        try:
            self._ensure_performance_table()

            cursor = self._conn.cursor()
            cursor.execute(
                """
                SELECT * FROM video_performance
                WHERE topic_type = ?
                ORDER BY conversion_rate DESC NULLS LAST
                LIMIT ?
                """,
                (topic_type, limit)
            )

            results = []
            for row in cursor.fetchall():
                video_dict = dict(row)

                if video_dict.get('angles'):
                    try:
                        video_dict['angles'] = json.loads(video_dict['angles'])
                    except (json.JSONDecodeError, TypeError):
                        video_dict['angles'] = []

                results.append(video_dict)

            return results

        except sqlite3.Error:
            return []

    def get_performance_by_angle(self, angle: str, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Get video performance filtered by content angle.

        Uses JSON search since angles are stored as JSON array.

        Args:
            angle: Angle to filter by (e.g., 'legal', 'historical')
            limit: Maximum records to return

        Returns:
            List of video performance dicts containing the specified angle

        Example:
            legal_videos = db.get_performance_by_angle('legal')
            for v in legal_videos:
                print(f"{v['title']}: {v['angles']}")
        """
        try:
            self._ensure_performance_table()

            cursor = self._conn.cursor()

            search_pattern = f'%"{angle}"%'

            cursor.execute(
                """
                SELECT * FROM video_performance
                WHERE angles LIKE ?
                ORDER BY conversion_rate DESC NULLS LAST
                LIMIT ?
                """,
                (search_pattern, limit)
            )

            results = []
            for row in cursor.fetchall():
                video_dict = dict(row)

                if video_dict.get('angles'):
                    try:
                        video_dict['angles'] = json.loads(video_dict['angles'])
                    except (json.JSONDecodeError, TypeError):
                        video_dict['angles'] = []

                results.append(video_dict)

            return results

        except sqlite3.Error:
            return []

    def get_top_converters(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get videos with highest subscriber conversion rates.

        Args:
            limit: Number of top videos to return (default 10)

        Returns:
            List of video performance dicts sorted by conversion_rate DESC

        Example:
            top = db.get_top_converters(limit=5)
            for v in top:
                print(f"{v['title']}: {v['conversion_rate']:.3f}% conversion")
        """
        try:
            self._ensure_performance_table()

            cursor = self._conn.cursor()
            cursor.execute(
                """
                SELECT * FROM video_performance
                WHERE conversion_rate IS NOT NULL
                ORDER BY conversion_rate DESC
                LIMIT ?
                """,
                (limit,)
            )

            results = []
            for row in cursor.fetchall():
                video_dict = dict(row)

                if video_dict.get('angles'):
                    try:
                        video_dict['angles'] = json.loads(video_dict['angles'])
                    except (json.JSONDecodeError, TypeError):
                        video_dict['angles'] = []

                results.append(video_dict)

            return results

        except sqlite3.Error:
            return []

    # =========================================================================
    # VARIANT TRACKING METHODS (Phase 29)
    # =========================================================================

    def record_package_version(
        self,
        project_slug: str,
        kind: str,
        value: str,
        *,
        video_id: Optional[str] = None,
        content_hash: Optional[str] = None,
        source_path: Optional[str] = None,
        effective_at: Optional[str] = None,
        supersedes_id: Optional[int] = None,
        experiment_id: Optional[str] = None,
        reason: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Record an observed title/thumbnail version; never judge its quality."""
        if kind not in {"title", "thumbnail"}:
            return self._err("record_package_version", "kind must be title or thumbnail")
        if not project_slug.strip() or not value.strip():
            return self._err("record_package_version", "project_slug and value are required")
        now = datetime.now(timezone.utc).isoformat()
        effective = effective_at or now
        try:
            cursor = self._conn.execute(
                """
                INSERT INTO package_versions
                    (project_slug, video_id, kind, value, content_hash, source_path,
                     effective_at, recorded_at, supersedes_id, experiment_id, reason)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    project_slug.strip(), video_id, kind, value.strip(), content_hash,
                    source_path, effective, now, supersedes_id, experiment_id, reason,
                ),
            )
            self._conn.commit()
            return {"status": "inserted", "version_id": cursor.lastrowid}
        except sqlite3.Error as exc:
            return self._err("record_package_version", "Database error recording package version", exc)

    def get_package_versions(self, project_slug: str) -> List[Dict[str, Any]]:
        """Return a project's package history in effective chronological order."""
        try:
            rows = self._conn.execute(
                """
                SELECT * FROM package_versions
                WHERE project_slug = ?
                ORDER BY effective_at, id
                """,
                (project_slug,),
            ).fetchall()
            return [dict(row) for row in rows]
        except sqlite3.Error:
            return []

    # =========================================================================
    # RECOMMENDATION / PREDICTION LEDGER
    # =========================================================================

    def record_recommendation(
        self,
        project_slug: str,
        decision_kind: str,
        recommendation: str,
        rationale: str,
        predicted_mechanism: str,
        *,
        expected_observation: Optional[str] = None,
        decision_status: str = "proposed",
        evidence_limitations: Optional[str] = None,
        recorded_at: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Record reasoning before an outcome is known; never calculate a score."""
        allowed_kinds = {"topic", "package", "workflow", "research", "business", "other"}
        allowed_statuses = {"proposed", "accepted", "rejected", "superseded", "reviewed"}
        if decision_kind not in allowed_kinds:
            return self._err("record_recommendation", "unknown decision kind")
        if decision_status not in allowed_statuses:
            return self._err("record_recommendation", "unknown decision status")
        required = (project_slug, recommendation, rationale, predicted_mechanism)
        if any(not value or not value.strip() for value in required):
            return self._err(
                "record_recommendation",
                "project, recommendation, rationale and predicted mechanism are required",
            )
        stamp = recorded_at or datetime.now(timezone.utc).isoformat()
        try:
            cursor = self._conn.execute(
                """
                INSERT INTO recommendation_ledger
                    (project_slug, decision_kind, recommendation, rationale,
                     predicted_mechanism, expected_observation, decision_status,
                     recorded_at, evidence_limitations)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    project_slug.strip(), decision_kind, recommendation.strip(),
                    rationale.strip(), predicted_mechanism.strip(),
                    expected_observation.strip() if expected_observation else None,
                    decision_status, stamp,
                    evidence_limitations.strip() if evidence_limitations else None,
                ),
            )
            self._conn.commit()
            return {"status": "inserted", "recommendation_id": cursor.lastrowid}
        except sqlite3.Error as exc:
            return self._err("record_recommendation", "Database error recording recommendation", exc)

    def record_recommendation_outcome(
        self,
        recommendation_id: int,
        outcome: str,
        revised_confidence: str,
        *,
        outcome_as_of: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Attach the observed outcome and the resulting confidence revision."""
        if not outcome.strip() or not revised_confidence.strip():
            return self._err(
                "record_recommendation_outcome",
                "outcome and revised confidence are required",
            )
        stamp = outcome_as_of or datetime.now(timezone.utc).isoformat()
        try:
            cursor = self._conn.execute(
                """
                UPDATE recommendation_ledger
                SET outcome = ?, outcome_as_of = ?, revised_confidence = ?,
                    decision_status = 'reviewed'
                WHERE id = ?
                """,
                (outcome.strip(), stamp, revised_confidence.strip(), recommendation_id),
            )
            if cursor.rowcount != 1:
                self._conn.rollback()
                return self._err(
                    "record_recommendation_outcome",
                    "recommendation not found",
                    recommendation_id=recommendation_id,
                )
            self._conn.commit()
            return {"status": "updated", "recommendation_id": recommendation_id}
        except sqlite3.Error as exc:
            return self._err(
                "record_recommendation_outcome",
                "Database error recording recommendation outcome",
                exc,
            )

    def get_recommendations(self, project_slug: str) -> List[Dict[str, Any]]:
        """Return the recorded reasoning chain in chronological order."""
        try:
            rows = self._conn.execute(
                """
                SELECT * FROM recommendation_ledger
                WHERE project_slug = ?
                ORDER BY recorded_at, id
                """,
                (project_slug,),
            ).fetchall()
            return [dict(row) for row in rows]
        except sqlite3.Error:
            return []

    def add_thumbnail_variant(
        self,
        video_id: str,
        variant_letter: str,
        file_path: str,
        visual_patterns: List[str],
        perceptual_hash: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Register a thumbnail variant for a video.

        Args:
            video_id: YouTube video ID
            variant_letter: Single uppercase letter (A-Z)
            file_path: Path to thumbnail file
            visual_patterns: List of visual pattern tags (e.g., ['map', 'face', 'text'])
            perceptual_hash: Optional perceptual hash (hex string from ImageHash)

        Returns:
            Success: {'status': 'inserted', 'variant_id': int}
            Failure: {'error': str}

        Example:
            result = db.add_thumbnail_variant(
                'TEST123', 'A', '/path/to/thumb.jpg', ['map', 'text'], 'abc123def456'
            )
        """
        try:
            if not variant_letter or len(variant_letter) != 1 or not variant_letter.isupper():
                return self._err('add_thumbnail_variant', 'variant_letter must be a single uppercase letter (A-Z)')

            if variant_letter < 'A' or variant_letter > 'Z':
                return self._err('add_thumbnail_variant', 'variant_letter must be between A and Z')

            cursor = self._conn.cursor()

            cursor.execute(
                """
                INSERT INTO thumbnail_variants
                (video_id, variant_letter, file_path, visual_pattern_tags, perceptual_hash, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    video_id,
                    variant_letter,
                    file_path,
                    json.dumps(visual_patterns),
                    perceptual_hash,
                    datetime.now(timezone.utc).date().isoformat()
                )
            )

            self._conn.commit()
            return {'status': 'inserted', 'variant_id': cursor.lastrowid}

        except sqlite3.Error as e:
            return self._err('add_thumbnail_variant', f'Database error: {str(e)}', e)

    def add_title_variant(
        self,
        video_id: str,
        variant_letter: str,
        title_text: str,
        formula_tags: List[str]
    ) -> Dict[str, Any]:
        """
        Register a title variant for a video.

        Args:
            video_id: YouTube video ID
            variant_letter: Single uppercase letter (A-Z)
            title_text: The title text
            formula_tags: List of formula tags (e.g., ['mechanism', 'document'])

        Returns:
            Success: {'status': 'inserted', 'variant_id': int}
            Failure: {'error': str}

        Example:
            result = db.add_title_variant(
                'TEST123', 'A', 'How Colonial Borders Still Kill Today', ['mechanism']
            )
        """
        try:
            if not variant_letter or len(variant_letter) != 1 or not variant_letter.isupper():
                return self._err('add_title_variant', 'variant_letter must be a single uppercase letter (A-Z)')

            if variant_letter < 'A' or variant_letter > 'Z':
                return self._err('add_title_variant', 'variant_letter must be between A and Z')

            cursor = self._conn.cursor()

            cursor.execute(
                """
                INSERT INTO title_variants
                (video_id, variant_letter, title_text, character_count, formula_tags, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    video_id,
                    variant_letter,
                    title_text,
                    len(title_text),
                    json.dumps(formula_tags),
                    datetime.now(timezone.utc).date().isoformat()
                )
            )

            self._conn.commit()
            return {'status': 'inserted', 'variant_id': cursor.lastrowid}

        except sqlite3.Error as e:
            return self._err('add_title_variant', f'Database error: {str(e)}', e)

    def add_ctr_snapshot(
        self,
        video_id: str,
        ctr_percent: float,
        impression_count: int,
        view_count: int,
        active_thumbnail_id: Optional[int] = None,
        active_title_id: Optional[int] = None,
        snapshot_date: Optional[str] = None,
        is_late_entry: bool = False
    ) -> Dict[str, Any]:
        """
        Record a CTR snapshot for a video.

        Args:
            video_id: YouTube video ID
            ctr_percent: CTR percentage (0-100)
            impression_count: Number of impressions
            view_count: Number of views
            active_thumbnail_id: ID of active thumbnail variant (optional)
            active_title_id: ID of active title variant (optional)
            snapshot_date: Date of snapshot (YYYY-MM-DD), defaults to today
            is_late_entry: Whether this is a late data entry (default False)

        Returns:
            Success: {'status': 'inserted', 'snapshot_id': int}
            Failure: {'error': str}

        Example:
            result = db.add_ctr_snapshot('TEST123', 4.5, 1000, 45)
        """
        try:
            if ctr_percent < 0 or ctr_percent > 100:
                return self._err('add_ctr_snapshot', 'ctr_percent must be between 0 and 100')

            if impression_count < 0 or view_count < 0:
                return self._err('add_ctr_snapshot', 'impression_count and view_count must be non-negative')

            if snapshot_date is None:
                snapshot_date = datetime.now(timezone.utc).date().isoformat()

            recorded_at = datetime.now(timezone.utc).date().isoformat()

            cursor = self._conn.cursor()

            cursor.execute(
                """
                INSERT INTO ctr_snapshots
                (video_id, snapshot_date, ctr_percent, impression_count, view_count,
                 active_thumbnail_id, active_title_id, recorded_at, is_late_entry)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    video_id,
                    snapshot_date,
                    ctr_percent,
                    impression_count,
                    view_count,
                    active_thumbnail_id,
                    active_title_id,
                    recorded_at,
                    1 if is_late_entry else 0
                )
            )

            self._conn.commit()
            return {'status': 'inserted', 'snapshot_id': cursor.lastrowid}

        except sqlite3.Error as e:
            return self._err('add_ctr_snapshot', f'Database error: {str(e)}', e)

    def get_thumbnail_variants(self, video_id: str) -> List[Dict[str, Any]]:
        """
        Get all thumbnail variants for a video.

        Args:
            video_id: YouTube video ID

        Returns:
            List of thumbnail variant dicts (empty list if none found)

        Example:
            variants = db.get_thumbnail_variants('TEST123')
            for v in variants:
                print(f"{v['variant_letter']}: {v['visual_pattern_tags']}")
        """
        try:
            cursor = self._conn.cursor()
            cursor.execute(
                """
                SELECT * FROM thumbnail_variants
                WHERE video_id = ?
                ORDER BY variant_letter
                """,
                (video_id,)
            )

            results = []
            for row in cursor.fetchall():
                variant_dict = dict(row)

                if variant_dict.get('visual_pattern_tags'):
                    try:
                        variant_dict['visual_pattern_tags'] = json.loads(variant_dict['visual_pattern_tags'])
                    except (json.JSONDecodeError, TypeError):
                        variant_dict['visual_pattern_tags'] = []

                results.append(variant_dict)

            return results

        except sqlite3.Error:
            return []

    def get_title_variants(self, video_id: str) -> List[Dict[str, Any]]:
        """
        Get all title variants for a video.

        Args:
            video_id: YouTube video ID

        Returns:
            List of title variant dicts (empty list if none found)

        Example:
            variants = db.get_title_variants('TEST123')
            for v in variants:
                print(f"{v['variant_letter']}: {v['title_text']} ({v['character_count']} chars)")
        """
        try:
            cursor = self._conn.cursor()
            cursor.execute(
                """
                SELECT * FROM title_variants
                WHERE video_id = ?
                ORDER BY variant_letter
                """,
                (video_id,)
            )

            results = []
            for row in cursor.fetchall():
                variant_dict = dict(row)

                if variant_dict.get('formula_tags'):
                    try:
                        variant_dict['formula_tags'] = json.loads(variant_dict['formula_tags'])
                    except (json.JSONDecodeError, TypeError):
                        variant_dict['formula_tags'] = []

                results.append(variant_dict)

            return results

        except sqlite3.Error:
            return []

    def get_ctr_snapshots(self, video_id: str) -> List[Dict[str, Any]]:
        """
        Get all CTR snapshots for a video, ordered by snapshot date.

        Args:
            video_id: YouTube video ID

        Returns:
            List of CTR snapshot dicts (empty list if none found)

        Example:
            snapshots = db.get_ctr_snapshots('TEST123')
            for s in snapshots:
                print(f"{s['snapshot_date']}: {s['ctr_percent']}% CTR")
        """
        try:
            cursor = self._conn.cursor()
            cursor.execute(
                """
                SELECT * FROM ctr_snapshots
                WHERE video_id = ?
                ORDER BY snapshot_date ASC
                """,
                (video_id,)
            )

            return [dict(row) for row in cursor.fetchall()]

        except sqlite3.Error:
            return []

    def get_variant_summary(self, video_id: str) -> Dict[str, Any]:
        """
        Get summary counts of variants and snapshots for a video.

        Args:
            video_id: YouTube video ID

        Returns:
            Dict with thumbnail_count, title_count, snapshot_count

        Example:
            summary = db.get_variant_summary('TEST123')
            print(f"Video has {summary['thumbnails']} thumbnails, {summary['titles']} titles")
        """
        try:
            cursor = self._conn.cursor()

            cursor.execute(
                "SELECT COUNT(*) as count FROM thumbnail_variants WHERE video_id = ?",
                (video_id,)
            )
            thumb_count = cursor.fetchone()['count']

            cursor.execute(
                "SELECT COUNT(*) as count FROM title_variants WHERE video_id = ?",
                (video_id,)
            )
            title_count = cursor.fetchone()['count']

            cursor.execute(
                "SELECT COUNT(*) as count FROM ctr_snapshots WHERE video_id = ?",
                (video_id,)
            )
            snapshot_count = cursor.fetchone()['count']

            return {
                'video_id': video_id,
                'thumbnails': thumb_count,
                'titles': title_count,
                'snapshots': snapshot_count
            }

        except sqlite3.Error as e:
            return {
                'video_id': video_id,
                'thumbnails': 0,
                'titles': 0,
                'snapshots': 0,
                'error': str(e)
            }

    def get_latest_ctr(self, video_id: str) -> Dict[str, Any]:
        """
        Get the most recent CTR snapshot for a video.

        Args:
            video_id: YouTube video ID

        Returns:
            Latest CTR snapshot dict, or {'error': 'not found'}

        Example:
            latest = db.get_latest_ctr('TEST123')
            if 'error' not in latest:
                print(f"Latest CTR: {latest['ctr_percent']}%")
        """
        try:
            cursor = self._conn.cursor()
            cursor.execute(
                """
                SELECT * FROM ctr_snapshots
                WHERE video_id = ?
                ORDER BY snapshot_date DESC
                LIMIT 1
                """,
                (video_id,)
            )

            row = cursor.fetchone()
            if row:
                return dict(row)
            else:
                return self._err('get_latest_ctr', 'not found')

        except sqlite3.Error as e:
            return self._err('get_latest_ctr', f'Database error: {str(e)}', e)

    # =========================================================================
    # CTR ANALYSIS METHODS (Phase 30)
    # =========================================================================

    def get_variant_ctr_summary(
        self,
        video_id: str,
        variant_type: str = 'thumbnail'
    ) -> List[Dict[str, Any]]:
        """
        Get CTR summary grouped by variant for a video.

        Aggregates CTR snapshots by active variant, returning average CTR,
        total impressions, and snapshot count per variant.

        Args:
            video_id: YouTube video ID
            variant_type: 'thumbnail' or 'title'

        Returns:
            List of dicts with keys:
                - variant_id: int
                - variant_letter: str
                - avg_ctr: float
                - total_impressions: int
                - snapshot_count: int
            Empty list if no attributed snapshots found.

        Example:
            summary = db.get_variant_ctr_summary('TEST123', 'thumbnail')
            for v in summary:
                print(f"Variant {v['variant_letter']}: {v['avg_ctr']:.1f}%")
        """
        try:
            cursor = self._conn.cursor()

            if variant_type == 'thumbnail':
                cursor.execute(
                    """
                    SELECT
                        s.active_thumbnail_id as variant_id,
                        t.variant_letter,
                        AVG(s.ctr_percent) as avg_ctr,
                        SUM(s.impression_count) as total_impressions,
                        COUNT(*) as snapshot_count
                    FROM ctr_snapshots s
                    JOIN thumbnail_variants t ON s.active_thumbnail_id = t.id
                    WHERE s.video_id = ? AND s.active_thumbnail_id IS NOT NULL
                    GROUP BY s.active_thumbnail_id, t.variant_letter
                    ORDER BY avg_ctr DESC
                    """,
                    (video_id,)
                )
            else:
                cursor.execute(
                    """
                    SELECT
                        s.active_title_id as variant_id,
                        t.variant_letter,
                        AVG(s.ctr_percent) as avg_ctr,
                        SUM(s.impression_count) as total_impressions,
                        COUNT(*) as snapshot_count
                    FROM ctr_snapshots s
                    JOIN title_variants t ON s.active_title_id = t.id
                    WHERE s.video_id = ? AND s.active_title_id IS NOT NULL
                    GROUP BY s.active_title_id, t.variant_letter
                    ORDER BY avg_ctr DESC
                    """,
                    (video_id,)
                )

            results = []
            for row in cursor.fetchall():
                results.append({
                    'variant_id': row[0],
                    'variant_letter': row[1],
                    'avg_ctr': row[2],
                    'total_impressions': row[3],
                    'snapshot_count': row[4]
                })

            return results

        except sqlite3.Error:
            return []

    def get_channel_ctr_benchmarks(self) -> Dict[str, Any]:
        """
        Get channel-wide CTR benchmarks by category.

        Uses the latest CTR snapshot per video to avoid bias from
        videos with more frequent snapshots. Groups by video_performance
        topic_type for category breakdown.

        Returns:
            Dict with keys:
                - overall: {avg_ctr, video_count, date_range: {earliest, latest}}
                - by_category: {category: {avg_ctr, video_count}}

        Example:
            benchmarks = db.get_channel_ctr_benchmarks()
            print(f"Overall avg: {benchmarks['overall']['avg_ctr']:.1f}%")
        """
        try:
            import statistics as stats

            # Canonical valid-latest CTR per video (is_valid=1, one row per
            # video, ctr>0 so quarantined double-count rows and unavailable
            # zeros don't drag the channel average). topic_type joined
            # separately. See tools/discovery/ctr_reads.py / ADR-0017.
            latest = latest_valid_ctr_by_video(self._conn, require_ctr=True)
            topic_map = {
                vid: (tt or 'general')
                for vid, tt in self._conn.execute(
                    "SELECT video_id, topic_type FROM video_performance"
                )
            }
            rows = [
                (vid, rec['ctr_percent'], rec['snapshot_date'],
                 topic_map.get(vid, 'general'))
                for vid, rec in latest.items()
            ]

            if not rows:
                return {
                    'overall': {
                        'avg_ctr': 0,
                        'video_count': 0,
                        'date_range': {'earliest': None, 'latest': None}
                    },
                    'by_category': {}
                }

            all_ctrs = []
            all_dates = []
            by_category = {}

            for row in rows:
                video_id, ctr, date, topic_type = row
                all_ctrs.append(ctr)
                all_dates.append(date)

                if topic_type not in by_category:
                    by_category[topic_type] = {'ctrs': [], 'count': 0}
                by_category[topic_type]['ctrs'].append(ctr)
                by_category[topic_type]['count'] += 1

            overall_avg = stats.mean(all_ctrs) if all_ctrs else 0
            dates_sorted = sorted([d for d in all_dates if d])

            category_stats = {}
            for cat, data in by_category.items():
                category_stats[cat] = {
                    'avg_ctr': stats.mean(data['ctrs']) if data['ctrs'] else 0,
                    'video_count': data['count']
                }

            return {
                'overall': {
                    'avg_ctr': overall_avg,
                    'video_count': len(all_ctrs),
                    'date_range': {
                        'earliest': dates_sorted[0] if dates_sorted else None,
                        'latest': dates_sorted[-1] if dates_sorted else None
                    }
                },
                'by_category': category_stats
            }

        except (sqlite3.Error, KeyError, TypeError, ZeroDivisionError):
            return {
                'overall': {
                    'avg_ctr': 0,
                    'video_count': 0,
                    'date_range': {'earliest': None, 'latest': None}
                },
                'by_category': {}
            }

    # =========================================================================
    # FEEDBACK LOOP METHODS (Phase 31)
    # =========================================================================

    def store_video_feedback(self, video_id: str, feedback_data: dict) -> dict:
        """
        Store parsed feedback from POST-PUBLISH-ANALYSIS file into video_performance table.

        Updates feedback columns with parsed insights:
        - retention_drop_point: biggest drop position percentage
        - discovery_issues: JSON-encoded discovery diagnostics
        - lessons_learned: JSON-encoded observations and actionable items

        Args:
            video_id: YouTube video ID
            feedback_data: Dict with keys:
                - biggest_drop_position: int (position percentage)
                - observations: list[str]
                - actionable: list[str]
                - discovery: dict (optional)

        Returns:
            {'status': 'updated', 'video_id': video_id} on success
            {'status': 'no_match', 'video_id': video_id} if video not in performance table
            {'error': msg} on failure

        Example:
            result = db.store_video_feedback('XbGl1Kcspt4', {
                'biggest_drop_position': 3,
                'observations': ['Strong retention'],
                'actionable': ['Consider similar content'],
                'discovery': {'primary_issue': 'NONE', 'severity': 'LOW'}
            })
        """
        try:
            cursor = self._conn.cursor()

            discovery = feedback_data.get('discovery', {})
            discovery_json = json.dumps(discovery) if discovery else None

            lessons = {
                'observations': feedback_data.get('observations', []),
                'actionable': feedback_data.get('actionable', [])
            }
            lessons_json = json.dumps(lessons)

            cursor.execute(
                """
                UPDATE video_performance
                SET retention_drop_point = ?,
                    discovery_issues = ?,
                    lessons_learned = ?
                WHERE video_id = ?
                """,
                (
                    feedback_data.get('biggest_drop_position'),
                    discovery_json,
                    lessons_json,
                    video_id
                )
            )

            self._conn.commit()

            if cursor.rowcount == 0:
                return {'status': 'no_match', 'video_id': video_id}

            return {'status': 'updated', 'video_id': video_id}

        except sqlite3.Error as e:
            return self._err('store_video_feedback', f'Database error: {str(e)}', e)

    def get_video_feedback(self, video_id: str) -> dict:
        """
        Retrieve feedback for a specific video.

        Args:
            video_id: YouTube video ID

        Returns:
            Dict with video info and feedback data:
                - video_id, title, topic_type, conversion_rate
                - drop_point: int or None
                - discovery: dict or None (parsed from JSON)
                - lessons: dict with observations/actionable lists (parsed from JSON)
            {'error': 'not_found'} if video not in table
            {'error': msg} on failure

        Example:
            feedback = db.get_video_feedback('XbGl1Kcspt4')
            if 'error' not in feedback:
                print(f"Observations: {feedback['lessons']['observations']}")
        """
        try:
            cursor = self._conn.cursor()
            cursor.execute(
                """
                SELECT video_id, title, topic_type, conversion_rate,
                       retention_drop_point, discovery_issues, lessons_learned
                FROM video_performance
                WHERE video_id = ?
                """,
                (video_id,)
            )

            row = cursor.fetchone()
            if not row:
                return self._err('get_video_feedback', 'not_found')

            discovery_issues = json.loads(row[5]) if row[5] else None
            lessons_learned = json.loads(row[6]) if row[6] else None

            return {
                'video_id': row[0],
                'title': row[1],
                'topic_type': row[2],
                'conversion_rate': row[3],
                'drop_point': row[4],
                'discovery': discovery_issues,
                'lessons': lessons_learned
            }

        except sqlite3.Error as e:
            return self._err('get_video_feedback', f'Database error: {str(e)}', e)
        except json.JSONDecodeError as e:
            return self._err('get_video_feedback', f'JSON parse error: {str(e)}', e)

    def get_feedback_by_topic(self, topic_type: str, limit: int = 10) -> dict:
        """
        Retrieve feedback from videos in a specific topic category.

        Queries videos with lessons_learned data, ordered by conversion_rate descending
        (highest performing videos first).

        Args:
            topic_type: Topic category ('territorial', 'ideological', 'legal', etc.)
            limit: Maximum number of videos to return

        Returns:
            Dict with:
                - videos: list of video dicts with feedback
                - count: number of videos returned
                - topic: topic_type queried

        Example:
            result = db.get_feedback_by_topic('territorial', limit=5)
            for video in result['videos']:
                print(f"{video['title']}: {video['lessons']['observations']}")
        """
        try:
            cursor = self._conn.cursor()
            cursor.execute(
                """
                SELECT video_id, title, topic_type, conversion_rate,
                       retention_drop_point, lessons_learned
                FROM video_performance
                WHERE topic_type = ? AND lessons_learned IS NOT NULL
                ORDER BY conversion_rate DESC
                LIMIT ?
                """,
                (topic_type, limit)
            )

            rows = cursor.fetchall()
            videos = []

            for row in rows:
                lessons = json.loads(row[5]) if row[5] else {'observations': [], 'actionable': []}

                videos.append({
                    'video_id': row[0],
                    'title': row[1],
                    'topic_type': row[2],
                    'conversion_rate': row[3],
                    'drop_point': row[4],
                    'lessons': lessons
                })

            return {
                'videos': videos,
                'count': len(videos),
                'topic': topic_type
            }

        except sqlite3.Error as e:
            return self._err('get_feedback_by_topic', f'Database error: {str(e)}', e)
        except json.JSONDecodeError as e:
            return self._err('get_feedback_by_topic', f'JSON parse error: {str(e)}', e)

    def has_feedback(self, video_id: str) -> bool:
        """
        Check if video has feedback stored.

        Quick boolean check for whether lessons_learned is populated.

        Args:
            video_id: YouTube video ID

        Returns:
            True if video has lessons_learned data, False otherwise

        Example:
            if db.has_feedback('XbGl1Kcspt4'):
                print("Feedback available")
        """
        try:
            cursor = self._conn.cursor()
            cursor.execute(
                """
                SELECT lessons_learned
                FROM video_performance
                WHERE video_id = ? AND lessons_learned IS NOT NULL
                """,
                (video_id,)
            )

            return cursor.fetchone() is not None

        except sqlite3.Error:
            return False
