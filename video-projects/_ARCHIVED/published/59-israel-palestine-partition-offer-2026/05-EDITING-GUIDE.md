# Editing Guide — #59 Israel/Palestine: The Partition Offer

**Source:** `rought cut.srt` vs `SCRIPT.md` (🔒 locked 2026-06-24) + `ON-SCREEN-CARDS.md` (card manifest)
**Region covered:** Full video, 11 min 17 sec (VO-only rough cut)
**Generated:** 2026-06-25

> **Experiment note (creator):** This cut went "more with gut" — deliberately *less direct quoting*, with most primary sources carried *on screen* instead of read aloud. That choice shows up cleanly in the diff: mid-body scholar attributions (Karsh, Kattan, Reedman by name) were stripped from the VO, while the climactic Morris-vs-Khalidi duel in Act 6 was kept spoken. The editorial consequence — and the whole bet of this video — is that **the on-screen cards now carry the evidentiary weight the voice used to.** If a card is late, missing, or unreadable, the claim it backs goes naked. So card timing matters more on this cut than on any previous one.

> ⚠️ **TRANSCRIPTION CAVEAT (read before trusting any word-level flag):** The rough-cut SRT is **auto-generated from low-quality phone audio**, so word-level mismatches are suspect by default — most are ASR errors, not misspeaks.
>
> ✅ **RESOLVED via clean audio (2026-06-25):** the creator's separate clean voice recording (`Recording (14).m4a`) was transcribed with Whisper → `_research/CLEAN-AUDIO-TRANSCRIPT-2026-06-25.txt`. This is the ground truth of what he actually said. The ear-checks are now settled:
> - Act 3 "economically **protected**" → he actually said **"compromised"** (correct — weakened/dependent). Phone-SRT error. **No fix.**
> - Act 1 "overlooks how **fair** the deal was" → **CONFIRMED REAL** (he said "fair," not "unfair"). Genuine ambiguity — see Editing Decisions A.
> - Reedman → **CONFIRMED REAL**: he literally said *"an independent economic expert, a certain arrangement"* — a verbal placeholder, not an ASR garble. Needs naming or dropping.
> - Cleared as ASR-only (he said it right): "talking point" (not "token"), "argued **that** the UN," "Central Political **pact**" (not "Act"); "Bursheba"/"Khaledi" are caption-only spellings.
> - Cold open: "UN Resolution **101**" was an instant flub, immediately re-taken as "181" — verify the final picture uses the 181 take.
>
> The clean transcript also exposes the **retake hot-spots** (where he restarted lines) — see Editing Decisions A. Structural recommendations (cut / move / VO / card timing / pacing / loudness) never depended on the transcription and stand regardless.

---

## TL;DR — top 7 actions

1. **Audio is the headline decision: swap in the clean recorder audio you already have.** The phone track is **−27.0 LUFS** (13 dB under target) and peaking at **+0.1 dBTP** (clipping). You don't need to re-perform — `Recording (14).m4a` is the same session at good quality. Conform it to the cut (dual-system replacement, take-by-take) and normalize to **−14 LUFS / −1 dBTP** with a limiter (not a flat boost). This fixes loudness *and* the words (the clean read says "compromised," not the phone-SRT's "protected"). See Editing Decisions A.
2. **Two genuine fixes — confirmed against the clean audio** (everything else cleared as ASR noise):
   - **Reedman placeholder (Act 3, ~01:04:25):** he really said *"an independent economic expert, **a certain arrangement**, to assess…"* — no name on tape. Name him **John Reedman** (VO drop-in) or drop the phrase and let the card carry it.
   - **Act 1 "overlooks how fair the deal was" (~01:02:15):** he really said "fair," and it's ambiguous to the ear (sounds like "doesn't appreciate how fair it was," inverting Act 2). Clarify via VO drop-in — e.g. *"overlooks how **unfair** the deal was"* or *"overlooks **whether** the deal was fair at all."*
   - (Act 3 "protected" is a **non-issue** — he said "**compromised**," which is correct.)
3. **Everything else at the word level was ASR noise — no action.** Clean transcript confirms: "talking point," "argued **that** the UN," "central political **pact**"; Bursheba/Khaledi are caption-only spellings. The cold-open "Resolution 101" flub was re-taken as 181 — just confirm the picture uses the 181 take.
4. **Card timing is load-bearing this cut.** Every dropped attribution (Morris allocation, Karsh-Negev, Kattan-84%, demographics, Reedman, legal verdict, Liberia, Philippines, FRUS memo, Balfour, Khalidi) must land *as a card* on the matching beat — timecode map below. This is the experiment's make-or-break.
5. **Optional cut:** the Act 4→Act 5 seam restates "it was only a recommendation / nobody to enforce." A ~10–15s tighten there is the one content trim worth considering. Otherwise pacing is fine.
6. **`/fix` captions are deferred** (per creator) — and a clean-VO re-record would make `/fix` mostly unnecessary anyway, since you'd re-transcribe clean audio.
7. **Pacing is on target** (11:17 vs 10.5–11 min). No structural trims required.

