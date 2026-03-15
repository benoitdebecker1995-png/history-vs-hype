---
gsd_state_version: 1.0
milestone: v5.1
milestone_name: Codebase Hardening
status: completed
last_updated: "2026-03-15T23:27:15.351Z"
last_activity: "2026-03-14 — Phase 62 added: proactive topic discovery"
progress:
  total_phases: 61
  completed_phases: 55
  total_plans: 118
  completed_plans: 118
  percent: 100
---

---
gsd_state_version: 1.0
milestone: v5.1
milestone_name: Codebase Hardening
status: completed
last_updated: "2026-03-15T22:32:13.549Z"
last_activity: "2026-03-14 — Phase 62 added: proactive topic discovery"
progress:
  total_phases: 60
  completed_phases: 54
  total_plans: 117
  completed_plans: 117
  percent: 100
---

# State: History vs Hype Workspace

**Initialized:** 2025-01-19
**Last Updated:** 2026-03-14 (v6.0 Packaging Pipeline complete — retitle pipeline + data-driven scoring gate)

## Project Reference

See: `.planning/PROJECT.md` (updated 2026-02-24)

**Core value:** Every video shows sources on screen
**Current focus:** v6.0 Packaging Pipeline — Phase 62: Proactive Topic Discovery

## Current Position

**Milestone:** v6.0 Packaging Pipeline
**Phase:** 62 — Proactive Topic Discovery (not yet planned)
**Status:** Milestone complete
**Last activity:** 2026-03-14 — Phase 62 added: proactive topic discovery

**Progress:**
[██████████] 100%

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
| v4.0 | Untranslated Evidence Pipeline | 39-41 | 2026-02-18 |
| v5.0 | Production Intelligence | 42-47 | 2026-02-22 |
| v5.1 | Codebase Hardening | 48-54 | 2026-03-01 |
| v5.2 | Growth Engine | 55-59 | 2026-03-01 |
| v6.0 | Packaging Pipeline | 60-61 | 2026-03-14 |

**Full history:** `.planning/MILESTONES.md`
**Archives:** `.planning/milestones/`

## v6.0 Phase Order

| Phase | Name | Requirements | Depends On |
|-------|------|-------------|------------|
| 60 | Retitle & Rethumb Pipeline | RETITLE-01..06 | Phase 59 |
| 61 | Data-driven Packaging Gate | GATE-01..05 | Phase 60 |
| 62 | Proactive Topic Discovery | DISC-01..05 | Phase 61 |

## v5.1 Phase Order

| Phase | Name | Requirements | Depends On |
|-------|------|-------------|------------|
| 48 | Package Structure & Dependencies | PKG-01..03, DEP-01..03 | v5.0 done |
| 49 | Dead Code Cleanup | CLEAN-01..03 | Phase 48 |
| 50 | Error Handling | ERR-01..03 | Phase 49 |
| 51 | Logging & CLI Standardization | LOG-01..03, CLI-01..03 | Phase 50 |
| 52 | Database Hardening | DB-01..03 | Phase 48 |
| 53 | Integration Testing | TEST-01..07 | Phases 48-52 |
| 54 | External Intelligence Synthesis | EIS-01..05 | Phase 53 |

## Accumulated Context

### Decisions

v5.0 decisions archived in PROJECT.md Key Decisions table. See `.planning/milestones/v5.0-ROADMAP.md`.

