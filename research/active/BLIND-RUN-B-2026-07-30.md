# BLIND next-video discovery — RUN B

**Date:** 2026-07-30
**Brief:** `.claude/PROMPTS/blind-next-video-discovery.md`
**Discipline:** ADR-0020 (`docs/adr/0020-strategy-claims-carry-the-same-evidentiary-burden-as-on-screen-claims.md`)
**Generation angle (assigned):** start from the **evidence**, not the claim. Work outward from bounded,
auditable exhibits — contested quantitative estimates resting on one model, single texts carrying an
ideological load, forensic results used to settle what they cannot settle.

**Delivered:** 2 candidates. 9 killed. Rejection log at the end.

---

## Instruments used, and what each cannot tell you

| Instrument | Used for | Known blindness (declared per ADR-0020) |
|---|---|---|
| `youtube.videos().list(part=snippet,statistics,contentDetails, id=…)` | **every** reach figure below | none material — exact, 1 quota unit |
| `youtube.playlistItems().list` over the **full uploads playlist** | catalogue-checks | complete per channel; does not cover channels not checked |
| `youtube.search().list` (order=viewCount, relevanceLanguage=en) | finding candidate referees | ranking endpoint; **cannot establish absence**. Quota `Search Queries per day` **exhausted mid-run** — noted per candidate where it limited framings |
| `vidiq_keyword_research` | volume / competition / topMarkets | `estimatedMonthlySearch: 0` recurs on long-tail phrasings; treated as **no measurement**, never as zero demand |
| `vidiq_youtube_search` | attempted referee search | **returned `{"results":[]}` on 3 separate queries.** Its emptiness means nothing. Discarded. |
| `WebSearch` (allowed_domains youtube.com) | recovering candidate IDs after search quota died | every recovered ID was then **verified by `videos().list`** |

**No negative claim in this document appears without its instrument named beside it.**

---

# CANDIDATE 1 — "The 100 Million": the arithmetic behind communism's death toll

### 1. The claim as its proponents state it

> "Communism killed 100 million people in the twentieth century."

Load-bearing sub-claim: **"Mao killed 45 million in the Great Leap Forward"** (Frank Dikötter,
*Mao's Great Famine*, 2010 — "worked, starved or beaten to death").

The 100 million originates in Stéphane Courtois's introduction to *Le Livre noir du communisme*
(1997), which sums country-by-country subtotals — China ~65M, USSR ~20M — into a single headline.

### 2. Why this creator would obsess over it

It is the purest available specimen of his own stated project. Three exhibits, all bounded:

- **A book's own authors repudiating its headline number.** Nicolas Werth (who wrote roughly a third
  of the *Black Book*) and Jean-Louis Margolin (160+ pages on East Asia) rebuked Courtois in
  *Le Monde* in 1997 over the introduction, objected that he was driving toward a round hundred
  million, and **tried to withdraw their contributions entirely — abandoning it only when their
  lawyers said it could not be done.** Verified across the Wikipedia article on the *Black Book*,
  Jacobin (Jan 2025), and the peer-reviewed reception study in *Revue d'études comparatives
  Est-Ouest* 2020/2 (Cairn.info). **Flagged for Phase-2 NotebookLM verification: the exact Le Monde
  date and wording must be pinned before it goes on screen.**
- **One survey generating a factor-of-three range.** Every Great Leap Forward estimate descends from
  the same instrument: the **1982 One-per-Thousand Fertility Survey** (Chinese State Family Planning
  Commission — retrospective birth histories from a nationally representative sample of **310,101
  women aged 15–67**), read against the 1953 / 1964 / 1982 censuses. From that one instrument:
  **Coale ≈ 16.5M · Banister ≈ 30M · Dikötter 45M.** The spread is not produced by new evidence. It
  is produced by **what each author assumes the death rate would have been without the famine.**
  (Reported baselines: official 1960 rate 25.4/1000; Coale raised to ≈39; Banister to 44.6 —
  **these three specific baseline figures came from partisan secondary sites and are NOT yet
  verified; they must be taken from Coale 1984 and Banister 1987 directly.**)
- **A famine economist's published objection.** Cormac Ó Gráda, *"Great Leap into Famine: A Review
  Essay"*, **Population and Development Review 37(1), 2011** (Wiley): Dikötter's assumed normal
  mortality of 10 per thousand is **"implausibly low"** and operates to maximise the count; the book
  is "more like a catalogue of anecdotes about atrocities than a sustained analytic argument."

This is Shape **C** (one dataset carrying an entire ideological argument) fused with Shape **D**
(proponents right that the catastrophe was vast and policy-caused, extrapolating to a precision the
instrument cannot bear).

### 3. Who asserts it now — ID-verified reach

| ID | Views | Dur | Date | Channel / title |
|---|---|---|---|---|
| `SIGwVeWfXg0` | 4,916,055 | 0:59 | 2021-12-10 | The Mind Forge — Which Dictator Killed The Most People |
| `MDgoBoa8JR0` | 252,845 | 31:37 | 2024-04-24 | Henry Stewart History — Why Communism So Often Ends in Starvation |
| `i8x_0dXoaxU` | 163,173 | 9:39 | 2021-08-02 | China in Focus / NTD — How communism killed 80 million in China |
| `KuZICSrDkv8` | 62,711 | 0:59 | 2021-07-17 | China in Focus / NTD — same claim, short |
| `7yaPUL-oGjI` | 46,486 | 1:09 | 2016-10-12 | Victims of Communism Memorial Foundation — 100 Years, 100 Million Killed |
| `xX-QuoWWsi8` | 40,920 | 8:53 | 2017-11-08 | The Daily Wire — Communist Lies Killed 100 Million People |
| `M9YG8NwA2EE` | 3,809 | 1:10 | 2019-09-25 | Breitbart — Trump Reminds U.N.: Socialism, Communism Killed 100 Million |

