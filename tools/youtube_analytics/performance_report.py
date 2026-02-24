"""
Performance Report Generator

Aggregates video performance data by topic type and content angle to identify
patterns that correlate with high subscriber conversion.

Usage:
    Python:
        from performance_report import (
            aggregate_by_topic,
            aggregate_by_angle,
            generate_performance_report,
            save_report
        )

        # Generate and save report
        report = generate_performance_report()
        save_report(report)

    CLI (via performance.py):
        python performance.py --report              # Generate full report
        python performance.py --report --save       # Generate and save
        python performance.py --by-topic            # Show conversion by topic
        python performance.py --by-angle            # Show conversion by angle

Dependencies:
    - database.py (Phase 15+) for KeywordDB queries
"""

import sys
import json
from pathlib import Path
from datetime import datetime, timezone
from collections import defaultdict
from statistics import mean, median
from typing import Dict, List, Any, Optional

try:
    from tools.discovery.database import KeywordDB
    DATABASE_AVAILABLE = True
except ImportError:
    DATABASE_AVAILABLE = False


def aggregate_by_topic(videos: List[dict], min_count: int = 2) -> Dict[str, Dict[str, Any]]:
    """
    Aggregate video performance by topic type.

    Groups videos by topic_type and calculates statistics for each group.
    Only includes topics with at least min_count videos for statistical significance.

    Args:
        videos: List of video performance dicts from database
        min_count: Minimum videos required to include a topic (default 2)

    Returns:
        Dict mapping topic -> stats:
            {
                'territorial': {
                    'count': 5,
                    'avg_conversion_rate': 0.85,
                    'median_conversion_rate': 0.82,
                    'avg_views': 15000,
                    'total_subscribers_gained': 42,
                    'videos': ['Title 1', 'Title 2', ...]
                },
                ...
            }

    Example:
        >>> stats = aggregate_by_topic(videos)
        >>> print(stats['territorial']['avg_conversion_rate'])
        0.85
    """
    # Group videos by topic
    by_topic = defaultdict(list)

    for video in videos:
        topic = video.get('topic_type') or 'general'
        by_topic[topic].append(video)

    # Calculate stats for each topic
    result = {}

    for topic, topic_videos in by_topic.items():
        if len(topic_videos) < min_count:
            continue

        conversion_rates = [
            v.get('conversion_rate', 0) or 0
            for v in topic_videos
        ]
        views = [v.get('views', 0) or 0 for v in topic_videos]
        subs_gained = [v.get('subscribers_gained', 0) or 0 for v in topic_videos]

        result[topic] = {
            'count': len(topic_videos),
            'avg_conversion_rate': mean(conversion_rates) if conversion_rates else 0,
            'median_conversion_rate': median(conversion_rates) if conversion_rates else 0,
            'avg_views': mean(views) if views else 0,
            'total_subscribers_gained': sum(subs_gained),
            'videos': [v.get('title', 'Unknown') for v in topic_videos]
        }

    return result


def aggregate_by_angle(videos: List[dict], min_count: int = 2) -> Dict[str, Dict[str, Any]]:
    """
    Aggregate video performance by content angle.

    Groups videos by each angle they contain (videos can appear in multiple groups).
    Only includes angles with at least min_count videos for statistical significance.

    Args:
        videos: List of video performance dicts from database
        min_count: Minimum videos required to include an angle (default 2)

    Returns:
        Dict mapping angle -> stats (same structure as aggregate_by_topic)

    Example:
        >>> stats = aggregate_by_angle(videos)
        >>> print(stats['legal']['avg_conversion_rate'])
        0.92
    """
    # Group videos by angle (video can appear in multiple groups)
    by_angle = defaultdict(list)

    for video in videos:
        angles = video.get('angles') or []

        # Handle case where angles might still be JSON string
        if isinstance(angles, str):
            try:
                angles = json.loads(angles)
            except (json.JSONDecodeError, TypeError):
                angles = []

        # If no angles, use 'general'
        if not angles:
            angles = ['general']

        for angle in angles:
            by_angle[angle].append(video)

    # Calculate stats for each angle
    result = {}

    for angle, angle_videos in by_angle.items():
        if len(angle_videos) < min_count:
            continue

        conversion_rates = [
            v.get('conversion_rate', 0) or 0
            for v in angle_videos
        ]
        views = [v.get('views', 0) or 0 for v in angle_videos]
        subs_gained = [v.get('subscribers_gained', 0) or 0 for v in angle_videos]

        result[angle] = {
            'count': len(angle_videos),
            'avg_conversion_rate': mean(conversion_rates) if conversion_rates else 0,
            'median_conversion_rate': median(conversion_rates) if conversion_rates else 0,
            'avg_views': mean(views) if views else 0,
            'total_subscribers_gained': sum(subs_gained),
            'videos': [v.get('title', 'Unknown') for v in angle_videos]
        }

    return result


