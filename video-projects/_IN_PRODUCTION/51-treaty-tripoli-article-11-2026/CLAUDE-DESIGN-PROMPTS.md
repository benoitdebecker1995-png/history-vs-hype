# Claude Design Prompts — Tripoli Article 11

Copy any prompt below and paste into https://claude.ai/design as one message. Each is self-contained — quote text verbatim from `01-VERIFIED-RESEARCH.md`, anti-slop directives included, dimensions specified.

**House style locked across all prompts** (so the assets feel like a coherent set):
- Modern editorial / museum-exhibit-text-panel aesthetic
- Warm charcoal background `#14110F` (or cream `#F1EBDD` if specified)
- Cream type `#F4EDE0`, accent gold `#E8D9A8`
- Body serif: EB Garamond (or Source Serif Pro / Spectral as fallback)
- UI sans: Inter (or system-ui)
- 1920×1080 (16:9, YouTube-safe)
- **Hard exclusions across the set:** no faux-parchment textures, no torn-paper edges, no sepia gradients, no "vintage" filters, no blackletter / Old English fonts, no decorative initial caps or flourishes, no AI-generated period imagery, no drop shadows mimicking an old book

If a prompt produces something that drifts toward "fake old document" — paste it back with: *"Strip all aging effects. Keep the typography modern. The intervention is honestly modern; the source it cites is from 1797 or 1931."*

---

## Prompt 1 — Hurgronje "no equivalent" quote card (Beat 4 reveal)

```
Create a 1920×1080 quote card for a YouTube history video. Modern editorial design — think museum exhibit text panel, not vintage parchment.

Background: warm charcoal #14110F (not pure black).
Type: cream #F4EDE0 with warm gold #E8D9A8 accents on emphasized words.
Serif for the quote (EB Garamond, Source Serif Pro, or Spectral). Sans-serif for labels and citations (Inter or system).

Layout:
- Small uppercase label at top, letterspaced 0.22em, color #A89882: "ANNOTATED TRANSLATION OF 1930"
- Large serif quote, left-aligned, ~64px, max width 1400px:
  "The eleventh article of the Barlow translation has no equivalent whatever in the Arabic. The Arabic text opposite that article is a letter from Hassan Pasha of Algiers to Yussuf Pasha of Tripoli."
  Italicize "no equivalent whatever" in warm gold.
- Single 80px hairline divider below the quote
- Italic attribution, ~24px: "C. Snouck Hurgronje, University of Leiden"
- Small uppercase citation footer, ~14px, letterspaced, color #6F6354: "IN HUNTER MILLER, ED., TREATIES AND OTHER INTERNATIONAL ACTS OF THE UNITED STATES, VOL. 2, P. 371 — GOVERNMENT PRINTING OFFICE, 1931"
- Tiny "HISTORY VS HYPE" wordmark bottom-right, 12px, 0.32em letterspacing, color #5A4F3F

NO faux aging, NO parchment, NO drop shadows, NO decorative flourishes. The intervention is modern; the source it quotes is from 1931.
```

---

## Prompt 2 — Hurgronje "stupid secretary" quote card (Beat 4)

```
Create a 1920×1080 quote card for a YouTube history video. Same house style as before — warm charcoal #14110F background, cream #F4EDE0 type, EB Garamond serif for quote, Inter for labels.

Layout:
- Eyebrow label top, uppercase, letterspaced 0.22em, color #A89882: "ON THE LETTER BOUND IN PLACE OF ARTICLE 11"
- Large serif quote, left-aligned, ~56px (slightly smaller than usual — quote is longer):
  "Three fourths of the letter consists of an introduction, drawn up by a stupid secretary who just knew a certain number of bombastic words and expressions occurring in solemn documents, but entirely failed to catch their real meaning."
  Italicize "a stupid secretary" in warm gold #E8D9A8.
- 80px hairline divider
- Italic attribution: "C. Snouck Hurgronje"
- Uppercase citation footer: "IN HUNTER MILLER, ED., TREATIES AND OTHER INTERNATIONAL ACTS OF THE UNITED STATES, VOL. 2, P. 371 — GOVERNMENT PRINTING OFFICE, 1931"
- Bottom-right wordmark "HISTORY VS HYPE"

Modern editorial only. No vintage effects.
```

---

## Prompt 3 — Miller "most extraordinary" quote card (Beat 6 closing)

