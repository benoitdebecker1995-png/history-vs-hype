#!/usr/bin/env python3
"""
Technique Library - Database CRUD for creator technique storage.

Stores extracted patterns from transcript analysis in creator_techniques table.
Follows error dict pattern from existing tools (returns {'error': msg} on failure).

Usage:
    from technique_library import TechniqueLibrary

    lib = TechniqueLibrary()
    lib.add_technique('opening_hook', 'visual_contrast', ...)
    techniques = lib.get_techniques_by_category('opening_hook')

Database: tools/discovery/keywords.db (schema v29)
"""

import sqlite3
import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
import argparse


class TechniqueLibrary:
    """
    Database CRUD operations for creator technique storage.

    All methods return dicts with results or {'error': msg} on failure.
    Migrates schema to v29 on first run.
    """

    def __init__(self, db_path: Optional[str] = None):
        """
        Initialize database connection.

        Args:
            db_path: Path to SQLite database (default: ../../tools/discovery/keywords.db)
        """
        if db_path is None:
            # Default to keywords.db in tools/discovery/
            script_dir = Path(__file__).parent
            db_path = str(script_dir / '../../tools/discovery/keywords.db')

        self.db_path = Path(db_path).resolve()
        self._conn = None
        self._ensure_connection()
        self._ensure_schema_v28()
        self._ensure_schema_v29()

    def _ensure_connection(self):
        """Ensure database connection exists."""
        if self._conn is None:
            self._conn = sqlite3.connect(str(self.db_path))
            self._conn.row_factory = sqlite3.Row

    def _get_schema_version(self) -> int:
        """Get current schema version from PRAGMA user_version."""
        try:
            cursor = self._conn.cursor()
            cursor.execute("PRAGMA user_version")
            row = cursor.fetchone()
            return row[0] if row else 0
        except sqlite3.Error:
            return 0

    def _set_schema_version(self, version: int):
        """Set schema version via PRAGMA user_version."""
        try:
            cursor = self._conn.cursor()
            cursor.execute(f"PRAGMA user_version = {version}")
            self._conn.commit()
        except sqlite3.Error:
            pass

    def _ensure_schema_v28(self):
        """
        Migrate database to schema v28 (creator_techniques table).

        Creates:
        - creator_techniques table with technique metadata and creator examples
        - Indexes on category and universal/count for efficient querying
        """
        if self._get_schema_version() >= 28:
            return  # Already migrated

        print("[Phase 37] Migrating database to v28: adding creator_techniques table...", file=sys.stderr)

        try:
            cursor = self._conn.cursor()

            # Create creator_techniques table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS creator_techniques (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    technique_category TEXT NOT NULL,
                    technique_name TEXT NOT NULL,
                    formula TEXT,
                    when_to_use TEXT,
                    creator_examples TEXT,
                    creator_count INTEGER DEFAULT 1,
                    is_universal BOOLEAN DEFAULT 0,
                    style_guide_ref TEXT,
                    created_at DATE NOT NULL,
                    UNIQUE(technique_category, technique_name)
                )
            """)

            # Create indexes for efficient querying
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_technique_category
                ON creator_techniques(technique_category)
            """)

            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_technique_universal_count
                ON creator_techniques(is_universal DESC, creator_count DESC)
            """)

            # Bump schema version to 28
            self._set_schema_version(28)

            self._conn.commit()
            print("[Phase 37] Schema migrated to v28 successfully", file=sys.stderr)

        except sqlite3.Error as e:
            print(f"[Phase 37] Migration failed: {e}", file=sys.stderr)
            return {'error': f'Schema migration failed: {e}'}

    def _ensure_schema_v29(self):
        """
        Migrate database to schema v29 (script_choices table for choice logging).

        Creates:
        - script_choices table with selected/rejected variants and recommendation tracking
        - Indexes on choice_type/topic_type and choice_date for efficient pattern queries
        """
        if self._get_schema_version() >= 29:
            return  # Already migrated

        print("[Phase 38] Migrating database to v29: adding script_choices table...", file=sys.stderr)

        try:
            cursor = self._conn.cursor()

            # Create script_choices table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS script_choices (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    choice_type TEXT NOT NULL,
                    project_path TEXT NOT NULL,
                    topic_type TEXT,
                    selected_variant TEXT NOT NULL,
                    selected_technique TEXT,
                    rejected_variants TEXT,
                    recommended_technique TEXT,
                    choice_date DATE NOT NULL,
                    UNIQUE(choice_type, project_path)
                )
            """)

            # Create indexes for efficient querying
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_choice_type_topic
                ON script_choices(choice_type, topic_type)
            """)

            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_choice_date
                ON script_choices(choice_date DESC)
            """)

            # Bump schema version to 29
            self._set_schema_version(29)

            self._conn.commit()
            print("[Phase 38] Schema migrated to v29 successfully", file=sys.stderr)

        except sqlite3.Error as e:
            print(f"[Phase 38] Migration failed: {e}", file=sys.stderr)
            return {'error': f'Schema migration failed: {e}'}

    def add_technique(
        self,
        category: str,
        name: str,
        formula: str,
        when_to_use: str,
        creator_examples: List[Dict[str, str]],
        is_universal: bool = False,
        style_guide_ref: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Add or update technique in database.

        Args:
            category: Technique category (opening_hook, transition, evidence, pacing)
            name: Technique name (e.g., 'visual_contrast', 'causal_chain')
            formula: Pattern formula or template
            when_to_use: Usage guidance
            creator_examples: List of {'creator': str, 'video': str, 'text': str}
            is_universal: Whether technique appears across 3+ creators
            style_guide_ref: Reference to STYLE-GUIDE.md section if applicable

        Returns:
            {'technique_id': int, 'action': 'inserted'|'updated'} on success
            {'error': msg} on failure
        """
        try:
            # Calculate creator count from unique creators in examples
            unique_creators = set(ex['creator'] for ex in creator_examples)
            creator_count = len(unique_creators)

            # Serialize creator_examples to JSON
            examples_json = json.dumps(creator_examples)

            cursor = self._conn.cursor()

            # UPSERT: Insert or update on conflict
            cursor.execute("""
                INSERT INTO creator_techniques (
                    technique_category, technique_name, formula, when_to_use,
                    creator_examples, creator_count, is_universal, style_guide_ref,
                    created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(technique_category, technique_name) DO UPDATE SET
                    formula = excluded.formula,
                    when_to_use = excluded.when_to_use,
                    creator_examples = excluded.creator_examples,
                    creator_count = excluded.creator_count,
                    is_universal = excluded.is_universal,
                    style_guide_ref = excluded.style_guide_ref
            """, (
                category, name, formula, when_to_use, examples_json,
                creator_count, is_universal, style_guide_ref,
                datetime.now().date().isoformat()
            ))

            self._conn.commit()

            # Determine if insert or update
            action = 'updated' if cursor.rowcount == 2 else 'inserted'

            return {
                'technique_id': cursor.lastrowid,
                'action': action
            }

        except sqlite3.Error as e:
            return {'error': f'Failed to add technique: {e}'}

    def get_techniques_by_category(self, category: str) -> List[Dict[str, Any]]:
        """
        Get all techniques in a category, ordered by creator_count DESC.

        Args:
            category: Category to filter by

        Returns:
            List of technique dicts with creator_examples parsed from JSON
        """
        try:
            cursor = self._conn.cursor()
            cursor.execute("""
                SELECT * FROM creator_techniques
                WHERE technique_category = ?
                ORDER BY creator_count DESC
            """, (category,))

            rows = cursor.fetchall()
            results = []

            for row in rows:
                technique = dict(row)
                # Parse creator_examples JSON back to list
                if technique['creator_examples']:
                    technique['creator_examples'] = json.loads(technique['creator_examples'])
                results.append(technique)

            return results

        except sqlite3.Error as e:
            return [{'error': f'Query failed: {e}'}]

    def get_universal_techniques(self) -> List[Dict[str, Any]]:
        """
        Get all universal techniques (is_universal=True), ordered by creator_count DESC.

        Returns:
            List of technique dicts
        """
        try:
            cursor = self._conn.cursor()
            cursor.execute("""
                SELECT * FROM creator_techniques
                WHERE is_universal = 1
                ORDER BY creator_count DESC
            """)

            rows = cursor.fetchall()
            results = []

            for row in rows:
                technique = dict(row)
                if technique['creator_examples']:
                    technique['creator_examples'] = json.loads(technique['creator_examples'])
                results.append(technique)

            return results

        except sqlite3.Error as e:
            return [{'error': f'Query failed: {e}'}]

    def get_all_techniques(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Get all techniques, grouped by category.

        Returns:
            {'category_name': [techniques], ...}
        """
        try:
            cursor = self._conn.cursor()
            cursor.execute("""
                SELECT * FROM creator_techniques
                ORDER BY technique_category, creator_count DESC
            """)

            rows = cursor.fetchall()
            grouped = {}

            for row in rows:
                technique = dict(row)
                if technique['creator_examples']:
                    technique['creator_examples'] = json.loads(technique['creator_examples'])

                category = technique['technique_category']
                if category not in grouped:
                    grouped[category] = []
                grouped[category].append(technique)

            return grouped

        except sqlite3.Error as e:
            return {'error': f'Query failed: {e}'}

    def get_technique_categories(self) -> List[str]:
        """
        Get list of distinct technique categories.

        Returns:
            List of category names
        """
        try:
            cursor = self._conn.cursor()
            cursor.execute("""
                SELECT DISTINCT technique_category
                FROM creator_techniques
                ORDER BY technique_category
            """)

            return [row[0] for row in cursor.fetchall()]

        except sqlite3.Error as e:
            return [f'ERROR: {e}']

    def search_techniques(self, query: str) -> List[Dict[str, Any]]:
        """
        Search techniques by name, formula, or when_to_use.

        Args:
            query: Search term

        Returns:
            List of matching techniques
        """
        try:
            cursor = self._conn.cursor()
            search_pattern = f'%{query}%'

            cursor.execute("""
                SELECT * FROM creator_techniques
                WHERE technique_name LIKE ?
                   OR formula LIKE ?
                   OR when_to_use LIKE ?
                ORDER BY creator_count DESC
            """, (search_pattern, search_pattern, search_pattern))

            rows = cursor.fetchall()
            results = []

            for row in rows:
                technique = dict(row)
                if technique['creator_examples']:
                    technique['creator_examples'] = json.loads(technique['creator_examples'])
                results.append(technique)

            return results

        except sqlite3.Error as e:
            return [{'error': f'Search failed: {e}'}]

    def store_analysis_results(self, analyses: List[Dict[str, Any]]) -> Dict[str, int]:
        """
        Transform transcript analysis results into technique rows.

        Takes output from transcript_analyzer.analyze_all_transcripts(),
        aggregates patterns by type, and stores as techniques.

        Args:
            analyses: List of analysis dicts from transcript_analyzer

        Returns:
            {'stored': int, 'updated': int, 'errors': int}
        """
        stored = 0
        updated = 0
        errors = 0

        # Aggregate patterns by type across all transcripts
        pattern_aggregator = {}

        for analysis in analyses:
            if 'error' in analysis:
                errors += 1
                continue

            creator = analysis.get('creator', 'Unknown')
            file_name = Path(analysis.get('file', '')).name

            # Process opening hook patterns
            opening_hook = analysis.get('opening_hook', {})
            for pattern in opening_hook.get('detected_patterns', []):
                key = ('opening_hook', pattern)
                if key not in pattern_aggregator:
                    pattern_aggregator[key] = []
                pattern_aggregator[key].append({
                    'creator': creator,
                    'video': file_name,
                    'text': opening_hook.get('text_sample', '')[:200]
                })

            # Process transition patterns
            transitions = analysis.get('transitions', [])
            for trans in transitions:
                pattern_type = trans.get('pattern_type')
                key = ('transition', pattern_type)
                if key not in pattern_aggregator:
                    pattern_aggregator[key] = []
                pattern_aggregator[key].append({
                    'creator': creator,
                    'video': file_name,
                    'text': trans.get('text', '')[:200]
                })

        # Store aggregated patterns as techniques
        for (category, name), examples in pattern_aggregator.items():
            # Deduplicate examples by creator (keep first occurrence)
            seen_creators = set()
            unique_examples = []
            for ex in examples:
                if ex['creator'] not in seen_creators:
                    seen_creators.add(ex['creator'])
                    unique_examples.append(ex)

            # Create technique
            formula = f"Pattern: {name}"
            when_to_use = "Extracted from creator transcripts"
            is_universal = len(unique_examples) >= 3

            result = self.add_technique(
                category=category,
                name=name,
                formula=formula,
                when_to_use=when_to_use,
                creator_examples=unique_examples[:10],  # Limit to 10 examples
                is_universal=is_universal
            )

            if 'error' in result:
                errors += 1
            elif result['action'] == 'inserted':
                stored += 1
            else:
                updated += 1

        return {
            'stored': stored,
            'updated': updated,
            'errors': errors
        }

    def get_stats(self) -> Dict[str, Any]:
        """
        Get database statistics.

        Returns:
            {
                'total_techniques': int,
                'universal_count': int,
                'by_category': {'category': count, ...}
            }
        """
        try:
            cursor = self._conn.cursor()

            # Total techniques
            cursor.execute("SELECT COUNT(*) FROM creator_techniques")
            total = cursor.fetchone()[0]

            # Universal count
            cursor.execute("SELECT COUNT(*) FROM creator_techniques WHERE is_universal = 1")
            universal = cursor.fetchone()[0]

            # By category
            cursor.execute("""
                SELECT technique_category, COUNT(*) as count
                FROM creator_techniques
                GROUP BY technique_category
                ORDER BY count DESC
            """)
            by_category = {row[0]: row[1] for row in cursor.fetchall()}

            return {
                'total_techniques': total,
                'universal_count': universal,
                'by_category': by_category
            }

        except sqlite3.Error as e:
            return {'error': f'Stats query failed: {e}'}

    def get_statistics(self) -> Dict[str, Any]:
        """Alias for get_stats() for compatibility with pattern_synthesizer_v2."""
        return self.get_stats()

    def _update_technique_universal_status(
        self,
        technique_id: int,
        is_universal: bool,
        style_guide_ref: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Update technique universal status and Part 6 cross-reference.

        Args:
            technique_id: Technique ID to update
            is_universal: Whether technique is universal (3+ creators)
            style_guide_ref: Part 6 cross-reference (e.g., "Part 6.1: Visual Contrast Hook")

        Returns:
            {'success': True} or {'error': str}
        """
        try:
            cursor = self._conn.cursor()
            cursor.execute("""
                UPDATE creator_techniques
                SET is_universal = ?,
                    style_guide_ref = ?
                WHERE id = ?
            """, (is_universal, style_guide_ref, technique_id))

            self._conn.commit()
            return {'success': True}

        except sqlite3.Error as e:
            return {'error': f'Update failed: {e}'}

    # ========== CHOICE LOGGING METHODS (Phase 38) ==========

    def log_choice(
        self,
        choice_type: str,
        project_path: str,
        topic_type: str,
        selected_variant: str,
        selected_technique: Optional[str],
        all_variants: List[str],
        recommended_technique: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Log user's variant choice with full context.

        Args:
            choice_type: 'opening_hook' or 'structural_approach'
            project_path: Path to video project directory
            topic_type: 'territorial', 'ideological', 'factcheck', etc.
            selected_variant: 'Hook A', 'Structure 1', etc.
            selected_technique: Part 8 technique name (or None)
            all_variants: ['Hook A', 'Hook B', 'Hook C']
            recommended_technique: What was recommended (for override tracking)

        Returns:
            {'logged': True, 'action': 'inserted'|'updated'} on success
            {'error': msg} on failure
        """
        try:
            # Compute rejected variants
            rejected = [v for v in all_variants if v != selected_variant]

            # Normalize project path
            normalized_path = str(Path(project_path).resolve())

            cursor = self._conn.cursor()

            # UPSERT pattern
            cursor.execute("""
                INSERT INTO script_choices (
                    choice_type, project_path, topic_type,
                    selected_variant, selected_technique, rejected_variants,
                    recommended_technique, choice_date
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(choice_type, project_path) DO UPDATE SET
                    selected_variant = excluded.selected_variant,
                    selected_technique = excluded.selected_technique,
                    rejected_variants = excluded.rejected_variants,
                    recommended_technique = excluded.recommended_technique,
                    choice_date = excluded.choice_date
            """, (
                choice_type,
                normalized_path,
                topic_type,
                selected_variant,
                selected_technique,
                json.dumps(rejected),
                recommended_technique,
                datetime.now().date().isoformat()
            ))

            self._conn.commit()

            # Determine action (2 rows affected = update, 1 = insert)
            action = 'updated' if cursor.rowcount == 2 else 'inserted'

            return {
                'logged': True,
                'action': action
            }

        except sqlite3.Error as e:
            return {'error': f'Failed to log choice: {e}'}

    def get_choices(
        self,
        choice_type: Optional[str] = None,
        topic_type: Optional[str] = None,
        limit: int = 50
    ) -> Dict[str, Any]:
        """
        Query script_choices with optional filters.

        Args:
            choice_type: Filter by 'opening_hook' or 'structural_approach'
            topic_type: Filter by topic type
            limit: Maximum results to return

        Returns:
            {'choices': [list of dicts]} on success
            {'error': msg} on failure
        """
        try:
            cursor = self._conn.cursor()

            # Build query with optional filters
            conditions = []
            params = []

            if choice_type:
                conditions.append("choice_type = ?")
                params.append(choice_type)

            if topic_type:
                conditions.append("topic_type = ?")
                params.append(topic_type)

            where_clause = " AND ".join(conditions) if conditions else "1=1"
            params.append(limit)

            cursor.execute(f"""
                SELECT * FROM script_choices
                WHERE {where_clause}
                ORDER BY choice_date DESC
                LIMIT ?
            """, params)

            rows = cursor.fetchall()
            choices = []

            for row in rows:
                choice = dict(row)
                # Deserialize rejected_variants from JSON
                if choice['rejected_variants']:
                    choice['rejected_variants'] = json.loads(choice['rejected_variants'])
                else:
                    choice['rejected_variants'] = []
                choices.append(choice)

            return {'choices': choices}

        except sqlite3.Error as e:
            return {'error': f'Query failed: {e}'}

    def get_choice_stats(self) -> Dict[str, Any]:
        """
        Get choice statistics.

        Returns:
            {
                'total': int,
                'by_type': {'opening_hook': count, 'structural_approach': count},
                'by_topic': {'territorial': count, ...}
            }
        """
        try:
            cursor = self._conn.cursor()

            # Total choices
            cursor.execute("SELECT COUNT(*) FROM script_choices")
            total = cursor.fetchone()[0]

            # By choice_type
            cursor.execute("""
                SELECT choice_type, COUNT(*) as count
                FROM script_choices
                GROUP BY choice_type
            """)
            by_type = {row[0]: row[1] for row in cursor.fetchall()}

            # By topic_type
            cursor.execute("""
                SELECT topic_type, COUNT(*) as count
                FROM script_choices
                WHERE topic_type IS NOT NULL
                GROUP BY topic_type
            """)
            by_topic = {row[0]: row[1] for row in cursor.fetchall()}

            return {
                'total': total,
                'by_type': by_type,
                'by_topic': by_topic
            }

        except sqlite3.Error as e:
            return {'error': f'Stats query failed: {e}'}

    def get_recommendation(
        self,
        choice_type: str,
        topic_type: str,
        available_techniques: Optional[List[Dict[str, Any]]] = None,
        decay_factor: float = 0.9
    ) -> Optional[Dict[str, Any]]:
        """
        Get recommended technique based on past choices with recency weighting.

        Implements three-tier fallback:
        1. Topic-specific (>=3 choices for this topic_type)
        2. Global (>=5 choices across all topics)
        3. Part 8 fallback (highest creator_count)

        Args:
            choice_type: 'opening_hook' or 'structural_approach'
            topic_type: 'territorial', 'ideological', etc.
            available_techniques: List of technique dicts with 'name' and 'creator_count'
            decay_factor: Exponential decay factor (0.9 = each older choice worth 90%)

        Returns:
            {
                'recommended': technique_name,
                'reason': str,
                'confidence': 'HIGH'|'MEDIUM'|'LOW',
                'source': 'topic'|'global'|'part8'
            } or None if insufficient data
        """
        try:
            cursor = self._conn.cursor()

            # Tier 1: Topic-specific (>=3 choices)
            cursor.execute("""
                SELECT selected_technique, choice_date
                FROM script_choices
                WHERE choice_type = ? AND topic_type = ?
                ORDER BY choice_date DESC
            """, (choice_type, topic_type))

            topic_choices = cursor.fetchall()

            if len(topic_choices) >= 3:
                # Score techniques using exponential decay
                scores = {}
                for idx, row in enumerate(topic_choices):
                    tech = row[0]
                    if tech:
                        weight = decay_factor ** idx
                        scores[tech] = scores.get(tech, 0) + weight

                # Find highest scoring technique that should still be recommended
                for tech in sorted(scores.keys(), key=lambda t: scores[t], reverse=True):
                    if self._should_recommend(tech, choice_type, topic_type):
                        selections = sum(1 for r in topic_choices if r[0] == tech)
                        return {
                            'recommended': tech,
                            'reason': f'you chose this pattern {selections}/{len(topic_choices)} times for {topic_type} topics',
                            'confidence': 'HIGH' if len(topic_choices) >= 5 else 'MEDIUM',
                            'source': 'topic'
                        }

            # Tier 2: Global (>=5 choices across all topics)
            cursor.execute("""
                SELECT selected_technique, choice_date
                FROM script_choices
                WHERE choice_type = ?
                ORDER BY choice_date DESC
            """, (choice_type,))

            global_choices = cursor.fetchall()

            if len(global_choices) >= 5:
                # Score techniques using exponential decay
                scores = {}
                for idx, row in enumerate(global_choices):
                    tech = row[0]
                    if tech:
                        weight = decay_factor ** idx
                        scores[tech] = scores.get(tech, 0) + weight

                # Find highest scoring technique
                for tech in sorted(scores.keys(), key=lambda t: scores[t], reverse=True):
                    if self._should_recommend(tech, choice_type, topic_type):
                        selections = sum(1 for r in global_choices if r[0] == tech)
                        return {
                            'recommended': tech,
                            'reason': f'you chose this pattern {selections}/{len(global_choices)} times overall',
                            'confidence': 'MEDIUM',
                            'source': 'global'
                        }

            # Tier 3: Part 8 fallback (highest creator_count)
            if available_techniques:
                # Sort by creator_count and return highest
                sorted_techs = sorted(
                    available_techniques,
                    key=lambda t: t.get('creator_count', 0),
                    reverse=True
                )
                if sorted_techs:
                    top = sorted_techs[0]
                    tech_name = top.get('name') or top.get('technique_name', 'unknown')
                    creator_count = top.get('creator_count', 0)
                    return {
                        'recommended': tech_name,
                        'reason': f'most validated by creators ({creator_count} creators)',
                        'confidence': 'LOW',
                        'source': 'part8'
                    }

            # No recommendation available
            return None

        except sqlite3.Error as e:
            return None

    def _should_recommend(
        self,
        technique: str,
        choice_type: str,
        topic_type: str
    ) -> bool:
        """
        Check if technique should be recommended (auto-adjust after 3 consecutive overrides).

        Args:
            technique: Technique name to check
            choice_type: 'opening_hook' or 'structural_approach'
            topic_type: Topic type filter

        Returns:
            False if technique was recommended but overridden 3 consecutive times, else True
        """
        try:
            cursor = self._conn.cursor()

            # Get last 3 choices where this technique was recommended
            cursor.execute("""
                SELECT selected_technique, recommended_technique
                FROM script_choices
                WHERE choice_type = ? AND topic_type = ? AND recommended_technique = ?
                ORDER BY choice_date DESC
                LIMIT 3
            """, (choice_type, topic_type, technique))

            rows = cursor.fetchall()

            # If we have 3 consecutive overrides, don't recommend
            if len(rows) == 3:
                all_overridden = all(row[0] != row[1] for row in rows)
                if all_overridden:
                    return False

            return True

        except sqlite3.Error:
            return True  # On error, allow recommendation

    def get_choice_summary_for_topic(
        self,
        topic_type: str
    ) -> Dict[str, Any]:
        """
        Get choice pattern summary for a topic type (for surfacing in /script).

        Args:
            topic_type: Topic type to analyze

        Returns:
            {
                'hook_patterns': [{'technique': str, 'count': int, 'total': int}],
                'structure_patterns': [...]
            }
        """
        try:
            result = {
                'hook_patterns': [],
                'structure_patterns': []
            }

            cursor = self._conn.cursor()

            # Hook patterns
            cursor.execute("""
                SELECT selected_technique, COUNT(*) as count
                FROM script_choices
                WHERE choice_type = 'opening_hook' AND topic_type = ?
                GROUP BY selected_technique
                ORDER BY count DESC
            """, (topic_type,))

            hook_rows = cursor.fetchall()
            hook_total = sum(row[1] for row in hook_rows)

            if hook_total > 0:
                result['hook_patterns'] = [
                    {'technique': row[0], 'count': row[1], 'total': hook_total}
                    for row in hook_rows
                ]

            # Structure patterns
            cursor.execute("""
                SELECT selected_technique, COUNT(*) as count
                FROM script_choices
                WHERE choice_type = 'structural_approach' AND topic_type = ?
                GROUP BY selected_technique
                ORDER BY count DESC
            """, (topic_type,))

            structure_rows = cursor.fetchall()
            structure_total = sum(row[1] for row in structure_rows)

            if structure_total > 0:
                result['structure_patterns'] = [
                    {'technique': row[0], 'count': row[1], 'total': structure_total}
                    for row in structure_rows
                ]

            return result

        except sqlite3.Error as e:
            return {'error': f'Query failed: {e}'}


def main():
    parser = argparse.ArgumentParser(description='Technique Library - Creator technique storage')
    parser.add_argument('--store-from', metavar='FILE',
                        help='Store analysis results from JSON file')
    parser.add_argument('--list', metavar='CATEGORY', nargs='?', const='ALL',
                        help='List techniques (all or by category)')
    parser.add_argument('--search', metavar='QUERY',
                        help='Search techniques')
    parser.add_argument('--stats', action='store_true',
                        help='Show database statistics')
    parser.add_argument('--choices', metavar='TOPIC_TYPE', nargs='?', const=None,
                        help='Show logged script choices (all or filtered by topic type)')
    parser.add_argument('--choice-stats', action='store_true',
                        help='Show choice statistics')
    parser.add_argument('--db', metavar='PATH',
                        help='Override database path')

    args = parser.parse_args()

    # Initialize library
    lib = TechniqueLibrary(db_path=args.db)

    if args.store_from:
        # Load analysis results from file
        try:
            with open(args.store_from, 'r', encoding='utf-8') as f:
                data = json.load(f)
                analyses = data.get('analyses', [])

            result = lib.store_analysis_results(analyses)
            print(json.dumps(result, indent=2))

        except Exception as e:
            print(json.dumps({'error': f'Failed to load file: {e}'}), file=sys.stderr)
            sys.exit(1)

    elif args.list:
        if args.list == 'ALL':
            techniques = lib.get_all_techniques()
        else:
            techniques = {args.list: lib.get_techniques_by_category(args.list)}

        print(json.dumps(techniques, indent=2))

    elif args.search:
        results = lib.search_techniques(args.search)
        print(json.dumps(results, indent=2))

    elif args.stats:
        stats = lib.get_stats()
        print(json.dumps(stats, indent=2))

    elif args.choices is not None:
        # Show logged choices
        result = lib.get_choices(topic_type=args.choices if args.choices else None)

        if 'error' in result:
            print(json.dumps(result, indent=2), file=sys.stderr)
            sys.exit(1)

        choices = result['choices']

        if not choices:
            print("No choices logged yet. Use /script --variants to start.")
        else:
            # Display as table
            print(f"\n{'Date':<12} {'Project':<40} {'Topic':<12} {'Type':<18} {'Selected':<15} {'Technique':<25}")
            print("-" * 130)

            for choice in choices:
                project_name = Path(choice['project_path']).name if choice['project_path'] else 'N/A'
                project_display = project_name[:38] + '..' if len(project_name) > 40 else project_name
                topic = choice['topic_type'] or 'N/A'
                choice_type = choice['choice_type'].replace('_', ' ').title()
                selected = choice['selected_variant'] or 'N/A'
                technique = choice['selected_technique'] or 'N/A'
                technique_display = technique[:23] + '..' if len(technique) > 25 else technique
                date = choice['choice_date']

                print(f"{date:<12} {project_display:<40} {topic:<12} {choice_type:<18} {selected:<15} {technique_display:<25}")

            print(f"\nTotal: {len(choices)} choice(s)")

    elif args.choice_stats:
        # Show choice statistics
        stats = lib.get_choice_stats()

        if 'error' in stats:
            print(json.dumps(stats, indent=2), file=sys.stderr)
            sys.exit(1)

        print("\n=== Choice Statistics ===\n")
        print(f"Total choices: {stats['total']}")

        if stats['by_type']:
            print("\nBy choice type:")
            for choice_type, count in stats['by_type'].items():
                print(f"  {choice_type}: {count}")

        if stats['by_topic']:
            print("\nBy topic type:")
            for topic_type, count in stats['by_topic'].items():
                print(f"  {topic_type}: {count}")

        if stats['total'] == 0:
            print("\nNo choices logged yet. Use /script --variants to start.")

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
