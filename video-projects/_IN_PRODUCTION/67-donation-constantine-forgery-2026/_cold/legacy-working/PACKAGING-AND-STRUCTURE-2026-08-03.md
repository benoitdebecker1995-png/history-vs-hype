# Title Set + Script Structure — #67

**Date:** 2026-08-03 · Follows `BREAKOUT-VERDICT-2026-08-03.md`
**Rule applied:** the scorer is recorded, not obeyed (r = −0.053 on this channel). The binding test is
the **11%-shape test** derived from the six videos that ever got real impressions.

---

## ⛔ CORRECTION STAMP — 2026-08-04. THE GOVERNING RULE ABOVE IS RETIRED, AND THE TITLE LOCK WITH IT.

**Verified by direct query.** The "six videos that ever got real impressions" were six *trailing
28-day windows* read out of `analytics.db.videos.impressions` (`ctr_as_of` holds only `2026-07-28` and
`2026-02-23`). Against lifetime `studio_ctr_rows`: median impressions **2,923** not 56, **16** videos
over 5,000 not 1, and lifetime CTR runs **continuously 0.46%→9.41%** with **no video at 11%**.

**Three things in this document fall:**

1. ⛔ **The 11%-shape test.** Not downgraded to "a directional read" as § FINAL LOCK proposed —
   **retired.** It was fitted to windows as small as 17 and 21 impressions. `PACKAGING_MANDATE.md`
   already carried the answer: *[CONFIRMED, null, n=56] no topic FORMULA in the data* (p=0.18).
2. ⛔ **The stated evidence for the locked title.** *"How a Coin Exposed a Vatican Forgery"* was locked
   because *"the channel's only `How…` title is its best CTR (11.6%)"*. KGB's **lifetime** CTR is
   **7.90%** and it is not the channel's best — `JD Vance Claims Christians Found Child Sacrifice` is
   **9.41%**, the Guatemala sequel **9.18%**. The title may still be right; this is not why.
3. ⚠ **The title↔cold-open split is real and unresolved.** § SCRIPT STRUCTURE row 1 opens 0:00–0:45 on
   the 1440/1448/1456 career timeline — written when the title was *"The Vatican Hired the Man Who
   Exposed Its Forgery."* The § ONE STRUCTURAL CORRECTION claim that *"the structure already puts the
   coin there"* is **wrong**: the coin is row two, at 0:45.

**Demand geography — the red-team's one open risk, now measured (vidIQ, 2026-08-04):**

| Term | US /mo | GB /mo | Global topMarkets |
|---|---:|---:|---|
| **constantine** | **11,321** | **2,830** | VN 16%, BR 13.5%, US 10.8%, IN 8% |
| vatican | 5,749 | 2,874 | VN 27%, BR 12%, PK 9%, ES 6%, HU 6% |
| rome | 27,835 | 12,652 | — |
| history of rome | 19,217 | — | US 13.7%, PK 9.8%, RU 9.8%, CA 5.9% |
| medieval europe | 3,197 | 3,197 | PK 29%, BD 21%, IN 21% ⛔ |

⭐ **Constantine out-polls Vatican in both of the channel's biggest markets** — 11,321 vs 5,749 in the
US — which turns the red-team's "restore the famous noun" from a fame-rule inference into a measured
one. **`Vatican`, the current title's search anchor, is the weaker anchor here and its global
distribution points at the wrong continent.**

⚠ **Still unmeasured, reported as unmeasured:** the exact phrase `donation of constantine` returns an
**empty `topMarkets`** on every query and does not appear in either country list, so its 3,412/mo
global remains unallocated. Empty is a false negative from this instrument, not evidence of absence
(`feedback-never-assert-absence-without-direct-check`).

**What survives:** the beat-level research mapping, the exhibit inventory, the thumbnail data
(document-as-focal-object negative, red not a lever, n=46), the farm-signature ban, the
attribute-never-assert rule on `CONCORDIA ORBIS`, and the production-readiness check.

