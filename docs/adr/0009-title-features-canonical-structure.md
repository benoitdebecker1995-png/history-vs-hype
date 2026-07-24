# title_features: one canonical home for title structure

**Date:** 2026-06-25
**Status:** accepted

Peer to ADR-0004/0005/0008 (the store/resolver seams). This ADR exists because "what structural pattern is this title, and what features does it carry" was implemented ~5 times across the codebase, the copies had **drifted from each other and from the gold standard**, and a `/improve-codebase-architecture` pass (2026-06-25) surfaced it. Future runs that re-find scattered title classifiers should be answered with this ADR.

## What the seam is

`tools/title_features.py` — pure `str -> features`, no DB, no scoring, no I/O.

- **`pattern(title)`** — the 6-class structural taxonomy: `versus`, `the_x_that`, `colon`, `question`, `how_why`, `declarative`. Priority order matters (`versus` and `the_x_that` before `colon`).
- **Feature predicates** — `has_year`, `has_specific_number` (excludes "200-Year-Old" duration adjectives), `has_active_verb`, `has_named_entity`, `has_evidence_promise`, `has_controversy_frame`.

`title_scorer.py` holds the canonical logic's *origin* and now imports it back, re-exporting `detect_pattern` for backward compatibility. The analytics pattern-classifier copies delegate to `pattern()`.

## Scope — what this is NOT

This module owns **how a title is phrased**, not **what the video is about**. Topic classification (`territorial` / `ideological` / `colonial`) is a separate concept and stays where it lives: `growth_data.classify_title`, `discovery.intent_mapper.classify_title`, `intel.topic_vocabulary.classify_title`. Those three share the verb "classify_title" but answer a different question; the architecture review's raw count of "9 implementations" conflated them by name. Merging them here would couple two unrelated concepts. **Do not add topic rules to title_features.**

Also out of scope (single-home, not duplicated): `patterns.detect_title_pattern` — the channel title-*template* names ("[X]'s [Noun] Problem"), a distinct aggregation taxonomy.

## The drift this fixes

Five copies of the structural classifier existed; **none matched the title_scorer gold standard they each claimed to match** (their docstrings literally said "matching title_scorer.py"):

- `ctr_by_source_analysis.classify_title_pattern` and `traffic_analysis.classify_title_pattern` — byte-identical to each other; treated `|` as colon, lacked `the_x_that`, used broad interrogative-prefix question detection.
- `build_deliverables.classify_title_pattern` — same, plus extra `can/could` prefixes.
- `title_scorer.detect_pattern` — the richest (has `the_x_that`), keyed `question` off a trailing `?` only.

The feature predicates had **divergent correctness**, not just divergent code: `title_scorer.has_specific_number` excludes "200-Year-Old"; `patterns.extract_title_structure` used a naive `has_number = \d+`.

## Decision — canonical = title_scorer's logic

Per the design grill, `title_scorer`'s versions are canonical (it is the tested gold standard, 3 test files). The three recompute-each-run copies adopt it. This **drops** the copies' `|`-as-colon and broad-question-prefix heuristics — a deliberate, accepted semantic shift. It is safe because those copies write to **in-memory report fields recomputed each run** (`vid['title_pattern']`), not stored buckets; the reports simply align with the scorer's taxonomy on the next run. No migration, no historical rewrite.

If the `|`-as-colon / interrogative-prefix breadth is later judged worth keeping, the right move is to enrich the canonical `pattern()` (and re-baseline title_scorer's tests), not to re-fork.

## Migration — staged

First cohort (2026-06-25): the recompute-each-run copies — `ctr_by_source_analysis`, `traffic_analysis`, `build_deliverables` — now delegate to `pattern()`. `title_scorer` imports its own logic back.

**Deferred** (recorded so a future run doesn't think they were missed):

- `backfill_high_impact.classify_title_formula` — returns a **multi-label tag list** (structural + `evidence_promise` / `caps_clickbait` / `has_number`) and **persists** it to `keywords.db` `title_variants.formula_tags` (INSERT at line 76). Unifying it needs a tag-list adapter over `title_features` plus a stored-data continuity decision. Different shape, real persistence — its own pass.
- ~~`preflight/scorer._classify_title_pattern` — returns a `(pattern, score, issues)` tuple entangled with preflight scoring. Migrate the pattern half when preflight is next touched.~~ **Closed 2026-07-01:** inspection showed it was *fallback-only* (the primary path already takes its pattern from `title_scorer` → `title_features`). Lifted to module level as `_classify_title_pattern_fallback`, taxonomy delegated to `pattern()` (adopting `how_why` in place of the split `how`/`why` labels — matching what the primary path already reports), score/penalty policy kept local. Pinned by `tools/tests/test_preflight_title_fallback.py`.
- `patterns.extract_title_structure` — its naive feature dict could read `title_features` predicates, upgrading correctness; deferred to avoid touching the patterns.py report shape in this pass.

## Considered alternatives

- **Pattern classifier only** (leave the predicates in title_scorer). Rejected — the predicates were duplicated with divergent correctness too; pulling them is the larger share of the win.
- **Leave title_scorer as the canonical home, others import from it.** Rejected — `title_scorer` is a 49KB module with DB/scoring; lightweight analytics callers shouldn't import all of it to ask "is this a versus title." A lean `str -> features` module is the honest seam.
- **Include the topic classifiers.** Rejected — different concept (see Scope).

## Consequences

- **Test surface.** `tests/test_title_features.py` (17 tests) — the canonical taxonomy and predicates had **no direct tests** before; the drifted copies had none at all. Includes the priority-ordering and `200-Year-Old` cases the copies got wrong.
- **Behavior preserved for scoring.** `title_scorer`'s full suite (niche, db, regression, generator, metadata) passes unchanged — the move is import-only.
- **Fixed 7 pre-existing stale tests.** 7 `test_hard_reject_*` assertions in `test_title_scorer_niche.py` / `test_title_scorer_db.py` failed on HEAD independent of this change — they asserted the auto-REJECT behavior title_scorer **v5 deliberately retired** (changelog C1). Updated to assert the real v5 contract: style rules (year/colon/the_x_that) produce non-fatal `style_warnings` and a grade computed from score (never `REJECTED`), while `strict=True` promotes them back to `hard_rejects` → `REJECTED` — so each test now also exercises the preserved `--strict` escape hatch. Full title suite: 131 passed, 0 failed.
- **Re-litigation guard.** Future `/improve-codebase-architecture` runs that surface "merge the title classifiers" should be answered with this ADR — including the explicit exclusion of the topic classifiers. If the deferred items above need doing, supersede rather than re-fork.
