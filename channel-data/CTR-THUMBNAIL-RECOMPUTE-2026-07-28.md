# Thumbnail feature rules, corrected Browse-served recompute

**Corrected:** 2026-07-29 · **Authoritative conclusions:** `CTR-THUMBNAIL-FINDINGS-2026-06.md`

## Correction to the July 28th method

The first version of this note called its cohort “served videos only” but imposed its
floor on **overall Studio impressions** from `studio_ctr_rows`. That was the wrong
denominator for the reported problem: in `surface_ctr`, **38 of 56 videos have fewer
than 1,000 lifetime Browse impressions**.

This correction uses Browse impressions and Browse CTR from `surface_ctr`, joined to
the six hand-tagged booleans in `thumbnail_features`. All reads went through
`AnalyticsStore.execute()`.

- 56 videos have surface data.
- 18 videos have at least 1,000 Browse impressions.
- 17 of those 18 have thumbnail-feature tags.
- The feature deltas below are percentage-point differences in **median Browse CTR**
  between flag=1 and flag=0.

## Corrected result

| feature | all tagged n (yes/no) | all tagged Δ | Browse-served n (yes/no) | Browse-served Δ | excluding both Guatemala videos |
|---|---:|---:|---:|---:|---:|
| document as focal | 47 (13/34) | −0.37 pp | 17 (2/15) | −1.67 pp | −1.59 pp (2/13) |
| creator face | 47 (11/36) | −0.44 pp | 17 (4/13) | −1.35 pp | **+0.35 pp** (4/11) |
| emotional face | 47 (2/45) | −0.49 pp | 17 (1/16) | +0.11 pp | +0.21 pp (1/14) |
| clean map | 47 (24/23) | +0.01 pp | 17 (11/6) | +0.16 pp | +0.08 pp (9/6) |
| busy composition | 47 (26/21) | −0.29 pp | 17 (8/9) | −1.35 pp | **+0.35 pp** (8/7) |
| red pop | 47 (29/18) | +0.12 pp | 17 (10/7) | +0.67 pp | **−0.23 pp** (8/7) |

## Reconciled conclusion

**None of the six feature rules is validated.**

- Red is neither a winner nor a poison. Its sign reverses when the two Guatemala
  videos are removed.
- Creator face and busy composition also reverse sign under that sensitivity check.
- Clean map is effectively null.
- Emotional face has only one flagged case in the served cohort.
- Document-as-focal stays negative, but its flagged arm is only two videos. Unreadable
  document text can still fail an independent feed-size legibility check; this data
  does not establish a CTR rule.

The earlier claim that a “no creator face” feature rule survived is withdrawn. The
cross-sectional data cannot isolate thumbnail effects from topic, title, traffic
surface, publication era, and channel size at publication.

No checker or gate was changed. Any enforcement change requires owner review of the
corrected conclusions first.

## Honest limits

- `surface_ctr` is a lifetime, manually imported snapshot from June 27th. It has no
  timestamp column or automated writer.
- `thumbnail_features` covers 47 videos and was hand-tagged in a one-off session; it
  has no writer and no operation taxonomy.
- The 1,000-impression floor removes obvious three-digit noise but leaves only 17
  tagged videos, with feature arms as small as one or two.
- These are observational comparisons, not randomized thumbnail experiments.

---

# Addendum — the 5 swap experiments, read out at last

`swap_experiments` held five title/thumbnail rescues from June, all still `PENDING` with no post-swap
reading. `impressions_daily` now covers the whole post-swap period, so they can finally be scored.

| video | swap | baseline | post-swap impressions | verdict |
|---|---|---|---:|---|
| They Didn't Just Buy Slaves | 15 Jun, thumbnail | 1.91% / 2,672 | **218** | INCONCLUSIVE |
| Treaty of Tripoli | 26 Jun, title+thumb | 0.44% / 450 | **192** | INCONCLUSIVE |
| 1947 Partition Map | 26 Jun, title+thumb | 1.43% / 2,721 | **78** | INCONCLUSIVE |
| Hijab status symbol | 26 Jun, title+thumb | 1.38% / 2,242 | **482** | INCONCLUSIVE |
| Two Countries Split a Continent | 26 Jun, title+thumb | 3.12% / 19,388 | **127** | INCONCLUSIVE |

**None of them can be read, and the reason is the finding.** In the 33–43 days since the swaps, these five
videos received between **78 and 482 impressions each**. The Brazil video had 19,388 lifetime impressions
at baseline and has gained roughly 500 since. A post-swap CTR computed on 78 impressions and 2 clicks is
not a measurement.

**You cannot repackage your way out of not being served.** These swaps were the channel's only within-video
causal evidence, and they were spent on videos the algorithm had already stopped showing. The experiment
design was sound; the subjects were dead.

**Consequence for method:** a swap is only testable on a video still receiving meaningful impressions.
Before running one, check current daily impressions in `impressions_daily` and require a rate that will
accumulate ≥1,000 impressions inside the read window. Otherwise it produces a PENDING row that sits for a
month and then reads as noise.

**Consequence for ADR-0007's open questions:** every "confirm via A/B" deferral in the packaging docs is
still unfulfilled, and this attempt shows the naive version of it does not work at this channel's scale.
Either the swap runs on a live, still-served video, or it runs through YouTube's native Test & Compare
(which splits traffic on the *same* video, sidestepping the problem entirely) — availability unconfirmed.
