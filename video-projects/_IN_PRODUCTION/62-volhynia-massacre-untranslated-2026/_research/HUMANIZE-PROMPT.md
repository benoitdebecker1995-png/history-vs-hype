# HUMANIZE PROMPT — for GPT-5.6, paste with `VO-v7.1.md`

> Built 2026-07-22 against the **measured** failure modes of the previous ChatGPT pass on CH3/CH4/CH9
> (see `_adlib/t7-harvest-2026-07-22.md`): it drifted *more formal* on 3 of 3 chapters, stripped an
> attribution off a quotation, truncated a quote, broke a pronoun referent, produced a fragment
> triplet, and stacked a participial clause before the main verb. Sections 3 and 5 exist because of
> those six things specifically. Do not trim them.
>
> **⚠ REVISED 2026-07-22 after the v7.2 pass was rejected.** v7.2 hit every numeric target and still
> failed: it inverted the `so`:`but` ratio to buy the connector count, put all three hedges on
> evidentiary beats, cut a deliberate sequencing guard as "repetition", invented an actor via a flow
> edit, and rewrote eleven lines that came from the creator's own mouth. Sections 0, 4, 5 and the
> V4 note are the fixes. The eleventh problem — it had no way to know which lines were his —
> is fixed by the corpus file, which is now mandatory.
>
> **Workflow: paste THREE things, in this order —**
> 1. `channel-data/calibration/VOICE-CORPUS-FOR-MODEL-PASSES.md` (the locked lines; without it, expect v7.2 again)
> 2. this prompt
> 3. the VO script
>
> → get the rewrite + the change table → bring the change table back here for fact-checking against
> `01-VERIFIED-RESEARCH.md` and `_research/SOURCE-GENEALOGY.md`.

---

## THE PROMPT (copy everything below this line)

You are helping a YouTube history creator make his own script sound like him. You are not writing a new script. You are doing a voice, logic and flow pass on a finished, fact-checked one.

### 0. Read the voice corpus first — it overrides everything below

You have been given a file called **VOICE-CORPUS-FOR-MODEL-PASSES.md**. Read it before the script.

Its §1 is a list of lines the creator produced with his own mouth across seven read-alouds. **Those lines are locked. Do not rewrite, reorder, split, merge, or "improve" them — not for flow, not for connectors, not for tightness, not because one looks like a fragment or a metaphor or a repetition.** If any rule in this prompt tells you to change a locked line, the rule is wrong for that line: leave it alone and note it in your change table.

Its §2 is a list of phrases he has rejected out loud. Never write one.

**This is not optional context. A previous pass of this exact job hit every numeric target and was rejected anyway, because it rewrote eleven of his own lines** — it deleted "you cannot call that spontaneous," called "the anti-Polish sentiment was alive and well" a minted phrase, swapped "buries" for "leaves out," and plained away "a grain of truth," which he has said on record is how he speaks.

### 1. Who is speaking

He runs a small, honest, source-based history channel. The governing image, in his own words: **"like me talking to people in a bar."** A smart friend explaining history to you over a drink — plain, simple, genuinely interesting, without sacrificing historical integrity.

His stance is **explain, don't judge.** He is a referee who goes to the document, not a prosecutor delivering a verdict. He shows you what the evidence says and lets you weigh it. He concedes what the other side gets right. When there is a judgment to be made, he attributes it to the historian who made it, or he asks the viewer the question and leaves it open.

He sounds like an analytic mind reasoning out loud through a causal chain — conversational, intellectually honest, dry. He is **not** clipped and punchy, **not** an ice-cold systems explainer, **not** breathless, and **not** a rapid scale-comparison narrator. Those are all wrong.

His two enemies, both of which he rejects:
1. **Staccato / gimmick** — chopped fragments, eight-word gavel verdicts, "guess what."
2. **Purple / writerly prose** — over-explaining, padding, literary flourish, stacked credentials.

The target is the lean middle: plain, tight, clear bar-talk. Explain the mechanism simply, then stop.

### 2. What you are changing

Sentence joints, breath, connectors, word choice, paragraph logic. Nothing else.

The topic is a real atrocity. Keep the register level and unshowy throughout. Never make a phrase more vivid, more ironic, or more knowing than it already is. There is no room anywhere in this script for wit about the killing.

### 3. HARD RULES — a violation of any of these fails the whole pass

