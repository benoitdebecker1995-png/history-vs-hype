# ADR-0030: Back-catalogue retitle tests are not runnable — retire them

**Status:** Accepted — 2026-08-27
**Extends:** ADR-0029 (the title_scorer composite is non-predictive)

## Context

ADR-0029 left the channel with no validated title instrument and named a replacement hypothesis —
titles that name an actor performing an act with a stake outperform topic, myth and method framings.
The stated way to test it was a three-video back-catalogue retitle experiment: Berlin Conference,
Medieval Literacy and Sol Invictus, title only, predicted CTR recorded first, read at 28 days. It was
described as "the cheapest growth available."

Before running it, the candidates were checked for whether they still receive impressions. They do
not.

**Impressions in the 30 days to 24 August 2026** (`impressions_daily`, `keywords.db`):

| Video | Impressions | Clicks | CTR |
|---|---:|---:|---:|
| Guatemala vs Belize | 3,259 | 285 | 8.75% |
| Belize ICJ | 758 | 86 | 11.35% |
| KGB / Palestinian resistance | 368 | 29 | 7.88% |
| Spanish Inquisition | 241 | 9 | 3.73% |
| Treaty of Tripoli | 226 | 30 | 13.27% |
| **Sol Invictus** *(candidate)* | **149** | 14 | 9.40% |
| **Medieval Literacy** *(candidate)* | **61** | 6 | 9.84% |
| **Berlin Conference** *(candidate)* | **29** | 0 | 0.00% |

Channel total over the same window: 7,389 impressions, 553 clicks.

**The power arithmetic.** Detecting a move from 3% to 6% CTR at conventional power requires roughly
**750 impressions per arm**. Berlin Conference accumulates that in about **two years**. Sol Invictus,
the healthiest candidate, needs roughly five months per arm. A 28-day read would collect 27–140
impressions, whose CTR estimate carries a confidence interval wider than the effect being measured.

**The structural problem, which no candidate choice fixes.** There is no video that is both *served
enough to measure* and *converting badly enough to be worth improving*. The only two videos with real
impressions — Belize at 3,259 and its sequel at 758 — already convert at 8.75% and 11.35%. Running an
experiment on the channel's single functioning asset is not a reasonable trade.

**And the premise underneath was wrong.** A video receiving 29 impressions a month has not been
throttled by its title. YouTube has stopped serving it, and a new title does not summon impressions
that are not being offered. The 159,017 unclicked impressions recorded in
`channel-data/PACKAGING-DIAGNOSIS-2026-08-26.md` are historical; a retitle does not recover them.

## Decision

**Back-catalogue retitle experiments are retired, not deferred.** Do not propose them as a growth
lever, a validation route, or "cheap because it needs no filming." The cost is not filming time — it
is three spent titles and a sixth uninformative swap in a ledger that already holds five.

**The actor/act/stake hypothesis can only be tested prospectively, on new uploads**, where a video
receives its initial serving push and accumulates impressions fast enough for CTR to mean something.

That makes it a **season-long question, not a month-long one**. A single upload is one data point;
a title *rule* needs several. The discipline that makes it eventually answerable is the one already
required before publication: intended audience, expected traffic mode, package hypothesis, main
uncertainty — recorded in `PROJECT.md` *before* upload, then read at 7 and 28 days.

Volhynia is the first entry. Its prediction is already recorded.

## Consequences

The channel has no fast route to validating a title rule. That is the honest state. The alternative —
running an underpowered test and reading a result off 40 impressions — is how unvalidated rules got
into the guidance layer in the first place (ADR-0029).

Retitling a dead video may still be worth doing for *discoverability* reasons — a better search anchor
on a video with genuine search demand is a different argument, resting on the measured anchor filter
(ADR-0023) rather than on a CTR prediction. That is not this test and must not be reported as it.

## Caveat on the data

`impressions_daily` is populated from the YouTube Reporting API and may not capture every surface.
Channel CTR over this window reads 7.48%, well above the 3.05% mean computed from the Studio export
in ADR-0029, which suggests the two sources see different slices. **Get a fresh Studio export before
treating these absolute numbers as complete.**

The *relative* picture is not in doubt and is what this decision rests on: three orders of magnitude
separate Belize from Berlin Conference, and no reasonable reading of either source closes that gap.
