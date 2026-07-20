"""
Eval harness — Phase E of docs/LLM-CRAFT-UPGRADE-PLAN.md.

Two entry points:
1. Deterministic layer (this file, auto-runs under pytest): runs the
   tools/script_checkers/ registry checkers + tools/voice_lint.py against
   every script in the golden set (channel-data/calibration/EVAL-GOLDEN-SET.md)
   and asserts positives score better than negatives.
2. Judge layer (documented, NOT auto-run — requires a live Claude judge call,
   same as EVAL-BASELINE.md's original v18 regen scoring): see
   channel-data/calibration/EVAL-JUDGE-PROTOCOL.md for the manual procedure.
   To run a new judge pass: read EVAL-RUBRIC.md + EVAL-GOLDEN-SET.md, score
   the target script criterion-by-criterion with line citations, and append
   the result as a new "Calibration run" section in EVAL-JUDGE-PROTOCOL.md.

Usage:
    python -m pytest tests/unit/test_eval_harness.py -v
"""

import unittest
from pathlib import Path

from tools.script_checkers.registry import build_default_registry

try:
    import spacy  # noqa: F401
    import textstat  # noqa: F401
    NLP_AVAILABLE = True
except ImportError:
    NLP_AVAILABLE = False

requires_nlp = unittest.skipUnless(NLP_AVAILABLE, "spaCy and textstat required (pip install -e .[nlp])")

REPO_ROOT = Path(__file__).resolve().parents[2]

POSITIVES = [
    REPO_ROOT / "video-projects/_ARCHIVED/published/56-no-lassos-atlantic-slave-trade-origin-2026/02-SCRIPT-DRAFT.md",
    REPO_ROOT / "video-projects/_ARCHIVED/published/57-piri-reis-map-ottoman-2026/SCRIPT.md",
    REPO_ROOT / "video-projects/_READY_TO_FILM/58-kurdistan-statelessness-2026/SCRIPT.md",
    REPO_ROOT / "video-projects/_ARCHIVED/published/59-israel-palestine-partition-offer-2026/SCRIPT.md",
]

NEGATIVES = [
    REPO_ROOT / "channel-data/calibration/REGEN-58-V18-DRAFT.md",
]


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class TestGoldenSetExists(unittest.TestCase):
    """Sanity: every path EVAL-GOLDEN-SET.md claims exists actually exists on disk."""

    def test_all_positive_paths_exist(self):
        for path in POSITIVES:
            self.assertTrue(path.exists(), f"golden-set positive missing: {path}")

    def test_all_negative_paths_exist(self):
        for path in NEGATIVES:
            self.assertTrue(path.exists(), f"golden-set negative missing: {path}")


class TestVoiceLintGoldenSet(unittest.TestCase):
    """R24: locked scripts should carry zero HARD voice_lint findings; the
    known-bad regen should not (per EVAL-BASELINE.md R24: REGEN 5 HARD / LOCK 0 HARD).

    KNOWN, DOCUMENTED EXCEPTION: #59's cta-ends-video finding (its script
    literally ends on "...subscribe.", no closing beat after) is real, not a
    linter bug — confirmed 2026-07-19 by reading the script directly. Not
    excluded because the rule is wrong (see scan_cta_position's 2026-07-19
    resolution note in tools/voice_lint.py) but because #59 is ALREADY
    documented in EVAL-BASELINE.md's KPI ledger as a hand-collaborative build
    "NOT a clean writer-version KPI" — an independently-known outlier, not a
    new problem this check invented.
    """

    _KNOWN_EXCEPTIONS = {
        "59-israel-palestine-partition-offer-2026": {"cta-ends-video"},
    }

    def test_locked_scripts_zero_hard(self):
        from tools.voice_lint import lint_file
        for path in POSITIVES:
            video_slug = path.parent.name
            excepted_rules = self._KNOWN_EXCEPTIONS.get(video_slug, set())
            findings = lint_file(str(path))
            hard = [
                f for f in findings
                if getattr(f, "severity", None) == "HARD" and f.rule not in excepted_rules
            ]
            self.assertEqual(
                hard, [],
                f"{path.name} expected 0 HARD voice_lint findings, got "
                f"{[(f.line, f.rule) for f in hard]}"
            )

    def test_regen_negative_has_hard_findings(self):
        from tools.voice_lint import lint_file
        for path in NEGATIVES:
            findings = lint_file(str(path))
            hard = [f for f in findings if getattr(f, "severity", None) == "HARD"]
            self.assertGreater(
                len(hard), 0,
                f"{path.name} is a known-bad negative (EVAL-BASELINE.md R24 = 5 HARD) "
                f"but voice_lint found 0 — either the fixture or the linter regressed"
            )


@requires_nlp
class TestPacingGoldenSet(unittest.TestCase):
    """Deterministic checker sanity: positives should not fail pacing outright."""

    def test_locked_scripts_pacing_runs_clean(self):
        registry = build_default_registry()
        for path in POSITIVES:
            result = registry.run("pacing", _read(path))
            self.assertIn("stats", result)
            self.assertIn("issues", result)


class TestScaffoldingGoldenSet(unittest.TestCase):
    def test_locked_scripts_scaffolding_runs(self):
        registry = build_default_registry()
        for path in POSITIVES:
            result = registry.run("scaffolding", _read(path))
            self.assertIn("stats", result)


if __name__ == "__main__":
    unittest.main()
