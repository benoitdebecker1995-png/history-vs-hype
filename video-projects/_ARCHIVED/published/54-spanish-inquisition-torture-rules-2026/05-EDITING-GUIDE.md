# Editing Guide — #54 Spanish Inquisition

**Source:** `rough cut.srt` vs `02-SCRIPT-DRAFT.md` (DRAFT, three passes complete 2026-05-08)
**Region covered:** Full video, 7:48 (target was 5:00 — +56% overshoot, see Pacing)
**Generated:** 2026-05-11
**Status:** Rough cut filmed; ship as Format-C close-read vibes test per `04-ROUGH-CUT-POSTMORTEM.md`

> All timecodes in this guide are **VIDEO time** (SRT minus 1-hour offset). The SRT itself is offset by 01:00:00. Run `/fix` before final captioning — it handles the offset and the typos in one pass.

---

## TL;DR — top 7 actions

1. **🚨 RE-RECORD §6 line at 06:54** — audio says *"a worse **enemy** than a sudden demise"*; correct word is **"death"** (Kamen p.232 verbatim). Single-line pickup, ~5 seconds. Drop in over the existing Shot 16 quote card. Audio/visual mismatch on a "show-you-the-sources" channel = self-inflicted credibility hit.
2. **Run `/fix` before burn-in captions** — at least 18 proper-noun/foreign-term transcription errors detected (Hassner ×4, Torquemada ×2, Compilación, Instrucciones, Marina González, Díaz de Cáceres, Ciudad Real, Kamen ×2). See Section 6.
3. **Generate the §XV f.6v centerpiece (Shot 2) FIRST** — it appears 4× across the video (00:37 / 02:44 / 03:17 / 07:13) with three sequential highlight reveals. One PDF screenshot, three highlight overlay layers in DR. Block all other facsimile work behind this.
4. **Doctor claim at 02:23 → use Shot 3c (Kamen p.240 quote card), NOT Instruction 55** — the primary text restricts the chamber to "Judges, Notary, and ministers" and excludes the doctor. Showing f.34 here would contradict the audio. See `01-VERIFIED-RESEARCH.md` Claim 2.4c.
5. **Hook B-roll: lead with de Bry engravings (1598) on the Black Legend setup** — the propaganda images everyone has in their head, not the reality. Transition to Compilación title page (Shot 1) on "they wrote one" at 00:15. The visual switch is the thesis.
6. **Drop the §5 emotional beat into silence**, not under music — "He'd been protecting people who were already gone" (05:43) carries more weight bare. Music re-enters at §6 transition.
7. **§7 close = Shot 2 with all 3 highlights visible simultaneously** at 07:28 ("the clause that made all of it negotiable"). The page itself is the climax visual. Slow hold to 07:43 before subscribe card.

---

## Segment 1 — Black Legend hook (00:00 → 00:11)

**SRT lines 1–6 — what's on tape:**
> *"Everyone thinks they know what the Spanish Inquisition was. Torture chambers, thumbscrews, dungeons where people disappeared, centuries of religious terror operating entirely outside the law."*

**vs script said:**
> Same content, near-identical phrasing. Script said "outside any law"; tape says "outside the law" — minor.

**Verdict:** KEEP. Clean read, hook lands.

**Issues:**

| # | Timestamp | Issue | Fix |
|---|---|---|---|
| 1 | 00:00 → 00:11 | No issues — clean delivery | None |

**B-roll for segment (talking head + period propaganda imagery):**

- **00:00 → 00:06** — De Bry, *The Inquisition in Europe* engravings (1598). Wikimedia Commons: `Category:Theodor de Bry — The Inquisition in Europe`. Pulley + pyre images. **The mythos visual — Protestant propaganda the rest of the video dismantles.**
- **00:06 → 00:11** — Limborch, *Historia Inquisitionis* fold-out plates (1692). Archive.org: search "Historia Inquisitionis Limborch" — look for "Instruction of the Torture" plates (1731 English translation has higher contrast). **The bureaucratic-torture composition: scribe taking notes while victim is bound — already nodding at the channel's thesis without saying it.**

**Music:** Single low pad. No melody yet. Set up tension.

---

## Segment 2 — Turn ("That last part, outside the law…") (00:11 → 00:15)

**SRT lines 7–8:**
> *"That last part, outside the law, is where the story breaks down."*

**Verdict:** KEEP. This is your turn moment — script's exact phrasing.

**Issues:**

| # | Timestamp | Issue | Fix |
|---|---|---|---|
| — | — | None | — |

**B-roll:**
- **00:11 → 00:15** — Hold on a final de Bry/Limborch engraving with slight desaturation push (visual signal: "we're about to leave the myth"). OR cut to talking head on the turn word "breaks down" — emphasizes the pivot.

**Music:** Pad continues. Don't swell here — the swell goes on Shot 1.

---

## Segment 3 — "They wrote one" → Compilación reveal (00:15 → 00:43)

**SRT lines 9–24:**
> *"They didn't act outside the law, they wrote one. The rules for torture, who had to be in the room, what could and couldn't be done, what made a confession legally valid, and the exceptions. This is the Compilation de las Insuciones, the procedural manual for running an Inquisition Tribunal written in 1484 and used for over two centuries. One paragraph in particular contains everything the rest of this video is about. Paragraph 15."*

**vs script said:**
> Script: *"They didn't act outside the law. They wrote one — and they wrote it down."* — DROPPED "and they wrote it down."
>
> Postmortem confirms intentional cut for trim. **Verdict: KEEP your version.** The "wrote it down" line was a redundant beat.

**Issues:**

| # | Timestamp | Issue | Fix |
|---|---|---|---|
| 2 | 00:27 (line 17) | "Compilation de las Insuciones" — auto-transcription. You said "Compilación" correctly. | Caption fix only. `/fix` will catch. |

**B-roll for segment (THIS IS THE RVEAL):**

