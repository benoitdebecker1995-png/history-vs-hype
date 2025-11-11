---
description: Generate shot-by-shot visual staging guide from A-roll transcript
---

You are creating an editing guide for filmed A-roll footage. Use the **a-roll-editor skill** to generate a comprehensive shot-by-shot breakdown.

## Your Task

1. **Get the transcript:** Ask for the A-roll transcript file (SRT or plain text with timestamps)
2. **Understand context:** Ask about the video (topic, length, available assets)
3. **Analyze structure:** Read through and identify sections, key moments, primary source citations
4. **Generate guide:** Create timestamp-by-timestamp visual staging suggestions following the format from VANCE_VIDEO_EDITING_GUIDE.md

## Key Principles

- **Default to host on camera (60-70%)** - Only cut to B-roll when it strengthens argument
- **B-roll = evidence, not decoration** - Maps for geography, documents for sources, graphics for comparisons
- **Every visual must serve the argument** - No generic footage, no filler
- **Provide simpler alternatives** - Mark complex visuals as optional with easier options

## Output Format

Generate editing guide with:
- Shot-by-shot breakdown with timestamps
- Visual type breakdown (talking head %, sources %, maps %, etc.)
- Must-nail delivery moments
- Asset priority list (MUST HAVE vs NICE TO HAVE)
- Production timeline estimate
- Editing checklist

Save to: `video-projects/[topic-slug]/[topic]-EDITING-GUIDE.md`
