# ADR-0018 — `impressions_daily` is the launch-window grain

**Status:** Accepted · **Date:** 2026-07-28
**Supersedes nothing. Constrains:** ADR-0017 (canonical valid-latest-CTR read) stays intact.

## Context

The channel's breakout hypothesis H3 (`channel-data/BREAKOUT-HYPOTHESES.md`) is pre-registered against
**first-28-day impressions** — confirm at ≥9,000, kill below 4,500. When we went to measure it we found the
instrument could not answer the question.

Four findings, all verified live on 2026-07-28:

1. **`ctr_snapshots.impression_count` is a sliding ~30-report-day sum ending ~D−3**, not a cumulative
   count. For any video older than about a month it does not contain the launch window at all.
2. **It is anchored to RUN date, not DATA date.** A missed collector run is unrecoverable: the window has
   already slid. This is not hypothetical — `HvH-CtrTracker` was registered **weekly, Mondays**, video #59
   published on a Sunday, and days 0–4 were never captured. 88% of that video's lifetime impressions landed
   on day 1.
3. **There is no cumulative endpoint.** YouTube Analytics API v2 rejects `impressions` outright
   (`HTTP 400: Unknown identifier`); `channel_traffic_source_a3` has no impressions column. Only
   `channel_reach_basic_a1` carries `video_thumbnail_impressions`, and it carries a `date` column — so
   cumulative must be **reconstructed by summing daily rows**.
4. **Reporting API retention is only ~60 days** (measured: 63 unique intervals, 2026-05-24 → 2026-07-25).
   Whatever is not ingested inside that window is gone for good.

## Decision

**Persist the daily fact. Derive everything else.**

New table `impressions_daily(video_id, metric_date, traffic_source, impressions, clicks, ctr_percent,
report_create_time, ingested_at)` with `PRIMARY KEY (video_id, metric_date, traffic_source)`, created via
the sanctioned seam `tools/discovery/schema_manager._ensure_impressions_daily_table()` and mirrored in
`tools/discovery/schema.sql` (both are required — the fresh-DB path runs `schema.sql`, the existing-DB path
runs the `_ensure_*` migrations; putting it in only one makes construction non-idempotent, which the
migration test correctly caught).

Consequences of that key:

- **Ingest is idempotent by data date.** A missed run self-heals on the next run while those days remain in
  retention. Verified: three consecutive full sweeps produced identical row counts and identical sums.
- **Regenerated reports REPLACE rather than ADD** (`ON CONFLICT ... DO UPDATE ... WHERE
  excluded.report_create_time > report_create_time`). The original double-count bug class is prevented
  structurally, not detected afterwards.
- **`traffic_source` is in the key from day one, defaulting to `'ALL'`.** H3 is framed on *browse*
  impressions but `channel_reach_basic_a1` reports totals. Job `31fd84bd-0dbf-436b-a608-8f80a16b2d93`
  (`channel_reach_combined_a1`) was created 2026-07-28 to find out whether a per-surface breakdown is
  available; its reports take 24–48h. If it delivers, browse-only rows land beside the `'ALL'` rows with no
  migration.

**`ctr_snapshots.impression_count` keeps its rolling meaning and is NOT repurposed.** Six consumers read it
with those semantics (`ctr_reads`, `swap_ledger`, `packaging_autopilot`, `performance_tracker`, and the two
backfill tools). Redefining a column under its consumers is the divergence ADR-0017 exists to prevent.

**Derived reads live in `tools/discovery/ctr_reads.py`** — the ADR-0017 seam — as `d28_for()` and
`d28_impressions_by_video()`. No new reads module.

**Completeness is measured against report coverage, not the video's own rows.** A day on which a video got
zero impressions produces no CSV row at all, so counting the video's rows made a fully-covered window read
24/28 and would have permanently excluded quiet videos from any baseline. `d28_for` therefore returns
`days_covered` (report-days held for the window) *and* `days_with_data` (days the video appeared), and
`complete` keys off the former.

**Validation is always-on.** The pre-existing lifetime check compares against a hand-made Studio CSV and in
practice never ran — partly because `take_snapshot` anchored the freshness gate to `date.today()` when the
real window ends ~D−3, making it permanently 3 days too strict. That anchor is fixed, and a second check
(`validate_rolling_against_daily`) compares the rolling aggregate to the daily rows the same run persisted.
Both derive from the same reports, so over the same window they must be equal — a duplicated report inflates
one and not the other. That check needs no manual input and runs every time.

## Consequences

- **`HvH-CtrTracker` must run daily** (changed 2026-07-28 from weekly Mondays). Not a preference: retention
  is ~60 days and this table is the only durable record of a launch window. Running more often than daily
  buys nothing — the API publishes one report per day.
- **Only two complete first-28-day windows are historically reconstructable** (`aSfZtrgGjwA` = 2,422 and
  `zt7VntgauC8` = 3,088), because retention predates everything older. **The 9,000/4,500 thresholds
  therefore rest on n=2.** Do not silently retune them — that is what pre-registration exists to prevent —
  but state the basis honestly wherever they are cited.
- **Manual Studio Advanced-mode exports are the only route to older history.** `studio_import.py` already
  supports `--surface browse --start --end` and content-hashes for idempotency; no code is needed, it is
  data entry.
- **A total-impressions threshold cannot distinguish a demand pocket from a failed test batch.** #59 reached
  10,087 by day 21 and would "confirm" H3, yet 88% arrived on day 1 and serve collapsed to ~44/day by day 3.
  Now that daily shape is available, H3 needs a second, shape-based criterion — written into
  `BREAKOUT-HYPOTHESES.md` and dated **before** the next publish, or it is post-hoc.

## Verification (real data, per `validation-standards`)

| check | expected | result |
|---|---|---|
| Reconstruction oracle | #59 cumulative @2026-07-23 ≈ Studio lifetime 10,925 | **10,930** (0.05%) |
| Day-0 recovery | rows for 2026-07-04 = 865, 2026-07-05 = 9,626 — days never collected | **both present** |
| Complete windows | `aSfZtrgGjwA` 2,422 · `zt7VntgauC8` 3,088 · #59 10,087/21/partial | **all three exact** |
| Idempotency | three consecutive sweeps → identical rows and sum | **2,255 / 33,538 unchanged** |
| Double-count trip-wire | doubling one video's rolling figure must fail the closed-loop check | **caught** |
| Consumer non-regression | ADR-0017 contract unmoved | **full suite: 803 passed, 13 skipped** |
