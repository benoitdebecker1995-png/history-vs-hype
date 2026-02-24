"""
Test Retention Scorer Module

TDD test suite for retention_scorer.py covering all scoring contracts.
These tests define the expected behavior before implementation.

Run: python -m tools.youtube_analytics.test_retention_scorer
"""

import unittest
from unittest.mock import Mock, patch
from dataclasses import dataclass


# Mock Section class for testing
@dataclass
class Section:
    heading: str
    text: str
    word_count: int = 0
    section_type: str = 'body'


# Import will fail initially (RED phase) - this is correct
try:
    from retention_scorer import (
        score_section,
        score_all_sections,
        get_topic_baseline,
        format_retention_warnings,
        count_evidence_markers,
        measure_modern_relevance_gap,
        detect_voice_patterns
    )
    SCORER_AVAILABLE = True
except ImportError:
    SCORER_AVAILABLE = False


class TestScoreSection(unittest.TestCase):
    """Test score_section function contracts"""

    @unittest.skipUnless(SCORER_AVAILABLE, "retention_scorer not yet implemented")
    def test_short_section_with_evidence_scores_low_risk(self):
        """Short section with evidence markers should score LOW risk"""
        section_text = """According to Smith in his book, page 47, the treaty states
        that "borders shall be fixed at the river". This matters today because
        the dispute continues over these exact boundaries."""

        result = score_section(
            section_text=section_text,
            section_type='body',
            topic_type='territorial'
        )

        self.assertGreaterEqual(result['score'], 0.7)
        self.assertEqual(result['risk_level'], 'LOW')

    @unittest.skipUnless(SCORER_AVAILABLE, "retention_scorer not yet implemented")
    def test_long_section_no_evidence_scores_high_risk(self):
        """Long section without evidence or modern relevance should score HIGH risk"""
        # 400+ word section with no evidence markers
        section_text = """The historical period saw many changes occur in the region.
        Various powers contested the territory through diplomatic means and military
        campaigns. The population experienced significant disruption during this time.
        Different factions emerged with competing claims to legitimacy and control.
        The administrative structures underwent transformation as new systems were
        implemented. Cultural practices evolved in response to external pressures.
        Economic relationships shifted as trade patterns changed. Political alliances
        formed and dissolved repeatedly throughout the period. Social hierarchies were
        challenged and reconstituted in new forms. Religious institutions played
        various roles in mediating conflicts and providing continuity. The landscape
        itself was altered by construction projects and environmental factors. Military
        fortifications were built and abandoned as strategic priorities shifted.
        Diplomatic negotiations proceeded through formal and informal channels. Written
        records from the period reflect diverse perspectives on events. Archaeological
        evidence suggests patterns of settlement and movement. Material culture shows
        influences from multiple traditions blending together. Language use reveals
        contact between different communities and groups. Legal frameworks were adapted
        from earlier models while incorporating new elements. Educational systems
        transmitted knowledge and values to subsequent generations. Artistic production
        reflected both continuity with tradition and innovative responses."""

        result = score_section(
            section_text=section_text,
            section_type='body',
            topic_type='territorial'
        )

        self.assertLess(result['score'], 0.5)
        self.assertEqual(result['risk_level'], 'HIGH')
        self.assertGreaterEqual(len(result['warnings']), 2)

    @unittest.skipUnless(SCORER_AVAILABLE, "retention_scorer not yet implemented")
    def test_section_with_voice_patterns_gets_fewer_warnings(self):
        """Section with voice patterns should have fewer warnings than one without"""
        section_a = """According to the treaty, consequently the borders shifted, which
        meant that the population found themselves on different sides. This matters today
        because the dispute continues."""

        section_b = """The borders changed during this period. The population was affected
        by these changes. There were consequences. The situation developed over time.
        Various factors played roles. Different outcomes emerged."""

        result_a = score_section(section_a, 'body', 'territorial')
        result_b = score_section(section_b, 'body', 'territorial')

        self.assertLess(len(result_a['warnings']), len(result_b['warnings']))

    @unittest.skipUnless(SCORER_AVAILABLE, "retention_scorer not yet implemented")
    def test_intro_with_abstract_opening_gets_warning(self):
        """Intro starting with abstract concept should get warning"""
        section_text = """The concept of borders has evolved throughout history. To
        understand this evolution, we must examine various factors. In order to
        appreciate the complexity, we should consider multiple perspectives."""

        result = score_section(
            section_text=section_text,
            section_type='intro',
            topic_type='territorial'
        )

        # Check that at least one warning mentions abstract or opening
        warning_texts = [w.get('issue', '').lower() for w in result['warnings']]
        has_abstract_warning = any('abstract' in w or 'opening' in w for w in warning_texts)
        self.assertTrue(has_abstract_warning)

    @unittest.skipUnless(SCORER_AVAILABLE, "retention_scorer not yet implemented")
    def test_conclusion_without_forward_statement_gets_warning(self):
        """Conclusion without modern/forward-looking element should get warning"""
        section_text = """The treaty was signed in 1859. The borders were established
        at that time. Both sides accepted the agreement. The matter was settled through
        diplomatic means."""

        result = score_section(
            section_text=section_text,
            section_type='conclusion',
            topic_type='territorial'
        )

        # Check that at least one warning mentions closing or forward
        warning_texts = [w.get('issue', '').lower() for w in result['warnings']]
        has_closing_warning = any('closing' in w or 'forward' in w for w in warning_texts)
        self.assertTrue(has_closing_warning)


