# PHRASING-AUDIT-2026-07-21.md — whole-script syntax, diction, clause and paragraph audit

> **Target:** `SCRIPT.md` v7.0 (2,760 words of VO by my extraction; the header says 2,843/2,816 — see § Honest limits).
> **Brief, in his words:** *"its about the whole script how to phrase things. not only numbers and shit like everything. i feel like theres still some ai speak in the logic and phrasing and words used and the way the script is structured with phrases and stuff."*
>
> **Scope split — read alongside, do not merge:**
> - `REFERENCE-LANE-FIGURATION-2026-07-21.md` owns **figuration** (metaphor, colour, antithesis density). This file owns **syntax, diction, clause order, connective joints, paragraph shape.** No overlap; where I touch a line that file also touched, I say so.
> - `BLIND-EVIDENCE-DESIGN-2026-07-21.md` owns **evidence architecture.** Structure is settled. Nothing below reopens beat order.
> - `VOICE-PROFILE.md` § "Adversarial drift audit (Fable Phase 2)" owns **T1–T8 rhetorical tells.** I report *violations* of those existing caps (T5, T7, T8 all fire here) but claim no credit for discovering them. Everything in § 5 is a tell **not** in T1–T8.
>
> **Epistemic tags:** MEASURED = counted from a named corpus, script reproducible. INFERRED = my reading. IDEA = lane-derived, non-binding per house rule. His gold fingerprint and his live read-aloud picks are ground truth and beat both.

---

## 0. IF YOU ONLY DO FIVE THINGS

Ranked by severity across the whole script. All five are cheap; three of them **save words**.

**1. Let "so" and "but" do the work the em-dash is currently doing.** MEASURED. Your unscripted gold runs `so` at **11.8 per 1,000 words** and `but` at **9.2** — 21.0 combined. This script runs 3.3 and 4.4 — **7.6 combined, 36% of your natural rate.** Meanwhile the em-dash runs at **24.6 per 1,000**. The em-dash isn't decorating; it has *replaced your causal spine*. Roughly 15 of them sit between two complete clauses where your mouth would put a word. VOICE-PROFILE protects the em-dash as a **within-sentence pivot into a verdict** (✅ canon) — that use stays. The one to kill is em-dash-as-conjunction. Cost: 0 to +1 word each.

**2. Six sentences you cannot say in one breath.** MEASURED. 54w (CH1), 56w (CH5), 46w (CH2), 46w (CH10), 42w (CH4), 40w (CH8) — none of them quote-carried. Another ~14 sit in the 30–39w band. Your gold's true ceiling is **~30 words**; every "sentence" above 40 in the gold transcript is an ASR punctuation gap, not something you said. The fix is the canon one from the Natural→Scripted table — **two medium sentences, never a staccato stab.** Splitting these costs +1 to +7 words total and buys back every one of them in delivery.

**3. Colon-reveals: 17 in the script against an existing cap of ~2.** MEASURED, **existing rule — Fable T8**, not a new find. 14 are true withhold-then-reveals; 3 are legitimate quote hand-offs (exempt). Rate: **6.2/1k vs gold 0.0 and lane maximum 0.7/1k** — you are running this device eight times the lane's heaviest user. It is the single most-blown budget in the script.

