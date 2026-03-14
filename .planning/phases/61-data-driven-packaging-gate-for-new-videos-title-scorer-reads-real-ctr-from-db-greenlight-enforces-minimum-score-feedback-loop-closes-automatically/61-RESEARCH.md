# Phase 61: Data-Driven Packaging Gate — Research

**Researched:** 2026-03-13
**Domain:** Python CLI tooling, SQLite, title scoring, CTR feedback loop integration
**Confidence:** HIGH

---

## Summary

Phase 61 wires real per-title CTR data from the database into the scoring pipeline and closes the feedback loop so the system learns from every publish event automatically. Currently `title_scorer.py` uses hardcoded pattern scores derived from a single manual data collection (2026-02-23). The `/greenlight` command enforces a 65+ minimum but relies on those static weights. When a new video is published and its CTR lands in YouTube Studio, that data is never written back to influence future scoring.

The three integration points this phase must connect are: (1) `tools/discovery/keywords.db` → `ctr_snapshots` and `video_performance` tables, which already store per-video CTR when manually entered; (2) `tools/title_scorer.py`, which reads only its own hardcoded constants; and (3) `tools/preflight/scorer.py` and `.claude/commands/greenlight.md`, which call `score_title()` and gate project creation on the result.

The primary work is: extend `title_scorer.py` to query the DB for pattern-level CTR averages and use those in place of (or weighted against) the static constants; extend `greenlight.md` and `scorer.py` to enforce a DB-informed minimum; and add a post-publish write path that captures CTR from the POST-PUBLISH-ANALYSIS files and stores it against the title pattern that was live at publish time.

**Primary recommendation:** Build a `TitleCTRStore` module that reads/writes CTR by title pattern from `keywords.db`, inject it as an optional enhancement into `title_scorer.py` (static constants remain the fallback when DB is empty), and add a `--record-ctr` flag to `title_scorer.py` or a new `record_publish.py` entry point that closes the loop after each publish.

---

## Current System Audit

### title_scorer.py — Current State

Location: `tools/title_scorer.py`
Invocation: `python -m tools.title_scorer "Title Here"`

**What it does now:**
- Detects pattern (versus, declarative, how_why, question, colon, the_x_that)
- Looks up hardcoded `PATTERN_SCORES` dict (derived from manual audit, static)
- Applies fixed penalties: YEAR_PENALTY = -50, COLON_PENALTY = -50, THE_X_THAT_PENALTY = -50
- Applies bonuses for specific numbers (+10) and active verbs (+5)
- Returns grade: REJECTED / A / B / C / D / F
- Minimum to pass: 65 (enforced by PACKAGING_MANDATE.md and `/greenlight`)

**Current hardcoded CTR data (from 2026-02-23 snapshot):**
```python
PATTERN_SCORES = {
    'versus': 75,      # ~3.7% CTR, n=2 verified
    'declarative': 65, # 3.8% CTR, n=19 — most reliable
    'how_why': 55,     # 3.3% CTR, n=5
    'question': 45,    # 2.4% CTR, n=1 — LOW confidence
    'colon': 30,       # 2.3% CTR — confirmed penalty
    'the_x_that': 10,  # no data — assumed worst
}
```

**The gap:** These scores never update. As more videos are published and CTR data enters the DB, the static scores become stale.

### greenlight.md — Current State

Location: `.claude/commands/greenlight.md`
Calls: `from tools.title_scorer import score_title`

**What it does now:**
- Imports `score_title()` directly — no DB query
- Enforces: GO if best title ≥ 65, REVIEW if any component is CAUTION, STOP if best title < 40
- The 65 minimum is hardcoded in the command prose, not enforced programmatically

**The gap:** greenlight has no awareness of whether the 65 threshold reflects actual observed CTR. The threshold is a policy constant, not data-derived.

### preflight/scorer.py — Current State

Location: `tools/preflight/scorer.py`
Weights: `title: 0.25` of composite preflight score

