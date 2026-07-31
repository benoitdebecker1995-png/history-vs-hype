# BLIND RUN A — next-video discovery, claim-first generation

**Date:** 2026-07-30
**Brief:** `.claude/PROMPTS/blind-next-video-discovery.md`
**Discipline:** ADR-0020 (`docs/adr/0020-strategy-claims-carry-the-same-evidentiary-burden-as-on-screen-claims.md`)
**Generation angle (assigned):** start from the *claim*, not the topic. Work outward from a specific
weaponised assertion in Western political argument to whether anyone has refereed it.

**Blindness note:** `research/active/weaponised-historical-claims-referee-gaps-2026-07-29.md` exists in
this directory. It was **not opened**. Nothing in this file derives from it. If it overlaps, that is
convergence, not contamination.

---

## 0. Instruments of record (read this before citing anything below)

| Instrument | What it did | What it cannot tell you |
|---|---|---|
| `youtube.videos().list(part='snippet,statistics,contentDetails', id=…)` | **Every view count, duration and publish date in this file was resolved this way.** Search was used only to *nominate* IDs; every nominated ID was then re-queried by ID. | Nothing about videos it was never handed. |
| `youtube.search().list` | 38 query framings across 9 candidate claims. **Quota metric "Search Queries per day" was exhausted at framing 38** (HTTP 429, logged). | It is a ranked sample. It cannot establish absence. |
| `youtube.playlistItems().list` over the **full** uploads playlist | Catalogue-checked 8 channels; regex-grepped every title. Counts below are `fetched / videoCount` so you can see coverage. | Only titles. A referee segment buried inside an unrelated title would be missed. |
| `vidiq_keyword_research` (GB, `research` mode) | Ran on `slavery reparations britain` and `british nationality act 1948`. | **It returned volume 0 for both seeds and drifted to "news"/"text to speech" related terms. It produced no usable demand signal for either and is not cited as evidence anywhere below.** |
| `tools.title_scorer.has_search_anchor()` | Tuple-read `(found, term)` on all proposed titles. | Title-filter mechanics only. A valid `packaging_lock` is not a greenlight (ADR-0020). |
| `analytics.db` + filesystem | 58 published rows; `_IN_PRODUCTION/` (20), `_READY_TO_FILM/` (1), `_BACKLOG/` (22), `_ARCHIVED/published/` (34) enumerated for collisions. | — |

