# SUMMARY — v9.0 Lean Agent-Orchestrated Workflow

**Milestone:** v9.0
**Researched:** 2026-04-21
**Confidence:** HIGH (where noted); MEDIUM for tool-level consolidation scope

---

## Executive summary

v9.0 is a meta-refactor of the workspace itself — not a content feature. The workspace has grown to 25 commands, 9 agents, 35 reference files, and ~100 Python tools. Main context regularly hits rate limits. Commands run like silent scripts instead of dialogues. A workflow-simplification milestone (v1.0 Phase 05) was already tried once and did not stick. The surface area grew back within months because no rules existed to defend it.

The v9.0 thesis is architectural, not cosmetic: **the main context should be an orchestrator only**. Every heavy read, every multi-step reasoning chain, every reference aggregation belongs inside a sub-agent whose context never returns to main — only a ≤200-word summary does. This is the single highest-leverage change for token efficiency and is the mechanism by which conversational flow becomes affordable (checkpoints cost tokens; if main is already lean, checkpoints are free).

The secondary insight is that the previous simplification failed for a specific, nameable reason: **regression by accretion**. Needs were met by adding files rather than extending existing ones. v9.0 must ship both the clean state AND the rules that keep it clean (codified in a new `.claude/AGENT-ORCHESTRATION.md`, defended by a monthly surface-area check, enforced by an "extend, don't add" default). Without rule-level defense, any cleanup is temporary.

The milestone also folds in five unfinished v8.0 requirements (BRIDGE-01/02 for publish alignment, NLM-01/02/03 for NotebookLM auto-queries). These were originally independent quality gates; they are now absorbed into the refactored commands.

---

## Key findings

### Existing infrastructure (STACK)

