# Phase 49 Deferred Items

Items discovered but out-of-scope for Phase 49 tasks.

## Pre-existing Import Issues (Phase 48 miss)

### video_report.py uses bare imports — pre-existing from Phase 48 rename

**File:** `tools/youtube_analytics/video_report.py` (lines 33-35)

**Issue:**
```python
from metrics import get_video_metrics    # line 33
from retention import get_retention_data  # line 34
from ctr import get_ctr_metrics          # line 35
```

These are bare module imports that only worked when `sys.path.insert(0, 'tools/youtube-analytics')` was active. Phase 48-02 replaced all sys.path hacks with absolute/relative imports across the codebase, but `video_report.py` was missed.

**Effect:** `from tools.youtube_analytics.analyze import run_analysis` fails because `analyze.py` imports `video_report` which then fails with `ModuleNotFoundError: No module named 'metrics'`.

**Fix required:** Change to relative imports:
```python
from .metrics import get_video_metrics
from .retention import get_retention_data
from .ctr import get_ctr_metrics
```

**Discovered during:** Phase 49-02 Task 2 smoke test
**Root cause phase:** Phase 48-02 (import rewrite)
**Correct phase to fix:** Phase 48 cleanup or Phase 50 (Error Handling)
**Commit to reference:** b6e9cb6 (rename phase), 3f4a870 (48-02 import rewrites)
