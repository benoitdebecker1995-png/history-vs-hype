"""
Swap Ledger + growth-lever regression tests.

Covers:
  - swap_ledger.open_experiment rejects a two-variable swap (single-variable guard)
  - swap_ledger.read_experiment computes delta_pp + verdict from a seeded ctr_snapshot
  - swap_ledger.list/experiments_due flags an overdue PENDING experiment
  - packaging_intel.scan_competitor_outliers respects the `days` recency filter
    (the latent bug fix: the SQL now actually filters published_at)

Run:
    pytest tools/tests/test_swap_ledger.py -v
"""

import sqlite3
import sys
from datetime import date, timedelta
from pathlib import Path

import pytest

_REPO_ROOT = Path(__file__).resolve().parents[2]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from tools import swap_ledger  # noqa: E402
from tools.packaging_intel import scan_competitor_outliers  # noqa: E402


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------
@pytest.fixture
def ledger_db(tmp_path, monkeypatch):
    """A temp keywords-like DB with a ctr_snapshots table + redirected MD view."""
    db = tmp_path / "keywords.db"
    conn = sqlite3.connect(db)
    conn.execute(
        """
        CREATE TABLE ctr_snapshots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            video_id TEXT NOT NULL,
            snapshot_date DATE NOT NULL,
            ctr_percent REAL NOT NULL,
            impression_count INTEGER NOT NULL,
            view_count INTEGER NOT NULL,
            is_valid INTEGER NOT NULL DEFAULT 1
        )
        """
    )
    conn.commit()
    conn.close()
    # Redirect the auto-generated MD view so the real one isn't clobbered.
    monkeypatch.setattr(swap_ledger, "_LEDGER_MD", tmp_path / "SWAP-LEDGER.md")
    return str(db)


def _seed_snapshot(db_path, video_id, ctr, impr, snapshot_date):
    conn = sqlite3.connect(db_path)
    conn.execute(
        "INSERT INTO ctr_snapshots (video_id, snapshot_date, ctr_percent, "
        "impression_count, view_count) VALUES (?, ?, ?, ?, ?)",
        (video_id, snapshot_date, ctr, impr, 0),
    )
    conn.commit()
    conn.close()


# ---------------------------------------------------------------------------
# Single-variable guard
# ---------------------------------------------------------------------------
def test_open_rejects_two_variable_swap(ledger_db):
    res = swap_ledger.open_experiment(
        video_id="VID1", variable="title", also_changed="thumbnail",
        baseline_ctr=2.0, db_path=ledger_db,
    )
    assert "error" in res
    assert "TWO-VARIABLE" in res["error"]


def test_open_accepts_single_variable(ledger_db):
    res = swap_ledger.open_experiment(
        video_id="VID1", variable="thumbnail", also_changed=None,
        baseline_ctr=1.91, baseline_impr=2672, surface="Suggested",
        read_in_days=21, db_path=ledger_db,
    )
    assert res.get("status") == "opened"
    assert isinstance(res["id"], int)


# ---------------------------------------------------------------------------
# read computes delta + verdict
# ---------------------------------------------------------------------------
def test_read_computes_lift(ledger_db):
    opened = swap_ledger.open_experiment(
        video_id="VIDLIFT", variable="thumbnail", baseline_ctr=2.0,
        baseline_impr=1000, read_in_days=0, db_path=ledger_db,
    )
    # Post-swap reading: 3.0% (today, on/after swap_date) -> +1.0pp -> LIFT
    _seed_snapshot(ledger_db, "VIDLIFT", 3.0, 1500, date.today().isoformat())
    res = swap_ledger.read_experiment(opened["id"], db_path=ledger_db)
    assert res["verdict"] == "LIFT"
    assert res["delta_pp"] == pytest.approx(1.0)
    assert "recipe_line" in res  # LIFT emits a proven-recipes paste line


def test_read_computes_drop(ledger_db):
    opened = swap_ledger.open_experiment(
        video_id="VIDDROP", variable="title", baseline_ctr=3.0,
        read_in_days=0, db_path=ledger_db,
    )
    _seed_snapshot(ledger_db, "VIDDROP", 1.5, 1500, date.today().isoformat())
    res = swap_ledger.read_experiment(opened["id"], db_path=ledger_db)
    assert res["verdict"] == "DROP"
    assert res["delta_pp"] == pytest.approx(-1.5)


def test_read_without_snapshot_errors(ledger_db):
    opened = swap_ledger.open_experiment(
        video_id="VIDNONE", variable="thumbnail", baseline_ctr=2.0,
        read_in_days=0, db_path=ledger_db,
    )
    res = swap_ledger.read_experiment(opened["id"], db_path=ledger_db)
    assert "error" in res
    assert "No post-swap" in res["error"]


# ---------------------------------------------------------------------------
# list / experiments_due
# ---------------------------------------------------------------------------
def test_list_flags_overdue_pending(ledger_db):
    swap_ledger.open_experiment(
        video_id="VIDDUE", variable="thumbnail", baseline_ctr=2.0,
        read_in_days=-1, db_path=ledger_db,  # planned read date in the past
    )
    due = swap_ledger.experiments_due(db_path=ledger_db)
    assert len(due) == 1
    assert due[0]["video_id"] == "VIDDUE"
    assert due[0]["due"] is True


def test_list_not_due_when_future(ledger_db):
    swap_ledger.open_experiment(
        video_id="VIDFUT", variable="thumbnail", baseline_ctr=2.0,
        read_in_days=30, db_path=ledger_db,
    )
    assert swap_ledger.experiments_due(db_path=ledger_db) == []


# ---------------------------------------------------------------------------
# Growth lever — scan_competitor_outliers days filter (the bug fix)
# ---------------------------------------------------------------------------
@pytest.fixture
def intel_db(tmp_path):
    db = tmp_path / "intel.db"
    conn = sqlite3.connect(db)
    conn.execute(
        """
        CREATE TABLE competitor_videos (
            video_id TEXT, title TEXT, views INTEGER, is_outlier INTEGER,
            outlier_ratio REAL, topic_cluster TEXT, published_at TEXT, channel_id TEXT
        )
        """
    )
    conn.execute("CREATE TABLE competitor_channels (channel_id TEXT)")
    recent = (date.today() - timedelta(days=10)).isoformat() + "T00:00:00Z"
    old = (date.today() - timedelta(days=200)).isoformat() + "T00:00:00Z"
    conn.executemany(
        "INSERT INTO competitor_videos VALUES (?,?,?,?,?,?,?,?)",
        [
            ("rNEW", "Recent outlier", 500000, 1, 5.0, "topic", recent, "C1"),
            ("rOLD", "Old outlier", 900000, 1, 9.0, "topic", old, "C1"),
        ],
    )
    conn.commit()
    conn.close()
    return str(db)


def test_scan_outliers_excludes_old(intel_db):
    out = scan_competitor_outliers(db_path=intel_db, min_ratio=3.0, days=90)
    titles = [o["title"] for o in out]
    assert "Recent outlier" in titles
    assert "Old outlier" not in titles  # >90 days -> filtered (the bug fix)


def test_scan_outliers_wide_window_includes_old(intel_db):
    out = scan_competitor_outliers(db_path=intel_db, min_ratio=3.0, days=365)
    titles = [o["title"] for o in out]
    assert "Recent outlier" in titles
    assert "Old outlier" in titles
