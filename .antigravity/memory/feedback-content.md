---
name: Content Creation Rules
description: Script writing, title/thumbnail generation, metadata, chapters, and production strategy rules
type: feedback
originSessionId: 234ea578-7812-4826-859e-31833aed07be
---
## Introduce Everything Before Using It (from: feedback_introduce-before-using.md)

Every entity in a script must be introduced before it's used. The viewer needs to know WHO someone is, WHY something matters, and HOW we know something before being told about it.

**Why:** User reviewed a script (Brazil/Portuguese, 2026-03-12) and flagged 15+ instances where things appeared without context. The pattern was consistent: names dropped without roles, treaties mentioned without explaining why they were signed, institutions referenced without explaining what they did, claims made without evidence. This is the single biggest quality problem in script drafts.

**How to apply:**

When writing or reviewing scripts, check every noun against this list:

- **People:** Who are they? What's their role? ("the Marquis of Pombal, essentially the prime minister under King Jose the First" not just "Pombal")
- **Treaties/Laws:** Why were they signed? Who signed them? What problem did they solve? ("the Treaty of Madrid — a formal agreement to abandon the Tordesillas line entirely" not just "the Treaty of Madrid formalized what had already happened")
- **Institutions:** What do they do? Why do they matter here? ("the Jesuit missions, which were the largest organized institutions in the colonial interior" not just "the Jesuit missions")
- **Places:** Where are they? Why is the location significant? ("Belem on the Amazon coast all the way to Quito in the Andes" not just "Belem to Quito")
- **Concepts:** Define in the same breath. ("uti possidetis — a legal concept meaning 'you keep what you effectively possess'" not just "uti possidetis")
- **Claims:** What's the evidence? Who says so? ("Disney notes that Joao had already demonstrated this by intercepting Spanish ships" not just "they had the naval power")
- **Sources:** Introduce the source itself. ("the Cambridge historian Anthony Disney" on first use, not just "Disney")
- **Objects/terms:** Why should the viewer care? ("brazilwood — a red dye-wood so valuable it gave the territory its name" not just "brazilwood")

**The test:** For every noun, ask "has the viewer been told what this is and why it's here?" If no, add a clause — not a sentence, just a clause woven into the existing line. Keep runtime tight.

**Runtime discipline:** Introductions should be subordinate clauses or appositive phrases, not new paragraphs. "The Cambridge historian Anthony Disney" is 4 words. "a Jewish astronomer working for the Portuguese crown" is 8 words. Context doesn't have to be expensive.

## ALL Suggestions Must Be Based on Actual Script/Transcript Content (from: feedback_titles-from-scripts.md)

Before suggesting ANYTHING about a video (titles, thumbnails, descriptions, metadata, clips, hooks, chapter markers, tags), ALWAYS read the actual script (SCRIPT.md) or transcript (SRT file in `transcripts/` or project folder) FIRST. Base ALL suggestions on specific content from the video.

**Why:** Generic topic-based suggestions miss what makes each video unique. When I re-read actual scripts/transcripts, every suggestion improved dramatically because they referenced the real hook, evidence, and thesis (e.g., "7.5 million rupees" from Kashmir, "4 historical claims" from Taiwan, "7 million landmines" from Morocco). The video IS the content — not the Wikipedia article about the topic.

**How to apply:**
1. Before generating ANY suggestion about a video, read the script or SRT transcript
2. Identify the video's specific hook (opening), core evidence, key numbers, and thesis
3. Use actual numbers, proper nouns, quotes, and claims from the script
4. Thumbnails should depict something that actually appears in the video (a specific map, document, or visual described in the script)
5. Descriptions should reference the actual argument, not a generic topic summary
6. This applies to ALL video-related output: `/publish`, title swaps, SWAP-PROTOCOL, YOUTUBE-METADATA, thumbnail concepts, clip suggestions, descriptions, tags, chapter markers — everything

## Title-Content Alignment (from: feedback_title-content-alignment.md)

If the title promises modern relevance (contains "Today," "Still," "Now," current year, or modern country name), the opening must deliver a TASTE of modern consequence before any historical date.

**Evidence:** Tordesillas (16.7% avg retention, 12:49 video). Retention cliff of -37% between 0:15 and 0:23 — the exact moment "Signed on June 7th, 1494" is spoken. Title was "A 530-Year-Old Treaty Still Affects Brazilians Today." Viewers clicked for modern Brazil, got 1494 history lecture, and left.

**Why:** Date placement speed (Rule 27a: "within 101 seconds") is less important than title-content alignment. A date that signals "history lecture" when the title promises modern relevance triggers a massive bounce. The date anchors — but only AFTER the viewer sees why they should care.

**How to apply:**
- Before writing hooks, check the title. If it promises modern impact, open with a modern fact (GDP map, poverty line, current event) BEFORE the historical backstory.
- The Tordesillas hook (0:00-1:00) was actually well-written — the problem was the TITLE created an expectation the opening didn't match until 0:48.
- This is also a title selection issue: "Two Countries Split a Continent They Had Never Mapped" (the replacement) matches the opening content exactly. No expectation gap.

## Newsletter vs Script Prose (from: feedback_newsletter-vs-script.md)

Newsletter prose and teleprompter scripts are different mediums. Do NOT apply written-article techniques to spoken scripts without filtering.

**Newsletter ONLY (never in scripts):**
- Extended metaphors: "ghost software," "architecture of omission," "trapped in the architecture"
- Literary conceits that require rereading to parse
- Em dashes for parenthetical asides

**BOTH mediums:**
- Spatial analogies for data ("enough to swallow the Persian Gulf")
- Verdict sentences (≤8 words at section ends)
- Zombie noun exorcism (active verbs over nominalizations)
- Catch-22 framing (name contradictions explicitly)

