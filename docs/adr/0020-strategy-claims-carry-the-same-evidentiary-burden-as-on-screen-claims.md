# ADR-0020 — Strategy claims carry the same evidentiary burden as on-screen claims

**Date:** 2026-07-30
**Status:** Accepted
**Supersedes:** the whitespace anchor in `tools/TOPIC-RUBRIC.md` v2 (2026-06-11)

## Context

On 2026-07-29 project #64 (`64-ancient-dna-aryan-weaponised-2026`) was greenlit on the claim that
**"nobody is refereeing it from the papers — cleanest whitespace measured this session."** That claim
was written into the project's `PROJECT-STATUS.md` and drove the decision.

It was false. World of Antiquity, *"When did SANSKRIT appear in India? | The GENETIC Evidence"*
(`NQX5LlJ7YXg`), 736,169 views, 1h13m24s, published 2022-03-14, is exactly that referee. It was
missed because two instruments were consulted — `vidiq_outliers` (ranks on breakout/recency; omits
older videos even with `sort: viewCount` and `publishedWithin: allTime`) and `intel.db`
(~100 most recent uploads per channel) — and **their silence was treated as proof of absence.** The
video's ID had been supplied by the source that cited it, and was never queried.

An audit that day found the cause is structural, not incidental:

1. **The rubric asked for a claim its instrument could not produce.** The whitespace anchor read
   *"no quality English coverage of the topic = 100"*, with a top-12 SERP on 1–2 queries named as the
   method. That is a universal negative from a sample, weighted at 25% of topic selection.
2. **No document in `tools/`, `.claude/` or `channel-data/` required verifying a negative claim.**
   A grep for absence-of-evidence discipline returned nothing outside worktrees.
3. **The asymmetry.** The repo has rigorous, tiered provenance discipline for claims that go ON
   SCREEN — `primary-source` and `historian` skills, `fact-checking-protocol.md`, SOURCE-GENEALOGY,
   genealogy verdicts. It had **none** for the claims that decide WHAT GETS MADE: whitespace, demand,
   referee gaps. Those were scored, written into project files, and cited as fact with no instrument
   of record and no verification requirement.

The channel's own content teaches that absence of evidence is not evidence of absence. The apparatus
selecting its topics did not apply that to itself.

## Decision

**A strategy claim that decides what gets made carries the same evidentiary burden as a claim that
goes on screen.**

Three enforcement changes:

1. **`serp_title_study.py` now emits a "WHAT THIS STUDY CANNOT TELL YOU" block above its whitespace
   section** — the exact queries run, the sample size, an explicit statement that it cannot establish
   absence, the required phrasing (*"searched X, did not find"*, never *"none exists"*), the verify-by-ID
   instruction, and the #64 precedent. The old section is renamed **"Positioning whitespace — TITLE
   STRUCTURE ONLY (not topic coverage)"**, because that is all it ever measured. The artifact carries
   its own limits wherever it is cited.

2. **`TOPIC-RUBRIC.md` caps SERP-only whitespace at 50.** Scoring above 50 requires the
   referee-absence protocol: ≥4 query framings including partisan wording; catalogue-checking the 3
   likeliest channels (not via ranking endpoints); **verifying by ID any candidate referee named by any
   source, including another model**; and recording instruments + date in the project file.

3. **Any candidate referee supplied with an ID, URL or exact title is queried directly.**
   `youtube.videos().list(part=..., id=...)` is exact and costs 1 quota unit. A search is never a
   substitute for a supplied identifier.

## Consequences

- #64's whitespace claim is retracted in place in its `PROJECT-STATUS.md`, with the real video, its
  ID, and how the error occurred. What may survive is narrower (the 2019 Rakhigarhi press inversion
  and the four co-authors publicly contradicting each other) and **must be checked against
  `NQX5LlJ7YXg`'s contents before the project advances.**
- A mechanically VALID `packaging_lock` is **not** a greenlight. The lock tests title filters; it says
  nothing about topic viability. These were conflated on 2026-07-29.
- Existing whitespace = 100 scores elsewhere in `channel-data/` and `TOPIC-PIPELINE.md` were produced
  under the old anchor and should be treated as **≤50 until re-verified under the protocol.**
- Cost: whitespace above 50 is now materially more expensive to claim. That is the intent.

## Related

ADR-0007 (thumbnail checks are filters, never predictors) · ADR-0012 (a rule that must bind goes in
code, not prose) · `feedback-never-assert-absence-without-direct-check` in memory.
