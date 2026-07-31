# Can candidate discovery be made systematic? — frame assessment

**Date:** 2026-07-30
**Brief:** `.claude/PROMPTS/systematic-candidate-frame-assessment.md`
**Discipline:** ADR-0020 — every negative claim below names the instrument that produced it.

---

## 0. Instruments of record

Everything asserted here was produced by one of these, on 2026-07-30. Where I could not run an
instrument, §6 says so explicitly.

| # | Instrument | What it can establish | What it cannot |
|---|---|---|---|
| I1 | MediaWiki API `list=categorymembers`, en.wikipedia.org | Exact membership of a named category at a named depth | Nothing about categories not queried; depth ≥2 is drift-contaminated (measured, §2.1) |
| I2 | YouTube Data API v3 `playlistItems.list` over a channel's uploads playlist | **Exhaustive** channel catalogue (ADR-0020's prescribed referee instrument) | Video *content* — I read titles only |
| I3 | archive.org `advancedsearch.php` + `/metadata/` | Holdings and access-restriction flags | Whether a lending copy is borrowable in practice |
| I4 | WordPress REST API `/wp-json/wp/v2/` on contestedhistories.org | Publicly exposed post-type counts | The project's internal (unexposed) database |
| I5 | `WebSearch` / `WebFetch` | Existence and publisher-stated size of a work | Absence — a null search proves nothing |
| I6 | Local SQLite: `tools/intel/intel.db`, `tools/youtube_analytics/analytics.db`; filesystem count of `video-projects/*` | Current inventory and cadence | — |

---

## 1. Verdict

**Semi-systematic — the frames exist and one of them is genuinely good. Do not build the pipeline anyway.**

Three findings, in descending order of how much they should change behaviour.

### 1.1 Candidate supply is not the bottleneck, and it is not close (I6)

Measured today:

- `_IN_PRODUCTION/` — **20** projects
- `_BACKLOG/` — **22** projects
- `_READY_TO_FILM/` — **1** project
- Discovered-but-unscaffolded candidates from the four passes — **45**

That is **88 unshipped topics.**

Throughput, from `analytics.db`: 58 published; the last six publish dates run 2026-05-08 → 2026-07-05,
i.e. ~3/month at the recent peak, and **nothing has published in the 25 days since 2026-07-05.**

At 3 videos/month, existing inventory is **roughly 29 months deep.** `CLAUDE.md` states the growth
bottleneck in its own words — *"Packaging, not content. Only 3/47 broke 2K views"* — and
`channel-data/NEXT-VIDEO-DISCOVERY-HANDOFF.md` frames the problem as serve (median **302** browse
impressions), not topic supply.

The brief's premise — "screening is cheap; generation is the bottleneck" — is true *within the
discovery activity* and false *for the channel*. Generation is the bottleneck of a process that is
itself not binding. **Any hours spent finding candidate #46 are hours not spent on the constraint that
is actually limiting the channel.** This is the single most important line in this document.

### 1.2 The N̂ ≈ 85–107 estimate is biased low, and I can show it

Capture-recapture requires independent samples. The four passes shared a brief and, for three of them,
a model prior. I tested independence directly.

I drew a **random sample of 30** (seed fixed) from `Category:Pseudohistory` direct members (I1, n=241).
Judging each against the brief, ~5 are plausible pre-screen candidates: *"There was no such thing as
Palestinians"*, *"The bride is beautiful, but she is married to another man"*, *Masada myth*,
*Cuba de ayer*, *Anti-Normanism*.

**Overlap with the 45 already found: zero.**

Chapman on n₁=45, n₂≈5, m=0 gives N̂ = (46 × 6)/1 − 1 ≈ **275**, not 107. I do not believe 275 either —
one small draw, and my pre-screen judgement is not the real screen. The defensible conclusion is
narrower and more useful:

> The four passes did not sample the space. They sampled *one region* of it — Anglophone
> political-economy disputes (British Empire, India drain, communism death tolls, capitalism/enclosure,
> Irish famine, US constitutional). The nationalist-myth and ethnogenesis-myth region is almost
> untouched, and it is exactly the region an external index enumerates well.

So the honest answer to "is half the space found" is: **unknown, and the estimator cannot tell you,**
because the assumption it rests on is measurably violated. This does not change the recommendation,
because §1.1 makes N irrelevant.

### 1.3 One frame is verified, free, and reaches the unsampled region

`Category:Historical negationism` (I1, n=**54** direct members) is the highest-signal list I found. Full
membership was retrieved. Entries the four passes never surfaced, with real exhibits:

