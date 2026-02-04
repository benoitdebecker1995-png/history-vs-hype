---
phase: 24-edit-guide-generation
plan: 01
subsystem: production-tools
tags: [python, script-parser, timing-calculation, edit-guide, markdown-generation]

# Dependency graph
requires:
  - phase: 22-script-parser-entity-detection
    provides: ScriptParser, EntityExtractor, Section, Entity dataclasses
  - phase: 23-b-roll-generation
    provides: BRollGenerator, Shot dataclass with section_references
provides:
  - EditGuideGenerator class with timing-aware edit guide generation
  - Duration calculation at 150 WPM with 10-second minimum
  - Cumulative timing sheet generation
  - Shot-by-shot breakdown matching EDITING-GUIDE.md format
  - Visual assets checklist by priority
  - CLI --edit-guide flag for instant guide generation
affects: [25-filming-certification, 26-post-production-tools]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "150 WPM timing calculation as standard for video estimation"
    - "Cumulative timing with MM:SS formatting"
    - "Section-to-shot mapping via section_references"
    - "UTF-8 encoding for Windows console output"

key-files:
  created:
    - tools/production/editguide.py
  modified:
    - tools/production/__init__.py
    - tools/production/parser.py

key-decisions:
  - "150 WPM as standard speech rate (industry standard for video timing)"
  - "10-second minimum for very short sections (prevents unrealistic estimates)"
  - "MM:SS format for timing (matches video editing software conventions)"
  - "UTF-8 stdout encoding on Windows (handles unicode checkmarks in output)"

patterns-established:
  - "SectionTiming dataclass tracks cumulative start/end times for each section"
  - "Shot-by-shot breakdown groups shots by section for logical flow"
  - "Visual assets checklist auto-generated from shot priorities"

# Metrics
duration: 4min
completed: 2026-02-04
---

# Phase 24 Plan 01: Edit Guide Generation Summary

**Timing-aware edit guide generator producing EDITING-GUIDE.md format from parsed scripts in <30 seconds via CLI**

## Performance

- **Duration:** 4 min
- **Started:** 2026-02-04T18:53:39Z
- **Completed:** 2026-02-04T19:04:18Z
- **Tasks:** 3
- **Files modified:** 3

## Accomplishments
- EditGuideGenerator class generates complete EDITING-GUIDE.md matching existing format
- Duration calculation at 150 WPM with 10-second minimum for accuracy
- Cumulative timing sheet with MM:SS formatted start/end times per section
- Shot-by-shot breakdown grouping B-roll and talking head entries by section
- Visual assets checklist auto-generated from shot priorities
- CLI integration via `--edit-guide` flag for instant generation
- Integration tested with Chagos script: 91 shots, 10:53 runtime, 12 sections

## Task Commits

Each task was committed atomically:

1. **Task 1: Create EditGuideGenerator with timing calculation** - `e7d38fd` (feat)
2. **Task 2: Update module exports and CLI integration** - `89039c1` (feat)
3. **Task 3: Integration test with existing script** - `09591e2` (fix)

## Files Created/Modified
- `tools/production/editguide.py` - EditGuideGenerator class with timing calculation, shot breakdown generation, and EDITING-GUIDE.md formatting
- `tools/production/__init__.py` - Export EditGuideGenerator and SectionTiming
- `tools/production/parser.py` - Add --edit-guide CLI flag, UTF-8 encoding for Windows

## Decisions Made

**1. 150 WPM as timing standard**
- Industry standard speaking rate for video narration
- Matches existing manual timing estimates
- Verified: 150 words = 60 sec, 300 words = 120 sec

**2. 10-second minimum for short sections**
- Prevents unrealistic sub-10-second estimates for brief transitions
- Matches real-world speaking pace with pauses

**3. UTF-8 encoding for Windows console**
- Required to handle unicode characters (✅) in output
- Prevents UnicodeEncodeError when printing to stdout
- Platform-specific encoding setup on Windows only

**4. Section-to-shot mapping via section_references**
- Uses existing BRollGenerator section_references field
- Enables logical grouping of shots within sections
- Maintains shot context from Phase 23

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] UTF-8 encoding error on Windows console**
- **Found during:** Task 3 (Integration test)
- **Issue:** UnicodeEncodeError when printing edit guide with unicode checkmarks to Windows console
- **Fix:** Added platform-specific UTF-8 encoding setup for stdout on Windows
- **Files modified:** tools/production/parser.py
- **Verification:** Edit guide prints successfully with all unicode characters
- **Committed in:** 09591e2 (Task 3 commit)

---

**Total deviations:** 1 auto-fixed (1 blocking)
**Impact on plan:** Essential fix for Windows compatibility. No scope creep.

## Issues Encountered
- Initial integration test failed due to incorrect script filename (expected 02-SCRIPT-DRAFT.md, actual SCRIPT.md) - resolved by checking actual files with Glob
- Unicode encoding error on Windows - resolved with platform-specific UTF-8 stdout setup

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

**Ready for Phase 25 (Filming Certification):**
- Edit guide generation provides timing estimates for filming preparation
- Shot-by-shot breakdown guides camera work and B-roll planning
- Visual assets checklist ensures all materials ready before filming

**Ready for Phase 26 (Post-Production Tools):**
- Edit guide format matches existing EDITING-GUIDE.md structure
- Timing calculations accurate at 150 WPM for editing timeline
- Shot markers enable automated editing workflow tools

**Integration verified:**
- Chagos script: 91 shots generated, 10:53 total runtime
- 12 sections with cumulative timing
- Visual assets by priority (Priority 2, 3 detected)
- Quality checklist template included

**No blockers or concerns.**

---
*Phase: 24-edit-guide-generation*
*Completed: 2026-02-04*
