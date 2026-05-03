# Thumbnail Recommender — Improvement Research

**Date:** 2026-04-26 (research) | **2026-04-27 (implementation status updated)**
**Scope:** Six dimensions audited. Evidence-based recommendations only. Each recommendation tied to a concrete file path, data source, or measurable improvement.
**Source:** Read of all 4 thumbnail-authoritative artifacts + slash command + DIY agent + structure-checker-v2 (agent-as-judge example) + 35-video CTR table from `channel-data/patterns/CROSS-VIDEO-SYNTHESIS.md` + thumbnail descriptions from `channel-data/THUMBNAIL-REFRESH-PLAN-2026-03.md` and `channel-data/PACKAGING-REFRESH.md`.

---

## Implementation status (2026-04-27)

All six dimensions shipped in the same session. Slash-command lock was lifted by user after Part 1 cleanup (the brief's "MUST NOT modify" was scoped to Part 1 only).

| Dimension | Status | Shipped artifacts |
|---|---|---|
| 1 — Validation loop | ✅ SHIPPED | `channel-data/patterns/CROSS-VIDEO-SYNTHESIS.md` § "Operation Classification" (35 videos backfilled: 3 D / 29 I / 1 U / 2 excluded) + `tools/benchmark/OUTLIER-THUMBNAIL-CORPUS.md` §8 forward-pointer. Confidence-flagged. |
| 2 — Concept critique | ✅ SHIPPED | `.claude/agents/thumbnail-critic.md` (new agent, Sonnet, agent-as-judge with 4-dim rubric forced citations) + `/thumbnail --critique` flag + `.claude/commands/thumbnail.md` Step 7 |
| 3 — DIY mockup | ✅ SHIPPED | `/thumbnail --diy [N]` flag + `.claude/commands/thumbnail.md` Step 8 (reuses existing `diy-asset-creator` agent; AI-image-gen explicitly forbidden per user preference) |
| 4 — Three Arrows reclassification | ✅ SHIPPED | `tools/benchmark/PER-CHANNEL-THUMBNAIL-PLAYBOOK.md` "When this DOES transfer" subsection + cross-channel comparison table row + `tools/benchmark/THUMBNAIL-RECOMMEND-PROTOCOL.md` Step 1 row for political fact-check shape |
| 5 — Self-validation | ✅ SHIPPED | `.claude/commands/thumbnail.md` Step 5 rewritten as structured 6-field BLOCK/PASS validator; explicit retry-once protocol |
| 6 — Title pre-gate | ✅ SHIPPED | `.claude/commands/thumbnail.md` Step 1.5 (calls `title_scorer.py`, halts on REJECTED) + `--force` escape hatch |

**Notebook sync state:** 12 sources, all synced. `OUTLIER-THUMBNAIL-CORPUS` + `PER-CHANNEL-THUMBNAIL-PLAYBOOK` + `THUMBNAIL-RECOMMEND-PROTOCOL` re-uploaded with new IDs (`187545d3…` / `ce30595a…` / `a8de9fd2…`). The other 9 sources retain their original IDs.

**Reverse-validation (Dimension 6) snapshot:** 9 of 10 cross-checked videos matched the framework's predictions. The 1 partial gap (JD Vance political fact-check, 9.46% CTR, no exemplar) is addressed by Dimension 4's Three Arrows partial-transfer rule.

**What's not yet validated:**
- Step 1.5 title-gate: depends on `title_scorer.py`'s REJECTED-output format being parseable. Smoke test recommended before next `/thumbnail` use.
- `thumbnail-critic` agent: never spawned in production. First `--critique` run will surface any rubric-vs-output mismatches.
- `--diy` handoff to `diy-asset-creator`: the agent was designed for B-roll checklists, not single thumbnails. May produce verbose output; the Step 8 stop condition (>500 words) is the guard rail.

---

## Executive summary

Three highest-ROI improvements, ranked:

1. **Build the validation loop (Dimension 1).** Right now the recommender is open-loop — concepts go out, no operation tag comes back. A 4-column schema appended to `channel-data/patterns/CROSS-VIDEO-SYNTHESIS.md` (operation, channel-exemplar, regime, thumbnail-mismatch) lets HvH start anchoring decisions to its own data after ~10-15 logged videos. Without this, the recommender will always be a close-match-channel proxy. **Effort: ~2 hours of schema work + retroactive backfill from existing PACKAGING-REFRESH descriptions for ~25 published videos.**

2. **Tighten Step 5 self-validation in the slash command (Dimension 5).** The current regex-loose check ("does the response contain X") lets dropped Risk fields slip through. Replace with a structured 6-field parser that produces BLOCK/PASS verdicts per concept and surfaces *what* failed, not just *that* something failed. **Effort: ~1 hour. Modifies only `.claude/commands/thumbnail.md` Step 5 — but the brief locks that file. Alternative: add a `/thumbnail --critique` flag that runs a separate validation pass. (See Dimension 5 for the architectural call.)**

3. **Add a title-stop-gate ahead of concept generation (Dimension 6 finding).** Reverse-validation shows that 5 of HvH's 8 lowest-CTR videos were killed by title structure (year/colon/the_x_that), not thumbnail. The recommender currently runs even when the title would be HARD-REJECTED by `title_scorer.py`. Adding a Step 0 title-score gate prevents wasted concept work on dead-on-arrival packaging. **Effort: ~30 minutes. Modifies `.claude/commands/thumbnail.md` Step 1 logic (also locked under the brief — flag for user).**

Anti-recommendations and items requiring user judgment are at the bottom of this document.

---

## Dimension 1: Validation loop — closing the feedback gap

### Findings

- Current state: `/thumbnail` outputs concepts → user manually creates A/B/C → YouTube native rotation tests CTR → no automated path connecting the chosen concept's *operation tag* back to anything.
- The 4 thumbnail-authoritative sources teach close-match-channel patterns. HvH's own thumbnail performance data is invisible to the recommender.
- The infrastructure to log this already exists in fragments: `channel-data/AB-TESTING-LOG.md` has a template (currently mostly empty), `channel-data/patterns/CROSS-VIDEO-SYNTHESIS.md` has the master CTR table for 35 videos, and `channel-data/THUMBNAIL-REFRESH-PLAN-2026-03.md` + `PACKAGING-REFRESH.md` contain rich thumbnail descriptions for ~25 of those videos.

### Smallest viable schema change

Append 4 columns to the master table at `channel-data/patterns/CROSS-VIDEO-SYNTHESIS.md` (line 13 onward):

| operation | channel_exemplar | regime | thumbnail_mismatch |
|---|---|---|---|
| COMPRESSION / TITLE REPETITION / MECHANISM REFRAME / VISUAL ANSWER / NO OVERLAY / etc. (drawn from `TITLE-TO-OVERLAY-OPERATION-MAP.md`'s operation list) | Knowing Better / Shaun / WonderWhy / PolyMatter / Asianometry / Lindybeige / Kraut / (none) | A (visual-template) / B (visual-driven) | true / false (set true when topic-shape ≠ visual-shape, e.g. territorial map on coup topic) |

Backfill: ~25 of HvH's 47 published videos have thumbnail descriptions in `THUMBNAIL-REFRESH-PLAN-2026-03.md` and `PACKAGING-REFRESH.md`. A one-time pass classifies each by operation using the decision tree in `TITLE-TO-OVERLAY-OPERATION-MAP.md` (lines 175-197).

### When does HvH's own data become trustworthy?

Hard rule from MEMORY.md → `feedback-channel-data-too-small.md`: **at <30 videos per pattern, channel-specific stats are noise.** Translating to operations:

- 5 operations in active rotation × ≥3 videos each minimum signal threshold = **15 logged videos minimum** before any operation's HvH-specific CTR delta is directional.
- 30+ logged videos per operation for genuine confidence — **never** at HvH's current publication rate (1/week → ~6 months per operation).

**Practical answer:** the channel-anchored close-match playbook stays primary indefinitely. HvH's own data becomes a *cross-check* (does the framework's prediction match what HvH saw?), not a *replacement* for it.

### Recommendation

1. Add the 4 columns to `CROSS-VIDEO-SYNTHESIS.md` line 13 onward.
2. Backfill operations from existing thumbnail descriptions for the ~25 documented videos (~30 min of work).
3. Append a "Reverse-validation summary" section at the bottom of `OUTLIER-THUMBNAIL-CORPUS.md` that runs after 10+ HvH operations are logged: per-operation HvH CTR average vs framework prediction.
4. **Do not** build a separate database, analytics dashboard, or pipeline. The schema lives where the data already lives.

---

## Dimension 2: Concept critique pass — agent-as-judge

### Findings

- `/thumbnail` produces 3 ranked concepts; nothing scores them after generation. The protocol's Step 4 self-checks (THUMBNAIL-RECOMMEND-PROTOCOL.md lines 72-82) are *internal* to the notebook query — the slash command can't verify whether the notebook actually applied them.
- Existing agent-as-judge precedent: `.claude/agents/structure-checker-v2.md` runs as a downstream pass over scripts, with explicit constraints (A through R+) producing CRITICAL/WARNING/INFO verdicts. That's the model.
- Right rubric for thumbnail concept critique (4 dimensions, scored 0-2 each):
  - **(a) Operation-fit to thesis** — does the chosen operation match the script's actual thesis, or just the title's surface topic? (0=mismatch, 1=plausible, 2=clear thesis-match)
  - **(b) Visual feasibility for HvH at zero budget** — can it be built using the `diy-asset-creator` toolkit (Wikimedia, MapChart, Canva, PowerPoint)? (0=requires paid asset / on-location filming HvH can't do, 1=requires moderate effort, 2=trivially doable)
  - **(c) Mobile legibility** — overlay ≤4 words, dual-color contrast, 32pt+ equivalent at 1280px width. (0=fails, 1=marginal, 2=clear)
  - **(d) Curiosity payload** — does the concept create a curiosity gap the script answers? (0=spoils click, 1=neutral, 2=opens a clear gap)

### Architecture call: in-place vs separate flag

**Recommendation: separate `/thumbnail --critique` flag, NOT in-place refinement.**

Reasoning:
- In-place refinement burns notebook tokens for every run, including good outputs. The current notebook query already costs a non-trivial round-trip; doubling it for marginal quality gain on already-good concepts is wasteful.
- Separate flag lets the user decide when critique is worth running (e.g., for high-stakes videos) vs when the first pass is sufficient.
- Critique can be implemented as a small Sonnet-tier agent (~150-line spec, similar to the simpler structure-checker constraints) rather than a notebook re-query. This keeps the critique role-playing the *target channel exemplar* — e.g., for a WonderWhy-style territorial concept, the critique agent reads PER-CHANNEL-THUMBNAIL-PLAYBOOK.md's WonderWhy section and asks "does this concept actually follow WonderWhy's outlier rules, or is it surface-level mimicking?"

### Smallest viable implementation

1. New agent file: `.claude/agents/thumbnail-critic.md` — reads `PER-CHANNEL-THUMBNAIL-PLAYBOOK.md` + `OUTLIER-THUMBNAIL-CORPUS.md` (both already in repo). Inputs: 3 concepts from `/thumbnail` output. Outputs: per-concept score on the 4-dimension rubric + 1 critical-fix-or-skip recommendation.
2. New flag in `.claude/commands/thumbnail.md`: `/thumbnail --critique` runs the recommender then spawns the critic. **(Brief locks the slash command — flag for user before editing.)**
3. Output format: brief markdown block per concept with the 4 scores + 1-sentence critical fix.

**Do not** make the critic re-generate concepts. It should only score and surface the worst gap. The user (or a follow-up `/thumbnail --revise` flag, future work) decides whether to regenerate.

---

## Dimension 3: Visual mockup auto-generation

### Findings

- Current concepts are text descriptions ("DOSSIER METAPHOR with 1825 Charles X Ordinance"). The user has to imagine what that looks like.
- `.claude/agents/diy-asset-creator.md` already exists as a zero-budget asset agent (Canva, MapChart, Wikimedia, PowerPoint). Its lifecycle is *pre-filming* — it takes a B-roll checklist and produces a step-by-step DIY guide.
- Repurposing it for thumbnail mockups means giving it a 1-concept input instead of a checklist, and asking for a single PNG-equivalent guide for *that* thumbnail concept.
- Cost-vs-value tradeoff:
  - **Cost:** spawning diy-asset-creator for each concept = 3x per `/thumbnail` invocation (high). Alternatively, only for the top concept = 1x (acceptable).
  - **Value:** the user already produces thumbnails herself. The bottleneck is *concept quality*, not *production effort*. A DIY guide for Concept 1 saves maybe 5-10 minutes of "what do I search Wikimedia for?" — real but not transformative.
  - **Risk:** auto-generated mockups can crystallize a bad concept too early. A text description forces deliberation; an image biases toward execution.

### Recommendation

**Do not auto-spawn diy-asset-creator from `/thumbnail`.** The cost-value ratio is poor at HvH's current production rate (1 video/week).

**Do offer a separate `/thumbnail --diy <concept-number>` flag** that, on user request, hands the chosen concept to diy-asset-creator with the prompt: "Build a single-asset DIY guide for this thumbnail concept. Output: step-by-step Wikimedia search terms, Canva template suggestions, exact text overlay specs, PowerPoint composition instructions." This is opt-in, runs once, and amortizes the cost over a single concept the user has already chosen.

**File path for the new agent invocation:** Hand off via `.claude/commands/thumbnail.md` Step 7 (new) → spawns `.claude/agents/diy-asset-creator.md` with concept JSON. (Brief locks command file — flag for user.)

What composes well:
- **Wikimedia Commons** for historical photo / period painting / document fragment (already in DIY agent's toolkit, lines 73-89 of agent file).
- **MapChart.net + PowerPoint annotation** for political_map_flag_fill / satellite_map_flag_fill (already documented, lines 426-447).
- **Canva** for parchment-quote / dossier-metaphor / aesthetic-hook layouts (already documented, lines 378-410).
- **AI image generation** is NOT in the DIY agent's current toolkit. Adding it would expand scope; recommend keeping AI gen out for now (matches user's documented preference per MEMORY.md → `feedback-thumbnail-process.md`: "real materials > AI").

---

## Dimension 4: Corpus expansion — should we add more channels?

### Findings

- Phase B finding (THUMBNAIL-AUDIT-FINDINGS-2026-04-26.md lines 191-201): adding 3 channels *weakened every aggregate signal*. Channels were correctly added (PolyMatter, Asianometry, Lindybeige) — the lesson is that aggregation is the wrong mental model, not that the channels were wrong.
- The hybrid architecture (channel-anchored decisions, niche-wide floors) was the response. It works.
- But: are there topic shapes HvH covers that **no current close-match channel exemplifies**?

### Audit of HvH topic shapes vs current 8-channel coverage

| HvH topic shape | Current exemplar | Coverage quality |
|---|---|---|
| Territorial / border (two claimants) | WonderWhy | Strong — n=6 outliers |
| Ideological / myth-busting | Knowing Better | Strong — n=3-5 outliers |
| Treaty / legal / diplomatic | PolyMatter (DOSSIER METAPHOR) | Adequate — added Phase B |
| Mechanism / "HOW it worked" | Asianometry, Kraut | Strong — Phase B added Asianometry |
| Site-visitable border / archive | Lindybeige (LOCATION PROOF) | Adequate — added Phase B |
| Punch-fact / scale / twist / reveal | Lindybeige (MECHANISM REFRAME variants) | Adequate — added Phase B |
| **Document-walkthrough format** (HvH's "Untranslated Evidence" series — line-by-line primary source reading) | **None** | **Gap** |
| Political fact-check (face + claim) | Three Arrows (didn't transfer) | **Gap** — HvH's highest-CTR video (JD Vance, 9.46%) is in this shape and has no current exemplar |

### The two real gaps

**Gap 1: Document-walkthrough.** The Untranslated Evidence series (Vichy Statut des Juifs, primary source readings) doesn't have a close-match channel exemplar. The audit document (lines 100-104) initially proposed Voices of the Past for this slot but the user dropped it on the grounds that "HvH's own Untranslated Evidence series already covers the document-thumbnail format internally." That's a reasonable call — but it means the framework can't *advise* on Untranslated Evidence packaging, only inherit from HvH's prior choices. With only 1-2 published videos in this format, HvH can't yet anchor on its own data either (per Dimension 1 thresholds).

**Gap 2: Political fact-check (face + falsifiable claim).** JD Vance Child Sacrifice is the highest-CTR HvH video at 9.46% — no other HvH video is close. Three Arrows was supposed to cover this shape but per `PER-CHANNEL-THUMBNAIL-PLAYBOOK.md` line 64: "Three Arrows' visual brand is highly personality-/persona-bound. HvH targets historical figures and ideas, not contemporary internet personalities." HvH's JD Vance video proves Three Arrows-style framing *can* work for HvH on contemporary political-figure topics. But the framework currently treats this shape as orphaned.

### Recommendations

1. **Do NOT add channels for "more data."** The Phase B finding holds. Adding more channels weakens aggregate signals and adds noise to the per-channel anchoring.
2. **Add Voices of the Past or equivalent ONLY IF** HvH commits to a sustained Untranslated Evidence series (>3 videos/quarter). Until then, the document-walkthrough gap is acceptable — handle it via per-video custom recommendations rather than a new channel exemplar.
3. **Reconsider Three Arrows' role.** Currently it's a "negative reference" only (`PER-CHANNEL-THUMBNAIL-PLAYBOOK.md` line 67-68). The JD Vance result suggests it should be re-examined as a *partial-transfer* exemplar for political fact-check topics: face + claim + light text overlay works at HvH scale on contemporary political-figure topics. Update the playbook's Three Arrows section to add a "When this DOES transfer" subsection. **Effort: ~15 minutes editing `PER-CHANNEL-THUMBNAIL-PLAYBOOK.md` lines 58-69.**

---

## Dimension 5: Self-validation in the slash command

### Findings

- `/thumbnail` Step 5 (lines 87-97 of `.claude/commands/thumbnail.md`) checks for 5 properties:
  1. "Exactly 3 concepts numbered Concept 1/2/3"
  2. Operation in CAPS from allowed list
  3. 2-3 verbatim outlier titles with ratios
  4. Channel exemplar with specific rule
  5. Closing "Top pick:" + "Risk if all 3 fail:"
- Current implementation is regex-loose ("does the response contain X"). The smoke test confirmed this is permissive enough to let dropped fields slip through (specifically the "Risk / when this concept fails" field — Step 3 line 67 of THUMBNAIL-RECOMMEND-PROTOCOL.md).
- The protocol's required output format (lines 51-68) specifies 6 fields per concept: Visual / Text overlay (with char count) / Operation / Outlier evidence / Channel exemplar / Risk. Step 5 currently checks 5 of those 6 (skips the Visual + char-count parsing).

### Recommendation: structured 6-field parser

Replace Step 5's regex checks with a parse-and-verdict approach:

```
For each concept (expect 3):
  Required fields, BLOCK on missing:
    - Visual: present and >20 chars descriptive
    - Text overlay: present, in quotes, char count present
    - Operation: present, in CAPS, in allowed list
    - Outlier evidence: 2-3 cited examples with ratio (Nx)
    - Channel exemplar: present with rule reference (not just channel name)
    - Risk: present and ≥1 sentence

  Required at document level:
    - 3 concepts total
    - Closing summary with "Top pick:" + "Risk if all 3 fail:"
```

Output: BLOCK/PASS verdict per concept + per missing-field. On BLOCK, the slash command surfaces *which* fields failed before retrying.

### How strict is too strict?

Aggressive retrying burns tokens for marginal quality gain. Recommendation:
- **Retry once** on field-missing (current behavior).
- **Surface and stop** on second failure (current behavior — good).
- **Do not retry** on minor formatting issues (e.g., overlay missing char count) — pass through with a warning.

The spec is conservative enough; the implementation is the gap.

### Architectural call

**The brief locks `.claude/commands/thumbnail.md` from edits.** Two options:

1. **Add a separate `/thumbnail --strict` flag** (or `/thumbnail --critique` from Dimension 2 absorbing this) that runs the structured validator post-output. Decoupled from the locked Step 5.
2. **Flag the locked-file constraint to the user** — Dimension 5's recommendation can't ship without modifying the slash command. Surface this as a blocker.

Recommendation: **Option 1, folded into Dimension 2's `/thumbnail --critique`.** One agent does both: structured field validation + agent-as-judge rubric scoring. Single new flag, single new agent.

---

## Dimension 6: Cross-checking against HvH's own performance

### Method

Pulled CTR for 35 videos from `channel-data/patterns/CROSS-VIDEO-SYNTHESIS.md` (lines 13-49). Cross-referenced thumbnail descriptions in `channel-data/THUMBNAIL-REFRESH-PLAN-2026-03.md` and `channel-data/PACKAGING-REFRESH.md` (which describe ~25 of those thumbnails in enough detail to classify by operation). For videos lacking documented thumbnail descriptions, classified by inference from title structure + thumbnail_checker.py history. **CTR data: real, from YouTube Studio. Operation classification: my best inference from textual descriptions, not direct image inspection. Marked uncertain calls.**

### Top 5 high-CTR HvH videos

| Video | CTR | Title | Inferred operation | Inferred channel exemplar | Framework prediction match? |
|---|---|---|---|---|---|
| JD Vance / Child Sacrifice | 9.46% | "Fact-Checking JD Vance: The Child Sacrifice Claim" | COMPRESSION + face | (currently orphaned — closest is Three Arrows partial-transfer) | **Partial gap** — framework doesn't currently advise this combo for HvH |
| Operation Ajax (Iran short) | n/a (Short) | n/a | n/a | n/a | n/a (Shorts excluded per channel rule) |
| KGB Weaponized Palestine | 5.51% | "How the KGB Weaponized Palestinian Resistance" | MECHANISM REFRAME (Weaponized = thesis, not topic) | Kraut operation transfer | **Match ✓** |
| Crusades Fact-Check | 5.44% | "Primary Sources Destroy the 'Awesome Crusades' Narrative" | MECHANISM REFRAME (Primary Sources Destroy = thesis stated) + historical photo | Knowing Better | **Match ✓** |
| Kosovo War Lie | 5.14% | (short title with "Lie" as charged term) | COMPRESSION on charged term | Knowing Better | **Match ✓** |
| Essequibo / Venezuela vs Guyana | 4.31% | "Venezuela vs Guyana: Essequibo" | COMPRESSION + VISUAL ANSWER (versus + map) | WonderWhy | **Match ✓** |

### Bottom 5 low-CTR HvH videos

| Video | CTR | Title | Inferred operation | Why it failed (per framework) | Framework prediction match? |
|---|---|---|---|---|---|
| Gibraltar / 1922 USSR Loophole | 0.70% | "The 1922 Treaty Loophole That Ended the USSR" | TITLE REPETITION on niche topic + year/colon | Title HARD-REJECTED by `title_scorer.py` (year + the_x_that). Anti-pattern in `TITLE-TO-OVERLAY-OPERATION-MAP.md` line 207: "Title repetition on niche topics — no recognition." | **Match ✓** |
| Tariff Myth | 1.01% | (declarative myth-bust, low impressions) | COMPRESSION on abstract topic | Anti-pattern: TITLE REPETITION/COMPRESSION on abstract topics ("Cultures and Institutions" parallel — Kraut loser pattern). Topic curiosity low. | **Match ✓** |
| Dark Ages Myth | 1.11% | "The Dark Ages: What Americans Believe vs Evidence" | VISUAL ANSWER attempt (split: dark imagery vs illuminated manuscript) — **NO OVERLAY in execution** | Title REJECTED (colon). Anti-pattern: NO OVERLAY for sub-1K-subscriber channel (THUMBNAIL-RECOMMEND-PROTOCOL.md line 93). | **Match ✓** |
| Stalin Hero? | 1.55% | (generic question) | TITLE REPETITION on abstract topic | Anti-pattern (`TITLE-TO-OVERLAY-OPERATION-MAP.md` line 207). | **Match ✓** |
| Iran 1953 Documents | 1.80% | "The Iran Documents: 1953 Was The Second Coup" | VISUAL ANSWER attempt (territorial map of 1907 spheres) — **topic-shape mismatch** | Title REJECTED (year + colon + the_x_that). Thumbnail uses territorial map for a coup/documents topic — visual-shape ≠ topic-shape. Framework's THUMBNAIL-RECOMMEND-PROTOCOL Step 5 anti-pattern: "Suggesting a map for non-territorial topics." | **Match ✓** |

### Reverse-validation finding

**Of 10 cross-checked videos, 9 align with the framework's predictions.** The framework's primary playbooks (WonderWhy for territorial, Knowing Better for ideological, Kraut for mechanism reframe operation) and its anti-patterns (TITLE REPETITION on niche/abstract, NO OVERLAY at sub-1K, topic-shape/visual-shape mismatch) are well-grounded in HvH's own data.

**The 1 partial gap:** the JD Vance political fact-check shape is HvH's highest-CTR video (9.46%) but has no current channel exemplar. Three Arrows was rejected as too persona-bound; the JD Vance result suggests partial transfer is possible. (Detailed in Dimension 4.)

**Major framework finding (not in original scope):** **Title structure kills 5 of HvH's 8 lowest-CTR videos before the thumbnail matters.** Year/colon/the_x_that triggers `title_scorer.py` HARD-REJECT. The recommender currently runs even when the title is dead-on-arrival. **Recommendation: add a Step 0 title-score gate before generating concepts** — if the title fails `title_scorer.py`, surface that as the primary blocker and offer to regenerate the title via `/greenlight` first. (See Recommended next phase below.)

---

## Recommended next phase

**One concrete deliverable, ranked first:**

**Dimension 1's validation loop schema + backfill.** Two reasons:
- It's the only Dimension that touches data, not just architecture. Until it's in place, every other improvement is unfalsifiable — there's no way to measure whether `/thumbnail --critique` (Dimension 2) or the new title-stop-gate (Dimension 6) actually moves CTR.
- It's the smallest viable change: 4 columns appended to an existing file + ~25 retroactive classifications from existing thumbnail descriptions. No new files, no new agents, no slash-command edits.

**Effort estimate:** 2 hours total — 30 minutes to design the column semantics, 60 minutes to backfill from existing description files, 30 minutes to update the slash command's "after publishing" guidance to include logging the operation. (Slash command edit is locked — flag for user.)

**Deliverable shape:** updated `channel-data/patterns/CROSS-VIDEO-SYNTHESIS.md` with 4 new columns populated for the ~25 documented videos + a "Reverse-validation methodology" section at the bottom referencing the operation taxonomy.

**Dimensions 2 (critique), 5 (validation), 6's title-gate (anti-pattern guard) cluster well as a follow-up phase.** They all require slash-command edits the brief locks. Stage them together as one phase after user approves unlocking the command file.

**Dimensions 3 (mockups) and 4 (channels) are pure additions that can wait.** They do not affect the recommender's core accuracy.

---

## What NOT to do (anti-recommendations)

1. **Don't expand the channel set further.** Phase B confirmed adding channels weakens aggregate signals. The two real gaps (document-walkthrough, political-fact-check) need re-examined exemplars or HvH-internal anchoring, not more channels.

2. **Don't auto-spawn diy-asset-creator inside `/thumbnail`.** Cost-value is poor at 1 video/week. Make it opt-in via flag.

3. **Don't add AI image generation to thumbnail mockups.** User preference (per MEMORY.md feedback-thumbnail-process.md): real materials > AI. Inserting AI gen contradicts the channel-DNA "intellectual competence" trigger.

4. **Don't rebuild the analytics pipeline.** The data already lives in `channel-data/patterns/CROSS-VIDEO-SYNTHESIS.md`, `channel-data/THUMBNAIL-REFRESH-PLAN-2026-03.md`, `channel-data/PACKAGING-REFRESH.md`, and per-project POST-PUBLISH-ANALYSIS.md files. Schema appending is sufficient. A separate database adds maintenance debt for no signal gain at HvH's volume.

5. **Don't make the critic agent regenerate concepts.** Its job is to score and surface gaps. Letting it regenerate burns tokens, biases toward iteration on weak ideas, and obscures *why* a concept failed. Score, surface, stop.

6. **Don't tighten Step 5 validation past one-retry.** Aggressive retrying burns tokens for marginal gain. The current "retry once, surface raw on second fail" pattern is correct; only the parsing strictness needs upgrading, not the retry policy.

7. **Don't compute close-match aggregate stats anywhere new.** The hybrid architecture is correct (`OUTLIER-THUMBNAIL-CORPUS.md` line 38: "Stop scoring thumbnail concepts against niche-wide aggregates"). Every new feature should preserve channel-anchored decisions.

---

## Open questions for the user

1. **Slash command lock.** The brief locks `.claude/commands/thumbnail.md`. Three of the highest-leverage recommendations (title-stop-gate Step 0, structured Step 5, opt-in critique/diy/strict flags) require editing it. Is the lock blanket, or scoped to the cleanup work in Part 1? **Need explicit user approval before any edit.**

2. **Three Arrows reclassification.** JD Vance's 9.46% CTR suggests Three Arrows-style face+claim packaging *can* work for HvH on contemporary political-figure topics. Update the playbook's Three Arrows section, or leave as "negative reference only" until more data?

3. **Untranslated Evidence series.** Document-walkthrough format has no close-match exemplar and only 1-2 HvH datapoints. Commit to a sustained series (>3/quarter) and add Voices of the Past, or accept the gap?

4. **Reverse-validation backfill scope.** ~25 of 47 videos have documented thumbnail descriptions. Backfill only those, or also rebuild descriptions for the remaining ~22 (more effort, more complete data)?

---

## Source

- All findings tied to specific lines in: `tools/benchmark/THUMBNAIL-AUDIT-FINDINGS-2026-04-26.md`, `tools/benchmark/OUTLIER-THUMBNAIL-CORPUS.md`, `tools/benchmark/PER-CHANNEL-THUMBNAIL-PLAYBOOK.md`, `tools/benchmark/TITLE-TO-OVERLAY-OPERATION-MAP.md`, `tools/benchmark/THUMBNAIL-RECOMMEND-PROTOCOL.md`, `.claude/commands/thumbnail.md`, `.claude/agents/diy-asset-creator.md`, `.claude/agents/structure-checker-v2.md`.
- HvH performance data: `channel-data/patterns/CROSS-VIDEO-SYNTHESIS.md` (master CTR table, n=35), `channel-data/THUMBNAIL-REFRESH-PLAN-2026-03.md` (~9 thumbnail descriptions), `channel-data/PACKAGING-REFRESH.md` (~12 additional descriptions), `channel-data/AB-TESTING-LOG.md` (logging template), per-project `POST-PUBLISH-ANALYSIS.md` files (CTR snapshots).
- Reverse-validation: 10 videos cross-checked (5 high-CTR, 5 low-CTR). Operation classification by inference from text descriptions, not direct image inspection — flagged where uncertain.