```
Create a 1920×1080 quote card. Same house style — warm charcoal background, cream serif type, gold accents.

Layout:
- Eyebrow label: "EDITOR'S NOTE, 1931"
- Large serif quote (~64px):
  "Most extraordinary (and wholly unexplained) is the fact that Article 11 of the Barlow translation, with its famous phrase, 'the government of the United States of America is not in any sense founded on the Christian Religion,' does not exist at all. There is no Article 11."
  Italicize "(and wholly unexplained)" in warm gold.
- Hairline divider
- Italic attribution: "Hunter Miller, editor — State Department historian"
- Citation footer: "TREATIES AND OTHER INTERNATIONAL ACTS OF THE UNITED STATES, VOL. 2, P. 384 — GOVERNMENT PRINTING OFFICE, 1931"
- Bottom-right wordmark "HISTORY VS HYPE"

Modern editorial. The italicized parenthetical is the emotional weight — typography should let it breathe.
```

---

## Prompt 4 — Spellberg "he probably never knew" quote card (Beat 5)

```
Create a 1920×1080 quote card. Same house style — warm charcoal background, cream serif type, gold accents.

Layout:
- Eyebrow label: "ON JOEL BARLOW'S SIGNATURE"
- Large serif quote, slightly larger than usual (~72px because quote is short and should land hard):
  "He probably never knew that Article 11 never existed in an Arabic translation."
  Italicize "never existed" in warm gold.
- Hairline divider
- Italic attribution: "Denise A. Spellberg, University of Texas at Austin"
- Citation footer: "THOMAS JEFFERSON'S QUR'AN: ISLAM AND THE FOUNDERS — ALFRED A. KNOPF, 2013"
- Bottom-right wordmark "HISTORY VS HYPE"

Modern editorial. The short quote should fill the frame visually — generous whitespace above and below.
```

---

## Prompt 5 — Crane "wielded as often" quote card (Beat 6 closing)

```
Create a 1920×1080 quote card. Same house style.

Layout:
- Eyebrow label: "ON THE LATER READING OF ARTICLE 11"
- Large serif quote (~72px):
  "The language of Article 11 was wielded as often by Christian nationalists as by militant secularists."
  Italicize both "Christian nationalists" and "militant secularists" in warm gold — they should feel as a balanced pair visually.
- Hairline divider
- Italic attribution: "Jacob Crane, Bentley University"
- Citation footer: "'READING AMERICAN SECULARISM IN THE 1797 TREATY OF TRIPOLI' — AMERICAN QUARTERLY 72:2, P. 405 — JOHNS HOPKINS UNIVERSITY PRESS, 2020"
- Bottom-right wordmark "HISTORY VS HYPE"

Modern editorial. The two italicized phrases should look symmetrical — that's the editorial point.
```

---

## Prompt 6 — 133-year timeline (Beat 6 closing setup)

```
Create a 1920×1080 horizontal timeline graphic for a YouTube history video. Modern data-viz aesthetic — minimal, editorial. NOT a "vintage scroll" or anything textured.

Background: warm charcoal #14110F.
Type: cream #F4EDE0, with warm gold #E8D9A8 for emphasized labels, muted #B8A88E for secondary events.

Top of frame:
- Small uppercase subtitle: "THE STRANGEST PART ISN'T THE MISSING TEXT"
- Large serif title beneath: "It's what happened in the 133 years before anyone noticed."
  Italicize "133 years" in warm gold.

Middle: a horizontal "broken" timeline. Three event clusters:

LEFT CLUSTER (1796–1797):
- Nov 4, 1796 — "Treaty signed at Tripoli"
- Jun 7, 1797 — "Senate ratifies Article 11"
- Jun 23, 1797 — "Cobbett: 'trampling upon the cross'" (this one rendered slightly muted to indicate minor reaction)

CENTER (the silence):
- Large italic serif text "133 years of silence"
- Below it, small uppercase letterspaced sublabel: "NO SCHOLAR OPENS THE FILE"
- The horizontal axis line through this segment should be a dotted/dashed pattern (not solid) to visually distinguish the silent period

RIGHT CLUSTER (1930–2020):
- 1930 — "Hurgronje examines the Arabic"
- 1931 — "Miller publishes the gap"
- 2020 — "Crane: secular reading is a re-reading" (slightly muted)

Each event = small luminous dot on the axis (cream/gold), with a thin vertical stem connecting to its label. Date in monospace (JetBrains Mono or similar). Description in serif.

Stem direction alternates up/down for readability — first event up, second down, etc.

Bottom-right: "HISTORY VS HYPE" wordmark.

Modern data viz only. NO illustrated decorations, NO period engravings, NO faux-old elements. The dramatic device is the visual gap in the middle of the timeline.
```