class TestGetTopicBaseline(unittest.TestCase):
    """Test get_topic_baseline function contracts"""

    @unittest.skipUnless(SCORER_AVAILABLE, "retention_scorer not yet implemented")
    @patch('retention_scorer.KeywordDB')
    def test_returns_hardcoded_defaults_when_no_data(self, mock_db_class):
        """Should return hardcoded defaults when database has no data"""
        mock_db = Mock()
        mock_db.get_all_performance.return_value = []
        mock_db_class.return_value = mock_db

        result = get_topic_baseline('nonexistent_topic')

        self.assertEqual(result['avg_section_length'], 150)
        self.assertEqual(result['confidence'], 'default')

    @unittest.skipUnless(SCORER_AVAILABLE, "retention_scorer not yet implemented")
    @patch('retention_scorer.KeywordDB')
    def test_falls_back_to_channel_average_for_sparse_topic(self, mock_db_class):
        """Should use channel average when specific topic has <3 videos"""
        mock_db = Mock()

        # Return 10 territorial videos and 1 colonial video
        mock_db.get_all_performance.return_value = [
            {'video_id': 'vid1', 'topic_type': 'territorial', 'lessons_learned': '{}'},
            {'video_id': 'vid2', 'topic_type': 'territorial', 'lessons_learned': '{}'},
            {'video_id': 'vid3', 'topic_type': 'territorial', 'lessons_learned': '{}'},
            {'video_id': 'vid4', 'topic_type': 'territorial', 'lessons_learned': '{}'},
            {'video_id': 'vid5', 'topic_type': 'territorial', 'lessons_learned': '{}'},
            {'video_id': 'vid6', 'topic_type': 'territorial', 'lessons_learned': '{}'},
            {'video_id': 'vid7', 'topic_type': 'territorial', 'lessons_learned': '{}'},
            {'video_id': 'vid8', 'topic_type': 'territorial', 'lessons_learned': '{}'},
            {'video_id': 'vid9', 'topic_type': 'territorial', 'lessons_learned': '{}'},
            {'video_id': 'vid10', 'topic_type': 'territorial', 'lessons_learned': '{}'},
            {'video_id': 'vid11', 'topic_type': 'colonial', 'lessons_learned': '{}'},
        ]
        mock_db_class.return_value = mock_db

        result = get_topic_baseline('colonial')

        # Should use channel average (not defaults, not colonial-specific)
        self.assertNotEqual(result['confidence'], 'default')
        self.assertGreater(result['video_count'], 1)


