---
phase: 52-database-hardening
plan: 01
subsystem: database
tags: [sqlite, pragma, user_version, migration, intel-db, kb_store]

# Dependency graph
requires:
  - phase: 48-package-structure
    provides: absolute tools.* imports (tools.logging_config available)
  - phase: 51-logging-cli-standardization
    provides: get_logger pattern established across all tools
provides:
  - PRAGMA user_version schema tracking on intel.db
  - Atomic migration chain in KBStore._migrate_schema()
  - Graceful bootstrap for pre-versioning intel.db files (version 0 -> 2)
  - True DDL rollback via autocommit=False migration connections
affects: [53-integration-testing, tools/intel/kb_store.py consumers]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "PRAGMA user_version version-gated migration chain (matches keywords.db pattern)"
    - "autocommit=False connections for migration DDL to ensure true transaction rollback"
    - "Individual conn.execute() calls inside with conn: blocks (not executescript) for rollback support"
    - "Version stamped AFTER DDL block succeeds (never inside with conn: block)"

key-files:
  created: []
  modified:
    - tools/intel/kb_store.py

key-decisions:
  - "autocommit=False required for Python 3.12+ sqlite3 DDL rollback — default isolation_level='' does not roll back ALTER TABLE via 'with conn:'"
  - "Migration connections use autocommit=False; public method connections retain default behavior (explicit conn.commit() per operation)"
  - "CURRENT_SCHEMA_VERSION = 2 module constant for future migration additions"
  - "Pre-versioning db bootstrap: check table existence first, skip DDL if tables exist, stamp version 1 unconditionally"

patterns-established:
  - "Migration pattern: version-gated if version < N: blocks with autocommit=False connection and with conn: for atomic DDL"
  - "Version stamp: _set_schema_version(N) called outside and after with conn: block"

requirements-completed: [DB-01, DB-03]

# Metrics
duration: 5min
completed: 2026-02-28
---

# Phase 52 Plan 01: Database Hardening (intel.db) Summary

**PRAGMA user_version migration chain added to KBStore replacing three ad-hoc _ensure_* methods with a unified atomic _migrate_schema() that bootstraps existing databases from version 0 to version 2**

## Performance

- **Duration:** 5 min
- **Started:** 2026-02-28T11:52:32Z
- **Completed:** 2026-02-28T11:56:47Z
- **Tasks:** 2
- **Files modified:** 1

## Accomplishments

- Added CURRENT_SCHEMA_VERSION = 2 module constant and three new methods: _get_schema_version(), _set_schema_version(), _migrate_schema()
- Replaced _init_schema() + _ensure_topic_cluster_column() + _ensure_outlier_ratio_column() with unified versioned migration chain
- Confirmed and fixed DDL rollback: Python 3.12+ sqlite3 requires autocommit=False for true ALTER TABLE rollback via `with conn:`
- Production intel.db bootstrapped to user_version=2 with all columns present

## Task Commits

Each task was committed atomically:

1. **Task 1: Add versioned migration chain to KBStore** - `fc189dc` (feat)
2. **Task 2: Verify rollback atomicity — fix autocommit=False** - `2f9fe8f` (fix)

**Plan metadata:** `[pending]` (docs: complete plan)

## Files Created/Modified

- `tools/intel/kb_store.py` - Added CURRENT_SCHEMA_VERSION constant, _get_schema_version(), _set_schema_version(), _migrate_schema() methods; removed _init_schema(), _ensure_topic_cluster_column(), _ensure_outlier_ratio_column(); added get_logger import

## Decisions Made

- Used autocommit=False for migration-specific connections rather than changing the global _connect() method — keeps public method behavior unchanged while enabling true DDL rollback
- Python 3.14.2 on this system; autocommit=False is available (Python 3.12+ feature, confirmed present)
- Pre-versioning bootstrap: check `sqlite_master` for existing tables, skip CREATE TABLE DDL if present, always stamp version 1 — prevents duplicate table errors on existing databases

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Fixed DDL rollback by using autocommit=False migration connections**
- **Found during:** Task 2 (Verify rollback atomicity)
- **Issue:** Python's default `isolation_level=''` does NOT roll back ALTER TABLE via `with conn:` in Python 3.12+. DDL is auto-committed before the transaction boundary takes effect. The plan specified `with conn:` blocks would provide rollback, which was correct conceptually but required `autocommit=False` to actually work.
- **Fix:** Changed both migration connections (v<1 and v<2 gates) from `self._connect()` to `sqlite3.connect(str(self.db_path), autocommit=False)` with `row_factory` set explicitly
- **Files modified:** tools/intel/kb_store.py
- **Verification:** Atomicity test confirms topic_cluster not committed after simulated mid-migration RuntimeError; PRAGMA user_version remains at 1
- **Committed in:** 2f9fe8f (Task 2 commit)

---

**Total deviations:** 1 auto-fixed (1 bug)
**Impact on plan:** Essential correctness fix. Without autocommit=False, the rollback guarantee in the plan's success criteria would not hold on Python 3.12+.

## Issues Encountered

- SQL splitting via `";\n"` kept leading comment lines with each CREATE TABLE statement. Initial filter `not stmt.startswith("--")` skipped entire statements when they led with comments. Fixed by stripping comment lines from each statement while preserving the SQL body (Task 1, auto-fixed inline before commit).

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- DB-01 and DB-03 satisfied for intel.db
- DB-02 (analytics.db) is addressed in plan 52-02
- Pattern established: autocommit=False migration connections + with conn: DDL blocks for all future migration work

---
*Phase: 52-database-hardening*
*Completed: 2026-02-28*
