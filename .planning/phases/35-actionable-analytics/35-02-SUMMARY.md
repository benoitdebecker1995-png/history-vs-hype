---
phase: 35-actionable-analytics
plan: 02
subsystem: analytics
tags: [performance-aggregation, feedback-queries, pre-script-insights, topic-strategy]

# Dependency graph
requires:
  - phase: 31-feedback-loop-integration
    provides: video_performance table and feedback storage infrastructure
  - phase: 19-video-performance-tracking
    provides: TAG_VOCABULARY and performance classification patterns
provides:
  - Topic strategy aggregation with confidence flags and concrete next steps
  - Pre-script insight surfacing combining feedback + strategy + retention
  - Proactive insight display for /script command integration (ready for 35-03)
affects: [35-03-command-integration, script-command, analyze-command]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - Topic performance aggregation with adaptive confidence levels
    - Pre-script insight surfacing pattern (replacing post-mortem preambles)
    - Pattern suggestion generation referencing STYLE-GUIDE.md Part 6

key-files:
  created:
    - tools/youtube-analytics/topic_strategy.py
  modified:
    - tools/youtube-analytics/feedback_queries.py

key-decisions:
  - "Use confidence flags (high/medium/low) based on video count thresholds (6+/3-5/<3)"
  - "Generate concrete next steps instead of generic recommendations ('Prioritize X' not 'Do more of X')"
  - "Reference STYLE-GUIDE.md Part 6 patterns in suggestions for actionability"
  - "Extract retention lessons from observations with drop magnitude parsing"
  - "Maintain backward compatibility - get_insights_preamble unchanged"

patterns-established:
  - "Topic strategy pattern: aggregate by topic_type, flag low-confidence, generate actionable steps"
  - "Pre-script insight pattern: combine multiple sources (feedback + strategy + patterns) into single display"
  - "Graceful degradation pattern: TOPIC_STRATEGY_AVAILABLE flag allows optional integration"

# Metrics
duration: 3min
completed: 2026-02-11
---

# Phase 35 Plan 02: Topic Strategy Aggregation & Pre-Script Insights

**Topic performance aggregation with confidence flags and pre-script insight surfacing combining feedback, strategy, and retention lessons**

## Performance

- **Duration:** 3 min
- **Started:** 2026-02-11T17:43:00Z
- **Completed:** 2026-02-11T17:45:41Z
- **Tasks:** 2
- **Files modified:** 2 (1 created, 1 extended)

## Accomplishments

- topic_strategy.py aggregates performance by topic type with avg retention, conversion, best/worst videos, and concrete next steps
- Pre-script insight surfacing (get_pre_script_insights) combines topic feedback, strategy summary, and pattern suggestions
- Confidence flags warn when insights based on <3 videos per topic
- Pattern suggestions reference STYLE-GUIDE.md Part 6 for actionability
- Backward compatible - existing feedback_queries functions unchanged

## Task Commits

Each task was committed atomically:

1. **Task 1: Create topic_strategy.py** - `952bc13` (feat)
2. **Task 2: Extend feedback_queries.py with pre-script insights** - `799efde` (feat)

## Files Created/Modified

- `tools/youtube-analytics/topic_strategy.py` (537 lines) - Aggregates video_performance by topic_type, calculates averages, generates concrete next steps, provides terminal/markdown formatting with CLI
- `tools/youtube-analytics/feedback_queries.py` (+242 lines) - Added get_pre_script_insights(), format_pre_script_display(), _generate_pattern_suggestions() with TOPIC_STRATEGY_AVAILABLE flag

## Decisions Made

**Confidence thresholds:** 6+ videos = high, 3-5 = medium, <3 = low. Based on research insight that small dataset (~15 videos total) requires explicit confidence signaling.

**Concrete next steps:** Generate actionable recommendations ("Prioritize territorial -- 0.42% conversion vs 0.28% average") instead of generic advice ("do more territorial videos"). Addresses ACTN-03 requirement.

**Pattern references:** Link suggestions to STYLE-GUIDE.md Part 6 specific patterns (e.g., "zero-impact moments Part 6.4 Pattern 2"). Makes recommendations actionable by pointing to documented techniques.

**Backward compatibility:** Maintain get_insights_preamble() unchanged for other commands. New get_pre_script_insights() is enhanced replacement specifically for /script context.

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None - both modules integrated cleanly with existing infrastructure (KeywordDB, performance.py TAG_VOCABULARY, feedback storage).

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

Ready for Plan 35-03 (command integration):
- topic_strategy.generate_topic_strategy() provides aggregated performance data
- feedback_queries.get_pre_script_insights() provides structured insight dict
- format_pre_script_display() provides ready-to-display text
- Both modules return error dicts on failure (graceful degradation)

Blockers: None. Plan 35-03 can wire these functions into /analyze and /script commands immediately.

## Self-Check: PASSED

All claims verified:
- FOUND: tools/youtube-analytics/topic_strategy.py
- FOUND: 952bc13 (Task 1 commit)
- FOUND: 799efde (Task 2 commit)

---
*Phase: 35-actionable-analytics*
*Completed: 2026-02-11*
