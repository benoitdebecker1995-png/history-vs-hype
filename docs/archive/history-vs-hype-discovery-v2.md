# Discovery & Breakout Layer (v2 — VidIQ Pro integrated)

Bolts onto skills-v2. Replaces/expands Phase 1 (Topic & Demand). Built for the 0–1K reality: the algo barely knows what you are, so you can't lean on Browse/Home traffic. You live on **search**, **suggested-from-bigger-creators**, and **outlier velocity**.

**What changed in this revision:** VidIQ Pro is now treated as a foundational tool, not duplicated. Skills consume its outputs and add the one layer VidIQ can't: "is the top result *wrong*?" That filter is what makes evidence-based myth-busting a real edge.

## The brutal mechanics at your stage

1. **Browse/Home is mostly dead** until the algo has enough signal to classify you. ~2K subs is the rough inflection.
2. **Search and Suggested do the heavy lifting.** Search rewards topic gaps. Suggested rewards sitting next to bigger creators' videos *while they're hot*.
3. **One outlier confirms nothing — two confirm a pattern.** Stalin hit 1.4K. The algo just started learning. The next breakout has to land in the next 3–5 uploads or the signal decays.
4. **Outliers are made of mismatches.** Either demand >> supply (search gap), or quality >> existing supply (the top result is wrong/shallow), or you're suggested-feed-adjacent to a video 10–100× your size *right now*.

Three of the four breakout levers are upstream of the script. Your discovery skills decide whether the video has a chance *before you research it*.

---

## How VidIQ Pro fits

You operate VidIQ — the skills don't try to replace it. VidIQ does what it does well: keyword volume, competition scoring, Daily Ideas, Outlier feed, competitor tracking, SEO scoring. The skills consume those outputs and add the **"is this winnable for an evidence channel"** decision layer on top.

```
VidIQ Pro (you operate)
    ├─ Daily Ideas ───────────┐
    ├─ Keyword research ──────┤
    ├─ Outlier feed ──────────┼──→ vidiq-bridge ──→ discovery skills
    └─ Competitor tracking ───┘
```

### `vidiq-bridge` (foundational infrastructure)
Wraps your VidIQ Pro exports into a structured format the other skills consume. Saves you re-pasting CSVs into different skill contexts.

**Process:**
1. You drop VidIQ exports (keyword research CSVs, Outlier list exports, Daily Ideas screenshots/text) into `discovery/vidiq-inbox/`.
2. Skill parses and normalizes into structured records: `{keyword, search_volume, competition, outlier_ratio, top_results, last_updated}`.
3. Maintains a rolling `discovery/vidiq-state.md` — the canonical view of your current VidIQ research, queryable by other skills.
4. Flags stale entries (>14 days) so you know to refresh.

**Output:** structured VidIQ data the discovery skills can reach for without you re-exporting every time.

**Stop condition:** if a candidate keyword lacks a VidIQ record, the skill prompts you to run it in VidIQ first rather than guessing.

---

## The Priority 3 (discovery edition)

These replace v2's `topic-intake` as the front door.

### 🥇 `outlier-hunter`
**What it does:** ingests VidIQ's Outlier feed + Daily Ideas + your saved keyword research, then applies the one filter VidIQ can't: *is the existing top result on this topic factually wrong, shallow, or stale?* That's where your evidence-based positioning wins by default.

**Process:**
1. Reads from `vidiq-bridge` — VidIQ has already done the "what's outperforming" math. Skill takes that as input, doesn't recompute it.
2. For each VidIQ-flagged outlier or high-potential keyword, runs the actual YouTube search and pulls top 5–10 results: titles, view counts, channel sizes, ages, top-thumbnail patterns.
3. Applies the **evidence-channel filter** — three sub-categories:
   - **"Top result is wrong"** — myth-busting bullseye. Sample the top video, check against your knowledge + a quick primary-source spot-check. If the top result is factually weak, this is a high-conviction bet.
   - **"Top result is 8+ years old"** — algo hungry for fresh take, lower competitive bar.
   - **"Top result is shallow"** — high views but surface-level treatment. Your trilingual + primary-source angle wins on depth.
4. Cross-references against `breakout-pattern-extractor`'s template: does this topic fit the shape that's worked for your channel?

**Output:** `discovery/outlier-board.md` — ranked topics with both VidIQ's quantitative data *and* the qualitative evidence-gap assessment.

**Stop condition:** rejects topics where the top 3 results are accurate, recent (<2 years), and on big channels (>100K). That's saturated lane; you're not winning the search there, and you're not adding value as a corrective.

---

### 🥈 `suggested-piggyback`
**What it does:** identifies recent big-creator uploads in your niche or adjacent niches where your myth-busting take could land in their Suggested feed.

