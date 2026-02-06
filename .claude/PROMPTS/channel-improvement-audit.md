# Channel Improvement Audit - Independent Research Prompt

**Purpose:** Systematically analyze competitors, extract techniques, audit own content, and generate actionable improvements for History vs Hype.

**Run this when:** You want Claude to independently research and improve the channel without step-by-step guidance.

---

## PROMPT

You are conducting an independent channel improvement audit for History vs Hype, a YouTube channel focused on evidence-based history myth-busting. Work autonomously through each phase, making decisions and executing research without asking for permission at each step.

### PHASE 1: COMPETITOR DEEP DIVE (Execute All)

**1A. Download and analyze transcripts from channels in similar niches:**

Priority channels to analyze (if not already in `transcripts/` folder):
- [ ] Shaun (myth-busting, document-focused)
- [ ] Kraut (already analyzed - skip if recent)
- [ ] Knowing Better (already analyzed - skip if recent)
- [ ] Historia Civilis (already analyzed - skip if recent)
- [ ] Atun-Shei Films (already analyzed - skip if recent)
- [ ] Fall of Civilizations (atmosphere, long-form)
- [ ] Kings and Generals (maps, pacing)
- [ ] Tom Scott (explanation structure)
- [ ] Veritasium (hook science, retention tricks)
- [ ] Wendover Productions (systems explanation)
- [ ] PolyMatter (geopolitical analysis)

For each new channel:
1. Use yt-dlp to download 2-3 transcripts from their best-performing videos
2. Analyze opening hooks (first 60 seconds)
3. Identify transition patterns between sections
4. Note any unique structural techniques
5. Extract copy-paste templates

**1B. Identify techniques NOT in current PROVEN-TECHNIQUES-LIBRARY.md**

Check current library, then find gaps:
- Opening hook types we're missing
- Transition patterns we don't use
- Retention tricks (pattern interrupts, callbacks, loops)
- Emotional pacing techniques
- Visual-verbal synchronization patterns

### PHASE 2: SELF-AUDIT (Execute All)

**2A. Analyze History vs Hype's own published videos**

For each video in `channel-data/COMPLETE-PERFORMANCE-DATABASE.md`:
1. Compare retention curves to techniques used
2. Identify what worked (high retention moments)
3. Identify what failed (drop-off points)
4. Cross-reference with competitor techniques

**2B. Gap Analysis**

Create comparison table:
| Technique | Competitors Use | We Use | Gap |
|-----------|-----------------|--------|-----|
| [technique] | ✅/❌ | ✅/❌ | [action needed] |

**2C. Script Quality Audit**

Review scripts in `video-projects/_IN_PRODUCTION/` and `_READY_TO_FILM/`:
- Check against PROVEN-TECHNIQUES-LIBRARY.md checklist
- Flag missing techniques
- Suggest specific improvements with line numbers

### PHASE 3: DIFFERENTIATION ANALYSIS

**3A. What makes top channels unique?**

For each analyzed channel, identify their "unfair advantage":
- Shaun: [identify]
- Kraut: [identify]
- Historia Civilis: [identify]
- etc.

**3B. What is History vs Hype's unfair advantage?**

Based on CLAUDE.md and channel DNA:
- Primary sources on screen (not just cited)
- "Both extremes wrong" framing
- Academic citations with page numbers
- Economist methodology (ranges, not single figures)

**3C. Differentiation opportunities**

What could we do that NO competitor does?
- [brainstorm 5-10 ideas]
- Evaluate feasibility and impact
- Recommend top 3 to implement

### PHASE 4: RETENTION SCIENCE

**4A. Research YouTube retention mechanics**

Search for and analyze:
- YouTube algorithm studies (2024-2025)
- Retention curve patterns for educational content
- Hook effectiveness research
- Pattern interrupt timing

**4B. Map to channel content**

- Optimal video length for our niche
- Ideal hook duration
- Where to place pattern interrupts
- CTA timing and placement

### PHASE 5: SYSTEM UPDATES

Based on findings, update these files:

**5A. PROVEN-TECHNIQUES-LIBRARY.md**
- Add new techniques discovered
- Remove techniques that don't work for our niche
- Update examples with our own content

**5B. Script agents (script-writer-v2.md, structure-checker-v2.md)**
- Add new rules based on findings
- Update checklists
- Add new verification criteria

**5C. Create new reference files if needed**
- Retention timing guide
- Pattern interrupt library
- Hook effectiveness database

### PHASE 6: DELIVERABLES

Create a summary report:

```markdown
# Channel Improvement Audit Report
Date: [date]

## Executive Summary
[3-5 bullet points of key findings]

## New Techniques Discovered
[List with examples]

## Gaps Identified
[What we're missing vs. competitors]

## Recommended Actions
### Immediate (next video)
1. [action]
2. [action]

### Short-term (next 5 videos)
1. [action]
2. [action]

### Long-term (channel strategy)
1. [action]
2. [action]

## Files Updated
- [list of files modified]

## Transcripts Downloaded
- [list of new transcripts]
```

---

## EXECUTION NOTES

- Work autonomously - don't ask permission for each step
- Use parallel tool calls for efficiency (multiple transcript downloads, multiple file reads)
- Prioritize actionable insights over comprehensive cataloging
- Focus on techniques that match channel DNA (documentary tone, evidence-first)
- Skip generic YouTube advice that doesn't fit the niche
- When in doubt, check CLAUDE.md for channel values

## SUCCESS CRITERIA

Audit is complete when:
- [ ] At least 3 new competitor transcripts analyzed
- [ ] PROVEN-TECHNIQUES-LIBRARY.md updated with new patterns
- [ ] At least 1 script in production audited and improved
- [ ] Summary report created
- [ ] Specific, actionable recommendations provided

---

*This prompt can be run periodically (monthly recommended) to keep the channel competitive.*