- **Operation Legacy** — the British colonial document-destruction programme. Exhibit: the Hanslope
  Park "migrated archives" released 2011–13 after the Mau Mau litigation, plus the destruction
  certificates. This is *literally* the creator's thesis — how historians know what they know, and what
  was done to stop them knowing it. Live in the British Empire debate. Not in the 45.
- **NCERT textbook controversies** — Indian textbook revision. Exhibit: before/after editions,
  deleted chapters, diffable. Auditable in the strongest sense.
- **On the Historical Unity of Russians and Ukrainians** — Putin's July 2021 essay. The creator's own
  stated motivating example. Exhibit: the essay itself. **Check for collision** before pursuing.
- **Paper genocide** — indigenous census erasure. Exhibit: census enumeration records.
- **White Legend** / **Cuba de ayer** — Spanish-colonial and Cuban-exile counter-myths, live in
  Hispanophone identity politics.

Also flagged and *not* recommended: *Report about Case Srebrenica*, *Nakba denial*, *Denial of the
October 7 attacks*, *Bosnian genocide denial* — moderation and serve risk per the brief's own
constraints (224 lifetime comments across 28 videos; he cannot arbitrate a war in his comments).

---

## 2. Ranked frames

Best first. "Hit rate" = fraction of frame entries reaching pre-screen, from a sample where I drew one,
from reasoning where I did not — stated per row.

### Rank 1 — Wikipedia negationism / pseudohistory categories · **USE THIS ONE**

| Field | Finding |
|---|---|
| What / who | English Wikipedia category system; maintained by volunteer editors |
| Size (I1, exact) | `Historical negationism` **54** · `Pseudohistory` **241** · `Genocide denial` **17** · `Conspiracy theories` **53** · **union at depth-0 = 340** (Pseudohistory ∩ Negationism = 12) |
| Access | MediaWiki API, free, no key, no rate problem. Requires a `User-Agent` header (a bare request 403s) |
| Hit rate | **~17% to pre-screen**, measured on a random 30 from Pseudohistory (5/30). The 54-entry Negationism list is denser — my read is ~5–8 plausible of 54, and it is *far* better targeted |
| Overlap with the 45 | **Zero** in the measured sample. This is the frame's actual value |
| Cost / 100 screened | **$0.** ~3.5h agent pre-screen at ~2 min/entry, ~1.3h full screen for survivors |
| Reproduce | `list=categorymembers&cmtitle=Category:Historical_negationism&cmtype=page&cmlimit=500` |

**Adversarial note.** Do *not* recurse. Measured drift (I1): Pseudohistory holds 241 articles at depth-0,
935 at depth-1, 2,423 at depth-2, **4,516 at depth-3**; Negationism goes 54 → 610 → 1,842 → 3,254. By
depth 2 the tree has wandered into unrelated topics and the frame stops being a frame. The depth-0
union of 340 is the whole usable corpus. It is also *finite and small enough to finish in one sitting* —
which is the only reason I expect it to actually get used.

### Rank 2 — *History in Dispute* (St. James Press / Gale) · **right shape, hard wall**

| Field | Finding |
|---|---|
| What / who | Reference series; each entry = one historiographical controversy with signed point-counterpoint essays (1,500–2,000 words each) plus **primary-source excerpts**. Advisory board of academics |
| Size (I5, publisher-stated) | **21 volumes, ~1,000 point-counterpoint essays, 7,350 pages**, published 1999–2005 |
| Access | **Blocked in practice.** Gale eBooks = institutional subscription. archive.org (I3) holds only **4 of 21** volumes (`historyindispute` 0002, 0005, 0007, 0014), all `access-restricted-item: true`, `inlibrary`/`printdisabled`, ACS/LCP-encrypted — controlled digital lending only |
| Hit rate | Unmeasured. Shape is ideal (A and B disputes with exhibits); staleness is the problem — content is **21+ years old** and the volume themes skew to curriculum standards (WWI, WWII, Cold War, US Civil War), the region the four passes already worked |
| Overlap | Likely **high** with the 45, precisely because both draw on the same canonical-controversy pool |
| Cost / 100 | Unknown; gated on access I could not establish |

**The cheap route I could not close:** you only need the ~50 entry titles per volume, not the text.
Tables of contents are often free via Google Books / WorldCat / library guides, and the channel's
academic-source budget is unlimited for the shortlist. **I did not retrieve a single volume's TOC** —
see §6. Worth 20 minutes *only if* Rank 1 is exhausted, which §1.1 says it won't be.

### Rank 3 — Contested Histories (EuroClio / IHJR) · **enumerable, wrong unit**