**What it does now:**
- Calls `score_title()` from `title_scorer.py` to evaluate title candidates extracted from `YOUTUBE-METADATA.md`
- Uses title score to compute a weighted composite with topic (20%), script (25%), thumbnail (15%), duration (15%)
- Gate threshold: 70+ composite = READY

**The gap:** Same as above — `score_title()` is called with no DB injection, so the title gate is static.

### CTR Data in the DB — Current State

**`keywords.db` → `video_performance` table:**
- Stores: `video_id`, `title`, `views`, `conversion_rate`, `topic_type`, `angles`, `published_at`
- Does NOT store: `ctr_percent` (this column is missing from `video_performance`)
- CTR data flows through `ctr_snapshots` table only

**`keywords.db` → `ctr_snapshots` table (Phase 27):**
- Stores: `video_id`, `snapshot_date`, `ctr_percent`, `impression_count`, `view_count`
- `add_ctr_snapshot()` exists in `database.py` — validated input
- `get_ctr_snapshots(video_id)` returns per-video history
- `get_channel_ctr_benchmarks()` returns averages grouped by `topic_type`

**The gap:** `ctr_snapshots` stores CTR per video, not per title pattern. To compute pattern-level CTR averages from DB, you need to: (1) look up each video's title, (2) detect its pattern, (3) group by pattern, (4) average `ctr_percent`. This join is not currently built anywhere.

**Critical finding:** The YouTube API does NOT expose impressions or CTR — confirmed in `ctr_tracker.py` comments: "Since the YouTube Analytics API does NOT expose impressions or CTR (those are YouTube Studio only)". CTR data enters the system only via manual entry from YouTube Studio or via `add_ctr_snapshot()` calls. The feedback loop must be triggered manually (or by parsing POST-PUBLISH-ANALYSIS files that contain CTR when entered).

**CTR in POST-PUBLISH-ANALYSIS files:** Looking at actual files, CTR shows as "Not available via API" in API-generated analyses. CTR is present in `CROSS-VIDEO-SYNTHESIS.md` master table (manually entered). So the primary CTR source for the DB is that manually-maintained table, not the API.

### CROSS-VIDEO-SYNTHESIS.md — The Real CTR Source

Location: `channel-data/patterns/CROSS-VIDEO-SYNTHESIS.md`
Format: Markdown table with columns: Title | Views | Retention | CTR | Impressions | Subs | Type

This file already contains CTR for 31 videos (some marked n/a). The `retitle_audit.py` and `retitle_gen.py` tools already parse it via `_parse_synthesis_table()`. This is the authoritative CTR source for Phase 61's DB ingestion.

### retitle_audit.py — Already Does Half the Job

Location: `tools/retitle_audit.py`

This tool (built for Phase 60) already:
- Parses `CROSS-VIDEO-SYNTHESIS.md` master table
- Extracts per-video CTR + impressions
- Computes "wasted impressions" = impressions × (target_CTR - actual_CTR)
- Outputs prioritized retitle list

Phase 61 can reuse or extend its parsing logic to feed CTR into the DB.

---

## Architecture Patterns

### Pattern 1: DB-Backed Pattern Scoring (Enhancement, Not Replacement)

The static `PATTERN_SCORES` dict stays as the fallback. A new `TitleCTRStore` class (or module-level function) queries `keywords.db` for actual CTR grouped by pattern and returns overrides where n ≥ 3 (minimum sample threshold).

```python
# tools/title_ctr_store.py (new module)
def get_pattern_scores_from_db(db_path=None, min_sample=3) -> dict:
    """
    Query ctr_snapshots + video title patterns to compute actual avg CTR per pattern.
    Returns override dict; empty if insufficient data.
    """
    # 1. Fetch all (video_id, ctr_percent) from ctr_snapshots (latest per video)
    # 2. Fetch all (video_id, title) from video_performance
    # 3. For each video, detect_pattern(title)
    # 4. Group by pattern, average ctr_percent, filter n >= min_sample
    # 5. Convert CTR% to 0-100 score using linear mapping
    # Returns: {'declarative': 67, 'versus': 78, ...} — only patterns with enough data
```

