# Phase 1: File Cleanup - Research

**Researched:** 2026-01-19
**Domain:** File organization, naming conventions, duplicate detection
**Confidence:** HIGH

## Summary

This research phase examined the History vs Hype workspace to identify outdated files, duplicates, and naming inconsistencies that should be addressed before other organizational phases. The workspace has a solid foundation with clear lifecycle folders for video projects, but accumulated technical debt in several areas.

**Key findings:**
1. Multiple workflow-related documents exist across directories with varying levels of currency
2. Root-level VTT files should be moved to the transcripts folder
3. The library folder contains many unrelated personal documents mixed with research materials
4. Research folder has identified but unresolved duplicates
5. Naming conventions are documented but inconsistently applied across scripts

**Primary recommendation:** Focus cleanup on (1) consolidating workflow documentation to eliminate confusion about authoritative sources, (2) relocating misplaced files, and (3) enforcing the existing documented naming conventions rather than creating new ones.

## Outdated Files Analysis

### Confirmed Outdated (DELETE)

| File/Path | Why Outdated | Evidence |
|-----------|--------------|----------|
| `_archive-old/` (entire folder) | Contains superseded workflow proposals from Nov 2025 | All 3 files describe improvements already implemented |
| `.claude/README.md` | References `/create-video` command that doesn't exist; workflow described is outdated | START-HERE.md and CLAUDE.md are authoritative |
| `guides/MASTER_WORKFLOW.md` | Superseded by `.claude/REFERENCE/workflow.md` | CLAUDE.md references workflow.md as authoritative |
| `guides/WORKFLOW_GUIDE.md` | Duplicates content in workflow.md | Only 7KB vs 40KB comprehensive version |
| `research/UPDATED_FACT_CHECKING_WORKFLOW.md` | From Nov 2025, superseded by verified workflow | START-HERE.md documents current workflow |
| `research/QUOTE_VERIFICATION_PROTOCOL.md` | Subsumed into fact-checking agents and protocols | .claude/REFERENCE/ has comprehensive coverage |
| `guides/AGENT-IMPROVEMENTS-2025.md` | Historical planning doc, changes implemented | Agents now in .claude/agents/ |
| `templates/START_HERE_COMPLETE_SYSTEM.md` | Nov 2025, superseded by START-HERE.md in root | Older version with outdated commands |
| Root: `prompt_evaluation_templates.json` | Duplicate of `.claude/tools/prompt_evaluation_templates.json` | Same file in two places |
| Root: `nul` | Empty file, likely accidental | 0 bytes, created Jan 19 |

### Files to Review for Deletion

| File/Path | Concern | Action Needed |
|-----------|---------|---------------|
| `guides/CHANNEL_GROWTH_MASTER_SYSTEM.md` | Nov 2025, may overlap with channel-data strategies | Compare with current channel-data files |
| `guides/POLITICIAN_FACTCHECK_SERIES_PLAN.md` | Nov 2025 planning doc | Check if still relevant |
| `channel-data/archive/*` | 8 files from Oct-Nov 2025 | Review for any unique content before cleanup |
| `video-ideas/enhanced_prompt_generator.md` | Sep 2025, very old | Check if superseded |

**Confidence:** HIGH - Based on file dates, CLAUDE.md references, and START-HERE.md documentation hierarchy.

## Duplicate Files Analysis

### Confirmed Duplicates

| Original | Duplicates | Action |
|----------|------------|--------|
| `transcripts/Kraut/The Origins of Russian Authoritarianism.en.vtt` | `transcripts/Kraut - The Origins of Russian Authoritarianism.en.vtt` | Keep organized version, delete root |
| `research/Cambodia-Thailand_NotebookLM-Research-Compilation.md` | `(1).md` and `(2).md` versions in `_archive/` | Merge useful content, delete duplicates |
| `research/_archive/History vs Hype.docx` | `History_vs_Hype.docx` | Keep newest, delete older |
| `transcripts/south-china-sea-map.srt` | `south-china-sea-map-duplicate.srt` | Delete explicit duplicate |
| `transcripts/SPANISH-subtitles-1.srt` | `SPANISH-subtitles-2.srt` | Same file size, likely duplicate |
| `transcripts/essequibo-venezuela-guyana.srt` | `essequibo-venezuela-guyana-ALT-VERSION.srt` | Review then consolidate |
| `transcripts/thailand-cambodia-border.srt` | `thailand-cambodia-border-ALT-VERSION.srt` | Review then consolidate |
| `transcripts/DUPLICATE-alt-version-*.srt` (3 files) | Named as duplicates | Delete all 3 |

