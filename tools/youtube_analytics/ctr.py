"""
YouTube Analytics CTR (Click-Through Rate) Fetcher

Fetches thumbnail impressions and CTR for a video via the YouTube Analytics API.
Implements graceful fallback when CTR metrics are unavailable (per API limitations).

Usage:
    CLI:
        python ctr.py VIDEO_ID

    Python:
        from ctr import get_ctr_metrics

        result = get_ctr_metrics('VIDEO_ID')
        if result['ctr_available']:
            print(f"CTR: {result['ctr_percent']}%")
        else:
            print("CTR not available via API")

Returns:
    JSON dict with CTR metrics or fallback structure (never crashes).

Notes:
    - CTR metrics may not be available via API for all videos
    - Per Google Issue Tracker #254665034, availability is inconsistent
    - On unavailability, returns structured fallback (not error)

Dependencies:
    - auth.py (Phase 7) for OAuth2 authentication
"""

import sys
import json
from datetime import datetime, date, timezone

from tools.logging_config import get_logger
from tools.youtube_analytics.auth import get_authenticated_service

logger = get_logger(__name__)

try:
    from googleapiclient.errors import HttpError
except ImportError:
    # Fallback if import path differs
    HttpError = Exception


def get_ctr_metrics(video_id: str, start_date: str = None, end_date: str = None) -> dict:
    """
    Fetch CTR metrics for a video with graceful fallback.

    Args:
        video_id: YouTube video ID (e.g., 'dQw4w9WgXcQ')
        start_date: Start of date range (YYYY-MM-DD). Default: 2020-01-01
        end_date: End of date range (YYYY-MM-DD). Default: today

    Returns:
        Success case:
            {
                "video_id": "...",
                "impressions": int,
                "ctr_percent": float,  # Already as percentage (e.g., 4.2)
                "ctr_available": True,
                "ctr_source": "api",
                "date_range": {"start": "YYYY-MM-DD", "end": "YYYY-MM-DD"},
                "fetched_at": "ISO timestamp"
            }

        Fallback case (CTR unavailable via API):
            {
                "video_id": "...",
                "impressions": None,
                "ctr_percent": None,
                "ctr_available": False,
                "ctr_source": "api_unavailable",
                "note": "CTR metrics not available via API. Check YouTube Studio manually.",
                "date_range": {"start": "YYYY-MM-DD", "end": "YYYY-MM-DD"},
                "fetched_at": "ISO timestamp"
            }

        Error case (general API error):
            {"error": "Error message", "video_id": "..."}
    """
    # Default date range: 2020-01-01 to today (captures full video lifetime)
    if start_date is None:
        start_date = '2020-01-01'
    if end_date is None:
        end_date = date.today().isoformat()

    fetched_at = datetime.now(timezone.utc).isoformat()
    date_range = {'start': start_date, 'end': end_date}

    try:
        # Build YouTube Analytics service
        youtube_analytics = get_authenticated_service('youtubeAnalytics', 'v2')

        # Query CTR metrics
        response = youtube_analytics.reports().query(
            ids='channel==MINE',
            startDate=start_date,
            endDate=end_date,
            metrics='views,videoThumbnailImpressions,videoThumbnailImpressionsClickRate',
            dimensions='video',
            filters=f'video=={video_id}',
            maxResults=1
        ).execute()

        # Check if we got data
        rows = response.get('rows', [])
        if not rows:
            # No data returned - could be new video or no impressions yet
            return {
                'video_id': video_id,
                'impressions': None,
                'ctr_percent': None,
                'ctr_available': False,
                'ctr_source': 'api_unavailable',
                'note': 'No CTR data returned. Video may be new or have insufficient impressions.',
                'date_range': date_range,
                'fetched_at': fetched_at
            }

        # Parse response
        row = rows[0]
        column_headers = [h['name'] for h in response.get('columnHeaders', [])]
        data = dict(zip(column_headers, row))

        # Extract CTR metrics
        impressions = data.get('videoThumbnailImpressions')
        ctr_rate = data.get('videoThumbnailImpressionsClickRate')

        if impressions is not None and ctr_rate is not None:
            return {
                'video_id': video_id,
                'impressions': int(impressions),
                'ctr_percent': round(float(ctr_rate) * 100, 2),  # Convert to percentage
                'ctr_available': True,
                'ctr_source': 'api',
                'date_range': date_range,
                'fetched_at': fetched_at
            }
        else:
            # CTR fields present but null/missing
            return {
                'video_id': video_id,
                'impressions': None,
                'ctr_percent': None,
                'ctr_available': False,
                'ctr_source': 'api_unavailable',
                'note': 'CTR metrics not available via API. Check YouTube Studio manually.',
                'date_range': date_range,
                'fetched_at': fetched_at
            }

    except HttpError as e:
        status_code = e.resp.status if hasattr(e, 'resp') else None
        error_content = str(e)

        # Check if this is specifically a CTR unavailability error
        is_ctr_specific_error = (
            status_code in (400, 403) and
            ('videoThumbnailImpressions' in error_content.lower() or
             'ctr' in error_content.lower() or
             'impressions' in error_content.lower())
        )

        if is_ctr_specific_error or status_code == 400:
            # CTR-specific unavailability - return fallback, not error
            return {
                'video_id': video_id,
                'impressions': None,
                'ctr_percent': None,
                'ctr_available': False,
                'ctr_source': 'api_unavailable',
                'note': 'CTR metrics not available via API. Check YouTube Studio manually.',
                'date_range': date_range,
                'fetched_at': fetched_at
            }

        elif status_code == 403:
            # Quota or permission issue
            return {
                'error': 'API quota exceeded or permission denied',
                'video_id': video_id,
                'details': error_content
            }

        else:
            # General API error
            return {
                'error': f'API error (HTTP {status_code})',
                'video_id': video_id,
                'details': error_content
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
        description="Fetch CTR (click-through rate) metrics for a YouTube video.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  python -m tools.youtube_analytics.ctr dQw4w9WgXcQ
  python -m tools.youtube_analytics.ctr dQw4w9WgXcQ --start-date 2025-01-01

Note: CTR metrics may not be available via API for all videos.
If unavailable, returns a structured fallback with a note to check YouTube Studio.""",
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

    result = get_ctr_metrics(args.video_id, args.start_date, args.end_date)
    print(json.dumps(result, indent=2))
