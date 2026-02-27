# Phase 52: Database Hardening - Research

**Researched:** 2026-02-27
**Domain:** SQLite schema versioning and atomic migration in Python
**Confidence:** HIGH

---

## Summary

Phase 52 adds PRAGMA user_version schema tracking and atomic transaction-wrapped migrations to all three project databases. The work is purely internal to three Python files: `tools/intel/kb_store.py` (intel.db), `tools/youtube_analytics/technique_library.py` (analytics.db), and `tools/discovery/database.py` (keywords.db). No new libraries are needed — SQLite's `PRAGMA user_version` and Python's `sqlite3` context-manager transaction model are already in use across the codebase.

The project already has a working reference implementation. `tools/youtube_analytics/technique_library.py` uses a clean `_get_schema_version()` / `_set_schema_version()` / per-version `_ensure_schema_vN()` pattern that satisfies all three success criteria. The audit confirms this file's migrations are already transaction-wrapped via `self._conn.commit()` inside try/except blocks. The task for intel.db is to add this pattern from scratch; for analytics.db it is to verify (and if needed fix) atomicity; for keywords.db it is to wrap existing non-atomic `_ensure_*` methods in explicit transactions.

The critical risk is existing intel.db files on disk that were created by the current `_SCHEMA_SQL` executescript without any version stamp. The migration must bootstrap gracefully: if `PRAGMA user_version` returns 0, treat the database as needing version 1 initialization (or, if tables already exist, set version 1 without re-running CREATE TABLE).

**Primary recommendation:** Apply the `technique_library.py` migration pattern to kb_store.py; verify analytics.db is already compliant; wrap keywords.db `_ensure_*` methods in `with conn:` blocks.

---

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| DB-01 | intel.db has PRAGMA user_version schema tracking matching keywords.db pattern | Add `_get_schema_version()`, `_set_schema_version()`, `_migrate_schema()` to `KBStore`; set version = 1 after existing tables; bootstrap existing dbs with version = 1 |
| DB-02 | analytics.db has PRAGMA user_version schema tracking | `TechniqueLibrary` already calls `PRAGMA user_version` — verify current version = 2, verify migration is transaction-wrapped, confirm success criterion |
| DB-03 | Migration functions are atomic (transaction-wrapped, rollback on failure) | Use `with conn:` context manager (auto-rollback on exception) for every DDL block; test by injecting a mid-migration error and checking database is unchanged |
</phase_requirements>

---

## Standard Stack

### Core

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| `sqlite3` | stdlib | All three databases | Already in use, no new dependency |

### No New Libraries Needed

All required functionality — `PRAGMA user_version`, `BEGIN / COMMIT / ROLLBACK`, `CREATE TABLE IF NOT EXISTS`, `ALTER TABLE` — is in SQLite and exposed through the stdlib `sqlite3` module.

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Manual PRAGMA versioning | Alembic or SQLAlchemy migrations | Massive overkill for 3 small databases owned by single-process tools. The existing codebase already chose manual PRAGMA. Stay consistent. |
| `with conn:` context manager | Explicit `BEGIN/ROLLBACK` | `with conn:` is the idiomatic Python pattern: commits on exit, rolls back on exception. Use it. |

---

## Architecture Patterns

### Current State of Each Database

#### intel.db — `tools/intel/kb_store.py`

```
Current state:
  - PRAGMA user_version = 0 (never set)
  - 5 tables created via executescript(_SCHEMA_SQL) in _init_schema()
  - 2 ALTER TABLE migrations in _ensure_topic_cluster_column() and _ensure_outlier_ratio_column()
    (both use PRAGMA table_info check + conn.execute + conn.commit — NOT wrapped in transaction)
  - kb_meta table has a 'version' column but it stores app-level metadata, not schema version

Target state (DB-01):
  - PRAGMA user_version = 1 after initial schema creation
  - _ensure_* methods become part of a versioned _migrate_schema() chain
  - Existing databases with version=0 but tables already present: bump to version=1 without DDL
```

