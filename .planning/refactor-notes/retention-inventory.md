# Retention Pipeline Inventory (Phase G1)

> Snapshot of the public surface of the 7 `tools/youtube_analytics/retention*.py` modules **as of 2026-05-04**, before the planned `RetentionInference` convergence (G2-G4). The pinning test in `tests/test_retention_pipeline.py` enforces this surface during refactor.
>
> This file documents shape only — no design proposals. Edit-compose decisions belong to G2.

---

## Module 1: `retention.py`

**Purpose:** Fetch raw audience-retention curves from the YouTube Analytics API and detect drop-offs. Single video at a time.

**Dependencies:** `tools.youtube_analytics.auth.get_authenticated_service`, `googleapiclient.errors.HttpError`.

| Function | Consumes | Produces |
|----------|----------|----------|
| `get_retention_data(video_id, start_date=None, end_date=None)` | YouTube video ID, optional date range | Dict with `video_id`, `data_points` (list of `{position, retention, relative}`), `drop_off_points`, `summary` (`avg_retention`, `min_retention`, `final_retention`), `date_range`, `fetched_at`. On error: `{error, video_id, details?}`. |
| `find_drop_off_points(data_points, threshold=0.05)` | Data-points list | List of `{position, retention_before, retention_after, drop, timestamp_hint}`. Pure function. |
| `_get_position_hint(position)` _(private)_ | Float 0.0-1.0 | Bucket label: `intro`, `early`, `first half`, `second half`, `toward end`, `conclusion`. |

**CLI entry:** `python -m tools.youtube_analytics.retention <video_id> [--threshold FLOAT] [-v|-q]`. Prints JSON.

**Side effects:** Calls YouTube Analytics API (auth required). No DB writes.

---

## Module 2: `retention_mapper.py`

**Purpose:** Map percentage-based retention drops onto specific script sections using word-count-based timing estimates.

**Dependencies:** `tools.production.parser.{Section, ScriptParser}` (with a fallback `Section` dataclass for test envs).

| Function | Consumes | Produces |
|----------|----------|----------|
| `map_retention_to_sections(drop_off_points, sections, wpm=150)` | Drops list (from `retention.py`) + Section objects + WPM | List of `{section_heading, section_type, drop_position, drop_magnitude, retention_before, retention_after, word_range, estimated_timestamp, section_content_preview, position_in_section}`. Returns `[]` on bad input. |
| `estimate_section_timestamps(sections, wpm=150)` | Section objects + WPM | List of `{heading, start_time_str, end_time_str, duration_seconds, word_count}`. |
| `format_mapped_drops_table(mapped_drops)` | Mapped drops list | Markdown table string sorted by magnitude (HIGH/MEDIUM/LOW severity). |
| `_format_time(seconds)` _(private)_ | Float seconds | `M:SS` string. |

**Side effects:** None. Pure transformation.

---

## Module 3: `retention_decoder.py`

**Purpose:** Correlate channel-wide script structure with retention to generate `script-writer-v2` Rule 20 constraints. Operates on aggregate data.

**Dependencies:** `tools/youtube_analytics/analytics.db` (videos table with `avg_view_percentage`, `duration_seconds`, etc.).

### Class: `RetentionDecoder`

| Method | Consumes | Produces |
|--------|----------|----------|
| `__init__(self)` | — | Sets `self.analytics_db = ANALYTICS_DB`. |
| `_get_videos(self)` _(private)_ | analytics.db | List of video dicts (filtered: `avg_view_percentage > 0 AND duration_seconds > 120`). |
| `classify_hook_type(self, title)` | Title string | `myth-bust`, `document-reveal`, `how-why`, `question`, `curiosity-gap`, or `statement`. |
| `classify_duration_bucket(self, seconds)` | Int seconds | `short (<7m)`, `medium (7-11m)`, `long (11-16m)`, `very-long (16m+)`. |
| `classify_specificity(self, title)` | Title string | `specific` or `general` (regex on dates/document terms). |
| `analyze(self)` | analytics.db | Dict with `video_count`, `channel_avg_retention`, `by_hook_type`, `by_duration`, `by_topic`, `by_specificity`, `correlations`, `top_findings`, `rule20_constraints`. Error dict if <5 videos. |
| `_compute_correlations(self, videos, avg_ret)` _(private)_ | Videos + avg | List of `{factor, finding, effect_size, direction}` for duration/views/conversion. |
| `_generate_findings(...)` _(private)_ | Aggregates | List of human-readable finding strings (gated by `MIN_BUCKET_SIZE = 3`). |
| `_generate_rule20(...)` _(private)_ | Aggregates | List of constraint strings for Rule 20. |
| `get_hook_retention_map(self)` | analytics.db | `by_hook_type` dict from `analyze()`. |
| `get_rule20_text(self)` | analytics.db | Markdown block ready for `script-writer-v2`. |

