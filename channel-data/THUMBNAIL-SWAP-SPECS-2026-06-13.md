# Thumbnail Swap — Render Specs (2026-06-13)

Paint-by-numbers builds for the two SWAP-CHECKLIST videos. Canvas = **1280×720 px** (16:9), export JPG/PNG <2 MB.
**Mobile safe zone:** keep all key text within the central 90%; **avoid the bottom-right ~250×80 px** (YouTube duration stamp sits there).
**Font:** Anton (free, Google Fonts) or Montserrat ExtraBold — heavy condensed sans. All headline text: white `#FFFFFF`, **black stroke 8-10 px**, soft drop shadow (0/4 px, 40% black). No verdict words.

---

## Video 1 — Atlantic Slave Trade  (`aSfZtrgGjwA`)
### Concept: "The Claim vs The Receipts" (fixed)

Keeps the conflict/face hook that's already earning 1.91%; fixes the two failures — illegible document and no topic signal.

**Layout (x from left, y from top):**
| Element | Position | Spec |
|---|---|---|
| Background | full 1280×720 | Dark charcoal `#141414`, subtle vignette |
| LEFT panel — claimant | x 0–440 (34%) | The same person from current thumb. Desaturate 50%, cool tint, slight darken. Crop head-and-shoulders, face in upper area. |
| Divider | x ≈ 440, full height | 6 px vertical bar, deep red `#B11212` |
| RIGHT panel — the document | x 460–1280 (64%) | Aged primary source (papal bull / Portuguese slave ledger). **Large and legible** — fills the panel, rotated ~4°, drop shadow. Warm parchment tone, raise contrast so script texture reads. |
| Small label over face | x 30, y 40 | `THE CLAIM` — Anton ~52 px, white, red underline bar |
| MAIN headline | centered across bottom, x 60–1180, baseline y ≈ 660 | `THEY WROTE IT DOWN` — Anton ~120 px, on a 70%-black full-width band (y 560–720). Sits left-of-center to dodge the bottom-right stamp. |
| Accent (optional) | on document | small red wax-seal graphic for a color pop |

**Why it converts:** face = recognition + conflict; legible document = the "receipts" payoff; `THEY WROTE IT DOWN` reinforces the title's "The Documents Prove It." Title carries the topic keyword, thumb carries the visual proof — no duplication.

**Assets (public domain — Wikimedia Commons / archive.org):**
- Search: `Romanus Pontifex manuscript`, `Dum Diversas bull`, `Casa da Guiné ledger`, `Portuguese slave trade document 15th century`.
- Pick the one with the most visible handwriting/seal texture. Keep the claimant image from your existing `thumb a.psd`.

---

## Video 2 — Hijab / The Veil  (`mCR5f_ZcB5k`)
### Concept: "1,800 Years Before Islam" (single ancient subject)

**Layout:**
| Element | Position | Spec |
|---|---|---|
| Background | full 1280×720 | Near-black `#0D0D0D`, faint Assyrian-relief texture at 15% opacity (reuse your current brick/relief asset, darkened) |
| HERO — ancient veiled figure | x 40–620, vertically centered, ~80% frame height | Ancient veiled statue/relief where the **head-drape is unmistakable**. Stone tone, warm rim-light from right, strong shadow side left. Cut out from its own background, drop shadow to separate from BG. |
| Headline line 1 | x 650, y ≈ 240 | `1,800 YEARS` — Anton ~150 px. "1,800" in amber-gold `#E8B23A`, "YEARS" white. |
| Headline line 2 | x 650, y ≈ 400 | `BEFORE ISLAM` — Anton ~150 px, white |
| Corner tag | x 40, y 660 | `Assyrian Law · 1200 BCE` — Montserrat SemiBold ~38 px, muted grey `#AAAAAA` |

**Why it converts:** the veil = instant topic recognition; a visibly *ancient* artifact = the curiosity gap made visual; `1,800 YEARS` (gold) is the thumb-stopper number. Using an ancient relief instead of a modern hijab **removes the polemic read** that's the likeliest cause of the 1.48% — you keep the substance, drop the culture-war signal that makes browse viewers scroll past.

**Assets (public domain — verify the piece is pre-Islamic, i.e. BCE–early CE):**
- Search: `Hellenistic veiled woman statue`, `veiled head statue ancient`, `Tanagra veiled figure`, `Mesopotamian veiled woman relief`, `Assyrian palace relief` (for the background texture).
- Choose a figure where cloth clearly covers the head/hair — that's what reads as "veil" at thumbnail size. Avoid Baroque/Renaissance pieces (they read "modern marble," not "ancient").

---

## Build notes
- Both: render at 1280×720, then **shrink to ~320×180 and check legibility** — if the headline isn't readable at that size, enlarge the text, don't add more.
- Text overlay = 2-3 words max (channel rule). The number does the work on the hijab one.
- Save working files next to the originals (`thumb_v2.psd` / `.png`) in each project folder; don't overwrite the published originals so revert is clean.
- A/B option: native YouTube test the new thumb against the current one if you want a clean read (you can upload 3 variants).
