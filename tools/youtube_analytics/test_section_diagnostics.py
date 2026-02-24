"""
Tests for section_diagnostics.py

Tests section drop diagnosis and voice pattern recommendations.
"""

import pytest


class TestLoadVoicePatterns:
    """Test voice pattern loading"""

    def test_patterns_structure(self):
        """Voice patterns organized by category"""
        from section_diagnostics import load_voice_patterns

        patterns = load_voice_patterns()

        assert 'openings' in patterns
        assert 'transitions' in patterns
        assert 'evidence' in patterns
        assert 'rhythm' in patterns

        # Check opening patterns exist
        assert 'visual_contrast_hook' in patterns['openings']
        assert 'current_event_hook' in patterns['openings']

        # Check each pattern has required fields
        pattern = patterns['openings']['visual_contrast_hook']
        assert 'name' in pattern
        assert 'formula' in pattern
        assert 'when' in pattern
        assert 'style_guide_ref' in pattern


class TestDiagnoseSectionDrop:
    """Test section drop diagnosis"""

    def test_abstract_opening_detection(self):
        """Detect abstract opening anti-pattern"""
        from section_diagnostics import diagnose_section_drop

        section_text = "The concept of sovereignty has been debated for centuries. To understand the dispute..."

        result = diagnose_section_drop(section_text, "Introduction", "intro", 0.08)

        assert len(result['root_causes']) > 0
        assert any('abstract' in cause.lower() for cause in result['root_causes'])
        assert len(result['recommendations']) > 0
        # Should recommend concrete opening pattern
        assert any('STYLE-GUIDE.md Part 6' in rec['pattern_ref'] for rec in result['recommendations'])

    def test_missing_causal_chain_detection(self):
        """Detect missing causal chain pattern"""
        from section_diagnostics import diagnose_section_drop

        section_text = "Britain signed the treaty in 1859. Guatemala disputed the boundary. The conflict escalated."

        result = diagnose_section_drop(section_text, "Background", "body", 0.07)

        assert len(result['root_causes']) > 0
        assert any('causal' in cause.lower() for cause in result['root_causes'])
        # Should recommend Kraut-Style Causal Chain
        assert any('causal chain' in rec['pattern'].lower() for rec in result['recommendations'])

    def test_causal_chain_present_passes(self):
        """Section with causal chains passes check"""
        from section_diagnostics import diagnose_section_drop

        section_text = "Britain signed the treaty in 1859, which meant that Guatemala lost territory. Consequently, they disputed the boundary."

        result = diagnose_section_drop(section_text, "Background", "body", 0.04)

        # Should NOT flag missing causal chain
        assert not any('causal' in cause.lower() for cause in result['root_causes'])

    def test_missing_evidence_detection(self):
        """Detect lack of evidence introduction"""
        from section_diagnostics import diagnose_section_drop

        section_text = "Many historians believe the treaty was unfair. The boundaries were poorly defined."

        result = diagnose_section_drop(section_text, "Analysis", "body", 0.09)

        assert len(result['root_causes']) > 0
        assert any('evidence' in cause.lower() for cause in result['root_causes'])
        # Should recommend evidence pattern
        assert any('quote' in rec['pattern'].lower() or 'evidence' in rec['pattern'].lower()
                   for rec in result['recommendations'])

    def test_evidence_present_passes(self):
        """Section with proper evidence passes check"""
        from section_diagnostics import diagnose_section_drop

        section_text = "According to historian Jane Smith in The Treaty Analysis, page 45, 'the boundary was intentionally vague.'"

        result = diagnose_section_drop(section_text, "Analysis", "body", 0.04)

        # Should NOT flag missing evidence
        assert not any('evidence' in cause.lower() for cause in result['root_causes'])

    def test_missing_modern_relevance_detection(self):
        """Detect lack of modern relevance"""
        from section_diagnostics import diagnose_section_drop

        section_text = "In 1859, Britain and Guatemala signed a treaty. The document established boundaries based on colonial claims from the 1700s."

        result = diagnose_section_drop(section_text, "Background", "body", 0.08)

        assert len(result['root_causes']) > 0
        assert any('modern' in cause.lower() or 'relevance' in cause.lower() for cause in result['root_causes'])

    def test_modern_relevance_present_passes(self):
        """Section with modern relevance passes check"""
        from section_diagnostics import diagnose_section_drop

        section_text = "The 1859 treaty established boundaries that still fuel disputes today. In 2024, both nations returned to the ICJ."

        result = diagnose_section_drop(section_text, "Background", "body", 0.04)

        # Should NOT flag missing modern relevance
        assert not any('modern' in cause.lower() for cause in result['root_causes'])

    def test_severity_classification(self):
        """Severity based on drop magnitude"""
        from section_diagnostics import diagnose_section_drop

        high_drop = diagnose_section_drop("Abstract content...", "Test", "body", 0.15)
        medium_drop = diagnose_section_drop("Abstract content...", "Test", "body", 0.07)
        low_drop = diagnose_section_drop("Abstract content...", "Test", "body", 0.03)

        assert high_drop['severity'] == 'HIGH'
        assert medium_drop['severity'] == 'MEDIUM'
        assert low_drop['severity'] == 'LOW'

    def test_confidence_assessment(self):
        """Confidence based on drop magnitude and pattern count"""
        from section_diagnostics import diagnose_section_drop

        # High drop with multiple anti-patterns = high confidence
        result = diagnose_section_drop("The concept of sovereignty...", "Test", "body", 0.12)

        assert result['confidence'] in ['high', 'medium', 'low']

    def test_position_in_section_affects_diagnosis(self):
        """Position within section considered in diagnosis"""
        from section_diagnostics import diagnose_section_drop

        # Drop at beginning of section (abstract opening issue)
        early_result = diagnose_section_drop("The concept of...", "Test", "body", 0.08, position_in_section=0.1)

        # Drop at end of section (pacing/conclusion issue)
        late_result = diagnose_section_drop("The concept of...", "Test", "body", 0.08, position_in_section=0.9)

        # Both should diagnose, but may have different recommendations
        assert len(early_result['recommendations']) > 0
        assert len(late_result['recommendations']) > 0


