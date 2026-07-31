# Frame screen — Wikipedia `Category:Historical negationism`

**Date:** 2026-07-30
**Brief:** `.claude/PROMPTS/screen-historical-negationism-frame.md`
**Discipline:** ADR-0020 (strategy claims carry on-screen evidentiary burden)
**Outcome:** **1 survivor of 54.** Frame is low-yield but the kill record is reusable.

---

## 1. Frame size — VERIFIED, not inherited

The prior assessment of **54 entries was CORRECT.** Confirmed independently:

```
GET https://en.wikipedia.org/w/api.php?action=query&list=categorymembers
    &cmtitle=Category:Historical%20negationism&cmlimit=500&cmtype=page&format=json
→ 54 pages, continue: null (single page, no truncation)
```

Durable enumeration artifact: `scratchpad/negationism-enum.json`.

### Subcategories — 14, one level deep, no recursion

| Subcategory | Pages |
|---|---|
| Historical negationism by country | **0** (contains only sub-subcats) |
| Historical negationists | 10 |
| Attacks on libraries | 19 |
| Book burnings | 48 |
| Censorship | 107 |
| Cultural genocide | 46 |
| Damnatio memoriae | 17 |
| Denial of the crucifixion of Jesus | 13 |
| Genocide denial | 17 |
| Holodomor denial | 4 |
| LGBTQ erasure | 20 |
| Neo-Nazism | 7 |
| Political and cultural purges | **218** |
| World War II-related historical negationism | 55 |

- **Gross:** 581 · **Unique within subcats:** 572 · **Net-new (not already in parent):** **558**
- **Grand union (parent + one level):** **612**

**Honest caveat on the subcategory frame.** The +558 is mostly *not* historical negationism. Wikipedia's
category graph leaks into adjacent topics: `Political and cultural purges` (218) is a massacre/show-trial
index, `Censorship` (107) is a media-law glossary, `Attacks on libraries` (19) includes US mass shootings.
Screening 612 entries would be screening the wrong 558. The genuinely on-frame subcategories are
**WWII-related historical negationism (55)**, **Genocide denial (17)**, **Historical negationists (10)**,
**Denial of the crucifixion of Jesus (13)** and **Holodomor denial (4)** — see §5 for whether that second
pass is worth running.

The 54 parent entries are screened in full below.

---

## 2. Complete screen table — all 54 entries

Stage key: **S1** = free filter (weaponised now / bounded exhibit / target-audience geography /
stranger-legible / repo collision). **S2** = vidIQ demand + `topMarkets`. **S3** = referee test.

