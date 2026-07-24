# VERIFY — SCRIPT.md v7.0 (2026-07-21)

**Scope:** VO only, `## SCRIPT` → `## PRONUNCIATION`, excluding `>` ON-SCREEN blocks (read as evidence of card intent, not checked as VO). **This is a gate, not an improvement pass.**
**Baseline:** last formal pass was `03-FACT-CHECK-VERIFICATION.md` against v6.1 (2026-07-19). v7.0 restructured, merged CH4+CH5, applied 32 phrasing rewrites (`scratchpad/apply_phrasing.py`, `E = [...]`), and swapped 18 em-dashes for connectors (`_research/CONNECTOR-PICKS-2026-07-21.md`). No git baseline exists — the diff was reconstructed from those two files plus the SCRIPT.md header.
**Authorities used:** `01-VERIFIED-RESEARCH.md` · `_research/SOURCE-GENEALOGY.md` (rows 1–12 + 2026-07-17/18/19 addenda) · `SOURCES.md` · `RECORD-CARDS.md` ⑥ · `_adlib/act3a-raw.md` · `_adlib/t5-readthrough-2026-07-17.md` · SCRIPT.md § Landmines.
**Result: 8 BLOCKERS · 31 CORRECTIONS · 7 UNVERIFIABLE.** Three blockers are new in v7.0; five are pre-existing and survived the v6.1 pass. **SCRIPT.md was not edited.**

> ⚠ **Un-recorded edits found.** The script does not match the `apply_phrasing.py` post-states in at least nine places (CH4-2 dash restored · CH4-3/4 "intelligence" dropped · CH5-2 Redesha reframed · CH5-3 "just like the last time" dropped · CH7-2 "UPA started most of it" cut · CH8-4 "went back and edited" → "cleaned up" · CLOSE-1 "I think" dropped). The header documents these as the owner's six one-by-one calls, so they are intentional — but the E-list is **not** a complete diff of today's work. Every finding below was checked against the ledger directly, not against the E-list.

---

# BLOCKERS

*Must fix before filming: factual error, misattribution, or a broken landmine.*

---

### B1 — Motyka does not "put it at" 70,000:20,000. Snyder prints it, and Motyka's own figure is higher. **[NEW in v7.0]**

**Current (CH6):**
> "Grzegorz Motyka, Poland's leading historian of the UPA, puts it at roughly seventy thousand dead Poles to twenty thousand dead Ukrainians."

**Governing rows:**
- `01-VERIFIED-RESEARCH.md` § T4 REBUILD item 6: "**70K:20K = Snyder p.204, based on Motyka's research** [RL p.269 fn: Motyka himself thinks Polish toll 'might be closer to 100,000']."
- § DEEPENING PASS #1: the raw cited text is **Snyder, *Reconstruction* p.204** — "about seventy thousand Poles to perhaps twenty thousand Ukrainians."
- `01-VERIFIED-RESEARCH.md` RULES 5 (attribution ≠ quote) and 6 (predicate precision).

**What's wrong — two things, and the second is worse than the first.**
1. **Misattribution of the print source.** The figure is Snyder's, derived from Motyka's research. "Motyka puts it at" claims a source showing Motyka stating that ratio. We do not have one. This is exactly the Rule-5 failure the ledger was built to catch.
2. **It may contradict Motyka's own position.** RL p.269 fn 1297 records that Motyka thinks the Polish toll "might be closer to 100,000." Putting 70,000 in his mouth as *his* count states a figure he is on record doubting — about a living, named historian, in a video he plausibly sees.

v6.1's "The count comes from Grzegorz Motyka…" was already loose; v7.0's "puts it at" hardens it into a direct attribution. The prior pass (row 26) conflated the two sources and did not catch it.

**Replacement (preserves the Polish-camp credential, which is doing real work — a Polish source conceding a ratio):**
> "But even with those killings counted, the numbers stay lopsided. Timothy Snyder, working from the Polish historian Grzegorz Motyka's research, puts the whole conflict at roughly seventy thousand dead Poles to twenty thousand dead Ukrainians."

⚠ If the card names Motyka, it must not imply 70,000 is his ceiling.

---

### B2 — "made it a crime" misstates what Law #2538-1 does. **[NEW in v7.0 — the E-list changed "an offence" → "a crime"]**

**Current (CH1):**
> "So in 2015, Ukraine wrote them into law as fighters for Ukrainian independence, and made it a crime to publicly disrespect them."

