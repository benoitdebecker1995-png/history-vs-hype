# State: History vs Hype Workspace

**Initialized:** 2025-01-19
**Last Updated:** 2026-02-20 (42-02 NLM ingestion tool completed)

## Project Reference

See: `.planning/PROJECT.md` (updated 2026-02-19)

**Core value:** Every video shows sources on screen
**Current focus:** v5.0 Production Intelligence

## Current Position

**Milestone:** v5.0 Production Intelligence
**Phase:** 42 of 46 (Pipeline Hardening & Research Ingestion)
**Status:** Ready to plan
**Last activity:** 2026-02-20 — NLM ingestion tool built (nlm_ingest.py), /research --ingest command documented

**Progress:**
[██████████] 99%

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

**Full history:** `.planning/MILESTONES.md`
**Archives:** `.planning/milestones/`

## What's Available

**Workspace commands:**
- `/status` — project state and next action
- `/help` — phase-organized command list
- `/research --new` — start new video project
- `/next` — get ranked topic recommendations based on winning patterns

**Analytics commands (v1.1+v1.6+v2.0):**
- `/analyze VIDEO_ID` — post-publish video analysis (+ variant tracking + CTR analysis + feedback insights + section diagnostics)
- `/analyze VIDEO_ID --script PATH` — section-level retention diagnostics with voice pattern recommendations
- `/patterns` — cross-video pattern recognition (+ feedback patterns)

**Discovery commands (v1.2 + v1.3):**
- `/discover TOPIC` — keyword research workflow
- `/discover --demand "keyword"` — demand analysis with opportunity scoring
- `/discover --opportunity "topic"` — complete opportunity analysis (demand + competition + production)
- `/discover --check FILE` — pre-publish metadata validation

**Full command list:** Run `/help`

## Accumulated Context

### Roadmap Evolution
- Phase 42.1 inserted after Phase 42: Translation Pipeline Claude Code Integration (URGENT) — refactor translation modules to use Claude Code's LLM layer instead of direct Anthropic API calls, enabling Pro plan users without API keys

## Decisions

Recent decisions affecting current work:
- for v5.0
- [Phase 42]: Pure Python .env parsing (no dotenv): minimizes dependencies, 15-line implementation
- [Phase 42]: wrap_api_error uses duck-typed exception matching to avoid circular imports in env_loader
- [Phase 42]: Smoke test uses real API calls (not mocks) to validate actual connectivity
- [Phase 42]: Hybrid NLM parsing: structured bullet detection first, freeform sentence-splitting fallback — handles both NLM output modes without user configuration
- [Phase 42]: Error dict API pattern (never raise) for nlm_ingest.py — keeps slash command integration simple with consistent error checking
- [Phase 42.1]: Keep TRANSLATION_SYSTEM_PROMPT in Python (domain knowledge stays with data layer, per RESEARCH.md Pitfall 1 option b)
- [Phase 42.1]: Smoke test rewritten as 4-step pure Python health check — module imports + payload builder + response parser, no API calls
- [Phase 43-youtube-intelligence-engine]: feedparser only new dependency; No BeautifulSoup needed — LLM synthesis handles messy text
- [Phase 43-youtube-intelligence-engine]: Graceful RSS-only fallback when YouTube API auth fails; competitor enrichment non-fatal
- [Phase 43-youtube-intelligence-engine]: Text-analysis mode is primary synthesis path for automated refresh; SYNTHESIS_PROMPT constant reserved for /intel command in Claude Code agent context
- [Phase 43-youtube-intelligence-engine]: 10-phase refresh orchestrator: errors collected and returned, pipeline continues on individual phase failure
- [Phase 43-youtube-intelligence-engine]: query.py returns formatted Markdown strings (not raw dicts) — display-ready output simplifies /intel command logic
- [Phase 43-youtube-intelligence-engine]: PRE-SCRIPT INTELLIGENCE in script-writer-v2 is light integration (read as context, do not display) — Phase 45 will deepen with Rule 19
- [Phase 44-analytics-backfill-feedback-loop]: avg_retention_pct added via migration in backfill.py (not database.py) — keeps Phase 44 self-contained without modifying core DB layer
- [Phase 44-analytics-backfill-feedback-loop]: Own-channel filtering uses both JSON pre-fetch files as authoritative ID set (40 IDs) — prevents competitor data contaminating channel insights
- [Phase 44-analytics-backfill-feedback-loop]: Composite score weights: views 0.4, retention 0.35, conversion 0.25 — normalized 0-1 against channel max per user decision
- [Phase 44-analytics-backfill-feedback-loop]: Channel insights section placed after Flags table in all three commands — consistent insertion point before first workflow section
- [Phase 44-analytics-backfill-feedback-loop]: analyze.py uses PROJECT_ROOT constant for generate_channel_insights_report() — avoids CWD ambiguity when invoked from different directories
- [Phase 45-hook-optimization-intelligence-integration]: YouTube Intelligence advisory placed after Channel Insights in prep/publish — keeps own-channel vs algorithm/niche data sources visually separate
- [Phase 45-hook-optimization-intelligence-integration]: Workflow-specific focus lines per command: /script=hooks/algorithm, /prep=format/B-roll, /publish=titles/CTR
- [Phase 45-hook-optimization-intelligence-integration]: Rule 19 supersedes Rule 9 Section A (Opening Hook Selection) for first 60 seconds — Rule 9 hook types become subsets of 4-beat formula
- [Phase 45-hook-optimization-intelligence-integration]: STEP 8 in REASONING FRAMEWORK updated to reference Rule 19 directly, replacing old Part 4 formula reference
- [Phase 46-project-dashboard]: time.time() - st_mtime for days-since calculation: avoids timezone-aware/naive mixing on Windows
- [Phase 46-project-dashboard]: DASHBOARD MODE placed before DETECTION LOGIC for logical flow: no-arg check first, then project detection
- [Phase 46-project-dashboard]: Step 0 routing in DETECTION LOGIC makes no-arg -> dashboard path explicit and unambiguous

## Session Continuity

### Last Session

- **Date:** 2026-02-20
- **Work:** Executed 42-02-PLAN.md — NLM ingestion tool (nlm_ingest.py), /research --ingest workflow
- **Output:** tools/research/nlm_ingest.py, tools/research/__init__.py, .claude/commands/research.md updated
- **Stopped at:** Completed 46-02-PLAN.md

### Next Session

**Next action:** `/gsd:plan-phase 43` — plan next v5.0 phase

## Technical Notes

- YouTube Analytics API requires Google Cloud project (configured)
- OAuth2 token auto-refreshes (saved in credentials/token.json)
- keywords.db schema version 29 (auto-migration with PRAGMA user_version)
- Feature flags: VARIANTS_AVAILABLE, BENCHMARKS_AVAILABLE, FEEDBACK_AVAILABLE, DIAGNOSTICS_AVAILABLE, TOPIC_STRATEGY_AVAILABLE, PLAYBOOK_AVAILABLE, SCORER_AVAILABLE
- anthropic SDK required for notebooklm_bridge.py (`pip install anthropic>=0.40.0`)
- spaCy requires Python 3.11-3.13 (not 3.14)

## Known Issues

- Python 3.14 + spaCy incompatibility (use 3.11-3.13)
- Voice patterns empty until user runs --rebuild-voice
- trendspyg, scrapetube not installed (graceful degradation)

---

*State updated: 2026-02-19 after v5.0 roadmap created*
