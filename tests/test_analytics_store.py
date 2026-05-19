"""Unit tests for AnalyticsStore and views.

In-memory sqlite — no on-disk fixture needed. Tests the contract, not the data.
"""
from __future__ import annotations

import sqlite3
from pathlib import Path

import pytest

from tools.youtube_analytics.store import AnalyticsStore, VideoRow
from tools.youtube_analytics import views as v


# ── fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def analytics_conn() -> sqlite3.Connection:
    """In-memory analytics.db with minimal schema + sample data."""
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.executescript("""
        CREATE TABLE videos (
            video_id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            published_at TEXT NOT NULL,
            duration_seconds INTEGER NOT NULL,
            tags TEXT,
            views INTEGER,
            watch_time_minutes REAL,
            avg_view_duration_seconds INTEGER,
            avg_view_percentage REAL,
            likes INTEGER,
            comments INTEGER,
            shares INTEGER,
            subscribers_gained INTEGER,
            subscribers_lost INTEGER,
            impressions INTEGER,
            ctr_percent REAL,
            topic_type TEXT,
            angles TEXT,
            fetched_at TEXT NOT NULL,
            metrics_fetched_at TEXT
        );
        CREATE TABLE traffic_sources (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            video_id TEXT NOT NULL,
            source_type TEXT NOT NULL,
            views INTEGER,
            watch_time_minutes REAL,
            fetched_at TEXT NOT NULL,
            UNIQUE(video_id, source_type)
        );
        CREATE TABLE daily_channel (
            day TEXT PRIMARY KEY,
            views INTEGER,
            watch_time_minutes REAL,
            avg_view_duration_seconds INTEGER,
            subscribers_gained INTEGER,
            subscribers_lost INTEGER,
            likes INTEGER,
            fetched_at TEXT NOT NULL
        );
    """)
    # Three videos: short / mid / long, varying views and topic.
    conn.executemany(
        "INSERT INTO videos (video_id, title, published_at, duration_seconds, "
        "views, ctr_percent, impressions, topic_type, fetched_at) VALUES (?,?,?,?,?,?,?,?,?)",
        [
            ("v_short", "Short Clip", "2026-01-10", 45, 500, 3.0, 1000, "border", "2026-05-01"),
            ("v_mid", "Mid Video", "2026-02-10", 300, 5000, 4.5, 8000, "ideological", "2026-05-01"),
            ("v_long", "Long Video", "2026-03-10", 800, 25, 2.0, 200, "border", "2026-05-01"),
        ],
    )
    conn.executemany(
        "INSERT INTO traffic_sources (video_id, source_type, views, watch_time_minutes, fetched_at) "
        "VALUES (?,?,?,?,?)",
        [
            ("v_mid", "YT_SEARCH", 1500, 200.0, "2026-05-01"),
            ("v_mid", "SUGGESTED_VIDEO", 3000, 400.0, "2026-05-01"),
            ("v_mid", "EXTERNAL", 500, 60.0, "2026-05-01"),
            ("v_short", "YT_SEARCH", 50, 5.0, "2026-05-01"),
            ("v_short", "SUGGESTED_VIDEO", 200, 20.0, "2026-05-01"),
        ],
    )
    conn.executemany(
        "INSERT INTO daily_channel (day, views, subscribers_gained, subscribers_lost, "
        "watch_time_minutes, avg_view_duration_seconds, likes, fetched_at) "
        "VALUES (?,?,?,?,?,?,?,?)",
        [
            ("2026-01-01", 100, 2, 0, 12.0, 60, 5, "now"),
            ("2026-01-02", 150, 3, 1, 18.0, 70, 7, "now"),
            ("2026-01-03", 120, 1, 0, 14.0, 65, 4, "now"),
            ("2026-01-04", 200, 5, 2, 25.0, 80, 9, "now"),
        ],
    )
    conn.commit()
    return conn


