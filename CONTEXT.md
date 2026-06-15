# History vs Hype — Video Content Domain

This context captures the canonical terms used when developing video content for the History vs Hype channel. Terms here define how concepts are named in scripts, research, and production decisions — not in code.

**Per-project terms live in each video folder's `GLOSSARY.md`** (e.g. #52 hijab/veil terminology and locked structure, #56 slave-trade terms). This file holds channel-wide concepts only. (Scope cleanup 2026-06-12.)

## Production terms

**Post-publish report**:
The per-video markdown artifact written after publication, recording observed performance (views, retention curve, CTR, subscribers gained), drop-off points, and human-authored lessons. Lives at `video-projects/_ARCHIVED/<slug>/POST-PUBLISH-ANALYSIS.md` or `channel-data/analyses/POST-PUBLISH-ANALYSIS-<video_id>.md`. The canonical input to `/patterns`, `/analyze`, `/retitle`, `/news-hooks`, the dashboard, and the reconcile loop — i.e., the **lessons** loop that turns raw analytics into channel learnings.
_Avoid_: "feedback file," "analysis file," "POST-PUBLISH" used as a free-floating noun. Always say "post-publish report" when the artifact is the referent.

**Auditor's edge**:
The channel's core competitive advantage: showing the primary source document on screen with page numbers and exact quotes.
_Avoid_: "Research" (too generic — the edge is in the *display*, not just the finding).

**Untranslated Evidence (series)**:
Channel sub-series built on close-reading primary documents that exist in non-English originals and have no faithful English translation. Episodes #37 Vichy, #49 Code Noir. Concept = untranslated *documents*, NOT untranslated *video topics*.
_Avoid_: using "Untranslated Evidence" for the topic-arbitrage method (importing topics from non-English YouTube channels) — that is a distinct, currently-unbranded sourcing method.

**Specificity bomb**:
Hook type scoring 5.4x retention lift (85-video niche corpus). Requires a named person, a named document, and a concrete surprising fact — not a general claim.

**Mechanism word**:
A title-level term naming the *type of action or distortion* the video exposes — not the parties involved. Examples: "split," "partition," "forgery," "extension," "translation gap," "court paper-over-people" (mechanism), "independence problem" (mechanism). Empirically, 2026 wins (Two Countries Split a Continent 788v, 229 Ethnic Groups 439v, Somaliland Independence Problem 396v) all carry a mechanism word. 2026 sub-50 misses (Bakassi, Honduras Bay Islands, Mexico Missing Island, Tripoli) led with named parties without a mechanism word.
_Avoid_: Party-led titles ("Nigeria vs Cameroon," "Honduras vs UK," "Treaty of Tripoli...") without a mechanism word doing the work alongside.

**Parties-with-mechanism rule**:
Title-construction rule for this channel at sub-1K subs: country/treaty names are permitted in titles ONLY when the rest of the title contains a **mechanism word** that a non-specialist can recognize as the universal distortion. "Somaliland's Legal Independence *Problem*" works (mechanism: independence problem). "Nigeria vs Cameroon. The Court Chose Paper Over People" fails (mechanism is poetic, not categorical). Audience doesn't search the parties — they search the mechanism.
_Avoid_: Bare party-vs-party titles without mechanism word.

**Turn beat (generic)**:
The 15–25% runtime slot where the thesis forms for the viewer. Each video locks its own turn beat (see its GLOSSARY.md).

**Five-civilization pattern (hook-frame template)**:
Reusable hook construction: establish the same rule/pattern across 4-6 independent civilizations or cases in one sentence each — the pattern, not a single case, is the opening argument. Origin: #52 (see its GLOSSARY.md for the worked example).

**Passes-to-lock**:
The script-quality KPI: number of full top-to-bottom read-aloud or revision rounds that produce script edits before the script locks. Micro-fixes inside a round don't count as a separate pass. Reference points: #56 = 6 (READ-ALOUD v3→v8); #58 ≈ 2-3 (v17 baseline). Target: fewer passes with each script-writer calibration cycle (defined 2026-06-12, UPGRADE-PLAN Phase 1).
_Avoid_: counting line-level micro-fixes or packaging edits as passes.

## Packaging / thumbnail terms

**Thumbnail clickability**:
Whether a thumbnail earns the click. Measurable ONLY *live* — two distinct signals: native **Test & Compare** (the variant winner) and the reach-window CTR trend in `ctr_snapshots` (don't conflate them; at current traffic A/B isn't viable yet, so the operative read is the reach-window trend + single-variable swaps). There is **no pre-publish clickability score**. Pre-publish tools verify NECESSARY CONDITIONS (clarity, feed-size legibility, curiosity-gap), they do not predict the winner. See `.claude/REFERENCE/THUMBNAIL-CRAFT-RECIPE.md` and ADR 0007.
_Avoid_: calling any pre-publish number (CLIP differentiation, a checker score) a "clickability" measure — that was the false-confidence bug fixed 2026-06-14.

