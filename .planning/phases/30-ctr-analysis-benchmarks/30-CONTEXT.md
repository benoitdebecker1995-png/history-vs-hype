# Phase 30: CTR Analysis & Benchmarks - Context

**Gathered:** 2026-02-07
**Status:** Ready for planning

<domain>
## Phase Boundary

Statistical analysis of CTR data to determine winning thumbnail/title variants and establish channel-specific performance benchmarks by topic category. Uses data from Phase 29's variant tracking (CTR snapshots, variant registrations). Only applies to long-form videos (not Shorts).

</domain>

<decisions>
## Implementation Decisions

### Significance testing
- Practical heuristic approach (not full statistical tests) — simple rules a solo creator can act on
- Minimum CTR difference threshold: Claude's discretion (based on channel's typical CTR range)
- Verdict labels: Claude's discretion (match the channel's direct, evidence-based tone)
- Single-variant videos: compare against category average CTR (don't require A/B pair to give feedback)

### Benchmark categories
- Category system: Claude's discretion (reuse Phase 19 classify_topic() categories or adjust based on video count and distribution)
- Minimum videos per category: Claude's discretion (based on catalog size)
- Always show BOTH overall channel average AND category-specific average for context
- Benchmark comparison method (latest vs 7-day standardized): Claude's discretion (pick fairest comparison)

### Output & presentation
- Two entry points: quick summary in /analyze AND detailed standalone CLI command
- /analyze: add verdict/context alongside existing Phase 29 variant tables — format at Claude's discretion
- Standalone CLI: terminal output by default, --markdown flag for file output (matches existing CLI patterns)
- Action recommendations: Claude's discretion on when to recommend (switch, wait, record more)

### Decision thresholds
- Minimum impression count before comparing: Claude's discretion (based on channel impression velocity)
- Minimum snapshots for trending: Claude's discretion (balance between early signal and reliability)
- Data freshness warning: Claude's discretion (threshold that matches publishing cadence)
- Active variant attribution (--thumbnail-id, --title-id): Claude's discretion (enforce vs keep optional)
- **Long-form videos only** — exclude Shorts from all CTR analysis and benchmarks

### Claude's Discretion
- Minimum CTR difference threshold for "winner" verdict
- Verdict label language
- Category system granularity
- Minimum videos per category bucket
- Benchmark time window (latest vs standardized snapshot)
- Impression minimum for comparison
- Snapshot minimum for trending
- Freshness warning threshold
- Active variant attribution enforcement
- When to show recommendations vs just data

</decisions>

<specifics>
## Specific Ideas

- Channel currently has ~10 published long-form videos (197 subs, 82K+ views)
- Existing Phase 19 topic classification: territorial, ideological, legal
- Phase 29 record-ctr already has optional --thumbnail-id and --title-id flags
- Phase 29 trend calculation already shows UP/DOWN/FLAT with 2+ snapshots
- VidIQ scores don't predict this channel's performance (83-scored title got 21x more views than 97-scored) — benchmarks should be channel-specific, not industry averages

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 30-ctr-analysis-benchmarks*
*Context gathered: 2026-02-07*
