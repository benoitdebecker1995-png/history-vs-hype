"""
Tests for retention_mapper.py

Tests retention-to-script section mapping without API calls.
"""

import pytest
from dataclasses import dataclass
from tools.youtube_analytics.retention_inference import RetentionInference

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
        result = RetentionInference.mapped_drops(drops, sections)
        assert len(result) == 1
        assert result[0]['section_heading'] == 'Introduction'
        assert result[0]['drop_position'] == 0.5
        assert result[0]['drop_magnitude'] == 0.10
        assert result[0]['section_type'] == 'intro'

    def test_multi_section_multi_drop(self):
        """Multiple drops across multiple sections"""
        sections = [
            MockSection("Introduction", "Intro content...", 100, 1, "intro"),
            MockSection("Background", "Background content...", 200, 10, "body"),
            MockSection("Analysis", "Analysis content...", 150, 25, "body"),
            MockSection("Conclusion", "Conclusion content...", 50, 40, "conclusion")
        ]
        drops = [
            {'position': 0.15, 'retention_before': 0.95, 'retention_after': 0.88, 'drop': 0.07, 'timestamp_hint': 'early'},
            {'position': 0.35, 'retention_before': 0.85, 'retention_after': 0.72, 'drop': 0.13, 'timestamp_hint': 'first half'}
        ]
        result = RetentionInference.mapped_drops(drops, sections)
        assert len(result) == 2
        assert result[0]['section_heading'] == 'Introduction'
        assert result[1]['section_heading'] == 'Background'

    def test_drop_at_section_boundary(self):
        """Drop exactly at section boundary"""
        sections = [
            MockSection("First", "Content A", 100, 1, "intro"),
            MockSection("Second", "Content B", 100, 10, "body")
        ]
        drops = [
            {'position': 0.5, 'retention_before': 0.80, 'retention_after': 0.70, 'drop': 0.10, 'timestamp_hint': 'first half'}
        ]
        result = RetentionInference.mapped_drops(drops, sections)
        assert len(result) == 1
        assert result[0]['section_heading'] == 'Second'

    def test_empty_drops_list(self):
        """Empty drops list returns empty result"""
        sections = [MockSection("Test", "Content", 100, 1, "intro")]
        drops = []
        result = RetentionInference.mapped_drops(drops, sections)
        assert result == []

    def test_empty_sections_list(self):
        """Empty sections list returns empty result"""
        sections = []
        drops = [{'position': 0.5, 'retention_before': 0.80, 'retention_after': 0.70, 'drop': 0.10, 'timestamp_hint': 'first half'}]
        result = RetentionInference.mapped_drops(drops, sections)
        assert result == []

    def test_drop_outside_section_boundaries(self):
        """Drop position outside any section boundary is skipped"""
        sections = [MockSection("Introduction", "Content", 100, 1, "intro")]
        drops = [{'position': 1.5, 'retention_before': 0.80, 'retention_after': 0.70, 'drop': 0.10, 'timestamp_hint': 'conclusion'}]
        result = RetentionInference.mapped_drops(drops, sections)
        assert len(result) == 0

    def test_position_in_section_calculation(self):
        """Position within section calculated correctly"""
        sections = [
            MockSection("Introduction", "Content", 200, 1, "intro"),
            MockSection("Body", "More content", 200, 10, "body")
        ]
        drops = [{'position': 0.75, 'retention_before': 0.80, 'retention_after': 0.70, 'drop': 0.10, 'timestamp_hint': 'second half'}]
        result = RetentionInference.mapped_drops(drops, sections)
        assert len(result) == 1
        assert result[0]['position_in_section'] == 0.5


class TestEstimateSectionTimestamps:
    """Test section timestamp estimation"""

    def test_estimate_timestamps(self):
        """Estimate timestamps for sections"""
        sections = [
            MockSection("Intro", "Content", 150, 1, "intro"),
            MockSection("Body", "Content", 300, 10, "body")
        ]
        result = RetentionInference.section_timestamps(sections, wpm=150)
        assert len(result) == 2
        assert result[0]['heading'] == 'Intro'
        assert result[0]['start_time_str'] == '0:00'
        assert result[0]['end_time_str'] == '1:00'
        assert result[1]['heading'] == 'Body'
        assert result[1]['start_time_str'] == '1:00'
        assert result[1]['end_time_str'] == '3:00'

    def test_wpm_variation(self):
        """Estimation changes with WPM"""
        sections = [MockSection("Intro", "Content", 150, 1, "intro")]
        result_150 = RetentionInference.section_timestamps(sections, wpm=150)
        result_300 = RetentionInference.section_timestamps(sections, wpm=300)
        assert result_150[0]['end_time_str'] == '1:00'
        assert result_300[0]['end_time_str'] == '0:30'

    def test_empty_list(self):
        """Empty list returns empty result"""
        assert RetentionInference.section_timestamps([]) == []


class TestFormatMappedDropsTable:
    """Test markdown table formatting"""

    def test_format_table(self):
        """Format mapped drops as markdown table"""
        mapped_drops = [
            {
                'section_heading': 'Intro',
                'drop_magnitude': 0.08,
                'retention_before': 0.90,
                'retention_after': 0.82,
                'estimated_timestamp': '0:45'
            }
        ]
        table = RetentionInference.format_drops_table(mapped_drops)
        assert '| Intro |' in table
        assert '| 8.0% |' in table
        assert '| 90.0% → 82.0% |' in table
        assert '| 0:45 |' in table
        assert '| MEDIUM |' in table

    def test_severity_classification(self):
        """Drops classified as LOW/MEDIUM/HIGH severity"""
        drops = [
            {'section_heading': 'A', 'drop_magnitude': 0.04, 'retention_before': 0.90, 'retention_after': 0.86, 'estimated_timestamp': '0:10'},
            {'section_heading': 'B', 'drop_magnitude': 0.07, 'retention_before': 0.90, 'retention_after': 0.83, 'estimated_timestamp': '0:20'},
            {'section_heading': 'C', 'drop_magnitude': 0.12, 'retention_before': 0.90, 'retention_after': 0.78, 'estimated_timestamp': '0:30'}
        ]
        table = RetentionInference.format_drops_table(drops)
        assert '| LOW |' in table
        assert '| MEDIUM |' in table
        assert '| HIGH |' in table

    def test_empty_list(self):
        """Empty list returns empty message"""
        assert "No significant drops" in RetentionInference.format_drops_table([])
