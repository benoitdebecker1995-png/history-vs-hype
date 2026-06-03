# Competitor Research — Packaging / Script / Thumbnail Signals

**Date:** 2026-06-03 · **Source:** `tools/intel/intel.db` (pull dated 2026-05-26, 8 days old)
**Corpus:** 872 videos / 10 tracked channels · 702 longform (≥3 min) · 49 longform outliers
**Outlier =** view_count vs that channel's own rolling baseline (`outlier_ratio`). It measures *what broke out relative to a channel's norm*, not absolute views — so a 5x Kraut video and a 5x RealLifeLore video are both "this beat their usual."

> Scope honesty: intel.db holds **titles, views, duration, topic clusters** → this is **packaging** research. It has **no thumbnail field** and **no transcripts**. Thumbnail patterns live in the separate 650-thumb CLIP corpus (`data-patterns.md`); per-topic script-structure gaps need the `competitor-gap` agent. Both flagged below.

---

## 1. Packaging — the meat

### Outlier hit-rate by channel (longform)
Who breaks out *most often* tells you whose packaging to study:

| Channel | Outliers / longform | Rate | DNA fit |
|---|---|---|---|
| **Kraut** | 9/57 | **16%** | style-match — deep causal chains |
| RealLifeLore* | 8/64 | 12% | geography/maps, same demo |
| Fall of Civilizations | 5/43 | 12% | systems-collapse framing |
| **Knowing Better** | 10/93 | **11%** | forensic / revisionism — closest DNA |
| Shaun | 4/74 | 5% | document-first |
| Johnny Harris | 2/40 | 5% | geopolitics |
| Wendover | 4/100 | 4% | logistics explainer |
| Kings & Generals | 2/51 | 4% | battle narration |
| HistoryMarche | 3/95 | 3% | battle narration |
| Historia Civilis | 2/85 | 2% | minimalist Roman |

\*RealLifeLore (`UCP5...7Ww`) is in the video table but missing from `competitor_channels` — **DB bug, should be re-added** so its outliers get attributed.

**Read:** the *revisionist / ideological-argument* channels (Kraut, Knowing Better) break out 3–4x more often than the *battle-narration* channels (Historia Civilis, HistoryMarche, K&G). That's the lane we're in. Pure chronological "Battle of X" packaging under-converts even on big channels.

### The pipe-subtitle structure is the single strongest portable pattern
`Curiosity Hook | Specific Keyword Topic`

- **24%** of longform outliers use `" | "` vs **12%** of all longform — it's **2x over-represented in winners.**
- It solves *our* exact tension: front-load an emotional/curiosity hook **and** keep the searchable keyword. Examples from the swipe file:
  - `The Part of History You've Always Skipped | Neoslavery` (9.4x)
  - `Playing the Victim | Historical Revisionism and Japan` (7.9x)
  - `They Were Just in the Way | Indian Removal` (4.0x)
  - `Subverting the Narrative | Holocaust Denial and the Lost Cause` (4.1x)
  - `American Exceptionalism but as a Religion | Mormons` (4.0x)

This is a near-perfect fit for our Format-C debunk videos: **left of the pipe = the myth/emotional framing, right of the pipe = the keyword anchor a 515-sub channel needs for search.** Worth A/B testing on #58 / #59.

### First word of outlier titles
`The` (9), `How` (7), `Why` (5) = **43% of outliers** open with one of three words.
- Declarative `The…` leads (matches our packaging mandate: declarative = default, 3.8% CTR).
- `How/Why` = the curiosity-question lane (12/49). Both work; **listicle/number openers do not appear** except Fall of Civ's numbered series (which rides an existing binge audience, not transferable).

---

## 2. Title swipe file — portable archetypes

Strip the subject, keep the *move*. These are the reusable shapes (IDEAS, not mandates — per Rules-Hedge):

