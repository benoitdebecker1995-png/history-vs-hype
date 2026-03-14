---
phase: 60-retitle-and-rethumb-underperforming-videos-with-impressions-but-low-ctr
plan: 01
subsystem: workflow
tags: [retitle, thumbnail, ctr, packaging, slash-command, youtube-studio]

# Dependency graph
requires:
  - phase: 60-context
    provides: locked decisions for selection criteria, workflow, measurement window, flags
  - phase: 61-data-driven-packaging-gate
    provides: DB-enriched title_scorer with real CTR calibration
provides:
  - /retitle slash command orchestrating full retitle pipeline
  - --audit mode for ranked underperformer inspection
  - --check mode for 7-day post-swap CTR measurement
  - --revert mode for copy-paste rollback
affects: [future-retitle-batches, post-publish-analysis-format, ctr-feedback-loop]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Slash command markdown file pattern (.claude/commands/) with YAML frontmatter, Claude interprets at runtime"
    - "Retention-weighted priority scoring: priority = wasted_impressions × (1 + retention_bonus)"
    - "7-day measurement window override for existing published videos (not 48h)"
    - "Fallback chain: script-generated titles → CANDIDATES dict → RETITLE-RECOMMENDATIONS.md"

key-files:
  created:
    - .claude/commands/retitle.md
  modified: []

key-decisions:
  - "Retention weighting formula: priority_score = wasted_impressions × (1 + retention_bonus) where bonus is +0.5 if retention >= 35%, +0.25 if 25-35%, +0 below 25% — surfaces content-quality wins over dual packaging+content failures"
  - "Score threshold 65 minimum and REJECTED grade = hard block — consistent with /publish gate"
  - "SWAP-CHECKLIST.md is ephemeral (regenerated each run); SWAP LOG in POST-PUBLISH-ANALYSIS.md is permanent record"
  - "7-day measurement window for retitles (not 48h from SWAP-PROTOCOL.md) — older videos need algorithm re-testing time"
  - "--check flag reads swap date from SWAP LOG and refuses measurement if < 7 days elapsed"
  - "Map type auto-suggestion: vs/conflict → split-map, movement verbs → arrow-flow, treaty/legal → document-on-map, 3+ claimants → labeled-zone, default → split-map"

patterns-established:
  - "Retitle slash command pattern: orchestrate Python tools via sys.path.insert + import at runtime, no new Python modules needed"
  - "SWAP LOG format: markdown table in POST-PUBLISH-ANALYSIS.md with append-not-overwrite semantics"

requirements-completed: [RETITLE-01, RETITLE-02, RETITLE-03]

# Metrics
duration: 2min
completed: 2026-03-14
---

# Phase 60 Plan 01: Retitle Slash Command Summary

**`/retitle` slash command wiring retitle_audit, retitle_gen, title_scorer, and thumbnail_checker into a full pipeline with audit, generate, score, thumbnail-check, and SWAP-CHECKLIST.md output**

## Performance

- **Duration:** 2 min
- **Started:** 2026-03-14T23:11:52Z
- **Completed:** 2026-03-14T23:14:06Z
- **Tasks:** 1
- **Files modified:** 1

## Accomplishments

- Created `.claude/commands/retitle.md` (366 lines) with YAML frontmatter and 4 operating modes
- Full pipeline mode: runs retitle_audit with retention-weighted sort, generates script-based candidates per video, scores all via title_scorer, checks thumbnail compliance, writes SWAP-CHECKLIST.md to channel-data/
- Audit-only mode: ranked underperformer list with retention-weighted priority column, no candidate generation
- Post-swap measurement mode (`--check`): 7-day guard, collects post-CTR from user, evaluates success/revert, triggers ctr_ingest on success
- Revert mode (`--revert`): pulls old title from SWAP LOG for immediate copy-paste

## Task Commits

1. **Task 1: Create /retitle slash command** - `c6ee486` (feat)

## Files Created/Modified

- `.claude/commands/retitle.md` — Slash command orchestrating full retitle pipeline (audit → generate → score → thumbnail check → SWAP-CHECKLIST.md output)

## Decisions Made

- Retention weighting formula chosen: `priority_score = wasted_impressions × (1 + retention_bonus)`. Bonus tiers: +0.5 if retention >= 35%, +0.25 if 25-35%, +0 below 25%. This surfaces "South China Sea" (50.5% retention, 1.83% CTR) above "Dark Ages" (13% retention, 1.11% CTR) — a title fix won't hold viewers with content problems.
- Used same score threshold (65 minimum, REJECTED = hard block) as `/publish` command for consistency.
- SWAP-CHECKLIST.md marked ephemeral — regenerated on each run. SWAP LOG in POST-PUBLISH-ANALYSIS.md is the durable record with revert capability.
- Map type auto-suggestion logic based on content signals in title/diagnosis: vs/conflict → split-map, movement/extraction verbs → arrow-flow, treaty/legal central → document-on-map, 3+ country claimants → labeled-zone.

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- `/retitle` command is ready to use immediately
- Run `/retitle --audit` first to see the current underperformer landscape
- Run `/retitle` to generate the first SWAP-CHECKLIST.md batch
- Phase 60 Plan 02 follows (if planned): SWAP LOG injection tooling or additional pipeline steps

---
*Phase: 60-retitle-and-rethumb-underperforming-videos-with-impressions-but-low-ctr*
*Completed: 2026-03-14*
