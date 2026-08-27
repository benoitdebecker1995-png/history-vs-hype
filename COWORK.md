# History vs Hype — Cowork adapter

`AGENTS.md` is the active shared operating contract. Everything in it applies here.

The difference from the Claude Code, Codex and Gemini adapters is that **Cowork starts without this
repository.** Those tools read `AGENTS.md`, `CHANNEL.md` and `ACTIVE_PROJECT` off disk. Cowork cannot,
so the state has to be carried in.

## The start packet

Upload these six, in this order. Together they are roughly the smallest thing that makes a cold
session useful. Nothing else is needed to begin.

| # | File | What it carries |
|---|---|---|
| 1 | `AGENTS.md` | The operating contract — how to work, what to load, historical safety, voice |
| 2 | `CHANNEL.md` | Channel identity, objectives, current evidence, what is already ruled out |
| 3 | `channel-data/creator-model/OPERATING-MODEL.md` | How Benoit thinks and talks. Sections 2 and 3 are the read-aloud rules and narration gates |
| 4 | `_research/NEXT-VIDEO-BRIEF-2026-08-26.md` | Self-contained. Everything needed to choose the next video, including the kill test |
| 5 | `channel-data/PACKAGING-DIAGNOSIS-2026-08-26.md` | **The most important file here.** Why packaging is the constraint, with the numbers |
| 6 | `channel-data/audience/CORRECTIONS-2026-08-24.md` | Every factual challenge from the comments, checked, with verdicts. Read `VERIFICATION-2026-08-26.md` beside it — it corrects two of its items against the video itself |

For work on the current video, add project 62's `PROJECT.md`, `RESEARCH.md` and `SCRIPT.md`. Those
three are the whole hot state; the rest of that folder is in `_cold/legacy-working/` and is history.

Deeper voice evidence, if a passage needs it: `READTHROUGH-PATCH-2026-08-17.md` and
`VOICE-CALIBRATION-JUNE-2026.md`, both in `channel-data/creator-model/`. Do not upload
`VOICE-EVIDENCE.md` wholesale — it is a 171 KB query-only corpus.

## Start from the diagnosis, not from scratch

Three things are settled by measurement as of 26 August 2026. A session that re-opens them is wasting
the creator's time. Full evidence in `PACKAGING-DIAGNOSIS-2026-08-26.md`.

**Frequency is not the constraint.** 39 long-form videos went out in the forty weeks to 5 July 2026.
Weekly has been run. Never propose "publish more" as the growth strategy.

**Writing is not the constraint.** Six videos under 120 views hold viewers longer than the
30,762-view breakout. Do not optimise the script in pursuit of views. Voice work is for identity and
the creator's own standard, not for growth.

**Packaging is the constraint.** 159,017 impressions were served to 27 videos that converted 5,898
views. CTR across the catalogue runs 0.46% to 9.41%, and CTR gates how much YouTube serves at all.

### The packaging rule

**Winners name someone doing something with a stake. Losers name a topic, a myth, or a method.**

| Clicked | | Not clicked | |
|---|---:|---|---:|
| JD Vance Claims Christians Found Child Sacrifice | 9.41% | The $24 Manhattan Myth | 0.46% |
| How the KGB Weaponized Palestinian Resistance | 7.90% | The Historical Pattern Nobody Wants to Admit | 1.01% |
| London's Stock Exchange Funded a Genocide | 7.45% | Medieval Europe's Hidden Literacy Boom | 1.11% |

A title carrying "fact check", "the myth of", "what historians got wrong", or a bare topic noun is in
the 1% band by measurement, not by taste.

**Draft the title before the script, not after the edit.** If the angle cannot be titled as an actor
doing something with a stake, the angle is wrong — and that is worth learning in an afternoon rather
than a fortnight.

Treat the rule as the leading hypothesis, not settled fact. A three-video retitle test is running to
check whether it is causal or merely correlated with live-conflict subjects.

**The metric is CTR, not views.** 6% or better clears the bottleneck. 2% does not, however good the
research was.

## What does not travel

Say so plainly rather than guessing at an answer these would have given:

- **The three databases.** `analytics.db`, `keywords.db`, `intel.db`. All channel history, retention,
  keyword and competitor data lives in them.
- **The 263 Python tools**, including every checker, gate and scorer.
- **The seven scheduled routines.** They currently fail every morning; see below.
- **The media.** Footage, rough cuts, `library/` PDFs, thumbnails — all on `G:\`.

For live channel numbers, the vidIQ connector answers directly. For anything historical about the
channel's own performance, the answer is in a database Cowork cannot reach: ask for it rather than
estimating.

## Current state — 26 August 2026

597 subscribers. Long-form took **2,907 views in the last 90 days** across ~50 videos. Nothing
long-form has published since early July, and suggested traffic is down to 893 views a quarter, so
the channel reads as dormant. Volhynia is filmed and being edited and is the committed next upload.
Everything else is downstream of it.

**Impressions and click-through are not currently knowable.** The collector broke on 28 July and the
analytics API surface in use does not expose them. Whether the problem is too few impressions or a
click-through problem is genuinely open — get it from YouTube Studio before building on either.

## Known broken — do not read these as current

- All seven `HvH-*` scheduled tasks fail on every run and have written no log since 24 August.
- `analytics.db` last refreshed 20 August, `keywords.db` 17 August, `intel.db` 10 August.
- CTR data stale since 28 July.
- 13 of the 15 projects in `_IN_PRODUCTION` are missing their three hot files. Only 62 and 67 have
  them. Making any other one active starts a session blind.
- Git holds 44 unpushed commits, a 3.99 GB pack and 352 uncommitted files.

## Stop list

Accepted on 13 August, restated 23 August, and still right:

- No architecture audits or redesigns before a video ships.
- No new commands, skills, agents, databases, scores or governance layers.
- No further tooling or model benchmarking.
- Do not expand research once the script-bearing claims are supportable.
- Do not predict breakouts from tiny, mostly unserved cohorts.
- Do not enlarge the voice corpus instead of capturing current speech.
- Repository cleanup is not channel progress.

**On plugins and skills specifically.** Eight skills were built and measured against a baseline that
had only the operating contract and the creator model. **Seven made no measurable difference and cost
17% more tokens.** The one that beat baseline — by 33 points — was `repairing-script-voice`, and it
won because it returns text that can be pasted into the teleprompter instead of a memo ending in a
question. Apply that test to anything Cowork offers: does it hand back usable work, or a document
about the work?
