# State: History vs Hype Workspace

**Initialized:** 2025-01-19
**Last Updated:** 2026-01-25

## Project Reference

See: `.planning/PROJECT.md` (updated 2026-01-23)

**Core value:** Every video shows sources on screen — viewers see the evidence themselves
**Current focus:** v1.1 Analytics & Learning Loop — build feedback system for learning what works

## Current Position

**Milestone:** v1.1 Analytics & Learning Loop
**Phase:** 9 - Post-Publish Analysis (Plan 01 complete)
**Status:** In progress - Plan 02-03 remaining

**Progress:**
```
[████████░░          ] 47% — Plan 09-01 complete (7/15 requirements)
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
| 7 | API Foundation | 3 | ✓ Complete |
| 8 | Data Pull Scripts | 3 | ✓ Complete |
| 9 | Post-Publish Analysis | 6 | In Progress (Plan 01 done) |
| 10 | Pattern Recognition | 3 | Blocked (needs Phase 9) |

**Total requirements:** 15
**Completed:** 7/15 (Phase 7 + Phase 8 + Plan 09-01)

## Session Continuity

### Last Session

- **Date:** 2026-01-25
- **Work:** Completed Phase 9 Plan 01 - Comment fetching and channel averages infrastructure
- **Output:**
  - tools/youtube-analytics/comments.py — Comment fetcher and categorizer
  - tools/youtube-analytics/channel_averages.py — Channel benchmark calculator

### Next Session

1. **Execute Plan 09-02:** Create analyze.py orchestrator
2. **Execute Plan 09-03:** Create /analyze slash command

### Important Context

- **Phase 9 Plan 01 delivered:** comments.py and channel_averages.py ready for analyze.py integration
- **Comment categorization:** questions, objections, requests, other categories
- **Benchmark comparison:** compare_to_channel() provides above/below/at_average with delta percentages
- **Minimum 3 videos required** for meaningful channel averages
- **All scripts importable:** `from comments import fetch_and_categorize_comments`

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

### Technical Notes

- YouTube Analytics API requires Google Cloud project ✓
- OAuth2 for channel authorization (user must authorize once) ✓
- Comments available via YouTube Data API v3 commentThreads.list() ✓
- Retention data comes from YouTube Analytics API reports
- **CTR confirmed:** Not available via API, returns graceful fallback with note to check YouTube Studio
- **Data scripts ready:** metrics.py, retention.py, ctr.py, video_report.py
- **Comment scripts ready:** comments.py with categorization, channel_averages.py with benchmarks

---

*State updated: 2026-01-25 after Plan 09-01 completion*
