# Phase 51 Audit: Logging & CLI Standardization

## 1. print() Statement Inventory

**Total: 1,454 print() calls across 73 files**

### Top offenders (by count):

| File | Count | Notes |
|------|-------|-------|
| `youtube-analytics/performance.py` | 130 | Mostly OUTPUT (reports) |
| `youtube-analytics/patterns.py` | 91 | Mix of OUTPUT + INFO |
| `prompt_evaluation.py` | 70 | Mostly OUTPUT |
| `youtube-analytics/backfill.py` | 51 | Mix INFO + ERROR |
| `history-clip-tool/build.py` | 62 | Out of scope |
| `history-clip-tool/setup_ffmpeg_portable.py` | 39 | Out of scope |
| `youtube-analytics/analyze.py` | 38 | Mostly OUTPUT |
| `discovery/orchestrator.py` | 47 | Mix OUTPUT + INFO |
| `discovery/backfill_gaps.py` | 65 | Mix INFO + DEBUG |
| `youtube-analytics/feedback_queries.py` | 9 | DEBUG/ERROR |

### Category breakdown (estimated):

| Category | Log Level | Estimated Count | Action |
|----------|-----------|-----------------|--------|
| OUTPUT (user-facing results) | Keep as print() | ~600 | No change — CLI output |
| INFO (progress/status) | logging.info | ~400 | Replace |
| DEBUG (diagnostic) | logging.debug | ~200 | Replace |
| WARNING (potential issue) | logging.warning | ~50 | Replace |
| ERROR (failure) | logging.error + stderr | ~100 | Replace |
| Out of scope (history-clip-tool) | — | ~100 | Skip |

**Key insight:** About 600 print() calls are intentional CLI output (report formatting, tables, results). These should STAY as print(). Only ~750 internal print() calls need to become logging calls.

### Files using `print(..., file=sys.stderr)` (already error-aware):
- autocomplete.py, backfill.py, feedback.py, benchmarks.py, pattern_synthesizer_v2.py, playbook_synthesizer.py, retention_scorer.py, script-checkers/cli.py

## 2. Existing logging Usage

**Only 1 file uses Python logging:** `tools/history-clip-tool/src/utils/logger.py`

```python
import logging
logger = logging.getLogger(name)
```

This is in the history-clip-tool (out of scope). **Zero files in main tools/ use the logging module.**

## 3. CLI Entry Points (61 files with `if __name__ == '__main__':`)

### Uses argparse (28 files):

| File | Has --help | Has --verbose | Has --quiet |
|------|-----------|---------------|-------------|
| `discovery/autocomplete.py` | Yes | No | No |
| `discovery/backfill_gaps.py` | Yes | No | No |
| `discovery/competition.py` | Yes | No | No |
| `discovery/demand.py` | Yes | No | No |
| `discovery/diagnostics.py` | Yes | No | No |
| `discovery/format_filters.py` | Yes | No | No |
| `discovery/intent_mapper.py` | Yes | No | No |
| `discovery/keywords.py` | Yes | No | No |
| `discovery/metadata_checker.py` | Yes | No | No |
| `discovery/orchestrator.py` | Yes | No | No |
| `discovery/recommender.py` | Yes | No | No |
| `discovery/vidiq_workflow.py` | Yes | No | No |
| `document_discovery/cli.py` | Yes | No | No |
| `translation/cli.py` | Yes | No | No |
| `translation/verification.py` | Yes | No | No |
| `production/parser.py` | Yes | No | No |
| `production/split_screen_guide.py` | Yes | No | No |
| `production/editguide.py` | Yes | No | No |
| `production/metadata.py` | Yes | No | No |
| `youtube-analytics/analyze.py` | Yes | No | No |
| `youtube-analytics/backfill.py` | Yes | No | No |
| `youtube-analytics/benchmarks.py` | Yes | No | No |
| `youtube-analytics/feedback.py` | Yes | No | No |
| `youtube-analytics/performance.py` | Yes | No | No |
| `youtube-analytics/topic_strategy.py` | Yes | No | No |
| `youtube-analytics/technique_library.py` | Yes | No | No |
| `script-checkers/cli.py` | Yes | No | No |
| `intel/query.py` | Yes | No | No |