---

## Prompt 7 — Side-by-side English vs Arabic frame (Beat 3→4 transition)

```
Create a 1920×1080 split-screen design template for a YouTube history video. The video centers on a 1797 treaty where the English text contains an article (Article 11) that the Arabic original does not contain — instead, the Arabic page is a letter.

I will provide two scanned page images later — for now, generate the design with two placeholder zones.

Layout: vertical split, two equal panels separated by a single thin hairline at center.

LEFT panel:
- Top label, uppercase letterspaced 0.32em, color #A89882: "ENGLISH — SENATE-RATIFIED TEXT"
- Center: a placeholder zone (dashed outline) for the English Article 11 page scan
- Bottom-left caption, italic serif #B8A88E: "Article 11, Treaty of Tripoli — Ratified Wed, June 7, 1797"

RIGHT panel:
- Top label, uppercase letterspaced 0.32em, color #A89882: "ARABIC — OPPOSITE THAT ARTICLE"
- Center: placeholder zone for the Arabic facsimile page scan
- Bottom-right caption, italic serif: "Letter from Hassan Pasha of Algiers to Yussuf Pasha of Tripoli"

Center seam: thin vertical hairline #3A322A between panels, with a small framed center overlay box reading "MISSING IN ARABIC" — bordered, modern Inter sans-serif, letterspaced, with "IN ARABIC" in warm gold.

Background everywhere: deep warm charcoal #0E0C0A.

Bottom-right corner: small "HISTORY VS HYPE" wordmark.

Modern editorial only. No frames or borders that mimic old picture frames. The placeholder zones are clean dashed rectangles, ready for image swap-in.
```

---

## Prompt 8 — Arabic page annotation overlay (Beat 4 reveal)

```
Create a 1920×1080 design overlay concept for a YouTube history video. The shot shows a real scan of an Arabic manuscript page (from a 1931 State Department publication). My modern annotation goes on top to mark where the missing Article 11 should be.

Generate the design with a placeholder zone for the scan image.

Background: deep warm charcoal #0E0C0A.

Center-left: a vertical placeholder rectangle (~1100×920px) where the Arabic scan will live. Around the image area, the "intervention" markup:

1. A clean modern callout box (saturated gold border #E8B547, 2px) drawn over the area where Article 11 "should be" — roughly the middle-upper third of the page. Subtle outer glow at 10% opacity. Small L-shaped corner brackets at top-left and bottom-right of the callout to make it read as a designed marker, not a hand-drawn circle.

2. To the right of the scan: a connected annotation label.
   - Thin 80px gold lead-line at the top of the label
   - Small uppercase pin label (gold, letterspaced 0.32em, ~13px): "WHERE ARTICLE 11 SHOULD BE"
   - Below it, serif text (~32px, line-height 1.32):
     "A letter from Hassan Pasha of Algiers to Yussuf Pasha of Tripoli — not Article 11."
     Italicize both names in warm gold #E8D9A8.
   - Bottom of the label, uppercase citation footer (~12px, letterspaced, color #6F6354):
     "IDENTIFIED BY C. SNOUCK HURGRONJE, 1930
     HUNTER MILLER, ED., VOL. 2, P. 371"

Top-left of frame: small uppercase header tag, letterspaced 0.32em, color #A89882: "ARABIC ORIGINAL — OPPOSITE ARTICLE 11"

Bottom-right: tiny "HISTORY VS HYPE" wordmark.

The whole design language is "professor marks up a slide" — deliberate, modern, clearly graphic. NOT a fake-aged document with hand-drawn red ink. The intervention is honestly modern; what it cites is from 1797 / 1931.
```

---

## Prompt 9 — Article 11 hero shot (Beat 3 — when the article is read aloud)

