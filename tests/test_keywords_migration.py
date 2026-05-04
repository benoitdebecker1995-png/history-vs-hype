"""Migration regression tests for tools.discovery.database (KeywordDB).

Pins the F2 audit contract: every `_ensure_*` migration runs to completion
on a fresh DB, the expected tables exist, and repeat construction is
idempotent. Each `_ensure_*` body is wrapped in `with self._conn:` so a
partial failure rolls back rather than leaving the DB in a half-migrated state.
"""
import sqlite3

import pytest

from tools.discovery.database import KeywordDB


EXPECTED_TABLES = {
    # Created during init_database() from schema.sql
    "keywords",
    "keyword_intents",
    "keyword_performance",
    "trends",
    "competitor_videos",
    "competitor_channels",
    "opportunity_scores",
    # Created by _ensure_lifecycle_columns
    "lifecycle_history",
    # Created by _ensure_performance_table
    "video_performance",
    # Created by _ensure_variant_tables
    "thumbnail_variants",
    "title_variants",
    # Created by _ensure_ctr_snapshots_table
    "ctr_snapshots",
    # Created by _ensure_feedback_tables
    "section_feedback",
}


def _fetch_tables(db_path) -> set[str]:
    conn = sqlite3.connect(str(db_path))
    try:
        rows = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        ).fetchall()
    finally:
        conn.close()
    return {r[0] for r in rows}


def test_fresh_db_creates_all_expected_tables(tmp_path):
    """Every audit-listed table exists after KeywordDB construction (subset of EXPECTED)."""
    db = tmp_path / "test_keywords.db"
    KeywordDB(db_path=str(db))
    tables = _fetch_tables(db)
    missing = EXPECTED_TABLES - tables
    assert not missing, f"Missing tables after init: {missing}"


def test_audit_required_tables_subset_present(tmp_path):
    """The specific audit-mentioned tables are present (lifecycle_history, video_performance, thumbnail/title variants, ctr_snapshots, section_feedback)."""
    db = tmp_path / "test_keywords.db"
    KeywordDB(db_path=str(db))
    tables = _fetch_tables(db)
    audit_required = {
        "lifecycle_history",
        "video_performance",
        "thumbnail_variants",
        "title_variants",
        "ctr_snapshots",
        "section_feedback",
    }
    missing = audit_required - tables
    assert not missing, f"Audit-required tables missing: {missing}"


def test_repeat_construction_is_idempotent(tmp_path):
    """Constructing KeywordDB on an already-migrated DB doesn't error or duplicate tables."""
    db = tmp_path / "test_keywords.db"
    KeywordDB(db_path=str(db))
    first = _fetch_tables(db)
    KeywordDB(db_path=str(db))
    KeywordDB(db_path=str(db))
    second = _fetch_tables(db)
    assert first == second


def test_classification_columns_added_on_competitor_videos(tmp_path):
    """_ensure_classification_columns adds format / angles / quality_tier / classified_at."""
    db = tmp_path / "test_keywords.db"
    KeywordDB(db_path=str(db))
    conn = sqlite3.connect(str(db))
    try:
        cols = {r[1] for r in conn.execute("PRAGMA table_info(competitor_videos)").fetchall()}
    finally:
        conn.close()
    for col in ("format", "angles", "quality_tier", "classified_at"):
        assert col in cols, f"Expected column '{col}' missing from competitor_videos"


def test_lifecycle_columns_added_on_keywords(tmp_path):
    """_ensure_lifecycle_columns adds lifecycle_state / lifecycle_updated_at / opportunity_*."""
    db = tmp_path / "test_keywords.db"
    KeywordDB(db_path=str(db))
    conn = sqlite3.connect(str(db))
    try:
        cols = {r[1] for r in conn.execute("PRAGMA table_info(keywords)").fetchall()}
    finally:
        conn.close()
    for col in ("lifecycle_state", "lifecycle_updated_at", "opportunity_score_final", "opportunity_category"):
        assert col in cols, f"Expected column '{col}' missing from keywords"


def test_production_columns_added_on_keywords(tmp_path):
    """_ensure_production_columns adds production_constraints / constraint_checked_at / is_production_blocked."""
    db = tmp_path / "test_keywords.db"
    KeywordDB(db_path=str(db))
    conn = sqlite3.connect(str(db))
    try:
        cols = {r[1] for r in conn.execute("PRAGMA table_info(keywords)").fetchall()}
    finally:
        conn.close()
    for col in ("production_constraints", "constraint_checked_at", "is_production_blocked"):
        assert col in cols, f"Expected column '{col}' missing from keywords"
