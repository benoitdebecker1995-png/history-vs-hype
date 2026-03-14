"""
Unit tests for tools/title_ctr_store.py

Tests use an in-memory SQLite DB (written to tmp file) that mirrors
the ctr_snapshots + video_performance schema.
"""

import sqlite3
import tempfile
import os
import pytest


def _create_test_db(rows):
    """
    Create a temp SQLite DB with ctr_snapshots + video_performance tables.

    rows: list of dicts with keys:
        video_id, title, ctr_percent, snapshot_date
        (impression_count, view_count default to 1000, 30)
    Returns: path to temp DB file (caller must delete after use).
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

    for row in rows:
        # Insert into video_performance (upsert-style)
        conn.execute(
            "INSERT OR IGNORE INTO video_performance (video_id, title) VALUES (?, ?)",
            (row["video_id"], row.get("title", f"Title for {row['video_id']}"))
        )
        conn.execute(
            """
            INSERT INTO ctr_snapshots
                (video_id, snapshot_date, ctr_percent, impression_count, view_count, recorded_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                row["video_id"],
                row.get("snapshot_date", "2026-02-23"),
                row["ctr_percent"],
                row.get("impression_count", 1000),
                row.get("view_count", 30),
                row.get("snapshot_date", "2026-02-23"),
            )
        )

    conn.commit()
    conn.close()
    return path


