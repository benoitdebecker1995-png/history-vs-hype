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


def filter_quality_competition(
    videos: List[Dict],
    min_views: int = 1000,
    min_percentile: int = 25
) -> List[Dict]:
    """
    Filter to quality competition only.

    Quality signals:
    1. View count > threshold (1K minimum)
    2. View count > Nth percentile of sample
    3. Channel appears multiple times (established creator)

    Args:
        videos: List of video dicts with 'view_count' and 'channel_name'
        min_views: Minimum view count threshold (default 1000)
        min_percentile: Minimum percentile threshold (default 25th)

    Returns:
        Filtered list with quality_signals dict and quality_tier added.

    Example:
        >>> videos = [{'view_count': 100000, 'channel_name': 'Big Channel'}, ...]
        >>> filtered = filter_quality_competition(videos, min_views=1000)
        >>> filtered[0]['quality_tier']
        'high'
    """
    if not videos:
        return []

    # Calculate percentile threshold from sample
    view_counts = [v.get('view_count', 0) for v in videos]
    view_counts.sort()

    percentile_index = int(len(view_counts) * (min_percentile / 100.0))
    percentile_threshold = view_counts[percentile_index] if percentile_index < len(view_counts) else 0

    # Effective threshold is max of min_views and percentile
    effective_threshold = max(min_views, percentile_threshold)

    # Count channel occurrences for established creator detection
    channel_counts = Counter(v.get('channel_name', '') for v in videos if v.get('channel_name'))

    # Calculate quality tiers (75th and 25th percentile)
    p75_index = int(len(view_counts) * 0.75)
    p75_threshold = view_counts[p75_index] if p75_index < len(view_counts) else view_counts[-1]

    filtered = []
    for video in videos:
        view_count = video.get('view_count', 0)
        channel_name = video.get('channel_name', '')

        # Apply quality filter
        if view_count < effective_threshold:
            continue

        # Build quality signals
        is_established = channel_counts.get(channel_name, 0) > 1

        quality_signals = {
            'above_min_views': view_count >= min_views,
            'above_percentile': view_count >= percentile_threshold,
            'established_creator': is_established,
            'view_count': view_count
        }

        # Assign quality tier
        if view_count >= p75_threshold:
            quality_tier = 'high'
        elif view_count >= effective_threshold:
            quality_tier = 'medium'
        else:
            quality_tier = 'low'

        # Add to filtered list with enrichment
        enriched_video = video.copy()
        enriched_video['quality_signals'] = quality_signals
        enriched_video['quality_tier'] = quality_tier
        filtered.append(enriched_video)

    return filtered


def calculate_differentiation_score(
    videos: List[Dict],
    channel_angles: List[str] = None
) -> Dict[str, Any]:
    """
    Calculate differentiation opportunities based on angle frequency.

    Args:
        videos: List of video dicts with 'angles' key (list of angle categories)
        channel_angles: Channel's preferred angles (default: ['legal', 'historical'])

    Returns:
        {
            'angle_distribution': {'political': 45.2, 'legal': 12.1, ...},
            'gap_scores': {'legal': 0.73, 'economic': 0.85, ...},
            'recommended_angle': 'economic',
            'differentiation_score': 0.85,
            'total_videos_analyzed': int
        }

    Example:
        >>> videos = [{'angles': ['political']}, {'angles': ['political', 'historical']}]
        >>> result = calculate_differentiation_score(videos)
        >>> result['gap_scores']['legal']
        1.0  # No legal angle videos = maximum gap
    """
    from tools.discovery.classifiers import ANGLE_KEYWORDS

    if channel_angles is None:
        channel_angles = ['legal', 'historical']  # Channel DNA default

    if not videos:
        # No competition = maximum opportunity
        return {
            'angle_distribution': {},
            'gap_scores': {angle: 1.0 for angle in ANGLE_KEYWORDS.keys()},
            'recommended_angle': channel_angles[0] if channel_angles else 'legal',
            'differentiation_score': 1.0,
            'total_videos_analyzed': 0
        }

    # Count angle occurrences across all videos
    angle_counts = Counter()
    total_angle_instances = 0

    for video in videos:
        angles = video.get('angles', [])
        for angle in angles:
            if angle != 'general':  # Exclude generic classification
                angle_counts[angle] += 1
                total_angle_instances += 1

    # Calculate angle distribution (percentage)
    angle_distribution = {}
    for angle in ANGLE_KEYWORDS.keys():
        count = angle_counts.get(angle, 0)
        percentage = (count / total_angle_instances * 100.0) if total_angle_instances > 0 else 0.0
        angle_distribution[angle] = round(percentage, 1)

    # Calculate gap scores (inverse of frequency, 1.0 = no competition)
    gap_scores = {}
    for angle in ANGLE_KEYWORDS.keys():
        frequency = angle_distribution[angle] / 100.0  # Convert back to 0-1
        gap_scores[angle] = round(1.0 - frequency, 2)

    # Find best angle from channel_angles based on gap score
    best_angle = channel_angles[0] if channel_angles else 'legal'
    best_gap = 0.0

    for angle in channel_angles:
        if angle in gap_scores and gap_scores[angle] > best_gap:
            best_gap = gap_scores[angle]
            best_angle = angle

    return {
        'angle_distribution': angle_distribution,
        'gap_scores': gap_scores,
        'recommended_angle': best_angle,
        'differentiation_score': best_gap,
        'total_videos_analyzed': len(videos)
    }


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
