---
description: Reconcile project state — folder lifecycle, AUTO blocks, derived docs. Auto-fires when user says "I uploaded/released/published X".
model: sonnet
---

# /reconcile — Project State Reconciler

Owns folder moves between `_IN_PRODUCTION/` → `_READY_TO_FILM/` → `_ARCHIVED/published/`, the `<!-- AUTO:reconcile -->` block at the top of each per-folder `PROJECT-STATUS.md`, and regeneration of root overview docs. Truth sources: filesystem (lifecycle stage) + `tools/youtube_analytics/analytics.db` (publish status) + in-folder narrative (hand-written).

## Conversational trigger

When the user says any of:
- *"I uploaded X"* / *"I released X"* / *"I published X"*
- *"X went up"* / *"X is live"*

...where X is a project name/slug/URL, run `/reconcile <X>` automatically. If X is ambiguous (multiple folders could match), ask once: "Which project — #54 Inquisition or #X?" Resolution is the only place Claude pauses.

## Modes

```
/reconcile                       Full scan, propose all changes, user approves
/reconcile <slug>                Single project (substring match against folder names)
/reconcile --dry-run             Show proposed diff; apply nothing
/reconcile --migrate             First-run retro: extra surface area for unmatched folders
/reconcile --undo                Reverse the latest reconcile run (folder moves + file restores)
/reconcile --auto-publish-only   Routine 6 mode. Archives YouTube-confirmed publishes only.
                                 NEVER touches memory snapshots or MEMORY.md.
```

## Run it

```bash
python -m tools.reconcile.reconcile [args]
```

The script reads `tools/youtube_analytics/analytics.db` (refreshed daily by Routine 3 at 08:00) as the truth source for publish status. No direct YouTube API calls.

## Output

- Folder moves visible via `git status` (use `git mv` semantics — Python's `shutil.move` preserves history when staged).
- Per-folder `PROJECT-STATUS.md` gets/updates an `<!-- AUTO:reconcile -->` block at the top. Narrative below `<!-- /AUTO:reconcile -->` is preserved verbatim.
- Root `video-projects/PROJECT_STATUS.md` and `PROJECT_REGISTRY.md` regenerated from filesystem + analytics.db.
- `.brain/index.md §3 Active Topics` refreshed (Routine 4 still updates this independently for stale-nag purposes).
- Reversible diff log written to `.brain/_inbox/reconcile-YYYY-MM-DD-HHMM.diff` with `.pre-diff` backups beside each edited file.

## Matching strategy (folder ↔ video)

Three tiers, in priority order:

1. **Manual override** — `tools/reconcile/manual-matches.json` (folder_name → video_id). Wins over everything. Used to handle the gray zone of folders whose slug doesn't fuzzy-match the published title.
2. **Tier 1 deterministic** — scan folder's `PROJECT-STATUS.md` / `YOUTUBE-METADATA.md` / `POST-PUBLISH-ANALYSIS.md` for an 11-char Video ID that matches `analytics.db`. Score 1.0.
3. **Tier 2 fuzzy** — token-overlap between folder slug and video title. Score 0.0–1.0.
   - ≥0.85 → auto-propose match
   - 0.5–0.85 → gray zone, surfaced for user review (no auto-archive)
   - <0.5 → no match, folder stays put

## Memory snapshot handling

**Interactive mode** (`/reconcile` with no auto flag): when archiving a project, prompts "Any lessons to promote to `feedback-*.md` before deleting memory snapshot?" Pauses for user; deletes `memory/[N]-production-state.md` + removes its MEMORY.md index line after.

**`--auto-publish-only`** (Routine 6): NEVER touches memory snapshots or MEMORY.md. Logs: "snapshot for #X still active — run /reconcile to promote lessons + delete." Next interactive run cleans up.

## Manual override file

`tools/reconcile/manual-matches.json` — JSON dict mapping folder names to video IDs. Used during retro migration to nail down folders where Tier 1 + Tier 2 both miss.

```json
{
  "40-berlin-conference-1884-2026": "WgE2FLsDhfk",
  "45-manhattan-purchase-myth-2026": "mg6ujk6rDVE"
}
```

## Reference

- Plan: `C:\Users\Benoi\.claude\plans\drifting-folders-reconcile.md`
- Core script: `tools/reconcile/reconcile.py`
- Matcher: `tools/reconcile/match.py`
- Routine 6: `.claude/routines/reconcile-daily.md`
- Behavioral rule: `memory/feedback-project-reconciliation.md`
