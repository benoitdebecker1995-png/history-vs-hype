# `hypothesis-ledger` — Your Spec

Built from your answers. This is the version that runs on HvH, not a generic template.

---

## What this skill knows about you

**Your tested mechanisms (track record exists):**
- `search-gap` — top results are bad/missing/stale
- `news-bridge` — anniversaries, current events touching historical myths

**Your untested mechanisms (no data yet, high priority to test):**
- `suggested-piggyback` — sit next to a bigger creator's recent upload
- `cross-niche` — pulls multiple audience tribes
- `external-traffic` — engineered first-24h velocity from Reddit/X/Discord

**Your one breakout (Stalin, 1.4K) was likely one of the untested three.** The skill backfills this on init via your YouTube API setup. Until that runs, you don't actually know what worked.

**Hard constraints (coach will never violate):**
- Long-form 8–12 min only — no shorts pivot recommendations, ever
- Evidence-first packaging — no clickbait titles, no overpromise thumbs

**Soft constraints (open to data-driven retirement):**
- Untranslated Evidence format
- Any of the three formats can be deprioritized if 5+ falsified bets accumulate

**Your honesty pattern:** "tries to be fair." Light scaffolding required — the skill enforces *exactly one* primary attribution per failed bet (bet / execution / unclear), with one supporting data point. No hedging cells.

**Coach style:** active. Pushes pivots based on data. When you resist, it asks your reasoning and logs it. Over time, surfaces patterns in your resistance.

---

## Initialization (runs once, on skill install)

The skill uses your existing Claude Code + YouTube API setup to backfill the ledger from your 7 published videos. No manual work from you.