**All 28 have argparse but NONE have --verbose or --quiet.**

### Uses manual sys.argv parsing (no argparse):

| File | Current Parsing |
|------|----------------|
| `citation_extractor.py` | argparse (good) |
| `notebooklm_bridge.py` | argparse (good) |
| `youtube-analytics/auth.py` | No args |
| `youtube-analytics/ctr.py` | Manual sys.argv |
| `youtube-analytics/channel_averages.py` | Manual sys.argv |
| `youtube-analytics/comments.py` | Manual sys.argv |
| `youtube-analytics/feedback_queries.py` | argparse |
| `youtube-analytics/metrics.py` | Manual sys.argv |
| `youtube-analytics/retention.py` | Manual sys.argv |
| `youtube-analytics/video_report.py` | Manual sys.argv |
| `youtube-analytics/variants.py` | Manual sys.argv |
| `youtube-analytics/section_diagnostics.py` | Manual sys.argv |
| `youtube-analytics/retention_mapper.py` | Manual sys.argv |
| `youtube-analytics/retention_scorer.py` | Manual sys.argv |
| `youtube-analytics/playbook_synthesizer.py` | Manual sys.argv |
| `youtube-analytics/performance_report.py` | Manual sys.argv |
| `youtube-analytics/pattern_extractor.py` | Manual sys.argv |
| `youtube-analytics/pattern_synthesizer_v2.py` | argparse |
| `youtube-analytics/patterns.py` | argparse |
| `youtube-analytics/feedback_parser.py` | argparse |
| `youtube-analytics/transcript_analyzer.py` | argparse |

**~13 files use manual sys.argv** — need conversion to argparse.

## 4. Exit Code Patterns

### Files using sys.exit():
- Most argparse files exit 0 on success (implicit) and 1 on error
- Several files use `sys.exit(1)` for missing dependencies (good)
- Some files don't call sys.exit() at all — just end

### Inconsistencies:
- Some errors print to stderr + exit 1 (good)
- Some errors print to stdout + continue (bad)
- Some errors silently return without exit code (bad)

## 5. Proposed Logging Architecture

### Shared module: `tools/common/logging_config.py`

```python
import logging
import sys

def setup_logging(name: str, verbose: bool = False, quiet: bool = False) -> logging.Logger:
    """Configure logging for a tool module."""
    logger = logging.getLogger(name)

    if quiet:
        logger.setLevel(logging.ERROR)
    elif verbose:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    handler = logging.StreamHandler(sys.stderr)
    formatter = logging.Formatter('%(levelname)s: %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
```

### Standard argparse additions:

```python
parser.add_argument('--verbose', '-v', action='store_true', help='Show debug output')
parser.add_argument('--quiet', '-q', action='store_true', help='Only show errors')
```

### Mapping rules:
- `print(f"Processing {x}...")` → `logger.info(f"Processing {x}...")`
- `print(f"DEBUG: {x}")` → `logger.debug(f"{x}")`
- `print(f"WARNING: {x}")` → `logger.warning(f"{x}")`
- `print(f"ERROR: {x}", file=sys.stderr)` → `logger.error(f"{x}")`
- `print(report_table)` → Keep as `print()` (intentional output)

## Summary

| Category | Count | Action |
|----------|-------|--------|
| print() calls to convert | ~750 | Replace with logging |
| print() calls to keep | ~600 | CLI output, no change |
| Files with argparse | 28 | Add --verbose/--quiet |
| Files with manual argv | ~13 | Convert to argparse |
| Files with no args | ~5 | Add argparse if CLI |
| Files already using logging | 0 | Start from scratch |
