---
name: Newsletter Rules
description: Newsletter article writing — failure modes from script conversion, author voice patterns, model author techniques
type: feedback
---

## Script-to-Article Conversion Failures (from: feedback_article-writing-v1.md)

### The Core Problem
Video scripts converted to articles read like "scripts with B-ROLL tags stripped out." Performance hides lack of connective tissue. The article-writer agent v1.0 produced this exact failure.

**Why:** The agent rules focused on WHAT to remove (tags, timestamps) but not HOW to rebuild for written medium. Written articles need connective tissue, narrative arcs, and evidence-as-story that video gets for free from visuals.

**How to apply:** Every future article conversion must be checked against these 7 failure modes before output.

---

### Failure Mode 1: Teleprompter Phrasing (Pinker's metadiscourse warning)
Phrases that work as presenter pivots but bog down written prose:
- "Here's the part usually left out of the story" — reader assumes you're providing new info; don't announce it
- "But watch what happens when you test the data" — direct instruction to a viewer
- "The question isn't what happened. It's how." — presenter's bridge; reader can see the question if you orient their gaze
- "But this wasn't about land. The number — 370 leagues — was about wind." — dramatic pause for camera stare

**Rule:** Cut ALL signposting. If you name what you're about to do, you've failed.

### Failure Mode 2: Video Jump Cuts Instead of Written Flow
Subheadings doing the work of a "cut to black" rather than logic bridging sections. Articles need "arcs of coherence" — the reader must know WHY you're moving to the next topic.

**Rule:** Every section transition needs a connective sentence explaining how A leads to B. Howes uses the *problem* of navigation to naturally introduce the Casa de Contratacion as a *solution*. Mirror this: problem → solution arcs, not topic → topic jumps.

### Failure Mode 3: Visual Dependence (Missing B-Roll)
Paragraphs that rely on the reader having a virtual display:
- "Open a language map of South America" — zombie instruction without visual
- Physical descriptions that are camera close-ups without intellectual connection

**Rule:** Describe the SHAPE of what the reader would see, as Howes describes France being "thinner than everyone supposed." Don't instruct; paint.

### Failure Mode 4: Evidence as Textbook Entry Instead of Narrative
- Volta do Mar explained like a geography lesson → needs a terrified navigator
- Romanus Pontifex presented as date + pope + block quote → needs the Pope as character issuing a corporate charter for slavery
- Laudares study presented as methodology → "Gini point has no emotional weight"
- Franchise model explained in abstract business terms → needs Coelho liquidating his life

**Rules (from model authors):**
- Pinker: If you name the researcher, you've failed. Data speaks for itself.
- Howes: If a paragraph explains a "system," rewrite it to follow a man trying to survive that system.
- Bryson: If you use a decimal point, follow it with a hammer blow under 5 words.
- Graeber: Treat institutions as characters with moral contradictions.

### Failure Mode 5: Rhythm Flatlines
3+ consecutive sentences of similar length = "narrative hum." Verdict sentences carrying zombie nouns instead of landing as hammers.

**Rules:**
- Verdict sentences must be under 8 words (ideally under 5)
- After every evidence build, collapse to a punch: "The map was a chokehold." "He was blind." "The ink was enough."
- Never 5 sentences of same length in a row
- The 1514 merchant newsletter passage ("Brazilwood below deck. Human beings above.") is the gold standard — replicate this rhythm

### Failure Mode 6: TED Talk Endings
Jumping from specific evidence (Brazilian census data) to speculative futures (moon bases, asteroid mining) = rhetorical whiplash. Unearned escalation.

