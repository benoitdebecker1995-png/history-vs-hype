---
phase: 48-package-structure-dependencies
plan: 02
subsystem: infra
tags: [python-packaging, imports, sys-path-cleanup, relative-imports, absolute-imports]

requires:
  - 48-01 (directory renames and __init__.py files)
provides:
  - "Zero sys.path.insert/append calls in any live tool file"
  - "All cross-package imports use from tools.* absolute syntax"
  - "All same-package imports use relative syntax (from .module import X)"
  - "discovery/diagnostics.py uses lazy function-level imports for youtube_analytics"
  - "discovery/recommender.py uses lazy function-level import for pattern_extractor"
affects:
  - 48-03 (pyproject.toml — packages are now properly importable)
  - 53-integration-testing (pytest can import all packages without path hacks)

tech-stack:
  added: []
  patterns:
    - "Cross-package import: from tools.discovery.database import KeywordDB"
    - "Same-package import: from .module import Symbol"
    - "Lazy import pattern for circular dependencies: def _load_X(): try: from tools.Y.X import Z; return Z"
    - "Relative import from package __init__: from . import BaseChecker"

key-files:
  created: []
  modified:
    - tools/youtube_analytics/analyze.py
    - tools/youtube_analytics/backfill.py
    - tools/youtube_analytics/benchmarks.py
    - tools/youtube_analytics/feedback.py
    - tools/youtube_analytics/feedback_parser.py
    - tools/youtube_analytics/feedback_queries.py
    - tools/youtube_analytics/pattern_extractor.py
    - tools/youtube_analytics/pattern_synthesizer_v2.py
    - tools/youtube_analytics/performance.py
    - tools/youtube_analytics/performance_report.py
    - tools/youtube_analytics/playbook_synthesizer.py
    - tools/youtube_analytics/retention_mapper.py
    - tools/youtube_analytics/retention_scorer.py
    - tools/youtube_analytics/topic_strategy.py
    - tools/youtube_analytics/variants.py
    - tools/youtube_analytics/test_retention_mapper.py
    - tools/discovery/backfill_gaps.py
    - tools/discovery/demand.py
    - tools/discovery/diagnostics.py
    - tools/discovery/keywords.py
    - tools/discovery/orchestrator.py
    - tools/discovery/recommender.py
    - tools/document_discovery/cli.py
    - tools/intel/competitor_tracker.py
    - tools/production/parser.py
    - tools/script_checkers/checkers/flow.py
    - tools/script_checkers/checkers/pacing.py
    - tools/script_checkers/checkers/repetition.py
    - tools/script_checkers/checkers/scaffolding.py
    - tools/script_checkers/checkers/stumble.py
    - tools/script_checkers/cli.py
    - tools/script_checkers/tests/test_pacing.py
    - tools/translation/cli.py
    - tools/translation/smoke_test.py
    - tools/translation/structure_detector.py

key-decisions:
  - "Lazy import pattern used for discovery/diagnostics.py and discovery/recommender.py to break youtube_analytics circular dependency"
  - "Self sys.path hacks in same-package files converted to relative imports (from .module)"
  - "Cross-package imports converted to absolute tools.* syntax (from tools.discovery.database import KeywordDB)"
  - "discovery/demand.py and discovery/keywords.py fixed as Rule 3 auto-fix (blocking smoke test)"
  - "script_checkers/checkers/*.py BaseChecker imports fixed as Rule 3 auto-fix (blocking smoke test)"
  - "test_retention_mapper.py orphaned sys.path removed as Rule 1 auto-fix (dead code)"

requirements-completed: [PKG-02]

duration: 10min
completed: 2026-02-24
---

# Phase 48 Plan 02: Import Rewrites Summary

**Replaced all 37+ sys.path.insert/append hacks with proper absolute tools.* and relative imports, enabling `from tools.discovery import orchestrator` to work from any working directory without path manipulation**

## Performance

- **Duration:** 10 min
- **Started:** 2026-02-24T23:28:23Z
- **Completed:** 2026-02-24T23:38:50Z
- **Tasks:** 2
- **Files modified:** 35

