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
import json
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
            else:
                # Ensure classification columns exist (Phase 16 migration)
                self._ensure_classification_columns()
                # Ensure production constraint columns exist (Phase 17 migration)
                self._ensure_production_columns()
                # Ensure lifecycle columns exist (Phase 18 migration)
                self._ensure_lifecycle_columns()
                # Ensure video_performance table exists (Phase 19 migration)
                self._ensure_performance_table()
                # Ensure Phase 27 tables exist
                self._ensure_variant_tables()
                self._ensure_ctr_snapshots_table()
                self._ensure_feedback_tables()

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

    # =========================================================================
    # DEMAND RESEARCH METHODS (Phase 15)
    # =========================================================================

    def add_trend(
        self,
        keyword_id: int,
        interest: int,
        trend_direction: str,
        percent_change: float,
        region: str = 'US'
    ) -> Dict[str, Any]:
        """
        Add trend data for a keyword.

        Args:
            keyword_id: Keyword ID
            interest: Normalized interest 0-100
            trend_direction: 'rising', 'stable', or 'declining'
            percent_change: Percentage change (+45.2 or -20.1)
            region: Region code (default 'US')

        Returns:
            {'status': 'inserted', 'trend_id': int} on success
            {'error': msg} on failure
        """
        try:
            cursor = self._conn.cursor()
            now = datetime.utcnow().isoformat()

            cursor.execute(
                """
                INSERT INTO trends (keyword_id, fetched_at, interest, trend_direction, percent_change, region)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (keyword_id, now, interest, trend_direction, percent_change, region)
            )

            self._conn.commit()

            return {
                'status': 'inserted',
                'trend_id': cursor.lastrowid
            }

        except sqlite3.IntegrityError as e:
            return {'error': 'Integrity constraint violated', 'details': str(e)}
        except sqlite3.OperationalError as e:
            return {'error': 'Database operation failed', 'details': str(e)}

    def get_cached_trend(self, keyword_id: int, max_age_days: int = 7) -> Optional[Dict[str, Any]]:
        """
        Get cached trend data if not expired.

        Args:
            keyword_id: Keyword ID
            max_age_days: Maximum age in days (default 7, use 0 for force refresh, 999 for stale fallback)

        Returns:
            Trend dict with data_age_days field, or None if not found/expired
        """
        try:
            cursor = self._conn.cursor()

            cursor.execute(
                """
                SELECT *,
                    CAST((julianday('now') - julianday(fetched_at)) AS INTEGER) AS data_age_days
                FROM trends
                WHERE keyword_id = ?
                ORDER BY fetched_at DESC
                LIMIT 1
                """,
                (keyword_id,)
            )

            row = cursor.fetchone()

            if row is None:
                return None

            result = dict(row)

            # Check if data is too old (unless max_age_days is very large for stale fallback)
            if result['data_age_days'] > max_age_days:
                return None

            return result

        except sqlite3.Error:
            return None

    def get_latest_trend(self, keyword_id: int) -> Dict[str, Any]:
        """
        Get most recent trend record regardless of age.

        Args:
            keyword_id: Keyword ID

        Returns:
            Trend dict on success
            {'error': 'not found'} if no trend data exists
        """
        try:
            cursor = self._conn.cursor()

            cursor.execute(
                """
                SELECT *,
                    CAST((julianday('now') - julianday(fetched_at)) AS INTEGER) AS data_age_days
                FROM trends
                WHERE keyword_id = ?
                ORDER BY fetched_at DESC
                LIMIT 1
                """,
                (keyword_id,)
            )

            row = cursor.fetchone()

            if row is None:
                return {'error': 'not found'}

            return dict(row)

        except sqlite3.Error as e:
            return {'error': 'Database operation failed', 'details': str(e)}

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
            now = datetime.utcnow().date().isoformat()

            # Calculate video age if published_at is provided
            video_age_days = None
            if published_at:
                try:
                    pub_date = datetime.fromisoformat(published_at.replace('Z', '+00:00'))
                    video_age_days = (datetime.utcnow() - pub_date.replace(tzinfo=None)).days
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
            return {'error': 'Integrity constraint violated', 'details': str(e)}
        except sqlite3.OperationalError as e:
            return {'error': 'Database operation failed', 'details': str(e)}

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

            # Get video and channel counts with data age
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

    def add_opportunity_score(
        self,
        keyword_id: int,
        demand_score: float,
        competition_score: float,
        opportunity_ratio: float,
        category: str
    ) -> Dict[str, Any]:
        """
        Add calculated opportunity score for a keyword.

        Args:
            keyword_id: Keyword ID
            demand_score: Autocomplete position proxy (0-100)
            competition_score: Video + channel count
            opportunity_ratio: demand/competition
            category: 'High', 'Medium', or 'Low'

        Returns:
            {'status': 'inserted'} on success
            {'error': msg} on failure
        """
        try:
            cursor = self._conn.cursor()
            now = datetime.utcnow().date().isoformat()

            cursor.execute(
                """
                INSERT INTO opportunity_scores (keyword_id, demand_score, competition_score, opportunity_ratio, opportunity_category, calculated_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (keyword_id, demand_score, competition_score, opportunity_ratio, category, now)
            )

            self._conn.commit()

            return {'status': 'inserted'}

        except sqlite3.IntegrityError as e:
            return {'error': 'Integrity constraint violated', 'details': str(e)}
        except sqlite3.OperationalError as e:
            return {'error': 'Database operation failed', 'details': str(e)}

    def get_opportunity_score(self, keyword_id: int, max_age_days: int = 7) -> Optional[Dict[str, Any]]:
        """
        Get cached opportunity score for a keyword.

        Args:
            keyword_id: Keyword ID
            max_age_days: Maximum age in days

        Returns:
            Opportunity score dict with data_age_days, or None if not found/expired
        """
        try:
            cursor = self._conn.cursor()

            cursor.execute(
                """
                SELECT *,
                    CAST((julianday('now') - julianday(calculated_at)) AS INTEGER) AS data_age_days
                FROM opportunity_scores
                WHERE keyword_id = ?
                ORDER BY calculated_at DESC
                LIMIT 1
                """,
                (keyword_id,)
            )

            row = cursor.fetchone()

            if row is None:
                return None

            result = dict(row)

            # Check if data is too old
            if result['data_age_days'] > max_age_days:
                return None

            return result

        except sqlite3.Error:
            return None

    # =========================================================================
    # CLASSIFICATION METHODS (Phase 16)
    # =========================================================================

    def _ensure_classification_columns(self):
        """
        Safely add classification columns to competitor_videos if they don't exist.

        This allows existing databases to migrate without manual schema updates.
        Executes ALTER TABLE statements for each missing column.
        """
        try:
            cursor = self._conn.cursor()

            # Check which columns exist
            cursor.execute("PRAGMA table_info(competitor_videos)")
            existing_columns = {row[1] for row in cursor.fetchall()}

            # Add missing classification columns
            columns_to_add = {
                'format': 'ALTER TABLE competitor_videos ADD COLUMN format TEXT',
                'angles': 'ALTER TABLE competitor_videos ADD COLUMN angles TEXT',
                'quality_tier': 'ALTER TABLE competitor_videos ADD COLUMN quality_tier TEXT',
                'classified_at': 'ALTER TABLE competitor_videos ADD COLUMN classified_at DATE'
            }

            for col_name, alter_sql in columns_to_add.items():
                if col_name not in existing_columns:
                    cursor.execute(alter_sql)

            # Create indexes if they don't exist
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_competitor_format ON competitor_videos(keyword_id, format)"
            )
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_competitor_quality ON competitor_videos(keyword_id, quality_tier)"
            )

            self._conn.commit()

        except sqlite3.Error:
            # If table doesn't exist yet, this is fine (will be created during init)
            pass

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

        Example:
            db.update_video_classification(
                'abc123',
                'documentary',
                ['legal', 'historical'],
                'high'
            )
        """
        try:
            import json

            cursor = self._conn.cursor()
            now = datetime.utcnow().date().isoformat()

            # Convert angles list to JSON string
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
                return {'error': 'Video not found', 'video_id': video_id}

            return {'status': 'updated'}

        except sqlite3.Error as e:
            return {'error': 'Database operation failed', 'details': str(e)}

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

        Example:
            videos = db.get_classified_videos(
                keyword_id=5,
                format_filter='documentary',
                quality_filter='high',
                max_age_days=7
            )
        """
        try:
            import json

            cursor = self._conn.cursor()

            # Build query with optional filters
            query = """
                SELECT *,
                    CAST((julianday('now') - julianday(classified_at)) AS INTEGER) AS data_age_days
                FROM competitor_videos
                WHERE keyword_id = ?
                    AND classified_at IS NOT NULL
            """
            params = [keyword_id]

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

                # Parse angles JSON back to list
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
    # PRODUCTION CONSTRAINT METHODS (Phase 17)
    # =========================================================================

    def _ensure_production_columns(self):
        """
        Safely add production constraint columns to keywords if they don't exist.

        This allows existing databases to migrate without manual schema updates.
        Executes ALTER TABLE statements for each missing column.
        """
        try:
            cursor = self._conn.cursor()

            # Check which columns exist in keywords table
            cursor.execute("PRAGMA table_info(keywords)")
            existing_columns = {row[1] for row in cursor.fetchall()}

            # Add missing production constraint columns
            columns_to_add = {
                'production_constraints': 'ALTER TABLE keywords ADD COLUMN production_constraints TEXT',
                'constraint_checked_at': 'ALTER TABLE keywords ADD COLUMN constraint_checked_at DATE',
                'is_production_blocked': 'ALTER TABLE keywords ADD COLUMN is_production_blocked BOOLEAN DEFAULT 0'
            }

            for col_name, alter_sql in columns_to_add.items():
                if col_name not in existing_columns:
                    cursor.execute(alter_sql)

            # Create index if it doesn't exist
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_keywords_blocked ON keywords(is_production_blocked, constraint_checked_at DESC)"
            )

            self._conn.commit()

        except sqlite3.Error:
            # If table doesn't exist yet, this is fine (will be created during init)
            pass

    def store_production_constraints(
        self,
        keyword_id: int,
        animation_required: bool,
        document_score: int,
        sources_found: int = 0,
        source_examples: Optional[List[str]] = None,
        source_hints: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Store production constraint evaluation for a keyword.

        Constraints are stored as JSON for flexibility. Keywords requiring
        animation are marked as blocked for quick filtering.

        Args:
            keyword_id: Keyword ID from keywords table
            animation_required: True if topic requires animation (hard block)
            document_score: 0-4 document-friendliness score
            sources_found: Number of academic sources found (0 if not checked)
            source_examples: Optional list of example source names
            source_hints: Optional dict with search queries and expected types

        Returns:
            {'status': 'stored', 'keyword_id': keyword_id} on success
            {'error': msg} on failure

        Example:
            db.store_production_constraints(
                keyword_id=5,
                animation_required=False,
                document_score=3,
                sources_found=5,
                source_examples=['Cambridge Press Book', 'JSTOR Article'],
                source_hints={'queries': [...], 'expected_types': ['monograph']}
            )
        """
        try:
            import json

            cursor = self._conn.cursor()
            now = datetime.utcnow().date().isoformat()

            # Build constraints JSON
            constraints = {
                'animation_required': animation_required,
                'document_score': document_score,
                'sources_found': sources_found,
                'source_examples': source_examples or [],
                'source_hints': source_hints or {},
                'checked_at': now
            }
            constraints_json = json.dumps(constraints)

            # is_production_blocked = True if animation required
            is_blocked = 1 if animation_required else 0

            cursor.execute(
                """
                UPDATE keywords
                SET production_constraints = ?,
                    constraint_checked_at = ?,
                    is_production_blocked = ?
                WHERE id = ?
                """,
                (constraints_json, now, is_blocked, keyword_id)
            )

            self._conn.commit()

            if cursor.rowcount == 0:
                return {'error': 'Keyword not found', 'keyword_id': keyword_id}

            return {'status': 'stored', 'keyword_id': keyword_id}

        except sqlite3.Error as e:
            return {'error': 'Database operation failed', 'details': str(e)}

    def get_production_constraints(
        self,
        keyword_id: int,
        max_age_days: int = 90
    ) -> Optional[Dict[str, Any]]:
        """
        Retrieve production constraint evaluation for a keyword.

        Returns None if not found or too old.

        Args:
            keyword_id: Keyword ID from keywords table
            max_age_days: Maximum age of constraint check in days (default 90)

        Returns:
            {
                'animation_required': bool,
                'document_score': int,
                'sources_found': int,
                'source_examples': list,
                'source_hints': dict,
                'checked_at': str,
                'is_production_blocked': bool,
                'data_age_days': int
            }
            or None if not found or too old

        Example:
            constraints = db.get_production_constraints(keyword_id=5)
            if constraints and constraints['is_production_blocked']:
                print("Skip this topic - requires animation")
        """
        try:
            import json

            cursor = self._conn.cursor()

            cursor.execute(
                """
                SELECT production_constraints,
                       constraint_checked_at,
                       is_production_blocked,
                       CAST((julianday('now') - julianday(constraint_checked_at)) AS INTEGER) AS data_age_days
                FROM keywords
                WHERE id = ?
                  AND constraint_checked_at IS NOT NULL
                """,
                (keyword_id,)
            )

            row = cursor.fetchone()

            if row is None:
                return None

            data_age_days = row['data_age_days'] or 0

            # Check if too old
            if data_age_days > max_age_days:
                return None

            # Parse constraints JSON
            constraints_json = row['production_constraints']
            if not constraints_json:
                return None

            try:
                constraints = json.loads(constraints_json)
            except (json.JSONDecodeError, TypeError):
                return None

            # Add runtime fields
            constraints['is_production_blocked'] = bool(row['is_production_blocked'])
            constraints['data_age_days'] = data_age_days

            return constraints

        except sqlite3.Error:
            return None

    # =========================================================================
    # LIFECYCLE STATE METHODS (Phase 18)
    # =========================================================================

    # Valid lifecycle states and allowed transitions
    LIFECYCLE_STATES = [
        'DISCOVERED',
        'ANALYZED',
        'RESEARCHING',
        'SCRIPTING',
        'FILMED',
        'PUBLISHED',
        'ARCHIVED'
    ]

    LIFECYCLE_TRANSITIONS = {
        'DISCOVERED': ['ANALYZED', 'ARCHIVED'],
        'ANALYZED': ['RESEARCHING', 'ARCHIVED'],
        'RESEARCHING': ['SCRIPTING', 'ARCHIVED'],
        'SCRIPTING': ['FILMED', 'ARCHIVED'],
        'FILMED': ['PUBLISHED', 'ARCHIVED'],
        'PUBLISHED': ['ARCHIVED'],
        'ARCHIVED': []
    }

    def _ensure_lifecycle_columns(self):
        """
        Safely add lifecycle state columns to keywords if they don't exist.

        This allows existing databases to migrate without manual schema updates.
        Executes ALTER TABLE statements for each missing column and creates
        lifecycle_history table.
        """
        try:
            cursor = self._conn.cursor()

            # Check which columns exist in keywords table
            cursor.execute("PRAGMA table_info(keywords)")
            existing_columns = {row[1] for row in cursor.fetchall()}

            # Add missing lifecycle columns
            columns_to_add = {
                'lifecycle_state': "ALTER TABLE keywords ADD COLUMN lifecycle_state TEXT DEFAULT 'DISCOVERED'",
                'lifecycle_updated_at': 'ALTER TABLE keywords ADD COLUMN lifecycle_updated_at DATE',
                'opportunity_score_final': 'ALTER TABLE keywords ADD COLUMN opportunity_score_final REAL',
                'opportunity_category': 'ALTER TABLE keywords ADD COLUMN opportunity_category TEXT'
            }

            for col_name, alter_sql in columns_to_add.items():
                if col_name not in existing_columns:
                    cursor.execute(alter_sql)

            # Create lifecycle_history table if it doesn't exist
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS lifecycle_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    keyword_id INTEGER NOT NULL,
                    from_state TEXT NOT NULL,
                    to_state TEXT NOT NULL,
                    transitioned_at DATE NOT NULL,
                    FOREIGN KEY (keyword_id) REFERENCES keywords(id)
                )
                """
            )

            # Create index if it doesn't exist
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_lifecycle_history ON lifecycle_history(keyword_id, transitioned_at DESC)"
            )

            self._conn.commit()

        except sqlite3.Error:
            # If table doesn't exist yet, this is fine (will be created during init)
            pass

    def set_lifecycle_state(self, keyword_id: int, new_state: str) -> Dict[str, Any]:
        """
        Transition keyword to new lifecycle state with validation.

        Valid states: DISCOVERED, ANALYZED, RESEARCHING, SCRIPTING, FILMED, PUBLISHED, ARCHIVED
        Validates transition rules before updating.

        Args:
            keyword_id: Keyword ID from keywords table
            new_state: Target lifecycle state

        Returns:
            {'status': 'transitioned', 'from': str, 'to': str, 'timestamp': str} on success
            {'error': msg, 'allowed': [str]} on invalid transition

        Example:
            result = db.set_lifecycle_state(5, 'ANALYZED')
            # After scoring is complete
        """
        try:
            # Validate new state
            if new_state not in self.LIFECYCLE_STATES:
                return {
                    'error': f'Invalid state: {new_state}',
                    'allowed': self.LIFECYCLE_STATES
                }

            cursor = self._conn.cursor()

            # Get current state
            cursor.execute(
                "SELECT lifecycle_state FROM keywords WHERE id = ?",
                (keyword_id,)
            )
            row = cursor.fetchone()

            if row is None:
                return {'error': 'Keyword not found', 'keyword_id': keyword_id}

            current_state = row[0] or 'DISCOVERED'

            # Validate transition
            allowed_transitions = self.LIFECYCLE_TRANSITIONS.get(current_state, [])
            if new_state not in allowed_transitions:
                return {
                    'error': f'Invalid transition from {current_state} to {new_state}',
                    'allowed': allowed_transitions,
                    'current_state': current_state
                }

            # Update state
            timestamp = datetime.utcnow().date().isoformat()
            cursor.execute(
                """
                UPDATE keywords
                SET lifecycle_state = ?,
                    lifecycle_updated_at = ?
                WHERE id = ?
                """,
                (new_state, timestamp, keyword_id)
            )

            # Log transition to history
            cursor.execute(
                """
                INSERT INTO lifecycle_history (keyword_id, from_state, to_state, transitioned_at)
                VALUES (?, ?, ?, ?)
                """,
                (keyword_id, current_state, new_state, timestamp)
            )

            self._conn.commit()

            return {
                'status': 'transitioned',
                'from': current_state,
                'to': new_state,
                'timestamp': timestamp
            }

        except sqlite3.Error as e:
            return {'error': 'Database operation failed', 'details': str(e)}

    def get_lifecycle_state(self, keyword_id: int) -> str:
        """
        Get current lifecycle state for a keyword.

        Args:
            keyword_id: Keyword ID from keywords table

        Returns:
            Current state string (default 'DISCOVERED' if not set)

        Example:
            state = db.get_lifecycle_state(5)
            if state == 'ANALYZED':
                print("Ready for research phase")
        """
        try:
            cursor = self._conn.cursor()

            cursor.execute(
                "SELECT lifecycle_state FROM keywords WHERE id = ?",
                (keyword_id,)
            )
            row = cursor.fetchone()

            if row is None or row[0] is None:
                return 'DISCOVERED'

            return row[0]

        except sqlite3.Error:
            return 'DISCOVERED'

    def get_keywords_by_lifecycle(self, state: str, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Get all keywords in a specific lifecycle state.

        Returns keywords sorted by opportunity_score_final DESC (highest scoring first).

        Args:
            state: Lifecycle state to filter by
            limit: Maximum number of keywords to return

        Returns:
            List of keyword dicts with opportunity scores

        Example:
            analyzed = db.get_keywords_by_lifecycle('ANALYZED', limit=10)
            for kw in analyzed:
                print(f"{kw['keyword']}: {kw['opportunity_score_final']}")
        """
        try:
            cursor = self._conn.cursor()

            cursor.execute(
                """
                SELECT *
                FROM keywords
                WHERE lifecycle_state = ?
                ORDER BY opportunity_score_final DESC NULLS LAST
                LIMIT ?
                """,
                (state, limit)
            )

            return [dict(row) for row in cursor.fetchall()]

        except sqlite3.Error:
            return []


    # =========================================================================
    # VIDEO PERFORMANCE METHODS (Phase 19)
    # =========================================================================

    def _ensure_performance_table(self):
        """
        Safely create video_performance table if it doesn't exist.

        This allows existing databases to migrate without manual schema updates.
        """
        try:
            cursor = self._conn.cursor()

            # Check if table exists
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='video_performance'"
            )
            if cursor.fetchone() is not None:
                return  # Table exists

            # Create table
            cursor.execute(
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

            # Create indexes
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_performance_conversion ON video_performance(conversion_rate DESC)"
            )
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_performance_topic ON video_performance(topic_type)"
            )
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_performance_fetched ON video_performance(fetched_at DESC)"
            )

            self._conn.commit()

        except sqlite3.Error:
            # If connection issue, this is fine (will be handled on init)
            pass

    def get_schema_version(self) -> int:
        """
        Get current schema version from SQLite user_version pragma.

        Returns:
            Schema version integer (0 if never set)

        Example:
            version = db.get_schema_version()
            if version < 27:
                print("Migration needed")
        """
        try:
            cursor = self._conn.cursor()
            cursor.execute("PRAGMA user_version")
            row = cursor.fetchone()
            return row[0] if row else 0
        except sqlite3.Error:
            return 0

    def set_schema_version(self, version: int):
        """
        Set schema version in SQLite user_version pragma.

        Args:
            version: Schema version to set

        Example:
            db.set_schema_version(27)
        """
        try:
            cursor = self._conn.cursor()
            cursor.execute(f"PRAGMA user_version = {version}")
            self._conn.commit()
        except sqlite3.Error:
            pass

    def _backup_database(self) -> Optional[str]:
        """
        Create timestamped backup of database before migration.

        Backup location: tools/discovery/backups/
        Backup format: keywords_pre_v27_{YYYYMMDD_HHMMSS}.db

        Returns:
            Backup file path on success, None on failure

        Example:
            backup_path = db._backup_database()
            if backup_path:
                print(f"Backed up to: {backup_path}")
        """
        try:
            import shutil
            from pathlib import Path

            # Create backup directory
            backup_dir = Path(__file__).parent / 'backups'
            backup_dir.mkdir(exist_ok=True)

            # Generate timestamped filename
            timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
            backup_filename = f'keywords_pre_v27_{timestamp}.db'
            backup_path = backup_dir / backup_filename

            # Close connection, copy, reopen
            self._conn.close()
            self._conn = None

            shutil.copy2(self.db_path, backup_path)

            # Reopen connection
            self._ensure_connection()

            print(f"[Phase 27] Database backed up to: {backup_path}")
            return str(backup_path)

        except Exception:
            # Reopen connection if it was closed
            if self._conn is None:
                self._ensure_connection()
            return None

    def _ensure_variant_tables(self):
        """
        Create Phase 27 variant tracking tables if they don't exist.

        Creates:
        - thumbnail_variants: stores thumbnail file paths and visual pattern tags
        - title_variants: stores title text and formula tags

        Includes backup and schema version tracking.
        """
        try:
            # Check if already migrated
            if self.get_schema_version() >= 27:
                return

            print("[Phase 27] Migrating database: adding variant tracking tables...")

            # Backup before migration (without reopening connection)
            import shutil
            from pathlib import Path

            backup_dir = Path(__file__).parent / 'backups'
            backup_dir.mkdir(exist_ok=True)
            timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
            backup_filename = f'keywords_pre_v27_{timestamp}.db'
            backup_path = backup_dir / backup_filename

            # Close connection temporarily for backup
            self._conn.close()
            shutil.copy2(self.db_path, backup_path)
            # Reopen connection WITHOUT triggering _ensure_connection recursion
            self._conn = sqlite3.connect(self.db_path)
            self._conn.row_factory = sqlite3.Row

            print(f"[Phase 27] Database backed up to: {backup_path}")

            cursor = self._conn.cursor()

            # Create thumbnail_variants table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS thumbnail_variants (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    video_id TEXT NOT NULL,
                    variant_letter TEXT NOT NULL,
                    file_path TEXT NOT NULL,
                    perceptual_hash TEXT,
                    visual_pattern_tags TEXT,
                    created_at DATE NOT NULL,
                    FOREIGN KEY (video_id) REFERENCES video_performance(video_id)
                )
                """
            )

            # Create indexes for thumbnail_variants
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_thumbnail_video ON thumbnail_variants(video_id)"
            )
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_thumbnail_hash ON thumbnail_variants(perceptual_hash)"
            )

            # Create title_variants table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS title_variants (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    video_id TEXT NOT NULL,
                    variant_letter TEXT NOT NULL,
                    title_text TEXT NOT NULL,
                    character_count INTEGER NOT NULL,
                    formula_tags TEXT,
                    created_at DATE NOT NULL,
                    FOREIGN KEY (video_id) REFERENCES video_performance(video_id)
                )
                """
            )

            # Create index for title_variants
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_title_video ON title_variants(video_id)"
            )

            self._conn.commit()

            print("[Phase 27] Variant tables created (thumbnail_variants, title_variants)")

            # Set schema version to 27
            self.set_schema_version(27)

        except sqlite3.Error:
            pass

    def _ensure_ctr_snapshots_table(self):
        """
        Create Phase 27 CTR snapshot tracking table if it doesn't exist.

        Creates:
        - ctr_snapshots: stores monthly CTR snapshots with active variant references
        """
        try:
            cursor = self._conn.cursor()

            # Check if table already exists
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='ctr_snapshots'"
            )
            if cursor.fetchone() is not None:
                return

            # Create ctr_snapshots table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS ctr_snapshots (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    video_id TEXT NOT NULL,
                    snapshot_date DATE NOT NULL,
                    ctr_percent REAL NOT NULL,
                    impression_count INTEGER NOT NULL,
                    view_count INTEGER NOT NULL,
                    active_thumbnail_id INTEGER,
                    active_title_id INTEGER,
                    is_late_entry BOOLEAN DEFAULT 0,
                    recorded_at DATE NOT NULL,
                    FOREIGN KEY (video_id) REFERENCES video_performance(video_id),
                    FOREIGN KEY (active_thumbnail_id) REFERENCES thumbnail_variants(id),
                    FOREIGN KEY (active_title_id) REFERENCES title_variants(id)
                )
                """
            )

            # Create index
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_ctr_video_date ON ctr_snapshots(video_id, snapshot_date DESC)"
            )

            self._conn.commit()

        except sqlite3.Error:
            pass

    def _ensure_feedback_tables(self):
        """
        Create Phase 27 feedback storage tables and columns if they don't exist.

        Creates:
        - Feedback columns on video_performance (retention_drop_point, discovery_issues, lessons_learned)
        - section_feedback table: stores section-level retention notes
        """
        try:
            cursor = self._conn.cursor()

            # Check which columns exist in video_performance
            cursor.execute("PRAGMA table_info(video_performance)")
            existing_columns = {row[1] for row in cursor.fetchall()}

            # Add missing feedback columns
            columns_to_add = {
                'retention_drop_point': 'ALTER TABLE video_performance ADD COLUMN retention_drop_point INTEGER',
                'discovery_issues': 'ALTER TABLE video_performance ADD COLUMN discovery_issues TEXT',
                'lessons_learned': 'ALTER TABLE video_performance ADD COLUMN lessons_learned TEXT'
            }

            for col_name, alter_sql in columns_to_add.items():
                if col_name not in existing_columns:
                    cursor.execute(alter_sql)

            # Create section_feedback table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS section_feedback (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    video_id TEXT NOT NULL,
                    section_name TEXT NOT NULL,
                    retention_percent REAL,
                    notes TEXT,
                    created_at DATE,
                    FOREIGN KEY (video_id) REFERENCES video_performance(video_id)
                )
                """
            )

            # Create index
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_section_feedback_video ON section_feedback(video_id)"
            )

            self._conn.commit()

        except sqlite3.Error:
            pass

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
            import json

            # Ensure table exists
            self._ensure_performance_table()

            cursor = self._conn.cursor()
            now = datetime.utcnow().date().isoformat()

            # Convert angles list to JSON
            angles_json = json.dumps(angles) if angles else None

            # Check if video exists
            cursor.execute(
                "SELECT id FROM video_performance WHERE video_id = ?",
                (video_id,)
            )
            existing = cursor.fetchone()

            if existing:
                # Update existing record
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
                # Insert new record
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
            return {'error': 'Database operation failed', 'details': str(e)}

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
            import json

            # Ensure table exists
            self._ensure_performance_table()

            cursor = self._conn.cursor()

            cursor.execute(
                "SELECT * FROM video_performance WHERE video_id = ?",
                (video_id,)
            )

            row = cursor.fetchone()

            if row is None:
                return {'error': 'not found', 'video_id': video_id}

            result = dict(row)

            # Parse angles JSON back to list
            if result.get('angles'):
                try:
                    result['angles'] = json.loads(result['angles'])
                except (json.JSONDecodeError, TypeError):
                    result['angles'] = []

            return result

        except sqlite3.Error as e:
            return {'error': 'Database operation failed', 'details': str(e)}

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
            import json

            # Ensure table exists
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

                # Parse angles JSON
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
            import json

            # Ensure table exists
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
            import json

            # Ensure table exists
            self._ensure_performance_table()

            cursor = self._conn.cursor()

            # SQLite JSON search using LIKE on the JSON string
            # This works because angles are stored as ["angle1", "angle2"]
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
            import json

            # Ensure table exists
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
            import json
            from datetime import datetime

            # Validate variant_letter
            if not variant_letter or len(variant_letter) != 1 or not variant_letter.isupper():
                return {'error': 'variant_letter must be a single uppercase letter (A-Z)'}

            if variant_letter < 'A' or variant_letter > 'Z':
                return {'error': 'variant_letter must be between A and Z'}

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
                    datetime.utcnow().date().isoformat()
                )
            )

            self._conn.commit()
            return {'status': 'inserted', 'variant_id': cursor.lastrowid}

        except sqlite3.Error as e:
            return {'error': f'Database error: {str(e)}'}

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
            import json
            from datetime import datetime

            # Validate variant_letter
            if not variant_letter or len(variant_letter) != 1 or not variant_letter.isupper():
                return {'error': 'variant_letter must be a single uppercase letter (A-Z)'}

            if variant_letter < 'A' or variant_letter > 'Z':
                return {'error': 'variant_letter must be between A and Z'}

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
                    datetime.utcnow().date().isoformat()
                )
            )

            self._conn.commit()
            return {'status': 'inserted', 'variant_id': cursor.lastrowid}

        except sqlite3.Error as e:
            return {'error': f'Database error: {str(e)}'}

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
            from datetime import datetime

            # Validate ctr_percent
            if ctr_percent < 0 or ctr_percent > 100:
                return {'error': 'ctr_percent must be between 0 and 100'}

            # Validate counts
            if impression_count < 0 or view_count < 0:
                return {'error': 'impression_count and view_count must be non-negative'}

            # Set dates
            if snapshot_date is None:
                snapshot_date = datetime.utcnow().date().isoformat()

            recorded_at = datetime.utcnow().date().isoformat()

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
            return {'error': f'Database error: {str(e)}'}

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
            import json

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

                # Parse visual_pattern_tags from JSON
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
            import json

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

                # Parse formula_tags from JSON
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

            # Count thumbnails
            cursor.execute(
                "SELECT COUNT(*) as count FROM thumbnail_variants WHERE video_id = ?",
                (video_id,)
            )
            thumb_count = cursor.fetchone()['count']

            # Count titles
            cursor.execute(
                "SELECT COUNT(*) as count FROM title_variants WHERE video_id = ?",
                (video_id,)
            )
            title_count = cursor.fetchone()['count']

            # Count snapshots
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
                return {'error': 'not found'}

        except sqlite3.Error as e:
            return {'error': f'Database error: {str(e)}'}

    # =========================================================================
    # PHASE 30: CTR ANALYSIS METHODS
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

            cursor = self._conn.cursor()

            # Get latest snapshot per video with topic_type
            cursor.execute(
                """
                SELECT
                    s.video_id,
                    s.ctr_percent,
                    s.snapshot_date,
                    COALESCE(vp.topic_type, 'general') as topic_type
                FROM ctr_snapshots s
                LEFT JOIN video_performance vp ON s.video_id = vp.video_id
                WHERE s.snapshot_date = (
                    SELECT MAX(snapshot_date) FROM ctr_snapshots
                    WHERE video_id = s.video_id
                )
                """
            )

            rows = cursor.fetchall()

            if not rows:
                return {
                    'overall': {
                        'avg_ctr': 0,
                        'video_count': 0,
                        'date_range': {'earliest': None, 'latest': None}
                    },
                    'by_category': {}
                }

            # Aggregate data
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

            # Calculate overall stats
            overall_avg = stats.mean(all_ctrs) if all_ctrs else 0
            dates_sorted = sorted([d for d in all_dates if d])

            # Calculate per-category stats
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

        except Exception:
            return {
                'overall': {
                    'avg_ctr': 0,
                    'video_count': 0,
                    'date_range': {'earliest': None, 'latest': None}
                },
                'by_category': {}
            }

    # =========================================================================
    # PHASE 31: FEEDBACK LOOP METHODS
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

            # Prepare JSON fields
            discovery = feedback_data.get('discovery', {})
            discovery_json = json.dumps(discovery) if discovery else None

            lessons = {
                'observations': feedback_data.get('observations', []),
                'actionable': feedback_data.get('actionable', [])
            }
            lessons_json = json.dumps(lessons)

            # Update video_performance row
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
            return {'error': f'Database error: {str(e)}'}

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
                return {'error': 'not_found'}

            # Parse JSON columns with null-safety
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
            return {'error': f'Database error: {str(e)}'}
        except json.JSONDecodeError as e:
            return {'error': f'JSON parse error: {str(e)}'}

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
                # Parse lessons_learned JSON with null-safety
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
            return {'error': f'Database error: {str(e)}'}
        except json.JSONDecodeError as e:
            return {'error': f'JSON parse error: {str(e)}'}

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
