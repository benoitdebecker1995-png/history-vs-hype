# A/B Test Results + Traffic-Source CTR (2026-06-27)

The only CAUSAL packaging data we have (Test & Compare = same image, randomized) + the
CTR-by-surface split. Companions to CTR-TITLE-FORMULA / CTR-THUMBNAIL-FINDINGS.

---

## Traffic-source CTR (Studio export, channel aggregate — Guatemala-weighted)

| surface | impressions | views | CTR |
|---|---:|---:|---:|
| Browse (Home feed) | 349,433 (61%) | 33,263 | **7.50%** |
| YouTube search | 32,416 | 3,189 | **6.73%** |
| Suggested videos | 175,948 | 6,363 | **3.07%** |
| Channel pages | 16,537 | 548 | 2.63% |
| Playlists | 2,225 | 167 | 3.46% |
| **Total** | 576,559 | 47,722 | 5.95% |

**Read:** thumbnails convert HEALTHY on Browse (7.5%) and Search (6.73%) — the click is not
broadly broken. Weakness is the **Suggested** surface (3.07%) + the many obscure videos that
never earn Browse impressions. The low per-video blended median (2.51%) is mostly an
impressions-distribution artifact, not a thumbnail-quality failure. Lever stays: fame →
Browse impressions → healthy click. Caveat: aggregate is dominated by Guatemala; a
Video×Source export would give per-video Browse CTR (next pull).

---

## Per-video surface CTR (Browse + Suggested exports, 2026-06-27)

Files: `D:\browse table.csv`, `D:\suggested table.csv`. Persisted to
`analytics.db.surface_ctr` (video_id, browse_impr/ctr, sugg_impr/ctr).

**BROWSE CTR = the purest packaging signal** (cold Home feed, no search intent). Reliable
subset (Browse impr ≥1,500, n=16):
- **Fame delta +2.23%** (famous-topic median **5.65%** vs non-famous **3.42%**) — LARGER than
  the blended +1.26%. Fame matters most on the discovery surface, where strangers decide.
- Validated rules HOLD on this clean surface: clutter hurts (busy 4.26% vs clean 5.65%),
  document-focal low (Somaliland 3.42, Stalin 2.07), map mild +.
- Top Browse CTRs: JD Vance 11.15%, Guatemala-2 9.83%, Guatemala-1 8.44%, Venezuela 6.5%,
  Kashmir 5.75%, Crusades 5.65%. Packaging WORKS when the topic is famous.

**SUGGESTED CTR proves the CLUSTER effect** (impr ≥2,000):
| CTR | video | cluster? |
|---:|---|---|
| 7.31% | Guatemala-2 | Latin-Am border-dispute cluster |
| 4.15% | Guatemala-1 | cluster |
| 3.96% | Venezuela–Guyana | cluster |
| 3.24% | Israel/Palestine myths | |
| 0.93–0.56% | Kashmir, Stalin, Trade Wars, Sol Invictus, China-Taiwan, Medieval, USSR | isolated |

The dispute cluster pulls **4–7% on Suggested; isolated videos 0.5–1% — a 4–7× swing.**
Videos in a tight topical neighborhood feed each other's Suggested traffic; one-offs get
suggested next to unrelated content and die. → DATA-BACKED cluster strategy: ship 2–3 in the
same dispute family.

---

## Test & Compare A/B results (3 old videos)

**Two hard caveats:** (1) metric is **Watch-time share**, NOT CTR (click × retention, YT's
own optimization target); (2) ALL THREE returned **"finished without a conclusive result"**
— not statistically significant. Small-channel traffic can't power A/B to significance yet.
Each test held the IMAGE constant and varied only the TEXT OVERLAY → clean overlay-wording test.

| video | variant (overlay) | watch-time share |
|---|---|---:|
| Guatemala "Country Might Disappear" | **DOES BELIZE EXIST? / ICJ RULING 2027** | **38.7%** |
| | GUATEMALA VS BELIZE / BORDER ON TRIAL | 34.5% |
| | GUATEMALA VS BELIZE / ENTIRE COUNTRY CLAIMED | 26.8% |
| JD Vance child sacrifice | **3 HISTORICAL CLAIMS / FACT CHECKED** | **36.8%** |
| | CHILD SACRIFICE? / THE REAL EVIDENCE | 32.9% |
| | VANCE vs HISTORY / WHO'S RIGHT? | 30.3% |
| Crusades | **CRUSADES… / FACT CHECKED** | **37.2%** |
| | CRUSADES… / MYTHS BUSTED | 31.9% |
| | CRUSADES… / REALITY CHECK | 30.9% |

**Cross-test signals (directional — all individually inconclusive):**
- **"FACT CHECKED" beat its synonyms in 2 independent tests** ("Myths Busted", "Reality
  Check", "The Real Evidence"). Best current candidate for default verdict-overlay wording.
- **Existential question ("DOES BELIZE EXIST?") beat flat framings** ("Border on Trial",
  "Entire Country Claimed") on Guatemala.
- Consistent with the validated title levers (verdict language + curiosity gap).

**Meta-finding:** native A/B will keep returning "inconclusive" until the channel earns
enough impressions per video to reach significance — i.e., A/B power is itself gated on
fame/topic. Run it anyway (every overlay datapoint compounds), but don't expect clean wins
until traffic grows. Use multi-video repetition (like "FACT CHECKED" winning twice) as the
real signal, not any single inconclusive test.
