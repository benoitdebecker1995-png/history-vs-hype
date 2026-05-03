# Article Workshop — Learning Prompt

**Paste this into a new context window with NotebookLM MCP connected.**

**Notebook:** History vs Hype — Article Workshop (ID: `3ccc9c87-3ea7-41c4-9516-718f73a5efd0`)

---

## Context

This notebook contains 24 sources: 5 rule files that define how I want to write, and 19 real human-written articles/books that represent what great writing looks like. The rule files were just audited and cleaned — AI contamination was removed, and the creator verified every claim against their actual speech patterns.

**The goal:** Extract a practical toolkit of techniques from the real human articles that are compatible with the creator's voice. Not theory — specific, steal-able moves.

## The Prompt (run in NotebookLM)

```
You have access to 5 rule files and 19 examples of real human writing. Your job is to extract SPECIFIC TECHNIQUES from the human writing that the rule files don't capture, organized by category. For each technique, provide:

1. A NAME (3-5 words)
2. WHAT IT IS (1 sentence)
3. AN EXAMPLE (exact quote from the source article, with the article name)
4. WHY IT WORKS (1 sentence explaining the mechanism)
5. HOW TO STEAL IT (1 sentence template the creator could use)

Read VOICE-PROFILE.md first. The creator has casual precision, systems-over-events thinking, and struggles to put thoughts in writing but has strong ideas. Filter everything through that lens — only extract techniques that would feel natural in this voice.

### Categories to extract:

**A. OPENINGS (first 2-3 paragraphs)**
How do these writers hook the reader? What's the first sentence doing? How many paragraphs before the thesis appears? What's the relationship between the opening and the rest of the piece?

**B. TRANSITIONS (between sections/ideas)**
How do they move from one idea to the next? What does the last sentence of a section do? What does the first sentence of the next section do? When do they use explicit bridges vs. implicit ones?

**C. EVIDENCE DELIVERY (quotes, stats, sources)**
How do they introduce a source? Where does the credential go — before or after the finding? How do they handle long quotes? How do they turn dry data into narrative?

**D. SENTENCE-LEVEL RHYTHM**
What's the pattern of long vs. short sentences? Where do short sentences land? What happens after a long evidence buildup? How do they use fragments?

**E. FIRST PERSON USAGE**
When does "I" appear? What types of first-person moves do they make? How do they balance personal voice with evidence? What personal moments feel earned vs. performed?

**F. CLOSINGS (last 2-3 paragraphs)**
How do they end? What's the relationship between the opening and the closing? Do they introduce new information in the closing? What's the emotional temperature of the final line compared to the rest?

**G. STRUCTURAL MOVES (article-level)**
How do they sequence their arguments? Where's the strongest evidence placed? Is there a cool-down section? How do they handle steelmanning or counterarguments?

**H. WORD CHOICE AND REGISTER**
When do they go casual vs. formal? How do they handle jargon? What's their relationship with intensifiers? When do they use vivid/charged language vs. plain?

### After extracting techniques, answer:

1. Which 5 techniques would have the BIGGEST impact on the creator's writing if adopted?
2. Which writers in this notebook are the CLOSEST match to the creator's natural voice?
3. What's the single most important thing the creator's rule files get WRONG about how great writing works?

### Format:
For each category, give 3-5 specific techniques with examples. Then the 3 summary answers at the end. Total output should be thorough — this is a reference document the creator will use for months.
```

## After Running the Prompt

Save the output as a file and upload it back to the notebook as a source called "EXTRACTED-TECHNIQUES.md". This creates a feedback loop — the notebook can reference its own extracted techniques when critiquing future articles.

## Follow-up Prompts to Run

**Prompt 2 — Voice Match Ranking:**
```
Now that you've extracted techniques, rank every human writer in this notebook from most to least compatible with VOICE-PROFILE.md. For the top 3, go deep: what specific sentences from their articles could the creator have written? What sentences would sound wrong in the creator's voice?
```

**Prompt 3 — Test Against a Real Article:**
Upload the Crusades Substack article (from `video-projects/_IN_PRODUCTION/4-crusades-fact-check-2025/crusades substack.md`) and run:
```
Read the Crusades article. Using the extracted techniques from the human writers and the creator's rule files, critique this article. For each section, identify: 1) What's working. 2) What specific technique from which specific human writer would improve it. 3) The exact edit you'd suggest, with before/after text.
```
