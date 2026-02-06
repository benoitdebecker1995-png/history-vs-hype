---
phase: 28-pacing-analysis
plan: 02
subsystem: script-quality
tags: [cli, config, output-formatting, pacing, textstat]

# Dependency graph
requires:
  - phase: 28-01
    provides: PacingChecker engine with scoring, sparklines, flat zones
provides:
  - CLI integration: --pacing flag for standalone pacing analysis
  - Config integration: 7 pacing thresholds in config.py dataclass
  - Output formatting: format_pacing_report() with problems-only default and verbose mode
  - Exit code mapping: FAIL=2, NEEDS WORK=1, PASS=0
affects: [users running script-checkers CLI, future checker additions]

# Tech tracking
tech-stack:
  added: []
  patterns: [problems-only default output, verbose flag for full breakdown, checker-specific output routing]

key-files:
  created: []
  modified:
    - tools/script-checkers/config.py
    - tools/script-checkers/cli.py
    - tools/script-checkers/output.py

key-decisions:
  - "Problems-only default: pacing report shows only flagged sections unless --verbose passed"
  - "Standalone vs. appended: pacing-only run uses pacing format exclusively, mixed runs append pacing to standard report"
  - "Exit code mapping: pacing verdict (PASS/NEEDS WORK/FAIL) maps to standard exit codes (0/1/2)"
  - "Verdict-first layout: verdict and energy arc displayed before section details for immediate go/no-go"
  - "Advisories separate from scores: hook and B-roll advisories shown as separate section, not included in composite score"

patterns-established:
  - "Checker-specific output: specialized formatters for checkers with unique report structures"
  - "Verbose mode pattern: --verbose flag for detailed breakdowns without changing default behavior"
  - "Config threshold access: all thresholds stored in Config dataclass, accessed via getattr() with defaults"

# Metrics
duration: 4min
completed: 2026-02-06
---

# Phase 28 Plan 02: Config Integration Summary

**CLI integration complete: --pacing flag produces problems-only report by default, --verbose shows full metrics table, exit codes map to verdicts**

## Performance

- **Duration:** 4 min
- **Started:** 2026-02-06T22:34:00Z
- **Completed:** 2026-02-06T22:38:56Z
- **Tasks:** 2
- **Files modified:** 3

## Accomplishments
- Pacing thresholds added to config.py (7 fields: variance, delta, density, pass/fail cutoffs, flat zone window/tolerance)
- CLI --pacing flag execution with textstat import guard and RuntimeError handling
- format_pacing_report() method with problems-only default and verbose full-breakdown mode
- Exit code integration: pacing verdicts map to standard codes (FAIL=2, NEEDS WORK=1, PASS=0)
- Help text updated with --pacing and --verbose flag documentation

## Task Commits

Each task was committed atomically:

1. **Task 1: Add pacing thresholds to config.py and register PacingChecker** - `29e3ad2` (feat)
2. **Task 2: Add --pacing flag to CLI and pacing output formatting** - `3fbd267` (feat)

## Files Created/Modified
- `tools/script-checkers/config.py` - Added 7 pacing threshold fields to Config dataclass
- `tools/script-checkers/cli.py` - Added --pacing/--verbose flags, run_checkers() pacing execution, exit code mapping, output routing
- `tools/script-checkers/output.py` - Added format_pacing_report() with problems-only and verbose modes

## Decisions Made

**Problems-only default output:**
- Default `--pacing` shows only flagged sections (score < 75)
- `--pacing --verbose` shows full section-by-section metrics table
- Rationale: users want quick go/no-go, detailed breakdown optional

**Standalone vs. appended output routing:**
- Single-checker run (`--pacing` alone): use pacing format exclusively
- Multi-checker run (`--all` or mixed flags): append pacing report after standard report
- Rationale: pacing has unique report structure incompatible with generic summary format

**Exit code mapping:**
- Pacing verdict determines exit code independently of other checkers
- FAIL verdict → exit 2 (errors)
- NEEDS WORK verdict → exit 1 (warnings)
- PASS verdict → exit 0 (no issues)
- Rationale: pacing verdict is authoritative go/no-go signal for filming decision

**Verdict-first layout:**
- Verdict and energy arc shown before section details
- Allows user to see outcome immediately without scrolling
- Rationale: filming decision should be visible in first 2 lines

**Advisories separate from scores:**
- Hook and B-roll advisories in separate "Advisories" section
- Not included in composite score or flagged section count
- Rationale: advisories are suggestions, not blockers (consistent with Plan 01 design)

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

**Python 3.14 compatibility limitation (documented, not blocking):**
- spaCy 3.8 depends on Pydantic v1 which is incompatible with Python 3.14
- Pacing checker works on Python 3.11-3.13
- Issue already documented in STATE.md from Plan 01
- Not a blocker: production environment can use Python 3.13
- Static verification confirms all code structure is correct

## User Setup Required

None - no external service configuration required.

Users running pacing checker need:
- Python 3.11-3.13 (not 3.14)
- textstat library: `pip install textstat`
- spaCy + en_core_web_sm model: `python -m spacy download en_core_web_sm`

## Next Phase Readiness

**CLI integration complete:**
- Users can run `python cli.py script.md --pacing` for problems-only report
- Users can run `python cli.py script.md --pacing --verbose` for full breakdown
- Users can run `python cli.py script.md --all` to include pacing with other checkers
- Exit codes reflect pacing verdict for CI/CD integration

**Ready for Phase 29 (Thumbnail & Title Tracking):**
- Script quality tooling complete
- Focus shifts to Click & Keep (CTR optimization)
- No blockers

**Patterns established for future checkers:**
- Checker-specific output formatters (when generic summary insufficient)
- Problems-only default with --verbose override
- Config threshold pattern (dataclass fields with getattr defaults)
- Exit code integration for checker verdicts

## Self-Check: PASSED

All modified files exist:
- tools/script-checkers/config.py
- tools/script-checkers/cli.py
- tools/script-checkers/output.py

All commits exist:
- 29e3ad2 (Task 1)
- 3fbd267 (Task 2)

---
*Phase: 28-pacing-analysis*
*Completed: 2026-02-06*
