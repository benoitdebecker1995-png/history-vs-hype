# State: History vs Hype Workspace

**Initialized:** 2025-01-19
**Last Updated:** 2026-01-26

## Project Reference

See: `.planning/PROJECT.md` (updated 2026-01-23)

**Core value:** Every video shows sources on screen — viewers see the evidence themselves
**Current focus:** v1.1 Analytics & Learning Loop — COMPLETE

## Current Position

**Milestone:** v1.1 Analytics & Learning Loop
**Phase:** 10 - Pattern Recognition (Complete)
**Plan:** 03 of 3 complete
**Status:** Phase 10 complete, v1.1 milestone shipped

**Progress:**
```
[████████████████████] 100% — v1.1 complete (15/15 requirements)
```

## Milestone History

| Version | Name | Phases | Shipped |
|---------|------|--------|---------|
| v1.0 | Workspace Optimization | 0.1, 1-6 | 2026-01-23 |
| v1.1 | Analytics & Learning Loop | 7-10 | 2026-01-26 |

**Full history:** `.planning/MILESTONES.md`

## v1.1 Phase Overview

| Phase | Name | Requirements | Status |
|-------|------|--------------|--------|
| 7 | API Foundation | 3 | Complete |
| 8 | Data Pull Scripts | 3 | Complete |
| 9 | Post-Publish Analysis | 6 | Complete |
| 10 | Pattern Recognition | 3 | Complete |

**Total requirements:** 15
**Completed:** 15/15 (All phases complete)

## Session Continuity

### Last Session

- **Date:** 2026-01-26
- **Work:** Completed Phase 10 Plan 03 - Monthly summaries and /patterns slash command
- **Output:**
  - tools/youtube-analytics/patterns.py — Enhanced with monthly summary, time windows (~1900 lines)
  - .claude/commands/patterns.md — /patterns slash command documentation
  - channel-data/patterns/MONTHLY-2026-01.md — January 2026 monthly summary

### Next Session

1. **v1.1 shipped** - Analytics & Learning Loop complete
2. **Available commands:**
   - `/analyze VIDEO_ID` - Single video post-publish analysis
   - `/patterns` - Cross-video pattern analysis (all reports)
   - `/patterns --topic` - Topic performance only
   - `/patterns --title` - Title/thumbnail patterns only
   - `/patterns --monthly` - Current month summary

### Important Context

- **Phase 10 complete:** All PATRN requirements satisfied
  - PATRN-01: Topic tagging and aggregation (Plan 01)
  - PATRN-02: Monthly summary generation (Plan 03)
  - PATRN-03: Title/thumbnail patterns correlated with CTR (Plan 02)
- **Key deliverables:**
  - `get_videos_for_period()` filters videos by days or month
  - `generate_monthly_summary()` creates comprehensive monthly reports
  - `generate_all_reports()` creates topic, title, and monthly reports at once
  - `/patterns` slash command triggers pattern analysis on demand
- **File locations:**
  - Module: `tools/youtube-analytics/patterns.py`
  - Command: `.claude/commands/patterns.md`
  - Reports: `channel-data/patterns/` (TOPIC-ANALYSIS.md, TITLE-PATTERNS.md, MONTHLY-*.md)

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
| Minimum 2 videos for attribute comparisons | Avoid misleading single-video comparisons |
| 9 title patterns from COMPETITOR-TITLE-DATABASE | Detect proven title formulas for correlation |
| Thumbnail type as map/face/document/mixed/unknown | Categorize thumbnails for CTR correlation |
| Monthly default to current month | Most common use case when no args provided |
| /patterns --all as default | Comprehensive report generation is primary use case |
| Lower min_count for monthly (1 vs 3) | Fewer videos per month requires lower threshold |

### Technical Notes

- YouTube Analytics API requires Google Cloud project
- OAuth2 for channel authorization (user must authorize once)
- Comments available via YouTube Data API v3 commentThreads.list()
- Retention data comes from YouTube Analytics API reports
- **CTR confirmed:** Not available via API, returns graceful fallback with note to check YouTube Studio
- **Data scripts ready:** metrics.py, retention.py, ctr.py, video_report.py
- **Comment scripts ready:** comments.py with categorization, channel_averages.py with benchmarks
- **Analysis engine ready:** analyze.py with lesson generation, markdown output, and file saving
- **Slash commands ready:** /analyze and /patterns trigger full workflows
- **Pattern analysis ready:** patterns.py with topic tagging, title/thumbnail analysis, monthly summaries
- **Title patterns:** 9 patterns detected (e.g., "[Topic]: [Subtitle]", "Why [X] Is/Are [Verb]")
- **Thumbnail extraction:** Parses YOUTUBE-METADATA.md for type and attributes
- **Time windows:** get_videos_for_period() supports days (rolling) or month/year (specific)
- **Reports:** TOPIC-ANALYSIS.md, TITLE-PATTERNS.md, MONTHLY-{YYYY}-{MM}.md

---

*State updated: 2026-01-26 after Phase 10 completion (v1.1 shipped)*
