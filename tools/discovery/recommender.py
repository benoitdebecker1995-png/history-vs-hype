"""
Topic Recommender Module

Recommends NEW topics based on winning patterns and opportunity scores,
filtering out topics already in production or archived.

Usage:
    CLI:
        python recommender.py                  # Default 5 recommendations
        python recommender.py --limit 10       # More recommendations
        python recommender.py --json           # JSON output
        python recommender.py --topic-type territorial  # Filter by topic

    Python:
        from recommender import TopicRecommender
        from database import KeywordDB

        db = KeywordDB()
        recommender = TopicRecommender(db)
        result = recommender.recommend(limit=5)

Dependencies:
    - database.py (Phase 15+) for KeywordDB queries
    - pattern_extractor.py (Phase 20) for winning patterns

Phase: 21 - Recommendation Engine
"""

import sys
import json
import argparse
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional, Tuple

# Add parent directory to path for youtube-analytics imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'youtube-analytics'))

try:
    from database import KeywordDB
    DATABASE_AVAILABLE = True
except ImportError:
    DATABASE_AVAILABLE = False

try:
    from pattern_extractor import extract_winning_patterns
    PATTERNS_AVAILABLE = True
except ImportError:
    PATTERNS_AVAILABLE = False


def get_existing_topics() -> List[str]:
    """
    Scan video-projects folders to find existing topics.

    Scans _IN_PRODUCTION/ and _ARCHIVED/ folders to extract topic slugs
    from folder names like "1-somaliland-2025" -> "somaliland".

    Returns:
        List of lowercase topic strings for case-insensitive matching.
        Empty list if directories not found.

    Example:
        >>> existing = get_existing_topics()
        >>> print(existing[:3])
        ['somaliland', 'dark ages', 'iran 1953 coup']
    """
    topics = []
    project_root = Path(__file__).parent.parent.parent

    # Folders to scan
    folders = [
        project_root / 'video-projects' / '_IN_PRODUCTION',
        project_root / 'video-projects' / '_ARCHIVED'
    ]

    for folder in folders:
        if not folder.exists():
            continue

        try:
            for item in folder.iterdir():
                if not item.is_dir():
                    continue

                # Skip README.md and hidden folders
                if item.name.startswith('.') or item.name == 'README.md':
                    continue

                # Parse folder name: {number}-{topic-slug-year} or old-{topic}
                name = item.name.lower()

                # Handle "old-topic" format in _ARCHIVED
                if name.startswith('old-'):
                    topic = name[4:]  # Remove "old-" prefix
                else:
                    # Handle "{number}-{topic-slug-year}" format
                    # E.g., "10-dark-ages-2025" -> "dark ages"
                    parts = name.split('-')

                    # Skip if no parts
                    if not parts:
                        continue

                    # Remove leading number if present
                    if parts[0].isdigit():
                        parts = parts[1:]

                    # Remove trailing year if present (4-digit number)
                    if parts and len(parts[-1]) == 4 and parts[-1].isdigit():
                        parts = parts[:-1]

                    # Join remaining parts with spaces
                    topic = ' '.join(parts)

                if topic:
                    topics.append(topic)

        except OSError:
            # Handle permission errors or other OS issues
            continue

    return topics


def topic_matches_existing(keyword: str, existing: List[str]) -> bool:
    """
    Check if keyword matches any existing topic using word-level matching.

    Uses word-level matching (not substring) to prevent false positives.
    "iran coup" matches "iran 1953 coup" but "iranian" does NOT match "iran".

    Args:
        keyword: Keyword to check (e.g., "iran coup documentary")
        existing: List of existing topic strings

    Returns:
        True if match found, False otherwise

    Example:
        >>> existing = ['iran 1953 coup', 'dark ages', 'somaliland']
        >>> topic_matches_existing('iran coup', existing)
        True
        >>> topic_matches_existing('iranian revolution', existing)
        False
    """
    if not existing:
        return False

    # Normalize keyword to words
    keyword_words = set(keyword.lower().split())

    for topic in existing:
        topic_words = set(topic.lower().split())

        # Check if all topic words appear in keyword
        # OR all keyword words appear in topic
        if topic_words.issubset(keyword_words) or keyword_words.issubset(topic_words):
            return True

        # Also check for significant overlap (>= 2 common words)
        common = keyword_words.intersection(topic_words)
        if len(common) >= 2:
            return True

    return False