**Superseded by:** `ANGLE-LOCK-2026-08-04.md` once the spine is decided.

---

## THE TEST (empirical, from `analytics.db`)

| | 11% CTR titles | 2% CTR titles |
|---|---|---|
| Examples | *The Country That Might Disappear: Guatemala vs Belize* · *How the KGB Weaponized Palestinian Resistance* | *The 1947 UN Plan Wasn't Legally Binding* · *The Hijab Was Never About Modesty* |
| Shape | **a concrete situation with consequences for identifiable people** | **a proposition about a thing** |
| Test | Someone does something, and it lands on someone | A claim is asserted about an object |

⛔ **Farm-signature ban:** no `[N] years` + `forged/fake document`. Five uploads in 90 days, all <65 views.

---

## SCORED SET

| Score | Chars | Mobile | Shape | Title |
|---:|---:|---|---|---|
| **82** | **49** | ✅ | actor+verb, reversal | ⭐ **"The Vatican Hired the Man Who Exposed Its Forgery"** |
| **87** | 52 | ✅ | actor+verb, reversal | ⭐ **"The Man Who Exposed the Vatican Became Its Secretary"** |
| 80 | 57 | ⚠ cut | actor+verb+**stake** | "Two Men Exposed the Same Forgery. Only One Was Destroyed." |
| 80 | 50 | ✅ | actor+verb+stake | "Two Men Caught the Same Forgery. One Was Destroyed." |
| 70 | 51 | ✅ | actor+verb | "The Pope's Own Coins Proved He Never Ruled Rome" |
| 55 | 51 | ✅ | weak verb | "He Defended the Forgery by Forging His Own Evidence" |
| — | — | — | — | *(controls below)* |
| **100** | 64 | ⚠ cut | ⛔ **proposition + FARM** | ~~"The Vatican Claimed Europe for 400 Years. The Latin Gave It Away."~~ **RETIRED** |
| 70 | 53 | ✅ | proven 11% / 30,540 views | *"The Country That Might Disappear: Guatemala vs Belize"* |

### 🔒 RECOMMENDATION

**Primary: "The Vatican Hired the Man Who Exposed Its Forgery."**
49 characters, survives mobile truncation, names the topic so the thumbnail doesn't have to, and is a
**reversal** — the one thing none of the fifteen competing videos can claim. It also delivers on
**C17b**, which is verified from five sources.

**A/B swap: "The Man Who Exposed the Vatican Became Its Secretary."**
Same fact, mystery-forward, ends on the payoff word. Single-variable swap — identical claim, different
shape. This is the honest A/B the channel's discipline asks for.

**Hold in reserve: "Two Men Caught the Same Forgery. One Was Destroyed."**
The strongest *story* (C20a), but it needs the thumbnail to carry the topic, since nothing in the
title says what the forgery is.

⚠ **Before locking:** run `/curiosity`, re-run the live SERP check, and confirm the thumbnail does not
duplicate the title's words (title carries the reversal, thumbnail carries the object).

---

## SCRIPT STRUCTURE — 11:30, under the 12:00 cap

**Governing rule: the title's promise is the spine, not the ending.** The title says the Vatican hired
him. The script says so in the first forty seconds, and then spends eleven minutes earning *why* —
so nothing is bait and the open question never closes early.

Thesis (T1, unchanged): **two men caught one forgery by testing it against two different worlds.**

