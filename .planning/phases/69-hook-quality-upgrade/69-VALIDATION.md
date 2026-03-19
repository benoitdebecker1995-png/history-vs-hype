---
phase: 69
slug: hook-quality-upgrade
status: validated
nyquist_compliant: true
wave_0_complete: true
created: 2026-03-18
validated: 2026-03-18
---

# Phase 69 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest (auto-discovers unittest.TestCase) |
| **Config file** | pyproject.toml (inferred from existing test runs) |
| **Quick run command** | `python -m pytest tests/unit/test_hook_scorer.py -x -q` |
| **Full suite command** | `python -m pytest tests/ -q` |
| **Estimated runtime** | ~5 seconds |

---

## Sampling Rate

- **After every task commit:** Run `python -m pytest tests/unit/test_hook_scorer.py -x -q`
- **After every plan wave:** Run `python -m pytest tests/ -q`
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 5 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 69-01-01 | 01 | 1 | HOOK-01 | unit | `python -m pytest tests/unit/test_hook_scorer.py::TestFulfillmentCheck::test_entity_echo_pass -x` | ✅ | ✅ green |
| 69-01-02 | 01 | 1 | HOOK-01 | unit | `python -m pytest tests/unit/test_hook_scorer.py::TestFulfillmentCheck::test_entity_echo_fail -x` | ✅ | ✅ green |
| 69-01-03 | 01 | 1 | HOOK-01 | unit | `python -m pytest tests/unit/test_hook_scorer.py::TestFulfillmentCheck::test_promise_type_mismatch -x` | ✅ | ✅ green |
| 69-01-04 | 01 | 1 | HOOK-01 | unit | `python -m pytest tests/unit/test_hook_scorer.py::TestScoreHook::test_no_title_skips_fulfillment -x` | ✅ | ✅ green |
| 69-01-05 | 01 | 1 | HOOK-02 | unit | `python -m pytest tests/unit/test_hook_scorer.py::TestStyleRecommendation::test_territorial_recommends_cold_fact -x` | ✅ | ✅ green |
| 69-01-06 | 01 | 1 | HOOK-02 | unit | `python -m pytest tests/unit/test_hook_scorer.py::TestStyleRecommendation::test_ideological_recommends_myth_contradiction -x` | ✅ | ✅ green |
| 69-01-07 | 01 | 1 | HOOK-02 | unit | `python -m pytest tests/unit/test_hook_scorer.py::TestStyleRecommendation::test_low_confidence_no_score_impact -x` | ✅ | ✅ green |
| 69-01-08 | 01 | 1 | HOOK-01+02 | unit | `python -m pytest tests/unit/test_hook_scorer.py::TestScoreHook::test_backward_compat_no_title -x` | ✅ | ✅ green |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [x] `tests/unit/test_hook_scorer.py` — 31 tests covering HOOK-01 fulfillment check, HOOK-02 style recommendation, framework detection, backward compat

*Existing infrastructure covers framework and conftest: pytest, conftest.py, tests/unit/ all present and confirmed working.*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| LLM-generated hook variants are stylistically correct | HOOK-02 | LLM output is non-deterministic | Run `/script --hooks` on a territorial script, verify cold_fact variant reads naturally |
| Mismatch fix suggestion is actionable | HOOK-01 | Requires human judgment on suggestion quality | Review 3+ fail outputs, confirm fix suggestions are specific and useful |

---

## Validation Sign-Off

- [x] All tasks have `<automated>` verify or Wave 0 dependencies
- [x] Sampling continuity: no 3 consecutive tasks without automated verify
- [x] Wave 0 covers all MISSING references
- [x] No watch-mode flags
- [x] Feedback latency < 5s
- [x] `nyquist_compliant: true` set in frontmatter

**Approval:** validated 2026-03-18 (31 tests, all green)
