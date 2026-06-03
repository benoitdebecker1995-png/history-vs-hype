# PLAN — P11 v2: Research-as-Production-Input Reframe
**Date:** 2026-05-21 (v2 supersedes v1 same date)
**Status:** DRAFT (awaiting user approval to hand to Sonnet)
**Source:** Follow-up to `PLAN-2026-05-21-session-improvements.md`. v1 was scoped to "catch the Lloyd Jones attribution class." v2 reframes to the user's actual target: **make videos better via better research**, where "better research" = topic discovery (already handled) + video viability (new) + NotebookLM angle-discovery (new) + source acquisition (new) + validated-for stamp (carried from v1).

**Implementer:** Sonnet (when approved)

---

## 0. Why v1 was wrong scope and v2 exists

v1 designed a research-phase attribution gate to catch the Lloyd Jones / scopic regime cite-selection drift earlier than `/verify` Step 7.5. Honest catch-rate against the Hijab #52 failure set: 1 of 5. Per the grill, that's incremental — not what "research improves videos" means.

The Hijab #52 failures are also not the right optimization target for research-phase improvements. The real target: **research today produces a fact ledger, but not a production input.** The script phase re-does most of the work — thesis discovery, hook selection, mechanism-word lock, source-tier mapping. When research returns a fact set that doesn't actually fuel a 8-12 min video, the channel discovers it at script-write or comment-mine time. Cycle cost: weeks per missed topic.

v2 attacks this by making the research phase do four things it doesn't do today:

| Workstream | Status today | v2 outcome |
|---|---|---|
| Topic surfacing (interesting things) | Handled (`/comment-mine`, VidIQ, competitor) | Unchanged |
| Video viability gate | None | PROCEED / SHARPEN / DEFER verdict on every topic at research-time, BEFORE deep Phase 2 spend |
| NotebookLM angle-discovery | NLM used for verification only | NLM also surfaces candidate hooks, thesis verbs, closing payoffs from the notebook itself |
| Source acquisition | Ad-hoc | Prioritized acquisition queue mapped to T-tier gaps |
| Validation dimensions | Single ✅ flag | Validated-for stamp records what was actually checked (carried from v1) |

---

## 1. What P11 v2 ships (four sub-tasks)

| Sub-task | Target file | Purpose |
|---|---|---|
| **P11.1** | `D:\History vs Hype\.claude\commands\research.md` | Research-Viability Gate: PROCEED / SHARPEN / DEFER verdict after Phase 1, before full Phase 2 spend |
| **P11.2** | `D:\History vs Hype\.claude\commands\research.md` + `D:\History vs Hype\.claude\REFERENCE\NOTEBOOKLM-RESEARCH-PROMPTS.md` | Phase 2 angle-discovery: NLM-driven candidate hooks, thesis verbs, closing payoffs |
| **P11.3** | `D:\History vs Hype\.claude\commands\research.md` + `D:\History vs Hype\.claude\templates\01-VERIFIED-RESEARCH-TEMPLATE.md` | Source-acquisition queue: prioritized list of primary sources to chase, mapped to T-tier upgrade gaps |
| **P11.4** | `D:\History vs Hype\.claude\templates\01-VERIFIED-RESEARCH-TEMPLATE.md` | Validated-for stamp on claim/quote/archival blocks (carried from P11 v1) |

Four files touched total. P11.1 + P11.2 share `research.md`. P11.3 + P11.4 share the template. Independent to implement; recommended order in §6.

---

## 2. P11.1 — Research-Viability Gate

**File to edit:** `D:\History vs Hype\.claude\commands\research.md`

**Problem this solves:** Today, after `/greenlight` passes (packaging viability), the channel proceeds straight to deep Phase 2 NotebookLM verification. There's no checkpoint between Phase 1 (internet research brief) and full Phase 2 (academic verification) that asks: *given what we know from Phase 1, can this topic actually become a defensible 8-12 min video at this channel's standard?* When the answer is no, the discovery comes at script-time or never.

