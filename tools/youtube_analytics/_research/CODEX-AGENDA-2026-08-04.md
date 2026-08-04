# What Codex should work on next — ranked agenda

**2026-08-04.** Written after the Codex port landed (`.agents/skills/`, `.codex/`), which changes the
premise of every earlier `CODEX-*.md` brief: those all said *"you read this repo but can't write
it."* **Codex can now write.** So the agenda below is execution-shaped, not essay-shaped — and it
deliberately avoids another interpretive pass over channel data, which has now been done seven times
and is exhausted.

Every number here was pulled from the live databases on 2026-08-04, not copied from a doc. Where a
doc and the database disagreed, the database won and the disagreement is item 6.

---

> **UPDATE, same day, after diagnosing item 0.** Items 0 and 3 were written from the July handoff
> and were partly wrong; both are corrected in place below. Short version: **item 0 is now fixed in
> code except for one command only the machine owner can run**, and **item 3's "harvest the swap
> experiments" was already done — they came back dead**, which is a finding rather than a task.

## 0. ~~BLOCKING~~ FIXED, except one human step

`Get-ScheduledTaskInfo`, 2026-08-04:

| Task | Last run | Result |
|---|---|---|
| HvH-GrowthRefresh | 2026-08-03 07:45 | `0x1` |
| HvH-CtrTracker | 2026-08-03 07:30 | `0x41306` (terminated) |
| HvH-ChannelHealth · HvH-Reconcile · HvH-BrainHygiene · HvH-StaleProjects | 2026-08-03 | `0x4E` (78 = preflight refusal) |

Four routines are failing the preflight gate, the CTR tracker is being terminated, and the growth
refresh errors. Newest `impressions_daily` row is **2026-08-01** — the data every packaging and topic
decision reads is three days stale and not self-healing.

**Diagnosed and fixed 2026-08-04.** Two independent causes, not one:

1. **GrowthRefresh** — the ~42-minute serial-call problem was already fixed; it now runs in **428
   seconds with 6 workers** and exits 0 on 08-01, -02, -03 and -04. The 08-03 07:45 `0x1` was
   something else entirely, and the traceback in `.brain/_inbox/growth-refresh-2026-08-03.log` is
   explicit: the YouTube OAuth refresh token was revoked → a *scheduled* run called
   `flow.run_local_server(port=8080)` → `[WinError 10048]`, because the port was already held. A
   headless task tried to open a browser consent page nobody could answer, on a hard-coded port.
   **Fixed** in `tools/youtube_analytics/auth.py`: ephemeral loopback port (`port=0`, valid for this
   `installed`/Desktop client), plus an `InteractiveAuthRequired` guard that exits **78** with a fix
   instruction instead of hanging until the task limit kills it. Wrappers now export
   `HVH_NONINTERACTIVE=1`. Pins: `tests/unit/test_auth_noninteractive.py` (18).
2. **The four `0x4E` routines** — single cause, and it is NOT the YouTube credential: the **claude
   CLI's** refresh token is blank. `.brain/_inbox/channel-health-run-2026-08-04.log` says so
   verbatim. **Only the machine owner can fix this**, from a terminal as this Windows user:

   ```
   claude auth login --claudeai
   ```

   Until then ChannelHealth, Reconcile, BrainHygiene and StaleProjects keep refusing at the
   pre-flight and `/reconcile` keeps not archiving publishes.

**Not stale after all:** `impressions_daily` ending 2026-08-01 on 2026-08-04 is the Reporting API's
own ~D−3 lag, not a broken pipeline. Retracted from the first draft of this file.

---

## 1. The launch-shape question — answerable for the first time

`keywords.db.impressions_daily`: **2,553 rows, 57 videos, 2026-05-24 → 2026-08-01**, per-video
per-day grain. This did not exist when the discovery handoff was written, and it is the single
biggest change in the evidence base.

`NEXT-VIDEO-DISCOVERY-HANDOFF.md` §9 asks for a **shape** criterion on H3 — day-1 share, or a floor
on days 8–28 — because a total-impressions threshold cannot distinguish a demand pocket from a failed
test batch. #59 took 88% of its lifetime impressions on day one and would have *passed* a
total-only bar while being a total failure. That shape is now computable.

