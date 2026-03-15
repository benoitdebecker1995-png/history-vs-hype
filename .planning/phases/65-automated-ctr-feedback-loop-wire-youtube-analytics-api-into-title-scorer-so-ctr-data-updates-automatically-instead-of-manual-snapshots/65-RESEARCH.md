# Phase 65: Automated CTR Feedback Loop - Research

**Researched:** 2026-03-15
**Domain:** YouTube Analytics API + Python scheduled automation (Windows)
**Confidence:** HIGH

---

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- **Data source:** API-first. Try YouTube Analytics API for all videos; fall back to manual entry for API failures.
- **Reuse `get_ctr_metrics()`** in `tools/youtube_analytics/ctr.py` — already queries `videoThumbnailImpressions` + `videoThumbnailImpressionsClickRate`.
- **Latest data wins.** Most recent snapshot (manual or API) is authoritative. No source precedence logic.
- **Google Issue #254665034** — some videos will not return CTR. Those are logged for manual entry.
- **Extend `ctr_tracker.py`**, do not create a separate tool.
- **Fetch CTR for all ~47 long-form videos every run** — one API batch fits within quota.
- **Also update view counts in `video_performance` table** since the API is already being hit.
- **Keep `ctr_ingest.py` + `CROSS-VIDEO-SYNTHESIS.md` as fallback** — do not deprecate manual pipeline.
- **Write to same `ctr_snapshots` table** — `title_ctr_store.py` already picks `MAX(snapshot_date)`.
- **Fully hands-off scheduled execution.** One-time manual OAuth browser flow to create `token.json`, then auto-refresh.
- **Refresh token stays alive** as long as the scheduled task keeps running (Google revokes after 6 months of no use).
- **End-of-run summary:** "CTR updated for X/47 videos. Title scorer now using DB-enriched scores: declarative=N, versus=N..."

### Claude's Discretion
- Scheduler platform choice (Windows Task Scheduler vs Python scheduler vs other)
- Refresh frequency (daily vs weekly — balance API quota vs data freshness)
- DB schema: whether to add `source` column to `ctr_snapshots` or use existing `is_late_entry` flag
- Zero CTR handling: threshold for filtering out insufficient-data videos
- Failed-fetch reporting: print summary vs write file vs log-only
- Error resilience: retry strategy, partial success handling
- Logging approach for unattended runs (log file vs stdout capture)
- API batching/rate limiting strategy for ~47 per-video Analytics API calls
- OAuth token expiry handling

### Deferred Ideas (OUT OF SCOPE)
None — discussion stayed within phase scope.
</user_constraints>

---

## Summary

Phase 65 extends the existing `ctr_tracker.py` to also fetch real CTR data (impressions + click rate) from the YouTube Analytics API for every long-form video, then stores the results into the existing `ctr_snapshots` table in `keywords.db`. The `title_ctr_store.py` → `title_scorer.py` → `greenlight` chain already reads from this table and picks `MAX(snapshot_date)` automatically, so once CTR rows land in the DB the entire downstream scoring chain upgrades without any code changes.

The key technical constraint is that the YouTube Analytics API does not support bulk CTR queries. CTR (`videoThumbnailImpressions`, `videoThumbnailImpressionsClickRate`) requires one `reports().query()` call per video. For ~47 videos this is ~47 sequential API calls, well within the default daily quota of 10,000 units (each query costs ~1–5 units). The existing `get_ctr_metrics()` function in `ctr.py` already handles graceful fallback when a video's CTR is unavailable via API.

Scheduling on Windows is best done via Windows Task Scheduler with a Python script invoked directly. The OAuth token auto-refreshes via `google-auth` as long as requests happen before Google's 6-month inactivity window. The end-of-run summary printed to stdout confirms the scorer is using fresh data.

**Primary recommendation:** Extend `take_snapshot()` in `ctr_tracker.py` to call `get_ctr_metrics()` per video and upsert CTR + impressions alongside existing view counts. Add a weekly Windows Task Scheduler trigger and a log file for unattended diagnostics.

---

## Standard Stack

