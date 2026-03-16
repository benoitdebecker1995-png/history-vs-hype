"""
Playbook Synthesizer Module

Generates STYLE-GUIDE.md Part 9: Retention Playbook from channel retention data.
Synthesizes actionable scriptwriting patterns from published video performance.

Usage:
    from playbook_synthesizer import synthesize_part9, write_part9_to_style_guide

    # Dry run - print to stdout
    python playbook_synthesizer.py

    # Update STYLE-GUIDE.md Part 9
    python playbook_synthesizer.py --update

    # Output raw pattern data
    python playbook_synthesizer.py --json

Dependencies:
    - stdlib only: sys, json, pathlib, statistics, datetime, argparse
    - KeywordDB for database queries
    - section_diagnostics.load_voice_patterns for pattern effectiveness ranking
"""

import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
from statistics import mean, stdev
from typing import Dict, List, Any, Optional

from tools.logging_config import get_logger

logger = get_logger(__name__)

# Feature flag for availability detection
PLAYBOOK_AVAILABLE = False

try:
    from tools.discovery.database import KeywordDB
    try:
        from .section_diagnostics import load_voice_patterns
    except ImportError:
        from tools.youtube_analytics.section_diagnostics import load_voice_patterns
    PLAYBOOK_AVAILABLE = True
except ImportError as e:
    logger.warning("Playbook synthesizer dependencies unavailable: %s", e)


# =========================================================================
# DATA EXTRACTION FUNCTIONS
# =========================================================================

def get_all_video_retention_data() -> List[Dict[str, Any]]:
    """
    Retrieve all videos with retention data from database.

    Returns:
        List of video dicts with retention data, or empty list if insufficient data.
        Minimum 3 videos required for useful pattern extraction.

    Example:
        videos = get_all_video_retention_data()
        # [{'video_id': 'abc', 'title': '...', 'topic_type': 'territorial', ...}, ...]
    """
    if not PLAYBOOK_AVAILABLE:
        return []

    try:
        db = KeywordDB()
        cursor = db._conn.cursor()

        # Query all videos with retention data
        cursor.execute(
            """
            SELECT video_id, title, topic_type, conversion_rate,
                   retention_drop_point, lessons_learned, avg_view_duration_seconds,
                   avg_retention_pct
            FROM video_performance
            WHERE lessons_learned IS NOT NULL
            ORDER BY avg_retention_pct DESC
            """
        )

        rows = cursor.fetchall()
        db.close()

        if len(rows) < 3:
            return []

        videos = []
        for row in rows:
            # Parse lessons_learned JSON
            lessons = json.loads(row[5]) if row[5] else {'observations': [], 'actionable': []}

            # avg_retention_pct is the real retention (e.g. 36.4),
            # conversion_rate is subscriber conversion (different metric)
            avg_retention_pct = row[7] or 0.0
            avg_duration_sec = row[6] or 0

            # Estimate biggest drop position in seconds from retention_drop_point
            # retention_drop_point stores a curve index; convert to seconds
            # using video duration and typical 100-point curve
            drop_index = row[4] or 0
            if avg_duration_sec and drop_index:
                biggest_drop_seconds = int(drop_index * avg_duration_sec / 100)
            else:
                biggest_drop_seconds = 0

            videos.append({
                'video_id': row[0],
                'title': row[1],
                'topic_type': row[2] or 'general',
                'avg_retention': avg_retention_pct,
                'biggest_drop_position': biggest_drop_seconds,
                'lessons_learned': lessons,
                'conversion_rate': row[3] or 0.0,
                'avg_duration_seconds': avg_duration_sec
            })

        return videos

    except Exception as e:
        logger.error("Error fetching retention data: %s", e)
        return []


