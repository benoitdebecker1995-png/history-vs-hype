# EVAL-GOLDEN-SET.md — golden set for the Phase E eval harness

> **LLM-CRAFT-UPGRADE-PLAN E2, 2026-07-19.** Feeds `EVAL-RUBRIC.md` (E1) and `EVAL-JUDGE-PROTOCOL.md` (E3). Every path below was confirmed to exist on disk at write time.

## Positives — locked scripts, CALIBRATION-CORPUS-backed

Scripts the creator has actually locked (read-aloud passed), each with a corresponding section in `CALIBRATION-CORPUS.md` proving the rubric criteria were genuinely derived from these videos' deltas.

| Video | Script path | Corpus section |
|---|---|---|
| #56 No Lassos (Atlantic Slave Trade) | `video-projects/_ARCHIVED/published/56-no-lassos-atlantic-slave-trade-origin-2026/02-SCRIPT-DRAFT.md` | `CALIBRATION-CORPUS.md` ~line 24 |
| #57 Piri Reis Map | `video-projects/_ARCHIVED/published/57-piri-reis-map-ottoman-2026/SCRIPT.md` | `CALIBRATION-CORPUS.md` ~line 118 |
| #58 Kurdistan Statelessness | `video-projects/_READY_TO_FILM/58-kurdistan-statelessness-2026/SCRIPT.md` | `CALIBRATION-CORPUS.md` ~line 218 |
| #59 Israel/Palestine Partition Offer | `video-projects/_ARCHIVED/published/59-israel-palestine-partition-offer-2026/SCRIPT.md` | `CALIBRATION-CORPUS.md` ~line 257 |

Note: #58 sits in `_READY_TO_FILM/`, not `_ARCHIVED/published/` — script-locked but not yet uploaded. Included as a positive because lock (not publish) is what the rubric criteria certify.

**Known exception:** `#59`'s script literally ends on its CTA ("...subscribe." is the final sentence) — confirmed by reading the script, not a linter artifact. `voice_lint.py`'s `cta-ends-video` check (fixed 2026-07-19 alongside the R22 reconciliation) correctly flags this. Not treated as a golden-set defect because `EVAL-BASELINE.md`'s KPI ledger already documents `#59` as a hand-collaborative build, "NOT a clean writer-version KPI" — an independently-known outlier. See `tests/unit/test_eval_harness.py`'s `_KNOWN_EXCEPTIONS`.

## Negatives

| Sample | Path | Why negative |
|---|---|---|
| REGEN-58-v18 (blind regen) | `channel-data/calibration/REGEN-58-V18-DRAFT.md` | Scored FAIL/PARTIAL on R22/R24/R19/R23 in `EVAL-BASELINE.md` — a real, already-scored negative |
| Generic-AI control (Sonnet, zero style guidance) | `channel-data/fable-digests/D2-voice-triad.md` (sample C) | Fable Phase 2 adversarial drift audit's control sample; acceptance target is "AI control ≥5 HARD" on `voice_lint.py` — a known-bad baseline |

## Voice-gold reference (outranks derived rules on conflict)

Per the creator's explicit 2026-07-15 directive (`VOICE-PROFILE.md` ~line 499, "THE PIPELINE FLIP"): *"Treat the `_adlib/` transcripts as a HIGHER authority than this profile's derived rules when they conflict."* Used by the E3 judge as ground truth for voice register, not scored pass/fail against the structural rubric (R01–R24 are structure/substance criteria derived from LOCKED scripts; the adlib transcripts are pre-script raw material, not a script).

`video-projects/_IN_PRODUCTION/62-volhynia-massacre-untranslated-2026/_adlib/` — 14 files: `act1-raw.md` … `act5-raw.md`, `act2b-sanitization-raw.md`, `act3a-retell-raw.md`, `followups-raw.md`, `t1`–`t5-readthrough-2026-07-1{6,7}.md`.

## Held-out script — BLOCKED, no candidate exists yet

**Finding:** the in-sample caveat cannot be fixed today. Checked every #-numbered video against its lifecycle stage and corpus status:

- #56, #57, #59 — published, corpus-mined (positives above).
- #58 — locked, corpus-mined (positive above).
- #60 Guadalupe Hidalgo, #61 Spanish Colonization, #62 Volhynia — all sit in `_IN_PRODUCTION/`, meaning per `CLAUDE.md`'s lifecycle definition none has a locked script yet (`_READY_TO_FILM` is the lock signal; none of the three has moved there). #62 has extensive read-aloud data (T1–T6, 2026-07-16→18) but is still iterating (v5.3 as of the T4 read) — not locked.

**Conclusion:** there is currently no locked-but-unmined script to hold out. Every locked script the corpus could test against was used to build the corpus. **Action for a future session:** the moment the next video locks — Panama #36 is next per project state (`video-projects/_IN_PRODUCTION/36-panama-canal-deconcini-2026/`) — mark it held-out *before* mining its deltas into `CALIBRATION-CORPUS.md`, run the E3 judge against it first, and only mine it afterward. This is also the plan's own pre-registered test: `EVAL-BASELINE.md`'s KPI ledger already reserves Panama as "first clean v18 test."

## Change log

- 2026-07-19 — E2: golden set defined; held-out slot flagged BLOCKED pending Panama's lock (tracked in `EVAL-BASELINE.md` KPI ledger, plan step L1).
