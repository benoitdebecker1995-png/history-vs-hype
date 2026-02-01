---
phase: 18-opportunity-scoring
plan: 01
subsystem: discovery
tags: [mcdm, saw-formula, lifecycle-tracking, channel-dna-filtering, sqlite]

# Dependency graph
requires:
  - phase: 15-database-foundation-demand-research
    provides: "Demand analysis with search_volume_proxy and data_age_days"
  - phase: 16-competition-analysis
    provides: "Competition differentiation_score (0-1) for gap scoring"
  - phase: 17-format-filtering
    provides: "Production constraints with document_score and is_production_blocked"
provides:
  - "OpportunityScorer class with SAW formula combining demand, gap, fit"
  - "Lifecycle state tracking (DISCOVERED -> ANALYZED -> RESEARCHING -> SCRIPTING -> FILMED -> PUBLISHED -> ARCHIVED)"
  - "Channel DNA violation filtering (clickbait, news-first, politician-focus)"
  - "Opportunity score 0-100 with category (Excellent, Good, Fair, Poor, Blocked)"
affects: [18-02-orchestrator, future-validation-phases]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "SAW (Simple Additive Weighting) for multi-criteria scoring"
    - "Hard constraint pre-filtering (return None, not 0, for blocked topics)"
    - "State machine in SQLite with transition validation"
    - "Component breakdown for score transparency"

key-files:
  created:
    - tools/discovery/opportunity.py
  modified:
    - tools/discovery/schema.sql
    - tools/discovery/database.py

key-decisions:
  - "SAW formula with equal weights (0.33, 0.33, 0.34) for demand, gap, fit"
  - "Hard constraints filter BEFORE scoring (animation + channel DNA blocks return None)"
  - "Lifecycle states tracked in database with transition validation per RESEARCH.md Pattern 2"
  - "Category thresholds: Excellent >=70, Good >=50, Fair >=30, Poor <30"
  - "Channel DNA violations: clickbait keywords, news-first patterns, politician-focus (starting with name)"

patterns-established:
  - "Pattern 1: Hard constraint pre-filtering - check blockers first, return None if blocked, score only if passable"
  - "Pattern 2: State machine transition validation - dictionary-based allowed transitions, reject invalid state changes"
  - "Pattern 3: Component transparency - return normalized values, weights, and contributions for each scoring factor"

# Metrics
duration: 3min
completed: 2026-02-01
---

# Phase 18 Plan 01: Opportunity Scoring Summary

**SAW scoring formula with channel DNA filtering and lifecycle state tracking for keyword progression from discovery to publication**

## Performance

- **Duration:** 3 min
- **Started:** 2026-02-01T18:03:29Z
- **Completed:** 2026-02-01T18:06:20Z
- **Tasks:** 2
- **Files modified:** 3

## Accomplishments

- OpportunityScorer calculates 0-100 scores using weighted SAW formula
- Channel DNA filtering blocks clickbait, news-first, and politician-focus keywords before scoring
- Lifecycle state machine tracks progression (DISCOVERED -> ANALYZED -> ... -> PUBLISHED -> ARCHIVED)
- Hard constraint filtering returns None for blocked topics (not 0), preventing wasted effort

## Task Commits

Each task was committed atomically:

1. **Task 1: Extend schema and database with lifecycle state columns** - `6c2c30a` (feat)
2. **Task 2: Create OpportunityScorer with SAW formula and Channel DNA filtering** - `2de2e86` (feat)

## Files Created/Modified

- `tools/discovery/opportunity.py` - OpportunityScorer class with SAW formula and channel DNA filtering
- `tools/discovery/schema.sql` - Added lifecycle_state, lifecycle_updated_at, opportunity_score_final, opportunity_category columns; created lifecycle_history table
- `tools/discovery/database.py` - Added set_lifecycle_state(), get_lifecycle_state(), get_keywords_by_lifecycle() methods with transition validation

## Decisions Made

**Scoring formula configuration:**
- Equal weights across demand (0.33), gap (0.33), and fit (0.34) for initial validation
- Slightly higher fit weight (0.34) reflects channel focus on document-heavy topics
- Weights configurable via OpportunityScorer constructor for future experimentation

**Hard constraint filtering:**
- Animation-required topics return score=None (not 0) with is_blocked=True
- Channel DNA violations return score=None with specific violation type (clickbait/news-first/politician-focus)
- Pre-filtering prevents scoring logic from running on blocked topics

**Lifecycle state management:**
- DISCOVERED is initial state for all new keywords
- State transitions validated per RESEARCH.md Pattern 2 (dictionary-based allowed transitions)
- Invalid transitions return error dict with allowed states list
- Transition history logged to lifecycle_history table for audit trail

**Category thresholds:**
- Excellent: >=70 (high demand + low competition + document-friendly)
- Good: >=50 (medium across all factors)
- Fair: >=30 (viable but lower priority)
- Poor: <30 (low scoring, research carefully before pursuing)

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None - implementation followed RESEARCH.md patterns directly.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

**Ready for Phase 18 Plan 02 (Orchestrator):**
- OpportunityScorer API complete: score_opportunity() and save_opportunity_score()
- Database supports lifecycle tracking and opportunity score caching
- Hard constraints filter animation-required and channel DNA violations
- Component breakdown enables debugging and weight adjustment

**Success criteria met:**
- ✅ OPP-01 partial: Opportunity score calculation implemented (orchestrator in Plan 02)
- ✅ OPP-02: Production constraints weighted in scoring (animation = blocked, document_score in formula)
- ✅ OPP-03: Channel DNA rules auto-filter topics via _violates_channel_dna()
- ✅ OPP-04 partial: Lifecycle states defined and tracked (state transitions in database)

**Next actions:**
- Plan 02 will create OpportunityOrchestrator to coordinate Phase 15-17 modules
- Plan 02 will add CLI for end-to-end opportunity analysis
- Plan 02 will implement Markdown report generation with component breakdown

---
*Phase: 18-opportunity-scoring*
*Completed: 2026-02-01*
