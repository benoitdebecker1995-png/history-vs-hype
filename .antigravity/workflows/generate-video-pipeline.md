---
name: generate-video-pipeline
trigger: /generate-video-pipeline
description: End-to-end repeatable pipeline for producing one History vs Hype video from topic idea → published asset. Designed for Antigravity multi-agent parallel execution.
agents:
  - content-script
  - fact-check
  - packaging
  - asset
  - analytics
artifact_type: implementation-plan
---

# /generate-video-pipeline — Master Workflow

> **Invocation:**
> ```
> /generate-video-pipeline "topic phrase"
> /generate-video-pipeline --project 56-no-lassos-atlantic-slave-trade-origin-2026
> /generate-video-pipeline --resume <slug>
> ```
> Produces an Antigravity Task List with explicit stage gates. Each agent owns specific files (see `ANTIGRAVITY_MIGRATION.md` § 4 — Agent Ownership Matrix).

---

## Inputs

- `$TOPIC` — natural-language topic ("hijab origins", "atlantic slave trade beginnings"). Required for new projects.
- `$PROJECT_SLUG` — existing folder slug under `video-projects/_IN_PRODUCTION/` or `_READY_TO_FILM/`. Required for `--project` mode.

---

## Stage 0 — Greenlight (Packaging agent, ~10 min)

**Gate:** Pass → Stage 1. Fail → drop topic, propose reframes.

1. Run `python -m tools.discovery.demand "$TOPIC"` — get monthly search volume.
   - **HARD STOP** if < 1,000 searches/mo.
2. Run `python -m tools.production.title_generator "$TOPIC" --count 12` — generate 12 candidate titles.
3. Filter titles through `tools/title_scorer.py`:
   - reject any title containing a year token (–46% CTR)
   - reject any title containing `:` (–28% CTR)
   - reject any title without a *mechanism word* (see `CONTEXT.md`)
4. Run competitor-gap scan: `python -m tools.intel.competitor_patterns --topic "$TOPIC"`.
5. Generate 3 thumbnail concepts via the `thumbnail` skill (DIY-feasible, mobile-legible, no verdict overlay).
6. **Output artifact:** `video-projects/_IN_PRODUCTION/<NN>-<slug>-2026/PACKAGING-CONCEPT.md`
   - 3 ranked title candidates + 3 ranked thumbnail concepts
   - VidIQ score, competition score, mechanism-word audit
   - Greenlight verdict: ✅ proceed / ❌ drop / ⏳ reframe

**Stage-0 exit criterion:** `PACKAGING-CONCEPT.md` exists and the user (or autonomous gate) selects one packaging variant.

---

## Stage 1 — Research Phase 1 (Content/Script agent, ~2–4 h, runs in parallel with Stage 0 Step 5)

**Goal:** map the topic landscape, identify every claim that needs verification.

1. Create project folder: `video-projects/_IN_PRODUCTION/<NN>-<slug>-2026/` if not already present.
2. Generate the 8 standard files (empty stubs):
   - `01-VERIFIED-RESEARCH.md` — single source of truth (with ✅/⏳/❌ markers)
   - `02-SCRIPT-DRAFT.md` — empty
   - `03-FACT-CHECK-VERIFICATION.md` — empty
   - `PROJECT-STATUS.md` — with AUTO-block scaffold
   - `NOTEBOOKLM-SOURCE-LIST.md` — empty
   - `NOTEBOOKLM-PROMPTS.md` — empty
   - `YOUTUBE-METADATA.md` — copy locked packaging concept
   - `_research/` subfolder for raw scraps
3. **Wikipedia + open-web scan** via `wiki-researcher` agent pattern:
   - dispatch a Gemini Flash bulk-read job for the top 5 Wikipedia articles touching the topic
   - extract 15–30 candidate claims into `01-VERIFIED-RESEARCH.md` marked `❓ PHASE-1`
4. **Competitor-gap analysis** via `competitor-gap` agent:
   - fetch 8–12 closest competing videos, extract what they cover, identify *gaps*
   - output: `_research/COMPETITOR-GAPS.md`
5. **Source-list generation** (Tier 1/2/3 academic) — `python -m tools.research.source_list "$TOPIC"`
   - output: `NOTEBOOKLM-SOURCE-LIST.md` with 10–20 university-press books, peer-reviewed articles, primary documents

**Stage-1 exit criterion:** ≥ 20 candidate claims in `01-VERIFIED-RESEARCH.md` (all ❓); source list with ≥ 10 Tier-1 sources.

---

## Stage 2 — Research Phase 2: NotebookLM Verification (Content/Script + Fact-Check agents, ~2 h)

**This is the channel's competitive advantage. Do not skip.**

