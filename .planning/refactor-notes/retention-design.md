# RetentionInference — Design Sketch (Phase G2)

> **Planning only.** No code lands in this step. Source-of-truth for G3 (implement) and G4 (delete superseded modules). Companion to `retention-inventory.md` (G1) and pinned by `tests/test_retention_pipeline.py`.

The 7-file retention smear has three jobs entangled across modules:

1. **Fetch** raw retention curves (YouTube Analytics API).
2. **Map** drops and curves onto script structure (sections × words × timing).
3. **Decode/Score** what those drops *mean* (correlations, predictions, constraints).

`RetentionInference` collapses (2) and (3) behind a small object surface. (1) stays where it belongs — in a thin fetcher.

---

## Proposed surface

```python
class RetentionInference:
    """Single entry point for retention-derived insights about a script.

    Stateless except for the curve and sections it was constructed with.
    All four insight methods are pure functions of those two inputs plus
    optional config. No DB access from this class — callers inject the
    decoder/predictor data sources.
    """

    def __init__(
        self,
        curve: RetentionCurve,
        sections: list[ParsedSection],
        wpm: int = 150,
    ) -> None: ...

    # 1. Drops aligned to script sections (was: retention.find_drop_off_points
    #    + retention_mapper.map_retention_to_sections)
    def mapped_drops(self, threshold: float = 0.05) -> list[MappedSection]: ...

    # 2. Per-section retention-risk score (was: retention_scorer.score_section
    #    + score_all_sections)
    def section_scores(self, topic_type: str) -> list[RetentionScore]: ...

    # 3. Forward prediction without a real curve (was:
    #    retention_predictor.predict_retention)
    @classmethod
    def predict_from_sections(
        cls,
        sections: list[ParsedSection],
        topic_type: str,
    ) -> list[RetentionScore]: ...

    # 4. Channel-level decoded intent (was: retention_decoder.analyze
    #    + retention_by_topic.analyze_content_deltas_by_topic +
    #    retention_analysis.aggregate_results)
    @staticmethod
    def decode_channel(videos: list[VideoRecord]) -> DecodedIntent: ...
```

**Why 4 methods:** matches the four conceptual jobs after fetching — *align*, *score*, *predict*, *decode*. Adding a fifth would split one of these. Going below four would re-entangle predict and score (one is forward, one is backward; conflating breaks the pin).

**Why two are class/static:** `predict_from_sections` doesn't need a curve (we don't have one yet), and `decode_channel` operates on the cross-video corpus, not a single script. Keeping them on the same class keeps the import surface small without forcing instance construction.

---

## Function → method mapping

Every public function in the inventory must land somewhere. "Fetcher" = stays in `retention.py`. "Delete" = the function's responsibility folds into another caller and the function itself goes.

### `retention.py` (fetcher — stays)
| Existing function | Destination |
|-------------------|-------------|
| `get_retention_data()` | **fetcher** — only caller of YT Analytics API. Returns `RetentionCurve`. |
| `find_drop_off_points()` | **`RetentionInference.mapped_drops`** (absorbed; threshold becomes a method arg). |
| `_get_position_hint()` | **delete** — replaced by the `MappedSection.position_zone` field, computed once from `position`. |

### `retention_mapper.py`
| Existing function | Destination |
|-------------------|-------------|
| `map_retention_to_sections()` | **`RetentionInference.mapped_drops`** (absorbed). |
| `estimate_section_timestamps()` | **delete** — already implicit in `MappedSection.estimated_timestamp`; standalone callers (none in repo) inline it. |
| `format_mapped_drops_table()` | **move to a presenter** — `tools/youtube_analytics/_presenters.py`. Not part of the inference seam. |
| `_format_time()` | **move to presenter** (same file). |

