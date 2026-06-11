# PHASE-2-VOICE-LINT-SPEC — voice_lint.py new rules (Fable Phase 2, 2026-06-11)

Spec author: Fable 5 (inline, FABLE-PLAN Phase 2). Implementer: Sonnet agent.
Source analysis: `VOICE-PROFILE.md` §"Adversarial drift audit (Fable Phase 2, 2026-06-11)" + `D2-voice-triad.md`.

## Acceptance gate (the three-way test — MUST pass before commit)

1. **Gold fixture** (`tools/tests/voice-fixtures/gold-unscripted.md`) → **0 HARD, 0 WARN**
2. **AI-control fixture** (`tools/tests/voice-fixtures/ai-control.md`) → **≥ 5 HARD**
3. **#58 locked script** (`video-projects/_READY_TO_FILM/58-kurdistan-statelessness-2026/SCRIPT.md`) → **0 HARD** (new WARNs are expected and fine — they are the drift tells)

Fixtures: extract VERBATIM from `channel-data/fable-digests/D2-voice-triad.md` — SAMPLE A body (the full unscripted transcript paragraph) → gold fixture; SAMPLE C body (between its header and the ALIGNED EXCERPTS divider, the spoken text only, keep the `**Section Header**` lines — they're masked as structural) → ai-control fixture. Add a 3-line header comment in each fixture noting provenance.

Run: `python -m tools.voice_lint <file>` from repo root, all three; paste the three summary lines into the commit message.

## New HARD rules (C-only tells; verified zero-hit on gold and #58 during spec analysis)

Add to `HARD_REGEXES` (ignorecase=True unless noted). Predicted hits in parentheses.

| id | pattern | fix text | predicted |
|---|---|---|---|
| `agenda-announce` | `\bwe'?re going to (answer|explore|break down|dive into|look at)\b` | Agenda announcement — generic-AI opener. Start on the substance (bar-talk test #2); the question is shown by answering it. | C×1 |
| `changed-everything` | `\bchanged everything\b` | "X changed everything" — AI hinge cliché. Name what actually changed, concretely. | C×1 |
| `heres-the-thing` | `\bhere'?s the thing\b` | Meta-framing throat-clear. Delete; say the thing. | C×1 |
| `heres-why-standalone` | `\b[Aa]nd here'?s why\b|\bhere'?s why[.:]` | "Here's why" announcement — the zoom-out must be invisible (bar-talk #2). Walk into the cause with "because/so". | C×1 |
| `comment-bait` | `\blet me know in the comments\b` | Engagement-bait CTA — not his register. CTA = value-CTA ("go to the document"), earned by the prior beat. | C×1 |
| `love-your-thoughts` | `\bI'?d love to hear your thoughts\b` | Engagement-bait CTA. Cut. | C×1 |
| `tragedy-of` | `\bthe tragedy of\b` | Melodrama telegraph (family: dark-twist / darkest-chapter). State the event plainly, let it land. | C×1 |
| `isnt-just-its` | `\bisn'?t just [^.!?]{0,60}— it'?s\b` | "isn't just X — it's Y" escalation-correction tic (AI default). One claim, stated directly. | C×1 |
| `understand-go-back` | `\b[Tt]o understand [^.!?]{0,60}[, ]+(you|we) (have|need) to go back\b` | Obligatory-journey transition — verbatim-class AI tissue (matched the control word-for-word). Bridge by consequence instead: "So…" / thesis-forward. | C×1 (also fires on published #56 — expected, not gated) |
| `ghost-hangs` | `\b(ghost|shadow|weight) of [^.!?]{0,40}(hangs|hung|looms|loomed)\b` | Abstraction-as-agent poetry — purple prose, anti-voice. Cut or replace with a concrete fact. | C×1 |
| `population-compare` | `\bmore than the (entire )?population of\b` | Forced scale comparison (anti-voice family; closes a gap in the existing scale-* rules). State the plain figure. | C×1 |

Predicted control total: **11 HARD** (≥5 with margin). Existing rules contribute ~0 on C.

## New WARN rules (drift-frequency tells — advisory; WILL fire on #58, that is intended)

1. **`sinister-adverb`** — add to `WARN_ALWAYS` as regex (extend that table to support regex kind, or add a parallel `WARN_REGEXES` list): `\b(quietly|simply|conveniently|neatly|promptly) (erased|junked|vanished|disappeared|dropped|forgotten|ignored|buried)\b` → "Knowing-narrator wink. State the act plainly and name the agent." Predicted: B1×1 ("quietly erased"), C×1 ("simply erased"). Note: B1's `he simply "disappeared"` will also match — acceptable at WARN (it's quote-adjacent narration; human judges).
2. **`scholarly-hedge`** — `WARN_REGEXES`: `\b(essentially|arguably|in many ways|at its core|in essence|considerable autonomy|considerable independence)\b` → "Scholarly hedge = model fingerprint. His hedges are colloquial (basically/actually/kind of) — swap or delete." Predicted: C×2, gold 0 (gold's *basically* stays NOT_CRINGE), B1 0.
3. **`in-x-words`** — threshold counter (like `WARN_LITERALS`, max_allowed=2), regex `\bin (his|her|their|[A-Z][\w]*'?s?) words\b`: → "The 'in X's words' attribution formula ×3+ — the anonymous-attribution crutch (Standing dislike #2). Name the scholar once, let [SHOW] cards carry the rest, vary the frame." Predicted: B1 = 3 → fires; gold/C = 0.
4. **`negation-correction-density`** — new scanner `scan_negation_pairs`, ONE summary finding when count > 4 per file, listing line numbers. Count = matches of either form, over spoken sentences:
   - same-sentence dash form: `\b(wasn'?t|isn'?t|didn'?t|weren'?t)\b[^.!?—]{0,80}—\s*(it was|it'?s|they were|they built|he |she )`
   - cross-sentence form: sentence *i* ends matching `\b(wasn'?t|isn'?t|didn'?t|weren'?t|never)\b[^.!?]{0,80}[.!?]$` AND sentence *i+1* starts matching `^(It|They|He|She|This|That)\s+(was|were|is|are|built|created|stopped|did)\b`
   Fix text: "Negation-correction engine over budget (VOICE-PROFILE T1: A=0, scripts ≈9-15). Keep only EARNED pairs (live myth); state the rest directly." Predicted: B1 fires (~6), B2 fires (~10+), gold 0, C ~3 (borderline — don't tune to force a C hit; C is convicted by HARDs).
5. **`triad-density`** — threshold counter, max_allowed=3: `,\s+[^,.!?]{2,40},\s+and\s+[^,.!?]{2,50}[.!?]` → "Symmetric-triad garnish over budget (his enumeration is uneven/flowing; cap ~2 outside a declared ledger beat)." Predicted: C ≈ 5 → fires; B1 ≈ 2 safe; gold 0.
6. **`colon-reveal-density`** — threshold counter, max_allowed=3: colon mid-sentence followed by a short reveal ending the sentence, e.g. `[a-z][^.!?:"]{10,}: [A-Z][^.!?:]{0,40}[.!?]` — EXCLUDE matches where the colon is followed by a quote mark (quote hand-offs are sanctioned). Tuning latitude granted; if false positives on quote-intro lines can't be cleanly excluded, ship at max_allowed=4 or drop this rule (lowest-value of the set). Predicted: B1 borderline, C low.

## NOT mechanized (deliberately — judgment tells, lint can't see them)

Documented in VOICE-PROFILE T2/T3/T4: escalating aphorism pairs, balanced-clause epigrams, button-per-paragraph rhythm. These need semantic judgment → they live in the profile + script-writer-v2 Rule 13 #7 and are checked by the writing/review agents, not regex. Do NOT attempt clever regexes for them.

## Housekeeping

- Update the module docstring SOURCE-OF-TRUTH note: rules now also transcribe `VOICE-PROFILE.md` §"Adversarial drift audit (Fable Phase 2, 2026-06-11)".
- Keep exit-code semantics unchanged (HARD-only fail). WARNs never fail.
- Commit message: `feat(voice-lint): Fable Phase 2 — generic-AI tell rules + drift-frequency WARNs` + the three acceptance summary lines.