This is how small channels jump. Real Civil War / Kings & Generals / Voices of the Past / Real Engineering / Wendover drops a video on a topic your debunk angle pairs with — you publish within 48–72h, with title/thumb engineered to look like the natural next click, and the algo starts surfacing you to *their* viewers.

**Process:**
1. Maintains a watchlist of ~30 channels in your niche + adjacent (geopolitics, military history, world history, language history) — overlaps with VidIQ's competitor tracking but goes broader.
2. Daily/twice-weekly pull of their recent uploads via YouTube MCP.
3. For each, asks: *is there a myth, contested claim, or "you only got half the story" angle this video opens up?*
4. Flags candidates with: source video URL, view velocity, your angle, urgency (window typically 48–72h before the suggested heat fades).
5. Cross-checks against your existing research backlog and `vidiq-bridge` data — if VidIQ already shows the related keyword as low-comp, urgency goes up.

**Output:** `discovery/piggyback-board.md` — time-sensitive opportunities, ranked by source-video heat × angle strength × VidIQ keyword fit.

**This is where Stalin-shaped breakouts come from.** Your Stalin video almost certainly got a suggested-feed lift from something. Find that pattern and engineer it.

---

### 🥉 `breakout-pattern-extractor`
**What it does:** reverse-engineers your own outliers (currently: Stalin) to identify what made them work, so the next attempts can replicate the *shape*, not the topic.