**Thumbnail differentiation**:
How visually unlike the competitor shelf a thumbnail is (CLIP cosine, `thumbnail_image_audit`). **Informational only** — a low-information blob scores highly "differentiated" precisely because it's empty. Differentiation ≠ clickability.

**Thumbnail operation**:
The job the overlay+visual performs — COMPRESSION, DOSSIER METAPHOR, MECHANISM REFRAME, VISUAL ANSWER, LOCATION PROOF (`PER-CHANNEL-THUMBNAIL-PLAYBOOK.md`). The operation is the win-predictor; the *presence of a text overlay* is a **floor** (90%+ of all videos have one), not a predictor.
_Avoid_: scoring "has a text overlay" as a positive — score the operation the overlay performs.

## Voice & delivery (channel-wide)

> Canonical fingerprint and full rules: `.claude/REFERENCE/VOICE-PROFILE.md` (picks-validated, `/voice-discovery` 2026-06-05). VOICE-PROFILE.md **wins on conflict** with `WRITING-VOICE-AND-STYLE.md`. These are term definitions only; the rules/examples live in the profile.

**Bar-talk register**:
The creator's spoken DELIVERY — plain, conversational, calm explanation, "like me talking to people in a bar." The *delivery* axis; **Calm Prosecutor** is the *stance* axis (weighs evidence, concedes, reaches verdicts, never polemic). Synthesis: a calm prosecutor explaining the case to a friend in a bar.
_Avoid_: reading "bar-talk" as license for folksy/slangy padding ("a bunch of", "little") or for ranting — it is plain + CLEAN + calm, never staccato-gimmick and never purple prose.

**Calm bar-talk ceiling**:
The explanatory lean has a hard upper bound. Explain the mechanism plainly, then stop. The two enemies are BOTH the staccato/8-word-gavel AND writerly prose. He picks the *tighter* paragraph and flags "too much prose," over-citing, and clunky transitions as standing problems.
_Avoid_: treating "explanatory" as "verbose."

**Auditor pivot**:
The on-camera spoken move that enacts the **Auditor's edge** — "So let's actually read it" (collaborative "let's", NOT first-person "So I read it"). Edge = the strategy (display the primary source); pivot = the spoken line that takes the viewer there.
_Avoid_: dressing it up; the pivot is plain and collaborative.

**Thesis-forward transition**:
A beat-to-beat bridge that names where we're going and hands directly into the next beat's subject (thesis-forward statement, or a plain causal bridge naming the next subject, or a thesis-pointed question → plain statement). This is the creator's **#1 standing weakness** — every transition must bridge, not sit adjacent.
_Avoid_: vague referents ("gets the very first one wrong" → "the very first *what*?"); calling the common story flatly "wrong" (→ "oversimplified / tells only one part").

**Concede-first**:
The creator's single most reliable scripted move (built into his natural speech): state the appeal, then deny the truth. "It's fascinating to watch. It's also, very often, just not true."
_Avoid_: leading with the rebuttal before granting what's real.

**Famous-then-puncture**:
The cold-open pattern he prefers — set the famous thing up, THEN reveal the twist ("Everyone knows Saladin… Almost nobody knows he was a Kurd"), over a bare one-liner.

**Natural→scripted translation**:
The principle that **scripted-him is calmer and tighter than unscripted-him.** His unscripted video is the source of his values, concede-instinct, and vivid concrete nouns — but raw heat becomes calm concession, long run-ons become two medium sentences, and "I guess" hedges are dropped. Gold-standard exemplar: his first unscripted video (`yt:yMAWJcjo_ug`).
_Avoid_: importing the raw unscripted passion (or the staccato of the delivered SRTs) into scripts as-is.

## Relationships

- **Calm Prosecutor** (stance) and **bar-talk register** (delivery) are the two axes of the same voice — the stance is *what he does*, the register is *how it sounds*
- **Auditor pivot** (the spoken line) enacts the **Auditor's edge** (the display strategy) on camera
- **Auditor's edge** lives in the *visual* channel (show the document, always); the voice rule "credentials sparingly" governs the *spoken* channel (attribute a quote once, crisply; never stack verbal "as historian X writes" chains). They do not conflict — different channels.
- **Concede-first** + **thesis-forward transition** are the two moves that carry the **bar-talk register** without tipping into either staccato gimmick or purple prose

## Flagged ambiguities

- "Untranslated" was used for two distinct concepts in 2026-05-07 weekend-test planning: (1) the existing **Untranslated Evidence** document series, (2) a topic-sourcing method that imports high-performing topics from non-English-language history YouTube channels. Resolved: keep Untranslated Evidence pure (documents only); the sourcing method is unbranded until retention justifies a series slot. Working titles "Foreign Desk" / "The Import" — DO NOT use in production yet.
- "Pilot" is overloaded: (a) the channel's **Pilot Episode template** (8-10 min rapid-test format from `CONTENT-TIMELINE-2026.md`), and (b) the colloquial sense ("pilot a new format" — testing anything experimental). When ambiguous, qualify as "Pilot Episode template" for (a) or "format pilot" for (b).
