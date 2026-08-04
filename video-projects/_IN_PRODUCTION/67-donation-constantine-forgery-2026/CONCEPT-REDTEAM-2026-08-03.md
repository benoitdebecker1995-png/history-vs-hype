# Concept Red-Team — #67 Donation of Constantine

**Date:** 2026-08-03 · **Brief:** attack the plan; find the better video if one exists
**Data:** `analytics.db` (`videos`, `studio_ctr_rows`, `surface_ctr`, `retention_curves`,
`opener_retention`, `traffic_sources`, `search_terms`) · live vidIQ keyword + outlier queries ·
project research files
**Rule observed:** one superlative permitted in this document; it is spent in Q5.

> ## ✅ FINDING 0 INDEPENDENTLY CONFIRMED — 2026-08-04
>
> Re-run against the live `analytics.db` through `AnalyticsStore`, not hand-rolled SQL (ADR-0017):
>
> | read | table | n | median impressions | max |
> |---|---|---:|---:|---:|
> | trailing window | `analytics.db.videos.impressions` | 58 | **56** | 10,952 |
> | lifetime | `analytics.db.studio_ctr_rows.impressions` | 57 | **2,923** | 292,398 |
>
> `videos.ctr_as_of` holds exactly **two** dates — `2026-02-23` (1 video) and `2026-07-28` (57) —
> so it stamps when the snapshot was taken, not how long each video has been live. It is a window,
> and reading it as lifetime understates by **~52×**.
>
> **Therefore, and permanently:** the "56-impression median" and the "11% vs 2% bimodal shape test"
> are artifacts of the wrong column. Neither may be cited again, here or anywhere. The canonical
> reads are `AnalyticsStore.lifetime_ctr_by_video()` (how a video actually did) and
> `snapshot_ctr_by_video()` (the recent window); both stamp every row with `grain`, `as_of` and
> `source_table` so the grain cannot be lost in transit. Pinned by
> `tests/test_packaging_ctr_grain.py`; the rule is ADR-0024.
>
> The verdict below already reflects this correction — this block records the evidence for it, so
> the numbers are not re-derived from the snapshot column a third time.

---

## VERDICT (5 lines)

1. **Keep the topic. Change the packaging analysis it was built on** — the two packaging documents
   read a trailing-window column as lifetime, so the "56-impression median", the "11% vs 2% shape
   test" and the stated reason for the locked title are all artifacts. Real lifetime median: **2,923
   impressions; 16 of 57 videos over 5,000.**
2. **None of the five alternative topics beats the Donation as a lead.** Medieval forgery, Mabillon,
   the Greek transmission, Pecock and the institutions angle all return **0 estimated monthly
   searches** and carry no famous entity. The Donation owns the only recognisable proper noun in the
   research: **Constantine**.
3. **The locked title omits that noun**, and fame is this channel's one validated CTR driver
   (+2.23 on Browse). That is the single biggest reason this does 300 views.
4. **The cold open is broken as written** — the title promises a coin and the first 45 seconds
   deliver a career timeline. The channel loses **31.6 percentage points in the first 60 seconds**
   and only ~8 pp between 5:00 and 11:30.
5. **11:30 is a non-issue.** Duration↔views ρ=+0.135, duration↔CTR ρ=−0.002, and retention percentage
   ↔views ρ=+0.007. The 12-minute cap optimises the one metric on this channel that predicts nothing.

---

## STRONGEST CASE AGAINST THIS VIDEO

Stated as an opponent would state it, before I answer it.

**1. The field says the ceiling is low and the plan has no answer to that.** The best English
long-form on this topic is 4,309 views on a 70,000-subscriber channel — a 6% view/sub ratio. Five
content-farm uploads in 90 days all died under 65 views. A 515-sub channel entering a strip-mined
niche with no live hook and no tailwind is bidding for the same 4,000 views, at best, and the honest
base rate is the 115 views that `Medieval Europe's Hidden Literacy Boom` got on 7,475 impressions.

**2. The moat is a distinction nobody asked for.** The declared differentiator is *two men, two
methods* — Cusa tested the record, Valla tested the words. Across ~80 comment threads mined on the
two highest-signal videos in this topic, **zero** raised it. The project's own comment mine recorded
that. The four reversals are similarly unrequested: nobody is asking whether the *defence* was
doctored, because nobody knew there was a defence.

