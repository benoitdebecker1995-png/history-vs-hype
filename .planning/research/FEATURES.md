# Feature Landscape: v7.0 Packaging and Hooks Overhaul

**Domain:** YouTube edu/history packaging tools — title scoring, hook generation, metadata optimization
**Focus:** What actually drives clicks and retention on edu/history channels, grounded in 500K-5M sub competitor patterns and own channel data
**Researched:** 2026-03-16
**Confidence:** HIGH (own-channel data n=47 videos, n=870 competitor videos in intel.db, n=17 hook-retention correlations)

---

## Context: The Core Problem This Milestone Solves

The existing title_scorer.py scores against the channel's own CTR data. With only 3 videos ever breaking 2K views and most videos getting under 3K impressions, the self-referential loop is the problem: high scores get awarded to patterns that "beat" a 2% baseline. The new system must be grounded in what works for edu/history channels at scale (Kraut 604K, Knowing Better 952K, Shaun 760K, Fall of Civilizations 1.5M, Historia Civilis 1.1M) and in proven patterns from this channel's own top performers.

---

## Table Stakes

Features users (solo creator) expect from a packaging toolset. Missing = the toolset is not better than what already exists.

| Feature | Why Expected | Complexity | Existing State |
|---------|--------------|------------|----------------|
| Title generation grounded in competitor patterns | Without external reference, tool re-learns bad habits from own low-CTR data | Med | title_scorer.py uses own-channel CTR only |
| Hard-reject enforcement for proven anti-patterns | Year (-46%), colon (-28%), "The X That Y" (1.2% CTR) are measured — must auto-reject | Low | Implemented in PACKAGING_MANDATE but needs tighter tool enforcement |
| Hook generation with human-conflict framing | 9.46% CTR vs 1.1% CTR difference = human conflict titles win; tool must know this | Med | Rule 19 exists but not grounded in competitor data |
| Metadata description template with keyword-first structure | First 2 lines of description are search-indexed; template must enforce this | Low | METADATA-CHECKLIST.md exists as manual reference only |
| Thumbnail concept output per video type | Map-first policy is validated (territorial dispute channel needs visual contrast) | Low | thumbnail_checker.py validates but doesn't generate concepts |
| Title scored against 3%+ CTR target (not own-channel baseline) | Channel baseline is ~2.7%; scoring against it rewards mediocrity | Med | title_scorer.py score = min(100, max(0, int(ctr_percent * 17))) — maps own CTR |
| Hook variant generation with at least 3 hook styles | cold_fact, myth-contradiction, and fact-check hooks cover the channel's content types | Med | --variants flag exists; quality needs grounding in hook-retention data |

---

## Differentiators

Features that set the v7.0 toolset apart from generic YouTube packaging advice.

| Feature | Value Proposition | Complexity | Notes |
|---------|-------------------|------------|-------|
| Hook scorer that checks the 5-second title-fulfillment rule | The "2% dropout" (15-30% of viewers lost in first 5 seconds) is a thumbnail-title mismatch problem — hook must immediately deliver on what title promised | Med | Unique to this channel's discovery; no generic tool checks this |
| Competitor-anchored title scoring using extracted formulas | Score new titles against Kraut/Knowing Better/Shaun/Johnny Harris patterns at matched sub tiers, not own low-CTR history | High | Requires building or importing competitor formula weights |
| Content-grounded title generation (script → title) | Top titles are derived from the specific document/number/contradiction in the script — "Britain Sold Kashmir for 7.5 Million Rupees" not generic "Kashmir Explained" | Med | THUMBNAIL-REFRESH-PLAN shows this pattern; tool must read script |
| Hook quality scorer with 4-beat completeness check | Rule 19 exists but no automated checker verifies: cold_fact present? myth present? contradiction present? payoff present? | Low-Med | Straightforward regex/Claude check against 4-beat structure |
| "Versus" title detector and recommender | Versus pattern (~3.7% CTR) is underused; tool should flag when topic has two competing entities and hasn't generated a versus variant | Low | Simple logic: does topic have two named entities? suggest versus |
| Metadata bundle coherence check | Title + thumbnail concept + description must all reference the same hook element (the specific number, document, or contradiction) | Med | Currently no check for title/thumbnail/description alignment |
| Topic-type CTR benchmark calibration | Territorial dispute titles need 3%+ target; political fact-check titles can aim for 5%+ (JD Vance baseline); tool should know the difference | Med | Channel data supports segmentation: political 9.46%, territorial 3.1-4.3% |
| Self-referential loop detector | Flags when scoring is based on fewer than N=5 examples of a pattern, forcing fallback to competitor benchmarks | Low | Prevents the core v6.0 problem from re-emerging |

