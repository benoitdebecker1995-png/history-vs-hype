"""
Topic Strategy Module

Aggregates video performance by topic type and generates concrete next steps.
Flags low-confidence insights when based on fewer than 3 videos.

Usage:
    from topic_strategy import generate_topic_strategy, format_strategy_terminal

    strategy = generate_topic_strategy()
    print(format_strategy_terminal(strategy))

    # Or save markdown report
    from topic_strategy import format_strategy_markdown
    markdown = format_strategy_markdown(strategy)
    with open('TOPIC-STRATEGY.md', 'w') as f:
        f.write(markdown)

CLI:
    python topic_strategy.py                    # Terminal format
    python topic_strategy.py --markdown         # Markdown format
    python topic_strategy.py --save             # Save to channel-data/

Dependencies:
    - KeywordDB for video_performance queries
    - performance.py TAG_VOCABULARY for topic classification
    - stdlib: json, statistics, datetime, pathlib
"""

import sys
import json
from pathlib import Path
from datetime import datetime, timezone
from statistics import mean, median
from typing import Dict, List, Any, Optional

from tools.discovery.database import KeywordDB

# Import TAG_VOCABULARY from performance.py
try:
    from .performance import TAG_VOCABULARY
except ImportError:
    # Fallback if performance.py not available
    TAG_VOCABULARY = {
        'territorial': ['dispute', 'border', 'territory'],
        'ideological': ['myth', 'debunk', 'fact-check'],
        'colonial': ['colonial', 'empire', 'independence'],
        'legal': ['treaty', 'court', 'icj', 'ruling'],
        'general': []
    }


# =========================================================================
# STRATEGY GENERATION
# =========================================================================

def generate_topic_strategy() -> Dict[str, Any]:
    """
    Aggregate performance by topic type and generate concrete recommendations.

    Queries video_performance table, groups by topic_type, calculates averages,
    flags low-confidence insights, and generates actionable next steps.

    Returns:
        Strategy dict on success:
            {
                'topic_stats': [
                    {
                        'topic': 'territorial',
                        'avg_retention': 0.34,
                        'avg_conversion': 0.42,
                        'video_count': 5,
                        'confidence': 'high',
                        'best_video': {'title': '...', 'conversion': 0.8},
                        'worst_video': {'title': '...', 'conversion': 0.1},
                        'common_observations': [...]
                    }
                ],
                'best_performing': [...],  # Top 2 topic types
                'worst_performing': [...],  # Bottom 2 topic types
                'concrete_next_steps': [...],
                'channel_average_conversion': float,
                'total_videos': int,
                'generated_at': str
            }

        Error dict on failure:
            {'error': msg}
    """
    try:
        db = KeywordDB()

        # Query all videos with performance data
        cursor = db._conn.cursor()
        cursor.execute("""
            SELECT video_id, title, topic_type, conversion_rate,
                   avg_retention_pct, lessons_learned, views, subscribers_gained
            FROM video_performance
            WHERE conversion_rate IS NOT NULL
            ORDER BY conversion_rate DESC
        """)

        rows = cursor.fetchall()
        db.close()

        if not rows:
            return {'error': 'No video performance data available. Run performance.py --fetch-all first.'}

        # Group by topic type
        by_topic = {}
        all_conversions = []

        for row in rows:
            topic = row['topic_type'] or 'general'
            conversion = row['conversion_rate'] or 0
            retention = row['avg_retention_pct'] or 0
            title = row['title'] or 'Unknown'
            lessons = row['lessons_learned']

            all_conversions.append(conversion)

            if topic not in by_topic:
                by_topic[topic] = {
                    'videos': [],
                    'conversions': [],
                    'retentions': [],
                    'observations': []
                }

            by_topic[topic]['videos'].append({
                'title': title,
                'conversion': conversion,
                'retention': retention
            })
            by_topic[topic]['conversions'].append(conversion)
            by_topic[topic]['retentions'].append(retention)

            # Extract observations from lessons_learned
            if lessons:
                try:
                    lessons_obj = json.loads(lessons)
                    observations = lessons_obj.get('observations', [])
                    by_topic[topic]['observations'].extend(observations)
                except (json.JSONDecodeError, TypeError, AttributeError, KeyError):
                    pass

        # Calculate channel average
        channel_avg_conversion = mean(all_conversions) if all_conversions else 0

        # Calculate stats for each topic
        topic_stats = []

        for topic, data in by_topic.items():
            video_count = len(data['videos'])

            # Calculate averages
            avg_conversion = mean(data['conversions']) if data['conversions'] else 0
            avg_retention = mean(data['retentions']) if data['retentions'] else 0

            # Determine confidence
            if video_count >= 6:
                confidence = 'high'
            elif video_count >= 3:
                confidence = 'medium'
            else:
                confidence = 'low'

            # Find best and worst videos
            best_video = max(data['videos'], key=lambda v: v['conversion'])
            worst_video = min(data['videos'], key=lambda v: v['conversion'])

            # Extract common observations (top 3 most frequent)
            common_observations = _extract_common_observations(data['observations'], limit=3)

            topic_stats.append({
                'topic': topic,
                'avg_retention': avg_retention,
                'avg_conversion': avg_conversion,
                'video_count': video_count,
                'confidence': confidence,
                'best_video': {
                    'title': best_video['title'],
                    'conversion': best_video['conversion']
                },
                'worst_video': {
                    'title': worst_video['title'],
                    'conversion': worst_video['conversion']
                },
                'common_observations': common_observations
            })

        # Sort by conversion rate descending
        topic_stats.sort(key=lambda t: t['avg_conversion'], reverse=True)

        # Identify best and worst performers
        best_performing = topic_stats[:2] if len(topic_stats) >= 2 else topic_stats
        worst_performing = topic_stats[-2:] if len(topic_stats) >= 2 else []

        # Generate concrete next steps
        next_steps = _generate_next_steps(
            topic_stats,
            best_performing,
            worst_performing,
            channel_avg_conversion
        )

        return {
            'topic_stats': topic_stats,
            'best_performing': best_performing,
            'worst_performing': worst_performing,
            'concrete_next_steps': next_steps,
            'channel_average_conversion': channel_avg_conversion,
            'total_videos': len(rows),
            'generated_at': datetime.now(timezone.utc).isoformat() + 'Z'
        }

    except Exception as e:
        return {'error': f'Database error: {str(e)}'}


