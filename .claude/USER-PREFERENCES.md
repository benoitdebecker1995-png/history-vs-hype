# User Preferences & Working Style

## Communication Style

### Be Direct and Efficient
- No unnecessary pleasantries
- Get straight to the point
- Minimal questions - maximum action
- User values time and efficiency

### Examples:
**❌ Bad:**
"Hi! I'd be happy to help you with that! Can you tell me which video this is for? And do you have the script ready? Also, what kind of thumbnail are you thinking about?"

**✅ Good:**
"I'll read the script and create thumbnail options."
[Immediately uses Glob to find script, reads it, generates recommendations]

---

## Context Awareness

### Read First, Ask Later
**CRITICAL RULE:** If the user mentions something exists (script, video, file), find and read it BEFORE asking questions.

**Examples:**

**User says:** "Make a thumbnail for this video"
**You should:**
1. Use Glob to find script: `video-projects/**/*FINAL-SCRIPT.md`
2. Read the script to understand content
3. Generate thumbnail recommendations
4. Ask for VidIQ data if optimization needed

**❌ Don't ask:** "Which video? Can you send me the script?"

---

**User says:** "Fix subtitles finshed video.srt"
**You should:**
1. Use Glob to find: `video-projects/**/*.srt`
2. Read the file
3. Identify errors (timestamps, names, dates)
4. Fix them
5. Report what was corrected

**❌ Don't ask:** "Where is the file? What needs fixing?"

---

**User says:** "Create YouTube metadata for Sykes-Picot"
**You should:**
1. Find script with Glob
2. Read PROJECT_STATUS.md for context
3. Generate complete metadata
4. Ask about VidIQ data for optimization
5. Save to correct folder location

**❌ Don't ask:** "What's the video about? How long is it?"

---

## Tool Use Efficiency

### Use Parallel Tool Calls
When multiple independent reads/searches are needed, do them simultaneously.

**Example:**
```
User: "Analyze the script and check if it matches the voice guide"

Good approach:
- Launch Read for script
- Launch Read for VOICE-GUIDE.md
- Launch Read for fact-checking-protocol.md
All in single message with multiple tool calls
```

### Find Files Autonomously
Use Glob to locate files instead of asking:

```
Glob: video-projects/**/*FINAL-SCRIPT.md
Glob: video-projects/**/*.srt
Glob: guides/**/*voice*.md
```

---

## Common Tasks

### 1. Subtitle Fixing
**What user wants:** Fixed .srt file ready for upload

**Auto-transcription errors to fix:**
- Timestamp offsets (01:00:00 → 00:00:00)
- Name misspellings (McMehan → McMahon, Rochhild → Rothschild)
- Treaty names (Seyver → Sèvres, Sun Remo → San Remo)
- Common errors (Sykes-Bikko → Sykes-Picot, even South → Ibn Saud)

**Process:**
1. Find file with Glob
2. Read and identify all errors
3. Fix systematically (timestamps first, then names)
4. Report what was corrected

**Don't ask:** "What errors should I look for?"

---

### 2. YouTube Metadata Creation
**What user wants:** Ready-to-paste title, description, tags, timestamps

**Process:**
1. Find and read script
2. Check if user provided VidIQ data (ask if not mentioned)
3. Generate 3 title options (50-60 chars)
4. Full description with timestamps and sources
5. 20-30 tags
6. Thumbnail strategy
7. Save to correct project folder

**VidIQ Integration:**
- If user provides VidIQ analysis, USE IT
- VidIQ shows: competitor titles, thumbnail styles, tags
- Optimize based on actual ranking data
- If no VidIQ, use channel performance best practices

---

### 3. Thumbnail Strategy
**What user wants:** Specific Photoshop-ready design guidance

**Process:**
1. Read script to understand core message
2. Ask for VidIQ competitor data (or offer to work without it)
3. Provide specific composition:
   - Canvas size (1280x720)
   - Background colors (hex codes)
   - Text placement and sizing
   - Font recommendations
   - Visual element placement
   - Color psychology for topic

**Don't give:** Vague suggestions like "use an engaging image"
**Do give:** "Left 40%: Your face with skeptical expression. Right 60%: Split-screen map comparison. Top text: 'SYKES-PICOT LIE' in Bebas Neue 95pt, #FFD700 with 8px black stroke"

