# HANDOFF — Bandera video + workflow change
_Session date: 11 July 2026. Paste into Claude Code as context._

---

## PART 1 — WORKFLOW CHANGE (applies to all future videos)

**Problem identified:** Research briefs don't convert into scripts. Two separate causes, previously conflated:

1. **Wrong organising axis.** Research is organised by knowledge (topic → source → finding). A script is organised by time (what the viewer believes at minute 3, and what breaks it at minute 4). A "brief" that's still a knowledge document just adds a step.

2. **Scripts don't sound like Benoit.** Voice profiles built from *written* scripts teach written voice. Benoit has to *say* the words — his mouth catches what his eye would forgive. LLM voice-matching plateaus at ~80% and the missing 20% is exactly the part that gets noticed.

**Fixes adopted:**

### A. Belief-state beat sheet replaces the research brief
Every beat has four fields, nothing else:
- **Viewer currently believes:** …
- **What breaks it:** the evidence, with document + page
- **Viewer now believes:** …
- **Question this opens:** ← hook into the next beat

Filter rule: if a beat can't fill "question this opens," it doesn't earn its place. Cut it. This is a retention filter that runs *before* any prose is written.

### B. Record-then-cut replaces script-writing
1. Benoit records himself talking through a beat, out loud, messy, one take.
2. Transcribe.
3. Claude does **subtractive editing only** — tighten, cut repetition, reorder, flag where evidence lands. **Never writes a new sentence.**
4. Every word in the final script is one he actually said, so it cannot sound un-like him.

**Standing rule (unchanged, now reinforced): Claude does not generate script prose. Ever.**

### C. Voice profile = diagnostic, not generator
Build from *published video transcripts*, not written scripts. Measure: sentence-length distribution, real transition words, how he cites a source aloud, what he never says. Use it as a checklist to catch AI-tells — not as a style prompt.

---

## PART 2 — TOPIC DECISION

### What was rejected and why
**Volhynia massacre — the lane closed.** The demand signal (Polish HBC video comments asking for English subs) was from July 2025. Supply filled in since: World History (Aug 2025), Rethinking WWII (Oct 2025), The Black Box (Nov 2025), History Without Chains (May 2026), a channel literally named "Volhynia Massacre" (July 2026), OllieKayPolitical (11 July 2026). Mostly AI slop, but it occupies the search page. vidIQ outlier scan found **zero** Volhynia history breakouts in the past year.

### Keyword data (vidIQ, US-enriched)
| keyword | volume | competition | est. monthly |
|---|---|---|---|
| volhynia massacre | 53 | 26 | 3,300 |
| ukrainian insurgent army | 55 | 34 | 4,700 |
| stepan bandera | 55 | 45 | 5,100 |
| bandera | 64 | 59 | 19,650 |
| **execution of stepan bandera** | **53** | **15** | **3,300** |
| "was bandera a nazi" | 0 | — | 0 |

Two takeaways:
- "execution of stepan bandera" is the lowest-competition entry on the board.
- **Question-phrased keywords have zero YouTube volume.** Curiosity framing must be a *noun phrase*, not a question. (Refines the existing rule.)

### CHOSEN VIDEO
**"Bandera — The Man Both Sides Invented"**

**Thesis:** Bandera wasn't Hitler's puppet — he was a fascist in his own right. That's worse for *both* narratives, and nobody on English YouTube is telling it.

**The trap to avoid:** this video can accidentally become a Bandera hagiography. "The Nazis imprisoned him" is true but lethal if left there — he was a *Sonderhäftling* in the Zellenbau with privileges, not a man in a death camp.

---

## PART 3 — BEAT SHEET (v1, pre-Lebed rebuild)

1. **Believes:** Bandera is the Ukrainian Nazi Putin invokes. → **Breaks:** 15 Oct 1959, the KGB murdered him in Munich with a cyanide spray gun. → **Now:** Moscow killed him. → **Opens:** why kill a Nazi 14 years after the war?

2. **Believes:** he must've been a serious Nazi then. → **Breaks:** the Germans held him at Sachsenhausen. → **Now:** the Nazis locked him up. → **Opens:** so was he a victim?

3. **Believes:** he was a victim. → **Breaks:** ⚠️ KILL THIS IMMEDIATELY. Zellenbau, special-prisoner wing, bedroom/living room/kitchen, communicated with the OUN via his wife. Not martyrdom — storage. → **Now:** I'm being told the uncomfortable version. → **Opens:** then what WAS he?

4. **Believes:** something in between. → **Breaks:** the May 1941 OUN-B militia instructions — written *before* Barbarossa. Lviv pogroms, June–July 1941, by OUN militias in his name while he was still at liberty. → **Now:** a fascist on his own account, not Hitler's servant. → **Opens:** what about Volhynia?

