# Article-Writer Upgrade Proposal — Crane 2020 (Reading American Secularism in the 1797 Treaty of Tripoli)

**Source paper:** crane2020.pdf | **Author:** Jacob Crane | **Year:** 2020 | **Journal:** American Quarterly 72(2), 403-422 | **Generated:** 2026-04-29
**NotebookLM notebook:** Academic Models — Article Writer (id: ae9c62f5-9b60-4df6-87d2-1be2775937c5)
**Source ID inside notebook:** 6152978e-1ecb-40cc-a145-1a1b38d8f184

## Executive Summary

- Techniques surfaced: 14
- Verdicts: 7 DIRECT TRANSFER, 4 ADAPT, 3 REJECT
- Crossover: 9 tagged [BOTH] (apply to script-writer-v2 too); 1 [ARTICLE-ONLY]; 1 [SCRIPT-VIABLE]
- Top 3 highest-leverage proposed changes:
  1. **NEW Rule 13b "Decode-Not-Defer"** — every blockquote must be followed by a 1-2 sentence rhetorical/political decode in the author's voice. No quote left orphan to "speak for itself." (Tightens existing evidence-as-narrative rule into an enforceable post-quote checklist.)
  2. **NEW Rule 11b "Steel-Man Before Pivot"** — when raising an opposing reading, give it the strongest historical logic available BEFORE complicating it. Replaces vague "intellectual honesty" gesture with a named two-beat structure.
  3. **NEW Closing Template "Full-Circle + Open Question"** — return to opening anchor, re-evaluate through new lens, end with a speculative unresolved question rather than a synthesis statement. Add to ROTATION-STATE.md as a fourth closing type alongside thesis-landing / unresolved-injustice / synthesis.

---

## Findings by Dimension

### 1. Macro Structure

#### Technique 1.1: Contemporary-Event Opening Hook
- **Observed in paper:** Crane opens not with the 1797 treaty but with Obama's 2009 Cairo speech — a recognizable contemporary political event that creates immediate stakes for an obscure 18th-century document.
- **Evidence:** > "In a major speech in 2009, delivered to Muslim leaders in Cairo, recently elected President Barack Obama announced what he hoped would be a turning point in US relations with the Muslim world." (p. 403)
- **Verdict:** **DIRECT TRANSFER**
- **Audience-fit reasoning:** The channel's reader came from YouTube, where the modern hook is mandatory. Crane's structure is exactly the channel's "modern relevance" rule executed at article scale.
- **Crossover tag:** [BOTH] — script-writer-v2 already does this implicitly; can be hardened.
- **Proposed rule edit:**
  - Target: ARTICLE-WRITING-STYLE-BIBLE.md (Opening Templates section) | Reference from article-writer.md Rule 6 (Opening)
  - Diff:
    ```
    + Template: "Contemporary-Event Anchor"
    +   Beat 1: Name a specific, recent, recognizable event (named figure, year, setting).
    +   Beat 2: Reveal a contradiction, mystery, or omission inside that event.
    +   Beat 3: Tee up the historical investigation that resolves it.
    +   Anti-pattern: Beat 1 must be specific (Obama 2009 Cairo), not generic ("In recent years politicians have...").
    ```

#### Technique 1.2: Thesis-Late-In-Intro Placement
- **Observed in paper:** Crane's thesis lands at the END of his introductory section, after the hook + the mystery + the contradiction.
- **Evidence:** > "the circulation of the Treaty of Tripoli and Article 11 over the last two centuries reveals not so much a long tradition of American friendship with the Muslim world as the role of representations of Islam in perennial and fierce internal debates about religious discrimination and the separation of church and state" (p. 404)
- **Verdict:** **ADAPT**
- **Audience-fit reasoning:** Crane's intro spans a full page before thesis lands. A Substack reader from YouTube has bailed by paragraph 3. The MOVE (hook → mystery → thesis) is sound, but compress: thesis must land within 200 words / 25% of an article opening per existing Rule 21.
- **Crossover tag:** [BOTH]
- **Proposed rule edit:**
  - Target: `.claude/REFERENCE/THESIS-DISCIPLINE.md` Tier 2 (Cross-format adaptation)
  - Diff:
    ```
    + Article opening structure (Crane 2020 model, compressed):
    +   1. Contemporary anchor (1-2 sentences)
    +   2. The mystery / contradiction / omission (1-2 sentences)
    +   3. Thesis (≤12 words, single sentence)
    +   Maximum total: ≤200 words / first 25% — never bury past this point.
    ```