1. **Withheld-subject curiosity** — `The Part of History You've Always Skipped`, `You Don't See in 4K`, `Why This Part of Africa is Erased on Every Map`
2. **Audience-indictment** — `What Americans don't understand about X`, `How PragerU Lies to You`
3. **Reframe-as-religion / reframe-as-genre** — `American Exceptionalism but as a Religion`, `If Veterans Ruled the World | Starship Troopers`
4. **Inevitability / process** — `South Africa's Slow, Inevitable March Towards Collapse`, `The Best-Run Dictatorship in History`
5. **Named-mechanism debunk** — `Playing the Victim | Historical Revisionism`, `Subverting the Narrative | Holocaust Denial` ← **closest to our voice**

Archetype #5 + the pipe structure is the highest-DNA-fit combo on the board.

---

## 3. Script / structure signals (from topic clusters)

Among the 49 longform outliers, the dominant cluster tag is **`ideological`** (appears in ~18 of 49, far ahead of `war`, `colonial`, `territorial`). Translation: **argument-driven / myth-busting framing out-breaks pure military or geographic framing** — even on channels built on battles. This is direct external corroboration of our channel thesis ("intellectual competence / debunk > narrative").

What the DB **cannot** tell you: how they structure the script (hook timing, turn placement, evidence stacking). For that, run the `competitor-gap` agent per-topic — it pulls transcripts + Gemini-extracts coverage. Recommend doing this on #58 Kurdistan and #59 I/P specifically, not generally.

---

## 4. Thumbnail — honest gap

intel.db has **no thumbnail data**. I did not analyze thumbnails and won't fake it. Two real routes:
- The **650-thumb CLIP corpus** (`data-patterns.md`) already encodes niche thumbnail formulas (text-overlay 87%, no-face 0%, maps for territorial).
- For *current* competitor thumbnails, the per-channel `/thumbnail` flow pulls the close-match outlier corpus at decision time.

If you want a live thumbnail scrape of these 10 channels' recent uploads, that's a separate build (yt-dlp `--write-thumbnail` + CLIP) — say the word and I'll spec it.

---

## 5. Caution — do NOT copy their duration

Outlier median runtime = **40 min** vs 24 min non-outlier. **Ignore this for our channel.** Their breakouts run long because established audiences binge; our own data (n=47, r=−0.455 duration↔retention, hard 12-min cap) says the opposite for a 515-sub channel. This is the textbook "their audience ≠ our audience" trap — flagging per Apply-Own-Framework. The *packaging* patterns transfer; the *runtime* does not.

---

---

## 6. THUMBNAILS — (from `tools/benchmark/`, CLIP-tagged, dated 2026-05-03)

intel.db has no thumbnails, but a separate corpus does: **~820 competitor thumbnails, 17 channels, outliers filtered at 3x, hand-tagged for face/map/icon/text + overlay operation.** The key insight: **averaging the niche is useless** (Three Arrows: face=winner; Kraut: face=loser — the mean predicts nothing). Rules are **channel-anchored by topic shape**. Match the HvH video to its closest exemplar:

| HvH topic shape | Exemplar | Operation | Visual |
|---|---|---|---|
| Territorial / border | **WonderWhy** | COMPRESSION + VISUAL ANSWER | map w/ flag-fill (sub-type by claimant count) |
| Ideological / myth-bust | **Knowing Better** | COMPRESSION (topic word right of pipe) | historical photo of subject + face |
| Treaty / legal / "intelligence-coded" | **PolyMatter** | TITLE REPETITION + DOSSIER METAPHOR | classified-folder / document collage |
| Mechanism / "HOW it worked" | **Kraut / Asianometry** | MECHANISM REFRAME (name the *thesis*, not the topic) | industrial/diagram (Asianometry replicable) |
| Systemic failure (compound, structural) | **PolyMatter** | AESTHETIC HOOK + intensified overlay | period art |
| Site-visitable border/archive | **Lindybeige** | LOCATION PROOF (creator on location) | outdoor on-site shot |
| Punch-fact / scale / reveal | **Lindybeige** | MECHANISM REFRAME variants (scale/twist/reveal) | demonstration/composite |
| Contemporary figure + falsifiable claim | **Three Arrows (partial)** | COMPRESSION + face | recognizable photo of figure + charged term |
| Iconic cultural touchstone (rare) | **Shaun** | TITLE REPETITION / no overlay | iconic photo alone |