Only three videos have a true launch window inside the data:

| Published | Video | Days | Impressions |
|---|---|---|---|
| 2026-05-28 | They Didn't Just Buy Slaves… | 65 | 2,963 |
| 2026-06-04 | The Piri Reis Map… | 49 | 3,258 |
| 2026-07-05 | Israel vs Palestine, 1947 UN Plan… | 29 | 11,013 |

**The task:** characterise the decay shape of those three, build the reusable read as a tool
(`impressions_daily` → day-1 share, day-3 cliff, days 8–28 floor), and wire it so future launches are
scored automatically.

**The trap, and it is the whole discipline here:** **n=3.** The existing 9,000/4,500 thresholds
already rest on n=2 and the repo requires that caveat every time they are cited. The deliverable is a
*characterisation and an instrument*, never a tuned threshold. Any output that proposes new numeric
gates off three videos is overfitting and should be rejected.

---

## 2. The thumbnail evidence base is computed on unserved videos — and contradicts itself

`analytics.db.thumbnail_features`: **47 rows of 58 videos**, six booleans — `doc, cf, em, map, busy,
red`. No `operation` column, no writer script.

Three defects, all documented in the handoff §7 and none fixed:

1. **The deltas are noise.** 38 of 56 videos have <1,000 lifetime browse impressions, so the feature
   deltas in `CTR-THUMBNAIL-FINDINGS-2026-06.md` (−0.71 doc, +0.65 map, −0.52 busy) are medians over
   three-digit-impression readings. Recompute restricted to served-only (n≈18) and say what survives.
2. **The file argues against itself.** Its validation table kills "red pop" (−0.67, marked OVER-FIT,
   KILLED); forty lines later it prescribes red as winner-recipe item #3, and
   `THUMBNAIL-CRAFT-RECIPE.md` [T2] rule 5 still calls red the channel's look-here signal. **Any
   agent reading top-to-bottom adopts the killed rule** — including the thumbnail generator.
3. **The generator's real decision variable was never tested.** It chooses an *operation*; the table
   stores six unrelated booleans. Add the operation column and backfill it.

**Why this ranks high:** packaging is the stated growth bottleneck, and the thumbnail is the named
binding constraint on the video currently in flight.

---

## 3. The A/B instrument is dead — and the docs still say it's unread

The handoff lists "5 swap experiments sit PENDING and unread… the channel's only within-video causal
evidence. Harvest it." **They were harvested. Every one returned the same verdict:**

| Video | Variable | Baseline | After swap |
|---|---|---|---|
| aSfZtrgGjwA | thumbnail | 1.91% @ 2,672 | 2.75% @ **218** |
| liW4BSh46DU | title+thumbnail | 0.44% @ 450 | 10.94% @ **192** |
| -kg30uRUY1M | title+thumbnail | 1.43% @ 2,721 | 2.56% @ **78** |
| mCR5f_ZcB5k | title+thumbnail | 1.38% @ 2,242 | 2.90% @ **482** |
| WgE2FLsDhfk | title+thumbnail | 3.12% @ **19,388** | 0.79% @ **127** |

All five: `INCONCLUSIVE-NOT-SERVED`. Post-swap impressions collapsed by one to two orders of
magnitude, so the new CTR is measured on nothing. The 10.94% is 192 impressions; the 19,388-impression
video fell to 127.

**The finding nobody has written down: you cannot A/B packaging on this channel while serve is the
constraint, because the swap itself coincides with the serve ending.** That kills the channel's only
causal instrument, and it should be recorded as such rather than left as a to-do.

**The research question for Codex** — and this one is genuinely open: is there *any* within-video
causal design that survives a serve-limited channel? Candidates to evaluate, not assume: swapping only
while a video is actively being served (day-grain data now makes "actively served" detectable), or
measuring on a surface other than browse. If the answer is no, say so plainly and close the line.

---

## 4. The gap-hunter's competitor set may still be misaligned with the lane

