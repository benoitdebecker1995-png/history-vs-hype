# State: History vs Hype Workspace

**Initialized:** 2025-01-19
**Last Updated:** 2026-02-13 (v3.0 roadmap created)

## Project Reference

See: `.planning/PROJECT.md` (updated 2026-02-12)

**Core value:** Every video shows sources on screen
**Current focus:** Phase 36 - Retention Science

## Current Position

**Milestone:** v3.0 Adaptive Scriptwriter
**Phase:** 36 of 38 (Retention Science)
**Plan:** Ready to plan
**Status:** Ready to plan Phase 36
**Last activity:** 2026-02-13 — v3.0 roadmap created

**Progress:**
v1.0 [####################] 100% — Workspace Optimization (archived)
v1.1 [####################] 100% — Analytics & Learning Loop (archived)
v1.2 [####################] 100% — Script Quality & Discovery (archived)
v1.3 [####################] 100% — Niche Discovery (archived)
v1.4 [####################] 100% — Learning Loop (archived)
v1.5 [####################] 100% — Production Acceleration (archived)
v1.6 [####################] 100% — Click & Keep (archived)
v2.0 [####################] 100% — Channel Intelligence (archived)
v3.0 [░░░░░░░░░░░░░░░░░░░░] 0% — Adaptive Scriptwriter (in progress)

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
| v3.0 | Adaptive Scriptwriter | 36-38 | In progress |

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

**Performance analysis (v1.4):**
- `python tools/youtube-analytics/performance.py --fetch-all` — fetch performance data for all videos
- `python tools/youtube-analytics/performance.py --patterns` — extract winning patterns
- `python tools/discovery/recommender.py` — get topic recommendations

**Script quality tools (v1.2+v1.6):**
- `python tools/script-checkers/cli.py script.md --all` — run all checkers
- `python tools/script-checkers/cli.py script.md --pacing` — pacing analysis

**Production tools (v1.5):**
- `python tools/production/parser.py script.md --package` — generate all outputs in one command

**CTR & Variant tools (v1.6):**
- `python tools/youtube-analytics/variants.py register-thumb VIDEO_ID A path.jpg --tags map,text`
- `python tools/youtube-analytics/benchmarks.py compare VIDEO_ID` — CTR verdict
- `python tools/youtube-analytics/feedback.py backfill` — import POST-PUBLISH-ANALYSIS data

**NotebookLM Research Bridge (v2.0):**
- `python tools/notebooklm_bridge.py "TOPIC" --type TYPE --output DIR` — generate academic source list
- `python tools/citation_extractor.py nlm-output.txt --format detailed` — extract NotebookLM citations
- `.claude/REFERENCE/NOTEBOOKLM-RESEARCH-PROMPTS.md` — copy-paste research prompts

**Actionable Analytics (v2.0):**
- `python tools/youtube-analytics/retention_mapper.py` — map retention drops to script sections
- `python tools/youtube-analytics/section_diagnostics.py` — diagnose retention drops with pattern recommendations
- `python tools/youtube-analytics/topic_strategy.py` — aggregate performance by topic type
- `python tools/youtube-analytics/feedback_queries.py` — query pre-script insights

## Session Continuity

### Last Session

- **Date:** 2026-02-13
- **Work:** Created v3.0 roadmap
- **Output:** ROADMAP.md updated with Phases 36-38, REQUIREMENTS.md traceability updated

### Next Session

**Next action:** `/gsd:plan-phase 36` to create Phase 36 plan

## Technical Notes

- YouTube Analytics API requires Google Cloud project (configured)
- OAuth2 token auto-refreshes (saved in credentials/token.json)
- CTR not available via API — graceful fallback prompts for manual entry
- spaCy requires Python 3.11-3.13 (not 3.14)
- Voice patterns require user to run `--rebuild-voice` to populate
- keywords.db schema version 27 (auto-migration with PRAGMA user_version)
- External packages (trendspyg, scrapetube) optional - graceful degradation
- Feature flags: VARIANTS_AVAILABLE, BENCHMARKS_AVAILABLE, FEEDBACK_AVAILABLE, DIAGNOSTICS_AVAILABLE, TOPIC_STRATEGY_AVAILABLE
- anthropic SDK required for notebooklm_bridge.py (`pip install anthropic>=0.40.0`)
- Retention mapping uses fixed 150 WPM for word-count timing
- Section diagnostics hardcode 29 voice patterns from STYLE-GUIDE.md Part 6

## Known Issues

**Python 3.14 Compatibility:**
- spaCy 3.8 dependency (Pydantic v1) incompatible with Python 3.14.2
- Stumble and flow checkers work on Python 3.11-3.13
- Scaffolding and repetition checkers work on all Python versions

**Voice Fingerprinting Setup:**
- User must install srt library (`pip install srt`)
- User must run `--rebuild-voice` to populate patterns from corpus

**External Package Dependencies:**
- trendspyg, scrapetube not installed — demand analysis degrades gracefully
- Unicode arrows may cause encoding issues on Windows cp1252 console

---

*State updated: 2026-02-13 after v3.0 roadmap created*