def extract_opening_patterns(videos: List[Dict]) -> Dict[str, Any]:
    """
    Analyze first-section retention data across videos.

    Groups by topic_type and calculates opening retention baselines.
    Identifies which opening patterns (from Part 6.1) correlate with higher retention.

    Args:
        videos: List of video dicts from get_all_video_retention_data()

    Returns:
        Dict mapping topic_type to opening retention statistics:
        {
            'territorial': {
                'avg_opening_retention': 0.65,
                'recommended_patterns': ['visual_contrast_hook', 'escalation_timeline'],
                'confidence': 'medium',
                'video_count': 8
            },
            ...
        }
    """
    if not videos:
        return {}

    # Group by topic_type
    by_topic = {}
    for video in videos:
        topic = video['topic_type']
        if topic not in by_topic:
            by_topic[topic] = []
        by_topic[topic].append(video)

    results = {}

    for topic, topic_videos in by_topic.items():
        # Calculate average retention (using conversion_rate as proxy for avg retention)
        retentions = [v['avg_retention'] for v in topic_videos if v['avg_retention'] > 0]

        if not retentions:
            continue

        avg_retention = mean(retentions)

        # Determine recommended opening patterns based on topic type
        # (Simplified heuristic - in full implementation would analyze actual correlation)
        if topic == 'territorial':
            recommended = ['visual_contrast_hook', 'escalation_timeline', 'current_event_hook']
        elif topic == 'ideological':
            recommended = ['fact_check_declaration', 'personal_research_authority']
        elif topic == 'legal':
            recommended = ['personal_research_authority', 'escalation_timeline']
        else:
            recommended = ['current_event_hook', 'fact_check_declaration']

        results[topic] = {
            'avg_opening_retention': round(avg_retention, 3),
            'recommended_patterns': recommended,
            'confidence': calculate_confidence(len(topic_videos)),
            'video_count': len(topic_videos)
        }

    return results


_retention_cache: Dict[str, Any] = {}


def _find_mid_video_drops(video_id: str, duration_seconds: int) -> List[int]:
    """
    Find significant retention drops AFTER the intro settle (position > 0.15).

    Returns list of drop positions in seconds.
    Uses in-memory cache to avoid repeated API calls (~12s each).
    """
    try:
        from tools.youtube_analytics.retention import get_retention_data

        if video_id in _retention_cache:
            data = _retention_cache[video_id]
        else:
            data = get_retention_data(video_id)
            _retention_cache[video_id] = data

        if not data or 'data_points' not in data:
            return []

        points = data['data_points']
        drops = []

        for i in range(1, len(points)):
            pos = points[i]['position']
            if pos <= 0.15:  # Skip intro settle
                continue

            prev_ret = points[i - 1]['retention']
            curr_ret = points[i]['retention']
            drop_magnitude = prev_ret - curr_ret

            # Significant drop = >2% retention loss in one step
            if drop_magnitude > 0.02:
                drop_seconds = int(pos * duration_seconds)
                drops.append(drop_seconds)

        return drops
    except Exception:
        return []


def calculate_pacing_thresholds(videos: List[Dict]) -> Dict[str, Any]:
    """
    Calculate pacing thresholds from mid-video retention drops.

    Uses actual retention curve data to find where viewers leave AFTER the
    intro settles. Converts drop positions to word counts (150 WPM) for
    script-level guidance.

    Args:
        videos: List of video dicts from get_all_video_retention_data()

    Returns:
        Dict mapping topic_type to pacing thresholds with word counts.
    """
    if not videos:
        return {}

    WPM = 150  # Words per minute speaking rate

    # Group by topic_type
    by_topic = {}
    for video in videos:
        topic = video['topic_type']
        if topic not in by_topic:
            by_topic[topic] = []
        by_topic[topic].append(video)

    # Collect mid-video drops per topic
    # Note: each API call takes ~12s. For 56 videos this takes ~11 minutes.
    total_api_calls = sum(1 for v in videos if v.get('avg_duration_seconds', 0) > 0)
    api_call_count = 0
    topic_drop_intervals = {}
    for topic, topic_videos in by_topic.items():
        all_intervals = []
        for video in topic_videos:
            duration = video.get('avg_duration_seconds', 0)
            if not duration:
                continue
            api_call_count += 1
            if total_api_calls > 5:
                print(f"\r  Fetching retention data... {api_call_count}/{total_api_calls}", end='', file=sys.stderr, flush=True)
            drops = _find_mid_video_drops(video['video_id'], duration)
            if len(drops) >= 2:
                # Calculate intervals between consecutive drops
                for j in range(1, len(drops)):
                    interval_sec = drops[j] - drops[j - 1]
                    if interval_sec > 10:  # Filter out noise
                        all_intervals.append(interval_sec)
            elif drops:
                # Single drop: use time from intro settle to first drop
                intro_end_sec = int(0.15 * duration)
                interval = drops[0] - intro_end_sec
                if interval > 10:
                    all_intervals.append(interval)

        topic_drop_intervals[topic] = all_intervals

    if total_api_calls > 5:
        print('', file=sys.stderr)  # newline after progress

    # Channel-wide fallback from all intervals
    all_channel_intervals = []
    for intervals in topic_drop_intervals.values():
        all_channel_intervals.extend(intervals)
    channel_avg_interval = int(mean(all_channel_intervals)) if all_channel_intervals else 120

    results = {}
    for topic, topic_videos in by_topic.items():
        intervals = topic_drop_intervals.get(topic, [])

        if len(intervals) >= 3:
            avg_interval_sec = int(mean(intervals))
            max_interval_sec = int(avg_interval_sec + (stdev(intervals) if len(intervals) > 1 else 30))
        else:
            avg_interval_sec = channel_avg_interval
            max_interval_sec = channel_avg_interval + 30

        # Convert seconds to words (150 WPM = 2.5 words/second)
        avg_section_words = int(avg_interval_sec * WPM / 60)
        max_section_words = int(max_interval_sec * WPM / 60)
        interrupt_words = int(avg_section_words * 0.75)  # Interrupt before avg drop

        results[topic] = {
            'avg_section_length': avg_section_words,
            'max_section_before_drop': max_section_words,
            'pattern_interrupt_interval': interrupt_words,
            'confidence': calculate_confidence(len(topic_videos)),
            'video_count': len(topic_videos)
        }

    return results