---

## Segment 1 — COLD OPEN (01:00:00 → 01:00:58)

**SRT lines 1–25 — what's on tape:**
> *"This is UN resolution 181, the 1947 plan to split Palestine into two states, one Jewish and one Arab. It was the first time the international community voted on the region's future. To one side it recognized the Jewish people's right to a sovereign state. To the other, foreign powers carved up a country that was already owned by the Palestinians. Almost nobody arguing about it has actually read the relevant documents. When you do, the first surprise isn't about borders. Before the final vote, the Arab states argued to the UN had no legal authority under its own charter to partition a country against the will of its majority. They motioned the world court to rule on the legal validity of the plan. That motion was defeated by a single vote, 21 to 20. The partition resolution passed five days later, leaving its legal foundation permanently unsettled."*

**vs script said:**
> *"...the day the Jewish people's right to a country was finally recognized. To the other, it's the day their homeland was signed away over their heads. And almost nobody arguing about it has read it. **So I read the documents.** And the first thing that jumps out..."*

**Verdict:** KEEP (with two flagged decisions)

**Issues:**
| # | Timestamp | Issue | Fix |
|---|---|---|---|
| 1 | ~01:00:34 | *"the Arab states argued to the UN had no legal authority"* — missing word ("argued **that** the UN had…"); audible stumble on line 2 of the video | MEDIUM pickup — hook real estate; re-record the sentence clean |
| 2 | ~01:00:28 | Script's deliberate first-person beat **"So I read the documents"** was dropped (it was a lock-day restoration and sets up the close). Tape says "When you do" instead | DECIDE — cheap one-line pickup restores the cold-open identity + Act-CLOSE callback. Optional if the gut version is intended |
| 3 | ~01:00:18 | *"a country that was already owned by the Palestinians"* — flat "owned" is loaded, but it's inside the "to the other side" framing, so acceptable as narrative voice | KEEP |

**On-screen cards for segment:**
- 01:00:00 **CHYRON** "UN General Assembly Resolution 181 — 29 November 1947" over the document push-in (✅ CLEAN, card manifest).
- ~01:00:48 **CHYRON** "Referral to World Court — defeated by one vote, 21–20, 24 Nov 1947" on the "defeated by a single vote, 21 to 20" beat (✅ CLEAN; Kattan pp.150–151 + Cohen p.289). This is the cold-open's evidentiary anchor — land it precisely on the number.
- SHOW: Res 181 text → partition map dissolve.

**B-roll for segment:** UN GA voting / Lake Success 1947 — see B-roll research §1.

**Music note:** weighty/low bed; let it drop out under "That motion was defeated by a single vote" for emphasis.

---

## Segment 2 — ACT 1: THE TWO STORIES (01:00:59 → 01:02:14)

**SRT lines 26–63 — what's on tape:**
> *"This video is a look at the documents themselves, matching the popular narratives against the text and the facts historians actually agree on. By 1947, Britain had ruled Palestine for 30 years under a League of Nations mandate. Decades of escalating conflict… The standard Israeli narrative… The Jewish leadership accepted. The Arab leadership refused… One side chose compromise. The Arab side chose war… The standard Arab narrative is different… a committee of foreign governments handed more than half of it to a minority population… they refused to legitimize the partition of their own country. Neither narrative fully captures what was written in the plan itself. **The Israeli version overlooks how fair the deal was. The Arab version overlooks if the plan could even be enforced.**"*

**vs script said:**
> *"The Israeli version **fails on whether the Arabs got a fair deal**; the Arab version, on whether anything was really imposed from the outside."*

**Verdict:** DECIDE — one thesis-hinge line at risk

**Issues:**
| # | Timestamp | Issue | Fix |
|---|---|---|---|
| 1 | ~01:02:15 | **"The Israeli version overlooks how fair the deal was."** Intended meaning (per script + all of Act 2): the Israeli narrative is *wrong* that it was fair. But "overlooks how fair the deal was" reads to the ear as "doesn't appreciate how fair it was" — the **opposite**. Parallel structure with the next line saves it only if the viewer parses "overlooks [the question of] how fair" | **HIGH/DECIDE** — re-record "...overlooks how **un**fair the deal was" (cleanest), OR pin an on-screen card "Was it fair? → Act 2" that frames it as the open question. Don't ship it ambiguous |
| 2 | ~01:01:53 | Script's "mostly **European** Jewish minority — outsiders" → tape drops "European." Minor | KEEP |
| 3 | — | Added "under a League of Nations mandate" — accurate, good tightening | KEEP |

**On-screen cards for segment:** none required (narrative framing). Consider a simple two-column "Israeli story / Arab story" lower-third montage.

**B-roll for segment:** Mandate-era Palestine + 1948 armies — see B-roll research §2, §3.

---

## Segment 3 — ACT 2: WAS IT FAIR? (01:02:15 → 01:03:56)

