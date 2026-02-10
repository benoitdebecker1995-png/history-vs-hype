# State: History vs Hype Workspace

**Initialized:** 2025-01-19
**Last Updated:** 2026-02-10 (v2.0 roadmap created)

## Project Reference

See: `.planning/PROJECT.md` (updated 2026-02-09)

**Core value:** Every video shows sources on screen
**Current focus:** Phase 33 - Voice Pattern Library

## Current Position

**Milestone:** v2.0 Channel Intelligence
**Phase:** 33 of 35 (Voice Pattern Library)
**Plan:** Planning phase
**Status:** Ready to plan
**Last activity:** 2026-02-10 — v2.0 roadmap created with 3 phases (33-35)

**Progress:**
v1.0 [####################] 100% — Workspace Optimization (archived)
v1.1 [####################] 100% — Analytics & Learning Loop (archived)
v1.2 [####################] 100% — Script Quality & Discovery (archived)
v1.3 [####################] 100% — Niche Discovery (archived)
v1.4 [####################] 100% — Learning Loop (archived)
v1.5 [####################] 100% — Production Acceleration (archived)
v1.6 [####################] 100% — Click & Keep (archived)
v2.0 [                    ] 0% — Channel Intelligence (0/3 phases)

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

**Full history:** `.planning/MILESTONES.md`
**Archives:** `.planning/milestones/`

## What's Available

**Workspace commands:**
- `/status` — project state and next action
- `/help` — phase-organized command list
- `/research --new` — start new video project
- `/next` — get ranked topic recommendations based on winning patterns

**Analytics commands (v1.1+v1.6):**
- `/analyze VIDEO_ID` — post-publish video analysis (+ variant tracking + CTR analysis + feedback insights)
- `/patterns` — cross-video pattern recognition (+ feedback patterns)

**Discovery commands (v1.2 + v1.3):**
- `/discover TOPIC` — keyword research workflow
- `/discover --demand "keyword"` — demand analysis with opportunity scoring
- `/discover --opportunity "topic"` — complete opportunity analysis (demand + competition + production)
- `/discover --check FILE` — pre-publish metadata validation

**Performance analysis (v1.4):**
- `python tools/youtube-analytics/performance.py --fetch-all` — fetch performance data for all videos
- `python tools/youtube-analytics/performance.py --patterns` — extract winning patterns
- `python tools/discovery/recommender.py` — get topic recommendations

**Script quality tools (v1.2+v1.6):**
- `python tools/script-checkers/cli.py script.md --all` — run all checkers
- `python tools/script-checkers/cli.py script.md --pacing` — pacing analysis
- `python tools/script-checkers/cli.py script.md --pacing --verbose` — full section-by-section breakdown

**Production tools (v1.5):**
- `python tools/production/parser.py script.md --package` — generate all outputs in one command

**CTR & Variant tools (v1.6):**
- `python tools/youtube-analytics/variants.py register-thumb VIDEO_ID A path.jpg --tags map,text` — register thumbnail
- `python tools/youtube-analytics/variants.py register-title VIDEO_ID A "Title" --tags mechanism` — register title
- `python tools/youtube-analytics/variants.py record-ctr VIDEO_ID 7.5 --date 2026-02-09` — record CTR
- `python tools/youtube-analytics/benchmarks.py compare VIDEO_ID` — CTR verdict
- `python tools/youtube-analytics/feedback.py backfill` — import POST-PUBLISH-ANALYSIS data
- `python tools/youtube-analytics/feedback.py query --topic territorial` — query insights
- `python tools/youtube-analytics/feedback.py patterns` — feedback pattern report

## Session Continuity

### Last Session

- **Date:** 2026-02-10
- **Work:** Created v2.0 roadmap with 3 phases
- **Output:** ROADMAP.md updated, STATE.md refreshed

### Next Session

**Current work:** v2.0 Channel Intelligence — Phase 33 Voice Pattern Library
**Next action:** `/gsd:plan-phase 33` to begin voice pattern implementation

## Accumulated Context

### v2.0 Roadmap Overview

**Phase 33: Voice Pattern Library** (VOICE-01 to VOICE-04)
- Goal: Scripts match creator's proven voice patterns
- Approach: Reference document expansion (STYLE-GUIDE.md Part 6)
- Zero new code required

**Phase 34: NotebookLM Research Bridge** (NLMB-01 to NLMB-03)
- Goal: Research workflow connects NotebookLM to verified research
- Approach: Format converters and source recommenders
- No API automation (manual workflow preserved)

**Phase 35: Actionable Analytics** (ACTN-01 to ACTN-04)
- Goal: Retention mapping with concrete fixes
- Approach: Map drops to script sections, generate recommendations
- Depends on Phase 33 (voice patterns for recommendations)

### Technical Notes

- YouTube Analytics API requires Google Cloud project (configured)
- OAuth2 token auto-refreshes (saved in credentials/token.json)
- CTR not available via API — graceful fallback prompts for manual entry
- spaCy requires Python 3.11-3.13 (not 3.14)
- Voice patterns require user to run `--rebuild-voice` to populate
- keywords.db schema version 27 (auto-migration with PRAGMA user_version)
- External packages (trendspyg, scrapetube) optional - graceful degradation
- Feature flags: VARIANTS_AVAILABLE, BENCHMARKS_AVAILABLE, FEEDBACK_AVAILABLE for graceful import

### Known Issues

**Python 3.14 Compatibility:**
- spaCy 3.8 dependency (Pydantic v1) incompatible with Python 3.14.2
- Stumble and flow checkers work on Python 3.11-3.13
- Scaffolding and repetition checkers work on all Python versions
- **v2.0 blocker:** Python 3.14 → 3.13 downgrade required before Phase 34/35 development

**Voice Fingerprinting Setup:**
- User must install srt library (`pip install srt`)
- User must run `--rebuild-voice` to populate patterns from corpus
- **v2.0 note:** Voice pattern extraction requires ≥5 transcripts for reliability

**External Package Dependencies:**
- trendspyg, scrapetube not installed — demand analysis degrades gracefully
- Unicode arrows may cause encoding issues on Windows cp1252 console

---

*State updated: 2026-02-10 after v2.0 roadmap creation*
