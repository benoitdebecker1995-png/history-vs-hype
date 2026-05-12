# Project Folder Cleanup Proposal

**Current Status:** 13 files, 248KB total
**Goal:** Streamline for YouTube production workflow

---

## Current File Audit

### ✅ ESSENTIAL - Keep in Root (Production Files)
These are actively needed for filming/editing:

1. **SCRIPT-DRAFT-02-FINAL.md** (25K) → Rename to `FINAL-SCRIPT.md`
2. **B-ROLL-CHECKLIST.md** (26K) → Keep as-is
3. **DIY-ASSET-GUIDE.md** (16K) → Keep as-is
4. **FACT-CHECK-VERIFICATION.md** (18K) → Keep as-is

**Total: 4 files, 85KB**

---

### 📁 USEFUL REFERENCE - Move to `_research/` Subfolder
Background research useful for revisions/comments but not needed for filming:

5. **RESEARCH-SUMMARY.md** (25K) → Move to `_research/`
6. **PROJECT-BRIEF.md** (7.3K) → Move to `_research/`
7. **NOTEBOOKLM-PROMPTS.md** (19K) → Move to `_research/`
8. **NOTEBOOKLM-SOURCE-LIST.md** (15K) → Move to `_research/`

**Total: 4 files, 66KB**

---

### ❌ DELETE - Redundant/Superseded
These can be safely deleted:

9. **SCRIPT-DRAFT-01.md** (20K) → Delete (superseded by DRAFT-02-FINAL)
10. **CLAIMS-TO-VERIFY.md** (21K) → Delete (now in FACT-CHECK-VERIFICATION.md)
11. **VERIFICATION-ISSUES-REPORT.md** (15K) → Delete (debugging doc from today)
12. **VERIFICATION-RESOLUTION.md** (16K) → Delete (debugging doc from today)
13. **WORKFLOW-FIX-SUMMARY.md** (5.8K) → Delete (workflow fix completed)

**Total: 5 files, 78KB to delete**

---

## Proposed Final Structure

```
video-projects/_IN_PRODUCTION/4-crusades-fact-check-2025/
│
├── FINAL-SCRIPT.md (25K) ← Ready to film from this
├── FACT-CHECK-VERIFICATION.md (18K) ← All claims verified
├── B-ROLL-CHECKLIST.md (26K) ← Visual assets needed
├── DIY-ASSET-GUIDE.md (16K) ← How to create B-roll
│
└── _research/ (subfolder for reference)
    ├── RESEARCH-SUMMARY.md (25K)
    ├── PROJECT-BRIEF.md (7.3K)
    ├── NOTEBOOKLM-PROMPTS.md (19K)
    └── NOTEBOOKLM-SOURCE-LIST.md (15K)
```

**Result:**
- **Root folder:** 4 essential production files (85KB)
- **_research/ folder:** 4 reference files (66KB)
- **Total:** 8 files, 151KB (down from 13 files, 248KB)
- **Space saved:** 97KB (39% reduction)
- **Clutter removed:** 5 redundant files deleted

---

## Why This Structure Works for YouTube Production

### What You See When Opening the Folder:
```
FINAL-SCRIPT.md ← "This is what I film"
FACT-CHECK-VERIFICATION.md ← "This proves everything is accurate"
B-ROLL-CHECKLIST.md ← "This is what visuals I need"
DIY-ASSET-GUIDE.md ← "This is how I create the visuals"
_research/ ← "Background stuff if I need it"
```

### Clear Workflow:
1. **Pre-filming:** Read FINAL-SCRIPT.md, check B-ROLL-CHECKLIST.md
2. **Creating assets:** Use DIY-ASSET-GUIDE.md
3. **If questioned:** Check FACT-CHECK-VERIFICATION.md for sources
4. **For revisions/comments:** Dive into _research/ folder

### No Confusion:
- ❌ No "which script is final?" (only one script in root)
- ❌ No "is this verified?" (one fact-check doc)
- ❌ No "what are these debugging files?" (deleted)
- ✅ Everything in root is production-ready

---

## Missing Production Files (Should Create)

Based on FOLDER-STRUCTURE-GUIDE.md, you're missing:

### 🆕 YOUTUBE-METADATA.md
**Should contain:**
- Optimized title
- Full description with timestamps
- Tags list
- Thumbnail specs
- Upload checklist

