# Phase 67: Title Scorer Recalibration - Research

**Researched:** 2026-03-17
**Domain:** Python scoring tool modification — `tools/title_scorer.py`, new `tools/benchmark_store.py`
**Confidence:** HIGH

---

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

**Niche Percentile Display**
- VPS-not-CTR caveat goes in help text and docs only, NOT in scoring output
- Niche percentile appears in BOTH `/greenlight` and direct title scorer output
- Use relative labels ("below niche median", "top third", "bottom quartile") — no raw VPS numbers in default output

**Small-Sample Fallback Logic**
- When <5 internal examples for a pattern: SUBSTITUTE niche benchmark score entirely (not blend, not warning-only)
- Always show fallback warning when substitution happens: "Using niche benchmark (only N internal examples)"

**Topic-Type CTR Targets**
- Grade thresholds ADJUST per topic type — same 0-100 score, but what constitutes "passing" shifts per topic
- Topic detection: auto-detect from title keywords by default, `--topic` flag overrides
- Show the gap in output: "Grade: C — political fact-check topics need B+ (score 75+)"
- Two-tier target system: niche benchmark median = floor, REQUIREMENTS.md targets (3%/4%/5%) = aspirational "good"
- Universal minimum lowered to 50 (from 65). Territorial may only need 50+, political needs 75+

**Score Recalibration Math**
- Keep 0-100 scale — recalibrate PATTERN_SCORES base values, don't change scale
- `benchmark_store.py` loads `niche_benchmark.json` from file each run (no caching)
- `benchmark_store.py` must return graceful None when `niche_benchmark.json` is absent

### Claude's Discretion
- Exact niche percentile output format (inline vs block)
- VPS-to-score mapping formula for fallback substitution
- Colon penalty level (keep hard reject vs downgrade based on data analysis)
- Per-pattern fallback threshold tuning (as long as BENCH-02 met)
- Topic auto-detection keyword lists
- Grade threshold values per topic type (as long as two-tier floor/target system is implemented)

### Deferred Ideas (OUT OF SCOPE)
None — discussion stayed within phase scope
</user_constraints>

---

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| BENCH-01 | Title scorer anchors "passing" (65/100) to 4%+ CTR based on edu/history competitor norms, not own-channel baseline | niche_benchmark.json provides competitor VPS medians by pattern; VPS-to-score mapping formula translates these into 0-100 scale recalibration |
| BENCH-02 | Scorer flags when a pattern score is based on fewer than 5 examples and falls back to competitor benchmarks | title_ctr_store.py already uses min_sample=3; phase raises threshold to 5 and switches from "exclude" to "substitute niche benchmark" behavior |
| BENCH-03 | Scorer applies different CTR targets by topic type (territorial 3%+, political fact-check 5%+, ideological 4%+) | niche_benchmark.json has by_topic_type section with median VPS per type; classify_topic_type() in performance.py detects topic from title keywords |
</phase_requirements>

---

## Summary

Phase 67 modifies `tools/title_scorer.py` and adds `tools/benchmark_store.py` to break the self-referential calibration loop where "passing" was judged against the channel's own low-CTR history. The channel's 33-video CTR sample has a measured average of roughly 3.2–3.8% across patterns — which is actually below what edu/history niche competitors achieve. Phase 66 produced `channel-data/niche_benchmark.json` with 239 competitor videos (VPS data by pattern and topic type). This phase wires that data into the scorer.

The two key behavioral changes are: (1) `benchmark_store.py` becomes the single interface for reading niche data, with a graceful None fallback if the file is absent; (2) `score_title()` gains a `topic_type` parameter, and grade thresholds shift per topic so territorial titles need a score of 50+ while political fact-check titles need 75+. The small-sample fallback is the most behavior-changing element: patterns with fewer than 5 internal examples no longer silently use a weak average — they substitute the niche benchmark score and display a warning.

**Primary recommendation:** Follow the `db_enriched`/`db_base_score` layering pattern already in `score_title()` — add a parallel `niche_enriched`/`niche_base_score` layer consumed by the same return dict, then extend `format_result()` to append the niche percentile line beneath the score.

