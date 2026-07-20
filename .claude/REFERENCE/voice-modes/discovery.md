---
description: Intensive interview to fully map the creator's spoken voice into one canonical profile
model: opus
---

# /voice discover — Map the creator's voice, once, properly  *(mode of `/voice`)*

**Why this exists.** Across many scripts, the assistant keeps *re-learning* the creator's voice per-session and keeps drifting into generic-explainer / essay-prose cringe ("keep both in your head at once," "this is the part the rest of the story hangs on"). The voice knowledge is scattered across five files and never gets consolidated or pressure-tested directly with the creator. This session fixes that: an intensive, structured interview that produces **one canonical voice profile**, validated by the creator's own choices, then propagated into the spec and the script agent so future drafts start in-voice.

**Run this in a FRESH context window.** It is context-heavy by design. Origin: #58 Kurdistan, 2026-06-05 — creator: *"after all these passes you still don't know my voice… have an intensive session where you ask everything possible to fully understand my voice… but don't bloat this chat — prepare a prompt to run in a fresh context."*

---

## Operating principles (read first, obey throughout)

1. **Picks, not prose.** The creator [struggles to write thoughts down](memory). NEVER ask "describe your voice" or "how do you like to sound." Ask by giving **3–4 concrete line options** and learning from which he picks. Use `AskUserQuestion` for almost everything. Open-ended questions only where a pick genuinely can't capture it (Phase 3), and keep those few.
2. **His LIVE picks are ground truth. SRTs are only a hypothesis.** Confirmed by the creator (2026-06-05): *"live picks are definitely better."* The finished-cut `.srt`s are heavily edited and may have drifted from how he'd say it cold — so they seed a *starting hypothesis*, nothing more. The moment a live pick or a typed edit contradicts the SRT-derived fingerprint, **the live pick wins and the fingerprint is wrong** — rewrite the hypothesis, don't argue with the human. Use SRT lines as one side of an A/B pair, but never present the SRT version as "the right answer"; let him choose blind.
3. **Stay lean.** Offload bulk SRT reading to Gemini (`/gemini`), per the creator's bulk-read preference. Pull back only the distilled fingerprint, not raw transcripts. Don't read 20 SRTs into main context.
4. **Learn live, write once.** Track every pick + reaction as you go. Synthesize into the canonical artifact only in Phase 4.
5. **Terse.** No preamble past one sentence, no emoji, no end-of-turn summaries. Match channel style.
6. **This is voice, not facts or structure.** Don't redesign arguments or re-verify claims. Stay on cadence, word choice, register, rhythm, connective tissue, openings/closings.

---

## Phase 0 — Load every voice asset + build a hypothesis (FIRST ACTION)

Read in parallel (one message), then dispatch Gemini:

1. `D:\History vs Hype\.claude\REFERENCE\WRITING-VOICE-AND-STYLE.md` index — routes to the comprehensive spec, PARTS 1-5 sibling files.
2. `C:\Users\Benoi\.claude\projects\D--History-vs-Hype\memory\feedback-script-voice-calibration.md` — picks-derived model + the #58 block (the "ask me / give me options" method and what his Kurdistan picks revealed).
3. `C:\Users\Benoi\.claude\projects\D--History-vs-Hype\memory\feedback-scriptcollab.md` — the "Voice-Pass Patterns" canonical cringe ruleset.
4. `C:\Users\Benoi\.claude\projects\D--History-vs-Hype\memory\feedback-staccato-delivery.md` — fragment + frequency-cap rule.
5. `C:\Users\Benoi\.claude\projects\D--History-vs-Hype\memory\feedback-read-aloud-catches-logic.md` — why read-aloud is the T1 gate.
6. `D:\History vs Hype\video-projects\_READY_TO_FILM\57-piri-reis-map-ottoman-2026\VOICE-FINGERPRINT.md` — the prior script-vs-SRT ad-lib fingerprint.
7. `D:\History vs Hype\video-projects\_READY_TO_FILM\58-kurdistan-statelessness-2026\SCRIPT.md` — live material; the v2 voice pass + the lines he picked are in here.