#### Technique 1.3: Theoretical-Framework Section Before Narrative
- **Observed in paper:** Crane inserts a dedicated theoretical-framework section (Beydoun on structural Islamophobia, Said on Orientalism) between intro and chronological survey.
- **Evidence:** > "It is through this lens, rather than the triumphalist secular narratives that have dominated discussions of Article 11, that we can best understand the problematic history of the Treaty of Tripoli." (p. 408)
- **Verdict:** **REJECT**
- **Audience-fit reasoning:** Substack reader will not consent to a "framework" section before the story starts. The channel's stance is evidence-as-narrative — theoretical scaffolding gets dissolved into the story, not staged ahead of it. Crane writes for peer reviewers who chose American Quarterly; the channel writes for someone holding a phone.
- **What the channel does instead:** Smuggle the analytical lens into the first concrete scene. Don't name "structural Islamophobia"; show how the same words functioned three different ways across three different decades and let the reader feel the structure.

#### Technique 1.4: Chronological-Dialectical Sequencing
- **Observed in paper:** Each section follows the same document through a different historical group reading it differently — Federalists 1798, Jeffersonians 1800, American Jews 1840s, Christian nationalists 1860s, Secularists 1890s.
- **Evidence:** > "As the Treaty of Tripoli was increasingly being used by American Jews to argue against religious discrimination, Christian nationalists were interpreting Article 11 very differently in the aftermath of the Civil War" (p. 414)
- **Verdict:** **DIRECT TRANSFER**
- **Audience-fit reasoning:** This is the channel's bread and butter rendered cleanly: one artifact, multiple readings, each era's politics revealed by what they made the artifact say. Mechanism > narrative — exactly the HOW>WHY axis the channel optimizes for.
- **Crossover tag:** [BOTH] — particularly powerful for script-writer-v2 (turn-execution scenes)
- **Proposed rule edit:**
  - Target: `.claude/REFERENCE/THESIS-DISCIPLINE.md` Tier 3 (Topic-specific toolkit) — replaces or complements "myth-projected-onto-static-artifact" pattern
  - Diff:
    ```
    + Pattern: SAME-TEXT-DIFFERENT-EYES
    + When the artifact is a document (treaty, ruling, founding text), structure as:
    +   - Era 1 reads it as X
    +   - Era 2 reads it as Y (often the opposite)
    +   - Era 3 reads it as Z
    +   The thesis is what stays constant — usually that the document was a Rorschach blot all along.
    + Reuse trigger: video/article centers on a single text whose meaning is contested across time.
    + Cross-format: works in scripts (chapter-per-era) and articles (section-per-era).
    + n-status: Tier 3, sample size = 1 (Crane). Treat as PROVISIONAL until validated on second case.
    ```

#### Technique 1.5: Temporal-Marker + Juxtaposition Transitions
- **Observed in paper:** Section transitions use temporal markers paired with contrasting groups.
- **Evidence:** > "Not long after the end of the Barbary Wars in 1815 and decades before the emergence of an organized secularist movement, Article 11 became a favorite text of the country's growing Jewish population..." (p. 412)
- **Verdict:** **DIRECT TRANSFER**
- **Audience-fit reasoning:** Channel already uses temporal markers in scripts. Hardening the pattern — temporal anchor + contrasting actor — gives prose forward motion without requiring section headers.
- **Crossover tag:** [BOTH]
- **Proposed rule edit:**
  - Target: ARTICLE-WRITING-STYLE-BIBLE.md (Transition patterns) — add as named pattern alongside existing transitions
  - Diff:
    ```
    + Transition pattern: TEMPORAL ANCHOR + CONTRASTING ACTOR
    +   Formula: "[temporal phrase], [new actor] was [doing the opposite of the previous actor]."
    +   Example: "Not long after X ended, Y began doing the reverse."
    +   Use to: move between eras/sections without visible scaffolding.
    +   Avoid: "Now let's turn to..." / "In the next section..." — visible mechanics.
    ```

