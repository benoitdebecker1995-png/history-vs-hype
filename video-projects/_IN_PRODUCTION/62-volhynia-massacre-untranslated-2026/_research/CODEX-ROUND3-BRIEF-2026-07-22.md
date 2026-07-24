# ROUND 3 — read-check and lock
**2026-07-22. Round 2 verified and merged. Draft: 2,745 words ≈ 14.7 min · 0 HARD · 0 WARN.**

## What happened to your Round 2

**All 18 change-table rows applied.** Two execution errors fixed on my side, not sent back:

1. **Change #1 was appended, not substituted.** The cold open ended up with "The attacks and reports can show whether the massacre was organized" *and* "The reports show that the killing was organized" — the beat answered its own question and killed the promise structure. Now: *"…The harder question is whether the decision can be traced to the UPA leadership. That is the one thing nobody can produce — an order from the top that everyone can inspect."*
2. **Change #12 traded an abstraction stack for a symmetric triad** and tripped the linter's triad-density rule. Split into two uneven sentences: *"The timing and the scale were different. The UPA hit villages on the same days, and its commanders reported the results up the chain."*

## The four held decisions — his calls, all applied

| decision | his pick |
|---|---|
| Exact wording | **Your B.** First-person research act. He agreed the impersonal version was an overcorrection. |
| "denounced" | **Changed to "called."** The plainer-verb rule wins; the T7 "taken as-is" was passive acceptance inside a chapter he was reviewing for other things, not a pick. |
| Reconciliation placement | **Moved to CH9**, merged with the exhumation tail so it is stated once: *"It's not that Ukraine has offered Poland nothing. The two countries signed a reconciliation declaration in 1997, and in 2023 the two presidents mourned the victims together. But those ceremonies never settled Poland's demand to dig up the graves and name the dead."* Closes your V2 and V4. |
| Desertion | **Taken**, with one change — see below. |

## ⚠ A ninth lock violation, in the line you proposed cutting

Your costed swap displaced *"By then, the movement had both the idea of removing Poles and trained men capable of doing it."*

**That line is itself a drift from a locked line.** Corpus §1 L60, T1: **"Now the idea had men to carry it out."**

So the swap was cutting the corrupted form of his own landing. It is now **restored** rather than cut, and your desertion sentence was added on top. Net +8 words instead of net 0, and he keeps his landing in his own words. Better outcome than the swap you costed — but you could not have seen it, because the drifted version reads perfectly well.

## The rule that ninth violation reveals — put this at the top of `VOICE-RULES-DERIVED-2026-07-22.md`

Nine lock violations were found in this draft across two sessions. **Every one of them moved in the same direction**, and none of them was bad writing:

| his line | what replaced it | the move |
|---|---|---|
| "This state lasted for about three years." | "It lasted about three years." | concrete noun → pronoun |
| "The east of Ukraine fell… In the west, Volhynia…" | one merged sentence | two sentences → one |
| "That's what I try to do on this channel. I go to the sources…" | em-dash merge | two sentences → one |
| "So that's why honoring these men is useful now." | "gives Ukraine a history of resistance to Moscow" | plain landing → abstract summary |
| "Now the idea had men to carry it out." | "the movement had both the idea… and trained men capable…" | plain landing → abstract summary |
| "reporting a finished job up to his superiors" | "telling his superiors he had destroyed…" | verbal phrase → nominal shuffle |
| "the intellectual father of the Organization of Ukrainian Nationalists" | "…of the OUN" | expansion → acronym |
| "calls Russia's atrocities at Bucha what they are" | "…by their name" | idiom → generic phrase |
| "We should try to look… without justifying everything that they did" | "As long as we don't downplay…" | recast into a conditional |

**Derived rule — `CONFIRMED`, n=9, and it is the most useful thing this session produced:**

> **His lines are not lost to bad writing. They are lost to tidying.** Every violation was grammatical, most were *shorter*, several were arguably clearer in isolation, and not one would be caught by a linter or a style rule — because each is an improvement by every standard except the one that matters. The specific moves are: merging two of his sentences into one, replacing a concrete noun with a pronoun, and converting a plain landing into an abstract summary of itself.
>
> **Operational consequence:** a locked line cannot be protected by any rule about quality. It can only be protected by the diff. Any pass that touches a chapter containing locked lines must diff against corpus §1 *before* returning, not after — and "I only tightened it" is the exact signature of the failure, not a defence.

Fold this into the corpus header and `VOICE-PROFILE.md` at end of session.

## Round 3 — what to do now

Read the merged `VO-v8-referee-draft.md` start to finish **as one performance**, out loud in your head, at speaking pace. Nothing else.

Return only:
1. **Every place you stumble** — with the specific reason (breath too long, referent the ear can't carry, two stresses colliding, a joint that needs a connector the page doesn't have). Line-level, with a fix.
2. **Any beat where the argument's causal thread drops** for a listener who cannot scroll back.
3. **A verdict: film it, or name the one thing that must change first.**

**No new ideas. No restructuring. No cuts unless something is genuinely unreadable aloud.** He films tomorrow.

Three known-and-accepted items — do not re-flag them:
- The closing rhetorical question stands unanswered by his explicit choice.
- `so`:`but` is 1.00 against his natural 1.29, and `and` is 28.4 against his 34.2. **Four written passes have now failed to close this. It is a microphone problem, not a page problem** — do not try to fix it by inserting connectors.
- Runtime 14.7 against a 12-minute channel cap, with a twice-confirmed exemption.
