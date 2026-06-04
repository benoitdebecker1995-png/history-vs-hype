# Synthetic E2E Test Report — Migration Validation

**Date:** 2026-05-17
**Project tested:** `45-manhattan-purchase-myth-2026` (The Lenape Never Sold Manhattan)
**Video ID:** mg6ujk6rDVE (published 2026-05-08)
**Test type:** Structural validation (full re-execution blocked on NotebookLM manual step)

---

## Results

| Check | Result | Detail |
|---|---|---|
| Gate 1 — ≥90% claims ✅ | ✅ PASS | 56/56 verified (100%) |
| Gate 2 — APPROVED | ✅ PASS | `03-FACT-CHECK-VERIFICATION.md` verdict: APPROVED |
| Required files present | ✅ PASS | SCRIPT.md, 03-FACT-CHECK, YOUTUBE-METADATA, PROJECT-STATUS, _research/01-VERIFIED-RESEARCH all exist |
| Folder lifecycle | ✅ PASS | `_IN_PRODUCTION` = false, `_ARCHIVED/published` = true |
| analytics.db match | ✅ PASS | `mg6ujk6rDVE` present, published_at 2026-05-08 |
| Word budget (Rule 10) | ⚠️ DEVIATION | 4,262 words vs 1,980 cap (10-min Format A/B). Pre-Rule-10 project (rule added in script-writer-v2 v15.0, 2026-05-09 — after this video shipped). Expected for legacy projects. |
| AUTO-block format | ⚠️ MINOR DRIFT | Opening tag is `<!-- AUTO:reconcile — do not edit manually... -->` (long-form), not the canonical `<!-- AUTO:reconcile -->`. Content is correct; string-match logic in new agents should handle the long-form variant. |

---

## Verdict: STRUCTURAL VALIDATION PASSED

The pipeline file structure, quality gates, folder lifecycle, and analytics.db registration all match expected state. The two deviations are known legacy issues, not migration-introduced regressions.

## Action Items
1. Update Analytics agent's reconcile logic to handle both `<!-- AUTO:reconcile -->` and `<!-- AUTO:reconcile — do not edit... -->` opening-tag variants.
2. New projects post-migration will enforce Rule 10 word budget via structure-checker-v2 Constraint BD (Format A/B WARNING). No backfill needed for legacy projects.

## What a Full Re-Run Would Require
- User uploads source list to NotebookLM (Stage 2, manual)
- User runs NLM prompts and pastes output (Stage 2, manual)
- Structure-checker-v2 B–BD audit on script (automated, runs in Stage 3)
- These steps are not skippable — they are the editorial advantage, not overhead

---

**Tested by:** Antigravity Analytics Agent (Sonnet 4.6) / migrated from Claude Code