1. **User uploads** the source list to NotebookLM (manual step — Antigravity surfaces a checklist).
2. **Generate verification prompts** via `notebook-researcher` agent — output: `NOTEBOOKLM-PROMPTS.md`. One prompt per claim cluster (5–8 prompts total).
3. **Run prompts via MCP** (no manual paste required):
   ```
   mcp__notebooklm__notebook_query(notebook_id=<id>, query=<prompt>)
   ```
   Output written directly to `_research/NLM-RAW-<timestamp>.md` by the Content/Script agent.
   Fallback if MCP unavailable: user runs prompts in browser and pastes output manually.
4. **Ingest** via `python -m tools.research.nlm_ingest --project <slug>` — extracts citations + page numbers, updates `01-VERIFIED-RESEARCH.md`:
   - `✅ VERIFIED` if exact quote + page round-trip confirmed
   - `⏳ RESEARCHING` if quote matches but page missing
   - `❌ UNVERIFIABLE` if NLM cannot ground
5. **Thesis discipline check** (`notebook-researcher` agent, Use Case 18):
   - articulate the locked thesis in ≤ 12 words
   - **fail = stop**, return to Step 2 with sharper prompts

**Stage-2 exit criterion (Gate 1):** ≥ 90% of claims marked ✅, ≤ 5% marked ⏳, the rest ❌ or removed. **Blocking.**

---

## Stage 3 — Script Writing (Content/Script agent, ~1–1.5 h, model: Opus)

**Hard rule:** anything not ✅ in `01-VERIFIED-RESEARCH.md` cannot enter the script.

1. **Hook variants** — run `script-writer-v2` agent in `--variants` mode: generate 5 hook candidates, score against title-fulfillment + specificity-bomb pattern (5.4× lift, n=85).
2. **Pick hook** — auto-rank by specificity score; surface top 3 for user confirmation.
3. **Full script draft** — `script-writer-v2` writes `02-SCRIPT-DRAFT.md`:
   - target word count: format-specific — Format A/B = `runtime_sec × 3.3`; Format C (document-heavy) = `runtime_sec × 2.5`
   - turn beat at 15–25% runtime
   - modern relevance touch every ≤ 90 s
   - primary documents flagged with `[ON SCREEN]` cues — **Lane Choreography** rule (Rule 41)
   - every "but actually / loophole / exception" beat establishes baseline first (**Rule 40**)
   - every blockquote round-tripped to NotebookLM (**Rule 42**)
4. **Structure check** — `structure-checker-v2` runs Constraints A–BD audit. Any BLOCK = revise. WARN = surface to user.
5. **Polish pass** — `/polish` skill on locked script (model: Opus). Final AI-pattern scrub.
6. **Teleprompter export** — strip `[ON SCREEN]` and `<!-- ... -->` cues; emit `FINAL-SCRIPT.md` formatted for reading.

**Stage-3 exit criterion:** `FINAL-SCRIPT.md` exists, passes structure-checker Tier-1 mandates, word count within format budget.

---

## Stage 4 — Fact-Check Cross-Verification (Fact-Check agent, ~30 min, runs in parallel with Stage 5)

**Goal:** every claim in `FINAL-SCRIPT.md` traces to `01-VERIFIED-RESEARCH.md` with zero drift.

1. `claims-extractor` agent reads `FINAL-SCRIPT.md`, produces structured claim list with timestamps.
2. `fact-checker` agent cross-references each claim against:
   - `01-VERIFIED-RESEARCH.md` (must have ✅ marker)
   - source-tier hierarchy in `.claude/REFERENCE/fact-checking-protocol.md`
   - exact quote + page number for every blockquote
3. Run simplification detection — `python -m tools.script_checkers /fact-check-simplification` (8 anti-oversimplification rules).
4. **Auditor's edge check** — every on-screen quote must be from primary document, not secondary scholar.
5. **Output:** `03-FACT-CHECK-VERIFICATION.md` with verdict per claim and overall `✅ APPROVED FOR FILMING` or `❌ NEEDS REVISION`.

**Stage-4 exit criterion (Gate 2):** 100% of claims pass; zero ⏳ in published script. **Blocking.**

---

## Stage 5 — Asset Generation (Asset agent, runs in parallel with Stage 4)

1. **Thumbnail final** — `thumbnail` skill regenerates locked concept with primary materials (no AI render unless explicitly approved). Run `thumbnail-critic` for 4-dimension score (operation-fit, DIY-feasibility, mobile-legibility, curiosity-payload).
2. **B-roll plan** — `python -m tools.production.broll --project <slug>` → `BROLL-PLAN.md` with timestamp-mapped visual cues from script's `[ON SCREEN]` tags.
3. **DIY assets** — for any expensive B-roll, dispatch `diy-asset-creator` agent (Canva, MapChart, Wikimedia, PowerPoint templates).
4. **Edit guide skeleton** — `python -m tools.production.editguide --project <slug>` → `EDITING-GUIDE-SHOT-BY-SHOT.md`.