**Rules:**
- Stay at the crime scene. The evidence is the verdict.
- Circle back to the opening (Graeber returns to Henry Ford)
- Or end with a scholarly gap (Howes ends with what's missing from the record)
- Or end with the micro-tragedy character (Ribeiro on the beach = the system made human)
- NEVER trade precise lethality of data for speculative fluff

### Failure Mode 7: Em Dashes
User flagged that em dashes are perceived as a sign of AI writing. NotebookLM validation confirmed.

**Rule:** NEVER use em dashes in article prose. Replace with commas, periods, colons, or parentheses. Only exception: blockquote attributions ("> — Author").

---

### The Reframe Test
"Most readers assume _____, but the evidence shows _____."
If you can't fill the first blank with a REAL belief readers hold, the reframe isn't working.

**Weak:** "Unmeasurable lines create measurable inequality" (observation, not inversion)
**Strong:** "Most readers assume empires require precise maps to function, but the most successful colonial border in history was drawn by men who admitted they were blind."
**Strong:** "Most readers assume the Treaty of Tordesillas was a calculated division of new continents, but the evidence shows it was a desperate attempt to catch a specific wind."

---

### Model Author Techniques (Calibrated Against Examples)

| Author | Technique | Application |
|--------|-----------|-------------|
| Graeber | Reframe Detonator — invalidate something the reader owns (their bank account, their map) | Openings, reframes |
| Howes | Contextual Zooming — start from the average person's ignorance, build mechanistically | Section pacing, transitions |
| Howes | Mechanistic Pacing — patient, expansive sentences walking through a system | Mid-article evidence |
| Bryson | Narrative Data Transformation — never raw numbers without a human-scale metaphor | Statistics, studies |
| Pinker | Anti-metadiscourse — never tell the reader what you're doing | Every sentence |
| Mukherjee | Micro-Tragedy — one real person representing a system | Openings, closings |
| Rosling | Data Confrontation — confront reader with a number that proves them wrong | Openings |

---

### Structural Frameworks (Minto, Zinsser, Pinker, Axios, Perell)

**Minto Pyramid — Top-Down Structure**
- Problem: Draft follows research journey (bottom-up). Reader has to "scrabble about" to find significance.
- Rule: Present the verdict BEFORE the evidence. State the 10% poverty gap (effect) before the 370-league line (cause).
- SCQA Opening Framework:
  - **Situation:** Non-controversial anchor ("In 1494, Spain and Portugal signed a treaty to divide the world.")
  - **Complication:** Tension that triggers reader's question ("The men who drew it couldn't measure it.")
  - **Question:** Core question explicitly ("How does an unmeasurable line still govern Brazilian bank accounts?")
  - **Answer:** Top point / verdict immediately

**Zinsser — Kill Zombie Nouns**
- "The implementation of the treaty" → "The kings struggled to draw the line"
- Active verbs ALWAYS. Every passive "is/was" → active verb with a human actor.
- Strip qualifiers: "a bit," "sort of," "rather," "in a sense" — prosecutor doesn't say evidence is "a bit conclusive"

**Axios Smart Brevity — Core 4**
1. Muscular tease: Subject line ≤6 words
2. One strong lede: First sentence tells reader something they don't know
3. Axiom: Bold **Why it matters:** or **By the numbers:** for skimmers
4. Go deeper: Historical nuance AFTER the decision point to continue
- Sub-sections under 200 words. Bullet data points, don't blob them.
- Readers spend average 26 seconds on a story. Visual hierarchy traps the skimmer's eye.

**Perell POP — Optimize for Surprise**
- CRIBS audit: mark every passage as Confusing, Repetitive, Interesting, Boring, or Surprising
- Double down on Surprising, delete Boring
- Trust primary sources — "children above deck, brazilwood below" needs no feature-style tricks
- "If this is the ONLY thing the reader sees, is it exactly what I want to stick?"

**Three Grounded Endings (Kill the Moon Leap)**
1. Scrivener's Loop (Graeber): Return to Toledo. "The ink was enough."
2. Ribeiro Verdict (Mukherjee/Bryson): "We no longer leave convicts on the beach, but we are still living in the architecture they were left to build. The line is still there."
3. Ghost Software Gap (Howes/Harari): "The question is whether we can ever uninstall it."

---

### Example Articles for Calibration
Saved at: `video-projects/_IN_PRODUCTION/41-treaty-tordesillas-2026/_research/examples/`
1. Howes — The House of Trade (navigation, maps, institutional mechanism)
2. Howes — The Forgotten Golden Age (primary sources, comparative, reframe ending)
3. Graeber — Money Is Just an IOU (reframe detonator, verdict sentences, circular ending)
4. Howes — The Real Roaring Twenties (named individuals, evidence-as-story)

---

## Author Voice v3.0 — Interview Findings (from: feedback_article-voice-v3.md)

Article-writer v3.0 rebuilt from author voice interview (2026-03-28) + Harari/Pinker NotebookLM analysis.

**Core identity:** Scholar who writes clearly. Not a journalist, not a content creator. Harari/Pinker model: academic authority delivered accessibly.

**Key patterns from interview:**
- Enters topics through related precedents ("did you know X works the same way?"), never definitions
- Skepticism before excitement: verifies before celebrating a finding
- Instinct is "that's incomplete" not "that's wrong" (complexifier, not debunker)
- Teacher's instinct: "if you remember only one thing..."
- Plain words over academic words: "solidified" not "ossified"
- Transitions: "on top of that," "at the same time," "this brings us to"
- Limitations stated honestly: "we have to keep in mind," "history is never 100%"
- Controversial claims attributed: "one side claims..." not stated as author's fact
- Writes formal then loosens (academic rigor first, accessibility second)
- Hates: opinions disguised as facts, no limitation disclosure, oversimplification
- Overused phrases: "like," "you know," "btw"

**Reading between the lines:**
- Thinks in patterns across centuries, not timelines
- Joy comes from learning, not from having content
- Connects abstract history to physical experience (places visited, documents read, comment sections)
- The "I knew X, but Y" pattern is his signature: setup assumption, pivot, land on what changed
- Needs AI to write at higher technical level than he can on first draft, but with HIS sensibility

**Anti-patterns (things v2.0 did wrong):**
- Dramatic mic drops ("He was blind.") — replace with observations/facts
- Extended metaphors stacked together — cap at 2-3, each must explain not decorate
- [PERSONAL] markers creating two distinct voices — weave first person throughout
- Academic vocabulary where plain words work — translate down without simplifying argument
- Never acknowledging limitations — always include at least one

**Why:** v2.0 Tordesillas article had detectable voice-shift between AI prose and author additions. Author's rough personal additions carried more authenticity than polished AI sections. The gap isn't quality, it's that AI sections feel performed and author sections feel lived.

**How to apply:** Read article-writer v3.0 agent (Rules 13-19) and ARTICLE-WRITING-STYLE-BIBLE.md (Author's Voice section) before any article work.
