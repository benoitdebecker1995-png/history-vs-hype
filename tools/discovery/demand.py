"""
Demand Analysis Module

Aggregates demand signals from multiple sources:
- Autocomplete position (search volume proxy)
- Google Trends (trend direction)
- Related query expansion
- Competition ratio scoring

Usage:
    CLI:
        python demand.py "dark ages myth"
        python demand.py --keywords "dark ages, crusades" --refresh
        python demand.py "topic" --json
        python demand.py "topic" -v

    Python:
        from demand import DemandAnalyzer
        from database import KeywordDB

        db = KeywordDB()
        analyzer = DemandAnalyzer(db)
        result = analyzer.analyze_keyword("dark ages myth")

Returns aggregated demand data with staleness warnings per CONTEXT.md decisions.
"""

from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
import asyncio

from .database import KeywordDB
from .trends import get_trend_direction, TRENDSPYG_AVAILABLE
from .competition import get_competition_count, SCRAPETUBE_AVAILABLE
from .autocomplete import get_autocomplete_suggestions


class DemandAnalyzer:
    """
    Aggregate demand signals for keyword opportunity analysis.

    Implements caching with 7-day freshness (per CONTEXT.md):
    - Warning when data >7 days old
    - Fallback to stale cache on API failure
    - --refresh flag support via force_refresh parameter
    """

    def __init__(self, db: KeywordDB, cache_days: int = 7):
        """
        Initialize DemandAnalyzer.

        Args:
            db: KeywordDB instance for caching
            cache_days: Default cache duration in days (default 7)
        """
        self.db = db
        self.cache_days = cache_days

    def analyze_keyword(self, keyword: str, force_refresh: bool = False) -> Dict[str, Any]:
        """
        Analyze demand for a keyword, aggregating all signals.

        Workflow:
        1. Check database cache (unless force_refresh)
        2. If stale/missing, fetch fresh data from each source
        3. Calculate opportunity ratio
        4. Cache results
        5. Return with staleness warnings

        Args:
            keyword: Keyword to analyze
            force_refresh: Ignore cache (--refresh flag)

        Returns:
            {
                'keyword': str,
                'search_volume_proxy': int,  # autocomplete position score 0-100
                'trend_direction': str,  # 'up +45%', '-> 0%', 'v -20%'
                'related_queries': List[str],  # 10-20 related
                'competition': {'video_count': int, 'channel_count': int},
                'opportunity_ratio': str,  # '4.2x (High Opportunity)'
                'opportunity_category': str,  # 'High', 'Medium', 'Low'
                'data_age_days': int,
                'warnings': List[str]
            }
        """
        warnings = []
        max_age = 0 if force_refresh else self.cache_days

        # Ensure keyword exists in database
        keyword_result = self.db.add_keyword(keyword, source='demand_analysis')
        if 'error' in keyword_result:
            return keyword_result
        keyword_id = keyword_result['keyword_id']

        # 1. Get autocomplete suggestions (for position score + related queries)
        try:
            autocomplete_result = asyncio.run(get_autocomplete_suggestions(keyword, max_suggestions=20))
        except RuntimeError:
            # Event loop already running (e.g., in Jupyter)
            loop = asyncio.get_event_loop()
            autocomplete_result = loop.run_until_complete(get_autocomplete_suggestions(keyword, max_suggestions=20))

        if 'error' in autocomplete_result:
            warnings.append(f"Autocomplete: {autocomplete_result['error']}")
            suggestions = []
            position_score = 0
        else:
            suggestions = autocomplete_result.get('suggestions', [])
            position_score = self.calculate_position_score(keyword, suggestions)

        # 2. Get trend direction
        trend_data = self.db.get_cached_trend(keyword_id, max_age_days=max_age)

        if trend_data is None:
            # Fetch fresh trend data
            fresh_trend = get_trend_direction(keyword)

            if 'error' in fresh_trend:
                warnings.append(f"Trends: {fresh_trend['error']}")
                trend_direction = '\u2192 0%'
                percent_change = 0
            else:
                percent_change = fresh_trend.get('percent_change', 0)
                trend_direction = self.format_trend_direction(percent_change)

                # Cache it
                self.db.add_trend(
                    keyword_id=keyword_id,
                    interest=fresh_trend.get('interest', 0),
                    trend_direction=fresh_trend.get('direction', 'stable'),
                    percent_change=percent_change
                )
            data_age_trend = 0
        else:
            trend_direction = self.format_trend_direction(trend_data.get('percent_change', 0))
            percent_change = trend_data.get('percent_change', 0)
            data_age_trend = trend_data.get('data_age_days', 0)

            if data_age_trend > self.cache_days:
                warnings.append(f"Trend data is {data_age_trend} days old")

        # 3. Get competition count
        competition_data = self.db.get_competition_count(keyword_id, max_age_days=max_age)

        if competition_data is None:
            # Fetch fresh competition data
            fresh_comp = get_competition_count(keyword)

            if 'error' in fresh_comp:
                warnings.append(f"Competition: {fresh_comp['error']}")
                video_count = 0
                channel_count = 0
            else:
                video_count = fresh_comp.get('video_count_raw', 0)
                channel_count = fresh_comp.get('unique_channels', 0)

                # Cache competition videos
                for video in fresh_comp.get('videos', [])[:20]:  # Store top 20
                    if video.get('video_id'):
                        self.db.add_competitor_video(
                            video_id=video['video_id'],
                            channel_id=0,  # Channel lookup deferred to Phase 16
                            keyword_id=keyword_id,
                            title=video.get('title', ''),
                            view_count=video.get('view_count', 0),
                            published_at=None
                        )
            data_age_comp = 0
        else:
            video_count = competition_data.get('video_count', 0)
            channel_count = competition_data.get('channel_count', 0)
            data_age_comp = competition_data.get('data_age_days', 0)

            if data_age_comp > self.cache_days:
                warnings.append(f"Competition data is {data_age_comp} days old")

        # 4. Calculate opportunity ratio
        opportunity = self.calculate_opportunity_ratio(position_score, video_count)

        # Cache opportunity score
        self.db.add_opportunity_score(
            keyword_id=keyword_id,
            demand_score=position_score,
            competition_score=video_count,
            opportunity_ratio=opportunity['ratio'] if opportunity['ratio'] != float('inf') else 999,
            category=opportunity['category']
        )

        # 5. Return aggregated result
        return {
            'keyword': keyword,
            'search_volume_proxy': position_score,
            'trend_direction': trend_direction,
            'related_queries': suggestions[:15],  # Top 15 related
            'competition': {
                'video_count': video_count,
                'channel_count': channel_count
            },
            'opportunity_ratio': opportunity['display'],
            'opportunity_category': opportunity['category'],
            'data_age_days': max(data_age_trend, data_age_comp),
            'warnings': warnings if warnings else None,
            'fetched_at': datetime.now(timezone.utc).isoformat() + 'Z'
        }

    def calculate_position_score(self, keyword: str, suggestions: List[str]) -> int:
        """
        Calculate search volume proxy from autocomplete position.

        Position 1 = 100 (highest demand)
        Position 10 = 10 (lowest demand)
        Not found = 0

        Based on SEO research: 23% of users select from autocomplete.

        Args:
            keyword: Keyword to find in suggestions
            suggestions: List of autocomplete suggestions

        Returns:
            Score 0-100 based on position (100 = position 1, 0 = not found)
        """
        try:
            # Case-insensitive match
            lower_suggestions = [s.lower() for s in suggestions]
            position = lower_suggestions.index(keyword.lower()) + 1
            score = max(0, 100 - (position - 1) * 10)
            return score
        except ValueError:
            return 0

    def calculate_opportunity_ratio(self, demand_score: float, competition_count: int) -> Dict[str, Any]:
        """
        Calculate demand/competition ratio with conservative thresholds.

        From CONTEXT.md:
        - High: >4x (only obvious wins given high research overhead)
        - Medium: 2-4x
        - Low: <2x

        Args:
            demand_score: Demand score (0-100 from position scoring)
            competition_count: Number of competing videos

        Returns:
            {
                'ratio': float,
                'display': str,  # '4.2x (High Opportunity)'
                'category': str  # 'High', 'Medium', 'Low'
            }
        """
        if competition_count == 0:
            return {
                'ratio': float('inf'),
                'display': 'Inf (No Competition)',
                'category': 'High'
            }

        ratio = demand_score / max(competition_count, 1)

        if ratio >= 4.0:
            category = 'High'
        elif ratio >= 2.0:
            category = 'Medium'
        else:
            category = 'Low'

        return {
            'ratio': ratio,
            'display': f'{ratio:.1f}x ({category} Opportunity)',
            'category': category
        }

    def format_trend_direction(self, percent_change: float) -> str:
        """
        Format trend direction with arrow and percentage.

        From CONTEXT.md: Arrow + percentage (^ +45% or v -20%)

        Args:
            percent_change: Percentage change (+45.2 or -20.1)

        Returns:
            Formatted string with arrow and percentage
        """
        if percent_change > 20:
            return f'\u2191 +{percent_change:.0f}%'
        elif percent_change < -20:
            return f'\u2193 {percent_change:.0f}%'
        else:
            return f'\u2192 {percent_change:+.0f}%'


