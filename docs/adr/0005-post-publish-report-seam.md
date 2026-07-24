# PostPublishStore: seam over POST-PUBLISH-ANALYSIS.md

**Date:** 2026-05-19
**Status:** accepted

Peer to ADR-0004 (analytics.db vs keywords.db split). This ADR exists because the post-publish report is the channel's third canonical data source — alongside `analytics.db` and `keywords.db` — but unlike the two SQLite stores, the markdown corpus had no module-level seam. Future `/improve-codebase-architecture` runs that surface "consolidate the duplicate parsers" or "merge the post-publish reader into youtube_analytics" should be answered with this ADR.

## What the seam is

`tools/post_publish/` — a peer package alongside `tools/youtube_analytics/` and `tools/discovery/`, structured to mirror the two existing SQLite-store packages.

- **`PostPublishStore`** owns discovery and parsing of `POST-PUBLISH-ANALYSIS.md` files. Discovery roots are the four canonical paths: `channel-data/analyses/POST-PUBLISH-ANALYSIS-*.md` plus `video-projects/{_IN_PRODUCTION,_READY_TO_FILM,_ARCHIVED}/*/POST-PUBLISH-ANALYSIS.md`.
- **`PostPublishReport`** is a frozen dataclass — the typed return shape. 14 fields covering header metrics, body sections (observations, actionable, drop_points, discovery), and source-path provenance. Body sections default to empty lists / `None` when the report doesn't contain them yet.
- **Error contract:** `PostPublishStore.load(path)` raises `PostPublishMalformedError` (no video_id) or `PostPublishMissingError` (unreadable file). `PostPublishStore.discover_and_load_all()` is a lenient bulk iterator that logs and skips both — preserving the silent-skip behaviour that consumers like `news_hook_monitor` and the dashboard depend on.

See CONTEXT.md "Post-publish report" for the domain definition of the artifact itself.

## Why a new package, not inside youtube_analytics/ or discovery/

Three packages had a plausible claim:

- `tools/youtube_analytics/` — where `AnalyticsStore` lives. Post-publish reports describe analytics-side metrics.
- `tools/discovery/` — where `KeywordStore` lives. Discovery scripts (`news_hook_monitor`, `performance_tracker`, `backfill_high_impact`) are heavy consumers.
- `tools/production/` — these files are written by `/publish`, an output of the production loop.

The other two stores live in the package that **owns** the data (`AnalyticsStore` reads what `youtube_analytics/backfill.py` writes; `KeywordStore` reads what `discovery/` modules write). Post-publish reports are different — their producer (the `/publish` workflow under `tools/production/`) and their consumers (analytics + discovery + dashboard + reconcile) are different packages. A neutral peer is the only honest placement.

## Field-shape contract

Retention values are stored as **percents** (e.g. `avg_retention_pct = 28.1`), matching the source markdown directly. The prior `patterns.py` parser silently stored `avg_retention` as a fraction (`0.281`); the prior `feedback_parser.py` parser stored it as a percent. Same field name, different units. The new dataclass exposes both forms — `.avg_retention_pct` and `.avg_retention_fraction` — so callers migrating from either old parser can pick the form they already use.

CTR is similarly a percent. The field is `ctr_percent`; a `.ctr` property exposes the legacy `feedback_parser` name.

## Considered alternatives

- **Lazy / on-demand body parsing.** Rejected. The files are small (a few KB) and the corpus is ~50 reports. The complexity cost of lazy properties or a two-method API (`load_summary` vs `load_full`) doesn't pay back. Eager all-fields with empty-list defaults matches what both old parsers were already doing implicitly.
- **Return `None` or `{'error': ...}` on parse failure instead of raising.** Rejected for the seam itself — the dashboard, backfill, and one-off scripts need different reactions to "missing file" vs "malformed file," and a return-shape contract can't carry that distinction cleanly. The lenient `discover_and_load_all()` helper restores the silent-skip behavior for callers that prefer it.
- **Consolidate into the existing `feedback_parser.py`** (don't create a new package). Rejected. `feedback_parser.py` was *meant* to be the consolidation point; `patterns.py` re-implemented `parse_analysis_file` instead of importing it, and the two diverged in field names and units. The shape of the problem was that there was no proper seam, so consumers kept rolling their own. A new package with a typed contract is the only fix that prevents recurrence.
- **Skip `tools/post_publish/` and put the store inside `tools/production/`.** Rejected. Consumers vastly outnumber producers (1 writer, ~16 readers), so co-locating with consumers is closer to the truth — but no single consumer package owns more than a fraction of them. Neutral peer wins.

## Known friction (not blockers, but worth recording)

- ~~**Per-file dict shims still exist** in `patterns.py` (`_report_to_patterns_dict`) and `feedback_parser.py` (`_report_to_feedback_dict`). … **Action deferred** until friction motivates it.~~ **Resolved 2026-07-01** (architecture pass, candidate 4). Consumer tracing showed the percent dialect's numeric fields (`avg_retention`, `ctr`) had **zero live readers** — `analyze.py` and `backfill_all` only consumed the id/list fields. So the divergence was killed by deleting one dialect, not migrating both: `_report_to_feedback_dict` + `feedback_parser.parse_analysis_file` **deleted**, their three consumers (`analyze.py` auto-store, `backfill_all`, the single-file CLI) read `PostPublishReport` attributes directly. `patterns.parse_analysis_file` (fraction dialect, zero callers) **deleted**. `_report_to_patterns_dict` **kept, demoted to module-internal working format**: patterns.py's own aggregate dicts reuse the same key names (`stats['avg_retention']` as fraction), so converting ~60 read sites to attribute access in a 1,955-line untested module would mix two access styles under identical names — more unit-bug risk than the module-private dict it removes. With only one dialect left, confined to one module and documented at its constructor, there is no cross-module divergence to guard. Full internalization can ride a future patterns.py overhaul.
- **Section-level retention parsing** lives outside the store. `backfill_high_impact.py:extract_retention_sections` parses time-coded segments (`| 0:00-1:30 | Hook | 45% | ...`) that the markdown sometimes carries but `PostPublishReport` doesn't expose. Similarly `ctr_by_source_analysis.py:_extract_ctr_from_content` catches a "CTR Trend: X% -> Y%" pattern not in the store. Both kept local to avoid widening `PostPublishReport`'s surface until a second consumer needs the field.
- **The unit-mismatch history** (`avg_retention` as fraction in one parser, percent in the other) was a silent data-shape bug that lived for an unknown duration. Caught only during the consolidation pass. Documented here so future readers don't recreate it.

## Consequences

- **Discoverability.** New callers reading or writing post-publish data have a single typed entry point. `from tools.post_publish import PostPublishStore` is the canonical import.
- **Test surface.** The seam has a real test suite (`tests/test_post_publish_store.py`, 12 tests). Before this ADR, the post-publish parsing logic had zero direct tests — coverage was implicit through `backfill_all`'s integration runs.
- **Coverage expansion.** Two of the migrated callers (`backfill_high_impact.py`, `ctr_by_source_analysis.py`) previously globbed only a subset of the four canonical roots. After migration they cover all four — strictly more complete, no behavioural regression.
- **Re-litigation guard.** Future `/improve-codebase-architecture` runs that surface "merge post-publish parsing into youtube_analytics" or "make the dataclass lazy" should be answered with this ADR. If the friction grows beyond the items above, supersede this ADR rather than silently restructuring.