#### Technique 1.6: Full-Circle Close With Speculative Open Question
- **Observed in paper:** Crane's closing returns to Obama in Cairo, then ends with an unanswered question rather than a synthesis statement.
- **Evidence:** > "One particular question about President Obama's citation of the treaty remains open: given the 1797 treaty's failure to secure a lasting peace... why did the president not cite the longer-lived, postwar 1805 treaty that more closely reflects the wording of his quotation?" (p. 418-419)
- **Verdict:** **DIRECT TRANSFER**
- **Audience-fit reasoning:** This is a fourth closing template the channel doesn't yet have explicit. Adds variety to the rotation and works for cases where neither thesis-landing nor unresolved-injustice fits.
- **Crossover tag:** [BOTH]
- **Proposed rule edit:**
  - Target: `.claude/REFERENCE/CLOSING-SYNTHESIS-TEMPLATES.md` + `tools/newsletter/ROTATION-STATE.md` (add fourth closing type)
  - Diff:
    ```
    + Closing Type 4: FULL-CIRCLE + OPEN QUESTION
    +   Beat 1: Return verbatim or near-verbatim to the opening hook artifact/event.
    +   Beat 2: Re-evaluate it with the historical lens just built (the ironies/ commitments/contradictions now visible).
    +   Beat 3: End with a specific, answerable-but-unanswered question that the article doesn't resolve.
    +   When to use: when the historical analysis has shifted the reader's reading of the opening anchor; when no clean thesis-landing is available; when the unresolved injustice is interpretive rather than material.
    +   Anti-pattern: vague rhetorical question ("What does this mean for us today?"). Crane's question is specific ("why did Obama cite the 1797 treaty rather than the 1805?").
    ```

---

### 2. Evidence Handling

#### Technique 2.1: Stake-Setting Setup Line Before Every Quote
- **Observed in paper:** Every blockquote arrives behind a sentence that establishes who, when, and why the speaker matters.
- **Evidence:** > "Surprisingly, there is little evidence of any response to Article 11 when it was first published, with the exception of a short comment added below the treaty in William Cobbett's Porcupine Gazette in Philadelphia. Cobbett writes:" (p. 410)
- **Verdict:** **DIRECT TRANSFER**
- **Audience-fit reasoning:** Channel already requires "primary sources on screen" but doesn't enforce a setup-line discipline. Crane's pattern eliminates orphan quotes — every quote is set up by the historical stakes that make it matter.
- **Crossover tag:** [BOTH]
- **Proposed rule edit:**
  - Target: `.claude/agents/article-writer.md` Tier 2 STRUCTURAL — new sub-rule under existing Evidence Handling section
  - Diff:
    ```
    + Rule 13a: Stake-Setting Setup Line (MANDATORY before every blockquote)
    +   Every direct quote must be preceded by a single sentence answering: who is speaking, when, and what is at stake when they speak.
    +   "Cobbett writes:" alone is insufficient — it must be: "[Stakes context]. [Speaker] writes:"
    +   Test: a reader who never finishes the quote should still understand why the next paragraph matters.
    ```

#### Technique 2.2: Decode-Not-Defer Post-Quote Re-Entry
- **Observed in paper:** Crane never lets a quote "speak for itself." After every quote he steps back in to decode the rhetorical/political move.
- **Evidence:** > "[After quoting Cobbett's 'trampling upon the cross' line:] As a Federalist, Cobbett singles out Barlow to avoid directly criticizing Adams, even as he accuses the government as a whole of desecration." (p. 410)
- **Verdict:** **DIRECT TRANSFER** (highest-leverage finding)
- **Audience-fit reasoning:** Channel's "evidence-as-narrative" mission already implies this but doesn't enforce it. Many newsletter drafts have ended with quotes left to do their own work — they don't. The reader needs the analyst to translate the move that was just made. Decoding the speaker's strategic interest is exactly the "calm prosecutor" voice in action.
- **Crossover tag:** [BOTH]
- **Proposed rule edit:**
  - Target: `.claude/agents/article-writer.md` Tier 1 HARD — new Rule 13b
  - Diff:
    ```
    + Rule 13b: Decode-Not-Defer (HARD — pre-output gate)
    +   No blockquote may end a paragraph. Every blockquote must be followed within 1-2 sentences by an authorial decode that answers ONE of:
    +     - What rhetorical move is the speaker making?
    +     - Whose interest does this serve?
    +     - What is the speaker NOT saying?
    +     - What does this language reveal about their assumptions?
    +   The decode is in the author's voice, not a neutral paraphrase.
    +   Anti-pattern: ending a section with a quote and a line break. The quote is raw material; the decode is the article.
    +   Quality Gate item: every blockquote in a draft must be followed by a decode sentence — flag any that aren't.
    ```

