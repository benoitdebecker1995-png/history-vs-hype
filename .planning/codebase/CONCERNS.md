# Codebase Concerns

**Analysis Date:** 2026-01-19

## Tech Debt

**Script Version Proliferation:**
- Issue: Multiple "final" scripts exist for the same video project with inconsistent naming
- Files:
  - `video-projects/_IN_PRODUCTION/vance-part-2-review/FINAL_YOUR_VOICE_SCRIPT.md`
  - `video-projects/_IN_PRODUCTION/vance-part-2-review/FINAL_PRODUCTION_SCRIPT.md`
  - `video-projects/_IN_PRODUCTION/1-somaliland-2025/FINAL-FILMING-SCRIPT.md`
  - `video-projects/_IN_PRODUCTION/1-somaliland-2025/FILMING-SCRIPT-FINAL.md`
  - `video-projects/_IN_PRODUCTION/6-bir-tawil-2025/FINAL-SCRIPT.md` AND `_old-versions/SCRIPT-V3-FINAL.md`
  - `video-projects/_IN_PRODUCTION/13-belize-icj-endgame-2025/FINAL-SCRIPT.md` AND `_old-versions/FINAL-SCRIPT-V1.md`, `FINAL-SCRIPT-V2.md`
  - `video-projects/_IN_PRODUCTION/19-flat-earth-medieval-2025/FINAL-SCRIPT.md`, `FINAL-SCRIPT-V2.md`, `FINAL-SCRIPT-V3.md`
- Impact: Confusion about which script is authoritative; risk of filming from wrong version
- Fix approach: Consolidate to single `FINAL-SCRIPT.md` per project; archive old versions to `_old-versions/` subdirectory; documented in `video-projects/PROJECT_STATUS.md` lines 242-251

**Naming Convention Inconsistency:**
- Issue: Mixed naming conventions across script files
- Files: Throughout `video-projects/_IN_PRODUCTION/`
  - Some use `FINAL-SCRIPT.md` (correct per CLAUDE.md)
  - Others use `FINAL-SCRIPT-V2-EDITED.md`, `FINAL-SCRIPT-V2-REVISED.md`
  - vance-part-2 uses `FINAL_YOUR_VOICE_SCRIPT.md`, `FINAL_PRODUCTION_SCRIPT.md` (underscores, different naming)
- Impact: Harder to locate the correct file; breaks pattern-based tooling
- Fix approach: Standardize to `FINAL-SCRIPT.md` only; if multiple revisions needed, use `_old-versions/` subdirectory

**Stale PROJECT_STATUS.md:**
- Issue: `video-projects/PROJECT_STATUS.md` shows "Last Updated: 2025-12-22" but lists only 15 active projects; actual `_IN_PRODUCTION/` contains 30+ folders
- Files: `video-projects/PROJECT_STATUS.md`
- Impact: Project tracker is incomplete; new projects (21-haiti, 22-iran-1953-coup, etc.) not tracked
- Fix approach: Update PROJECT_STATUS.md to reflect all current projects; consider automation

**Hardcoded Paths in Python Scripts:**
- Issue: Library organization scripts contain absolute paths
- Files:
  - `library/organize_books.py` line 14-15: `DOWNLOADS = Path(r"C:\Users\benoi\Downloads")`, `LIBRARY = Path(r"C:\Users\benoi\Documents\History vs Hype\library\by-topic")`
- Impact: Scripts will fail on different machines or if directory structure changes
- Fix approach: Use relative paths or environment variables; add configuration file

**Duplicate Project Numbering:**
- Issue: Multiple projects share same number prefix
- Files:
  - `video-projects/_IN_PRODUCTION/22-guadalupe-hidalgo-2025/`
  - `video-projects/_IN_PRODUCTION/22-iran-1953-coup-2025/`
  - `video-projects/_IN_PRODUCTION/22-iran-protests-history-2025/`
- Impact: Ambiguous project references; potential merge conflicts
- Fix approach: Reassign unique numbers; update any references

---

## Known Bugs

**Pre-Publication Error Pattern (Documented):**
- Symptoms: Facts verified from memory instead of source; dates/titles slightly wrong
- Files: `video-projects/_CORRECTIONS-LOG.md` lines 10-33
- Trigger: Copying facts from memory instead of verbatim from sources
- Workaround: RULE 4 added to `script-writer-v2.md` requiring exact quotes for dates/names/occupations

