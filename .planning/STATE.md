# State: History vs Hype Workspace

**Initialized:** 2025-01-19
**Last Updated:** 2026-02-11 (Phase 35 complete: Actionable Analytics)

## Project Reference

See: `.planning/PROJECT.md` (updated 2026-02-09)

**Core value:** Every video shows sources on screen
**Current focus:** v2.0 Channel Intelligence — Phase 35 next

## Current Position

**Milestone:** v2.0 Channel Intelligence
**Phase:** 35 of 35 (Actionable Analytics)
**Plan:** 03 of 03 complete (all plans complete)
**Status:** Complete
**Last activity:** 2026-02-11 — Completed 35-03: Command Integration (wired retention diagnostics into /analyze --script and pre-script insights into /script)

**Progress:**
[██████████] 100%
v1.1 [####################] 100% — Analytics & Learning Loop (archived)
v1.2 [####################] 100% — Script Quality & Discovery (archived)
v1.3 [####################] 100% — Niche Discovery (archived)
v1.4 [####################] 100% — Learning Loop (archived)
v1.5 [####################] 100% — Production Acceleration (archived)
v1.6 [####################] 100% — Click & Keep (archived)
v2.0 [####################] 100% — Channel Intelligence (all 3 phases complete)

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

- **Date:** 2026-02-11
- **Work:** Completed Phase 35 Plan 02 (Topic Strategy Aggregation & Pre-Script Insights)
- **Output:** topic_strategy.py, extended feedback_queries.py with get_pre_script_insights()

### Next Session

**Current work:** v2.0 Channel Intelligence milestone complete
**Next action:** Ship v2.0 or start new milestone with `/gsd:new-milestone`

**Phase 35 Progress (COMPLETE):**
- ✅ 35-01 complete: Retention Mapper & Section Diagnostics
  - retention_mapper.py (275 LOC) — Maps retention drops to script sections
  - section_diagnostics.py (448 LOC) — Diagnoses anti-patterns, recommends patterns
  - Commits: 3e19cba, 0872f64
- ✅ 35-02 complete: Topic Strategy & Pre-Script Insights
  - topic_strategy.py (537 LOC) — Aggregates performance by topic with confidence flags
  - feedback_queries.py extended (+242 lines) — get_pre_script_insights()
  - Commits: 952bc13, 799efde
- ✅ 35-03 complete: Command Integration
  - analyze.py extended (+127 LOC) — generate_section_diagnostics with --script flag
  - .claude/commands/analyze.md — SECTION-LEVEL RETENTION DIAGNOSTICS documentation
  - .claude/commands/script.md — PRE-SCRIPT INTELLIGENCE documentation
  - Commits: 3edc5aa, 1899527, 61f9ed5

**Phase 34 Progress (COMPLETE):**
- ✅ 34-01 complete: Academic Source List Generator
  - notebooklm_bridge.py (316 LOC) — Claude API source generation
  - /sources --generate command added
  - Commits: fc7c4d1, 0880481
- ✅ 34-02 complete: Citation Extractor + Prompt Library
  - citation_extractor.py (356 LOC) — regex-based NotebookLM parsing
  - NOTEBOOKLM-RESEARCH-PROMPTS.md (404 lines) — 5+ core prompts
  - /verify --extract-nlm command added
  - Commits: 98ee560, 1e82cf0, 402139d

**Phase 33 Progress (COMPLETE):**
- ✅ 33-01 complete: Voice Pattern Library extracted
  - 22 patterns documented with formulas, examples, templates
  - STYLE-GUIDE.md Part 6 created, Part 7 renumbered
  - Commit: 6e404b5
- ✅ 33-02 complete: Agent integration
  - script-writer-v2 Rule 14 added (Part 6 pattern application)
  - Commit: a395c6d

## Accumulated Context

### v2.0 Roadmap Overview

**Phase 33: Voice Pattern Library** (VOICE-01 to VOICE-04) ✅ COMPLETE
- Goal: Scripts match creator's proven voice patterns
- Approach: Reference document expansion (STYLE-GUIDE.md Part 6)
- Zero new code required
- Output: 22 patterns + agent integration

**Phase 34: NotebookLM Research Bridge** (NLMB-01 to NLMB-03) ✅ COMPLETE
- Goal: Research workflow connects NotebookLM to verified research
- Approach: Python CLI tools + reference doc + command updates
- Output: notebooklm_bridge.py + citation_extractor.py + prompt library

**Phase 35: Actionable Analytics** (ACTN-01 to ACTN-04) ✅ COMPLETE
- Goal: Retention mapping with concrete fixes
- Approach: Map drops to script sections, generate recommendations
- Depends on Phase 33 (voice patterns for recommendations)
- ✅ 35-01 complete: Retention Mapper & Section Diagnostics
  - retention_mapper.py (275 LOC) — Maps retention drops to script sections via word-count timing
  - section_diagnostics.py (448 LOC) — Diagnoses anti-patterns, recommends STYLE-GUIDE.md Part 6 patterns
  - Hardcoded 22 voice patterns for stability (5 openings, 8 transitions, 5 evidence, 4 rhythm)
  - Severity: HIGH >10%, MEDIUM 5-10%, LOW <5%
  - Commits: 3e19cba, 0872f64
- ✅ 35-02 complete: Topic Strategy & Pre-Script Insights
  - topic_strategy.py (537 LOC) — Aggregates performance by topic with confidence flags
  - feedback_queries.py extended (+242 lines) — get_pre_script_insights()
  - Commits: 952bc13, 799efde
- ✅ 35-03 complete: Command Integration
  - analyze.py extended (+127 LOC) — generate_section_diagnostics with --script flag
  - /analyze --script documentation, /script pre-intelligence documentation
  - Commits: 3edc5aa, 1899527, 61f9ed5

### Technical Notes

- YouTube Analytics API requires Google Cloud project (configured)
- OAuth2 token auto-refreshes (saved in credentials/token.json)
- CTR not available via API — graceful fallback prompts for manual entry
- spaCy requires Python 3.11-3.13 (not 3.14)
- Voice patterns require user to run `--rebuild-voice` to populate
- keywords.db schema version 27 (auto-migration with PRAGMA user_version)
- External packages (trendspyg, scrapetube) optional - graceful degradation
- Feature flags: VARIANTS_AVAILABLE, BENCHMARKS_AVAILABLE, FEEDBACK_AVAILABLE for graceful import
- anthropic SDK required for notebooklm_bridge.py (`pip install anthropic>=0.40.0`)
- Retention mapping uses fixed 150 WPM for word-count timing (good enough for diagnostics)
- Section diagnostics hardcode 22 voice patterns from STYLE-GUIDE.md Part 6 (stable, no runtime parsing)

### Known Issues

**Python 3.14 Compatibility:**
- spaCy 3.8 dependency (Pydantic v1) incompatible with Python 3.14.2
- Stumble and flow checkers work on Python 3.11-3.13
- Scaffolding and repetition checkers work on all Python versions

**Voice Fingerprinting Setup:**
- User must install srt library (`pip install srt`)
- User must run `--rebuild-voice` to populate patterns from corpus
- **v2.0 note:** Voice pattern extraction requires ≥5 transcripts for reliability

**External Package Dependencies:**
- trendspyg, scrapetube not installed — demand analysis degrades gracefully
- Unicode arrows may cause encoding issues on Windows cp1252 console

---

*State updated: 2026-02-11 after Phase 34 completion*
