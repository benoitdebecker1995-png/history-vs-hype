---
phase: 46-project-dashboard
plan: 01
subsystem: dashboard
tags: [pathlib, stdlib, project-scanner, dashboard, mtime, phase-detection, intel-cross-reference]

# Dependency graph
requires:
  - phase: 43-youtube-intelligence-engine
    provides: channel-data/youtube-intelligence.md with Trending Topics table
provides:
  - tools/dashboard/project_scanner.py — scan_projects(), format_dashboard(), detect_phase(), days_since_activity(), extract_topic_slug(), extract_intel_topics()
  - tools/dashboard/__init__.py — module entry point
affects:
  - 46-02 (status.md enhancement — will import from tools/dashboard/)
  - Any future dashboard-aware command

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "All-stdlib module pattern: pathlib + time + re, no external dependencies, consistent with tools/intel/ and tools/research/"
    - "mtime-based activity detection: time.time() - st_mtime avoids timezone-aware/naive mixing"
    - "Top-level-only file scanning: iterdir() with is_file() check, no recursive walk"
    - "Intel cross-reference: direct file read of youtube-intelligence.md, line-by-line parse, graceful empty-list fallback"

key-files:
  created:
    - tools/dashboard/__init__.py
    - tools/dashboard/project_scanner.py
  modified: []

key-decisions:
  - "time.time() - st_mtime for days-since calculation: avoids timezone-aware/naive mixing on Windows (Pitfall 1 from RESEARCH.md)"
  - "Top-level files only for mtime scan: prevents _research/ subdirectory activity from inflating staleness count (Pitfall 3)"
  - "Published projects separated to footer summary, suppressed from main table: reduces noise for the 6 published-but-not-archived projects"
  - "Idea-phase suppression when >10 active non-idea projects: keeps table scannable; 15 idea projects not shown in current state"
  - "extract_intel_topics() never raises: returns empty list on missing file or any exception — consistent with prep.md/publish.md intel skip pattern"

patterns-established:
  - "Pattern: scan_projects() returns a dict with 'projects', 'ready_to_film', 'intel_topics' keys — display-ready data separation"
  - "Pattern: detect_phase() takes a set of file name strings (not Path objects) — testable without filesystem"
  - "Pattern: days_since_activity() returns 999 sentinel for unknown (no files or OSError) — never raises"

requirements-completed: [DASH-01, DASH-02, DASH-03]

# Metrics
duration: 2min
completed: 2026-02-22
---

# Phase 46 Plan 01: Project Dashboard Scanner Summary

**stdlib-only project scanner for _IN_PRODUCTION/ producing a prioritized Markdown dashboard table with phase detection, staleness flagging, and youtube-intelligence.md trending-topic cross-reference**

## Performance

- **Duration:** 2 min
- **Started:** 2026-02-22T15:01:15Z
- **Completed:** 2026-02-22T15:03:23Z
- **Tasks:** 1
- **Files modified:** 2

## Accomplishments

- scan_projects() correctly classifies all 38 _IN_PRODUCTION/ projects by phase (filming-ready, fact-checked, scripting, research, idea)
- format_dashboard() produces a scannable Markdown table sorted by priority (filming-ready first), with STALE flags for projects >14 days inactive
- Intel cross-reference reads youtube-intelligence.md Trending Topics table and matches against project slugs; gracefully skips if file missing
- Published projects (6 found) separated to footer summary line; 15 idea-phase projects suppressed from main table with count shown at bottom
- _READY_TO_FILM footer shows 1-sykes-picot-2025

## Task Commits

Each task was committed atomically:

1. **Task 1: Create tools/dashboard/ module with project_scanner.py** - `eac0761` (feat)

## Files Created/Modified

- `tools/dashboard/__init__.py` — Module docstring only (follows intel/ pattern)
- `tools/dashboard/project_scanner.py` — All dashboard logic: detect_phase(), days_since_activity(), extract_topic_slug(), extract_intel_topics(), scan_projects(), format_dashboard()

## Decisions Made

- Used `time.time() - st_mtime` instead of datetime for days-since calculation to avoid timezone-aware/naive mixing on Windows (Pitfall 1 from RESEARCH.md)
- Scan only top-level files (not recursive) to prevent subdirectory activity from inflating staleness count (Pitfall 3)
- `detect_phase()` takes `set[str]` file names rather than `Path` objects — makes unit testing trivial without filesystem
- Idea-phase projects suppressed from table when there are >10 active non-idea projects; summary count shown regardless when >5 ideas exist
- `extract_intel_topics()` wraps entire read in try/except, returns empty list — consistent with how prep.md/publish.md handle missing intel file

## Deviations from Plan

None — plan executed exactly as written. All 6 functions implemented per spec. All verifications passed.

## Issues Encountered

None. The research file accurately described all pitfalls and patterns upfront. 38 projects scanned (research mentioned ~39, which counted README files that the scanner correctly skips per Pitfall 2).

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

- tools/dashboard/ module ready for import by status.md enhancement (Phase 46, Plan 02)
- Integration call: `from tools.dashboard.project_scanner import scan_projects, format_dashboard`
- status.md should call scan_projects('.') and print(format_dashboard(data)) when invoked with no project argument

---
*Phase: 46-project-dashboard*
*Completed: 2026-02-22*
