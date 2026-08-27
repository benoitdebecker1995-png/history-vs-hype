"""Tests for tools/preflight/claim_status.py — the graded evidence gate (ADR-0021).

Each test below pins a failure that actually occurred in project #66 on 2026-07-30.
They are regression tests for a research process, not for a parser.
"""

import io
import os
import subprocess
import sys
from contextlib import contextmanager
from pathlib import Path

import pytest

from tools.preflight.claim_status import LADDER, WEIGHT, check_file, check_text, main

REPO_ROOT = Path(__file__).resolve().parents[1]


def _rules(res):
    return {v["rule"] for v in res["violations"]}


class TestLadder:
    def test_ladder_is_ordered_and_weighted(self):
        assert LADDER[0] == "ASSERTED"
        assert LADDER[-1] == "SETTLED"
        # CONTESTED sits BESIDE corroborated, not above it — a contested claim is
        # evidentially strong but not settled.
        assert WEIGHT["CONTESTED"] == WEIGHT["CORROBORATED"]
        assert WEIGHT["ASSERTED"] < WEIGHT["SOURCED"] < WEIGHT["INSPECTED"]
        assert WEIGHT["CORROBORATED"] < WEIGHT["SETTLED"]


class TestR1VerdictWords:
    """The #66 failure: 'R1 REFUTED' written from a single uncorroborated source."""

    def test_verdict_at_inspected_fails(self):
        res = check_text("- [INSPECTED] REFUTED: the cash-crop claim. FIC p.42.")
        assert res["verdict"] == "FAIL"
        assert "R1" in _rules(res)

    def test_verdict_at_corroborated_passes(self):
        res = check_text(
            "- [CORROBORATED] REFUTED: food shipped to England. FIC p.42 + Behrens p.352."
        )
        assert res["verdict"] == "PASS"

    def test_verdict_with_no_tag_fails(self):
        res = check_text("## THE HINGE — RESOLVED FROM THE PRIMARY RECORD")
        assert res["verdict"] == "FAIL"
        assert "R1" in _rules(res)

    def test_prose_about_the_rules_is_not_flagged(self):
        """The ladder documentation itself must not trip the checker."""
        res = check_text(
            "R1 says verdict words may only appear at CORROBORATED or above.\n"
            "This rule requires a locator; the vocabulary is graded."
        )
        assert res["verdict"] == "PASS"


class TestR2Circularity:
    """The #66 hinge failure: FIC supply data used to adjudicate a dispute about FIC data."""

    def test_declared_circular_cannot_exceed_inspected(self):
        res = check_text(
            "- [CORROBORATED] Supply was adequate. circular: FIC judging FIC. p.209"
        )
        assert res["verdict"] == "FAIL"
        assert "R2" in _rules(res)

    def test_circular_at_inspected_is_allowed(self):
        res = check_text(
            "- [INSPECTED] Supply was 43 weeks. circular: FIC's own estimate. p.209"
        )
        assert res["verdict"] == "PASS"


class TestR3Locator:
    """The #66 failure: 'Sen is FREE' asserted from a search hit, no metadata check."""

    def test_inspected_without_locator_fails(self):
        res = check_text("- [INSPECTED] Sen is freely downloadable.")
        assert res["verdict"] == "FAIL"
        assert "R3" in _rules(res)

    def test_locator_forms_are_accepted(self):
        for loc in ("p. 42", "pp. 155-158", "CAB 65/36", "ch. XVI", "`identifier-x`"):
            res = check_text(f"- [INSPECTED] A claim with a locator {loc}.")
            assert res["verdict"] == "PASS", loc

    def test_roman_numeral_pages_are_locators(self):
        """Front matter is roman-numbered; #67 quoted Bowersock's introduction at p. ix."""
        for loc in ("p. ix", "pp. ix-x", "p. xvi", "page xiv", "p. xliv"):
            res = check_text(f"- [CORROBORATED] A claim from the introduction, {loc}.")
            assert res["verdict"] == "PASS", loc

    def test_roman_branch_does_not_swallow_english_words(self):
        """'civil' and 'did' are spelled from the roman letter set but are not numerals."""
        for near_miss in ("p. civil", "page did", "pp. mild"):
            res = check_text(f"- [CORROBORATED] A claim citing {near_miss} and nothing else.")
            assert res["verdict"] == "FAIL", near_miss

    def test_below_inspected_needs_no_locator(self):
        res = check_text("- [ASSERTED] A model said the figure was 188,000 tons.")
        assert res["verdict"] == "PASS"


class TestR4Settled:
    def test_settled_requires_named_opposition(self):
        res = check_text("- [SETTLED] Denial policy caused hoarding. FIC p.26.")
        assert res["verdict"] == "FAIL"
        assert "R4" in _rules(res)

    def test_settled_with_opposition_passes(self):
        res = check_text(
            "- [SETTLED] Export bans were real. FIC p.24. opposed-by: none in Roy (2012) ch.4."
        )
        assert res["verdict"] == "PASS"


