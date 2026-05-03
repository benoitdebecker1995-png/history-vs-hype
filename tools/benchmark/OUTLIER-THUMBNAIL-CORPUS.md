# Outlier Thumbnail Corpus — Close-Match Channels

**Date:** 2026-04-26
**Purpose:** Replace channel-average thumbnail data (which described floors, not winners) with outlier-vs-loser delta data (which describes what actually predicts a 3x+ video). This is the new primary input for the Packaging Intelligence notebook.

**Method:** For each of the 8 close-match channels (Knowing Better, Shaun, Three Arrows, Kraut, WonderWhy + PolyMatter, Asianometry, Lindybeige added 2026-04-26), pull every classified video, compute view ratio against channel median, split into outliers (≥3x median) and content losers (<0.5x, with Q&A/milestone/merch/companion-bonus content removed). 14 non-content videos dropped from raw losers.

**Threshold rationale:** 3x median chosen for signal-to-noise over n. Outlier n=30, loser n=57 across 8 channels.

**Key finding (read first):** Outliers do **not** differ from losers on text-overlay rate (text overlay is a floor every channel meets, not a winning predictor). Outliers differ on **visual concept fit** and **overlay operation**. The differential below is the real rule set.

---

## 1. Aggregate signal differential

### 8-channel close-match (n=30 outliers vs n=57 losers) — UPDATED 2026-04-26

| Signal | Outliers | Losers | Δ | Interpretation |
|---|---|---|---|---|
| `has_map` | 20% | 18% | +2pp | **Maps not predictive in aggregate** — the +19pp from 5-channel disappears when PolyMatter and Asianometry (no-map outliers) are included. Channel-anchored signal. |
| `has_text` | 90% | 96% | **−6pp** | Text overlay floor confirmed at expanded n. |
| `has_face` | 30% | 35% | **−5pp** | Faces slightly hurt on average — but signal is dominated by Lindybeige (face-heavy brand). Channel-anchored. |
| `has_arrows` | 3% | 9% | −6pp | Arrows correlate with losers. |
| `has_icons` | 30% | 33% | −3pp | Icons not predictive in aggregate — the +18pp in the 5-channel was Kraut/WonderWhy specific. |

### Original 5-channel close-match (n=16 outliers vs n=37 losers, kept for comparison)

| Signal | Outliers | Losers | Δ |
|---|---|---|---|
| `has_map` | 38% | 19% | **+19pp** |
| `has_text` | 81% | 95% | **−14pp** |
| `has_face` | 19% | 30% | **−11pp** |
| `has_arrows` | 6% | 14% | −8pp |
| `has_icons` | 56% | 38% | **+18pp** |

**Read this carefully.** Adding 3 new close-match channels (n=14 more outliers, n=20 more losers) **weakened every aggregate signal**. That's not a measurement problem — it's confirmation that **outlier patterns are channel-anchored, not niche-wide**. PolyMatter's outliers don't use maps (counter to WonderWhy). Asianometry's outliers don't use faces (counter to Lindybeige). Lindybeige's outliers don't use icons (counter to Kraut). Averaging contradictions dilutes everything.

**Operational rule:** Stop scoring thumbnail concepts against niche-wide aggregates. Score against the closest channel exemplar's outlier pattern (see PER-CHANNEL-THUMBNAIL-PLAYBOOK.md).

**Floor confirmed:** Text overlay at 90-96% across both groups. It's the floor every channel meets, not a winning predictor. Stop scoring "added text overlay" as a positive — score the *operation the overlay performs* instead (see TITLE-TO-OVERLAY-OPERATION-MAP.md).

---

## 2. Full outlier corpus (≥3x channel median, sorted descending)

Each row tagged with the **overlay operation** the thumbnail performs. See TITLE-TO-OVERLAY-OPERATION-MAP.md for definitions.

