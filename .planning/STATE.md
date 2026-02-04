# State: History vs Hype Workspace

**Initialized:** 2025-01-19
**Last Updated:** 2026-02-04 (Phase 24-01 complete)

## Project Reference

See: `.planning/PROJECT.md` (updated 2026-02-03)

**Core value:** Every video shows sources on screen
**Current focus:** v1.5 Production Acceleration — Phase 24 complete, ready for Phase 25

## Current Position

**Milestone:** v1.5 Production Acceleration
**Phase:** 24 - Edit Guide Generation
**Plan:** 01 complete
**Status:** Phase 24 complete
**Last activity:** 2026-02-04 — Completed 24-01-PLAN.md (Edit Guide Generation)

**Progress:**
```
v1.0 [####################] 100% — Workspace Optimization (archived)
v1.1 [####################] 100% — Analytics & Learning Loop (archived)
v1.2 [####################] 100% — Script Quality & Discovery (archived)
v1.3 [####################] 100% — Niche Discovery (archived)
v1.4 [####################] 100% — Learning Loop (archived)
v1.5 [##########----------]  50% — Production Acceleration (ACTIVE)
     Phase 22: Script Parser [####] 100%
     Phase 23: B-Roll Gen    [####] 100%
     Phase 24: Edit Guide    [####] 100%
     Phase 25: Metadata      [----] 0%
     Phase 26: Package Cmd   [----] 0%
```

## Milestone History

| Version | Name | Phases | Shipped |
|---------|------|--------|---------|
| v1.0 | Workspace Optimization | 0.1, 1-7 | 2026-01-23 |
| v1.1 | Analytics & Learning Loop | 8-10 | 2026-01-26 |
| v1.2 | Script Quality & Discovery | 11-14 | 2026-01-30 |
| v1.3 | Niche Discovery | 15-18 | 2026-02-02 |
| v1.4 | Learning Loop | 19-21 | 2026-02-02 |

**Full history:** `.planning/MILESTONES.md`
**Archives:** `.planning/milestones/`

## What's Available

**Workspace commands:**
- `/status` — project state and next action
- `/help` — phase-organized command list
- `/research --new` — start new video project
- `/next` — get ranked topic recommendations based on winning patterns

**Analytics commands (v1.1):**
- `/analyze VIDEO_ID` — post-publish video analysis
- `/patterns` — cross-video pattern recognition

**Discovery commands (v1.2 + v1.3):**
- `/discover TOPIC` — keyword research workflow
- `/discover --demand "keyword"` — demand analysis with opportunity scoring
- `/discover --opportunity "topic"` — complete opportunity analysis (demand + competition + production)
- `/discover --check FILE` — pre-publish metadata validation
- `python tools/discovery/orchestrator.py "keyword"` — complete niche discovery with Markdown reports
- `python tools/discovery/competition.py "keyword"` — competition analysis with differentiation

**Performance analysis (v1.4):**
- `python tools/youtube-analytics/performance.py --fetch-all` — fetch performance data for all videos
- `python tools/youtube-analytics/performance.py --patterns` — extract winning patterns
- `python tools/youtube-analytics/performance.py --strengths` — show channel strength scores
- `python tools/discovery/recommender.py` — get topic recommendations

**Script quality tools (v1.2):**
- `python tools/script-checkers/cli.py script.md --all` — run all checkers
- `python tools/script-checkers/cli.py script.md --voice` — apply voice patterns

**Production tools (v1.5 - NEW):**
- `python tools/production/parser.py script.md` — parse script, show sections and entities
- `python tools/production/parser.py script.md --broll` — generate B-roll checklist from script
- `python tools/production/parser.py script.md --edit-guide` — generate EDITING-GUIDE.md with timing

## Session Continuity

### Last Session

- **Date:** 2026-02-04
- **Work:** Completed Phase 24-01 Edit Guide Generation
- **Output:**
  - EditGuideGenerator class generates complete EDITING-GUIDE.md format
  - Duration calculation at 150 WPM with 10-second minimum
  - Cumulative timing with MM:SS formatted start/end times
  - Shot-by-shot breakdown grouping B-roll and talking head entries
  - Visual assets checklist auto-generated from shot priorities
  - CLI: `python tools/production/parser.py script.md --edit-guide`
  - Integration tested: Chagos script (91 shots, 10:53 runtime, 12 sections)

### Next Session

**Current work:** Phase 25 - Metadata Generation

**Phase 25 Goal:** Generate YouTube metadata (titles, descriptions, tags) from scripts

**Dependencies available:**
- ScriptParser: `from tools.production import ScriptParser`
- EntityExtractor: `from tools.production import EntityExtractor`
- BRollGenerator: `from tools.production import BRollGenerator`
- EditGuideGenerator: `from tools.production import EditGuideGenerator`
- Section/Entity/Shot/SectionTiming dataclasses for structured data

**Next action:** Create 25-01-PLAN.md for metadata generation implementation

## Accumulated Context

### Technical Notes