---

## Standard Stack

### Core (no new dependencies)
| File | Role | Notes |
|------|------|-------|
| `tools/title_scorer.py` | Main scorer — modify in place | `PATTERN_SCORES`, `score_title()`, `format_result()`, `detect_pattern()` all touched |
| `tools/benchmark_store.py` | NEW — thin loader for niche_benchmark.json | Pure stdlib (json, pathlib). No DB. |
| `tools/title_ctr_store.py` | Existing DB-backed CTR loader | Pattern for how benchmark_store should be structured |
| `tools/preflight/scorer.py` | Consumes `score_title()` output — must propagate niche fields | `_score_title_metadata()` at line 373 calls `score_title()` and reads its return dict |
| `channel-data/niche_benchmark.json` | Phase 66 deliverable — source of truth for niche data | 239 videos, 5 channels, by_pattern + by_topic_type sections |

### No new packages required
The entire phase uses stdlib only (`json`, `pathlib`, `re`). No pip installs.

---

## Architecture Patterns

### Recommended Project Structure
```
tools/
├── title_scorer.py          # Modified: new niche_enriched return keys, topic_type param
├── benchmark_store.py       # NEW: loads niche_benchmark.json, returns None gracefully
├── title_ctr_store.py       # Unchanged (pattern reference only)
└── preflight/
    └── scorer.py            # Modified: propagate niche_percentile to title gate output
channel-data/
└── niche_benchmark.json     # Phase 66 deliverable — read by benchmark_store.py
```

### Pattern 1: Layered Scoring (existing — extend it)
**What:** `score_title()` already layers DB overrides on top of static PATTERN_SCORES. The `db_enriched` / `db_base_score` keys in the return dict signal which source was used. Niche benchmark follows identical layering.

**When to use:** Whenever an external data source can override a static default.

**Existing implementation reference (title_scorer.py lines 136–147):**
```python
db_overrides = {}
if db_path is not None:
    try:
        from tools.title_ctr_store import get_pattern_ctr_from_db
        db_overrides = get_pattern_ctr_from_db(db_path)
    except Exception:
        pass  # Silent fallback — never crash due to DB issues

db_base_score = db_overrides.get(pattern)  # None if not in DB
db_enriched = db_base_score is not None
base = db_base_score if db_enriched else PATTERN_SCORES.get(pattern, 50)
```

**Niche layer addition (same pattern):**
```python
niche_data = benchmark_store.load()  # returns None if file absent
niche_base_score = None
niche_enriched = False
if niche_data and pattern in niche_data.get('by_pattern', {}):
    pat = niche_data['by_pattern'][pattern]
    if pat.get('sample_count', 0) >= 1:
        niche_base_score = _vps_to_score(pat['median_vps'])
        niche_enriched = True
```

### Pattern 2: benchmark_store.py — thin file loader
**What:** Reads `channel-data/niche_benchmark.json` relative to project root. Returns full dict or None. No caching (file is <10KB, negligible I/O per CONTEXT.md decision).

**Graceful None contract:** Every caller must handle `None` return without crashing. benchmark_store.py itself never raises — it only returns None on any failure.

```python
# tools/benchmark_store.py
import json
from pathlib import Path
from typing import Optional, Dict, Any

_BENCHMARK_PATH = Path(__file__).resolve().parent.parent / 'channel-data' / 'niche_benchmark.json'

def load(path: Optional[Path] = None) -> Optional[Dict[str, Any]]:
    """Load niche_benchmark.json. Returns None if absent or unreadable."""
    target = path or _BENCHMARK_PATH
    try:
        return json.loads(target.read_text(encoding='utf-8'))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None
```

### Pattern 3: Topic-type grade thresholds
**What:** Grade cutoffs currently hardcoded in `score_title()` (A=80, B=65, C=50, D=35). Phase adds a topic-type dispatch table that replaces or augments those cutoffs based on REQUIREMENTS.md targets (territorial 3%+, political 5%+, ideological 4%+).

