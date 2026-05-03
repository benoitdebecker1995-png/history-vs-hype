# Thumbnail Notebook — Audit Findings

**Date:** 2026-04-26
**Scope:** Audit existing thumbnail data driving the Packaging Intelligence notebook + scope new sources to add (capped at 2-3 close-match channels per direction).
**Method:** Re-extract raw_data + classifications for the 5 close-match channels (Knowing Better, Shaun, Three Arrows, Kraut, WonderWhy), split into outliers (≥2x channel median, n=45) and losers (<0.5x, n=50). Compare against the channel-average findings the current notebook is built on. Test the live notebook with a realistic script→thumbnail prompt.

**Bottom line:** The notebook isn't broken — its inputs are. It's been trained on **channel-average data, not winner-vs-loser data**. The rules it enforces ("text overlay mandatory", "27% face usage", "14% map usage in close-match") describe the *baseline* a channel hits on every video, not the *delta* that separates a 3M-view outlier from a 60K-view dud. That's why the suggestions feel generic — they replicate the median, not the winner.

---

## 1. The single biggest accuracy problem

**Outliers vs losers in close-match channels (n=45 outliers / n=50 losers):**

| Signal | Outliers | Losers | Δ | Current MD claim |
|---|---|---|---|---|
| `has_text` | 82% | **92%** | **−10pp** | "Mandatory — 87% of niche" |
| `has_map` | 29% | 16% | +13pp | "14% in close-match" |
| `has_face` | 29% | 26% | +3pp | "27% in close-match" |
| `has_arrows` | 13% | 12% | +1pp | "Optional, ~12%" |
| `has_icons` | 49% | 32% | +17pp | "Optional, ~14%" |

**Read this carefully:** `has_text` is *higher in losers than in outliers*. Text overlay isn't a winning predictor — it's a **floor**, not a signal. Maps and icons actually do predict winners (+13pp, +17pp). The current notebook rules teach the floor as if it were the ceiling.

**Implication:** Every time the notebook says "add text overlay because 87% of niche uses it", that's true but useless — losers also have it. The advice doesn't differentiate.

---

## 2. The "27% face usage" rule averages contradictions

| Channel | Outlier face % | Loser face % | What it means |
|---|---|---|---|
| Three Arrows | 100% | 0% | Face is THE differentiator |
| Knowing Better | 57% | 38% | Face helps |
| WonderWhy | 20% | 33% | Face hurts |
| Shaun | 14% | 0% | Both low (text-dominant brand) |
| Kraut | 15% | 36% | Face hurts |

The "27% in close-match" group average is the mathematical mean of channels where face is the strongest predictor of winning (Three Arrows) and channels where face actively hurts (Kraut, WonderWhy). Averaging these produces a number that predicts nothing.

**Implication:** "Face usage" is a **brand-anchored decision**, not a niche-wide rule. It belongs in a per-channel playbook, not a corpus average.

---

## 3. The notebook is querying "what's typical", not "what wins"

Tested live notebook with a realistic Haiti debt prompt. The three concepts it returned ("THE RANSOM" on document, Charles X portrait + "EXTORTION", chained ledger + "122 YEARS") are competent but **don't reflect any actual outlier pattern from the 5 close-match channels**.

**Top 6 close-match outliers (sorted by ratio):**

| Ratio | Channel | Title | Overlay | Visual |
|---|---|---|---|---|
| 7.8x | Kraut | Trump's Biggest Failure | "Ni Hao" | animation |
| 7.7x | Knowing Better | The Part of History You've Always Skipped \| Neoslavery | "Neoslavery" | historical_photo |
| 7.0x | Kraut | How Vodka ruined Russia | "A HISTORY OF SYSTEMIC ADDICTION" | animation |
| 6.8x | WonderWhy | The Breakup of Yugoslavia | "Breakup of Yugoslavia" | political_map_flag_fill |
| 6.4x | WonderWhy | Why Ireland Split into the Republic… | "WHY IRELAND SPLIT" | satellite_map_flag_fill |
| 4.7x | Kraut | The Turkish Century \| From Hittites to Atatürk | "THE TURKISH CENTURY…" | animation |

