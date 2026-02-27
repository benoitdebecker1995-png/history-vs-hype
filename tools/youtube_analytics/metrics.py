"""
YouTube Analytics Metrics Fetcher

Fetches core engagement metrics (views, watch time, likes, comments, shares,
subscribers gained/lost) for any video via the YouTube Analytics API.

Usage:
    CLI:
        python metrics.py VIDEO_ID
        python metrics.py VIDEO_ID --start-date 2025-01-01 --end-date 2025-12-31

    Python:
        from metrics import get_video_metrics

        result = get_video_metrics('VIDEO_ID')
        print(result['views'])
        print(result['watch_time_minutes'])

Returns:
    JSON dict with all engagement metrics, video title, and date range.
    On error, returns dict with 'error' key instead of crashing.

Dependencies:
    - auth.py (Phase 7) for OAuth2 authentication
    - google-api-python-client
    - google-auth-oauthlib
"""

import sys
import json
from datetime import datetime, timezone, date

from tools.logging_config import get_logger
from tools.youtube_analytics.auth import get_authenticated_service

logger = get_logger(__name__)

try:
    from googleapiclient.errors import HttpError
except ImportError:
    # Fallback if import path differs
    HttpError = Exception


def get_video_title(video_id: str) -> str | None:
    """
    Fetch video title from YouTube Data API.

    Args:
        video_id: YouTube video ID

    Returns:
        Video title string, or None if lookup fails
    """
    try:
        youtube = get_authenticated_service('youtube', 'v3')
        response = youtube.videos().list(
            part='snippet',
            id=video_id
        ).execute()

        items = response.get('items', [])
        if items:
            return items[0]['snippet']['title']
        return None

    except Exception:
        # Title lookup failure should not crash the whole request
        return None


def get_video_metrics(video_id: str, start_date: str = None, end_date: str = None) -> dict:
    """
    Fetch core engagement metrics for a video.

    Args:
        video_id: YouTube video ID (e.g., 'dQw4w9WgXcQ')
        start_date: Start of date range (YYYY-MM-DD). Default: 2020-01-01
        end_date: End of date range (YYYY-MM-DD). Default: today

    Returns:
        dict with metrics on success:
            {
                "video_id": "...",
                "title": "Video Title" or None,
                "views": int,
                "watch_time_minutes": float,
                "avg_view_duration_seconds": int,
                "likes": int,
                "dislikes": int,
                "comments": int,
                "shares": int,
                "subscribers_gained": int,
                "subscribers_lost": int,
                "date_range": {"start": "YYYY-MM-DD", "end": "YYYY-MM-DD"},
                "fetched_at": "ISO timestamp"
            }

        dict with error on failure:
            {"error": "Error message", "video_id": "..."}
    """
    # Default date range: 2020-01-01 to today (captures full video lifetime)
    if start_date is None:
        start_date = '2020-01-01'
    if end_date is None:
        end_date = date.today().isoformat()

    try:
        # Build YouTube Analytics service
        youtube_analytics = get_authenticated_service('youtubeAnalytics', 'v2')

        # Query metrics
        response = youtube_analytics.reports().query(
            ids='channel==MINE',
            startDate=start_date,
            endDate=end_date,
            metrics='views,estimatedMinutesWatched,averageViewDuration,likes,dislikes,comments,shares,subscribersGained,subscribersLost',
            dimensions='video',
            filters=f'video=={video_id}',
            maxResults=1
        ).execute()

        # Check if we got data
        rows = response.get('rows', [])
        if not rows:
            return {
                'error': 'No data found for video',
                'video_id': video_id,
                'note': 'Video may not exist, be private, or have no analytics data yet'
            }

        # Parse response - row contains [video_id, metric1, metric2, ...]
        row = rows[0]

        # Map column headers to values
        column_headers = [h['name'] for h in response.get('columnHeaders', [])]
        data = dict(zip(column_headers, row))

        # Fetch video title (failure here won't crash the request)
        title = get_video_title(video_id)

        # Build result dict with snake_case keys
        result = {
            'video_id': video_id,
            'title': title,
            'views': int(data.get('views', 0)),
            'watch_time_minutes': float(data.get('estimatedMinutesWatched', 0)),
            'avg_view_duration_seconds': int(data.get('averageViewDuration', 0)),
            'likes': int(data.get('likes', 0)),
            'dislikes': int(data.get('dislikes', 0)),
            'comments': int(data.get('comments', 0)),
            'shares': int(data.get('shares', 0)),
            'subscribers_gained': int(data.get('subscribersGained', 0)),
            'subscribers_lost': int(data.get('subscribersLost', 0)),
            'date_range': {
                'start': start_date,
                'end': end_date
            },
            'fetched_at': datetime.now(timezone.utc).isoformat() + 'Z'
        }

        return result

    except HttpError as e:
        # Handle specific HTTP errors
        status_code = e.resp.status if hasattr(e, 'resp') else None

        if status_code == 400:
            return {
                'error': 'Invalid video ID or bad request',
                'video_id': video_id,
                'details': str(e)
            }
        elif status_code == 403:
            return {
                'error': 'API quota exceeded or permission denied',
                'video_id': video_id,
                'details': str(e)
            }
        elif status_code == 404:
            return {
                'error': 'Video not found',
                'video_id': video_id
            }
        else:
            return {
                'error': f'API error (HTTP {status_code})',
                'video_id': video_id,
                'details': str(e)
            }

    except Exception as e:
        return {
            'error': f'Unexpected error: {type(e).__name__}',
            'video_id': video_id,
            'details': str(e)
        }


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description="Fetch engagement metrics for a YouTube video.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  python -m tools.youtube_analytics.metrics dQw4w9WgXcQ
  python -m tools.youtube_analytics.metrics dQw4w9WgXcQ --start-date 2025-01-01 --end-date 2025-12-31""",
    )
    parser.add_argument("video_id", help="YouTube video ID")
    parser.add_argument(
        "--start-date", metavar="YYYY-MM-DD",
        help="Start date for metrics window (default: 2020-01-01)",
    )
    parser.add_argument(
        "--end-date", metavar="YYYY-MM-DD",
        help="End date for metrics window (default: today)",
    )

    verbosity = parser.add_mutually_exclusive_group()
    verbosity.add_argument("--verbose", "-v", action="store_true", help="Show debug output on stderr")
    verbosity.add_argument("--quiet", "-q", action="store_true", help="Only show errors on stderr")

    args = parser.parse_args()

    from tools.logging_config import setup_logging
    setup_logging(args.verbose, args.quiet)

    result = get_video_metrics(args.video_id, args.start_date, args.end_date)
    print(json.dumps(result, indent=2))
