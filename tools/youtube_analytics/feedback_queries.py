"""
Feedback Query Module

Retrieves and formats insights from past video performance feedback.
Supports topic-specific queries, universal insights, and success/failure pattern extraction.

Usage:
    from feedback_queries import get_insights_preamble, extract_success_patterns

    # Get preamble for /script command
    preamble = get_insights_preamble('territorial', 'script')

    # Extract patterns
    success = extract_success_patterns()
    failure = extract_failure_patterns()

Dependencies:
    - stdlib only: sys, json, pathlib, statistics, typing
    - KeywordDB for database queries
    - pattern_extractor (optional) for integration
"""

import sys
import json
from pathlib import Path
from datetime import datetime, timezone
from statistics import mean
from typing import Dict, List, Any, Optional

from tools.discovery.database import KeywordDB

# Optional pattern_extractor integration
try:
    from .pattern_extractor import extract_winning_patterns
    PATTERN_EXTRACTOR_AVAILABLE = True
except ImportError:
    PATTERN_EXTRACTOR_AVAILABLE = False

# Optional topic_strategy integration
try:
    from .topic_strategy import generate_topic_strategy
    TOPIC_STRATEGY_AVAILABLE = True
except ImportError:
    TOPIC_STRATEGY_AVAILABLE = False


# =========================================================================
# INSIGHT RETRIEVAL FUNCTIONS
# =========================================================================

def get_insights_for_topic(topic_type: str, command: str = 'script', limit: int = 5) -> dict:
    """
    Retrieve category-specific insights from videos matching topic_type.

    Filters insights by command type:
    - 'script': Content and pacing insights (retention, hooks, structure)
    - 'prep': Production insights (B-roll, edit pacing, visual evidence)
    - 'publish': CTR and title insights (thumbnails, metadata, impressions)

    Args:
        topic_type: Topic category (territorial, ideological, legal, colonial, general)
        command: Command context for filtering ('script', 'prep', 'publish')
        limit: Maximum number of insights to return

    Returns:
        Dict with insights list, count, topic, and command
    """
    db = KeywordDB()
    result = db.get_feedback_by_topic(topic_type, limit=limit)
    db.close()

    if 'error' in result:
        return {'insights': [], 'count': 0, 'topic': topic_type, 'command': command}

    videos = result.get('videos', [])

    # Filter keywords by command type
    if command == 'script':
        filter_keywords = ['retention', 'pacing', 'hook', 'section', 'structure',
                          'opening', 'engagement', 'drop', 'flow', 'transition']
    elif command == 'prep':
        filter_keywords = ['b-roll', 'visual', 'edit', 'production', 'thumbnail',
                          'footage', 'asset', 'timing', 'cut', 'evidence']
    elif command == 'publish':
        filter_keywords = ['ctr', 'title', 'thumbnail', 'impressions', 'click',
                          'metadata', 'description', 'tag', 'discovery']
    else:
        filter_keywords = []  # No filter, return all

    insights = []
    for video in videos:
        video_id = video.get('video_id', '')
        title = video.get('title', 'Unknown')
        conversion_rate = video.get('conversion_rate', 0) or 0
        lessons = video.get('lessons_learned', {})

        observations = lessons.get('observations', [])

        # Apply keyword filter
        filtered_observations = []
        for obs in observations:
            obs_lower = obs.lower()
            # If no filter keywords, include all
            if not filter_keywords:
                filtered_observations.append(obs)
            # Otherwise, check if observation contains any keyword
            elif any(keyword in obs_lower for keyword in filter_keywords):
                filtered_observations.append(obs)

        # If filtering resulted in nothing, include all observations as fallback
        if not filtered_observations and observations:
            filtered_observations = observations[:2]  # First 2 as fallback

        # Add each observation as separate insight
        for obs in filtered_observations[:2]:  # Max 2 per video
            insights.append({
                'video_id': video_id,
                'title': title,
                'observation': obs,
                'conversion_rate': conversion_rate
            })

    return {
        'insights': insights[:limit],
        'count': len(insights[:limit]),
        'topic': topic_type,
        'command': command
    }


