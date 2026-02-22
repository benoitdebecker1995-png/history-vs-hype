# Phase 46: Project Dashboard - Context

**Gathered:** 2026-02-21
**Status:** Ready for planning

<domain>
## Phase Boundary

Enhance /status to show all projects in _IN_PRODUCTION/ with current phase, next action, days since last activity. Projects ranked by priority (filming-ready first). Time-sensitive topic flagging using YouTube Intelligence Engine data.

</domain>

<decisions>
## Implementation Decisions

### Dashboard output format
- Enhance existing /status command (not a new command)
- Table format showing: project name, current phase, next action, days since activity
- Projects sorted by priority: filming-ready > research phase > ideas
- Brief and scannable — not a wall of text

### Priority ranking logic
- Detect project phase from files present: FINAL-SCRIPT.md = filming-ready, 02-SCRIPT-DRAFT.md = scripting, 01-VERIFIED-RESEARCH.md = research, just folder = idea
- Days since last activity from git log or file modification dates
- Flag stale projects (>14 days inactive)

### Time-sensitive flagging
- Read youtube-intelligence.md for trending topics and deadline data
- Cross-reference project topics against intel data
- Flag format: brief note next to project (e.g., "ICJ ruling 2027 — deadline approaching")
- Skip silently if no intel data available

### Claude's Discretion
- Exact table formatting and column widths
- How to detect project topic for intel cross-reference
- Whether to include archived projects count as summary line
- Color/emoji usage in output

</decisions>

<specifics>
## Specific Ideas

- Should feel like a project manager's daily standup view — what needs attention NOW
- Priority ranking should make it obvious what to work on next
- Time-sensitive flags are the differentiator — not just "what's there" but "what's urgent"

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope.

</deferred>

---

*Phase: 46-project-dashboard*
*Context gathered: 2026-02-21*
