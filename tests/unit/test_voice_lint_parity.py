"""
Unit tests for voice_lint.py <-> VOICE-PROFILE.md parity.

Docs/LLM-CRAFT-UPGRADE-PLAN.md D1: voice_lint.py is hand-transcribed from
VOICE-PROFILE.md ("update RULES here when the profile changes" per its own
docstring) with no automated check that they stay in sync. This file is that
check, sourced directly from the profile's own staged examples (not
re-derived) so a future correction that goes uncoded shows up as a failing
test instead of silent drift.

When VOICE-PROFILE.md stages a NEW lint-rule correction, add its examples
here as a new test case — that's what "parity" means in practice for a tool
transcribed from prose (a full NLP-parse of the profile would be brittle and
is not attempted).

Usage:
    python -m pytest tests/unit/test_voice_lint_parity.py -v
"""

import unittest

from tools.voice_lint import (
    scan_understand_go_back,
    scan_patterns,
    mask_comments,
)


class TestUnderstandGoBackException(unittest.TestCase):
    """VOICE-PROFILE.md ~line 505: T7 demoted HARD -> WARN-with-exception.

    His own 2026-07-15 _adlib/ ad-libs (verbatim, quoted in the profile):
      "In order to understand why it happened, we first have to agree…"
      "In order to understand how this massacre could happen, we have to go
       back to 1918"
    Both are HIS voice (a walked chain follows) and must NOT fire, even at WARN.
    """

    def _run(self, text: str):
        lines = mask_comments(text.splitlines())
        return scan_understand_go_back("test.md", lines)

    def test_exception_walked_chain_with_year_not_flagged(self):
        findings = self._run(
            "In order to understand how this massacre could happen, we have "
            "to go back to 1918 and the collapse of the empire that followed it."
        )
        self.assertEqual(findings, [], "walked chain with a year must be excepted, not flagged")

    def test_exception_walked_chain_long_continuation_not_flagged(self):
        findings = self._run(
            "In order to understand why it happened, we first have to agree "
            "on what actually happened on the ground before anyone signed anything."
        )
        self.assertEqual(findings, [], "walked chain with a long continuation must be excepted")

    def test_bare_transition_still_flagged_as_warn(self):
        findings = self._run(
            "To understand this, we have to go back."
        )
        self.assertEqual(len(findings), 1, "bare/empty transition with no walked chain must still fire")
        self.assertEqual(findings[0].severity, "WARN", "must be WARN, not HARD, post-demotion")
        self.assertEqual(findings[0].rule, "understand-go-back")

    def test_no_longer_hard_via_scan_patterns(self):
        """The rule must be fully removed from HARD_REGEXES — scan_patterns()
        (the HARD-literal/regex scanner) must never emit it, even on the bare form."""
        lines = mask_comments(["To understand this, we have to go back."])
        findings = scan_patterns("test.md", lines)
        rule_ids = {f.rule for f in findings}
        self.assertNotIn("understand-go-back", rule_ids, "must not appear via the HARD scanner")


class TestNowCommaException(unittest.TestCase):
    """VOICE-PROFILE.md ~line 505: 'Now,' excepted from youtuber-opener;
    only the empty 'Now —' camera-turn stays banned."""

    def _run(self, lines: list):
        masked = mask_comments(lines)
        return scan_patterns("test.md", masked)

    def test_relevance_scaffold_now_comma_not_flagged(self):
        # His own ad-lib phrasing, VOICE-PROFILE.md ~line 505.
        findings = self._run(["Now, it is important to mention that the treaty was never ratified."])
        rule_ids = {f.rule for f in findings}
        self.assertNotIn("youtuber-opener", rule_ids, "'Now,' relevance-scaffold opener is his voice, must not fire")

    def test_empty_camera_turn_now_dash_still_flagged(self):
        findings = self._run(["Now — let's get into it."])
        rule_ids = {f.rule for f in findings}
        self.assertIn("youtuber-opener", rule_ids, "empty 'Now —' camera-turn must still be banned")

    def test_look_comma_still_flagged(self):
        findings = self._run(["Look, this is the part everyone gets wrong."])
        rule_ids = {f.rule for f in findings}
        self.assertIn("youtuber-opener", rule_ids, "'Look,' is unaffected by this correction, must still fire")


if __name__ == "__main__":
    unittest.main()