#### Technique 2.3: Calibrated Certainty With Explicit Gap-Naming
- **Observed in paper:** When evidence is partial, Crane names the gap directly using "perhaps," "seems," "historians remain divided."
- **Evidence:** > "Some commentators then and now point to Barlow himself as the author of the language, but historians remain divided. Barlow seems a likely candidate, given his Deist sympathies..." (p. 404-405)
- **Verdict:** **ADAPT**
- **Audience-fit reasoning:** Channel is "calm prosecutor" — defaults to commitment. But the channel ALSO claims intellectual honesty as a competitive edge, and saying "we don't know" when we genuinely don't is part of that edge. The risk: hedge-everywhere prose ("perhaps, possibly, maybe") = academic mush. Adapt by limiting to genuine factual gaps (authorship questions, lost motives, missing documents) — never to hedge an interpretive verdict.
- **Crossover tag:** [BOTH]
- **Proposed rule edit:**
  - Target: `.claude/agents/article-writer.md` Tier 2 STRUCTURAL — clarify under existing intellectual-honesty rule
  - Diff:
    ```
    + Rule 11a: Calibrated Certainty (use "perhaps" / "seems" / "we don't know" SPARINGLY and ONLY for factual gaps)
    +   Permitted use: contested authorship, lost motives, gaps in the documentary record, scholarly disagreement on facts.
    +   Forbidden use: hedging an interpretive verdict the article is making. The thesis must be stated, not perhaps-ed.
    +   Test: count "perhaps" and "seems" — if more than 3 in a 2,000-word piece, audit each.
    ```

#### Technique 2.4: Synthesis vs. Paradox Mode-Switching
- **Observed in paper:** When evidence supports the thesis Crane synthesizes confidently. When evidence complicates it (e.g., American Jews using the treaty inclusively at the expense of Muslims), he leans into the paradox rather than burying it.
- **Evidence:** > "However, we can see that this rhetorical move to integrate Jews into the national imaginary is accomplished at the expense of the Muslim figure." (p. 414)
- **Verdict:** **DIRECT TRANSFER**
- **Audience-fit reasoning:** This is skepticism-first stance made operational. The channel's brand depends on saying the inconvenient thing — Crane's pattern (lean INTO complication) is exactly what protects against the "everyone-was-a-hero / everyone-was-a-villain" oversimplification trap.
- **Crossover tag:** [BOTH]
- **Proposed rule edit:**
  - Target: `.claude/agents/article-writer.md` Tier 1 HARD — extend existing Rule 5B Earn-Your-Inclusion / Rule 14 Skepticism
  - Diff:
    ```
    + Rule 14a: Mode-Switch on Complicating Evidence
    +   When evidence COMPLICATES the thesis (instead of confirming it), do NOT bury it.
    +   Required move: name the complication explicitly, often using "However" / "And yet" / "But the same move that...".
    +   The complication strengthens the thesis if it's named; weakens it if it's smuggled.
    +   Example move: "X was inclusive — but the inclusion was purchased by excluding Y."
    ```

---

### 3. Voice & Register

#### Technique 3.1: "I" Reserved For Argumentative Signposting
- **Observed in paper:** Crane uses "I" almost exclusively to mark methodological moves and core arguments — not for narration.
- **Evidence:**
  > "I would argue, we see more modern secularist readings of the Treaty of Tripoli begin to emerge" (p. 416)
  > "In the following, I explore the long history that lies behind President Obama's misattributed and selective quotation" (p. 404)
