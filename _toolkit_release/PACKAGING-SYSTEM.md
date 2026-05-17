# THE HISTORY YOUTUBE PACKAGING SYSTEM

### How a 515-Sub History Channel Grew 173% in 90 Days by Packaging Better, Not Working Harder

*A reverse-engineered methodology with measured CTR data, hard-rejection rules, and the actual Python scripts behind it.*

---

## Read This First

If you run a history, geopolitics, or fact-checking YouTube channel under 50K subs, you have one bottleneck. It is **not** content quality. It is **not** upload frequency. It is **not** SEO.

It is **packaging**: title, thumbnail, hook. The 8-second decision YouTube viewers make on the home page or in the suggested sidebar.

This guide documents the packaging system that took a niche history channel from **169 subs (Nov 2025) to 462+ subs (Feb 2026)** — a **173% growth rate in 90 days**, in a niche where most channels plateau under 1,000.

Across **47 long-form videos** with measured CTR data, this system identifies:

- Three hard-reject patterns that cost you 28-46% of CTR every time you use them
- Six bonus signals that the top-CTR videos all share
- A 48-hour swap protocol that converts dying videos into climbing ones
- The exact `PATTERN_SCORES` calibration with sample sizes and confidence levels

You'll also get the five Python scripts that automate this — but the scripts are the cheap part. The thinking is the expensive part. Read the methodology first. Use the scripts as reference. Calibrate to your own channel as your own CTR data accumulates.

---

## TABLE OF CONTENTS

1. The One Mental Model — Why Packaging Is Everything
2. The Six Title Patterns — Ranked by Measured CTR
3. The Three Hard Rejects — Patterns That Cost 28-46% CTR
4. The Six Bonus Signals — What Top-CTR Titles All Share
5. The 48-Hour Swap Protocol — Save Dying Videos
6. The Retitle Decision Tree — When to Redo, When to Move On
7. The Thumbnail Companion Rules — Niche-Specific Findings
8. Calibrating to Your Channel — How to Build Your Own PATTERN_SCORES
9. Appendix A: The Python Scripts (with annotations)
10. Appendix B: Worked Examples — 12 Real Titles Scored
11. Appendix C: 50-Title Pre-Flight Checklist

---

## 1. THE ONE MENTAL MODEL

The most important sentence in this guide:

> **Packaging is the price of admission. Content is the experience inside the gate. If the price is too high, no one finds out the experience is great.**

For a niche history channel, content quality is over-supplied — there are dozens of well-researched channels with low view counts because their titles and thumbnails fail the home-page audit. YouTube's algorithm runs an experiment every time it suggests your video: it shows your thumbnail to ~500 viewers and measures click-through. Below 2% CTR, the experiment ends and your video is dead.

You have **2% CTR or 18 months of stagnation**. That's the binary. This guide exists to keep you above 2%.

**The data behind every claim in this guide:**

- 47 long-form videos with measured CTR (12 months of data)
- 33 videos with paired CTR + impression data (the calibration set)
- 388 competitor titles in the same niche (geopolitics + history + fact-checking)
- 650 competitor thumbnails analyzed for visual patterns
- 4 retitle experiments with before/after CTR delta

When a number appears in this guide without a sample size in parentheses, it's from the n=33 calibration set. When you see "(n=X)", read X carefully. Small-n claims are directional, not gospel.

---

## 2. THE SIX TITLE PATTERNS — RANKED BY MEASURED CTR

There are exactly six structural patterns YouTube history titles fall into. They are not aesthetic preferences. They are measurable categories with measurable CTR ceilings.

### Pattern Tier List (with confidence levels)

| Tier | Pattern | Avg CTR | Sample Size | Confidence | When to Use |
|------|---------|---------|-------------|------------|-------------|
| S    | versus  | ~3.7% | n=4 (n=2 verified) | MEDIUM | Bilateral disputes, two-sided debates |
| A    | declarative | 3.8% | **n=19** | **HIGHEST** | Default for everything else |
| B    | how_why | 3.3% | n=5 | MEDIUM | Mechanism explanations |
| C    | question | 2.4% | n=1 | LOW (single video!) | Almost never |
| D    | colon | 2.3% | n=4+ | HIGH (penalty confirmed) | Never as "Topic: Subtitle" |
| F    | the_x_that | ~1.2% | n=0 (all retitled away) | HIGH | Rewrite immediately |

