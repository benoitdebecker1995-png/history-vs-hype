"""
Pattern Extractor Module

Extracts "winning patterns" from video performance data to identify what topics,
angles, and attributes correlate with highest subscriber conversion.

Usage:
    Python:
        from pattern_extractor import (
            extract_winning_patterns,
            calculate_channel_strengths,
            generate_winning_patterns_report
        )

        # Extract complete profile
        profile = extract_winning_patterns()
        print(profile['insights'])

        # Generate and save report
        path = generate_winning_patterns_report()
        print(f"Report saved to: {path}")

    CLI (via performance.py):
        python performance.py --patterns              # Extract and display
        python performance.py --patterns --save       # Extract and save report
        python performance.py --strengths             # Show channel strengths

Dependencies:
    - database.py (Phase 15+) for KeywordDB queries
    - performance_report.py (Phase 19) for aggregate_by_topic, aggregate_by_angle
"""

import sys
import json
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter
from statistics import mean
from typing import Dict, List, Any, Optional

try:
    from tools.discovery.database import KeywordDB
    DATABASE_AVAILABLE = True
except ImportError:
    DATABASE_AVAILABLE = False

try:
    from .performance_report import aggregate_by_topic, aggregate_by_angle
    REPORT_AVAILABLE = True
except ImportError:
    REPORT_AVAILABLE = False


def extract_topic_ranking(videos: List[dict]) -> List[dict]:
    """
    Rank topics by average conversion rate.

    Groups videos by topic_type and calculates statistics for each group.

    Args:
        videos: List of video performance dicts from database

    Returns:
        List of topic stats sorted by avg_conversion DESC:
            [
                {'topic': 'territorial', 'avg_conversion': 0.85, 'count': 5, 'total_subs': 42},
                {'topic': 'colonial', 'avg_conversion': 0.62, 'count': 3, 'total_subs': 18},
                ...
            ]

    Example:
        >>> ranking = extract_topic_ranking(videos)
        >>> print(f"Best topic: {ranking[0]['topic']} ({ranking[0]['avg_conversion']:.2f}%)")
        Best topic: territorial (0.85%)
    """
    if not videos:
        return []

    # Group videos by topic
    by_topic = {}
    for video in videos:
        topic = video.get('topic_type') or 'general'
        if topic not in by_topic:
            by_topic[topic] = []
        by_topic[topic].append(video)

    # Calculate stats for each topic
    ranking = []
    for topic, topic_videos in by_topic.items():
        conversion_rates = [
            v.get('conversion_rate', 0) or 0
            for v in topic_videos
        ]
        total_subs = sum(
            v.get('subscribers_gained', 0) or 0
            for v in topic_videos
        )

        ranking.append({
            'topic': topic,
            'avg_conversion': mean(conversion_rates) if conversion_rates else 0,
            'count': len(topic_videos),
            'total_subs': total_subs
        })

    # Sort by avg_conversion descending
    ranking.sort(key=lambda x: x['avg_conversion'], reverse=True)

    return ranking


def extract_angle_ranking(videos: List[dict]) -> List[dict]:
    """
    Rank angles by average conversion rate.

    Groups videos by each angle they contain (videos can appear in multiple groups).

    Args:
        videos: List of video performance dicts from database

    Returns:
        List of angle stats sorted by avg_conversion DESC:
            [
                {'angle': 'legal', 'avg_conversion': 0.92, 'count': 4, 'total_subs': 35},
                {'angle': 'historical', 'avg_conversion': 0.71, 'count': 8, 'total_subs': 50},
                ...
            ]

    Example:
        >>> ranking = extract_angle_ranking(videos)
        >>> print(f"Best angle: {ranking[0]['angle']} ({ranking[0]['avg_conversion']:.2f}%)")
        Best angle: legal (0.92%)
    """
    if not videos:
        return []

    # Group videos by angle (video can appear in multiple groups)
    by_angle = {}
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
            if angle not in by_angle:
                by_angle[angle] = []
            by_angle[angle].append(video)

    # Calculate stats for each angle
    ranking = []
    for angle, angle_videos in by_angle.items():
        conversion_rates = [
            v.get('conversion_rate', 0) or 0
            for v in angle_videos
        ]
        total_subs = sum(
            v.get('subscribers_gained', 0) or 0
            for v in angle_videos
        )

        ranking.append({
            'angle': angle,
            'avg_conversion': mean(conversion_rates) if conversion_rates else 0,
            'count': len(angle_videos),
            'total_subs': total_subs
        })

    # Sort by avg_conversion descending
    ranking.sort(key=lambda x: x['avg_conversion'], reverse=True)

    return ranking


