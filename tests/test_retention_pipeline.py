"""High-level pinning test for the retention pipeline (Phase G safety net).

This test exercises the *current* surface of the 7 retention modules in their
natural composition order:

    retention.py          -> find_drop_off_points (synthetic input — API skipped)
    retention_mapper.py   -> map_retention_to_sections
    retention_decoder.py  -> RetentionDecoder.classify_hook_type / classify_specificity
    retention_scorer.py   -> score_section / score_all_sections
    retention_predictor.py -> predict_from_text
    retention_by_topic.py -> classify_topic
    retention_analysis.py -> classify_content / _normalize

The test PINS BEHAVIOR — it makes no claims about correctness, only that the
public functions still produce dicts with the documented shape. Any change to
output keys breaks this test, which is the point: it acts as a regression net
during the upcoming RetentionInference convergence (Phase G2-G4).

Notes:
- get_retention_data() requires YouTube Analytics API auth, so we substitute
  a synthetic data_points list at the entry point.
- RetentionDecoder.analyze() requires analytics.db with real video data; we
  test the classifier surface only.
- The post-publish fixture is read to assert presence (per the G1 spec).
"""
from pathlib import Path

import pytest

FIXTURES_DIR = Path(__file__).parent / "fixtures"
POST_PUBLISH_FIXTURE = FIXTURES_DIR / "test_post_publish.md"
SCRIPT_FIXTURE = FIXTURES_DIR / "test_script.md"


# ---------------------------------------------------------------------------
# 1. retention.py — drop-off detection (synthetic input)
# ---------------------------------------------------------------------------

def test_find_drop_off_points_returns_list():
    """find_drop_off_points returns a list of drop dicts with the expected keys."""
    from tools.youtube_analytics.retention import find_drop_off_points

    data_points = [
        {"position": 0.00, "retention": 1.00, "relative": None},
        {"position": 0.10, "retention": 0.95, "relative": None},
        {"position": 0.20, "retention": 0.50, "relative": None},  # 45% drop
        {"position": 0.30, "retention": 0.48, "relative": None},
        {"position": 0.50, "retention": 0.30, "relative": None},  # 18% drop
        {"position": 0.90, "retention": 0.28, "relative": None},
    ]
    drops = find_drop_off_points(data_points, threshold=0.05)

    assert isinstance(drops, list)
    assert len(drops) >= 2
    for d in drops:
        assert {"position", "retention_before", "retention_after", "drop", "timestamp_hint"} <= d.keys()


def test_find_drop_off_points_empty_input():
    """Empty input returns empty list, not None or error."""
    from tools.youtube_analytics.retention import find_drop_off_points

    assert find_drop_off_points([]) == []
    assert find_drop_off_points([{"position": 0, "retention": 1}]) == []


# ---------------------------------------------------------------------------
# 2. retention_mapper.py — drops × parsed sections
# ---------------------------------------------------------------------------

def _parse_fixture_script_for_mapper():
    """Parse the script fixture using the same ScriptParser the mapper expects."""
    from tools.production.parser import ScriptParser
    return ScriptParser().parse_file(SCRIPT_FIXTURE)


def test_map_retention_to_sections_returns_mapped_drops():
    """map_retention_to_sections aligns drops to sections with documented shape."""
    from tools.youtube_analytics.retention import find_drop_off_points
    from tools.youtube_analytics.retention_mapper import map_retention_to_sections

    sections = _parse_fixture_script_for_mapper()
    assert sections, "ScriptParser returned no sections from fixture"

    # Synthetic curve covering the full video
    drops = find_drop_off_points([
        {"position": 0.00, "retention": 1.00, "relative": None},
        {"position": 0.30, "retention": 0.65, "relative": None},  # ~30% mark drop
        {"position": 0.70, "retention": 0.40, "relative": None},  # ~70% mark drop
    ], threshold=0.05)

    mapped = map_retention_to_sections(drops, sections)

    assert isinstance(mapped, list)
    expected_keys = {
        "section_heading", "section_type", "drop_position", "drop_magnitude",
        "retention_before", "retention_after", "word_range",
        "estimated_timestamp", "section_content_preview", "position_in_section",
    }
    for m in mapped:
        assert expected_keys <= m.keys(), f"missing keys: {expected_keys - m.keys()}"


def test_estimate_section_timestamps_returns_per_section_timing():
    """estimate_section_timestamps returns one timing dict per section."""
    from tools.youtube_analytics.retention_mapper import estimate_section_timestamps

    sections = _parse_fixture_script_for_mapper()
    timings = estimate_section_timestamps(sections, wpm=150)

    assert len(timings) == len(sections)
    for t in timings:
        assert {"heading", "start_time_str", "end_time_str", "duration_seconds", "word_count"} <= t.keys()


# ---------------------------------------------------------------------------
# 3. retention_decoder.py — classifier surface (analyze() needs real DB)
# ---------------------------------------------------------------------------

