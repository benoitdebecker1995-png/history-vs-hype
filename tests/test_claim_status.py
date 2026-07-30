"""Tests for tools/preflight/claim_status.py — the graded evidence gate (ADR-0021).

Each test below pins a failure that actually occurred in project #66 on 2026-07-30.
They are regression tests for a research process, not for a parser.
"""

from tools.preflight.claim_status import LADDER, WEIGHT, check_file, check_text


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
