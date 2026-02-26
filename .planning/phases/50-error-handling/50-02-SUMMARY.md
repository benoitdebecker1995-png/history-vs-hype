---
phase: 50-error-handling
plan: 02
subsystem: error-handling
tags: [python, exception-handling, sqlite3, json, OSError, UnicodeDecodeError]

# Dependency graph
requires:
  - phase: 50-01-error-handling
    provides: youtube_analytics/ bare except cleanup (Task 1 committed, Task 2 pending)
provides:
  - "Zero bare except: blocks in intel/, discovery/, production/, dashboard/, history-clip-tool/"
  - "Zero except Exception: pass blocks in intel/, discovery/, production/, dashboard/"
  - "split_screen_guide._parse_script() returns error dict with module/operation/details on failure"
  - "All new error dicts include ERR-03 structured context (module, operation, details)"
affects: [51-logging-cli, 53-integration-testing]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Specific exception narrowing: sqlite3.OperationalError for ALTER TABLE guards, json.JSONDecodeError/TypeError for json.loads, OSError/UnicodeDecodeError for file reads"
    - "ERR-03 error dict format: {error, module, operation, details} for all new error dicts in modified files"
    - "Caller update pattern: check isinstance(result, dict) and 'error' in result when return type changes from None to error dict"

key-files:
  created: []
  modified:
    - tools/intel/kb_store.py
    - tools/intel/kb_exporter.py
    - tools/intel/topic_scorer.py
    - tools/discovery/competition.py
    - tools/discovery/backfill_gaps.py
    - tools/discovery/recommender.py
    - tools/discovery/database.py
    - tools/production/split_screen_guide.py
    - tools/dashboard/project_scanner.py
    - tools/history-clip-tool/launcher.py

key-decisions:
  - "scope-boundary: analyze.py except Exception pass (line 1306) is Plan 01 incomplete work — not touched in Plan 02; ERR-01 full codebase gate deferred until Plan 01 Task 2 runs"
  - "split_screen_guide method name: plan referenced _read_file but actual file uses _parse_script — ERR-03 dict uses correct method name _parse_script"
  - "recommender.py intel call: kept except Exception as e with noqa comment — intel scoring is non-blocking, exception type is unknowable (wraps external tool function)"
  - "database.py backup except: added as e capture even though unused — satisfies pitfall 4 from research (silent exception drops)"

patterns-established:
  - "ALTER TABLE guards use sqlite3.OperationalError (not broad Exception)"
  - "json.loads guards use json.JSONDecodeError, TypeError (handles None input)"
  - "File read guards use OSError, UnicodeDecodeError"
  - "Error dict return type change requires caller update: isinstance(x, dict) and 'error' in x check"

requirements-completed: [ERR-01, ERR-02, ERR-03]

# Metrics
duration: 20min
completed: 2026-02-25
---

# Phase 50 Plan 02: Error Handling — intel/, discovery/, production/, dashboard/ Summary

**10 files narrowed from broad/bare excepts to specific exception types; split_screen_guide._parse_script() upgraded to return structured error dict with module/operation/details fields**

## Performance

- **Duration:** ~20 min
- **Started:** 2026-02-25T18:10:00Z
- **Completed:** 2026-02-25T18:30:00Z
- **Tasks:** 2
- **Files modified:** 10

## Accomplishments
- Zero bare `except:` blocks remain in intel/, discovery/, production/, dashboard/, history-clip-tool/ (ERR-01 satisfied for these packages)
- Zero `except Exception: pass` blocks remain in intel/, discovery/, production/, dashboard/ (ERR-01 satisfied for these packages)
- `split_screen_guide._parse_script()` now returns `{'error': ..., 'module': 'split_screen_guide', 'operation': '_parse_script', 'details': str(e)}` on file read failure (ERR-02 + ERR-03)
- All 10 modified files use specific Python stdlib exception types matched to their actual operations

## Task Commits

Each task was committed atomically:

1. **Task 1: Fix broad excepts in intel/ and discovery/ packages** - `b5a3d66` (fix)
2. **Task 2: Fix bare excepts in production/, dashboard/, history-clip-tool/ + ERR-02/ERR-03** - `47c81ae` (fix)

**Plan metadata:** [created in final commit]

## Files Created/Modified
- `tools/intel/kb_store.py` - 3 `except Exception` → `sqlite3.OperationalError` (ALTER TABLE guards) + `ValueError/TypeError/sqlite3.Error` (is_stale)
- `tools/intel/kb_exporter.py` - 1 `except Exception` → `json.JSONDecodeError, TypeError` (json.loads in _render_algo_section)
- `tools/intel/topic_scorer.py` - 7 `except Exception` → specific types per operation (sqlite3.Error, json.JSONDecodeError, KeyError, TypeError, ValueError, ZeroDivisionError, ImportError)
- `tools/discovery/competition.py` - 1 `except Exception` → `ValueError, AttributeError, TypeError` (DB classification persist)
- `tools/discovery/backfill_gaps.py` - 2 `except Exception` → `sqlite3.Error`; added `import sqlite3`
- `tools/discovery/recommender.py` - 1 `except Exception` → `except Exception as e` with noqa comment (non-blocking intel score)
- `tools/discovery/database.py` - 2 `except Exception` → `OSError/sqlite3.Error as e` (backup) + `sqlite3.Error/KeyError/TypeError/ZeroDivisionError as e` (CTR stats)
- `tools/production/split_screen_guide.py` - bare `except:` → `OSError, UnicodeDecodeError as e`; return None → error dict with module/operation/details; caller updated to handle new return type
- `tools/dashboard/project_scanner.py` - 1 `except Exception` → `OSError, UnicodeDecodeError`
- `tools/history-clip-tool/launcher.py` - 1 bare `except:` → `OSError` (socket connect_ex)

## Decisions Made
- `split_screen_guide` method was `_parse_script` not `_read_file` (plan cited wrong name from research). ERR-03 dict uses actual method name `_parse_script`.
- `recommender.py` intel score call kept as `except Exception as e` — the function wraps `_intel_score_topic()` which can raise anything; broad catch is intentional with noqa comment.
- `database.py` backup except: added `as e` capture even though e is unused — follows research pitfall 4 guidance (never silent `except Exception:` without capture).
- ERR-03 scope held to files modified in this plan only — no retrofit of existing 153 error dicts.

## Deviations from Plan

### Out-of-scope item noted

**Plan 01 incomplete work:** `tools/youtube_analytics/analyze.py` line 1306 still has `except Exception: pass`. This is Plan 01's Task 2 (backfill.py, benchmarks.py, analyze.py, video_report.py) which was not committed. Plan 02's scope explicitly excludes `youtube_analytics/`. This item remains for Plan 01 Task 2 completion.

None within Plan 02 scope — plan executed exactly as specified for all 10 in-scope files.

## Issues Encountered
- Plan referenced `_read_file` method in split_screen_guide.py but the actual method is `_parse_script`. The fix was applied to the correct method with correct naming in the error dict. No functional impact.
- ERR-01 codebase-wide grep shows 1 remaining `except Exception: pass` in `analyze.py` (Plan 01 scope) — this is pre-existing, not introduced by Plan 02.

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- intel/, discovery/, production/, dashboard/ error handling complete
- Plan 01 Task 2 (backfill.py, benchmarks.py, analyze.py, video_report.py) still needs execution before ERR-01 is fully satisfied codebase-wide
- Phase 51 (Logging & CLI Standardization) ready to proceed once Plan 01 Task 2 is done

---
*Phase: 50-error-handling*
*Completed: 2026-02-25*
