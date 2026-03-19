---
phase: 70
slug: metadata-packaging-integration
status: validated
nyquist_compliant: true
wave_0_complete: true
created: 2026-03-18
validated: 2026-03-18
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
| 70-01-01 | 01 | 1 | META-01 | unit | `pytest tests/unit/test_metadata_bundle.py::TestGenerateDescription::test_first_line_not_in_this_video -x` | ✅ | ✅ green |
| 70-01-02 | 01 | 1 | META-01 | unit | `pytest tests/unit/test_metadata_bundle.py::TestExtractCitations -x` | ✅ 4 tests | ✅ green |
| 70-01-03 | 01 | 1 | META-01 | unit | `pytest tests/unit/test_metadata_bundle.py::TestGenerateDescription::test_warning_when_no_citations -x` | ✅ | ✅ green |
| 70-01-04 | 01 | 1 | META-02 | unit | `pytest tests/unit/test_metadata_bundle.py::TestGenerateThumbnailConcepts::test_territorial_returns_three_concepts -x` | ✅ | ✅ green |
| 70-01-05 | 01 | 1 | META-02 | unit | `pytest tests/unit/test_metadata_bundle.py::TestGenerateThumbnailConcepts::test_concept_contains_script_entity -x` | ✅ | ✅ green |
| 70-01-06 | 01 | 1 | META-02 | unit | `pytest tests/unit/test_metadata_bundle.py::TestGenerateThumbnailConcepts::test_each_concept_has_thumbnail_checker_badge -x` | ✅ | ✅ green |
| 70-02-01 | 02 | 2 | META-03 | unit | `pytest tests/unit/test_title_generator.py::TestFormatTitleCandidatesCoherenceColumn -x` | ✅ 4 tests | ✅ green |
| 70-02-02 | 02 | 2 | META-03 | unit | `pytest tests/unit/test_metadata_bundle.py::TestCoherenceCheck::test_full_match_returns_3_of_3 -x` | ✅ | ✅ green |
| 70-02-03 | 02 | 2 | META-03 | unit | `pytest tests/unit/test_metadata_bundle.py::TestCoherenceCheck::test_detail_section_present_for_mismatch -x` | ✅ | ✅ green |
| 70-02-04 | 02 | 2 | CLICKBAIT | unit | `pytest tests/unit/test_metadata_bundle.py::TestClickbaitConsolidation::test_metadata_imports_clickbait_from_title_scorer -x` | ✅ | ✅ green |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [x] `tests/unit/test_metadata_bundle.py` — 30 tests covering META-01 (description), META-02 (thumbnails), META-03 (coherence), CLICKBAIT consolidation
- [x] `tests/unit/test_title_generator.py` — 4 coherence column tests in TestFormatTitleCandidatesCoherenceColumn

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| `/publish` full bundle output looks correct in terminal | META-01/02/03 | Visual formatting check | Run `/publish` on a completed script, verify section order and formatting |

---

## Validation Sign-Off

- [x] All tasks have `<automated>` verify or Wave 0 dependencies
- [x] Sampling continuity: no 3 consecutive tasks without automated verify
- [x] Wave 0 covers all MISSING references
- [x] No watch-mode flags
- [x] Feedback latency < 15s
- [x] `nyquist_compliant: true` set in frontmatter

**Approval:** validated 2026-03-18 (30 tests, all green)
