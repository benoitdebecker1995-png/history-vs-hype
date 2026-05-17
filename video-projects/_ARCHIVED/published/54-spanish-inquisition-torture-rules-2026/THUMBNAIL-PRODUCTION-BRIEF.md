# Thumbnail Production Brief — #54 Spanish Inquisition

**Purpose:** Production-grade specs for hand-building 3 thumbnail PNGs in Photoshop (or equivalent), with optional image-gen-assisted composition/cleanup. ABC test rotation paired to the title rotation in `YOUTUBE-METADATA.md`.

**Brand rule reminder (per `feedback-thumbnail-process.md`):** Real period material is the source of truth. Image generation is permitted ONLY for compositional cleanup, color grading, masking, accent overlays (highlighter streaks, marker boxes), and seamless layering of real assets. **Do NOT generate new "Inquisition art" from prompt.** Do NOT regenerate figures, faces, or document text. The historical material is the brand.

---

## Universal canvas + export specs

| Spec | Value |
|---|---|
| Canvas | 1280 × 720 px (16:9, YouTube standard) |
| Color space | sRGB |
| Format | PNG (uncompressed for upload) |
| Max file size | 2 MB |
| Safe zone | Avoid bottom-right 240×60 px (YouTube duration overlay) |
| Mobile legibility test | Every overlay must be readable at 320×180 px (5× downscale). Open the PNG, downscale, view on phone — if you can't read the overlay text in 1 second, it fails. |
| Type family across all 3 | One sans-serif family for brand consistency. Recommended: **Bebas Neue Bold**, **Anton**, **Oswald Bold**, or **Impact**. Use the same family across α / β / γ. |
| Universal stroke | 4–6 px black (#000000) outline on all overlay text, for white-text-on-any-background contrast |

---

## Pair α — HERO

### Title paired
> *The Spanish Inquisition Wrote Its Own Torture Manual. Paragraph 15 Has a Loophole.*

### Source assets

| Layer | Asset | License | Source |
|---|---|---|---|
| Base | Francisco de Goya, *Caprichos* no. 24 — *No hubo remedio* (1797–99) | Public domain | Wikimedia Commons — search filename: `Museo_del_Prado_-_Goya_-_Caprichos_-_No._24_-_No_hubo_remedio.jpg` |

### Layer stack (bottom to top)

1. **Base etching** — Goya *Capricho* 24 at full canvas. Crop to fit 16:9 with focus on the central prisoner figure (sanbenito + mounted donkey + jeering crowd). The prisoner's face must be visible.
2. **Color grade adjustment** — desaturate to ~40% saturation (NOT full B&W; preserve some sepia warmth in shadows). Increase contrast +20%. Slight curves S-shape for drama.
3. **Vignette** — radial gradient, dark edges, ~30% opacity black, soft falloff. Pulls eye to prisoner.
4. **Highlighter streak (accent)** — 1–2 horizontal yellow strokes at upper-third (where the prisoner's "verdict scroll" hangs). Color: **#FFEB3B** (high-saturation yellow). Opacity: 50–65%. Brush: rough marker, NOT crisp rectangle. Width: ~80–120 px. Length: ~400–600 px. Suggests a real physical highlighter pulled across a hidden line of text (the loophole).
5. **Overlay text** — see below.

### Overlay text spec

| Property | Value |
|---|---|
| Text | `LEGAL WORKAROUND` |
| Lines | 1 (single line) OR 2 stacked (`LEGAL` / `WORKAROUND`) — depending on layout test |
| Font | Bebas Neue Bold (or Impact) — all caps |
| Size | 110–130 pt (single line) or 140–160 pt (two-line stack) |
| Color | White #FFFFFF |
| Stroke | 5 px black #000000 outline |
| Drop shadow | Optional — 2 px down, 50% black, 4 px blur |
| Placement | Lower-third, center-aligned. Y-anchor at ~70% canvas height. Text bottom edge ~120 px from canvas bottom (clears YouTube duration overlay). |

### Mobile legibility check
At 320×180, the prisoner figure must be recognizable as a hooded penitent. The overlay text must read in <1 second. The yellow streak must remain visible (not blend into background).

### Image-gen prompt (for compositional cleanup only)

```
Source: Goya etching "No hubo remedio" (Capricho 24, 1797–99, public domain).
Edit instructions: Desaturate to approximately 40 percent saturation, preserving warm
sepia in shadows. Increase contrast moderately. Apply a soft radial vignette darkening
the canvas edges. Composite a single rough horizontal yellow highlighter brush stroke
(simulating a marker drawn across a hidden text line) in the upper-third area.
Highlighter color: high-saturation yellow #FFEB3B, opacity 50-65%, brush width 80-120 px.
DO NOT regenerate the etching figures or add new objects. Preserve all original Goya
line work and crowd composition. The yellow streak is the only synthetic addition.
Final canvas: 1280x720, sRGB, PNG.
```

---

## Pair β

### Title paired
> *The Spanish Inquisition's Torture Methods Came From a Manual. Paragraph 15 Has a Catch.*

### Source assets

| Layer | Asset | License | Source |
|---|---|---|---|
| Base | Bernard Picart, Inquisition torture engraving from *Cérémonies et coutumes religieuses de tous les peuples du monde* (Amsterdam, 1723–37) | Public domain | Wikimedia Commons / Internet Archive — search "Picart Inquisition torture engraving" — multiple plates available; pick the one with most dramatic shadow + clearly visible torture mechanism |
| Composite | Period typography render of *Compilación de las Instrucciones* Article XV (Spanish original, 1484, or 1576 facsimile) | Public domain | Wikimedia Commons / Internet Archive — search "Compilación de las Instrucciones 1576" or "Torquemada Instrucciones Articulo XV." If unavailable: render Article XV text in a period Spanish typography (e.g., Garamond, Caslon) on aged parchment background |

### Layer stack (bottom to top)

1. **Base engraving** — Picart torture chamber, full canvas, crop to dramatic torture-in-progress focus. High shadow contrast preserved.
2. **Sepia grade** — warm sepia/parchment color overlay at ~25% opacity (multiply blend mode) to unify with composite document.
3. **Document composite** — Compilación scan layered as a "loose page" placed in the lower-left OR upper-right corner. Slight rotation 5–10°. Document occupies ~25–30% of canvas area.
4. **Drop shadow under document** — 8 px down, 12 px blur, 60% black. Gives "loose paper on top" feel.
5. **Paperclip graphic (optional)** — small metallic paperclip illustration at the corner where the document meets canvas. Sells the dossier metaphor. PNG asset, free clipart fine.
6. **Red marker box (accent)** — hand-drawn rough rectangle around the "Articulo XV" / "Paragraph 15" line on the Compilación scan. Color: **#CC0000**. Stroke: 6 px. NOT a crisp Photoshop rectangle — use a brush to draw it slightly imperfect (rough corners, slight tremor). Suggests a real pen mark.
7. **Overlay text** — see below.

### Overlay text spec

| Property | Value |
|---|---|
| Text | `THE TORTURE MANUAL` |
| Lines | 2 stacked (`THE TORTURE` / `MANUAL`) for visual weight |
| Font | Bebas Neue Bold (matching α) |
| Size | 110–130 pt per line |
| Color | White #FFFFFF |
| Stroke | 5 px black outline |
| Placement | Top-center OR bottom-center (whichever side has less Picart detail). Test both. Avoid covering the marker box on the document. |

### Optional dossier touches (ship 1 max — don't stack)

- Single thin black "redaction bar" (~80 px × 20 px) over a non-essential area of the engraving. NOT over text or faces. Sells "classified" feel without obscuring content.
- Slight aged-paper grain texture overlay at 15% opacity across full canvas.

### Mobile legibility check
At 320×180, the torture chamber must read as a torture chamber (not generic period scene). The Compilación page must be visible as a separate document layer. The red marker box must remain visible. The overlay text must read in <1 second.

### Image-gen prompt (for compositional cleanup only)

```
Composite three real public-domain assets:
1. Base layer: Bernard Picart Inquisition torture engraving (1720s, public domain, source provided).
2. Composite layer: Period typography page of Compilación de las Instrucciones, Article XV
   (1484/1576, public domain, source provided), positioned as a loose document overlaid
   in the lower-left or upper-right corner, rotated 5-10 degrees, with realistic drop
   shadow underneath suggesting it sits on top of the engraving.
3. Accent: A hand-drawn-style red marker rectangle (color #CC0000, 6 px stroke, slightly
   imperfect/rough corners) around the "Articulo XV" line on the document. The marker
   should look like a real pen mark, NOT a crisp digital rectangle.
Color grade: sepia/parchment warmth across both layers to unify them.
Optional: subtle paperclip graphic at the corner where document meets canvas; subtle
aged-paper grain at 15% opacity.
DO NOT regenerate the engraving figures, faces, or torture mechanism. DO NOT regenerate
the Spanish text on the document. Preserve all original line work.
Final canvas: 1280x720, sRGB, PNG.
```

---

## Pair γ

### Title paired
> *The Spanish Inquisition Documented Its Torture Methods. Most Critics Skip Paragraph 15.*

### Source assets

| Layer | Asset | License | Source |
|---|---|---|---|
| Foreground | Torture device from Philipp van Limborch, *Historia Inquisitionis* (Amsterdam, 1692) — pick ONE device (strappado, rack, or thumbscrews) at the engraver's most detailed plate | Public domain | Wikimedia Commons / Internet Archive — search "Limborch Historia Inquisitionis 1692 torture engraving" |
| Background | Parchment scan of 1484 Compilación page (any clear period rendering of Article XV text) | Public domain | Same source as Pair β document layer; can reuse |

### Layer stack (bottom to top)

1. **Parchment background** — fills full canvas, slight aged warmth (#F5E6C8 base tone), subtle paper grain texture. Period authentic, not modern off-white.
2. **Compilación text layer (subtle)** — period Spanish text from Article XV faintly visible across the parchment (opacity 35–50%). Provides intellectual-competence signal: "this is on top of the actual document." Don't make text fully readable; it's atmospheric, not informational.
3. **Torture device cutout** — Limborch woodcut device, transparent background, MACRO close-up. Device fills ~50–60% of canvas (dominant element). Position: slightly off-center to the left (rule of thirds), leaving right-third clear for overlay text.
4. **Drop shadow under device** — 12 px down, 20 px blur, 50% black. Realistic "object resting on document" depth.
5. **Subtle vignette** — radial dark edges at 20% opacity. Pulls eye to device.
6. **Overlay text** — see below.

### Overlay text spec

| Property | Value |
|---|---|
| Text | `PARAGRAPH 15` |
| Lines | 2 stacked (`PARAGRAPH` / `15`) — gives the number visual weight |
| Font | Bebas Neue Bold (matching α and β) |
| Size | 130 pt for `PARAGRAPH`, 200 pt for `15` (the number is the punch — make it bigger) |
| Color | White #FFFFFF |
| Stroke | 6–8 px black outline (extra thick because parchment background has variable contrast) |
| Drop shadow | 3 px down, 60% black, 6 px blur |
| Placement | Right-third of canvas (the device is left-third). Y-anchor: vertically centered or slight-bottom-bias. |

### Optional credit micro-text

If the chosen torture device isn't instantly recognizable as Inquisition-era, add micro-text in lowest-corner: `Limborch, Historia Inquisitionis (1692)` at 10 pt, 60% opacity white-with-stroke. Anchors authenticity for skeptical viewers.

### Mobile legibility check
At 320×180, the device shape must be recognizable as a torture mechanism (not a chair, not a tool, not abstract). The number "15" must be readable at first glance. If the device is ambiguous at small size, swap to a more recognizable plate.

### Image-gen prompt (for compositional cleanup only)

```
Composite two real public-domain assets:
1. Background: Parchment scan with faint Compilación de las Instrucciones Article XV
   text visible at 35-50% opacity (1484/1576, public domain, source provided). Aged
   warm tone (#F5E6C8 base). Subtle paper grain texture across full canvas.
2. Foreground: Cutout of a torture device from Limborch's Historia Inquisitionis (1692,
   public domain, source provided). MACRO close-up — device fills 50-60% of canvas,
   positioned in left-third (rule of thirds). Realistic drop shadow underneath
   (12 px down, 20 px blur, 50% black) so the device appears to physically rest on the
   parchment.
3. Subtle radial vignette darkening canvas edges at 20% opacity.
DO NOT regenerate or modernize the torture device woodcut. Preserve all original
Limborch line work. DO NOT regenerate the Spanish text on the parchment.
Final canvas: 1280x720, sRGB, PNG.
```

---

## Brand consistency across α / β / γ

These three thumbnails will rotate via YouTube native A/B. Visual cohesion matters — viewers seeing them across discovery surfaces should perceive them as one channel.

| Element | Standard across all 3 |
|---|---|
| Type family | Same sans-serif (Bebas Neue Bold or equivalent) |
| Stroke spec | 4–8 px black on white text |
| Color register | Period-authentic — sepia, parchment, oxblood, ink-black. NO modern saturated palettes. |
| Accent color | One per thumbnail (yellow on α, red on β, none on γ). Single accent only — no rainbow. |
| Verdict words | Forbidden on all three. No "BRUTAL," "EVIL," "SHOCKING." Overlays are noun/mechanism anchors only. |
| Faces | No creator face. Period figures only. |
| AI imagery | Forbidden as primary content. Permitted for compositional cleanup, color grading, masking, accent layers, and seamless compositing of real public-domain source assets. |

---

## Pre-publish checklist

For each of α / β / γ:

- [ ] Source assets downloaded from Wikimedia/Internet Archive (cite in filename: `α_goya_capricho24.psd`)
- [ ] Layer stack built per spec
- [ ] Color grade applied
- [ ] Accent layer (highlighter / marker box / vignette) added
- [ ] Overlay text rendered with stroke + drop shadow
- [ ] Exported as 1280×720 PNG, sRGB, under 2 MB
- [ ] Mobile legibility test passed (downscale to 320×180, view on phone, readable in <1 second)
- [ ] Filename convention: `54-thumb-α-LEGAL-WORKAROUND.png`, `54-thumb-β-TORTURE-MANUAL.png`, `54-thumb-γ-PARAGRAPH-15.png`
- [ ] Saved to project folder root for upload

---

## Troubleshooting

**If the Limborch torture device looks too generic / not Inquisition-recognizable:**
Swap to a different Limborch plate. The 1692 first edition has multiple torture engravings; pick the strappado (hanging-by-arms) — most universally recognizable as Inquisition imagery.

**If the Picart engraving is too small-detail / loses readability at mobile:**
Crop tighter to a single torture pose (one figure being tortured, one tormentor). Sacrifice context for legibility.

**If the Goya Capricho 24 prisoner figure isn't reading as a sanbenito-clad penitent:**
The conical hat (coroza) is the iconographic tell. Make sure the crop includes the hat. If the original Wikimedia file is too low-res, use the Museo del Prado high-resolution download (free, registered account).

**If the yellow highlighter on α reads as a Photoshop element rather than a real marker:**
Use a pressure-sensitive marker brush or a real photo of a yellow highlighter stroke. Vary the opacity slightly across the stroke length (real markers don't apply uniformly).

**If the red marker box on β looks too crisp / digital:**
Hand-draw it with a tablet, or use a "marker" brush preset. A real pen mark has slight tremor and uneven pressure.