### Core (already installed — no new dependencies)
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| `google-api-python-client` | existing | YouTube Analytics API calls | Already in pyproject.toml, used by `ctr.py` |
| `google-auth-oauthlib` | existing | OAuth2 flow + token management | Already in `auth.py` |
| `google-auth` | existing | Token auto-refresh via `Request()` | Already in `auth.py` |
| `sqlite3` | stdlib | Write to `keywords.db` ctr_snapshots | No new dep |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| Windows Task Scheduler | OS built-in | Unattended schedule trigger | Primary scheduler on Windows |
| `schtasks.exe` | OS built-in | CLI to create/modify Task Scheduler jobs | Script-based setup |
| Python `logging` + file handler | stdlib | Log file for unattended runs | All output must persist when no terminal present |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Windows Task Scheduler | `schedule` Python library | Python scheduler requires a long-running process; Task Scheduler is fire-and-forget and survives reboots |
| Windows Task Scheduler | `APScheduler` | Same issue — requires persistent process |
| Per-video `get_ctr_metrics()` calls | Bulk Analytics query | Bulk CTR query does not exist in YouTube Analytics API v2; per-video is the only option |
| Weekly refresh | Daily refresh | Weekly is sufficient — CTR data is lifetime cumulative, not session-specific. Daily wastes quota with marginal freshness gain |

**Installation:** No new packages required.

---

## Architecture Patterns

### Recommended Project Structure
No new files needed. Changes are contained to:
```
tools/
└── youtube_analytics/
    └── ctr_tracker.py   # Extend take_snapshot() + add CTR fetch + summary print
```

Optionally add a scheduler setup script:
```
tools/
└── youtube_analytics/
    └── setup_scheduler.py   # One-time Windows Task Scheduler registration
```

### Pattern 1: Extend `take_snapshot()` to Fetch CTR
**What:** After fetching view counts (which already works), loop through all `longform_ids` and call `get_ctr_metrics(video_id)` for each. Store `ctr_percent` and `impression_count` directly into the same `ctr_snapshots` row being written.

**When to use:** Every scheduled run.

**Key insight:** `store_snapshot()` currently writes `ctr_percent=0, impression_count=0` as placeholders. The fix is to populate these from the API result before calling `store_snapshot()`. If CTR is unavailable (`ctr_available: False`), store `0` as before (fallback behavior unchanged).

**Current `store_snapshot()` signature:**
```python
def store_snapshot(conn, video_id, views, snapshot_date):
    conn.execute(
        "INSERT INTO ctr_snapshots "
        "(video_id, snapshot_date, ctr_percent, impression_count, view_count, "
        " is_late_entry, recorded_at) "
        "VALUES (?, ?, 0, 0, ?, 0, ?)",
        ...
    )
```

**New signature (minimal change):**
```python
def store_snapshot(conn, video_id, views, snapshot_date,
                   ctr_percent=0.0, impression_count=0):
    conn.execute(
        "INSERT INTO ctr_snapshots "
        "(video_id, snapshot_date, ctr_percent, impression_count, view_count, "
        " is_late_entry, recorded_at) "
        "VALUES (?, ?, ?, ?, ?, 0, ?)",
        (video_id, snapshot_date, ctr_percent, impression_count, views, snapshot_date)
    )
```

### Pattern 2: Per-Video CTR Loop with Rate Limiting
**What:** After the batch view-count fetch, loop ~47 video IDs, call `get_ctr_metrics(vid)`, handle `ctr_available: True/False/error`. Add a small `time.sleep(0.1)` between calls to avoid burst quota consumption.

**When to use:** Inside the extended `take_snapshot()`.

```python
import time
from tools.youtube_analytics.ctr import get_ctr_metrics

ctr_results = {}
ctr_fetched = 0
ctr_unavailable = []

for vid in longform_ids:
    result = get_ctr_metrics(vid)
    if 'error' in result:
        logger.warning("CTR fetch error for %s: %s", vid, result['error'])
        ctr_unavailable.append(vid)
    elif result.get('ctr_available'):
        ctr_results[vid] = {
            'ctr_percent': result['ctr_percent'],
            'impression_count': result['impressions'],
        }
        ctr_fetched += 1
    else:
        ctr_unavailable.append(vid)
    time.sleep(0.1)

logger.info("CTR fetched for %d/%d videos. %d unavailable via API.",
            ctr_fetched, len(longform_ids), len(ctr_unavailable))
```

### Pattern 3: End-of-Run Summary (Locked Requirement)
**What:** After storing snapshots, call `get_pattern_ctr_from_db()` and print the live pattern scores.

