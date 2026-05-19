# Two-store split: analytics.db vs keywords.db

**Date:** 2026-05-18
**Status:** accepted

This is the first code-architecture ADR in the project (prior ADRs are content decisions). It exists because a `/improve-codebase-architecture` pass flagged the two-store layout as a "consolidate" candidate, and the rationale for keeping them separate lives only in git history. Future re-runs of the same skill — or future me — will keep proposing consolidation unless the reasoning is written down.

## The split

- **`tools/youtube_analytics/analytics.db`** — our channel's data, pulled from the YouTube Data + Analytics APIs. Tables: `videos`, `daily_channel`, `traffic_sources`. Origin commit: `30dbe86 feat(55): analytics data foundation — YouTube API backfill into analytics.db`. Writers: `growth_data.py`, `ctr_tracker.py`, `traffic_analysis.py`. Entry point in active workflow: `python -m tools.youtube_analytics.backfill`.
- **`tools/discovery/keywords.db`** — discovery and packaging intelligence, fed by VidIQ keyword data and downstream scoring. Tables: `keywords`, `keyword_performance`, `opportunity_scores`, `title_variants`, `thumbnail_variants`, `ctr_snapshots`, `lifecycle_history`, and others. Owned by `tools/discovery/` (phase-H extracted `KeywordStore`, `PerformanceTracker`, `IntentClassifier` from a previously monolithic `database.py`).

The two stores answer different questions: *"how is our channel performing?"* vs *"what should we make next, and how should we package it?"*. They have different upstream sources (YouTube API vs VidIQ), different write cadences, and different consumers.

## Why not consolidate

- **Upstream divergence.** YouTube API and VidIQ are unrelated providers with unrelated schemas and unrelated rate limits. Merging them into one store gives a schema with `NULL`-heavy columns and no natural primary key.
- **Failure isolation.** A VidIQ data corruption shouldn't be able to break the backfill of our own retention metrics, and vice versa.
- **Lifecycle.** `analytics.db` rows are append-mostly (each video gets one row, daily metrics accumulate). `keywords.db` rows are highly mutable (opportunity scores re-rank, variants get tested and retired). Different mutation patterns favor different schemas.

## Considered alternatives

- **Consolidate into one store.** Rejected for the reasons above. Also: consolidation would require migrating the phase-H seam (`KeywordStore` etc.) — that work has already paid for itself in locality, and re-shuffling it costs more than it saves.
- **Three-store split** (e.g., extracting `ctr_snapshots` out of keywords.db into its own store, because CTR is "our data" not "discovery data"). Rejected — `ctr_snapshots` is tied to `title_variants` and `thumbnail_variants` and lives in their lifecycle.

## Known friction (not blockers, but worth recording)

- `traffic_sources` exists in **both** stores with diverging row counts (482 in analytics.db, 390 in keywords.db as of 2026-05-18). Origin of the duplication is unremembered. The divergence hasn't bitten any analysis yet. **Action deferred** — revisit if either side starts producing surprising numbers.
- ~~`tools/youtube_analytics/backfill.py:24` carries a stale docstring claim~~ **(resolved before stage 2 — the claim is no longer present in the file).**

## Consequences

- **Discoverability.** New contributors (human or agent) read this ADR before assuming the two stores are an accident.
- **Storage seam refactor (closed 2026-05-19).** The analytics.db seam was operationalized in five stages between 2026-05-18 and 2026-05-19:
  - *Stage 1* (commit `1e524dc`) — `AnalyticsStore` introduced as a read-only peer to `KeywordStore`, with `videos()`, `traffic_sources()`, `traffic_totals_by_source()`, `daily_channel()`, `execute()`. Cross-store `views.py` merge module added.
  - *Stage 2* (commits `86709f7`, `dad0370`, `a3de4e4`) — three clean read-side bypassers migrated: the weekly retention routine, `description_analyzer`, and `reconcile.analytics_db_age_hours`.
  - *Stage 3* (commits `5d0ab22`, `3890ad4`, `221341d`) — write side opened. `upsert_traffic_source()` + `commit()` added; `traffic_analysis.save_traffic_json`, `backfill._build_traffic_section`, and `growth_data.store_traffic_sources` all migrated. The duplicate `INSERT OR REPLACE` vs `INSERT ... ON CONFLICT` SQL for the same table collapsed to one path.
  - *Stage 4* (commits `ff14ac2`, `8357c52`, `abc843c`, `c07a823`, `ede4766`) — mixed-DB callers (`packaging_autopilot`, `packaging_intel`, `reconcile/match`) migrated for their analytics.db touch points; `upsert_daily_metric` added + `growth_data.store_daily_metrics` migrated; `VideoRow` dataclass + `upsert_video` added + `growth_data.store_videos` migrated.
  - All `sqlite3.connect(analytics.db)` callers now route through `AnalyticsStore` except `growth_data.ensure_schema()`, which keeps a raw conn — schema migration is intentionally outside the domain-write surface.
- **Re-litigation guard.** Future `/improve-codebase-architecture` runs that surface "consolidate the two stores" should be answered with this ADR. If the friction grows beyond the known items above, supersede this ADR rather than silently consolidating.