**Not used, deliberately:** `vidiq_outliers` (ranks on breakout/recency; the #64 failure mode),
`intel.db` (~100 recent uploads/channel), the autocomplete scraper and `demand_scorer` (bot-walled /
placeholder floor).

**One unverified item, disclosed:** a Polish short — Archiwum Czasu, *"Czy Polska naprawdę zrzekła się
REPARACJI od Niemiec?"*, 2026-05-02, ~197K — appeared in search but I could not re-read its ID reliably
from my own log, so **it is excluded from the evidence base below** rather than cited from search output.
Two other Polish items on the same claim *were* ID-verified and are cited instead.

---

## 1. How the candidate set was generated (and mostly destroyed)

I worked from the assertion side: claims currently made in political speech, opinion columns, campaign
and advocacy material, viral posts, and think-tank publications that recruit history to win a present-day
argument. Nine claims were taken far enough to measure. **Seven were killed.** The pattern that killed
them is worth stating, because it should shape the next run:

> A claim loud enough to reach mainstream Western political speech, *and* legible as a "history topic"
> a documentary channel can farm, is already adjudicated at 100K–3M views. The surviving whitespace is
> where the political claim is loud but the **specific document or dataset carrying it** is obscure —
> obscure enough that no explainer channel has read it on screen.

Both surviving candidates have that shape: a one-page administrative document, and a public ledger.

---

# CANDIDATE 1 — Germany's entire legal case against Poland rests on a page that may never have been lawfully published

**Shape:** A (historians and international lawyers genuinely disagree; both national camps assert
certainty) with a hard C core (one document carries the whole argument).

### 1. The claim as its proponents state it

**German government position:** the reparations question is closed. Poland renounced all reparations
claims against Germany in the declaration of **23 August 1953**, effective 1 January 1954, and
reaffirmed that renunciation subsequently. There is nothing left to discuss.

**Polish government position (currently asserted by the head of state):** Poland never validly renounced
anything. The 1953 declaration was (a) extracted under Soviet coercion, (b) issued by the Council of
Ministers, which under the Constitution of 22 July 1952 had no competence over international obligations
— that lay with the Council of State, and (c) **never published in either *Dziennik Ustaw* or *Monitor
Polski***, and an unpublished act is not law. Poland is owed roughly **PLN 6.2 trillion / €1.3 trillion**
(the three-volume Mularczyk report, 1 September 2022).

### 2. Why this creator would obsess over it

This is the creator's stated chain with no seams: a claim asserted as settled fact by two governments →
one archival document → a publication-and-competence question that is *checkable* → a genuine scholarly
split → a clean statement of what is settled, what is contested, and what cannot be known. The German
position is not propaganda: unilateral declarations really do bind states in international law. The
Polish position is not nationalism: the publication gap is a documented fact. And the leading Polish
international lawyer on the file, **Jan Barcz**, argues *against his own government*. A referee who says
"the strongest version of Germany's case is X, and Poland's best point is not the one its politicians
lead with" is doing exactly what the brief describes.

It is also a native fit for **Untranslated Evidence**: the operative text is Polish, one page, and no
Anglophone audience has read it.

### 3. Who asserts it now — names, dates, ID-verified reach

| Assertion | Date | Reach (ID-verified) |
|---|---|---|
| President **Karol Nawrocki** demands reparations from Germany in his **Auschwitz Holocaust Remembrance Day speech** | 2026-01-27 | print/wire (Notes From Poland) |
| Nawrocki to President **Steinmeier**, in Berlin: the case "is still open"; later proposes Germany fund Polish rearmament *in lieu* of reparations | 2025-09 / 2026-01 | PAP, Euronews |
| German federal government: closed, per the 1953 declaration | standing position, restated 2025–26 | — |
| `2frbNy_shh8` DW News, *"Poland is demanding €1.3 trillion in reparations from Germany – what's behind it?"*, 8m15s | 2022-10-15 | **651,159** |
| `lfhSqi1OG6E` Al Jazeera English, *Inside Story*, 25m16s | 2022-09-03 | **91,724** |
| `6tUEi4KBAS8` Bądź Na Bieżąco (PL), *"Co NAPRAWDĘ Niemcy myślą o Polakach – Reparacje"*, 12m31s | 2017-10-13 | **233,022** |
| `YivbYAVD8Pc` oludzibudzi (PL), *"Jabłoński vs Szczuka o reparacjach – kto ma rację?"*, 57s | **2026-02-23** | **167,545** |
| `plilI56H4Yo` Codziennik (PL), *"DLACZEGO POLSKA NIE OTRZYMAŁA REPARACJI OD NIEMIEC?!"*, 34s | **2026-06-06** | **25,585** |
| `TNm53d48WRQ` A! To Ciekawe (PL), Nawrocki vs Germany, 8m57s | 2025-09-01 | **18,971** |

The two 2026 Polish shorts matter: they show the claim is being fought *this year*, in short form, at
scale — i.e. it is live argument, not archive.

### 4. Why the target audience cares

Politically engaged men 25–44 in **Germany** (a named target market) are inside this argument: it is
their government's liability position, it is adjacent to the AfD-era fight over memory politics, and it
sits on the EU's largest bilateral fault line. UK/US/CA viewers of political commentary get the thing
they actually reward — a mechanism: *how a state escapes a debt using an administrative technicality,
and whether the technicality holds*. HOW, not WHY. Logistics/legal/admin, which is the channel's
verified subscriber trigger.

### 5. Demand evidence — and its weakness, stated plainly

- English-language assertion ecosystem: **~743K** ID-verified across DW + Al Jazeera, both from 2022.
- Polish-language ecosystem: **~445K** ID-verified, including **193K in 2026 alone**.
- `vidiq_keyword_research` produced nothing usable (see §0). **No keyword volume figure is claimed here.**
- `topMarkets`: **not obtained** — the tool returned empty `topMarkets` arrays on every seed I tried.
  I am therefore *inferring* PL/DE concentration from the language distribution of the assertion
  ecosystem, and flagging it as inference, not measurement.

**This is the candidate's weak flank.** Demand for the claim is demonstrated; demand *in the channel's
converting markets* is inferred, not measured. See §14 for the exact pre-greenlight test.

### 6. Referee-gap evidence

**Queries run (8 framings — partisan, neutral, document-level, and German-language):**
1. `Poland Germany war reparations 1953 waiver`
2. `did Poland waive war reparations 1953 declaration`
3. `Poland demands 1.3 trillion reparations Germany explained`
4. `Poland Germany reparations legal claim historians`
5. `Bierut declaration 1953 reparations Poland`
6. `Poland reparations Germany legally binding waiver document`
7. `Verzicht Polen Reparationen 1953 Erklaerung` *(German)*
8. `Poland Germany reparations who is right`

**Channels catalogue-checked by FULL uploads playlist** (grep `poland|polish|reparation|german|warsaw`):

| Channel | Subs | videoCount | fetched | Poland/Germany hits | Reparations adjudication |
|---|---|---|---|---|---|
| TLDR News EU | 1,140,000 | 1,004 | **1,002** | 98 | **none** |
| TLDR News Global | 1,150,000 | 946 | **946** | 1 | **none** |
| Kraut | 603,000 | 64 | **65** | 7 | **none** |
| CaspianReport | 1,850,000 | 566 | **566** | 11 | **none** |

TLDR News EU is the single likeliest referee — a 1.14M-sub channel that does European legal-political
explainers and has published 98 Poland/Germany videos. Its closest item, `BJ_IQTRqh5U` *"Why
Poland-Germany Tensions Are Rising"* (2025-07-14, **283,341** views), was ID-verified and its description
read: it is about **border controls and migrant returns**, not reparations.

**Closest adjudicators, ID-verified, and precisely what they fail to do:**
- `2frbNy_shh8` DW News, 8m15s, 651,159. Four years old, and a news explainer: it reports that Poland
  demands and Germany refuses. It does not put the 1953 declaration on screen, does not address the
  publication gap, does not address Council-of-Ministers competence, and does not name a specialist on
  either side.
- `lfhSqi1OG6E` Al Jazeera *Inside Story*, 25m16s, 91,724. A panel. Advocates state positions; no source
  criticism, no document.
- Neither states the strongest version of the opposing case. Neither separates consensus from dispute
  from uncertainty. **Neither is a referee under the brief's definition.**

**Required phrasing:** I searched the 8 framings above and catalogue-checked those 4 channels by full
uploads playlist, and **did not find** an adjudication of the 1953 declaration's legal validity in
English. I have not proven one does not exist. Specifically not excluded: German- and Polish-language
long-form (my German framing was one query and my search quota then ran out), podcast-only audio, and
adjudication buried inside a differently-titled video on any of the four channels.

### 7. The exhibit — and whether it is obtainable

**Primary:** the Declaration of the Government of the Polish People's Republic, **23 August 1953**
(preceded by the Council of Ministers resolution of 19 August 1953; issued the day after the Soviet–GDR
protocol of 22 August 1953 relieving the GDR of reparations). Circulated in *Trybuna Ludu*, 24 August 1953.

**The auditable test the viewer can run themselves** — this is the strongest single asset here: the 1953
volumes of ***Monitor Polski*** and ***Dziennik Ustaw*** are digitised and index-searchable online. The
viewer can search for the declaration and **fail to find it**, on camera, in thirty seconds. That is the
brief's "makes the conclusion auditable rather than a matter of trusting the presenter", literally.

**Supporting exhibits, all obtainable:** Barcz & Ruchniewicz's published document selection on the
23 August 1953 declarations (*Monitor Konstytucyjny*) — a curated primary corpus; the Constitution of
22 July 1952 (treaty competence vested in the Council of State); the Soviet–GDR protocol of 22 August
1953; the 1970 Warsaw Treaty; the 1990 Two-Plus-Four Treaty; the 2022 Mularczyk report (3 vols, public);
the Bundestag Scientific Services opinion (2017).

Obtainability: **high**. Translation work required (Polish → English) — which is the series' whole point.

### 8. Honest evidentiary map

**Supports Poland**
- The declaration is not in *Dziennik Ustaw* or *Monitor Polski* for 1953–56. Documented, checkable.
- Under the 22 July 1952 Constitution, treaty ratification/denunciation lay with the Council of State,
  not the Council of Ministers that resolved the waiver. A real ultra vires argument.
- The timing (one day after the Soviet–GDR protocol) is strong circumstantial evidence of Soviet dictation.
- The declaration is framed toward *Germany* in a context where the FRG was not the addressee.

**Undermines Poland**
- International law recognises binding unilateral declarations made publicly with intent to be bound
  (the ICJ's *Nuclear Tests* line). Domestic publication defects do not automatically void an
  international undertaking.
- Half a century of Polish conduct consistent with the waiver — the 1970 Warsaw Treaty, the 1975
  Gierek–Schmidt package, and subsequent official Polish statements — invites estoppel/acquiescence.
- The 1990 Two-Plus-Four settlement was designed to close the German question.
- Germany did pay through other channels (1972 pensions; the 1991 Foundation for Polish-German
  Reconciliation; the 2000 forced-labour foundation) — small against the claim, but not nothing.
- The territorial-compensation argument: Poland received German territory to the Oder-Neisse line.

**Unknowable / limits certainty**
- Whether any promulgation occurred through a channel not preserved.
- The completeness of the Soviet pressure record; the internal decision trail is partial.
- Whether the archived resolution text matches what was actually declared.
- Any valuation of "€1.3 trillion" depends on counting foregone growth — a modelling choice, not a fact.
  **The video must not adopt the figure; it must show what the figure is made of.**

### 9. Specialists and the real state of scholarship

- **Jan Barcz** (SGH Warsaw) — Poland's leading authority on the file; co-editor with **Krzysztof
  Ruchniewicz** of the 23 August 1953 document selection; argues the renunciation binds Poland. A Polish
  specialist contradicting the Polish government is the single most valuable voice for this video.
- **Stanisław Żerko** (Instytut Zachodni, Poznań) — argues a German compensation debt persists.
- **Krzysztof Gruszczyński** — SSRN 2023, on the future of the claims (*modus operandi*).
- **Władysław Czapliński** — Polish international law.
- German side: **Christian Tomuschat**, **Andreas Zimmermann**; plus the Bundestag Scientific Services
  2017 opinion, which conceded arguable points and is therefore useful as a hostile-witness exhibit.
- Advocacy institutions to treat as *parties*, not sources: Instytut Strat Wojennych im. Jana Karskiego,
  Warsaw Institute, reparations-for-poland.com.

**State of scholarship:** genuinely unsettled on the *legal* question; not unsettled on the *facts* of
what was signed and when. Exactly the brief's Shape A/B boundary.

### 10. Provisional title + thumbnail, and the anchor filter

`has_search_anchor()` returns a tuple; all three read `(True, 'Poland')`:
- **"Germany Says Poland Gave Up Its Reparations. The Document Was Never Published"** → `(True, 'Poland')`
- "Poland Wants 1.3 Trillion From Germany. One Unpublished Page Decides It" → `(True, 'Poland')`
- "Germany's Case Against Poland Rests on One Page Nobody Printed" → `(True, 'Poland')`

Declarative, no colon, no year, anchor inside 40 chars. Thumbnail promise: the 1953 declaration page
beside the 1953 *Monitor Polski* index, with the absence marked — text overlay 2–4 words
("NEVER PUBLISHED"). Maps are unnecessary; the document *is* the image.

**A mechanically valid lock is not a greenlight (ADR-0020).** This clears the filter; it does not pass a gate.

### 11. Why these viewers return for the method

The transferable test is: *when a state says a matter is legally closed, find the instrument that closed
it and ask whether the instrument was validly made.* That test runs on Chagos, Gibraltar, the Belavezha
Accords, Guadalupe Hidalgo — everything this channel already does well. This episode teaches the tool,
and the back catalogue is where you go to use it.

### 12. Strongest reason to kill it

**Demand in the converting markets is inferred, not measured.** The ID-verified 2026 traffic on this
claim is Polish-language. Poland is not a target market, and the channel's one breakout converted at its
floor (5.0 subs/1,000) precisely because reach landed outside the target pocket. If YouTube serves this
to Poland, it repeats that failure with a smaller ceiling. Secondary: WWII-reparations framing sits near
sensitivity-flagged categories, and the failure mode there is undiagnosable silence.

### 13. Confidence

- **Demand: LOW-MEDIUM.** The claim is demonstrably live (193K of ID-verified 2026 short-form). Target-market
  demand is unmeasured, and the one tool that could have measured it returned nothing usable.
- **Referee gap: HIGH.** 8 framings; 4 channels catalogue-checked at 2,579 titles fetched of 2,580
  claimed; the likeliest referee's closest video ID-verified and read, and it is about border controls.
- **Exhibit: HIGH.** One page, digitised, and the viewer can run the negative test themselves.

---

# CANDIDATE 2 — "British taxpayers were still paying off the slave-owner compensation until 2015"

**Shape:** D (proponents are right about a large, shocking core and extrapolate past what the records
support) — and symmetric, because the *counter*-camp overreaches in the opposite direction.

### 1. The claim as its proponents state it

When Britain abolished slavery it compensated **the slave owners, not the enslaved**: **£20 million**
voted under the Slavery Abolition Act 1833 and distributed under the Slave Compensation Act 1837 across
roughly **46,000 awards** — around 40% of annual government expenditure. To fund it the Treasury borrowed
£15 million in 1835. **And British taxpayers did not finish paying that debt until 2015** — a fact HM
Treasury itself tweeted on **9 February 2018** before deleting it, and which the CARICOM Reparations
Commission has used ever since.

**The counter-claim, asserted just as confidently:** the 2015 line is a myth; the loan was long since
repaid; the whole thing is reparations propaganda.

### 2. Why this creator would obsess over it

Both camps are wrong in the same place, and the truth is stranger than either. The compensation is real
and larger than most viewers believe. The 2015 date is also real — but not for the reason it is used:
the 1835 borrowing was rolled into the government's gilt programme, ultimately into an **undated** gilt,
and in 2015 the Treasury redeemed *all* remaining undated gilts as portfolio housekeeping. And then the
part nobody says out loud: **the Treasury has no record of how many original 1835 holders converted
rather than redeemed**, so *how much* of that specific debt survived to 2015 is **not knowable**. A claim
that is neither true nor false but unresolvable from the surviving records is the purest possible
illustration of "here is what the evidence permits."

### 3. Who asserts it now — names, dates, ID-verified reach

| Assertion | Date | Reach (ID-verified) |
|---|---|---|
| **HM Treasury** tweets that taxpayers helped pay for it; deleted after backlash | **2018-02-09** | the tweet is itself an exhibit |
| **Hilary Beckles**, CARICOM Reparations Commission chair, adopts the 2015 claim | 2018-02-22, recurring | — |
| `SZvkTmNQSy4` Al Jazeera English, *"The truth about the British Empire and slavery: Mehdi Hasan and Nigel Biggar"*, 51m51s | **2025-12-05** | **1,543,549** |
| `O97F3GZhVFU` GBNews, *"'Royal Navy DIDN'T get rid of slavery!' Farage clashes with activist"*, 8m13s | 2023-06-07 | **472,566** |
| `lPMGs1E0ijA` Cambridge Union, *"This House Would Pay Reparations"*, 1h47m20s | 2022-11-10 | **37,813** |
| `qDZcEo1UB-0` History Debunked, *"Lenny Henry says Britain should pay £19 Trillion…"*, 3m55s | 2025-10-04 | **34,207** |
| `6L_ri2rjBYs` History Debunked, *"David Lammy demands reparations…"*, 3m35s | 2025-02-09 | **36,765** |
| `KPJ50QyM0h0` History Debunked, *"The unfair idea of reparations…"*, 8m13s | **2026-07-05** | **8,909** |
| `m4A7QPuiDbk` New Culture Forum, *"£20 TRILLION?! Britain Should Not Pay a SINGLE PENNY…"*, 26m1s | 2023-10-06 | **17,437** |
| `uGkakhzWj1c` New Culture Forum, *"UN Judge Says Britain Must Pay £18 TRILLION…"*, 10m7s | 2023-08-25 | **27,661** |

Note the **December 2025** Al Jazeera debate at **1.54M** — the argument is at peak volume in English,
seven months ago, in the channel's #1 market.

### 4. Why the target audience cares

UK is the channel's #1 market and this is a first-order live UK political argument (reparations at
Commonwealth level, Lammy, CARICOM, Reform-adjacent counter-mobilisation). It is also *fiscal and
administrative*: a ledger, a loan, a gilt, a deletion. That is the mechanism register the audience
rewards. And it is a topic where both tribes arrive certain, which is the channel's whole proposition.

### 5. Demand evidence

- Assertion ecosystem, ID-verified: **~2.18M** across the ten items above, **1.54M of it from December 2025**.
- A 262,000-subscriber channel (History Debunked) is farming this claim continuously: **86 of its 5,207
  titles** match `reparation|compensat|slavery|caribbean|abolition|1833` — full catalogue fetched
  (5,207/5,207) — most recently 2026-07-05.
- `vidiq_keyword_research` (GB) on `slavery reparations britain` returned **seed volume 0** and drifted to
  "news"/"gb news". **No volume figure is claimed.** `topMarkets` came back empty.
- Language and channel mix imply GB/US concentration. That is inference, not measurement.

### 6. Referee-gap evidence

**Queries run (7 framings — partisan both directions, neutral, and document-level):**
1. `Britain paid slave owners compensation 1833 taxpayers 2015`
2. `slavery compensation loan Britain paid until 2015 myth`
3. `Legacies of British Slavery database slave owners`
4. `British slave owner compensation 20 million reparations debate`
5. `we paid slave owners until 2015 British taxpayers`
6. `Slavery Abolition Act loan 15 million explained`
7. `does Britain owe the Caribbean reparations historians evidence`

*(An eighth framing, `slave compensation records National Archives who was paid`, was the query that hit
the daily search-quota ceiling and returned nothing. Its emptiness is a quota artifact and carries no
evidentiary weight.)*

**Channels catalogue-checked by FULL uploads playlist:**

| Channel | Subs | videoCount | fetched | Hits | What they are |
|---|---|---|---|---|---|
| History Debunked | 262,000 | 5,207 | **5,207** | **86** | pure assertion, one side; no adjudication |
| Shaun | 763,000 | 74 | **74** | **0** | the likeliest long-form left adjudicator has **never touched it** |
| History Hit | 1,970,000 | 810 | **596** | **2** | 2022 abolition-motive explainers only |
| Empire (Dalrymple/Anand) | 80,200 | 491 | **439** | **19** | a whole slavery series — micro-audience |

**Closest adjudicators, ID-verified, and precisely what they fail to do:**
- `-vI5RR7sMDM` The Story Is Told, *"Britain Paid Slaveholders Till 2015…"*, 6m28s, 2026-02-22 —
  **10,188 views**. This is the only video I found on the exact claim, and it **asserts** it rather than
  testing it. No gilt mechanics, no Treasury-records gap.
- `KiGD2oUPi88` / `Z0iI8uSt4Jk` History Hit, *"Why Did Britain Abolish Slavery in 1833?"* Pt1/Pt2 —
  **160,165** and **69,781**. About abolition motives. Not the compensation loan, not the 2015 claim.
- `aQFL-5xf55c` UCL, *"Britain's legacy of slavery"*, 6m8s, 2011 — **75,564**. A project trailer for the
  database, not an adjudication of a claim that post-dates it by seven years.
- Empire podcast: `4pVBGb-pCiE` *A Reckoning with Slavery* **1,809**; `nrcLYV_fw0k` *The Long Death of
  Slavery* **981**; `mQdQAnMiXCU` *Slavery's Demise* **863**; `ul6MAejIZoI` *Nazis, reparations, and laws
  'just for the English to see'* **1,003**; `NRk12O5b5wM` series intro **4,314**. Rigorous, and
  **three orders of magnitude below the assertion ecosystem** — not a referee "at meaningful scale."
- `SZvkTmNQSy4` Al Jazeera (1,543,549) is a *debate*, not a referee: two advocates, no source criticism,
  no document, and the moderator is a participant.

**Required phrasing:** I searched the 7 framings above and catalogue-checked those 4 channels by full
uploads playlist (6,316 titles fetched), and **did not find** a referee that puts the compensation
records on screen and tests the 2015 claim. I have not proven one does not exist. Specifically not
excluded: BBC/Channel 4 broadcast documentaries not surfaced by these framings, university lecture
uploads, and anything inside a differently-titled video on the checked channels.

### 7. The exhibit — and whether it is obtainable

**The strongest "run it yourself" exhibit of anything I measured.** The **UCL Legacies of British
Slave-ownership database** is public and searchable by name, parish and award: the viewer can type in a
surname on camera and read the payout. Behind it sits the primary series itself — the **Slave Compensation
Commission records, T71, at The National Archives** — and the **Bank of England working paper (2022) "The
collection of slavery compensation, 1835–43"**, which is a dataset of who actually collected.

For the 2015 half: the **deleted HM Treasury tweet of 9 February 2018** (archived), the gilt trail
(£15m borrowed 1835, £11.25m of it in 3% Consolidated Annuities → rolled into an undated 4% Consolidated
Loan → all remaining undated gilts redeemed **1 February 2015**), and **Full Fact's** documentation that
the Treasury holds no record of the conversion-versus-redemption split. Obtainability: **high**, all free.

### 8. Honest evidentiary map

**Supports the claim** — the compensation is real, enormous, and went to owners; ~46,000 awards; the
1835 borrowing is documented; the 1 February 2015 redemption of undated gilts is a fact; the Treasury
itself asserted the link in 2018.

**Undermines the strong version** — the 1835 debt was not a ring-fenced obligation ticking down for 180
years; it was absorbed into the general gilt stock. Holders between 1835 and 1927 could redeem or
convert. The 2015 event was portfolio modernisation, not the final instalment of a slavery debt. Anyone
saying "we were paying slave owners until 2015" is describing a bookkeeping lineage as if it were a
payment schedule.

**Unknowable** — how much of the original 1835 borrowing survived into the 2015 instrument. The Treasury
does not have the records. **Neither camp can win this point, and that is the episode's spine.**

### 9. Specialists and the real state of scholarship

- **Nicholas Draper**, *The Price of Emancipation* (Cambridge UP, 2010) — the authority on the compensation.
- **Catherine Hall, Nicholas Draper, Keith McClelland, Katie Donington, Rachel Lang**, *Legacies of
  British Slave-ownership* (Cambridge UP, 2014).
- The **UCL LBS** project apparatus (database + methodology notes).
- **Bank of England** working paper (2022) on collection, 1835–43.
- Parties, not sources: **Hilary Beckles** / CARICOM Reparations Commission; **Nigel Biggar** on the
  other side; **Full Fact** and the **Tax Justice Network** as intermediaries with their own framing.

**State of scholarship:** the compensation itself is *settled* and well-documented — this is not a
historians' dispute. The dispute is entirely about **inference from a documented fact**, plus one
genuinely unresolvable records gap. Shape B/D, not A. State that honestly on screen rather than
manufacturing a scholarly controversy.

### 10. Provisional title + thumbnail, and the anchor filter

All `(True, 'Britain')`:
- **"Britain Paid Slave Owners Until 2015? The Records Don't Say That"** → `(True, 'Britain')`
- "Britain Says It Paid Slave Owners Until 2015. The Treasury Deleted the Tweet" → `(True, 'Britain')`
- "Britain Paid Slave Owners 20 Million. The Ledger Is Public" → `(True, 'Britain')`

Thumbnail: a compensation-award page with a named payout legible, text overlay "£20,000,000". No face.
Note the second variant carries a year in a *non*-leading position — a Tier-2 hedge, A/B-testable, not
a violation.

### 11. Why these viewers return for the method

The lesson is *trace the money to the instrument*: a shocking factoid usually compresses a real archival
fact and a bookkeeping lineage into one sentence, and separating them is a skill. Plus the meta-lesson
the channel is built to teach: sometimes the records ran out, and the honest verdict is "unresolvable."

### 12. Strongest reason to kill it

**Serve suppression you cannot diagnose.** Slavery-and-reparations sits squarely in a
sensitivity-flagged category; median reach is already 302 browse impressions, and 29 of 56 videos got
under 350. If reach is throttled, the result is silence indistinguishable from a bad topic. The channel's
own nearest data point is `aSfZtrgGjwA` *"They Didn't Just Buy Slaves. They Built the System."* —
**89 views** (2026-05-28). That is roughly the channel median, so it is not proof of a category penalty
— but it is not encouraging either. Secondary: with 224 lifetime comments across 28 videos, this is the
topic most likely to produce a comment war he cannot referee.

### 13. Confidence

- **Demand: MEDIUM-HIGH.** ~2.18M ID-verified assertion reach, 1.54M of it from December 2025, in the
  #1 market, plus a 262K-sub channel producing on the claim monthly. Keyword-level volume: unmeasured.
- **Referee gap: MEDIUM-HIGH.** 7 framings; 6,316 titles catalogue-checked; the only video on the exact
  claim has 10,188 views and asserts it; Shaun's 74-video catalogue is empty; Empire's coverage is
  rigorous but 3 orders of magnitude too small.
- **Exhibit: HIGH.** Public searchable database + T71 + a BoE dataset + a deleted government tweet.

---

## Collisions found (flagged, not disqualifying)

| Candidate | Collision | Assessment |
|---|---|---|
| C2 Britain / compensation | `_BACKLOG/11-industrial-revolution-2025` | Adjacent (Williams-thesis territory). Parked. C2 is narrower and document-led. |
| C2 | `_BACKLOG/21-haiti-independence-debt-2025` | Same genre (colonial indemnity arithmetic), different state pair. Could be a series. |
| C2 | published `aSfZtrgGjwA` / `_ARCHIVED/published/56-no-lassos-atlantic-slave-trade-origin-2026` (**89 views**) | Not a topic collision (that video is about the trade's origins), but it is the channel's only serve datapoint in the category. |
| C1 Poland / Germany | `_IN_PRODUCTION/62-volhynia-massacre-untranslated-2026`; `_BACKLOG/63-bandera-both-sides-invented-2026` | Poland-adjacent and both in the Untranslated line. **Sequencing risk, not a topic collision** — two consecutive Poland-facing episodes may narrow the served pocket. Worth a scheduling decision. |
| C1 | `_IN_PRODUCTION/37-untranslated-vichy-statut-juifs-2026`, published `imPn_OxLYlk` | Same series mechanic (untranslated state document). Confirms format capability. |
| — | `_IN_PRODUCTION/64-ancient-dna-aryan-weaponised-2026` | Not a collision, but the ADR-0020 precedent case. Its whitespace claim is retracted; do not treat it as an occupied slot. |

---

## Ranked order and single recommendation

**1. Candidate 1 — Poland/Germany, the 1953 declaration.**
**2. Candidate 2 — Britain's slave-owner compensation and the 2015 claim.**

### Recommendation: Candidate 1.

**Why it beats Candidate 2**, despite C2 having the better-measured demand:

1. **It is the channel's empirically proven shape.** Every one of the top performers in `analytics.db` is
   *State A vs State B, adjudicated by a legal instrument*: Guatemala/Belize (30,469 and 5,622),
   Essequibo (1,967), Turkey/Greek islands (974). Not one top performer is a "Britain and slavery"
   video, and the one attempt returned 89 views. C1 is that shape exactly; C2 is a shape the channel
   has tried once, weakly.
2. **The referee gap is the most rigorously instrumented finding in this run** — and the likeliest
   referee was eliminated by ID, not by silence: TLDR News EU has 98 Poland/Germany videos across a
   fully-fetched 1,002-title catalogue, and its closest candidate (`BJ_IQTRqh5U`, 283,341) is about
   border controls.
3. **The exhibit supports a negative test the viewer performs themselves** — searching the 1953
   *Monitor Polski* index and finding nothing. That is a stronger demonstration of method than any
   positive document, and C2's database, excellent as it is, only does the positive half.
4. **Its principal risk is measurable before commitment; C2's is not.** C1's weakness is unproven
   target-market demand — testable with one instrument run. C2's weakness is possible reach suppression
   in a sensitivity-flagged category, which the brief itself identifies as *"silence you cannot
   diagnose."* Prefer the measurable risk.
5. **Moderation load.** Poland-vs-Germany over an administrative instrument will draw argument; slavery
   reparations will draw a war. 224 lifetime comments is not a moderation capability.

**Keep Candidate 2 warm.** If the C1 demand test comes back PL-dominant, C2 is the fallback and its
demand is already the best-evidenced of anything measured here.

---

## What must be verified before greenlight

**Candidate 1 (blocking):**
1. **Target-market demand.** Search quota resets tomorrow. Run `serp_title_study` on `poland germany
   reparations`, `1953 reparations waiver`, `german war reparations poland` and — critically — obtain
   real `topMarkets` for at least one seed. **If the pocket is PL-dominant with DE below roughly a
   quarter, downgrade to C2.** Do not proceed on the inference in §5.
2. **Close the referee gap in German and Polish.** I ran one German framing before quota death and zero
   Polish framings. Minimum: 3 German + 3 Polish framings, plus a full-uploads catalogue check of
   ZDF/Terra X History and one Polish history channel above 200K subs. If a German-language adjudication
   of the 1953 declaration exists at scale, **drop the candidate.**
3. **Verify by ID any referee named by any source, including another model or Run B.** ADR-0020 §3.
4. **Confirm the publication negative first-hand.** Read the digitised 1953–56 *Monitor Polski* and
   *Dziennik Ustaw* indices directly. This is the video's spine; it cannot rest on secondary summary.
   If it turns out the declaration *was* promulgated somewhere, the episode changes shape entirely.
5. **Get Barcz's actual argument in his own words, with page numbers** — the whole intellectual-honesty
   payload depends on representing the Polish specialist who disagrees with Poland accurately.
6. **Sensitivity check:** decide how to handle WWII-reparations framing without tripping category limits,
   and whether the title should lead on the legal mechanism rather than the war.

**Candidate 2 (if promoted):**
1. Resolve the gilt chain to primary sources — not Full Fact's summary. Which undated gilt, which
   conversion, which 1927 operation, and the exact 1 February 2015 redemption notice.
2. Obtain the archived HM Treasury tweet and its deletion date.
3. Read the Bank of England 2022 working paper's dataset for a showable series.
4. Re-run framings 5–8 (quota-blocked) plus a full catalogue check of BBC/Channel 4 uploads.

---

## Rejection log — every candidate dropped, with the ID-verified evidence that killed it

**1. Birthright citizenship / the truncated Senator Jacob Howard quote of 1866.**
Live: Trump EO 14160 (2025-01-20); *Trump v. Barbara* decided 6–3 against the EO **2026-06-30**, with
Thomas and Alito dissenting on historical grounds. Perfect Shape C — one 1866 Senate floor sentence,
routinely quoted with an ellipsis, carrying the entire originalist case; exhibit is the *Congressional
Globe*, 39th Congress.
**Killed by saturation on both sides, all ID-verified:** assertion — PragerU `gyMXVg_MfYo` **6,036,704**;
Heritage `tVkqXu6mq4c` **3,053,758**. Adjudication — Vox `OBFX4EuAWHc` 12m58s **3,186,466**;
Jake the Lawyer `ebYaEUVuiug` 22m27s **58,709**; Heather Cox Richardson `OhGcekHJGqs` 17m6s **40,512**;
Open to Debate `9ynvOxWKNDA` 58m8s **40,346** (a formal both-sides debate). Plus a June-2026 SCOTUS news
flood. Also fails the anchor filter: `has_search_anchor("America Ends Birthright Citizenship…")` →
**`(False, '')`**; `"The 14th Amendment Never Said That…"` → **`(False, '')`**. Post-peak, saturated,
unpackagable.

**2. Dresden death toll / the forged *Tagesbefehl Nr. 47*.**
Near-perfect exhibit — an authentic order (20,204 dead to 20 March 1945, projecting ~25,000) against a
forgery that added a zero (202,040 / 250,000), used by David Irving and recycled by the German far right;
the 2010 Historikerkommission put it at 22,700–25,000. Germany is a target market and the 80th
anniversary fell in the 2025 election window.
**Killed: a dense referee ecosystem already exists.** Terra X History (ZDF) `htPOnvQZSBU`
*"Die Bombardierung von Dresden: Mythos und Wahrheit"* 18m58s **1,660,441** — the German-market referee,
by title and by broadcaster. Kraut `voF7KCOm6eY` 50m22s **1,051,200**. TIKhistory `PrrBRQDD_Jo` 57m3s
**662,060**. HardThrasher `vxVEmYk-oO0` 54m16s **112,434** (2026-01-20). Drop and do not rationalise.

**3. Holodomor — famine or genocide.**
Shape A on paper: real historian disagreement over intent, a documentary chain (1932 requisition
decrees, the November 1932 blacklists, the January 1933 border-sealing decree).
**Killed on two counts.** (a) The adjudication ecosystem, while partisan, is enormous and mutually
engaging: BadEmpanada `3kaaYvauNho` 1h37m17s **433,674**; MentisWave `cL-hS2HaA6Q` 33m22s **296,746** and
`MG0-sRQEbwE` 43m12s **138,861**; Vox `lejDbulJN54` **2,547,923**. (b) Moderation: this is the highest
comment-war-risk historical topic on the platform, against 224 lifetime comments of moderation capacity.

**4. The India "$45 trillion drain" figure.** — *the largest measured referee gap in this run, killed on
audience.* Assertion, ID-verified: FactTechz `zLq4CeDo8oI` **14,540,506**; VICE `x_jGPf764d0`
**1,036,331**; plus WION, Odd Compass and Jaishankar clips well past 10M combined. Adjudication:
**one video** — HISTORY CHRONICLES `ohCGQNDxJxI` *"Did Britain REALLY Steal $45 Trillion from India?"*
5m6s, **13,048 views**. A gap of roughly three orders of magnitude, on a figure asserted in UK and
Commonwealth reparations argument, with an auditable exhibit (Patnaik's method and the colonial fiscal
series). **Killed by pocket risk:** every large asserting channel is India-facing, so YouTube's audience
graph will serve it to IN, and the channel's one breakout converted at its floor (5.0/1,000) for exactly
that reason. **This is the strongest candidate that a channel with different target markets should take.**

**5. "Britain ended slavery" / the Royal Navy West Africa Squadron.**
The conservative mirror of Candidate 2, and symmetric-target attractive.
**Killed: a specialist is mid-series on it right now.** Drachinifel `ROwTL6UW_wA` 45m56s **139,383**
(2026-02-04), `nCmwEgW6CGs` 38m4s **74,118** (2026-03-18), `GakoHkH2Aqk` 26m17s **41,314** (2026-06-03),
plus `TiSekII0sjw` **215,056**; and History Hit `KiGD2oUPi88` **160,165**.

**6. The Monroe Doctrine — what the 1823 text actually says vs. how Trump invoked it over Venezuela.**
Very live (January 2026 news cycle; "Donroe Doctrine").
**Killed on explainer saturation:** History Matters `qZYrj2YOmsw` **981,167**; Khan Academy `Woh4gwIFpic`
**343,882**; National Museum of American History `EElXGPupRUk` **304,083**; Kings and Generals
`OxYWONIMgsk` 24m32s **248,973**; CSIS `CgMN4IPfDMI` **137,143**. The residual gap (that the doctrine was
two paragraphs of an annual message, that the name came ~30 years later, and that the Royal Navy enforced
it) is too narrow to carry a video into that feed.

**7. The "Kalergi Plan" and the 1925 *Praktischer Idealismus* passage.**
Textually the best Shape C I found — one book, one demonstrably truncated passage, carrying an entire
ideological argument; obtainable exhibit.
**Killed on three counts.** (a) Demand is modest: the whole assertion ecosystem I could ID-verify is
~150K (ALI TABRIZI `e4GQlwuXjTM` 27m40s **51,210**; Lavader `8L9LoHU7k2I` 19m3s **58,784**), against
Mr. Beat's general treatment `pyUQP-R48yg` 24m31s **2,061,112**. (b) Severe sensitivity-flag exposure —
antisemitic-conspiracy adjacency, where suppressed reach is undiagnosable. (c) Guaranteed comment war.
Retain as a *segment* inside a future episode, not an episode.

**8. "Nobody voted for mass immigration" — the 1948 British Nationality Act and the 1950s cabinet papers.**
The largest demand/adjudication asymmetry I found inside the target market: assertion — GBNews
`Nlod_2qX91I` 25m55s **3,390,595** and `NrDQ6XLvJGg` 20m42s **380,633**; Sky News `zTs3PDEkB2w`
**805,279**; plus continuous Reform/LBC/Talk output. Document-led adjudication: my framing
`Britain postwar immigration cabinet papers keep England white` returned **nothing relevant at all**, and
the Powell-adjacent long-form that exists is biographical, not documentary — The Rest Is History
`OstDReKXRfk` 1h14m7s **278,332**; The People Profiles `dGEpEcvryGU` **395,154**.
**Not killed on evidence — killed on capacity.** Reach suppression risk is high, the comment load would
be the most hostile on the channel, and 224 lifetime comments is not the moderation base for it. Record
it: if the channel ever has moderation capacity, this is the largest in-market gap on the board.

**9. Germany/Greece 1953 London Debt Agreement, and Greenland's 1951 defence agreement.** Dropped before
measurement: the Greek claim is not currently loud in Western political speech, and Greenland collides
with `_BACKLOG/33-greenland-independence-2026` inside a 2025–26 news flood I had no search quota left to
instrument. Neither is refuted — **neither was tested.** Do not read their absence here as a verdict.

---

## Honest limits of this run

- **Search quota died at framing 38.** Candidates 1 and 2 have 8 and 7 framings respectively, which
  clears the ≥4 bar; candidate 9 has zero. No emptiness reported in this file after the 429 is evidence
  of anything.
- **`vidiq_keyword_research` produced no usable demand or `topMarkets` data on any seed I tried.** Every
  demand statement here rests on ID-verified view counts of the assertion ecosystem instead — a better
  instrument for a claim-first run, but it measures *argument volume*, not *search intent*. No search-volume
  figure is asserted anywhere in this document.
- **Catalogue checks read titles only.** History Hit (596/810) and Empire (439/491) were incompletely
  fetched; that is stated inline.
- **`topMarkets` was never obtained for any candidate.** Every pocket-risk statement in this file is
  labelled inference. The brief asked for `topMarkets` on every anchor; I could not deliver it and am
  not disguising the gap.
- One Polish video (~197K) was **excluded** rather than cited from search output, because I could not
  re-verify its ID.