`title_scorer.py` uses it like:

```python
def score_title(title: str, db_path=None) -> dict:
    db_overrides = {}
    if db_path is not None:
        try:
            db_overrides = get_pattern_scores_from_db(db_path)
        except Exception:
            pass  # Silent fallback to static scores
    pattern = detect_pattern(title)
    base = db_overrides.get(pattern) or PATTERN_SCORES.get(pattern, 50)
    ...
```

This approach ensures backward compatibility — `score_title("Title")` with no `db_path` behaves identically to the current implementation.

### Pattern 2: CTR Ingestion from CROSS-VIDEO-SYNTHESIS.md

A new `ingest_ctr_from_synthesis.py` (or flag on backfill.py) reads the master table and writes rows to `ctr_snapshots`:

```python
# Pseudocode
for row in parse_synthesis_table(synthesis_path):
    if row['ctr'] is not None and row['video_id']:
        db.add_ctr_snapshot(
            video_id=row['video_id'],
            ctr_percent=row['ctr'],
            impression_count=row['impressions'] or 0,
            view_count=row['views'],
            snapshot_date=row['publish_date'] or '2026-02-23',  # single-snapshot fallback
        )
```

This populates the DB from the already-complete manual data. Once populated, `get_channel_ctr_benchmarks()` becomes meaningful.

### Pattern 3: Greenlight Minimum Score Enforcement

The current greenlight command reads the score but compares it to a hardcoded `65`. Make this a queryable constant:

```python
# tools/preflight/constants.py (new or extend existing)
GREENLIGHT_TITLE_MIN = 65   # static floor
```

Pass `db_path` to `score_title()` so the greenlight command benefits from live CTR data without changing the threshold logic. The threshold itself (65) stays static unless the planner decides to derive it from data.

### Pattern 4: Post-Publish CTR Record (Closing the Loop)

When the user runs `/analyze --post-publish` or saves a POST-PUBLISH-ANALYSIS file with CTR data, a write path should automatically store that CTR to `ctr_snapshots`. The `feedback_parser.py` already parses these files but currently only captures retention/lessons, not CTR.

Extend `feedback_parser.py` to also extract CTR and impressions from POST-PUBLISH-ANALYSIS files, then call `add_ctr_snapshot()`.

The alternative (simpler) approach: when `retitle_audit.py` parses CROSS-VIDEO-SYNTHESIS.md for Phase 60's audit, it already has CTR data. A `--ingest` flag on retitle_audit.py could write that data to the DB as a side effect.

---

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| sqlite3 | stdlib | DB queries | Already used everywhere via KeywordDB |
| re | stdlib | Pattern detection | Already in title_scorer.py |
| pathlib | stdlib | File paths | Project standard |
| argparse | stdlib | CLI | Project standard (Phase 51) |

### Existing Modules to Reuse
| Module | Location | What to Reuse |
|--------|----------|---------------|
| `KeywordDB` | `tools/discovery/database.py` | `add_ctr_snapshot()`, `get_ctr_snapshots()`, `get_channel_ctr_benchmarks()` |
| `detect_pattern()` | `tools/title_scorer.py` | Extract to importable function for `title_ctr_store.py` |
| `_parse_synthesis_table()` | `tools/retitle_audit.py` | Reuse for CTR ingestion (or extract to shared util) |
| `setup_logging()` | `tools/logging_config.py` | Project standard logging |

**No new dependencies needed.** This is all stdlib + existing project code.

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| CTR parsing from synthesis table | New parser | Extend `retitle_audit._parse_synthesis_table()` | Already parses the format correctly |
| DB write for CTR snapshots | New DB layer | `KeywordDB.add_ctr_snapshot()` | Validated, atomic, already exists |
| Pattern detection | Re-implement | Import `detect_pattern()` from `title_scorer.py` | Canonical definition already correct |
| CLI argument handling | Custom sys.argv | `argparse` with `--verbose`/`--quiet` (Phase 51 standard) | Consistent with all other tools |
| Channel CTR aggregation | Manual SQL | `KeywordDB.get_channel_ctr_benchmarks()` | Already groups by topic_type |