def extract_top_converter_profile(top_videos: List[dict], n: int = 5) -> dict:
    """
    Extract common attributes from top N converting videos.

    Analyzes the top performers to identify shared characteristics.

    Args:
        top_videos: List of video performance dicts sorted by conversion DESC
        n: Number of top videos to analyze (default 5)

    Returns:
        Profile dict with dominant attributes:
            {
                'n': 5,
                'dominant_topic': 'territorial',
                'dominant_angles': ['legal', 'historical'],
                'avg_duration_seconds': 720,
                'avg_views': 8500,
                'avg_likes_per_view': 0.04,
                'avg_comments_per_view': 0.002,
                'videos': ['Title 1', 'Title 2', ...]
            }

    Example:
        >>> profile = extract_top_converter_profile(top_videos, n=5)
        >>> print(f"Top converters are mostly {profile['dominant_topic']}")
        Top converters are mostly territorial
    """
    if not top_videos:
        return {
            'n': 0,
            'dominant_topic': None,
            'dominant_angles': [],
            'avg_duration_seconds': 0,
            'avg_views': 0,
            'avg_likes_per_view': 0,
            'avg_comments_per_view': 0,
            'videos': []
        }

    # Take top N videos
    analyzed = top_videos[:n]
    actual_n = len(analyzed)

    # Find dominant topic
    topics = [v.get('topic_type', 'general') for v in analyzed]
    topic_counter = Counter(topics)
    dominant_topic = topic_counter.most_common(1)[0][0] if topic_counter else None

    # Find dominant angles (top 2)
    all_angles = []
    for v in analyzed:
        angles = v.get('angles') or []
        if isinstance(angles, str):
            try:
                angles = json.loads(angles)
            except (json.JSONDecodeError, TypeError):
                angles = []
        all_angles.extend(angles)

    angle_counter = Counter(all_angles)
    dominant_angles = [a for a, _ in angle_counter.most_common(2)]

    # Calculate averages
    durations = [v.get('avg_view_duration_seconds', 0) or 0 for v in analyzed]
    views_list = [v.get('views', 0) or 0 for v in analyzed]
    likes_list = [v.get('likes', 0) or 0 for v in analyzed]
    comments_list = [v.get('comments', 0) or 0 for v in analyzed]

    avg_views = mean(views_list) if views_list else 0
    avg_likes = mean(likes_list) if likes_list else 0
    avg_comments = mean(comments_list) if comments_list else 0

    # Calculate engagement ratios (avoid division by zero)
    likes_per_view = avg_likes / avg_views if avg_views > 0 else 0
    comments_per_view = avg_comments / avg_views if avg_views > 0 else 0

    return {
        'n': actual_n,
        'dominant_topic': dominant_topic,
        'dominant_angles': dominant_angles,
        'avg_duration_seconds': mean(durations) if durations else 0,
        'avg_views': avg_views,
        'avg_likes_per_view': likes_per_view,
        'avg_comments_per_view': comments_per_view,
        'videos': [v.get('title', 'Unknown')[:50] for v in analyzed]
    }


