---
description: Recurring voice-calibration drill — sharpen the canonical voice profile through live A/B line picks on real script beats. The repeatable loop, not the one-time map.
model: opus
---

# /voice grill — sharpen the voice profile, one beat at a time

**What this is.** A *recurring* calibration drill that sharpens the assistant's model of the creator's spoken voice (`VOICE-PROFILE.md`) by drilling **real beats from a live script** as concrete A/B picks, locking a prediction before each, and folding every pick back into the profile. It improves the script being drilled AND the profile at the same time.

**How it differs from its siblings (don't confuse them):**
- `/voice discover` — the **one-time bootstrap** that *created* `VOICE-PROFILE.md` from scratch (intensive interview, SRT mining, Phases 0–5). Run once. Done.
- `/voice tooling` — the **one-time autonomous** follow-up that built `tools/voice_lint.py` + exemplars. Done.
- `/voice grill` (this) — the **repeatable maintenance loop.** Run whenever there's a script with beats that feel even slightly off, or an open grill queue, or a profile rule you suspect is stale. Lightweight. No SRT re-mining, no tooling build.

**Origin:** #58 Kurdistan voice sessions (2026-06-05 → 2026-06-07). The grill method that worked got proven across ~5 sessions; session 4 (2026-06-07) distilled the method below and the calibration law. Replaces the ad-hoc `/grill-with-docs`-for-voice hack (that skill is built for code/ADRs — half its machinery is dead weight on voice; see the §"Why not grill-with-docs").

---

## Operating principles (read first, obey throughout)

1. **Concrete line options in CHAT — never the truncating box.** For line-level drilling, write **2–3 full-text line variants directly in the chat message.** Do NOT use `AskUserQuestion` for line drills — its preview box truncates and the creator has flagged this repeatedly. `AskUserQuestion` is allowed ONLY for a binary meta-decision (e.g. "continue or stop"), never for picking between rewrites. The creator [reasons from concrete examples, not rule-abstractions](memory) — show him lines, not options like "deliver flat vs lean in." See memory `feedback-grill-easier`.
2. **He picks + notes; YOU derive the rule.** His job is to pick the line that sounds like him and add a note. Your job is to extract the abstract rule from the pick and write it into the profile. Never ask him to articulate a principle.
3. **His LIVE picks are ground truth.** When a pick contradicts `VOICE-PROFILE.md`, the pick wins — rewrite the profile, don't argue. (The profile itself says this.)
4. **Lock your pick BEFORE he answers — and KEEP IT HIDDEN (ROT13). Present the options NEUTRALLY (correction 2026-06-08).** Do NOT state which option you recommend in plaintext — a visible rec anchors his choice and corrupts the calibration signal (the whole point is measuring his *independent* instinct). Encode BOTH your recommended option AND your one-line prediction of his pick in ROT13, locked before he answers; decode after he picks. Misses are the highest-value data — they expose where the profile (or your read of it) is wrong. This is what turns a drill into calibration.
5. **One beat at a time.** Surface it, drill it, resolve it, apply it, THEN the next. No batching beats.
6. **Run the 9-check Bar-talk Lock Test on every option BEFORE showing it** (it's at the top of `VOICE-PROFILE.md`). Options that fail #1 (say-it-out-loud/flowing), #2 (start on substance), or #3 (walk every leap) are what burn drill rounds. Fix them before they reach him.
7. **Update the profile INLINE as rules crystallize. Apply confirmed line fixes to the script live. DO NOT COMMIT.** Leave everything in the working tree for review.
8. **Voice only.** Don't redesign arguments or re-verify claims here. But preserve historian discipline: keep `[SOURCE]`/`[SHOW]`/`[NLM]` tags + verbatim quotes intact; if a rewrite needs a phrasing or quote, query NotebookLM — never fabricate.
9. **Terse.** One-sentence preamble per beat, no end-of-turn fluff. Match channel style.

---

## The calibration law (use it to form every prediction)

Discovered 2026-06-07, validated across the session — the single best predictor of his picks:

> **Completeness beats → he picks MORE.** When the choice is about *explaining a claim*, he takes the option that adds the *why / what-it-cost* on both halves. Under-explaining a strong beat wastes it.
>
> **Device & transition beats → he picks LEAN.** When the choice is about a *structural or rhetorical device* (a meta-frame, a signpost question, a first-person flourish, a verbal concede, an analogy over a literal fact), he cuts it and lets substance / the document carry it.

The standing failure mode is applying "more" to a device beat (over-framing) or "lean" to a completeness beat (clipping the why). Classify the beat FIRST, then predict. Corollaries proven in-session:
- **A "make it better / clearer" ask on a FRAMING beat still gets a LEAN answer (2026-06-07 #59, two misses in one session).** When he asks to *improve* a framing/device line (a neutrality declaration, a tee, a signpost), the fix is to re-word it — sharpen, concretize, plain-swap — NOT to add a clause. The "→ pick more" half of the law fires ONLY when the beat is *explaining a claim*. Twice this session I answered "improve the neutrality line" by ADDING (first cut-it, then bolt-the-method-onto-it); both lost to the lean concrete swap. If the substance an added clause would carry already lives in another beat, adding it here is just cross-beat redundancy. **Improve a framing beat by subtraction/precision, not addition.**
- **Owned procedural openers stay; evaluative meta-frames go.** "So let's get the facts straight" stays; "the popular story oversimplifies — and it's just wrong" goes.
- **Lead with the primary document, don't narrate a verbal concede.** The treaty on screen concedes the famous point for you.
- **Concrete callbacks that bookend = OK (flowing); abstract verdict re-listing = cut.**
- **Callback / thread-word seeds are the device-beat EXCEPTION to "lean" (2026-06-08 #59).** "Device → lean" is right for framing/signpost devices; a thread word planted to pay off in the close is a device whose *function is the echo*, so build the plant to structurally rhyme with the payoff (hang both on the same noun), don't strip it to the minimal placement. I predicted the leanest front-load ("On paper, the UN split the land…"); he picked the payoff-rhyming "A plan that, on paper, would split…" — a MISS toward lean on a callback device.
- **Anti-staccato is near-absolute** — the #1 "too-AI" tell. The fix for a chopped beat is almost always "connect into flowing sentences," not "trim further."
- **Classify a "bridge"/"turn" by FUNCTION, not surface position (2026-06-08 #59 corollary, hard-confirmed 2026-06-28 #36 — TWO misses, one session, same direction).** The "device → lean" half fires only on a frame that's PURE STRUCTURE (a bare signpost, a neutrality tee, "here's where it turns"). When the transition-frame itself CARRIES the load-bearing surprise — a controlling-idea seed ("wasn't the canal exactly — it was a document that let it act like the owner"), an over-delivery claim ("the strangest thing isn't… it's that he gave America more than America asked for") — it is a COMPLETENESS beat → predict the FULLER option. The standing miss is reading "it's a transition" off position and predicting lean; check whether the frame delivers substance first.

### Drift sensor — when to re-bootstrap instead of grill
The ROT13 predictions double as a rot detector. Log each beat's prediction hit/miss in the resume file. `/voice grill` only *sharpens*; when the profile stops modelling him, re-run the full `/voice discover` bootstrap instead (not more grilling). Triggers — any one:
- **Prediction hit-rate craters** across a session (≈<50% when register was never in question — the profile no longer predicts him).
- **New format / channel direction** the profile never covered.
- **Fresh corpus of finished cuts** worth re-mining (his delivered voice has moved on).
Otherwise grill is enough. No extra machinery — the calibration prediction-locking IS the sensor.

---

## The loop

### Step 0 — orient (read, in parallel)
1. `.claude/REFERENCE/VOICE-PROFILE.md` IN FULL — especially the ⭐ BAR-TALK LOCK TEST and the cringe no-list. This is canonical and the source of truth for every rule you write back.
2. The target `SCRIPT.md` + its `01-VERIFIED-RESEARCH.md` (pull real beats; preserve tags/quotes).
3. The project's `VOICE-DRILL-RESUME.md` if one exists (the open grill queue + prior-session record). If none exists and this is a multi-beat session, create one (see §Resume file).
4. Memory: `feedback-grill-easier`, `feedback-script-voice-calibration`.

**Lock-state check (gates whether script edits are allowed) — do this before drilling.** The script is LOCKED if the read-aloud T1 gate already passed, OR a teleprompter has been derived, OR a `FINAL-SCRIPT.md` / `.mp4` rough cut exists.
- **Unlocked (pre-read-aloud)** → normal mode: apply confirmed line fixes to `SCRIPT.md` live (voice work *is* part of getting to film-ready).
- **Locked** → **profile-only mode**: learn + stage/write the rule to the profile, but DO NOT edit the script. Record each proposed line change as a logged override in the resume file for the human to decide whether to unlock + re-derive the teleprompter. Never silently desync a locked script from its teleprompter ([[feedback-teleprompter-after-lock]]).

Then **run the linter** to free the drill for substance:
`python -m tools.voice_lint <path/to/SCRIPT.md>` — fix any HARD/WARN first; note that act-start REVIEW flags are usually false positives (bridges live in the prior act's tail).

### Step 1 — pick the next beat
From the resume queue, OR scan the script for beats that feel off. Prefer beats where you can **surface a contradiction**: the script violates a profile rule, OR two profile rules conflict, OR a "blessed" line lost on a recent live pick. Lead the beat by naming that contradiction in one line — it's the sharpest entry and the highest-value thing to resolve.

### Step 2 — drill it
- Write **2–3 full-text line variants** in chat, each a genuinely different *angle* (not synonyms): e.g. current/meta-frame · concede-first · document-forward · flat-continuity. Real beat, real tags.
- Each variant must already pass the 9-check.
- Lock your recommended option AND your **ROT13 prediction** of his pick (BOTH hidden — present the options neutrally, never a plaintext rec; it anchors him). Classify the beat via the calibration law first.

### Step 3 — resolve + record
- He picks + notes. **Decode your prediction; own the miss if you missed, and say what it teaches.**
- **Derive the rule** from the pick.
- **Apply** the confirmed line to the script — *unlocked mode only* (Step 0 lock check). In profile-only mode, log the change as an override in the resume file instead of editing. (Show nothing extra — the Edit is the diff.)
- **Apply the GENERALITY GATE before any profile write.** Classify the rule:
  - **Universal** (cadence, connectors, openings/closings, the calibration law, anti-staccato, concede-instinct) → write into the `VOICE-PROFILE.md` body, with the ✅ approved line and the ❌ rejected counter-example, dated.
  - **Topic/format-specific** (e.g. atrocity register, document-reveal handling, a territorial-only move) → do NOT pollute the body. Stage it in the profile's **"Pending / topic-specific (un-promoted)"** section (see §Single source of truth), tagged with the topic it came from. **Promote into the body only once the same rule recurs across ≥2 different topics.** One drill on one topic is a hypothesis, not a canonical law (mirrors [Channel Data Not Actionable] n-threshold + [Vibes-Test Framing]).
- **Update the resume file** queue item (resolved + the rule + the script line).
- Next beat.

### Step 4 — close
- Re-run the linter (confirm still clean).
- Update the resume file's status block (session N, what's resolved, the NEXT gate).
- Tight report: beats resolved, script edits applied (line list), profile sections touched, any new calibration finding, what's pending (usually the creator's **read-aloud T1 gate**). **Not committed.**

---

## Resume file (cross-session continuity)

Each drilled project keeps a `VOICE-DRILL-RESUME.md` in its folder: a top status block (date/session, what's resolved, NEXT gate) + an **OPEN GRILL QUEUE** of un-drilled beats/questions + a historical record of applied fixes. This is the pickup point for the next session — a fresh window reads `VOICE-PROFILE.md` IN FULL + this file, then continues the queue. Mark items `✅ RESOLVED <date>` with the rule + the script line; never delete the record.

---

## Single source of truth (anti-fragmentation)
`VOICE-PROFILE.md` is the ONE home for voice rules — full stop. Nothing else is a rule home:
- **Profile body** = promoted rules (universal, or topic-recurring across ≥2 topics).
- **Profile bottom section "Pending / topic-specific (un-promoted)"** = staged single-topic rules, each tagged with the topic(s) seen (`[kurdistan]`, `[flat-earth]`…). When a tag list hits 2 distinct topics, move the rule up into the body. Step 0 greps this section at session start to spot promotions.
- **`VOICE-DRILL-RESUME.md`** = per-project queue + applied-fix log ONLY — never a rule home.
- **memory `feedback-script-voice-calibration`** = pointer to the profile as canonical — never a duplicate ruleset.
- **Script footer notes** = a per-script record of what was applied — never the sole home of a rule.

Re-fragmentation across these surfaces is the exact failure `/voice discover` Phase 4 warned about; this rule prevents it.

## Hard rules
- **Full-text line options in chat for line drills. Never the truncating AskUserQuestion box.**
- **ROT13-lock a prediction before every pick.** Classify the beat (completeness vs device) with the calibration law first.
- **Live picks > the profile.** A pick that contradicts a rule rewrites the rule.
- **Update the profile inline; DO NOT COMMIT.** Apply line fixes to the script live ONLY in unlocked mode; on a locked script (read-aloud done / teleprompter exists) switch to **profile-only mode** — never silently desync a locked script ([[feedback-teleprompter-after-lock]]).
- **Voice only; preserve `[SOURCE]`/`[SHOW]`/`[NLM]` tags + verbatim; NotebookLM for phrasing, never fabricate** (historian discipline holds).
- **No new ADR unless a genuinely architecture-level voice decision emerges** (rare; the canonical home for voice rules is `VOICE-PROFILE.md`, not `CONTEXT.md`/ADRs). ADR 0006 already records "profile supersedes manual."

## Why not /grill-with-docs (the thing this replaces)
`/grill-with-docs` is built for code/domain modeling — its glossary-sharpening + contradiction-surfacing + update-docs-inline *spine* transfers to voice and is worth keeping. But its *modality* (dense open questions) fights the creator's working style, and ~half its machinery (ADR offers, code cross-referencing, CONTEXT.md glossary, second-grill-on-plan) is inert on voice. This command keeps the spine, swaps in the concrete-line-A/B modality, and drops the dead weight.

## Kickoff
`/voice grill` — then run Step 0. If invoked on a specific project, drill that script's resume queue; otherwise ask which script (one binary AskUserQuestion is fine here).
