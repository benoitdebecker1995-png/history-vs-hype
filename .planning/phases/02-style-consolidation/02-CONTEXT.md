# Phase 2: Style Consolidation - Context

**Gathered:** 2026-01-20
**Status:** Ready for planning

<domain>
## Phase Boundary

Single authoritative style reference that scriptwriter enforces consistently. Consolidates scattered style notes into one document, captures new preferences automatically, and ensures the scriptwriter agent applies these rules.

Requirements:
- STYL-01: Consolidate scattered style notes into one authoritative reference
- STYL-02: Scriptwriter enforces spoken-delivery voice (not essay voice)
- STYL-03: Preference tracking system (captures word choices, patterns from feedback)

</domain>

<decisions>
## Implementation Decisions

### Style doc structure
- Supports both quick lookup and full read-through
- Categorized rules with brief examples (not example-first or rules-only)
- Brief rationale for each rule (one line explaining "why")
- Claude decides section organization based on existing style notes

### Preference capture
- Auto-capture: corrections automatically logged without explicit prompts
- Direct to guide: new patterns added immediately (no staging file)
- Format: rule statement plus before/after example pair
- Claude decides whether USER-PREFERENCES.md speaking patterns section merges into style guide

### Scriptwriter enforcement
- Guidelines with judgment: follow rules but deviate if context warrants
- Flag only major deviations (structural/voice changes, not minor wording)
- Core non-negotiable: spoken delivery (must sound natural when read aloud)
- Both internalized and referenced: core rules baked into script-writer-v2 agent, full guide available as reference

### Source consolidation
- Keep old files as supplements (main guide for rules, old files for extended examples/context)
- Claude lists scattered style files to consolidate
- Location: Claude decides based on existing structure
- CLAUDE.md: summarize + link (brief summary, "See STYLE-GUIDE.md for full rules")

### Claude's Discretion
- Section organization for style guide
- Whether to merge USER-PREFERENCES.md speaking patterns into style guide
- Exact location of authoritative style guide file
- How to structure the "supplements" relationship with old files

</decisions>

<specifics>
## Specific Ideas

- The scriptwriter should read like explaining to a friend, not reading a document
- Auto-capture means when user makes a correction like "don't say X, say Y", that pattern gets added
- Rule format example: "Use ordinal dates with 'On' prefix for spoken delivery" + "On June 16th, 2014" not "June 16, 2014"

</specifics>

<deferred>
## Deferred Ideas

None - discussion stayed within phase scope

</deferred>

---

*Phase: 02-style-consolidation*
*Context gathered: 2026-01-20*