**SRT lines 64–110 — what's on tape:**
> *"The core Arab objection was straightforward. They refused to accept being turned overnight into a minority, into a Jewish state. The numbers that are in the plan are uncontested. The UN resolution awarded 55% of the land to the Jewish state at a time when Jews made up roughly one third of the population and legally owned about 7% of the land. Defenders of the resolution argue these percentages are misleading. Most of that 55% was the Negev, a vast arid desert in the south… But the documents and access show that even with the southern desert included, the Jewish state was allocated 84% of the country's existing farmland. And even more importantly, the Negev was not empty. Britain's 1946 census counted over 100,000 Bedouin Arabs in the Bursheba district compared to just 1,000 Jews… roughly 500,000 Jews and 410,000 Arabs… those calculations excluded most of the Bedouin… Include them and that Jewish majority disappears… The fundamental issue wasn't the amount of land, but rather who would end up governing whom."*

**vs script said:** (Act 2 attributes the objection to **Benny Morris** by name, and the "misleading percentages" defense to **Efraim Karsh** by name.)

**Verdict:** KEEP VO — but the dropped attributions MUST become cards (this is the experiment's load-bearing moment)

**Issues:**
| # | Timestamp | Issue | Fix |
|---|---|---|---|
| 1 | ~01:02:15 | Benny Morris attribution **dropped** from VO ("The core Arab objection was straightforward" instead of "Benny Morris — an Israeli historian — sums up…"). Rhetorical cost: an *Israeli* historian voicing the *Arab* steelman is the strongest version | Restore via **card** on the 55%/7% beat (see cards). Intentional per experiment — don't re-record |
| 2 | ~01:02:45 | Efraim Karsh attribution **dropped** ("Defenders of the resolution argue") | Restore via Karsh-Negev **card** (see cards) |
| 3 | ~01:03:03 (cut) | **RE-DIAGNOSED 2026-07-03 — NOT a filler stumble.** The cut caption reads *"the **documents and access** show… allocated 84% of the country's existing farmland"* (the uncut transcript heard the same audio as *"the document's **annexes** show"*). Either way it tells the viewer *the documents show 84%* — a **false attribution**: the 84% is Kattan citing **Khan's UN speech (A/PV.126)** citing an untitled **UK-delegation paper**, NOT anything the plan's documents/annexes state. (Also "documents and access" is garbled, and the VO contradicts its own "Kattan" card.) | **HIGH — pickup re-record** (replacement line + primary card below) |
| 4 | ~01:03:20 | Caption: **"Bursheba"** → Beersheba | `/fix` |

**On-screen cards for segment (high density — this is the evidence act):**
- ~01:02:30 **CARD** Morris allocation: *"The partition resolution had earmarked some 55 per cent of Palestine for the Jewish State… [Jews] owned some seven per cent."* — label **"Benny Morris — Israeli historian"** (Morris, *Birth… Revisited* 2004, p.141). Land it on "55%… owned about 7%."
- ~01:02:50 **CARD** Karsh-Negev: *"that vast and largely unpopulated desert south of the Gaza–Beersheba line…"* — label **"Efraim Karsh — defends the resolution"** (*Palestine Betrayed*, Yale 2010, p.103). Land on "Most of that 55% was the Negev."
- ~01:03:08 **CARD — REPLACES the old "84% farmland / annexes" card (corrected 2026-07-03; see Issue #3).** Old VO line needs a pickup.
  - **Replacement pickup VO:** *"But the desert was only part of what the Jewish state got. The UN's own committee found it was handed 'the best agricultural lands in Palestine' — the coastal plain, the valleys, and practically the whole of the citrus belt — leaving the Arab state 'mountainous regions, largely uncultivable.'"* (flows into "And even more importantly, the Negev was not empty.")
  - **Replacement CARD (primary UN doc):** *"the proposed Jewish State is allotted… the best agricultural lands in Palestine, leaving to the Arab State certain mountainous regions, largely uncultivable."* — label **"UN Ad Hoc Committee — Report of Sub-Committee 2, A/AC.14/32 (11 Nov 1947)"** (`2ece8af6`). ⚠️ eyeball the verbatim against a clean A/AC.14/32 copy before render (NLM OCR is mangled).
  - **Optional citrus card:** *"The Jews will have the more economically developed part of the country embracing practically the whole of the citrus-producing area"* — UNSCOP Report 1947, quoted by Sub-Cttee 2 (clean text via Smith `243736dc`). Say "the citrus *area*," never "most of the citrus" — production was ~equally split.
  - **Optional hard-number card (Kattan's OWN voice, if you want a figure):** *"Even in Safad, which was awarded to the Jewish state… the Arabs owned 68 per cent of the land whereas Jews owned a mere 18 per cent."* — label "Victor Kattan — international-law historian" (Kattan **p.157**, `94a0ed73`).
  - *Why the swap:* the primary UN quote rebuts Karsh's "empty desert" directly, comes from the UN's own body (not a partisan speech), sits on the evidentiary floor, and removes the VO↔card contradiction. Old Kattan-84% card retired.
- ~01:03:18 **CARD** Beersheba census (**primary**): *"In its southern section (the Beersheba area), there are 1,020 Jews as against an Arab population of 103,820."* — **A/AC.14/32, Sub-Cttee 2, p.41 ¶65** (in-project scan). Label as Sub-Cttee 2's *contested* count, underlying census = *A Survey of Palestine* 1946.
- ~01:03:30 **CARD** demographics: "498,000 Jews / 407,000 Arabs (excl. ~90,000 Bedouin)" — Cohen p.289.
- SHOW: 55/45 map + "~7% Jewish-owned" overlay; 1946 census table + Negev shaded.

**Music note:** pull energy back for the "who would end up governing whom" button — it's the act's thesis line.

---

## Segment 4 — ACT 3: THE STATE THAT COULDN'T STAND (01:03:56 → 01:05:01)

**SRT lines 111–143 — what's on tape:**
> *"The second structural flaw was more practical. The proposed map split the country into six different interwoven enclaves, three for the Jewish state and three for the Arab state. Because Palestine had always functioned as a single economic unit, the UN tried to fix this fragmentation by forcing both states into a mandatory shared customs union. During the drafting phase, the UN committee appointed an independent economic expert, **a certain arrangement**, to assess whether these fractured territories could survive independently. His report was definitive. The Arab state would definitely not be viable without a customs union. Because the Jewish state was allocated to major commercial ports and the industrialized coastal plain, **the Arab state was economically protected from day one.** It could only function if the neighbor it was partitioning from agreed to support its economy…"*

**vs script said:**
> *"...an independent economic expert, P.C. Reedman… His verdict: the Arab state 'would definitely not be viable without a customs union.' The Jewish state had the ports and the developed land — it could survive alone. **The Arab state couldn't**…"*

**Verdict:** FIX — two HIGH-priority audio errors in one act

**Issues:**
| # | Timestamp | Issue | Fix |
|---|---|---|---|
| 1 | ~01:04:46 | ~~"economically protected"~~ — **RESOLVED via clean audio: he said "economically compromised," which is correct.** Phone-SRT error only | **NO ACTION** (caption-only if keeping phone audio) |
| 2 | ~01:04:25 | **"a certain arrangement"** — CONFIRMED on clean audio: the expert's name is genuinely missing (verbal placeholder). Correct name = **John Reedman** (lock-day correction from "P.C. Reedman") | **REAL FIX** — VO drop-in naming "John Reedman," OR drop the phrase ("an independent economic expert") and let the card carry the name. Do not ship "a certain arrangement" |
| 3 | — | "would definitely not be viable without a customs union" — verbatim survives in VO, good | KEEP |

**On-screen cards for segment:**
- ~01:04:10 **CARD** Res 181 economic-union clause (customs union / Joint Economic Board) — Part I §D (✅ CLEAN).
- ~01:04:35 **CARD** Reedman verdict: *"would definitely not be viable without a customs union."* — attribute **"John Reedman — UNSCOP economic expert"** (Ben-Dror p.176; primary backstop UNSCOP Report A/364). **This card both carries the quote AND fixes the garbled name** — make it land on "His report was definitive."
- SHOW: trace the six blocks + the two "kissing points"; highlight ports (Haifa/Jaffa) on the Jewish side.

---

## Segment 5 — ACT 4: IT WASN'T LAW (01:05:01 → 01:06:30)

**SRT lines 144–186 — what's on tape:**
> *"The biggest pro-Palestinian **token point** about this plan is that it was imposed by the UN. But imposition requires binding legal authority and resolution 181 possessed none… The General Assembly recommends the partition plan to the mandatory power, Britain, and requests the Security Council to implement it. Under the UN Charter, the General Assembly holds no legislative power… the UN's own legal department formally concluded at the time that the text had no obligatory character whatsoever. **It was a blueprint, not a law.** … the United States exerted intense diplomatic and economic pressure… Liberia, heavily reliant on American rubber exports, was privately warned… The Philippines, who initially denounced the partition plan… changed their vote to yes after a pseudo-threatening telegram… The pressure worked. Resolution 181 passed 33 to 13."*

**Verdict:** KEEP — strong act, two small caption/word notes

**Issues:**
| # | Timestamp | Issue | Fix |
|---|---|---|---|
| 1 | ~01:05:01 | "pro-Palestinian **token point**" — likely "talking point" mis-said/mis-transcribed; also introduces "pro-Palestinian" labeling the script deliberately avoids (it uses "the Arab side") | LOW — `/fix` caption to "talking point"; re-record only if pickups happening (consider "The loudest Arab talking point" to keep register) |
| 2 | ~01:06:18 | Script's vivid detail "two **US Supreme Court justices**" (Murphy & Frankfurter) dropped to "US officials" | Restore via Philippines **card** (names the justices) |
| 3 | — | **"It was a blueprint, not a law."** — ad-lib better than script | **KEEP** |
| 4 | ~01:06:28 | "passed 33 to 13" — concrete vote count added, accurate | **KEEP** |

**On-screen cards for segment:**
- ~01:05:17 **CARD** Res 181 operative words: *"Recommends to the United Kingdom… the adoption and implementation… of the Plan of Partition"* / *"Requests that the Security Council take the necessary measures."* — **highlight "Recommends" / "Requests"** (✅ CLEAN). This is the act's spine — hold it long.
- ~01:05:48 **CARD** legal verdict: *"no obligatory character whatsoever."* — attribute **"the UN Secretariat / UN's own legal staff"** (Kattan p.155). ⛔ NOT Kelsen.
- ~01:06:00 **CARD** Liberia: *"high pressure electioneering…"* — "Liberia's protest to the State Dept, Dec 1947" (Cohen p.297 → NARA 501.BB Pal/12-947).
- ~01:06:18 **CARD** Philippines: justices Murphy & Frankfurter telegram verbatim (Cohen p.297) — names the justices the VO dropped.
- (World-Court 21–20 chyron may re-flash here as the callback.)

---

## Segment 6 — ACT 5: NOBODY COULD MAKE IT HAPPEN (01:06:30 → 01:08:09)

**SRT lines 187–234 — what's on tape:**
> *"…remember that the resolution was just a recommendation. A recommendation that could still be enforced if a major power provides the military power to back it up. But implementing partition against the will of the local majority required an army, and nobody was willing to send one… the council took no action. The small five-member commission dispatched to Jerusalem… warned the UN that without an international force, the country would descend into open warfare the moment British forces withdrew. Britain was finally broken and military exhausted after World War II and refused to spend British lives… 11 days before the UN vote, the US State Department drafted a classified memorandum acknowledging that having championed partition, America was morally obliged to help… Yet its final recommendation was to oppose the use of American troops. Washington calculated that military intervention would alienate the oil-producing Arab world and open a strategic door for Soviet intervention…"*

**Verdict:** KEEP — clean act, matches script intent

**Issues:**
| # | Timestamp | Issue | Fix |
|---|---|---|---|
| 1 | — | "five-member commission" — accurate detail added | KEEP |
| 2 | ~01:07:44 | VO paraphrases the FRUS memo ("oppose the use of American troops") — the verbatim "discourage the use of force" lives on the card | KEEP; card carries verbatim |

**On-screen cards for segment:**
- ~01:07:00 **CARD** Commission collapse warning: *"The Commission envisages the possibility of collapse of security and administrative services…"* — **S/663, 29 Jan 1948** (primary).
- ~01:07:50 **CARD** FRUS memo (**PRIMARY**): *"The US should seek to discourage the use of force for implementation…"* — **FRUS 1947 vol. V, Doc 872, 18 Nov 1947**. The clean primary of the act — hold it on "oppose the use of American troops."

**B-roll for segment:** post-WWII Britain, troop withdrawal, US State Dept — see B-roll research §6, §7.

---

## Segment 7 — ACT 6: THE DECISION ON TRIAL (01:08:09 → 01:10:24)

**SRT lines 235–299 — what's on tape:**
> *"This leaves the **Central Political Act**, the Arab leadership's total rejection of the plan. Was that rejection a catastrophic strategic blunder or was accepting the plan completely impossible? Historian Benny Morris frames it as an historic error… By rejecting compromise, gambling on a military solution… and losing, they walked away with nothing. **Triggering the massive Palestinian refugee crisis.** Historian Rashid Khaledi reads the document through a different lens… Accepting partition meant volunteering to become a minority… To him, the partition plan was the culmination of that erasure. This view deserved some pushback. The resolution itself did not erase the Arab population. It explicitly guaranteed an independent Arab state on nearly half the land, and it mandated… equal non-discriminatory civil and political rights… What the plan did demand the Arab majority to give up was not their rights, but their claim to the entire country. The Arab leadership supported a different resolution. The night of the vote, a competing proposal drafted by India, Iran, and Yugoslavia… A single federal democratic state… once it passed, the federal alternative was discarded…"*

**Verdict:** KEEP — the dueling-historians structure survives intact (the right call: strip mid-body names, keep the climax spoken)

**Issues:**
| # | Timestamp | Issue | Fix |
|---|---|---|---|
| 1 | ~01:08:09 | "the **Central Political Act**" — garbled phrasing (script: "the thing people actually argue about") | LOW — `/fix` caption; re-record optional |
| 2 | ~01:08:40 | **"Triggering the massive Palestinian refugee crisis"** — ad-libbed causal claim. It's inside Morris's framing, but delivered flat it can read as the channel's own verdict on the Nakba's cause (sensitive) | **MEDIUM/DECIDE** — keep a persistent "Benny Morris's reading" label on screen through this beat so it's clearly *his* causal chain, not the referee's; or trim the sentence |
| 3 | lines 253/263 | Caption: **"Khaledi"** → Khalidi | `/fix` |
| 4 | ~01:09:57 (cut) | **Re-checked against the CUT 2026-07-03 — KEEP.** The cut delivers *"drafted by India, Iran, and Yugoslavia"* — the actual authors of the UNSCOP **minority federal plan** — so the credit is accurate and the procedural beat (partition called first → federal alternative sidelined) matches C17. (My earlier "wrong — it's Lebanon" note was from the *uncut* transcript, which had an "India"-only take.) Residual: the proposal *formally tabled the night of the vote* was Lebanon's (Iran moving to adjourn) — a compression, not a false claim. | **LOW — KEEP** (optional precision tighten in `VO-PICKUPS.md`) |
| 5 | ~01:08:30 | "deserved some pushback" / "constituted" tense slips — inaudible | KEEP |

**On-screen cards for segment:**
- ~01:08:20 (optional) Morris label only — no Morris verbatim is in VO, so no quote card required.
- ~01:09:15 **CARD** "non-Jewish communities" (**primary phrase**): *"existing non-Jewish communities in Palestine."* — card it to the **Balfour Declaration (1917)**; VO credits Khalidi's reading (Khalidi p.27).
- ~01:09:25 **CARD** Khalidi verdict (optional): *"designed to negate their existence"* — label **"Rashid Khalidi — Palestinian historian"** (Khalidi p.120). VO paraphrases as "culmination of that erasure," so the card adds the sharper verbatim if wanted.
- ~01:09:40 **CARD** ⭐ Res 181 equal-rights (the document pushback): *"No discrimination of any kind shall be made between the inhabitants on the ground of race, religion, language or sex."* (Declaration Ch.2 §2) + binding hook *"The Constitutions of the States shall embody Chapters 1 and 2…"* This card **is** the referee's pushback — must be on screen on "equal non-discriminatory… rights."
- ~01:10:00 **CARD** federal counter-offer (optional): A/PV.128.

---

## Segment 8 — ENDING + CLOSE (01:10:24 → 01:11:17)

**SRT lines 300–324 — what's on tape:**
> *"In the end, the borders of the resolution never mattered. What did matter is that the resolution was the first time that the Jewish state got international recognition. What it did not create was a stable border. Those lines were drawn by the 1948 war. When the fighting paused, the territory under Israeli control grew from the proposed 55% to roughly 78%. The independent Arab state envisioned by the UN never came into being. Its remaining fragments were annexed or occupied by Jordan and Egypt. Both sides present simple stories that fall apart when you read the actual document. The 1947 plan was an unfair recommendation that had nobody behind it to enforce when it passed. If you want more history driven by the source documents, rather than the modern commentary, please subscribe."*

**vs script said:** (script CLOSE: "The loudest version of history is usually not the true one…")

**Verdict:** KEEP — the rewritten close is tighter than the script

**Issues:**
| # | Timestamp | Issue | Fix |
|---|---|---|---|
| 1 | ~01:11:05 | **"an unfair recommendation that had nobody behind it to enforce"** — one-line crystallization of the whole thesis. Excellent | **KEEP** |
| 2 | ~01:11:11 | CTA "history driven by the source documents" pays off the doc-reader identity — **even though "So I read the documents" was dropped in the cold open** (see Segment 1 #2: restoring that line would close the loop) | KEEP |

**On-screen cards for segment:**
- ~01:10:45 **CARD/VISUAL** ⭐ cross-camp 55→78/79%: **Shlaim** (Israeli) *"...from the 55 percent… to 79 percent."* (*Iron Wall* p.47) beside **Khalidi** (Palestinian) *"...controlled 78 percent…"* (Khalidi p.60). The two opposite corners landing on one number — the consensus payoff.
- **VISUAL** Ghost-map dissolve: 181 map (55%) → 1949 Green Line (~78%), silent.

**B-roll for segment:** 1948 war / refugees / Green Line — see B-roll research §8.

---

## Pacing assessment

| Marker | Script target | Rough cut actual | Delta |
|---|---|---|---|
| Total runtime | 10.5–11 min | **11:17** (VO-only) | +2.6% over the 11:00 ceiling |
| Cold open | ~55–60s | ~58s | on target |
| Act balance | — | evenly distributed | no bloated act |

**Verdict:** On target. No structural trims required. Final assembly with B-roll/card holds may add a touch — if it pushes past ~11:30, trim from Act 5 (the US/Britain non-enforcement beat has the most paraphrase slack). The channel's hard 12-min cap is not at risk.

---

## Caption pass — DEFERRED

Per creator: hold `/fix` for now. The SRT is auto-generated from bad phone audio, so its "errors" are mostly ASR artifacts (Bursheba, Khaledi, "a certain arrangement," "token point," the missing "that," "Central Political Act"). **If you re-record a clean VO (recommended — see TL;DR #1), re-transcribe the clean audio and `/fix` becomes nearly a no-op.** If instead you keep the phone audio, run `/fix` once on the final assembly before burn-in. Either way, no manual caption work now.

---

## Editing decisions — cut / move / voiceover

Organized by **editing action**. The clean audio (`Recording (14).m4a`) is the ground truth, so the word-level items below are now confirmed, not guesses.

### A. AUDIO / VOICEOVER (the strategic call)

- **Swap the phone scratch audio for the clean recorder audio (dual-system), then normalize.** You already have a good-quality recording — no need to re-perform the whole thing. Conform it take-by-take to the existing picture (the .m4a is the full 23.7-min session with all retakes; pick the clean takes to match the cut), then run loudness normalization to **−14 LUFS / −1 dBTP**. This fixes the −27 LUFS/clipping fail *and* gives correct words (e.g. the Act 3 line is "compromised," not the phone-SRT's "protected"). This is the main audio move.
- **Two genuine fixes remain — they're wrong in the clean audio too, so they need an edit or a small pickup:**
  - **Reedman placeholder (Act 3):** simplest fix is an **edit, not a pickup** — cut the two words "a certain arrangement" so it reads *"…an independent economic expert, to assess whether…"* and let the on-screen card name **John Reedman**. (Or record a 2-second pickup saying the name.)
  - **Act 1 "overlooks how fair the deal was":** small **pickup** of "…how **unfair** the deal was" (or "…**whether** the deal was fair at all"). If you'd rather not pick up, pin a card that frames it as the open question ("Was it fair? →") so the ear isn't left with the inversion. Pickup is cleaner.
- **Optional VO add** — restore "**So I read the documents**" in the cold open (a lock-day first-person beat that sets up the CLOSE callback "history driven by the source documents"). Cheap, on-brand.

### A2. RETAKE HOT-SPOTS (from the clean session — confirm the cut used good takes)

The raw session shows where delivery was shaky and he restarted. Spot-check that the final picture/audio landed on the clean take at each:
- **Cold open:** "UN Resolution **101**" flub → re-taken as 181 (✅ phone SRT shows 181 used — just eyeball the picture). Also "the Internet…" false start; "regions" → "region's future."
- **Act 4 — the big one:** *"the General Assembly holds no legislative power"* restarted **~5 times** (clean audio 10:23–11:55). His hardest line — make sure the cut uses one clean pass and there's no doubled audio.
- Other single restarts to verify: "the land was overwhelmingly Arab" (×3), "a committee of foreign governments" (×3-4), "minority **inside** vs **into** a Jewish state" (use "inside"), "his **formal** report / his report," "major power proved/provided," "federal democratic state" (×3).
- **Content note — re-checked against the CUT 2026-07-03.** The cut names **India, Iran, and Yugoslavia** — the accurate authors of the UNSCOP minority federal plan — so this is **defensible as delivered** (my earlier "India alone is wrong" note came from the uncut transcript). Only residual: the proposal formally tabled the night of the vote was Lebanon's (Iran moved to adjourn) — minor compression. See `VO-PICKUPS.md` Pickup 2 (KEEP / optional tighten).

### B. CUT

- **Optional ~10–15s trim at the Act 4→Act 5 seam** (~01:06:30) — the line "remember that the resolution was just a recommendation. A recommendation that could still be enforced if a major power provides the military power" restates Act 4's just-made point. Tightening it sharpens the pivot into the enforcement-vacuum act. Length is already on target, so this is polish, not necessity.
- **No other content cuts** — the two-narratives setup, the evidence act, and the dueling-historians climax all earn their runtime.

### C. MOVE

- Already done well on tape: "this is the deal the Israeli side refers to" landed at the end of Act 3 (good — it buttons the fairness case).
- **Visual move (no VO):** re-flash the World Court "21–20" chyron in Act 4 as a callback when legality comes up again — ties the cold-open hook to the legality grain-of-truth.

### D. KEEP (the gut cut improved on the script — do not touch)

- "It was a blueprint, not a law." (Act 4)
- "The pressure worked. Resolution 181 passed 33 to 13." (Act 4)
- "an unfair recommendation that had nobody behind it to enforce" (close)
- The whole Act 6 Morris-vs-Khalidi structure — keeping it spoken while stripping mid-body scholar names was the right instinct.
- Dropped mid-body scholar names (Karsh, Kattan, Reedman) — intentional per the experiment; restore via **cards**, never by re-adding to VO.

### E. CARD LABEL (no VO change)

- Act 6 "triggering the massive Palestinian refugee crisis" — keep a persistent "**Benny Morris's reading**" label on screen through that beat so the Nakba-causation claim reads as *his* framing, not the referee's verdict. (This is a graphics decision, independent of audio.)

---

## Music & silence beats

| Time | Beat | Recommendation |
|---|---|---|
| ~01:00:48 | "defeated by a single vote, 21 to 20" | drop the bed to near-silence on the number |
| ~01:02:13 | "who would end up governing whom" | pull energy back; let the line sit |
| ~01:05:14 | "It was a blueprint, not a law." | beat of silence after |
| ~01:08:09 | turn into Act 6 ("the thing people actually argue about") | tonal shift — warmer/quieter bed for the dueling historians |
| ~01:10:45 | cross-camp 55→78/79% ghost-map | swell under the two-historians-one-number payoff |
| ~01:11:05 | "an unfair recommendation that had nobody behind it" | bed out for the thesis button before CTA |

---

## Audio loudness

(From `tools.preflight.audio_loudness` on `2026_06_25_12_01_20.mp4`.)

| Metric | Measured | YouTube target | Verdict |
|---|---|---|---|
| Integrated | **−27.0 LUFS** | −16…−12 (−14 ideal) | ❌ **QUIET** (13 dB under) |
| True peak | **+0.1 dBTP** | ≤ −1 | ❌ **CLIPPING risk** |
| Loudness range | 8.8 LU | 4–15 | ✅ OK |

**Action:** Measured on the *phone* track — this is the scratch audio, not your final. The fix is to **conform the clean `Recording (14).m4a` to the cut**, then normalize that to −14 LUFS / −1 dBTP (two-pass loudnorm raises level and limits peaks in one pass). Re-run this check on the final assembly. `/publish` Gate 3 is only a backstop; don't rely on it.

ffmpeg one-liner if your editor doesn't expose loudnorm:
`ffmpeg -i in.mp4 -af loudnorm=I=-14:TP=-1:LRA=11 -c:v copy out.mp4`

---

## B-roll research (talking-head gaps the cards don't cover)

> **Gemini Flash pass FAILED** — `429 RESOURCE_EXHAUSTED` (daily quota hit). No named source links were returned. The described list below is the Tier-B fallback (search hints, not named sources). Re-run later, or paste the saved prompt into the Gemini/AI Studio web UI — prompt is at the bottom of this section.

Most load-bearing visuals are the **on-screen cards** (mapped per-segment above). The cards cover every primary document and scholar quote. The gaps below need *atmospheric/period* footage:

- **§1 Cold open** — UN GA voting on Res 181 (29 Nov 1947, Flushing Meadows/Lake Success); the physical document.
- **§2 Mandate era** — Britain in Palestine 1917–1947; Arab–Jewish communal tension; ports, Jerusalem.
- **§3 Two narratives** — Ben-Gurion / Arab Higher Committee; 1948 armies.
- **§4 Negev & farmland** — Negev desert, Beersheba-district Bedouin, coastal citrus plain.
- **§5 Enclave map** — the actual UN partition map (six zones); Haifa/Jaffa ports.
- **§6 US pressure** — State Dept, Liberia/Firestone, Philippines delegation.
- **§7 British withdrawal** — exhausted post-WWII Britain, troops leaving 1948, UN Palestine Commission.
- **§8 1948 war & aftermath** — the war, refugees, Green Line.

> **Note:** Public-domain originals only — no AI imagery (channel rule). Maps can be built in MapChart/Canva from the 181 boundary data; the official UN partition map (A/RES/181 annex) is itself public-domain and the strongest §5 asset.

**Paste-ready web-UI prompt** (use if you want named source links — Gemini CLI was quota-blocked):
> For a YouTube history video on the 1947 UN Partition Plan for Palestine (Resolution 181), find specific PUBLIC-DOMAIN B-roll for these 8 narrative gaps (the primary documents are already sourced). For each, give 2–3 candidates as: source name (year/origin) · where to find (archive.org / Wikimedia Commons / LoC / UN Audiovisual Library) with a search term · why it fits. No AI imagery — photos, newsreels, period maps, primary docs only. Gaps: (1) UN GA voting on Res 181, 29 Nov 1947, Lake Success; (2) Mandate-era Palestine 1917–47, Arab–Jewish tension; (3) Ben-Gurion / Arab Higher Committee / 1948 armies; (4) Negev desert, Beersheba Bedouin, coastal citrus plain; (5) the official UN partition map (six zones), Haifa/Jaffa ports; (6) 1947 US State Dept, Liberia/Firestone, Philippines delegation; (7) post-WWII Britain, troop withdrawal 1948, UN Palestine Commission; (8) 1948 war, Palestinian refugees, the Green Line.

---

## Done state

When this video is locked you should have:
- [ ] **Audio resolved** — clean `Recording (14).m4a` conformed to the cut and normalized to −14 LUFS / −1 dBTP (phone scratch audio replaced)
- [ ] **Reedman fix** — "a certain arrangement" edited out (card names John Reedman), or 2s name pickup
- [ ] **Act 1 "how fair" clarified** — small "unfair"/"whether…fair" pickup, or a disambiguating card
- [ ] **Retake hot-spots verified** — esp. the "no legislative power" cluster; cut uses one clean take, no doubled audio
- [ ] (Optional) cold-open "So I read the documents" restored
- [ ] (Optional) Act 4→Act 5 seam tightened ~10–15s
- [ ] Captions: `/fix` on the final clean audio (deferred for now)
- [ ] All on-screen cards placed on their matching beats (the experiment lives or dies here) — especially the Kattan-84%, Reedman, Liberia/Philippines, equal-rights, and cross-camp 55→78/79% cards whose attributions the VO dropped
- [ ] World Court "21–20" chyron re-flashed as the Act 4 legality callback
- [ ] Act 6 Nakba-causation line carries a persistent "Morris's reading" label
- [ ] B-roll sourced for the 8 atmospheric gaps (public-domain only)
- [ ] Ghost-map dissolve (55% → ~78%) built for the close
