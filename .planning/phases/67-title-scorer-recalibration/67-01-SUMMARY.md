---
phase: 67-title-scorer-recalibration
plan: 01
subsystem: tools
tags: [title-scorer, benchmark, niche-data, tdd, recalibration]
requirements: [BENCH-01, BENCH-02, BENCH-03]
dependency_graph:
  requires: [channel-data/niche_benchmark.json, tools/title_ctr_store.py, tools/youtube_analytics/performance.py]
  provides: [tools/benchmark_store.py, tools/title_scorer.py (recalibrated)]
  affects: [tools/preflight/scorer.py, .claude/commands/preflight.md, any caller of score_title()]
tech_stack:
  added: []
  patterns: [TDD red-green, sentinel object pattern for optional param disambiguation, lazy imports for circular-import avoidance]
key_files:
  created:
    - tools/benchmark_store.py
    - tests/unit/test_benchmark_store.py
    - tests/unit/test_title_scorer_niche.py
  modified:
    - tools/title_scorer.py
    - tests/unit/test_title_scorer_db.py
decisions:
  - "Colon hard-reject kept despite niche colon VPS 0.776: inflated by Knowing Better/Kraut pipe-style titles, own-channel penalty is -28.1% CTR (HIGH confidence)"
  - "Sentinel object used in get_niche_score(data=_SENTINEL) to distinguish 'not passed' from 'None passed as failed load result'"
  - "_OWN_CHANNEL_MIN_SAMPLE=5: niche substitution triggers only when own-channel n < 5"
  - "Grade thresholds intentionally recalibrated: general pass=60/good=70 vs old pass=50/good=65 (raises bar to niche standard)"
  - "niche_enriched=True only when niche substitution happens; niche_base_score key always present for informational context"
metrics:
  duration: "7 minutes"
  completed_date: "2026-03-17"
  tasks_completed: 2
  files_changed: 5
---

# Phase 67 Plan 01: Benchmark Store + Score Title Recalibration Summary

**One-liner:** Created `benchmark_store.py` as the niche data interface and recalibrated `score_title()` with topic-type grade thresholds, small-sample niche fallback, and niche percentile labels — breaking the self-referential low-CTR calibration loop.

## What Was Built

### Task 1: benchmark_store.py

New module `tools/benchmark_store.py` provides a single clean interface to `channel-data/niche_benchmark.json`:

- `load(path=None)` — reads JSON, returns dict or None, never raises
- `get_niche_score(pattern, data=_SENTINEL)` — VPS-to-score conversion (`int(vps * 115)`) with LOW-confidence guard (versus n=1 correctly returns None)
- `TOPIC_GRADE_THRESHOLDS` — per-topic pass/good targets: territorial 50/65, ideological 60/70, political_fact_check 75/85, general 60/70
- `get_topic_thresholds(topic_type)` — returns thresholds with general fallback
- `normalize_topic_type(t)` — maps performance.py 8-type taxonomy to niche 3+1 taxonomy

### Task 2: score_title() recalibration

Modified `tools/title_scorer.py` `score_title()` with new `topic_type` parameter:

- **Topic auto-detection**: calls `classify_topic_type()` from `performance.py` then normalizes
- **Small-sample fallback (BENCH-02)**: when `db_path` provided AND own-channel n < 5 AND niche data available, substitutes niche benchmark as base score + sets `fallback_warning`
- **Topic-aware grades (BENCH-03)**: grade thresholds driven by topic type (territorial B=65, political_fact_check B=85)
- **Niche percentile label (BENCH-01)**: compares final score against niche median per pattern ("top third of niche", "above niche median", etc.)
- 6 new return dict keys added (no existing keys renamed)

### Verification results

```
68 passed in 1.64s (test_benchmark_store.py + test_title_scorer_niche.py)
12 passed in 1.71s (test_title_scorer_db.py — existing tests, updated)
```

Manual spot check confirms BENCH-03:
```
"France Divided Haiti" --topic territorial    → 65/100 (B)
"France Divided Haiti" --topic political_fact_check → 65/100 (D) + gap message
```

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Existing test_title_scorer_db.py tests used n=3 expecting db_enriched=True**

- **Found during:** Task 2 GREEN implementation
- **Issue:** Three tests in `test_title_scorer_db.py` created 3 own-channel samples and expected `db_enriched=True`. With the new `_OWN_CHANNEL_MIN_SAMPLE=5` threshold, n=3 now correctly triggers niche fallback (BENCH-02), setting `db_enriched=False`.
- **Fix:** Updated those 3 tests to use `n_declarative=5` (meets new threshold). One test's assertion relaxed to check `db_enriched is False` without asserting the specific base score (consistent with invalid-path static fallback behavior).
- **Files modified:** `tests/unit/test_title_scorer_db.py`
- **Commit:** 24c5e50

**2. [Rule 1 - Bug] get_niche_score(data=None) auto-loaded from real file when None was passed**

- **Found during:** Task 1 GREEN testing
- **Issue:** Test `test_returns_none_when_data_is_none` passed `data=None` expecting None, but the function auto-loaded the real benchmark file (which exists), returning a score.
- **Fix:** Used sentinel object `_SENTINEL = object()` to distinguish "not passed" (trigger auto-load) from "explicitly passed None" (treat as failed load). Test updated to pass `load(missing_path)` result as an explicit None rather than testing raw None.
- **Files modified:** `tools/benchmark_store.py`, `tests/unit/test_benchmark_store.py`
- **Commit:** 5c995fb

## Self-Check

Files created/modified:
- `tools/benchmark_store.py` — EXISTS
- `tools/title_scorer.py` — EXISTS (modified)
- `tests/unit/test_benchmark_store.py` — EXISTS
- `tests/unit/test_title_scorer_niche.py` — EXISTS
- `tests/unit/test_title_scorer_db.py` — EXISTS (modified)

Commits:
- 105d3ec — test(67-01): add failing tests for benchmark_store
- 5c995fb — feat(67-01): create benchmark_store.py with niche benchmark interface
- 8ffc09e — test(67-01): add failing tests for score_title() niche integration
- 24c5e50 — feat(67-01): recalibrate score_title() with niche layer, topic types, small-sample fallback

## Self-Check: PASSED
