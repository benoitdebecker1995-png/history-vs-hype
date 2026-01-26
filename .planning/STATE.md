# State: History vs Hype Workspace

**Initialized:** 2025-01-19
**Last Updated:** 2026-01-26

## Project Reference

See: `.planning/PROJECT.md` (updated 2026-01-23)

**Core value:** Every video shows sources on screen — viewers see the evidence themselves
**Current focus:** v1.1 Analytics & Learning Loop — build feedback system for learning what works

## Current Position

**Milestone:** v1.1 Analytics & Learning Loop
**Phase:** 10 - Pattern Recognition (In Progress)
**Plan:** 01 of 3 complete
**Status:** Plan 10-01 complete, ready for Plan 10-02

**Progress:**
```
[████████████████░░░░] 80% — Plan 10-01 complete (12/15 requirements)
```

## Milestone History

| Version | Name | Phases | Shipped |
|---------|------|--------|---------|
| v1.0 | Workspace Optimization | 0.1, 1-6 | 2026-01-23 |
| v1.1 | Analytics & Learning Loop | 7-10 | In Progress |

**Full history:** `.planning/MILESTONES.md`

## v1.1 Phase Overview

| Phase | Name | Requirements | Status |
|-------|------|--------------|--------|
| 7 | API Foundation | 3 | Complete |
| 8 | Data Pull Scripts | 3 | Complete |
| 9 | Post-Publish Analysis | 6 | Complete |
| 10 | Pattern Recognition | 3 | Plan 01 complete |

**Total requirements:** 15
**Completed:** 12/15 (Phase 7 + Phase 8 + Phase 9 + Plan 10-01)

## Session Continuity

### Last Session

- **Date:** 2026-01-26
- **Work:** Completed Phase 10 Plan 01 - Topic performance tracking
- **Output:**
  - tools/youtube-analytics/patterns.py — Core pattern analysis module (809 lines)
  - channel-data/patterns/TOPIC-ANALYSIS.md — Initial topic performance report

### Next Session

1. **Continue Phase 10:** Pattern Recognition (2 plans remaining)
   - Plan 10-02: Title/thumbnail pattern analysis
   - Plan 10-03: Audience insight aggregation

### Important Context

- **Plan 10-01 complete:** PATRN-01 (cross-video comparison by topic type) satisfied
- **Key deliverables:**
  - `patterns.py` with collect_video_data, auto_tag_video, aggregate_by_topic
  - `--topic-report` generates TOPIC-ANALYSIS.md with insights-first format
  - Fixed TAG_VOCABULARY with 6 categories for consistent tagging
  - Minimum 3 videos per topic enforced for statistical validity
- **File locations:**
  - Module: `tools/youtube-analytics/patterns.py`
  - Reports: `channel-data/patterns/TOPIC-ANALYSIS.md`

## Accumulated Context

### Decisions Made

| Decision | Rationale |
|----------|-----------|
| 4 phases for v1.1 | Clear dependency chain: API -> Data -> Analysis -> Patterns |
| Phase numbering starts at 7 | Continues from v1.0 (phases 0.1-6) |
| Analysis command as single entry point | User experience: one command triggers full analysis |
| Desktop app OAuth type | Simpler flow for CLI tools - no redirect URI needed |
| Belt-and-suspenders gitignore | Both local and root gitignore for credentials security |
| External OAuth consent | Allows any Google account as test user during development |
| Port 8080 for OAuth | Standard port that works reliably for local OAuth server |
| Error dict pattern | Return {error: msg} instead of exceptions for API scripts |
| Default date range 2020-01-01 | Captures full video lifetime without user input |
| Position hints for retention | 6 segments map % to human-readable labels |
| Configurable drop-off threshold | Default 5%, adjustable for sensitivity |
| CTR fallback strategy | Return structured response when API unavailable |
| Combined reporter pattern | video_report.py orchestrates all data fetchers |
| Drop-offs sorted by magnitude | Biggest drops first for actionability |
| Relevance ordering for comments | Top comments by likes/replies first |
| Minimum 3 videos for averages | Fewer would produce misleading benchmarks |
| 5% threshold for at_average | Avoid over-sensitivity to minor variations |
| ASCII curve via retention.py | Full data points needed; video_report only has summary |
| Fallback location for analyses | channel-data/analyses/ when no project folder match |
| Project folder search order | _IN_PRODUCTION first, then _READY_TO_FILM, then _ARCHIVED |
| TAG_VOCABULARY with 6 categories | Covers channel content: territorial, ideological, colonial, politician, archaeological, medieval |
| Insights-first report format | Per 10-CONTEXT.md - actionable insights before data tables |

### Technical Notes

- YouTube Analytics API requires Google Cloud project
- OAuth2 for channel authorization (user must authorize once)
- Comments available via YouTube Data API v3 commentThreads.list()
- Retention data comes from YouTube Analytics API reports
- **CTR confirmed:** Not available via API, returns graceful fallback with note to check YouTube Studio
- **Data scripts ready:** metrics.py, retention.py, ctr.py, video_report.py
- **Comment scripts ready:** comments.py with categorization, channel_averages.py with benchmarks
- **Analysis engine ready:** analyze.py with lesson generation, markdown output, and file saving
- **Slash command ready:** /analyze triggers full workflow
- **Pattern analysis ready:** patterns.py with topic tagging, aggregation, and report generation

---

*State updated: 2026-01-26 after Plan 10-01 completion*
