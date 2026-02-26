"""
YouTube Channel Averages Calculator

Calculates channel-wide benchmark averages from recent videos for
performance comparison ("this video vs channel average").

Usage:
    CLI:
        python channel_averages.py
        python channel_averages.py --compare VIDEO_ID
        python channel_averages.py --last-n 5

    Python:
        from channel_averages import get_channel_averages, compare_to_channel

        averages = get_channel_averages(last_n_videos=10)
        comparison = compare_to_channel(video_metrics, averages)

Returns:
    Channel averages dict:
        {
            "sample_size": int,
            "avg_views": float,
            "avg_watch_time_minutes": float,
            "avg_likes": float,
            "avg_comments": float,
            "avg_subscribers_gained": float,
            "video_ids_sampled": [...],
            "fetched_at": "ISO timestamp"
        }

Dependencies:
    - auth.py (Phase 7) for OAuth2 authentication
    - metrics.py (Phase 8) for video metrics fetching
"""

import sys
import json
from datetime import datetime, timezone

from tools.youtube_analytics.auth import get_authenticated_service
from tools.youtube_analytics.metrics import get_video_metrics

try:
    from googleapiclient.errors import HttpError
except ImportError:
    HttpError = Exception


def get_recent_video_ids(max_videos: int = 10) -> list[str] | dict:
    """
    Get video IDs of recent uploads from the authenticated channel.

    Uses YouTube Data API v3 search.list() with forMine=True.

    Args:
        max_videos: Maximum number of video IDs to return (default 10)

    Returns:
        list of video ID strings on success
        dict with error on failure
    """
    try:
        youtube = get_authenticated_service('youtube', 'v3')

        response = youtube.search().list(
            part='id',
            forMine=True,
            type='video',
            order='date',  # Most recent first
            maxResults=max_videos
        ).execute()

        video_ids = [
            item['id']['videoId']
            for item in response.get('items', [])
            if item['id'].get('videoId')
        ]

        return video_ids

    except HttpError as e:
        status_code = e.resp.status if hasattr(e, 'resp') else None
        return {
            'error': f'API error (HTTP {status_code})',
            'details': str(e)
        }

    except Exception as e:
        return {
            'error': f'Unexpected error: {type(e).__name__}',
            'details': str(e)
        }


def get_channel_averages(last_n_videos: int = 10) -> dict:
    """
    Calculate channel-wide benchmark averages from recent videos.

    Fetches metrics for the last N videos and calculates averages.
    Requires minimum 3 videos for meaningful averages.

    Args:
        last_n_videos: Number of recent videos to sample (default 10)

    Returns:
        dict with averages on success:
            {
                "sample_size": int,
                "avg_views": float,
                "avg_watch_time_minutes": float,
                "avg_likes": float,
                "avg_comments": float,
                "avg_shares": float,
                "avg_subscribers_gained": float,
                "avg_subscribers_lost": float,
                "avg_view_duration_seconds": float,
                "video_ids_sampled": [...],
                "fetched_at": "ISO timestamp"
            }

        dict with error on failure:
            {"error": "..."}
    """
    # Get recent video IDs
    video_ids = get_recent_video_ids(last_n_videos)

    if isinstance(video_ids, dict) and 'error' in video_ids:
        return video_ids

    if not video_ids:
        return {
            'error': 'No videos found for channel',
            'note': 'Channel may be new or have no public videos'
        }

    # Fetch metrics for each video
    metrics_list = []
    failed_videos = []

    for vid in video_ids:
        result = get_video_metrics(vid)
        if 'error' not in result:
            metrics_list.append(result)
        else:
            failed_videos.append(vid)

    # Require minimum 3 videos for meaningful averages
    if len(metrics_list) < 3:
        return {
            'error': 'Insufficient data for meaningful averages',
            'videos_found': len(video_ids),
            'videos_with_data': len(metrics_list),
            'minimum_required': 3,
            'note': 'Need at least 3 videos with analytics data'
        }

    # Calculate averages
    n = len(metrics_list)

    averages = {
        'sample_size': n,
        'avg_views': sum(m['views'] for m in metrics_list) / n,
        'avg_watch_time_minutes': sum(m['watch_time_minutes'] for m in metrics_list) / n,
        'avg_likes': sum(m['likes'] for m in metrics_list) / n,
        'avg_comments': sum(m['comments'] for m in metrics_list) / n,
        'avg_shares': sum(m['shares'] for m in metrics_list) / n,
        'avg_subscribers_gained': sum(m['subscribers_gained'] for m in metrics_list) / n,
        'avg_subscribers_lost': sum(m['subscribers_lost'] for m in metrics_list) / n,
        'avg_view_duration_seconds': sum(m['avg_view_duration_seconds'] for m in metrics_list) / n,
        'video_ids_sampled': [m['video_id'] for m in metrics_list],
        'fetched_at': datetime.now(timezone.utc).isoformat() + 'Z'
    }

    # Add note about failed videos if any
    if failed_videos:
        averages['note'] = f'{len(failed_videos)} video(s) excluded due to missing data'
        averages['excluded_video_ids'] = failed_videos

    return averages


