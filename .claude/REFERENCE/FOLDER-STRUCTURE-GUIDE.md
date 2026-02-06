# Folder Structure Guide for Claude

## CRITICAL RULES - READ FIRST

**NEVER create loose folders in `video-projects/` root**

**ALWAYS check project location before creating files**

**ALWAYS save files in the correct lifecycle folder**

---

## Project Lifecycle Folders

### `video-projects/_IN_PRODUCTION/`
**Purpose:** Active research and scripting projects

**Contents:**
- Research files
- Draft scripts
- Fact-checking documents
- NotebookLM outputs
- Source recommendations

**Naming convention:**
```
video-projects/_IN_PRODUCTION/[number]-[topic-slug-year]/
Example: video-projects/_IN_PRODUCTION/3-kashmir-partition-2025/
```

**When to use:**
- New project starting research
- Scripting in progress
- Fact-checking not yet complete

---

### `video-projects/_READY_TO_FILM/`
**Purpose:** Finalized scripts ready for filming

**Contents:**
- FINAL-SCRIPT.md
- YOUTUBE-METADATA.md
- B-ROLL-CHECKLIST.md
- FACT-CHECK-VERIFICATION-SPREADSHEET.md
- Visual planning guides
- Completed research files

**Naming convention:**
```
video-projects/_READY_TO_FILM/[number]-[topic-slug-year]/
Example: video-projects/_READY_TO_FILM/1-sykes-picot-2025/
```

**When to use:**
- Script finalized and fact-checked
- Ready for filming
- All production documents complete

---

### `video-projects/_ARCHIVED/`
**Purpose:** Published or cancelled projects

**Contents:**
- Everything from _READY_TO_FILM/
- Published video metadata
- Performance analytics
- Post-production notes

**When to use:**
- Video published to YouTube
- Project cancelled/abandoned
- Historical reference

---

## Standard File Names

Within each project folder:

**Research & Development:**
- `00-QUICK-START-CHECKLIST.md`
- `01-topic-brief.md`
- `02-preliminary-research.md`
- `03-source-recommendations.md`
- `04-notebooklm-prompts.md`
- `05-notebooklm-output.md`
- `06-research-analysis.md`
- `07-script-draft.md`
- `07-script-draft-FINAL-VERIFIED.md`

**Production Ready:**
- `FINAL-SCRIPT.md` - **THE ONE TO FILM FROM** (only one allowed)
- `YOUTUBE-METADATA.md` - Title, description, tags, timestamps
- `B-ROLL-CHECKLIST.md` - Visual requirements
- `FACT-CHECK-VERIFICATION-SPREADSHEET.md` - Source verification
- `EDITING-GUIDE-SHOT-BY-SHOT.md` - Visual staging

---

## Script Versioning Rules (CRITICAL)

### The Rule: ONE Final Script
**Only `FINAL-SCRIPT.md` should exist when ready to film.**

When you revise a script:
1. Update `FINAL-SCRIPT.md` directly (preferred), OR
2. If keeping old version: rename old to `_old-versions/FINAL-SCRIPT-V1.md`

### What NOT to Do
```
❌ FINAL-SCRIPT.md + FINAL-SCRIPT-V2.md + FINAL-SCRIPT-V3.md (which is current?)
❌ SCRIPT-V3-FINAL.md + SCRIPT-V4-FINAL.md (confusing naming)
❌ FINAL-SCRIPT-V2-EDITED.md (unclear if this is THE final)
```

### What TO Do
```
✅ FINAL-SCRIPT.md (the one to film)
✅ _old-versions/FINAL-SCRIPT-V1.md (archived)
✅ _old-versions/FINAL-SCRIPT-V2.md (archived)
```

### During Active Development
While actively iterating:
- Keep working version as `02-SCRIPT-DRAFT.md` (from verified workflow)
- Only create `FINAL-SCRIPT.md` when truly final
- If you need to track major revisions during dev: use `02-SCRIPT-DRAFT-V2.md`

### Before Moving to _READY_TO_FILM
- [ ] Only ONE script file named `FINAL-SCRIPT.md`
- [ ] Old versions moved to `_old-versions/` or deleted
- [ ] No ambiguity about which script to film

**Editing/Post:**
- `finshed video.srt` - Subtitle file (often has typos, needs fixing)
- `[topic]_AUTOCUE.md` - Teleprompter version

---

## How to Check Project Location

