"""Tests for tools/preflight/serp_thumb_study.py.

Pins the 2026-07-30 defect found running the study for project #65: all 8 Gemini
Flash vision calls failed (`gemini` was not on PATH — exit 127, empty stdout), the
header honestly said `Tagged: 0/8`, and the tool nonetheless wrote

    ## Whitespace (operations ABSENT from this shelf — attack here)
    - COMPRESSION, TITLE_REPETITION, MECHANISM_REFRAME, VISUAL_ANSWER, NO_OVERLAY, ...

i.e. every operation, because none were observed — plus `Face present: 0/0 (0%)`.
`/thumbnail` Step 2.6 reads that whitespace line as "the gap to occupy". Absence of
a result rendered as evidence of absence (ADR-0020).
"""

import subprocess

import pytest

from tools.preflight import serp_thumb_study as sts
from tools.preflight.serp_thumb_study import (
    MIN_TAGGED_FRACTION,
    GeminiUnavailable,
    _aggregate,
    build_study,
    run,
    tag_thumbnail,
)

TAGS = {
    "overlay_text": "THE REAL STORY",
    "overlay_words": 3,
    "framing": "declarative",
    "face": True,
    "map": False,
    "dominant_colors": ["red", "black"],
    "subject": "man beside a cipher machine",
    "operation": "COMPRESSION",
}


def _records(total, tagged, error="unparseable response — exit 127, stdout='', stderr=''"):
    out = []
    for i in range(total):
        r = {"id": f"vid{i:04d}", "title": f"T{i}", "channel": f"Chan{i}", "views": 1000 - i}
        if i < tagged:
            r["tags"], r["tag_error"] = dict(TAGS), ""
        else:
            r["tags"], r["tag_error"] = None, error
        out.append(r)
    return out


def _has_claims(md):
    """True if the report makes any composition or whitespace claim.

    These are the exact strings a downstream reader keys on — `/thumbnail`
    Step 2.6 lifts the line under `## Whitespace`.
    """
    return ("## Whitespace" in md
            or "## Shelf composition" in md
            or "Face present" in md
            or "Map present" in md)


class TestAggregateRefusesUnobservedShelves:
    def test_zero_tagged_yields_none_absent_ops_not_a_full_list(self):
        a = _aggregate(_records(8, 0))
        assert a["n"] == 0 and a["total"] == 8
        assert a["reliable"] is False
        # The old code returned every operation here — the strongest possible
        # whitespace claim from zero evidence.
        assert a["absent_ops"] is None

    def test_below_threshold_is_unreliable(self):
        a = _aggregate(_records(8, 3))  # 37.5% < 50%
        assert a["reliable"] is False
        assert a["absent_ops"] is None

    def test_at_threshold_is_reliable(self):
        a = _aggregate(_records(8, 4))  # exactly 50%
        assert a["reliable"] is True
        assert a["coverage"] == pytest.approx(MIN_TAGGED_FRACTION)
        assert isinstance(a["absent_ops"], list)

    def test_full_coverage_absent_ops_excludes_observed_operation(self):
        a = _aggregate(_records(8, 8))
        assert a["reliable"] is True
        assert "COMPRESSION" not in a["absent_ops"]
        assert "NO_OVERLAY" in a["absent_ops"]

    def test_empty_record_set_is_not_reliable(self):
        a = _aggregate([])
        assert a["reliable"] is False and a["absent_ops"] is None


class TestZeroTagRunMakesNoClaims:
    def test_no_whitespace_or_composition_section(self):
        md = build_study("65-enigma-polish", _records(8, 0))
        assert not _has_claims(md)
        # Specifically, the #65 output line must not be reproducible.
        assert "MECHANISM_REFRAME, VISUAL_ANSWER" not in md
        assert "0/0 (0%)" not in md

    def test_emits_a_failure_block_naming_what_failed_and_how_many(self):
        md = build_study("65-enigma-polish", _records(8, 0))
        assert "STUDY FAILED" in md
        assert "0 of 8 thumbnails tagged" in md
        assert "(8x)" in md  # failure reason with its count
        assert "exit 127" in md

    def test_run_exits_non_zero(self, tmp_path, monkeypatch):
        res = _fake_run(tmp_path, monkeypatch, total=3, ok=0)
        assert res["ok"] is False
        assert res["tagged"] == 0 and res["total"] == 3
        assert not _has_claims((tmp_path / "s.md").read_text(encoding="utf-8"))


class TestPartialTagRunBelowThresholdMakesNoClaims:
    def test_no_whitespace_or_composition_section(self):
        md = build_study("partial", _records(8, 3))
        assert not _has_claims(md)
        assert "3 of 8 thumbnails tagged (38%)" in md

    def test_run_exits_non_zero(self, tmp_path, monkeypatch):
        res = _fake_run(tmp_path, monkeypatch, total=8, ok=3)
        assert res["ok"] is False
        assert res["tagged"] == 3
        assert not _has_claims((tmp_path / "s.md").read_text(encoding="utf-8"))


class TestFullTagRunStillWritesTheNormalReport:
    def test_report_has_composition_and_whitespace(self):
        md = build_study("gibraltar", _records(8, 8))
        assert "## Shelf composition" in md
        assert "**Face present:** 8/8 (100%)" in md
        assert "## Whitespace (operations ABSENT from this shelf" in md
        assert "NO_OVERLAY" in md
        assert "STUDY FAILED" not in md

    def test_run_reports_ok(self, tmp_path, monkeypatch):
        res = _fake_run(tmp_path, monkeypatch, total=4, ok=4)
        assert res["ok"] is True and res["tagged"] == 4
        md = (tmp_path / "s.md").read_text(encoding="utf-8")
        assert "## Shelf composition" in md and "## Whitespace" in md

    def test_above_threshold_but_partial_carries_a_sample_caveat(self, tmp_path, monkeypatch):
        md = build_study("partial-ok", _records(8, 6))  # 75% — reliable
        assert "## Whitespace" in md
        assert "read off **6 of 8**" in md
        assert "absent from the tagged sample" in md


