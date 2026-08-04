# Agent Orchestration Rules (v9.0)

> **Status:** Load-bearing spec for v9.0. Cited by Phases 74-79.
> **Length discipline:** Hard cap 400 lines. This doc is itself the first test of "extend, don't add" — if it grows past 400 lines, it has failed its own rule. Prefer examples and terse statements over explanation.

## Why This Doc Exists

Main context is an orchestrator. Heavy reads and multi-step reasoning are delegated to sub-agents. Main context never ingests what a sub-agent can return as a summary.

These rules are codified so the lean state survives past v9.0. Without a cite-able spec, every later refactor re-decides the same tradeoffs and drifts — the exact failure mode v1.0 Phase 05 shipped (cleanup that re-accumulated within months; see `.planning/ROADMAP.md` line 200). This doc is the regression defense. Phase 79 enforces it month-over-month via `/status --surface`.

## Spawning Pattern

**Three triggers. If ANY is true, spawn a sub-agent. Do not read in main context.**

1. Read >500 lines (any single file or cumulative across the step)
2. Reasoning >3 steps (chain-of-thought that doesn't collapse to a one-liner)
3. Parallel independent work (2+ tasks with no shared state that can execute concurrently)

**How to invoke:**

- Use the Task tool with an explicit `subagent_type`.
- Main context does NOT open the files the sub-agent will read. Not even to "check". Opening defeats the point.
- Spawn prompt MUST include three blocks:
  1. `<read_first>` — exact absolute paths the sub-agent must read
  2. Single goal — one sentence, imperative
  3. Return Contract — pasted verbatim from the fenced block in the next section (use the `<!-- RETURN-CONTRACT-V1 -->` marker as the extraction anchor)

**Anti-pattern — do not do this:**

- Main context opens the file "just to check" before spawning. Every orphan read defeats the token budget and trains the wrong habit.
- Reading the sub-agent's output file in full after the return. The summary + `OUTPUT:` handoff line is the contract; main reads the file on demand only if a specific quote or range is needed.

## Return Contract

Every sub-agent spawn prompt MUST include the fenced block below verbatim. Phase 75a-d and Phase 77 extract this block mechanically by grepping the marker range.

<!-- RETURN-CONTRACT-V1 -->
```
=== SUB-AGENT RETURN CONTRACT v1 ===

1. SUMMARY (≤200 words). Structured as:
   - What you did (1-2 sentences)
   - Where the output lives (absolute path)
   - What's next (1 sentence — the orchestrator's next move)

2. WRITE FULL OUTPUT TO DISK. Path convention:
   `.planning/phases/{phase}/agent-outputs/{agent}-{task}-{timestamp}.md`
   (or a project-appropriate path stated in the spawn prompt).
   Do NOT return the full output inline.

3. NO RAW DUMPS. Do not paste raw quotes, transcripts, or any excerpt
   >10 lines into the return. If the caller needs a specific quote,
   cite the file + line range; the orchestrator reads on demand.

4. HANDOFF LINE. Final line of the return MUST be exactly:
   `OUTPUT: <absolute-path>`
   The orchestrator parses this line to pick up the artifact.

=== END CONTRACT ===
```
<!-- /RETURN-CONTRACT-V1 -->

Phase 75a-d and Phase 77 paste this block verbatim into their agent prompts. If this contract changes, bump to `RETURN-CONTRACT-V2` and update callers — do not silently edit.

## Relayed Claims Are Not Findings

**A claim that arrives from a sub-agent is unverified until the orchestrator verifies it.** Passing it to the user as a finding is publishing someone else's unchecked work under your own name.

**The rule:** before a relayed claim drives a decision or reaches the user, either **check it** — run the query, open the file, resolve the identifier — or **label it as relayed** and say so in the same breath. Both are acceptable. Silently promoting agent output to fact is not.

**Say which is which.** A return that mixes both should read like: *"I verified the data-error findings myself; the retention figures and the search results are the agent's, relayed."*

*Why this is a rule and not a preference: on 2026-08-03 a red-team agent reported that a title "omits the only recognisable proper noun in the research." The title contained **Vatican**. The claim rested on a gap in a hand-maintained list, was relayed to the user as a finding, and was corrected by the user rather than by any check. Same session: three analytics conclusions built on a snapshot column read as lifetime, all three surfaced as fact.*

**This is ADR-0020 (`strategy claims carry the same evidentiary burden as on-screen claims`) applied to agent output.** The burden does not lighten because a sub-agent carried it.

⚠ **The corollary for sub-agent briefs:** tell the agent not to trust the orchestrator's summaries either. An agent handed "median impressions is 56" will reason from it. Brief agents to query the source themselves and say so when they cannot.

## Reference Loading Tiers

Every reference belongs to exactly one tier. Every additional ref above Tier 0 requires a named caller — no orphan refs.

- **Tier 0 — Always loaded:** `CLAUDE.md`, `MEMORY.md`. Loaded into every session unconditionally. Tier 0 is tiny on purpose.
- **Tier 1 — Phase-critical:** loaded by the orchestrator when the current phase or command cites them in its frontmatter. Example: a `/research` command that declares `@.claude/REFERENCE/NOTEBOOKLM-SOURCE-STANDARDS.md` in its context block.
- **Tier 2 — Task-specific:** loaded ONLY by the sub-agent that needs them, named in that agent's `<read_first>` block. Main context never reads these. Example: a research sub-agent reading `.claude/REFERENCE/fact-checking-protocol.md` — main never touches that file.
- **Tier 3 — On-demand:** loaded only if explicitly requested by the user mid-run or cited by a prior artifact during the current session. No frontmatter claim, no automatic inclusion.

**Core principle:** Every additional ref above Tier 0 requires a named caller — no orphan refs.

**Cross-references:** Phase 74 (REF-05) regenerates `.claude/REFERENCE/INDEX.md` with "last used by" annotations so orphan refs surface in grep. Phase 79 (TOK-04) adds reference-load accounting per command so duplication between Tier 1 and Tier 2 stays visible. This doc defines the tiers; those phases enforce them.

## Rate-Limit Resilience

Rate limits are expected, not exceptional. The orchestrator handles them; it does NOT fail the command.

**Detection surface.** On any spawn response, inspect for:

- HTTP status `429`
- Error strings matching (case-insensitive): `rate`, `rate-exceeded`, `rate limit`, `too many requests`

**Rule — sequential fallback:**

1. On detection, the orchestrator serializes pending spawns. Parallel queue collapses to sequential, one at a time.
2. The failed spawn is retried after backoff.
3. Backoff schedule: 30s, 60s, 120s. Three retries maximum.
4. If all three retries fail, the orchestrator raises an AskUserQuestion checkpoint with the failing agent name, the attempted retries, and three options (retry once more / switch to paste-prompt fallback / abort). First option = recommended.

**Spec vs implementation.** This section is the spec. Phase 75a is the first implementation — its worked example will make the sequential retry loop concrete. Subsequent phases cite this section; they do not re-decide the schedule.

### ⭐ DURABLE OUTPUT — the failure this section did NOT cover (added 2026-07-21, learned the hard way)

The rules above handle a spawn that is *refused*. They do nothing for the failure that actually cost a session: **an agent dies MID-RUN — session limit, process exit, context exhaustion — after doing all the work and before writing anything.** On 2026-07-21, five agent deaths across one day produced **four with zero output on disk**, including one that had "retrieved and read all 8 sources" and one whose message was literally "dataset is solid, now the trend tests." Hours of retrieval, thrown away.

**Every agent brief MUST carry a durable-output instruction. Non-negotiable, no exceptions:**

> "Write your output file EARLY with whatever is solid, then refine it in place. A partial file on disk beats a complete analysis that dies with the session. If you are running low on room, prioritise: (a) get the file written, (b) the headline finding, (c) the detail."

**Corollaries, all learned 2026-07-21:**
- **Scratch work is recoverable; transcripts often aren't.** An agent that leaves `results.json` + its extraction script in the scratchpad can be finished by the main thread in minutes. One did exactly that — the drift study's write-up was salvaged from `results.json` after the agent died, and the salvage even *corrected* the finding the orchestrator had already written into canon. **Tell agents to persist intermediate data, not just conclusions.**
- **Check disk before resuming or respawning.** `SendMessage` to a dead agent resumes it from its transcript when one exists, and re-does nothing. But confirm what landed first: on 2026-07-21 one agent's 46KB output file was complete on disk while its notification said "failed."
- **Session limits are account-wide.** When one agent dies on a session limit, resuming its siblings immediately just burns three more attempts on the same wall. Read the reset time out of the error and wait.
- **A spawn is not free.** Five agents ran on one video in one day; the fourth and fifth returned real value (a false canon entry overturned, a bad citation caught) but the *third* mostly confirmed prior work. Before spawning, state what decision the output will change. If the answer is "none," don't spawn.

## Extend, Don't Add

**Default rule.** Before creating any new reference, command, or agent, check whether an existing one can absorb the change. Extend first. Create only if extension is impossible.

**Acceptance test.** New surface area (a new ref file, a new command, a new agent) requires a named justification in the phase's CONTEXT.md or ROADMAP entry — not an implicit choice. "We needed a place to put it" is not a justification. "No existing surface carries this responsibility and here's the boundary" is.

**Self-test.** This doc is capped at 400 lines. If it bloats past that cap, it has failed its own rule. Split or cut — do not grow.

**Enforcement mechanism.** Phase 79 (TOK-03) runs a monthly `/status --surface` check reporting command count, ref count, Python file count, and agent count against the v9.0 baseline. A >10% increase in any count fires a warning. Rule codified here; measurement enforced there — "rule here, measurement there."

## Worked Examples

<!-- PLACEHOLDER: filled by Phase 75a (/research pilot). Do not write examples in Phase 73. -->
<!-- Phase 75a success criterion #7 (ROADMAP line 298): "Pattern documented in .claude/AGENT-ORCHESTRATION.md as a concrete worked example so 75b/c/d can cite 'apply the 75a pattern'". -->
<!-- Phase 75a APPENDS here — does not rewrite earlier sections. -->

## Running on Codex (added 2026-08-04)

Everything above is harness-neutral and applies unchanged on Codex / GPT-5.6: the three spawn
triggers, the return contract, the durable-output instruction, "a spawn is not free". Four things
differ, and only four:

| | Claude Code | Codex |
|---|---|---|
| Invocation | Task tool with `subagent_type` | `spawn_agent` (hooks match it as `Agent`) |
| Definitions | `.claude/agents/*.md` | `.codex/agents/*.toml` — port of the same files |
| Tool narrowing | `tools:` frontmatter list | no per-agent tool list; use `sandbox_mode = "read-only"` and instructions |
| Parallelism | rate-limit backoff rule above | `agents.max_concurrent_threads_per_session = 4` in `.codex/config.toml` caps it first |

**Model pins.** The TOMLs pin `gpt-5.6-sol` where the Claude file said opus, `gpt-5.6-terra` for
sonnet, `gpt-5.6-luna` for haiku. A custom agent file's `model` beats the `[agents]` default.

**The rate-limit section still applies** — the concurrency cap makes 429s rarer, not impossible, and
the sequential-fallback rule is what to do when one lands.

**Drift.** The TOMLs embed each agent body verbatim, so an edit to `.claude/agents/*.md` does not
reach Codex until it is re-ported. `tests/unit/test_codex_surface_parity.py` fails when they diverge.

## Cross-References

- `CLAUDE.md` Critical Reminders item 15 — pointer to this doc from always-loaded project instructions.
- `AGENTS.md` (repo root) — the Codex-side entry document; `.agents/skills/` + `.codex/` are the port.
- `.claude/USER-PREFERENCES.md` "Main Context = Orchestrator Only" section — user-facing restatement of the core rule.
- `.planning/ROADMAP.md` Phase 79 — monthly surface-area check via `/status --surface`; the enforcement mechanism for "Extend, Don't Add".
- `.planning/REQUIREMENTS.md` AGENT-01 (line 18) — the requirement this doc satisfies.
- `.planning/REQUIREMENTS.md` AGENT-06, AGENT-07 — return-contract standardization across agents and rate-limit resilience (both cite this doc).