**3. The plan is a research artefact wearing a video's clothes.** ~86 tracked claims, eleven months
of sourcing energy, and the structure uses fifteen of them across four turns in 690 seconds. Four
reversals in eleven minutes is one every 170 seconds — less setup per reversal than the channel's own
data says the audience needs, and the plan's justification for the density is that competitors
*cannot copy it*, which is a claim about the competition, not about the viewer.

**4. It ships alone.** Every isolated upload in this catalogue died; the two clustered ones are the
only videos above 1,967 views. The siblings are seeds in a research file. `SCRIPT.md` is 85 bytes.

**5. And the honest finding disappoints the audience the topic attracts.** C26 — nobody suppressed
it, the Index listing is 1559 — cuts directly against the anticlerical grievance that drives every
comment section in this space. The plan flags this and then does not solve it.

**What survives of that case:** points 3, 4 and 5 are correct and are addressed in the
recommendations below. **What does not survive:** point 1 rests on the same trailing-window column as
the rest of the packaging analysis (see Finding 0), and point 2 is right about the diagnosis and
wrong about the cure — the demanded question *is* answerable from this research, it is just not the
spine.

---

## ⛔ FINDING 0 — THE ANALYSIS THIS PLAN RESTS ON USED THE WRONG COLUMN

Everything else is downstream of this, so it goes first.

`BREAKOUT-VERDICT-2026-08-03.md` and `PACKAGING-AND-STRUCTURE-2026-08-03.md` are built on
`videos.impressions` / `videos.ctr_percent`. **Those are trailing-window snapshots, not lifetime.**
`videos.ctr_as_of` holds exactly two values — `2026-07-28` and `2026-02-23`. For a mostly dormant back
catalogue that is a ~28-day window: it measures how much YouTube served a 2025 video *last month*.

The lifetime truth is `studio_ctr_rows` (July-23 Studio lifetime export, 57 videos), which
`PACKAGING_MANDATE.md` itself names "the freshest CTR truth."

| | `videos.*` (window) | `studio_ctr_rows` (lifetime) |
|---|---:|---:|
| Median impressions | **56** | **2,923** |
| Videos ≥5,000 impressions | **1** | **16** |
| Guatemala breakout | 3,915 @ 11.03% | **292,398 @ 7.66%** |
| Guatemala sequel | 1,558 @ 11.42% | 44,295 @ 9.18% |
| KGB | 594 @ 11.62% | **4,760 @ 7.90%** |
| Venezuela–Guyana | 17 @ 5.88% | 36,263 @ 4.30% |
| Turkey / 152 Islands | 55 @ 7.27% | 22,034 @ 3.20% |
| Brazil | 145 @ 0.69% | 19,894 @ 3.12% |
| Berlin Conference | 55 @ 0.00% | 9,485 @ 3.66% |

The one video where the two agree is `Israel vs Palestine. The 1947 UN Plan…` (10,952 vs 10,925) —
because it published 2026-07-05, so its lifetime *is* its trailing window. That coincidence is what
made the broken column look credible.

**Three consequences, each of which overturns something the plan treats as settled:**

1. ⛔ **"Median impressions 56 / only 1 video of 58 ever exceeded 5,000 / impressions are the binding
   constraint" is false.** Sixteen videos cleared 5,000 lifetime impressions; five cleared 20,000.
   YouTube tests this channel routinely. The tests fail on the **click**, not on the serve. That is a
   different problem with a different fix, and it means script and structure work is not futile —
   it means the title/thumbnail pair is carrying the whole load, exactly as the mandate's Gate-2
   model says.
2. ⛔ **The "11% vs 2% bimodal shape test" does not exist in lifetime data.** Lifetime CTR runs
   continuously from 0.46% to 9.41% with no gap. The actor+verb-vs-proposition doctrine in
   `PACKAGING-AND-STRUCTURE` was fitted to five small trailing windows. It should be dropped, not
   downgraded — and note the mandate had already told you so: *"[CONFIRMED, null, n=56] No topic
   FORMULA in the data."*
