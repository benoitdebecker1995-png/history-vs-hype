# Metadata Checklist

**Standalone reference for YouTube publishing. Use alongside `/publish`.**

> **Cross-ref:** Title generation rules and penalty data also in `TITLE-GENERATION-PROTOCOL.md`. Keep both in sync.

---

## Title (CRITICAL — biggest lever for growth)

- [ ] **10 options generated** (not 3) — variety across patterns
- [ ] **Each flagged as SEARCH or BROWSE** — search titles target keywords people type; browse titles optimize for feed clicks
- [ ] **Under 60 characters** — readable on mobile
- [ ] **Front-load keyword** — main topic word in first 3-4 words
- [ ] **Year in title** — graded penalty, not a ban. `YEAR_PENALTY -15` / `YEAR_PENALTY_HOOK -5` (`tools/title_scorer.py:308-310`). The old "-46%" figure was topic-confounded and is retired.
- [ ] **Colon in title** — graded penalty, not a ban. `COLON_PENALTY -10`, and **0 for versus titles** (`tools/title_scorer.py:311-313`). The channel's #1 and #3 videos both use colons.
- [ ] **No "The X That Y" pattern** — hard reject per PACKAGING_MANDATE
- [ ] **Scored by `title_scorer.py`** — minimum 60/100
- [ ] **Declarative or versus pattern preferred** — highest measured CTR
- [ ] **Read aloud test** — would you click this on your phone?

### Title Pattern Quick Reference

| Pattern | Avg CTR | Example |
|---------|---------|---------|
| Versus | ~3.7% | "Spain vs Portugal: Who Really Owned the New World?" |
| Declarative | ~3.8% | "How Spain and Portugal Divided the World" |
| How/Why | ~3.3% | "Why Brazil Speaks Portuguese" |
| Colon | ~2.3% | "Treaty of Tordesillas: How the Pope Split the Globe" |

---

## Thumbnail (Second biggest lever)

- [ ] **3-5 concepts generated** — variety of visual approaches
- [ ] **2-4 word text overlay** — mandatory (87% of niche, n=650). Short phrase, NOT full title
- [ ] **No talking-head face** — 0% of niche uses selfie/talking head. Historical/subject photos OK
- [ ] **Map-first when territorial** — maps for border/territory topics (88% of geo channels)
- [ ] **Historical/document visual when myth-busting** — maps optional for ideological topics (14% of closest matches)
- [ ] **Phone-size test** — shrink to 160x90px, still readable?
- [ ] **High contrast** — readable at thumbnail size
- [ ] **Checked by `thumbnail_checker.py`** — passes automated gates

---

## Description (Niche-benchmarked, 150 descriptions across 14 channels)

- [ ] **First line is thesis/hook** — NOT generic topic. "In 1494, the Pope drew a line..." beats "This video covers the Treaty of Tordesillas." Fall of Civilizations leads with evocative hooks even in descriptions.
- [ ] **First 2 lines keyword-rich** — these show in search results. Front-load the main topic keyword.
- [ ] **Source citations included** — full academic references. 73% of our descriptions cite sources vs 43% niche avg — this is our competitive advantage, keep it.
- [ ] **Chapters/timestamps** — we include in 84% of videos vs 29% niche. Keep doing this.
- [ ] **1-line subscribe CTA** — 94% of niche includes one. We only have 44%. Add "Subscribe for evidence-based history" or similar.
- [ ] **3-5 hashtags at END** — not in first 3 lines (YouTube shows first 3 hashtags above title if placed early)
- [ ] **Target 1,000-2,000 chars** — niche avg is 2,030 chars. Ours averages 2,011. On target.
- [ ] **No links in first 2 lines** — Kraut/CaspianReport waste first lines on sponsor links. Don't do this.

### Description Formula (from niche analysis)
```
LINE 1: Thesis statement or strongest specific claim
LINE 2: What this video examines / unique angle

2-4 sentence summary with main keyword 2-3x.

TIMESTAMPS
0:00 - [Chapter]
X:XX - [Chapter]

SOURCES
[Academic citations: author, title, publisher, year, pages]

Subscribe for evidence-based history analysis.

#Hashtag1 #Hashtag2 #Hashtag3
```

---

## Tags

- [ ] **15-20 tags** — comma-separated, ready to paste
- [ ] **Mix of broad + specific** — "history" + "Treaty of Tordesillas 1494"
- [ ] **Include:** topic keywords, person names, document names, related events
- [ ] **VidIQ keyword check** — verify search volume on top 3 tags

---

## Search Term Optimization (from SEARCH-TERM-ANALYSIS.md, 2026-03-21)

- [ ] **Title-search mismatch check** — Before publishing, ask: "What will people *type* to find this?" If the answer differs from the title, add the search term to the description first paragraph. 9 of 24 analyzed videos had 0% title-search overlap (e.g., audience searched "selknam" for a video titled "London's Stock Exchange Funded a Genocide").
- [ ] **Top search terms in description first paragraph** — Include the most likely search query in the first 2 lines. These show in search results. High-value terms (best watch time per view): "belize guatemala dispute" (6.1 min/view), "somaliland" (5.0), "guatemala history" (4.9), "history of belize" (4.9).
- [ ] **Untapped keywords** — Check if traffic-driving terms are missing from title. Top opportunities: scholar names (e.g., "ervand abrahamian"), country-specific terms (e.g., "selknam"), and "history of [country]" formulations.
- [ ] **Cross-video bridging terms for playlists** — These terms appear across 2+ videos and indicate audience overlap. Use for playlist grouping and end-screen links:
  - "belize" (72 views, 2 videos, 3.3 min/view)
  - "guatemala" (9 views, 2 videos, 2.4 min/view)
  - "ervand abrahamian" (5 views, 2 videos, 2.8 min/view)
  - "greece vs turkey" (2 views, 2 videos, 4.5 min/view)

---

## Pre-Publish Final Check

- [ ] Title scored by title_scorer.py (score displayed)
- [ ] Thumbnail passes thumbnail_checker.py
- [ ] Description first line is compelling
- [ ] Publishing day is Monday-Thursday (never Friday)
- [ ] Optimal time: 9-11 AM EST
