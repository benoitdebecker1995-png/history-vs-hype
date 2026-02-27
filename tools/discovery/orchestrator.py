"""
Opportunity Orchestrator Module

Combines Phase 15-17 modules into a single analysis pipeline:
- Demand analysis (Phase 15)
- Competition analysis (Phase 16)
- Production constraints (Phase 17)
- Opportunity scoring (Phase 18)

Usage:
    CLI:
        python orchestrator.py "dark ages myth"
        python orchestrator.py "treaty of versailles" --report
        python orchestrator.py --list-state ANALYZED

    Python:
        from tools.discovery.orchestrator import OpportunityOrchestrator
        from tools.discovery.database import KeywordDB

        db = KeywordDB()
        orch = OpportunityOrchestrator(db)
        result = orch.analyze_opportunity("dark ages myth")
"""

import sys
import argparse
import json
from pathlib import Path
from typing import Dict, Optional, Any, List
from datetime import datetime, timezone

from .database import KeywordDB
from .demand import DemandAnalyzer
from .competition import CompetitionAnalyzer
from .format_filters import evaluate_production_constraints
from .opportunity import OpportunityScorer
from tools.logging_config import get_logger

logger = get_logger(__name__)


class OpportunityOrchestrator:
    """
    Orchestrate opportunity scoring across all phases.

    Aggregates: Demand (15) + Competition (16) + Format (17) → Opportunity (18)
    """

    def __init__(self, db: KeywordDB):
        """
        Initialize opportunity orchestrator.

        Args:
            db: KeywordDB instance
        """
        self.db = db
        self.demand = DemandAnalyzer(db)
        self.competition = CompetitionAnalyzer()
        self.scorer = OpportunityScorer(db)

    def analyze_opportunity(self, keyword: str, force_refresh: bool = False) -> Dict[str, Any]:
        """
        Complete opportunity analysis pipeline.

        STEP 1: Run demand analysis (Phase 15)
        STEP 2: Get keyword_id from database
        STEP 3: Run competition analysis (Phase 16)
        STEP 4: Get/evaluate production constraints (Phase 17)
        STEP 5: Score opportunity (Phase 18)
        STEP 6: Save score and update lifecycle
        STEP 7: Build complete result dict with all data from phases

        Args:
            keyword: Keyword to analyze
            force_refresh: Force refresh all cached data

        Returns:
            Complete opportunity analysis dict or error dict
        """
        # STEP 1: Demand analysis
        logger.info("[1/5] Running demand analysis for '%s'...", keyword)
        demand_data = self.demand.analyze_keyword(keyword, force_refresh=force_refresh)

        if 'error' in demand_data:
            return demand_data

        # STEP 2: Get keyword_id from database
        keyword_record = self.db.get_keyword(keyword)
        if not keyword_record:
            return {'error': f'Keyword not found in database: {keyword}'}

        keyword_id = keyword_record['id']

        # STEP 3: Competition analysis
        logger.info("[2/5] Running competition analysis...")
        comp_data = self.competition.analyze_competition(keyword)

        if 'error' in comp_data:
            return comp_data

        # STEP 4: Get/evaluate production constraints
        logger.info("[3/5] Evaluating production constraints...")
        constraints = self.db.get_production_constraints(keyword_id)

        if constraints is None:
            # Evaluate and store if not cached
            constraints = evaluate_production_constraints(keyword)

            # Store in database
            cursor = self.db._conn.cursor()
            cursor.execute(
                """
                UPDATE keywords
                SET production_constraints = ?,
                    constraint_checked_at = ?
                WHERE id = ?
                """,
                (json.dumps(constraints), datetime.now(timezone.utc).date().isoformat(), keyword_id)
            )
            self.db._conn.commit()

        # STEP 5: Score opportunity
        logger.info("[4/5] Calculating opportunity score...")
        score_result = self.scorer.score_opportunity(
            keyword_id=keyword_id,
            demand_data=demand_data,
            competition_data=comp_data,
            constraints=constraints
        )

        # STEP 6: Save score and update lifecycle
        logger.info("[5/5] Saving results...")
        save_result = self.scorer.save_opportunity_score(keyword_id, score_result)

        if 'error' in save_result:
            logger.warning("Failed to save score: %s", save_result['error'])

        # STEP 7: Build complete result dict
        result = {
            'keyword': keyword,
            'keyword_id': keyword_id,
            'opportunity_score': score_result.get('opportunity_score'),
            'category': score_result.get('category'),
            'is_blocked': score_result.get('is_blocked', False),
            'block_reason': score_result.get('block_reason'),
            'components': score_result.get('components', {}),
            'demand': {
                'search_volume_proxy': demand_data.get('search_volume_proxy', 0),
                'trend_direction': demand_data.get('trend_direction', 'unknown'),
                'opportunity_ratio': demand_data.get('opportunity_ratio', 'N/A')
            },
            'competition': {
                'video_count': comp_data.get('video_count', 0),
                'channel_count': comp_data.get('channel_count', 0),
                'quality_video_count': comp_data.get('quality_video_count', 0),
                'differentiation_score': comp_data.get('differentiation_score', 0),
                'recommended_angle': comp_data.get('recommended_angle', 'unknown')
            },
            'production': {
                'document_score': constraints.get('document_score', 2),
                'is_animation_blocked': constraints.get('is_production_blocked', False),
                'source_hints': constraints.get('source_hints', {})
            },
            'lifecycle_state': self.db.get_lifecycle_state(keyword_id),
            'data_age_days': score_result.get('data_age_days', 0),
            'warnings': score_result.get('warnings', []),
            'fetched_at': datetime.now(timezone.utc).isoformat() + 'Z'
        }

        return result

    def transition_keyword(self, keyword: str, new_state: str) -> Dict[str, Any]:
        """
        Transition keyword to new lifecycle state.

        Args:
            keyword: Keyword to transition
            new_state: Target lifecycle state

        Returns:
            Result dict with status or error
        """
        keyword_record = self.db.get_keyword(keyword)
        if not keyword_record:
            return {'error': f'Keyword not found: {keyword}'}

        keyword_id = keyword_record['id']

        result = self.db.set_lifecycle_state(keyword_id, new_state)
        return result

    def list_by_state(self, state: str, limit: int = 50) -> List[Dict]:
        """
        Get all keywords in a specific lifecycle state.

        Args:
            state: Lifecycle state to filter by
            limit: Maximum number of results

        Returns:
            List of keyword dicts with opportunity scores
        """
        keywords = self.db.get_keywords_by_lifecycle(state, limit)
        return keywords

    def generate_report(self, keyword: str, output_path: Optional[str] = None) -> str:
        """
        Generate Markdown opportunity report from analysis.

        Args:
            keyword: Keyword to analyze and report on
            output_path: Optional file path to write report

        Returns:
            Rendered Markdown string
        """
        # Run analysis
        analysis = self.analyze_opportunity(keyword)

        if 'error' in analysis:
            return f"# Error\n\n{analysis['error']}"

        # Load Jinja2 template
        try:
            from jinja2 import Environment, FileSystemLoader

            template_dir = Path(__file__).parent / 'templates'
            env = Environment(loader=FileSystemLoader(template_dir))
            template = env.get_template('opportunity_report.md.j2')

            # Render template
            markdown = template.render(data=analysis)

            # Write to file if path provided
            if output_path:
                Path(output_path).write_text(markdown, encoding='utf-8')
                logger.info("Report saved to: %s", output_path)

            return markdown

        except ImportError:
            # Fallback to simple formatting if jinja2 not installed
            return self._generate_simple_report(analysis, output_path)

    def _generate_simple_report(self, data: Dict, output_path: Optional[str] = None) -> str:
        """
        Generate simple Markdown report without Jinja2.

        Args:
            data: Analysis data dict
            output_path: Optional file path to write report

        Returns:
            Simple Markdown string
        """
        lines = [
            f"# Opportunity Report: {data['keyword']}",
            "",
            f"**Generated:** {data['fetched_at']}",
            f"**Lifecycle State:** {data['lifecycle_state']}",
            "",
            "---",
            "",
            "## Opportunity Score",
            ""
        ]

        if data['is_blocked']:
            lines.extend([
                f"**BLOCKED:** {data['block_reason']}",
                "",
                "This topic cannot be produced with the channel's documentary format.",
                ""
            ])
        else:
            score = data['opportunity_score']
            bar_filled = int(score / 5)
            bar_empty = 20 - bar_filled
            bar = '[' + '#' * bar_filled + '-' * bar_empty + ']'

            lines.extend([
                f"**Score:** {score}/100 ({data['category']})",
                "",
                f"`{bar}`",
                ""
            ])

        # Add demand section
        lines.extend([
            "---",
            "",
            "## Demand Analysis",
            "",
            "| Metric | Value |",
            "|--------|-------|",
            f"| Search Volume Proxy | {data['demand']['search_volume_proxy']} |",
            f"| Trend Direction | {data['demand']['trend_direction']} |",
            f"| Opportunity Ratio | {data['demand']['opportunity_ratio']} |",
            ""
        ])

        # Add competition section
        lines.extend([
            "---",
            "",
            "## Competition Analysis",
            "",
            "| Metric | Value |",
            "|--------|-------|",
            f"| Total Videos | {data['competition']['video_count']} |",
            f"| Unique Channels | {data['competition']['channel_count']} |",
            f"| Quality Videos | {data['competition']['quality_video_count']} |",
            f"| Differentiation Score | {data['competition']['differentiation_score']} |",
            f"| Recommended Angle | {data['competition']['recommended_angle']} |",
            ""
        ])

        # Add production section
        lines.extend([
            "---",
            "",
            "## Production Constraints",
            "",
            "| Metric | Value |",
            "|--------|-------|",
            f"| Document Score | {data['production']['document_score']}/4 |",
            f"| Animation Blocked | {'Yes' if data['production']['is_animation_blocked'] else 'No'} |",
            ""
        ])

        markdown = '\n'.join(lines)

        if output_path:
            Path(output_path).write_text(markdown, encoding='utf-8')
            logger.info("Report saved to: %s", output_path)

        return markdown


