# _BACKLOG — Dormant / Parked Projects

Holding bucket **outside** the project lifecycle (`_IN_PRODUCTION/ → _READY_TO_FILM/ → _ARCHIVED/published/`).

**What lives here:** projects that are real but not actively being worked — research stubs, stalled drafts, dead duplicates. Parked so `_IN_PRODUCTION/` shows only what's live.

**Why it's safe:** the scanners (`tools/hooks/session_context.py`, `tools/dashboard/project_scanner.py`, `tools/reconcile/reconcile.py`) all glob only the 3 lifecycle folders, so `_BACKLOG/` is invisible to dashboards, session-start surfacing, and reconcile. Nothing here is deleted — it's just out of the way.

**To resume a project:** `git mv video-projects/_BACKLOG/<folder> video-projects/_IN_PRODUCTION/<folder>` and run `/reconcile`.

**Do NOT put here:** published videos (→ `_ARCHIVED/published/`) or filmed/script-locked work headed to upload (→ `_READY_TO_FILM/`).

---

Populated 2026-06-03 from a backlog triage: 23 dormant folders moved out of `_IN_PRODUCTION/` (which had accumulated 27 folders, only 3 active). Includes confirmed dead duplicates (#23 christmas → dup of published #18; #42 brazil → dup of published #41) and false-positive "post-publish" stubs (#12 guatemala, #25 iran — their POST-PUBLISH-ANALYSIS.md files are cross-links, NOT proof of publish; both unpublished). See `tools/reconcile/manual-matches.json` notes.