## Accomplishments

- Removed every `sys.path.insert` / `sys.path.append` call from all live tool files (excluding dead files `_competitor_fetch.py` and `_csv_backfill.py`)
- All 15 youtube_analytics/ files converted: cross-package imports → `from tools.discovery.*` and `from tools.production.*`; self-imports → relative `from .module import X`
- All 12 remaining package files converted: discovery/, translation/, document_discovery/, production/, intel/, script_checkers/
- Implemented lazy import pattern in discovery/diagnostics.py and discovery/recommender.py to break the youtube_analytics circular dependency
- All four end-to-end smoke tests pass from repo root

## Task Commits

| Task | Name | Commit | Files |
|------|------|--------|-------|
| 1 | Replace sys.path hacks in youtube_analytics/ | (pre-committed from prior session) | 15 files |
| 2 | Replace sys.path hacks in discovery/, translation/, document_discovery/, production/, intel/, script_checkers/ | 54c5b6f | 19 files |

Note: Task 1 changes were already committed in a prior undocumented session. The edit operations in this session confirmed correctness by producing zero-diff against the committed versions.

## Files Modified

**youtube_analytics/ (Task 1 — already committed):**
- `analyze.py` - 3 hacks: sys.path for discovery/ and production/ → `from tools.discovery.diagnostics`, `from tools.production.parser`; sibling imports → relative
- `backfill.py` - 2 hacks: discovery/ → `from tools.discovery.database`; self → `from .performance`
- `benchmarks.py` - 1 hack: discovery/ → `from tools.discovery.database`
- `feedback.py` - 2 hacks: self and discovery/ → relative + `from tools.discovery.database`
- `feedback_parser.py` - 1 inline hack inside function → `from tools.discovery.database`
- `feedback_queries.py` - 1 hack: discovery/ → `from tools.discovery.database`; sibling → relative
- `pattern_extractor.py` - 1 hack: discovery/ → `from tools.discovery.database`; sibling → relative
- `pattern_synthesizer_v2.py` - 1 self-hack → `from .technique_library`, `from .transcript_analyzer`
- `performance.py` - 1 hack: discovery/ → `from tools.discovery.database`; siblings → relative
- `performance_report.py` - 1 hack: discovery/ → `from tools.discovery.database`
- `playbook_synthesizer.py` - 1 hack: discovery/ → `from tools.discovery.database`; sibling → relative
- `retention_mapper.py` - 1 hack: production/ → `from tools.production.parser`
- `retention_scorer.py` - 2 hacks: discovery/ and production/ in `__main__` block → absolute imports
- `topic_strategy.py` - 1 hack: discovery/ → `from tools.discovery.database`; sibling → relative
- `variants.py` - 1 hack: discovery/ → `from tools.discovery.database`
- `test_retention_mapper.py` - orphaned sys.path removed (Rule 1 auto-fix)

**Other packages (Task 2 — committed 54c5b6f):**
- `discovery/backfill_gaps.py` - self sys.path → `from .database`
- `discovery/demand.py` - bare sibling imports → relative (Rule 3 auto-fix — blocking smoke test)
- `discovery/diagnostics.py` - module-level sys.path → lazy import functions `_load_channel_averages()`, `_load_video_metrics()`
- `discovery/keywords.py` - `from database` → `from .database` (Rule 3 auto-fix)
- `discovery/orchestrator.py` - self sys.path → relative imports for all sibling modules
- `discovery/recommender.py` - 2 sys.path hacks → `from .database` + lazy `_load_pattern_extractor()` + already-absolute intel import
- `document_discovery/cli.py` - self sys.path → relative imports
- `intel/competitor_tracker.py` - inline sys.path in auth function → `from tools.youtube_analytics.auth`
- `production/parser.py` - project-root sys.path in `__main__` → removed (package already importable)
- `script_checkers/checkers/flow.py` - `from checkers import BaseChecker` → `from . import BaseChecker`
- `script_checkers/checkers/pacing.py` - sys.path → `from tools.production.parser`; `from checkers` → `from . import BaseChecker`
- `script_checkers/checkers/repetition.py` - `from checkers import BaseChecker` → `from . import BaseChecker`
- `script_checkers/checkers/scaffolding.py` - `from checkers` → `from .`; `from config` → `from tools.script_checkers.config`
- `script_checkers/checkers/stumble.py` - `from checkers import BaseChecker` → `from . import BaseChecker`
- `script_checkers/cli.py` - `from config`, `from output` → relative; lazy function imports → relative
- `script_checkers/tests/test_pacing.py` - sys.path → `from tools.script_checkers.checkers.pacing`
- `translation/cli.py` - self sys.path → relative imports
- `translation/smoke_test.py` - self sys.path + bare module imports → `from tools.translation.*`
- `translation/structure_detector.py` - inline sys.path → `from tools.document_discovery.structure_assessor`

