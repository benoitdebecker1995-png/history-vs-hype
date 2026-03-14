"""
Unit tests for tools/title_scorer.py — db_path parameter.

Tests verify that score_title() with an optional db_path:
- Uses DB-derived base scores when the pattern has sufficient data
- Falls back to static PATTERN_SCORES when pattern not in DB
- Falls back silently when db_path is invalid (no crash)
- Preserves backward compatibility when db_path=None
- Still applies hard reject penalties regardless of DB scores
"""

import sqlite3
import tempfile
import os
import pytest


def _create_test_db_with_data(declarative_ctr=3.8, n_declarative=3):
    """
    Create a temp SQLite DB with n_declarative declarative titles at a given CTR.

    Returns: path to temp file (caller must delete).
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

    for i in range(n_declarative):
        vid = f"decl_{i}"
        conn.execute(
            "INSERT OR IGNORE INTO video_performance (video_id, title) VALUES (?, ?)",
            (vid, f"France Conquered Haiti Video {i}")
        )
        conn.execute(
            "INSERT INTO ctr_snapshots (video_id, snapshot_date, ctr_percent, impression_count, view_count, recorded_at) VALUES (?, ?, ?, ?, ?, ?)",
            (vid, "2026-02-23", declarative_ctr, 1000, 30, "2026-02-23")
        )

    conn.commit()
    conn.close()
    return path


class TestScoreTitleDbPath:
    """Tests for score_title() with optional db_path parameter."""

    def test_backward_compatible_without_db_path(self):
        """
        score_title() without db_path returns same result as current implementation.
        Verifies no regression in existing callers.
        """
        from tools.title_scorer import score_title, PATTERN_SCORES

        result = score_title("France Conquered Haiti Debt Payment")
        assert "title" in result
        assert "score" in result
        assert "grade" in result
        assert "pattern" in result
        assert "base_score" in result
        assert result["base_score"] == PATTERN_SCORES[result["pattern"]]

    def test_db_path_none_uses_static_scores(self):
        """Explicit db_path=None uses static PATTERN_SCORES (same as no db_path)."""
        from tools.title_scorer import score_title, PATTERN_SCORES

        result = score_title("France Conquered Haiti Debt Payment", db_path=None)
        assert result["base_score"] == PATTERN_SCORES[result["pattern"]]
        assert result["db_enriched"] is False

    def test_db_enriched_false_without_db_path(self):
        """Return dict includes db_enriched=False when no db_path provided."""
        from tools.title_scorer import score_title

        result = score_title("France Conquered Haiti Debt Payment")
        assert "db_enriched" in result
        assert result["db_enriched"] is False

    def test_db_enriched_false_none_db_path(self):
        """Return dict includes db_enriched=False when db_path=None."""
        from tools.title_scorer import score_title

        result = score_title("France Conquered Haiti Debt Payment", db_path=None)
        assert result["db_enriched"] is False

    def test_db_base_score_none_without_db_path(self):
        """Return dict includes db_base_score=None when no db_path provided."""
        from tools.title_scorer import score_title

        result = score_title("France Conquered Haiti Debt Payment")
        assert "db_base_score" in result
        assert result["db_base_score"] is None

    def test_uses_db_derived_score_when_pattern_in_db(self):
        """
        score_title() with db_path uses DB-derived base score when pattern has data.
        """
        from tools.title_scorer import score_title

        # Create DB with declarative titles at 5.0% CTR -> score = int(5.0 * 17) = 85
        path = _create_test_db_with_data(declarative_ctr=5.0, n_declarative=3)
        try:
            result = score_title("France Conquered Haiti Debt Payment", db_path=path)
            assert result["db_enriched"] is True
            assert result["pattern"] == "declarative"
            # DB base score = int(5.0 * 17) = 85
            assert result["db_base_score"] == 85
            assert result["base_score"] == 85
        finally:
            os.unlink(path)

    def test_falls_back_to_static_when_pattern_not_in_db(self):
        """
        score_title() with db_path but pattern not in DB falls back to static.
        DB only has declarative data; versus title should use static score.
        """
        from tools.title_scorer import score_title, PATTERN_SCORES

        # DB has only declarative data — no versus data
        path = _create_test_db_with_data(declarative_ctr=5.0, n_declarative=3)
        try:
            result = score_title("France vs Haiti - Forced Debt", db_path=path)
            assert result["pattern"] == "versus"
            # Pattern not in DB -> fall back to static
            assert result["base_score"] == PATTERN_SCORES["versus"]
            # db_enriched should be False since this specific pattern used static
            assert result["db_enriched"] is False
        finally:
            os.unlink(path)

    def test_invalid_db_path_falls_back_silently(self):
        """
        score_title() with invalid/non-existent db_path uses static scores (no crash).
        """
        from tools.title_scorer import score_title, PATTERN_SCORES

        result = score_title(
            "France Conquered Haiti Debt Payment",
            db_path="/nonexistent/path/db.db"
        )
        assert result["pattern"] == "declarative"
        assert result["base_score"] == PATTERN_SCORES["declarative"]
        assert result["db_enriched"] is False

    def test_hard_rejects_still_apply_with_db_path(self):
        """
        Hard reject penalties (year, colon, the_x_that) still apply regardless of DB scores.
        DB with high CTR does not override REJECTED grade for year-containing titles.
        """
        from tools.title_scorer import score_title

        path = _create_test_db_with_data(declarative_ctr=5.0, n_declarative=3)
        try:
            # Title has a year — should be REJECTED even with excellent DB scores
            result = score_title("France Conquered Haiti in 1825", db_path=path)
            assert result["grade"] == "REJECTED"
            assert len(result["hard_rejects"]) > 0
        finally:
            os.unlink(path)

    def test_colon_hard_reject_with_db_path(self):
        """Colon penalty still produces REJECTED grade even when DB scores are high."""
        from tools.title_scorer import score_title

        path = _create_test_db_with_data(declarative_ctr=5.0, n_declarative=3)
        try:
            result = score_title("France vs Haiti: The Forced Debt", db_path=path)
            assert result["grade"] == "REJECTED"
        finally:
            os.unlink(path)

    def test_return_dict_has_required_keys(self):
        """Return dict includes all original keys plus db_enriched and db_base_score."""
        from tools.title_scorer import score_title

        result = score_title("France Conquered Haiti Debt Payment")
        required_keys = {
            "title", "score", "grade", "pattern", "length",
            "base_score", "penalties", "bonuses", "suggestions",
            "hard_rejects", "db_enriched", "db_base_score"
        }
        assert required_keys.issubset(result.keys())

    def test_db_base_score_populated_when_db_used(self):
        """db_base_score is the DB-derived score (not None) when DB data available."""
        from tools.title_scorer import score_title

        path = _create_test_db_with_data(declarative_ctr=4.0, n_declarative=3)
        try:
            result = score_title("France Conquered Haiti Debt Payment", db_path=path)
            assert result["db_enriched"] is True
            assert result["db_base_score"] is not None
            # int(4.0 * 17) = 68
            assert result["db_base_score"] == 68
        finally:
            os.unlink(path)
