---
name: source-command-status
description: "Reads current project state across the lifecycle folders and names the single next action. Use when: asked 'what should I do', 'where are we', 'what's the status', or at the start of a work session."
---

> **Codex note.** This is the Codex port of `.claude/commands/status.md`, which stays canonical.
> The procedure below is that file verbatim. While running here: a `/name` reference is the
> `source-command-name` skill in `.agents/skills/`; "the Task tool" means spawning a Codex agent
> from `.codex/agents/`; "Claude" means you.

# /status - Context-Aware Project Router

Show current project state and suggest the logical next action. This command detects project context automatically and provides workflow guidance.

## Usage

```
/status                      # Dashboard: all projects overview
/status [project]            # Single project: detailed status + next action
```

Also responds to natural language:
- "What should I do?"
- "What's next?"
- "Where am I?"
- "Project status"
- "Show all projects"
- "Project dashboard"
- "What's in production"

---

## DASHBOARD MODE (No Arguments)

**Trigger condition:** User runs `/status` with no arguments, or says "show all projects", "project dashboard", "what's in production"

**Action:** Run the following Python code block:

```python
import sys
sys.path.insert(0, '.')
from tools.dashboard.project_scanner import scan_projects, format_dashboard

data = scan_projects('.')
print(format_dashboard(data))
```

**Display:** Show the output directly to the user. The formatted dashboard IS the response — no additional processing needed.

**After displaying:** Ask "Which project would you like to work on?" to guide the user to a specific project action.

---

## DETECTION LOGIC

### Step 0: Check for Dashboard Mode

**If no arguments provided** (user ran `/status` with no project name) → Run **DASHBOARD MODE** (above) instead of the detection logic below.

### Step 1: Find Active Project

**Check in order:**

1. **User-specified project:** If user provides project name, use that
2. **Git status:** Check recently modified files in `video-projects/_IN_PRODUCTION/`
3. **Directory scan:** Find projects with recent activity (modified in last 7 days)

```bash
# Find recently modified projects
git status --porcelain | grep "video-projects/_IN_PRODUCTION"
ls -lt video-projects/_IN_PRODUCTION/ | head -5
```

**If multiple projects active:** List them and ask user which one.

**If no active project:** Suggest starting new project with `/research`.

### Step 2: Assess Project State

**Check file existence in project folder:**

| File | Meaning |
|------|---------|
| `01-VERIFIED-RESEARCH.md` | Research exists |
| `SCRIPT.md` (with content beyond placeholder) | Script written |
| `03-FACT-CHECK-VERIFICATION.md` (with verdict) | Verified |
| `YOUTUBE-METADATA.md` | Metadata ready |
| `EDITING-GUIDE.md` or `B-ROLL-CHECKLIST.md` | Filming prep done |

**Check research status:**
- Open `01-VERIFIED-RESEARCH.md`
- Count verified claims vs. total claims
- Calculate verification percentage

**Check script status:**
- If SCRIPT.md exists, check if it has actual content (not just placeholder)
- Word count to estimate completeness

**Check verification status:**
- Look for `VERDICT:` line in 03-FACT-CHECK-VERIFICATION.md
- Values: APPROVED, NEEDS REVISION, or not yet verified

### Step 3: Determine Phase

**Phase Logic:**

```
IF no project folder:
    → No active project (suggest /research --new)

ELSE IF no 01-VERIFIED-RESEARCH.md OR research < 90% verified:
    → Pre-production Phase 1: Research
    → Suggest: Continue research, or /sources for NotebookLM prompts

ELSE IF no SCRIPT.md OR SCRIPT.md is placeholder only:
    → Production Phase 1: Scripting
    → Suggest: /script to write from verified research

ELSE IF no 03-FACT-CHECK-VERIFICATION.md OR no APPROVED verdict:
    → Production Phase 2: Verification
    → Suggest: /verify to fact-check script

ELSE IF no YOUTUBE-METADATA.md:
    → Post-production Phase 1: Metadata
    → Suggest: /publish for YouTube metadata

ELSE IF no EDITING-GUIDE.md:
    → Post-production Phase 2: Filming Prep
    → Suggest: /prep for edit guide and B-roll checklist

ELSE:
    → Complete: Ready to film
    → Suggest: Check all files, then film!
```

### Step 4: Generate Status Report

**Output format:**

```markdown
## Project Status: [Project Name]

**Phase:** [Pre-production | Production | Post-production | Complete]
**Location:** video-projects/_IN_PRODUCTION/[folder]/

### Current State

- [x] Research complete (01-VERIFIED-RESEARCH.md) - 95% verified
- [x] Script written (SCRIPT.md) - 2,847 words
- [ ] Fact-check verified (03-FACT-CHECK-VERIFICATION.md)
- [ ] Metadata ready (YOUTUBE-METADATA.md)
- [ ] Filming prep (EDITING-GUIDE.md)

### Suggested Next Action

**Run:** `/verify`
**Why:** Script is complete. Fact-check before filming to catch any errors.

### Alternative Actions

- `/script --review` - Review script for quality issues first
- `/script --revise` - Make changes to script
- `/prep --edit-guide` - Skip to filming prep (not recommended)
```