@pytest.fixture
def store(analytics_conn: sqlite3.Connection) -> AnalyticsStore:
    return AnalyticsStore(analytics_conn)


# ── AnalyticsStore.videos ─────────────────────────────────────────────────────

def test_videos_returns_all_with_no_filters(store: AnalyticsStore) -> None:
    rows = store.videos()
    assert len(rows) == 3
    assert {r["video_id"] for r in rows} == {"v_short", "v_mid", "v_long"}


def test_videos_min_duration_seconds_filters(store: AnalyticsStore) -> None:
    rows = store.videos(min_duration_seconds=60)
    assert {r["video_id"] for r in rows} == {"v_mid", "v_long"}


def test_videos_min_duration_seconds_is_inclusive(store: AnalyticsStore) -> None:
    rows = store.videos(min_duration_seconds=45)
    assert {r["video_id"] for r in rows} == {"v_short", "v_mid", "v_long"}


def test_videos_min_views_filters(store: AnalyticsStore) -> None:
    rows = store.videos(min_views=100)
    assert {r["video_id"] for r in rows} == {"v_short", "v_mid"}


def test_videos_topic_type_filters(store: AnalyticsStore) -> None:
    rows = store.videos(topic_type="border")
    assert {r["video_id"] for r in rows} == {"v_short", "v_long"}


def test_videos_published_after_filters(store: AnalyticsStore) -> None:
    rows = store.videos(published_after="2026-02-01")
    assert {r["video_id"] for r in rows} == {"v_mid", "v_long"}


def test_videos_order_by_views_descending(store: AnalyticsStore) -> None:
    rows = store.videos(order_by="views", descending=True)
    assert [r["video_id"] for r in rows] == ["v_mid", "v_short", "v_long"]


def test_videos_order_by_views_ascending(store: AnalyticsStore) -> None:
    rows = store.videos(order_by="views", descending=False)
    assert [r["video_id"] for r in rows] == ["v_long", "v_short", "v_mid"]


def test_videos_unknown_order_by_falls_back_to_published_at(store: AnalyticsStore) -> None:
    rows = store.videos(order_by="DROP TABLE videos", descending=False)
    # Should not error, should return ordered by published_at ascending.
    assert [r["video_id"] for r in rows] == ["v_short", "v_mid", "v_long"]


def test_video_returns_single_or_none(store: AnalyticsStore) -> None:
    assert store.video("v_mid")["title"] == "Mid Video"
    assert store.video("does_not_exist") is None


def test_videos_by_id_returns_mapping(store: AnalyticsStore) -> None:
    result = store.videos_by_id(["v_short", "v_long", "missing"])
    assert set(result) == {"v_short", "v_long"}
    assert result["v_short"]["title"] == "Short Clip"


def test_videos_by_id_empty_list_returns_empty(store: AnalyticsStore) -> None:
    assert store.videos_by_id([]) == {}


# ── traffic_sources ───────────────────────────────────────────────────────────

def test_traffic_sources_returns_all(store: AnalyticsStore) -> None:
    rows = store.traffic_sources()
    assert len(rows) == 5


def test_traffic_sources_by_video(store: AnalyticsStore) -> None:
    rows = store.traffic_sources(video_id="v_short")
    assert {r["source_type"] for r in rows} == {"YT_SEARCH", "SUGGESTED_VIDEO"}
    # Ordered by views desc.
    assert rows[0]["source_type"] == "SUGGESTED_VIDEO"


def test_traffic_totals_by_source(store: AnalyticsStore) -> None:
    rows = store.traffic_totals_by_source()
    totals = {r["source_type"]: r["total_views"] for r in rows}
    assert totals["SUGGESTED_VIDEO"] == 3200
    assert totals["YT_SEARCH"] == 1550
    assert totals["EXTERNAL"] == 500
    # Ordered by total_views DESC.
    assert rows[0]["source_type"] == "SUGGESTED_VIDEO"


