"""
Unit tests for ctr_tracker.py CTR fetch and summary functionality.

Tests cover:
  1. CTR stored correctly when API returns ctr_available=True
  2. Fallback to ctr_percent=0 when API returns ctr_available=False
  3. Partial failure: one video errors, another succeeds — both get rows
  4. Summary output includes "CTR updated for X/Y videos" and pattern scores
  5. Duplicate guard: today's snapshot already exists → take_snapshot returns early
"""

import sqlite3
import pytest
from unittest.mock import patch, MagicMock, call

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS ctr_snapshots (
    video_id TEXT,
    snapshot_date TEXT,
    ctr_percent REAL,
    impression_count INTEGER,
    view_count INTEGER,
    is_late_entry INTEGER,
    recorded_at TEXT
)
"""


def make_in_memory_conn():
    """Return an in-memory SQLite connection with ctr_snapshots created."""
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.execute(CREATE_TABLE_SQL)
    conn.commit()
    return conn


class NonClosingConnection:
    """Wraps a real sqlite3 connection but ignores close() so tests can query after take_snapshot."""

    def __init__(self, conn):
        self._conn = conn

    def execute(self, *args, **kwargs):
        return self._conn.execute(*args, **kwargs)

    def commit(self):
        return self._conn.commit()

    def close(self):
        pass  # intentionally no-op

    @property
    def row_factory(self):
        return self._conn.row_factory

    @row_factory.setter
    def row_factory(self, value):
        self._conn.row_factory = value

    def fetchall(self):
        return self._conn.fetchall()


FAKE_VIDEO_IDS = ["vid001", "vid002", "vid003"]
FAKE_VIEW_COUNTS = {"vid001": 1000, "vid002": 2000, "vid003": 3000}

FAKE_METADATA = [
    {"id": "vid001", "title": "Video One", "duration": 600},
    {"id": "vid002", "title": "Video Two", "duration": 800},
    {"id": "vid003", "title": "Video Three", "duration": 900},
]


# ---------------------------------------------------------------------------
# Test 1: CTR stored in snapshot when available
# ---------------------------------------------------------------------------

def test_ctr_stored_in_snapshot():
    """When store_snapshot is called with real CTR values, it writes them to the DB."""
    from tools.youtube_analytics.ctr_tracker import store_snapshot

    conn = make_in_memory_conn()
    store_snapshot(conn, "vid001", 1000, "2026-03-15", ctr_percent=4.2, impression_count=5000)
    conn.commit()

    row = conn.execute(
        "SELECT * FROM ctr_snapshots WHERE video_id = 'vid001'"
    ).fetchone()

    assert row is not None
    assert row["video_id"] == "vid001"
    assert row["view_count"] == 1000
    assert row["ctr_percent"] == pytest.approx(4.2)
    assert row["impression_count"] == 5000
    assert row["is_late_entry"] == 0
    conn.close()


# ---------------------------------------------------------------------------
# Test 2: CTR unavailable fallback
# ---------------------------------------------------------------------------

def test_ctr_unavailable_fallback():
    """When store_snapshot is called without CTR params, it writes zeros but keeps view_count."""
    from tools.youtube_analytics.ctr_tracker import store_snapshot

    conn = make_in_memory_conn()
    # Call with defaults (simulating ctr_available=False case)
    store_snapshot(conn, "vid002", 2000, "2026-03-15")
    conn.commit()

    row = conn.execute(
        "SELECT * FROM ctr_snapshots WHERE video_id = 'vid002'"
    ).fetchone()

    assert row is not None
    assert row["view_count"] == 2000
    assert row["ctr_percent"] == pytest.approx(0.0)
    assert row["impression_count"] == 0
    conn.close()


# ---------------------------------------------------------------------------
# Test 3: Partial failure — error video gets zeros, success video gets real CTR
# ---------------------------------------------------------------------------

def test_ctr_partial_failure():
    """One video errors, another succeeds — both get snapshot rows."""
    real_conn = make_in_memory_conn()
    wrapper = NonClosingConnection(real_conn)

    def fake_ctr_metrics(video_id):
        if video_id == "vid001":
            return {"error": "API quota exceeded", "video_id": "vid001"}
        else:
            return {
                "video_id": video_id,
                "impressions": 3000,
                "ctr_percent": 3.5,
                "ctr_available": True,
            }

    with patch("tools.youtube_analytics.ctr_tracker._get_db", return_value=wrapper), \
         patch("tools.youtube_analytics.ctr_tracker.fetch_all_video_ids",
               return_value=FAKE_VIDEO_IDS[:2]), \
         patch("tools.youtube_analytics.ctr_tracker.fetch_video_metadata",
               return_value=FAKE_METADATA[:2]), \
         patch("tools.youtube_analytics.ctr_tracker.fetch_view_counts",
               return_value={"vid001": 1000, "vid002": 2000}), \
         patch("tools.youtube_analytics.ctr_tracker.get_ctr_metrics",
               side_effect=fake_ctr_metrics), \
         patch("tools.youtube_analytics.ctr_tracker.get_pattern_ctr_from_db",
               return_value={}), \
         patch("tools.youtube_analytics.ctr_tracker.DB_PATH", "ignored"):

        from tools.youtube_analytics.ctr_tracker import take_snapshot
        stored, snapshot_date = take_snapshot()

    # Both videos should have snapshot rows
    rows = real_conn.execute(
        "SELECT * FROM ctr_snapshots ORDER BY video_id"
    ).fetchall()
    assert len(rows) == 2, f"Expected 2 rows, got {len(rows)}"

    vid001_row = next(r for r in rows if r["video_id"] == "vid001")
    vid002_row = next(r for r in rows if r["video_id"] == "vid002")

    # Error video: ctr_percent=0, but view_count stored
    assert vid001_row["ctr_percent"] == pytest.approx(0.0)
    assert vid001_row["view_count"] == 1000

    # Success video: real CTR
    assert vid002_row["ctr_percent"] == pytest.approx(3.5)
    assert vid002_row["impression_count"] == 3000
    real_conn.close()


# ---------------------------------------------------------------------------
# Test 4: Summary output
# ---------------------------------------------------------------------------

def test_summary_output(capsys):
    """Summary print includes 'CTR updated for X/Y videos' and pattern scores."""
    real_conn = make_in_memory_conn()
    wrapper = NonClosingConnection(real_conn)

    ctr_responses = {
        "vid001": {"video_id": "vid001", "impressions": 5000, "ctr_percent": 4.2, "ctr_available": True},
        "vid002": {"video_id": "vid002", "impressions": None, "ctr_percent": None, "ctr_available": False},
        "vid003": {"video_id": "vid003", "impressions": 3000, "ctr_percent": 3.5, "ctr_available": True},
    }

    with patch("tools.youtube_analytics.ctr_tracker._get_db", return_value=wrapper), \
         patch("tools.youtube_analytics.ctr_tracker.fetch_all_video_ids",
               return_value=FAKE_VIDEO_IDS), \
         patch("tools.youtube_analytics.ctr_tracker.fetch_video_metadata",
               return_value=FAKE_METADATA), \
         patch("tools.youtube_analytics.ctr_tracker.fetch_view_counts",
               return_value=FAKE_VIEW_COUNTS), \
         patch("tools.youtube_analytics.ctr_tracker.get_ctr_metrics",
               side_effect=lambda vid: ctr_responses[vid]), \
         patch("tools.youtube_analytics.ctr_tracker.get_pattern_ctr_from_db",
               return_value={"declarative": 64}), \
         patch("tools.youtube_analytics.ctr_tracker.DB_PATH", "ignored"):

        from tools.youtube_analytics.ctr_tracker import take_snapshot
        take_snapshot()

    captured = capsys.readouterr()
    output = captured.out

    # Should show CTR count line (2 of 3 videos had CTR available)
    assert "CTR updated for" in output
    assert "2/3" in output

    # Should show pattern scores from DB
    assert "declarative" in output
    assert "64" in output

    real_conn.close()


# ---------------------------------------------------------------------------
# Test 5: Duplicate guard
# ---------------------------------------------------------------------------

def test_duplicate_guard():
    """When snapshot for today already exists, take_snapshot returns early without fetching."""
    real_conn = make_in_memory_conn()
    wrapper = NonClosingConnection(real_conn)
    today = "2026-03-15"

    # Pre-populate with today's snapshot
    real_conn.execute(
        "INSERT INTO ctr_snapshots (video_id, snapshot_date, ctr_percent, impression_count, "
        "view_count, is_late_entry, recorded_at) VALUES (?, ?, 0, 0, 1000, 0, ?)",
        ("vid001", today, today)
    )
    real_conn.commit()

    with patch("tools.youtube_analytics.ctr_tracker._get_db", return_value=wrapper), \
         patch("tools.youtube_analytics.ctr_tracker.fetch_all_video_ids") as mock_fetch, \
         patch("tools.youtube_analytics.ctr_tracker.date") as mock_date:

        mock_date.today.return_value.isoformat.return_value = today

        from tools.youtube_analytics.ctr_tracker import take_snapshot
        stored, snapshot_date = take_snapshot()

        # fetch_all_video_ids should NOT be called when snapshot already exists
        mock_fetch.assert_not_called()

    assert stored == 1  # Returns existing row count
    real_conn.close()
