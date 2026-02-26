# Phase 51: Logging & CLI Standardization - Research

**Researched:** 2026-02-26
**Domain:** Python standard library logging + argparse; zero external dependencies
**Confidence:** HIGH

---

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

**Output Routing:**
- stdout = intentional output (tables, reports, scores, results) — what Claude reads
- stderr = log messages (progress, warnings, debug) — diagnostic only
- Intentional print() calls (~600) stay as print() to stdout — no wrapper function needed
- Diagnostic print() calls (~750) get converted to logging at appropriate levels
- Non-fatal issues: log warning inline and continue (don't collect/summarize)

**Verbosity Levels:**
- Three levels: --quiet (errors only), default (INFO), --verbose (DEBUG)
- No --debug level, no stackable -v/-vv
- Default verbosity is INFO — shows key milestones ("Processing 12 videos...", "Done.")
- Always respect explicit flags — no magic TTY detection or auto-suppression
- Slash commands can pass --quiet if they want silence

**Log Format:**
- Default: level + message only (e.g., "WARNING: 2 videos missing data")
- --verbose: adds module name (e.g., "[discovery.trends] DEBUG: querying 45 keywords")
- No timestamps in default mode
- Colors when TTY detected, plain text when piped/redirected
- Plain text prefixes (WARNING:, ERROR:, DEBUG:) — no emoji
- Shared logging module (e.g., tools/logging_config.py) — one setup_logging(verbose, quiet) function all tools import

**CLI Consistency:**
- Full argparse conversion for all 13 manual sys.argv files — proper --help, validation, type checking
- All tools get the same CLI treatment regardless of invocation method (no internal-only exceptions)
- --help format: one-liner description + usage pattern + argument descriptions + 1-2 examples
- --verbose and --quiet are mutually exclusive (argparse group — error if both passed)
- All 28 existing argparse files get --verbose/--quiet added to their existing parsers

### Claude's Discretion
- Exact log messages for each tool's INFO milestones
- How to categorize each of the ~1,454 print() calls (intentional vs. diagnostic)
- Color implementation details (colorama vs. ANSI codes vs. logging formatter)
- Argument naming conventions for tool-specific flags

### Deferred Ideas (OUT OF SCOPE)
None — discussion stayed within phase scope
</user_constraints>

---

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| LOG-01 | Logging module configured with module-level loggers across all tool directories | Logging hierarchy: configure `tools` root logger in `tools/logging_config.py`; all `tools.*` child loggers inherit it automatically via propagation |
| LOG-02 | All print() calls in tool modules replaced with appropriate log level (DEBUG/INFO/WARNING/ERROR) | 750 diagnostic prints across 73 files need conversion; categorization rules in Code Examples section; ~600 intentional output prints stay as print() |
| LOG-03 | Log output goes to stderr with configurable verbosity (--verbose/--quiet flags) | `logging.StreamHandler(sys.stderr)` + argparse mutually exclusive group; setup_logging() wires both |
| CLI-01 | All CLI entry points use argparse with --help | 12 true sys.argv files need argparse conversion; 28 existing argparse files need --verbose/--quiet additions; some "entry points" (retention_mapper, section_diagnostics) are module-only — no CLI needed |
| CLI-02 | Consistent error output format across all tools (stderr, exit code 1) | Already partially in place: ~50 files use `print(..., file=sys.stderr)` + `sys.exit(1)`; need to standardize the remaining inconsistencies |
| CLI-03 | Standard --verbose/--quiet flags wired to logging levels | Argparse mutually exclusive group + `setup_logging(args.verbose, args.quiet)` call in every `main()` |
</phase_requirements>

---

## Summary

Phase 51 is a pure-Python standard library phase. Python's `logging` module and `argparse` provide everything needed — no new packages are required. The codebase currently has zero files using `logging` in the main `tools/` directories (only `history-clip-tool/` which is out of scope), and 1,454 `print()` calls spread across 73 files.

The key architectural insight is Python's logger hierarchy: a single `setup_logging()` call on the `tools` root logger automatically applies to every `tools.discovery.*`, `tools.youtube_analytics.*`, and `tools.intel.*` child logger through propagation. Each module then creates its own `logger = logging.getLogger(__name__)` and uses it without knowing about the configuration. The entry point calls `setup_logging(args.verbose, args.quiet)` once in `main()` — that's the entire wiring.

The 1,454 print() calls sort into two buckets: ~600 intentional output (tables, JSON results, reports — stay as `print()`) and ~750 diagnostic prints (progress, warnings, errors — become `logging` calls). Distinguishing them is the main judgment task. The audit's top files by count (performance.py at 130, patterns.py at 91) are primarily intentional output; the heavy diagnostic files are backfill_gaps.py and intel/refresh.py. The actual conversion work is mechanical once categories are decided.

**Primary recommendation:** Create `tools/logging_config.py` first (Wave 0), then work through files in dependency order: shared modules before CLI entry points, to avoid re-touching files.

---

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| `logging` | stdlib (3.14) | Module-level loggers, configurable levels, StreamHandler | Zero dependency, Python's designed solution for this exact problem |
| `argparse` | stdlib (3.14) | CLI argument parsing, --help generation, type checking | Built-in, handles edge cases (mutually exclusive groups, nargs, type coercion) |
| `sys` | stdlib | `sys.stderr` routing, `sys.exit()`, `sys.stdout.isatty()` | Already imported in all entry points |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| `colorama` | 0.4.6 (installed) | Windows ANSI escape sequence support | Only needed in `logging_config.py` for the color formatter |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| stdlib `logging` | `loguru` (third-party) | loguru is simpler but adds a dependency; stdlib logging is sufficient for this codebase's needs |
| `colorama` | Raw ANSI codes | Raw ANSI works on Linux/Mac but fails on Windows terminals without colorama; colorama is already installed |
| `argparse` | `click` (third-party) | click is ergonomic but adds dependency; argparse is already used in 28 files — consistency wins |

**Installation:** No new packages needed. `colorama` is already installed. All other libraries are stdlib.

---

## Architecture Patterns

### Recommended Project Structure

```
tools/
├── logging_config.py         # NEW: shared setup_logging() + get_logger()
├── __init__.py               # existing — add NullHandler registration
├── discovery/
│   ├── orchestrator.py       # existing argparse: add --verbose/--quiet
│   └── ... (12 more)
├── youtube_analytics/
│   ├── channel_averages.py   # existing sys.argv: convert to argparse
│   ├── comments.py           # existing sys.argv: convert to argparse
│   ├── ctr.py                # existing sys.argv: convert to argparse
│   ├── metrics.py            # existing sys.argv: convert to argparse
│   ├── retention.py          # existing sys.argv: convert to argparse
│   ├── video_report.py       # existing sys.argv: convert to argparse
│   └── ... (print conversions only for others)
├── intel/
│   └── refresh.py            # print conversions (called from query.py CLI)
└── ...
```

### Pattern 1: Shared Logging Module

**What:** Single `tools/logging_config.py` with `setup_logging()` and a convenience `get_logger()`. All tool modules import `get_logger(__name__)` for their module-level logger.

**When to use:** All modules in `tools/` that produce diagnostic output.

**Example:**
```python
# tools/logging_config.py
import logging
import sys


def setup_logging(verbose: bool = False, quiet: bool = False) -> None:
    """Configure logging for History vs Hype tools.

    Called once in main() of each CLI entry point.
    All tools.* child loggers inherit this configuration automatically.

    Args:
        verbose: If True, show DEBUG messages with module name prefix.
        quiet:   If True, show only ERROR messages.
    """
    if verbose and quiet:
        raise ValueError("verbose and quiet are mutually exclusive")

    root = logging.getLogger("tools")

    if quiet:
        root.setLevel(logging.ERROR)
    elif verbose:
        root.setLevel(logging.DEBUG)
    else:
        root.setLevel(logging.INFO)

    # Clear any handlers added by previous calls (e.g., in tests)
    root.handlers.clear()

    handler = logging.StreamHandler(sys.stderr)

    use_color = sys.stderr.isatty()
    if use_color:
        import colorama
        colorama.init()
        formatter = _ColorFormatter(_verbose_fmt() if verbose else _default_fmt())
    else:
        formatter = logging.Formatter(_verbose_fmt() if verbose else _default_fmt())

    handler.setFormatter(formatter)
    root.addHandler(handler)

    # Don't propagate to root Python logger
    root.propagate = False


def get_logger(name: str) -> logging.Logger:
    """Get a module-level logger.

    Usage in any module:
        from tools.logging_config import get_logger
        logger = get_logger(__name__)
    """
    return logging.getLogger(name)


def _default_fmt() -> str:
    return "%(levelname)s: %(message)s"


def _verbose_fmt() -> str:
    return "[%(name)s] %(levelname)s: %(message)s"


class _ColorFormatter(logging.Formatter):
    """Adds ANSI colors to levelname when stderr is a TTY."""
    _COLORS = {
        "DEBUG":    "\033[36m",   # cyan
        "INFO":     "\033[32m",   # green
        "WARNING":  "\033[33m",   # yellow
        "ERROR":    "\033[31m",   # red
        "CRITICAL": "\033[31;1m", # bold red
    }
    _RESET = "\033[0m"

    def format(self, record: logging.LogRecord) -> str:
        color = self._COLORS.get(record.levelname, "")
        record = logging.makeLogRecord(record.__dict__)
        record.levelname = f"{color}{record.levelname}{self._RESET}"
        return super().format(record)
```

### Pattern 2: Module-Level Logger Declaration

**What:** Every module declares one `logger` at module level, immediately after imports.

**When to use:** Any `tools/` module that currently has diagnostic `print()` calls.

**Example:**
```python
# At top of any tools module, after imports:
from tools.logging_config import get_logger
logger = get_logger(__name__)

# Usage inside functions:
logger.info("Processing %d videos...", len(video_ids))
logger.debug("Query params: %s", params)
logger.warning("2 videos missing retention data — skipping")
logger.error("API call failed: %s", result["error"])
```

### Pattern 3: CLI Entry Point Standard Template

**What:** Every `if __name__ == "__main__":` block follows the same structure: build parser, add --verbose/--quiet as mutually exclusive group, parse args, call `setup_logging()`, call `main(args)`.

**When to use:** All 41 true CLI entry points (28 existing argparse + 12 sys.argv conversions + 1 simple ones like auth.py).

**Example:**
```python
# Standard CLI entry point pattern
def main(args: argparse.Namespace) -> None:
    """Main entry point logic."""
    # all business logic here

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Fetch channel averages from recent videos.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  python -m tools.youtube_analytics.channel_averages
  python -m tools.youtube_analytics.channel_averages --compare wCFReiCGiks
  python -m tools.youtube_analytics.channel_averages --last-n 5 --compare wCFReiCGiks""",
    )
    # Tool-specific arguments
    parser.add_argument("--compare", metavar="VIDEO_ID", help="Compare video to channel averages")
    parser.add_argument("--last-n", type=int, default=10, metavar="N",
                        help="Use last N videos for averages (default: 10)")

    # Standard verbosity (ALWAYS add last, after tool-specific args)
    verbosity = parser.add_mutually_exclusive_group()
    verbosity.add_argument("--verbose", action="store_true", help="Show debug output on stderr")
    verbosity.add_argument("--quiet", action="store_true", help="Only show errors on stderr")

    args = parser.parse_args()

    from tools.logging_config import setup_logging
    setup_logging(args.verbose, args.quiet)

    main(args)
```

### Pattern 4: Error Exit Standard

**What:** On error, print to stderr, exit with code 1. Never print errors to stdout.

**When to use:** All error conditions in CLI entry points. Module functions return `{'error': msg}` dict — the CLI entry point converts that to stderr + exit 1.

**Example:**
```python
result = get_video_metrics(video_id)
if "error" in result:
    import sys
    print(f"ERROR: {result['error']}", file=sys.stderr)
    sys.exit(1)
# Intentional output goes to stdout:
print(json.dumps(result, indent=2))
```

### Anti-Patterns to Avoid

- **Configuring the root Python logger:** Always configure `logging.getLogger("tools")`, not `logging.getLogger()`. Configuring the root logger would suppress output from third-party libraries.
- **Adding NullHandler at module level in tool modules:** NullHandler is for library code meant to be imported. These tools ARE applications (they have `__main__` blocks). Add NullHandler only in `tools/__init__.py` as a library-layer safeguard.
- **Calling `setup_logging()` at module import time:** Only call it inside `if __name__ == "__main__"` blocks. Modules imported by other modules must not configure logging — that's the caller's responsibility.
- **Using `logging.basicConfig()`:** This configures the root Python logger globally. Use `logging.getLogger("tools")` instead.
- **Mixing print() and logger in the same diagnostic path:** Pick one. Diagnostic output = logger. Intentional results = print(). Never both for the same message.
- **Converting intentional output to logging:** `print(json.dumps(result))`, report tables, and formatted result displays are intentional output. They stay as `print()`. Converting them to `logger.info()` would break piping and Claude integration.

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Mutually exclusive --verbose/--quiet | Custom flag conflict check | `parser.add_mutually_exclusive_group()` | argparse handles the error message automatically |
| Log level mapping | Custom verbosity integer → string conversion | `logging.ERROR`, `logging.INFO`, `logging.DEBUG` constants | stdlib handles all level semantics |
| TTY color detection on Windows | Custom Windows console check | `sys.stderr.isatty()` + `colorama.init()` | colorama wraps Windows console API transparently |
| Per-handler level filtering | Duplicate handler setup | Single handler on `tools` logger + level on logger itself | Logger level filters before handler; one handler is sufficient |
| Stripping ANSI from non-TTY | Custom formatter fallback | `isatty()` check before adding color formatter | Simpler: use plain Formatter when not TTY, ColorFormatter when TTY |

**Key insight:** The Python logging hierarchy (parent → child propagation) eliminates the need for any registry or central coordinator. One `setup_logging()` call on the `tools` logger configures all 73 files simultaneously through Python's built-in propagation mechanism.

---

## Common Pitfalls

### Pitfall 1: Converting Intentional Output to Logging

**What goes wrong:** `print(json.dumps(result))` gets converted to `logger.info(json.dumps(result))`. Now `python tool.py | jq .` breaks because JSON goes to stderr instead of stdout.

**Why it happens:** The ~750 / ~600 split requires judgment on each print() call. Automated grep-and-replace would hit both categories.

**How to avoid:** Rule of thumb — if the output is consumed by a caller (Claude, a shell pipe, another tool), it stays as `print()`. If it describes what the tool is doing (progress, warnings, status), it becomes logging. When in doubt: is this the *result* or the *narration*?

**Warning signs:** Any `print(json.dumps(...))`, `print(f"{'Column':<15}")` table formatting, or `print(report_content)` — these are intentional output.

### Pitfall 2: Logging Before `setup_logging()` Is Called

**What goes wrong:** A module calls `logger.info(...)` at import time (e.g., during feature flag detection). `setup_logging()` hasn't been called yet, so Python's logging of last resort fires — the message goes to `sys.stderr` with a generic format, ignoring verbosity settings.

**Why it happens:** Module-level code runs at import time, before `main()` parses args.

**How to avoid:** Only log inside functions, never at module level. Feature flag detection code (try/except import blocks) should use `print(..., file=sys.stderr)` if they need to emit warnings, OR silence them (since they're ImportError fallbacks, not runtime errors).

**Warning signs:** `logger.info(...)` or `logger.debug(...)` calls outside function bodies.

### Pitfall 3: Multiple `setup_logging()` Calls Stacking Handlers

**What goes wrong:** A test or tool calls `setup_logging()` twice. Python's logging appends handlers — the second call adds a second StreamHandler, causing every log message to print twice.

**Why it happens:** `logging.getLogger("tools")` returns the same object every time — calling `addHandler()` twice adds two handlers.

**How to avoid:** `setup_logging()` must call `root.handlers.clear()` before adding the new handler (included in the code example above). Alternatively, check `if not root.handlers:` before adding.

**Warning signs:** Duplicate log lines during testing.

### Pitfall 4: Files Listed in Audit That Don't Need CLI Conversion

**What goes wrong:** Files listed as "manual sys.argv" in the audit get full argparse conversion when they don't actually need it.

**Why it happens:** The audit listed all files with `if __name__ == "__main__":`. Some (retention_mapper.py, section_diagnostics.py) only print a usage hint — they're Python modules, not real CLI tools. Their `__main__` block is a developer convenience, not a user-facing CLI.

**How to avoid:** Before converting any file, read its `__main__` block. If it says "Usage: from module import function", it needs only print()-to-logger conversion for any internal prints, not a full argparse CLI build.

**Warning signs:** `__main__` block that just prints "Module Name\nUsage: from X import Y" — these are docs, not CLIs.

### Pitfall 5: `--verbose`/`--quiet` Piped Through to Library Functions

**What goes wrong:** The argparse `args.verbose` and `args.quiet` booleans get passed down through function calls as parameters, coupling business logic to CLI concerns.

**Why it happens:** Developers want to respect verbosity in library functions.

**How to avoid:** `setup_logging()` in `main()` configures the logger hierarchy once. Library functions just call `logger.debug(...)` or `logger.info(...)` — the configured log level filters automatically. Never pass `verbose` or `quiet` as function parameters to library code.

### Pitfall 6: The `youtube_analytics/auth.py` Non-CLI

**What goes wrong:** `auth.py` gets full argparse treatment. But its `__main__` block is `pass` or a test call — it has no user-facing CLI.

**Why it happens:** It has `if __name__ == "__main__":` and was listed among files to check.

**How to avoid:** `auth.py`'s main block is internal testing infrastructure. Add only `setup_logging()` if needed, skip argparse if there are no user-facing arguments.

---

## Code Examples

Verified patterns from Python stdlib (Python 3.14 compatible):

### Mutually Exclusive Argument Group

```python
# Source: Python docs — argparse.add_mutually_exclusive_group()
verbosity = parser.add_mutually_exclusive_group()
verbosity.add_argument("--verbose", "-v", action="store_true",
                       help="Show debug output on stderr")
verbosity.add_argument("--quiet", "-q", action="store_true",
                       help="Only show errors on stderr")
# argparse automatically rejects: python tool.py --verbose --quiet
# Error: "argument --quiet: not allowed with argument --verbose"
```

### sys.argv Conversion Pattern (e.g., metrics.py)

**Before:**
```python
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python metrics.py VIDEO_ID [--start-date YYYY-MM-DD]")
        sys.exit(1)
    video_id = sys.argv[1]
    start_date = None
    args = sys.argv[2:]
    for i, arg in enumerate(args):
        if arg == '--start-date' and i + 1 < len(args):
            start_date = args[i + 1]
    result = get_video_metrics(video_id, start_date)
    print(json.dumps(result, indent=2))
```

**After:**
```python
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Fetch engagement metrics for a YouTube video.",
        epilog="""Examples:
  python -m tools.youtube_analytics.metrics dQw4w9WgXcQ
  python -m tools.youtube_analytics.metrics dQw4w9WgXcQ --start-date 2025-01-01""",
    )
    parser.add_argument("video_id", help="YouTube video ID")
    parser.add_argument("--start-date", metavar="YYYY-MM-DD",
                        help="Start date for metrics window")
    parser.add_argument("--end-date", metavar="YYYY-MM-DD",
                        help="End date for metrics window")
    verbosity = parser.add_mutually_exclusive_group()
    verbosity.add_argument("--verbose", action="store_true",
                           help="Show debug output on stderr")
    verbosity.add_argument("--quiet", action="store_true",
                           help="Only show errors on stderr")

    args = parser.parse_args()
    from tools.logging_config import setup_logging
    setup_logging(args.verbose, args.quiet)

    result = get_video_metrics(args.video_id, args.start_date, args.end_date)
    if "error" in result:
        print(f"ERROR: {result['error']}", file=sys.stderr)
        sys.exit(1)
    print(json.dumps(result, indent=2))
```

### Print-to-Logger Conversion Decision Table

```python
# KEEP as print() — intentional output (result data, reports, tables):
print(json.dumps(result, indent=2))              # JSON result → stdout
print(f"{'Column':<15} {'Value':>10}")           # table formatting → stdout
print(report_text)                               # full report → stdout

# CONVERT to logger — diagnostic/progress:
# Before:
print(f"Processing {len(videos)} videos...")
print(f"WARNING: 2 videos missing data")
print(f"DEBUG: querying {n} keywords")
print(f"ERROR: {result['error']}", file=sys.stderr)

# After:
logger.info("Processing %d videos...", len(videos))
logger.warning("2 videos missing data")
logger.debug("querying %d keywords", n)
logger.error("%s", result["error"])   # error also triggers sys.exit(1) in CLI layer

# EDGE CASE — progress within a loop (diagnostic):
# Before: print(f"  {kw} -> {category}", end=' ')
# After:  logger.debug("%s -> %s", kw, category)
# Note: logger doesn't support end=' ' — reformulate as a single post-loop summary
# logger.info("Classified %d keywords", classified)
```

### Logger Name Convention

```python
# In tools/discovery/orchestrator.py:
logger = logging.getLogger(__name__)
# Results in logger name: "tools.discovery.orchestrator"
# Propagates to "tools.discovery" → "tools" → configured handler

# In __verbose__ format, output looks like:
# [tools.discovery.orchestrator] DEBUG: Running demand analysis for 'dark ages'
```

### Existing sys.stderr Prints — Direct Conversion

Many files already use `print(..., file=sys.stderr)`. These convert trivially:

```python
# Before (autocomplete.py):
print(f"Processing {i+1}/{len(seeds)}: {seed}", file=sys.stderr)
print(f"Rate limited. Backing off {backoff}s...", file=sys.stderr)
print("ERROR: database module not found.", file=sys.stderr)

# After:
logger.info("Processing %d/%d: %s", i+1, len(seeds), seed)
logger.warning("Rate limited. Backing off %ds...", backoff)
logger.error("database module not found")
```

---

## Actual File Scope (Phase 51)

Based on direct codebase inspection, the real scope is:

### True sys.argv files (need argparse conversion + --verbose/--quiet):
12 files confirmed with manual sys.argv parsing:
1. `youtube_analytics/channel_averages.py` — loop-based argv parsing
2. `youtube_analytics/comments.py` — loop-based argv parsing
3. `youtube_analytics/ctr.py` — manual argv parsing
4. `youtube_analytics/metrics.py` — loop-based argv parsing
5. `youtube_analytics/retention.py` — index-based argv parsing
6. `youtube_analytics/video_report.py` — manual argv parsing
7. `discovery/intent_mapper.py` — uses sys.argv[1] check in argparse-adjacent code
8. `discovery/diagnostics.py` — uses sys.argv index checks alongside argparse
9. `production/parser.py` — uses sys.argv
10. `youtube_analytics/analyze.py` — extensive sys.argv manual parsing (1,332 lines)
11. `youtube_analytics/feedback_parser.py` — uses argparse but also sys.argv
12. `youtube_analytics/patterns.py` — uses argparse but also sys.argv

### Existing argparse files (add --verbose/--quiet only):
28 files (all discovery/, document_discovery/cli.py, translation/, production/split_screen_guide.py, production/editguide.py, production/metadata.py, youtube_analytics/analyze.py, backfill.py, benchmarks.py, feedback.py, performance.py, topic_strategy.py, technique_library.py, script_checkers/cli.py, intel/query.py)

### Module-only "entry points" (no CLI conversion needed):
- `youtube_analytics/retention_mapper.py` — `__main__` just prints "Usage: from retention_mapper import X"
- `youtube_analytics/section_diagnostics.py` — same pattern (2 print calls total)
- `youtube_analytics/auth.py` — no args; runs OAuth test
- `intel/refresh.py` — called from query.py, not standalone CLI

### Files with print() conversions only (no CLI work):
- `intel/refresh.py` — all diagnostic prints, many `print(f"  [{phase}/10] ...")` pattern → `logger.info`
- `youtube_analytics/backfill.py` — mix of Stage headers (intentional output) + progress prints (diagnostic)
- `youtube_analytics/backfill_gaps.py` — heavy diagnostic mix

---

## State of the Art

| Old Approach | Current Approach | Impact |
|--------------|------------------|--------|
| `print(..., file=sys.stderr)` for errors | `logger.error(...)` | Respects --quiet; automatically routed to stderr |
| Manual `if sys.argv[1] == '--help'` | `argparse` built-in --help | Consistent format, auto-generated, handles edge cases |
| No verbosity control | `--verbose` / `--quiet` flags | Slash commands can pass `--quiet` for clean output |
| 0 files using logging | All tools/* use `logging` | LOG-01 through LOG-03 satisfied |

**What remains current:**
- Python stdlib `logging` and `argparse` are stable, no deprecations in Python 3.14
- `colorama 0.4.6` is current (last release 2023); no changes needed to usage pattern
- Logger hierarchy (propagation) behavior is unchanged since Python 2.7

---

## Open Questions

1. **What is `intel/refresh.py`'s CLI status?**
   - What we know: It has a `__main__` block but is primarily called via `intel/query.py` or slash commands. It has 26 diagnostic `print()` calls using the `_print_phase(n, description)` helper pattern.
   - What's unclear: Does `refresh.py` need its own `--verbose/--quiet` argparse, or does it inherit verbosity from whatever calls it?
   - Recommendation: `refresh.py` is a module, not a user-facing CLI. Convert its prints to `logger.info/debug`, but don't add argparse to it. The caller (`query.py`) handles CLI.

2. **How aggressive to be on the 600 "intentional output" classification?**
   - What we know: The audit estimated ~600 intentional, ~750 diagnostic. The actual number requires per-file judgment.
   - What's unclear: Some files (backfill.py stage headers, orchestrator.py report tables) have a mix on the same line.
   - Recommendation: When in doubt, keep as `print()`. A false-negative (leaving a diagnostic as print) is safer than a false-positive (converting intentional output to logging, breaking callers).

3. **Should `tools/__init__.py` add a NullHandler for library safety?**
   - What we know: `tools/__init__.py` is currently empty. Adding `logging.getLogger("tools").addHandler(logging.NullHandler())` is Python's recommended pattern for library packages.
   - What's unclear: These tools are scripts, not libraries. But they can be imported.
   - Recommendation: Add the NullHandler to `tools/__init__.py`. It costs nothing and prevents "No handlers could be found for logger 'tools'" warnings if a module is imported without calling `setup_logging()`.

---

## Sources

### Primary (HIGH confidence)
- Python 3.14 stdlib — `logging` module — verified via `python -c "import logging; ..."` on installed interpreter
- Python 3.14 stdlib — `argparse` module — verified via `python -c "import argparse; ..."` on installed interpreter
- Direct codebase inspection — all 55 `if __name__ == "__main__":` files examined, 73 print()-bearing files counted via audit

### Secondary (MEDIUM confidence)
- Python logging docs — logging HOWTO — https://docs.python.org/3/howto/logging.html — standard pattern for library vs application logging
- colorama README — https://github.com/tartley/colorama — verified `colorama 0.4.6` installed, `colorama.init()` required on Windows for ANSI

### Tertiary (LOW confidence)
- None — all findings verified via direct code/interpreter inspection

---

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — stdlib only; verified on installed Python 3.14; colorama confirmed installed at 0.4.6
- Architecture: HIGH — logger hierarchy behavior verified via interpreter; patterns are textbook Python logging
- Pitfalls: HIGH — derived from direct codebase inspection of actual print() patterns and file structures
- File scope: HIGH — confirmed by grep; audit counts verified; sys.argv files confirmed by reading __main__ blocks

**Research date:** 2026-02-26
**Valid until:** 2026-09-01 (stdlib is stable; no risk of logging/argparse API changes)
