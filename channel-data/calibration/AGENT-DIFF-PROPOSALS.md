# AGENT-DIFF-PROPOSALS.md — v18 candidate diffs from the calibration corpus

> **UPGRADE-PLAN S11, compiled 2026-06-12.** Learn-from-paper format: these are PROPOSALS, not applied edits — S12 walks them with the creator; only approved diffs land. Rejected proposals stay here marked REJECTED with the reason (that's calibration data too).
>
> **Tier discipline (S11 spec):** VALIDATED corpus entries → rule changes. HYPOTHESIS/IDEA entries → at most WARN-level checks or A/B notes, **never hard rules**. Every diff cites its corpus entries (`CALIBRATION-CORPUS.md` IDs; GR-* = grill-validated 2026-06-12).
>
> **Out of scope here:** voice-register changes (H1–H7 in `INTERVIEW-AGENDA.md` handoff) — those route through `/voice` grill → VOICE-PROFILE.md → then voice_lint, never directly. Lint proposals below are fingerprint-quantitative only.

**Approval walk order (S12):** D-block (script.md flow) first — it's the biggest workflow change; then A-block (writer), B-block (checker), C-block (lint).

---

# A. `.claude/agents/script-writer-v2.md` → v18.0

## P-A1 — New Tier 1 hard rule: LOAD-BEARING FACTS IN MAIN CLAUSES (promote or cut)
**Target:** Tier 1, new Rule 48 (after Rule 47).
**Proposed:** "A fact that must survive delivery gets its own main clause. If it can't earn a main clause within the runtime budget, it moves to the on-screen card or gets cut. It NEVER rides in an em-dash aside or relative clause. Example: ~~'He takes his royal fifth — 46 people for his personal estate — and the rest go to auction.'~~ → 'He takes his royal fifth. Forty-six people, for his personal estate. The rest go to auction.'"
**Cites:** GR-A7 (VALIDATED HARD), 56-24, CRAFT R2 (imported, but hard status comes from the grill pick, not the import).

## P-A2 — Amend Rule 36 (THESIS THROUGH-LINE): thesis spoken in full ONCE, at the close
**Target:** Rule 36 §"Thesis machinery — three structural slots" + Rule 23 (CLOSING MECHANICS).
**Proposed:** the full thesis line is reserved for the close; the whole video is architecture for it. Early slots carry the thesis IMPLICITLY (callback words, evidence ordering) — no early same-words plant, no paraphrase restatement anywhere. Any recap-shaped restatement is an anti-pattern (add to Rule 36 anti-patterns list).
**Cites:** GR-A2 (VALIDATED), 57-05, RP-6, RP-7. CRAFT R6 explicitly REJECTED.

## P-A3 — Amend Rule 17/Rule 12: method declaration compressed — no standalone method beat
**Target:** Rule 17 (HOOK FORMULA) tail + Rule 12 (FIRST EVIDENCE BY 0:90).
**Proposed:** the method declaration is either (a) one clause on the hook tail ("…and the way to settle it is to just read the sources. So let's read them.") or (b) deferred until the first source is on screen. A standalone pre-evidence method beat is an anti-pattern — the 0:45–1:40 zone gets evidence, not throat-clearing. (Supersedes the #56 method-bridge precedent — `feedback-script-structural-architecture` P6 needs a matching note at S12 apply time.)
**Cites:** GR-A3 (VALIDATED), 56-13 (refined), RP-8 (hypothesis context only).

## P-A4 — Amend Rule 23 (CLOSING MECHANICS): closers run chronological
**Target:** Rule 23.
**Proposed:** closer spine = strict chronology; dramatic irony comes from the timeline, never from structural intercutting. One flash-forward clause permitted ONLY when the outcome is already known/obvious to the viewer. Structural flashbacks in closers are an anti-pattern.
**Cites:** GR-A4 (VALIDATED), 57-27 (upgraded by grill).

## P-A5 — Amend Rules 44 + 32H (quote handling): paraphrase-default, verbatim earned
**Target:** Rule 44 (LONG-QUOTE SPLIT) + Rule 32H (Long Quote Handling).
**Proposed:** default for EVERY quote: VO speaks the paraphrase/interpretation in his voice; the card carries the exact words. A quote earns verbatim delivery only when it can land with zero gloss (self-sufficiency test) — and at most one spoken verbatim per beat. Guard sentence to add verbatim: "The video is an explanation that uses quotes, never a sum of quotes."
**Cites:** GR-A5 (VALIDATED), 56-11(b), 56-28, 57-25, RP-7.

## P-A6 — Amend Rule 38 (CONCEDE-AND-PIVOT): source-anchored micro-concessions
**Target:** Rule 38 + Rule 21B (Steelmanning).
**Proposed:** in ADDITION to the sectioned concede (architecture unchanged), every evidence beat whose on-screen source genuinely confirms part of the opposing claim concedes that part in the same breath ("And yes — that part's true.") then pivots to what else the source shows. Anchor condition: the concession must be visible in the source on screen — never a ritual "to be fair." Also the standard handling for confirmation-risk quotes.
**Cites:** GR-A6 (VALIDATED), 56-02, 56-17 (preserved), RC-01 (IDEA → adopted via grill pick, so rule-level is legitimate).

## P-A7 — Amend Rule 13 (ANTI-PATTERNS): the filler-beat catalogue + disclaimer gate
**Target:** Rule 13.
**Proposed additions:** (1) four beat types that get cut even when polished: real-vs-fake-research meta beats, moving-claim enumeration arcs, origin-of-the-claim history, corroboration stacking after the primary-source nail ("one nail per debunk"). (2) Disclaimers are trigger-gated: include ONLY when sensitive topic / stating own opinion / deliberately one-sided weighting / honesty requires it; otherwise the method line carries the fairness signal. Same gate for scholar-fallibility beats (trigger 4, when the correction record does argumentative work).
**Cites:** GR-A1 (VALIDATED), 57-06, 57-16, 57-30 (resolved).

## P-A8 — Amend Rule 41 (LANE CHOREOGRAPHY): enumeration–asset match
**Target:** Rule 41.
**Proposed:** any scripted enumeration of N items used as proof must specify a `[SHOW]` asset displaying those N items, labeled and followable. Build the asset to the list or trim the list to the asset BEFORE filming — an unmatched enumeration gets trimmed live to whatever the asset supports.
**Cites:** GR-A8 (VALIDATED — premise of 57-29c refuted and replaced by this rule).

## P-A9 — Amend Rules 19 + 32 (evidence selection): the thesis-bearing artifact
**Target:** Rule 19 (EVIDENCE SEQUENCING) + Rule 32 (VISUAL STAGING).
**Proposed:** evidence hunting recognizes a third class beyond quotes and numbers: an object or document-feature that proves the point by itself (Lausanne's zero instances of "Kurd"; the Piri Reis source-list label). When research supplies one (see P-D5), the beat may LEAD with the artifact, then one causal sentence. Use conditions (all three): explains the point / non-academic grasps it instantly / honest. Sub-rule: the changed-mind scholar credential ("X, who long argued the opposite, now writes…") — use when true, never manufactured.
**Cites:** GR-A9 (VALIDATED), RC-03/RC-04 (IDEA → adopted via grill), GS-08 context.

## P-A10 — Rule 32 A/B note: the engineered no-VO hold — TEST, not rule
**Target:** Rule 32C (Document Reveals) — note only.
**Proposed (A/B note, not a mandate):** one image-only hold (1–3s) per video, marked `[HOLD ON DOCUMENT — no VO, 2s]`, placed after the single strongest document reveal. Status: creator-approved TEST; judge at edit layer + retention before promoting. Tier-capped: stays an A/B note in v18.
**Cites:** GR-A10 (VALIDATED decision / unproven device), CRAFT R9 (IDEA — correctly capped at test).

## P-A11 — RP-7 delivery-survival note (WARN-level guidance, not a rule)
**Target:** Rule 7 (SPOKEN DELIVERY) — advisory paragraph.
**Proposed:** write the VO layer as if delivery will shed: mid-sentence asides (hard-covered by P-A1), recap lines, second verbatims in a beat, foreign-language reads, and any term not in the video's established terminology (pre-normalize quoted archaic spellings for the spoken layer; verbatim stays on the card). Advisory because the underlying SRT deltas are HYPOTHESIS-tier — except where a grill pick hardened them (P-A1, P-A5).
**Cites:** RP-7 (HYPOTHESIS — capped at advisory), 56-26, 57-26, 56-25.

---

# B. `.claude/agents/structure-checker-v2.md` — Wave 12

All new constraints get the standard CONSTRAINT output-block format. Severity per tier discipline: grill-validated → CRITICAL/WARNING as marked; hypothesis-sourced → WARNING max.

## P-B1 — CONSTRAINT T2: Load-bearing fact inside aside — CRITICAL
Flag any sentence where a date, number, name, or causal claim sits inside an em-dash aside or relative clause. Fix instruction: promote to main clause or move to card/cut. **Cites:** GR-A7 (VALIDATED HARD).

## P-B2 — CONSTRAINT U2: Standalone method beat before first evidence — WARNING
Flag a pre-first-evidence paragraph whose function is method declaration ("What I want to do in this video…") with no document on screen. Fix: compress to hook-tail clause or move post-first-source. **Cites:** GR-A3 (VALIDATED).

## P-B3 — CONSTRAINT V2: Early full-thesis statement / recap restatement — WARNING
Flag (a) a full-thesis declarative in the first half that matches the closing verdict's content, (b) any paraphrase recap of previously-stated material. **Cites:** GR-A2 (VALIDATED), 57-05.

## P-B4 — CONSTRAINT W2: Non-chronological closer — WARNING
In the final section, flag date sequences that run backwards (structural flashback). Pass if the only violation is a single flash-forward clause to a known outcome. **Cites:** GR-A4 (VALIDATED).

## P-B5 — CONSTRAINT X2: Spoken-verbatim budget — WARNING
Flag >1 verbatim quote written for VO in a single beat, and any VO blockquote >25 words lacking a self-sufficiency justification note. **Cites:** GR-A5 (VALIDATED).

## P-B6 — CONSTRAINT Y2: Enumeration–asset match — WARNING
Flag any scripted ≥3-item proof enumeration with no `[SHOW]` note specifying an asset that displays those items. **Cites:** GR-A8 (VALIDATED).

## P-B7 — CONSTRAINT Z2: Ungated disclaimer — WARNING
Flag disclaimer-shaped beats ("this isn't an attack on…", "I'm not saying…" openers) when none of the four triggers is declared in script metadata (sensitive / own-opinion / one-sided / honesty). **Cites:** GR-A1 (VALIDATED).

## P-B8 — Micro-concession presence check — INFO
On beats whose quote opens by appearing to confirm the opposing claim (confirmation-risk class), note whether a same-breath concession is present. INFO not WARNING: presence is contextual. **Cites:** GR-A6 (VALIDATED), 56-02.

---

# C. `tools/voice_lint.py` — new checks (thresholds from FINGERPRINT-UNSCRIPTED §9)

All fingerprint-derived thresholds are single-sample (741 words) start values → **everything below ships WARN or REVIEW, nothing HARD.** Source-of-truth note in the file header stays: these mechanize FINGERPRINT-UNSCRIPTED quantitative data; VOICE-PROFILE.md still supersedes.

## P-C1 — `really-intensifier` — WARN
Flag `really` used as intensifier (≥1 per script). Fix: his intensifier is "very" (very=9, really=0 in gold). Add `very` to NOT_CRINGE documentation list. **Cites:** GS-06 (VALIDATED fingerprint).

## P-C2 — `rhetorical-question` — REVIEW
Flag any sentence ending `?` in VO where the next sentence does not begin an answer (heuristic: next sentence starts with a connector/pronoun-answer). Setup-questions immediately answered = PASS. REVIEW-only: the chain-vs-zero tension is H3, pending /voice. **Cites:** GS-03 (VALIDATED), 57-28, RC-06c (IDEA — capped).

## P-C3 — `sentence-band` — WARN
Per-beat sentence-length median outside 10–22 words → WARN (protects flowing register from clipped-gavel AND run-on). Note in rule comment: broadcast prior is 15–20 (CRAFT R3, IDEA) — log both numbers, A/B the tighter band later, don't enforce it. **Cites:** GS-01 (VALIDATED), CRAFT R3 (IDEA — note only).

## P-C4 — `fragment-share` — WARN
1–5-word sentences >20% of script → WARN (gold baseline 13%, functional not dramatic). Complements the existing staccato-triplet HARD (which stays). **Cites:** GS-01 (VALIDATED).

## P-C5 — `writer-connector-density` — WARN
`which is why` + `and that meant` combined >2 per script → WARN (absent in unscripted speech; writer's tools to ration). **Cites:** GS-02 (VALIDATED).

## P-C6 — `youtuber-openers` — WARN
Sentence-initial `Now,` / `Look,` / `Listen` → WARN each (absent in gold; existing "here's" cap unchanged). **Cites:** GS-04 (VALIDATED).

## P-C7 — `verdict-hedge-presence` — INFO (optional, lowest priority)
If the closing verdict paragraph contains zero colloquial hedge (I think / I guess / kind of), emit INFO. Hedge family is constitutive (~1.5/100w). Optional: skip if noisy. **Cites:** GS-05 (VALIDATED).

---

# D. `.claude/commands/script.md` — revision-economy flow (the headline changes)

## P-D1 — NEW HARD GATE: STRUCTURE LOCK (beat-list gate) before any prose
**Target:** insert between "Research Verification Gate" and "Before Writing".
**Proposed:** before any sentence-level work, present a one-screen beat list — each beat = one line + its evidence — checked against the locked title ("what is the video we're trying to make"). User approves the spine; prose only after. No transition/cadence/polish passes on an unlocked structure.
**Cites:** GR-B2 (VALIDATED HARD GATE), 57-15, 57-03.

## P-D2 — Co-draft becomes the default write flow (replaces draft-then-revise)
**Target:** "Write the Script" §Workflow Steps + the writer's 3-checkpoint protocol (extend, don't discard).
**Proposed:** after the beat-list lock, the script is BUILT WITH the creator: at load-bearing/uncertain phrasing points (hook, verdict line, mechanism beats, key transitions), pause and show 2–3 prepared line variants in chat (Bar-talk pre-filtered; grill-easier format); assemble from picked lines. Cold full drafts are the anti-pattern (10x+ fix rounds; mid-revision rewrites shift the whole video's feel). Post-draft changes must stay small and localized. The writer's existing Checkpoints 1–3 become the minimum, not the total.
**Cites:** GR-B1 (VALIDATED), 57-07, 57-08, 58-05.

## P-D3 — Preparation bar before ANY creator input
**Target:** "Before Writing" + checkpoint instructions.
**Proposed:** before requesting any input (including beat-list and co-draft checkpoints): research fully digested (better too much than too little), topic genuinely understood, and a committed own idea of phrasing + video build. Checkpoints show prepared variants, never blank questions. ("Drive, don't punt" applied to the whole flow.)
**Cites:** GR-B3(a) (VALIDATED), 57-02.

## P-D4 — Pre-read-aloud HEAVY GATE (ordered, guaranteed)
**Target:** "After Generation" / pre-lock sequence.
**Proposed mandatory order before the script goes to the creator's top-to-bottom read-aloud:** (1) notebook grounding on all mechanism beats → (2) attribution audit → (3) seam flow-check (in/out at every paragraph) → (4) voice_lint → (5) corpus-scan → (6) Bar-talk test on solo-written lines. His read-aloud is T1 verification, never a draft filter. Plus per-round hygiene: every rewritten beat gets a scoped re-scan (lint + register) before its diff is shown; one full-script scan at the lock gate.
**Cites:** GR-B3(b) (VALIDATED), GR-B4 (VALIDATED), 56-05, 56-06, 57-10, 58-03.

## P-D5 — Quote bank completeness gate (research-side precondition)
**Target:** "Research Verification Gate" — extend; mirror note for `/research` Phase 2 (S12 decides whether to edit research.md too).
**Proposed:** scripting is blocked until 01-VERIFIED-RESEARCH contains the COMPLETE quote bank — all useful quotes round-trip-verified with page + provenance. The script writes from the bank only; any quote not in the bank mid-draft = STOP, route to research round-trip, never inline. Lock-gate backstop unchanged: load-bearing on-screen verbatims get one re-confirmation (verification notes go stale). Research directive added: hunt one thesis-bearing artifact per act (feeds P-A9).
**Cites:** GR-B5 (VALIDATED), GR-A9 (VALIDATED), 58-01, 58-02.

## P-D6 — Teleprompter export: professional render, selective pause markers
**Target:** "TELEPROMPTER EXPORT (`--teleprompter`)".
**Proposed:** render to professional teleprompter conventions; pause/beat markers added ONLY where a pause is load-bearing (the 2–3 seams per script where the pause IS the effect — pre-reveal, post-verdict). Never systematic marking. Lock-gate discipline (teleprompter-after-lock) unchanged.
**Cites:** GR-B6 (VALIDATED), 56-25 (hypothesis context).

---

# Deferred / rejected at compile time

- **CRAFT R6 (strategic redundancy)** — REJECTED by grill (GR-A2): thesis once, at the close.
- **CRAFT R1/R3 (OTPS / 15–20w band)** — not adopted as rules; R3's band logged as an A/B note inside P-C3 only.
- **CRAFT R12 (claptrap devices)** — placement question unresolved; register half routed to /voice (H5). No proposal.
- **Proof-list arity rule** — withdrawn; premise refuted (GR-A8 replaced it with enumeration–asset match).
- **H1–H7 voice tensions** (fragments-as-pivots, formal connectors, question chains, tier-aloud honesty, contrast pairs, limitation disclosure, OTPS sentence-shape) — awaiting `/voice` grill; nothing encoded.
- **N13 "Wikipedia tells me" transparency** — not proposed (channel academic positioning); only the honesty mechanic survives, inside /voice H4.

# S12 walk checklist

- [ ] D-block (flow) — P-D1..P-D6
- [ ] A-block (writer v18) — P-A1..P-A11
- [ ] B-block (checker Wave 12) — P-B1..P-B8
- [ ] C-block (lint) — P-C1..P-C7
- [ ] On apply: bump script-writer-v2 → v18.0, structure-checker-v2 → Wave 12, voice_lint rule list; update `memory/agent-versions.md`; record rejections back into CALIBRATION-CORPUS.md.
