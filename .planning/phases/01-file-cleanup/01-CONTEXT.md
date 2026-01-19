# Phase 1: File Cleanup - Context

**Gathered:** 2025-01-19
**Status:** Ready for planning

<domain>
## Phase Boundary

Clean up the workspace so it contains only current, relevant files with clear organization. Remove outdated files, consolidate duplicates into single sources of truth, and establish naming conventions. This is the foundation that enables all other phases.

</domain>

<decisions>
## Implementation Decisions

### Archive Criteria
- Delete outdated files completely (no archive folder)
- "Outdated" means: superseded versions, deprecated workflow references, conflicting guidance
- Abandoned video projects (never made) should be KEPT — might return to these ideas
- Review step before deletion: Claude's discretion on whether to auto-delete or generate a review list

### Consolidation Rules
- Merge content from duplicates (combine useful parts from all versions)
- After merging, source files: Claude's discretion on delete vs backup
- Duplication exists across: style guidance, workflow docs, script versions, research notes
- Script version files (V1, V2, FINAL): Claude decides whether to clean now or defer to Phase 4

### Naming Conventions
- Need conventions for: video project folders, scripts, research files, guides/docs
- Pattern for project folders: Claude's discretion (number+topic, date+topic, etc.)
- Word separation style: Claude's discretion (hyphens, underscores, etc.)
- Preserve existing patterns that work; only change what's broken

### Folder Structure
- Current lifecycle folders (_IN_PRODUCTION, _READY_TO_FILM, _ARCHIVED): Claude assesses if working
- Reference document location: Claude determines best location
- Cluttered folders: Claude audits and identifies issues
- Structure documentation: Claude decides if needed

### Claude's Discretion
- Review step approach (auto-delete vs review list)
- What to do with source files after merging
- Boundary between this phase and Phase 4 for script versions
- Naming patterns and word separation style
- Whether to preserve or change existing folder structure
- Location for reference documents
- Whether folder structure documentation is needed

</decisions>

<specifics>
## Specific Ideas

- User trusts Claude to assess what's working and what needs changing
- Abandoned video ideas should be preserved — user might return to them
- Style guidance, workflow docs, script versions, and research notes all have duplication
- User is okay with deleting rather than archiving — clean slate preferred

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 01-file-cleanup*
*Context gathered: 2025-01-19*
