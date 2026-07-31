# CTR Thumbnail Findings — served-cohort recompute (corrected 2026-07-29)

**Status:** Recomputed and reconciled. **Informational only — no gate or checker was
changed.** This supersedes the June 27th “FULL-56 VALIDATION” table and the
high/low-extremes recipe previously in this file.

## Decision summary

- The channel does **not** have enough served videos to validate a thumbnail-feature
  predictor.
- `surface_ctr` contains 56 videos, but **38 have fewer than 1,000 lifetime Browse
  impressions**. Only 18 clear that floor.
- `thumbnail_features` is frozen at 47 tagged videos. After joining it to
  `surface_ctr`, the served-and-tagged cohort is **n=17**; several feature arms shrink
  to n=1–4.
- **Red is neither a winner rule nor a poison rule.** Its sign changes with cohort
  selection and Guatemala inclusion. Do not prescribe or penalize red from this data.
- Document-as-focal remains directionally negative, but only **2 of 17** served tagged
  videos carry the flag. That is a hypothesis, not a validated gate.
- Busy composition, creator face, emotional face, and clean map are also unvalidated.
  Their deltas are unstable, near zero, or supported by tiny arms.

The only binding thumbnail checks should continue to come from independent necessary
conditions: technical compliance, feed-size legibility, and title↔thumbnail coherence.
Those are craft filters, not predictions from this dataset.

---

## Source and method

**Data surfaces**

- `analytics.db.surface_ctr`: 56 rows; lifetime Browse impressions and Browse CTR from
  the manual Studio export captured June 27th. The table has no timestamp column and no
  writer, so it is historical/directional rather than current.
- `analytics.db.thumbnail_features`: 47 hand-tagged rows (`doc`, `cf`, `em`, `map`,
  `busy`, `red`); no writer and no operation taxonomy.
- `analytics.db.videos`: title lookup and channel-video membership.

All reads were made through `AnalyticsStore.execute()`. The robustness cut is
`browse_impr >= 1,000`. Reported deltas are **percentage-point differences between
median Browse CTR for flag=1 and flag=0**.

Why Browse: this is the cold feed where the thumbnail has to earn the click. Using
overall Studio impressions, as the July 28th first recompute did, left 40 videos above
1,000 and did not test the 38-of-56 Browse-serve problem that triggered this audit.

---

## Recomputed feature deltas

| feature | all tagged n (yes/no) | all tagged Δ | served n (yes/no) | served Δ | served excluding both Guatemala videos |
|---|---:|---:|---:|---:|---:|
| document as focal | 47 (13/34) | −0.37 pp | 17 (2/15) | **−1.67 pp** | −1.59 pp (2/13) |
| creator face | 47 (11/36) | −0.44 pp | 17 (4/13) | −1.35 pp | **+0.35 pp** (4/11) |
| emotional face | 47 (2/45) | −0.49 pp | 17 (1/16) | +0.11 pp | +0.21 pp (1/14) |
| clean map | 47 (24/23) | +0.01 pp | 17 (11/6) | +0.16 pp | +0.08 pp (9/6) |
| busy composition | 47 (26/21) | −0.29 pp | 17 (8/9) | −1.35 pp | **+0.35 pp** (8/7) |
| red pop | 47 (29/18) | +0.12 pp | 17 (10/7) | +0.67 pp | **−0.23 pp** (8/7) |

### Interpretation

- **No “CONFIRMED good/bad” verdict survives.** The served cohort is too small for
  feature-level conclusions, and the arms are often badly imbalanced.
- **Map is effectively null** in every defensible cut. The two Guatemala thumbnails
  explain much of the intuitive “map/red wins” story, but similarly tagged thumbnails
  range from 3–6% Browse CTR.
- **Red is demonstrably unstable.** It reads +0.67 pp with both Guatemala videos and
  −0.23 pp without them. The correct verdict is **unmeasurable**, not winner or loser.
- **Busy is also unstable.** It reads −1.35 pp in the served cohort but +0.35 pp after
  removing both Guatemala videos. The best-served JD Vance thumbnail is itself tagged
  busy, showing that the six booleans do not capture the actual visual operation.
- **Document-focal is the only direction that does not reverse**, but n=2 flagged
  cases cannot validate a channel rule. A page of unreadable body text may still fail
  the independent feed-size legibility filter; that is a different, defensible claim.
- **“Emote if a face is shown” has no channel evidence.** Only one served thumbnail is
  tagged both creator-face and emotional.

## What the old extremes audit can still say

The six highest- and six lowest-CTR thumbnails remain useful examples to inspect, but
they cannot supply a shared winner recipe:

- high CTR mixes maps, faces, memes, stamps, and no-overlay compositions;
- low CTR mixes documents, maps, faces, paintings, and charts;
- title, topic fame, traffic surface, publication era, and thumbnail all change at once;
- therefore the audit is descriptive, not causal.

The old prescriptions—“clean map wins,” “red conflict pop,” “documents/charts kill,”
and “only an emoting face works”—are retired as **own-channel data claims**.

---

## Craft defaults that remain independently justified

These may guide a concept without pretending the channel data predicts CTR:

1. **Pass technical and feed-size legibility checks.** Small body text must resolve or
   be removed.
2. **Keep title and thumbnail coherent while preserving a curiosity gap.**
3. **Catch typos and rendering defects.**
4. **Start with one clear visual operation and few competing elements.** This is a
   craft default to test, not a measured channel law.
5. **Use color—including red—only when the composition calls for it.** There is no
   channel-specific red rule.

---

## Review checkpoint before enforcement changes

No enforcement surface was edited in this task. If the owner accepts these conclusions,
the next bounded change would be reviewed separately:

1. remove the stale `n=47 / −0.7% CTR` predictive claim from
   `tools/preflight/thumbnail_checker.py` Rule 6 while preserving the independent
   feed-size-legibility concern;
2. decide whether “busy composition” remains a necessary-condition craft review or
   loses its fixed score deduction;
3. remove downstream claims that red is the channel’s data-backed “look-here signal”;
4. keep all resulting checks as filters, never clickability predictions (ADR-0007).

Until that review happens, this file supplies **no new gate**.

---

## Data needed for a real conclusion

- Native Test & Compare or another within-video randomized comparison.
- A live video receiving enough traffic to accumulate at least 1,000 impressions in the
  read window; dead back-catalog swaps cannot answer the question.
- A reproducible thumbnail tagging process that records the actual operation
  (COMPRESSION, MECHANISM REFRAME, VISUAL ANSWER, LOCATION PROOF, etc.), not only six
  booleans.

With only 17 served-and-tagged videos, every feature conclusion remains a hypothesis.
