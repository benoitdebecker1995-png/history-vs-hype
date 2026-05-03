# Per-Channel Thumbnail Playbook — Close-Match Channels

**Date:** 2026-04-26
**Purpose:** Channel-anchored thumbnail decision rules. Replaces the averaged "27% face usage in close-match" style of rule, which was the mathematical mean of channels with opposite face signals (Three Arrows: face = winner. Kraut: face = loser). Averaging contradictions produces a number that predicts nothing.

**How to use:** When the script is being packaged, identify which close-match channel HvH is closest to *for that specific topic shape*, then apply that channel's rule — not the niche-wide average. HvH is a hybrid; different topics map to different exemplars.

**Hybrid rule architecture:**
- **Niche-wide rules act as floors** (assume them; they don't differentiate winners): documentary aesthetic, no creator selfie, mobile legibility, color contrast.
- **Channel-anchored rules drive decisions** (this file): face yes/no, map yes/no, primary visual concept, overlay operation.

---

## Knowing Better (medium=787,808 views, 5 close-match outliers in dataset)

### Outlier signal vs loser signal
| Signal | Outliers (n=3) | Losers (n=3) | Δ | Rule |
|---|---|---|---|---|
| has_face | **100%** | 33% | +67pp | **FACE = WINNER** when face is historical/subject (not selfie) or creator-in-costume |
| has_text | 100% | 100% | 0 | Floor — both have it |
| has_map | 0% | 0% | 0 | Maps not used at outlier level |
| has_icons | 0% | 0% | 0 | Icons not used |

### Decision rule
- **Always include a face** — historical photo of subject, creator in costume, or evocative period photograph
- **Overlay operation: COMPRESSION** — strip the title to the topic word right of the pipe ("Indian Removal", "Neoslavery", "Mormons" — but use the full angle-phrase if it's punchy: "American Exceptionalism but as a Religion")
- **Visual: historical_photo > props_objects > creator_in_costume**
- Channel logo always present (brand discipline; not relevant to HvH)

### Mapping to HvH
- HvH ideological/myth-busting topics: Knowing Better is the closest exemplar. Use historical photo of subject + COMPRESSION-style overlay.
- Example: HvH "Vance Speech" video → Knowing Better-style would be a stark photo of Vance + "American Exceptionalism" or similar single-phrase overlay.

---

## Shaun (median=1,084,176 views, n=3 outliers)

### Outlier signal vs loser signal
| Signal | Outliers (n=3) | Losers (n=4) | Δ | Rule |
|---|---|---|---|---|
| has_text | 67% | 100% | **−33pp** | **TEXT IS NOT THE WIN** — text-heavy thumbnails LOSE here |
| has_face | 0% | 0% | 0 | Faceless |
| has_map | 0% | 0% | 0 | No maps |

### Decision rule
- **Minimal text or no text** — Shaun's outliers include the unadorned "Hiroshima photo" (no text) and "THE BELL CURVE" (book title repetition only). Loser thumbnails over-explain.
- **Overlay operation: TITLE REPETITION on cultural touchstones** ("Harry Potter", "The Bell Curve") — works only when the title alone is a click magnet
- **Visual: artwork or historical_photo** (iconic moment/object only — not generic period imagery)
- **Brand: clean and understated** — Shaun's signature

### Mapping to HvH
- HvH's "iconic-moment" topics map here (Hiroshima, Bell Curve, etc.). When the topic itself is a recognizable cultural anchor, restrain the overlay — let the visual carry it.
- Example: an HvH video on a famous treaty (Versailles, Tordesillas, Lateran) → Shaun-style would be the document or famous painting alone, with no overlay or just the treaty name.
- **Counter-rule for HvH:** Most HvH topics are *not* household names (Bir Tawil, Bakassi, Halaib). For those, Shaun's TITLE-REPETITION-only model fails. Only use this when the topic IS the click.

---

## Three Arrows (median=546,167 views, n=0 outliers at 3x in 31-video sample)

### Outlier signal
**No outliers at 3x threshold in the 31-video sample.** At 2x threshold (less reliable n=3): 100% face, 100% stock-photo face, 67% icons. The brand is "target's face + red arrow X-out" but at 3x it doesn't appear in the dataset.

### Decision rule
- **Limited applicability for HvH** — Three Arrows' visual brand (target's face + debunking marker) is highly personality-/persona-bound. HvH targets historical figures and ideas, not contemporary internet personalities, so the X-out-on-pundit pattern doesn't transfer.
- **What does transfer:** Three Arrows' losers ALL have text overlay (100%) and 0% face. The pattern that loses at Three Arrows mirrors what HvH should avoid: text-heavy without a clear visual subject.

### Mapping to HvH
- Use Three Arrows as a **negative reference** for general myth-busting topics — text-heavy without a clear visual subject loses there and loses at HvH too.
- Drop from primary playbook rotation for territorial / ideological / treaty topics.

### When this DOES transfer (added 2026-04-26 from HvH reverse-validation)

**HvH's highest-CTR video to date is JD Vance / Child Sacrifice at 9.46% CTR** — Three Arrows-style packaging on a contemporary political-figure topic. The Three Arrows pattern *does* transfer to HvH on a narrow topic shape:

**Topic shape that fits:** contemporary political figure or public commentator + a specific falsifiable historical claim. The viewer recognizes the figure; the claim creates curiosity; the face anchors the visual.

**Operation:** COMPRESSION on the charged claim term. **Visual:** recognizable photo of the figure (NOT a creator selfie). **Overlay:** the charged term from the claim ("CHILD SACRIFICE", "OPERATION X", etc.) — NOT a debunking X-out marker (that's Three Arrows-specific brand).

**Why partial transfer, not full:**
- Use the *operation* (face + COMPRESSION on charged claim).
- Do NOT use Three Arrows' *visual brand* (red X-out, sneer-frame stock photo).
- Do NOT use this for general myth-busting topics where no specific public figure is being checked — those still route to the Knowing Better playbook (historical photo + COMPRESSION).

**Confidence:** n=1 in HvH's data (JD Vance, 9.46% CTR; Armenian Genocide / Trump 3.84% is a weaker secondary). Re-validate after 3+ political-fact-check videos publish. Treat as directional, not locked.

**Anti-pattern:** don't pair a face with a niche topic the audience can't anchor to. The face works because Vance is a known figure with a checkable claim. A historical figure unknown to the cold viewer (e.g., a 19th-century scholar) does NOT trigger this rule — route those to Knowing Better's historical-photo playbook.

---

## Kraut (median=685,859 views, n=4 outliers)

### Outlier signal vs loser signal
| Signal | Outliers (n=4) | Losers (n=13) | Δ | Rule |
|---|---|---|---|---|
| has_face | **0%** | 38% | **−38pp** | **FACE HURTS** — counter-rule to Knowing Better |
| has_icons | 75% | 31% | +44pp | Icons (flag badges, country symbols) lift |
| has_map | 25% | 8% | +17pp | Maps used moderately |
| has_text | 75% | 85% | −10pp | Text not differentiating |

### Decision rule
- **No face, never** (illustrations of countryballs are still "face" by classifier — those LOSE)
- **Country symbols / flag icons / animated geo-shapes** — Kraut's brand is countryball animation. The icon-as-visual is the differentiator.
- **Overlay operation: MECHANISM REFRAME** ("How Vodka ruined Russia" → "A HISTORY OF SYSTEMIC ADDICTION") or NO OVERLAY (when animation is iconic enough)
- **Visual: animation** (proprietary; not directly replicable for HvH)

### Mapping to HvH
- HvH can't replicate countryball animation, so don't treat Kraut's *visual* as a model.
- **What DOES transfer:** Kraut's MECHANISM REFRAME operation. When HvH's title names a topic ("Vodka and Russia") but the actual thesis is a mechanism ("systemic addiction"), the overlay should name the *thesis*, not repeat the *topic*. This is the most underused operation in HvH's current thumbnail thinking.
- Example: HvH "France Bankrupted Haiti" → MECHANISM REFRAME could be "ENFORCED BY GUNBOATS" or "COMPOUND INTEREST FOR 122 YEARS" — names the actual mechanism, not the topic.

---

## WonderWhy (median=964,720 views, n=6 outliers — best signal in dataset)

### Outlier signal vs loser signal
| Signal | Outliers (n=6) | Losers (n=14) | Δ | Rule |
|---|---|---|---|---|
| has_map | **83%** | 43% | **+40pp** | **MAP = DIFFERENTIATOR** |
| has_icons | 100% | 64% | +36pp | Icons (flag fills, color coding) lift |
| has_face | 0% | 36% | **−36pp** | **FACE HURTS** (political figures dominate losers — Macron, Zelensky) |
| has_text | 83% | 100% | −17pp | Text not differentiating |

### Decision rule
- **Map-first, faceless** — political figures kill the thumbnail
- **Map sub-types matter** — outlier maps are NOT generic. They're:
  - `political_map_flag_fill` (countries colored with their flags) — for split/division topics
  - `satellite_map_flag_fill` (satellite imagery + flag overlay) — for territorial topics
  - `venn_diagram_flags` (two flags as overlapping circles) — for comparison topics
  - `globe_with_flag_pins` — for survey/tour topics
  - `satellite_map_color_coded` — for multi-region topics
- **Overlay operation: COMPRESSION + VISUAL ANSWER** — long title compressed to 3-5 words; map *answers* the title visually
- **Avoid political figures** — every loser with a face has a contemporary political figure (Zelensky, Macron, footballer). Historical/abstract works; current-events face does not.

### Mapping to HvH
- **WonderWhy is the strongest exemplar for HvH territorial/border topics.** Use this playbook for: Bir Tawil, Bakassi, Halaib, Essequibo, Sabah, Andorra, Kashmir, Bhutan-China, Belize-Guatemala.
- Match the map sub-type to the topic shape:
  - Border dispute (two claimants): `political_map_flag_fill` — both flags color-fill their claimed territory
  - Disputed/no-man's-land: `satellite_map_flag_fill` with the disputed area marked
  - Comparison (Latino/Hispanic, Cyprus North/South): `venn_diagram_flags`
  - Multi-claimant complex border (Pakistan/India/China): `satellite_map_color_coded`
- **The overlay should compress the title to 3-5 words AND the map should visually answer it.** Both at once. This is the highest-leverage finding.

---

## PolyMatter (median=471,805 views, n=4 outliers — added Phase B)

### Outlier signal vs loser signal
| Signal | Outliers (n=4) | Losers (n=10) | Δ | Rule |
|---|---|---|---|---|
| has_text | 100% | 100% | 0 | Floor — universal |
| has_map | 0% | 30% | **−30pp** | **MAPS HURT** despite topical geo content (counter to WonderWhy) |
| has_face | 25% | 30% | −5pp | Faces neutral — when present, political figure (Putin, Maduro) framed in dossier aesthetic |
| has_icons | 0% | 10% | −10pp | Icons not used at outlier level |

### Decision rule (Regime A — visual-template channel)
- **Visual template is brand discipline, not packaging strategy.** Every PolyMatter thumbnail uses bold black-and-white text in box overlays + a single concept visual + the hexagonal P logo. Outliers and losers share this template.
- The outlier-vs-loser delta is **topic curiosity**, not visual differentiation.
- **Aesthetic hooks that lifted outliers:**
  - **Dossier metaphor** (folders, paperclips, redactions) — frames topic as classified intelligence ("What Putin Fears" 6.9x)
  - **Soviet-realism painting** — frames topic as historical inevitability ("End of Cheap Chinese Labor" 3.7x)
  - **Chart/diagram answering the title** — visual answer paired with a pop-econ catchphrase compression ("PEAK CHINA?" 3.2x)
  - **Prop metaphor with national signifier** (graduation cap on US flag) — for systemic-failure topics ("How College Broke America" 3.2x)
- **What didn't differentiate**: the same flag-with-landmark template was used on outliers and losers. Style isn't the win; topic is.

### Mapping to HvH
- **PolyMatter is the closest format match for HvH** (talking-head + B-roll, 8-15 min, hybrid history/geo, primary sources).
- For HvH videos with clear thesis-shaped topics, copy the operation: bold text overlay + one concept visual + dossier/aesthetic hook for tone.
- **Specific transfers:**
  - HvH treaty/legal/diplomatic videos → DOSSIER METAPHOR aesthetic (folders, classified-document framing, redaction bars). Matches "intellectual competence" subscriber trigger.
  - HvH systemic-failure videos ("France Bankrupted Haiti", "Operation Condor") → AESTHETIC HOOK (period-appropriate art) + intensified overlay
  - HvH chart-answer videos (rare but possible: "How Often Has India and China Actually Fought?") → VISUAL ANSWER + COMPRESSION

### Anti-pattern (PolyMatter losers)
- "Doctor Shortage", "Puerto Rico Bankrupt", "Students Falling Behind" — same template, lower-curiosity topics. **Lesson: at PolyMatter's scale, the template doesn't save a low-curiosity topic.** HvH should heed this — don't expect a "good thumbnail" to lift a topic that has no inherent click magnetism.

---

## Asianometry (median=142,133 views, n=2 outliers — added Phase B)

### Outlier signal vs loser signal
| Signal | Outliers (n=2) | Losers (n=5) | Δ | Rule |
|---|---|---|---|---|
| has_text | 100% | 100% | 0 | Floor — every thumbnail has the green-bar lower-left text |
| has_face | **0%** | 40% | **−40pp** | **FACES HURT** even at small n — historical-figure faces correlate with retrospective topics |
| has_map | 0% | 0% | 0 | Maps not used |

### Decision rule (Regime A — visual-template channel; topic-timing matters)
- **Strict brand discipline:** every Asianometry thumbnail has the deer logo + green-bar topic text in lower-left + Asianometry red bar. Template is fixed.
- The outlier-vs-loser delta is **topic timing**:
  - **Outliers** are CONTEMPORARY mechanism: ongoing tech/industry stories ("Thyristor Revolution" 3.4x, "IS TSMC KILLING AI?" 3.0x)
  - **Losers** are HISTORICAL retrospectives: "Birth of POSCO 1968" (0.33x), "Golden Age of Antibiotics" (0.42x)
- **Operation choices:** outliers use MECHANISM REFRAME (Thyristors → "REVOLUTION") and COMPRESSION + ESCALATION ("braking" → "KILLING").

### Mapping to HvH
- **Asianometry teaches HvH the operation, not the visual.** HvH's "untranslated evidence" / "treaty mechanism" videos can borrow:
  - **MECHANISM REFRAME** — name the underlying system, not the topic. "Thyristors Did to Power…" → "THE THYRISTOR REVOLUTION"
  - **COMPRESSION + ESCALATION** — intensify the verb in compression. "Braking the AI Boom" → "KILLING AI"
  - For HvH's Bakassi: "The 1913 Treaty Resolved Bakassi" → "THE TREATY ENDED IT" (escalation)
- **Topic-timing lesson:** if HvH covers a contemporary mechanism (current border dispute, ongoing legal case), the thumbnail can be more aggressive. If HvH covers a historical retrospective, expect lower CTR ceiling regardless of thumbnail.

---

## Lindybeige (median=20,487 views, n=8 outliers — added Phase B)

### Outlier signal vs loser signal
| Signal | Outliers (n=8) | Losers (n=5) | Δ | Rule |
|---|---|---|---|---|
| has_text | 100% | 100% | 0 | Floor |
| has_face | 62% | 80% | −18pp | **FACE NEUTRAL** — both groups face-heavy; not the differentiator |
| has_map | 0% | 0% | 0 | No maps in this brand |
| has_icons | 0% | **80%** | **−80pp** | **ICONS HURT STRONGLY** — Lindybeige's "club" branded losers use iconography; outliers don't |

### Decision rule (Regime B — visual-driven channel; operation is novel)
- **Highest signal-to-noise of all 8 channels** (n=8 outliers, biggest icon delta).
- Lindybeige outliers split into 3 distinct visual modes:
  1. **LOCATION PROOF** — creator visibly IN the location/situation the title describes ("On Holiday in a Country at War" 7.0x — creator outdoors in Ukraine; "A walk around Lviv in wartime" 4.8x; "Postcard from The Field of Mars" 3.8x). Authenticity is the click.
  2. **NARRATIVE BEAT** — overlay is a full sentence narrating an in-video update for an ongoing series ("BIGMAC IS BACK AND NOW THERE ARE NO SNIPERS LEFT IN UKRAINE" 9.3x). Doesn't transfer to standalone videos.
  3. **MECHANISM REFRAME (variants)** — overlay names a sharper version of the title:
     - *Scale*: "and they built 300 of them" (Roman war engine 11.3x — title is a curiosity-prompt, overlay is the scale shock)
     - *Twist*: "Drilling through stone with BONE" (4.1x — title says "stone-age technology"; overlay reveals the surprise material)
     - *Reveal*: "This cemetery is now full" (3.8x — title is poetic; overlay is the punch fact)
     - *Reframe*: "The Many Silly Flaws of HELM'S DEEP" (4.7x — title asks question; overlay answers it dismissively)
- **Anti-pattern (losers):** "club"-branded recurring content ("RULES of HEMA CLUB", "RULES of BLUES CLUB", "FINDERS KEEPERS Episode Two") — meta-content franchises with built-in audience caps.

### Mapping to HvH
- **LOCATION PROOF** is the most underused operation in HvH packaging and the most transferable from Lindybeige. HvH could:
  - Film at the actual disputed border (Bir Tawil, Bakassi, Halaib) and use creator-on-location as primary visual
  - Film at the document archive holding the original treaty
  - Film at the historic site (Tordesillas archive, ICJ courtroom exterior)
- **MECHANISM REFRAME variants** (scale, twist, reveal, reframe) — direct transfer to HvH:
  - HvH "France Bankrupted Haiti" → SCALE variant: "**5x the national budget. For 122 years.**"
  - HvH "The Bakassi Peninsula Belongs to Cameroon" → REVEAL variant: poetic title; overlay = "150,000 PEOPLE. ASKED NOTHING."
  - HvH "The Crusades Weren't Religious" → REFRAME variant: title makes a claim; overlay names the actual mechanism ("They Were Land Speculation")
- **NARRATIVE BEAT** — doesn't transfer; HvH isn't an ongoing dispatch series.
- **Avoid "rules of"-style meta-content** — Lindybeige's clearest anti-signal.

---

## Cross-channel comparison: when does HvH apply which playbook? (Updated 2026-04-26)

| HvH topic shape | Closest channel exemplar | Operation | Visual |
|---|---|---|---|
| Territorial/border (two claimants) | **WonderWhy** | COMPRESSION + VISUAL ANSWER | political_map_flag_fill |
| Territorial/border (disputed/no-man's) | **WonderWhy** | COMPRESSION + VISUAL ANSWER | satellite_map_flag_fill |
| Comparison/distinction | **WonderWhy** | VISUAL ANSWER | venn_diagram_flags |
| Multi-region complex | **WonderWhy** | COMPRESSION + VISUAL ANSWER | satellite_map_color_coded |
| Ideological / myth-busting / debunking | **Knowing Better** | COMPRESSION | historical_photo of subject |
| Iconic cultural touchstone (rare for HvH) | **Shaun** | TITLE REPETITION or NO OVERLAY | iconic photo/artwork only |
| Mechanism / "HOW it worked" (animated brand) | Kraut *(operation only — not visual)* | MECHANISM REFRAME | (n/a) |
| **Mechanism / HOW (replicable visual)** | **Asianometry** *(new)* | **MECHANISM REFRAME, COMPRESSION + ESCALATION** | industrial_photo / factory_photo / diagram_chart |
| **Treaty / legal / diplomatic / intelligence-coded** | **PolyMatter** *(new)* | **TITLE REPETITION + DOSSIER METAPHOR** | document_collage / classified-folder aesthetic |
| **Systemic failure (compound interest, structural)** | **PolyMatter** *(new)* | **AESTHETIC HOOK + intensified overlay** | period-appropriate art (Soviet-realism, etc.) |
| **Site-visitable border / archive / location** | **Lindybeige** *(new)* | **LOCATION PROOF** | creator on outdoor location |
| **Punch-fact / scale / twist / reveal** topics | **Lindybeige** *(new)* | **MECHANISM REFRAME variants (scale/twist/reveal)** | demonstration / stock_composite / outdoor |
| Personality/persona debunking (general) | (none — Three Arrows visual brand doesn't transfer) | — | — |
| **Political fact-check (contemporary public figure + falsifiable claim)** | **Three Arrows (partial transfer)** *(added 2026-04-26)* | **COMPRESSION + face** | **recognizable photo of the figure (not creator selfie) + charged claim term** |

### Two regimes (Phase B finding)

The 8-channel data sorts close-match channels into two outlier-prediction regimes. HvH should match each video to the right regime:

**Regime A — Visual-template channels** (Kraut, WonderWhy, PolyMatter, Asianometry):
- Channel has a strict visual template; outliers and losers look the same
- The outlier signal is **topic curiosity + operation**, not visual variation
- HvH-relevant for: Untranslated Evidence series, treaty/legal videos, recurring formats

**Regime B — Visual-driven channels** (Knowing Better, Shaun, Lindybeige):
- Each video gets a fresh visual decision tied to topic shape
- The outlier signal is **operation + concept fit**
- HvH-relevant for: standalone myth-busting videos, territorial videos, location-anchored videos

---

## Source

Per-channel splits and aggregate stats: `tools/benchmark/_outlier_thumbs_3x_filtered.json`
Outlier corpus with operation tags: `tools/benchmark/OUTLIER-THUMBNAIL-CORPUS.md`
Operation definitions: `tools/benchmark/TITLE-TO-OVERLAY-OPERATION-MAP.md`
