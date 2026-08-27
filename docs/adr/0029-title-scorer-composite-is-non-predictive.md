# ADR-0029: The title_scorer composite is non-predictive of CTR on this channel

**Status:** Accepted — 2026-08-27

## Context

ADR-0012 established filters-decide/scores-inform, and ADR-0028 excluded composite scores from normal
front-room packets. Both were architectural judgements. Neither measured whether the
`tools/title_scorer.py` composite actually predicts anything.

It was never checked against outcomes in roughly a year of use. The creator's own account on
2026-08-27 was that the scoring tools "don't produce good results / videos don't get clicks."

That is now measured. Source: `channel-data/analytics-exports/Table data.csv`, the YouTube Studio
export covering 22 July 2025 – 23 July 2026, which carries per-video impressions and impression CTR.
Method: score every published title with `score_title()`, keep the 47 with ≥1,000 impressions so CTR
is meaningful, and correlate the composite against actual CTR.

**Result.**

| Score band | n | mean CTR | median |
|---|---:|---:|---:|
| 90–100 | 16 | 3.69% | 3.09% |
| 70–89 | 18 | 2.78% | 2.35% |
| under 70 | 13 | 2.63% | 2.26% |
| **exactly 100** | **4** | **2.67%** | **2.94%** |

Spearman rank correlation **+0.173** (n=47). Channel mean CTR across the set: **3.05%**.

The failure is specifically at the top of the scale. A perfect 100 predicts **below-average** CTR —
worse than the band beneath it. Two inversions make the practical cost concrete:

- *"How the KGB Weaponized Palestinian Resistance"* — **7.90% CTR**, scored **67**.
- *"Israel vs Palestine. The Document Everyone Cites…"* — **1.60% CTR**, scored **100**.
- *"The Country That Might Disappear"* (the 30,762-view breakout) — **7.66%**, scored **82**.
- *"The Berlin Conference…"* — scored **22**, and outperformed all four perfect scores at 3.66%.

Acting on the score would have moved the creator from a 7.90% title to a 1.60% one.

A weak-but-directional signal would be tolerable in an enrichment field. A maximum score that
predicts below-average performance is a calibration failure at exactly the point a human acts on it.

## Decision

The `title_scorer` **composite score is non-predictive** and must not appear as guidance anywhere a
human reads it as advice.

What stays, because it is mechanical rather than predictive:

- `find_search_anchor()` / `has_search_anchor()` — measures real search volume (ADR-0023).
- `detect_clickbait()` / `hard_rejects` — a brand rule, not a prediction.

`tools/preflight/packaging_lock.py` is unchanged. It already treats the composite as enrichment,
explicitly *"Read, never gates; cannot upgrade a filter FAIL."* The gate was never the problem.

`.claude/rules/packaging.md` is corrected: it presented `title_scorer.py` as the title-generation
tool and carried a per-pattern CTR figure attached to the wrong pattern (see ADR body below).

**The general rule this establishes:** any tool producing a number a human uses to make a decision is
either checked against real outcomes, or it carries a non-predictive label. An unvalidated number in
a guidance document is worse than no number, because it displaces judgement.

## Also corrected

`.claude/rules/packaging.md` claimed *"Declarative = default (3.8% CTR)"*. Measured on the same 47
titles:

| Pattern | n | mean CTR |
|---|---:|---:|
| versus | 9 | 3.88% |
| how_why | 5 | 3.75% |
| declarative | 26 | 2.82% |
| colon | 6 | 2.41% |

Declarative is the second-lowest at **2.82%**; the 3.88% belongs to `versus`. **These differences are
within noise at these sample sizes** and must not become the next unvalidated rule. Recorded as a
correction to a specific wrong number, not as evidence that `versus` titles are better.

## Consequences

The channel has no validated title-selection instrument. That is the honest state, and it is better
than a miscalibrated one, because a 100 was actively misleading.

The working replacement hypothesis — that titles naming an actor performing an act with a stake
outperform topic, myth and method framings — is recorded in
`channel-data/PACKAGING-DIAGNOSIS-2026-08-26.md` and is **derived from this same 47-row sample**. It
therefore has no more standing than the composite it replaces until tested on data it was not drawn
from. **Superseded on method by ADR-0030:** the back-catalogue retitle test named there is not
runnable at this channel's current impression volumes. The hypothesis can only be tested
prospectively across new uploads.

This measurement is re-runnable from the CSV whenever a fresh Studio export lands, and should be
re-run before any future title tool is trusted.
