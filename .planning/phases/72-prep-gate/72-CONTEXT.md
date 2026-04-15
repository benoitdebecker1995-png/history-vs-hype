# Phase 72: Prep Gate - Context

**Gathered:** 2026-04-15
**Status:** Ready for planning

<domain>
## Phase Boundary

Block `/prep` when `03-FACT-CHECK-VERIFICATION.md` verdict is not APPROVED. Users cannot enter filming prep on a video that has not passed the fact-check quality gate. Display the verdict and outstanding revision items when blocking.

</domain>

<decisions>
## Implementation Decisions

### Verdict detection
- Scan for lines containing "Verdict:" (case-insensitive) and check if "APPROVED" keyword appears anywhere in that line
- Catches variants like "APPROVED FOR FILMING", "APPROVED WITH NOTES", etc.
- Anything without APPROVED = blocked
- Verdict must explicitly say APPROVED — do not infer approval from resolved fix counts
- If verdict says APPROVED but required fix sections exist, pass with warning showing fix count

### Mode gating
- Gate ALL /prep modes: --edit-guide, --assets, --full, --split-screen
- Gate interactive mode too (check before presenting options)
- All of these are pre-filming prep, so all require verified facts

### Missing file behavior
- Missing file = BLOCK (not warn). Unlike Phase 71's research gate, missing fact-check means the verification step was skipped entirely
- Placeholder files (exist but contain no verdict line) = treat as missing, block with message "Fact-check file exists but contains no verdict"

### Block/pass message format
- BLOCK: Show verdict found (or "No verdict"), count of issues by severity, and list each item with one-line description
- PASS: Show verdict + summary stats from the executive summary table (claims verified, minor, clarification, fixed)
- Follow Phase 71's message format pattern (bordered block with clear BLOCKED/PASSED label)

### Claude's Discretion
- Exact regex/parsing approach for verdict line detection
- How to extract issue counts from varying file formats
- Message formatting details within the established pattern

</decisions>

<specifics>
## Specific Ideas

- Follow the exact same gate pattern as Phase 71's Research Verification Gate in `/script` — read file, parse, apply logic, display bordered message
- Real example format from Haiti project: `**Overall Verdict:** APPROVED FOR FILMING (with 1 required fix)` with executive summary table and `REQUIRED FIX` sections marked with red circle emoji
- Somaliland project shows placeholder format: `**Status:** WAITING FOR PHASE 2 COMPLETION` with no verdict line

</specifics>

<code_context>
## Existing Code Insights

### Reusable Assets
- Phase 71's Research Verification Gate in `.claude/commands/script.md` (lines 147-204): exact pattern to replicate — file lookup, marker counting, gate logic, bordered message
- `/verify` command generates `03-FACT-CHECK-VERIFICATION.md` with the verdict and fix sections

### Established Patterns
- Gate message format: `--- GATE NAME: BLOCKED/PASSED ---` with project name, counts, and fix instructions
- File lookup: Glob for `video-projects/**/[project]/03-FACT-CHECK-VERIFICATION.md`
- Modes that skip gates: Phase 71 skips for --revise, --review, --teleprompter (but Phase 72 gates all modes)

### Integration Points
- Gate goes into `.claude/commands/prep.md` as a new mandatory section before any generation
- Runs after Channel Insights Context and YouTube Intelligence Context sections but before any output generation

</code_context>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 72-prep-gate*
*Context gathered: 2026-04-15*