def get_universal_insights(limit: int = 2) -> dict:
    """
    Retrieve insights that apply to ALL videos regardless of topic.

    Looks for universal patterns: pacing, engagement, conversion, average.
    Prioritizes high-performing videos.

    Args:
        limit: Maximum number of universal insights to return

    Returns:
        Dict with insights list and count
    """
    db = KeywordDB()

    # Get all videos with feedback, sorted by conversion rate
    cursor = db._conn.cursor()
    cursor.execute("""
        SELECT video_id, title, conversion_rate, lessons_learned
        FROM video_performance
        WHERE lessons_learned IS NOT NULL
        ORDER BY conversion_rate DESC
    """)

    rows = cursor.fetchall()
    db.close()

    if not rows:
        return {'insights': [], 'count': 0}

    # Look for universal patterns
    universal_keywords = ['pacing', 'engagement', 'conversion', 'average',
                         'retention', 'hook', 'structure', 'overall']

    insights = []
    for row in rows:
        video_id = row['video_id']
        title = row['title']
        conversion_rate = row['conversion_rate'] or 0
        lessons_raw = row['lessons_learned']

        if not lessons_raw:
            continue

        lessons = json.loads(lessons_raw) if lessons_raw else {}
        observations = lessons.get('observations', [])

        # Look for universal observations
        for obs in observations:
            obs_lower = obs.lower()
            if any(keyword in obs_lower for keyword in universal_keywords):
                insights.append({
                    'video_id': video_id,
                    'title': title,
                    'observation': obs,
                    'conversion_rate': conversion_rate
                })
                break  # One per video

        if len(insights) >= limit:
            break

    return {
        'insights': insights[:limit],
        'count': len(insights[:limit])
    }


def get_insights_preamble(topic_type: str, command: str = 'script') -> str:
    """
    Generate formatted preamble combining topic-specific and universal insights.

    This is what /script, /prep, /publish commands will call to show
    relevant past performance insights before generation.

    Args:
        topic_type: Topic category
        command: Command context ('script', 'prep', 'publish')

    Returns:
        Formatted preamble text, or empty string if no insights available
    """
    topic_insights = get_insights_for_topic(topic_type, command, limit=4)
    universal_insights = get_universal_insights(limit=2)

    if topic_insights['count'] == 0 and universal_insights['count'] == 0:
        return ''

    lines = ['--- Past Performance Insights ---', '']

    # Topic-specific insights
    if topic_insights['count'] > 0:
        lines.append(f"From similar videos ({topic_type}):")
        for insight in topic_insights['insights']:
            title = insight['title']
            obs = insight['observation']
            conv = insight['conversion_rate']
            lines.append(f"- [{title}]: {obs} (conversion: {conv:.2f}%)")
        lines.append('')

    # Universal patterns
    if universal_insights['count'] > 0:
        lines.append("Universal patterns:")
        for insight in universal_insights['insights']:
            obs = insight['observation']
            lines.append(f"- {obs}")
        lines.append('')

    lines.append('---')

    return '\n'.join(lines)


# =========================================================================
# PATTERN EXTRACTION FUNCTIONS
# =========================================================================

def _calculate_threshold(videos: List[dict], topic_type: Optional[str] = None) -> tuple:
    """
    Calculate performance threshold adaptively.

    Strategy:
    - Topic-specific average if topic has 3+ videos
    - Channel-wide average otherwise

    Args:
        videos: List of video performance dicts
        topic_type: Optional topic to calculate topic-specific threshold

    Returns:
        Tuple of (threshold_value, method_name)
    """
    if topic_type:
        topic_videos = [v for v in videos if v.get('topic_type') == topic_type]
        if len(topic_videos) >= 3:
            rates = [v.get('conversion_rate', 0) or 0 for v in topic_videos]
            try:
                return mean(rates), 'topic_average'
            except:
                pass  # Fall through to channel average

    # Fallback to channel average
    rates = [v.get('conversion_rate', 0) or 0 for v in videos if v.get('conversion_rate')]
    if rates:
        try:
            return mean(rates), 'channel_average'
        except:
            pass

    return 0.0, 'default'


