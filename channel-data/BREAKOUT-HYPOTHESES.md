# BREAKOUT HYPOTHESES — Next 5 Uploads

**Built:** 2026-06-10 (Fable Phase 1) | **Input:** D1 breakout dossier + D4 whitespace scan
**Status:** ACTIVE — each upload should consciously run one of these as its A/B test. Update the Outcome column as data lands; a hypothesis is CONFIRMED or KILLED only by its named metric, not by vibes.

> ### 🎯 PRE-REGISTERED THRESHOLDS FOR #36 PANAMA (locked 2026-07-28, BEFORE publish)
> | metric | confirm | kill |
> |---|---|---|
> | **H3** first-28-day impressions | **≥9,000** (≥3× recent median) | **<4,500** (<1.5×) |
> | **H2** first-28-day CTR (≥1,000 impr) | **≥4%** | <2.5% |
> | **H6** both terms present | pocket named ✓ · stranger-legible ✓ | — |
> | **H3 geography — the falsifiable one** | disproportionate share of views from **Panama + US-Panamanian diaspora**, checked in Studio exactly as Belize was | **generic-US geography ⇒ H3 is WRONG** and something else drove Belize |
>
> ### ➕ ADDED 2026-07-28, BEFORE #36 PUBLISHES — H3 needs a SHAPE criterion, not just a total
> | metric | confirm | kill |
> |---|---|---|
> | **H3-shape** day-1 share of first-28-day impressions | **<60%** | **≥80% ⇒ test batch, not a pocket** |
> | **H3-shape** impressions in days 8–28 | **≥1,500** | **<300 ⇒ serve collapsed** |
>
> **Why this was added, and why it is not post-hoc.** A total-only threshold cannot tell a demand pocket
> from a failed test batch, and #59 proves it. Its daily series — recoverable only now that
> `impressions_daily` exists — reads **9,626 impressions on day 1, then 44, 102, 44, 50…** It reached
> **10,087 by day 21 and would have "CONFIRMED" H3 at ≥9,000**, while actually being a video YouTube served
> once, tested, and cut inside 48 hours. That is the opposite of what H3 claims to detect.
> This **strengthens** a pre-registered hypothesis using a measurement that did not exist when it was
> written; it is dated and locked **before** #36 publishes. **The 9,000 / 4,500 totals are NOT retuned** —
> re-deriving thresholds after seeing results is exactly what pre-registration prevents.
>
> ⚠ **Honest basis:** only **two** complete first-28-day windows are historically reconstructable
> (`aSfZtrgGjwA` = 2,422 · `zt7VntgauC8` = 3,088), because Reporting API retention is ~60 days.
> **The 9,000/4,500 numbers rest on n=2.** Manual Studio Advanced-mode exports for the last ~16 videos are
> the only way to give them a real distribution (`studio_import.py` already supports it — data entry, no
> code). Cite the n=2 basis whenever these thresholds are used.
>
> ⚠ **Surface caveat:** H3 is framed on **browse** impressions, but `channel_reach_basic_a1` reports
> **total** impressions across all surfaces. Job `31fd84bd-0dbf-436b-a608-8f80a16b2d93`
> (`channel_reach_combined_a1`) was created 2026-07-28 to test whether a per-surface split is available;
> reports take 24–48h. **Until it lands, treat these thresholds as total-impression thresholds.**
>
> ✅ **~~Measurement gap~~ — CLOSED 2026-07-28.** `HvH-CtrTracker` ran **weekly, Mondays only**, which is
> why #59's launch window was lost (published a Sunday; days 0–4 never captured). Now: **daily at 14:30**,
> writing `impressions_daily` at the **data-date** grain, so ingest is idempotent and a missed run
> self-heals rather than losing the day. Day 0 of #59 was recovered retroactively from API history as
> proof. See ADR-0018.

**Baselines (for thresholds):** channel median views = 91; recent-upload impression tests = 1.7K–5.2K (fresh ctr_tracker window); channel median CTR = 2.48% (lifetime snapshot); avg-watch median = 28.1%.

---

## Identity guard (recalibrated 2026-06-11, user directive)

The channel is **method-first**: history through primary sources, showing how history is done (positioning set in the intro video, yt:yMAWJcjo_ug). Everything below is packaging tactics WITHIN that identity. No hypothesis may push the channel toward regional positioning ("the Belize/Latin-America channel") or stakes-first geopolitics framing (RealLifeLore lane = anti-voice). Demand pockets are raids; the brand is the method.

## The causal story these hypotheses test

Forensics say the 3 breakouts shared: (1) a live contemporary hook at publish, (2) country-name head terms with search volume, (3) bilateral-conflict existential stakes in the title. No current packaging rule captured any of these. Meanwhile the title construction rules (colon/year/pattern) explain almost none of the variance: the scorer REJECTED the #1 and #3 videos and gave 100/A to videos that died at 228 views.

