# Phase 67: Title Scorer Recalibration - Context

**Gathered:** 2026-03-17
**Status:** Ready for planning

<domain>
## Phase Boundary

Recalibrate `tools/title_scorer.py` so "passing" is anchored to niche competitor norms (from Phase 66 `niche_benchmark.json`), not solely own-channel low-CTR history. Add niche percentile display, small-sample fallback to competitor benchmarks, and topic-type-specific CTR targets. Create `tools/benchmark_store.py` as the single interface for reading niche benchmark data.

</domain>

<decisions>
## Implementation Decisions

### Niche Percentile Display
- Claude's discretion on exact layout (inline vs separate section) — pick clearest format for existing output structure
- VPS-not-CTR caveat goes in help text and docs only, NOT in scoring output (keeps output clean)
- Niche percentile appears in BOTH `/greenlight` and direct title scorer output — wherever title scores appear
- Use relative labels ("below niche median", "top third", "bottom quartile") — no raw VPS numbers in default output

### Small-Sample Fallback Logic
- When <5 internal examples for a pattern: SUBSTITUTE niche benchmark score entirely (not blend, not warning-only)
- Always show fallback warning when substitution happens (not verbose-only): "Using niche benchmark (only N internal examples)"
- Claude's discretion on exact threshold per pattern (flat 5 or adjusted) as long as BENCH-02 success criterion is met
- Claude's discretion on VPS-to-score mapping formula — pick approach that preserves backward compatibility while incorporating niche data

### Topic-Type CTR Targets
- Grade thresholds ADJUST per topic type — same 0-100 score, but what constitutes "passing" shifts per topic
- Topic detection: auto-detect from title keywords by default, `--topic` flag overrides
- Show the gap in output: "Grade: C — political fact-check topics need B+ (score 75+)"
- Two-tier target system: niche benchmark median = floor (minimum expectation), REQUIREMENTS.md targets (3%/4%/5%) = aspirational "good" threshold
- Universal minimum lowered to 50 (from 65). Topic-specific threshold sets the real passing bar. Territorial may only need 50+, political needs 75+.

### Score Recalibration Math
- Keep 0-100 scale — recalibrate PATTERN_SCORES base values, don't change the scale itself
- Claude's discretion on colon hard-reject: analyze the discrepancy between own-channel -28% penalty and niche 0.78 median VPS, pick appropriate penalty level
- `benchmark_store.py` loads `niche_benchmark.json` from file each run (no caching). File is <10KB, negligible I/O
- `benchmark_store.py` must return graceful None when `niche_benchmark.json` is absent — existing workflows never blocked

### Claude's Discretion
- Exact niche percentile output format (inline vs block)
- VPS-to-score mapping formula for fallback substitution
- Colon penalty level (keep hard reject vs downgrade based on data analysis)
- Per-pattern fallback threshold tuning (as long as BENCH-02 met)
- Topic auto-detection keyword lists
- Grade threshold values per topic type (as long as two-tier floor/target system is implemented)

</decisions>

<specifics>
## Specific Ideas

- Success criterion 1 specifies exact format example: "Score: 71/100 — niche median is 5.2% CTR, you are in the bottom third" — adapt to use relative labels per discussion, but match this level of specificity
- The niche benchmark data uses VPS (views/subscriber ratio), not actual CTR. All display should treat this as a proxy signal, not ground truth
- Existing `PATTERN_SCORES` dict in title_scorer.py is the single place to update base scores — keep this pattern
- The `db_enriched` / `db_base_score` pattern in `score_title()` already shows how to layer external data — niche benchmark follows the same approach

</specifics>

<code_context>
## Existing Code Insights

### Reusable Assets
- `tools/title_scorer.py`: Core scorer with `detect_pattern()`, `score_title()`, `PATTERN_SCORES` dict. Already supports DB-enriched scoring via `db_path` parameter
- `tools/title_ctr_store.py`: `get_pattern_ctr_from_db()` — pattern for loading external CTR overrides into scorer
- `tools/youtube_analytics/benchmarks.py`: Verdict calculation, category benchmarks — pattern for confidence levels and tier logic
- `tools/preflight/scorer.py`: Consumes title scorer output for /greenlight — integration point for niche percentile display

### Established Patterns
- `PATTERN_SCORES` dict: Static base scores, overrideable by DB. Same pattern extends to niche benchmark override
- `db_enriched` / `db_base_score` return keys: Signals which data source was used. Extend with `niche_enriched` / `niche_base_score`
- Confidence levels: Already used in niche_benchmark.json (LOW/MEDIUM/HIGH) and benchmarks.py
- Hard reject pattern: `hard_rejects` list in `score_title()` — any HARD REJECT overrides grade to REJECTED

### Integration Points
- `score_title()` return dict → consumed by `tools/preflight/scorer.py` and `/greenlight` command
- `channel-data/niche_benchmark.json` → read by new `tools/benchmark_store.py`
- `--topic` flag → new parameter for `score_title()` and CLI interface
- Grade thresholds → currently hardcoded in `score_title()` (A=80, B=65, C=50, D=35)

</code_context>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 67-title-scorer-recalibration*
*Context gathered: 2026-03-17*
