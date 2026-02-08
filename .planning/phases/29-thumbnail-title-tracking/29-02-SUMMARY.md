---
phase: 29-thumbnail-title-tracking
plan: 02
subsystem: analytics
tags: [python, youtube-analytics, variant-tracking, ctr-analysis]

# Dependency graph
requires:
  - phase: 29-01
    provides: KeywordDB methods for variant tracking (get_variant_summary, get_thumbnail_variants, get_title_variants, get_ctr_snapshots)
provides:
  - Variant-aware /analyze command that displays registered variants and CTR history
  - CTR trend calculation showing delta between first and last snapshots
  - Graceful degradation when variant tracking unavailable
affects: [post-publish-workflow, youtube-analytics]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "VARIANTS_AVAILABLE flag for graceful import degradation (matches DISCOVERY_AVAILABLE pattern)"
    - "Passive data display in analysis output (no new CLI flags needed)"
    - "CTR trend calculation from chronological snapshots"

key-files:
  created: []
  modified: [tools/youtube-analytics/analyze.py]

key-decisions:
  - "Reused existing DISCOVERY_AVAILABLE import pattern for VARIANTS_AVAILABLE flag"
  - "Added variant section after Discovery Diagnostics, before Errors section"
  - "Only display variant section when variant data exists (graceful absence)"
  - "CTR trend shows direction (up/down/flat) and delta when 2+ snapshots exist"

patterns-established:
  - "Variant section structure: summary counts → thumbnail table → title table → CTR history → trend"
  - "Truncate thumbnail hash to first 8 chars for readability"
  - "Truncate title text to 50 chars with ellipsis for table display"
  - "CTR snapshots in chronological order from database query"

# Metrics
duration: 5min
completed: 2026-02-08
---

# Phase 29 Plan 02: Variant Tracking Summary

**Integrated variant tracking into /analyze output with thumbnail/title variant tables, CTR history, and trend calculation**

## Performance

- **Duration:** 5 min
- **Started:** 2026-02-08T00:01:56Z
- **Completed:** 2026-02-08T00:07:23Z
- **Tasks:** 1
- **Files modified:** 1

## Accomplishments
- Extended analyze.py to query variant data when VARIANTS_AVAILABLE
- Added Variant Tracking section to markdown output with 3 tables (thumbnails, titles, CTR snapshots)
- Implemented CTR trend calculation showing direction and delta when 2+ snapshots exist
- Maintained graceful degradation when KeywordDB import fails
- Verified no variant section appears when no variants registered (graceful absence)

## Task Commits

Each task was committed atomically:

1. **Task 1: Add variant section to /analyze output** - `e7cb418` (feat)

## Files Created/Modified
- `tools/youtube-analytics/analyze.py` - Added KeywordDB import, variant data fetching in run_analysis(), and variant section in format_analysis_markdown()

## Decisions Made
- **Import pattern:** Reused existing discovery import pattern with sys.path.insert and VARIANTS_AVAILABLE flag for consistency
- **Section placement:** Added variant section after Discovery Diagnostics (line 946) for logical flow: performance → retention → comments → lessons → discovery → variants → errors
- **CTR trend logic:** Direction determined by comparing first and last snapshots (not sequential deltas) to show overall trend
- **Table truncation:** Hash truncated to 8 chars, title to 50 chars for markdown table readability

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

Phase 29 complete (2/2 plans). Variant tracking system ready for production use.

**Ready for:**
- Recording thumbnail variants with perceptual hashes and tags
- Recording title variants with character counts and formula tags
- Recording CTR snapshots during post-publish analysis
- Viewing variant history alongside performance data in /analyze

**Workflow complete:**
1. User runs `/analyze VIDEO_ID` after publish
2. User registers variants: `python variants.py register-thumb VIDEO_ID A path/to/thumb.png --tags "map,evidence"`
3. User records CTR: `python variants.py record-ctr VIDEO_ID 4.5 1000 45`
4. User runs `/analyze VIDEO_ID` again to see variant data alongside performance metrics
5. User can track CTR evolution: `python variants.py snapshots VIDEO_ID`

**No blockers.** Phase 29 is complete and functional.

---
*Phase: 29-thumbnail-title-tracking*
*Completed: 2026-02-08*

## Self-Check: PASSED

All files and commits verified:
- ✓ tools/youtube-analytics/analyze.py exists
- ✓ Commit e7cb418 exists
