---
phase: 48-package-structure-dependencies
plan: 03
subsystem: infra
tags: [python-packaging, pyproject-toml, hatchling, pip, dependencies]

# Dependency graph
requires:
  - phase: 48-01
    provides: "youtube_analytics/ and script_checkers/ directories renamed to underscore form (correct Python package names)"
provides:
  - "pyproject.toml at repo root — single source of dependency truth"
  - "pip install -e . installs google-api-python-client + anthropic (core deps)"
  - "pip install -e .[youtube,intel,nlp,discovery,translation,thumbnails,dev,test,all] installs feature groups"
  - "tools/discovery/requirements.txt deleted"
  - "tools/youtube_analytics/requirements.txt deleted"
  - "tools/script_checkers/requirements.txt deleted"
affects:
  - 53-integration-testing (test extras group provides pytest + pytest-cov)
  - 49-dead-code-cleanup (can rely on pyproject.toml as canonical dep list)

# Tech tracking
tech-stack:
  added:
    - "hatchling (build backend for pyproject.toml)"
  patterns:
    - "Single root pyproject.toml pattern: one file declares all deps for all tools"
    - "Extras groups by feature: [youtube], [intel], [nlp], [discovery], [translation], [thumbnails]"
    - "pip install -e . for core deps only; pip install -e .[group] for optional features"

key-files:
  created:
    - pyproject.toml
  modified: []
  deleted:
    - tools/discovery/requirements.txt
    - tools/youtube_analytics/requirements.txt
    - tools/script_checkers/requirements.txt

key-decisions:
  - "Used trendspyg (not trendspy) — confirmed from actual import in tools/discovery/trends.py docstring"
  - "Core deps (google-api + anthropic) hardcoded in [project].dependencies (no feature flag)"
  - "youtube extras group duplicates core google-api deps (explicit group definition per plan spec)"
  - "tools/history-clip-tool/requirements.txt untouched — standalone tool, explicitly out of scope"
  - "hatchling chosen as build backend (per plan spec — lightweight, modern, no setup.py)"

patterns-established:
  - "pyproject.toml is the single source of dependency truth — no per-package requirements.txt"
  - "Extras groups match feature flags: [intel] for feedparser, [nlp] for spacy/textstat, etc."

requirements-completed: [DEP-01, DEP-02, DEP-03]

# Metrics
duration: 4min
completed: 2026-02-24
---

# Phase 48 Plan 03: Package Structure & Dependencies Summary

**Root pyproject.toml with 8 extras groups replaces 3 per-package requirements.txt files, making `pip install -e .` the single onboarding command**

## Performance

- **Duration:** 4 min
- **Started:** 2026-02-24T23:28:09Z
- **Completed:** 2026-02-24T23:32:00Z
- **Tasks:** 2
- **Files modified:** 4 (1 created, 3 deleted)

## Accomplishments

- Created `pyproject.toml` at repo root with name `history-vs-hype-tools`, version `5.1.0`, `python_requires >= "3.11"`
- Defined 8 optional extras groups: youtube, intel, nlp, discovery, translation, thumbnails, dev, test, plus all-in-one `[all]`
- Deleted three per-package requirements.txt files that pyproject.toml now supersedes
- Verified `pip install -e . --dry-run` and `pip install -e .[dev,test] --dry-run` both succeed without error

## Task Commits

Each task was committed atomically:

1. **Task 1: Create root pyproject.toml with all dependencies** - `c82db03` (chore)
2. **Task 2: Delete per-package requirements.txt files and validate install** - `a380c34` (chore)

## Files Created/Modified

**Created:**
- `pyproject.toml` - Single source of truth for all dependencies (core + 8 optional extras groups)

**Deleted:**
- `tools/discovery/requirements.txt` - Superseded by pyproject.toml [discovery] group
- `tools/youtube_analytics/requirements.txt` - Superseded by pyproject.toml [youtube] group
- `tools/script_checkers/requirements.txt` - Superseded by pyproject.toml [nlp] group

**Unchanged (intentional):**
- `tools/history-clip-tool/requirements.txt` - Standalone tool, explicitly out of scope per audit

## Decisions Made

- Confirmed `trendspyg` as the correct pip package name by reading the actual import and docstring in `tools/discovery/trends.py` ("pip install trendspyg") — the plan noted this needed verification and correctly suspected the package name differed from the import name
- Used hatchling as build backend per plan spec (lightweight, no setup.py needed)
- Core dependencies kept minimal in `[project].dependencies`: only google-api-python-client and anthropic (both unconditionally required)
- tools/history-clip-tool/requirements.txt left untouched per explicit plan instruction

## Deviations from Plan

None - plan executed exactly as written. Package name `trendspyg` was pre-flagged in the plan as requiring verification; confirmed and used correctly.

## Issues Encountered

None - pyproject.toml parsed correctly on first write, dry-run validation passed immediately.

## User Setup Required

None - no external service configuration required. Developers can now run `pip install -e .` from repo root instead of per-directory requirements.txt installs.

## Next Phase Readiness

- Phase 49 (Dead Code Cleanup) can proceed: pyproject.toml is stable reference for dependency audit
- Phase 53 (Integration Testing) dependency declared: `pip install -e .[test]` installs pytest + pytest-cov
- All three requirements requirements DEP-01, DEP-02, DEP-03 fulfilled

---
*Phase: 48-package-structure-dependencies*
*Completed: 2026-02-24*

## Self-Check: PASSED

| Check | Result |
|-------|--------|
| pyproject.toml at repo root | FOUND |
| tools/discovery/requirements.txt | GONE |
| tools/youtube_analytics/requirements.txt | GONE |
| tools/script_checkers/requirements.txt | GONE |
| tools/history-clip-tool/requirements.txt | FOUND (untouched, correct) |
| 48-03-SUMMARY.md | FOUND |
| commit c82db03 (Task 1) | FOUND |
| commit a380c34 (Task 2) | FOUND |
