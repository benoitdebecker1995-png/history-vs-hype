---
name: scouting-video-topics
description: Finds the next History vs Hype video — a subject with real existing audience where the source work is genuinely undone — and kills candidates that fail a competitive check. Use when asked what to make next, for video ideas, whether a topic is worth doing, whether a niche or angle could work, or to check who else has covered something. Encodes which lanes the channel has already tested and failed at, so dead ones are not re-proposed.
---

# Scouting video topics

Roughly a year of topic selection produced one video that worked out of about fifty. This procedure exists to stop repeating the specific mistakes that produced the rest.

**Read the "what has already been tested and does not work" section of `CHANNEL.md` before proposing anything.** It carries the current record with real numbers, and it is maintained as the channel changes so it stays true. This file carries the method; that file carries the facts.

## The two levers are separate

The failure underneath most of the catalogue is treating "unique and rigorous" and "someone wants to watch this" as one decision. They are two.

**The subject supplies recognition** — whether anybody has heard of the thing. This is where audience comes from and it has almost never been optimised.

**The investigation supplies uniqueness and integrity** — what question gets asked, which sources get opened, what is refused as overclaiming. This has never been compromised.

The catalogue's worst performers chose both for obscurity: an obscure subject investigated obscurely reaches nobody, however good the work. Its one breakout had a mass-recognisable subject in the moment paired with a specific, rigorous investigation — and that split happened by accident, not design.

Choose it deliberately. Borrow the audience from the subject; keep the integrity in the investigation.

## Two rules that follow

**Do not propose a subject on the grounds that nobody has covered it.** That criterion selects for obscurity every time, because undone work is most abundant where attention is thinnest. It is how the dead lane in `CHANNEL.md` happened, repeatedly.

**Do not use composite scores.** No opportunity score, viral score, breakout score, or weighted ranking. They manufacture false precision and are quarantined from decisions. Recommend in prose with the decisive evidence, the counterargument, and what would reverse the recommendation.

## What to look for instead

Fame produces retellers, not archivists. On a famous subject the work that gets done is retelling — explainers, complete histories, the shallow "actually that's a myth" correction. What almost nobody does is find where a specific sentence, number, or image first entered the record.

So **provenance work sits undone at the top of the recognition curve, not despite the fame but because of it.** That is the cell to hunt in: mass recognition and an untraced claim in the same object. `tracing-claim-provenance` is what gets run once a candidate is chosen.

Strong candidates usually have: a person, event, object, or image with existing mass recognition; a specific claim whose origin has never been followed backwards; evidence that can be put on screen and interrogated; several discoveries rather than one correction stretched thin; and a payoff about how historical knowledge gets made and transmitted.

Weak candidates: complete-history explainers; mystery recaps ending in "nobody knows"; debunks whose entire payoff is "this is false"; academic distinctions that will not fit in a title; anything needing physical archive travel before the premise can be established; and anything where a successful English creator has already done the exact investigation well.

## The kill test — run it before recommending anything

This is where the last search wobbled: a promising angle turned out to have a near-identical English video published days earlier, found only after substantial work. Finding that late nearly wasted a production cycle.

Search the *exact angle*, not the subject. Use `vidiq_youtube_search` on the specific question, `vidiq_similar_videos` on the closest match, and `vidiq_outliers` to see what actually performs in the space. Then report honestly:

- Who has attempted this exact investigation, and how did it perform?
- Is the gap "nobody has thought of this" or "nobody has done it properly"? Both are legitimate bets, but they are different ones and he should know which he is taking.
- Where a competitor exists, name what is specifically thin or wrong in their treatment. If the answer is "not much", say so and drop the candidate.

Run `vidiq_keyword_research` on the plain-language question to confirm demand is real rather than assumed, and that it is long-form demand rather than Shorts traffic.

## Research burden

Deep reading, source tracing and translation checking are all acceptable. The boundary is reachability: the decisive evidence must be gettable through digitised documents, books, articles, databases, or accessible experts. A topic becomes unattractive when untranslated archival material is indispensable just to establish the title promise.

## Output

Not a ranked table of twenty. Two or three candidates, each with: the question the video asks in one sentence; the central revelation; what goes on screen, concretely; the two or three strongest "yes, but" turns, since repeated turns are what make it an investigation rather than a debunk; the competitive picture with named videos and real numbers; and why it might fail.

Then a single recommendation with a reason — not a menu. Say plainly when the evidence does not support picking one.

## When he chooses, stop

Once he commits, the search is over. Do not surface marginally better alternatives or reopen because something interesting appeared. Switching cost rises steeply as a video advances, and a project he owns has more claim on his commitment than a generated suggestion. Move to the next unresolved problem.

## Record the prediction before publishing

For a consequential topic choice, write down the recommendation, the reasoning, the mechanism expected to produce views, and what you expect to observe — before the outcome is known. Attach the real numbers afterwards. One noisy result updates confidence; it does not become a channel law.

This is the only way the channel accumulates knowledge instead of anecdotes, and its absence is why a year of publishing produced no usable pattern.
