---
phase: 65
slug: automated-ctr-feedback-loop
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-03-15
---

# Phase 65 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest (existing, from pyproject.toml) |
| **Config file** | `pyproject.toml` `[tool.pytest.ini_options]` |
| **Quick run command** | `python -m pytest tests/youtube_analytics/test_ctr_tracker.py -x -q` |
| **Full suite command** | `python -m pytest tests/ -q` |
| **Estimated runtime** | ~5 seconds |

---

## Sampling Rate

- **After every task commit:** Run `python -m pytest tests/youtube_analytics/test_ctr_tracker.py -x -q`
- **After every plan wave:** Run `python -m pytest tests/ -q`
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 5 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 65-01-01 | 01 | 1 | CTR fetch populates ctr_percent | unit | `pytest tests/youtube_analytics/test_ctr_tracker.py::test_ctr_stored_in_snapshot -x` | ❌ W0 | ⬜ pending |
| 65-01-02 | 01 | 1 | Unavailable CTR writes view_count fallback | unit | `pytest tests/youtube_analytics/test_ctr_tracker.py::test_ctr_unavailable_fallback -x` | ❌ W0 | ⬜ pending |
| 65-01-03 | 01 | 1 | API error does not abort loop | unit | `pytest tests/youtube_analytics/test_ctr_tracker.py::test_ctr_partial_failure -x` | ❌ W0 | ⬜ pending |
| 65-01-04 | 01 | 1 | End-of-run summary prints pattern scores | unit | `pytest tests/youtube_analytics/test_ctr_tracker.py::test_summary_output -x` | ❌ W0 | ⬜ pending |
| 65-01-05 | 01 | 1 | Duplicate snapshot guard skips same day | unit | `pytest tests/youtube_analytics/test_ctr_tracker.py::test_duplicate_guard -x` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `tests/youtube_analytics/test_ctr_tracker.py` — stubs for all 5 behaviors above
- [ ] Mock for `get_ctr_metrics()` — mock at `tools.youtube_analytics.ctr_tracker.get_ctr_metrics`

*Existing pytest infrastructure covers framework install.*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Windows Task Scheduler fires on schedule | Scheduled execution | OS-level scheduler, not testable in pytest | Create task, wait for trigger, check log output |
| OAuth token refresh across sessions | Token persistence | Requires real Google credentials | Run script, wait >1hr, run again, verify no re-auth prompt |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 5s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