def calculate_channel_strengths(topic_stats: dict, angle_stats: dict) -> dict:
    """
    Calculate channel strength scores (0-100) for key competencies.

    Scores based on how well each category performs relative to average.

    Args:
        topic_stats: Dict from aggregate_by_topic() with topic -> stats mapping
        angle_stats: Dict from aggregate_by_angle() with angle -> stats mapping

    Returns:
        Strength scores dict:
            {
                'document_heavy': 85,
                'academic': 90,
                'legal_territorial': 95
            }

        Scores normalized to 0-100 using formula:
        min(100, (category_avg / overall_avg) * 50)

    Example:
        >>> strengths = calculate_channel_strengths(topic_stats, angle_stats)
        >>> print(f"Document-heavy score: {strengths['document_heavy']}")
        Document-heavy score: 85
    """
    if not topic_stats and not angle_stats:
        return {
            'document_heavy': 0,
            'academic': 0,
            'legal_territorial': 0
        }

    # Calculate overall average conversion rate
    all_conversions = []
    for stats in topic_stats.values():
        all_conversions.append(stats.get('avg_conversion_rate', 0))
    for stats in angle_stats.values():
        all_conversions.append(stats.get('avg_conversion_rate', 0))

    overall_avg = mean(all_conversions) if all_conversions else 0.001  # Avoid division by zero

    # Document-heavy: Based on legal + historical angle performance
    legal_perf = angle_stats.get('legal', {}).get('avg_conversion_rate', 0)
    historical_perf = angle_stats.get('historical', {}).get('avg_conversion_rate', 0)
    document_combined = (legal_perf + historical_perf) / 2 if (legal_perf or historical_perf) else 0
    document_heavy = min(100, (document_combined / overall_avg) * 50) if overall_avg > 0 else 0

    # Academic: Based on ideological (fact-check/myth) topic performance
    ideological_perf = topic_stats.get('ideological', {}).get('avg_conversion_rate', 0)
    academic = min(100, (ideological_perf / overall_avg) * 50) if overall_avg > 0 else 0

    # Legal/territorial: Combined performance of both categories
    legal_topic_perf = topic_stats.get('legal', {}).get('avg_conversion_rate', 0)
    territorial_perf = topic_stats.get('territorial', {}).get('avg_conversion_rate', 0)
    legal_angle_perf = angle_stats.get('legal', {}).get('avg_conversion_rate', 0)
    geographic_perf = angle_stats.get('geographic', {}).get('avg_conversion_rate', 0)

    legal_territorial_combined = mean([
        p for p in [legal_topic_perf, territorial_perf, legal_angle_perf, geographic_perf]
        if p > 0
    ]) if any([legal_topic_perf, territorial_perf, legal_angle_perf, geographic_perf]) else 0

    legal_territorial = min(100, (legal_territorial_combined / overall_avg) * 50) if overall_avg > 0 else 0

    return {
        'document_heavy': round(document_heavy, 1),
        'academic': round(academic, 1),
        'legal_territorial': round(legal_territorial, 1)
    }


def generate_insights(
    topic_ranking: List[dict],
    angle_ranking: List[dict],
    profile: dict,
    strengths: dict
) -> List[str]:
    """
    Generate actionable insight strings from extracted patterns.

    Creates 3-5 insights comparing top performers to averages.

    Args:
        topic_ranking: Output from extract_topic_ranking()
        angle_ranking: Output from extract_angle_ranking()
        profile: Output from extract_top_converter_profile()
        strengths: Output from calculate_channel_strengths()

    Returns:
        List of insight strings:
            [
                'Territorial topics convert 1.4x better than average',
                'Legal angle correlates with 23% higher conversion',
                'Top 5 converters share legal + territorial combination',
            ]

    Example:
        >>> insights = generate_insights(topic_ranking, angle_ranking, profile, strengths)
        >>> for i in insights:
        ...     print(f"- {i}")
    """
    insights = []

    # Topic insights
    if len(topic_ranking) >= 2:
        best = topic_ranking[0]
        avg_conversion = mean([t['avg_conversion'] for t in topic_ranking])

        if avg_conversion > 0:
            ratio = best['avg_conversion'] / avg_conversion
            insights.append(
                f"{best['topic'].title()} topics convert {ratio:.1f}x better than average "
                f"({best['avg_conversion']:.2f}% vs {avg_conversion:.2f}%)"
            )

        # Compare best vs worst
        worst = topic_ranking[-1]
        if worst['avg_conversion'] > 0:
            ratio = best['avg_conversion'] / worst['avg_conversion']
            if ratio > 1.5:
                insights.append(
                    f"{best['topic'].title()} outperforms {worst['topic']} by {ratio:.1f}x"
                )

    # Angle insights
    if len(angle_ranking) >= 1:
        best_angle = angle_ranking[0]
        avg_conversion = mean([a['avg_conversion'] for a in angle_ranking])

        if avg_conversion > 0:
            pct_better = ((best_angle['avg_conversion'] / avg_conversion) - 1) * 100
            if pct_better > 10:
                insights.append(
                    f"{best_angle['angle'].title()} angle correlates with {pct_better:.0f}% higher conversion"
                )

    # Top converter profile insights
    if profile.get('dominant_topic') and profile.get('dominant_angles'):
        angles_str = ' + '.join(profile['dominant_angles'])
        insights.append(
            f"Top {profile['n']} converters share {profile['dominant_topic']} topic with {angles_str} angles"
        )

    # Strength insights
    if strengths:
        best_strength = max(strengths.items(), key=lambda x: x[1])
        if best_strength[1] > 60:
            strength_names = {
                'document_heavy': 'Document-heavy format',
                'academic': 'Academic fact-checking',
                'legal_territorial': 'Legal/territorial analysis'
            }
            insights.append(
                f"Channel excels at {strength_names.get(best_strength[0], best_strength[0])} "
                f"(strength score: {best_strength[1]:.0f}/100)"
            )

    # Sample size warning if needed
    total_videos = sum(t['count'] for t in topic_ranking)
    if total_videos < 10:
        insights.append(
            f"Note: Limited data ({total_videos} videos) - patterns may not be reliable"
        )

    return insights


