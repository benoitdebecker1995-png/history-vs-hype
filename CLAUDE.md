# CLAUDE.md

## Repository Overview

**History vs Hype** — YouTube channel: evidence-based myth-busting about geopolitics, colonial history, border disputes, and ideological narratives. Academic research + primary sources to debunk historical myths.

**Stats:** 515 subs, 219K+ views, 47 long-form, 28.1% median retention | **Audience:** Males 25-44 (UK, DE, CA, US)
**Format:** 8-12 min hybrid talking head + B-roll evidence | **Hard cap 12 min** (r=-0.455 duration-retention, n=47)

**Subscriber trigger:** "intellectual competence" — proving you understand SYSTEMS, not narratives. HOW > WHY. Mechanism > politics. Logistics/legal/admin angles win. RealLifeLore/Wendover overlap audience.

**Growth bottleneck:** Packaging, not content. Only 3/47 broke 2K views. Content that gets impressions performs well. `/greenlight` BEFORE any research.

---

## Skill Library (read `project-onboarding` first in any cold session)

Nine skills under `.claude/skills/` carry the project's operating knowledge — built 2026-07 so
any session (junior engineer or smaller model) can debug, extend, validate, and advance this
project at standard: `project-onboarding` (entry router) · `codebase-atlas` · `data-stores` ·
`debugging-playbook` · `automation-ops` · `extending-safely` · `authoring-skills` (craft standard
for writing skills/commands/agents) · `validation-standards` ·
`production-map` (+ pre-existing `historian`; + `primary-source`, the on-screen-provenance
discipline that pairs with the `primary-source-hunter` agent). Index: `.claude/skills/README.md`. Skills route
to authoritative files rather than duplicating them; when this file and a skill disagree on an
implementation detail, the skill's live-verified claim is usually newer — verify, then fix both.

---

## Knowledge Graphs

⚠ **The graphify MCP servers do NOT resolve** (verified 2026-07-30 — their Python 3.12 was
uninstalled). Use grep/Glob. The graph *data* survives: `graphify-out/graph.json`, and
`python graphify-out/research/query.py "<entity>"` for the sparse research graph (under ~3 hits ⇒
read files instead). Recovery + open work: `.claude/REFERENCE/GRAPHIFY-OPS.md`.

---

## Core Principles

1. **Historical integrity** — every claim verified with credible sources
2. **Real quotes with page numbers** — word-for-word from academic sources (the competitive advantage)
3. **Modern relevance** — connect history to 2024-2026 developments
4. **Academic balance** — present multiple perspectives, acknowledge counter-evidence
5. **Deep causal chains** — explain WHY (spoken-register connectors: so, which is why, and that meant; formal "consequently/thereby" sparingly)
6. **No oversimplification** — maintain nuance while accessible

---

## Quick Start Commands

**Pre-production:** `/grill-angle` (sharpen angle) → `/greenlight` (packaging gate, before ANY research) → `/research` → `/research --sources`
**Production:** `/script` → `/verify` → `/prep` → `/thumbnail`
**Post-production:** `/editing-guide` (after rough cut) → `/fix` (subtitle correction) → `/publish` → `/engage` → (on upload) `/reconcile <slug>`
**Navigation:** `/status` | `/reconcile` | `/help` | `/next`
**Article writing:** `article-writer` agent (CONVERT / WRITE / EDIT / WORKSHOP modes — invoke directly)
**Analytics:** `/analyze` | `/patterns` | `/growth` | `/retitle`

---

## File Organization (CRITICAL)

**Lifecycle folders (MANDATORY):**
- `video-projects/_IN_PRODUCTION/` → `_READY_TO_FILM/` → `_ARCHIVED/published/`
- **NEVER** create loose folders in `video-projects/` root
- Naming: `video-projects/[lifecycle]/[number]-[topic-slug-year]/`

**Folder lifecycle (truth source: filesystem + analytics.db):**
- `_IN_PRODUCTION/` — research / scripting / fact-check phase
- `_READY_TO_FILM/` — `FINAL-SCRIPT.md` exists OR `.mp4` rough cut exists, no YouTube URL yet (covers: script-locked OR filmed OR in-post)
- `_ARCHIVED/published/` — YouTube published. Matched via `analytics.db` Video ID.
- `_BACKLOG/` — **holding bucket, OUTSIDE the lifecycle.** Dormant/parked projects not actively being worked. Invisible to scanners (`session_context.py`, `project_scanner.py`, `reconcile.py` all glob only the 3 lifecycle folders), so it declutters the active surface without losing work. Pull a folder back to `_IN_PRODUCTION/` when you resume it. NOT for published or filmed work (those go to their lifecycle bucket).

**Before creating any file:** Read `PROJECT_STATUS.md` → Glob for existing folder → confirm lifecycle stage

