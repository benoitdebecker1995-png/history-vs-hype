# ARCHITECTURE — v9.0 Lean Agent-Orchestrated Workflow

**Researched:** 2026-04-21
**Domain:** Refactoring the existing command/agent/reference/tool surface so the main context stays lean (orchestrator only), sub-agents carry heavy reads and reasoning, and the user experience becomes conversational rather than silent-autopilot.

---

## 1. Orchestrator vs. Sub-Agent Responsibility Split

The core architectural principle of v9.0: **the main context is an orchestrator**, not a worker. Every heavy read, reasoning chain, or reference aggregation belongs inside a sub-agent whose context never returns to main — only a ≤200-word summary does.

| Responsibility | Owner | Why |
|---|---|---|
| Route user intent → pick command/skill | Main (orchestrator) | Needs full conversation state |
| Ask user for mid-flow decisions (AskUserQuestion) | Main | Only main talks to user |
| Hold orchestrator state (step, user answers, last agent ID) | Main | Single source of truth for the command run |
| Read >500 lines of reference/source files | Sub-agent | Isolation keeps those tokens out of main |
| Multi-step reasoning (>3 logical steps) | Sub-agent | Same reason |
| Write large structured outputs (roadmap, research docs, script drafts) | Sub-agent (writes to disk) | Main reads only what it needs |
| Query NotebookLM or Context7 MCP | Sub-agent | Responses can be large |
| Score titles / hooks / thumbnails | Python tool called by main | Bounded output (<50 tokens) |
| Load reference files for style compliance | Sub-agent only | Agents own the reference cache |
| Detect & recover from rate limits | Main | Must decide sequential fallback |

**Anti-pattern:** main context reads STYLE-GUIDE + VOICE-PROFILE + creator-techniques + hook templates (~10k tokens) to "check" something. Correct pattern: spawn a style-check sub-agent with `<files_to_read>` block, ask for ≤200-word verdict.

---

## 2. Reference Loading Strategy

Reference files (`.claude/REFERENCE/*.md`, 35 files) are the single biggest source of repeated context load. v9.0 rule:

| Tier | Who loads it | How |
|---|---|---|
| Tier 0 — `CLAUDE.md` | Every session (automatic) | System-loaded, always present. Must stay tight. |
| Tier 1 — Command-specific top refs | Main, only when command runs | e.g. `/script` loads `STYLE-GUIDE.md` inline. Max 1-2 per command. |
| Tier 2 — Agent-scoped refs | Sub-agent only | Listed in agent prompt's `<files_to_read>` block. Never touches main. |
| Tier 3 — On-demand lookup | Main via Grep, not Read | "What does STYLE-GUIDE say about X?" → Grep the one line. |

**Rule:** if two refs overlap >40%, merge them. Measured overlaps to resolve (from FEATURES.md):
- STYLE-GUIDE + VOICE-PROFILE + creator-techniques → one authoritative Script Voice doc
- OPENING-HOOK-TEMPLATES + HOOK-PATTERN-LIBRARY → one Hook Patterns doc

---

## 3. Conversation State Flow (per command)

```
USER INVOKES /command
    │
    ▼
MAIN (orchestrator)
  ├─ Parse args + load command file (Tier 1 ref only)
  ├─ [Optional] AskUserQuestion checkpoint #1 — clarify intent
  │
  ├─► SPAWN AGENT A (heavy read / analysis)
  │     ├─ Agent loads Tier 2 refs
  │     ├─ Agent reads source files (video project dir, script draft, etc.)
  │     ├─ Agent writes result to disk (e.g. DRAFT.md)
  │     └─ Agent returns ≤200-word summary to main
  │
  ├─ Main reads summary (NOT the full output)
  ├─ [Optional] AskUserQuestion checkpoint #2 — confirm before costly next step
  │
  ├─► SPAWN AGENT B (conditional on user answer)
  │     └─ Returns summary
  │
  ├─ Main reads only top-N lines of Agent B output if needed (offset + limit)
  └─ Post-command summary (3 lines): "done X, next is Y, file at Z"
```

**Checkpoint placement rule:** one AskUserQuestion minimum per heavy command, placed BEFORE the most expensive action (spawning >2 agents, writing a full script, publishing, etc.).

---

## 4. Sub-Agent Return Contract

Every agent prompt must end with this contract (copy-paste):

```
RETURN CONTRACT
- Write all substantive output to disk at [exact path]
- Return to main context: ≤200 words with (a) 1-line verdict, (b) file path written, (c) top-3 findings, (d) any blocker/flag
- Do NOT return full content, quotes, or raw data — main will Read the file if needed
- If you cannot complete: return the blocker in ≤50 words + exact next step
```

This is codified once in `.claude/AGENT-ORCHESTRATION.md` (new file, v9.0 deliverable) and referenced by each agent.

---

## 5. Integration Points (where v9.0 changes land)

| Touchpoint | Current State | v9.0 Change |
|---|---|---|
| `.claude/commands/*.md` (25 files) | Mix of declarative + inline reads | Each heavy command adds: agent spawn list, AskUserQuestion checkpoint positions, token budget declaration in frontmatter |
| `.claude/agents/*.md` (9 files) | Varied prompt styles | Standardize return contract + `<files_to_read>` block across all |
| `.claude/REFERENCE/*.md` (35 files) | Overlap + dead refs | Consolidate to ~15; add INDEX.md regeneration |
| `tools/*.py` (~100 files) | Many unused | Dependency-graph → delete dead + dedupe |
| `.claude/AGENT-ORCHESTRATION.md` | Does not exist | NEW — codifies spawning pattern, return contract, ref loading rules |
| `.claude/USER-PREFERENCES.md` | Exists | Add section: "Main context = orchestrator only" |
| Memory (`feedback-workflow-architecture.md`) | Created 2026-04-21 | Keep — drives all future sessions |