**Stage-5 exit criterion:** thumbnail file in folder; B-roll plan written; all expensive assets have DIY guide or sourced URL.

---

## Stage 6 — Move to _READY_TO_FILM (single atomic step)

When **Gates 1 + 2** both pass and Stage 5 outputs exist:

1. `git mv "video-projects/_IN_PRODUCTION/<slug>" "video-projects/_READY_TO_FILM/<slug>"`
2. Update `video-projects/PROJECT_REGISTRY.md` (auto via `tools/reconcile`).
3. Refresh AUTO block in per-folder `PROJECT-STATUS.md`.
4. Surface to user: *"<slug> is ready. Film when scheduled."*

---

## Stage 7 — Post-Production (Asset agent, after user films)

1. User imports MP4 + auto-transcript.
2. `/fix` skill — subtitle correction pass against `FINAL-SCRIPT.md`.
3. `/editing-guide` skill — segment-by-segment editing playbook from rough-cut SRT.
4. User edits in DaVinci Resolve, exports final MP4.

---

## Stage 8 — Publish + Analytics (Packaging + Analytics agents)

1. `/publish` — generates YouTube metadata package (description, tags, chapters, end-screen plan, A/B title rotation set).
2. User uploads to YouTube; pastes URL into chat.
3. **User says** *"I uploaded <slug>"* → autonomous trigger of `/reconcile <slug>`:
   - moves folder to `_ARCHIVED/published/`
   - updates `analytics.db`
   - prompts user to promote project-memory lessons → `feedback-*.md` before snapshot deletion
4. After 7 days: `/analyze --post-publish <slug>` runs retention audit, traffic-source breakdown, CTR pull from YouTube Studio (manual CSV).
5. `/patterns` updates the cross-video pattern library.

---

## Parallelism Map (Antigravity multi-agent execution)

```
T+0h:  [Packaging] ──── Stage 0 (Greenlight) ────────────┐
                                                         │
T+0h:  [Content]   ──── Stage 1 (Phase 1 research)  ─────┤   ◄── parallel
                                                         │
T+0h:  [Asset]     ──── Stage 5a (thumbnail concepts) ───┘
                              │
                              ▼ (after Stage 0 gate)
T+4h:  [Content]   ──── Stage 2 (NotebookLM Phase 2)  ── waits on user upload
                              │
                              ▼ (Gate 1)
T+8h:  [Content]   ──── Stage 3 (script draft)  ────────┐
                                                        │
T+8h:  [Asset]     ──── Stage 5b (B-roll plan stub) ────┤   ◄── parallel
                                                        │
T+9h:  [Fact-Check]──── Stage 4 (cross-verify) ─────────┘
                              │
                              ▼ (Gate 2)
T+10h: move to _READY_TO_FILM
                              │
                              ▼   (filming day — user-paced)
T+Nd:  [Asset]     ──── Stage 7 (post-production)
T+Nd:  [Packaging] ──── Stage 8 (publish)
T+N+7: [Analytics] ──── Stage 8 (post-publish analysis)
```

**Critical-path serial steps (cannot parallelize):** Stage 0 gate → Stage 2 → Gate 1 → Stage 3 → Gate 2.
**Parallel windows:** Stage 1 ‖ Stage 5a; Stage 3 ‖ Stage 5b ‖ Stage 4-prep.

---

## Failure Modes (auto-pause & surface to user)

| Trigger | Action |
|---|---|
| Demand < 1K/mo at Stage 0 | Halt. Suggest 3 reframes via `competitor-gap`. |
| < 90% ✅ after Stage 2 | Halt. Re-run NotebookLM with sharper prompts. |
| Structure-checker BLOCK at Stage 3 | Halt. Surface specific Tier-1 violation. |
| 100% gate fails at Stage 4 | Halt. Show diff between script and verified research. |
| `/reconcile` finds folder-state drift | Halt. Surface AUTO-block diff before applying. |
| Memory record contradicts current file state | Halt. Re-read file; update memory before continuing. |

---

## Artifact Convention

Each stage emits a verifiable Artifact (Antigravity Task List entry):

```
ARTIFACT: <stage-name>
STATUS:   ✅ | ⏳ | ❌
OUTPUT:   <absolute-path-to-primary-file>
SUMMARY:  ≤ 80 words. What ran, what's next.
GATES:    pass | fail (which gate, why)
```

The next agent in the chain reads `OUTPUT` to pick up.

---

**Manual override:** any stage can be re-run with `--force` — but Gates 1 and 2 cannot be bypassed. They are hard blocks by editorial mandate.
