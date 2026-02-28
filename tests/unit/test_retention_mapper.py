"""
Tests for retention_mapper.py

Tests retention-to-script section mapping without API calls.
"""

import pytest
from dataclasses import dataclass


# Mock Section class (mirrors parser.py Section)
@dataclass
class MockSection:
    """Mock Section object for testing"""
    heading: str
    content: str
    word_count: int
    start_line: int
    section_type: str


class TestMapRetentionToSections:
    """Test retention drop mapping to script sections"""

    def test_single_section_single_drop(self):
        """Single drop in single section"""
        from tools.youtube_analytics.retention_mapper import map_retention_to_sections

        sections = [
            MockSection(
                heading="Introduction",
                content="This is the introduction section with about fifty words of content.",
                word_count=100,
                start_line=1,
                section_type="intro"
            )
        ]

        drops = [
            {
                'position': 0.5,  # Middle of video
                'retention_before': 0.80,
                'retention_after': 0.70,
                'drop': 0.10,
                'timestamp_hint': 'first half'
            }
        ]

        result = map_retention_to_sections(drops, sections)

        assert len(result) == 1
        assert result[0]['section_heading'] == 'Introduction'
        assert result[0]['drop_position'] == 0.5
        assert result[0]['drop_magnitude'] == 0.10
        assert result[0]['section_type'] == 'intro'
        assert result[0]['word_range'] == (0, 100)
        assert 'estimated_timestamp' in result[0]
        assert 'section_content_preview' in result[0]

    def test_multi_section_multi_drop(self):
        """Multiple drops across multiple sections"""
        from tools.youtube_analytics.retention_mapper import map_retention_to_sections

        sections = [
            MockSection("Introduction", "Intro content...", 100, 1, "intro"),
            MockSection("Background", "Background content...", 200, 10, "body"),
            MockSection("Analysis", "Analysis content...", 150, 25, "body"),
            MockSection("Conclusion", "Conclusion content...", 50, 40, "conclusion")
        ]
        # Total: 500 words
        # Section boundaries: 0-0.2, 0.2-0.6, 0.6-0.9, 0.9-1.0

        drops = [
            {'position': 0.15, 'retention_before': 0.95, 'retention_after': 0.88, 'drop': 0.07, 'timestamp_hint': 'early'},
            {'position': 0.35, 'retention_before': 0.85, 'retention_after': 0.72, 'drop': 0.13, 'timestamp_hint': 'first half'}
        ]

        result = map_retention_to_sections(drops, sections)

        assert len(result) == 2
        # First drop in Introduction (0-0.2)
        assert result[0]['section_heading'] == 'Introduction'
        assert result[0]['drop_position'] == 0.15
        # Second drop in Background (0.2-0.6)
        assert result[1]['section_heading'] == 'Background'
        assert result[1]['drop_position'] == 0.35

    def test_drop_at_section_boundary(self):
        """Drop exactly at section boundary"""
        from tools.youtube_analytics.retention_mapper import map_retention_to_sections

        sections = [
            MockSection("First", "Content A", 100, 1, "intro"),
            MockSection("Second", "Content B", 100, 10, "body")
        ]
        # Boundary at 0.5

        drops = [
            {'position': 0.5, 'retention_before': 0.80, 'retention_after': 0.70, 'drop': 0.10, 'timestamp_hint': 'first half'}
        ]

        result = map_retention_to_sections(drops, sections)

        assert len(result) == 1
        # Should map to second section (position at start of second section)
        assert result[0]['section_heading'] == 'Second'

    def test_empty_drops_list(self):
        """Empty drops list returns empty result"""
        from tools.youtube_analytics.retention_mapper import map_retention_to_sections

        sections = [MockSection("Test", "Content", 100, 1, "intro")]
        drops = []

        result = map_retention_to_sections(drops, sections)

        assert result == []

    def test_empty_sections_list(self):
        """Empty sections list returns empty result"""
        from tools.youtube_analytics.retention_mapper import map_retention_to_sections

        sections = []
        drops = [{'position': 0.5, 'retention_before': 0.80, 'retention_after': 0.70, 'drop': 0.10, 'timestamp_hint': 'first half'}]

        result = map_retention_to_sections(drops, sections)

        assert result == []

    def test_drop_outside_section_boundaries(self):
        """Drop position outside any section boundary is skipped"""
        from tools.youtube_analytics.retention_mapper import map_retention_to_sections

        sections = [
            MockSection("Introduction", "Content", 100, 1, "intro")
        ]
        # Section covers 0.0-1.0, so drop at 1.5 is invalid

        drops = [
            {'position': 1.5, 'retention_before': 0.80, 'retention_after': 0.70, 'drop': 0.10, 'timestamp_hint': 'conclusion'}
        ]

        result = map_retention_to_sections(drops, sections)

        # Invalid position should be skipped
        assert len(result) == 0

    def test_position_in_section_calculation(self):
        """Position within section calculated correctly"""
        from tools.youtube_analytics.retention_mapper import map_retention_to_sections

        sections = [
            MockSection("Introduction", "Content", 200, 1, "intro"),
            MockSection("Body", "More content", 200, 10, "body")
        ]
        # Total 400 words: Intro 0-0.5, Body 0.5-1.0

        drops = [
            {'position': 0.75, 'retention_before': 0.80, 'retention_after': 0.70, 'drop': 0.10, 'timestamp_hint': 'second half'}
        ]

        result = map_retention_to_sections(drops, sections)

        assert len(result) == 1
        # Drop at 0.75 in Body section (0.5-1.0)
        # Position within section: (0.75 - 0.5) / (1.0 - 0.5) = 0.5
        assert result[0]['position_in_section'] == 0.5


