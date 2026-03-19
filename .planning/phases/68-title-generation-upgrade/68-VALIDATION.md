---
phase: 68
slug: title-generation-upgrade
status: validated
nyquist_compliant: true
wave_0_complete: true
created: 2026-03-17
validated: 2026-03-18
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
| 68-01-01 | 01 | 1 | TITLE-01 | unit | `pytest tests/unit/test_title_generator.py::TestTitleMaterialExtractorNumbers::test_extracts_number_from_body -x` | ✅ | ✅ green |
| 68-01-02 | 01 | 1 | TITLE-01 | unit | `pytest tests/unit/test_title_generator.py::TestTitleMaterialExtractorDocuments::test_extracts_document_name -x` | ✅ | ✅ green |
| 68-01-03 | 01 | 1 | TITLE-01 | unit | `pytest tests/unit/test_title_generator.py::TestTitleMaterialExtractorContradictions::test_extracts_contradiction -x` | ✅ | ✅ green |
| 68-01-04 | 01 | 1 | TITLE-01 | unit | `pytest tests/unit/test_title_generator.py::TestSRTInput::test_srt_input_extracts_material -x` | ✅ | ✅ green |
| 68-01-05 | 01 | 1 | TITLE-01 | unit | `pytest tests/unit/test_title_generator.py::TestPositionWeighting::test_position_weighting_intro_higher_than_body -x` | ✅ | ✅ green |
| 68-01-06 | 01 | 1 | TITLE-02 | unit | `pytest tests/unit/test_title_generator.py::TestVersusDetection::test_versus_auto_detection_strong_signal -x` | ✅ | ✅ green |
| 68-01-07 | 01 | 1 | TITLE-02 | unit | `pytest tests/unit/test_title_generator.py::TestCandidateGeneration::test_declarative_always_generated -x` | ✅ | ✅ green |
| 68-01-08 | 01 | 1 | TITLE-02 | unit | `pytest tests/unit/test_title_generator.py::TestVersusDetection::test_versus_weak_signal_not_primary -x` | ✅ | ✅ green |
| 68-02-01 | 02 | 2 | TITLE-03 | unit | `pytest tests/unit/test_title_generator.py::TestFormatTitleCandidates::test_year_candidate_ranked_last -x` | ✅ | ✅ green |
| 68-02-02 | 02 | 2 | TITLE-03 | unit | `pytest tests/unit/test_title_generator.py::TestFormatTitleCandidates::test_penalized_candidates_show_warning -x` | ✅ | ✅ green |
| 68-02-03 | 02 | 2 | TITLE-03 | unit | `pytest tests/unit/test_title_generator.py::TestFormatTitleCandidates::test_all_candidates_shown -x` | ✅ | ✅ green |
| 68-02-04 | 02 | 2 | TITLE-03 | unit | `pytest tests/unit/test_title_generator.py::TestFormatTitleCandidates::test_format_ranked_table -x` | ✅ | ✅ green |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [x] `tests/unit/test_title_generator.py` — 27 tests covering TITLE-01, TITLE-02, TITLE-03 (exceeds planned 13)
- [x] `tools/production/title_generator.py` — 806 lines, fully implemented

*Existing infrastructure: `tests/` directory, pytest, `tests/conftest.py` with fixtures — all exist.*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| `/publish --titles` end-to-end output format | TITLE-01, TITLE-02, TITLE-03 | Requires Claude generation + formatted output review | Run `/publish --titles` on a real script and verify ranked table format |

---

## Validation Sign-Off

- [x] All tasks have `<automated>` verify or Wave 0 dependencies
- [x] Sampling continuity: no 3 consecutive tasks without automated verify
- [x] Wave 0 covers all MISSING references
- [x] No watch-mode flags
- [x] Feedback latency < 5s
- [x] `nyquist_compliant: true` set in frontmatter

**Approval:** validated 2026-03-18 (27 tests, all green)
