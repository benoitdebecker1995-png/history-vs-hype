# State: History vs Hype Workspace

**Initialized:** 2025-01-19
**Last Updated:** 2026-02-01 (Plan 16-02 complete)

## Project Reference

See: `.planning/PROJECT.md` (updated 2026-01-31)

**Core value:** Find high-potential topics with low competition that fit document-heavy format
**Current focus:** v1.3 Niche Discovery — Phase 16 (Competition Analysis)

## Current Position

**Milestone:** v1.3 Niche Discovery
**Phase:** 16 - Competition Analysis
**Plan:** 2 of 2
**Status:** Phase 16 complete (competition analysis with differentiation scoring)
**Last activity:** 2026-02-01 — Completed 16-02-PLAN.md (quality filtering + gap analysis + CLI)

**Progress:**
```
v1.0 [####################] 100% — Workspace Optimization (archived)
v1.1 [####################] 100% — Analytics & Learning Loop (archived)
v1.2 [####################] 100% — Script Quality & Discovery (archived)
v1.3 [########            ]  40% — Niche Discovery (Phase 15-16 complete)
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
- **Work:** Executed Plan 16-02 (Differentiation Analysis)
- **Output:**
  - Added filter_quality_competition() with percentile-based filtering
  - Added calculate_differentiation_score() for gap analysis
  - Extended CompetitionAnalyzer with analyze_competition() method
  - Created CLI tool with pretty output and JSON mode
  - Updated discover.md with competition analysis documentation
  - Commits: c42baa2, 3e4e22f, 9e48653, 9376b50

### Next Session

**Current work:** Phase 16 complete

**Phase 16 delivered:**
- Classification foundation (format/angle detection)
- Quality filtering (percentile-based)
- Differentiation scoring (gap analysis)
- CLI tool for manual keyword research

**Next action:** Continue v1.3 milestone or start new phase (check PROJECT.md roadmap)

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

---

*State updated: 2026-02-01 after Plan 16-02 complete*
