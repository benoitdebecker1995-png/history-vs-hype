# Skill-Craft Glossary

Vocabulary for reasoning about instruction surfaces (skills, commands, agents). Disclosed from `authoring-skills/SKILL.md` so the top stays legible. Terms adapted from Matt Pocock's `writing-great-skills`; repo-specific terms marked **(HvH)**.

## Root

- **Determinism** — the property a skill imports into a stochastic model: a fixed *process*, not a fixed output.
- **Predictability** — the root virtue. The agent takes the same process every run. Every lever below serves it.

## Invocation

- **Model-invoked** — the description stays in the agent's reach; the agent fires the skill on its own and other skills can reach it. Pays **context load**.
- **User-invoked** — `disable-model-invocation: true`; only the owner, typing the name, can invoke it. Pays **cognitive load**.
- **Context load** — the always-present cost of a description sitting in the window every turn.
- **Cognitive load** — the human cost of having to remember a user-invoked surface exists.
- **Router** — one user-invoked surface that names the others and when to reach for each; cures piled-up cognitive load. **(HvH)** ours is `project-onboarding`.
- **Descriptions-are-triggers (HvH)** — house design goal: a description's job is to make auto-invocation fire, so it is written as concrete trigger conditions, not a summary.

## The description

- **Description** — frontmatter line doing two jobs: state what the surface is, and list the branches that trigger it.
- **Branch** — a distinct path through the skill; each earns its own trigger. Different runs take different branches.
- **Trigger** — a concrete condition (file path, owner utterance, state) that should fire the skill. Collected in the **`Use when:`** clause.

## Information hierarchy

- **Information hierarchy** — the ladder ranking material by how immediately the agent needs it: step → in-skill reference → external reference.
- **Step** — an ordered action in SKILL.md; the primary tier.
- **Completion criterion** — the condition that tells the agent a step is done. Must be *checkable* and, where it matters, *exhaustive*. **(HvH)** stop-flags and gates are completion criteria.
- **Reference** — a definition, rule, or fact consulted on demand. May be a flat peer-set (all rules on one rung) — fine, not a smell.
- **Context pointer** — the link that reaches an external file; its *wording* decides how reliably the agent follows it.
- **Progressive disclosure** — moving material down the ladder into a linked sibling file so the top stays legible. **(HvH)** cap SKILL.md ≤ ~250 lines.
- **Co-location** — keeping a concept's definition, rules, and caveats under one heading so reading one part brings its neighbours.

## Granularity

- **Granularity** — how finely skills are divided. Each cut spends one of the two loads, so split only when the cut earns it.
- **Split by invocation** — break off a model-invoked skill when a distinct leading word should trigger it, or another skill must reach it.
- **Split by sequence** — hide **post-completion steps** so their pull doesn't make the agent rush the current one.
- **Post-completion steps** — steps still ahead that tempt premature completion of the step in front.
- **Legwork** — the digging the agent does within the work; a demanding completion criterion drives more of it.

## Leading words

- **Leading word** — a compact concept already in the model's pretraining that the agent thinks with while running the skill (*tight*, *red*, *tracer bullet*). Anchors a region of behaviour in the fewest tokens; anchors execution in the body and invocation in the description.
- **HvH-coined leading words** — *extend-don't-add*, *footnote-laundering*, *predicate drift*, *defer the dangerous writer*, *filters-not-predictors*, *auditor's edge*. Promote them to where they fire.

## Pruning

- **Single source of truth** — one authoritative place for each meaning, so changing behaviour is a one-place edit.
- **Route-not-fork (HvH)** — a skill points at the authoritative ADR/REFERENCE/command and says when/why to read it; it never copies that content.
- **Relevance** — does a line still bear on what the skill does?
- **No-op** — a line the model already obeys by default. Test: does it change behaviour versus the default? Hunt sentence-by-sentence.

## Failure modes

- **Premature completion** — ending a step before it's done, attention slipping to being done.
- **Duplication** — the same meaning in more than one place.
- **Sediment** — stale layers that settle because adding feels safe and removing feels risky.
- **Sprawl** — too long even when every line is live and unique.
- **Negation** — steering by prohibition, which backfires (*don't think of an elephant*). Fix by prompting the **positive**.

## Repo gates

- **Earn-your-place gate (HvH)** — the extend-don't-add acceptance test (three greps + named justification) owned by `extending-safely`; runs *before* this craft standard.
- **Cold-Sonnet audience (HvH)** — the assumed reader: a fresh Sonnet-class session with only CLAUDE.md + MEMORY.md loaded.
