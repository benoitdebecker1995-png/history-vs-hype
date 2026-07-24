"""
Tests for the Studio CSV importer (Codex spec §1.D, 2026-07-22).

Temp analytics.db per test (repo rule). One real-data acceptance check against
the July-23 export lives in test_real_july23_csv.
"""
import sqlite3
import unittest
from pathlib import Path
import tempfile

from tools.youtube_analytics.growth_data import ensure_schema
from tools.youtube_analytics.store import AnalyticsStore
from tools.youtube_analytics import studio_import as si

_HEADER = "Content,Video title,Impressions,Impressions click-through rate (%)\n"


def _csv(tmp: Path, body: str, name="export.csv") -> Path:
    p = tmp / name
    p.write_text(_HEADER + body, encoding="utf-8")
    return p


def _db_with_videos(tmp: Path, vids) -> Path:
    dbp = tmp / "analytics.db"
    conn = sqlite3.connect(dbp)
    ensure_schema(conn)
    conn.executemany(
        "INSERT INTO videos (video_id, title, published_at, duration_seconds, fetched_at) "
        "VALUES (?,?,?,?,?)",
        [(v, v, "2026-01-01", 300, "2026-07-23") for v in vids],
    )
    conn.commit()
    conn.close()
    return dbp


class TestStudioImport(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())

    def test_imports_and_matches(self):
        db = _db_with_videos(self.tmp, ["A", "B"])
        csv = _csv(self.tmp, "Total,,999,9.9\nA,Title A,1000,2.5\nB,Title B,500,1.0\n")
        r = si.import_studio_csv(csv, as_of="2026-07-23", analytics_db=db)
        self.assertEqual(r["status"], "imported")
        self.assertEqual(r["rows"], 2)          # Total skipped
        self.assertEqual(r["matched"], 2)
        with AnalyticsStore.open(db) as s:
            life, asof = s.latest_studio_lifetime()
        self.assertEqual(asof, "2026-07-23")
        self.assertEqual(life["A"], {"impressions": 1000, "ctr_percent": 2.5})

    def test_reimport_same_file_is_idempotent(self):
        db = _db_with_videos(self.tmp, ["A"])
        csv = _csv(self.tmp, "A,T,100,1.0\n")
        si.import_studio_csv(csv, as_of="2026-07-23", analytics_db=db)
        r2 = si.import_studio_csv(csv, as_of="2026-07-23", analytics_db=db)
        self.assertEqual(r2["status"], "duplicate")
        with AnalyticsStore.open(db) as s:
            n = s._conn.execute("SELECT COUNT(*) FROM studio_ctr_imports").fetchone()[0]
        self.assertEqual(n, 1)

    def test_unmatched_rows_stored_and_reported(self):
        db = _db_with_videos(self.tmp, ["A"])          # B not known
        csv = _csv(self.tmp, "A,T,100,1.0\nB,T,50,0.5\n")
        r = si.import_studio_csv(csv, as_of="2026-07-23", analytics_db=db)
        self.assertEqual(r["matched"], 1)
        self.assertEqual(r["unmatched"], 1)

    def test_genuine_zero_ctr_preserved(self):
        db = _db_with_videos(self.tmp, ["A"])
        csv = _csv(self.tmp, "A,T,800,0.0\n")
        si.import_studio_csv(csv, as_of="2026-07-23", analytics_db=db)
        with AnalyticsStore.open(db) as s:
            life, _ = s.latest_studio_lifetime()
        self.assertEqual(life["A"]["ctr_percent"], 0.0)

    def test_missing_header_rejected(self):
        db = _db_with_videos(self.tmp, ["A"])
        bad = self.tmp / "bad.csv"
        bad.write_text("Content,Video title\nA,T\n", encoding="utf-8")
        with self.assertRaises(si.StudioImportError):
            si.import_studio_csv(bad, as_of="2026-07-23", analytics_db=db)

    def test_duplicate_video_id_rejected(self):
        db = _db_with_videos(self.tmp, ["A"])
        csv = _csv(self.tmp, "A,T,100,1.0\nA,T,200,2.0\n")
        with self.assertRaises(si.StudioImportError):
            si.import_studio_csv(csv, as_of="2026-07-23", analytics_db=db)

    def test_ctr_out_of_range_rejected(self):
        db = _db_with_videos(self.tmp, ["A"])
        csv = _csv(self.tmp, "A,T,100,150.0\n")
        with self.assertRaises(si.StudioImportError):
            si.import_studio_csv(csv, as_of="2026-07-23", analytics_db=db)

    def test_date_range_requires_start_and_end(self):
        db = _db_with_videos(self.tmp, ["A"])
        csv = _csv(self.tmp, "A,T,100,1.0\n")
        with self.assertRaises(si.StudioImportError):
            si.import_studio_csv(csv, as_of="2026-07-23", start="2026-07-01", analytics_db=db)


class TestRealJuly23(unittest.TestCase):
    CSV = Path("channel-data/analytics-exports/Table data.csv")

    @unittest.skipUnless(CSV.exists(), "July-23 Studio CSV not present")
    def test_acceptance_fixture(self):
        # Parse only (no DB) — the real import ran against live analytics.db already.
        rows = si.parse_studio_csv(self.CSV)
        self.assertEqual(len(rows), 57)
        by_id = {r["video_id"]: r for r in rows}
        self.assertIn("OHWq4jY8iAY", by_id)
        self.assertEqual(by_id["OHWq4jY8iAY"]["impressions"], 10925)
        self.assertEqual(by_id["OHWq4jY8iAY"]["ctr_percent"], 1.6)


if __name__ == "__main__":
    unittest.main()
