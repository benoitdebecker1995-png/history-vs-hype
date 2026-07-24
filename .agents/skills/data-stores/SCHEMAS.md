# Data-store schemas & ownership matrix

Depth file for [SKILL.md](SKILL.md). Row counts and freshest-timestamps are as of the live-verified
inventory pass of 2026-07-01/02 — they drift daily; treat them as scale indicators, not current values.
Re-check freshness with the recipes in SKILL.md. Anything not cheaply re-verifiable is marked [UNVERIFIED].

## analytics.db — `D:\History vs Hype\tools\youtube_analytics\analytics.db`

Schema versioning: `growth_data.py` `ensure_schema()`, `PRAGMA user_version`, `CURRENT_SCHEMA_VERSION = 3`
(v1 = videos/traffic_sources/daily_channel; v2 = retention_curves/search_terms/subscribed_status;
v3 = opener_retention). WAL mode set by `AnalyticsStore._open_conn`.

| Table | Rows | Key columns / notes |
|---|---|---|
| `videos` | 57 | `video_id` PK, title, published_at, duration_seconds, tags JSON, views, watch_time_minutes, avg_view_duration_seconds, `avg_view_percentage` (PERCENT, e.g. 35.3), likes/comments/shares, subscribers_gained/lost, impressions, `ctr_percent` (typically NULL — not a CTR source), topic_type, angles JSON, fetched_at, **`metrics_fetched_at`** (the reconcile freshness-gate column) |
| `traffic_sources` | 516 | id PK AUTOINC, video_id, source_type (YT_SEARCH/RELATED_VIDEO/SUBSCRIBER/…), views, watch_time_minutes, UNIQUE(video_id, source_type) |
| `daily_channel` | 210 | `day` TEXT PK, channel-level daily views/watch/subs/likes. No per-video per-day table exists anywhere |
| `retention_curves` | 5,700 | PK (video_id, elapsed_ratio 0.00–1.00, ~100 buckets), `audience_watch_ratio` (FRACTION, 1.0 = 100%), relative_performance |
| `search_terms` | 139 | PK (video_id, term), views, watch_time_minutes |
| `subscribed_status` | 113 | PK (video_id, status SUBSCRIBED/UNSUBSCRIBED), views, watch, avg_view_percentage |
| `opener_retention` | 21 | video_id PK, opener_text (verbatim 0:00–0:30 from SRT), hook_archetype, first_30s_retention (FRACTION), intro_drop_30s, topic_type. DIAGNOSTIC-ONLY per schema comment |
| `surface_ctr` | 56 | video_id PK, browse_impr/browse_ctr, sugg_impr/sugg_ctr. No timestamp column. Session-written 2026-06-27 |
| `thumbnail_features` | 47 | video_id PK, boolean-ish tags: doc, cf, em, map, busy, red. No timestamp column. Session-written 2026-06-27 |

`growth_data.EXCLUDED_VIDEO_IDS` hard-excludes two 2014 pre-channel test uploads
(`-EFfYT190ew`, `exDA-YSe-nc`) at fetch time so purges survive refreshes.

### Ownership (all writes via `AnalyticsStore` — effective writers are the store-method callers)

| Table | Writers (effective) | Readers |
|---|---|---|
| videos | growth_data (`store.upsert_video`) | reconcile (match + reconcile.py), retitle_gen, packaging_intel, packaging_autopilot, benchmark/outlier_title_dissector, discovery/performance_tracker, ya/feedback_queries, growth_dashboard, patterns, retention_inference, channel-health routine (raw SQL embedded in its prompt — schema changes break it silently), routines/retention_audit_weekly |
| traffic_sources | growth_data (`upsert_traffic_source`), traffic_analysis | backfill, views.py (cross-store merge), growth_data |
| daily_channel | growth_data (`upsert_daily_metric`) | growth_data, growth_dashboard (reader list grep-verified 2026-07-03) |
| retention_curves | growth_data (`upsert_retention_point`) | backfill, retention_analysis / retention_by_topic / curve_shape_analysis / opener_retention via store, routines/retention_audit_weekly |
| search_terms | growth_data (`upsert_search_term`) | backfill, search_term_analysis |
| subscribed_status | growth_data (`upsert_subscribed_status`) | analysis modules via store surface |
| opener_retention | `tools/youtube_analytics/opener_retention.py` backfill (via `store.upsert_opener_retention` — call site `opener_retention.py:133`, verified 2026-07-03) | `/opener` command, `get_opener_diagnostic()` |
| surface_ctr | NO code writer (one-off session scripts 2026-06-27, flop-autopsy/CTR-audit) | NO code reader — queried conversationally; cited by `tools/PACKAGING_MANDATE.md` |
| thumbnail_features | same | same — hypotheses in `channel-data/CTR-THUMBNAIL-FINDINGS-2026-06.md` derive from it |

