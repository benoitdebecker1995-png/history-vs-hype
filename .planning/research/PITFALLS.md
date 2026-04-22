# PITFALLS — v9.0 Lean Agent-Orchestrated Workflow

**Researched:** 2026-04-21
**Domain:** Refactoring an existing Claude Code workspace (25 commands, 9 agents, 35 refs, 100+ Python files) for lean main context, heavy agent delegation, conversational flow, aggressive deletion.

**Context:** Prior "simplification" milestone (v1.0 Phase 05) did not stick — surface area grew back. This milestone must address the REASON it didn't stick, not just repeat the cleanup.

---

## Executive summary

The dangerous failure mode for v9.0 is **regression by accretion**: finishing the milestone with a lean workspace, then watching it re-bloat over the next three months because the forces that caused bloat in the first place were never named or neutralized. The Python tool count, reference count, and command count grew organically between v1.0 and v9.0 because every new need was met by adding a file rather than extending an existing one. Without codified rules that redirect "add" pressure into "extend" or "consolidate" pressure, any cleanup is temporary.

The secondary risk is **token-heavy cleanup**: this milestone itself is the kind of workflow-refactor work that burns main-context tokens fastest (reading every command to refactor it, every reference to merge it, every Python tool to classify it). The milestone will embarrass its own goal if executed in main context instead of via agents.

---

## Refactor Pitfalls

### Pitfall 1 — Regression by Accretion (root cause of v1.0 Phase 05 failure)

**What goes wrong:** v9.0 ships clean, but three months later the workspace looks like it did in March 2026 — 35+ refs, 100+ Python files, overlapping commands. User adds a new need, adds a new file, nobody notices until the next audit.

**Why it happens:**
1. **Additive pressure** — every new requirement seems easier to satisfy with a new file than by extending an existing one.
2. **Reference doc accretion** — refs get written when a pattern is discovered, never pruned when that pattern consolidates.
3. **Python tooling growth** — a new scorer, a new fetcher, a new analyzer each feels like the right primitive, accruing as siblings.
4. **Command convenience additions** — "I need a shortcut for X" → new command instead of a flag on an existing one.

**Prevention (codify in `.claude/AGENT-ORCHESTRATION.md` and CLAUDE.md):**
- **Extend, don't add** as a default design rule: new needs get a flag on an existing command, a section in an existing ref, or a function in an existing tool before they get a new file.
- **Monthly surface-area check**: `/status --surface` shows command count, ref count, Python file count, agent count. Compare to v9.0 baseline.
- **Deletion as first-class work**: every phase should have at least one deletion target, not just additions.
- **Reference lifecycle tag**: each ref has a "last used by" annotation (Category 3 differentiator in FEATURES.md). Unused >60 days = deletion candidate.

**Warning signs:** Command count rising. New ref created with "notes" or "thoughts" in filename. Python file with no caller. Ref with 0 `.claude/` mentions outside its own file.

**Phase to address:** Phase 73 (Foundation) codifies the rules. Phase 79 (Token Instrumentation) adds the monthly surface-area check.

---

### Pitfall 2 — Refactor in Main Context (the milestone embarrasses its own goal)

**What goes wrong:** v9.0 executes with main context reading every command file, every reference, every Python tool to decide what to cut. Rate limits hit mid-milestone. User frustrated.

**Why it happens:** Refactor work feels like it requires "seeing everything at once." The natural impulse is to Read the whole file tree. But this is the exact pattern v9.0 exists to kill.

**Prevention:**
- Every phase MUST spawn a sub-agent for any scan of >3 files. Main reads only the agent's summary + the files the agent flags as requiring main-context decisions.
- Use Glob + Grep before Read. Cheap discovery beats expensive reading.
- Sequential agent spawning (not 4-parallel) — this session's rate limit failure is direct evidence.

**Warning sign:** A single main-context turn reads >10 files. Stop and delegate.

**Phase to address:** All phases. Codified in Phase 73 output.

---

