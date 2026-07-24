# Brain Hygiene — 2026-06-27

_Two runs today: 17:48 (morning analytics artifacts) and 22:56 (scheduled nightly). Consolidated below._

## Queue ingested
None — `.brain/_queue/` empty on both runs.

## Lint findings
None (clean on both runs).
- Stale `[UNVERIFIED]` (>90d): 0 (only hits are prior reports referencing the lint category, not real claims)
- Orphan pages: 0 (`sources/` + `threads/` empty)
- Dead links: 0 (no URLs present in `.brain/**/*.md`)
- Open contradictions: 0 (`wiki/contradictions/` absent — skipped)

## Index changes

### Run 1 — 17:48
- **§2** — added 2 rows: per-video retention curves (n=57); why long-form underperforms (holdout-tested).
- **§4** — prepended 4 bullets: `CHANNEL-PERFORMANCE-DATA-2026-06`, `LONGFORM-FAILURE-DIAGNOSIS-2026-06`, `FLOP-AUTOPSY-PLAN-2026-06`, `OPENER-RETENTION-DIAGNOSIS` (2026-06-26).
- **§5** — timestamp → 17:48; added explicit dead-links=0 line.
- **§6** — no change.

### Run 2 — 22:56 (this run)
Four more analytics artifacts were written today **after** the 17:48 run and were not yet recorded:
- **§2 Knowledge-by-Question** — added 2 rows:
  - CTR title + thumbnail formula (derived, my data, n=56) → `channel-data/CTR-TITLE-FORMULA-2026-06.md`, `channel-data/CTR-THUMBNAIL-FINDINGS-2026-06.md`
  - Causal A/B + traffic-source CTR split, per-video funnel autopsy → `channel-data/AB-TEST-AND-TRAFFIC-CTR-2026-06.md`, `channel-data/FLOP-AUTOPSY-TABLE.md`
- **§4 Recently Added / Changed** — prepended 4 bullets:
  - `channel-data/CTR-TITLE-FORMULA-2026-06.md`
  - `channel-data/CTR-THUMBNAIL-FINDINGS-2026-06.md`
  - `channel-data/AB-TEST-AND-TRAFFIC-CTR-2026-06.md`
  - `channel-data/FLOP-AUTOPSY-TABLE.md`
  - No pruning: oldest existing bullets (2026-06-13) are exactly 14 days old, still inside the window.
- **§5 Health Signals** — timestamp → 2026-06-27 22:56; all counts still 0.
- **§6 Cross-Root Links** — no change. Re-verified all 4 in-production `01-VERIFIED-RESEARCH.md` (36, 59, 60, 61) still carry zero `~/llm-brain/` references; active-project set unchanged.

All writes confined to `.brain/`. No git push, no project files touched.
