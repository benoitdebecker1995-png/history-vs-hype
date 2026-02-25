# Phase 49: Dead Code Cleanup - Context

**Gathered:** 2026-02-25
**Status:** Ready for planning

<domain>
## Phase Boundary

Remove all code that isn't actively used from tools/. This covers: deleting known dead files (7 confirmed), auditing modules for unreachable functions, and handling orphaned artifacts (backup directories, scratch files). datetime.utcnow() is already fixed (zero occurrences) — that requirement is pre-satisfied.

</domain>

<decisions>
## Implementation Decisions

### Unused function audit depth
- **Full audit** of every public function in large modules (database.py, patterns.py, prompt_evaluation.py at minimum)
- Document caller count for each public function; remove those with zero callers
- No separate audit report file — just delete dead code, commit messages document what was removed

### prompt_evaluation.py disposition
- If deleted, commit message must describe what the module did and why it was removed (descriptive commit)

### Deletion method
- Standard `git rm` — no archive folders. Git history preserves everything
- Clean all stale references when removing a function: imports in other files, docstring mentions, comments
- After each deletion pass, run import checks on affected modules to verify nothing breaks

### Claude's Discretion
- Which modules beyond database.py and patterns.py warrant full audit (based on size and refactor history)
- Whether 1-caller functions should be flagged or left alone
- prompt_evaluation.py: read it, decide keep vs delete based on future value
- tools/discovery/backups/: check if anything still writes to it, then delete or .gitignore accordingly
- Whether to add .gitignore rules for scratch file patterns (e.g., `_*.json`, `backups/`)
- How to organize commits (logical groupings at Claude's discretion)

</decisions>

<specifics>
## Specific Ideas

No specific requirements — open to standard approaches

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 49-dead-code-cleanup*
*Context gathered: 2026-02-25*
