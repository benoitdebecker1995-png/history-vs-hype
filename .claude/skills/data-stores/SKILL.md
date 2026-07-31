---
name: data-stores
description: Map of the repo's data layer — the three live SQLite databases (analytics.db, keywords.db, intel.db), the flat-file data stores, refresh chains and staleness semantics, the truth-source hierarchy for project state, and AUTO-zone rules in status docs. Use when: querying or citing numbers from analytics.db / keywords.db / intel.db; asking "which table holds X"; data looks stale, missing, or frozen; deciding which source is authoritative for project state; editing PROJECT-STATUS.md anywhere near an <!-- AUTO: --> block; tempted to add, drop, or "clean up" a table. NOT for diagnosing why an automation broke (→ debugging-playbook) or scheduled-task registration/admin (→ automation-ops).
---

# Data Stores

## The four databases

| DB | Path | Question it answers | Freshness column |
|---|---|---|---|
| analytics.db | `G:\History vs Hype\tools\youtube_analytics\analytics.db` | "How is OUR channel performing?" (YouTube Data + Analytics APIs) | `videos.metrics_fetched_at` |
| keywords.db | `G:\History vs Hype\tools\discovery\keywords.db` | "What should we make next / how to package it?" (VidIQ + downstream scoring + real CTR) | `ctr_snapshots.snapshot_date` |
| intel.db | `G:\History vs Hype\tools\intel\intel.db` | Competitor / algorithm knowledge base | `kb_meta.last_refresh` |
| projects.db | `G:\History vs Hype\tools\history-clip-tool\data\projects.db` | DORMANT — unrelated Shorts clip tool, untouched since 2026-01. Exclude from all data-layer reasoning. | — |

The analytics/keywords split is DELIBERATE — different providers, different mutation
patterns, failure isolation. **Never propose consolidating them**; the standing answer is
`docs/adr/0004-two-store-split-analytics-vs-keywords.md` (read it before touching either schema).

## Which number lives where (routing)

- **Views, retention, traffic sources, impressions** → analytics.db.
- **CTR** → keywords.db `ctr_snapshots`. The Analytics API does not serve CTR for this channel, so
  `analytics.db videos.ctr_percent` is typically NULL — **analytics.db is not an API CTR source**
  (the session-written `surface_ctr` table DOES hold browse/suggested CTR splits — see its row below).
  Writer: `python -m tools.youtube_analytics.ctr_tracker` (weekly Mon 07:30 via `HvH-CtrTracker` since 2026-07-03; see staleness below).
  **Channel-filter trap (live-verified 2026-07-02):** the table also holds NON-channel video_ids
  (313 distinct ids vs 57 channel videos — competitor/study rows, even an excluded 2014 test upload)
  and multiple rows per (video, date). Any channel-level aggregate must join to `analytics.db videos`
  and dedup to latest-per-video — and even then, don't present a self-computed aggregate as
  “the channel median”: the canonical distribution analysis (median 2.51%, n≈56, 2026-06) lives in
  `channel-data/FLOP-AUTOPSY-TABLE.md`; snapshots mix dates, so recompute deliberately, not casually.
- **Competitor videos / algo + niche snapshots** → intel.db.
- **Project lifecycle state** → filesystem + analytics.db + PROJECT-STATUS.md narrative (hierarchy below) — never a registry doc alone.
- **Post-publish analysis** → the POST-PUBLISH-ANALYSIS.md markdown corpus (ADR-0005), read via
  `tools/post_publish/` `PostPublishStore` — the fourth canonical store.

## analytics.db (11 tables — schema v5)

Schema owner: `tools/youtube_analytics/growth_data.py` `ensure_schema()` (the only sanctioned raw-conn
writer). ALL other writes route through `AnalyticsStore` in `tools/youtube_analytics/store.py` — never
open a raw write connection. `AnalyticsStore.open()` raises `FileNotFoundError` if the DB is missing
(no auto-create). WAL mode is on; use `mode=ro` URIs for inspection.

