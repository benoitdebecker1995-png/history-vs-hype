---
phase: 5
plan: 3
name: User-Facing Documentation Updates
subsystem: documentation
tags: [documentation, commands, workflow]
dependency-graph:
  requires:
    - 05-01 (command consolidation)
    - 05-02 (agent simplification)
  provides:
    - simplified-start-here
    - updated-claude-md
    - deprecated-commands-archive
    - streamlined-workflow-reference
  affects:
    - future user onboarding
tech-stack:
  patterns:
    - "ask Claude" guidance over detailed docs
    - phase-organized command reference
    - /status and /help for discovery
key-files:
  modified:
    - START-HERE.md
    - CLAUDE.md
    - VERIFIED-WORKFLOW-QUICK-REFERENCE.md
  created:
    - .claude/commands/_DEPRECATED/README.md
    - .claude/commands/_DEPRECATED/*.md (21 files)
decisions:
  - decision: "Ask Claude first" as primary START-HERE guidance
    rationale: User describes what they want; Claude knows the system
  - decision: Archive deprecated commands rather than delete
    rationale: Preserves git history and provides migration reference
  - decision: 65% reduction in workflow reference
    rationale: Core workflow preserved; redundant sections removed
metrics:
  duration: ~25 minutes
  completed: 2026-01-22
---

# Phase 5 Plan 3: User-Facing Documentation Updates Summary

User-facing docs now direct users to describe what they want rather than memorize commands.

## What Changed

### Task 1: START-HERE.md Simplification
- **Before:** 503 lines with detailed workflow documentation
- **After:** 38 lines with "just ask Claude" guidance
- **Key changes:**
  - Primary guidance: "Just ask Claude what you want to do"
  - Quick commands table organized by phase
  - References /status and /help for discovery
  - Technical details stay in CLAUDE.md (for Claude to read)

### Task 2: CLAUDE.md Quick Start Update
- Replaced 20+ command list with phase-organized structure
- Updated command references:
  - `/new-video-verified` -> `/research --new`
  - `/publish-correction` -> `/engage --correction`
- Added navigation commands (/status, /help)

### Task 3: Deprecated Commands Archive
- Created `.claude/commands/_DEPRECATED/` folder
- Moved 21 old commands with deprecation headers
- Each file shows replacement command
- README.md contains full migration table
- Main commands folder now contains only 10 active commands

### Task 4: VERIFIED-WORKFLOW-QUICK-REFERENCE.md
- **Before:** 509 lines
- **After:** 179 lines (65% reduction)
- **Preserved:** Core 3-phase workflow, quality gates, error prevention
- **Removed:** Redundant sections (templates, troubleshooting, detailed checklists)
- Updated all command references

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] fix-subtitles.md still in main folder**
- **Found during:** Task 3
- **Issue:** Old fix-subtitles.md not in deprecation list but replaced by /fix
- **Fix:** Added to deprecation archive, updated README migration table
- **Files modified:** .claude/commands/_DEPRECATED/fix-subtitles.md, README.md
- **Commit:** b6f38a2

## Commits

| Hash | Type | Description |
|------|------|-------------|
| 7871524 | docs | Simplify START-HERE.md to minimal entry point |
| 1d3fac0 | docs | Update CLAUDE.md Quick Start to consolidated commands |
| b6f38a2 | refactor | Archive deprecated commands to _DEPRECATED folder |
| d1786fb | docs | Simplify VERIFIED-WORKFLOW-QUICK-REFERENCE.md |

## Verification Results

- [x] START-HERE.md under 50 lines (38 lines)
- [x] START-HERE.md contains "ask Claude" guidance
- [x] START-HERE.md references /status and /help
- [x] CLAUDE.md has no old command references
- [x] Main commands folder has 10 active commands
- [x] _DEPRECATED folder has 22 files (21 commands + README)
- [x] Workflow reference significantly reduced (65%)

## Files Changed

**Modified:**
- `START-HERE.md` - 503 -> 38 lines
- `CLAUDE.md` - Quick Start section updated
- `VERIFIED-WORKFLOW-QUICK-REFERENCE.md` - 509 -> 179 lines

**Created:**
- `.claude/commands/_DEPRECATED/README.md`
- 21 deprecated command files with headers

**Deleted (from main commands):**
- 21 command files (moved to _DEPRECATED)

## Next Phase Readiness

Phase 5 (Workflow Simplification) is now complete:
- 05-01: Command consolidation (8 commands from 20+)
- 05-02: Agent simplification (3 agents from 8)
- 05-03: Documentation updates (this plan)

**System is ready for normal use with simplified interface.**

## Impact

| Metric | Before | After |
|--------|--------|-------|
| START-HERE.md lines | 503 | 38 |
| Active commands | 20+ | 10 |
| Workflow reference lines | 509 | 179 |
| User mental load | "memorize commands" | "ask Claude" |