def calculate_pattern_multiplier(
    keyword: str,
    topic_type: Optional[str],
    angles: Optional[List[str]],
    patterns: Dict[str, Any]
) -> Tuple[float, List[str]]:
    """
    Calculate pattern multiplier based on winning patterns.

    Boosts topics that match the channel's proven winning patterns.

    Args:
        keyword: The keyword being scored
        topic_type: Topic classification (e.g., 'territorial', 'ideological')
        angles: List of content angles (e.g., ['legal', 'historical'])
        patterns: Winning patterns dict from extract_winning_patterns()

    Returns:
        Tuple of (multiplier, reasons):
        - multiplier: 1.0-1.5 boost factor
        - reasons: List of strings explaining the boost

    Example:
        >>> patterns = extract_winning_patterns()
        >>> mult, reasons = calculate_pattern_multiplier(
        ...     'treaty of versailles',
        ...     'territorial',
        ...     ['legal', 'historical'],
        ...     patterns
        ... )
        >>> print(f"Multiplier: {mult:.2f}")
        Multiplier: 1.40
    """
    multiplier = 1.0
    reasons = []

    # Check if patterns data is valid
    if not patterns or 'error' in patterns:
        return 1.0, ['Pattern data unavailable - using base score']

    top_converter_profile = patterns.get('top_converter_profile', {})
    channel_strengths = patterns.get('channel_strengths', {})

    # +0.3 if topic matches dominant topic of top converters
    dominant_topic = top_converter_profile.get('dominant_topic')
    if topic_type and dominant_topic and topic_type.lower() == dominant_topic.lower():
        multiplier += 0.3
        reasons.append(f"Matches dominant topic: {dominant_topic}")

    # +0.2 if any angle matches dominant angles
    dominant_angles = top_converter_profile.get('dominant_angles', [])
    if angles and dominant_angles:
        matching_angles = [a for a in angles if a.lower() in [da.lower() for da in dominant_angles]]
        if matching_angles:
            multiplier += 0.2
            reasons.append(f"Matches top angles: {', '.join(matching_angles)}")

    # +0.1 if topic correlates with high channel strength (>70)
    if topic_type:
        # Map topic types to strength categories
        strength_mapping = {
            'territorial': 'legal_territorial',
            'legal': 'legal_territorial',
            'ideological': 'academic',
            'colonial': 'document_heavy',
            'archaeological': 'document_heavy'
        }

        strength_key = strength_mapping.get(topic_type.lower())
        if strength_key and channel_strengths.get(strength_key, 0) > 70:
            multiplier += 0.1
            reasons.append(f"Channel strength {strength_key}: {channel_strengths[strength_key]:.0f}/100")

    # Cap at 1.5 maximum
    multiplier = min(1.5, multiplier)

    if not reasons:
        reasons.append('No pattern match - using base score')

    return multiplier, reasons


