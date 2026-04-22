# STACK — v9.0 Lean Agent-Orchestrated Workflow

**Researched:** 2026-04-21 (inline, due to rate limit on parallel agents — see Pitfalls)
**Milestone focus:** refactor existing workspace for lean main context + heavy agent delegation + conversational flow + aggressive deletion

---

## Existing Infrastructure to Leverage

| Capability | Where | How it supports v9.0 |
|---|---|---|
| **Subagent spawning** (Agent tool) | Claude Code native | Sub-agents get isolated context; only summary returns to main. Core to token savings. |
| **Skill tool** | Claude Code native | Commands invoke as Skills — discoverable, gated, own context. Already used by /script, /research, etc. |
| **AskUserQuestion tool** | Claude Code native | Mid-flow user checkpoints; option-based = short tokens vs freeform. Core to "conversational". |
| **Glob + Grep** | Claude Code native | Cheap file discovery without reading; use before Read. |
| **SlashCommand / command files** | `.claude/commands/*.md` (25 files) | Declarative command definitions already live here. Refactor in place, no new infra. |
| **Agent definitions** | `.claude/agents/*.md` (9 files) | Declarative agent prompts. Can be consolidated, updated, added to. |
| **Reference files** | `.claude/REFERENCE/*.md` (35 files) | Prompt context for agents. Candidates for consolidation and dead-link cleanup. |
| **.planning/ GSD workflow** | existing | v1.0–v8.0 tracked here. This milestone uses same pattern. |
| **Memory system** | `C:\Users\Benoi\.claude\projects\D--History-vs-Hype\memory\` | Feedback rules persist across sessions. New rule saved 2026-04-21 for agent-orchestrated preference. |
| **Python tool registry** | `tools/` (~100 Python files, ~48K LOC) | Heavy surface area. Triage candidate. |

---

## Patterns for Agent Delegation (proven vs new)

| Pattern | Status | When to use | Token savings |
|---|---|---|---|
| Spawn agent with `<files_to_read>` list and require it to return ≤200-word summary | Proven in gsd-* agents | Any task that needs to read >2 files or >500 lines | ~80% (full content stays in agent) |
| Spawn agent to Write to disk, main reads only top-N results | Proven in gsd-roadmapper, research-synthesizer | Large structured outputs (roadmap, research) | ~70% |
| Chain agents where output of one = input file path for next | Proven in gsd-new-project flow | Multi-stage pipelines like research → synthesize → plan | Linear, no duplication |
| Sequential agent spawn (NOT parallel) when rate limits are tight | New rule — this session | Any time user hits caps, fallback to serial | Lower burst, same total |
| Main context holds **only** orchestrator state: current step, user answers, last agent ID | Partially observed | Every command should follow this discipline | Hard to quantify, prevents bloat |

---

## Token-Saving Techniques Available

1. **Agent isolation** — sub-agent context doesn't come back to main. This is the biggest lever. Every heavy read (>500 lines) should go here.
2. **Skill-local context** — Skills define their own context block. Scoped reads happen inside the skill, not in main.
3. **Glob before Read** — cheap discovery, then read only the specific file needed.
4. **AskUserQuestion option-based** — option labels are tokens-cheap vs elicitation paragraphs.
5. **Return contracts** — agents told to return ≤200 words produce summaries, not full content.
6. **Reference file consolidation** — when 3 files overlap, agents load 3 × context; merge → 1 × context.
7. **Command consolidation** — overlapping commands double-read refs; one command = one read.
8. **Python tool retirement** — every tool file deleted = zero load cost forever.

---

## What NOT to Add

| Temptation | Why not |
|---|---|
| A new LLM proxy layer (e.g., wrapper around Claude for "cost tracking") | Claude Code already handles this. Adding a layer adds context. |
| A configuration DSL for command/agent routing | YAML/JSON adds parse steps. Markdown + frontmatter already works. |
| A meta-orchestrator command ("/run-all", "/do-everything") | Fights the conversational principle. User-directed checkpoints are the design. |
| A new Python framework (e.g., LangChain, LangGraph) | Duplicates what Claude Code already offers. Adds surface area. |
| New reference doc categories | Consolidate first. Adding before cutting = net-negative. |
| Backwards-compat shims for deleted commands | Git keeps history. Users won't notice things that are gone. |
| Auto-spawning background agents without checkpoints | Violates conversational principle. No silent autopilot. |

---

## Integration Notes

- **Existing commands**: Every command file can be refactored in place. No new directory.
- **Existing agents**: Can be updated in their `.md` files. Can add new ones. Can delete unused ones.
- **Existing Python tools**: Can be deleted freely — git history preserves. Tools imported by other tools need dependency check before delete.
- **Existing references**: Merge targets: STYLE-GUIDE.md + VOICE-PROFILE.md + creator-techniques.md overlap; OPENING-HOOK-TEMPLATES.md + HOOK-PATTERN-LIBRARY.md overlap.
- **Preserve**: `.planning/` directory structure (GSD workflow), `video-projects/` folder structure (lifecycle), `memory/` (user feedback persistence).

---

## Open Questions for User Input During Requirements

- Which 5-8 core commands are sacred (never touched)? → influences aggressive deletion boundaries
- Are there any Python tools the user runs manually (outside commands)? → if yes, deletion must respect those
- Is the teleprompter script export path still sacred? → referenced in CLAUDE.md as non-optional

---

## Confidence

| Area | Confidence | Basis |
|---|---|---|
| Agent delegation savings | HIGH | Proven in current gsd-* flow; basic Claude Code primitive |
| AskUserQuestion mid-flow | HIGH | Already used by gsd-new-milestone workflow (this session confirms) |
| Safe to delete unused commands | HIGH | Git history + 30-day usage check |
| Safe to delete unused Python files | MEDIUM | Some are imports-of-imports; need dependency graph before mass delete |
| Consolidation of 35 refs to ~15 | MEDIUM | Overlap is visible in file names; actual content overlap needs agent review |
| Sequential over parallel agent spawn for rate-limit-prone accounts | HIGH | Direct observation this session: 4 parallel agents → all hit limit |

---

*Research written in main context on 2026-04-21 due to rate limit preventing agent spawn. Normal pattern should be agent-delegated.*
