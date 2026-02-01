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
            else:
                # Ensure classification columns exist (Phase 16 migration)
                self._ensure_classification_columns()
                # Ensure production constraint columns exist (Phase 17 migration)
                self._ensure_production_columns()

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
        source_examples: Optional[List[str]] = None
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

        Returns:
            {'status': 'stored', 'keyword_id': keyword_id} on success
            {'error': msg} on failure

        Example:
            db.store_production_constraints(
                keyword_id=5,
                animation_required=False,
                document_score=3,
                sources_found=5,
                source_examples=['Cambridge Press Book', 'JSTOR Article']
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
