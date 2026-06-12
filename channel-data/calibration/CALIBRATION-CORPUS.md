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

## Side files (created by later S-steps)

- `FINGERPRINT-UNSCRIPTED.md` — S5
- `REFERENCE-CREATOR-NATURALNESS.md` — S6
- `CRAFT-RULES-IMPORTED.md` — S7
- `INTERVIEW-AGENDA.md` — S8
- `AGENT-DIFF-PROPOSALS.md` — S11
- `EVAL-BASELINE.md` — S13
