---
phase: 67-title-scorer-recalibration
plan: 02
subsystem: tools
tags: [title-scorer, preflight, niche-display, format, cli]
requirements: [BENCH-01, BENCH-02, BENCH-03]
dependency_graph:
  requires: [tools/benchmark_store.py, tools/title_scorer.py (recalibrated from Plan 01)]
  provides: [tools/title_scorer.py (updated format_result + --topic flag), tools/preflight/scorer.py (niche context propagation)]
  affects: [/greenlight title gate output, any direct CLI usage of title_scorer]
tech_stack:
  added: []
  patterns: [graceful .get() defaults for backward compatibility, try/except fallback in preflight]
key_files:
  created: []
  modified:
    - tools/title_scorer.py
    - tools/preflight/scorer.py
decisions:
  - "Topic line only shown when gap_message present (grade below B) — cleaner output, no noise for passing titles"
  - "Source line uses clean labels: 'niche benchmark (competitor data)' vs 'DB-enriched (base score from live CTR data)'"
  - "Notice: prefix used for fallback_warning line to distinguish from Penalty/Bonus lines"
  - "format_result() uses .get() throughout — old result dicts from pre-Phase-67 code paths produce clean output"
  - "topic_type normalized via benchmark_store before passing to score_title() in preflight"
metrics:
  duration: "5 minutes"
  completed_date: "2026-03-17"
  tasks_completed: 2
  files_changed: 2
---

# Phase 67 Plan 02: Niche Display + Preflight Integration Summary

**One-liner:** Wired niche percentile labels into format_result() Score line and CLI output, added --topic flag, and propagated niche context through preflight/scorer.py so /greenlight title gate surfaces benchmark data.

## What Was Built

### Task 1: format_result() and CLI updates (tools/title_scorer.py)

Modified `format_result()` to surface Plan 01's new result keys in clean readable output:

- **Score line with niche label (BENCH-01):** `Score: 65/100 (B) — above niche median`
- **Topic/gap line (BENCH-03):** Only shown when grade is C/D/F — `Topic: political_fact_check — needs score 85+ for B (currently 65)`. Hidden when grade A/B (no gap to show).
- **Source line:** Clean labels — `niche benchmark (competitor data)` vs `DB-enriched (base score from live CTR data)` vs static fallback.
- **Notice line (BENCH-02):** `Notice: Using niche benchmark (only N internal examples, need 5)` — shown only when niche fallback active.
- **Backward compatibility:** All `.get()` calls with defaults — old result dicts (missing Phase 67 keys) produce clean output.

Added `--topic` CLI flag:
- Already present in CLI from Plan 01 implementation (noted in code comments)
- Verified working: `python -m tools.title_scorer "Title" --db --topic territorial`
- CLI header updates to: `TITLE SCORER — History vs Hype (DB-enriched), topic: territorial`

### Task 2: Preflight niche context propagation (tools/preflight/scorer.py)

Modified `_score_title_metadata()` to propagate niche context into `notes`:

- **topic_type normalization:** Normalizes via `benchmark_store.normalize_topic_type()` before passing to `score_title()` — unifies the 8-type classify_topic_type() taxonomy with the 3+1 niche taxonomy.
- **Niche notes (BENCH-01):** `Niche position: above niche median` added to notes when label present.
- **Fallback warning (BENCH-02):** `Using niche benchmark (only N internal examples...)` added to notes when substitution active.
- **Gap message (BENCH-03):** `Topic target: territorial topics need score 65+ for B (currently 51)` added to notes when grade below B.
- **Fallback preserved:** `_classify_title_pattern()` fallback intact when `score_title()` unavailable.

### Verification results

```
68 passed in 1.27s (test_benchmark_store.py + test_title_scorer_niche.py — unchanged)
```

CLI spot checks:
```
"France Divided Haiti" --topic territorial
  Score:   65/100 (B) — above niche median   ← BENCH-01

"France Divided Haiti" --topic political_fact_check
  Score:   65/100 (D) — above niche median
  Topic:   political_fact_check — political_fact_check topics need score 85+ for B (currently 65)  ← BENCH-03
```

Preflight integration assertion:
```python
r = _score_title_metadata('', ['France Divided Haiti'], 'territorial')
# notes: ['Niche position: below niche median', 'Topic target: territorial topics need...']
# PASS: niche context found in notes
```

## Deviations from Plan

None — plan executed exactly as written.

The `--topic` CLI flag was already present from Plan 01 (the CLI section was already updated). Task 1 correctly focused on `format_result()` output format and the CLI header update.

## Self-Check

Files modified:
- `tools/title_scorer.py` — EXISTS
- `tools/preflight/scorer.py` — EXISTS

Commits:
- b168beb — feat(67-02): update format_result() with niche display and --topic flag
- 2611cbc — feat(67-02): propagate niche context through preflight/scorer.py

## Self-Check: PASSED