**Two highest-leverage transfers for us:**
- **MECHANISM REFRAME** (most underused): when the title names a topic but the thesis is a mechanism, the overlay should name the *mechanism* — "France Bankrupted Haiti" → `COMPOUND INTEREST FOR 122 YEARS`, not a topic repeat.
- **WonderWhy map-as-answer** for our territorial bread-and-butter: compress title to 3–5 words AND let the map visually answer it, both at once.

Niche-wide floors (assume, don't differentiate): documentary aesthetic, no creator selfie, mobile legibility, contrast. Source: `tools/benchmark/PER-CHANNEL-THUMBNAIL-PLAYBOOK.md`, `OUTLIER-THUMBNAIL-CORPUS.md`, `TITLE-TO-OVERLAY-OPERATION-MAP.md`.

---

## 7. SCRIPTS — (from `tools/benchmark/`, ~200 transcripts read in full, + WAVE 2–8 deep-dives)

Five close-DNA channels (Kraut, Shaun, Knowing Better, Three Arrows, WonderWhy) dissected for opening/structure/sourcing/turn. The transferable findings:

**A. The "Everyone Knows Wrong" move — in 11 of 15 core transcripts.** State what everyone was taught → pause → "still wrong" → reveal. *The single most common opening in the niche.* (Knowing Better Neoslavery: "When was the last slave freed? 1865… Still wrong.")

**B. Tell the wrong version first, in full** (60–120s) as if true, THEN dismantle. Builds the before/after contrast. Shaun (Hiroshima) and Knowing Better are gold standard. → **myth-first framing should be DEFAULT for our debunk videos** (corroborates our own 30.3% vs 22.4% retention finding).

**C. Time-to-topic is brutal.** WonderWhy states the question in sentence 1; Three Arrows names the target in <15s. Only Kraut delays 2–4 min — and he has 1M+ subs to afford it. **At our size, topic keyword must land <30s.**

**D. The "turn" comes early in winners** — Shaun ~2:30, Knowing Better ~1:00. Earlier turn = higher retention. (Matches our 15–25% runtime turn rule.)

**E. Perform citations with credential chains, spoken not just shown:** `[Full name] + [title/why they matter] + [quote]`. This is where our page-number advantage is wasted if it stays on-screen only — Shaun *reads it aloud*. Our edge is real but under-performed.

**F. Named opponents** (Crowder, PragerU) create search demand + adversarial structure. We avoid this by design ("referee not partisan") — but the data says named-target videos out-perform. Worth testing on ideological topics only.

Source: `tools/benchmark/SCRIPT-PATTERN-ANALYSIS.md`, `TRANSCRIPT-STRUCTURE-ANALYSIS.md`, `WAVE-8-SCRIPT-TECHNIQUES.md`. Several of these (myth-first, credential chains, <30s topic) are already encoded in script-writer-v2 — worth a re-audit that they survived to current rules.

---

## Action items
1. **A/B test the pipe-subtitle title** (`Myth framing | Keyword`) on #58 and #59 — strongest *fresh* packaging move here.
2. Thumbnails for #58/#59: #58 (Kurdistan, territorial+ideological) → WonderWhy map-as-answer OR Knowing Better historical-photo; #59 (I/P, treaty/legal) → **PolyMatter dossier metaphor**.
3. **Re-add RealLifeLore** to `competitor_channels` table (attribution bug).
4. **Refresh both corpora** — intel.db pull 8 days old (`python -m tools.intel.refresh`); benchmark thumbnail/script docs ~1 month old.
5. **Run `competitor-gap` per-topic** for #58/#59 — DB/corpus give general patterns; gap agent gives *this-topic* coverage holes.
6. Confirm script-writer-v2 still encodes the myth-first / <30s-topic / credential-chain rules (section 7).