**Module constants:** `ANALYTICS_DB`, `MIN_BUCKET_SIZE = 3`.

**CLI entry:** `python -m tools.youtube_analytics.retention_decoder [--findings|--rule20|--json] [-v|-q]`.

**Side effects:** Reads `analytics.db`. No writes.

---

## Module 4: `retention_analysis.py`

**Purpose:** Cross-video correlation between SRT subtitle content and retention curves, written to `channel-data/patterns/RETENTION-SCRIPT-CORRELATION.md`. Cached fetch layer.

**Dependencies:** `analytics.db`, SRT files in `transcripts/` and `video-projects/_IN_PRODUCTION/`, retention cache dir, network for non-cached fetches.

| Function | Consumes | Produces |
|----------|----------|----------|
| `_normalize(text)` | Text | Lowercase, punctuation-stripped, collapsed whitespace. |
| `_slug_tokens(slug)` | SRT filename slug | Set of >2-char tokens. |
| `_should_skip_srt(path)` | Path | Bool — skips non-English / backups. |
| `find_all_srts()` | — | List of candidate SRT paths. |
| `build_srt_mapping()` | — | `{video_id: Path}` via fuzzy matching. |
| `_parse_srt_timestamp(ts)` | `HH:MM:SS,mmm` string | Float seconds. |
| `parse_srt(path)` | SRT path | List of `{start, end, text}` segments. |
| `classify_content(text)` | Segment text | Content label (e.g., `evidence`, `narrative`, `analysis`). |
| `classify_window(segments, center_time, ...)` | Segments + window | Aggregated label. |
| `_cache_path(video_id)` / `_load_cached(video_id)` / `_save_cache(video_id, data)` | — | JSON cache I/O. |
| `fetch_retention_cached(video_id, force_refresh=False)` | video_id | Cached or freshly-fetched retention dict. |
| `analyze_video(video_id, title, duration_seconds, ...)` | video metadata | Per-video analysis dict. |
| `aggregate_results(analyses)` | List of analyses | Aggregate dict (top deltas, content-type effects). |
| `_fmt_time(seconds)` / `_delta_indicator(delta)` _(private)_ | — | Display helpers. |
| `generate_report(agg, analyses)` | Aggregate + per-video | Markdown report string. |
| `_generate_recommendations(agg)` _(private)_ | Aggregate | List of recommendation strings. |
| `run_analysis(video_id=None, cached_only=False, ...)` | filters | Full pipeline orchestrator. |
| `main()` | argv | CLI entry point. |

**CLI entry:** `python -m tools.youtube_analytics.retention_analysis [--video ID|--report|--cached]`.

**Side effects:** Writes `channel-data/patterns/RETENTION-SCRIPT-CORRELATION.md`, cache files.

---

## Module 5: `retention_by_topic.py`

**Purpose:** Compare retention curves bucketed by topic_type to find topic-specific drop signatures.

**Dependencies:** `analytics.db`, retention cache from `retention_analysis.py`.

| Function | Consumes | Produces |
|----------|----------|----------|
| `classify_topic(title, db_topic_type)` | Title + DB column | Topic bucket string (uses title regex with DB fallback). |
| `load_all_videos()` | analytics.db | List of video dicts. |
| `load_retention(video_id)` | video_id | Cached retention `data_points` or `None`. |
| `analyze_retention_curve(data_points)` | data_points | Curve summary (mean retention by zone). |
| `compute_avg_curve(all_curves)` | List of curves | Averaged curve. |
| `analyze_content_deltas_by_topic(...)` | Per-topic data | Per-topic delta dict. |
| `generate_report(...)` | Aggregate | Markdown report. |
| `main()` | argv | CLI entry point. |

**CLI entry:** `python -m tools.youtube_analytics.retention_by_topic`.

**Side effects:** Writes a markdown report (path defined inside `generate_report`).

---

## Module 6: `retention_predictor.py`

**Purpose:** Predict retention curve for a script *before publishing*. Mirrors decoder/scorer but runs forward (script → curve) instead of backward (data → constraints).

**Dependencies:** Standalone parser inside the file (`parse_script_with_structure`), no DB.

