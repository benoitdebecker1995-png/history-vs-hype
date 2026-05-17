# Nanobana Prompts — #54 Spanish Inquisition

**Generated:** 2026-05-11
**Purpose:** Ready-to-paste image generation prompts for each B-roll shot.

## Visual language rules (apply to all shots)

- **Compilación shots (1, 2, 3a, 3b, 4, 6, 7, 8):** Use actual PDF screenshots from `_research/documents/Compilacion_de_las_Instrucciones_del_Oficio_de_la_Santa_Inquisicion_(IA_BRes14068130Despacho).pdf` as the base. Nanobana generates the translation overlay panel and highlight box only.
- **Handwritten records (13, 14):** Full nanobana generation — no real scan available for 14; 13 user has Beinart text.
- **Method illustrations (5b, 5c, 5d):** Check Wikimedia Commons for period engravings first. Use nanobana only if no suitable CC image found.
- **Quote cards (3c, 5a, 9, 15, 16):** Typography/design spec — no image generation needed. Build in DaVinci Resolve or Canva.
- **SSCI cover (17):** Use actual PDF screenshot. No nanobana.

**Highlight color:** Yellow (#FFE066) transparent overlay, 40% opacity — high contrast against aged parchment without obscuring text.
**Citation tag:** Lower-right corner, 9pt, same font as translation overlay.
**Minimum screen time per shot:** 2.5 seconds.

---

## CATEGORY A — COMPILACIÓN PRINTED PAGE SHOTS
### (Base = real PDF screenshot. Nanobana = translation overlay + highlight.)

---

### Shot 1 — Compilación Title Page

**Base:** Screenshot the actual title page from the Compilación PDF (front matter before f. 1r).

**Nanobana overlay prompt:**
```
Add a translation panel below the title page of a 1630 Spanish ecclesiastical printed book.
The panel uses the same aged parchment texture as the page. Typography: humanist roman typeface
matching the period, in dark sepia ink, slightly smaller than the title type. Text reads:

"Compilation of the Instructions of the Office of the Holy Inquisition"
[smaller line] "Argüello edition, 1630 — founding text: Torquemada, 1484; expanded Valdés, 1561"

Citation tag lower-right: "Argüello 1630, Compilación de las Instrucciones"

Do not add any modern elements. The overlay must look as if it was printed on the same page
in the same era.
```

**Timing:** Hold 3 seconds at §1 hook (~0:25).

---

### Shot 2 — Article XV Full Text (f. 6v) — THE CENTERPIECE

**Base:** Screenshot f. 6v from the Compilación PDF. This page contains the full §XV paragraph including all three key clauses.

**Nanobana overlay prompt — translation panel:**
```
Add a translation panel in the right margin or below of a 1630 Spanish printed page showing
§XV of the Compilación. Typography: humanist roman, sepia ink, aged parchment texture. Text reads:

"§XV — Half-proofs and Torture
'If the said crime appears half-proven, the inquisitors shall consider putting the accused
to the question of torture. If the accused confesses under torture, and afterward ratifies
his confession on the next or third day, he shall be punished as convicted.
[...] The aforesaid does not deny that the inquisitors can repeat the question of torture
in a case where they must and can do so by law.'"

Citation tag lower-right: "Torquemada 1484, Compilación f. 6v (Argüello 1630 ed.)"

Match the period typography. No modern fonts.
```

**Three sequential highlight overlays (generate separately, composite in edit):**

**Highlight 2a — Half-proof entry** (§3 turn, ~1:35):
```
On the f. 6v screenshot, add a semi-transparent yellow (#FFE066, 40% opacity) rectangular
highlight box around the phrase: "pareciendo semiplenamente probado" (appears in the
opening clause of §XV). Box has no border, soft edges. All other text remains visible.
```

**Highlight 2b — Ratification clause** (~2:25):
```
Move the yellow highlight box to surround: "el dia siguiente, ó a tercero dia... ratificare,
o afirmare la dicha su confession" in the §XV paragraph. Same style as Highlight 2a.
```

**Highlight 2c — Loophole clause** (§4, ~2:35):
```
Move the yellow highlight box to surround the FINAL sentence of §XV:
"no se quita, que los Inquisidores puedan repetir la questión del tormento en caso que
de Derecho lo deviessen" — the last line of the paragraph.
Same yellow highlight. This is the thesis payload: rule and escape hatch on the same page.
```

**Timing:** Shot 2 holds across §1+§7. Highlights cycle through §3–§4. Slow hold on full page at §7 close (~4:55).

---

### Shot 3a — Inquisitor + Ordinario Mandate (f. 33r, Instruction 48)

**Base:** Screenshot f. 33r from the Compilación PDF.

**Nanobana overlay prompt:**
```
On a 1630 Spanish printed page (f. 33r of the Compilación), add:

1. A yellow highlight box around: "se hallen presentes todos los Inquisidores, y Ordinario,
   y assimismo a la execucion del" (Instruction 48).

2. A translation panel in period humanist roman typography, sepia ink, aged parchment:
   "All the Inquisitors and the Ordinario [bishop's representative] shall be present
   at the pronouncing of the torture sentence, and likewise at its execution."

3. Citation tag lower-right: "Valdés 1561, Instruction 48, Compilación f. 33r"

No modern typography. Match the page's 1630 print aesthetic.
```

**Timing:** §3, ~1:50. Hold 3 seconds.

---

### Shot 3b — Notary Mandate (f. 34, Instruction 55)

**Base:** Screenshot f. 34 from the Compilación PDF.

**Nanobana overlay prompt:**
```
On a 1630 Spanish printed page (f. 34 of the Compilación, Instruction 55), add:

1. A yellow highlight box around: "AL Tormento no se debe hallar presente persona alguna
   mas de los Juezes y el Notario y ministros del tormento."

2. A translation panel in period humanist roman typography, sepia ink, aged parchment:
   "At the Torture no person whatsoever should be present other than the Judges,
   the Notary, and the ministers of the torture."

3. Citation tag lower-right: "Valdés 1561, Instruction 55, Compilación f. 34"

This is the definitive personnel list. Match 1630 print aesthetic exactly.
```

**Timing:** §3, ~1:55. Hold 2.5 seconds. Cut immediately after — do not linger (the restriction clause could confuse viewers if held too long without audio context).

---

### Shot 3c — Doctor Quote Card (Kamen p. 240) — DESIGN SPEC, no nanobana

**Design spec for DaVinci Resolve / Canva:**
```
Background: warm off-white (#F5F0E8), subtle parchment texture (low opacity)
Quote text: "physicians were usually available in case of emergency"
Font: Georgia or similar serif, 28pt, dark charcoal (#2C2C2C), italic
Attribution line: "— Henry Kamen, The Spanish Inquisition: A Historical Revision, p. 240"
Sub-attribution: "Yale University Press, 4th ed. 2014"
Font size for attribution: 16pt, regular weight
Layout: centered, quote above attribution, generous white space
NO period typography — this is a scholar quote card, visually distinct from primary document shots
```

**Timing:** §3, ~2:00. Hold 2.5 seconds.

---

### Shot 4 — Three Warnings / Moniciones (f. 29r)

**Base:** Screenshot f. 29r from the Compilación PDF.

**Nanobana overlay prompt:**
```
On a 1630 Spanish printed page (f. 29r of the Compilación, Instruction 17), add:

1. A yellow highlight box around: "haciéndole tres moniciones en diferentes dias,
   con alguna interpolación."

2. A translation panel in period humanist roman typography, sepia ink:
   "Making three warnings on different days, with some interval between them."

3. Citation tag lower-right: "Valdés 1561, Instruction 17, Compilación f. 29r"

Viewer's eye should land on "tres" (three) as the audio says "warned three times."
Match 1630 print aesthetic.
```

**Timing:** §3, ~2:00. Hold 2.5 seconds.

---

### Shot 5a — Kamen p. 239 Sentence — DESIGN SPEC, no nanobana

**Design spec:**
```
Reproduce a clean facsimile of Kamen's book page. Style: academic book typography.
Font: Times New Roman or similar, 12pt body, justified, black on white.
Quote to highlight (yellow underline): "The three main ones were the garrucha, the toca and the potro."
Page header: "240    THE SPANISH INQUISITION"
Citation tag lower-right: "Henry Kamen, The Spanish Inquisition: A Historical Revision, p. 240 (Yale UP)"
Subtle cream (#FAFAF5) background to suggest book paper. Not parchment — this is a modern academic text.
```

**Timing:** §3, ~2:15. Hold 2.5 seconds before cutting to 5b.

---

### Shot 5b — Garrucha (Strappado)

**Check first:** Wikimedia Commons → search "strappado engraving" or "garrucha inquisición grabado". Use CC image if found.

**Nanobana generation prompt (if no CC image):**
```
A period woodcut or copper engraving, circa 1500-1650, showing the strappado (garrucha)
torture device. A figure is suspended from the ceiling by ropes tied to their wrists behind
their back. Weights hang from their feet. The figure is in mid-drop. Dark line work on aged
cream paper. No color. Style: 16th-century Spanish or Italian ecclesiastical woodcut, similar
to Torquemada-era illustrated manuscripts. Minimal background. The device mechanism should
be clearly visible — ceiling pulley, rope, figure, weights. No text on the image itself.
```

**Overlay (add in edit):**
```
Spanish term: "GARRUCHA" — bold, period serif typography, dark ink, upper-left
English description: "wrists bound behind back — hoisted by pulley — dropped suddenly"
Citation tag lower-right: "Hassner, Anatomy of Torture, p. 25"
```

**Timing:** §3, ~2:20. Hold 2 seconds before cutting to 5c.

---

### Shot 5c — Toca (Waterboarding)

**Check first:** Wikimedia Commons → search "toca inquisition" or "waterboarding historical engraving."

**Nanobana generation prompt (if no CC image):**
```
A period woodcut or copper engraving, circa 1500-1650, showing the toca (water torture).
A figure is reclined on a board, head tilted back, mouth forced open. A cloth (toca) is
inserted in the throat. An official pours water from a clay jar onto the cloth.
One or two officials attend. Dark line work on aged cream paper. No color.
Style: 16th-century Spanish woodcut, ecclesiastical imprint aesthetic. Clear, readable composition.
The water jar (jarro) should be visibly present.
```

**Overlay (add in edit):**
```
Spanish term: "TOCA" — bold, period serif typography, dark ink, upper-left
English description: "linen cloth inserted in throat — water poured slowly from a jar"
Citation tag lower-right: "Hassner, Anatomy of Torture, p. 25"
```

**Timing:** §3, ~2:22. Hold 2 seconds. Ties to §5 where Díaz de Cáceres receives 7 jars.

---

### Shot 5d — Potro (Rack/Cords)

**Check first:** Wikimedia Commons → search "potro inquisición cordeles" or "rack torture engraving Spanish."

**Nanobana generation prompt (if no CC image):**
```
A period woodcut or copper engraving, circa 1500-1650, showing the potro (cord torture).
A figure is bound to a rack or board. Cords are wrapped tightly around the limbs —
calves, thighs, arms. An official tightens them with a garrote stick (tourniquet method).
Dark line work on aged cream paper. No color.
Style: 16th-century Spanish woodcut. The cord-tightening mechanism should be legible.
```

**Overlay (add in edit):**
```
Spanish term: "POTRO" — bold, period serif typography, dark ink, upper-left
English description: "cords wrapped around limbs — tightened by turns"
Citation tag lower-right: "Hassner, Anatomy of Torture, p. 25"
```

**Timing:** §3, ~2:24. Hold 2 seconds before returning to §XV document.

---

### Shots 6, 7, 8 — f. 6v Sequential Highlights

These reuse the Shot 2 base image (f. 6v PDF screenshot) with different highlight positions. No additional generation needed — just composite the three highlight overlays from Shot 2 (2a, 2b, 2c) at the correct edit points:

- **Shot 8 (half-proof):** Highlight 2a — fires at §3 turn (~1:35)
- **Shot 6 (ratification):** Highlight 2b — fires when narration reads the §XV quote (~2:25)
- **Shot 7 (loophole):** Highlight 2c — fires at §4 reveal (~2:35). This is the thesis payload. After 2c fires, do NOT cut away — zoom out slightly to show full paragraph, then hold so viewer sees rule (2b) and loophole (2c) on the same page simultaneously.

---

## CATEGORY B — HANDWRITTEN COURT RECORDS

---

### Shot 13 — Inquisition Torture Session Record, Ciudad Real c. 1494

**Source text:** AHN Inquisición, Ciudad Real tribunal records, Beinart transcription series.
Trial 91 (Marina González, April 29, 1494) is undigitized — original Spanish not recoverable
without AHN access. Spanish text below is verbatim from Trial 100 (María González, same Ciudad
Real tribunal, same procedural formula, Beinart Vol. II). Scribe language is standardized across
cases; the disrobing/rack/cord sequence uses near-identical formula in both trials.
Visual labeled as "AHN Inquisición, Ciudad Real, c. 1494 — procedural transcript" (not Trial 91
specifically) to avoid attributing Trial 100 text to Trial 91.

**Full nanobana generation prompt:**
```
Generate a full-page facsimile of a late 15th-century Castilian court manuscript page.
Style: Gothic cursive (letra procesal / cortesana), the standard secretarial hand of
Castilian tribunals circa 1480-1510. Dark brown iron gall ink on yellowed parchment.
Slight ink bleeding at stroke ends. Occasional abbreviation marks above words.
Ruled horizontal lines faintly visible beneath the text (dry-point ruling, typical of period).
Page dimensions approximately 22cm × 30cm. Single column. No illumination or decoration —
this is a working court record, not a manuscript.

The text should begin mid-paragraph (the session is already in progress) with the following
authentic period Spanish, verbatim from the Ciudad Real Inquisition tribunal records:

"Sus reverencias la mandaron desnudar, amonestándola ut supra.
Fue mandada poner en la escalera e atar con los cordeles,
e estando en la escalera dixo: 'Apretenme e mátenme,
que no tengo de dezir mas de lo que tengo dicho.'
E dixo que ya tiene dicho la verdad, que avnque la hasian mil pedamos
en el tormento e en el carrillo, que no dirá otra cosa syno la verdad."

The text runs 8-12 lines. No chapter heading visible — this is the middle of a longer document.
A partial folio number faintly visible in upper-right margin in the same brown ink.
```

**Translation overlay prompt (period hand style):**
```
Generate a companion panel in the same Gothic cursive hand style, slightly lighter ink
(as if added by a different scribe or at a different time), containing the English translation:

"Their reverences ordered her to undress, admonishing her as above.
She was ordered to be put on the rack and to be tied with the cords.
And being on the rack she said: 'Tighten me and kill me,
for I have no more to say than what I have already said.'
She said that she has already told the truth, that even if they made her
into a thousand pieces in the torture, she will say nothing else but the truth."

Place this panel below the Spanish text or in the right margin. Match the handwriting
style of the primary text — not modern typography. The translation should look like
it was written on the same page by a period hand.

Below the translation, in smaller script matching the same style:
"AHN Inquisición, Ciudad Real, c. 1494 — procedural transcript
(Beinart, Records of the Trials of the Spanish Inquisition in Ciudad Real, Vol. II)"
```

**Timing:** §3, ~1:40 (introduced when Marina González is named). Hold 3 seconds on full page, then zoom slowly to the key passage as it is read aloud.

---

### Shot 14 — Díaz de Cáceres Trial Record, Mexico City 1601

**Note:** AGN Vol. 61, Exp. 159 is not digitized. Full nanobana generation. The citation tag is real — the visual is a period-accurate reconstruction.

**Full nanobana generation prompt:**
```
Generate a full-page facsimile of an early 17th-century Mexican Inquisition court manuscript.
Style: Spanish colonial secretarial hand (humanistic cursive adapted for colonial administrative
use), circa 1590-1610. Dark brown iron-gall ink on cream-colored laid paper (not parchment —
Mexican Inquisition records typically used European laid paper). Horizontal chain lines visible.
Light water-staining at upper right edge. Occasional crossed-out words with single horizontal
strike (corrections typical of notarial records). Single column, dense text.

The document begins with a formal heading in slightly larger script:
"Processo contra Antonio Diaz de Caceres. Año de 1596."

Then the body text in normal secretarial hand includes content describing (in period Spanish):
— The date: "En la ciudad de Mexico, a dos dias del mes de Março de mil y seiscientos y vn años"
  [March 2, 1601]
— The charge: Judaizing
— The session: being raised by the garrucha, the application of cordeles, the water jars
— The key phrase indicating silence: "dixo que le matavan, pero no confesso cosa alguna"
  ["he said they were killing him, but he confessed nothing"]

Run 10-14 lines of dense secretarial script. Period abbreviations (q̃ for que, p̃ for per).
Folio number "fol. 61" in upper-right margin.
```

**Translation overlay prompt (period hand style):**
```
Generate a companion panel in the same 17th-century colonial secretarial hand, slightly lighter ink,
containing the English translation of the key passage:

"March 2, 1601. Mexico City.
He was hoisted to the ceiling by ropes — twelve times.
Ropes wrapped around his calves, thighs, and shins — tightened twelve times.
Seven jars of water forced down his throat.
'He screamed that they were killing him. He revealed nothing.'"

Place below the Spanish text or in the right margin. Match the handwriting style.
Below in smaller script: "AGN México, Inquisición, Vol. 61, Exp. 159, Parte 1 (1596–1601)"
```

**Timing:** §5, ~3:15. Hold on heading (1 sec) then slow pan down to the session record as the torture details are narrated. The key phrase "dixo que le matavan" should be visible when the audio hits "screamed they were killing him."

---

## CATEGORY C — QUOTE CARDS (Design specs — no image generation)

---

### Shot 9 — Silence = Innocence (Hassner p. 145)

```
Background: warm off-white (#F5F0E8)
Quote text (italic, 26pt Georgia):
"The Inquisition... interpreted silence as a divinely inspired proof of innocence."
Attribution (16pt, regular): "— Prof. Ron Hassner, UC Berkeley"
Sub-attribution (13pt): "Anatomy of Torture (Cornell University Press, 2022), p. 145"
Layout: centered, generous vertical padding
Style: clean modern academic — visually DISTINCT from period document shots
```

---

### Shot 11 Beat 1 — CIA "Hot Blood" (Hassner p. 17)

```
Background: warm off-white (#F5F0E8)
Quote text (italic, 26pt Georgia):
"This was hot-blooded torture."
Attribution (16pt): "— Hassner, Anatomy of Torture, p. 17"
Sub-attribution (13pt): "contrasted with the Inquisition's 'cold-blooded' bureaucratic procedure"
```

### Shot 11 Beat 2 — SSCI Report Cover

Use actual PDF screenshot of the SSCI 2014 executive summary cover/title page.

**Overlay (add in edit):**
```
Add citation tag lower-right: "Senate Intelligence Committee, CIA Detention Study, Dec. 9, 2014"
Add small text lower-left: "(Hassner's primary source for the CIA comparison, n. 34, p. 158)"
```

---

### Shot 15 — Converso Toledo Writer (Kamen p. 232)

```
Background: warm off-white (#F5F0E8)
Opening line (12pt, regular, italic, dark gray): "A converso writer in Toledo, 1538:"
Quote text (italic, 26pt Georgia):
"Continual fear is a worse death than a sudden demise."
Attribution (16pt): "— Kamen, The Spanish Inquisition: A Historical Revision, p. 232"
Sub-attribution (13pt): "Source: AHN Inquisición, Leg. 1867, No. 36 (cited in Kamen, Ch. 9, n. 3)"
                         "Probable author: Sebastián de Horozco, Toledo (c. 1510–1581)"
```

**Note:** The AHN archive reference in the sub-attribution is the Auditor's Edge even without the scan — it shows the source chain behind Kamen's quote.

---

### Shot 16 — 3,000 Executions (Kamen p. 254)

```
Background: warm off-white (#F5F0E8)
Quote text (italic, 26pt Georgia):
"A maximum of three thousand persons may have suffered death during
the entire history of the tribunal."
Attribution (16pt): "— Henry Kamen, The Spanish Inquisition: A Historical Revision, p. 254"
Sub-attribution (13pt): "Yale University Press, 4th ed. 2014"
```

---

## Shot sequence summary

| Shot | Timing | Base | Nanobana needed? |
|---|---|---|---|
| 1 | §1 ~0:25 | PDF screenshot | Translation overlay only |
| 2 / 8 / 6 / 7 | §1+§3+§4 | PDF screenshot f. 6v | Three highlight overlays |
| 3a | §3 ~1:50 | PDF screenshot f. 33r | Highlight + translation overlay |
| 3b | §3 ~1:55 | PDF screenshot f. 34 | Highlight + translation overlay |
| 3c | §3 ~2:00 | — | Design spec (quote card) |
| 4 | §3 ~2:00 | PDF screenshot f. 29r | Highlight + translation overlay |
| 5a | §3 ~2:15 | — | Design spec (book page facsimile) |
| 5b | §3 ~2:20 | CC image or full gen | Illustration + overlay |
| 5c | §3 ~2:22 | CC image or full gen | Illustration + overlay |
| 5d | §3 ~2:24 | CC image or full gen | Illustration + overlay |
| 9 | §5 ~3:50 | — | Design spec (quote card) |
| 11 Beat 1 | §2 ~1:10 | — | Design spec (quote card) |
| 11 Beat 2 | §2 ~1:15 | SSCI PDF screenshot | Citation overlay only |
| 13 | §3 ~1:40 | Full gen (handwritten) | Full generation + translation |
| 14 | §5 ~3:15 | Full gen (handwritten) | Full generation + translation |
| 15 | §6 ~4:00 | — | Design spec (quote card) |
| 16 | §6 ~3:55 | — | Design spec (quote card) |