3. ⛔ **The stated justification for the locked title is wrong on its own terms.** *"How a Coin
   Exposed a Vatican Forgery"* was locked because *"the channel's only `How…` title is its best CTR
   (11.6%)."* KGB's lifetime CTR is **7.90%**, and it is not the channel's best — `JD Vance Claims
   Christians Found Child Sacrifice` is **9.41%** and the Guatemala sequel is **9.18%**. The title
   may still be defensible; the evidence offered for it is not evidence.

📌 The KGB video's real distinguishing feature is in `traffic_sources`, and the plan missed it:
**377 of its 596 views came from `YT_SEARCH`** — people typing `operation sig` (48 views in
`search_terms`). Its 5.37% subs-per-view came from **search intent on a named entity**, not from the
word "How". The plan copied the syntax and dropped the mechanism.

---

## Q1 — Is the Donation of Constantine even the right topic?

**Answer: yes, and none of the five alternatives comes close. But the reason it survives is fame, not
gap.**

### The alternatives, measured

vidIQ keyword research, `country=US`:

| Anchor | Est. monthly | Verdict |
|---|---:|---|
| **donation of constantine** | **3,412** | passes V1 GO (≥1,000) |
| lorenzo valla | 3,654 | ⚠ related-keyword neighbourhood is *filosofia*, *epicuro*, *fondazione* — Italian/Spanish student search, not UK/DE/CA/US |
| constantine the great | 8,149 | famous parent, right shape |
| papal states | 3,946 | |
| **medieval forgery** | **0** | |
| **historical forgery** | **0** | |
| **fake medieval document** | **0** | |
| **textual criticism history** | **0** | |
| **how do we know history is true** | **0** | |
| **donation of constantine forgery** | **0** | the compound phrase has no volume; the bare entity does |

- **Mabillon vs Papebroch (the birth of document forensics).** Zero volume on every phrasing tested,
  no famous entity, and `C21` in the research file records that **Mabillon does not mention Valla or
  the Donation** — so the lineage that would make it a natural lead does not exist. As a *lead* it is
  strictly worse. Keep it as a standalone, not as the flagship.
- **Pecock / English heresy trials.** No fame, no volume. Its value is the fate-inversion *inside*
  #67 (C20a), which is where the plan already puts it.
- **Greek/Byzantine transmission (C24, C38, C41).** Load-bearing behind the Quirini beat; on screen
  it is a stemma lecture. The plan is right to cut it to one sentence.
- **Sociology of institutions knowingly using fake documents.** No anchor at all — this is a thesis,
  not a topic. But see Q5: it is the *spine* the video should have, delivered through the Donation.

### Does the channel actually get punished for going medieval?

Testable, and the answer is no. Cohort of 11 pre-modern / myth-bust videos (no living state party)
vs the other 46, lifetime CTR:

| | median lifetime CTR |
|---|---:|
| Pre-modern cohort (n=11) | **2.29%** |
| Everything else (n=46) | **2.59%** |

A 0.3 pp gap on n=11 is not a penalty. And the cohort contains a working existence proof:
**`Primary Sources Destroy the 'Awesome Crusades' Narrative` — 10,036 lifetime impressions, 5.47%
CTR, 698 views, 604 of them from the home feed.** A pre-modern, method-first, primary-source-framed
video pulled a Browse push on this channel. That is the closest structural precedent #67 has, and it
is a good one.

The counter-example in the same cohort is the warning: **`Medieval Europe's Hidden Literacy Boom` —
7,475 impressions, 1.11% CTR, 115 views.** Served plenty. Nobody clicked. The difference between
5.47% and 1.11% is not era. It is that one title contains *Crusades* and the other contains
*Medieval Europe's Hidden Literacy Boom*.

### The live-field check

An outlier sweep (`how historians prove a document is fake forgery`, long-form, 12 months) returned
**no medieval-forgery cluster at all** — true crime, election news, woodworking. Nothing in this
space is being pushed. That confirms the earlier finding and it cuts both ways: no competition, and
no tailwind.

📌 One live signal worth recording, from a `Vatican / pope / medieval church` outlier sweep
(3 months, <400K subs, >20K views): **`Why Is the Vatican a Country?` — Sankofa, 1,130 subscribers,
34,932 views, 7:03, breakout score 790.** A nano-channel cleared 35K views on the Vatican's temporal
sovereignty in the last quarter. The Donation of Constantine *is* the origin document of that
question, and the plan does not connect to it anywhere. Also: **Pope Leo XIV is generating steady
volume right now** (EWTN, network news in the same sweep) — a live V1 hook the project has not
claimed.