### Pitfall 3 — Consolidation Without Content Audit

**What goes wrong:** STYLE-GUIDE + VOICE-PROFILE + creator-techniques get merged by concatenation. The new doc is 3× the length, contradictions remain, agents still load the whole thing.

**Why it happens:** Merging is easier than synthesizing. File-level merge (cat A B C > D) feels done.

**Prevention:**
- Consolidation = re-writing, not concatenation. A merged ref must be shorter than the sum of its parts (target: ~70% of total).
- Resolve contradictions explicitly (e.g., the known "It's important to note that..." disagreement between STYLE-GUIDE and VOICE-PROFILE) — don't leave both rules.
- Tier the merged doc: core rules up front, edge cases later, examples last. Agents that need rules don't load examples.

**Warning signs:** Merged ref longer than original total. Same rule stated twice with different words. "See [deleted file]" links.

**Phase to address:** Phase 74 (Reference Consolidation).

---

### Pitfall 4 — Deletion Without Dependency Graph (Python tooling)

**What goes wrong:** A "dead" Python file is deleted. A command or an agent breaks silently because the agent's prompt says `python tools/X.py` and X.py is gone.

**Why it happens:** Static dependency analysis misses dynamic invocations (subprocess calls, prompt-embedded commands, task scheduler entries).

**Prevention:**
- Before any Python deletion phase: build a dependency graph covering (a) Python `import` statements, (b) subprocess/os.system calls, (c) `.claude/` mentions in agent/command prompts, (d) scripts in `tasks/` or Windows Task Scheduler.
- Test: run every command in the test list after deletion. Silent failures = prompt-embedded reference to deleted file.
- Soft-delete first: move to `_GRAVEYARD/` directory for one week; hard-delete only if nothing broke.

**Phase to address:** Phase 78 (Python Tool Triage).

---

## Token / Context Pitfalls

### Pitfall 5 — Agents That Return Everything

**What goes wrong:** A sub-agent is spawned to "read the script draft and check style compliance." It returns the full script plus comments. Main context bloats as if the agent never ran.

**Why it happens:** Agent prompts don't enforce the return contract. Agents default to being "thorough" (verbose).

**Prevention:**
- Every agent prompt ends with the return contract block (ARCHITECTURE.md §4). ≤200 words. File path + verdict + top findings + blocker. No raw quotes.
- If main genuinely needs the content, agent writes it to disk; main Reads only the span needed (offset + limit).
- Orchestrator audit: any agent summary >300 words is a contract violation — fix the agent prompt.

