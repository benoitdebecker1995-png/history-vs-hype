---
phase: 43-youtube-intelligence-engine
plan: 02
subsystem: database
tags: [sqlite, youtube-algorithm, competitor-intelligence, pattern-analysis, markdown-export, text-analysis]

# Dependency graph
requires:
  - phase: 43-youtube-intelligence-engine
    plan: 01
    provides: KBStore CRUD, algo_scraper (5 sources), competitor_tracker (RSS+API), intel.db schema

provides:
  - algo_synthesizer.py: text-analysis synthesis of scraped algorithm content into structured JSON model + SYNTHESIS_PROMPT constant for LLM mode
  - pattern_analyzer.py: outlier detection at >= 3x channel median views, niche format/hook/topic extraction, heuristic outlier analysis
  - kb_exporter.py: generates channel-data/youtube-intelligence.md from intel.db (4 sections, target < 3000 words)
  - refresh.py: 10-phase orchestrator tying all modules together with purge-and-replace, error collection, staleness check
  - channel-data/youtube-intelligence.md: agent-readable KB snapshot (auto-generated)

affects:
  - 43-03-PLAN (query.py + /intel command will invoke run_refresh and read youtube-intelligence.md)
  - 43-04-PLAN (script-writer-v2 KB integration reads youtube-intelligence.md)
  - script-writer-v2 agent (light KB integration: reads Algorithm Mechanics + Niche Patterns sections)

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Text-analysis synthesizer: keyword scoring + sentence extraction as fallback for LLM synthesis — SYNTHESIS_PROMPT constant available for agent-context LLM mode"
    - "Noise filtering: _is_noise_sentence() filters JSON-LD/CSS blobs from scraped pages before sentence extraction"
    - "Purge-and-replace: purge_competitor_videos() called in Phase 5 before saving new videos (rolling window)"
    - "10-phase pipeline pattern: each phase wrapped in try/except, errors collected in list, pipeline continues"
    - "Outlier detection: per-channel median (requires >= 3 videos), flags at views >= median * 3.0x"
    - "Duration distribution: 5 buckets (0-10min, 10-20min, 20-30min, 30-45min, 45+min) + unknown"
    - "Markdown export target: < 3000 words using tables + bullets (not prose)"

key-files:
  created:
    - tools/intel/algo_synthesizer.py
    - tools/intel/pattern_analyzer.py
    - tools/intel/kb_exporter.py
    - tools/intel/refresh.py
    - channel-data/youtube-intelligence.md
  modified: []

key-decisions:
  - "Text-analysis mode is the primary synthesis path for automated refresh; LLM mode (SYNTHESIS_PROMPT) is reserved for the /intel command when running in Claude Code agent context"
  - "Noise filter added to sentence extractor: skips sentences starting with JSON-LD/CSS markers or > 400 chars (auto-fix during implementation)"
  - "ensure_channels_loaded() bootstraps competitor_channels table from JSON on first run — idempotent upsert prevents duplicates"
  - "Pipeline errors are collected and returned, not raised — all 10 phases attempt to run regardless of individual failures"

patterns-established:
  - "Pattern: 10-phase orchestrator with per-phase error collection — each phase in try/except, errors list appended, pipeline continues"
  - "Pattern: Staleness check gate — run_refresh() checks is_stale() unless force=True; skip returns structured dict"
  - "Pattern: Markdown KB export < 3000 words targeting agent context efficiency (tables/bullets, 5 capped per section)"

requirements-completed: [INTEL-01, INTEL-02, INTEL-03, INTEL-04]

# Metrics
duration: 7min
completed: 2026-02-21
---

# Phase 43 Plan 02: YouTube Intelligence Engine Summary

**LLM synthesis pipeline and Markdown KB export: text-analysis synthesizer with SYNTHESIS_PROMPT, 3x-median outlier detector, niche pattern extractor, and 10-phase refresh orchestrator producing youtube-intelligence.md under 3000 words**

## Performance

- **Duration:** 7 min
- **Started:** 2026-02-21T04:25:46Z
- **Completed:** 2026-02-21T04:32:21Z
- **Tasks:** 2
- **Files modified:** 5

## Accomplishments

- algo_synthesizer.py: text-analysis fallback synthesizes scraped content into structured algorithm JSON model (signal weights, pipeline mechanics, longform insights, satisfaction signals, thresholds); SYNTHESIS_PROMPT constant for agent-context LLM synthesis
- pattern_analyzer.py: detect_outliers() groups by channel_id, requires >= 3 videos for meaningful median, flags at 3x; extract_niche_patterns() produces duration distribution (5 buckets), title formula counts (5 formulas), trending topics (10 history/edu keyword clusters); generate_outlier_analysis() adds heuristic possible_reasons
- kb_exporter.py + refresh.py: full end-to-end pipeline verified running on real data (3/5 algo sources scraped, 2 channels fetched, 30 videos saved, patterns extracted, youtube-intelligence.md exported at 478 words)

