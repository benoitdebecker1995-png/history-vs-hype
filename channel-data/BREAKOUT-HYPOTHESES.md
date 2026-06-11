# BREAKOUT HYPOTHESES — Next 5 Uploads

**Built:** 2026-06-10 (Fable Phase 1) | **Input:** D1 breakout dossier + D4 whitespace scan
**Status:** ACTIVE — each upload should consciously run one of these as its A/B test. Update the Outcome column as data lands; a hypothesis is CONFIRMED or KILLED only by its named metric, not by vibes.

**Baselines (for thresholds):** channel median views = 91; recent-upload impression tests = 1.7K–5.2K (fresh ctr_tracker window); channel median CTR = 2.48% (lifetime snapshot); avg-watch median = 28.1%.

---

## The causal story these hypotheses test

Forensics say the 3 breakouts shared: (1) a live contemporary hook at publish, (2) country-name head terms with search volume, (3) bilateral-conflict existential stakes in the title, (4) — for B2 — being a sequel to a proven winner. No current packaging rule captured any of these. Meanwhile the title construction rules (colon/year/pattern) explain almost none of the variance: the scorer REJECTED the #1 and #3 videos and gave 100/A to videos that died at 228 views.

---

## H1 — Topicality gate drives the impression test

**Claim:** Uploads with a verifiable live news hook (active dispute/ruling/public claim) get materially more first-month impressions than evergreen uploads, independent of title construction.
**Evidence for:** All 4 breakouts had one. The A-grade 2025 stall cohort had none and never cleared 5.5K lifetime impressions.
**Test:** Across the next 5 uploads, tag each at publish: HOOK or EVERGREEN (pre-registered in YOUTUBE-METADATA.md, not retro-fitted).
**Confirm:** median first-28-day impressions of HOOK uploads ≥3x EVERGREEN uploads.
**Kill:** HOOK ≤1.5x EVERGREEN.
**Action if confirmed:** V1 demand gate tightens — evergreen topics need >1K/mo search volume to compensate for no hook.

## H2 — The Gate-2 CTR target: ≥4% on the test batch

**Claim:** With country-anchored title + SERP-differentiated thumbnail, recent uploads can convert YouTube's test batch at ≥4% (vs the 1.48–3.81% the last three uploads scored), which sustains the push.
**Evidence for:** YouTube tested #56 (5,188 imp), #57 (3,097), hijab (1,759) — all failed <4%. Breakout-adjacent CTRs where measured: 4.31%, 5.41% (lifetime); fresh winners 8–18%.
**Test:** Next 5 uploads, first-28-day CTR on ≥1K impressions (ctr_tracker).
**Confirm:** ≥2 of 5 uploads hit ≥4%.
**Kill:** <2.5% on 2 consecutive uploads despite country-anchored packaging → the problem is upstream (topic selection), revisit H1/H4.

## H3 — Sequel inheritance: feed the proven audience

**Claim:** A follow-up to the channel's one proven franchise (Guatemala–Belize / Essequibo / Latin-American territorial) inherits distribution from the breakout cluster.
**Evidence for:** B2 (ICJ follow-up) did 5,355 views — 59x channel median — published 5 weeks after B1, 69% via the same browse/subscriber channel + 16% related-video. The channel gained 198 subs from B1+B2 and has published ZERO Latin-America territorial videos since 2025-12-04.
**Test:** One of the next 5 uploads = Guatemala-Belize ICJ update or Essequibo development (both disputes remain active; check news_hook_monitor first).
**Confirm:** ≥1,000 views in 28 days (≥10x median).
**Kill:** <300 views in 28 days.
**Note:** This is the highest-expected-value single action available. It tests cheap and fast.

## H4 — Country-stakes framing beats document-forensic framing in titles

**Claim:** Titles that lead with country + existential stakes outperform titles that lead with the document/artifact/myth — even for the same video.
**Evidence for:** Breakouts: "The Country That Might Disappear", "The Oil War Over Essequibo". Stalls: "The Lenape Never Sold Manhattan" (0% CTR on 101 imp), "Treaty of Tripoli:…" (37 views), "Britain Expelled 2,000 Islanders. The Memo Proves It" (29 views). The channel's identity drifted into document-marquee titles; the doc should be the in-video payoff, not the title's subject.
**Test:** Native A/B (3 title+thumbnail combos, uploaded together per standing practice) on ≥2 of the next 5 uploads: at least one country-stakes arm vs one document-forensic arm, same thumbnail family.
**Confirm:** country-stakes arm wins the impressions×CTR composite in ≥2 of 3 tests.
**Kill:** document arm wins ≥2 of 3.

## H5 — Colon reintroduction (retire the hard reject permanently)

**Claim:** "X vs Y: Stakes" colon titles are at worst neutral (the -28% penalty was topic-confounded).
**Evidence for:** #1, #2, #3 videos all have colons; fresh CTRs 8.49% / 12.11% / (4.31% lifetime).
**Test:** One A/B arm on a versus-topic upload uses the colon format. Single-variable: same thumbnail, same head term. Judge on search impressions + CTR composite (per data-overrides-rules-for-testing — not CTR alone).
**Confirm (non-inferiority):** colon arm within 10% of the best arm's composite → colon rule stays HEDGE/neutral forever.
**Kill:** colon arm loses by >25% → restore -25 penalty (still not auto-REJECT).

---

## Pre-registration log

| Upload | Date | Hypotheses carried | Arms | Outcome |
|---|---|---|---|---|
| #58 Kurdistan | (pending) | H2 (CTR ≥4% target), H1-tag: EVERGREEN | A/B already locked | — |
| #59 I/P partition pilot | (pending) | H1-tag: HOOK, H2, H4 candidate | — | — |
| (H3 sequel slot) | — | H3 + H1-tag: HOOK | — | — |
| — | — | — | — | — |
| — | — | — | — | — |

*Review trigger: after upload 5, score each hypothesis CONFIRMED / KILLED / EXTEND, then re-tier the mandate accordingly.*