**Governing rows:** `01-VERIFIED-RESEARCH.md` § MODERN HOOK — "the **2015 decommunization Law #2538-1** legally codified OUN/UPA as 'fighters for independence' + **sanctioned** 'disrespect'"; § ACKNOWLEDGMENT PASS — "2015 memory laws codified OUN/UPA as 'fighters for independence' + **penalize** public 'disrespect'."

**What's wrong:** no ledger row says "crime." The statute declares public disrespect *unlawful* and refers liability out to existing legislation; it did not create a criminal offence. On a live statute in a high-heat video, the penalty class is precisely what a hostile commenter checks. The pre-swap wording ("an offence") was closer to the ledger than the new one.

**Replacement:**
> "So in 2015, Ukraine wrote them into law as fighters for Ukrainian independence, and made it illegal to publicly disrespect them."

---

### B3 — "around fifty-five thousand" is a number no source states, and it breaks a named landmine. **[NEW in CH1; carried in CH5]**

**Current — twice:**
> CH1: "By the end of that year, around fifty-five thousand Polish civilians were dead."
> CH5: "By the end of that year, across Volhynia, the toll had run to around fifty-five thousand Poles."

**Governing rows:**
- `01-VERIFIED-RESEARCH.md` § VERIFIED NUMBERS: Polish dead, Volhynia only, 1943 = **~50,000–60,000** (McBride p.633; Snyder; Motyka).
- `RECORD-CARDS.md` ⑥ **⚠ Landmine:** "50–60K = **Volhynia only** … **Lead with the precision, not a round number.**"
- SCRIPT.md header § Landmines: "numbers discipline (50–60K / 36,000+ named …)".

**What's wrong:** 55,000 is an invented midpoint. No source in the corpus states it. The record card's landmine forbids exactly this move by name. CH1's instance is new prose and has never been verified at all.

**Replacement (both places):**
> CH1: "By the end of that year, somewhere between fifty and sixty thousand Polish civilians were dead."
> CH5: "By the end of that year, across Volhynia, the toll had run to somewhere between fifty and sixty thousand Poles."

