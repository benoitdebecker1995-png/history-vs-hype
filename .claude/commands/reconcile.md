---
description: Reconcile project state — folder lifecycle, AUTO blocks, derived docs. Auto-fires when user says "I uploaded/released/published X".
model: opus
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

## Lifecycle-Transition Snapshot Refresh

> See `memory/feedback-project-reconciliation.md` for the broader reconcile lifecycle rule and the Hijab #52 stale-snapshot origin.

When `/reconcile` moves a project across a lifecycle boundary (`_IN_PRODUCTION/` → `_READY_TO_FILM/`, or `_READY_TO_FILM/` → `_ARCHIVED/published/`), run this snapshot check before any other per-project prompt (including the lessons-promotion prompt at archive time).

### Trigger condition

Any cross-folder move detected during the current reconcile run.

### Snapshot detection

Check whether a per-project memory snapshot exists at:

```
C:\Users\Benoi\.claude\projects\D--History-vs-Hype\memory\<NN>-<slug>-production-state.md
```

Pattern: `<number>-<slug>-production-state.md`. Use Glob to locate it.

### If snapshot exists

Fire an `AskUserQuestion` with this prompt:

> "Memory snapshot `<NN>-<slug>-production-state.md` was last substantively updated on `<date>`, which predates the current lifecycle transition (`<from>` → `<to>`). The snapshot may contain stale state — old titles, old thumbnail concepts, old folder paths. How should this be handled?"

Options:
- **Refresh inline** — Open the snapshot, update fields known to have changed (current folder location, locked title, locked thumbnail concept, locked thesis). Save with new dated entry appended.
- **Mark stale, defer refresh** — Append a `> STALE AS OF <date> — superseded by <transition>` block at the top of the snapshot. Future sessions will see the stale-flag and re-derive from current files.
- **Accept as-is** — User explicitly judges the snapshot is still current despite the transition. Append a `> CONFIRMED CURRENT AT <date>` block at the top.

### If snapshot does NOT exist

Skip the prompt. No-op.

### Ordering at archive transition

When moving `_READY_TO_FILM/` → `_ARCHIVED/published/`: the snapshot-refresh prompt fires **first**, then the existing lessons-promotion prompt (see `## Memory snapshot handling` above). Refresh-or-mark-stale is the precondition for lessons-promotion + snapshot deletion.

### Research-graph staleness marker

After any archive-direction move (`_READY_TO_FILM/` → `_ARCHIVED/published/`), touch `graphify-out/research/.needs_refresh` and write the newly-archived slug into it (one per line, append). This signals that `RESEARCH-GRAPH.json` and the research graph (`graphify-out/research/graph.json` + viz) are behind by N videos.

```powershell
$marker = 'graphify-out\research\.needs_refresh'
Add-Content -Path $marker -Value '<newly-archived-slug>'
```

Do NOT auto-rebuild the research graph inside `/reconcile` — it costs a Gemini Flash call. The user runs `python tools/refresh-research-graph.py` when they want a refresh (see that script for the one-shot pipeline). The marker is purely a visibility signal — `/status` and future Claude sessions can read it to surface "research graph is N videos behind."

---

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
