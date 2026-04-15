# Phase 73: Bridge Test - Context

**Gathered:** 2026-04-15
**Status:** Ready for planning

<domain>
## Phase Boundary

Auto-run a full pipeline alignment check during `/publish` that blocks on mismatches before the video goes live. The check traces the full viewer pipeline: thumbnail visual → title promise → hook delivery, and blocks publishing when alignment is weak.

</domain>

<decisions>
## Implementation Decisions

### Auto-trigger scope
- Run on ALL generation modes: --metadata, --titles, --thumbs, --full, and interactive
- Skip for non-generation modes: --clips, --prompts, --intake, --synthesize, --evaluate
- If no script exists: skip silently (no message, same as Phase 71 missing-file approach)
- Run AFTER output generation, not before — test checks what was actually produced

### Scoring system
- Reuse existing TIGHT/ADEQUATE/GAP/NONE verdict system from `/publish` (lines 437-441)
- WEAK = GAP or NONE. STRONG = TIGHT or ADEQUATE
- Full pipeline check: thumbnail visual → title promise → hook delivery → turn. Check all three connections
- Require thumbnail concepts to exist before running. If no thumbnail concepts generated yet, skip bridge test silently
- Flag with fix suggestion: "WEAK ALIGNMENT: Title promises X but hook opens with Y instead. Suggestion: lead with X in first sentence." — specific gap + actionable fix

### Output format
- Bordered block inline, consistent with Phase 71-72 gate visual language
- STRONG: brief one-line confirmation ("Bridge Test: STRONG — Title delivers on hook within 15s")
- WEAK: bordered warning block with explanation of the gap
- BLOCK on WEAK alignment. WEAK bridge = stop. Can't publish with a title/hook mismatch. Matches Phase 71-72 blocking gate pattern
- Check ALL title variants when multiple are generated (A/B testing). Flag any WEAK ones individually

### Claude's Discretion
- Exact method for extracting "core promise" from title
- How to determine which part of hook "delivers" on the promise
- Formatting of multi-variant bridge results table
- How to handle cases where thumbnail concepts exist but have no overlay text

</decisions>

<specifics>
## Specific Ideas

- Existing bridge analysis in `/publish` (lines 424-443) already defines the TIGHT/ADEQUATE/GAP/NONE verdict system with specific timing thresholds — auto-bridge should use the same criteria
- Full pipeline: thumbnail visual → title promise → hook delivery. Auto-bridge now matches the comprehensive manual analysis scope
- Phase 72's bordered message pattern (BLOCKED/PASSED) should inform the visual style. Use BLOCKED for WEAK, PASSED for STRONG — this is a blocking gate like Phase 71-72

</specifics>

<code_context>
## Existing Code Insights

### Reusable Assets
- Bridge verdict definitions in `.claude/commands/publish.md` (lines 437-441): TIGHT (<15s), ADEQUATE (<30s), GAP (2min+), NONE
- Phase 71-72 bordered message pattern: `--- GATE NAME: STATUS ---` with details
- Title scorer in `tools/title_scorer.py`: entity extraction could inform promise detection

### Established Patterns
- Gates run before generation (Phase 71-72), but this check runs AFTER generation
- All /publish modes already read the script for metadata generation
- Bridge analysis section already exists in manual thumbnail pairing workflow

### Integration Points
- New section in `.claude/commands/publish.md` — runs after title + thumbnail generation, before final metadata output
- Reads `02-SCRIPT-DRAFT.md` for hook text (first 30 seconds)
- Reads thumbnail concepts for overlay text
- Tests each generated title variant individually against thumbnail + hook

</code_context>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 73-bridge-test*
*Context gathered: 2026-04-15*
