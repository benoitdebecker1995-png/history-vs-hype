# Gemini-in-YouTube Prompts (Studio surface) — live-insight set

**Built 2026-06-14.** Paste-ready prompts the **user** runs inside **YouTube Studio Gemini** (which can
see the channel's private analytics — per-video CTR, impressions, traffic source, viewer type), then
pastes the answer back. Same operating pattern as the VidIQ in-app chat and `serp_thumb_study`:
Claude authors the prompt, the user runs it, Claude reads the result.

**Why this exists:** the static corpora (`analytics.db`, `intel.db`, the 2026-02-23/06-10 CTR
snapshots) are months stale, and native A/B / live-window numbers are captured nowhere else. These
prompts are **enrichment, not a gate** — paste-back is optional.

**Reliability note (important):** the per-video *number* prompts (CTR / impressions / traffic /
search-terms / viewer-split) read straight from Studio analytics and proved **accurate** this
session. The **visual thumbnail teardown (P7) HALLUCINATED** — it "described" thumbnails it could not
actually see (it invented a single-face Hijab thumbnail that is really a 3-panel timeline). **Do not
trust Gemini's descriptions of thumbnail *images*; verify against the real file.** Use it for numbers,
not for vision.

---

## P1 — Recent-uploads Gate-2 scan (impressions vs CTR; thumbnail-test status)
```
Act as my channel analyst. For my last 12 published long-form videos (exclude Shorts), give me a
markdown table: Title | Published | Impressions | CTR% | Avg view % | Top traffic source
(Browse/Suggested/Search/other) | Thumbnail Test result. For "Thumbnail Test result", if a Test &
Compare experiment ran, name the winning variant + margin/confidence; else "none". Then: (1) which
got 1,000+ impressions but CTR under 4%? (2) for any completed thumbnail test, what visually
differed between winner and loser? (3) among the highest-CTR videos, what is the dominant traffic
source? If you can't access a field, say so instead of estimating.
```

## P2 — 90-day over-performers + live niche formats (greenlight outlier input)
```
Using my channel's data and niche: which of my last ~20 videos most over-performed their expected
baseline (views or CTR) in the last 90 days, and what did they share (topic, title pattern, thumbnail
style)? Separately: what topics and packaging formats are currently driving impressions and new
(non-subscriber) viewer reach for small history / geopolitics channels like mine right now? Flag
anything you're inferring vs. reading from my data.
```

## P3 — All-time CTR winners vs losers (validate the craft recipe)
```
Act as my channel analyst. Lifetime data, long-form only, minimum 500 impressions. Two tables.
Table A — my 8 HIGHEST-CTR videos: Title | Impressions | CTR% | Avg view % | Top traffic source.
Table B — my 8 LOWEST-CTR videos: same columns. Then: (1) what do the top-8 titles share (pattern,
keywords, length, numbers)? (2) the bottom-8? (3) for the top 3, the thumbnail's main visual element
if visible? Mark anything inferred vs read from data.  [NB: trust the numbers, not the thumbnail
descriptions — see reliability note.]
```

## P4 — Top search terms (validate the keyword-ladder / search-anchor lever)
```
Act as my channel analyst. From YouTube Search traffic, last 90 days: list the top 20 search terms
that brought me impressions — Term | Impressions | CTR% (if available). Then: (1) which terms are
country/region/entity names vs generic phrases? (2) which have high impressions but low CTR (shown,
not clicked)? (3) which of my videos does each top term lead to? Read from data; flag inference.
```

## P5 — First-48h ramp (calibrate the swap-protocol trigger)
```
Act as my channel analyst. For my last 6 long-form uploads, compare first 48 hours vs first 10 days:
Title | Impressions @48h | CTR% @48h | Impressions @10d | CTR% @10d. Then: (1) did impressions keep
climbing after 48h or plateau? (2) at what point did the algorithm stop pushing the underperformers?
(3) is there a first-48h CTR threshold that separated videos that kept getting impressions from those
that stalled? Read from data; flag inference.
```

## P6 — New vs returning + what you're "riding" (the growth target)
```
Act as my channel analyst, last 90 days. (A) Split CTR and views by NEW vs RETURNING viewers — do
non-subscribers click at a different rate? (B) for my best Suggested-traffic videos, which
videos/channels is my content most suggested next to? (C) what % of my views come from
non-subscribers? Read from data; flag inference.
```

## P-SWAP — Best thumbnail-swap test bed (single-variable click-fix loop)
```
Act as my channel analyst. I want to run a THUMBNAIL-ONLY swap experiment. A video whose reach has
died gives no signal, so I need one still being shown. Find my best 3-5 candidates: Title |
Impressions (last 28 days) | CTR% (last 28 days) | Dominant traffic source | Lifetime CTR%. Rank for
fit, where the ideal has ALL of: still pulling meaningful impressions in the last 28 days; low CTR
(headroom); impressions skewed to Browse/Suggested (where the THUMBNAIL drives the click); enough
volume to read a change in ~2-4 weeks. Name the single best first test and why. Read from data; flag
inference.
```

## P7 — Thumbnail visual teardown — ⚠️ UNRELIABLE, use with caution
```
Act as my packaging analyst. Look at the actual THUMBNAILS (images, not titles) of [WINNERS list] vs
[LOSERS list]. For each: main subject · # focal points · text overlay (words + size) · dominant
colors · any red/accent · real-photo vs illustration/AI · readable at small size. Then: 3 visual
traits the WINNERS share that the LOSERS lack. Describe only what you can actually see.
```
**⚠️ This prompt hallucinated real thumbnails (2026-06-14).** Prefer pulling the real image files and
judging them directly (or with a vision tool you control). Keep only if you cross-check every claim.

---

**Wired into:** the 48h **swap protocol** (P5 + P-SWAP — judge on new-viewer CTR, watch the ~1.3%
@48h throttle floor) and `/greenlight` **outlier-mining** (P2 as a live complement to the static
`intel.db` scan). See `tools/SWAP-PROTOCOL.md`, `.claude/commands/greenlight.md`, ADR 0007.
