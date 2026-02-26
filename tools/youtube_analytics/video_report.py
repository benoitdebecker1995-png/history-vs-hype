"""
YouTube Video Performance Report Generator

Combines metrics, retention, and CTR data into a unified report.

Usage:
    CLI:
        python video_report.py VIDEO_ID
        python video_report.py VIDEO_ID --json
        python video_report.py VIDEO_ID --markdown

    Import:
        from video_report import generate_video_report

        report = generate_video_report('VIDEO_ID')
        print(report['engagement']['views'])

Output:
    JSON (default) or Markdown format with complete video analysis.
    Partial failures don't crash - errors captured in report.

Dependencies:
    - metrics.py (engagement metrics)
    - retention.py (retention curve)
    - ctr.py (click-through rate)
    - auth.py (OAuth2 authentication)
"""

import sys
import json
from datetime import datetime, timezone, date

from tools.logging_config import get_logger
from tools.youtube_analytics.metrics import get_video_metrics
from tools.youtube_analytics.retention import get_retention_data
from tools.youtube_analytics.ctr import get_ctr_metrics

logger = get_logger(__name__)


def generate_video_report(video_id: str, start_date: str = None, end_date: str = None) -> dict:
    """
    Generate a comprehensive video performance report.

    Aggregates data from metrics, retention, and CTR modules.
    Handles partial failures gracefully.

    Args:
        video_id: YouTube video ID (e.g., 'dQw4w9WgXcQ')
        start_date: Start of date range (YYYY-MM-DD). Default: 2020-01-01
        end_date: End of date range (YYYY-MM-DD). Default: today

    Returns:
        dict with complete report:
            {
                "video_id": "...",
                "title": "..." or None,
                "fetched_at": "ISO timestamp",
                "date_range": {"start": "...", "end": "..."},
                "engagement": {...} or None,
                "ctr": {...} or None,
                "retention": {...} or None,
                "summary": {...},
                "errors": []
            }
    """
    errors = []
    fetched_at = datetime.now(timezone.utc).isoformat()

    # Fetch engagement metrics
    metrics_result = get_video_metrics(video_id, start_date, end_date)
    if 'error' in metrics_result:
        errors.append({'source': 'metrics', 'message': metrics_result['error']})
        engagement = None
        title = None
        # Use actual date for 'end' instead of 'today'
        actual_end = end_date or date.today().isoformat()
        date_range = {'start': start_date or '2020-01-01', 'end': actual_end}
    else:
        engagement = {
            'views': metrics_result.get('views'),
            'watch_time_minutes': metrics_result.get('watch_time_minutes'),
            'avg_view_duration_seconds': metrics_result.get('avg_view_duration_seconds'),
            'likes': metrics_result.get('likes'),
            'dislikes': metrics_result.get('dislikes'),
            'comments': metrics_result.get('comments'),
            'shares': metrics_result.get('shares'),
            'subscribers_gained': metrics_result.get('subscribers_gained'),
            'subscribers_lost': metrics_result.get('subscribers_lost')
        }
        title = metrics_result.get('title')
        date_range = metrics_result.get('date_range', {'start': start_date, 'end': end_date})

    # Fetch CTR metrics
    ctr_result = get_ctr_metrics(video_id, start_date, end_date)
    if 'error' in ctr_result:
        errors.append({'source': 'ctr', 'message': ctr_result['error']})
        ctr = None
    else:
        ctr = {
            'impressions': ctr_result.get('impressions'),
            'ctr_percent': ctr_result.get('ctr_percent'),
            'available': ctr_result.get('ctr_available', False),
            'source': ctr_result.get('ctr_source')
        }
        if not ctr['available']:
            ctr['note'] = ctr_result.get('note', 'CTR not available via API')

    # Fetch retention data
    retention_result = get_retention_data(video_id, start_date, end_date)
    if 'error' in retention_result:
        errors.append({'source': 'retention', 'message': retention_result['error']})
        retention = None
    else:
        summary = retention_result.get('summary', {})
        retention = {
            'avg_retention': summary.get('avg_retention'),
            'final_retention': summary.get('final_retention'),
            'drop_off_points': retention_result.get('drop_off_points', []),
            'data_points_count': len(retention_result.get('data_points', []))
        }

    # Build summary statistics
    report_summary = _build_summary(engagement, ctr, retention)

    return {
        'video_id': video_id,
        'title': title,
        'fetched_at': fetched_at,
        'date_range': date_range,
        'engagement': engagement,
        'ctr': ctr,
        'retention': retention,
        'summary': report_summary,
        'errors': errors
    }


