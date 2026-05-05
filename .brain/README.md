# .brain — Project knowledge root

This directory is the **additive extension** of the History vs Hype knowledge base. It does NOT replace existing brain roots — it adds what they don't cover and indexes everything.

## What lives here

| Dir | Purpose |
|-----|---------|
| `index.md` | Godlike multi-root catalog — start here every session |
| `_inbox/` | Routine output landing zone (Cloud + Desktop tasks write dated files here) |
| `_queue/` | Paste-and-forget raw items awaiting ingestion |
| `sources/` | Verified quotes by book, project-scoped (extends `~/llm-brain/wiki/quotes/`) |
| `threads/` | Cross-source synthesis narratives |
| `methodology/` | Decision docs: model routing, Gemini handoff, brain map |

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
- This README is MANUAL — update only when the structure changes