| Time | Beat | Content | Ref |
|---|---|---|---|
| **0:00–0:45** | **COLD OPEN — deliver the title** | 1440: a man proves the document the popes had leaned on for centuries is fake. **1448: the Pope makes him apostolic scriptor. 1456: papal secretary.** That is not the story you have heard. *Open question: how does that happen?* | C17b |
| **0:45–2:00** | **THE MECHANISM — the coin** ⭐ | Valla: gold coins of Constantine circulate, Latin not Greek, *"many of which are in my own possession"*, legend **Concordia orbis**. Whoever rules, mints. *"An infinite number would be found for the popes — none are found."* Then **his own metaphor**: *"We tell counterfeit coins apart… and shall we not tell counterfeit doctrine apart?"* | C19, C19a |
| **2:00–3:15** | **THE DOCUMENT** | What it claimed. On screen: **Fuhrmann p. 87, ll. 220–222** — *frygium*, *lorum qui imperiale circumdare assolet collum*. Words that don't belong in the fourth century. Keep tight — this is evidence, not a lecture. | C23 |
| **3:15–4:30** | **TWO MEN, TWO WORLDS** (the thesis) | **Cusa, 1433** — tests the *record*: the popes had to get Pepin, then Charlemagne, to reconquer land they supposedly already owned. **Valla, 1440** — tests the *words*. Same forgery, two different tests. | C0, C13c |
| **≈4:30** | 🔔 **CTA — here, not at the end** | 39% through, after the first real payoff. The channel's documented leak was a CTA at ~80% where only 22.4% still watched. | conversion memory |
| **4:30–6:00** | **REVERSAL 1 — nobody was hiding it** | Otto III's chancery called it a forgery **c. 1001**. The Church's own canon lawyers flagged it — the ***palea***, straw beside grain. And **nobody suppressed Valla**: the Index listing is **1559**, a century after he died. The "forbidden book" story came from his own publishers. | C8, C26 |
| **6:00–8:00** | ⭐⭐ **REVERSAL 2 — the defence was faked** | **Quirini, 1447**: sends the Pope a Greek "older witness" — having quietly deleted *satrapes*, the strap clause, the shoes. Every word Valla convicted, gone. **Steuco, 1547**: prints a Greek colophon proving his ancient witness was copied **in December 1206, for a Roman cardinal**. He published the evidence against himself. | C22, C39 |
| **8:00–9:00** | **THE HONESTY BEAT** | Valla did it too: he knew the mosaic inscription and left it out; never touched the *Liber Pontificalis*; in 1444 forced a *Decretum* reading when the Creed was at stake — *"at odds with a disinterested philology."* **Camporeale, his greatest admirer, is the one who says so.** And Steuco's objection was right *in principle* — establish the ***vera lectio*** first. | C14d, C32a, C39d |
| **9:00–10:15** | **THE ANSWER TO THE TITLE** | Why hire him? Because in 1440 the document's falsity was not yet the scandal it became in 1518. Alfonso had already settled with the pope — Valla refused to retract anyway. Meanwhile **Pecock**, who exposed the same forgery *to defend the Church*, was made to recant, had his books burned, and died confined. **The reaction had nothing to do with the document.** | C17d, C20a |
| **10:15–11:30** | **CLOSE** | Steuco used the *better* method — find the oldest witness — and still lost, because his family tree was upside down. **It took until 1929 to prove which way it ran.** Being right didn't make Valla matter; being *useful* did — von Hutten prints it 1518, five languages by 1546. | C15b, C17c |

### Why this order

- **The reversal structure is the moat.** All fifteen competitors run *fake → caught → Church embarrassed*.
  This runs *caught → and then nothing happened → and the defence was faked too → and the man who
  defended the Church was the one destroyed.* Four turns they cannot copy without our sources.
- **Approval before the ask.** The coin lands at 2:00 — satisfying, verifiable, needs no Latin. Likes
  (not retention) predict subscribing on this channel, so the CTA follows the approval moment.
- **Every act has a filmable object**: a coin, a printed page, a deleted clause, a colophon.

---

## ⛔ WHAT GETS CUT (and where it goes)

| Cut | Why | Destination |
|---|---|---|
| Sangiorgi's *restitutio* + the unfalsifiable suppression device (C34a–b) | Superb, but it is a *fourth* reversal and the script already has three | **Sibling 1** |
| Bolognini defending one forgery to save another (C34c) | Same | **Sibling 1** |
| The Greek transmission chain, 1252 → Blastares → Quirini (C24, C38, C41) | Load-bearing *behind* the Quirini beat; on screen it is a stemma lecture | Keep one sentence only |
| Mabillon vs Papebroch (C21 📌) | Different document set, different century | **Sibling 2** |
| The six datings, 750–850 (C35a) | ⚠ **One line max**, and never a single date | One line |
| Whethamstede (C35c) | One clause — *"and he was not the only one noticing"* | One clause |
| Pecock's method in full (C1, C2, Levine) | Compressed to the fate-inversion at 9:00 | **Sibling 3** |