## Task Commits

Each task was committed atomically:

1. **Task 1: Algorithm synthesizer and pattern analyzer** - `0cdb5a7` (feat)
2. **Task 2: KB exporter and refresh orchestrator** - `6316eae` (feat)

**Plan metadata:** (docs commit follows)

## Files Created/Modified

- `tools/intel/algo_synthesizer.py` - Text-analysis synthesis mode + SYNTHESIS_PROMPT LLM constant; _is_noise_sentence() filter added during implementation (339 lines)
- `tools/intel/pattern_analyzer.py` - detect_outliers(), extract_niche_patterns(), generate_outlier_analysis() with history/edu niche keyword clusters (372 lines)
- `tools/intel/kb_exporter.py` - export_kb_to_markdown() with 5 section renderers; targets < 3000 words (369 lines)
- `tools/intel/refresh.py` - run_refresh() 10-phase pipeline, ensure_channels_loaded(), get_refresh_summary(), staleness check (412 lines)
- `channel-data/youtube-intelligence.md` - Auto-generated KB snapshot (populated from real run, 478 words)

## Decisions Made

- Text-analysis mode is primary for automated Python refresh; SYNTHESIS_PROMPT is available for the /intel command to pass scraped text to Claude Code's LLM (same pattern as notebooklm_bridge.py from Phase 42.1)
- ensure_channels_loaded() bootstraps competitor_channels table from competitor_channels.json on every refresh — idempotent upsert means safe to call repeatedly
- Pipeline errors are collected and returned as a list, not raised — all 10 phases attempt to run regardless of individual failures (11 non-fatal errors on first run: 2 JS-rendered scrape pages, API auth issues for 8 channels)

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Added noise-sentence filter to text extractor**
- **Found during:** Task 2 (kb_exporter export verification)
- **Issue:** `_extract_sentences_with_keywords()` was returning JSON-LD schema blobs and CSS strings as "sentences" because blog pages contain structured data sections that survived HTML-to-text stripping
- **Fix:** Added `_is_noise_sentence()` helper that skips sentences starting with `{`, `[`, `*`, `.`, `#`, sentences > 400 chars, or sentences with > 3 braces; all extracted sentences truncated to 250 chars
- **Files modified:** tools/intel/algo_synthesizer.py
- **Verification:** youtube-intelligence.md regenerated at 478 words (was 1176 with raw JSON-LD fragments); all section content readable
- **Committed in:** 6316eae (Task 2 commit)

---

**Total deviations:** 1 auto-fixed (Rule 1 — bug)
**Impact on plan:** Fix was necessary for correct output. The text-analysis mode was producing unreadable Markdown with JSON-LD blobs. No scope creep.

## Issues Encountered

- 2 of 5 algorithm sources (OutlierKit, marketingagent) return JS-rendered pages that static requests can't parse fully — content is partial. This matches RESEARCH.md Open Question 4 ("If JS-rendered, add playwright as optional fallback"). Non-fatal: 3 sources still scraped successfully with meaningful content.
- 8 of 10 competitor channels couldn't be enriched with YouTube Data API (token refresh needed, only 2 channels had valid cached sessions). RSS feeds still returned titles and publish dates; duration data is None for those channels.

## User Setup Required

None — no external service configuration required for this plan.

## Next Phase Readiness

- run_refresh() end-to-end pipeline is operational: algo sources scraped, competitors fetched, outliers detected, Markdown exported
- youtube-intelligence.md exists at channel-data/youtube-intelligence.md ready for agent reads
- All 9 verification items from plan spec pass
- 43-03-PLAN (query.py + /intel command) can build on run_refresh() directly
- 43-04-PLAN (script-writer-v2 KB integration) can read channel-data/youtube-intelligence.md immediately
- Full API enrichment will work once YouTube OAuth token is refreshed for all 10 channels

## Self-Check: PASSED

- FOUND: tools/intel/algo_synthesizer.py
- FOUND: tools/intel/pattern_analyzer.py
- FOUND: tools/intel/kb_exporter.py
- FOUND: tools/intel/refresh.py
- FOUND: channel-data/youtube-intelligence.md
- FOUND: commit 0cdb5a7 (Task 1 — algo synthesizer and pattern analyzer)
- FOUND: commit 6316eae (Task 2 — KB exporter and refresh orchestrator)

---
*Phase: 43-youtube-intelligence-engine*
*Completed: 2026-02-21*