**B1 reinterpretation (2026-06-11):** Studio geography (user-verified) shows B1's audience was largely Belize-national. The breakout was an **underserved demand pocket** — a real English-speaking audience with near-zero quality English coverage of an active dispute — not franchise equity. B2 (+5 weeks, inside B1's push window) inherited the push; the Sapodilla Cayes sequel (`sXadwOj8VoA`, 2026-03-30, same project folder) got 47 views with only 7 subscriber/browse views despite 41.5% avg watch. Pocket audiences are topic-bound and decay with the push.

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

## H3 — Underserved demand pocket (REPLACES sequel-inheritance, which is KILLED)

**Killed predecessor (2026-06-11):** "Sequel inheritance" was already tested before this doc existed and failed: the Sapodilla Cayes follow-up (`sXadwOj8VoA`, 2026-03-30) — a direct continuation of the B1/B2 Guatemala–Belize franchise — did 47 views, 0 subs, 7 subscriber/browse views, despite top-decile retention (41.5% avg watch). B2's 5,355 came from publishing INSIDE B1's active push window, not from durable audience equity. Honest caveat: the Sapodilla title never named Belize or Sapodilla ("Honduras Called These Islands…"), so the pocket was never signaled — the kill is strong but not airtight. Either way, no more Guatemala–Belize sequels as a strategy bet; the user is not building a Belize channel.

**Replacement claim:** Topics with (a) a real English-speaking national/diaspora audience, (b) near-zero quality English coverage on the SERP, and (c) an active dispute/news cycle get disproportionate impression tests. This is what B1 actually validated. These are **raids — one per region, method-first framing** — never repositioning.
**Test:** One of the next 5 uploads targets a verified pocket. Pocket checklist at greenlight: SERP scan shows no quality English explainer + active local news cycle or VidIQ volume + passes channel-DNA test ("primary sources on screen, matters in 10 years").
**Confirm:** ≥3x median first-28-day impressions vs the channel's recent uploads.
**Kill:** <1.5x — pocket theory adds nothing over plain H1 topicality.

### H3 shape addendum — record the shape, do NOT add a threshold (2026-08-04)

**Why:** a total-impressions test cannot separate a demand pocket from a test batch that failed.
#59 took **9,626 impressions on day one — 95% of its 28-day window** — then ran a 2% tail across
days 8–28. On totals alone it would have *passed* the 9,000 bar while being a total failure.

**Instrument:** `tools.discovery.ctr_reads.launch_shape_for(conn, video_id, published_date)` —
day-1 share, days 1–3 share, days 8–28 tail share, peak day, and the daily series. It reproduces
the two known complete windows (2,422 and 3,088) exactly. It returns **no verdict**, by design.

**All three launch windows we hold** (ingest began 2026-05-24, so this is the whole sample):

| video | 28-day impr | day 1 | day-1 share | days 1–3 | days 8–28 tail | peak day |
|---|---:|---:|---:|---:|---:|---:|
| Slave-trade system | 2,422 | 1,659 | 68% | 85% | 8% | 1 |
| Piri Reis map | 3,088 | 158 | 5% | 55% | 3% | 4 |
| #59 I/P 1947 UN plan | 10,148 | 9,626 | **95%** | 96% | **2%** | 1 |

