# What to do differently on the NEXT video — at-creation rules
**2026-07-23, for Codex. Forward-looking only. You read this repo but can't write it — return the rules in chat, each with its evidence and confidence, so the main thread can verify before the creator builds to them.**

## The reframe

Every prior run diagnosed the 57 EXISTING videos and proposed patches (retitle #59, add "Operation SIG" to a description). The creator's actual goal is **future videos** — the decisions made at creation time, before/while making the next one. This run turns the verified findings into **at-creation defaults**, and asks the one forward question nobody has: is anything about a video *decidable up front* that predicts whether it gets pushed?

Do NOT re-propose fixes to existing videos. Every output must answer: **"what do I decide BEFORE or DURING making the next video?"**

## Already verified — translate these into forward rules, don't re-derive

All of these were reproduced against the data by the main thread this week; cite them, restate them as at-creation instructions:

- **Structure / opener (CONFIRMED, n=55):** the winner/loser retention gap is decided by the 20% mark; the recurring failure is the **5–10% post-hook handoff** (verified: r20 top vs bottom quartile 48.7% vs 27.8%; the fragile band is the beat right after the cold open). Forward rule: write the next script so the beat after the hook goes straight into substance — no slack transition there.
- **Distribution (CONFIRMED null, n=56):** NO post-publish quality metric predicts impressions (retention ρ≈0, CTR ρ≈+0.18, like-rate *negative*). Sub-feed/search shares are symptoms of being pushed, not levers. Forward implication: you cannot earn distribution with retention/engagement tuning — the at-creation levers are **topic choice and packaging**, full stop.
- **Title CTR (HYPOTHESIS, n=8):** evidence-promise titles ran 3.91% vs 2.41%. Forward default: the next title makes a concrete, contestable evidence claim, not a "hidden mystery" tease.
- **Search (CONFIRMED concentration):** search demand is entity-led — 47% of non-Guatemala search views come from 5 exact named entities. Forward rule: if the video's subject has a searched proper name (a person, an operation, a treaty), put that exact name in the title or first description line at upload.
- **Thumbnail (HYPOTHESIS):** document-as-focal-object was negatively associated; busy hurt; red didn't hold up. Forward default: one clear focal object, not a document page; fewer elements.
- **Length (CONFIRMED null in range):** 5–13 min shows no duration→retention signal (r≈−.12). Forward rule: length isn't a lever in the normal range — decide runtime by the argument, don't cap reflexively.

## The one genuinely forward question to investigate

Distribution is decided upstream of everything measurable (finding #1). The only upstream thing decided AT CREATION is **the topic and how recognizable it is.** So:

- Is there any at-creation-knowable signal — `topic_type`, presence of a famous named entity, territorial-dispute vs abstract-concept, ongoing-news vs evergreen — that separates the videos that got impressions from the ones that didn't? Guatemala (an active territorial dispute with a recognizable stake) is the one breakout; is that a pattern (recognizable-stakes topics get tested harder) or an n=1 accident?
- ⚠ This is the hardest question in the dataset and the most confounded. Report it as a HYPOTHESIS with the confound named. A rigorous "the data can't answer this from 57 videos with one outlier" is an acceptable and useful answer — do not manufacture a topic formula.
- Cross-check against the channel's existing topic doctrine (`tools/PACKAGING_MANDATE.md`, `CLAUDE.md` channel DNA: "history with modern relevance," subscriber trigger = "understands systems," HOW > WHY). Flag anything the data supports or contradicts.

## What to produce

A single **"next-video checklist"** — the at-creation decisions in order (topic → title → thumbnail → cold-open + post-hook structure → length), each with:
- the forward rule (what to do on the next video),
- the evidence + `n` + CONFIRMED/HYPOTHESIS,
- and where it's only a default-to-test vs a real constraint.

Then, separately: the topic-signal investigation result (a rule, or an honest null with the confound).

## Guardrails
- **Forward rules are defaults to test, not laws** — n<30 means every one is provisional; the channel A/B-tests packaging natively, so frame each as "start here, one variable at a time."
- **Don't invent a topic formula** from 57 videos with a single outlier. The Guatemala distortion is fatal to any topic aggregate — report with-and-without it or use medians.
- **Distinguish the three levers** — topic (gets pushed), packaging (gets clicked), structure (gets held). A forward rule must say which outcome it moves.
- **Evergreen identity holds** — forward rules must keep "history with modern relevance," never drift to chasing timely news hooks.
- **Don't touch #62.**
- **Verifiable** — any number carries the query.

Return the next-video checklist and the topic-signal result. Rank the checklist by how much each decision moves the biggest bottleneck (distribution first, then click, then hold).