```python
from tools.title_ctr_store import get_pattern_ctr_from_db

pattern_scores = get_pattern_ctr_from_db(str(DB_PATH))
if pattern_scores:
    score_str = ", ".join(f"{k}={v}" for k, v in sorted(pattern_scores.items()))
    print(f"CTR updated for {ctr_fetched}/{len(longform_ids)} videos. "
          f"Title scorer now using DB-enriched scores: {score_str}")
else:
    print(f"CTR updated for {ctr_fetched}/{len(longform_ids)} videos. "
          f"Title scorer using static scores (insufficient DB data).")
```

### Pattern 4: Log File for Unattended Runs
**What:** When running unattended (no TTY), direct log output to a rotating file alongside stdout capture.

**Implementation:** Add an optional `--log-file PATH` argument to the CLI. Windows Task Scheduler can also redirect stdout/stderr via the "Start In" + argument configuration.

**Simpler approach:** Windows Task Scheduler captures stdout/stderr if configured with `cmd /c "python -m tools.youtube_analytics.ctr_tracker >> logs\ctr_tracker.log 2>&1"`.

### Pattern 5: Windows Task Scheduler Setup
**What:** Register a weekly trigger using `schtasks.exe`.

```batch
schtasks /Create /TN "HistoryVsHype\CTRTracker" ^
  /TR "cmd /c cd /D D:\History vs Hype && python -m tools.youtube_analytics.ctr_tracker >> logs\ctr_tracker.log 2>&1" ^
  /SC WEEKLY /D MON /ST 09:00 ^
  /F
```

Note: The `/D "History vs Hype"` working directory is required so relative DB paths resolve correctly. Use `/F` to overwrite if job already exists.

**Claude's Discretion: Recommended frequency — weekly (Monday 09:00).** Rationale: CTR data is lifetime cumulative (changes slowly), and the channel publishes roughly weekly. Daily runs provide negligible freshness gain for ~47 stable videos and waste OAuth calls.

### Anti-Patterns to Avoid
- **Don't create a separate scheduler script** — extend `ctr_tracker.py` as locked.
- **Don't add source precedence logic** — `title_ctr_store.py` already picks `MAX(snapshot_date)`, so latest wins automatically.
- **Don't add a `source` column to `ctr_snapshots`** — the existing `is_late_entry` flag already distinguishes manual (`is_late_entry=1`) from API rows (`is_late_entry=0`). Adding a `source` column adds migration complexity for no practical benefit. Use `is_late_entry=0` for API-sourced rows.
- **Don't fail the whole run if one video fails** — `get_ctr_metrics()` already returns `{'error': ...}` without raising. Log the failure, continue the loop, report in the summary.
- **Don't try to retry on quota errors** — YouTube Analytics API quota resets after 24 hours. On quota error, abort the run, log it, and let the scheduler retry next week.

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| CTR fetch with fallback | Custom Analytics query | `get_ctr_metrics()` in `ctr.py` | Already handles HTTP 400/403, graceful fallback, CTR conversion (rate → percent), all edge cases |
| OAuth token management | Custom refresh logic | `auth.py` `get_credentials()` | Already handles load, refresh, browser flow, token save |
| CTR storage | Direct SQL inserts | `db.add_ctr_snapshot()` in `database.py` | Validates ranges, handles `recorded_at`, matches schema exactly |
| Pattern scoring | Custom aggregation | `get_pattern_ctr_from_db()` | Already groups by pattern, applies min_sample filter, calibrates to 0-100 scale |
| View count fetch | Per-video Data API | `fetch_view_counts()` (batch 50) | Already batches 50 at a time, much faster than Analytics API |

**Key insight:** The entire pipeline — fetch → store → score → report — is already built. This phase wires the missing segment: CTR fetch inside the snapshot loop.

---

## Common Pitfalls

### Pitfall 1: `recorded_at` Field Uses Date Not Datetime
**What goes wrong:** `store_snapshot()` sets `recorded_at = snapshot_date` (a date string). `add_ctr_snapshot()` also sets `recorded_at = datetime.now().date().isoformat()`. Both are ISO date strings, not full timestamps. This is intentional in the schema but inconsistent with the column name.
**Why it happens:** Schema defined `recorded_at` as TEXT, no constraint on format.
**How to avoid:** Match the existing `store_snapshot()` pattern — pass `snapshot_date` as `recorded_at`. Do not change the format.