| Field | Finding |
|---|---|
| What / who | EU-funded database of disputes over statues, street names and historical markers. EuroClio + Institute for Historical Justice and Reconciliation, The Hague |
| Size — **claimed vs verified** | Site and press claim **"over 600 case studies, 134 countries."** The public WordPress REST API (I4) exposes custom post type `resources-new` with `X-WP-Total: **248**`, 3 pages. **The 600+ figure is not publicly enumerable; 248 is what exists behind the API.** Recording the discrepancy, not resolving it |
| Access | Free, open, no key: `/wp-json/wp/v2/resources-new?per_page=100&_fields=id,title,link` |
| Hit rate | **Low, ~10%.** Verified by inspection of returned titles: Faidherbe statue, St Vladimir statue Moscow, Macdonald statue Victoria, Voortrekker Monument, Emancipation Memorial. The unit is a **memory-politics dispute**, not a contested factual claim with an exhibit. Usable only where the statue fight turns on a disputed fact about the person (Colston and the Royal African Company ledgers; Leopold II) |
| Overlap | Low with the 45 — but low overlap with a low-yield frame is not worth much |
| Cost / 100 | $0, ~2h |

### Rank 4 — Full-catalogue enumeration of a defined assertion-channel set · **the ADR-0020 instrument, scaled**

Invert the search: instead of enumerating claims and then hunting for reach, enumerate *high-reach
assertion channels* and read the claims off their catalogues. The sampling unit is then the thing the
screen actually tests — a live weaponisation with ID-verified reach — rather than a proxy for it.

**Verified feasible (I2).** Full enumeration of PragerU's uploads playlist returned **6,651 items in 134
API calls** — 134 units against a 10,000/day quota. Exhaustive, not windowed, which is exactly the fix
ADR-0020 prescribes over `vidiq_outliers` and `intel.db` (~100 recent uploads/channel).
`tools/intel/intel.db` already holds a **30-channel** roster and 2,697 competitor videos.

**And then it fails on content.** Measured on the PragerU catalogue:

- 6,651 total → **302** history-keyword titles (4.5%) → **77** in the flagship "5-Minute Video" series
- **283** items are children's content (`Leo & Layla`, `TBH:`, `PragerU Kids`)
- The 77 are overwhelmingly US civics explainer (the Constitution series), US Founding hagiography,
  and Israel advocacy — *not* contested claims with auditable exhibits
- The residue that does qualify is **pre-refereed**: Atun-Shei Films, Knowing Better and others exist
  specifically to referee this catalogue. Run A independently reached the same kill — it ID-verified
  PragerU `gyMXVg_MfYo` (6,036,704 views) on birthright citizenship and killed it on referee saturation
- Geographic mismatch: US-domestic content against a UK/DE/CA/US politically-engaged audience whose
  proven topics are territorial and international

**Verdict: enumerable, cheap, and near-zero yield for this channel.** Keep the *technique* (exhaustive
uploads-playlist enumeration) as the referee-check instrument it already is. Do not use it as a
generation frame.

### Rank 5 — `intel.db` comment corpus · **demand overlay, not a frame**

Local, free, already indexed (I6): **9,712 comment signals** across **415 videos** and **25 channels**;
1,374 with ≥50 likes. Pre-tagged `patterns` — `question` 5,880, `pocket` 1,677, **`unmet_supply` 806** —
and `demand_types` — `language` 586, `ideology` 279, `method` 111, `enclosure` 73, `archive` 64.

It is tagged for *demand shape*, not *claim shape*, so it does not generate candidates. But the 806
`unmet_supply` rows are the closest thing the repo has to a native "nobody has covered this" signal from
the actual target audience. **Best use: rank a shortlist produced elsewhere, not produce one.**

### Rank 6 — Wikipedia *List of common misconceptions about history* · **too small, too trivial**

Exists (I5). ~**73** entries across Ancient / Middle Ages / Early modern / Modern, US-heavy in the last
section. Cheap enough to screen entirely in one sitting, but the content is the generic-myth material
the brief's own failure-mode list rules out (horned helmets, flat earth). **Screen it once for
completeness; expect ~0–1 survivors.**

### Dropped frames, with the instrument that dropped them