**What this does and does not license.** It shows the two failure modes are distinguishable in
day-grain data: a front-loaded dump (#59) looks nothing like a build (Piri Reis, peak on day 4).
It does **not** license a share threshold — **n=3**, every one of them a non-breakout, and no
successful launch is in the sample at all, so "what a good shape looks like" is unobserved. The
9,000/4,500 numbers stay exactly as pre-registered; retuning them now would be post-hoc.

**Record the shape for every future launch.** When a fourth and fifth window close, a criterion
becomes arguable. Until then this is a description with a sample size attached, and the tail share
is the number to watch — all three died in the tail, whatever they did on day one.

## H4 — Searched-anchor-first beats document-first in titles (reframed 2026-06-11)

**Claim:** Titles that front-load the SEARCHED subject (the country/conflict/figure people actually type) outperform titles that front-load the document/artifact/obscure entity — for the same video. The evidence reveal stays as the second punch ("…The Documents Disagree"), which is the method-first identity doing the clicking work, not stakes-vaporware.
**Evidence for:** Stalls front-load zero-volume terms: "The Lenape Never Sold Manhattan" (0% CTR on 101 imp), "Treaty of Tripoli:…" (37 views), "Britain Expelled 2,000 Islanders. The Memo Proves It" (29 views). Breakouts front-load searched subjects. NOT a license for geopolitics-stakes framing (anti-voice); the anchor names the subject, the second sentence promises the evidence.
**Test:** Native A/B (3 title+thumbnail combos, uploaded together) on ≥2 of the next 5 uploads: searched-anchor-first arm vs document-first arm, same thumbnail family.
**Confirm:** anchor-first arm wins the impressions×CTR composite in ≥2 of 3 tests.
**Kill:** document-first arm wins ≥2 of 3 — then the method-marquee IS the brand draw and V2 gets softened.

## H5 — Colon reintroduction (retire the hard reject permanently)

**Claim:** "X vs Y: Stakes" colon titles are at worst neutral (the -28% penalty was topic-confounded).
**Evidence for:** #1, #2, #3 videos all have colons; fresh CTRs 8.49% / 12.11% / (4.31% lifetime).
**Test:** One A/B arm on a versus-topic upload uses the colon format. Single-variable: same thumbnail, same head term. Judge on search impressions + CTR composite (per data-overrides-rules-for-testing — not CTR alone).
**Confirm (non-inferiority):** colon arm within 10% of the best arm's composite → colon rule stays HEDGE/neutral forever.
**Kill:** colon arm loses by >25% → restore -25 penalty (still not auto-REJECT).

---

## H6 — The two-term serve model (NEW 2026-07-28, supersedes "stakes-first" as a lone factor)

**Built from:** `channel-data/BREAKOUT-MECHANICS-2026-07.md`. Four predictors of serve size were tested
and ALL failed (CTR, retention, thumbnail feature tags, peer coverage; plus channel-state and topic_type).
The escalation event is **not predictable** from anything measurable. H6 is the best surviving *descriptive*
model, and it is explicitly n=1 on the winning cell.

**Claim:** serve size needs BOTH terms, and either alone underperforms:
> **(1) the POCKET is named in the title** — an English-reading national/diaspora audience must be able
> to see the video is about them · **(2) the STAKE is legible to a stranger** — parseable with zero prior
> knowledge of the dispute.

**Evidence (the channel's own H3-shaped uploads):**

| video | pocket | named | stranger-legible | impressions |
|---|---|:-:|:-:|---:|
| "**The Country That Might Disappear**: Guatemala vs Belize" | Belize | ✓ | **✓** | **292,398** |
| "The Oil War Over **Essequibo**" | Guyana | ✓ | ✗ (must know Essequibo) | 36,263 |
| "**Somaliland's** Legal Independence Problem" | Somaliland | ✓ | ✗ (abstract) | 6,187 |
| "Britain Drew the India–Pakistan Border in 5 Weeks" | India/Pak | ✓ | ✓ but coverage saturated | 3,111 |
| "Britain Expelled 2,000 Islanders" (**Chagos, unnamed**) | Chagos | ✗ | ✓ | 781 |
| "Honduras Called These Islands…" (**Sapodilla/Belize, unnamed**) | Belize | ✗ | ✓ | 508 |

**Aggregate:** H3-shaped uploads (n=9) median **5,610** impressions / **228** views vs **2,772 / 92** for
everything else — ~2×, and **3 of the channel's top 5 by views are H3-shaped.** The mechanism is real;
the variance inside it is what H6 explains.
**Note this reconciles H3 with the "stranger-legible stakes" idea — they are not rival explanations, they
are the two terms.** Belize is the only upload that has both.

**Test:** across the next 4 uploads, tag each at publish for BOTH terms (pocket-named Y/N ·
stranger-legible Y/N), pre-registered in `YOUTUBE-METADATA.md`, never retro-fitted.
**Confirm:** both-terms uploads median first-28-day impressions ≥3× single-term uploads.
**Kill:** <1.5×, or a both-terms upload lands under 5,000 impressions twice.
**⚠ Standing caveat:** the winning cell is **n=1**. Do not treat H6 as a formula. It sets the packaging
brief; it does not predict the serve.

---

## Pre-registration log

| Upload | Date | Hypotheses carried | Arms | Outcome |
|---|---|---|---|---|
| #58 Kurdistan | (pending) | H2 (CTR ≥4% target), H1-tag: EVERGREEN | A/B already locked | — |
| #59 I/P partition pilot | (pending) | H1-tag: HOOK, H2, H4 candidate | — | — |
| **#36 Panama — H3 POCKET SLOT, FILLED 2026-07-28** | (pending) | **H3** pocket raid · **H6** both-terms · H1-tag: **HOOK** (re-verified 2026-07-28: ICC arbitration >US$2B, Panama missed the 13 Mar deadline, Beijing "heavy price"; runs years) · H2 (CTR ≥4%) · H4 A/B | **LEAD:** "America Took the Panama Canal With a Treaty. Panama Took It Back." (65ch) · **ARM B:** "A Frenchman Signed Away the Panama Canal. Panama Took It Back." (62ch) — single-variable, same second sentence, same thumbnail family | — |
| sXadwOj8VoA Sapodilla | 2026-03-30 | (retro) sequel-inheritance | n/a | KILLED — 47 views, 7 sub/browse views, 41.5% watch |
| Panama Canal treaties (greenlit 2026-06-11) | (pending) | H1-tag: HOOK (verified live: CK Hutchison/Supreme Court cycle), H2 (CTR ≥4%), H4 A/B | A: "Panama vs the Canal Treaty. Not One Panamanian Signed It." (93/A, curiosity 82) · B: "No Panamanian Signed the Panama Canal Treaty. Here's Who Did." (77/B, curiosity 84) — same thumbnail family | — |
| — | — | — | — | — |

*Review trigger: after upload 5, score each hypothesis CONFIRMED / KILLED / EXTEND, then re-tier the mandate accordingly.*