**What to add:** A new section in `research.md` titled `### Step N: Research-Viability Gate (PROCEED / SHARPEN / DEFER)`. Sonnet, find the right step number — this runs after the Phase 1 brief is drafted (around current Step 7 / line 211) and BEFORE the full Phase 2 NotebookLM verification spend.

**Behavior the section must specify:**

1. **Trigger condition.** Runs once per topic, after Phase 1 brief is drafted and the initial NotebookLM notebook is populated with Phase 1 sources (Wikipedia, news, top-3 academic suggestions). Cannot be skipped — `/research` cannot proceed to deep Phase 2 without a verdict.

2. **Four viability checks.** For each topic, evaluate against the channel's locked standards:

   **a. Primary-source accessibility map.** From the Phase 1 brief, list every load-bearing claim and estimate its likely tier:
   - T1 candidates: count of claims where a primary document is plausibly accessible (digitized, edition known, in language the channel can verify — French/Spanish/German/Latin/Greek/Dutch)
   - T2 candidates: count of claims where a primary exists but only via Anglophone scholar quotation
   - T3-only: count of claims where only scholarly interpretation is available
   - Output a ratio. Heuristic: if T3-only > 30%, the topic is at the channel's verification ceiling. Flag for SHARPEN or DEFER.

   **b. Specificity-bomb count.** Per the niche-wide data (5.4x retention lift for specificity_bomb hook type), the topic must have ≥3 specific named documents/figures/quotes available that could anchor the hook + turn + closer. Heuristic: query the Phase 1 NotebookLM notebook for specific dates, named documents, named figures with documented actions. If <3 surface clearly, the topic lacks the specificity engine.

   **c. Mechanism-word NLM-confidence.** Per `feedback-auditors-edge.md` extension and `feedback-topic-vs-angle-ordering.md`, the title's mechanism word must be technically defensible against primary documents. Generate 3 candidate mechanism words from Phase 1 brief. For each, run a NotebookLM confidence query (per existing `feedback-notebook-citation-grounding.md` scope-b rule). At least one mechanism word must return HIGH confidence. If all three return LOW, the topic doesn't yet have a defensible mechanism — flag SHARPEN (gather more sources) or DEFER (mechanism may not exist).

   **d. Thesis-discipline pre-check.** Per `THESIS-DISCIPLINE.md`, can a ≤12-word throughline be drafted from the Phase 1 brief? Run the 9-step procedure on the brief. If the throughline collapses to a fact-list rather than a sharp claim, the topic lacks thesis density — flag SHARPEN.

3. **Verdict logic.**

   - **PROCEED** — All four checks pass. Topic is viable; deep Phase 2 spend is justified. Move to next step.
   - **SHARPEN** — One or two checks soft-fail. Topic is plausibly viable but needs another round of Phase 1 work (additional sources, sharper angle, mechanism-word substitution). Output a specific punch-list of what's missing. Re-run viability gate after the punch-list closes.
   - **DEFER** — Three or four checks fail, OR the T3-only ratio exceeds 30% in a language the channel can't verify directly. Topic is not viable at the channel's current standard. Output a deferral note: what would need to change (language capability built, sources acquired, angle re-found) before this topic becomes viable. Move to channel-data/TOPIC-PIPELINE.md backlog.

4. **Output: `RESEARCH-VIABILITY.md` in the project folder.** Single file containing:
   - The four check results with evidence
   - The verdict
   - If SHARPEN: the punch-list
   - If DEFER: the deferral note
   - Signed-off date and verifier (user or agent)

5. **Gate behavior.** `/research` cannot enter deep Phase 2 verification until `RESEARCH-VIABILITY.md` shows verdict PROCEED. SHARPEN routes back to Phase 1. DEFER moves the topic to backlog.

**Where to place the step:** Inside the `/research` workflow, after Phase 1 brief generation and before the Phase 2 NotebookLM verification step. Sonnet: read the full file first to find the right insertion point — current structure runs Step 7 (Phase 1 deliverable) → Step 8 (NotebookLM source list). The gate inserts as Step 7.5 or as a new Step 8 with existing Step 8 renumbered.