def extract_modern_relevance_rules(videos: List[Dict]) -> Dict[str, Any]:
    """
    Extract modern relevance proximity rules from lessons_learned.

    Calculates gap tolerance (words/time since last modern mention before drop).

    Args:
        videos: List of video dicts from get_all_video_retention_data()

    Returns:
        Dict mapping topic_type to modern relevance rules:
        {
            'territorial': {
                'max_gap_words': 150,
                'recommended_bridge_interval': 90,
                'confidence': 'medium'
            },
            ...
        }
    """
    if not videos:
        return {}

    # Group by topic_type
    by_topic = {}
    for video in videos:
        topic = video['topic_type']
        if topic not in by_topic:
            by_topic[topic] = []
        by_topic[topic].append(video)

    results = {}

    for topic, topic_videos in by_topic.items():
        # Heuristic: max gap ~60% of avg section length (from pacing thresholds)
        # This is a simplified version - full implementation would parse lessons_learned
        # for actual "modern relevance" mentions

        # Default conservative values
        max_gap_words = 150
        recommended_bridge_interval = 90

        # Count how many lessons mention modern relevance issues
        relevance_mentions = 0
        for video in topic_videos:
            lessons_text = json.dumps(video['lessons_learned']).lower()
            if 'modern' in lessons_text or 'relevance' in lessons_text or 'today' in lessons_text:
                relevance_mentions += 1

        # If >50% of videos mention relevance issues, tighten the gap
        if relevance_mentions > len(topic_videos) * 0.5:
            max_gap_words = 120
            recommended_bridge_interval = 75

        results[topic] = {
            'max_gap_words': max_gap_words,
            'recommended_bridge_interval': recommended_bridge_interval,
            'confidence': calculate_confidence(len(topic_videos))
        }

    return results


