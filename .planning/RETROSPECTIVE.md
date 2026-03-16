# Project Retrospective

*A living document updated after each milestone. Lessons feed forward into future planning.*

## Milestone: v6.0 — Packaging Pipeline

**Shipped:** 2026-03-16
**Phases:** 6 | **Plans:** 11

### What Was Built
- `/retitle` pipeline: audit → generate → score → SWAP-CHECKLIST → measure → feedback loop
- Data-driven title scoring gate: live CTR from DB flows through greenlight/preflight automatically
- Proactive topic discovery: autocomplete + competitor gaps + Google Trends via `/discover --scan`
- Gap closure: wired DB-enriched scoring everywhere, fixed private access patterns
- MCP server evaluation: adopted 2, skipped 9 with evidence
- Automated CTR feedback loop: weekly Task Scheduler → YouTube API → ctr_snapshots → title_scorer

### What Worked
- Milestone audit before completion caught the INT-01 gap (retitle not using DB scores) — Phase 63 fixed it before shipping
- TDD approach on title_ctr_store and ctr_ingest caught edge cases early (LIKE matching, late entry flags)
- Evidence-based MCP evaluation saved time — didn't waste effort on broken YouTube MCPs
- Gap closure as dedicated phase is a good pattern — catches integration issues that per-phase verification misses

### What Was Inefficient
- Phases 64-65 were added after the original v6.0 scope (60-63) — scope creep, though both delivered value
- SUMMARY frontmatter gaps in 60-02, 61-02, 61-03 — requirements_completed field left empty during execution, caught by audit
- Nyquist validation incomplete for phases 61 and 62 — validation gap tracking needs to be more automated

### Patterns Established
- Gap closure phase as standard milestone closer (Phase 63 pattern)
- Milestone audit → gap closure → completion as 3-step shipping sequence
- MCP evaluation with install-test-verdict workflow for any new tool adoption
- Weekly automated data refresh via Task Scheduler for any periodic pipeline

### Key Lessons
1. **Audit before completing milestones** — v6.0 audit caught a real integration gap that would have shipped broken
2. **DB-enriched scoring needs end-to-end wiring** — it's not enough to build the store; every consumer must pass db_path
3. **MCP ecosystem is immature** — most YouTube-related MCPs are broken; build your own tools instead of depending on community packages
4. **15 autocomplete seeds is the sweet spot** — <90s runtime, sufficient coverage for channel niches

### Cost Observations
- Model mix: primarily opus for execution, sonnet for research agents
- 72 commits over 15 days (moderate pace, mixed with video production work)
- Notable: Phase 64 (MCP eval) was mostly investigation, not code — low token cost, high information value

---

## Cross-Milestone Trends

### Process Evolution

| Milestone | Phases | Plans | Key Change |
|-----------|--------|-------|------------|
| v5.1 | 7 | 17 | Codebase hardening — production-grade error handling, logging, testing |
| v5.2 | 5 | 5 | Growth engine — YouTube Analytics data drives decisions |
| v6.0 | 6 | 11 | Packaging pipeline — fixing the distribution bottleneck |

### Top Lessons (Verified Across Milestones)

1. **Audit before shipping** — milestone audits consistently find 1-2 integration gaps that phase-level verification misses (v5.1, v6.0)
2. **Gap closure phases work** — dedicated cleanup phase after audit is more efficient than trying to fix issues during completion
3. **TDD pays off for data pipelines** — title_ctr_store, ctr_ingest, discovery_scanner all benefited from test-first approach