**Step 1: Read PROJECT_STATUS.md**
```
Read: video-projects/PROJECT_STATUS.md
Find: Current active projects and their locations
```

**Step 2: Use Glob to confirm**
```
Glob pattern: video-projects/**/*[topic-keyword]*/
Confirms exact folder path
```

**Step 3: Verify before creating files**
```
- Check folder exists
- Confirm it's in correct lifecycle stage
- Use exact path for file creation
```

---

## Common Tasks & File Locations

### Creating YouTube Metadata
```
1. Find script: video-projects/_READY_TO_FILM/[project]/FINAL-SCRIPT.md
2. Read script content
3. Generate metadata
4. Save to: video-projects/_READY_TO_FILM/[project]/YOUTUBE-METADATA.md
```

### Writing New Script
```
1. Read PROJECT_STATUS.md
2. Find project in _IN_PRODUCTION/ or _READY_TO_FILM/
3. Save script to that folder
4. Use standard naming: FINAL-SCRIPT.md
```

### Fixing Subtitles
```
1. Find: video-projects/_READY_TO_FILM/[project]/*.srt
2. Fix common errors (timestamps, names)
3. Save in place
```

### Analyzing Script Structure
```
1. Find script: Use Glob pattern
2. Read and analyze
3. NO file creation needed (analysis only)
```

---

## Incorrect vs. Correct Examples

### ❌ WRONG - Loose folder in root
```
video-projects/sykes-picot-2025/YOUTUBE-METADATA.md
```

### ✅ CORRECT - In lifecycle folder
```
video-projects/_READY_TO_FILM/1-sykes-picot-2025/YOUTUBE-METADATA.md
```

### ❌ WRONG - Creating new root folder
```
mkdir video-projects/new-topic-2025
```

### ✅ CORRECT - Creating in lifecycle folder
```
mkdir video-projects/_IN_PRODUCTION/4-new-topic-2025
```

---

## Project Movement Through Lifecycle

**New Project:**
```
video-projects/_IN_PRODUCTION/4-topic-2025/
```

**Script Ready:**
```
mv video-projects/_IN_PRODUCTION/4-topic-2025 video-projects/_READY_TO_FILM/4-topic-2025
Update PROJECT_STATUS.md
```

**Published:**
```
mv video-projects/_READY_TO_FILM/4-topic-2025 video-projects/_ARCHIVED/4-topic-2025
Update PROJECT_STATUS.md
```

---

## Pre-Creation Checklist

Before creating ANY file in video-projects/:

- [ ] Read PROJECT_STATUS.md to understand current state
- [ ] Use Glob to find existing project folder
- [ ] Confirm folder is in correct lifecycle stage
- [ ] Verify I'm not creating a loose folder in root
- [ ] Use exact path from Glob results
- [ ] Save with standard naming convention

---

## User Preferences Related to Folders

1. **Read context first**
   - Don't ask "where should I save this?"
   - Use Glob to find the project
   - Save to the correct location automatically

2. **Be efficient**
   - No questions about folder structure
   - Check and confirm location silently
   - Just do it correctly

3. **Clean up mistakes**
   - If you create a loose folder, delete it immediately
   - Move files to correct location
   - Update PROJECT_STATUS.md if needed

---

## Common Mistakes to Avoid

1. **Creating `video-projects/topic-name/` folders**
   - ALWAYS use lifecycle folders

2. **Not checking existing location**
   - Project might already exist
   - Might be in wrong lifecycle stage

3. **Asking user for folder location**
   - You can find it with Glob
   - Read PROJECT_STATUS.md
   - Be autonomous

4. **Inconsistent naming**
   - Use standard file names
   - Follow project numbering
   - Keep year suffix

---

## Quick Reference

**Find project location:**
```
1. Glob: video-projects/**/*[keyword]*/
2. Or read: video-projects/PROJECT_STATUS.md
```

**Standard paths:**
```
_IN_PRODUCTION: Active work
_READY_TO_FILM: Ready to shoot
_ARCHIVED: Published/cancelled
```

**Standard files:**
```
FINAL-SCRIPT.md
YOUTUBE-METADATA.md
B-ROLL-CHECKLIST.md
FACT-CHECK-VERIFICATION-SPREADSHEET.md
```

**Never do:**
```
❌ video-projects/loose-folder/
❌ Asking user where to save
❌ Creating without checking location
```

**Always do:**
```
✅ Check PROJECT_STATUS.md first
✅ Use Glob to confirm location
✅ Save to lifecycle folder
✅ Use standard naming
```
