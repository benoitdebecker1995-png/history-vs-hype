# State: History vs Hype Workspace

**Initialized:** 2025-01-19
**Last Updated:** 2026-02-02 (Phase 20 Plan 01 complete)

## Project Reference

See: `.planning/PROJECT.md` (updated 2026-02-02)

**Core value:** Every video shows sources on screen
**Current focus:** v1.4 Learning Loop — Phase 20 Plan 01 complete

## Current Position

**Milestone:** v1.4 Learning Loop
**Phase:** 20 of 21 (Pattern Extraction) — IN PROGRESS
**Plan:** 01 of 01 complete
**Status:** Phase complete
**Last activity:** 2026-02-02 — Completed 20-01-PLAN.md (Pattern Extraction)

**Progress:**
```
v1.0 [####################] 100% — Workspace Optimization (archived)
v1.1 [####################] 100% — Analytics & Learning Loop (archived)
v1.2 [####################] 100% — Script Quality & Discovery (archived)
v1.3 [####################] 100% — Niche Discovery (archived)
v1.4 [##############      ]  67% — Learning Loop (Phase 20 complete)
```

## Milestone History

| Version | Name | Phases | Shipped |
|---------|------|--------|---------|
| v1.0 | Workspace Optimization | 0.1, 1-7 | 2026-01-23 |
| v1.1 | Analytics & Learning Loop | 8-10 | 2026-01-26 |
| v1.2 | Script Quality & Discovery | 11-14 | 2026-01-30 |
| v1.3 | Niche Discovery | 15-18 | 2026-02-02 |

**Full history:** `.planning/MILESTONES.md`
**Archives:** `.planning/milestones/`

## What's Available

**Workspace commands:**
- `/status` — project state and next action
- `/help` — phase-organized command list
- `/research --new` — start new video project

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

**Script quality tools (v1.2):**
- `python tools/script-checkers/cli.py script.md --all` — run all checkers
- `python tools/script-checkers/cli.py script.md --voice` — apply voice patterns

## Session Continuity

### Last Session

- **Date:** 2026-02-02
- **Work:** Completed Phase 20 Plan 01 (Pattern Extraction)
- **Output:**
  - pattern_extractor.py with 7 extraction functions
  - performance.py extended with --patterns and --strengths CLI flags
  - WINNING-PATTERNS.md report template generated
  - Channel strength scoring (document_heavy, academic, legal_territorial)

### Next Session

**Current work:** Plan Phase 21 (Topic Recommendations)

**v1.4 Goal:** "Based on everything — your performance, competition, skills, and constraints — here are the best topics to make next"

**Target features:**
- Performance analysis (subscriber conversion per video, winning patterns) - COMPLETE
- Pattern extraction (topic/angle rankings, channel strengths) - COMPLETE
- Competition integration (saturated vs underserved, quality gaps)
- Skills/strengths profiling (document-heavy, academic, legal/territorial) - COMPLETE
- Time/constraint awareness (solo creator, research overhead)
- Existing work filtering (exclude `_IN_PRODUCTION/` and `_ARCHIVED/`)
- Unified `/next` command with ranked opportunities

**Next action:** Plan Phase 21 with `/gsd:plan-phase 21`

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

### v1.3 Architecture Decisions

**Tech stack:**
- trendspyg for Google Trends data
- python-youtube for YouTube Data API v3
- scrapetube for quota-free video counting fallback
- keywords.db extended with 5 new tables (Plan 15-01 complete)

**Design patterns:**
- Follow error dict pattern from Phase 13
- Production constraint filtering FIRST (fail fast on animation-required)
- Track data staleness (trends expire, competition changes)
- Log raw candidates before filtering (validate filter accuracy later)
- Graceful degradation when external packages not installed

### Plan 15-01 Decisions

- **7-day cache default:** All cached data methods return `data_age_days` field
- **Conservative opportunity thresholds:** High >4x, Medium 2-4x, Low <2x
- **Linear position scoring:** Position 1=100, Position 10=10, Not found=0
- **Trend arrow thresholds:** >20% change for rising/declining, otherwise stable

### Plan 15-02 Decisions

- **60-second rate limit cooldown:** After Google Trends rate limit detection
- **100-video sample size:** Per RESEARCH.md pitfall 5, avoid slow full iteration
- **Top 20 video caching:** Store first 20 competitor videos to database
- **PACKAGE_AVAILABLE flags:** Check external package availability at import time

### Plan 16-01 Decisions

- **Channel-based format detection:** Use channel name as primary signal (stronger than title keywords)
- **Multi-angle support:** Videos can have multiple angle classifications (legal + historical)
- **JSON angle storage:** Store angles as JSON array in TEXT column (SQLite lacks native array type)
- **Automatic schema migration:** _ensure_classification_columns() adds columns if missing (zero-friction upgrade)

### Plan 16-02 Decisions