### Partial Duplicates (Content Overlap)

| File Group | Issue | Merge Strategy |
|------------|-------|----------------|
| Workflow docs across guides/, research/, .claude/REFERENCE/ | Same topic in 3+ places | Consolidate to .claude/REFERENCE/workflow.md |
| Vance research files in research/ vs video-projects/ | Split across locations | Move all to video-projects/ folder |
| Style guides: author-style.md, scriptwriting-style.md | Separate but related | Keep both - different purposes |

**Confidence:** HIGH - File names and sizes make duplicates obvious.

## Misplaced Files Analysis

### Root-Level Files to Relocate

| File | Current Location | Target Location |
|------|------------------|-----------------|
| 8x `haiti-*.vtt` files | Root | `transcripts/haiti/` (create subfolder) |
| `history-vs-hype-video.en.vtt` | Root | `transcripts/` |
| `peru-protests.en.vtt` | Root | `transcripts/` |
| `reparations-mehdi-biggar.en.vtt` | Root | `transcripts/` |
| 3x `niche-*.vtt` files | Root | `transcripts/niche-research/` (create) |
| `voice-analysis-unscripted.en.vtt` | Root | `transcripts/` |
| `PROJECT_REGISTRY.md` | Root | `video-projects/` or delete if unused |
| `prompt_evaluation_templates.json` | Root | Delete (duplicate in .claude/tools/) |

### Files in Wrong Folders

| File | Current Location | Target Location |
|------|------------------|-----------------|
| `guides/HYBRID_TALKING_HEAD_GUIDE.md` | guides/ | .claude/REFERENCE/ (referenced in CLAUDE.md) |
| `guides/fact-checking-protocol.md` | guides/ | .claude/REFERENCE/ (core workflow) |
| `guides/youtube-comment-response-guide.md` | guides/ | .claude/REFERENCE/ (referenced in CLAUDE.md) |
| `guides/VOICE-GUIDE.md` | guides/ | .claude/REFERENCE/ (style/voice content) |
| Research .docx files in research/ | research/ | Convert to .md or delete if superseded |

**Rationale:** CLAUDE.md establishes `.claude/REFERENCE/` as the authoritative location for reference documentation. Files referenced in CLAUDE.md that live elsewhere create confusion.

**Confidence:** MEDIUM - Moving files requires verifying no broken references.

## Library Folder Assessment

The `library/by-topic/general-history/` folder contains many files that appear unrelated to the channel:

### Unrelated Personal Documents (Sample)
- Multiple CV files: `CV-Europass-20200131-DeBecker-EN.pdf` (8+ copies)
- `Becker - terecht bij professoren en assistenten voor (n.d.).pdf` (8+ copies)
- `Engels - Praktisch Engels (n.d.).pdf` (4 copies)
- Various university study materials in Dutch
- Gaming PDFs (Grim Hollow campaign guide)
- Financial documents (energy certificates)

### Legitimate Research Materials (Keep)
- Mitrokhin Archive volumes
- Cambridge Middle East Studies
- Oxford Medieval Texts
- Academic press publications on relevant topics

**Recommendation:** User should manually review library/by-topic/general-history/ and remove personal files. This appears to be an old sync folder with accumulated personal documents mixed with research materials. Automation cannot safely distinguish personal from research files.

**Confidence:** HIGH - File names clearly indicate non-research content.

## Naming Convention Audit

### Documented Conventions (from FOLDER-STRUCTURE-GUIDE.md)

**Video Project Folders:**
```
video-projects/_IN_PRODUCTION/[number]-[topic-slug-year]/
Example: video-projects/_IN_PRODUCTION/3-kashmir-partition-2025/
```

**Script Files:**
- `FINAL-SCRIPT.md` - THE one to film from
- `02-SCRIPT-DRAFT.md` - During development
- Old versions: `_old-versions/FINAL-SCRIPT-V1.md`

