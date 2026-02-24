"""
Retention-to-Script Section Mapper

Maps YouTube Analytics retention drop points (percentage-based positions)
to specific script sections using word-count-based timing estimates.

Usage:
    from retention_mapper import map_retention_to_sections

    # Get drops from retention.py
    retention_data = get_retention_data(video_id)
    drops = retention_data['drop_off_points']

    # Parse script sections
    parser = ScriptParser()
    sections = parser.parse_file('path/to/script.md')

    # Map drops to sections
    mapped = map_retention_to_sections(drops, sections)
"""

import sys
from pathlib import Path

# Import ScriptParser from production tools
sys.path.insert(0, str(Path(__file__).parent.parent / 'production'))

try:
    from parser import Section, ScriptParser
except ImportError:
    # Fallback for test environment
    from dataclasses import dataclass

    @dataclass
    class Section:
        heading: str
        content: str
        word_count: int
        start_line: int
        section_type: str


def map_retention_to_sections(drop_off_points, sections, wpm=150):
    """
    Map retention drop points to specific script sections.

    Converts YouTube's percentage-based retention positions (0.0-1.0)
    to script section boundaries using word-count-based timing.

    Args:
        drop_off_points: List of drop dicts from retention.py
            Each dict has: {position, retention_before, retention_after, drop, timestamp_hint}
        sections: List of Section objects from parser.py
            Each has: heading, content, word_count, start_line, section_type
        wpm: Words per minute speaking rate (default 150)

    Returns:
        List of mapped drop dicts:
        [
            {
                'section_heading': str,
                'section_type': str,
                'drop_position': float,
                'drop_magnitude': float,
                'retention_before': float,
                'retention_after': float,
                'word_range': (int, int),
                'estimated_timestamp': str,
                'section_content_preview': str,
                'position_in_section': float
            },
            ...
        ]

        Returns empty list on error or empty inputs.
    """
    # Handle edge cases
    if not drop_off_points or not sections:
        return []

    try:
        # Calculate total words
        total_words = sum(s.word_count for s in sections)
        if total_words == 0:
            return []

        # Calculate cumulative word percentages for each section
        cumulative = []
        running_total = 0

        for section in sections:
            start_pct = running_total / total_words
            end_pct = (running_total + section.word_count) / total_words

            cumulative.append({
                'section': section,
                'start_pct': start_pct,
                'end_pct': end_pct,
                'start_word': running_total,
                'end_word': running_total + section.word_count
            })

            running_total += section.word_count

        # Map each drop to a section
        mapped_drops = []

        for drop in drop_off_points:
            position = drop.get('position', 0)

            # Skip invalid positions
            if position < 0 or position > 1.0:
                continue

            # Find which section this drop falls in
            for item in cumulative:
                # Use <= for start to handle position at exact boundary
                if item['start_pct'] <= position < item['end_pct']:
                    section = item['section']

                    # Calculate position within section (0.0-1.0)
                    section_range = item['end_pct'] - item['start_pct']
                    if section_range > 0:
                        position_in_section = (position - item['start_pct']) / section_range
                    else:
                        position_in_section = 0.0

                    # Estimate timestamp range for section
                    start_seconds = (item['start_word'] / wpm) * 60
                    end_seconds = (item['end_word'] / wpm) * 60
                    timestamp_str = f"{_format_time(start_seconds)}-{_format_time(end_seconds)}"

                    # Get content preview (first 100 chars)
                    preview = section.content[:100] + '...' if len(section.content) > 100 else section.content

                    mapped_drops.append({
                        'section_heading': section.heading,
                        'section_type': section.section_type,
                        'drop_position': position,
                        'drop_magnitude': drop.get('drop', 0),
                        'retention_before': drop.get('retention_before', 0),
                        'retention_after': drop.get('retention_after', 0),
                        'word_range': (item['start_word'], item['end_word']),
                        'estimated_timestamp': timestamp_str,
                        'section_content_preview': preview,
                        'position_in_section': position_in_section
                    })
                    break

        return mapped_drops

    except Exception:
        # Return empty list on any error (never raise)
        return []


def estimate_section_timestamps(sections, wpm=150):
    """
    Estimate timestamp ranges for each section based on word count.

    Args:
        sections: List of Section objects
        wpm: Words per minute speaking rate (default 150)

    Returns:
        List of dicts:
        [
            {
                'heading': str,
                'start_time_str': str,  # "M:SS"
                'end_time_str': str,    # "M:SS"
                'duration_seconds': int,
                'word_count': int
            },
            ...
        ]
    """
    if not sections:
        return []

    try:
        timestamps = []
        cumulative_seconds = 0

        for section in sections:
            start_seconds = cumulative_seconds
            duration_seconds = (section.word_count / wpm) * 60
            end_seconds = start_seconds + duration_seconds

            timestamps.append({
                'heading': section.heading,
                'start_time_str': _format_time(start_seconds),
                'end_time_str': _format_time(end_seconds),
                'duration_seconds': int(duration_seconds),
                'word_count': section.word_count
            })

            cumulative_seconds = end_seconds

        return timestamps

    except Exception:
        return []


def format_mapped_drops_table(mapped_drops):
    """
    Format mapped drops as markdown table.

    Args:
        mapped_drops: List of mapped drop dicts

    Returns:
        Formatted markdown table string sorted by magnitude (biggest first).
        Columns: Section | Drop | Retention | Est. Time | Severity
        Severity: HIGH (>10%), MEDIUM (5-10%), LOW (<5%)
    """
    if not mapped_drops:
        return "No retention drops to display."

    try:
        # Sort by magnitude (biggest first)
        sorted_drops = sorted(mapped_drops, key=lambda d: d.get('drop_magnitude', 0), reverse=True)

        # Build table
        lines = []
        lines.append("| Section | Drop | Retention | Est. Time | Severity |")
        lines.append("|---------|------|-----------|-----------|----------|")

        for drop in sorted_drops:
            section = drop.get('section_heading', 'Unknown')
            magnitude = drop.get('drop_magnitude', 0)
            before = drop.get('retention_before', 0)
            after = drop.get('retention_after', 0)
            timestamp = drop.get('estimated_timestamp', 'N/A')

            # Calculate severity
            if magnitude > 0.10:
                severity = 'HIGH'
            elif magnitude >= 0.05:
                severity = 'MEDIUM'
            else:
                severity = 'LOW'

            # Format retention change
            retention_str = f"{before:.1%} → {after:.1%}"
            drop_str = f"{magnitude:.1%}"

            lines.append(f"| {section} | {drop_str} | {retention_str} | {timestamp} | {severity} |")

        return '\n'.join(lines)

    except Exception:
        return "Error formatting drops table."


def _format_time(seconds):
    """
    Format seconds as M:SS timestamp.

    Args:
        seconds: Time in seconds

    Returns:
        String like "1:30", "5:45", "12:00"
    """
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes}:{secs:02d}"


if __name__ == '__main__':
    # Example usage
    print("Retention Mapper Module")
    print("Usage: from retention_mapper import map_retention_to_sections")