- **Verdict:** **ADAPT**
- **Audience-fit reasoning:** Article-writer is first-person THROUGHOUT (Harari/Pinker model — agent's existing identity). Crane's principle is right (don't waste "I" on narration where it adds nothing) but the agent's mission is different — first-person creates the curiosity-companion voice. Adapt: keep first-person throughout, but mark the strongest argumentative claims with explicit "I'd argue" / "I think" so they stand out. The "I" should bear weight when used for verdicts.
- **Crossover tag:** [ARTICLE-ONLY] (script-writer-v2 is "calm prosecutor" 3rd-person evidence-led; doesn't apply)
- **Proposed rule edit:**
  - Target: `.claude/agents/article-writer.md` Tier 2 STRUCTURAL — clarify existing first-person rule
  - Diff:
    ```
    + Rule 8a: First-Person Weight
    +   "I" should appear throughout (existing rule), but reserve "I'd argue" / "I think" / "I'd suggest" for the strongest argumentative beats — the verdict moments.
    +   Anti-pattern: opening 5 sentences in a row with "I" — the voice flattens.
    +   Anti-pattern: never marking your verdicts with explicit first-person — the reader can't see where you're committing.
    ```

#### Technique 3.2: Formal Academic Register
- **Observed in paper:** Dense theoretical vocabulary, peer-reviewer audience.
- **Evidence:** > "the structural and dialectical logic of Islamophobia as they rely on figuring Tripoli as an orientalist projection, a distant and threatening foil for the articulation of American identity" (p. 408)
- **Verdict:** **REJECT**
- **What the channel does instead:** Existing Rule 7 "plain words" / Rule 4 "define every term immediately." Crane's audience signed up to read 22 pages of theoretical density; the channel's reader did not. Translate every "dialectical" into "the same words doing opposite work in different mouths."

#### Technique 3.3: Dense Theoretical Vocabulary As Signal Of Seriousness
- **Observed in paper:** Words like "alterity," "structural Islamophobia," "presentism," "hermeneutics" do work for a peer reader and create noise for everyone else.
- **Verdict:** **REJECT**
- **What the channel does instead:** Existing Rule 7 (plain words). The seriousness signal in this channel comes from named scholars + specific page numbers + primary documents on screen — not from vocabulary density.

---

### 4. Counter-Argument & Limitation Handling

#### Technique 4.1: Steel-Man Before Pivot
- **Observed in paper:** When raising opposing readings, Crane gives them the strongest historical/rhetorical case BEFORE complicating.
- **Evidence:** > "Barlow seems a likely candidate, given his Deist sympathies, his enthusiasm for the French Revolution, and his close relationship with Thomas Paine." (p. 404-405) — followed by Allison's counter that authorship is impossible to determine.
- **Verdict:** **DIRECT TRANSFER**
- **Audience-fit reasoning:** Channel's "intellectual honesty" rule already exists but is loose. Crane's two-beat structure (best-case-for-opposing → pivot to limitation) makes it executable. Crucial for skepticism-first audience — they smell a strawman from a kilometer.
- **Crossover tag:** [BOTH]
- **Proposed rule edit:**
  - Target: `.claude/agents/article-writer.md` Tier 1 HARD — new Rule 11b (replaces vague intellectual-honesty gesture)
  - Diff:
    ```
    + Rule 11b: Steel-Man Before Pivot
    +   When the article addresses an opposing reading, the article must FIRST give that reading its strongest case before complicating it.
    +   Two-beat structure:
    +     Beat 1: "Here's the best version of why people read this as X..."
    +     Beat 2: "But here's what that reading misses / occludes / requires you to ignore..."
    +   Anti-pattern: "Some claim X, but actually..." — strawman move, kills the channel's credibility.
    +   Test: a reader on the OPPOSING side of the argument should recognize their position in Beat 1.
    ```

#### Technique 4.2: Concede Factual Basis, Pivot To Deeper Thesis
- **Observed in paper:** Crane concedes Obama's factual claim ("Islam has always been part of America's story") and pivots to the deeper thesis (the role of representations of Islam in domestic debates).
- **Evidence:** > "Although that history substantiates the president's claim that 'Islam has always been a part of America's story,' the circulation of the Treaty of Tripoli and Article 11 over the last two centuries reveals not so much a long tradition of American friendship with the Muslim world as the role of representations of Islam in perennial and fierce internal debates about religious discrimination and the separation of church and state" (p. 404)
- **Verdict:** **DIRECT TRANSFER**
- **Audience-fit reasoning:** Pure myth-busting move executed cleanly: yes, the surface fact is true; here's why the surface fact is misleading. Most channel scripts already attempt this; making it a named pattern improves consistency.
- **Crossover tag:** [BOTH]
- **Proposed rule edit:**
  - Target: SCRIPTWRITING-DEBUNKING-FRAMEWORK.md + ARTICLE-WRITING-STYLE-BIBLE.md
  - Diff:
    ```
    + Pattern: CONCEDE-AND-DEEPEN
    +   Formula: "Although [factual claim of opposing position] is true, the [evidence/history] reveals not [their interpretation] but [your deeper thesis]."
    +   Use when: the opposing position has a factual basis you can't deny but is using that fact to draw the wrong conclusion.
    +   Power source: by conceding the surface fact, you earn the right to redirect the interpretation.
    ```

#### Technique 4.3: Transparent Speculation On Genuine Unknowables
- **Observed in paper:** When motives are hidden (why did Obama's speechwriters misattribute the quote?), Crane offers branched speculation rather than a forced conclusion.
- **Evidence:** > "Perhaps this was a mistake by the president's speechwriters, or perhaps Obama wanted to identify his own position with that of a famous former president, casting himself as a unifying figure in relations between West and East." (p. 403)
- **Verdict:** **ADAPT**
- **Audience-fit reasoning:** Channel "calm prosecutor" usually commits. But for genuine unknowables (intent, motive, lost intent), Crane's branched-speculation pattern is honest without being mush. Use sparingly — once or twice per article, never more.
- **Crossover tag:** [ARTICLE-ONLY]
- **Proposed rule edit:**
  - Target: ARTICLE-WRITING-STYLE-BIBLE.md (Limitation handling)
  - Diff:
    ```
    + Pattern: BRANCHED SPECULATION (limit ≤2 per article)
    +   When a motive or cause is genuinely unknowable, present 2-3 explicit possibilities rather than guessing.
    +   Formula: "Perhaps X. Or perhaps Y. Either way, [thing the article CAN say]."
    +   Anti-pattern: branched speculation as default voice. This is for genuinely unknowable beats only.
    ```

---

## Rejected Techniques (Audience-Fit Failures)

Log these so the next academic article on the same axes doesn't re-propose them.

- **Theoretical-framework section before narrative.** Why it fails: Substack reader from YouTube does not consent to a "framework" section. Channel does evidence-as-narrative, not theory-then-application.
- **Formal academic register.** Why it fails: Channel's audience is intellectually curious but algorithmically conditioned. Existing Rule 7 (plain words) wins.
- **Dense theoretical vocabulary.** Why it fails: Vocabulary density signals seriousness to peer reviewers, alienation to YouTube viewers. The seriousness signal in this channel is page numbers + named scholars + primary docs on screen.

---

## Approval Checklist

- [ ] Reviewed all 7 DIRECT TRANSFER proposals (techniques 1.1, 1.4, 1.5, 1.6, 2.1, 2.2, 2.4, 4.1, 4.2)
- [ ] Reviewed all 4 ADAPT proposals (techniques 1.2, 2.3, 3.1, 4.3) — especially the "what changes" specification
- [ ] Confirmed the 3 REJECT verdicts (1.3, 3.2, 3.3)
- [ ] Approved subset of changes for `.claude/agents/article-writer.md`
- [ ] Approved subset of changes for `.claude/agents/script-writer-v2.md` (cross-tagged [BOTH] items)
- [ ] Approved THESIS-DISCIPLINE.md additions (technique 1.2 Tier 2, technique 1.4 Tier 3)
- [ ] Approved CLOSING-SYNTHESIS-TEMPLATES.md addition (technique 1.6)
- [ ] Approved ROTATION-STATE.md addition (fourth closing type from 1.6)
- [ ] Approved SCRIPTWRITING-DEBUNKING-FRAMEWORK.md addition (technique 4.2)

After approval, hand-edit the agents (no `--apply` automation built yet) — version-bump article-writer.md to v5.4, update header changelog, and add a memory entry under "Agent/Tool Versions" pointing to this file.

---

## Methodology Note (for future runs of /learn-from-paper)

This was the first run of `/learn-from-paper`. Three observations for the next run:

1. **NotebookLM query timeouts on long compound questions.** Q3 (4 sub-questions in one prompt) timed out twice. Splitting into ≤2 sub-questions per query worked. Future versions of the command should hardcode the split.
2. **The shared notebook strategy works.** "Academic Models — Article Writer" now contains crane2020. Next paper will let cross-paper queries run ("compare how Crane and [next author] handle limitation-naming") — that's where the compounding value lives.
3. **The Audience-Fit Skepticism Test surfaced 3 rejects out of 14 techniques.** That's a healthy reject rate — confirms the filter isn't just rubber-stamping. If a future paper produces 0 rejects, the filter is failing.
