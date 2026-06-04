---
name: Thesis Discipline (Universal Throughline)
description: Universal 9-step throughline-finding procedure baked into script-writer-v2 (Rule 36) and article-writer (Rule 21). Source: /thesis-discovery 2026-04-29 from Manhattan/Tripoli iteration.
type: feedback
originSessionId: 8ef5c034-4296-431d-a7a9-3265287842c1
---
## Rule

Every script and article must derive a thesis via the universal 9-step procedure in `.claude/REFERENCE/THESIS-DISCIPLINE.md` BEFORE drafting. The thesis is a single ≤12-word claim, falsifiable, bigger than the case, that the audience carries away. Without thesis discipline, even tight evidence chains end as case summaries. Both agents enforce this.

**Why:** the user surfaced this gap on the Tripoli rough cut (2026-04-27) post-recording — the video chained evidence beautifully but ended without crystallizing a takeaway. The /thesis-discovery workflow on 2026-04-29 confirmed the methodology must be UNIVERSAL (any topic, any format), not topic-specific. The user explicitly rejected n=2 close-line patterns from being codified as universal rules — those are PROVISIONAL until performance data exists.

**How to apply:**

1. **Script-writer-v2 (Rule 36)** — fail-closed. If the agent cannot articulate a thesis in ≤12 words via Steps 1-9, the topic is not yet ready for scripting; return to research.
2. **Article-writer (Rule 21)** — mode-dependent:
   - CONVERT mode: inherit thesis from script's `**Thesis (Rule 36):**` metadata field. If missing, run NotebookLM Use Case 18 against research before drafting.
   - WRITE mode: derive thesis via Steps 1-9. If undeliverable, insert `[THESIS GAP — needs Use Case 18 before publish]` flag at top of draft (fail-open). User decides whether to fix or ship.
   - EDIT mode: audit existing draft against Steps 4-9; surface failures as line-level fixes, never silently rewrite.
3. **Topic-specific close patterns** (Manhattan/Tripoli "X didn't change, Y did" pivot, named-actors-and-reason close, placeable-artifact close, etc.) live in THESIS-DISCIPLINE.md Tier 3 with PROVISIONAL n=2 caveat. Treat as ideas for myth-projected-onto-static-artifact videos, not universal rules. Re-evaluate after both videos publish and analytics are available.

**Video #54 failure mode (2026-05-13 post-publish):** Thesis was clean (11 words, locked), but the video still felt like it jumped around. Root cause: three competing conclusions, none set up, none resolving the thesis:
- "The loophole was in the same paragraph" (procedural paradox — the actual thesis)
- "The real impact was living in fear" (human cost — different thesis, different audience takeaway)
- "Critics and defenders both miss X" (debate-referee — third thesis, no setup)

Plus the myth setup was unattributable: "people think the Inquisition operated outside the law" — user's reaction was "who thinks that btw??" — the myth wasn't grounded in a real, nameable claim.

Two new sub-rules added from this:

**Sub-rule A — Thesis execution ≠ thesis articulation.** A locked 11-word thesis does not enforce itself. After thesis lock, audit every beat: does this beat BUILD TOWARD, or AWAY FROM, or RESOLVE the thesis? A beat that produces a *different* conclusion than the thesis is a competing thesis. If three conclusions exist in the video, the thesis was never enforced beat-by-beat. Structure-checker or script-writer must run a "thesis trace" — label each beat's contribution to the thesis, not just check that a thesis exists.

**Sub-rule B — Myth must be attributable.** The opening myth must point to a specific, real claim. "People think X" is not a myth — it's a vague gesture. Test: *Who specifically thinks this? Where can a viewer verify it?* Acceptable: a named documentary, a scholarly position, a common media framing with an example, a real quote. Not acceptable: "people think," "many believe," "it's commonly assumed." If you can't name a source, the myth isn't concrete enough to refute — either find the source or reframe the opening.

**Stop conditions / anti-patterns:**

- Do NOT codify close-line patterns as universal rules without performance data. The user explicitly rejected this in /thesis-discovery (Q3 + Q5: "topic-specific to time-shifted-meaning videos"). Channel feedback memory rule "[Channel Data Not Actionable]" applies — n<30 is noise, n=2 is anecdote.
- Do NOT silently fix thesis gaps. If derivation fails, flag explicitly. The user has explicit feedback against silent corrections.
- Do NOT reuse Tripoli/Manhattan close lines as templates for unrelated topics. They worked there because the topic was static-artifact-with-shifting-meaning. Other topics need other close architectures.

**Files updated 2026-04-29:**
- New: `.claude/REFERENCE/THESIS-DISCIPLINE.md` (canonical universal methodology)
- New: `C:\Users\Benoi\.claude\projects\D--History-vs-Hype\memory\feedback-thesis-discipline.md` (this file)
- script-writer-v2.md → v14.5 (Rule 36 references THESIS-DISCIPLINE.md)
- article-writer.md → v5.1 (new Rule 21 + Quality Gate update)
- MEMORY.md (index entry added)

**Cross-reference:**
- The original signal that surfaced this discipline: `feedback-rough-cut-instincts.md` Instinct 8 (Tripoli post-recording gap)
- Operator-invocable workflow for ad-hoc thesis derivation on any project: `.claude/REFERENCE/THESIS-DERIVATION-WORKFLOW-PROMPT.md`
- NotebookLM prompt that runs Steps 1-7 against research: Use Case 18 in `NOTEBOOKLM-SCRIPTWRITING-PROMPTS.md`
