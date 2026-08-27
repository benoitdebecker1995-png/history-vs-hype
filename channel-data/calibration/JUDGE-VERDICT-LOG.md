# JUDGE-VERDICT-LOG.md — persisted inline LLM-judge verdicts

> **LLM-CRAFT-UPGRADE-PLAN D3, 2026-07-19.** Two of this repo's LLM-as-judge calls — `/script` Step 3a (packaging coherence) and `/verify` Steps 7.5–7.9 (attribution/provenance/adversarial review) — previously ran ad hoc each session with output only in the chat transcript. This file is where they persist, so drift and (eventually) judge-to-creator agreement become measurable across videos instead of evaporating.
>
> **Append-only.** Newest entries at the bottom of each table. Do not edit past entries — if a verdict turns out to have been wrong, add a note in a new entry, don't rewrite history.
>
> **Filters-not-predictors (ADR-0007/0012):** every verdict logged here is informational. None of them gate lock, publish, or any other decision on their own — the existing gates (packaging coherence FAIL handling in `/script`, the 7.6/7.7/7.8 HARD blocks in `/verify`) already decide what blocks; this ledger just remembers what the judge said.

## Packaging coherence (`/script` Step 3a)

| Date | Command | Video slug | Scores | Overall |
|---|---|---|---|---|
| _(none yet — first entry lands the next time `/script` runs Step 4b)_ | | | | |
| 2026-08-10 | /script Step 3a | 62-volhynia-massacre-untranslated-2026 | promise=PASS verb=PASS specificity=PASS | OVERALL=MATCH |
| 2026-08-11 | /script Step 3a | 62-volhynia-massacre-untranslated-2026 | promise=PASS verb=PASS specificity=PASS | OVERALL=MATCH |

## Attribution / provenance / adversarial (`/verify` Steps 7.5–7.9)

| Date | Command | Video slug | Gemini raised / survived / NLM-confirmed | Gate tripped |
|---|---|---|---|---|
| _(none yet — first entry lands the next time `/verify` completes Steps 7.5-7.9)_ | | | | |