Living political figures in the chain: Trump (UNGA 2019, on the record and still recirculating —
`csz-iZVZPbo`, 2026-07-07, Italian repost), the Daily Wire, the Victims of Communism Memorial
Foundation, and — on the rebuttal side — Musk, Peterson and Shapiro named by name in
`qOQqVXzgt2g` (17,266, 2025-03-18).

### 4. Why the target audience cares

This is *the* number in Anglophone online political argument. The channel's verified subscriber
overlap is political-commentary channels, not history hobbyists — and this figure is the
load-bearing statistic on one side of that entire ecosystem, with the counter-figure ("capitalism
killed more") load-bearing on the other. Both sides quote a number neither has audited.

### 5. Demand evidence (vidIQ, 2026-07-30)

| Keyword | Est. monthly | Competition | US countryVolume | topMarkets |
|---|---|---|---|---|
| communism | 47,568 | 56.5 | **25,370** | **US 53.3% · IN 13.3% · GB 13.3% · CZ 6.7% · IT 6.7%** |
| mao zedong | 64,046 | 54.5 | 15,249 | US 23.8% · VN 9.5% · ID 9.5% · PL 9.5% · IN 9.5% |
| chinese history | 72,070 | 45.0 | 21,020 | VN 31.8% · US 27.3% · SG 13.6% |
| great leap forward | 7,266 | 49.0 | — | (no data) |
| great chinese famine | 4,424 | **26.0** | — | (no data) |
| what is communism | 18,620 | 32.4 | — | (no data) |

**`communism`'s topMarkets is the best target-market profile measured anywhere in this run** —
66.6% US+GB, versus the ww2/empire cluster's PK/VN/IN skew. `great chinese famine` at competition 26
is the low-competition entry point. Long-tail phrasings ("how many people did communism kill",
"great leap forward famine death toll") returned `estimatedMonthlySearch: 0` — **treated as no
measurement, not as zero demand.**

### 6. Referee-gap evidence

**Queries run** (`youtube.search().list`, order=viewCount, relevanceLanguage=en, 2026-07-30) — four
framings including the partisan wording proponents use:
1. `how many people did communism kill 100 million` *(proponent wording)*
2. `black book of communism death toll criticism` *(source-critical wording)*
3. `great leap forward death toll historians estimates` *(neutral + historian)*
4. `mao famine 45 million dikotter evidence` *(neutral + evidence)*

**Channels catalogue-checked by FULL uploads playlist** (`playlistItems`, not a ranking endpoint;
grep `communis|100 million|death toll|\bmao\b|famine|leap forward|holodomor|black book`):

| Channel | Subs | Uploads walked | Relevant hits |
|---|---|---|---|
| Second Thought `UCJm2TgUqtK1_NLBrjNQ1P-w` | 1.91M | 426 | **0** (2 false positives) |
| Historia Civilis `UCv_vLHiWVBh_FR9vbeuiY-A` | 1.09M | 89 | **0** |
| Kraut `UCr_Q-bPpcw5fJ-Oow1BW1NQ` | 603K | 65 | **0** |
| TIKhistory `UCfZz8F37oSJ2rtcEJHM2kCg` | 428K | 511 | **0** (1 hit: "Hitler was a Communist in early 1919") |
| The Cynical Historian `UCN5mhhJYPcNUKBMZkR5Nfzg` | 319K | 472 | **0** |
| BadEmpanada `UCUzmizB92LJ9oxf5T_snZNA` | 206K | 139 | 4 hits — Holodomor ×2, Bengal ×1, Gaza ×1; **none on the 100 million** |

**Closest adjudicators, ID-verified:**

| ID | Views | Dur | Date | Channel / title | What it fails to do |
|---|---|---|---|---|---|
| `rIB4e8AfPcM` | 213,799 | 17:08 | 2025-06-30 | Hakim — The Death Toll of Capitalism (and the 100 million lie) | Self-identified Marxist-Leninist. Counter-accounting, not source criticism. Does not audit the instrument; substitutes a rival body count |
| `Q5LMxXC8qWg` | 182,861 | 52:44 | 2021-10-19 | Balkan Odyssey — Capitalism killed (at least) 3.4 billion people | Mirror-image partisan escalation |
| `wflMmNTXqKk` | 133,949 | 21:39 | 2019-12-29 | Viki1999 — The REAL death toll of communism | Video essay, conclusion-forward |
| `EyCGVhbfLDc` | 105,387 | 16:35 | 2024-09-27 | overzealots — Black Book of Neoliberalism | Parody-inversion of the book, not an audit of it |
| `4RIFgoVNVUQ` | **12,993** | 49:32 | 2020-10-27 | The Young Hegelian — How Many People Did Communism Kill? Breaking Down The Numbers | **Closest to a genuine adjudication in the entire field — and it reached 12,993 people.** Channel framing is explicitly left-Hegelian |

**Searched those four framings and catalogue-checked those six channels; did not find a referee.**
Specifically: **searched and catalogue-checked as above and found no video that (a) names the 1982
One-per-Thousand Fertility Survey, (b) shows the 16.5M–45M range is produced by a baseline
assumption rather than by evidence, (c) quotes Werth's and Margolin's repudiation, or (d) engages
Ó Gráda's *Population and Development Review* review.** The adjudication ecosystem is ~648K views of
*partisan rebuttal*; the assertion ecosystem is millions. The one attempt at genuine arithmetic got
13K.

### 7. The exhibit, and whether it is obtainable

Three, layered, all obtainable:
1. **Courtois's introduction** to *The Black Book of Communism* (Harvard UP 1999 English ed.) — the
   page where the subtotals are summed. Buy the book. On-screen: the actual page.
2. **Werth and Margolin's *Le Monde* rebuke (1997)** — needs archive retrieval; *Le Monde* archive or
   a library database. **Obtainability: MEDIUM. This is the single riskiest exhibit and must be
   secured before greenlight.**
3. **Coale (1984) and Banister (1987)** baseline tables + the 1982 One-per-Thousand Survey
   description, and **Ó Gráda, PDR 37(1) 2011** (Wiley — obtainable). Obtainability: HIGH.

### 8. Honest evidentiary map

**Supports the proponents** — the Great Leap famine was catastrophic and policy-caused; tens of
millions died; the provincial archives Dikötter worked in are real and are damning about local
violence and coercion; post-1991 Soviet archival work has *confirmed* very large Gulag and Terror
figures that Cold-War-era leftists denied.

**Undermines them** — the 100 million has no single instrument behind it; it is an addition of
heterogeneous subtotals produced by incompatible methods, and two of the three principal
contributors publicly rejected the total. The 45M sits at the ceiling of a 16.5–45M range whose
spread is a modelling choice.

**Unknowable** — the counterfactual mortality baseline for China 1958–62. There is no
non-catastrophic China to measure against. Also unknowable: whether famine mortality reporting was
suppressed symmetrically across provinces, which sets a floor on how precise any reconstruction can
ever be.

### 9. Specialists and works

Frank Dikötter (*Mao's Great Famine*, 2010) · Yang Jisheng (*Tombstone*) · Cao Shuji · Cormac
Ó Gráda (*Famine: A Short History*; PDR 2011 review) · Ansley Coale · Judith Banister · Nicolas
Werth · Jean-Louis Margolin · Stéphane Courtois · Stephen Wheatcroft & R.W. Davies (Soviet series).
**Real state of scholarship:** the *fact* of mass death is settled. The *magnitude* is a live,
published, methodological dispute among demographers. The public is shown a single number.

### 10. Provisional title + thumbnail, anchor filter

- `Mao Killed 45 Million. One Book Made That Number Up` → `has_search_anchor` = **(True, 'Mao')** ✅
- `China Says 15 Million Died. The West Says 45. The Data Says Neither` → **(True, 'China')** ✅
- `The 100 Million Figure Came From One Book. Two Authors Disowned It` → **(False, '')** ❌ — do not use

Thumbnail promise: the survey sample line — *310,101 women* — beside three wildly different totals.
Text overlay 2–4 words ("ONE SURVEY. THREE ANSWERS."). No face. Not territorial, so no map.

### 11. Why these viewers return for the method

The transferable skill is the highest-value one he can teach: **when someone hands you a death toll,
ask what the counterfactual baseline is.** That test works on the Holodomor, on Bengal, on Iraq
casualty counts, on COVID excess mortality — every argument this audience is already inside.

### 12. Strongest reason to kill it

**Serve plus moderation, compounding.** China-plus-communism sits adjacent to
sensitivity-flagged political categories, and the failure mode is silence he cannot diagnose against
a 302-impression median. Worse: the honest verdict — *tens of millions died and the precision is
manufactured* — reads as apologia to one camp and as concession to the other. **With 224 lifetime
comments across 28 videos he has no moderation muscle for a Marxist-versus-anticommunist brawl, and
this framing guarantees one.** That is the real risk, and it is not small.

### 13. Confidence

- **Demand: MEDIUM-HIGH.** Strong, US/GB-weighted volume on `communism`; the narrow framing is
  unmeasured (0-returns), so the anchor keyword is generic rather than specific.
- **Referee gap: HIGH.** Six full catalogues walked, four framings, every closest adjudicator
  ID-verified and every one of them partisan. This is the strongest referee-absence evidence in this
  run.
- **Exhibit: MEDIUM-HIGH.** Two of three exhibits are trivially obtainable; the *Le Monde* rebuke is
  the risk, and three baseline figures are currently sourced only to partisan secondary sites.

---

# CANDIDATE 2 — The Bengal Famine 1943: the report both camps skip

### 1. The claim as its proponents state it

> "Churchill deliberately starved three million Bengalis. It was wilful mass starvation."

And its mirror, currently the louder one in Britain:

> "The famine had nothing to do with Churchill. Saying so is a barefaced lie."

### 2. Why this creator would obsess over it

Because the adjudicating document exists, is 254 pages, is free, is in English, and **neither camp
cites it.** The **Famine Inquiry Commission, *Report on Bengal* (Government of India, May 1945)** —
Sir John Woodhead chairing — is the contemporaneous official inquiry, with the rice-availability
tables, the procurement figures and the apportionment of blame. It is a genuine referee in paper
form, and both 2026 camps argue past it.

Shape **A** (specialists genuinely disagree while both political camps assert certainty) and
Shape **B** (facts largely settled, *inference* — intent versus incompetence — contested).

### 3. Who asserts it now — names, dates, ID-verified reach

**The live flashpoint is six weeks old and it is British.** In June 2026 the National Portrait
Gallery removed Helen Cammock's commissioned 40-minute installation *Persistence*, which stated that
Cromwell "starved people, en masse, a little like the willful starvation of the Indian population by
Winston Churchill." Historian and former NPG trustee **Andrew Roberts** wrote to protest "in the
strongest possible terms," calling the accusation "foul and vile" and "a barefaced lie"; his letter
was **countersigned by more than 50 members of the House of Lords, including Churchill's grandson
Nicholas Soames.** The artist withdrew the work. (Euronews 2026-06-24; GB News; *The Independent*.)

| ID | Views | Dur | Date | Channel / title | Side |
|---|---|---|---|---|---|
| `plZkO3y9_hY` | 261,555 | 51:51 | 2020-03-31 | BadEmpanada — The Bengal Famine and Winston Churchill | prosecution (partisan) |
| `2KOw_R5s5Qc` | 207,941 | 6:08 | 2023-09-20 | Keerthi — How was Bengal Famine caused by Winston Churchill? | prosecution |
| `0ORnLUQxMHk` | 31,046 | 5:07 | 2021-06-09 | Peepul Tree World — Churchill's Death Blow | prosecution |
| `kzA8Af09p80` | 27,344 | 6:48 | 2022-12-26 | **Douglas Murray** — Winston Churchill and the Bengal Famine | defence |
| `uCN7VO7p9LI` | 8,962 | 3:38 | 2021-06-10 | Historia Maxima — Did Churchill Cause the Bengal Famine? | mixed |
| `VM_JWKT5Rhw` | 3,231 | 4:17 | 2026-06-16 | WION Gravitas — London Exhibition Proves Churchill Killed Bengalis | prosecution |
| `pFdmOf9ohAg` | 2,140 | 4:05 | 2026-06-23 | India Today Global — NPG Drops Churchill Exhibit | news |

The symmetry the brief asks for is *already built into the topic*: a living right-wing commentator
(Murray) and a living historian-peer bloc (Roberts, Soames) on one side; a commissioned artist and an
anti-imperialist left on the other. He can referee between them, and the evidence embarrasses both.

### 4. Why the target audience cares

Churchill is the single most contested figure in British public identity, and the June 2026 row put
it back in the UK press with 50 peers attached. UK is a primary target market. This is history being
used to win a live argument about national self-image — the exact trigger the brief names.

### 5. Demand evidence (vidIQ, 2026-07-30)

| Keyword | Est. monthly | Competition | topMarkets |
|---|---|---|---|
| bengal famine | 5,342 | 40.9 | (no data) |
| bengal famine 1943 | 4,941 | 31.8 | (no data) |
| bengal famine of 1943 | 4,254 | **24.1** | (no data) |
| bengal famine of 1943 documentary | 4,472 | **19.7** | (no data) |
| winston churchill | 92,940 | 59.0 | **BR 15.6% · ID 9.4% · IN 9.4% · PK 9.4% · BD 6.3%** |
| british empire | 55,887 | 54.0 | **PK 22.2% · ID 11.1% · IN 11.1% · BD 11.1% · FR 5.6%** |
| indian history | 103,138 | 40.8 | **IN 83.3%** |
| british raj | 4,596 | 51.3 | (no data) |

**Read this honestly: the specific famine keywords have decent volume at unusually low competition
(19.7–31.8), but the surrounding cluster is South-Asia-dominant.** `indian history` is 83% India;
`british empire` is 22% Pakistan; `winston churchill` has *no target country in its top five*. The
famine-specific rows returned no topMarkets data, so I cannot state their geography — but the
neighbourhood is a warning, not a reassurance.

### 6. Referee-gap evidence — **and this evidence is thinner than Candidate 1's**

**Queries run:** the YouTube `Search Queries per day` quota was **exhausted** before I reached this
candidate's framings, so I recovered candidates via `WebSearch` restricted to `youtube.com` and then
**ID-verified every one** with `videos().list`. That is a weaker instrument than four ranked
framings, and I am recording the shortfall rather than papering over it.

**Framings run (via WebSearch, youtube.com only):** `bengal famine 1943 churchill blame historians
evidence debate documentary`.
**Framings NOT run — must be run before greenlight:** partisan wording (`churchill genocide bengal`),
neutral causal (`what caused the bengal famine 1943`), and `famine inquiry commission 1945`.

**Channels catalogue-checked by FULL uploads playlist** (grep `bengal|churchill|india|empire`):

| Channel | Subs | Uploads walked | Bengal hits |
|---|---|---|---|
| BadEmpanada `UCUzmizB92LJ9oxf5T_snZNA` | 206K | 139 | 1 — `plZkO3y9_hY` |
| The Cynical Historian `UCN5mhhJYPcNUKBMZkR5Nfzg` | 319K | 472 | **0** |
| Kraut `UCr_Q-bPpcw5fJ-Oow1BW1NQ` | 603K | 65 | **0** |

**Only three channels catalogue-checked. The brief asks for 3–6. This is the floor, not the
standard.** Channels that should still be walked: Knowing Better (walked for `famine|hunger|export`
→ 0, but not for `bengal|churchill`), History Debunked, Simple History, TLDR/Empire-podcast
YouTube surfaces.

**Closest adjudicator, ID-verified:** BadEmpanada `plZkO3y9_hY`, **261,555 views, 51:51, 2020-03-31.**
This is the only long-form treatment in the field. **What it fails to do:** it is an explicitly
anti-imperialist prosecution by a self-identified communist — a partisan counter-video, which the
brief rules out as a referee. It does not steelman the Roy/Ó Gráda supply-and-provincial-failure
case, and — the decisive point — **searched and catalogue-checked as above and found no video that
puts the 1945 Famine Inquiry Commission report on screen at all.** Douglas Murray's defence
(`kzA8Af09p80`, 27,344, 6:48) doesn't cite it either.

### 7. The exhibit, and whether it is obtainable

**Obtainability: HIGH — the highest in this run.** *Famine Inquiry Commission, Report on Bengal*
(Government of India Press, May 1945, 254 pp.) is on the Internet Archive under multiple
identifiers — `dli.ministry.12773`, `in.ernet.dli.2015.206311`, `dli.ernet.26318`, `dli.csl.1036` —
plus a clean PDF at indiaofthepast.org, and a National Archives (UK) catalogue record. Public domain
Government of India publication. Screen-ready.

Supporting exhibits: War Cabinet shipping minutes (TNA); Mishra et al. 2019 *Geophysical Research
Letters* — the paper showing 1943 was **not** a drought year, now the prosecution's favourite
citation and worth interrogating on its own terms.

### 8. Honest evidentiary map

**Supports the prosecution** — Britain refused or slow-walked shipping at points during 1943; the
1943 harvest failure was not a simple drought (Mishra 2019); Churchill's private remarks about
Indians are documented and ugly; London had the legal authority to compel relief and did not use it
at the speed available.

**Supports the defence** — Tirthankar Roy: the decisive failure was the *elected Bengal provincial
government's* refusal to admit a famine existed, with Civil Supplies Minister **Suhrawardy**
maintaining throughout that there was no food shortage; interregional trade broke down for reasons
still not fully understood; and there is little evidence Churchill's personal views drove War Cabinet
policy — "the cabinet believed what Calcutta and Delhi told it: that there was no shortage of food in
Bengal." Ó Gráda adds a finding that cuts against a *left* orthodoxy: there **was** a real food
availability decline, so the historiographical focus on hoarding and speculation is misplaced.

**Unknowable** — Churchill's subjective intent. There is no document in which he wills Bengali
deaths, and the absence of such a document neither convicts nor exonerates. Also unknowable: the
death toll itself, where the Commission's ~1.5M, Sen's ~3M and Maharatna's reconstruction diverge on
the same registration data — the *same* baseline-choice problem as Candidate 1, which makes these
two candidates a natural pair rather than rivals.

### 9. Specialists and works

Tirthankar Roy (*Famines in India: Enduring Lessons*, LSE) · Cormac Ó Gráda · Amartya Sen (*Poverty
and Famines*) · Madhusree Mukerjee (*Churchill's Secret War*) · Arup Maharatna · Mishra et al. 2019
(GRL) · Andrew Roberts (defence, and a living participant) · the Woodhead Commission itself.
**Real state of scholarship:** economic historians have moved substantially toward supply-decline +
provincial-government failure and away from both "Churchill's genocide" and "unavoidable natural
disaster." The public sees only the two poles.

### 10. Provisional title + thumbnail, anchor filter

- `Churchill and the Bengal Famine. The 1945 Report Nobody Reads` → **(True, 'Churchill')** ✅
- `Britain Investigated the Bengal Famine in 1945. Both Sides Skip the Report` → **(True, 'Britain')** ✅

Thumbnail promise: the Commission report's cover or a table page, with an overlay naming the year.
Text overlay 2–4 words ("THE 1945 REPORT"). No face. Non-territorial → no map required.

### 11. Why these viewers return for the method

He models the move a historian makes and a partisan never does: **when two camps fight over intent,
go find the contemporaneous inquiry and read what it actually apportions.** And the twist — the
inquiry blames a Bengali elected government as well as London — is the kind of result that satisfies
neither camp and therefore proves he followed evidence rather than a side.

### 12. Strongest reason to kill it

**Pocket risk, and it is the channel's documented worst failure mode.** `indian history` is 83%
India; `british empire` skews Pakistan/Indonesia/India/Bangladesh; `winston churchill` has no target
country in its top five. The channel's one breakout converted at 5.0 subscribers per 1,000 views —
its **floor** — precisely because the audience landed outside the target countries. Bengal famine
content has a strong prior to land in India. The June 2026 UK news event is the counter-argument, but
it is a hope about routing, not a measurement of it.

Secondary: the comment section is a Churchill-legacy war between British patriots and Indian
nationalists, and 224 lifetime comments is not the moderation capacity for that.

### 13. Confidence

- **Demand: MEDIUM.** Real, low-competition famine-specific volume (4,254–5,342/mo at competition
  19.7–40.9); geography unmeasured on those exact rows and adversely skewed in the neighbourhood.
- **Referee gap: MEDIUM.** One long-form partisan incumbent at 261K; the *specific* document appears
  nowhere. **But only three channels were catalogue-checked and only one framing was run.** This
  claim is not yet at ADR-0020 standard and must not be scored above 50 until it is.
- **Exhibit: HIGH.** 254 pages, public domain, five verified download locations.

---

# Ranking, recommendation, and what must be verified first

**Ranked: 1 — the "100 Million" arithmetic. 2 — the Bengal Famine report.**

**Recommendation: Candidate 1.**

**Why it beats Candidate 2.** Three reasons, in order of weight.

1. **Market geography.** `communism` is 53% US and 13% GB — 66.6% target market. Bengal's
   neighbourhood is South-Asia-dominant and runs straight into the channel's documented
   worst-converting pocket. Serve is the binding constraint, and this is the only lever in the set
   that moves it in the right direction.
2. **Referee-absence evidence quality.** Candidate 1 has four ranked framings plus six full
   uploads-playlist walks totalling 1,712 videos, with every closest adjudicator ID-verified and
   every one of them partisan. Candidate 2 has one framing and three walks. Under ADR-0020 these are
   not the same claim strength, and I am ranking on the strength of the evidence rather than on the
   attractiveness of the story.
3. **Method transfer.** "Ask what the counterfactual baseline is" is a test the viewer can run on a
   dozen arguments he is already having. Candidate 2's lesson ("find the contemporaneous inquiry") is
   good but narrower.

Candidate 2's advantages are real and should not be lost: a better exhibit, a live dated UK
flashpoint six weeks old, a cleaner anchor, and a genuinely symmetric target set. **They share the
same technical spine — a death toll whose range is set by a baseline assumption — so Candidate 2 is
the natural sequel, not a discard.**

### Must be verified before greenlight (Candidate 1)

1. **Secure the *Le Monde* 1997 Werth/Margolin rebuke** — exact date, exact wording, retrievable
   scan. If it cannot be obtained, the opening exhibit collapses and the video needs restructuring
   around the demographic instrument alone.
2. **Replace the three baseline death-rate figures** (25.4 / ≈39 / 44.6) with values read directly
   from Coale 1984 and Banister 1987. They currently rest on partisan secondary sites and would fail
   `/verify`.
3. **Read Ó Gráda, PDR 37(1) 2011 in full** and confirm the "implausibly low 10 per thousand" quote
   with a page number.
4. **Two more referee catalogue-checks** on channels not yet walked — candidates: Knowing Better
   (walked for famine terms, 0; re-walk for `communis|100 million`), History Debunked, Whatifalthist,
   Ryan Chapman (correct channel ID — the handle I resolved was a 55-subscriber decoy),
   PhilosophyTube, Some More News.
5. **Run `serp_title_study`** and read the "WHAT THIS STUDY CANNOT TELL YOU" block before letting any
   whitespace number above 50 enter a project file.
6. **Serve-risk probe:** decide explicitly whether to accept limited-reach risk on a
   China+communism topic, or to reframe the packaging around the *China famine demography* rather
   than the word "communism". This is a judgement call for the owner, not a measurement.

### Repo collisions — FLAGGED, not disqualifying

- **`video-projects/_BACKLOG/9-communism-definition-2025/`** — a full project (SCRIPT.md,
  FACT-CHECK-VERIFICATION.md dated 2025-01-26 "VERIFIED - Production Ready", NotebookLM source list).
  Its subject is *defining* communism from Marx texts and Soviet statistics — **adjacent but not
  identical** to the death-toll arithmetic. It is dormant in `_BACKLOG/`. **Its NotebookLM source
  list and Soviet-statistics fact-check are directly reusable and would materially cut Candidate 1's
  research cost.** Ranked on merit, its existence is an *asset* here, not a blocker.
- **`_IN_PRODUCTION/61-spanish-colonization-black-legend-2026/`** — collides with the
  pre-Columbian-population candidate in the rejection log below (both are colonial-depopulation
  quantification). Noted there.
- No collision found with Candidate 2. Grepped `video-projects/`, `channel-data/` and
  `.claude/REFERENCE/` for `bengal|churchill|famine inquiry`; only hit was a Churchill mention inside
  `channel-data/FORMAT-EXPERIMENTS/History YouTuber Seeks Misconception Debunks.md` line 51, on the
  unrelated McMahon–Hussein item.

---

# REJECTION LOG

Every candidate generated and dropped, with the ID-verified evidence that killed it.

### R1 — The Shroud of Turin: the 1988 raw radiocarbon data · **KILLED on referee**

*The strongest candidate in this run on demand and exhibit, and I am killing it anyway.*

The case was excellent. Verified: the 1988 three-lab radiocarbon raw data were **never released**;
2017 FOIA requests forced the British Museum to hand over its files "not dated or arranged in any
order"; **Casabianca, Marinelli, Pernagallo & Torrisi, *Archaeometry* 61(6):1223, published
2019-03-22**, found the counts unequivocally heterogeneous, undermining the precision of the
1260–1390 interval. And the 2022 counter-claim — De Caro et al., *Heritage*, WAXS dating of a
**single 0.5mm × 1.0mm thread** to 55–74 AD, calibrated against one Masada reference sample, by
researchers who are sindonologists rather than textile-dating specialists, with De Caro himself
asking other labs to replicate (none have). Textbook Shape D.

Demand was the best measured anywhere: `shroud of turin` **108,188/mo, US countryVolume 17,082**,
topMarkets IN 22% / US 17% / VN 11% / **GB 8%**; `shroud of turin carbon dating` 4,334/mo at
competition **30.8**. Assertion ecosystem sits *exactly* on the channel's verified overlap audience:
Tucker Carlson `rKMQY49py4w` **3,321,069** (1:33:26, 2025-08-08), Michael Knowles `OElbxDPsqpw`
**2,367,682**, Matt Fradd `HAbuG-oVq1Q` **3,586,511**, Dr John Campbell `YT1R2kDPHFA` **2,473,253**,
CBN `xN-BTXkqCkw` **1,158,233**, Cross Examined `rVNc9Dlnj2A` **360,647** (2026-04-07), Tucker
Carlson Network `6HVyuNClk9A` **257,333** ("The 5 Scientific Facts That Prove…").

**What killed it.** Catalogue-checked by full uploads playlist:
Religion for Breakfast (1.25M subs, 363 uploads) **0** · Miniminuteman (3.45M, 391) **0** ·
World of Antiquity (352K, 562) **0** · UsefulCharts (2.08M, 295) **0** · Paulogia (157K, 736) **0** ·
Gnostic Informant (241K, 732) **0** · History for Atheists (8.4K, 32) **0** · Professor Dave (2,000)
**0** — and then **Dan McClellan `UCAAJCQ0FCqRmAEv95SyTfNg` (258K subs, 2,000 uploads walked): ten
Shroud videos**, a sustained April–May 2026 run by a credentialed scholar, ID-verified:
`desnYBi2dDU` **53,124** / 8:32 / 2026-04-07 *"The debunked C14 dating of the Shroud of Turin"* —
**literally my exhibit** · `FV5qpHIV3KE` 49,974 / 15:04 · `gd4G4BC9Imc` 49,172 / 9:57 ·
`2Rw7p1xnfNk` **46,820** / 14:17 *"This technology shows the Shroud is authentic?"* — **the WAXS
paper** · `z416X_cmOHM` 45,711 · `fcPkhtCoPG8` 41,506 · `1BMiNvnPEL4` 41,429 · `ilf1aLPFEzU` 34,597 ·
`XHgqkP-Nws4` 29,574 · `Ib0BvuQSDWI` 22,710. **≈414,000 cumulative views, three months ago.**
Plus Emma Thorne `AVLjeByCmdw` **168,659** / 23:38 / 2025-09-06 *"The Shroud of Turin is Fake: All
the Evidence"*, and MythVision `TlQRFcRO2ew` **15,253** / 42:36 / 2026-04-24 debunking Tucker's guest
by name.

I checked whether Metatron was the referee and found he is **not** — both his Shroud videos
(`tAQQhBnCVQs` **731,325** / 47:41 / 2022-12-30; `yK8x4lvFl1M` **247,147** / 35:02 / 2024-10-19) cite
only advocacy sources in their descriptions: shroudofturin.com (Turin Shroud Center), shroudresearch.net,
magiscenter.com, Giulio Fanti. That finding *strengthened* the candidate. Dan McClellan then destroyed it.

**Refusing to rationalise:** I could argue McClellan argues one side and the un-refereed position is
"neither date is defensible." That is precisely the reasoning ADR-0020 was written to stop. A
credentialed scholar with 258K subscribers ran ten videos on this exhibit twelve weeks ago. **Dropped.**
Secondary kills: `Turin`/`Shroud` **fail** `has_search_anchor` (only an `Italy` reframe passes), and
the Catholic-apologetics comment load is beyond 224-lifetime-comment moderation capacity.

### R2 — The Irish Famine food-export ledgers · **KILLED on referee**

The assertion ecosystem is enormous and shorts-driven ("Britain exported food while a million
starved" — dozens of videos), and the actual net-trade finding (imports exceeded exports from 1847;
Ó Gráda versus Kinealy) surfaces publicly almost nowhere — the only specialist treatment I found was
`3oDkBt7No5I`, **920 views**, Liam Kennedy on famine food exports.

**What killed it.** **Irish History Podcast `UCtsjMpfYmxq_71xZcQhHxWw`** (Fin Dwyer, professional
historian, 75.1K subs) — full uploads playlist walked, 530 videos, **92 famine hits**, including a
26-part evidence-led series and: `17RE_G-DJzg` *"Why didn't Irish people eat fish during the Great
Famine?"* **1,901,232 views** (a myth-buster at genuine scale) · `vbx0FfGuJ48` *"What was the real
cause of the Great Irish Famine?"* **23,015** · `gphW2tYoDRU` *"Charles Trevelyan: The Man Behind the
Great Irish Famine?"* **35,329** · `8zJxTob18m4` *"Was the Great Famine a Genocide?"* 827 ·
`43Cc9mkTskA` *"Free Trade or Famine 1845-46"* 532. Plus **Extra History** (4.59M subs): a five-part
series and `q3cE_pQhBOU` *"Irish Potato Famine — Lies"* **176,055** — their explicit
self-correction format. Plus TED-Ed `OUieqzVZdQc` **1,148,165** *"What really caused the Irish Potato
Famine."* A credible referee exists at meaningful scale. **Dropped.**

### R3 — Dresden: the forged Tagesbefehl and the 2010 Historians' Commission · **KILLED on referee**

Superb exhibit shape (a documented forgery — 20,204 becoming 202,040 — plus the city-commissioned
2010 Historikerkommission report), live German political usage, and Germany is a target market.

**What killed it.** **HardThrasher `UCKe688ci_VwKVCr0GVZkDhQ`** (103K subs) — full uploads playlist
walked, 69 videos: `vxVEmYk-oO0` *"Bomber War Ep9 — Dresden — Targets, Tangents & Genocide"*
**112,434** / 54:16 / 2026-01-20 · `Fed0sUNTcY0` *"Bomber War Ep. 10 — Firestorm Dresden"*
**85,697** / 54:28 / 2026-02-05 · `7bb9jnAL7Ig` *"Dresden Myths: Debunking Common Misconceptions"*
**26,989** / 2026-01-19. **≈225,000 views across a footnoted, source-cited two-part treatment
published six months ago** — Ep9's description carries numbered citations to Taylor's *Dresden* and
McDonough. Also Potential History `clWVfASJ7dc` **701,371**, DW News `YwkMo1_rWM0` **385,417**, and
`vBBfT9mR_Kc` (Audit The Past, 129 views, 2026-07-02) has already taken the exact
Goebbels-inflated-toll angle. Secondary: `Dresden` fails `has_search_anchor`; Nazi-adjacent content
carries serve risk. **Dropped.**

### R4 — The Nazi gun-control claim: the 1928 and 1938 statutes · **KILLED on demand**

Genuinely thin referee field — the only English treatments I could find and ID-verify were
`3e6JO2JxifY` (Carolyn Kraft, **16,144** / 28:08 / 2025-09-28), `TBO6MCFXN1E` (**859** / 10:14),
`zK2oaQF-DY8` (Brofessor Stein, **102,545** / 18:21 / 2026-03-28 — a many-myths omnibus), and
`B9u8XMTBQ8c` (JoergSprave, **145,648**, German, about *modern* German law). Perfect
Untranslated-Evidence-series fit (the 1938 Waffengesetz).

**What killed it: demand.** `gun control` **6,474/mo** at competition 60.5; `nazi gun control`
returned **0 volume** at competition 61; `second amendment` 5,031; `right to bear arms` 4,469. Under
1K/mo on the specific framing is a hard stop, and the general framings are low-volume,
high-competition. Compounding: firearms content is a live YouTube limited-reach category, so the
serve risk lands on top of weak demand. **Dropped.**

### R5 — The pre-Columbian population number (Dobyns 1966 / Koch et al. 2019) · **KILLED on demand + collision**

Excellent shape: the "90–95% died" and "100 million" figures rest on Dobyns' 1966 depopulation-ratio
extrapolation; Rosenblat said 13 million; Koch et al. 2019 (*Quaternary Science Reviews*) turned it
into a precise 56 million plus a climate signal now quoted as settled fact.

**What killed it.** Demand on the specific question is **unmeasured** — `native american population
before columbus` returned `estimatedMonthlySearch: 0` (no measurement), and the general terms carry
severe pocket risk: `native americans` **61,342/mo** but topMarkets **VN 30% / PK 10%** with US
countryVolume only **3,067**; `native american` 147,599/mo with US 9.8%; `history of the americas`
3,617. No demonstrated demand plus the channel's worst geography. **Collision:**
`_IN_PRODUCTION/61-spanish-colonization-black-legend-2026` occupies the adjacent ground — flagged.
Referee gap was never tested; do not read this rejection as a whitespace claim. **Dropped.**

### R6 — Aztec sacrifice numbers vs the Huei Tzompantli excavation · **KILLED on tooling + collision**

Real exhibit: the Templo Mayor skull-rack excavations (~650 skulls, then a further 119 section) set a
hard archaeological floor against Andrés de Tapia's colonial claim of 136,000, while confirming the
practice was real and organised. Coverage found is all short news clips — Science Magazine
`hOz7a2oEgrQ` **209,965** / 3:23, BBC REEL `ljF0YO1FoqY` **63,703** / 3:27, TomoNews `uWRtQpKktcQ`
**19,387** / 2:25 and `VXQ1Zb-Hyh8` **8,769** / 8:10 — i.e. no long-form adjudication surfaced.

**What killed it:** I could not test it to standard. `vidiq_youtube_search` returned
`{"results":[]}` and the YouTube search quota was exhausted, so I could run neither four framings nor
catalogue-checks of the channels most likely to hold it (**Ancient Americas**, World of Antiquity,
Miniminuteman, Fall of Civilizations). **I am not claiming whitespace here — I am recording that the
instruments failed.** Also collides with `#61 black legend`. **Dropped as untested, not as unviable —
this is the best candidate to re-test once search quota resets.**

### R7 — Holodomor: the 1932 grain-export series and the 22 Jan 1933 directive · **KILLED on moderation**

Genuine specialist dispute (Conquest/Applebaum versus Davies & Wheatcroft), a bounded exhibit (the
export tonnage series plus the Stalin–Molotov directive restricting peasant movement out of Ukraine
and Kuban), and live target-market politics — Germany recognised it as genocide in Nov 2022, as did
Canada. **Killed on the brief's own explicit constraint: he cannot arbitrate a war in his comments,
and 224 lifetime comments across 28 videos is the entire moderation budget.** Compounding: the field
is already held by partisan long-form — BadEmpanada `3kaaYvauNho` **433,674** / 1:37:17 / 2022-04-26
and `4L3d0GJlzgc` **154,447** / 41:54 / 2024-02-24. Also collides with `#62 Volhynia` (in
production) and three published Ukraine/USSR videos. **Dropped.**

### R8 — The Höfle Telegram and how the Reinhard death toll is actually known · **KILLED on shape + serve**

A magnificent bounded exhibit (the January 1943 decrypt totalling 1,274,166 arrivals at four camps),
and it directly serves "show the method by which a claim can be known to be false." **Killed on two
brief-level rules:** the evidence is radically asymmetric, and the brief prohibits both-sides framing
where that is true; and Holocaust content sits squarely in a limited-reach category where the failure
mode is undiagnosable silence against a 302-impression median. Moderation load would also be extreme.
No referee search was run. **Dropped on shape, not on gap.**

### R9 — The witch-trial "9 million" figure · **KILLED on generic-myth failure mode**

The 9 million traces to Gottfried Christian Voigt (1784) extrapolating from one town's records —
a beautiful auditable extrapolation error against Levack's ~40–50,000 executions from surviving court
records. **Killed as a generic myth-debunk:** the brief's failure-mode list bars generic myths, the
correction is already widely circulated, and Esoterica/adjacent channels are the obvious incumbents.
Not catalogue-checked; **no absence is claimed. Dropped.**

---

## Method notes and honest limits of this run

- **Every reach figure in this document was verified by `youtube.videos().list(part='snippet,
  statistics,contentDetails', id=…)` on 2026-07-30.** No count is taken from a search snippet, a
  ranking endpoint, `intel.db`, or another model.
- **Full uploads-playlist walks performed:** 22 channels, ~11,400 video titles enumerated. Where a
  walk capped at 2,000 (Professor Dave, MythVision, Dan McClellan) that is stated.
- **Two instruments failed silently and are recorded rather than trusted:** `vidiq_youtube_search`
  returned `{"results":[]}` three times, and `youtube.search().list` hit its daily quota mid-run.
  Candidate 2 and R6 carry the resulting shortfall explicitly.
- **One regex artefact caught and corrected:** an early catalogue grep on `turin` matched the word
  "Featuring", producing false hits on World of Antiquity and Professor Dave. Re-run with `\bturin\b`;
  both are genuinely 0.
- **A channel-handle decoy caught:** `@RyanChapman` resolves to a 55-subscriber, 3-video channel, and
  `@Kraut_` / `@TheCynicalHistorian` / `@HistoryDebunked` all failed or resolved wrongly. All
  catalogue-checks in this document use resolved `UC…` IDs, listed inline.
- **No whitespace figure in this document should be scored above 50** until the pre-greenlight
  verification list is closed.
