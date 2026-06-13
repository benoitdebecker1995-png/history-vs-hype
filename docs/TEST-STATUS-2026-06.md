# Test-Suite Status + Calibration-Tool Gaps — 2026-06-12

> **UPGRADE-PLAN T2.** Full-suite run, failure triage, and a coverage-gap list for the three calibration-relevant tools. **Scope rule (per the plan):** fix only failures *caused by Phase-0 moves*; everything else is reported as a finding, not silently fixed. **Result: none of the 18 failures is Phase-0 fallout — so nothing was fixed here.** All are stale tests (behavior deliberately changed) or pre-existing design drift, documented below with the specific fix each needs.

## Run summary

```
python -m pytest tests/ tools/tests/ tools/script_checkers/tests/ -p no:cacheprovider -q
→ 18 failed, 539 passed, 13 skipped, 2 warnings in 509s (8m29s)
```

`tools/youtube_analytics/` was run **separately** (different import convention — see §C) and could not be collected.

`-p no:cacheprovider` is required on this machine: `.pytest_cache/` is not writable (WinError 5), which otherwise emits a warning every run. Cosmetic, but worth a `.gitignore`/permissions note.

## A. title_scorer failures — STALE TESTS (8) — **not Phase-0**

The scorer was deliberately re-tiered on 2026-06-11 (Fable Phase 1 "P1 scorer v5/mandate re-tier"; CLAUDE.md item 13: *"Years/colons in titles = HEDGE, not ban — graded penalties… the old -46%/-28% hard rule was topic-confounded; the channel's #1 and #3 videos have colons"*). Years/colons/"The X That" no longer hard-reject — they apply graded penalties. These tests assert the **removed** behavior:

| Test | Asserts | Now returns |
|---|---|---|
| `test_title_scorer_niche.py::TestBackwardCompatibility::test_hard_reject_year_still_works` | year ⇒ `REJECTED` | `B` |
| `…::test_hard_reject_colon_still_works` | colon ⇒ `REJECTED` | graded |
| `…::test_hard_reject_the_x_that_still_works` | "The X That" ⇒ `REJECTED` | graded |
| `…::TestTopicTypeGradeThresholds::test_hard_rejects_override_topic_type_grade` | hard-reject overrides grade | no hard reject |
| `…::test_colon_hard_reject_with_topic_type` | colon ⇒ `REJECTED` | graded |
| `test_title_scorer_db.py::TestScoreTitleDbPath::test_hard_rejects_still_apply_with_db_path` | hard reject w/ db path | graded |
| `…::test_colon_hard_reject_with_db_path` | colon ⇒ `REJECTED` w/ db | graded |
| `tools/tests/test_scorer_regression.py::test_regression_pass` | regression baseline incl. hard rejects | drift |

**Finding:** the test suite was not updated when the scorer re-tiered. The fix is a calibration decision (what *should* a year/colon title now grade?), so it belongs to a focused scorer-test refresh with the calibration owner — not a silent rewrite mid-audit. The `TestBackwardCompatibility` class name is itself now misleading: it guards backward-compat with a rule the project intentionally reversed.

## B. script_checkers pacing failures — STALE TESTS (9) — **not Phase-0**

`tools/script_checkers/checkers/pacing.py:445` returns early with `all_sections: []` for single-section input (sensible: *"pacing analysis requires multiple sections"*). The 9 failing tests feed one `## Test Section` and then index `result['all_sections'][0]` → `IndexError`. (`test_composite_score_perfect/floor/degraded`, `test_entity_density_*`, `test_sentence_variance_*`, `test_flesch_delta_first_section`, `test_broll_markers_stripped`.)

**Finding:** tests predate the single-section guard (or the parser's section-count behavior changed). `pacing.py` history shows last edits in the 48-01/48-02 refactor era + the benchmark-corpus add — no Phase-0 involvement. Fix = give each test fixture ≥2 `##` sections so the checker actually runs. Low-risk but a test-authoring change, deferred to the calibration-tool test pass (see §D).

## C. youtube_analytics — COLLECTION ERRORS (6 files) — **not Phase-0**

`python -m pytest tools/youtube_analytics/` fails collection 3 ways, all the same root cause — **inconsistent import conventions**:
- Test files use **bare** imports (`from auth import…`, `from transcript_analyzer import…`, `from pattern_synthesizer_v2 import…`) → `ModuleNotFoundError` when run from repo root.
- Run from inside the dir, the modules themselves use **relative** imports inside an `except ImportError: sys.exit(1)` guard (`pattern_synthesizer_v2.py:42-47`) → pytest `INTERNALERROR: SystemExit: 1`.

The two conventions are mutually exclusive; no invocation passes without a `conftest.py` to fix `sys.path` or normalizing the imports. The `sys.exit(1)` at import time is the aggravating factor — a library module should raise, not exit, so a missing dep degrades gracefully instead of killing the test collector.

**Finding:** pre-existing (these files predate Phase 0). Fix = add `tools/youtube_analytics/conftest.py` that inserts the dir on `sys.path`, **and** change the module import-guard from `sys.exit(1)` to re-raise. Reported, not fixed (touches 6 modules' import architecture).

## D. Calibration-tool coverage gaps

The plan's three calibration-relevant tools:

| Tool | Test files | Coverage verdict |
|---|---|---|
| `tools/voice_lint.py` (v18, 33.9 KB) | **none** | **ZERO automated tests.** 9 public scanners unguarded: `scan_patterns`, `scan_staccato`, `scan_stacked_credentials`, `scan_negation_pairs`, `scan_sentence_band`, `scan_fragment_share`, `scan_questions`, `scan_verdict_hedge`, `scan_transitions` (+ `_judge_transition`, `clean_line`, `mask_comments`, `word_count`). The canonical voice fingerprint linter has no regression net — a threshold tweak can silently change every script's lint output. **Highest-priority gap.** |
| `tools/title_scorer.py` (47 KB) | `tests/unit/test_title_scorer_db.py`, `…_niche.py`, `tools/tests/test_scorer_regression.py` | Exists but **8 tests assert removed behavior** (§A). The *new* graded-penalty behavior is **not** positively tested — no test pins "year title ⇒ grade B with penalty X." Untested: graded-penalty magnitudes, topic-type grade thresholds under the v5 tiering, db-path scoring path. |
| `tools/script_checkers/checkers/` (5 checkers) | only `test_pacing.py` (failing, §B) | **4 of 5 checkers have no tests:** `flow.py`, `repetition.py`, `scaffolding.py`, `stumble.py`. `pacing.py` has tests but they're stale. Effective automated coverage of the checker suite ≈ 0. |

## Recommendations (for a follow-up calibration-test pass — not done here)

1. **voice_lint.py regression tests first** — it's the canonical voice gate with zero coverage; bugs here silently corrupt every script lint. Pin each scanner against a known-good + known-bad fixture, with thresholds sourced from `FINGERPRINT-UNSCRIPTED.md` (the S5 quantitative data).
2. **Refresh title_scorer tests to the v5 re-tier** — delete/rewrite the `TestBackwardCompatibility` hard-reject assertions; add positive tests for the new graded grades. Requires the calibration owner to confirm target grades. Re-baseline `test_scorer_regression.py`.
3. **Fix pacing fixtures (≥2 sections) + add the 4 missing checker test files** (flow/repetition/scaffolding/stumble).
4. **youtube_analytics:** add `conftest.py` + convert `sys.exit(1)` import-guards to re-raise.
5. **Add `.pytest_cache/` to `.gitignore`** (or grant write) to kill the per-run permission warning.

All five are findings/gaps, not Phase-0 fallout — none was fixed under T2's scope.
