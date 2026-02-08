---
phase: 29-thumbnail-title-tracking
plan: 01
subsystem: analytics
tags: [database, cli, variant-tracking, ctr, imagehash]

# Dependency graph
requires:
  - phase: 27-database-foundation
    provides: thumbnail_variants, title_variants, ctr_snapshots tables
  - phase: 16-angle-classification
    provides: JSON tag storage pattern
provides:
  - KeywordDB CRUD methods for variant tracking (8 methods)
  - variants.py CLI with 5 subcommands
  - Perceptual hash generation for thumbnails (optional imagehash)
  - CTR snapshot recording with variant FK references
  - Trend analysis for CTR history
affects: [29-02-analyze-integration]

# Tech tracking
tech-stack:
  added: [imagehash (optional), PIL (optional)]
  patterns: [error dict returns, JSON tag storage round-trip, graceful import fallback, sys.path insert for cross-module imports]

key-files:
  created:
    - tools/youtube-analytics/variants.py
  modified:
    - tools/discovery/database.py

key-decisions:
  - "Error dict pattern: return {'status': 'inserted', ...} on success, {'error': msg} on failure"
  - "JSON tag storage: use json.dumps() to store lists, json.loads() to retrieve (matching Phase 16)"
  - "Variant letter validation: single uppercase A-Z character"
  - "CTR validation: must be 0-100 range"
  - "Perceptual hash: optional with graceful fallback if imagehash not installed"
  - "Snapshot date: defaults to today (UTC) but accepts custom dates for late entries"
  - "Trend analysis: compare earliest to latest CTR for UP/DOWN/FLAT direction"
  - "Tag parsing: comma-separated strings split and trimmed"

patterns-established:
  - "CRUD methods follow established error dict pattern from Phase 19"
  - "JSON tag parsing matches get_classified_videos pattern from Phase 16"
  - "sys.path insert matches analyze.py pattern for cross-module imports"
  - "Video ID validation: r'^[\w-]{11}$' matching YouTube ID format"
  - "Graceful optional dependency: try/except ImportError with AVAILABLE flag"
  - "Import datetime and json inside methods (matching existing patterns)"

# Metrics
duration: 5min
completed: 2026-02-07
---

# Phase 29 Plan 01: Variant Tracking CRUD & CLI Summary

**Extended KeywordDB with 8 Phase 29 CRUD methods and created standalone variant management CLI with 5 subcommands for registering thumbnails, titles, and recording CTR snapshots**

## Performance

- **Duration:** 5 min
- **Started:** 2026-02-07T21:26:11Z
- **Completed:** 2026-02-07T21:31:13Z
- **Tasks:** 2 (database CRUD + CLI module)
- **Files modified:** 2

## Accomplishments

- 8 new CRUD methods in KeywordDB following error dict return pattern
- variants.py CLI module with 5 subcommands (register-thumb, register-title, record-ctr, list, snapshots)
- JSON tag storage works round-trip (store as JSON, retrieve as list)
- Perceptual hash generation with graceful imagehash fallback
- CTR validation rejects values outside 0-100 range
- Trend analysis shows UP/DOWN/FLAT CTR changes over time
- Human-readable formatted table output

## Task Commits

Each task committed atomically:

1. **Database CRUD methods** - `6a11275` (feat: 8 CRUD methods for variant tracking)
2. **CLI module** - `bc04ded` (feat: variant management CLI with 5 subcommands)

## Files Created/Modified

- `tools/discovery/database.py` - Added Phase 29 CRUD methods section with 8 methods
- `tools/youtube-analytics/variants.py` - New CLI module with 5 subcommands (424 lines)

## Decisions Made

**Database Layer:**
- All CRUD methods follow error dict pattern: `{'status': 'inserted', 'variant_id': N}` on success, `{'error': msg}` on failure
- JSON tag storage matches Phase 16 pattern: json.dumps() to store, json.loads() to retrieve
- Variant letter validation: single uppercase A-Z character enforced
- CTR percent validation: must be 0-100 range, negative counts rejected
- Import datetime and json inside methods (matching existing pattern on lines 833, 890)

**CLI Interface:**
- Video ID validation uses YouTube 11-character pattern: `r'^[\w-]{11}$'`
- Perceptual hash generation optional: graceful fallback if imagehash not installed
- Tag parsing: comma-separated strings split and trimmed
- Trend analysis: compares earliest to latest snapshot for delta calculation
- sys.path pattern matches analyze.py for KeywordDB import

**Methods Implemented:**
1. add_thumbnail_variant() - validates letter, stores visual patterns as JSON, optional hash
2. add_title_variant() - validates letter, auto-calculates character count, stores formula tags as JSON
3. add_ctr_snapshot() - validates CTR 0-100, stores impression/view counts with variant FKs
4. get_thumbnail_variants() - retrieves with JSON tag parsing
5. get_title_variants() - retrieves with JSON tag parsing
6. get_ctr_snapshots() - ordered by snapshot_date ASC for trend analysis
7. get_variant_summary() - quick counts for thumbnails/titles/snapshots
8. get_latest_ctr() - most recent CTR snapshot with DESC ordering

**CLI Commands:**
1. register-thumb - registers thumbnail with file path, visual patterns, perceptual hash
2. register-title - registers title with text, character count, formula tags
3. record-ctr - records CTR snapshot with impressions, views, optional variant FKs
4. list - shows all variants for a video in formatted tables
5. snapshots - displays CTR history with trend analysis (UP/DOWN/FLAT)

## Next Phase Readiness

**Ready for 29-02 (analyze integration):**
- Database CRUD methods tested and working
- CLI provides manual data entry workflow
- JSON tag storage proven working round-trip
- Variant tracking foundation complete

**Blockers:** None

**Testing Notes:**
- All CRUD methods tested with round-trip JSON parsing
- CLI commands tested with both valid and invalid inputs
- Validation correctly rejects CTR > 100, invalid video IDs, invalid variant letters
- Trend analysis correctly calculates delta and direction
- Test data cleaned up after verification

## Self-Check: PASSED

All key files exist:
- tools/youtube-analytics/variants.py (created)
- tools/discovery/database.py (modified)

All commits present:
- 6a11275 (Phase 29 CRUD methods)
- bc04ded (variant management CLI)
