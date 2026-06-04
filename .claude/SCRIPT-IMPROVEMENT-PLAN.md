# Script-Writer-v2 Improvement Plan — Cut User Correction Work

> **How to execute:** Say *"execute the script improvement plan"* (this file: `.claude/SCRIPT-IMPROVEMENT-PLAN.md`). All changes land in `.claude/agents/script-writer-v2.md` unless noted. Implement Changes 1–4 in order; each is independently shippable.

---

## Context

**Goal:** The user spends heavy time rewriting AI scripts to fix three things — (1) logical sense, (2) easy-to-follow, (3) hallucination. The aim is scripts that arrive *more professional* so the user does *less correction work*. **Final authority stays with the user** — AI reduces the janitorial burden but never overrides the user's judgment on argument/logic.

---

## Diagnosis (evidence-led)

**The rules already exist** — Rule 2/5/42 (anti-hallucination), Rule 3/36 (logic), Rule 4/8 (clarity). They don't *fire reliably*. Three confirmed reasons:

1. **Hallucination defense is a single buried checkbox.** The entire "facts traceable to research" guard is one line (`script-writer-v2.md:1561`) inside a 50-item self-assertion checklist at the bottom of a 1,737-line file. No mechanism forces claim-by-claim tracing — the model rubber-stamps it.
2. **Verification is manual, downstream, hand-off.** `/verify`, `fact-checker`, `structure-checker-v2` are all robust HARD GATES but must be invoked by hand *after* the draft lands. The user is the integration glue — running them, reading findings, applying every fix. That *is* the "lots of correction work."
3. **AI cannot catch deep logic post-hoc.** Per the user's own verified memory `read-aloud-catches-logic` (#56, 2026-05-25): even Opus reading its own draft aloud missed **all 6** substantive issues the user caught (a quote confirming the opposite claim, a steelman on the wrong sub-claim, an 80-year unaddressed gap). AI tools caught only surface vocabulary tics.

**Conclusion — split the three pains into two classes:**
- **Hallucination = mechanizable.** Claim → research-line traceability is pattern-matching, not comprehension. Safe to automate (AI auto-cuts).
- **Logic + follow-ability = NOT mechanizable post-hoc.** Only leverage is *up-front prevention* + *protecting the read-aloud*. AI flags candidate spots, never rewrites.

---

## Strategy: Split by Defect Class (user-confirmed)

| Defect class | Who fixes | Where the leverage is |
|---|---|---|
| Hallucination / unsourced claim | **AI auto-cuts + flags** | New Claims Ledger hard gate before delivery |
| Logic / framing / scope | **AI flags only → user fixes** | Up-front prevention + Read-Aloud Flag List; read-aloud stays mandatory gate |
| Surface vocab tics | existing tools (Tier 2) | unchanged |

---

## The Changes (all in `script-writer-v2.md` unless noted)

### Change 1 — Claims Ledger + hard traceability gate (HALLUCINATION)
Replace the single buried checkbox (`:1561`) with a **structured pre-delivery pass**:
- Enumerate every factual sentence in the draft (dates, names, numbers, "which meant that…" causal bridges, attributions).
- Tag each with its source: `research file + line/section`, or `[NO SOURCE]`.
- **Auto-action:** every `[NO SOURCE]` claim is either cut or rewritten to the nearest sourced statement, OR demoted to an explicit `[NEEDS VERIFICATION]` flag if load-bearing. No silent shipping of unsourced claims.
- **Output the ledger as a visible appendix** (`## CLAIMS LEDGER`) so the user can audit every auto-cut and override — *authority stays with the user*.
- This makes Rule 2/5/42 a *mechanism*, not a self-asserted checkbox.

### Change 2 — Up-front prevention (LOGIC + FOLLOW-ABILITY)
Strengthen the existing **Checkpoint 2 (Outline)** — catch structure defects before 3,000 words exist:
- **Timeline-completeness check:** no unexplained gap between dated events (the #56 80-year-gap failure mode).
- **Thesis-scope lock:** name the *exact* claim being rebutted, in the claimant's own words, so the steelman can't drift to the wrong sub-claim (#56 failure mode).
- **Logic-bridge plan:** every section→section transition names its connector before prose is written (operationalizes Rule 3 at outline stage, not as a post-hoc checkbox).
- Add a **quote-cold-test** to evidence selection: read each quote *cold* and ask "does this support or undercut my claim?" (the #56 de Marees quote accidentally confirmed the opposing claim).

### Change 3 — Read-Aloud Flag List (LOGIC — flag only)
New short output section `## READ-ALOUD FLAGS` listing **only mechanically-detectable** structural risks for the user to check during read-aloud: timeline gaps, undefined terms, sections lacking a connector, absolute-language assertions, cross-section redundancy.
- **Honest framing baked in:** this list does NOT validate the argument and does NOT replace the read-aloud. Memory `read-aloud-catches-logic` is explicit — "don't ship without it." The flag list narrows where the user looks; it never greenlights.

### Change 4 — Slim the frontmatter (ENABLER: make rules fire)
Move the ~120-line `version:` changelog out of frontmatter into `script-writer-v2-CHANGELOG.md`. Keep only the current version number. This reclaims context budget so the rules and the new ledger pass actually get model attention.

---

## Explicitly Dropped (and why)
- **Promise architecture, comment mining, angle differentiation** — packaging/demand concerns, zero effect on logic/clarity/hallucination.
- **Full rule-tree refactor** — cosmetic; Change 4 captures the attention win at far lower risk.
- **A back-end "AI self-audit for logic"** — the user's own data proves it doesn't work; building it would give false confidence and erode the read-aloud.

---

## Files to Change
| File | Change |
|---|---|
| `.claude/agents/script-writer-v2.md` | Replace checklist item :1561 with Claims Ledger pass; add timeline/thesis-scope/logic-bridge checks to Checkpoint 2; add quote-cold-test to evidence selection; add `## READ-ALOUD FLAGS` + `## CLAIMS LEDGER` to OUTPUT FORMAT; strip version history from frontmatter |
| `.claude/agents/script-writer-v2-CHANGELOG.md` | **New** — extracted version history |

---

## Verification
1. Run `/script` on a project with an existing `01-VERIFIED-RESEARCH.md` (e.g. an archived video, dry-run). Confirm the output includes a `## CLAIMS LEDGER` where every factual sentence maps to a source line, and any unsourced claim appears cut or flagged — not silently present.
2. Plant a deliberate unsourced causal bridge in a test research set; confirm the ledger catches and flags it.
3. Confirm Checkpoint 2 now emits the timeline-completeness + thesis-scope + logic-bridge plan before drafting.
4. Confirm `## READ-ALOUD FLAGS` appears and explicitly states it does not replace the read-aloud.
5. Confirm frontmatter is ≤10 lines and CHANGELOG holds the history.
6. **Acceptance:** on the next real script, the user's correction time on *sourcing* drops to near-zero (auto-cut), and read-aloud time goes to argument-level issues only.
