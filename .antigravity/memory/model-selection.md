---
name: Model selection cheat-sheet
description: Which Claude/Gemini model fits which task — surface before starting work
type: reference
originSessionId: 9e7ffb50-9cb0-4b82-ba34-f9d2180f1da2
---
# Model selection by task

| Task | Model | Why |
|---|---|---|
| Script polish / locking pass | Opus | Catches subtle category slips, factual looseness that Sonnet misses |
| Iterative drafting / mid-process flag-and-discuss | Sonnet | Fast, cheap, catches obvious cadence/transition issues |
| Newsletter writing | Opus | High-stakes prose, voice consistency matters |
| Article-writer agent (CONVERT/WRITE/EDIT) | Opus | Already set in agent frontmatter |
| script-writer-v2 agent | Opus | Already set in agent frontmatter |
| Bulk Wikipedia / source reads | Gemini Flash | Locked rule per `feedback-gemini-model-default.md` |
| Quick lookups / file searches / git status | Haiku/Sonnet default | No need for Opus depth |
| Verification against specific sources | NotebookLM | Source-grounded, prevents general-LLM drift |
| Code research / debugging exploration | Sonnet for routine, Opus for hard | Pick by depth needed |

## Behavioral rule (added 2026-05-08)

When starting a task with a clear best-fit model that differs from the current model, recommend it in one sentence before beginning. Let user override.

Example: if user starts a script polish session in Sonnet, lead with: "Final polish lands harder in Opus — switch?" Don't pre-empt every task; only when the difference is meaningful.

## Source

Video #54 Spanish Inquisition session (2026-05-08): user demonstrated dual-pass benefit. Sonnet caught 8 obvious flags fast; Opus caught 4 additional flags Sonnet missed (category slip in §6, factual looseness in §7 close, three-sentence Hassner intro tightening, pre-frame redundancy detection). Locked the principle: Opus for final polish pass, Sonnet for iteration.

User's underlying ask: "i dont know which model to use for which task... but preferably it would either do it automatically or tell me before starting a task what model is best."
