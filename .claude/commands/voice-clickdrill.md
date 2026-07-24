---
description: Click-based voice calibration — the grill loop with an AskUserQuestion click UI instead of chat A/B, so the creator just clicks options. Low-effort.
model: opus
---

# /voice-clickdrill — click-to-calibrate (low-effort grill)

The creator wants to **just click options, minimal typing**, and have his picks calibrate `VOICE-PROFILE.md` + improve the script. This is the `grill` loop (`.claude/REFERENCE/voice-modes/grill.md`) with an **AskUserQuestion click UI** swapped in for the chat A/B.

Arg = project slug. Default = the active `_IN_PRODUCTION` script that has an open `VOICE-DRILL-RESUME.md` (currently `36-panama-canal-deconcini-2026`).

## Setup (do silently, first)
1. Read IN FULL: `.claude/REFERENCE/VOICE-PROFILE.md`, `.claude/REFERENCE/voice-modes/grill.md`, the target `SCRIPT.md` + its `VOICE-DRILL-RESUME.md`. Skim memories `feedback-grill-easier`, `feedback-script-voice-calibration`.
2. **Lock-state:** unlocked (no teleprompter / `FINAL-SCRIPT.md` / `.mp4`) → apply confirmed line fixes to `SCRIPT.md` live. Locked → profile-only mode (log changes, don't edit the script).
3. Voice only. Preserve `[SHOW]`/`[SOURCE]`/`[NLM]` tags + verbatim quotes. Query NotebookLM for any phrasing/fact (the project's research notebook — #36 = `b3314135-7d32-475a-8c2b-5012450c7cc9`), never fabricate. **DO NOT COMMIT.**

## The loop (repeat in batches)
1. **Pick 3–4 beats** that feel even slightly off — the resume's OPEN QUEUE first, else scan the script for profile contradictions (a rule violated, two rules conflicting, a "blessed" line that lost recently).
2. **Per beat: 2–3 genuinely different FULL-TEXT variants** — different *angles*, not synonyms (e.g. flowing / lean / document-first / concede-first). Run the ⭐ BAR-TALK LOCK TEST on each BEFORE showing it (kill anything failing say-it-out-loud / start-on-substance / walk-every-leap).
3. **ROT13-lock your prediction** of his pick for EACH beat in the chat message, *before* asking (classify completeness-vs-device per the calibration law first). Keep it hidden; present the options neutrally — a visible rec corrupts the signal.
4. **Ask via `AskUserQuestion`** — ONE question per beat, **batched up to 4 per call** so he clicks through several at once:
   - `header`: ≤12-char tag (e.g. "Turn", "Close").
   - `label`: the angle in 1–5 words ("flowing", "lean", "document-first").
   - **`preview`: the FULL line text.** ← the whole point. NEVER put the variant only in the label — it truncates, which he has flagged repeatedly. The preview panel shows the full line untruncated.
   - single-select (previews require single-select). The auto "Other" lets him type a custom pick or note.
5. **On his clicks:** decode your ROT13 predictions, own any misses + say what they teach (misses are the highest-value data), derive the abstract rule from each pick.
6. **GENERALITY GATE:** universal rule (cadence, connectors, openings/closings, anti-staccato, the calibration law) → write into `VOICE-PROFILE.md` body with ✅ line + ❌ counter-example, dated. Topic/format-specific → stage in the profile's "Pending / topic-specific (un-promoted)" section, tagged with the topic; promote only after it recurs across ≥2 topics. Apply confirmed lines to `SCRIPT.md`.
7. **Update `VOICE-DRILL-RESUME.md`** (queue item resolved + rule + line; applied-fix log). Run `python -m tools.voice_lint <path/to/SCRIPT.md>` to stay 0-HARD. Next batch.

## Fallback
If a preview ever truncates, the UI misbehaves, or he says the box is bad → drop to **chat full-text options** for that batch (the standard grill modality). The click UI is a convenience, not a hard requirement.

## Style
Terse. One line of preamble per batch → the ROT13 block → the `AskUserQuestion` call. Let him click. Stop after ~4–5 batches or when he says stop. End each session with the tight grill close (beats resolved · script edits · profile sections touched · new calibration finding · NOT committed · next gate = his read-aloud).
