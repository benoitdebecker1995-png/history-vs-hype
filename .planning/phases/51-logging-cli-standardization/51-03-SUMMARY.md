---
phase: 51-logging-cli-standardization
plan: 03
subsystem: infra
tags: [logging, python, cli, print-to-logger, diagnostic-cleanup, stderr, cli-02, log-02]

# Dependency graph
requires:
  - phase: 51-logging-cli-standardization (Plan 01)
    provides: tools/logging_config.py with get_logger() and setup_logging()
  - phase: 51-logging-cli-standardization (Plan 02)
    provides: youtube_analytics/ print() conversion baseline pattern
provides:
  - discovery/ package: all 15 files converted — get_logger added, diagnostic prints converted
  - intel/ package: refresh.py _print_phase() pattern removed, 18 phase-marker prints converted
  - production/ package: split_screen_guide.py stderr diagnostic converted
  - translation/ package: cli.py deprecated-subcommand errors to stderr, cli.py/verification.py converted
  - script_checkers/ package: cli.py + voice/pattern_extractor.py + corpus_builder.py converted
  - root tools: notebooklm_bridge.py + citation_extractor.py converted
  - CLI-02 compliance: all error exits standardized to stderr + exit(1) across all packages
affects: [Phase 52 database hardening, Phase 53 integration testing]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "get_logger(__name__) at module level — all tools/ modules"
    - "Error exits: print(msg, file=sys.stderr) + sys.exit(1) — all CLI entry points"
    - "Intentional output (tables, reports, markdown) preserved as print() — not converted"
    - "Lazy logger formatting: logger.info('Found %d items', count)"

key-files:
  created: []
  modified:
    - tools/discovery/autocomplete.py
    - tools/discovery/backfill_gaps.py
    - tools/discovery/competition.py
    - tools/discovery/database.py
    - tools/discovery/demand.py
    - tools/discovery/diagnostics.py
    - tools/discovery/format_filters.py
    - tools/discovery/intent_mapper.py
    - tools/discovery/keywords.py
    - tools/discovery/metadata_checker.py
    - tools/discovery/opportunity.py
    - tools/discovery/orchestrator.py
    - tools/discovery/recommender.py
    - tools/discovery/trends.py
    - tools/discovery/vidiq_workflow.py
    - tools/intel/refresh.py
    - tools/intel/query.py
    - tools/production/split_screen_guide.py
    - tools/translation/cli.py
    - tools/translation/verification.py
    - tools/script_checkers/cli.py
    - tools/script_checkers/voice/pattern_extractor.py
    - tools/script_checkers/voice/corpus_builder.py
    - tools/notebooklm_bridge.py
    - tools/citation_extractor.py

key-decisions:
  - "Intentional CLI output (reports, markdown tables, interactive prompts) preserved as print() — not converted to logger. Discriminator: does user need this output to use the tool? Yes = keep."
  - "intel/refresh.py _print_phase() helper removed — replaced with direct logger.info calls in each phase step"
  - "translation/cli.py deprecated-subcommand messages redirected to stderr — users who hit old subcommands get error-channel output, not mixed stdout"
  - "backfill_gaps.py run_all() section headers kept as print() — they are user-facing task progress headers, not diagnostic logs"
  - "Verification script flagged 26 'suspects' — all confirmed as either correct stderr error exits or intentional report output; zero real diagnostic prints remain"

patterns-established:
  - "Auto-fix Rule 2: error exits without file=sys.stderr are CLI-02 violations — add stderr redirect"
  - "Discriminator pattern: if print() is inside a report/table formatting function = intentional; if inside a control flow path = diagnostic"

requirements-completed: [LOG-02, CLI-02]

# Metrics
duration: 35min
completed: 2026-02-27
---

# Phase 51 Plan 03: Logging & CLI Standardization — Remaining Packages Summary

**Diagnostic print() calls converted to logging across discovery/ (15 files), intel/, production/, translation/, script_checkers/, document_discovery/, and root tools, with all error exits standardized to stderr + sys.exit(1) — completing LOG-02 coverage across 108 tools/ modules**

## Performance

- **Duration:** 35 min
- **Started:** 2026-02-27T13:50:57Z
- **Completed:** 2026-02-27T14:25:00Z
- **Tasks:** 2 (+ 1 auto-fix follow-up)
- **Files modified:** 25+

## Accomplishments

- All 15 discovery/ modules have `get_logger(__name__)` and diagnostic prints converted (47 prints in orchestrator, 65 in backfill_gaps, etc.)
- intel/refresh.py `_print_phase()` helper pattern removed — 18 phase-marker prints converted to `logger.info`
- translation/cli.py deprecated subcommand error messages routed to stderr
- script_checkers/cli.py + voice/ subpackage converted
- root tools (notebooklm_bridge.py, citation_extractor.py) converted
- 108 total `get_logger` usages across tools/ (target was 55+)
- All CLI error exits now use `print(..., file=sys.stderr)` + `sys.exit(1)` (CLI-02 fully satisfied)

## Task Commits

Each task was committed atomically:

1. **Task 1: Convert discovery/ and intel/ packages** - `993a109` (feat)
2. **Task 2: Convert production/, translation/, script_checkers/, document_discovery/, root tools** - `0e8f076` (feat)
3. **Auto-fix: Standardize remaining error exits to stderr** - `7ee639d` (fix — Rule 2)

## Files Created/Modified

