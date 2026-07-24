"""get_channel_ctr_benchmarks must compute the channel CTR average from the
canonical valid-latest read only — no quarantined double-count rows, no
unavailable (impression_count=0 / ctr=0) rows, one row per video (ADR-0017).

Before the fix, MAX(snapshot_date) with no is_valid filter let a video's invalid
2026-07-23 double-count row set its benchmark CTR.
"""

import sqlite3

import pytest

from tools.discovery.performance_tracker import PerformanceTracker


@pytest.fixture
def db(tmp_path):
    path = tmp_path / "keywords.db"
    conn = sqlite3.connect(path)
    conn.executescript(
        """
        CREATE TABLE video_performance (
            video_id TEXT UNIQUE NOT NULL,
            title TEXT,
            topic_type TEXT
        );
        CREATE TABLE ctr_snapshots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            video_id TEXT NOT NULL,
            snapshot_date DATE NOT NULL,
            ctr_percent REAL NOT NULL,
            impression_count INTEGER NOT NULL,
            view_count INTEGER NOT NULL,
            is_valid INTEGER NOT NULL DEFAULT 1,
            invalid_reason TEXT
        );
        """
    )
    conn.executemany(
        "INSERT INTO video_performance (video_id, title, topic_type) VALUES (?,?,?)",
        [("A", "t", "colonial"), ("B", "t", "colonial")],
    )
    conn.executemany(
        "INSERT INTO ctr_snapshots "
        "(video_id, snapshot_date, ctr_percent, impression_count, view_count, is_valid, invalid_reason) "
        "VALUES (?,?,?,?,?,?,?)",
        [
            # A: valid 4.0% on 07-10, then an INVALID 40.0% double-count on 07-23.
            ("A", "2026-07-10", 4.0, 1000, 100, 1, None),
            ("A", "2026-07-23", 40.0, 2000, 200, 0, "double-count"),
            # B: valid 6.0% on 07-10, plus a later view-only/unavailable row.
            ("B", "2026-07-10", 6.0, 800, 80, 1, None),
            ("B", "2026-07-22", 0.0, 0, 90, 1, None),  # ctr/impr = 0 -> unavailable
        ],
    )
    conn.commit()
    conn.close()
    return str(path)


def test_channel_avg_uses_valid_nonzero_only(db):
    pt = PerformanceTracker.connect(db)
    try:
        b = pt.get_channel_ctr_benchmarks()
    finally:
        pt.close()
    overall = b["overall"]
    # Only A@4.0 and B@6.0 count -> mean 5.0. The invalid 40.0 and the zero are out.
    assert overall["video_count"] == 2
    assert overall["avg_ctr"] == pytest.approx(5.0)
    assert overall["date_range"]["latest"] == "2026-07-10"  # not the invalid 07-23
    assert b["by_category"]["colonial"]["avg_ctr"] == pytest.approx(5.0)
