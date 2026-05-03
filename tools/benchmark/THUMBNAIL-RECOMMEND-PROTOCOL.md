# Thumbnail Recommendation Protocol — House Prompt

**Purpose:** Lock the format and reasoning every thumbnail recommendation must follow when this notebook is queried. Anyone querying this notebook for thumbnail concepts MUST follow this protocol exactly. Do not deviate.

**When to apply:** Any query that asks for thumbnail concepts, ideas, recommendations, or evaluations for a History vs Hype video. The query may be phrased casually ("what thumbnail for this?") or formally — output format is identical.

**Source dependencies (must cite from these):**
- `OUTLIER-THUMBNAIL-CORPUS.md` — the 30 verified outlier thumbnails (≥3x channel median) across 8 close-match channels
- `PER-CHANNEL-THUMBNAIL-PLAYBOOK.md` — channel-anchored decision rules with two-regimes section
- `TITLE-TO-OVERLAY-OPERATION-MAP.md` — the 5 overlay operations + variants

If a query cannot be answered from these sources, say so. Never fabricate outlier examples. Never invent ratios.

---

## Step 1 — Classify the topic shape

Pick ONE primary shape from the table below. If the topic spans two shapes, pick the more specific one and note the secondary shape under "alternative concept."

| Topic shape | Recognized by | Closest exemplar | Default operation |
|---|---|---|---|
| Territorial / border (two claimants) | Two named countries claiming the same area | WonderWhy | COMPRESSION + VISUAL ANSWER (political_map_flag_fill) |
| Territorial / border (disputed / no-man's) | Single area with unclear sovereignty | WonderWhy | COMPRESSION + VISUAL ANSWER (satellite_map_flag_fill) |
| Comparison / distinction | "X vs Y", "difference between" | WonderWhy | VISUAL ANSWER (venn_diagram_flags) |
| Multi-region complex border | 3+ claimants, complex geography | WonderWhy | COMPRESSION + VISUAL ANSWER (satellite_map_color_coded) |
| Ideological / myth-busting | "X was actually Y", "the myth of Z" | Knowing Better | COMPRESSION (historical_photo) |
| Iconic cultural touchstone | Famous treaty, named event recognizable to cold viewer | Shaun | TITLE REPETITION or NO OVERLAY (iconic photo / artwork) |
| Mechanism / "HOW it worked" (replicable visual) | Process, system, supply chain, institutional dynamics | Asianometry | MECHANISM REFRAME or COMPRESSION + ESCALATION (industrial / factory / chart) |
| Treaty / legal / diplomatic / intelligence-coded | Specific document, ruling, declassified record | PolyMatter | TITLE REPETITION + DOSSIER METAPHOR (document_collage / classified-folder aesthetic) |
| Systemic failure (compound interest, structural) | Interest accrual, institutional collapse, structural exploitation | PolyMatter | AESTHETIC HOOK + intensified overlay (period-appropriate art) |
| Site-visitable border / archive / location | Creator can physically visit the place | Lindybeige | LOCATION PROOF (creator on outdoor location) |
| Punch-fact / scale / twist / reveal | Topic has a shocking number, surprise material, or punch fact | Lindybeige | MECHANISM REFRAME variants (scale / twist / reveal) |
| **Political fact-check (contemporary public figure + falsifiable claim)** *(added 2026-04-26)* | Named contemporary politician / commentator + a specific checkable historical or factual claim | **Three Arrows (partial transfer)** | **COMPRESSION** on the charged claim term; visual = recognizable photo of the figure (NOT creator selfie, NOT Three Arrows red X-out brand) |

---

## Step 2 — Generate exactly 3 concepts

Each concept must operate on a DIFFERENT axis of the topic. Do not produce three concepts that all use the same operation. Mix:
- One concept that fits the topic's primary shape (default operation from Step 1)
- One concept that uses MECHANISM REFRAME on the script's actual thesis (the argument behind the title)
- One concept that uses a third operation appropriate to a secondary angle (LOCATION PROOF if site-visitable; VISUAL ANSWER if there's a clean visual primitive; AESTHETIC HOOK if the topic has period-art resonance; etc.)

Rank concepts by predicted CTR for HvH's audience (Males 25-44, evidence-based myth-busting, "intellectual competence" trigger). Concept 1 = highest predicted lift.

---

## Step 3 — Required output format

For EACH of the 3 concepts, output ALL six fields below. Do not omit any. Do not paraphrase the field names.

```
### Concept N: [Short descriptive name — e.g., "The Treaty Dossier" or "The Geographic Answer"]

* **Visual:** [Specific description of the primary visual. Name the asset type: historical_photo / political_map_flag_fill / satellite_map_flag_fill / venn_diagram_flags / document_collage / industrial_photo / period_painting / creator_on_location / etc. Describe composition, color contrast, and any compositing.]

* **Text overlay:** "EXACT OVERLAY TEXT" (character count: N chars)

* **(a) Overlay operation:** **[OPERATION NAME IN CAPS]** — [one-sentence justification: why this operation fits this topic shape, and what it accomplishes that another operation wouldn't]

* **(b) Outlier evidence (cite 2–3 from OUTLIER-THUMBNAIL-CORPUS):**
  - [Channel]: *"[Title]"* — overlay [verbatim overlay] (Nx views) — [why this is a topic-shape match, in ≤15 words]
  - [Channel]: *"[Title]"* — overlay [verbatim overlay] (Nx views) — [why match]
  - [Channel]: *"[Title]"* — overlay [verbatim overlay] (Nx views) — [why match]

* **(c) Channel exemplar (from PER-CHANNEL-THUMBNAIL-PLAYBOOK):** **[Channel name]** — [name the specific decision rule from that channel's section, e.g., "WonderWhy's map-first rule for territorial topics with two claimants" or "PolyMatter's DOSSIER METAPHOR mapped to treaty/legal topics"].

* **Risk / when this concept fails:** [One sentence on what would make this concept underperform — e.g., "fails if the topic is not recognizable as a treaty document on its own; pair with a recognizable framing element"]
```

---

## Step 4 — Self-checks before returning

Before returning the answer, verify each concept passes ALL of:

1. **Operation explicitly named** in CAPS, drawn from this list only: COMPRESSION, TITLE REPETITION, MECHANISM REFRAME (with optional variant: scale / twist / reveal / intensified), VISUAL ANSWER, NO OVERLAY, LOCATION PROOF, NARRATIVE BEAT, AESTHETIC HOOK, COMPRESSION + VISUAL ANSWER, COMPRESSION + ESCALATION, TITLE REPETITION + DOSSIER METAPHOR, TITLE REPETITION + AESTHETIC HOOK, TITLE REPETITION + LOCATION PROOF.
2. **2–3 outlier examples** cited verbatim from OUTLIER-THUMBNAIL-CORPUS with their actual ratios. No invented examples. No generic references like "WonderWhy maps in general."
3. **Channel exemplar** referenced with a specific decision rule from PER-CHANNEL-THUMBNAIL-PLAYBOOK, not just the channel name.
4. **No contradiction** with the per-channel playbook. If your operation+channel pairing differs from the cross-channel comparison table at the bottom of PER-CHANNEL-THUMBNAIL-PLAYBOOK, you must flag the deviation in the Risk field and justify why it's appropriate.
5. **Floor is not the recommendation.** Do not recommend "add a text overlay" as the win — text overlay is the floor (90–96% across both outliers and losers). The win is the operation the overlay performs.
6. **NARRATIVE BEAT** is Lindybeige-specific (ongoing dispatch series). Do NOT recommend NARRATIVE BEAT for HvH — it does not transfer.

---

## Step 5 — Anti-patterns to refuse

If you find yourself producing any of the following, stop and revise:

- **Generic "add bold 2-4 word text overlay" advice** — name the operation that overlay performs.
- **Suggesting a face when the closest channel exemplar's playbook says faces hurt** (Kraut, WonderWhy, Asianometry) — check the per-channel playbook before adding faces.
- **Suggesting a map for non-territorial topics** — maps are WonderWhy-specific signal, not a niche-wide rule. PolyMatter outliers actively avoid maps.
- **Suggesting MECHANISM REFRAME without naming a sharp ≤4-word thesis** — if you can't compress the thesis to ≤4 words, switch to COMPRESSION on the topic.
- **Suggesting NO OVERLAY for a sub-1K-subscriber channel** — risky without brand recognition. HvH is at 515 subs; require an iconic visual or skip this operation.
- **Recommending an operation that contradicts the script's thesis** — if the title says "X was state policy" and the script proves coordinated policy, do NOT recommend an overlay that suggests rogue actors.

---

## Step 6 — Closing summary (mandatory)

After the 3 concepts, end with a 2-line summary:

```
**Top pick:** Concept N. Reason: [single sentence — the topic-shape + operation + exemplar combination that does the most work].
**Risk if all 3 fail:** [What does the failure mode of all 3 concepts share? E.g., "all 3 assume the viewer recognizes 'Bakassi' as a place — if not, retest with a primary visual that anchors geography first"].
```

---

## Notes for the querying agent

- If the query provides a script, prioritize concepts whose operation aligns with the script's thesis (not just the title).
- If the query provides only a title, note "no script provided" and ask for one if the topic shape is ambiguous.
- If the query asks for fewer than 3 concepts, still produce 3 — let the user pick. Three is the minimum decision set.
- If the query asks for more than 3 concepts, produce exactly 3 ranked + a 4th "alternative" if the topic clearly straddles two shapes.
- Do not suggest concepts that require assets HvH cannot produce (e.g., proprietary countryball animation = Kraut). Use Kraut as an *operation* exemplar only.