| Ratio | Channel | Title | Overlay | Visual | Operation |
|---|---|---|---|---|---|
| 11.3x | Lindybeige | The ancient Roman war engine that could kill you in five different ways | "and they built 300 of them" | illustration of war engine | **MECHANISM REFRAME (scale)** — overlay names the *scale stat* not the topic; numerical shock |
| 9.3x | Lindybeige | Two Brits and a dog in a bunker in Ukraine | "BIGMAC IS BACK AND NOW THERE ARE NO SNIPERS LEFT IN UKRAINE" | creator_costume in war zone | **NARRATIVE BEAT** — overlay narrates the in-video update; full sentence; war-zone B-roll authenticity |
| 7.8x | Kraut | Trump's Biggest Failure | "Ni Hao" | animation (China-coded) | **MECHANISM REFRAME** — overlay names the hidden punchline (China) |
| 7.8x | WonderWhy | Fun Fact About Every Country in the World - Part 1 | "Fun Fact About Every Country in the World Part 1" | satellite world map | **TITLE REPETITION** — title is curiosity-complete; visual = same world |
| 7.7x | Knowing Better | The Part of History You've Always Skipped \| Neoslavery | "Neoslavery" | historical photo | **COMPRESSION** — 10-word title → 1 charged word |
| 7.0x | Lindybeige | On Holiday in a Country at War | "On HOLIDAY in a COUNTRY at WAR" | creator on outdoor location | **TITLE REPETITION + LOCATION PROOF** — creator visibly IN the location the title describes |
| 7.0x | Kraut | How Vodka ruined Russia | "A HISTORY OF SYSTEMIC ADDICTION" | animation | **MECHANISM REFRAME** — vodka → systemic addiction (the actual thesis) |
| 7.0x | Shaun | Harry Potter | "HARRY POTTER" | artwork | **TITLE REPETITION** — title is a cultural touchstone; no compression needed |
| 6.9x | PolyMatter | What Putin Fears More Than War | "WHAT PUTIN FEARS MORE THAN WAR" | document_collage with Putin's eyes | **TITLE REPETITION + DOSSIER METAPHOR** — declassified-document aesthetic frames the click |
| 6.8x | WonderWhy | The Breakup of Yugoslavia | "Breakup of Yugoslavia" | political_map_flag_fill | **TITLE REPETITION + VISUAL ANSWER** — map shows the breakup |
| 6.4x | WonderWhy | Why Ireland Split into the Republic of Ireland & Northern Ireland | "WHY IRELAND SPLIT" | satellite_map_flag_fill | **COMPRESSION + VISUAL ANSWER** — long title → 3 words; map answers it |
| 4.8x | WonderWhy | The Most Complex International Borders in the World - Part 2 | "PAKISTAN, INDIA, CHINA" | satellite_map_color_coded | **COMPRESSION + VISUAL ANSWER** — vague title → specific geographies |
| 4.8x | Lindybeige | A walk around Lviv in wartime | "A Walk Around LVIV in Wartime" | creator on outdoor location | **TITLE REPETITION + LOCATION PROOF** |
| 4.7x | Kraut | The Turkish Century \| From Hittites to Atatürk | "THE TURKISH CENTURY FROM HITTITE TO ATATURK" | animation | **TITLE REPETITION** |
| 4.7x | Lindybeige | Helm's Deep - impregnable fortress or waste of good stone? | "The Many Silly Flaws of HELM'S DEEP" | stock composite (Tolkien fortress) | **MECHANISM REFRAME** — title asks question; overlay answers ("Many Silly Flaws") |
| 4.3x | Lindybeige | A point about Roman war-waggons | "A point about Roman war-waggons" | text_dominant on parchment | **TITLE REPETITION + NO VISUAL** — eccentric brand absorbs no-visual |
| 4.1x | WonderWhy | What's the Difference Between Latino and Hispanic? | "LATINO / HISPANIC" | venn_diagram_flags | **VISUAL ANSWER** — venn diagram answers the question |
| 4.1x | Lindybeige | Drilling through a stone with stone-age technology | "Drilling through stone with BONE" | demonstration (hands working) | **MECHANISM REFRAME (twist)** — title says "stone-age tech"; overlay reveals "BONE" — punchline-first |
| 4.0x | Kraut | India & Pakistan - A continuing Story | (none) | animation | **NO OVERLAY (visual-only)** — Kraut's animation is the brand |
| 3.8x | Lindybeige | Postcard from The Field of Mars - a war cemetery in wartime | "This cemetery is now full" | creator at cemetery (outdoor) | **MECHANISM REFRAME (reveal)** — title is poetic; overlay is the punch fact |
| 3.7x | PolyMatter | The End of Cheap Chinese Labor | "THE END OF CHEAP CHINESE LABOR" | historical_painting (Soviet realism) | **TITLE REPETITION + AESTHETIC HOOK** — Soviet propaganda art reinforces "end of an era" |
| 3.5x | WonderWhy | A Geopolitical Tour of the World | (none) | globe_with_flag_pins | **NO OVERLAY (visual-only)** — globe + flag pins is the story |
| 3.5x | Shaun | The Bell Curve | "THE BELL CURVE" | text_dominant | **TITLE REPETITION** — book title = cultural touchstone |
| 3.4x | Asianometry | Thyristors Did to Power What Transistors Did to Logic | "THE THYRISTOR REVOLUTION" | industrial_photo | **MECHANISM REFRAME** — long analogy title → 3-word category claim |
| 3.3x | Knowing Better | American Exceptionalism but as a Religion \| Mormons | "American Exceptionalism but as a Religion" | creator (in costume) | **TITLE REPETITION (left of pipe)** — left side is the angle, right side is the topic |
| 3.2x | PolyMatter | How College Broke the Labor Market | "HOW COLLEGE BROKE AMERICA" | prop_metaphor (graduation cap on US flag) | **MECHANISM REFRAME (intensified)** — "labor market" → "AMERICA"; broader/sharper claim |
| 3.2x | PolyMatter | China's Fundamental Economic Problem | "PEAK CHINA?" | chart_diagram (overlapping bell curves) | **VISUAL ANSWER + COMPRESSION** — chart IS the answer; overlay compresses to a pop-econ phrase |
| 3.2x | Knowing Better | They Were Just in the Way \| Indian Removal | "Indian Removal" | historical_photo | **COMPRESSION (right of pipe)** — emotional title left, topic right; overlay = topic |
| 3.1x | Shaun | Dropping the Bomb: Hiroshima & Nagasaki | (none) | historical_photo | **NO OVERLAY (visual-only)** — Hiroshima photo is iconic enough |
| 3.0x | Asianometry | Silicon Valley Thinks TSMC is Braking the AI Boom | "IS TSMC KILLING AI?" | factory_photo | **COMPRESSION + ESCALATION** — "braking" → "KILLING"; verb intensified for click |