class TestGetPatternCtrFromDb:
    """Tests for get_pattern_ctr_from_db()"""

    def test_empty_db_returns_empty_dict(self):
        """Empty DB (no CTR rows) returns empty dict."""
        from tools.title_ctr_store import get_pattern_ctr_from_db

        path = _create_test_db([])
        try:
            result = get_pattern_ctr_from_db(path)
            assert result == {}
        finally:
            os.unlink(path)

    def test_three_declarative_titles_return_average(self):
        """3 declarative titles with known CTR return correct pattern score."""
        from tools.title_ctr_store import get_pattern_ctr_from_db

        # 3.8% CTR * 17 = 64.6 -> int -> 64
        rows = [
            {"video_id": "v1", "title": "France Conquered Haiti", "ctr_percent": 3.8},
            {"video_id": "v2", "title": "Spain Divided the World", "ctr_percent": 3.8},
            {"video_id": "v3", "title": "Britain Erased the Map", "ctr_percent": 3.8},
        ]
        path = _create_test_db(rows)
        try:
            result = get_pattern_ctr_from_db(path)
            assert "declarative" in result
            # 3.8 * 17 = 64.6 -> int(64.6) = 64
            assert result["declarative"] == 64
        finally:
            os.unlink(path)

    def test_pattern_with_only_two_videos_excluded(self):
        """Pattern with fewer than min_sample=3 videos is excluded."""
        from tools.title_ctr_store import get_pattern_ctr_from_db

        rows = [
            {"video_id": "v1", "title": "France Conquered Haiti", "ctr_percent": 4.0},
            {"video_id": "v2", "title": "Spain Divided the World", "ctr_percent": 4.0},
            # Only 2 declarative videos — below min_sample=3
        ]
        path = _create_test_db(rows)
        try:
            result = get_pattern_ctr_from_db(path)
            assert "declarative" not in result
        finally:
            os.unlink(path)

    def test_zero_ctr_rows_excluded(self):
        """Rows with ctr_percent=0 are excluded (API velocity snapshots)."""
        from tools.title_ctr_store import get_pattern_ctr_from_db

        rows = [
            {"video_id": "v1", "title": "France Conquered Haiti", "ctr_percent": 0.0},
            {"video_id": "v2", "title": "Spain Divided the World", "ctr_percent": 0.0},
            {"video_id": "v3", "title": "Britain Erased the Map", "ctr_percent": 0.0},
        ]
        path = _create_test_db(rows)
        try:
            result = get_pattern_ctr_from_db(path)
            # All zero CTR rows excluded -> no patterns qualify
            assert result == {}
        finally:
            os.unlink(path)

    def test_multiple_patterns_independent(self):
        """Multiple patterns each return independently correct averages."""
        from tools.title_ctr_store import get_pattern_ctr_from_db

        rows = [
            # 3 declarative titles at 3.8% CTR -> 64
            {"video_id": "d1", "title": "France Conquered Haiti", "ctr_percent": 3.8},
            {"video_id": "d2", "title": "Spain Divided the World", "ctr_percent": 3.8},
            {"video_id": "d3", "title": "Britain Erased the Map", "ctr_percent": 3.8},
            # 3 versus titles at 4.7% CTR -> int(4.7 * 17) = int(79.9) = 79
            {"video_id": "vs1", "title": "Spain vs Portugal - Division", "ctr_percent": 4.7},
            {"video_id": "vs2", "title": "France vs Haiti - Debt Trap", "ctr_percent": 4.7},
            {"video_id": "vs3", "title": "Rome vs Carthage - Final War", "ctr_percent": 4.7},
        ]
        path = _create_test_db(rows)
        try:
            result = get_pattern_ctr_from_db(path)
            assert "declarative" in result
            assert result["declarative"] == 64   # int(3.8 * 17) = 64
            assert "versus" in result
            assert result["versus"] == 79        # int(4.7 * 17) = 79
        finally:
            os.unlink(path)

    def test_calibration_38_pct_maps_to_64(self):
        """
        CTR calibration: 3.8% CTR maps to score 64.
        Channel baseline: 3.8% = declarative = 65 in static scores.
        DB formula: int(3.8 * 17) = 64 (within 1 point is acceptable).
        """
        from tools.title_ctr_store import get_pattern_ctr_from_db

        rows = [
            {"video_id": "v1", "title": "France Conquered Haiti", "ctr_percent": 3.8},
            {"video_id": "v2", "title": "Spain Divided the World", "ctr_percent": 3.8},
            {"video_id": "v3", "title": "Britain Erased the Map", "ctr_percent": 3.8},
        ]
        path = _create_test_db(rows)
        try:
            result = get_pattern_ctr_from_db(path)
            score = result.get("declarative", -1)
            # 3.8 * 17 = 64.6 -> int -> 64, close to static 65
            assert 60 <= score <= 70, f"Expected score near 65, got {score}"
        finally:
            os.unlink(path)

    def test_invalid_db_path_returns_empty_dict(self):
        """Non-existent DB path returns empty dict, no exception."""
        from tools.title_ctr_store import get_pattern_ctr_from_db

        result = get_pattern_ctr_from_db("/nonexistent/path/to.db")
        assert result == {}

    def test_only_latest_snapshot_per_video_used(self):
        """When a video has multiple snapshots, only the latest non-zero one is used."""
        from tools.title_ctr_store import get_pattern_ctr_from_db

        # v1 has an old 2.0% snapshot and a newer 4.0% snapshot
        # If both counted, avg would be 3.0; if only latest, avg = 4.0
        rows = [
            {
                "video_id": "v1", "title": "France Conquered Haiti",
                "ctr_percent": 2.0, "snapshot_date": "2026-01-01"
            },
            {
                "video_id": "v1", "title": "France Conquered Haiti",
                "ctr_percent": 4.0, "snapshot_date": "2026-02-23"
            },
            {"video_id": "v2", "title": "Spain Divided the World", "ctr_percent": 4.0},
            {"video_id": "v3", "title": "Britain Erased the Map", "ctr_percent": 4.0},
        ]
        path = _create_test_db(rows)
        try:
            result = get_pattern_ctr_from_db(path)
            # All 3 videos have latest snapshot at 4.0% -> score = int(4.0 * 17) = 68
            assert "declarative" in result
            assert result["declarative"] == 68   # int(4.0 * 17) = 68
        finally:
            os.unlink(path)

    def test_custom_min_sample(self):
        """min_sample=2 allows patterns with only 2 videos."""
        from tools.title_ctr_store import get_pattern_ctr_from_db

        rows = [
            {"video_id": "v1", "title": "France Conquered Haiti", "ctr_percent": 4.0},
            {"video_id": "v2", "title": "Spain Divided the World", "ctr_percent": 4.0},
        ]
        path = _create_test_db(rows)
        try:
            result = get_pattern_ctr_from_db(path, min_sample=2)
            assert "declarative" in result
        finally:
            os.unlink(path)

    def test_score_capped_at_100(self):
        """Extremely high CTR (>5.9%) does not produce score >100."""
        from tools.title_ctr_store import get_pattern_ctr_from_db

        rows = [
            {"video_id": "v1", "title": "France vs Haiti - Forced Payments", "ctr_percent": 10.0},
            {"video_id": "v2", "title": "Spain vs Portugal - New World", "ctr_percent": 10.0},
            {"video_id": "v3", "title": "Rome vs Carthage - Final War", "ctr_percent": 10.0},
        ]
        path = _create_test_db(rows)
        try:
            result = get_pattern_ctr_from_db(path)
            assert "versus" in result
            assert result["versus"] <= 100
        finally:
            os.unlink(path)