---

## Anti-Features

Features that seem useful but would waste build time or actively hurt output quality.

| Anti-Feature | Why Avoid | What to Do Instead |
|--------------|-----------|-------------------|
| A/B thumbnail testing framework | YouTube's A/B tool requires 10K+ views per video; channel gets 100-500 views; any A/B result is noise | Document the 3-thumbnail concept rule; manually swap after 48h if CTR <3% |
| CTR prediction ML model trained on own channel | 48 videos is nowhere near enough for reliable ML; will overfit to noise | Use rule-based scoring against known competitor patterns + hard reject rules |
| Automated thumbnail creation / Photoshop scripting | Solo creator already uses Photoshop; automation adds fragility without much time savings | Improve concept generation quality — better briefs = better manual execution |
| "Optimize for engagement rate" scoring | High engagement + low views = niche passion audience YouTube can't place; engagement rate is vanity for a 475-sub channel | Optimize for CTR and impressions signals only |
| Generic YouTube algorithm tips in tool output | "Use cards! Add an end screen! Upload at 3pm!" is noise at this channel's scale | Surface only channel-specific, data-backed rules |
| Retroactive title A/B testing on all 48 videos simultaneously | Retitling all 48 at once destroys the ability to measure what worked | Prioritize top 10 by wasted impressions; swap 1-2 per week; measure each |
| Hook length optimization below 30 seconds | Hook quality is about structure (cold_fact → myth → contradiction → payoff), not word count | Keep Rule 19 4-beat structure as the constraint; don't add word-count targets |
| Description hashtag optimization | YouTube's own guidance and channel data both show hashtags in description first 3 lines waste prime keyword real estate | Keep hashtag field separate; first 3 description lines = keywords + hook |

---

## Feature Dependencies

Dependencies on existing shipped features and on each other.

```
EXISTING (v6.0 shipped):
  title_scorer.py          ← v7.0 must extend, not replace
  PACKAGING_MANDATE.md     ← source of hard-reject rules
  thumbnail_checker.py     ← validates but doesn't generate
  /publish --titles        ← entry point for new title generation
  keywords.db              ← stores CTR history; self-referential loop lives here
  CROSS-VIDEO-SYNTHESIS.md ← source of per-pattern CTR averages (n=35+)
  HOOK-RETENTION-CORRELATION.md ← 17-video hook style data
  COMPETITOR-TITLE-DATABASE.md  ← 870 competitor videos with formulas
  intel.db                 ← competitor data store
  Rule 19 (OPENING-HOOK-TEMPLATES.md) ← 4-beat formula, 6 templates

NEW FEATURES (v7.0) — internal dependencies:
  Competitor benchmark weights → Title scorer upgrade (needed first)
  Title scorer upgrade → Hook quality scorer (shares scoring logic)
  Hook quality scorer → Hook generator upgrade (generates what scorer will accept)
  Script-grounded title extraction → Content-grounded title generation
  All above → /publish --titles output quality improvement
```

---

## MVP Recommendation

The channel's bottleneck is not missing features — it's that existing features score against the wrong benchmark. The MVP is a targeted upgrade to what exists, not new modules.

**Prioritize:**
1. **Competitor-anchored title scoring** — Replace the self-referential CTR scoring with external benchmarks. The scoring formula `min(100, max(0, int(ctr_percent * 17)))` maps own CTR which peaks at 9.46% (1 video). Replace with a formula that anchors 4% CTR = "passing" based on competitor norms for edu/history channels, with a minimum floor of 65/100 for anything below 4%.
2. **Content-grounded title generation** — When `/publish --titles` runs, it must read the script and extract: the specific number, document name, and contradiction/claim. These become the raw material for titles. "Britain Sold Kashmir for 7.5 Million Rupees" comes from reading the script, not from generic templates.
3. **Hook quality scorer** — A light automated check that verifies Rule 19 4-beat structure is present (cold_fact + myth + contradiction + payoff) and that the hook's first sentence matches the title's promise. Catches the "thumbnail-mismatch dropout" problem before filming.
4. **Versus title recommender** — When a topic involves two named entities (countries, political figures, ideologies), automatically generate a versus variant as one of the title candidates. Versus is underused relative to its measured CTR advantage.

**Defer:**
- Full competitor formula library ingestion: medium complexity, low urgency once external benchmark anchoring is in the scorer
- Metadata bundle coherence check: useful but manual review is adequate until enough videos are produced under the new system
- Topic-type CTR benchmark segmentation: implement as phase 2 once the baseline competitor-anchored scoring is working

