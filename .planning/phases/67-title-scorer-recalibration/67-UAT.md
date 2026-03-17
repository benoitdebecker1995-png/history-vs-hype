---
status: complete
phase: 67-title-scorer-recalibration
source: [67-01-SUMMARY.md, 67-02-SUMMARY.md]
started: 2026-03-17T12:00:00Z
updated: 2026-03-17T12:30:00Z
---

## Current Test

[testing complete]

## Tests

### 1. Basic title scoring still works
expected: Run `python -m tools.title_scorer "The Pope Who Split the World"` — returns a score, grade, and pattern detection without errors.
result: pass

### 2. --topic flag changes grade thresholds
expected: Run with --topic territorial then --topic political_fact_check. Same title gets different grades — territorial passes easier (B at 65) while political_fact_check requires 85 for B.
result: pass

### 3. Niche percentile label appears on Score line
expected: Score line includes a niche context label like "above niche median" or "below niche median" after the grade.
result: pass

### 4. Niche fallback warning when few own-channel samples
expected: When own-channel has <5 examples for the pattern, output shows a Notice line about using niche benchmark.
result: pass

### 5. format_result() backward compatibility
expected: Run without --db flag. Output is clean with no errors — static fallback works as before.
result: pass

### 6. Existing tests pass
expected: Run all 80 tests across test_benchmark_store.py, test_title_scorer_niche.py, test_title_scorer_db.py — all pass.
result: pass

## Summary

total: 6
passed: 6
issues: 0
pending: 0
skipped: 0

## Gaps

[none]
