---
phase: 61
slug: data-driven-packaging-gate
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-03-13
---

# Phase 61 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest |
| **Config file** | pyproject.toml (`testpaths = ["tests"]`) |
| **Quick run command** | `pytest tests/unit/test_title_ctr_store.py tests/unit/test_title_scorer_db.py -x -q` |
| **Full suite command** | `pytest tests/ -v` |
| **Estimated runtime** | ~5 seconds |

---

## Sampling Rate

- **After every task commit:** Run `pytest tests/unit/test_title_ctr_store.py tests/unit/test_title_scorer_db.py -x -q`
- **After every plan wave:** Run `pytest tests/ -v`
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 5 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 61-01-01 | 01 | 0 | Wave 0 stubs | unit | `pytest tests/unit/test_title_ctr_store.py -x -q` | ❌ W0 | ⬜ pending |
| 61-01-02 | 01 | 0 | Wave 0 stubs | unit | `pytest tests/unit/test_title_scorer_db.py -x -q` | ❌ W0 | ⬜ pending |
| 61-01-03 | 01 | 0 | Wave 0 stubs | integration | `pytest tests/integration/test_ctr_ingest.py -x -q` | ❌ W0 | ⬜ pending |
| 61-02-01 | 02 | 1 | get_pattern_ctr_from_db() returns correct averages | unit | `pytest tests/unit/test_title_ctr_store.py -x -q` | ❌ W0 | ⬜ pending |
| 61-02-02 | 02 | 1 | get_pattern_ctr_from_db() fallback when DB empty | unit | same | ❌ W0 | ⬜ pending |
| 61-02-03 | 02 | 1 | get_pattern_ctr_from_db() skips below min_sample | unit | same | ❌ W0 | ⬜ pending |
| 61-03-01 | 03 | 1 | score_title() with db_path uses DB scores | unit | `pytest tests/unit/test_title_scorer_db.py -x -q` | ❌ W0 | ⬜ pending |
| 61-03-02 | 03 | 1 | score_title() without db_path unchanged | unit | same | ❌ W0 | ⬜ pending |
| 61-04-01 | 04 | 2 | Ingest writes correct rows, returns count | integration | `pytest tests/integration/test_ctr_ingest.py -x -q` | ❌ W0 | ⬜ pending |
| 61-04-02 | 04 | 2 | CTR rows with 0 excluded from averages | unit | `pytest tests/unit/test_title_ctr_store.py -x -q` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `tests/unit/test_title_ctr_store.py` — stubs for get_pattern_ctr_from_db() behaviors
- [ ] `tests/unit/test_title_scorer_db.py` — stubs for score_title() with db_path param
- [ ] `tests/integration/test_ctr_ingest.py` — integration test for synthesis → DB ingest

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Greenlight produces GO when best title >= 65 with DB enrichment | End-to-end gate | Requires full command pipeline + real DB state | Run `/greenlight` on a test topic, verify output includes DB-sourced CTR |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 5s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
