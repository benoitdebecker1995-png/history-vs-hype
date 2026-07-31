# ADR-0019 — Own-channel thumbnail features are informational; structural norms may bind

**Status:** Accepted · **Date:** 2026-07-29  
**Extends:** ADR-0007. **Supersedes nothing.**

## Context

ADR-0007 established that pre-publish thumbnail tools are necessary-condition
filters, never clickability predictors, and removed map/document penalties.
`tools/preflight/thumbnail_checker.py` later drifted back into predictive scoring:
document-as-focal and busy-composition descriptions each deducted 10 points, while
the document rationale cited a retired all-tagged `n=47` CTR comparison.

The corrected Browse-served recompute in
`channel-data/CTR-THUMBNAIL-FINDINGS-2026-06.md` shows why those deductions cannot
bind:

- 38 of 56 videos have fewer than 1,000 lifetime Browse impressions;
- only 17 sufficiently served videos also have thumbnail-feature tags;
- document-as-focal has only 2 flagged examples in that cohort;
- busy composition changes from −1.35 percentage points to +0.35 when the two
  Guatemala videos are excluded;
- creator face also reverses, map is effectively null, and red is unstable.

None of the six hand-tagged features is validated. Cross-sectional CTR cannot
separate the thumbnail from topic, title, traffic surface, publication era, or
channel size at publication.

That finding does **not** invalidate every independent evidence base. Overlay
presence comes from a different dataset and question: 87% of a classified
650-thumbnail competitor corpus uses text. That niche-wide structural norm is
large enough to require REVIEW when a concept has no overlay. It is still not a
prediction that adding text will make the thumbnail click.

A new ADR is required because ADR history is append-only: the later checker drift
must be recorded as a new decision rather than silently rewriting ADR-0007.

## Decision

Bring `thumbnail_checker.py` back into line with ADR-0007:

- Own-channel feature observations remain visible as informational notes but
  carry **no score impact**: creator/talking-head use, document-as-focal,
  map/color choice, and busy composition. Stock imagery also remains a craft
  note rather than a mechanical condition.
- Do not turn any served-cohort delta into a deduction. The observational
  `n=17` channel cohort is hypothesis-generating only.
- A text-free concept is a structural REVIEW failure, grounded in the separate
  niche corpus (`87%`, `n=650`). Overlay presence is a floor, not a clickability
  bonus; adding an overlay cannot produce a predictive “winner” verdict.
- Keep the independently justified necessary conditions unchanged:
  rendered-image feed-size legibility, technical compliance, and the
  title↔thumbnail curiosity-gap/duplication check.
- Overlay absence and title duplication each downgrade the concept to REVIEW.
  Overlay-length scoring remains a feed-size legibility proxy. Map and color
  remain informational.
- Nothing moves into `tools/preflight/packaging_lock.py`; no feature in this
  recompute has earned a binding gate.

The checker retains its existing result shape. Informational observations stay in
`issues` for human review, but they do not lower `score` or change `verdict`.

## Consequences

- A concept can pass the mechanical conditions while still displaying craft notes.
  PASS means “no necessary-condition failure detected,” never “this will click.”
- The no-text pin is deliberately restored to REVIEW 75. Talking head, stock
  imagery, document-focal, and busy composition still keep a score of 100 when
  no binding condition fails.
- The review reproducer changes from PASS 100/100 to REVIEW 75/100:
  `a photo of me talking to camera, no text, cluttered background, stock photo`.
  Only overlay absence binds; creator face, clutter, and stock remain notes.
- Published project #54 (Spanish Inquisition) provides the real-tree calibration
  example: the pre-change checker returned REVIEW 60/100 because its three-concept
  brief contained the words `host` and `cluttered`; the corrected checker returns
  PASS 100/100 while retaining both observations as informational notes. Its
  overlay-length and title-curiosity checks remain unchanged.
- Reversal requires evidence strong enough to supersede ADR-0007 and this ADR,
  ideally a sufficiently powered within-video randomized comparison rather than
  another cross-sectional feature table.