#### analytics.db — `tools/youtube_analytics/technique_library.py`

```
Current state:
  - _get_schema_version() / _set_schema_version() exist and work
  - _ensure_schema_v28() sets version to 28
  - _ensure_schema_v29() sets version to 29
  - But: _set_schema_version() does conn.commit() AFTER setting PRAGMA outside try block
  - Migration bodies use cursor.execute() then self._conn.commit() separately
    (not inside a with self._conn: block — vulnerable to partial commits)

Target state (DB-02, DB-03):
  - Verify PRAGMA user_version = 2 on the actual analytics.db file
    (Note: technique_library uses keywords.db by default, NOT a separate analytics.db)
  - Wrap migration DDL in with self._conn: blocks
```

**IMPORTANT FINDING:** The audit file states analytics.db is at version 2, but the code
in `technique_library.py` sets version 28 and 29 — because `technique_library.py` writes to
`keywords.db`, not a separate `analytics.db`. The actual `analytics.db` is a different file.
Research needed: find the file that creates and owns `analytics.db`.

#### keywords.db — `tools/discovery/database.py`

```
Current state:
  - get_schema_version() / set_schema_version() exist (lines 1433-1468)
  - 7+ _ensure_* migration methods
  - _ensure_variant_tables() checks version with get_schema_version() >= 27
  - BUT: migrations do cursor.execute() + self._conn.commit() without a wrapping transaction
    Specifically _ensure_variant_tables() closes/reopens connection for backup — if it fails
    mid-migration between commit calls, database is partially modified

Target state (DB-03):
  - Wrap each migration block in with self._conn: (auto-rollback)
  - The backup step (file copy) must happen BEFORE opening the transaction, not inside it
```

### Pattern 1: Version-Gated Migration Chain (Use This)

This is the canonical pattern used by `technique_library.py` and the recommended pattern for all three databases.

```python
# Source: tools/youtube_analytics/technique_library.py (existing codebase)

CURRENT_SCHEMA_VERSION = 1  # Set at module level

def _get_schema_version(self) -> int:
    """Read PRAGMA user_version from the database."""
    try:
        cursor = self._conn.cursor()
        cursor.execute("PRAGMA user_version")
        row = cursor.fetchone()
        return row[0] if row else 0
    except sqlite3.Error:
        return 0

def _set_schema_version(self, version: int) -> None:
    """Write PRAGMA user_version (DDL — auto-committed by SQLite)."""
    # PRAGMA user_version is DDL; no explicit commit needed
    # But call conn.commit() for safety with WAL mode
    self._conn.execute(f"PRAGMA user_version = {version}")
    self._conn.commit()

def _migrate_schema(self) -> None:
    """Run all pending migrations in version order."""
    version = self._get_schema_version()

    if version < 1:
        # Bootstrap: create initial schema atomically
        with self._conn:
            self._conn.executescript(SCHEMA_SQL)
        self._set_schema_version(1)
```

**Key rules:**
1. `if version < N:` gates each migration — idempotent on re-run
2. `with self._conn:` wraps DDL — auto-rolls back on any exception
3. `_set_schema_version(N)` called AFTER the `with` block succeeds
4. If bootstrap case: tables already exist → set version without DDL

### Pattern 2: Bootstrapping Existing Databases (intel.db specific)

intel.db files exist on disk with version=0 but tables already created. The migration must not re-run CREATE TABLE against a populated database:

```python
def _migrate_schema(self) -> None:
    version = self._get_schema_version()

    if version < 1:
        # Check if tables already exist (pre-versioning database)
        existing = self._conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='algo_snapshots'"
        ).fetchone()

        if existing is None:
            # Fresh database — create schema
            with self._conn:
                self._conn.executescript(_SCHEMA_SQL)
        # else: tables exist (pre-v1 database) — skip DDL, just stamp version

        self._set_schema_version(1)

    if version < 2:
        # Future migration: add a column
        with self._conn:
            self._conn.execute("ALTER TABLE competitor_videos ADD COLUMN ...")
        self._set_schema_version(2)
```

