---
gsd_state_version: 1.0
milestone: v7.0
milestone_name: Packaging & Hooks Overhaul
status: in_progress
last_updated: "2026-03-18T21:19:59.529Z"
last_activity: 2026-03-17 — Phase 67 plan 02 complete (niche display, --topic flag, preflight integration)
progress:
  total_phases: 5
  completed_phases: 4
  total_plans: 7
  completed_plans: 7
---

---
gsd_state_version: 1.0
milestone: v7.0
milestone_name: Packaging & Hooks Overhaul
status: in_progress
last_updated: "2026-03-17T22:44:08.675Z"
last_activity: 2026-03-17 — Phase 67 plan 01 complete (niche benchmark layer, topic-type grades)
progress:
  total_phases: 5
  completed_phases: 2
  total_plans: 3
  completed_plans: 3
  percent: 100
---

---
gsd_state_version: 1.0
milestone: v7.0
milestone_name: Packaging & Hooks Overhaul
status: in_progress
last_updated: "2026-03-17T22:39:43.711Z"
last_activity: 2026-03-16 — v7.0 roadmap created, Phases 66-70 defined
progress:
  [██████████] 100%
  completed_phases: 1
  total_plans: 3
  completed_plans: 2
---

---
gsd_state_version: 1.0
milestone: v7.0
milestone_name: Packaging & Hooks Overhaul
status: in_progress
last_updated: "2026-03-17"
last_activity: "2026-03-17 — Phase 66 plan 01 complete (real YouTube data extraction)"
current_phase: 66
progress:
  total_phases: 5
  completed_phases: 0
  total_plans: 1
  completed_plans: 1
  percent: 20
decisions:
  - "Shaun excluded (192K subs, below 500K). 4 format-matched channels."
  - "VidIQ not used — only for keyword search volume."
  - "7 hooks rate-limited — backfill script at tools/benchmark/backfill_hooks.py"
---

---
gsd_state_version: 1.0
milestone: v7.0
milestone_name: Packaging & Hooks Overhaul
status: roadmap_complete
last_updated: "2026-03-16"
last_activity: "2026-03-16 — v7.0 roadmap created, Phases 66-70 defined"
progress:
  [██████████] 99%
  completed_phases: 65
  total_plans: 132
  completed_plans: 132
  percent: 0
---

# State: History vs Hype Workspace

**Initialized:** 2025-01-19
**Last Updated:** 2026-03-16 (v7.0 roadmap created)

## Project Reference

See: `.planning/PROJECT.md` (updated 2026-03-16)

**Core value:** Every video shows sources on screen
**Current focus:** v7.0 — Packaging & Hooks Overhaul

## Current Position

Phase: 67 — Title Scorer Recalibration
Plan: 02 complete — Phase 67 complete
Status: Phase 67 complete — niche display wired into format_result() and /greenlight
Last activity: 2026-03-17 — Phase 67 plan 02 complete (niche display, --topic flag, preflight integration)

Progress: [██████████] 100% (138/138 plans complete)

## Milestone History

| Version | Name | Phases | Shipped |
|---------|------|--------|---------|
| v1.0 | Workspace Optimization | 0.1, 1-7 | 2026-01-23 |
| v1.1 | Analytics & Learning Loop | 8-10 | 2026-01-26 |
| v1.2 | Script Quality & Discovery | 11-14 | 2026-01-30 |
| v1.3 | Niche Discovery | 15-18 | 2026-02-02 |
| v1.4 | Learning Loop | 19-21 | 2026-02-02 |
| v1.5 | Production Acceleration | 22-26 | 2026-02-05 |
| v1.6 | Click & Keep | 27-32 | 2026-02-09 |
| v2.0 | Channel Intelligence | 33-35 | 2026-02-11 |
| v3.0 | Adaptive Scriptwriter | 36-38 | 2026-02-15 |
| v4.0 | Untranslated Evidence Pipeline | 39-41 | 2026-02-18 |
| v5.0 | Production Intelligence | 42-47 | 2026-02-22 |
| v5.1 | Codebase Hardening | 48-54 | 2026-03-01 |
| v5.2 | Growth Engine | 55-59 | 2026-03-01 |
| v6.0 | Packaging Pipeline | 60-65 | 2026-03-16 |

**Full history:** `.planning/MILESTONES.md`
**Archives:** `.planning/milestones/`

## v7.0 Phase Map

| Phase | Name | Requirements | Status |
|-------|------|--------------|--------|
| 66 | External Benchmark Research | (prerequisite — unblocks all) | Not started |
| 67 | Title Scorer Recalibration | BENCH-01, BENCH-02, BENCH-03 | Not started |
| 68 | Title Generation Upgrade | TITLE-01, TITLE-02, TITLE-03 | Not started |
| 69 | Hook Quality Upgrade | HOOK-01, HOOK-02 | Not started |
| 70 | Metadata & Packaging Integration | META-01, META-02, META-03 | Not started |