def extract_success_patterns(threshold_type: str = 'adaptive') -> dict:
    """
    Extract patterns from high-performing videos.

    Uses adaptive threshold: above-average conversion per topic_type,
    falling back to channel average if topic has <3 videos.

    Args:
        threshold_type: 'adaptive' (only supported option)

    Returns:
        Dict with patterns list, video_count, threshold, and method
    """
    db = KeywordDB()

    # Get all videos with feedback
    cursor = db._conn.cursor()
    cursor.execute("""
        SELECT video_id, title, topic_type, conversion_rate,
               retention_drop_point, discovery_issues, lessons_learned
        FROM video_performance
        WHERE lessons_learned IS NOT NULL
        ORDER BY conversion_rate DESC
    """)

    rows = cursor.fetchall()
    db.close()

    if not rows:
        return {'patterns': [], 'video_count': 0, 'threshold': 0, 'method': 'no_data'}

    # Convert rows to dicts
    videos = []
    for row in rows:
        video = dict(row)
        # Parse JSON columns
        if video.get('discovery_issues'):
            video['discovery_issues'] = json.loads(video['discovery_issues'])
        if video.get('lessons_learned'):
            video['lessons_learned'] = json.loads(video['lessons_learned'])
        videos.append(video)

    # Calculate threshold
    threshold, method = _calculate_threshold(videos)

    # Filter high-performers
    high_performers = [v for v in videos if (v.get('conversion_rate') or 0) >= threshold]

    if not high_performers:
        return {'patterns': [], 'video_count': 0, 'threshold': threshold, 'method': method}

    # Extract patterns
    patterns = []

    # Content attributes: dominant topics
    topic_counter = {}
    for video in high_performers:
        topic = video.get('topic_type', 'general')
        topic_counter[topic] = topic_counter.get(topic, 0) + 1

    for topic, count in topic_counter.items():
        if count >= 2:  # Appears in at least 2 videos
            video_titles = [v['title'] for v in high_performers if v.get('topic_type') == topic]
            patterns.append({
                'type': 'success',
                'attribute': 'topic_type',
                'value': topic,
                'frequency': count,
                'videos': video_titles[:3]  # First 3
            })

    # Content attributes: common observations
    observation_counter = {}
    for video in high_performers:
        lessons = video.get('lessons_learned', {})
        observations = lessons.get('observations', [])
        for obs in observations:
            # Extract key phrases (first 50 chars)
            key = obs[:50].strip()
            if key not in observation_counter:
                observation_counter[key] = {'count': 0, 'videos': []}
            observation_counter[key]['count'] += 1
            observation_counter[key]['videos'].append(video['title'])

    for obs_key, data in observation_counter.items():
        if data['count'] >= 2:
            patterns.append({
                'type': 'success',
                'attribute': 'observation',
                'value': obs_key,
                'frequency': data['count'],
                'videos': data['videos'][:3]
            })

    # Production attributes: retention (low drop = good)
    good_retention_videos = [v for v in high_performers if (v.get('retention_drop_point') or 100) > 50]
    if len(good_retention_videos) >= 2:
        patterns.append({
            'type': 'success',
            'attribute': 'retention',
            'value': 'sustained_retention',
            'frequency': len(good_retention_videos),
            'videos': [v['title'] for v in good_retention_videos[:3]]
        })

    return {
        'patterns': patterns,
        'video_count': len(high_performers),
        'threshold': threshold,
        'method': method
    }