## Decisions Made

- Used lazy import pattern (function-level import) for discovery/diagnostics.py and discovery/recommender.py to avoid circular import at module level (discovery ↔ youtube_analytics)
- For pacing.py inside checkers/ subpackage, `from . import BaseChecker` accesses the package's `__init__.py` where BaseChecker is defined
- demand.py, keywords.py, and script_checkers/checkers/*.py bare imports fixed as Rule 3 (blocking smoke test) even though not in original file list
- cli.py in script_checkers had both top-level and lazy function-level imports — all converted to relative

## Deviations from Plan

### Auto-fixed Issues (Rule 3 — Blocking)

**1. [Rule 3 - Blocking] Fixed bare imports in discovery/demand.py and discovery/keywords.py**
- **Found during:** Task 2 smoke test verification
- **Issue:** `from tools.discovery import orchestrator` failed because `demand.py` imported `from database`, `from trends`, etc. (bare names) which work when that directory is in sys.path but not when imported as a package
- **Fix:** Converted to relative imports (`from .database`, `from .trends`, etc.)
- **Files modified:** `tools/discovery/demand.py`, `tools/discovery/keywords.py`
- **Commit:** 54c5b6f

**2. [Rule 3 - Blocking] Fixed bare imports in script_checkers/checkers/*.py**
- **Found during:** Task 2 smoke test verification
- **Issue:** `from tools.script_checkers.checkers import pacing` failed because `stumble.py`, `flow.py`, `repetition.py`, `scaffolding.py` all used `from checkers import BaseChecker` (bare name)
- **Fix:** Converted to `from . import BaseChecker` (relative import from package `__init__.py`)
- **Files modified:** `flow.py`, `repetition.py`, `scaffolding.py`, `stumble.py`, and `cli.py` (lazy imports)
- **Commit:** 54c5b6f

**3. [Rule 1 - Bug] Removed orphaned sys.path in test_retention_mapper.py**
- **Found during:** Task 1 sys.path sweep
- **Issue:** Line 9 added production/ to sys.path but no subsequent import from production/ existed — dead code
- **Fix:** Removed the orphaned `sys.path.insert` and associated imports
- **Files modified:** `tools/youtube_analytics/test_retention_mapper.py`
- **Commit:** Already committed in prior session

## Verification Results

```
discovery.orchestrator OK
intel.kb_store OK
youtube_analytics.backfill OK
script_checkers.pacing OK

Zero sys.path hacks remaining in live code
```

## Self-Check: PASSED

| Check | Result |
|-------|--------|
| sys.path.insert/append in youtube_analytics/ | ZERO |
| sys.path.insert/append in discovery/ | ZERO |
| sys.path.insert/append in translation/ | ZERO |
| sys.path.insert/append in document_discovery/ | ZERO |
| sys.path.insert/append in production/ | ZERO |
| sys.path.insert/append in intel/ | ZERO |
| sys.path.insert/append in script_checkers/ | ZERO |
| from tools.discovery import orchestrator | PASS |
| from tools.intel import kb_store | PASS |
| from tools.youtube_analytics import backfill | PASS |
| from tools.script_checkers.checkers import pacing | PASS |
| commit 54c5b6f (Task 2) | FOUND |

---
*Phase: 48-package-structure-dependencies*
*Completed: 2026-02-24*