```
Create a 1920×1080 hero text frame for a YouTube history video. The shot is the moment a primary-source treaty article is read aloud — Article 11 of the 1797 Treaty of Tripoli.

This is NOT a recreation of an 18th-century document. It is a modern editorial presentation of an 18th-century quote. The viewer should read it; they should not believe they're looking at an antique scan.

Background: cream #F1EBDD (warm paper-like, but flat — no texture, no aging, no grain).
Type: deep ink #1A1612 for the body, with warm brown #4A3A1F for emphasized words.

Layout:
- Small uppercase header, letterspaced 0.32em, color #6F6354: "ARTICLE 11 — TREATY OF PEACE AND FRIENDSHIP, 1797"
- Large serif quote, full-width centered, ~50–56px (whole article is long), classical serif (EB Garamond or similar):

"As the government of the United States of America is not in any sense founded on the Christian Religion, — as it has in itself no character of enmity against the laws, religion or tranquility of Musselmen, — and as the said States never have entered into any war or act of hostility against any Mehomitan nation, it is declared by the parties that no pretext arising from religious opinions shall ever produce an interruption of the harmony existing between the two countries."

Italicize the clause "is not in any sense founded on the Christian Religion" in warm brown #4A3A1F as the emphasized phrase.

- Below the quote: 80px hairline #B8A88E
- Small italic attribution: "Senate-ratified text — June 7, 1797"
- Small uppercase citation footer, letterspaced, color #8A7B66: "IN HUNTER MILLER, ED., TREATIES AND OTHER INTERNATIONAL ACTS OF THE UNITED STATES, VOL. 2 — GOVERNMENT PRINTING OFFICE, 1931"
- Bottom-right wordmark "HISTORY VS HYPE"

NO ornamental borders, NO faux-period engravings, NO long-S ligatures (we are reading this in modern context). Modern typesetting of an 18th-century text.
```

---

## Prompt 10 — Lower-third name super (for any historian intro on screen)

```
Create a reusable 1920×1080 lower-third name super template for a YouTube history channel. It should be a thin overlay that lives in the bottom-left of the screen, reserving the top 75% for footage / B-roll.

Style: modern documentary, BBC / Atlantic / Nat Geo level. Not flashy.

Bottom-left composition (occupies ~bottom 18% of frame):
- A horizontal warm-gold accent line (#E8D9A8), 4px tall, 80px wide, at the very top of the lower-third zone
- 24px below, the name in serif (EB Garamond), bold, ~48px, color cream #F4EDE0:
  [NAME PLACEHOLDER — e.g., "Denise A. Spellberg"]
- 8px below, the credential in sans-serif (Inter), regular, ~22px, italic, color #B8A88E:
  [CREDENTIAL PLACEHOLDER — e.g., "Author, Thomas Jefferson's Qur'an (2013)"]
- Optional second line below the credential in even smaller sans-serif (~16px, letterspaced 0.18em, uppercase, color #8A7B66):
  [INSTITUTION — e.g., "UNIVERSITY OF TEXAS AT AUSTIN"]

The lower-third should have NO solid background bar — text floats over the footage. If contrast is poor against bright footage, add a subtle linear gradient from the bottom edge fading from #14110F at 70% opacity to fully transparent over 240px.

Generate three example renders with these placeholders filled in:
1. "Denise A. Spellberg" / "Author, Thomas Jefferson's Qur'an (2013)" / "UNIVERSITY OF TEXAS AT AUSTIN"
2. "Jacob Crane" / "American Quarterly, 2020" / "BENTLEY UNIVERSITY"
3. "Hunter Miller" / "Editor, Treaties of the United States (1931)" / "U.S. STATE DEPARTMENT"

Modern documentary only. No animated swooshes, no glassy panels, no bevels.
```

---

## Prompt 11 — End-screen / closing card

```
Create a 1920×1080 end-screen closing card for a YouTube history video about the 1797 Treaty of Tripoli.

Background: warm charcoal #14110F.
Type: cream #F4EDE0 with warm gold #E8D9A8 accents.

Layout:
- Top third: small uppercase label "HISTORY VS HYPE" letterspaced 0.32em, ~14px, color #A89882
- Center: a single italic serif line, ~72px, max width 1400px:
  "The fight is real. It just isn't from 1797."
  (Italicize "from 1797" in warm gold.)
- Below the line: thin 80px hairline divider
- Below divider, two side-by-side video-thumbnail placeholder rectangles (16:9 aspect each, ~480×270 with thin gold hairline frame). Above the left one a small label "RELATED VIDEO"; above the right one a small label "SUBSCRIBE."
- Tiny citation footer at the bottom, uppercase letterspaced, color #5A4F3F: "PRIMARY SOURCES IN DESCRIPTION — HUNTER MILLER 1931, SENATE EXECUTIVE JOURNAL VOL. 1 P. 244, SPELLBERG 2013, HASELBY 2015, CRANE 2020"

Modern editorial / documentary close. NO confetti, NO subscribe-button graphics with bells, NO faux-paper background. Calm and confident.
```