**The biggest finding from this calibration:** the *declarative* pattern has the largest sample (n=19) and is the most reliable. If you can't decide, declarative is the safest default.

### How to Detect Each Pattern (the regex layer)

The Python tool detects patterns in this order (first match wins):

```python
# 1. versus — "X vs Y", "X versus Y"
re.search(r'\bvs\.?\b|\bversus\b', title.lower())

# 2. the_x_that — "The [1-3 words] That [Verb]"
re.search(r'^the\s+(?:\w+\s+){0,2}\w+\s+that\s+', title.lower())

# 3. colon — any colon present
':' in title

# 4. question — ends with ?
title.strip().endswith('?')

# 5. how_why — starts with how/why
re.search(r'^(how|why)\b', title.lower())

# 6. declarative — fallback default
```

Order matters. "How Spain vs Portugal Divided the World" detects as **versus** (first match), not how_why. This is correct because the versus framing dominates the click decision.

### Why Each Tier Performs the Way It Does

**S-tier (versus):** Activates conflict primitives. The brain reads "X vs Y" and *expects* drama. If the topic is bilateral, this is your highest-CTR option. If you force it onto a non-bilateral topic, it backfires.

**A-tier (declarative):** Maximum reliability because it makes one promise and keeps it. "France Forced Haiti to Pay for Its Own Freedom" is a complete sentence with a clear subject, verb, and stake. Boring? No — boring is "What France Did to Haiti" (vague verb) or "France and Haiti's Complicated History" (no verb).

**B-tier (how_why):** Useful for mechanism content but requires the audience to *want* the explanation. Lower top-end ceiling because curiosity is asymmetric — viewers click "how" titles less than declarative ones, but if they click, retention is higher.

**C-tier (question):** The ?-ending pattern underperforms because it makes the *viewer* do the cognitive work of "do I want to know the answer?" — a friction step. Single datapoint in this calibration set, but the pattern matches across competitor data.

**D-tier (colon):** Treated as a hard reject in most contexts (see Section 3) because "Topic: Subtitle" reads as documentary-style and signals "long, dry, academic." YouTube CTR drops 28%.

**F-tier (the_x_that):** Worst pattern in measured history-channel data. Every title with this pattern in the original data set was eventually retitled away. Estimated 1.2% CTR — below the algorithm-survival threshold.

---

## 3. THE THREE HARD REJECTS

Three patterns are so reliably toxic that the scoring system flags them as **HARD REJECT** — meaning the score gets capped regardless of other factors.

### Hard Reject 1: YEAR AS TOPIC LABEL — Costs 46% CTR

A 4-digit year used as the framing of the title destroys CTR.

**Reject examples:**
- "The 1494 Line: Spain and Portugal's Treaty"
- "Iran 1979: The Hostage Crisis"
- "1492: How Columbus Landed"

**Acceptable hook usage (mild penalty only):**
- "Flat Earth Was Invented in 1828" (year as hook, not topic)
- "Banned for 200 Years"
- "Since 1953"

The **detection rule** for hook usage:

```python
hook_patterns = [
    r'(?:invented|created|started|began|built|written|signed|passed|founded)\s+in\s+\d{4}',
    r'(?:since|from|after|before|until)\s+\d{4}',
    r'\d+-year-old',
    r'for\s+\d+\s+years?',
    r'\d+\s+years?\s+(?:of|ago|later|old)',
]
```

If the year matches one of these patterns, use a -10 penalty. If it doesn't, hard-reject (-50).

**Calibration sample:** 5 titles with years vs 30 without. Years averaged **45.6% lower CTR**. This is one of the highest-confidence findings in the data set.

**Why:** Years signal "history class" to the casual viewer. Even a viewer interested in history avoids titles that look like textbook chapters. Move the year to the description.

### Hard Reject 2: COLON AS "TOPIC: SUBTITLE" — Costs 28% CTR

The single character `:` triggers a 28% CTR penalty when used in the structure "Topic: Subtitle" or "Word: Explanation."

**Reject examples:**
- "Operation Condor: The CIA's Secret War"
- "The Crusades: A Forgotten Reality"
- "Tordesillas: How Spain Won Half the World"

**Acceptable colon usage (reduced -10 penalty):**
- "Venezuela vs Guyana: Who Owns Essequibo?" (colon after versus = stakes framing)

The **detection rule** for the acceptable case:

```python
def _colon_is_versus_stakes(title):
    colon_pos = title.find(':')
    if colon_pos < 0: return False
    before_colon = title[:colon_pos].lower()
    return bool(re.search(r'\bvs\.?\b|\bversus\b', before_colon))
```

If the colon comes *after* a versus matchup, it serves a different function — it's stating the stakes of the conflict. That's tolerable.

**The fix:** Replace colons with em-dash (—), period, or just delete them. Compare:
- BAD: "Operation Condor: The CIA's Secret War" (colon)
- GOOD: "Operation Condor — The CIA's Secret War in Latin America" (em-dash)
- BETTER: "The CIA Ran a Death Squad Network in Latin America" (declarative, no colon, evidence promise)

**Why:** Colons signal documentary or academic content. They look like the spine of a Penguin Classics paperback. Casual viewers — even intellectual ones — interpret this as "long, dry, requires effort" and click something else.

### Hard Reject 3: THE X THAT Y PATTERN — ~1.2% CTR

The pattern "The [Noun] That [Verb-ed Something]" is the worst-performing pattern in measured history-channel data.

**Reject examples:**
- "The Country That Disappeared"
- "The Treaty That Divided the World"
- "The Empire That Collapsed Overnight"

This pattern survived in BuzzFeed and listicle culture and bled into YouTube history. It's a curiosity gap with no anchor — viewers can't tell what they're getting.

**The fix:** Replace with declarative or versus framing. Compare:
- BAD: "The Country That Might Disappear: Guatemala vs Belize" (the_x_that + colon)
- GOOD: "The Country That Might Disappear" → rewritten to "Guatemala Could Annex Half of Belize. Here's How."

For reference, a real channel had "The Country That Might Disappear: Guatemala vs Belize" as its top video at 28.8K views and 7.6% CTR. The salvaging factor was the versus framing carrying it. **Imagine the ceiling without the the_x_that drag.**

---

## 4. THE SIX BONUS SIGNALS — WHAT TOP-CTR TITLES ALL SHARE

Six measurable signals correlate with above-niche-median CTR. Apply them when the base pattern is sound.

### Bonus 1: EVIDENCE PROMISE (+10 score, top channel signal)

The single strongest CTR signal in this calibration set.

**Trigger phrases:**
- "here's"
- "the evidence"
- "the proof"
- "the documents"
- "documents prove"
- "documents show"
- "primary source"
- "the receipt", "every receipt"
- "we found", "we read"
- "the original", "the actual"
- "word for word"

**Top-CTR title in calibration set:** "JD Vance Claims Christians Found Child Sacrifice. Here's the Evidence." → **9.5% CTR.**

This signal works because intellectual male 25-44 viewers (the dominant history-channel demographic) are *evidence-oriented*. They distrust narrative claims and respond to titles that promise verification.

If your channel does primary-source work, every title should consider an evidence-promise variant.

### Bonus 2: NAMED ENTITY (+5 score)

Titles that name specific countries, leaders, or organizations get more impressions than abstract titles. The algorithm uses the named entity to identify viewer interest.

**Examples that trigger:**
- "France vs Haiti" (two named countries)
- "Trump Walks Back Christian Sacrifice Claim" (named leader)
- "NATO's Forgotten Article" (named org)

**Examples that don't:**
- "The Empire's Forgotten Tax" (no named entity)
- "How a Treaty Divided Half the World" (no named entity)

The named-entity bonus stacks with versus pattern detection. "Spain vs Portugal" gets pattern bonus + entity bonus.

### Bonus 3: CONTROVERSY / MYTH-BUSTING FRAME (+5 score)

Accusation framing creates tension and drives clicks.

**Trigger words:**
- myth, lie, fake, hoax
- claims, claim
- debunk, destroy
- narrative, propaganda
- secret, hidden
- nobody (as in "Nobody Tells You")
- sacrifice, walked back, phantom, illegal

**Top-CTR examples in calibration:**
- "Started With a Lie" (5.1% CTR)
- "Destroy the Narrative" (5.4% CTR)
- "Weaponized Palestine" (5.5% CTR)

The danger: don't confuse controversy framing with **clickbait**. The titles above all delivered on their promise in the video. Clickbait promises and doesn't deliver — eventually penalized by retention drops.

### Bonus 4: SCALE WORD (+5 score, 1.33x outlier lift)

