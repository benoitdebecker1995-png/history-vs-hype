"""KeywordStore — single-responsibility store for keyword discovery data.

Extracted from tools/discovery/database.py (Phase H3 refactor).
Owns: keywords, keyword_intents, keyword_performance, opportunity_scores,
      lifecycle_history tables.

Constructor accepts a sqlite3.Connection for testability (DI pattern).
See .planning/refactor-notes/database-partition.md for full design.
"""
import json
import sqlite3
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from tools.logging_config import get_logger

logger = get_logger(__name__)


class KeywordStore:
    """CRUD and lifecycle operations for keyword discovery data.

    Takes an open sqlite3.Connection — caller is responsible for connection
    lifecycle (open, close, row_factory).
    """

    LIFECYCLE_STATES = [
        'DISCOVERED',
        'ANALYZED',
        'RESEARCHING',
        'SCRIPTING',
        'FILMED',
        'PUBLISHED',
        'ARCHIVED',
    ]

    LIFECYCLE_TRANSITIONS = {
        'DISCOVERED': ['ANALYZED', 'ARCHIVED'],
        'ANALYZED': ['RESEARCHING', 'ARCHIVED'],
        'RESEARCHING': ['SCRIPTING', 'ARCHIVED'],
        'SCRIPTING': ['FILMED', 'ARCHIVED'],
        'FILMED': ['PUBLISHED', 'ARCHIVED'],
        'PUBLISHED': ['ARCHIVED'],
        'ARCHIVED': [],
    }

    def __init__(self, conn: sqlite3.Connection) -> None:
        self._conn = conn

    @classmethod
    def connect(cls, db_path: Optional[str] = None) -> 'KeywordStore':
        """Open a database connection and return a ready KeywordStore.

        Uses KeywordDB internally to run schema init + migrations, then hands
        off the connection. Local import avoids circular dependency.
        """
        from tools.discovery.database import KeywordDB  # deferred — avoids circular import
        kdb = KeywordDB(db_path)
        return cls(kdb._conn)

    def close(self) -> None:
        """Close the underlying database connection."""
        if self._conn:
            self._conn.close()
            self._conn = None

    # ── helpers ───────────────────────────────────────────────────────────────

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

    # ── keyword CRUD ──────────────────────────────────────────────────────────

    def add_keyword(
        self,
        keyword: str,
        source: str = 'manual',
        search_volume: Optional[int] = None,
        competition: Optional[float] = None,
    ) -> Dict[str, Any]:
        try:
            cursor = self._conn.cursor()
            now = datetime.now(timezone.utc).date().isoformat()

            cursor.execute("SELECT id, first_discovered FROM keywords WHERE keyword = ?", (keyword,))
            existing = cursor.fetchone()

            if existing:
                keyword_id = existing['id']
                cursor.execute(
                    """
                    UPDATE keywords
                    SET search_volume = COALESCE(?, search_volume),
                        competition_score = COALESCE(?, competition_score),
                        last_updated = ?,
                        source = ?
                    WHERE id = ?
                    """,
                    (search_volume, competition, now, source, keyword_id),
                )
                action = 'updated'
            else:
                cursor.execute(
                    """
                    INSERT INTO keywords (keyword, search_volume, competition_score, first_discovered, last_updated, source)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (keyword, search_volume, competition, now, now, source),
                )
                keyword_id = cursor.lastrowid
                action = 'inserted'

            self._conn.commit()
            return {'keyword_id': keyword_id, 'keyword': keyword, 'action': action}

        except sqlite3.Error as e:
            return self._err('add_keyword', f'Database error adding keyword: {type(e).__name__}', e)
        except Exception as e:
            return self._err('add_keyword', f'Unexpected error: {type(e).__name__}', e)

    def get_keyword(self, keyword: str) -> Dict[str, Any]:
        try:
            cursor = self._conn.cursor()
            cursor.execute("SELECT * FROM keywords WHERE keyword = ?", (keyword,))
            row = cursor.fetchone()
            if row is None:
                return self._err('get_keyword', 'Keyword not found', keyword=keyword)
            return dict(row)
        except sqlite3.Error as e:
            return self._err('get_keyword', f'Database error: {type(e).__name__}', e)

    def search_keywords(self, pattern: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
        try:
            cursor = self._conn.cursor()
            if pattern is None:
                cursor.execute("SELECT * FROM keywords ORDER BY last_updated DESC LIMIT ?", (limit,))
            else:
                cursor.execute(
                    "SELECT * FROM keywords WHERE keyword LIKE ? ORDER BY last_updated DESC LIMIT ?",
                    (pattern, limit),
                )
            return [dict(row) for row in cursor.fetchall()]
        except sqlite3.Error:
            return []

    def get_keywords_by_source(self, source: str, limit: int = 50) -> List[Dict[str, Any]]:
        try:
            cursor = self._conn.cursor()
            cursor.execute(
                "SELECT * FROM keywords WHERE source = ? ORDER BY last_updated DESC LIMIT ?",
                (source, limit),
            )
            return [dict(row) for row in cursor.fetchall()]
        except sqlite3.Error:
            return []

    def get_keywords_by_intent(self, intent_category: str, limit: int = 50) -> List[Dict[str, Any]]:
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
                (intent_category, limit),
            )
            return [dict(row) for row in cursor.fetchall()]
        except sqlite3.Error:
            return []

    # ── intent ────────────────────────────────────────────────────────────────

    def set_intent(
        self,
        keyword_id: int,
        category: str,
        confidence: float,
        is_primary: bool = False,
    ) -> Dict[str, Any]:
        try:
            cursor = self._conn.cursor()
            if is_primary:
                cursor.execute(
                    "UPDATE keyword_intents SET is_primary = 0 WHERE keyword_id = ?",
                    (keyword_id,),
                )
            cursor.execute(
                """
                INSERT INTO keyword_intents (keyword_id, intent_category, confidence, is_primary)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(keyword_id, intent_category) DO UPDATE SET
                    confidence = excluded.confidence,
                    is_primary = excluded.is_primary
                """,
                (keyword_id, category, confidence, is_primary),
            )
            self._conn.commit()
            return {
                'status': 'set',
                'keyword_id': keyword_id,
                'intent': category,
                'confidence': confidence,
                'is_primary': is_primary,
            }
        except sqlite3.Error as e:
            return self._err('set_intent', f'Database error setting intent: {type(e).__name__}', e)

    # ── performance tracking ──────────────────────────────────────────────────

    def add_performance(
        self,
        keyword_id: int,
        video_id: str,
        impressions: Optional[int] = None,
        ctr: Optional[float] = None,
        views: Optional[int] = None,
        watch_time_minutes: Optional[int] = None,
    ) -> Dict[str, Any]:
        try:
            cursor = self._conn.cursor()
            now = datetime.now(timezone.utc).date().isoformat()
            cursor.execute(
                """
                INSERT INTO keyword_performance (keyword_id, video_id, impressions, ctr, views, watch_time_minutes, measured_date)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (keyword_id, video_id, impressions, ctr, views, watch_time_minutes, now),
            )
            self._conn.commit()
            return {'status': 'tracked', 'performance_id': cursor.lastrowid}
        except sqlite3.Error as e:
            return self._err('add_performance', f'Database error tracking performance: {type(e).__name__}', e)

    def get_keyword_stats(self) -> Dict[str, Any]:
        try:
            cursor = self._conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM keywords")
            total_keywords = cursor.fetchone()[0]
            cursor.execute("SELECT source, COUNT(*) FROM keywords GROUP BY source")
            by_source = {row[0]: row[1] for row in cursor.fetchall()}
            cursor.execute("SELECT COUNT(DISTINCT keyword_id) FROM keyword_intents")
            with_intent = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(DISTINCT keyword_id) FROM keyword_performance")
            with_performance = cursor.fetchone()[0]
            return {
                'total_keywords': total_keywords,
                'by_source': by_source,
                'with_intent': with_intent,
                'with_performance': with_performance,
            }
        except sqlite3.Error:
            return {}

    # ── opportunity scores ────────────────────────────────────────────────────

    def add_opportunity_score(
        self,
        keyword_id: int,
        demand_score: float,
        competition_score: float,
        opportunity_ratio: float,
        category: str,
    ) -> Dict[str, Any]:
        try:
            cursor = self._conn.cursor()
            now = datetime.now(timezone.utc).date().isoformat()
            cursor.execute(
                """
                INSERT INTO opportunity_scores (keyword_id, demand_score, competition_score, opportunity_ratio, opportunity_category, calculated_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (keyword_id, demand_score, competition_score, opportunity_ratio, category, now),
            )
            self._conn.commit()
            return {'status': 'inserted'}
        except sqlite3.IntegrityError as e:
            return self._err('add_opportunity_score', 'Integrity constraint violated', e)
        except sqlite3.OperationalError as e:
            return self._err('add_opportunity_score', 'Database operation failed', e)

    def get_opportunity_score(self, keyword_id: int, max_age_days: int = 7) -> Optional[Dict[str, Any]]:
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
                (keyword_id,),
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

    def save_opportunity_score(
        self,
        keyword_id: int,
        opportunity_score: float,
        category: str,
        components: Optional[Dict[str, Any]] = None,
        is_blocked: bool = False,
    ) -> Dict[str, Any]:
        try:
            cursor = self._conn.cursor()
            now = datetime.now(timezone.utc).date().isoformat()
            cursor.execute(
                """
                UPDATE keywords
                SET opportunity_score_final = ?,
                    opportunity_category = ?
                WHERE id = ?
                """,
                (opportunity_score, category, keyword_id),
            )
            if not is_blocked and components:
                demand_score = components.get('demand', {}).get('normalized', 0)
                gap_score = components.get('gap', {}).get('normalized', 0)
                opportunity_ratio = (opportunity_score or 0) / 100.0
                cursor.execute(
                    """
                    INSERT INTO opportunity_scores
                        (keyword_id, demand_score, competition_score,
                         opportunity_ratio, opportunity_category, calculated_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (keyword_id, demand_score, gap_score, opportunity_ratio, category, now),
                )
            self._conn.commit()
            current_state = self.get_lifecycle_state(keyword_id)
            if current_state == 'DISCOVERED':
                self.set_lifecycle_state(keyword_id, 'ANALYZED')
            return {'status': 'saved', 'keyword_id': keyword_id}
        except sqlite3.Error as e:
            return self._err('save_opportunity_score', 'Failed to save opportunity score', e)

    # ── production constraints ────────────────────────────────────────────────

    def store_production_constraints(
        self,
        keyword_id: int,
        animation_required: bool,
        document_score: int,
        sources_found: int = 0,
        source_examples: Optional[List[str]] = None,
        source_hints: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        try:
            cursor = self._conn.cursor()
            now = datetime.now(timezone.utc).date().isoformat()
            constraints = {
                'animation_required': animation_required,
                'document_score': document_score,
                'sources_found': sources_found,
                'source_examples': source_examples or [],
                'source_hints': source_hints or {},
                'checked_at': now,
            }
            constraints_json = json.dumps(constraints)
            is_blocked = 1 if animation_required else 0
            cursor.execute(
                """
                UPDATE keywords
                SET production_constraints = ?,
                    constraint_checked_at = ?,
                    is_production_blocked = ?
                WHERE id = ?
                """,
                (constraints_json, now, is_blocked, keyword_id),
            )
            self._conn.commit()
            if cursor.rowcount == 0:
                return self._err('store_production_constraints', 'Keyword not found', keyword_id=keyword_id)
            return {'status': 'stored', 'keyword_id': keyword_id}
        except sqlite3.Error as e:
            return self._err('store_production_constraints', 'Database operation failed', e)

    def get_production_constraints(
        self,
        keyword_id: int,
        max_age_days: int = 90,
    ) -> Optional[Dict[str, Any]]:
        try:
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
                (keyword_id,),
            )
            row = cursor.fetchone()
            if row is None:
                return None
            data_age_days = row['data_age_days'] or 0
            if data_age_days > max_age_days:
                return None
            constraints_json = row['production_constraints']
            if not constraints_json:
                return None
            try:
                constraints = json.loads(constraints_json)
            except (json.JSONDecodeError, TypeError):
                return None
            constraints['is_production_blocked'] = bool(row['is_production_blocked'])
            constraints['data_age_days'] = data_age_days
            return constraints
        except sqlite3.Error:
            return None

    # ── lifecycle state ───────────────────────────────────────────────────────

    def set_lifecycle_state(self, keyword_id: int, new_state: str) -> Dict[str, Any]:
        try:
            if new_state not in self.LIFECYCLE_STATES:
                return self._err('set_lifecycle_state', f'Invalid state: {new_state}', allowed=self.LIFECYCLE_STATES)
            cursor = self._conn.cursor()
            cursor.execute("SELECT lifecycle_state FROM keywords WHERE id = ?", (keyword_id,))
            row = cursor.fetchone()
            if row is None:
                return self._err('set_lifecycle_state', 'Keyword not found', keyword_id=keyword_id)
            current_state = row[0] or 'DISCOVERED'
            allowed_transitions = self.LIFECYCLE_TRANSITIONS.get(current_state, [])
            if new_state not in allowed_transitions:
                return self._err(
                    'set_lifecycle_state',
                    f'Invalid transition from {current_state} to {new_state}',
                    allowed=allowed_transitions,
                    current_state=current_state,
                )
            timestamp = datetime.now(timezone.utc).date().isoformat()
            cursor.execute(
                """
                UPDATE keywords
                SET lifecycle_state = ?,
                    lifecycle_updated_at = ?
                WHERE id = ?
                """,
                (new_state, timestamp, keyword_id),
            )
            cursor.execute(
                """
                INSERT INTO lifecycle_history (keyword_id, from_state, to_state, transitioned_at)
                VALUES (?, ?, ?, ?)
                """,
                (keyword_id, current_state, new_state, timestamp),
            )
            self._conn.commit()
            return {'status': 'transitioned', 'from': current_state, 'to': new_state, 'timestamp': timestamp}
        except sqlite3.Error as e:
            return self._err('set_lifecycle_state', 'Database operation failed', e)

    def get_lifecycle_state(self, keyword_id: int) -> str:
        try:
            cursor = self._conn.cursor()
            cursor.execute("SELECT lifecycle_state FROM keywords WHERE id = ?", (keyword_id,))
            row = cursor.fetchone()
            if row is None or row[0] is None:
                return 'DISCOVERED'
            return row[0]
        except sqlite3.Error:
            return 'DISCOVERED'

    def get_keywords_by_lifecycle(self, state: str, limit: int = 50) -> List[Dict[str, Any]]:
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
                (state, limit),
            )
            return [dict(row) for row in cursor.fetchall()]
        except sqlite3.Error:
            return []
