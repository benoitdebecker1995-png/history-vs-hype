---
phase: 43-youtube-intelligence-engine
plan: 01
subsystem: database
tags: [sqlite, feedparser, youtube-rss, youtube-data-api, competitor-tracking, algorithm-scraper]

# Dependency graph
requires:
  - phase: 42.1-translation-pipeline-claude-code-integration
    provides: notebooklm_bridge.py pattern for LLM synthesis (used in downstream algo_synthesizer.py)
  - phase: 33-voice-pattern-library
    provides: tools/youtube-analytics/auth.py for YouTube Data API OAuth2

provides:
  - SQLite knowledge base (tools/intel/intel.db) with 5 tables and 3 indexes
  - KBStore class: full CRUD for algo_snapshots, competitor_channels, competitor_videos, niche_snapshots, kb_meta
  - algo_scraper: 5 authoritative algorithm sources (vidIQ, OutlierKit, Creator Insider RSS, Buffer, marketingagent)
  - competitor_tracker: YouTube RSS feed fetcher + Data API enrichment for 10 channels
  - competitor_channels.json: 10-channel registry (style-match + broad-history + geopolitics tiers)
  - parse_iso_duration: ISO 8601 PT1H2M3S to seconds converter
  - feedparser installed as new dependency

affects:
  - 43-02-PLAN (algo synthesizer and KB exporter will read intel.db via KBStore)
  - 43-03-PLAN (refresh orchestrator, /intel command)
  - 43-04-PLAN (script-writer-v2 KB integration)

# Tech tracking
tech-stack:
  added:
    - feedparser 6.0.12 (pip install feedparser) — YouTube RSS and Atom feed parsing
  patterns:
    - "Error-dict pattern: all KBStore/tracker methods return {'error': msg} on failure, never raise"
    - "Schema auto-init on first connection — same pattern as keywords.db"
    - "JSON columns: json.dumps/json.loads for all structured fields (signal_weights, algorithm_model, etc.)"
    - "Auth reuse via sys.path.insert for tools/youtube-analytics/auth.py — matching analyze.py pattern"
    - "feedparser graceful fallback: FEEDPARSER_AVAILABLE flag, meaningful error if not installed"
    - "Purge-and-replace: purge_competitor_videos() before each refresh (rolling window)"
    - "RSS-only fallback: API enrichment errors are non-fatal, caller proceeds with partial data"

key-files:
  created:
    - tools/intel/__init__.py
    - tools/intel/kb_store.py
    - tools/intel/algo_scraper.py
    - tools/intel/competitor_tracker.py
    - tools/intel/competitor_channels.json
  modified: []

key-decisions:
  - "feedparser only new dependency — requests, sqlite3, google-api-python-client all already installed"
  - "No BeautifulSoup: simple regex HTML stripping sufficient; LLM synthesis handles messy text"
  - "Graceful RSS-only fallback when YouTube API auth fails — enrichment non-fatal"
  - "10 channels in JSON config covering 3 tiers: style-match (5), broad-history (3), geopolitics (1), broad-history/format (1)"
  - "Channel IDs from RESEARCH.md noted as approximate — _comment field warns to verify via YouTube channel pages"
  - "max_age_days >= (not >) for is_stale boundary — edge: 7-day-old KB is stale, not 7+1"

patterns-established:
  - "Pattern: Hybrid SQLite + generated Markdown — SQLite for CRUD, Markdown for agent reads (see kb_exporter.py in Phase 43-02)"
  - "Pattern: YouTube RSS as primary competitor data source (free, no quota, officially supported)"
  - "Pattern: YouTube Data API videos.list for enrichment (1 quota unit/call, 50 IDs max) — NEVER search.list (100 units)"

requirements-completed: [INTEL-01, INTEL-03, INTEL-04]

# Metrics
duration: 4min
completed: 2026-02-21
---

# Phase 43 Plan 01: YouTube Intelligence Engine Summary

**SQLite knowledge base (intel.db) with 5 tables, algorithm blog scraper for 5 authoritative sources, and competitor tracker fetching 10 channels via YouTube RSS feeds with Data API enrichment**

## Performance

