# Thumbnail Build Guide — Piri Reis #57 (zero-budget, free tools)

**Goal:** render 3 PNGs (1280×720, <2 MB each) to the spec in `THUMBNAIL-CONCEPTS.md → BUILD SPEC`.
**Final set:**
| Combo | Face | Overlay | Title (A/B) |
|---|---|---|---|
| 1 — debunk | Hancock solo | **CITES COLUMBUS** | What Graham Hancock Gets Wrong About the Piri Reis Map |
| 2 — read-it | Hancock solo | **NOBODY READ IT** | Graham Hancock's Lost Civilization Map |
| 3 — forensic | none (document) | **READ THE CORNER** | What the Piri Reis Map Actually Says |

All three share the **Forensic Dossier** DNA: macro Ottoman inscription on parchment + paperclipped white translation card + angled red **TRANSCRIPT** stamp. Build the document base once, then make 3 copies.

---

## 0. Tool

**Photopea** (free, browser, no signup, full Photoshop-style control): https://www.photopea.com
Needs: layer **Stroke** style, **Gaussian Blur**, **Hue/Saturation** (desaturate), layer rotate, drop shadow, **Image → Image Size** super-resolution. Canva Free works for a simpler version but its text-stroke and blur control are weaker — prefer Photopea.

---

## 1. Gather assets

**A. Piri Reis map (parchment + inscription).** Public domain (1513).
- Wikimedia Commons high-res: search **"Piri reis world map 01.jpg"** (the famous fragment). Download full resolution.
- **Inscription 6** = the long dense paragraph of Ottoman script (the source list). On the map it's the big block of text in the lower-left/center. Crop a tight, dense rectangle of that script for the macro hero.

