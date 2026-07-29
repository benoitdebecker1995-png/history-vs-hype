# Thumbnail feature rules, recomputed on served videos only

**Date:** 2026-07-28 · **Supersedes the validation table in** `CTR-THUMBNAIL-FINDINGS-2026-06.md`
**Source:** `thumbnail_features` ⋈ `studio_ctr_rows` (lifetime Studio export, 2026-07-23), n=47 joined.

## Why this was run

The enforced rules in `tools/preflight/thumbnail_checker.py` (RULE 6 and friends) come from median CTR
deltas computed across all 47 tagged videos. But **serve is wildly unequal on this channel**: one video
holds 292,398 of ~500,000 lifetime impressions, and the median video has **2,258**. A "median CTR" over
that population is mostly a median over three-digit-impression noise.

So: recompute the same deltas at increasing impression floors. A real image effect should survive. An
artifact of which videos happened to get served should not.

## Result

| feature | floor 0 (n=47) | floor 1,000 (n=40) | floor 5,000 (n=13) |
|---|---:|---:|---:|
| document-as-focal | **−0.73** | **−0.73** | *untestable — 1 of 13* |
| creator face | −0.10 | −0.16 | −0.98 |
| clean map | **+0.64** | **+0.64** | **−1.72** ⚠ *reverses* |
| busy composition | **−0.48** | −0.54 | −0.15 *collapses* |
| red pop | −0.68 | −0.71 | −0.28 *collapses* |

## What this means — and what it does NOT mean

**It does not mean maps are bad.** The floor-5,000 map arm is 10 videos against **3**, and those 3 are
JD Vance (9.41%), Crusades (5.47%) and Sol Invictus (2.48%). A median of three is one video wide. The
reversal is noise.

**The real finding is that both cuts are fatal, in opposite directions:**

- At **floor 0**, 34 of 47 videos sit below 5,000 impressions. The deltas are dominated by videos YouTube
  barely showed to anyone — you are measuring the algorithm's serve decision, not the image's clickability.
- At a **meaningful floor**, there are only 13 videos and one arm routinely drops to n≤3. Nothing can be
  computed.

**So the six-boolean feature rules cannot be validated with the data this channel has.** Not "they are
wrong" — *unvalidatable*. `thumbnail_checker.py` currently applies fixed deductions derived from the
floor-0 numbers as if they were established. They are not.

## The sharper observation: the taxonomy doesn't describe the winners

The four best-served-and-clicked images:

| CTR | impressions | doc | face | map | red | busy | video |
|---:|---:|:--:|:--:|:--:|:--:|:--:|---|
| **9.41%** | 9,969 | 0 | 0 | 0 | 0 | 1 | JD Vance / child sacrifice |
| **9.18%** | 44,295 | 0 | 0 | 1 | 1 | 0 | Guatemala vs Belize (ICJ) |
| **7.66%** | 292,398 | 0 | 0 | 1 | 1 | 0 | Guatemala — country that might disappear |
| **5.47%** | 10,036 | 0 | 0 | 0 | 0 | 0 | Crusades primary sources |

**They share nothing on these six flags** except "no document" and "no creator face" — and one of them is
flagged *busy*, which the rules penalise. The two Guatemala images are near-identical on the flags to the
India–Pakistan image at 3.17% and the Berlin Conference at 3.66%.

**Six booleans do not capture what makes these images work.** That is consistent with what
`OUTLIER-THUMBNAIL-CORPUS.md` already found niche-wide ("outlier patterns are channel-anchored, not
niche-wide"; every aggregate signal weakened as n grew), and with ADR-0007's rule that pre-publish
thumbnail checks are **filters, never predictors**.

## Actions

1. **Demote the feature deltas from CONFIRMED to UNVALIDATED** in `CTR-THUMBNAIL-FINDINGS-2026-06.md`.
   They are not measurements of image quality; they are partly measurements of serve.
2. **Keep `thumbnail_checker.py` running, but as necessary-condition filters only** — legibility, overlay
   word count, curiosity gap, no-creator-face. Those are craft constraints with independent justification.
   The point *scores* should not be read as predictions. This is ADR-0007's position; the docs had drifted
   from it.
3. **The one surviving filter stands:** no `cf=1` (creator face) video has ever cleared 4% CTR (max 3.83,
   n=8–11 depending on cut), and the direction strengthens under a floor rather than collapsing. Necessary,
   not sufficient.
4. **Tag the channel's own thumbnails with the OPERATION taxonomy** (COMPRESSION, MECHANISM REFRAME, VISUAL
   ANSWER, TITLE REPETITION, LOCATION PROOF, AESTHETIC HOOK). That is the variable `/thumbnail` and
   `thumbnail-critic` actually reason in, and it has **never been recorded for a single HvH image** —
   `thumbnail_features` has six booleans and no operation column, no writer script, and covers 47 of 59
   videos. Until that exists, the generator's core decision variable is validated only against 30 outliers
   on eight *other* channels.
5. **Stop deriving new thumbnail rules from cross-sectional own-channel CTR.** With 13 meaningfully-served
   videos it cannot support feature-level conclusions. Within-video swaps are the only design that can —
   see the 5 uncollected experiments in `swap_experiments`.

## Honest limits of this analysis

- `studio_ctr_rows` is a lifetime export dated **2026-07-23**; CTR is lifetime, not launch-window.
- `thumbnail_features` covers **47 of 59** videos and was hand-tagged in a one-off session with no writer
  script — it cannot be regenerated or extended without redoing that by hand.
- Impression floors are correlated with topic, publish date and channel size at publish time. None of the
  cuts above control for those. **That is the point:** if a delta cannot survive a crude robustness check,
  it should not be enforced as a rule.

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