def _build_summary(engagement: dict, ctr: dict, retention: dict) -> dict:
    """
    Calculate summary statistics from available data.

    Args:
        engagement: Engagement metrics dict or None
        ctr: CTR metrics dict or None
        retention: Retention metrics dict or None

    Returns:
        dict with calculated summary stats
    """
    summary = {}

    if engagement:
        views = engagement.get('views', 0) or 0
        watch_time = engagement.get('watch_time_minutes', 0) or 0
        likes = engagement.get('likes', 0) or 0
        comments = engagement.get('comments', 0) or 0

        # Views per minute of content watched
        if watch_time > 0:
            summary['views_per_watch_minute'] = round(views / watch_time, 2)

        # Engagement rate: (likes + comments) / views * 100
        if views > 0:
            summary['engagement_rate'] = round((likes + comments) / views * 100, 2)

        # Format watch time as hours
        summary['watch_time_hours'] = round(watch_time / 60, 1)

        # Format avg duration as mm:ss
        avg_seconds = engagement.get('avg_view_duration_seconds', 0) or 0
        minutes = avg_seconds // 60
        seconds = avg_seconds % 60
        summary['avg_duration_formatted'] = f"{minutes}:{seconds:02d}"

    if retention:
        avg_ret = retention.get('avg_retention')
        if avg_ret is not None:
            summary['retention_percent'] = round(avg_ret * 100, 1)
            # Threshold: 35% is good for educational content
            if avg_ret >= 0.35:
                summary['retention_rating'] = 'good'
            elif avg_ret >= 0.25:
                summary['retention_rating'] = 'average'
            else:
                summary['retention_rating'] = 'needs work'

        # Biggest drop-off
        drops = retention.get('drop_off_points', [])
        if drops:
            biggest = max(drops, key=lambda d: d.get('drop', 0))
            summary['biggest_drop'] = {
                'position': round(biggest.get('position', 0) * 100, 1),
                'drop_percent': round(biggest.get('drop', 0) * 100, 1),
                'location': biggest.get('timestamp_hint', 'unknown')
            }

    if ctr:
        if ctr.get('available') and ctr.get('ctr_percent') is not None:
            summary['ctr_status'] = f"{ctr['ctr_percent']}%"
        else:
            summary['ctr_status'] = 'Check YouTube Studio'

    return summary


