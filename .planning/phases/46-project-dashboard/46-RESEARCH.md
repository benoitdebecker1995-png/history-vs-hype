# Phase 46: Project Dashboard - Research

**Researched:** 2026-02-22
**Domain:** Slash command enhancement, filesystem scanning, Python tool module
**Confidence:** HIGH — all findings from direct codebase inspection

---

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

- **Dashboard output format:** Enhance existing /status command (not a new command). Table format showing: project name, current phase, next action, days since activity. Projects sorted by priority: filming-ready > research phase > ideas. Brief and scannable — not a wall of text.
- **Priority ranking logic:** Detect project phase from files present: FINAL-SCRIPT.md = filming-ready, 02-SCRIPT-DRAFT.md = scripting, 01-VERIFIED-RESEARCH.md = research, just folder = idea. Days since last activity from git log or file modification dates. Flag stale projects (>14 days inactive).
- **Time-sensitive flagging:** Read youtube-intelligence.md for trending topics and deadline data. Cross-reference project topics against intel data. Flag format: brief note next to project (e.g., "ICJ ruling 2027 — deadline approaching"). Skip silently if no intel data available.

### Claude's Discretion

- Exact table formatting and column widths
- How to detect project topic for intel cross-reference
- Whether to include archived projects count as summary line
- Color/emoji usage in output

### Deferred Ideas (OUT OF SCOPE)

None — discussion stayed within phase scope.
</user_constraints>

---

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| DASH-01 | /status shows all projects in production with current phase, next action, and days since last activity | Phase detection logic (files-present method) + filesystem mtime for days since activity confirmed working |
| DASH-02 | Projects ranked by priority (filming-ready first, then research phase, then ideas) | Priority tier mapping documented below; 39 folders scanned and classified correctly |
| DASH-03 | Dashboard integrates with YouTube Intelligence Engine to flag time-sensitive topics | query.py and youtube-intelligence.md format confirmed; KBStore niche_snapshots.trending_topics is the cross-reference source |
</phase_requirements>

---

## Summary

Phase 46 enhances `/status` from a single-project status checker into a multi-project dashboard. The current `/status` command is a pure LLM instruction file (no Python, no external calls beyond git bash commands it instructs the agent to run). The enhancement means `/status` (with no arguments) should show all projects, while `/status [project]` retains the current single-project behavior.

The codebase already has a complete Python tooling pattern used by other commands: a `tools/` module (`tools/intel/`, `tools/youtube-analytics/`, etc.) called via inline Python code blocks in the slash command `.md` file. Phase 46 follows this same pattern with a new `tools/dashboard/` module.

The _IN_PRODUCTION folder contains 39 projects (38 numbered + "Tariffs"). Phase detection works cleanly via file presence. The intel integration reads `channel-data/youtube-intelligence.md` (a flat Markdown file updated by `/intel --refresh`) — the same pattern used by `/prep`, `/script`, and `/publish`. No new database tables are needed.

**Primary recommendation:** Create `tools/dashboard/project_scanner.py` containing the scan/classify/rank logic, then update `.claude/commands/status.md` to call it inline when no project argument is given.

---

## Standard Stack

