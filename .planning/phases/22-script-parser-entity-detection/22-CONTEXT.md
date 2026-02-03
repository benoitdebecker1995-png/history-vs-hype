# Phase 22: Script Parser & Entity Detection - Context

**Gathered:** 2026-02-03
**Status:** Ready for planning

<domain>
## Phase Boundary

Foundation for extracting structure and entities from scripts. Parses markdown scripts into structured sections, extracts named entities (places, people, documents, dates, organizations), classifies entities by type, and calculates section word counts for timing estimation.

This is infrastructure consumed by Phases 23-26. No user-facing output files — just Python modules that downstream phases call.

</domain>

<decisions>
## Implementation Decisions

### Section Detection
- Scripts use **markdown H2 headers (##)** as section boundaries
- Header names are **topic-specific** (e.g., "The Treaty", "Modern Consequences"), not standardized
- If script has no ## headers, treat entire script as **one section**
- Scripts may or may not have H1 title or YAML frontmatter — handle both cases

### Entity Types
- Extract **5 entity types**: Places, People, Documents, Dates/Events, Organizations
- Organizations are a **separate type** (not merged with places/people)
- **Deduplicate entities** but also track mention positions
  - Output: unique entity list with mention count + list of positions in script

### Script Format
- **Markdown only** (.md files)
- Handle scripts with or without title headers
- Treat missing headers as single-section script (don't error)

### Claude's Discretion
- **Detection method**: Choose between regex patterns, NLP (spaCy), or hybrid based on tradeoffs
- **Output format**: Dataclasses vs plain dicts — follow existing codebase patterns
- **File caching**: Whether to write JSON cache of parsed results
- **Module location**: Where to place in tools/ directory
- **Word count granularity**: Per-section vs also per-entity-mention context
- **Section type inference**: Whether to infer intro/body/conclusion by position
- **Elements to ignore**: Which markdown elements (comments, code blocks) to skip

</decisions>

<specifics>
## Specific Ideas

No specific requirements — open to standard approaches. User deferred most implementation details to Claude's judgment.

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope.

</deferred>

---

*Phase: 22-script-parser-entity-detection*
*Context gathered: 2026-02-03*