- **Duration:** 4 min
- **Started:** 2026-02-21T04:19:35Z
- **Completed:** 2026-02-21T04:23:19Z
- **Tasks:** 2
- **Files modified:** 5

## Accomplishments

- KBStore class with full CRUD for all 5 tables: algo_snapshots, competitor_channels, competitor_videos, niche_snapshots, kb_meta with 3 performance indexes
- algo_scraper with 5 authoritative sources (vidIQ HIGH, OutlierKit HIGH, Creator Insider HIGHEST/RSS, Buffer MEDIUM, marketingagent MEDIUM) and HTML-to-text pipeline
- competitor_tracker fetching 10 channels via YouTube RSS (feedparser) with YouTube Data API enrichment for views, likes, duration; graceful fallback to RSS-only if auth fails

## Task Commits

Each task was committed atomically:

1. **Task 1: SQLite storage layer and algorithm scraper** - `20d8daf` (feat)
2. **Task 2: Competitor tracker with RSS feeds and API enrichment** - `fa66856` (feat)

**Plan metadata:** (docs commit follows)

## Files Created/Modified

- `tools/intel/__init__.py` - Package docstring for YouTube Intelligence Engine
- `tools/intel/kb_store.py` - KBStore class: SQLite schema auto-init + full CRUD for 5 tables (280 lines)
- `tools/intel/algo_scraper.py` - ALGO_SOURCES list (5 sources), scrape_source(), scrape_all_sources(), _html_to_text() (130 lines)
- `tools/intel/competitor_tracker.py` - load_channel_config, fetch_channel_rss, enrich_videos_with_metadata, fetch_all_competitors, parse_iso_duration (230 lines)
- `tools/intel/competitor_channels.json` - 10-channel registry with tier annotations and verification notes

## Decisions Made

- feedparser 6.0.12 is the only new dependency (pip install feedparser); all others already installed
- No BeautifulSoup: simple `re.sub(r'<[^>]+>', ' ', html)` extraction is sufficient because algo_synthesizer.py (Phase 43-02) will handle messy text via LLM
- Graceful RSS-only fallback: YouTube API auth failures are non-fatal — competitor_tracker logs error and proceeds with RSS data (views/duration will be None)
- 10 channels in competitor_channels.json covering 3 tiers per RESEARCH.md recommendations; channel IDs noted as "approximate, verify before production" in _comment field
- is_stale uses >= (not >) for the max_age_days boundary: a 7-day-old KB is stale

## Deviations from Plan

None — plan executed exactly as written. feedparser was not pre-installed (as expected per RESEARCH.md Standard Stack notes), installed as Rule 3 dependency before Task 1 (blocking issue resolution).

## Issues Encountered

- feedparser was not installed (expected per RESEARCH.md). Installed via `pip install feedparser` before Task 1 execution.

## User Setup Required

None — no external service configuration required for this plan. YouTube Data API enrichment uses the existing auth.py/token.json OAuth2 setup from tools/youtube-analytics/. feedparser installed automatically.

## Next Phase Readiness

- intel.db created with correct 5-table schema and 3 indexes
- KBStore CRUD verified: save/get algo_snapshots, competitor_channels, competitor_videos, niche_snapshots; set/get last_refresh; is_stale()
- algo_scraper ready: 5 sources configured, scrape_source/scrape_all_sources can be called by algo_synthesizer.py (Phase 43-02)
- competitor_tracker ready: fetch_all_competitors() returns merged RSS + API data, ready for pattern_analyzer.py (Phase 43-02)
- All data flows into KBStore via save methods — 43-02 can build the synthesis and export layer on top of this foundation

## Self-Check: PASSED

- FOUND: tools/intel/__init__.py
- FOUND: tools/intel/kb_store.py
- FOUND: tools/intel/algo_scraper.py
- FOUND: tools/intel/competitor_tracker.py
- FOUND: tools/intel/competitor_channels.json
- FOUND: tools/intel/intel.db (auto-created by KBStore)
- FOUND: commit 20d8daf (Task 1 — SQLite storage layer and algorithm scraper)
- FOUND: commit fa66856 (Task 2 — competitor tracker with RSS feeds and API enrichment)

---
*Phase: 43-youtube-intelligence-engine*
*Completed: 2026-02-21*
