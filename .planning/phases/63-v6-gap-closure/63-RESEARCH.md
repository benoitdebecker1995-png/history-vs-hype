# Phase 63: v6.0 Gap Closure & Tech Debt - Research

**Researched:** 2026-03-15
**Domain:** Python tool integration, slash command wiring, documentation housekeeping
**Confidence:** HIGH

---

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| RETITLE-02 | `/retitle` generates script-based title candidates scored by title_scorer, outputs SWAP-CHECKLIST.md with old title, new title, new description, thumbnail concept | INT-01 fix wires DB-enriched scoring into Step 4c of retitle.md; currently using static scores only |
| GATE-02 | Title scorer integrates with DB for live CTR-based pattern scoring | Already implemented in greenlight/preflight/CLI; gap is retitle.md not passing db_path to score_title() |
</phase_requirements>

---

## Summary

Phase 63 is pure tech debt closure — no new features. The v6.0-MILESTONE-AUDIT.md identified 7 non-critical items across 4 categories: one integration gap (INT-01), one private attribute access bug (ctr_ingest.py), frontmatter gaps in 3 SUMMARY files, and a stale REQUIREMENTS.md traceability table.

The integration gap (INT-01) is the only item with functional impact: `/retitle` candidate scoring calls `score_title(t)` without `db_path`, so it uses static pattern scores even when live CTR data has been ingested into keywords.db. The fix is a two-line change in retitle.md Step 4c. All other items are documentation and code hygiene.

The `ctr_ingest.py` private attribute access (`db._conn.cursor()`) is fragile coupling — if KeywordDB ever changes its connection management, this silently breaks. The fix requires either a new thin public method on KeywordDB or using `get_all_video_performance()` with Python-side title filtering. The latter avoids adding new public surface area but is less efficient (loads all records). Adding a narrow `search_video_performance_by_title()` method is cleaner and matches the existing public-method pattern in database.py.

**Primary recommendation:** Four isolated tasks, each independently executable. Order: INT-01 fix first (highest functional impact), then ctr_ingest bug, then SUMMARY frontmatter, then REQUIREMENTS.md table update.

---

## Standard Stack

### Core (all already present — no new dependencies)

| File | Role | What Changes |
|------|------|-------------|
| `.claude/commands/retitle.md` | Slash command definition | Step 4c: add KeywordDB init + pass db_path to score_title() |
| `tools/ctr_ingest.py` | CTR ingestion library + CLI | `_lookup_video_id()`: replace `db._conn.cursor()` with public API |
| `tools/discovery/database.py` | KeywordDB public API | Optionally add `search_video_performance_by_title(prefix)` method |
| `.planning/phases/60-.../60-02-SUMMARY.md` | Phase 60 plan 02 summary | Add `requirements_completed: [RETITLE-04, RETITLE-05, RETITLE-06]` to frontmatter |
| `.planning/phases/61-.../61-02-SUMMARY.md` | Phase 61 plan 02 summary | Add `requirements_completed: [GATE-03]` to frontmatter |
| `.planning/phases/61-.../61-03-SUMMARY.md` | Phase 61 plan 03 summary | Add `requirements_completed: [GATE-04, GATE-05]` to frontmatter |
| `.planning/REQUIREMENTS.md` | Requirements traceability | Update stale "Not started" rows to "Complete" for phases 55-62 |

---

## Architecture Patterns

### INT-01 Fix Pattern

The fix mirrors exactly what `greenlight.md` and `scorer.py` already do (confirmed from 61-03-SUMMARY.md):

```python
# Pattern used in scorer.py and greenlight.md (Phase 61-03 decision)
from tools.discovery.database import KeywordDB
db = KeywordDB()
db_path = db.db_path
db.close()

# Then pass to score_title:
scored = [(t, score_title(t, db_path=db_path)) for t in all_options]
```

The `score_title()` signature is: `score_title(title: str, db_path: str = None) -> dict`
The `db_path=None` default means no change is needed for callers that omit it — backward compatible.

**Location in retitle.md:** Step 4c, currently:
```python
scored = [(t, score_title(t)) for t in all_options]
```
Must become:
```python
from tools.discovery.database import KeywordDB
_db = KeywordDB()
scored = [(t, score_title(t, db_path=_db.db_path)) for t in all_options]
_db.close()
```