class TestGeminiFailureIsDiagnosable:
    """The 2026-07-30 root cause: a missing CLI exits 127 with EMPTY stdout, so the
    old `unparseable tag for X: %s` printed nothing after the colon."""

    def test_exit_127_raises_instead_of_looking_like_a_parse_failure(self, tmp_path, monkeypatch):
        monkeypatch.setattr(subprocess, "run", lambda *a, **k: subprocess.CompletedProcess(
            args=a, returncode=127, stdout="", stderr="bash: line 1: gemini: command not found"))
        with pytest.raises(GeminiUnavailable) as e:
            tag_thumbnail(tmp_path / "x.jpg")
        assert "command not found" in str(e.value)

    def test_parse_failure_reason_carries_both_streams_and_exit_code(self, tmp_path, monkeypatch):
        monkeypatch.setattr(subprocess, "run", lambda *a, **k: subprocess.CompletedProcess(
            args=a, returncode=1, stdout="Quota exceeded.", stderr="429 RESOURCE_EXHAUSTED"))
        tags, reason = tag_thumbnail(tmp_path / "x.jpg")
        assert tags is None
        assert "exit 1" in reason
        assert "Quota exceeded." in reason
        assert "429 RESOURCE_EXHAUSTED" in reason

    def test_valid_response_parses(self, tmp_path, monkeypatch):
        import json as _json
        monkeypatch.setattr(subprocess, "run", lambda *a, **k: subprocess.CompletedProcess(
            args=a, returncode=0, stdout="```json\n" + _json.dumps(TAGS) + "\n```", stderr=""))
        tags, reason = tag_thumbnail(tmp_path / "x.jpg")
        assert reason == "" and tags["operation"] == "COMPRESSION"

    def test_missing_cli_aborts_the_run_without_downloading(self, tmp_path, monkeypatch):
        calls = []
        monkeypatch.setattr(sts, "_gemini_probe", lambda: None)
        monkeypatch.setattr(sts, "_download_serp", lambda ids: calls.append(ids) or [])
        monkeypatch.setattr(sts, "tag_thumbnail", lambda p, retries=1: pytest.fail("must not tag"))
        res = run("slug", [], "a,b,c", 8, str(tmp_path / "s.md"))
        assert res["ok"] is False and "not found on PATH" in res["aborted"]
        assert calls == []  # no thumbnails fetched for a run that cannot classify

    def test_mid_run_unavailability_aborts_the_rest(self, tmp_path, monkeypatch):
        seen = []

        def _tag(p, retries=1):
            seen.append(p)
            raise GeminiUnavailable("`gemini` is not runnable here (exit 127): ...")

        monkeypatch.setattr(sts, "_gemini_probe", lambda: "/usr/bin/gemini")
        monkeypatch.setattr(sts, "_download_serp",
                            lambda ids: [tmp_path / f"{i}.jpg" for i in ids])
        monkeypatch.setattr(sts, "tag_thumbnail", _tag)
        res = run("slug", [], "a,b,c,d", 8, str(tmp_path / "s.md"))
        assert len(seen) == 1  # abort after the first, not 4 identical failures
        assert res["ok"] is False


class TestSynthesizeExcludesUnderTaggedStudies:
    def test_a_zero_tag_study_does_not_become_durable_whitespace(self, tmp_path):
        import json

        (tmp_path / "broken-2026-07-30.json").write_text(
            json.dumps(_records(8, 0)), encoding="utf-8")
        with pytest.raises(SystemExit) as e:
            sts.synthesize(tmp_path)
        assert "0/8 tagged" in str(e.value)

    def test_reliable_studies_still_synthesize(self, tmp_path):
        import json

        for slug in ("alpha", "beta"):
            (tmp_path / f"{slug}-2026-07-30.json").write_text(
                json.dumps(_records(8, 8)), encoding="utf-8")
        (tmp_path / "broken-2026-07-30.json").write_text(
            json.dumps(_records(8, 1)), encoding="utf-8")
        path = sts.synthesize(tmp_path)
        md = __import__("pathlib").Path(path).read_text(encoding="utf-8")
        assert "**Studies analyzed:** 2" in md
        assert "broken (1/8 tagged)" in md
        # COMPRESSION was observed in both -> never proposed as whitespace.
        assert "Operation COMPRESSION is chronically absent" not in md
        assert "Operation NO_OVERLAY is chronically absent" in md


def _fake_run(tmp_path, monkeypatch, total, ok):
    """Drive run() with the network + Gemini stubbed out."""
    ids = [f"vid{i:04d}" for i in range(total)]
    monkeypatch.setattr(sts, "_gemini_probe", lambda: "/usr/bin/gemini")
    monkeypatch.setattr(sts, "_download_serp",
                        lambda vids: [tmp_path / f"{v}.jpg" for v in vids])
    order = iter(range(total))
    monkeypatch.setattr(
        sts, "tag_thumbnail",
        lambda p, retries=1: (dict(TAGS), "") if next(order) < ok
        else (None, "unparseable response — exit 127, stdout='', stderr=''"),
    )
    return run("slug", [], ",".join(ids), total, str(tmp_path / "s.md"))
