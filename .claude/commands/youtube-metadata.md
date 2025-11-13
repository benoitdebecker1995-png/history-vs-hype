---
description: Generate optimized YouTube title, description, tags, and timestamps
---

You are generating YouTube metadata for a History vs Hype video.

## Step 1: Read Context FIRST

**BEFORE asking any questions:**

1. **Find the script:**
   ```
   - Use Glob to find script: video-projects/**/*FINAL-SCRIPT.md
   - Read the script to understand content
   - Extract title, runtime estimate, structure
   ```

2. **Find project location:**
   ```
   - Read video-projects/PROJECT_STATUS.md
   - Identify which project this is for
   - Confirm folder location (usually _READY_TO_FILM/)
   ```

3. **Check for VidIQ data:**
   - If user mentions VidIQ, ask for the analysis
   - VidIQ provides: competitor titles, thumbnail styles, tag recommendations
   - If available, use it to optimize metadata

## Step 2: Generate Metadata

Based on script content, create:

1. **Title Options (3 variations):**
   - 50-60 characters
   - Include main hook/myth
   - Optimize for search (if VidIQ data available, use competitor insights)

2. **Description:**
   - Opening hook (first 125 chars crucial)
   - Structured breakdown with timestamps
   - ALL sources cited with specific references
   - Academic sources, primary documents, expert citations
   - CTA for subscription

3. **Timestamps:**
   - Extract from script structure
   - Clear section names
   - Match actual video flow

4. **Tags (20-30):**
   - Primary (high volume search terms)
   - Secondary (specific discovery)
   - Long-tail (niche)
   - If VidIQ data available, prioritize their recommendations

5. **Thumbnail Strategy:**
   - Based on script hook and evidence
   - If VidIQ data available, reference competitor analysis
   - Specific composition recommendations

## Step 3: Save to Correct Location

**CRITICAL: Check folder structure BEFORE saving**

```
WRONG: video-projects/topic-name/YOUTUBE-METADATA.md
RIGHT: video-projects/_READY_TO_FILM/1-topic-name/YOUTUBE-METADATA.md
```

**Process:**
1. Use Glob to find project folder
2. Verify location (usually _READY_TO_FILM/ or _IN_PRODUCTION/)
3. Save as `YOUTUBE-METADATA.md` in that folder

## User Preferences

- **Be efficient:** Don't ask for script if you can find it with Glob
- **Read first:** Check existing files before asking questions
- **VidIQ integration:** If user provides VidIQ data, use it to optimize
- **Direct approach:** Get to work, minimal questions

## Output Format

Create complete ready-to-use metadata file with all sections above.
