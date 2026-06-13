# EVAL-BASELINE.md — v18 in-sample regression baseline (S13)

> **UPGRADE-PLAN S13, 2026-06-12.** Method: script-writer-v2 **v18.0** blind-regenerated a #58 draft from `01-VERIFIED-RESEARCH.md` only (forbidden: the locked SCRIPT.md and all #58 session artifacts; checkpoints self-resolved). The regen (`REGEN-58-V18-DRAFT.md`, ~2,650 words) is scored against the human-locked `SCRIPT.md` on a rubric derived from CALIBRATION-CORPUS VALIDATED entries (one checkable criterion each; process-only entries like GR-B1..B7 are not text-checkable and are excluded).
>
> ⚠️ **IN-SAMPLE CAVEAT (read first): v18 was trained on #58's deltas; a pass means "lessons encoded," NOT "generalizes." The real test = Panama passes-to-lock + the pre-registered H2 gate (first-28-day CTR ≥4%).**

## Scores

| # | Criterion (short) | Source | REGEN | LOCK | Notes |
|---|---|---|---|---|---|
| R01 | Claim-first cold open | RP-1, 56-11a | PASS | PASS | Both open on the Saladin puncture-claim ("he wasn't an Arab… he was a Kurd"), not scene-setting; target myth lands inside the open (~0:45). |
| R02 | No standalone method beat; first doc ~0:90 | GR-A3 | PASS | PASS | Ibn al-Athir card on screen ~0:20 in both; REGEN defers method to CTA tail, LOCK's "you don't have to take my word for it" is a hook-tail clause. |
| R03 | Thesis once, at close only | GR-A2, 57-05 | PARTIAL | PARTIAL | Both pre-state the thesis mechanism in the Act-4 cat's-paw synthesis ("nobody around them ever wanted them to have one" — REGEN L334 / LOCK L109) before the close; LOCK's cold open also near-states it agentlessly. |
| R04 | Chronological closer | GR-A4 | PASS | PASS | REGEN Act 4 runs 1946→1975→1988→2026→close; LOCK runs 1988→today→2026→close; no structural flashback in either. |
| R05 | Quote economy: paraphrase default, ≤1 spoken verbatim/beat | GR-A5 | PASS | PARTIAL | REGEN paraphrases İnönü/Fraser with verbatim on cards, ~1 spoken quote/beat throughout; LOCK stacks 3 spoken verbatims in the Curzon/İnönü beat + 4 in the Mosul beat, and "separated from the pen…" needs its gloss to land. |
| R06 | Quotes framed: setup before, close-read after | 56-02, 56-18, RP-4 | PASS | PASS | REGEN: "Read what the committee actually concluded" → Pike quote → "In other words…"; LOCK: recognition stakes set before Curzon/İnönü, closed with "Curzon being right didn't change a thing." |
| R07 | Confirmation-risk quotes get same-breath concession | GR-A6 | PASS | PASS | Both handle Nezan's "main barrier": REGEN "the feuds were real… but the empires didn't just find that division, they fed it" (L176); LOCK "the feuds they're pointing to were real. But that's only half of it" (L65). |
| R08 | No load-bearing fact in dash-aside/relative clause | GR-A7 | PASS | PASS | Numbers/dates ride main clauses in both (R48 visible in REGEN); REGEN's 10%-royalties fact sits after an em-dash but in emphatic sentence-final position (L268), not a buried aside. |
| R09 | ≥3-item enumerations have matching [SHOW] | GR-A8 | PARTIAL | PARTIAL | REGEN's Kor sovereignty trio (cannons/coins/khutba, L101) and 5-emirate list (L121) lack item-displaying assets; LOCK's Kor enum shows only the coin (L47) and the Act-4 ledger card shows the cat's-paw quote, not the three items. |
| R10 | Artifact-led beat | GR-A9 | PASS | PASS | Lausanne zero-"Kurd" count leads its beat in both (REGEN L278 at ~78%, LOCK L96); REGEN adds the Bedirxan coin legend as a second artifact lead. |
| R11 | Disclaimers trigger-gated | GR-A1 | PASS | PASS | REGEN's sole "I want to be careful here" (L121) gates the C33 one-sided-weighting/honesty concession; LOCK carries no viewer-directed disclaimer at all. |
| R12 | No mirrored-binary close / date-math opener | 56-12, GS-05 | PASS | PASS | Both close on the McDowall imagination/ground line resolved into the thesis, not an aphorism; both open on "Everyone knows Saladin," no date-math. |
| R13 | No stagey rhetorical-question transitions | 56-16, GS-03, 57-28 | PASS | PASS | All questions are setup-questions answered in the next sentence ("So if 1639 didn't do it, what did? The answer is…" REGEN L155; "So why did Britain let it happen…? It came down to one province" LOCK L90). |
| R14 | Closing recap counts match what was shown | 56-14, RP-6 | PASS | PASS | REGEN's "real states, real coins, real laws" maps to Soran/Bohtan/Bitlis, Kor+Bedirxan coins, purse-of-gold/hükûmet; LOCK's "hero, kingdoms, coins" all appeared, coin re-shown at close. |
| R15 | Steelman is a full evidence beat with on-screen sources | 56-17 | PARTIAL | PASS | REGEN's "too divided" steelman quotes Nezan and Klein but specifies no [SHOW] card for either (L173–176 GUIDE block) — name-checked, not screened; LOCK puts the Nezan "main barrier" card on screen plus the cousin-defection evidence (L65). |
| R16 | No editorial labels | 56-19 | PASS | PASS | Neither speaks "smoking gun"/"gaslights"-class labels; indictments are close-reads ("That's a choice, written down" REGEN L280; LOCK's "quietly junked" is McDowall's own quoted phrase). |
| R17 | Numbers as spoken in VO | 56-21 | PASS | PASS | Quantities spelled in both ("three hundred thousand and eight hundred thousand" REGEN L199; "twelve thousand cavalry" LOCK L45); calendar years in digits per convention. |
| R18 | Report the claim, don't sell it | 57-01 | PASS | PASS | Opposing claims stated flat with literal verbs in both ("you'll often hear that the Kurds were first split apart in 1639… the treaty drew no line" REGEN L144–152; "You've probably heard some version of the answer" LOCK L31). |
| R19 | Structure matches title scope (states are the spine) | 57-03, 57-15 | PARTIAL | PASS | REGEN cut the on-spine Ubeydullah 1880 statehood bridge (self-flagged, L470) while keeping the off-spine Mahabad+Pike grievance beats; LOCK made the opposite trade — kept Ubeydullah's "first nucleus of a Kurdish state," cut Pike. |
| R20 | No filler-beat types | 57-06, 57-16 | PASS | PASS | Neither has research-meta, claim-evolution arc, origin-of-claim history, or science-stacking; both bust 1639 with the treaty text and stop at one nail. |
| R21 | Genealogy steelman (concede kernel, isolate leap) | 57-18 | PASS | PASS | Both concede the division kernel and isolate the leap (REGEN: division real but engineered, L175–176; LOCK: "feuds were real… that's only half of it" + Sèvres "you could call it a betrayal — but really," L78). |
| R22 | CTA at ~70%, single, closer ends on document beat | 57-20 | FAIL | PASS | REGEN places its only CTA at ~100% (L360) so the video ENDS on the CTA, not a document beat; LOCK's CTA sits at end of Act 3 (~70%, L99, explicitly value-anchored) and the closer ends on the McDowall line + the coin re-shown. |
| R23 | No Sykes-Picot beat | 58-07 | PARTIAL | PASS | REGEN has no Sykes-Picot-centered beat but one name-drop survives ("three centuries before Sykes-Picot ever drew a line," L144) against the lock's drop-entirely decision; LOCK spoken text has zero mentions. |
| R24 | voice_lint 0 HARD | 58-11, VOICE-PROFILE | FAIL | PASS | Supplied: REGEN 5 HARD / 17 WARN / 10 REVIEW (heres-the-thing ×2, "one word:" ×2, erased-the-Kurds ×1); LOCK 0 HARD / 10 WARN / 6 REVIEW under v18 rules. |