**4. Abstract nouns doing the talking.** MEASURED + INFERRED. Nominalizations run **22.5/1k vs your gold's 11.8** — 1.9×. Worse than the rate is the *placement*: eight sentences put an abstraction in the subject slot where you'd put a person or a country — *"The violence they had started… came back"*, *"The count comes from Motyka"*, *"The same collaboration existed"*, *"The fact that we don't have this piece of paper is why…"*, *"That refusal hands Russia a weapon"*. Your gold almost never does this. Swapping to a human subject usually **saves words** and improves attribution (CH7's "The count comes from" fix answers a T4 flag you raised twice).

**5. Your own three loudest markers are missing.** MEASURED. `very` — gold **11.8/1k**, script **0**. Colloquial hedge family (`basically` / `kind of` / `I think` / `I guess`) — gold **~15.8/1k**, script **0.7**. `so` — covered in #1. VOICE-PROFILE correctly tells scripts to drop *"I guess"* nerve-hedges, but it never told them to strip `very`, `basically`, or clause-final `I think` — and FINGERPRINT §9 calls the hedge family constitutive. Five restorations, zero to two words each. The CLOSE fix in § 4 (CH-CLOSE-1) restores `I think` at **zero word cost** and is the highest-identity single edit in the file.

### The number you asked for

| | Words | Share |
|---|---|---|
| **Traceable to your own mouth** (≥40% 5-gram overlap with the ad-lib/read-aloud corpus) | 299 | **10.8%** |
| **Partially traceable** (15–40% overlap — your shape, Claude's polish) | 334 | **12.1%** |
| **Claude-authored** (<15% overlap) | 2,127 | **77.1%** |
| *Memo:* declared never-read-aloud (RE-SPEAK LIST) | 392 | 14.2% |

**≈23% creator-harvested / ≈77% Claude-authored.** MEASURED against an 8,293-token corpus built from `act1–act5-raw.md`, `act2b`, `act3a-retell`, `followups-raw.md` and every double-quoted string in `t1`–`t5` readthroughs. Conservative in both directions: a line you reworded loosely then Claude polished scores low (undercount), while a Claude line you *quoted back while criticising it* scores as yours (overcount). Treat 23% as a band of roughly 18–28%, not a point.

Per-chapter, the harvest is very unevenly spread — and it tracks the phrasing problems almost exactly:

| Chapter | Words | Harvest-linked | Never read aloud |
|---|---|---|---|
| COLD OPEN | 225 | 21% | 0% |
| CH1 Two things at once | 338 | 11% | **45%** |
| CH2 The lost state | 178 | 18% | 8% |
| CH3 The false dawn | 191 | 20% | 0% |
| CH4 The policemen | 193 | 34% | **44%** |
| **CH5 The army** | 273 | **3%** | 4% |
| CH6 Bloody Sunday | 132 | 30% | 0% |
| CH7 Two-sided? | 246 | 32% | 6% |
| **CH8 The missing paper** | 537 | 18% | 17% |
| CH9 The word | 139 | **50%** | 9% |
| CH10 Who the deadlock serves | 110 | 42% | 0% |
| CLOSE | 198 | 37% | 8% |

**CH5 is the outlier — 3% harvest-linked, and it holds the 56-word sentence, the 44-word Redesha frame and the 39-word Snyder frame.** CH9 and CH10, the most harvested chapters, are the cleanest. That correlation is the whole audit in one table.

---

## 1. Verdict on "still bloated with AI speak"

**Partly true, and not where you'd guess.** MEASURED:

**Where the instinct is WRONG — vocabulary.** Latinate content-word share is **7.6%**, *below* your gold (9.2%) and well below the lane (10.9%). Syllables per content word 1.96 vs gold 1.84, lane 2.02. Passive voice **2.9/1k vs lane 7.9**. Six condensation passes did their job: the diction is not inflated. Only about a dozen individual words sit above your register (§ 3), and half of those are unavoidable technical terms.

**Where the instinct is RIGHT — the joints and the breath.** The connective spine has been replaced by punctuation (§ 0.1), the sentences run past your natural ceiling (§ 0.2), the reveal devices are 8× budget (§ 0.3), and abstractions occupy subject slots (§ 0.4). None of that is "fancy words." It is exactly what you described as *"the logic and phrasing… and the way the script is structured with phrases"* — the grammar of an essay wearing plain vocabulary.

**Where the instinct overshoots — paragraph landings.** See § 6.4. The paragraph shape is inside the range of your own two locked, published scripts. Don't fix it.

---

## 2. The three-way metrics table

Same measurement code across all three references. Full sources in § Honest limits.

| Metric | **A. HIS GOLD** unscripted `yMAWJcjo_ug` (761w) | **B. LANE** 7 punctuated transcripts (18,535w) | **C. SCRIPT #62 v7.0** (2,760w) | Read |
|---|---|---|---|---|
| Sentences | 40 | 982 | 150 | |
| Median length | 13w | 16w | 16w | on-lane, above gold |
| Mean length | 19.0w | 18.9w | 18.4w | ✅ fine |
| % over 25w | 20.0 | 23.6 | 22.0 | ✅ fine |
| % over 35w | 12.5 *(all 5 are ASR artifacts → true ≈0)* | 8.6 | **8.7** | ⚠ vs gold |
| % under 8w | 22.5 | 15.6 | 14.0 | mild — fewer short beats than you |
| Clauses / sentence | 3.12 | 2.60 | 2.57 | ✅ fine |
| **Em-dash /1k** | 0 *(n/a in ASR)* | 2.0 | **24.6** | ⚠⚠ see § 6.1 |
| Front-loaded opener % | 0.0 | 11.2 | **18.0** | ⚠ but mostly benign — § 5.3 |
| Appositive /1k | 11.8 | 14.8 | 12.3 | ✅ fine |
| **Nominalization /1k** | 11.8 | 19.2 | **22.5** | ⚠⚠ |
| Passive /1k | 2.6 | 7.9 | 2.9 | ✅ good |
| Sentence-initial discourse marker % | 25.0 | 26.7 | 28.0 | ✅ rate fine, **mix wrong** ↓ |
| — `so` /1k | **11.8** | 5.5 | **3.3** | ⚠⚠ |
| — `but` /1k | **9.2** | 7.3 | **4.4** | ⚠ |
| — `because` /1k | 5.3 | 1.8 | 2.9 | ✅ |
| — `and` /1k | 34.2 | 26.6 | 30.4 | ✅ |
| Contractions /1k | 27.6 | 24.9 | 20.7 | mild |
| Latinate content-word % | 9.2 | 10.9 | **7.6** | ✅ **below** both |
| Syllables / content word | 1.84 | 2.02 | 1.96 | ✅ fine |
| Questions % of sentences | 0.0 | 4.6 | 2.0 | ✅ (3 questions, all answered) |
| **Colon-reveal /1k** | **0.0** | 0.0–0.7 | **6.2** | ⚠⚠⚠ |
| Interrupted-subject constructions | 0 | 0–1 per video | 9 | ⚠⚠ |
| `very` /1k | **11.8** | 1.7 | **0.0** | ⚠ identity |
| Colloquial hedge family /1k | **~15.8** | ~1.8 | **0.7** | ⚠ identity |
| Scholarly hedges (`essentially`/`arguably`/`largely`) | 0 | 0.13 | **0** | ✅ clean |

### The em-dash number needs a control — here it is

Comparing a *written* script's em-dashes against ASR transcripts that contain none is unfair. So the honest comparator is **your own locked, filmed, published scripts**:

| | so+but /1k | em-dash /1k | ratio em-dash : spoken connectors |
|---|---|---|---|
| **A. Gold unscripted** | **21.0** | 0 *(n/a)* | — |
| #56 locked/published (written) | 6.4 | 4.5 | **0.71** |
| #57 locked/published (written) | 6.7 | 22.3 | **3.33** |
| **#62 v7.0** | 7.6 | 24.6 | **3.24** |

MEASURED. Two things fall out, and both matter:

1. **This is not a #62 problem — it is a scripting-layer problem, and it started at #57.** #62 is a near-exact clone of #57's ratio. #56 wrote the same content with a quarter of the dashes.
2. **Every written script — including the two you filmed and shipped — cuts your spoken connectors to about a third of your natural rate.** 21.0 → ~6.5–7.6, consistently, across three scripts. That's the deepest measured drift in this whole audit and it long predates v7.0.

---

## 3. Diction: where the vocabulary sits above your register

MEASURED against a 10,473-word attested vocabulary (gold VTT + every published `.srt` + every published teleprompter/FINAL-SCRIPT + this project's `_adlib`). 48 content words in the VO appear nowhere in that corpus. Most are innocuous topic nouns you simply haven't had occasion to say (*livestock, o'clock, rifles, doors, statues, Galicia*) — no action. These are the ones that actually sit above your register:

| Word | Line | Verdict |
|---|---|---|
| **curated** | CH8 "This movement **curated** its own record" | ⚠ Modern gallery/tech word. You have never said it. → *"This movement cleaned up its own record"* or *"went back and edited its own record."* Note "curated" is also doing show-don't-tell work the next clause already does. |
| **offence** | CH1 "made it an **offence** to publicly disrespect them" | ⚠ British legal noun. → **"made it a crime to publicly disrespect them."** Your ad-lib says *"made insulting them criminal"* — but "insulting" narrows the law's actual wording, so keep *publicly disrespect* and swap only the noun. Precision holds. |
| **branded** | CH1 "get you **branded** a traitor" | Minor. Your ad-lib uses **"labeled"** ("labeled a Nazi collaborator"). → *"get you labelled a traitor."* |
| **visibly** | CH5 "the Germans were **visibly** losing" | Minor adverbial garnish. → *"the Germans were clearly losing"* or just *"were losing."* Saves 1. |
| **hardened** (killers) | CH5 "Not all of them were **hardened** killers" | Cliché collocation, not yours. → *"Not all of them were killers already"* — and it sets up the next clause ("but some already were") better. Saves 1. |
| **factored in** | CH7 "even with the retaliation **factored in**" | Business register + nominalization. → *"even with those killings counted."* Saves 1. |
| **grants** (concessive) | CH9 "Even Motyka **grants** that…" | Academic-concessive verb. → *"Even Motyka accepts that…"* |
| **pledges** | CH3 "it **pledges** the new state to…" | Borderline — it *is* the precise verb for a founding document binding a state. **Keep.** Flagging only so you can overrule me. |
| **inspiration / a current struggle** | CLOSE "look to the past for **inspiration in a current struggle**" | Two abstractions in six words, in the most personal beat of the script. → see CH-CLOSE-2. |
| **commemorating** | CLOSE "is **commemorating** men who…" | High-register — **but this sentence is 🔒-locked and T4 recorded no voice complaint on the Bucha line. NO REWRITE.** Flagged for your call only. |
| **perpetrators**, **undisputed**, **lopsided**, **registry** | various | **NOT flags — these are yours.** All four appear verbatim in `act4-raw.md` / `followups-raw.md`. Do not "simplify" them. |

Unavoidable technical vocabulary that stays: *denazification, exhumation, proclamation, auxiliary (policemen), reconciliation declaration, Operation Vistula, Sachsenhausen*. Historical precision outranks register here; every one names a specific thing with no plain synonym.

---

## 4. Chapter-by-chapter pass

Severity: **⚠⚠⚠** = fix before film · **⚠⚠** = fix if you touch the chapter · **⚠** = your call. Word delta given for every rewrite. Anything traceable to your mouth is in § 5 with **no rewrite**.

### COLD OPEN

**CO-1 ⚠⚠ — colon-reveal + withheld subject.**
> "Three weeks later, one of Ukraine's closest allies took its highest award back from Ukraine's president: Poland — the country that had been arming Ukraine, funding it, and taking in its refugees."

Tell: T8 colon-reveal used for **delayed identification** — the sentence deliberately withholds "Poland" for suspense, then re-opens with an em-dash appositive. Two suspense devices in 31 words. Gold = 0 of either. Also unsayable: subject-to-payload distance is 14 words.
→ **"Three weeks later, Poland took its highest award back from Ukraine's president. And Poland is the country that had been arming Ukraine, funding it, taking in its refugees."** *(−4 words. Two breaths. The "And Poland is the country that…" repetition is the gold-standard `and`-chain from FINGERPRINT §4, and it lands harder than the withheld reveal because the surprise was never the name — it was the reversal.)*

**CO-2 ⚠ — pseudo-cleft.**
> "What we're going to do is look at which of those grains the documents actually support."

Tell: `What X is/does…` pseudo-cleft. Gold = 0; lane = 0.3/1k. Your own `followups-raw.md` gives the natural shape: *"That's what I'm trying to do with this video. Look at the primary sources…"* — right-dislocated, not fronted.
→ **"So that's what I'm doing in this video. Looking at which of those grains the documents actually support."** *(+3 words. Restores a sentence-initial `so`, which the script is starved of.)*

**CO-3 — HOLD, no change.** The three-things evidentiary test (32w, colon, symmetric triad) is a **declared ledger beat** — explicitly sanctioned under T6 — and it is a structural promise the video keeps (header ¶ "What moved"). It is also your 2026-07-21 call. The only thing I'd consider is `so` for the colon, and I don't recommend even that: the colon is what makes the three items sound like a checklist, which is the point.

---

### CH 1 — TWO THINGS AT ONCE

*45% of this chapter has never been read aloud — the highest in the script. It also carries the longest sentence.*

**CH1-1 ⚠⚠⚠ — the 54-word sentence.** Longest in the script bar one.
> "They fought for an independent Ukraine against everyone who held it: the Germans arrested the movement's leader in 1941 and held him for three years, two of his brothers died in Auschwitz, and when the Soviets came back the UPA kept fighting them out of the forests into the 1950s, until they were finally defeated."

Tell: colon-reveal + three coordinated clauses + a trailing subordinate, all on one breath, in the beat where you first state one of the two grains. Nobody can deliver this.
→ **"They fought for an independent Ukraine against everyone who held it. The Germans arrested the movement's leader in 1941 and held him for three years, and two of his brothers died in Auschwitz. And when the Soviets came back, the UPA kept fighting them out of the forests into the 1950s, until they were finally defeated."** *(+4 words. Three breaths, `and`-chained across the boundary exactly as gold does — FINGERPRINT §4 "And-chaining across sentence boundaries when extending a case.")*

**CH1-2 ⚠⚠ — subject buried under two interruptions.**
> "In 2012 — three years before it passed — Grzegorz Rossoliński-Liebe, who wrote the leading biography of Bandera, tried to lecture on this in Ukraine."

Tell: **interrupted subject** — a fronted dashed parenthesis, then a name, then a relative clause, then finally the verb. 13 words between "In 2012" and "tried". Gold = 0 interrupted subjects; lane = 0–1 per video. This is the construction the ear most reliably loses.
→ **"Grzegorz Rossoliński-Liebe wrote the leading biography of Bandera. In 2012 — three years before that law passed — he tried to lecture on this in Ukraine."** *(+1 word. Name first, one fact per breath, and "that law" tightens the referent the ⚠ note in the ON-SCREEN block is already worried about.)*

**CH1-3 ⚠ — participial opener.**
> "Writing about these killings can get you branded a traitor, or a Russian agent."

Tell: participial (`-ing`) sentence opener. Gold = 0. Reads as written prose; also "branded" (§ 3).
→ **"Write about these killings, and you can get labelled a traitor, or a Russian agent."** *(+1 word. Imperative-then-consequence is your natural shape — FINGERPRINT §6 "invitations are imperatives.")*

**CH1-4 ⚠ — passive + agentless.**
> "His events were shut down by threats."
→ **"Threats shut the events down."** *(−2 words. Keeps the agent as vague as the ledger requires, but active.)*

**CH1-5 ⚠ — nominalization pair + register.**
> "…and made it an **offence** to publicly disrespect them."
→ **"…and made it a crime to publicly disrespect them."** *(±0. See § 3 — "insulting" would be tighter but narrows the law's actual wording. Precision wins.)*

---

### CH 2 — THE LOST STATE

**CH2-1 ⚠⚠⚠ — the 46-word chapter landing.**
> "And one of the movement's military thinkers, Kolodzinskyi, wrote down what that would mean in practice: when the day of independence came, the western lands would have to be cleared of other peoples — because land full of someone else's people is land someone else can claim."

Tell: colon-reveal + fronted temporal subordinate + em-dash-as-`because` + a passive at the exact moment the script states the doctrine that causes the massacre. Four constructions stacked on the chapter's most load-bearing sentence.
→ **"And one of the movement's military thinkers, Kolodzinskyi, wrote down what that would mean in practice. When the day of independence came, the western lands would have to be cleared of other peoples. Because land full of someone else's people is land someone else can claim."** *(+1 word. Three breaths; the final `Because` sentence is the causal landing, which is where you actually want the weight. Note the runtime menu calls this beat load-bearing and advises against cutting it — this makes it survive the ear without cutting anything.)*

**CH2-2 ⚠⚠ — three em-dashes in one sentence.**
> "And the west — Volhynia and Galicia — went to the new Poland, because the powers that had won the war sat around a table and assigned the land — and Ukraine wasn't at that table."

Tell: dashes 1–2 are a legitimate appositive; dash 3 is a **conjunction wearing a dash** (it means "but"/"and"). 33 words.
→ **"And the west — Volhynia and Galicia — went to the new Poland. The powers that won the war sat around a table and assigned the land, and Ukraine wasn't at that table."** *(±0 words. Your T4 harvest for this beat is "the WWI victors sat around the table and assigned land; Ukraine had no say" — this is closer to it.)*

**CH2-3 ⚠ — colon after a scene-setter.**
> "After the First World War, Ukrainians did what half of Europe was doing: they proclaimed a state of their own."
→ **"After the First World War, Ukrainians did what half of Europe was doing. They proclaimed a state of their own."** *(±0 words. One of the 14 withhold-reveals gone for free.)*

---

### CH 3 — THE FALSE DAWN

**CH3-1 ⚠⚠ — 33w, relative-clause chain into a nominalization triad.**
> "In 1941 the enemy of an independent Ukraine was Moscow — the power that had occupied Ukraine for two decades, and whose rule had meant terror, deportations, and a famine that starved millions of Ukrainians."

Tell: `whose`-relative (written register — zero instances in gold) hung off an appositive hung off an em-dash. The famine — the emotional peak of the sentence — arrives 30 words in.
→ **"In 1941 the enemy of an independent Ukraine was Moscow — the power that had occupied Ukraine for two decades. Its rule had meant terror, deportations, and a famine that starved millions of Ukrainians."** *(+3 words. Two breaths; the famine now lands as its own clause.)*

**CH3-2 ⚠ — split the Stetsko frame off the quote.**
> "And the text of this proclamation survives, signed by Stetsko — it pledges the new state to 'collaborate closely with National Socialist Greater Germany…'"

The frame *"And the text of this proclamation survives"* is **your verbatim T4 harvest — untouched.** Only the join is mine: an em-dash carrying a new independent clause into a 25-word quote.
→ **"And the text of this proclamation survives, signed by Stetsko. In it, the new state pledges to 'collaborate closely with National Socialist Greater Germany…'"** *(±0 words. Gives the reader-aloud a beat to land the document before the quote starts — and the ON-SCREEN note wants the autograph to BANG on "survives," which now gets its own sentence end.)*

**CH3-3 ⚠ — harvest drift, see § 5.** *"Not because they necessarily loved the Nazis — it was a practical alliance."* Your T4 harvest is *"Not because they loved the Nazis. It was a practical alliance."* Two changes crept in: an added "necessarily" and a period converted to an em-dash. Treated in § 5.

---

### CH 4 — THE POLICEMEN

**CH4-1 ⚠⚠⚠ — the 42-word motive list.**
> "They had joined for all kinds of reasons: a wage and food rations in a country that had little of either, an exemption for their family from the forced-labor roundups, and for some, the power it gave them over their neighbours."

Tell: colon-reveal + a three-item list built entirely from **noun phrases with no verbs** (`a wage`, `an exemption`, `the power`). This is the purest nominalization stack in the script — nobody *does* anything for 30 words. It's also the beat that decides whether the viewer sees these men as people or as a category.
→ **"They had joined for all kinds of reasons. Some wanted the wage and the food rations, in a country that had little of either. Some wanted their family kept out of the forced-labour roundups. And some just wanted the power it gave them over their neighbours."** *(+2 words. Human subject in every clause, verbs restored, colon gone. Note this is more precise, not less: it says explicitly that different men joined for different reasons, which the original list only implied — and it protects against the "they were all ideologues" reading McBride pp. 651–52 warns about.)*

**CH4-2 ⚠⚠ — 34w, double-dash interrupt.**
> "In time it turned on the Germans too — raiding prisons to free its people, ambushing convoys — though that was more to show Ukrainians whose side it was on than to actually hurt the Germans."

Tell: a 9-word parenthesis wedged between the main clause and its concessive, then a `more X than Y` comparative that has to be held across 20 words. *(The concessive tail — "though that was more to show Ukrainians whose side it was on" — is in the RE-SPEAK carry-over list from v6.1 and is close to your T4 dictation; I'm splitting around it, not rewriting it.)*
→ **"In time it turned on the Germans too — raiding prisons to free its people, ambushing convoys. Though that was more to show Ukrainians whose side it was on than to actually hurt the Germans."** *(±0 words. Same two units, one breath each.)*

**CH4-3 ⚠ — T5 violation (existing rule).**
> "the nationalist leadership had **quietly** ordered its own members into the police"

Tell: **Fable T5 sinister-understatement adverb** — the knowing-narrator wink. Gold = 0. Existing WARN-tier lexical flag, not my find.
→ drop the adverb: **"the nationalist leadership had ordered its own members into the police."** *(−1 word. The fact is sinister; the adverb tells the viewer how to feel about it, which is exactly the show-don't-announce directive from T4 root-cause #1.)*

**CH4-4 ⚠ — chapter landing carries a colon and 32 words.**
> "But Ukraine had an extra layer: the nationalist leadership had ordered its own members into the police — to get trained, collect weapons and intelligence for the army it planned to build."
→ **"But Ukraine had an extra layer. The nationalist leadership had ordered its own members into the police — to get trained, and to collect weapons and intelligence for the army it planned to build."** *(+2 words. "But Ukraine had an extra layer." is in the RE-SPEAK carry-over list — keep the wording exactly, just close the sentence.)*

---

### CH 5 — THE ARMY

*3% harvest-linked — the least of any chapter, and it shows.*

**CH5-1 ⚠⚠⚠ — the 56-word sentence. The worst single line in the script.**
> "In the spring of 1943, the call went out, and around five thousand policemen deserted the Germans and joined the nationalists in the forest — the leadership wanted those men before anyone else got them — the police were leaving the losing side anyway, and whoever took them in got an army: rifles, training, and everything 1942 had taught them."

Tell: everything at once — fronted PP, two em-dashes both acting as sentence boundaries, three appositive units, a colon-reveal, and a final triad. Fifty-six words. Your gold's ceiling is thirty.
→ **"In the spring of 1943, the call went out, and around five thousand policemen deserted the Germans and joined the nationalists in the forest. The leadership wanted those men before anyone else got them. The police were leaving the losing side anyway, and whoever took them in got an army — rifles, training, and everything 1942 had taught them."** *(+4 words. Three breaths. "everything 1942 had taught them" is untouched — you've read it clean five times and OPEN QUESTION #5 is an accuracy question, not a phrasing one; nothing here bears on it.)*

**CH5-2 ⚠⚠ — fronted object + interrupted subject + colon.**
> "What the new army did with men like him, Redesha himself explained after the war, under interrogation: 'We burned Polish settlements…'"

Tell: the object clause is fronted, the subject then arrives mid-sentence and is immediately interrupted by two adverbials before the quote. Three delays before the document speaks — and T4 root-cause #1 says point with the screen, weigh in voice.
→ **"After the war, under interrogation, Redesha explained what the new army did with men like him: 'We burned Polish settlements…'"** *(−3 words. Colon retained — quote hand-off colons are exempt from the T8 cap.)*

**CH5-3 ⚠ — 39w Snyder frame.**
> "As the historian Timothy Snyder puts it, they believed Ukraine's final enemy would be 'a resurrected Poland' — a Poland that, just like the last time, would point at the Poles living in the west and claim the land again."

Tell: fronted attribution + quote + em-dash appositive that itself contains an interrupted subject (`a Poland that, just like the last time, would point`). VOICE-PROFILE § "Owning source weight aloud" wants the source weighed in voice — this frame does it, so the attribution stays; the tail is the problem.
→ **"As the historian Timothy Snyder puts it, they believed Ukraine's final enemy would be 'a resurrected Poland.' A Poland that, just like the last time, would point at the Poles living in the west and claim the land again."** *(±0 words. The fragment-second-sentence is deliberate and is a shape you use — FINGERPRINT §1 records short functional sentences at 13%.)*

**CH5-4 ⚠ — diction.** *"Not all of them were **hardened** killers"* → **"Not all of them were killers already"** *(−1; sets up "but some already were" cleanly). *"the Germans were **visibly** losing"* → **"the Germans were clearly losing"** *(±0).*

---

### CH 6 — BLOODY SUNDAY

*The tightest chapter in the script — 132 words, eight sentences, median 14w, and it does the most work per word anywhere in the video. One item.*

**CH6-1 ⚠⚠ — the 39-word landing, and the cheapest fix in the file.**
> "We know this because a Polish husband-and-wife team, the Siemaszkos, spent decades building a registry of the dead — in their volumes, they list about thirty-six thousand names, one by one, often with the cause of death."

Tell: em-dash carrying a full independent clause, on a 39-word sentence, at the moment the registry — the video's emotional exhibit — arrives.
→ **"We know this because a Polish husband-and-wife team, the Siemaszkos, spent decades building a registry of the dead. In their volumes they list about thirty-six thousand names, one by one, often with the cause of death."** *(−1 word. Literally free. And the pause between the two sentences is where the wall-of-names graphic wants to land.)*

---

### CH 7 — TWO-SIDED?

**CH7-1 ⚠⚠⚠ — abstract subject + colon, on the concession beat.**
> "The violence they had started in 1943 came back the other way: Polish underground units hit Ukrainian villages in 1944, and in 1947 communist Poland deported around a hundred and forty thousand Ukrainians from their homes in Operation Vistula."

Tell: abstract noun as subject (`The violence… came back`) + colon-reveal, 36 words. This is your steelman beat — VOICE-PROFILE § Steelman/concede — and it is the one place the script most needs to sound like a person conceding, not a paragraph resolving.
→ **"The violence they started in 1943 came back the other way. Polish underground units hit Ukrainian villages in 1944, and in 1947 communist Poland deported around a hundred and forty thousand Ukrainians from their homes in Operation Vistula."** *(−1 word. Colon gone, two breaths, and dropping "had" tightens the tense per VOICE-PROFILE § Tense.)*

**CH7-2 ⚠⚠ — abstract subject hiding an attribution T4 flagged twice.**
> "The count comes from Grzegorz Motyka, Poland's leading historian of the UPA: roughly seventy thousand dead Poles to twenty thousand dead Ukrainians, with the UPA starting most of it."

Tell: `The count comes from X:` — an abstraction in the subject slot, the human moved into a prepositional phrase, and the verdict clause (`with the UPA starting most of it`) left dangling as an absolute construction with **no stated speaker**. Your T4 note asks of this exact line: *"whose claim? Do we have a document? Do Ukrainians also agree?"*
→ **"Grzegorz Motyka, Poland's leading historian of the UPA, puts it at roughly seventy thousand dead Poles to twenty thousand dead Ukrainians — and he says the UPA started most of it."** *(−1 word. Person as subject; the contested clause is now explicitly Motyka's, which is more accurate, not less. The very next line — "Ukraine's official historians mostly dispute the framing… They don't dispute the numbers" — reads twice as sharply once the numbers have a named owner.)*

**CH7-3 ⚠ — register.** *"even with the retaliation factored in"* → **"even with those killings counted"** *(−1).*

**CH7-4 — HOLD.** The chapter's exit — *"You cannot call that spontaneous. Then the question becomes: who organized it?"* — is your T4 verbatim harvest and you called the joint "perfect." **No rewrite.** The colon there is yours. See § 5.

---

### CH 8 — THE MISSING PAPER

*537 words, the longest chapter, 18% harvested. It is also the chapter that must survive being listened to once, without rewind.*

**CH8-1 ⚠⚠⚠ — the 40-word custody sentence with a 12-word appositive between subject and verb.**
> "And Ukraine's answer — from the man who ran both the state archive and the state's memory institute — is that none of it is real: the confession faked by the KGB, the letter not even in the file it's cited from."

Tell: interrupted subject (12 words between "answer" and "is") + colon-reveal + two verbless noun-phrase items. In the single most evidentially delicate paragraph in the video, the listener has to hold an unfinished subject across an appositive and then unpack two headless fragments.
→ **"And Ukraine's answer comes from the man who ran both the state archive and the state's memory institute. He says none of it is real — the confession was faked by the KGB, and the letter isn't even in the file it's cited from."** *(+3 words. Two breaths, verbs restored in both items, and the attribution now sits in its own clause where the ear can catch that this is a *person's* claim, not a country's. That distinction is the whole beat.)*

**CH8-2 ⚠⚠ — pseudo-cleft + colon on the custody verdict.**
> "What survives is a transcription from an archive nobody can check: classified again, by the best account, or burned when the Soviet Union collapsed."

Tell: `What X is…` pseudo-cleft (gold 0) + colon-reveal + the nominalization `transcription`. And this line carries a **binding landmine** — "letter = published transcription ONLY, never 'we have the letter'" — so the rewrite must not lose "transcription."
→ **"So what we have is a transcription, from an archive nobody can check. Classified again, by the best account — or burned when the Soviet Union collapsed."** *(+1 word. `So what we have is` is the right-dislocated shape you actually use; "transcription" preserved exactly; the alternatives now get their own breath, which is where the doubt should sit.)*

**CH8-3 ⚠⚠ — 35w, subject-verb distance.**
> "In 1944, with the Soviets slowly defeating the Germans, many UPA units made a secret deal with the Germans for the weapons they were leaving behind — while presenting themselves to the world as anti-Nazi fighters."

Tell: fronted PP + fronted absolute clause (`with the Soviets slowly defeating…`) before the subject arrives, then an em-dash carrying a participial contrast. Two front-loads plus a dangling participle.
→ **"By 1944 the Soviets were slowly beating the Germans. And many UPA units made a secret deal with the Germans for the weapons they were leaving behind — while telling the world they were anti-Nazi fighters."** *(±0 words. "presenting themselves to the world as" → "telling the world they were" swaps a nominal for a verb and drops a syllable-heavy phrase; the reversal is the point of the beat and it now lands as one clean contrast.)*

**CH8-4 ⚠ — diction.** *"This movement **curated** its own record, and you can watch it happen."* This sentence is on the RE-SPEAK LIST (never read aloud). → **"This movement went back and edited its own record, and you can watch it happen."** *(+3 words. "edited" is the word the beat's own payoff uses — "They were not misremembering. They were purposefully editing" is your T4 harvest — so this plants it early instead of introducing a word you'd never say.)*

**CH8-5 ⚠ — colon on the museum landing.**
> "And after Ukraine finally became independent in 1991, that edited version made it home: in a Bandera museum outside Lviv, the proclamation went on display with the Hitler passage missing."
→ **"And after Ukraine finally became independent in 1991, that edited version made it home. In a Bandera museum outside Lviv, the proclamation went on display with the Hitler passage missing."** *(±0.)*

**CH8-6 — HOLD, two lines.** *"But if we follow these orders and reports back to the top, at a certain point the paper stops."* and *"What no one can actually produce is an order to kill the Poles with his signature on it."* — both are your T4 verbatim harvests (the second is also in the RE-SPEAK carry-over list). The second is a pseudo-cleft, which everywhere else in this audit I'd flag. **Your mouth produced it. No rewrite.** See § 6.2.

---

### CH 9 — THE WORD

*50% harvest-linked — the cleanest chapter in the script. Two small items, both structural rather than voice.*

**CH9-1 ⚠⚠ — abstract subject with an interrupted predicate.**
> "The fact that we don't have this piece of paper is why, eighty years later, Ukraine and Poland still can't agree what to call this massacre."

Tell: `The fact that…` as subject — the most bookish subject construction in English — plus an adverbial wedged between "why" and its clause. 26 words before the actual dispute is named.
→ **"And because that piece of paper is missing, Ukraine and Poland still can't agree what to call this massacre — eighty years later."** *(−4 words. `Because` opens it, which is your causal register; "eighty years later" moves to the end where it hits as the sting instead of as a speed bump.)*

**CH9-2 ⚠ — two semicolons.** A semicolon is inaudible; there is no way to read one. The script has two, both in this chapter.
> "…no signed order ever surfaced; what convinced him…" → **"Even Motyka accepts that no signed order ever turned up. What convinced him to call it a genocide was the coordination — everything going off everywhere at once."** *(±0. "what convinced him to call it a genocide was the coordination" is your T4 verbatim — untouched.)*
> "…blocked the exhumation of the graves; the digs only resumed in 2025." → **"For years it even blocked the exhumation of the graves. The digs only resumed in 2025."** *(±0.)*

---

### CH 10 — WHO THE DEADLOCK SERVES

**CH10-1 ⚠⚠⚠ — 46 words, subject and verb 21 words apart.**
> "All while Russia sits on the Soviet central files — the same files the Soviet Union held for fifty years while calling these men fascist butchers — and has never produced the one piece of paper that would prove the directive to cleanse Volhynia came from the top."

Tell: the second verb (`has never produced`) is stranded 21 words from its subject by a 20-word dashed parenthesis. The closing clause is **your T4 verbatim harvest** — *"has never produced the one paper that would prove that this directive to cleanse Volhynia of the Poles came from the top"* — and it is the argumentative summit of the whole video. Right now it arrives out of breath.
→ **"All while Russia sits on the Soviet central files — the files the Soviet Union held for fifty years while calling these men fascist butchers. And Russia has never produced the one piece of paper that would prove the directive to cleanse Volhynia came from the top."** *(+4 words. Your harvested clause now gets a full breath and a sentence-initial `And`, which is how you chain a case in the gold. This is worth four words.)*

**CH10-2 ⚠ — colon + abstract subject.**
> "And that refusal hands Russia a weapon: Russia takes this real, undisputed crime and uses it to argue that Ukraine is a Nazi state — and that view then justifies a war against it."
→ **"And that refusal hands Russia a weapon. Russia takes this real, undisputed crime and uses it to argue that Ukraine is a Nazi state — and that argument then justifies a war against it."** *(±0. "view" → "argument" because it's an argument being made, not a view being held — marginally more precise as well as more concrete. "undisputed" is yours, kept.)*

---

### CLOSE

**CH-CLOSE-1 ⚠⚠⚠ — the highest-identity edit in the script, at zero word cost.**
> "Because that, in the end, is what this whole fight is about: whether you can glorify people for one thing they stood for, when they also did other terrible things."

Tell: your T4 thesis harvest was a **question with a clause-final hedge** — *"Are you justified in glorifying people for one event or for one reason, even if they did other bad things? **I think that's the whole fight.**"* The script converted it into a fronted cleft (`Because that, in the end, is what… about:`) with a colon-reveal and demoted your question to a subordinate `whether`-clause. Every one of your signature markers was stripped in the conversion: the question, the first-person stance, the clause-final `I think`.
→ **"And that, I think, is the whole fight. Can you glorify people for one thing they stood for, when they also did other terrible things?"** *(±0 words. Restores `I think` — one of your two most frequent gold markers and currently at zero across 2,760 words — and restores the question you chose twice. FINGERPRINT §6 records zero *free-floating rhetorical* questions, but this is the permitted type: a genuine question the video has just spent fifteen minutes answering.)*

**CH-CLOSE-2 ⚠⚠ — two abstractions in the most personal sentence in the script.**
> "In my opinion, it's not wrong to look to the past for **inspiration in a current struggle**."

Tell: `inspiration` + `a current struggle` — two abstract nouns in a beat that opens with `In my opinion` (a pure gold first-person stance marker). The frame is yours; the payload is essay vocabulary.
→ **"In my opinion, there's nothing wrong with looking to the past for heroes when you're in a fight now."** *(±0 words. "heroes" is the video's own keyword — it's in the title, the decree and the cold open — so this closes a loop the current wording leaves open. "a fight now" is concrete and second-person.)*

**CH-CLOSE-3 — HOLD, flagged only.** *"The same state that calls Russia's atrocities at Bucha by their name is commemorating men who did similar things to the Poles, eighty years ago."* — 🔒 locked, and T4 explicitly records "Bucha line: no voice complaints." It carries an interrupted subject (10 words) and `commemorating`. **No rewrite.** If you ever unlock it: *"The same state that calls Russia's atrocities at Bucha by their name is honouring men who did similar things to the Poles, eighty years ago"* — one word, and "honouring" is the decree's own verb.

---

## 5. Harvested lines — FLAGGED, NO REWRITES

Every line below trips something this audit flags elsewhere, **and came out of your mouth.** Your mouth is ground truth on whether a line is sayable. They are listed so you can see the tension, not so you can act on it — and so that no future pass "fixes" them by accident.

| Line | Source | What it trips | Why it stands |
|---|---|---|---|
| "And to understand how we got to the massacre, we have to go back a hundred years — to a country that lived for about three years, and then disappeared." | T4 verbatim harvest | **Fable T7 — HARD ban on "to understand X we have to go back"** | See § 6.2. A HARD lint rule is contradicted by your own dictation. Rule needs scoping; line stands. |
| "You cannot call that spontaneous. Then the question becomes: who organized it?" | T4 verbatim | Colon-reveal (T8) + period-stab (VOICE-PROFILE demotes) | You called this joint *"perfect"* at T4. Untouchable. |
| "What no one can actually produce is an order to kill the Poles with his signature on it." | T4 verbatim + RE-SPEAK carry-over | Pseudo-cleft (gold = 0) | Your construction. Everywhere else I'd flag it; here it's evidence the gold's zero is a sample-size artifact, not a ban. |
| "But if we follow these orders and reports back to the top, at a certain point the paper stops." | T4 verbatim | Fronted `if`-subordinate before main verb | Yours. |
| "That isn't a mob of angry people — that's an officer reporting up a chain of command." | T4 verbatim ("That is an officer reporting up a chain of command") | **Fable T1 negation-correction engine** — the headline tell | Yours, and the negated claim is live (the video's whole question is mob-vs-order). T1's budget rule calls this an *earned* pair. Stands. |
| "The anti-Polish sentiment was alive and well in the UPA." | T4 verbatim | Nominalization as subject | Yours, and it replaced a line you rejected outright ("their own papers carry the mood" — *"I never talk like this. Never, never, never."*). Stands. |
| "…the passage pledging collaboration with Hitler's Germany is simply gone. **They erased it.**" | T5 verbatim | **T5 sinister-understatement adverb** (`simply`) + period-stab | Yours, both halves, from T5. Stands. Contrast CH4-3's "quietly," which is Claude's — that one goes. |
| "That's the main point of contention." | T4 verbatim (replaced "deadlock" — *"Deadlock, I don't talk like this"*) | `contention` nominalization | Yours. Note the chapter heading still says "WHO THE DEADLOCK SERVES" — the word you rejected survives in the heading. Cosmetic; VO is clean. |
| "…has never produced the one piece of paper that would prove the directive to cleanse Volhynia came from the top." | T4 verbatim | Nominalization (`the directive`) | Yours. CH10-1 splits the sentence *around* it without touching a word of it. |
| "what convinced him to call it a genocide was the coordination" | T4 verbatim | Pseudo-cleft + nominalization | Yours. CH9-2 changes only the punctuation before it. |
| "Two-sided is half right." / "They don't dispute the numbers." | RE-SPEAK #7 / near-harvest | Period-stab verdicts | Read-adjacent; both are five words and land. Leave. |
| "Not because they necessarily loved the Nazis — it was a practical alliance." | T4 verbatim, **with drift** | — | ⚠ **The only harvest-drift I found.** Your version: *"Not because they loved the Nazis. It was a practical alliance."* The script added **"necessarily"** and swapped your period for an em-dash. Restoring your exact wording saves 1 word. This is a restoration, not a rewrite. |
| "main perpetrators" · "undisputed" · "lopsided" · "registry" · "blocked the exhumation of the graves" | `act4-raw.md`, `followups-raw.md` | Latinate / high-register on a naive diction scan | **All four are your words.** Any future diction pass that flags them is wrong. |

---

## 6. Identity check — where the lane and your fingerprint disagree

House rule: lane practice is IDEA tier; **your measured fingerprint and your live picks win.** Four live conflicts.

### 6.1 Sentence length — fingerprint wins, and it was probably already pushed the wrong way

**Lane says fine. Your gold says no.** MEASURED both ways:
- Lane (7 punctuated, 18,535w): 8.6% of sentences over 35 words; 9% land in the 31–40 band; 5% run past 41.
- Your gold: 26–30w is the top real bucket. **Every sentence over 40 words in the gold transcript is an ASR punctuation gap, not an utterance.** True over-35 rate ≈ 0%.
- Script: 8.7% over 35 — **statistically indistinguishable from the lane, and off the end of your own distribution.**

If a prior pass justified long chained sentences by pointing at the lane, that reasoning is unsound *for you*. Six sentences at 40–56 words is not lane-normal-therefore-fine; it is lane-normal-therefore-someone-else's-mouth.

⚠ **And the correction has a documented failure mode.** VOICE-PROFILE's HEADLINE CORRECTION says chopping is the **#1 "too-AI" tell** and that the fix for a generated-sounding line is usually *stop chopping*. Both things are true and they don't conflict, because the canon already resolves it — Natural→Scripted table, row 3: *"Long causal run-on (natural speech) → **Two medium sentences** — NOT a run-on, NOT staccato."* **Every split in § 4 produces two flowing sentences. None produces a stab.** If a rewrite in this file ever reads as a stab, it's wrong — reject it.

### 6.2 The T7 HARD ban is contradicted by your own mouth

**Fable T7 marks "to understand X we/you have to go back" as a HARD lint rule**, on the evidence that #56's version matched the zero-guidance AI control *verbatim*. That is real evidence.

But your **T4 dictation produced the construction unprompted**: *"And to understand how we got there… we have to go back a hundred years, to a country that lived for about three years, and then disappeared."* It's in the harvest list, and it's in the script.

**Your live production beats a corpus-derived HARD rule.** Two readings, and I can't settle it from here:
- (a) The tell is the *bare* tour-guide form ("To understand the Kurdish question, you have to go back to…") — abstract topic, no destination. Your version names a destination and characterises it in the same breath ("a country that lived for about three years, and then disappeared"), which is the opposite of tissue: it's a hook.
- (b) You absorbed the phrase *from reading the script* across five read-throughs, and the harvest is contaminated.

**Recommendation:** keep the line, and **do not let T7 fire as HARD on it**. Flag for the next `/voice grill` — it needs one clean A/B against a version with the same destination and no "to understand" frame. Until then this is unresolved, not settled.

### 6.3 Hedges — the profile and the fingerprint genuinely disagree, and both are partly right

- FINGERPRINT §3 measures the colloquial hedge family at ~15.8/1k and §9 calls it *constitutive*.
- VOICE-PROFILE's Natural→Scripted table says drop *"I guess"* — "that was first-video nerves."
- Script: **0.7/1k.** `basically` 0, `I think` 0, `I guess` 0, `very` 0. Only `actually` survives at 1.45/1k, which is dead-on your gold's 1.31.

**Reading:** the profile's instruction was narrow — drop the *humility* hedge that undercuts a claim. It was applied as a blanket strip. `very` isn't a hedge at all (it's your intensifier, gold 11.8/1k, and FINGERPRINT §9 explicitly says *do not flag it — it's him*), and clause-final `I think` on a **verdict** is the opposite of nerves: it's the referee register the whole video is built on. CH-CLOSE-1 restores exactly one `I think`, at the one place the argument becomes yours. That's the minimum honest correction.

### 6.4 Paragraph landings — the lane can't answer this, and your own scripts disagree with each other

The brief asks whether every paragraph resolves on a landing (Fable T4). **I cannot measure this against the lane or the gold** — auto-caption transcripts have no paragraph structure at all. So the only valid comparator is your own written scripts. MEASURED:

| | Paras (2+ sents) | Ends on the paragraph's **longest** sentence | Ends on a **button** (≤0.6× para mean) | Ends ≤9w | Last-sentence / mean ratio |
|---|---|---|---|---|---|
| **#62 v7.0** | 34 | **47%** | 24% | 18% | **1.20** |
| #57 locked/published | 36 | 25% | 39% | 58% | 0.91 |
| #56 locked/published | 21 | **57%** | 0% | 24% | 1.12 |

**#62 sits between your own two shipped scripts and closer to #56.** Fable T4 asks for "roughly a third of paragraphs ending on plain information or a forward link" — #62 clears that. **Do not add buttons. Do not remove them either.** The T4 tell is not firing here.

What *is* firing is a different thing wearing T4's clothes: **eleven paragraphs end on their longest sentence, and in six of those the landing runs 30–46 words.** The problem isn't that the paragraph fails to land — it's that the landing arrives after the listener has run out of air. CH2-1, CH5-1, CH6-1, CH8-1 and CH10-1 all fix a *breath* problem that looks like a *shape* problem. **This corrects the brief's framing: the paragraph-level issue is breath, not buttons.**

---

## 7. Precision-preserving simplification pairs from the lane

IDEA tier throughout — these are moves, not rules, and none of them is binding. Verbatim + timestamp from the 14 pulled transcripts. Selected for the transformation move, and specifically for moves this script could use.

**P1 — Stefan Milo, "First Human Footprints in America?" [8:17–8:28] — *name the mechanism, not the term*.**
> "This is a problem because aquatic plants can pull old carbon out of the lake mud and sludge through their roots, and can potentially give a much older radiocarbon date than their real age."

The reservoir effect is never named. He describes the physical thing happening (*roots pull old carbon out of mud*) and then states the consequence in the same breath. **Nothing is vaguer** — "much older than their real age" is precise about direction and about the fact that it's an artefact. **Where #62 could use it:** CH8's custody argument. "Classified again, by the best account, or burned when the Soviet Union collapsed" is doing this already; "a transcription from an archive nobody can check" is not — it names a category instead of describing a state of affairs.

**P2 — Milo, same video [9:39–9:56] — *let the pattern carry the inference*.**
> "…they are younger in the top and older at the bottom. That is a great sign that these dates are accurate. If there was something going on with the Ruppia plants pulling old carbon, you might expect the dates to be all jumbled up perhaps. But they are in the correct order, from oldest to youngest."

He states the observation, states what the alternative *would* look like, then states what was actually seen. **This is exactly the shape of your cold-open evidentiary test** — "if an order came down from the top, it would have left three things behind." Milo's version is the same logic in ordinary words, and note the hedge (`perhaps`) sitting inside the technical reasoning rather than being stripped out of it.

**P3 — Premodernist, "Library of Alexandria" [5:21–5:49] — *inventory the absence*.**
> "…we don't have direct evidence of this about the library itself, because in fact we have extremely little information to go on about the library itself in terms of historical data. We have no archaeological information – or virtually none. The site of the Museum has not been excavated. And literary references to the library are very rare. We have just a few mentions in various sources, usually just mentions in passing when talking about something else."

The single most transferable passage in the whole lane for this video. He argues from *absence of evidence* without a single abstract noun and without hedging into mush: he **enumerates the specific things that don't exist** (no dig, few literary mentions, and those in passing). Note the self-correction *"or virtually none"* left in — precision *increased* by an interruption. **Where #62 could use it:** CH8, the paper-stops beat. "At a certain point the paper stops" is your line and it's good, but the inventory that would earn it is currently compressed into "the historians who've tried can't get the file."

**P4 — Premodernist, "Seward's Folly" [0:00–0:27] — *state the myth, deny it flat, promise the mechanism*.**
> "…it's often perceived as 'Seward's folly,' that there was no economic benefit seen at the time for it, it just seemed like an Arctic wasteland… But in fact that's not true. Many people at the time, in 1867, saw a lot of value in Alaska and approved of the purchase."

Four words for the denial — *"But in fact that's not true"* — and no metaphor anywhere. **Directly relevant to CH7's "Two-sided is half right,"** which does the same job in five words and is one of the best lines in your script. Confirms the move; no change needed.

**P5 — Historia Civilis, "The Pomerium" [8:52–8:59] — *turn an abstract legal effect into a physical event*.**
> "When proconsuls or propraetors crossed the pomerium, all of their legal command authority evaporated, instantly transforming them back into private citizens."

A jurisdictional boundary rendered as something that *happens to a person when he walks*. **Where #62 could use it:** CH1's 2015 law. "Ukraine wrote them into law as fighters for Ukrainian independence, and made it an offence to publicly disrespect them" is accurate and inert. What the law *does to a person* — that's the Rossoliński-Liebe beat sitting right after it, currently doing that work separately. Not a rewrite I'd force; a connection worth noticing.

**P6 — Historia Civilis, same [16:03–16:09] — *the one-sentence plain summary, at the end, after the detail*.**
> "So broadly speaking, we can say that the pomerium was the legal mechanism that separated Rome's military from Rome's government."

Sixteen minutes of Roman constitutional arcana, closed with one sentence a stranger could repeat. Note `So broadly speaking, we can say that` — an explicit scope-hedge that makes the compression honest rather than glib. **Where #62 could use it:** you have this — *"It tells you what kind of record we're reading"* (CH8's landing, 9 words). It's the best summary line in the script and it does the job in half the words. No change; noted as confirmation that your instinct here is already at lane standard.

**P7 — Religion for Breakfast, "Gen Z" [0:45–1:07] — *numbers as a shape, not a list*.**
> "Back in 2007, about 78% of American adults identified as Christian. By 2024, that number sat at roughly 63%… But notice here that this long downward slide is not continuing at the same pace. Over the last 5 years or so, the graph has stabilized, hovering in roughly the 60 to 64% range."

Two anchors, then the *shape*. Every number carries `about` / `roughly` / `or so` — the hedges are what make it precise, because the underlying data is a range. **Where #62 could use it:** CH7's 70K:20K. CH7-2's rewrite already moves toward this by attributing to Motyka; "roughly" is already in your line. Confirms the practice.

**Move summary:** *name the mechanism not the term* (P1) · *state what the alternative would look like* (P2) · *enumerate the specific absences* (P3) · *deny flat in four words* (P4) · *render the abstract as something that happens to a person* (P5) · *close on one repeatable sentence with an honest scope-hedge* (P6) · *anchor, then shape, and keep the hedges* (P7).

---

## 8. Runtime effect

The rewrites in § 4 net out at roughly **+8 to +12 words** across the whole script — about four seconds. Individually: eleven are word-neutral or negative (CO-1 −4, CH1-4 −2, CH5-2 −3, CH6-1 −1, CH7-1 −1, CH7-2 −1, CH7-3 −1, CH9-1 −4, CH4-3 −1, CH5-4 −1, plus six at ±0), and the additions are all breath-splits on the six longest sentences (+1 to +4 each).

**This audit does not get you to 12 minutes and does not try to.** The RUNTIME MENU is correct that word-level tightening is exhausted and only a deleted beat moves the number. What these edits do is make the 15 minutes deliverable in one take. If you take Menu option **A** (merge CH4+CH5, −150), note that CH4-1 and CH5-1 — two of the three worst sentences in the script — both live inside the merged material, so run the merge first and re-apply from this file afterwards.

---

## 9. Honest limits

1. **Extraction disagreement.** My VO extractor yields **2,760 words**; the script header says 2,843 and the RUNTIME MENU says 2,816. The gap is a few dozen words in inline-bold and ⚠-prefixed lines I skip. Per-chapter counts here will not match the RUNTIME MENU exactly. Nothing in the analysis turns on it, but don't cite my numbers for runtime.
2. **Lane transcripts are unpunctuated for 7 of 14.** Atun (×2), fig tree (×2), RFB atheists/lilith/statues came back as single unbroken blocks. **Every sentence-level lane statistic in § 2 uses only the 7 punctuated transcripts** (18,535 words). Word-level statistics (Latinate share, connectors, syllables) use all 14 (38,105 words). Where a table says "lane," check which. `youtube_transcript_api` is IP-blocked from this machine; the 14 files are the entire available sample and were not re-pulled.
3. **Punctuation is the transcriber's, not the speaker's, in every lane and gold figure.** Em-dash rates for A and B are structurally zero and mean nothing. That is precisely why § 2 adds the written-script control table — the em-dash finding rests on that table, not on the lane comparison.
4. **The gold is one video, 761 words, 40 sentences.** Every gold figure is a single-sample point estimate on a *nervous first recording*. `so` at 11.8/1k could plausibly be 8 or 15 in a bigger sample. The direction of the finding (script ≪ gold) is robust; the magnitude is not. FINGERPRINT's own header says the same.
5. **The 23%/77% harvest split is a band, not a point.** Method and both bias directions stated in § 0. It measures *5-gram lexical overlap*, which is a proxy for authorship, not authorship itself.
6. **Paragraph-shape has no external comparator at all** (§ 6.4) — only your own two shipped scripts, n=21 and n=36 paragraphs. Weakest evidence in the file; treated accordingly.
7. **Nominalization, appositive, passive and front-loading counts are regex heuristics.** They over-count (proper nouns ending `-tion`, appositives that are really lists) and under-count (zero-derived nominals like *"the count"*, *"the killing"* — which is why § 0.4 leans on the eight hand-checked abstract subjects rather than on the rate alone). Ratios between corpora are more reliable than any single number.
8. **I did not re-verify a single historical claim.** Every rewrite preserves the claim, the attribution and the hedging of the line it replaces, and where a rewrite could shift precision (CH1-5 *offence/crime/insulting*, CH3-2 *pledges*, CH7-2 *Motyka's attribution*, CH8-2 *transcription*) I said so inline and defaulted to the more precise option. If any rewrite reads as trading accuracy for smoothness, it's wrong — reject it and tell me.
9. **Six lines carry binding landmines** (header ¶ "Landmines"). CH8-2 touches the transcription line; I preserved "transcription" exactly and never wrote "we have the letter." No other rewrite touches a landmine line. **Re-check CH8-2 against the landmine list before it goes in.**

---

## 10. Reproduce this

```
scratchpad/  (session 29d2bb97)
  attrib.py   harvest-vs-authored split, per chapter
  line.py     per-paragraph + per-sentence flag diagnostic (the § 4 source)
  para.py     paragraph-shape stats + attested-vocabulary diction check
scratchpad/  (session 5c2c8af8 — prior agent, reused unchanged)
  metrics.py  three-way metric table + extraction/normalisation
  metrics2.py adds his locked/published scripts as controls
  dist.py     sentence-length histograms
  tx/         14 lane transcripts
```
Corpora: `transcripts/voice-analysis-unscripted.en.vtt` (gold) · `_adlib/*.md` (his mouth) · `_ARCHIVED/published/*/FINAL-SCRIPT-TELEPROMPTER.txt` + `*.srt` (his written and delivered) · `scratchpad/tx/*.txt` (lane).
