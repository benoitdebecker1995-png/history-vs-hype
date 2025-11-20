# Project-Wide Cleanup Proposal
## Streamlining History vs Hype for YouTube Production

**Current Status:** Scattered files across multiple redundant folders
**Goal:** Clean, focused structure optimized for making YouTube videos

---

## PROBLEMS IDENTIFIED

### 1. Redundant Archive Folders
**Problem:** Two places for old content
- `archive/` - 29 old Claude Code artifacts (compass_artifact files)
- `scripts-archive/` - Old video scripts (KGB, Kosovo, Sahel, etc.)
- `video-projects/_ARCHIVED/` - Meant for archived video projects (currently empty)

**Confusion:** Where should old stuff go?

---

### 2. Redundant Research Folders
**Problem:** Research in two places
- `research/` - 32 old research files + active/completed subfolders
- `video-projects/_IN_PRODUCTION/[project]/` - Each project has its own research

**Confusion:** Should research be centralized or per-project?

---

### 3. Orphaned Scripts Folder
**Problem:** `scripts/` folder exists separately from `video-projects/`
- Has 3 old completed scripts (Lagertha, Protocols, Belize-Guatemala)
- Has `automation/` subfolder

**Confusion:** Is this still used? Conflicts with `video-projects/` workflow

---

### 4. Unclear Planning Folder
**Problem:** `planning/` has only 3 files
- CHANNEL_GROWTH_MASTER_SYSTEM.md
- POLITICIAN_FACTCHECK_SERIES_PLAN.md
- WORKFLOW_GUIDE.md

**Confusion:** Should these be in `guides/` instead?

---

### 5. Outdated MASTER_INDEX.md
**Problem:** Last updated 2025-11-10, references old projects
- Mentions "sykes-picot-2025" and "vance-part-2-review"
- Actual current projects: "3-fuentes-fact-check-2025" and "4-crusades-fact-check-2025"

---

## RECOMMENDED STRUCTURE

### Core Principle: **Production-Focused Hierarchy**

```
History vs Hype/
│
├── 📄 README.md ← Quick channel overview
├── 📄 CLAUDE.md ← Instructions for Claude Code
│
├── 📁 .claude/ ← Claude Code configuration (keep as-is)
│
├── 📁 video-projects/ ← **PRIMARY WORKSPACE**
│   ├── _IN_PRODUCTION/ ← Active video projects
│   ├── _READY_TO_FILM/ ← Finalized scripts
│   └── _ARCHIVED/ ← Published/cancelled videos
│
├── 📁 library/ ← Academic books & sources for NotebookLM (keep as-is)
│   ├── by-topic/
│   └── for-notebooklm/
│
├── 📁 guides/ ← Production workflows & reference
│   ├── MASTER_WORKFLOW.md
│   ├── fact-checking-protocol.md
│   ├── HYBRID_TALKING_HEAD_GUIDE.md
│   └── [other production guides]
│
├── 📁 templates/ ← Reusable project templates
│
├── 📁 channel-data/ ← Analytics, performance data
│
└── 📁 _archive-old/ ← Everything deprecated (hidden)
    ├── old-claude-artifacts/
    ├── old-scripts/
    ├── old-research/
    └── old-planning/
```

---

## CLEANUP ACTIONS

### Phase 1: Delete Junk ❌

**Delete `archive/` folder** (29 old Claude artifacts - no value)
```bash
rm -rf "archive/"
```

**Saved:** Clutter removed, no useful content lost

---

### Phase 2: Consolidate Archives 📦

