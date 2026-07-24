# VideoProjectRepo: a read-only resolver over the lifecycle folders

**Date:** 2026-06-25
**Status:** accepted

Peer to ADR-0004 (analytics.db vs keywords.db) and ADR-0005 (post-publish seam). This ADR exists because the video-project folders are the channel's fourth canonical data surface — but unlike the SQLite stores and the post-publish corpus, "where do projects live and what phase is each one" had no module-level seam. It was re-derived in ~27 places. A `/improve-codebase-architecture` pass (2026-06-25) surfaced it as the highest-leverage deepening; this ADR records the scoping decisions so future runs don't re-litigate them.

## What the seam is

`tools/video_projects/` — a peer package alongside `tools/youtube_analytics/`, `tools/discovery/`, and `tools/post_publish/`.

- **`VideoProjectRepo`** owns discovery and path resolution across the three *live* lifecycle stages: `all()`, `in_stage(stage)`, `by_slug(slug, stage=None)`. REPO_ROOT-anchored (ends the cwd-relative vs `PROJECT_ROOT` split between callers).
- **`VideoProject`** is the resolved unit: cheap identity (`slug`, `path`, `stage`) plus lazy `files`, `phase`, `topic_slug`. `phase` reuses `project_scanner.detect_phase` (its one home) — the rule is not re-implemented.
- **`Stage`** tokens map to the canonical layout. `_BACKLOG/` and `_ARCHIVED/old-*` are deliberately absent — they are outside the lifecycle (see CONTEXT.md "Lifecycle stage").
- **Error contract:** `by_slug` returns `None` on no match and raises `AmbiguousSlugError` on multiple — mirroring the reconcile "ask once if ambiguous" rule rather than silently picking one.

See CONTEXT.md "Lifecycle stage" / "Phase" for the domain definitions of stage vs phase.

## Decision 1 — read-only

The resolver does **not** move folders between stages. The folder-move machinery — `shutil.move` + `.pre-diff` backups + the reversible diff log + `--undo` — stays in `tools/reconcile/`. Reconcile asks the resolver for source/dest paths but keeps owning the mutation.

*Why.* Reconcile's move path is the most dangerous code touching these folders and already has its tested home. Pulling it through a new seam would buy nothing and risk the one operation that can lose work. Discovery (the part that was actually duplicated 27×) and mutation (which was never duplicated — it lives once, in reconcile) are different concerns; only the duplicated one needs a seam.

## Decision 2 — rich, but lazy

`VideoProject` exposes content (`.script`, `.post_publish`) by **composing the existing typed readers** (`production.ScriptParser`, `post_publish.PostPublishStore`) on first access, with imports kept function-local to avoid an import cycle. Identity stays cheap; parse cost is paid only when contents are read. `.status` / `.research` currently expose resolved paths only — they await their own typed readers (the "markdown-artifact reader" candidate from the same review), which will slot in behind the same lazy properties.

*Why not lean identity-only.* A single object answering "where is this project / what phase / what's in its artifacts" is the natural entry point for the ~16 callers that need both. Laziness keeps that breadth from costing the discovery-only callers anything.

## Migration — staged, not big-bang

Following the ADR-0004 / ADR-0005 precedent (`AnalyticsStore`, `PostPublishStore` were migrated incrementally with transitional shims), the ~27 call sites move opportunistically. First cohort (2026-06-25), cleanest read-side sites:

- `tools/hooks/session_context.py` — was cwd-relative `glob`; output is byte-identical post-migration.
- `tools/topic_pipeline.py:get_existing_projects` — was scanning `_ARCHIVED/` at the wrong depth (picked up the literal `published` folder and abandoned `old-*` drafts while **missing** the real published slugs one level deeper). Now correct via `repo.all()`.
- `tools/retitle_gen.py:get_opening_text` — hardcoded `_IN_PRODUCTION/<slug>`, which never existed for the published videos retitle targets, so it silently fell through. Now `repo.by_slug` resolves across all stages.

Second cohort (2026-06-25), the remaining genuine folder-discovery sites:

