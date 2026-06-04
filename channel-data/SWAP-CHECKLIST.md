# SWAP CHECKLIST — 2026-06-03

**Generated:** 2026-06-03 | **Batch size:** 1 (targeted) | **Measure at:** 2026-06-10

> **Instructions:** Open this file in one window, YouTube Studio in another.
> Change the title on swap day for a clean 7-day comparison window.
> Targeted single-video run (not the standard top-5 audit) — surfaced from the
> analytics refresh as the channel's clearest packaging-trapped win.

---

## Video 1: Putin / NATO Promise

**Video ID:** `499YLd1BHZ4`
**Studio link:** https://studio.youtube.com/video/499YLd1BHZ4/edit
**Diagnosis:** LOW_IMPRESSIONS + low CTR. 48.3% retention (well above channel avg) trapped behind a 2.47% CTR title. Pure packaging failure — the content holds viewers; the title doesn't earn the click or signal topic relevance for impressions.

### OLD TITLE (copy to revert)
Putin Says NATO Promised Not to Expand. The Documents Disagree.

### NEW TITLE
Putin's NATO Promise Never Existed. 1,000 Documents Prove It
*(score 77/100, grade B, pattern: declarative — +15 over current)*

### Title Source
RETITLE-RECOMMENDATIONS via CATALOG-OPTIMIZATION-PLAN.md, re-scored this run, then **verified against the actual video transcript** (pulled 2026-06-03, saved at `channel-data/analyses/TRANSCRIPT-499YLd1BHZ4.txt`). No project-folder script exists for this video.

### All Scored Candidates
| Score | Grade | Title |
|-------|-------|-------|
| 77 | B | Putin's NATO Promise Never Existed. 1,000 Documents Prove It |
| 72 | B | NATO Never Promised Russia Anything. The Documents Prove It |
| 67 | C | Putin Lied About a NATO Promise. 1,000 Documents Exposed Him |
| 67 | C | NATO Never Promised Not to Expand. 1,000 Documents Prove It |
| 62 | D | *(CURRENT)* Putin Says NATO Promised Not to Expand. The Documents Disagree. |
| 57 | F | Putin Says NATO Broke a Promise. 1,000 Documents Say Otherwise |
| 57 | D | The NATO Promise Putin Keeps Citing Never Existed |
| 52 | D | NATO Promised Not to Expand. 1,000 Declassified Documents Disagree |

**Accuracy note (transcript-verified):** The title is well-grounded. The video's actual thesis is that Baker's "not one inch eastward" (Feb 9 1990, German Federal Archives) referred *only* to East German territory during reunification — NOT to Poland/Ukraine/Eastern Europe — and that Bush soon after told Gorbachev any country may choose its own path. So the broad "NATO promised not to expand" pledge Putin cites never existed. "Never Existed" matches the video's argument exactly. Runner-up (72/B) is the cleaner-attribution alternative if preferred.

### NEW DESCRIPTION (first 3 lines only — replace existing opening)
Did NATO promise Russia it would never expand east? Putin has cited that promise dozens of times to justify the war in Ukraine. The declassified record says it never existed.
Yale historian M.E. Sarotte had 1,000+ documents declassified from six national archives — and Baker's actual 1990 words ("not one inch eastward") were about East German territory, not Eastern Europe. Bush then told Gorbachev any country could choose its own path.
Evidence-based, straight from the declassified diplomatic record — not talking points.

### THUMBNAIL
**Status:** MANUAL CHECK REQUIRED — no project folder / YOUTUBE-METADATA.md for this video.
**Type:** document-on-map (declassified document is the central evidence; NATO-eastward map as backdrop)
**Concept:** Map of Europe with NATO expansion shading pushing east toward Russia; a "DECLASSIFIED"-stamped document overlaid in the foreground. Optional 2-word overlay: "NO PROMISE". No face.
**Color scheme:** NATO-blue west, cold grey/red Russia east, red stamp/overlay on the document.
**Checker result:** Not run (no project metadata). Verify against thumbnail_checker before swap if a thumbnail change is made.

### PRE-SWAP METRICS (for comparison at 7-day check)
- CTR: 2.47% | Impressions: 1,214 | Retention: 48.3% | Views: 46–51 | Subs: +3 (6.52%/100 views)
- Source: ctr_snapshots (4 snapshots, 2026-02-23); analytics.db has no API CTR for this video.

---

## Post-Swap Checklist

- [ ] Title changed in YouTube Studio
- [ ] Description first 3 lines updated (after SRT confirmation)
- [ ] Thumbnail reviewed (swap optional — title-first test is cleaner for isolating CTR delta)
- [ ] SWAP LOG added to POST-PUBLISH-ANALYSIS-499YLd1BHZ4.md (tell me "swaps executed" and I'll inject it)
- [ ] Calendar reminder: **2026-06-10** — run `/retitle --check 499YLd1BHZ4`

### SWAP LOG Entry Template (paste into POST-PUBLISH-ANALYSIS-499YLd1BHZ4.md)

```
## SWAP LOG

| Date | Type | Old Value | New Value | Pre-CTR | Post-CTR | Result |
|------|------|-----------|-----------|---------|---------|--------|
| 2026-06-03 | title | "Putin Says NATO Promised Not to Expand. The Documents Disagree." | "Putin's NATO Promise Never Existed. 1,000 Documents Prove It" | 2.47% | TBD | pending |
```