## keywords.db — `D:\History vs Hype\tools\discovery\keywords.db`

Schema evolution: `tools/discovery/schema_manager.py` (also writes the `backups/keywords_pre_v27_*.db`
pre-migration copies — one per migration-path run; 18 present at the 2026-07-02 recount, pruning behavior unverified).

| Table | Rows | Freshest ts (at audit) | Notes |
|---|---|---|---|
| `keywords` | 122 | last_updated 2026-06-11 | keyword UNIQUE, search_volume, competition_score, vidiq_overall_score, source, lifecycle_state, production_constraints, opportunity_score_final |
| `keyword_intents` | 144 | — | PK (keyword_id, intent_category), confidence |
| `keyword_performance` | 163 | measured_date 2026-03-16 | keyword↔video impressions/ctr/views |
| `opportunity_scores` | 141 | calculated_at 2026-03-08 | demand/competition/ratio/category |
| `lifecycle_history` | 112 | transitioned_at 2026-03-08 | WRITE-ONLY — no code reads it |
| `title_variants` | 91 | created_at 2026-03-08 | per-video A/B title text + formula_tags |
| `thumbnail_variants` | 43 | created_at 2026-03-06 | per-video variant file_path + perceptual_hash |
| `ctr_snapshots` | 1055 | snapshot_date 2026-07-03 (weekly Mon refresh via HvH-CtrTracker) | per-video dated CTR/impressions/views; FKs to video_performance + active variant ids; `is_late_entry` flag. Feeds title_scorer live-CTR. **Not channel-only:** 313 distinct video_ids vs 57 channel videos (competitor/study rows) + multiple rows per (video, date) — join to `analytics.videos` and dedup latest-per-video before any channel aggregate |
| `video_performance` | 386 | fetched_at 2026-06-25 | ~57 videos × multiple fetch generations — ALWAYS take latest `fetched_at` per video_id; + retention_drop_point, discovery_issues, lessons_learned, avg_retention_pct, ctr_percent, impression_count |
| `section_feedback` | 137 | created_at 2026-03-10 | per-section retention notes |
| `script_choices` | 16 | choice_date 2026-03-06 | selected/rejected script variants per project |
| `creator_techniques` | 10 | created_at 2026-02-14 | technique library |
| `trends` | 78 | fetched_at 2026-02-24 | Google Trends interest per keyword |
| `traffic_sources` | 390 | fetched_at 2026-03-10 | DEAD duplicate of analytics.db table (ADR-0004 known friction). Different UNIQUE constraint too: (video_id, source_type, fetched_at) vs analytics' (video_id, source_type) |
| `daily_channel_metrics` | 89 | — | DEAD — zero writers AND zero readers |
| `swap_experiments` | 5 | swap_date 2026-06-26 | single-variable title/thumbnail swap ledger: baseline/post CTR+impressions, surface, verdict PENDING/LIFT/FLAT/DROP |
| view `keyword_analysis` | — | — | defined in `tools/discovery/schema.sql`; no code readers found |

### Ownership