Then **dispatch Gemini** (`/gemini`) to digest 8–12 finished-cut delivered SRTs spanning formats (debunk, territorial, document-reveal, ideological). Good candidates:
`video-projects\_READY_TO_FILM\1-sykes-picot-2025\finshed video.srt`, `…\51-treaty-tripoli-article-11-2026\tripoli finshed cut srt.srt`, `…\50-thermopylae-sources-2026\finished edit.srt`, `…\44-bakassi-peninsula-2026\bakassi_youtube.srt`, `…\37-untranslated-vichy-statut-juifs-2026\statut definitive.srt`, `…\41-treaty-tordesillas-2026\tordesillas.srt`, `…\45-manhattan-purchase-myth-2026\finshed cut.srt`, `…\13-belize-icj-endgame-2025\belize guatemala icj.srt`, plus the plain `transcripts\*.srt` set.

Ask Gemini to return ONLY a distilled fingerprint: typical sentence length + variance; fragment frequency and what they're used for; his actual opener patterns; his actual transition/connector words; rhetorical-question frequency; how he introduces quotes/documents; how he closes; recurring verbal habits ("But guess what?", "And here's why that matters", "Take X", "Not 1916."); contraction/slang level; any line that's unmistakably him.

**Output of Phase 0 (internal, ~10 bullets):** a written *hypothesis* of his voice across the dimensions in Phase 2 — explicitly provisional. The SRTs are edited artifacts, not his live instinct; every bullet is a guess to be confirmed or killed by his picks in Phases 1–2. If the interview contradicts the fingerprint, the interview is right.

Do NOT start Phase 1 until the fingerprint is back.

---

## Phase 1 — Diagnostic warm-up: his line vs a rewrite (calibrate the core axis)

Goal: lock the blunt↔polished axis and confirm the fingerprint with his own words.

Build 6–8 A/B pairs. Each = one **actual delivered line** from a finished-cut SRT, set against a plausible **"polished/explainer" rewrite** of the same beat. Run as `AskUserQuestion` (label one "A", one "B"; randomize which is the real one; put the full lines in the descriptions/previews). Ask: *"Which sounds like you?"*

After the batch, reflect back the pattern you're seeing in one or two lines and have him confirm or correct. This is the only place you summarize early — because it sets the frame for Phase 2.

---

## Phase 2 — Systematic dimension sweep (the core of the session)

Walk every voice dimension below. For EACH, generate 3–4 **concrete line options** (pull beats from Kurdistan + his past videos so the options are real, not abstract) and run `AskUserQuestion`. Batch up to 4 dimensions per call. Record each pick AND any custom edit he types (his edits are the highest-signal data — he often rewrites the option toward his real voice).

