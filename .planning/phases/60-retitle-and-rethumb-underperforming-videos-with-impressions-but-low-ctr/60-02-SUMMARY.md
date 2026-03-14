---
phase: 60-retitle-and-rethumb-underperforming-videos-with-impressions-but-low-ctr
plan: 02
subsystem: workflow
tags: [retitle, ctr-measurement, swap-log, feedback-loop, slash-command]

# Dependency graph
requires:
  - phase: 60-01
    provides: /retitle slash command with audit and full pipeline modes
  - phase: 61-data-driven-packaging-gate
    provides: ctr_ingest.py for feedback loop closure
provides:
  - /retitle --check flag: 7-day post-swap CTR measurement with success/revert decision
  - /retitle --revert flag: old title retrieval from SWAP LOG for copy-paste rollback
  - SWAP LOG injection: "swaps executed" trigger injects SWAP LOG into POST-PUBLISH-ANALYSIS files
  - Feedback loop closure: successful swaps ingest CTR data into keywords.db via ctr_ingest
affects: [post-publish-analysis-format, ctr-feedback-loop, title-scoring-calibration]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Dual-location POST-PUBLISH-ANALYSIS search: channel-data/analyses/ first, video-projects/ fallback"
    - "Append-not-overwrite semantics for SWAP LOG table entries"
    - "ctr_ingest.py existence guard before automated feedback — graceful degradation to manual"
    - "Create-if-missing pattern for POST-PUBLISH-ANALYSIS files"
    - "7-day guard blocks measurement before enough data accumulates"

key-files:
  created: []
  modified:
    - .claude/commands/retitle.md

key-decisions:
  - "ctr_ingest.py is optional — existence check before invocation, manual fallback if absent"
  - "POST-PUBLISH-ANALYSIS search order: channel-data/analyses/ primary, video-projects/ secondary — keeps new files in canonical location while supporting legacy project-folder files"
  - "SWAP LOG injection triggered by user saying 'swaps executed' — human confirms before Claude writes to files"
  - "Success threshold +0.5% CTR (inherited from 60-CONTEXT.md decision, documented explicitly in --check flow)"

# Metrics
duration: 5min
completed: 2026-03-14T23:17:31Z
---

# Phase 60 Plan 02: Retitle Measurement Loop Summary

**`--check` and `--revert` flags plus SWAP LOG injection close the retitle feedback loop: swap in Studio, inject log, wait 7 days, measure CTR delta, feed success data into keywords.db or revert with copy-paste.**

## Performance

- **Duration:** 5 min
- **Started:** 2026-03-14T23:12:00Z
- **Completed:** 2026-03-14T23:17:31Z
- **Tasks:** 1
- **Files modified:** 1

## Accomplishments

- Updated `.claude/commands/retitle.md` (+72 lines, -12 lines refactored)
- Added SWAP LOG injection section: "swaps executed" trigger with append-not-overwrite rule, create-if-missing logic, dual thumbnail/title row support
- Hardened `--check` mode: dual-location file search, explicit "No SWAP LOG" message, ctr_ingest.py existence guard
- Hardened `--revert` mode: dual-location file search, "no file found" error message
- Full pipeline documentation consistent: SWAP LOG format matches 60-RESEARCH.md spec throughout

## Task Commits

1. **Task 1: Add --check/--revert measurement loop and SWAP LOG injection** - `3880723` (feat)

## Files Created/Modified

- `.claude/commands/retitle.md` — Added SWAP LOG injection section and hardened --check/--revert with dual-location search, existence guards, and explicit error messages

## Decisions Made

- ctr_ingest.py is optional at runtime — `os.path.exists('tools/ctr_ingest.py')` guard before invocation prevents errors on setups where Phase 61 hasn't run yet
- POST-PUBLISH-ANALYSIS search order: `channel-data/analyses/` primary, `video-projects/` secondary — new files written to canonical location, legacy project-folder files still readable
- "Swaps executed" as the trigger phrase for SWAP LOG injection — user explicitly confirms before Claude modifies any files
- Renumbered --check steps to 1-4 (was 1-3, Step 1 was split to "locate file" + "verify window")

## Deviations from Plan

### Auto-fixed Issues

None.

### Notes on Pre-existing State

Plan 01 had already scaffolded `--check` and `--revert` modes in the command file. Plan 02 hardened those modes with the specific requirements from the plan spec (dual-location search, "No SWAP LOG" message, ctr_ingest guard) and added the SWAP LOG injection section which was referenced in Plan 01 but not fully specified as a standalone workflow step.

## Issues Encountered

None.

## User Setup Required

None — slash command file only, no external configuration.

## Next Phase Readiness

- `/retitle` command is fully functional end-to-end
- Full workflow: `--audit` → `/retitle` → "swaps executed" → SWAP LOG injected → 7 days → `--check` → SUCCESS/REVERT → ctr_ingest closes loop
- Phase 60 complete

---
*Phase: 60-retitle-and-rethumb-underperforming-videos-with-impressions-but-low-ctr*
*Completed: 2026-03-14*