`intel.db`: **9,712 comment_signals, 2,697 competitor videos, 30 channels** — nearly triple the 3,343
signals of the first sweep.

The recorded known-limit was that Metatron / ReligionForBreakfast / Alex O'Connor produced 1,397 of
3,343 signals while only 61 signals in the whole corpus carried treaty/border/court vocabulary. The
fix — widen `tools/intel/competitor_channels.json` across the four access barriers (enclosure,
language, ideology, archive) — was specified but the corpus has grown since.

**The task:** re-measure the skew on the current 9,712 before changing anything, then rebalance and
re-sweep. This decides which candidates the next-video search can even see.

---

## 5. The script gate that would cut passes-to-lock

`EVAL-BASELINE.md`, v18 blind regen scored against the human lock: **17 PASS / 5 PARTIAL / 2 FAIL**.
Both failures are mechanically catchable:

- **R22** — the regen put its single CTA at ~100%, so the video *ends* on the CTA. The lock places it
  at ~70% and closes on a document beat. (This is the same defect the conversion memory identifies as
  the breakout's leak: the CTA sat where only 22.4% were still watching.)
- **R24** — 5 voice_lint HARDs, all retired surface tics ("here's the thing" ×2, colon-reveal ×2).

The file's own conclusion is the useful part: *"rules-as-outline transferred, rules-as-diction did
not"* — and the heavy gate (GR-B3b) would have caught every one of these before the creator read a
line. **The task:** make that gate real and put it in front of the read-aloud. The payoff is measured
directly in passes-to-lock, which `EVAL-BASELINE` already tracks.

**Caveat to carry:** v18 was trained on #58's own deltas, so the baseline is in-sample. A pass means
"lessons encoded", not "generalises".

---

## 6. Doc-truth audit — cheap, mechanical, and overdue

While writing this agenda, two claims in `NEXT-VIDEO-DISCOVERY-HANDOFF.md` turned out to name the
wrong database:

- `impressions_daily` is described as an `analytics.db` table. It is in **keywords.db**.
- `thumbnail_features` is described as a `keywords.db` table. It is in **analytics.db**.

Neither is a typo with no consequence: an agent that follows the doc queries a table that does not
exist, gets an error or an empty result, and — per the repo's own standing failure mode — may read
that silence as an answer. This is exactly what ADR-0017 and ADR-0021 exist to prevent.

**The task:** mechanically extract every table, column and file path named in `channel-data/**.md`,
`.claude/**/*.md` and `AGENTS.md`, resolve each against the live schemas and filesystem, and report
the misses. No judgment, no numbers to invent, a clean pass/fail per claim — the ideal Codex job.

---

## Do NOT send these to Codex

1. **Anything requiring it to quote our numbers.** Documented failure: it reported `title_scorer`
   output of 64/74/69 when the actual scores were 92/87/82, and cited a 57-second Short as a
   competitor treatment. Give it the query to run and let the repo produce the figure. It is strong on
   argument and unreliable the moment it reaches for a measurement.
2. **Any "no referee exists" / whitespace claim.** The REFEREE-GAP TRAP: a 73-minute specialist
   adjudication with 736,169 views (`NQX5LlJ7YXg`) had existed since 2022 and was missed because two
   tools with excluding windows returned nothing and their silence was read as proof — then used to
   greenlight #64. Absence needs a direct check, always.
3. **Retuning the 9,000 / 4,500 breakout thresholds.** They are pre-registered and rest on n=2.
   Retuning them after seeing outcomes is post-hoc and destroys the test.
4. **The ~16 outstanding manual Studio Advanced-mode exports.** Real and still blocking a proper
   pre-May baseline, but it is data entry behind a login — a human task, not a delegable one.

---

## Suggested order

**0 → 6 → 2 → 1 → 3 → 5 → 4.**

Fix the pipes (0), then make the docs stop lying about where the data lives (6) — both are pure
engineering and both make everything after them trustworthy. Then thumbnail (2), because it is the
binding constraint on the video in flight. Then the launch-shape instrument (1). Items 3 and 5 are
research questions with real answers; 4 is a rebuild that only pays off once the sweep is aimed at the
right lane.
