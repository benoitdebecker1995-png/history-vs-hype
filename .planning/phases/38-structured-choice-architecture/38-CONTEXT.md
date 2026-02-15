# Phase 38: Structured Choice Architecture - Context

**Gathered:** 2026-02-14
**Status:** Ready for planning

<domain>
## Phase Boundary

Script-writer-v2 generates 2-3 opening hook variants and 2 structural approach variants when using `/script --variants`. User's choices are logged to database with project context. After 5+ choices, system recommends preferred options based on past patterns. Agent prompt consolidated within 1,500 line budget.

</domain>

<decisions>
## Implementation Decisions

### Variant Presentation
- Sequential with labels (Hook A, Hook B, Hook C) — user picks by letter
- Summary + key difference for structural approaches (3-5 sentences per approach, not full outlines)
- Footnote-style technique attribution (hook text first, Part 8/6 source as subtle note below)
- Flow: hook first, then structure — two sequential choice points before full script generation

### Choice Logging
- Log the picked variant AND all rejected variants (enables analysis of what user consistently avoids)
- Project-linked storage: choices stored in DB with video project path and topic type as columns
- Review via both CLI (`technique_library.py --choices`) and surfaced in `/script` before generation ("You chose visual contrast 4/5 times for territorial topics")
- Keep all choices forever — weight recent choices higher when recommending (recency-weighted)

### Recommendation Behavior
- Pre-rank with rationale: show all variants but rank preferred first with "(Recommended - you chose this pattern 4/5 times for territorial topics)"
- Topic-specific first: use topic-type patterns if 3+ choices exist, fall back to global if insufficient data
- Auto-adjust after 3 consecutive overrides — system recalculates and stops recommending that pattern
- Never auto-skip variants — always show when --variants flag is used. Recommendations inform order, not skip.

### Agent Prompt Consolidation
- Equal priority for voice/style rules (1-13) and data-driven rules (14-17) — merge overlapping rules rather than cutting
- Rule 13: condense to compact checklist format (forbidden phrases, validation checks as list, not prose)
- Rule 16 (choice generation): concise with references — brief instructions pointing to Part 8 and STYLE-GUIDE for examples
- 1,500 line budget is a soft target — allow up to 1,800 if quality would suffer from more cuts

### Claude's Discretion
- Exact format of the comparison display (spacing, borders, etc.)
- How recency weighting is calculated (exponential decay, linear, etc.)
- Which overlapping rules to merge during consolidation
- Fallback thresholds for topic-specific vs global recommendations

</decisions>

<specifics>
## Specific Ideas

- Variant presentation should feel like a quick A/B decision, not a lengthy review process
- Past choice patterns should surface naturally in /script output without requiring a separate command
- The choice logging should be invisible friction — just pick a letter and move on, logging happens silently
- Consolidation should preserve the "calm prosecutor" voice identity above all else

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 38-structured-choice-architecture*
*Context gathered: 2026-02-14*
