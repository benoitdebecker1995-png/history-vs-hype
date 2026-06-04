---
name: roi-comparison-methodology-what-to-invest-in-next-decisions
description: Two-stage filter→table methodology for picking the next video to invest in among active backburner projects + fresh pipeline topics. Designed for sub-1K-sub channel in exploration mode.
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 831eb5a1-13a9-4d7d-aa50-09d2bc77dcb2
---

## Rule

When deciding "what video should I work on next?" with multiple candidates (active backburner + fresh pipeline + parked packages), use a two-stage filter→table methodology — NOT a single composite score. Math on noisy estimates is theater; structured comparison surfaces the real trade-offs.

**Why:** At sub-1K-sub channel size in exploration mode, the right metric is P(outlier) per hour weighted by exploration value, not pure views or sub conversion. P(outlier) is genuinely hard to estimate; multiplying noisy numbers gives noisier numbers. The methodology is designed to surface evidence honestly without forcing false precision.

**Origin:** 2026-05-14 grill session after Inquisition #54 ship. User wanted to pick next video; field was 16 candidates (10 active backburner + Hijab + 5 fresh pipeline). Pure formula approach was rejected as false precision; pure judgment was rejected as advocacy-prone.

## How to apply

### Score framework (qualitative, not formula)

- **Numerator:** P(>2K views in 7 days) — HIGH/MED/LOW. Outlier probability is the right metric for sub-1K channels needing breakout hits, not steady singles.
- **Multiplier:** Novelty count vs last 5 published (6 dimensions: format / topic-type / hook / title-structure / visual-lane / runtime).
- **Denominator:** Hours-to-ship-from-current-state (loose estimate). Sunk costs don't count.

### Stage 1 — two parallel filters

**Fresh topics:** Use the existing Small-Channel Topic Rubric (40/20/20/10/5/5 — see `feedback-small-channel-rubric.md`). Drop bottom 50%.

**Active backburner projects:** 4 PASS/FAIL gates. Project must PASS all 4 to survive:
1. **Packaging defensibility** — viable title + thumbnail concept hits parties-with-mechanism rule? PASS/FAIL
2. **Time-to-finish** — <25 hours from current state to publish? PASS/FAIL
3. **Angle timeliness** — news/relevance hook still hot? PASS/FAIL
4. **Recent-pipeline novelty** — introduces ≥1 new dimension vs last 5 published? PASS/FAIL

Brutal filter; that's the point — most backburner projects are backburnered for a reason.

**Parked-package candidates (e.g., script-locked but unfilmed):** Light audit gate — does the locked package still hold up against post-lock lessons? If yes, auto-survive to Stage 2 with hours-to-ship flag.

### Stage 2 — comparison table (7 columns)

Survivors from both Stage 1 tracks meet here.

| Col | Type | Criteria |
|---|---|---|
| Candidate | label | Folder name or fresh topic |
| P(outlier) | H/M/L | HIGH = ≥3 niche outlier patterns + VidIQ ≥60 + clear mechanism word. MED = 1-2 patterns OR mid-range search. LOW = no patterns OR <40 search |
| Hours to ship | number | Loose estimate, current state to publish |
| Novelty | count + tags | How many of 6 dimensions does this test as new vs last 5 published |
| Key strength | one line | Most compelling reason this could outlier |
| Key risk | one line | Most likely failure mode |
| What this teaches | one line | Data point produced if it ships — most important column for exploration mode |

### Decision rule

- Agent produces table + recommended #1 + 2 alternatives + 1-paragraph reasoning each
- User overrides on judgment; agent defends with data per "no yes-manning"
- **Tiebreaker (top 3 within ~15%):** "What this teaches" column wins — operationalizes exploration weight

### Time budget

~3 hours total selection overhead for ~25-50 hour production decision (6-15% selection cost — reasonable).
- User: ~30 min VidIQ on top 5 fresh candidates (synchronous block)
- Agent: ~2.5 hours, parallel — folder reviews + niche pattern matching + Gemini saturation scan + table assembly

## Stop conditions / anti-patterns

- **Don't run this for every video** — it's overkill for a routine "what's next" decision after a clearly-planned sequence. Use when 5+ candidates compete with no obvious winner.
- **Don't include both fresh and active versions of same topic** — if Falklands is already an active project AND in fresh pipeline, treat as ONE active row. The pipeline's "ANALYZED" status may be stale.
- **Don't fabricate cells.** If a P(outlier) estimate has no supporting evidence in MEMORY.md / channel-data / VidIQ, mark it ESTIMATED and resolve before lock (per `feedback-small-channel-rubric.md`).
- **Don't override the table to favor a sunk-cost project.** Active projects get the same brutal gates as fresh; if they fail, they fail.

## Cross-references

- `feedback-small-channel-rubric.md` — Stage 1 filter for fresh topics (the 40/20/20/10/5/5 rubric)
- `feedback-channel-data-too-small.md` — why we use niche-wide patterns (n=42+) not channel-specific (n<30) for P(outlier) estimation
- `feedback-vibes-test-framing.md` — exploration mode framing for format experiments
- `competitor-findings.md` — niche outlier patterns (specificity_bomb 5.4x, two-sentence declarative 11% rate, scale signal 1.33x)
- `data-patterns.md` — niche benchmarks (388 titles, 650 thumbnails)
