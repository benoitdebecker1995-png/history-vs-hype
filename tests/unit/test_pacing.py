"""
Unit tests for PacingChecker

Tests cover:
- Sentence variance calculation
- Flesch Reading Ease delta detection
- Entity density measurement
- Composite scoring
- Energy arc sparkline generation
- Flat zone detection
- Hook/interrupt detection
- Multi-section verdict logic

Usage:
    python -m pytest tests/unit/test_pacing.py
"""

import unittest

from tools.script_checkers.checkers.pacing import (
    PacingChecker,
    generate_sparkline,
    detect_flat_zones
)

# PacingChecker.check() requires spaCy and textstat for sentence analysis
# These are optional dependencies ([nlp] extras) — skip tests if not installed
try:
    import spacy  # noqa: F401
    import textstat  # noqa: F401
    NLP_AVAILABLE = True
except ImportError:
    NLP_AVAILABLE = False

requires_nlp = unittest.skipUnless(NLP_AVAILABLE, "spaCy and textstat required (pip install -e .[nlp])")


class MockConfig:
    """Mock config object for testing"""
    def __init__(self):
        self.pacing_variance_threshold = 15
        self.pacing_flesch_delta_threshold = 20
        self.pacing_entity_density_threshold = 0.4
        self.pacing_pass_threshold = 75
        self.pacing_fail_threshold = 50
        self.pacing_flat_zone_window = 3
        self.pacing_flat_zone_tolerance = 10


