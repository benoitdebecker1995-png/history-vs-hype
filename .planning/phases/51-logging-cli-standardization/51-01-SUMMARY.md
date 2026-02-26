---
phase: 51-logging-cli-standardization
plan: "01"
subsystem: tools
tags: [logging, cli, argparse, standardization, infrastructure]
dependency_graph:
  requires: []
  provides: [tools/logging_config.py, argparse-cli-standard]
  affects: [all-tool-cli-entry-points, tools/__init__.py]
tech_stack:
  added: [logging_config.py]
  patterns: [argparse-mutually-exclusive-group, NullHandler-library-safety, tools-logger-hierarchy]
key_files:
  created:
    - tools/logging_config.py
  modified:
    - tools/__init__.py
    - tools/youtube_analytics/channel_averages.py
    - tools/youtube_analytics/comments.py
    - tools/youtube_analytics/ctr.py
    - tools/youtube_analytics/metrics.py
    - tools/youtube_analytics/retention.py
    - tools/youtube_analytics/video_report.py
    - tools/youtube_analytics/analyze.py
    - tools/youtube_analytics/feedback_parser.py
    - tools/youtube_analytics/patterns.py
    - tools/youtube_analytics/backfill.py
    - tools/youtube_analytics/benchmarks.py
    - tools/youtube_analytics/feedback.py
    - tools/youtube_analytics/performance.py
    - tools/youtube_analytics/topic_strategy.py
    - tools/youtube_analytics/technique_library.py
    - tools/youtube_analytics/playbook_synthesizer.py
    - tools/youtube_analytics/pattern_synthesizer_v2.py
    - tools/youtube_analytics/retention_scorer.py
    - tools/youtube_analytics/transcript_analyzer.py
    - tools/youtube_analytics/variants.py
    - tools/discovery/autocomplete.py
    - tools/discovery/backfill_gaps.py
    - tools/discovery/competition.py
    - tools/discovery/demand.py
    - tools/discovery/diagnostics.py
    - tools/discovery/format_filters.py
    - tools/discovery/intent_mapper.py
    - tools/discovery/keywords.py
    - tools/discovery/metadata_checker.py
    - tools/discovery/orchestrator.py
    - tools/discovery/recommender.py
    - tools/discovery/vidiq_workflow.py
    - tools/document_discovery/cli.py
    - tools/translation/cli.py
    - tools/translation/verification.py
    - tools/production/parser.py
    - tools/production/split_screen_guide.py
    - tools/script_checkers/cli.py
    - tools/citation_extractor.py
    - tools/notebooklm_bridge.py
decisions:
  - "Configure logging.getLogger('tools') not root logger — library-safe hierarchy"
  - "NullHandler in tools/__init__.py prevents 'No handlers' warnings when used as library"
  - "Mutually exclusive --verbose/-v and --quiet/-q group replaces standalone --verbose flags"
  - "setup_logging() called in __main__ blocks only, never at module import time"
  - "editguide.py, metadata.py, query.py excluded — smoke-test __main__ blocks, not real CLIs"
metrics:
  duration_minutes: 245
  tasks_completed: 2
  files_created: 1
  files_modified: 40
  completed_date: "2026-02-26"
---

# Phase 51 Plan 01: Logging Infrastructure and CLI Standardization Summary

**One-liner:** Shared `logging_config.py` with `setup_logging(verbose, quiet)` wired into all 40 CLI entry points via argparse mutually exclusive verbosity flags, replacing 12 manual sys.argv parsers.

---

## Tasks Completed

| Task | Name | Commit | Files |
|------|------|--------|-------|
| 1 | Create logging_config.py and update tools/__init__.py | 1941697 | tools/logging_config.py, tools/__init__.py |
| 2 | Convert sys.argv to argparse + add --verbose/--quiet to all CLIs | 7adf1b4 | 40 files across tools/ |

---

## What Was Built

### Task 1: Shared Logging Infrastructure

Created `tools/logging_config.py` with:

- `setup_logging(verbose, quiet)` — configures `logging.getLogger("tools")` (not root logger) with stderr StreamHandler; quiet=ERROR, default=INFO, verbose=DEBUG levels; ANSI color support via `_ColorFormatter` with colorama on TTY-detected terminals; `propagate = False` to prevent root logger pollution
- `get_logger(name)` — thin wrapper returning `logging.getLogger(name)` for module-level logger creation
- `_ColorFormatter` — ANSI color codes per level (cyan/green/yellow/red/bold-red), uses `logging.makeLogRecord(record.__dict__)` to avoid mutating original record

Updated `tools/__init__.py` with `logging.getLogger("tools").addHandler(logging.NullHandler())` for library-safe import — prevents "No handlers could be found for logger 'tools'" warnings when tools/ is imported as a library.

### Task 2: CLI Standardization Across 40 Entry Points

**Part A — Converted 12 sys.argv files to argparse:**

