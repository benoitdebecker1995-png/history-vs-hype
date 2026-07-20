# EVAL-RUBRIC.md — versioned, runnable script-eval criteria

> **LLM-CRAFT-UPGRADE-PLAN E1, 2026-07-19.** Extracted verbatim (not reworded) from `EVAL-BASELINE.md`'s R01–R24 table, which was itself derived from `CALIBRATION-CORPUS.md` VALIDATED entries. This file is the rubric of record for the Phase E eval harness (`EVAL-JUDGE-PROTOCOL.md`, `tests/unit/test_eval_harness.py`). When a new criterion is added here, add its corresponding row to `EVAL-BASELINE.md`'s ledger on the next eval run — this file and the ledger stay in sync by convention, not by code.
>
> **Verdict scale:** PASS / PARTIAL / FAIL / N-A, matching `EVAL-BASELINE.md`.

## Original criteria (R01–R24, from EVAL-BASELINE.md S13)

| ID | Axis | Criterion | Source |
|---|---|---|---|
| R01 | [St] | Claim-first cold open — the myth-puncture claim lands inside the open (~0:45), not scene-setting | RP-1, 56-11a |
| R02 | [St] | No standalone method beat; first document card appears ~0:20–0:90 | GR-A3 |
| R03 | [St] | Thesis stated once, at the close only — no earlier full pre-statement | GR-A2, 57-05 |
| R04 | [St] | Chronological closer — no structural flashback in Act 4 | GR-A4 |
| R05 | [V] | Quote economy: paraphrase-in-VO default, ≤1 spoken verbatim per beat, verbatim reserved for cards | GR-A5 |
| R06 | [St] | Quotes framed: setup sentence before, close-read sentence after | 56-02, 56-18, RP-4 |
| R07 | [Su] | Confirmation-risk quotes get a same-breath concession | GR-A6 |
| R08 | [Su] | No load-bearing fact placed in a dash-aside or relative clause — main clause or card only | GR-A7 |
| R09 | [St] | Every ≥3-item enumeration has a matching [SHOW] asset for each item | GR-A8 |
| R10 | [St] | Artifact-led beat — the strongest document/artifact leads its beat, not trails it | GR-A9 |
| R11 | [V] | Disclaimers are trigger-gated (sensitive / own-opinion / one-sided-weighting / honesty), not default | GR-A1 |
| R12 | [V] | No mirrored-binary close and no date-math cold open | 56-12, GS-05 |
| R13 | [V] | No stagey rhetorical-question transitions — every question is a setup-question answered next sentence | 56-16, GS-03, 57-28 |
| R14 | [Su] | Closing recap counts match exactly what was shown on screen | 56-14, RP-6 |
| R15 | [St] | Steelman is a full evidence beat with its own on-screen source card, not name-checked only | 56-17 |
| R16 | [V] | No editorial labels ("smoking gun," "gaslights"-class) — indictments are close-reads of the source's own words | 56-19 |
| R17 | [V] | Numbers spelled out as spoken in VO; calendar years in digits per convention | 56-21 |
| R18 | [Su] | Report the claim, don't sell it — opposing claims stated flat with literal verbs | 57-01 |
| R19 | [St] | Structure matches title scope — the spine element named in the title stays the spine of the script | 57-03, 57-15 |
| R20 | [St] | No filler-beat types (research-meta, claim-evolution arc, origin-of-claim history, science-stacking) | 57-06, 57-16 |
| R21 | [Su] | Genealogy steelman: concede the real kernel, isolate the leap that follows it | 57-18 |
| R22 | [St] | Single CTA at ~70% runtime; the closer itself ends on a document beat, not the CTA | 57-20 |
| R23 | [Su] | No Sykes-Picot beat/name-drop where the locked decision was to drop it entirely | 58-07 |
| R24 | [V] | `voice_lint.py` reports 0 HARD findings | 58-11, VOICE-PROFILE.md |

## New criteria — told-so-far ledger (from VOICE-PROFILE.md ~line 512, 2026-07-16 T1–T3 read-alouds)

Source: three full cold read-alouds on video #62 produced ~30 flags, almost all reducible to one failure class — the script rebutting or calling back to a claim that had not yet been stated on screen. Codified rule: *"a rebuttal is a referent too — its antecedent claim must exist on screen first."* Tier: **VALIDATED** (the creator's own read-aloud catches, not a hypothesis derived from SRT deltas).

| ID | Axis | Criterion | Source |
|---|---|---|---|
| R25 | [St] | Every rebuttal/negation ("wasn't," "isn't whole," "but that's only half of it," etc.) has its antecedent claim stated earlier in the same script — no forward-referencing rebuttal | VOICE-PROFILE.md ~line 512 |
| R26 | [St] | Every callback ("that same," "as we saw," "which massacre," pronoun-only references to an unnamed prior claim) resolves to a claim already on screen at that point, not one introduced later or never | VOICE-PROFILE.md ~line 512 |
| R27 | [St] | No single point is delivered 3+ times across different acts ("say it once" — cross-beat redundancy) | VOICE-PROFILE.md ~line 513 |
| R28 | [St] | No anti-concede-staging in the referee's own voice ("EVEN the [official record] accepts…") — official/primary records are led with as evidence, not extracted as concessions | VOICE-PROFILE.md ~line 514 |

## Change log

- 2026-07-19 — E1: file created, R01–R24 extracted verbatim from `EVAL-BASELINE.md`, R25–R28 added from the #62 told-so-far finding.
