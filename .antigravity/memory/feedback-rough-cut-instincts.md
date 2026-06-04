---
name: Rough Cut Instincts (Recording-Pass Script Revisions)
description: 7 patterns the user consistently applies during recording to a Claude-generated script — bake these into v1 to reduce edit-pass deviation
type: feedback
originSessionId: e6c721d6-472a-4615-a01e-3e681e3cea78
---
## Source incident — Tripoli rough cut (2026-04-27)

User recorded `02-SCRIPT-DRAFT.md` v5-FINAL of project 51 (Treaty of Tripoli Article 11). Comparing the rough cut SRT against the locked script revealed 7 distinct on-the-fly revisions. None were corrections; all were instinctive improvements applied while reading the script aloud. They are voice-level signal for what the script-writer-v2 agent should be doing in v1.

This is different from `feedback-scriptcollab.md` — that file covers user-as-editor (when they paste a draft). This file covers user-as-performer (when they read a Claude-generated script aloud and improve it on the fly).

---

## The 8 instincts (1–7 surfaced during recording, 8 surfaced post-recording)

### 1. Add the causal chain that the script stripped out for word count

**What happened:** Script Beat 2 jumped straight to consequence: *"American merchant ships were being seized. Their crews were being held for ransom. The United States needed a treaty."*

User read it as: *"When America declared independence in 1776, it lost the protection of the British Navy. Almost immediately, the corsairs of North Africa pounced. American merchant ships were being seized... Without a big navy to its name, the New Republic's only defense was diplomacy."*

**Why:** The script tried to be lean and assumed audience would infer the cause. User's instinct: explain the mechanism. This matches CLAUDE.md principle "Deep causal chains — explain WHY." The script wrote the symptom; user added the disease.

**How to apply:** When script-writer-v2 cuts setup for runtime, it cuts the causal chain *first* by mistake. Bake the cause-effect chain in at v1, even if it costs 10–15 seconds. The user will keep it. Only trim DETAILS (vote counts, citations, restatements), never trim CAUSATION.

---

### 2. Drop verbal Chekhov's gun in favor of visual setup

**What happened:** Script Beat 2 had: *"The Arabic original... was held for over a century in the State Department file. **It looks like this. We'll come back to it.**"*

User dropped both sentences. Just held the Arabic manuscript on screen and moved on.

**Why:** The verbal "we'll come back to it" felt YouTube-y for the Calm Prosecutor voice. The visual does the same structural work — show the artifact, the audience tracks it. Saying "we'll come back to it" announces the trick.

**How to apply:** For History vs Hype voice, prefer **visual** Chekhov's guns over verbal ones. Show the artifact with a caption; let silence and screen-time hold the unresolved thread. Verbal "we'll come back to it" / "remember that" / "this matters later" reads as influencer scaffolding the user instinctively rejects.

---

### 3. Drop staccato when it's stylistic decoration, not argument

**What happened:** Script Beat 4: *"Not mistranslated. Not paraphrased. Missing."*

User read it as: *"It was not mistranslated or paraphrased. The Arabic texts simply didn't contain the article."*

**Why:** Staccato fragments look punchy on the page but feel forced when spoken if they're not earned by stakes. The reveal is dramatic enough on its own — the staccato added nothing the prose couldn't carry.

**How to apply:** Reserve staccato for moments where the stakes are at peak — the reveal itself, a turn, a closing line. Don't deploy it on supporting beats. Calm Prosecutor voice = restrained delivery, occasional staccato hit. Script-writer-v2 currently over-uses staccato as a stylistic tic.

---

### 4. Drop self-aware tags ("It is, in other words..." / "That is, essentially...")

**What happened:** Script had two meta-explanatory tags:
- Beat 4: *"It is, in other words, the wrong document."*
- Beat 5: *"That is, essentially, the entirety of it."*

User dropped both. Trusted the audience to draw the conclusion.