def _extract_common_observations(observations: List[str], limit: int = 3) -> List[str]:
    """
    Extract most common observations from list.

    Groups similar observations by first 50 characters.

    Args:
        observations: List of observation strings
        limit: Max observations to return

    Returns:
        List of common observation strings
    """
    if not observations:
        return []

    # Count observation prefixes
    observation_counts = {}
    for obs in observations:
        # Use first 50 chars as key for grouping similar observations
        key = obs[:50].strip()
        observation_counts[key] = observation_counts.get(key, 0) + 1

    # Sort by frequency
    sorted_obs = sorted(
        observation_counts.items(),
        key=lambda x: x[1],
        reverse=True
    )

    # Return top N
    return [obs for obs, count in sorted_obs[:limit]]


def _generate_next_steps(
    topic_stats: List[Dict],
    best_performing: List[Dict],
    worst_performing: List[Dict],
    channel_avg: float
) -> List[str]:
    """
    Generate concrete next steps based on topic performance patterns.

    Args:
        topic_stats: All topic statistics
        best_performing: Top performing topics
        worst_performing: Bottom performing topics
        channel_avg: Channel average conversion rate

    Returns:
        List of actionable recommendation strings
    """
    steps = []

    # Recommendation 1: Prioritize best performer if significantly above average
    if best_performing:
        best = best_performing[0]
        if best['avg_conversion'] > channel_avg * 1.5:
            confidence_note = f" ({best['confidence']} confidence, {best['video_count']} videos)" if best['confidence'] == 'low' else ''
            steps.append(
                f"Prioritize {best['topic']} topics -- {best['avg_conversion']:.2f}% conversion "
                f"vs {channel_avg:.2f}% channel average{confidence_note}"
            )

    # Recommendation 2: Apply successful patterns to underperformers
    if best_performing and worst_performing and len(best_performing) > 0 and len(worst_performing) > 0:
        best = best_performing[0]
        worst = worst_performing[0]

        if best['common_observations'] and worst['avg_conversion'] < channel_avg * 0.5:
            top_observation = best['common_observations'][0][:40]  # Truncate for readability
            steps.append(
                f"Apply {best['topic']} patterns (e.g., '{top_observation}...') to {worst['topic']} videos"
            )

    # Recommendation 3: Reconsider approach for significantly underperforming topics
    if worst_performing:
        worst = worst_performing[0]
        if worst['avg_conversion'] < channel_avg * 0.5 and worst['video_count'] >= 3:
            steps.append(
                f"Reconsider {worst['topic']} approach -- {worst['avg_conversion']:.2f}% conversion "
                f"is {((channel_avg - worst['avg_conversion']) / channel_avg * 100):.0f}% below channel average"
            )

    # Recommendation 4: Cross-topic pattern application
    if len(best_performing) >= 2:
        best1 = best_performing[0]
        best2 = best_performing[1]
        steps.append(
            f"Combine {best1['topic']} and {best2['topic']} strengths for hybrid videos"
        )

    # Recommendation 5: Flag low-confidence insights
    low_confidence_topics = [t for t in topic_stats if t['confidence'] == 'low']
    if low_confidence_topics:
        topics_list = ', '.join([t['topic'] for t in low_confidence_topics[:3]])
        steps.append(
            f"Low confidence warning: Insights for {topics_list} based on <3 videos each"
        )

    return steps