### `retention_decoder.py`
| Existing function | Destination |
|-------------------|-------------|
| `RetentionDecoder.classify_hook_type()` | **`RetentionInference.decode_channel`** (private helper inside). |
| `RetentionDecoder.classify_duration_bucket()` | **`RetentionInference.decode_channel`** (private helper). |
| `RetentionDecoder.classify_specificity()` | **`RetentionInference.decode_channel`** (private helper). |
| `RetentionDecoder.analyze()` | **`RetentionInference.decode_channel`** (this IS the method). Returns `DecodedIntent`. |
| `RetentionDecoder._compute_correlations()` | **absorbed** into `decode_channel`. |
| `RetentionDecoder._generate_findings()` | **absorbed**. |
| `RetentionDecoder._generate_rule20()` | **move to presenter** — `_presenters.format_rule20(decoded: DecodedIntent)`. Pure formatting. |
| `RetentionDecoder.get_hook_retention_map()` | **delete** — caller uses `decoded.by_hook_type` directly. |
| `RetentionDecoder.get_rule20_text()` | **move to presenter** — same as `format_rule20`. |
| `RetentionDecoder._get_videos()` | **move** to a `VideoStore` repository (not part of inference). Loads from analytics.db. |

### `retention_analysis.py`
This module is two layers stacked: a cache/fetch layer and a content-correlation layer. They split.

| Existing function | Destination |
|-------------------|-------------|
| `_normalize`, `_slug_tokens`, `_should_skip_srt`, `find_all_srts`, `build_srt_mapping`, `_parse_srt_timestamp`, `parse_srt` | **move** to a `tools/transcripts/srt_index.py` (separate concern: SRT discovery). |
| `_cache_path`, `_load_cached`, `_save_cache`, `fetch_retention_cached` | **move** to `retention.py` as `cached_get_retention_data`. The fetcher is the only place that should know about caching. |
| `classify_content`, `classify_window` | **`RetentionInference.decode_channel`** (private helpers — content-type labels alongside hook-type). |
| `analyze_video`, `aggregate_results` | **absorbed** into `decode_channel`. |
| `_fmt_time`, `_delta_indicator` | **move to presenter**. |
| `generate_report`, `_generate_recommendations` | **move to presenter** — `_presenters.format_correlation_report(decoded)`. |
| `run_analysis` | **delete** — the orchestrator becomes a 5-line script in `tools/youtube_analytics/cli/correlate.py` calling the new seam. |
| `main` (CLI) | **rewrite** — minimal argparse over the new seam. |

### `retention_by_topic.py`
| Existing function | Destination |
|-------------------|-------------|
| `classify_topic` | **`RetentionInference.decode_channel`** (private helper). |
| `load_all_videos` | **move** to `VideoStore`. |
| `load_retention` | **move** — calls cached fetcher; lives in `retention.py`. |
| `analyze_retention_curve` | **absorbed** into `decode_channel`. |
| `compute_avg_curve` | **absorbed**. |
| `analyze_content_deltas_by_topic` | **absorbed** into `decode_channel` (returns per-topic deltas inside `DecodedIntent`). |
| `generate_report` | **move to presenter**. |
| `main` | **rewrite** — minimal CLI over new seam. |

### `retention_predictor.py`
| Existing function | Destination |
|-------------------|-------------|
| `_is_header`, `_extract_header`, `_is_metadata_block`, `_should_skip_line`, `_clean_inline_markdown` | **delete** — replaced by `tools.production.parser.ScriptParser`. The predictor's bespoke parser is duplication; the inventory's cross-cut #1 flagged this. |
| `parse_script_with_structure` | **delete** — replaced by `ScriptParser.parse_file` returning `Section` objects. The dict-shape divergence dies here. |
| `classify_section`, `summarize_section_types` | **`RetentionInference.predict_from_sections`** (private helpers). |
| `_get_position_zone`, `_estimate_read_minutes`, `_get_channel_avg_at` | **absorbed** into `predict_from_sections`. The hardcoded `_get_channel_avg_at` becomes a parameter sourced from `decode_channel`'s output (kills cross-cut #4 — single source of truth for channel avg). |
| `predict_from_file`, `predict_from_text` | **delete** — callers use `RetentionInference.predict_from_sections(ScriptParser().parse_file(path))`. Two-line glue. |
| `predict_retention` | **`RetentionInference.predict_from_sections`** (this IS the classmethod). |
| `_ascii_chart` | **move to presenter**. |
| `generate_report`, `_find_script_for_project` | **move to presenter** + a tiny CLI orchestrator. |
| `main` | **rewrite**. |

