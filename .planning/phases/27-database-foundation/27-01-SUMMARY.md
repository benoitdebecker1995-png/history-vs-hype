---
phase: 27-database-foundation
plan: 01
subsystem: database
tags: [sqlite, schema-migration, imagehash, textstat, variant-tracking, ctr-analysis, feedback-storage]

# Dependency graph
requires:
  - phase: 19-learning-loop
    provides: video_performance table with conversion tracking
provides:
  - Phase 27 schema migration with 4 new tables (thumbnail_variants, title_variants, ctr_snapshots, section_feedback)
  - Schema version tracking via PRAGMA user_version
  - Automatic database backup before migration
  - 3 new feedback columns on video_performance table
affects: [28-pacing-analysis, 29-thumbnail-title-tracking, 30-ctr-analysis, 31-feedback-loop]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Auto-migration pattern with schema version guard"
    - "Backup-before-migrate pattern with timestamped filenames"
    - "Zero-breaking-change migration via _ensure_*() methods"

key-files:
  created: []
  modified:
    - tools/discovery/database.py
    - tools/discovery/schema.sql

key-decisions:
  - "Use PRAGMA user_version for schema version tracking (SQLite-native, atomic)"
  - "Create backup before migration to prevent data loss"
  - "Migration guard checks schema version before running (prevents duplicate migrations)"
  - "Wire migration into _ensure_connection() for automatic execution on first access"

patterns-established:
  - "Migration method pattern: check version → backup → create tables → set version"
  - "Backup inline in migration method to avoid recursive connection reopening"
  - "Use sqlite3.Row factory for dict-like row access across all queries"

# Metrics
duration: 3min
completed: 2026-02-06
---

# Phase 27 Plan 01: Database Foundation Summary

**SQLite schema extended with 4 variant tracking tables, 3 feedback columns, automatic migration with backup, and schema version 27**

## Performance

- **Duration:** 3 minutes
- **Started:** 2026-02-06T18:04:04Z
- **Completed:** 2026-02-06T18:07:04Z
- **Tasks:** 2
- **Files modified:** 2

## Accomplishments
- Schema version tracking using PRAGMA user_version (version 27 set)
- Automatic database backup before migration (timestamped backups/ directory)
- 4 new tables created: thumbnail_variants, title_variants, ctr_snapshots, section_feedback
- 3 feedback columns added to video_performance: retention_drop_point, discovery_issues, lessons_learned
- Zero breaking changes - existing tools (recommender.py, performance.py) continue working

## Task Commits

Each task was committed atomically:

1. **Task 1: Add schema version tracking and backup mechanism** - `1d8bebe` (feat)
2. **Task 2: Create migration methods for all Phase 27 tables and columns** - `e692f54` (feat)

## Files Created/Modified
- `tools/discovery/database.py` - Added 3 schema tracking methods, 3 migration methods, wired into _ensure_connection()
- `tools/discovery/schema.sql` - Added Phase 27 section with table definitions and indexes

## Decisions Made

**1. Backup inline in _ensure_variant_tables()**
- **Rationale:** Original _backup_database() method closed/reopened connection, triggering recursive _ensure_connection() loop
- **Solution:** Backup logic moved inline with manual connection close/reopen without recursion
- **Impact:** Prevents infinite migration loop while preserving backup functionality

**2. Schema version guard at start of _ensure_variant_tables()**
- **Rationale:** Prevents duplicate migrations if connection reopened multiple times
- **Pattern:** `if get_schema_version() >= 27: return` before any schema changes
- **Impact:** Idempotent migration safe to call multiple times

**3. Set schema version at end of _ensure_variant_tables()**
- **Rationale:** First migration method sets version after all tables created
- **Pattern:** Other ensure methods check table existence individually (no version guard needed)
- **Impact:** Version 27 indicates Phase 27 migration complete

## Deviations from Plan

**1. [Rule 3 - Blocking] Fixed recursive migration loop**
- **Found during:** Task 2 (Testing migration execution)
- **Issue:** _backup_database() closed/reopened connection, triggering _ensure_connection() which called _ensure_variant_tables() again, creating infinite loop
- **Fix:** Moved backup logic inline in _ensure_variant_tables() with manual connection handling (close → copy → reopen without calling _ensure_connection())
- **Files modified:** tools/discovery/database.py
- **Verification:** Migration runs once, schema version 27 set, backup created
- **Committed in:** e692f54 (Task 2 commit)

---

**Total deviations:** 1 auto-fixed (1 blocking issue)
**Impact on plan:** Auto-fix essential to prevent infinite recursion. No scope creep.

## Issues Encountered

**Recursive migration loop:**
- **Problem:** _backup_database() method called _ensure_connection() when reopening connection, which triggered migration again
- **Resolution:** Moved backup logic inline with manual connection management to avoid recursion
- **Lesson:** When closing/reopening connections in migration code, avoid calling connection initialization methods that trigger migrations

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

**Ready for Phase 28 (Pacing Analysis):**
- Database schema complete with all Phase 27 tables
- Existing tools continue working (zero breaking changes verified)
- Migration pattern established for future schema extensions

**Ready for Phase 29 (Thumbnail & Title Tracking):**
- thumbnail_variants and title_variants tables ready for data insertion
- Indexes in place for efficient video_id lookups

**Ready for Phase 30 (CTR Analysis):**
- ctr_snapshots table ready for manual CTR entry storage
- Foreign keys link to variant tables for correlation analysis

**Ready for Phase 31 (Feedback Loop):**
- Feedback columns on video_performance ready for POST-PUBLISH-ANALYSIS parsing
- section_feedback table ready for retention notes

**No blockers or concerns.**

## Self-Check: PASSED

All commits, files, and schema version verified.

---
*Phase: 27-database-foundation*
*Completed: 2026-02-06*