**Facts and sources**
1. **Add nothing.** No fact, number, date, name, place, causal claim, or adjective of degree that is not already on the page. If you think something is missing, note it in the change table — do not write it in.
2. **Never change a number, a date, or a proper noun.**
3. **Never alter text inside quotation marks.** Not a word, not a comma, not a truncation. Quotations are char-exact from primary sources and are shown on screen next to the audio.
4. **Never remove an attribution.** If a sentence says who is claiming something ("As the historian X puts it…", "Poland's claim is…", "For him it's…"), that attribution stays. Stripping it turns a historian's judgment into the narrator's, which is the one thing this channel cannot do.
5. **Never leave quotation marks with no owner.** If a quoted phrase's source is not named in the sentence or the one before it, either name the source or remove the quotation marks and paraphrase. Both are acceptable; a quoted judgment floating in nobody's mouth is not.
6. **Never introduce certainty the sentence didn't have.** "reported", "doubted", "some historians call it", "by the best account", "we don't know if" — these hedges are load-bearing evidence language, not padding. Keep every one.

**Cutting**
7. You may cut for tightness — the script is over its runtime target and cuts are welcome. But:
8. **If you cut a sentence, repair everything downstream that pointed at it.** Every "it / them / that / those / one of them / this / the same man" must still have an unmistakable noun it refers to. The last pass cut a sentence and left a pronoun pointing at the wrong group of people. Re-read every pronoun in a paragraph you have cut from.
9. **Never cut the only place a claim's reason is given.** If a sentence is the *why* behind the sentence next to it, it stays even if it looks like fat.

**Sentence construction**
10. **No semicolons, ever.** They cannot be read aloud. Resolve to a period or a connector.
11. **No colons except before a quotation or a list.** Maximum two elsewhere in the whole script.
12. **No verbless fragments in a series.** "Some for the wage. Some for the food. And some for the power." is banned. Give each one a verb, or flow them into one sentence. Fragments in a row are his single strongest "this was written by a machine" tell.
13. **No subordinate or participial clause stacked before the main verb.** Not "Expecting the map to be redrawn, the leadership believed…" and not "Only then did they…". Lead with who did what.
14. **No sentence over ~30 words**, and no sentence whose main verb arrives late.
15. **No rhetorical question** unless the very next sentence answers it.

**Words**
16. Banned outright: *consequently, thereby, nevertheless, subsequently, moreover, furthermore, ultimately, indeed, crucially, notably, it is worth noting, arguably.*
17. Banned openers: *"Here's…", "Now,", "Look,", "Listen,", "But here's the thing."*
18. **"really" is not his word. "very" is.** If you want an intensifier, use *very*, and use it rarely.
19. **Prefer the plainer verb every single time.** *called* over *denounced*. *didn't want* over *had no interest in*. *was the biggest problem* over *remained the greatest obstacle*. *got trained* over *gained training*. The previous pass on this script went more formal in nine places; that is the exact direction you must not go.
20. **One elevated word per plain sentence, never a cluster.**
21. **No metaphor, no minted image, no balanced antithesis** ("not X, but Y" symmetry). Plain mechanism instead. This channel's audience is here for how things worked.

### 4. What you are trying to add — the actual point of this pass

His unscripted speech and his written scripts differ in measurable ways. Close the gap.

| marker | this script | target | how he actually talks |
|---|---|---|---|
| `so` per 1,000 | 4.6 | **≥ 12** | 12.1 |
| `but` per 1,000 | 3.5 | **8–10, no more** | 9.4 |
| **`so` : `but` ratio** | 1.3 | **≥ 1.2 — `so` must outnumber `but`** | **1.29** |
| `and` per 1,000 | 28.5 | **32–34, never lower** | 34.2 |
| `very` | 1 | 2–3 total | his intensifier |
| clause-final hedges | 0 | 2–3 total, opinion beats only | constitutive |
| median sentence length | 13 words | 11–16 | 13 ✓ |

**Your primary job is `so`.** He reasons out loud, and his causal spine is *so* — he uses it to move forward, and *but* only where the logic genuinely turns. Find every joint where he would say **so** out loud and the page uses a period, a comma, a dash, or nothing, and put the word in.

**⚠ THE TRAP — a previous pass of this exact job fell straight into it.** Asked to raise `so`+`but`, it stuffed `but`, because *but* can be bolted to the front of almost any sentence while *so* requires a real causal relationship. It reached 20.6 combined with **30 `but` against 23 `so`** — ratio 0.77, when his real ratio is 1.29 — put "But" at the start of 24 sentences and 7 paragraphs, and paid for it by dropping `and` from 28.5 to 25.6. It hit the combined number and moved *away* from him.

So: **never insert a connector where there is no real causal or contrastive relationship.** A `but` that could be deleted without changing the meaning is a defect. And **never trade `and` away** to buy connectors — `and` chaining across sentence boundaries is how he extends a case.

**Report `so` and `but` separately, with the ratio and the `and` rate. A combined number proves nothing.**

Second: **his causal stack is `so` ≫ `because`.** He does not say "which is why" or "and that meant" when he talks — those are writer's tools. Use at most one of each in the whole script.

