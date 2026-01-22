# Phase 4: Script Management - Context

**Gathered:** 2026-01-21
**Status:** Ready for planning

<domain>
## Phase Boundary

Eliminate script version sprawl (V2, V3, FINAL, FINAL-FINAL) by establishing one canonical script file per video with git tracking history, plus teleprompter-ready export. Creating/editing scripts is handled by existing commands; this phase focuses on file organization and export workflow.

</domain>

<decisions>
## Implementation Decisions

### Script file naming
- Canonical filename: `SCRIPT.md` (not `02-SCRIPT-DRAFT.md`)
- Location: Project root (e.g., `video-projects/_IN_PRODUCTION/19-flat-earth/SCRIPT.md`)
- Old numbered files (02-SCRIPT-DRAFT.md) renamed to SCRIPT.md during migration

### Version tracking workflow
- Git tracks all script changes — no more V2, V3, FINAL-v2 files
- Templates and commands should encourage committing script changes

### Teleprompter export
- Format: RTF with large font for PromptSmart compatibility
- Content: Spoken text ONLY — all markdown formatting and B-roll notes stripped
- Creates clean, readable output for filming

### Migration approach
- Audit existing projects first to understand scope
- Most recent file by date becomes SCRIPT.md
- Old V2/V3/FINAL files moved to `_archive/` subfolder
- Git history preserves everything

### Claude's Discretion
- Whether to keep FINAL-SCRIPT.md as separate file or make SCRIPT.md the only file
- Commit message format for script changes
- Whether to add a /script-history command
- Best integration point for commit reminders in workflow
- Teleprompter file output location (project folder vs desktop)
- Migration timing (all at once vs project-by-project)
- Specific font size for RTF export

</decisions>

<specifics>
## Specific Ideas

- PromptSmart or similar app is the teleprompter software
- RTF format chosen for easy reading with pre-formatted large font
- Old files should be preserved (moved to _archive/) not deleted

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 04-script-management*
*Context gathered: 2026-01-21*