class TestDiagnoseAllDrops:
    """Test batch diagnosis"""

    def test_diagnose_multiple_drops(self):
        """Diagnose all drops in batch"""
        from section_diagnostics import diagnose_all_drops
        from dataclasses import dataclass

        @dataclass
        class MockSection:
            heading: str
            content: str
            word_count: int
            start_line: int
            section_type: str

        sections = [
            MockSection("Intro", "The concept of sovereignty...", 100, 1, "intro"),
            MockSection("Body", "Britain signed the treaty. Guatemala objected.", 150, 10, "body")
        ]

        mapped_drops = [
            {
                'section_heading': 'Intro',
                'section_type': 'intro',
                'drop_magnitude': 0.10,
                'position_in_section': 0.2
            },
            {
                'section_heading': 'Body',
                'section_type': 'body',
                'drop_magnitude': 0.06,
                'position_in_section': 0.5
            }
        ]

        result = diagnose_all_drops(mapped_drops, sections)

        assert len(result) == 2
        assert result[0]['section_heading'] == 'Intro'
        assert result[0]['drop_magnitude'] == 0.10
        assert 'root_causes' in result[0]
        assert 'recommendations' in result[0]

    def test_sorted_by_severity(self):
        """Results sorted by severity then magnitude"""
        from section_diagnostics import diagnose_all_drops
        from dataclasses import dataclass

        @dataclass
        class MockSection:
            heading: str
            content: str
            word_count: int
            start_line: int
            section_type: str

        sections = [
            MockSection("Low", "Content with evidence according to Smith...", 100, 1, "body"),
            MockSection("High", "The concept of...", 150, 10, "body")
        ]

        mapped_drops = [
            {'section_heading': 'Low', 'section_type': 'body', 'drop_magnitude': 0.04, 'position_in_section': 0.5},
            {'section_heading': 'High', 'section_type': 'body', 'drop_magnitude': 0.12, 'position_in_section': 0.5}
        ]

        result = diagnose_all_drops(mapped_drops, sections)

        # HIGH severity should come first
        assert result[0]['severity'] == 'HIGH'
        assert result[1]['severity'] == 'LOW'


class TestFormatDiagnosticsMarkdown:
    """Test markdown formatting"""

    def test_format_diagnostics_report(self):
        """Format diagnostics as markdown"""
        from section_diagnostics import format_diagnostics_markdown

        diagnoses = [
            {
                'section_heading': 'Introduction',
                'drop_magnitude': 0.12,
                'severity': 'HIGH',
                'root_causes': ['Abstract opening - no concrete anchor'],
                'recommendations': [
                    {
                        'fix': 'Start with concrete date/place/document',
                        'pattern': 'Visual Contrast Hook',
                        'pattern_ref': 'STYLE-GUIDE.md Part 6.1 Pattern 1',
                        'insertion_hint': 'Replace first sentence'
                    }
                ],
                'confidence': 'high'
            }
        ]

        result = format_diagnostics_markdown(diagnoses)

        assert isinstance(result, str)
        assert 'Introduction' in result
        assert '12%' in result or '0.12' in result
        assert 'HIGH' in result
        assert 'Abstract opening' in result
        assert 'STYLE-GUIDE.md Part 6.1 Pattern 1' in result

    def test_grouped_by_severity(self):
        """Report groups by severity"""
        from section_diagnostics import format_diagnostics_markdown

        diagnoses = [
            {'section_heading': 'A', 'drop_magnitude': 0.12, 'severity': 'HIGH', 'root_causes': ['Issue'], 'recommendations': [], 'confidence': 'high'},
            {'section_heading': 'B', 'drop_magnitude': 0.06, 'severity': 'MEDIUM', 'root_causes': ['Issue'], 'recommendations': [], 'confidence': 'medium'},
            {'section_heading': 'C', 'drop_magnitude': 0.03, 'severity': 'LOW', 'root_causes': ['Issue'], 'recommendations': [], 'confidence': 'low'}
        ]

        result = format_diagnostics_markdown(diagnoses)

        # HIGH should appear before MEDIUM before LOW
        high_pos = result.index('HIGH')
        medium_pos = result.index('MEDIUM')
        low_pos = result.index('LOW')

        assert high_pos < medium_pos < low_pos

    def test_low_confidence_warning(self):
        """Low confidence warning displayed"""
        from section_diagnostics import format_diagnostics_markdown

        diagnoses = [
            {
                'section_heading': 'Test',
                'drop_magnitude': 0.08,
                'severity': 'MEDIUM',
                'root_causes': ['Issue'],
                'recommendations': [],
                'confidence': 'low'
            }
        ]

        result = format_diagnostics_markdown(diagnoses)

        assert 'low confidence' in result.lower() or 'limited' in result.lower()
