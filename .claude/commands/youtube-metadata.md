---
description: Generate optimized YouTube title, description, tags, and timestamps
---

You are generating YouTube metadata for a History vs Hype video.

## Step 1: Read Context FIRST

**BEFORE asking any questions:**

1. **Find the script:**
   ```
   - Use Glob to find script: video-projects/**/SCRIPT.md
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
   - **SEO Keyword Pivoting:** If primary keyword has zero search volume, pivot to related high-volume terms
     - Example: "Crusades fact-check" (0 volume) → "Jerusalem 1099: What Crusaders Really Wrote" (high volume)
     - SEO = searchable keywords (Jerusalem 1099, Crusades history)
     - Positioning = what video actually is (fact-check using primary sources)
     - Put dead keywords in description/tags, not title
   - If VidIQ data available, use their keyword recommendations

2. **Description - CRITICAL STRUCTURE:**

   **First 3 Lines (Frontload Keywords):**
   - Line 1: Primary keyword + video format (fact-check, primary sources, etc.)
   - Line 2: Specific event/topic with keywords (Jerusalem 1099, not just "Crusades")
   - Line 3: Method/sources used with natural keyword integration

   Example opening:
   ```
   A primary-source fact-check of viral claims that the Crusades were "awesome" and purely defensive.
   Using only what crusaders themselves wrote about the 1099 siege of Jerusalem in the First Crusade.
   We read the medieval crusader chronicles (Fulcher of Chartres, Raymond d'Aguilers, Gesta Francorum) to see what really happened.
   ```

   **Rest of Description:**
   - Structured breakdown with timestamps
   - ALL sources cited with specific references
   - Academic sources, primary documents, expert citations
   - Natural language (NOT keyword stuffing)
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

5. **Thumbnail Strategy - VidIQ Requirements:**

   **NOTE: User will use VidIQ for actual thumbnail design. DO NOT waste credits generating thumbnail concepts.**

   **Instead, document what VidIQ needs to suggest a good thumbnail:**

   When user asks about thumbnails, provide this information for VidIQ:

   **Required Information:**
   1. Core topic (specific event/dispute, e.g., "Jerusalem 1099 massacre fact-check")
   2. Video format (Short or longform)
   3. Visual assets available:
      - Maps (which regions/territories)
      - Primary documents (which specific sources)
      - Modern hooks (Pete Hegseth tattoo, viral video screenshot, etc.)
      - Face vs. no face preference
   4. Working title/main keywords
   5. Channel's thumbnail style:
      - Best performers (split-screen, text-heavy, map-focused?)
      - Mobile vs. desktop CTR data
      - Clean documentary vs. YouTube-native look preference
      - Color palette (muted historical vs. high-contrast)

   **Example response format:**
   ```
   For VidIQ thumbnail generation, here's what they need:

   1. Core topic: Fact-checking "Crusades Were Awesome" viral video using crusader chronicles
   2. Format: Longform (10 minutes)
   3. Assets: Medieval manuscripts (Fulcher of Chartres), Jerusalem maps, Pete Hegseth tattoo crop
   4. Keywords: Jerusalem 1099, Crusades history, primary sources
   5. Style: Split-screen format, muted historical colors, bold 2-4 word text, documentary aesthetic
   ```

   **DO NOT generate actual thumbnail mockups or detailed design concepts.**

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
