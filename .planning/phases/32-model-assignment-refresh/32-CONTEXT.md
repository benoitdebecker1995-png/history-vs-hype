# Phase 32: Model Assignment Refresh - Context

**Gathered:** 2026-02-09
**Status:** Ready for planning

<domain>
## Phase Boundary

Update all slash command files and agent configurations from outdated Claude 3.5 model names to current Claude 4.x model IDs. Close out Phase 28.1 (Plan 02 skipped). Verify no old model references remain.

</domain>

<decisions>
## Implementation Decisions

### Model Tier Mapping
- Keep existing tier assignments from Phase 13.1 (Opus/Sonnet/Haiku per command) — Claude reviews and flags any obvious mismatches but preserves the current distribution
- Script-writer-v2 stays on Opus — script quality is the channel's competitive edge, don't downgrade
- Model ID format: Claude picks what works best with Claude Code's model routing (short aliases vs full versioned IDs)

### Phase 28.1 Closure
- Skip Phase 28.1 Plan 02 (routing validation via OpenRouter) entirely — not worth pursuing
- Mark Phase 28.1 as complete in roadmap with note that Plan 02 was deliberately skipped
- Claude decides whether to reference the 28.1 token audit findings (routing notes) without scope creep

### Verification Approach
- Claude picks the appropriate verification level (grep audit, smoke test, or both)
- Claude decides whether a MODEL-REFERENCE.md document adds value given the file count

### Scope of Refresh
- Claude determines the full scope by grepping for old model IDs across the repo
- At minimum: 13 slash command YAML frontmatter + agent files in .claude/agents/
- At maximum: full repo sweep including docs (CLAUDE.md, STATE.md, etc.) if old references found
- Update existing MODEL-ASSIGNMENTS.md from Phase 13.1 — Claude checks format and decides approach
- Claude decides whether to close Phase 4 (Workflow Simplification — DEFERRED) as part of roadmap cleanup

### Claude's Discretion
- Extended thinking annotations in agent configs (whether to add explicit flags or let Claude Code handle it)
- Whether to include routing-readiness notes from 28.1 audit in command files
- Exact model ID format (short vs versioned)
- Verification depth (grep-only vs grep + smoke test)
- Whether MODEL-REFERENCE.md should be created/updated
- Phase 4 cleanup in roadmap

</decisions>

<specifics>
## Specific Ideas

- Current model IDs: claude-opus-4-6, claude-sonnet-4-5-20250929 (or claude-sonnet-4-5), claude-haiku-4-5-20251001 (or claude-haiku-4-5)
- Phase 13.1 created MODEL-ASSIGNMENTS.md — check and update that file
- 28.1 TOKEN-AUDIT.md has the routing tier analysis if Claude wants to reference it
- This is the last phase in v1.6 Click & Keep — completing it ships the milestone

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 32-model-assignment-refresh*
*Context gathered: 2026-02-09*