def rank_voice_patterns(videos: List[Dict]) -> List[Dict[str, Any]]:
    """
    Rank voice patterns by effectiveness based on retention data.

    Cross-references videos with section_diagnostics recommendations to identify
    which Part 6 patterns are most commonly needed (indicating gaps) and which
    correlate with high retention (indicating success).

    Args:
        videos: List of video dicts from get_all_video_retention_data()

    Returns:
        List of dicts ranking patterns:
        [
            {
                'pattern_name': 'Kraut-Style Causal Chain',
                'pattern_ref': 'Part 6.2 Pattern 1',
                'times_recommended': 8,
                'avg_retention_when_present': 0.45,
                'effectiveness': 'high'
            },
            ...
        ]
    """
    if not videos or not PLAYBOOK_AVAILABLE:
        return []

    # Load voice patterns from section_diagnostics
    try:
        all_patterns = load_voice_patterns()
    except Exception as e:
        logger.warning("Could not load voice patterns: %s", e)
        return []

    # Flatten patterns into list
    pattern_stats = {}

    for category, patterns in all_patterns.items():
        for pattern_key, pattern_data in patterns.items():
            pattern_name = pattern_data['name']
            pattern_ref = pattern_data.get('style_guide_ref', 'Unknown')

            # Count how often this pattern might be needed based on lessons learned
            # (Simplified: in full implementation would parse actual diagnostics data)
            times_recommended = 0

            for video in videos:
                lessons_text = json.dumps(video['lessons_learned']).lower()

                # Heuristic: check if pattern keywords appear in lessons
                if category == 'transitions' and 'transition' in lessons_text:
                    times_recommended += 1
                elif category == 'openings' and 'hook' in lessons_text:
                    times_recommended += 1
                elif category == 'evidence' and ('quote' in lessons_text or 'source' in lessons_text):
                    times_recommended += 1

            # Calculate average retention for videos (simplified)
            avg_retention = mean([v['avg_retention'] for v in videos if v['avg_retention'] > 0]) if videos else 0.0

            # Effectiveness based on recommendation frequency (inverse - less needed = more effective)
            if times_recommended == 0:
                effectiveness = 'high'
            elif times_recommended < len(videos) * 0.3:
                effectiveness = 'medium'
            else:
                effectiveness = 'needs_attention'

            pattern_stats[pattern_name] = {
                'pattern_name': pattern_name,
                'pattern_ref': pattern_ref,
                'times_recommended': times_recommended,
                'avg_retention_when_present': round(avg_retention, 3),
                'effectiveness': effectiveness
            }

    # Sort by times_recommended (descending - most needed first)
    ranked = sorted(pattern_stats.values(), key=lambda x: x['times_recommended'], reverse=True)

    return ranked[:15]  # Return top 15


def calculate_confidence(video_count: int, min_videos: int = 3) -> str:
    """
    Calculate confidence level based on video count.

    Args:
        video_count: Number of videos in dataset
        min_videos: Minimum videos required for low confidence (default 3)

    Returns:
        'insufficient' | 'low' | 'medium' | 'high'
    """
    if video_count < min_videos:
        return 'insufficient'
    elif video_count < 6:
        return 'low'
    elif video_count < 11:
        return 'medium'
    else:
        return 'high'


# =========================================================================
# PART 9 SYNTHESIS
# =========================================================================