**Runtime honesty:** the research file holds ~86 tracked claims. **This structure uses about fifteen.**
That ratio is correct — the surplus is what makes the fifteen defensible under comment scrutiny.

---

# REVISED TITLE SET — demand-tested, 2026-08-03

**New gate added:** a title must map to a **documented comment thread**, not to a research finding I
find satisfying. Sample: Polidoro IT (235 comments) + Stephan's EN (27) + Historias de la Historia ES
(1,441, mined 2026-08-01).

## ⚠ The distinction that resolves the tension

**Comment demand ≠ click demand.** People argue about *"was it ever really used?"* **because they
already watched.** That proves topic engagement, not stopping power. A Browse title has one job: make
a stranger stop scrolling. **So demand belongs in the script and the pinned comment; the title needs
mechanics.** The best candidate does both.

| Score | Chars | Demand anchor | Title |
|---:|---:|---|---|
| 67 | **43** | ⭐ method contested (EN + ES) | 🔒 **"He Caught the Vatican's Forgery With a Coin"** |
| 82 | 49 | ⚠ none observed | ⭐ **"The Vatican Hired the Man Who Exposed Its Forgery"** — A/B challenger |
| 55 | 48 | ⭐⭐ strongest thread (IT ×4) | "Rome Kept Citing the Forgery After It Was Caught" |
| 77 | 50 | method contested | "He Proved the Vatican's Document Fake Using a Coin" |
| 70 | 39 | method contested | "A Coin Proved the Pope Never Ruled Rome" |
| 85 | 56 ⚠CUT | was-it-used | "Rome Cited the Forgery for 500 Years After It Was Caught" |

## 🔒 PRIMARY — "He Caught the Vatican's Forgery With a Coin"

**43 characters — the shortest thing tested, zero truncation risk on mobile.**

- ✅ **Concrete, unexpected object.** The surprise is that the weapon is a *coin*, not a document. That
  is a stopping image, and it is literally the first exhibit in the script (C19, at 0:45).
- ✅ **Maps to demonstrated demand** — the *method* is what viewers spontaneously contest
  (EN: *"a fossilized language used only administratively doesn't have the same changes, I think
  nothing of this"* = Steuco's argument, reconstructed by a viewer; ES: a commenter reconstructs the
  philological method unprompted).
- ✅ Actor + verb + object — the 11%-shape.
- ⚠ **"He" is anonymous** and no stake is stated. **The thumbnail must supply both** — the coin, and a
  face or an institution.
- Scores 67. **Ignore that** (r = −0.053; the breakout scores 70).

## ⭐ A/B CHALLENGER — "The Vatican Hired the Man Who Exposed Its Forgery"

Keep it, and keep it honest: **no observed demand**, but the best shape metrics and a self-contained
reversal. Running it against the coin title tests **concrete object vs reversal** — a result that
transfers to every future title on this channel. That is worth more than winning this one video.

## Where the demanded question actually goes

**"Was it ever really believed or used?"** — the strongest documented thread (four independent
commenters on the best-performing video) — is served by:
1. **The 4:30–6:00 script beat** (C8, C26, C41) — Otto III's chancery c. 1001, the *palea*, and the
   1559 Index, against the demonstrable deployments from Leo IX 1053 to Steuco 1547.
2. **The pinned comment**, posted at upload, stating the answer in three sentences and inviting the
   argument. Polidoro's pinned-comment tactic held 1,441 comments civil.
3. **The description's first two lines.**

⛔ **Do not put it in the title.** Its natural phrasings run 56–66 characters and truncate, and the
strongest of them ("nobody believed it") is the **2% proposition shape**.