### ctr_ingest.py Private Access Fix

**Current code (line 147-178):**
```python
def _lookup_video_id(db, title: str) -> str | None:
    prefix = title[:40].replace("'", "''")
    try:
        cursor = db._conn.cursor()  # FRAGILE: private attribute access
        cursor.execute(
            "SELECT video_id FROM video_performance WHERE title LIKE ? COLLATE NOCASE LIMIT 1",
            (f"%{prefix}%",),
        )
        row = cursor.fetchone()
        if row:
            return row[0]
    except Exception as exc:
        logger.warning("DB lookup error for title '%s': %s", title, exc)
    return None
```

**Option A: Add public method to KeywordDB (RECOMMENDED)**

Add `search_video_performance_by_title(title_prefix: str) -> str | None` to `database.py`. This is a 15-line addition that:
- Follows the existing public-method pattern (try/except, error dict)
- Returns `video_id` string or `None`
- Uses the same LIKE query already tested in integration tests

```python
def search_video_performance_by_title(self, title_prefix: str) -> str | None:
    """Look up video_id by title prefix using case-insensitive LIKE match."""
    try:
        self._ensure_performance_table()
        prefix = title_prefix[:40].replace("'", "''")
        cursor = self._conn.cursor()
        cursor.execute(
            "SELECT video_id FROM video_performance "
            "WHERE title LIKE ? COLLATE NOCASE LIMIT 1",
            (f"%{prefix}%",),
        )
        row = cursor.fetchone()
        return row[0] if row else None
    except Exception as exc:
        logger.warning("DB lookup error for '%s': %s", title_prefix, exc)
        return None
```

**Option B: Use `get_all_video_performance()` with Python filtering**

Loads all records (~47 rows for this channel), filters in Python:
```python
all_videos = db.get_all_video_performance(limit=500)
prefix = title[:40].lower()
for v in all_videos:
    if prefix in v.get('title', '').lower():
        return v['video_id']
return None
```
Simpler (no DB changes) but loads all records for every title lookup. With 47 videos and ~30 lookups per ingest run, this is ~1,410 in-memory row comparisons — acceptable but wasteful.

**Recommendation: Option A** — adds one clean public method, keeps the SQL lookup efficient, aligns with the codebase pattern. The existing integration test suite in `tests/integration/test_ctr_ingest.py` tests `_lookup_video_id` behavior and will need to be updated to verify the same behavior still works via the new path.

### SUMMARY Frontmatter Pattern

Existing SUMMARY files use YAML frontmatter. The `requirements_completed` key is used in other phases but was omitted from 60-02, 61-02, 61-03 at the time of writing. Pattern from a correctly-filled SUMMARY (e.g., 61-01-SUMMARY.md):

```yaml
---
phase: 61-data-driven-packaging-gate
plan: 01
requirements_completed: [GATE-01, GATE-02]
...
---
```

The audit maps which requirements each plan satisfies:
- **60-02:** RETITLE-04 (--check), RETITLE-05 (--revert), RETITLE-06 (SWAP LOG)
- **61-02:** GATE-03 (CTR ingestion from CROSS-VIDEO-SYNTHESIS.md)
- **61-03:** GATE-04 (greenlight/preflight use DB scores), GATE-05 (feedback loop documented)

Source: v6.0-MILESTONE-AUDIT.md requirements coverage table + phase SUMMARY accomplishment sections.

### REQUIREMENTS.md Traceability Fix

The current traceability table (lines 93-134) shows "Not started" for DATA-01 through GROW-05 (phases 55-59) and correctly shows "Complete" for RETITLE-01..06 and GATE-01..05 and DISC-01..05.

However: phases 55-59 (v5.2 Growth Engine) were marked as shipped in STATE.md on 2026-03-01. The REQUIREMENTS.md traceability was not updated to reflect this.

**Rows to update:** DATA-01..04 (Phase 55), CTR-01..04 + SEO-01..03 (Phase 56), GAP-01..04 (Phase 57), RET-01..04 (Phase 58), GROW-01..05 (Phase 59) — all "Not started" → "Complete".