Dimensions to cover (don't skip; reorder freely):

1. **Sentence rhythm** — jab-length fragments vs flowing sentences vs deliberate mix. (His SRTs skew short/choppy — test where the line is.)
2. **Cold-open / hook** — how he grabs in the first 5 seconds (paradox? blunt fact? "guess what"? document?).
3. **Transitions between beats** — THE biggest cringe source. Give options ranging from no-connective (just state the next thing) → "here's why that matters" → "guess who" → essay-bridge. Find his real connective tissue.
4. **The turn / reveal** — how he flips from myth to evidence ("But guess what? They're all wrong." vs softer).
5. **Document / quote hand-off** — how he sets up a quote or on-screen source ("Here's what it actually says" vs "Notice this phrase" vs blunt read).
6. **Mechanism explanation** — the second-person "when you X, you get Y" walk-through (he kept it on #58 — confirm and find its edges).
7. **Causal connectors** — "so" / "which is why" / "here's why that matters" / "and that meant" — which are his, which read as filler to him.
8. **Closings** — #58 he chose a verbatim source-quote close (McDowall). Test: does he prefer ending on a scholar/primary quote, a blunt one-liner, or a callback bookend?
9. **Humor / dryness** — how much, what kind (History-Matters dry understatement? none?).
10. **Emotional register / heat** — Calm Prosecutor coldness vs occasional spike; where he allows feeling.
11. **Direct address** — "you" vs "we"; tolerance for rhetorical questions (he dislikes pile-ups — find his cap).
12. **Casualness ceiling** — contractions (default), slang tolerance, where casual tips into cringe for him.
13. **CTA** — how a mid-video subscribe ask sounds in his mouth (still-open #58 item — get a real preference).
14. **Personal cringe no-list** — show 8–12 candidate lines (incl. ones he's killed before: "keep both in your head," "there's a dark twist," "the receipt," "let's play their game," "buckle up"). He marks which make him cringe. Expands the forbidden list with HIS reactions, in his words.

Where he types a custom edit instead of picking, treat that as the canonical answer and ask one tight follow-up to nail it.

---

## Phase 3 — A few open probes (only what picks can't capture)

Keep to 3–4, and make each answerable by pointing rather than essay-writing:
- "Name 2–3 creators whose *delivery* feels closest to yours — and one whose feels the opposite." (calibrates the reference set; current spec guesses Kraut/Alex O'Connor/History Matters/Wendover — verify.)
- "Point me at one past video of yours whose voice you're proudest of." (becomes the gold-standard exemplar.)
- "One word or phrase you catch yourself saying a lot that I should keep." 
- "Anything I keep doing that bugs you that we haven't named yet?"

---

## Phase 4 — Synthesize → write the canonical profile + propagate

1. **Write** `D:\History vs Hype\.claude\REFERENCE\VOICE-PROFILE.md` — the single distilled, picks-validated personal voice profile. Structure:
   - One-paragraph voice signature (what he sounds like, in plain terms).
   - The fingerprint (rhythm, openers, transitions, closings, connectors) — each rule paired with a **real example line HE approved** and a **counter-example he rejected**.
   - His personal cringe no-list, in his words.
   - The reference creators (confirmed in Phase 3).
   - Dimension-by-dimension do/don't.
   This file is the quick-reference companion to the comprehensive `WRITING-VOICE-AND-STYLE.md`; it is the *fingerprint*, that file is the *manual*.
2. **Update** `feedback-script-voice-calibration.md` — fold the consolidated model in; note `VOICE-PROFILE.md` as canonical; link `[[script-revision-grounding]]`.
3. **Propose** (don't silently apply) folding the top ~10 rules into `WRITING-VOICE-AND-STYLE-P1-CORE-VOICE.md` §1.1–1.3 and into the `script-writer-v2` agent system prompt, so future drafts START in-voice. Show the diff; get approval.
4. **Reconcile the scattered docs** — name the overlaps between WRITING-VOICE-AND-STYLE.md, VOICE-FINGERPRINT.md (#57), feedback-scriptcollab.md, feedback-staccato-delivery.md; recommend which stays canonical for what, so this doesn't re-fragment.

---

## Phase 5 — Validate on Kurdistan (and advance it)

Per the creator's instruction, use #58 as the live test:
1. Pick 4–6 lines in `58-kurdistan…\SCRIPT.md` that still feel even slightly off.
2. Predict, from the new profile, which rewrite he'll prefer — then offer options and check the profile's prediction against his pick.
3. Apply the wins to the Kurdistan script live (improves #58 at the same time).
4. If predictions match his picks consistently, the profile is validated. If not, fix the profile, not just the line.
5. Hand #58 back to its **read-aloud (T1) gate**. Update the #58 footer note. Kurdistan was ON HOLD for this session and now resumes there.

---

## Hard rules

- **AskUserQuestion is the default tool.** Picks over prose, always. His typed edits to an option outrank the option.
- **Real lines, not abstractions.** Every option is a concrete sentence, ideally from his own work.
- **Live picks > SRT fingerprint.** When a pick or typed edit conflicts with the SRT-derived hypothesis, the pick wins and the profile gets rewritten. The transcripts seed questions; they never overrule the human.
- **Gemini for bulk; main context stays lean.** Never dump raw SRTs into the session.
- **Write the artifact once (Phase 4), propagate with approval.** No silent edits to the spec or the agent.
- **Don't touch facts/structure.** Voice only.
- **Kurdistan stays on hold** until Phase 5.

## Kickoff line (paste into the fresh window)

`/voice discover` — then let Phase 0 run. (This is the `discover` mode of the `/voice` command; full playbook lives at `.claude/REFERENCE/voice-modes/discovery.md`.)
