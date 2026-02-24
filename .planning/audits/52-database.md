# Phase 52 Audit: Database Hardening

## 1. Database Files

| Database | Location | Schema Versioning | Tables |
|----------|----------|-------------------|--------|
| `keywords.db` | `tools/discovery/keywords.db` | PRAGMA user_version = 29 | 12+ tables |
| `intel.db` | `tools/intel/intel.db` | **None** | 5 tables |
| `analytics.db` | (created by technique_library.py) | PRAGMA user_version (partial) | 2 tables |

## 2. keywords.db Schema Management (GOOD — model to follow)

**File:** `tools/discovery/database.py` (2,927 lines)

### Version tracking:
```python
# Line 1443
cursor.execute("PRAGMA user_version")
version = cursor.fetchone()[0]

# Line 1461
cursor.execute(f"PRAGMA user_version = {version}")
```

### Migration methods (7 total):
| Method | From → To | What It Does |
|--------|-----------|-------------|
| `_ensure_lifecycle_table()` | v18+ | Creates lifecycle_history table |
| `_ensure_performance_tables()` | v19+ | Creates video_performance table |
| `_ensure_variant_tables()` | v20+ | Creates thumbnail_variants, title_variants, ctr_snapshots |
| `_ensure_feedback_tables()` | v21+ | Creates section_feedback table |
| `_ensure_script_choices_table()` | v28+ | Creates script_choices table |
| Various `ALTER TABLE` | Incremental | Adds columns to existing tables |

### Schema file: `tools/discovery/schema.sql`
- Contains full CREATE TABLE statements for all 12+ tables
- Used for fresh database creation
- Migrations handle upgrades from any version

### Transaction handling:
- **NOT consistently transaction-wrapped** — some _ensure_* methods use implicit autocommit
- No explicit rollback on failure
- `CREATE TABLE IF NOT EXISTS` is idempotent (safe to re-run)
- `ALTER TABLE ADD COLUMN` will fail if column exists (caught by try/except)

### Migration chain: Not strictly versioned — uses `IF NOT EXISTS` and `try/except` for idempotent operations rather than version-gated migrations.

## 3. intel.db Schema Management (NONE — needs work)

**File:** `tools/intel/kb_store.py`

### Table creation:
```python
# Lines 26-78 — all created in __init__
CREATE TABLE IF NOT EXISTS algo_snapshots (...)
CREATE TABLE IF NOT EXISTS competitor_channels (...)
CREATE TABLE IF NOT EXISTS competitor_videos (...)
CREATE TABLE IF NOT EXISTS niche_snapshots (...)
CREATE TABLE IF NOT EXISTS kb_meta (...)
```

### Issues:
- **No PRAGMA user_version** — no schema tracking at all
- **No migration path** — if a column needs adding, there's no mechanism
- Tables created on every connection via `IF NOT EXISTS`
- No schema.sql reference file
- kb_meta table stores key-value metadata but not schema version

### Current tables (5):
1. `algo_snapshots` — algorithm knowledge snapshots
2. `competitor_channels` — channel IDs, names, subscriber counts
3. `competitor_videos` — video metadata from competitors
4. `niche_snapshots` — niche pattern snapshots
5. `kb_meta` — key-value metadata store

## 4. analytics.db Schema Management (PARTIAL)

**File:** `tools/youtube-analytics/technique_library.py`

### Version tracking (exists but limited):
```python
# Line 60-73
def _get_schema_version(self):
    cursor.execute("PRAGMA user_version")
    return cursor.fetchone()[0]

def _set_schema_version(self, version):
    cursor.execute(f"PRAGMA user_version = {version}")
```

### Tables (2):
1. `creator_techniques` — extracted creator patterns (line 96)
2. `script_choices` — user hook/structure choices (line 150)

### Migration:
- Has `_migrate_schema()` method
- Version 1 → 2 migration exists (adds script_choices table)
- Currently at version 2
- **Migrations ARE transaction-wrapped** (good model)

## 5. Migration Risks

### Risk 1: keywords.db ALTER TABLE failures
- `ALTER TABLE ADD COLUMN` with try/except Exception — if it fails for a reason OTHER than "column already exists", the error is swallowed
- **Fix:** Check specific error message or use `PRAGMA table_info` to verify column exists first

### Risk 2: intel.db has no upgrade path
- If we add a column to competitor_channels, existing databases won't get it
- `CREATE TABLE IF NOT EXISTS` won't add new columns to existing tables
- **Fix:** Add PRAGMA user_version + migration functions

### Risk 3: Non-atomic migrations in keywords.db
- Multiple `_ensure_*` methods run independently
- If one fails mid-way, database is in partial state
- **Fix:** Wrap all migrations in a single transaction per version bump

### Risk 4: Missing indexes
- keywords.db has indexes defined in schema.sql
- intel.db has no explicit indexes (relies on PRIMARY KEY only)
- **Fix:** Add indexes for common query patterns (competitor_videos.channel_id, algo_snapshots.topic)

## 6. Proposed Schema Versioning Pattern

Apply the technique_library.py pattern (best current example) to all three databases:

```python
def _migrate_schema(self):
    version = self._get_schema_version()

    if version < 1:
        with self.conn:  # Transaction
            # Create all initial tables
            self.conn.executescript(SCHEMA_SQL)
            self._set_schema_version(1)

    if version < 2:
        with self.conn:  # Transaction
            self.conn.execute("ALTER TABLE ...")
            self._set_schema_version(2)
```

### Target versions:
- keywords.db: Set to 29 (current, document existing migrations)
- intel.db: Set to 1 (initial schema), then increment as needed
- analytics.db: Already at 2 (continue from there)

## Summary

| Database | Has Versioning | Has Migrations | Atomic Transactions | Action |
|----------|---------------|----------------|--------------------|----|
| keywords.db | Yes (v29) | Yes (7 methods) | No | Wrap in transactions |
| intel.db | **No** | **No** | N/A | Add versioning + migrations |
| analytics.db | Yes (v2) | Yes (1 migration) | **Yes** | Model for others |