def extract_winning_patterns() -> dict:
    """
    Extract complete "winning patterns" profile from performance data.

    Orchestration function that calls all extraction functions and
    combines results into comprehensive profile.

    Returns:
        Complete profile dict:
            {
                'extracted_at': '2026-02-02T12:00:00Z',
                'videos_analyzed': 20,
                'topic_ranking': [...],
                'angle_ranking': [...],
                'top_converter_profile': {...},
                'channel_strengths': {...},
                'insights': [...]
            }

        On failure: {'error': msg}

    Example:
        >>> profile = extract_winning_patterns()
        >>> if 'error' not in profile:
        ...     print(f"Analyzed {profile['videos_analyzed']} videos")
        ...     print(f"Best topic: {profile['topic_ranking'][0]['topic']}")
    """
    # Check dependencies
    if not DATABASE_AVAILABLE:
        return {'error': 'Database module not available'}

    if not REPORT_AVAILABLE:
        return {'error': 'Performance report module not available'}

    # Fetch data from database
    try:
        db = KeywordDB()
        all_videos = db.get_all_video_performance(limit=500)
        top_videos = db.get_top_converters(limit=10)
        db.close()
    except Exception as e:
        return {'error': f'Database error: {str(e)}'}

    if not all_videos:
        return {
            'error': 'No performance data found. Run `python performance.py --fetch-all` first.'
        }

    # Extract rankings
    topic_ranking = extract_topic_ranking(all_videos)
    angle_ranking = extract_angle_ranking(all_videos)

    # Get top converter profile
    top_converter_profile = extract_top_converter_profile(top_videos, n=5)

    # Aggregate for strength calculation (using performance_report functions)
    topic_stats = aggregate_by_topic(all_videos, min_count=1)
    angle_stats = aggregate_by_angle(all_videos, min_count=1)

    # Calculate channel strengths
    channel_strengths = calculate_channel_strengths(topic_stats, angle_stats)

    # Generate insights
    insights = generate_insights(
        topic_ranking,
        angle_ranking,
        top_converter_profile,
        channel_strengths
    )

    # Build complete profile
    return {
        'extracted_at': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'videos_analyzed': len(all_videos),
        'topic_ranking': topic_ranking,
        'angle_ranking': angle_ranking,
        'top_converter_profile': top_converter_profile,
        'channel_strengths': channel_strengths,
        'insights': insights
    }