**Note:** The audit specifically flags DISC-01..05 and RETITLE-01..06 as stale, but inspecting the current REQUIREMENTS.md shows RETITLE and GATE and DISC rows already show "Complete". The actual stale rows are phases 55-59. Verify exact current state before writing.

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead |
|---------|-------------|-------------|
| DB-enriched title scoring | Custom scoring bypass | `score_title(t, db_path=db.db_path)` — already implemented |
| Title-to-video_id lookup | New query infrastructure | Either new `search_video_performance_by_title()` or `get_all_video_performance()` |
| Frontmatter editing | Script/parser | Direct Read + Edit on YAML frontmatter in SUMMARY files |

---

## Common Pitfalls

### Pitfall 1: Closing db Before Use in retitle.md
**What goes wrong:** If you close `_db` before the scoring loop, `db_path` is a string path (str) not a connection — this is fine, `score_title()` just needs the path string. But if you close then try to use the object again, it silently reconnects. Close after the scored loop.
**How to avoid:** Follow the scorer.py pattern exactly — extract `.db_path` string, then close immediately.

### Pitfall 2: Breaking ctr_ingest Integration Tests
**What goes wrong:** `tests/integration/test_ctr_ingest.py` has 8 tests covering `_lookup_video_id` behavior. If you change the function to call a new public method, the tests still pass because they test behavior, not internals. But if you delete `_lookup_video_id` entirely and inline the call, the test file imports must be checked.
**How to avoid:** Keep `_lookup_video_id` as the private helper but have it delegate to `db.search_video_performance_by_title()`.

### Pitfall 3: SUMMARY Frontmatter Position
**What goes wrong:** Adding `requirements_completed` key outside the YAML delimiters (`---`) puts it in the markdown body, not parsed as frontmatter.
**How to avoid:** The `requirements_completed` key must be inside the opening `---` / `---` block, before the first `#` heading.

### Pitfall 4: REQUIREMENTS.md Traceability — Wrong Rows
**What goes wrong:** The audit mentions DISC and RETITLE as stale, but the actual REQUIREMENTS.md already has them as "Complete". The actually stale rows are phases 55-59 (DATA, CTR, SEO, GAP, RET, GROW).
**How to avoid:** Read the current REQUIREMENTS.md before editing — do not trust the audit's characterization of which specific rows are wrong without verifying.

---

## Code Examples

### retitle.md Step 4c — Before and After

**Before (current — static scores only):**
```python
# Source: .claude/commands/retitle.md Step 4c
from tools.title_scorer import score_title

all_options = list(dict.fromkeys(script_titles + manual_options))
scored = [(t, score_title(t)) for t in all_options]
```

**After (DB-enriched — INT-01 fix):**
```python
# Source: Pattern from tools/preflight/scorer.py (Phase 61-03)
from tools.title_scorer import score_title
from tools.discovery.database import KeywordDB

all_options = list(dict.fromkeys(script_titles + manual_options))
_db = KeywordDB()
scored = [(t, score_title(t, db_path=_db.db_path)) for t in all_options]
_db.close()
```

### ctr_ingest.py _lookup_video_id — Before and After

**Before (current — private access):**
```python
# Source: tools/ctr_ingest.py line 147
def _lookup_video_id(db, title: str) -> str | None:
    prefix = title[:40].replace("'", "''")
    try:
        cursor = db._conn.cursor()  # private attribute
        cursor.execute(
            "SELECT video_id FROM video_performance WHERE title LIKE ? COLLATE NOCASE LIMIT 1",
            (f"%{prefix}%",),
        )
        row = cursor.fetchone()
        if row:
            return row[0]
    except Exception as exc:
        logger.warning("DB lookup error for title '%s': %s", title, exc)
    return None
```

**After (using new public method — Option A):**
```python
def _lookup_video_id(db, title: str) -> str | None:
    return db.search_video_performance_by_title(title)
```

---

## State of the Art

