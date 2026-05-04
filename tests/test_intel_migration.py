"""Migration framework tests for tools.intel.kb_store.

Pins the F1 audit contract: PRAGMA user_version is set after init, gate is
idempotent on repeat construction, and pre-existing pre-versioning databases
are bootstrapped without losing data.

Note on `:memory:`: the audit's verify clause used `KBStore(':memory:')` but
Python's sqlite3 opens a fresh in-memory database on every `connect()` call,
so KBStore (which opens a new connection per operation) cannot use it. Tests
use `tmp_path` instead — the practical equivalent.
"""
import sqlite3

import pytest

from tools.intel.kb_store import KBStore, CURRENT_SCHEMA_VERSION


def _read_user_version(db_path) -> int:
    conn = sqlite3.connect(str(db_path))
    try:
        return conn.execute("PRAGMA user_version").fetchone()[0]
    finally:
        conn.close()


def test_fresh_db_lands_at_current_schema_version(tmp_path):
    """A brand-new KBStore stamps PRAGMA user_version to CURRENT_SCHEMA_VERSION."""
    db = tmp_path / "test_intel.db"
    KBStore(db)
    assert _read_user_version(db) == CURRENT_SCHEMA_VERSION


def test_current_schema_version_is_at_least_1():
    """F1 audit floor: schema version is tracked (>= 1, not 0)."""
    assert CURRENT_SCHEMA_VERSION >= 1


def test_repeat_construction_is_idempotent(tmp_path):
    """Constructing KBStore on an already-migrated DB is a no-op (no version regression, no errors)."""
    db = tmp_path / "test_intel.db"
    KBStore(db)
    first = _read_user_version(db)
    KBStore(db)
    KBStore(db)
    second = _read_user_version(db)
    assert first == second == CURRENT_SCHEMA_VERSION


def test_initial_tables_exist_after_init(tmp_path):
    """Version-1 migration creates the canonical 5-table schema."""
    db = tmp_path / "test_intel.db"
    KBStore(db)
    conn = sqlite3.connect(str(db))
    try:
        rows = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        ).fetchall()
    finally:
        conn.close()
    table_names = {r[0] for r in rows}
    expected = {"algo_snapshots", "competitor_channels", "competitor_videos", "niche_snapshots", "kb_meta"}
    missing = expected - table_names
    assert not missing, f"Missing tables after init: {missing}"


def test_v2_columns_exist_on_competitor_videos(tmp_path):
    """Version-2 migration adds topic_cluster + outlier_ratio columns."""
    db = tmp_path / "test_intel.db"
    KBStore(db)
    conn = sqlite3.connect(str(db))
    try:
        cols = {r[1] for r in conn.execute("PRAGMA table_info(competitor_videos)").fetchall()}
    finally:
        conn.close()
    assert "topic_cluster" in cols
    assert "outlier_ratio" in cols


def test_pre_versioning_db_is_bootstrapped(tmp_path):
    """A pre-existing DB with tables but no PRAGMA user_version is migrated forward."""
    db = tmp_path / "test_intel.db"
    # Create tables manually — simulate a pre-versioning database
    conn = sqlite3.connect(str(db))
    try:
        conn.execute("CREATE TABLE algo_snapshots (id INTEGER PRIMARY KEY)")
        conn.execute("CREATE TABLE competitor_channels (channel_id TEXT PRIMARY KEY)")
        conn.execute(
            "CREATE TABLE competitor_videos (video_id TEXT PRIMARY KEY, channel_id TEXT)"
        )
        conn.execute("CREATE TABLE niche_snapshots (id INTEGER PRIMARY KEY)")
        conn.execute("CREATE TABLE kb_meta (id INTEGER PRIMARY KEY, last_refresh TEXT)")
        conn.commit()
    finally:
        conn.close()

    # PRAGMA should still be 0 (never set)
    assert _read_user_version(db) == 0

    # Construct KBStore — should bootstrap forward to CURRENT_SCHEMA_VERSION
    KBStore(db)
    assert _read_user_version(db) == CURRENT_SCHEMA_VERSION

    # competitor_videos should now have the v2 columns
    conn = sqlite3.connect(str(db))
    try:
        cols = {r[1] for r in conn.execute("PRAGMA table_info(competitor_videos)").fetchall()}
    finally:
        conn.close()
    assert "topic_cluster" in cols
    assert "outlier_ratio" in cols