def extract_failure_patterns(threshold_type: str = 'adaptive') -> dict:
    """
    Extract patterns from low-performing videos.

    Uses adaptive threshold: below-average conversion per topic_type,
    falling back to channel average if topic has <3 videos.

    Args:
        threshold_type: 'adaptive' (only supported option)

    Returns:
        Dict with patterns list, video_count, threshold, and method
    """
    db = KeywordDB()

    # Get all videos with feedback
    cursor = db._conn.cursor()
    cursor.execute("""
        SELECT video_id, title, topic_type, conversion_rate,
               retention_drop_point, discovery_issues, lessons_learned
        FROM video_performance
        WHERE lessons_learned IS NOT NULL
        ORDER BY conversion_rate ASC
    """)

    rows = cursor.fetchall()
    db.close()

    if not rows:
        return {'patterns': [], 'video_count': 0, 'threshold': 0, 'method': 'no_data'}

    # Convert rows to dicts
    videos = []
    for row in rows:
        video = dict(row)
        # Parse JSON columns
        if video.get('discovery_issues'):
            video['discovery_issues'] = json.loads(video['discovery_issues'])
        if video.get('lessons_learned'):
            video['lessons_learned'] = json.loads(video['lessons_learned'])
        videos.append(video)

    # Calculate threshold
    threshold, method = _calculate_threshold(videos)

    # Filter low-performers
    low_performers = [v for v in videos if (v.get('conversion_rate') or 0) < threshold]

    if not low_performers:
        return {'patterns': [], 'video_count': 0, 'threshold': threshold, 'method': method}

    # Extract patterns
    patterns = []

    # Content attributes: common observations (likely negative)
    observation_counter = {}
    for video in low_performers:
        lessons = video.get('lessons_learned', {})
        observations = lessons.get('observations', [])
        for obs in observations:
            # Extract key phrases
            key = obs[:50].strip()
            if key not in observation_counter:
                observation_counter[key] = {'count': 0, 'videos': []}
            observation_counter[key]['count'] += 1
            observation_counter[key]['videos'].append(video['title'])

    for obs_key, data in observation_counter.items():
        if data['count'] >= 2:
            patterns.append({
                'type': 'failure',
                'attribute': 'observation',
                'value': obs_key,
                'frequency': data['count'],
                'videos': data['videos'][:3]
            })

    # Production attributes: early retention drops
    early_drop_videos = [v for v in low_performers if (v.get('retention_drop_point') or 100) <= 30]
    if len(early_drop_videos) >= 2:
        patterns.append({
            'type': 'failure',
            'attribute': 'retention',
            'value': 'early_drop',
            'frequency': len(early_drop_videos),
            'videos': [v['title'] for v in early_drop_videos[:3]]
        })

    # Discovery issues
    discovery_issue_counter = {}
    for video in low_performers:
        discovery = video.get('discovery_issues')
        if discovery and discovery.get('primary_issue'):
            issue = discovery['primary_issue']
            if issue not in discovery_issue_counter:
                discovery_issue_counter[issue] = {'count': 0, 'videos': []}
            discovery_issue_counter[issue]['count'] += 1
            discovery_issue_counter[issue]['videos'].append(video['title'])

    for issue, data in discovery_issue_counter.items():
        if data['count'] >= 1:  # Even 1 is worth noting
            patterns.append({
                'type': 'failure',
                'attribute': 'discovery',
                'value': issue,
                'frequency': data['count'],
                'videos': data['videos'][:3]
            })

    return {
        'patterns': patterns,
        'video_count': len(low_performers),
        'threshold': threshold,
        'method': method
    }


def generate_patterns_report() -> dict:
    """
    Generate comprehensive patterns report combining success, failure, and winning patterns.

    Integrates with pattern_extractor if available.

    Returns:
        Dict with success, failure, winning patterns, and timestamp
    """
    success = extract_success_patterns()
    failure = extract_failure_patterns()

    # Integrate with pattern_extractor if available
    winning = None
    if PATTERN_EXTRACTOR_AVAILABLE:
        try:
            winning = extract_winning_patterns()
        except:
            winning = None

    return {
        'success': success,
        'failure': failure,
        'winning': winning,
        'generated_at': datetime.now(timezone.utc).isoformat()
    }


# =========================================================================
# PRE-SCRIPT INSIGHT SURFACING
# =========================================================================

