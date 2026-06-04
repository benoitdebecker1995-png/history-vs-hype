---
name: Project State Reconciliation
description: "I uploaded X" auto-triggers /reconcile X. Folder lifecycle, AUTO blocks, memory snapshots — automated reconciliation pipeline replacing the old "drift is accepted" framing.
type: feedback
originSessionId: a8e4b793-43f0-4204-8b3b-d4d1e4074bff
---
# Project State Reconciliation

When the user says "I uploaded X" / "I released X" / "I published X" / "X is live" / "X went up" — run `/reconcile <X>` immediately. The utterance IS the write trigger.

**Why:** Project file drift used to be treated as accepted reality in `workflow-observations.md` (lines 11-15). The user clarified during the 2026-05-12 grill: drift is a bug, not a feature. State files going stale (PROJECT-STATUS.md, memory snapshots, root PROJECT_STATUS.md, folder location) was the loudest failure of the workflow. The fix is to (a) make filesystem + analytics.db canonical for state, (b) auto-regenerate derived docs, (c) move folders on publish.

**How to apply:**

- **Conversational trigger.** When ANY publish-related utterance arrives, parse the project reference (slug, topic name, URL, video ID) and run `/reconcile <ref>`. If ambiguous, ask ONCE which project before proceeding. The phrase covers "uploaded", "released", "published", "is live", "went up".
- **Do NOT just look up the video.** Do NOT acknowledge and ask the user to update files. Do NOT assume `_IN_PRODUCTION/X/PROJECT-STATUS.md` is current. The reconcile DOES the work.
- **Do NOT use the old "check YouTube API" pattern from `workflow-observations.md`.** That framing is superseded.
- **Truth sources:** filesystem → lifecycle stage; `tools/youtube_analytics/analytics.db` → publish status; in-folder PROJECT-STATUS.md narrative (below `<!-- /AUTO:reconcile -->`) → hand-written.
- **Folder lifecycle:** `_IN_PRODUCTION/` (pre-script) → `_READY_TO_FILM/` (script-locked OR filmed OR in-post, pre-publish) → `_ARCHIVED/published/` (YouTube confirmed).
- **AUTO block convention:** every per-folder `PROJECT-STATUS.md` has a `<!-- AUTO:reconcile -->` block at the top with stable fields (Status, Lifecycle, Video ID, Published date, Last reconciled). Narrative below `<!-- /AUTO:reconcile -->` is hand-written and preserved verbatim across reconcile runs.
- **Memory snapshots** (`memory/[N]-production-state.md`): frozen point-in-time snapshots during active project life. Append new dated entries when state changes mid-project; do NOT overwrite prior claims. On archive (interactive `/reconcile` only — Routine 6 doesn't touch them), user is prompted to promote lessons to `feedback-*.md` files before snapshot is deleted + MEMORY.md index line removed.
- **Backstop:** Routine 6 runs daily 08:30, auto-archives any new YouTube publishes (high-confidence match only). It never moves folders into _READY_TO_FILM (script-lock / filming transitions stay manual). It never touches memory snapshots. Stale `analytics.db` (>36h) trips a fail-loud alert in `.brain/_inbox/`.
- **Undo:** every `/reconcile` run writes a reversible `.diff` log with `.pre-diff` file backups. `/reconcile --undo` reverses the latest run.
- **Matching tiers:** manual override (`tools/reconcile/manual-matches.json`) → Tier 1 deterministic (Video ID extracted from folder files + validated against analytics.db) → Tier 2 fuzzy (token overlap ≥0.85 auto, 0.5-0.85 gray-zone user pick, <0.5 leave folder).

**Origin:** 2026-05-12 grill on the drift problem. Two-pass design surfaced the asymmetric handling needed (interactive vs Routine 6) and the matching difficulty (~13 published videos had no slug-title token overlap, requiring manual-matches.json bootstrap). Implementation: `tools/reconcile/`, `.claude/commands/reconcile.md`, `.claude/routines/reconcile-daily.md`. Plan: `~/.claude/plans/drifting-folders-reconcile.md`.
