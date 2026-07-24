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
Three systematic lock-direction edits: (a) hook restructured claim-first (open on the claim being debunked, then the scene — → memory `feedback-script-structural-architecture` P1); (b) long archaic verbatims (Equiano, Gorrevod) paraphrased in his voice in VO with the verbatim held on screen; (c) abstract economics (Manning) leads with the concrete example (15-to-1 Dahomey price ratio) before the principle — → memory `feedback-script-structural-architecture` P4 concrete-first. *Source: READ-ALOUD-v6-2026-05-25.md header + body diff vs v5.* **Confidence ↑ (S3):** the paraphrase-in-VO/verbatim-on-card split in (b) is independently confirmed at the delivery layer in BOTH videos — even VO-scripted verbatims drifted or compressed to paraphrase on camera (56-28, 57-25, 57-26).

### 56-12 [V] Lock-version edits v7→v8: cut the aphoristic mirrored binary; cut date-math openers — VALIDATED
At final lock he removed "Read it. The denial contains the confession." (quotable but op-ed-register mirrored aphorism — the Fig Tree scan had flagged it MEDIUM; he kept it for 4 versions, cut it at lock) and removed the "Sixty-three years after Romanus Pontifex," date-math opener. Also: the streamer-position paraphrase was verified against actual transcripts before lock (never paraphrase an opponent unverified). *Source: READ-ALOUD-v8-2026-05-25.md header.*

### 56-13 [St] Method-declaration bridge beat — VALIDATED
v8 added a 15-second standalone beat between hook and concede: "What I want to do in this video is go through some primary sources to clear up this misconception. But before we do that, let me make something clear." → memory `feedback-script-structural-architecture` P6 (method declaration). *Source: READ-ALOUD-v8-2026-05-25.md METHOD BRIDGE.*

### 56-14 [Su] Closing must name only what was shown — VALIDATED
"the desperate letters of African kings" (plural) when only ONE king's letter was shown = factual error caught by the creator. Montage/recap language must match the evidence count exactly. *Source: REWRITE-PLAN-2026-05-25.md §C5, §D.9.*

### S2 additions — draft-vs-locked diff (02-SCRIPT-DRAFT-v1-locked.md → 02-SCRIPT-DRAFT.md v8 final), mined 2026-06-12

### 56-15 [St] GUIDE-bullets don't survive lock — everything becomes fully scripted prose with camera-state choreography — VALIDATED
v1-locked had whole sections as `[GUIDE]` bullet lists (concede beat, every post-quote interpretation block). The final has zero bullets: every beat is written-out spoken prose, interleaved with explicit camera state (`[OPEN ON TALKING HEAD]` / `[CUT TO:]` / `[BACK TO TALKING HEAD]` / `[POINTER — highlight …]`). The lock direction is full scripting plus shot blocking inside the script, not talking points left to delivery. *Source: diff 02-SCRIPT-DRAFT-v1-locked.md → 02-SCRIPT-DRAFT.md (v8).*

### 56-16 [V] Rhetorical-question transitions get compressed or cut at lock — VALIDATED
v1's stagey questions ("What happens when you ignore the modern culture war and just read the receipts…?", "So how did Europe respond when an African monarch begged them to stop?") were cut; the one question that survived was radically shortened ("…why is a reigning African monarch on the record demanding a cessation of the trade while it was happening?" → "why is the King of Kongo demanding it stop?"). Transitions became declarative callbacks ("To understand why, we have to go back to the chronicle we opened with"). *Source: diff v1-locked → v8.*

### 56-17 [Su] The steelman is an evidence beat — give it its own primary sources, not a name-check — VALIDATED
v1's concede beat was six bullets citing Thomas Sowell. The final replaced it with a full evidence section: Ahmed Baba verbatim on screen (religion-bound enslavement), Equiano on inter-polity limits, the 1,000-vs-80,000 comparison graphic, and Lovejoy's "mode of production" framing. Concede beats get the same document-on-screen treatment as attack beats. *Source: diff v1-locked → v8, CONCEED-BEAT section.*

### 56-18 [Su] Interpret every quote after it lands — close reading, not just confirmation-risk setup — VALIDATED
Generalizes 56-02: v1 frequently let quotes land with a one-line bullet; the final adds an explicit plain-language reading after each ("He's not saying 'no slaves are being taken.' He's saying Kongo is so large you wouldn't notice"; "De Marees is admitting two things…"). Setup before + interpretation after became the uniform quote frame at lock. *Source: diff v1-locked → v8, João III + de Marees beats.*

### 56-19 [V] Editorial labels out, close reading in — VALIDATED
v1's loaded labels ("The buyer literally gaslights the supplier", "an aggressive, diplomatic steamroller", "the smoking gun") were all removed. The final does the work by paraphrase-precision instead ("The denial isn't 'we're not doing this' — it's 'you won't miss them.' The Crown wasn't denying the trade. It was denying the scale."). The indictment comes from the document's own logic, never from a name the narrator sticks on it. *Source: diff v1-locked → v8.*

### 56-20 [P] Lock direction can be EXPANSION — +54% words when the draft under-evidences — VALIDATED
1,180 → ~1,820 spoken words from draft-lock to final. The growth was all evidence: Dum Diversas, the 1518 asiento (a whole new evidence section), the raid→system bridge beat, the upgraded steelman. Counter-instance to "editing = cutting": when a draft asserts more than it shows, the locked version is longer. Pairs with 58-06 (completeness → MORE). *Source: word counts + diff v1-locked → v8.*

### 56-21 [V] Numbers are written as they're spoken — VALIDATED
"80,000" → "eighty thousand"; "81,000" row read as "eighty-one thousand"; "338,000" → "three hundred thirty-eight thousand". Digits in the draft became spelled-out spoken forms at lock (teleprompter-ready, no on-the-fly conversion). *Source: diff v1-locked → v8.*

### 56-22 [Su] The closing verdict gets scoped down and earns an audience-honesty beat — VALIDATED
v1 closed on an absolutist aphorism ("Buyers didn't find the Atlantic slave system—they engineered it."). The final closes with an honesty move ("I'm not under any illusion this will convince people who use history as a weapon in the culture war") plus a scoped claim ("The talking point is too broad to show the full picture… what didn't exist was the scale, the legal authority, and the racial logic"). Verdicts shrink to exactly what the shown evidence supports. Sibling of 56-14. *Source: diff v1-locked → v8, CLOSING VERDICT.*

### S3 additions — SRT-vs-script ad-lib deltas (`finished cut.srt` vs locked 02-SCRIPT-DRAFT.md), mined 2026-06-12 — **ALL HYPOTHESIS** (per postmortem-methodology: the finished-cut SRT conflates on-camera ad-libs with edit-room cuts; nothing here is creator-confirmed as intentional)

### 56-23 [V] He performs the opponent's claim in its actual vernacular, not the script's neutral summary — HYPOTHESIS
Script: "Europeans never kidnapped anyone in Africa. They just bought slaves from a pre-existing African market." Delivered: the streamer's own wording, re-voiced — "didn't go over to Africa with a lasso and start wrangling up random black people. We didn't do that. We went over there and other black people sold them to us. They were already slaves to begin with." The claim-statement beat works as impersonation-of-the-claim, not summary — and it carries the video's title word ("lasso"). *Source: finished cut.srt 0:05–0:17 vs v8 HOOK.*

### 56-24 [V] Mid-sentence parentheticals and em-dash asides get dropped on camera — HYPOTHESIS
"He takes his royal fifth — 46 people for his personal estate —" gone; "from what is now southeastern Nigeria" → "from what is now Nigeria"; the Cape Verde clause and entrepôt sentence gone; "And the man who recorded that scene was Prince Henry's own court historian" gone. Same delta in #57 ("the one that answered every question people would spend the next five centuries asking" dropped from the death line). If a fact is load-bearing, don't park it in an aside — delivery sheds asides first. *Source: finished cut.srt vs v8, hook + asiento beats; #57 SRT closer.*

### 56-25 [St] Beat-boundary cliffhangers get merged into flowing continuation — HYPOTHESIS
Script ends Evidence 1 on the standalone hook "Then the Europeans stopped raiding." and opens the Bridge with "The raids didn't stop because Europeans had a change of heart." Delivered as one continuous sentence: "Then the Europeans stopped raiding, not because they had a change of heart, they stopped because African forces shut them down." He doesn't perform the dramatic pause; written cliffhanger-seams flatten into connective flow. *Source: finished cut.srt 4:55–5:03 vs v8 seam Evidence 1 → Bridge.*

### 56-26 [V] Foreign-language verbatims don't survive delivery — English only in VO — HYPOTHESIS
The scripted Latin read ("…illorumque personas in perpetuam servitutem redigendi…") plus the "On the left, the original Latin — on the right, the English" tour line were cut entirely on camera; the Romanus Pontifex beat went straight to the English operative verbs (and the Dum Diversas mention moved ahead of the quote, simplifying the sequence). Latin/foreign text belongs on the card; the voice reads English. *Source: finished cut.srt 8:43–9:11 vs v8 Evidence 3.*

### 56-27 [V] Live micro-smoothing: un-contraction for emphasis + added connectives — HYPOTHESIS
"That's true." delivered as "That is true." (deliberate stress un-contraction — the reverse of the global contraction rule); "Europe did organize slave raids" → "Europeans initially did organize slave raids"; "The lasso wasn't working." → "…wasn't working anymore"; "From now on — trade." → "From now on, just trade." His smoothing particles (initially/anymore/just) signal arc-position. *Source: finished cut.srt vs v8, multiple beats.*