### `retention_scorer.py`
| Existing function | Destination |
|-------------------|-------------|
| `count_evidence_markers`, `measure_modern_relevance_gap`, `detect_voice_patterns` | **absorbed** into `RetentionInference.section_scores` as private helpers. (Or: extracted to `tools/production/section_features.py` if reused outside retention.) |
| `get_topic_baseline` | **inject** — `RetentionInference.__init__` takes a `baselines: TopicBaselines` mapping rather than reading KeywordDB at score time. Cross-cut #6 (no shared types) is partially fixed by this dep injection. |
| `score_section` | **`RetentionInference.section_scores`** (per-element). |
| `score_all_sections` | **`RetentionInference.section_scores`** (this IS the method). The `.text` vs `.content` quirk dies — we standardize on `ParsedSection.content`. |
| `format_retention_warnings` | **move to presenter**. |

---

## Data types

All four are immutable dataclasses (`frozen=True`). `Section` already exists in `tools.production.parser` — we standardize on it under the alias `ParsedSection`.

```python
from dataclasses import dataclass, field
from tools.production.parser import Section as ParsedSection  # alias for clarity

@dataclass(frozen=True)
class RetentionPoint:
    """One sample on the curve."""
    position: float          # 0.0–1.0 (elapsedVideoTimeRatio)
    retention: float         # 0.0–1.0+ (audienceWatchRatio)
    relative: float | None   # vs similar videos (relativeRetentionPerformance)


@dataclass(frozen=True)
class RetentionCurve:
    """Output of retention.py fetcher. The only YT-API-shaped object."""
    video_id: str
    points: tuple[RetentionPoint, ...]
    fetched_at: str          # ISO 8601
    summary: dict            # {avg_retention, min_retention, final_retention}


@dataclass(frozen=True)
class MappedSection:
    """A retention drop pinned to a script section."""
    section_heading: str
    section_type: str        # 'intro' | 'body' | 'conclusion'
    drop_position: float     # 0.0–1.0 in video
    drop_magnitude: float    # 0.0–1.0
    retention_before: float
    retention_after: float
    word_range: tuple[int, int]
    estimated_timestamp: str # 'M:SS-M:SS'
    section_content_preview: str
    position_in_section: float   # 0.0–1.0 within section
    position_zone: str       # was retention._get_position_hint


@dataclass(frozen=True)
class RetentionScore:
    """Predicted retention risk for one section."""
    section_heading: str
    score: float             # 0.0–1.0
    risk_level: str          # 'LOW' | 'MEDIUM' | 'HIGH'
    warnings: tuple[dict, ...]
    metrics: dict            # word_count, evidence_density, modern_gap, voice_patterns


@dataclass(frozen=True)
class DecodedIntent:
    """Channel-level structural patterns extracted from a video corpus."""
    video_count: int
    channel_avg_retention: float
    by_hook_type: dict[str, dict]
    by_duration: dict[str, dict]
    by_topic: dict[str, dict]
    by_specificity: dict[str, dict]
    correlations: tuple[dict, ...]
    top_findings: tuple[str, ...]
    rule20_constraints: tuple[str, ...]
```

**Notes:**
- `RetentionCurve` is the *only* shape that mirrors the YT Analytics API directly. Internally, `points` is a tuple of typed records, not a list of loose dicts.
- `MappedSection` and `RetentionScore` are flat — no nested dicts beyond `metrics`/`warnings` (kept open for now to avoid breaking the pinning test; G3 may tighten).
- `DecodedIntent` keeps `by_*` as `dict[str, dict]` because the bucket keys are dynamic (hook types vary). G3 may extract a `BucketStats` dataclass if useful.

---

## What stays in `retention.py`

After convergence, `retention.py` is ~80-120 lines:

```python
def get_retention_data(video_id: str, ...) -> RetentionCurve | dict:
    """ONLY caller of youtubeAnalytics.reports().query()."""

def cached_get_retention_data(video_id: str, force_refresh: bool = False) -> RetentionCurve | None:
    """Disk-cached wrapper, absorbing retention_analysis._cache_*."""

# That's it. No detection, no mapping, no scoring, no formatting.
# Even find_drop_off_points moves out — the curve is just sample points.
```

