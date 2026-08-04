# AGENTS.md

Project guidance for **Codex / GPT-5.6** working in this repository. The Claude Code surface
(`.claude/`) is the canonical source of truth for every rule below; this file and the Codex surface
(`.agents/skills/`, `.codex/`) are the hand-maintained port of it. When the two disagree, `.claude/`
wins and the port needs fixing.

## Repository Overview

**History vs Hype** — YouTube channel: evidence-based myth-busting about geopolitics, colonial
history, border disputes, and ideological narratives. Academic research + primary sources to debunk
historical myths.

**Stats:** 515 subs, 219K+ views, 47 long-form, 28.1% median retention | **Audience:** Males 25-44
(UK, DE, CA, US)
**Format:** 8-12 min hybrid talking head + B-roll evidence | **Hard cap 12 min**
(r=-0.455 duration-retention, n=47)

**Subscriber trigger:** "intellectual competence" — proving you understand SYSTEMS, not narratives.
HOW > WHY. Mechanism > politics. Logistics/legal/admin angles win. RealLifeLore/Wendover overlap
audience.

**Growth bottleneck:** Packaging, not content. Only 3/47 broke 2K views. Content that gets
impressions performs well. Run the greenlight gate BEFORE any research.

---

## How this project's workflows reach you on Codex

Claude Code has slash commands, sub-agents, path-scoped rules and skills. Codex has skills,
sub-agents and `AGENTS.md`. The mapping:

| Claude Code | Codex | Where |
|---|---|---|
| 34 slash commands (`/greenlight`, `/script`, …) | skills named `source-command-<name>` | `.agents/skills/` |
| 11 project skills | same skills | `.agents/skills/` |
| 4 path-scoped rules | 3 rule-skills + this file's nested copies | `.agents/skills/`, `tools/AGENTS.md`, `tests/AGENTS.md` |
| 12 sub-agents | custom agents | `.codex/agents/*.toml` |
| 3 lifecycle hooks | same 3 scripts, same 3 events | `.codex/hooks.json` |
| MCP servers | the 3 from `.mcp.json` + vidiq + playwright | `.codex/config.toml` |

A skill fires implicitly off its description, or you can name it: `$source-command-greenlight`.

**Two fidelity gaps to know about:**

1. **Rules are model-triggered here, not automatic.** On Claude Code the voice rules, packaging
   penalties and source-tier rules load the moment a matching file is opened. On Codex they are
   skills that fire off their description. **Before writing or editing a `SCRIPT.md`, a
   `YOUTUBE-METADATA.md`, or a `01-VERIFIED-RESEARCH.md`, load the matching rule-skill yourself**
   (`rule-script-writing`, `rule-packaging`, `rule-research-verification`). Don't assume it fired.
2. **No per-workflow model pin.** Claude's command files pin a model each; Codex skills run at the
   session model, which `.codex/config.toml` pins to `gpt-5.6-sol` at `high` effort (sol's own
   default is `low` — leaving it unset is how a heavy session quietly runs shallow). The cheap
   routing workflows (`status`, `help`) therefore cost the same as the expensive ones here.
   Sub-agents pin their own model and effort per file; `.codex/agents/` is the place to change that.

**Keeping the port honest.** `.claude/` is canonical and nothing syncs automatically, so an edit
there does not reach Codex until it is re-ported. `python -m pytest tests/unit/test_codex_surface_parity.py`
fails the moment the two drift — run it after touching anything under `.claude/`.

**Entry point for a cold session:** read the `project-onboarding` skill first. It routes to the
other ten (`codebase-atlas`, `data-stores`, `debugging-playbook`, `automation-ops`,
`extending-safely`, `authoring-skills`, `validation-standards`, `production-map`, `historian`,
`primary-source`).

---

## Knowledge Graphs

Two MCP servers, declared in `.codex/config.toml`:

- `graphify-code` — 90,745 nodes / 97,940 edges over the repo AST (`graphify-out/graph.json`)
- `graphify-research` — 169-node concept graph over the archived `01-VERIFIED-RESEARCH.md` files