⚠ **Unverified, and it matters:** vidIQ returned an empty `topMarkets` array for both
`donation of constantine` and `lorenzo valla`, so **I could not confirm the geography of this topic's
demand.** By contrast `shroud of turin` (100,602/mo) returns **US 18.2%, GB 9.1%** — the channel's
exact audience. The adjacent-shelf saturation that `COMPETITOR-GAP-ANALYSIS` §4 recorded as a
negative is, on the mandate's own fame rule, the demand signal. **The Shroud is not in this
research** and cannot be this video; it belongs on the next-topic list.

---

## Q2 — Is the cold open right?

**Answer: no, and the defect is mechanical rather than aesthetic — the locked title and the locked
cold open are describing two different videos.**

### The mismatch

`PACKAGING-AND-STRUCTURE` §SCRIPT STRUCTURE, row one: **0:00–0:45 = "COLD OPEN — deliver the title"**,
content = *1440 he proves it fake / 1448 apostolic scriptor / 1456 papal secretary*. The coin is
row two, **0:45–2:00**.

That structure was written when the title was *"The Vatican Hired the Man Who Exposed Its Forgery."*
The title was later changed to *"How a Coin Exposed a Vatican Forgery"* — and the structure was never
moved. The document's own correction section then states: *"On an 11:30 runtime that seam is
0:35–1:10. ✅ The structure already puts the coin there."* **It does not.** At 0:35 the viewer is
hearing about papal appointments in 1448.

### What the retention data says that costs

Pooled `retention_curves` for all 58 videos, bucketed by **absolute elapsed seconds** (median
`audience_watch_ratio`):

| elapsed | median retained | Δ |
|---|---:|---:|
| 0:00 | 76.4% | — |
| 0:30 | 53.0% | **−23.4 pp** |
| 1:00 | 44.8% | **−8.2 pp** |
| 1:30 | 40.6% | −4.3 |
| 2:00 | 37.3% | −3.3 |
| 3:00 | 33.3% | −1.3 |
| 5:00 | 27.0% | −0.1 |
| 8:00 | 22.4% | −0.9 |
| 11:30 | 18.6% | +0.9 |

**31.6 percentage points leave in the first sixty seconds. The whole stretch from 5:00 to 11:30 costs
8.4 pp.** A title promise delivered at 0:45 is delivered to roughly two-thirds of the people who saw
it delivered at 0:05.

### Which of the four candidates

`opener_retention` (n=21) ranks first-30s retention. Top: **0.715** — *"Open a map of Central America,
you see Belize…"* (a concrete instruction) and **0.713** — *"March 1st, 2025, 7am, a Venezuelan
warship sails within 700 meters…"* (a dated physical scene). Bottom: **0.511** — *"No, Ukraine isn't
fake. Hi, my name is Benoît. I make videos about history…"* (self-introduction).

Against that:

| Candidate | Verdict |
|---|---|
| ⭐ **The coin** | **Take it.** It is the only candidate that is a physical object at second zero, it is the one the locked title promises, and it converts an abstract philological claim into a thing you can hold. Same move as the two best-holding openers on the channel. |
| **Fate inversion (Pecock destroyed, Valla promoted)** | Best *challenger*: two people and a consequence, no Latin required, and it is the shape that holds. But it does not deliver the coin title — so it is only viable if the title moves with it. |
| **The doctored defence (Quirini/Steuco)** | ⛔ No. It needs ~90 seconds of setup — who Quirini is, what he deleted, why deletion convicts — before it lands. Spending it at 0:00 burns the payoff before the audience can price it. It is correctly placed at 6:00. |
| **Otto III, DO III 389** | ⛔ No, for a reason the project already documented: the production-readiness check lists it as **"NOT HELD — audio-only claim; nothing to show."** A cold open with no exhibit, on a channel whose whole product is exhibits, and whose actor is "a chancery." Excellent as the 4:30 reversal; unusable at 0:00. |

**The binding recommendation is not "coin vs inversion." It is: pick one and make the title and the
first ten seconds the same object.** The current plan's split is a defect regardless of which side
you resolve it to.

---

## Q3 — Is 11:30 right?

**Answer: it is fine, and the 12-minute cap is optimising a metric that predicts nothing on this
channel. Derived from the data, not assumed.**

n=57 long-form, lifetime figures:

| relationship | Pearson | Spearman |
|---|---:|---:|
| duration ↔ avg_view_**percentage** | **−0.511** | −0.373 |
| duration ↔ avg_view_**seconds** | **+0.535** | +0.543 |
| duration ↔ lifetime impressions | — | +0.148 |
| duration ↔ views | — | +0.135 |
| duration ↔ CTR | — | −0.002 |
| **avg_view_percentage ↔ views** | — | **+0.007** |
| avg_view_percentage ↔ impressions | — | −0.001 |
| impressions ↔ views | — | **+0.885** |
| CTR ↔ views | — | +0.544 |

The CLAUDE.md cap cites r=−0.455 on duration↔retention; I reproduce **−0.511** on n=57, so the
correlation is real. But it is a correlation with **percentage**, and percentage correlates with
views at **+0.007** and with impressions at **−0.001**. Absolute watch seconds — the thing YouTube
actually banks — goes **up** with duration (+0.535). This matches the mandate's own
*"[CONFIRMED, null, n=47] Length is not a lever in 5–13 min."*

Duration bands (median):

| band | n | AVP | AVD sec | views | lifetime impr |
|---|---:|---:|---:|---:|---:|
| 3:20–8:00 | 10 | 32.0% | 118 | 54 | 1,782 |
| 8:00–10:00 | 9 | 29.8% | 169 | 104 | 2,889 |
| 10:00–11:00 | 15 | 30.4% | 193 | 125 | 3,478 |
| **11:00–12:00** | 12 | 27.3% | 186 | 116 | 3,396 |
| 12:00+ | 11 | 25.4% | 210 | 77 | 1,474 |

The 12:00+ band's lower views are confounded — that band is Iran, Flat Earth, Armenia, the weak
topics — so I will not use it to defend the cap. `Why The Sol Invictus Story Is Completely Wrong`
runs **14:39** and posts 51.8% retention at 60 seconds and the channel's second-best subscriber
conversion (3.12%/view).

**Conclusion: 11:30 costs nothing and buys nothing. Cutting good material to reach 12:00 would be a
net loss; the cap should be treated as a soft convention, not a constraint on this script.** Runtime
is not on the list of things that determine this video's outcome.

---

## Q4 — The single biggest reason this does 300 views instead of 30,000

**The title spends all 36 of its characters on an unnamed object and an abstract category, and omits
the one famous proper noun this research owns: *Constantine*.**

*"How a Coin Exposed a Vatican Forgery."* The concrete nouns are **a coin** (not famous, not
searched, no prior opinion attached) and **a Vatican forgery** (a category, not a thing).

Why that is the binding failure, in order of evidence strength:

1. **Fame is this channel's only validated CTR driver.** `PACKAGING_MANDATE`, n=56:
   *"FAME is the #1 validated CTR driver: +0.87 blended, +2.23 on Browse (famous-topic Browse CTR
   5.65% vs 3.41%)"* — and *"packaging only pays once the topic is famous."* Browse+Suggested is
   **33,445 + 6,976 lifetime views** against **3,294** from search, so this is a feed judgement made
   in under a second by someone who has never heard of Lorenzo Valla.
2. **The channel's own catalogue separates on recognition, not on era or syntax.** Crusades: 5.47%
   CTR, 698 views. Medieval Literacy Boom: 1.11% CTR, 115 views — on a *comparable* 7,475 impressions.
   Sol Invictus and Piri Reis are proper nouns almost nobody knows: 2.48% and 3.85%, 224 and 156
   views. Recognisable entity in the title is the line these fall on.
3. **The demand that exists is attached to the exact phrase the title drops.**
   `donation of constantine` = 3,412/mo; the compound `donation of constantine forgery` = **0**.
   People search the entity, not the charge. And `search_terms` shows this channel's search traffic
   is almost purely exact proper nouns — `belize` 84, `operation sig` 48, `armenian genocide` 35,
   `guatemala history` 25, `treaty of tripoli` 23, `nick fuentes` 20, `benny morris` 7,
   `graham hancock` 6, `ervand abrahamian` 6 — corroborating the mandate's
   *"[CONFIRMED concentration] Search demand is entity-led."*
4. **"Vatican" does not fix it.** 100,602/mo, but top markets **VN, BR, PK, ES, HU** against a
   UK/DE/CA/US audience. It passes `has_search_anchor` and still points at the wrong continent.
   📌 The plan already noticed the recognizer is unreliable here — it records that the 30,540-view
   breakout **fails** the same gate.