## Accumulated Context

### Decisions

v6.0 decisions archived in `.planning/milestones/v6.0-ROADMAP.md`.

Key v7.0 design decisions (from research):
- Phase 66 is a research deliverable only — zero code should reference niche_benchmark.json or HOOK-PATTERN-LIBRARY.md before they are authored
- Benchmark data is advisory, not a hard gate — own-channel score remains primary; niche percentile is additive context
- All new features must extend existing commands (/publish, /greenlight, /script) — no new standalone invocation points
- benchmark_store.py requires graceful None fallback so missing niche_benchmark.json never blocks existing workflows
- Hook scoring runs after agent generation, not inside the agent (avoids circular feedback loop)
- CLICKBAIT_PATTERNS vs active_verbs inconsistency (metadata.py vs title_scorer.py) to be reconciled in Phase 70
- [Phase 54]: 4-strategy cascade for bulk paste splitting (markdown heading > plain step > triple-dash > double-newline)
- [Phase 54]: save_batch() continues on individual save errors rather than aborting batch
- [Phase 54-external-intelligence-synthesis]: Renamed _score_moderation -> score_moderation and _SAFE_ALTERNATIVES -> SAFE_ALTERNATIVES for public import from synthesis_engine.py
- [Phase 67]: Colon hard-reject kept despite niche colon VPS 0.776 (inflated by pipe-style titles from Knowing Better/Kraut)
- [Phase 67]: _OWN_CHANNEL_MIN_SAMPLE=5: niche substitution triggers when own-channel n < 5
- [Phase 67]: Grade thresholds intentionally recalibrated: general pass=60/good=70 raises bar vs old pass=50/good=65
- [Phase 67]: Topic line only shown when gap_message present (grade below B) — cleaner output
- [Phase 68-title-generation-upgrade]: Supplementary _extract_named_documents() added for Treaty-of-X patterns that entities.py misses
- [Phase 68-title-generation-upgrade]: detect_versus_signal: 100-word co-occurrence window, score=hits/3.0 capped at 1.0
- [Phase 68-title-generation-upgrade]: SRT positional heuristic: first/last 20% words get intro/conclusion weights
- [Phase 68]: format_title_candidates() appends warning lines below table for hard_rejects to preserve table parse-ability
- [Phase 68]: MetadataGenerator._db_path auto-resolves to tools/discovery/keywords.db at __init__ time; TitleVariant kept as deprecated for backward compat
- [Phase 69]: Framework detection: binary full/partial scoring — anomaly 15/10, stakes tiered by hit count, inciting 10/7/0
- [Phase 69]: Fulfillment check is pass/fail display only — not added to 100-point total_score (per Research pitfall #2)
- [Phase 69]: Style score modifier +5/-5 only at HIGH confidence (7+ examples); advisory-only at <5 examples
- [Phase 69]: --title flag is optional: omitting silently skips fulfillment check
- [Phase 69]: Urgency thresholds: score>=70 AND fulfillment pass=LOW; >=50 OR fail=MEDIUM; <50=HIGH

### Pending Todos

- Run ctr_tracker.py before starting Phase 67 to confirm CTR snapshot freshness (all snapshots currently dated 2026-02-23)
- Audit Rules 19-22 in script-writer-v2 before adding Rule 23 in Phase 69 (prior v3.0 consolidation precedent)

### Blockers/Concerns

None. Phase 66 is a manual research task — no external dependencies.

## Session Continuity

### Last Session

- **Date:** 2026-03-16
- **Work:** v7.0 roadmap created, Phases 66-70 defined, REQUIREMENTS.md traceability updated

### Next Session

**Next action:** `/gsd:plan-phase 66` — plan Phase 66 (External Benchmark Research)

## Technical Notes

- keywords.db schema version 29 (auto-migration with PRAGMA user_version)
- intel.db schema version 2 — Phase 69 will migrate to v3 (competitor_hooks table)
- sys.path.insert hacks REMOVED — all tools use proper absolute tools.* or relative imports
- spaCy requires Python 3.11-3.13 (not 3.14)
- MCP servers installed: Context7, Playwright
- CTR feedback loop: ctr_tracker.py + Windows Task Scheduler (weekly)
- One new dependency in v7.0: Pillow>=10.0.0 in [thumbnails] extras in pyproject.toml (Phase 70)

---

*State updated: 2026-03-16 after v7.0 roadmap created*