class TestEstimateSectionTimestamps:
    """Test section timestamp estimation"""

    def test_single_section_timestamp(self):
        """Single section timestamp calculation"""
        from tools.youtube_analytics.retention_mapper import estimate_section_timestamps

        sections = [
            MockSection("Introduction", "Content", 150, 1, "intro")
        ]
        # 150 words at 150 WPM = 1 minute

        result = estimate_section_timestamps(sections, wpm=150)

        assert len(result) == 1
        assert result[0]['heading'] == 'Introduction'
        assert result[0]['start_time_str'] == '0:00'
        assert result[0]['end_time_str'] == '1:00'
        assert result[0]['duration_seconds'] == 60
        assert result[0]['word_count'] == 150

    def test_multi_section_timestamps(self):
        """Multiple sections with cumulative timing"""
        from tools.youtube_analytics.retention_mapper import estimate_section_timestamps

        sections = [
            MockSection("Introduction", "Content", 75, 1, "intro"),    # 0:00-0:30
            MockSection("Body", "Content", 150, 10, "body"),           # 0:30-1:30
            MockSection("Conclusion", "Content", 75, 20, "conclusion") # 1:30-2:00
        ]

        result = estimate_section_timestamps(sections, wpm=150)

        assert len(result) == 3
        assert result[0]['start_time_str'] == '0:00'
        assert result[0]['end_time_str'] == '0:30'
        assert result[1]['start_time_str'] == '0:30'
        assert result[1]['end_time_str'] == '1:30'
        assert result[2]['start_time_str'] == '1:30'
        assert result[2]['end_time_str'] == '2:00'

    def test_timestamp_formatting(self):
        """Timestamp formatting M:SS"""
        from tools.youtube_analytics.retention_mapper import estimate_section_timestamps

        sections = [
            MockSection("Long", "Content", 900, 1, "body")  # 6 minutes
        ]

        result = estimate_section_timestamps(sections, wpm=150)

        assert result[0]['start_time_str'] == '0:00'
        assert result[0]['end_time_str'] == '6:00'


class TestFormatMappedDropsTable:
    """Test markdown table formatting"""

    def test_format_table_output(self):
        """Format mapped drops as markdown table"""
        from tools.youtube_analytics.retention_mapper import format_mapped_drops_table

        mapped_drops = [
            {
                'section_heading': 'Introduction',
                'drop_magnitude': 0.12,
                'retention_before': 0.90,
                'retention_after': 0.78,
                'estimated_timestamp': '0:00-1:30',
                'section_type': 'intro'
            },
            {
                'section_heading': 'Background',
                'drop_magnitude': 0.06,
                'retention_before': 0.75,
                'retention_after': 0.69,
                'estimated_timestamp': '1:30-3:00',
                'section_type': 'body'
            }
        ]

        result = format_mapped_drops_table(mapped_drops)

        assert isinstance(result, str)
        assert 'Introduction' in result
        assert 'Background' in result
        assert 'HIGH' in result  # 12% drop
        assert 'MEDIUM' in result  # 6% drop
        # Should be sorted by magnitude (biggest first)
        intro_pos = result.index('Introduction')
        background_pos = result.index('Background')
        assert intro_pos < background_pos

    def test_severity_classification(self):
        """Severity thresholds correct"""
        from tools.youtube_analytics.retention_mapper import format_mapped_drops_table

        drops = [
            {'section_heading': 'High', 'drop_magnitude': 0.15, 'retention_before': 0.9, 'retention_after': 0.75, 'estimated_timestamp': '0:00-1:00', 'section_type': 'intro'},
            {'section_heading': 'Medium', 'drop_magnitude': 0.07, 'retention_before': 0.8, 'retention_after': 0.73, 'estimated_timestamp': '1:00-2:00', 'section_type': 'body'},
            {'section_heading': 'Low', 'drop_magnitude': 0.03, 'retention_before': 0.7, 'retention_after': 0.67, 'estimated_timestamp': '2:00-3:00', 'section_type': 'body'}
        ]

        result = format_mapped_drops_table(drops)

        # HIGH: >10%, MEDIUM: 5-10%, LOW: <5%
        assert result.count('HIGH') == 1
        assert result.count('MEDIUM') == 1
        assert result.count('LOW') == 1