**Runner-up cause, and it is close:** the video ships alone. See Q5.

**Not the cause:** research depth, retention, runtime, or the reversal structure. Retention↔views is
+0.007. Nothing in the script moves distribution.

---

## Q5 — Is there a cluster play?

**Yes, and it is the strongest quantitative result in this document.**

`surface_ctr`, all videos with ≥1,500 Suggested impressions (n=24):

| | median Suggested CTR |
|---|---:|
| The three border-dispute cluster members (Guatemala ×2, Venezuela–Guyana) | **4.15%** |
| The other 21 | **1.12%** |

Individually: Guatemala sequel **7.31%**, Guatemala breakout **4.15%**, Venezuela–Guyana **3.96%**.
Against isolated uploads: Medieval Literacy **0.75%**, Trade Wars **0.80%**, Sol Invictus **0.77%**,
Spanish Inquisition **0.76%**, Vichy **0.97%**, Soviet Union **0.56%**. A **3.7× median split** on
the surface that a topic like #67 must live on, since it has no country name to ride Browse with.

**And the window is narrow.** The three that worked published **2025-10-19 → 2025-12-04** (six weeks).
The fourth and fifth family members — Honduras/Sapodilla (2026-03-30) and Nigeria vs Cameroon
(2026-04-16) — arrived four months late and never cleared 1,500 Suggested impressions at all:
508 and 669 lifetime impressions, 53 and 20 views. **A sibling shipped a quarter later is not a
cluster.**

### The two best siblings

Judged on the thing that actually produces Suggested adjacency — **shared entities**, not shared
themes.

1. ⭐ **"Who Actually Forged It" (C8 + C35a + Fried).** Shares every entity with #67: Constantine, the
   Donation, the papacy, the same 3,412/mo search term. Maximum adjacency. The research file already
   designed the handoff — *"#67 ends where this one begins."* It also answers Levine's unanswered
   question (C20b), so it is intellectually load-bearing rather than a spin-off.