**Two-tier system:** floor = niche median (minimum expectation), aspirational = REQUIREMENTS.md CTR target.

```python
# Grade passing threshold by topic type
TOPIC_GRADE_THRESHOLDS = {
    'territorial':         {'pass': 50, 'good': 65},   # 3%+ CTR target
    'ideological':         {'pass': 60, 'good': 70},   # 4%+ CTR target
    'political_fact_check': {'pass': 75, 'good': 85},  # 5%+ CTR target
    'general':             {'pass': 60, 'good': 70},   # default
}
```

### Pattern 4: Niche percentile — relative label computation
**What:** Given a title's score, compute its position relative to the niche distribution for that pattern and emit a relative label ("top third", "above niche median", "bottom quartile").

**Data available in niche_benchmark.json:** `min_vps`, `max_vps`, `median_vps` per pattern. No full distribution, only these three points. Compute percentile estimate by linear interpolation between min and max, with median as the 50th-percentile anchor.

```python
def _niche_percentile_label(score: int, pattern: str, niche_data: dict) -> str:
    """Estimate rough percentile against niche using min/median/max VPS."""
    pat = niche_data.get('by_pattern', {}).get(pattern)
    if not pat:
        return ''
    niche_score = _vps_to_score(pat['median_vps'])
    if score >= niche_score * 1.3:
        return 'top third of niche'
    elif score >= niche_score:
        return 'above niche median'
    elif score >= niche_score * 0.7:
        return 'below niche median'
    else:
        return 'bottom quartile of niche'
```

### Anti-Patterns to Avoid
- **Blending own-channel score with niche score:** CONTEXT.md is explicit — substitute, don't blend. When <5 internal examples, the niche score IS the base score.
- **Showing raw VPS numbers in default output:** VPS is not CTR. The caveat belongs in `--help` only.
- **Raising a FileNotFoundError from benchmark_store.py:** Any exception must be swallowed and return None. Existing workflows must not block.
- **Adding niche data to the hard-reject logic:** Hard rejects (year, colon, the_x_that) are own-channel pattern — don't override them with niche data.

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Topic type detection | New keyword classifier | `classify_topic_type()` from `tools/youtube_analytics/performance.py` | Already handles territorial/ideological/colonial/legal/medieval/politician/general; extend keyword lists if needed |
| Percentile stats | Full statistical distribution | Linear interpolation on min/median/max from niche_benchmark.json | Only 3 data points available per pattern — complex stats would be false precision |
| JSON caching | In-memory LRU cache | No cache needed — file is <10KB per CONTEXT.md decision | Simpler code, no stale-data risk |
| Score-to-CTR conversion | New formula | Extend `title_ctr_store.py`'s existing `score = min(100, max(0, int(ctr_percent * 17)))` formula | Already calibrated so 3.8% CTR → 64, matching static declarative baseline |

---

## Common Pitfalls

### Pitfall 1: topic_type name mismatch between systems
**What goes wrong:** `classify_topic_type()` returns `'territorial'`, `'ideological'`, `'colonial'`, `'politician'`, `'medieval'`, `'legal'`, `'general'`. `niche_benchmark.json` by_topic_type has `'territorial'`, `'ideological'`, `'political_fact_check'`. These don't map 1:1.
**Why it happens:** Phase 66 used different taxonomy than the existing performance.py classifier.
**How to avoid:** Map `'politician'` → `'political_fact_check'`, `'colonial'` + `'legal'` → `'territorial'` or `'general'` in benchmark_store lookup. Define a `_normalize_topic_type(t)` mapping function.
**Warning signs:** KeyError on `niche_data['by_topic_type'][topic_type]` — means the topic type string wasn't normalized.

### Pitfall 2: sample_count for 'versus' pattern is 1 in niche data
**What goes wrong:** niche_benchmark.json shows `versus` has `sample_count: 1` and `confidence: "LOW"`. If the niche benchmark substitution is applied uncritically for low-confidence niche data, it may actually be LESS reliable than the own-channel score of n=2.
**Why it happens:** Only one versus-pattern video in the competitor set.
**How to avoid:** Add a confidence guard: only substitute niche benchmark when niche `sample_count >= 3` AND `confidence != "LOW"`. Otherwise keep static PATTERN_SCORES for that pattern.
**Warning signs:** `versus` titles getting artificially depressed scores (niche median_vps=2.812 maps to a high score, actually good here, but the point is to guard the logic).