**What it pulls per video:**
- Traffic sources (Browse / Suggested / Search / External / End screens)
- Top suggested-from videos (who's algorithmically adjacent to you)
- Top search queries driving impressions
- Retention curve
- CTR by impression source
- Final view count, watch time, sub conversion

**What it produces:**
- Seeded `channel/bets.md` with all 7 videos, retroactive mechanism attribution (best-effort from Studio data)
- **Stalin post-mortem** — the headline output. Answers: did Stalin break out via suggested-feed, search, or external? Which channels was it adjacent to? What did the retention curve look like?
- Initial channel median (your rolling 5-video baseline)
- First mechanism distribution: "0 piggyback bets, 0 cross-niche, 0 external-push, X search-gap, Y news-bridge"

The first time you see this output is when the coach makes its first real intervention. Likely something like: *"You've published 7 videos, 5 used the same mechanism class. Stalin appears to have worked via [piggyback / external] — which you've never deliberately tried again."*

---

## The ledger schema

`channel/bets.md` — one row per published video.

```
| video | format | mechanism bet | signal read | exp CTR | exp AVD | actual CTR | actual AVD | views | vs median | verdict | primary failure | lesson |
```

**Required fields at bet time** (pre-publish, ~10 min):
- `mechanism bet` — picks from your 5-mechanism vocabulary
- `signal read` — concrete pointer (the competitor video URL, the VidIQ keyword, the news event date)
- `exp CTR`, `exp AVD` — your numerical bet

**Required fields at T+7d** (~15 min):
- `actual CTR`, `actual AVD`, `views`, `vs median`
- `verdict` — confirmed / partial / falsified
- `primary failure` — required only for partial/falsified. Exactly one: `bet` / `execution` / `unclear`. No hedging.
- `lesson` — one sentence. The most valuable cell.

---

## Verdict logic

- **Confirmed:** CTR and AVD both ≥ target. Views ≥ 1.5× median.
- **Partial:** one of CTR/AVD landed, the other missed by ≤30%. Or views landed but engagement softer than projected.
- **Falsified:** both CTR and AVD missed, OR views < 0.8× median.

**Breakout tag (separate from verdict):** `views ≥ 2× rolling 5-video median`. Floats up as channel grows. Currently probably ~700–1000 depending on your real median (skill computes from backfill).

---

## Channel rollup (after every T+7d post-mortem)

Auto-updates `channel/ledger-state.md` with:

**Mechanism win rates**
```
search-gap:        2/4 confirmed  (50%)
news-bridge:       1/3 confirmed  (33%)
suggested-piggyback: untested
cross-niche:       untested
external-traffic:  untested
```

**Calibration**
```
When you predict CTR ≥ 6%, you actually hit:  4.8% avg  → overconfident by 1.2pp
When you predict AVD ≥ 45%, you actually hit: 41% avg  → overconfident by 4pp
```

**Pattern alerts** (active coach speaks here)

---

## Coach behavior — your version

The coach intervenes at three moments:

### 1. At bet proposal time

Before you commit to a mechanism for a new video, coach checks:

- **Untested-mechanism alert** — "You're proposing search-gap. Piggyback and cross-niche remain untested after 8 videos. Want to make this one a piggyback bet instead, or commit to declining for a documented reason?"
- **Repeat-failure alert** — "Last two news-bridge bets falsified (Cyprus, Kashmir). Picking news-bridge again — what's different about this one?"
- **Calibration check** — if you write `exp CTR ≥ 8%` and your last 5 CTR predictions averaged 5%, coach asks: "Your last 5 predictions overshot by 2pp on average. Confidence justified here, or want to dial expected to 6%?"

### 2. At T+7d post-mortem

- If you mark failure as `unclear`, coach pushes: "Studio data shows traffic was 70% Search, AVD held until minute 6, then dropped. That looks more like execution than bet — want to refine?"
- Cross-references your stated lesson against past lessons. If you've written "thumbnail was weak" three times: "Thumbnail flagged as primary failure 3× now. Worth a deliberate thumb-vs-shelf review session?"

### 3. At channel rollup

- **Mechanism retirement suggestion** — "3 falsified news-bridge bets in a row. Demote? (Y = require strong signal to bet on this again / N = keep at current weight / Defer = revisit after 2 more videos)"
- **Mechanism promotion suggestion** — "First piggyback bet just confirmed at 2.3× median. Bias next 3 topic candidates toward more piggyback?"

### When you resist

Coach asks: *"What's the reasoning?"* You answer in 1–2 sentences. It logs to `channel/resistance-log.md` with date, recommendation, your stated reason.

After 3 instances of the same recommendation declined for similar reasons:

> *"You've declined the piggyback suggestion 3 times, citing 'topics don't feel right' each time. Two options: (1) make 'no piggyback' an explicit hard constraint and the coach stops suggesting it, or (2) commit to one piggyback bet in the next 5 videos. Which?"*

This is the loop. Either it becomes an explicit constraint (and the coach respects it forever), or it becomes a commitment with a deadline. No more drift.

---

## Hard rules the coach will never break

These are encoded as hard constraints, not preferences:

1. Never recommend shorts, vertical content, or sub-8-minute videos
2. Never recommend titles with overpromise, fake-curiosity, or sensationalism beyond your established voice
3. Never recommend thumbnails that misrepresent script content
4. Never recommend topic pivots that violate `channel-memory`'s "won't cover" list

If the data says "your channel would grow faster with shorts," the coach reports the finding but does not recommend the action. Your call whether to revisit the constraint.

---

## What runs on Day 1

1. Install skill.
2. Skill calls YouTube API across your 7 published videos.
3. ~20 minutes later: full backfilled `bets.md` + Stalin breakout analysis + initial mechanism distribution + first coach intervention.

You'll likely learn three things you didn't know before the file finishes generating:

- What actually drove Stalin
- Which of your 7 videos was your *worst* bet (not the lowest-viewed — the one where you were most miscalibrated)
- Which untested mechanism your existing data suggests is the highest-EV bet to try next

That's the entire point of the ledger. Everything that comes after is incremental compounding.
