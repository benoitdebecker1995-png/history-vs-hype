# Routine 3 — Daily Channel Health Snapshot

**Purpose:** Each morning, check last 7 days of analytics against 30-day baseline. Only surfaces anomalies — silent if everything is normal. Catches tanking videos on day 2, not day 7.

**Schedule:** Daily, 08:00 local (Desktop scheduled task) — after Routine 7 (`HvH-GrowthRefresh`, 07:45) refreshes `analytics.db`, so this reads fresh metrics.
**Why Desktop:** Reads the local `tools/youtube_analytics/analytics.db` (the local copy is the freshest; the committed copy lags). **This routine only READS — it does NOT refresh the DB.** The refresh is Routine 7 (`growth_data --refresh`).
**Expected cost:** 1 of the 5 daily Routines credits.

---

## Paste this into Desktop Scheduled Task (prompt field)

```
You are operating inside the History vs Hype repository at D:\History vs Hype.

STEP 1 — Read channel baseline from channel-data/stats.md.
Extract the 30-day baseline values for: CTR, AVD (average view duration), week-1 retention %.

STEP 2 — Query recent videos' current metrics from analytics.db.
The DB lives at `tools/youtube_analytics/analytics.db` (NOT repo root). The table is
`videos` — one row per video holding its current-snapshot metrics (there is no
per-video per-day history table; `daily_channel` is channel-level only):

  python -c "
  import sqlite3, json
  from datetime import datetime, timedelta, timezone
  conn = sqlite3.connect('tools/youtube_analytics/analytics.db')
  cutoff = (datetime.now(timezone.utc) - timedelta(days=30)).strftime('%Y-%m-%dT%H:%M:%SZ')
  rows = conn.execute('''
    SELECT video_id, title, published_at, views,
           ctr_percent, avg_view_duration_seconds, avg_view_percentage
    FROM videos
    WHERE published_at >= ?
    ORDER BY published_at DESC
  ''', (cutoff,)).fetchall()
  print(json.dumps(rows, default=str))
  conn.close()
  "

(30-day window because the channel publishes ~weekly — a 7-day window often returns 0 rows.
`avg_view_percentage` is the week-1 retention proxy; `ctr_percent` may be NULL because CTR
comes from the Reporting API via `ctr_tracker`, not the Analytics API — skip NULLs, don't flag them.)

STEP 3 — Compare against baseline. Flag ONLY if ANY of:
  - CTR (`ctr_percent`) deviates more than 1.5 standard deviations from 30-day baseline (skip if NULL)
  - AVD (`avg_view_duration_seconds`) deviates more than 1.5 standard deviations from 30-day baseline
  - Week-1 retention (`avg_view_percentage`) for any video < 22%
  - (Per-video day-over-day view-velocity drop is NOT checkable on the current schema — no
    per-video daily history is stored. Skip this check until such a table exists.)

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