### Pitfall 3: Colon pattern inconsistency — own-channel vs niche
**What goes wrong:** Own-channel data shows colon at 2.3% CTR (HARD REJECT penalty). Niche data shows colon with `median_vps: 0.776` (higher than declarative at 0.565). If niche data overrides own-channel hard-reject, the tool becomes permissive about colons.
**Why it happens:** Competitor channels (Knowing Better, Kraut) use pipe `|` which is coded as "colon" by `detect_pattern()` — but pipe is stylistically different from colon. Niche colon data is inflated by pipe-style titles.
**How to avoid:** Keep colon as HARD REJECT based on own-channel data. Niche data for 'colon' should NOT override the penalty — the niche samples include pipe syntax. Document this in benchmark_store.py and title_scorer.py comments.
**Warning signs:** Colon-pattern titles passing with B grade instead of REJECTED.

### Pitfall 4: preflight/scorer.py score_title() result dict changes breaking the gate
**What goes wrong:** `_score_title_metadata()` in preflight/scorer.py reads specific keys from `score_title()` return dict (`score`, `pattern`, `hard_rejects`, `suggestions`). Adding new keys is safe; renaming existing keys breaks it.
**Why it happens:** The integration point is implicit — no formal interface contract.
**How to avoid:** Only ADD new keys (`niche_enriched`, `niche_base_score`, `niche_percentile`, `topic_type_target`) to the return dict. Never rename existing keys.
**Warning signs:** preflight scorer returning 50 neutral score (its exception fallback) after title_scorer changes.

### Pitfall 5: `--topic` CLI flag collides with existing argparse setup
**What goes wrong:** `title_scorer.py` CLI uses `argparse`. Adding `--topic` must not conflict with existing `--db`, `--file`, `--ingest` flags.
**Why it happens:** Argparse namespace collision if flag name is reused.
**How to avoid:** Add `--topic` as a standalone optional arg with `choices=['territorial', 'ideological', 'political_fact_check', 'general']` plus a sentinel for auto-detect (None default). Also pass `topic_type` through to `score_title()` parameter.

---

## Code Examples

Verified patterns from existing codebase:

### VPS-to-score mapping (extend title_ctr_store.py formula)
```python
# Source: tools/title_ctr_store.py line 9-11
# Existing: score = min(100, max(0, int(ctr_percent * 17)))
# Maps 3.8% CTR -> 64 (matching static declarative of 65)
#
# For VPS, we need a different multiplier since VPS != CTR.
# niche declarative median_vps = 0.565, target score ~65
# => multiplier = 65 / 0.565 = ~115
# But VPS is unbounded (outliers reach 26.0), so cap at 100.
def _vps_to_score(vps: float) -> int:
    """Convert views-per-subscriber ratio to 0-100 score.
    Calibrated so niche declarative median (0.565 VPS) -> 65 score."""
    return min(100, max(0, int(vps * 115)))
```

### Small-sample fallback substitution (new logic in score_title)
```python
# Source: extends pattern from tools/title_ctr_store.py get_pattern_ctr_from_db()
# When own-channel has <5 examples, substitute niche benchmark entirely

def _get_pattern_sample_count(db_path: str, pattern: str) -> int:
    """Return number of own-channel videos matching this pattern (from DB)."""
    # Query ctr_snapshots JOIN video_performance, group by pattern
    # Returns 0 if DB unavailable
    ...

# In score_title():
own_sample_count = _get_pattern_sample_count(db_path, pattern) if db_path else 0
MIN_INTERNAL_SAMPLE = 5

if own_sample_count < MIN_INTERNAL_SAMPLE and niche_base_score is not None:
    base = niche_base_score
    fallback_warning = f"Using niche benchmark (only {own_sample_count} internal examples)"
else:
    base = db_base_score if db_enriched else PATTERN_SCORES.get(pattern, 50)
    fallback_warning = None
```

