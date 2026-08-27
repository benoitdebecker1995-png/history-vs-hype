---
name: repairing-script-voice
description: Repairs a History vs Hype script passage so it sounds like Benoit speaking rather than AI prose, by diagnosing the underlying cause and rewriting the text directly. Use whenever a draft is said to sound like AI, not sound like him, feel too polished or off, or when asked whether a paragraph is in his voice — and before handing over any script prose written for him. Fixes the passage; never produces an audit document.
---

# Repairing script voice

Benoit reads his scripts word for word off a teleprompter. That makes voice failure fatal rather than cosmetic: a sentence he cannot say in his own mouth stops the recording. This procedure exists because the previous approach produced version after version plus a folder of VOICE-AUDIT files, and the drafts still did not sound like him.

## The rule that matters most

**Repair the text. Do not write a document about the text.**

Producing a diagnostic file instead of a fixed passage reproduces the exact failure this replaces. Hand back the rewritten passage first, then say what was wrong. He is trying to record, not to read an assessment.

Two ways this goes wrong even when a rewrite is offered, both worth naming because they feel helpful at the time:

**Handing back a sketch.** Four lines and "something like this" where the passage was twenty leaves him exactly where he started. He cannot film a gesture at the shape. Replace every line, or cut it and say what was cut.

**Ending on a question he has to answer first.** If it is unclear which act he means, or whether the passage replaces existing text or precedes it, take the most likely reading and deliver the text anyway, saying in one line which reading you took. A question with no usable draft attached costs him a recording session; a draft built on the wrong assumption costs him thirty seconds.

## Where the evidence lives

- `channel-data/creator-model/OPERATING-MODEL.md` — sections 2 (Voice) and 10 (Language calibration). Read those two sections, not the whole file.
- `channel-data/creator-model/VOICE-EVIDENCE.md` — a large raw corpus of his spontaneous speech. **Never load it whole.** Grep it for the subject, the argumentative move, or a distinctive phrase in the passage being fixed, and read the few hits that come back.
- The active project's `_adlib/` folder when one exists. That is him talking through this specific video unscripted, and it beats any general rule.

Direct raw speech and wording he has already approved outrank every generalisation, including everything below. If a rule here contradicts something he actually said, he wins.

## The target register

Cleaned spoken analytic prose. Not a transcript, not an essay, not a documentary narrator.

Keep: his thought order, the real causal scaffolding, necessary context, meaningful qualifications, ordinary verbs, direct inspection of evidence, questions that genuinely audit a claim, and moderately long flowing sentences when the logic needs the bridge.

Cut: filler, repetition, abandoned starts, word-searching, stacked abstractions, institutional wording where a plain verb works, artificial punch fragments, decorative symmetry, slogans, faux-documentary rhetoric.

He builds thoughts while speaking — provisional formulation, test, context, scope correction, then a sharper version. That sequence is the substance, not noise to be tidied into a topic sentence. Flattening it into a clean assertion is the most common way a rewrite stops sounding like him.

## Diagnose the cause, not the symptom

When a passage fails, the reason is almost always one of these five. Naming the right one is what makes a fix possible rather than a reshuffle.

**A connector carrying no load.** Placing two facts side by side creates a question; the connector has to answer it. "So", "but", "because", "instead" must each mark a real logical or causal step. A connector used for rhythm is the loudest AI tell in his drafts.

**A missing mechanism hidden by a transition.** When a draft jumps from an idea to an action — ideology to massacre, decree to enforcement — ask what made the action possible: organisation, manpower, opportunity, command, institutional change. "Meanwhile" and "and so" are where that gap gets buried. This is a research problem wearing a prose problem's clothes, and it needs saying out loud rather than smoothing.

**A formal synonym where an ordinary word works.** "Underlying causal mechanism" for "why it happened". "Utilise", "facilitate", "constitute". He uses plain precise words and does not stack writerly ones.

**Rhetorical furniture.** Watch specifically for: "the contradiction was built into", decorative "on paper / in practice", "this wasn't merely X, it was Y", "neither X nor Y", "that changes everything", "beneath the surface", "the truth was more complicated". Also every paragraph landing on a big line. He does not close every beat with a slogan.

**A qualification deleted for flow.** His hedges usually carry information about scope or evidence quality. Removing one to tighten a sentence changes what he is claiming, and he hears it immediately.

## Running the pass

Work on the passage pointed at plus its immediate neighbours — voice problems are usually a seam between two beats rather than one bad sentence.

1. Read it aloud in your head as a person speaking. Mark where you would stumble, run out of breath, or say something you do not believe.
2. For each mark, name which of the five causes it is. If none fits, the sentence is probably fine and this is polishing — leave it. Rewriting more of a passage than the fault requires is its own failure: it costs him a re-read of lines that were already working, and it makes the next pass harder to trust. When one paragraph is broken and three are fine, fix the one.
3. Pull two or three passages from `VOICE-EVIDENCE.md` or `_adlib/` relevant to *this* argument, not generically representative.
4. Rewrite, preferring to restore his structure over inventing a better one.
5. If the real problem is a missing mechanism, say so plainly instead of writing around it. A fluent paragraph over a hole is worse than an awkward one that shows the hole.

## Generalise the correction

When he rejects something, the point is not to fix that sentence but to stop producing it. State the general constraint in one line so he does not have to teach it again on the next passage. If it is a durable rule about his voice, offer to add it to `OPERATING-MODEL.md` rather than leaving it in a chat log.

## What good output looks like

The repaired passage, then something like:

> Two things were wrong. "This wasn't just a border dispute, it was a legal argument" is the not-X-but-Y frame you hate — I replaced it with the actual distinction. And the jump from the 1859 treaty to Guatemala's later position had no mechanism in it; I've flagged that rather than bridged it, because it needs a sentence about what changed politically and I don't have one.

Not a table. Not a severity rating. Not a file.