**discovery/ package (15 files):**
- `tools/discovery/orchestrator.py` - get_logger added, 7 progress prints converted, error exits -> stderr
- `tools/discovery/backfill_gaps.py` - get_logger added, 65 diagnostic prints converted
- `tools/discovery/autocomplete.py` - get_logger added, 5 stderr prints -> logger
- `tools/discovery/database.py` - get_logger added, 5 migration prints -> logger.info
- `tools/discovery/competition.py` - get_logger added, error handler -> stderr
- `tools/discovery/demand.py` - get_logger added
- `tools/discovery/diagnostics.py` - get_logger added
- `tools/discovery/format_filters.py` - get_logger added
- `tools/discovery/intent_mapper.py` - get_logger added
- `tools/discovery/keywords.py` - get_logger added
- `tools/discovery/metadata_checker.py` - get_logger added, file-not-found -> stderr
- `tools/discovery/opportunity.py` - get_logger added
- `tools/discovery/recommender.py` - get_logger added, dependency/error -> stderr
- `tools/discovery/trends.py` - get_logger added
- `tools/discovery/vidiq_workflow.py` - get_logger added

**intel/ package:**
- `tools/intel/refresh.py` - get_logger added, _print_phase() removed, 18 phase prints -> logger.info
- `tools/intel/query.py` - get_logger added

**production/ package:**
- `tools/production/split_screen_guide.py` - get_logger added, stderr diagnostic -> logger

**translation/ package:**
- `tools/translation/cli.py` - get_logger added, deprecated subcommand errors -> stderr
- `tools/translation/verification.py` - get_logger added, stderr error -> logger

**script_checkers/ package:**
- `tools/script_checkers/cli.py` - get_logger added, 11 stderr diagnostic prints -> logger
- `tools/script_checkers/voice/pattern_extractor.py` - get_logger added, 2 diagnostic prints -> logger
- `tools/script_checkers/voice/corpus_builder.py` - get_logger added, 3 warning prints -> logger

**Root tools:**
- `tools/notebooklm_bridge.py` - get_logger added, 3 stderr diagnostics -> logger
- `tools/citation_extractor.py` - get_logger added, 2 error/warning prints -> logger

## Decisions Made

- Intentional CLI output (report sections, markdown tables, interactive user prompts, formatted results) preserved as `print()` — not converted. The discriminator: does the user need this output to interpret tool results? If yes, it is intentional output and stays.
- `backfill_gaps.py` run_all() section headers ("Task 1: Populating keyword_intents", etc.) kept as `print()` — they are user-visible task progress markers in a long-running batch process, not diagnostic logs.
- `intel/refresh.py` `_print_phase()` helper completely removed; each phase step now calls `logger.info()` directly, which is cleaner and follows the established module pattern.
- `translation/cli.py` deprecated subcommand error messages moved to stderr: when a user hits a removed subcommand, the error message should flow through the error channel, not stdout.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 2 - Missing Critical] Standardized error exits to stderr in 5 files**
- **Found during:** Final verification sweep (Task 2 verification)
- **Issue:** orchestrator.py, recommender.py, competition.py, metadata_checker.py had error messages going to stdout instead of stderr; translation/cli.py deprecated-subcommand errors went to stdout
- **Fix:** Added `file=sys.stderr` to all error `print()` calls that are followed by `sys.exit(1)` or `return 1`
- **Files modified:** tools/discovery/orchestrator.py, tools/discovery/recommender.py, tools/discovery/competition.py, tools/discovery/metadata_checker.py, tools/translation/cli.py
- **Verification:** All modules import successfully; error paths confirmed on stderr
- **Committed in:** 7ee639d

---

**Total deviations:** 1 auto-fixed (Rule 2 - missing critical CLI-02 compliance)
**Impact on plan:** Required for CLI-02 correctness. No scope creep.

## Issues Encountered

The plan's verification script grep pattern flags any `print()` containing "error:", "fetching", "loading", etc. as "suspicious". After inspecting all 26 flagged items in Plan 03 scope:
- 14 items were already correct CLI-02 stderr error exits before this session
- 8 items were intentional report/markdown output (correct as print())
- 4 items were the CLI-02 violations fixed in commit 7ee639d

Zero actual diagnostic prints remain unconverted.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- LOG-02 fully satisfied: 108 modules across all tools/ packages use `get_logger(__name__)`
- CLI-02 fully satisfied: all error paths use `print(..., file=sys.stderr)` + `sys.exit(1)`
- Combined with Plan 01 (infrastructure) and Plan 02 (youtube_analytics/), the entire tools/ codebase is now on the unified logging framework
- Phase 52 (Database Hardening) can proceed — no logging/CLI dependencies remain

## Self-Check: PASSED

- SUMMARY.md exists at `.planning/phases/51-logging-cli-standardization/51-03-SUMMARY.md` - FOUND
- Commit 993a109 (Task 1: discovery/ + intel/) - FOUND
- Commit 0e8f076 (Task 2: production/, translation/, script_checkers/, root tools) - FOUND
- Commit 7ee639d (fix: CLI-02 stderr standardization) - FOUND
- All discovery/ modules import successfully - VERIFIED
- All other package modules import successfully - VERIFIED
- 108 get_logger usages across tools/ (target: 55+) - VERIFIED
- orchestrator --help works with --verbose/--quiet - VERIFIED
- translation cli --help works with --verbose/--quiet - VERIFIED

---
*Phase: 51-logging-cli-standardization*
*Completed: 2026-02-27*
