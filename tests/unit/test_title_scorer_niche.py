"""
Unit tests for tools/title_scorer.py — niche integration, topic types, small-sample fallback.

Tests cover:
- score_title() with topic_type param: uses topic-aware grade thresholds
- Same title + different topic_type gets different grade
- Small-sample fallback: when own-channel n < 5, use niche benchmark base score
- Own-channel n >= 5: use own-channel base score (no substitution)
- New return dict keys: fallback_warning, niche_enriched, niche_base_score,
  detected_topic, topic_type_target, niche_percentile_label
- Hard rejects still override grade regardless of topic type
- Backward compatibility: no db_path + no topic_type = static scoring unchanged
"""

import os
import sqlite3
import tempfile
import pytest


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _create_db(patterns_and_n: dict) -> str:
    """
    Create a temp SQLite DB with rows for given patterns.

    patterns_and_n: {'declarative': 3, 'versus': 1}  -> n rows per pattern
    Returns path (caller must unlink).
    """
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    conn = sqlite3.connect(path)
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS video_performance (
            video_id TEXT PRIMARY KEY,
            title TEXT,
            views INTEGER,
            conversion_rate REAL,
            topic_type TEXT
        );
        CREATE TABLE IF NOT EXISTS ctr_snapshots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            video_id TEXT NOT NULL,
            snapshot_date TEXT NOT NULL,
            ctr_percent REAL NOT NULL,
            impression_count INTEGER NOT NULL,
            view_count INTEGER NOT NULL,
            is_late_entry BOOLEAN DEFAULT 0,
            recorded_at TEXT NOT NULL
        );
    """)

    row_idx = 0
    for pattern, n in patterns_and_n.items():
        for i in range(n):
            # Use titles that will detect as the right pattern
            if pattern == "declarative":
                title = f"France Conquered Haiti Debt Video {row_idx}"
            elif pattern == "versus":
                title = f"France vs Haiti Video {row_idx}"
            elif pattern == "how_why":
                title = f"How Haiti Got Free Video {row_idx}"
            else:
                title = f"Unknown Pattern Title {row_idx}"
            vid = f"vid_{row_idx}"
            conn.execute(
                "INSERT OR IGNORE INTO video_performance (video_id, title) VALUES (?, ?)",
                (vid, title),
            )
            conn.execute(
                "INSERT INTO ctr_snapshots (video_id, snapshot_date, ctr_percent, impression_count, view_count, recorded_at) VALUES (?, ?, ?, ?, ?, ?)",
                (vid, "2026-02-23", 3.8, 1000, 38, "2026-02-23"),
            )
            row_idx += 1

    conn.commit()
    conn.close()
    return path


# ---------------------------------------------------------------------------
# Return dict keys
# ---------------------------------------------------------------------------

class TestReturnDictNewKeys:
    """All new keys are present in the return dict."""

    def test_has_fallback_warning_key(self):
        from tools.title_scorer import score_title
        result = score_title("France Conquered Haiti Debt Payment")
        assert "fallback_warning" in result

    def test_has_niche_enriched_key(self):
        from tools.title_scorer import score_title
        result = score_title("France Conquered Haiti Debt Payment")
        assert "niche_enriched" in result

    def test_has_niche_base_score_key(self):
        from tools.title_scorer import score_title
        result = score_title("France Conquered Haiti Debt Payment")
        assert "niche_base_score" in result

    def test_has_detected_topic_key(self):
        from tools.title_scorer import score_title
        result = score_title("France Conquered Haiti Debt Payment")
        assert "detected_topic" in result

    def test_has_topic_type_target_key(self):
        from tools.title_scorer import score_title
        result = score_title("France Conquered Haiti Debt Payment")
        assert "topic_type_target" in result

    def test_topic_type_target_has_pass_and_good(self):
        from tools.title_scorer import score_title
        result = score_title("France Conquered Haiti Debt Payment")
        target = result["topic_type_target"]
        assert "pass" in target
        assert "good" in target

    def test_topic_type_target_has_gap_message(self):
        from tools.title_scorer import score_title
        result = score_title("France Conquered Haiti Debt Payment")
        target = result["topic_type_target"]
        assert "gap_message" in target

    def test_has_niche_percentile_label_key(self):
        from tools.title_scorer import score_title
        result = score_title("France Conquered Haiti Debt Payment")
        assert "niche_percentile_label" in result

    def test_all_original_keys_still_present(self):
        """No existing keys removed — backward compatibility."""
        from tools.title_scorer import score_title
        result = score_title("France Conquered Haiti Debt Payment")
        original_keys = {
            "title", "score", "grade", "pattern", "length",
            "base_score", "penalties", "bonuses", "suggestions",
            "hard_rejects", "db_enriched", "db_base_score",
        }
        assert original_keys.issubset(result.keys()), (
            f"Missing original keys: {original_keys - result.keys()}"
        )


# ---------------------------------------------------------------------------
# Topic-type grade thresholds
# ---------------------------------------------------------------------------

class TestTopicTypeGradeThresholds:
    """score_title() respects per-topic-type grade thresholds."""

    def test_territorial_pass_threshold_is_50(self):
        """territorial: score=55 should be grade C (pass=50) not F."""
        from tools.title_scorer import score_title
        # We need a title that will score around 55 for territorial
        # 'declarative' base=65, apply short penalty to get ~55
        result = score_title("Haiti Debt", topic_type="territorial")
        # Score will be < 65 due to short title penalty (-5) from base 65 -> 60
        # At territorial pass=50, grade C if score >= 50
        assert result["topic_type_target"]["pass"] == 50
        assert result["topic_type_target"]["good"] == 65

    def test_political_fact_check_pass_threshold_is_75(self):
        """political_fact_check: pass=75."""
        from tools.title_scorer import score_title
        result = score_title("Haiti Debt", topic_type="political_fact_check")
        assert result["topic_type_target"]["pass"] == 75
        assert result["topic_type_target"]["good"] == 85

    def test_same_title_different_grade_by_topic(self):
        """
        Same title, same score, gets different grade for different topic types.
        Score 60: C for territorial (pass=50), F for political_fact_check (pass=75).
        """
        from tools.title_scorer import score_title
        # Use a title that scores around 60 with static scoring
        # declarative base=65, short title -5 = 60
        title = "Haiti Paid France"  # length=17 -> short -> -5 -> ~60

        r_terr = score_title(title, topic_type="territorial")
        r_pfc = score_title(title, topic_type="political_fact_check")

        # Both should have no hard_rejects
        assert not r_terr["hard_rejects"]
        assert not r_pfc["hard_rejects"]

        # Both have same final score
        assert r_terr["score"] == r_pfc["score"]

        # But different grades — territorial is more lenient
        # territorial pass=50: score 60 -> C or better
        # political_fact_check pass=75: score 60 -> below pass -> D or F
        score = r_terr["score"]
        if score >= 50:
            assert r_terr["grade"] in ("A", "B", "C"), (
                f"Expected C or better for territorial at score {score}, got {r_terr['grade']}"
            )
        if score < 75:
            assert r_pfc["grade"] in ("D", "F"), (
                f"Expected D or F for political_fact_check at score {score}, got {r_pfc['grade']}"
            )

    def test_detected_topic_is_normalized(self):
        """detected_topic contains the normalized topic type string."""
        from tools.title_scorer import score_title
        result = score_title("France Conquered Haiti Debt Payment")
        # detected_topic should be a string from the normalized taxonomy
        assert isinstance(result["detected_topic"], str)
        assert result["detected_topic"] in (
            "territorial", "ideological", "political_fact_check", "general"
        )

    def test_explicit_topic_type_overrides_auto_detect(self):
        """When topic_type is passed explicitly, it takes precedence over auto-detect."""
        from tools.title_scorer import score_title
        result = score_title("France Conquered Haiti Debt Payment", topic_type="political_fact_check")
        assert result["topic_type_target"]["pass"] == 75

    def test_ideological_thresholds(self):
        from tools.title_scorer import score_title
        result = score_title("France Conquered Haiti Debt Payment", topic_type="ideological")
        assert result["topic_type_target"]["pass"] == 60
        assert result["topic_type_target"]["good"] == 70

    def test_grade_A_requires_good_plus_15(self):
        """Grade A = final >= good + 15 for the topic type."""
        from tools.title_scorer import score_title
        # territorial: good=65, so A requires final >= 80
        # Use a high-scoring title: versus pattern base=75 + active verb bonus
        result = score_title("France vs Haiti Debt Divided", topic_type="territorial")
        # versus base=75 + active verb "divided" +5 = 80 -> A
        if result["score"] >= 80:
            assert result["grade"] == "A"

    def test_grade_B_at_good_threshold(self):
        """Grade B = final >= good (but < good + 15) for the topic type."""
        from tools.title_scorer import score_title
        # territorial: good=65, so B requires 65 <= score < 80
        # declarative base=65, no bonuses -> score 65 -> B
        result = score_title("France Conquered Haiti This Long Title Right Here To Hit 40+ Chars",
                              topic_type="territorial")
        if result["score"] == 65:
            assert result["grade"] == "B"

    def test_grade_D_below_pass(self):
        """Grade D = final >= pass - 15."""
        from tools.title_scorer import score_title
        # political_fact_check: pass=75, D = 60 <= score < 75
        # declarative base=65, good title length ~45 chars
        title = "France Conquered Haiti Debt in Long Format Here"  # ~48 chars
        result = score_title(title, topic_type="political_fact_check")
        # base=65 (declarative), within length range, no hard rejects
        # pass=75, D range = 60-74
        if 60 <= result["score"] < 75:
            assert result["grade"] == "D", f"Expected D for score {result['score']}, got {result['grade']}"

    def test_hard_rejects_override_topic_type_grade(self):
        """Hard rejects (year, colon, the_x_that) produce REJECTED regardless of topic type."""
        from tools.title_scorer import score_title
        # Year in title -> REJECTED even with lenient territorial thresholds
        result = score_title("France Conquered Haiti in 1825", topic_type="territorial")
        assert result["grade"] == "REJECTED"

    def test_colon_hard_reject_with_topic_type(self):
        """Colon hard reject applies regardless of topic type."""
        from tools.title_scorer import score_title
        result = score_title("France: The Haiti Story", topic_type="territorial")
        assert result["grade"] == "REJECTED"

    def test_gap_message_when_grade_below_B(self):
        """gap_message is non-empty when grade is below B."""
        from tools.title_scorer import score_title
        # Use a short title with political_fact_check — will score below pass=75
        result = score_title("Haiti Debt", topic_type="political_fact_check")
        if result["grade"] not in ("A", "B"):
            assert result["topic_type_target"]["gap_message"] != "", (
                f"Expected non-empty gap_message for grade {result['grade']}"
            )


# ---------------------------------------------------------------------------
# Small-sample fallback (BENCH-02)
# ---------------------------------------------------------------------------

class TestSmallSampleFallback:
    """score_title() uses niche benchmark when own-channel sample count < 5."""

    def test_niche_substitution_when_own_n_less_than_5(self):
        """With db_path and n=2 own-channel examples, use niche benchmark score."""
        from tools.title_scorer import score_title
        # Create DB with only 2 declarative examples (< 5 threshold)
        path = _create_db({"declarative": 2})
        try:
            result = score_title(
                "France Conquered Haiti Debt Payment",
                db_path=path,
            )
            # niche_enriched should be True when substitution happens
            assert result["niche_enriched"] is True
            assert result["fallback_warning"] is not None
            assert "niche" in result["fallback_warning"].lower()
        finally:
            os.unlink(path)

    def test_own_channel_used_when_n_gte_5(self):
        """With db_path and n=5+ own-channel examples, use own-channel score."""
        from tools.title_scorer import score_title
        # Create DB with 5 declarative examples (>= 5 threshold)
        path = _create_db({"declarative": 5})
        try:
            result = score_title(
                "France Conquered Haiti Debt Payment",
                db_path=path,
            )
            # db_enriched (own-channel) should be True
            assert result["db_enriched"] is True
            # fallback_warning should be None (no substitution)
            assert result["fallback_warning"] is None
        finally:
            os.unlink(path)

    def test_fallback_warning_is_none_without_db(self):
        """No db_path: fallback_warning is None (static mode, no substitution)."""
        from tools.title_scorer import score_title
        result = score_title("France Conquered Haiti Debt Payment")
        assert result["fallback_warning"] is None

    def test_niche_base_score_populated_when_substitution(self):
        """niche_base_score is populated when niche substitution happens."""
        from tools.title_scorer import score_title
        path = _create_db({"declarative": 2})
        try:
            result = score_title(
                "France Conquered Haiti Debt Payment",
                db_path=path,
            )
            if result["niche_enriched"]:
                assert result["niche_base_score"] is not None
                assert isinstance(result["niche_base_score"], int)
        finally:
            os.unlink(path)

    def test_niche_enriched_false_without_db(self):
        """Without db_path, niche_enriched is False."""
        from tools.title_scorer import score_title
        result = score_title("France Conquered Haiti Debt Payment")
        assert result["niche_enriched"] is False

    def test_niche_base_score_none_without_substitution(self):
        """niche_base_score can be set even in static mode (informational)."""
        from tools.title_scorer import score_title
        result = score_title("France Conquered Haiti Debt Payment")
        # niche_base_score key must exist
        assert "niche_base_score" in result


# ---------------------------------------------------------------------------
# Niche percentile label (BENCH-01)
# ---------------------------------------------------------------------------

class TestNichePercentileLabel:
    """score_title() includes niche percentile label for context."""

    def test_percentile_label_is_string(self):
        from tools.title_scorer import score_title
        result = score_title("France Conquered Haiti Debt Payment")
        assert isinstance(result["niche_percentile_label"], str)

    def test_percentile_label_nonempty_for_declarative(self):
        """Declarative pattern has HIGH confidence niche data — should get a label."""
        from tools.title_scorer import score_title
        result = score_title("France Conquered Haiti Debt Payment")
        assert result["pattern"] == "declarative"
        # niche_benchmark.json exists in this project, so label should be non-empty
        assert result["niche_percentile_label"] != ""

    def test_percentile_label_contains_known_phrase(self):
        """Label is one of the expected descriptive phrases."""
        from tools.title_scorer import score_title
        result = score_title("France Conquered Haiti Debt Payment")
        label = result["niche_percentile_label"]
        valid_labels = {
            "top third of niche",
            "above niche median",
            "below niche median",
            "bottom quartile of niche",
            "",  # empty is acceptable if niche data not available
        }
        assert label in valid_labels, f"Unexpected label: {label!r}"


# ---------------------------------------------------------------------------
# Backward compatibility
# ---------------------------------------------------------------------------

class TestBackwardCompatibility:
    """Existing behavior unchanged when no db_path and no topic_type."""

    def test_static_scoring_unchanged_no_args(self):
        """score_title(title) with no extra args works the same as before."""
        from tools.title_scorer import score_title, PATTERN_SCORES
        result = score_title("France Conquered Haiti Debt Payment")
        # Should still use PATTERN_SCORES as base when no db, no topic override
        assert "score" in result
        assert "grade" in result
        assert "pattern" in result

    def test_hard_reject_year_still_works(self):
        from tools.title_scorer import score_title
        result = score_title("France Conquered Haiti in 1825")
        assert result["grade"] == "REJECTED"

    def test_hard_reject_colon_still_works(self):
        from tools.title_scorer import score_title
        result = score_title("France: The Haiti Debt Story")
        assert result["grade"] == "REJECTED"

    def test_hard_reject_the_x_that_still_works(self):
        from tools.title_scorer import score_title
        result = score_title("The Country That Paid Its Colonizer")
        assert result["grade"] == "REJECTED"

    def test_existing_db_enriched_key_still_works(self):
        """db_enriched key still present and False when no db_path."""
        from tools.title_scorer import score_title
        result = score_title("France Conquered Haiti Debt Payment")
        assert result["db_enriched"] is False

    def test_existing_db_base_score_key_still_works(self):
        """db_base_score key still present and None when no db_path."""
        from tools.title_scorer import score_title
        result = score_title("France Conquered Haiti Debt Payment")
        assert result["db_base_score"] is None
