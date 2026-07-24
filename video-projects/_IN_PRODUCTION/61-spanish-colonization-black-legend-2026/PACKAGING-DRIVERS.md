# PACKAGING DRIVERS — what made the popular comps win (#61)
_2026-06-18. Scan of the real comp set (view counts + titles from `.info.json`; hooks from auto-subs; thumbnails downloaded + visually inspected — no fabrication). Feeds the title + thumbnail lock. Packaging = the channel's #1 growth bottleneck._

## POPULARITY LANDSCAPE (real view counts)
| Views | Dur | Channel | Title | Relevance |
|---|---|---|---|---|
| 10.8M | 11:19 | CrashCourse | "The Black Legend, Native Americans, and Spaniards" | school/brand traffic, not packaging model |
| 3.7M | 45m | HISTORY | "Engineering an Empire: The Aztecs" | TV episode |
| 3.1M | 6:16 | RealLifeLore | "What If All Spanish Speaking Countries United Today?" | our overlap audience; hypothetical |
| 2.4M | 101m | Knowledgia | "How were The Americas Colonized? — The Entire History" | survey; question hook |
| 1.9M | 5:41 | TED-Ed | "Ugly History: The Spanish Inquisition" | Inquisition (we CUT) |
| 1.85M | 14:06 | Kings & Generals | "Aztecs: Arrival of Cortes and the Conquistadors" | conquest |
| **1.26M** | 19:33 | **Armchair** | **"FALL of the Aztecs: How 400 Spaniards Toppled an Empire"** | **hook-title winner = OUR cold open** |
| 854K | 22:08 | Voices of the Past | "Aztec Perspective on First Contact… 16th century" | **method validator (document-led)** |
| 835K | 31m | Whatifalthist | "Understanding Latin America" | grand-narrative |
| 801K | 13:02 | Kings & Generals | "Spanish Conquest of the Incan Empire" | Inca |
| 219K | 13:43 | History Guy | "Potosi: The Silver Mine that Changed the World" | silver |
| **20.7K** | **41:10** | **Hipstorian** | **"The Black Legend: How Propaganda Shapes History"** | **our direct referee comp — FLOPPED. Cautionary.** |

## HOOK PATTERNS (how the winners OPEN — verbatim from subs)
- **Armchair (1.26M):** opens DRY/chronological — "at the start of 1519 the Aztec Empire was a dominant force in Mesoamerica…" → **the curiosity gap is in the TITLE, not the script open.** The "How 400 Spaniards" promise sells the click; the video then teaches.
- **K&G Inca (801K):** cinematic scale + modern relevance — "500 years ago atop the snow-capped Andes… two new empires smashed into each other in a collision that reverberates [today]."
- **Knowledgia (2.4M):** question-stack — "Why did the Europeans colonize the Americas? What drove…"
- **Hipstorian (20.7K, referee comp):** opens on the **2020 BLM statue-topplings** — i.e. led with the Columbus-Day culture-war register. → **direct evidence to open on the DOCUMENT (native civil war) and save the modern war for the CLOSE.** The one video with our thesis led with the swamp register and underperformed.

## THUMBNAIL PATTERNS (downloaded + inspected)
- **Armchair "CONQUEST" (1.26M):** bold illustrated conquistador (helmet/plume, wide-eyed) + gold coins + stylized map with red arrows + giant pointing hand + "GOLD" repeated; one big word "CONQUEST." Illustrated, energetic, single-word overlay, map element. NO face (illustrated character).
- **CrashCourse "NATIVES & SPANIARDS" (10.8M):** flat brand illustration + bunting + banner text. Brand-driven, not a model.
- **Voices of the Past "THE AZTECS ON THE FIRST EUROPEANS" (854K):** clean SPLIT — left Aztec pyramid + turquoise mosaic skull; right a colonial landing painting. **Real primary-source ART, no face, big legible text top+bottom, contrast composition.** ← This is the document-led channel's packaging, and it maps to OUR identity + playbook (text overlay 87% niche, no face 0%, primary sources on screen).
- **Hipstorian referee (20.7K):** a de Bry/codex ATROCITY image (Spaniard abusing a native) + the host's FACE (bearded, glasses) + "The Spanish / The Cruellest People Of Europe." → **Two mistakes for a referee video:** (1) FACE (0% niche outlier rate), (2) thumbnail is BLACK-LEGEND-coded ("Cruellest People" + atrocity image) on a video that concludes "neutral gray" — packaging contradicts thesis. Avoid both.

## SYNTHESIS → OUR PACKAGING
**The opening:** open on the **document/native-civil-war** (Armchair proves the hook belongs in the title; Hipstorian proves leading with the modern statue-war underperforms). Modern frame → CLOSE only.
**The thumbnail (recommended):** **document-SPLIT, no face, 2–4 word overlay** — the de Bry atrocity engraving (Black) | a clean law/treaty/ledger page (White), split down the middle = the referee thesis MADE VISUAL. This borrows Voices-of-the-Past's proven document-art-split (854K) and fixes Hipstorian's face + one-sided coding. Maps optional (territorial element like Armchair) but the split is stronger for the dual-legend thesis. Run `thumbnail_checker.py` / `/thumbnail` against this.
**The title:** lead with the **"black legend"** search anchor (39.8K/mo @66 VidIQ), **two-sentence declarative, NO colon** (colon tanked the keyword-led variants to 32–39).

### Title candidates (title_scorer --db --topic ideological; FILTER not predictor — feed to VidIQ A/B)
| Score | Title | Note |
|---|---|---|
| **60 (C)** | **"The Black Legend Is Real. So Is the Lie That Replaced It."** | keyword anchor + two-sentence + referee thesis + no colon — **recommended lead** |
| 56 (D) | "How 900 Spaniards Toppled the Aztec Empire (They Didn't)" | Armchair-family number/curiosity; no Black-Legend anchor |
| 55 (D) | "The Spanish Didn't Conquer the Aztec Empire. Their Neighbors Did." | native-civil-war, two-sentence; strong cold-open match |
| 55 (D) | "The Two Biggest Lies About the Conquistadors" | "conquistadors" anchor, referee |
| 32–39 (F) | colon variants ("The Black Legend: …") | colon penalty — drop the colon, same idea rises |
> Per the channel's A/B method: pair the **#1 (keyword+referee)** with a **thumbnail that carries the curiosity**, and test against the **#3 (native-civil-war)** as the alt. Lock via VidIQ chat (keyword vol + competition) + native A/B rotation, not the scorer alone.

## GAPS WE OWN (none of the popular comps occupy)
- A **tight (<12 min) referee** — the only referee (Hipstorian) is 41 min AND flopped on packaging. Unoccupied.
- **Document-on-screen PROOF** of the dual-legend thesis (VoP proves the format sells; nobody applies it to the legends).
- **Khipu** — 0/13 comps. **Huaca Toledo ledger** — 0 comps. **Silver-to-China conduit** — 0 comps synthesize it.
