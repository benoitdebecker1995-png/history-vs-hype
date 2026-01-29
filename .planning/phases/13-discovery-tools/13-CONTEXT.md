# Phase 13: Discovery Tools - Context

**Gathered:** 2026-01-29
**Status:** Ready for planning

<domain>
## Phase Boundary

SEO and keyword research tools for YouTube topic discovery. Includes long-tail keyword extraction, search intent classification, impression/CTR diagnostics, and metadata consistency checking. Tools help find topics that fit the channel's "historical method + primary sources" value proposition.

</domain>

<decisions>
## Implementation Decisions

### Keyword Extraction
- **Sourcing:** Both YouTube autocomplete scraping AND manual seed entry
- **Seed format:** Single topic or comma-separated batch supported
- **All lengths included:** Not filtered to 3-4 words only
- **Search volume:** Include estimates if available (VidIQ or similar)
- **Persistence:** Keyword database tracks research over time
- **Competitor keywords:** Include analysis of what Kraut, Knowing Better, etc. rank for

### Intent Classification
- **Categories:** Custom for history niche, reflecting "historical method + primary sources" value
  - Categories should capture: myth-busting, territorial disputes, ideological narratives, primary source reveals, timeline corrections, etc.
- **Multi-intent:** Primary + secondary intent supported (not single-label)
- **Channel DNA fit score:** Flag titles that match documentary/evidence style
- **Learn from analytics:** Weight categories by what performed well historically
- **Competitor reference:** Use COMPETITOR-TITLE-DATABASE.md for pattern learning
- **Explanations:** Brief by default, detailed rationale on demand (flag)

### Diagnostic Thresholds
- **Impression baseline:** Compare to channels of similar size (not fixed numbers)
- **Data source:** YouTube Analytics API for benchmarks
- **7-day window:** Standard discovery period for analysis
- **CTR threshold:** Claude determines appropriate threshold
- **Integration:** Extend existing /analyze command (not separate)
- **Fixes:** Actionable suggestions for immediate fixes PLUS learning for future videos
- **Rescue suggestions:** Identify underperformers worth updating, mainly to learn from

### Output Format
- **Interface:** Mix of new commands and extensions to existing (/research, /analyze, /publish)
- **Storage:** Both project-specific folders AND central channel-data
- **Format:** Markdown tables default, --json flag for programmatic use
- **Metadata check:** Integrated into /publish as pre-publish gate AND standalone
- **History:** Optional --history flag for trends over time
- **Verbosity:** -q flag for quick mode, detailed by default
- **Queryable database:** Claude determines useful query patterns

### VidIQ Integration
- **API approach:** Check if VidIQ API available; if not, provide prompts for manual input
- **Guided workflow:** Step-by-step prompts ("Now search X in VidIQ, paste results")
- **Data value:** All VidIQ data valuable (search volume, competitor stats, predictions)
- **Storage:** Project-specific (in video-project folder when researching a topic)
- **DNA conflicts:** Nuanced recommendations explaining trade-offs, user decides

### Claude's Discretion
- Number of autocomplete suggestions per seed keyword
- Topic grouping from keywords (if useful)
- Title variant suggestions (classify + suggest if useful)
- Confidence scores for intent classification
- Diagnostic learnings feeding into keyword database
- Contextual help links in outputs
- VidIQ prediction tracking against actual performance
- Channel DNA filter application

</decisions>

<specifics>
## Specific Ideas

- "I like to bring the historical method to a wider audience and show the primary sources when possible" — this is the channel's core value proposition
- Intent categories should reflect content types: myth-busting, territorial disputes, ideological narratives, primary source reveals
- Learning from diagnostics is key — not just fixing current video but improving future ones
- Your existing pattern recognition (/patterns) should connect with diagnostic learnings

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 13-discovery-tools*
*Context gathered: 2026-01-29*