def generate_winning_patterns_report() -> str:
    """
    Generate markdown report from winning patterns and save to file.

    Creates comprehensive report with all pattern data and saves to
    channel-data/patterns/WINNING-PATTERNS.md

    Returns:
        Path to saved report file on success
        Error message string on failure

    Example:
        >>> path = generate_winning_patterns_report()
        >>> print(f"Report saved to: {path}")
        Report saved to: D:/History vs Hype/channel-data/patterns/WINNING-PATTERNS.md
    """
    # Extract patterns
    profile = extract_winning_patterns()

    if 'error' in profile:
        return f"Error: {profile['error']}"

    # Build report
    lines = [
        "# Winning Patterns Report",
        "",
        f"**Extracted:** {profile['extracted_at']}",
        f"**Videos Analyzed:** {profile['videos_analyzed']}",
        "",
    ]

    # Summary section
    lines.append("## Summary")
    lines.append("")
    if profile['insights']:
        for insight in profile['insights']:
            lines.append(f"- {insight}")
    else:
        lines.append("- Insufficient data for pattern detection")
    lines.append("")

    # Topic Ranking section
    lines.append("## Topic Ranking")
    lines.append("")
    lines.append("Topics ranked by subscriber conversion rate:")
    lines.append("")
    if profile['topic_ranking']:
        lines.append("| Rank | Topic | Avg Conversion | Videos | Total Subs |")
        lines.append("|------|-------|----------------|--------|------------|")
        for i, t in enumerate(profile['topic_ranking'], 1):
            lines.append(
                f"| {i} | {t['topic']} | {t['avg_conversion']:.3f}% | "
                f"{t['count']} | {t['total_subs']} |"
            )
    else:
        lines.append("*No topic data available*")
    lines.append("")

    # Angle Ranking section
    lines.append("## Angle Ranking")
    lines.append("")
    lines.append("Content angles ranked by subscriber conversion rate:")
    lines.append("")
    if profile['angle_ranking']:
        lines.append("| Rank | Angle | Avg Conversion | Videos | Total Subs |")
        lines.append("|------|-------|----------------|--------|------------|")
        for i, a in enumerate(profile['angle_ranking'], 1):
            lines.append(
                f"| {i} | {a['angle']} | {a['avg_conversion']:.3f}% | "
                f"{a['count']} | {a['total_subs']} |"
            )
    else:
        lines.append("*No angle data available*")
    lines.append("")

    # Top Converter Profile section
    lines.append("## Top Converter Profile")
    lines.append("")
    tp = profile['top_converter_profile']
    lines.append(f"Analysis of top {tp['n']} converting videos:")
    lines.append("")
    lines.append(f"- **Dominant Topic:** {tp['dominant_topic'] or 'N/A'}")
    lines.append(f"- **Dominant Angles:** {', '.join(tp['dominant_angles']) if tp['dominant_angles'] else 'N/A'}")
    lines.append(f"- **Avg Duration:** {tp['avg_duration_seconds']:.0f} seconds")
    lines.append(f"- **Avg Views:** {tp['avg_views']:,.0f}")
    lines.append(f"- **Likes/View:** {tp['avg_likes_per_view']:.4f}")
    lines.append(f"- **Comments/View:** {tp['avg_comments_per_view']:.5f}")
    lines.append("")
    if tp['videos']:
        lines.append("**Top Videos:**")
        for v in tp['videos']:
            lines.append(f"- {v}")
    lines.append("")

    # Channel Strengths section
    lines.append("## Channel Strengths")
    lines.append("")
    lines.append("Strength scores based on performance in key competency areas:")
    lines.append("")
    cs = profile['channel_strengths']

    def strength_bar(score: float) -> str:
        """Generate ASCII bar for strength score."""
        filled = int(score / 10)
        empty = 10 - filled
        return '#' * filled + '-' * empty

    lines.append("| Strength | Score | Bar |")
    lines.append("|----------|-------|-----|")
    lines.append(f"| Document-heavy | {cs['document_heavy']:.1f} | {strength_bar(cs['document_heavy'])} |")
    lines.append(f"| Academic | {cs['academic']:.1f} | {strength_bar(cs['academic'])} |")
    lines.append(f"| Legal/Territorial | {cs['legal_territorial']:.1f} | {strength_bar(cs['legal_territorial'])} |")
    lines.append("")

    # Recommendations section
    lines.append("## Recommendations")
    lines.append("")
    if profile['topic_ranking']:
        best_topic = profile['topic_ranking'][0]
        lines.append(f"- [ ] Prioritize **{best_topic['topic']}** topics for subscriber growth")
    if profile['angle_ranking']:
        best_angle = profile['angle_ranking'][0]
        lines.append(f"- [ ] Use **{best_angle['angle']}** angle in upcoming videos")
    if tp['dominant_topic'] and tp['dominant_angles']:
        lines.append(
            f"- [ ] Combine **{tp['dominant_topic']}** topic with "
            f"**{', '.join(tp['dominant_angles'])}** angles for best results"
        )
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("*Report generated by pattern_extractor.py (Phase 20)*")

    # Save report
    project_root = Path(__file__).parent.parent.parent
    output_path = project_root / 'channel-data' / 'patterns' / 'WINNING-PATTERNS.md'

    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text('\n'.join(lines), encoding='utf-8')
        return str(output_path)
    except Exception as e:
        return f"Error saving report: {str(e)}"


if __name__ == '__main__':
    # Quick test
    print("Extracting winning patterns...")
    profile = extract_winning_patterns()

    if 'error' in profile:
        print(f"Error: {profile['error']}")
    else:
        print(f"Analyzed {profile['videos_analyzed']} videos")
        print(f"\nTop topics:")
        for t in profile['topic_ranking'][:3]:
            print(f"  - {t['topic']}: {t['avg_conversion']:.3f}%")
        print(f"\nTop angles:")
        for a in profile['angle_ranking'][:3]:
            print(f"  - {a['angle']}: {a['avg_conversion']:.3f}%")
        print(f"\nChannel strengths:")
        for k, v in profile['channel_strengths'].items():
            print(f"  - {k}: {v:.1f}")
        print(f"\nInsights:")
        for i in profile['insights']:
            print(f"  - {i}")
