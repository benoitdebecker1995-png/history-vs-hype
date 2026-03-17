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
| 67-01-01 | 01 | 1 | BENCH-01 | unit | `pytest tests/unit/test_benchmark_store.py::test_graceful_none -x` | ❌ W0 | ⬜ pending |
| 67-01-02 | 01 | 1 | BENCH-01, BENCH-02, BENCH-03 | unit | `pytest tests/unit/test_title_scorer_niche.py -x -q` | ❌ W0 | ⬜ pending |
| 67-02-01 | 02 | 2 | BENCH-01, BENCH-02 | integration | `python -m tools.title_scorer "France Divided Haiti" --topic territorial --db tools/intel/intel.db` | N/A | ⬜ pending |
| 67-02-02 | 02 | 2 | BENCH-01 | integration | `python -c "from tools.preflight.scorer import _score_title_metadata; r = _score_title_metadata(...); assert any('niche' in n.lower() for n in r['notes'])"` | N/A | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `tests/unit/test_benchmark_store.py` — covers BENCH-01 graceful None fallback
- [ ] `tests/unit/test_title_scorer_niche.py` — covers BENCH-01 niche percentile, BENCH-02 small-sample fallback, BENCH-03 topic-type thresholds

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