**Pattern the notebook is missing:** outlier overlays are one of three things — (a) radical title compression to a single charged word ("Neoslavery", "Indian Removal"), (b) a *mechanism reframe* of the topic ("A HISTORY OF SYSTEMIC ADDICTION" reframes "vodka"), or (c) the visual *answers the title* (venn_diagram_flags for "Latino vs Hispanic"). The notebook outputs (a) but not (b) or (c) — because those mechanisms aren't named anywhere in the source data.

---

## 4. Loser data is polluted by non-content uploads

8 of the 50 close-match "losers" aren't real content failures — they're Q&As, milestone celebrations, giveaways, or merch announcements:

- "100k Q&A!" / "300k Q&A!" / "10.000+ Subscriber Q&A!"
- "The All-New King-Sized Knowing Better Notebook" (merch)
- "A Christmas giveaway with XPPen"
- "Steampunk KB Mission Archive | SDA Lore Recap" (lore content)
- "YouTube Q&A!"
- "Indigenously Aboriginal Native American Terms | Indian Removal Bonus" (companion content)

**Implication:** Loser-pattern stats are 16% noise. Filter `is_content_video=true` before computing any rule.

---

## 5. Source-coverage gaps (the part the user asked about)

Current 14 channels cover myth-busting (5), animated (3), document/evidence (2), geo (2), different-model (2). **What's missing relative to History vs Hype's actual format (8-12 min talking-head + B-roll, sources, hybrid history/geo):**

| Gap | What's missing | Current coverage |
|---|---|---|
| **Hybrid history/geo, talking-head, mid-length** | HvH's exact format | None — closest is WonderWhy (animated maps) |
| **Mechanism / "HOW it worked" channels** | Channel DNA's HOW>WHY trigger | Partial (Kraut for political mechanism only) |
| **Document-as-thumbnail format** | Untranslated Evidence series equivalent | None |

### Recommended adds (2-3 channels max, per scope)

1. **PolyMatter** (~1.4M subs)
   - Format: 8-15 min talking-head + B-roll, hybrid history/geo/business, primary sources, document overlays
   - Why: Closest format match to HvH that exists at scale. Maps + text overlays + document inserts. Talking head with B-roll cutaways. Same duration band.
   - Expected pattern data: how a hybrid history/geo channel resolves the WonderWhy (map-heavy) vs Knowing Better (object-heavy) split that close-match averaging currently smears.

2. **Asianometry** (~750K subs)
   - Format: 10-20 min, faceless, mechanism/how-it-works (industrial history, supply chain, geopolitics), document-heavy
   - Why: HvH's subscriber trigger is "intellectual competence — proving you understand SYSTEMS, not narratives." Asianometry is the niche exemplar of mechanism-first thumbnails. Fills a gap no current source channel covers.
   - Expected pattern data: thumbnail patterns for HOW/mechanism topics — currently underrepresented.

3. **Voices of the Past** (~1.4M subs)
   - Format: Primary historical documents read aloud with on-screen translation, faceless, document-dominant thumbnails
   - Why: Direct format match to HvH's Untranslated Evidence series. Document-as-primary-visual is currently a 0-channel category in the benchmark.
   - Expected pattern data: ground truth for document thumbnails — currently extrapolated, not measured.

---

## 6. Why the notebook fails at "script + title → winning thumbnail"

Five mechanisms compounding:

1. **Wrong unit of analysis.** Sources describe channel-average prevalence, not outlier delta. The notebook can answer "what does Knowing Better usually do?" but not "what made Neoslavery a 7.7x outlier?"
2. **No outlier corpus.** No source file lists *which specific videos* hit ≥2x with *which specific thumbnail*. Inference is impossible.
3. **No title→overlay mapping rule.** Outliers compress, reframe, or answer. Sources don't name those operations, so the LLM defaults to compression only.
4. **No visual taxonomy granularity.** "Map" is one bit. WonderWhy outliers use 5 distinct map types (`political_map_flag_fill`, `satellite_map_flag_fill`, `venn_diagram_flags`, `globe_with_flag_pins`, `satellite_map_color_coded`). The notebook recommends "use a map" — useless without sub-type.
5. **Channel-average rules suppress channel-anchored signals.** "27% face" averaging Three Arrows (face = winner) with Kraut (face = loser) destroys the actual decision rule.