---

## Prompt 12 — Thumbnail variant (if you want Claude Design to test alternates)

```
Create three 1280×720 YouTube thumbnail variants for a video titled "The Treaty Of Tripoli's Most Famous Line Isn't In Arabic." The hook is that a US treaty article ratified by the Senate in 1797 does not appear in the Arabic original of that same treaty. The thumbnail should communicate forensic / document mystery, NOT political controversy.

Common constraints (all three):
- 1280×720 16:9
- Big legible 2–4 word text overlay (mobile-safe)
- No human face, no presenter
- Modern editorial, NOT vintage pastiche
- Warm charcoal or deep navy background
- Cream / warm-gold type
- A real document or fragment of a document is welcome IF it can be sourced from a public-domain scan; do not generate fake period documents

Variant A — Split-screen comparison
Left: English article fragment. Right: Arabic page fragment. Big overlay across the seam: "MISSING IN ARABIC" (white/cream, sans-serif, letterspaced).

Variant B — Single document, redaction-style negation
A single document fragment centered. Over it, a clean modern strikethrough or "X" mark in warm gold. Big text below: "NEVER WAS THERE" or "NOT IN ARABIC" — pick the punchier of the two.

Variant C — Date-paradox specificity
Centered framed text "1797 / 1930" in monospace, with a thin vertical line between. Below it, large serif: "MISSING ARTICLE" with a hairline arrow pointing back up to "1930." Background is a soft archival texture (NOT aged paper).

For all three: render multiple compositions until the typography reads cleanly at YouTube's mobile thumbnail size (~120px wide). The text MUST survive that downsampling.
```

---

## Iteration prompts (use these to refine after first generation)

If a result feels too "AI-slop":
> Strip ALL aging, parchment, sepia, and "vintage" effects. The design intervention is honestly modern; only the text content is from 1797 or 1931. Re-render with this constraint.

If type is too small at YouTube playback:
> Re-render with the main quote at 1.3× current size and the citation footer reduced by 25%. This will be played at 1080p where small type is unreadable.

If composition feels generic:
> Re-render with more aggressive whitespace — push the quote into the upper-center two-thirds, leave the bottom third nearly empty except for the divider, attribution, and citation. This is editorial pacing, not poster pacing.

If the eyebrow label looks like a YouTube tag:
> Re-render with the eyebrow in much smaller, more letterspaced uppercase Inter at 14–16px. The eyebrow should whisper context, not announce it.

If gold accent is too saturated:
> Desaturate the warm gold by 30%. We want it to read as "tarnished gold" rather than "warning yellow."

---

## Order to generate (recommended)

1. Start with **Prompt 1** (Hurgronje 371). It's the iconic quote and will calibrate the house style.
2. Once Prompt 1 looks right, run **Prompts 2–5** in any order — they should inherit the style automatically. If Claude Design loses the style, paste the locked house-style block (top of this file) ahead of each new prompt.
3. **Prompt 6** (timeline) is the hardest — expect 2–3 iterations.
4. **Prompts 7–8** depend on having the HathiTrust scans. Generate the design template first; swap in scans later.
5. **Prompt 9** (Article 11 hero) — only if you want a "designed" version of the read-aloud moment. Otherwise just use the real HathiTrust scan from `B-ROLL-ASSET-MANIFEST.md` Section 1.1.
6. **Prompts 10–11** (lower-thirds, end-screen) — channel-level reusable templates. Worth doing well once.
7. **Prompt 12** (thumbnails) — only if the locked thumbnail concept (split-screen with "MISSING IN ARABIC") needs alternate variants for native A/B.

Save outputs as PNG. Drop into `assets/` next to the HTML versions I built — Claude Design output and HTML fallback can coexist; pick whichever looks better per beat.
