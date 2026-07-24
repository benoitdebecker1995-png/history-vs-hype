# .brain — Project knowledge root

This directory is the **additive extension** of the History vs Hype knowledge base. It does NOT replace existing brain roots — it adds what they don't cover and indexes everything.

## What lives here

| Dir | Purpose |
|-----|---------|
| `index.md` | Godlike multi-root catalog — start here every session |
| `_inbox/` | Routine output landing zone (Cloud + Desktop tasks write dated files here) |
| `_queue/` | Paste-and-forget raw items awaiting ingestion |
| `topics/` | **Topic notes** — verified claims re-filed by CONCEPT. *Derived, never hand-edited.* |
| `sources/` | **Source notes** — one per book/paper/document: what it is cited for, across every episode. *Derived.* |
| `threads/` | **Argument notes** — our own synthesis, questions, speculation. *Hand-written.* |
| `methodology/` | Decision docs: model routing, Gemini handoff, brain map |

### The three note types

Research is filed per VIDEO in `01-VERIFIED-RESEARCH.md`, which means it stops
compounding the moment an episode ships. `topics/` re-files the same verified
claims by concept so episode N+1 is cheaper than episode N. Three layers, one
rule each:

- **`sources/`** — what someone *else* said. Immutable.
- **`topics/`** — claims extracted from those sources, grouped by concept, each
  carrying its attribution and the episode that verified it. Our interpretation,
  never our speculation.
- **`threads/`** — what *we* say. Pure synthesis. This is the only one you write
  by hand.

Keeping speculation physically separate from extracted claims is the point: a
topic note can be reused in a script without re-checking whose idea it was.

## What lives ELSEWHERE (do not duplicate)

| Root | What it owns |
|------|-------------|
| `channel-data/` | Channel analytics, competitor tracking, CTR baselines, POST-PUBLISH-ANALYSIS, topic pipeline |
| `tools/benchmark/` | Title/thumbnail/hook playbooks, WAVE analyses, outlier corpus |
| `~/llm-brain/wiki/` | Cross-project methodology, entities, concepts, quotes by source |
| `~/.claude/projects/D--History-vs-Hype/memory/` | User behavior rules, feedback, channel stats, workflow notes |
| `.claude/REFERENCE/` | Claude-instruction files (prompts, writing voice, templates) — NOT knowledge |

## Maintenance contract

- `.brain/index.md` AUTO sections updated nightly by Routine 5 (Desktop scheduled task)
- `.brain/_inbox/` files reviewed by user, never auto-deleted
- `.brain/_queue/` consumed by Routine 5 — drop raw content here, it gets processed
- `.brain/topics/` + `.brain/sources/` are **fully regenerated** by
  `python -m tools.brain.topic_mine build`. Stale notes are deleted on each run,
  so an edit made directly in those folders is lost on the next build. Fix the
  upstream `01-VERIFIED-RESEARCH.md` and re-mine instead. See ADR-0016.
- `.brain/topics/_taxonomy.json` is the one file in `topics/` that IS hand-written
  — it folds raw extraction slugs into canonical concepts. Topics missing from it
  render as `status: provisional`.
- This README is MANUAL — update only when the structure changes
