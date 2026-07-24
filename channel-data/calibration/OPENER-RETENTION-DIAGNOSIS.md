# Retention Investigation — Consolidated Findings (2026-06-26)

**Supersedes** the earlier n=21 opener-retention diagnosis (which ran on a pre-backfill DB
and an unverified 61/58/31 Gemini-paste trio). This is the canonical record after the data
was fixed and the hypotheses were holdout-tested.

---

## TL;DR

We spent this investigation hunting for a **within-video formula** that separates our hits
from our misses. **Four candidate formulas were tested; all four died.** The thing that
actually tracks performance is **topic** (broad / current / territorial-dispute stakes) and
**packaging** (disputed-map thumbnails), not how the script is written or opened.

**Act on:** topic selection + disputed-map thumbnail + CTA-at-the-very-end.
**Stop doing:** engineering the opening to a template — no opening template survived testing.

---

## 1. The data is now real (was the blocking problem)

- `analytics.db` was backfilled **2026-06-26** with genuine YouTube API retention curves for
  **all 57 long-form videos** (verified against the May-3 cache to ±0.003; 57/57 curves
  distinct — no synthetic fill). Previously only ~21 were mapped.
- The "Tripoli" video (the lost best-retainer) **is** `liW4BSh46DU` — "America's Founding
  Secular Quote Was Never in the Original" — first30 ≈ 0.71, body ≈ 0.49, AVP 45.8% (2nd-
  highest). Its problem is impressions (42 views), not retention.
- Corrected headline correlations on the full set:
  - `first30 ↔ body_mean` = **+0.46 (n=57)** — early bleed and whole-video bleed move
    together. NOT an opener-cliff problem; a whole-video level.
  - `duration ↔ body` = **−0.09 (n=48)** — essentially zero (see §2).

## 2. Four formulas tested → four deaths

| Formula (hypothesis) | How it died | n |
|---|---|---|
| **Opener craft score** | composite/SUCCES score vs first-30s retention rho ≈ 0 (flat) | 21 |
| **List vs single-thread** | Kashmir is a clean single-thread and is a *worst* bleeder; Sahel (list) and Kashmir (thread) both bleed → structure doesn't predict | 8 |
| **Length / "go shorter"** | duration↔body = −0.09 on n=48; buckets flat to 13 min. The −0.30 I first quoted was a skewed 21-video subset. | 48 |
| **Proof-first opening** (lead with document/date/quote, not context) | **Failed the holdout:** context-first 41.1% vs proof-first 39.8% @ 0:90 — a dead heat. | 15 holdout |

**Why they kept dying — the selection-on-extremes trap.** Each "finding" was derived by
looking at the *best* and *worst* videos and labeling them after the fact (best happened to
be proof/short/single-thread; worst happened to be context/long/list). Select on the
dependent variable and you can manufacture almost any pattern; the middle of the distribution
shows it isn't real. **Rule going forward: any within-video pattern derived from a best/worst
subset must be holdout-tested on the rest before it earns any authority.**

## 3. What actually survived

**TOPIC is the recurring signal.** Every time a formula died, the data re-pointed at topic:
broad / current / famous territorial-or-legal-dispute stakes retain and get clicked (NATO,
Soviet collapse, Guatemala–Belize, South China Sea); niche / academic / distant topics bleed
and don't get clicked (Brazil's measurement error, a 38-dead border skirmish, 7th-century
Isidore of Seville). The holdout's own conclusion ("specificity can't save a topic that lacks
broad appeal"), the mid-video "niche-shift" drop, and the thumbnail CTR data all triangulate
on topic. Directional, but it's the best-supported lever and it matches CLAUDE.md's standing
"packaging/impressions is the bottleneck, not within-video content."

**Two clean, actionable wins:**

1. ~~**Thumbnail = disputed-territory MAP + number overlay.**~~ **RETRACTED 2026-06-27.** I
   over-called this "the strongest signal." On re-test the two tools contradict each other and
   classify the *same* videos into opposite buckets (JD Vance 9.37% = "document" to YT-Studio,
   "face" to VidIQ); yesterday's VidIQ said documents are WORST (0.93–1.62%), next-day YT-Studio
   said BEST (9.37%). The DB has **no CTR data** to adjudicate. Category averages are outlier-
   placement artifacts (selection-on-extremes again). **Durable residual: text-only thumbnails
   are worst (both tools agree). Map-vs-document is undecided — settle it per-video by native
   A/B, not by category CTR.** See `CHANNEL-PERFORMANCE-DATA-2026-06.md` thumbnail section.
2. **Move every like/subscribe CTA to the final 5%.** A mid-video CTA reads as "the new info
   is over." Kashmir's "please consider liking…" at 7:45 (2 min before the end) cost ~9% of
   remaining viewers — confirmed present in the transcript.

**Mid-video (directional):** drops cluster at "context detours / how-we-got-here history
dumps." Best bodies use a "layered reveal" (document → consequence → contradicting document →
what's next). Bridge any deep-history detour to a modern link.

## 4. The hard constraint that shaped all of this

**An LLM cannot reliably judge whether a hook is "strong" or a script is "good."** That
judgment is the unreliable, confabulation-prone part. The reliable workflow is: locate where
retention drops (real data) → tag the script with **objective countable features** (year,
number, list-announcement, methodology phrase, hedge, quote — all regex) → correlate with the
real curve → **holdout-test** before believing it. Claude's role is plumbing + stats +
verification, not taste.

## 5. Tool reliability — verify every claim

YT Studio Gemini and VidIQ both confabulate specific numbers. Caught this session:
- VidIQ: "Suggested traffic 1.4% (algorithm stopped pushing you)" → actually **13.2%** (healthy).
- VidIQ: "back-half relative retention exceeds 1.0, content is great" → actually **0.65** (below par).
- YT Studio: "ban every 'What if I told you' hook" → falsified by its own #5 best opener
  (KGB-PLO) which uses that exact phrase and holds.
- YT Studio's "best/working" videos in audit #1 were all **Shorts** (101–109% APV = loops).

Always re-check tool numbers against `analytics.db` before acting.

---

*Investigation 2026-06-26. Single channel, n small throughout — directional. Read-only over
`analytics.db` (retention_curves + videos + traffic_sources) plus YT-Studio-Gemini and VidIQ
channel-aware reads (verified, not trusted).*
