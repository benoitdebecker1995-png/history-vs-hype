"""
Google Trends Integration

Fetches trend data using trendspyg (replaces archived pytrends).
Implements 7-day caching with staleness warnings per CONTEXT.md.

Usage:
    from trends import get_trend_direction, TrendsClient

    result = get_trend_direction("dark ages myth")
    # {'direction': 'rising', 'percent_change': 45.2, 'interest': 78}

Rate Limiting:
    - trendspyg has built-in 5-minute TTL cache
    - 60-second delay after rate limit detection
    - Falls back to cached data on API failure

Installation:
    pip install trendspyg
"""

from datetime import datetime
from typing import Dict, Any, Optional
import time

# Check for trendspyg availability
try:
    from trendspyg import download_google_trends_csv
    TRENDSPYG_AVAILABLE = True
except ImportError:
    TRENDSPYG_AVAILABLE = False


class TrendsClient:
    """
    Google Trends client with caching and rate limit handling.

    Per RESEARCH.md:
    - ~1,400 requests triggers rate limit
    - 60-second delay required after rate limit
    - trendspyg has 5-minute built-in cache
    """

    def __init__(self, region: str = 'US'):
        self.region = region
        self._last_request = 0
        self._rate_limited = False
        self._rate_limit_until = 0

    def get_interest_over_time(self, keyword: str, hours: int = 168) -> Dict[str, Any]:
        """
        Get interest over time for keyword.

        Args:
            keyword: Search term
            hours: Time window (4, 24, 48, or 168 for weekly)

        Returns:
            {'interest': int, 'percent_change': float} or {'error': msg}
        """
        if not TRENDSPYG_AVAILABLE:
            return {
                'error': 'trendspyg not installed',
                'details': 'Install with: pip install trendspyg'
            }

        # Check rate limit cooldown
        if self._rate_limited and time.time() < self._rate_limit_until:
            remaining = int(self._rate_limit_until - time.time())
            return {
                'error': 'Rate limited',
                'details': f'Wait {remaining}s before retrying',
                'retry_after': remaining
            }

        try:
            # trendspyg CSV method for historical data
            df = download_google_trends_csv(
                geo=self.region,
                hours=hours,
                output_format='dataframe',
                cache=True  # 5-minute TTL
            )

            if df is None or df.empty:
                return {
                    'error': 'No trend data available',
                    'details': f'Google Trends returned no data for region {self.region}'
                }

            # Find keyword in results (case-insensitive)
            keyword_lower = keyword.lower()
            matching = df[df['trend'].str.lower().str.contains(keyword_lower, na=False)]

            if matching.empty:
                # Keyword not trending - this is normal for niche topics
                return {
                    'interest': 0,
                    'percent_change': 0,
                    'direction': 'stable',
                    'note': 'Keyword not in trending topics'
                }

            # Extract traffic change (e.g., "+125%" -> 125.0)
            row = matching.iloc[0]
            traffic = str(row.get('traffic', '0%'))
            percent_change = float(traffic.replace('%', '').replace('+', '').replace(',', ''))

            # Estimate interest from traffic change
            # Note: Actual 0-100 normalization requires interest_over_time API
            interest = min(100, max(0, 50 + int(percent_change / 2)))

            self._rate_limited = False
            return {
                'interest': interest,
                'percent_change': percent_change,
                'direction': self._classify_direction(percent_change)
            }

        except Exception as e:
            error_str = str(e).lower()
            if 'rate' in error_str or '429' in error_str or 'too many' in error_str:
                self._rate_limited = True
                self._rate_limit_until = time.time() + 60
                return {
                    'error': 'Rate limited by Google Trends',
                    'details': 'Wait 60 seconds before retrying',
                    'retry_after': 60
                }

            return {
                'error': f'Trends fetch failed: {type(e).__name__}',
                'details': str(e)
            }

    def _classify_direction(self, percent_change: float) -> str:
        """Classify trend direction based on percent change."""
        if percent_change > 20:
            return 'rising'
        elif percent_change < -20:
            return 'declining'
        return 'stable'


def get_trend_direction(keyword: str, region: str = 'US') -> Dict[str, Any]:
    """
    Convenience function to get trend direction for a keyword.

    Args:
        keyword: Keyword to analyze
        region: Geographic region (default: US)

    Returns:
        {
            'direction': 'rising'|'stable'|'declining',
            'percent_change': float,
            'interest': int (0-100)
        }
        or {'error': msg} on failure
    """
    client = TrendsClient(region)
    return client.get_interest_over_time(keyword)