class TestFileHandling:
    def test_missing_file_returns_error_dict_not_raise(self):
        res = check_file("does/not/exist.md")
        assert "error" in res
        assert "no such file" in res["error"]

    def test_counts_and_tallies(self, tmp_path):
        f = tmp_path / "r.md"
        f.write_text(
            "- [ASSERTED] x\n- [SOURCED] y\n- [INSPECTED] z p.1\n",
            encoding="utf-8",
        )
        res = check_file(str(f))
        assert res["claims"] == 3
        assert res["by_status"]["ASSERTED"] == 1
        assert res["by_status"]["INSPECTED"] == 1
        assert res["verdict"] == "PASS"


class TestFrontier:
    """The #66 failure: research reported finished twice while obtainable sources
    remained unread. The owner had to ask 'Why did you stop?' both times."""

    def test_open_thread_blocks_completion(self):
        from tools.preflight.claim_status import frontier

        res = frontier("- [SOURCED] Bowbrick 1986. next: buy article")
        assert res["verdict"] == "OPEN"
        assert res["open"][0]["next"].startswith("buy")

    def test_next_none_closes_a_thread(self):
        from tools.preflight.claim_status import frontier

        res = frontier("- [INSPECTED] Net importer. FIC p.42. next: none — settled by table")
        assert res["verdict"] == "COMPLETE"
        assert len(res["closed"]) == 1

    def test_untracked_claim_blocks_completion(self):
        from tools.preflight.claim_status import frontier

        res = frontier("- [SOURCED] Greenough on provincial failure")
        assert res["verdict"] == "OPEN"
        assert len(res["untracked"]) == 1

    def test_corroborated_claims_are_not_frontier_items(self):
        from tools.preflight.claim_status import frontier

        res = frontier("- [CORROBORATED] Cabinet diagnosed hoarding. p.156 + p.352")
        assert res["verdict"] == "COMPLETE"
        assert res["open"] == [] and res["untracked"] == []


class TestTone:
    """The #66 failure: 'everything is the next best thing or the strongest find'."""

    def test_multiple_superlatives_go_over_budget(self):
        from tools.preflight.claim_status import tone

        res = tone(
            "This is the strongest exhibit.\nThe strongest finding yet.\nThe decisive line."
        )
        assert res["verdict"] == "OVER"
        assert res["counts"]["superlative"] >= 3

    def test_one_superlative_is_within_budget(self):
        from tools.preflight.claim_status import tone

        res = tone("The Cabinet minute is the strongest exhibit because it dates the decision.")
        assert res["verdict"] == "OK"

    def test_awe_words_are_counted(self):
        from tools.preflight.claim_status import tone

        res = tone("This is the mother lode. A spectacular, devastating find.")
        assert res["counts"]["awe"] >= 3

    def test_plain_prose_is_clean(self):
        from tools.preflight.claim_status import tone

        res = tone("The minute records the diagnosis and the decision, dated 4 August 1943.")
        assert res["verdict"] == "OK"
        assert res["counts"]["awe"] == 0


# ---------------------------------------------------------------------------
# Console encoding
# ---------------------------------------------------------------------------

# The repo's research files mark claims with ⛔ ⚠ ⭐ by convention, and --frontier
# echoes file text back: the whole line for an untracked claim, the next-action for an
# open thread. cp1252 has no code point for any of those glyphs.
OPEN_THREAD = "- ⛔ [SOURCED] Bowersock's introduction is unread | next: ⛔ order the Penn Press scan\n"
UNTRACKED = "- ⭐ [ASSERTED] Valla dated the forgery to the eighth century\n"


@contextmanager
def cp1252_console():
    """Run a block with sys.stdout/sys.stderr as strict cp1252 streams.

    This is what a piped stdout looks like on Windows: Python falls back to the
    ANSI codepage, and every glyph outside it is a hard UnicodeEncodeError.
    Yields a callable returning everything written to stdout so far, decoded.

    Deliberately a context manager and not a fixture: pytest re-installs its own
    sys.stdout when the call phase begins, so a swap made during fixture setup is
    silently undone before the test body runs.
    """
    out_buf, err_buf = io.BytesIO(), io.BytesIO()
    out = io.TextIOWrapper(out_buf, encoding="cp1252", errors="strict", write_through=True)
    err = io.TextIOWrapper(err_buf, encoding="cp1252", errors="strict", write_through=True)
    saved_out, saved_err = sys.stdout, sys.stderr
    sys.stdout, sys.stderr = out, err
    try:
        def read():
            out.flush()
            return out_buf.getvalue().decode("cp1252")

        yield read
    finally:
        sys.stdout, sys.stderr = saved_out, saved_err


