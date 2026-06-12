---
description: Autonomous follow-up to /voice discover — build the voice linter, add few-shot exemplars, wire transition auditing, and reconcile the style manual. Runs without user input.
---

# /voice tooling — make the voice profile + scriptwriter better (autonomous)  *(mode of `/voice`)*

**Run this in a fresh context window.** It executes the no-user-input next steps from the 2026-06-05 `/voice discover` + `/grill-with-docs` sessions. The user is unavailable during this run — be autonomous, but **do not commit** (leave changes in the working tree for review) and **do not delete or destroy** existing content. End with a tight report of what changed and what still needs his judgment.

## Operating principles
- Terse, no preamble, no end-of-turn fluff. Match the channel's working style.
- Autonomous: don't ask questions you can answer by reading the repo. The user cannot respond this session.
- **Decisions already LOCKED — do NOT relitigate** (they are recorded; honor them):
  - `VOICE-PROFILE.md` is canonical and wins on conflict with `WRITING-VOICE-AND-STYLE.md`.
  - Voice-wins-unconditionally over niche-wide retention devices (authenticity is the product) — see `docs/adr/0006`.
  - Reference models = Kraut + Alex O'Connor; anti-voice = RealLifeLore.
- Token-efficient: offload any bulk reading to Gemini (`/gemini`); keep main context lean.

## Phase 0 — orient (read first, in parallel)
1. `.claude/REFERENCE/VOICE-PROFILE.md` — the canonical fingerprint (incl. the cringe no-list, the NOT-cringe list, the natural→scripted translation table, the transition rule).
2. `CONTEXT.md` § "Voice & delivery (channel-wide)" + the voice Relationships.
3. `docs/adr/0006-voice-profile-supersedes-style-manual.md` — why the profile supersedes the manual.
4. `C:\Users\Benoi\.claude\projects\D--History-vs-Hype\memory\feedback-script-voice-calibration.md` — origin trail + the ⚠️ reversed-notes flag.
5. `.claude/agents/script-writer-v2.md` — the 8-point VOICE PROFILE callout in AGENT MISSION (v16.5).
6. `WRITING-VOICE-AND-STYLE.md` §1.1, §1.3, §1.4, §2.3, §3.2 — the correction-callouts already inserted.
7. One existing tool in `tools/` (e.g. `tools/title_scorer.py`) — to copy CLI/argparse/reporting conventions for Task 1.

Do not proceed until you've read 1–3 and skimmed 5–6. The cringe lists and the locked decisions are the source of truth for everything below.

## Task 1 — Voice linter (`tools/voice_lint.py`) — highest ROI, deterministic
Build a Python CLI that scans a `SCRIPT.md` (or glob) and flags voice violations BEFORE the read-aloud gate, so the human read-aloud is freed for substance. Follow the conventions of the sibling tool you read in Phase 0 (argparse, `--help`, clear stdout report, non-zero exit if hard-cringe found).

