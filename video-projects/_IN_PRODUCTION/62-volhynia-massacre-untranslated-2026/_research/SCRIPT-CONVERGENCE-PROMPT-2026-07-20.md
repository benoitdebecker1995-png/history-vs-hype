# Prompt for a fresh session — converge #62's script to final

Paste everything below into a new context window (Opus recommended — this is a convergence/polish pass on a script that's already been read aloud 5 times, not a first draft).

---

## Your task

Project: `video-projects/_IN_PRODUCTION/62-volhynia-massacre-untranslated-2026/`. The creator has read the current `SCRIPT.md` (v6.1) five times and wants ONE more restructuring pass to converge on a final, film-ready script — not a rewrite from scratch. Before writing anything, read the files below in full, then **restate your understanding of the creator's intent back to him in plain language and wait for confirmation** before producing the script. He's explicit that he wants this convergence step, not a blind rewrite.

## Read these files first, in this order

1. `CREATOR-INTENT.md` — the *why* underneath the thesis (the self-sabotage paradox, the double-move neutrality, the comprehension→mirror landing). This governs the cold open, the close, and tone throughout.
2. `02-STRUCTURE-SYNTHESIS.md` — the locked thesis (Rule 36, ≤12 words: *"Nations build heroes by remembering the resistance and burying the massacre."*), the slot map, the camp-tagging rule, the debunking overlay.
3. `SCRIPT.md` — the current v6.1 build. This is your base text, not a reference doc to ignore. Read the header notes (landmines, evergreen guard, show-don't-announce) — those are binding constraints, not suggestions.
4. `01-VERIFIED-RESEARCH.md` — the full verified fact ledger with ✅/⚠/❌ tags. Do not introduce any claim that isn't in here or in `SOURCE-GENEALOGY.md`.
5. `SOURCE-GENEALOGY.md` and `ON-SCREEN-SOURCES.md` — provenance for every on-screen card.
6. `_research/WHAT-WE-CAN-USE-HBC.md` — competitor differentiation (the Polish 2.3M HBC video takes the Polish-advocacy verdict; this video referees instead; primary documents on screen are the moat).
7. `.claude/REFERENCE/VOICE-PROFILE.md` — canonical voice rules, single source of truth (ADR-0006). Pay special attention to the 2026-07-20 additions: the open-question ledger (§Transitions), show-don't-announce, owning source weight aloud, the rhetorical-question-chain correction, the limitation-disclosure reframe (draft line staged, not locked), and the mid-paragraph pivot-fragment confirmation.
8. `channel-data/calibration/CALIBRATION-CORPUS.md` — read the `## #62` section (entries 62-01 through 62-10) in full. These are real live-pick findings from this exact project's five read-aloud sessions (`_adlib/t1-readthrough-2026-07-16.md` through `t5-readthrough-2026-07-17.md`, plus `followups-raw.md`) — treat them as validated, not hypotheses.
9. The `_adlib/` read-through files themselves (t1–t5 + followups-raw.md) — these contain the creator's own real spoken corrections across five full cold-reads. Where the corpus entries above summarize a rule, these files are the ground truth the rule was drawn from.

## The one structural change the creator wants

**Keep the cold open exactly as it is — word for word.** It was built and researched specifically for the click/watch decision (packaging-gated, not up for revision here).

**Restructure what comes after it.** Currently the script runs cold-open → chronological history (1918→1943, the massacre, the evidence adjudication, the movement burying its own past) → and only in the final act (CH8) does it explain why Ukraine honors these men *today* (the 2015 law, passed after the Crimea annexation) and the Poland/Ukraine dispute. The creator wants that reordered:

1. **Cold open** — unchanged.
2. **New early block, compressed:** what these men actually did — both the resistance/fighting-both-occupiers side AND the ethnic-cleansing side — stated plainly, both true at once. Then: why Ukraine honors them *now*, specifically anchored on the 2015 law passed after Russia's Crimea annexation (the "a nation at war needs its resistance symbols" mechanism from `CREATOR-INTENT.md`). This block's job is to make the cold-open paradox make sense early, not hold it as a twist for the end.
3. **Main body** — the deep evidentiary dive: the documents and evidence for and against these men (the missing-paper adjudication, Klyachkivsky's paper trail vs. the absent signature — NOT Lebed, see below), and why Poland and Ukraine are actually fighting over this (genocide vs. ethnic cleansing, the camp-tagging rule from `02-STRUCTURE-SYNTHESIS.md`).
4. **Close** — the mirror/universalizing beat (Washington/Napoleon/Leopold II) stays, per `CREATOR-INTENT.md`'s intended landing (comprehension → mirror). Confirm with the creator if any of this act's content needs to move earlier now that "why honored now" isn't the CH8 surprise anymore — some of CH8's dispute material may now belong in the new main body instead of staying backloaded.

**Do not reintroduce Lebed.** This was tested and settled this session: Klyachkivsky is the correct throughline (he's the one who signed everything else — tribunals, land reform, defense orders — under "Klym Savur," which is what makes "he signed everything else, but not this" a real, showable argument). Lebed's claim is testimony-only with no comparable paper trail, and he's already earmarked as `#63` follow-up material per `01-VERIFIED-RESEARCH.md` line ~245 (CIA-vs-MI6 angle). Introducing him here would violate the open-question ledger (62-01) — a new unexplained actor for a claim that isn't even the strongest one available.

## Constraints (non-negotiable)

- Runtime stays at the 12-minute hard cap (~2,600 words at the creator's delivery pace, per the `SCRIPT.md` header).
- The double-move neutrality holds: uneven-on-the-history (no false balance — it was organized, UPA-initiated, asymmetric) + firewall-on-the-present (the 1943 crime being real does not make "Ukraine is a Nazi state today" true).
- Show, don't announce: never narrate the act of displaying a document (VOICE-PROFILE.md §Cold-open). Weigh sources' evidentiary class in voice; let the screen do the pointing.
- Apply the open-question ledger (62-01) throughout: every beat should answer a question already raised and raise the next one. No claim gets re-answered once it's closed (say-it-once, 62-06). No new term/actor appears without being introduced first.
- Every on-screen card needs a genealogy-verified source per `SOURCE-GENEALOGY.md` — don't invent or loosen any citation.
- Run `python -m tools.voice_lint SCRIPT.md` before presenting the final draft and report the HARD/WARN count.

## Process

1. Read everything above.
2. Summarize back to the creator: the restructure you're about to do, in plain terms, and flag anything in the current CH8 material that you think needs to move into the new main body as a result of "why honored now" moving earlier. Wait for his go-ahead.
3. Write the converged script as a revision of the existing `SCRIPT.md` (preserve what's already working — CH1-CH7's actual content is mostly reusable, this is a reordering + a new connective block, not new research).
4. Run the linter, report results, and flag anything that still needs his read-aloud confirmation (per `.claude/REFERENCE/voice-modes/grill.md` — anything not yet read-aloud-tested stays flagged, not silently locked).
