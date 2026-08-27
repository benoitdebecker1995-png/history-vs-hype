# 0023 — Search-anchor fame is measured, not listed

**Status:** Accepted (2026-08-03)

## Context

FILTER 1 of the packaging lock (ADR-0012) asks whether a title leads with a famous searchable
term. The reasoning is sound and unchanged: a 515-sub channel has no ranking power for a bare
obscure proper noun, so the recognisable parent keyword goes in the first ~40 characters and the
obscure entity is the reveal. What was broken was the **recognition mechanism**.

`has_search_anchor()` decided PASS/FAIL by membership in `HEAD_TERMS`, a hand-maintained set of
~240 strings. Because the filter is BINDING, a term missing from the set is not a soft miss — it
blocks the title. The set has been patched three times for exactly that reason in eight weeks, each
time after it rejected something famous:

| Date | Rejected | Measured demand | Fix applied |
|---|---|---|---|
| 2026-07-01 | "Zelensky" (#62) | world figure | appended to the set (ADR-0012) |
| 2026-07-30 | "Alan Turing" (#65) | 98,056/mo | appended to the set (v6.1 A2) |
| 2026-08-01 | "Constantine" (#67) | 115,704/mo | *this ADR* |

The #67 case is the one that makes the pattern undeniable. "Constantine" failed while "Vatican"
(95,503/mo) passed — a term with **more** measured demand than the one the set happened to contain.
"Pope", "Constantinople", "Rome" and "Catholic Church" failed too. Title candidates were regenerated
to avoid all of them under a constraint that did not exist; when the terms were patched in locally,
five candidates gained +12 each and one went 80/B → 92/A. The scorer's own docstring had already
diagnosed it — *"The list was sovereign-state biased by construction; fame is the test"* — and then
prescribed more strings.

A fourth append would fix the fourth instance and leave the mechanism intact for the fifth. The
defect is not which strings are in the set. It is that **fame was defined as "somebody remembered to
type it"**, in a filter that blocks work when the memory fails.

A separate defect found in the same pass is recorded here because it changes the same filter's
verdicts: the 40-char window was applied as `title[:40]`, which truncates mid-word, so a head term
that *began* inside the window but crossed its edge could not match its own word boundary. That
false-FAILed the channel's only breakout ("The Country That Might Disappear: Guatemala vs Belize",
Guatemala at char 34, 292,398 impressions at 7.66% CTR) and three other live titles.

## Decision

**A term is a search anchor if it is CURATED or MEASURED. Measurement is the general rule; the
curated set is a convenience floor.**

- **Measured (`ANCHOR_VOLUME_FLOOR = 1000`).** Any term with a verified monthly search volume at or
  above the floor recorded in `keywords.db` anchors, with no code change. The floor is deliberately
  the *same number and units* as the `/greenlight` demand gate's GO line (≥1,000/mo) — one volume
  vocabulary in the repo, not two. Recognition matches word n-grams beginning inside the window
  against the recorded terms, so a multi-word phrase ("Donation of Constantine") is recognised as
  itself, not as a bag of words.
- **Curated (`HEAD_TERMS`, `ALLOWED_ACRONYMS`).** Kept as a zero-setup fast path so a fresh clone
  with an empty keyword store still recognises "France". It is explicitly **not** the definition of
  fame, and the set now carries a stop-note at its tail pointing at the recording command.
- **The repair path is a measurement, not an edit.** `python -m tools.title_scorer --record-anchor
  "<term>" --volume <n> --anchor-source vidiq-YYYY-MM-DD` writes through `KeywordStore`. `--volume`
  below the floor is refused and `--anchor-source` is mandatory: an unsourced number is not
  evidence. **The FAIL message itself prints this command**, because a FAIL means one of two very
  different things — "this title leads with something obscure" (rewrite the title) or "this term is
  famous and nobody has measured it" (record it) — and the creator hitting it mid-greenlight is the
  person best placed to tell which.
- **Provenance is recorded in the lock block.** `find_search_anchor()` returns an `AnchorMatch`
  carrying the term, its position, and either "curated head term" or the volume plus the source tag.
  `packaging_lock` writes that line, so every PASS says *why* it passed and is auditable later.
  `has_search_anchor()` keeps its `(found, term)` tuple contract for existing callers.
- **The window is a START position**, not a substring: a head term must *begin* within
  `ANCHOR_WINDOW_CHARS` (40) and may run past it. The window itself is unchanged — no catalogue
  title has a head term starting at or beyond 40, so there is evidence for measuring it correctly,
  none for widening it.
- **No network call in the recognizer.** The volume table is read from `keywords.db` once and cached
  per process, re-read only when the file changes. `has_search_anchor` runs inside scoring loops;
  per-call I/O would have been an unacceptable design.

Seeded 2026-08-03 with vidIQ measurements for the terms the defect report named: Rome 265,693 ·
Constantine 113,206 · Vatican 100,602 · Alan Turing 87,786 · Pope 69,409 · Constantinople 50,361 ·
Catholic Church 23,599 · Donation of Constantine 3,412. These are records with provenance, not list
entries — which is the whole distinction this ADR draws.

## Consequences

- **Good:** the filter self-repairs from work already being done. `/greenlight` measures topic demand
  before packaging anyway, so terms enter the recognizer as a byproduct — "berlin conference"
  (11,648/mo) and 68 other recorded keywords became anchors on the day this shipped, with no one
  curating anything. A false FAIL now costs one command instead of a code change, a test run and a
  commit. Every PASS carries a number and a source instead of an implicit "someone typed this once".
- **Cost:** the recognizer now depends on data as well as code, so its verdict can differ between two
  clones with different keyword stores. Mitigated three ways: the curated floor means the common
  cases never depend on data; a missing/locked/empty store degrades to the curated path instead of
  failing; and `tests/unit/test_search_anchor.py` pins the mechanism against tmp stores *and* pins
  the live store against the two documented regressions, so a stale store fails CI rather than a
  creator's greenlight.
- **Cost:** volumes go stale. The `source` tag carries the measurement date and lands in the lock
  block, so staleness is visible where the decision is read. No expiry is enforced — a term that was
  searched 100,000 times a month in 2026 does not stop being recognisable in 2027, and a hard expiry
  would reintroduce exactly the "gate blocks work for a bookkeeping reason" failure being fixed.
- **Not changed:** the gate's reasoning, its bindingness, `SEARCH_ANCHOR_BONUS` (+12), and every
  weight in the scorer. This is a recognition change only.
- **Reversible by** deleting the volume lookup and returning to list membership — which is the
  failure this ADR exists to prevent, and would need to explain the fourth append.

See: ADR 0012 (packaging advancement is code-gated), ADR 0007 (filters, not predictors), ADR 0009
(`title_features` owns structure — fame recognition deliberately does not live there),
`tools/title_scorer.py` (v6.2 changelog block), `tools/PACKAGING_MANDATE.md` §V2,
`.claude/rules/packaging.md` §1 (the shared ≥1,000/mo demand vocabulary).