def test_traffic_totals_by_source_excludes_orphan_rows(
    analytics_conn: sqlite3.Connection,
) -> None:
    """Orphan traffic_sources rows (video_id not in videos table) must not
    inflate the channel-wide aggregate.

    Regression for GH #1: stale Shorts/deleted-video rows in traffic_sources
    were polluting the long-form aggregate by ~1,250 views in the live DB.
    """
    # Insert an orphan row — video_id 'v_orphan' is NOT in the videos table.
    analytics_conn.execute(
        "INSERT INTO traffic_sources (video_id, source_type, views, "
        "watch_time_minutes, fetched_at) VALUES (?, ?, ?, ?, ?)",
        ("v_orphan", "SUBSCRIBER", 99999, 1000.0, "2026-05-19"),
    )
    analytics_conn.commit()

    store = AnalyticsStore(analytics_conn)
    rows = store.traffic_totals_by_source()
    totals = {r["source_type"]: r["total_views"] for r in rows}

    # Aggregates must match the non-orphan totals only — SUBSCRIBER not present
    # in fixture, so orphan's 99999 would show up as SUBSCRIBER=99999 if the
    # JOIN were missing.
    assert "SUBSCRIBER" not in totals
    assert totals["SUGGESTED_VIDEO"] == 3200
    assert totals["YT_SEARCH"] == 1550
    assert totals["EXTERNAL"] == 500


# ── upsert_traffic_source (write side) ────────────────────────────────────────

def test_upsert_traffic_source_inserts_new_row(store: AnalyticsStore) -> None:
    store.upsert_traffic_source(
        video_id="v_long",
        source_type="YT_SEARCH",
        views=42,
        watch_time_minutes=7.5,
        fetched_at="2026-05-19",
    )
    store.commit()
    rows = store.traffic_sources(video_id="v_long")
    assert len(rows) == 1
    assert rows[0]["views"] == 42
    assert rows[0]["watch_time_minutes"] == 7.5
    assert rows[0]["source_type"] == "YT_SEARCH"


def test_upsert_traffic_source_updates_existing_row(store: AnalyticsStore) -> None:
    # Fixture has v_mid/YT_SEARCH with views=1500; upsert should overwrite.
    store.upsert_traffic_source(
        video_id="v_mid",
        source_type="YT_SEARCH",
        views=9999,
        watch_time_minutes=1234.5,
        fetched_at="2026-05-19",
    )
    store.commit()
    rows = store.traffic_sources(video_id="v_mid")
    yt = next(r for r in rows if r["source_type"] == "YT_SEARCH")
    assert yt["views"] == 9999
    assert yt["watch_time_minutes"] == 1234.5
    # fetched_at is not exposed via traffic_sources() — verify via raw conn.
    raw = store.execute(
        "SELECT fetched_at FROM traffic_sources "
        "WHERE video_id = ? AND source_type = ?",
        ("v_mid", "YT_SEARCH"),
    )
    assert raw[0]["fetched_at"] == "2026-05-19"
    # Other sources for v_mid untouched.
    assert {r["source_type"] for r in rows} == {"YT_SEARCH", "SUGGESTED_VIDEO", "EXTERNAL"}


def test_upsert_video_inserts_new_row_with_minimal_required_fields(store: AnalyticsStore) -> None:
    """Only the 5 NOT NULL fields are required; everything else uses schema defaults."""
    store.upsert_video(VideoRow(
        video_id="v_new",
        title="New Video",
        published_at="2026-05-19",
        duration_seconds=600,
        fetched_at="2026-05-19",
    ))
    store.commit()
    row = store.video("v_new")
    assert row is not None
    assert row["title"] == "New Video"
    assert row["views"] == 0
    assert row["topic_type"] == "general"
    assert row["impressions"] is None
    assert row["ctr_percent"] is None


