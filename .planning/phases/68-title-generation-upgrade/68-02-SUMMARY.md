---
phase: 68-title-generation-upgrade
plan: "02"
subsystem: tools/production
tags: [title-generation, metadata, output-format, scoring, tdd]
dependency_graph:
  requires: ["68-01"]
  provides: ["format_title_candidates", "metadata-ranked-output"]
  affects: ["tools/production/metadata.py", "tools/production/title_generator.py"]
tech_stack:
  added: []
  patterns: ["ranked-table-output", "delegation-pattern", "deprecation-marker"]
key_files:
  created: []
  modified:
    - tools/production/title_generator.py
    - tools/production/metadata.py
    - tests/unit/test_title_generator.py
decisions:
  - "format_title_candidates() appends warning lines below table (not inline) to preserve table parse-ability"
  - "MetadataGenerator._db_path auto-resolves to tools/discovery/keywords.db at __init__ time using absolute path"
  - "TitleVariant dataclass kept with deprecation docstring for backward compatibility; not removed"
  - "Warning format: newline prefix then '[warning] #N penalized: reason' — matches CONTEXT.md output spec"
metrics:
  duration: "~8 minutes"
  completed: "2026-03-18T11:25:31Z"
  tasks_completed: 1
  files_modified: 3
---

# Phase 68 Plan 02: Title Generation Integration Summary

Wired `format_title_candidates()` into `metadata.py`, replacing the fixed A/B/C table with a ranked scored output driven by the full-script extraction engine from plan 01.

## What Was Built

### format_title_candidates() — title_generator.py

New module-level function added after `generate_title_candidates()`:

- Sorts candidates by score descending (enforced even if already sorted)
- Renders `## Title Candidates (ranked by score)` header + markdown table with columns: `# | Title | Score | Grade | Pattern`
- Appends `[warning] #N penalized: reason` lines below the table for every `hard_rejects` entry
- All candidates shown — none silently dropped (user decision from Phase 68 CONTEXT)

### metadata.py changes

1. Import: `from .title_generator import generate_title_candidates, format_title_candidates`
2. `MetadataGenerator.__init__`: accepts optional `db_path`; auto-resolves to `tools/discovery/keywords.db` if present
3. `_generate_title_variants()`: replaced 100-line A/B/C generator with single `generate_title_candidates()` call; returns `list[dict]` instead of `list[TitleVariant]`
4. `generate_metadata_draft()`: calls `format_title_candidates(title_candidates)` and embeds result directly; removed old table loop and "Test A vs B first" recommendation line
5. `TitleVariant` dataclass: marked deprecated in docstring, not deleted

### Tests added (5 new in TestFormatTitleCandidates)

- `test_format_ranked_table`: header + table columns + rank-1 is highest scorer
- `test_penalized_candidates_show_warning`: hard_rejects appear as warning lines
- `test_all_candidates_shown`: all 5 candidates visible including 2 penalized
- `test_year_candidate_ranked_last`: low-score candidate in table after high-score one
- `test_output_replaces_abc`: `generate_metadata_draft` output has "Title Candidates", not "Title A/B/C Test Variants"

## Test Results

- Plan 01 tests: 18 passed (unchanged)
- Plan 02 tests: 5 passed (new)
- Total title_generator suite: 23 passed
- Full suite: 275 passed, 8 pre-existing failures (test_intel, test_pacing, test_ctr_tracker — not related to this plan)

## Deviations from Plan

None - plan executed exactly as written.

## Self-Check

- [x] `tools/production/title_generator.py` — format_title_candidates() added
- [x] `tools/production/metadata.py` — imports wired, _generate_title_variants delegated, A/B/C removed
- [x] `tests/unit/test_title_generator.py` — 5 new tests
- [x] Commit e6fadfa exists

## Self-Check: PASSED