### Operation distribution among outliers (n=30)

| Operation | Count | % | Notes |
|---|---|---|---|
| **TITLE REPETITION** (incl. variants like "left of pipe", "+ location proof", "+ aesthetic hook", "+ dossier metaphor") | 11 | 37% | Most common — when the title is already curiosity-complete or has a strong visual analog |
| **MECHANISM REFRAME** (incl. variants: scale, intensified, twist, reveal) | 9 | 30% | Up significantly from 5-channel data — Lindybeige and PolyMatter both lean on punch-fact reframes |
| **COMPRESSION** (incl. + visual answer, + escalation) | 7 | 23% | Often paired with another operation |
| **VISUAL ANSWER** (low text) | 2 | 7% | Largely WonderWhy-specific (venn, color-coded map) |
| **NO OVERLAY (visual-only)** | 3 | 10% | Reserved for iconic visuals (Hiroshima, signature animation, globe-flag-pins) |
| **NARRATIVE BEAT** (Lindybeige-specific) | 1 | 3% | New operation found in Lindybeige outliers — overlay narrates an in-video update; full sentence |
| **LOCATION PROOF** (Lindybeige-specific) | 2 | 7% | New operation: creator visibly IN the location/situation the title describes — authenticity proof |

**6 of 30 outliers (20%) have no text overlay or use a "soft" overlay (sub-7-char or ambient).** Within range of the niche-wide loser/no-text rate. The "text overlay mandatory" rule remains a *floor*, not a winning predictor. The decision rule is unchanged: **does the overlay perform an operation the visual can't?** If yes, add it. If no, skip it.

### New operations identified in Phase B (added 2026-04-26)

The 3 new channels surfaced 4 operations that weren't visible in the 5-channel data:

