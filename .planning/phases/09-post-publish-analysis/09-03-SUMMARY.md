---
phase: 09-post-publish-analysis
plan: 03
subsystem: analytics-tools
tags: [python, slash-command, file-saving, project-discovery]
completed: 2026-01-25
duration: ~20 minutes

dependency-graph:
  requires: ["09-02"]
  provides: ["analyze-slash-command", "auto-save-analysis"]
  affects: ["10-01"]

tech-stack:
  added: []
  patterns: ["project-folder-discovery", "graceful-fallback"]

key-files:
  created:
    - .claude/commands/analyze.md
    - channel-data/analyses/.gitkeep
  modified:
    - tools/youtube-analytics/analyze.py

decisions:
  - id: "fallback-location"
    choice: "channel-data/analyses/ for unmatched videos"
    rationale: "Central location for analyses when no project folder match found"
  - id: "search-order"
    choice: "_IN_PRODUCTION first, then _READY_TO_FILM, then _ARCHIVED"
    rationale: "Most likely to find active projects first"

metrics:
  tasks: 3
  commits: 3
  files_created: 2
  files_modified: 1
---

# Phase 9 Plan 03: Slash Command and File Saving Summary

**One-liner:** /analyze slash command with automatic project folder discovery and file saving, completing the post-publish analysis workflow.

## What Was Built

### Task 1: Project Folder Discovery and File Saving

Added two new functions to `analyze.py`:

**find_project_folder(video_id=None, video_title=None)**

Searches for project folders matching video ID or title.

Search strategy:
1. Video ID in any .md file within project folders
2. Title word matching against folder names
3. Returns absolute path or None

Search order:
- `video-projects/_IN_PRODUCTION/*`
- `video-projects/_READY_TO_FILM/*`
- `video-projects/_ARCHIVED/*`

**save_analysis(analysis, output_path=None)**

Saves analysis to appropriate location.

Behavior:
1. If `output_path` provided, use it
2. Else try `find_project_folder()` to match video
3. If matched: save as `{folder}/POST-PUBLISH-ANALYSIS.md`
4. If not matched: save to `channel-data/analyses/POST-PUBLISH-ANALYSIS-{video_id}.md`

Returns: `{'saved_to': path, 'project_folder_found': bool}`

**CLI Additions:**
```bash
python analyze.py VIDEO_ID --save
python analyze.py VIDEO_ID --save --output ./custom/path.md
```

### Task 2: /analyze Slash Command

Created `.claude/commands/analyze.md` with:

- Clear usage documentation
- What the command does (5-step workflow)
- Examples for all input formats
- Execution instructions for Claude
- CTR fallback documentation
- Related commands section

**Usage:**
```
/analyze VIDEO_ID_OR_URL [--ctr VALUE]
```

### Task 3: Analyses Fallback Directory

Created `channel-data/analyses/` with `.gitkeep` to ensure:
- Directory exists for fallback saves
- Analysis files are tracked in git

## Verification Results

| Test | Command | Result |
|------|---------|--------|
| Import functions | `from analyze import find_project_folder, save_analysis` | OK |
| Find known video | `find_project_folder('6aFkoX6g1fE')` | Returns crusades-fact-check path |
| Find unknown video | `find_project_folder('wCFReiCGiks')` | Returns None (expected) |
| Invalid video ID | `python analyze.py INVALID123456` | Graceful error in JSON |
| Fallback directory | `ls channel-data/analyses/` | .gitkeep exists |

## Commits

| Hash | Description |
|------|-------------|
| 2c32ffa | feat(09-03): add project folder discovery and file saving to analyze.py |
| 2011eed | feat(09-03): create /analyze slash command |
| e35a1a9 | chore(09-03): create analyses fallback directory |

## Deviations from Plan

None - plan executed exactly as written.

## Requirements Coverage (Phase 9 Complete)

| Requirement | Status | Implementation |
|-------------|--------|----------------|
| ANALYSIS-01 | Complete | `/analyze` command triggers full analysis |
| ANALYSIS-02 | Complete | CTR comparison + manual fallback |
| ANALYSIS-03 | Complete | All drop-offs with timestamps/locations |
| ANALYSIS-04 | Complete | Comments fetched and categorized |
| ANALYSIS-05 | Complete | Lessons in observations + actionable format |
| ANALYSIS-06 | Complete | Analysis linked to project folder (or fallback) |

## Full Workflow

User runs `/analyze VIDEO_ID`:
1. Claude executes `python analyze.py VIDEO_ID --save --markdown`
2. Analysis fetches metrics, retention, comments
3. Benchmarks calculated against channel average
4. Lessons generated automatically
5. File saved to project folder or fallback
6. Markdown displayed to user with saved location

## Next Phase Readiness

Phase 10 (Pattern Recognition) can proceed:
- All Phase 9 requirements complete
- Analysis files saved consistently
- Data available for pattern recognition across videos

No blockers identified. Phase 9 complete.
