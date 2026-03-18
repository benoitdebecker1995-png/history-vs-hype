---
phase: 68
slug: title-generation-upgrade
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-03-17
---

# Phase 68 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest (existing) |
| **Config file** | `pyproject.toml [tool.pytest]` |
| **Quick run command** | `python -m pytest tests/unit/test_title_generator.py -x -q` |
| **Full suite command** | `python -m pytest tests/ -q` |
| **Estimated runtime** | ~5 seconds |

---

## Sampling Rate

- **After every task commit:** Run `python -m pytest tests/unit/test_title_generator.py -x -q`
- **After every plan wave:** Run `python -m pytest tests/ -q`
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 5 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 68-01-01 | 01 | 1 | TITLE-01 | unit | `pytest tests/unit/test_title_generator.py::test_extracts_number_from_body -x` | ❌ W0 | ⬜ pending |
| 68-01-02 | 01 | 1 | TITLE-01 | unit | `pytest tests/unit/test_title_generator.py::test_extracts_document_name -x` | ❌ W0 | ⬜ pending |
| 68-01-03 | 01 | 1 | TITLE-01 | unit | `pytest tests/unit/test_title_generator.py::test_extracts_contradiction -x` | ❌ W0 | ⬜ pending |
| 68-01-04 | 01 | 1 | TITLE-01 | unit | `pytest tests/unit/test_title_generator.py::test_srt_input_extracts_material -x` | ❌ W0 | ⬜ pending |
| 68-01-05 | 01 | 1 | TITLE-01 | unit | `pytest tests/unit/test_title_generator.py::test_position_weighting -x` | ❌ W0 | ⬜ pending |
| 68-01-06 | 01 | 1 | TITLE-02 | unit | `pytest tests/unit/test_title_generator.py::test_versus_auto_detection -x` | ❌ W0 | ⬜ pending |
| 68-01-07 | 01 | 1 | TITLE-02 | unit | `pytest tests/unit/test_title_generator.py::test_declarative_always_generated -x` | ❌ W0 | ⬜ pending |
| 68-01-08 | 01 | 1 | TITLE-02 | unit | `pytest tests/unit/test_title_generator.py::test_versus_weak_signal_not_primary -x` | ❌ W0 | ⬜ pending |
| 68-02-01 | 02 | 2 | TITLE-03 | unit | `pytest tests/unit/test_title_generator.py::test_year_candidate_ranked_last -x` | ❌ W0 | ⬜ pending |
| 68-02-02 | 02 | 2 | TITLE-03 | unit | `pytest tests/unit/test_title_generator.py::test_colon_candidate_ranked_last -x` | ❌ W0 | ⬜ pending |
| 68-02-03 | 02 | 2 | TITLE-03 | unit | `pytest tests/unit/test_title_generator.py::test_all_candidates_shown -x` | ❌ W0 | ⬜ pending |
| 68-02-04 | 02 | 2 | TITLE-03 | unit | `pytest tests/unit/test_title_generator.py::test_output_is_ranked_table -x` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `tests/unit/test_title_generator.py` — stubs for TITLE-01, TITLE-02, TITLE-03 (all 13 tests)
- [ ] `tools/production/title_generator.py` — module skeleton (importable, classes/functions defined with NotImplementedError)

*Existing infrastructure: `tests/` directory, pytest, `tests/conftest.py` with fixtures — all exist.*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| `/publish --titles` end-to-end output format | TITLE-01, TITLE-02, TITLE-03 | Requires Claude generation + formatted output review | Run `/publish --titles` on a real script and verify ranked table format |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 5s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
