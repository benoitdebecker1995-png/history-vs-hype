---
name: Tool Discovery Before Proposing
description: Before proposing any new command, section, agent, or utility that does X, grep existing tooling for X. Don't duplicate.
type: feedback
originSessionId: acf6893b-dd34-4e58-89e9-9290f916aa55
---

# Tool Discovery Before Proposing

## The rule

Before proposing any new command, section, agent, or utility that does X, grep existing tooling for X. If existing tool covers it, defer/reference instead of duplicating.

## Why

2026-05-11 — while designing `/editing-guide`, proposed building "Section 6: Subtitle Correction" inside the command. User caught it: *"we have skill specifically for fixing subtitiles??"* The existing `/fix` command (with `auto_srt_fixer.py`, script-cross-reference, timestamp offset handling) was already doing exactly that. The proposed section would have duplicated 100% of `/fix`.

Cost of the miss: ~30% of unnecessary build time. Cost of preventing: two `Grep` calls (<5 seconds, <100 tokens).

Asymmetry strongly favors checking. Duplicate functionality is also a maintenance cost — two places to update when behavior changes.

## How to apply

**Triggers when:** about to propose NEW capability X (slash command, section inside a command, agent, utility, automation) that's plausibly already done. Fires especially in domains where tooling already exists (post-production, research, packaging, fact-checking, analytics).

**Action — three cheap searches before proposing:**

1. `Glob '.claude/commands/*.md'` then `Grep <X-keyword>` across the matches
2. `Glob '~/.claude/skills/**/*'` then `Grep <X-keyword>`
3. `Grep <X-keyword> .claude/REFERENCE/`

If existing tool covers it:
- Defer/reference in the new design (*"caption fixing → run `/fix` first"*)
- Don't duplicate the logic
- Don't even propose the section/subsection

If only adjacent tooling exists:
- Surface the adjacency in the plan (*"this overlaps with `/X`; differentiating because Y"*)
- Make the differentiation explicit

## Counter-examples (when NOT to fire)

- Implementing a one-off file write or read — not a "new capability"
- Writing a script for a specific project (not a reusable tool)
- Generating an analysis artifact (not adding to the channel's tool suite)

The rule is about **proposing new persistent capability X**, not every task.
