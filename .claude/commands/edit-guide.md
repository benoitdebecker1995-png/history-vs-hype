---
description: Generate shot-by-shot visual staging guide from A-roll transcript
---

You are creating an editing guide for filmed A-roll footage. Use the **a-roll-editor skill** to generate a comprehensive shot-by-shot breakdown.

## Your Task

1. **Read the script FIRST:** Before doing anything, read the full script (not just SRT) to understand:
   - What claims are being fact-checked
   - What primary sources are cited
   - What the argument structure is

2. **Ask clarifying questions about primary sources:**
   - For EACH document mentioned (telegrams, reports, studies), ask: "What does this document actually record?"
   - For Nazi documents: Ask what specific language/euphemisms are used
   - For historical documents: Ask what the exact context is
   - **NEVER assume you know what a document contains without asking**

3. **Get the transcript:** Confirm location of A-roll transcript file (SRT or plain text with timestamps)

4. **Understand context:** Ask about the video (topic, length, available assets)

5. **Analyze structure:** Read through and identify sections, key moments, primary source citations

6. **Generate guide:** Create timestamp-by-timestamp visual staging suggestions following the format from VANCE_VIDEO_EDITING_GUIDE.md

## Key Principles

- **Verify before you write** - Read the script, ask about primary sources, don't assume
- **Default to host on camera (60-70%)** - Only cut to B-roll when it strengthens argument
- **B-roll = evidence, not decoration** - Maps for geography, documents for sources, graphics for comparisons
- **Every visual must serve the argument** - No generic footage, no filler
- **Context matters for credibility** - Specify what documents actually record (e.g., "deportation trains" vs "death counts")
- **Provide simpler alternatives** - Mark complex visuals as optional with easier options

## CRITICAL: Primary Source Accuracy

When the script cites primary sources (especially for fact-checking videos):
- **Ask what the document actually records** before writing the guide
- Include specific context in text overlays (e.g., "Höfle Telegram = deportation train arrivals")
- Note any euphemisms or coded language (e.g., "Sonderbehandlung/SB = Nazi euphemism for killing")
- For Holocaust/genocide videos: Precision is ESSENTIAL for credibility

## Output Format

Generate editing guide with:
- Shot-by-shot breakdown with timestamps
- Visual type breakdown (talking head %, sources %, maps %, etc.)
- Must-nail delivery moments
- Asset priority list (MUST HAVE vs NICE TO HAVE)
- Production timeline estimate
- Editing checklist

Save to: `video-projects/[topic-slug]/[topic]-EDITING-GUIDE.md`