**Why:** These phrases announce "I'm now telling you what to think." Calm Prosecutor voice = present the evidence, let the audience reach the verdict. Self-aware tags break that.

**How to apply:** Audit script v1 for "in other words," "essentially," "basically," "to put it simply." If the next clause restates what the audience just heard, cut the whole sentence. The original line stands alone.

---

### 5. Drop verbal source citations; let on-screen overlay carry it

**What happened:** Script Beat 5: *"Per Sam Haselby, on page 109 of his 2015 Oxford monograph: Article 11 was the breaking point. Dwight rejected Barlow's radicalism..."*

User read it as: *"Disgusted by his former protege's radical turn, Dwight publicly denounced him and ordered Barlow's portrait stripped from the walls of the university."*

**Why:** Reciting "page 109 of his 2015 Oxford monograph" in voiceover sounds like academic posturing. The on-screen citation overlay does the credibility work. The voiceover should narrate the *story*.

**How to apply:** In script v1, put the citation in the **on-screen overlay direction**, not the spoken line. VO line says the claim; visual line shows the source. This already works for Hunter Miller / Hurgronje quotes (text overlay verbatim) — extend the pattern to ALL secondary-historian citations. Save 5–8 seconds per video.

**Exception:** The forensic-mystery beats where the historian's act of finding the document IS the story (Hurgronje examining the original, Hunter Miller flagging the gap). There the historian belongs in the voiceover.

---

### 6. Drop precision numbers that don't pay off in argument

**What happened:** Script Beat 3: *"The Senate voted yes. Twenty-three senators. None against. The Senate Journal records it on page 244."*

User read it as: *"The Senate voted yes. The Senate Journal records it on page 244."*

**Why:** "Twenty-three senators. None against." was decoration. The argument doesn't turn on the vote count. The Senate Journal page reference IS the argument — it's the primary-source anchor.

**How to apply:** Audit every numerical specific in script v1. Ask: does this number pay off in the argument? If yes (page 371, page 244, June 7th 1797 = the dates and citations that anchor evidence), keep. If no (vote counts, monetary figures with no comparison, populations cited once and never again), cut. The Calm Prosecutor uses numbers as exhibits, not flair.

---

### 7. Document-anchored close, not abstract close

**What happened:** Script Beat 6 closing: *"Both sides of the modern fight read themselves into a 1797 document that nobody at the time even debated — and the signers only half-understood. **The fight is real. It just isn't from 1797.**"*

User's improvised closing: *"Today this English text is wielded as the ultimate weapon in a modern culture war. But the Arabic original, it's just a mundane letter between two politicians."*

**Why:** "The fight is real. It just isn't from 1797" is a thesis statement about the meta-argument. User's version is a thesis statement about the **two documents** — which is what the entire video has been about. It returns to the artifacts. Document-first close beats abstraction close.

**How to apply:** For document-first format videos, the closing line should refer to a specific artifact shown earlier — the manuscript, the page number, the named treaty. Not the abstraction it represents. Test: can you point at the screen during the closing line? If yes, the close is anchored.

---

### 8. Articulate a single-sentence thesis the audience walks away with — bigger than the case (surfaced post-recording, 2026-04-27)

