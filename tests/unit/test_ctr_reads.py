"""Behavioral pins for the canonical valid-latest-CTR read seam (ctr_reads).

Reproduces the exact defect shape the 2026-07-23 audit found in keywords.db:
a video whose latest snapshot is an INVALID (quarantined) double-count row that
was winning MAX(snapshot_date) over its valid earlier row, plus duplicate valid
rows on the same date that multiplied a video's weight. Expected values are
hand-derived, not recomputed the way the query computes them.
"""

import sqlite3

import pytest

from tools.discovery.ctr_reads import (
    latest_valid_ctr_by_video,
    latest_valid_ctr_for,
    latest_valid_snapshot_date,
)


@pytest.fixture
def conn():
    c = sqlite3.connect(":memory:")
    c.executescript(
        """
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
    rows = [
        # A: valid 07-10 (ctr 5.0) then an INVALID 07-23 double-count (ctr 9.9).
        ("A", "2026-07-10", 5.0, 1000, 100, 1, None),
        ("A", "2026-07-23", 9.9, 2000, 200, 0, "collector double-count"),
        # B: two VALID rows on the SAME date — must collapse to one (highest id).
        ("B", "2026-07-10", 4.0, 800, 80, 1, None),
        ("B", "2026-07-10", 4.5, 900, 90, 1, None),
        # C: only INVALID rows — excluded entirely.
        ("C", "2026-07-23", 8.0, 500, 50, 0, "collector double-count"),
        # D: valid but zero CTR — excluded when require_ctr, included otherwise.
        ("D", "2026-07-10", 0.0, 300, 30, 1, None),
    ]
    c.executemany(
        "INSERT INTO ctr_snapshots "
        "(video_id, snapshot_date, ctr_percent, impression_count, view_count, is_valid, invalid_reason) "
        "VALUES (?,?,?,?,?,?,?)",
        rows,
    )
    c.commit()
    yield c
    c.close()


def test_by_video_excludes_invalid_and_zero(conn):
    got = latest_valid_ctr_by_video(conn, require_ctr=True)
    assert set(got) == {"A", "B"}  # C invalid-only, D zero-CTR both excluded
    # A must use its VALID 07-10 row (5.0), NOT the invalid 07-23 row (9.9).
    assert got["A"]["ctr_percent"] == 5.0
    assert got["A"]["snapshot_date"] == "2026-07-10"


def test_by_video_dedups_same_date_to_highest_id(conn):
    got = latest_valid_ctr_by_video(conn, require_ctr=True)
    # B had two valid rows on 07-10; exactly one survives, the later insert (4.5).
    assert got["B"]["ctr_percent"] == 4.5


def test_by_video_includes_zero_when_not_required(conn):
    got = latest_valid_ctr_by_video(conn, require_ctr=False)
    assert "D" in got and got["D"]["ctr_percent"] == 0.0
    assert "C" not in got  # still invalid-only


def test_for_single_video_picks_valid(conn):
    rec = latest_valid_ctr_for(conn, "A", require_ctr=True)
    assert rec is not None
    assert rec["ctr_percent"] == 5.0 and rec["snapshot_date"] == "2026-07-10"


def test_for_invalid_only_video_is_none(conn):
    assert latest_valid_ctr_for(conn, "C", require_ctr=True) is None


def test_for_after_date_filters(conn):
    # Nothing valid on/after 07-15 for A (only the invalid 07-23 exists).
    assert latest_valid_ctr_for(conn, "A", after_date="2026-07-15") is None
    assert latest_valid_ctr_for(conn, "A", after_date="2026-07-01") is not None


def test_latest_valid_date_ignores_invalid(conn):
    # 07-23 rows are all invalid -> newest VALID date is 07-10.
    assert latest_valid_snapshot_date(conn, require_ctr=True) == "2026-07-10"


def test_reads_never_raise_on_missing_table():
    empty = sqlite3.connect(":memory:")
    try:
        assert latest_valid_ctr_by_video(empty) == {}
        assert latest_valid_ctr_for(empty, "A") is None
        assert latest_valid_snapshot_date(empty) is None
    finally:
        empty.close()
