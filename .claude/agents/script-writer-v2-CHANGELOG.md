# script-writer-v2 — Version History

> Extracted from the agent frontmatter (2026-05-28) to reclaim context budget so the operative rules and the Claims Ledger pass get model attention. The agent file's `version:` field now carries only the current number; the full history lives here.

> **Regression-trigger procedure (2026-07-19, LLM-CRAFT-UPGRADE-PLAN E5):** any version bump to this file must run the eval harness (`tests/unit/test_eval_harness.py` + `channel-data/calibration/EVAL-JUDGE-PROTOCOL.md`) against `channel-data/calibration/EVAL-GOLDEN-SET.md` before the new version is adopted, and record the result in `EVAL-BASELINE.md`. Full procedure there under "Regression-trigger procedure."

## v17.0 (2026-06-11 — Fable Phase 3: retention rule validation)

Every quantitative retention/engagement claim cross-examined against actual retention curves (D3 digest: 15-video cliff dataset + RETENTION-SCRIPT-CORRELATION n=42/4,200 points + HOOK-RETENTION-CORRELATION n=17). Full 50-rule verdict table: `channel-data/fable-digests/PHASE-3-RETENTION-ADJUDICATION.md`. structure-checker-v2 re-tiered in the same pass (validated→hard, hedge→soft).