def get_pre_script_insights(topic_type: str, limit: int = 5) -> dict:
    """
    Get comprehensive pre-script insights combining multiple sources.

    Surfaces retention lessons, topic strategy summary, and pattern suggestions
    BEFORE /script generation. Replaces get_insights_preamble for /script context.

    Args:
        topic_type: Topic category (territorial, ideological, colonial, legal, general)
        limit: Max number of past videos to reference for retention lessons

    Returns:
        Dict with structured insights:
            {
                'topic_type': str,
                'video_count': int,
                'confidence': 'high' | 'medium' | 'low',
                'retention_lessons': [
                    {
                        'lesson': 'Lost 12% viewers at treaty text section',
                        'recommendation': 'Show treaty on screen, don\'t read aloud',
                        'source_video': 'Belize (2025-01-15)',
                        'drop_magnitude': 0.12
                    }
                ],
                'topic_strategy_summary': str,
                'pattern_suggestions': [str],
                'display_text': str
            }
    """
    # Get topic-specific feedback
    topic_insights = get_insights_for_topic(topic_type, command='script', limit=limit)
    video_count = topic_insights.get('count', 0)

    # Determine confidence based on video count
    if video_count >= 5:
        confidence = 'high'
    elif video_count >= 3:
        confidence = 'medium'
    else:
        confidence = 'low'

    # Extract retention lessons from topic insights
    retention_lessons = []
    for insight in topic_insights.get('insights', []):
        observation = insight.get('observation', '')
        video_title = insight.get('title', 'Unknown')

        # Parse retention-related observations
        # Look for patterns like "lost X%", "drop", "retention", etc.
        if any(kw in observation.lower() for kw in ['lost', 'drop', 'retention', 'viewers left']):
            # Try to extract drop magnitude if present
            drop_magnitude = 0.0
            obs_lower = observation.lower()
            # Simple regex-free extraction: look for "XX%" patterns
            words = obs_lower.replace('%', ' % ').split()
            for i, word in enumerate(words):
                if word == '%' and i > 0:
                    try:
                        drop_magnitude = float(words[i-1]) / 100
                        break
                    except:
                        pass

            # Extract recommendation if present (after "should", "could", "try")
            recommendation = ''
            for marker in [' should ', ' could ', ' try ', ' recommend ']:
                if marker in obs_lower:
                    parts = observation.split(marker, 1)
                    if len(parts) > 1:
                        recommendation = parts[1].strip()
                        break

            if not recommendation:
                recommendation = 'Review section for engagement issues'

            retention_lessons.append({
                'lesson': observation,
                'recommendation': recommendation,
                'source_video': video_title,
                'drop_magnitude': drop_magnitude
            })

    # Get topic strategy summary if available
    topic_strategy_summary = ''
    if TOPIC_STRATEGY_AVAILABLE:
        try:
            strategy = generate_topic_strategy()
            if 'error' not in strategy:
                # Find stats for this topic type
                for stat in strategy.get('topic_stats', []):
                    if stat['topic'] == topic_type:
                        topic_strategy_summary = (
                            f"{topic_type}: {stat['avg_conversion']:.2f}% conversion, "
                            f"{stat['avg_retention']:.1f}% retention "
                            f"({stat['confidence']} confidence, {stat['video_count']} videos)"
                        )
                        break
        except:
            pass  # Fail gracefully

    # Generate pattern suggestions based on topic type
    pattern_suggestions = _generate_pattern_suggestions(topic_type, retention_lessons)

    # Build display text
    display_text = format_pre_script_display({
        'topic_type': topic_type,
        'video_count': video_count,
        'confidence': confidence,
        'retention_lessons': retention_lessons[:3],  # Top 3
        'topic_strategy_summary': topic_strategy_summary,
        'pattern_suggestions': pattern_suggestions
    })

    return {
        'topic_type': topic_type,
        'video_count': video_count,
        'confidence': confidence,
        'retention_lessons': retention_lessons,
        'topic_strategy_summary': topic_strategy_summary,
        'pattern_suggestions': pattern_suggestions,
        'display_text': display_text
    }


