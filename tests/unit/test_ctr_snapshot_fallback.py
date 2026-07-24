"""
Tests for the keywords.db -> analytics.db CTR bridge (growth_data).

Root cause fixed 2026-07-22: the Analytics API does not expose CTR for this
channel, so `ctr_tracker` writes reach data to keywords.db.ctr_snapshots — but
`growth_data --refresh` only ever read the (empty) API path, leaving
analytics.db.videos.ctr_percent NULL for all 58 videos. Every consumer of that
column read zero. `fetch_ctr_from_snapshots` is the missing bridge.

Logic is tested against a TEMP keywords.db built per-test (deterministic, no
dependence on live contents — repo rule). A single read-only smoke test runs
against the real keywords.db to satisfy the real-data-verification rule.
"""

import sqlite3
import unittest
from datetime import date, timedelta
from pathlib import Path
import tempfile

from tools.youtube_analytics.growth_data import (
    fetch_ctr_from_snapshots,
    merge_ctr_with_snapshot_fallback,
    _warn_if_stale,
    CTR_STALE_AFTER_DAYS,
    _KEYWORDS_DB,
)

_SNAPSHOT_DDL = """
CREATE TABLE ctr_snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    video_id TEXT,
    snapshot_date TEXT,
    ctr_percent REAL,
    impression_count INTEGER,
    view_count INTEGER NOT NULL DEFAULT 0,
    is_valid INTEGER NOT NULL DEFAULT 1
);
"""


def _make_db(rows):
    """rows: (video_id, snapshot_date, ctr_percent, impression_count[, is_valid]).
    is_valid defaults to 1 if omitted. Returns Path."""
    fd = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
    fd.close()
    conn = sqlite3.connect(fd.name)
    conn.executescript(_SNAPSHOT_DDL)
    norm = [(r + (1,)) if len(r) == 4 else r for r in rows]
    conn.executemany(
        "INSERT INTO ctr_snapshots (video_id, snapshot_date, ctr_percent, impression_count, is_valid)"
        " VALUES (?,?,?,?,?)", norm,
    )
    conn.commit()
    conn.close()
    return Path(fd.name)


class TestBridgeLogic(unittest.TestCase):
    def test_latest_snapshot_wins(self):
        db = _make_db([
            ("A", "2026-07-01", 5.0, 100),
            ("A", "2026-07-23", 2.0, 300),
        ])
        r = fetch_ctr_from_snapshots(["A"], keywords_db=db)
        self.assertEqual(r["A"], {"impressions": 300, "ctr_percent": 2.0,
                                  "ctr_as_of": "2026-07-23"})

    def test_genuine_zero_ctr_with_impressions_is_kept(self):
        # latest row is a real 0% on impressions; must NOT fall back to older nonzero
        db = _make_db([
            ("A", "2026-07-01", 5.0, 100),
            ("A", "2026-07-23", 0.0, 250),
        ])
        r = fetch_ctr_from_snapshots(["A"], keywords_db=db)
        self.assertEqual(r["A"]["ctr_percent"], 0.0)
        self.assertEqual(r["A"]["impressions"], 250)

    def test_zero_impression_rows_are_skipped(self):
        # A video whose only recent row has 0 impressions falls back to its last
        # impression-bearing row (older) — and the stamp reflects that older date.
        db = _make_db([
            ("A", "2026-02-23", 4.0, 900),
            ("A", "2026-07-23", 0.0, 0),
        ])
        r = fetch_ctr_from_snapshots(["A"], keywords_db=db)
        self.assertEqual(r["A"]["impressions"], 900)
        self.assertEqual(r["A"]["ctr_as_of"], "2026-02-23")

    def test_quarantined_rows_are_excluded(self):
        # is_valid=0 (a double-counted snapshot) must be skipped; the bridge
        # falls back to the latest VALID row — exactly the #59 07-13/07-23 case.
        db = _make_db([
            ("A", "2026-07-10", 4.0, 10690, 1),   # clean
            ("A", "2026-07-23", 1.5, 20919, 0),   # quarantined double-count
        ])
        r = fetch_ctr_from_snapshots(["A"], keywords_db=db)
        self.assertEqual(r["A"]["impressions"], 10690)
        self.assertEqual(r["A"]["ctr_as_of"], "2026-07-10")

    def test_duplicate_rows_same_date_are_deterministic(self):
        # Two rows, same video + date, different id. Must always pick MAX(id).
        db = _make_db([
            ("A", "2026-07-23", 1.0, 100),   # id 1
            ("A", "2026-07-23", 9.9, 999),   # id 2 — the winner
        ])
        r = fetch_ctr_from_snapshots(["A"], keywords_db=db)
        self.assertEqual(r["A"]["ctr_percent"], 9.9)
        self.assertEqual(r["A"]["impressions"], 999)

    def test_only_requested_ids_returned_in_store_shape(self):
        db = _make_db([("A", "2026-07-23", 2.0, 100), ("B", "2026-07-23", 3.0, 200)])
        r = fetch_ctr_from_snapshots(["A"], keywords_db=db)
        self.assertEqual(set(r), {"A"})
        self.assertLessEqual({"impressions", "ctr_percent", "ctr_as_of"}, set(r["A"]))

    def test_missing_db_returns_empty_not_crash(self):
        self.assertEqual(
            fetch_ctr_from_snapshots(["x"], keywords_db=Path("nope/missing.db")), {})

    def test_merge_lets_api_value_win(self):
        db = _make_db([("A", "2026-07-23", 2.0, 100)])
        merged = merge_ctr_with_snapshot_fallback(
            {"A": {"impressions": 1, "ctr_percent": 99.9}}, ["A"], keywords_db=db)
        self.assertEqual(merged["A"]["ctr_percent"], 99.9)

    def test_merge_fills_only_gaps(self):
        db = _make_db([("A", "2026-07-23", 2.0, 100)])
        merged = merge_ctr_with_snapshot_fallback({}, ["A"], keywords_db=db)
        self.assertEqual(merged["A"]["impressions"], 100)