**Detect (HARD cringe — pull the exact list from VOICE-PROFILE.md, don't hardcode from memory):**
- Literal strings (case-insensitive, word-boundary): "buckle up", "but guess what", "guess who", "guess what", "stay with me", "the receipt", "let's play their game", "keep both in your head", "there's a dark twist", "here's what almost no video".
- Regex patterns: `\b(one|two) words?:` (compressed reveal); `\berased the (Kurds|[A-Z]\w+)\b` (prefer "wrote them out"); present-tense decade scene-drop: `Go back to the \d{4}s` / `It'?s the \d{4}s\.` followed by present-tense verbs.
- Forced scale-comparison (script-side anti-voice): `the size of \w+`, `roughly the population of`, `more people than (lived|live) in`, `that'?s like looking back at`.
- Stacked credentials: 2+ of (`as .*historian`, `\bwrites\b`, `\bargues\b`, `according to`) within a 4-sentence window.
- Staccato triplet: 3+ consecutive sentences of ≤4 words each (fragments-for-emphasis run).

**Warn (dispreferred, not forbidden):** flag but lower severity — "here's where it gets interesting" if it appears >1×; "Think about that"; compression like a bare pronoun callback ("they wrote one"). Do NOT flag the NOT-cringe items as hard errors (see VOICE-PROFILE.md "NOT cringe" list — `basically`, `the system worked exactly as designed`, single "here's where it gets interesting", etc.).

**Transition check (folds in Task 3):** detect act/section headers (`^##`, `^---`) and check the FIRST sentence after each handoff for: (a) a thesis-forward / causal bridge vs a bare topic jump; (b) vague referents ("the very first one", "this"/"that"/"it" with no antecedent in the same line); (c) the common-story called flatly "wrong". Report each handoff with a PASS/REVIEW verdict — this is heuristic, so REVIEW (not FAIL) on ambiguity.

**Output:** grouped report — file, line number, matched text, rule, severity, and the profile's suggested fix. Summary counts at the end.

**Acceptance:** run it on `video-projects/_READY_TO_FILM/58-kurdistan-statelessness-2026/SCRIPT.md` (should be near-clean — the 11 voice wins are already applied) AND on an older cringe-heavy draft (e.g. an early `02-SCRIPT-DRAFT.md` or a pre-fix script) to confirm it catches real cases. Show both runs' summaries in your report. Add a one-line usage note to `memory/tools.md` (or the tools inventory the repo uses) and a pointer in `VOICE-PROFILE.md`.

## Task 2 — Few-shot worked exemplar (lifts first drafts)
Agents imitate examples better than they obey rules. Add a compact **"Worked exemplar"** block to `VOICE-PROFILE.md` (and a 1-line pointer from the `script-writer-v2` callout, point 8):
- The accepted from-scratch flat-Earth cold open (option A from the session — find it in the conversation log / regenerate from the profile if absent): the famous-then-puncture + concede-first + two-medium-sentence model.
- ONE before/after pair: a generic-explainer draft paragraph → its bar-talk rewrite, annotated with which rules fired (concede-first, tighten to two medium sentences, plain numbers, thesis-forward).
Keep it to ~25 lines. Real lines only; do not fabricate quotes or facts — use the #58 beats already in the script as raw material.

## Task 3 — Transition audit (his #1 standing weakness)
Two parts:
1. The linter's transition check (above) is the automated half.
2. Add a short prose step to the relevant command — read `.claude/commands/polish.md` and `.claude/commands/verify.md`, pick whichever already owns line-level voice passes, and add a "Transition audit" step: for every act/section handoff, confirm it is thesis-forward and hands into the next beat's subject (per VOICE-PROFILE.md "Transitions"). Keep it as a checklist item, not a new sub-agent. Show the diff in your report.

## Task 4 — Reconcile the manual body with the profile (prevent agent confusion)
`WRITING-VOICE-AND-STYLE.md` now carries correction-callouts, but the BODY of §1.4 (staccato/8-word-gavel emphasis) and §2.3 (scale-comparison) still teaches the opposite as primary — a fresh agent skimming the body gets mixed signals. Rewrite those BODY sections so they lead with the profile's position, demoting the old guidance to "rare device."
- **CRITICAL CONSTRAINT:** this manual serves BOTH script-writer and article-writer. The §2.3 scale-comparison guidance is **article-OK** (the override I added is script-side). Preserve article-side nuance — frame the demotions as "Script: … / Article: …" where they differ, per the file's own pointer rule. Do not delete the article-side value.
- Keep the callouts (they're the audit trail) but make the body no longer contradict them.
- This is the authoritative style file — edit surgically, preserve all article-side content, do not drop examples. If a section's rewrite is genuinely ambiguous between script/article, leave the callout and add a `TODO(voice): confirm with creator` rather than guessing.

## Task 5 (optional, if time) — Use-and-correct loop scaffold
Create a lightweight template `video-projects/_templates/VOICE-OVERRIDE-LOG.md` (or wherever per-project artifacts live — check the folder structure first): a tiny table for logging, per script, which voice rules the creator overrode during read-aloud (rule → what he changed it to → date). Add one line to the read-aloud step in the relevant command telling the user/agent to append overrides here, so the profile sharpens over time. Do NOT build automation around it — just the template + the hook.

## What this run must NOT do
- Do not record an unscripted-debunk exemplar (needs the creator to film — that's his task, #1 on the next-steps list).
- Do not commit or push. Do not delete VOICE-PROFILE.md content, the manual callouts, or ADR 0006.
- Do not relitigate the locked decisions in Phase 0.

## Final report (end of run)
A tight summary: files created/edited, the two linter runs' summary counts, anything you hit `TODO(voice)` on, and the ONE thing most worth the creator's attention when he's back (likely: review the manual-body rewrite in Task 4, and feed in a real unscripted-debunk recording for the profile's next sharpening).