Words that imply massive scope correlate with outlier performance across 650 competitor videos.

**Scale words:**
- every, all, entire, whole
- century, centuries, forever
- million, billion, thousand
- empire, world, continent, civilization
- generation, generations

**Why this works:** Scale signals stakes. "How Spain Conquered the World" outperforms "How Spain Conquered Mexico" not because Mexico is uninteresting but because *world* signals greater consequence.

### Bonus 5: TWO-SENTENCE FORMULA (+5 score, 11% outlier rate)

The strongest *structural* pattern across 650 competitor videos. Titles with two sentences (period in the middle) hit outlier status (3x channel average) at 11% — the highest rate of any structural feature.

**Examples:**
- "JD Vance Claims Christians Found Child Sacrifice. Here's the Evidence."
- "France Forced Haiti to Pay. The Receipts Are 200 Years Old."
- "The Documents Were Just Released. They Prove Operation Condor Was American."

**Detection regex:**

```python
# Three+ lowercase chars before period (excludes "Dr.", "St.", "vs.")
re.search(r'(?<=[a-z]{3})\.\s+[A-Z]', title)
```

**Why this works:** Two sentences = setup + payoff. The first sentence creates a question; the second promises an answer. The brain processes this as a complete narrative arc, not a fragment.

### Bonus 6: SPECIFIC NUMBER (+10 score)

Numbers that aren't years or vague duration adjectives.

**Triggers:**
- "5 Myths About the Crusades"
- "122 Years of French Extraction From Haiti"
- "The 47 Articles of the Treaty That Most People Never Read"

**Excluded (no bonus):**
- "200-Year-Old Lie" (duration-as-adjective is a vague scale marker)
- "1492" (year, see Hard Reject 1)

**Detection logic:**

```python
def has_specific_number(title):
    no_years = re.sub(r'\b(1[0-9]{3}|20[0-2][0-9])\b', '', title)
    no_duration_adj = re.sub(r'\b\d+-[Yy]ear-?\w*', '', no_years)
    return bool(re.search(r'\b\d+\b', no_duration_adj))
```

---

## 5. THE 48-HOUR SWAP PROTOCOL — SAVE DYING VIDEOS

Every video has 48 hours to prove it can survive YouTube's algorithm test. After 48 hours and 500+ impressions, the data is statistically reliable enough to act on.

### The Three-Threshold Decision

| 48h CTR | Action | Why |
|---------|--------|-----|
| **< 2%** | **SWAP TITLE + THUMBNAIL** | Both elements are failing. Algorithm is killing the video. Full reset. |
| **2-4%** | **SWAP TITLE ONLY** | Title is the bottleneck. Thumbnail is doing its job (impressions are coming) but title isn't converting. |
| **> 4%** | **HOLD STEADY** | Above niche median. Don't touch. Let it run. |

The threshold for action is **500+ impressions**. Below that, CTR is statistically noisy.

### Why 48 Hours Specifically

YouTube's algorithm makes its decision about video viability in the first 48-72 hours. If CTR is below niche threshold during that window, the video gets demoted in suggestions and the long-tail dies. If you swap during the demotion phase, you can sometimes recover. After the demotion phase, swaps rarely revive a dead video — but they can boost retention for users who arrive via search.

### The High-Retention-Low-Views Edge Case

Sometimes a video has good retention (>30%) but few views (<100). This is a **packaging problem, not a content problem**. The viewers who *do* find it stay, but not enough are clicking.

**Action:** Retitle. The content is sound. The packaging is dead-on-arrival.

**Detection rule:**

```python
if retention > 30 and views < 100 and ctr > 0 and ctr < 3:
    flag_as_retitle_candidate = True
```

These are your highest-leverage interventions. A 30%+ retention video with bad packaging is *always* worth a retitle attempt. You're not gambling — you know the content works.

---

## 6. THE RETITLE DECISION TREE

Not every underperforming video deserves a retitle. Cost (your time) vs benefit (likely view recovery) matters.

### Step 1: Is the video <30 days old?

- **YES** → Continue to Step 2.
- **NO** → Don't retitle unless retention is >40%. Old videos rarely recover. Spend the time on the next upload.

### Step 2: Is retention >25%?

- **YES** → Retitle is worth attempting. Continue to Step 3.
- **NO** → Don't retitle. Content quality is the issue. Lessons-learned for next time.

### Step 3: What's the current pattern?

