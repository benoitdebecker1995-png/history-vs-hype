# EVAL-JUDGE-PROTOCOL.md — LLM-as-judge procedure + measured agreement

> **LLM-CRAFT-UPGRADE-PLAN E3, 2026-07-19.** Per Hamel Husain's alignment rule: a judge is only trustworthy once its agreement with a human's actual verdicts is measured, not assumed. This file states the judge procedure, records one real calibration run, and is honest about that run's limits.
>
> **Hard constraint (ADR-0007/0012, filters-not-predictors):** this judge's output informs revision. It never gates lock. Only the creator's read-aloud gates lock. A judge PASS is not permission to skip the human read-aloud; a judge FAIL is not a block — it's a flag for the writer to address before the human reads.

## The procedure

For each criterion in `EVAL-RUBRIC.md`:
1. Read the full script text.
2. Locate the specific line(s) that bear on the criterion.
3. Assign PASS / PARTIAL / FAIL / N-A, matching `EVAL-BASELINE.md`'s existing scale.
4. Cite the exact line(s) that earned the verdict — no verdict without a citation, same evidentiary discipline as `EVAL-BASELINE.md`'s R01–R24 table.
5. Where a criterion is ambiguous on the text alone (e.g. R19 spine judgment calls), state the reasoning, not just the verdict.

## Calibration run #1 (2026-07-19) — honesty note on blindness

**What this run is:** the E2 golden set (`EVAL-GOLDEN-SET.md`) found no fresh held-out script — every locked script is already mined into `CALIBRATION-CORPUS.md`, and the newest in-progress script (#62) isn't locked yet. So this run cannot be a genuine blind-agreement measurement against a human verdict nobody has seen yet. Two things were still possible, and both were done honestly rather than dressed up as more than they are:

**(A) Genuinely new scoring — R25–R28 (told-so-far criteria) against #58's locked script.** These criteria didn't exist before E1 today, so no prior verdict exists to be influenced by. Scored cold against `video-projects/_READY_TO_FILM/58-kurdistan-statelessness-2026/SCRIPT.md`:

| ID | Verdict | Citation |
|---|---|---|
| R25 | PASS | Every negation checked has its antecedent immediately preceding: L41 "a name on a map isn't a state" ← antecedent L39 (name/dynasty facts just given); L49 "never *the* Kurdish state" ← antecedent L47 (Kor paragraph); L65 "that's only half of it" ← antecedent same paragraph ("too divided" framing); L86 "Curzon being right didn't change a thing" ← antecedent L84 (Curzon quote, same beat). No forward-referencing rebuttal found. |
| R26 | PASS | L27 "that same town" ← antecedent "Tikrit" same sentence; L66 "the empire that ruled them collapsed" ← antecedent established across Act 2. No unresolved pronoun/callback found. |
| R27 | PASS | The "used, never given a state" thesis is stated in full once, at L109 (Act 4 opening synthesis), elaborated once more at L113 (closer) — this is the close developing its own point, not the same point landing in 3+ separate acts. (Notable overlap with the pre-existing R03 PARTIAL verdict — see below.) |
| R28 | PASS | No "EVEN the [record] accepts…" construction found; primary sources (Ibn al-Athir, Cambridge, McDowall) are led with throughout, not staged as concessions. |

This is real, first-ever scoring — a legitimate data point, not a reproduction of a known answer.

**(B) Process audit, not blind scoring — a 2-criterion spot-check on R01–R24.** Because this session had already read `EVAL-BASELINE.md`'s recorded LOCK column earlier in the conversation, re-scoring the full R01–R24 set and reporting "agreement" against that column would be circular — it would measure memory, not judgment. Instead, two criteria were re-derived from the script text alone, checking whether the citation actually supports the recorded verdict (an audit of rubric operationalizability, not a blind test):

- **R22** (CTA at ~70%, closer ends on a document beat): confirmed — L98 places the single CTA immediately after Act 3 (~70% of the ~2,605-word script), and the closer (L103–113) ends on the thematic synthesis line, not the CTA. Recorded PASS is well-supported.
- **R19** (structure matches title scope): confirmed — title claims "had states," and Act 1 ("THEY HAD STATES") through Act 4 all keep the emirates/statehood thread as the spine, including the Ubeydullah "first nucleus of a Kurdish state" quote (L66) that the plan's own EVAL-BASELINE interpretation notes REGEN cut and LOCK kept. Recorded PASS is well-supported.

**What this run does NOT establish:** an agreement percentage. That requires either a fresh session with no prior exposure to an answer key running the full blind pass, or real new data — the next video to lock. **Action, tracked as plan step L1:** when Panama (#36) locks, run this judge blind against the pre-lock draft (or the lock itself, per the original E3 prompt's fallback) before any corpus-mining happens, and compare against the creator's actual read-aloud catches for that video. That is the first true calibration number. Record it as Calibration run #2 in this file when it happens.

## Verdict ledger

Per plan step E5, every future harness run (triggered by a version bump to `script-writer-v2.md`, `structure-checker-v2.md`, or `VOICE-PROFILE.md`'s HARD rules) appends a dated entry here and to `EVAL-BASELINE.md`'s ledger.

- 2026-07-19 — Calibration run #1 (this file). R25–R28 scored fresh against #58 LOCK (all PASS). R22/R19 process-audited against #58 LOCK (both confirmed well-cited). No blind-agreement percentage yet — deferred to Panama's lock.