**Standard project files:**
- `01-VERIFIED-RESEARCH.md` — single source of truth for verified facts
- `02-SCRIPT-DRAFT.md` — production-ready script
- `03-FACT-CHECK-VERIFICATION.md` — final quality gate
- `YOUTUBE-METADATA.md` — title, description, tags, timestamps
- `PROJECT-STATUS.md` — per-folder narrative. Top of file has a `<!-- AUTO:reconcile -->` block (managed by `/reconcile`); narrative below `<!-- /AUTO:reconcile -->` is hand-written and never overwritten.

See: `.claude/REFERENCE/FOLDER-STRUCTURE-GUIDE.md`

---

## Project State Reconciliation (folder drift)

**Truth sources:**
- Filesystem → lifecycle stage
- `tools/youtube_analytics/analytics.db` → publish status (Video ID, title, published_at)
- In-folder `PROJECT-STATUS.md` narrative → hand-written project state

**Derived (auto-regenerated by `/reconcile`):**
- Folder location (`_IN_PRODUCTION/` ↔ `_READY_TO_FILM/` ↔ `_ARCHIVED/published/`)
- AUTO block at top of per-folder `PROJECT-STATUS.md`
- Root `video-projects/PROJECT_STATUS.md` and `PROJECT_REGISTRY.md`
- `.brain/index.md §3` Active Topics

**Conversational trigger (MANDATORY):** When the user says "I uploaded X" / "I released X" / "I published X" / "X is live" / "X went up" — run `/reconcile <X>` immediately. Do NOT just look up the video. Do NOT assume project files are current. The utterance IS the write trigger. If X is ambiguous (multiple folders match), ask once before proceeding.

**Conversational trigger — script lock (MANDATORY):** When the user declares a script locked ("script locked" / "lock it" / "T1 passed" / read-aloud passed top-to-bottom) — IMMEDIATELY run the post-lock delta-mine for that video: (1) consolidate its read-aloud notes, version diffs, and session corrections into `channel-data/calibration/CALIBRATION-CORPUS.md` (axis-tagged, tiered, per the corpus header rules); (2) append any new contradictions to `channel-data/calibration/INTERVIEW-AGENDA.md`; (3) record the video's passes-to-lock count in `channel-data/calibration/EVAL-BASELINE.md`. The lock declaration IS the mining trigger — deltas are freshest at lock and go stale fast. See the `feedback-calibration-loop` memory (user-memory store, not a repo path).

**Backstop:** Routine 6 (`HvH-Reconcile`, daily 08:30) archives publishes missed by conversation and NEVER touches memory snapshots — lessons-promotion stays gated on interactive `/reconcile`. It depends on Routine 7 (`HvH-GrowthRefresh`, 07:45) keeping `analytics.db` fresh; the chain is 07:45 refresh → 08:00 channel-health → 08:30 reconcile. Schedules, wrapper scripts and health checks: **automation-ops** skill. `/reconcile` also backstops the calibration loop, flagging locked scripts whose deltas aren't in the corpus.

**Memory snapshots** (`memory/[N]-production-state.md`): frozen point-in-time during active project life. Append new dated entries; don't overwrite. On archive (interactive `/reconcile` only), user is prompted to promote lessons to `feedback-*.md` before snapshot is deleted.

See: `.claude/commands/reconcile.md` | the `feedback-project-reconciliation` memory

---

## The pipeline, and where its rules live

`/greenlight` (packaging gate) → `/research` → `/script` → `/verify` → `/prep` → `/publish`

1. **Research + Verify** → `01-VERIFIED-RESEARCH.md`, each fact ✅/⏳/❌. Gate: 90%+ before writing.
2. **Script from verified facts ONLY** → `02-SCRIPT-DRAFT.md`. Unverified fact ⇒ STOP and verify.
3. **Cross-check** → `03-FACT-CHECK-VERIFICATION.md`, every line vs the research. ✅ APPROVED / ❌ REVISION.

The detailed rules are **path-scoped** in `.claude/rules/` — they load automatically when you open a
matching file, so they are not repeated here (split 2026-07-31; nothing was dropped):

| Rule file | Loads when you open | Covers |
|---|---|---|
| `script-writing.md` | `SCRIPT.md`, `*SCRIPT-DRAFT.md`, `FINAL-SCRIPT.md` | Calm-Prosecutor voice, structure, language-to-avoid, templates, voice_lint |
| `packaging.md` | `YOUTUBE-METADATA.md`, `THUMBNAIL-*.md`, `title_scorer.py` | Demand gate, title penalties, thumbnail rules, collision check |
| `research-verification.md` | `01-VERIFIED-RESEARCH.md`, `03-FACT-CHECK-*.md`, `_research/**` | Two-phase research, source tiers, red flags, graded claim status |
| `python-tools.md` | `tools/**/*.py`, `tests/**/*.py` | Import/error/logging contracts, seams, test discipline |

**NEVER skip Phase 2** (NotebookLM academic verification) — that is the competitive advantage.
**Channel DNA:** history with modern relevance, NOT geopolitics with historical background. Test:
"Will this matter in 10 years regardless of who's in power?"