class TopicRecommender:
    """
    Recommends topics based on winning patterns and opportunity scores.

    Combines:
    - Opportunity scores from Phase 18
    - Winning patterns from Phase 20
    - Exclusion of existing production topics

    Example:
        db = KeywordDB()
        recommender = TopicRecommender(db)
        result = recommender.recommend(limit=5)
        for r in result['recommendations']:
            print(f"{r['rank']}. {r['keyword']}: {r['final_score']:.1f}")
    """

    def __init__(self, db: 'KeywordDB'):
        """
        Initialize recommender with database connection.

        Args:
            db: KeywordDB instance for querying keywords
        """
        self.db = db

    def recommend(
        self,
        limit: int = 5,
        topic_filter: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate ranked topic recommendations.

        Pipeline:
        1. Load winning patterns
        2. Get all ANALYZED keywords from database
        3. Filter out topics matching existing production folders
        4. Calculate pattern multiplier for each
        5. Compute final_score = opportunity_score * multiplier
        6. Sort and return top N

        Args:
            limit: Maximum recommendations to return (default 5)
            topic_filter: Optional topic type to filter by (e.g., 'territorial')

        Returns:
            Dict with recommendations and metadata:
            {
                'recommendations': [...],
                'patterns_used': {...},
                'excluded_count': int,
                'analyzed_at': str
            }

            On error: {'error': msg}
        """
        # Load winning patterns
        if PATTERNS_AVAILABLE:
            try:
                patterns = extract_winning_patterns()
            except Exception as e:
                patterns = {'error': str(e)}
        else:
            patterns = {'error': 'Pattern extractor not available'}

        patterns_used = None
        if 'error' not in patterns:
            patterns_used = {
                'dominant_topic': patterns.get('top_converter_profile', {}).get('dominant_topic'),
                'dominant_angles': patterns.get('top_converter_profile', {}).get('dominant_angles', []),
                'channel_strengths': patterns.get('channel_strengths', {})
            }

        # Get all ANALYZED keywords
        keywords = self.db.get_keywords_by_lifecycle('ANALYZED', limit=500)

        if not keywords:
            return {
                'error': 'No ANALYZED keywords found. Run orchestrator.py to analyze topics first.',
                'help': 'python orchestrator.py "your topic" to add and analyze a topic'
            }

        # Get existing topics
        existing_topics = get_existing_topics()
        excluded_count = 0

        # Score each keyword
        scored = []
        for kw in keywords:
            keyword = kw.get('keyword', '')

            # Skip if matches existing topic
            if topic_matches_existing(keyword, existing_topics):
                excluded_count += 1
                continue

            # Get opportunity score and category
            opportunity_score = kw.get('opportunity_score_final') or 0
            opportunity_category = kw.get('opportunity_category') or 'Unknown'

            # Skip blocked topics
            if kw.get('is_production_blocked'):
                excluded_count += 1
                continue

            # Get topic classification from production constraints if available
            topic_type = None
            angles = []

            constraints_json = kw.get('production_constraints')
            if constraints_json:
                try:
                    constraints = json.loads(constraints_json) if isinstance(constraints_json, str) else constraints_json
                    topic_type = constraints.get('topic_type')
                    angles = constraints.get('angles', [])
                except (json.JSONDecodeError, TypeError):
                    pass

            # Calculate pattern multiplier
            pattern_multiplier, reasons = calculate_pattern_multiplier(
                keyword, topic_type, angles, patterns
            )

            # Calculate final score (capped at 100)
            final_score = min(100, opportunity_score * pattern_multiplier)

            # Apply topic filter if specified
            if topic_filter and topic_type:
                if topic_type.lower() != topic_filter.lower():
                    continue
            elif topic_filter:
                # Skip if no topic_type and filter is specified
                continue

            scored.append({
                'keyword': keyword,
                'keyword_id': kw.get('id'),
                'opportunity_score': opportunity_score,
                'opportunity_category': opportunity_category,
                'topic_type': topic_type,
                'angles': angles,
                'pattern_multiplier': pattern_multiplier,
                'final_score': final_score,
                'reasons': reasons,
                'action': f'python orchestrator.py "{keyword}" --report'
            })

        # Sort by final_score descending
        scored.sort(key=lambda x: x['final_score'], reverse=True)

        # Add rank and limit
        recommendations = []
        for i, item in enumerate(scored[:limit], 1):
            item['rank'] = i
            recommendations.append(item)

        return {
            'recommendations': recommendations,
            'patterns_used': patterns_used,
            'excluded_count': excluded_count,
            'total_analyzed': len(keywords),
            'analyzed_at': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
        }

    def format_recommendation(self, rec: Dict[str, Any]) -> str:
        """
        Format a single recommendation as markdown.

        Args:
            rec: Recommendation dict from recommend()

        Returns:
            Formatted markdown string
        """
        lines = [
            f"### {rec['rank']}. {rec['keyword']}",
            "",
            f"**Final Score:** {rec['final_score']:.1f}/100",
            f"**Category:** {rec['opportunity_category']}",
            ""
        ]

        # Add score breakdown
        lines.append("| Metric | Value |")
        lines.append("|--------|-------|")
        lines.append(f"| Opportunity Score | {rec['opportunity_score']:.1f} |")
        lines.append(f"| Pattern Multiplier | {rec['pattern_multiplier']:.2f}x |")

        if rec.get('topic_type'):
            lines.append(f"| Topic Type | {rec['topic_type']} |")
        if rec.get('angles'):
            lines.append(f"| Angles | {', '.join(rec['angles'])} |")

        lines.append("")

        # Add reasons
        if rec.get('reasons'):
            lines.append("**Pattern Match:**")
            for reason in rec['reasons']:
                lines.append(f"- {reason}")
            lines.append("")

        # Add action
        lines.append(f"**Next Step:** `{rec['action']}`")
        lines.append("")

        return '\n'.join(lines)

    def format_report(self, recommendations: List[Dict[str, Any]], metadata: Dict[str, Any]) -> str:
        """
        Format full recommendation report as markdown.

        Args:
            recommendations: List of recommendation dicts
            metadata: Report metadata (patterns_used, excluded_count, etc.)

        Returns:
            Complete markdown report
        """
        lines = [
            "# Topic Recommendations",
            "",
            f"**Generated:** {metadata.get('analyzed_at', 'Unknown')}",
            f"**Keywords Analyzed:** {metadata.get('total_analyzed', 0)}",
            f"**Topics Excluded:** {metadata.get('excluded_count', 0)} (already in production)",
            ""
        ]

        # Patterns used
        patterns = metadata.get('patterns_used')
        if patterns:
            lines.extend([
                "## Winning Patterns Applied",
                "",
                f"- **Dominant Topic:** {patterns.get('dominant_topic', 'N/A')}",
                f"- **Dominant Angles:** {', '.join(patterns.get('dominant_angles', [])) or 'N/A'}",
                ""
            ])

            strengths = patterns.get('channel_strengths', {})
            if strengths:
                lines.append("**Channel Strengths:**")
                for key, value in strengths.items():
                    lines.append(f"- {key}: {value:.0f}/100")
                lines.append("")

        # Summary table
        lines.extend([
            "## Recommendations Summary",
            "",
            "| Rank | Keyword | Score | Category | Multiplier |",
            "|------|---------|-------|----------|------------|"
        ])

        for rec in recommendations:
            lines.append(
                f"| {rec['rank']} | {rec['keyword'][:30]} | "
                f"{rec['final_score']:.1f} | {rec['opportunity_category']} | "
                f"{rec['pattern_multiplier']:.2f}x |"
            )

        lines.append("")

        # Detailed recommendations
        lines.append("## Detailed Recommendations")
        lines.append("")

        for rec in recommendations:
            lines.append(self.format_recommendation(rec))
            lines.append("---")
            lines.append("")

        lines.append("*Report generated by recommender.py (Phase 21)*")

        return '\n'.join(lines)


def main():
    """CLI entry point for topic recommender."""
    parser = argparse.ArgumentParser(
        description='Topic Recommender - Suggest new topics based on winning patterns',
        epilog='''
Examples:
  python recommender.py                  # Default 5 recommendations
  python recommender.py --limit 10       # More recommendations
  python recommender.py --json           # JSON output
  python recommender.py --topic-type territorial  # Filter by topic
        '''
    )

    parser.add_argument(
        '--limit', '-n',
        type=int,
        default=5,
        help='Number of recommendations to show (default: 5)'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output as JSON'
    )
    parser.add_argument(
        '--refresh',
        action='store_true',
        help='Force refresh winning patterns (not implemented yet)'
    )
    parser.add_argument(
        '--topic-type',
        help='Filter by topic type (e.g., territorial, ideological)'
    )
    parser.add_argument(
        '--save',
        help='Save report to file path'
    )

    args = parser.parse_args()

    # Check dependencies
    if not DATABASE_AVAILABLE:
        print("Error: database.py module not available.")
        sys.exit(1)

    # Initialize
    db = KeywordDB()
    recommender = TopicRecommender(db)

    # Get recommendations
    result = recommender.recommend(
        limit=args.limit,
        topic_filter=args.topic_type
    )

    if 'error' in result:
        print(f"Error: {result['error']}")
        if result.get('help'):
            print(f"Help: {result['help']}")
        sys.exit(1)

    # Output format
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        # Generate markdown report
        report = recommender.format_report(
            result['recommendations'],
            {
                'patterns_used': result.get('patterns_used'),
                'excluded_count': result.get('excluded_count'),
                'total_analyzed': result.get('total_analyzed'),
                'analyzed_at': result.get('analyzed_at')
            }
        )

        if args.save:
            Path(args.save).write_text(report, encoding='utf-8')
            print(f"Report saved to: {args.save}")
        else:
            # Print summary to console
            print("\n" + "=" * 60)
            print("  TOPIC RECOMMENDATIONS")
            print("=" * 60)
            print(f"\nAnalyzed: {result['total_analyzed']} keywords")
            print(f"Excluded: {result['excluded_count']} (already in production)")
            print()

            if result.get('patterns_used'):
                patterns = result['patterns_used']
                print("Winning Pattern Match:")
                print(f"  Dominant topic: {patterns.get('dominant_topic', 'N/A')}")
                print(f"  Top angles: {', '.join(patterns.get('dominant_angles', [])) or 'N/A'}")
                print()

            print("-" * 60)
            print(f"{'Rank':>4} | {'Score':>5} | {'Mult':>5} | Keyword")
            print("-" * 60)

            for rec in result['recommendations']:
                print(
                    f"{rec['rank']:>4} | "
                    f"{rec['final_score']:>5.1f} | "
                    f"{rec['pattern_multiplier']:>5.2f} | "
                    f"{rec['keyword'][:40]}"
                )

            print("-" * 60)
            print()

            # Show top recommendation details
            if result['recommendations']:
                top = result['recommendations'][0]
                print(f"TOP RECOMMENDATION: {top['keyword']}")
                print(f"  Score: {top['final_score']:.1f}/100 ({top['opportunity_category']})")
                print(f"  Pattern Match: {', '.join(top['reasons'])}")
                print(f"\n  Next: {top['action']}")

            print()

    db.close()


if __name__ == '__main__':
    main()