This is the only module that talks to the YouTube Analytics API or the disk cache. Everything else takes a `RetentionCurve` (or constructs one for testing) and runs locally.

---

## Deletion test

For each of the 7 modules: if we deleted the module today and forced callers to inline what they need, would complexity *concentrate* (good — fewer seams to maintain) or *just move* (bad — we'd be hiding entanglement)?

| Module | Verdict | Reasoning |
|--------|---------|-----------|
| `retention.py` | **Keep (slim)** | The API-call concern is real and well-isolated. Deletion would scatter API knowledge across the codebase. Concentrate further by absorbing `retention_analysis.fetch_retention_cached` here. |
| `retention_mapper.py` | **Delete** | All three public functions belong to `RetentionInference.mapped_drops` (or to a presenter module). No standalone callers in the repo besides `analyze.py` and `_post_publish_report.py`, both of which already import the inference layer once it exists. Concentrate. |
| `retention_decoder.py` | **Delete (class folds in)** | The class structure was vestigial — it had no state worth keeping (just `self.analytics_db`). Methods are pure. Folding into `RetentionInference.decode_channel` + a `VideoStore` for DB reads is a clean cut. Concentrate. |
| `retention_analysis.py` | **Split + delete** | Two unrelated concerns: SRT indexing (move to `tools/transcripts/srt_index.py`) and content correlation (folds into `decode_channel`). Cache layer moves into `retention.py`. The orchestrator becomes a CLI wrapper. After the split, the file is empty; delete. Concentrate, with one move. |
| `retention_by_topic.py` | **Delete** | Pure overlap with decoder once topic bucketing is just a `decoded.by_topic` field on `DecodedIntent`. Reports become presenter calls. Concentrate. |
| `retention_predictor.py` | **Delete (mostly)** | The bespoke parser is duplicated work — `ScriptParser` is the source of truth. The hardcoded channel-avg baseline is a real bug surfaced by the inventory (cross-cut #4); it must come from `DecodedIntent.channel_avg_retention`. After absorbing `predict_retention` and dropping the parser, the module is two helper functions deep. Concentrate. |
| `retention_scorer.py` | **Delete** | All five public functions are private helpers under `section_scores` once we standardize on `ParsedSection.content`. The `.text` vs `.content` mismatch (cross-cut #1) dies in the move. Topic baselines move from runtime KeywordDB lookup to constructor injection. Concentrate. |

**Net file count:** 7 retention-prefixed modules → 1 (`retention.py`) + 1 (`retention_inference.py`) + 1 presenter + 1 CLI orchestrator + 1 SRT index extracted to `tools/transcripts/`.

---

## Open questions for G3

These are recorded here, not blockers — G3 implementation will resolve them. None require changing G1's pinning test.

1. **`VideoStore` placement.** Should the corpus loader live in `tools/youtube_analytics/video_store.py` or in `tools/discovery/database.py` next to `KeywordDB`? Lean toward analytics — different DB, different concerns.
2. **SRT index location.** `tools/transcripts/srt_index.py` is the proposed home, but `tools/transcripts/` doesn't exist yet. Either create it or park the SRT helpers in `tools/youtube_analytics/_srt_index.py` (private to analytics).
3. **Curve caching format.** Existing JSON cache stays — no need to rewrite during convergence. Just move it.
4. **Presenter module name.** `_presenters.py` (private) vs `presenters.py` (public). Lean private; the seam is `RetentionInference`, not the formatters.
5. **`MappedSection.metrics` / `warnings` typing.** Tuples of dicts now; could be tuples of dataclasses post-G3 once we know the shape settles. Defer until the pinning test stops needing dict-key flexibility.

---

## What G3 must NOT do

- Change `find_drop_off_points`'s current numeric behavior (the pinning test asserts shape, but the deletion replaces the function — keep the threshold-comparison logic identical when porting).
- Reach into the YouTube Analytics API from anywhere except `retention.py`.
- Re-introduce the `.text`/`.content` parser-shape divergence.
- Hardcode channel averages (the predictor's `_get_channel_avg_at` is the bug to kill — channel avg flows from `DecodedIntent`).
- Modify `tests/test_retention_pipeline.py` until G4 (deletion) is complete; that test remains the pinning net throughout the convergence.