| Function | Consumes | Produces |
|----------|----------|----------|
| `_is_header(line)` / `_extract_header(line)` _(private)_ | Markdown lines | Header detection. |
| `_is_metadata_block(lines, start)` _(private)_ | Lines + cursor | End-line of metadata block. |
| `_should_skip_line(line)` _(private)_ | Line | Bool. |
| `_clean_inline_markdown(text)` _(private)_ | Text | Cleaned text. |
| `parse_script_with_structure(script_path)` | Path | List of `{header, sentences, line_start, word_count}` dicts. |
| `classify_section(section)` | Section dict | List of per-sentence classifications. |
| `summarize_section_types(classified)` | Classifications | Type-count summary dict. |
| `_get_position_zone(fraction)` _(private)_ | Float | Zone label. |
| `_estimate_read_minutes(word_count, wpm=160)` _(private)_ | Word count | Float minutes. |
| `_get_channel_avg_at(position_pct)` _(private)_ | Position % | Channel-baseline retention number (hardcoded). |
| `predict_from_file(script_path, verbose=False)` | Path | Prediction dict (see `predict_retention`). |
| `predict_from_text(script_text, verbose=False)` | Text | Same as `predict_from_file` but tempfile-backed. |
| `predict_retention(sections, verbose=False)` | Section list | `{curve, sections, flags, recommendations, total_words, estimated_script_duration_min, estimated_filmed_duration_min, predicted_final_retention, channel_avg_final_retention}`. |
| `_ascii_chart(curve, channel_avg=None, width=50)` _(private)_ | Curve | ASCII line chart string. |
| `generate_report(result, script_path, verbose=False)` | Prediction | Markdown report string. |
| `_find_script_for_project(slug)` _(private)_ | Project slug | Path to script file or None. |
| `main()` | argv | CLI entry point. |

**Note:** Has its OWN parser distinct from `tools.production.parser.ScriptParser`. Returns dicts, not `Section` objects — divergent from mapper/scorer.

**CLI entry:** `python -m tools.youtube_analytics.retention_predictor`.

**Side effects:** Reads tempfile in `predict_from_text`. No DB I/O.

---

## Module 7: `retention_scorer.py`

**Purpose:** Score individual script sections for predicted retention risk based on length, evidence density, modern relevance, and voice patterns. Generates STYLE-GUIDE-pattern-referenced warnings.

**Dependencies:** Optional `tools.discovery.database.KeywordDB` (for topic baselines), optional `section_diagnostics.load_voice_patterns` (with fallback).

| Function | Consumes | Produces |
|----------|----------|----------|
| `count_evidence_markers(text)` | Section text | Int count of evidence-marker hits. |
| `measure_modern_relevance_gap(text)` | Section text | Int — words since last "modern relevance" hit. |
| `detect_voice_patterns(text)` | Section text | List of detected pattern names. |
| `get_topic_baseline(topic_type)` | Topic string | Baseline dict from KeywordDB (or hardcoded fallback). |
| `score_section(section_text, section_type, topic_type, baseline=None)` | Section text + types | `{score, risk_level, warnings, metrics}`. `score` is float; `risk_level` ∈ `{LOW, MEDIUM, HIGH}`. |
| `score_all_sections(sections, topic_type)` | Section objects + topic | List of `score_section` results, each with `section_heading` added. **NOTE:** Expects `section.text` attribute, but `tools.production.parser.Section` exposes `.content`. Caller compatibility quirk. |
| `format_retention_warnings(scored_sections)` | Scored sections | Markdown warnings table. |

**Side effects:** Reads keywords.db for baselines (best-effort, has fallback). No writes.

---

## Cross-cutting observations

These are NOT design proposals (G2's scope), but visible facts:

1. **Two parsers in play.** `retention_predictor.parse_script_with_structure()` returns dicts; `retention_mapper`/`retention_scorer` use `tools.production.parser.ScriptParser` (which returns `Section` objects with `.heading`/`.content`). The scorer's `score_all_sections` expects `.text` — incompatible with the production parser's `.content` attribute.
2. **Three databases referenced.** `retention.py` (no DB, API-only), `retention_decoder`/`retention_analysis`/`retention_by_topic` (`analytics.db`), `retention_scorer` (`keywords.db` for baselines).
3. **Two retention-fetch paths.** `retention.py` fetches fresh; `retention_analysis.fetch_retention_cached` adds a cache layer. Neither uses the other.
4. **`_get_channel_avg_at` is a hardcoded baseline** in `retention_predictor.py`. The decoder computes channel avg dynamically. Two sources of truth for "channel average retention."
5. **`MIN_BUCKET_SIZE = 3`** appears only in decoder; analysis uses different thresholds; predictor uses none.
6. **No shared types.** Each module defines its own dict shape for retention/sections/scores — convergence would benefit from a single `RetentionPoint`, `Drop`, `ScoredSection` set of dataclasses.

---

## Pinning test reference

`tests/test_retention_pipeline.py` covers:
- `find_drop_off_points` shape (synthetic input — API skipped)
- `map_retention_to_sections` + `estimate_section_timestamps` shape
- `RetentionDecoder.classify_*` vocabulary
- `score_section` shape
- `predict_from_text` shape
- `classify_topic` and `classify_content` shape
- End-to-end pipeline composition (drops → mapped → scored)

Anything that breaks these tests during G2-G4 is a behavior change, not a refactor.