def format_as_markdown(report: dict) -> str:
    """
    Format report as human-readable Markdown.

    Args:
        report: Report dict from generate_video_report()

    Returns:
        Markdown-formatted string
    """
    lines = []

    # Header
    title = report.get('title') or report.get('video_id')
    lines.append(f"# Video Report: {title}")
    lines.append("")
    lines.append(f"**Video ID:** {report.get('video_id')}")

    date_range = report.get('date_range', {})
    if date_range:
        lines.append(f"**Data from:** {date_range.get('start')} to {date_range.get('end')}")

    lines.append(f"**Report generated:** {report.get('fetched_at', 'Unknown')}")
    lines.append("")

    # Quick Insights
    summary = report.get('summary', {})
    engagement = report.get('engagement')
    retention = report.get('retention')

    lines.append("## Quick Insights")
    lines.append("")

    if 'retention_percent' in summary:
        rating = summary.get('retention_rating', 'unknown')
        # Add threshold context
        threshold_note = ""
        if rating == 'good':
            threshold_note = " - above 35% benchmark"
        elif rating == 'needs work':
            threshold_note = " - below 25% benchmark"
        lines.append(f"- **Average retention:** {summary['retention_percent']}% ({rating}{threshold_note})")

    if 'biggest_drop' in summary:
        drop = summary['biggest_drop']
        lines.append(f"- **Biggest drop-off:** {drop['drop_percent']}% at {drop['position']}% ({drop['location']})")
        # Add drop-off count
        if retention and retention.get('drop_off_points'):
            drop_count = len(retention['drop_off_points'])
            lines.append(f"- **Total significant drops:** {drop_count}")

    lines.append(f"- **CTR:** {summary.get('ctr_status', 'N/A')}")

    if 'engagement_rate' in summary:
        eng_rate = summary['engagement_rate']
        # Add context for engagement rate
        eng_note = ""
        if eng_rate >= 5:
            eng_note = " (excellent)"
        elif eng_rate >= 2:
            eng_note = " (good)"
        elif eng_rate >= 1:
            eng_note = " (average)"
        else:
            eng_note = " (low)"
        lines.append(f"- **Engagement rate:** {eng_rate}%{eng_note}")

    if 'watch_time_hours' in summary:
        lines.append(f"- **Total watch time:** {summary['watch_time_hours']} hours")

    # Add subscriber efficiency metric
    if engagement:
        subs = engagement.get('subscribers_gained', 0) or 0
        views = engagement.get('views', 0) or 0
        if views > 0 and subs > 0:
            subs_per_100_views = round(subs / views * 100, 2)
            lines.append(f"- **Subscribers per 100 views:** {subs_per_100_views}")

    lines.append("")

    # Engagement metrics table
    engagement = report.get('engagement')
    if engagement:
        lines.append("## Performance Metrics")
        lines.append("")
        lines.append("| Metric | Value |")
        lines.append("|--------|-------|")

        views = engagement.get('views', 0)
        lines.append(f"| Views | {views:,} |")

        if summary.get('watch_time_hours'):
            lines.append(f"| Watch Time | {summary['watch_time_hours']} hours |")

        if summary.get('avg_duration_formatted'):
            lines.append(f"| Avg Duration | {summary['avg_duration_formatted']} |")

        likes = engagement.get('likes', 0)
        dislikes = engagement.get('dislikes', 0)
        lines.append(f"| Likes / Dislikes | {likes:,} / {dislikes:,} |")

        comments = engagement.get('comments', 0)
        lines.append(f"| Comments | {comments:,} |")

        shares = engagement.get('shares', 0)
        lines.append(f"| Shares | {shares:,} |")

        subs_gained = engagement.get('subscribers_gained', 0)
        subs_lost = engagement.get('subscribers_lost', 0)
        lines.append(f"| Subscribers Gained/Lost | +{subs_gained} / -{subs_lost} |")

        lines.append("")
    else:
        lines.append("## Performance Metrics")
        lines.append("")
        lines.append("*Metrics data unavailable*")
        lines.append("")

    # CTR section
    ctr = report.get('ctr')
    lines.append("## Click-Through Rate")
    lines.append("")
    if ctr and ctr.get('available'):
        lines.append(f"- **Impressions:** {ctr.get('impressions', 0):,}")
        lines.append(f"- **CTR:** {ctr.get('ctr_percent')}%")
    else:
        lines.append("*CTR not available via API. Check YouTube Studio manually.*")
    lines.append("")

    # Retention section
    retention = report.get('retention')
    if retention:
        lines.append("## Retention Analysis")
        lines.append("")

        avg_ret = retention.get('avg_retention')
        if avg_ret is not None:
            lines.append(f"- **Average retention:** {round(avg_ret * 100, 1)}%")

        final_ret = retention.get('final_retention')
        if final_ret is not None:
            lines.append(f"- **Final retention:** {round(final_ret * 100, 1)}%")

        lines.append(f"- **Data points:** {retention.get('data_points_count', 0)}")
        lines.append("")

        # Drop-off table - sorted by magnitude (biggest first)
        drops = retention.get('drop_off_points', [])
        if drops:
            lines.append("### Retention Drop-offs")
            lines.append("")
            lines.append("*Sorted by impact (biggest drops first)*")
            lines.append("")
            lines.append("| Position | Viewers Lost | Location |")
            lines.append("|----------|--------------|----------|")

            # Sort by drop magnitude (biggest first)
            sorted_drops = sorted(drops, key=lambda d: d.get('drop', 0), reverse=True)

            for drop in sorted_drops[:10]:  # Limit to top 10
                pos = round(drop.get('position', 0) * 100, 1)
                lost = round(drop.get('drop', 0) * 100, 1)
                hint = drop.get('timestamp_hint', 'unknown')
                lines.append(f"| {pos}% | {lost}% dropped | {hint} |")

            if len(drops) > 10:
                lines.append(f"| ... | ({len(drops) - 10} more drops) | ... |")

            lines.append("")
    else:
        lines.append("## Retention Analysis")
        lines.append("")
        lines.append("*Retention data unavailable*")
        lines.append("")

    # Errors section
    errors = report.get('errors', [])
    if errors:
        lines.append("## Errors")
        lines.append("")
        for err in errors:
            lines.append(f"- **{err.get('source')}:** {err.get('message')}")
        lines.append("")

    return "\n".join(lines)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate a comprehensive performance report for a YouTube video.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  python -m tools.youtube_analytics.video_report dQw4w9WgXcQ
  python -m tools.youtube_analytics.video_report dQw4w9WgXcQ --markdown""",
    )
    parser.add_argument("video_id", help="YouTube video ID")

    fmt_group = parser.add_mutually_exclusive_group()
    fmt_group.add_argument(
        "--json", action="store_true", default=True,
        help="Output as JSON (default)",
    )
    fmt_group.add_argument(
        "--markdown", action="store_true",
        help="Output as human-readable Markdown",
    )

    verbosity = parser.add_mutually_exclusive_group()
    verbosity.add_argument("--verbose", "-v", action="store_true", help="Show debug output on stderr")
    verbosity.add_argument("--quiet", "-q", action="store_true", help="Only show errors on stderr")

    args = parser.parse_args()

    from tools.logging_config import setup_logging
    setup_logging(args.verbose, args.quiet)

    report = generate_video_report(args.video_id)

    if args.markdown:
        print(format_as_markdown(report))
    else:
        print(json.dumps(report, indent=2))
