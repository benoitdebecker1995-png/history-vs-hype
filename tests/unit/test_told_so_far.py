"""
Unit tests for ToldSoFarChecker (SCRIPT-06).

Mechanizes VOICE-PROFILE.md's #62 T1-T3 read-aloud finding (~line 512):
"a rebuttal is a referent too — its antecedent claim must exist on screen
first." His ~30 flags on that pass reduced to this one failure class
(quoted in the profile: "which massacre?", "what case?", "a callback to
something that doesn't exist"). These tests use constructed script snippets
representative of that failure class, not verbatim profile text (the
profile quotes his spoken read-aloud reactions, not script lines).

Usage:
    python -m pytest tests/unit/test_told_so_far.py
"""

import unittest

from tools.script_checkers.checkers.told_so_far import ToldSoFarChecker


class MockConfig:
    pass


class TestToldSoFarChecker(unittest.TestCase):
    def setUp(self):
        self.checker = ToldSoFarChecker(MockConfig())

    def test_rebuttal_with_no_antecedent_is_flagged(self):
        # "That massacre" is negated/called back to without ever being introduced —
        # representative of VOICE-PROFILE.md's "which massacre?" read-aloud confusion.
        text = (
            "The village was quiet that morning.\n\n"
            "That massacre wasn't random violence — it was coordinated from the top.\n"
        )
        result = self.checker.check(text)
        self.assertGreaterEqual(result['stats']['flagged'], 1)
        self.assertEqual(result['stats']['severity'], 'warning')

    def test_rebuttal_with_earlier_antecedent_is_not_flagged(self):
        # The massacre IS introduced (and named) first, so the later negation
        # shares a content word with something already on screen.
        text = (
            "In July 1943, militants carried out a massacre across dozens of "
            "villages in a single night.\n\n"
            "That massacre wasn't random violence — it was coordinated from the top.\n"
        )
        result = self.checker.check(text)
        self.assertEqual(result['stats']['flagged'], 0)

    def test_callback_with_no_antecedent_is_flagged(self):
        text = (
            "The treaty was signed in March.\n\n"
            "As we saw, the same case collapsed within a year.\n"
        )
        result = self.checker.check(text)
        self.assertGreaterEqual(result['stats']['flagged'], 1)

    def test_clean_script_with_no_triggers_has_zero_issues(self):
        text = (
            "The empire controlled the region for three centuries.\n\n"
            "In 1920, that changed when the treaty was signed.\n"
        )
        result = self.checker.check(text)
        self.assertEqual(result['stats']['total_triggers'], 0)
        self.assertEqual(result['stats']['flagged'], 0)
        self.assertEqual(result['stats']['severity'], 'ok')

    def test_structural_lines_are_ignored(self):
        text = (
            "## ACT 1\n\n"
            "**STATUS:** locked\n\n"
            "[SHOW: some card]\n\n"
            "The empire controlled the region for three centuries.\n"
        )
        result = self.checker.check(text)
        self.assertEqual(result['stats']['total_triggers'], 0)

    def test_returns_issues_and_stats_shape(self):
        result = self.checker.check("Nothing happened.")
        self.assertIn('issues', result)
        self.assertIn('stats', result)
        self.assertIsInstance(result['issues'], list)
        self.assertIsInstance(result['stats'], dict)


if __name__ == "__main__":
    unittest.main()