def compare_to_channel(video_metrics: dict, channel_averages: dict) -> dict:
    """
    Compare a single video's metrics to channel averages.

    Calculates whether each metric is above, below, or at the channel average,
    along with the percentage difference.

    Args:
        video_metrics: dict from get_video_metrics()
        channel_averages: dict from get_channel_averages()

    Returns:
        dict with comparison for each metric:
            {
                "video_id": "...",
                "video_title": "...",
                "comparisons": {
                    "views": {
                        "value": 1500,
                        "average": 1000.0,
                        "vs_average": "above",
                        "delta_percent": 50.0
                    },
                    "watch_time_minutes": {...},
                    ...
                },
                "summary": {
                    "above_average": ["views", "likes"],
                    "below_average": ["watch_time_minutes"],
                    "at_average": []
                }
            }

        dict with error if inputs are invalid
    """
    # Validate inputs
    if 'error' in video_metrics:
        return {
            'error': 'Video metrics contain error',
            'video_error': video_metrics['error']
        }

    if 'error' in channel_averages:
        return {
            'error': 'Channel averages contain error',
            'averages_error': channel_averages['error']
        }

    # Mapping of video metric keys to channel average keys
    metric_mapping = {
        'views': 'avg_views',
        'watch_time_minutes': 'avg_watch_time_minutes',
        'likes': 'avg_likes',
        'comments': 'avg_comments',
        'shares': 'avg_shares',
        'subscribers_gained': 'avg_subscribers_gained',
        'avg_view_duration_seconds': 'avg_view_duration_seconds'
    }

    comparisons = {}
    summary = {
        'above_average': [],
        'below_average': [],
        'at_average': []
    }

    for video_key, avg_key in metric_mapping.items():
        video_value = video_metrics.get(video_key, 0)
        avg_value = channel_averages.get(avg_key, 0)

        # Calculate delta percentage
        if avg_value > 0:
            delta_percent = ((video_value - avg_value) / avg_value) * 100
        else:
            delta_percent = 0.0 if video_value == 0 else 100.0

        # Determine if above, below, or at average (within 5% = at average)
        if abs(delta_percent) <= 5:
            vs_average = 'at_average'
            summary['at_average'].append(video_key)
        elif delta_percent > 0:
            vs_average = 'above'
            summary['above_average'].append(video_key)
        else:
            vs_average = 'below'
            summary['below_average'].append(video_key)

        comparisons[video_key] = {
            'value': video_value,
            'average': round(avg_value, 1),
            'vs_average': vs_average,
            'delta_percent': round(delta_percent, 1)
        }

    return {
        'video_id': video_metrics.get('video_id'),
        'video_title': video_metrics.get('title'),
        'comparisons': comparisons,
        'summary': summary,
        'sample_size': channel_averages.get('sample_size'),
        'compared_at': datetime.now(timezone.utc).isoformat() + 'Z'
    }


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description="Calculate channel benchmark averages from recent videos.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  python -m tools.youtube_analytics.channel_averages
  python -m tools.youtube_analytics.channel_averages --compare wCFReiCGiks
  python -m tools.youtube_analytics.channel_averages --last-n 5 --compare wCFReiCGiks""",
    )
    parser.add_argument(
        "--compare", metavar="VIDEO_ID",
        help="Compare a video to channel averages",
    )
    parser.add_argument(
        "--last-n", type=int, default=10, metavar="N",
        help="Use last N videos for averages (default: 10)",
    )

    verbosity = parser.add_mutually_exclusive_group()
    verbosity.add_argument("--verbose", "-v", action="store_true", help="Show debug output on stderr")
    verbosity.add_argument("--quiet", "-q", action="store_true", help="Only show errors on stderr")

    args = parser.parse_args()

    from tools.logging_config import setup_logging
    setup_logging(args.verbose, args.quiet)

    averages = get_channel_averages(args.last_n)

    if 'error' in averages:
        print(json.dumps(averages, indent=2))
        sys.exit(1)

    if args.compare:
        video_metrics = get_video_metrics(args.compare)

        if 'error' in video_metrics:
            print(json.dumps(video_metrics, indent=2))
            sys.exit(1)

        comparison = compare_to_channel(video_metrics, averages)
        print(json.dumps(comparison, indent=2))
    else:
        print(json.dumps(averages, indent=2))