| Current Pattern | Retitle Strategy |
|-----------------|------------------|
| declarative | Try versus framing if topic has two sides; or add evidence promise. |
| how_why | Convert to declarative two-sentence ("Statement. Evidence promise."). |
| versus | Try declarative with controversy frame ("X Claims Y. Documents Say Otherwise."). |
| colon | Remove colon, replace with em-dash or split into two sentences. |
| question | Convert to declarative. Questions consistently underperform. |
| the_x_that | Complete rewrite. This pattern cannot be salvaged. |

### Step 4: Score the new candidate

Run it through the title scoring system. Reject if it scores below 60 in your topic category.

### Step 5: Do not retitle more than twice

If two retitles haven't moved the needle, the video is dead. Stop sinking time. The algorithm has decided.

---

## 7. THE THUMBNAIL COMPANION RULES

A title without a matching thumbnail wastes the title's signal. Six niche-specific findings from analyzing **650 competitor thumbnails**:

1. **Text overlay is mandatory.** 87% of high-performing thumbnails in history/geopolitics niches use 2-4 word text overlays. Not the full title — a separate hook phrase.
2. **Faces underperform.** 0% of niche outliers used a face as the dominant element. (This is niche-specific — it's the opposite for vlogs.)
3. **Maps work for territorial.** Topics about borders, disputes, or geographic claims should use a map-based composition. CTR lift averaged 1.7x in this calibration.
4. **High-contrast colors only.** Yellow, red, white text on dark backgrounds. Pastels and gradients underperform on mobile (where 60-70% of clicks come from).
5. **One focal element.** Two competing visual elements split attention and drop CTR. Pick the one strongest visual.
6. **Match the title's emotional register.** Controversy-framed titles need controversy thumbnails. Mismatch kills CTR.

---

## 8. CALIBRATING TO YOUR CHANNEL

The PATTERN_SCORES in this guide are calibrated to one specific history channel. Yours will differ — likely 5-15 percentage points up or down per pattern.

### The 90-Day Calibration Plan

**Days 1-30: Gather baseline.**

For each existing video, log: title, pattern (use the regex detection), measured CTR after 30 days, impression count.

**Days 31-60: Identify your channel's strongest pattern.**

Compute average CTR per pattern *for your channel*. The top 1-2 patterns are your "house style." Use them as defaults.

**Days 61-90: Test the hard rejects.**

Don't trust this guide blindly — test it. Publish one video with a known-bad pattern (e.g., a colon title) alongside videos with optimal patterns. Compare CTR. The penalty *should* match this guide's findings within 5 percentage points. If not, your audience may have different preferences.

### How to Update PATTERN_SCORES

Once you have 5+ data points per pattern, you can compute:

```
your_pattern_score = (your_avg_ctr_for_pattern / your_avg_ctr_overall) * 50
```

This rescales the pattern's CTR to a 0-100 score relative to your channel's median performance.

A pattern at 1.5x your median = score of 75. A pattern at 0.5x = score of 25.

---

## 9. APPENDIX A: THE PYTHON SCRIPTS

Five scripts ship with this guide:

1. **`title_scorer.py`** — Score a title 0-100 against the rules in this guide.
2. **`packaging_autopilot.py`** — Run the 48h swap check on your recent videos.
3. **`article_scorer.py`** — Same logic, applied to newsletter article subject lines and structure.
4. **`subject_line_scorer.py`** — Email-specific subject line grader.
5. **`retitle_gen.py`** — Auto-generate retitle candidates from a video's opening hook.

**Important calibration warning:** These scripts come hardcoded with one channel's CTR data. They are useful as **reference implementations** — read the code, see how each rule maps to a function, then either:

(a) Replace the `PATTERN_SCORES` dict with your own values once you have 30+ days of data, OR
(b) Treat the scores as relative grades, not absolute predictions, until you've calibrated.

The dependencies (`benchmark_store`, `keywords.db`, `analytics.db`) are channel-specific data layers. Strip them out by setting `db_path=None` in `score_title()`. You'll get the static-mode score, which is exactly the methodology in this guide expressed as code.

See `scripts/README.md` for run instructions.

---

## 10. APPENDIX B: 12 WORKED EXAMPLES

Each example shows the title, score, breakdown, and what was done.

### Example 1: The 28K-View Outlier (kept as-is)

**Title:** "The Country That Might Disappear: Guatemala vs Belize"

- Pattern: versus (the colon-after-versus carries it)
- Penalties: -10 (the_x_that fragment in opening), -10 (colon after versus)
- Bonuses: +5 (named entity), +5 (scale word "country")
- Final score: 65 (B grade)
- Real CTR: **7.6%**, 28.8K views, +142 subs

**Lesson:** The versus pattern's strength rescued an otherwise weak structure. If the the_x_that fragment had been removed ("Guatemala vs Belize: The Border Dispute That Could Erase a Country") the score would have hit 80+.

### Example 2: The 9.5% CTR Champion

**Title:** "JD Vance Claims Christians Found Child Sacrifice. Here's the Evidence."

- Pattern: declarative
- Bonuses: +10 (evidence promise), +5 (named entity), +5 (controversy frame), +5 (two-sentence)
- Final score: 90 (A grade)
- Real CTR: **9.5%** — highest in calibration set

**Lesson:** Stack the bonuses. Evidence promise + named entity + controversy + two-sentence = top of niche.

### Example 3: The Self-Inflicted Wound

**Title (rejected):** "1494: The Treaty That Divided the World"

- Pattern: the_x_that
- Penalties: -50 (year as topic label), -50 (the_x_that pattern)
- Final score: 0 (REJECTED)

**Rewrite:** "Spain and Portugal Divided the World With One Line. The Treaty Is Still Affecting Borders Today."

- Pattern: declarative, two-sentence
- Bonuses: +5 (named entities), +5 (scale word "world"), +5 (two-sentence formula)
- Final score: 80 (A grade)

### Example 4: The Borderline Save

**Title (initial):** "Operation Condor: The CIA's Secret War"

- Pattern: colon (HARD REJECT)
- Final score: 30 (REJECTED)

**Rewrite:** "The CIA Helped Run a Death Squad Network Across Latin America. The Documents Are Now Public."

- Pattern: declarative + two-sentence + evidence promise
- Final score: 85 (A grade)

*[8 more worked examples follow in the full PDF — covering each pattern, hard reject, and bonus signal in real-channel scenarios]*

---

## 11. APPENDIX C: 50-TITLE PRE-FLIGHT CHECKLIST

Before you publish *any* title, run through this checklist:

**Pattern**
- [ ] Is the pattern A-tier (versus or declarative)? If C/D/F-tier, rewrite.
- [ ] Does the pattern match the topic? (versus only for bilateral; how_why only for mechanism content)

**Hard rejects**
- [ ] No year as topic label
- [ ] No colon as "Topic: Subtitle"
- [ ] No "The X That Y" pattern

**Bonuses**
- [ ] Does it have an evidence promise? (top signal)
- [ ] Does it name a specific entity (country, leader, org)?
- [ ] Does it use a controversy/myth-busting frame?
- [ ] Does it include a scale word?
- [ ] Does it use the two-sentence formula?
- [ ] Does it include a specific number (not a year)?

**Length and mobile**
- [ ] Between 35-70 characters
- [ ] First 40 characters tell the story (mobile cutoff)

**Final test**
- [ ] Read it out loud. Would you click it on the YouTube home page?
- [ ] Show it to one person who isn't a history fan. Do they understand what they'd be clicking?

---

## CLOSING

The whole system reduces to four operations:

1. **Detect the pattern.** Versus or declarative = ship. Question or the_x_that = rewrite.
2. **Apply the hard rejects.** Years, colons, the_x_that — eliminate without exception.
3. **Stack the bonuses.** Evidence promise, named entity, controversy frame, two-sentence formula. Three or more = strong title.
4. **Watch the 48h CTR.** Below 2% = swap both. 2-4% = swap title. Above 4% = hold.

That's the entire system. The Python scripts automate the detection and scoring. The methodology is what makes them useful.

If you implement this for 90 days and your CTR doesn't move, email the contact in `scripts/README.md` — the higher-tier package includes a Loom walkthrough where I'll review your specific titles and tell you what's wrong.

Otherwise: ship more titles. Calibrate to your channel. Don't trust this guide more than your own data once you have 30+ data points per pattern.

Good luck.

---

*Methodology developed by the History vs Hype YouTube channel. This guide ships with five Python scripts as reference implementations. Buyers of the $99 tier receive a 60-minute async Loom walkthrough scoring 5 of their own titles live.*

*Version 1.0 — 2026-05-08*
