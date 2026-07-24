"""
Schema Manager

Formerly the monolithic database.py (Phase H5 refactor). Owns:
- Database connection setup and schema initialization
- Schema migration helpers (_ensure_* methods)
- AmbiguousReview methods: trend tracking, schema versioning
- __getattr__ delegation to KeywordStore / IntentClassifier / PerformanceTracker

All business logic now lives in the three focused stores. This module is the
backward-compat entry point for callers that still use KeywordDB directly.

Usage (legacy):
    from tools.discovery.schema_manager import KeywordDB

    db = KeywordDB()
    db.add_keyword('dark ages myth', source='autocomplete')  # delegated to KeywordStore
    db.close()

Prefer new callers to import from the focused stores directly.
"""

import sqlite3
import json
import shutil
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional, Dict, List, Any

from tools.logging_config import get_logger
from tools.discovery.keyword_store import KeywordStore
from tools.discovery.intent_classifier import IntentClassifier
from tools.discovery.performance_tracker import PerformanceTracker

logger = get_logger(__name__)


class KeywordDB:
    """
    Backward-compat facade over KeywordStore + IntentClassifier + PerformanceTracker.

    Public methods delegate to the appropriate store via __getattr__.
    AmbiguousReview methods (trends, schema versioning) remain inline.
    """

    def __init__(self, db_path: Optional[str] = None):
        if db_path is None:
            module_dir = Path(__file__).parent
            db_path = str(module_dir / 'keywords.db')

        self.db_path = db_path
        self._conn = None
        self._ensure_connection()
        self._keyword_store = KeywordStore(self._conn)
        self._intent_classifier = IntentClassifier.__new__(IntentClassifier)
        self._intent_classifier._conn = self._conn
        self._performance_tracker = PerformanceTracker(self._conn)

    def __getattr__(self, name: str):
        if name.startswith('_'):
            raise AttributeError(name)
        for store in (self._keyword_store, self._intent_classifier, self._performance_tracker):
            if hasattr(store, name):
                return getattr(store, name)
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

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

    def _ensure_connection(self):
        """Ensure database connection exists and initialize schema if needed."""
        if self._conn is None:
            self._conn = sqlite3.connect(self.db_path)
            self._conn.row_factory = sqlite3.Row

            cursor = self._conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='keywords'")

            if cursor.fetchone() is None:
                self.init_database()
            else:
                self._ensure_classification_columns()
                self._ensure_production_columns()
                self._ensure_lifecycle_columns()
                self._ensure_performance_table()
                self._ensure_variant_tables()
                self._ensure_ctr_snapshots_table()
                self._ensure_feedback_tables()

    def init_database(self) -> Dict[str, Any]:
        """Initialize database from schema.sql."""
        try:
            schema_path = Path(__file__).parent / 'schema.sql'

            if not schema_path.exists():
                return self._err('init_database', 'schema.sql not found', path=str(schema_path))

            schema_sql = schema_path.read_text(encoding='utf-8')

            cursor = self._conn.cursor()
            cursor.executescript(schema_sql)
            self._conn.commit()

            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
            tables = [row[0] for row in cursor.fetchall()]

            return {
                'status': 'initialized',
                'tables': tables,
                'database': self.db_path
            }

        except sqlite3.Error as e:
            return self._err('init_database', f'Database initialization failed: {type(e).__name__}', e)
        except Exception as e:
            return self._err('init_database', f'Unexpected error during initialization: {type(e).__name__}', e)

    def close(self):
        """Close database connection."""
        if self._conn:
            self._conn.close()
            self._conn = None

    # =========================================================================
    # SCHEMA VERSIONING
    # =========================================================================

    def get_schema_version(self) -> int:
        """Get current schema version from SQLite user_version pragma."""
        try:
            cursor = self._conn.cursor()
            cursor.execute("PRAGMA user_version")
            row = cursor.fetchone()
            return row[0] if row else 0
        except sqlite3.Error:
            return 0

    def set_schema_version(self, version: int):
        """Set schema version in SQLite user_version pragma."""
        try:
            cursor = self._conn.cursor()
            cursor.execute(f"PRAGMA user_version = {version}")
            self._conn.commit()
        except sqlite3.Error as e:
            logger.error("Failed to set schema version %d: %s", version, e)

    def _backup_database(self) -> Optional[str]:
        """Create timestamped backup of database before migration."""
        try:
            backup_dir = Path(__file__).parent / 'backups'
            backup_dir.mkdir(exist_ok=True)

            timestamp = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')
            backup_filename = f'keywords_pre_v27_{timestamp}.db'
            backup_path = backup_dir / backup_filename

            self._conn.close()
            self._conn = None

            shutil.copy2(self.db_path, backup_path)

            self._ensure_connection()

            logger.info("[Phase 27] Database backed up to: %s", backup_path)
            return str(backup_path)

        except (OSError, sqlite3.Error):
            if self._conn is None:
                self._ensure_connection()
            return None

    # =========================================================================
    # DEMAND RESEARCH METHODS (AmbiguousReview — Phase 15)
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
            now = datetime.now(timezone.utc).isoformat()

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
            return self._err('add_trend', 'Integrity constraint violated', e)
        except sqlite3.OperationalError as e:
            return self._err('add_trend', 'Database operation failed', e)

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
                return self._err('get_latest_trend', 'not found')

            return dict(row)

        except sqlite3.Error as e:
            return self._err('get_latest_trend', 'Database operation failed', e)

    # =========================================================================
    # SCHEMA MIGRATION HELPERS
    # =========================================================================

    def _ensure_classification_columns(self):
        """Safely add classification columns to competitor_videos if they don't exist."""
        if not self._table_exists('competitor_videos'):
            return

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

    def _ensure_production_columns(self):
        """Safely add production constraint columns to keywords if they don't exist."""
        if not self._table_exists('keywords'):
            return

        cursor = self._conn.cursor()
        cursor.execute("PRAGMA table_info(keywords)")
        existing_columns = {row[1] for row in cursor.fetchall()}

        columns_to_add = {
            'production_constraints': 'ALTER TABLE keywords ADD COLUMN production_constraints TEXT',
            'constraint_checked_at': 'ALTER TABLE keywords ADD COLUMN constraint_checked_at DATE',
            'is_production_blocked': 'ALTER TABLE keywords ADD COLUMN is_production_blocked BOOLEAN DEFAULT 0'
        }

        with self._conn:
            for col_name, alter_sql in columns_to_add.items():
                if col_name not in existing_columns:
                    self._conn.execute(alter_sql)
            self._conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_keywords_blocked ON keywords(is_production_blocked, constraint_checked_at DESC)"
            )

    def _ensure_lifecycle_columns(self):
        """Safely add lifecycle state columns to keywords if they don't exist."""
        if not self._table_exists('keywords'):
            return

        cursor = self._conn.cursor()
        cursor.execute("PRAGMA table_info(keywords)")
        existing_columns = {row[1] for row in cursor.fetchall()}

        columns_to_add = {
            'lifecycle_state': "ALTER TABLE keywords ADD COLUMN lifecycle_state TEXT DEFAULT 'DISCOVERED'",
            'lifecycle_updated_at': 'ALTER TABLE keywords ADD COLUMN lifecycle_updated_at DATE',
            'opportunity_score_final': 'ALTER TABLE keywords ADD COLUMN opportunity_score_final REAL',
            'opportunity_category': 'ALTER TABLE keywords ADD COLUMN opportunity_category TEXT'
        }

        with self._conn:
            for col_name, alter_sql in columns_to_add.items():
                if col_name not in existing_columns:
                    self._conn.execute(alter_sql)

            self._conn.execute(
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

            self._conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_lifecycle_history ON lifecycle_history(keyword_id, transitioned_at DESC)"
            )

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

    def _ensure_variant_tables(self):
        """Create Phase 27 variant tracking tables if they don't exist."""
        try:
            if self.get_schema_version() >= 27:
                return

            logger.info("[Phase 27] Migrating database: adding variant tracking tables...")

            backup_dir = Path(__file__).parent / 'backups'
            backup_dir.mkdir(exist_ok=True)
            timestamp = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')
            backup_filename = f'keywords_pre_v27_{timestamp}.db'
            backup_path = backup_dir / backup_filename

            self._conn.close()
            shutil.copy2(self.db_path, backup_path)
            self._conn = sqlite3.connect(self.db_path)
            self._conn.row_factory = sqlite3.Row

            logger.info("[Phase 27] Database backed up to: %s", backup_path)

            with self._conn:
                cursor = self._conn.cursor()

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
                cursor.execute(
                    "CREATE INDEX IF NOT EXISTS idx_thumbnail_video ON thumbnail_variants(video_id)"
                )
                cursor.execute(
                    "CREATE INDEX IF NOT EXISTS idx_thumbnail_hash ON thumbnail_variants(perceptual_hash)"
                )
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
                cursor.execute(
                    "CREATE INDEX IF NOT EXISTS idx_title_video ON title_variants(video_id)"
                )

            logger.info("[Phase 27] Variant tables created (thumbnail_variants, title_variants)")
            self.set_schema_version(27)

        except sqlite3.Error as e:
            logger.error("Migration to v27 failed: %s", e)

    def _ensure_ctr_snapshots_table(self):
        """Create Phase 27 CTR snapshot table + ensure the validity columns.

        is_valid/invalid_reason (added 2026-07-22) let a polluted snapshot be
        quarantined without deletion — the 2026-07-13/07-23 rows were double-
        counted by the collector and must be readable-but-excluded, not lost.
        """
        try:
            with self._conn:
                cursor = self._conn.cursor()
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
                        is_valid INTEGER NOT NULL DEFAULT 1,
                        invalid_reason TEXT,
                        FOREIGN KEY (video_id) REFERENCES video_performance(video_id),
                        FOREIGN KEY (active_thumbnail_id) REFERENCES thumbnail_variants(id),
                        FOREIGN KEY (active_title_id) REFERENCES title_variants(id)
                    )
                    """
                )
                cursor.execute(
                    "CREATE INDEX IF NOT EXISTS idx_ctr_video_date ON ctr_snapshots(video_id, snapshot_date DESC)"
                )
                # Idempotent column migration for DBs created before 2026-07-22.
                existing = {r[1] for r in cursor.execute("PRAGMA table_info(ctr_snapshots)")}
                if "is_valid" not in existing:
                    cursor.execute(
                        "ALTER TABLE ctr_snapshots ADD COLUMN is_valid INTEGER NOT NULL DEFAULT 1"
                    )
                if "invalid_reason" not in existing:
                    cursor.execute(
                        "ALTER TABLE ctr_snapshots ADD COLUMN invalid_reason TEXT"
                    )

        except sqlite3.Error as e:
            logger.error("Migration ctr_snapshots failed: %s", e)

    def _ensure_feedback_tables(self):
        """Create Phase 27 feedback storage tables and columns if they don't exist."""
        if not self._table_exists('video_performance'):
            return

        cursor = self._conn.cursor()
        cursor.execute("PRAGMA table_info(video_performance)")
        existing_columns = {row[1] for row in cursor.fetchall()}

        columns_to_add = {
            'retention_drop_point': 'ALTER TABLE video_performance ADD COLUMN retention_drop_point INTEGER',
            'discovery_issues': 'ALTER TABLE video_performance ADD COLUMN discovery_issues TEXT',
            'lessons_learned': 'ALTER TABLE video_performance ADD COLUMN lessons_learned TEXT'
        }

        with self._conn:
            cursor = self._conn.cursor()

            for col_name, alter_sql in columns_to_add.items():
                if col_name not in existing_columns:
                    cursor.execute(alter_sql)

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
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_section_feedback_video ON section_feedback(video_id)"
            )


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
