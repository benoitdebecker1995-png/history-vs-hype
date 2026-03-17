---
phase: 66
slug: external-benchmark-research
status: draft
nyquist_compliant: true
wave_0_complete: true
created: 2026-03-16
---

# Phase 66 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | None — Phase 66 is research only, zero code |
| **Config file** | N/A |
| **Quick run command** | `python -c "import json; json.load(open('channel-data/niche_benchmark.json'))"` |
| **Full suite command** | See deliverable checks below |
| **Estimated runtime** | ~2 seconds |

---

## Sampling Rate

- **After every task commit:** Spot-check relevant output file exists and is non-empty
- **After every plan wave:** Run all JSON validation checks below
- **Before `/gsd:verify-work`:** All 4 success criteria confirmed TRUE
- **Max feedback latency:** 2 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | Status |
|---------|------|------|-------------|-----------|-------------------|--------|
| 66-01-01 | 01 | 1 | CTR refresh | ctr_tracker output | `python -m tools.youtube_analytics.ctr_tracker --report-only` | ⬜ pending |
| 66-01-02 | 01 | 1 | niche_benchmark.json | JSON parse + field check | `python -c "import json; d=json.load(open('channel-data/niche_benchmark.json')); assert 'metadata' in d and 'by_pattern' in d and 'by_topic_type' in d"` | ⬜ pending |
| 66-01-03 | 01 | 1 | channels >= 5 | JSON field check | `python -c "import json; d=json.load(open('channel-data/niche_benchmark.json')); assert len(d['metadata']['channels_sampled']) >= 5"` | ⬜ pending |
| 66-01-04 | 01 | 1 | niche-hook-patterns.md | File exists + non-empty | `test -s channel-data/niche-hook-patterns.md` | ⬜ pending |
| 66-01-05 | 01 | 1 | HOOK-PATTERN-LIBRARY.md | Heading structure | `grep -c "## Pattern:" .claude/REFERENCE/HOOK-PATTERN-LIBRARY.md` (>= 4) | ⬜ pending |
| 66-01-06 | 01 | 1 | 50% from 100K+ | Manual review | User review gate | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

Existing infrastructure covers all phase requirements. No test files needed — this phase produces data files, not code. Verification is file-existence checks and manual review.

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Hook examples >= 50% from 100K+ channels | SC #3 | Requires human judgment on channel matching | Review HOOK-PATTERN-LIBRARY.md examples against channel list |
| CTR proxy methodology quality | SC #1 | Views/sub ratio interpretation needs human review | Spot-check 3-5 outlier identifications against YouTube |
| User approval of channel list | CONTEXT decision | User approves final channel selection | Present list, get approval before proceeding |

---

## Validation Sign-Off

- [x] All tasks have automated verify or manual verification plan
- [x] Sampling continuity: no 3 consecutive tasks without verification
- [x] Wave 0 covers all MISSING references (none needed)
- [x] No watch-mode flags
- [x] Feedback latency < 2s
- [x] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
