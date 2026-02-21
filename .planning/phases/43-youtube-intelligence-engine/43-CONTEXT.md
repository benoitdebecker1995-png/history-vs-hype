# Phase 43: YouTube Intelligence Engine - Context

**Gathered:** 2026-02-20
**Status:** Ready for planning

<domain>
## Phase Boundary

Build a local knowledge base of YouTube algorithm mechanics and history/edu niche patterns that stays current through automated refresh. Includes competitor channel monitoring with outlier detection and trend analysis. Knowledge base is queryable via dedicated command and auto-surfaces in production commands. Absorbs existing manual analysis files (SCRIPT-STRUCTURE-ANALYSIS.md, COMPETITOR-TITLE-DATABASE.md).

</domain>

<decisions>
## Implementation Decisions

### Knowledge Base Content
- Deep algorithm mechanics: full model of browse vs search vs suggested pipelines, satisfaction signals, audience segments, shadow metrics — not just practical tips
- Full niche intelligence: formats, lengths, hook styles, thumbnail patterns, title formulas, posting frequency, audience overlap for history/edu niche
- Longform only — ignore Shorts strategy entirely
- Include SEO/discovery trends: trending search terms and topic interest in history/edu niche
- Absorb and replace existing manual analysis files (SCRIPT-STRUCTURE-ANALYSIS.md, COMPETITOR-TITLE-DATABASE.md) — one source of truth
- Research best algorithm sources during planning (user doesn't have strong preferences on specific sources)
- Purge outdated data on refresh — knowledge base always reflects current reality

### Refresh Mechanism
- Integrated into workflow: auto-refresh when starting pre-production commands (/research --new, /script) if data is stale — no separate refresh command needed
- Show changes after refresh: display summary of what's new/changed since last run
- No time limit on refresh duration — comprehensiveness over speed
- Purge outdated data — replace, don't accumulate

### Query Interface
- Both natural language AND structured flags: natural language for exploration, structured flags for common queries (algorithm summary, competitor report, niche trends)
- Light integration now: script-writer agent reads KB and incorporates insights into decisions (hook structure, pacing). Phase 45 deepens this.
- Agent reads KB approach: intelligence is consumed by agents as context, not shown as tips

### Competitor Monitoring
- Research which channels to track during planning phase (beyond the 5 style references)
- Full analysis per competitor upload: titles, views, upload dates, video length, thumbnail style, topic category, engagement signals
- Include AI-generated analysis of WHY outlier videos performed (pattern identification)

### Claude's Discretion
- Storage format (SQLite vs markdown vs hybrid)
- Raw + insights vs insights-only storage decision
- Temporal tracking (changelog vs current-state-only)
- Channel size focus (small channel specific vs general + small)
- Confidence/reliability rating system for claims
- Niche scope filter (style-match channels vs broad history/edu)
- Data sources for refresh (web search vs custom scrapers vs YouTube API)
- Command name (/intel vs extending /discover)
- Output depth defaults (concise vs detailed)
- Source citations in query results
- Agent access scope (which agents read KB)
- Topic overlap alerting
- Competitor lookback period
- Channel management approach (config file vs command)
- Infrastructure sharing with /patterns command

</decisions>

<specifics>
## Specific Ideas

- User wants this as pre-production context: run refresh before each video, intelligence informs script-writer decisions
- Existing SCRIPT-STRUCTURE-ANALYSIS.md and COMPETITOR-TITLE-DATABASE.md should be migrated into the engine (absorb and replace)
- Agent-reads-KB pattern: script-writer-v2 references KB sections during generation, not shown as separate tips
- "I don't know the best sources — you research that" — researcher agent should identify authoritative YouTube algorithm sources
- Channel is 450+ subs, longform documentary format, history/edu niche — intelligence should be calibrated to this profile

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 43-youtube-intelligence-engine*
*Context gathered: 2026-02-20*
