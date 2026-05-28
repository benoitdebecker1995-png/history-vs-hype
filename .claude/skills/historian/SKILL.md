---
name: historian
description: Historian-mode research discipline for the History vs Hype channel. Enforces three hard rules and three stop-flags during active historical research. Use when: querying a NotebookLM notebook, working in `_IN_PRODUCTION/` project folders, reading or editing `01-VERIFIED-RESEARCH.md`, running any `/research` subcommand, or whenever Claude is acting as a historical researcher (filing claims, building source lists, adding content to verified research). DORMANT during project mechanics (Step 0: demand gate, folder creation, title pre-gen).
---

# Historian Mode

## Historian Stages

| Stage | Name | Trigger |
|---|---|---|
| 0 | Project Setup | Folder creation, demand gate, title pre-gen — **skill dormant** |
| A | Historiographical Baseline | Wiki brief → preliminary research → viability gate → competitor gap |
| B | Source Criticism | NLM source list → provenance check → user notebook upload |
| C | Corroboration | NLM ingestion → claim verification → mechanism-word lock → angle-discovery |

Stages sit *inside* channel Phase 1 (Research). Channel Phases (Research/Script/Fact-check) are separate and unchanged.

## Three Hard Rules

**Rule 1 — NLM-anchor:** Every verbatim quote filed in `01-VERIFIED-RESEARCH.md` MUST carry an NLM source ID. No exceptions. Violation fires `[FLAG: NEED SOURCES]` or `[FLAG: LIBRARY ACQUISITION]`. See [WEB-POLICY.md](WEB-POLICY.md).

**Rule 2 — Tier-discipline:** Every claim must carry [P]/[S]/[S→P] tier + T1/T2/T3 tier-vibe. Single-source claims and [S]-tagged on-screen claims fire a flag. If a named acquisition target exists → `[FLAG: LIBRARY ACQUISITION]`. If no target → `[FLAG: NEED SOURCES]`.

**Rule 3 — Fork-detection:** When two NLM-grounded scholars interpret the same evidence differently AND the framing affects script tone or thesis direction, halt immediately. Fire `[FLAG: DIRECTION NEEDED]` and present both framings to the user.

## Stop Flags

| Flag | Fires when | Spec |
|---|---|---|
| `[FLAG: NEED SOURCES]` | Verbatim quote has no NLM anchor + no known acquisition target; or single-source [S] on-screen claim | [STOP-FLAGS.md](STOP-FLAGS.md) |
| `[FLAG: LIBRARY ACQUISITION]` | Verbatim quote has no NLM anchor but a specific named source would close the gap | [STOP-FLAGS.md](STOP-FLAGS.md) |
| `[FLAG: DIRECTION NEEDED]` | Two NLM-grounded scholars diverge on framing that affects script tone or thesis | [STOP-FLAGS.md](STOP-FLAGS.md) |

**When a flag fires:** state the flag text, explain why it fired, halt research output, and wait for user direction. Do NOT continue filing claims past an unresolved flag.

## Stage Transitions

Surface conversationally at natural moments: *"Stage A complete — ready for Stage B?"*

On user confirm, append a `## Historian Stage State` section to `PROJECT-STATUS.md` **below the `<!-- /AUTO:reconcile -->` marker** (not inside the AUTO block). See [STAGE-AUDITS.md](STAGE-AUDITS.md) for pre-transition checklists.

```
## Historian Stage State
**Current stage:** Stage [X] — [Name] (locked [YYYY-MM-DD])
**Next stage:** Stage [Y] — [Name]
**Outstanding flags:** [None / list of unresolved flags]
**Stage A locked:** [date or "pending"]
**Stage B locked:** [date or "pending"]
**Stage C locked:** [date or "pending"]
```

## Migration (existing projects)

For `/research --existing` on projects without stage markers, infer from artifacts:

| Evidence | Inferred stage |
|---|---|
| 20+ ✅ claims in `01-VERIFIED-RESEARCH.md` + notebook ID present | Stage C |
| `00-NOTEBOOKLM-SOURCE-LIST.md` + NLM notebook populated + <5 ✅ claims | Stage B |
| `_research/00-PRELIMINARY-BRIEF.md` exists + no NLM notebook | Stage A |

Surface inference: *"I infer Stage C based on [evidence]. Confirm?"* Write Stage State section only after user confirms.

## Supplementary Files

- [STOP-FLAGS.md](STOP-FLAGS.md) — full spec + Piri Reis examples for all three flags
- [STAGE-AUDITS.md](STAGE-AUDITS.md) — stage-boundary audit checklists
- [WEB-POLICY.md](WEB-POLICY.md) — verbatim/paraphrase policy with worked examples