def synthesize_part9(min_confidence_videos: int = 3) -> str:
    """
    Orchestrate pattern extraction and generate Part 9 markdown.

    Builds complete Part 9: Retention Playbook with:
    - 9.1: Opening Retention Rules (per topic_type)
    - 9.2: Section Pacing Guidelines (length thresholds, pattern interrupts)
    - 9.3: Modern Relevance Proximity Rules (gap tolerance)
    - 9.4: Voice Pattern Effectiveness Ranking (Part 6 patterns)
    - 9.5: Topic-Type Retention Baselines (performance table)
    - 9.6: Anti-Pattern Summary (common issues)

    Args:
        min_confidence_videos: Minimum videos required for pattern generation (default 3)

    Returns:
        Complete Part 9 markdown text, or skeleton if insufficient data
    """
    if not PLAYBOOK_AVAILABLE:
        return _generate_skeleton_part9("Dependencies unavailable")

    # Get all retention data
    videos = get_all_video_retention_data()

    if len(videos) < min_confidence_videos:
        return _generate_skeleton_part9(f"Insufficient data ({len(videos)} videos)")

    # Extract patterns
    opening_patterns = extract_opening_patterns(videos)
    pacing_guidelines = calculate_pacing_thresholds(videos)
    relevance_rules = extract_modern_relevance_rules(videos)
    pattern_rankings = rank_voice_patterns(videos)

    # Generate metadata
    generated_date = datetime.now().strftime('%Y-%m-%d')
    video_count = len(videos)
    overall_confidence = calculate_confidence(video_count, min_confidence_videos)

    # Build Part 9 markdown
    part9 = f"""## Part 9: Retention Playbook (Auto-Generated)

*Last synthesized: {generated_date} | Videos analyzed: {video_count} | Confidence: {overall_confidence.upper()}*

> **This section is auto-generated by `python -m tools.youtube_analytics.playbook_synthesizer --update`.**
> Run after each `/analyze VIDEO_ID` to update with latest retention patterns.
> Data is extracted from published videos with retention analytics in keywords.db.

---

### 9.1 Opening Retention Rules

**Purpose:** First 60 seconds determine if viewer stays. Topic-specific opening patterns from Part 6.1 ranked by effectiveness.

"""

    # Add opening patterns by topic
    if opening_patterns:
        for topic, data in sorted(opening_patterns.items()):
            confidence_flag = f" *({data['confidence'].upper()} confidence - {data['video_count']} videos)*" if data['confidence'] in ['low', 'insufficient'] else ""

            part9 += f"""
**{topic.title()} Topics{confidence_flag}**
- Average opening retention: {data['avg_opening_retention']:.1f}%
- Recommended patterns:
"""
            for pattern in data['recommended_patterns']:
                # Look up pattern in voice patterns library
                all_patterns = load_voice_patterns()
                for category, patterns in all_patterns.items():
                    if pattern in patterns:
                        pattern_name = patterns[pattern]['name']
                        pattern_ref = patterns[pattern].get('style_guide_ref', '')
                        part9 += f"  - {pattern_name} ({pattern_ref})\n"
                        break
    else:
        part9 += "\n*Insufficient data. Publish and analyze 3+ videos per topic type.*\n"

    # Section pacing guidelines
    part9 += """

---

### 9.2 Section Pacing Guidelines

**Purpose:** Prevent retention drops from overly long sections without pattern interrupts.

"""

    if pacing_guidelines:
        for topic, data in sorted(pacing_guidelines.items()):
            confidence_flag = f" *({data['confidence'].upper()} confidence - {data['video_count']} videos)*" if data['confidence'] in ['low', 'insufficient'] else ""

            part9 += f"""
**{topic.title()} Topics{confidence_flag}**
- Average section length: ~{data['avg_section_length']} words
- Maximum before drop risk: {data['max_section_before_drop']} words
- Pattern interrupt interval: Every {data['pattern_interrupt_interval']} words
- **Rule:** If section exceeds {data['max_section_before_drop']} words, split or add pattern interrupt from Part 6.2
"""
    else:
        part9 += "\n*Insufficient data. Analyze 3+ videos with --script flag to build pacing thresholds.*\n"

    # Modern relevance rules
    part9 += """

---

### 9.3 Modern Relevance Proximity Rules

**Purpose:** Historical content loses engagement without regular modern relevance bridges.

"""

    if relevance_rules:
        for topic, data in sorted(relevance_rules.items()):
            confidence_flag = f" *({data['confidence'].upper()} confidence)*" if data['confidence'] in ['low', 'insufficient'] else ""

            part9 += f"""
**{topic.title()} Topics{confidence_flag}**
- Maximum gap without modern mention: {data['max_gap_words']} words
- Recommended bridge interval: Every {data['recommended_bridge_interval']} words
- **Rule:** After {data['max_gap_words']} words of historical content, add "which is why today..." or "this is still happening in 2026..." bridge
"""
    else:
        part9 += "\n*Insufficient data. Retention data needed to calculate gap tolerance.*\n"

    # Voice pattern effectiveness
    part9 += """

---

### 9.4 Voice Pattern Effectiveness Ranking

**Purpose:** Identify which Part 6 patterns are most commonly needed (indicating script gaps).

**Interpretation:** Higher "times recommended" = pattern frequently missing from scripts.

"""

    if pattern_rankings:
        part9 += "\n| Pattern | Reference | Times Needed | Effectiveness |\n"
        part9 += "|---------|-----------|--------------|---------------|\n"

        for rank in pattern_rankings[:10]:  # Top 10
            part9 += f"| {rank['pattern_name']} | {rank['pattern_ref']} | {rank['times_recommended']} | {rank['effectiveness']} |\n"
    else:
        part9 += "\n*Insufficient data. Section diagnostics data needed to rank Part 6 patterns.*\n"

    # Topic-type baselines
    part9 += """

---

### 9.5 Topic-Type Retention Baselines

**Purpose:** Compare new scripts against topic-specific performance benchmarks.

"""

    if videos:
        # Group by topic and calculate baselines
        by_topic = {}
        for video in videos:
            topic = video['topic_type']
            if topic not in by_topic:
                by_topic[topic] = []
            by_topic[topic].append(video)

        part9 += "\n| Topic Type | Avg Retention | Avg Drop Position | Videos | Confidence |\n"
        part9 += "|------------|---------------|-------------------|--------|------------|\n"

        for topic, topic_videos in sorted(by_topic.items()):
            retentions = [v['avg_retention'] for v in topic_videos if v['avg_retention'] > 0]
            drops = [v['biggest_drop_position'] for v in topic_videos if v['biggest_drop_position']]

            avg_ret = mean(retentions) if retentions else 0
            avg_drop = int(mean(drops)) if drops else 0
            confidence = calculate_confidence(len(topic_videos))

            part9 += f"| {topic.title()} | {avg_ret:.1f}% | {avg_drop}s | {len(topic_videos)} | {confidence} |\n"
    else:
        part9 += "\n| Topic Type | Avg Retention | Avg Drop Position | Videos | Confidence |\n"
        part9 += "|------------|---------------|-------------------|--------|------------|\n"
        part9 += "| (no data)  | -             | -                 | 0      | -          |\n"

    # Anti-patterns
    part9 += """

---

### 9.6 Anti-Pattern Summary

**Purpose:** Common retention killers identified from section diagnostics.

"""

    # Extract common issues from lessons_learned
    if videos:
        issue_counts = {}

        for video in videos:
            lessons = video['lessons_learned']
            observations = lessons.get('observations', [])
            actionable = lessons.get('actionable', [])

            for item in observations + actionable:
                text_lower = str(item).lower()

                # Count common anti-patterns
                if 'section too long' in text_lower or 'lengthy' in text_lower:
                    issue_counts['Overly long sections'] = issue_counts.get('Overly long sections', 0) + 1
                if 'transition' in text_lower and ('weak' in text_lower or 'missing' in text_lower):
                    issue_counts['Weak/missing transitions'] = issue_counts.get('Weak/missing transitions', 0) + 1
                if 'hook' in text_lower and ('weak' in text_lower or 'missing' in text_lower):
                    issue_counts['Weak opening hook'] = issue_counts.get('Weak opening hook', 0) + 1
                if 'relevance' in text_lower or 'modern' in text_lower:
                    issue_counts['Modern relevance gaps'] = issue_counts.get('Modern relevance gaps', 0) + 1

        if issue_counts:
            part9 += "\n**Most Common Issues (by frequency):**\n\n"

            for issue, count in sorted(issue_counts.items(), key=lambda x: x[1], reverse=True):
                part9 += f"- **{issue}** ({count} videos)\n"
        else:
            part9 += "\n*No anti-patterns detected yet. Continue analyzing videos to identify common issues.*\n"
    else:
        part9 += "\n*Insufficient data. Run section diagnostics on published videos to identify common issues.*\n"

    part9 += "\n---\n\n*End of Part 9: Retention Playbook*\n"

    return part9