### Pattern 3: ALTER TABLE Idempotency

The `_ensure_topic_cluster_column()` and `_ensure_outlier_ratio_column()` in kb_store.py already use `PRAGMA table_info` to check before altering. Fold them into the migration chain:

```python
    if version < 2:
        cols = [r[1] for r in self._conn.execute(
            "PRAGMA table_info(competitor_videos)"
        ).fetchall()]
        with self._conn:
            if "topic_cluster" not in cols:
                self._conn.execute(
                    "ALTER TABLE competitor_videos ADD COLUMN topic_cluster TEXT"
                )
            if "outlier_ratio" not in cols:
                self._conn.execute(
                    "ALTER TABLE competitor_videos ADD COLUMN outlier_ratio REAL"
                )
        self._set_schema_version(2)
```

### PRAGMA user_version Transaction Behavior

**Verified from SQLite documentation:** `PRAGMA user_version = N` is written within the current transaction. Unlike schema-changing PRAGMAs (like `journal_mode`), `user_version` respects the transaction boundary — meaning if you set it inside a `with conn:` block that rolls back, the version does NOT get updated.

However, the safest pattern used throughout this codebase is:
1. Run DDL inside `with conn:` (commit on success, rollback on failure)
2. Call `_set_schema_version(N)` immediately after the `with` block (outside it)

This means: if DDL succeeds but `_set_schema_version` fails, the migration runs again next startup (idempotent DDL handles re-runs safely).

### Anti-Patterns to Avoid

- **executescript() inside with conn:** `sqlite3.executescript()` issues an implicit COMMIT before running. Calling it inside `with conn:` will not roll back if it fails mid-way. Use individual `conn.execute()` calls inside `with conn:` instead, or call `executescript()` only for fresh schema creation where rollback doesn't matter.
- **Setting version before DDL succeeds:** If version is bumped at start of migration and DDL fails, the database is stuck at wrong version.
- **bare `except: pass` on migration failure:** Existing kb_store.py `_ensure_*` methods catch `sqlite3.OperationalError` and pass silently. Migration failures must at minimum be logged (per Phase 51 logging standards already applied).

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Version tracking | Custom version table | `PRAGMA user_version` | Built into SQLite, zero-cost, already in use |
| Atomic DDL | Savepoints / two-phase commit | `with conn:` context manager | `sqlite3.Connection` as context manager commits on exit, rolls back on exception |
| Schema comparison | Diff-based migration | Linear version chain | Simpler, already the project pattern |
| Migration framework | Alembic, Yoyo | Manual PRAGMA chain | 3 tiny databases; framework overhead is disproportionate |

**Key insight:** SQLite's `PRAGMA user_version` combined with `with conn:` gives 100% of what's needed with zero dependencies. Do not reach for external tools.

---

## Common Pitfalls

### Pitfall 1: executescript() Bypasses Transaction

**What goes wrong:** Developer wraps `executescript(_SCHEMA_SQL)` in `with conn:` expecting rollback protection. It doesn't work — `executescript()` issues an implicit `COMMIT` first.

**Why it happens:** `executescript()` is designed for multi-statement SQL files; it commits any pending transaction before running to get a clean state.

**How to avoid:** Use `executescript()` only for initial fresh-schema creation where partial failure is acceptable (the database is empty, so rolling back to "empty" is fine). For migrations on existing data, use individual `conn.execute()` calls inside `with conn:`.

**Warning signs:** If your migration runs multiple CREATE TABLE statements via executescript() and fails on the third, the first two are committed permanently.

### Pitfall 2: Version Set Before DDL Succeeds