**Cross-reference to add at the top of the new section:** "See `memory/feedback-auditors-edge.md` §'tier-vibe' for the T-tier accessibility map, `feedback-notebook-citation-grounding.md` §'mechanism claims' for the NLM-confidence check, `THESIS-DISCIPLINE.md` for the throughline pre-check, and `feedback-topic-vs-angle-ordering.md` for the broader 'angle locks at research, not script' principle."

**Acceptance:** After the edit, a dry-run of `/research` on a hypothetical new topic produces a `RESEARCH-VIABILITY.md` with the four checks evaluated and a verdict. Sonnet should NOT execute against a live topic — the acceptance is structural (the workflow step exists, the file shape is correct).

---

## 3. P11.2 — Phase 2 NotebookLM Angle-Discovery

**Files to edit:**
- `D:\History vs Hype\.claude\commands\research.md`
- `D:\History vs Hype\.claude\REFERENCE\NOTEBOOKLM-RESEARCH-PROMPTS.md`

**Problem this solves:** Phase 2 NotebookLM today does verification work — round-trip quotes, confirm citations, surface contradictions. The notebook *also* contains the raw material for the script's structural decisions (hook, turn, closer, mechanism word, thesis verb), but the workflow doesn't query for them. Discovery happens at script-write time when the writer is reading the verified-research file and improvising. Improvisation produces inconsistent quality.

**What to add to `research.md`:** A new section titled `### Step N+1: NotebookLM Angle-Discovery Pass`. Sonnet: this runs as part of Phase 2, AFTER standard verification is complete, BEFORE the `01-VERIFIED-RESEARCH.md` is marked READY TO WRITE SCRIPT.

**Behavior the section must specify:**

1. **Three angle-discovery queries to run, in order.** Each query is a canonical prompt from `NOTEBOOKLM-RESEARCH-PROMPTS.md` (added in this sub-task — see below).

   **Query AD-1: Candidate Hook Quotes (specificity-ranked).** Ask NotebookLM to surface the top 5 most specific, surprising, anchor-able quotes from the notebook — quotes that contain a named person + a named document or date + a concrete fact. Rank by specificity-bomb score (named entities + date precision + factual surprise). Each candidate gets a Tier tag (T1/T2/T3 per `feedback-auditors-edge.md`) and a quote-grounding confidence score.

   **Query AD-2: Candidate Thesis Verbs (mechanism-word grounding).** Per `THESIS-DISCIPLINE.md`, the ≤12-word throughline contains a single action verb (the mechanism word — "mistranslated," "extended," "forbade," "engineered"). Ask NotebookLM to surface 3 candidate verbs that describe what the historical actors actually did in this topic, with quote evidence supporting each. Per `feedback-auditors-edge.md` extension, the mechanism word must be technically defensible.

   **Query AD-3: Candidate Closing Payoffs.** Ask NotebookLM to surface the 3 most surprising or anchoring facts in the notebook that could carry the script's closing beat — facts that re-frame what the viewer just learned in a memorable single line. Rank by surprise + concreteness + memorability.

2. **Output to `01-VERIFIED-RESEARCH.md`.** Add a new section titled `## CANDIDATE ANGLES (NLM-discovered, Phase 2)` containing:
   - **Top 5 hook quote candidates** — full quote, source, page, tier, specificity-bomb score
   - **Top 3 thesis verb candidates** — verb, supporting evidence, NLM-confidence
   - **Top 3 closing payoff candidates** — fact, source, surprise-score, suggested phrasing

3. **Use case downstream.** When the script phase begins, the writer (or `script-writer-v2` agent) does not start from scratch — they start from the candidate angles. Final hook / thesis verb / closer are chosen from the candidate list (or explicitly rejected with a recorded reason). This routes the channel's specificity discipline upstream of script-write, instead of relying on the writer's improvisation.