def _generate_pattern_suggestions(topic_type: str, retention_lessons: List[dict]) -> List[str]:
    """
    Generate pattern suggestions based on topic type and retention lessons.

    Args:
        topic_type: Video topic category
        retention_lessons: List of retention lesson dicts

    Returns:
        List of pattern suggestion strings
    """
    suggestions = []

    # Topic-specific pattern suggestions (referencing STYLE-GUIDE.md Part 6)
    topic_patterns = {
        'territorial': [
            'Use zero-impact moments for dramatic numerical reveals (STYLE-GUIDE Part 6.4 Pattern 2)',
            'Show treaties/maps on screen rather than describing (STYLE-GUIDE Part 3)'
        ],
        'ideological': [
            'Apply intellectual honesty pattern when addressing opposing views (STYLE-GUIDE Part 6.2 Pattern 1)',
            'Use causal chains to show historical consequences (STYLE-GUIDE Part 6.1 Pattern 3)'
        ],
        'legal': [
            'Display legal documents as primary evidence (STYLE-GUIDE Part 3)',
            'Use precise legal terminology with immediate definitions (STYLE-GUIDE Part 6.1 Pattern 5)'
        ],
        'colonial': [
            'Emphasize causal chains between colonial actions and modern consequences (STYLE-GUIDE Part 6.1 Pattern 3)',
            'Use comparative framing to show patterns across regions (STYLE-GUIDE Part 6.3 Pattern 1)'
        ]
    }

    # Add topic-specific patterns
    if topic_type in topic_patterns:
        suggestions.extend(topic_patterns[topic_type][:2])  # Max 2 per topic

    # Add retention-driven suggestions
    if retention_lessons:
        # Check for common drop patterns
        early_drops = [l for l in retention_lessons if l['drop_magnitude'] > 0.10]
        if early_drops:
            suggestions.append(
                'Consider adding pattern interrupt (rhetorical question, document reveal) '
                'to prevent early viewer drop (STYLE-GUIDE Part 6.4)'
            )

    return suggestions[:3]  # Max 3 suggestions


def format_pre_script_display(insights: dict) -> str:
    """
    Format pre-script insights as compact, readable block for display.

    Args:
        insights: Dict with topic_type, confidence, retention_lessons,
                 topic_strategy_summary, pattern_suggestions

    Returns:
        Pre-formatted text block ready to display, or empty string if no insights
    """
    topic = insights.get('topic_type', 'unknown')
    confidence = insights.get('confidence', 'low')
    video_count = insights.get('video_count', 0)
    retention_lessons = insights.get('retention_lessons', [])
    strategy_summary = insights.get('topic_strategy_summary', '')
    pattern_suggestions = insights.get('pattern_suggestions', [])

    # If no data, return empty
    if not (retention_lessons or strategy_summary or pattern_suggestions):
        return ''

    lines = [
        f"--- Pre-Script Intelligence ({topic}, {confidence} confidence) ---",
        ''
    ]

    # Topic performance summary
    if strategy_summary:
        lines.append(f"Topic Performance: {strategy_summary}")
        lines.append('')

    # Retention lessons
    if retention_lessons:
        lines.append(f"Retention Lessons ({video_count} past video{'s' if video_count != 1 else ''}):")
        for lesson in retention_lessons:
            source = lesson.get('source_video', 'Unknown')
            observation = lesson.get('lesson', '')[:80]  # Truncate
            recommendation = lesson.get('recommendation', '')[:60]
            lines.append(f"- [{source}]: {observation}")
            if recommendation:
                lines.append(f"  -> {recommendation}")
        lines.append('')

    # Pattern suggestions
    if pattern_suggestions:
        lines.append('Suggested Patterns:')
        for suggestion in pattern_suggestions:
            lines.append(f"- {suggestion}")
        lines.append('')

    lines.append('---')

    return '\n'.join(lines)


# =========================================================================
# FORMATTING FUNCTIONS
# =========================================================================