def identify_top_converters(videos: List[dict], n: int = 5) -> List[dict]:
    """
    Identify top converting videos.

    Args:
        videos: List of video performance dicts
        n: Number of top videos to return (default 5)

    Returns:
        List of top n videos sorted by conversion_rate DESC
    """
    # Filter out videos without conversion rate
    valid_videos = [
        v for v in videos
        if v.get('conversion_rate') is not None
    ]

    # Sort by conversion rate descending
    sorted_videos = sorted(
        valid_videos,
        key=lambda v: v.get('conversion_rate', 0) or 0,
        reverse=True
    )

    return sorted_videos[:n]


def identify_conversion_patterns(
    topic_stats: Dict[str, Dict[str, Any]],
    angle_stats: Dict[str, Dict[str, Any]]
) -> List[str]:
    """
    Generate insight strings from aggregated stats.

    Compares best vs worst performers and generates actionable insights.

    Args:
        topic_stats: Output from aggregate_by_topic()
        angle_stats: Output from aggregate_by_angle()

    Returns:
        List of insight strings

    Example:
        >>> insights = identify_conversion_patterns(topic_stats, angle_stats)
        >>> for i in insights:
        ...     print(f"- {i}")
        - Territorial topics average 0.85 subs/100 views (2x higher than colonial)
        - Legal angle correlates with highest conversion (0.92 subs/100 views)
    """
    insights = []

    # Topic insights
    if topic_stats:
        # Sort topics by conversion rate
        sorted_topics = sorted(
            topic_stats.items(),
            key=lambda x: x[1]['avg_conversion_rate'],
            reverse=True
        )

        if len(sorted_topics) >= 1:
            best_topic = sorted_topics[0]
            insights.append(
                f"{best_topic[0].title()} topics have highest conversion: "
                f"{best_topic[1]['avg_conversion_rate']:.2f} subs/100 views "
                f"({best_topic[1]['count']} videos)"
            )

        if len(sorted_topics) >= 2:
            best = sorted_topics[0]
            worst = sorted_topics[-1]
            if worst[1]['avg_conversion_rate'] > 0:
                ratio = best[1]['avg_conversion_rate'] / worst[1]['avg_conversion_rate']
                insights.append(
                    f"{best[0].title()} converts {ratio:.1f}x better than {worst[0]}"
                )

    # Angle insights
    if angle_stats:
        sorted_angles = sorted(
            angle_stats.items(),
            key=lambda x: x[1]['avg_conversion_rate'],
            reverse=True
        )

        if len(sorted_angles) >= 1:
            best_angle = sorted_angles[0]
            insights.append(
                f"{best_angle[0].title()} angle correlates with strong conversion: "
                f"{best_angle[1]['avg_conversion_rate']:.2f} subs/100 views"
            )

    # Sample size warnings
    small_samples = []
    for topic, stats in topic_stats.items():
        if stats['count'] < 3:
            small_samples.append(f"{topic} ({stats['count']})")

    if small_samples:
        insights.append(
            f"Note: Low sample sizes for {', '.join(small_samples)} - patterns may not be reliable"
        )

    return insights