1. **MECHANISM REFRAME (variants)** — splits into 4 sub-types: *scale* (the Roman war engine: "and they built 300 of them"), *intensified* ("labor market" → "AMERICA"), *twist* ("stone-age technology" → "BONE"), *reveal* (poetic title → punch fact). All share: overlay reframes the topic to a sharper or more shocking version.
2. **NARRATIVE BEAT** (Lindybeige) — overlay is a full sentence narrating the in-video status update. Works in ongoing dispatch series. Doesn't transfer to standalone HvH videos.
3. **LOCATION PROOF** (Lindybeige) — creator visibly in the location/situation the title describes. The overlay just repeats the title; the *visual* does authenticity work. HvH could apply: filming the actual disputed border, the document archive, the courthouse — where possible.
4. **DOSSIER METAPHOR** (PolyMatter) — declassified-document aesthetic (folders, paperclips, redactions) framing the topic. Works on geopolitical/intelligence-coded subjects. HvH-relevant for treaty/legal/diplomatic topics.

---

## 3. Content loser corpus (<0.5x channel median, n=57 after filter)

Filtered: dropped 14 non-content videos (Q&As, channel milestones, merch, "Bonus" companion content). The full list of dropped titles is in §5.

**Loser visual signal stats already in §1.** Below: representative losers showing the *failure mode*.

| Ratio | Channel | Title | Overlay | Failure mode |
|---|---|---|---|---|
| 0.08x | WonderWhy | Ukraine's EU Membership Bid Explained | "UKRAINE IN THE EU?" | Topical news ages out; political figure (Zelensky) bundled with map dilutes both |
| 0.17x | Knowing Better | Indigenously Aboriginal Native American Terms \| Indian Removal Bonus | "WTF is an Amerindian?" | Companion content — anchors to parent video |
| 0.17x | WonderWhy | Why the President of France is Prince of Andorra | (full title repeated) | Title-repetition operation but title is *too specific/niche* — no curiosity payload |
| 0.20x | WonderWhy | Do We Really Need Time Zones? | "yes. + city labels" | Question→sarcastic answer kills curiosity — overlay spoils click reason |
| 0.22x | Kraut | The Difference between Cultures and Institutions | "CULTURES AND INSTITUTIONS" | Title repetition on abstract topic — no concrete hook |
| 0.22x | Knowing Better | The War to Save the Buffalo \| Indian Removal Bonus | "Buffalo War" | Companion content + compression on already-niche topic |
| 0.25x | PolyMatter | Are America's Students Falling Behind? | "ARE U.S. STUDENTS FALLING BEHIND?" | **Identical visual template to outliers** — title-repetition on a low-curiosity question topic; same prop_metaphor as their winners. The thumbnail isn't the failure; the topic is. |
| 0.27x | PolyMatter | Why Puerto Rico's Economy Doesn't Work | "HOW PUERTO RICO WENT BANKRUPT" | Same template as outliers (flag-with-landmark + bold overlay) but topic isn't curiosity-rich. **Floor identical to outliers.** |
| 0.30x | PolyMatter | The European Country Putin Stubbornly Refuses to Invade | "THE ONE COUNTRY PUTIN WON'T INVADE" | Strong title operation (compression + curiosity-question) but lost. **Suggests topical/political-news fatigue** — Putin-coded content is saturated for this channel. |
| 0.27x | Asianometry | Looking Back on 2025 | "LOOKING BACK AT 2025" | Year-end retrospective — should arguably be filtered as non-content. |
| 0.33x | Asianometry | South Korea Defied the Gods to Build its Steel Colossus | "THE BIRTH OF POSCO" | Historical retrospective in a channel whose outliers are *contemporary mechanism* (Thyristor revolution, TSMC). Topic timing mismatch. |
| 0.42x | Asianometry | The Great Golden Age of Antibiotics | "THE GOLDEN AGE OF ANTIBIOTICS" | Same — historical retrospective; channel rewards contemporary tech. |
| 0.40x | Lindybeige | Blues Club | "The RULES of BLUES CLUB" | Niche club content; "club" branded losers vs travelogue/historical outliers — clear topic-bucket signal |
| 0.47x | Lindybeige | The rules of HEMA CLUB | "The RULES of HEMA CLUB" | Same niche-club pattern |

### Loser failure-mode taxonomy (updated)