5. **Believes:** Bandera ordered Volhynia. → **Breaks:** he was in German custody throughout. Orders ran through Shukhevych and Klym Savur. → **Now:** he didn't order it. → **Opens:** then why is his name on it?

6. **Believes:** he's been unfairly blamed. → **Breaks:** the perpetrators called themselves *banderivtsi*. He never repudiated it after release. You don't have to sign the order to own the name. → **Now:** the guilt is real but not the guilt he's charged with. → **Opens:** who benefits from getting this wrong?

7. **Believes:** it's just sloppy history. → **Breaks:** Karlsruhe, 1962. Stashynsky confesses; the court rules the **Soviet state** was the principal. → **Now:** a court formally named Moscow the murderer. → **Opens:** so why does Moscow keep saying his name?

8. **Believes:** Russia hates Bandera. → **Breaks:** Moscow built the bogeyman it now invokes. Kyiv made him a hero *in reaction* (Zelensky's May 2026 "Heroes of the UPA" decree). → **Now:** both sides need the myth. → **Opens:** what does the real man look like?

9. **Close:** neither Nazi nor hero. A fascist the Nazis jailed and the Soviets murdered, whose name both still need. **The documents refuse to serve anybody.**

**Beats 3 and 6 are load-bearing. Do not cut for pace.** They're what makes the video unbrigadable — concede the strongest point against you before anyone can throw it.

### ⚠️ PENDING REBUILD: beats 7–8 around Lebed (see Part 4)

---

## PART 4 — THE MOAT: CIA DECLASSIFIED FILES

**This is the differentiator.** Free, English, public — `cia.gov/readingroom`. File series `BANDERA, STEFAN_0001`–`_0085`+, plus Project **AERODYNAMIC** files released under the Nazi War Crimes Disclosure Act.

Nobody uses them because they're miserable OCR'd scans and it's a week of eye strain. **That's a labour moat, not a language moat** — the slop channels physically cannot do it.

### Find #1 — Bandera denying he's a fascist, in his own voice
His **December 1954 Cologne radio interview**, preserved in CIA archives: Ukrainian nationalism "has nothing in common with Nazism, fascism or national-socialism"; it fights "totalitarianism, racism, dictatorship and violence of any kind."

**Production note:** put that on screen beside the May 1941 militia instructions. Same organisation, same man, thirteen years apart. Don't call him a liar — show both documents and stop talking.

### Find #2 — The CIA didn't back Bandera. It backed the man who ordered Volhynia.
Everyone says "CIA-backed Nazi Bandera." The files say the opposite. Through AERODYNAMIC the Agency funded **Mykola Lebed** and his Prolog operation in New York — Bandera's *rival*. Lebed ran OUN-B in western Ukraine while Bandera sat in Sachsenhausen, and in **April 1943 proposed to "cleanse the entire revolutionary territory of the Polish population."** The CIA shielded him from war-crimes prosecution into the 1990s.

**America protected the architect of Volhynia. It wasn't Bandera. It was the man Bandera's name is used to hide.**

This is a document-driven argument nobody has made. It only works for a primary-source channel, because the claim is unbelievable until you show the paper.

### 🚨 HARD RULE FOR CIA FILES
**A document *in* a CIA file is not a CIA *claim*.** Those folders contain collected Soviet disinformation — e.g. `BANDERA, STEFAN_0018` reads as Soviet propaganda calling Bandera the Gestapo's puppet. Citing it as "the CIA said" would be a self-inflicted kill shot.

For every CIA document used on camera, state: **who wrote it, for whom, and how it got into the folder.** Say it out loud in the video. It's the most credible thing available and the slop channels never do it.

---

## PART 5 — SOURCES

### Tier 1 — primary
- **BGH Karlsruhe, verdict 19 Oct 1962, case 9 StE 4/62** (BGHSt 18, 87). German. Stashynsky convicted as *Gehilfe*; court named Shelepin/Khrushchev as principals. ⚠️ Presiding judge Heinrich Jagusch was a former NSDAP member who compared Stashynsky to Eichmann. **Address this out loud — do not hide it.**
- **Bandera's Sachsenhausen prisoner card, no. 72192.** Assigned Oct 1943; release 28 Sept 1944. Chase a scan from Stiftung Brandenburgische Gedenkstätten / Sachsenhausen Memorial. **This is the on-camera artifact.**
- **OUN-B militia instructions, May 1941** — permits liquidation of "undesirable Polish, Muscovite and Jewish activists"; "minorities policy" section marks Muscovites/Poles/Jews for destruction. **Predates Barbarossa.** Reproduced in Himka (English); original in *ОУН в 1941 році: документи*.
- **Act of Restoration of Ukrainian Statehood, 30 June 1941.** Pledges close work with National-Socialist Greater Germany "under the leadership of its leader Adolf Hitler." ⚠️ But the Germans did NOT approve it — it blindsided them.
- **Einsatzgruppen *Ereignismeldung*, 16 July 1941** — records the OUN-B slogan.
- ⭐ **EHRI online course, `training.ehri-project.eu/pogroms-1941/`** — primary docs with English translations. A01 (Stetsko on Jews, pre-war), A04 (OUN-B pogrom incitement poster), A07 (Stetsko backing German "methods of exterminating Jewry", July 1941). **Free, English — likely removes the need for a Ukrainian reader.**
- **Three conflicting accounts of when Bandera reached Zellenbau:** Stetsko (1967) says Jan 1942; Bandera's 1950 interview says Berlin until 1943; his 1956 Munich interrogation says winter 1942–43. His own story doesn't line up.

### Tier 2 — scholarship (English, no reader needed)
- Rossoliński-Liebe, *Stepan Bandera: The Life and Afterlife of a Ukrainian Nationalist* (2014) — definitive. Documents the Zellenbau privileges.
- Himka, "The Lviv Pogrom of 1941," *Canadian Slavonic Papers* 53 (2011).
- Plokhy, *The Man with the Poison Gun* (2016) — Stashynsky narrative.
- Motyka (Polish) — Volhynia command chain.

### The opposition — read or get ambushed
- Marples, Cârstocea, Veselý all attack Rossoliński-Liebe's fascism framing (definition too wide / book intentionally hostile).
- Snyder: similar violence occurred where the OUN had no presence.
- Kopstein/Motyl/Kiebuzinski: multiple contributory factors — NKVD prison massacres, pre-existing antisemitism among Poles *and* Ukrainians, petty criminals on the ground.
- OUN-B's Second Congress (Kraków, April 1941) formally *discouraged* pogroms. The local instructions cut the other way. **Both are true.**

### Numbers — lock before recording
- Poles killed, Volhynia + E. Galicia: **70,000–100,000**
- Ukrainians killed in reprisals: **10,000–20,000**
- Jews killed in the Volhynia/Galicia massacres: **1,000–2,000** (highly uncertain)
- Lviv pogrom Jewish deaths: **4,000 (Pohl) / 5,000 (Breitman) / 6,000 (Longerich)** — give the range, name them
- OUN-B arrested by Gestapo by Dec 1941: **~1,500**; sent to Auschwitz **~200**, of whom **~30 died, including both of Bandera's brothers**

---

## PART 6 — FACTUAL TRAPS

1. **Bandera was NOT in a camp for the whole war.** Exact sequence: 5 July 1941 *custodia honesta* in Kraków → Berlin → released 14 July, confined to the city → Spandau from 15 Sept 1941 → Sachsenhausen from Jan 1942 → released 28 Sept 1944. **He was at liberty during the Lviv pogrom of 1 July.** Arrest came four days later. Get this exactly right or the video collapses.
2. **Fridental Castle.** The Germans let the Zellenbau Ukrainians out to meet OUN representatives 200m from the camp. Destroys "he was locked up, he couldn't have known."
3. **Both his brothers died at Auschwitz.** Do not skip. It earns the right to call him a fascist thirty seconds later.
4. **He never repudiated Volhynia after release.**

---

## PART 7 — OPEN ITEMS

- [ ] **Rebuild beats 7–8 around Lebed / AERODYNAMIC.** (Agreed, not yet done.)
- [ ] **Readers hired:** German + Polish, budget approved.
  - *German brief:* BGH 9 StE 4/62 — verbatim reasoning on the *Gehilfe* finding + Stashynsky's courtroom account of weapon and order chain. Request scan of prisoner card 72192 from Sachsenhausen Memorial. *Ereignismeldung* of 16 July 1941.
  - *Polish brief:* Motyka on the Volhynia command chain — what the record shows and does NOT show about Bandera. Must support "no signed order, and he was in a cell" without overclaiming.
  - *Ukrainian:* check EHRI first — probably unnecessary.
- [ ] **Grind the CIA reading room.** `BANDERA, STEFAN_*` + AERODYNAMIC vols. Log provenance for every document.
- [ ] **Notebook check blocked** — Drive access was declined this session. Re-approve and cross-check the bundle against what's already loaded, so nothing is researched twice.
- [ ] **Thumbnail + title:** lead on the *execution* angle (competition 15). Noun phrase, not a question.
- [ ] **Record beat 1** out loud, one take, messy. Then subtractive edit only.