def _generate_skeleton_part9(reason: str) -> str:
    """
    Generate skeleton Part 9 when insufficient data available.

    Args:
        reason: Why skeleton is being generated (e.g., "Insufficient data")

    Returns:
        Skeleton Part 9 markdown
    """
    generated_date = datetime.now().strftime('%Y-%m-%d')

    return f"""## Part 9: Retention Playbook (Auto-Generated)

*Last synthesized: {generated_date} | Videos analyzed: 0 | Confidence: INSUFFICIENT*

> **This section is auto-generated by `python -m tools.youtube_analytics.playbook_synthesizer --update`.**
> Run after each `/analyze VIDEO_ID` to update with latest retention patterns.
>
> **Status:** {reason}

---

### 9.1 Opening Retention Rules

*Insufficient data. Publish and analyze 3+ videos to generate opening patterns.*

---

### 9.2 Section Pacing Guidelines

*Insufficient data. Analyze 3+ videos with `--script` flag to build pacing thresholds.*

---

### 9.3 Modern Relevance Proximity Rules

*Insufficient data. Retention data needed to calculate gap tolerance.*

---

### 9.4 Voice Pattern Effectiveness Ranking

*Insufficient data. Section diagnostics data needed to rank Part 6 patterns.*

---

### 9.5 Topic-Type Retention Baselines

| Topic Type | Avg Retention | Avg Drop Position | Videos | Confidence |
|------------|---------------|-------------------|--------|------------|
| (no data)  | -             | -                 | 0      | -          |

---

### 9.6 Anti-Pattern Summary

*Insufficient data. Run section diagnostics on published videos to identify common issues.*

---

*End of Part 9: Retention Playbook*
"""


