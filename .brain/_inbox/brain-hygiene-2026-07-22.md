# Brain Hygiene — 2026-07-22

## Queue ingested

0 items — `.brain/_queue/` was empty. No Gemini dispatch needed.

## Lint findings

None (0 total).

- **Dead links:** 0 — no URLs present anywhere in `.brain/**/*.md`, so the 5-link spot-check had nothing to sample.
- **Orphan pages:** 0 — `.brain/sources/` and `.brain/threads/` are both still empty.
- **Stale `[UNVERIFIED]` claims (>90d):** 0 — the 8 grep hits are prior hygiene reports naming the lint category, not real claims.
- **Open contradictions:** unverifiable, not zero. `~/llm-brain/wiki/contradictions/` sits outside this session's allowed working directories (`D:\History vs Hype`, `D:\tmp`); `ls`, `Test-Path`, and Glob were all refused. Carried forward as "skipped", same as prior runs.

## Index changes

`.brain/index.md` — AUTO sections only (§1/§2/§3 untouched):

- **§4 Recently Added / Changed:** placeholder ("no brain-root files in the last 14 days") replaced with two real entries — `channel-data/calibration/CALIBRATION-CORPUS.md` and `channel-data/calibration/VOICE-DRIFT-CROSS-SCRIPT-2026-07-21.md`, both modified today 07:50–07:51. Nothing to prune (window was empty).
- **§5 Health Signals:** LAST LINT stamped 2026-07-22 07:53. All counts unchanged from 2026-07-21.
- **§6 Cross-Root Links:** no change. The five `_IN_PRODUCTION` projects (36, 60, 61, 62, 63) match the list already recorded, and a grep of every `01-VERIFIED-RESEARCH.md` found zero `~/llm-brain/` references. No project left `_IN_PRODUCTION` since the last run, so nothing to archive.
- Header date bumped 2026-07-21 → 2026-07-22.

## Flag for the owner (not a brain-lint finding)

The 07:51 run log (`brain-hygiene-run-2026-07-22.log`) carries two permission warnings from `.claude/settings.local.json`:

```
Write(.brain/**) is not matched by file permission checks — only Edit(path) rules are.
Write(//d/History vs Hype/.brain/**) is not matched by file permission checks.
```

Both allow-rules are inert as written. `Edit(...)` rules cover all file-editing tools including Write; `Write(...)` rules do not. Left unfixed, a headless Routine 5 run that needs to *create* a file (a new `sources/` page from a queue item, or this report) can stall on an unattended permission prompt. Fix is a one-line rename of each rule from `Write(` to `Edit(`. Not applied here — `settings.local.json` is outside this routine's write scope (`.brain/` only).