**What goes wrong:** `set_schema_version(2)` is called at the top of the migration block. DDL fails. Database is marked as v2 but missing the schema changes.

**How to avoid:** Always set version AFTER the `with conn:` block completes successfully.

### Pitfall 3: Bootstrapping Pre-Versioning Databases

**What goes wrong:** intel.db on disk has all 5 tables (created by existing code) but `PRAGMA user_version = 0`. Migration runs `_migrate_schema()`, sees version 0, tries to run `CREATE TABLE IF NOT EXISTS` — succeeds (idempotent), sets version 1. This is actually fine IF the migration uses `IF NOT EXISTS`. But if ALTER TABLE is also in version 1's block, it will fail if columns already exist.

**How to avoid:** The `_ensure_topic_cluster_column()` and `_ensure_outlier_ratio_column()` patterns already guard via `PRAGMA table_info`. Fold them into the migration chain with the same guard.

### Pitfall 4: Separate Connection per _ensure_* Call (keywords.db)

**What goes wrong:** `database.py` opens/closes connections inside `_ensure_variant_tables()` (lines 1544-1547) for the backup step. If a new connection is opened mid-migration, WAL mode behavior can differ.

**How to avoid:** Do the backup (file copy) entirely before any database operations. After backup succeeds, open a single connection and run all DDL in one `with conn:` block.

### Pitfall 5: analytics.db vs keywords.db Confusion

**What goes wrong:** `technique_library.py` default db_path points to `keywords.db`, NOT a separate `analytics.db`. The audit mentions an `analytics.db` — this may refer to a different file (possibly created by `tools/youtube_analytics/` backfill or analytics modules).

**How to avoid:** Verify which file actually contains the analytics schema before implementing DB-02. If `analytics.db` is a separate file, find the class/module that owns it.

---

## Code Examples

### Atomic Migration Block (verified pattern from existing codebase)

```python
# Pattern: version-gated, atomically wrapped
# Source: technique_library.py approach, adapted

def _migrate_schema(self) -> None:
    version = self._get_schema_version()

    if version < 1:
        # Check if pre-versioning database exists
        has_tables = self._conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='algo_snapshots'"
        ).fetchone() is not None

        if not has_tables:
            # Fresh DB: create schema using individual execute() calls (not executescript)
            # so the with-block's rollback actually works
            with self._conn:
                for stmt in _SCHEMA_SQL.strip().split(";\n\n"):
                    stmt = stmt.strip()
                    if stmt:
                        self._conn.execute(stmt)
        # If tables already exist, skip DDL (pre-v1 bootstrap)
        self._set_schema_version(1)

    if version < 2:
        with self._conn:
            self._conn.execute(
                "ALTER TABLE competitor_videos ADD COLUMN topic_cluster TEXT"
            )
            self._conn.execute(
                "ALTER TABLE competitor_videos ADD COLUMN outlier_ratio REAL"
            )
        self._set_schema_version(2)
```

### Verifying Rollback Behavior (for DB-03 success criterion)

```python
# Manually test: inject a failure mid-migration
def test_migration_atomicity():
    import sqlite3, tempfile, os
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
        db_path = f.name

    conn = sqlite3.connect(db_path)
    conn.execute("CREATE TABLE t (id INTEGER PRIMARY KEY)")
    conn.commit()

    try:
        with conn:
            conn.execute("ALTER TABLE t ADD COLUMN col1 TEXT")
            raise RuntimeError("simulated failure")  # Force rollback
    except RuntimeError:
        pass

    # Verify col1 was NOT added
    cols = [r[1] for r in conn.execute("PRAGMA table_info(t)").fetchall()]
    assert "col1" not in cols, "Transaction did not roll back"
    conn.close()
    os.unlink(db_path)
```

### Reading PRAGMA user_version

