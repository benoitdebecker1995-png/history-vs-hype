# Phase 73: Foundation - Context

**Gathered:** 2026-04-22
**Status:** Ready for planning
**Source:** v9.0 ROADMAP.md + REQUIREMENTS.md (AGENT-01)

<domain>
## Phase Boundary

Codify the agent-orchestration rules that every subsequent v9.0 phase cites. Write `.claude/AGENT-ORCHESTRATION.md` as the single authoritative rules document governing: when to spawn sub-agents, the return contract sub-agents must honor, how to partition references across tiers, and how to behave under rate limits.

Without this doc, Phases 74–79 lack a reference standard and v9.0's thesis ("rules that keep it clean") collapses — same failure mode as v1.0 Phase 05 (cleanup that re-accumulated within months).

**In scope:** Writing the rules doc + minimal integration touches (CLAUDE.md reference line, USER-PREFERENCES.md "Main context = orchestrator only" section).

**Out of scope:** Applying the rules to any command/agent (that's Phase 75a–d's work), refactoring existing agents (cross-cutting work deferred to Phase 75a pilot).

</domain>

<decisions>
## Implementation Decisions

### Document structure (locked)
The doc MUST contain these 5 named sections so every later phase can cite a specific anchor:

1. **Spawning pattern** — when to spawn (read >500 lines, reasoning >3 steps, parallel independent work), how to invoke, what to put in the prompt
2. **Return contract** — the copy-pasteable block that every sub-agent's prompt must include; defines: ≤200-word summary, write full output to disk (not into return), no raw quotes dumped into main context, explicit handoff path
3. **Reference loading tiers** — Tier 0 (always-loaded: CLAUDE.md, MEMORY.md), Tier 1 (phase-critical: loaded by orchestrator), Tier 2 (task-specific: loaded by sub-agent only), Tier 3 (on-demand: loaded only if cited by user or prior artifact)
4. **Rate-limit resilience** — sequential-over-parallel fallback rule: detect 429 / rate-exceeded, serialize spawning, retry sequentially instead of failing
5. **"Extend, don't add" default** — before creating any new ref/command/agent, check whether an existing one can absorb the change. New surface area requires justification. Doc itself is an example (stays under 400 lines).

### Return contract specifics (locked)
The return contract block is the single most-reused artifact — it gets pasted verbatim into agent prompts in Phase 75a–d and Phase 77. It MUST include:
- Line describing the ≤200-word summary requirement (structured: what / where output lives / what's next)
- Explicit "write full output to disk" instruction with path convention
- Explicit "do NOT dump raw quotes, transcripts, or >10-line excerpts into the return" instruction
- Handoff format: `OUTPUT: <absolute-path>` line for the orchestrator to pick up

### Integration touches (locked)
- `CLAUDE.md` — add one line in Critical Reminders section: "15. Read `.claude/AGENT-ORCHESTRATION.md` before spawning sub-agents — return contract, tiers, rate-limit rule"
- `.claude/USER-PREFERENCES.md` — add a new section "Main Context = Orchestrator Only" that restates the core rule and points to AGENT-ORCHESTRATION.md

### Doc length constraint (locked)
Hard cap: 400 lines. The doc itself is the first test of "extend, don't add" — if it bloats past 400 lines, it has already failed its own rule. Prefer examples over explanation; reference the worked-example section (added later in Phase 75a) rather than inlining every pattern.

### Claude's Discretion
- Exact section headings and order (beyond the 5 named sections above)
- Whether to include a short "Why this doc exists" preamble or jump straight to rules
- Examples for the spawning pattern section (concrete or abstract — either is fine as long as a future session can cite the section)
- Wording of the return contract block (as long as all 4 required elements are present)

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### v9.0 Milestone Context
- `.planning/ROADMAP.md` — Phase 73 entry (line 244), dependency graph showing every later phase cites this doc
- `.planning/REQUIREMENTS.md` — AGENT-01 definition (line 18), plus the Out-of-Scope table that bounds v9.0

### Existing Surface to Reference (not modify)
- `.claude/agents/*.md` — 9 existing agents (inventory only — Phase 75a applies the contract to them, not this phase)
- `.claude/commands/research.md` — pilot target for Phase 75a (referenced here only to ground the "what the rules will apply to")
- `.claude/USER-PREFERENCES.md` — target for one of the integration touches

### v9.0 Regression Defense
- The load-bearing claim in ROADMAP is that Phase 79's monthly surface-area check enforces "extend, don't add". Phase 73 codifies the rule; Phase 79 enforces it. This linkage must be explicit in the doc so future sessions see it.

</canonical_refs>

<specifics>
## Specific Ideas

- The return contract block is the single most-copied artifact in v9.0. Treat it like an API contract — if it changes later, every pasted instance has to be updated. Get it right the first time.
- The doc is cited by ROADMAP's Phase 75a success criterion #7: "Pattern documented in `.claude/AGENT-ORCHESTRATION.md` as a concrete worked example". So the doc needs a section that Phase 75a will *extend* with a worked example — not a section Phase 75a re-writes. Leave a named placeholder: `## Worked Examples` (empty in Phase 73, filled in Phase 75a).
- "Main context = orchestrator only" is both a user-preferences rule AND an agent-orchestration rule. Put the full rationale in AGENT-ORCHESTRATION.md; put a one-line pointer + "why it matters for session flow" in USER-PREFERENCES.md.
- Rate-limit resilience is explicitly called out in ROADMAP Phase 75a success criterion #6. The rule in this doc is the spec; Phase 75a is the first implementation. The doc must be concrete enough that Phase 75a can implement without re-deciding.

</specifics>

<deferred>
## Deferred Ideas

- Per-agent token measurement patterns — deferred to Phase 79 (TOK-02)
- Reference-load accounting format — deferred to Phase 79 (TOK-04)
- Concrete worked examples of the spawning pattern — deferred to Phase 75a (pilot adds them after the pattern is proven on `/research`)
- Agent pool manager / queue — explicitly out of scope per REQUIREMENTS.md

</deferred>

---

*Phase: 73-foundation*
*Context gathered: 2026-04-22 (derived from v9.0 ROADMAP.md Phase 73 section + REQUIREMENTS.md AGENT-01)*
*Prior context (v8.0 bridge-test, deferred): `.planning/milestones/v8.0-73-bridge-test-CONTEXT-deferred.md`*
