# Phase 51: Logging & CLI Standardization - Context

**Gathered:** 2026-02-26
**Status:** Ready for planning

<domain>
## Phase Boundary

Replace ~750 diagnostic print() calls with proper logging, add --verbose/--quiet/--help to all CLI entry points (28 argparse + 13 manual sys.argv), and standardize error output to stderr with exit code 1. Scope: tools/ directory only. ~600 intentional output print() calls stay as print().

</domain>

<decisions>
## Implementation Decisions

### Output Routing
- **stdout = intentional output** (tables, reports, scores, results) — what Claude reads
- **stderr = log messages** (progress, warnings, debug) — diagnostic only
- Intentional print() calls (~600) stay as print() to stdout — no wrapper function needed
- Diagnostic print() calls (~750) get converted to logging at appropriate levels
- Non-fatal issues: log warning inline and continue (don't collect/summarize)

### Verbosity Levels
- **Three levels:** --quiet (errors only), default (INFO), --verbose (DEBUG)
- No --debug level, no stackable -v/-vv
- Default verbosity is INFO — shows key milestones ("Processing 12 videos...", "Done.")
- Always respect explicit flags — no magic TTY detection or auto-suppression
- Slash commands can pass --quiet if they want silence

### Log Format
- **Default:** level + message only (e.g., "WARNING: 2 videos missing data")
- **--verbose:** adds module name (e.g., "[discovery.trends] DEBUG: querying 45 keywords")
- No timestamps in default mode
- Colors when TTY detected, plain text when piped/redirected
- Plain text prefixes (WARNING:, ERROR:, DEBUG:) — no emoji
- **Shared logging module** (e.g., tools/logging_config.py) — one setup_logging(verbose, quiet) function all tools import

### CLI Consistency
- **Full argparse conversion** for all 13 manual sys.argv files — proper --help, validation, type checking
- All tools get the same CLI treatment regardless of invocation method (no internal-only exceptions)
- **--help format:** one-liner description + usage pattern + argument descriptions + 1-2 examples
- --verbose and --quiet are **mutually exclusive** (argparse group — error if both passed)
- All 28 existing argparse files get --verbose/--quiet added to their existing parsers

### Claude's Discretion
- Exact log messages for each tool's INFO milestones
- How to categorize each of the ~1,454 print() calls (intentional vs. diagnostic)
- Color implementation details (colorama vs. ANSI codes vs. logging formatter)
- Argument naming conventions for tool-specific flags

</decisions>

<specifics>
## Specific Ideas

- The shared logging module should be dead simple to use: `from tools.logging_config import setup_logging` then `setup_logging(args.verbose, args.quiet)` in main()
- Success criteria requires `grep -r "print(" tools/` to return zero matches outside CLI entry points — this is the hard constraint

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 51-logging-cli-standardization*
*Context gathered: 2026-02-26*