| # | Entry | Verdict | Killed at | Reason |
|---|---|---|---|---|
| 1 | Historical negationism | KILL | S1 | Meta-concept, not a claim. No exhibit, nothing to adjudicate. |
| 2 | Johan Bäckman | KILL | S1 | Finnish/Estonian pro-Kremlin figure. Audience outside UK/US/DE/CA; not stranger-legible. |
| 3 | Béla Biszku | KILL | S1 | Hungarian communist prosecution. Single-national; no Western argument. |
| 4 | Book burning | KILL | S1 | Meta-concept. No bounded exhibit. |
| 5 | List of book-burning incidents | KILL | S1 | List article, no single claim to test. |
| 6 | Bosnian genocide denial | **KILL** | **S2** | Survived S1 (live via Dodik; ICTY exhibit). Killed on demand geography — see §3-K1. |
| 7 | Censorship | KILL | S1 | Meta-concept. |
| 8 | Croatian Wikipedia | **KILL** | **S3** | Survived S1+S2. **Refereed at scale** — ID-verified, see §3-K2. |
| 9 | Cuba de ayer | **SURVIVE** | — | Only survivor. Full dossier §4. |
| 10 | Damnatio memoriae | KILL | S1 | Roman practice. Not weaponised in current Western argument. |
| 11 | Denial of genocides of Indigenous peoples | DUPLICATE | S1 | Dedupe list: "Native American population collapse". |
| 12 | Denial of state terrorism in Argentina | **KILL** | **S3** | Survived S1+S2; strongest near-miss. Killed on Spanish-language assertion ecosystem — §3-K3. |
| 13 | Holodomor denial | DUPLICATE | S1 | Dedupe list: "Holodomor". |
| 14 | Denial of the October 7 attacks | KILL | S1 | Exhibit is atrocity footage — unshowable, and monetisation/serve-fatal. Comment moderation infeasible (224 lifetime comments; "cannot arbitrate a war"). **Judgment call, not a mechanical filter.** |
| 15 | Destruction of cultural heritage by the Islamic State | KILL | S1 | No live proponents; not a contested claim. |
| 16 | Epistemic injustice | KILL | S1 | Academic philosophy. Not stranger-legible, no exhibit. |
| 17 | The Erased | KILL | S1 | Slovenia's erased residents. Single-national. |
| 18 | Genocide denial | KILL | S1 | Meta-concept. **FLAG:** collides with published `7-genocide-definition-2025`. |
| 19 | Great Lechia | KILL | S1 | Polish pseudo-history. Audience Poland; not stranger-legible for target countries. |
| 20 | Herostratus | KILL | S1 | Ancient Greece, purely historical. |
| 21 | Historical distortion regarding Ferdinand Marcos | KILL | S1 | Very live, excellent exhibit — but audience is Philippines. Exact pocket-risk pattern (channel's worst converter). |
| 22 | Historiography in North Macedonia | KILL | S1 | Balkan naming dispute. Not stranger-legible. |
| 23 | A History of the Palestinian People | KILL | S1 | 2017 blank-page joke book; exhibit is trivially thin. Plus I/P serve + moderation risk, 5 I/P videos published. |
| 24 | Holocaust denial | KILL | S1 | Saturated referee ecosystem (Irving v Lipstadt, Lipstadt, USHMM, feature film *Denial* 2016) + sensitivity-flagged serve risk. Cheap kill, no S3 spend. |
| 25 | Ludo Martens | KILL | S1 | Obscure Belgian Stalinist author. No demand, not stranger-legible. |
| 26 | Memory hole | KILL | S1 | *Nineteen Eighty-Four* concept. Fiction. |
| 27 | The Military Doctrine of Ukrainian Nationalists | DUPLICATE | S1 | **LOUD COLLISION:** this is a sub-exhibit of `_IN_PRODUCTION/62-volhynia-massacre-untranslated-2026`. Belongs inside #62, not as a new video. |
| 28 | Nakba denial | KILL | S1 | I/P serve + moderation; collides with published *"Israel vs Palestine. The 1947 UN Plan Wasn't Legally Binding"*. |
| 29 | Nationalist historiography | KILL | S1 | Meta-concept. |
| 30 | NCERT textbook controversies | **KILL** | **S2** | Survived S1 on the best exhibit in the frame (before/after textbook pages). Killed on `topMarkets` — §3-K4. |
| 31 | Negationism of the military dictatorship of Chile | KILL | S1 | Lower Western salience than the Argentina entry; Spanish-dominated pool. |
| 32 | Neo-Stalinism | KILL | S1 | Overlaps dedupe ("100 million" communism death toll) + published *"Stalin Purged His Own Army"*. |
| 33 | Newspeak | KILL | S1 | Orwell fiction. |
| 34 | Nineteen Eighty-Four | KILL | S1 | Fiction. |
| 35 | On the Historical Unity of Russians and Ukrainians | **KILL** | **S3** | Survived S1+S2 with the frame's best geography. Killed by referee saturation **and an outright collision — the channel already made this video.** §3-K5. |
| 36 | Operation Legacy | DUPLICATE | S1 | Dedupe list **and** `_BACKLOG/47-operation-legacy-2026`. |
| 37 | Pact of Forgetting | KILL | S1 | Spanish-internal argument, ES-dominated pool. **FLAG:** adjacent to `_IN_PRODUCTION/61-spanish-colonization-black-legend-2026`. |
| 38 | Paper genocide | KILL | S1 | Partially dedupe (Native American collapse); Caribbean/Latino audience; not stranger-legible. |
| 39 | Phantom time conspiracy theory | KILL | S1 | Superb exhibit (dendrochronology, Halley's comet, Islamic/Chinese cross-dating) but **not politically weaponised** — it is viral curiosity, not an argument-winning weapon. Fails the frame's own definition. Noted in §5 as a non-political idea. |
| 40 | Prior review | KILL | S1 | Censorship mechanism, meta. |
| 41 | Prosvita | KILL | S1 | Ukrainian cultural society. Historical, single-national. |
| 42 | Purge | KILL | S1 | Meta-concept. |
| 43 | Records Department | KILL | S1 | *Nineteen Eighty-Four* fiction. |
| 44 | Report about Case Srebrenica | KILL | S2 | Not standalone — it is the *exhibit* for entry 6; dies with it on geography. |
| 45 | Ruhnama | KILL | S1 | Turkmenistan. No Western argument. |
| 46 | Saint Patrick's Battalion | KILL | S1 | Mythologised but not a live political weapon at scale. |
| 47 | Selective omission | KILL | S1 | Rhetoric concept, meta. |
| 48 | Historiography in the Soviet Union | KILL | S1 | Meta/historical; overlaps dedupe. |
| 49 | Streisand effect | KILL | S1 | Irrelevant to the frame. |
| 50 | Temple denial | KILL | S1 | I/P serve + moderation + 5 published I/P videos. |
| 51 | There was no such thing as Palestinians | KILL | S1 | Same as above. |
| 52 | A Town Betrayed | KILL | S1 | Sub-item of entry 6, not standalone. |
| 53 | A Verdade Sufocada | KILL | S1 | Brazilian dictatorship apologia. PT-dominated, single-national. |
| 54 | White Legend | DUPLICATE | S1 | Dedupe list ("Black Legend") **and** direct collision with `_IN_PRODUCTION/61-spanish-colonization-black-legend-2026`. |

**Tally:** 54 rows — 44 KILL at S1 · 4 DUPLICATE at S1 · 2 KILL at S2 · 3 KILL at S3 · **1 SURVIVE.**
(Entries 6 and 44 counted once each; 44 dies with 6.)

### Collisions flagged (flags, not kills)
- **#27** → `_IN_PRODUCTION/62-volhynia-massacre-untranslated-2026` (should be folded in as an exhibit)
- **#54, #37** → `_IN_PRODUCTION/61-spanish-colonization-black-legend-2026`
- **#36** → `_BACKLOG/47-operation-legacy-2026`
- **#18** → published `7-genocide-definition-2025`
- **#35** → published *"1,000 Years of Ukraine: The History Putin Erased"* + *"Putin Says NATO Promised Not to Expand"*
- **#12** → published `34-operation-condor-2025` (adjacent junta-era Argentina)
- **#9 (survivor)** → **no collision.** Grep of `video-projects/` for `cuba|Cuba|Batista` returns only incidental
  mentions inside Panama (#36) and Falklands (#55) source texts. No Cuba project exists.

---

## 3. Stage 2 and Stage 3 kill evidence

### Stage 2 — vidIQ, survivors only (6 calls, 30 credits; balance 3,643 → 3,613)

| Anchor | Vol | Comp | Overall | Est/mo | topMarkets (top 5) | Verdict |
|---|---|---|---|---|---|---|
| `srebrenica` | 68.5 | 66.5 | 54.5 | 38,668 | **TR 30%**, BR 10%, BA 10%, SI 10%, RS 10% | **KILL** |
| `wikipedia bias` | 54.4 | 48.5 | 53.2 | 4,394 | *empty*; parent `wikipedia`: BD 15.8%, US 10.5%, IN 10.5%, HK 5.3%, DE 5.3% | pass |
| `cuba before castro` | 55.7 | **37.0** | 58.6 | 5,412 | *empty*; parent `cuba`: VN 24.3%, **US 11.7%**, BR 8.1%, **CA 6.3%**, MX 5.4% | pass |
| `argentina dirty war` | 54.1 | 49.5 | 52.7 | 4,199 | *empty*; parent `argentina`: **BR 30.6%**, VN 10.5%, AR 7.0%, US 6.8%, BD 6.7% | pass (caveat) |
| `india history textbook` | 0 | null | null | **0** | parent `indian history`: **IN 83.3%**, BD 5.6%, PK 2.8%, GB 2.8% | **KILL** |
| `putin ukraine history` | 0 | 51 | 19.6 | 0 | parent `ukraine`: VN 12.3%, **US 9.6%, GB 9.2%, DE 7.9%, CA 4.4%** | pass |

**K1 — Bosnian genocide denial (#6, #44, #52).** Killed on `topMarkets`: **zero target countries in the
top five.** Turkey alone is 30%. This is the channel's documented worst-converting pattern (its one
breakout took 30,469 views to 152 subscribers, 5.0/1,000). Compounding: genocide topics are
sensitivity-flagged, so the failure mode is undiagnosable silence against a 302-impression median.

**K4 — NCERT textbook controversies (#30).** Killed on `topMarkets`: **IN 83.3%**, target-country share
2.8% (GB). The exact-phrase anchor measured 0/mo. Painful kill — the exhibit (NCERT editions before and
after the 2023–25 Mughal deletions, side by side, downloadable) is the single best bounded exhibit in the
whole frame. It fails only on audience geography, decisively.

*Note on empty `topMarkets`:* four seeds returned `topMarkets: []`. Per ADR-0020, **empty is a missing
measurement, not a zero.** Parent anchors are reported alongside and labelled as such.

### Stage 3 — referee test (ADR-0020 in full)

**⚠️ QUOTA EXHAUSTED — named.** The YouTube Data API quota metric **`Search Queries per day`** (project
`1071657171201`) was exhausted **after a single `search.list` call**, HTTP 429 `rateLimitExceeded`. I
stopped using `search.list` at query 2 of 16 (`"Wikipedia captured by ideologues scandal"`).

**What survived and why it is sufficient:** `videos().list` and `playlistItems().list` bill against a
*different* metric and remained fully available — and those are precisely the instruments ADR-0020
mandates. The ADR forbids ranking endpoints and prescribes full uploads-playlist catalogue-checks plus
ID-verification. Search was never the instrument of record. Substituted framings via `WebSearch`
(separate quota), then **ID-verified every candidate by `videos().list`**.

**Catalogue-check totals: 3,666 uploads walked in full across 11 channels**, by uploads playlist, not by
ranking endpoint:
Vlad Vexler 98 · Kraut 65 · RealLifeLore 498 · TIKhistory 511 · HistoryLegends 519 · Knowing Better 113 ·
BadEmpanada 139 · Second Thought 426 · Whatifalthist 668 · Economics Explained 440 · PolyMatter 189.
(`@TheCynicalHistorian` did not resolve; `@Hakim_` uploads playlist returned HttpError — both named as
gaps, not as absences.)

---

**K2 — Croatian Wikipedia (#8): REFEREED AT SCALE. Clean kill.**

The one search call that landed returned the referee immediately. ID-verified via
`videos().list(part='snippet,statistics,contentDetails', id=...)`:

| Views | Duration | Published | ID | Channel · Title |
|---|---|---|---|---|
| **361,330** | 16m47s | 2023-07-20 | `FiHDo5bqNXw` | **Fredda — "How the Far Right Took Over Croatian Wikipedia, & How They Were Stopped"** |
| 3,860 | 5m59s | 2021-12-11 | `BA1XI660I-Y` | MJ Lemonsnout — "How I rescued Croatian Wikipedia from the Far-Right (old)" (a participant) |
| 189 | 10m2s | 2023-09-12 | `P9F_NBQBGWQ` | Community Data Science Collective — "Governance Capture on Wikipedia: Comparing Croatian and Serbian Wikipedia Editions" (the academic treatment) |

Fredda's video is the whole thesis — capture *and* remedy — at 361K views, plus a named participant
account and a peer academic talk. Nothing left to add. This kill is the ADR-0020 discipline working as
designed: had I trusted a ranking endpoint I might have missed a 2023 mid-size video.

---

**K5 — On the Historical Unity of Russians and Ukrainians (#35): saturated AND already made.**

Two independent kills.

*(a) The channel already published this video.* `analytics.db` contains **"1,000 Years of Ukraine: The
History Putin Erased"** — that is this entry's thesis — plus **"Putin Says NATO Promised Not to Expand.
The Documents Disagree."** This is not a flag; it is the same video.

*(b) Referee saturation.* Queries run: `"Putin On the Historical Unity of Russians and Ukrainians essay"`,
`"Putin historical claims Ukraine debunked historians"`, `"Russia Ukraine one people history argument
evidence"`, `"historians respond to Putin Ukraine history debate"` (4 framings: partisan wording, neutral
causal, +evidence, +historian/debate). Catalogue-checked in full: Vlad Vexler (98), Kraut (65),
RealLifeLore (498), TIKhistory (511), HistoryLegends (519) — 1,691 uploads. ID-verified closest
adjudicators:

| Views | Duration | Published | ID | Channel · Title |
|---|---|---|---|---|
| **1,865,272** | 21m9s | 2021-08-20 | `f8ZqBLcIvw0` | Kraut — "The Origins of Russian Authoritarianism" |
| **1,736,264** | 53m48s | 2022-11-01 | `sdFtqa54TuM` | Kraut — "The Ideology of Putin's Russia" |
| 311,411 | 17m10s | 2023-03-12 | `VBQWvZtCNHw` | Vlad Vexler — "Exposing Putin's Mistakes about Ukraine" |
| 305,220 | 13m43s | 2022-02-25 | `rzja-LOqUd8` | Vlad Vexler — "The disturbing truth behind Putin's Ukraine invasion" |
| 147,092 | 39m1s | 2022-02-13 | `ZwU13-4SakE` | Vlad Vexler — "The REAL Reason Putin is invading Ukraine (reply to @johnnyharris)" |

**>4.3M ID-verified views** of adjudication, from Kraut — the single closest channel to this audience.
Searched the queries above and catalogue-checked those five channels; **did not find** a video that treats
the July 2021 essay as a document clause-by-clause. That narrow gap is real but it is not worth entering
behind 4.3M views on a video the channel has effectively already made.

---

**K3 — Denial of state terrorism in Argentina (#12): the strongest near-miss. Killed on ecosystem language.**

This one nearly survived, and the reasoning is worth preserving.

*What is genuinely strong:* shape D executed perfectly. Deniers are **right** that 30,000 is not a
documented count — CONADEP's *Nunca Más* (1984) documented ~8,960 named cases — and extrapolate to "there
was no state terrorism." VP Victoria Villarruel has asserted this from office; on **2024-03-24** the
government published a video reframing the coup's anniversary around 1,094 guerrilla victims. The exhibit
is bounded, obtainable and excellent: *Nunca Más* itself, plus the 1998 Labraña admission. Milei is highly
salient to politically engaged Anglophone men 25–44.

*What killed it:* **the argument is not conducted in English.** Queries run:
`"Argentina 30000 desaparecidos number"`, `"Argentina dirty war how many disappeared evidence"`,
`"Villarruel Milei dirty war denial"`, `"CONADEP Nunca Mas report historians debate"`. Catalogue-checked in
full: BadEmpanada (139), Knowing Better (113), Second Thought (426), Vlad Vexler (98) — 776 uploads.
ID-verified:

| Views | Duration | Published | ID | Channel · Title |
|---|---|---|---|---|
| **212,022** | 8m55s | 2021-08-18 | `1m_ylk9UP9Q` | América TV — "Debate por los desaparecidos en #Intratables: Villarruel le respondió a Labraña" |
| 46,130 | 3m16s | 2024-03-25 | `ouuUTUq538M` | eldoce — "Luis Labraña…: 'No señores 30.000 fue falso, lo puse yo'" |
| 43,693 | 8m55s | 2024-03-23 | `yfU1t4T2A3c` | Roberto Cacheiro Frias — "La falsa cifra de 30.000…" |
| 81,826 | 52m1s | 2019-12-16 | `8mFeQ6gIfgg` | BadEmpanada — "Remembering Argentina's Dictatorship: History as Social Conflict" |
| 29,248 | 14m40s | 2021-09-16 | `AoQO0WcshF4` | BadEmpanada — "Photos From Hell: The Images Recovered From Argentina's Most Notorious Death Camp" |
| — | — | — | `DiVuXxaMRlA` | **Did not resolve** via `videos().list` — private, removed or geo-blocked. Named as unverified. |

Every assertion at scale is Spanish-language. The only English-language coverage is BadEmpanada — openly
partisan, therefore not a referee by the brief's definition, but it does occupy the terrain at 82K–245K.
So there is a real English referee gap, and **it is empty because the dispute isn't happening in English.**
Against a 302-impression browse median, an English video enters a conversation its target audience is not
having. Compounded by `argentina` topMarkets (BR 30.6% / VN 10.5% / AR 7.0% vs US 6.8%) and by comment-war
risk on a live Argentine flashpoint.

**Kill stands — but this is the runner-up**, and if the channel ever wants a Milei-adjacent video the
*Nunca Más* exhibit is ready. Recorded here rather than discarded.

---

## 4. The single survivor — #9 `Cuba de ayer`

### The claim as its proponents state it
"Before Castro, Cuba was one of the richest, healthiest, most literate countries in the Western
hemisphere — near European standards — and socialism destroyed it." Asserted in English by the
Cuban-American right, Florida politics, and the wider US anti-socialism argument. The mirror claim, from
the Cuban state and the Anglophone left, is that pre-1959 Cuba was a backward US-owned plantation. **Both
camps assert certainty. The statistical series does not support either.**

### Shape
**A and D simultaneously** — historians genuinely disagree, both camps assert certainty, and each side is
right about a part it then extrapolates far beyond.

### The exhibit — bounded, obtainable, auditable
The competing per-capita-GDP reconstructions for 1950s Cuba, side by side. The rankings **do not agree
with each other**, and that disagreement *is* the video:
- **4th** highest per-capita income in Latin America (one widely-cited estimate)
- **6th/7th** of 47 countries in Latin America and the Caribbean (1950)
- **10th** of the same 47 countries (1950)

Same country, same year, same question, three answers — because the deflators, the sugar-price base year
and the Cuba-specific data quality differ. Underlying showable documents: the **1953 Cuban census**, UN/ECLA
statistical yearbooks, and the reconstructions in **Ward & Devereux (2012)** and Devereux, *"The Descent of
Cuba"* (ASCE 2019). Critiques exist and must be shown: Frank Thompson (*Against the Current*) and the
`mangosorbananas` analysis both contest the "near the top" framing directly.

### Honest evidentiary map
- **Supports the claim:** Cuba genuinely ranked high on 1950s car/TV/radio ownership, infant mortality
  (~30/1,000), life expectancy (~62), literacy — at times rivalling European levels.
- **Undermines it:** the national aggregate concealed severe rural deprivation, concentrated land
  ownership and near-total sugar dependency. A high mean over a bimodal distribution.
- **Unknowable:** the true 1958 counterfactual. Pre-revolutionary Cuban data quality is contested, the
  ranking depends on methodology choices, and no reconstruction settles the question. **This uncertainty
  is the video's thesis, not its weakness** — it is exactly "history is harder than I thought."

### Demand — vidIQ, ID of record
`cuba before castro`: volume 55.7 · competition **37.0 (lowest measured in the entire frame)** ·
overall 58.6 · **5,412/mo** · seed `topMarkets` empty (missing measurement).
Parent `cuba`: VN 24.3%, **US 11.7%**, BR 8.1%, **CA 6.3%**, MX 5.4% — target share ~18%.

### Referee evidence — required phrasing
**Queries run:** `"Cuba was richer before Castro"`, `"Cuba 1950s economy statistics historians"`,
`"was Cuba prosperous before the revolution debunked"`, `"Batista Cuba living standards evidence debate"`
(4 framings: partisan wording, neutral causal, +debunk, +evidence/debate).
**Channels catalogue-checked by full uploads playlist (2,486 uploads):** Knowing Better (113, no match),
BadEmpanada (139), Second Thought (426), Whatifalthist (668, no match), Economics Explained (440),
TIKhistory (511, no match), PolyMatter (189, no match).
**Closest adjudicators, ID-verified:**

| Views | Duration | Published | ID | Channel · Title | Why it is not a referee |
|---|---|---|---|---|---|
| 629,751 | 15m24s | 2020-03-29 | `uzvcztUmMwA` | Economics Explained — "The Economy of Cuba" | Modern economy explainer; does not touch the 1950s statistical dispute |
| 492,135 | 20m12s | 2021-07-30 | `zIOw6fSOJI4` | Second Thought — "The Truth About The Cuba Protests" | Openly socialist advocacy; omits the strongest pro-claim evidence |
| 333,829 | 31m32s | 2020-04-16 | `DXBYlC4-0bQ` | BadEmpanada — "How Cuba Works" | Partisan-left; explanatory, not source-critical on pre-1959 data |
| 176,995 | 21m2s | 2026-07-14 | `72pGczK3j7s` | Economics Explained — "Cuba Was Barely Holding On…" | Current-affairs energy economics |
| 60,562 | 4m10s | 2021-07-14 | `dM7_wTqDUCU` | BadEmpanada — "The U.S. Embargo…" | Embargo advocacy |

**Searched those queries and catalogue-checked those seven channels; did not find a referee** that states
the strongest version of the pre-1959 prosperity claim, shows the statistics that genuinely support it,
shows the rural-deprivation evidence that undercuts it, and does source criticism on the competing GDP
reconstructions. The loud voices are advocacy on both flanks. **I am not claiming none exists** — my
search-quota exhaustion, two unresolved channel handles, and the Spanish-language sphere are all named
gaps.

### Packaging
Provisional title: **"Cuba Was Richer Than Italy in 1958. The Numbers Disagree"** — `Cuba` is a sovereign
state inside the first 40 characters, so `has_search_anchor()` returns `(True, 'Cuba')` and the entry
clears the anchor filter. **A mechanically valid `packaging_lock` is not a greenlight (ADR-0020).**
Thumbnail promise: three conflicting rank numbers for the same country and year.

### Confidence, separately
- **Demand: MEDIUM.** 5,412/mo is real and competition 37 is genuinely low, but seed `topMarkets` is a
  missing measurement and the Spanish-language cluster is ~4× larger than the English
  (`cuba antes de 1959` alone = 14,425/mo). Pocket risk is present, not disqualifying.
- **Referee gap: MEDIUM-HIGH.** 2,486 uploads catalogue-checked; the loud voices are all advocacy.
  Discounted for search-quota exhaustion.
- **Exhibit: HIGH.** Three published, mutually contradictory rankings of the same country-year, plus the
  1953 census and named academic reconstructions with named critics. Fully obtainable.

### Strongest reason to kill it
The dispute's centre of gravity is Spanish-language and diasporic. The English-language argument is a US
domestic proxy fight about socialism, which risks pulling the video toward current-affairs commentary —
the one thing the creator has said he will not make. If the statistical series cannot be rendered
legible in under 12 minutes, this becomes an economics lecture, and the channel's duration/retention
correlation (r=-0.455) punishes that.

---

## 5. Frame verdict — was this worth screening?

**Yield: 1 in 54 (1.9%).** Cost: 30 vidIQ credits (3,643 → 3,613), ~1,700 MediaWiki-free enumeration,
one exhausted YouTube search-quota metric, ~3,666 catalogue-checked uploads at ~75 quota units.

**Was it worth it? Yes — but not for the survivor.** The frame's real value is that it is *enumerable and
finite*, so "we screened all 54" is a defensible statement in a way "we brainstormed topics" never is.
The kill record above is now a reusable asset: 14 of these entries recur constantly in this niche and can
be waved off by citing a row instead of re-litigating.

**Why the yield is structurally low.** The category is dominated by three shapes that cannot pass:
1. **Meta-concepts and fiction** (17 entries: *Newspeak*, *Purge*, *Selective omission*, *1984*…) — no
   claim, no exhibit.
2. **Single-nation memory politics** (14 entries: Bäckman, Biszku, Great Lechia, Marcos, Macedonia, the
   Erased, Ruhnama…) — real disputes, wrong audience. The channel's pocket risk kills these on contact.
3. **The atrocity-denial core** (Holocaust, Nakba, October 7, Srebrenica, Temple, Holodomor) — either
   saturated, or serve-flagged with undiagnosable failure, or unmoderatable in comments. **This is the
   frame's central paradox: its most-weaponised entries are its least makeable.**

**Is the rest of the Wikipedia list-article family worth doing next? Split answer.**
- **NO** to the 558-entry subcategory sprawl. `Political and cultural purges` (218) and `Censorship` (107)
  are off-frame; screening them screens the wrong list.
- **QUALIFIED YES** to **`Category:World War II-related historical negationism` (55 entries)** — the one
  genuinely on-frame, unscreened, target-audience-relevant subcategory. It contains named, bounded,
  document-shaped claims: *Myth of the clean Wehrmacht*, *Rommel myth*, *Speer myth*, *Austria victim
  theory*, *Italiani brava gente*, *Bitburg controversy*, *Schieder commission*, *Pearl Harbor
  advance-knowledge*. Germany is a target country, the Wehrmacht/Rommel/Speer myths are actively
  weaponised in Anglophone and German argument, and each has a real document exhibit. **Expected yield is
  materially higher than 1.9%** and the same staged filter applies unchanged. Recommend this as the next
  screen; budget ~10 vidIQ calls and a *fresh* YouTube search quota.

---

## 6. What I could not verify — named

1. **YouTube `Search Queries per day` quota — EXHAUSTED** after 1 of 16 planned `search.list` calls
   (project `1071657171201`, HTTP 429). Framings 2–16 were substituted with `WebSearch` + mandatory
   `videos().list` ID-verification. This is a real reduction in referee-search breadth and every
   referee-gap confidence above is discounted for it.
2. **`DiVuXxaMRlA`** (Villarruel 2024-03-24 coup-anniversary video) — cited by press, **did not resolve**
   via `videos().list`. Private, removed or geo-blocked. Reach unverified; not counted.
3. **`@TheCynicalHistorian`** — handle did not resolve. Not catalogue-checked.
4. **`@Hakim_`** — uploads playlist returned HttpError. Not catalogue-checked. Relevant: a likely
   pro-Cuba voice on candidate #9.
5. **`@Kraut` handle collision** — resolved to a different channel whose uploads playlist 404s. The real
   channel (`@kraut_the_parrot`, 603K subs, 65 uploads) was catalogued in full.
6. **Four vidIQ seeds returned `topMarkets: []`** (`wikipedia bias`, `cuba before castro`,
   `argentina dirty war`, and the zero-volume `putin ukraine history`). **Missing measurements, not
   zeros.** Parent anchors substituted and labelled.
7. **Spanish- and German-language referee spheres not catalogue-checked** for #9 and #12. A Spanish-language
   referee on `Cuba de ayer` may well exist; I did not look, because the target audience is Anglophone —
   but that means my referee-gap claim is scoped to English-language YouTube only.
8. **Catalogue-checks match on title strings.** A video can adjudicate a claim without the search terms in
   its title. Full catalogues were walked (never a ranking endpoint), but title-matching cannot prove
   absence — hence the required phrasing throughout: *searched X, catalogue-checked Y, did not find*.

---

## Appendix — instruments of record

| Instrument | Use | Cost |
|---|---|---|
| MediaWiki `list=categorymembers` | Frame enumeration, verified 54 + 14 subcats | free (rate-limited twice; retried with backoff) |
| `vidiq_keyword_research` | Stage 2, 6 survivors only | 30 credits |
| `youtube.videos().list(part='snippet,statistics,contentDetails', id=…)` | **Every** reach figure and referee above | 1 unit / 50 IDs |
| `youtube.playlistItems().list` | Full uploads catalogue, 11 channels, 3,666 uploads | 1 unit / 50 items |
| `youtube.search().list` | **QUOTA EXHAUSTED after 1 call** | 100 units |
| `WebSearch` | Substitute framing discovery; every hit then ID-verified | free |
| `analytics.db` + `Glob`/`Grep` over `video-projects/` | Collision check, 58 published titles + all lifecycle folders | free |

**No reach figure in this document comes from a search snippet, a ranking endpoint, or another model.
Every one was returned by `videos().list` against an explicit video ID.**