| Old State | Current State | Change | Impact |
|-----------|---------------|--------|--------|
| `/retitle` uses static pattern scores | After INT-01 fix: uses DB-enriched scores when available | Phase 63 | Retitle candidates ranked by live CTR data, not hardcoded baselines |
| `ctr_ingest` uses `db._conn` directly | After fix: uses public KeywordDB method | Phase 63 | Less fragile to internal refactors of KeywordDB |
| SUMMARY frontmatter missing `requirements_completed` | After fix: frontmatter complete | Phase 63 | Traceability tools can auto-verify requirement coverage |

---

## Open Questions

1. **Does KeywordDB need a public `search_video_performance_by_title()` method, or is `get_all_video_performance()` + Python filtering acceptable?**
   - What we know: `get_all_video_performance()` loads all records; the channel has ~47 videos; performance is not a concern at this scale
   - What's unclear: Whether future phases will add more callers that need the SQL-level lookup
   - Recommendation: Add the public method (Option A) — it's 15 lines, follows the pattern, and is the right abstraction boundary

2. **Are phases 55-59 requirements actually "Complete" or were they stubs that never fully shipped?**
   - What we know: STATE.md says "v5.2 Growth Engine" shipped 2026-03-01 with phases 55-59 complete
   - What's unclear: The REQUIREMENTS.md notes "Not started" which may mean the requirements were aspirational descriptions that pre-date actual implementation
   - Recommendation: Read the 55-59 VERIFICATION.md files (if they exist) before updating traceability — only mark "Complete" if the verification passed

---

## Validation Architecture

`workflow.nyquist_validation` key is absent from `.planning/config.json` — treat as enabled.

### Test Framework

| Property | Value |
|----------|-------|
| Framework | pytest |
| Config file | `pyproject.toml` (testpaths = ["tests"]) |
| Quick run command | `pytest tests/integration/test_ctr_ingest.py -x` |
| Full suite command | `pytest` |

### Phase Requirements → Test Map

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| RETITLE-02 | `/retitle` scores candidates with DB-enriched scores when available | manual (slash command) | manual — no automated test for .md slash command | N/A |
| GATE-02 | `score_title(db_path=...)` returns `db_enriched: True` when DB has data | unit | `pytest tests/ -k "score_title or title_scorer" -x` | check |
| ctr_ingest fix | `_lookup_video_id` behavior unchanged after refactor | integration | `pytest tests/integration/test_ctr_ingest.py -x` | ✅ |

### Sampling Rate

- **Per task commit:** `pytest tests/integration/test_ctr_ingest.py -x`
- **Per wave merge:** `pytest`
- **Phase gate:** Full suite green before `/gsd:verify-work`

### Wave 0 Gaps

None — existing test infrastructure covers the ctr_ingest behavior. The INT-01 fix is in a `.md` slash command file (not Python) so no automated test is needed; manual verification is the gate.

---

## Sources

### Primary (HIGH confidence)
- `.planning/v6.0-MILESTONE-AUDIT.md` — definitive list of gaps and tech debt, audited 2026-03-15
- `tools/ctr_ingest.py` — actual code showing `db._conn.cursor()` at line 168
- `tools/title_scorer.py` — `score_title(title, db_path=None)` signature confirmed
- `.claude/commands/retitle.md` — Step 4c confirmed calling `score_title(t)` without db_path
- `tools/discovery/database.py` — KeywordDB public API confirmed: no `search_video_performance_by_title()` exists
- `.planning/phases/61-.../61-03-SUMMARY.md` — Pattern for DB-enriched scoring confirmed from prior work

### Secondary (MEDIUM confidence)
- `.planning/phases/60-.../60-02-SUMMARY.md` — Confirms what RETITLE-04, 05, 06 cover
- `.planning/phases/61-.../61-02-SUMMARY.md` — Confirms GATE-03 coverage

---

## Metadata

**Confidence breakdown:**
- INT-01 fix: HIGH — code location confirmed, exact fix pattern exists in scorer.py
- ctr_ingest private access fix: HIGH — line 168 confirmed, two viable options documented
- SUMMARY frontmatter: HIGH — keys and values confirmed from audit + phase content
- REQUIREMENTS.md update: MEDIUM — exact rows to update need verification (read file first)

**Research date:** 2026-03-15
**Valid until:** Indefinite — this is gap closure for already-shipped code, not a moving target