**Current status:** Metadata is scattered in script comments
**Recommendation:** Extract into dedicated file

---

## Comparison to Fuentes Project

**Fuentes project has the SAME problem!**

**Current state:** 22 files, 532KB

**Essential production files:**
- 09-script-FINAL-CORRECTED.md (24K)
- FACT-CHECK-VERIFICATION.md (6.7K)
- B-ROLL-CHECKLIST.md (4.8K)
- YOUTUBE-METADATA.md (5.5K)
- FUENTES-EDITING-GUIDE.md (27K)
- fuentes claims checked.srt (19K) - subtitle file

**Old iterations (should delete/archive):**
- 06-script-draft.md, 07-script-REVISED.md, 08-script-CONVERSATIONAL.md (3 old drafts!)
- GROK-FEEDBACK-ASSESSMENT.md, GROK-RESEARCH-RAW.md

**Research files (should move to `_research/`):**
- All the 00-04 numbered files
- notebooklm output fuentes.md (192KB! - huge file)
- FINAL-NOTEBOOKLM-SOURCES.md, LEAN-NOTEBOOKLM-LIST.md, etc.

**Fuentes could go from 22 files → 6 production files + _research/ folder**

**Both projects need the same cleanup approach.**

---

## Recommended Actions

### Option A: Full Cleanup (Recommended)
```bash
# 1. Rename final script
mv SCRIPT-DRAFT-02-FINAL.md FINAL-SCRIPT.md

# 2. Create research subfolder
mkdir _research

# 3. Move research files
mv RESEARCH-SUMMARY.md _research/
mv PROJECT-BRIEF.md _research/
mv NOTEBOOKLM-PROMPTS.md _research/
mv NOTEBOOKLM-SOURCE-LIST.md _research/

# 4. Delete redundant files
rm SCRIPT-DRAFT-01.md
rm CLAIMS-TO-VERIFY.md
rm VERIFICATION-ISSUES-REPORT.md
rm VERIFICATION-RESOLUTION.md
rm WORKFLOW-FIX-SUMMARY.md
```

**Result:** Clean, focused production folder

---

### Option B: Minimal Cleanup (Conservative)
```bash
# 1. Just delete debugging files
rm VERIFICATION-ISSUES-REPORT.md
rm VERIFICATION-RESOLUTION.md
rm WORKFLOW-FIX-SUMMARY.md

# 2. Delete old script draft
rm SCRIPT-DRAFT-01.md
```

**Result:** Removes obvious clutter but keeps all content files

---

### Option C: Archive Instead of Delete (Safest)
```bash
# Create archive folder
mkdir _archive

# Move everything we'd otherwise delete
mv SCRIPT-DRAFT-01.md _archive/
mv CLAIMS-TO-VERIFY.md _archive/
mv VERIFICATION-ISSUES-REPORT.md _archive/
mv VERIFICATION-RESOLUTION.md _archive/
mv WORKFLOW-FIX-SUMMARY.md _archive/

# Move research to subfolder
mkdir _research
mv RESEARCH-SUMMARY.md _research/
mv PROJECT-BRIEF.md _research/
mv NOTEBOOKLM-PROMPTS.md _research/
mv NOTEBOOKLM-SOURCE-LIST.md _research/
mv NOTEBOOKLM-SOURCE-LIST.md _research/

# Rename final script
mv SCRIPT-DRAFT-02-FINAL.md FINAL-SCRIPT.md
```

**Result:** Nothing deleted, but organized out of sight

---

## My Recommendation: Option A (Full Cleanup)

**Why:**
1. **Old drafts have no value** - You have the final version
2. **Debugging docs were just for today** - Workflow is fixed now
3. **Research should be in subfolder** - Keeps root clean
4. **FINAL-SCRIPT.md naming is clear** - No ambiguity about which file to use

**When ready to film:**
- Open folder
- See 4 files: script, fact-check, b-roll list, DIY guide
- Everything else tucked away in `_research/`

---

## Do You Want Me To:

**A.** Execute Option A (full cleanup) ✅ Recommended
**B.** Execute Option B (minimal cleanup)
**C.** Execute Option C (archive everything, delete nothing)
**D.** Something else (tell me what)

I can run the commands now if you approve.
