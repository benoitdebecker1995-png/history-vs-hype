# State: History vs Hype Workspace

**Initialized:** 2025-01-19
**Last Updated:** 2026-02-14 (Phase 36 planned)

## Project Reference

See: `.planning/PROJECT.md` (updated 2026-02-12)

**Core value:** Every video shows sources on screen
**Current focus:** Phase 36 - Retention Science

## Current Position

**Milestone:** v3.0 Adaptive Scriptwriter
**Phase:** 36 of 38 (Retention Science)
**Plan:** 3 of 3 complete (36-01 ✓, 36-02 ✓, 36-03 ✓)
**Status:** Phase complete — ready for Phase 37
**Last activity:** 2026-02-14 — Completed 36-03 (feedback loop integration)

**Progress:**
v1.0 [####################] 100% — Workspace Optimization (archived)
v1.1 [####################] 100% — Analytics & Learning Loop (archived)
v1.2 [####################] 100% — Script Quality & Discovery (archived)
v1.3 [####################] 100% — Niche Discovery (archived)
v1.4 [####################] 100% — Learning Loop (archived)
v1.5 [####################] 100% — Production Acceleration (archived)
v1.6 [####################] 100% — Click & Keep (archived)
v2.0 [####################] 100% — Channel Intelligence (archived)
v3.0 [██████░░░░░░░░░░░░░░░] 33% — Adaptive Scriptwriter (in progress)

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

**Retention Playbook (v3.0 Phase 36):**
- `python tools/youtube-analytics/playbook_synthesizer.py` — dry run (print Part 9 to stdout)
- `python tools/youtube-analytics/playbook_synthesizer.py --update` — regenerate STYLE-GUIDE.md Part 9 from latest retention data
- `python tools/youtube-analytics/playbook_synthesizer.py --json` — output raw pattern data for debugging

**Retention Scoring (v3.0 Phase 36):**
- `python tools/youtube-analytics/retention_scorer.py SCRIPT_PATH --topic TYPE` — score script sections for retention risk
- Score thresholds: HIGH (<0.5), MEDIUM (0.5-0.7), LOW (>0.7)
- Scoring weights: evidence 35%, relevance 40%, length 20%, patterns +20% cap
- Topic baselines: 3-video threshold for topic-specific, falls back to channel avg or defaults
- Modern relevance markers use word boundaries to avoid false positives

## Session Continuity

### Last Session

- **Date:** 2026-02-14
- **Work:** Executed Plans 36-01, 36-02, and 36-03 (Phase 36 complete)
- **Output:**
  - 36-01: playbook_synthesizer.py (852 LOC), STYLE-GUIDE.md Part 9
  - 36-02: retention_scorer.py (674 LOC), test_retention_scorer.py (296 LOC, 13 tests passing)
  - 36-03: Feedback loop integration (script-writer-v2 Rule 15, /script retention scoring, /analyze playbook auto-update)
- **Commits:** e1de2b4, 935fff8 (36-01), 54ec88d, d69a67c (36-02), ba2aa81, c4b4ddd (36-03)

### Next Session

**Next action:** `/gsd:plan-phase 37` to plan next phase in v3.0 milestone

## Technical Notes

- YouTube Analytics API requires Google Cloud project (configured)
- OAuth2 token auto-refreshes (saved in credentials/token.json)
- CTR not available via API — graceful fallback prompts for manual entry
- spaCy requires Python 3.11-3.13 (not 3.14)
- Voice patterns require user to run `--rebuild-voice` to populate
- keywords.db schema version 27 (auto-migration with PRAGMA user_version)
- External packages (trendspyg, scrapetube) optional - graceful degradation
- Feature flags: VARIANTS_AVAILABLE, BENCHMARKS_AVAILABLE, FEEDBACK_AVAILABLE, DIAGNOSTICS_AVAILABLE, TOPIC_STRATEGY_AVAILABLE, PLAYBOOK_AVAILABLE, SCORER_AVAILABLE
- anthropic SDK required for notebooklm_bridge.py (`pip install anthropic>=0.40.0`)
- Retention mapping uses fixed 150 WPM for word-count timing
- Section diagnostics hardcode 29 voice patterns from STYLE-GUIDE.md Part 6
- Playbook synthesizer generates Part 9 from video_performance.lessons_learned (requires 3+ videos for patterns)
- STYLE-GUIDE.md Part 9 auto-updated with `python tools/youtube-analytics/playbook_synthesizer.py --update`

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

*State updated: 2026-02-14 after Phase 36 planned*
