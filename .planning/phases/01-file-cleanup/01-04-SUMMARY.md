---
phase: 01-file-cleanup
plan: 04
subsystem: file-organization
tags: [naming-conventions, script-management, folder-structure]

# Dependency graph
requires:
  - phase: 01-01
    provides: Deleted outdated files, cleared workspace noise
  - phase: 01-02
    provides: Consolidated duplicate files
  - phase: 01-03
    provides: Relocated misplaced files to proper locations
provides:
  - Consistent [number]-[topic]-[year] folder naming across all projects
  - Single FINAL-SCRIPT.md per project with old versions archived
  - Complete user review list for library folder cleanup
affects: [project-creation, script-management, future-video-projects]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Project folders follow ^[0-9]+-[a-z0-9-]+-[0-9]{4}$ pattern"
    - "Each project has exactly one FINAL-SCRIPT.md"
    - "Old script versions archived in _old-versions/ subfolder"
    - "Project numbers are unique (no duplicates)"

key-files:
  created:
    - .planning/phases/01-file-cleanup/USER-REVIEW-NEEDED.md
  modified:
    - video-projects/_IN_PRODUCTION/6-bir-tawil-2025/FINAL-SCRIPT.md (renamed from SCRIPT-V4-FINAL.md)
    - video-projects/_IN_PRODUCTION/9-communism-definition-2025/FINAL-SCRIPT.md
    - video-projects/_IN_PRODUCTION/10-dark-ages-2025/FINAL-SCRIPT.md
    - video-projects/_IN_PRODUCTION/11-industrial-revolution-2025/FINAL-SCRIPT.md
    - video-projects/_IN_PRODUCTION/13-belize-icj-endgame-2025/FINAL-SCRIPT.md
  renamed:
    - 4-christmas-origins-2025 -> 23-christmas-origins-2025
    - 22-iran-1953-coup-2025 -> 24-iran-1953-coup-2025
    - 22-iran-protests-history-2025 -> 25-iran-protests-history-2025
    - czechoslovakia-velvet-divorce-2025 -> 26-czechoslovakia-velvet-divorce-2025
    - PERU -> 27-peru-2025
    - vance-part-2-review -> 28-vance-part-2-review-2025
    - research-session-autonomous -> 29-format-research-2025
  deleted:
    - 22-guadalupe-hidalgo-2025 (empty duplicate of 20-)
    - Multiple old script versions (moved to _old-versions/)

key-decisions:
  - "Renumber christmas-origins from 4 to 23 (newer project)"
  - "Keep crusades-fact-check as 4 (older, established)"
  - "Delete empty 22-guadalupe-hidalgo-2025 (20- has content)"
  - "Library folder flagged for manual review (728 files with mixed personal/research)"

patterns-established:
  - "All project folders match [number]-[topic]-[year] regex"
  - "No duplicate project numbers allowed"
  - "Script consolidation: FINAL-SCRIPT.md only, others in _old-versions/"

# Metrics
duration: 7min
completed: 2026-01-20
---

# Phase 1 Plan 04: Naming Conventions Summary

**Enforced [number]-[topic]-[year] naming across all 28 project folders, consolidated scripts to single FINAL-SCRIPT.md per project, created user review list for library cleanup**

## Performance

- **Duration:** 7 min
- **Started:** 2026-01-20T17:15:10Z
- **Completed:** 2026-01-20T17:22:38Z
- **Tasks:** 3/3

## Accomplishments

- All project folders now follow `^[0-9]+-[a-z0-9-]+-[0-9]{4}$` pattern
- Fixed duplicate project numbers (4 and 22 were duplicated)
- Added missing number prefixes to 4 folders
- Consolidated scripts: each project has exactly one FINAL-SCRIPT.md
- Old script versions preserved in `_old-versions/` subfolders
- Library folder cleanup documented for manual user review

## Task Commits

Each task was committed atomically:

1. **Task 1: Consolidate script versions** - `641eb9a` (chore)
   - 6 projects now have single FINAL-SCRIPT.md
   - Old versions archived in _old-versions/
   - Net removal of 21 files