**Move old scripts to video-projects/_ARCHIVED/**
```bash
# Move scripts-archive contents
mv "scripts-archive/kgb-scripts" "video-projects/_ARCHIVED/old-kgb/"
mv "scripts-archive/kosovo-scripts" "video-projects/_ARCHIVED/old-kosovo/"
mv "scripts-archive/sahel-crisis" "video-projects/_ARCHIVED/old-sahel/"
mv "scripts-archive/other-old-scripts" "video-projects/_ARCHIVED/old-misc/"

# Move orphaned scripts from scripts/
mv "scripts/Lagertha_Script_Final.md" "video-projects/_ARCHIVED/old-lagertha/"
mv "scripts/Protocols_Autocue_Script.md" "video-projects/_ARCHIVED/old-protocols/"
mv "scripts/Belize_Guatemala_Dispute_Complete_Video_Strategy.md" "video-projects/_ARCHIVED/old-belize/"

# Delete now-empty scripts-archive folder
rm -rf "scripts-archive/"
```

**Result:** All old video content in ONE place (video-projects/_ARCHIVED/)

---

### Phase 3: Consolidate Research 📚

**Option A (Recommended): Delete Old Research**
- All old research in `research/` is for completed/abandoned projects
- Current projects have their own research in video-projects/
- Old research has no value (can't be reused for different topics)

```bash
# Archive old research (don't delete yet, just in case)
mkdir "_archive-old"
mv "research/" "_archive-old/old-research/"
```

**Option B (Conservative): Keep General Research**
- Rename `research/` to `research-archive/` to make it clear it's old
- Keep only genuinely reusable research (sources-reference.md, QUOTE_VERIFICATION_PROTOCOL.md)
- Delete project-specific research files

---

### Phase 4: Consolidate Planning 📋

**Move planning docs to guides/**
```bash
mv "planning/CHANNEL_GROWTH_MASTER_SYSTEM.md" "guides/"
mv "planning/POLITICIAN_FACTCHECK_SERIES_PLAN.md" "guides/"
mv "planning/WORKFLOW_GUIDE.md" "guides/"

# Delete empty planning folder
rm -rf "planning/"
```

**Result:** All workflow/planning guidance in ONE place (guides/)

---

### Phase 5: Clean Up Root Files 🧹

**Current root files:**
- AGENT-IMPROVEMENTS-2025.md
- BACKUP-GUIDE.md
- CLAUDE.md ← keep
- MASTER_INDEX.md
- VOICE-GUIDE.md
- why the crusades were awesome.txt ← what is this?

**Move to appropriate locations:**
```bash
# Move to guides/
mv "AGENT-IMPROVEMENTS-2025.md" "guides/"
mv "BACKUP-GUIDE.md" "guides/"
mv "VOICE-GUIDE.md" "guides/"

# Update and keep
# MASTER_INDEX.md → update to reflect new structure
# CLAUDE.md → keep as-is (main instructions)

# Investigate/delete
# "why the crusades were awesome.txt" → probably reference material, move to crusades project?
```

**Result:** Clean root folder with only essential navigation files

---

### Phase 6: Fix video-projects/ Clutter 📂

**Apply cleanup to each project folder:**

**For Fuentes (3-fuentes-fact-check-2025/):**
```bash
# Delete old drafts
rm 06-script-draft.md
rm 07-script-REVISED.md
rm 08-script-CONVERSATIONAL.md

# Move research to subfolder
mkdir _research
mv 00-* _research/
mv 01-* _research/
mv 02-* _research/
mv 03-* _research/
mv 04-* _research/
mv FINAL-NOTEBOOKLM-SOURCES.md _research/
mv "notebooklm output fuentes.md" _research/
mv GROK-* _research/
mv LEAN-NOTEBOOKLM-LIST.md _research/

# Rename final script
mv 09-script-FINAL-CORRECTED.md FINAL-SCRIPT.md

# Keep in root:
# FINAL-SCRIPT.md
# FACT-CHECK-VERIFICATION.md
# B-ROLL-CHECKLIST.md
# YOUTUBE-METADATA.md
# FUENTES-EDITING-GUIDE.md
# fuentes claims checked.srt
```

**For Crusades (4-crusades-fact-check-2025/):**
```bash
# Already mostly clean from today's work
# Just need to move RESEARCH-SUMMARY.md to _research/ folder

mkdir _research
mv RESEARCH-SUMMARY.md _research/
mv PROJECT-BRIEF.md _research/
mv NOTEBOOKLM-PROMPTS.md _research/
mv NOTEBOOKLM-SOURCE-LIST.md _research/
mv CLEANUP-PROPOSAL.md _research/ # today's work
rm SCRIPT-DRAFT-01.md # old iteration

# Rename final script
mv SCRIPT-DRAFT-02-FINAL.md FINAL-SCRIPT.md
```

---

## FINAL STRUCTURE AFTER CLEANUP

```
History vs Hype/
│
├── 📄 README.md (channel overview)
├── 📄 CLAUDE.md (Claude instructions)
│
├── 📁 .claude/ (configuration - untouched)
├── 📁 .git/ (version control - untouched)
│
├── 📁 video-projects/
│   │
│   ├── _IN_PRODUCTION/
│   │   ├── 3-fuentes-fact-check-2025/
│   │   │   ├── FINAL-SCRIPT.md
│   │   │   ├── FACT-CHECK-VERIFICATION.md
│   │   │   ├── B-ROLL-CHECKLIST.md
│   │   │   ├── YOUTUBE-METADATA.md
│   │   │   ├── FUENTES-EDITING-GUIDE.md
│   │   │   ├── fuentes claims checked.srt
│   │   │   └── _research/ (10+ files moved here)
│   │   │
│   │   └── 4-crusades-fact-check-2025/
│   │       ├── FINAL-SCRIPT.md
│   │       ├── FACT-CHECK-VERIFICATION.md
│   │       ├── B-ROLL-CHECKLIST.md
│   │       ├── DIY-ASSET-GUIDE.md
│   │       └── _research/ (4 files moved here)
│   │
│   ├── _READY_TO_FILM/ (currently empty - ready for next video)
│   │
│   └── _ARCHIVED/
│       ├── old-kgb/
│       ├── old-kosovo/
│       ├── old-sahel/
│       ├── old-protocols/
│       ├── old-lagertha/
│       ├── old-belize/
│       └── old-misc/
│
├── 📁 library/ (academic sources - untouched)
│   ├── by-topic/
│   └── for-notebooklm/
│
├── 📁 guides/
│   ├── MASTER_WORKFLOW.md
│   ├── fact-checking-protocol.md
│   ├── HYBRID_TALKING_HEAD_GUIDE.md
│   ├── AGENT-IMPROVEMENTS-2025.md (moved from root)
│   ├── BACKUP-GUIDE.md (moved from root)
│   ├── VOICE-GUIDE.md (moved from root)
│   ├── CHANNEL_GROWTH_MASTER_SYSTEM.md (from planning/)
│   ├── POLITICIAN_FACTCHECK_SERIES_PLAN.md (from planning/)
│   └── WORKFLOW_GUIDE.md (from planning/)
│
├── 📁 templates/ (project templates - untouched)
│
├── 📁 channel-data/ (analytics - untouched)
│
├── 📁 transcripts/ (subtitle files - untouched)
│
├── 📁 video-ideas/ (topic brainstorming - untouched)
│
└── 📁 _archive-old/ (deprecated stuff - hidden from view)
    └── old-research/ (32 old research files from research/)
```

---

## BENEFITS

### Before Cleanup:
- 13 top-level folders
- Scattered archives in 3 places
- Research duplicated in 2 places
- Scripts in 3 different locations
- Cluttered project folders (22 files in Fuentes!)
- Unclear which files are current

### After Cleanup:
- 8 top-level folders (focused)
- All archives in video-projects/_ARCHIVED/
- Research only in project folders
- Scripts only in video-projects/
- Clean project folders (6 files in root, research tucked away)
- Crystal clear: FINAL-SCRIPT.md is what you film from

### When Opening video-projects/_IN_PRODUCTION/3-fuentes-fact-check-2025/:
```
✅ FINAL-SCRIPT.md ← This is what I film
✅ FACT-CHECK-VERIFICATION.md ← This proves it's accurate
✅ B-ROLL-CHECKLIST.md ← This is what visuals I need
✅ YOUTUBE-METADATA.md ← This is title/description/tags
✅ FUENTES-EDITING-GUIDE.md ← This is shot-by-shot guide
✅ fuentes claims checked.srt ← Subtitle file
✅ _research/ ← Background stuff (out of sight)
```

**No confusion. No clutter. Production-ready.**

---

## EXECUTION PLAN

### Recommended Order:
1. **Phase 1** (delete junk) - Safe, no value lost
2. **Phase 6** (clean project folders) - Immediate benefit
3. **Phase 2** (consolidate old videos) - Organize archives
4. **Phase 5** (clean root) - Tidy up top level
5. **Phase 4** (consolidate planning) - Merge guides
6. **Phase 3** (archive old research) - Move to _archive-old/ (don't delete yet)

### Time Required:
- **Automated script:** 5 minutes
- **Manual review:** 15 minutes
- **Total:** ~20 minutes

---

## DO YOU WANT ME TO:

**A.** Create bash script to execute all phases automatically
**B.** Execute phases manually (with your approval at each step)
**C.** Start with just Phase 1 + Phase 6 (safest - delete junk + clean project folders)
**D.** Something else (tell me what)

**I recommend Option C** - Delete obvious junk, clean project folders, see how it feels before doing more aggressive consolidation.