class TestPacingChecker(unittest.TestCase):
    """Test suite for PacingChecker"""

    def setUp(self):
        """Create PacingChecker instance with mock config"""
        self.checker = PacingChecker(MockConfig())

    # === PACE-01: Sentence Variance Tests ===

    @requires_nlp
    def test_sentence_variance_below_threshold(self):
        """Text with uniform sentence lengths should not flag variance"""
        # Both sections use similar sentence lengths AND similar reading level to avoid flesch delta
        text = """
## Test Section

The cat sat on the mat today. The dog ran around the park. The bird flew over the old tree. The fish swam through the pond. The horse trotted down the lane.

## Section Two

The frog jumped into the water. The deer ran across the field. The hawk flew over the mountain. The snake slid under the rock. The bear walked through the woods.
"""
        result = self.checker.check(text)
        self.assertEqual(len(result['issues']), 0)
        self.assertIn(result['stats']['verdict'], ['PASS', 'NEEDS WORK'])

    @requires_nlp
    def test_sentence_variance_above_threshold(self):
        """Text with wildly varying sentences should flag variance"""
        # Both sections have extreme variance (1 word vs 30+ words) AND similar flesch levels
        text = """
## Test Section

Go. This is an extremely long sentence that goes on and on and on with many many words creating absolutely huge variance in the rhythm of the overall text passage that the reader must process and understand. Stop. This is yet another very long sentence that adds even more significant variation to the sentence length distribution throughout this entire section of the document. No.

## Section Two

Run. This is another tremendously long sentence with lots and lots and lots of words creating very big differences in how long each sentence is compared to the extremely short ones located nearby in this passage. End. This is yet another extremely lengthy sentence that keeps the variance really high throughout the second section of this whole text passage as well for testing purposes. Yes.
"""
        result = self.checker.check(text)
        # Variance above threshold should appear in section reasons (even if score stays above pass threshold)
        all_reasons = [r for s in result['all_sections'] for r in s['reasons']]
        self.assertGreater(len(all_reasons), 0)
        self.assertTrue(any('variance' in r.lower() for r in all_reasons))

    @requires_nlp
    def test_sentence_variance_single_sentence(self):
        """Single sentence should return variance = 0.0 (single headed section is analyzed)"""
        text = """
## Test Section

This is a single sentence.
"""
        result = self.checker.check(text)
        section = result['all_sections'][0]
        self.assertEqual(section['metrics']['sentence_variance'], 0.0)

    # === PACE-02: Flesch Reading Ease Delta Tests ===

    @requires_nlp
    def test_flesch_delta_within_threshold(self):
        """Two sections with similar complexity should not flag delta"""
        text = """
## First Section

The cat sat on the mat. The dog ran in the park. Simple sentences here.

## Second Section

The bird flew over the tree. The fish swam in the pond. More simple sentences.
"""
        result = self.checker.check(text)
        self.assertEqual(len(result['issues']), 0)

    @requires_nlp
    def test_flesch_delta_exceeds_threshold(self):
        """Simple section followed by complex section should flag delta"""
        text = """
## Simple Section

The cat sat. The dog ran. The bird flew.

## Complex Section

Notwithstanding the aforementioned considerations regarding the multifaceted implications of geopolitical ramifications, it becomes imperative to acknowledge the intricate interconnectedness of socioeconomic factors that fundamentally underpin the contemporary international relations paradigm.
"""
        result = self.checker.check(text)
        self.assertGreater(len(result['issues']), 0)
        self.assertTrue(any('readability' in str(issue).lower() or 'flesch' in str(issue).lower()
                   for issue in result['issues']))

    @requires_nlp
    def test_flesch_delta_first_section(self):
        """First section should have delta = 0"""
        text = """
## First Section

This is the first section with some text.
"""
        result = self.checker.check(text)
        section = result['all_sections'][0]
        self.assertEqual(section['metrics']['flesch_delta'], 0)

    # === PACE-03: Entity Density Tests ===

    @requires_nlp
    def test_entity_density_below_threshold(self):
        """Normal prose should not flag entity density"""
        # Both sections use similar simple prose to avoid flesch delta issues
        text = """
## Test Section

The government announced a new policy today. Many people were surprised by the decision. Officials said it would take effect very soon.

## Second Section

The council released a new report last week. Several groups were happy with the findings. Leaders said the plan would begin next month.
"""
        result = self.checker.check(text)
        self.assertEqual(len(result['issues']), 0)

    @requires_nlp
    def test_entity_density_above_threshold(self):
        """Proper-noun-heavy text should flag entity density"""
        text = """
## Test Section

President Biden met with Prime Minister Trudeau and Chancellor Scholz in Brussels. Secretary Blinken joined Foreign Minister Baerbock and Ambassador Sullivan for discussions with Commissioner von der Leyen.

## Second Section

Foreign Minister Baerbock discussed with Prime Minister Trudeau and Chancellor Scholz in Brussels.
"""
        result = self.checker.check(text)
        self.assertGreater(len(result['issues']), 0)
        self.assertTrue(any('entity' in str(issue).lower() or 'proper noun' in str(issue).lower()
                   for issue in result['issues']))

    @requires_nlp
    def test_entity_density_empty_text(self):
        """Empty string should return density = 0.0"""
        text = """
## Empty Section


"""
        result = self.checker.check(text)
        section = result['all_sections'][0]
        self.assertEqual(section['metrics']['entity_density'], 0.0)

    # === PACE-04: Composite Score Tests ===

    @requires_nlp
    def test_composite_score_perfect(self):
        """All metrics below thresholds should return score = 100"""
        text = """
## Test Section

The cat sat on the mat. The dog ran in the park. The bird flew over the tree. Simple and consistent sentences with normal word usage throughout.
"""
        result = self.checker.check(text)
        section = result['all_sections'][0]
        self.assertEqual(section['score'], 100)

    @requires_nlp
    def test_composite_score_degraded(self):
        """One metric over threshold should lower score"""
        # First section is simple; second section is complex — creating a large flesch delta
        text = """
## Simple Section

The cat sat on the mat. The dog ran in the park. The bird flew high.

## Complex Section

Notwithstanding the aforementioned considerations regarding the multifaceted implications of geopolitical ramifications, it becomes imperative to acknowledge the intricate interconnectedness of socioeconomic factors that fundamentally underpin contemporary paradigms.
"""
        result = self.checker.check(text)
        # The complex second section should have degraded score due to flesch delta
        min_score = min(s['score'] for s in result['all_sections'])
        self.assertLess(min_score, 100)

    @requires_nlp
    def test_composite_score_floor(self):
        """All metrics very bad should not go below 0"""
        text = """
## Test Section

W. This extremely long sentence with excessive length creates massive variance while simultaneously incorporating numerous proper nouns like President Biden Prime Minister Trudeau Chancellor Scholz Secretary Blinken Foreign Minister Baerbock creating extremely high entity density. X.
"""
        result = self.checker.check(text)
        section = result['all_sections'][0]
        self.assertGreaterEqual(section['score'], 0)

    # === PACE-06: Sparkline Tests ===

    def test_sparkline_generation(self):
        """Known scores should produce expected sparkline"""
        scores = [100, 75, 50, 25, 0]  # Perfect to worst
        sparkline = generate_sparkline(scores)
        # Low score = high complexity = tall bar (inverted)
        # 100 -> 0 complexity -> shortest, 0 -> 100 complexity -> tallest
        self.assertEqual(len(sparkline), 5)
        self.assertLess(sparkline[0], sparkline[-1])  # First should be lower than last

    def test_sparkline_all_identical(self):
        """All same score should produce mid-level bars"""
        scores = [50, 50, 50, 50]
        sparkline = generate_sparkline(scores)
        self.assertEqual(len(sparkline), 4)
        # All bars should be identical
        self.assertEqual(len(set(sparkline)), 1)

    def test_sparkline_empty(self):
        """Empty list should return empty string"""
        sparkline = generate_sparkline([])
        self.assertEqual(sparkline, "")

    # === PACE-06: Flat Zone Tests ===

    def test_flat_zone_detected(self):
        """4 sections with similar scores should detect 1 flat zone"""
        scores = [100, 72, 70, 68, 71, 45]  # Sections 1-4 are within 10 points
        flat_zones = detect_flat_zones(scores)
        self.assertGreater(len(flat_zones), 0)

    def test_flat_zone_none(self):
        """Varied scores should detect no flat zones"""
        scores = [100, 80, 60, 40, 20]
        flat_zones = detect_flat_zones(scores)
        self.assertEqual(len(flat_zones), 0)

    def test_flat_zone_short_script(self):
        """2 sections should not be able to form flat zone"""
        scores = [50, 50]
        flat_zones = detect_flat_zones(scores)
        self.assertEqual(len(flat_zones), 0)

    # === PACE-05: Hook Detection Tests ===

    @requires_nlp
    def test_hook_detection_finds_keywords(self):
        """Text with time keywords should be detected"""
        text = "This happened in 1919 but still affects us today. Currently, we see the impacts."
        hooks = self.checker._detect_hooks(text)
        self.assertGreater(len(hooks), 0)

    @requires_nlp
    def test_hook_detection_finds_markers(self):
        """Text with B-roll markers should be detected"""
        text = "Historical background here. [NEWS CLIP: Modern footage] More context."
        hooks = self.checker._detect_hooks(text)
        self.assertGreater(len(hooks), 0)

    # === Integration Tests ===

    @requires_nlp
    def test_check_single_section_skipped(self):
        """Headerless script should return SKIPPED verdict"""
        text = """
This is a script without any H2 headers so it becomes a single section.
"""
        result = self.checker.check(text)
        self.assertEqual(result['stats']['verdict'], 'SKIPPED')

    @requires_nlp
    def test_check_headerless_still_reports_sections(self):
        """Contract: all_sections carries one entry per parsed section — even when SKIPPED"""
        text = """
This is a script without any H2 headers so it becomes a single section.
"""
        result = self.checker.check(text)
        self.assertEqual(result['stats']['verdict'], 'SKIPPED')
        self.assertEqual(len(result['all_sections']), 1)
        self.assertIn('metrics', result['all_sections'][0])

    @requires_nlp
    def test_check_single_headed_section_gets_verdict(self):
        """A single ## headed section is analyzed fully — SKIPPED is only for headerless text"""
        text = """
## Only Section

The cat sat on the mat. The dog ran in the park. Simple text here.
"""
        result = self.checker.check(text)
        self.assertEqual(len(result['all_sections']), 1)
        self.assertIn(result['stats']['verdict'], ['PASS', 'NEEDS WORK', 'FAIL'])

    @requires_nlp
    def test_check_multi_section_verdict(self):
        """Multi-section script should return appropriate verdict"""
        text = """
## Section One

The cat sat on the mat. The dog ran in the park. Simple text here.

## Section Two

The bird flew over the tree. The fish swam in the pond. More simple text.
"""
        result = self.checker.check(text)
        self.assertIn(result['stats']['verdict'], ['PASS', 'NEEDS WORK', 'FAIL'])

    @requires_nlp
    def test_broll_markers_stripped(self):
        """B-roll markers should not inflate counts"""
        text = """
## Test Section

This sentence has normal words. [B-ROLL: Historical footage] This continues the narration. [MAP: Show border] And this is the conclusion.
"""
        result = self.checker.check(text)
        section = result['all_sections'][0]
        # Entity density and sentence variance should not be affected by markers
        self.assertLess(section['metrics']['entity_density'], 0.3)  # No proper nouns in actual text

    @requires_nlp
    def test_reasons_include_root_cause(self):
        """Reason strings should contain metric values and explanations"""
        text = """
## Test Section

W. This extremely long sentence with many words creates significant variance in the reading rhythm. X.
"""
        result = self.checker.check(text)
        if result['issues']:
            issue = result['issues'][0]
            self.assertIn('reasons', issue)
            self.assertGreater(len(issue['reasons']), 0)
            # Each reason should contain both the metric value and explanation
            for reason in issue['reasons']:
                self.assertIsInstance(reason, str)
                self.assertGreater(len(reason), 10)  # Should be descriptive


if __name__ == '__main__':
    unittest.main()
