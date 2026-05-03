# Thesis Discovery — Improve script-writer-v2 + article-writer

**Purpose:** Socratic-discovery workflow. Surface WHY the thesis/red-thread approach clicks for the creator, codify it into named principles, and bake those principles into both agent files. Designed to run AFTER several thesis-locked projects (currently: Manhattan #45 + Tripoli #51) when patterns are visible but unarticulated.

**Outcome:** Updated `script-writer-v2.md`, updated `article-writer.md`, new `THESIS-DISCIPLINE.md` reference doc, indexed memory.

**Hard rule:** This is a discovery loop. DO NOT write to agent files before Phase 3 user approval. DO NOT invent principles the user did not validate.

---

## SYSTEM CONTEXT (auto-load before Phase 1)

Read these files in parallel before doing anything else:

- `.claude/agents/script-writer-v2.md` — current Rule 36 (THESIS THROUGH-LINE), Quality Checklist, metadata template
- `.claude/agents/article-writer.md` — current state (NO thesis discipline yet)
- `.claude/REFERENCE/THESIS-DERIVATION-WORKFLOW-PROMPT.md` — existing Phase 0-6 workflow
- `.claude/REFERENCE/NOTEBOOKLM-SCRIPTWRITING-PROMPTS.md` — Use Case 18 (Thesis Articulation Check)
- `.claude/REFERENCE/SCRIPT-TO-DELIVERY-LESSONS.md` — Lesson 32 (Walk-Away Test)
- `C:\Users\Benoi\.claude\projects\D--History-vs-Hype\memory\feedback-rough-cut-instincts.md` — the 8 instincts
- `video-projects/_IN_PRODUCTION/45-manhattan-purchase-myth-2026/SCRIPT.md` — locked thesis + close (Option 1: William Penn / American Legion)
- `video-projects/_IN_PRODUCTION/45-manhattan-purchase-myth-2026/THESIS-CANDIDATES-NLM.md` — 5 candidates from Round 1
- `video-projects/_IN_PRODUCTION/45-manhattan-purchase-myth-2026/THESIS-THROUGHLINE-EDITS-NLM.md` — Round 2 audit
- `video-projects/_IN_PRODUCTION/51-treaty-tripoli-article-11-2026/tripoli, rough cut, instincts.srt` — voice ground truth (the user's improvised close)
- `video-projects/_IN_PRODUCTION/51-treaty-tripoli-article-11-2026/02-SCRIPT-DRAFT.md` — Tripoli script vs delivery

State briefly: "Loaded context. Starting Phase 1 — NotebookLM synthesis."

---

## PHASE 1 — NotebookLM synthesis call

Notebook: `92a51593-8878-4314-a144-bb926ef1584a`
Conversation continuation (Manhattan thesis chain): `77dd43f6-6aa3-449a-a9bd-63840ae5ae63`

Call `mcp__notebooklm__notebook_query` with this exact text:

```
Synthesize the design space we've been navigating across the Manhattan thesis lock (project 45) and the Tripoli rough-cut close (project 51). The creator says the thesis approach feels like "a theme payoff or thing the video works towards" but cannot articulate WHY. Do these three things:

1. List 5 distinct DESIGN CHOICES we made implicitly during these projects. For each: state the choice we ended up making and the alternative we rejected. Examples of axis types (do not just reuse these — derive your own from the actual work):
   - thesis as ABSTRACT PRINCIPLE vs CONCRETE TAKEAWAY
   - close as SLOGAN vs as DEFLATION
   - thesis stated VERBATIM in script vs FELT through evidence
   - quote-bridged close vs author-written close
   - cause-chain density vs evidence density

2. Generate 5 SHARP diagnostic questions that will force the creator to articulate WHY the choices we made click. Each question MUST:
   - Reference TWO specific examples from the actual work (e.g., "Compare 'manufactured motive' (rejected) vs 'cast those projections into a bronze plaque' (locked) — which feels earned, and pin down the structural reason in one sentence")
   - Be answerable in 2-4 sentences
   - Surface a PRINCIPLE, not just a preference
   - Avoid yes/no framing
   - Use the creator's actual rejected/locked examples — not hypotheticals

3. For each question, state in ONE LINE the design principle the answer will lock in.

Do not invent design principles. Surface ones already IMPLIED by the choices in the locked work. Output as numbered list with question + principle on each.
```

If the query fails or returns < 5 questions, retry once with tightened framing. If still failing, escalate to the user before continuing.

---

## PHASE 2 — Surface questions to user

Take NotebookLM's 5 questions. For each, use `AskUserQuestion` (max 4 options + free-text "Other"). If a question has no good multi-choice options, ask in plain text — do not invent fake options to fit the tool.

Ask one at a time, NOT all 5 in one call. Each question informs the framing of the next.

After each answer, write a one-line internal note: "Q[N] surfaced: [principle]." Do not show these notes to the user yet.

---

## PHASE 3 — Synthesize and confirm

Distill the 5 answers into:

1. **3–5 named principles** — short, voice-matched ("the close lands on a physical object, never an abstraction"). State each as a falsifiable rule.
2. **Ban list** — specific phrases/patterns that trigger cringe (e.g., "manufactured motive," "Which is why," "in other words").
3. **Required list** — specific patterns that produce the earned feel (e.g., "X didn't change, Y did" pivot; modern-stakes opening; artifact deflation).
4. **Cross-format mapping** — how each principle applies to scripts vs articles. Note: scripts have hook/turn/close; articles have lede/pivot/landing.

Show the user this 1-screen synthesis. Ask: "Does this match what you actually feel? Yes / refine / redo."

If "redo," return to Phase 1 with sharper framing (use the user's pushback as the new constraint).

---

## PHASE 4 — Apply to agents (only after Phase 3 approval)

### a) Update `.claude/agents/script-writer-v2.md`
- Refine Rule 36 (THESIS THROUGH-LINE) with new principles
- Add or expand a "Voice-Anchored Closing" subsection with the locked 4-beat rhythm + ban list + required list
- Update Quality Checklist with new gates
- Bump version (currently v14.4 → v14.5)
- Add to changelog: "v14.5 — Thesis discipline locked from Manhattan/Tripoli iteration. New principles: [list]. Source: `THESIS-DISCIPLINE.md`."

### b) Update `.claude/agents/article-writer.md`
- Add a new Rule (next available number) for THESIS DISCIPLINE adapted for articles
- Map 3-slot structure: opening lede / mid-piece pivot / closing artifact-anchor
- Add same ban list + required list
- Bump version (currently v5.0 → v5.1)
- Add to changelog

### c) Create `.claude/REFERENCE/THESIS-DISCIPLINE.md`
Structure:
```
# Thesis Discipline — Voice-Locked Principles

**Locked:** [today's date]
**Source:** Manhattan #45 + Tripoli #51 iteration; discovery via /thesis-discovery on [date]

## Principles
[3-5 named principles, falsifiable]

## Ban list
[phrases that trigger cringe — with examples from rejected work]

## Required list
[patterns that produce earned feel — with examples from locked work]

## Cross-format slot mapping
| Slot | Script | Article |
|---|---|---|
| Tee-up | Hook (artifact + question) | Lede (artifact + question) |
| Pivot | Turn beat (~20% mark) | Mid-piece (after evidence stack) |
| Landing | Close (4-beat rhythm) | Closing paragraph (artifact-anchored) |

## Worked examples
- Manhattan: thesis = "[thesis]"; close = Option 1 (William Penn / American Legion)
- Tripoli: thesis = "[thesis]"; close = "didn't change but the culture did" (rough-cut improvised)

## Rejected (banned) examples
- "The bronze plaque covers a missing archive with a manufactured motive." — academic-sloganeering
- "Which is why the plaque calls its own story a legend." — too compressed; outsources thesis to cited quote
- [...]
```

### d) Memory + index update
- Create `C:\Users\Benoi\.claude\projects\D--History-vs-Hype\memory\feedback-thesis-discipline.md` with:
  - Frontmatter: `name: Thesis Discipline (Voice-Locked)`, `description: Locked principles for thesis through-line in scripts and articles. Source: Manhattan/Tripoli iteration via /thesis-discovery.`, `type: feedback`
  - Body: lead with the rule, then **Why:** (the user's stated reason), then **How to apply:** (when this fires)
- Add one line to `MEMORY.md`:
  `- [Thesis Discipline](feedback-thesis-discipline.md) — voice-locked principles for thesis through-line; source: Manhattan/Tripoli iteration`

---

## PHASE 5 — Confirm

Show user a one-screen diff summary:
- "script-writer-v2.md → v14.5: added [X principles], banned [Y phrases]"
- "article-writer.md → v5.1: added thesis discipline rule"
- "Created THESIS-DISCIPLINE.md"
- "Memory indexed"

Ask: "Commit?" If yes → atomic commit with message format `agents(thesis): lock voice-anchored thesis discipline from /thesis-discovery — script-writer v14.5, article-writer v5.1, THESIS-DISCIPLINE.md`.

---

## CONSTRAINTS

- MUST NOT write to agent files before Phase 3 user approval
- MUST NOT invent principles the user did not validate
- MUST keep each NotebookLM call under 3500 chars
- MUST NOT touch locked project files (Manhattan #45 SCRIPT.md, Tripoli #51 SCRIPT.md)
- MUST NOT skip the discovery loop and write straight to agent files
- Stop conditions: if user rejects synthesis at Phase 3 twice, stop and report — do not push through

## SUCCESS CONDITION

- Agents updated, ref doc created, memory indexed
- Principles are TESTABLE (each rule is falsifiable: "the close lands on a physical object" → can be checked yes/no on any draft)
- User confirms the synthesis matches what they actually feel
- Next time the user runs script-writer-v2 or article-writer on a new project, the thesis discipline fires automatically without re-litigating