**Totals:** REGEN 17 PASS / 5 PARTIAL / 2 FAIL / 0 N-A · LOCK 21 PASS / 3 PARTIAL / 0 FAIL / 0 N-A

## Interpretation

The regen encoded the structural lessons convincingly. Strongest three: (1) R05 quote economy — paraphrase-in-VO with verbatim on cards and ~one spoken quote per beat is actually CLEANER than the lock, which still stacks three spoken verbatims in the Curzon/İnönü beat and four in the Mosul beat; (2) R10/R02 document discipline — first source on screen at ~0:20, no standalone method beat, and the Lausanne zero-"Kurd" count leads its beat at the prescribed ~78% slot; (3) R04/R13/R20 architecture — chronological closer, setup-questions only, and a complete absence of the four filler-beat types, which were the expensive lessons of #56–57. Where it failed: (1) R22 — it parked the single CTA at 100% and ended the video on it, inverting the 57-20 rule it could recite (its own comment says "earned by the document beat"); (2) R24 — 5 lint HARDs, all retired surface tics ("here's the thing" ×2, "one word:" colon-reveal ×2, "erased the Kurds"), which says the prose layer drifts back to generic-AI register even when the structure layer is fully encoded — rules-as-outline transferred, rules-as-diction did not; (3) R19/R23 editorial judgment — it cut the on-spine Ubeydullah statehood bridge while keeping the off-spine Pike beat and let one Sykes-Picot name-drop survive, the exact spine-protection calls the creator made at lock and which aren't derivable from the research file alone. The heavy gate (GR-B3b) would have caught the 5 HARDs, the colon-reveals, and the CTA misplacement mechanically before the creator ever read a line — meaning the residual human cost in this regen is concentrated in the judgment layer (spine trades, lane bans), not the rule layer.

## Passes-to-lock KPI ledger

| Video | Writer version | Passes to lock | Notes |
|---|---|---|---|
| #58 Kurdistan | v17 | ≈2–3 full passes (+ ~6 line-level drill sessions) | baseline (58-10); read-aloud T1 2026-06-10 |
| #36 Panama | v18 | TBD | first clean v18 test; H2 gate: first-28-day CTR ≥4% |

*(S14 standing loop appends each future video's passes-to-lock here at lock declaration.)*