**Research Files:**
```
[Topic]_[Type]_[Date].md
Examples:
- Dark-Ages_NotebookLM-Output_2025-12.md
- Crusades_Preliminary-Research_2025-11.md
```

### Current Violations Found

**In video-projects/_IN_PRODUCTION/:**

| Project | Issue | Fix |
|---------|-------|-----|
| `vance-part-2-review/` | Multiple "final" scripts: FINAL_YOUR_VOICE_SCRIPT.md, FINAL_PRODUCTION_SCRIPT.md | Consolidate to single FINAL-SCRIPT.md |
| `6-bir-tawil-2025/` | SCRIPT-V4-FINAL.md (wrong naming) | Rename to FINAL-SCRIPT.md |
| `9-communism-definition-2025/` | FINAL-SCRIPT-V2-EDITED.md | Rename to FINAL-SCRIPT.md |
| `10-dark-ages-2025/` | FINAL-SCRIPT-V2-EDITED.md | Rename to FINAL-SCRIPT.md |
| `11-industrial-revolution-2025/` | FINAL-SCRIPT-V2-REVISED.md | Rename to FINAL-SCRIPT.md |
| `13-belize-icj-endgame-2025/` | V1, V2, V3 all exist | Keep V3, archive others |
| `czechoslovakia-velvet-divorce-2025/` | Missing number prefix | Add number prefix |
| `PERU/` | ALL CAPS, no number, no year | Rename completely |
| Two `22-guadalupe-hidalgo-2025/` folders | Duplicate numbering with 22-iran folders | Renumber one |

**In transcripts/:**
- Mix of formats: `topic-name.en.vtt`, `Topic - Name.en.vtt`, `topic_name.srt`
- Creator subfolders have different naming: `Kraut/` vs flat files with `kraut-` prefix

**In research/:**
- Inconsistent naming: underscores vs hyphens, some with dates, most without

**Confidence:** HIGH - Compared against documented conventions in FOLDER-STRUCTURE-GUIDE.md.

## Don't Hand-Roll

Problems with existing solutions in this workspace:

| Problem | Existing Solution | Why Use It |
|---------|-------------------|------------|
| Knowing where to put files | FOLDER-STRUCTURE-GUIDE.md | Already documented, Claude knows it |
| Script versioning | _old-versions/ subfolder pattern | Documented in guide, prevents confusion |
| Workflow reference | START-HERE.md hierarchy | Tier 1/2/3 authority established |
| Transcript organization | transcripts/ with creator subfolders | Pattern exists for Kraut, Shaun, etc. |

**Key insight:** The conventions already exist and are well-documented. The problem is enforcement, not definition.

## Common Pitfalls

### Pitfall 1: Deleting Files Still Referenced

**What goes wrong:** A file is deleted but CLAUDE.md or another doc references it
**Why it happens:** References scattered across many documentation files
**How to avoid:** Search for file references before deletion
**Warning signs:** Broken links in documentation, Claude asking for missing files

### Pitfall 2: Moving Files Without Updating References

**What goes wrong:** File moved but old path hardcoded elsewhere
**Why it happens:** Multiple docs reference the same file
**How to avoid:** Grep for file path before moving, update all references
**Warning signs:** 404s in documentation, "file not found" errors

### Pitfall 3: Merging Duplicates Without Checking Content

**What goes wrong:** "Duplicate" files actually have different content
**Why it happens:** Files diverged after initial copy
**How to avoid:** Diff files before merge, check file sizes and dates
**Warning signs:** Different file sizes, different modification dates

### Pitfall 4: Over-Organizing Active Projects

**What goes wrong:** Disrupting active work to enforce conventions
**Why it happens:** Desire for consistency overrides practicality
**How to avoid:** Only touch IN_PRODUCTION projects that are stalled
**Warning signs:** User complains about lost work, files in wrong state

## Architecture Patterns

### Current Structure (Working Well)

```
video-projects/
├── _IN_PRODUCTION/      # Active work
├── _READY_TO_FILM/      # Approved scripts
├── _ARCHIVED/           # Published/cancelled
├── _ANALYTICS/          # Performance data
├── _CORRECTIONS-LOG.md  # Error tracking
└── PROJECT_STATUS.md    # Overview

.claude/
├── agents/              # Agent definitions
├── commands/            # Slash commands
├── REFERENCE/           # Authoritative docs
├── skills/              # Skill definitions
├── templates/           # Project templates
├── tools/               # Scripts and utilities
├── _ARCHIVE/            # Deprecated .claude files
└── PROMPTS/             # Research prompts
```

