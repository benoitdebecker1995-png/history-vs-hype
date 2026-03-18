---
phase: 69-hook-quality-upgrade
plan: "01"
subsystem: hook-scorer
tags: [hook-scorer, tdd, framework-detection, title-fulfillment, style-recommendation]
dependency_graph:
  requires: []
  provides: [tools.research.hook_scorer.score_hook, tools.research.hook_scorer.rank_hooks, tools.research.hook_scorer.format_hook_ranking, tools.research.hook_scorer.detect_topic_from_script]
  affects: [/script --hooks (Plan 02), script-writer-v2 Rule 19]
tech_stack:
  added: []
  patterns: [Document Reveal framework detection, entity echo fulfillment check, pattern library runtime parsing, confidence-based score modifier]
key_files:
  created:
    - tests/unit/test_hook_scorer.py
    - tools/research/hook_scorer.py
  modified: []
decisions:
  - "Framework detection: binary full/partial scoring (anomaly: 15 strong / 10 weak, stakes: tiered by hit count, inciting: 10/7/0)"
  - "Fulfillment check is pass/fail display only — not added to 100-point total_score (per Research pitfall #2)"
  - "Style score modifier: +5 match / -5 mismatch only at HIGH confidence (7+ examples); advisory-only at <5 examples"
  - "Entity extraction: EntityExtractor with regex fallback for title entities"
  - "Pattern library: graceful empty-dict return when file missing"
metrics:
  duration_minutes: 5
  completed_date: "2026-03-18"
  tasks_completed: 2
  files_created: 2
  files_modified: 0
  tests_added: 31
  tests_passing: 31
requirements_satisfied: [HOOK-01, HOOK-02]
---

# Phase 69 Plan 01: Hook Quality Upgrade — Scorer Summary

**One-liner:** Document Reveal framework detection (anomaly/stakes/inciting_incident) replaces 4-beat scoring; title-fulfillment check with entity echo + promise-type alignment; topic-type style recommendation from HOOK-PATTERN-LIBRARY.md with confidence-based scoring.

## What Was Built

### Task 1: TDD RED — Failing Tests
Created `tests/unit/test_hook_scorer.py` with 31 test methods across 6 test classes. Tests were written against the planned interface before implementation, confirming RED phase failures against the old code.

Test classes:
- `TestFrameworkDetection` — anomaly/stakes/inciting_incident detection, framework/beats key replacement
- `TestFulfillmentCheck` — entity echo pass/fail, promise-type match/mismatch, fix suggestion generation
- `TestScoreHook` — backward compat, no-title/no-topic skips, score range validation
- `TestStyleRecommendation` — topic-to-style mapping, confidence levels, score modifiers
- `TestFormatHookRanking` — Framework column, not Beats column
- `TestDetectTopicFromScript` — keyword-based topic detection

### Task 2: TDD GREEN — Implementation

**Part A: _detect_framework()** replaces `_detect_beats()`:
- `anomaly` (0-15): specific 3-4 digit number, document keyword, or named entity in first 30 words
- `stakes` (0-15): tiered scoring by hit count of consequence language ("which meant", "entire", "million", "empire", etc.)
- `inciting_incident` (0-10): pivot language ("but", "except", "the problem was", "here's what") in first 112 words
- Result dict: `framework_score` (not `beat_score`), `framework` dict (not `beats`)

**Part B: _check_fulfillment()** — runs when `title` provided:
- Entity echo: `EntityExtractor(use_spacy=False).extract(title)` with fallback capitalized-word extraction; checks first 50 words of hook
- Promise-type: classifies title as `conflict/document/myth-bust/mechanism` by keyword; verifies hook opening delivers same type
- Fix suggestion: names the specific gap and provides actionable rewrite guidance
- Added to result as `fulfillment` key — not scored in the 100-point total

**Part C: _load_pattern_library()** — parses `.claude/REFERENCE/HOOK-PATTERN-LIBRARY.md`:
- Splits by `## Pattern:` delimiter
- Extracts topic types, first-sentence examples, counts
- Confidence: `high` (7+), `medium` (5-6), `low` (<5)
- Graceful empty dict if file missing

**Part D: score_hook() signature upgrade**:
- New signature: `score_hook(text, label='', title=None, topic_type=None)`
- All new params default None (backward compatible)
- When `title` provided: adds `fulfillment` key
- When `topic_type` provided: adds `style_recommendation` key + applies score modifier
- `format_hook_ranking()` updated: Framework column instead of Beats
- `rank_hooks()` passes `title` and `topic_type` through

**Part E: detect_topic_from_script()**:
- Keyword-matching against first 2000 chars of script
- Returns `territorial`, `ideological`, `political_fact_check`, or `general`
- Same TOPIC_KEYWORDS pattern as Phase 67 title_scorer.py
- Exported for Plan 02 (`/script --hooks`)

## Verification

All plan verification criteria passed:
1. `pytest tests/unit/test_hook_scorer.py` — 31 passed
2. `pytest tests/` — 0 new failures (8 pre-existing failures in unrelated test files unchanged)
3. Backward compat: `score_hook('test text here' * 10)` → valid 0-100 score, `framework` key present, `beats` key absent
4. Fulfillment: `score_hook(hook, title='Spain vs Portugal...')` → shows entity echo + promise type
5. Style: `score_hook(hook, topic_type='territorial')` → `style_recommendation.recommended == 'cold_fact'`

## Deviations from Plan

None — plan executed exactly as written.

## Commits

| Task | Commit | Message |
|------|--------|---------|
| Task 1 (RED) | 8b1bdab | test(69-01): add failing tests for upgraded hook scorer framework detection, fulfillment, style |
| Task 2 (GREEN) | 7cf94c1 | feat(69-01): upgrade hook_scorer with framework detection, fulfillment check, style recommendation |

## Self-Check: PASSED

- `tests/unit/test_hook_scorer.py` exists and has 31 tests
- `tools/research/hook_scorer.py` exists with all exported functions
- Commits 8b1bdab and 7cf94c1 confirmed in git log
- Full test suite: 31 new tests pass, 0 regressions