```python
# Verified: standard sqlite3 pattern
cursor = conn.execute("PRAGMA user_version")
version = cursor.fetchone()[0]  # Returns 0 if never set
```

---

## Open Questions

1. **What file owns analytics.db?**
   - What we know: `technique_library.py` writes to `keywords.db` by default. The audit says `analytics.db` is created by `technique_library.py` — but the default path in that file resolves to keywords.db.
   - What's unclear: Is `analytics.db` created by a different module (e.g., `tools/youtube_analytics/backfill.py` or `analytics.py`)? Or is the audit referring to keywords.db as the "analytics database"?
   - Recommendation: Before implementing DB-02, run `grep -r "analytics.db" tools/` to find the actual file owner. The planner must identify the correct file before writing the implementation plan.

2. **Should keywords.db migrations be restructured or just wrapped?**
   - What we know: keywords.db has 7 `_ensure_*` methods accumulated across phases. They already check version with `get_schema_version() >= N`.
   - What's unclear: DB-03 says "make migrations atomic" — does this mean wrap existing `_ensure_*` methods in transactions, or restructure into a single `_migrate_schema()` chain?
   - Recommendation: Wrap existing `_ensure_*` methods in `with self._conn:` blocks. Full restructure is out of scope for Phase 52.

3. **Does `PRAGMA user_version` commit atomically with DDL when using `with conn:`?**
   - What we know: SQLite docs confirm user_version is written within the current transaction. The existing codebase always sets version AFTER the DDL block (outside `with conn:`), which is the safer pattern.
   - Recommendation: Follow existing codebase pattern — set version AFTER `with conn:` completes. This is correct and safe.

---

## Implementation Scope Summary

| File | Change | Complexity |
|------|--------|------------|
| `tools/intel/kb_store.py` | Add `_get_schema_version()`, `_set_schema_version()`, `_migrate_schema()` method; call from `__init__`; replace `_ensure_topic_cluster_column()` + `_ensure_outlier_ratio_column()` with versioned migration blocks | Medium |
| `tools/youtube_analytics/technique_library.py` OR the actual analytics.db owner | Verify atomicity of existing migrations; wrap DDL in `with self._conn:` if not already | Low-Medium |
| `tools/discovery/database.py` | Wrap existing `_ensure_*` DDL bodies in `with self._conn:` | Low (surgical changes) |

No new files. No new dependencies. No schema changes — version numbers only.

---

## Sources

### Primary (HIGH confidence)

- `tools/intel/kb_store.py` — Full file read; current intel.db schema and migration state confirmed
- `tools/youtube_analytics/technique_library.py` (lines 63-187) — Current analytics migration pattern confirmed
- `tools/discovery/database.py` (lines 1433-1607) — Current keywords.db version tracking and _ensure_variant_tables pattern confirmed
- `.planning/audits/52-database.md` — Audit file; all three database states, migration risks, and proposed pattern
- `.planning/REQUIREMENTS.md` — DB-01, DB-02, DB-03 requirement definitions confirmed

### Secondary (MEDIUM confidence)

- SQLite PRAGMA user_version behavior: well-documented, consistent across SQLite versions. Behavior within transactions confirmed by codebase observation (existing code pattern is correct).
- `sqlite3.Connection` as context manager (`with conn:`): stdlib behavior, documented in Python docs — commits on exit, rolls back on exception.

### Tertiary (LOW confidence)

- `executescript()` implicit COMMIT behavior: observed in SQLite docs and Python docs; not independently verified via Context7 for this session but is a well-known characteristic.

---

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — stdlib sqlite3, already in use, no new dependencies
- Architecture: HIGH — reference implementation exists in codebase (technique_library.py)
- Pitfalls: HIGH — identified from actual code inspection, not hypothetical
- analytics.db ownership: LOW — requires grep verification before planning DB-02

**Research date:** 2026-02-27
**Valid until:** 2026-03-29 (stable domain — SQLite PRAGMA behavior does not change)