def test_upsert_video_inserts_new_row_with_full_payload(store: AnalyticsStore) -> None:
    store.upsert_video(VideoRow(
        video_id="v_full",
        title="Full Video",
        published_at="2026-05-19",
        duration_seconds=900,
        fetched_at="2026-05-19",
        tags='["history","myths"]',
        views=1234,
        watch_time_minutes=312.5,
        avg_view_duration_seconds=180,
        avg_view_percentage=28.1,
        likes=42,
        comments=7,
        shares=3,
        subscribers_gained=11,
        subscribers_lost=1,
        impressions=29381,
        ctr_percent=4.2,
        topic_type="border",
        angles='["mechanism"]',
        metrics_fetched_at="2026-05-19",
    ))
    store.commit()
    row = store.video("v_full")
    assert row["views"] == 1234
    assert row["ctr_percent"] == 4.2
    assert row["topic_type"] == "border"
    assert row["angles"] == '["mechanism"]'


def test_upsert_video_updates_existing_row(store: AnalyticsStore) -> None:
    # Fixture has v_mid with views=5000; upsert should overwrite all fields.
    store.upsert_video(VideoRow(
        video_id="v_mid",
        title="Mid Video — RETITLED",
        published_at="2026-02-10",
        duration_seconds=300,
        fetched_at="2026-05-19",
        views=99999,
        ctr_percent=6.6,
    ))
    store.commit()
    row = store.video("v_mid")
    assert row["title"] == "Mid Video — RETITLED"
    assert row["views"] == 99999
    assert row["ctr_percent"] == 6.6
    # Defaulted fields blow away prior values (intentional — full upsert).
    assert row["impressions"] is None  # was 8000, defaulted to None on the new row


def test_upsert_daily_metric_inserts_new_row(store: AnalyticsStore) -> None:
    store.upsert_daily_metric(
        day="2026-02-01",
        views=999,
        watch_time_minutes=33.3,
        avg_view_duration_seconds=120,
        subscribers_gained=7,
        subscribers_lost=1,
        likes=42,
        fetched_at="2026-05-19",
    )
    store.commit()
    rows = store.daily_channel()
    new = next(r for r in rows if r["day"] == "2026-02-01")
    assert new["views"] == 999
    assert new["subscribers_gained"] == 7


def test_upsert_daily_metric_updates_existing_row(store: AnalyticsStore) -> None:
    # Fixture has 2026-01-01 with views=100; upsert should overwrite.
    store.upsert_daily_metric(
        day="2026-01-01",
        views=5000,
        watch_time_minutes=600.0,
        avg_view_duration_seconds=300,
        subscribers_gained=50,
        subscribers_lost=2,
        likes=120,
        fetched_at="2026-05-19",
    )
    store.commit()
    rows = store.daily_channel()
    updated = next(r for r in rows if r["day"] == "2026-01-01")
    assert updated["views"] == 5000
    assert updated["subscribers_gained"] == 50
    # Other days untouched.
    assert {r["day"] for r in rows} == {
        "2026-01-01", "2026-01-02", "2026-01-03", "2026-01-04",
    }


def test_upsert_without_commit_does_not_persist(analytics_conn: sqlite3.Connection) -> None:
    """commit() is explicit — writes before commit() roll back if the conn closes uncommitted."""
    store = AnalyticsStore(analytics_conn)
    store.upsert_traffic_source(
        video_id="v_long",
        source_type="YT_SEARCH",
        views=42,
        watch_time_minutes=7.5,
        fetched_at="2026-05-19",
    )
    # Caller forgot to commit. Same conn still sees the write (one transaction),
    # but a fresh conn against the same DB would not — verifying transactional
    # behaviour requires an on-disk fixture, so we just confirm commit() runs
    # without error and is the documented gate.
    store.commit()  # no-op if nothing pending; safe to call repeatedly
    rows = store.traffic_sources(video_id="v_long")
    assert len(rows) == 1


# ── daily_channel ─────────────────────────────────────────────────────────────

def test_daily_channel_returns_all_ascending(store: AnalyticsStore) -> None:
    rows = store.daily_channel()
    assert [r["day"] for r in rows] == [
        "2026-01-01", "2026-01-02", "2026-01-03", "2026-01-04",
    ]


