# Breakout Verdict — #67 Donation of Constantine

**Date:** 2026-08-03 · **Analyst mode:** packaging/growth, not history
**Sources:** `analytics.db` (58 videos) · `title_scorer` · vidIQ keyword research · vidIQ live SERP

---

## ⛔ CORRECTION STAMP — 2026-08-04. THIS DOCUMENT READ THE WRONG COLUMN.

**Verified by direct query, not inferred.** Every impression and CTR figure below comes from
`analytics.db.videos.impressions` / `.ctr_percent`, which are **trailing-window snapshots**, not
lifetime. `videos.ctr_as_of` holds exactly two dates — `2026-07-28` (57 videos) and `2026-02-23` (1).
Lifetime truth is `studio_ctr_rows` (2026-07-23 Studio export, 57 videos).

| | `videos.*` (window) | `studio_ctr_rows` (lifetime) |
|---|---:|---:|
| Median impressions | **56.5** | **2,923** |
| Videos ≥5,000 impressions | **1** | **16** |
| Videos ≥20,000 impressions | **0** | **4** |

**What that overturns in this document:**

1. ⛔ *"Median impressions: 56. One video in 58 ever recorded ≥5,000"* (§ line 60) — **false.** Sixteen
   videos cleared 5,000 lifetime impressions. YouTube tests this channel routinely; the tests fail on
   the **click**, not the serve.
2. ⛔ *"~11% or ~2%. Nothing between"* (§ line 72) — **the bimodality does not exist.** Lifetime CTR
   runs continuously from **0.46% to 9.41%**, median 2.48%, with no gap at the claimed split. **No
   video on this channel has an 11% lifetime CTR at all** — the 11% figures were 20-to-3,900-impression
   windows. The actor+verb-vs-proposition "shape test" built on them is retired, not downgraded.
3. ⛔ *"Impressions are the binding constraint. Nothing in the script fixes a 56-impression median"*
   (§ line 179) — **false, and it inverts the conclusion.** Serve is not the bottleneck; the click is.
   Title and thumbnail carry the load, exactly as `PACKAGING_MANDATE.md`'s Gate-2 model says.

**What survives:** the field scan, the competitor table, the vidIQ keyword volumes, and the
farm-signature ban. The research in this document is fine; its packaging conclusions are not.

Full derivation: `CONCEPT-REDTEAM-2026-08-03.md` § FINDING 0 (verified 2026-08-04).
📌 **Out of scope here, still open:** the same window/lifetime confusion may contaminate analyses in
other project folders and any doctrine derived from `videos.impressions` repo-wide.

---

## VERDICT IN ONE LINE

**The research is more than enough. The packaging as locked is a near-certain failure — because the
locked title is structurally identical to five AI-farm videos published in the last 90 days that
averaged 43 views.**

Do not shelve. **Reframe.** The fix is free and the asset that makes it possible is already in the
research file.

---

## 1. THE FIELD — this topic was strip-mined in 2026

Live vidIQ search, `Donation of Constantine forgery Valla`, long-form, by view count:

| Views | Channel | Subs | Published | Title |
|---:|---|---:|---|---|
| 40,431 | Massimo Polidoro | 342K | 2021 | *"Grandi falsi: la Donazione di Costantino"* — **Italian** |
| 4,309 | Stephan's History of the World | 69.8K | 2024 | "The Church's Most Famous Forgery" |
| 2,633 | WikiWikiup (TTS bot) | 91K | 2016 | "Lorenzo Valla" |
| 1,171 | Stephan's | 69.8K | 2026-06 | "Lorenzo Valla exposed forged Church documents…" |
| 846 | Jason Sylvester | 894 | 2024 | "Fact vs Fiction: The Donation of Constantine" |
| 421 | Holy History | 15K | 2025-11 | "…The Biggest Forgery in Catholic History" |
| **63** | Buried History | 757 | **2026-06** | **"The Pope Controlled Every King in Europe For 700 Years — Using a Forged Document"** |
| **61** | The Fire & the Veil | 207 | **2026-06** | **"The Document That Built Papal Power Was a Forgery — and the Church Admits It"** |
| **38** | Theology Made | 4.9K | **2026-05** | **"The Fake Document That Gave the Pope Power Over Kings for 700 Years"** |
| **30** | Stories with Dastan | 0 | **2026-06** | **"The Forged Document That Ruled Europe for 1000 Years"** |
| **25** | Schooled by Voss | 1 | **2026-06** | **"The Lie That Built the Pope's Empire"** |

### ⛔ The finding