2. **Task 2: Fix folder naming convention** - `c603455` (chore)
   - 7 folders renamed to match convention
   - 1 empty duplicate folder deleted
   - Fixed duplicate numbers 4 and 22
   - 79 files affected

3. **Task 3: Document conventions and create user review list** - `37074eb` (docs)
   - Created USER-REVIEW-NEEDED.md
   - Verified FOLDER-STRUCTURE-GUIDE.md accuracy
   - Documented library cleanup items

## Folder Renaming Reference

| Old Name | New Name | Reason |
|----------|----------|--------|
| 4-christmas-origins-2025 | 23-christmas-origins-2025 | Fix duplicate #4 |
| 22-iran-1953-coup-2025 | 24-iran-1953-coup-2025 | Fix triplicate #22 |
| 22-iran-protests-history-2025 | 25-iran-protests-history-2025 | Fix triplicate #22 |
| czechoslovakia-velvet-divorce-2025 | 26-czechoslovakia-velvet-divorce-2025 | Missing number |
| PERU | 27-peru-2025 | ALL CAPS, missing number/year |
| vance-part-2-review | 28-vance-part-2-review-2025 | Missing number/year |
| research-session-autonomous | 29-format-research-2025 | Missing number/year |
| 22-guadalupe-hidalgo-2025 | (deleted) | Empty duplicate of #20 |

## Script Consolidation Reference

| Project | Canonical Script | Archived to _old-versions/ |
|---------|-----------------|---------------------------|
| 6-bir-tawil-2025 | FINAL-SCRIPT.md (was SCRIPT-V4-FINAL.md) | V1, V2, V3-FINAL, V4.3-CONVERSATIONAL, SCRIPT-DRAFT-V1 |
| 9-communism-definition-2025 | FINAL-SCRIPT.md | FINAL-SCRIPT-V2-EDITED.md |
| 10-dark-ages-2025 | FINAL-SCRIPT.md | FINAL-SCRIPT-V2-EDITED.md |
| 11-industrial-revolution-2025 | FINAL-SCRIPT.md | FINAL-SCRIPT-V2-REVISED.md |
| 13-belize-icj-endgame-2025 | FINAL-SCRIPT.md | V1, V2 (V3 deleted) |
| 28-vance-part-2-review-2025 | FINAL-SCRIPT.md | 4 old script versions |

## Decisions Made

| Decision | Rationale |
|----------|-----------|
| Keep 4-crusades as #4, renumber christmas-origins | Crusades is older project (Nov), christmas is newer (Dec) |
| Delete 22-guadalupe-hidalgo-2025 | Empty folder; 20-guadalupe-hidalgo-2025 has all content |
| Library cleanup is manual | 728 files with personal/research mix; too risky for automation |
| Next available number is 30 | Numbers 1-13, 14-21, 23-29 now in use |

## Deviations from Plan

### Additional Issues Found

**1. [Rule 1 - Bug] Found additional folder naming violations**
- **Found during:** Task 2 investigation
- **Issue:** Plan mentioned 9 violations; found 4 additional unnumbered folders
- **Fix:** Applied same fix (add number prefix) to research-session-autonomous
- **Impact:** More complete cleanup

**2. [Rule 1 - Bug] Number 4 was also duplicated (not just 22)**
- **Found during:** Task 2 investigation
- **Issue:** Plan only mentioned 22 triplicate; 4 was also duplicated
- **Fix:** Renumbered 4-christmas-origins to 23
- **Impact:** All duplicate numbers resolved

### Plan Accuracy Notes

The research phase correctly identified violations but some script consolidation was already done in working directory before plan execution (uncommitted changes). Task 1 committed these existing changes rather than redoing the work.

## Issues Encountered

None - all file operations completed successfully.

## Next Phase Readiness

- All project folders follow naming convention
- All projects have single canonical FINAL-SCRIPT.md
- FOLDER-STRUCTURE-GUIDE.md is accurate and current
- Library cleanup flagged for user manual review
- Ready for Phase 02 (Style Consolidation)

## Current Project Number Allocation

Numbers in use: 1-13, 14-21, 23-29
Gap: 22 (was removed - duplicate)
Next available: 30

---
*Phase: 01-file-cleanup*
*Completed: 2026-01-20*
