---
phase: 70
slug: metadata-packaging-integration
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-03-18
---

# Phase 70 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest (used throughout the codebase) |
| **Config file** | None — tests run via `python -m pytest tests/` |
| **Quick run command** | `python -m pytest tests/test_metadata.py tests/test_title_generator.py -x -q` |
| **Full suite command** | `python -m pytest tests/ -q` |
| **Estimated runtime** | ~15 seconds |

---

## Sampling Rate

- **After every task commit:** Run `python -m pytest tests/test_metadata.py tests/test_title_generator.py -x -q`
- **After every plan wave:** Run `python -m pytest tests/ -q`
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 15 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 70-01-01 | 01 | 1 | META-01 | unit | `pytest tests/test_metadata.py::test_description_seo_first_line -x` | ❌ W0 | ⬜ pending |
| 70-01-02 | 01 | 1 | META-01 | unit | `pytest tests/test_metadata.py::test_citation_extraction -x` | ❌ W0 | ⬜ pending |
| 70-01-03 | 01 | 1 | META-01 | unit | `pytest tests/test_metadata.py::test_description_warns_missing_citations -x` | ❌ W0 | ⬜ pending |
| 70-01-04 | 01 | 1 | META-02 | unit | `pytest tests/test_metadata.py::test_thumbnail_three_concepts_territorial -x` | ❌ W0 | ⬜ pending |
| 70-01-05 | 01 | 1 | META-02 | unit | `pytest tests/test_metadata.py::test_thumbnail_concepts_are_grounded -x` | ❌ W0 | ⬜ pending |
| 70-01-06 | 01 | 1 | META-02 | unit | `pytest tests/test_metadata.py::test_thumbnail_concepts_validated -x` | ❌ W0 | ⬜ pending |
| 70-02-01 | 02 | 2 | META-03 | unit | `pytest tests/test_title_generator.py::test_format_title_candidates_coherence_column -x` | ❌ W0 | ⬜ pending |
| 70-02-02 | 02 | 2 | META-03 | unit | `pytest tests/test_metadata.py::test_coherence_check_counts -x` | ❌ W0 | ⬜ pending |
| 70-02-03 | 02 | 2 | META-03 | unit | `pytest tests/test_metadata.py::test_coherence_detail_only_mismatches -x` | ❌ W0 | ⬜ pending |
| 70-02-04 | 02 | 2 | CLICKBAIT | unit | `pytest tests/test_metadata.py::test_clickbait_import_from_title_scorer -x` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `tests/test_metadata.py` — stubs for META-01, META-02, META-03, CLICKBAIT migration (7 new test functions)
- [ ] `tests/test_title_generator.py` — add `test_format_title_candidates_coherence_column` (1 new test function, existing file likely exists)

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| `/publish` full bundle output looks correct in terminal | META-01/02/03 | Visual formatting check | Run `/publish` on a completed script, verify section order and formatting |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 15s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
