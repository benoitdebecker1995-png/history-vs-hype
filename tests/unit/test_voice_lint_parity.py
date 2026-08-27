"""
Regression tests for older profile rules retained under creator model v3.

Docs/LLM-CRAFT-UPGRADE-PLAN.md D1: voice_lint.py is hand-transcribed from
VOICE-PROFILE.md ("update RULES here when the profile changes" per its own
docstring) with no automated check that they stay in sync. This file is that
check, sourced directly from the profile's own staged examples (not
re-derived) so a future correction that goes uncoded shows up as a failing
test instead of silent drift.

New creator-model rules and corrections belong in v3-specific tests. These
cases remain because the older direct picks are compatible evidence, not
because the legacy profile still controls active retrieval.

Usage:
    python -m pytest tests/unit/test_voice_lint_parity.py -v
"""

import unittest

from tools.voice_lint import (
    scan_understand_go_back,
    scan_patterns,
    scan_cta_position,
    mask_comments,
    mask_appendix_sections,
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


class TestCtaPositionReconciliation(unittest.TestCase):
    """2026-07-19: scan_cta_position resolved a real contradiction with
    CALIBRATION-CORPUS 57-20 / EVAL-BASELINE.md R22 — the original rule
    (CTA must be in the final 5%) HARD-flagged #57/#58's own validated
    lock-time CTA placement (~70%, closer ends on a document beat after it).
    """

    def _make_lines(self, before_words: int, cta_sentence: str, after_words: int):
        # Build a script where the CTA sits at a known word-position with a
        # known amount of content following, so scan_cta_position's math is
        # exercised directly rather than guessed at from a real script.
        before = " ".join(f"word{i}" for i in range(before_words)) + "."
        after = " ".join(f"tail{i}" for i in range(after_words)) + "." if after_words else ""
        lines = [before, "", cta_sentence]
        if after:
            lines += ["", after]
        return mask_comments(lines)

    def test_validated_70pct_cta_with_document_close_not_flagged(self):
        # ~70% position, ~370 words follow (matches #58's actual shape).
        lines = self._make_lines(700, "If you like that, subscribe.", 370)
        findings = scan_cta_position("test.md", lines)
        self.assertEqual(findings, [], "validated ~70%-with-close pattern must not be flagged")

    def test_genuinely_early_cta_still_flagged(self):
        # ~20% position — well below the validated pattern, still premature.
        lines = self._make_lines(200, "Please subscribe to the channel.", 800)
        findings = scan_cta_position("test.md", lines)
        rule_ids = {f.rule for f in findings}
        self.assertIn("cta-too-early", rule_ids, "a genuinely early CTA must still fire")

    def test_cta_ending_the_video_still_flagged(self):
        # Matches the actual R22 FAIL case (REGEN-58-v18: CTA at ~100%, nothing after).
        lines = self._make_lines(1000, "If that's the history you want, subscribe.", 0)
        findings = scan_cta_position("test.md", lines)
        rule_ids = {f.rule for f in findings}
        self.assertIn("cta-ends-video", rule_ids, "a CTA the video ends on must still fire")


class TestAppendixSectionMasking(unittest.TestCase):
    """2026-07-19: voice_lint.py misread '## VERIFICATION NOTES' bibliography
    bullets as staccato spoken prose (real bug found on #56's actual script).
    """

    def test_verification_notes_section_is_blanked(self):
        lines = [
            "The empire ruled for three centuries.",
            "",
            "## VERIFICATION NOTES",
            "- Manning citation: Ch. 5, p. 106",
            "- Zurara poisoned arrows: Ch. LXXXVI, p. 402",
        ]
        masked = mask_appendix_sections(lines)
        self.assertEqual(len(masked), len(lines), "line count must be preserved")
        self.assertEqual(masked[0], lines[0], "content before the heading is untouched")
        self.assertEqual(masked[3].strip(), "", "citation bullets under the heading are blanked")
        self.assertEqual(masked[4].strip(), "", "citation bullets under the heading are blanked")

    def test_sources_section_is_also_blanked(self):
        lines = ["Spoken line.", "## SOURCES CITED", "- Some Author, p. 12"]
        masked = mask_appendix_sections(lines)
        self.assertEqual(masked[0], lines[0])
        self.assertEqual(masked[2].strip(), "")

    def test_no_appendix_heading_leaves_lines_untouched(self):
        lines = ["The empire ruled for three centuries.", "It fell in 1923."]
        masked = mask_appendix_sections(lines)
        self.assertEqual(masked, lines)


if __name__ == "__main__":
    unittest.main()