# =========================================================================
# FORMATTING FUNCTIONS
# =========================================================================

def format_strategy_terminal(strategy: Dict[str, Any]) -> str:
    """
    Format strategy as compact ASCII table for terminal display.

    Args:
        strategy: Dict from generate_topic_strategy()

    Returns:
        ASCII table string (Windows cp1252 compatible)
    """
    if 'error' in strategy:
        return f"Error: {strategy['error']}"

    lines = ['TOPIC STRATEGY', '']

    # Summary stats
    lines.append(f"Total videos: {strategy['total_videos']}")
    lines.append(f"Channel average: {strategy['channel_average_conversion']:.2f}%")
    lines.append(f"Generated: {strategy['generated_at'][:10]}")
    lines.append('')

    # Topic performance table
    lines.append(f"{'Topic':<15} {'Videos':>7} {'Avg Ret%':>9} {'Conv%':>8} {'Confidence':<10}")
    lines.append('-' * 65)

    for stat in strategy['topic_stats']:
        topic = stat['topic'][:13]
        videos = stat['video_count']
        retention = stat['avg_retention']
        conversion = stat['avg_conversion']
        confidence = stat['confidence']

        lines.append(
            f"{topic:<15} {videos:>7} {retention:>8.1f}% {conversion:>7.2f}% {confidence:<10}"
        )

    lines.append('-' * 65)
    lines.append('')

    # Next steps
    lines.append('NEXT STEPS:')
    for i, step in enumerate(strategy['concrete_next_steps'], 1):
        lines.append(f"{i}. {step}")

    lines.append('')

    return '\n'.join(lines)


