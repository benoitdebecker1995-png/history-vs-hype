---
phase: 68-title-generation-upgrade
plan: "01"
subsystem: tools/production
tags: [title-generation, material-extraction, versus-detection, scoring, tdd]
dependency_graph:
  requires:
    - tools/production/entities.py (EntityExtractor)
    - tools/production/parser.py (ScriptParser, Section, strip_for_teleprompter)
    - tools/title_scorer.py (score_title)
  provides:
    - tools/production/title_generator.py (TitleMaterialExtractor, TitleCandidateGenerator, detect_versus_signal, generate_title_candidates)
  affects:
    - Phase 68 plan 02 (publish command integration)
tech_stack:
  added: []
  patterns:
    - TDD (RED -> GREEN, 18 unit tests)
    - Position-weighted entity accumulation (intro=2x, conclusion=1.5x, body=1x)
    - Co-occurrence window scoring for versus signal detection
    - Supplementary regex document extraction for "Treaty of X" patterns
key_files:
  created:
    - tools/production/title_generator.py
    - tests/unit/test_title_generator.py
  modified: []
decisions:
  - "Supplementary _extract_named_documents() added to catch 'Treaty of X' patterns that entities.py misses due to its suffix-based regex (e.g., 'Treaty of Utrecht' not matched without year)"
  - "detect_versus_signal uses 100-word co-occurrence window with CONFLICT_MARKERS list, score = hits/3.0 capped at 1.0"
  - "SRT extraction uses first/last 20% heuristic for position weighting (no real section boundaries available)"
  - "All candidates auto-scored via score_title(); unit tests mock score_title to avoid DB/benchmark dependency"
metrics:
  duration: "~35 minutes"
  completed_date: "2026-03-18"
  tasks_completed: 1
  tasks_total: 1
  files_created: 2
  files_modified: 0
  tests_added: 18
  tests_passing: 18
---

# Phase 68 Plan 01: Title Generation Engine Summary

**One-liner:** Script-grounded title engine with SRT support, versus auto-detection via conflict co-occurrence, and candidate generation with auto-scoring via score_title().

## What Was Built

`tools/production/title_generator.py` — a new module with four public exports:

**TitleMaterialExtractor**
- `extract_from_sections(sections)` — Scans all script sections, applying position weights (intro=2.0, conclusion=1.5, body=1.0) to entity/number/document/contradiction extraction. Merges entities by normalized key, accumulating weighted scores.
- `extract_from_srt(srt_path_or_text)` — Strips SRT sequence numbers, timestamps, and HTML tags; applies positional heuristic (first/last 20% = intro/conclusion weight) to create synthetic sections.
- `_extract_named_documents()` — Supplementary pass for "Treaty of X" and "Proper Noun + document keyword" patterns that entities.py misses.
- `_extract_numbers_with_context()` — Range percentages (10-15%), single percentages (42%), plain integers; skips years (1000-2099).
- `_extract_contradictions()` — Regex for "contrary to popular belief", "in fact/reality", "actually", "the myth", etc. Returns (myth_phrase, reality_phrase) pairs.

**detect_versus_signal(entities, full_text)**
- Module-level function. Checks top-6 entity pairs (place/person/org) for co-occurrence within 100-word windows alongside CONFLICT_MARKERS. Score = hits/3.0 capped at 1.0.

**TitleCandidateGenerator**
- `generate(material, versus_signal, topic_type, db_path)` — Always produces declarative variant; adds how_why when documents/contradictions present; adds versus when signal_strength > 0; adds curiosity/paradox when contradictions exist. Each candidate merged with full score_title() result dict.

**generate_title_candidates(sections, srt_text, topic_type, db_path)**
- Orchestration function: extract -> detect_versus -> generate -> sort by score descending.

## Tests

18 unit tests in `tests/unit/test_title_generator.py`:
- Number extraction (with/without year skipping)
- Document extraction ("Treaty of Utrecht")
- Contradiction extraction (negation patterns)
- SRT input (sequence/timestamp stripping, material types)
- Position weighting (intro entity outweighs body entity)
- Versus detection (strong signal, weak signal, empty entities)
- Candidate generation (declarative always present, all candidates scored, versus when signal, no versus without signal, max 70 char titles)
- Convenience function (sections input, SRT input, sorted output)

All 18 tests pass. score_title() mocked in tests to avoid DB/benchmark_store dependencies.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Supplementary document extraction for "Treaty of X" patterns**
- **Found during:** Task 1 (GREEN phase, first test run)
- **Issue:** entities.py `_extract_documents()` uses a suffix-based regex requiring the document keyword at the end of the name (e.g., "British Somaliland Independence Act 1960"). "Treaty of Utrecht" (keyword at start, proper name after "of") returned zero document entities.
- **Fix:** Added `_extract_named_documents()` private method handling both "keyword of ProperName" and "ProperName keyword" patterns. Called inside `extract_from_sections()` after entity extractor, creating synthetic Entity objects added to doc_acc.
- **Files modified:** tools/production/title_generator.py
- **Commit:** c1792bc

## Self-Check

Files created:
- `tools/production/title_generator.py` — exists
- `tests/unit/test_title_generator.py` — exists

Commits:
- c1792bc — feat(68-01): create title generation engine with material extractor and candidate generator

## Self-Check: PASSED