### Pitfall 2: Duplicate Snapshot Guard Only Checks View Count Rows
**What goes wrong:** `take_snapshot()` checks `COUNT(*) FROM ctr_snapshots WHERE snapshot_date = ?` before running. If view-count rows already exist for today but CTR rows don't, the guard fires and skips the CTR fetch entirely.
**Why it happens:** The guard was written before CTR was added to this function.
**How to avoid:** The existing guard is correct behavior — if a snapshot already ran today, skip entirely. This is idempotency. The weekly schedule prevents same-day re-runs in normal operation. If a forced re-run is needed, delete today's rows manually.

### Pitfall 3: YouTube Analytics CTR Returns Rate, Not Percent
**What goes wrong:** `videoThumbnailImpressionsClickRate` returns a decimal (e.g., `0.042` = 4.2%). Storing this directly as `ctr_percent` would make it 100x too small, breaking the `title_ctr_store.py` calibration formula (`ctr_percent * 17`).
**Why it happens:** API naming is misleading. The field is a ratio, not a percentage.
**How to avoid:** `get_ctr_metrics()` already converts: `ctr_percent = round(float(ctr_rate) * 100, 2)`. Always use `get_ctr_metrics()` output, not raw API values.
**Warning signs:** Pattern scores of 0 or 1 when they should be 60-80.

### Pitfall 4: `get_ctr_metrics()` Builds a New Auth Service on Every Call
**What goes wrong:** For 47 videos, `get_ctr_metrics()` calls `get_authenticated_service()` 47 times, which calls `get_credentials()` 47 times, which checks and potentially writes `token.json` 47 times.
**Why it happens:** `get_ctr_metrics()` is designed as a stateless function.
**How to avoid:** Build the Analytics service once before the loop and pass it in, or accept the overhead (token.json reads are cheap file I/O; no network round trip after first call since credentials object is valid). At 47 calls this is acceptable. No change needed unless profiling shows a real bottleneck.

### Pitfall 5: Windows Task Scheduler Working Directory
**What goes wrong:** `python -m tools.youtube_analytics.ctr_tracker` fails because relative paths (DB paths, credentials) resolve from the wrong directory.
**Why it happens:** Task Scheduler's default working directory is `System32`, not the project root.
**How to avoid:** Always set "Start In" to `D:\History vs Hype` in the Task Scheduler action, or use `cd /D "D:\History vs Hype" &&` in the command.

### Pitfall 6: Google Revokes Refresh Token After 6 Months of Inactivity
**What goes wrong:** Scheduled task stops running (holiday, PC off), token expires, next run fails with `RefreshError`.
**Why it happens:** Google automatically revokes OAuth refresh tokens inactive for 6+ months.
**How to avoid:** `auth.py` already handles `RefreshError` — sets `creds = None` and re-enters the browser flow. For unattended runs this means the task will fail and the log will show `RefreshError`. Add a clear log message: "Refresh token revoked — run `python -m tools.youtube_analytics.auth` interactively to re-authorize." The log file will capture this.

### Pitfall 7: `view_count` in `video_performance` vs `ctr_snapshots`
**What goes wrong:** The CONTEXT.md states to "also update view counts in `video_performance` table." But `ctr_tracker.py` stores views in `ctr_snapshots`, not in `video_performance`. These are different tables in different DBs (`keywords.db` vs `analytics.db`).
**Why it happens:** The context note may mean updating the `videos` table in `analytics.db`, or it may mean the `view_count` column in `ctr_snapshots` rows.
**How to avoid:** The `ctr_snapshots` rows already store `view_count` as part of each snapshot. The `video_performance` table in `keywords.db` is for title/variant tracking and is populated by `ctr_ingest.py`. No additional `video_performance` write is needed from `ctr_tracker.py`. Verify intent during planning: if updating `analytics.db` `videos.views` is intended, that requires a separate `growth_data.py` call and is out of phase scope.

---

## Code Examples

