# BLIND next-video discovery brief

**Purpose:** independent discovery of the channel's next video, deliberately withholding all prior
candidate work so the result is a genuine replication rather than a confirmation.

**What is deliberately EXCLUDED from this brief:** every candidate topic previously considered, every
reach figure previously gathered, and every conclusion previously reached — by any model or human.
The executing agent must generate candidates from primary discovery only. If you happen to arrive at
something already considered, that is a valid convergence signal; being *told* it would not be.

---

## The channel

**History vs Hype.** Evidence-based history for a general audience: primary sources on screen,
academic sourcing, page numbers. ~515 subscribers, 58 long-form videos published.

## What the creator wants to make — in his own words

> "Explaining how history works and how historians come to certain conclusions. Why for example we
> can say that Russian claims to Ukraine are bullshit."

> "Make the historical discipline more accessible… bring history closer to the people and cut through
> the ideological bullshit."

Not a debunk channel. He wants to **show the method by which a claim can be known to be false or
uncertain** — so the viewer can run the test themselves.

His investigative chain: **public claim → original evidence → source criticism → scholarly argument →
what is actually settled → what prevents greater certainty.**

He is pulled in when:
- Something is confidently stated as fact and the honest answer is "here is what the evidence permits"
- A controversial question has no clean public answer
- History is being used to win a modern political, ideological or moral argument
- Public debate reduces history to heroes and villains, or cherry-picks convenient evidence
- The public misunderstands how historians reason from incomplete, biased or conflicting evidence

He wants viewers to leave thinking: *"more complicated than I thought — he showed his sources,
disclosed his assumptions, and followed the evidence further than either camp."*

Target feelings, his own pick: *"I finally understand how this worked"* + *"history is harder and
stranger than I thought."*

**Exhibit preference (strong, not absolute):** a bounded piece of evidence the viewer can inspect —
a report, decree, telegram, manuscript, dataset, excavation, statistical series, corpus of testimony.
Something that makes the conclusion auditable rather than a matter of trusting the presenter.

**Period:** no constraint. "The topic decides."

**Ideological targets: symmetric.** Nationalist myth, pseudo-history, and claims by living political
figures all qualify, whoever is making them. He will enter a crowded topic if there is something the
incumbents missed. He will not make a current-affairs commentary video with history as background.

## Audience

Politically engaged men 25–44 in the UK, US, Germany and Canada. (Verified: vidIQ subscriber-overlap
shows this audience overlaps political-commentary channels, **not** history-hobbyist channels.)

A topic qualifies on relevance if it is active in Western political debate, shapes Western policy or
identity, or is a Western misconception about elsewhere with real consequences.

## Qualifying shapes — find examples of any

- **A** Historians genuinely disagree, and both political camps assert certainty
- **B** Facts settled, inference contested — "we agree what happened, not what it means"
- **C** One text, statistic, artifact or study carrying an entire ideological argument
- **D** Proponents are right about one part and extrapolate far beyond it

## Content-gap standard

Qualifies only if the adjudication is absent, or tiny relative to the assertion ecosystem, or existing
coverage tells the story without testing the evidence, or existing "debunks" are partisan rebuttals
that omit the strongest opposing evidence.

**A partisan counter-video is not a referee.** A referee states the strongest version of the claim,
presents evidence that genuinely supports it, presents contradictory evidence, does source criticism,
represents specialists accurately, and separates consensus from dispute from uncertainty.
**If a credible referee already exists at meaningful scale, drop the candidate. Do not rationalise.**

---

## ⛔ MANDATORY VERIFICATION PROTOCOL (ADR-0020)

A strategy claim that decides what gets made carries the same evidentiary burden as a claim that goes
on screen. **A search returning nothing is NOT evidence something does not exist.**

1. **Never write "no referee exists."** Write *"searched \<these queries\>, catalogue-checked \<these
   channels\>, did not find a referee."*
2. **Verify every reach figure and every candidate referee BY ID:**
   `youtube.videos().list(part='snippet,statistics,contentDetails', id=...)` — exact, 1 quota unit.
   If any source names a video, query that ID. **Never substitute a search for a supplied identifier.**
