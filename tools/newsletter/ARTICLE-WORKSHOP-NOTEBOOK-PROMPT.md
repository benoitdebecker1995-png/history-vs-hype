# Article Workshop Notebook — Setup Prompt

**Paste this into a new context window to continue building the notebook.**

---

## Context

I created a NotebookLM notebook called **"History vs Hype — Article Workshop"** (ID: `3ccc9c87-3ea7-41c4-9516-718f73a5efd0`). Its purpose is to critique and improve my Substack articles before publishing. It should learn from REAL human writing, not AI-generated text.

## Current State

**Already uploaded (3 sources):**
1. `ARTICLE-WRITING-STYLE-BIBLE.md` — my 30 distilled writing rules (derived from 9 authors + 4 writing craft books)
2. `article-writer.md` — my article-writer agent rules (v5.0, 20 rules in 3 tiers)
3. `STYLE-GUIDE.md` — my video script style guide (overlapping principles adapted for page)

**Still needs uploading:**
4. `.claude/REFERENCE/VOICE-PROFILE.md` — my voice profile (word choice, sentence rhythm, delivery patterns from real speech samples). Upload failed due to MCP disconnect.

## What I Need You To Do

### 1. Upload VOICE-PROFILE.md
Upload `.claude/REFERENCE/VOICE-PROFILE.md` to the notebook. This is critical — it captures how I actually speak, derived from voice samples.

### 2. Suggest and discuss real human-written sources to add

The notebook needs REAL human writing to learn from. NO AI-generated content. The sources should be books, articles, and newsletters written by actual humans that exemplify the techniques I'm trying to master.

**Category A: Writing craft books (the sources my Style Bible was derived from)**

These are the books that informed my rules. Uploading the ACTUAL books lets the notebook check whether my rules accurately captured the techniques, find techniques I missed, and identify rules I may have oversimplified.

| Book | Author | Why |
|------|--------|-----|
| *The Sense of Style* | Steven Pinker | Classic Style, metadiscourse, Curse of Knowledge |
| *On Writing Well* | William Zinsser | Kill zombie nouns, simplify, endings |
| *The Pyramid Principle* | Barbara Minto | SCQA, top-down logic, MECE |
| *Smart Brevity* | Jim VandeHei et al. | Axios visual hierarchy, 26-second rule |

**Category B: The 9 "master authors" my voice is modeled on**

My Style Bible extracted techniques from these authors. Uploading chapters or excerpts lets the notebook compare my actual writing against the originals and catch where I'm imitating poorly or missing something.

| Book | Author | Technique I'm borrowing |
|------|--------|------------------------|
| *Sapiens* | Yuval Noah Harari | Imagined orders, Necker Cube flips, cosmic zoom |
| *Guns, Germs, and Steel* | Jared Diamond | Ultimate causes, pre-emptive ethical strike |
| *A Short History of Nearly Everything* | Bill Bryson | Narrative data, spatial analogies, humor |
| *Debt: The First 5,000 Years* | David Graeber | Moral dissonance, ghost fictions |
| *The Emperor of All Maladies* | Siddhartha Mukherjee | Micro-tragedy, unburdening |
| *The Silk Roads* | Peter Frankopan | Physical artifact anchoring |
| *The Selfish Gene* | Richard Dawkins | Revealing metaphors |
| *Factfulness* | Hans Rosling | Myth-busting, trends vs drama |

**Category C: Successful newsletter/longform writers to study**

These are real humans writing in formats close to what I'm building. Uploading their best pieces would give the notebook examples of what "great" looks like in practice.

Suggestions (discuss which fit best):
- **Heather Cox Richardson** (*Letters from an American*) — history newsletter, massive audience, daily format
- **Matt Lakeman** — long-form country analyses, deep research, engaging prose
- **Erik Hoel** (*The Intrinsic Perspective*) — science/philosophy, strong personal voice
- **Freddie deBoer** — contrarian takes, fierce personal voice
- **Anne Applebaum** (Atlantic) — authoritarianism/history, clear prose
- **Patrick Wyman** (*Perspectives*) — history newsletter, academic rigor + accessibility
- **Bret Devereaux** (*A Collection of Unmitigated Pedantry*) — military/ancient history, pedagogical voice

### 3. CRITICAL CAVEAT: Audit my rules against the real sources

Once the real books are uploaded alongside my rules, I want the notebook to **forensically audit whether my Style Bible, article-writer agent, and style guide are actually correct.** Specific things to check:

1. **Techniques I may have oversimplified** — Did I reduce a nuanced authorial technique to a mechanical rule that misses the point?
2. **Techniques I missed entirely** — What do these authors do that my rules don't capture at all?
3. **Rules that contradict each other** — Are there places where my Style Bible says one thing and my article-writer says another?
4. **Rules that contradict the source material** — Did I misinterpret Pinker, Minto, or Zinsser? Does my "Zero Metadiscourse" rule go further than Pinker actually recommends?
5. **Voice profile vs. rules conflict** — Does my Voice Profile (how I actually speak) conflict with my Style Bible (how I want to write)? Which should win?
6. **Overengineered rules** — Are any rules so specific they constrain more than they help? The article-writer has 20 rules in 3 tiers — is that too many?
7. **Missing from the rotation system** — My ROTATION-STATE.md shows I overuse SCQA openings (5/6), Loop endings (5/6), and "On top of that" transitions (4/6). Are there techniques from the master authors I'm not even tracking?

**Prompt to run after sources are uploaded:**

```
Read all sources in this notebook. Then forensically audit the three rule files (ARTICLE-WRITING-STYLE-BIBLE.md, article-writer.md, STYLE-GUIDE.md) against the actual writing craft books and master author excerpts. For each rule file, answer:

1. Which rules accurately capture what the source authors do?
2. Which rules oversimplify or misrepresent the original technique?
3. Which techniques from the source authors are completely missing from the rules?
4. Where do the three rule files contradict each other?
5. Where does VOICE-PROFILE.md (how I actually speak) conflict with the rules (how I want to write)?
6. Which rules are overengineered — so specific they constrain creativity rather than enabling it?
7. What opening, ending, bridge, or evidence-delivery techniques do these authors use that aren't in my rotation system at all?

Be brutal. I want the problems, not reassurance. Cite specific passages from the source books to support each finding.
```

## My Published Articles (for reference, NOT to upload)

These are AI-assisted, so don't upload them as voice examples. But they show what the rules produce in practice:
- Crusades article (just revised — uses Nicetas hook, Tancred Catch-22, March Pact, Arabic coinage)
- 5 prior articles tracked in `tools/newsletter/ROTATION-STATE.md`

## What I Already Have in Another Notebook

"The Mind's Eye: A Guide to Twenty-First Century Style" (25 sources) — this is my existing style reference notebook. It likely already has the Pinker, Zinsser, Minto, and Axios books. I may want to consolidate rather than duplicate. Check what's in there first before re-uploading.