### Core

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| pathlib | stdlib | Filesystem traversal, file existence checks | Used throughout all tools/* modules |
| os.stat / pathlib.stat() | stdlib | File mtime for "days since activity" | No subprocess needed for file dates |
| subprocess / git | system | Git log fallback for last-committed activity | Same approach used in status.md already |

### Supporting

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| datetime | stdlib | Days-since calculation from mtime or git timestamp | Required for stale detection |
| re | stdlib | Topic extraction from folder name slug | Needed for intel cross-reference without reading files |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| pathlib.stat().st_mtime | git log --format="%ai" | Mtime is faster (no subprocess), covers untracked files; git only covers committed changes. Use mtime as primary. |
| Reading PROJECT-STATUS.md for topic | Parse folder name slug | Folder name is always present and fast. PROJECT-STATUS.md parsing is slower and not standardized. |
| tools/intel/query.py functions | Direct youtube-intelligence.md read | Direct file read is simpler for dashboard use case; query.py functions return formatted Markdown which is harder to cross-reference against project slugs |

**No new pip installs required.** All stdlib.

---

## Architecture Patterns

### Recommended Project Structure

```
tools/dashboard/
├── __init__.py          # Module docstring only (follows intel/ pattern)
└── project_scanner.py   # All dashboard logic: scan, classify, rank, format
```

The command file is updated in place:

```
.claude/commands/status.md   # Enhanced: new "DASHBOARD MODE" section prepended
```

### Pattern 1: Python Inline Code Block in Slash Command

All v4.0/v5.0 slash commands call Python tools via inline code blocks. The agent reads the `.md`, sees the code block, and executes it. This is the established pattern.

**How analyze.md does it:**
```python
import sys
sys.path.insert(0, '.')
from pathlib import Path
from tools.youtube_analytics.backfill import run_backfill

project_root = Path('.')
result = run_backfill(project_root)
print(f"JSON import: {result['imported_json']} videos")
```

**Dashboard pattern (for status.md):**
```python
import sys
sys.path.insert(0, '.')
from tools.dashboard.project_scanner import scan_projects, format_dashboard

results = scan_projects(project_root='.')
print(format_dashboard(results))
```

### Pattern 2: Phase Detection via File Presence

Confirmed working approach (verified against all 39 _IN_PRODUCTION folders):

```python
def detect_phase(folder: Path) -> str:
    files = {f.name for f in folder.iterdir() if f.is_file()}
    # Filming-ready signals (strongest)
    if 'FINAL-SCRIPT.md' in files:
        return 'filming-ready'
    if any('TELEPROMPTER' in f.upper() for f in files):
        return 'filming-ready'
    # Fact-checked: script + verification present
    if '03-FACT-CHECK-VERIFICATION.md' in files and (
        '02-SCRIPT-DRAFT.md' in files or 'SCRIPT.md' in files
    ):
        return 'fact-checked'
    # Scripting: draft script present
    if '02-SCRIPT-DRAFT.md' in files or 'SCRIPT.md' in files:
        return 'scripting'
    # Research: research file present
    if '01-VERIFIED-RESEARCH.md' in files:
        return 'research'
    return 'idea'
```

**Phase priority order for sorting (highest = most urgent):**

| Priority | Phase | Files Present |
|----------|-------|---------------|
| 1 (highest) | filming-ready | FINAL-SCRIPT.md or TELEPROMPTER*.md |
| 2 | fact-checked | 03-FACT-CHECK-VERIFICATION.md + SCRIPT |
| 3 | scripting | 02-SCRIPT-DRAFT.md or SCRIPT.md |
| 4 | research | 01-VERIFIED-RESEARCH.md |
| 5 (lowest) | idea | folder only |

### Pattern 3: Days Since Activity (mtime-based)

File system mtime is more reliable than git for this use case because most files in _IN_PRODUCTION are untracked (videos, PSD files, audio recordings). Git log shows commits, but the user's actual activity is better reflected by when any file in the folder was last modified.

```python
import os
from datetime import datetime, timezone

def days_since_activity(folder: Path) -> int:
    latest_mtime = 0.0
    for item in folder.iterdir():
        try:
            mtime = item.stat().st_mtime
            if mtime > latest_mtime:
                latest_mtime = mtime
        except OSError:
            pass
    if latest_mtime == 0.0:
        return 999  # sentinel for unknown
    delta = datetime.now(timezone.utc).timestamp() - latest_mtime
    return int(delta / 86400)
```

**Stale threshold:** >14 days per CONTEXT.md decision.

### Pattern 4: Next Action Mapping

| Phase | Next Action |
|-------|-------------|
| filming-ready | Film it |
| fact-checked | /prep --edit-guide |
| scripting | /verify |
| research | /script |
| idea | /research --new |

### Pattern 5: Topic Extraction from Folder Name

The folder naming convention `[number]-[topic-slug]-[year]` allows topic extraction without reading files:

```python
import re

def extract_topic_slug(folder_name: str) -> str:
    """Extract topic words from folder slug like '35-gibraltar-treaty-utrecht-2026'"""
    # Remove leading number and trailing year
    slug = re.sub(r'^\d+-', '', folder_name)
    slug = re.sub(r'-\d{4}$', '', slug)
    return slug.replace('-', ' ')
    # Returns: 'gibraltar treaty utrecht'
```

This is used to cross-reference against intel trending topics (simple substring matching).

### Pattern 6: Intel Cross-Reference

The `channel-data/youtube-intelligence.md` file is the authoritative intel source (same as `/prep`, `/script`, `/publish`). The trending_topics section format is:

```markdown
### Trending Topics

| Topic | Count | % |
| ----- | ----- | - |
| war | 5 | 16.7% |
| roman | 1 | 3.3% |
```

For the dashboard, read this file directly and extract the trending topic words. Then do simple substring matching against the project slug. This is LLM-suitable logic (the agent can do this comparison during output generation without Python).

**Time-sensitive flagging approach:** The intel data currently does NOT contain explicit deadline dates (those come from the project's own research files). The CONTEXT example "ICJ ruling 2027 — deadline approaching" would need to come from PROJECT-STATUS.md or the verified research file. However, the trending topic cross-reference IS available from intel.

**Recommendation:** Keep intel cross-reference lightweight — match project slug words against intel trending topics. If a project topic overlaps with a trending topic, surface a brief note. For deadline flagging, read the first 30 lines of PROJECT-STATUS.md (if present) looking for year references like "2026", "2027", "expir", "deadline", "ICJ".

### Pattern 7: Skip Published Projects

Projects with `POST-PUBLISH-ANALYSIS.md` are already published (6 found in _IN_PRODUCTION). The dashboard should either skip these or show them in a separate "Published (not archived)" count. Per CONTEXT: the user wants "projects in _IN_PRODUCTION with priority ranking" — published projects should appear in a separate summary line, not clutter the priority table.

### Anti-Patterns to Avoid

- **Reading every file in every project:** Only check file names and mtime, not file contents (except PROJECT-STATUS.md for deadline hints). 39 projects x reading full content = too slow.
- **Blocking on missing intel:** Same as other commands — skip intel cross-reference silently if `channel-data/youtube-intelligence.md` doesn't exist.
- **Treating _READY_TO_FILM as in-production:** The dashboard scans _IN_PRODUCTION only. _READY_TO_FILM (currently has 1 project: 1-sykes-picot-2025) can be listed separately if it has content.
- **git log as primary mtime source:** Git only tracks committed files. Most project assets (mp4, psd, srt, audio) are untracked. Use filesystem mtime.
- **Creating a new command:** User explicitly decided to enhance /status, not add a new command.

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| File type filtering | Custom extension blacklists | Skip subdirectories, accept all file mtimes | Subdirs (like `_research/`) are walked but their mtime propagates to parent on Windows; just check top-level files |
| Markdown table formatting | Custom table builder | f-string formatting with fixed-width padding | Simple, no dependencies, readable |
| Intel parsing | Full Markdown parser | Line-by-line scan for "Trending Topics" section | Only need topic words from one table |

---

## Common Pitfalls

### Pitfall 1: Windows mtime vs git timestamp discrepancy

**What goes wrong:** On Windows, `pathlib.stat().st_mtime` reflects the local timezone implicitly while `datetime.now()` returns local time. The subtraction works correctly for day-count purposes, but mixing `timezone.utc` timestamps with naive local datetimes will produce wrong results.

**How to avoid:** Use `datetime.now().timestamp()` (naive, local) and compare against `st_mtime` (also local). OR use `datetime.now(timezone.utc).timestamp()` and ensure mtime is also treated as UTC. Don't mix tz-aware and naive. Simplest: `int((time.time() - st_mtime) / 86400)` using `time.time()` which returns UTC epoch on all platforms.

**Warning signs:** Days counts come out negative or very large (thousands of days).

### Pitfall 2: Folder name exceptions

**What goes wrong:** `_IN_PRODUCTION/` contains non-numbered items: `README.md`, `README-UNTRANSLATED-TOPICS.md`, `Tariffs/` folder. The scanner must filter to only directories and skip README files.

**How to avoid:** `for item in Path(prod_dir).iterdir(): if item.is_dir() and not item.name.startswith('README'):`

**Warning signs:** KeyError or AttributeError when processing non-project items.

### Pitfall 3: Subdirectories inflating mtime

**What goes wrong:** Some projects have `_research/`, `_sources/` subdirectories. If the scanner recursively walks these, it may find recent activity in a subdir that makes a stale project look active.

**How to avoid:** Scan only top-level files in the project folder (not recursive). The relevant activity is top-level files (script, research, fact-check, SRT).

### Pitfall 4: 03-FACT-CHECK-VERIFICATION.md without a script = false positive

**What goes wrong:** Phase detection checks for `03-FACT-CHECK-VERIFICATION.md` to detect "fact-checked" phase. But the file may exist without a script (e.g., an empty placeholder). Must also check for script file presence.

**How to avoid:** Phase detection requires BOTH `03-FACT-CHECK-VERIFICATION.md` AND (`02-SCRIPT-DRAFT.md` OR `SCRIPT.md`) for "fact-checked" phase (already reflected in Pattern 2 above).

### Pitfall 5: Status.md current single-project mode breaks

**What goes wrong:** Enhancing `/status` to show all projects by default could break the existing workflow for single-project status checks.

**How to avoid:** The update to `status.md` must preserve the existing single-project logic. Structure the command as:
- `/status` with no args → Dashboard mode (all projects table)
- `/status [project]` → Existing single-project mode (unchanged)
- Natural language "What should I do?" → Existing mode

---

## Code Examples

### Full scan_projects() signature

```python
# tools/dashboard/project_scanner.py

from pathlib import Path
import time
import re
from typing import Optional

PHASE_PRIORITY = {
    'filming-ready': 1,
    'fact-checked':  2,
    'scripting':     3,
    'research':      4,
    'idea':          5,
}

NEXT_ACTION = {
    'filming-ready': 'Film it',
    'fact-checked':  '/prep --edit-guide',
    'scripting':     '/verify',
    'research':      '/script',
    'idea':          '/research --new',
}

STALE_THRESHOLD_DAYS = 14

def scan_projects(project_root: str = '.') -> dict:
    """
    Scan _IN_PRODUCTION for all projects. Returns dict with:
      - projects: list of project dicts (name, phase, next_action, days_since, stale, published)
      - ready_to_film: list from _READY_TO_FILM (if any)
      - intel_topics: list of trending topic strings from youtube-intelligence.md
    """
    root = Path(project_root)
    prod_dir = root / 'video-projects' / '_IN_PRODUCTION'
    ready_dir = root / 'video-projects' / '_READY_TO_FILM'
    intel_path = root / 'channel-data' / 'youtube-intelligence.md'

    projects = []
    for folder in sorted(prod_dir.iterdir()):
        if not folder.is_dir() or folder.name.startswith('README'):
            continue
        files = {f.name for f in folder.iterdir() if f.is_file()}
        phase = detect_phase(files)
        days = days_since_activity_top_level(folder)
        published = 'POST-PUBLISH-ANALYSIS.md' in files
        topic_slug = extract_topic_slug(folder.name)
        projects.append({
            'name': folder.name,
            'phase': phase,
            'priority': PHASE_PRIORITY.get(phase, 99),
            'next_action': NEXT_ACTION.get(phase, '?'),
            'days_since': days,
            'stale': days > STALE_THRESHOLD_DAYS,
            'published': published,
            'topic_slug': topic_slug,
        })

    # Sort: published last, then by priority, then by days_since (most recent first)
    projects.sort(key=lambda p: (p['published'], p['priority'], p['days_since']))

    intel_topics = extract_intel_topics(intel_path)

    # _READY_TO_FILM
    ready = []
    if ready_dir.exists():
        for folder in sorted(ready_dir.iterdir()):
            if folder.is_dir() and not folder.name.startswith('README'):
                ready.append(folder.name)

    return {'projects': projects, 'ready_to_film': ready, 'intel_topics': intel_topics}
```

### format_dashboard() output target

```
## Project Dashboard

| Project | Phase | Next Action | Days Since Activity |
|---------|-------|-------------|---------------------|
| 31-bermeja-island-2025 | fact-checked | /prep --edit-guide | 3 |
| 35-gibraltar-treaty-utrecht-2026 | scripting | /verify | 3 |
| 37-untranslated-vichy-statut-juifs-2026 | fact-checked | /prep --edit-guide | 2 |
| 38-spanish-colonial-law-untranslated-2026 | fact-checked | /prep --edit-guide | 3 |
| 23-christmas-origins-2025 | scripting | /verify | 7 ⚠ STALE |
| ... | ... | ... | ... |

**6 published (not archived):** 1-somaliland, 4-crusades, 12-guatemala, 24-iran-1953, 25-iran-protests, 34-operation-condor
**_READY_TO_FILM:** 1-sykes-picot-2025

Intel cross-reference: "border" topic trending — 35-gibraltar, 36-panama-canal match
```

### extract_intel_topics() from youtube-intelligence.md

```python
def extract_intel_topics(intel_path: Path) -> list[str]:
    """
    Read youtube-intelligence.md and extract trending topic words.
    Returns empty list if file missing (never raises).
    """
    if not intel_path.exists():
        return []
    try:
        content = intel_path.read_text(encoding='utf-8')
        topics = []
        in_trending = False
        for line in content.splitlines():
            if 'Trending Topics' in line:
                in_trending = True
                continue
            if in_trending and line.startswith('|'):
                # Parse table rows: | topic | count | % |
                parts = [p.strip() for p in line.split('|')]
                parts = [p for p in parts if p]
                if parts and parts[0] not in ('Topic', '-----'):
                    topics.append(parts[0])
            elif in_trending and line.startswith('#'):
                break  # End of section
        return topics
    except Exception:
        return []
```

---

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| /status = single project checker | /status = dashboard + single project | Phase 46 | Removes need to remember which project is active |
| Days since = git log | Days since = filesystem mtime | Phase 46 | Captures untracked file activity (videos, PSDs, audio) |
| Intel = advisory context during generation | Intel = time-sensitive flag in dashboard | Phase 46 | Surfaces urgency before user even picks a project |

---

## Open Questions

1. **Should published projects be suppressed entirely from the dashboard table?**
   - What we know: 6 projects have POST-PUBLISH-ANALYSIS.md but are still in _IN_PRODUCTION
   - What's unclear: User may want to see them (to remember to archive) or suppress them (noise)
   - Recommendation: Show count in footer ("6 published — consider archiving"), suppress from main table

2. **How specific should the intel deadline flag be?**
   - What we know: youtube-intelligence.md has trending_topics (generic: "war", "border", "roman") but no deadline dates. Deadlines are buried in project research files.
   - What's unclear: User CONTEXT example says "ICJ ruling 2027 — deadline approaching" which implies reading project files
   - Recommendation: Two-tier approach: (a) trending topic match from intel (always available), (b) optional PROJECT-STATUS.md first-50-lines scan for year references like "2027", "ICJ", "expir" — only for projects in top priority tiers (filming-ready, fact-checked, scripting)

3. **Should idea-phase projects show in dashboard at all?**
   - What we know: 20+ projects are "idea" phase (just a folder or basic brief). These would dominate the table.
   - What's unclear: User said "sorted by priority" but didn't explicitly say to suppress ideas
   - Recommendation: Show ideas as a collapsed count at bottom: "22 idea-phase projects not shown" to keep table scannable

---

## Sources

### Primary (HIGH confidence)

- Direct codebase inspection: `G:/History vs Hype/.claude/commands/status.md` — confirmed pure LLM instruction + bash; no Python
- Direct codebase inspection: `G:/History vs Hype/tools/intel/query.py` — confirmed integration pattern for Python tools
- Direct codebase inspection: `G:/History vs Hype/tools/intel/kb_store.py` — confirmed intel.db schema and KBStore pattern
- Direct codebase inspection: `G:/History vs Hype/channel-data/youtube-intelligence.md` — confirmed file format, trending topics section
- Direct filesystem scan: 39 _IN_PRODUCTION folders classified by file presence — phase detection approach validated
- Direct mtime scan: All 39 folders → confirmed mtime-based activity detection works (covers untracked files)
- Direct codebase inspection: `G:/History vs Hype/.claude/commands/analyze.md` — confirmed Python inline code block pattern
- Direct codebase inspection: `G:/History vs Hype/.claude/commands/prep.md` — confirmed intel cross-reference pattern (read file, extract 2-3 lines, skip silently if missing)

### Secondary (MEDIUM confidence)

- Observation: 6 projects have POST-PUBLISH-ANALYSIS.md in _IN_PRODUCTION — indicates published-not-archived pattern
- Observation: Only 4 projects have TELEPROMPTER file — this is the strongest filming-ready signal alongside FINAL-SCRIPT.md
- Observation: _READY_TO_FILM contains 1 project (1-sykes-picot-2025) — should be mentioned in dashboard footer

---

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — all stdlib, same as every other tools/* module
- Architecture: HIGH — directly observed from working commands (analyze.md, prep.md, intel/)
- Phase detection: HIGH — manually verified against 39 real projects
- Intel cross-reference: HIGH — file format confirmed, approach matches existing /prep pattern
- Pitfalls: HIGH — observed in actual project data (6 published, README non-dirs, _research subdirs)

**Research date:** 2026-02-22
**Valid until:** Stable — filesystem conventions and tool patterns don't change frequently; valid 90+ days