class TestNarrowCodepageOutput:
    """The 2026-08-02 failure: `claim_status --frontier` on project #67 died with
    UnicodeEncodeError on '⛔' before printing its verdict.

    The analysis was fine — only the printing failed. But this CLI's exit code is
    the completion gate in /research, and the crash also exits 1, which is exactly
    what a genuine OPEN verdict returns. An encoding problem must never be able to
    stand in for a research verdict.
    """

    def test_the_fixtures_still_reach_the_formatter(self):
        """Guard: these tests only prove anything while the glyph actually lands in the
        rendered report. If format_frontier ever stops echoing file text, this fails
        loudly instead of the suite going quietly green on a bug it no longer covers."""
        from tools.preflight.claim_status import format_frontier, frontier

        assert "⛔" in format_frontier(frontier(OPEN_THREAD))
        assert "⭐" in format_frontier(frontier(UNTRACKED))

    def test_frontier_prints_its_verdict_through_a_cp1252_stdout(self, tmp_path):
        f = tmp_path / "01-VERIFIED-RESEARCH.md"
        f.write_text(OPEN_THREAD, encoding="utf-8")

        with cp1252_console() as stdout:
            rc = main(["--frontier", str(f)])  # must not raise
            report = stdout()

        assert "RESEARCH FRONTIER" in report
        assert "VERDICT: OPEN" in report
        # The glyph degrades to '?'; the next-action it decorates survives intact.
        assert "order the Penn Press scan" in report
        assert "⛔" not in report
        assert rc == 1  # OPEN — the verdict, reached and reported, not a crash

    def test_frontier_complete_still_exits_zero_through_a_cp1252_stdout(self, tmp_path):
        """The half a crash can never produce: a clean pass with unprintable glyphs."""
        f = tmp_path / "01-VERIFIED-RESEARCH.md"
        f.write_text(
            "- ⛔ [CORROBORATED] Valla exposed the forgery. p. ix + Bowersock p. xvi.\n"
            "- ⭐ [INSPECTED] The text survives in Cod. Vat. lat. 1984. next: none — collated\n",
            encoding="utf-8",
        )

        with cp1252_console() as stdout:
            rc = main(["--frontier", str(f)])
            report = stdout()

        assert "VERDICT: COMPLETE" in report
        assert rc == 0

    def test_untracked_claims_print_through_a_cp1252_stdout(self, tmp_path):
        f = tmp_path / "01-VERIFIED-RESEARCH.md"
        f.write_text(UNTRACKED, encoding="utf-8")

        with cp1252_console() as stdout:
            rc = main(["--frontier", str(f)])
            report = stdout()

        assert "UNTRACKED" in report
        assert "Valla dated the forgery" in report
        assert rc == 1

    def test_default_mode_prints_violations_through_a_cp1252_stdout(self, tmp_path):
        """Default mode echoes raw text too — but only for violations, which is why
        it looked healthy on the same file while --frontier died."""
        f = tmp_path / "01-VERIFIED-RESEARCH.md"
        f.write_text("- ⛔ [INSPECTED] REFUTED: the donation is genuine.\n", encoding="utf-8")

        with cp1252_console() as stdout:
            rc = main([str(f)])
            report = stdout()

        assert "VERDICT: FAIL" in report
        assert "[R1]" in report
        assert "the donation is genuine" in report
        assert rc == 1

    def test_tone_mode_prints_hits_through_a_cp1252_stdout(self, tmp_path):
        f = tmp_path / "notes.md"
        f.write_text(
            "⭐ The strongest exhibit yet.\n⭐ A spectacular, devastating find.\n"
            "⭐ The single most important document.\n",
            encoding="utf-8",
        )

        with cp1252_console() as stdout:
            rc = main(["--tone", str(f)])
            report = stdout()

        assert "VERDICT: OVER" in report
        assert "strongest" in report
        assert rc == 0  # tone is a signal, not a gate

    def test_ladder_prints_through_a_cp1252_stdout(self):
        """--ladder prints the module docstring, which carries ✅ ⏳ ❌ of its own:
        a second crash path in the same file, independent of any input file."""
        with cp1252_console() as stdout:
            rc = main(["--ladder"])
            report = stdout()

        assert "THE LADDER" in report
        assert "CORROBORATED" in report
        assert rc == 0

    def test_missing_file_error_still_reaches_stdout(self):
        with cp1252_console() as stdout:
            rc = main(["--frontier", "does/not/exist.md"])
            report = stdout()

        assert "no such file" in report
        assert rc == 1

    @pytest.mark.parametrize(
        "args, expected_rc, expected_text",
        [(["--frontier"], 1, "VERDICT: OPEN"), (["--ladder"], 0, "THE LADDER")],
    )
    def test_cli_survives_a_cp1252_console_end_to_end(
        self, tmp_path, args, expected_rc, expected_text
    ):
        """Subprocess pin of the reported repro: PYTHONIOENCODING=cp1252 is what the
        owner's console does, and it is the only way to prove the real interpreter
        stdout — not a monkeypatched one — carries the verdict out."""
        f = tmp_path / "01-VERIFIED-RESEARCH.md"
        f.write_text(OPEN_THREAD, encoding="utf-8")
        cmd = [sys.executable, "-m", "tools.preflight.claim_status", *args]
        if "--ladder" not in args:
            cmd.append(str(f))

        env = {**os.environ, "PYTHONIOENCODING": "cp1252"}
        proc = subprocess.run(
            cmd, cwd=REPO_ROOT, env=env, capture_output=True, text=True,
            encoding="cp1252", errors="replace",
        )

        assert "UnicodeEncodeError" not in proc.stderr
        assert expected_text in proc.stdout
        assert proc.returncode == expected_rc
