# FEATURES — v9.0 Lean Agent-Orchestrated Workflow

**Researched:** 2026-04-21
**Grouping:** 7 feature categories derived from user's stated preferences (more agents, lean main, conversational, cut waste, quality gates, better videos).

---

## 1. Agent Delegation

**Table stakes:**
- Refactor heaviest commands (`/research`, `/script`, `/greenlight`, `/publish`) to spawn agents for any read >500 lines or reasoning >3 steps (M) — foundational, nothing else works without this
- Return-contract standard in agent prompts: every agent instructed to write files directly + return ≤200-word summary (S) — depends on above
- Document the spawning pattern once in `.claude/AGENT-ORCHESTRATION.md` so future commands copy it (S)

**Differentiators:**
- Sequential-then-parallel fallback: if rate limit detected, retry sequentially instead of failing (S) — learns from this session's failure
- Agent chain discovery: detect when one agent's output = next agent's input, auto-link (M)
- Per-command token budget declaration in command frontmatter (XS) — "this command aims for <15k main-context tokens"

**Anti-features:**
- Auto-orchestrator that dispatches agents without user checkpoints — fights conversational principle
- Agent pool manager / queue — over-engineering for solo creator
- LLM-based agent routing — adds a meta-layer, defeats savings

---

## 2. Command Consolidation

**Table stakes:**
- Merge analytics commands: `/analyze` + `/deep-analytics` + `/patterns` + `/growth` → 1 command with flags (M)
- Merge discovery commands: `/research` + `/sources` + `/discover` → decide single entry point (M)
- Delete deprecated commands (anything in `.claude/commands/_DEPRECATED/`) (XS)
- Audit `/help` output: does it still list real commands? (XS)

**Differentiators:**
- Command usage telemetry: log which commands are actually invoked over 30 days, then cut anything <1 use/month (S)
- Aliases for merged commands (`/analyze deep` works where `/deep-analytics` used to) (S)

**Anti-features:**
- "Universal /do command" — fights discoverability
- Backwards-compatibility wrapper for every deleted command — git history is enough

---

## 3. Reference Consolidation

**Table stakes:**
- Fix 10 dead refs from 2026-04-14 audit (XS) — blocks nothing but cheap quick win
- Resolve STYLE-GUIDE vs VOICE-PROFILE contradiction on "It's important to note that..." (XS)
- Merge overlapping scriptwriting refs: STYLE-GUIDE + VOICE-PROFILE + creator-techniques + SCRIPTWRITING-EXAMPLES + SCRIPTWRITING-DEBUNKING-FRAMEWORK → 2 authoritative files max (L)
- Merge overlapping hook refs: OPENING-HOOK-TEMPLATES + HOOK-PATTERN-LIBRARY → 1 (S)

**Differentiators:**
- INDEX.md regenerated from actual file list (XS) — so agents have a fresh directory
- Per-reference "last used by" annotation so dead refs surface (S)

**Anti-features:**
- Splitting refs into ever-finer categories — goes the wrong direction
- Versioned refs (v1/v2/v3) — commit history is enough

---

## 4. Python Tool Triage

**Table stakes:**
- Find dead Python files (no imports anywhere in repo, never invoked by commands/agents) and delete (M)
- Find duplicated tools (e.g., multiple dashboards, multiple title scorers) and pick one (M)
- Remove `test_*.py` from production dirs (they belong in `tests/`) (S)
- Audit `tools/history-clip-tool/` — is this a separate FastAPI app? Still needed? (S)

**Differentiators:**
- Dependency graph generator: shows which tool imports which (M) — for safe deletion
- Tool manifest: every remaining tool documented with purpose, owner command, last touched (M)

**Anti-features:**
- Rewriting all Python tools as agent prompts — wholesale replacement is too risky for one milestone
- Moving all Python to a separate package — pyproject.toml already exists

---

## 5. Conversational Flow