### 56-28 [Su] Quote wording drifts when spoken — verbatim fidelity lives on the card, not in the voice — HYPOTHESIS
The de Marees quote was restructured aloud ("They do not have at their disposal a multitude of captives on the Gold Coast. They cannot be purchased in large numbers." vs the scripted "…multitude of Captives, and so on the Gold Coast they cannot be purchased in large numbers."). Even a scripted verbatim drifts in delivery; the on-screen card is the only reliable verbatim layer. Confirms the 56-11(b) paraphrase-in-VO/verbatim-on-card split as the safe default. *Source: finished cut.srt 7:07–7:24 vs v8 Evidence 2.*

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
Read-aloud catches: cold pronouns ("That's slow" — that's WHAT?), buried logic (1528 update never said WHY it mattered), undefined antecedents, recap-redundancy, vestigial references from prior structures. Earlier-approved phrasings may need cutting once their context changes — flag the override transparently. *Source: WRITER-LESSONS.md §1.5, §4.5.* **Confidence ↑ (S3):** recap-redundancy also dies at the DELIVERY layer — #56's delivered cut dropped the scripted Equiano recap ("His community had slavery. His own father owned slaves…") and the post-quote source-list enumeration recap in #57; recaps that survive the read-aloud still get shed on camera.

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
When he changes a scripted line live he makes it plainer, adds a concrete noun, or breaks it into an enumerated beat; he never adds YouTuber garnish. So "reads cringey" almost always = the WRITER added garnish. Tier note: SRT-derived (hypothesis per postmortem-methodology), but consistent with all later VALIDATED grill data. ⚠️ VOICE-PROFILE header explicitly supersedes SRT fingerprints where they conflict (the SRTs are heavily edited). *Source: VOICE-FINGERPRINT.md headline.* **Confidence ↑ (S3):** the full SRT-vs-script passes on #56 and #57 (56-23..28, 57-24..29) found the same direction in every systematic delta — plainer transitions, dropped apparatus, restored credentials, direct questions; zero garnish additions.

### 57-12 [V] The cringe inventory — 13 assistant-introduced phrasings, all stripped — VALIDATED
Concrete banlist of what the assistant inserted across v1-v4 and the creator cut: "Here's what almost no video will tell you," "signed by the man they call the mystery," "let's play their game," "the receipt," "hot take," "keep that test in your pocket," "mystery-sellers," "let's do what nobody does," "If there's anything you remember from this video…," vestigial references, label-without-substance ("That's a Rorschach test"), close-recaps. Largely absorbed into VOICE-PROFILE's cringe no-list — kept here as the historical instance record with per-line context. *Source: WRITER-LESSONS.md §5.2.*

### 57-13 [P] Two-stage gate: gut-pick first, tool/critic second — VALIDATED
Creator's gut pick first; scorer/critic only if unsure. Don't override a clearly on-brand gut pick with scorer points (he rejected scorer-pushed titles that read clickbait). *Source: WRITER-LESSONS.md §6.3.*

### 57-14 [V] Voice rules from #57 now canonical elsewhere — cross-refs only
The full DO/DON'T catalogue (enumeration cadence, "There's just one problem," plain-concrete verbs, credential+name+"put it," dry irony at the opponent's material, fan-directed concession, "let's" is his, "basically" OK, understated-honesty move, "so busy…they…" irony, counter the conspiracy STRUCTURE) → `VOICE-PROFILE.md` (canonical, supersedes) + `VOICE-FINGERPRINT.md` (instance record). Do not re-derive from here; the profile wins on conflict.

### S2 additions — version-chain diff (SCRIPT-v2.md → SCRIPT-v3.md → SCRIPT-v4.md → SCRIPT.md locked), mined 2026-06-12

### 57-15 [P] Structure-lock before prose passes — two full polish passes were sunk cost — VALIDATED
v2 (transition rewrite, 5,407 words) and v3 (competitor-cadence pass, 5,233 words) both polished prose on the wrong structure (Hancock-debunk under a "What the map actually says" title). The v4 refocus cut ~1,750 words (→3,488) by changing the spine, discarding most of both passes. Quantified version of 57-03: run the title-scope check and lock structure BEFORE any sentence-level pass; prose work on an unlocked structure has near-zero survival. *Source: word counts + diff SCRIPT-v2/v3 → SCRIPT-v4.*

### 57-16 [St] The filler-beat cut catalogue holds even for POLISHED beats — confidence upgrade for 57-06 — VALIDATED
The v3→v4 diff removed, wholesale: the moving-claim geographic-migration arc (~480 words, v2/v3's centerpiece "turn"), the real-vs-manufactured-mystery meta beat (~250 words, "keep that test in your pocket"), the origin-of-the-claim history (Mallery radio broadcast + USAF off-duty letters), and the glaciology corroboration stack (34M years / 740k-yr core / 3km). Every one was sourced, teased, and payoff-threaded — craft quality didn't save them. Beat TYPE predicts the cut, not execution. *Source: diff SCRIPT-v3 → SCRIPT-v4; confirms 57-06 (a)–(d).*

### 57-17 [Su] Debunk by positive identification, not refutation stack — VALIDATED
v2/v3's Antarctica beat refuted (letters debunk → inscription 10 "read that again" → California-island analogy → glaciology escalation). The lock replaces the stack with a positive ID: the southern coast IS Brazil (Cabo Frio / Rio / Cananéia toponyms in correct order) running into the terra australis every 1500s mapmaker drew, with inscription 10 doing only the ice-kill and McIntosh's cherry-picking point closing it. "Here's what it actually is" beat "here's why they're wrong" at lock. *Source: diff SCRIPT-v3 Beat 6 → SCRIPT.md Beat 4.*

### 57-18 [Su] Genealogy steelman — concede the kernel, isolate the leap — VALIDATED
v3 dismissed the Alexandria claim ("people heard Alexander, Ptolemy, Alexandria and built a library out of a coincidence"). The lock reconstructs how the proponent actually got there: "Hancock got the Library of Alexandria from Hapgood, in 1966. And Hapgood got it, in part, from the map itself — the source list really does say the oldest charts go back to the time of Alexander… But that last step is his, not Piri Reis's." Concede what's genuinely in the document, then isolate the single unsupported step. Strongest anti-strawman pattern in the chain. *Source: diff SCRIPT-v3 Beat 3 → SCRIPT.md Beat 2.*

### 57-19 [P] Imported-cadence and imported-format passes get reverted at the creator pass — VALIDATED
v3 imported competitor patterns wholesale: direct-address garnish ("let's play their game," "I told you… Here's the fingerprint," "Read that again," "Let's do what nobody does"), promissory teaser-threading (⟶TEASER/PAYOFF), and the two-sentence on-screen paradox card (the 5.3x niche outlier format). v4/lock stripped virtually all of it — the cold open went back to plain spoken escalation, the teaser apparatus vanished with the beats it pointed at. An entire pass modeled on competitor transcripts was net-negative. What DOES survive import: structural/visual patterns (split-screen build, document pointers). Pairs with 56-07 (NLM ports) — register imports fail, mechanics imports survive. *Source: diff SCRIPT-v3 → SCRIPT-v4/SCRIPT.md; v3 changelog vs lock.*

### 57-20 [St] CTA at ~70%, value-anchored with a forward tease; the closer ends on an image — VALIDATED
v2/v3 ended on a hard CTA ("…subscribe. That's the whole channel."). The lock moves the CTA to ~70% (end of Beat 3, after the strongest reveal), anchors it to the channel method ("That's what I try to do on this channel — go to the document and read it"), and teases forward ("There's still the bottom of the map"). The closer carries no second CTA and ends on the lingering Soucek image + bookend line. *Source: diff SCRIPT-v3 Beat 8 → SCRIPT.md Beats 3/6.*

### 57-21 [V] The disclaimer is addressed to the viewer's attachment, not the target's character — VALIDATED
v2: "this isn't about whether Graham Hancock is a good guy." v3 added "By all accounts, he is." The lock reframes entirely: "if you like Graham Hancock and the stories he tells, this isn't an attack on the stories. I'm just trying to explain why the scientific community doesn't agree with him." Speak to the parasocial viewer directly; don't adjudicate the opponent's character in either direction. *Source: diff cold opens v2 → v3 → SCRIPT.md.*

### 57-22 [P] The locked script doubles as an audit trail — SOURCE blocks carry adjudication, not just citations — VALIDATED
Lock-stage SOURCE blocks record scholarly splits and the editorial ruling ("McIntosh/Soucek read the eight as Ptolemaic… Pinto reads them as KMMS. We follow McIntosh/Soucek… The thesis holds under both"), scope rationales ("scoped to 'who can read the original' deliberately"), and flagged overclaim cuts ("⚠️ 'the one man who could read it' was an overclaim and is cut"). v2/v3 blocks were bare IDs. This is what made the post-film cağferiye attribution fix traceable. *Source: diff SOURCE blocks v2/v3 → SCRIPT.md.*

### 57-23 [Su] v4→lock diff = the attribution-audit fix — cross-ref only
The only substantive v4→SCRIPT.md change is the cağferiye reattribution (named-proponent claim → "appearance the next lines debunk," after the post-film audit found neither Hapgood nor Hancock builds on the word). → memory `feedback-attribution-audit` (canonical) + ATTRIBUTION-AUDIT.md / VO-PICKUP-cagferiye.md (instance record).

### S3 additions — SRT-vs-script ad-lib deltas (`finished cut.srt` vs locked SCRIPT.md), mined 2026-06-12 — **ALL HYPOTHESIS** (finished-cut SRT conflates ad-libs with edit-room cuts)

### 57-24 [Su] Missing credentials get restored by ad-lib — introduce-before-using is instinctive — HYPOTHESIS
The locked script's first McIntosh mention carries no credential (the v3 credential chain was lost in the v4 refocus). On camera he added one unprompted: "McIntosh, **who wrote the authoritative book on this map**, checked the map…" When the script omits a source's authority intro, he patches it live — so the writer should never leave it out. *Source: finished cut.srt 2:05–2:14 vs SCRIPT.md Beat 2.*

### 57-25 [V] Scripted verbatims compress to paraphrase in VO — the card carries the quote — HYPOTHESIS
McIntosh's "…he never makes such a statement in any of the map inscriptions" blockquote: only the script's paraphrase ("the claim simply isn't there") was spoken. Hancock's Bimini scuba-dive blockquote: not spoken at all; he goes straight from claim description to "Piri Reis labeled that coast himself." Pattern across both videos (see 56-28): blockquotes written for VO tend to be delivered as paraphrase or skipped, with the verbatim presumably on screen. Script-side implication: write the paraphrase line FOR the voice and mark the verbatim as card-only from the start. *Source: finished cut.srt 2:05–2:16, 4:05–4:23 vs SCRIPT.md Beats 2–3.*

### 57-26 [V] Archaic transliterations in quotes get normalized live to the terms already taught — HYPOTHESIS
Kahle's "Dja'fariye is a mistake… for dja'grafiye, geography" was spoken as "Cağferiye is a mistake for jughrafiya — geography," matching the spellings the video had already established. He won't switch transliteration systems mid-video even inside a quote; scripts quoting period/scholarly orthography should pre-normalize the spoken version (verbatim stays on the card). *Source: finished cut.srt 3:56–4:00 vs SCRIPT.md Beat 2 Kahle quote.*

### 57-27 [St] The flashback closer was flattened to chronology in the delivered cut — HYPOTHESIS
Script order: 400-years-ignored → Porte → 1929 rediscovery → Kahle decode → [Beat 6] execution → "mutilated remains" → bookend. Delivered order: ignored → Porte → "rolled up and shelved" → **execution and death** → "mutilated remains" → "and there it stayed… until 1929" → Kahle decode → bookend. The man dies before the map is found — a strict timeline, stronger dramatic irony ("He died never knowing…"). Whether ad-lib or edit-room, the delivered structure beat the scripted flashback; candidate rule: closers run chronological. *Source: finished cut.srt 8:29–10:27 vs SCRIPT.md Beats 5–6.*

### 57-28 [V] Embedded colon-clauses become direct spoken questions — HYPOTHESIS
"There's one small mystery here: how an Ottoman admiral ended up with a map by Columbus." delivered as "There is one small mystery here. How does an Ottoman admiral end up with a map by Columbus?" He converts written subordination into a real question-and-answer rhythm. Distinct from staged rhetorical questions (which get cut — 56-16): this is a genuine setup question he then immediately answers. *Source: finished cut.srt 4:59–5:05 vs SCRIPT.md Beat 3.*

### 57-29 [Su] Delivery degrades precision: attribution anchors shed, similar entities swapped, lists truncated — HYPOTHESIS
Three precision losses on camera: (a) "Ptolemy's geography said one had to exist" → "One had to exist to balance the globe" (expository attribution dropped — the exact drift class feedback-attribution-audit polices at script stage); (b) "the one **Hancock** points to most often" delivered as "**Hapgood**" (similar-name entity swap, said once, corrected implicitly later); (c) the three scripted toponyms (Cabo Frio, Rio de Janeiro, Cananéia) delivered as two. Script-side mitigation: put load-bearing attributions in non-droppable positions, build disambiguation handles for confusable name-pairs (→ structural-architecture P8), and treat 3-item proof-lists as 2-survivable. *Source: finished cut.srt 4:05, 6:52–6:55, 7:16 vs SCRIPT.md Beats 3–4.*

### 57-30 [St] The parasocial disclaimer and two honesty beats did not survive to the finished cut — HYPOTHESIS + ⚠️ S8 CONTRADICTION FLAG
Cut between lock and publish: (a) the entire viewer-directed disclaimer ("if you like Graham Hancock and the stories he tells, this isn't an attack on the stories…") plus the Hancock/Lex intro line — compressed to "This video is about one document and what it says when you actually read it"; (b) "Kahle could read the original Ottoman. Hapgood couldn't — and he wrote his book thirty years later anyway" (the authority contrast the v4 reframe built); (c) "Kahle got plenty wrong, too — and McIntosh and others corrected him, point by point" (the accumulated-corrections honesty beat). All three were deliberate v4/lock investments (57-21, v4 reframe notes) that the delivered video dropped. Contradicts 57-21's VALIDATED status at the delivery layer — queue for S8/S9: does he actually want these beats, or do they die every time? *Source: finished cut.srt 0:26–0:48, 3:49–4:01, 9:41–10:11 vs SCRIPT.md Beats 1/2/5.*

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

## #59 — Israel/Palestine: The Partition Offer (Res 181) — script locked 2026-06-24

Source artifacts: `video-projects/_IN_PRODUCTION/59-israel-palestine-partition-offer-2026/` — `_research/READ-ALOUD-LESSONS-2026-06-23.md` (deltas 1–51), `SCRIPT.md` (locked lean cut), `01-VERIFIED-RESEARCH.md` (C16/C18 provenance notes). All entries VALIDATED (creator line-edits + live picks in an extended collaborative read-aloud, 2026-06-23→24). ⚠️ Per the creator's explicit instruction this session, the live read-aloud signal is ground truth for THIS script; VOICE-PROFILE.md is the cross-video default, not the per-video authority (see 59-20).

### 59-01 [St] Referee fork — consensus-first, attribute each camp by name, never resolve — VALIDATED
The Act 6 "decision on trial" (Morris blunder ⇄ Khalidi principled): state what both camps agree on, lay out the disputed part attributing each view + its reasoning, end on "they disagree about one thing only." Intro each pole by its READ ("Morris reads it as a blunder" / "Khalidi sees the opposite"), not "the biggest proponent is X." *Source: lessons §I delta 41 + Act 6 lock.*

### 59-02 [V] Frame the fork on CONCRETE STAKES, not moral labels — VALIDATED
He rejected "principled vs intransigent" (moral) for "was the 'no' a blunder, or was saying yes never an option" (the cost of each choice). Live words: "blunder" (threads to Morris), "reasonable"; "stand" reads weird in the close. *Source: lessons delta 41.*

### 59-03 [St] End on cross-camp CONSENSUS, not a rhetorical flourish — VALIDATED
He cut the planted "ghost map / only ever existed on paper" payoff as "bullshit"; the climax he wants is "the different claims and the historical consensus with the sources." Ending = what every historian across the divide agrees happened (gave legitimacy not a border; the war drew the 55→78% line; the Arab state never came into being), stated flat in VO with the cross-camp agreement (Shlaim 79 ⇄ Khalidi 78) carried ON SCREEN, not recited. ⚠️ Tension with VOICE-PROFILE's thread-word/callback-device rule (the "on paper" plant→payoff) → INTERVIEW-AGENDA A-59a. *Source: session Q1 + ending lock.*

### 59-04 [St] Fold the verdict-recap; don't re-state what the trials already earned — VALIDATED
Act 7 first re-stated the fair/imposed verdicts Acts 2–5 had proved; he flagged "we already kind of did this." Verdict act keeps only the NEW material (the precision + the consensus) and opens straight on it. *Source: session Q3.*

### 59-05 [St] Every beat must name what it PROVES to the thesis — VALIDATED
He killed a vote-night beat with "why is it here?? what does it prove???" — it was doing two muddy jobs (a legality echo that restated Trial 2 + a federal-offer aside). Fix: cut the redundant half, state the surviving point in-line ("the 'no' was a no to THIS plan, not to any deal"). *Source: lessons delta 45.*

### 59-06 [Su] Pushback rides the DOCUMENT, not "historian X says" — even inside a fork — VALIDATED
The anti-Khalidi rebuttal grounds in Res 181's own text (it created an Arab state + required equal minority rights); the pro-Israel scholars (Karsh/Shapira) drop to silent on-screen corroboration. The auditor's edge applies to the rebuttal too. *Source: lessons delta 44.*

### 59-07 [V] Let the document rebut the partisan — don't label the person — VALIDATED (intra-session reversal)
He first asked to flag Khalidi's partisanship ("he's very partisan"), then CUT "open advocate" → "That is Khalidi's interpretation" + the document ("let the sources speak… otherwise very accusatory"). ⚠️ reversal within one session → INTERVIEW-AGENDA A-59b. *Source: session.*

### 59-08 [Su] A steelman must not inflate its own facts — VALIDATED
"The Arabs were offered a state on most of the land" was FALSE (they got ~45%; the Jewish state got the 55% "most") and contradicted Act 2; he caught it instantly. The blunder case is "offered a state," full stop — the land fraction undercuts the steelman. Verify every number inside a steelman against the already-established facts. *Source: lessons delta 42.*

### 59-09 [Su] "Plucked defeat from the jaws of victory" = 1939 White Paper, NOT 1947 partition — VALIDATED (provenance)
Grounded check (Morris `234bb4fe`): the phrase is anchored to the 1939 White Paper rejection (al-Husseini), tagged "as was the Palestinians' wont" (general pattern) but belonging to 1939. ⛔ not usable as a 1947-partition quote (Rule 4B drift) — correctly omitted from the lock. *Source: 01-VERIFIED-RESEARCH C16 provenance note.*

### 59-10 [Su] Ladder the pressure beat to the primary the scholar cites — VALIDATED
Cohen is SECONDARY; the US vote-pressure examples ladder to FRUS/NARA/PRO (Liberia → NA minute, 9 Dec 1947, Liberia's own "high pressure electioneering" complaint; Philippines → Ayers diary + FO 371/61889). On-screen = primary provenance or Cohen-as-conduit, never "primary-in-hand." Laddering surfaced the primary "high pressure electioneering" verbatim, which went into the VO. *Source: session ladder query + 01-VERIFIED-RESEARCH C18.*

### 59-11 [Su] Restore the contested-label on a contested move — VALIDATED
Cutting the Bedouin nomad-vs-resident caveat presented the Arab-majority recount as settled fact — the exact crop the video accuses both sides of. Restored one clause ("the UN treated them as nomads, not residents; the Arabs said that was backwards"). The honesty caveat is non-optional even when trimming for length. *Source: session QC + Act 2.*

### 59-12 [St] Cutting a setup line can break a downstream quote's referent — VALIDATED
He cut the customs-union setup in Act 3; Reedman's "not viable WITHOUT a customs union" then referenced a customs union never introduced. Before deleting a setup clause, scan forward for a quote/claim that depends on it. Sibling of the protect-callback-referent-when-cutting rule (58, → VOICE-PROFILE). *Source: session final QC.*

### 59-13 [St] Flow-out of an OPEN fork into a verdict act needs a bridge — VALIDATED
Act 6 ends unresolved; the ending resolves a different thing (the consensus). Hand off explicitly: "that may never get a settled answer; what the resolution actually did isn't really in dispute." Delta-6 flow applied at the ACT seam, not just the beat seam. *Source: lessons delta 46.*

### 59-14 [St] Thesis-forward seam between the two trials — VALIDATED
The Trial-1→Trial-2 hand-off was a flat list-pivot ("that's the first claim… the second…"); sharpened to pose-the-next-question-and-answer-it ("if it was forced on anyone, someone had to do the forcing… 181 was none of those"). *Source: structure-notebook check + Act 4.*

### 59-15 [V] Cut a list to the one load-bearing item — VALIDATED
The minority triad (no say over governance / children's schooling / immigration) → just immigration ("the thing the whole fight was really about"). Keep the item that carries the point; drop the enumeration. *Source: lessons + Act 6.*

### 59-16 [V] Neutrality by hedging contested ownership — VALIDATED
"their country" → "a country they thought of as theirs"; "imposed" → "imposed from the outside"; cut "on their own land" wherever it recurred. The script won't assert whose land it was as fact — only that they believed it. *Source: lessons §A + creator edits.*

### 59-17 [P] ⭐ NotebookLM is a RETRIEVAL tool, not a prose editor — VALIDATED
"Quote X on Y" grounds (`sources_used` populated). "Rewrite my paragraph/act for clarity" returns empty `sources_used` = pure generation = it invents quotes ("death warrant"), re-adds tags you cut, re-spends reserved payoffs ("ended up with nothing" = a held Act-7 line). `nlm login --force` fixes empty-grounding on a RETRIEVAL query; it will NOT fix a generation query (nothing to retrieve). Use NLM to GET scholar framing, then do voice/structure Claude-side. *Source: lessons §J delta 43.*

### 59-18 [P] The NLM self-review CONFABULATES — treat its flags as hypotheses — VALIDATED
Self-review = upload the assembled VO as a source, query three notebooks: the project research notebook (accuracy/inconsistency — most valuable), The Debunking Handbook (effectiveness), Competitor Script Structure (retention patterns); delete the uploaded copy after. But the accuracy audit "flagged" a line that wasn't in the script (bled from an earlier query) and re-made an attribution error already fixed (Kelsen vs UN Secretariat). Trust the grounded confirmations; re-check every criticism against the actual script. *Source: lessons delta 48.*

### 59-19 [P] Two review corpora can disagree — the disagreement is the signal — VALIDATED
Debunking Handbook = lead with the FACT (myth-first risks familiarity/worldview backfire); competitor-retention corpus = lead with the believed STORY (curiosity gap). Different objectives — belief-change vs watch-time. For a retention-bottlenecked YouTube channel, weight the retention corpus (channel data: myth-first retains better). Tier AI structural advice against LOCKED voice/strategy: reject off-voice (e.g. "professional vulnerability," sensory payoff), flag locked-decision conflicts as A/B (myth-first hook vs the SEO-anchored open), apply only the on-voice non-conflicting wins. *Source: lessons deltas 49–50.*

### 59-20 [P] ⭐ For a SPECIFIC video, the live read-aloud signal supersedes the canonical VOICE-PROFILE — VALIDATED
His explicit instruction: don't audit a script against `VOICE-PROFILE.md` (older, drifted) — audit against THIS video's edits + read-aloud lessons + feedback. The canonical profile is the cross-video default; the live read is the per-script authority. (Mirrors the corpus header tier rule — VALIDATED creator picks outrank inherited canon.) *Source: session voice-check instruction.*

### 59-21 [P] Draft whole beats, not snippets — VALIDATED
Token economy: once the axis/structure is locked, deliver the full beat in one block with minimal surrounding commentary; he still reads line-by-line and reacts, but the unit of delivery is the beat, not the sentence. *Source: lessons delta 40.*

### 59-22 [V] #59 voice rules reinforcing VOICE-PROFILE — cross-refs only
Reconfirmed live this video (do not duplicate as new rules): kill self-narration/signpost openers ("before we test anything," "let's start with fair," "that wording was deliberate"); no staccato fragment triplets; plain numbers, no forced comparison; label things directly ("Here is the Israeli side"); push the verdict onto the document; neutrality disarmer is a hard constraint on this charged topic; first-person research act fits because the premise IS an investigation ("So I read the documents"). → VOICE-PROFILE (canonical).

> **S14 second mining pass — on-screen-card verbatim cleanup (post-lock, 2026-06-24).** The 59-01..22 set mined the read-aloud/script deltas at lock. 59-23..27 below mine the SEPARATE post-lock card-verification pass (every displayed verbatim → char-exact text + page-verified citation). Axis = mostly [P]/[Su] sourcing discipline; no new voice/structure deltas (the VO was unchanged).

### 59-23 [P] ⭐ NLM CLI page numbers are unreliable — page-verify every on-screen verbatim against the actual source PDF — VALIDATED
NLM's CLI returns page numbers that are frequently wrong (gave Khalidi pp.161/73/24 from an ungrounded query — real pages 120/60/27; even grounded queries can mis-page). For every on-screen verbatim card: open the source PDF (library / Downloads / in-project scan), locate the quote with PyMuPDF, and read the **folio = the first standalone page-number line** — IGNORING libgen printer-signature ruler lines ("1 2 3 … 40 41" repeated on every page; these are NOT page numbers — Karsh's Negev line is printed **p.103**, not the "40/41" ruler that fooled the first read). Empty `sources_used` = ungrounded = don't use the quote OR the page; confirm char-exact wording via `nlm source content <id>` (raw text, definitive on wording). Extends 59-17/18. → memory `primary-source-ladder`. *Source: this session's ON-SCREEN-CARDS cleanup.*

### 59-24 [Su] ⭐ Statistical/census figures ladder to the ORIGINATING survey, not the committee/scholar that re-tallied — VALIDATED (creator catch)
The Beersheba "1,020 Jews / 103,820 Arabs" figure was being carded to the Sub-Cttee 2 report / Kattan; the creator flagged the data ORIGIN is **A Survey of Palestine (1946)**. Resolution: the on-screen verbatim sentence is the UN Sub-Cttee 2 report's (A/AC.14/32, its own p.41 — a primary UN doc, computing the proposed-Jewish-State *southern section* incl. the Bedouin estimate); the underlying census is the British Survey (Table 7b: Beersheba sub-district = 5,360 Moslems / 150 Jews *settled*, excl. nomads). For ANY statistic, ask "which document first MEASURED this?" and name that as the origin even if the card shows the intermediate's sentence. This is the channel's whole purpose — go to the document that *made* the number. → memory `primary-source-ladder`. *Source: creator correction, this session.*

### 59-25 [P] On-screen card cleanup is a distinct post-lock pre-film gate — VALIDATED
Locked VO ≠ locked cards. After lock, every displayed verbatim/chyron needs char-exact text + a page-verified citation BEFORE film, captured in a per-video `ON-SCREEN-CARDS.md` manifest (card → verbatim → source → page → status; verify only what the VO actually puts on screen). This pass cleared 11 ⚠️ cards against the real PDFs. *Source: this session.*

### 59-26 [Su] Verify proper-noun attributions on cards even when non-load-bearing — VALIDATED
The Reedman card read "P.C. Reedman"; the actual source (Ben-Dror) names him **"John Reedman."** A name on a card is an attribution claim — check it against the source, not memory/prior drafts. Extends the attribution-audit predicate-drift rule to proper nouns. → memory `attribution-audit`. *Source: this session card pass + Gemini name-hunt corroboration.*

### 59-27 [Su] When the primary is archival-only, the scholar conduit IS the honest terminal — VALIDATED (refines 59-10)
Laddering to the primary stops at "as gettable as it gets." A Gemini web-hunt confirmed the four S→P card originals (Liberia NARA minute 501.BB Pal/12-947; Philippines Murphy/Frankfurter telegram → Murphy Papers, Michigan; Reedman's UNSCOP economic assessment; Cunningham's diary → St Antony's) are archival-only and not freely published — so **Cohen p.297 / Ben-Dror p.176 / Louis p.530 are the correct terminal conduits**, provided each reproduces the verbatim and ideally cites the archival primary in its footnote (Cohen's fn 100 = the NARA minute). ⚠️ Gemini web answers = LEADS, not verification (confabulates URLs/catalog numbers) — one real lead surfaced: the Philippines cable may be reproduced in Radosh & Radosh, *A Safe Haven* ch.7 (verify before use). *Source: this session primary-source hunt (`_research/GEMINI-primary-source-hunt-2026-06-24.md`).*

---

## #62 — Volhynia/OUN-UPA (Untranslated Evidence) — script in progress, T1–T5 full cold-reads 2026-07-16/17

Source artifacts: `video-projects/_IN_PRODUCTION/62-volhynia-massacre-untranslated-2026/_adlib/` — `t1-readthrough-2026-07-16.md` through `t5-readthrough-2026-07-17.md`, `followups-raw.md`. Unlike prior corpora entries (built from line-level read-aloud diffs on a near-final draft), these are FIVE consecutive full cold-reads on a script under active structural rebuild (v3→v5.4) — the density of root-cause, cross-beat findings is unusually high because the same failure classes recur and get progressively diagnosed. Mined 2026-07-20 (`/voice grill`, prompted by the creator flagging these reads as his clearest voice examples). Not yet script-locked — full KPI/EVAL-BASELINE mine still fires again at lock.

### 62-01 [St] ⭐⭐ The open-question ledger — a paragraph is legal only if it answers the viewer's currently-open question and raises the next — VALIDATED
Derived from T1+T2 (~40 complaints resolve to five violations of one principle): **V1** new term/claim used before it's introduced ("who the fuck is the UPA") · **V2** answering a question the viewer never asked ("nobody gives a fuck if it's legal") · **V3** raising a question and not answering it ("why is Lebed not enough? if I don't understand, viewers won't") · **V4** re-answering an already-closed question (repetition) · **V5** breaking a promise the script itself made (promised primary documents, delivered a scholar quote). His own diagnosis: "we can condense a lot just by adding some logic back into the script" — closed questions can't be legally re-answered, so enforcing the ledger kills repetition as a side effect, not a separate fix. **Compose method (his/Minto-pyramid shape, not just an audit checklist):** before prose, write the video as a numbered Q→A chain, every joint explicitly BUT or THEREFORE, never "and then"; any beat that can't name which open question it answers gets moved or cut. Extends the existing continuity-of-reference rule (VOICE-PROFILE §Transitions, "again/this time" needs a depicted antecedent) from back-pointers specifically to the full claim/promise/question state of the video. **PROMOTE:** written into `VOICE-PROFILE.md` §Transitions and `WRITING-VOICE-AND-STYLE-P4-DEBUNKING.md` 2026-07-20 (this session); flagged as a candidate extension for the `told_so_far.py` checker (Phase D2), which currently only covers the V1/rebuttal-antecedent case — V2–V5 are unimplemented. *Source: T1 HEADLINE DIAGNOSIS + T2 ⭐⭐ ROOT DIAGNOSIS.*

### 62-02 [St] Argumentative story order beats chronological narration on a multi-camp topic — VALIDATED
v4 fix: reordered from a chronological/thematic story stack to accusation-first (Poland's claim) → defense (Ukraine's story, now reacting to a STATED accusation rather than floating) → exploitation (Russia). Fixes both "a tragedy, not a policy — what policy?" (the defense needs something concrete to react to) and the cold-open handoff (which ends on the accusation). Generalizes: when a topic has competing camps, sequence them so each later camp's material answers a question the prior camp's beat just raised — not by neutral chronology. *Source: T2 v4 fix #1.*

### 62-03 [Su] ⭐⭐ Don't narrate as settled fact what a later beat itself calls unprovable — VALIDATED
CH4 asserted "the leadership decided to change the facts on the ground" as narrated fact; CH6 then argues the top-order attribution is genuinely disputed (McBride runs two live theses: central Lebed order vs. regional Klyachkivsky/Shukhevych initiative). His catch: "we are insinuating the call came from the leadership... unless we have proof, we should say how we know this." Fix shape: state the POLICY'S existence as fact (not disputed), scaffold the WHO-ORDERED-IT question explicitly as open ("it sounds an awful lot like... but is there any hard evidence — any proof beyond oral testimony?"), and resolve it later at the crux beat, not before. Same failure class as an unattributed steelman claim, but for the narrator's OWN causal assertions — auditor's-edge discipline applies to the referee's voice, not just to quoted sources. *Source: T5 ⭐⭐ ROOT CAUSE 1 (~4 minutes of commentary, his deepest note of the whole read-aloud series).*

### 62-04 [V] Show, don't announce the act of displaying a document — VALIDATED (narrows the existing "on your screen" scene-pointing rule)
Every instance of narrating that a document is being shown got cut on the ear: "It survives — this is it, on your screen" → "It survives. It reads:" ("we will just show it on the screen instead of saying that we are showing it"); "this is it, on your screen" → "the text of this proclamation survives"; "— put the original and the reprint side by side, you can see it yourself —" → cut entirely. Reconciles with the T3 finding below (62-05): weigh the source's *nature and evidentiary class* in voice, but don't narrate the *mechanical act* of putting it on screen — the screen does that work by existing. *Source: T4 ⭐⭐ ROOT CAUSE 1.*

### 62-05 [Su]/[V] Primary sources must be SPOKEN, not just carded — reverses an over-correction toward invisible sourcing — VALIDATED
"Our whole shtick is that we talk about primary sources, and we have never, up till now, talked about primary sources... I want this to be the differentiating factor: here are the sources people talk about, and this is how you can look at them or interpret them. We are not doing this. Which is stupid." A prior draft (v5) had over-corrected toward card-only sourcing (Kraut-style invisible documentation) after 62-04's display-narration cut; his correction: keep the display narration cut, but each source still needs its class-of-evidence and how-to-weigh-it walked in VO (the Klymchak chain-of-command walk, the confession-under-duress walk), not just shown. *Source: T3 ⭐⭐ DIRECTIVE 1.*

### 62-06 [St] Say-it-once at whole-video scale, not just within a beat — VALIDATED
Three T5 hits of the same argument landing twice across DIFFERENT acts (not adjacent paragraphs): the Russia-never-produced-the-document argument in both CH6 and CH8 ("we are repeating ourselves... we could move the beat to CH8, that would make sense" — collapsed to one, later location); "so that's the clash" vs. "every nation builds its heroes" paragraphs restating the same point; a negation-pair ("they were not misremembering, they were purposefully editing") simplified to a flat positive ("they erased it"). Generalizes 56-05's within-beat register whack-a-mole to full-script scale: an argument used to close a question can't be redeployed later to close it again — if it needs restating, move it, don't duplicate it. *Source: T5 ⭐⭐ ROOT CAUSE 2.*

### 62-07 [V] "Not necessarily" as the recurring absolutes-softener on a causal claim that's plausible but unproven — VALIDATED
Recurring self-correction across multiple reads: "Not because they **necessarily** loved the Nazis" (alliance-motive line), "It wasn't NECESSARILY loyalty to Hitler" (police-motive line). When a motive/causal claim is plausible and evidence-consistent but not directly sourced, the qualifier goes on the strong verb ("necessarily loved/necessarily loyal"), not a hedge clause bolted onto the sentence — keeps the claim confident while marking exactly what isn't proven. *Source: T5 verbatim harvest, T1 police-beat motive-cut.*

### 62-08 [Su] A symmetrizing rhetorical device must not erase the actual asymmetry — VALIDATED (guard, not yet re-tested live)
The graves-flip beat ("both peoples decided to cleanse or safeguard their land") landed as a device but oversells parity: one side (UPA, organized) started the killing and did most of it; the other side's response (Vistula) was a government deportation, not a matching massacre. Guard applied: keep the flip's structure (mirrored geography — Volhynia is now Ukraine, the reprisal lands are now Poland) but weld it to the existing scale/who-started-it concession so the device doesn't overcorrect into false symmetry. Same family as the auditor's-edge "concede what's real, don't inflate the other side to match." *Source: F1 follow-up ad-lib + rebuild guard.*

### 62-09 [P] Full cold-reads surface structure bugs that line-level polish passes can't — VALIDATED
Five consecutive full-script cold reads (T1–T5, 2026-07-16/17) on the SAME underlying draft found progressively deeper issues each pass — T1/T2 caught the open-question-ledger violations (structural), T3 caught an inversion in the sourcing directive, T4 caught display-narration tics + ~6 remaining structural spots, T5 caught one deep objectivity issue plus whole-video-scale repetition. None of these were catchable by a single read or by the mechanical checkers alone (voice_lint, told_so_far) — they require holding the ENTIRE argument state across ~13 minutes at once. Supports the plan's E-phase premise (a standing eval harness matters) but also argues the harness's deterministic layer has a real ceiling: this class of finding needs either a full LLM-judge pass against the whole script or an actual human read-aloud, not per-beat checkers. *Source: T1–T5 aggregate pattern.*

### 62-10 [St] A beat that answers no CURRENTLY open question gets moved to where one exists, not cut by default — VALIDATED
The Gaj/Werba testimony beat drew no complaint on content across four reads, but its placement kept getting flagged ("not sure if this is the right place... doesn't feel like it fits in this spot"). Diagnosis (T2, applying 62-01): the beat answered no open question in late Act 4; moved to the Act 5 "were both peoples monsters?" beat, where it directly answers the question just raised. A recurring placement complaint on content he otherwise likes is a ledger-fit problem, not a quality problem — relocate before cutting. *Source: T2 v4 audit item 2; T4 "not sure if this is the right place" (open, resolved by the T2 move).*

### 62-11 [V] ⭐⭐ The balanced antithesis is THE garnish tell — not "colourful language" in general — VALIDATED (2 live picks)
2026-07-21, v7.0 restructure. He flagged the script as having "too much colourful extra language that I don't think is necessary" but could not localise it. A six-channel lane study (`_research/REFERENCE-LANE-FIGURATION-2026-07-21.md`; fig tree · Historia Civilis · Premodernist · Atun-Shei · ReligionForBreakfast · Stefan Milo; 12 transcripts, 30,810 words) localised it to ONE figure family: **balanced/antithetical epigram**, lane mean **0.24/1k words ≈ one per video**, and **zero in 10,757 words** across the two closest register matches (RFB, Milo) — against **~2.1/1k** in the draft, i.e. ~9× lane mean. Everything else he suspected was in range: his dead-metaphor rate (4.3/1k) is lane-normal (3.8), and live metaphors *of the evidence itself* ("at a certain point the paper stops") are the single best-supported figure class in the lane. **The diagnosis that matched his felt sense: 6 of 16 suspect lines came from the ~240 words of NEW connective prose written that day (8.5% of the script producing 37% of the colour) — writing joints between relocated beats pulls the writer toward antithesis to make seams feel intentional.** Practical rule: when restructuring, audit the new mortar for mirrored clauses, not the whole script. *Source: creator flag + lane study + 2 live picks below.*

### 62-12 [V] ⭐⭐ A lane-wide ABSENCE outranks his own earlier harvested line — reverses T-read primacy in one specific case — VALIDATED
Both 2026-07-21 picks went AGAINST his own prior read-aloud harvests and WITH the lane evidence, against my recommendation on both. (a) **"The enemy of their enemy would be their friend"** — a T4 verbatim harvest he wavered on and settled — CUT, on the finding that the lane uses unflagged proverbs only in a *source's* mouth, never the narrator's. (b) **"That is not a mob of angry people. That is an officer, reporting up a chain of command"** — two spliced harvests (T3 + T4), read clean 3×  — FLOWED into one em-dash sentence. **The discriminator:** T-read primacy (`01-VERIFIED-RESEARCH` condensation item 9 — "the one he read clean twice overrides a word-count win") holds against *word-count* and *style-preference* arguments, but NOT against evidence that a construction is absent from the register he's aiming at. A line surviving his read means his ear didn't catch it, which is weaker than it looks — the drift audit's whole premise is that *rate* tells are invisible at line level (`VOICE-PROFILE.md` §Adversarial drift audit, "each instance reads fine; the frequency is the residual AI accent"). So: his read is ground truth on whether a line is SAYABLE; it is not ground truth on whether the line's FAMILY is his. *Source: 2 live picks, 2026-07-21.*

### 62-17 [P] ⭐⭐ A reworded line is a RULE, not a swap — derive the principle, then hunt it where he didn't flag — VALIDATED (his correction, twice, forcefully)
2026-07-21 T6. After harvesting ~41 of his rewordings as literal substitutions, he pushed back hard: *"I DON'T THINK YOU LISTENED TO MY READTHROUGH WELL OR YOU DIDN'T UNDERSTAND THE COMMENTS I MADE"* and then *"YOU NEED TO UNDERSTAND MY COMMENTS AND WHY I SAID THEM OR WHY I SAID THINGS DIFFERENTLY."* **The failure mode is mechanical substitution: he says X, the page becomes X, and the fault he was correcting survives untouched everywhere else in the script.** Working the principles instead (see `VOICE-PROFILE.md` §"Who is allowed to rule") turned three of his line-changes into three rules, and the rules then caught **four further violations he had not flagged — three of them in prose written that same day, after he had already corrected the identical fault elsewhere in the same read.** Operational: for every read-aloud delta, write the WHY next to the WHAT, then grep the whole script for the why. The delta is a sample; the rule is the finding. *Source: T6 + his two pushbacks.*

### 62-18 [P] ⚠ A catalogue is a to-do list, not a receipt — writing his notes down is not doing them
Same session, the failure that triggered 62-17. His T6 notes were written into `_adlib/t6-readthrough-2026-07-21.md` in full and correctly — including four items filed under headings labelled "⭐⭐ ROOT ASK," i.e. correctly identified as the most important in the read — **and then none of those four were acted on**, because cataloguing them felt like completing them. Separately, a message announced "four things I held back" and then asked about two; the remaining two sat unresolved through three subsequent edit rounds. **Guard: after writing a read-aloud catalogue, immediately produce a separate APPLIED/NOT-APPLIED checklist against it, and treat any un-actioned ROOT-level item as blocking. Never let the catalogue file be the only record of what still needs doing.** *Source: seven un-actioned T6 notes, surfaced only because he re-read the script and pushed back.*

### 62-21 [P] ⚠⚠ CORRECTION TO 62-14b AND 62-16 — the `so`/`but`/`very` "gap" was measured against the wrong register, and the 21.0 target is a 741-word artifact — MEASURED
2026-07-22, raised by the creator unprompted: *"we could clean up our so and but and very because that's how I talk improvising, but maybe that's not the best for an explaining YouTube video."* **He is right, and the instrument was wrong.** Four passes (v7.0, v7.2, T7, Round 2) chased a target of **21.0/1k** `so`+`but`. That number comes from `FINGERPRINT-UNSCRIPTED.md` = **741 words, 39 sentences, ONE video** — `yt:yMAWJcjo_ug`, his *nervous first channel-intro recording* — and **that file's own header warns against exactly this use**: *"a single-sample point estimate, not a stable rate… never hard gates… this is his nervous first recording in pure conversational register — scripted-delivery comparisons must go through VOICE-PROFILE."* It was promoted to a binding pre-lock threshold anyway.
**Re-measured 2026-07-22 across three registers of the same speaker:**

| register | sample | `so` | `but` | ratio | `so`+`but` | `very` |
|---|---|---|---|---|---|---|
| improvised (#62 ad-lib dictations) | **4,992 w** | 6.0 | 4.4 | 1.36 | **10.4** | 4.6 |
| read-aloud approved (corpus §1 locked lines) | 1,069 w | 3.7 | 3.7 | **1.00** | **≥7.5** | 0.9 |
| #62 script as locked | 2,757 w | 4.7 | 4.7 | 1.00 | **9.4** | 0.4 |
| the old "gold" target | *741 w* | 11.8 | 9.2 | 1.29 | *21.0* | *11.8* |

**Three findings.** ① The 21.0 does not replicate: a 6.7× larger unscripted sample of the same speaker on the same topic gives **10.4**. ② **The markers decline monotonically as register formalises — in his own mouth, on his own lines.** `very` runs 4.6 improvised → 0.9 in the lines he read aloud and kept → 0.4 written. So `very` is an *improvisation artifact*, not a constitutive marker, and **62-16 is wrong on that point.** ③ **The ratio rule is also register-bound:** `so` outnumbers `but` when he improvises (1.36) and flattens to **1.00** in his own read-aloud-approved lines. "So must outnumber but" is not a law of his voice; it is a law of his *thinking out loud*.
⚠ **Caveat, stated because this file has been burned before:** the locked-line corpus is **extracted fragments**, and connectors live at the joints extraction drops — so 7.5 is a **floor, not a point estimate**, and the `and` rate there (12.2) is pure extraction artifact and must not be cited. The number cannot be biased *upward*, which is what matters here. Falsifier: a full transcribed read-aloud of a locked script measuring ≥15/1k would overturn this.
**⭐⭐ CONFIRMED OUT OF SAMPLE, same day, on a DIFFERENT and PUBLISHED video — and the falsifier failed.** #56 (`yt:aSfZtrgGjwA`) is the only other project with read-aloud records. Comparing the read-aloud page he was handed against the **auto-transcript of what he actually said on camera**:

| #56 | words | `so` | `but` | ratio | `so`+`but` | `very` |
|---|---|---|---|---|---|---|
| the PAGE handed to him | 1,725 | 4.6 | 7.0 | 0.67 | **11.6** | 0.6 |
| what he SAID, published | 1,589 | 3.1 | 6.3 | **0.50** | **9.4** | **0.0** |

**Three things this settles.** ① The stated falsifier for this entry was "a transcribed read-aloud measuring ≥15/1k overturns it." It came in at **9.4** — identical to #62's current script. The band 8–11 holds on a second video, in his own delivered voice. ② **`very` is ZERO across a full published video.** Not low — absent. 62-16's "`very` is constitutive" is **dead**; it is an improvisation-only marker, and no ASR artifact explains a clean zero across 1,589 words. ③ **The ratio is 0.50 — `but` outnumbers `so` two to one in his actual delivery**, and he pushed it further that way than the page did (0.67 → 0.50). **"He is a `so` speaker" is false for scripted delivery** and must never again be used as a target.
⚠⚠ **And the direction was backwards.** The T7 carried-forward note, and advice given to him on 2026-07-22, both held that *"the `very`/hedge gap is a microphone problem, not a page problem — it closes at the mic."* **It does not. At the microphone, reading a script, he STRIPS connectors** (11.6 → 9.4) and says `very` zero times. He tightens; he does not loosen. Any future pass that adds markers "because he'll say them anyway" is adding words he will delete on camera. ⚠ Caveat: YouTube transcript, and he ad-libs pickups, so ±1/1k. Nothing that moves the conclusion.
**Operational:** the ≥12 aspiration and the "41% of natural" framing are **WITHDRAWN**. Keep the **≥8/1k floor** as a drift check only — it catches punctuation-replacing-connectors, which is real (62-14). **No ceiling, no ratio target, and stop adding `very` and clause-final hedges to written drafts** — four passes produced one `very` between them because the register does not want one. The pre-lock band is **8–11/1k, and #62 at 9.4 is already inside it.** *Source: measured 2026-07-22 by the main thread; creator-initiated. Supersedes the connector half of 62-14b and the `very` half of 62-16.*

### 62-20 [P] ⭐⭐ His lines are not lost to bad writing — they are lost to TIDYING — MEASURED (n=9)
2026-07-22, #62 Codex collaboration. Nine violations of the locked-line corpus were found in one draft across two sessions (six by Codex, two by the main thread on audit, one — the ninth — inside the very line Codex proposed cutting). **Every one moved in the same direction, and not one was bad writing:**

| his line | what replaced it | the move |
|---|---|---|
| "This state lasted for about three years." | "It lasted about three years." | concrete noun → pronoun |
| "The east **of Ukraine** fell… **In the west**, Volhynia…" | one merged sentence | two sentences → one |
| "That's what I try to do on this channel. **I go** to the sources…" | em-dash merge | two sentences → one |
| "So that's why honoring these men is useful now." | "gives Ukraine a history of resistance to Moscow" | plain landing → abstract summary |
| "Now the idea had men to carry it out." | "the movement had both the idea… and trained men capable…" | plain landing → abstract summary |
| "reporting a finished job **up to** his superiors" | "telling his superiors he had destroyed…" | verbal phrase → nominal shuffle |
| "…father of the **Organization of Ukrainian Nationalists**" | "…father of the OUN" | expansion → acronym |
| "calls Russia's atrocities at Bucha **what they are**" | "…by their name" | idiom → generic phrase |
| "**We should try to look**… without justifying everything they did" | "As long as we don't downplay…" | recast into a conditional |

**Every replacement is grammatical. Most are shorter. Several are clearer in isolation. None would be caught by `voice_lint` or any style rule** — because each is an improvement by every standard except the one that matters. The three recurring moves are: **merging two of his sentences into one · replacing a concrete noun with a pronoun · converting a plain landing into an abstract summary of itself.**
**Operational consequence — the reason this is the session's most valuable finding:** *a locked line cannot be protected by any rule about quality; it can only be protected by the diff.* Any pass touching a chapter with locked lines must diff against `VOICE-CORPUS-FOR-MODEL-PASSES.md` §1 **before returning**, not after. **"I only tightened it" is the signature of the failure, not a defence.** Also note the discovery pattern: the ninth violation was invisible for seven read-alouds *and* two model audits, and surfaced only because a costed cut proposal put that exact line under a diff. *Source: nine measured diffs, 2026-07-22.*

### 62-19 [Su] Two exhibits from the same source about the same subject need YEAR-handles, not noun-handles — VALIDATED
2026-07-21. CH7 carries two Stelmashchuk papers — a 1945 confession and a 1943 letter — each with a different Ukrainian objection, one checkable and one not. Written as one interleaved paragraph it failed; rewritten as two paragraphs (claim → attack → answer each) it **still** failed, and he mis-assigned the rebuttal: *"we DO have a copy of this LETTER from 1961 in Ukraine's archives? WHY DOES UKRAINE CLAIM ITS FAKE THEN?"* — the 1963 copy is of the **confession**, not the letter. Fix that worked: **tag every mention with its year** ("the 1945 confession", "the 1943 letter"), including inside each rebuttal, plus one explicit sentence that the two objections are *different* ("And Ukraine's objection to this one is different…"). Generalises: when two pieces of evidence share a source, a subject and an opponent, the nouns naming them are not distinctive enough for the ear — a date is. ⚠ Standing risk flagged: if a future read still trips there, the answer is likely to cut one document rather than rewrite a fourth time. *Source: his mis-read, which was the diagnosis.*

### 62-14b [P] ⚠⚠ CORRECTION TO 62-14 — the "#57 em-dash drift" was an n=2 artifact and is WITHDRAWN — MEASURED (n=25)
2026-07-21, same day. 62-14 below claims the em-dash-replacing-connectors drift is "a scripting-layer drift dating to #57," on the strength of **two** scripts (#56 ratio 0.71, #57 ratio 3.33). The cross-script measurement (`VOICE-DRIFT-CROSS-SCRIPT-2026-07-21.md`, 25 measurable written scripts) **falsifies it**: em-dash runs at a **catalogue median of 18.5/1k from video #1 onward** (range 3.7–29.2), video #1 itself is 23.8, and the trend is flat (videos ≤30 median 17.6 · >30 median 19.1). **#56 at 5.3 is the outlier — second-lowest in the catalogue — not #57 at 21.4.** Heavy em-dash use is his scripted norm. **No em-dash threshold may be set.** ⭐ **BUT the connector half of 62-14 is now VERIFIED and is the study's strongest finding** (recomputed same day, total `so`+`but` across all 28 scripts): **gold 21.0/1k · catalogue median 7.4 · range 3.2–13.7 · every script below half his natural rate**, from video #1, with no trend. So "written scripts cut his connectors to about a third of natural" was CORRECT; only "it started at #57" was false. ⚠ **Use the connector rate directly, not the em-dash:connector ratio** — the ratio's spread (0.00–8.25) is em-dash noise on a near-constant connector floor. **Pre-lock floor: `so`+`but` ≥ 8/1k.** #62 v7.0 after a full connector pass = 8.6 (41% of natural). **What DID replicate:** nominalization is the real catalogue-wide drift (gold 11.8/1k vs catalogue median **38.7**, high in every script), and sentence length drifts **short** (gold median 13 vs catalogue **9**) — i.e. the staccato tell, not a wordiness tell. **The transferable lesson is methodological: a two-video voice comparison produced a confident, canon-altering, false finding that was written into `VOICE-PROFILE.md` within the hour. Single-video voice claims get checked against the catalogue BEFORE they enter canon.** *Source: cross-script measurement; the write-up was salvaged by the main thread after the agent was killed by a session limit.*

### 62-14 [V] ⭐⭐ The AI accent is in the JOINTS, not the vocabulary — ⚠ **its em-dash/#57 claim is SUPERSEDED by 62-14b above; the rest stands** — MEASURED (live pick pending)
2026-07-21 whole-script phrasing audit (`_research/PHRASING-AUDIT-2026-07-21.md`), triggered by his flag that the script was "bloated with ai speak… in the logic and phrasing and words used and the way the script is structured with phrases." **The instinct was right and the location was wrong.** Vocabulary measured *cleaner than his own gold*: Latinate content-word share 7.6% (gold 9.2%, lane 10.9%), passive 2.9/1k (lane 7.9), scholarly hedges 0. Six condensation passes had already stripped the diction. **The drift was entirely structural:** colon-reveals 17 against the existing Fable T8 cap of ~2 (6.2/1k vs gold 0.0, lane max 0.7) · nominalizations 22.5/1k vs gold 11.8 · thirteen sentences over 35 words, six at 40–56, against a true spoken ceiling of ~30 · abstractions in subject slots where his gold puts a person or a country. **⭐ THE HEADLINE: his spoken causal spine has been replaced by punctuation.** Gold runs `so` 11.8/1k + `but` 9.2/1k = **21.0**; the script ran **7.6** while the em-dash ran **24.6/1k**. Control against his own locked/filmed/published scripts — em-dash : spoken-connector ratio = **0.71 (#56) · 3.33 (#57) · 3.24 (#62)** — proves this is a **scripting-layer drift dating to #57, not a per-video fault**, and that every written script cuts his connectors to about a third of natural. 32 rewrites applied (colons 17→7, semicolons 2→0, real over-35w sentences 13→0, WARN 15→10, net −3 words); the em-dash only moved 24.6→21.8, because the rest requires swapping the dash for the *word his mouth would use*, which is a read-aloud job. **Guard on the fix:** anti-staccato is his #1 too-AI tell, so every split must yield two FLOWING sentences (Natural→Scripted row 3), never a stab. *Source: measured audit; not yet read-aloud confirmed.*

### 62-15 [V] ⭐ Harvest share predicts phrasing quality — 23% of the script is his mouth, and the 3%-harvest chapter held the worst sentences — MEASURED
Same audit. 5-gram overlap against an 8,293-token corpus of his ad-libs + read-aloud quotes: **10.8% high-confidence + 12.1% partial = ≈23% creator-harvested, ≈77% Claude-authored** (band 18–28%; conservative both directions). Per-chapter the harvest is uneven and **tracks the defect density almost exactly**: CH9 at 50% harvested was the cleanest chapter in the script; **CH5 at 3% harvested held the 56-word sentence, the 44-word Redesha frame and the 39-word Snyder frame** — the three worst in the video. This is the quantitative version of [[feedback-read-aloud-catches-logic]] and of 62-11's finding that the same day's new connective prose produced 37% of the flagged figures from 8.5% of the words. **Operational read: harvest share is a cheap defect predictor — chapters written without his voice in the room need the heaviest phrasing scrutiny, and the fix is to get more of the script through his mouth, not through more passes.** *Source: measured audit 2026-07-21.*

### 62-16 [V] The hedge strip was over-applied — `very` and clause-final `I think` are constitutive, not nerves — PARTIALLY VALIDATED
`FINGERPRINT-UNSCRIPTED` §3/§9 measure his colloquial hedge family at ~15.8/1k and `very` at 11.8/1k, and call them constitutive. `VOICE-PROFILE`'s Natural→Scripted table says drop "I guess" as first-video nerves. **That narrow instruction got applied as a blanket strip:** the v7.0 script ran the hedge family at 0.7/1k with `basically`, `I think`, `I guess` and `very` all at literally ZERO across 2,841 words (only `actually` survived, at 1.45/1k — dead-on his gold's 1.31). The distinction the profile intended: drop the *humility* hedge that undercuts a claim; keep the intensifier and keep clause-final `I think` on a **verdict**, which is referee register, not nerves. Applied: the CLOSE restored to his T4 shape — *"And that, I think, is the whole fight. Can you glorify people for one thing they stood for, when they also did other terrible things?"* — replacing a fronted cleft + colon that had demoted his question to a subordinate `whether`-clause. Zero word cost. ⚠ `very` still at 0; not yet restored anywhere. *Source: audit §6.3; the CLOSE restoration is not yet read-aloud confirmed.*

### 62-13 [V] He is BELOW the lane floor on deadpan understatement — IDEA, not yet tested live
Same study: register-drop/deadpan understatement runs **0.8–2.2 per 1k words in 6/6 lane channels** (second-most-universal figure measured); v7.0 has ~0. His §Humor rule ("only when it arises naturally — never a quota; zero is fine") is about *jokes*, but the lane move is a flat sentence letting an absurd or grim fact deflate itself — different device. Also **resolves the open S8/N1 tension**: the register-drop is lane-universal, but every instance found across six channels is a **complete sentence with a verb** — the FRAGMENT form is Kraut's personal tic, not the lane's, which is consistent with the 2026-07-20 grill finding that anti-staccato has no pivot-position carve-out. ⚠ Untested on him; on an atrocity topic the constraint is that it can never sit on the killing itself. *Source: lane study §4 L1; no live pick yet.*

---

## Gold standard — unscripted video (`yMAWJcjo_ug`) — S5 fingerprint, 2026-06-12

Source: `channel-data/calibration/FINGERPRINT-UNSCRIPTED.md` (full quantitative distributions there — 741 words, 39 sentences, single-sample caveat applies). Tier: **VALIDATED** (it IS him), scope-limited to the unscripted conversational register; VOICE-PROFILE.md supersedes on conflict.

### GS-01 [V] Flat, wide sentence-length distribution — flowing, not clipped — VALIDATED
Median 13w, mean 19w, modal bucket 11–15w, and a genuine 26% of sentences at 21+ words. Short sentences are 13% and functional, never dramatic fragments. Quantifies the VOICE-PROFILE flowing-over-staccato reversal. *Source: FINGERPRINT §1.*

### GS-02 [V] Causal stack: so ≫ because; "which is why" / "and that meant" don't occur unscripted — VALIDATED
so=9 (6 sentence-initial), because=4, "the reason why"=1, which-is-why=0, and-that-meant=0. The style guide's fancier connectors are writer's tools to ration, not his defaults. *Source: FINGERPRINT §2.*

### GS-03 [V] Zero rhetorical questions — invitations are imperatives — VALIDATED
0 questions in 39 sentences; audience asks are imperative ("send them my way," "ask me to debunk something"). Free-floating rhetorical questions have a natural baseline of ~0 (setup-questions he immediately answers are the one scripted exception — 57-28). *Source: FINGERPRINT §6.*

### GS-04 [V] First-person stance openers, not presentational openers — VALIDATED
Sentence starts: I/I'm (8), So (6), And (6). Zero "Here's/Now,/Look,/Listen." He enters a thought through his own position ("I'm passionate about…," "I know that…"). *Source: FINGERPRINT §4.*

### GS-05 [V] Clause-final hedges and "yeah"-exhale closes; never aphoristic closes — VALIDATED
"…I guess" ×3 clause-final, "so yeah…" paragraph exhales, scope-back qualifiers at sentence end ("at least in the historical community"). The aphoristic mirrored close is alien to the register (squares with 56-12's lock-stage cut). *Source: FINGERPRINT §5.*

### GS-06 [V] "very" is the intensifier; "really" = 0 — VALIDATED
very=9 (1.2/100w: "very first," "very little basis," "very good reason"); really=0. Cheap, checkable lint datum. *Source: FINGERPRINT §3.*

### GS-07 [V] One Latinate word per plain sentence — elevation never clusters — VALIDATED
"propagate," "fantastical," "misinterpreted," "counterbalance" each sit alone inside otherwise plain sentences. Cluster of abstract Latinate vocabulary = writer's register error (the 56-05 jargon-cluster whack-a-mole, seen from the positive side). *Source: FINGERPRINT §8.*

### GS-08 [V] Audience-as-collaborator imperatives — VALIDATED
"Send them my way" ×2, "send me constructive feedback," "ask me to debunk something even if you believe it," "you don't have to take my word for it, but please look into these things" — the engagement register is collaborative tasking, and it's the embryo of the channel method line (#57's "go to the document and read it"). *Source: FINGERPRINT §8.*

### GS-09 [V] Dry concrete-image mockery, triple-adjective dismissals — VALIDATED
"Turn you into a parrot" (bad pedagogy), "cool and edgy and flashy" (viral junk, polysyndeton listing). Mockery lands through a concrete image or a flat list — never sneering, never hot. *Source: FINGERPRINT §8.*

### GS-10 [V] Push-through self-correction — repeat the function word, never re-cast — VALIDATED
16 stutter-repeat events/741w ("that that are known," "I I I try"); zero sentence abandonments, zero "let me rephrase." His delivery absorbs imperfection without resetting — script rhythm should assume forward momentum, not clean-room sentences. *Source: FINGERPRINT §7.*

---

## Reference creators (Kraut + Alex O'Connor) — S6 naturalness mine, 2026-06-12

Source: `channel-data/calibration/REFERENCE-CREATOR-NATURALNESS.md` (full inventory + verbatim anchors there). Tier: **ALL IDEA** — his refs, not his voice (rules-hedge); ⚡TENSION items are queued for S8 as the most informative.

### RC-01 [V] Same-breath concession-pivot — IDEA
Both refs concede and pivot inside one sentence ("yes there are indeed non-biblical sources… however it is worth noticing…"), as a per-evidence reflex rather than a dedicated steelman section. Candidate upgrade to the channel's concede-first structure: micro-concessions at every evidence beat, not only the Act-1 concede. *Source: REFERENCE-CREATOR-NATURALNESS N9, §5.1.*

### RC-02 [V] One wry interpretive sentence immediately after evidence, then move on — IDEA
Both refs cap evidence with exactly one interpretation line, often dry ("the name kind of gives away the predatory nature"; "right off the bat this isn't really an argument for atheism") — never milked into a paragraph. Sharpens 56-18 (interpret every quote) with a LENGTH cap: one sentence. *Source: N2/N7 + §5.2.*

### RC-03 [Su] Concrete artifact carries the thesis — IDEA
Kraut's unclosable Stolichnaya bottle (designed on the assumption the bottle is finished in one sitting) does the work of a statistics paragraph. Research-phase implication: hunt for one thesis-bearing ARTIFACT per act, not just quotes and numbers. Extends concrete-first (P4) from sentence level to evidence selection. *Source: N8.*

### RC-04 [Su] Source's epistemic journey as credential — IDEA
O'Connor: "my friend and biblical scholar John Nelson… a Christian who used to think it could be reconciled but changed his mind." A changed-mind scholar is a stronger trust signal than a title alone — natural fit for debunk formats where the steelman needs teeth. *Source: N12.*

### RC-05 [V] Limitation disclosure as authority move — IDEA
O'Connor names what is NOT his area on contested terrain ("church patristics is really not my area… don't look to me for advice"). Gold standard has the same instinct ("I'm not a history teacher although I do tutor it"). Candidate: one scripted limitation-disclosure beat on videos where he's reading outside his strongest lane. *Source: N4; GS cross-ref.*

### RC-06 [V] ⚡TENSION bundle — fragment-pivots, formal connectors, answered-question chains — IDEA (route to S8)
Three ref mechanics conflict with validated/gold signals: (a) Kraut's register-drop fragment "Then came the Mongols." vs the earned-fragment reversal; (b) Kraut's free However/Consequently vs the gold so≫because stack; (c) O'Connor's 2-3-question dialectical chains (immediately answered) vs GS-03 zero-rhetorical-questions. Each needs a grill line-variant test, not adoption. *Source: N1/N10 + §2 + Tensions section.*

---

## S4 — Retention-curve → beat mapping (all post-publish reports), mined 2026-06-12

> **ALL HYPOTHESIS [St]/[Su].** Per `memory/feedback-channel-data-too-small`: individual-video retention is noise — nothing below is actionable per-video; only the cross-video zone histogram (RP-8) is promoted, and even that stays a hypothesis. Beat labels: 13 videos map to actual chapter names from their YOUTUBE-METADATA.md; the rest get coarse zone labels (the analyses report position % only). Severity: HIGH ≥10% of remaining viewers lost at that point, MED 5–10%, LOW <5%. Source files: `channel-data/analyses/POST-PUBLISH-ANALYSIS-*.md` + archived project folders.

**No retention data (no mapping possible):** `Q5Pfv_dPubU`, `c2uRn7U9jsk`, `ejkC0ecYyxk` (analysis ran before data existed / API errors), `imPn_OxLYlk` #37 Vichy (report has no retention section).

**Data anomaly:** `o8A0CqQDQws` (#24 Iran protests) reports 112.1% average retention — measurement artifact; rows kept but excluded from interpretation.

### 5 Big Myths About Israel and Palestine Busted! (`7fpBz6uo504`, avg ret 33.4%, 718s)

| Pos % | Beat | Drop | Candidate cause |
|---|---|---|---|
| 2% | hook (0-5%) | HIGH (13.6%) | packaging→content mismatch; arrivals bounce on claim confirm |
| 3% | hook (0-5%) | MED (8.2%) | packaging→content mismatch; arrivals bounce on claim confirm |
| 4% | hook (0-5%) | MED (7.2%) | packaging→content mismatch; arrivals bounce on claim confirm |

### Did Pagans Actually Copy Christmas? (`l8abBf4aMv8`, avg ret 25.0%, 879s)

| Pos % | Beat | Drop | Candidate cause |
|---|---|---|---|
| 2% | hook (0-5%) | HIGH (17.3%) | packaging→content mismatch; arrivals bounce on claim confirm |
| 3% | hook (0-5%) | HIGH (16.2%) | packaging→content mismatch; arrivals bounce on claim confirm |
| 5% | hook (0-5%) | MED (5.2%) | packaging→content mismatch; arrivals bounce on claim confirm |

### Europe's Last Divided Capital: The Cyprus Problem (`n-CUSE4bDvg`, avg ret 35.9%, 556s)

| Pos % | Beat | Drop | Candidate cause |
|---|---|---|---|
| 2% | hook (0-5%) | HIGH (20.2%) | packaging→content mismatch; arrivals bounce on claim confirm |
| 3% | hook (0-5%) | HIGH (10.1%) | packaging→content mismatch; arrivals bounce on claim confirm |
| 4% | hook (0-5%) | HIGH (12.1%) | packaging→content mismatch; arrivals bounce on claim confirm |

### Four Articles That Killed the Soviet Union #GeoPolitics #ColdWar (`PZqOXNvi9Ks`, avg ret 67.2%)

| Pos % | Beat | Drop | Candidate cause |
|---|---|---|---|
| 4% | hook (0-5%) | MED (7.5%) | packaging→content mismatch; arrivals bounce on claim confirm |
| 5% | hook (0-5%) | MED (6.7%) | packaging→content mismatch; arrivals bounce on claim confirm |
| 9% | setup (6-14%) | MED (5.0%) | setup/method drag before the turn |
| 10% | setup (6-14%) | MED (5.6%) | setup/method drag before the turn |
| 11% | setup (6-14%) | MED (8.7%) | setup/method drag before the turn |
| 12% | setup (6-14%) | MED (5.9%) | setup/method drag before the turn |

### Honduras Called These Islands British Territory. Then Claimed Them (`sXadwOj8VoA`, avg ret 40.9%, 653s)

| Pos % | Beat | Drop | Candidate cause |
|---|---|---|---|
| 3% | hook (0-5%) — ch: "Britain's Last African Colony" | HIGH (24.1%) | packaging→content mismatch; arrivals bounce on claim confirm |
| 5% | hook (0-5%) — ch: "Britain's Last African Colony" | HIGH (10.3%) | packaging→content mismatch; arrivals bounce on claim confirm |
| 18% | turn zone (15-25%) — ch: "The 1,500 People Already Living There" | MED (6.9%) | turn beat late, weak, or absent |
| 35% | first-half evidence (26-50%) — ch: ""Your Island Has Been Sold"" | MED (6.9%) | evidence-beat fatigue / missing pattern interrupt |

### How 3 Coups Ended 60 Years of French Control in Africa (`jLZngVFKWVg`, avg ret 17.7%, 812s)

| Pos % | Beat | Drop | Candidate cause |
|---|---|---|---|
| 2% | hook (0-5%) | HIGH (18.5%) | packaging→content mismatch; arrivals bounce on claim confirm |
| 3% | hook (0-5%) | HIGH (14.8%) | packaging→content mismatch; arrivals bounce on claim confirm |
| 5% | hook (0-5%) | HIGH (11.1%) | packaging→content mismatch; arrivals bounce on claim confirm |
| 6% | setup (6-14%) | HIGH (11.1%) | setup/method drag before the turn |
| 15% | turn zone (15-25%) | MED (7.4%) | turn beat late, weak, or absent |

### How the KGB Weaponized Palestinian Resistance (`UH2PddfaaR8`, avg ret 44.8%, 606s)

| Pos % | Beat | Drop | Candidate cause |
|---|---|---|---|
| 2% | hook (0-5%) | HIGH (16.2%) | packaging→content mismatch; arrivals bounce on claim confirm |
| 3% | hook (0-5%) | MED (8.9%) | packaging→content mismatch; arrivals bounce on claim confirm |

### How The Soviet Union Died In Just 3 Weeks (`5LMKEVybT3E`, avg ret 47.8%)

| Pos % | Beat | Drop | Candidate cause |
|---|---|---|---|
| 15% | turn zone (15-25%) | MED (7.3%) | turn beat late, weak, or absent |
| 17% | turn zone (15-25%) | MED (7.4%) | turn beat late, weak, or absent |
| 19% | turn zone (15-25%) | HIGH (11.8%) | turn beat late, weak, or absent |
| 20% | turn zone (15-25%) | MED (5.9%) | turn beat late, weak, or absent |
| 22% | turn zone (15-25%) | MED (5.9%) | turn beat late, weak, or absent |

### I Investigated the SHOCKING Sale of Kashmir and Here's What I Found! (`lPilDVSAeEM`, avg ret 21.3%, 629s)

| Pos % | Beat | Drop | Candidate cause |
|---|---|---|---|
| 2% | hook (0-5%) | MED (9.6%) | packaging→content mismatch; arrivals bounce on claim confirm |
| 3% | hook (0-5%) | HIGH (11.4%) | packaging→content mismatch; arrivals bounce on claim confirm |
| 4% | hook (0-5%) | HIGH (16.8%) | packaging→content mismatch; arrivals bounce on claim confirm |
| 6% | setup (6-14%) | MED (8.2%) | setup/method drag before the turn |

### Iran's Protests: The Same Fight for 120 Years (`o8A0CqQDQws`, avg ret 112.1%)

| Pos % | Beat | Drop | Candidate cause |
|---|---|---|---|
| 10% | setup (6-14%) | MED (6.3%) | setup/method drag before the turn |

### Iran’s 1979 Referendum During the Hostage Crisis (`VgcQSUgYyYQ`, avg ret 46.1%)

| Pos % | Beat | Drop | Candidate cause |
|---|---|---|---|
| 15% | turn zone (15-25%) | MED (6.3%) | turn beat late, weak, or absent |
| 18% | turn zone (15-25%) | MED (5.6%) | turn beat late, weak, or absent |
| 20% | turn zone (15-25%) | MED (5.6%) | turn beat late, weak, or absent |

### ISIS Cited This Map. It Never Decided Anything. (`BXyT8OTGBBo`, avg ret 36.9%, 666s)

| Pos % | Beat | Drop | Candidate cause |
|---|---|---|---|
| 2% | hook (0-5%) | HIGH (18.8%) | packaging→content mismatch; arrivals bounce on claim confirm |
| 3% | hook (0-5%) | HIGH (15.6%) | packaging→content mismatch; arrivals bounce on claim confirm |
| 4% | hook (0-5%) | HIGH (10.4%) | packaging→content mismatch; arrivals bounce on claim confirm |
| 9% | setup (6-14%) | MED (5.2%) | setup/method drag before the turn |
| 11% | setup (6-14%) | MED (6.2%) | setup/method drag before the turn |

### Morocco's 1,700-Mile Wall (And the Vote That Never Happened) (`QgDJSu0Y5K0`, avg ret 28.2%, 667s)

| Pos % | Beat | Drop | Candidate cause |
|---|---|---|---|
| 2% | hook (0-5%) | HIGH (16.2%) | packaging→content mismatch; arrivals bounce on claim confirm |
| 3% | hook (0-5%) | HIGH (14.3%) | packaging→content mismatch; arrivals bounce on claim confirm |
| 4% | hook (0-5%) | MED (6.7%) | packaging→content mismatch; arrivals bounce on claim confirm |
| 6% | setup (6-14%) | MED (5.7%) | setup/method drag before the turn |
| 7% | setup (6-14%) | MED (5.7%) | setup/method drag before the turn |

### Operation Ajax: Not a Fluke, But a Repeat (`ztgOuhZOJEs`, avg ret 63.3%)

| Pos % | Beat | Drop | Candidate cause |
|---|---|---|---|
| 25% | turn zone (15-25%) | MED (5.4%) | turn beat late, weak, or absent |
| 38% | first-half evidence (26-50%) | MED (5.4%) | evidence-beat fatigue / missing pattern interrupt |

### Primary Sources Destroy the 'Awesome Crusades' Narrative (`VyPv2n4mii8`, avg ret 28.4%, 635s)

| Pos % | Beat | Drop | Candidate cause |
|---|---|---|---|
| 2% | hook (0-5%) | MED (6.0%) | packaging→content mismatch; arrivals bounce on claim confirm |
| 3% | hook (0-5%) | HIGH (17.4%) | packaging→content mismatch; arrivals bounce on claim confirm |
| 4% | hook (0-5%) | HIGH (12.9%) | packaging→content mismatch; arrivals bounce on claim confirm |
| 6% | setup (6-14%) | MED (5.3%) | setup/method drag before the turn |

### Putin Says NATO Promised Not to Expand. The Documents Disagree. (`499YLd1BHZ4`, avg ret 48.3%, 342s)

| Pos % | Beat | Drop | Candidate cause |
|---|---|---|---|
| 2% | hook (0-5%) | MED (6.5%) | packaging→content mismatch; arrivals bounce on claim confirm |
| 5% | hook (0-5%) | MED (8.7%) | packaging→content mismatch; arrivals bounce on claim confirm |
| 35% | first-half evidence (26-50%) | MED (6.5%) | evidence-beat fatigue / missing pattern interrupt |
| 96% | close (76-100%) | MED (6.5%) | payoff done — recap/CTA exit |

### Russia Warned About Crimea & Donbas in 1991 (`a2cJZOEgjZE`, avg ret 68.4%)

| Pos % | Beat | Drop | Candidate cause |
|---|---|---|---|
| 21% | turn zone (15-25%) | MED (6.4%) | turn beat late, weak, or absent |
| 23% | turn zone (15-25%) | MED (5.4%) | turn beat late, weak, or absent |
| 28% | first-half evidence (26-50%) | MED (5.0%) | evidence-beat fatigue / missing pattern interrupt |

### Somaliland's Legal Independence Problem (`GuL9PtXEjN0`, avg ret 25.8%, 673s)

| Pos % | Beat | Drop | Candidate cause |
|---|---|---|---|
| 2% | hook (0-5%) — ch: "The country the world forgot" | HIGH (17.3%) | packaging→content mismatch; arrivals bounce on claim confirm |
| 3% | hook (0-5%) — ch: "The country the world forgot" | HIGH (17.6%) | packaging→content mismatch; arrivals bounce on claim confirm |
| 4% | hook (0-5%) — ch: "The country the world forgot" | MED (9.2%) | packaging→content mismatch; arrivals bounce on claim confirm |
| 5% | hook (0-5%) — ch: "The country the world forgot" | MED (7.1%) | packaging→content mismatch; arrivals bounce on claim confirm |
| 6% | setup (6-14%) — ch: "The country the world forgot" | MED (7.1%) | setup/method drag before the turn |

### The 'Ancient Hatreds' Narrative Is Completely Wrong About the Middle East (`Ac-k2p9Gvj4`, avg ret 32.2%, 568s)

| Pos % | Beat | Drop | Candidate cause |
|---|---|---|---|
| 2% | hook (0-5%) | HIGH (17.4%) | packaging→content mismatch; arrivals bounce on claim confirm |
| 3% | hook (0-5%) | HIGH (10.9%) | packaging→content mismatch; arrivals bounce on claim confirm |
| 4% | hook (0-5%) | MED (8.7%) | packaging→content mismatch; arrivals bounce on claim confirm |
| 6% | setup (6-14%) | MED (5.4%) | setup/method drag before the turn |

### The 1922 Treaty Loophole That Ended the USSR (`TYNaIu28LeU`, avg ret 31.2%, 291s)

| Pos % | Beat | Drop | Candidate cause |
|---|---|---|---|
| 2% | hook (0-5%) | HIGH (16.7%) | packaging→content mismatch; arrivals bounce on claim confirm |
| 3% | hook (0-5%) | MED (8.3%) | packaging→content mismatch; arrivals bounce on claim confirm |
| 4% | hook (0-5%) | MED (8.3%) | packaging→content mismatch; arrivals bounce on claim confirm |
| 27% | first-half evidence (26-50%) | MED (8.3%) | evidence-beat fatigue / missing pattern interrupt |

### The 1947 Map That Set the South China Sea on Fire (`LrthC_8Hb2Y`, avg ret 50.5%, 282s)

| Pos % | Beat | Drop | Candidate cause |
|---|---|---|---|
| 2% | hook (0-5%) | MED (8.8%) | packaging→content mismatch; arrivals bounce on claim confirm |
| 5% | hook (0-5%) | MED (6.6%) | packaging→content mismatch; arrivals bounce on claim confirm |
| 6% | setup (6-14%) | MED (6.6%) | setup/method drag before the turn |

### The 1947 Partition Map Didn't Follow Religion (`-kg30uRUY1M`, avg ret 25.8%, 639s)

| Pos % | Beat | Drop | Candidate cause |
|---|---|---|---|
| 2% | hook (0-5%) — ch: "The Draft Map" | HIGH (25.3%) | packaging→content mismatch; arrivals bounce on claim confirm |
| 3% | hook (0-5%) — ch: "The Draft Map" | HIGH (14.3%) | packaging→content mismatch; arrivals bounce on claim confirm |
| 5% | hook (0-5%) — ch: "The Draft Map" | MED (5.5%) | packaging→content mismatch; arrivals bounce on claim confirm |
| 100% | close (76-100%) — ch: "The Road to Kashmir" | MED (5.5%) | payoff done — recap/CTA exit |

### The 200‑Year‑Old Tariff Myth That Drains Your Wallet (`JkH4XIHfnJU`, avg ret 32.1%, 692s)

| Pos % | Beat | Drop | Candidate cause |
|---|---|---|---|
| 2% | hook (0-5%) | HIGH (13.3%) | packaging→content mismatch; arrivals bounce on claim confirm |
| 3% | hook (0-5%) | HIGH (12.4%) | packaging→content mismatch; arrivals bounce on claim confirm |
| 6% | setup (6-14%) | MED (5.7%) | setup/method drag before the turn |

### The Dark Ages: What Americans Believe vs What the Evidence Shows (`-QG8trhNsoM`, avg ret 31.7%, 645s)

| Pos % | Beat | Drop | Candidate cause |
|---|---|---|---|
| 2% | hook (0-5%) — ch: "What Americans think about the Middle Ages" | HIGH (14.2%) | packaging→content mismatch; arrivals bounce on claim confirm |
| 3% | hook (0-5%) — ch: "What Americans think about the Middle Ages" | HIGH (10.4%) | packaging→content mismatch; arrivals bounce on claim confirm |
| 4% | hook (0-5%) — ch: "What Americans think about the Middle Ages" | MED (8.5%) | packaging→content mismatch; arrivals bounce on claim confirm |
| 5% | hook (0-5%) — ch: "What Americans think about the Middle Ages" | MED (6.6%) | packaging→content mismatch; arrivals bounce on claim confirm |

### The Flat Earth Myth Was Invented in 1828. Here's Who Did It. (`LuLZYZWMiU4`, avg ret 13.2%, 1070s)

| Pos % | Beat | Drop | Candidate cause |
|---|---|---|---|
| 2% | hook (0-5%) | HIGH (12.8%) | packaging→content mismatch; arrivals bounce on claim confirm |
| 3% | hook (0-5%) | HIGH (25.6%) | packaging→content mismatch; arrivals bounce on claim confirm |
| 4% | hook (0-5%) | HIGH (16.8%) | packaging→content mismatch; arrivals bounce on claim confirm |

### The Georgia Playbook: How 2008 Predicted Ukraine (`71xY0Pt4T-M`, avg ret 26.8%, 360s)

| Pos % | Beat | Drop | Candidate cause |
|---|---|---|---|
| 2% | hook (0-5%) | HIGH (12.8%) | packaging→content mismatch; arrivals bounce on claim confirm |
| 3% | hook (0-5%) | HIGH (10.3%) | packaging→content mismatch; arrivals bounce on claim confirm |
| 5% | hook (0-5%) | HIGH (10.2%) | packaging→content mismatch; arrivals bounce on claim confirm |
| 6% | setup (6-14%) | MED (7.7%) | setup/method drag before the turn |
| 9% | setup (6-14%) | HIGH (10.3%) | setup/method drag before the turn |
| 11% | setup (6-14%) | MED (5.1%) | setup/method drag before the turn |
| 21% | turn zone (15-25%) | MED (5.1%) | turn beat late, weak, or absent |
| 32% | first-half evidence (26-50%) | MED (5.1%) | evidence-beat fatigue / missing pattern interrupt |
| 33% | first-half evidence (26-50%) | MED (5.1%) | evidence-beat fatigue / missing pattern interrupt |
| 36% | first-half evidence (26-50%) | MED (5.1%) | evidence-beat fatigue / missing pattern interrupt |

### The Hidden Pattern Behind the Armenia Conflict (`UxsXdUj0EhU`, avg ret 32.1%, 842s)

| Pos % | Beat | Drop | Candidate cause |
|---|---|---|---|
| 2% | hook (0-5%) | HIGH (29.4%) | packaging→content mismatch; arrivals bounce on claim confirm |
| 3% | hook (0-5%) | HIGH (10.1%) | packaging→content mismatch; arrivals bounce on claim confirm |
| 6% | setup (6-14%) | MED (7.3%) | setup/method drag before the turn |
| 7% | setup (6-14%) | MED (5.5%) | setup/method drag before the turn |

### The Middle East: A British Betrayal (`njjQoeA9lTE`, avg ret 48.3%)

| Pos % | Beat | Drop | Candidate cause |
|---|---|---|---|
| 6% | setup (6-14%) | HIGH (12.9%) | setup/method drag before the turn |
| 9% | setup (6-14%) | MED (5.9%) | setup/method drag before the turn |
| 11% | setup (6-14%) | MED (7.1%) | setup/method drag before the turn |

### The Phantom Island That Was on Maps for 400 Years (`P6yalauLDic`, avg ret 28.2%, 495s)

| Pos % | Beat | Drop | Candidate cause |
|---|---|---|---|
| 2% | hook (0-5%) — ch: "The Phantom Island" | HIGH (20.0%) | packaging→content mismatch; arrivals bounce on claim confirm |
| 5% | hook (0-5%) — ch: "The Phantom Island" | HIGH (10.0%) | packaging→content mismatch; arrivals bounce on claim confirm |
| 7% | setup (6-14%) — ch: "The Phantom Island" | HIGH (10.0%) | setup/method drag before the turn |
| 18% | turn zone (15-25%) — ch: "The 1539 Error" | HIGH (30.0%) | turn beat late, weak, or absent |
| 19% | turn zone (15-25%) — ch: "The 1539 Error" | HIGH (10.0%) | turn beat late, weak, or absent |
| 26% | first-half evidence (26-50%) — ch: "The 1539 Error" | HIGH (10.0%) | evidence-beat fatigue / missing pattern interrupt |

### The Piri Reis Map Cites Columbus. Hancock Calls It 12,000 Years Old (`zt7VntgauC8`, avg ret 32.2%, 628s)

| Pos % | Beat | Drop | Candidate cause |
|---|---|---|---|
| 3% | hook (0-5%) — ch: "The claim" | HIGH (11.1%) | packaging→content mismatch; arrivals bounce on claim confirm |
| 4% | hook (0-5%) — ch: "The claim" | MED (9.0%) | packaging→content mismatch; arrivals bounce on claim confirm |
| 5% | hook (0-5%) — ch: "The claim" | MED (8.3%) | packaging→content mismatch; arrivals bounce on claim confirm |
| 6% | setup (6-14%) — ch: "The claim" | MED (5.6%) | setup/method drag before the turn |

### Two Countries Split a Continent They Had Never Mapped (`WgE2FLsDhfk`, avg ret 18.8%, 769s)

| Pos % | Beat | Drop | Candidate cause |
|---|---|---|---|
| 2% | hook (0-5%) — ch: "The Language Map" | MED (7.4%) | packaging→content mismatch; arrivals bounce on claim confirm |
| 3% | hook (0-5%) — ch: "The Language Map" | HIGH (35.6%) | packaging→content mismatch; arrivals bounce on claim confirm |
| 4% | hook (0-5%) — ch: "The Language Map" | HIGH (12.0%) | packaging→content mismatch; arrivals bounce on claim confirm |
| 5% | hook (0-5%) — ch: "The Language Map" | MED (7.2%) | packaging→content mismatch; arrivals bounce on claim confirm |

### Venezuela vs Guyana: The Oil War Over Essequibo (`oDK52GwjTIo`, avg ret 35.6%, 633s)

| Pos % | Beat | Drop | Candidate cause |
|---|---|---|---|
| 2% | hook (0-5%) | MED (7.6%) | packaging→content mismatch; arrivals bounce on claim confirm |
| 3% | hook (0-5%) | MED (8.0%) | packaging→content mismatch; arrivals bounce on claim confirm |
| 4% | hook (0-5%) | MED (5.5%) | packaging→content mismatch; arrivals bounce on claim confirm |

### Was Lagertha Real? DNA Says Female Viking Warriors Existed (`2RQWu-cyO90`, avg ret 28.9%, 606s)

| Pos % | Beat | Drop | Candidate cause |
|---|---|---|---|
| 2% | hook (0-5%) | HIGH (19.6%) | packaging→content mismatch; arrivals bounce on claim confirm |
| 4% | hook (0-5%) | HIGH (21.7%) | packaging→content mismatch; arrivals bounce on claim confirm |
| 6% | setup (6-14%) | MED (6.5%) | setup/method drag before the turn |
| 57% | second-half evidence (51-75%) | MED (6.5%) | mid-evidence drag |

### Was Stalin Really a Hero? The Evidence Says Otherwise (`Yx5oywZs-rk`, avg ret 38.1%, 602s)

| Pos % | Beat | Drop | Candidate cause |
|---|---|---|---|
| 2% | hook (0-5%) | HIGH (20.0%) | packaging→content mismatch; arrivals bounce on claim confirm |
| 3% | hook (0-5%) | MED (7.5%) | packaging→content mismatch; arrivals bounce on claim confirm |
| 5% | hook (0-5%) | MED (5.0%) | packaging→content mismatch; arrivals bounce on claim confirm |

### Why a 1908 Map is Still Killing People: Thailand vs. Cambodia (`xODFE2Pyubo`, avg ret 30.6%, 442s)

| Pos % | Beat | Drop | Candidate cause |
|---|---|---|---|
| 2% | hook (0-5%) | HIGH (25.9%) | packaging→content mismatch; arrivals bounce on claim confirm |
| 4% | hook (0-5%) | HIGH (14.8%) | packaging→content mismatch; arrivals bounce on claim confirm |
| 6% | setup (6-14%) | MED (7.4%) | setup/method drag before the turn |
| 9% | setup (6-14%) | MED (7.4%) | setup/method drag before the turn |
| 16% | turn zone (15-25%) | MED (7.4%) | turn beat late, weak, or absent |
| 32% | first-half evidence (26-50%) | MED (7.4%) | evidence-beat fatigue / missing pattern interrupt |
| 40% | first-half evidence (26-50%) | MED (7.4%) | evidence-beat fatigue / missing pattern interrupt |
| 64% | second-half evidence (51-75%) | MED (7.4%) | mid-evidence drag |
| 74% | second-half evidence (51-75%) | MED (7.4%) | mid-evidence drag |

### Why Egypt and Sudan Both Reject Bir Tawil (`XKAqt_ZLHGo`, avg ret 23.2%, 534s)

| Pos % | Beat | Drop | Candidate cause |
|---|---|---|---|
| 2% | hook (0-5%) — ch: "A Virginia Dad Claims African Territory" | HIGH (13.4%) | packaging→content mismatch; arrivals bounce on claim confirm |
| 4% | hook (0-5%) — ch: "A Virginia Dad Claims African Territory" | HIGH (17.9%) | packaging→content mismatch; arrivals bounce on claim confirm |
| 5% | hook (0-5%) — ch: "A Virginia Dad Claims African Territory" | MED (7.5%) | packaging→content mismatch; arrivals bounce on claim confirm |

### Why Iran's 1906 Revolution Was Unique (`ICCROht7uK8`, avg ret 72.9%)

| Pos % | Beat | Drop | Candidate cause |
|---|---|---|---|
| 16% | turn zone (15-25%) | MED (6.5%) | turn beat late, weak, or absent |
| 20% | turn zone (15-25%) | MED (6.5%) | turn beat late, weak, or absent |
| 25% | turn zone (15-25%) | MED (5.7%) | turn beat late, weak, or absent |

### Why Spain Didn't "Civilize" Peru: The 500-Year Lie (`6GybGd_q25w`, avg ret 32.2%, 754s)

| Pos % | Beat | Drop | Candidate cause |
|---|---|---|---|
| 2% | hook (0-5%) | HIGH (22.2%) | packaging→content mismatch; arrivals bounce on claim confirm |
| 3% | hook (0-5%) | HIGH (15.6%) | packaging→content mismatch; arrivals bounce on claim confirm |
| 18% | turn zone (15-25%) | MED (8.9%) | turn beat late, weak, or absent |
| 38% | first-half evidence (26-50%) | MED (6.7%) | evidence-beat fatigue / missing pattern interrupt |
| 100% | close (76-100%) | MED (8.9%) | payoff done — recap/CTA exit |

### Why Trump Walked Back the Armenian Genocide (`Oc7oq292HkM`, avg ret 28.9%, 753s)

| Pos % | Beat | Drop | Candidate cause |
|---|---|---|---|
| 2% | hook (0-5%) | HIGH (17.1%) | packaging→content mismatch; arrivals bounce on claim confirm |
| 3% | hook (0-5%) | MED (7.6%) | packaging→content mismatch; arrivals bounce on claim confirm |
| 4% | hook (0-5%) | HIGH (10.8%) | packaging→content mismatch; arrivals bounce on claim confirm |
| 5% | hook (0-5%) | MED (5.1%) | packaging→content mismatch; arrivals bounce on claim confirm |
| 6% | setup (6-14%) | MED (5.1%) | setup/method drag before the turn |

### Yes Slavery Existed In Africa. Then Europe Took Over (`aSfZtrgGjwA`, avg ret 28.2%, 667s)

| Pos % | Beat | Drop | Candidate cause |
|---|---|---|---|
| 2% | hook (0-5%) — ch: "The Claim" | HIGH (20.0%) | packaging→content mismatch; arrivals bounce on claim confirm |
| 3% | hook (0-5%) — ch: "The Claim" | MED (6.7%) | packaging→content mismatch; arrivals bounce on claim confirm |
| 4% | hook (0-5%) — ch: "The Claim" | HIGH (10.7%) | packaging→content mismatch; arrivals bounce on claim confirm |
| 8% | setup (6-14%) — ch: "The Claim" | MED (5.3%) | setup/method drag before the turn |

### S4 cross-video zone histogram (videos with ≥1 drop in zone, n=40)

| Zone | Videos | Promoted? |
|---|---|---|
| hook (0–5%) | 33 | → RP-8 |
| setup (6–14%) | 20 | → RP-8 |
| turn zone (15–25%) | 11 | → RP-8 |
| first-half evidence (26–50%) | 9 | → RP-8 |
| close (76–100%) | 3 | → RP-8 (borderline, exactly 3) |
| second-half evidence (51–75%) | 2 | NOT promoted (<3 videos) |

---

## Recurring patterns (cross-video)

*(Populated by S2 from the draft-vs-locked diffs, 2026-06-12. Each pattern cites its per-video evidence; all VALIDATED unless noted.)*

### RP-1 [St] Claim-first cold open — the lock version always restructures the hook around the claim
#56: scene-first v1 (Prince Henry 1444) → claim-first v8 ("There's a claim… It goes like this" + streamer clip, scene becomes the payoff). #57: narrated-context v2 and paradox-card v3 → spoken claim-stack escalation at lock ("most accurate map… seafaring civilization… aliens"). → memory `feedback-script-structural-architecture` P1, now diff-validated in 2 videos. *Evidence: 56-11(a) + #57 cold-open chain.*

### RP-2 [P] Register imports fail, mechanics imports survive
Externally-imported REGISTER (NLM Fig-Tree parasocial signatures in #56; competitor direct-address cadence + paradox-card format in #57 v3) gets systematically stripped at the creator pass. Externally-imported MECHANICS (document-reveal pointers, split-screen translation builds, stay-on-face quote performance) survive and spread. Test imports by class before spending a pass on them. *Evidence: 56-07 + 57-19; consistent with 58-04 (own old tics as negative corpus).*

### RP-3 [V] Stagey rhetorical questions and quotable aphorisms get cut at lock — even after surviving multiple versions
#56: "What happens when you ignore the culture war…?" cut; "Read it. The denial contains the confession." cut at v8 after surviving 4 versions; date-math opener cut. #57: "keep that test in your pocket," "Let's do what nobody does," paradox-card copy — all cut. The writer's most quotable lines are the most likely lock casualties. *Evidence: 56-12 + 56-16 + 57-16/57-19.*

### RP-4 [Su] Quote discipline: set up what it proves before, close-read it after
#56: de Marees confirmation-risk front-load (56-02) generalized to every quote at lock (56-18). #57: baseline-before-exception survived every rewrite (the Hancock claim stated fairly before each debunk), and the lock added the genealogy steelman (57-18). The frame around a quote is as load-bearing as the quote. *Evidence: 56-02/56-18 + 57-01/57-18.*

### RP-5 [P] Lock-direction length is bimodal: evidence beats expand, device beats get cut
#56 GREW 1,180→1,820 (under-evidenced draft gained an asiento section, a bridge beat, a full steelman). #57 SHRANK 5,407→3,640 (device/meta/corroboration beats cut wholesale). Same law as #58's grill calibration: completeness → MORE, device → LEAN (58-06). "Tighten the script" is the wrong instruction; the right one is "expand the evidence, cut the apparatus." *Evidence: 56-20 + 57-15/57-16 + 58-06.*

### RP-6 [Su] Verdict language shrinks to what was shown
#56: absolutist closing aphorism → scoped claim + audience-honesty beat (56-22), plural "letters of African kings" corrected to the one letter shown (56-14). #57: "the one man who could read it" overclaim cut at lock (57-22); editorial labels replaced by close reading in #56 (56-19) and report-don't-sell in #57 (57-01). The locked script consistently claims LESS than the draft and proves more. *Evidence: 56-14/56-19/56-22 + 57-01/57-22.*

### RP-7 [V] Delivery strips written apparatus: asides, recaps, second verbatims, foreign text — HYPOTHESIS (S3, both videos)
On camera, both #56 and #57 shed the same four apparatus classes: mid-sentence em-dash asides (56-24), recap lines (57-05 confidence note), VO-scripted verbatims beyond the first (56-26/56-28/57-25), and anything not in the video's established terminology (57-26). Script-side implication: write the VO layer as if these will be dropped — load-bearing facts in main clauses, one verbatim per beat in the voice, the rest on cards. Tier stays HYPOTHESIS until a grill confirms intent (the cuts could be edit-room, not instinct). *Evidence: S3 entries across #56 + #57.*

### RP-8 [St] Retention-drop zone histogram — where the channel's videos lose people — HYPOTHESIS (S4, n=40)
Across every video with retention data: hook-zone drops (0–5%) in 33/40 videos (universal arrival-bounce — partly platform noise, but severity varies 6%→26%, so hook quality still differentiates); setup-zone (6–14%) in 20/40 (the most channel-specific cluster — method/setup drag before the turn); turn-zone (15–25%) in 11/40 (consistent with the validated turn-at-15–25% rule: when the turn is late or weak, this is where it shows); first-half evidence (26–50%) in 9/40; close (76–100%) in 3/40 (borderline at exactly 3). Second-half (51–75%) appeared in only 2 videos — NOT promoted. Interpretation stays hypothesis: per-video curves are noise (feedback-channel-data-too-small); what 3+ videos share is the ZONE, not a confirmed cause. Strongest writable lead: the 6–14% setup zone is the biggest non-universal cluster — candidate S8 grill question on what occupies minutes 0:45–1:40 of a typical script. *Evidence: S4 section tables, 162 drop rows.*

---

## S9 grill resolutions (Session A, 2026-06-12) — all VALIDATED (user-picked)

### GR-A9 [Su] Artifact-hunt directive: one thesis-bearing object per act — VALIDATED
Research phase explicitly hunts a third evidence class beyond quotes and numbers: an object or document-feature that proves the point by itself (Kraut's unclosable Stolichnaya bottle; the channel's own accidental versions — Lausanne's zero instances of "Kurd," the Piri Reis source-list inscription). Beats may then open on the THING instead of a statistic. Use conditions (all three): it explains the point; a non-academic grasps it instantly; it's honest — no cherry-picked prop. Imports RC-03; extends concrete-first (P4) from sentence level to evidence selection. Wire into /research + 01-VERIFIED-RESEARCH template at S11. Sub-rule (RC-04 adopted): the changed-mind scholar credential ("X, who long argued the opposite, now writes…") — use when true, never manufactured. *Source: S9 grill 2026-06-12, agenda item A9.*

### GR-B7 [P] The canonical production flow — creator-stated end-to-end (S12) — VALIDATED
Stated in his own words at S12 (2026-06-12), refining GR-B1/B2: (1) decide the video together (interest + keywords + comment mining + competitor research + initial research); (2) deep research surfaces material — scope/thesis allowed to move; (3) structure emerges DURING research as a loop (propose → push back → agree → re-research in function of the video → adjust); (4) loop converges on a final structure + evidence per beat — he approves (= the structure lock); (5) PRE-SCRIPT QUESTION ROUND — specific prepared questions on evidence presentation, transitions, key sentences, asked BEFORE writing (amends GR-B1: checkpoints move pre-script, one round, not mid-writing interruptions); (6) full script written FROM the answers; (7) his read-through = T1 verification — SUCCESS METRIC: zero feedback needed; whatever's off gets fixed locally; (8) everything he says feeds the calibration loop. Canonicalized in `.claude/commands/script.md` §THE CANONICAL PRODUCTION FLOW. *Source: S12 walk 2026-06-12, creator process statement.*

### GR-B6 [P] Teleprompter = professional render; pause markers selective, never systematic — VALIDATED
The teleprompter render (derived from locked SCRIPT.md, per teleprompter-after-lock) is built to professional teleprompter conventions. Pause/beat markers are added only where a pause is load-bearing (the 2–3 seams per script where the pause IS the effect — pre-reveal, post-verdict); everything else flows unmarked. Addresses 56-25 (unmarked written drama gets flattened live) without over-marking. *Source: S10 grill 2026-06-12, agenda item B6.*

### GR-B5 [P] Quote completeness is a RESEARCH deliverable — script writes from the bank only — VALIDATED
Phase-2 research must extract ALL useful quotes for the video — round-trip-verified verbatims with page + provenance — into 01-VERIFIED-RESEARCH before scripting begins. The script is written from the bank only; no new quotes enter mid-draft (kills mid-draft verification churn at the source). Backstop unchanged: load-bearing on-screen verbatims get one re-confirmation at the lock gate (58-02 — verification notes go stale), cheap because the bank did the heavy lifting. Strengthens the single-source-of-truth doctrine from "verified facts only" to "complete quote extraction before writing"; sibling of GR-B3's better-too-much-than-too-little research bar. *Source: S10 grill 2026-06-12, agenda item B5.*

### GR-B4 [P] Re-scan both layers: scoped per-round on new text + full script at lock — VALIDATED
Every beat written or rewritten in a round is re-scanned (voice_lint + register/corpus-scan) BEFORE the round's diff is shown, flags inline; plus one comprehensive full-script scan at the lock gate for accumulated regressions. Codifies 56-05 (register whack-a-mole: new text concentrates new flags) into mechanical /script flow. *Source: S10 grill 2026-06-12, agenda item B4.*

### GR-B3 [P] Preparation bar + heavy gate: creator input is the LAST gate, never the first filter — VALIDATED
Two layers. (a) PREPARATION BAR before requesting ANY creator input (including GR-B1 checkpoints and the GR-B2 beat-list): research thoroughly first — better too much than too little — fully understand the topic, and arrive with a committed idea of how to phrase everything and how to build the video. Checkpoints show prepared variants, never blank questions (extends 57-02 digest-don't-punt). (b) HEAVY GATE before his top-to-bottom read-aloud, guaranteed-done in order: notebook grounding on all mechanism beats → attribution audit → seam flow-check (57-10) → voice_lint → corpus-scan → Bar-talk test on solo-written lines. Slowest to first read, fewest wasted reads — his read-aloud is T1 verification, not a draft filter. *Source: S10 grill 2026-06-12, agenda item B3.*

### GR-B2 [P] Beat-list gate: lock the spine before any prose — VALIDATED (HARD GATE)
Before sentence-level work of any kind: the creator approves a one-screen beat list (each beat = one line + its evidence) checked against the title — "what is the video we're trying to make." Prose is co-written (GR-B1) only on the locked spine. Codifies 57-15 (two polish passes sunk on the wrong structure) and 57-03 (title-scope check) into a formal /script gate. v18 flow: beat-list lock → co-write with checkpoints → small local polish. *Source: S10 grill 2026-06-12, agenda item B2.*

### GR-B1 [P] Co-draft the script — checkpoint phrasings DURING writing, don't deliver a draft to demolish — VALIDATED
The revision-economy model is collaborative drafting: while writing, at load-bearing or uncertain phrasing points (hook, verdict line, mechanism beats, key transitions), pause and ask the creator the best way to phrase it — concrete variants in chat (feedback-grill-easier format) — and assemble the script from picked lines. Full-draft-then-revise is the failure mode: cold drafts invite 10x+ fix rounds, and mid-revision rewrites change the feel and structure of the whole video. Post-draft changes must stay small and localized. Dissolves the batch-size question (no big revision rounds if co-built); refines 57-08 (propose-don't-act) and 57-07 ("more phrases" = he wants more 2-3-option checkpoints); pairs with 58-05 (pre-filter candidates via Bar-talk test before showing). Checkpoint-class operationalization → S11 /script flow design. *Source: S10 grill 2026-06-12, agenda item B1.*

### GR-A10 [St] One engineered no-VO hold per video — adopted as a TEST — VALIDATED (decision), device unproven
One image-only hold (1–3s), placed after the single strongest document reveal, marked in the script/edit guide ("[HOLD ON DOCUMENT — no VO, 2s]"). User-approved as worth testing — NOT yet a proven device; judge at the edit layer + retention check before promoting to standing rule. Imports CRAFT R9 scoped to one hold per video; pairs with stay-on-face quote performance (56-08). *Source: S9 grill 2026-06-12, agenda item A10.*

### GR-A8 [St] Scripted enumerations need a matching on-screen asset — no arity rule — VALIDATED
The #57 toponym truncation (57-29c) is EXPLAINED, not a pattern: the on-screen asset was a map with translations, not the scripted three-item list, so he trimmed the spoken list to what the viewer could follow. The "proof lists are 2-survivable" candidate rule is WITHDRAWN. Actual rule (prep layer): when the script enumerates N items as proof, the asset must display those N items (labeled, followable); build the asset to the list or trim the list to the asset BEFORE filming. Methodology note: textbook case of why SRT deltas stay HYPOTHESIS until the creator explains the cause (feedback-postmortem-methodology). *Source: S9 grill 2026-06-12, agenda item A8.*

### GR-A7 [Su] Load-bearing facts: promote it or cut it — never in an aside — VALIDATED (HARD RULE)
A fact that must survive delivery gets its own main clause ("He takes his royal fifth. Forty-six people, for his personal estate."). If it can't earn a main clause within the runtime budget, it moves to the on-screen card or gets cut — it never rides in an em-dash aside or relative clause, because delivery sheds asides first (56-24 upgraded from HYPOTHESIS; imports CRAFT R2 as a hard rule scoped to load-bearing facts). *Source: S9 grill 2026-06-12, agenda item A7.*

### GR-A6 [Su] Source-anchored micro-concessions at evidence beats — concede the true part when the source shows it — VALIDATED
When the document on screen genuinely confirms part of the opposing claim, concede that part in the same breath ("And yes — that's a Dutch trader confirming Africans sold slaves to Europeans. That part's true.") then pivot to what else the source shows. Per-beat reflex IN ADDITION to the sectioned concede (56-17 architecture stands). Anchor condition: the concession must be shown by the on-screen source — never a ritual "to be fair." Imports RC-01 (refs' same-breath concession-pivot) in source-anchored form; doubles as the standard handling of confirmation-risk quotes (56-02). *Source: S9 grill 2026-06-12, agenda item A6.*

### GR-A5 [Su] Quote default = paraphrase in VO + verbatim on card; verbatim delivery is earned by self-sufficiency — VALIDATED
Default for every quote: the voice speaks the paraphrase/explanation, the card carries the exact words — because most historical quotes need their meaning explained, and that explanation IS the channel's job. Exception: a quote strong enough to live by itself (no gloss needed) gets read verbatim — and is stronger for being rare. Underlying guard: the video is an explanation that uses quotes, never a sum of quotes. Upgrades 56-11(b)/56-28/57-25 to rule; extends VOICE-PROFILE's quote-stack→speak-one+cards with the self-sufficiency test for WHICH one earns the voice. *Source: S9 grill 2026-06-12, agenda item A5.*

### GR-A4 [St] Closers run chronological — flash-forward only when the outcome is already known — VALIDATED
The closer's spine is strict chronology; the dramatic irony comes from the timeline itself ("He died never knowing…" → "and there it stayed… until 1929"), never from structural intercutting. A flash-forward clause is permitted only when the outcome is already known or obvious to the viewer, so it spoils nothing. Upgrades 57-27 from HYPOTHESIS to rule: the delivered chronological order was the right call, not an accident. *Source: S9 grill 2026-06-12, agenda item A4.*

### GR-A3 [St] Method declaration: one hook-tail clause OR after the first source — never a standalone pre-evidence beat — VALIDATED
What occupies 0:45–1:40 is evidence, not throat-clearing. The method declaration either (a) compresses to a clause on the hook tail ("…and the way to settle it is to just read the sources. So let's read them.") or (b) waits until the first source is on screen, then declares the method with the document as exhibit. Refines 56-13 (the standalone method bridge was the weaker form) and answers RP-8's setup-zone drag (20/40 videos bleed at 6–14%): get to the first document fast. *Source: S9 grill 2026-06-12, agenda item A3.*

### GR-A2 [St] Thesis spoken in full ONCE — at the close; the whole video is setup for it — VALIDATED
The video's thesis is stated clearly at the END; everything before exists to earn that line. No early same-words plant, no restatement device — imported craft rule R6 (strategic redundancy) is REJECTED even in exact-words form. The verdict line is a destination, not a refrain; recaps stay dead (57-05, RP-7 confirmed at the rule level). Pairs with RP-6 (verdict language scoped to what was shown) — one terminal, scoped, fully-earned thesis line. *Source: S9 grill 2026-06-12, agenda item A2.*

### GR-A1 [St] Disclaimers are trigger-gated, not default — VALIDATED
Viewer-directed disclaimers don't come naturally and enter a script ONLY when a trigger fires: (1) genuinely sensitive topic; (2) the creator is giving his own opinion; (3) the video deliberately gives one side more weight; (4) plain honesty requires it (hijab #52 precedent). Default = the method line does the disclaimer's work ("This video is about one document and what it says when you actually read it") — the channel's core is presenting the discipline of history and how historians reach conclusions, which carries the fairness signal by itself. Resolves the 57-30 contradiction: the Hancock disclaimer died at delivery because no trigger fired. Scholar-fallibility honesty beats ("Kahle got plenty wrong, too") fall under trigger 4 — include when the correction record does argumentative work, never as ritual. *Source: S9 grill 2026-06-12, agenda item A1.*

---

## Side files (created by later S-steps)

- `FINGERPRINT-UNSCRIPTED.md` — S5
- `REFERENCE-CREATOR-NATURALNESS.md` — S6
- `CRAFT-RULES-IMPORTED.md` — S7
- `INTERVIEW-AGENDA.md` — S8
- `AGENT-DIFF-PROPOSALS.md` — S11
- `EVAL-BASELINE.md` — S13