**Phase to address:** Phase 73 (codify contract), Phase 75 (refactor 4 heavy commands' agents).

---

### Pitfall 6 — Reference Pre-Loading by Main

**What goes wrong:** A command file says "Read STYLE-GUIDE.md before running." Main reads it every invocation. 8k tokens × every /script call.

**Why it happens:** The old pattern was "prep main with everything it might need." v9.0 reverses this: main loads only the command file; agents load Tier-2 refs.

**Prevention:**
- Audit every command file for "Read X.md" instructions in main-context language. Move those into the agent's `<files_to_read>` block.
- Command files state: "Main reads only this file + user answers. Agents read refs."

**Phase to address:** Phase 75 (Command Delegation Refactor).

---

### Pitfall 7 — AskUserQuestion Becoming a Token Hog

**What goes wrong:** AskUserQuestion prompts become long freeform elicitations ("please describe in detail what you want to do, including X Y Z and any preferences about A B C"). The token savings from agent isolation get eaten by chatty prompts.

**Why it happens:** Writing clear options is harder than writing open questions.

**Prevention:**
- Option-based questions only (3-4 options, each ≤8 words).
- First option is always the recommended path (consistent with existing memory rule).
- Freeform allowed only when the answer space is truly unbounded (project name, paste content).
- Skip the question entirely when the default can be safely inferred.

**Phase to address:** Phase 75 — each refactored command has its checkpoint positions + option lists documented.

---

## Deletion Pitfalls

### Pitfall 8 — Aggressive Deletion of In-Progress Work

**What goes wrong:** 19 projects in `video-projects/_IN_PRODUCTION/`. Triage deletes "old" ones. User realizes one was about to be revived.

**Why it happens:** "In production" as a folder name loses signal when half the folder is stalled.

**Prevention:**
- Python tool / ref deletion is in scope for v9.0. `video-projects/` content is NOT — out of scope.
- Any workflow-level file deletion is soft-delete first (`_GRAVEYARD/`, 7-day quarantine).
- Git history is the real safety net — every deletion is one commit, easy to revert.

**Phase to address:** All phases — apply soft-delete as the default.

---

### Pitfall 9 — Merging Commands That Serve Different Mental Models

**What goes wrong:** `/research` and `/sources` are merged because "both are discovery." But `/research` is Phase 1 (landscape) and `/sources` is Phase 2 (academic verification). User loses the mental gate between them; NotebookLM Phase 2 gets skipped.

**Why it happens:** File-level similarity (both about finding things) masks workflow-level distinction (gate between them).

**Prevention:**
- Merge only commands that serve the same user intent at the same workflow stage.
- If two commands share files or flags but represent different workflow gates, keep them separate or merge with explicit mode flags that preserve the gate.
- User consultation before any command merge (AskUserQuestion in Phase 76).

**Phase to address:** Phase 76 (Command Consolidation).

---

### Pitfall 10 — Quality Gates That Aren't Actionable

**What goes wrong:** BRIDGE-01 (title/thumb/hook alignment) flags "weak alignment" but gives no direction. User is told they failed the gate with no fix in hand. User overrides; next time the gate fires, they skip reading the warning.

**Why it happens:** Detection is cheaper to build than remediation. Gates ship with the "flag" step but not the "here's how to fix" step.

**Prevention:**
- Every gate output = verdict + specific gap + concrete next step. "Title promises 'exposed' but hook delivers 'academic overview' → rewrite hook first 10s to include the reveal the title promises. See HOOK-PATTERNS.md §3."
- Gates that can't produce a concrete next step are not ready to ship — ship without the gate, don't ship a noisy gate.

**Phase to address:** Phase 77 (Quality Gates v8.0 carry-over).

---

## Meta-Pitfall: This Milestone Itself

**Direct evidence from this session:** 4 parallel `gsd-project-researcher` agents spawned in this very session ALL hit rate limits. The fallback was to write research files in main context — the exact thing v9.0 exists to prevent.

**Root causes observed in this session:**
1. Parallel agent spawning on a rate-limited account — lesson: default to sequential, detect 429, serialize.
2. Main context doing work agents should have done — lesson: spawn first, main reads summary.
3. Missing rate-limit resilience in orchestrator — lesson: Phase 79's Rate-Limit Resilience deliverable is not optional.

**Preventions for the milestone execution:**
- Every v9.0 phase uses sequential agent spawning by default. Parallel only when the user explicitly OKs it AND the phase says "independent, non-competing agents."
- Every phase's PLAN.md has a "token budget" line (e.g., "main context <15k tokens through plan") and a rate-limit fallback.
- If a v9.0 phase finds itself reading >10 files in main, stop and re-plan.

---

## The One Overriding Risk

**Root risk:** The milestone achieves the clean state and then doesn't hold it.

v1.0 Phase 05 "workflow-simplification" happened. The repo was cleaned. 15 months later, 35 refs + 100+ Python files. Simplification didn't stick because **no rules kept it simple**.

v9.0 must ship (a) the clean state AND (b) the rules that keep it clean — codified in `.claude/AGENT-ORCHESTRATION.md`, enforced by the monthly surface-area check, defended by the "extend, don't add" default.

If Phase 73 (Foundation) is rushed — if the rules are vague, not codified, or not referenced by later phases — the entire milestone is a short-term win and a long-term repeat.

---

*Researched 2026-04-21 in main context due to rate limit — the meta-pitfall demonstrated itself.*