---

# FINAL LOCK + THUMBNAIL BRIEF — 2026-08-03

## ⛔ THREE CORRECTIONS TO THIS DOCUMENT (checked against `PACKAGING_MANDATE.md`, fresh n=56 July-23 data)

**1. My "red thumbnail" read was an over-fit and is WITHDRAWN.** On n=5 all three 11% thumbnails had
`red=1`. On the full **n=46**: *"**red is not a lever** (2.48% vs 3.16%)."* The mandate's own
"OVER-FIT KILLS" warning caught this. **Do not brief for red.**

**2. The "11%-shape test" is downgraded from a gate to a directional read.** It came from n=6. The
mandate has **[CONFIRMED, null, n=56] no topic FORMULA in the data** (Kruskal–Wallis **p=0.18**), and
says explicitly: *"Do not build a 'make territorial disputes' doctrine."* **Keep the actor+verb
preference as a tiebreaker, not as law.**

**3. "Search is nearly irrelevant" was too strong.** Search is a small share of views but
**[CONFIRMED] entity-led and concentrated** — 47% of non-Guatemala search views come from **5 exact
named terms**. **V2 is a hard PASS/FAIL gate.** ✅ Both finalists pass: `has_search_anchor` returns
`(True, 'Vatican')` for each.
📌 Note: *"The Country That Might Disappear: Guatemala vs Belize"* — the 30,540-view breakout — **FAILS**
that recognizer. Another instance of a tool disagreeing with reality; record, don't obey.

## 🔒 TITLE — LOCKED

**Primary: "How a Coin Exposed a Vatican Forgery"** — 36 chars · curiosity **75** · scorer 62 · V2 ✅

Supported by three independent things: the channel's **only** `How…` title is its best CTR (11.6%) and
best subscriber conversion (**5.4%/view, 10× the Guatemala breakout**); the mandate's
**[HYPOTHESIS, n=8] evidence-promise titles run higher CTR** (3.28% vs 2.41%) and a coin *is* an
evidence promise; and it satisfies the channel-DNA note — *front-load the searched subject, deliver
the primary-source reveal as the second punch.*

**A/B challenger: "The Vatican Hired the Man Who Exposed Its Forgery"** — 49 chars · curiosity **83**
Optimises clicks rather than subscribers. Tests **mechanism-promise vs reversal** — a result that
transfers to every future title.

⚠ **Honest risk on the primary:** V2's evidence says the stall cohort is *"dominated by document/myth-first
titles."* Ours leads with an object, not the entity. It passes the gate but sits closer to that shape
than the challenger does. **That is precisely what the A/B is for.**

---

## 🎨 THUMBNAIL BRIEF

**Governing data (n=46, `thumbnail_features` + mandate):** *"One clear focal object, few elements."*
· **document-as-focal-object NEGATIVE** (2.39% vs 3.11%) · busy weak-negative · **red not a lever**.
📌 `em=0` on all five tagged thumbnails — **this channel has never used a face.** Untested, not disproven.

### The concept

**Focal object: a single gold coin of Constantine, filling the frame.**

This is the rare case where the data points the same way twice. The strongest exhibit in the research
(C19) is *not* the document — and **documents are the one thing measurably negative in the thumbnail
data.** A parchment reads as a beige rectangle of unreadable text at 60 px. **A coin reads as a coin at
any size**: round, metallic, high-contrast, instantly legible, and unexpected on a video about a
forged charter.

- **One object. Nothing else.** No parchment, no map, no split-screen, no arrows.
- **Do not brief for red.** Gold-on-dark is the natural palette; let the object's own colour carry it.
- Extreme close-up so the *Concordia orbis* legend and the cross are visible but not readable —
  texture, not information.

### Overlay text — must NOT repeat the title

The title already says *coin* and *forgery*. Per the division-of-labour rule the overlay must **raise
the question or name the charge**, not restate the object. And it must supply the **stakes the title
lacks** (curiosity scored 27/40 there).

