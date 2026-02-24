# State: History vs Hype Workspace

**Initialized:** 2025-01-19
**Last Updated:** 2026-02-24 (v5.1 milestone started)

## Project Reference

See: `.planning/PROJECT.md` (updated 2026-02-22)

**Core value:** Every video shows sources on screen
**Current focus:** v5.1 Codebase Hardening

## Current Position

**Milestone:** v5.1 Codebase Hardening
**Phase:** Not started (defining requirements)
**Status:** Defining requirements
**Last activity:** 2026-02-24 — Milestone v5.1 started

**Progress:**
[░░░░░░░░░░] 0%

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

**Full history:** `.planning/MILESTONES.md`
**Archives:** `.planning/milestones/`

## What's Available

**Workspace commands:**
- `/status` — project state and next action
- `/help` — phase-organized command list
- `/research --new` — start new video project
- `/next` — get ranked topic recommendations based on winning patterns

**Analytics commands (v1.1+v1.6+v2.0):**
- `/analyze VIDEO_ID` — post-publish video analysis (+ variant tracking + CTR analysis + feedback insights + section diagnostics)
- `/analyze VIDEO_ID --script PATH` — section-level retention diagnostics with voice pattern recommendations
- `/patterns` — cross-video pattern recognition (+ feedback patterns)

**Discovery commands (v1.2 + v1.3):**
- `/discover TOPIC` — keyword research workflow
- `/discover --demand "keyword"` — demand analysis with opportunity scoring
- `/discover --opportunity "topic"` — complete opportunity analysis (demand + competition + production)
- `/discover --check FILE` — pre-publish metadata validation

**Full command list:** Run `/help`

## Accumulated Context

v5.0 decisions archived in PROJECT.md Key Decisions table. See `.planning/milestones/v5.0-ROADMAP.md` for full phase details.

## Session Continuity

### Last Session

- **Date:** 2026-02-24
- **Work:** Started v5.1 Codebase Hardening milestone — requirements and roadmap definition
- **Output:** PROJECT.md and STATE.md updated for v5.1

### Next Session

**Next action:** `/gsd:plan-phase 48` — plan first phase

## Technical Notes

- YouTube Analytics API requires Google Cloud project (configured)
- OAuth2 token auto-refreshes (saved in credentials/token.json)
- keywords.db schema version 29 (auto-migration with PRAGMA user_version)
- Feature flags: VARIANTS_AVAILABLE, BENCHMARKS_AVAILABLE, FEEDBACK_AVAILABLE, DIAGNOSTICS_AVAILABLE, TOPIC_STRATEGY_AVAILABLE, PLAYBOOK_AVAILABLE, SCORER_AVAILABLE
- anthropic SDK required for notebooklm_bridge.py (`pip install anthropic>=0.40.0`)
- spaCy requires Python 3.11-3.13 (not 3.14)

## Known Issues

- Python 3.14 + spaCy incompatibility (use 3.11-3.13)
- Voice patterns empty until user runs --rebuild-voice
- trendspyg, scrapetube not installed (graceful degradation)

---

*State updated: 2026-02-19 after v5.0 roadmap created*