---

## 6. Build Order (phase dependencies)

Phase numbering continues from v8.0 (last phase was 72). v9.0 begins at Phase 73.

1. **Phase 73 — Foundation**: Write `.claude/AGENT-ORCHESTRATION.md`. Codify spawning pattern, return contract, ref loading rules. This is the reference every other phase cites. (XS-S)
2. **Phase 74 — Reference Consolidation**: Merge overlapping refs (STYLE-GUIDE trio, hook trio). Fix 10 dead refs. Regenerate INDEX.md. Must happen before Python triage because some tools reference docs. (L)
3. **Phase 75 — Command Delegation Refactor**: Refactor the 4 heaviest commands (`/research`, `/script`, `/greenlight`, `/publish`) to spawn agents for any read >500 lines. Add AskUserQuestion checkpoints. Add frontmatter token budgets. (M)
4. **Phase 76 — Command Consolidation**: Merge analytics commands (`/analyze` + `/deep-analytics` + `/patterns` + `/growth` → `/analyze` with flags). Merge discovery commands. Delete deprecated. (M)
5. **Phase 77 — Quality Gates (v8.0 carry-over)**: BRIDGE-01/02 (publish alignment test), NLM-01/02/03 (NotebookLM auto-queries in /script, /greenlight, prose critique). Depends on Phase 75 — gates live inside refactored commands. (M)
6. **Phase 78 — Python Tool Triage**: Dependency graph, delete dead, dedupe duplicates, move test_*.py out of production dirs, audit history-clip-tool/. (M)
7. **Phase 79 — Token-Saving Instrumentation**: Per-agent token measurement in summaries, reference-load accounting per command, rate-limit resilience pattern. Codified into each command's frontmatter. (S)

Phases 73-77 are the critical path (user value). Phases 78-79 are hardening.

---

## 7. Data Flow Examples

### Example A: `/script` (heavy command, typical v9.0 shape)

```
User: /script 36-bakassi-peninsula-2026

MAIN
  ├─ Read .claude/commands/script.md (Tier 1)
  ├─ Glob video-projects/_IN_PRODUCTION/36-*/  → confirm folder
  ├─ AskUserQuestion: "Which script mode?" (new / revise / hook-variants)
  │     ↳ User: new
  │
  ├─► AGENT script-writer-v2
  │     <files_to_read>
  │       video-projects/.../01-VERIFIED-RESEARCH.md
  │       .claude/REFERENCE/STYLE-GUIDE.md
  │       .claude/REFERENCE/HOOK-PATTERNS.md  (consolidated in Phase 74)
  │     </files_to_read>
  │     Writes: video-projects/.../02-SCRIPT-DRAFT.md
  │     Returns: "Draft done. 11:40 est. Hook variant: myth-bust. Turn at 18%. 3 flags: [list]"
  │
  ├─ Main reads the 3 flagged lines via Grep (not full file)
  ├─ AskUserQuestion: "Run NLM competitor structure check?" (default yes per NLM-01)
  │     ↳ User: yes
  │
  ├─► AGENT notebooklm-query (NLM-01 gate)
  │     Returns: "3 structural divergences flagged. See [file]."
  │
  └─ Post-command: "Draft at 02-SCRIPT-DRAFT.md. Next: /verify."
```

Main context cost: command file (~3k) + 3 agent summaries (~600) + user answers (~200) = **~4k tokens**.
Old flow (main reads research + style guide + hook templates + writes draft inline): ~25-35k tokens.
**Savings: ~85%.**

### Example B: `/greenlight` (with NLM-02 gate)

```
User: /greenlight "France's Haiti debt"

MAIN
  ├─ Read .claude/commands/greenlight.md
  ├─ AskUserQuestion: "Full greenlight (demand + titles + thumbs + NLM check)?"
  │
  ├─► AGENT demand-checker (VidIQ + niche data) → returns verdict
  ├─► AGENT title-generator (gets titles + title_scorer.py output) → returns top-5
  ├─► AGENT notebooklm-query NLM-02 → competitor title pattern match → verdict
  │
  ├─ If any gate FAILS: AskUserQuestion: "Fail on X. Proceed, iterate, or kill?"
  └─ Post-command: verdict + files + next step
```

---

## 8. What NOT to build (architectural guardrails)

| Temptation | Why not |
|---|---|
| A single "/do-everything" command | Violates conversational principle — user-directed checkpoints are the design |
| A background agent manager / pool | Over-engineering for solo creator; Claude Code's native Agent tool is enough |
| A new config DSL for routing | Markdown + frontmatter already works |
| An LLM-based router that picks agents automatically | Adds a meta-layer that defeats the token savings |
| Backwards-compat shims for deleted commands | Git history preserves; users re-learn names |
| Replacing Python tools with agent prompts wholesale | Too risky for one milestone — triage, don't rewrite |

---

## 9. Confidence

| Area | Confidence | Basis |
|---|---|---|
| Orchestrator/agent split saves tokens | HIGH | Claude Code primitive; observed in gsd-* flow |
| Reference consolidation is net-positive | HIGH | Overlap is visible in filenames; audit found 10 dead refs |
| Command consolidation won't hurt discoverability | MEDIUM | Aliases + /help update required |
| Python triage is safe with dep graph | MEDIUM | 100+ files; some imports-of-imports |
| AskUserQuestion checkpoints improve UX | HIGH | User explicitly stated preference 2026-04-21 |
| NLM auto-queries actually fire reliably | MEDIUM | MCP server integration, fallback to paste-prompt required |

---

*Researched 2026-04-21 inline (rate limit on parallel agents — see PITFALLS Meta-Pitfall).*