| Frame | Instrument | Why dropped |
|---|---|---|
| r/AskHistorians FAQ index, r/badhistory | `old.reddit.com/*.json` direct → **HTTP 403 Blocked**; `WebFetch www.reddit.com` → refused | **Access-blocked, not absent.** Both corpora are real and would be excellent — r/badhistory is an index of public claims with the source criticism pre-done. Blocked with the tools available. Revisit if a Reddit-capable fetch appears |
| Snopes history vertical | `WebFetch snopes.com/history/` → **HTTP 402 Payment Required** | Blocked. Also: fact-checkers cover current rumours; the history vertical is thin |
| Google Fact Check Tools API / ClaimReview | I5 — API confirmed real and free, needs a Cloud API key. **No key in the repo** (`.env.example` lists only `ANTHROPIC_API_KEY`); no `.env` exists | Could not run a query, so hit rate is unmeasured. Expected low: ClaimReview is "did politician X say Y", not historiographical dispute with an exhibit. Adding a key is free if someone wants to test it |
| Georg Eckert Institute textbook disputes | I5, one search | Real institute; library of **176,500** textbooks. **No searchable controversy database surfaced.** I did not query gei.de directly — treat as *not found*, not *nonexistent* |
| Retraction / erratum literature | Not queried | Reasoned drop: history retractions are rare and are disciplinary disputes, not public weaponisations. Named as unqueried |
| Palgrave/Routledge national-myth volumes | I5 | Real works exist (*National Myths: Constructed Pasts, Contested Presents*, Bouchard, Routledge; *Palgrave Handbook of State-Sponsored History After 1945*). But these are **theory about myth-making**, not indexed lists of claims. A chapter is an argument, not a candidate. Low yield per hour of reading |
| Parliamentary / congressional historian testimony | Not queried | govinfo and Hansard both have free APIs; plausibly enumerable. **Unassessed** — I ran out of the budget I judged this worth given §1.1 |

---

## 3. Recommendation — a worklist, not a pipeline

The brief names the failure mode: *"an elegant pipeline nobody runs."* Given §1.1, a pipeline is not
merely unlikely to be run — it would be the wrong thing to run. So the recommendation is deliberately
the smallest possible artifact.

**Do this once, in one sitting, and then stop:**

1. **Pull the frame** (~2 min, $0). One MediaWiki call:
   `list=categorymembers&cmtitle=Category:Historical_negationism&cmtype=page&cmlimit=500`.
   Optionally union with `Category:Genocide_denial` (17) and `Category:Pseudohistory` (241) for the
   full 340. Send a `User-Agent`.
2. **Dump it to a static ledger** — a markdown checklist in `channel-data/`, one line per entry. A file
   with checkboxes gets worked; a pipeline gets admired. No new tooling, no scheduled task, no code.
3. **Pre-screen at ~2 min/entry**, killing on the first failure:
   - **Kill 1 — shape.** Is there a *bounded exhibit* a viewer could inspect? No exhibit → dead.
     (This kills most of the Pseudohistory list: dead theories, fiction, organisations.)
   - **Kill 2 — liveness.** Asserted by someone with reach *now*, in UK/US/DE/CA debate? Dead theories
     are dead topics.
   - **Kill 3 — serve/moderation.** Active-war and genocide-denial adjacents: kill on the brief's own
     capacity constraint, not on merit.
4. **Full screen the survivors** at the brief's ~5 min: vidIQ demand → `serp_title_study` →
   **exhaustive uploads-playlist catalogue check** of the 3–6 likeliest referees, per ADR-0020. Never
   substitute a search for a supplied ID.
5. **Stop at 54.** Do not recurse the category tree (§2, Rank 1 adversarial note).

**Automatable:** step 1 entirely; the demand pull and SERP study in step 4. **Needs judgement:** all
three kills in step 3, and the referee-quality call in step 4 — "is this a referee or a partisan
rebuttal" is the judgement the whole brief turns on and it does not automate.

**Expected yield, stated honestly and pessimistically:** ~17% of frame entries reach pre-screen
(measured); referee-gap is the dominant killer in the historical record (Run A killed 6 of 9 rejects on
referee, Run B 3 of 9); channel-fit, demand and serve kill most of what remains. Expect **1–3
greenlight-grade candidates per 100 frame entries** — so roughly **1 from the 54-entry Negationism
list.** Note the four passes produced 45 candidates and **zero greenlights** to date. Candidates are
not the scarce good.

**Total cost to work the whole 340-entry union:** ~$0 in tooling, ~12h of agent pre-screen, ~4h of full
screening. **My recommendation is to spend ~1h of it** — the 54-entry Negationism list only, where
Operation Legacy and NCERT already sit in plain sight — and put the other 15h into packaging and serve.

**Where it breaks:** (a) Wikipedia category membership is volunteer-curated and drifts — re-pull rather
than cache; (b) the pre-screen kills are judgement calls and a cold agent will apply them
inconsistently, so the ledger must record *why* each entry died or the next pass re-litigates all 340;
(c) if anyone recurses the tree to "be thorough", the frame degrades to 4,516 entries and the work
never finishes. That is the most likely way this fails.