- **25th percentile quality threshold:** Balance filtering noise while retaining meaningful competition
- **Inverse frequency gap scoring:** 1.0 - frequency (higher = bigger opportunity, bounded 0-1)
- **Default channel angles ['legal', 'historical']:** Matches channel DNA from CLAUDE.md
- **Graceful degradation for database:** Classification works even if persistence unavailable

### Technical Notes (Phase 16)

- keywords.db schema extended with classification columns (format, angles, quality_tier, classified_at)
- Automatic migration from Phase 15 schema via _ensure_classification_columns()
- 13 animation channel keywords, 10 documentary channel keywords
- 5 angle categories with 73 total keywords (political, legal, historical, economic, geographic)
- JSON storage for angles list (parsed on retrieval)
- Quality tiers: high (>75th percentile), medium (25-75th), low (<25th)
- Gap scores: 0-1 where 1.0 = no competition, 0.0 = saturated

### Plan 17-01 Decisions

- **Keyword-based detection over ML:** Simple, deterministic, no external dependencies
- **Confidence scoring for mixed signals:** Lower confidence (0.5-0.6) when both animation and documentary keywords present
- **90-day default staleness:** Production constraints change slowly, longer cache than demand data
- **JSON storage for flexibility:** Can extend constraint fields without schema changes
- **is_production_blocked flag:** Quick boolean filter for animation-required topics

### Technical Notes (Phase 17)

- format_filters.py: 35+ animation keywords, 40+ documentary-safe keywords
- DOCUMENT_FRIENDLY_KEYWORDS with point values (+3 for treaty/court, +2 for law/colonial, +1 for war/history)
- CONCEPT_HEAVY_KEYWORDS with negative values (-2 for philosophy/theory, -1 for ideology)
- Baseline score 2, adds/subtracts, clamps to 0-4
- evaluate_production_constraints() combines both checks with recommendation

---

### Plan 17-02 Decisions

- **Query generation, not API calls:** No HTTP requests; generates search strings for manual use
- **Site-filtered searches:** Queries include site: filters for academic publishers
- **Confidence based on specificity:** More document-friendly keywords = higher confidence
- **ASCII-safe CLI output:** Avoids Unicode issues on Windows console

### Plan 18-01 Decisions

- **SAW formula with equal weights:** demand=0.33, gap=0.33, fit=0.34 (balanced starting point for validation)
- **Hard constraint pre-filtering:** Animation + channel DNA blocks return score=None (not 0), preventing wasted scoring effort
- **Lifecycle state machine:** Dictionary-based transition validation, reject invalid state changes
- **Category thresholds:** Excellent >=70, Good >=50, Fair >=30, Poor <30
- **Channel DNA violations:** Clickbait keywords, news-first patterns, politician-focus (starting with name only)
- **Component transparency:** Return normalized values, weights, contributions for each scoring factor

### Plan 18-02 Decisions

- **Jinja2 for report templates:** Separates logic from presentation, easy to maintain, with graceful fallback to simple formatting
- **ASCII-safe CLI output:** # and - for progress bars (avoid Unicode encoding issues on Windows cp1252 console)
- **5-step pipeline:** demand -> competition -> constraints -> scoring -> persistence (with auto-save and lifecycle transition)
- **Auto-transition to ANALYZED:** After scoring, keywords automatically move from DISCOVERED to ANALYZED state
- **Orchestrator pattern:** Single class coordinating multiple module calls with data aggregation (facade pattern)

### Plan 19-01 Decisions

- **Conversion formula:** (subscribers_gained / views) * 100, returns percentage
- **Topic classification:** Reuse TAG_VOCABULARY pattern from patterns.py for consistency
- **Angle classification:** Reuse classify_angles from Phase 16 (code reuse)
- **JSON angle storage:** Store angles as JSON TEXT (SQLite lacks native array type)
- **Auto-migration:** _ensure_performance_table() creates table on first access

### Technical Notes (Phase 19)

- video_performance table with indexes on conversion_rate, topic_type, fetched_at
- performance.py fetcher module integrates metrics.py + channel_averages.py
- CLI: `python performance.py --fetch-all` to populate database
- CLI: `python performance.py --top 10` to show top converters
- Graceful degradation when database unavailable

### Plan 20-01 Decisions

- **Strength normalization formula:** min(100, (category_avg / overall_avg) * 50)
- **Dominant extraction:** Counter.most_common() for finding dominant topics/angles
- **Insight generation:** Compare best vs average, best vs worst for actionable insights
- **ASCII progress bars:** # for filled, - for empty (Windows cp1252 safe)

### Technical Notes (Phase 20)

- pattern_extractor.py with 7 functions for pattern extraction
- Channel strengths: document_heavy, academic, legal_territorial (0-100 scores)
- CLI: `python performance.py --patterns` to extract and display patterns
- CLI: `python performance.py --patterns --save` to generate WINNING-PATTERNS.md
- CLI: `python performance.py --strengths` for focused strength view

---

*State updated: 2026-02-02 after 20-01-PLAN.md complete*
