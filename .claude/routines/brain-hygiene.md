# Routine 5 — Nightly Brain Hygiene + Index Maintenance

**Purpose:** Every night, process the brain queue, lint for dead links and stale content, and refresh `.brain/index.md` AUTO sections. The repo's knowledge base stays coherent without manual upkeep.

> **▶ EXECUTION DIRECTIVE (you are being run headless via `claude -p` — the routine path):** You ARE the nightly brain-hygiene routine. Execute STEP 1–5 in the fenced block below **right now** against this repo at `G:\History vs Hype` — do not treat the block as a template to describe or "paste somewhere." The `## Setup` and `## Guardrails` sections are reference for the human; honor every guardrail but do not act on the Setup section. If `.brain/_queue/` is empty AND lint finds <3 issues AND index.md needs no material change, exit silently per STEP 4 (that is correct success, not a skip). Do NOT respond with "what would you like to work on?" — you already have your task: the steps below.

**Schedule:** Daily, 22:00 local (Desktop scheduled task — end of day)
**Why Desktop:** Reads across all 4 brain roots including non-repo paths (`~/llm-brain/`, project memory).
**Expected cost:** 1 of the 5 daily Routines credits.

---

## Paste this into Desktop Scheduled Task (prompt field)

```
You are operating inside the History vs Hype repository at G:\History vs Hype.

The brain has 5 roots:
- channel-data/            → channel performance + competitor tracking
- tools/benchmark/         → title/thumbnail/hook playbooks
- .brain/                  → sources, threads, methodology, inbox
- ~/llm-brain/             → global cross-project methodology
- ~/.claude/projects/D--History-vs-Hype/memory/  → user/feedback/project memories

STEP 1 — Process .brain/_queue/ (paste-and-forget items):

  For each file in .brain/_queue/:
    a. Determine type: raw transcript, article URL, quote dump, or concept note.
    b. If it's a URL or bulk text (>2000 chars): pipe to Gemini for extraction:
       gemini --yolo -p "Extract structured notes from this content. Output: ## SUMMARY (3-5 sentences), ## KEY QUOTES (verbatim, with attribution), ## CONCEPTS (bullet list), ## CONNECTIONS TO HISTORY VS HYPE (how this applies to the channel). Content follows." -o text
    c. Write structured output to .brain/sources/ (for verified quotes) or .brain/threads/ (for cross-source synthesis).
    d. Delete the processed item from .brain/_queue/.

STEP 2 — Brain-lint pass:

  Check for:
  a. Dead links: any URL in .brain/**/*.md that returns 404 (spot-check 5 random links)
  b. Orphan pages: files in .brain/threads/ or .brain/sources/ with no inbound links
  c. Stale claims: any claim in .brain/**/*.md older than 90 days marked as [UNVERIFIED]
  d. Contradictions: scan for "<!-- CONTRADICTION" markers in wiki/contradictions/

  Collect findings. Only report if ≥3 total issues found.

STEP 3 — Refresh .brain/index.md AUTO sections:

  Read .brain/index.md. Identify sections by their <!-- AUTO:routine-5 --> markers.
  Only edit content between a <!-- AUTO:routine-5 --> marker and the next --- divider.
  Do NOT touch <!-- MANUAL --> sections (§1 Multi-Root Map, §3 Active Topics).

  a. §4 "Recently added / changed":
     - Find the block starting with "## 4. Recently Added"
     - Prepend a new bullet for EACH file written or modified today (format: "- YYYY-MM-DD — `path` — one-line description")
     - Remove any bullet whose date is older than 14 days from today
     - Leave existing bullets in place; only prepend/prune

  b. §5 "Health signals":
     - Find the ``` code block under "## 5. Health Signals"
     - Replace its contents with:
       LAST LINT: YYYY-MM-DD HH:MM
       Stale items (>90d unverified):  [count from Step 2c]
       Orphan pages (no inbound links): [count from Step 2b]
       Open contradictions:             [count from Step 2d]
       Next lint scheduled:             tomorrow 22:00 local (Routine 5)

  c. §6 "Cross-root links":
     - Glob video-projects/_IN_PRODUCTION/*/01-VERIFIED-RESEARCH.md
     - Grep each for ~/llm-brain/ references
     - Replace the §6 body with grouped bullet lists per active project
     - Archive references from projects no longer in _IN_PRODUCTION (move to "Prior projects" subsection)

  Only edit AUTO sections. Do NOT touch § 1, 2, 3.

STEP 4 — Decide whether to emit a report:
  Emit .brain/_inbox/brain-hygiene-YYYY-MM-DD.md ONLY if:
  - ≥3 items ingested from _queue/ (Step 1), OR
  - ≥3 lint findings (Step 2), OR
  - index.md changed materially (more than timestamp update)

  Report format:
  # Brain Hygiene — YYYY-MM-DD

  ## Queue ingested
  [N items processed — list titles]

  ## Lint findings
  [List issues found, or "None"]

  ## Index changes
  [Summary of what changed in index.md]

STEP 5 — Stop. Do not edit video project files. Do not push to git.
All writes are local to .brain/.
```

---

## Setup (Windows Task Scheduler)

```powershell
$action = New-ScheduledTaskAction -Execute "claude" -Argument "--print `"$(Get-Content .claude\routines\brain-hygiene.md -Raw)`"" -WorkingDirectory "G:\History vs Hype"
$trigger = New-ScheduledTaskTrigger -Daily -At "22:00"
Register-ScheduledTask -TaskName "HvH-BrainHygiene" -Action $action -Trigger $trigger -RunLevel Highest
```

## Guardrails
- **Never** edit video project files (scripts, research, metadata).
- **Never** push to git — local brain maintenance only.
- Only writes: `.brain/sources/`, `.brain/threads/`, `.brain/_inbox/`, `.brain/index.md` (AUTO sections only).
- If Gemini quota exhausted: skip Step 1 bulk items, log "Queue processing skipped (Gemini quota)".
- If `.brain/_queue/` is empty and lint finds <3 issues: exit silently.

## Interpreting results
- **No report (typical):** Routine ran, queue empty, brain healthy. No action needed.
- **Report with queue items:** New sources ingested — review .brain/sources/ for quality.
- **Report with lint findings:** Check .brain/index.md §5 for specific issues.
- **Report with index changes:** Review §4 to see what was added to the recently-changed feed.
