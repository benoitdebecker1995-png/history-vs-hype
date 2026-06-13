# CLAUDE.md

## Repository Overview

**History vs Hype** — YouTube channel: evidence-based myth-busting about geopolitics, colonial history, border disputes, and ideological narratives. Academic research + primary sources to debunk historical myths.

**Stats:** 515 subs, 219K+ views, 47 long-form, 28.1% median retention | **Audience:** Males 25-44 (UK, DE, CA, US)
**Format:** 8-12 min hybrid talking head + B-roll evidence | **Hard cap 12 min** (r=-0.455 duration-retention, n=47)

**Subscriber trigger:** "intellectual competence" — proving you understand SYSTEMS, not narratives. HOW > WHY. Mechanism > politics. Logistics/legal/admin angles win. RealLifeLore/Wendover overlap audience.

**Growth bottleneck:** Packaging, not content. Only 3/47 broke 2K views. Content that gets impressions performs well. `/greenlight` BEFORE any research.

---

## Knowledge Graphs (MCP)

Two MCP servers are live for this project: `graphify-code` (54K-node AST graph of the whole repo) and `graphify-research` (sparse 110-node concept graph from 16 archived `01-VERIFIED-RESEARCH.md` files). Graphs survive across sessions. Post-commit hook keeps the code graph fresh.

**Prefer graph queries over grep/Read when the question is structural:**
- "Where does X live" / "what does X depend on" → `mcp__graphify-code__query_graph` or `mcp__graphify-code__get_neighbors`
- "How does A connect to B" → `mcp__graphify-code__shortest_path`
- "What are the most-connected hubs" → `mcp__graphify-code__god_nodes`
- "Have we covered scholar / treaty / topic Z across videos" → `mcp__graphify-research__query_graph`

**Honest scope:** Code graph is dense and reliable. Research graph is sparse — query it for entity-specific lookups ("did we cite Mamdani"), but if it returns <3 hits fall back to file reads. Densifying the research graph is on the open-work list.

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

**Pre-production:** `/greenlight` (FIRST) → `/research` → `/sources`
**Production:** `/script` → `/verify` → `/prep` → `/thumbnail`
**Post-production:** `/editing-guide` (after rough cut) → `/fix` (subtitle correction) → `/publish` → `/engage` → (on upload) `/reconcile <slug>`
**Navigation:** `/status` | `/reconcile` | `/help` | `/next` | `/intel`
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

See: `.claude/FOLDER-STRUCTURE-GUIDE.md`

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

**Conversational trigger — script lock (MANDATORY):** When the user declares a script locked ("script locked" / "lock it" / "T1 passed" / read-aloud passed top-to-bottom) — IMMEDIATELY run the post-lock delta-mine for that video: (1) consolidate its read-aloud notes, version diffs, and session corrections into `channel-data/calibration/CALIBRATION-CORPUS.md` (axis-tagged, tiered, per the corpus header rules); (2) append any new contradictions to `channel-data/calibration/INTERVIEW-AGENDA.md`; (3) record the video's passes-to-lock count in `channel-data/calibration/EVAL-BASELINE.md`. The lock declaration IS the mining trigger — deltas are freshest at lock and go stale fast. See `memory/feedback-calibration-loop.md`.

**Backstop:** Routine 6 (`run-reconcile.ps1`, `--auto-publish-only`) is *designed* to run daily 08:30 to archive any new YouTube publishes missed by conversation, and NEVER touches memory snapshots — lessons-promotion stays gated on interactive `/reconcile`. ⚠️ **As of the W3 audit (2026-06-12) Routine 6 is NOT actually scheduled** — no `HvH-Reconcile` task is registered and zero `reconcile-*.log` files exist, so the daily backstop is currently inactive; the conversational "I uploaded X" → `/reconcile` trigger is the only live archival path until it's registered (`schtasks /Create /TN HvH-Reconcile /TR "powershell -File 'D:\History vs Hype\.claude\routines\run-reconcile.ps1'" /SC DAILY /ST 08:30`). See `docs/AUDIT-COMMANDS-2026-06.md` § Routine health. `/reconcile` itself backstops the calibration loop: each run flags locked scripts whose deltas aren't in the corpus (see `.claude/commands/reconcile.md`).

**Memory snapshots** (`memory/[N]-production-state.md`): frozen point-in-time during active project life. Append new dated entries; don't overwrite. On archive (interactive `/reconcile` only), user is prompted to promote lessons to `feedback-*.md` before snapshot is deleted.

See: `.claude/commands/reconcile.md` | `memory/feedback-project-reconciliation.md`

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

See: `.claude/FACT-CHECK-SIMPLIFICATION-RULES.md` for 8 anti-oversimplification rules

---

## Packaging-First Workflow

1. **Search demand** — <1K/mo = hard stop
2. **Title generation** — `title_scorer.py`. No years (-46% CTR), no colons (-28%). Front-load keyword. Declarative = default (3.8% CTR).
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

---

## Agent skills

### Issue tracker

Issues live in GitHub Issues for `benoitdebecker1995-png/history-vs-hype`, accessed via `gh` CLI. See `docs/agents/issue-tracker.md`.

### Triage labels

Default canonical labels: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context layout — `CONTEXT.md` and `docs/adr/` at repo root. See `docs/agents/domain.md`.

---

## Key References

- **Style:** `.claude/REFERENCE/WRITING-VOICE-AND-STYLE.md` (authoritative)
- **Commands:** `.claude/commands/` | **Agents:** `.claude/agents/`
- **Reference index:** `.claude/REFERENCE/INDEX.md`
- **Packaging:** `tools/PACKAGING_MANDATE.md`
- **Performance data:** See memory files (patterns, analytics, competitor findings)
- **Topic pipeline:** `channel-data/TOPIC-PIPELINE.md`

**Start:** `/greenlight` → `/research --new`
