---
phase: 06-competitive-intelligence
plan: 01
subsystem: learning-system
tags: [techniques, tracking, improvement-loop]

dependency-graph:
  requires: []
  provides:
    - technique-effectiveness-tracking
    - technique-usage-logging
    - untried-technique-surfacing
  affects: [script-writing, technique-selection]

tech-stack:
  added: []
  patterns: [learning-loop, effectiveness-tracking]

key-files:
  created:
    - channel-data/TECHNIQUE-USAGE-LOG.md
  modified:
    - .claude/REFERENCE/PROVEN-TECHNIQUES-LIBRARY.md

decisions:
  - id: technique-log-structure
    choice: "Usage log with rating scale, summary table, and untried checklist"
    rationale: "Enables multiple learning views: per-video, per-technique, opportunities"

metrics:
  duration: ~7 minutes
  completed: 2026-01-23
---

# Phase 06 Plan 01: Effectiveness Tracking Summary

**One-liner:** Created technique usage log and added tracking fields to 25 techniques, enabling a learning loop to discover what actually works.

## What Was Built

### 1. TECHNIQUE-USAGE-LOG.md (New File)
Central tracking file with:
- **Rating scale (1-5)** with clear criteria (Excellent to Failed)
- **Usage log table** capturing: Date, Video, Technique, Section, Retention, Rating, Notes
- **Performance summary table** aggregating usage counts and average ratings per technique
- **Untried techniques checklist** organized by category (Opening Hooks, Argument & Evidence, etc.)

### 2. PROVEN-TECHNIQUES-LIBRARY.md (Enhanced)
Added to existing 836-line file:
- **Tracking note at top** pointing to usage log
- **25 effectiveness tracking blocks** (one per technique section):
  - `**Effectiveness:** Not yet rated`
  - `**Used in:** (none yet)`
  - `**Log usage:** Update channel-data/TECHNIQUE-USAGE-LOG.md`
- **"How to Track Effectiveness" section** at end with 3-step workflow

## Learning Loop Enabled

```
Use technique in video
       |
       v
Log in TECHNIQUE-USAGE-LOG.md (date, video, technique, section)
       |
       v
Rate 1-5 after video publishes (based on retention/feel)
       |
       v
Update PROVEN-TECHNIQUES-LIBRARY.md (change "Not yet rated" to actual rating)
       |
       v
Over time: See which techniques actually work vs. theoretical
```

## Decisions Made

| Decision | Rationale |
|----------|-----------|
| 5-point rating scale | Balances granularity with simplicity; clear criteria for each level |
| Usage log + summary tables | Multiple views: per-video tracking AND technique-level aggregation |
| Untried checklist by category | Easy to spot opportunities when planning new video openings/arguments |
| Tracking fields on each technique | In-context reminder; don't need to leave library to log usage |

## Deviations from Plan

None - plan executed exactly as written.

## Files Changed

| File | Change | Lines |
|------|--------|-------|
| `channel-data/TECHNIQUE-USAGE-LOG.md` | Created | 132 |
| `.claude/REFERENCE/PROVEN-TECHNIQUES-LIBRARY.md` | Enhanced with tracking | +112 |

## Commits

| Hash | Message |
|------|---------|
| ecc7d36 | feat(06-01): create TECHNIQUE-USAGE-LOG.md for tracking technique performance |
| 8442fed | feat(06-01): add effectiveness tracking fields to PROVEN-TECHNIQUES-LIBRARY.md |

## Verification Results

1. TECHNIQUE-USAGE-LOG.md exists with complete structure (rating scale, log table, summary, untried list)
2. PROVEN-TECHNIQUES-LIBRARY.md has 25 "Effectiveness:" fields
3. Cross-reference: library points to log (25+ references)
4. Cross-reference: log references library (in Untried Techniques section)
5. No structural changes to existing technique organization

## Success Criteria Met

- [x] User can record technique usage with video reference and rating
- [x] User can see performance summary across techniques
- [x] User can see which techniques haven't been tried yet
- [x] Tracking fields exist on techniques without breaking existing organization

## Next Phase Readiness

Phase 06 Plan 02 (Gap Analysis Database) can proceed. No blockers.

---

*Summary generated: 2026-01-23*