- **+EVIDENCE TIERS preamble** — VALIDATED / HEDGE / RETIRED tags now appear in rule text; the two behavior-changing findings summarized up top.
- **+Rule 47 RETENTION-ZONE DISCIPLINE (Tier 1)** — the only script-level retention rules with direct own-channel support: (A) early-zone personal-authority ban — no "I went/read/checked/pulled", no multi-clause credential chains in first ~90s (early delta −0.051 n=88 vs mid −0.0001 n=10; LO_fUeX9IEQ −12.5pp at 00:15–00:18 ON its credential chain; LuLZYZWMiU4 −25.2pp at 00:21–00:32); (B) cliff-zone humility — the 2–4% drop is universal in 15/15 videos regardless of hook quality (GuL9PtXEjN0's strongest-in-dataset hook cliffs identically), so hook prose gets normal craft attention and extra revision cycles go to packaging/body; (C) statistics as the mid-video re-engagement tool (61% positive n=354; the rare genuine recoveries land on stat/evidence beats); (D) closing-third statistic mandatory + no post-verdict padding (late stats +0.001 n=114, the only zone×type cell that gains viewers; late-quarter collapses: 7fpBz6uo504 −12.3pp, UH2PddfaaR8 −15.1pp across 75→100%).
- **Rule 17 hook authority signal REMOVED from mandate (the contradiction catch):** the rule-set required "So I read/checked/found..." inside the hook — i.e., the worst-measured content type (personal_authority) in the worst-measured zone. Auditor pivot now lands at the turn; visual carrot carries hook credibility. Rule 26 "front-load one research moment in hook (Beat 3)" retired for the same reason.
- **Rule 15 myth-first demoted MANDATORY → strong default; "30.3% vs 22.4%" RETIRED as data (the conflation catch):** identical numbers to the topic-retention table (ideological 30.3 / colonial 22.4) — structure⊗topic confound; the default survives on niche-corpus support (85 transcripts). Checker Constraint U: CRITICAL → WARNING.
- **Rule 12 first-evidence-by-0:90 re-grounded:** "delays lose 15-25% and never recover" was the universal hemorrhage misread as a violation penalty; stays as channel-identity default (HEDGE). Checker Constraints A + B: CRITICAL → WARNING. Constraint B's "To understand how, you need to see..." bridge example removed (Rule 13.7 tour-guide HARD lint conflict).
- **Rule 10 duration cap confirmed VALIDATED** — the strongest surviving rule: r=−0.455 (n=47) + D3 corroboration (3 over-cap videos rank 3rd/13th/15th worst of top-15). Checker Constraint T stays CRITICAL; its formula updated from the stale 1.80x overwrite buffer (~5,400-word cap) to the two-tier 1.20x (~3,600 words; Format C → BD budgets).
- **Rule 16 turn placement aligned to the hedge:** own-channel cross-validation (n=40) found NO 25-35% retention penalty; checker turn-placement flag WARNING → INFO.
- **Rule 11 "validated across 39 videos" struck** (no surviving methodology); Rule 14 "territorial = 2,449 avg views" RETIRED (Guatemala one-video traffic distortion, 51% of channel traffic); hook-type percentages annotated with true per-cell n (36.7% is n=4).
- **"44% script survival" RETIRED as stale (user-flagged):** pre-two-tier measurement; v16+ two-tier target is 80%+. Removed from Constraint AV and checker Phase 4.5.
- **Modern-relevance "every 90s" frequency mandate RETIRED:** content type measures −0.010 (n=577), worse than narration; woven-vs-standalone check survives (HEDGE).
- **+structure-checker Constraints BE** (early-zone personal-authority scan, WARNING) **+ BF** (late-quarter collapse audit: closing-third statistic WARNING, padding scan, post-verdict length).
- Phase 2 generic-AI anti-patterns (Rule 13.7) carried unchanged.

## v16.6 (2026-06-11 — Fable Phase 2: generic-AI tell list)
- **+Rule 13 #7 "The Generic-AI Prose Engine"** — introspective tell list (what models default to when sounding incisive) cross-validated against the D2 voice triad (gold unscripted vs #56/#58 locked vs zero-guidance AI control). Headline finding: the **negation-correction engine** ("It wasn't X. It was Y.") runs at A=0 / C≈5 / B1≈9 / B2≈15 — locked scripts out-AI the AI control. Budgets: 3-4 earned correction-pairs, 1 balanced epigram/act, 1 verdict per beat (no escalating aphorism re-mints), ⅓ of paragraphs end un-buttoned, 2 colon-reveals, 2 symmetric triads outside P7 ledgers.
- Evidence + full audit: `VOICE-PROFILE.md` §"Adversarial drift audit (Fable Phase 2, 2026-06-11)". Mechanized half: 11 new HARD + 6 WARN lint rules per `channel-data/fable-digests/PHASE-2-VOICE-LINT-SPEC.md`.

## v16.5 (2026-06-05 — `/voice-discovery` canonical voice profile wired in)
- **+Tier-1 mandatory reference `VOICE-PROFILE.md`** (READ FIRST) — canonical picks-validated personal voice fingerprint from the `/voice-discovery` session (~40 line-level live picks + typed rewrites + #58 prediction validation). Where it conflicts with WRITING-VOICE-AND-STYLE.md, the profile wins.
- **+7-point "VOICE PROFILE" callout in AGENT MISSION** so every `[VERBATIM]` block starts in-voice. Headline: he's **more explanatory than the staccato/8-word-gavel emphasis suggests** (over-applied to him). Signature shape = flowing parallel clauses → em-dash → verdict-with-the-catch; never staccato two-beats.
- **Retired gimmick hooks** "But guess what?" / "guess who" (lose to plain/analytical turns); banned "One word: X" reveals.
- **Past tense default**; historical present ONLY for a single dramatic moment, never decade/era scene-setting.
- **Plain numbers** (anti-RealLifeLore — his explicit anti-voice); **atrocity = plain fact + specific *attributed* culpability**, never sensory/abstract-sermon.
- **Reference models corrected** in spec §1.1: Kraut + Alex O'Connor (not Wendover/History-Matters). Spec corrections also at §1.4 (explanatory default + historical-present refinement), §2.3 (numbers override), §1.3 (cringe additions). Gold-standard exemplar = creator's first UNSCRIPTED video (yt:yMAWJcjo_ug).

## v16.4 (2026-06-04 — Tier-2 new-channel mining: Asianometry, Mr. Beat, Step Back, Metatron)
- **+Rule 46 Defect Taxonomy 10th row — False Homogenization** (Step Back "What Nobody Is Saying About I/P") — debunk "Group X all believes Y" by mapping real internal factions ("Zionism is not a monolith"). Referee-neutral (adds nuance, doesn't pick a side) — vetted as compatible with the locked Calm-Prosecutor voice. #59-relevant.
- **SKIPPED — Pattern-Through-Repetition** (Mr. Beat): repeating an identical causal clause across N cases. Useful inductively BUT clashes with locked style — staccato feedback caps repetition at "3+ = filler" and voice-calibration warns against persona/comedy tics ("you guessed it"). Calm Prosecutor lands patterns via understatement. Not encoded by design.
- **No rule from Asianometry** (Steel Colossus) — competent narrative-mechanism; reinforces repeated-failure escalation + sourcing-honesty + reversal close (all encoded). Detached no-"you" register ≠ our voice.
- **Metatron not deep-read** — current uploads are rage-bait ("HE ANNIHILATED NOLAN", "COPE"); a live counter-example of Rule 13 #6 (Contempt Undercuts Authority), not worth the context budget.
- **Step Back doubles as the clearest counter-example** of the partisan-contempt failure (Rule 13 #6) — debunk-format video that forfeits referee neutrality ("to which I say good", "just don't watch Vox"). Reinforces, doesn't re-encode.
- Transcripts pulled + cleaned to `transcripts/{Asianometry,Mr Beat,Step Back History,Metatron}/*.txt`.

## v16.3 (2026-06-04 — Tier-1 new-channel mining: PolyMatter, Premodernist, Cynical Historian)
- **+Rule 21 C#7 Disanalogy Enumeration** (PolyMatter "Taiwan is Not Venezuela") — debunk a *false* analogy by enumerating how the two cases differ, escalating. Inverse of C#6 (true parallel breaks their logic; this breaks a false parallel they assert). **Primary tool for #59 I/P.**
- **+Rule 21 C#2 Magnitude-Bounding Concession** (PolyMatter) — concede the point is real but *smaller* than claimed, then cap it ("$15B is not nothing — still won't bankrupt the world's 2nd-largest economy"). Grants the premise, denies the *magnitude* (vs Hypothetical Concession which denies the *inference*).
- **+Rule 36 Spoken Scope Lock** (PolyMatter) — declare on-screen what the video is NOT about, then state the argument; pre-empts the morality/blame derail and the "you didn't address X" comment. One per script, after the hook.
- **+Rule 46 Defect Taxonomy 9th row — Hindsight Inflation** (Premodernist "Council of Nicaea") — treating an event as a decisive turning point contemporaries didn't experience as one; counter-device = inhabit a contemporary's POV + their own words.
- **+Rule 15 Myth-Stack cold open** (Premodernist) — rapid serial negation of 3–4 associated myths, then narrow to the one sophisticated misconception the video is actually about.
- Cynical Historian "Methodology" yielded no new script rule (taxonomy lecture; reinforces inductive close + "it's not what you think" mini-turn); orthodox→revisionist→post-revisionist frame routed to historian skill, not here.
- Transcripts pulled + cleaned to `transcripts/{PolyMatter,Premodernist,Cynical Historian}/*.txt`. Premodernist delivery is unscripted (filler/tangents) — structure mined, delivery NOT a model.

## v16.2 (2026-06-04 — Alex O'Connor argumentation mining, voice-match)
- **+Rule 21 C#6 Parallel / Symmetry Rebuttal** — apply the opponent's own inference rule to a case where it obviously fails ("born elsewhere → you wouldn't be an atheist either"; Wright brothers didn't own a 747). Attacks their inference *rule*, distinct from Source-Flip (their source) and Contradiction Catalogue (their other claims). Alex O'Connor's signature; the single highest-value rebuttal gap.
- **+Rule 21 B Generous Reconstruction / Steelman-Repair** — repair the target's botched argument before answering ("maybe you meant 'atheist' not 'secular'"); pre-empts the strawman rebuttal, makes the dismantle land as inevitable. Pairs with C+ Position Guard.
- **+Rule 46 Defect Taxonomy 8th row — Wrong Target** — the evidence is real but proves a *different* proposition than claimed ("religion causes wars" argues harm, not falsehood). Separate the proposition under debate from the adjacent one the evidence supports.
- **+Rule 18 Analogy-as-Rebuttal (micro)** — sentence-level Parallel Comparison where the concrete analogy does the logical work of killing one inference ("we should be glad cancer exists, because chemotherapy?"). Macro Parallel Comparison's micro twin.
- **+Rule 13 anti-pattern #6 — Contempt Undercuts Authority** — snark/ad hominem/venting forfeit the auditor's neutrality; early-vs-mature Alex O'Connor A/B shows the conceding voice wins. Codifies a failure mode; does NOT change the locked voice register.
- Also: added 8 competitor channels to tracking (Alex O'Connor, Premodernist, The Cynical Historian, PolyMatter, Asianometry, Metatron, Mr. Beat, Step Back History) — `competitor-channels.yaml` + `tools/intel/competitor_channels.json`, yt-dlp-verified IDs.
- Origin: research pass 2026-06-04 — Waves 5B/5C/8/8B confirmed to already cover sentence rhythm / transitions / macro-structure / most anti-patterns; the genuine gap was Alex O'Connor (flagged voice-match, never formally mined). Voice register untouched.

## v16.1 (2026-06-04 — competitor re-audit, 3 closest-match debunk scripts)
- **Rule 46 promoted candidate → validated default** — confirmed as the dominant structure of the closest-match niche debunk corpus (KB "In Defense of Columbus" 40-min source-flip, KB "Lost Cause", RFB); stripped the "NOT yet validated on our own n" hedge; still strong default, not Tier-1.
- **+Rule 46 Defect Taxonomy** (sub-section) — 7 named error categories to HUNT FOR in the target's claim (truncated quote, mistranslation, temporal compression, misattribution, selective sourcing, anachronism, false projection); complement to Rule 21's rebuttal MOVES; name the defect explicitly in VO; maps to #57 Piri Reis (false projection + temporal compression) and #58 Kurdistan (misattribution).
- **+Rule 45 Conceptual-frame bookend** — reconciles Rule 45 (cut the meta-thesis) with Rule 36 (thesis bigger than case): case-is-the-point → cut; thesis-bigger-than-case → keep the frame and bookend (open + close on the abstraction). Validated on KB Columbus + Kraut Vodka, both of which open and close on a universal claim.
- **+Rule 21 C+ Position Guard** — distinct from steelmanning the opponent: protects the CREATOR's own position in contrarian/auditor's-edge debunks from being misread as advocacy ("Am I saying Columbus was good? No."); place at the 2–3 most-exculpatory-sounding beats; highest relevance to #59 I/P split-verdict format.
- Origin: re-audit of Knowing Better (Lost Cause, In Defense of Columbus) + Kraut (How Vodka Ruined Russia) against v16.0 encoded structure, 2026-06-04. Architecture otherwise held up; these are the 4 genuine gaps. (5th candidate — delayed attribution on famous names as a Rule 8 exception — deferred to user decision; not encoded.)

## v16.0 (2026-05-27 — Video #52 Hijab postmortem)
- **+Rule 43 Myth-Narration Skip** (Tier 2) — for famous myths, skip the "here's how the story goes" standard narration act; audience pre-loads the myth, reciting it stalls; Hook → Turn → Dismantling works without it; n=2 Manhattan+Hijab.
- **+Rule 44 Long-Quote Split** (Tier 2) — delegated verbatim quotes >30 words split into VO punchline + [ON SCREEN] full text; n=2 Manhattan+Hijab, break point ≈30 words confirmed.
- **+Rule 45 Evidence-Anchored Close** (Tier 2) — when closer, audit whether the meta-thesis sentence does work the evidence-comparison sentence isn't already doing; if not, cut meta-thesis, keep evidence comparison; n=2 Tripoli+Hijab, user-confirmed deliberate at Hijab.
- **+Rule 42 sub-rule E (Inherited Claims Re-grounding)** — when rewriting an existing beat that contains named-person or named-place claims, re-ground even if claim predates the edit; inherited claims ≠ auto-grounded; origin: Hijab Delta 26 Aisha bint Talha "granddaughter of Abu Bakr" → "niece of Aisha" caught at take, not at script.
- **+Instinct 5 scope extension** — ALL secondary sourcing strips from VO to overlay, not just historian citations — scholar names, manuscript titles, verse numbers, foreign-language transliterations, quote extensions; n=2+ Tripoli+Hijab; exception: ONE load-bearing term per section stays in VO.
- **+Mechanism Vocabulary Library** (new section, n=2) — library: trap, class line, registry administration, blurring, killed, complete mechanical failure, tactical engineers, mechanism of erasure, structural collision, retrofitting, manufactured, fabricated, engineered, projected backward.
- Origin: Hijab #52 rough cut 2026-05-18.

## v15.0 (2026-05-09 — Video #54 Inquisition rough-cut post-mortem)
- **+Rule 40 Baseline-Before-Exception** (Tier 1, universal) — every "but actually" / "loophole" / "exception" / "rule X applies" beat must establish the baseline being subverted BEFORE the beat lands, via Path A VO scaffold OR Path B [ON SCREEN] visual scaffold; sibling to Rule 3 myth-refutation but inverse direction; thesis-discipline link: if locked thesis contains "loophole/exception/but/however/actually" the antecedent of that pivot must appear before the pivot does.
- **+Rule 41 Lane Choreography** (Tier 1, universal) — every rule-asserting VO beat must commit to a visual lane; featured-exhibit-only [ON SCREEN] usage where central document is visualized but supporting rules aren't = FAIL; script's job is lane choreography not VO drafting.
- **+Rule 42 Citation Grounding** (Tier 1, universal) — port from article-writer Rule 5C; every blockquote round-trips through project NotebookLM notebook before script lock; ⏳ Confirm verbatim is not acceptable for film-ready scripts; cannot reach DRAFT-LOCKED with any ⏳ rows in fact-check verification.
- **+Rule 10 Format-Specific WPM Calibration** — Format C forensic close-read = ~150 WPM, word budget = runtime_seconds × 2.5; Standard Format A/B = ~200 WPM, runtime_seconds × 3.3; old 250 WPM × 1.20x assumption was wrong for document-heavy formats.
- Origin: Inquisition #54 rough cut ran 7:48 vs 5:00 target (+56% overshoot); script never set up "torture only once" baseline that §XV's loophole loopholes; user added scaffolding live during recording; same VO-mono failure recurred at §5 silence=innocence and §2 cold/hot blood frame; §6 Toledo "worse death/enemy" quote went to film with ⏳ deferred verification. Memory: feedback-baseline-before-exception.md.

## v14.9 (2026-05-08b — Video #54 user read-through pass)
- **+Rule 3 myth-refutation sub-rule** — refutation must explicitly negate THAT claim before producing evidence; evidence alone doesn't refute — applies to hooks, turns, counter-balance.
- **+Rule 7 decoder audit** — assess every primary-source quote for "does listener understand significance immediately?" — Kamen Jewish/Muslim quote needed unpacking even though not legalese.
- **+Rule 8 Content-vs-Genre** — when introducing a primary document, name CONTENT not just GENRE — "rules for how to investigate, interrogate, torture, sentence" not "a bureaucratic manual".
- **+Rule 8 Charge specification** — when a person is a CASE STUDY with multi-paragraph block / >30s investment, name the charge; procedural placeholders don't need it — scope by depth of treatment.
- **+Rule 17 Earn-the-title-card-beat** — standalone dramatic beats like "Paragraph fifteen." need a setup sentence in prior beat that promises what's coming; don't drop title-cards cold.
- **+Rule 27.B Section-opening connector** — section openings can't plant a new time/place anchor cold — need connector phrase tying back to prior section's last beat.
- **+NEW Rule 32K How-we-know attribution voice** — weave source into prose for dramatic/emotional/interpretive claims; leave to citation tags for uncontested procedure; don't over-attribute — citation parade kills momentum.
- Origin: user read-through after Sonnet+Opus polish — surfaced specificity, significance, sourcing, and decoding gaps that AI passes had missed.

## v14.8 (2026-05-08 — Video #54 Spanish Inquisition Sonnet+Opus polish pass)
- **+Rule 4 vague-antecedent sub-check** (spoken-delivery) — every demonstrative + ambiguous pronoun must have unambiguous referent in immediately prior sentence.
- **+Rule 7 "In other words"** added to decoder-phrase patterns (allowed when quote needs translation OR explication; filler-before-paraphrase still discouraged).
- **+Rule 23 CTA guardrail** — one sentence + this-video's-specific-value, not generic templates; ask user if unsure of distinct value.
- **+Rule 31D "Category-match"** — when bridging individual case → aggregate, categories must match — don't transition "torture case" → "executions count" without naming the shift.
- **+Rule 32H Pre-frame audit sub-bullet** — when quote has both pre-frame + post-quote decoder, audit if pre-frame is restating decoder; compress to question + quote + decoder if redundant; keep if priming for legalese, introducing source, or doing emotional setup.
- **+Rule 39 anaphora as 5th named rhythm** — full sentences with repeated stem ≠ staccato; cut pattern = anaphoric pile-up + Frequency cap meta-principle generalized (any device 3+ times = filler unless deliberate refrain).
- **+Tier 3 header note** — techniques are tools not defaults; overuse kills effect.
- Origin: Video #54 polish pass — user explicit principle "these are just methods, some work in some instances."

## v14.7 (2026-04-30)
- Cross-paper STRUCTURAL wave from 13-paper academic corpus — Rule 17b Concrete-Anchor 4-Beat, Rule 27.B handoff mechanisms, Rule 32G.3 Political-interest decode, Rule 39 4 named rhythms, FORMAT-TEMPLATES #9-10.

## v14.6 (2026-04-30 — STRONG signals)
- Rule 32.I + Rule 16 + Rule 37 + Rule 38.

## v14.5 (2026-04-29)
- Rule 36 references THESIS-DISCIPLINE.md.

## v14.4
- Rule 36 THESIS THROUGH-LINE + Rule 32F.2b visual Chekhov's gun.
