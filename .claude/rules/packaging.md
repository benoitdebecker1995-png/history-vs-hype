---
paths:
  - "**/YOUTUBE-METADATA.md"
  - "**/THUMBNAIL-*.md"
  - "channel-data/serp-studies/**"
  - "tools/title_scorer.py"
  - "tools/PACKAGING_MANDATE.md"
---

# Packaging

Loaded only when packaging files are open. Moved out of CLAUDE.md 2026-07-31 — rules unchanged.

1. **Search demand** — graded gate, NOT a hard stop: GO ≥1,000/mo · CAUTION 500–999 · STOP <500, and a **verified live news hook overrides a STOP**. Authority: `.claude/commands/greenlight.md` Step 1.
   - **Record the decision in `recommendation_ledger` before research starts (ADR-0031)** — the measured volume, the anchor term it was measured on, the band, and what you expect to follow. Only two of 47 published videos can currently be matched to the demand they were greenlit on, so the threshold has never been validated and cannot be until this is kept.
   - ⚠ **Demand predicts SERVING, not CLICKING.** Berlin Conference measured 11,648/mo, was served 9,485 impressions, and converted 3.66%. A passing demand score is a necessary condition, never a forecast of performance (ADR-0029).
2. **Title checks** — `title_scorer.py`, for its **mechanical** parts only: the measured search anchor (`find_search_anchor`, ADR-0023) and the clickbait brand-gate (`detect_clickbait` / `hard_rejects`). Front-load the keyword.
   - ⚠ **The composite 0–100 score is NON-PREDICTIVE. Do not use it to choose a title (ADR-0029).** Measured 2026-08-27 across 47 published titles with ≥1,000 impressions: Spearman **+0.173**, and the four titles it scored **100 average 2.67% CTR** — *below* the 3.05% channel mean. It scored the 7.90% KGB title 67 and the 1.60% Israel/Palestine title 100.
   - **Years and colons are graded penalties, not bans** — `YEAR_PENALTY -15`, `COLON_PENALTY -10`, `COLON_PENALTY_VERSUS 0` (`tools/title_scorer.py:308-313`, authoritative). The old −46%/−28% "hard rule" was topic-confounded and is **retired**; the channel's #1 and #3 videos both use colons. These penalties feed the composite, so they inherit its non-predictiveness — treat them as style preferences, not evidence.
   - **There is currently no validated title-selection instrument.** The working hypothesis (actor + act + stake) is in `channel-data/PACKAGING-DIAGNOSIS-2026-08-26.md` and is **untested** — drawn from the same 47 rows. It can only be tested prospectively, on new uploads (ADR-0030): back-catalogue retitle tests are retired because the candidates receive 29–149 impressions a month and would need ~750 per arm.
3. **Thumbnail concept** — text overlay MANDATORY (87% niche), no face (0% niche), maps for territorial. `thumbnail_checker.py`
4. **THEN research** — only after `/greenlight` passes

**Text overlay on thumbnails** — 2-4 words, not the full title. Maps for territorial topics.

**Filters decide, scores inform (ADR-0012).** A rule that must bind is a filter in
`tools/preflight/packaging_lock.py` — code, not prose in a command file. Enrichment can never
upgrade a filter FAIL.

**Validate or label (ADR-0029).** Any tool producing a number a human uses to decide is either
checked against real outcomes, or it carries a non-predictive label. `title_scorer`'s composite went
a year unchecked and was steering title choices the wrong way. An unvalidated number in a guidance
document is worse than no number, because it displaces judgement. Before trusting any scoring output
here, ask when it was last correlated against `channel-data/analytics-exports/Table data.csv`.

**Collision-check before proposing a video:** `python -m tools.preflight.candidate_preflight "<topic>"`.
A published match is a stop. Run it *before* the pitch, not after.

See: `tools/PACKAGING_MANDATE.md` | `.claude/REFERENCE/TITLE-GENERATION-PROTOCOL.md`
