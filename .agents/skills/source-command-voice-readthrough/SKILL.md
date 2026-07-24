---
name: "source-command-voice-readthrough"
description: "AI dry-run of the creator read-aloud on an UNLOCKED draft SCRIPT.md — read every beat in his voice, flag stumbles with concrete rewrites, and sharpen VOICE-PROFILE.md from what the read surfaces. Precedes the human T1 read-aloud; goal = zero feedback when he reads it."
---

# source-command-voice-readthrough

Use this skill when the user asks to run the migrated source command `voice-readthrough`.

## Command Template

# /voice-readthrough <project-slug>

The **dry-run of the read-aloud.** Before the creator reads a fresh draft top-to-bottom (the T1 gate in `/script`), this command has Codex *perform* that read in his voice — sentence by sentence — catching the lines that would make him stumble, and feeding anything new back into the canonical voice profile. It is the bridge between writing the draft and the human read: if this pass is honest, the human read should need **zero feedback** (v18 target, CALIBRATION-CORPUS GR-B).

This is NOT `/voice grill` (abstract recurring calibration on off-beats) and NOT the human T1 read. It is the **AI read-aloud** of one specific live draft.

## Shared invariants (inherited from `/voice` — obey all)
- **Canonical artifact = `.Codex/REFERENCE/VOICE-PROFILE.md`.** The ONE home for voice rules. New findings stage in its **"Pending / topic-specific (un-promoted)"** section and promote into the body only after recurring across **≥2 topics** (the generality gate). Never invent a global rule from a single script.
- **His LIVE picks are ground truth** — if he reworks a line during the pass, that pick rewrites the profile, even against an existing rule.
- **Concrete line options go in CHAT**, never the truncating `AskUserQuestion` box ([[feedback-grill-easier]]).
- **Update the profile inline; DO NOT COMMIT; voice only.** Preserve `[SHOW]`/`[SOURCE]`/`[NLM]` tags + verbatim quotes; use NotebookLM for phrasing, never fabricate a quote.
- **LOCK-STATE GATE (hard):** run only on an **UNLOCKED** `SCRIPT.md` (no `STATUS: LOCKED` marker, no `FINAL-SCRIPT.md`, read-aloud not yet passed, no teleprompter). On a locked script → **profile-only mode**: do the read for profile deltas, but make NO edits to `SCRIPT.md` ([[feedback-teleprompter-after-lock]]). The teleprompter is downstream and derived.

## Procedure

**0. Locate + gate.** Glob `video-projects/**/<slug>/SCRIPT.md`. Confirm unlocked (else profile-only). Read it in full.

**1. Load the fingerprint + mechanical pre-pass.**
- Read `.Codex/REFERENCE/VOICE-PROFILE.md` in full (the bar-talk lock test's 9 checks + the fingerprint rules + the cringe no-list are the rubric for this read).
- Run `python -m tools.voice_lint "<path to SCRIPT.md>"`. Fix every HARD and every WARN you agree with first (mechanical tics) so the human-judgment read isn't cluttered by lint-catchable noise.

**2. Perform the read — beat by beat, sentence by sentence.** For each sentence, actually *say it in one breath* (lock-test #1) and judge it against the 9 checks. Mark each line:
- **PASS** — sounds like him; flows; substance-first; plain; carries the why; concrete; honest.
- **STUMBLE** — flag the exact line, name which check/rule it fails (e.g. "#1 say-it-out-loud → chopped," "#3 walk-the-leap → asserts without crossing," "cringe: obscurity-claim," "transition: bare jump"), and give **one concrete rewrite in his voice** right there.
Watch especially for the standing failure spots: clunky transitions (#1 complaint), the synthesis/landing runway, staccato fragments + period-stab verdicts, over-citation, "clearer = tighter not more," carry-every-referent-for-the-ear, and the cringe no-list.

**3. Show the read-through table** in chat:
```
BEAT          LINE (excerpt)                          VERDICT   FIX
Hook          "…"                                      PASS      —
Act 1 ¶3      "…"                                      STUMBLE   "<rewrite>" (#3 walk-the-leap)
```
Then list the STUMBLE rewrites in full so he can pick/rework. **His rework of any line is ground truth → step 5.**

**4. Apply agreed fixes to SCRIPT.md** (unlocked only). After each rewritten beat, re-scan that beat (lint + a register re-read) before moving on. One full `voice_lint` run at the end; report the new HARD/WARN/REVIEW count.

**5. Sharpen the profile from what the read surfaced.** This is the half people skip. As you read, harvest:
- **Confirmations** — a rule the script obeyed well and he kept → note the live example (strengthens the rule).
- **Misses** — a line that passed lint + your judgment but he reworked anyway → that gap is a *new fingerprint signal*. Stage it.
- **New patterns** — a recurring move (good or bad) the profile doesn't name yet → stage it.
Write each to VOICE-PROFILE.md **"Pending / topic-specific (un-promoted)"** with: the rule (one line), an ✅ approved + ❌ rejected example, the date, and the origin (`<slug> read-through YYYY-MM-DD`). **Promote to the body only when it has fired on ≥2 topics.** If a finding *contradicts* an existing body rule and his live pick confirms it, edit the body rule (his pick wins) and log the reversal.

**6. Hand off.** Output: (a) the tightened SCRIPT.md is ready for the **human** T1 read-aloud; (b) the profile deltas you staged/promoted; (c) the final lint count. Remind: the human read-aloud is still the lock gate — this pass only aims to make it pass clean.

## Relationship to the rest of the loop
- **Upstream:** `/script` writes the draft + runs the heavy gate; this is the read-aloud dry-run inside that gate (step 7 of the canonical flow), before the human reads.
- **Sideways:** `/voice grill` handles abstract recurring calibration; `/voice-readthrough` is script-bound. Findings from both land in the same canonical profile under the same generality gate.
- **Downstream:** on the human "lock it," `/reconcile`-triggered post-lock delta-mine consolidates the session's picks into `CALIBRATION-CORPUS.md`; then `/script --teleprompter` renders the derived read.

## Origin
Created 2026-06-15 (during #36 Panama drafting) on creator request — "prompt to voice-read through it and sharpen the voice profile while doing so." Operationalizes the [[feedback-read-aloud-catches-logic]] insight (read-aloud catches substantive logic/voice that tools miss) as an AI pre-pass, and the [[feedback-calibration-loop]] (every read feeds the profile).
