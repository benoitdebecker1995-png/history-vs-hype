"""
Unit tests for tools/benchmark_store.py

Tests cover:
- load() returns dict when niche_benchmark.json exists
- load() returns None when file is missing
- load() returns None when file contains invalid JSON
- load(path=custom) reads from custom path
- load() never raises any exception
- get_niche_score() behavior for known/unknown patterns and LOW confidence
- get_topic_thresholds() for known types and fallback to general
- normalize_topic_type() mapping logic
"""

import json
import os
import tempfile
import pytest


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _write_valid_benchmark(path: str) -> dict:
    """Write a minimal valid niche_benchmark.json to path and return the data."""
    data = {
        "by_pattern": {
            "declarative": {
                "median_vps": 0.565,
                "sample_count": 104,
                "confidence": "HIGH",
            },
            "how_why": {
                "median_vps": 0.226,
                "sample_count": 61,
                "confidence": "HIGH",
            },
            "question": {
                "median_vps": 0.268,
                "sample_count": 8,
                "confidence": "MEDIUM",
            },
            "colon": {
                "median_vps": 0.776,
                "sample_count": 65,
                "confidence": "HIGH",
            },
            "versus": {
                "median_vps": 2.812,
                "sample_count": 1,
                "confidence": "LOW",
            },
            "low_tiny": {
                "median_vps": 1.5,
                "sample_count": 1,
                "confidence": "LOW",
            },
        },
        "by_topic_type": {
            "territorial": {
                "median_vps": 0.373,
                "sample_count": 191,
                "confidence": "HIGH",
            },
            "ideological": {
                "median_vps": 1.362,
                "sample_count": 24,
                "confidence": "HIGH",
            },
            "political_fact_check": {
                "median_vps": 0.557,
                "sample_count": 24,
                "confidence": "HIGH",
            },
        },
    }
    with open(path, "w") as f:
        json.dump(data, f)
    return data


# ---------------------------------------------------------------------------
# load()
# ---------------------------------------------------------------------------

class TestLoad:
    def test_returns_dict_when_file_exists(self, tmp_path):
        """load() returns a dict when a valid niche_benchmark.json exists at path."""
        bench_path = str(tmp_path / "niche_benchmark.json")
        _write_valid_benchmark(bench_path)

        from tools.benchmark_store import load
        result = load(path=bench_path)
        assert isinstance(result, dict)

    def test_returns_none_when_file_missing(self, tmp_path):
        """load() returns None when file does not exist — never raises."""
        from tools.benchmark_store import load
        result = load(path=str(tmp_path / "nonexistent.json"))
        assert result is None

    def test_returns_none_for_invalid_json(self, tmp_path):
        """load() returns None when file contains invalid JSON — never raises."""
        bad_path = str(tmp_path / "bad.json")
        with open(bad_path, "w") as f:
            f.write("{not valid json!!!")

        from tools.benchmark_store import load
        result = load(path=bad_path)
        assert result is None

    def test_custom_path_parameter(self, tmp_path):
        """load(path=custom) reads from the specified custom path."""
        bench_path = str(tmp_path / "niche_benchmark.json")
        data = _write_valid_benchmark(bench_path)

        from tools.benchmark_store import load
        result = load(path=bench_path)
        assert result is not None
        assert "by_pattern" in result
        assert result["by_pattern"]["declarative"]["median_vps"] == data["by_pattern"]["declarative"]["median_vps"]

    def test_never_raises_on_permission_error(self, tmp_path):
        """load() swallows all exceptions and returns None."""
        from tools.benchmark_store import load
        # Pass a path that looks like a directory (would cause an error)
        result = load(path=str(tmp_path))  # directory, not a file
        assert result is None

    def test_returns_none_on_empty_file(self, tmp_path):
        """load() returns None when the file is empty."""
        empty_path = str(tmp_path / "empty.json")
        with open(empty_path, "w") as f:
            f.write("")

        from tools.benchmark_store import load
        result = load(path=empty_path)
        assert result is None

    def test_returns_dict_contains_by_pattern(self, tmp_path):
        """load() result contains 'by_pattern' key when file is valid."""
        bench_path = str(tmp_path / "niche_benchmark.json")
        _write_valid_benchmark(bench_path)

        from tools.benchmark_store import load
        result = load(path=bench_path)
        assert result is not None
        assert "by_pattern" in result


