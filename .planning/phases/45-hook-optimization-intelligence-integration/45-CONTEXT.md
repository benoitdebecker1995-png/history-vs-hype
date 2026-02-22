# Phase 45: Hook Optimization & Intelligence Integration - Context

**Gathered:** 2026-02-21
**Status:** Ready for planning

<domain>
## Phase Boundary

Script-writer-v2 gets Rule 19 for algorithm-optimized hooks (cold fact → myth → contradiction → payoff). Hooks reference YouTube Intelligence Engine data for current best practices. Intelligence insights auto-surface during /script, /prep, /publish without manual lookup.

</domain>

<decisions>
## Implementation Decisions

### Hook structure (Rule 19)
- Follow cold fact → myth → contradiction → payoff structure for first 60 seconds
- Rule 19 should be flexible enough to adapt to different video types (territorial vs ideological vs untranslated)
- Hook should integrate naturally with existing Rule patterns (especially Rule 1 opening hooks and Rule 6 structure)
- Include retention triggers: information gap, visual carrot, authority signals

### Intelligence surfacing
- Follow same pattern as Phase 44's channel insights: read a file, display advisory block
- YouTube intelligence (youtube-intelligence.md) should surface during /script, /prep, /publish
- Advisory should be brief (2-3 lines) and workflow-specific (hook tips for /script, format tips for /prep, title patterns for /publish)
- Skip silently if intel file missing

### Intel freshness
- Reference live youtube-intelligence.md data, not hardcoded assumptions
- If data is stale (>30 days), note staleness but still use it
- Fallback to sensible defaults if no intel data available at all

### Claude's Discretion
- Exact hook formula variations per video type
- How Rule 19 interacts with existing Rules 1, 6, 17
- Intelligence section placement within command prompts
- Whether to combine with Phase 44's channel insights or keep separate

</decisions>

<specifics>
## Specific Ideas

- Hook structure inspired by channel's best performers: Belize (23K views) opened with territorial claim, Dark Ages opened with myth contradiction
- Intelligence surfacing should feel like Phase 44's channel insights pattern — proven approach
- Rule 19 should reference the retention science from Phase 36 and creator techniques from Phase 37

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope.

</deferred>

---

*Phase: 45-hook-optimization-intelligence-integration*
*Context gathered: 2026-02-21*