3. **Referee search requires ≥4 query framings** — the partisan wording proponents use, neutral causal
   wording, and combinations with *historian / evidence / debate / debunk*.
4. **Catalogue-check the 3–6 channels most likely to have refereed it**, by FULL uploads playlist.
   `vidiq_outliers` ranks on breakout/recency and omits older videos even with `sort: viewCount`;
   `intel.db` holds only ~100 recent uploads per channel. **Neither can prove absence.**
5. Tools whose emptiness means nothing here: the autocomplete scraper and yt-dlp comments are
   **bot-walled and return empty rather than erroring**; the free-source `demand_scorer` emits a
   **200/mo floor placeholder** that is not a measurement.

**Precedent:** on 2026-07-29 a "cleanest whitespace of the session" claim was written into a project
file and used to greenlight it. A 73-minute specialist adjudication with 736,169 views had existed
since 2022. Two tools were consulted, both had windows that excluded it, and their silence was read as
proof. Do not repeat this.

## Channel-fit constraints (repo facts, verify against the tree)

- **Collision:** check all published titles in `analytics.db`, plus `video-projects/_IN_PRODUCTION/`,
  `_READY_TO_FILM/` and `_BACKLOG/`. Existing projects are **eligible and ranked on merit** — flag the
  collision loudly, do not disqualify.
- **Serve is the binding constraint.** Median video reaches **302 browse impressions**; 29 of 56 got
  under 350. Topics in sensitivity-flagged categories risk limited reach, and the failure mode is
  silence you cannot diagnose. Say so where it applies.
- **Pocket risk:** audiences outside the target countries convert worst — the channel's one breakout
  took 30,469 views to 152 subscribers (5.0/1,000, its floor). Check `topMarkets` on every anchor.
- **Moderation:** 224 lifetime comments across 28 videos. He cannot arbitrate a war in his comments.
- **Anchor filter:** `tools.title_scorer.has_search_anchor()` recognises only sovereign states,
  geographic shorthands, acronyms and famous surnames, in the **first 40 characters**, and returns a
  **tuple** — read `(found, term)`. A non-geographic subject fails `packaging_lock` at lock time.
- A mechanically valid packaging lock is **not** a greenlight.

## Tools available

`WebSearch` / `WebFetch` · YouTube Data API via `tools.youtube_analytics.auth.get_authenticated_service`
· `tools.preflight.serp_title_study` · vidIQ MCP (`vidiq_keyword_research`, `vidiq_outliers`,
`vidiq_similar_channels`) · `analytics.db`, `intel.db` · repo `Read`/`Grep`/`Glob`.

## Deliver

**At most three candidates. Kill hard — two exceptional beats six polite.** Per candidate:

1. The claim as its proponents state it
2. Why this creator would obsess over it
3. Who asserts it now — names, dates, **ID-verified** reach
4. Why the target audience cares
5. Demand evidence — vidIQ volume, competition, `topMarkets`, views-per-hour where available
6. Referee-gap evidence — **the exact queries run, the channels catalogue-checked, closest adjudicators
   with ID-verified counts, and precisely what they fail to do**
7. The exhibit, and whether it is obtainable
8. Honest evidentiary map — supports / undermines / unknowable
9. Specialists and works, and the real state of scholarship
10. Provisional title + thumbnail promise, and whether it clears the anchor filter
11. Why these viewers return for the method
12. Strongest reason to kill it
13. Confidence, separately: demand · referee gap · exhibit

Then: ranked order · single recommendation · why it beats the others · what must be verified before
greenlight · **rejection log naming every candidate dropped with the ID-verified evidence that killed it.**

## Failure modes

No interesting disputes without demonstrated demand. No textbook survey questions. No generic myths or
trivia. No claims whose evidence is purely theoretical. No topics already refereed at scale. No padding
to a number. No "both sides" framing where the evidence is asymmetrical. No takedown that refuses to
state what genuinely supports the claim. **No negative claim without its instrument named beside it.**