---

## Build plan (phased — approve before any source generation)

### Phase A — Replace the corpus inputs (highest leverage)

1. Generate **`OUTLIER-THUMBNAIL-CORPUS.md`** for the 5 current close-match channels:
   - Top decile (≥2x median) per channel with full classification: title, ratio, primary_visual sub-type, overlay text, overlay style, face type, narrative function (compression / reframe / answer / topic-word)
   - Bottom decile (<0.5x) **filtered to content videos only** (drop Q&As/milestones/giveaways)
   - Differential summary: outlier % vs loser % per signal
   - Source: `_outlier_thumbs_close_match.json` (already generated, 95 records)

2. Generate **`PER-CHANNEL-THUMBNAIL-PLAYBOOK.md`** — one section per close-match channel with the channel-anchored rule (replaces averaged rules):
   - "Three Arrows: face = winner. 100% of outliers have face, 0% of losers."
   - "Kraut: face hurts. 15% outlier face vs 36% loser face."
   - This is what the LLM actually needs to make per-topic recommendations.

3. Generate **`TITLE-TO-OVERLAY-OPERATION-MAP.md`** — codify the 3 winning operations with worked examples:
   - **Compression** (e.g., "The Part of History You've Always Skipped | Neoslavery" → "Neoslavery")
   - **Mechanism reframe** (e.g., "How Vodka ruined Russia" → "A HISTORY OF SYSTEMIC ADDICTION")
   - **Visual answer** (e.g., "What's the Difference Between Latino and Hispanic?" → venn diagram of flags labelled "LATINO / HISPANIC")

### Phase B — Add 3 new channels to the benchmark

1. Run existing pipeline (`tools/benchmark/extract_channel_data.py`, `download_thumbnails.py`, classify) for: PolyMatter, Asianometry, Voices of the Past. ~50 thumbnails each = 150 new records.
2. Re-run outlier extraction including new channels.
3. Update `THUMBNAIL-NICHE-ANALYSIS.md` with the expanded close-match group (8 channels instead of 5).

### Phase C — Replace notebook sources

1. Delete the older `HvH Packaging Intelligence` (4 sources) — superseded by `Packaging Intelligence — History vs Hype` (9 sources).
2. Replace channel-average sources in `Packaging Intelligence — History vs Hype` with the three Phase A files + the expanded analysis from Phase B.
3. Re-test with the same Haiti debt prompt and 2 others. Compare suggestions against actual outlier patterns.

**Approval gates:**
- After Phase A drafts → user reviews the corpus and per-channel playbook before I touch the live notebook
- After Phase B classification → user reviews 3 new channel patterns before merging into close-match group
- Phase C is a clean swap once A+B are validated

---

## Open questions for the user

1. **Channel selection lock-in:** PolyMatter / Asianometry / Voices of the Past — any veto, or substitution for a channel you watch and rate higher? (Lindybeige and History Time are runners-up.)
2. **Loser filter:** OK to drop Q&As, milestone videos, merch posts, and "Bonus" companion content from loser stats? (Saves ~16% noise.)
3. **Outlier threshold:** I used 2x median. Bumping to 3x gives stronger signal but n drops from 45 to ~20. Which do you want — n or signal-to-noise?
4. **Channel-anchored vs niche-wide rules:** willing to break from "one rule for the whole niche" and store per-channel rules? (This is the biggest mental shift — the corpus stops being a homogeneous pool.)

---

## Files referenced

- Current MD inputs being audited: `tools/benchmark/THUMBNAIL-NICHE-ANALYSIS.md`, `.claude/REFERENCE/THUMBNAIL-EVALUATION-FRAMEWORK.md`, `tools/preflight/thumbnail_checker.py`
- Setup guide: `tools/PACKAGING-NOTEBOOK-GUIDE.md`
- New raw output (this audit): `tools/benchmark/_outlier_thumbs_close_match.json` (45 outliers + 50 losers + 228 total close-match videos)
- Live notebooks tested: `Packaging Intelligence — History vs Hype` (98973069…), `HvH Packaging Intelligence` (8395f534…), `Thumbnail Inspiration — Niche Outliers` (8d9e459b…, created today)

