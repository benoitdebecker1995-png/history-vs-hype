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

⚠ **The two MCP servers are NOT registered — verified 2026-07-30.** `graphify` appears
nowhere in `~/.claude.json`, the Claude Desktop config, or the surviving backup, and no
`mcp__graphify-*` tool resolves. This file previously told sessions to prefer
`mcp__graphify-code__query_graph` etc. over grep; **those calls cannot work.** Use grep,
Glob, and the file-based queries below until the servers are re-registered
(`.claude/REFERENCE/GRAPHIFY-OPS.md` § Recovery).

**The graph data still exists** — only the MCP wiring is gone:
- Code graph — `graphify-out/graph.json` (81 MB, refreshed by the post-commit hook)
- Research graph — sparse ~110-node concept graph over the archived
  `01-VERIFIED-RESEARCH.md` files. Query it directly:
  ```bash
  python graphify-out/research/query.py "uti possidetis" --max-nodes 5
  ```
  Read `graphify-out/research/GRAPH_REPORT.md` for bridges and suggested questions.

**Honest scope:** the research graph is sparse — good for entity lookups ("did we cite
Mamdani"), but under ~3 hits means fall back to file reads.

Workflow patterns, recovery commands, and the open-work list: `.claude/REFERENCE/GRAPHIFY-OPS.md`.

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

## Research: Two-Phase Approach (CRITICAL)

**Phase 1: Internet research** — map landscape, identify claims to verify (Wikipedia, news, Google Scholar). All findings marked ❓. Free, 2-4 hours.

**Phase 2: NotebookLM academic verification** — university press books ONLY (Cambridge, Oxford, etc.), top scholars, critical editions. Budget UNLIMITED. Upload 10-20 sources, use citation grounding for exact page numbers. Output: verified quotes ready for script.

**NEVER skip Phase 2.** That's the competitive advantage. See: `.claude/REFERENCE/NOTEBOOKLM-SOURCE-STANDARDS.md`

---

## Verified Workflow (3-Phase Quality Gates)

1. **Research + Verify** → `01-VERIFIED-RESEARCH.md` — mark each fact ✅/⏳/❌. Gate: 90%+ verified before writing.
2. **Script from verified facts ONLY** → `02-SCRIPT-DRAFT.md` — if fact isn't verified, STOP and verify first.
3. **Cross-check** → `03-FACT-CHECK-VERIFICATION.md` — every script line vs verified research. Verdict: ✅ APPROVED or ❌ REVISION.

---

## Script Writing

**Authoritative reference:** `.claude/REFERENCE/WRITING-VOICE-AND-STYLE.md` — READ BEFORE WRITING ANY SCRIPT (PARTS 1-5 script-side).

**Voice:** "Calm Prosecutor" — emotionally low, intellectually high. Evidence-based referee.

**Key rules:** Real quotes with page numbers | Primary sources ON SCREEN | Define every term immediately | Contractions ("it's" not "it is") | Dates spoken ("On June 16th, 2014") | "Here's" max 2-4/script

**Structure:** Myth-first for non-territorial (30.3% vs 22.4% retention) | Turn at 15-25% runtime (3.2x, not 25-35% dead zone at 2.1x) | Modern relevance every 90s | Pattern interrupt every 2-3 min | Deep causal chains throughout

**Language to avoid:** "X is occupying Y" | "Z destroyed the culture" | absolutist language | conspiracy framing without documentation

**Templates:** `.claude/REFERENCE/OPENING-HOOK-TEMPLATES.md` | `.claude/REFERENCE/CLOSING-SYNTHESIS-TEMPLATES.md`

---

## Fact-Checking

**Source hierarchy:** See `.claude/REFERENCE/fact-checking-protocol.md`
- Tier 1: Primary documents, peer-reviewed (2010+), expert historians
- Tier 2: Journalists, intl org reports, declassified docs
- Tier 3: News sources (verify multiple), documentary evidence

**Red flags requiring immediate verification:**
- "The court ruled X..." → Which paragraph? Exact quote?
- "The treaty says..." → Which article? Exact language?
- Any quote without page number → Verify with primary source

**NEVER include unverified claims.** If you can't verify: don't include it, flag it, or ask user for source.

See: `.claude/REFERENCE/FACT-CHECK-SIMPLIFICATION-RULES.md` for 8 anti-oversimplification rules

---

## Packaging-First Workflow

1. **Search demand** — graded gate, NOT a hard stop: GO ≥1,000/mo · CAUTION 500–999 · STOP <500, and a **verified live news hook overrides a STOP**. Authority: `.claude/commands/greenlight.md` Step 1.
2. **Title generation** — `title_scorer.py`. Front-load keyword. Declarative = default (3.8% CTR). **Years and colons are graded penalties, not bans** — `YEAR_PENALTY -15`, `COLON_PENALTY -10`, `COLON_PENALTY_VERSUS 0` (`tools/title_scorer.py:308-313`, authoritative). The old −46%/−28% "hard rule" was topic-confounded and is **retired**; the channel's #1 and #3 videos both use colons.
3. **Thumbnail concept** — text overlay MANDATORY (87% niche), no face (0% niche), maps for territorial. `thumbnail_checker.py`
4. **THEN research** — only after `/greenlight` passes

See: `tools/PACKAGING_MANDATE.md` | `.claude/REFERENCE/TITLE-GENERATION-PROTOCOL.md`

**Channel DNA:** History channel with modern relevance, NOT geopolitics with historical background. Test: "Will this matter in 10 years regardless of who's in power?"

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

1. **PACKAGING FIRST** — `/greenlight` before ANY research
2. **NEVER skip Phase 2** (NotebookLM) — that's the competitive advantage
3. **ACADEMIC SOURCES ONLY** — university presses, top scholars. Budget UNLIMITED
4. **REAL QUOTES with page numbers** — not summaries
5. **Primary sources ON SCREEN** — non-optional
6. **Read WRITING-VOICE-AND-STYLE.md before scripts** — voice, delivery, patterns, checklist (PARTS 1-5)
7. **Write for spoken delivery** — contractions, natural phrasing
8. **Deep causal chains** — explain WHY (spoken-register connectors: so, which is why, and that meant; formal "consequently/thereby" sparingly)
9. **Intellectual honesty** — acknowledge what opposing side gets right
10. **Single source of truth** — 01-VERIFIED-RESEARCH.md only
11. **Quality gates** — 90% verified → write; 100% cross-checked → film
12. **HOW > WHY** for subscriber growth — mechanisms/logistics, not politics
13. **Years/colons in titles = HEDGE, not ban** — graded penalties, A/B-testable (the old -46%/-28% hard rule was topic-confounded; the channel's #1 and #3 videos have colons). See `tools/PACKAGING_MANDATE.md` Tier 2
14. **Text overlay on thumbnails** — 2-4 words, not full title. Maps for territorial.
15. **AGENT ORCHESTRATION** — Read `.claude/AGENT-ORCHESTRATION.md` before spawning sub-agents — return contract, tiers, rate-limit rule
16. **Claim status is graded, not binary** — `ASSERTED → SOURCED → INSPECTED → CORROBORATED/CONTESTED → SETTLED`. Verdict words (REFUTED/PROVEN/RESOLVED) only at CORROBORATED+. Check with `python -m tools.preflight.claim_status <file.md>`; `--frontier` says whether research is actually finished. ADR-0021
17. **Collision-check before proposing a video** — `python -m tools.preflight.candidate_preflight "<topic>"`. Published match = stop. Run it *before* the pitch, not after
18. **Calibration** — lead with the outcome · one superlative per project, max · narrate once not per step · hold scope · correct once, quietly. See Working Style above and `.claude/REFERENCE/OPUS-5-CALIBRATION.md`

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
