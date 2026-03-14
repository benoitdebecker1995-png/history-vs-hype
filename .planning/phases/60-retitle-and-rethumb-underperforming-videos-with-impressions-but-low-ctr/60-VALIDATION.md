---
phase: 60
slug: retitle-and-rethumb-underperforming-videos-with-impressions-but-low-ctr
status: draft
nyquist_compliant: true
wave_0_complete: true
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

- **After every task commit:** Run file-existence verify commands from plan tasks
- **After every plan wave:** Run `python -m pytest tests/ -x -q` (existing tests only)
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 10 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | Status |
|---------|------|------|-------------|-----------|-------------------|--------|
| 60-01-01 | 01 | 1 | Slash command creation | file check | `test -f ".claude/commands/retitle.md" && head -5 ".claude/commands/retitle.md" \| grep -q "description:" && echo "PASS" \|\| echo "FAIL"` | pending |
| 60-02-01 | 02 | 2 | --check/--revert flags | content check | `grep -cE "retitle --check\|retitle --revert\|SWAP LOG" ".claude/commands/retitle.md" \| awk '{exit ($1 >= 3 ? 0 : 1)}' && echo "PASS" \|\| echo "FAIL"` | pending |

*Status: pending / green / red / flaky*

---

## Wave 0 Requirements

None. This phase creates a slash command (.md instructions file), not Python modules. The underlying tools (retitle_audit.py, retitle_gen.py, title_scorer.py, thumbnail_checker.py) are pre-existing and have their own test coverage. New unit tests for those tools are out of scope for this phase.

*Existing infrastructure covers ctr_ingest integration tests.*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| SWAP-CHECKLIST.md format | Copy-paste friendly | Requires human readability judgment | Open alongside YouTube Studio, verify each entry is self-contained |
| Thumbnail concept quality | Map type suggestions | Requires visual/creative judgment | Check suggested map types match video content |
| /retitle end-to-end | Full pipeline works at runtime | Slash command interpreted by Claude at runtime | Run `/retitle --audit` and verify output |

---

## Validation Sign-Off

- [x] All tasks have `<automated>` verify commands
- [x] Sampling continuity: no 3 consecutive tasks without automated verify
- [x] No Wave 0 gaps (no testable Python created by this phase)
- [x] No watch-mode flags
- [x] Feedback latency < 10s
- [x] `nyquist_compliant: true` set in frontmatter

**Approval:** ready
