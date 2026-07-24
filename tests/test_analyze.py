"""Tests for analyze.run_analysis via the AnalysisSource seam.

run_analysis had zero tests because it fetched live YouTube/DB data directly.
Feeding it an InMemoryAnalysisSource (ADR-0011) lets us check the assembled
report AND every partial-failure branch against known input — no network.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.youtube_analytics.analyze import run_analysis  # noqa: E402
from tools.youtube_analytics.analysis_source import (  # noqa: E402
    InMemoryAnalysisSource,
    LiveAnalysisSource,
)

VID = "dQw4w9WgXcQ"  # valid 11-char id


def _video_report(**over):
    base = {
        "title": "My Video",
        "engagement": {"views": 1500, "subscribers_gained": 20, "likes": 100, "comments": 30},
        "retention": {"avg_retention": 0.30},
        "ctr": {"ctr_percent": 4.0, "available": True, "impressions": 1000},
        "errors": [],
    }
    base.update(over)
    return base


def _comments():
    return {
        "total_fetched": 5,
        "categories": {"questions": ["q1"], "objections": [], "requests": ["r1"], "other": []},
    }


def _ok_source(**over):
    """A source where the core fetches succeed; video_metrics short-circuits the
    comparison (compare_to_channel is real synthesis, exercised separately)."""
    kw = dict(
        video_report=_video_report(),
        comments=_comments(),
        channel_averages={"avg_views": 1000},
        video_metrics={"error": "skip comparison"},
    )
    kw.update(over)
    return InMemoryAnalysisSource(**{k: v for k, v in kw.items() if k != "raises"},
                                  raises=over.get("raises"))


def test_happy_path_assembles_report():
    r = run_analysis(VID, source=_ok_source())
    assert r["video_id"] == VID
    assert r["title"] == "My Video"
    assert r["engagement"]["views"] == 1500
    assert r["ctr"]["ctr_percent"] == 4.0
    assert r["retention"]["avg_retention"] == 0.30
    assert r["comments"]["total"] == 5
    assert r["comments"]["questions"] == ["q1"]
    assert r["benchmarks"]["channel_averages"] == {"avg_views": 1000}
    assert r["benchmarks"]["comparison"] is None
    assert isinstance(r["lessons"], dict) and "observations" in r["lessons"]
    assert r["errors"] == []


def test_manual_ctr_override():
    r = run_analysis(VID, manual_ctr=7.5, source=_ok_source())
    assert r["ctr"]["ctr_percent"] == 7.5
    assert r["ctr"]["source"] == "manual"


def test_comments_error_collected_and_zeroed():
    r = run_analysis(VID, source=_ok_source(comments={"error": "quota exceeded"}))
    assert any(e["source"] == "comments" for e in r["errors"])
    assert r["comments"]["total"] == 0
    assert r["comments"]["questions"] == []


def test_channel_averages_error_nulls_benchmarks():
    r = run_analysis(VID, source=_ok_source(channel_averages={"error": "no data"}))
    assert any(e["source"] == "channel_averages" for e in r["errors"])
    assert r["benchmarks"]["channel_averages"] is None
    assert r["benchmarks"]["comparison"] is None


def test_video_report_errors_propagate():
    src = _ok_source(video_report=_video_report(errors=[{"source": "retention", "message": "no curve"}]))
    r = run_analysis(VID, source=src)
    assert any(e["source"] == "retention" for e in r["errors"])


def test_variant_fetch_failure_collected():
    src = _ok_source(raises={"variant_data": RuntimeError("db locked")})
    r = run_analysis(VID, source=src)
    assert any(e["source"] == "variants" for e in r["errors"])
    assert r["variants"] is None


def test_ctr_analysis_runs_when_variants_present():
    variants = {"summary": {"thumbnails": 2, "titles": 1, "snapshots": 3},
                "thumbnails": [], "titles": [], "snapshots": []}
    ctr = {"thumbnail_verdict": {"winner": "A"}, "title_verdict": {"winner": "B"}, "benchmarks": {}}
    r = run_analysis(VID, source=_ok_source(variant_data=variants, ctr_analysis=ctr))
    assert r["variants"] == variants
    assert r["ctr_analysis"] == ctr


def test_ctr_analysis_failure_collected():
    variants = {"summary": {"thumbnails": 1, "titles": 0, "snapshots": 0},
                "thumbnails": [], "titles": [], "snapshots": []}
    src = _ok_source(variant_data=variants, raises={"ctr_analysis": RuntimeError("benchmark fail")})
    r = run_analysis(VID, source=src)
    assert any(e["source"] == "ctr_analysis" for e in r["errors"])


def test_no_variants_means_no_ctr_analysis_call():
    # variant_data None (default) -> ctr_analysis must not even be attempted
    src = _ok_source(raises={"ctr_analysis": RuntimeError("should never be called")})
    r = run_analysis(VID, source=src)
    assert r["ctr_analysis"] is None
    assert not any(e["source"] == "ctr_analysis" for e in r["errors"])


def test_invalid_input_early_return():
    r = run_analysis("this is not a video", source=InMemoryAnalysisSource())
    assert r["title"] is None
    assert any(e["source"] == "input" for e in r["errors"])


def test_bare_fake_runs_offline():
    r = run_analysis(VID, source=InMemoryAnalysisSource())
    assert {"video_id", "title", "lessons", "errors", "benchmarks", "comments"} <= set(r)


def test_unknown_source_kwarg_rejected():
    import pytest
    with pytest.raises(TypeError):
        InMemoryAnalysisSource(nonsense={})


def test_live_source_conforms_to_interface():
    live = LiveAnalysisSource()
    for m in ("video_report", "comments", "channel_averages",
              "video_metrics", "variant_data", "ctr_analysis"):
        assert callable(getattr(live, m))