- YouTube Analytics API requires Google Cloud project (configured)
- OAuth2 token auto-refreshes (saved in credentials/token.json)
- CTR not available via API — graceful fallback prompts for manual entry
- spaCy requires Python 3.11-3.13 (not 3.14)
- Voice patterns require user to run `--rebuild-voice` to populate
- keywords.db schema extended in Phase 15-01 with 5 demand tables
- External packages (trendspyg, scrapetube) optional - graceful degradation

### Known Issues

**Python 3.14 Compatibility:**
- spaCy 3.8 dependency (Pydantic v1) incompatible with Python 3.14.2
- Stumble and flow checkers work on Python 3.11-3.13
- Scaffolding and repetition checkers work on all Python versions

**Voice Fingerprinting Setup:**
- User must install srt library (`pip install srt`)
- User must run `--rebuild-voice` to populate patterns from corpus

**External Package Dependencies (Plan 15-02):**
- trendspyg, scrapetube not installed — demand analysis degrades gracefully
- Unicode arrows may cause encoding issues on Windows cp1252 console

### v1.4 Architecture Decisions

**Phase 19-01 Decisions:**
- **Conversion formula:** (subscribers_gained / views) * 100, returns percentage
- **Topic classification:** Reuse TAG_VOCABULARY pattern from patterns.py for consistency
- **Angle classification:** Reuse classify_angles from Phase 16 (code reuse)
- **JSON angle storage:** Store angles as JSON TEXT (SQLite lacks native array type)
- **Auto-migration:** _ensure_performance_table() creates table on first access

**Phase 20-01 Decisions:**
- **Strength normalization formula:** min(100, (category_avg / overall_avg) * 50)
- **Dominant extraction:** Counter.most_common() for finding dominant topics/angles
- **Insight generation:** Compare best vs average, best vs worst for actionable insights
- **ASCII progress bars:** # for filled, - for empty (Windows cp1252 safe)

**Phase 21-01 Decisions:**
- **Topic matching:** Word-level comparison, not substring (prevent false positives)
- **Multiplier cap:** Maximum 1.5x boost (prevent overwhelming opportunity score)
- **Exclusion sources:** Scan _IN_PRODUCTION/ and _ARCHIVED/ folders
- **Graceful degradation:** Proceed with multiplier=1.0 if pattern extraction fails

### Technical Notes (v1.4)

- video_performance table with indexes on conversion_rate, topic_type, fetched_at
- performance.py integrates metrics.py + channel_averages.py for conversion tracking
- pattern_extractor.py provides winning patterns for recommendation scoring
- recommender.py scans video-projects/ folders and excludes existing topics
- `/next` command documentation at `.claude/commands/next.md`

### v1.5 Architecture Decisions

**Phase 22-01 Decisions:**
- **Module location:** tools/production/ for all production acceleration tools
- **Entity extraction approach:** Hybrid regex + optional spaCy (use_spacy=True)
- **Section type inference:** Position-based (first=intro, last=conclusion) with keyword override
- **Word count calculation:** Strip all B-roll markers before counting spoken words
- **Entity deduplication:** Normalize (lowercase, strip "the ", collapse whitespace), merge by key
- **Person blocklist:** Filter marker-derived false positives (talking head, text on screen, etc.)

**Phase 22-01 Patterns Established:**
- Lazy spaCy loading with graceful fallback to regex-only
- Domain-specific keyword dictionaries for classification
- Marker stripping before both word count and entity extraction

**Phase 23-01 Decisions:**
- **Source URLs:** Use search URLs instead of fabricated file paths (safe, always valid)
- **Archive hierarchy:** Organized by topic category (holocaust, legal, medieval, colonial, general)
- **Priority thresholds:** 3+ mentions for documents, 5+ mentions for maps/portraits → Priority 1
- **DIY instructions:** MapChart.net for maps (free, zero-budget friendly)
- **Visual type classification:** Keyword detection (maritime → strategic_map, territory → map)

**Phase 23-01 Patterns Established:**
- Shot dataclass pattern: entity + visual_type + priority + source_urls + diy_instructions + section_references
- Topic detection: Aggregate entity text, check keyword matches, return category
- Priority assignment: Type-specific thresholds based on mention counts
- Markdown output: Group by visual type, include DIY instructions, priority checklist at end

**Phase 24-01 Decisions:**
- **150 WPM timing standard:** Industry standard speaking rate for video narration
- **10-second minimum:** Prevents unrealistic sub-10-second estimates for brief transitions
- **MM:SS formatting:** Matches video editing software conventions
- **UTF-8 encoding on Windows:** Platform-specific stdout setup to handle unicode characters
- **Section-to-shot mapping:** Uses BRollGenerator section_references field for logical grouping

**Phase 24-01 Patterns Established:**
- SectionTiming dataclass tracks cumulative start/end times for each section
- Shot-by-shot breakdown groups shots by section for logical flow
- Visual assets checklist auto-generated from shot priorities
- Edit guide format matches existing EDITING-GUIDE.md structure
- calculate_duration_seconds(word_count) → estimated seconds at 150 WPM
- format_time(seconds) → MM:SS string

---

*State updated: 2026-02-04 after Phase 24-01 complete*