---

# Phase B Addendum (executed 2026-04-26)

**User decisions locked in before execution:**
- Channels: PolyMatter, Asianometry, **Lindybeige** (replaced Voices of the Past — HvH's own Untranslated Evidence series already covers the document-thumbnail format internally)
- Loser filter: approved (drop Q&As/milestones/merch/bonus)
- Outlier threshold: **3x** (signal-to-noise over n)
- Rules architecture: **hybrid** — niche-wide rules as floors, channel-anchored rules as decisions

**What ran:**
1. `tools/benchmark/backfill_close_match_2026_04.py` extracted 50 videos × 3 channels = 150 video-metadata records via yt-dlp (~10 min)
2. `tools/benchmark/download_thumbnails.py` fetched 150 new thumbnails (cached 650 existing)
3. 3 sonnet-model agents in parallel classified 150 thumbnails (~3.5 min)
4. `tools/benchmark/aggregate_outliers_v2.py` re-ran outlier extraction across 8 channels

## Phase B finding 1 — Adding channels weakened every aggregate signal

| Signal | 5-channel Δ (outlier vs loser) | 8-channel Δ | What this means |
|---|---|---|---|
| `has_map` | +19pp | +2pp | Maps signal lived in WonderWhy — PolyMatter and Asianometry kill the average |
| `has_text` | −14pp | −6pp | Text-as-floor confirmed at expanded n |
| `has_face` | −11pp | −5pp | Lindybeige's face-heavy brand cancels Kraut/WonderWhy's face-hurts signal |
| `has_arrows` | −8pp | −6pp | Arrows mildly correlate with losers in both groups |
| `has_icons` | +18pp | −3pp | Icons signal was Kraut/WonderWhy specific — Lindybeige's icon-hurts (-80pp at channel level) flipped the aggregate |

**Read this carefully.** The expected outcome of Phase B was to *strengthen* the niche-wide signal by adding more outliers. Instead, every aggregate signal *weakened*. **This is confirmation that channel-anchored rules are correct and niche-averaging is wrong.** Stop computing close-match aggregate stats. Use per-channel deltas only.

## Phase B finding 2 — Two outlier-prediction regimes exist

The 8 close-match channels split into two distinct regimes for what predicts an outlier:

**Regime A — Visual-template channels** (Kraut, WonderWhy, PolyMatter, Asianometry):
- The thumbnail style is the *channel's brand template*. Outliers and losers look the same.
- Outlier signal = topic curiosity + overlay operation. Style is the floor; topic and operation are the differentiators.
- *PolyMatter is the cleanest example:* "What Putin Fears" (6.9x) and "Doctor Shortage" (0.32x) use identical bold-text + concept-visual templates. Only the topic differs.

**Regime B — Visual-driven channels** (Knowing Better, Shaun, Lindybeige):
- Visual concept varies per video and *does* differentiate winners.
- Outlier signal = operation + concept fit (historical photo vs creator-in-costume vs cultural-touchstone artwork vs creator-on-location).

**HvH straddles both regimes.** Untranslated Evidence series → Regime A (document-overlay template). Standard videos → Regime B (fresh visual per topic).

## Phase B finding 3 — 4 new operations identified

The 3 new channels surfaced operations not visible in the 5-channel data:

1. **MECHANISM REFRAME splits into 4 sub-types** (mostly Lindybeige + Asianometry):
   - *Scale*: "and they built 300 of them" — the shocking number
   - *Twist*: "Drilling through stone with BONE" — the surprise material
   - *Reveal*: "This cemetery is now full" — the punch fact
   - *Intensified/Escalation*: "labor market" → "AMERICA"; "braking" → "KILLING"
2. **LOCATION PROOF** (Lindybeige) — creator visibly in the location/situation. Authenticity is the click. **Highly transferable to HvH** — film at the disputed border, the document archive, the courthouse exterior.
3. **NARRATIVE BEAT** (Lindybeige) — overlay narrates an in-video update for an ongoing dispatch series. **Doesn't transfer to HvH** (no ongoing dispatch series).
4. **DOSSIER METAPHOR** (PolyMatter) — declassified-document aesthetic (folders, paperclips, redactions). **Highly transferable** for HvH treaty/legal/diplomatic videos. Matches the "intellectual competence" subscriber trigger directly.

## Phase B finding 4 — New loser failure modes

3 new failure patterns from the new channels:

5. **Identical template, low-curiosity topic** (PolyMatter signal) — visual template is identical to outliers; the loser signal is **topic curiosity**, not thumbnail style. *Lesson: at scale, a "good thumbnail" doesn't save a low-curiosity topic.*
6. **Topic-timing mismatch** (Asianometry signal) — channel's outliers are CONTEMPORARY mechanism (Thyristors today, TSMC today). Losers are HISTORICAL retrospectives (POSCO 1968, antibiotics history). Same channel, same template — topic time-horizon matters.
7. **Niche-club content** (Lindybeige signal) — "club"-branded recurring content franchises ("RULES of HEMA CLUB", "FINDERS KEEPERS Episode Two") consistently underperform versus singular topic videos.

## Updated source files (Phase B output)

- `tools/benchmark/OUTLIER-THUMBNAIL-CORPUS.md` — updated §1 (8-channel + 5-channel comparison), §2 (added 14 new outlier rows + new operations), §3 (new loser failure modes), §4 (per-channel strategy + two regimes), §5 (added 1 dropped non-content video), §6 (new source paths).
- `tools/benchmark/PER-CHANNEL-THUMBNAIL-PLAYBOOK.md` — added 3 new channel sections (PolyMatter, Asianometry, Lindybeige) + updated cross-channel comparison table + two-regimes section.
- `tools/benchmark/TITLE-TO-OVERLAY-OPERATION-MAP.md` — *not modified*. Operations are stable; new variants documented in OUTLIER-CORPUS §2.
- New: `tools/benchmark/aggregate_outliers_v2.py`, `tools/benchmark/backfill_close_match_2026_04.py`, `tools/benchmark/_outlier_thumbs_3x_filtered_v2.json`.

## Highest-leverage transfers to HvH (post-Phase B)

In priority order, the operations Phase B surfaced that HvH should adopt:

1. **DOSSIER METAPHOR** for treaty/legal/diplomatic videos — document-collage aesthetic with bold-text overlay. Direct fit with channel DNA. Try on the next Bakassi/Sabah/Halaib video.
2. **LOCATION PROOF** when filming on-site is feasible — creator at the actual disputed border or document archive. Authenticity differentiator that no current HvH thumbnail uses.
3. **MECHANISM REFRAME (scale/twist/reveal)** — sharper than plain compression. "Indemnity Forced on Haiti" → "5x THE NATIONAL BUDGET" (scale). "Bakassi Belongs to Cameroon" → "150,000 PEOPLE. NEVER ASKED" (reveal).
4. **AESTHETIC HOOK** for systemic-failure topics — period-appropriate art (Soviet realism for "End of an Era" framings, etc.).

## Phase C readiness check

Phase A (3 corpus files) + Phase B (3 channels added) → ready to swap the live notebook sources when user approves.

**Recommended Phase C steps (await user go-ahead):**
1. Delete the older `HvH Packaging Intelligence` notebook (8395f534…, 4 sources, superseded)
2. In `Packaging Intelligence — History vs Hype` (98973069…), upload the 3 corpus MD files as new text sources, deprecate the old channel-average sources
3. Re-run the same Haiti debt prompt + 2 others (territorial topic, mechanism topic) and compare new outputs against Phase A baseline outputs
4. Sanity check: the new notebook should name the *operation* explicitly and reference at least 2 outlier examples by name in its response

If Phase C goes well, optionally update:
- `tools/preflight/thumbnail_checker.py` — replace 87% text-overlay rule with operation-aware scoring
- `.claude/REFERENCE/THUMBNAIL-EVALUATION-FRAMEWORK.md` — add per-channel-anchored rules section

These are not part of the current scope — flag for later.