# ---------------------------------------------------------------------------
# get_niche_score()
# ---------------------------------------------------------------------------

class TestGetNicheScore:
    def test_returns_score_for_known_pattern(self, tmp_path):
        """get_niche_score returns VPS-converted score for known pattern with HIGH confidence."""
        bench_path = str(tmp_path / "niche_benchmark.json")
        _write_valid_benchmark(bench_path)

        from tools.benchmark_store import load, get_niche_score
        data = load(path=bench_path)
        score = get_niche_score("declarative", data)
        # declarative median_vps = 0.565, formula: min(100, max(0, int(0.565 * 115))) = int(64.975) = 64
        assert score == 64

    def test_returns_none_for_unknown_pattern(self, tmp_path):
        """get_niche_score returns None for pattern not in by_pattern."""
        bench_path = str(tmp_path / "niche_benchmark.json")
        _write_valid_benchmark(bench_path)

        from tools.benchmark_store import load, get_niche_score
        data = load(path=bench_path)
        score = get_niche_score("nonexistent_pattern", data)
        assert score is None

    def test_returns_none_when_data_is_none(self):
        """get_niche_score returns None when data=None (file missing scenario)."""
        from tools.benchmark_store import get_niche_score
        score = get_niche_score("declarative", None)
        assert score is None

    def test_returns_none_for_low_confidence_small_sample(self, tmp_path):
        """get_niche_score returns None when confidence==LOW and sample_count < 3."""
        bench_path = str(tmp_path / "niche_benchmark.json")
        _write_valid_benchmark(bench_path)

        from tools.benchmark_store import load, get_niche_score
        data = load(path=bench_path)
        # 'versus' has confidence=LOW and sample_count=1 — should return None
        score = get_niche_score("versus", data)
        assert score is None

    def test_returns_none_for_low_tiny_confidence(self, tmp_path):
        """get_niche_score returns None for any LOW confidence with sample_count < 3."""
        bench_path = str(tmp_path / "niche_benchmark.json")
        _write_valid_benchmark(bench_path)

        from tools.benchmark_store import load, get_niche_score
        data = load(path=bench_path)
        # 'low_tiny' has confidence=LOW and sample_count=1
        score = get_niche_score("low_tiny", data)
        assert score is None

    def test_how_why_score_is_correct(self, tmp_path):
        """get_niche_score correctly converts how_why VPS to score."""
        bench_path = str(tmp_path / "niche_benchmark.json")
        _write_valid_benchmark(bench_path)

        from tools.benchmark_store import load, get_niche_score
        data = load(path=bench_path)
        score = get_niche_score("how_why", data)
        # how_why median_vps = 0.226, score = int(0.226 * 115) = int(25.99) = 25
        assert score == 25

    def test_returns_score_for_medium_confidence(self, tmp_path):
        """get_niche_score returns score for MEDIUM confidence pattern (not filtered out)."""
        bench_path = str(tmp_path / "niche_benchmark.json")
        _write_valid_benchmark(bench_path)

        from tools.benchmark_store import load, get_niche_score
        data = load(path=bench_path)
        # question has MEDIUM confidence, sample_count=8 — should return a score
        score = get_niche_score("question", data)
        assert score is not None
        assert isinstance(score, int)

    def test_loads_data_when_not_passed(self, tmp_path, monkeypatch):
        """get_niche_score loads data internally when data=None but default path exists."""
        bench_path = str(tmp_path / "niche_benchmark.json")
        _write_valid_benchmark(bench_path)

        # Monkeypatch DEFAULT_PATH in benchmark_store to our temp file
        import tools.benchmark_store as bs
        original_path = bs.DEFAULT_PATH
        monkeypatch.setattr(bs, "DEFAULT_PATH", bench_path)
        try:
            score = bs.get_niche_score("declarative")
            # Should load and return score
            assert score is not None
        finally:
            bs.DEFAULT_PATH = original_path


# ---------------------------------------------------------------------------
# TOPIC_GRADE_THRESHOLDS + get_topic_thresholds()
# ---------------------------------------------------------------------------

