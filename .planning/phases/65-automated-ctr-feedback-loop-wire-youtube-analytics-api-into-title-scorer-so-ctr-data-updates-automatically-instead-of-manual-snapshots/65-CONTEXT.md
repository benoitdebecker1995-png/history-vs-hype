# Phase 65: Automated CTR Feedback Loop - Context

**Gathered:** 2026-03-15
**Status:** Ready for planning

<domain>
## Phase Boundary

Wire YouTube Analytics API into title scorer so CTR data updates automatically instead of manual snapshots. Replace the manual CROSS-VIDEO-SYNTHESIS.md → ctr_ingest.py pipeline with an automated API-based flow that runs on a schedule without user intervention. Title scorer pattern scores update from real CTR data without any manual steps.

</domain>

<decisions>
## Implementation Decisions

### Data Source Strategy
- API-first approach: try YouTube Analytics API for all videos, fall back to manual entry for failures
- `get_ctr_metrics()` in ctr.py already queries `videoThumbnailImpressions` + `videoThumbnailImpressionsClickRate` — reuse this
- Latest data wins: most recent snapshot (manual or API) is used, no source precedence logic
- Google Issue #254665034 means some videos won't return CTR — those are logged for manual entry

### Update Trigger & Frequency
- Extend existing `ctr_tracker.py` rather than creating a separate tool
- Fetch CTR for ALL ~47 long-form videos every run (one API batch fits in quota)
- Also update view counts in video_performance table since API is already being hit
- YouTube Analytics API requires per-video queries (no bulk CTR endpoint) — Claude decides batching/rate approach

### Migration from Manual Flow
- Keep `ctr_ingest.py` + CROSS-VIDEO-SYNTHESIS.md as fallback for videos where API returns no CTR
- Don't deprecate manual pipeline — it's the safety net for API gaps
- Write to same `ctr_snapshots` table — title_ctr_store.py already picks MAX(snapshot_date), so latest API data naturally wins

### Automation & Scheduling
- Fully hands-off: scheduled task runs without user intervention
- One-time manual OAuth flow required (browser redirect) to create token.json, then auto-refresh forever
- Refresh token stays alive as long as scheduled task keeps running (Google revokes after 6 months of no use)
- End-of-run summary printed: "CTR updated for X/47 videos. Title scorer now using DB-enriched scores: declarative=N, versus=N..."

### Claude's Discretion
- Scheduler platform choice (Windows Task Scheduler vs Python scheduler vs other)
- Refresh frequency (daily vs weekly — balance API quota vs data freshness)
- DB schema: whether to add `source` column to ctr_snapshots or use existing is_late_entry flag
- Zero CTR handling: threshold for filtering out insufficient-data videos
- Failed-fetch reporting: print summary vs write file vs log-only
- Error resilience: retry strategy, partial success handling
- Logging approach for unattended runs (log file vs stdout capture)
- API batching/rate limiting strategy for ~47 per-video Analytics API calls
- OAuth token expiry handling

</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- `tools/youtube_analytics/ctr.py`: `get_ctr_metrics(video_id)` — already queries Analytics API v2 for CTR with graceful fallback. Returns `ctr_available: bool` + `ctr_percent` + `impressions`
- `tools/youtube_analytics/ctr_tracker.py`: Daily view-count snapshot tool — extend this with CTR fetch. Already has `take_snapshot()`, `compare_snapshots()`, `store_snapshot()`, DB connection, CLI with --verbose/--quiet
- `tools/title_ctr_store.py`: `get_pattern_ctr_from_db()` — reads ctr_snapshots, computes pattern scores. No changes needed (reads latest snapshot automatically)
- `tools/ctr_ingest.py`: Manual pipeline reading CROSS-VIDEO-SYNTHESIS.md → ctr_snapshots. Stays as fallback
- `tools/youtube_analytics/auth.py`: `get_authenticated_service()` — handles OAuth2 token refresh
- `tools/youtube_analytics/growth_data.py`: `fetch_all_video_ids()`, `fetch_video_metadata()` — catalog fetch already in ctr_tracker

### Established Patterns
- `ctr_snapshots` table schema: `(video_id, snapshot_date, ctr_percent, impression_count, view_count, is_late_entry, recorded_at)`
- Feature flag pattern: graceful degradation when data unavailable
- `tools.logging_config`: `get_logger(__name__)` + `setup_logging(verbose, quiet)` for all CLI tools
- Error dict pattern: return `{'error': msg}` not raise exceptions

### Integration Points
- `ctr_tracker.py` → `ctr.py` (new: add CTR fetch to existing view-count snapshot)
- `ctr_snapshots` table → `title_ctr_store.py` → `title_scorer.py` (existing: no changes needed)
- `title_scorer.py` → `greenlight.md` / `preflight/scorer.py` / `retitle.md` (existing: automatically benefits)
- `video_performance` table update with fresh view counts (new addition to ctr_tracker scope)
- Windows Task Scheduler or equivalent for scheduled execution (new)

</code_context>

<specifics>
## Specific Ideas

- User wants truly hands-off automation — "fully hands-off (cron/scheduled)" was the explicit choice
- OAuth requires one-time manual browser flow, then scheduled runs auto-refresh the token
- The channel has ~47 long-form videos — small enough to fetch all every run
- End-of-run summary should confirm title_scorer is using fresh data with actual pattern scores shown

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 65-automated-ctr-feedback-loop*
*Context gathered: 2026-03-15*