- `channel_averages.py` — loop-based argv parsing → argparse with `--compare`, `--last-n`
- `comments.py` — loop-based argv → argparse with `video_id`, `--limit`, `--quality`
- `ctr.py` — manual argv → argparse with `video_id`, `--start-date`, `--end-date`
- `metrics.py` — loop-based argv → argparse with `video_id`, `--start-date`
- `retention.py` — index-based argv → argparse with `video_id`
- `video_report.py` — manual argv → argparse with `video_id`, `--json`/`--markdown` format group
- `analyze.py` — extensive 7-flag argv → argparse with all flags preserved
- `feedback_parser.py` — mixed argparse+argv → clean argparse with positional `target`
- `patterns.py` — mixed argparse+argv → clean argparse with `--monthly nargs="*"`
- `diagnostics.py` — mixed argparse+argv → pure argparse
- `intent_mapper.py` — sys.argv[1] check → argparse with `--batch QUERIES`
- `parser.py` — sys.argv manipulation → argparse using `arg_parser` variable to avoid shadowing `parser = ScriptParser()`

**Part B — Added --verbose/--quiet to all 40 CLI entry points:**

Every file with a real argparse-based CLI got:
```python
verbosity = parser.add_mutually_exclusive_group()
verbosity.add_argument("--verbose", "-v", action="store_true", help="Show debug output on stderr")
verbosity.add_argument("--quiet", "-q", action="store_true", help="Only show errors on stderr")
```

And after `args = parser.parse_args()`:
```python
from tools.logging_config import setup_logging
setup_logging(args.verbose, args.quiet)
```

---

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking Issue] Fixed bare relative imports in 5 youtube_analytics files**
- **Found during:** Task 2 verification (--help test suite)
- **Issue:** `channel_averages.py`, `comments.py`, `ctr.py`, `metrics.py`, `retention.py` all used `from auth import get_authenticated_service` — works when invoked as `python channel_averages.py` but fails as `python -m tools.youtube_analytics.channel_averages` (Phase 48 standard invocation pattern)
- **Fix:** Changed all 5 files to use absolute path `from tools.youtube_analytics.auth import get_authenticated_service`; also wrapped `from googleapiclient.errors import HttpError` in `retention.py` with try/except
- **Files modified:** channel_averages.py, comments.py, ctr.py, metrics.py, retention.py
- **Commit:** 7adf1b4

**2. [Rule 1 - Bug] Fixed UnicodeEncodeError in pattern_synthesizer_v2.py help text**
- **Found during:** Task 2 verification (--help test on Windows cp1252 terminal)
- **Issue:** Arrow character `→` in argparse help string caused `UnicodeEncodeError: 'charmap' codec can't encode character '\u2192'` on Windows default console encoding
- **Fix:** Changed `→` to `->` in the `--synthesize` argument help string
- **Files modified:** tools/youtube_analytics/pattern_synthesizer_v2.py
- **Commit:** 7adf1b4

**3. [Rule 2 - Missing Critical Functionality] Added missing setup_logging() call in script_checkers/cli.py**
- **Found during:** Task 2 verification
- **Issue:** Previous session had added the mutually exclusive group but forgot to wire `setup_logging()` after `args = parser.parse_args()`
- **Fix:** Added the `setup_logging(args.verbose, args.quiet)` call
- **Files modified:** tools/script_checkers/cli.py
- **Commit:** 7adf1b4

### Scope Decisions

- **3 files excluded from argparse conversion:** `intel/query.py`, `production/editguide.py`, `production/metadata.py` — their `__main__` blocks are dev smoke-tests (single print statement), not real CLI entry points per plan guidance
- **`arg_parser` variable name** used in `production/parser.py` to avoid shadowing the `parser = ScriptParser()` business logic object

---

## Verification Results

All success criteria confirmed post-commit:

| Check | Result |
|-------|--------|
| sys.argv in __main__ blocks | 0 violations |
| mutually_exclusive_group count | 40 files (matches CLI entry point count) |
| `from tools.logging_config import setup_logging, get_logger` | OK |
| NullHandler on tools logger | OK |
| Sample --help tests (metrics, channel_averages, orchestrator) | ALL PASSED |

---

## Decisions Made

1. **Configure `logging.getLogger("tools")` not root logger** — library-safe hierarchy; all `tools.*` child loggers inherit via propagation automatically
2. **NullHandler in tools/__init__.py** — prevents "No handlers" warnings when the package is imported by external code or tests
3. **Mutually exclusive group replaces standalone --verbose** — files that already had `-v`/`--verbose` (competition.py, demand.py, format_filters.py, script_checkers/cli.py) had their flag replaced with the mutually exclusive group while preserving the `args.verbose` attribute name so existing business logic continues unchanged
4. **setup_logging() in __main__ only** — never at module import time; logging is a CLI concern, not a library concern
5. **editguide.py, metadata.py, query.py excluded** — smoke-test `__main__` blocks with no user arguments are not CLI entry points

---

## Self-Check: PASSED

Files verified to exist:
- tools/logging_config.py: FOUND
- tools/__init__.py: FOUND (contains NullHandler)

Commits verified to exist:
- 1941697 (Task 1): FOUND
- 7adf1b4 (Task 2): FOUND
