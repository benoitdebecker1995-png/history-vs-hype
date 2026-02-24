---
phase: 48-package-structure-dependencies
plan: 01
subsystem: infra
tags: [python-packaging, imports, directory-rename, init-py]

requires: []
provides:
  - "tools/youtube_analytics/ directory (renamed from youtube-analytics/)"
  - "tools/script_checkers/ directory (renamed from script-checkers/)"
  - "tools/__init__.py (marks tools/ as Python package)"
  - "tools/youtube_analytics/__init__.py (marks youtube_analytics/ as Python package)"
  - "tools/script_checkers/__init__.py (marks script_checkers/ as Python package)"
  - "tools/script_checkers/tests/__init__.py (pytest discovery for tests/)"
  - "Zero references to hyphenated names in active codebase"
affects:
  - 48-02 (import rewrites depend on renamed directories)
  - 48-03 (pyproject.toml depends on correct package names)
  - 49-dead-code-cleanup (removing dead files from youtube_analytics/)
  - 53-integration-testing (pytest discovery needs tests/__init__.py)

tech-stack:
  added: []
  patterns:
    - "Python package structure: tools/ is now a proper package hierarchy"
    - "Module invocation: python -m tools.youtube_analytics.X (not cd + python X.py)"
    - "Empty __init__.py files: mark directories as packages, no re-exports"

key-files:
  created:
    - tools/__init__.py
    - tools/youtube_analytics/__init__.py
    - tools/script_checkers/__init__.py
    - tools/script_checkers/tests/__init__.py
  modified:
    - tools/discovery/diagnostics.py
    - tools/discovery/recommender.py
    - tools/intel/competitor_tracker.py
    - tools/intel/algo_scraper.py
    - tools/script_checkers/tests/test_pacing.py
    - tools/script_checkers/VOICE-SETUP.md
    - tools/youtube_analytics/analyze.py
    - tools/youtube_analytics/backfill.py
    - tools/youtube_analytics/feedback.py
    - tools/youtube_analytics/pattern_synthesizer_v2.py
    - tools/youtube_analytics/patterns.py
    - tools/youtube_analytics/playbook_synthesizer.py
    - tools/youtube_analytics/test_connection.py
    - tools/youtube_analytics/test_retention_scorer.py
    - .claude/commands/analyze.md
    - .claude/commands/next.md
    - .claude/commands/patterns.md
    - .claude/commands/prep.md
    - .claude/commands/publish.md
    - .claude/commands/script.md
    - .claude/REFERENCE/STYLE-GUIDE.md
    - AGENTS.md
    - channel-data/channel-insights.md
    - video-projects/_IN_PRODUCTION/31-bermeja-island-2025/YOUTUBE-METADATA.md

key-decisions:
  - "git mv used for directory renames so git tracks file history (not delete+add)"
  - "Dead files _competitor_fetch.py and _csv_backfill.py left untouched (removed in Phase 49)"
  - "Historical .planning/ docs retain old path strings (legitimate historical artifacts)"
  - "Command files updated to python -m invocation pattern (not cd + python script.py)"
  - "All __init__.py files are intentionally empty (no re-exports, always import explicitly)"

patterns-established:
  - "Invocation pattern: python -m tools.youtube_analytics.X from repo root"
  - "sys.path hacks updated to use underscore names (full cleanup in Plan 02)"

requirements-completed: [PKG-01, PKG-03]

duration: 7min
completed: 2026-02-24
---

# Phase 48 Plan 01: Package Structure & Dependencies Summary

**Renamed tools/youtube-analytics/ and tools/script-checkers/ to Python-legal underscore names via git mv, added four empty __init__.py files, and swept all 24+ active-codebase references from hyphenated to underscore path forms**

## Performance

- **Duration:** 7 min
- **Started:** 2026-02-24T23:16:51Z
- **Completed:** 2026-02-24T23:24:09Z
- **Tasks:** 2
- **Files modified:** 28

## Accomplishments

- Renamed `tools/youtube-analytics/` to `tools/youtube_analytics/` and `tools/script-checkers/` to `tools/script_checkers/` using git mv (history preserved)
- Created four empty `__init__.py` files making `tools.youtube_analytics` and `tools.script_checkers` importable as Python packages
- Swept all hyphenated path references across active codebase: 6 command files, 2 REFERENCE files, 9 youtube_analytics Python files, 3 intel/discovery Python files, 2 script_checkers files, and 3 project docs

## Task Commits

Each task was committed atomically:

1. **Task 1: Rename directories and create __init__.py files** - `b6e9cb6` (chore)
2. **Task 2: Sweep all references to old hyphenated names** - `3208fdc` (chore)