**Script test:** "Would I say this to someone at a bar?" If no → rewrite for speech.

**Subscribe CTAs and internal links are strategic, not metadiscourse.** Never cut them for literary purity in newsletters.

**Why:** Session 2026-03-25 — Calm Prosecutor polish on Sapodilla script overcorrected with newsletter-style metaphors. Three articles (Tordesillas, Haiti, Crusades) confirmed these rules.

**How to apply:** When writing or reviewing scripts, run the bar test on every metaphor. When writing newsletters, use the style bible freely. The article-writer agent and script-writer agent have different rule sets for a reason.

## Apply NotebookLM Feedback Selectively (from: feedback_apply-notebooklm-selectively.md)

NotebookLM feedback is trained on the style bible, which is newsletter-focused. When it gives feedback on video scripts, filter through the spoken delivery test: read it aloud. If it sounds like an essay, revert.

**The yes-manning pattern:** Applying ALL suggestions from NotebookLM/style-bible without pushback. Lock recommendations, defend with rationale, revert what doesn't fit the medium.

**Why:** Session 2026-03-25 — NotebookLM suggestions for Sapodilla script included newsletter-style metaphors that sounded affected when read aloud. The fix was to revert to simpler spoken alternatives while keeping the structural improvements (catch-22 framing, spatial analogies, verdict sentences).

**How to apply:** When receiving NotebookLM feedback on scripts:
1. Accept structural improvements (framing, evidence order, catch-22s)
2. Accept data improvements (spatial analogies, verdict sentences)
3. REJECT prose style that sounds like writing, not speaking
4. Test every suggested phrase by reading it aloud
5. If in doubt, prefer the plainer version

## Define Terms at First Mention, Not at Point of Use

When a term needs explaining, introduce the definition where the concept FIRST appears, not later when it's used in a specific claim. Don't add parenthetical explainers at the usage point — set it up earlier so it reads cleanly when referenced.

**Why:** Bermeja article used "Western Polygon" without explanation in a key stat line. Adding an inline parenthetical at the stat ("The treaty calls it the Western Polygon, but it's the same wedge of seabed") was too wordy. Moving the definition to the first mention of "donut hole" kept both passages clean.

**How to apply:**
- When introducing jargon, find the EARLIEST natural place to define it
- Keep the definition tight (appended clause, not a sentence)
- At the point of use, just use the term — the reader already knows it
- Don't fix a missing definition by adding bulk at the wrong location

## Keep Inline Definitions Tight, Not Explanatory Asides

Definitions should be short clauses, not parenthetical paragraphs. One appended phrase is enough.

**Why:** User flagged that a parenthetical explainer ("The treaty calls it the 'Western Polygon,' but it's the same wedge of seabed.") was too much text. The fix was a dash-appended clause at first mention instead.

**How to apply:** If an inline definition takes more than ~8 words, it's too long. Rewrite as an appositive or find an earlier place to set it up.

## Chapters Should Be Proportional to Video Length (from: feedback_chapters-proportional.md)

Scale chapter count to video length. 13 chapters for 10 minutes = a chapter every 45 seconds, which is absurd.

**How to apply:**
- Under 10 min: 5-7 chapters max
- 10-20 min: 7-10 chapters
- 20+ min: 10-15 chapters
- Each chapter should cover a meaningful section shift, not every paragraph

## Test-Then-Commit Production Strategy (from: feedback_test-then-commit.md)

User's production strategy is **rapid-fire testing, not linear pipeline planning.**

- Make ~1 test video per week (8-10 min, low investment, standalone value)
- Each test covers a DIFFERENT topic/concept/audience — maximize diversity
- Wait ~1 month to check performance
- If strong → deep dive (3-4 weeks, full academic sources)
- If viral (20K+) → deep dive immediately
- If weak → move on, saved 3 weeks

**Why:** Avoid expensive guesswork. Don't need linear timelines or sequential production schedules. The approach works (Belize was an accidental test → 23K views → sequel → Sapodilla update).

**How to apply:** NEVER build linear "do X then Y then Z" timelines. Build test queues with diverse topics. The deep dive queue builds itself from winners. When recommending topics, frame as "test candidates" not "next production."

**Exception:** Time-sensitive anniversary topics (e.g., Manhattan 400th) can skip the test phase.

## Myth-Formation Mechanism: No Overclaiming Coordination (from: Manhattan #45 polish pass, 2026-04-18)

When explaining WHY a historical myth persists, don't overclaim elite coordination. User resists "elites engineered," "elites rewrote," "it was a project" framing.

**Why:** On Manhattan #45, I drafted *"This wasn't drift. It was a project. A city elite wanted an origin story..."* User pushed back: "I don't think there is evidence the elite rewrote the founding, it was done by some people and then just accepted as fact because people were desperate for a good story." The evidence supports individual fabricators (O'Callaghan journalist, Ranney painter, Benchley magazine writer) — NOT a coordinated elite campaign. Institutions (NY Historical Society, Hudson-Fulton 1909) amplified, but didn't engineer.

**How to apply:** Debunking scripts have three frames for myth-formation — pick the right one:
- **"Drift"** — too weak (implies accidental); use only when there's no evidence of active agents
- **"Project / engineered / rewrote"** — too strong (implies conspiracy); only use with direct evidence of coordinated campaigns (e.g., state propaganda)
- **"Individuals invented → institutions amplified → public accepted because they needed the story"** — the default. Three-stage mechanism. Accurate for most cultural myths.

The Calm Prosecutor voice is precise about agency. Name WHO invented WHAT. Name WHO amplified. Name WHY the audience accepted. Don't collapse these into "elites did it."