| Table | What | Written by (effective) |
|---|---|---|
| `videos` | 1 row/video (n≈57): views, watch time, `avg_view_percentage`, impressions, `metrics_fetched_at` | growth_data --refresh (daily 07:45) |
| `traffic_sources` | per-video per-source views (LIVE copy — see dead twin in keywords.db) | growth_data, traffic_analysis |
| `daily_channel` | channel-level daily metrics. **Channel-level ONLY — no per-video per-day table exists**, so per-video velocity checks are impossible on this schema | growth_data |
| `retention_curves` | ~100 buckets/video, `audience_watch_ratio` | growth_data |
| `search_terms`, `subscribed_status` | per-video search terms / sub-status splits | growth_data |
| `opener_retention` | first-30s retention per opener (n=21). DIAGNOSTIC-ONLY — too small to rank | opener_retention backfill module |
| `surface_ctr`, `thumbnail_features` | browse/suggested CTR splits + thumbnail tags | **no code writer** — session-written 2026-06-27 |

- **`surface_ctr` + `thumbnail_features` look orphaned but are LOAD-BEARING** — they back the current
  packaging mandate (`tools/PACKAGING_MANDATE.md` cites them). They're queried conversationally, not by
  code. Do NOT "clean them up".
- **Units flip:** `videos.avg_view_percentage` is a PERCENT (28.1); `retention_curves.audience_watch_ratio`
  and `opener_retention.first_30s_retention` are FRACTIONS (0–1). This exact confusion was once a silent
  live bug (ADR-0005). Check units before comparing across tables.
- Two 2014 pre-channel test uploads are hard-excluded at fetch (`growth_data.EXCLUDED_VIDEO_IDS`).

## keywords.db (16 tables + 1 view)

Schema evolution: `tools/discovery/schema_manager.py` (writes a `backups/keywords_pre_v27_*.db` copy on
every migration-path run; 18 present at the 2026-07-02 recount — the count fluctuates, pruning behavior unverified). Domain seams:
`tools/discovery/keyword_store.py` (`KeywordStore`), `performance_tracker.py`, `intent_classifier.py`.

Live tables that matter: `keywords`, `keyword_intents`, `keyword_performance`, `opportunity_scores`,
`title_variants`, `thumbnail_variants`, `ctr_snapshots`, `video_performance`, `swap_experiments`,
`trends`, `section_feedback`, `script_choices`, `creator_techniques`.

**Dead / trap tables — never read these for current numbers:**

| Table | Status |
|---|---|
| `traffic_sources` (keywords copy) | DEAD — frozen 2026-03-10, no writer. The LIVE copy is in analytics.db (ADR-0004 "known friction") |
| `daily_channel_metrics` | DEAD — zero writers AND zero readers; superseded by analytics.db `daily_channel` |
| `lifecycle_history` | write-only — no code reads it |
| view `keyword_analysis` | no code readers |