### Topic-specific grade output in format_result
```python
# Extend format_result() to show topic context after grade line
topic_target = result.get('topic_type_target', {})
if topic_target.get('gap_message'):
    lines.append(f"  Topic:   {result.get('detected_topic', 'general')} — {topic_target['gap_message']}")
# Example output:
#   Topic:   political_fact_check — needs score 75+ to pass (currently 62)
```

### Niche percentile inline in format_result
```python
# Add niche context line after Score line
niche_label = result.get('niche_percentile_label', '')
if niche_label:
    niche_median_ctr = result.get('niche_median_ctr_display', '')
    lines[score_line_index] += f" — niche median ~{niche_median_ctr}, you are {niche_label}"
# Example output:
#   Score:   71/100 (B) — niche median ~3.2% CTR proxy, you are above niche median
```

---

## Niche Benchmark Data (from Phase 66)

### Pattern-level data
| Pattern | Niche Median VPS | Sample Count | Confidence | Implied Score |
|---------|-----------------|--------------|------------|--------------|
| versus | 2.812 | 1 | LOW | ~100 (unreliable — guard against substitution) |
| declarative | 0.565 | 104 | HIGH | ~65 |
| how_why | 0.226 | 61 | HIGH | ~26 |
| question | 0.268 | 8 | MEDIUM | ~31 |
| colon | 0.776 | 65 | HIGH | ~89 (BUT: do not use — pipe inflation, own-channel data is authoritative) |

Key observation: `how_why` has a lower niche VPS median (0.226) than own-channel CTR suggests (3.3% → score 55). The niche VPS data includes Kraut/Toldinstone which have different conversion dynamics. This means niche VPS is not a straightforward CTR proxy — use it to show context, not to override own-channel for well-sampled patterns.

### Topic-type data
| Topic Type | Niche Median VPS | Sample Count | REQUIREMENTS.md CTR Target |
|------------|-----------------|--------------|----------------------------|
| territorial | 0.373 | 191 | 3%+ |
| ideological | 1.362 | 24 | 4%+ |
| political_fact_check | 0.557 | 24 | 5%+ |

Observation: ideological topics have the highest niche median VPS (1.362) — these topics punch above their weight on subscriber conversion (confirmed by CLAUDE.md: 2.31% sub rate for ideological vs 0.65% for territorial). REQUIREMENTS.md sets 5%+ for political fact-check but the niche median VPS for that type is only 0.557 — the 5% target is aspirational, not a niche norm.

---

## State of the Art

| Old Behavior | New Behavior | Impact |
|--------------|-------------|--------|
| "passing" = B grade (65+) based on own-channel low CTR | "passing" floor = 50 universal, real bar set per topic type | Political fact-check titles need 75+ to be considered viable |
| Pattern with n=2 own data silently uses weak average | n<5 own data triggers niche substitution + visible warning | "versus" pattern properly flagged as small-sample |
| No competitor context in output | Niche percentile label shown on score line | User sees "you are below niche median" without needing to know VPS math |
| grade thresholds identical for all topic types | Separate pass/good thresholds per topic type | Same raw title scored at C for territorial but F for political |

---

## Open Questions

1. **How to handle own-channel sample count lookup without DB**
   - What we know: `title_ctr_store.py` needs the DB to count samples. When no DB is present (`--db` flag not passed), own_sample_count defaults to 0, which would trigger niche substitution for every pattern.
   - What's unclear: Should niche substitution only activate when `--db` is passed (i.e., user opted into DB-enriched mode)? Or should it always activate when niche data is available?
   - Recommendation: Activate niche substitution only when `db_path` is provided AND own sample count < 5. When `db_path` is None (static mode), use PATTERN_SCORES as-is and append niche percentile context only (no score substitution). This preserves backward-compatible static mode.

