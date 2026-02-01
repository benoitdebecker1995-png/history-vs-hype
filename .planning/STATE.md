# State: History vs Hype Workspace

**Initialized:** 2025-01-19
**Last Updated:** 2026-02-01 (Plan 18-01 complete)

## Project Reference

See: `.planning/PROJECT.md` (updated 2026-01-31)

**Core value:** Find high-potential topics with low competition that fit document-heavy format
**Current focus:** v1.3 Niche Discovery — Phase 18 (Opportunity Scoring)

## Current Position

**Milestone:** v1.3 Niche Discovery
**Phase:** 18 - Opportunity Scoring & Orchestrator
**Plan:** 18-01 complete (1 of 2 plans)
**Status:** In progress - Plan 18-01 done, ready for Plan 18-02
**Last activity:** 2026-02-01 — Completed 18-01-PLAN.md

**Progress:**
```
v1.0 [####################] 100% — Workspace Optimization (archived)
v1.1 [####################] 100% — Analytics & Learning Loop (archived)
v1.2 [####################] 100% — Script Quality & Discovery (archived)
v1.3 [#################   ]  85% — Niche Discovery (Phases 15-17 complete, 18-01 done)
```

## Milestone History

| Version | Name | Phases | Shipped |
|---------|------|--------|---------|
| v1.0 | Workspace Optimization | 0.1, 1-7 | 2026-01-23 |
| v1.1 | Analytics & Learning Loop | 8-10 | 2026-01-26 |
| v1.2 | Script Quality & Discovery | 11-14 | 2026-01-30 |

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
- `/discover --check FILE` — pre-publish metadata validation
- `python tools/discovery/competition.py "keyword"` — competition analysis with differentiation

**Script quality tools (v1.2):**
- `python tools/script-checkers/cli.py script.md --all` — run all checkers
- `python tools/script-checkers/cli.py script.md --voice` — apply voice patterns

## Session Continuity

### Last Session

- **Date:** 2026-02-01
- **Work:** Completed Plan 18-01 (Opportunity Scoring)
- **Output:**
  - OpportunityScorer with SAW formula (demand × 0.33 + gap × 0.33 + fit × 0.34)
  - Channel DNA filtering (blocks clickbait, news-first, politician-focus)
  - Lifecycle state tracking (DISCOVERED -> ANALYZED -> ... -> PUBLISHED -> ARCHIVED)
  - Database extended with lifecycle_state, lifecycle_history table
  - Commits: 6c2c30a, 2de2e86

### Next Session

**Current work:** Phase 18 Plan 01 complete, ready for Plan 18-02

**Plan 18-01 complete:**
- ✅ OPP-01 partial: Opportunity score calculation implemented
- ✅ OPP-02: Production constraints weighted in scoring
- ✅ OPP-03: Channel DNA rules auto-filter topics
- ✅ OPP-04 partial: Lifecycle states defined and tracked

**Next action:** Execute Plan 18-02 (Orchestrator + CLI + Report Generation)

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

---

*State updated: 2026-02-01 after Plan 18-01 complete*
