---
phase: 67
slug: title-scorer-recalibration
status: validated
nyquist_compliant: true
wave_0_complete: true
created: 2026-03-17
validated: 2026-03-18
---

# Phase 67 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest |
| **Config file** | pyproject.toml or pytest.ini (check existing) |
| **Quick run command** | `pytest tests/unit/test_title_scorer_niche.py -x -q` |
| **Full suite command** | `pytest tests/unit/ -q` |
| **Estimated runtime** | ~5 seconds |

---

## Sampling Rate

- **After every task commit:** Run `pytest tests/unit/test_title_scorer_niche.py -x -q`
- **After every plan wave:** Run `pytest tests/unit/ -q`
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 5 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 67-01-01 | 01 | 1 | BENCH-01 | unit | `pytest tests/unit/test_benchmark_store.py -x -q` | ✅ 31 tests | ✅ green |
| 67-01-02 | 01 | 1 | BENCH-01, BENCH-02, BENCH-03 | unit | `pytest tests/unit/test_title_scorer_niche.py -x -q` | ✅ 37 tests | ✅ green |
| 67-02-01 | 02 | 2 | BENCH-01, BENCH-02 | integration | `python -m tools.title_scorer "France Divided Haiti" --topic territorial --db tools/intel/intel.db` | ✅ CLI verified | ✅ green |
| 67-02-02 | 02 | 2 | BENCH-01 | integration | Preflight niche propagation check | ✅ VERIFICATION confirmed | ✅ green |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [x] `tests/unit/test_benchmark_store.py` — 31 tests covering load(), get_niche_score(), TOPIC_GRADE_THRESHOLDS, normalize_topic_type()
- [x] `tests/unit/test_title_scorer_niche.py` — 37 tests covering niche percentile, small-sample fallback, topic-type thresholds

*Existing infrastructure covers pytest framework.*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Niche percentile readable in `/greenlight` output | BENCH-01 | CLI formatting visual check | Run `/greenlight` on a test topic and verify niche percentile line appears |

---

## Validation Sign-Off

- [x] All tasks have `<automated>` verify or Wave 0 dependencies
- [x] Sampling continuity: no 3 consecutive tasks without automated verify
- [x] Wave 0 covers all MISSING references
- [x] No watch-mode flags
- [x] Feedback latency < 5s
- [x] `nyquist_compliant: true` set in frontmatter

**Approval:** validated 2026-03-18 (68 tests, all green)
