"""
Demand Analysis Module

Aggregates demand signals from multiple sources:
- Autocomplete position (search volume proxy)
- Google Trends (trend direction)
- Related query expansion
- Competition ratio scoring

Usage:
    from demand import DemandAnalyzer
    from database import KeywordDB

    db = KeywordDB()
    analyzer = DemandAnalyzer(db)
    result = analyzer.analyze_keyword("dark ages myth")

Returns aggregated demand data with staleness warnings per CONTEXT.md decisions.
"""

from datetime import datetime
from typing import Dict, Any, List, Optional
from database import KeywordDB


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

        Returns:
            {
                'keyword': str,
                'search_volume_proxy': int,  # autocomplete position score 0-100
                'trend_direction': str,  # '^ +45%', '-> 0%', 'v -20%'
                'related_queries': List[str],  # 10-20 related
                'competition_ratio': str,  # '4.2x (High Opportunity)'
                'data_age_days': int,
                'warnings': List[str]
            }
        """
        # Stub implementation - external data sources added in Plan 02
        # This method will aggregate:
        # 1. Autocomplete position -> search_volume_proxy (DEM-01)
        # 2. Google Trends -> trend_direction (DEM-02)
        # 3. Related queries -> expansion candidates (DEM-03)
        # 4. Competition count -> opportunity ratio (DEM-04)
        return {
            'keyword': keyword,
            'search_volume_proxy': 0,
            'trend_direction': '-> 0%',
            'related_queries': [],
            'competition_ratio': 'Not calculated',
            'data_age_days': 0,
            'warnings': ['Stub implementation - external data sources added in Plan 02']
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
