---
phase: 42-pipeline-hardening-research-ingestion
plan: "01"
subsystem: translation-pipeline
tags: [credentials, env-loader, smoke-test, error-handling, dx]
dependency_graph:
  requires: []
  provides:
    - tools/translation/env_loader.py
    - tools/translation/smoke_test.py
    - .env.example
  affects:
    - tools/translation/translator.py
    - tools/translation/cross_checker.py
    - tools/translation/legal_annotator.py
    - tools/translation/surprise_detector.py
    - tools/translation/verification.py
    - tools/translation/cli.py
tech_stack:
  added:
    - pure Python .env file parsing (no dotenv dependency)
  patterns:
    - env_loader: centralized credential resolution with fallback chain (.env -> os.environ)
    - wrap_api_error: duck-typed exception to actionable message converter
    - smoke_test: 5-step end-to-end validation with timing and exit codes
key_files:
  created:
    - tools/translation/env_loader.py
    - tools/translation/smoke_test.py
    - .env.example
  modified:
    - tools/translation/translator.py
    - tools/translation/cross_checker.py
    - tools/translation/legal_annotator.py
    - tools/translation/surprise_detector.py
    - tools/translation/verification.py
    - tools/translation/cli.py
decisions:
  - Pure Python .env parsing (no python-dotenv): minimizes dependencies per project conventions
  - Duck-typed exception matching in wrap_api_error: avoids anthropic import in env_loader (circular import prevention)
  - Real API calls in smoke_test: validates actual connectivity, not mocks
  - ensure_env_example() called on module import: idempotent side effect that creates template on first use
metrics:
  duration_seconds: 221
  completed_date: "2026-02-20"
  tasks_completed: 2
  tasks_total: 2
  files_created: 3
  files_modified: 6
---

# Phase 42 Plan 01: Translation Pipeline Credential Management and Smoke Test Summary

One-liner: Pure Python .env credential loader with actionable error messages and 5-step end-to-end smoke test for the translation pipeline.

## What Was Built

### Task 1: env_loader.py + All Module Updates (commit 23d53fb)

Created `tools/translation/env_loader.py` with three public functions:

- `load_api_key()` — reads `.env` file at project root (`G:/History vs Hype/.env`) using pure Python parsing. Falls back to `os.environ['ANTHROPIC_API_KEY']`. Returns `{'key': str}` on success or `{'error': str}` with step-by-step fix instructions including the exact `echo` command to add the key.
- `wrap_api_error(exception)` — converts Anthropic API exceptions to actionable messages using duck-typed class name matching (no anthropic import in env_loader). Handles AuthenticationError, RateLimitError, APIConnectionError, and generic fallback.
- `ensure_env_example()` — idempotent function that creates `.env.example` template on first import.

Updated all 5 translation modules (`translator.py`, `cross_checker.py`, `legal_annotator.py`, `surprise_detector.py`, `verification.py`) to:
- Import `load_api_key, wrap_api_error` from `env_loader`
- Replace `os.environ.get('ANTHROPIC_API_KEY')` with `load_api_key()` in `__init__`
- Wrap API call exceptions with `wrap_api_error()` instead of raw `str(e)`

Zero `os.environ.get('ANTHROPIC_API_KEY')` calls remain in any translation module.

### Task 2: smoke_test.py + CLI smoketest subcommand (commit 24b59c1)

Created `tools/translation/smoke_test.py` with 5-step validation:

1. **Credential check** — calls `load_api_key()`, shows masked key + source (.env file vs env var), fails with actionable error if missing
2. **Structure detection** — runs `StructureDetector().detect_structure()` on embedded French test document (preamble + 3 articles), verifies section_count >= 2
3. **Translation** — runs `Translator().translate_document()` with real API call, verifies non-empty translations
4. **Formatting** — runs `Formatter().format_paired()`, verifies non-empty markdown output containing `##`
5. **Pipeline integrity** — verifies section IDs flow from input to output with no translation failures

Added `smoketest` subcommand to `cli.py`:
- `python tools/translation/cli.py smoketest` runs `run_smoke_test()`
- Listed in `--help` output
- Exit code 0 on all pass, 1 on any failure

## Verification Results

All 5 plan verification criteria confirmed:

1. `load_api_key()` returns key or actionable error with fix instructions
2. Zero `os.environ.get('ANTHROPIC_API_KEY')` matches across all 5 modules
3. `.env.example` exists at project root with commented placeholder
4. `python tools/translation/cli.py smoketest` runs 5-step validation (step 1 fails gracefully without API key)
5. `python tools/translation/cli.py --help` shows `smoketest` subcommand

## Deviations from Plan

None — plan executed exactly as written.

## Decisions Made

1. **Pure Python .env parsing**: Implemented 15-line `_parse_env_file()` that handles KEY=value, comments (#), blank lines, and quoted values. No python-dotenv dependency per project convention of minimizing external dependencies.

2. **Duck-typed exception matching in wrap_api_error**: Used `type(exception).__name__` string matching instead of `isinstance()` checks. This avoids importing anthropic in env_loader.py (which would create a circular import risk) and also works if the anthropic package isn't installed.

3. **Real API calls in smoke test**: The plan explicitly requires real API calls to validate actual connectivity. The test document is a short 3-article French decree (~100 words) that generates 3-4 translation API calls.

4. **ensure_env_example() on module import**: Called at module level in env_loader.py as a non-fatal idempotent side effect. Creates the template on first import without requiring explicit initialization.

## Self-Check: PASSED

Files verified present:
- FOUND: tools/translation/env_loader.py
- FOUND: tools/translation/smoke_test.py
- FOUND: .env.example

Commits verified:
- 23d53fb: feat(42-01): add env_loader and update all translation modules
- 24b59c1: feat(42-01): add smoke_test.py and smoketest subcommand to cli.py