---

## Detailed Feature Analysis by Domain

### Domain 1: Title Generation and Scoring

**What competitor data shows:**
- The edu/history channels at 500K-5M subs use these dominant title structures (from 870-video intel.db): "other" (55.2%), "how_why" (24.1%), "colon_split" (13.3%). "Other" and "how_why" are the high performers.
- Kraut's 604K subs top videos: "Trump's Biggest Failure" (4M), "How Mexico Got So Violent" (2M) — direct active language, short, no colons
- Knowing Better's top videos: "[Claim], Actually" (2M), "[Subject] Was Worse Than You Thought" (1.5M) — direct thesis statement
- Shaun's top: "The Bell Curve" (3.7M, single title) — minimalist when brand is established; before brand: "[Entity] Lies to You", "[Claim] Isn't Real"
- Johnny Harris: "The REAL Reason [Event]" (5M+) — escalation word + causal explanation
- Channel's own data: versus and declarative outperform colon and question in measured CTR

**What the existing tool gets wrong:**
- Scores 3.8% CTR as 64/100 — this is the *channel's own* 3.8% average, but 3.8% is already good relative to edu/history norms. The tool penalizes anything under 3.8% rather than rewarding anything above it.
- No awareness of competitor pattern norms — a Knowing Better-style "[Claim], Actually" title would score poorly because the channel's own data has no examples of this pattern
- The tool cannot generate titles from script content — it only scores what you bring to it

**Required improvements:**
- Anchor "passing" score (65/100) to 4% CTR based on competitor norms, not own-channel baseline
- Build title generation into `/publish --titles` that reads the script for: specific number, named document, active conflict entity A vs entity B, claim being debunked
- Add 8+ title patterns from competitor data as scored formulas: versus, declarative, "[Claim] Actually", "[Person] vs [Topic]", "How [Entity] [Verb]ed", "The [Specific Number] That [Verb]"
- Hard reject patterns already validated: year (-46%), colon (-28%), "The X That Y" (1.2%), question (-36%)

### Domain 2: Hook Generation

**What the data shows:**
- Best hooks by retention: cold_fact (28.2% avg, n=11) and myth-contradiction (29.3% avg, n=2) — both outperform document-first (23.9%) and pure context (28.2%)
- Top 2 hooks by retention both open with: specific concrete claim + modern urgency + methodology promise. All within first 25 seconds.
- The 2% dropout (average 17.1% of viewers lost in first 10-30 seconds across 31 videos) is a title-promise fulfillment problem: viewer clicked on a title, then did NOT see that thing immediately
- Specific failure mode: "I read this document" (document-first) without first establishing stakes = Flat Earth video (11.57% retention, the worst in the dataset)
- Competitor patterns from Knowing Better, Shaun, Johnny Harris: all use a "myth then contradiction" structure with a specific named authority being wrong, not abstract general claims
- Rule 19 4-beat structure (cold_fact → myth → contradiction → payoff) already encodes the right pattern; the problem is generation quality and the lack of an automated check

