# Requirements: History vs Hype Workspace

**Defined:** 2026-04-14 (v8.0) | **Updated:** 2026-04-21 (v9.0)
**Core Value:** Every video shows sources on screen — viewers see the evidence themselves

---

## v9.0 Requirements — Lean Agent-Orchestrated Workflow

**Milestone goal:** Main context = orchestrator only. Heavy reads + reasoning delegated to sub-agents. Conversational flow via AskUserQuestion checkpoints. Aggressive deletion with soft-delete safety net. Rules codified so the lean state survives past v9.0.

**Output metric:** Every change must answer "does this improve retention, CTR, or script quality?" If unclear — cut.

---

### Category 1 — Agent Delegation (foundation)

- [ ] **AGENT-01**: Create `.claude/AGENT-ORCHESTRATION.md` codifying: when to spawn, the sub-agent return contract (≤200-word summary, write to disk, no raw quotes), reference-loading tiers, sequential-over-parallel rate-limit rule
- [ ] **AGENT-02**: Refactor `/research` command so any read >500 lines or reasoning >3 steps spawns a sub-agent; main reads only the returned summary
- [ ] **AGENT-03**: Refactor `/script` command with same rule — script generation, structure check, and reference loading all run inside sub-agents
- [ ] **AGENT-04**: Refactor `/greenlight` command with same rule — demand check, title gen, thumbnail eval all run inside sub-agents
- [ ] **AGENT-05**: Refactor `/publish` command with same rule — metadata gen, gate checks, NLM queries all run inside sub-agents
- [ ] **AGENT-06**: Standardize return contract across all 9 existing agents in `.claude/agents/*.md` — every agent ends with the contract block from AGENT-01
- [ ] **AGENT-07**: Rate-limit resilience — detect 429 / rate-exceeded, serialize agent spawning, retry sequentially instead of failing

### Category 2 — Command Consolidation

- [ ] **CMD-01**: Merge analytics commands (`/analyze` + `/deep-analytics` + `/patterns` + `/growth`) into one `/analyze` with flags (--deep, --patterns, --growth)
- [ ] **CMD-02**: Merge discovery commands — decide single entry point from `/research` + `/sources` + `/discover`. AskUserQuestion before merge to preserve workflow gates
- [ ] **CMD-03**: Delete all commands in `.claude/commands/_DEPRECATED/` (soft-delete to `_GRAVEYARD/` first, 7-day quarantine)
- [ ] **CMD-04**: Audit `/help` output — ensure it lists only real, current commands. Remove references to deleted/merged commands. Add aliases for merged ones

### Category 3 — Reference Consolidation

- [ ] **REF-01**: Fix the 10 dead references identified in 2026-04-14 audit
- [ ] **REF-02**: Resolve STYLE-GUIDE vs VOICE-PROFILE contradiction on "It's important to note that..." — decide canonical rule, state in the merged doc
- [ ] **REF-03**: Merge scriptwriting reference trio (STYLE-GUIDE + VOICE-PROFILE + creator-techniques + SCRIPTWRITING-EXAMPLES + SCRIPTWRITING-DEBUNKING-FRAMEWORK) into ≤2 authoritative files. Merge is synthesis, not concatenation (target: ~70% of total length)
- [ ] **REF-04**: Merge hook reference duo (OPENING-HOOK-TEMPLATES + HOOK-PATTERN-LIBRARY) into one file
- [ ] **REF-05**: Regenerate `.claude/REFERENCE/INDEX.md` from actual file list post-consolidation

### Category 4 — Python Tool Triage

- [ ] **PY-01**: Build dependency graph covering Python imports + subprocess calls + `.claude/` prompt mentions + Task Scheduler entries before any deletion
- [ ] **PY-02**: Delete dead Python files (zero callers across imports, subprocess, prompts, tasks) via soft-delete to `_GRAVEYARD/`, 7-day quarantine, then hard-delete
- [ ] **PY-03**: Identify and consolidate duplicated tools (multiple dashboards, multiple title scorers) — pick one per function, delete the rest
- [ ] **PY-04**: Move `test_*.py` files out of production directories into `tests/`
- [ ] **PY-05**: Decide fate of `tools/history-clip-tool/` — keep, consolidate, or delete (requires separate FastAPI app audit)

### Category 5 — Conversational Flow

