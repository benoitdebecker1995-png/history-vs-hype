"""
Integration test for CTR ingestion pipeline.

Tests the synthesis-to-DB pipeline: reading CROSS-VIDEO-SYNTHESIS.md and
writing CTR data to keywords.db via add_ctr_snapshot().
"""
import pytest
import textwrap
from pathlib import Path


# ─── Fixtures ───────────────────────────────────────────────────────────────

@pytest.fixture
def db_with_videos(tmp_path):
    """In-memory KeywordDB with 5 video_performance rows inserted."""
    from tools.discovery.database import KeywordDB
    db = KeywordDB(db_path=":memory:")

    # Insert 5 test videos with known video_ids and titles
    cursor = db._conn.cursor()
    today = "2026-02-23"
    rows = [
        ("VID001", "Venezuela vs Guyana: Essequibo",     1962, "2026-02-23"),
        ("VID002", "Turkey vs Greece Islands",            923,  "2026-02-23"),
        ("VID003", "Crusades Fact-Check",                 669,  "2026-02-23"),
        ("VID004", "Dark Ages Myth",                      110,  "2026-02-23"),
        ("VID005", "Christmas / Pagans",                  194,  "2026-02-23"),
    ]
    for video_id, title, views, fetched_at in rows:
        cursor.execute(
            """
            INSERT INTO video_performance (video_id, title, views, fetched_at)
            VALUES (?, ?, ?, ?)
            """,
            (video_id, title, views, fetched_at),
        )
    db._conn.commit()
    yield db
    db.close()


@pytest.fixture
def synthesis_with_ctr(tmp_path):
    """Temporary CROSS-VIDEO-SYNTHESIS.md with 3 CTR rows, 1 missing, 1 unmatched."""
    content = textwrap.dedent("""\
        # Cross-Video Synthesis

        ## Master Performance Table

        Ranked by views, with key metrics.

        | # | Title | Views | Retention | CTR | Impressions | Subs | Type |
        |---|-------|-------|-----------|-----|-------------|------|------|
        | 1 | Venezuela vs Guyana: Essequibo | 1,962 | 35.6% | 4.31% | 36,129 | +19 | Territorial |
        | 2 | Turkey vs Greece Islands | 923 | 41.0% | 3.10% | 21,546 | +13 | Territorial |
        | 3 | Crusades Fact-Check | 669 | 28.4% | 5.44% | 9,776 | +7 | Ideological Myth |
        | 4 | Dark Ages Myth | 110 | 31.7% | n/a | 7,237 | +2 | Ideological Myth |
        | 5 | Completely Unknown Video | 50 | 25.0% | 2.50% | 1,000 | +0 | Unknown |
    """)
    f = tmp_path / "CROSS-VIDEO-SYNTHESIS.md"
    f.write_text(content, encoding="utf-8")
    return f


# ─── Tests ──────────────────────────────────────────────────────────────────

def test_ingest_synthesis_ctr_importable():
    """ingest_synthesis_ctr is importable from tools.ctr_ingest."""
    from tools.ctr_ingest import ingest_synthesis_ctr
    assert callable(ingest_synthesis_ctr)


def test_ingest_writes_correct_rows(db_with_videos, synthesis_with_ctr):
    """Rows with CTR data whose titles match video_performance are written."""
    from tools.ctr_ingest import ingest_synthesis_ctr

    result = ingest_synthesis_ctr(synthesis_with_ctr, db_with_videos)

    # 3 videos have CTR + match (Essequibo, Turkey/Greece, Crusades)
    assert result["written"] == 3


def test_ingest_skips_missing_ctr(db_with_videos, synthesis_with_ctr):
    """Videos without CTR data (n/a) are skipped and counted."""
    from tools.ctr_ingest import ingest_synthesis_ctr

    result = ingest_synthesis_ctr(synthesis_with_ctr, db_with_videos)

    # Dark Ages has n/a CTR → skipped
    assert result["skipped"] >= 1


def test_ingest_counts_unmatched_titles(db_with_videos, synthesis_with_ctr):
    """Videos whose title cannot be matched to video_performance are tracked."""
    from tools.ctr_ingest import ingest_synthesis_ctr

    result = ingest_synthesis_ctr(synthesis_with_ctr, db_with_videos)

    # "Completely Unknown Video" has no match in video_performance
    assert result["unmatched"] >= 1


def test_ingest_result_has_required_keys(db_with_videos, synthesis_with_ctr):
    """Result dict has written, skipped, unmatched, errors keys."""
    from tools.ctr_ingest import ingest_synthesis_ctr

    result = ingest_synthesis_ctr(synthesis_with_ctr, db_with_videos)

    assert "written" in result
    assert "skipped" in result
    assert "unmatched" in result
    assert "errors" in result


def test_ingest_idempotent(db_with_videos, synthesis_with_ctr):
    """Running ingest twice on same data does not error (no crash on duplicate)."""
    from tools.ctr_ingest import ingest_synthesis_ctr

    result1 = ingest_synthesis_ctr(synthesis_with_ctr, db_with_videos)
    result2 = ingest_synthesis_ctr(synthesis_with_ctr, db_with_videos)

    # Both runs should complete without raising
    assert result1["written"] >= 0
    assert result2["written"] >= 0
    # errors list should be a list (may contain duplicate key errors, but no crash)
    assert isinstance(result2["errors"], list)


def test_ctr_values_written_to_db(db_with_videos, synthesis_with_ctr):
    """CTR values stored in ctr_snapshots match the synthesis table values."""
    from tools.ctr_ingest import ingest_synthesis_ctr

    ingest_synthesis_ctr(synthesis_with_ctr, db_with_videos)

    cursor = db_with_videos._conn.cursor()
    cursor.execute(
        "SELECT ctr_percent FROM ctr_snapshots WHERE video_id = ?",
        ("VID001",),
    )
    row = cursor.fetchone()
    assert row is not None, "VID001 (Essequibo) should have a ctr_snapshot row"
    assert abs(row[0] - 4.31) < 0.01


def test_dry_run_writes_nothing(db_with_videos, synthesis_with_ctr):
    """dry_run=True returns preview but writes no rows to ctr_snapshots."""
    from tools.ctr_ingest import ingest_synthesis_ctr

    result = ingest_synthesis_ctr(synthesis_with_ctr, db_with_videos, dry_run=True)

    cursor = db_with_videos._conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM ctr_snapshots")
    count = cursor.fetchone()[0]

    assert count == 0, "dry_run should not write any rows"
    assert result["written"] == 0
    assert result["would_write"] >= 3
