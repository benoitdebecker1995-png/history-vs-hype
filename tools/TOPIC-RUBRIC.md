# TOPIC RUBRIC v2 — Small-Channel Topic Selection (Fable Phase 4)

**Effective:** 2026-06-11 | **Supersedes:** memory `feedback-small-channel-rubric.md` v1 (40/20/20/10/5/5, 2026-05-08)
**Authority:** Phase 1 breakout forensics (`tools/PACKAGING_MANDATE.md` funnel model, D1 dossier) + D4 whitespace scan (`channel-data/fable-digests/D4-competitor-topic-map.md`) + v1's documented-source methodology (VidIQ published scoring, Backlinko/TubeBuddy small-channel guidance)
**Scope:** FRESH topic selection at sub-1K subs. NOT for series commitments, parked-package revivals already decided, or follow-ups to a specific recent video — those are editorial pipeline decisions (see "When NOT to apply").

---

## What changed from v1, and why

Phase 1 forensics showed the v1 rubric scores the wrong gate. v1 was pure evergreen-search logic (VidIQ 40% + title CTR 20%). But the catalog's binding constraint is **Gate 1: does YouTube test you at all** — and what got videos tested was a *live contemporary hook* plus a searched head term, not keyword volume alone. The A-grade 2025 evergreen cohort (China/Taiwan 100, Kashmir 100, Cyprus 90) never cleared 5.5K lifetime impressions; all 4 breakouts had an active dispute/ruling/public claim at publish. v1 had **no topicality dimension at all**.

Second gap: v1's "Top-3 saturation" (20%) asked *is the topic covered* — binary. D4 shows the real question is **can this channel say something the shelf doesn't serve**: the niche over-serves narrative/moral/debunk framing broadly, while the primary-document/legal/administrative forensic angle is chronically open. Coverage ≠ angle coverage.

v2 therefore: adds gates (identity, demand floor), adds topicality (20%), upgrades saturation → whitespace (25%) with angle-level anchors, trims VidIQ to 30% and title-format CTR to 10% (construction explains little Gate-1 variance; it's a Gate-2 execution variable enforced at title lock by V4 anyway).

**Weights are policy, not data** (same epistemic status as the 65-point title threshold). The *dimensions* are evidence-ranked; the exact percentages are judgment. Re-tier after the BREAKOUT-HYPOTHESES review trigger (upload 5).

---

## GATES (pass/fail BEFORE scoring — a fail ends the candidacy)

**G0 — Identity (overrides everything, incl. demand).** Method-first channel-DNA test: can this be told primary-documents-on-screen, and does it matter in 10 years regardless of who's in power? No regional positioning, no stakes-first geopolitics framing (RealLifeLore lane = anti-voice). Per the 2026-06-11 identity guard in `PACKAGING_MANDATE.md`.

**G1 — Demand floor (= mandate V1, VALIDATED tier).** VidIQ search volume >500/mo **or** a verifiable live news hook (active dispute, ruling, public claim by a notable figure). Hook claims must be **web-verified for date and content** before counting (per cultural-moment-verification — don't trust prior briefs).

---

## COMPOSITE (0–100, weighted)

| Weight | Dimension | Scoring | Source / tool | Evidence tier |
|---|---|---|---|---|
| **30%** | VidIQ Overall Keyword Score (0–100) | Direct | `vidiq_keyword_research(keyword, mode="research")` MCP → `overallScore` (or the in-app keyword prefix number). Never hand-build vol×comp transforms. | VALIDATED methodology (VidIQ published composite) |
| **20%** | Topicality / live-hook strength | Verified active hook (dispute/ruling/claim live NOW) = 100 · credible dated upcoming event or major anniversary ≤6 mo = 50 · evergreen = 0 | `news_hook_monitor.py` + mandatory web verification of date AND content | All 4 breakouts had one; stall cohort had none (D1, n=57). Formal ≥3x test pending = H1 |
| **25%** | Whitespace (shelf × angle) | Quality English explainer exists AND serves the doc-forensic angle = 0 · shelf exists but primary-doc/legal/admin angle unserved = 50 · no quality English coverage of the topic = 100 | Live SERP scan: `serp_title_study.py --slug X --query "..."` + top-result skim. Live SERP beats static intel corpus (corpus-refresh mechanics). | D4 corpus map + B1 pocket forensics (the one organic breakout was a zero-coverage topic) |
| **10%** | Title CTR format fit | VidIQ Channel CTR score for the natural title format; if untested, cross-batch format average flagged **ESTIMATED** | VidIQ | HEDGE — construction explained little Gate-1 variance (scorer rejected the #1 and #3 videos) |
| **10%** | Small-channel rankability | competition <40 = 100 · 40–50 = 50 · >50 = 0 | VidIQ competition score | Backlinko/TubeBuddy published guidance |
| **5%** | Source verifiability + access | User's languages (FR/ES/DE/Dutch; Latin/Greek verification-only) + PDF/critical-edition availability; check `library/by-topic/` | Manual | Channel competitive advantage |

### POCKET flag (recorded, NOT scored)

Alongside the composite, check every candidate symmetrically against the H3 demand-pocket checklist: (a) real English-speaking national/diaspora audience, (b) near-zero quality English SERP coverage, (c) active dispute/news cycle. Flag `POCKET: YES/NO`. It stays out of the composite because H3 is an unconfirmed hypothesis (pre-registered in `BREAKOUT-HYPOTHESES.md`); a YES makes the candidate eligible for the dedicated pocket-raid upload slot. Pockets are **raids — one per region, method-first framing** — never repositioning.

---

## Hard application rules (carried from v1, all still binding)

1. **Tool-role separation.** VidIQ = keyword/search/title data only. Gemini/web = competitor scans, saturation, hook verification only. Manual = source/access/language. Mixing tools inside one criterion is the failure mode.
2. **No hand-built transforms.** VidIQ already publishes the composite. Inventing reach tables = fabrication.
3. **Symmetric data.** Every dimension queried for ALL candidates or dropped. One-candidate bonus checks rig the race.
4. **Tie-break:** top two within 10 points → collect the missing data (VidIQ batch, SERP scan, hook verification) before locking. Never manually override the math.
5. **No advocacy.** Once weights are locked, the composite IS the answer. To raise a score, find legitimate missing data.
6. **ESTIMATED values:** flag explicitly; run the underlying VidIQ batch before any lock that depends on one.

## Verification of correct application

- The rubric should occasionally pick a topic the user did NOT initially favor.
- Two independent runs on the same data produce the same ranking.
- Whitespace scores cite the actual SERP scan file (`channel-data/serp-studies/titles/<slug>-<date>.md`), not an impression.
- Topicality 100s cite a verified, dated source.

## When NOT to apply

Series commitments (e.g. the I/P "Claims on Trial" series), parked packages already being revived for cause, direct follow-ups to a recent video. Those live in the editorial pipeline. The rubric is for FRESH selection. (But a backlog folder does not exempt a topic — backlog candidates compete through the rubric like everyone else; banked research just lowers their cost, it doesn't raise their score.)

---

*Wired into `/greenlight` (Step 1b) and `channel-data/TOPIC-PIPELINE.md` ranking. Re-tier weights after the BREAKOUT-HYPOTHESES upload-5 review.*