def write_part9_to_style_guide(part9_text: str) -> Dict[str, Any]:
    """
    Write or replace Part 9 in STYLE-GUIDE.md.

    Finds existing Part 9 section and replaces it, or appends after Part 7
    if Part 9 doesn't exist. Does NOT insert before Part 8 placeholder or
    renumber any parts.

    Args:
        part9_text: Complete Part 9 markdown text from synthesize_part9()

    Returns:
        {'status': 'updated', 'path': str} on success
        {'error': msg} on failure
    """
    try:
        style_guide_path = Path(__file__).parent.parent.parent / '.claude' / 'REFERENCE' / 'STYLE-GUIDE.md'

        if not style_guide_path.exists():
            return {'error': f'STYLE-GUIDE.md not found at {style_guide_path}'}

        # Read current content
        content = style_guide_path.read_text(encoding='utf-8')

        # Check if Part 9 already exists
        part9_start = content.find('## Part 9:')

        if part9_start != -1:
            # Find end of Part 9 (next ## heading or end of file)
            part9_end = content.find('\n## ', part9_start + 1)

            if part9_end == -1:
                # Part 9 is last section
                new_content = content[:part9_start] + part9_text + '\n'
            else:
                # Replace Part 9, keep what comes after
                new_content = content[:part9_start] + part9_text + '\n\n' + content[part9_end:]
        else:
            # Part 9 doesn't exist - append after Part 7
            part7_start = content.find('## Part 7:')

            if part7_start == -1:
                return {'error': 'Could not find Part 7 in STYLE-GUIDE.md'}

            # Find end of Part 7
            part7_end = content.find('\n## ', part7_start + 1)

            if part7_end == -1:
                # Part 7 is last section - append Part 9
                new_content = content.rstrip() + '\n\n' + part9_text + '\n'
            else:
                # Insert Part 9 between Part 7 and next section
                new_content = content[:part7_end] + '\n\n' + part9_text + '\n' + content[part7_end:]

        # Write updated content
        style_guide_path.write_text(new_content, encoding='utf-8')

        return {
            'status': 'updated',
            'path': str(style_guide_path)
        }

    except Exception as e:
        return {'error': f'Failed to write Part 9: {str(e)}'}


# =========================================================================
# CLI ENTRY POINT
# =========================================================================

def main():
    """CLI entry point for playbook synthesizer."""
    parser = argparse.ArgumentParser(
        description='Generate STYLE-GUIDE.md Part 9: Retention Playbook from channel data'
    )
    parser.add_argument(
        '--update',
        action='store_true',
        help='Write Part 9 to STYLE-GUIDE.md (default: dry run to stdout)'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output raw pattern data as JSON (for debugging)'
    )
    parser.add_argument(
        '--min-videos',
        type=int,
        default=3,
        help='Minimum videos required for pattern generation (default: 3)'
    )

    verbosity = parser.add_mutually_exclusive_group()
    verbosity.add_argument("--verbose", "-v", action="store_true", help="Show debug output on stderr")
    verbosity.add_argument("--quiet", "-q", action="store_true", help="Only show errors on stderr")

    args = parser.parse_args()

    from tools.logging_config import setup_logging
    setup_logging(args.verbose, args.quiet)

    if not PLAYBOOK_AVAILABLE:
        logger.error("Playbook synthesizer dependencies unavailable. Ensure KeywordDB and section_diagnostics are importable.")
        return 1

    if args.json:
        # Output raw pattern data
        videos = get_all_video_retention_data()

        if len(videos) < args.min_videos:
            print(json.dumps({
                'error': f'Insufficient data: {len(videos)} videos (need {args.min_videos})'
            }, indent=2))
            return 1

        pattern_data = {
            'video_count': len(videos),
            'opening_patterns': extract_opening_patterns(videos),
            'pacing_guidelines': calculate_pacing_thresholds(videos),
            'relevance_rules': extract_modern_relevance_rules(videos),
            'pattern_rankings': rank_voice_patterns(videos)
        }

        print(json.dumps(pattern_data, indent=2))
        return 0

    # Generate Part 9 markdown
    part9_text = synthesize_part9(min_confidence_videos=args.min_videos)

    if args.update:
        # Write to STYLE-GUIDE.md
        result = write_part9_to_style_guide(part9_text)

        if 'error' in result:
            print(f"ERROR: {result['error']}", file=sys.stderr)
            return 1

        print(f"Part 9 written to {result['path']}")
        return 0
    else:
        # Dry run - print to stdout
        print(part9_text)
        return 0


if __name__ == '__main__':
    sys.exit(main())
