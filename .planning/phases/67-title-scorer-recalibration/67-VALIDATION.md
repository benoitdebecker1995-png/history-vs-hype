---
phase: 67
slug: title-scorer-recalibration
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-03-17
---

# Phase 67 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest |
| **Config file** | pyproject.toml or pytest.ini (check existing) |
| **Quick run command** | `pytest tools/tests/test_title_scorer.py -x -q` |
| **Full suite command** | `pytest tools/tests/ -q` |
| **Estimated runtime** | ~5 seconds |

---

## Sampling Rate

- **After every task commit:** Run `pytest tools/tests/test_title_scorer.py -x -q`
- **After every plan wave:** Run `pytest tools/tests/ -q`
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 5 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 67-01-01 | 01 | 1 | BENCH-01 | unit | `pytest tools/tests/test_benchmark_store.py::test_graceful_none -x` | ❌ W0 | ⬜ pending |
| 67-01-02 | 01 | 1 | BENCH-01 | unit | `pytest tools/tests/test_title_scorer.py::test_niche_percentile_label -x` | ❌ W0 | ⬜ pending |
| 67-02-01 | 02 | 1 | BENCH-02 | unit | `pytest tools/tests/test_title_scorer.py::test_small_sample_fallback -x` | ❌ W0 | ⬜ pending |
| 67-02-02 | 02 | 1 | BENCH-02 | unit | `pytest tools/tests/test_title_scorer.py::test_no_fallback_sufficient_sample -x` | ❌ W0 | ⬜ pending |
| 67-03-01 | 03 | 1 | BENCH-03 | unit | `pytest tools/tests/test_title_scorer.py::test_topic_grade_territorial -x` | ❌ W0 | ⬜ pending |
| 67-03-02 | 03 | 1 | BENCH-03 | unit | `pytest tools/tests/test_title_scorer.py::test_topic_grade_political -x` | ❌ W0 | ⬜ pending |
| 67-03-03 | 03 | 1 | BENCH-03 | unit | `pytest tools/tests/test_title_scorer.py::test_same_title_different_topics -x` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `tools/tests/test_title_scorer.py` — stubs for BENCH-01, BENCH-02, BENCH-03
- [ ] `tools/tests/test_benchmark_store.py` — covers BENCH-01 graceful None fallback

*Existing infrastructure covers pytest framework.*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Niche percentile readable in `/greenlight` output | BENCH-01 | CLI formatting visual check | Run `/greenlight` on a test topic and verify niche percentile line appears |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 5s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