**Table stakes:**
- Every heavy command (`/research`, `/script`, `/publish`, `/greenlight`) inserts ≥1 AskUserQuestion checkpoint at a key decision (M)
- Mid-flow checkpoints use option lists (3-4 options), not freeform elicitation (S) — tokens cheaper
- "Silent completion" becomes an error state — commands must check in at decision points (S)
- Checkpoint positions documented in each command file (XS)

**Differentiators:**
- "Confirm before costly step" pattern: AskUserQuestion before spawning >2 parallel agents (S)
- User-override default: AskUserQuestion's first option is always the recommended path (XS) — aligns with existing rule
- Post-command summary: 3-line "here's what was done, here's what's next" at end of every command (XS)

**Anti-features:**
- Interactive REPL inside commands — too much state
- Chatty confirmations for every trivial action — signal/noise

---

## 6. Quality Gates (v8.0 carry-over)

**Table stakes:**
- **BRIDGE-01**: During `/publish`, auto-run bridge test: title + thumbnail vs script first 30s alignment (M)
- **BRIDGE-02**: Bridge test flags WEAK alignments (title promises X, hook delivers Y) as warnings (S)
- **NLM-01**: After `/script` generation, auto-query Competitor notebook via NotebookLM MCP for structure comparison; fallback to ready-to-paste prompt (M)
- **NLM-02**: During `/greenlight` title evaluation, auto-query Competitor notebook for title pattern match; fallback to paste prompt (M)
- **NLM-03**: For high-stakes videos (user-flagged or ideological), auto-query Article Workshop notebook for prose critique; fallback to paste prompt (M)

**Differentiators:**
- Gate bypass logging: if user overrides a gate, note which video + reason (S) — catches workflow regressions
- Gate-failure surfacing in /status dashboard (XS)

**Anti-features:**
- Gates that can't be overridden — user knows context agent doesn't
- Gates without actionable next step — always tell user what to fix

---

## 7. Token-Saving Measures (Explicit)

**Table stakes:**
- Every command's frontmatter declares: expected main-context token budget, agent spawn count, fallback behavior (S)
- `.claude/AGENT-ORCHESTRATION.md` codifies: when to spawn, return contracts, reference loading rules (S)
- Rate-limit resilience pattern: detect 429 / rate-exceeded, serialize, retry (S) — learned from this session

**Differentiators:**
- Token measurement in agent summaries: each summary reports its own token usage so patterns emerge (M) — requires lightweight instrumentation
- Reference-load accounting: per command, list which refs get loaded (and by whom) so we see duplication (S)

**Anti-features:**
- Token-based circuit breakers that kill commands mid-flow — breaks conversational flow
- Usage dashboard as its own app — overkill for solo creator

---

## Complexity Summary

| Category | XS | S | M | L | Total effort est |
|---|---|---|---|---|---|
| 1. Agent Delegation | 1 | 2 | 1 | 0 | 2 phase days |
| 2. Command Consolidation | 1 | 1 | 2 | 0 | 2 days |
| 3. Reference Consolidation | 2 | 1 | 0 | 1 | 2 days |
| 4. Python Tool Triage | 0 | 1 | 3 | 0 | 3 days |
| 5. Conversational Flow | 2 | 3 | 1 | 0 | 2 days |
| 6. Quality Gates | 1 | 1 | 3 | 0 | 3 days |
| 7. Token-Saving Measures | 0 | 3 | 1 | 0 | 2 days |

**Ballpark:** 16 phase-days = ~4-6 weeks at 1 phase-day/work-day, depending on batching.

---

## Dependency Notes

- Category 1 (agent delegation) is foundational — everything else benefits from it, do first.
- Category 3 (reference consolidation) must precede Category 4's Python tool decisions where tools reference docs.
- Category 7 (token measures) should be wrapped into each phase's delivery, not a standalone phase.
- Category 6 (quality gates) is independent — can run in parallel with 1/2/3.

---

*Research written in main context on 2026-04-21 due to rate limit.*