---

## 4. Stopping rule

The brief proposes stopping on coverage of N̂. **Reject that** — §1.2 shows the estimator's independence
assumption is violated, so coverage of N̂ is not measurable and N̂ itself is biased low.

Stop on the constraint that actually binds:

> **Primary rule — inventory.** Discovery stops while unshipped inventory exceeds 12 months of
> throughput. Measured today: 88 unshipped topics against ~3/month = ~29 months. **Discovery should
> stop now** and resume only when inventory falls below ~36 topics.

> **Secondary rule — marginal referee survival.** If discovery runs anyway, stop a frame when 50
> consecutive fresh entries produce zero candidates surviving the referee gate. Measure survival past
> *referee*, not past pre-screen: referee is the dominant killer, so pre-screen counts flatter the yield.

> **Tripwire — decorrelation, not saturation.** If a *new* frame produces candidates with near-zero
> overlap against the pool (as Wikipedia just did, 0/5), that is evidence the space is under-sampled,
> not that discovery is working. Log it and still apply the primary rule. Novelty in the candidate pool
> is not value while 88 topics sit unshipped.

---

## 5. Direct answers to the brief's questions

1. **Verdict** — **Semi-systematic.** Enumerable, verified, free frames exist (Wikipedia depth-0
   union: **340**; Contested Histories: **248**; PragerU: **6,651**), and they demonstrably reach
   regions of the space that recall does not. But no frame enumerates "weaponised historical claims"
   as such; each is a proxy with a measured, moderate-to-poor hit rate. **And the whole question is
   optimising a non-binding constraint** — see §1.1.
2. **Frames** — §2, ranked, with sizes verified by named instrument.
3. **Pipeline** — §3, deliberately reduced to a one-sitting worklist. No new code, no task, no scheduler.
4. **Stopping rule** — §4. Stop now on inventory.
5. **Unverified** — §6.

---

## 6. What I could not verify

Named explicitly, per ADR-0020. None of these are claims of absence.

1. **Reddit corpora.** r/AskHistorians FAQ index and r/badhistory. `old.reddit.com` JSON endpoints
   returned **HTTP 403 Blocked**; `WebFetch` on `www.reddit.com` refused. Both corpora exist. I could
   not size or sample them. **This is the biggest gap in the assessment** — r/badhistory is plausibly a
   better frame than Rank 1 and I could not test it.
2. **Snopes history vertical.** `WebFetch` → **HTTP 402 Payment Required**. Size and composition unknown.
3. **Google Fact Check Tools API hit rate.** API confirmed real and free (I5) but **no key in the repo**,
   so I ran zero queries. My "expected low yield" is reasoning, not measurement.
4. **All *History in Dispute* TOCs.** I verified the series, its 21 volumes and ~1,000 essays (I5, publisher
   figures — *not independently counted*) and the archive.org access wall (I3). **I retrieved no volume's
   table of contents,** so the ~1,000 entry titles remain un-enumerated and the frame's real hit rate is
   unmeasured. Whether **UGent library access** (used elsewhere in `research/`) covers Gale eBooks is
   **unchecked**.
5. **archive.org search-inside.** `api.archivelab.org` **timed out** (WinError 10060); likely defunct. I did
   not find an alternate route into lending-restricted full text.
6. **Contested Histories: 600+ vs 248.** The public WP API exposes 248 `resources-new` (I4). The 600+ figure
   is the project's own claim about its internal database. I did not obtain the form-gated downloadable
   cases list, so I cannot say whether ~350 cases are simply unexposed or the claim is aspirational.
7. **PragerU content.** I read **titles only** (I2). Title keywords undercount — a video can make a
   historical claim without saying so in the title. The 4.5% density is a floor, and my kill of Rank 4
   rests partly on it. The kill is also supported by the pre-referee argument and by Run A's independent
   ID-verified finding, so I hold it — but the density number alone would not carry it.
8. **Georg Eckert Institute.** One WebSearch (I5) surfaced no searchable controversy database. **I did not
   query gei.de directly.** Not found ≠ does not exist.
9. **Parliamentary / congressional historian testimony.** govinfo and Hansard APIs are free and plausibly
   enumerable. **Entirely unassessed.**
10. **Hit rates generally.** The one measured rate (17%) comes from a **single random draw of 30**, judged by
    me against the brief rather than run through the actual screen. Confidence: low on the point estimate,
    moderate on the ordering, **high on the zero-overlap finding** (§1.2), which is the load-bearing result.
11. **Retraction/erratum literature.** Dropped on reasoning without querying any instrument.