def print_analysis_table(result: Dict):
    """
    Print opportunity analysis in ASCII table format.

    Args:
        result: Analysis result from analyze_opportunity()
    """
    print("\n" + "=" * 70)
    print(f"  Opportunity Analysis: {result['keyword']}")
    print("=" * 70)

    if result['is_blocked']:
        print(f"\nVERDICT: BLOCKED")
        print(f"  Reason: {result['block_reason']}")
        print()
        return

    score = result['opportunity_score']
    category = result['category']

    # Score bar (ASCII-safe)
    bar_filled = int(score / 5)
    bar_empty = 20 - bar_filled
    score_bar = '[' + '#' * bar_filled + '-' * bar_empty + ']'

    print(f"\nVERDICT: {category.upper()} ({score}/100)")
    print(f"  Score:              {score_bar}")

    # Production constraints
    doc_score = result['production']['document_score']
    doc_bar_filled = int(doc_score * 5)
    doc_bar_empty = 20 - doc_bar_filled
    doc_bar = '[' + '#' * doc_bar_filled + '-' * doc_bar_empty + ']'

    print(f"  Document Score:     {doc_score}/4  {doc_bar}")
    print(f"  Animation Risk:     {'HIGH' if result['production']['is_animation_blocked'] else 'LOW'}")

    # Components breakdown
    if result['components']:
        print("\nCOMPONENTS:")
        for name, comp in result['components'].items():
            contrib = comp['contribution']
            weight_pct = int(comp['weight'] * 100)
            print(f"  {name.capitalize():15} {comp['normalized']:5.1f}  (weight: {weight_pct:2d}%)  -> {contrib:5.1f}")

    # Demand details
    print("\nDEMAND:")
    print(f"  Search Volume:      {result['demand']['search_volume_proxy']}/100")
    print(f"  Trend:              {result['demand']['trend_direction']}")
    print(f"  Opportunity Ratio:  {result['demand']['opportunity_ratio']}")

    # Competition details
    print("\nCOMPETITION:")
    print(f"  Total Videos:       {result['competition']['video_count']}")
    print(f"  Quality Videos:     {result['competition']['quality_video_count']}")
    print(f"  Channels:           {result['competition']['channel_count']}")
    print(f"  Differentiation:    {result['competition']['differentiation_score']:.2f}")
    print(f"  Recommended Angle:  {result['competition']['recommended_angle']}")

    # Warnings
    if result['warnings']:
        print("\nWARNINGS:")
        for warning in result['warnings']:
            print(f"  - {warning}")

    # Recommendation
    print("\nRECOMMENDATION:", end=" ")
    if score >= 70:
        print("Proceed to research phase")
    elif score >= 50:
        print("Proceed with source verification")
    elif score >= 30:
        print("Consider alternatives or reframing")
    else:
        print("Low opportunity - skip or reframe significantly")

    print()