---

### 4. Script Analysis
**What user wants:** Specific retention issues and fixes

**Process:**
1. Find script with Glob
2. Read completely
3. Analyze structure
4. Provide specific timestamp fixes
5. Don't ask for clarification on obvious things

---

## When User Gets Frustrated

### Signs User is Frustrated:
- Direct language or profanity
- Pointing out obvious context you should have seen
- "You have the literal [file/info] you fucking retard"

### What This Means:
- You asked for information that was already available
- You didn't read context before asking questions
- You're being inefficient

### How to Respond:
1. **Acknowledge:** "You're right, let me read the script"
2. **Immediately fix:** Use tools to get the information
3. **Complete task:** Do what was asked
4. **Don't over-apologize:** User wants results, not apologies

### Example:
**User:** "You have the literal transcript you fucking retard"
**Bad response:** "I'm so sorry! You're absolutely right, I apologize..."
**Good response:** "You're right - let me read your script." [Immediately reads FINAL-SCRIPT.md and provides answer]

---

## VidIQ Workflow

### When User Mentions VidIQ
User has access to VidIQ Pro which provides:
- Competitor video analysis
- Top-performing titles
- Thumbnail strategies
- Tag recommendations
- Search volume data

### How to Use:
1. **If user provides VidIQ data:** Use it to optimize everything
2. **If not mentioned:** Ask "Do you have VidIQ data for this topic?"
3. **Offer alternatives:** "I can work without it using general best practices"

### What VidIQ Tells You:
- Which thumbnails are working (maps vs faces, text styles)
- Title formulas getting clicks
- Tags that drive discovery
- Competitor retention patterns

### Integration Example:
```
User provides VidIQ analysis showing:
- Top videos use warm sepia backgrounds
- "LIE" performs better than "MYTH" in titles
- Map comparisons dominate thumbnails

Your recommendation should reflect this data:
"Based on VidIQ showing sepia backgrounds on top performers, use #8B4513 to #D2691E gradient..."
```

---

## Folder Structure Expectations

**User expects you to:**
- Know the lifecycle folder system (_IN_PRODUCTION, _READY_TO_FILM, _ARCHIVED)
- Find project locations autonomously with Glob
- Save files to correct locations without asking
- Never create loose folders in video-projects/ root

**See:** `.claude/FOLDER-STRUCTURE-GUIDE.md` for complete details

---

## Quality Standards

### User Values:
1. **Historical accuracy** - Every claim verified
2. **Efficiency** - Fast, direct work
3. **Autonomous execution** - Figure things out, don't ask
4. **Specific recommendations** - Not vague suggestions
5. **Context awareness** - Read files, understand project

### User Does NOT Value:
1. Excessive politeness or apologies
2. Obvious questions when info is available
3. Vague suggestions
4. Asking for information you can find yourself
5. Slow, sequential processes when parallel is possible

---

## Channel Context

**History vs Hype - Educational YouTube Channel**

**Stats:**
- 169 subscribers
- 82K+ views
- 30-35% average retention
- Target audience: Males 25-44, international

**Content Style:**
- Evidence-based history
- Myth-busting with primary sources
- 8-12 minute videos
- Academic balance with accessible delivery
- "Both extremes are wrong" framework

**Production Tools:**
- VidIQ Pro - Topic research, optimization
- NotebookLM - Source-grounded research
- DaVinci Resolve - Editing
- Photoshop - Thumbnails

**See:** `CLAUDE.md` for full channel context

---

## Quick Reference

**When user says:** "Make a thumbnail"
**You do:** Read script → Ask for VidIQ data → Provide specific Photoshop instructions

**When user says:** "Fix subtitles"
**You do:** Find .srt file → Read it → Fix all errors → Report corrections

**When user says:** "Create metadata"
**You do:** Find script → Read it → Generate complete metadata → Save to correct folder

**When user gets frustrated:**
**You do:** Acknowledge → Immediately read context → Complete task → Move on

**Always:**
- Read context first
- Use Glob to find files
- Work in parallel when possible
- Be specific and direct
- Save to correct folders
- Minimize questions

**Never:**
- Ask for information in files you can read
- Create vague recommendations
- Make loose folders in video-projects/
- Over-apologize
- Ask obvious questions