class TestTopicGradeThresholds:
    def test_territorial_thresholds(self):
        """territorial topic has pass=50, good=65."""
        from tools.benchmark_store import TOPIC_GRADE_THRESHOLDS
        assert TOPIC_GRADE_THRESHOLDS["territorial"]["pass"] == 50
        assert TOPIC_GRADE_THRESHOLDS["territorial"]["good"] == 65

    def test_ideological_thresholds(self):
        """ideological topic has pass=60, good=70."""
        from tools.benchmark_store import TOPIC_GRADE_THRESHOLDS
        assert TOPIC_GRADE_THRESHOLDS["ideological"]["pass"] == 60
        assert TOPIC_GRADE_THRESHOLDS["ideological"]["good"] == 70

    def test_political_fact_check_thresholds(self):
        """political_fact_check topic has pass=75, good=85."""
        from tools.benchmark_store import TOPIC_GRADE_THRESHOLDS
        assert TOPIC_GRADE_THRESHOLDS["political_fact_check"]["pass"] == 75
        assert TOPIC_GRADE_THRESHOLDS["political_fact_check"]["good"] == 85

    def test_general_thresholds(self):
        """general topic has pass=60, good=70."""
        from tools.benchmark_store import TOPIC_GRADE_THRESHOLDS
        assert TOPIC_GRADE_THRESHOLDS["general"]["pass"] == 60
        assert TOPIC_GRADE_THRESHOLDS["general"]["good"] == 70

    def test_get_topic_thresholds_known_type(self):
        """get_topic_thresholds returns correct dict for known type."""
        from tools.benchmark_store import get_topic_thresholds
        result = get_topic_thresholds("territorial")
        assert result["pass"] == 50
        assert result["good"] == 65

    def test_get_topic_thresholds_unknown_type_falls_back_to_general(self):
        """get_topic_thresholds('unknown_type') returns general defaults."""
        from tools.benchmark_store import get_topic_thresholds
        result = get_topic_thresholds("unknown_type")
        assert result["pass"] == 60
        assert result["good"] == 70

    def test_get_topic_thresholds_political_fact_check(self):
        """get_topic_thresholds returns high thresholds for political_fact_check."""
        from tools.benchmark_store import get_topic_thresholds
        result = get_topic_thresholds("political_fact_check")
        assert result["pass"] == 75
        assert result["good"] == 85


# ---------------------------------------------------------------------------
# normalize_topic_type()
# ---------------------------------------------------------------------------

class TestNormalizeTopicType:
    def test_politician_maps_to_political_fact_check(self):
        from tools.benchmark_store import normalize_topic_type
        assert normalize_topic_type("politician") == "political_fact_check"

    def test_colonial_maps_to_territorial(self):
        from tools.benchmark_store import normalize_topic_type
        assert normalize_topic_type("colonial") == "territorial"

    def test_legal_maps_to_territorial(self):
        from tools.benchmark_store import normalize_topic_type
        assert normalize_topic_type("legal") == "territorial"

    def test_archaeological_maps_to_general(self):
        from tools.benchmark_store import normalize_topic_type
        assert normalize_topic_type("archaeological") == "general"

    def test_medieval_maps_to_general(self):
        from tools.benchmark_store import normalize_topic_type
        assert normalize_topic_type("medieval") == "general"

    def test_territorial_passthrough(self):
        from tools.benchmark_store import normalize_topic_type
        assert normalize_topic_type("territorial") == "territorial"

    def test_ideological_passthrough(self):
        from tools.benchmark_store import normalize_topic_type
        assert normalize_topic_type("ideological") == "ideological"

    def test_political_fact_check_passthrough(self):
        from tools.benchmark_store import normalize_topic_type
        assert normalize_topic_type("political_fact_check") == "political_fact_check"

    def test_general_passthrough(self):
        from tools.benchmark_store import normalize_topic_type
        assert normalize_topic_type("general") == "general"

    def test_unknown_type_maps_to_general(self):
        """Any unknown type falls back to 'general'."""
        from tools.benchmark_store import normalize_topic_type
        assert normalize_topic_type("xyz_unknown") == "general"