---

## Working Style

- **Be direct and efficient** — no pleasantries, get to the point
- **Read first, ask later** — use Glob/Read to find info, don't ask user
- **Parallel tool calls** — when multiple independent reads needed
- **Don't ask for info in files you can read** — find it yourself
- See: `.claude/USER-PREFERENCES.md` for complete guide

### Calibration (Opus 5 — these are specific because the model follows instructions literally)

Documented Opus 5 traits: longer responses, readier narration, longer written files, scope
expansion, loud correction-narration, readier delegation. Each has a rule. Full sourcing and the
remedies: **`.claude/REFERENCE/OPUS-5-CALIBRATION.md`**.

1. **Lead with the outcome.** First sentence answers "what happened" / "what did you find."
   Detail after. Caveats short, and after the answer.
2. **Calibrated language.** State what a finding is and what it supports; let the reader weigh it.
   **At most one "strongest/most important" per project**, and say what it changes. "Mother lode",
   "crown jewel", "spectacular" — no. *(Hyperbole is NOT a documented model trait; it is a house
   failure. See ADR-0021, which enforces the evidence half in code.)*
3. **Narrate once, not per step.** One sentence before the first tool call; updates only on a real
   finding or a change of direction.
4. **Written files match the task.** Cover the substance; no filler sections, no redundant
   summaries. A research file records findings and status — not a narrative of the session.
5. **Hold scope.** Deliver what was asked. Routine judgement calls are yours; check in only when
   readings differ materially. Better idea? Say it in a sentence, then do what was asked.
6. **Correct once, quietly.** Only when the error changes a decision. Then continue.
7. **Delegate rarely.** Only large, genuinely independent, parallel work. Never to verify your own
   work. ⚠ `USER-PREFERENCES.md` § "Main Context = Orchestrator Only" was tuned for a model that
   under-delegated — treat its trigger as an upper bound, not a prompt.

**Do NOT add self-verification scaffolding** ("double-check", "re-verify before responding").
Opus 5 self-verifies; such instructions cause over-verification. *(Checked 2026-07-30: the
`re-verify` rules in `/verify`, `/verify-flow-nlm` and `.claude/skills/historian/WEB-POLICY.md` are domain rules
about fast-moving facts — legitimate, keep them.)*

---

## Critical Reminders

These are the cross-cutting ones. Stage-specific rules (voice, source tiers, title penalties, claim
status) live in `.claude/rules/` and load when you open a matching file — they are not repeated here.

1. **PACKAGING FIRST** — `/greenlight` before ANY research. Collision-check first:
   `python -m tools.preflight.candidate_preflight "<topic>"`. A published match is a stop, and it
   runs *before* the pitch, not after.
2. **NEVER skip Phase 2** (NotebookLM academic verification) — that's the competitive advantage.
   University presses, top scholars, budget UNLIMITED.
3. **REAL QUOTES with page numbers, primary sources ON SCREEN** — not summaries, not optional.
   This is the whole product; unnamed authority ("historians argue") is its exact inverse.
4. **HOW > WHY** for subscriber growth — mechanisms and logistics, not politics.
5. **Intellectual honesty** — acknowledge what the opposing side gets right.
6. **AGENT ORCHESTRATION** — read `.claude/AGENT-ORCHESTRATION.md` before spawning sub-agents:
   return contract, tiers, rate-limit rule.
7. **Calibration** — lead with the outcome · one superlative per project, max · narrate once, not
   per step · hold scope · correct once, quietly. Working Style above, and
   `.claude/REFERENCE/OPUS-5-CALIBRATION.md`.

---

## Agent skills

- **Issues** — GitHub Issues on `benoitdebecker1995-png/history-vs-hype` via `gh` CLI → `docs/agents/issue-tracker.md`
- **Triage labels** — `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix` → `docs/agents/triage-labels.md`
- **Domain docs** — single-context layout, `CONTEXT.md` + `docs/adr/` at repo root → `docs/agents/domain.md`

---

## Key References

- **Style:** `.claude/REFERENCE/WRITING-VOICE-AND-STYLE.md` (authoritative)
- **Commands:** `.claude/commands/` | **Agents:** `.claude/agents/`
- **Reference index:** `.claude/REFERENCE/INDEX.md`
- **Packaging:** `tools/PACKAGING_MANDATE.md`
- **Performance data:** See memory files (patterns, analytics, competitor findings)
- **Topic pipeline:** `channel-data/TOPIC-PIPELINE.md`
- **Next-video discovery / breakout work (ACTIVE, cross-machine handoff):**
  `channel-data/NEXT-VIDEO-DISCOVERY-HANDOFF.md` — read this when asked to continue finding the next
  video, hunt topics with demand but no supply, or resume breakout/measurement work. Carries the serve-vs-CTR
  model, the two failure modes, the gap-hunter build spec, and current blockers.

**Start:** `/greenlight` → `/research --new`