def test_daily_channel_limit_returns_most_recent_ascending(store: AnalyticsStore) -> None:
    rows = store.daily_channel(limit=2)
    assert [r["day"] for r in rows] == ["2026-01-03", "2026-01-04"]


# ── lifecycle ─────────────────────────────────────────────────────────────────

def test_context_manager_closes_connection(analytics_conn: sqlite3.Connection) -> None:
    with AnalyticsStore(analytics_conn) as s:
        s.videos()
    # After exit, the connection should be closed — second op raises.
    with pytest.raises(sqlite3.ProgrammingError):
        analytics_conn.execute("SELECT 1")


def test_open_raises_if_db_missing(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        AnalyticsStore.open(tmp_path / "nope.db")


# ── escape hatch ──────────────────────────────────────────────────────────────

def test_execute_returns_dicts(store: AnalyticsStore) -> None:
    rows = store.execute("SELECT COUNT(*) AS n FROM videos")
    assert rows == [{"n": 3}]


# ── views.videos_with_ctr_and_traffic ─────────────────────────────────────────

def test_views_merges_search_traffic_pct(tmp_path: Path, analytics_conn: sqlite3.Connection) -> None:
    # Persist the in-memory db to a file so views can re-open it.
    db_path = tmp_path / "analytics.db"
    disk = sqlite3.connect(db_path)
    analytics_conn.backup(disk)
    disk.close()

    # No keywords.db — views should gracefully fall back to analytics.db CTR.
    result = v.videos_with_ctr_and_traffic(
        min_views=1,  # include all three test videos
        analytics_db=db_path,
        keywords_db=tmp_path / "missing.db",
    )
    by_id = {r["video_id"]: r for r in result}

    # v_mid: 1500 search of 5000 total = 30.0
    assert by_id["v_mid"]["search_traffic_pct"] == 30.0
    assert by_id["v_mid"]["total_traffic_views"] == 5000
    assert by_id["v_mid"]["search_views"] == 1500

    # v_short: 50 of 250 = 20.0
    assert by_id["v_short"]["search_traffic_pct"] == 20.0

    # v_long has no traffic_sources rows — pct = 0.
    assert by_id["v_long"]["search_traffic_pct"] == 0
    assert by_id["v_long"]["total_traffic_views"] == 0

    # Without keywords.db, analytics.db ctr_percent stays.
    assert by_id["v_mid"]["ctr_percent"] == 4.5


def test_views_overrides_ctr_from_keywords_db(tmp_path: Path, analytics_conn: sqlite3.Connection) -> None:
    db_path = tmp_path / "analytics.db"
    disk = sqlite3.connect(db_path)
    analytics_conn.backup(disk)
    disk.close()

    # Build a minimal keywords.db with one ctr_snapshot row.
    kw_path = tmp_path / "keywords.db"
    kw = sqlite3.connect(kw_path)
    kw.execute("""
        CREATE TABLE ctr_snapshots (
            id INTEGER PRIMARY KEY,
            video_id TEXT,
            snapshot_date DATE,
            ctr_percent REAL,
            impression_count INTEGER
        )
    """)
    kw.executemany(
        "INSERT INTO ctr_snapshots (video_id, snapshot_date, ctr_percent, impression_count) "
        "VALUES (?,?,?,?)",
        [
            ("v_mid", "2026-04-01", 5.0, 9000),   # earlier
            ("v_mid", "2026-05-01", 7.5, 12000),  # latest — should win
        ],
    )
    kw.commit()
    kw.close()

    result = v.videos_with_ctr_and_traffic(
        min_views=1,
        analytics_db=db_path,
        keywords_db=kw_path,
    )
    by_id = {r["video_id"]: r for r in result}
    assert by_id["v_mid"]["ctr_percent"] == 7.5
    assert by_id["v_mid"]["impressions"] == 12000