def format_patterns_markdown(report: dict) -> str:
    """
    Format patterns report as markdown for saving to PATTERNS.md.

    Args:
        report: Dict from generate_patterns_report()

    Returns:
        Markdown-formatted report string
    """
    lines = [
        '# Feedback Patterns Report',
        '',
        f"**Generated:** {report['generated_at']}",
        '',
        '---',
        ''
    ]

    # Success Patterns
    success = report.get('success', {})
    lines.append('## Success Patterns')
    lines.append('')

    if success.get('patterns'):
        lines.append(f"**High-performers:** {success['video_count']} videos above {success['threshold']:.2f}% conversion ({success['method']})")
        lines.append('')

        for pattern in success['patterns']:
            attr = pattern['attribute']
            value = pattern['value']
            freq = pattern['frequency']
            videos = pattern['videos']

            lines.append(f"### {attr.title()}: {value}")
            lines.append(f"**Frequency:** {freq} videos")
            lines.append('')
            lines.append('**Videos:**')
            for video in videos:
                lines.append(f"- {video}")
            lines.append('')
    else:
        lines.append('No success patterns identified yet (need more feedback data).')
        lines.append('')

    # Failure Patterns
    failure = report.get('failure', {})
    lines.append('---')
    lines.append('')
    lines.append('## Failure Patterns')
    lines.append('')

    if failure.get('patterns'):
        lines.append(f"**Low-performers:** {failure['video_count']} videos below {failure['threshold']:.2f}% conversion ({failure['method']})")
        lines.append('')

        for pattern in failure['patterns']:
            attr = pattern['attribute']
            value = pattern['value']
            freq = pattern['frequency']
            videos = pattern['videos']

            lines.append(f"### {attr.title()}: {value}")
            lines.append(f"**Frequency:** {freq} videos")
            lines.append('')
            lines.append('**Videos:**')
            for video in videos:
                lines.append(f"- {video}")
            lines.append('')
    else:
        lines.append('No failure patterns identified.')
        lines.append('')

    # Winning Patterns (from pattern_extractor)
    winning = report.get('winning')
    if winning:
        lines.append('---')
        lines.append('')
        lines.append('## Winning Patterns (Performance Data)')
        lines.append('')
        lines.append('*From pattern_extractor.py analysis*')
        lines.append('')

        insights = winning.get('insights', [])
        for insight in insights:
            lines.append(f"- {insight}")
        lines.append('')

    # Recommendations
    lines.append('---')
    lines.append('')
    lines.append('## Recommendations')
    lines.append('')

    if success.get('patterns'):
        lines.append('**Double down on:**')
        for pattern in success['patterns'][:3]:
            lines.append(f"- {pattern['attribute']}: {pattern['value']} ({pattern['frequency']} videos)")
        lines.append('')

    if failure.get('patterns'):
        lines.append('**Avoid:**')
        for pattern in failure['patterns'][:3]:
            lines.append(f"- {pattern['attribute']}: {pattern['value']} ({pattern['frequency']} videos)")
        lines.append('')

    return '\n'.join(lines)


def format_patterns_terminal(report: dict) -> str:
    """
    Format patterns report for terminal display (compact version).

    Args:
        report: Dict from generate_patterns_report()

    Returns:
        Terminal-formatted report string (ASCII only)
    """
    lines = ['FEEDBACK PATTERNS', '']

    # Success Patterns
    success = report.get('success', {})
    lines.append(f"SUCCESS PATTERNS ({success.get('video_count', 0)} high-performers):")

    if success.get('patterns'):
        for pattern in success['patterns'][:5]:
            attr = pattern['attribute']
            value = pattern['value'][:40]  # Truncate
            freq = pattern['frequency']
            lines.append(f"  [{attr}] {value} (x{freq})")
    else:
        lines.append('  None identified yet')

    lines.append('')

    # Failure Patterns
    failure = report.get('failure', {})
    lines.append(f"FAILURE PATTERNS ({failure.get('video_count', 0)} low-performers):")

    if failure.get('patterns'):
        for pattern in failure['patterns'][:5]:
            attr = pattern['attribute']
            value = pattern['value'][:40]  # Truncate
            freq = pattern['frequency']
            lines.append(f"  [!] [{attr}] {value} (x{freq})")
    else:
        lines.append('  None identified')

    lines.append('')

    # Winning Patterns summary
    winning = report.get('winning')
    if winning:
        insights = winning.get('insights', [])
        if insights:
            lines.append(f"WINNING PATTERNS: {len(insights)} insights")
            lines.append('')

    return '\n'.join(lines)


