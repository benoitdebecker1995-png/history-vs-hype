"""
YouTube Analytics Retention Curve Fetcher

Fetches audience retention data and identifies drop-off points for any video.

Usage:
    CLI:
        python retention.py VIDEO_ID
        python retention.py VIDEO_ID --threshold 0.03

    Import:
        from retention import get_retention_data, find_drop_off_points

        data = get_retention_data('VIDEO_ID')
        drop_offs = find_drop_off_points(data['data_points'], threshold=0.05)
"""

import sys
import json
from datetime import datetime, date, timezone

from tools.youtube_analytics.auth import get_authenticated_service

try:
    from googleapiclient.errors import HttpError
except ImportError:
    HttpError = Exception


def get_retention_data(video_id, start_date=None, end_date=None):
    """
    Fetch retention curve data for a video.

    Args:
        video_id: YouTube video ID (11 character string)
        start_date: Start of date range (YYYY-MM-DD), defaults to 2020-01-01
        end_date: End of date range (YYYY-MM-DD), defaults to today

    Returns:
        dict with:
            - video_id: The requested video ID
            - data_points: List of {position, retention, relative} dicts
            - summary: {avg_retention, min_retention, final_retention}
            - date_range: {start, end}
            - fetched_at: ISO timestamp

        On error:
            - {"error": "message", "video_id": video_id}
    """
    # Default date range: video lifetime
    if start_date is None:
        start_date = '2020-01-01'
    if end_date is None:
        end_date = date.today().isoformat()

    try:
        youtube_analytics = get_authenticated_service('youtubeAnalytics', 'v2')

        response = youtube_analytics.reports().query(
            ids='channel==MINE',
            startDate=start_date,
            endDate=end_date,
            metrics='audienceWatchRatio,relativeRetentionPerformance',
            dimensions='elapsedVideoTimeRatio',
            filters=f'video=={video_id};audienceType==ORGANIC',
            maxResults=200,
            sort='elapsedVideoTimeRatio'
        ).execute()

        # Check for empty response
        rows = response.get('rows', [])
        if not rows:
            return {
                "error": "No retention data found for video",
                "video_id": video_id
            }

        # Parse data points
        # Response columns: elapsedVideoTimeRatio, audienceWatchRatio, relativeRetentionPerformance
        data_points = []
        for row in rows:
            data_points.append({
                "position": row[0],  # 0.0 to 1.0
                "retention": row[1],  # 0.0 to 1.0+
                "relative": row[2] if len(row) > 2 else None  # vs similar videos
            })

        # Calculate summary statistics
        retentions = [dp["retention"] for dp in data_points]
        summary = {
            "avg_retention": sum(retentions) / len(retentions) if retentions else 0,
            "min_retention": min(retentions) if retentions else 0,
            "final_retention": retentions[-1] if retentions else 0
        }

        # Find drop-off points
        drop_offs = find_drop_off_points(data_points)

        return {
            "video_id": video_id,
            "data_points": data_points,
            "drop_off_points": drop_offs,
            "summary": summary,
            "date_range": {
                "start": start_date,
                "end": end_date
            },
            "fetched_at": datetime.now(timezone.utc).isoformat()
        }

    except HttpError as e:
        if e.resp.status == 400:
            return {
                "error": "Invalid video ID or bad request",
                "video_id": video_id,
                "details": str(e)
            }
        elif e.resp.status == 403:
            return {
                "error": "API quota exceeded or permission denied",
                "video_id": video_id,
                "details": str(e)
            }
        else:
            return {
                "error": f"API error: {e.resp.status}",
                "video_id": video_id,
                "details": str(e)
            }
    except Exception as e:
        return {
            "error": f"Unexpected error: {type(e).__name__}",
            "video_id": video_id,
            "details": str(e)
        }


def find_drop_off_points(data_points, threshold=0.05):
    """
    Identify significant drop-off points in retention curve.

    A drop-off occurs when retention decreases by more than the threshold
    between consecutive data points.

    Args:
        data_points: List of {position, retention, relative} dicts
        threshold: Minimum drop to flag (default 0.05 = 5%)

    Returns:
        List of drop-off dicts with:
            - position: Where in video (0.0 to 1.0)
            - retention_before: Retention before drop
            - retention_after: Retention after drop
            - drop: Magnitude of drop (positive number)
            - timestamp_hint: Human-readable position hint
    """
    drop_offs = []

    if len(data_points) < 2:
        return drop_offs

    for i in range(1, len(data_points)):
        prev = data_points[i - 1]
        curr = data_points[i]

        # Calculate delta (negative means viewers left)
        delta = curr["retention"] - prev["retention"]

        # Flag if drop exceeds threshold
        if delta < -threshold:
            drop_offs.append({
                "position": curr["position"],
                "retention_before": prev["retention"],
                "retention_after": curr["retention"],
                "drop": abs(delta),
                "timestamp_hint": _get_position_hint(curr["position"])
            })

    return drop_offs


def _get_position_hint(position):
    """
    Convert position (0.0-1.0) to human-readable hint.

    Args:
        position: Float from 0.0 to 1.0

    Returns:
        String like "intro", "early", "first half", etc.
    """
    if position <= 0.10:
        return "intro"
    elif position <= 0.25:
        return "early"
    elif position <= 0.50:
        return "first half"
    elif position <= 0.75:
        return "second half"
    elif position <= 0.90:
        return "toward end"
    else:
        return "conclusion"


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description="Fetch audience retention curve and drop-off points for a YouTube video.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  python -m tools.youtube_analytics.retention dQw4w9WgXcQ
  python -m tools.youtube_analytics.retention dQw4w9WgXcQ --threshold 0.03""",
    )
    parser.add_argument("video_id", help="YouTube video ID")
    parser.add_argument(
        "--threshold", type=float, default=0.05, metavar="FLOAT",
        help="Minimum retention drop to flag as significant (default: 0.05 = 5%%)",
    )

    verbosity = parser.add_mutually_exclusive_group()
    verbosity.add_argument("--verbose", "-v", action="store_true", help="Show debug output on stderr")
    verbosity.add_argument("--quiet", "-q", action="store_true", help="Only show errors on stderr")

    args = parser.parse_args()

    from tools.logging_config import setup_logging
    setup_logging(args.verbose, args.quiet)

    result = get_retention_data(args.video_id)

    # Re-run drop-off detection with custom threshold if specified
    if args.threshold != 0.05 and "data_points" in result:
        result["drop_off_points"] = find_drop_off_points(result["data_points"], args.threshold)

    print(json.dumps(result, indent=2))