2. ⭐ **"The Man Who Argued for the Forgery Became Pope" (C27, Pius II).** Shares the entity, adds a
   named human, and delivers the C27 finding — *a forgery exposed is not a claim withdrawn.* This is
   the one thing the comment mine documented as **live audience demand** (four independent commenters
   on the topic's best-performing video arguing about whether the document was ever believed or used).

⛔ **Correction to the research file's own ranking: Mabillon vs Papebroch is the worst cluster
candidate, not the best.** The file rates it ⭐ first among the CLUSTER SEEDS. It shares **no entity**
with #67 — different century, different documents, different people, zero overlapping search terms —
so YouTube has nothing to suggest it *on*. It is a fine standalone and a poor sibling. The seeds
should be re-ranked by entity overlap.

**Should a sibling lead instead?** No. #67 holds the famous entity; both siblings inherit their
recognisability from it. Lead with #67 and ship sibling 1 within four weeks.

---

## Q6 — What would RealLifeLore, Kraut or Wendover do with this research?

All three converge on one cut, and it is the cut the plan will resist most.

**They would all reduce four reversals to one.** The plan's declared moat is four turns — nobody
suppressed it / the defence was doctored / Steuco published the evidence against himself / Pecock was
destroyed for defending the Church. Four reversals in eleven minutes means none of them gets the
sixty seconds of setup that makes a reversal land, and the viewer stops updating after the second.

**RealLifeLore** would not make this video as scoped — there is no map and no living stakes. If
forced, he leads present-tense with the consequence: *the Vatican is a sovereign state, and the
document that started that claim is a fake.* He cuts Cusa, Quirini, Steuco, Pecock and every Latin
word, keeps Constantine and the Pope, and spends the runtime on the Papal States as territory. 📌 The
evidence that this framing works on this shelf right now is `Why Is the Vatican a Country?` —
**1,130 subs, 34,932 views in the last three months.**

**Kraut** keeps the historiography, which is why he is the closest fit, but he leads with the
*method* as thesis rather than as an exhibit: **C19a — Valla's own metaphor, that we tell counterfeit
coins apart, so why not counterfeit doctrine.** That sentence is currently a throwaway at 2:00; Kraut
opens on it and the whole video becomes an argument about how you catch a liar. He cuts Pecock and
the Greek transmission entirely, and he keeps Steuco — a serious, wrong opponent is his signature.
He would also refuse to cut at 12:00.

**Wendover** deletes every papal-politics beat and turns it into a procedure: *how do you prove a
document is fake?* Step 1 the object (the coin), step 2 the words that don't belong, step 3 the
witness that turns out to be a copy. The Donation becomes the worked example, and the video closes on
the general rule. He leads with the coin — which is the single point on which all three agree with
the locked title and against the locked cold open.

---

## THE BETTER VIDEO, IF THERE IS ONE

There is not a different *topic* hiding in this research. There is a better *video* on the same
topic, and it differs in three decisions.

### Title (direction, needs `/curiosity` + `title_scorer` + live SERP before locking)

> **"Constantine's Own Coins Say the Pope Never Ruled Rome"** — 51 chars

- Restores **Constantine** (8,149/mo) and sits adjacent to the exact demanded phrase
  (`donation of constantine`, 3,412/mo). Fame is the only validated CTR lever this channel has.
- Keeps the coin — so the thumbnail brief, the cleared CC BY-SA solidus and the 0:00 exhibit all
  survive unchanged.
- Names three things a stranger already has an opinion about: Constantine, the Pope, Rome.
- Nothing like the farm signature (`[N] years` + `forged document`), and nothing like the fifteen
  competitors, who all title the *charge*.
- ⚠ **Fact-check before use:** Valla's coin argument establishes *no papal coinage exists, therefore
  no papal rule* (C19). "Say" is the honest verb; **"prove" would overclaim** under the graded-claim
  rule. Check against C19/C19a and the `CONCORDIA ORBIS` caveat the project already flagged.

### Cold open — the coin, in shot, before second ten

Physical object first, argument second. It matches the two best-holding openers on the channel, it
delivers the title inside the window where 31.6 pp of the audience is decided, and it is the one beat
with a cleared, on-disk exhibit at 0:00. The 1440/1448/1456 career timeline moves to ~9:00, where the
plan already answers it.

### Spine — C27, not "two men, two methods"

Replace the thesis *two men caught one forgery by testing it against two different worlds* with
**C27: a forgery exposed is not a claim withdrawn.** Enea Silvio Piccolomini argued *for* the
Donation in 1436, absorbed the disproof, became Pope Pius II, and re-founded papal temporal rule on
other grounds — Setz, verbatim: the recognition that it is a forgery *"has no further consequences."*

Why this beats the plan's spine:

1. **It is the answer to the only demand the project actually measured.** The comment mine found four
   independent commenters on the topic's best-performing video arguing about whether the document was
   ever believed or used. The plan buries that at 4:30–6:00 and gives the spine to Cusa-vs-Valla —
   a distinction internal to historiography that **no commenter in either mined video raised.**
2. **It survives the intellectual-honesty problem the plan flagged and did not solve.** The plan notes
   that C26 (nobody suppressed it) *"will disappoint the audience the topic attracts."* Under the C27
   spine that finding stops being a disappointment and becomes the point: the Church did not need to
   suppress it, because exposure changed nothing.
3. **It makes the four reversals into one argument instead of four surprises** — which is the cut all
   three comparison creators would make, arrived at from a different direction.
4. **It is the sibling bridge.** C27 is sibling 2; the dating video is sibling 1. The spine is the
   cluster.

### Cost

**Rewrite of the structure table and a new title test set. No new research** — C19, C27, C22, C39,
C20a are all filed and the exhibits for all but Otto III and Steuco's own colophon are on disk.
`SCRIPT.md` is 85 bytes, so nothing is being thrown away.

### Ranked recommendations

| # | Recommendation | Expected impact | Cost |
|---|---|---|---|
| 1 | **Re-derive the packaging analysis from `studio_ctr_rows`, not `videos.impressions`.** Retire the "11%/2% shape test" and the "56-impression median" framing wherever they appear. | Highest — three locked decisions rest on the artifact, and it will corrupt every future video until fixed | ~1 hour of re-analysis; invalidates two documents' conclusions, not their research |
| 2 | **Put a famous proper noun back in the title.** Constantine, ideally with Rome or the Pope. | High — fame is the only validated CTR driver, n=56 | Free. One title-generation pass |
| 3 | **Resolve the title/cold-open split.** Coin in the title ⇒ coin on screen before 0:10. | High — 31.6 pp decided in 60 seconds | Free at this stage; expensive after filming |
| 4 | **Commit to shipping sibling 1 within four weeks of #67.** | High — 4.15% vs 1.12% median Suggested CTR (n=24), and the effect expires | One extra production cycle; research already exists |
| 5 | **Switch the spine to C27.** | Medium-high — converts the honest-but-disappointing finding into the payoff, and matches measured comment demand | Half a day of restructuring |
| 6 | **Cut to one reversal-with-setup; demote the rest to supporting evidence.** | Medium — retention, and retention does not move views. Do it for the comments and the likes | Structural, ~2 hours |
| 7 | **Stop treating 12:00 as a cap for this script.** | Low but free — removes a constraint that buys nothing | Free |
| 8 | **Log the Shroud of Turin as the next-topic candidate** (100,602/mo, US 18.2% + GB 9.1%). Not this video; not in this research. | Unscored — outside this project | New research cycle |

---

## WHAT I'D KEEP

- **The topic.** It survived every attack I could make on it. The alternatives are demonstrably worse.
- **The coin as lead exhibit and thumbnail object.** Correct on the data (`document-as-focal-object`
  is measurably negative; a coin reads at 60 px) and correct on the argument.
- **C22 — Quirini deleted the words Valla convicted, then dedicated the result to the Pope.** With
  `Setz p. 119` rendered and visually verified, this is the one card in the video that nobody in any
  language has. It stays at 6:00.
- **C39 — Steuco printing the colophon that dates his own "ancient witness" to 1206.**
- **The honesty beat (C14d / C32a)** — Camporeale, Valla's admirer, making the case against him.
  Non-negotiable for the channel's identity and it is the thing the field never does.
- **The early CTA at ~4:30**, justified as subscriber conversion and explicitly *not* as a
  distribution move. The plan's own correction on this is right.
- **The revised thumbnail test — three concepts, not three overlays.** The reasoning ("find something
  that works before attributing why") is correct at this stage.
- **The farm-signature ban.** `[N] years` + `forged document` stays banned.
- **The attribute-never-assert rule on `CONCORDIA ORBIS`.** Good catch, correctly handled.
- **The three-lever title test** (mechanism / reversal / stakes) rather than three phrasings.

---

## CONFIDENCE AND LIMITS

**High confidence:**
- Finding 0. `videos.impressions` vs `studio_ctr_rows` is a direct comparison of two columns in the
  same database, reproducible in one query, and `videos.ctr_as_of` explains the mechanism.
- The retention-by-absolute-time curve. 5,800 curve rows, 58 videos.
- The duration correlations. n=57, and they agree with the mandate's independent n=47 result.

**Medium confidence:**
- The cluster split (4.15% vs 1.12%). n=24 with only **3** videos in the treatment group, and it is
  **confounded with fame** — Guatemala and Venezuela were also the famous topics. The effect is large
  enough that I believe it; the size is not trustworthy.
- The pre-modern-cohort null (2.29% vs 2.59%). n=11. A null on a small sample cannot rule out a
  modest real penalty.
- The C27-spine recommendation. It rests on the comment mine's n≈80 threads on two videos, which is
  demand evidence for *engagement*, not for *clicks* — a distinction the packaging document itself
  drew correctly.

**Low confidence / unverified:**
- ⚠ **The geography of this topic's demand.** vidIQ returned an empty `topMarkets` for both
  `donation of constantine` and `lorenzo valla`. I could not confirm whether the 3,412/mo is
  UK/DE/CA/US or Italian/Spanish. Valla's related-keyword neighbourhood suggests the latter. **This
  is an unresolved risk in the greenlight and it should be checked before filming.**
- `surface_ctr` is a Feb-2026 legacy export with no reader or writer in `tools/`, missing #59. I used
  it only for the Browse/Suggested split, which it uniquely holds. Directional.
- `studio_ctr_rows` is a single lifetime export dated 2026-07-23; anything published after is absent.
- vidIQ volume figures are estimates from one query on one day.
- I did **not** verify the C-numbered research claims. I took the research file's own status tags at
  face value. Nothing in this document should be read as a fact-check of the history.
- I did not run `title_scorer` or `/curiosity` on the proposed title, and note that on this channel
  the scorer's grade has been shown to carry no predictive power (r=−0.053 on the plan's own
  measurement). Record the number, ignore the grade.