- [ ] **FLOW-01**: Every heavy command (`/research`, `/script`, `/publish`, `/greenlight`) inserts ≥1 AskUserQuestion checkpoint at a key decision point BEFORE any expensive action (>2 parallel agents, full script write, publish)
- [ ] **FLOW-02**: Checkpoint questions use option lists (3-4 options, each ≤8 words), not freeform elicitation
- [ ] **FLOW-03**: First option of every AskUserQuestion is the recommended/default path (aligns with existing memory rule)
- [ ] **FLOW-04**: Every command ends with a 3-line post-command summary: what was done, where the output is, what's next
- [ ] **FLOW-05**: Checkpoint positions documented in each refactored command's file (so agents/future-self can find them)

### Category 6 — Quality Gates (v8.0 carry-over)

- [ ] **BRIDGE-01**: During `/publish`, auto-run bridge test scoring title + thumbnail concept against script's first 30 seconds (hook alignment). Output = verdict + specific gap + concrete fix (not just a flag)
- [ ] **BRIDGE-02**: Bridge test flags WEAK alignments (title promises X, hook delivers Y) with actionable remediation text
- [ ] **NLM-01**: After `/script` generation, auto-query Competitor notebook via NotebookLM MCP for structure comparison (hook pattern, turn placement, evidence pacing, closing). Falls back to ready-to-paste prompt if MCP unavailable
- [ ] **NLM-02**: During `/greenlight` title evaluation, auto-query Competitor notebook via MCP for title pattern match against outlier patterns. Falls back to paste prompt
- [ ] **NLM-03**: For high-stakes videos (user-flagged or ideological topics), auto-query Article Workshop notebook via MCP for prose critique. Falls back to paste prompt

### Category 7 — Token-Saving Measures

- [ ] **TOK-01**: Every refactored command's frontmatter declares: expected main-context token budget, agent spawn count, fallback behavior
- [ ] **TOK-02**: Per-agent token measurement in summaries — each agent reports its own token usage so patterns emerge over time
- [ ] **TOK-03**: Monthly surface-area check via `/status --surface` — reports command count, ref count, Python file count, agent count against v9.0 baseline (regression-by-accretion defense)
- [ ] **TOK-04**: Reference-load accounting per command — doc lists which refs load at main level vs agent level, so duplication stays visible

---

## Out of Scope (explicitly cut from v9.0)

| Feature | Reason |
|---|---|
| `video-projects/` folder cleanup | Out of scope — risky to delete stalled projects that may revive |
| Universal `/do` meta-command | Fights conversational principle |
| Agent pool manager / queue | Over-engineering for solo creator |
| LLM-based agent routing | Adds meta-layer, defeats token savings |
| New reference doc categories | Consolidate before creating anything new |
| Backwards-compat shims for deleted commands | Git history preserves |
| Full Python rewrite as agent prompts | Too risky for one milestone — triage only |
| Usage telemetry dashboard as separate app | Overkill for solo creator; folded into `/status --surface` if at all |
| Token-based circuit breakers that kill commands mid-flow | Breaks conversational flow |

---

## Traceability

| Requirement | Phase | Status |
|---|---|---|
| **v8.0 completed (carried from prior roadmap)** | | |
| GATE-01, GATE-02, STRUCT-01, STRUCT-02 | Phase 71 | Complete |
| FACT-01, FACT-02 | Phase 72 | Complete |
| **v9.0 new** | | |
| AGENT-01 | Phase 73 (Foundation) | Pending |
| REF-01 through REF-05 | Phase 74 (Ref Consolidation) | Pending |
| AGENT-02, AGENT-03, AGENT-04, AGENT-05, AGENT-06, AGENT-07 | Phase 75 (Command Delegation Refactor) | Pending |
| FLOW-01, FLOW-02, FLOW-03, FLOW-04, FLOW-05 | Phase 75 (same phase — checkpoints land during refactor) | Pending |
| TOK-01 | Phase 75 (frontmatter budgets added during refactor) | Pending |
| CMD-01, CMD-02, CMD-03, CMD-04 | Phase 76 (Command Consolidation) | Pending |
| BRIDGE-01, BRIDGE-02, NLM-01, NLM-02, NLM-03 | Phase 77 (Quality Gates — v8.0 carry-over) | Pending |
| PY-01, PY-02, PY-03, PY-04, PY-05 | Phase 78 (Python Tool Triage) | Pending |
| TOK-02, TOK-03, TOK-04 | Phase 79 (Token-Saving Instrumentation) | Pending |

**Coverage:**
- v9.0 requirements: 30 total
- Mapped to phases 73-79: 30
- Unmapped: 0

**v8.0 carry-over status:**
- Completed in v8.0: 6/11 (GATE + STRUCT + FACT)
- Rolled into v9.0 Phase 77: 5/11 (BRIDGE-01/02, NLM-01/02/03)

---

*Requirements last updated: 2026-04-21 for v9.0 milestone*