**Five videos in the last three months, all using the same title frame, all under 65 views.** The
channels have 0, 1, 207, 757 and 4,930 subscribers. These are content-farm uploads.

**Our locked title —** *"The Vatican Claimed Europe for 400 Years. The Latin Gave It Away."* **— is the
same sentence.** `[Institution] + [held/claimed power] + [N hundred years] + [forgery reveal]`.

**This is not a coincidence to be argued around. It is a classifier problem.** The pattern has been
mass-produced into the ground in 2026, and it is now a negative signal in this topic space.

### The real ceiling
The **English long-form ceiling is ~4,300 views on a 70K-sub channel** — a 6% view/sub ratio, poor.
The only strong performer is Italian, from 2021, on a 342K channel.
⚠ **This corrects `COMPETITOR-GAP-ANALYSIS.md`**, which put the English ceiling at ~15K. That 15K
video (*Static in the Attic*) is **phantom-time conspiracy**, a different topic and a different audience.

---

## 2. THE CHANNEL — the constraint is impressions, not clicks or quality

From `analytics.db`, n = 58:

- **Median impressions: 56.** One video in 58 ever recorded ≥5,000.
- **Only 6 videos ever recorded ≥300 impressions.** Their CTRs are strictly **bimodal**:

| Impressions | CTR | Views | Subs | Title |
|---:|---:|---:|---:|---|
| 10,952 | **1.6%** | 308 | 5 | Israel vs Palestine. The 1947 UN Plan Wasn't Legally Binding |
| 3,915 | **11.0%** | **30,540** | **153** | The Country That Might Disappear: Guatemala vs Belize |
| 1,558 | **11.4%** | 5,640 | 54 | Guatemala vs Belize Dispute: What 3 ICJ Cases Show |
| 594 | **11.6%** | 596 | 32 | How the KGB Weaponized Palestinian Resistance |
| 517 | **2.9%** | 126 | 6 | The Hijab Was Never About Modesty… |
| 351 | **9.4%** | 459 | 7 | Somaliland's Legal Independence Problem |