def format_strategy_markdown(strategy: Dict[str, Any]) -> str:
    """
    Format strategy as full markdown report suitable for saving.

    Args:
        strategy: Dict from generate_topic_strategy()

    Returns:
        Markdown-formatted report string
    """
    if 'error' in strategy:
        return f"# Topic Strategy Error\n\n{strategy['error']}\n"

    lines = [
        '# Topic Strategy Report',
        '',
        f"**Generated:** {strategy['generated_at']}",
        f"**Total videos analyzed:** {strategy['total_videos']}",
        f"**Channel average conversion:** {strategy['channel_average_conversion']:.2f}%",
        '',
        '---',
        ''
    ]

    # Performance comparison table
    lines.append('## Performance by Topic Type')
    lines.append('')
    lines.append('| Topic | Videos | Avg Retention | Conversion | Confidence |')
    lines.append('|-------|--------|---------------|------------|------------|')

    for stat in strategy['topic_stats']:
        topic = stat['topic']
        videos = stat['video_count']
        retention = stat['avg_retention']
        conversion = stat['avg_conversion']
        confidence = stat['confidence']

        lines.append(
            f"| {topic} | {videos} | {retention:.1f}% | {conversion:.2f}% | {confidence} |"
        )

    lines.append('')

    # Best performers section
    lines.append('## Best Performing Topics')
    lines.append('')

    for stat in strategy['best_performing']:
        lines.append(f"### {stat['topic'].title()}")
        lines.append('')
        lines.append(f"**Performance:** {stat['avg_conversion']:.2f}% conversion, {stat['avg_retention']:.1f}% retention")
        lines.append(f"**Videos:** {stat['video_count']} ({stat['confidence']} confidence)")
        lines.append('')
        lines.append(f"**Best video:** {stat['best_video']['title']} ({stat['best_video']['conversion']:.2f}%)")
        lines.append('')

        if stat['common_observations']:
            lines.append('**Common patterns:**')
            for obs in stat['common_observations']:
                lines.append(f"- {obs}")
            lines.append('')

    # Worst performers section
    if strategy['worst_performing']:
        lines.append('---')
        lines.append('')
        lines.append('## Areas for Improvement')
        lines.append('')

        for stat in strategy['worst_performing']:
            lines.append(f"### {stat['topic'].title()}")
            lines.append('')
            lines.append(f"**Performance:** {stat['avg_conversion']:.2f}% conversion, {stat['avg_retention']:.1f}% retention")
            lines.append(f"**Videos:** {stat['video_count']} ({stat['confidence']} confidence)")
            lines.append('')
            lines.append(f"**Worst video:** {stat['worst_video']['title']} ({stat['worst_video']['conversion']:.2f}%)")
            lines.append('')

    # Recommendations section
    lines.append('---')
    lines.append('')
    lines.append('## Concrete Next Steps')
    lines.append('')

    for i, step in enumerate(strategy['concrete_next_steps'], 1):
        lines.append(f"{i}. {step}")

    lines.append('')

    # Confidence flags
    low_confidence = [t for t in strategy['topic_stats'] if t['confidence'] == 'low']
    if low_confidence:
        lines.append('---')
        lines.append('')
        lines.append('## Confidence Notes')
        lines.append('')
        lines.append('**Low confidence insights** (based on fewer than 3 videos):')
        lines.append('')
        for topic in low_confidence:
            lines.append(f"- **{topic['topic']}:** {topic['video_count']} video(s)")
        lines.append('')

    return '\n'.join(lines)


# =========================================================================
# CLI
# =========================================================================

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description='Generate topic strategy aggregation and recommendations',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        '--markdown',
        action='store_true',
        help='Output markdown format instead of terminal format'
    )
    parser.add_argument(
        '--save',
        action='store_true',
        help='Save markdown report to channel-data/TOPIC-STRATEGY.md'
    )

    verbosity = parser.add_mutually_exclusive_group()
    verbosity.add_argument("--verbose", "-v", action="store_true", help="Show debug output on stderr")
    verbosity.add_argument("--quiet", "-q", action="store_true", help="Only show errors on stderr")

    args = parser.parse_args()

    from tools.logging_config import setup_logging
    setup_logging(args.verbose, args.quiet)

    # Generate strategy
    strategy = generate_topic_strategy()

    if 'error' in strategy:
        print(f"Error: {strategy['error']}")
        sys.exit(1)

    # Output based on flags
    if args.save:
        # Save to channel-data/
        markdown = format_strategy_markdown(strategy)

        output_dir = Path(__file__).parent.parent.parent / 'channel-data'
        output_dir.mkdir(exist_ok=True)

        output_path = output_dir / 'TOPIC-STRATEGY.md'
        output_path.write_text(markdown, encoding='utf-8')

        print(f"Strategy report saved to: {output_path}")
        print()

        # Also print terminal format
        print(format_strategy_terminal(strategy))

    elif args.markdown:
        # Print markdown to stdout
        print(format_strategy_markdown(strategy))
    else:
        # Default: terminal format
        print(format_strategy_terminal(strategy))