Test these three, single-variable:
1. **"WHERE IS THE POPE'S?"** — the argument itself, in four words. Turns the object into a question.
2. **"1440"** — date only. Maximum restraint; lets the coin do everything.
3. **"NONE WERE EVER FOUND"** — states the absence that convicts the document.

**Recommended: option 1.** It is Valla's actual argument, it creates the gap the title doesn't, and it
cannot be confused with the farm thumbnails (which are uniformly popes, parchment and gold crosses).

### Asset needed

A public-domain image of a **Constantinian gold solidus, post-312, Latin legend, cross or Christogram
visible**. Sources: British Museum collection online, Wikimedia Commons, American Numismatic Society.
⚠ **Verify it is post-conversion and Latin-legend** — the whole argument in C19 depends on *"non Graecis
sed Latinis litteris."* A Greek-legend or pre-312 coin would be a self-inflicted factual error on the
one frame everyone sees.

---

## ⚠ ONE STRUCTURAL CORRECTION TO THE SCRIPT

**[CONFIRMED, n=55] The 5–10% post-hook seam is where holds are won or lost** — the beat right after
the cold open loses a mean **12.7 pp** against 4.7 pp for the next band. The mandate's instruction:
*"no welcome, methodology preamble, recap, or roadmap in the first 5–10%; go straight into substance."*

On an 11:30 runtime that seam is **0:35–1:10**. ✅ The structure already puts the coin there — **keep it
that way and add nothing.** No channel intro, no "in this video we'll look at", no thesis statement.
The coin argument *is* the substance and it starts immediately.

⚠ **Also separate two things I had blurred:** like-rate correlates **negatively** with impressions
(ρ = −0.26, n=56) — *"you cannot earn a push with retention/engagement tuning."* The early CTA is
justified as a **subscriber-conversion** move, not a distribution move. Distribution is title +
thumbnail + topic, and nothing else.

---

# 3 × 3 TEST SET + THE COIN — 2026-08-03

YouTube allows **3 titles and 3 thumbnails** per test. Each slot below varies **one** thing.

## ⚠ FACT-CHECK FIRST: Valla's coin legend does not match the surviving coins

Valla (C19) says his coins carried *"hac plerumque subscriptione subter imaginem crucis, **Concordia
orbis**."* **I could not verify `CONCORDIA ORBIS` as an attested Roman legend.** The attested
Constantinian Concordia types are **CONCORDIA AVGG NN**, *MILITVM*, *AVGVSTA*, *AVGVSTI*,
*PROVINCIARVM*. Searched OCRE, NumisWiki and Forum Ancient Coins: **no `CONCORDIA ORBIS`.**

**[CONTESTED]** · locator: Valla, Coleman p. 70 vs OCRE/NumisWiki legend indices · opposed-by: no attested ORBIS type found

⛔ **Script rule: attribute, never assert.** Say *"Valla says he owns many of them, mostly reading*
Concordia orbis *beneath a cross"* — **do not caption a coin `CONCORDIA ORBIS`.**
⭐ **His argument is untouched**: the coins are Constantine's, they are Latin, and no papal coinage
exists. Only the legend detail is doubtful — and *the man who convicted a document by reading its words
precisely, slightly misquoting a coin from memory* is a good beat, not a problem. ⚠ Do not inflate it
into the C14d/C32a selectivity theme; misremembering ≠ suppression.

## 🪙 THE COIN — verified and cleared

**PRIMARY — use this one.** `File:Solidus of Constantine I, AD 320.jpg`
- **1,500 × 708 px** · Ticinum mint · **AD 320** (post-conversion ✅)
- Obverse **CONSTANT-INVS P F AVG** · Reverse **CONCORD-I-A AVGG NN** — ⭐ a real Constantinian
  **Concordia** solidus, in **Latin**, which is as close to Valla's claim as the record allows