- `tools/discovery/recommender.py:get_existing_topics` — had its own copy of the number/year-strip slug parser AND the buggy `_ARCHIVED/` top-level scan; collapsed to `[p.topic_slug for p in repo.all()]` (now includes real published topics it previously missed).
- `tools/youtube_analytics/analyze.py:find_project_folder` — globbed `_ARCHIVED/*`, which never descended into `_ARCHIVED/published/<slug>`, so published videos' folders were never found; `repo.all()` fixes it.
- `tools/discovery/news_hook_monitor.py`, `tools/routines/competitor_drop_scan.py`, `tools/routines/modern_relevance_scan.py` — `_IN_PRODUCTION` scanners → `repo.in_stage(IN_PRODUCTION)`.
- `tools/script_checkers/voice/corpus_builder.py:find_video_pairs` — `_IN_PRODUCTION`+`_READY_TO_FILM` scan → `repo.in_stage(...)`.
- `tools/refresh-research-graph.py` — published-research bundler → `repo.in_stage(PUBLISHED)` (recursive per-project glob kept for the nested `_research/` case).

Three more latent bugs fixed incidentally (recommender's missed published topics, find_project_folder's unreachable published folders) — again, the duplication was carrying defects, not just noise. All migrations verified behavior-preserving against the live tree; 50 tests pass.

## Considered alternatives

- **Full lifecycle aggregate** (`VideoProject.move_to(stage)` owns the move). Rejected — Decision 1. Revisit only if a second, independent mover of these folders appears; today reconcile is the only one.
- **Lean identity-only** (no content readers). Rejected — Decision 2. The breadth is cheap given laziness and matches the caller population.
- **Move `detect_phase` into `video_projects`** (leave a shim in `project_scanner`). Deferred. `detect_phase` already has exactly one home and one extra importer (reconcile); reuse-by-import is lower-churn than relocating it now. Invert later if `project_scanner` itself migrates.
- **Migrate `post_publish` discovery in the first cohort.** Deferred. `post_publish/store.py` discovery roots are owned by ADR-0005, and the `VideoProject.post_publish` reader already composes `PostPublishStore` — migrating store discovery to the repo would invert that and risks an import cycle. Do it in a later stage with the cycle broken explicitly, or leave it under ADR-0005.

## Known friction (not blockers)

- **The genuine folder-discovery sites are now all migrated** (two cohorts, 2026-06-25). The remaining `_IN_PRODUCTION` / `_READY_TO_FILM` / `_ARCHIVED` grep hits are not discovery: docstring/usage examples (`prompt_generator`, `synthesis_engine`, `parser`, `vidiq_workflow`, `thumbnail_checker`, `nlm_ingest`), within-a-given-project globs that receive the project path as input (`preflight/scorer`, `preflight/thumbnail_checker`), and the deferred owners below. Leave the examples; migrate a within-project glob only if it starts discovering folders.
- **Deferred owners (intentional):** `reconcile.py` (owns the folder *moves* — Decision 1), `post_publish/store.py` (ADR-0005 owns its discovery roots), `dashboard/project_scanner.py` (defines `detect_phase`, which the repo reuses — migrating it would be circular).
- **`post_publish/store.py:140`** still globs `_ARCHIVED/*/POST-PUBLISH-ANALYSIS.md` — the wrong depth (real reports are at `_ARCHIVED/published/*/...`, line 141). Harmless on the current disk (no `old-*` carries that file) but latent. Fix when post_publish discovery migrates to the repo.
- **`.status` / `.research` are path-only** until their typed readers land.

## Consequences

- **Discoverability.** `from tools.video_projects import VideoProjectRepo` is the canonical entry point for "find projects / resolve a slug / what phase."
- **Test surface.** `tests/test_video_projects.py` (13 tests) — the first direct tests of the phase rule (`detect_phase` / `scan_projects` had none) plus stage canonicalization, `_ARCHIVED/old-*` + `_BACKLOG` exclusion, and `by_slug` resolution.
- **Re-litigation guard.** Future `/improve-codebase-architecture` runs that surface "make VideoProject own folder moves" or "drop the lazy content readers" should be answered with this ADR. If friction grows beyond the items above, supersede rather than silently restructure.