**What happened:** the Tripoli rough cut chains evidence beautifully (treaty signed → Article 11 ratified → Arabic missing → Hurgronje 1930 → Cobbett + Dwight reactions → 133-year silence → Crane's re-reading). But it ends without crystallizing a single takeaway the audience can carry into another conversation. Crane's "wielded by both sides" line is an *observation*, not a *thesis*. The viewer learns a thing; they don't carry an idea.

User raised this themselves while reviewing the cut: *"one thing i did miss from this video (that we can maybe take to another one) is an overarching message or thread or story."*

**Why this matters more than the other 7:** the other instincts are line-level / paragraph-level adjustments. This is structural. A script can pass every other instinct check and still fail this one — and it'll still feel like "interesting but forgettable" instead of "I'll be thinking about this for a week." This is what separates HvH evidence-density from a Wendover-style channel-defining claim.

**Why this happens with Claude-generated scripts:** the agent optimizes for evidence density and verbatim accuracy. Both are good. Neither produces a thesis. A thesis is upstream of evidence — it's the LENS that decides which evidence belongs in this video and which is for another video. Without a thesis lock at the planning stage, the script-writer fills the runtime with the strongest evidence available and ends on whichever historian's quote sounds most conclusive. That's a *case status*, not a *takeaway*.

**How to apply going forward:**

1. Before the script-writer agent gets its first turn, the user (or NotebookLM via Use Case 18) must answer: *"After watching this, the viewer should think: ___________." (≤12 words)*
2. The answer must be a CLAIM, not a summary; bigger than the case study; falsifiable in principle.
3. Five thesis types map to common HvH topics (power-asymmetry, time-shifted meaning, system-as-designed, mechanism-over-narrative, invisible-until-named).
4. The thesis must touch THREE structural slots in the script:
   - **Hook payoff preview** — tee up the thesis as a promise of investigation, don't state it
   - **Turn or 2nd hook** — the strongest evidence makes the audience FORM the thesis themselves
   - **Close** — single ≤12-word sentence that lands the thesis, anchored to a named artifact
5. If the script-writer can't articulate the thesis in 12 words, the topic isn't ready for scripting — it's still research.

**Codified into:**
- `script-writer-v2.md` Rule 36 (THESIS THROUGH-LINE) — Tier 2 STRUCTURAL, mandatory
- `NOTEBOOKLM-SCRIPTWRITING-PROMPTS.md` Use Case 18 (Thesis Articulation Check) — pre-writing gate
- `SCRIPT-TO-DELIVERY-LESSONS.md` Lesson 32 (Walk-Away Test)
- `script-writer-v2.md` SCRIPT METADATA template — `**Thesis (≤12 words, Rule 36):**` and `**Thesis Type:**` are now required metadata fields

**Candidate Tripoli theses (for the next video that revisits this material, or a follow-up):**
- "What gets ratified is what the powerful side can read." (power-asymmetry — primary)
- "What we 'always believed' the founders said is what later generations needed them to have said." (time-shifted meaning — secondary)
- "The most important things in history are what nobody noticed." (invisible-until-named — captures the 133-year silence)

---

## Net pattern across all 8

The user instinctively pulls the script *toward* the artifacts and *away* from rhetorical scaffolding. Setup (mechanism, causation) gets richer; performance (staccato, meta-tags, vote counts, verbal Chekhov's guns) gets stripped.

This is a stable signal. Bake it into script-writer-v2 v14.4:
- More cause-effect setup at v1
- Visual Chekhov's guns (cued in B-roll directions), not verbal ones
- Staccato reserved for reveals/turns/closes only
- No "in other words" / "essentially" / "to put it simply" auto-tags
- Citations in overlay directions, not voiceover, except when the historian's act of finding is the story
- Numerical specifics only when they anchor primary-source evidence
- Document-first format closes refer back to a named artifact

**Why this matters:** every instinct the user applies during recording = wasted script-writer-v2 effort + post-production friction. Every instinct caught at v1 = clean takes and faster edits.

---

## How to apply going forward

1. When script-writer-v2 generates v1 for a document-first format video, run this checklist before delivering:
   - Causal chain present in setup beats?
   - Chekhov's guns implemented as B-roll directions, not VO lines?
   - Staccato deployed only at reveal/turn/close?
   - No "in other words" / "essentially" tags?
   - Secondary citations in overlay directions, not VO?
   - Numerical specifics earn their seconds?
   - Closing line points at a named artifact?

2. When user pastes a rough cut SRT for editing analysis, compare against the locked script and look for these 8 patterns. If they're showing up, the script-writer didn't catch them. Log the gap.

3. **Done (2026-04-27):** Codified into `script-writer-v2.md` as Rule 36 (THESIS THROUGH-LINE) and Rule 32F.2b (visual Chekhov's gun). Quality checklist updated. Metadata template now requires `**Thesis (≤12 words):**` and `**Thesis Type:**` fields. Lessons 25–32 appended to `SCRIPT-TO-DELIVERY-LESSONS.md`. NotebookLM Use Case 18 added as the mandatory pre-writing thesis gate. Agent bumped to v14.4.

---

## Manhattan rough cut — IDEAS, not rules (2026-05-01)

Project 45. SCRIPT.md v-final vs `rough first cut.srt`. ~70% kept verbatim. 9 on-the-fly revisions: 4 reinforce instincts 1, 6, 25, 26 (stable signals). 5 are new — captured as **hypotheses to watch for in the next 2–3 forensic videos**, not rules to enforce. n=1 each. Per the rules-hedging principle: don't over-constrain script-writer-v2 from a single video. Sometimes deliberately NOT cutting is what makes HvH unique.

**Where they live:** Ideas 33–37 in `SCRIPT-TO-DELIVERY-LESSONS.md`. Not codified into script-writer-v2 rules.

### Idea 9. Skip Standard Myth Narration act for famous myths?
Manhattan's 1-min "Here's how the story goes. 1626. Peter Minuit steps ashore..." act got cut entirely. Hook → Turn → dismantling worked fine without it. Could be: famous myths pre-load in the audience's head, so reciting feels like stalling. Could also be: Manhattan-specific. Watch the next forensic video.

### Idea 10. Bolted-on Modern Relevance can read as tangent in forensic format?
Manhattan's 1-min 2026 NYC anniversary catalog (Founded by NYC, Lenape Heritage Day, MCNY exhibit, sentinels, Smithsonian) got cut entirely. The Belgian/Congo perspective survived because it generalized the *mechanism*; the catalog didn't. **Note:** contradicts CLAUDE.md "every 90s" mandate, but that's Iran-era talking-head; may be format-dependent. Don't refactor CLAUDE.md from n=1.

### Idea 11. Delegated verbatim quotes >30 words may not survive recording?
Tripoli's Crane closing (~20 words) survived. Manhattan's Hitakonanu'laxk steelman (~60 words) got paraphrased to ~25. Maybe break point ≈30 words. n=2 = weak signal. Could try splitting longer source quotes into VO punchline + on-screen full text overlay.

### Idea 12. Mechanism vocabulary keeps appearing on the fly?
User added during Manhattan recording (NOT in script): "complete mechanical failure of legal systems," "tactical engineers of a new civic identity," "mechanism of erasure," "mechanical misunderstandings." Channel DNA is HOW > WHY. Library to keep handy: *mechanical failure, tactical engineers, mechanism of erasure, structural collision, retrofitting, manufactured, fabricated, engineered, projected backward.* If this repeats across 2–3 scripts, worth pre-loading.

### Idea 13. Parallel-structure closings vs layered callbacks?
Manhattan script had sophisticated William Penn + American Legion layered callback (~50 words). User flattened to "In 1626... In 1821... In the centuries since..." (~35 words). Parallel rhythm carries spoken language. But layered callbacks have their own virtues (steelman callback, thesis pivot) — don't blanket-prefer one over the other. Could write both, let the user pick at recording.

---

## Net pattern across all 13

User pulls scripts *toward* artifacts and *away* from rhetorical scaffolding. Causation/mechanism gets richer; performance scaffolding (staccato, meta-tags, vote counts, verbal Chekhov's guns) gets stripped.

Manhattan adds 5 hypotheses to that pattern — none yet promoted to rules. Per memory rule [Rules Hedge, Not Prescribe]: agent-level changes need n≥2 confirmations across different topics before codification. Promote when 2–3 forensic videos in a row show the same cuts/additions; until then, ideas only.

**No script-writer-v2 changes applied. No CLAUDE.md changes applied.**