- Licence **CC BY-SA 2.5 + GFDL** — usable, **attribution required** (Classical Numismatic Group)
- `https://upload.wikimedia.org/wikipedia/commons/b/bc/Solidus_of_Constantine_I%2C_AD_320.jpg`
- Practical: the reverse crops to ~700 × 708, which fills a 720-high frame at ~3% upscale. Fine.

**BACKUP — cleanest licence.** `File:Gold Solidus of Constantine I, Nicomedia.jpg`
- 489 × 496 px · Nicomedia · **316 CE** · **CONSTANTINVS P F AVG**, Latin
- **CC0 1.0 — public domain, no attribution** · American Numismatic Society
- ⚠ Too small to fill a thumbnail; fine for on-screen B-roll
- `https://upload.wikimedia.org/wikipedia/commons/2/21/Gold_Solidus_of_Constantine_I%2C_Nicomedia.jpg`

📌 Higher resolution, if wanted: ANS MANTIS and CNG's own archive both hold larger files of these types.

## TITLES — 3 slots, 3 different levers

| # | Title | ch | curiosity | scorer | V2 | Lever being tested |
|---|---|---:|---:|---:|---|---|
| **A** | **How a Coin Exposed a Vatican Forgery** | 36 | 75 | 62 | ✅ | **Mechanism-promise.** Matches the channel's only `How…` title — best CTR (11.6%) and best sub conversion (5.4%/view) |
| **B** | **The Vatican Hired the Man Who Exposed Its Forgery** | 49 | **83** | 82 | ✅ | **Reversal.** Highest curiosity; optimises clicks over subs |
| **C** | **The Vatican Destroyed the Wrong Man** | **35** | — | **87** | ✅ | **Stakes.** The axis A and B are weakest on (27/40, 32/40). Front-loads the entity; shortest of all |

⚠ **C carries a claim risk.** It points at **Pecock** (C20a), who is a 9:00 beat, not the spine. If C
wins, the script must move the fate-inversion earlier or the title is a bait. **Decide that before
enabling C.**
📌 Rejected: *"Two Men Exposed the Vatican's Forgery. One Was Destroyed."* — scores 92, but 57 chars
truncates on mobile.

## THUMBNAILS — 3 slots, one variable each

**Fixed across all three** (from `thumbnail_features` n=46): **one clear focal object, few elements** ·
**no document as focal object** (measurably negative, 2.39% vs 3.11%) · not busy · **red is not a
lever — do not brief for it.** Gold-on-dark, the coin filling the frame.

| # | Image | Overlay | Variable tested |
|---|---|---|---|
| **1** | Coin alone, tight crop, gold on near-black | **"WHERE IS THE POPE'S?"** | *baseline* — Valla's argument as a question |
| **2** | Identical crop, identical treatment | **"1440"** | **text volume** — does minimal beat a sentence? |
| **3** | Coin **held between finger and thumb**, same crop scale | **"WHERE IS THE POPE'S?"** | **human presence** — `em=0` on all five tagged thumbnails; this channel has *never* used a hand or face. Untested, not disproven |

**Why "WHERE IS THE POPE'S?"** — the title already says *coin* and *forgery*, so per the
division-of-labour rule the overlay must raise the question, not restate the object. It also supplies
the **stakes the title lacks**, and it looks nothing like the competing thumbnails, which are
uniformly popes, parchment and gold crosses.

⚠ **Read 1 vs 2 and 1 vs 3 as separate single-variable results.** Do not change the crop, colour or
coin between slots — that is what makes the test mean anything.

---

# ⛔ CORRECTION: the thumbnail test was designed wrong — 2026-08-03

**My 3 thumbnails were the same thumbnail with different overlays.** Methodologically that is clean
single-variable testing. **Strategically it is wrong at this stage.** With a **56-impression median**
and one video in 58 ever served, the job is to **find something that works**, not to attribute *why*
a coin works. If the coin concept is simply wrong, all three slots fail and you learn nothing you
could act on.

**Revised: three different CONCEPTS.** Attribute later, once something wins.

