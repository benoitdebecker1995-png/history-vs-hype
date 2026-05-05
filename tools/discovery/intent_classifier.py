"""
Intent Classifier Module

Extracted from database.py (Phase H5 refactor). Owns all 4 methods related to
competitor video tracking and content format classification.

Usage:
    from tools.discovery.intent_classifier import IntentClassifier

    clf = IntentClassifier.connect()
    clf.add_competitor_video('vid123', channel_id=1, keyword_id=5, title='...')
    clf.close()
"""

import sqlite3
import json
from datetime import datetime, timezone
from typing import Optional, Dict, List, Any

from tools.logging_config import get_logger

logger = get_logger(__name__)


class IntentClassifier:
    """
    Competitor video intelligence and content classification.

    Wraps an injected sqlite3.Connection. Use connect() to construct from a
    full KeywordDB path, or pass a connection directly for testing.
    """

    def __init__(self, conn: sqlite3.Connection) -> None:
        self._conn = conn
        self._ensure_classification_columns()

    @classmethod
    def connect(cls, db_path: Optional[str] = None) -> 'IntentClassifier':
        from tools.discovery.database import KeywordDB  # deferred — avoids circular import
        kdb = KeywordDB(db_path)
        obj = object.__new__(cls)
        obj._conn = kdb._conn
        return obj

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

    def _table_exists(self, table_name: str) -> bool:
        cursor = self._conn.cursor()
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
            (table_name,)
        )
        return cursor.fetchone() is not None

    def _ensure_classification_columns(self) -> None:
        """Safely add classification columns to competitor_videos if they don't exist."""
        if not self._table_exists('competitor_videos'):
            return  # Will be created during init_database()

        cursor = self._conn.cursor()
        cursor.execute("PRAGMA table_info(competitor_videos)")
        existing_columns = {row[1] for row in cursor.fetchall()}

        columns_to_add = {
            'format': 'ALTER TABLE competitor_videos ADD COLUMN format TEXT',
            'angles': 'ALTER TABLE competitor_videos ADD COLUMN angles TEXT',
            'quality_tier': 'ALTER TABLE competitor_videos ADD COLUMN quality_tier TEXT',
            'classified_at': 'ALTER TABLE competitor_videos ADD COLUMN classified_at DATE'
        }

        with self._conn:
            for col_name, alter_sql in columns_to_add.items():
                if col_name not in existing_columns:
                    self._conn.execute(alter_sql)
            self._conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_competitor_format ON competitor_videos(keyword_id, format)"
            )
            self._conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_competitor_quality ON competitor_videos(keyword_id, quality_tier)"
            )

    # =========================================================================
    # COMPETITOR VIDEO METHODS
    # =========================================================================

    def add_competitor_video(
        self,
        video_id: str,
        channel_id: int,
        keyword_id: int,
        title: str,
        view_count: Optional[int] = None,
        published_at: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Add a competitor video for a keyword.

        Args:
            video_id: YouTube video ID
            channel_id: Database ID from competitor_channels table
            keyword_id: Keyword ID
            title: Video title
            view_count: Optional view count
            published_at: Optional publish date (ISO format)

        Returns:
            {'status': 'inserted'} on success
            {'error': msg} on failure
        """
        try:
            cursor = self._conn.cursor()
            now = datetime.now(timezone.utc).date().isoformat()

            video_age_days = None
            if published_at:
                try:
                    pub_date = datetime.fromisoformat(published_at.replace('Z', '+00:00'))
                    video_age_days = (datetime.now(timezone.utc) - pub_date.replace(tzinfo=None)).days
                except (ValueError, TypeError):
                    pass

            cursor.execute(
                """
                INSERT INTO competitor_videos (video_id, channel_id, keyword_id, title, view_count, published_at, video_age_days, discovered_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (video_id, channel_id, keyword_id, title, view_count, published_at, video_age_days, now)
            )

            self._conn.commit()

            return {'status': 'inserted'}

        except sqlite3.IntegrityError as e:
            return self._err('add_competitor_video', 'Integrity constraint violated', e)
        except sqlite3.OperationalError as e:
            return self._err('add_competitor_video', 'Database operation failed', e)

    def get_competition_count(self, keyword_id: int, max_age_days: int = 7) -> Optional[Dict[str, Any]]:
        """
        Get competition count for a keyword.

        Args:
            keyword_id: Keyword ID
            max_age_days: Maximum age in days for cached data

        Returns:
            {'video_count': int, 'channel_count': int, 'data_age_days': int} or None
        """
        try:
            cursor = self._conn.cursor()

            cursor.execute(
                """
                SELECT
                    COUNT(DISTINCT cv.video_id) AS video_count,
                    COUNT(DISTINCT cv.channel_id) AS channel_count,
                    CAST(MIN(julianday('now') - julianday(cv.discovered_at)) AS INTEGER) AS data_age_days
                FROM competitor_videos cv
                WHERE cv.keyword_id = ?
                    AND julianday('now') - julianday(cv.discovered_at) <= ?
                """,
                (keyword_id, max_age_days)
            )

            row = cursor.fetchone()

            if row is None or row['video_count'] == 0:
                return None

            return {
                'video_count': row['video_count'],
                'channel_count': row['channel_count'],
                'data_age_days': row['data_age_days'] if row['data_age_days'] is not None else 0
            }

        except sqlite3.Error:
            return None

    def update_video_classification(
        self,
        video_id: str,
        format_type: str,
        angles: List[str],
        quality_tier: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Update classification data for a competitor video.

        Args:
            video_id: YouTube video ID
            format_type: 'animation', 'documentary', or 'unknown'
            angles: List of angle categories (e.g., ['legal', 'historical'])
            quality_tier: Optional quality tier ('high', 'medium', 'low')

        Returns:
            {'status': 'updated'} on success
            {'error': msg} on failure
        """
        try:
            cursor = self._conn.cursor()
            now = datetime.now(timezone.utc).date().isoformat()

            angles_json = json.dumps(angles)

            cursor.execute(
                """
                UPDATE competitor_videos
                SET format = ?,
                    angles = ?,
                    quality_tier = ?,
                    classified_at = ?
                WHERE video_id = ?
                """,
                (format_type, angles_json, quality_tier, now, video_id)
            )

            self._conn.commit()

            if cursor.rowcount == 0:
                return self._err('update_video_classification', 'Video not found', video_id=video_id)

            return {'status': 'updated'}

        except sqlite3.Error as e:
            return self._err('update_video_classification', 'Database operation failed', e)

    def get_classified_videos(
        self,
        keyword_id: int,
        format_filter: Optional[str] = None,
        quality_filter: Optional[str] = None,
        max_age_days: int = 30
    ) -> List[Dict[str, Any]]:
        """
        Get classified videos for a keyword with optional filtering.

        Args:
            keyword_id: Keyword ID
            format_filter: Optional format to filter by ('animation', 'documentary')
            quality_filter: Optional quality tier to filter by ('high', 'medium', 'low')
            max_age_days: Maximum classification age in days

        Returns:
            List of video dicts with classification data and data_age_days field
        """
        try:
            cursor = self._conn.cursor()

            query = """
                SELECT *,
                    CAST((julianday('now') - julianday(classified_at)) AS INTEGER) AS data_age_days
                FROM competitor_videos
                WHERE keyword_id = ?
                    AND classified_at IS NOT NULL
            """
            params: List[Any] = [keyword_id]

            if format_filter:
                query += " AND format = ?"
                params.append(format_filter)

            if quality_filter:
                query += " AND quality_tier = ?"
                params.append(quality_filter)

            query += " AND julianday('now') - julianday(classified_at) <= ?"
            params.append(max_age_days)

            query += " ORDER BY classified_at DESC"

            cursor.execute(query, params)

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
