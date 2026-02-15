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

Database: tools/discovery/keywords.db (schema v28)
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
    Migrates schema to v28 on first run.
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

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