| # | Concept | Focal object | Overlay | The bet |
|---|---|---|---|---|
| **1** | **The evidence** | Constantine's gold solidus, tight, gold on near-black | **"WHERE IS THE POPE'S?"** | Valla's argument as an object. Differentiated — no competitor thumbnail uses a coin |
| **2** | **The face** | **Constantine's portrait enlarged from the coin's obverse**, filling frame | **"HE NEVER SIGNED IT"** | `em=0` on all 5 tagged thumbnails — **this channel has never used a face.** Faces are the single biggest untested lever available |
| **3** | **The absence** | The solidus, and beside it an **empty circular void** where a papal coin would be | **"ONE OF THESE WAS NEVER MINTED"** | The argument made visual — two elements, still "few". Highest concept risk, highest ceiling |

All three keep: **one clear focal object · no document · not busy · no red brief** (n=46).
⚠ **2 and 3 are genuinely untested shapes for this channel. That is the point.** Read the winner as
"this concept pulls", not "this variable pulls".

## Titles — same correction, already satisfied

A/B/C already test **three different levers** (mechanism / reversal / stakes), not three phrasings.
No change.

---

# ✅ PRODUCTION-READINESS CHECK — can we actually make this?

**Verdict: yes. Research and exhibits are ready; the script is not written.**

## Assets now on disk — `_assets/exhibits/` (created 2026-08-03)

| Asset | Source | Status |
|---|---|---|
| **Constantine solidus, AD 320, Ticinum** — *CONSTANT-INVS P F AVG* / *CONCORD-I-A AVGG NN* | Wikimedia / CNG, **CC BY-SA 2.5** (attribution required) | ✅ 1500×708 downloaded |
| **Constantine solidus, 316, Nicomedia** | ANS, **CC0** | ✅ 489×496 downloaded (B-roll only) |
| **Fuhrmann p. 87** — *frygium* + *lorum qui imperiale circumdare assolet collum* | P1, 300 dpi render | ✅ |
| **Fuhrmann p. 80** — *satrapibus* in the decree formula | P1, 300 dpi render | ✅ |
| ⭐ **Setz p. 119** — Quirini's *Sanctio*, ***provinciarum prefectis*** where *satrapibus* belongs, with critical apparatus | A5, 300 dpi render | ✅ **visually verified** |
| **Delph p. 60** — the Otranto colophon | A16, 300 dpi render | ⚠ rendered, **not yet eyeballed** |

## Beat-by-beat: does every scene have a showable exhibit?

| Beat | Exhibit | Ready? |
|---|---|---|
| 0:00 the coin | Solidus AD 320 | ✅ |
| 2:00 the document | Fuhrmann pp. 80, 87 | ✅ |
| 3:15 Cusa's Pepin proof | P3 Sigmund — render on demand | ✅ source held |
| 4:30 the *palea* | Coleman — render on demand | ✅ source held |
| 4:30 **Otto III, DO III 389** | ⛔ **NOT HELD** — only Fried quoting it | ⚠ **audio-only claim; nothing to show** |
| 6:00 Quirini doctored | Setz p. 119 | ✅ **the strongest card in the video** |
| 6:00 Steuco colophon | Delph p. 60 ✅ / Steuco's own page ⛔ (C40c, not located) | ⚠ show Delph, not Steuco |
| 8:00 Valla's omissions | Grafton — render on demand | ✅ source held |
| 9:00 Pecock | Levine + Bowersock | ✅ sources held |
| 10:15 close | Zanobini | ✅ source held |

**Two beats have no showable object: DO III 389, and Steuco's own colophon page.** Both are
adequately *sourced* (Fried; Delph) — they just can't be put on screen as primaries. **Write them as
narrated, not as document reveals.**

## What is actually missing

1. ⛔ **`SCRIPT.md` is 85 bytes — empty.** This is the only real blocker.
2. ⚠ No thumbnail comp built yet (assets exist, composition doesn't).
3. 📌 Optional: a higher-resolution solidus from ANS MANTIS or CNG if the coin fills the frame.
