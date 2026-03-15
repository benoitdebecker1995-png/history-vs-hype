---
phase: 64
slug: evaluate-youtube-mcp-servers-and-packaging-plugins-for-adoption
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-03-15
---

# Phase 64 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 7.x (existing) |
| **Config file** | pyproject.toml |
| **Quick run command** | `pytest tests/ -x --timeout=30` |
| **Full suite command** | `pytest tests/ --timeout=60` |
| **Estimated runtime** | ~45 seconds |

---

## Sampling Rate

- **After every task commit:** Run `pytest tests/ -x --timeout=30`
- **After every plan wave:** Run `pytest tests/ --timeout=60`
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 45 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 64-01-01 | 01 | 1 | EVAL-01 | integration | `claude mcp list` + install verification | N/A | ⬜ pending |
| 64-01-02 | 01 | 1 | EVAL-02 | integration | MCP test query + response validation | N/A | ⬜ pending |
| 64-01-03 | 01 | 1 | EVAL-03 | manual | Decision document review | N/A | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

*Existing infrastructure covers all phase requirements. This is an evaluation phase — validation is install-test-document, not unit tests.*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| MCP server responds to real queries | EVAL-02 | Requires live API keys and network | Run test query, verify structured response |
| Tool integration with existing pipeline | EVAL-02 | Requires human judgment on workflow fit | Compare output format with existing tools |
| Adopt/skip decision quality | EVAL-03 | Requires human review of evidence vs conclusion | Read DECISION.md, verify evidence supports verdicts |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 45s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