def test_decoder_classifiers_return_known_buckets():
    """The 3 classify_* methods return strings from a fixed vocabulary."""
    from tools.youtube_analytics.retention_decoder import RetentionDecoder

    rd = RetentionDecoder()

    title = "The Colonial Border Myth That Still Causes Wars"
    hook = rd.classify_hook_type(title)
    spec = rd.classify_specificity(title)
    bucket = rd.classify_duration_bucket(720)  # 12 min

    assert hook in {"myth-bust", "document-reveal", "how-why", "question", "curiosity-gap", "statement"}
    assert spec in {"specific", "general"}
    assert bucket in {"short (<7m)", "medium (7-11m)", "long (11-16m)", "very-long (16m+)"}


# ---------------------------------------------------------------------------
# 4. retention_scorer.py — section scoring
# ---------------------------------------------------------------------------

def test_score_section_returns_documented_keys():
    """score_section returns a dict with score / risk_level / warnings / metrics."""
    from tools.youtube_analytics.retention_scorer import score_section

    section_text = SCRIPT_FIXTURE.read_text(encoding="utf-8")
    result = score_section(
        section_text=section_text,
        section_type="body",
        topic_type="territorial",
    )

    assert {"score", "risk_level", "warnings", "metrics"} <= result.keys()
    assert isinstance(result["score"], float)
    assert result["risk_level"] in {"LOW", "MEDIUM", "HIGH"}
    assert isinstance(result["warnings"], list)
    assert isinstance(result["metrics"], dict)


# ---------------------------------------------------------------------------
# 5. retention_predictor.py — text -> prediction
# ---------------------------------------------------------------------------

def test_predict_from_text_returns_curve_and_flags():
    """predict_from_text on the script fixture returns the documented shape."""
    from tools.youtube_analytics.retention_predictor import predict_from_text

    text = SCRIPT_FIXTURE.read_text(encoding="utf-8")
    result = predict_from_text(text)

    assert isinstance(result, dict)
    # Pin actual current shape (docstring is stale — duration split into script/filmed):
    expected = {
        "curve", "sections", "flags", "recommendations", "total_words",
        "estimated_script_duration_min", "estimated_filmed_duration_min",
        "predicted_final_retention", "channel_avg_final_retention",
    }
    assert expected <= result.keys(), f"missing keys: {expected - result.keys()}"
    assert isinstance(result["curve"], list)
    assert isinstance(result["flags"], list)


# ---------------------------------------------------------------------------
# 6. retention_by_topic.py + retention_analysis.py — pure helpers
# ---------------------------------------------------------------------------

def test_classify_topic_returns_known_bucket():
    """classify_topic merges title hints with a db_topic_type fallback."""
    from tools.youtube_analytics.retention_by_topic import classify_topic

    bucket = classify_topic(
        title="The Colonial Border Myth That Still Causes Wars",
        db_topic_type="territorial",
    )
    assert isinstance(bucket, str)
    assert bucket  # non-empty


def test_classify_content_assigns_a_label():
    """classify_content (retention_analysis.py) labels arbitrary text."""
    from tools.youtube_analytics.retention_analysis import classify_content, _normalize

    label = classify_content("In 1859, Britain and Guatemala signed the treaty.")
    assert isinstance(label, str)

    norm = _normalize("Hello, World!")
    assert "," not in norm and "!" not in norm


# ---------------------------------------------------------------------------
# 7. Integration — pipeline composes (the "natural order" assertion)
# ---------------------------------------------------------------------------

def test_retention_pipeline_composes_end_to_end():
    """retention -> mapper -> scorer composes for the script fixture.

    Pins the natural-order pipeline: synthetic drops feed the mapper, which
    aligns to parsed sections; the scorer then runs over the same sections.
    Asserts the final scored output has the documented per-section shape.
    """
    from tools.youtube_analytics.retention import find_drop_off_points
    from tools.youtube_analytics.retention_mapper import map_retention_to_sections
    from tools.youtube_analytics.retention_scorer import score_section

    # 0. Fixture sanity
    assert POST_PUBLISH_FIXTURE.exists()
    assert SCRIPT_FIXTURE.exists()

    # 1. retention.py: synthetic curve -> drops
    drops = find_drop_off_points([
        {"position": 0.10, "retention": 0.92, "relative": None},
        {"position": 0.40, "retention": 0.55, "relative": None},
        {"position": 0.80, "retention": 0.30, "relative": None},
    ], threshold=0.05)
    assert drops, "Synthetic curve should produce drops"

    # 2. retention_mapper.py: drops × sections
    sections = _parse_fixture_script_for_mapper()
    mapped = map_retention_to_sections(drops, sections)
    assert isinstance(mapped, list)

    # 3. retention_scorer.py: score each parsed section
    scored = []
    for sec in sections:
        result = score_section(
            section_text=sec.content,
            section_type=sec.section_type,
            topic_type="territorial",
        )
        result["section_heading"] = sec.heading
        scored.append(result)

    assert len(scored) == len(sections)
    for r in scored:
        assert {"score", "risk_level", "warnings", "metrics", "section_heading"} <= r.keys()