**Prefer a graph query over grep/Read when the question is structural** — that is the whole point,
it costs far fewer tokens than reading files:
- "Where does X live / what depends on it" → `query_graph`, `get_neighbors`
- "How does A connect to B" → `shortest_path` · "Most-connected hubs" → `god_nodes`
- "Have we covered scholar/treaty Z" → `graphify-research` `query_graph`

**Honest scope:** the research graph is sparse — under ~3 hits, fall back to file reads. File-based
fallback: `python graphify-out/research/query.py "<entity>"`. Ops + recovery:
`.claude/REFERENCE/GRAPHIFY-OPS.md`.

---

## Core Principles

1. **Historical integrity** — every claim verified with credible sources
2. **Real quotes with page numbers** — word-for-word from academic sources (the competitive advantage)
3. **Modern relevance** — connect history to 2024-2026 developments
4. **Academic balance** — present multiple perspectives, acknowledge counter-evidence
5. **Deep causal chains** — explain WHY (spoken-register connectors: so, which is why, and that
   meant; formal "consequently/thereby" sparingly)
6. **No oversimplification** — maintain nuance while accessible

---

## The pipeline

`greenlight` (packaging gate) → `research` → `script` → `verify` → `prep` → `publish`

Each stage is a `source-command-*` skill.

1. **Research + Verify** → `01-VERIFIED-RESEARCH.md`, each fact ✅/⏳/❌. Gate: 90%+ before writing.
2. **Script from verified facts ONLY** → `02-SCRIPT-DRAFT.md`. Unverified fact ⇒ STOP and verify.
3. **Cross-check** → `03-FACT-CHECK-VERIFICATION.md`, every line vs the research.
   ✅ APPROVED / ❌ REVISION.

**Other workflows:** `grill-angle` (sharpen angle, before greenlight) · `thumbnail` · `opener` ·
`polish` · `editing-guide` · `fix` (subtitles) · `engage` · `reconcile` · `status` · `next` ·
`analyze` / `patterns` / `growth` / `retitle` · `translate` (Untranslated series) ·
`voice` / `voice-readthrough` / `voice-clickdrill` · `preflight` · `comment-mine` ·
`learn-from-paper` · `referee-retrofit` · `gemini` (bulk-read offload).

**NEVER skip Phase 2** (NotebookLM academic verification) — that is the competitive advantage.
**Channel DNA:** history with modern relevance, NOT geopolitics with historical background. Test:
"Will this matter in 10 years regardless of who's in power?"

---

## File Organization (CRITICAL)

**Lifecycle folders (MANDATORY):**
- `video-projects/_IN_PRODUCTION/` → `_READY_TO_FILM/` → `_ARCHIVED/published/`
- **NEVER** create loose folders in `video-projects/` root
- Naming: `video-projects/[lifecycle]/[number]-[topic-slug-year]/`

**Folder lifecycle (truth source: filesystem + analytics.db):**
- `_IN_PRODUCTION/` — research / scripting / fact-check phase
- `_READY_TO_FILM/` — `FINAL-SCRIPT.md` exists OR `.mp4` rough cut exists, no YouTube URL yet
- `_ARCHIVED/published/` — YouTube published. Matched via `analytics.db` Video ID.
- `_BACKLOG/` — **holding bucket, OUTSIDE the lifecycle.** Dormant/parked projects. Invisible to
  scanners (`session_context.py`, `project_scanner.py`, `reconcile.py` glob only the 3 lifecycle
  folders). Pull a folder back to `_IN_PRODUCTION/` when you resume it. NOT for published or filmed
  work.

**Before creating any file:** read `PROJECT_STATUS.md` → glob for an existing folder → confirm
lifecycle stage.

**Standard project files:** `01-VERIFIED-RESEARCH.md` (single source of truth for verified facts) ·
`02-SCRIPT-DRAFT.md` · `03-FACT-CHECK-VERIFICATION.md` · `YOUTUBE-METADATA.md` ·
`PROJECT-STATUS.md` (its `<!-- AUTO:reconcile -->` block is machine-managed; narrative below the
close tag is hand-written and never overwritten).

See: `.claude/REFERENCE/FOLDER-STRUCTURE-GUIDE.md`

---

## Project State Reconciliation (folder drift)

