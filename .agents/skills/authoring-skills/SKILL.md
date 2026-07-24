---
name: authoring-skills
description: Craft standard for writing and editing this repo's instruction surfaces — SKILL.md files, slash-command files, and agent files. The vocabulary and levers that make an instruction predictable. Use when: creating or editing any file under `.Codex/skills/`, `.Codex/commands/`, or `.Codex/agents/`; writing a skill/command/agent description; a skill/command/agent reads vague, bloated, or is ignored when it should fire; or another skill needs the skill-craft vocabulary. Decides HOW WELL the artifact is written; defers the should-it-exist gate to `extending-safely`.
---

# Authoring Skills

A skill, command, or agent exists to wrangle **determinism** out of a stochastic model. **Predictability** — the agent taking the same *process* every run, not producing the same output — is the root virtue; every lever below serves it. (Craft lineage: Matt Pocock's `writing-great-skills`, adapted to this repo's conventions.)

Bold terms are defined in [GLOSSARY.md](GLOSSARY.md).

This skill owns the **craft** — how to write the file well. The **earn-your-place gate** (should this surface exist at all: the three-greps + named-justification acceptance test) belongs to **extending-safely**. Clear that gate first; then author to the standard here.

## Invocation — pick the load you pay

Every surface pays one of two loads:

- **Model-invoked** keeps a **description** in the window every turn (**context load**), so the agent fires it on its own and other skills can reach it.
- **User-invoked** (`disable-model-invocation: true`) strips the description from the agent's reach — zero context load, but it spends **cognitive load**: the owner is the index that must remember it exists.

Adapt to this repo: our **descriptions are triggers** and auto-invocation is a design goal (`SKILL-LIBRARY-BUILD-2026-07.md`, principle 4). A discipline that should fire on its own is **model-invoked** with a trigger-rich `Use when:`. Reserve **user-invoked** for pipeline commands the owner types by name (`/greenlight`, `/script`, `/thumbnail`). When user-invoked surfaces pile past memory, the cure is a **router** — `project-onboarding` is ours.

## Writing the description

The description earns harder pruning than the body — every word sits in context every turn.

- **Front-load the leading word** — the description is where it does its invocation work.
- **One trigger per branch.** Synonyms that rename a single branch are **duplication** ("build features test-first … wants red-green" is one branch twice). Collapse them.
- Keep the **`Use when:` clause** naming concrete trigger conditions — file paths, owner utterances, states. That is what auto-invocation matches on.
- **Cut identity already in the body.** Triggers plus any "when another skill needs…" reach clause; nothing else.

## Information hierarchy — how immediately the agent needs each piece

1. **In-skill step** — an ordered action in SKILL.md. Each ends on a **completion criterion**: make it *checkable* (can the agent tell done from not-done?) and *exhaustive* ("every modified surface accounted for", not "produce a list"). A vague criterion invites **premature completion**. Our stop-flags and gates *are* completion criteria.
2. **In-skill reference** — a rule or fact consulted on demand. A flat peer-set (all rules of a review on one rung) is fine, not a smell.
3. **External reference** — pushed to a sibling file behind a **context pointer**, loaded only when the pointer fires.

**Progressive disclosure** is the move down the ladder so the top stays legible. Repo caps: SKILL.md ≤ ~250 lines; disclose long material to a named sibling (`RESEARCH-LOOP.md`, `STOP-FLAGS.md`, `SCHEMAS.md`). The pointer's *wording*, not its target, decides how reliably the agent reaches it. **Co-locate** a concept's definition, rules, and caveats under one heading so reading one part brings its neighbours.

## Leading words — the highest-leverage lever

A **leading word** is a compact concept already in the model's pretraining that the agent thinks with while running the skill (Matt's: *tight*, *red*, *tracer bullet*, *fog of war*). Repeated, it accumulates a distributed definition and anchors a whole region of behaviour in the fewest tokens. It serves predictability twice: in the body it anchors *execution*; in the description — and when the same word lives in prompts, docs, and code — it anchors *invocation*, firing the skill more reliably.

This repo already coins strong ones — **use them, and promote buried ones to the front** where they do invocation work: *extend-don't-add*, *footnote-laundering*, *predicate drift*, *defer the dangerous writer*, *filters-not-predictors*, *tight loop*. Hunt restatements ("fast, deterministic, low-overhead" → *tight*) and collapse each to a single token. Assume every long file is carrying restatements a leading word retires — go find them.

## The six failure modes (diagnose a weak file)

- **Premature completion** — a step ends before it's genuinely done, attention slipping to *being done*. Defence, in order: sharpen the completion criterion (cheap, local); only if it stays fuzzy *and* you see the rush, hide the **post-completion steps** by splitting.
- **Duplication** — the same meaning in two places; costs maintenance, tokens, and inflates its rank on the ladder. Keep one **single source of truth**. Repo form: skills *route to* the authoritative ADR/REFERENCE/command, never **fork** its content (principle 1).
- **Sediment** — stale layers that settle because adding feels safe and removing feels risky. The default fate of any file without a pruning pass.
- **Sprawl** — too long even when every line is live. Cure with the ladder: disclose reference behind pointers, split by branch or sequence.
- **No-op** — a line the model already obeys by default, so you pay load to say nothing. The test: *does it change behaviour versus the default?* "Be thorough" is a no-op; the fix is a stronger word (*relentless*), not more words. Hunt them sentence-by-sentence and delete the whole sentence.
- **Negation** — steering by prohibition backfires: *don't think of an elephant* names the elephant. **Prompt the positive** — state the target so the banned move is never spoken. Keep a bare "never X" only as a guardrail you can't phrase positively, and pair it with what to do instead ("enrich `pattern()` and re-baseline" carries "never fork" for free).

## Repo conventions (author to these)

- **Audience = a cold Sonnet-class session** with only AGENTS.md + MEMORY.md loaded and no prior conversation. Every instruction must execute from a fresh prompt.
- **Every path and command must run.** Live-verify before shipping — a dead path is a lie the next session inherits (Wave-3 review caught a routine bug this way).
- **Skills route · commands do · agents return.** A skill points at the authoritative doc and says *when/why* to read it; a command is a task procedure; an agent carries the Return Contract.
- **Format exemplar: `historian/SKILL.md`** — stages table, hard rules, stop-flags, disclosed supplementary files.
- **Register on creation:** one-line entry in `.Codex/skills/README.md` + a AGENTS.md § Skill Library pointer; user-reachable commands also update the `project-onboarding` router.

## Authoring checklist

- [ ] Earn-your-place gate cleared (**extending-safely**) — this surface has a named justification, not "we needed somewhere to put it".
- [ ] Description front-loads the leading word, one trigger per branch, concrete `Use when:`.
- [ ] Every step ends on a checkable, exhaustive completion criterion.
- [ ] Long reference disclosed to a named sibling; SKILL.md ≤ ~250 lines.
- [ ] Restatements collapsed into leading words; buried coinages promoted to where they fire.
- [ ] No-op sentence-hunt done; prohibitions reworded to positives except load-bearing guardrails.
- [ ] Every path/command live-verified; README + AGENTS.md pointer added.

## Related skills

- **extending-safely** — the should-it-exist gate (three greps + named justification) that runs *before* this craft standard, plus seam-routing for code changes.
- **project-onboarding** — the repo's router; the model for curing cognitive load across many user-invoked surfaces.