*(Secondary: CH1's "Polish civilians" is a qualifier the ledger's figure doesn't carry — the row reads "Polish dead." Defensible for Volhynia 1943, but CH5's plain "Poles" is the ledger's own predicate.)*

---

### B4 — "We know this because [the registry]" inverts the evidentiary relationship. **[carried from v6.1, never caught]**

**Current (CH5):**
> "…the toll had run to around fifty-five thousand Poles. **We know this because** a Polish husband-and-wife team, the Siemaszkos, spent decades building a registry of the dead. In their volumes they list about thirty-six thousand names…"

**Governing rows:** `01-VERIFIED-RESEARCH.md` § DEEPENING PASS #3 — "**Documented dead: 36,543–36,750** … **estimated total 50,000–60,000**." `RECORD-CARDS.md` ⑥ Must-land: "Across Volhynia the toll ran to 50–60 thousand Poles. **And we don't just estimate it —** a Polish husband-and-wife team spent decades building a registry…"

**What's wrong:** the registry documents ~36,500 by name; the 50–60K figure is an *estimate* built on top of it. "We know this because [the registry]" says the registry produced the higher number. It does not. The record card's own construction is the opposite: the registry is the **floor** under the estimate, not its source. This is the video's credibility exhibit; getting the logic backwards on it is the single easiest thing for an expert to attack.

**Replacement (fuses with B3):**
> "By the end of that year, across Volhynia, the toll had run to somewhere between fifty and sixty thousand Poles. And that estimate has a floor under it. A Polish husband-and-wife team, the Siemaszkos, spent decades building a registry of the dead. In their volumes they list about thirty-six thousand names, one by one."

---

### B5 — "often with the cause of death" is an unverified claim the owner himself flagged for verification-or-drop. **[carried]**

**Current (CH5):**
> "In their volumes they list about thirty-six thousand names, one by one, often with the cause of death."

**Governing row:** `_adlib/act3a-raw.md`, "Fact fixes for rebuild": *"'cause of death' isn't in the registry claim (names, listed one by one — **verify 'cause of death' or drop**)."*
`01-VERIFIED-RESEARCH.md` § DEEPENING PASS #3 grounds only the named-victim method ("Ustalono następujące nazwiska ofiar…"; "75 men and boys known by name who died in the flames").

**What's wrong:** the flag was raised by the creator's own read, never resolved, and the clause survived into v7.0. No ledger row supports it. Filming an unverified claim about a named source's methodology is a straight Rule-2 breach, and the fix is free.

**Replacement:** drop the clause.
> "In their volumes they list about thirty-six thousand names, one by one."

---

### B6 — "Genocide, in the strict sense, means intent from the top" is not the strict sense. **[carried]**

**Current (CH8):**
> "Genocide, in the strict sense, means intent from the top."

**Governing rows:** `01-VERIFIED-RESEARCH.md` § CONTESTED CLAIMS — "Poland (official): … genocide of Poles, **planned at OUN/UPA leadership level**"; "most scholars call it ethnic cleansing … **the planned-at-the-top question is exactly what the Klyachkivsky-order debate turns on**"; and "do NOT adjudicate the legal label on the channel's own authority."

**What's wrong:** the ledger grounds that *this dispute* turns on top-level planning. It does not ground — and the law does not support — the general proposition that genocide "in the strict sense" requires intent from the top. Under the Convention the element is intent to destroy the group as such; a plan or policy is evidentiary, not a legal ingredient. Saying "in the strict sense" makes it a definitional ruling in the channel's own voice, on the exact question the video refuses to adjudicate. This is the sentence a lawyer clips.

**Replacement (keeps the beat, restores the ledger's own framing):**
> "Genocide, in the strict sense, means intent to destroy the group — and the fight here is over whether that intent came from the top."

---

### B7 — "They don't dispute the numbers" is an absolutist claim the ledger contradicts. **[carried]**

**Current (CH6):**
> "Ukraine's official historians mostly dispute the framing — a mutual war, they say, not a one-sided cleansing. They don't dispute the numbers."

**Governing rows:**
- `01-VERIFIED-RESEARCH.md` § T4 REBUILD item 6 — the ledger's own recommended VO clause: "Ukraine's official school disputes the framing, **not mainly the arithmetic**." (Hrytsak "accepts ~3:1"; **Caruk/Kiczyj push equal-guilt symmetry** [Siemaszko pp.1060, 1076].)
- § STAGE C FINDING 2 — Viatrovych's **statistical** counter: "UPA report for Oct 1943 — Ukrainians lost 855 killed/burned, Poles 213." That is a numbers dispute.
- § LETTER TRACE — Katchanovski estimates ~35K UPA/SB victims in Volhynia against Siemaszko's 50–60K.

**What's wrong:** the ledger hedges with "not mainly"; the script drops the hedge and asserts a flat negative about a named group that its own research file documents disputing numbers. Rule 3 (unearned absolutist language).

**Replacement:**
> "Ukraine's official historians mostly dispute the framing — a mutual war, they say, not a one-sided cleansing. The arithmetic is not mainly what's in dispute."

---

### B8 — ON-SCREEN card would fabricate a Ukrainian source text. **[carried — card, not VO; flagged here because it is a landmine]**

**Current (CH7 ON-SCREEN block):**
> `"Nadzvychaine zariadzhennia," 06.04.1944, KAW M/II/30/2 — text fragment (Check-A UA).`

**Governing row:** `SOURCES.md` ACT 3 — **"Weapons ready — Death to Poles"** … "**English + transliteration only — NO Cyrillic (RL prints none).**"

**What's wrong:** RL reproduces no Cyrillic for this directive. A card built to the SCRIPT.md instruction ("text fragment," "Check-A UA") either shows a Ukrainian text that no source in the corpus prints, or sends a translator to check a text that doesn't exist. Either way it manufactures a document. `SOURCES.md` is the authority and the two files contradict.

**Replacement (card note):**
> `"Nadzvychaine zariadzhennia," 06.04.1944, KAW M/II/30/2 — English + transliteration ONLY, no Cyrillic (RL prints none; SOURCES.md ACT 3). Attribute to RL p.267 / fn.1267.`

The VO itself is clean — "one ends with the standing greeting" correctly under-claims against RL p.267's "these documents frequently ended with the greeting."

---

# CORRECTIONS

*Accurate but imprecise, or damaged by the restructure. Exact replacements given; each preserves meaning and register.*

## Cold open

**C1 — the promise has no antecedent for what the order was for.** "And if **an order** came down from the top, it would have left three things behind…" The last thing named is "the killing that report describes," three sentences back. This sentence is new, unverified, and carries the whole video's structure.
→ "And if **an order to do this** came down from the top, it would have left three things behind…"

## CH1

**C2 — "the movement" does not exist yet.** "The Germans arrested **the movement's leader** in 1941…" The OUN is not introduced until CH2; Bandera is not named until CH3. This is ex-CH8 material that the restructure moved *in front of* its own setup — the classic merge-at-distance break.
→ "The Germans arrested **their leader** in 1941 and held him for three years…" *(keeps CH3's "the movement's leader, Stepan Bandera" as the reveal it was written to be)*

**C3 — "until they were finally defeated" can bind to the Soviets.** "…the UPA kept fighting **them** out of the forests into the 1950s, until **they** were finally defeated." Two plurals, one pronoun each way. Created by the E-list CH1-1 split.
→ "…the UPA kept fighting them out of the forests into the 1950s, **until the Soviets finally crushed them**."

**C4 — "spend that" has no noun.** "So why **spend that**, in the middle of a war…"
→ "So why **spend that alliance**, in the middle of a war, on men who did what these men did in 1943?"

**C5 — "right now" dates the video.** "Ukraine is fighting for its existence **right now**." The evergreen guard is elsewhere honoured (no "this June," Zelensky on cards only); this is the one live datestamp in the VO and it costs nothing.
→ "Ukraine is fighting for its existence, and Poland is the ally on its land border."

**C6 — CH1's exit and CH2's opening say the same thing two sentences apart.** CH1 ends "…to a country that lived for **about three years**, and then disappeared." CH2 opens "…They proclaimed a state of their own. **That state lasted about three years.**" A restructure artifact — the cold open's old tail slid down to CH1 and now collides with CH2. Cut one. Cheapest: CH2 → "They proclaimed a state of their own. Its defeat left behind an idea, and that idea is where the massacre started."

**C7 — the 2012 tour was not entirely shut down.** "In 2012, threats **shut down a lecture tour** by the historian…" `03-FACT-CHECK-VERIFICATION.md` row 29 (web-verified 2026-07-19): invited for 6 lectures in 3 cities; the Lviv venue became unavailable, 3 of the 4 remaining were cancelled hours before, and **one was held** under police protection at the German embassy. v6.1's "His events were shut down" was accurate about the events; v7.0's compression makes the whole tour the object.
→ "In 2012, threats **cancelled most of a lecture tour** by the historian who wrote the leading biography of Bandera."

*(The sequencing guard survives: "the law put a name on something already there" + the spoken 2012/2015 dates carry it now that "three years before" is gone. Those five words are load-bearing — do not cut them, and the ON-SCREEN editor guard stays binding.)*

## CH2

**C8 — "It started with Dmytro Dontsov" has lost its referent, and briefly says something false.** The antecedent ("that idea") is four sentences and a topic change back; the nearest available "it" is "western Ukraine" in "for Poland to claim it." On the ear this reads as *the massacre* started with Dontsov. The condensation pass shortened "That idea started with…" → "It started with…" before the restructure moved the intervening territory block.
→ "**The idea** started with Dmytro Dontsov, the intellectual father of the Organization of Ukrainian Nationalists — the OUN."

**C9 — "other peoples" is vaguer than the source and mismatches the card.** "…the western lands would have to be cleared of **other peoples**." Himka p.389 (the verbatim the card will show): "sweep away literally to the last man **the Polish element** from the Western Ukrainian Lands and thus end Polish pretensions." The VO generalises where the card specifies, and the next sentence ("land someone else can claim") is the Polish claim-logic specifically.
→ "…the western lands would have to be cleared of **the Polish population**."

## CH3

**C10 — "they got their chance" binds to "other peoples."** The FIGURATION PASS swapped "the theory got its chance" → "they got their chance," which introduced a pronoun immediately after two plural non-actors ("other peoples," "someone else's people"). Worse if C9 is applied.
→ "Then, in the summer of 1941, **the movement** got its chance." *(avoids repeating "the nationalists," which arrives in the next sentence)*

**C11 — the Act quote drops the tail the ledger asked to keep.** VO ends at "…a new order in Europe and the world." `01-VERIFIED-RESEARCH.md` [P2]: "The 'Muscovite occupation' tail … sharpens the political logic — **keep it**." The quoted run is char-exact against Himka pp.208–209, so this is a research-decision reversal, not an error — and the following paragraph delivers the tail's substance ("the enemy of an independent Ukraine was Moscow"). Non-blocking either way, but the card guard is not optional: **"no silent cropping"** means the card shows the full passage including the Muscovite clause even if the VO stops early.

## CH4 *(the merged chapter — highest density of restructure damage)*

**C12 — "hurt them" binds to Ukrainians.** "…more to show **Ukrainians** whose side it was on than to actually hurt **them**." The condensation record only objected to "the German army"; "the Germans" was never the problem.
→ "…than to actually hurt **the Germans**."

**C13 — the connector swap asserts a causation the ledger routes differently.** "After Stalingrad, the Germans were clearly losing, **so** the nationalist leadership expected this war to end like the last one…" The ledger's driver is the WWI analogy ("read the future the way it remembered the past" — condensation item 4), with Stalingrad as timing (Snyder p.166: policemen "likely to leave their posts after Stalingrad"). The em-dash implied sequence; "so" asserts cause.
→ "After Stalingrad, the Germans were clearly losing**, and** the nationalist leadership expected this war to end like the last one, with the map redrawn at a conference."

**C14 — "Whoever took them in" dangles now that its setup is cut.** The RUNTIME MENU records that "the leadership wanted those men before anyone else did" was removed in Cut A. That clause was what made "whoever" mean anything; without it the sentence poses a competition the previous sentence already resolved ("joined the nationalists in the forest").
→ "**The nationalists got an army** — rifles, training, and everything 1942 had taught them."

**C15 — the Redesha quote is not char-exact.** VO: "It was explained to us that **this** would make it easier to bring about the coming Ukrainian revolution." McBride pp.652–53 (RAW-verified, genealogy Row 9): "It was explained to us [by OUN-UPA] that **by doing this it** would make it easier to bring about the coming 'Ukrainian revolution.'" The ledger licenses one natural-speech deviation only — "would never again **to** try" → "would never again try" — not this one. The card is char-exact by landmine, so the ear and the screen will disagree.
→ "It was explained to us that **by doing this, it** would make it easier to bring about the coming Ukrainian revolution."

**C16 — "everything 1942 had taught them" is the header's own OPEN QUESTION 5, still open.** Blind-spot audit ②: McBride pp.651–52 — "should not be assumed that participation in the Holocaust somehow caused participation in ethnic cleansing… the OUN-UPA either found or created killers irrespective of their participation in the Holocaust." The ledger's own honest swap:
→ "The nationalists got an army — rifles, training, and **experience**." *(owner's call; it is an accuracy question, not a style one)*

**C17 (Redesha, re-checked as instructed — the fix HELD).** "Others had no politics at all. One of those, a policeman named Redesha, explained after the war, under interrogation, what the new army did with men like him:" — accurate to McBride p.649 ("apolitical and had no connection to the nationalists before the war"); "One of those" binds cleanly to "Others"; the seasoned-killer implication is gone; provenance intact (name + "under interrogation" in VO, HDA SBU f.13 spr.1020 + McBride's "he bragged" caution on the card, per Row 9). **No change needed beyond C15.**

## CH5

**C18 — the chapter opens on a pronoun with no antecedent in reach.** "On July 11th, 1943, **they** hit around a hundred Polish villages at the same time." The preceding sentence is "The idea of removal had its army" — no plural actor. Across a chapter break, at the single most important factual beat in the video.
→ "On July 11th, 1943, **the UPA** hit around a hundred Polish villages at the same time."

**C19 — "the men" reads as the village men.** "The villagers were at mass. In Poryck, **the men** surrounded the church…"
→ "In Poryck, **the attackers** surrounded the church and fired machine guns through the doors during the eleven o'clock service."

**C20 — "Four thousand" states a round estimate as exact.** Ledger and record card both carry **~4,000** (McBride p.640; Snyder p.177).
→ "**Around four thousand** died that single day."

**C21 — "Survivors remembered them as…" generalises a plural testimony from one man.** The ledger's basis is a single Snyder p.204 recollection by **Waldemar Lotnik** — himself a Volhynian Pole who *took part in the 1944 mutual cleansings*, recalling a shared childhood, not the July 1943 attacks. The substance (neighbours took part) is separately grounded — McBride, "nationalists, but also policemen and average civilians"; Szawłowski, "thousands and thousands of ordinary peasants" (blind-spot ⑤) — but the testimonial framing is not. The owner's own T5 note says: *"We can just say the neighbors they had grown up with. We can leave the rest out."*
→ "And the killers were often not strangers. **They were the neighbours the villagers had grown up with.**" *(Lotnik stays on the card, where the ledger put him)*

## CH6

**C22 — "The violence they started" binds to "Poles and Ukrainians."** The preceding sentence is "Poles and Ukrainians killing each other in the chaos of occupation." The initiation claim is solid (Snyder p.203 "began the entire cycle"; blind-spot ④ SOLID) — the pronoun is not.
→ "**The violence the UPA started in 1943** came back the other way."

## CH7

**C23 — the Stelmashchuk quote is spliced without a mark.** VO: "the secret directive about the complete physical destruction of the Polish population." McBride p.642: "personally gave me the secret directive **from the OUN-B central provid** about the complete physical destruction of the Polish population **to be carried out in western Ukraine**." The quoted words are exact, but the run jumps an elision inside the quotation marks. The elision cuts *toward* caution (it drops the top-attribution and narrows scope), so it is not an overclaim — but the WARNINGS REGISTER item 4 says the VO "quotes McBride p.642 verbatim and stays there." Inaudible in VO; a problem the moment it is carded.
→ Either restore in full, or mark the elision on any card: "the secret directive […] about the complete physical destruction of the Polish population."

**C24 — "couldn't believe that order was real" overstates Motyka's predicate.** Motyka (raw-read 2026-07-17, ACQUISITION OUTCOMES): Stelmashchuk suspected **"przekręcenie w terenie"** — a distortion *in the field*, not from the centre; the letter was his appeal to verify. He doubted the order's provenance, not its existence.
→ "In June 1943, while the killing was underway, Stelmashchuk **doubted that order had really come from the top**. So he wrote to the leadership to check."

**C25 — the directive's *orality* is never spoken, and the whole verdict rests on it.** WARNINGS REGISTER item 5: "Any use of 'signed' for the letter = instant own-goal; **it reports an ORAL directive**." The VO correctly never calls it signed — but it also never says it was spoken, so the viewer is left to wonder why no paper exists. Katchanovski's English rendering: "gave me an **oral** and secret directive"; Motyka: "przekazał," relayed. One clause closes the video's biggest logical gap.
→ "In the letter, he repeats the same secret directive — **the one he says was given by word of mouth** — and names the men who'd carry it out."

**C26 — Viatrovych ran the security service's archive, not "the state archive."** "…the man who ran both **the state archive** and the state's memory institute." He directed the **SBU** archive (2008–2010) and UINP (2014–2019). The State Archival Service is a different institution, and this is a named living official's job title inside a beat accusing him of denial.
→ "…the man who ran both **the security service's archive** and the state's memory institute."

**C27 — "their founding document" is wrong and unreachable.** The Act of 30 June 1941 proclaimed a *state*; the OUN was founded in 1929. And the referent sits ~7 minutes back in CH3, where the script called it "this proclamation."
→ "And after the war, the ones who made it west carried **that 1941 proclamation** with them."

**C28 (self-burial firewall, re-checked as instructed — it HOLDS).** "This movement cleaned up its own record, and you can watch it happen" is grounded on RL fn.1378 ("kept the collaboration with the Germans a secret, portrayed itself as the enemy of 'Nazi imperialism'") + RL p.545 fn.2249 ("the fabricated text") + the 1991 museum display. It never implies the movement destroyed the kill-order — the two closing sentences do that work explicitly: "None of that tells you what happened to any one order. It tells you what kind of record we're reading." **Those two sentences are the firewall. If runtime pressure ever touches this beat, they are the last thing that may be cut.**

## CH8

**C29 — "eighty years later" contradicts the cold open's "eighty-three years later."** Both count from 1943; both are in the same video.
→ "…still can't agree what to call this massacre — **more than eighty years later**."

## CH9

**C30 — "that refusal" reaches past two intervening sentences** (the exhumation block) to "Ukraine won't."
→ "**And Ukraine's refusal** hands Russia a weapon."

**C31 — the split makes Russia's justification briefly sound like the narrator's.** "…uses it to argue that Ukraine is a Nazi state. **And that argument then justifies a war against it.**" With the dash gone, the new sentence opens with an unattributed assertion; "That is what 'denazification' means" repairs it a beat later, but the firewall-on-the-present is the one thing this video cannot afford to blur.
→ "And that argument is **how Russia justifies** the war against it. That is what 'denazification' means."

## CLOSE

**C32 — the thesis line ends on an orphan pronoun.** "…there's nothing wrong with looking to the past for heroes when you're in a fight now. **What's wrong is burying it.**" The nearest noun is "a fight." The E-list CLOSE-2 rewrite changed the object of the first sentence and left "it" pointing at nothing. The clarifying phrase ("what they did") arrives *after* the orphan, in the next sentence.
→ "What's wrong is **burying what they did**."

## Header hygiene (not VO, but the owner reads these at film)

**C33 — the RE-SPEAK LIST and RUNTIME MENU are stale.** The RE-SPEAK LIST still quotes lines that were cut or rewritten today: item 5 (the old "three years before it passed" RL joint), item 6 ("It isn't how they got there" — cut), item 7 ("Spontaneous is where it falls apart" — replaced), item 8 ("curated" — now "cleaned up"), and item 2 quotes two grain sentences that no longer appear. The RUNTIME MENU lists **Cut A as an available option** when the header says it is already applied, and its heading says **2,816 words** while its own table totals **2,714**. Reconcile before the read-aloud, or the read will chase lines that aren't in the script.

---

# CONFIRMED

*Checked against the ledger this pass and clean.*

**The three-part promise is delivered, in order.** Cold open: "attacks going off everywhere at once, reports coming back up the chain, and the order itself." → (1) coordination, CH5 (~100 villages, same day, McBride p.640) and CH6 ("whole waves of them killed in attacks on the same days"); (2) the reports, CH7 ¶1 (Klymchak reporting up the chain); (3) the order, CH7 ¶2 ("What no one can actually produce is an order to kill the Poles with his signature on it"). Two positives, crux negative, landing last. ✓ **If any of the three beats is cut for runtime, the cold-open sentence must change with it.**

**Quotes, char-exact against their ledger rows:** Klymchak, "I liquidated all Poles from young to old. I burned all the buildings and took the possessions and livestock for the needs of the battalion" (McBride p.648) ✓ · the Act of 30 June 1941, "collaborate closely with National Socialist Greater Germany, which under the leadership of Adolf Hitler is creating a new order in Europe and the world" (Himka pp.208–209) ✓ · Snyder, "a resurrected Poland" (p.166) ✓ · "Weapons ready. Death to Poles" (RL p.267 / fn.1267 → *Nadzvychaine zariadzhennia*, 06.04.1944) ✓ · Redesha's first sentence, "We burned Polish settlements so there would be no trace of their existence, and so that the Poles would never again try to lay claim to Ukraine" ✓ (natural-speech deviation from the printed "never again **to** try" is licensed by the round-trip note; card stays char-exact). See C15 and C23 for the two that are not clean.

**Quote framings, all correct:** the Klymchak report is "a report to his superiors" in VO, carded as "preserved in a Soviet case file, reproduced by historians" — never "signed archival document" ✓ (Row 2) · the Stelmashchuk confession is duress-framed in VO ("under interrogation," "a confession under duress, in the interrogators' own wording") ✓ (Row 1) · the letter is **never** called signed; the VO says "a transcription, from an archive nobody can check," and the "signed" characterization is correctly attributed to others ("Some of them call it Klym Savur's own signed order") ✓ (Rows 5, 5c — this is the precise form the header calls deliberate, and it is intact).

**The central adjudication holds.** "What no one can actually produce is an order to kill the Poles with his signature on it" — Row 5c settlement (every "signed" characterization traces to HDA SBU spr.11315 t.1 ch.2 ark.16, unreachable) ✓ un-catchable as phrased.

**Numbers:** ~140,000 Vistula (140,575, ENRS, 28 Apr 1947) ✓ · ~5,000 deserters, spring 1943 (RL p.547; 19 Mar–14 Apr) ✓ · ~100 villages, 11 July (McBride p.640, "over 100"; conservative) ✓ · 36,000+ named (36,543–36,750; card guard "never 33,454") ✓ · Bandera three years (Sep 1941–Sep 1944) ✓ · three weeks decree→revocation (26 May → 19 Jun 2026 = 24 days, rounds down) ✓ · eighty-three years (Aug 1943 → May 2026) ✓ · en-route killings before the assembly points (Siemaszko p.1045) ✓.

**Other v7.0 changes, checked and clean:** "Berlin wanted the land itself — settled by Germans and worked for Germany" = colony/Lebensraum + Ukrainians as manpower (Plokhy pp.287, 297) ✓, and it kills a show-don't-tell label without losing the claim · the police-infiltration purposes now rest on training + weapons only (Himka pp.275/279); "intelligence" correctly dropped ✓ · "quietly" correctly dropped ✓ · anti-German actions hedged exactly as Piotrowski frames them ("more to show Ukrainians whose side it was on") ✓ (blind-spot ③) · the SB-purge sentence is verbatim the corrected v6.1 form ("Ukrainians it considered unreliable — thousands of them, including men who refused to kill Poles") ✓ · "Even Motyka accepts that no signed order ever turned up… what convinced him was the coordination" ✓ (substance via McBride p.638 + Row 5c — ⚠ never quote Motyka on this; the two Polish quotes were caught as fabrications in the 2026-06-30 HYPE AUDIT) · Klyachkivsky's signed logistics orders (village defence No. 8, tribunals 15 May, land reform 15 Aug) ✓ · the 1963 archival copy and the Gorshkov notations "dated April 1945, two months after the interrogation" ✓ (Row 5b; 28 Feb → 24 Apr) · Stetsko "signed by Stetsko," not "own hand" ✓ (Row 10 correction held) · "two Polish villages" ✓ (Row 12, exact) · the archive argument appears **once**, in CH9, in the corrected narrow form ✓.

**Connector swaps.** All 18 sites checked. Sixteen are neutral (`. And` / `, and` / `. But` / `. The`). Two introduced a causal assertion: CH7 #13 (`So he wrote to the leadership to check`) is **grounded** — Motyka explicitly frames the letter as an appeal to verify ✓; CH4 #6 is **not** — see C13. Notably, the two places where "because" was offered (#10 neighbours, #16 the file) both took the neutral option, which was the right call: "because" would have asserted an evidentiary link neither source makes.

**Neutrality double-move survives.** Uneven on the history: UPA initiation stated (Snyder p.203), the 70K:20K asymmetry given, Poland's own Sejm concession used to carry the reciprocity, Viatrovych's symmetry thesis presented as the Ukrainian camp's position rather than fact. Firewall on the present: Poland keeps arming Ukraine; Russia's instrumentalization named without endorsing Russia; the close ends on a question with no ruling on genocide vs. ethnic cleansing in the channel's own voice ✓. The 1997/2023 reconciliation gestures stay LATE (CH8), so the hard sequencing guard survives the restructure ✓.

**Pre-judging check (corpus 62-03).** CH1's "that same army set out to clear Volhynia… of the Poles living there" asserts campaign intent before the crux — but it is licensed: McBride p.638, "regardless of debates over dates and provenance of the order to kill, the intent on the part of the OUN-UPA leadership is clear," and p.633, "highly coordinated ethnic cleansing campaign." Campaign intent (asserted early) and an examinable signed initiating order (unresolved at the crux) are distinct propositions, and CH7 keeps them distinct ✓. No other beat pre-judges.

---

# UNVERIFIABLE

*Needs a source we don't have. Stated plainly rather than guessed.*

**U1 — "Almost none of it ever translated into English" (cold open).** No ledger row supports this. The nearest is a *whitespace* finding about YouTube coverage ("Nobody brings the actual archival documents"), which is a different claim. And the project's own corpus cuts against it: McBride, Snyder, Himka and Katchanovski all render these documents in English — Katchanovski pp.15–16 prints the Stelmashchuk letter in English. This is a series-identity line ("Untranslated Evidence") and may be a claim the owner wants to make on his own authority; it cannot be verified from the ledger. A defensible narrowing: "Almost none of it has ever been published in English outside a handful of academic articles."

**U2 — "two of his brothers died in Auschwitz" (CH1).** The ledger and the CH3 card both say only "**his brothers** died at Auschwitz" (RL pp.381–397). The count of two is nowhere pinned in this project's files. Either pin it in RL before film or drop the number ("his brothers died in Auschwitz").

**U3 — Poryck: "Around two hundred people died in that one church" and "the eleven o'clock service" (CH5).** The ledger carries "~200 Poryck" against **Siemaszko p.896 with Check-A PL still pending** and does not settle whether the figure is for the church or for the locality. The 11:00 mass detail appears in no project file at all — `ADLIB-BRIEF.md` says only "churches surrounded during Sunday mass." Until the Check-A pass runs, the safe form is "Around two hundred people died at Poryck that morning" and the service time comes out. **Non-blocking only if the Check-A lands before film.**

**U4 — "for the army it planned to build" (CH4).** Himka pp.275/279 ground the March 1942 infiltration order's *content* (one OUN-B member per police unit; training; weapons). No row grounds the stated *purpose* of building a future army in March 1942 — and Snyder p.166 dates the decision to begin partisan actions to **February 1943**, eleven months later. Pre-existing (present in v6.1; the creator read it aloud at T5), so not a v7.0 regression, but the teleology is the script's, not a source's. Safe form: "…to get trained and to collect weapons."

**U5 — Motyka doubt-arc print pages (CH7).** The header's own Check-A item: the Motyka 2011 PDF is a Scribd rip whose pagination does not match the print edition. "przekręcenie w terenie" and "he ultimately carried the order out" are raw-read and real; the page pins are not. Blocks the card, not the VO.

**U6 — Kolodzinskyi verbatim page (CH2).** Round-trip reconciled the cite to **Himka p.389 print** (the earlier "pp.790–91" was an e-book location). The *Ukraina Moderna* 20 (2013) facsimile is acquired but the exact card page is still an open Check-A pick.

**U7 — Motyka's own higher Polish-toll estimate (bearing on B1).** RL p.269 fn 1297 records Motyka at "closer to 100,000," but the project has never pinned his own published figure directly. If B1's replacement is adopted, this stops mattering for the VO — but no card may present 70,000 as Motyka's number.

---

## Standing items carried forward (not findings)

Check-A translation-fidelity passes (Order No. 11 UA · Poryck/Siemaszko PL · Siemaszko p.1045 PL · letter transcription UA · Kolodzinskyi verbatim) · week-of-film re-verification of all 2026 facts (decree date, unit name, revocation date and actor, EP amendment, exhumation resumption) · decree № stays off screen, unverified · the Gemini adversarial pass (Step 7.9) still never ran.