class TestFreshnessContract(unittest.TestCase):
    """Guards the 2026-07-20 failure: ctr_tracker died, newest snapshot sat 10
    days old, and a naive bridge would serve it as current with no signal."""

    def _log(self):
        import io, logging
        from tools.youtube_analytics import growth_data as g
        buf = io.StringIO()
        h = logging.StreamHandler(buf)
        h.setLevel(logging.WARNING)
        logging.getLogger(g.__name__).addHandler(h)
        return buf

    def test_fresh_is_silent(self):
        buf = self._log()
        fresh = {"v": {"ctr_as_of": date.today().isoformat()}}
        self.assertEqual(_warn_if_stale(fresh), 0)
        self.assertNotIn("STALE", buf.getvalue())

    def test_stale_warns_and_reports_age(self):
        buf = self._log()
        old = (date.today() - timedelta(days=CTR_STALE_AFTER_DAYS + 2)).isoformat()
        self.assertEqual(_warn_if_stale({"v": {"ctr_as_of": old}}), CTR_STALE_AFTER_DAYS + 2)
        self.assertIn("STALE", buf.getvalue())

    def test_per_video_not_setwide(self):
        # 57 fresh + 1 ancient must WARN — the whole point of per-video.
        buf = self._log()
        ctr = {f"v{i}": {"ctr_as_of": date.today().isoformat()} for i in range(57)}
        ctr["old"] = {"ctr_as_of": (date.today() - timedelta(days=120)).isoformat()}
        self.assertEqual(_warn_if_stale(ctr), 120)
        self.assertIn("STALE", buf.getvalue())

    def test_exactly_at_bound_silent(self):
        buf = self._log()
        edge = (date.today() - timedelta(days=CTR_STALE_AFTER_DAYS)).isoformat()
        _warn_if_stale({"v": {"ctr_as_of": edge}})
        self.assertNotIn("STALE", buf.getvalue())

    def test_empty_returns_none(self):
        self.assertIsNone(_warn_if_stale({}))


@unittest.skipUnless(_KEYWORDS_DB.exists(), "keywords.db not present")
class TestLiveSmoke(unittest.TestCase):
    """Read-only real-data check — the logic is covered above on temp DBs; this
    only confirms the bridge runs against the live schema and returns the shape."""

    def test_bridge_runs_against_live_db(self):
        conn = sqlite3.connect(str(_KEYWORDS_DB))
        ids = [r[0] for r in conn.execute(
            "SELECT DISTINCT video_id FROM ctr_snapshots WHERE impression_count > 0 LIMIT 5")]
        conn.close()
        if not ids:
            self.skipTest("no impression-bearing snapshots live")
        r = fetch_ctr_from_snapshots(ids)
        self.assertTrue(r)
        for d in r.values():
            self.assertLessEqual({"impressions", "ctr_percent", "ctr_as_of"}, set(d))
            self.assertGreater(d["impressions"], 0)


if __name__ == "__main__":
    unittest.main()
