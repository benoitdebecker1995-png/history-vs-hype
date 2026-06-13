# Routine 4 — Daily Stale Project Nudge

**Purpose:** Every morning, scan `_IN_PRODUCTION/` for projects untouched more than 7 days. Surfaces the exact next action for each stale project so the morning session has a clear starting point.

> **▶ EXECUTION DIRECTIVE (you are being run headless via `claude -p` — the routine path):** You ARE the stale-project-nudge routine. Execute the STEP block below **right now** against this repo at `D:\History vs Hype` — do not treat it as a template to describe. The `## Setup`/`## Guardrails` sections are reference; honor the guardrails but don't act on Setup. If nothing is stale and `.brain/index.md` §3 is current, exit silently (correct success). Do NOT respond with "what would you like to work on?" — your task is the steps below.

**Schedule:** Daily, 09:00 local (Desktop scheduled task — after channel health)
**Why Desktop:** Reads local `video-projects/_IN_PRODUCTION/` mtimes and PROJECT-STATUS.md files.
**Expected cost:** 1 of the 5 daily Routines credits.

---

## Paste this into Desktop Scheduled Task (prompt field)

```
You are operating inside the History vs Hype repository at D:\History vs Hype.

STEP 1 — Scan all projects in video-projects/_IN_PRODUCTION/ for staleness:

  python -c "
  import os, json
  from datetime import datetime, timedelta
  from pathlib import Path

  cutoff = datetime.now() - timedelta(days=7)
  projects = []
  base = Path('video-projects/_IN_PRODUCTION')
  for folder in sorted(base.iterdir()):
      if not folder.is_dir(): continue
      mtime = max(
          (f.stat().st_mtime for f in folder.rglob('*') if f.is_file()),
          default=0
      )
      last_touched = datetime.fromtimestamp(mtime)
      days_stale = (datetime.now() - last_touched).days
      projects.append({'slug': folder.name, 'days_stale': days_stale, 'last_touched': last_touched.strftime('%Y-%m-%d')})
  print(json.dumps([p for p in projects if p['days_stale'] >= 7], indent=2))
  "

STEP 2 — For each stale project, read its PROJECT-STATUS.md and identify:
  - Current lifecycle stage (Research / Script / Fact-check / Ready to film / Filming / Post)
  - Blocking issue (if any)
  - Next concrete action

STEP 3 — If NO projects are stale AND .brain/index.md §3 (Active topics) is already current:
  Exit silently. Write nothing.

STEP 4 — If any projects are stale: write .brain/_inbox/stale-projects-YYYY-MM-DD.md with:

  # Stale Projects — YYYY-MM-DD

  ## [project-slug] — [N] days untouched

  **Stage:** [Research / Script / Fact-check / Ready to film]
  **Last touched:** [YYYY-MM-DD]
  **Blocking issue:** [from PROJECT-STATUS.md, or "none identified"]
  **Next action:** [specific, single step]
  **Estimated time:** [30 min / 2h / half-day]

  [Repeat for each stale project]

STEP 5 — Refresh .brain/index.md §3 (Active topics table):
  Update the "Last touched" column and "Stage" for each project in the table.
  Only edit the rows in the Active topics section — do NOT touch other sections.

STEP 6 — Stop. Do not edit PROJECT-STATUS.md or any project file.
Only allowed writes: .brain/_inbox/stale-projects-YYYY-MM-DD.md and .brain/index.md §3.
```

---

## Setup (Windows Task Scheduler)

```powershell
$action = New-ScheduledTaskAction -Execute "claude" -Argument "--print `"$(Get-Content .claude\routines\stale-project-nudge.md -Raw)`"" -WorkingDirectory "D:\History vs Hype"
$trigger = New-ScheduledTaskTrigger -Daily -At "09:00"
Register-ScheduledTask -TaskName "HvH-StaleProjects" -Action $action -Trigger $trigger -RunLevel Highest
```

## Guardrails
- **Never** edit `PROJECT-STATUS.md`, scripts, or research files.
- **Never** push to git — local alert only.
- Only writes: `.brain/_inbox/stale-projects-YYYY-MM-DD.md` and `.brain/index.md` §3 rows.
- If `_IN_PRODUCTION/` is empty: exit silently.

## Interpreting results
- **0 stale projects (typical):** Silent — no file written, index updated in place.
- **1+ stale projects:** File written with specific next action. Review during morning session.
- **Project stale > 21 days:** Consider moving to `_ARCHIVED/` or escalating priority.