**Truth sources:** filesystem → lifecycle stage · `tools/youtube_analytics/analytics.db` → publish
status · in-folder `PROJECT-STATUS.md` narrative → hand-written state.

**Derived (auto-regenerated by the `reconcile` skill):** folder location, the AUTO block, root
`PROJECT_STATUS.md` / `PROJECT_REGISTRY.md`, `.brain/index.md §3`.

**Conversational trigger (MANDATORY):** when the user says "I uploaded X" / "I released X" /
"I published X" / "X is live" / "X went up" — run the `reconcile` skill on X immediately. Do NOT
just look up the video. The utterance IS the write trigger. If X is ambiguous, ask once.

**Conversational trigger — script lock (MANDATORY):** when the user declares a script locked
("script locked" / "lock it" / "T1 passed") — immediately run the post-lock delta-mine: consolidate
read-aloud notes and session corrections into `channel-data/calibration/CALIBRATION-CORPUS.md`,
append new contradictions to `INTERVIEW-AGENDA.md`, record passes-to-lock in `EVAL-BASELINE.md`.
The lock declaration IS the mining trigger.

**Backstop:** a daily scheduled routine (`HvH-Reconcile`, 08:30) archives publishes missed by
conversation and never touches memory snapshots. Chain: 07:45 growth refresh → 08:00 channel-health
→ 08:30 reconcile. Details: `automation-ops` skill.

---

## Working Style

- **Be direct and efficient** — no pleasantries, get to the point
- **Read first, ask later** — glob/read to find info, don't ask the user
- **Don't ask for info in files you can read** — find it yourself
- **Lead with the outcome.** First sentence answers "what happened" / "what did you find."
- **Calibrated language.** State what a finding is and what it supports. At most one
  "strongest/most important" per project, and say what it changes. No "mother lode", "crown jewel",
  "spectacular".
- **Written files match the task.** No filler sections, no redundant summaries.
- **Hold scope.** Deliver what was asked. Better idea? Say it in a sentence, then do what was asked.
- **Correct once, quietly.** Only when the error changes a decision.
- See `.claude/USER-PREFERENCES.md` for the full guide.

### Sub-agents

16 custom agents live in `.codex/agents/*.toml` (article-writer, primary-source-hunter,
notebook-researcher, script-writer-v2, structure-checker-v2, packaging-adversary, thumbnail-critic,
comment-responder, competitor-gap, series-planner, wiki-researcher, diy-asset-creator, …).

Spawn one only for large, genuinely independent work — never to verify your own output. Every spawn
prompt carries: the exact paths to read, one imperative goal sentence, and the return contract from
`.claude/AGENT-ORCHESTRATION.md`. Concurrency cap is set by
`agents.max_concurrent_threads_per_session` in `.codex/config.toml`.

---

## Critical Reminders

1. **PACKAGING FIRST** — greenlight before ANY research. Collision-check first:
   `python -m tools.preflight.candidate_preflight "<topic>"`. A published match is a stop, and it
   runs *before* the pitch.
2. **NEVER skip Phase 2** (NotebookLM academic verification). University presses, top scholars,
   budget UNLIMITED.
3. **REAL QUOTES with page numbers, primary sources ON SCREEN** — not summaries, not optional.
   Unnamed authority ("historians argue") is the exact inverse of the product.
4. **HOW > WHY** for subscriber growth — mechanisms and logistics, not politics.
5. **Intellectual honesty** — acknowledge what the opposing side gets right.
6. **Load the rule-skill before writing** — see fidelity gap 1 above.

---

## Key References

- **Style:** `.claude/REFERENCE/WRITING-VOICE-AND-STYLE.md` (authoritative)
- **Reference index:** `.claude/REFERENCE/INDEX.md` · **Packaging:** `tools/PACKAGING_MANDATE.md`
- **Topic pipeline:** `channel-data/TOPIC-PIPELINE.md`
- **Next-video discovery / breakout work (ACTIVE):** `channel-data/NEXT-VIDEO-DISCOVERY-HANDOFF.md`
- **Issues:** GitHub Issues on `benoitdebecker1995-png/history-vs-hype` via `gh` → `docs/agents/issue-tracker.md`
- **Domain docs:** `CONTEXT.md` + `docs/adr/` at repo root → `docs/agents/domain.md`
