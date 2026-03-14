---
phase: 60
slug: retitle-and-rethumb-underperforming-videos-with-impressions-but-low-ctr
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-03-14
---

# Phase 60 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest |
| **Config file** | `pyproject.toml` (testpaths=["tests"]) |
| **Quick run command** | `python -m pytest tests/integration/test_ctr_ingest.py -x -q` |
| **Full suite command** | `python -m pytest tests/ -x -q` |
| **Estimated runtime** | ~10 seconds |

---

## Sampling Rate

- **After every task commit:** Run `python -m pytest tests/integration/test_ctr_ingest.py -x -q`
- **After every plan wave:** Run `python -m pytest tests/ -x -q`
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 10 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 60-01-01 | 01 | 1 | Audit ranking | unit | `python -m pytest tests/ -k "retitle_audit" -x -q` | ❌ W0 | ⬜ pending |
| 60-01-02 | 01 | 1 | Title generation | unit | `python -m pytest tests/ -k "retitle_gen" -x -q` | ❌ W0 | ⬜ pending |
| 60-02-01 | 02 | 1 | SWAP-CHECKLIST output | integration | Run `/retitle`, check output | N/A manual | ⬜ pending |
| 60-02-02 | 02 | 1 | SWAP LOG injection | unit | `python -m pytest tests/ -k "swap_log" -x -q` | ❌ W0 | ⬜ pending |
| 60-03-01 | 03 | 2 | --check 7-day guard | unit | `python -m pytest tests/ -k "retitle_check" -x -q` | ❌ W0 | ⬜ pending |
| 60-03-02 | 03 | 2 | ctr_ingest pipeline | integration | `python -m pytest tests/integration/test_ctr_ingest.py -x -q` | ✅ | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `tests/unit/test_retitle_audit.py` — covers audit ranking + retention weighting
- [ ] `tests/unit/test_retitle_gen.py` — covers title generation from scripts/SRTs
- [ ] `tests/unit/test_swap_log.py` — covers SWAP LOG section append logic
- [ ] `tests/unit/test_retitle_check.py` — covers 7-day guard + CTR comparison

*Existing infrastructure covers ctr_ingest integration tests.*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| SWAP-CHECKLIST.md format | Copy-paste friendly | Requires human readability judgment | Open alongside YouTube Studio, verify each entry is self-contained |
| Thumbnail concept quality | Map type suggestions | Requires visual/creative judgment | Check suggested map types match video content |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 10s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