| Table | Writers | Readers |
|---|---|---|
| keywords | keyword_store, orchestrator, backfill_high_impact | keyword_store, backfill_gaps, backfill_high_impact, intent_mapper, intel/competitor_patterns, packaging_intel, preflight/demand_checker + demand_scorer, swap_ledger, title_ctr_store, topic_pipeline, ya/gap_analyzer, ya/title_intelligence, ya/views |
| keyword_intents | keyword_store | keyword_store |
| keyword_performance | keyword_store, backfill_high_impact | keyword_store, backfill_high_impact |
| opportunity_scores | keyword_store | keyword_store |
| lifecycle_history | keyword_store | NOBODY (write-only) |
| title_variants / thumbnail_variants | performance_tracker, backfill_high_impact | performance_tracker, backfill_high_impact |
| ctr_snapshots | **ya/ctr_tracker** (main), performance_tracker, ctr_quick_add | title_ctr_store → title_scorer (live-CTR + staleness date), ya/benchmarks, swap_ledger, packaging_autopilot, ctr_quick_add, backfill_gaps, backfill_high_impact, ya/backfill, ya/views |
| video_performance | performance_tracker, ya/backfill | title_scorer, title_ctr_store, topic_pipeline, preflight/demand_checker, intel/competitor_patterns + topic_scorer, ya/analyze + benchmarks + feedback_queries + playbook_synthesizer + topic_strategy, backfill_gaps/high_impact |
| section_feedback | backfill_high_impact | backfill_high_impact |
| script_choices / creator_techniques | ya/technique_library (+ backfill_high_impact for script_choices) | same |
| trends | discovery/schema_manager | discovery/trends, backfill_gaps |
| traffic_sources (kw copy) | NOBODY (dead since 2026-03-10) | possibly legacy paths [UNVERIFIED — greps resolve to the analytics.db copy] |
| daily_channel_metrics | NOBODY | NOBODY |
| swap_experiments | tools/swap_ledger.py | tools/swap_ledger.py (+ derived `channel-data/SWAP-LEDGER.md`) |

("ya/" = `tools/youtube_analytics/`.)

## intel.db — `D:\History vs Hype\tools\intel\intel.db`

| Table | Rows | Freshest ts (at audit) | Notes |
|---|---|---|---|
| `algo_snapshots` | 17 | refreshed_at 2026-06-13 | JSON blobs: algorithm model, signal_weights, longform_insights, confidence |
| `competitor_channels` | 20 | added_at 2026-06-11 | bootstrapped/synced from `tools/intel/competitor_channels.json` on every refresh |
| `competitor_videos` | 1,800 | fetched_at 2026-07-01 | + is_outlier, outlier_reason, topic_cluster, outlier_ratio. Purge-and-replace on full refresh |
| `kb_meta` | 1 | last_refresh 2026-06-13 (live-verified 2026-07-02) | staleness/version row; `KBStore.is_stale(max_age_days=7)` |
| `niche_snapshots` | 15 | refreshed_at 2026-06-13 | JSON: format/hook patterns, trending topics |

### Ownership

| Table | Writers | Readers |
|---|---|---|
| algo_snapshots | kb_store (refresh Phase 3) | intel/topic_scorer, kb_store/query |
| competitor_channels | kb_store, query, packaging_intel (+ json bootstrap) | benchmark/rescan_corpus, discovery/discovery_scanner + intent_classifier, intel/competitor_tracker + refresh, packaging_intel |
| competitor_videos | kb_store (purge-and-replace), packaging_intel, discovery/backfill_gaps + intent_classifier, intel/competitor_patterns | topic_pipeline, ya/gap_analyzer, intel/topic_scorer + competitor_patterns, discovery modules |
| kb_meta | kb_store | kb_store (`is_stale`), query (staleness footer) |
| niche_snapshots | kb_store (refresh Phase 8) | intel/topic_scorer, kb_store |

## Timestamp dialects (why freshness math goes wrong)

Machine local timezone: America/Lima, UTC-5. Mixed dialects in the DBs:
- ISO-UTC `+00:00` — `fetched_at` written via the stores
- `Z`-suffix — `published_at` from the YouTube API
- DATE-only columns — throughout keywords.db (`snapshot_date`, `measured_date`, …)
- naive local `datetime.now()` — some log filenames

`check_db_freshness` (tools/logging_config.py) parses only the date part and pins UTC midnight
(up to ~1 day error). `reconcile.analytics_db_age_hours` correctly normalizes `Z` and naive→UTC.
Both return **sentinel 999** on any read failure — indistinguishable from "very stale" downstream.

## Backups & sidecars

- `tools/discovery/backups/keywords_pre_v27_*.db` — pre-migration copies of keywords.db, one per
  migration-path run (18 present at the 2026-07-02 recount; pruning behavior unverified).
- WAL `-wal`/`-shm` sidecars: none existed at inspection (clean checkpoint), but the three main DBs are
  git-tracked and perpetually "modified" — a mid-write snapshot can produce confusing diffs. Always
  inspect with `mode=ro` URIs.
- `tools/history-clip-tool/data/projects.db` — dormant SQLAlchemy store (1 project, 0 clips, last
  touched 2026-01-08). Out of scope.