**What the tool needs:**
- Hook generation that outputs per-video (reads the script): what is the strongest cold_fact (specific number or date), what is the myth the video debunks, what is the contradiction (the document or evidence), what is the payoff preview
- Automated 4-beat completeness check: does generated hook have all four beats? Does the first sentence match what the title promised?
- Hook style recommendation based on topic type: territorial disputes = cold_fact preferred; ideological myth-busting = myth-contradiction preferred; political fact-check = cold_fact (specific claim + source) preferred
- One additional hook style currently unimplemented: "authority stack" (multiple credible sources all believe the myth → I checked them all → they're all wrong). This is the Sykes-Picot video's highest-retention structure.

### Domain 3: Metadata (Description and Tags)

**What works:**
- 71.5% of channel views come from Browse/Home Feed — this is the algorithm promoting the video based on title + thumbnail + early performance signals. SEO tags are NOT the primary driver.
- YouTube Search accounts for 3.5% of views — tags matter for long-tail discovery but are secondary to browse performance
- Description first 2 lines are indexed for search; they must be keyword-dense AND compelling as standalone text (they show in search snippets)
- Channel's best descriptions include: the specific document examined, the specific claim debunked, and a "why this matters" modern relevance line

**What the tool needs:**
- Description template that enforces: keyword-rich first sentence + specific document/claim named + source citations block + timestamps
- Tags generated from: topic keywords + document names + named entities from script (people, places, treaties) + related search terms — 15-20 tags
- Publish timing gate already exists (Monday best day per channel data); reinforce in tool output

### Domain 4: Thumbnail Concept Generation

**What competitor data shows:**
- RealLifeLore (7.8M): map-focused thumbnails with colored geographic areas + bold stat — territory shown as visual conflict
- Wendover (4.9M): infographic/diagram style — system shown as visual
- Johnny Harris: face + location graphic (requires established personal brand; not the strategy here)
- Kraut: countryball characters + flags (requires animation capability; not viable)
- Channel's own data: map/mixed thumbnails avg 1.7x more views than document-only (n=4 vs n=4, LOW confidence but directional); no text overlay (3.3% CTR) vs text overlay (2.0% CTR); no face (3.3%) vs face (1.9%)
- THUMBNAIL-REFRESH-PLAN shows the best thumbnail concepts come from reading the script: the Kashmir thumbnail uses the Treaty of Amritsar price; the Peru thumbnail uses the 1503 papal bull; the Dark Ages thumbnail uses the illuminated manuscript

**What the tool needs:**
- Thumbnail concept generation reads the script for: the strongest visual document/map/evidence element, the two-entity conflict, the specific number or shocking detail
- Output: 3 concepts following the A/B/C template (A = split-map conflict, B = document-on-map, C = geographic context + evidence fragment)
- Each concept includes: main visual element, color palette (two distinct colors for the two sides), what specifically to show, what NOT to include (text, face, stock imagery)
- Phone-size readability test prompt: does the concept work at 160x90px without text?

---

## Feature Complexity Summary

| Feature | Complexity | Build Effort | Dependency |
|---------|------------|-------------|------------|
| Competitor-anchored title scorer | Med | 2-3 days | Competitor formula extraction |
| Content-grounded title generation (script reader) | Med | 2-3 days | Script parsing logic |
| Hook quality scorer (4-beat completeness) | Low-Med | 1-2 days | Rule 19 structure reference |
| Versus title recommender | Low | 0.5 days | NER on topic entities |
| Hook style recommender by topic type | Low | 0.5 days | Topic classification already exists |
| Thumbnail concept generator (script-grounded) | Med | 1-2 days | Script parsing logic (shared with title gen) |
| Metadata description template with enforcement | Low | 0.5 days | Existing METADATA-CHECKLIST |
| Self-referential loop detector | Low | 0.5 days | keywords.db query + n-count check |
| Topic-type CTR benchmark segmentation | Med | 1-2 days | CROSS-VIDEO-SYNTHESIS data |

---

## Sources and Confidence Levels

| Finding | Source | Confidence | Notes |
|---------|--------|------------|-------|
| Year penalty -46% CTR | channel-data/PACKAGING_MANDATE.md, n=6 vs n=27 | HIGH | Measured from own channel data, large enough sample |
| Colon penalty -28% CTR | channel-data/PACKAGING_MANDATE.md, n=9 vs n=26 | HIGH | Measured, reliable |
| Versus pattern 3.7% avg CTR | PACKAGING_MANDATE.md, n=2 | MEDIUM | Small sample; directional; matches competitor usage |
| Declarative pattern 3.8% avg CTR | PACKAGING_MANDATE.md, n=19 | HIGH | Largest sample, most reliable |
| cold_fact hook 28.2% avg retention | HOOK-RETENTION-CORRELATION.md, n=11 | MEDIUM | Small sample; directional |
| myth-contradiction hook 29.3% avg retention | HOOK-RETENTION-CORRELATION.md, n=2 | LOW-MEDIUM | Very small sample; consistent with theory |
| 71.5% views from Browse/Home Feed | channel-insights.md, n=47 videos | HIGH | Full channel dataset |
| 2% dropout = 17.1% avg viewer loss | CROSS-VIDEO-SYNTHESIS.md, n=31 | HIGH | Large sample, consistent |
| "Other" title pattern 55.2% of competitor videos | youtube-intelligence.md, n=870 | HIGH | Large sample from intel.db |
| Map/mixed thumbnails 1.7x views over document | TITLE-PATTERNS.md, n=4 vs n=4 | LOW | Tiny sample; use for direction only |
| No text overlay 3.3% CTR vs 2.0% | TITLE-PATTERNS.md, n=29 vs n=6 | MEDIUM | Decent sample |
| Competitor CTR norms 4-10% typical | youtube-intelligence.md (YouTube Creator Academy source) | HIGH | Official source |

---

*Researched: 2026-03-16 for v7.0 Packaging and Hooks Overhaul*
*Source priority: Channel own-data (HIGH) > Intel.db competitor data (MEDIUM-HIGH) > Training knowledge of competitor channels (MEDIUM)*