1. **Companion/bonus content** — anchored to a parent video, audience saturated. (Filtered out before this list.)
2. **Topical news / political figures** — ages out fast (Zelensky, Macron). Don't anchor thumbnails to currently-trending figures.
3. **Title-repetition on abstract topics** — "Cultures and Institutions" is a topic word, not a curiosity payload. The operation is right; the topic isn't outlier-shaped.
4. **Question→answer in overlay** — kills the click. "Do We Really Need Time Zones? / yes." spoils the only reason to watch.
5. **Identical template, low-curiosity topic** (PolyMatter signal — new) — the visual template is the channel's *floor*, not the differentiator. Outliers and losers share thumbnail structure. The differentiator is **topic curiosity**, not thumbnail style. *This is the most important Phase B finding for understanding channel-template channels.*
6. **Topic-timing mismatch** (Asianometry signal — new) — Asianometry's outliers are CONTEMPORARY mechanism (Thyristor revolution, TSMC). Losers are historical retrospectives (POSCO 1968, antibiotics history). Same channel, same template — the topic's *time horizon* matters.
7. **Niche-club content** (Lindybeige signal — new) — anything branded as a "club" or recurring meta-content franchise underperforms versus singular topic videos.

---

## 4. Per-channel operation strategy (cross-reference with PER-CHANNEL-THUMBNAIL-PLAYBOOK.md)

| Channel | Outlier operations used | Outlier visuals |
|---|---|---|
| Knowing Better | COMPRESSION (Neoslavery, Indian Removal), TITLE REPETITION | historical_photo + props_objects + creator_costume |
| Shaun | TITLE REPETITION, NO OVERLAY | text_dominant or historical_photo (cultural touchstones) |
| Three Arrows | (no 3x outliers in 31-video sample) | n/a |
| Kraut | MECHANISM REFRAME, TITLE REPETITION, NO OVERLAY | animation (proprietary brand) |
| WonderWhy | COMPRESSION, VISUAL ANSWER, TITLE REPETITION | satellite_map / political_map_flag_fill / venn_diagram_flags |
| **PolyMatter** *(new)* | **TITLE REPETITION + DOSSIER METAPHOR / AESTHETIC HOOK**, MECHANISM REFRAME (intensified), VISUAL ANSWER + COMPRESSION | document_collage, historical_painting, prop_metaphor, chart_diagram |
| **Asianometry** *(new)* | **MECHANISM REFRAME**, COMPRESSION + ESCALATION | industrial_photo, factory_photo (always with bold-text overlay) |
| **Lindybeige** *(new)* | **MECHANISM REFRAME (scale/twist/reveal)**, **NARRATIVE BEAT**, **LOCATION PROOF**, TITLE REPETITION | creator + creator_costume + outdoor_location + demonstration |

### Cross-channel pattern (Phase B finding)

The 8-channel data reveals **two distinct outlier-prediction regimes**:

**Regime A — Visual-template channels** (Kraut, WonderWhy, PolyMatter, Asianometry):
- Channel has a strict visual template (animation style, map style, document-collage aesthetic, industrial-photo style)
- Thumbnail style is the same on outliers and losers — it's the *floor*
- Outlier signal comes from the **topic** (curiosity-rich? contemporary? mechanism-shaped?) and the **operation** (mechanism reframe? compression?)
- *For HvH:* this means the thumbnail style is brand discipline, not packaging strategy. Pick the operation, then apply the brand template.

**Regime B — Visual-driven channels** (Knowing Better, Shaun, Lindybeige):
- Thumbnail visual itself varies and *does* differentiate winners
- Outlier signal comes partly from the visual concept (historical photo of subject vs creator-in-costume vs cultural-touchstone artwork)
- *For HvH:* this means each video gets a fresh visual decision, anchored to topic shape.

**HvH straddles both regimes.** Untranslated Evidence series should follow Regime A (document-overlay template, vary the operation). Standard videos should follow Regime B (fresh visual per topic).

---

## 5. Non-content videos filtered out (excluded from loser stats)

Reason: these don't represent thumbnail performance — they're channel events, milestones, or companion uploads with built-in audience caps.