---

## Common Pitfalls

### Pitfall 1: CTR Null Values in ctr_snapshots
**What goes wrong:** Many videos have `ctr_percent = 0` because `ctr_tracker.py` stores 0 when it takes view-velocity snapshots (it can't get CTR from the API). Aggregating all `ctr_snapshots` rows would dilute real CTR data with zero-valued API snapshots.
**How to avoid:** Filter `WHERE ctr_percent > 0` when computing pattern averages. Or add a column `is_manual_entry BOOLEAN` and filter on it.
**Warning signs:** Pattern averages come out near 0% despite good individual videos.

### Pitfall 2: Missing video_id Linkage Between Title and CTR
**What goes wrong:** `ctr_snapshots` has `video_id` + `ctr_percent`. `video_performance` has `video_id` + `title`. But some videos in `ctr_snapshots` may not have a matching row in `video_performance` (if CTR was entered before performance backfill ran). The LEFT JOIN between them must handle NULLs.
**How to avoid:** `LEFT JOIN video_performance vp ON cs.video_id = vp.video_id`, skip rows where `vp.title IS NULL`.

### Pitfall 3: Threshold Drift
**What goes wrong:** If DB-driven pattern scores are used to update the base scores, and the minimum threshold (65) remains static, a pattern might be systematically "easier" to pass if its real CTR improved. The grade system would no longer reflect relative difficulty.
**How to avoid:** Keep static PATTERN_SCORES as the calibration anchor. DB scores are additive adjustments (weighted blend), not direct replacements.

### Pitfall 4: Small Sample Bias
**What goes wrong:** If only 2 videos use a 'question' title pattern, averaging their CTR (one might be 9.46% like JD Vance — an outlier) would massively inflate the pattern score.
**How to avoid:** Enforce `min_sample=3` before using DB overrides for a pattern. Below that threshold, fall back to the static score.

### Pitfall 5: CTR Data Is a Single Snapshot, Not a Time Series
**What goes wrong:** CTR changes over a video's lifetime (high at launch, lower as algorithm stops promoting). A single snapshot date misrepresents the "packaging signal" CTR.
**How to avoid:** Document this limitation. Use the 48h post-publish CTR as the canonical packaging metric (this is what SWAP-PROTOCOL.md already uses). When ingesting from CROSS-VIDEO-SYNTHESIS, treat the data as directional, not precise.

### Pitfall 6: import cycle risk
**What goes wrong:** If `title_scorer.py` imports from `tools.title_ctr_store`, and `title_ctr_store` imports from `tools.discovery.database`, and something in the discovery package imports from title tools — circular import.
**How to avoid:** `title_ctr_store.py` should only import from `tools.discovery.database` (low-level), never from other `tools.*` modules. `title_scorer.py` imports `title_ctr_store` optionally (try/except). Use the established lazy import pattern from Phase 48.

---

## Code Examples

### Query CTR by Pattern (Core Logic)
```python
# Source: derived from KeywordDB._ensure_ctr_snapshots_table() schema
# and get_channel_ctr_benchmarks() pattern in tools/discovery/database.py

import sqlite3
from tools.title_scorer import detect_pattern

def get_pattern_ctr_from_db(db_path: str, min_sample: int = 3) -> dict:
    """Return {pattern: score_0_to_100} for patterns with enough data."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        rows = conn.execute("""
            SELECT vp.title, cs.ctr_percent
            FROM ctr_snapshots cs
            JOIN video_performance vp ON cs.video_id = vp.video_id
            WHERE cs.ctr_percent > 0
              AND vp.title IS NOT NULL
              AND cs.snapshot_date = (
                  SELECT MAX(snapshot_date) FROM ctr_snapshots
                  WHERE video_id = cs.video_id AND ctr_percent > 0
              )
        """).fetchall()
    finally:
        conn.close()

    from collections import defaultdict
    by_pattern = defaultdict(list)
    for row in rows:
        pattern = detect_pattern(row['title'])
        by_pattern[pattern].append(row['ctr_percent'])

    # Convert CTR% to 0-100 score (calibrated: 3.8% CTR = 65, 5%+ = 90)
    CTR_TO_SCORE = lambda ctr: min(100, max(0, int(ctr * 17)))

    return {
        pattern: CTR_TO_SCORE(sum(values) / len(values))
        for pattern, values in by_pattern.items()
        if len(values) >= min_sample
    }
```

### Ingest CTR from CROSS-VIDEO-SYNTHESIS.md
```python
# Source: extends _parse_synthesis_table() from tools/retitle_audit.py

from tools.discovery.database import KeywordDB
from tools.retitle_audit import _parse_synthesis_table
from pathlib import Path

def ingest_synthesis_ctr(synthesis_path: Path, db: KeywordDB) -> dict:
    """
    Read master table from CROSS-VIDEO-SYNTHESIS.md and store CTR rows.
    Returns {'written': N, 'skipped': N, 'errors': [...]}.
    """
    videos = _parse_synthesis_table(synthesis_path)
    written, skipped, errors = 0, 0, []
    for v in videos:
        if not v.get('video_id') or v.get('ctr') is None:
            skipped += 1
            continue
        result = db.add_ctr_snapshot(
            video_id=v['video_id'],
            ctr_percent=v['ctr'],
            impression_count=v.get('impressions') or 0,
            view_count=v.get('views') or 0,
            snapshot_date='2026-02-23',  # single-collection-date data
        )
        if 'error' in result:
            errors.append(result)
        else:
            written += 1
    return {'written': written, 'skipped': skipped, 'errors': errors}
```

### Greenlight Command Integration
```python
# Source: .claude/commands/greenlight.md current pattern
# Updated call pattern:

from tools.title_scorer import score_title
from tools.discovery.database import KeywordDB

db = KeywordDB()  # keywords.db
result = score_title(title, db_path=db.db_path)
# Threshold remains 65 — enforced by PACKAGING_MANDATE.md policy
if result['score'] >= 65 and not result['hard_rejects']:
    print("TITLE: GO")
else:
    print("TITLE: REVIEW")
```

---

## State of the Art

| Old Approach | Current Approach | What Phase 61 Adds |
|--------------|------------------|-------------------|
| Static pattern scores from one audit | Static + manual re-audit when patterns change | Static as fallback + live DB scores when n≥3 |
| No post-publish write path | Manual entry into CROSS-VIDEO-SYNTHESIS.md | Ingestion from synthesis file into DB on demand |
| Greenlight enforces static 65 | Same | Same threshold, but scores informed by real data |
| title_scorer reads no DB | Same | Optional db_path param; DB enriches base scores |

---

## Open Questions

1. **Where does the video_id live in CROSS-VIDEO-SYNTHESIS.md?**
   - What we know: The table has Title, Views, Retention, CTR, Impressions, Subs, Type columns.
   - What's unclear: There is no video_id column in the synthesis table. `retitle_audit.py` has a hardcoded `CANDIDATES` dict mapping video_ids to metadata, but `_parse_synthesis_table()` only gets the title.
   - Recommendation: In Phase 61, the ingestion step needs to resolve video_id from title using a lookup against `video_performance.title`. Add a fuzzy-match lookup (title substring match against DB) as the bridge. Alternatively, add video_id column to CROSS-VIDEO-SYNTHESIS.md during Phase 60 work.

2. **Should the 65 minimum threshold be data-derived or policy-fixed?**
   - What we know: 65 corresponds to declarative pattern base score (3.8% CTR, n=19). This is the most reliable pattern.
   - What's unclear: As more data accumulates, should the threshold rise? Or is it a floor regardless of what data shows?
   - Recommendation: Keep 65 as a policy constant in Phase 61. Add a `compute_recommended_threshold()` function that outputs the data-derived suggestion for the user to consider, but do not auto-update the gate.

3. **Is feedback_parser.py the right place to close the loop?**
   - What we know: `feedback_parser.py` already parses POST-PUBLISH-ANALYSIS files. Most API-generated files show "CTR: Not available via API."
   - What's unclear: If CTR is manually added to POST-PUBLISH-ANALYSIS files, does the parser currently extract it?
   - Recommendation: Check one file where CTR was manually entered (e.g., from CROSS-VIDEO-SYNTHESIS data). If the markdown structure is consistent, extend feedback_parser.py to extract CTR and impressions. If not, use the synthesis table ingestion as the primary path.

---

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | pytest |
| Config file | pyproject.toml (`testpaths = ["tests"]`) |
| Quick run command | `pytest tests/ -x -q` |
| Full suite command | `pytest tests/ -v` |

### Phase Requirements → Test Map
| Behavior | Test Type | File |
|----------|-----------|------|
| `get_pattern_ctr_from_db()` returns correct averages grouped by pattern | unit | `tests/unit/test_title_ctr_store.py` |
| `get_pattern_ctr_from_db()` falls back gracefully when DB empty | unit | same |
| `get_pattern_ctr_from_db()` skips patterns below min_sample threshold | unit | same |
| `score_title()` with db_path uses DB scores over static | unit | `tests/unit/test_title_scorer_db.py` |
| `score_title()` without db_path behaves identically to current | unit | same |
| CTR rows with `ctr_percent = 0` are excluded from averages | unit | `tests/unit/test_title_ctr_store.py` |
| Ingest function writes correct rows to DB and returns count | integration | `tests/integration/test_ctr_ingest.py` |
| Greenlight command produces GO when best title ≥ 65 with DB enrichment | smoke | manual |

### Sampling Rate
- **Per task commit:** `pytest tests/unit/test_title_ctr_store.py tests/unit/test_title_scorer_db.py -x -q`
- **Per wave merge:** `pytest tests/ -v`
- **Phase gate:** Full suite green before marking phase complete

### Wave 0 Gaps
- [ ] `tests/unit/test_title_ctr_store.py` — unit tests for TitleCTRStore / `get_pattern_ctr_from_db()`
- [ ] `tests/unit/test_title_scorer_db.py` — unit tests for `score_title()` with `db_path` param
- [ ] `tests/integration/test_ctr_ingest.py` — integration test for synthesis → DB ingest

---

## Sources

### Primary (HIGH confidence)
- `tools/title_scorer.py` — read directly, full code audit
- `tools/discovery/database.py` — read directly, `ctr_snapshots` schema and methods confirmed
- `tools/youtube_analytics/ctr_tracker.py` — read directly, confirmed API does NOT expose CTR
- `.claude/commands/greenlight.md` — read directly, full workflow audit
- `tools/preflight/scorer.py` — read directly, title gate weight confirmed (0.25)
- `tools/PACKAGING_MANDATE.md` — read directly, 65+ minimum confirmed
- `channel-data/patterns/CROSS-VIDEO-SYNTHESIS.md` — read directly, CTR data format confirmed
- `tools/retitle_audit.py` — read directly, `_parse_synthesis_table()` implementation confirmed

### Secondary (MEDIUM confidence)
- `tools/youtube_analytics/backfill.py` — confirms CTR not in API responses, manual entry required
- `channel-data/analyses/POST-PUBLISH-ANALYSIS-*.md` — sample files confirmed "CTR: Not available via API"

---

## Metadata

**Confidence breakdown:**
- Current system audit: HIGH — all files read directly
- DB schema: HIGH — confirmed from database.py source
- CTR data source: HIGH — confirmed API limitation from ctr_tracker.py docstring
- Architecture patterns: HIGH — directly derived from existing code patterns in project
- Open questions: MEDIUM — video_id linkage gap in synthesis table is a real unresolved issue

**Research date:** 2026-03-13
**Valid until:** 2026-06-13 (stable tooling, no external dependencies)