def format_query_terminal(result: dict) -> str:
    """
    Format query results for terminal display.

    Args:
        result: Dict from get_insights_for_topic() or get_video_feedback()

    Returns:
        Terminal-formatted table string
    """
    if 'insights' in result:
        # Topic query result
        insights = result['insights']
        if not insights:
            return f"No insights found for topic: {result.get('topic', 'unknown')}"

        lines = [
            f"INSIGHTS FOR {result.get('topic', '').upper()} ({result.get('count', 0)} found)",
            ''
        ]

        for insight in insights:
            title = insight['title'][:40]  # Truncate
            obs = insight['observation'][:80]  # Truncate
            conv = insight['conversion_rate']
            lines.append(f"{title}")
            lines.append(f"  {obs}")
            lines.append(f"  Conversion: {conv:.2f}%")
            lines.append('')

        return '\n'.join(lines)

    elif 'video_id' in result:
        # Single video result
        lines = [
            f"VIDEO FEEDBACK: {result.get('video_id', '')}",
            f"Title: {result.get('title', '')}",
            f"Topic: {result.get('topic_type', '')}",
            f"Conversion: {result.get('conversion_rate', 0):.2f}%",
            ''
        ]

        lessons = result.get('lessons_learned', {})
        observations = lessons.get('observations', [])

        if observations:
            lines.append('Observations:')
            for obs in observations:
                lines.append(f"  - {obs}")
            lines.append('')

        actionable = lessons.get('actionable', [])
        if actionable:
            lines.append('Actionable Items:')
            for item in actionable:
                lines.append(f"  - {item}")
            lines.append('')

        return '\n'.join(lines)

    else:
        return 'Unknown result format'


def format_query_markdown(result: dict) -> str:
    """
    Format query results as markdown report.

    Args:
        result: Dict from get_insights_for_topic() or get_video_feedback()

    Returns:
        Markdown-formatted report string
    """
    if 'insights' in result:
        # Topic query result
        insights = result['insights']
        topic = result.get('topic', 'unknown')
        command = result.get('command', '')

        lines = [
            f"# Insights for {topic.title()} Videos",
            '',
            f"**Command context:** {command}",
            f"**Results:** {result.get('count', 0)} insights",
            '',
            '---',
            ''
        ]

        for insight in insights:
            title = insight['title']
            video_id = insight['video_id']
            obs = insight['observation']
            conv = insight['conversion_rate']

            lines.append(f"## {title}")
            lines.append(f"**Video ID:** {video_id}")
            lines.append(f"**Conversion:** {conv:.2f}%")
            lines.append('')
            lines.append(obs)
            lines.append('')

        return '\n'.join(lines)

    elif 'video_id' in result:
        # Single video result
        lines = [
            f"# Video Feedback: {result.get('title', 'Unknown')}",
            '',
            f"**Video ID:** {result.get('video_id', '')}",
            f"**Topic:** {result.get('topic_type', '')}",
            f"**Conversion:** {result.get('conversion_rate', 0):.2f}%",
            '',
            '---',
            ''
        ]

        lessons = result.get('lessons_learned', {})

        observations = lessons.get('observations', [])
        if observations:
            lines.append('## Observations')
            lines.append('')
            for obs in observations:
                lines.append(f"- {obs}")
            lines.append('')

        actionable = lessons.get('actionable', [])
        if actionable:
            lines.append('## Actionable Items')
            lines.append('')
            for item in actionable:
                lines.append(f"- {item}")
            lines.append('')

        discovery = result.get('discovery_issues')
        if discovery:
            lines.append('## Discovery Issues')
            lines.append('')
            lines.append(f"**Primary Issue:** {discovery.get('primary_issue', 'Unknown')}")
            lines.append(f"**Severity:** {discovery.get('severity', 'Unknown')}")
            if discovery.get('summary'):
                lines.append(f"**Summary:** {discovery['summary']}")
            lines.append('')

        return '\n'.join(lines)

    else:
        return '# Unknown Result Format\n'


if __name__ == '__main__':
    # CLI testing
    print("Feedback Queries Module - Test")
    print()

    # Test insights
    preamble = get_insights_preamble('territorial', 'script')
    print("Preamble length:", len(preamble))
    print()

    # Test patterns
    success = extract_success_patterns()
    print(f"Success patterns: {success.get('video_count', 0)} high-performers")
    print(f"  Patterns found: {len(success.get('patterns', []))}")
    print()

    failure = extract_failure_patterns()
    print(f"Failure patterns: {failure.get('video_count', 0)} low-performers")
    print(f"  Patterns found: {len(failure.get('patterns', []))}")