- **00:15 → 00:19** — Hold on talking head OR last propaganda image, slight darken. Land *"they wrote one"* on a beat.
- **00:19 → 00:27** — Slow zoom out FROM darkened propaganda image OR straight cut to **Shot 1 (Compilación title page)** as you say *"the rules for torture..."* The visual switch from de Bry → Compilación = the thesis in one cut.
- **00:27 → 00:37** — **Shot 1 hold, slow push in.** The full title page should be readable for ~9 seconds. Highlight "Instrucciones" at ~00:32 (yellow #FFE066, 40% overlay). Citation tag lower-right: "Argüello 1630, Compilación de las Instrucciones."
- **00:37 → 00:43** — **Cut to Shot 2 (f.6v full page).** No highlight yet. The page is the new visual fact. Hold through "Paragraph 15" — let the audience see it before you name it.

**Asset status:**
- Shot 1: ⚠️ Needs PDF screenshot (Compilación title page) + nanobana overlay generation per `NANOBANA-PROMPTS.md` Shot 1
- Shot 2: ⚠️ Needs PDF screenshot of f.6v (CRITICAL — appears 4× in video; ONE good screenshot, 3 highlight layers in DR)

**Music:** Pad swells slightly on the cut to Shot 1 at 00:19. Hold under Shot 1. Drop to silence on the cut to Shot 2 at 00:37 — silence on "Paragraph 15" is the hook payoff.

---

## Segment 4 — Torquemada and Hassner intro (00:43 → 01:05)

**SRT lines 25–35:**
> *"The Insuciones were written in 1484 by Tomá de Torqumeda, the first Grand Inquisitor. It contained the rules for everything. How to investigate suspected heretics, how to interrogate them, how to torture them, how to sentence them. Ron Hessner, a political scientist at UC Berkeley, spent years in the Inquisition archives. Here's what he found."*

**Verdict:** KEEP. Clean delivery.

**Issues:**

| # | Timestamp | Issue | Fix |
|---|---|---|---|
| 3 | 00:46 (line 26) | "Tomá de Torqumeda" → "Tomás de Torquemada" | Caption fix only. `/fix` |
| 4 | 01:01 (line 32) | "Ron Hessner" → "Ron Hassner" | Caption fix only. `/fix` (recurs lines 45, 49 — multiple instances) |

**B-roll for segment:**

- **00:43 → 00:51** — Berruguete, *St. Dominic Presiding over an Auto-da-fé* (c. 1495). Wikimedia Commons: `Category:Pedro Berruguete — Saint Dominic Presiding over an Auto-da-fe`. The figure on the throne is the standard contemporary visual stand-in for Torquemada's era. **Caption overlay: "Berruguete, c. 1495 — Torquemada's lifetime"** (small lower-right; transparent about it being a stand-in, not a portrait).
- **00:51 → 00:58** — Cut to **Shot 1 callback** (Compilación title) OR to a 1576 edition title page (Google Books / HathiTrust: search "Instrucciones del Oficio de la Santa Inquisición") — show the rulebook is real, dated, official. Carries through *"how to investigate, interrogate, torture, sentence."*
- **00:58 → 01:05** — Cut to **Hassner book cover** (*Anatomy of Torture*, Cornell University Press 2022). Land on the cover during *"Ron Hassner, a political scientist at UC Berkeley."*

**Music:** Light bed continues. No swell.

---

## Segment 5 — Hassner "cold blood" quote + CIA contrast (01:05 → 01:32)

**SRT lines 36–47:**
> *"The torture practices of the Inquisition were the result of centuries of institutional learning. It tortured as part of a bureaucratic procedure designed to collect information. It tortured in cold blood. After 9-11, CIA interrogators tortured rashly with no oversight and no records. Hessner called that 'hot-blooded torture, improvised, vindictive, and reserved for whoever seemed guilty.'"*

**Verdict:** KEEP. The cold/hot blood beat is the modern-relevance anchor.

**Issues:**

| # | Timestamp | Issue | Fix |
|---|---|---|---|
| 5 | 01:25 (line 45) | "Hessner" again | `/fix` will catch all four instances |

**B-roll for segment:**

- **01:05 → 01:18** — **Hassner quote card** for "cold blood" passage. Per `NANOBANA-PROMPTS.md` quote card spec: `#F5F0E8` background, Georgia serif 26pt italic, citation "Hassner, *Anatomy of Torture*, p. 18." Match the existing Shot 9 / Shot 11 visual style.
- **01:18 → 01:25** — Cut to **SSCI 2014 report cover** (Senate Select Committee on Intelligence, Committee Study of CIA Detention and Interrogation Program). Available on govinfo.gov. **Then "scroll down" effect** to the heavily redacted Table of Contents.
- **01:25 → 01:32** — Cut to declassified CIA cable with "Top Secret" header + black-bar redactions. National Security Archive ("Torture Archive CIA"). Look for Abu Zubaydah cables 2002–2005. **Avoid Abu Ghraib photos** — the contrast we want is institutional/documentary (paperwork-as-evidence), not gore. Caption overlay: "SSCI Study, 2014 — heavily redacted."

**Music:** Bed dims at "cold blood." Silence under the SSCI cut for ~2s. Bed re-enters as the camera scrolls into redactions.

---

## Segment 6 — "That's why we know what happened to Marina González" (01:32 → 01:46)

**SRT lines 48–54:**
> *"The Inquisition is the opposite of that. Hessner called it 'the most extraordinary interrogational torture campaign in recorded history.' And the Inquisition's record survived. That's why we know exactly what happened to Marina Gonzalez."*

**Verdict:** KEEP. Clean transition into the case.

**Issues:**

| # | Timestamp | Issue | Fix |
|---|---|---|---|
| 6 | 01:46 (line 54) | "Marina Gonzalez" → "Marina González" | Caption fix only. `/fix` |

**B-roll for segment:**

- **01:32 → 01:40** — Hold on talking head OR Hassner quote card with second pull-quote ("most extraordinary interrogational torture campaign in recorded history"). Per existing Shot 11 spec.
- **01:40 → 01:46** — **Lead-in to Shot 13** (Marina González record). Start the page transition before her name lands — name and face/document hit together at 01:46.

**Music:** Bed re-enters fully. This is the bridge into the case.

---

## Segment 7 — Marina González scene (01:47 → 02:06)

**SRT lines 55–64:**
> *"April 29th, 1494, Ciudadreale, Spain. A scribe sits beside Marina Gonzalez in the torture chamber. Not to help her, but to write everything down. The scribe's first line: 'She was stripped of her old skirts and put on the rack, and her arms and legs were tied tightly with cords.'"*

**Verdict:** KEEP. The scene works as written.

**Issues:**

| # | Timestamp | Issue | Fix |
|---|---|---|---|
| 7 | 01:51 (line 55) | "Ciudadreale" → "Ciudad Real" | Caption fix only. `/fix` |
| 8 | 01:54 (line 56) | "Marina Gonzalez" recurrence | `/fix` will catch all instances |

**B-roll for segment:**

- **01:47 → 01:58** — **Shot 13 (Marina González record / Ciudad Real procedural transcript).** Full-page facsimile first. Hold static ~10 seconds. Per `NANOBANA-PROMPTS.md` Shot 13: 15th-century Castilian Gothic cursive, iron gall ink, citation tag "AHN Inquisición, Ciudad Real, c. 1494 — procedural transcript (Beinart, *Records of the Trials*, Vol. II)."
- **01:58 → 02:06** — **Slow zoom from full page to the key passage** (the disrobing/rack/cords lines). English overlay panel appears at ~02:00 in matching period hand style. Land the overlay text as the audio reads it.

**Asset status:** ⚠️ Shot 13 needs full nanobana generation BEFORE this segment can be edited. Use Trial 100 (María González) verbatim Spanish from notebook as text base — labeled as procedural transcript, not Trial 91 specifically. See `NANOBANA-PROMPTS.md` Shot 13.

**Music:** Bed quiets. Let the scribe's words land in near-silence.

---

## Segment 8 — Article 15 → personnel + warnings + methods (02:07 → 02:44)

**SRT lines 65–84:**
> *"The only reason we have this record is because Article 15 required it. To legally authorize a torture session, the Intrixiones required four people in that room before anyone touched her. The Inquisitor, a representative of the local bishop, a notary to record every word spoken, and a doctor monitoring the prisoner's condition throughout. Before any of that, the accused had to be warned three times on separate days, given a chance to confess voluntarily. Only after a written order from the Inquisitors could a torture session begin, limited to three methods chosen because they were the least likely to cause prominent injury."*

**Verdict:** KEEP. This is the procedural-rules dump — the spine of §3.

**Issues:**

| # | Timestamp | Issue | Fix |
|---|---|---|---|
| 9 | 02:14 (line 68) | "Intrixiones" → "Instrucciones" | Caption fix. `/fix` |
| 10 | 02:44 (line 84) | "prominent injury" → script said "permanent injury" | Verbal stumble. **Decide:** caption-fix to "permanent" (cleanest) OR pickup-record the line (overkill for a single word). **Recommend caption-fix only** — burned-in caption shows "permanent" and audio is close enough that no one notices. |

**B-roll for segment (multi-shot, paced):**

- **02:07 → 02:11** — **Shot 2 callback** (f.6v full page) on *"Article 15 required it."* No highlight — just the page itself reasserting itself. ~4 seconds.
- **02:11 → 02:17** — **Shot 3a (f.33r — inquisitor + ordinario)** on *"four people in that room."* Spanish verbatim *"se hallen presentes todos los Inquisidores, y Ordinario... y el Notario"* highlighted. English overlay below.
- **02:17 → 02:23** — Quick cut or transition to **Shot 3b (f.34 Instr.55 notary clause)** as you say *"a notary to record every word spoken."* Hold ~3s.
- **02:23 → 02:27** — **🚨 CRITICAL: Cut to Shot 3c (Kamen p.240 quote card), NOT Instruction 55 f.34.** As you say *"a doctor monitoring the prisoner's condition throughout"*, the visual MUST be the Kamen quote card: *"the doctor who in 1702 claimed back payment for his presence at 434 sessions of torture."* Per `01-VERIFIED-RESEARCH.md` Claim 2.4c: Instruction 55 explicitly excludes the doctor from the chamber. Showing f.34 here would contradict the audio.
- **02:27 → 02:33** — **Shot 4 (f.29r — three warnings)** on *"warned three times on separate days."* Highlight the Spanish phrase *"tres moniciones."*
- **02:33 → 02:44** — **Shot 5a (Kamen p.239 quote card naming the three methods).** Spanish-italic overlay: *garrucha / toca / potro.* Hold through end of segment.

**Asset status:**
- Shots 1, 2, 3a, 3b, 4: ⚠️ Need PDF screenshots from Compilación PDF on disk + nanobana overlays
- Shot 3c: design as quote card per `NANOBANA-PROMPTS.md` Category C
- Shot 5a: same — quote card

**Music:** Bed continues, low. Don't break for any of these — the rapid-fire rule list is its own rhythm.

---

## Segment 9 — Ratification clause (02:44 → 03:11)

**SRT lines 85–99:**
> *"If the prisoner confessed, here's what paragraph 15 says, word for word. 'If the accused confesses the crime under torture, and afterward ratifies or confirms his confession on the next or third day, he shall be punished as convicted.' In other words, a confession under torture couldn't convict you on its own. What counted was coming back the next morning, unbound and free, and repeating the same thing voluntarily in front of witnesses. The evidence wasn't what you said under torture, it was the ratification."*

**vs script said:**
> Script's ratification quote is verbatim identical. Script DID NOT have *"If the prisoner confessed, here's what paragraph 15 says..."* lead-in — that was added live. **Verdict: KEEP your lead-in** — sets up the verbatim block better.

**Issues:**

| # | Timestamp | Issue | Fix |
|---|---|---|---|
| — | — | None | — |

**B-roll for segment:**

- **02:44 → 02:50** — **Shot 2 return (f.6v full page).** No highlight yet. Anticipation hold.
- **02:50 → 02:53** — Highlight 1 appears: *"semiplenamente probado"* (half-proof entry condition). Yellow #FFE066, 40% opacity.
- **02:53 → 02:59** — Highlight 1 fades to soft state; **Highlight 2 appears: ratification clause** *"el dia siguiente, ó a tercero dia ratificare"* — as the audio reads the verbatim quote. English overlay panel appears below the page.
- **02:59 → 03:11** — Hold on Shot 6 (f.6v Highlight 2 active). Slowly fade English overlay out at 03:08 so the page itself carries the closing voiceover.

**Music:** Drop bed at start of verbatim quote (02:50). Silence under the quote. Re-enter quietly at *"In other words..."* (02:59).

---

## Segment 10 — The loophole reveal (03:17 → 03:36)

**SRT lines 100–110:**
> *"Now read the last line of that same paragraph. 'The aforesaid does not deny that the Inquisitors can repeat the question of torture in a case where they must and can do so by law.' This phrase is cited by historians to conclude that torture could only occur once. Why else would you use the word repeat as an exception?"*

**vs script said:**
> Script had this paragraph differently — *"Same article, same page — the rule and its escape hatch, written together"* — DROPPED.
>
> Postmortem confirms: this was the live patch (Finding 1 — Loophole-without-rule) that added the historian-attribution scaffolding. **Verdict: KEEP your version.** It does what the script's original line could not — names the historian's interpretation, anchors it to the word "repeat," makes the loophole's contradiction legible. **This is the strongest improvisation of the rough cut.**

**Issues:**

| # | Timestamp | Issue | Fix |
|---|---|---|---|
| — | — | None — best beat in the whole video | — |

**B-roll for segment (THE PAYOFF):**

- **03:17 → 03:20** — **Shot 2 prep (f.6v full page).** Hold ~3 seconds in silence. *"Now read the last line of that same paragraph"* is voiceover; visual is anticipation.
- **03:20 → 03:28** — **Highlight 3 appears: the loophole sentence** *"no se quita, que los Inquisidores puedan repetir la questión del tormento."* Audio reads the English translation simultaneously. English overlay below.
- **03:28 → 03:36** — Hold on Shot 7 (f.6v Highlight 3 active). All three highlights now visible on the same page. Slow push in to ~110% scale during the historian-attribution voiceover.

**Music:** Hard silence under Highlight 3 reveal. Bed re-enters slowly at 03:28 with a low minor pad. THIS is the dramatic beat — protect it from music until the reveal lands.

---

## Segment 11 — Suspension explanation + Hassner quote (03:37 → 04:05)

**SRT lines 111–124:**
> *"In practice, Inquisitors called this suspension. Instead of ending a torture session, you suspend it, and the next session is legally a continuation of the first, which means the prohibition on repeat torture technically never applies. Hasner writes, 'The procedures of the Inquisition prohibited torturing an individual more than once. This guideline could be circumvented by suspending a torture session, rather than ending it.'"*

**vs script said:**
> Script also had: *"The loophole wasn't discovered later or added by someone else — it was written into the original text by the same hand that wrote the rule. Multi-day torture wasn't an abuse of the system. It was built in from day one."* — DROPPED.
>
> Postmortem confirms: trim. **Verdict: KEEP your version.** "Built in from day one" was over-asserting the same beat. The Hassner quote does the work cleaner.

**Issues:**

| # | Timestamp | Issue | Fix |
|---|---|---|---|
| 11 | 03:55 (line 119) | "Hasner" → "Hassner" | `/fix` |

**B-roll for segment:**

- **03:37 → 03:53** — **Talking head** with occasional cut-aways to Shot 7 (f.6v loophole highlight) on the word *"suspend."* The "suspension" mechanism is a verbal explanation — let the page reappear briefly to anchor it.
- **03:53 → 04:05** — **Shot 9 (Hassner suspension quote card).** Per `NANOBANA-PROMPTS.md` quote card spec. Citation: "Hassner, *Anatomy of Torture*, p. 27."

**Music:** Bed continues quiet. No swell — the §4 climax was already at 03:20.

---

## Segment 12 — Atlantic transition + Díaz de Cáceres setup (04:06 → 04:18)

**SRT lines 125–130:**
> *"A century later, those same instructions were in use on the other side of the Atlantic. March 2, 1601, Mexico City. Hasner reconstructs the case from the surviving Inquisition trial records."*

**Verdict:** KEEP. Clean transition.

**Issues:**

| # | Timestamp | Issue | Fix |
|---|---|---|---|
| 12 | 04:14 (line 129) | "Hasner" again | `/fix` |

**B-roll for segment:**

- **04:06 → 04:10** — **Map of Spanish empire c. 1600** showing Atlantic span Spain → Mexico. Wikimedia Commons: search "Spanish Empire 1600 map" or "Spanish viceroyalties." Highlight Spain → New Spain transit. ~4 seconds.
- **04:10 → 04:14** — **Trasmonte, *Forma y Levantado de la Ciudad de México* (1628).** Wikimedia Commons: search "Plano de la Ciudad de México 1628 Trasmonte." Bird's-eye view of Mexico City — pan to the Zócalo. Caption: "Mexico City, c. 1600 — Trasmonte 1628."
- **04:14 → 04:18** — Cut to **Shot 14 (Díaz de Cáceres trial record)** as you name him. Hold the page entry through end of segment.

**Music:** New bed enters on the Atlantic transition. Slightly different texture than §3-§4 — signal "we've moved continents."

---

## Segment 13 — Díaz de Cáceres backstory: charge, family, four years (04:18 → 05:00)

**SRT lines 131–153:**
> *"Antonio Diaz de Caceres is brought to the torture chamber. He's been in an Inquisition cell since December 1596. The charge? Judaizing, secretly practicing Jewish rites after forced conversion to Christianity. His family members have already testified against him. After his first interrogation in 1597, he sat in his cell for nearly three years without questions or contacts. The Inquisition kept prisoners incommunicado. Hasner again, 'The prisoner could receive no information from friends or relatives about who was arrested subsequently or who testified before the tribunal.' Four years passed before they brought Diaz back to the chamber."*

**Verdict:** KEEP. The 4-year incommunicado detail is the most powerful scene-setting in §5.

**Issues:**

| # | Timestamp | Issue | Fix |
|---|---|---|---|
| 13 | 04:20 (line 131) | "Antonio Diaz de Caceres" → "Antonio Díaz de Cáceres" | `/fix` |
| 14 | 04:46 (line 146) | "in incommunicado" → "incommunicado" (extra "in") OR caption shows the spoken "in incommunicado" — verify on tape. If verbal, leave; if SRT artifact, fix. | Verify and decide |
| 15 | 04:47 (line 147) | "Hasner" again | `/fix` |
| 16 | 04:58 (line 153) | "Diaz" without accent | `/fix` |

**B-roll for segment:**

- **04:18 → 04:33** — **Shot 14 hold** (Díaz trial record, full page). Slow zoom into a section. Per `NANOBANA-PROMPTS.md` Shot 14 — full nanobana generation, citation "AGN México, Inquisición, Vol. 61, Exp. 159, Parte 1."
- **04:33 → 04:43** — **Inquisition trial record from PARES** (search "Proceso de fe Antonio Díaz de Cáceres" — though previous attempts to load PARES failed; if still inaccessible, use Shot 14 with closer zoom). Tier-A backup: Inquisition trial folio from Holy Office Mexico Collection on PARES if loadable. Caption overlay: "AGN México, Inq., Vol. 61, Exp. 159 — undigitized; visual is period-style facsimile."
- **04:43 → 04:55** — Cut to **Hassner quote card** for "incommunicado" passage. Per quote card spec. Citation: "Hassner, *Anatomy of Torture*, p. 116" (verify exact page in Hassner journal article PDF).
- **04:55 → 05:00** — Return to **Shot 14**, slight zoom out — re-establish the document is still the visual frame.

**Asset status:** ⚠️ Shot 14 needs full nanobana generation. AGN reference not digitized — use AGN citation tag with period-style reconstruction.

**Music:** Bed quiet under the four-year passage. Silence at *"Four years passed before they brought Díaz back to the chamber"* (04:55) — the duration is the gut-punch.

---

## Segment 14 — Torture session description (05:00 → 05:19)

**SRT lines 154–163:**
> *"He is hoisted to the ceiling by ropes tied to his twisted arms, then dropped 12 times. Ropes are wrapped around his calves, ties and shins, and tightened. Twelve times. Seven jars of water are forced down his throat. He screamed that they were killing him, but he revealed nothing."*

**Verdict:** KEEP. This is the scene; let it land.

**Issues:**

| # | Timestamp | Issue | Fix |
|---|---|---|---|
| 17 | 05:09 (line 158) | "calves, ties and shins" — script said "calves, thighs, and shins." "Ties" is a verbal slip OR transcription error for "thighs." | Verify on tape. If verbal slip: caption-fix to "thighs" (anatomically correct, defensible). If you said "ties" cleanly: leave but caption-fix anyway. **Recommend caption-fix.** |

**B-roll for segment:**

- **05:00 → 05:06** — **Shot 14 zoom into the session entry** (the disrobing/cord/pulley lines). If you have nanobana-rendered details of the rack/strappado action, lay over briefly. Otherwise hold on the document with slow push.
- **05:06 → 05:12** — Cut to **Shot 5b (Garrucha card)** OR **Shot 5d (Potro card)** quickly, named with Spanish + English. Per `NANOBANA-PROMPTS.md` method illustrations (check Wikimedia Commons period engravings before nanobana generation).
- **05:12 → 05:19** — Cut to **Shot 5c (Toca / waterboarding)** on *"Seven jars of water."* Hold through *"He screamed... revealed nothing."*

**Music:** Bed dims at 05:00. **Hard cut to silence at 05:14** ("He screamed that they were killing him") — silence carries the line. Hold silence through 05:19.

---

## Segment 15 — Silence = innocence + reconciliation (05:20 → 05:43)

**SRT lines 164–176:**
> *"Under Inquisition law, the same law that authorized the session, silence counts as innocence. The Inquisition took it as proof he had nothing to confess. He was reconciled to the church and cleared. Unbeknownst to him, the friends and family he'd refused to name had been burned the same month he was arrested. He'd been protecting people who were already gone."*

**vs script said:**
> Script had: *"Unbeknownst to him — Hassner's words — the friends and family..."* — DROPPED *"Hassner's words"* attribution.
>
> Postmortem confirms: gut-punch lands harder bare. **Verdict: KEEP your version.** Bare attribution-free reveal is stronger.

**Issues:**

| # | Timestamp | Issue | Fix |
|---|---|---|---|
| — | — | Clean delivery; emotional close lands | — |

**B-roll for segment:**

- **05:20 → 05:30** — **Shot 14 hold** OR talking head with desaturated talking-head treatment. The "silence = innocence" beat is verbal-driven.
- **05:30 → 05:43** — **Talking head** for the closing reveal. Don't cover the face here — the line *"He'd been protecting people who were already gone"* is yours to deliver to camera. Tier-B fallback if you want a visual: Goya's *Auto-da-fé* (c. 1812-1819, Wikimedia Commons) — small inset upper-right showing penitents in sanbenitos as you say *"burned the same month he was arrested."*

**Music:** Silence holds from §14. Bed re-enters quietly at 05:35 (after "people who were already gone"). Let the line sit in silence for ~1.5 seconds before music returns.

---

## Segment 16 — 3,000 executions + Kamen quote (05:44 → 06:13)

**SRT lines 177–190:**
> *"His friends and family weren't the only ones. The figure most cited about the Inquisition was around 3,000 executions over 350 years. That's Henry Kammen's estimate. It's probably close. Kammen also wrote this. 'The apparently low overall death rate masks a very high rate in the first half century of the Inquisition, and a consistently high rate affecting people of Jewish and Muslim origin.'"*

**Verdict:** KEEP.

**Issues:**

| # | Timestamp | Issue | Fix |
|---|---|---|---|
| 18 | 05:53 (line 182) | "Henry Kammen" → "Henry Kamen" | `/fix` (recurs line 184) |

**B-roll for segment:**

- **05:44 → 05:53** — **Talking head** transition on *"His friends and family weren't the only ones"* (1-2 seconds), then cut to **Shot 15 (Kamen p.254 quote card setup)** — show the page reference / book cover briefly before the quote.
- **05:53 → 05:58** — Hold on book cover OR cut to talking head: *"That's Henry Kamen's estimate. It's probably close."*
- **05:58 → 06:13** — **Shot 15 (Kamen quote card, full)** with the verbatim text *"The apparently low overall death rate masks a very high rate..."* Per `NANOBANA-PROMPTS.md` quote card spec. Citation: "Kamen, *The Spanish Inquisition: A Historical Revision*, Yale UP, p. 254."

**Music:** Bed continues quiet. No swell — the dramatic peak was §4 + §5.

---

## Segment 17 — Targeting machine / conversos (06:13 → 06:37)

**SRT lines 191–201:**
> *"In other words, the Inquisition wasn't operating against the whole population. It was a targeting machine aimed almost entirely at conversos. Descendants of Jews and Muslims forced to convert to Christianity. The 3,000 executions weren't spread evenly. They concentrated on the people, the Spanish state, never quite trusted to be Christian."*

**Verdict:** KEEP.

**Issues:**

| # | Timestamp | Issue | Fix |
|---|---|---|---|
| 19 | 06:30 (line 200) | "the people, the Spanish state, never" — punctuation ambiguity reads oddly in caption. Script: "the people the Spanish state never quite trusted." Decide: caption-rewrite without commas, or add em-dashes. | Caption fix |

**B-roll for segment:**

- **06:13 → 06:22** — **Estatutos de Limpieza de Sangre** manuscript (16th century). Gallica.bnf.fr: search "Limpieza de Sangre manuscript." Visual: family-tree-style genealogical chart with legal decree typography. Highlight/call-out the words *"Limpieza de Sangre"* on screen so the viewer reads the document's purpose.
- **06:22 → 06:30** — **Sanbenitos engraving** — the yellow penitential garments hung in churches. Wikimedia Commons: search "Sanbenitos hanging" — look for 1759 *Mémoires* of the Inquisition plates. Caption: "Sanbenitos hung in churches — generational mark of converso families."
- **06:30 → 06:37** — Cut to **map of Iberian conversos** OR period engraving of the 1492 Edict of Expulsion. Wikimedia Commons: search "Edicto de Granada 1492" or "Alhambra Decree." Caption: "1492 — forced conversion or expulsion."

**Music:** Bed continues. Slight chord shift at 06:13 — signal we're in the social-consequences territory now.

---

## Segment 18 — Converso writer in Toledo + 🚨 audio fix (06:37 → 06:57)

**SRT lines 202–215:**
> *"Most people remember the executions and the torture. They rarely think about what it meant to live under the Inquisition. This is what a converso writer in Toledo writes in 1538: 'Bit by bit, many rich people leave the country for foreign realms in order not to live all their lives in fear and trembling every time an officer of the Inquisition enters their house. For continual fear is a worse **enemy** than a sudden demise.'"*

**vs script said:**
> Script: *"For continual fear is a worse **death** than a sudden demise."* — Kamen p.232 verbatim is "death."
>
> 🚨 **CRITICAL audio mismatch.** Tape says "enemy"; correct word is "death." See post-mortem.

**Issues:**

| # | Timestamp | Issue | Fix |
|---|---|---|---|
| 20 | 06:54 (line 215) | 🚨 **"worse enemy" → "worse death"** | **RE-RECORD this line.** Single-line pickup, ~5 seconds. The Shot 16 visual will display the verbatim Kamen quote with "death" — audio/visual mismatch on a "show-you-the-sources" channel is a self-inflicted credibility hit. **HIGH priority.** |

**B-roll for segment:**

- **06:37 → 06:42** — **Talking head** transition on *"Most people remember executions and torture..."* OR Shot 15 callback (Kamen book cover) briefly.
- **06:42 → 06:57** — **Shot 16 (converso Toledo writer quote card).** Per `NANOBANA-PROMPTS.md` quote card spec. Full verbatim Kamen quote. **Citation tag includes AHN reference:** "Kamen, p. 232 (orig. AHN Inquisición, Leg. 1867, No. 36 — Sebastián de Horozco attributed)." Sub-attribution gives the primary archival anchor without claiming we've shown the AHN scan.

**Music:** Bed dims for the converso quote read. Silence on the closing line *"a worse [death] than a sudden demise"* — dramatic beat.

**Asset note:** Shot 16 quote card MUST display "death" (per Kamen verbatim). Once the §6 line is re-recorded, audio and visual align.

---

## Segment 19 — System produced + closing thesis (06:57 → 07:12)

**SRT lines 216–222:**
> *"This is what the system produced. Not just 3,000 executions, but generational fear. The rules weren't there to protect the accused. They were there to make the Inquisition run efficiently and harder to escape."*

**Verdict:** KEEP. Closing thesis statement.

**Issues:**

| # | Timestamp | Issue | Fix |
|---|---|---|---|
| — | — | Clean | — |

**B-roll for segment:**

- **06:57 → 07:05** — **Rizi, *Auto-da-fé in the Plaza Mayor of Madrid* (1683).** Prado Museum / Wikimedia Commons: search "Francisco Rizi Auto de Fe." **Crop into the audience faces** — the watching crowd is the "social atmosphere of denunciation." Avoid showing the executions themselves; we want the system's ambient weight.
- **07:05 → 07:12** — Cut to **Goya, *The Inquisition Tribunal* (c. 1812-1819).** Wikimedia Commons: search "Goya Inquisition Scene." Captures the psychological weight better than any contemporary work. Caption: "Goya, c. 1812 — painted at the Inquisition's end, capturing the system's psychological residue."

**Music:** Bed re-enters at 06:57 with a low minor pad — signals the closing thesis. Continues through end of §7.

---

## Segment 20 — §7 close: callback to f.6v + climax (07:13 → 07:32)

**SRT lines 223–235:**
> *"Tarkmada didn't invent cruelty. He organized it. He wrote rules that required a doctor in the room while we were being waterboarded. He wrote rules that made your confession invalid unless you repeated it freely the next morning. He wrote rules that said you couldn't be tortured twice for the same evidence. And in the same paragraph, he wrote the clause that made all of it negotiable."*

**vs script said:**
> Script: "you were being waterboarded" (you, not we). Tape says "we." Minor verbal stumble. **Caption-fix to "you"** — the script's second-person was deliberate (it places the listener in the chamber). "We" is a slip.

**Issues:**

| # | Timestamp | Issue | Fix |
|---|---|---|---|
| 21 | 07:13 (line 223) | "Tarkmada" → "Torquemada" | `/fix` |
| 22 | 07:16 (line 226) | "we were being waterboarded" → script said "you were being waterboarded" | Caption-fix to "you" (second-person was deliberate). Audio is close enough to leave; caption-only fix. |

**B-roll for segment (THE CLIMAX RETURN):**

- **07:13 → 07:18** — **Shot 2 RETURN (f.6v full page).** No highlights yet. The page itself is the visual fact reasserted. This callback is the §7 architecture — the same page from §1 reappears as the closer.
- **07:18 → 07:23** — **Highlight 2 (ratification clause)** appears on *"made your confession invalid unless you repeated it freely the next morning."* Yellow #FFE066 on *"el dia siguiente, ó a tercero dia ratificare."*
- **07:23 → 07:28** — **Highlight 3 (loophole)** appears on *"said you couldn't be tortured twice for the same evidence."* Now Highlights 2 + 3 both visible.
- **07:28 → 07:32** — **All 3 highlights visible simultaneously** on *"And in the same paragraph, he wrote the clause that made all of it negotiable."* Slow push in to ~115% scale. **THIS IS THE CLIMAX VISUAL.** The page that's been the spine of the video now shows all three discoveries at once.

**Music:** Bed swells slightly on each highlight reveal. Peaks at 07:28 with all three visible. Holds.

---

## Segment 21 — Final beat + CTA (07:33 → 07:48)

**SRT lines 236–244:**
> *"The people defending the Inquisition cite those protections. The critics cite the same document. They're both kind of right. They just don't read paragraph 15 all the way through. Subscribe. I try not to just tell a story, but I also try to show you the sources."*

**vs script said:**
> Script: *"They're both right."* Tape: *"They're both kind of right."* Postmortem confirms: hedged false symmetry, intentional. **KEEP.**
>
> Script CTA: *"Subscribe — I don't just tell the story, I show you the sources."* Tape: softened to *"I try not to just tell a story, but I also try to show you the sources."* Postmortem confirms: voice softened, intentional. **KEEP.**

**Issues:**

| # | Timestamp | Issue | Fix |
|---|---|---|---|
| — | — | Clean | — |

**B-roll for segment:**

- **07:33 → 07:43** — **Shot 2 slow hold-out** with all 3 highlights still visible. Slow zoom out to wide, page recedes. *"They just don't read paragraph 15 all the way through"* — the page itself is the proof.
- **07:43 → 07:48** — **Talking head + end card** for subscribe + CTA. Channel branding lower-third. End card with 2 video thumbnails appears at 07:46.

**Music:** Bed resolves with a soft chord at 07:43. End card music transition standard.

---

## Pacing assessment

| Marker | Script target | Rough cut actual | Delta |
|---|---|---|---|
| End of hook (§1) | ~0:35 | ~0:43 | +0:08 (slightly long, acceptable) |
| Marina González named (§2 close) | ~1:30 | ~1:46 | +0:16 |
| Loophole reveal (§4 climax) | ~2:35 | ~3:20 | +0:45 |
| Díaz de Cáceres setup (§5 open) | ~3:10 | ~4:10 | +1:00 |
| §6 Kamen verbatim | ~4:00 | ~5:58 | +1:58 |
| End of video | ~5:00 | ~7:48 | **+2:48 (+56%)** |

**Verdict:** Format C delivers slower than standard talking-head. Per script-writer-v2 v15.0 Rule 10 (Format-Specific WPM Calibration): document-heavy formats run ~150 WPM × 2.5 multiplier, NOT the 250 WPM × 1.20x assumed in pre-v15 drafts. **Acceptable for vibes-test purposes — postmortem reframes this as an 8-minute Format C close-read test, NOT a 5-minute compression test.**

**Don't tighten.** Trimming would mean cutting either:
- §5 (Díaz de Cáceres) — the emotional anchor of the entire video
- §3 procedural rules — the spine of the thesis

Both are load-bearing. Ship at 7:48.

---

## Caption pass — burned-in subtitles

**Recommendation:** **Run `/fix` before final caption burn-in.** 22+ proper-noun / foreign-term / minor-stumble caption issues detected. `/fix` handles the SRT script-cross-reference and timestamp offset (SRT starts at 01:00:00, needs to be 00:00:00 in DR) in one pass.

**Quick reference of issues found (full list embedded above per segment):**

- Hassner ×4 instances → SRT renders "Hessner" / "Hesner" / "Hasner"
- Torquemada ×2 → SRT renders "Torqumeda" / "Tarkmada"
- Compilación de las Instrucciones → "Compilation de las Insuciones"
- Instrucciones (line 68) → "Intrixiones"
- Marina González → "Marina Gonzalez" (no accent)
- Antonio Díaz de Cáceres → "Diaz de Caceres" (no accents)
- Ciudad Real → "Ciudadreale"
- Henry Kamen ×2 → "Kammen" (extra m)
- "prominent injury" (line 84) → script: "permanent injury" — verbal slip OR transcription error; caption-fix to "permanent"
- "calves, ties and shins" (line 158) → script: "calves, thighs, and shins" — caption-fix to "thighs"
- "we were being waterboarded" (line 226) → script: "you were being waterboarded" — caption-fix to "you" (deliberate second-person)
- Timestamp 1-hour offset → all SRT codes are `01:XX:XX,XXX`; DR needs `00:XX:XX,XXX`

**Do NOT manually correct in this guide — `/fix` handles it programmatically and writes a clean SRT. After running `/fix`, the resulting `fixed subs.srt` is what you burn in.**

---

## Re-record / pickup checklist

Ranked by impact:

### HIGH priority

1. **§6 line at 06:54 — "worse enemy" → "worse death"**
   - Single-line pickup, ~5 seconds. Drop in over Shot 16.
   - **Why HIGH:** Audio/visual mismatch on a "show-you-the-sources" channel where the on-screen quote card displays "death" (Kamen p.232 verbatim). Self-inflicted credibility hit if shipped uncorrected.
   - **Cost:** 5 minutes in the booth + 30 seconds in DR.

### LOW priority

2. **§3 line at 02:44 — "prominent injury" → "permanent injury"**
   - Verbal slip OR transcription artifact. Verify on tape.
   - **Why LOW:** Caption-fix only suffices. Audio is close enough that no listener catches it. Don't bother re-recording unless you're already in the booth for #1.

3. **§7 line at 07:16 — "we were being waterboarded" → "you were being waterboarded"**
   - Verbal stumble. The second-person was deliberate (places the listener in the chamber).
   - **Why LOW:** Caption-fix to "you" is enough. Audio "we" is technically wrong but doesn't break the close.

### OPTIONAL

4. **§5 line at 05:09 — "ties and shins" → "thighs and shins"**
   - Probably a transcription artifact (you likely said "thighs"). Verify on tape.
   - **If verbal:** caption-fix only. Skip pickup.

### Don't re-record

- The §1 cuts ("and they wrote it down" dropped) — better than script.
- The §4 patch ("This phrase is cited by historians... why else would you use the word repeat as an exception?") — the strongest improvisation in the rough cut.
- The §5 dropped attribution ("Hassner's words") — gut-punch lands harder bare.
- The §7 hedges ("both kind of right" / "I try not to just tell") — intentional voice softening, postmortem-confirmed one-off mood. Calm Prosecutor voice stays as-is across other videos.

---

## Music & silence beats

| Time | Beat | Recommendation |
|---|---|---|
| 0:00 → 0:11 | §1 Black Legend setup | Single low pad. No melody. |
| 0:11 → 0:19 | Turn | Pad continues. No swell. |
| 0:19 → 0:37 | Compilación reveal | Pad swells slightly on cut to Shot 1. Holds under Shot 1. |
| 0:37 → 0:43 | "Paragraph 15" reveal | **Drop to silence** on cut to Shot 2. Silence on "Paragraph 15." |
| 0:43 → 1:05 | §2 intro | Light bed re-enters quietly. |
| 1:05 → 1:18 | Hassner cold blood quote | Bed dims. Quote card lands quiet. |
| 1:18 → 1:32 | CIA contrast | **Silence under SSCI cut** for ~2s. Bed re-enters as redactions scroll. |
| 1:32 → 1:46 | Marina González bridge | Bed re-enters fully. |
| 1:47 → 2:06 | §3 scene | Bed quiets. Scribe's words land in near-silence. |
| 2:07 → 2:44 | Procedural rules dump | Bed continues low. Don't break — rapid-fire is its own rhythm. |
| 2:44 → 2:50 | Anticipation before §XV verbatim | Hold bed. |
| 2:50 → 2:59 | §XV verbatim quote | **Drop bed.** Silence under verbatim. |
| 2:59 → 3:11 | Decoder ("In other words...") | Bed re-enters quietly. |
| 3:17 → 3:20 | "Now read the last line" | **Hard silence.** ~3s in silence — anticipation. |
| 3:20 → 3:28 | 🎯 Loophole reveal | Hard silence under reveal. Bed re-enters at 3:28 with low minor pad. |
| 3:28 → 4:05 | §4 close + Hassner card | Bed continues quiet. No swell. |
| 4:06 → 4:18 | Atlantic transition | New bed (different texture — signals continent change). |
| 4:18 → 4:55 | Díaz backstory | Bed quiet. **Silence at 4:55** ("Four years passed"). |
| 4:55 → 5:00 | Bringing him back | Silence holds. |
| 5:00 → 5:14 | Torture session description | Bed quiet. |
| 5:14 → 5:19 | "He screamed... revealed nothing" | **Hard cut to silence.** Hold through 5:19. |
| 5:20 → 5:35 | Silence = innocence | Silence holds. |
| 5:35 → 5:43 | "People who were already gone" | Bed re-enters at 5:35. Let line sit ~1.5s in silence first. |
| 5:44 → 6:13 | Kamen quote | Bed continues quiet. No swell. |
| 6:13 → 6:37 | Targeting machine / conversos | Slight chord shift at 6:13 — social-consequences territory. |
| 6:37 → 6:57 | Converso writer quote | Bed dims for verbatim read. **Silence on the closing line** ("worse [death] than a sudden demise"). |
| 6:57 → 7:12 | Closing thesis | Bed re-enters with low minor pad at 6:57. |
| 7:13 → 7:28 | §7 climax build | Bed swells slightly on each highlight reveal. |
| 7:28 → 7:32 | All 3 highlights visible | Peaks. Holds. |
| 7:33 → 7:43 | Final beat | Bed resolves. |
| 7:43 → 7:48 | Subscribe + end card | End card music transition standard. |

---

## Done state

When this video is locked, you should have:

- [ ] §6 line re-recorded ("worse death" replacing "worse enemy") and dropped into Shot 16
- [ ] `/fix` run, producing `fixed subs.srt` with all 22+ caption issues + 1-hour timestamp offset corrected
- [ ] Compilación PDF screenshots taken for: title page (Shot 1), f.6v (Shot 2 — appears 4×, ONE screenshot reused with 3 highlight layers), f.33r (Shot 3a), f.34 Instr.55 (Shot 3b), f.29r (Shot 4)
- [ ] Nanobana overlays generated for all Compilación shots per `NANOBANA-PROMPTS.md` Category A
- [ ] Shot 13 (Marina González record) full nanobana generation complete using Trial 100 Spanish + procedural transcript citation
- [ ] Shot 14 (Díaz de Cáceres record) full nanobana generation complete with AGN citation tag
- [ ] Quote cards designed for Shots 3c, 5a, 9, 11, 15, 16 per `NANOBANA-PROMPTS.md` Category C — Shot 16 displays "death" verbatim
- [ ] B-roll fetched for talking-head segments: de Bry engravings, Berruguete, Trasmonte 1628 Mexico City, Limpieza de Sangre manuscript, Sanbenitos engraving, Rizi Auto-da-fé, Goya Inquisition Tribunal
- [ ] Music beds laid per the table above; silence beats protected at 0:37, 1:25, 2:50, 3:17, 5:14, 5:35, 6:54
- [ ] §7 climax: f.6v with all 3 highlights visible simultaneously at 7:28-7:32, slow push to 115% scale
- [ ] End card with 2 video thumbnails at 7:46
- [ ] Caption burn-in uses `fixed subs.srt` (NOT raw `rough cut.srt`)
- [ ] Final QC pass: confirm "death" displays on Shot 16 visual AND audio says "death" after pickup re-record

---

## Cross-references

- `01-VERIFIED-RESEARCH.md` — source verifications, especially Claim 2.4c (doctor not in primary text)
- `02-SCRIPT-DRAFT.md` — script ground truth for all diffs
- `03-FACT-CHECK-VERIFICATION.md` — verification gates
- `04-ROUGH-CUT-POSTMORTEM.md` — action items, v15.0 lessons captured
- `B-ROLL-FACSIMILE-SHOT-LIST.md` — 17 planned shots with folio references
- `NANOBANA-PROMPTS.md` — visual language rules, asset generation specs
- `_gemini-output/editing-guide-broll-2026-05-11.md` — full Gemini Flash B-roll research output (this guide pulls Tier A suggestions from there)
