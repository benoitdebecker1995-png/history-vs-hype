---
description: Generate a video script using the proven History vs Hype formula (based on successful Vance and Essequibo videos)
---

You are helping create a video script for the History vs Hype YouTube channel using the proven formula from top-performing videos.

## Your Task

1. **First, gather information:**
   - What's the topic/myth you want to debunk?
   - What's the modern hook? (Current event, political claim, recent news)
   - Do you have NotebookLM output to work from? (If yes, ask them to paste it)
   - If no NotebookLM output: Do you have other research ready? (Preliminary research, sources, documents)
   - Target length? (Default: 9-11 minutes - VidIQ data shows this performs best)
   - Any specific "smoking gun" evidence? (Key documents, statistics, quotes)

2. **If NotebookLM output provided:**
   - Save it to: `video-projects/[topic-slug]/05-notebooklm-output.md`
   - Cross-check claims against any preliminary research available
   - Flag any inconsistencies or claims needing extra verification

3. **Then use the script-generator skill** by reading and following: `.claude/skills/script-generator.md`

4. **Generate a complete script** following the proven structure:
   - IMMEDIATE DRAMA in first 8 seconds (concrete action, specific numbers)
   - STRONGEST EVIDENCE by 0:45 (CRITICAL: viewers drop at 1:11, so payoff must come early)
   - PATTERN REVELATION (minimum 3 interconnected claims)
   - PRIMARY SOURCES marked with visual cues
   - MODERN STAKES clear by 2:00 mark
   - Precise language (no vague "many" or "some")
   - Investigation framing ("So I went to the archives...")

5. **Include at the end:**
   - Fact-check priority list (Tier 1-3 evidence)
   - B-roll requirements (Critical/Important/Nice-to-have)
   - Visual planning (document reveals, maps, timelines)
   - Quality control checklist

## Key Principles

Follow the channel's proven formula:
- **Hook in 8 seconds:** "On March 1st, 2025, a Venezuelan warship—armed with a 76-millimeter cannon—penetrated over 100 nautical miles..."
- **Payoff-first structure:** Show modern consequences BEFORE historical causes
- **Named specifics:** "Second Lieutenant Ansel Murray" not "a soldier"
- **Precision:** "114 nautical miles" not "over 100 miles"
- **Primary sources on screen:** Mark every document with **[DOCUMENT: Mirari Vos Section 14]**
- **Academic framing:** Evidence-based, not political

## After Generation

Ask the user:
1. Does this opening grab you in 8 seconds?
2. Do you have the primary sources marked here?
3. Should I expand any section?
4. Want me to generate the YouTube description and tags?
5. Ready for fact-checking?

Remember: This channel prioritizes **historical integrity, evidence over opinion, and modern relevance**. Every claim needs sources. Every script gets fact-checked.

## Output Location

Save completed script to: `video-projects/[topic-slug]/06-script-draft.md`

Or if not part of a project: `scripts/[topic-name]-script.md`