def generate_performance_report() -> str:
    """
    Generate comprehensive performance report as markdown.

    Fetches all video performance from database, aggregates by topic and angle,
    identifies patterns, and formats as markdown report.

    Returns:
        Markdown string with full report

        If database unavailable or no data, returns report with appropriate message.

    Example:
        >>> report = generate_performance_report()
        >>> print(report[:100])
        # Performance Report: Subscriber Conversion Analysis
        ...
    """
    timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')

    # Check database availability
    if not DATABASE_AVAILABLE:
        return f"""# Performance Report: Subscriber Conversion Analysis

**Generated:** {timestamp}
**Status:** Database not available

Run `python performance.py --fetch-all` to populate the database first.
"""

    # Fetch data from database
    try:
        db = KeywordDB()
        videos = db.get_all_video_performance(limit=500)
        db.close()
    except Exception as e:
        return f"""# Performance Report: Subscriber Conversion Analysis

**Generated:** {timestamp}
**Status:** Error fetching data

Error: {str(e)}
"""

    if not videos:
        return f"""# Performance Report: Subscriber Conversion Analysis

**Generated:** {timestamp}
**Videos analyzed:** 0

No video performance data found. Run `python performance.py --fetch-all` to populate.
"""

    # Aggregate data
    topic_stats = aggregate_by_topic(videos, min_count=1)
    angle_stats = aggregate_by_angle(videos, min_count=1)
    top_converters = identify_top_converters(videos, n=5)
    insights = identify_conversion_patterns(topic_stats, angle_stats)

    # Build report
    lines = [
        "# Performance Report: Subscriber Conversion Analysis",
        "",
        f"**Generated:** {timestamp}",
        f"**Videos analyzed:** {len(videos)}",
        "",
    ]

    # Key Insights section
    lines.append("## Key Insights")
    lines.append("")
    if insights:
        for insight in insights:
            lines.append(f"- {insight}")
    else:
        lines.append("- Insufficient data for pattern detection")
    lines.append("")

    # Conversion by Topic Type section
    lines.append("## Conversion by Topic Type")
    lines.append("")
    if topic_stats:
        lines.append("| Topic | Videos | Avg Conversion | Median | Total Subs |")
        lines.append("|-------|--------|----------------|--------|------------|")

        # Sort by conversion rate descending
        sorted_topics = sorted(
            topic_stats.items(),
            key=lambda x: x[1]['avg_conversion_rate'],
            reverse=True
        )

        for topic, stats in sorted_topics:
            lines.append(
                f"| {topic} | {stats['count']} | "
                f"{stats['avg_conversion_rate']:.3f}% | "
                f"{stats['median_conversion_rate']:.3f}% | "
                f"{stats['total_subscribers_gained']} |"
            )
    else:
        lines.append("*No topic data available*")
    lines.append("")

    # Conversion by Angle section
    lines.append("## Conversion by Angle")
    lines.append("")
    if angle_stats:
        lines.append("| Angle | Videos | Avg Conversion | Median | Total Subs |")
        lines.append("|-------|--------|----------------|--------|------------|")

        sorted_angles = sorted(
            angle_stats.items(),
            key=lambda x: x[1]['avg_conversion_rate'],
            reverse=True
        )

        for angle, stats in sorted_angles:
            lines.append(
                f"| {angle} | {stats['count']} | "
                f"{stats['avg_conversion_rate']:.3f}% | "
                f"{stats['median_conversion_rate']:.3f}% | "
                f"{stats['total_subscribers_gained']} |"
            )
    else:
        lines.append("*No angle data available*")
    lines.append("")

    # Top Converters section
    lines.append("## Top Converters")
    lines.append("")
    if top_converters:
        lines.append("| Rank | Title | Conversion | Views | Subs Gained |")
        lines.append("|------|-------|------------|-------|-------------|")

        for i, video in enumerate(top_converters, 1):
            title = (video.get('title') or 'Unknown')[:40]
            conv = video.get('conversion_rate', 0) or 0
            views = video.get('views', 0) or 0
            subs = video.get('subscribers_gained', 0) or 0

            lines.append(f"| {i} | {title} | {conv:.3f}% | {views:,} | {subs} |")
    else:
        lines.append("*No conversion data available*")
    lines.append("")

    # Recommendations section
    lines.append("## Recommendations")
    lines.append("")

    if topic_stats:
        best_topic = max(topic_stats.items(), key=lambda x: x[1]['avg_conversion_rate'])
        lines.append(f"- [ ] Prioritize **{best_topic[0]}** topics for subscriber growth")

    if angle_stats:
        best_angle = max(angle_stats.items(), key=lambda x: x[1]['avg_conversion_rate'])
        lines.append(f"- [ ] Use **{best_angle[0]}** angle in upcoming videos")

    if len(videos) < 10:
        lines.append(f"- [ ] Collect more performance data ({len(videos)}/10 minimum for reliable patterns)")

    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("*Report generated by performance_report.py (Phase 19)*")

    return "\n".join(lines)


def save_report(report: str, path: Optional[str] = None) -> Dict[str, Any]:
    """
    Save performance report to file.

    Args:
        report: Markdown report string
        path: Custom save path (default: channel-data/patterns/PERFORMANCE-REPORT.md)

    Returns:
        {'saved_to': str} on success
        {'error': str} on failure
    """
    if path is None:
        # Default path relative to project root
        project_root = Path(__file__).parent.parent.parent
        default_path = project_root / 'channel-data' / 'patterns' / 'PERFORMANCE-REPORT.md'
        path = str(default_path)

    try:
        # Ensure directory exists
        Path(path).parent.mkdir(parents=True, exist_ok=True)

        # Write report
        with open(path, 'w', encoding='utf-8') as f:
            f.write(report)

        return {'saved_to': path}

    except Exception as e:
        return {'error': f'Failed to save report: {str(e)}'}


if __name__ == '__main__':
    # Quick test
    print("Generating performance report...")
    report = generate_performance_report()
    print(report)