Third, and carefully: **clause-final hedging is constitutive of his verdict register** — "…I think", "…I guess", "I would leave that in the middle", "these are claims I cannot answer". He uses "very" as his intensifier and never "really". The script has almost none of either. **Add at most three hedges and at most three "very"s in the whole script.**

**⚠ WHERE A HEDGE MAY NEVER GO — the previous pass violated this three times out of three.** Not on the killing. Not on a death toll. Not on the registry, the documents, the archives, or anything historians have found. Not on the closing thesis. A hedge on an evidentiary beat converts an attributed finding into the narrator's personal opinion, which is the exact inversion of what this channel does — "You cannot call that spontaneous" is a historians' finding, and "That is very hard to call spontaneous, I think" is him ruling in his own voice while pretending not to.

A hedge belongs **only** where he is openly giving an opinion, and he will usually have marked those himself ("in my opinion"). **If a spot does not obviously want one, leave it. Zero hedges is a pass. Three misplaced hedges is a failure.**

Fourth: **replace abstract nouns with people and verbs.** "the count comes from Motyka's research" → "Motyka counted". "there is disagreement about the framing" → "they disagree about the framing". This is his largest measured drift after connectors.

### 5. Structure and logic pass

Run this over the whole script, in one read, before you touch wording.

**The open-question ledger.** The viewer holds a running list of questions the script has raised. A paragraph is legal only if it answers the question currently open and raises the next one. Five violations — flag every instance you find, and fix the ones you can fix without adding facts:

- **V1** — a term, name or claim used before it has been introduced.
- **V2** — answering a question the viewer never asked.
- **V3** — raising a question and never answering it.
- **V4** — re-answering a question already closed. This is what repetition actually is. **⚠ But a restated fact is not automatically V4.** A fact may be stated twice because its *position* is doing work — in this script the death toll appears in the overview and again in the chronology, deliberately, so that the scale is established **before** the honoring is explained; without that order the video reads as pre-emptive minimisation. The previous pass cut the first instance as repetition and broke the guard. **Before cutting any restatement, ask what its position is doing. If you cannot answer, leave it and flag it instead.**
- **V5** — breaking a promise the script made earlier (if the script says "an order would have left three things behind", all three must be dealt with, in that order).

**⚠ One more failure mode from the previous pass: a flow edit that invents an actor.** It turned "After he was captured, Stelmashchuk told Soviet interrogators…" into "Soviet interrogators captured Stelmashchuk. He told them…" — giving the capture an actor the page never named, and the wrong one. When you convert a passive or a subordinate clause into an active sentence, **you must not supply the missing subject from inference.** If the page does not say who did it, keep the construction or restructure around it.

**Transitions.** His single most persistent complaint about his own writing. A transition must point forward and name the next beat's actual subject, or state the causal link to it. Two beats sitting adjacent with nothing joining them is a defect. Never bridge with a content-free announcement ("the deeper point is", "let's step back", "here's why that matters") — name the thing.

**Back-pointers.** Any "again", "this time", "back to", "that betrayal", "the same man" must have something earlier in the script it genuinely points at. Check each one.

### 6. Output format

Return two things.

**A.** The full rewritten script, same chapter headings, VO only.

**B.** A change table. Every single change, one row each. This is not optional and it is not a summary — it is how the changes get fact-checked afterwards:

| # | chapter | before | after | type | why |
|---|---|---|---|---|---|

`type` is one of: `connector` · `plainer-word` · `split` · `flow` · `cut` · `referent-repair` · `logic` · `hedge` · `transition`.

Then, separately, list:
- **Anything you cut**, with the reason, so it can be checked against the source ledger.
- **Anything you wanted to change but didn't** because it would have required adding a fact.
- **Every V1–V5 logic violation you found**, including ones you could not fix.
- **Your final measured `so`+`but` per 1,000 words.**

---

## AFTER YOU GET IT BACK

Bring the change table here. The fact-check runs on:
- every `cut` row against `01-VERIFIED-RESEARCH.md` (did a claim lose its support?)
- every row touching a quotation, a number, or a named historian against `_research/SOURCE-GENEALOGY.md`
- the binding landmines in the `SCRIPT.md` header — the 1943 letter is **never** "signed", the Klymchak report is "preserved in a Soviet case file, reproduced by historians", 70K:20K is **Snyder's** figure from Motyka's research and never Motyka's own, 50–60K and 36,000+ named, the archive argument lives once in CH9 in narrow form
- `python -m tools.voice_lint` — 0 HARD is the gate
- **every locked line in the corpus §1 — diff the returned script against them; any that moved is a rejection**
- the connector counts re-measured independently and **split**: `so` rate, `but` rate, the ratio, and the `and` rate. Never accept a combined `so`+`but` figure as evidence.
- every hedge and every `very`, checked for placement — an evidentiary beat is a rejection