**~11% or ~2%. Nothing between.** The 11% titles carry **named parties in conflict** or a **human
stake**. The 2% titles carry an **abstract proposition** (*"wasn't legally binding"*, *"was never
about modesty"*).

⛔ **Our locked title is the abstract-proposition shape.** *"The Latin"* is an abstract noun, and it is
ambiguous on a phone — Latin language? A Latin person? The one time YouTube served this channel
heavily (10,952 impressions), an abstract-proposition title converted at **1.6%** and the video died
at 308 views.

**Traffic mix:** Browse/Suggested **33,445** + Related **6,976** vs **YT_SEARCH 3,294 lifetime.**
⇒ **Search volume is nearly irrelevant to this channel.** The title is a *feed* object, not a query
match. The scorer's +12 "search anchor" bonus is optimising the wrong surface.

---

## 3. ⛔ THE TITLE SCORER IS ANTI-PREDICTIVE HERE — do not trust the 100/A

Scored the top 20 videos by views against their actual performance:

**Pearson r(title_score, views) = −0.053 (n = 20).** No predictive power; if anything, negative.

| Score | Views | Title |
|---:|---:|---|
| **100** | 257 | China vs Taiwan. 4 Historical Claims Exposed by Scholars |
| **100** | 228 | India vs Pakistan. Britain Sold Kashmir for 7.5 Million |
| **92** | 156 | The Piri Reis Map Cites Columbus… |
| **82** | 308 | Israel vs Palestine. The 1947 UN Plan… (**1.6% CTR**) |
| **70** | **30,540** | **The Country That Might Disappear: Guatemala vs Belize** |

Five titles score 100 and average **~814 views**. **The one breakout scores 70** — penalised −5 for a
colon, in a channel whose #1 and #3 videos both use colons.

**Our title scores 100/A. That is worth nothing.** It scores 100 partly for the *"two-sentence
formula (11% outlier rate)"* — a bonus shared by both of the channel's worst-converting served videos.

📌 This is consistent with ADR-0012 (*filters decide, scores inform*) — but the 100 has been read as
reassurance. **It isn't. Record the number, ignore the grade.**

---

## 4. DEMAND — real but thin, and pointed at the wrong countries

vidIQ keyword research:

| Keyword | Est. monthly | Competition | Note |
|---|---:|---:|---|
| donation of constantine | **3,412** | 21.3 | passes the ≥1,000 gate; modest |
| lorenzo valla | 3,654 | 26.9 | |
| papal states | 3,946 | 34.8 | |
| constantine the great | 8,149 | 37.4 | |
| **vatican** | **100,602** | 65.2 | ⚠ top markets **VN, BR, PK, ES, HU** |
| constantine | 113,206 | 59.5 | ⚠ top markets **VN, BR, US, IN, BD** |
| history of rome | 142,756 | 37.5 | ✅ **US 13.7%, CA** — matches channel audience |

⚠ **The "Vatican" anchor in the locked title pulls Vietnam, Brazil and Pakistan.** The channel's
audience is **UK/DE/CA/US males 25–44**. High-volume anchor, wrong geography, and search barely feeds
this channel anyway.

**No live cluster boost:** an outlier sweep on forgery/document-exposure framings over six months
returned no medieval-forgery breakouts — only true crime, politics and unrelated noise. **Nothing in
this space is being pushed right now.**

---

## 5. WHAT WE HAVE THAT NOBODY ELSE DOES

Every one of the 15 competing videos tells the same story: *document was fake → Valla caught it →
Church embarrassed.* **All three of those beats are contradicted by our own research.**

| Our finding | Ref | In the field? |
|---|---|---|
| **The defence was doctored** — Quirini (1447) deleted the exact words Valla convicted, then dedicated it to the Pope | C22 | **No — nowhere, any language** |
| **Steuco printed the colophon that destroys his own case** — his "ancient Greek witness" was copied for a Roman cardinal in 1206 | C39 | **No** |
| **The papacy hired Valla** — apostolic scriptor 1448, papal secretary 1456 | C17b | **No** |
| **Pecock was destroyed for defending the Church**; Valla promoted for attacking it | C20a | **No** |
| **Nobody suppressed it** — the Index listing is 1559 | C26 | **No — the field asserts the opposite** |
| The "Greek original" is a Latin round trip; the claim dates to 1252 | C24, C41 | **No** |

**That is a different video from all fifteen.** The problem is that **the locked title promises the
same video they made.**

---

## 6. THE RECOMMENDATION

### Kill the frame, not the project.

The current title sells *"a forged document held power for centuries."* That story is finished — the
farms ate it, and the classifier knows it.

**Sell the reversal instead: the defence was faked too.** Nobody has it, it has a human antagonist, and
it inverts the expectation the thumbnail sets up.

Direction only — these need scoring, `/curiosity`, and a live SERP re-check before locking:

- *"The Vatican Hired the Man Who Exposed Them."* — **the C17b fact, and it is a genuine reversal**
- *"He Faked the Evidence Defending a Forgery."* — the C22 finding, human antagonist, present tense
- *"Two Men Exposed the Same Forgery. Only One Was Destroyed."* — the C20a inversion; nearest to the
  proven *"Country That Might Disappear"* shape (human stake + implicit versus)

**Test against the channel's own evidence, not the scorer:** does it name people in conflict? Is there
a human stake? Would it read at a glance on a phone? The 11% titles pass; the 2% titles fail.

### Also
1. **⛔ Do not reuse `[N] years + forged document`** in title or thumbnail. It is the farm signature.
2. **Cluster it.** The breakout had a sibling; every isolated upload died. #67 should ship with at
   least one of the CLUSTER SEEDS planned, not alone.
3. **Impressions are the binding constraint.** Nothing in the script fixes a 56-impression median —
   only the title/thumbnail pair does.
4. **Retention is not the problem.** Top videos run 26–39% AVD. The research surplus protects
   retention and comments; it cannot buy reach.

---

## 7. HONEST LIMITS OF THIS ANALYSIS

- **n = 6** videos with meaningful impressions. The bimodal CTR pattern is suggestive, **not proven**.
- The `impressions` column is **internally inconsistent** — the breakout shows 30,540 views on 3,915
  impressions, which cannot be right. **Treat impressions as directional only.** The CTR figures on
  the six are still the best signal available.
- vidIQ view counts are a snapshot of one query on one day; a differently-phrased search would surface
  a different field.
- The five sub-65-view farm videos are **recent**, so their view counts may still be maturing — but
  five independent uploads all under 65 views in 90 days is a pattern, not noise.

---

# ADDENDUM — COMMENT MINE, 2026-08-03. **The title recommendation was not demand-tested. It is now.**

Mined `qAsK9uxoxCw` (Polidoro, IT, 40,431 views, 235 comments — the topic's best performer) and
`QV7rtg9ACpQ` (Stephan's, EN, 4,309 views — the best English performer). ~80 comment threads read.

## ⛔ What the audience does NOT talk about

**Zero mentions, across both videos, of:** Valla's fate · the Church employing him · Pecock ·
Steuco by name · anyone defending the document.

⛔ **The recommended title — "The Vatican Hired the Man Who Exposed Its Forgery" — sells a fact with
NO demonstrated audience demand.** It is a real finding (C17b) and a real reversal, but no viewer in
this sample is asking the question it answers. That was an inference from packaging shape, not from
evidence. **Recorded as a correction.**

## ⭐⭐ What they ARE arguing about — the live, unresolved question

**The most substantive and most-replied thread on the best-performing video is whether the document
was ever actually believed or used.** Four commenters independently, unprompted:

- **@CalogeroPeritore (9 likes, 5 replies):** *"Quanto alla Donazione di Costantino **non ci credeva
  nessuno nel Medioevo**, tanto è vero che nessuno dei più agguerriti papi… Gregorio VII, Innocenzo III,
  Innocenzo IV o Bonifacio VIII… se ci avessero veramente creduto non avrebbero esitato a inserirla
  nelle loro argomentazioni."*
- **@gig076:** *"A questo documento non ci ha creduto mai nessuno anche all'epoca dei fatti."*
- **@earthshaker5882 (2 likes):** *"il peso politico della Chiesa era già smisurato… un documento che
  può avere aiutato a legittimare un potere che fattualmente era già ben consolidato."*
- **@ihs42sm (3 likes):** the post-Constantine power vacuum explains papal temporal power, not the document.
- **@ellissi74** (long): political will, not the document, built the Papal States.

⭐ **This is exactly C8 + C26 + C41 territory, and we have the definitive answer in BOTH directions** —
Otto III's chancery called it a forgery c. 1001 and the *palea* flagged it, **and** it was demonstrably
deployed (Leo IX 1053, the 1252 *Tractatus*, Sangiorgi, Bolognini, Steuco 1547). **Nobody in the field
answers this. The audience is asking it out loud.**

## ⭐ Second demonstrated demand: the method itself is contested by viewers

**@vmpfernandez9376 (EN):** *"All spoken languages evolve with use by the people, a more fossilized
language used only administratively doesn't have the same changes. **I think nothing of this.**"*

**A viewer independently reconstructed Steuco's counter-argument** (C15a — transmission damage, not
forgery). **So the Steuco/defence material HAS demand** — the objection arises spontaneously, and our
answer to it (C39: Steuco's own witness was copied for a Roman cardinal in 1206) is unanswerable.

📌 Also: **@MM-op6ti** — *"Funny that Bracciolini would be so skeptical, who probably forged some of the
works of Cicero"* — the **forger-catches-forger irony has demand**, which is C34c (Bolognini).
📌 **@-GTN- (IT):** *"Cioè Niccolò Cusano è stato il primo debunker?"* — Cusa's priority gets noticed.

## ⚠ The emotional engine, and the trap

The dominant register is **anticlerical grievance**: *"no institution has such a long tradition of
creating fake news"* (28 likes) · *"funny the forgery was made by the same organisation that told us
children not to lie"* (9) · *"that's where the Church's wealth comes from"*. Plus *"should be taught
in schools"* (25).

⛔ **Our C26 finding cuts directly against that register** — nobody suppressed the treatise, the Church
conceded it, the Index listing is 1559. **That is the honest finding and it will disappoint the
audience the topic attracts.** Decide deliberately: this channel's identity is the honest reading, but
it costs the easiest engagement lever on the topic.

⚠ **English-specific trap:** the top English thread (9 likes, 7 replies) is denominational boundary
policing — *"that was the papacy, not the true Church"*, *"repentance is necessary for healing the
Schism."* Expect Catholic/Orthodox/Protestant fighting. **Polidoro's pinned-comment tactic
(COMPETITOR-GAP-ANALYSIS §3) is the mitigation.**

## REVISED TITLE DIRECTION

Move from the **undemanded** reversal toward the **demonstrated** question. Needs scoring + `/curiosity`:

- *"The Popes Cited a Forgery Their Own Clerks Had Flagged."* — the live question, actor+verb ⚠ verify against C8/C8a before use
- *"Historians Say Nobody Believed It. The Records Say They Used It Anyway."* — states the comment-thread argument, then overturns it
- *"He Proved It Was Fake in 1440. Rome Had Known Since 1001."* — the C8 beat, two dates, concrete ⚠ "known" overclaims; needs rewording

**Keep as A/B challenger:** *"The Vatican Hired the Man Who Exposed Its Forgery"* — no demonstrated
demand, but a genuine reversal of an expectation the audience visibly holds (they treat Valla as a
hero and assume the Church punished him). **Test it against a demand-led title rather than assuming it.**