---

## SPECIAL CASES

### No Active Project

```markdown
## No Active Project Detected

You don't have any projects in active development.

### Start a New Project

**Run:** `/research --new "Your Topic"`

This will:
1. Create project folder in _IN_PRODUCTION/
2. Set up research files
3. Generate NotebookLM source list

### Or Explore a Topic First

**Run:** `/research --topic-only "Topic"`

This researches without creating a project folder.
```

### Multiple Active Projects

```markdown
## Multiple Projects Detected

Found 3 projects with recent activity:

| Project | Phase | Last Modified |
|---------|-------|---------------|
| 19-flat-earth-medieval-2025 | Production | 2 hours ago |
| 21-haiti-independence-debt-2025 | Pre-production | 1 day ago |
| 15-library-alexandria-2025 | Pre-production | 3 days ago |

**Which project?** Enter number or name, or I'll assume the most recent.
```

### Project Needs Attention

When issues detected, flag them:

```markdown
### Attention Needed

**Research gaps:** 3 claims in 01-VERIFIED-RESEARCH.md still marked as unverified.

**Fact-check findings:** 03-FACT-CHECK-VERIFICATION.md shows NEEDS REVISION verdict.
See file for specific corrections needed.
```

---

## NATURAL LANGUAGE RESPONSES

This command also activates when user asks:

| User Says | Response |
|-----------|----------|
| "What should I do?" | Full status with next action |
| "What's next?" | Just the suggested next action |
| "Where am I?" | Phase and project location |
| "Project status" | Full status report |
| "What's the status of X?" | Status for specific project |
| "Am I ready to film?" | Verification status + checklist |

---

## QUICK STATUS (One-liner)

For brief status, output single line:

```
[Project] | [Phase] | Next: [Command]

Example:
19-flat-earth-medieval-2025 | Production | Next: /verify
```

---

## PUBLISHED VIDEO MONITOR (Auto-run in Dashboard Mode)

**After displaying the project dashboard, ALWAYS run the published video monitor.**

This checks for videos that need post-publish attention. It prevents the "publish and forget" pattern that kills views.

### Step 1: Check for Recent Publishes

Read `video-projects/PROJECT_STATUS.md` and identify all videos with status PUBLISHED. For each, check the published date.

### Step 2: Flag Videos Needing Attention

Display a **PUBLISHED VIDEO MONITOR** section after the dashboard:

```
--- PUBLISHED VIDEO MONITOR ---

SWAP CHECK (48h+):
  ! Vichy Statut des Juifs — published 2026-03-05 (8 days ago) — CHECK CTR IN YOUTUBE STUDIO
  ! Bermeja Island — title swapped 2026-03-05 (8 days ago) — CHECK POST-SWAP CTR

RETITLE CANDIDATES (high impressions, low CTR):
  ! Dark Ages — 7,237 imp, 1.11% CTR → 172 wasted clicks. SWAP TITLE + THUMBNAIL
  ! Tariff Myth — 6,055 imp, 1.01% CTR → 150 wasted clicks. SWAP TITLE + THUMBNAIL
  ! Stalin — 5,538 imp, 1.55% CTR → 107 wasted clicks. SWAP TITLE + THUMBNAIL

Run `python -m tools.retitle_audit` for full report.
See `channel-data/THUMBNAIL-REFRESH-PLAN-2026-03.md` for swap plan.

NEWS HOOKS (timely opportunities):
  Run `python -m tools.discovery.news_hook_monitor --scan` for current alerts.
---
```

### Step 3: Generate Monitor Data

Run the retitle audit tool to get the top retitle candidates:

```python
import sys
sys.path.insert(0, '.')
from tools.retitle_audit import audit
results = audit(min_impressions=1000, top_n=3)
for r in results:
    print(f"  ! {r['title']} — {r['impressions']:,} imp, {r['ctr']:.2f}% CTR → {r['wasted_impressions']} wasted clicks. {r['diagnosis']}")
```

### Rules:
- ALWAYS show the monitor in dashboard mode — never skip it
- Flag any video published in the last 7 days that hasn't had a 48h CTR check
- Flag any video with CTR < 2% and > 1,000 impressions as a retitle candidate
- If a THUMBNAIL-REFRESH-PLAN exists, mention it and how many swaps remain unchecked

---

## Reference Files

- **Project lifecycle folders:** `video-projects/_IN_PRODUCTION/`, `_READY_TO_FILM/`, `_ARCHIVED/`
- **Standard files:** 01-VERIFIED-RESEARCH.md, SCRIPT.md, 03-FACT-CHECK-VERIFICATION.md
- **Help command:** `/help` for full command menu
- **Retitle audit:** `python -m tools.retitle_audit` — wasted impressions report
- **Thumbnail refresh plan:** `channel-data/THUMBNAIL-REFRESH-PLAN-2026-03.md`
- **Swap protocol:** `tools/SWAP-PROTOCOL.md`