- **`video_performance` has ~386 rows for ~57 videos** — fetch generations accumulate. Always take the
  latest `fetched_at` per `video_id` (that's what `title_ctr_store` does).
- `swap_experiments` is truth for title/thumbnail swap tests; `channel-data/SWAP-LEDGER.md` is a DERIVED
  view regenerated by `tools/swap_ledger.py` — edit via the tool, never the .md.

## intel.db (5 tables)

Seam: `tools/intel/kb_store.py` (`KBStore`). Tables: `algo_snapshots`, `niche_snapshots`,
`competitor_channels`, `competitor_videos`, `kb_meta`. Staleness: `KBStore.is_stale(max_age_days=7)` off
`kb_meta.last_refresh`; every `tools/intel/query.py` output carries a staleness footer. Full refresh:
the old `/intel` command was removed — the live path is `python -c "from tools.intel.refresh import run_refresh; run_refresh()"`
from repo root (10-phase, network-heavy, do NOT run casually; exports `channel-data/youtube-intelligence.md`). `competitor_videos` is
purge-and-replace on refresh, but `tools/packaging_intel.py` also writes it incrementally — so
competitor rows can be weeks fresher than the snapshots (observed: videos 2026-07-01 vs snapshots
2026-06-13; that gap is normal, not a bug). `competitor_channels` re-bootstraps from
`tools/intel/competitor_channels.json` (repo file = source of truth) on every refresh.

## Refresh chains & staleness semantics

**Morning chain (Windows scheduled tasks — admin detail lives in automation-ops):**
07:45 `HvH-GrowthRefresh` writes analytics.db → 08:00 `HvH-ChannelHealth` reads it (READ-only) →
08:30 `HvH-Reconcile` freshness-gates on it → 09:00 `HvH-StaleProjects`. (Mondays: 07:30
`HvH-CtrTracker` first.) If the laptop was off/asleep, `HvH-MorningCatchup` (logon + 10:30
sweeper, since 2026-07-03) re-runs whatever is missing in this exact order.

- **Reconcile 36h gate** (`tools/reconcile/reconcile.py`, `MAX_DB_AGE_HOURS = 36`): in
  `--auto-publish-only` mode, if `MAX(metrics_fetched_at)` in `videos` is >36h old it writes
  `.brain/_inbox/reconcile-stale-db-YYYY-MM-DD.md`, exits 2, changes nothing. Any read failure returns
  **sentinel 999** — a locked/missing DB looks identical to a stale one.
- **The stale-alert prose blames "Routine 3" — that wording predates the 2026-06-13 fix.** The refresher
  is Routine 7 (`HvH-GrowthRefresh`); Routine 3 only reads. Manual refresh:
  `python -m tools.youtube_analytics.growth_data --refresh`.
- **Catch-up storms break ordering:** if the PC was off at trigger time, `StartWhenAvailable` fires all
  morning tasks simultaneously — reconcile can gate-abort while the refresh is still writing (observed
  live 2026-07-01). Fresh-but-unscanned is the expected aftermath; re-run reconcile after the refresh.
- **`ctr_snapshots` staleness ≠ analytics.db staleness.** analytics.db refreshes daily; `ctr_snapshots`
  moves when `ctr_tracker` runs — weekly Mon 07:30 via `HvH-CtrTracker` since 2026-07-03 (it previously froze for 18 days unscheduled; if stale again see F14).
  `title_scorer`'s live-CTR enrichment inherits this lag and reports it via
  `title_ctr_store.get_latest_snapshot_date()`. Related trap: the `/retitle` audit parses
  `channel-data/patterns/CROSS-VIDEO-SYNTHESIS.md`, bulk-generated 2026-03-07 and appended
  piecemeal since (F13) — real CTR lives in `ctr_snapshots`.
- Generic checker: `tools/logging_config.py:check_db_freshness(db, table, date_col, warn_days=7)`
  (allowlisted tables only; date-only parsing, up to ~1 day error; 999 sentinel on failure).
- **Timezones:** machine local = UTC-5 (America/Lima); DB timestamps are UTC with mixed dialects
  (`+00:00`, `Z`-suffix, DATE-only, naive-local log names). Compare in UTC or a 48h-stale reading can
  look like 43h.
- **Committed .db copies lag the local ones** — the three main DBs are git-tracked and show as
  perpetually modified. Never trust a checked-out .db on another machine for freshness decisions.

## Truth-source hierarchy (project state)

Authoritative, in order (CLAUDE.md §Project State Reconciliation — this deepens, doesn't repeat it):
1. **Filesystem** — which lifecycle folder the project sits in. `_BACKLOG/` + `_ARCHIVED/old-*` are
   outside the lifecycle and invisible to every scanner.
2. **analytics.db** — publish status (video_id, title, published_at). Reconcile trusts it INSTEAD of
   calling the YouTube API.
3. **Per-folder `PROJECT-STATUS.md` narrative** below the AUTO zone — hand-written, never machine-touched.

Everything else is DERIVED and regenerated by `/reconcile` — folder moves, the AUTO blocks, root
`video-projects/PROJECT_STATUS.md`, `PROJECT_REGISTRY.md`, `.brain/index.md §3`. Never hand-edit derived
surfaces; fix the truth source and re-run.

- Read-only navigation: `tools/video_projects/repo.py` `VideoProjectRepo` (ADR-0008). Mutation stays in
  reconcile. `by_slug()` raises `AmbiguousSlugError` on multiple matches — surface it, don't guess.
- Match overrides: `tools/reconcile/manual-matches.json` (hand-edited, wins over all matching tiers).
  **A `null` value means "NEVER match this folder"** — a deliberate block against stray video IDs in
  project files, not "unknown". Read its `_review_notes` before editing.
- POST-PUBLISH corpus reader exposes BOTH `.avg_retention_pct` (28.1) and `.avg_retention_fraction`
  (0.281) — pick deliberately.

## AUTO zones (fenced machine-owned blocks)

Grammar owner: `tools/video_projects/status_doc.py` — one `AutoZone` class holds markers, placement, and
the single write surgery (ADR-0014, `docs/adr/0014-statusdoc-owns-auto-zone-grammar.md`; read before
touching any fence logic — the surgery used to exist in three drifting copies). Marker matching is
**exact-string INCLUDING the note text** — a "harmless" edit to a marker line orphans the zone.

| Zone | Marker starts | Lives in | Body owner |
|---|---|---|---|
| `RECONCILE_ZONE` | `<!-- AUTO:reconcile` | each per-project `PROJECT-STATUS.md`, claims the TOP — a rewrite discards everything above its close marker | `reconcile.render_auto_block` |
| `PACKAGING_LOCK_ZONE` | `<!-- AUTO:packaging-lock` | same file, below the reconcile zone | `packaging_lock.render_lock_block` (ADR-0012 filters) |
| `RECONCILE_DASHBOARD_ZONE` | `<!-- AUTO:reconcile-dashboard` | root `video-projects/PROJECT_STATUS.md`, claims the top | `reconcile.render_root_status_block` |

Hand-edit rules: never edit inside a fence; write narrative only BELOW `<!-- /AUTO:reconcile -->` in
per-project files; the root dashboard's zone is machine-owned. New machine-owned block? Register an
`AutoZone`, don't write a fourth copy of the surgery. Tests pin this: `tests/test_status_doc.py`.

## Flat-file data stores (the ones with a machine writer or reader)

| File | Truth status |
|---|---|
| `channel-data/TOPIC-PIPELINE.md` | written by `tools/topic_pipeline.py`; read by discovery + routines |
| `channel-data/SWAP-LEDGER.md` | DERIVED from keywords.db `swap_experiments` — never hand-edit |
| `channel-data/youtube-intelligence.md` | DERIVED export of intel.db (refresh Phase 9) |
| `channel-data/patterns/CROSS-VIDEO-SYNTHESIS.md` | appended by `tools/ctr_quick_add.py` (dual-write with `ctr_snapshots`) |
| `channel-data/channel-insights.md` | written by `tools/youtube_analytics/backfill.py` Stage 4 |
| `channel-data/calibration/*` (CORPUS, EVAL-BASELINE, INTERVIEW-AGENDA) | Claude-session-written at script lock (conversational trigger); no tool code touches them |
| `channel-data/RETITLE-SHORTLIST.md` | session-written via `/retitle` |
| `channel-data/stats.md` | RETIRED — never existed; the channel-health routine that referenced it now computes its baseline live from analytics.db + ctr_snapshots (fixed 2026-07-03, F21). Don't create it |
| `channel-data/{competitor-drops,modern-relevance,keyword-tracking,retention-audits}/` | dated routine outputs |
| `tools/reconcile/manual-matches.json` | hand-edited override map (null = block) |
| `.brain/last-reconcile-ts.txt` + `.brain/_inbox/*` | reconcile heartbeat, run logs, reversible `.diff` files (power `--undo`) |

## Read-only query recipes (copy-paste, Git Bash / the Bash tool)

All five one-liners below ran live on this machine 2026-07-02/03. Pattern: `mode=ro` URI — spaces in the
path are accepted as-is. No `sqlite3` CLI exists here — always go through `python -c`. From PowerShell,
run these via the Bash tool or a temp .py file; don't fight PS quoting.

```bash
# Is analytics.db fresh? (reconcile's 36h gate reads exactly this)
python -c 'import sqlite3; con=sqlite3.connect(r"file:D:/History vs Hype/tools/youtube_analytics/analytics.db?mode=ro", uri=True); print(con.execute("SELECT MAX(metrics_fetched_at) FROM videos").fetchone()[0])'

# Top videos by views (units: avg_view_percentage is a PERCENT)
python -c 'import sqlite3; con=sqlite3.connect(r"file:D:/History vs Hype/tools/youtube_analytics/analytics.db?mode=ro", uri=True); [print(r) for r in con.execute("SELECT video_id, title, views, avg_view_percentage FROM videos ORDER BY views DESC LIMIT 10")]'

# Latest REAL CTR per CHANNEL video (joins analytics.db to exclude the ~256 non-channel rows and
# dedup to latest snapshot per video; ran live 2026-07-03). NEVER compute a fresh "current median"
# casually — canonical: median 2.51% (n≈56, 2026-06) in channel-data/FLOP-AUTOPSY-TABLE.md.
python -c 'import sqlite3; con=sqlite3.connect(r"file:D:/History vs Hype/tools/discovery/keywords.db?mode=ro", uri=True); con.execute("ATTACH DATABASE \"file:D:/History vs Hype/tools/youtube_analytics/analytics.db?mode=ro\" AS a"); [print(r) for r in con.execute("SELECT c.video_id, c.ctr_percent, c.impression_count, MAX(c.snapshot_date) FROM ctr_snapshots c JOIN a.videos v ON v.video_id=c.video_id WHERE c.ctr_percent > 0 GROUP BY c.video_id ORDER BY 4 DESC LIMIT 10")]'

# intel.db staleness (7-day threshold)
python -c 'import sqlite3; con=sqlite3.connect(r"file:D:/History vs Hype/tools/intel/intel.db?mode=ro", uri=True); print(con.execute("SELECT * FROM kb_meta").fetchone())'

# List tables in any of the three DBs (swap the path)
python -c 'import sqlite3; con=sqlite3.connect(r"file:D:/History vs Hype/tools/discovery/keywords.db?mode=ro", uri=True); [print(r[0]) for r in con.execute("SELECT name FROM sqlite_master WHERE type IN (\"table\",\"view\") ORDER BY name")]'
```

Full per-table row counts, column notes, and the writer/reader ownership matrix:
[SCHEMAS.md](SCHEMAS.md) — read it before writing to any table or claiming a table is unused.

## What the principal would not let slip

1. Citing analytics.db for CTR (it's NULL there) or keywords.db `traffic_sources` for traffic (dead copy).
2. Deleting `surface_ctr` / `thumbnail_features` because "no code references them".
3. Comparing a PERCENT retention column against a FRACTION one.
4. Editing SWAP-LEDGER.md, youtube-intelligence.md, or anything inside an AUTO fence by hand.
5. Treating a 999 freshness sentinel as "36+ hours stale" without checking whether the DB is simply locked/missing.
6. Taking any `video_performance` row without filtering to latest `fetched_at` per video.
7. Proposing store consolidation without reading ADR-0004 first.

## Related skills

- **codebase-atlas** — when you need the module/seam that OWNS a store (AnalyticsStore, KeywordStore, KBStore call sites) or general code navigation.
- **debugging-playbook** — when data is stale/missing and you need the diagnostic path (which log, which timestamp, which known failure mode).
- **automation-ops** — when the question is the scheduled tasks themselves (registration, wrappers, last-run result codes) or OAuth/MCP recovery.
- **extending-safely** — before adding a table, a writer, or a new derived doc; route through the existing seams.
- **validation-standards** — when verifying a change against real data (DB-pin pattern, what "verified" means here).
- **production-map** — when interpreting these numbers for channel decisions (n<30 noise, distribution-not-aggregates).