def main():
    """CLI entry point for opportunity orchestrator."""
    parser = argparse.ArgumentParser(
        description='Opportunity Orchestrator - Complete niche discovery analysis'
    )

    # Main arguments
    parser.add_argument('keyword', nargs='?', help='Keyword to analyze')
    parser.add_argument('--report', action='store_true', help='Generate Markdown report')
    parser.add_argument('--output', help='Output file path for report')
    parser.add_argument('--refresh', action='store_true', help='Force refresh all cached data')
    parser.add_argument('--json', action='store_true', help='Output JSON format')

    # Lifecycle management
    parser.add_argument('--list-state', help='List keywords by lifecycle state')
    parser.add_argument('--transition', nargs=2, metavar=('KEYWORD', 'STATE'),
                        help='Transition keyword to new state')

    verbosity = parser.add_mutually_exclusive_group()
    verbosity.add_argument("--verbose", "-v", action="store_true", help="Show debug output on stderr")
    verbosity.add_argument("--quiet", "-q", action="store_true", help="Only show errors on stderr")

    args = parser.parse_args()

    from tools.logging_config import setup_logging
    setup_logging(args.verbose, args.quiet)

    # Initialize database and orchestrator
    db = KeywordDB()
    orch = OpportunityOrchestrator(db)

    # List keywords by state
    if args.list_state:
        keywords = orch.list_by_state(args.list_state)

        if args.json:
            print(json.dumps(keywords, indent=2))
        else:
            print(f"\n=== Keywords in state: {args.list_state} ===\n")
            for kw in keywords:
                score = kw.get('opportunity_score_final', 'N/A')
                category = kw.get('opportunity_category', 'N/A')
                print(f"  {kw['keyword']:40} {score:>6} ({category})")
            print()

        return

    # Transition keyword state
    if args.transition:
        keyword, new_state = args.transition
        result = orch.transition_keyword(keyword, new_state)

        if 'error' in result:
            print(f"Error: {result['error']}", file=sys.stderr)
            sys.exit(1)
        else:
            print(f"Transitioned '{keyword}' from {result['from']} to {result['to']}")

        return

    # Analyze opportunity (requires keyword)
    if not args.keyword:
        parser.print_help()
        sys.exit(1)

    # Generate report
    if args.report:
        markdown = orch.generate_report(args.keyword, args.output)
        if not args.output:
            print(markdown)
        return

    # Run analysis
    result = orch.analyze_opportunity(args.keyword, force_refresh=args.refresh)

    if 'error' in result:
        print(f"Error: {result['error']}", file=sys.stderr)
        sys.exit(1)

    # Output format
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print_analysis_table(result)


if __name__ == '__main__':
    main()
