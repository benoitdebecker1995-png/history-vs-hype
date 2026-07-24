# Why Long-Form Is "Failing" — Diagnosis (2026-06-27)

**Method:** queried `analytics.db` directly (57 long-form, retention curves, traffic
sources, subscribed-status, daily channel, search terms). DB last refreshed 2026-06-26.
Numbers below are verified from the DB, not from memory or tool summaries.

---

## The reframe: this is NOT a content or retention problem

The channel's working assumption is "content is fine, packaging is the bottleneck."
The data half-confirms that and corrects it. The failure is **distribution**, and the
single biggest lever is **topic choice**, not within-video craft.

---

## Six verified findings

1. **Retention is fine and does NOT drive views.**
   - Median AVP 28.1% — normal for 10-min niche content. Best videos hit 44–49%.
   - `corr(views, retention) = 0.14` (≈ zero). `corr(log-views, retention) = 0.09`.
   - The breakout (Guatemala, 29,814 views) has only **rank-12/57** retention (35%).
   - Videos with the *best* retention (45.8%, 44.5%) have **42 and 51 views**.
   - → Optimizing openers/pacing/micro-retention cannot move views. Stop spending there.

2. **One video IS the channel.**
   - Guatemala "Country That Might Disappear" = **63.6%** of all 46,860 views.
   - Top 3 = 79%. Top 5 = 84%. Median video = **92 views**. 42/57 are under 200.
   - The channel had exactly one algorithmic breakout and has not repeated it.

3. **The channel is in decline since that breakout cooled.**
   - Monthly views (daily_channel): Dec 36,308 → Jan 24K → Feb 22K → Mar 23K →
     Apr 10K → May 12K → Jun ~2K. The Dec peak ≈ the Guatemala surge; once it faded,
     the channel reverted to its ~100-view baseline.
   - No learning curve: publish-cohort median views are flat-to-down across 12 months
     (best month Aug-2025 = 228; recent months 42–151). Iterations are not compounding.

4. **Topic TYPE is the strongest lever in the data.**
   | topic_type | n | median views | total views | share |
   |---|---:|---:|---:|---:|
   | territorial | 21 | **151** | 41,707 | **89%** |
   | ideological | 11 | 122 | 2,629 | 6% |
   | general | 16 | 84 | 2,008 | 4% |
   | colonial | 5 | 50 | 311 | <1% |
   | legal | 3 | 54 | 156 | <1% |
   - Territorial wins on median (robust to the outlier) AND owns every breakout:
     Guatemala×2, Venezuela-Guyana Essequibo, Turkey/Greek-islands, Berlin Conference.
   - The channel's *craft specialty* — forensic document/ideology debunks (Sol Invictus,
     Vichy law, $24 Manhattan, Flat Earth) — is its **distribution floor**.
   - **The tension: best craft, worst distribution.** The document-referee moat must
     ride a *territorial vehicle* to get served.

5. **This is a Suggested/Browse channel, not a Search channel.**
   - Search ≈ 5.8% of traffic (2,727 views; search_terms total 458). Suggested
     (RELATED_VIDEO) + Browse + subscriber feeds carry it.
   - 98.5% of views are from **unsubscribed** viewers (46,134 vs 726) — when a video
     gets served, it reaches new people fine. (This corrects the earlier "69% subscriber
     = trapped" read: that "SUBSCRIBER" label is a *traffic surface* concentrated in the
     one viral video, not the viewers' subscription status.)
   - Implication: views come from sitting *next to big videos in the Suggested feed.*
     Guatemala sat inside the huge RealLifeLore/geography-dispute ecosystem, so YouTube
     had somewhere to surface it — and it spawned a 2nd Guatemala video (5,387 views)
     purely in its slipstream. Obscure debunks have **no suggested parent**, so they
     never get served regardless of quality.

6. **DATA GAP — the diagnosis is capped here.**
   - `impressions` and `ctr_percent` are **NULL for all 57 videos.** The public YouTube
     Analytics API does not expose impressions or CTR; they live only in YouTube Studio
     (and VidIQ, which scrapes Studio). So the DB structurally cannot answer the most
     important question:
   - **Is each flop (A) low-impressions [YouTube never served it] or (B) low-CTR
     [served, nobody clicked]?** These have opposite fixes (A = topic demand + session
     signal; B = thumbnail/title). The "packaging is the bottleneck" thesis is currently
     **unverified** — it could equally be a "the algorithm never served it" problem.
   - The earlier thumbnail-CTR-by-style table is unreliable (two tools bucket the same
     videos oppositely; 0/57 real CTR). Do not act on it.

---

## What to do (ranked by leverage)

**1. Close the data gap before over-investing in packaging.**
Pull impressions + CTR per video from YouTube Studio (Content → per-video → Reach, or
VidIQ export) into analytics.db. With it we can finally split "never served" from
"served-not-clicked" and stop guessing. Cheap, highest diagnostic value.

**2. Topic selection is the real lever — commit to territorial/map disputes.**
Greenlight border/territory/sovereignty disputes that sit adjacent to the big geography
ecosystem (RealLifeLore/Wendover). Keep the forensic-document craft as the *delivery*,
but the *vehicle* must be territorial. Stop greenlighting standalone document/ideology
debunks with no suggested parent (they reliably floor out).

**3. Build clusters, not one-offs.**
The 2nd Guatemala video did 5,387 views off the 1st's slipstream. When any video gets
traction, ship 2–3 more in the SAME dispute cluster within 2–4 weeks to compound
suggested-feed adjacency. One-off topics waste any momentum.

**4. Packaging: disputed-map thumbnail, validated by native A/B.**
Direction (maps beat text/documents) is plausible but the CTR data is contested — so
treat it as a hypothesis and confirm with single-variable native A/B swaps, not the
distrusted category averages.

**5. Stop the micro-optimization treadmill.**
Opening formulas, proof-first ordering, list-vs-not all died out-of-sample on this
channel's own holdout. That effort is better spent on #1–#3.

---

## One-line summary

Long-form isn't failing on quality or retention — it's failing on **distribution**,
because most topics have no large neighbour in the Suggested feed. The fix is **pick
territorial/map disputes adjacent to big geography channels, ship them in clusters, and
get impressions/CTR data so we stop optimizing blind.**
