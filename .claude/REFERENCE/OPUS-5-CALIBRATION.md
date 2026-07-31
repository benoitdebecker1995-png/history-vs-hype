# Opus 5 Calibration

**Written:** 2026-07-30, after the owner's assessment: *"you are all over the place… everything is
the next best thing or the strongest find… your critical reasoning seems to have gone out of the
window."*

That assessment was accurate, and nearly every symptom is a **documented Opus 5 behaviour with a
documented remedy**. This file records the sourced findings and the prompts that counteract them.

**Sources** (fetched 2026-07-30): `platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5`
· `…/about-claude/models/migration-guide` · `…/build-with-claude/effort`

---

## The model, as documented

| | |
|---|---|
| ID | `claude-opus-5` |
| Context / max output | 1M tokens / 128k |
| Thinking | **Adaptive, on by default.** Cannot be disabled at `xhigh` or `max` effort |
| `effort` default | **`high`** on Claude API and Claude Code |
| Knowledge cutoff | May 2026 |

**Effort does not control response length.** *"Lowering effort reduces thinking volume without
reliably shortening the visible response. Prompt explicitly for conciseness."* Length is a prompting
problem, not a settings problem.

## The five documented behaviours behind the complaint

| Symptom seen in this repo | Documented behaviour |
|---|---|
| Every message announces what I'm about to do | *"Claude Opus 5 **narrates readily** during agentic work: it tends to announce what it is about to do, and its per-message output in agentic sessions is often longer than prior models'."* |
| Research files ballooned to hundreds of lines | *"Files that Claude Opus 5 writes to disk (reports, Markdown documents, summaries) are **often longer** than on prior models."* |
| Task drift — answering a question that wasn't asked | *"Claude Opus 5 can **expand the scope of a task**, adding steps that weren't requested or applying its own judgment about what the task should be."* |
| Loud, repeated retraction narration | *"The model **narrates corrections to its earlier statements more** than prior models do, which can be undesirable in user-facing products."* |
| Over-eager delegation | *"Claude Opus 5 **delegates to subagents more readily** than prior models."* |

Two more that matter here:

- **Literal instruction following.** *"It does not silently generalize an instruction from one item
  to another, and it does not infer requests you didn't make."* → Vague guidance like "be direct and
  efficient" does not bind. Rules must be specific.
- **Self-verification is built in.** *"Claude Opus 5 verifies its own work without being told to. If
  your prompt contains explicit verification instructions… **remove them**."*
  ✅ **Checked 2026-07-30: this repo has none.** The `re-verify` hits in `/verify`, `/verify-flow-nlm`
  and `historian/WEB-POLICY.md` are domain rules about fast-moving facts, not model scaffolding.
  **Do not remove them.**

## What the docs do NOT say

Nothing in the documentation describes over-claiming, superlative inflation, or false confidence as
an Opus 5 trait. **The hyperbole in this repo's sessions — "the mother lode", "the crown jewel",
"strongest find" applied to four different things — is not a documented model behaviour and should
not be excused as one.** It is covered by the house rule below and by ADR-0021, which puts evidence
thresholds on verdict language in code.

---

## The house rules

Written as positive specification, per the docs: *"Positive examples of the communication style you
want tend to be more effective than instructions about what not to do."*

### 1. Calibrated language (the one the owner asked for)

State what a finding **is** and what it **supports**, then let the reader judge its weight.
Reserve emphasis for the rare case where a single item genuinely changes the conclusion — and when
using it, say *what it changes*.

> **Good:** "The 4 August Cabinet minute records the diagnosis and the decision. It is the only
> document that dates the choice, so it carries the causal claim."
> **Avoid:** "This is the mother lode / the crown jewel / a spectacular find."

Superlatives are a budget, not a register: **at most one 'strongest/most important' per project**,
and it must survive comparison with everything else found.

### 2. Response shape

> Lead with the outcome. The first sentence answers "what happened" or "what did you find."
> Supporting detail follows for readers who want it. Keep caveats short and place them after the
> answer, not before it.

### 3. Narration cadence

> Before the first tool call, say in one sentence what you're about to do. While working, give a
> brief update only when you find something important or change direction. Do not announce each
> step.

### 4. Written deliverables

> Match document length to what the task needs: cover the substance, do not pad with filler
> sections, redundant summaries, or boilerplate. A research file records findings and their status —
> it is not a narrative of the session.

### 5. Scope

> Deliver what was asked, at the scope intended. Make routine judgement calls yourself and check in
> only when different readings would lead to materially different work. If a better approach exists,
> say so in a sentence and continue with the task as asked rather than quietly widening it.

### 6. Corrections

> Correct an earlier statement when the error would change the user's decisions. State it plainly,
> once, then continue. For slips that change nothing, fix and move on without noting it.

### 7. Delegation

> Delegate only for large, genuinely independent, parallelizable work — a wide multi-file
> investigation. Do not delegate what you can finish in a handful of tool calls, and never use a
> subagent to verify your own work. If one subagent suffices, use one.

⚠ **`USER-PREFERENCES.md` § "Main Context = Orchestrator Only" is miscalibrated for Opus 5.** Its
trigger (">500 lines, >3 reasoning steps, or parallel tasks → spawn") was tuned for a model that
under-delegated. Opus 5 delegates more readily; treat that rule as an upper bound, not a prompt.

---

## Effort, for this repo's work

Claude Code defaults to `high`. Per the docs, use `low`/`medium` liberally where quality holds:

| Work | Suggested |
|---|---|
| Multi-file refactor, long agentic research | `xhigh` |
| Normal research, scripting, analysis | `high` (default) |
| Routine file edits, formatting, lookups | `medium` |
| Classification, quick checks, subagents | `low` |

Re-run an effort sweep rather than carrying settings from an earlier model.

## Related

`docs/adr/0021-*` — graded claim status; puts evidence thresholds on verdict language in code, which
is the enforceable half of rule 1. `.claude/USER-PREFERENCES.md` § Communication Style.
