# ANTIGRAVITY_MIGRATION.md — Handoff Package

> **Audience:** Fresh Antigravity agent team picking up the History vs Hype workspace from Claude Code.
> **Author:** Claude Opus 4.7 (final state of the Claude Code pipeline, 2026-05-17).
> **Scope:** Architecture, agent role-out, technical debt, and pickup instructions. Does **not** modify execution code.

---

## 0. TL;DR

This workspace produces 8–12 minute evidence-based history videos at 1/week cadence. It currently runs on a Claude Code + Python + NotebookLM + DaVinci Resolve stack with ~25 slash commands and ~11 specialized sub-agents. Migration to Antigravity should preserve the **editorial mandates** (packaging-first, two-phase research, three-phase verified workflow, 12-min cap, Calm Prosecutor voice) and re-platform the **orchestration** onto Antigravity's parallel multi-agent model + 1M-token context + Artifacts system.

**Three files define the new shape:**
1. `WORKSPACE_RULES.md` — load into Antigravity's Rules panel. Hard constraints inherited by every agent.
2. `.antigravity/workflows/generate-video-pipeline.md` — repeatable end-to-end video pipeline.
3. This file — architecture summary + pickup instructions.

---

## 1. Current State of the Repository

### 1.1 What works (preserve)

| Subsystem | Files | Status |
|---|---|---|
| **Slash commands (25)** | `.claude/commands/*.md` | Mature. Each is a markdown spec with model routing, flags, internal calls. Port verbatim to Antigravity workflows. |
| **Specialized agents (11)** | `.claude/agents/*.md` | Mature. Have explicit return contracts (`*.contract.md` siblings). Port to Antigravity agent definitions. |
| **Python tools (`tools/`)** | 60+ Python modules under `pyproject.toml ≥3.11` | Mature. Hatchling build. Optional-extras groups (`[youtube]`, `[discovery]`, `[nlp]`, `[translation]`). Re-use as-is. |
| **Folder lifecycle** | `video-projects/_IN_PRODUCTION/` → `_READY_TO_FILM/` → `_ARCHIVED/published/` | Enforced via `/reconcile` + Routine 6 daily 08:30. |
| **analytics.db** | SQLite, channel-wide truth source | **Real path: `tools/youtube_analytics/analytics.db`** (56 videos, 482 traffic-source rows, 158 daily-channel rows as of 2026-05-17). Root-level `analytics.db` is a 0-byte ghost — ignore it. Read-only from agents. Updated by `/reconcile` and YouTube Analytics API ingest. |
| **NotebookLM workflow** | MCP: `mcp__notebooklm__notebook_list/query/describe` | **Queries now automated via MCP.** Source upload remains manual (one step). `tools/notebooklm_bridge.py` is fallback only. Stage 2 manual bottleneck reduced to: upload sources once → agent queries automatically. |
| **Memory (per-project)** | `C:\Users\Benoi\.claude\projects\d--History-vs-Hype\memory\` | Indexed in `MEMORY.md`. ~30 feedback files. **Migration risk: file path is Claude-Code-specific.** See § 5.3. |
| **Reference docs** | `.claude/REFERENCE/` — 30+ canonical guides (style, fact-check, hooks, thesis, format templates) | Mature. Treat as load-on-demand. |
| **Channel data** | `channel-data/` — patterns, competitor DB, content timeline, niche benchmarks | Reference-only inside agents. |

### 1.2 Data flow (canonical)

```
ideation         ─► /greenlight (Packaging) ─► PASS ─► /research --new (Content)
                                                            │
                                                            ▼
                          01-VERIFIED-RESEARCH.md ◄── Phase 1 (Wikipedia/competitors) [Content]
                                       │
                                       ▼
                          NotebookLM Phase 2 (academic) ◄── [Content + Fact-Check]
                                       │
                                       ▼ Gate 1: ≥90% ✅
                                       │
                          02-SCRIPT-DRAFT.md ◄── /script (Content, model=opus)
                                       │
                                       ▼
                          03-FACT-CHECK-VERIFICATION.md ◄── /verify (Fact-Check)
                                       │
                                       ▼ Gate 2: 100% pass
                                       │
                          FINAL-SCRIPT.md + YOUTUBE-METADATA.md + thumbnail concept
                                       │
                                       ▼  git mv to _READY_TO_FILM/
                                       │
                          filming + DaVinci edit (external, user-driven)
                                       │
                                       ▼
                          /editing-guide → /fix → /publish ─► YouTube upload
                                       │
                                       ▼  user says "I uploaded X"
                                       │
                          /reconcile <slug> ─► _ARCHIVED/published/ + analytics.db
                                       │
                                       ▼
                          /analyze → /patterns → /growth → /next