v5.1 ordering rationale: Package structure first (proper imports unblock everything else), dead code before error handling (don't harden code that's being deleted), logging+CLI paired (both wire --verbose/--quiet), DB hardening parallel to error/logging work, testing last (verifies final state of all changes).
- [Phase 48-01]: git mv used for directory renames to preserve file history (R100 similarity)
- [Phase 48-01]: python -m tools.youtube_analytics.X is the new invocation pattern for all tools
- [Phase 48-03]: Used trendspyg (not trendspy) — confirmed from actual import in tools/discovery/trends.py
- [Phase 48-03]: pyproject.toml is the single source of dependency truth — three per-package requirements.txt files deleted
- [Phase 48]: Lazy import pattern used for discovery/diagnostics.py and discovery/recommender.py to break youtube_analytics circular dependency
- [Phase 48]: All cross-package imports now use absolute tools.* syntax; same-package imports use relative from .module syntax
- [Phase 49-dead-code-cleanup]: prompt_evaluation.py deleted: zero Python callers, channel_voice_check CLI arg was never real (just a dict key), stale file paths from v3.0, superseded by script-writer-v2 + script_checkers/ + STYLE-GUIDE Part 6
- [Phase 49-dead-code-cleanup]: backups/ gitignored not deleted: database.py still writes to it during v27 migration for fresh installs; production DB at v29 so directory auto-creates on demand
- [Phase 49-dead-code-cleanup]: get_youtube_metadata() deleted from patterns.py: zero callers codebase-wide, not in module docstring public API, superseded by find_project_folder_for_video()
- [Phase 49-dead-code-cleanup]: video_report.py bare imports (from metrics/retention/ctr) are pre-existing Phase 48-02 miss: deferred to Phase 50 per scope boundary rule
- [Phase 50-error-handling]: split_screen_guide method _parse_script (not _read_file) fixed for ERR-02; ERR-03 scoped to modified files only; analyze.py Plan 01 Task 2 still pending
- [Phase 50]: video_report.py bare imports fixed: from metrics/retention/ctr → tools.youtube_analytics.*; downstream metrics.py→auth.py bare import is pre-existing out-of-scope issue
- [Phase 28.1-multi-model-token-optimization]: Quality validation deferred to first production use — /model switching requires interactive Claude Code session, not automatable
- [Phase 28.1-multi-model-token-optimization]: CCR v1.0.32 installed + OpenRouter API key configured — routing infrastructure fully ready as of 2026-02-26
- [Phase 51-logging-cli]: Configure logging.getLogger("tools") not root logger — library-safe hierarchy; NullHandler in tools/__init__.py prevents No-handlers warnings
- [Phase 51-logging-cli]: setup_logging() called in __main__ blocks only, never at module import time — logging is a CLI concern, not a library concern
- [Phase 51-logging-cli]: editguide.py, metadata.py, intel/query.py excluded from argparse conversion — smoke-test __main__ blocks with no user arguments are not real CLI entry points
- [Phase 51-logging-cli-standardization]: Intentional CLI output (reports, tables, interactive prompts) preserved as print() - discriminator: user needs this output to use the tool
- [Phase 51-logging-cli-standardization]: intel/refresh.py _print_phase() helper removed - replaced with direct logger.info calls per phase step, cleaner and consistent with module pattern
- [Phase 51]: Decision rule for print() vs logger: if output is the RESULT the user ran command to see, keep as print(); if narration/progress, convert to logger
- [Phase 52-database-hardening]: DB-02 resolution: technique_library.py operates on keywords.db (not analytics.db) — PRAGMA user_version tracking is correct and atomic on the database it actually owns
- [Phase 52-database-hardening]: Migration pattern: version set AFTER with self._conn: block succeeds, never inside — if DDL fails, version stays at old value and migration re-runs on next startup
- [Phase 52-database-hardening]: autocommit=False required for Python 3.12+ sqlite3 DDL rollback in migration connections
- [Phase 52-database-hardening]: CURRENT_SCHEMA_VERSION = 2 module constant; _migrate_schema() is single entry point for intel.db schema management
- [Phase 53-integration-testing]: spaCy-dependent pacing tests use @requires_nlp skip — spaCy is optional [nlp] dep, skip keeps CI clean
- [Phase 53-integration-testing]: KBStore fixture uses real tmp_path file (not :memory:) — per-call _connect() pattern requires real file for cross-call persistence
- [Phase 53-integration-testing]: pyproject.toml testpaths=[tests] — pytest discovery now targets tests/ tree, not tools/
- [Phase 53-integration-testing]: OpportunityOrchestrator full-pipeline smoke tests also mock db.get_keyword + scorer — demand mock alone insufficient; DB lookup follows immediately after demand analysis
- [Phase 53-integration-testing]: feedparser patch at tools.intel.algo_scraper.feedparser.parse AND tools.intel.competitor_tracker.feedparser.parse — both modules import feedparser independently at top-level
- [Phase 53-integration-testing]: TranslationDataBuilder.parse_response third param is original_text not source_language — test must match actual interface
- [Phase 54]: VIDIQ_CHAR_LIMIT=2000 as configurable constant for VidIQ Pro Coach prompt context
- [Phase 54]: Regex-scoring classifier for 5 response types — transparent and testable, no new dependencies
- [Phase 54]: Source weighting matrix: VidIQ 0.9 for keyword variant, Gemini 0.9 for curiosity, entities 0.9 for authority
- [Phase 54]: Moderation informational not blocking — HIGH flags with safe alternatives never prevent publishing
- [Phase 61]: Title matching uses LIKE on first 40 chars — synthesis table uses descriptive titles, video_performance stores YouTube API titles
- [Phase 61]: is_late_entry=True and snapshot_date=2026-02-23 for all ingest rows — marks historical backfill clearly
- [Phase 61]: dry_run parameter added to ingest_synthesis_ctr() — safe preview before DB mutation
- [Phase 61-01]: Lazy import pattern in title_ctr_store.py breaks circular import with title_scorer.py
- [Phase 61-01]: score = min(100, max(0, int(ctr_percent * 17))) calibration maps 3.8% CTR to 64 (near static declarative baseline of 65)
- [Phase 61-01]: db_enriched=False when pattern not in DB results — accurate signal to callers without inspecting internals
- [Phase 61-03]: greenlight.md and scorer.py use KeywordDB().db_path by default — DB enrichment is always attempted, falls back silently to static scores
- [Phase 61-03]: format_result() Source line shows DB-enriched vs static scores — user gets clear feedback on data source without inspecting internals
- [Phase 60-01]: Retention weighting formula: priority = wasted_impressions × (1 + retention_bonus) — surfaces content-quality packaging failures over dual packaging+content failures
- [Phase 60-01]: SWAP-CHECKLIST.md is ephemeral (regenerated each run); SWAP LOG in POST-PUBLISH-ANALYSIS.md is permanent record with 7-day measurement window
- [Phase 60]: ctr_ingest.py is optional — existence check before invocation, graceful degradation to manual instructions if absent
- [Phase 60]: POST-PUBLISH-ANALYSIS search order: channel-data/analyses/ primary, video-projects/ secondary
- [Phase 62-proactive-topic-discovery]: 15 seeds for autocomplete runtime balance (<90s vs 3+ min for 20-30 seeds)
- [Phase 62-proactive-topic-discovery]: CHANNEL_AVG_VIEWS_FALLBACK=1000 (conservative median, not 4234 mean skewed by outliers)
- [Phase 62-proactive-topic-discovery]: Feature flags must be patched alongside callables in tests: patch TRENDSPYG_AVAILABLE=True AND TrendsClient
- [Phase 62-02]: --scan section placed after flags table, before FULL KEYWORD RESEARCH — natural reading order for command reference
- [Phase 63-v6-gap-closure]: search_video_performance_by_title() added to KeywordDB as public method — ctr_ingest delegates entirely, eliminating private _conn access
- [Phase 63-v6-gap-closure]: retitle.md Step 4c now matches greenlight.md and scorer.py pattern: KeywordDB().db_path passed to score_title()
- [Phase 64-02]: ZubeidHendricks YouTube MCP SKIP: broken npm package — MCP SDK restructured dist/cjs/index.js path, package incompatible with current SDK
- [Phase 64-02]: Windsor AI SKIP: cloud-only OAuth connector, no installable MCP package, data coverage identical to existing tools/youtube_analytics/
- [Phase 64-02]: No YouTube transcript MCP: both tested options broken (ZubeidHendricks npm + DannySubsense pip); yt-dlp.exe remains the stable extraction path
- [Phase 64-02]: Phase 64 final: 2 ADOPT (Context7 + Playwright), 9 SKIP, 0 DEFER — DECISION.md locked 2026-03-15
- [Phase 65]: store_snapshot() extended with optional kwargs (ctr_percent=0.0, impression_count=0) — backward-compatible, existing callers unchanged
- [Phase 65]: NonClosingConnection wrapper used in tests — sqlite3.Connection.close is read-only at C level, cannot be patched
- [Phase 65]: logs/*.log in .gitignore (was logs/) — allows logs/.gitkeep to be tracked while ignoring generated log files

### Roadmap Evolution

- Phase 54 added: External Intelligence Synthesis — automated VidIQ/Gemini prompt generation, response parsing, metadata synthesis, moderation scoring, thumbnail blueprints
- Phase 60 added: Retitle and rethumb underperforming videos with impressions but low CTR
- Phase 61 added: Data-driven packaging gate for new videos — title scorer reads real CTR from DB, greenlight enforces minimum score, feedback loop closes automatically
- Phase 64 added: Evaluate YouTube MCP servers and packaging plugins for adoption
- Phase 65 added: Automated CTR feedback loop — wire YouTube Analytics API into title scorer so CTR data updates automatically instead of manual snapshots

### Pending Todos

None.

### Blockers/Concerns

None at roadmap time.

## Session Continuity

### Last Session

- **Date:** 2026-02-28
- **Work:** Executed 54-01 — created prompt_generator.py (4 VidIQ + 1 Gemini prompt, auto-adapted to script length) and intake_parser.py (regex-scoring classifier for 5 response types, JSON persistence with parseable_ratio tracking)
- **Output:** 54-01-SUMMARY.md created, commits 6ad105b (Task 1) + b873216 (Task 2)

### Next Session

**Next action:** Phase 54 Plan 02 — Synthesis engine (reads EXTERNAL-INTELLIGENCE.json, produces ranked metadata packages)

## Technical Notes

- keywords.db schema version 29 (auto-migration with PRAGMA user_version)
- intel.db and analytics.db need same PRAGMA versioning (Phase 52)
- sys.path.insert hacks REMOVED — all tools use proper absolute tools.* or relative imports (completed in 48-02)
- spaCy requires Python 3.11-3.13 (not 3.14)
- Feature flags: VARIANTS_AVAILABLE, BENCHMARKS_AVAILABLE, FEEDBACK_AVAILABLE, DIAGNOSTICS_AVAILABLE, TOPIC_STRATEGY_AVAILABLE, PLAYBOOK_AVAILABLE, SCORER_AVAILABLE

---

*State updated: 2026-02-28 after 54-01 execution complete*
