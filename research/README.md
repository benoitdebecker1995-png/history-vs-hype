# Research Folder Organization

**Last Cleaned:** 2026-01-21

---

## Folder Structure

This folder contains preliminary research and NotebookLM outputs that haven't been organized into specific video projects.

### Active Research Files
Files currently relevant to active or planned projects.

### `_archive/`
Move duplicate and outdated files here rather than deleting. See `_archive/CLEANUP-LOG.md` for history.

---

## Cleanup Checklist (2026-01-21)

- [x] Create `_archive/` subfolder
- [x] Move duplicate Cambodia-Thailand files (none found - already cleaned in Phase 1)
- [ ] Consolidate History vs Hype .docx files (user action needed)
- [ ] Move Vance research to project folder or archive (user action needed)
- [ ] Rename files to follow naming convention (optional)

---

## Maintenance Routine

### 30-Day Cleanup Rule

Files in research/ that are older than 30 days should be reviewed:

**If file relates to committed video project:**
- Move to `video-projects/_IN_PRODUCTION/[project]/_research/`

**If file is general reference:**
- Keep in research/ if still useful
- Move to research/_archive/ if outdated

**If file is duplicate or superseded:**
- Move to research/_archive/

**Monthly check (1st of each month):**
1. Sort research/ by modification date
2. Review files older than 30 days
3. Move to project folders or archive as appropriate
4. Update `_archive/CLEANUP-LOG.md` with actions taken

---

## Related Templates

When starting a new video project, use the standard _research subfolder structure:
- See: `.claude/templates/_RESEARCH-SUBFOLDER-TEMPLATE.md`

---

## File Naming Convention

**For new research:**
```
[Topic]_[Type]_[Date].md

Examples:
- Dark-Ages_NotebookLM-Output_2025-12.md
- Crusades_Preliminary-Research_2025-11.md
```

**File types:**
- `NotebookLM-Output` - Raw output from NotebookLM
- `Preliminary-Research` - Internet research before NotebookLM
- `Source-Recommendations` - Books/articles to purchase
- `Fact-Check-Results` - Verification outcomes

---

## When to Use This Folder vs. Project Folders

**Use `research/` for:**
- Topic exploration before committing to a video
- General reference materials
- Cross-project resources

**Use `video-projects/_IN_PRODUCTION/[project]/` for:**
- Research specific to a committed video project
- NotebookLM outputs for active scripts
- Anything you'll reference while writing a specific script
