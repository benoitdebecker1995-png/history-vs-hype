"""
Keyword Database Module

SQLite connection and CRUD operations for keyword discovery database.
Follows error dict pattern from existing tools (returns {'error': msg} on failure).

Usage:
    from database import KeywordDB

    db = KeywordDB()
    db.add_keyword('dark ages myth', source='autocomplete')
    results = db.search_keywords('dark%')

Database location: tools/discovery/keywords.db (relative to module)
"""

import sqlite3
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List, Any


class KeywordDB:
    """
    SQLite database connection and operations for keyword tracking.

    All methods return dicts with results or {'error': msg} on failure.
    Uses context manager for transactions.
    """

    def __init__(self, db_path: Optional[str] = None):
        """
        Initialize database connection.

        Args:
            db_path: Path to SQLite database (default: keywords.db in module directory)
        """
        if db_path is None:
            module_dir = Path(__file__).parent
            db_path = str(module_dir / 'keywords.db')

        self.db_path = db_path
        self._conn = None
        self._ensure_connection()

    def _ensure_connection(self):
        """Ensure database connection exists and initialize if needed"""
        if self._conn is None:
            self._conn = sqlite3.connect(self.db_path)
            self._conn.row_factory = sqlite3.Row

            # Check if database needs initialization
            cursor = self._conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='keywords'")

            if cursor.fetchone() is None:
                # Database needs initialization
                self.init_database()

    def init_database(self) -> Dict[str, Any]:
        """
        Initialize database from schema.sql.

        Returns:
            {'status': 'initialized', 'tables': [...]} on success
            {'error': msg} on failure
        """
        try:
            schema_path = Path(__file__).parent / 'schema.sql'

            if not schema_path.exists():
                return {
                    'error': 'schema.sql not found',
                    'path': str(schema_path)
                }

            schema_sql = schema_path.read_text(encoding='utf-8')

            cursor = self._conn.cursor()
            cursor.executescript(schema_sql)
            self._conn.commit()

            # Verify tables created
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
            tables = [row[0] for row in cursor.fetchall()]

            return {
                'status': 'initialized',
                'tables': tables,
                'database': self.db_path
            }

        except sqlite3.Error as e:
            return {
                'error': f'Database initialization failed: {type(e).__name__}',
                'details': str(e)
            }
        except Exception as e:
            return {
                'error': f'Unexpected error during initialization: {type(e).__name__}',
                'details': str(e)
            }

    def add_keyword(
        self,
        keyword: str,
        source: str = 'manual',
        search_volume: Optional[int] = None,
        competition: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Add or update keyword in database.

        Args:
            keyword: Keyword text
            source: Source ('autocomplete', 'manual', 'competitor', 'vidiq')
            search_volume: Optional search volume estimate
            competition: Optional competition score 0-100

        Returns:
            {'keyword_id': int, 'keyword': str, 'action': 'inserted'|'updated'} on success
            {'error': msg} on failure
        """
        try:
            cursor = self._conn.cursor()
            now = datetime.utcnow().date().isoformat()

            # Check if keyword exists
            cursor.execute("SELECT id, first_discovered FROM keywords WHERE keyword = ?", (keyword,))
            existing = cursor.fetchone()

            if existing:
                # Update existing
                keyword_id = existing['id']
                first_discovered = existing['first_discovered']

                cursor.execute(
                    """
                    UPDATE keywords
                    SET search_volume = COALESCE(?, search_volume),
                        competition_score = COALESCE(?, competition_score),
                        last_updated = ?,
                        source = ?
                    WHERE id = ?
                    """,
                    (search_volume, competition, now, source, keyword_id)
                )
                action = 'updated'
            else:
                # Insert new
                cursor.execute(
                    """
                    INSERT INTO keywords (keyword, search_volume, competition_score, first_discovered, last_updated, source)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (keyword, search_volume, competition, now, now, source)
                )
                keyword_id = cursor.lastrowid
                action = 'inserted'

            self._conn.commit()

            return {
                'keyword_id': keyword_id,
                'keyword': keyword,
                'action': action
            }

        except sqlite3.Error as e:
            return {
                'error': f'Database error adding keyword: {type(e).__name__}',
                'details': str(e)
            }
        except Exception as e:
            return {
                'error': f'Unexpected error: {type(e).__name__}',
                'details': str(e)
            }

    def get_keyword(self, keyword: str) -> Dict[str, Any]:
        """
        Retrieve keyword by exact match.

        Args:
            keyword: Exact keyword to find

        Returns:
            Keyword record dict on success
            {'error': msg} if not found or error
        """
        try:
            cursor = self._conn.cursor()
            cursor.execute("SELECT * FROM keywords WHERE keyword = ?", (keyword,))
            row = cursor.fetchone()

            if row is None:
                return {
                    'error': 'Keyword not found',
                    'keyword': keyword
                }

            return dict(row)

        except sqlite3.Error as e:
            return {
                'error': f'Database error: {type(e).__name__}',
                'details': str(e)
            }

    def search_keywords(self, pattern: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Search keywords with LIKE pattern.

        Args:
            pattern: SQL LIKE pattern (e.g., 'dark%', '%myth%'). None = all keywords.
            limit: Maximum results to return

        Returns:
            List of keyword dicts (empty list if none found)
        """
        try:
            cursor = self._conn.cursor()

            if pattern is None:
                cursor.execute("SELECT * FROM keywords ORDER BY last_updated DESC LIMIT ?", (limit,))
            else:
                cursor.execute(
                    "SELECT * FROM keywords WHERE keyword LIKE ? ORDER BY last_updated DESC LIMIT ?",
                    (pattern, limit)
                )

            return [dict(row) for row in cursor.fetchall()]

        except sqlite3.Error:
            return []

    def get_keywords_by_source(self, source: str, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Get keywords by source.

        Args:
            source: Source to filter by ('autocomplete', 'manual', 'competitor', 'vidiq')
            limit: Maximum results

        Returns:
            List of keyword dicts (empty list if none found)
        """
        try:
            cursor = self._conn.cursor()
            cursor.execute(
                "SELECT * FROM keywords WHERE source = ? ORDER BY last_updated DESC LIMIT ?",
                (source, limit)
            )
            return [dict(row) for row in cursor.fetchall()]

        except sqlite3.Error:
            return []

    def get_keywords_by_intent(self, intent_category: str, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Get keywords by intent category.

        Args:
            intent_category: Intent to filter by (e.g., 'MYTH_BUSTING')
            limit: Maximum results

        Returns:
            List of keyword dicts with intent data (empty list if none found)
        """
        try:
            cursor = self._conn.cursor()
            cursor.execute(
                """
                SELECT k.*, ki.intent_category, ki.confidence, ki.is_primary
                FROM keywords k
                JOIN keyword_intents ki ON k.id = ki.keyword_id
                WHERE ki.intent_category = ?
                ORDER BY ki.confidence DESC, k.last_updated DESC
                LIMIT ?
                """,
                (intent_category, limit)
            )
            return [dict(row) for row in cursor.fetchall()]

        except sqlite3.Error:
            return []

    def set_intent(
        self,
        keyword_id: int,
        category: str,
        confidence: float,
        is_primary: bool = False
    ) -> Dict[str, Any]:
        """
        Set intent classification for keyword.

        Args:
            keyword_id: Keyword ID
            category: Intent category (e.g., 'MYTH_BUSTING', 'TERRITORIAL_DISPUTE')
            confidence: Confidence score 0-1
            is_primary: Whether this is the primary intent

        Returns:
            {'status': 'set', 'keyword_id': int, 'intent': str} on success
            {'error': msg} on failure
        """
        try:
            cursor = self._conn.cursor()

            # If setting as primary, unset other primaries for this keyword
            if is_primary:
                cursor.execute(
                    "UPDATE keyword_intents SET is_primary = 0 WHERE keyword_id = ?",
                    (keyword_id,)
                )

            # Insert or update intent
            cursor.execute(
                """
                INSERT INTO keyword_intents (keyword_id, intent_category, confidence, is_primary)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(keyword_id, intent_category) DO UPDATE SET
                    confidence = excluded.confidence,
                    is_primary = excluded.is_primary
                """,
                (keyword_id, category, confidence, is_primary)
            )

            self._conn.commit()

            return {
                'status': 'set',
                'keyword_id': keyword_id,
                'intent': category,
                'confidence': confidence,
                'is_primary': is_primary
            }

        except sqlite3.Error as e:
            return {
                'error': f'Database error setting intent: {type(e).__name__}',
                'details': str(e)
            }

    def add_performance(
        self,
        keyword_id: int,
        video_id: str,
        impressions: Optional[int] = None,
        ctr: Optional[float] = None,
        views: Optional[int] = None,
        watch_time_minutes: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Track keyword performance for a video.

        Args:
            keyword_id: Keyword ID
            video_id: YouTube video ID
            impressions: Impression count
            ctr: Click-through rate (0-1)
            views: View count
            watch_time_minutes: Total watch time

        Returns:
            {'status': 'tracked', 'performance_id': int} on success
            {'error': msg} on failure
        """
        try:
            cursor = self._conn.cursor()
            now = datetime.utcnow().date().isoformat()

            cursor.execute(
                """
                INSERT INTO keyword_performance (keyword_id, video_id, impressions, ctr, views, watch_time_minutes, measured_date)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (keyword_id, video_id, impressions, ctr, views, watch_time_minutes, now)
            )

            self._conn.commit()

            return {
                'status': 'tracked',
                'performance_id': cursor.lastrowid
            }

        except sqlite3.Error as e:
            return {
                'error': f'Database error tracking performance: {type(e).__name__}',
                'details': str(e)
            }

    def get_keyword_stats(self) -> Dict[str, Any]:
        """
        Get summary statistics about keyword database.

        Returns:
            Dict with statistics (empty dict on error)
        """
        try:
            cursor = self._conn.cursor()

            # Total keywords
            cursor.execute("SELECT COUNT(*) FROM keywords")
            total_keywords = cursor.fetchone()[0]

            # Keywords by source
            cursor.execute("SELECT source, COUNT(*) FROM keywords GROUP BY source")
            by_source = {row[0]: row[1] for row in cursor.fetchall()}

            # Keywords with intents
            cursor.execute("SELECT COUNT(DISTINCT keyword_id) FROM keyword_intents")
            with_intent = cursor.fetchone()[0]

            # Keywords with performance data
            cursor.execute("SELECT COUNT(DISTINCT keyword_id) FROM keyword_performance")
            with_performance = cursor.fetchone()[0]

            return {
                'total_keywords': total_keywords,
                'by_source': by_source,
                'with_intent': with_intent,
                'with_performance': with_performance
            }

        except sqlite3.Error:
            return {}

    def close(self):
        """Close database connection"""
        if self._conn:
            self._conn.close()
            self._conn = None


def init_database(db_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Convenience function to initialize database.

    Args:
        db_path: Optional path to database file

    Returns:
        Result dict from KeywordDB.init_database()
    """
    db = KeywordDB(db_path)
    result = db.init_database()
    db.close()
    return result
