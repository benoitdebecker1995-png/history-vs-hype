---
phase: 62
slug: proactive-topic-discovery
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-03-14
---

# Phase 62 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest (installed, `tests/` directory exists) |
| **Config file** | `pyproject.toml` — `testpaths = ["tests"]` |
| **Quick run command** | `python -m pytest tests/test_discovery_scanner.py -x -q` |
| **Full suite command** | `python -m pytest tests/ -x -q` |
| **Estimated runtime** | ~5 seconds |

---

## Sampling Rate

- **After every task commit:** Run `python -m pytest tests/test_discovery_scanner.py -x -q`
- **After every plan wave:** Run `python -m pytest tests/ -x -q`
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 5 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 62-01-01 | 01 | 1 | DISC-01 | unit | `pytest tests/test_discovery_scanner.py::test_autocomplete_dedup -x` | ❌ W0 | ⬜ pending |
| 62-01-02 | 01 | 1 | DISC-02 | unit | `pytest tests/test_discovery_scanner.py::test_competitor_gap_detection -x` | ❌ W0 | ⬜ pending |
| 62-01-03 | 01 | 1 | DISC-03 | unit | `pytest tests/test_discovery_scanner.py::test_trends_breakout -x` | ❌ W0 | ⬜ pending |
| 62-01-04 | 01 | 1 | DISC-04 | unit | `pytest tests/test_discovery_scanner.py::test_extended_belize_scoring -x` | ❌ W0 | ⬜ pending |
| 62-01-05 | 01 | 1 | DISC-05 | unit | `pytest tests/test_discovery_scanner.py::test_dedup_pipeline -x` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `tests/test_discovery_scanner.py` — stubs for DISC-01 through DISC-05 with mocked external calls
- [ ] Fixtures: mock autocomplete result, mock competitor video list, mock trends result
- [ ] Mock patterns from Phase 53 integration tests (feedparser, anthropic, pyppeteer)

*No framework install needed — pytest already installed.*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| DISCOVERY-FEED.md output readable | DISC-04 | Markdown formatting is subjective | Visually inspect generated report |
| `/discover --scan` CLI integration | DISC-04 | Requires Claude Code slash command | Run `/discover --scan` in live session |
| Channel suggestion quality | DISC-02 | Relevance is subjective | Review suggested channels for niche fit |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 5s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