**Empty File in Root:**
- Symptoms: Zero-byte file exists in repository root
- Files: `nul` (0 bytes) in `D:\History vs Hype\`
- Trigger: Likely accidental Windows NUL device redirect
- Workaround: Delete the file

---

## Security Considerations

**eval() Vulnerability Fixed:**
- Risk: Previously used `eval()` to parse FFmpeg frame rates
- Files: `tools/history-clip-tool/src/core/video_processor.py` (fixed in v2.0)
- Current mitigation: Replaced with safe string parsing per `tools/history-clip-tool/IMPROVEMENTS.md` lines 16-35
- Recommendations: Audit other Python files for similar patterns

**Broad Permission Grants in settings.local.json:**
- Risk: Very permissive Bash command allowlist
- Files: `.claude/settings.local.json` lines 1-108
- Current mitigation: Permissions are scoped to specific tools (yt-dlp, python, etc.)
- Recommendations: Review and prune unused permissions; consider more specific patterns instead of wildcards

---

## Performance Bottlenecks

**No Major Performance Issues Detected:**
- Problem: Not applicable for content production repository
- Files: N/A
- Cause: This is primarily a documentation/content workflow repository, not a compute-intensive application
- Improvement path: N/A

---

## Fragile Areas

**Verified Workflow Quality Gates:**
- Files:
  - `CLAUDE.md` lines 193-228
  - `.claude/REFERENCE/FACT-CHECK-SIMPLIFICATION-RULES.md`
  - `.claude/REFERENCE/FACT-CHECK-VERIFICATION-PROTOCOL.md`
- Why fragile: Quality depends on human following the multi-phase workflow; easy to skip verification steps
- Safe modification: Any changes to workflow must update CLAUDE.md, VERIFIED-WORKFLOW-QUICK-REFERENCE.md, and agent files simultaneously
- Test coverage: Manual process; no automated verification

**Agent Dependencies:**
- Files: `.claude/agents/*.md`
- Why fragile: Agents reference specific file patterns and locations; if folder structure changes, agents may fail
- Safe modification: Update FOLDER-STRUCTURE-GUIDE.md and all agent files when changing folder conventions
- Test coverage: None

**Slash Commands:**
- Files: `.claude/commands/*.md`
- Why fragile: Commands reference other commands and skills; circular dependencies possible
- Safe modification: Check all command files for references before modifying
- Test coverage: None

---

## Scaling Limits

**Project Folder Growth:**
- Current capacity: 30+ projects in `_IN_PRODUCTION/`
- Limit: No technical limit, but manual tracking becomes unwieldy
- Scaling path: Consider database or automated tracking; move completed projects to `_ARCHIVED/` more frequently

**NotebookLM Source Management:**
- Current capacity: 50 sources per notebook (Gemini 2.0 limitation)
- Limit: 2M token context window
- Scaling path: Split large projects into multiple notebooks per CLAUDE.md guidance

---

## Dependencies at Risk

**yt-dlp Tool:**
- Risk: External binary stored in `tools/yt-dlp.exe`; may become outdated
- Impact: YouTube transcript fetching may break
- Migration plan: Update regularly; consider npm package instead

**NotebookLM (Gemini 2.0 Flash):**
- Risk: External Google service; could change API or features
- Impact: Core research workflow depends on it
- Migration plan: Document workflow steps so alternative tools could substitute

---

## Missing Critical Features

**No Automated Fact-Check Verification:**
- Problem: All fact-checking is manual; relies on human following protocol
- Blocks: Cannot guarantee all claims are verified before filming
- Current workaround: Manual checklists in VERIFIED-WORKFLOW-QUICK-REFERENCE.md

**No Version Control for Scripts:**
- Problem: Multiple script versions manually managed; no diff tracking
- Blocks: Cannot easily see what changed between versions
- Current workaround: Manual archiving to `_old-versions/` subdirectories

**No Project Template Automation:**
- Problem: New projects require manual file creation
- Blocks: Inconsistent project structure setup
- Current workaround: Templates in `templates/project-templates/` must be manually copied

---

## Test Coverage Gaps

**No Automated Tests for Python Tools:**
- What's not tested: `library/organize_books.py`, `library/auto_rename_books.py`, `.claude/tools/get-transcript.py`, `tools/prompt_evaluation.py`
- Files: Listed above
- Risk: Refactoring could break functionality silently
- Priority: Low (utility scripts, not critical path)

**No Tests for history-clip-tool:**
- What's not tested: `tools/history-clip-tool/tests/` directory exists but unclear coverage
- Files: `tools/history-clip-tool/src/**/*.py`
- Risk: Video processing changes could break export functionality
- Priority: Medium (affects clip export workflow)

**No Validation for Markdown Templates:**
- What's not tested: Template files in `.claude/templates/` and `templates/`
- Files: All `.md` templates
- Risk: Broken template syntax could confuse agents/commands
- Priority: Low (human-readable, easily caught)

---

## Archive/Cleanup Needed

**Old Archive Directories:**
- Files:
  - `_archive-old/` in root (contains workflow improvement proposals from Nov 2025)
  - `video-projects/_ARCHIVED/old-*` directories (8 archived project families)
  - `.claude/_ARCHIVE/` (contains superseded documentation)
- Impact: Increases cognitive load when navigating; unclear what's current
- Recommendation: Review and either delete or consolidate into single archive location

**Loose VTT Files in Root:**
- Files: Multiple `.vtt` and `.srt` files in project root
  - `haiti-comp-*.vtt` (6 files)
  - `niche-*.vtt` (3 files)
  - `peru-protests.en.vtt`
  - `reparations-mehdi-biggar.en.vtt`
  - `voice-analysis-unscripted.en.vtt`
  - `history-vs-hype-video.en.vtt`
- Impact: Cluttered root directory
- Recommendation: Move to `transcripts/` or relevant project folders

**Duplicate Prompt Evaluation Templates:**
- Files:
  - `.claude/tools/prompt_evaluation_templates.json`
  - `prompt_evaluation_templates.json` (in root)
- Impact: Unclear which is authoritative
- Recommendation: Keep one, delete duplicate

---

*Concerns audit: 2026-01-19*
