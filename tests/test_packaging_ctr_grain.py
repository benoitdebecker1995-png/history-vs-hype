"""Regression: the packaging path reads LIFETIME CTR, not the trailing snapshot.

ADR-0024. On 2026-08-03 `packaging_autopilot`'s channel-health block and
`packaging_intel`'s own-channel signal both read `videos.impressions` /
`videos.ctr_percent` — the collector's trailing snapshot — as if they were lifetime.

Measured damage on the live tree before the fix:

  * "Swap candidates (<4% CTR, >500 impressions)" reported **2**; the true lifetime
    answer was **42**. The >500 reliability test is nearly unsatisfiable against a
    column whose median is 56, so the detector was silently reporting almost nothing
    to fix.
  * Channel average CTR reported **5.45%** against a true lifetime **3.20%** — the
    snapshot covers only 36 of 57 videos and skews high.

These tests build a fixture where the two grains disagree in exactly that direction
and assert the packaging path picks lifetime.
"""
from __future__ import annotations

import sqlite3
import tempfile
from pathlib import Path

import pytest

from tools.youtube_analytics.growth_data import ensure_schema
from tools.youtube_analytics.store import AnalyticsStore
from tools.youtube_analytics import studio_import as si

_HEADER = "Content,Video title,Impressions,Impressions click-through rate (%)\n"


@pytest.fixture
def db_two_grains(tmp_path: Path) -> Path:
    """One video: tiny snapshot numbers, large lifetime numbers.

    Snapshot says 60 impressions @ 9.0% — fails a >500 impression test, and its CTR
    is above a 4% floor. Lifetime says 20,000 @ 2.0% — passes the impression test and
    is below the floor. Any consumer reading the wrong grain flips the answer.
    """
    db = tmp_path / "analytics.db"
    conn = sqlite3.connect(db)
    ensure_schema(conn)
    conn.execute(
        "INSERT INTO videos (video_id, title, published_at, duration_seconds, "
        "fetched_at, views, avg_view_percentage, impressions, ctr_percent, ctr_as_of) "
        "VALUES (?,?,?,?,?,?,?,?,?,?)",
        ("V1", "Guatemala vs Belize", "2026-01-01", 600, "2026-07-28",
         50, 35.0, 60, 9.0, "2026-07-28"),
    )
    conn.commit()
    conn.close()

    csv = tmp_path / "export.csv"
    csv.write_text(_HEADER + "V1,Guatemala vs Belize,20000,2.0\n", encoding="utf-8")
    si.import_studio_csv(csv, as_of="2026-07-23", analytics_db=db)
    return db


def test_fixture_really_does_disagree(db_two_grains: Path) -> None:
    """Guard the guard — if the grains ever agree, the tests below prove nothing."""
    with AnalyticsStore.open(db_two_grains) as s:
        life = s.lifetime_ctr_by_video()["V1"]
        snap = s.snapshot_ctr_by_video()["V1"]
    assert (life["impressions"], life["ctr_percent"]) == (20000, 2.0)
    assert (snap["impressions"], snap["ctr_percent"]) == (60, 9.0)


def test_swap_candidate_test_uses_lifetime_impressions(db_two_grains: Path) -> None:
    """The <4% CTR + >500 impressions rule, evaluated on both grains.

    This is the 2-vs-42 bug in miniature: on snapshot the video is invisible, on
    lifetime it is a swap candidate.
    """
    with AnalyticsStore.open(db_two_grains) as s:
        lifetime = s.lifetime_ctr_by_video()
        snapshot = s.snapshot_ctr_by_video()

    def swap_candidates(rows):
        return sum(
            1 for r in rows.values()
            if 0 < (r["ctr_percent"] or 0) < 4.0 and (r["impressions"] or 0) > 500
        )

    assert swap_candidates(lifetime) == 1, "lifetime must surface the swap candidate"
    assert swap_candidates(snapshot) == 0, "snapshot hides it — the original bug"


def test_channel_average_ctr_uses_lifetime(db_two_grains: Path) -> None:
    with AnalyticsStore.open(db_two_grains) as s:
        lifetime = s.lifetime_ctr_by_video()
    ctrs = [r["ctr_percent"] for r in lifetime.values() if r["ctr_percent"]]
    assert sum(ctrs) / len(ctrs) == pytest.approx(2.0)


def test_every_returned_row_states_its_grain(db_two_grains: Path) -> None:
    """A packaging number must not be able to travel without its provenance."""
    with AnalyticsStore.open(db_two_grains) as s:
        for grain, rows in (
            ("lifetime", s.lifetime_ctr_by_video()),
            ("snapshot", s.snapshot_ctr_by_video()),
        ):
            for rec in rows.values():
                assert rec["grain"] == grain
                assert rec["as_of"], "as_of must never be empty"
                assert rec["source_table"] in {"studio_ctr_rows", "videos"}
