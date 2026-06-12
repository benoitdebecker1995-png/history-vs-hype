# CALIBRATION-CORPUS.md — script-accuracy lesson corpus

> **Purpose:** single accumulation point for every script-calibration lesson (UPGRADE-PLAN Phase S). Feeds the S8 contradiction/gap report, the S9/S10 grill sessions, and the S11 agent-diff proposals for script-writer-v2 v18.
>
> **Created:** 2026-06-12 (S1 — consolidation of existing artifacts from #56, #57, #58). Entries here are CONSOLIDATED, not re-derived — each cites its source artifact.

## How to read an entry

**Axis tags** (every entry has exactly one primary):
- `[V]` voice — register, diction, rhythm, delivery
- `[St]` structure — beat order, transitions, architecture, visual blocking
- `[Su]` substance — claims, evidence, attribution, steelman quality
- `[P]` process — revision economy, collaboration mechanics, tooling, gates

**Tier** (source-tier rule, per `memory/feedback-postmortem-methodology.md`):
- `VALIDATED` — the creator made/approved this edit or stated the rule (read-aloud corrections, locked-script diffs, live grill picks)
- `HYPOTHESIS` — inferred from SRT deviations, retention mappings, or tool scans; plausible but not creator-confirmed
- `IDEA` — imported from outside (reference creators, craft literature); must be tested before becoming a rule (rules-hedge principle)

**Dedupe rule:** lessons already canonical in `.claude/REFERENCE/VOICE-PROFILE.md` are listed as one-line cross-refs (marked `→ VOICE-PROFILE`), never duplicated. Same for rules already canonical in a memory feedback file (marked `→ memory`).

---

## #56 — Atlantic Slave Trade ("No Lassos") — published

Source artifacts: `video-projects/_ARCHIVED/published/56-no-lassos-atlantic-slave-trade-origin-2026/` — REWRITE-PLAN-2026-05-25.md, PROSE-SCAN-2026-05-24.md, PROSE-SCAN-2026-05-25.md, READ-ALOUD-v3..v8, FIG-TREE-EDIT-PASS-PROPOSAL.md, FIG-TREE-EDIT-PASS-PREDICTIONS.md.

### 56-01 [Su] Steelman the RIGHT target — VALIDATED
The concede beat must address the actual strongest version of the opposing claim, not an adjacent one. #56's Ahmed Baba (Muslim-framework) steelman didn't reach the real right-wing claim (sub-Saharan inter-polity slavery); the video would have failed its debunking goal with the wrong claim refuted. Fix required a second steelman half (Davis p. 221 Wolof/Bamana saleable-vs-non-saleable). *Source: REWRITE-PLAN-2026-05-25.md §C1, §D.2.*

### 56-02 [Su] Front-load what an ambiguous quote proves — VALIDATED
When a quote opens by appearing to CONFIRM the claim being debunked (de Marees: "They also enslave one another…"), set up what it proves BEFORE playing it, and interpret it explicitly after. Never let a quote land cold and hope the viewer draws the right inference. *Source: REWRITE-PLAN-2026-05-25.md §D.7 (CONFIRMATION RISK).*

### 56-03 [Su] De-overclaim or earn it — VALIDATED
When the script asserts more than its evidence proves ("engineered top-down… before it even scaled"), either lower the claim language or add the evidence beat that earns it. #56 did both: softened Romanus Pontifex claims AND added the bridge beat that proves operationalization (Russell p. 250, Lovejoy Table 3.1, Donnan asiento). *Source: REWRITE-PLAN-2026-05-25.md §C3, §D.8.*

### 56-04 [St] Bridge beats can do quadruple duty — VALIDATED
An 80-year evidentiary gap (1444 raids → 1526 Afonso letter) is a structural hole the viewer feels. The new bridge beat simultaneously: filled the gap, lowered an overclaim elsewhere (by proving it), pre-staged a later evidence beat, and smoothed an abrupt transition. When a structural fix is needed, look for the single beat that resolves multiple flags. *Source: REWRITE-PLAN-2026-05-25.md §D.3.*

### 56-05 [V] Register whack-a-mole — rewrites swap jargon clusters, they don't remove them — VALIDATED
v2's industrial cluster (engineered / retooled / rewiring / top-down / scaled) was excised in v3 — and replaced by a bureaucratic cluster (papally-licensed extraction / legal framework / operationalized / mass commodity slavery). A register fix needs a RE-SCAN after rewrite; newly-written sections are where new flags concentrate (Bridge + Evidence 4 added 2 new HIGH flags). *Source: PROSE-SCAN-2026-05-25.md PART B (v2 survival check: 5 clean exits, 2 regressions, 3 partials).*

### 56-06 [P] Read-aloud and corpus-scan are complementary, not redundant — VALIDATED
Read-aloud flags are cadence/sentence-shape friction (embedded arithmetic, no breath point, back-compute); corpus-scan flags are vocabulary/register friction that reads smoothly silently (abstract noun pile-ups). Only 1 of ~21 flags converged across both tools on v2. Run both; treat convergent flags as highest-confidence. → memory `feedback-read-aloud-catches-logic` (read-aloud = T1 for logic; AI tools = T2 for surface vocab). *Source: PROSE-SCAN-2026-05-24.md PART C.*

### 56-07 [P] NotebookLM cannot separate editing-rhythm from voice-register — VALIDATED
Asked blind for Fig-Tree-STYLE edits with an explicit voice-preservation constraint, NLM ported parasocial verbal signatures anyway ("backstory over," "Got all that? Good.") — 4 violations on #52, 6 on #56; not a one-off. It also operated at lower resolution on document-treatment (missed the 5 biggest visual-leverage edits). The port/skip/translate filter is the load-bearing layer and must stay Claude-side. *Source: FIG-TREE-EDIT-PASS-PROPOSAL.md §6.*

### 56-08 [St] Spatial-pointer document reveal + stay-on-face quote performance generalize across formats — VALIDATED (adoption) / HYPOTHESIS (retention effect)
Document reveal with pointer language used 4× in #52, 5× in #56; stay-on-face for verbatim quote performance 2× / 4×. Both transferred cleanly from Format C to Format A/B and were adopted by the creator. The retention payoff remains a pre-registered prediction (results section never filled in — S4 should close this loop). *Source: FIG-TREE-EDIT-PASS-PROPOSAL.md §4; FIG-TREE-EDIT-PASS-PREDICTIONS.md §7 (TBD).*

### 56-09 [St] Numeric-comparison spatial pointer — VALIDATED (adoption) / HYPOTHESIS (effect)
When the script contains a quantitative comparison (1,000/yr vs 80,000/yr), build a two-column graphic and point at each value while reading ("Look at the numbers" → POINTER LEFT → POINTER RIGHT → back to face). Surfaced as a new pattern in #56; sibling of the document-reveal pointer. *Source: FIG-TREE-EDIT-PASS-PROPOSAL.md §4 (6th candidate rule).*

### 56-10 [P] Pre-register falsifiable predictions before filming — VALIDATED
The predictions file was written BEFORE filming, with timestamps to check, falsification conditions, confounds, and decision rules — explicitly to prevent hindsight bias when reading retention curves. This is the channel's template for testing any script-level rule change (directly reusable for the Panama v18 test). *Source: FIG-TREE-EDIT-PASS-PREDICTIONS.md (whole-file pattern).*

### 56-11 [St] Lock-version edits v5→v6: claim-first hook; paraphrase archaic quotes in VO, verbatim on card; example-first economics — VALIDATED
Three systematic lock-direction edits: (a) hook restructured claim-first (open on the claim being debunked, then the scene — → memory `feedback-script-structural-architecture` P1); (b) long archaic verbatims (Equiano, Gorrevod) paraphrased in his voice in VO with the verbatim held on screen; (c) abstract economics (Manning) leads with the concrete example (15-to-1 Dahomey price ratio) before the principle — → memory `feedback-script-structural-architecture` P4 concrete-first. *Source: READ-ALOUD-v6-2026-05-25.md header + body diff vs v5.*

### 56-12 [V] Lock-version edits v7→v8: cut the aphoristic mirrored binary; cut date-math openers — VALIDATED
At final lock he removed "Read it. The denial contains the confession." (quotable but op-ed-register mirrored aphorism — the Fig Tree scan had flagged it MEDIUM; he kept it for 4 versions, cut it at lock) and removed the "Sixty-three years after Romanus Pontifex," date-math opener. Also: the streamer-position paraphrase was verified against actual transcripts before lock (never paraphrase an opponent unverified). *Source: READ-ALOUD-v8-2026-05-25.md header.*

### 56-13 [St] Method-declaration bridge beat — VALIDATED
v8 added a 15-second standalone beat between hook and concede: "What I want to do in this video is go through some primary sources to clear up this misconception. But before we do that, let me make something clear." → memory `feedback-script-structural-architecture` P6 (method declaration). *Source: READ-ALOUD-v8-2026-05-25.md METHOD BRIDGE.*

### 56-14 [Su] Closing must name only what was shown — VALIDATED
"the desperate letters of African kings" (plural) when only ONE king's letter was shown = factual error caught by the creator. Montage/recap language must match the evidence count exactly. *Source: REWRITE-PLAN-2026-05-25.md §C5, §D.9.*

---

## #57 — Piri Reis Map — published

Source artifacts: `video-projects/_ARCHIVED/published/57-piri-reis-map-ottoman-2026/` — WRITER-LESSONS.md, VOICE-FINGERPRINT.md, REVISION-BRIEF-v6.md.

### 57-01 [Su] Report the claim — don't sell it — VALIDATED
The single biggest recurring error across v1→v4: narrating/inflating the opposing claim instead of stating it flat ("the only way to draw a map this accurate was from above" = building von Däniken's argument for him). State the claim plainly; let the document prosecute. Corollary: fix loose verbs to literal truth ("the landmass WAS Antarctica" → "the bottom DEPICTS Antarctica"). And never strawman — represent the claim as its strongest proponent actually makes it. *Source: WRITER-LESSONS.md §1.1; VOICE-FINGERPRINT.md "THE ROOT ERROR".*

### 57-02 [P] Digest creator shorthand — never parrot it — VALIDATED
When the creator floats a term ("status quaestionis") or rough sentence, that's thinking out loud, not the line. Extract the idea, write the publication version in his voice. Two parroting failure modes: pasting his term verbatim; handing the decision back as an A/B ("your call"). He wants the digested, committed deliverable. *Source: WRITER-LESSONS.md §1.2.*

### 57-03 [St] Scope-check against the title before drafting any beat — VALIDATED
The #57 rewrite consumed hours because the script was a Hancock debunk when the title was "What the Piri Reis Map Actually Says." When the title is "What X says/proves," the structure = guided tour of X (3-5 regions of the document); the opposing claim appears at each stop as a one-line foil; the debunk is implicit in showing what's actually there. "What is the video we're trying to make" = his scope-drift reset signal. *Source: WRITER-LESSONS.md §1.3, §7, §4.4.*

### 57-04 [P] Length discipline — clarity fixes bloat; over-cap means refocus, not trim — VALIDATED
Every clarity-fix added concrete detail: ~1,800 → ~3,100 words across one read-through. Recovering required killing whole sections or refocusing the structure (what won). Word-count at length-decision moments; 12-min cap ≈ 1,950 words @163wpm. *Source: WRITER-LESSONS.md §1.4, §6.6.*

### 57-05 [P] The read-through is the gate — and it catches different bug classes — VALIDATED
Read-aloud catches: cold pronouns ("That's slow" — that's WHAT?), buried logic (1528 update never said WHY it mattered), undefined antecedents, recap-redundancy, vestigial references from prior structures. Earlier-approved phrasings may need cutting once their context changes — flag the override transparently. *Source: WRITER-LESSONS.md §1.5, §4.5.*

### 57-06 [St] Filler-beat catalogue — four beat types that are usually cut — VALIDATED
(a) "real research vs fake research" meta beats (read as preaching); (b) moving-claim enumeration arcs across decades (recap-feel in delivery — one-line framing instead); (c) origin-of-the-claim history (Mallery/Hapgood/USAF — the document's own labels do the debunking); (d) corroborating-science stacking after the primary-source nail ("one nail per debunk"). *Source: WRITER-LESSONS.md §3.3.*

### 57-07 [P] Creator flag vocabulary — decoder table — VALIDATED
"doesn't make sense"/"huh?" = cold pronoun or buried logic → find and fix it. "cringey" = performative metadiscourse/slang/sanctimony → CUT, don't soften. "random" = missing bridge or beat doesn't belong. "awkward sentence" = state the idea plainly. "too much prose" = strip explainer prose, trust the evidence. "more phrases" = he wants more 2-3-option checkpoints. "keep X in VO" = content decision, honor it. *Source: WRITER-LESSONS.md §4.2; REVISION-BRIEF-v6.md collaboration block.*

### 57-08 [P] Propose, don't act — one beat at a time, explicit yes before writing — VALIDATED
Never batch; never write a file unprompted; never rewrite a whole file (unprompted full-file writes were rejected twice). "Drive, don't punt" applies to the THINKING (analysis, notebook query, recommendation), not to writing without approval. Options only when there's a genuine choice (max 3, different angles, mark a recommendation). *Source: REVISION-BRIEF-v6.md ⛔ OPERATING RULE.*

### 57-09 [P] Intent-first querying — VALIDATED
For each paragraph: state the intent plainly FIRST, then query the notebook against that intent (not the topic), and let the result confirm or redirect. Worked examples where the notebook redirected a wrong premise: "translation was wrong" → the error is Piri's own; "inscription 10 proves Brazil" → toponyms+cartometry do; "Hapgood made it up" → he misread the map. → memory `feedback-script-revision-grounding` (notebook-first is now a HARD rule). *Source: REVISION-BRIEF-v6.md §loop + notebook-usage worked examples.*

### 57-10 [St] Flow-check in + out at every paragraph seam — VALIDATED
At each paragraph: does the opening pronoun/connector have a clear antecedent in the previous paragraph? Does the ending set up the next? Cold pronouns and stranded transitions live at the seams, and they're invisible in isolated line review. *Source: REVISION-BRIEF-v6.md §loop step 3.*

### 57-11 [V] SRT headline finding: his ad-libs are more economical and concrete — never more gimmicky — HYPOTHESIS (SRT-derived)
When he changes a scripted line live he makes it plainer, adds a concrete noun, or breaks it into an enumerated beat; he never adds YouTuber garnish. So "reads cringey" almost always = the WRITER added garnish. Tier note: SRT-derived (hypothesis per postmortem-methodology), but consistent with all later VALIDATED grill data. ⚠️ VOICE-PROFILE header explicitly supersedes SRT fingerprints where they conflict (the SRTs are heavily edited). *Source: VOICE-FINGERPRINT.md headline.*

### 57-12 [V] The cringe inventory — 13 assistant-introduced phrasings, all stripped — VALIDATED
Concrete banlist of what the assistant inserted across v1-v4 and the creator cut: "Here's what almost no video will tell you," "signed by the man they call the mystery," "let's play their game," "the receipt," "hot take," "keep that test in your pocket," "mystery-sellers," "let's do what nobody does," "If there's anything you remember from this video…," vestigial references, label-without-substance ("That's a Rorschach test"), close-recaps. Largely absorbed into VOICE-PROFILE's cringe no-list — kept here as the historical instance record with per-line context. *Source: WRITER-LESSONS.md §5.2.*

### 57-13 [P] Two-stage gate: gut-pick first, tool/critic second — VALIDATED
Creator's gut pick first; scorer/critic only if unsure. Don't override a clearly on-brand gut pick with scorer points (he rejected scorer-pushed titles that read clickbait). *Source: WRITER-LESSONS.md §6.3.*

### 57-14 [V] Voice rules from #57 now canonical elsewhere — cross-refs only
The full DO/DON'T catalogue (enumeration cadence, "There's just one problem," plain-concrete verbs, credential+name+"put it," dry irony at the opponent's material, fan-directed concession, "let's" is his, "basically" OK, understated-honesty move, "so busy…they…" irony, counter the conspiracy STRUCTURE) → `VOICE-PROFILE.md` (canonical, supersedes) + `VOICE-FINGERPRINT.md` (instance record). Do not re-derive from here; the profile wins on conflict.

---

## #58 — Kurdistan Statelessness — script locked 2026-06-10

Source artifacts: `video-projects/_READY_TO_FILM/58-kurdistan-statelessness-2026/VOICE-DRILL-RESUME.md`; `memory/58-kurdistan-production-state.md`. Note: nearly all #58 VOICE rules were folded into VOICE-PROFILE.md live during the sessions (2026-06-06 → 2026-06-10 dated entries there) — those are cross-refs. What follows is what is NOT canonical elsewhere.

### 58-01 [Su] Attribution drift in broad notebook queries — scoped round-trip required — VALIDATED
A broad notebook query mis-attributed 8 quotes (to McDowall/Olson/James/Ateş etc.) while every citation actually collapsed to ONE source (Eppel). Only a scoped round-trip per quote made the cards safe. → memory `feedback-notebook-citation-grounding` + `feedback-attribution-audit`. *Source: VOICE-DRILL-RESUME.md Batch 4 note.*

### 58-02 [Su] Re-confirm verbatim provenance at the last gate — "verified" notes go stale — VALIDATED
McDowall "nuisance, not resolution" carried a 2026-06-06 "round-trip verified" note — and failed verbatim re-confirmation on 2026-06-12 (2 NLM queries). Retired and swapped for the verified "cat's paw" p.2. A verification note is a claim about a past query, not a property of the quote; re-confirm load-bearing verbatims at the final pass. *Source: memory/58-kurdistan-production-state.md 2026-06-12.*

### 58-03 [Su] Notebook as anti-yes-man guard on mechanism beats — VALIDATED
During the T1 read-aloud, grounding queries were run for EVERY mechanism beat before rewriting (1922 buy-off motive; Lausanne contains zero instances of "Kurd"; 1970 Manifesto → 1974 gutted-autonomy revolt cause; post-1975 Iran-alliance → Anfal) — and caught multiple would-have-shipped errors, including a real one (Ubeydullah was NOT "a religious leader, not a military one" — he raised 15-20k men). → memory `feedback-script-revision-grounding` (the ⛔ rule). *Source: VOICE-DRILL-RESUME.md session 6; memory 2026-06-09/06-10.*

### 58-04 [St] Mine your OWN published analogs as a negative corpus — VALIDATED
The creator's two closest published statelessness analogs (#Kashmir, #Western-Sahara) were saturated with now-banned tics ("the receipt," "What if I told you," power-sermon staccato close) — confirming them as a regression guard, not a style source. Before writing a new script in a topic family, check whether the channel's own precedents are positive or negative examples. *Source: VOICE-DRILL-RESUME.md session 5.*

### 58-05 [P] Pre-show lock test kills grill rounds — VALIDATED
The #58 sessions ran ~14 rounds largely because options reached the creator failing basic checks; operationalizing his lock-test ("I'd never talk to someone like this") into the 9-check Bar-talk Lock Test run BEFORE showing options was the round-count fix. → VOICE-PROFILE ⭐ BAR-TALK LOCK TEST (canonical). Process lesson kept here: the revision-economy lever is pre-filtering candidates, not generating more of them. *Source: VOICE-DRILL-RESUME.md resume header.*

### 58-06 [P] Calibration law: completeness → MORE; device → LEAN — cross-ref
On completeness beats (the WHY of a claim) he picks the fuller option; on device/transition beats he picks the leaner. All prediction misses in sessions 4-6 were this pendulum, never register. → VOICE-PROFILE (Bar-talk checks #3/#5) + memory `feedback-grill-easier`. *Source: VOICE-DRILL-RESUME.md sessions 4-5.*

### 58-07 [St] Saturated-lane check can kill a beat as late as lock — VALIDATED
Sykes-Picot was dropped ENTIRELY at the lock session (cold-open myth-stack + Lausanne beat) because competitor-gap analysis showed it as the saturated lane every competitor runs. Structural differentiation rules apply to individual beats, not just topic selection — and it's never too late to cut a beat competitors own. *Source: memory/58-kurdistan-production-state.md 2026-06-10.*

### 58-08 [P] "Make it better" on an at-cap script = swap/triage, not add — VALIDATED
Adding bulletproofing primaries without cutting pushed #58 over the 12-min cap; the fix was tightening the addition itself and triaging (HELD list for good-but-unaffordable material). Runtime is a forcing function: at cap, every addition needs a named victim. *Source: memory/58-kurdistan-production-state.md Round 8 lesson.*

### 58-09 [P] Honest length floor vs the cap — VALIDATED
The 12-min cap is real (r=-0.455), but a history-channel mandate has an honest floor: cutting #58 from 13.0 to 12.0 would have cost the emirate/treaty moat (the differentiator). The creator chose the moat, eyes open. Length decisions are moat-protection decisions, not just retention math. → memory `feedback-editor-agent-wordcount-untrusted` (length-floor note). *Source: memory/58-kurdistan-production-state.md 2026-06-10.*

### 58-10 [P] Passes-to-lock baseline (#58, v17 era) — VALIDATED (KPI datum)
#58 voice/lock trajectory: ~6 drill/grill sessions (2026-06-06 → 06-09) + full T1 read-aloud (~18 beats revised live) + a 12-min cut pass + post-lock quality pass (2026-06-12). KPI definition note: the plan counts PASSES-TO-LOCK; #58's baseline ≈ 2-3 full passes on the script body (drills were line-level calibration, not full passes). Panama (v18) is the first clean comparison. *Source: VOICE-DRILL-RESUME.md + memory production-state timeline.*

### 58-11 [V] #58 voice rules — cross-refs only
All locked into VOICE-PROFILE.md with 2026-06-06→06-10 dates: flowing-not-staccato as the #1 AI tell; earned-fragment reversal ("A country." cut); synthesis beats get no runway; bridge lives at the END of the outgoing beat; continuity-of-reference ("again" needs a depicted antecedent); protect-callback-referent-when-cutting; cold-open myth-stack must match the body; quote-stack → speak one + cards; SEO first-noun rule; humor literal-first; grim-irony consequence-anchor; named-agent atrocity voice; relation-verb precision. → VOICE-PROFILE (canonical). Do not duplicate.

---

## Recurring patterns (cross-video)

*(Initially empty at S1 — populated by S2+ when a pattern appears in 2+ videos. Candidates already visible but awaiting S2 diff evidence: read-aloud-as-gate (56-06/57-05), report-don't-sell vs front-load-the-quote (56-02/57-01), length-bloat-then-refocus (57-04/58-08).)*

---

## Side files (created by later S-steps)

- `FINGERPRINT-UNSCRIPTED.md` — S5
- `REFERENCE-CREATOR-NATURALNESS.md` — S6
- `CRAFT-RULES-IMPORTED.md` — S7
- `INTERVIEW-AGENDA.md` — S8
- `AGENT-DIFF-PROPOSALS.md` — S11
- `EVAL-BASELINE.md` — S13
