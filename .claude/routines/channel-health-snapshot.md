# Routine 3 — Daily Channel Health Snapshot

**Purpose:** Each morning, check last 7 days of analytics against 30-day baseline. Only surfaces anomalies — silent if everything is normal. Catches tanking videos on day 2, not day 7.

**Schedule:** Daily, 08:00 local (Desktop scheduled task)
**Why Desktop:** Requires `analytics.db` (local-only, not in repo).
**Expected cost:** 1 of the 5 daily Routines credits.

---

## Paste this into Desktop Scheduled Task (prompt field)

```
You are operating inside the History vs Hype repository at D:\History vs Hype.

STEP 1 — Read channel baseline from channel-data/stats.md.
Extract the 30-day baseline values for: CTR, AVD (average view duration), week-1 retention %.

STEP 2 — Query last 7 days from analytics.db:

  python -c "
  import sqlite3, json
  from datetime import datetime, timedelta
  conn = sqlite3.connect('analytics.db')
  cutoff = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
  rows = conn.execute('''
    SELECT video_id, title, date, views, ctr, avd_seconds, retention_pct
    FROM video_stats
    WHERE date >= ?
    ORDER BY date DESC
  ''', (cutoff,)).fetchall()
  print(json.dumps(rows, default=str))
  conn.close()
  "

STEP 3 — Compare against baseline. Flag ONLY if ANY of:
  - CTR deviates more than 1.5 standard deviations from 30-day baseline
  - AVD deviates more than 1.5 standard deviations from 30-day baseline
  - Week-1 retention for any video < 22%
  - Any video showing >30% view velocity drop day-over-day for 3+ consecutive days

STEP 4 — If NO anomalies: exit silently. Write nothing. Do not commit.

STEP 5 — If anomalies found: write .brain/_inbox/channel-health-YYYY-MM-DD.md with:

  # Channel Health Alert — YYYY-MM-DD

  **Anomalies detected:** [N]

  ## [Video title]
  **Metric:** [CTR / AVD / Retention / Velocity]
  **Baseline:** [X]
  **Actual:** [Y] ([+/-Z]% deviation, [N]σ)
  **Action options:**
  1. Retitle: run /retitle for this video
  2. Rethumb: open YouTube Studio > Custom Thumbnail
  3. Monitor: check again in 48h if deviation < 2σ

STEP 6 — Stop. Do not edit any video project files. Do not push to git.
This is a local-only alert file.
```

---

## Setup (Windows Task Scheduler)

```powershell
# Run once to register the scheduled task
$action = New-ScheduledTaskAction -Execute "claude" -Argument "--print `"$(Get-Content .claude\routines\channel-health-snapshot.md -Raw)`"" -WorkingDirectory "D:\History vs Hype"
$trigger = New-ScheduledTaskTrigger -Daily -At "08:00"
Register-ScheduledTask -TaskName "HvH-ChannelHealth" -Action $action -Trigger $trigger -RunLevel Highest
```

## Guardrails
- **Never** edit video project files.
- **Never** push to git — local alert only.
- Output ONLY to `.brain/_inbox/channel-health-YYYY-MM-DD.md`.
- If `analytics.db` not found: exit silently (database may be on a different drive).

## Interpreting results
- **0 anomalies (typical):** Silent — no file written.
- **CTR < 2%:** Consider retitle via `/retitle`.
- **Retention < 22% week 1:** Critical — rethumb before day 7.
- **Velocity drop 3+ days:** Video likely buried by algorithm — consider repost or boost.
