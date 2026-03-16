# Phase 66: External Benchmark Research - Context

**Gathered:** 2026-03-16
**Status:** Ready for planning

<domain>
## Phase Boundary

Research deliverable only — zero code. Produce benchmark data files that anchor all downstream tool recalibration (Phases 67-70) to external niche reality. Four deliverables: `niche_benchmark.json`, `niche-hook-patterns.md`, `HOOK-PATTERN-LIBRARY.md`, and fresh CTR snapshots via ctr_tracker.py.

</domain>

<decisions>
## Implementation Decisions

### Channel Selection Criteria
- 500K+ subscribers only — large enough for reliable CTR pattern data
- Format-matched to History vs Hype: talking head + evidence B-roll, document-based, maps (e.g., Kraut, Knowing Better, Shaun, History Matters style)
- No animation-heavy or high-production channels whose CTR norms reflect unreplicable formats
- Research phase identifies channels (not pre-seeded by user) — Claude discovers candidates, user approves final list
- 5-8 channels — Claude picks count based on data availability, minimum 5 per roadmap success criteria

### Benchmark JSON Structure
- **Granularity:** Range + median per pattern: `{min_ctr, max_ctr, median_ctr, sample_count, example_titles}`
- **Two dimensions:** Title pattern AND topic type as separate axes (enables BENCH-03 different CTR targets by topic type)
- **Content:** Aggregated stats + 2-3 example titles per pattern for human reference (no full raw data dump)
- **Metadata header:** `{collected_date, channels_sampled, total_videos_analyzed, refresh_after}` for automated staleness detection by benchmark_store.py

### Hook Pattern Extraction
- **Outlier identification:** Views-to-subscriber ratio (3x+ typical views) — videos where packaging + hook demonstrably worked
- **Analysis depth:** Rhetorical move classification (cold_fact, myth_contradiction, authority_challenge, specificity_bomb) with exact first sentence as example
- **Library structure:** Separated by topic type (territorial, ideological, political fact-check, etc.) to directly enable HOOK-02 requirement
- **Examples:** 8-10 per pattern type — comprehensive enough for script-writer-v2 to pick from

### Research Method
- **CTR proxy:** Views-based proxy only (views/subscriber ratio + view velocity). No VidIQ-estimated CTR — keeps methodology consistent
- **Transcript extraction:** Claude's discretion on method (auto-captions via yt-dlp, YouTube transcript API, or manual — whichever is most efficient)
- **Execution model:** Hybrid — Claude gathers what it can programmatically (channel discovery, transcript extraction, view counts via web search), user manually verifies and adds any CTR proxy data from VidIQ
- **CTR refresh:** ctr_tracker.py run included as Phase 66 deliverable (success criteria #4)

### Claude's Discretion
- Exact channel count (5-8 based on data availability)
- Transcript extraction method (auto-captions vs manual)
- JSON field naming conventions
- How to handle channels with inconsistent upload formats (some talking head, some not)
- Whether to include a "confidence" field per benchmark entry based on sample size

</decisions>

<specifics>
## Specific Ideas

- CTR proxy assumption: high views/subscriber ratio = good packaging (not just algorithmic luck). This is directional, not precise — benchmark data is advisory, not a hard gate
- Hook pattern library needs to be agent-consumable — structured so script-writer-v2 Rule 19 and hook_scorer.py can parse it programmatically
- Roadmap note: "Benchmark data is advisory, not a hard gate — own-channel score remains primary; niche percentile is additive context"

</specifics>

<code_context>
## Existing Code Insights

### Reusable Assets
- `tools/title_scorer.py`: Current title scoring with pattern detection (versus, declarative, how_why, question, colon). Phase 67 will add niche benchmark comparison
- `tools/research/hook_scorer.py`: Existing hook scorer — Phase 69 will add external pattern matching
- `tools/youtube_analytics/benchmarks.py`: Channel CTR benchmarks with category breakdown — Phase 67 will extend with niche comparison
- `tools/youtube_analytics/ctr_tracker.py`: Automated CTR refresh via YouTube Analytics API + Windows Task Scheduler

### Established Patterns
- Title patterns already classified: versus, declarative, how_why, question, colon — benchmark JSON should use same pattern names
- Topic types already classified: territorial, ideological, political fact-check — benchmark JSON should use same type names
- `tools/discovery/database.py` (KeywordDB): Existing pattern for storing/querying structured performance data

### Integration Points
- Phase 67 creates `tools/benchmark_store.py` to read `niche_benchmark.json` — JSON structure must be stable
- Phase 69 reads `HOOK-PATTERN-LIBRARY.md` for hook style recommendations
- `script-writer-v2` Rule 19 (4-beat hook formula) will reference hook pattern library examples

</code_context>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 66-external-benchmark-research*
*Context gathered: 2026-03-16*