**B. Hancock face (Combos 1 & 2).** Already extracted from the in-video JRE clip → `_broll-assets/thumb-face-candidates/hancock_01..20.png`.
- Pick the most **serious / least open-mouthed** frame with clean head framing (07 and 03 are decent; browse all 20). The headphones are fine — they read as "podcast," reinforcing recognition.
- **Crop above the burned-in caption band** (bottom ~25%).
- These are low-res (vertical Short). Upscale before use: Photopea **Image → Image Size**, tick *Preserve Details / resample*, ~2×; or free **Upscayl** (https://upscayl.org, open-source). If it still looks soft at 160 px, swap in a higher-res press still.
- **Gaze:** face goes top-left, document goes right — so he should look toward screen-right (toward the doc). If your chosen frame has him looking screen-left, **flip horizontal** (Edit → Transform → Flip).

**C. Fonts** (free, Google Fonts — download + load into Photopea via the text-tool font menu → "Load font"):
- **Anton** or **Bebas Neue** (headline / key word) — heavy, condensed, Impact-like.
- Impact (system) is an acceptable fallback.

**D. Paperclip PNG** (transparent): grab a free one from a stock-PNG site, or skip — a white card with a drop shadow reads as a card on its own.

**E. TRANSCRIPT stamp:** built in-tool (Step 3), no asset needed.

---

## 2. Canvas + background

1. New file **1280 × 720 px**, 72 dpi.
2. Background fill **#1C2022** (charcoal-navy). This frames the parchment and stops it blending into YouTube's white UI.

---

## 3. Document base (build ONCE, reuse for all 3)

1. Place the Piri Reis map crop. Scale so the parchment carries **50–70% of the visual weight**.
   - Combos 1 & 2: document fills the **center + right two-thirds** (face will sit top-left).
   - Combo 3: document **centered**, filling most of the frame.
2. **Blur & Pop depth:** duplicate the map layer. On the *back* copy, Gaussian Blur ~6–10 px. On the *front* copy, mask so only the **inscription-6 block stays razor-sharp**; let the map edges fall into the blur. Push **Clarity/Structure**: front copy → Filter → Sharpen, and a slight Levels contrast bump so the script texture feels physical.
3. **Warm the parchment:** Hue/Saturation or Color Balance → nudge toward warm stone/amber. Keep it muted (documentary), not saturated.
4. **Translation card:** white rounded rectangle, top edge of the frame, slight rotation (~3°), drop shadow (2–4 px, soft) so it floats. Add the paperclip PNG at its top edge. (Optional: 2–3 lines of small "translated" text on the card — keep illegibly small; it's texture, not a reading element.)
5. **TRANSCRIPT stamp:**
   - Text "TRANSCRIPT", Anton/Impact, fill **#FF0000** (or #CC0000 for a bloodier ink).
   - Add a thin (4–6 px) red rectangle border around it → looks like a rubber stamp.
   - Rotate **−12°**, opacity ~85%. Place it angled across part of the inscription (not over the face, not bottom-right).
   - Distress (optional): erase a few specks with a rough brush so it's not too clean.
6. **Yellow source-glow (Combo 1 especially):** find the word naming Columbus in the inscription crop; add a subtle yellow (#FFD23F) outer glow / soft highlight behind it. This is the +8 focal point that earns "CITES COLUMBUS."

Group these layers as **"DOC BASE"**. Duplicate the group twice so each combo has its own.

---

## 4. Per-combo assembly

### Combo 1 & 2 (faces)
1. Place the upscaled Hancock cut-out at the **top-left** (face centered near the top-left rule-of-thirds point ≈ x 427 / y 240). Head-and-shoulders, **face = 30–50% of frame height**.
2. **Desaturate** the face slightly (Hue/Sat −20 to −40) so it sits in the muted dossier palette.
3. Make sure his gaze points toward the document/stamp (flip if needed — see 1B).
4. Drop shadow behind the face so it lifts off the parchment.
5. Overlay text (Step 5).

### Combo 3 (faceless control)
1. No face. Document centered, card + stamp as the two supporting elements.
2. More negative space — let the inscription breathe.
3. Overlay text (Step 5).

---

## 5. Overlay text (the hook)

- Font **Anton / Bebas Neue**, **ALL CAPS**.
- **White fill + 6 px dark (#0E0E0E) stroke** (layer style → Stroke). If it sits over a busy part of the parchment, drop it on a small red or charcoal block instead. Target contrast ≥ 4.5:1.
- Placement: **lower third, left-aligned.** Keep ≥ 40–60 px off all edges and **completely out of the bottom-right** (YouTube duration badge).
- Size: the key word should be huge — roughly **110–140 px** cap height. It must be readable at 160 px.
- Per combo:
  - **Combo 1:** `CITES COLUMBUS` — consider emphasizing **COLUMBUS** (bigger / yellow) since the stamp + glow point at it.
  - **Combo 2:** `NOBODY READ IT`
  - **Combo 3:** `READ THE CORNER` — optional thin arrow/marker line from the text toward inscription 6.
- Exactly **3 elements** total (face + document + text/stamp). Do not add a 4th — overcrowding = −23% CTR.

---

## 6. Export + QC (before you call it done)

1. **Squint test:** shrink the canvas view to ~160×90 px (or stand back from the screen). You must instantly read: (1) serious face [Combos 1/2], (2) ancient document, (3) the red stamp / bold word. Any of them a blur → scale that element up. *This overrides everything.*
2. Export each as **PNG or JPG, <2 MB**, named e.g. `thumb-combo1.png`, `thumb-combo2.png`, `thumb-combo3.png` in the project folder.
3. Run the rendered-image audit (per combo):
   ```
   python -m tools.preflight.thumbnail_image_audit "video-projects/_READY_TO_FILM/57-piri-reis-map-ottoman-2026/thumb-combo3.png" --serp-ids ACEoMEZO17E,PYm3b4KpXA0,bPTgUZuL4Uk
   ```
   Read differentiation **per combo**: face combos (1/2) are *meant* to ride the Hancock cluster (TYPICAL/BLENDS-IN by design — the overlay carries the difference); faceless **Combo 3 should score STRONG pattern-break**.
4. All 3 built upfront → upload together for YouTube native A/B rotation (paired with their titles).

---

## Notes / honesty flags
- Face frames are from the in-video JRE clip → thumbnail face = first-5s face = a **tight bridge** (good). But low-res; upscale or swap if soft at 160 px.
- Clip content confirmed: frame 16 = Hancock on "the library of Alexandria had been destroyed" (matches the cold-open claim).
- No AI image generation — public-domain map + real video frame + in-tool stamp only (channel convention).
- Rationale + point values for every choice live in `THUMBNAIL-CONCEPTS.md → BUILD SPEC` (notebook-grounded 2026-06-04).