### Minimal CTR Fetch Loop (Verified from existing codebase)
```python
# Source: ctr.py get_ctr_metrics() + ctr_tracker.py take_snapshot() pattern

from tools.youtube_analytics.ctr import get_ctr_metrics
import time

ctr_map = {}          # video_id -> {'ctr_percent': float, 'impression_count': int}
ctr_unavailable = []  # video_ids where CTR not available

for vid in longform_ids:
    result = get_ctr_metrics(vid)
    if 'error' in result:
        logger.warning("CTR error for %s: %s", vid, result.get('error'))
        ctr_unavailable.append(vid)
    elif result.get('ctr_available'):
        ctr_map[vid] = {
            'ctr_percent': result['ctr_percent'],
            'impression_count': result['impressions'],
        }
    else:
        ctr_unavailable.append(vid)
    time.sleep(0.1)
```

### Extended `store_snapshot()` Signature
```python
# Backward-compatible extension — existing callers use default ctr_percent=0

def store_snapshot(conn: sqlite3.Connection, video_id: str,
                   views: int, snapshot_date: str,
                   ctr_percent: float = 0.0,
                   impression_count: int = 0) -> None:
    conn.execute(
        "INSERT INTO ctr_snapshots "
        "(video_id, snapshot_date, ctr_percent, impression_count, view_count, "
        " is_late_entry, recorded_at) "
        "VALUES (?, ?, ?, ?, ?, 0, ?)",
        (video_id, snapshot_date, ctr_percent, impression_count, views, snapshot_date)
    )
```

### End-of-Run Summary Print
```python
# Source: title_ctr_store.py get_pattern_ctr_from_db()

from tools.title_ctr_store import get_pattern_ctr_from_db

pattern_scores = get_pattern_ctr_from_db(str(DB_PATH))
total = len(longform_ids)
fetched = len(ctr_map)

if pattern_scores:
    score_str = ", ".join(
        f"{k}={v}" for k, v in sorted(pattern_scores.items())
    )
    print(f"CTR updated for {fetched}/{total} videos. "
          f"Title scorer now using DB-enriched scores: {score_str}")
else:
    print(f"CTR updated for {fetched}/{total} videos. "
          f"Title scorer using static scores (insufficient DB data).")

if ctr_unavailable:
    print(f"Manual entry needed for {len(ctr_unavailable)} videos "
          f"(API returned no CTR): {', '.join(ctr_unavailable)}")
```

### Windows Task Scheduler Registration (schtasks)
```batch
schtasks /Create ^
  /TN "HistoryVsHype\CTRTracker" ^
  /TR "cmd /c cd /D \"D:\History vs Hype\" && python -m tools.youtube_analytics.ctr_tracker >> logs\ctr_tracker.log 2>&1" ^
  /SC WEEKLY /D MON /ST 09:00 ^
  /F
```

---

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Manual CROSS-VIDEO-SYNTHESIS.md → `ctr_ingest.py` | API fetch in `ctr_tracker.py` on schedule | Phase 65 | Eliminates human intervention; data refreshes without user action |
| `ctr_percent=0` placeholder in snapshot rows | Real CTR from Analytics API | Phase 65 | `title_ctr_store.py` scores become live instead of based on one historical snapshot |
| Static pattern scores in `title_scorer.py` | DB-enriched scores via `title_ctr_store.py` | Phase 61 | Pattern scores already auto-update from DB; Phase 65 automates the DB population |

**Deprecated/outdated:**
- Nothing is being removed. `ctr_ingest.py` + manual pipeline stays as the safety net for videos where API returns no CTR.

---

## Open Questions

1. **`video_performance` table update scope**
   - What we know: CONTEXT.md says "also update view counts in `video_performance` table." The `ctr_snapshots` table already stores `view_count` per snapshot. The `video_performance` table is in `keywords.db` and tracks title variants.
   - What's unclear: Does this mean the `analytics.db` `videos.views` column, or the `view_count` within `ctr_snapshots` rows (which is already handled)?
   - Recommendation: Planner should clarify. The safest interpretation is that `view_count` in each `ctr_snapshots` row (already in `store_snapshot()`) satisfies this. Updating `analytics.db` would require calling `growth_data.py` fetch logic and is likely out of scope.

2. **Zero CTR threshold for filtering**
   - What we know: `title_ctr_store.py` already filters `WHERE ctr_percent > 0` so zero rows do not pollute pattern scores.
   - What's unclear: Should videos with `impression_count < N` also be excluded from pattern scoring? Current `min_sample=3` filters by number of videos per pattern, not per-video impression count.
   - Recommendation: No change needed. Current `> 0` filter and `min_sample` adequately handle noise. Document this in the summary output.

