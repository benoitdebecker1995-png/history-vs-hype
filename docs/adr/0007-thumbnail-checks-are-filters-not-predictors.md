# 0007 — Pre-publish thumbnail checks are necessary-condition filters, not clickability predictors

**Status:** Accepted (2026-06-14)

## Context

The thumbnail tooling implied it could score "clickability" before publish. `thumbnail_image_audit.py` rated thumbnails on **CLIP differentiation** (visual distance from the competitor shelf) and labelled a low score "STRONG pattern-break (good)", adding +5 / −20 to a 0–100 verdict. In practice this produced **false confidence**: the channel's two visibly-weak Kurdistan drafts (a muddy coin blob and a fragmented map) both scored **100/100 "STRONG"**, because a low-information blob is, trivially, *unlike* everything else on the shelf. `thumbnail_checker.py` likewise scored *floors* (presence of a text overlay) and actively penalised the on-voice dossier look (document-only −15, no-map-on-territorial −20).

Investigation (2026-06-14) established: there is **no pre-publish clickability oracle**. CLIP measures difference, not clicks; aesthetic judgement is opinion; the channel's own CTR is n<30 and confounded by topic + title. The only ground truth is native A/B (`ctr_snapshots`). Calibration on the 5 real winner/loser thumbnails confirmed that the one *image-computable* failure is feed-size illegibility (Laplacian-variance at 160px cleanly isolates the blob); the losing-but-legible thumbnails fail on *semantic* grounds (abstract overlay, multiple focal points, AI figure) that pixels cannot reveal.

## Decision

Pre-publish thumbnail tools are **necessary-condition FILTERS**, never clickability predictors:

- `thumbnail_image_audit.py` — verdict driven by a **computed feed-size legibility gate** (catches mushy blobs) + tech compliance. **CLIP differentiation is informational only** (no score impact; relabelled DISTINCT/TYPICAL/SIMILAR).
- `thumbnail_checker.py` — verifies concept necessary-conditions incl. a **curiosity-gap check** (overlay must not duplicate the title). The harmful map/document penalties are removed.
- Semantic conditions (curiosity-gap beyond string overlap, single-focal-point, AI-figure, voice) are handled by the concept checker, the `thumbnail-critic` agent, and human review — **not** claimed by any image score.
- **The only clickability verdicts are *live*, and they are two distinct signals — don't conflate them:** native **Test & Compare** (the *variant* verdict — which of N thumbnails wins, optimised for watch-time) and the **reach-window CTR trend** in `ctr_snapshots` (what the 48h swap protocol reacts to). Operation choice draws on the real outlier corpus. *(Correction 2026-06-14: 0 Test & Compare experiments have ever actually run, and at this channel's traffic A/B isn't yet viable — so the operative near-term verdict is the reach-window trend + SINGLE-VARIABLE before/after swaps, not A/B.)*

## Consequences

- **Good:** tooling stops greenlighting weak thumbnails; effort flows to the proven levers (clarity, curiosity-gap, operation) and to A/B. Honest about what is and isn't knowable.
- **Cost:** no comforting single "this thumbnail will work" number before publish; the verdict requires shipping 3 variants and waiting for CTR.
- **Reversible only by** re-introducing a predictive pre-publish score — which is the failure mode this ADR exists to prevent.

See: `.claude/REFERENCE/THUMBNAIL-CRAFT-RECIPE.md`, CONTEXT.md (Packaging / thumbnail terms).