**Process:** for any video that outperforms your channel median by 2×+:
1. Pulls Studio data: traffic sources, top suggested-from videos, top search queries, audience retention curve, CTR by impression source.
2. Cross-references with VidIQ's post-hoc scoring on that video's keywords (what VidIQ would have said about the topic *before* you made it — useful for calibrating whether VidIQ's signal correlates with your actual outliers).
3. Pulls the title structure (what angle: contrarian / number / named-figure / question / etc.).
4. Pulls thumb composition (focal element, emotional read, contrast pattern).
5. Pulls topic adjacencies (which big videos drove suggested impressions — these are your *real* algorithmic neighborhood).
6. Extracts a **breakout template**: "Videos that work for this channel have [title structure X], [thumb pattern Y], sit suggested-next-to [channels Z], match VidIQ signals [W], and break out via [traffic source]."

**Output:** `discovery/breakout-template.md` — a living doc updated after every 2×+ video. Every new topic candidate gets scored against this template.

**Critical:** the template is *probabilistic*, not prescriptive. After one outlier you have a hypothesis. After three you have a pattern. Don't lock in the template too early.

---

## Supporting Skills

### `search-gap-finder`
Two-filter design now. VidIQ already finds low-competition + high-volume keywords — that's the first filter, and you already run it in VidIQ. This skill adds the second filter: *among VidIQ's low-comp/high-vol candidates, which have top results that are factually weak?*

**Process:**
1. Pulls VidIQ-flagged low-comp/high-vol candidates via `vidiq-bridge`.
2. For each, runs the actual search and assesses top-3 result quality (the same eval as `outlier-hunter` but on a pre-filtered list).
3. Particularly tuned for **Quote Check** queries: "did Napoleon really say…", "what does the Treaty of … actually say". The entire format runs on search-gap economics, and VidIQ alone won't surface these — they're niche queries with modest volume but near-zero quality competition.

**Output:** `discovery/search-gaps.md` — VidIQ-validated keywords where evidence quality wins.

### `tipping-point-detector`
Unchanged — VidIQ doesn't track this. Monitors three signals weekly:
- **Anniversaries** rolling up in next 30/60/90 days (historical events that touch your niches)
- **News-history bridges** — current events that touch a historical myth (Ukraine ↔ Russian historical claims; Israel/Palestine ↔ 1948 myths; Taiwan ↔ One China narrative)
- **Media triggers** — books, prestige TV, films, viral threads touching your topics in next 60 days

Outputs a 60-day calendar. Discovery thrives on being *first* on the wave, not last. Pairs powerfully with `vidiq-bridge`: once you've identified an upcoming trigger, you can run the related keywords in VidIQ proactively, before competitors do.

### `cross-niche-bridge`
Finds topics that pull from neighboring audiences. Your Stalin video probably worked partly because it sat in *political-history Twitter*, *USSR-history*, and *communism-debate* audiences simultaneously. Single-niche topics underperform; multi-niche topics break out.

For each candidate, asks: which 2–3 distinct audiences would click this? If only one, it's a slow burner. If three, breakout candidate. Uses VidIQ's competitor-overlap data where available to validate audience adjacency.

### `payoff-density-checker`
Script-level breakout pattern. Breakout videos have ~1 "huh" moment per 60–90 seconds — a fact, reveal, source-shock, or counter-intuitive turn. Drier evidence videos have one every 3–4 minutes and die in retention.

Runs on `final.md` after you write it. Maps the payoff curve. Flags dry stretches >90s. Doesn't rewrite — tells you where to cut or insert a beat.

### `shareability-test`
One question: is there a single 30-second clip in this video so striking someone would screenshot the title, clip the moment, and post it to Reddit / X / Discord? If no, the video has a retention ceiling but no breakout ceiling.

Identifies the candidate "share moments" in your script and flags videos that don't have one before you film. Sometimes the fix is a script-level beat. Sometimes it means the topic itself was wrong.

### `thumb-vs-shelf`
Companion to `thumb-concept-forge`. Once you have a concept, this skill renders (or describes precisely) what your thumb would look like *sitting in the actual suggested shelf* for your target piggyback video. Forces differentiation by composition, color, and focal element. The thumb that looks great alone but blends into the shelf loses.

### `first-24h-velocity-plan`
Post-publish, but discovery-coded. The algo weights first-24h velocity heavily. This skill drafts an external traffic plan:
- Which subreddits accept your topic (and which mod rules apply)
- Which Twitter/X accounts to reply-with-link
- Which Discord communities are on-topic
- Whether to comment on the piggyback video (and what to say — never spam, always add value)
- Timing of each push relative to publish

Output: `06_post/velocity-plan.md`, executed by you.

---

## How this slots into the v2 workflow

The discovery layer sits *in front of* `format-router` and *replaces* the old `topic-intake`:

```
VidIQ Pro (you operate) ──→ vidiq-bridge ──→ discovery skills

DISCOVERY (new front door)
   outlier-hunter ──┐
   suggested-piggyback ─┤
   search-gap-finder ───┼──→ topic candidates with breakout scoring
   tipping-point-detector ──┤
   cross-niche-bridge ──┘
                           ↓
         (breakout-pattern-extractor scores each)
                           ↓
                      format-router
                           ↓
                  [existing v2 pipeline]
                           ↓
SCRIPT-LEVEL DISCOVERY (insert before broll-mapper)
   payoff-density-checker
   shareability-test
                           ↓
PACKAGING DISCOVERY (insert into packaging phase)
   thumb-vs-shelf  (after thumb-concept-forge)
                           ↓
POST-PUBLISH DISCOVERY (insert into post-publish phase)
   first-24h-velocity-plan
   breakout-pattern-extractor (re-runs after any 2x+ video)
```

---

## Revised build order

**Week 1 — discovery front door:**
1. `channel-memory` + `style-guide` + `project-init` (foundation)
2. `vidiq-bridge` (foundational — every discovery skill reads from it)
3. `outlier-hunter`
4. `suggested-piggyback`
5. `breakout-pattern-extractor` (seeded with Stalin video data)

You'll feel the impact in your next 2–3 uploads — topic selection alone shifts.

**Week 2 — script + thumb breakout layer:**
6. `payoff-density-checker`
7. `shareability-test`
8. `thumb-concept-forge` + `thumb-vs-shelf` (paired)
9. `title-forge`

**Week 3 — supporting discovery:**
10. `search-gap-finder`
11. `tipping-point-detector`
12. `cross-niche-bridge`
13. `first-24h-velocity-plan`

**Week 4 — research depth (from skills-v2):**
14. `source-deepening`
15. `research-to-brief`

Note the inversion: skills-v2 had research as week 1. With discovery prioritized, **picking the right topic** comes first; deepening research comes after you know the topic has breakout potential. Otherwise you do brilliant research on videos that 200 people watch.

**Week 5+** — everything else from skills-v2 in original order.

---

## What stays manual in VidIQ

The skills don't try to do what VidIQ does well. You keep:
- Running keyword exploration sessions in VidIQ when seeding a topic search
- Picking which competitors to track
- Skimming Daily Ideas
- Running ad-hoc keyword checks when an idea hits

The skills catch your VidIQ outputs and run the decision layer on top: *which of these win for an evidence channel, in your algorithmic neighborhood, on the breakout pattern that's worked for you.*

---

## The mindset shift

skills-v2 treated each video as a self-contained editorial project. The discovery layer treats each video as a **bet placed inside a market**.

The market has:
- Existing supply (competitors — VidIQ tracks this)
- Demand signals (search, comments, news — VidIQ tracks search; comment-miner and tipping-point-detector cover the rest)
- Heat (recent uploads pulling algorithmic attention — suggested-piggyback)
- Adjacencies (neighboring audiences — cross-niche-bridge)

You don't pick topics. You pick **bets where the market structure is in your favor.** Then you bring evidence-based execution to win the bet.

Stalin worked because it was a bet on a market with broken supply (lots of bad takes, few primary-source ones). Replicating that means finding the next broken-supply market, not the next "good topic." VidIQ tells you where the markets are. The skills tell you which ones a corrective evidence-based take can win.
