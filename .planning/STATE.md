# State: History vs Hype Workspace

**Initialized:** 2025-01-19
**Last Updated:** 2026-02-17 (Phase 39 complete)

## Project Reference

See: `.planning/PROJECT.md` (updated 2026-02-16)

**Core value:** Every video shows sources on screen
**Current focus:** v4.0 Untranslated Evidence Pipeline - Phase 39

## Current Position

**Milestone:** v4.0 Untranslated Evidence Pipeline
**Phase:** 39 of 41 (Document Discovery & Format Guide) - COMPLETE
**Plan:** Ready for Phase 40
**Status:** Milestone complete
**Last activity:** 2026-02-17 — Completed 39-02: Format reference guide (712 lines, 4 sections, episode structure + visual standards + quality bar + tone rules)

**Progress:**
[██████████] 97%
v1.1 [####################] 100% — Analytics & Learning Loop (archived)
v1.2 [####################] 100% — Script Quality & Discovery (archived)
v1.3 [####################] 100% — Niche Discovery (archived)
v1.4 [####################] 100% — Learning Loop (archived)
v1.5 [####################] 100% — Production Acceleration (archived)
v1.6 [####################] 100% — Click & Keep (archived)
v2.0 [####################] 100% — Channel Intelligence (archived)
v3.0 [####################] 100% — Adaptive Scriptwriter (shipped 2026-02-15)
v4.0 [█████░░░░░░░░░░░░░░░] 25% — Untranslated Evidence Pipeline (in progress)

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
| v4.0 | Untranslated Evidence Pipeline | 39-41 | In progress |

**Full history:** `.planning/MILESTONES.md`
**Archives:** `.planning/milestones/`

## v4.0 Roadmap Summary

**Milestone Goal:** Build the document translation-to-video pipeline for "Untranslated Evidence" series

**Phase Structure:**
- **Phase 39**: Document Discovery & Format Guide (4 requirements: DISC-01,02,03 + SCPT-03)
  - Success: Verify translation gaps, assess document structure, locate digitized originals, reference guide created
- **Phase 40**: Translation Pipeline (5 requirements: TRAN-01,02,03,04,05)
  - Success: Claude translation + DeepL cross-check + legal term annotation + surprise clause detection + split-screen formatting
- **Phase 41**: Verification & Production Integration (8 requirements: VERF-01,02,03 + SCPT-01,02 + PROD-01,02,03)
  - Success: /verify --translation mode, document-structured script generation, split-screen edit guides

**Coverage:** 16/16 requirements mapped (100%)

**Key Decisions:**
- Phase 39: Foundation for document sourcing, gap verification, and series format standards
- Phase 40: Core new capability — AI translation pipeline with multi-tool cross-checking
- Phase 41: Integration into existing commands (/verify, /script, /prep)

**Next action:** Plan Phase 39 — document discovery tools and format reference guide

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

**Creator Transcript Analysis (v3.0 Phase 37):**
- `python tools/youtube-analytics/transcript_analyzer.py --analyze-all` — batch analyze all transcripts (83 files)
- `python tools/youtube-analytics/transcript_analyzer.py --analyze FILE` — single file analysis
- `python tools/youtube-analytics/transcript_analyzer.py --stats` — transcript distribution stats
- `python tools/youtube-analytics/technique_library.py --store-from FILE` — store analysis results
- `python tools/youtube-analytics/technique_library.py --list [CATEGORY]` — list techniques
- `python tools/youtube-analytics/technique_library.py --search QUERY` — search techniques
- `python tools/youtube-analytics/technique_library.py --stats` — database statistics

**Choice Architecture (v3.0 Phase 38):**
- `python tools/youtube-analytics/technique_library.py --choices [TOPIC]` — view logged script choices
- `python tools/youtube-analytics/technique_library.py --choice-stats` — choice statistics by type/topic

## Decisions

**Phase 39 Plan 01 (Document Discovery Toolkit):**
- Language-agnostic design from the start (works for French, Spanish, Latin, German documents)
- Academic editions prioritized in archive lookups (critical editions with scholarly apparatus preferred)
- Video length estimates reflect channel philosophy: "As long as needed — optimize for completeness, not brevity"
- Full vs excerpt flexibility: both full-document and excerpt-based estimates provided

## Session Continuity

### Last Session

- **Date:** 2026-02-17
- **Work:** Completed Phase 39 (Document Discovery & Format Guide)
- **Output:**
  - **Plan 39-01:** Document discovery toolkit (gap checker, structure assessor, archive lookup)
  - **Plan 39-02:** Format reference guide (712 lines, 4 sections)
  - Translation gap verification module (searches Google Scholar, JSTOR, Academia.edu)
  - Document structure assessment (article counting, video length estimation)
  - Archive lookup with 14+ sources (Légifrance, Wikisource, IA, national archives, HathiTrust, etc.)
  - Episode structure template: 5-part flow (hook, intro, walkthrough, synthesis, relevance)
  - Split-screen visual approach without locked layout
  - Translation cross-check protocol (Claude + DeepL/Google)
  - Commits: ce2dd3c (39-01), f664262 (39-02)
- **Delivered:** All 4 Phase 39 requirements (DISC-01, DISC-02, DISC-03, SCPT-03)

### Next Session

**Next action:** Plan Phase 40 — Translation Pipeline

**Phase 40 scope:**
- TRAN-01: Primary translation (Claude/LLM with context awareness)
- TRAN-02: Cross-check verification (DeepL, Google Translate comparison)
- TRAN-03: Legal term annotation (historical dictionaries, etymology)
- TRAN-04: Surprise clause detection (compare to English-language narratives)
- TRAN-05: Split-screen formatting (parallel display output for editing)

**Success criteria to deliver:**
1. User can translate documents with Claude maintaining legal/historical context
2. User can cross-check translations against multiple independent sources
3. User can annotate legal/technical terms with historical definitions
4. User can detect clauses that contradict common English narratives
5. User can generate split-screen formatted output for video editing

## Technical Notes

- YouTube Analytics API requires Google Cloud project (configured)
- OAuth2 token auto-refreshes (saved in credentials/token.json)
- CTR not available via API — graceful fallback prompts for manual entry
- spaCy requires Python 3.11-3.13 (not 3.14)
- Voice patterns require user to run `--rebuild-voice` to populate
- keywords.db schema version 29 (auto-migration with PRAGMA user_version)
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

*State updated: 2026-02-16 after v4.0 roadmap creation*