2. **`topic_type` auto-detection vs `--topic` flag scope**
   - What we know: `classify_topic_type()` returns 8 types; niche_benchmark.json has 3. Many channel topics classify as 'colonial', 'medieval', etc. which have no direct niche benchmark entry.
   - What's unclear: Do colonial/medieval/legal map to 'territorial' for threshold purposes?
   - Recommendation: `_normalize_topic_type()` maps colonial/legal → territorial, medieval → general, politician → political_fact_check. Document the mapping table in benchmark_store.py.

---

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | pytest (detected in project) |
| Config file | pyproject.toml or pytest.ini (check existing) |
| Quick run command | `pytest tools/tests/test_title_scorer.py -x -q` |
| Full suite command | `pytest tools/tests/ -q` |

### Phase Requirements → Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| BENCH-01 | niche percentile label appears in score output | unit | `pytest tools/tests/test_title_scorer.py::test_niche_percentile_label -x` | Wave 0 |
| BENCH-01 | benchmark_store.load() returns None when file absent | unit | `pytest tools/tests/test_benchmark_store.py::test_graceful_none -x` | Wave 0 |
| BENCH-02 | small-sample substitution triggers warning message | unit | `pytest tools/tests/test_title_scorer.py::test_small_sample_fallback -x` | Wave 0 |
| BENCH-02 | no substitution when own sample >= 5 | unit | `pytest tools/tests/test_title_scorer.py::test_no_fallback_sufficient_sample -x` | Wave 0 |
| BENCH-03 | territorial title gets pass threshold 50 | unit | `pytest tools/tests/test_title_scorer.py::test_topic_grade_territorial -x` | Wave 0 |
| BENCH-03 | political_fact_check title gets pass threshold 75 | unit | `pytest tools/tests/test_title_scorer.py::test_topic_grade_political -x` | Wave 0 |
| BENCH-03 | same raw title scores differently per topic type | unit | `pytest tools/tests/test_title_scorer.py::test_same_title_different_topics -x` | Wave 0 |

### Sampling Rate
- **Per task commit:** `pytest tools/tests/test_title_scorer.py -q`
- **Per wave merge:** `pytest tools/tests/ -q`
- **Phase gate:** Full suite green before `/gsd:verify-work`

### Wave 0 Gaps
- [ ] `tools/tests/test_title_scorer.py` — covers BENCH-01, BENCH-02, BENCH-03
- [ ] `tools/tests/test_benchmark_store.py` — covers BENCH-01 graceful None
- [ ] Verify pytest config exists: `pyproject.toml` or `pytest.ini`

---

## Sources

### Primary (HIGH confidence)
- `tools/title_scorer.py` (lines 1–369) — full current implementation, `PATTERN_SCORES`, `score_title()`, `format_result()`, `detect_pattern()`
- `tools/title_ctr_store.py` — min_sample pattern, VPS-to-score formula reference (`ctr * 17`)
- `channel-data/niche_benchmark.json` — Phase 66 deliverable, 239-video competitor dataset
- `tools/preflight/scorer.py` (lines 373–590) — `_score_title_metadata()` integration point
- `tools/youtube_analytics/performance.py` (lines 161–190) — `classify_topic_type()` keyword classifier
- `.planning/phases/67-title-scorer-recalibration/67-CONTEXT.md` — locked decisions

### Secondary (MEDIUM confidence)
- `tools/youtube_analytics/benchmarks.py` — confidence level patterns (LOW/MEDIUM/HIGH) and verdict structure
- `.planning/REQUIREMENTS.md` — CTR targets (territorial 3%+, ideological 4%+, political fact-check 5%+)

---

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — all files read directly, no guesses
- Architecture: HIGH — extending well-understood layering pattern already in place
- Pitfalls: HIGH — colon/pipe inconsistency and topic taxonomy mismatch verified directly from niche_benchmark.json content
- Niche data: HIGH for declarative/how_why/colon (n=61-104), MEDIUM for question (n=8), LOW for versus (n=1)

**Research date:** 2026-03-17
**Valid until:** 2026-06-17 (matches niche_benchmark.json refresh_after date)
