# Phase 15: Database Foundation & Demand Research - Context

**Gathered:** 2026-01-31
**Status:** Ready for planning

<domain>
## Phase Boundary

Tools that quantify search demand for potential video topics. User can input keywords and get search volume proxy, trend direction, related query expansion, and competition ratio scoring. This is the data foundation — competition analysis, format filtering, and opportunity scoring are separate phases.

</domain>

<decisions>
## Implementation Decisions

### Output Format
- Both table and JSON via flag — default to table, --json for machine-readable
- Summary default, -v for full breakdown — concise by default, verbose flag for complete data
- Related queries in separate section — main keyword first, then "Related:" section below
- Batch results sorted by opportunity — best opportunities at top (highest demand/competition ratio)

### Scoring Interpretation
- Both ratio + category — show "4.2x (High Opportunity)" with number plus interpretation
- Conservative thresholds (4x+ = High) — High: >4x, Medium: 2-4x, Low: <2x — only flag obvious opportunities
- Arrow + percentage for trends — ↑ +45% or ↓ -20% — visual direction with exact change
- No legend (docs only) — keep output clean, reference documentation if confused

### CLI Invocation
- Extend /discover — add --demand flag to existing command for consolidated interface
- Quoted for multi-word — /discover --demand "sykes picot" — quotes for phrases, optional for single words
- Both file and inline batch — support --file keywords.txt AND comma-separated inline
- Auto-save to database — all queries cached in keywords.db automatically, build history over time

### Data Freshness
- 7 day cache duration — weekly refresh, trends change slowly for historical topics
- Warning + use cached — "Data is 45 days old" but still show it, you decide if refresh needed
- --refresh flag for force refresh — ignore cache and fetch fresh data on demand
- Fall back to stale cache on API failure — show old data with warning, something better than nothing

### Claude's Discretion
- Exact table column widths and formatting
- Database schema details beyond what's specified
- Error message wording
- Internal caching implementation

</decisions>

<specifics>
## Specific Ideas

- Conservative opportunity thresholds (4x+) reflect that this channel has high research overhead — only pursue obvious wins
- Auto-save builds keyword research history over time without extra effort
- 7-day cache balances freshness with API limits for historical topics that don't trend rapidly

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 15-database-foundation-demand-research*
*Context gathered: 2026-01-31*