## Files Created/Modified

**Created:**
- `tools/__init__.py` - Marks tools/ as Python package (empty)
- `tools/youtube_analytics/__init__.py` - Marks youtube_analytics/ as Python package (empty)
- `tools/script_checkers/__init__.py` - Marks script_checkers/ as Python package (empty)
- `tools/script_checkers/tests/__init__.py` - Enables pytest test discovery (empty)

**Modified (Python files - functional path updates):**
- `tools/discovery/diagnostics.py` - sys.path youtube-analytics -> youtube_analytics
- `tools/discovery/recommender.py` - sys.path youtube-analytics -> youtube_analytics
- `tools/intel/competitor_tracker.py` - path variable and comment updates
- `tools/intel/algo_scraper.py` - comment update
- `tools/youtube_analytics/backfill.py` - analytics_dir path vars, docstring, auto-generated label
- `tools/youtube_analytics/feedback.py` - sys.path update
- `tools/youtube_analytics/pattern_synthesizer_v2.py` - auto-generated label
- `tools/youtube_analytics/playbook_synthesizer.py` - two auto-generated labels
- `tools/youtube_analytics/analyze.py` - comment update
- `tools/youtube_analytics/patterns.py` - comment update
- `tools/youtube_analytics/test_connection.py` - usage comment
- `tools/youtube_analytics/test_retention_scorer.py` - usage comment

**Modified (command files and docs):**
- `.claude/commands/analyze.md` - Updated to python -m invocation pattern
- `.claude/commands/next.md` - Updated performance.py invocation
- `.claude/commands/patterns.md` - Updated patterns.py and feedback.py invocations
- `.claude/commands/prep.md` - Updated to inline sys.path + python pattern
- `.claude/commands/publish.md` - Updated to inline sys.path + python pattern
- `.claude/commands/script.md` - Updated multiple invocations and path references
- `.claude/REFERENCE/STYLE-GUIDE.md` - Updated two auto-generated section labels
- `AGENTS.md` - Updated directory listing
- `channel-data/channel-insights.md` - Updated re-run command
- `tools/script_checkers/VOICE-SETUP.md` - Updated cd commands to sys.path pattern
- `tools/script_checkers/tests/test_pacing.py` - Updated usage comment and variable comment
- `video-projects/_IN_PRODUCTION/31-bermeja-island-2025/YOUTUBE-METADATA.md` - Updated variants.py invocations

## Decisions Made

- Used `git mv` for directory renames so git tracks renames as R100 (100% similarity) rather than deletes+adds - history preserved
- Dead files `_competitor_fetch.py` and `_csv_backfill.py` left with their original sys.path lines intact (per plan: removed in Phase 49)
- Historical `.planning/` documentation files retain old path strings (legitimate historical artifacts, not active code)
- Command files updated to `python -m tools.youtube_analytics.X` invocation pattern throughout
- sys.path hacks in Python files updated to use underscore names now; full replacement with proper imports deferred to Plan 02

## Deviations from Plan

None - plan executed exactly as written. Dead files excluded per plan instructions. Historical planning docs excluded as they are reference artifacts, not active code.

## Issues Encountered

- Git's rename similarity detection initially confused the empty `tools/__init__.py` with `tools/youtube-analytics/credentials/.gitkeep` (both empty files, R100 similarity match). This is cosmetic git display behavior only; all files exist correctly on disk and were committed correctly.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- Both packages are importable: `from tools import youtube_analytics` and `from tools import script_checkers` succeed from repo root
- Plan 02 (import rewrites) can now convert sys.path hacks to proper `from tools.youtube_analytics import X` absolute imports
- Plan 03 (pyproject.toml) can reference `tools.youtube_analytics` and `tools.script_checkers` as package names
- Phase 49 (dead code cleanup) can safely remove `_competitor_fetch.py` and `_csv_backfill.py`

## Self-Check: PASSED

All files and directories verified present. Both commits confirmed in git log.

| Check | Result |
|-------|--------|
| tools/__init__.py | FOUND |
| tools/youtube_analytics/__init__.py | FOUND |
| tools/script_checkers/__init__.py | FOUND |
| tools/script_checkers/tests/__init__.py | FOUND |
| tools/youtube_analytics/ directory | FOUND |
| tools/script_checkers/ directory | FOUND |
| old youtube-analytics/ directory | GONE |
| old script-checkers/ directory | GONE |
| commit b6e9cb6 (Task 1) | FOUND |
| commit 3208fdc (Task 2) | FOUND |

---
*Phase: 48-package-structure-dependencies*
*Completed: 2026-02-24*