3. **`logs/` directory existence**
   - What we know: The Task Scheduler command redirects to `logs\ctr_tracker.log`.
   - What's unclear: Does this directory exist in the repo root?
   - Recommendation: Create `D:\History vs Hype\logs\.gitkeep` as a Wave 0 task, or handle in setup script.

---

## Validation Architecture

> `workflow.nyquist_validation` key is absent from `.planning/config.json` — treating as enabled.

### Test Framework
| Property | Value |
|----------|-------|
| Framework | pytest (existing, from pyproject.toml) |
| Config file | `pyproject.toml` `[tool.pytest.ini_options]` |
| Quick run command | `python -m pytest tests/youtube_analytics/test_ctr_tracker.py -x -q` |
| Full suite command | `python -m pytest tests/ -q` |

### Phase Requirements → Test Map
This phase has no formally assigned requirement IDs (null in CONTEXT). Behavioral requirements inferred from locked decisions:

| Behavior | Test Type | Automated Command | File Exists? |
|----------|-----------|-------------------|-------------|
| CTR fetch populates `ctr_percent` > 0 in snapshot rows | unit | `pytest tests/youtube_analytics/test_ctr_tracker.py::test_ctr_stored_in_snapshot -x` | Wave 0 |
| Unavailable CTR still writes `view_count` snapshot (fallback) | unit | `pytest tests/youtube_analytics/test_ctr_tracker.py::test_ctr_unavailable_fallback -x` | Wave 0 |
| API error for one video does not abort the loop | unit | `pytest tests/youtube_analytics/test_ctr_tracker.py::test_ctr_partial_failure -x` | Wave 0 |
| End-of-run summary prints pattern scores | unit | `pytest tests/youtube_analytics/test_ctr_tracker.py::test_summary_output -x` | Wave 0 |
| Duplicate snapshot guard still skips on same day | unit | `pytest tests/youtube_analytics/test_ctr_tracker.py::test_duplicate_guard -x` | Wave 0 |

### Sampling Rate
- **Per task commit:** `python -m pytest tests/youtube_analytics/test_ctr_tracker.py -x -q`
- **Per wave merge:** `python -m pytest tests/ -q`
- **Phase gate:** Full suite green before `/gsd:verify-work`

### Wave 0 Gaps
- [ ] `tests/youtube_analytics/test_ctr_tracker.py` — covers all 5 behaviors above
- [ ] Mock for `get_ctr_metrics()` needed (same pattern as existing analytics tests — mock at `tools.youtube_analytics.ctr_tracker.get_ctr_metrics`)
- [ ] In-memory SQLite fixture for `ctr_snapshots` (likely already exists in test conftest for Phase 61 tests — check `tests/conftest.py`)

---

## Sources

### Primary (HIGH confidence)
- Direct codebase inspection: `tools/youtube_analytics/ctr.py`, `ctr_tracker.py`, `auth.py`, `ctr_ingest.py`, `title_ctr_store.py`, `discovery/database.py`, `logging_config.py`
- `65-CONTEXT.md` — locked decisions and code context

### Secondary (MEDIUM confidence)
- `tools/youtube_analytics/growth_data.py` — confirms `fetch_all_video_ids()`, `fetch_video_metadata()` reuse pattern
- `.planning/STATE.md` Phase 61 decisions — confirms `is_late_entry`, `MAX(snapshot_date)`, `title_ctr_store.py` lazy import, calibration formula

### Tertiary (LOW confidence)
- Google Issue Tracker #254665034 — referenced in CONTEXT.md and `ctr.py` docstring; not independently verified in this session, but treated as confirmed given it is embedded in production code

---

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — all libraries already present and in active use
- Architecture: HIGH — all integration points are readable source code, not documentation
- Pitfalls: HIGH — most identified from direct code inspection (duplicate guard, rate conversion, recorder_at format), one from CONTEXT.md (token expiry)
- Scheduling: MEDIUM — Windows Task Scheduler approach is well-established but the specific command syntax needs validation on the actual machine

**Research date:** 2026-03-15
**Valid until:** 2026-04-15 (stable codebase; YouTube Analytics API v2 is mature)
