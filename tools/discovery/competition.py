"""
Competition Analysis Module

Counts videos and channels for keywords using scrapetube (quota-free).
YouTube Data API search costs 100 quota units - use sparingly.

Usage:
    from competition import get_competition_count, CompetitionAnalyzer

    result = get_competition_count("dark ages myth")
    # {'video_count': 47, 'unique_channels': 23, 'method': 'scrape'}

Per RESEARCH.md:
- scrapetube for video counts (no quota)
- Sample first 100 videos (full iteration too slow for 10K+)
- Cache results for 7 days

Installation:
    pip install scrapetube
"""

from datetime import datetime
from typing import Dict, Any, List, Optional
from collections import Counter

# Check for scrapetube availability
try:
    import scrapetube
    SCRAPETUBE_AVAILABLE = True
except ImportError:
    SCRAPETUBE_AVAILABLE = False


class CompetitionAnalyzer:
    """
    Analyze competition for keywords using YouTube search results.

    Prefers scrapetube (quota-free) over YouTube Data API (100 quota per search).
    Samples first N videos to avoid slow full iteration.
    """

    def __init__(self, sample_size: int = 100):
        """
        Initialize analyzer.

        Args:
            sample_size: Max videos to count (default 100, per RESEARCH.md pitfall 5)
        """
        self.sample_size = sample_size

    def count_videos(self, keyword: str) -> Dict[str, Any]:
        """
        Count videos for keyword search.

        Args:
            keyword: Search query

        Returns:
            {
                'video_count': int,
                'unique_channels': int,
                'sampled': bool,  # True if count is sample (not full)
                'sample_size': int,
                'videos': List[Dict]  # First N video metadata
            }
            or {'error': msg}
        """
        if not SCRAPETUBE_AVAILABLE:
            return {
                'error': 'scrapetube not installed',
                'details': 'Install with: pip install scrapetube'
            }

        try:
            videos = scrapetube.get_search(keyword)

            results = []
            channel_ids = []
            count = 0

            for video in videos:
                count += 1

                # Extract relevant metadata
                video_data = {
                    'video_id': video.get('videoId'),
                    'title': video.get('title', {}).get('runs', [{}])[0].get('text', ''),
                    'channel_id': video.get('ownerText', {}).get('runs', [{}])[0].get('navigationEndpoint', {}).get('browseEndpoint', {}).get('browseId'),
                    'channel_name': video.get('ownerText', {}).get('runs', [{}])[0].get('text', ''),
                    'view_count': self._parse_view_count(video.get('viewCountText', {}).get('simpleText', '0')),
                    'published_text': video.get('publishedTimeText', {}).get('simpleText', '')
                }

                results.append(video_data)
                if video_data['channel_id']:
                    channel_ids.append(video_data['channel_id'])

                # Stop at sample size
                if count >= self.sample_size:
                    break

            unique_channels = len(set(channel_ids))
            sampled = count >= self.sample_size

            return {
                'video_count': count if not sampled else f'{count}+',
                'video_count_raw': count,
                'unique_channels': unique_channels,
                'sampled': sampled,
                'sample_size': self.sample_size,
                'videos': results,
                'fetched_at': datetime.utcnow().isoformat() + 'Z'
            }

        except Exception as e:
            return {
                'error': f'Competition analysis failed: {type(e).__name__}',
                'details': str(e)
            }

    def _parse_view_count(self, view_text: str) -> int:
        """Parse view count text like '1.2M views' to integer."""
        try:
            # Remove 'views' suffix and clean
            text = view_text.lower().replace('views', '').replace('view', '').strip()

            if not text or text == 'no':
                return 0

            multipliers = {'k': 1000, 'm': 1000000, 'b': 1000000000}

            for suffix, mult in multipliers.items():
                if suffix in text:
                    num = float(text.replace(suffix, '').strip())
                    return int(num * mult)

            # Plain number
            return int(text.replace(',', ''))
        except (ValueError, AttributeError):
            return 0

    def get_top_channels(self, keyword: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get top channels covering a keyword.

        Returns list of channels sorted by total views on matching videos.
        """
        result = self.count_videos(keyword)

        if 'error' in result:
            return []

        # Aggregate by channel
        channel_stats = {}
        for video in result.get('videos', []):
            ch_id = video.get('channel_id')
            if not ch_id:
                continue

            if ch_id not in channel_stats:
                channel_stats[ch_id] = {
                    'channel_id': ch_id,
                    'channel_name': video.get('channel_name', ''),
                    'video_count': 0,
                    'total_views': 0
                }

            channel_stats[ch_id]['video_count'] += 1
            channel_stats[ch_id]['total_views'] += video.get('view_count', 0)

        # Sort by total views
        sorted_channels = sorted(
            channel_stats.values(),
            key=lambda x: x['total_views'],
            reverse=True
        )

        return sorted_channels[:limit]


def get_competition_count(keyword: str, sample_size: int = 100) -> Dict[str, Any]:
    """
    Convenience function to count competition for a keyword.

    Args:
        keyword: Search query
        sample_size: Max videos to count

    Returns:
        Competition count data or error dict
    """
    analyzer = CompetitionAnalyzer(sample_size)
    return analyzer.count_videos(keyword)
