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

- `traffic_sources` exists in **both** stores with diverging row counts (482 in analytics.db, 390 in keywords.db as of 2026-05-18). Origin of the duplication is unremembered. The divergence hasn't bitten any analysis yet. **Action deferred** — revisit if either side starts producing surprising numbers, or as part of the analytics-side storage seam refactor (see "Consequences").
- `tools/youtube_analytics/backfill.py:24` carries a stale docstring claim — `# Do NOT use analytics.db (empty). Use keywords.db via KeywordDB exclusively.` — which is factually wrong (analytics.db has live, recent writes) and will mislead future readers. **Action**: delete as part of the storage seam refactor.

## Consequences

- **Discoverability.** New contributors (human or agent) read this ADR before assuming the two stores are an accident.
- **Storage seam refactor (open).** The analytics.db side has no module-level seam — 29 callers reach `sqlite3.connect(analytics.db)` directly. A follow-up refactor will introduce an `AnalyticsStore` peer to `KeywordStore`, under a clean-cut migration. That refactor does **not** change this ADR — it operationalizes the split, it doesn't revisit it.
- **Re-litigation guard.** Future `/improve-codebase-architecture` runs that surface "consolidate the two stores" should be answered with this ADR. If the friction grows beyond the known items above, supersede this ADR rather than silently consolidating.