**What to add to `NOTEBOOKLM-RESEARCH-PROMPTS.md`:** Three new canonical prompts matching the existing file's format (`### Prompt N: <name>` / `**When to use:**` / `**Prompt:**` block / `**Example usage:**`). Prompts AD-1, AD-2, AD-3 each get one section.

For each prompt:
- Include `[TOPIC]`, `[NOTEBOOK_ID]` placeholders
- Ask NotebookLM to return responses with `[1], [2]` citation markers so the existing `tools/citation_extractor.py` works
- Specify ranking criteria explicitly so results are deterministic across runs

A worked example for each, ideally drawn from a past project (Tripoli #51, Inquisition #54, or Hijab #52) so future workers see what good output looks like.

**Where to place the new prompts:** Inside `NOTEBOOKLM-RESEARCH-PROMPTS.md`, in a new section after the existing "Core Research Prompts" titled `## Angle-Discovery Prompts (P11.2)`. Match the existing file's tone and structure.

**Cross-reference to add at the top of the `research.md` step:** "See `THESIS-DISCIPLINE.md` for the thesis-verb framework, `feedback-auditors-edge.md` for the tier-vibe applied to candidate quotes, `script-writer-v2` Rules 17/27.B/36/42 for downstream consumers of these candidates."

**Acceptance:** After the edit, the three new prompts exist in `NOTEBOOKLM-RESEARCH-PROMPTS.md` with worked examples. The Phase 2 workflow in `research.md` references them and specifies the output section in `01-VERIFIED-RESEARCH.md`.

---

## 4. P11.3 — Source-Acquisition Queue

**Files to edit:**
- `D:\History vs Hype\.claude\commands\research.md`
- `D:\History vs Hype\.claude\templates\01-VERIFIED-RESEARCH-TEMPLATE.md`

**Problem this solves:** When P11.1's viability gate returns SHARPEN with a T-tier accessibility gap (e.g., "5 load-bearing claims at T3-only; need T2 or T1 paths"), there's no workflow that produces a prioritized acquisition list. The user has to mentally translate the gap into a JSTOR/Library/ILL/archive task list. This makes upgrading T3→T2 or T2→T1 high-friction and rare.

**What to add to `01-VERIFIED-RESEARCH-TEMPLATE.md`:** A new section at the end of the template (before "RESEARCH NOTES") titled `## SOURCE ACQUISITION QUEUE`. The section structure:

```markdown
## SOURCE ACQUISITION QUEUE

**Purpose:** Track primary sources to acquire that would upgrade T3 claims to T2 or T1.
**Generated from:** RESEARCH-VIABILITY.md gap analysis.
**Status legend:** TARGETED / ATTEMPTING / ACQUIRED / UNAVAILABLE / DEFERRED

### Acquisition: [Source name]
- **Upgrades claim:** [Which claim in this file gets upgraded]
- **Current tier:** [T3 / T2]
- **Target tier:** [T2 / T1]
- **Source type:** [Primary document / Critical edition / Manuscript scan / Archival reference]
- **Access path:** [JSTOR URL / Library catalogue / ILL request / Archive contact / Online repository]
- **Estimated effort:** [Low / Medium / High] — [free / paywall / ILL turnaround / archive trip]
- **Priority:** [1-3, where 1 = blocks viability, 3 = nice-to-have]
- **Status:** TARGETED / ATTEMPTING / ACQUIRED / UNAVAILABLE / DEFERRED
- **Notes:** [Why this matters, why it's accessible, blockers]
```

Add a SUMMARY block above the individual entries:
```
**Queue summary:** [N] sources targeted | [N] acquired | [N] unavailable
**Highest priority unresolved:** [Source name + claim it unblocks]
```

**What to add to `research.md`:** A new section titled `### Step N+2: Source Acquisition Queue Generation`. This step runs AFTER P11.1's viability gate returns SHARPEN (or PROCEED with noted gaps), but BEFORE deep Phase 2 NotebookLM verification spend.

Behavior the section must specify:

1. **Trigger condition.** Runs when viability gate output shows ≥1 T3-only claim that could plausibly be upgraded. Skips when all claims are already T1 or T2.
2. **Per-gap analysis.** For each T3-only claim in the viability gap list:
   - Identify the primary document that would close the gap
   - Identify the access path (JSTOR / Library / ILL / archive)
   - Estimate effort (free vs paywall vs trip)
   - Assign priority based on how load-bearing the claim is (load-bearing for thesis = P1; load-bearing for scene = P2; nice-to-have = P3)
3. **Populate the SOURCE ACQUISITION QUEUE section** of `01-VERIFIED-RESEARCH.md` with one entry per gap.
4. **Output a punch-list.** A short markdown summary at the top of the queue: which P1 acquisitions block viability re-evaluation, which P2-P3 are nice-to-have.
5. **Re-evaluation hook.** After P1 acquisitions are marked ACQUIRED, the user re-runs `/research` viability gate. PROCEED becomes reachable.

**Where to place the step:** Inside the `/research` workflow, after the viability gate (P11.1) and before deep Phase 2. Sonnet: read the file to confirm the right insertion point.

**Cross-reference to add at the top of the new step:** "See `memory/feedback-auditors-edge.md` §'tier-vibe' for what T-tier upgrades mean and `memory/feedback-research-audit.md` for the existing P/S/S→P system this queue feeds."

**Acceptance:** After the edit, a fresh `01-VERIFIED-RESEARCH.md` (created via `/research`) carries the SOURCE ACQUISITION QUEUE section. The `/research` workflow has a step that populates it from viability-gap output.

---

## 5. P11.4 — Validated-for Stamp (carried from v1)

**File to edit:** `D:\History vs Hype\.claude\templates\01-VERIFIED-RESEARCH-TEMPLATE.md`

(Identical to v1's P11.A. Carried forward because the validated-for stamp is the structural enabler for the F5 methodology-bias rule. Brief restatement here; for full detail see v1 P11.A.)

**What to add:**

1. To the claim block: insert `**Validated for:** [verbatim text / attribution origin / edition+page / numeric value / all of the above]`, `**Validated against:** [NotebookLM project notebook ID / direct primary-source PDF path / scholar's apparatus only]`, `**Validation date:** [YYYY-MM-DD]` between `**Sources (min 2):**` and `**Notes:**`.
2. To the VERIFIED QUOTES block: insert the same three fields, replacing the existing single-line `**Verified:**` field.
3. To the ARCHIVAL REFERENCES block: insert the same three fields between `**Verified from:**` and `**Common errors:**`.
4. Update the RULES list to add Rule 4: "Every VERIFIED row must carry a Validated-for stamp. ✅ without a Validated-for value = treat as ⏳ until stamped."
5. Update the READY TO WRITE SCRIPT checklist to add: "- [ ] Every VERIFIED claim has a Validated-for stamp recording what dimension was checked"

**Cross-reference:** "See `memory/feedback-postmortem-methodology.md` §'second methodology-bias dimension' for why each ✅ row must record what dimension it was validated for."

**Acceptance:** Identical to v1 P11.A — fresh template carries the fields; rules/checklist updated.

---

## 6. Implementation order for Sonnet

Recommended sequential order (some are dependent; respect the order):

1. **P11.4 first** (template Validated-for stamp — smallest, no dependencies, prerequisite for P11.3's queue entries).
2. **P11.1 second** (viability gate — independent of the others; produces the gap analysis that P11.3 consumes).
3. **P11.3 third** (acquisition queue in template + research.md step — consumes P11.1's gap output; depends on P11.4's template structure being in place).
4. **P11.2 fourth** (angle-discovery in research.md + new prompts in NOTEBOOKLM-RESEARCH-PROMPTS.md — independent of the others structurally; placed last because it's the largest standalone block).

Each sub-task ends with the verification checklist from `PLAN-2026-05-21-session-improvements.md` §6:
- Read file end-to-end before editing
- Identify natural insertion point
- Include cross-reference at top of new section
- Match existing file's tone and structure
- Read-back of edited section to confirm

---

## 7. What P11 v2 does NOT solve (and why)

- **Arabic-source verification capability** — still parked. P11 v2 doesn't include the OCR + Arabic NotebookLM corpus pilot. When viability gate sees Arabic claims at T3-only with no language path, verdict will be DEFER (or SHARPEN with the acquisition queue noting "Arabic verifier needed"). This is the *honest* output; it's not solving Arabic, but it's flagging that it can't.
- **The Lloyd Jones attribution class** — caught downstream at `/verify` Step 7.5 (already shipped in P7). P11 v2 dropped v1's attribution gate because the catch is already in place; making it redundant at research time adds friction without changing the catch-rate (P7 fires before script-lock, which is upstream of every consequence).
- **Comment-mining integration** — `/comment-mine` already runs separately and feeds the angle pipeline. P11 v2 doesn't bundle it into `/research`; the two stay as parallel inputs to topic decisions.
- **Retroactive re-running on past projects** — forward-going only. Past `01-VERIFIED-RESEARCH.md` files don't get re-stamped, re-viability-checked, or re-acquisition-queued.
- **Tool sprawl** — per [Tool Discovery Before Proposing], extensions to existing `/research`, existing template, existing prompt file only. No new commands, no `/research-viability` sister tool, no `/source-acquire` standalone.

---

## 8. Honest assessment of P11 v2's expected impact

**What this will probably change in future videos:**

- **Fewer wasted Phase 2 spends** on topics that can't reach the channel's standard. Viability gate kills bad topics at hour 3 instead of hour 30.
- **Sharper hooks at lower writing cost.** Angle-discovery surfaces the specificity-bomb candidates from the notebook automatically. The writer chooses; they don't improvise.
- **Defensible mechanism words by default.** The viability gate forces mechanism-word grounding before deep Phase 2. Topics that don't have a defensible mechanism never reach the title phase.
- **Reduced session re-derivation cost.** Validated-for stamps mean future sessions don't inherit ✅ rows as universally authoritative — they see what was checked.

**What this will NOT change:**

- Arabic-source video viability (still gated by language capability, not by P11)
- Topics with genuinely no defensible mechanism (these get DEFERRED honestly, which is the correct outcome — but the channel still needs a viable topic to ship)
- Writing-stage quality (P11 makes research a better input to writing; it doesn't make the writer better)
- Channel growth bottleneck (packaging is still the #1 bottleneck per memory; P11 doesn't touch packaging)

**Cost vs. benefit at 1 video/week cadence:**

- Implementation cost (Sonnet pass): ~one focused session, 4 files
- Operational cost per video: viability gate adds ~30 min at Phase 1→2 boundary; angle-discovery adds ~20 min at Phase 2 end; acquisition queue is ~15 min when triggered; Validated-for stamps add ~1-2 min per claim
- Benefit per video: estimated 2-5 hours saved at script-write time (sharper inputs), plus the topic-kill savings on bad-fit topics

Net: probably positive at this cadence; verify after 3-4 videos with the new flow.

---

## 9. Cross-reference index for Sonnet

| Sub-task | Read this memory file first |
|---|---|
| P11.1 (viability gate) | `feedback-auditors-edge.md` + `feedback-topic-vs-angle-ordering.md` + `THESIS-DISCIPLINE.md` |
| P11.2 (angle-discovery + prompts) | `feedback-auditors-edge.md` + `THESIS-DISCIPLINE.md` + existing `NOTEBOOKLM-RESEARCH-PROMPTS.md` |
| P11.3 (acquisition queue) | `feedback-auditors-edge.md` (tier-vibe) + `feedback-research-audit.md` (P/S/S→P) |
| P11.4 (Validated-for stamp) | `feedback-postmortem-methodology.md` (validated-for principle) |

End of draft.
