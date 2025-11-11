# Claude Code Setup for History vs Hype

This directory contains custom skills and slash commands to help with YouTube video production.

## Quick Start

### Complete Workflow

**`/create-video`** - Full research-to-script pipeline
- Stage 1: Find trending topics (web + VidIQ)
- Stage 2: Deep preliminary research (free sources)
- Stage 3: Recommend authoritative sources to purchase
- Stage 4: Generate custom NotebookLM prompts
- Stage 5: Write script from NotebookLM output
- Creates organized project directory with all outputs
- Pauses between stages for your input

### Individual Stage Commands

**`/find-topic`** - Research trending topics only
- Web trend analysis (border disputes, political claims, historical myths)
- VidIQ CoachPro integration
- Top 3 recommendations with viral potential scores

**`/deep-research`** - Comprehensive preliminary analysis
- Uses only free sources (Wikipedia, archives, Google Scholar)
- Extracts smoking gun evidence with URLs
- Identifies patterns (3+ interconnected incidents)
- Modern relevance examples (2024-2025)
- YES/MAYBE/NO verdict on topic viability

**`/suggest-sources`** - Recommend books and articles to buy
- 20-30 authoritative sources (up to 50 if essential)
- Prioritizes "standard works" (cited 100+ times)
- Cost research (ebook, used, library)
- Acquisition priority and NotebookLM upload strategy

**`/notebooklm-prompts`** - Generate custom research prompts
- 6-8 fully customized prompts for your specific topic
- Evidence extraction, pattern recognition, counter-arguments
- Copy-paste ready for NotebookLM
- Optimized for citation extraction

**`/script`** - Generate video script
- Works with NotebookLM output or other research
- Proven Vance/Essequibo formula
- Includes fact-check priorities and B-roll requirements
- Flags inconsistencies needing verification

**`/fact-check`** - Verify all script claims
- Extracts statistics, quotes, historical events
- Organizes by evidence tier (1-3)
- Checks source hierarchy
- Pre-filming approval checklist

## Skills Available

### Research & Analysis Skills

**`topic-finder`** - Analyzes web trends and VidIQ data to find viral topics

**`deep-researcher`** - Conducts comprehensive preliminary research using free sources

**`source-recommender`** - Identifies authoritative academic sources worth purchasing

**`notebooklm-prompt-generator`** - Creates custom NotebookLM prompts for specific topics

### Production Skills

**`script-generator`** - Proven formula from Vance/Essequibo top performers

**`documentary-editing-guide`** - Shot-by-shot editing with hybrid talking-head strategy

## How to Use

### For New Videos (Complete Workflow)
**`/create-video`** - Does everything from topic research to script

### For Specific Stages
1. **Finding topics?** → `/find-topic`
2. **Have a topic, need research?** → `/deep-research`
3. **Research done, need sources?** → `/suggest-sources`
4. **Sources ready, need NotebookLM prompts?** → `/notebooklm-prompts`
5. **Have NotebookLM output, need script?** → `/script`
6. **Script done, need verification?** → `/fact-check`

## Project Directory Structure

When you run `/create-video`, it creates:

```
video-projects/
└── [topic-name]-[date]/
    ├── 01-trend-research.md (topics + VidIQ data)
    ├── 02-preliminary-research.md (deep analysis from free sources)
    ├── 03-source-recommendations.md (books/articles to buy)
    ├── 04-notebooklm-prompts.md (custom prompts)
    ├── 05-notebooklm-output.md (your responses)
    └── 06-script-draft.md (final script)
```

Everything organized in one place, easy to reference.

## File Organization

```
.claude/
├── README.md (this file)
├── SKILL.md (skill format documentation)
├── commands/
│   ├── create-video.md (master workflow)
│   ├── find-topic.md (trend research)
│   ├── deep-research.md (preliminary analysis)
│   ├── suggest-sources.md (source recommendations)
│   ├── notebooklm-prompts.md (prompt generation)
│   ├── script.md (script generation)
│   ├── fact-check.md (verification)
│   └── new-video.md (legacy - use create-video instead)
└── skills/
    ├── topic-finder.md (trend analysis engine)
    ├── deep-researcher.md (free source research)
    ├── source-recommender.md (academic source finder)
    ├── notebooklm-prompt-generator.md (custom prompts)
    ├── script-generator.md (proven formula)
    └── documentary-editing-guide.md (visual strategy)
```

## Channel Philosophy

These tools enforce the core principles:
1. **Historical integrity above all** - Every claim verified
2. **Evidence over opinion** - Show primary sources
3. **Modern relevance** - Connect history to 2025
4. **Academic balance** - Present multiple perspectives
5. **No oversimplification** - Maintain nuance

## Proven Formula Highlights

Based on your best-performing videos (Vance Part 2: 1.4K views, Essequibo):

**Opening Pattern:**
- Concrete action/number in first sentence
- Visual elements immediately clear
- Stakes obvious within 8 seconds
- Specificity: "114 nautical miles" not "over 100 miles"

**Structure:**
- Cold open (0:00-0:15): Immediate drama
- Setup & stakes (0:15-1:00): Modern hook, why it matters NOW
- Pattern reveal (1:00-10:00): Minimum 3 interconnected claims
- Synthesis (10:00-11:30): Why this matters in 2025
- CTA (11:30-12:00): Sources in description, subscribe

**Language:**
- Investigation framing: "So I went to the Vatican archives..."
- Precision: Named individuals, exact numbers, specific documents
- Academic tone: "Evidence suggests..." not political framing
- Pause cues: "[PAUSE - let that sink in]"

**Visuals:**
- 60-70% talking head (making arguments)
- 30-40% B-roll (maps 15-20%, primary sources 10-15%)
- B-roll is EVIDENCE, not decoration
- Mark every visual: **[DOCUMENT: Papal bull Dum Diversas]**

## Performance Stats

Target metrics based on current performance:
- **Average view duration:** 41.5% (excellent for 8-12 min educational)
- **Target length:** 8-12 minutes
- **Pacing:** 100-110 words per minute
- **Engagement trigger:** Every 2 minutes

## Recommended Workflow

### Option 1: Full Pipeline (When Exploring)
```
/create-video
→ Guides through all 5 stages
→ Creates organized project directory
→ Pauses for your input between stages
```

### Option 2: Jump to Specific Stage (When You Know What You Need)
```
Have a topic? → /deep-research
Have research? → /suggest-sources
Have sources? → /notebooklm-prompts
Have NotebookLM output? → /script
Have script? → /fact-check
```

### Option 3: Quick Script (Legacy Workflow)
```
/script
→ If you have research ready and just need the script
```

## Next Steps

1. Try `/create-video` to start your next project with full workflow
2. Or jump straight to `/find-topic` to research trending topics
3. Review `guides/History-vs-Hype_Master-Project-Template.md` for methodology
4. Check `guides/HYBRID_TALKING_HEAD_GUIDE.md` for visual strategy

## Support

These tools are designed to maintain quality while increasing efficiency. They enforce fact-checking protocols and proven formulas, but your editorial judgment always takes priority.

**Quality over quantity, always.**