class TestHelperFunctions(unittest.TestCase):
    """Test helper function contracts"""

    @unittest.skipUnless(SCORER_AVAILABLE, "retention_scorer not yet implemented")
    def test_count_evidence_markers(self):
        """Should count evidence markers in text"""
        text = """According to Smith, page 47, the treaty states that "borders shall
        be fixed". The document shows clear intent."""

        count = count_evidence_markers(text)

        # Should find: "according to", "page ", "treaty states", quotes, "document shows"
        self.assertGreaterEqual(count, 3)

    @unittest.skipUnless(SCORER_AVAILABLE, "retention_scorer not yet implemented")
    def test_measure_modern_relevance_gap_with_marker_at_end(self):
        """Gap should be 0 when modern marker is at end"""
        text = """Historical context here about events that happened long ago.
        This matters today."""

        gap = measure_modern_relevance_gap(text)

        self.assertEqual(gap, 0)

    @unittest.skipUnless(SCORER_AVAILABLE, "retention_scorer not yet implemented")
    def test_measure_modern_relevance_gap_no_marker(self):
        """Gap should equal word count when no modern marker present"""
        text = """Historical context with no connection whatsoever in this passage
        about ancient events."""

        gap = measure_modern_relevance_gap(text)

        word_count = len(text.split())
        self.assertEqual(gap, word_count)

    @unittest.skipUnless(SCORER_AVAILABLE, "retention_scorer not yet implemented")
    def test_detect_voice_patterns_finds_causal_connectors(self):
        """Should detect causal connector patterns"""
        text = """consequently the border shifted which meant that the population
        found themselves divided"""

        patterns = detect_voice_patterns(text)

        # Should find causal connectors
        self.assertGreater(len(patterns), 0)
        pattern_str = ' '.join(patterns).lower()
        self.assertTrue('causal' in pattern_str or 'consequently' in pattern_str)


class TestScoreAllSections(unittest.TestCase):
    """Test score_all_sections function contracts"""

    @unittest.skipUnless(SCORER_AVAILABLE, "retention_scorer not yet implemented")
    def test_score_all_sections_returns_list_with_headings(self):
        """Should return list with section_heading for each section"""
        sections = [
            Section(heading='Introduction', text='Short intro text.', word_count=3),
            Section(heading='Background', text='Some background context.', word_count=3),
        ]

        result = score_all_sections(sections, 'territorial')

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)
        self.assertIn('section_heading', result[0])
        self.assertEqual(result[0]['section_heading'], 'Introduction')


class TestFormatRetentionWarnings(unittest.TestCase):
    """Test format_retention_warnings function contracts"""

    @unittest.skipUnless(SCORER_AVAILABLE, "retention_scorer not yet implemented")
    def test_format_only_shows_medium_and_high(self):
        """Should only show MEDIUM and HIGH risk sections"""
        scored_sections = [
            {
                'section_heading': 'Low Risk Section',
                'risk_level': 'LOW',
                'score': 0.8,
                'warnings': []
            },
            {
                'section_heading': 'Medium Risk Section',
                'risk_level': 'MEDIUM',
                'score': 0.6,
                'warnings': [{'issue': 'Test warning'}]
            },
            {
                'section_heading': 'High Risk Section',
                'risk_level': 'HIGH',
                'score': 0.3,
                'warnings': [{'issue': 'Test warning'}]
            }
        ]

        formatted = format_retention_warnings(scored_sections)

        # Should contain MEDIUM and HIGH but not LOW
        self.assertIn('Medium Risk Section', formatted)
        self.assertIn('High Risk Section', formatted)
        self.assertNotIn('Low Risk Section', formatted)


if __name__ == '__main__':
    unittest.main()
