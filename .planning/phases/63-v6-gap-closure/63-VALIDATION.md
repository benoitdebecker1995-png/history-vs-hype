---
phase: 63
slug: v6-gap-closure
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-03-15
---

# Phase 63 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest |
| **Config file** | `pyproject.toml` (testpaths = ["tests"]) |
| **Quick run command** | `pytest tests/integration/test_ctr_ingest.py -x` |
| **Full suite command** | `pytest` |
| **Estimated runtime** | ~15 seconds |

---

## Sampling Rate

- **After every task commit:** Run `pytest tests/integration/test_ctr_ingest.py -x`
- **After every plan wave:** Run `pytest`
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 15 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 63-01-01 | 01 | 1 | RETITLE-02 | manual | manual — .md slash command, not Python | N/A | ⬜ pending |
| 63-01-02 | 01 | 1 | GATE-02 | unit | `pytest tests/ -k "score_title or title_scorer" -x` | check | ⬜ pending |
| 63-02-01 | 02 | 1 | ctr_ingest fix | integration | `pytest tests/integration/test_ctr_ingest.py -x` | ✅ | ⬜ pending |
| 63-03-01 | 03 | 1 | SUMMARY gaps | manual | `grep "requirements_completed" .planning/phases/60-*/*-SUMMARY.md .planning/phases/61-*/*-SUMMARY.md` | N/A | ⬜ pending |
| 63-03-02 | 03 | 1 | REQUIREMENTS.md | manual | `grep "Not started" .planning/REQUIREMENTS.md` | N/A | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

Existing infrastructure covers all phase requirements. No new test files needed.

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| `/retitle` uses DB-enriched scores | RETITLE-02 | Slash command in .md file, not Python | Run `/retitle` on a video, verify output shows `db_enriched: True` when DB data exists |
| SUMMARY frontmatter complete | docs | Frontmatter keys, not runtime behavior | grep for `requirements_completed` in affected SUMMARY files |
| REQUIREMENTS.md traceability | docs | Static documentation | Verify no "Not started" rows for completed phases |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 15s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