### Recommended Additions

```
transcripts/
├── creator-name/        # Creator-specific (Kraut/, Shaun/)
├── project-specific/    # haiti/, peru/ (group by research topic)
└── [flat files]         # One-off transcripts

research/
├── active/              # Currently being used
├── completed/           # Research for published videos
├── _archive/            # Old duplicates, superseded
└── comment-responses/   # YouTube comment research
```

## State of the Art

### What Changed Recently (2025-2026)

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Multiple workflow docs | Single authoritative workflow.md | Dec 2025 | Eliminates confusion |
| /create-video command | /new-video command | Nov 2025 | .claude/README.md outdated |
| Scattered style guides | Consolidated in REFERENCE/ | Dec 2025 | Multiple files still in guides/ |
| No documentation hierarchy | Tier 1/2/3 system | Jan 2026 | START-HERE.md authoritative |

### Deprecated Items

| Item | Why Deprecated | What Replaced It |
|------|----------------|------------------|
| `guides/WORKFLOW_GUIDE.md` | Too brief, incomplete | `.claude/REFERENCE/workflow.md` |
| `templates/START_HERE_COMPLETE_SYSTEM.md` | Nov 2025 version | `START-HERE.md` (root) |
| `/create-video` command | Command doesn't exist | `/new-video` |
| `.claude/CORE-WORKFLOW-SCRIPTWRITING-FACTCHECKING.md` | Moved to archive | Already in _ARCHIVE |

## Open Questions

### Question 1: Transcript Organization Strategy

**What we know:**
- Some creators have subfolders (Kraut/, Shaun/)
- Some transcripts are flat files
- Root has 8 haiti-related VTTs

**What's unclear:**
- Should ALL transcripts be in creator subfolders?
- Should project-specific transcripts (haiti research) have their own structure?
- What about transcripts for the channel's own videos?

**Recommendation:** Create project-specific subfolders for grouped research (haiti/, peru/), maintain creator subfolders for style reference, flatten remaining one-offs.

### Question 2: guides/ Folder Future

**What we know:**
- 15 files in guides/
- Many overlap with .claude/REFERENCE/
- Some referenced in CLAUDE.md

**What's unclear:**
- Should guides/ be eliminated entirely?
- Are there files in guides/ that shouldn't move to REFERENCE?

**Recommendation:** Move workflow/style/reference docs to .claude/REFERENCE/, keep guides/ only for non-Claude-specific guides (BACKUP-GUIDE.md, COPYRIGHT_FREE_MUSIC_GUIDE.md).

### Question 3: Library Folder Cleanup Scope

**What we know:**
- Contains legitimate academic sources
- Also contains unrelated personal files
- Very large (many PDFs)

**What's unclear:**
- Is this the user's main PDF library synced from elsewhere?
- Would deleting files here affect other systems?
- Scope of personal file cleanup

**Recommendation:** Flag for user manual review rather than automated cleanup.

## Sources

### Primary (HIGH confidence)
- `CLAUDE.md` - Current channel documentation (reviewed Jan 2026)
- `START-HERE.md` - Workflow quick start (reviewed Jan 2026)
- `.claude/REFERENCE/FOLDER-STRUCTURE-GUIDE.md` - Naming conventions
- `.claude/REFERENCE/workflow.md` - Authoritative workflow doc
- `video-projects/PROJECT_STATUS.md` - Current project state

### Secondary (MEDIUM confidence)
- File system analysis via Glob and ls commands
- File modification dates for recency assessment
- Cross-reference between documented conventions and actual files

### Tertiary (LOW confidence)
- Assumptions about which files are "outdated" based on dates alone
- Library folder assessment (user context unknown)

## Metadata

**Confidence breakdown:**
- Outdated files: HIGH - Cross-referenced against current docs
- Duplicates: HIGH - File names/sizes make obvious
- Misplaced files: MEDIUM - Requires path update verification
- Naming violations: HIGH - Compared against documented conventions
- Library assessment: MEDIUM - Requires user input for personal files

**Research date:** 2026-01-19
**Valid until:** 2026-02-19 (30 days - workspace structure relatively stable)