| Channel | Title | Why excluded |
|---|---|---|
| Knowing Better | Steampunk KB Mission Archive \| SDA Lore Recap | Channel lore content |
| Knowing Better | The All-New King-Sized Knowing Better Notebook | Merch announcement |
| Knowing Better | Geronimo: The Quintessential American Indian \| Indian Removal Bonus | Companion to parent video |
| Knowing Better | The War to Save the Buffalo \| Indian Removal Bonus | Companion to parent video |
| Knowing Better | Indigenously Aboriginal Native American Terms \| Indian Removal Bonus | Companion to parent video |
| Shaun | 300k Q&A! / 100k Q&A! / YouTube Q&A! | Channel milestones |
| Three Arrows | The little 50.000 Subscribers Q&A / The GREAT 10.000+ Subscriber Q&A! / What does THIS Logo mean? - 1.000 Subscriber Q&A | Channel milestones |
| Kraut | A Christmas giveaway with XPPen | Sponsorship/giveaway |
| WonderWhy | WonderWhy Flag Tier List (Bonus Video) | Bonus content |
| **Asianometry** | **Looking Back on 2025** | **Year-end retrospective (informational, low CTR by nature)** |

---

## 6. Source files

- Raw extraction (v2 — 8-channel close-match): `tools/benchmark/_outlier_thumbs_3x_filtered_v2.json` (per-channel + aggregate, threshold 3.0x for outliers, 0.5x for losers, content-only filter applied; n=30 outliers, n=57 losers, n=378 total close-match videos)
- Raw extraction (v1 — 5-channel close-match, kept for delta comparison): `tools/benchmark/_outlier_thumbs_3x_filtered.json`
- Aggregation script: `tools/benchmark/aggregate_outliers_v2.py` (re-runnable when more channels are added)
- New channel extractor: `tools/benchmark/backfill_close_match_2026_04.py` (PolyMatter, Asianometry, Lindybeige extraction)
- Thumbnails classified: `tools/benchmark/thumbnails/<channel>/_classifications.json` (per-thumbnail visual fields, all 8 channels)
- Raw video metadata: `tools/benchmark/raw_data/<channel>.json` (view counts, durations, upload dates)

---

## 7. How to use this corpus

When generating thumbnail concepts for a new HvH video, query the notebook with:

> "I'm making a video titled `<title>` about `<topic>`. The script focuses on `<key element>`. Looking at the OUTLIER THUMBNAIL CORPUS specifically (NOT channel averages), which overlay operation fits — compression, title repetition, mechanism reframe, visual answer, or no overlay? Show me the 3 closest outlier matches by topic shape and replicate their *operation*, not their visual."

The notebook should answer with: (a) the operation, (b) 2-3 outlier examples that used that operation on similar topic shapes, (c) the visual concept that operation needs.

---

## 8. Reverse-validation against HvH's own data (placeholder — recompute after n=10 logged operations)

**Status as of 2026-04-26:** classification backfill complete in `channel-data/patterns/CROSS-VIDEO-SYNTHESIS.md` § "Operation Classification". 35 published videos tagged: 3 documented (D), 29 title-inferred (I), 1 uncertain (U), 2 excluded (Short / Meta).

**Why this section exists:** the corpus above is built on close-match channels — not HvH itself. Once HvH has 10+ post-2026-04-26 videos with verified operation tags, this section should be updated with a per-operation CTR delta (HvH actual vs framework prediction). If a HvH-anchored signal contradicts the close-match playbook, the per-channel rules need a "Mapping to HvH" amendment.

**What to compute when triggered:**
1. Per-operation: average CTR of HvH videos using that operation. Compare to the close-match outliers using the same operation.
2. Per channel exemplar: HvH videos using that exemplar's playbook → average CTR. Confirm or contradict the playbook's transferability.
3. thumbnail_mismatch flag: aggregate CTR of mismatched videos (#31 Iran 1953 is the only one currently). Confirm the framework's anti-pattern rule.

**Don't compute prematurely.** At <10 logged datapoints per operation, signal is dominated by topic-curiosity noise (per `MEMORY.md` → `feedback-channel-data-too-small.md`). Wait.

**Current finding (one-shot from inferred classification):** `tools/benchmark/THUMBNAIL-RECOMMENDER-IMPROVEMENT-RESEARCH.md` Dimension 6 = 9 of 10 cross-checked videos match the framework's predictions. Re-validate with documented-confidence rows when n grows.