def analyze_demand(keyword: str, force_refresh: bool = False, db_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Convenience function for demand analysis.

    Args:
        keyword: Keyword to analyze
        force_refresh: Ignore cache and fetch fresh data
        db_path: Optional database path

    Returns:
        Demand analysis result or error dict
    """
    db = KeywordDB(db_path)
    analyzer = DemandAnalyzer(db)
    result = analyzer.analyze_keyword(keyword, force_refresh)
    db.close()
    return result


def main():
    """CLI entry point for demand analysis."""
    import argparse
    import json
    import sys

    parser = argparse.ArgumentParser(
        description='Analyze keyword demand with opportunity scoring',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python demand.py "dark ages myth"
  python demand.py --keywords "dark ages, crusades, colonialism"
  python demand.py --file topics.txt
  python demand.py "topic" --refresh
  python demand.py "topic" --json
  python demand.py "topic" -v

Requirements:
  pip install pyppeteer pyppeteer-stealth  # autocomplete
  pip install trendspyg                     # Google Trends
  pip install scrapetube                    # competition analysis
        """
    )
    parser.add_argument('keyword', nargs='?', help='Keyword to analyze')
    parser.add_argument('--keywords', help='Comma-separated keywords for batch')
    parser.add_argument('--file', help='File with keywords (one per line)')
    parser.add_argument('--refresh', action='store_true', help='Force refresh (ignore cache)')
    parser.add_argument('--json', action='store_true', help='JSON output')

    verbosity = parser.add_mutually_exclusive_group()
    verbosity.add_argument('-v', '--verbose', action='store_true',
                           help='Show debug output on stderr and verbose result details')
    verbosity.add_argument('--quiet', '-q', action='store_true',
                           help='Only show errors on stderr')

    args = parser.parse_args()

    from tools.logging_config import setup_logging
    setup_logging(args.verbose, args.quiet)

    # Collect keywords
    keywords = []
    if args.keyword:
        keywords.append(args.keyword)
    if args.keywords:
        keywords.extend([k.strip() for k in args.keywords.split(',') if k.strip()])
    if args.file:
        from pathlib import Path
        path = Path(args.file)
        if path.exists():
            keywords.extend([l.strip() for l in path.read_text().splitlines() if l.strip()])

    if not keywords:
        parser.print_help()
        sys.exit(1)

    # Analyze
    db = KeywordDB()
    analyzer = DemandAnalyzer(db)
    results = []

    for kw in keywords:
        result = analyzer.analyze_keyword(kw, force_refresh=args.refresh)
        results.append(result)

    db.close()

    # Output
    if args.json:
        print(json.dumps(results if len(results) > 1 else results[0], indent=2, default=str))
    else:
        # Table output (default per CONTEXT.md)
        for r in results:
            if 'error' in r:
                print(f"\n## {r.get('keyword', 'Unknown')}")
                print(f"**Error:** {r['error']}")
                continue

            print(f"\n## {r['keyword']}")
            print(f"\n| Metric | Value |")
            print(f"|--------|-------|")
            print(f"| Search Volume Proxy | {r['search_volume_proxy']} |")
            print(f"| Trend | {r['trend_direction']} |")
            print(f"| Competition | {r['competition']['video_count']} videos / {r['competition']['channel_count']} channels |")
            print(f"| **Opportunity** | **{r['opportunity_ratio']}** |")

            if r.get('warnings'):
                print(f"\n**Warnings:** {', '.join(r['warnings'])}")

            if args.verbose and r.get('related_queries'):
                print(f"\n### Related Queries")
                for i, q in enumerate(r['related_queries'][:10], 1):
                    print(f"{i}. {q}")


if __name__ == '__main__':
    main()
