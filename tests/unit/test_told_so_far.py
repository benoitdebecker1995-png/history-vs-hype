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
from pathlib import Path

from tools.script_checkers.checkers.told_so_far import ToldSoFarChecker

ROOT = Path(__file__).resolve().parents[2]
# Moved 2026-08-26 when project 62 was migrated to the three-file shape: everything
# except PROJECT/RESEARCH/SCRIPT went to _cold/legacy-working/. This fixture is a
# frozen script version, so it belongs there permanently.
VOLHYNIA = ROOT / "video-projects/_IN_PRODUCTION/62-volhynia-massacre-untranslated-2026/_cold/legacy-working/VO-v7.1.md"
LASSOS = ROOT / "video-projects/_ARCHIVED/published/56-no-lassos-atlantic-slave-trade-origin-2026/FINAL-SCRIPT-TELEPROMPTER.txt"


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


    def test_v5_volhynia_three_part_promise_is_satisfied(self):
        result = self.checker.check(VOLHYNIA.read_text(encoding="utf-8"))
        self.assertEqual(result['stats']['promises_found'], 1)
        self.assertEqual(result['stats']['broken_promises'], 0)
        self.assertFalse(any(issue['type'] == 'broken_promise' for issue in result['issues']))

    def test_v5_promise_items_are_extracted_verbatim(self):
        result = self.checker.check(VOLHYNIA.read_text(encoding="utf-8"))
        promise = next(i for i in result['issues'] if i['type'] == 'promise')
        self.assertEqual(promise['items'], [
            'attacks going off everywhere at once',
            'reports coming back up the chain',
            'the order itself',
        ])

    def test_v5_cutting_the_attacks_payoff_breaks_the_promise(self):
        # A REAL cut of a REAL payoff: CH5/CH6 carry the coordinated-attacks
        # beat, and `attacks` appears nowhere else after the cold-open promise.
        # NB: cutting at CH7 instead does NOT break detectably — `order` still
        # appears earlier as a verb and inside the question that raises it. That
        # is the honest limit of this check; see _check_promises' docstring.
        script = VOLHYNIA.read_text(encoding="utf-8")
        result = self.checker.check(script.split("## CH 5 — BLOODY SUNDAY", 1)[0])
        broken = [i for i in result['issues'] if i['type'] == 'broken_promise']
        self.assertEqual(result['stats']['broken_promises'], 1)
        self.assertEqual(broken[0]['severity'], 'review')
        self.assertEqual(broken[0]['unsatisfied'], ['attacks going off everywhere at once'])

    def test_v4_catches_the_deliberate_death_toll_restatement_specifically(self):
        # Non-vacuous: pins the actual pair. #62 states the toll twice ON PURPOSE
        # so scale lands before the honoring is explained; the checker must SEE it
        # and must hand it back as REVIEW carrying the position guard, never a cut.
        result = self.checker.check(VOLHYNIA.read_text(encoding="utf-8"))
        repeats = [i for i in result['issues'] if i['type'] == 'possible_reanswer']
        toll = [i for i in repeats
                if 'fifty' in i['sentence'].lower() and 'sixty' in i['sentence'].lower()]
        self.assertEqual(len(toll), 1, "must detect the deliberate death-toll restatement")
        self.assertIn('fifty', toll[0]['echoes'].lower())
        self.assertNotEqual(toll[0]['echoes_line'], toll[0]['line'])
        self.assertEqual(toll[0]['severity'], 'review')
        self.assertIn('position', toll[0]['suggestion'].lower())
        self.assertTrue(all(i['severity'] == 'review' for i in repeats))

    def test_real_56_script_gains_no_warning_and_no_false_promise(self):
        # Non-vacuous: asserts the counts, not just a property of a possibly
        # empty list. A published, creator-approved script must stay clean.
        result = self.checker.check(LASSOS.read_text(encoding="utf-8"))
        self.assertEqual(result['stats']['severity'], 'ok')
        self.assertEqual(result['stats']['flagged'], 0)
        self.assertEqual(result['stats']['promises_found'], 0)
        self.assertEqual(result['stats']['broken_promises'], 0)
        v4 = [i for i in result['issues'] if i['type'] == 'possible_reanswer']
        self.assertEqual(len(v4), 1)
        self.assertEqual(v4[0]['severity'], 'review')

    def test_v4_and_v5_never_escalate_overall_severity(self):
        # The project gates on `0 HARD`. An uncertain check that escalates is
        # worse than no check, so REVIEW findings must not move the verdict.
        result = self.checker.check(VOLHYNIA.read_text(encoding="utf-8"))
        self.assertTrue(any(i['severity'] == 'review' for i in result['issues']))
        self.assertEqual(result['stats']['severity'], 'ok')

    def test_v2_and_v3_are_explicitly_not_mechanized(self):
        result = self.checker.check(LASSOS.read_text(encoding="utf-8"))
        self.assertEqual(result['stats']['not_mechanized'], ['V2', 'V3'])
if __name__ == "__main__":
    unittest.main()