Everything needed is already in Claude Code: subagent spawning via the Agent tool, the Skill tool for command invocation, AskUserQuestion for mid-flow checkpoints, Glob/Grep for cheap discovery, and the `.planning/` GSD workflow for milestone tracking. The memory system at `C:\Users\Benoi\.claude\projects\D--History-vs-Hype\memory\` already carries the user's architectural preference (`feedback-workflow-architecture.md`, saved 2026-04-21) so it persists across sessions. No new frameworks, no new Python dependencies, no new MCPs — this milestone adds zero surface area outside the workspace itself.

The biggest untapped leverage point is the gap between what Claude Code CAN do (isolated sub-agent contexts, option-based AskUserQuestion, disk-as-state) and what the current commands actually do (read everything in main, long freeform user elicitation, keep state in conversation). v9.0 is largely about changing habits, not adding capability.

### Features (7 categories)

Grouped by user-stated preference. Each has table-stakes, differentiators, and anti-features.

1. **Agent Delegation** — the foundation. Refactor the 4 heaviest commands to spawn agents for any read >500 lines. Standardize the return contract (≤200-word summary). Sequential fallback when rate-limited.
2. **Command Consolidation** — merge analytics commands (4→1 with flags), discovery commands, delete deprecated, audit `/help`.
3. **Reference Consolidation** — fix 10 dead refs, resolve STYLE-GUIDE vs VOICE-PROFILE contradiction, merge scriptwriting ref trio to one file, merge hook ref duo to one file. Regenerate INDEX.md.
4. **Python Tool Triage** — dependency graph first, then delete dead files, dedupe duplicates, move test_*.py out of production dirs, audit standalone sub-apps.
5. **Conversational Flow** — every heavy command inserts ≥1 AskUserQuestion checkpoint at a key decision. Option-based (3-4 options), not freeform. First option = recommended path. Post-command 3-line summary.
6. **Quality Gates (v8.0 carry-over)** — BRIDGE-01/02 (title+thumb+hook alignment test in /publish), NLM-01/02/03 (NotebookLM auto-queries in /script, /greenlight, prose critique). Every gate output must include a concrete next-step fix, not just a flag.
7. **Token-Saving Measures** — frontmatter token budget declarations, the `.claude/AGENT-ORCHESTRATION.md` reference, rate-limit resilience pattern, per-agent token measurement in summaries.

**Ballpark effort:** 16 phase-days, ~4-6 weeks at 1 phase-day per work-day.

### Architecture approach

Main context is the orchestrator: routes intent, talks to user via AskUserQuestion, holds state (step, answers, last agent ID). Sub-agents carry heavy reads and reasoning. Every heavy command follows the same shape: main parses → AskUserQuestion checkpoint → spawn agent (with `<files_to_read>` block + return contract) → main reads summary → optional second checkpoint → post-command 3-line summary.

Reference loading is tiered: Tier 0 (CLAUDE.md, always present), Tier 1 (command-specific top refs loaded by main, max 1-2), Tier 2 (agent-scoped refs, never touching main), Tier 3 (Grep lookup instead of Read). This is the mechanism by which the 35→~15 ref consolidation pays off: fewer files × fewer loaders × smaller files = compounding savings.

Build order: Phase 73 Foundation (write `.claude/AGENT-ORCHESTRATION.md` — the rules doc every later phase cites) → Phase 74 Reference Consolidation → Phase 75 Command Delegation Refactor (4 heaviest commands) → Phase 76 Command Consolidation → Phase 77 Quality Gates (v8.0 carry-over) → Phase 78 Python Tool Triage → Phase 79 Token-Saving Instrumentation.

### Critical pitfalls

1. **Regression by accretion** — root cause of v1.0 Phase 05 failure. Prevention: codify "extend, don't add" in `.claude/AGENT-ORCHESTRATION.md`, add monthly surface-area check.
2. **Refactor in main context** — the milestone embarrassing its own goal. Prevention: every phase spawns agents for any scan >3 files; sequential over parallel. Direct evidence: this session hit rate limit running 4 parallel research agents.
3. **Consolidation without content audit** — concatenation instead of synthesis. Prevention: merged ref must be ~70% of total length; contradictions resolved explicitly.
4. **Deletion without dependency graph (Python)** — prompt-embedded references to deleted files. Prevention: dependency graph covering imports + subprocess + `.claude/` mentions + Task Scheduler; soft-delete first (`_GRAVEYARD/`, 7-day quarantine).
5. **Agents that return everything** — return contract not enforced. Prevention: contract block codified once, referenced by every agent; summaries >300 words flagged as violations.
6. **Reference pre-loading by main** — old "prep main with everything it might need" pattern. Prevention: command file audit to move "Read X.md" instructions into agent `<files_to_read>` blocks.
7. **AskUserQuestion becoming a token hog** — long freeform elicitation. Prevention: option-based only, 3-4 options, ≤8 words each, first = recommended.
8. **Aggressive deletion of in-progress work** — 19 stalled `_IN_PRODUCTION/` projects at risk. Prevention: scope excludes `video-projects/`; soft-delete default; git is safety net.
9. **Merging commands that serve different mental models** — `/research` vs `/sources` are two workflow gates, not one discovery. Prevention: merge only same-stage same-intent commands; user consultation before any merge.
10. **Quality gates that aren't actionable** — flag without fix. Prevention: every gate output = verdict + gap + concrete next step. Gates without remediation don't ship.

**Meta-pitfall:** this milestone itself is exactly the kind of refactor work that burns main-context tokens fastest. Demonstrated in this very session (rate limit hit on parallel researcher spawn).

---

## Implications for roadmap

### Phase 73 — Foundation (XS-S, ~1 day)
**Rationale:** The rules doc every later phase cites. Without it, Phases 74-79 can't reference a standard.
**Delivers:** `.claude/AGENT-ORCHESTRATION.md` (spawning pattern, return contract, ref loading rules, extend-don't-add default, sequential-over-parallel rule).
**Addresses:** Pitfalls 1 (regression), 2 (refactor-in-main), 5 (return contract).

### Phase 74 — Reference Consolidation (L, ~2 days)
**Rationale:** Python triage later depends on some tools referencing docs — refs must be stable first. Fixes the audit's 10 dead refs + the STYLE-GUIDE contradiction.
**Delivers:** merged scriptwriting ref (one file from 5 overlapping), merged hook ref (one file from 2), fixed dead links, regenerated INDEX.md, "last used by" annotation pattern.
**Addresses:** Pitfall 3 (synthesis not concat), Pitfall 6 (kill pre-loading pattern in agent refs).

### Phase 75 — Command Delegation Refactor (M, ~2 days)
**Rationale:** Central value-delivery phase. The 4 heaviest commands (`/research`, `/script`, `/greenlight`, `/publish`) each get: agent-spawn audit, AskUserQuestion checkpoint placement, frontmatter token budget.
**Delivers:** refactored command files, agent prompts updated with return contract + `<files_to_read>` blocks.
**Addresses:** Pitfalls 5 (contract), 6 (pre-loading), 7 (checkpoints). Core of the user-facing change.

### Phase 76 — Command Consolidation (M, ~2 days)
**Rationale:** Independent of 75 but benefits from the same architectural rules. Analytics 4→1, discovery merge, delete deprecated.
**Delivers:** consolidated `/analyze` with flags, consolidated discovery command, removed `_DEPRECATED/`, updated `/help`.
**Addresses:** Pitfall 9 (user-consult before each merge), Pitfall 1 (surface area reduction).

### Phase 77 — Quality Gates (v8.0 carry-over) (M, ~3 days)
**Rationale:** Must happen after 75 because gates live inside refactored commands. Rolls in the 5 unfinished v8.0 requirements.
**Delivers:** BRIDGE-01/02 in `/publish`, NLM-01/02/03 in `/script` + `/greenlight` + prose critique path.
**Addresses:** Pitfall 10 (gates must produce actionable next steps, not just warnings). Every gate = verdict + gap + fix.

### Phase 78 — Python Tool Triage (M, ~3 days)
**Rationale:** Depends on Phase 74 (refs stable) so agent/command prompts referencing tools are accurate. Dependency graph precedes any deletion.
**Delivers:** dependency graph, deleted dead files, deduped duplicates, test_*.py moved out of production dirs, decision on history-clip-tool/.
**Addresses:** Pitfall 4 (dep graph + soft-delete).

### Phase 79 — Token-Saving Instrumentation (S, ~2 days)
**Rationale:** Hardening layer. Makes future regressions visible before they become problems.
**Delivers:** per-agent token measurement in summaries, per-command reference-load accounting, rate-limit resilience pattern codified in `.claude/AGENT-ORCHESTRATION.md`, monthly surface-area check (`/status --surface`).
**Addresses:** Pitfall 1 (regression defense), Pitfall 2 (rate-limit resilience), meta-pitfall.

### Research flags

- **Phase 75 — token budget per command:** needs empirical measurement of current token consumption before setting targets. First refactor should instrument, not prescribe, the budget.
- **Phase 77 — BRIDGE-01 alignment scoring:** the detection algorithm (does the title promise match the hook payoff?) may require a small Claude-based classifier, not pure heuristics. Needs a short research spike in the planning step.

Phases with standard patterns (skip research spike):
- Phase 73 — rules doc, pure writing.
- Phase 74 — consolidation is well-understood; content audit + resolve contradictions.
- Phase 76 — command merges follow established patterns.
- Phase 78 — dep graph is standard static analysis + prompt-text grep.
- Phase 79 — instrumentation is thin wrappers, no novel design.

---

## Confidence assessment

| Area | Confidence | Basis |
|---|---|---|
| Stack | HIGH | Fully inventoried in STACK.md; zero new dependencies |
| Agent-delegation savings | HIGH | Claude Code primitive; proven in gsd-* flow |
| Reference consolidation is safe | HIGH | Overlaps visible in file names; audit found 10 dead refs |
| Command consolidation won't hurt discoverability | MEDIUM | Requires `/help` update + aliases; user consult before each merge |
| Python triage is safe with dep graph | MEDIUM | Dynamic invocations require prompt-text grep too |
| AskUserQuestion checkpoints improve UX | HIGH | User explicitly stated preference 2026-04-21 |
| Quality gates (v8.0 carry-over) ship on schedule | MEDIUM | Depends on Phase 75 refactor landing first |
| Cleanup will hold post-v9.0 | MEDIUM | Depends on rules being codified + surface-area check actually running |

**Overall confidence:** HIGH on the direction; MEDIUM on execution because the milestone itself is token-heavy work that must be disciplined agent-first.

### Gaps to address during planning

- Empirical token baseline per heavy command (measure before refactoring — needed for Phase 75 frontmatter budgets).
- BRIDGE-01 detection algorithm (heuristic vs LLM classifier — short spike in Phase 77 planning).
- Dependency graph tool choice (static analyzer vs custom script — decided in Phase 78 planning).
- Surface-area check output shape (`/status --surface` detail — decided in Phase 79 planning).

---

## Sources

- **Codebase observation (this session):** `.planning/PROJECT.md`, `.planning/STATE.md`, `.planning/REQUIREMENTS.md` (v8.0 unfinished items), `.claude/commands/` listing (25 files), `.claude/agents/` listing (9 files), `.claude/REFERENCE/` listing (35 files).
- **Memory:** `C:\Users\Benoi\.claude\projects\D--History-vs-Hype\memory\feedback-workflow-architecture.md` (user's architectural preference, saved 2026-04-21).
- **Prior workflow audit:** 2026-04-14 audit findings (10 dead refs, 1 contradiction, 3 missing quality gates) — referenced throughout FEATURES.md.
- **Direct session evidence:** rate limit on 4 parallel research agents (2026-04-21) — feeds Pitfall 2 and the Meta-Pitfall.
- **Claude Code primitives:** Agent tool, Skill tool, AskUserQuestion tool, Glob, Grep — all native, documented in STACK.md.

---

*Research completed 2026-04-21. Ready for REQUIREMENTS phase.*