```

### 1.3 Repository inventory (top-level)

```
d:\History vs Hype\
├── .claude/                     # Claude-Code-specific — port to .antigravity/
│   ├── agents/                  # 11 agent specs (→ Antigravity agents)
│   ├── commands/                # 25 slash command specs (→ Antigravity workflows)
│   ├── REFERENCE/               # 30+ load-on-demand reference docs
│   ├── AGENT-ORCHESTRATION.md   # v9.0 lean-orchestrator spec
│   ├── USER-PREFERENCES.md      # working-style rules
│   └── routines/                # scheduled daily/weekly jobs
├── .antigravity/                # NEW — Antigravity workflows live here
│   └── workflows/
│       └── generate-video-pipeline.md
├── .brain/                      # behavioral knowledge base (cross-project wiki staging)
├── .agents/                     # legacy agent skills (mostly empty)
├── .gemini/                     # Gemini CLI config
├── tools/                       # ~60 Python modules (re-used as-is)
├── video-projects/
│   ├── _IN_PRODUCTION/          # 22 active projects (as of 2026-05-17)
│   ├── _READY_TO_FILM/          # 2 projects (1 hijab, 1 sykes-picot)
│   └── _ARCHIVED/published/     # ~47 published videos
├── channel-data/                # analytics, competitor DB, content timeline
├── transcripts/                 # auto-transcripts from YouTube
├── library/                     # ~2000 source PDFs (Drive mirror in-progress)
├── tests/                       # pytest suite
├── analytics.db                 # 0-byte ghost — IGNORE. Real DB at tools/youtube_analytics/analytics.db
├── CLAUDE.md                    # legacy project instructions (still authoritative)
├── AGENTS.md                    # legacy WARP instructions
├── CONTEXT.md                   # domain glossary (terminology lockdown)
├── GEMINI.md                    # Gemini-specific instructions
├── WORKSPACE_RULES.md           # NEW — Antigravity Rules panel
├── ANTIGRAVITY_MIGRATION.md     # NEW — this file
├── VERIFIED-WORKFLOW-QUICK-REFERENCE.md
├── REFACTOR-PLAN.md             # in-progress refactor (paused; see § 5.5)
└── pyproject.toml
```

---

## 2. Editorial Mandates (do not weaken)

These are the channel's competitive moat. Migration must preserve them.

1. **Packaging-first.** `/greenlight` gates research. Demand < 1K/mo = hard stop. Channel grew through packaging fixes, not content depth.
2. **Two-phase research.** Phase 1 (open web, marked ❓) + Phase 2 (NotebookLM academic verification with page numbers, marked ✅). Phase 2 is non-negotiable.
3. **Three-phase verified workflow.** Research → Script → Cross-Check. Gate 1 (≥90% ✅). Gate 2 (100% script ↔ research match).
4. **Auditor's edge.** Primary documents on screen with page numbers and exact quotes. Scholars are citation-tag support, never the on-screen evidence.
5. **Calm Prosecutor voice.** Emotionally low, intellectually high. Acknowledge the opposing side's strongest point before refuting.
6. **12-minute cap.** r = –0.455 (n=47). Mechanical, not advisory.
7. **Mechanism word in title.** No party-vs-party titles without a mechanism word doing the work.

---

## 3. Why Antigravity (the architectural fit)

| Antigravity feature | Why it helps this workspace |
|---|---|
| **1M-token context window** | The orchestrator can hold the full `MEMORY.md` index + `WORKSPACE_RULES.md` + `CONTEXT.md` + the active project's 8 files simultaneously. Claude Code required aggressive sub-agent delegation (`AGENT-ORCHESTRATION.md` v9.0). |
| **Parallel multi-agent** | Stage 1 (Phase 1 research) ‖ Stage 0 Step 5 (thumbnail concepts) ‖ Stage 5b (B-roll planning) are independent. Today they serialize. |
| **Verifiable Artifacts (Task Lists + Implementation Plans)** | Maps cleanly onto our quality gates. Each Gate produces an Artifact; the next agent picks up the artifact. |
| **Rules panel** | `WORKSPACE_RULES.md` becomes a first-class constraint surface inherited by every agent, instead of a doc that agents must remember to read. |

---

## 4. Agent Role-Out (parallel workloads)

Five specialized roles. **Each owns specific files — no two agents write the same file.**

### 4.1 Content / Script Agent
- **Model preference:** Opus 4.7 (script lock, polish); Sonnet 4.6 (drafting); Gemini Flash (bulk source reads).
- **Owns:** `01-VERIFIED-RESEARCH.md`, `02-SCRIPT-DRAFT.md`, `FINAL-SCRIPT.md`, `_research/`.
- **Reads:** `CONTEXT.md`, `.claude/REFERENCE/WRITING-VOICE-AND-STYLE.md`, `THESIS-DISCIPLINE.md`, `HOOK-PATTERN-LIBRARY.md`, `FORMAT-TEMPLATES.md`, project's `01-VERIFIED-RESEARCH.md`.
- **Tools:** `tools.research.nlm_ingest`, `tools.script_checkers`, `tools.citation_extractor`.
- **Legacy commands wrapped:** `/research`, `/script`, `/polish`, `/learn-from-paper`, `/translate`.

### 4.2 Fact-Check / Data Validation Agent
- **Model preference:** Sonnet 4.6.
- **Owns:** `03-FACT-CHECK-VERIFICATION.md`, `_research/CLAIMS-AUDIT.md`.
- **Reads:** `.claude/REFERENCE/fact-checking-protocol.md`, `FACT-CHECK-SIMPLIFICATION-RULES.md`, project's `01-VERIFIED-RESEARCH.md` and `FINAL-SCRIPT.md`.
- **Tools:** `tools.citation_extractor`, `tools.script_checkers/*`.
- **Legacy agents wrapped:** `claims-extractor`, `fact-checker`, `structure-checker-v2`.
- **Legacy commands wrapped:** `/verify`.

### 4.3 Packaging Agent
- **Model preference:** Sonnet 4.6; Opus 4.7 only for final title-lock + thumbnail-critic synthesis.
- **Owns:** `YOUTUBE-METADATA.md`, `PACKAGING-CONCEPT.md`, thumbnail asset files in project root.
- **Reads:** `tools/PACKAGING_MANDATE.md`, `.claude/REFERENCE/TITLE-GENERATION-PROTOCOL.md`, `.claude/REFERENCE/THUMBNAIL-EVALUATION-FRAMEWORK.md`, channel-wide pattern data in `channel-data/`.
- **Tools:** `tools.discovery.*`, `tools.production.title_generator`, `tools.title_scorer`, `tools.intel.competitor_patterns`, `thumbnail_checker.py`.
- **Legacy commands wrapped:** `/greenlight`, `/thumbnail`, `/retitle`, `/curiosity`, `/comment-mine`, `/publish`.

### 4.4 Asset / Testing Agent
- **Model preference:** Haiku 4.5 (cheap, fast); Sonnet 4.6 for editing-guide synthesis.
- **Owns:** `BROLL-PLAN.md`, `EDITING-GUIDE-SHOT-BY-SHOT.md`, DIY asset specs, subtitle correction outputs, `tests/` runs.
- **Reads:** `FINAL-SCRIPT.md`, `BROLL-PLAN.md`.
- **Tools:** `tools.production.broll`, `tools.production.editguide`, `tools.production.split_screen_guide`, `tools.script_checkers.install_srt`.
- **Legacy agents wrapped:** `diy-asset-creator`, `thumbnail-critic`.
- **Legacy commands wrapped:** `/prep`, `/editing-guide`, `/fix`, `/engage`.

### 4.5 Analytics Agent
- **Model preference:** Sonnet 4.6.
- **Owns:** `channel-data/*` updates, `analytics.db` writes, AUTO-blocks in `PROJECT-STATUS.md` files, `video-projects/PROJECT_REGISTRY.md`.
- **Reads:** `analytics.db`, `_ARCHIVED/published/*/POST-PUBLISH-ANALYSIS.md`, YouTube Analytics API.
- **Tools:** `tools.youtube_analytics.*`, `tools.intel.*`, `tools.reconcile`, `tools.routines`, `tools.benchmark.*`.
- **Legacy commands wrapped:** `/analyze`, `/patterns`, `/growth`, `/next`, `/status`, `/reconcile`.

### 4.6 Coordination rules

- Cross-agent communication = **Artifact handoff**. Every stage emits `OUTPUT: <abs-path>` as the last line of its artifact summary; downstream agent reads that path.
- No agent silently spawns a sub-agent. If delegation is needed, declare it in the Implementation Plan.
- Agents may **read** any file in the project, but must not **write** outside their owned set.
- Locks at the file level — no Git locks needed because ownership is disjoint.

---

## 5. Technical Debt & Broken Logic (look out for)

### 5.1 Memory path is Claude-Code-specific
- Current location: `C:\Users\Benoi\.claude\projects\d--History-vs-Hype\memory\`
- `MEMORY.md` is 26 KB and **already exceeds the 24.4 KB load budget** — context warning was firing pre-migration.
- **Action for Antigravity team:** mirror the directory to a workspace-relative path (e.g., `.antigravity/memory/`) and symlink or copy on first run. Keep `MEMORY.md` index ≤ 200 chars per line; current entries are too long.

### 5.2 Two redundant top-level instruction files
- `CLAUDE.md` (Claude Code), `AGENTS.md` (WARP), `GEMINI.md` (Gemini), and now `WORKSPACE_RULES.md` (Antigravity).
- They overlap heavily on editorial rules.
- **Action:** treat `WORKSPACE_RULES.md` as authoritative going forward. Keep the others for archival reference only — do not edit them.

### 5.3 Slash-command markdown != Antigravity workflow markdown
- `.claude/commands/*.md` use Claude Code's frontmatter (`---\ndescription:\nmodel:\n---`).
- Antigravity workflows expect a different schema (see the example file: `agents:`, `artifact_type:`).
- **Action:** write a one-time adapter script (`tools/migrate/claude_commands_to_antigravity.py`) that translates each command file. Acceptance test: each translated workflow produces the same Artifact output for a synthetic input.

### 5.4 Reconciliation depends on conversation triggers
- `/reconcile <slug>` fires when the user **says** *"I uploaded X."* The trigger lives in the natural-language layer.
- Antigravity needs an equivalent: either (a) keep conversational trigger via a Rule, or (b) add a YouTube webhook listener.
- **Action:** Phase-1 keep the conversational trigger (preserves user habit). Phase-2 evaluate webhook.

### 5.5 In-progress refactor (paused)
- `REFACTOR-PLAN.md` describes an 11-step Claudebase overhaul. Step 5 proof-point passed (2026-05-10). All 5 daily routines deployed. Steps 6–11 untouched.
- **Action:** do NOT resume the refactor inside Claude Code. Re-evaluate which steps remain relevant under Antigravity's model; many will be obsoleted by Antigravity's native capabilities (parallel agents, Artifacts, 1M context).

### 5.6 Known broken / fragile spots

**Confirmed 2026-05-17 during #56 production:**
- `tools/production/parser.py` strips text between double backticks — caused citation blocks wrapped in backticks (`` `[CITATION: ...]` ``) to be eaten during `--package` run. Fix: scrub backticks from script before running parser, or patch the regex. Filed as known issue.
- `tools/discovery/discovery_scanner.py` uses Pyppeteer for YouTube autocomplete — **stealth flags break monthly** as YouTube updates anti-bot. Re-test on first migration day.
- ~~`tools/notebooklm_bridge.py` requires manual upload + paste cycle~~ — resolved. MCP server (`mcp__notebooklm__notebook_query`) automates prompt execution. Only source upload remains manual.
- `tools/youtube_analytics/analytics.db` has concurrent-write risk (Routine 6 08:30 daily + `/reconcile` both write, no mutex). Has not corrupted to date but theoretically unsafe. Root `analytics.db` is a 0-byte ghost — verified 2026-05-17.
- `library/` has ~2000 PDFs in-progress on a Drive mirror. The 3-layer plan (consolidate → Gemini rename → Drive + NLM integration) is at Layer 1. See memory: `project-drive-library.md`.
- ~70% of `CONTEXT.md` is Hijab #52-specific content that should migrate to a per-project `GLOSSARY.md` inside the video folder (flagged at the bottom of `CONTEXT.md`). Cleanup task for first quiet sprint.

### 5.7 Unverified claims floating in active projects
- Several `_IN_PRODUCTION/` projects have ⏳ markers older than 30 days. These should be either re-verified or downgraded to ❌.
- **Action:** Analytics agent runs a `--audit-stale-claims` pass on Day 1 of migration.

---

## 6. Day-One Pickup Instructions (for fresh Antigravity team)

### Step 1 — Bootstrap (30 min)
1. Open the workspace in Antigravity IDE: `d:\History vs Hype\`.
2. **Load `WORKSPACE_RULES.md` into the Rules panel.**
3. Verify Python environment: `python -m pip install -e .[all]` from repo root.
4. Verify `.env` exists with `YOUTUBE_API_KEY`, `ANTHROPIC_API_KEY`, `GEMINI_API_KEY`. Use `.env.example` as template.
5. Smoke-test analytics.db: `python -c "import sqlite3; print(sqlite3.connect('tools/youtube_analytics/analytics.db').execute('SELECT count(*) FROM videos').fetchone())"`. Expected: `(56,)` or higher.

### Step 2 — Mirror memory (15 min)
1. Copy `C:\Users\Benoi\.claude\projects\d--History-vs-Hype\memory\` → `.antigravity/memory/`.
2. Spot-check that 5 random entries open correctly and link targets resolve.
3. Append a line to `.antigravity/memory/MEMORY.md`: `## Migration\n- [Migration handoff](../../ANTIGRAVITY_MIGRATION.md) — 2026-05-17 cutover from Claude Code`.

### Step 3 — Register the 5 agents (1 h)
For each agent in § 4.1–4.5, create an Antigravity agent definition with:
- **Name** = role (Content/Script, Fact-Check, Packaging, Asset, Analytics)
- **Tools** = the listed Python modules
- **Files allowed for write** = the "Owns" set
- **Files allowed for read** = the "Reads" set (everything else readable but not writable)
- **Rules** = inherits `WORKSPACE_RULES.md`

### Step 4 — Register the master workflow (15 min)
Register `.antigravity/workflows/generate-video-pipeline.md` as the canonical pipeline. Verify it appears in the workflow palette.

### Step 5 — Run a synthetic end-to-end test (4 h)
- Pick a known-passed topic from `_ARCHIVED/published/` (e.g., a recent published video).
- Re-run `/generate-video-pipeline` against the same topic in a **scratch project** under `video-projects/_IN_PRODUCTION/_test-antigravity-cutover/`.
- Compare: should Gate 1 + Gate 2 land at the same verdict as the original project's archived files? If yes, migration is operational.
- Delete the scratch project.

### Step 6 — Audit stale ⏳ claims (1 h, Analytics agent)
- Scan all `_IN_PRODUCTION/*/01-VERIFIED-RESEARCH.md` for ⏳ markers > 30 days old.
- Surface to user with recommended re-verify-or-drop verdict per claim.

### Step 7 — Hand off to user (15 min)
- Send the user a one-page recap:
  - Rules panel loaded ✅
  - 5 agents registered ✅
  - Master workflow available as `/generate-video-pipeline` ✅
  - Memory mirrored ✅
  - Smoke test passed ✅
  - Open items: stale ⏳ claims, CONTEXT.md cleanup, library/ Layer 2, paused refactor decision.

---

## 7. Things to Explicitly NOT Do During Migration

- **Do not rewrite the Python tools.** They are mature and tested. Re-use as-is.
- **Do not change the folder lifecycle** (`_IN_PRODUCTION/` → `_READY_TO_FILM/` → `_ARCHIVED/published/`). External docs, README files, and the user's mental model depend on it.
- **Do not change `01/02/03-` filename conventions.** Hardcoded in `tools/citation_extractor.py`, `tools/research/nlm_ingest.py`, `/reconcile`, and ~15 other places.
- **Do not modify `analytics.db` schema.** The YouTube Analytics ingest, `/reconcile`, `/analyze`, and `/patterns` all read it.
- **Do not collapse the 5 agents into a single super-agent** "because Antigravity has 1M context." Parallelism is the point — five independent contexts can run concurrently and each owns a specific file set.
- **Do not delete CLAUDE.md / AGENTS.md / GEMINI.md.** They are historical and still referenced by `WORKSPACE_RULES.md` § 11.
- **Do not skip the synthetic E2E test** in Step 5 above. Migration is not complete until it passes.

---

## 8. Open Questions — RESOLVED 2026-05-17

1. **Memory:** Mirror to `.antigravity/memory/` ✅ DONE. Self-contained in repo; no runtime dependency on Claude Code user path. If a new Claude Code memory file is written, re-run the mirror command.
2. **REFACTOR-PLAN.md steps 6–11:** Re-scope under Antigravity. Do not resume in-place. Evaluate each remaining step against Antigravity's native capabilities (many will be obsoleted by 1M context + parallel agents + Artifacts). Schedule as a dedicated planning session.
3. **`/reconcile` trigger:** Conversational trigger only for now. YouTube webhook = Phase 2 decision.
4. **CONTEXT.md cleanup** (Hijab-specific content → per-project GLOSSARY.md): schedule for first quiet sprint.
5. **`library/` Layer 2** (Gemini-rename of ~2000 PDFs): Antigravity agent. See `ANTIGRAVITY_MIGRATION.md` § 10 appendix for asset agent scope — add library renaming as a sub-task.

---

## 9. Success Criteria for Migration

- ✅ One full video produced end-to-end through Antigravity (`/generate-video-pipeline`) hits both quality gates.
- ✅ `/reconcile` correctly archives a published video on user trigger.
- ✅ Routine 6 daily 08:30 backstop continues to fire (or is replaced by Antigravity scheduler).
- ✅ Synthetic E2E re-run of a known-passed archived topic reaches identical verdicts.
- ✅ All 5 agents stay within their write-ownership boundaries during a full pipeline run.
- ✅ User reports the channel-publish cadence (1/week) is unchanged or improved.

---

## 10. Appendix — Legacy Command → Agent Mapping (full)

| Claude Code command | New owning agent | Notes |
|---|---|---|
| `/greenlight` | Packaging | Pre-work viability gate |
| `/research` | Content/Script | Phase 1 + project setup |
| `/script` | Content/Script | Model = Opus |
| `/verify` | Fact-Check | Gate 2 |
| `/prep` | Asset | Edit/B-roll prep |
| `/thumbnail` | Packaging | 3 concepts, ranked |
| `/publish` | Packaging | YouTube metadata package |
| `/fix` | Asset | Subtitle correction |
| `/engage` | Asset | Comment responses |
| `/polish` | Content/Script | Final AI-pattern scrub |
| `/status` | Analytics | What should I do? |
| `/reconcile` | Analytics | Folder + DB state |
| `/analyze` | Analytics | Post-publish audit (long-form only) |
| `/patterns` | Analytics | Cross-video pattern analysis |
| `/growth` | Analytics | Channel dashboard |
| `/retitle` | Packaging | Underperformer rescue |
| `/next` | Analytics | Topic recommendation |
| `/help` | (any) | Phase-organized menu |
| `/refactor` | (paused — see § 5.5) | REFACTOR-PLAN.md step runner |
| `/learn-from-paper` | Content/Script | NotebookLM academic article mining |
| `/translate` | Content/Script | Untranslated-Evidence series |
| `/gemini` | (utility) | Bulk-read dispatcher |
| `/comment-mine` | Packaging | Demand measurement via comments |
| `/editing-guide` | Asset | Rough-cut → editing playbook |
| `/curiosity` | Packaging | Title psychology eval |

| Claude Code agent | New owning agent | Notes |
|---|---|---|
| `article-writer` | Content/Script | Newsletter mode; out-of-scope for video pipeline but stays available |
| `claims-extractor` | Fact-Check | Used in Stage 4 |
| `competitor-gap` | Packaging | Used in Stage 0 + Stage 1 |
| `diy-asset-creator` | Asset | Used in Stage 5 |
| `fact-checker` | Fact-Check | Stage 4 core |
| `notebook-researcher` | Content/Script | Stage 2 |
| `research-organizer` | Content/Script | Optional Stage 2 helper |
| `script-writer-v2` | Content/Script | Stage 3 core |
| `structure-checker-v2` | Fact-Check | Stage 3 structure audit |
| `thumbnail-critic` | Packaging | Stage 0 / Stage 5a |
| `wiki-researcher` | Content/Script | Stage 1 |

---

**End of handoff package.** Three files together (this one + `WORKSPACE_RULES.md` + `.antigravity/workflows/generate-video-pipeline.md`) are sufficient to onboard a new agent team. Everything else is reference. If a future operator can't pick up the workspace from these three files plus `CONTEXT.md`, the handoff has failed and these docs need a refresh.
