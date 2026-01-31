---
phase: 15-database-foundation-demand-research
plan: 01
subsystem: database
tags: [sqlite, demand-analysis, opportunity-scoring, caching]

# Dependency graph
requires:
  - phase: 13-token-optimization-model-assignment
    provides: keywords.db with existing schema and KeywordDB class
provides:
  - 5 new database tables for demand research (trends, competitor_channels, competitor_videos, opportunity_scores, validations)
  - 4 new indexes for time-series queries
  - 7 new KeywordDB methods for demand data caching
  - DemandAnalyzer class with position scoring and opportunity ratio calculation
affects: [15-02, 15-03, 16-competition-analysis, 17-filtering-ranking, 18-validation]

# Tech tracking
tech-stack:
  added: []
  patterns: [error-dict-returns, 7-day-cache-with-staleness, position-to-score-mapping]

key-files:
  created:
    - tools/discovery/demand.py
  modified:
    - tools/discovery/schema.sql
    - tools/discovery/database.py

key-decisions:
  - "7-day cache default with data_age_days tracking in all cached results"
  - "Conservative opportunity thresholds: High >4x, Medium 2-4x, Low <2x"
  - "Linear position-to-score mapping: position 1 = 100, position 10 = 10, not found = 0"

patterns-established:
  - "Cache pattern: return None if data too old, include data_age_days in valid results"
  - "Opportunity ratio: demand_score / competition_count with category thresholds"
  - "Trend formatting: arrow unicode + percentage (up/stable/down based on 20% threshold)"

# Metrics
duration: 12min
completed: 2026-01-31
---

# Phase 15 Plan 01: Database Foundation Summary

**Extended keyword database with 5 demand tables, 7 caching methods, and DemandAnalyzer class for opportunity ratio calculation**

## Performance

- **Duration:** 12 min
- **Started:** 2026-01-31T09:00:00Z
- **Completed:** 2026-01-31T09:12:00Z
- **Tasks:** 3
- **Files modified:** 3

## Accomplishments

- Extended schema.sql with 5 new tables for demand research data storage
- Added 7 database methods to KeywordDB for trend and opportunity caching with 7-day freshness
- Created DemandAnalyzer module with position scoring (autocomplete -> 0-100) and opportunity ratio (4x+ = High)
- All verification tests pass including position scoring, opportunity ratios, and trend formatting

## Task Commits

Each task was committed atomically:

1. **Task 1: Extend database schema with 5 new tables** - `c65b2ca` (feat)
2. **Task 2: Extend KeywordDB with demand data methods** - `a99710d` (feat)
3. **Task 3: Create DemandAnalyzer module** - `ddf581b` (feat)

## Files Created/Modified

- `tools/discovery/schema.sql` - Added trends, competitor_channels, competitor_videos, opportunity_scores, validations tables with 4 indexes
- `tools/discovery/database.py` - Added 7 methods: add_trend, get_cached_trend, get_latest_trend, add_competitor_video, get_competition_count, add_opportunity_score, get_opportunity_score
- `tools/discovery/demand.py` - New DemandAnalyzer class with calculate_position_score, calculate_opportunity_ratio, format_trend_direction, analyze_keyword stub

## Decisions Made

1. **Cache pattern:** All cached data methods return `data_age_days` field for staleness tracking, return `None` when data exceeds `max_age_days` parameter
2. **Opportunity thresholds:** Conservative 4x+ for High (per CONTEXT.md - high research overhead means only obvious wins)
3. **Position scoring:** Linear mapping from position 1-10 to score 100-10, with 0 for not found
4. **Trend arrow thresholds:** >20% change for rising/declining arrows, otherwise stable arrow

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

- **Existing database migration:** The existing keywords.db file didn't have the new tables initially. Running `init_database()` safely added the new tables using `CREATE TABLE IF NOT EXISTS` pattern without affecting existing data.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- Database foundation complete for Plan 02 (External Data Sources)
- DemandAnalyzer.analyze_keyword() is a stub ready for integration with:
  - Google autocomplete for position scoring
  - trendspyg for Google Trends data
  - YouTube Data API for competition counting
- All methods follow error dict pattern for consistent error handling

---
*Phase: 15-database-foundation-demand-research*
*Completed: 2026-01-31*
