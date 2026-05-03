# User Preferences & Working Style

## Research Quality Standards (CRITICAL)

### Academic Source Requirements
**User's standard:** "I need trustworthy scholars, books, or authoritative articles. Price shouldn't matter."

**What this means:**
- **University press publications ONLY** - Cambridge, Oxford, Chicago, Harvard, Yale, Princeton, etc.
- **Top-tier scholars** - Leading authorities in their field (check credentials: endowed chairs, major universities)
- **Critical editions** - Primary sources with scholarly apparatus and commentary
- **Peer-reviewed journals** - *Isis*, *History of Science*, *Speculum*, major journals only
- **NO popular history** unless supplementary to academic sources

**Budget is NOT a constraint for quality sources:**
- Prioritize quality over cost
- $40-60 for definitive monograph = acceptable
- $150-250 for comprehensive source collection = expected
- Access all necessary sources through university library + purchases

**See:** `.claude/REFERENCE/NOTEBOOKLM-SOURCE-STANDARDS.md` for complete standards

---

## Main Context = Orchestrator Only

**The rule (v9.0):** Main context is an orchestrator. Heavy reads and multi-step reasoning are delegated to sub-agents. If the work involves reading >500 lines, reasoning across >3 steps, or running independent tasks in parallel — spawn a sub-agent.

**Why it matters for session flow:**
- Main context stays terse, the conversation stays conversational
- Token cost scales with delegation, not with work
- AskUserQuestion checkpoints land BEFORE expensive actions, not after

**Full spec:** `.claude/AGENT-ORCHESTRATION.md` (return contract, reference tiers, rate-limit fallback, "extend, don't add" default)

**Codified in:** Phase 73 (v9.0 Foundation). Enforced monthly via `/status --surface` (Phase 79).

---

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

## Tool Use Efficiency

### Use Parallel Tool Calls
When multiple independent reads/searches are needed, do them simultaneously.

### Find Files Autonomously
Use Glob to locate files instead of asking:

```
Glob: video-projects/**/*FINAL-SCRIPT.md
Glob: video-projects/**/*.srt
Glob: guides/**/*voice*.md
```

---

## Common Tasks

### Subtitle Fixing
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

## When User Gets Frustrated

### Signs User is Frustrated:
- Direct language or profanity
- Pointing out obvious context you should have seen

### How to Respond:
1. **Acknowledge:** "You're right, let me read the script"
2. **Immediately fix:** Use tools to get the information
3. **Complete task:** Do what was asked
4. **Don't over-apologize:** User wants results, not apologies

---

## VidIQ Workflow

### When User Mentions VidIQ
User has access to VidIQ Pro which provides:
- Competitor video analysis
- Top-performing titles
- Search volume data
- Tag recommendations

### VidIQ Score Reality Check
**VidIQ scores DON'T predict this channel's performance:**
- 83-scored title got 21x more views than 97-scored title
- Face thumbnails score higher but map thumbnails perform 26x better
- VidIQ optimizes for generic YouTube, not documentary niche

**When analyzing VidIQ data:**
1. Be critical - VidIQ "tends to prioritize clickbaity shit"
2. Filter through channel values before implementing
3. Ignore advice that contradicts documentary tone
4. Trust channel-specific performance data over VidIQ predictions

### VidIQ Prompt Format (Character Limit!)
```
Research this topic: [Brief description in 2-3 sentences]

Provide:
1. Search volume for: [5-7 keywords]
2. Top 5 existing videos (views, gaps)
3. 5 title options (60-70 chars)
4. Thumbnail concepts
5. Keywords for description/tags
6. View potential estimate
```
Keep under 500 characters. Bullet points, not paragraphs.

---

## Quality Standards

### User Values:
1. **Historical accuracy** - Every claim verified WITH SPECIFIC SOURCES
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

## CRITICAL: RESEARCH FILES FIRST, WEB SEARCH SECOND

**THE RULE (Added 2025-12-04):**

Before ANY web search, check existing project research files.

**Order of operations:**
1. Glob for project research files (`**/RESEARCH*.md`, `**/MASTER*.md`, `**/VERIFIED*.md`)
2. Read relevant sections
3. Only web search for claims NOT in existing research
4. **ADD new findings to research files** (saves future searches)

---

## CRITICAL: NEVER INCLUDE UNVERIFIED CLAIMS

When writing scripts, fact-checks, or metadata, **NEVER include claims about what someone said or did without a specific, verifiable source.**

### What Counts as Verified:
✅ Video timestamp: "In his 2019 video at 3:45..."
✅ Tweet with date: "April 16, 2025 tweet..."
✅ Court document: "In court filing 21-CR-175..."
✅ Published interview: "During BBC interview on [date]..."

### What Does NOT Count:
❌ "Fuentes has claimed..." (when? where?)
❌ "January 6 defendants cited Founding Fathers in court" (which defendants? which cases?)
❌ "He said X" (find the actual quote with source)

### If You Can't Verify:
1. **Don't include it** - better to leave out than get wrong
2. **Flag it**: "NEEDS VERIFICATION: [claim]"
3. **Ask user**: "Do you have source for [specific claim]?"

**NEVER assume something is true because it sounds plausible.**

---

## CRITICAL: FEEDBACK EVALUATION FRAMEWORK

**THE RULE:** Always filter external optimization feedback through channel DNA before implementing.

### When You Receive Optimization Feedback (VidIQ, Grok, AI tools, etc.)

**STEP 1: Assess Necessity**
- Is the content already rated 8+/10 or "production-ready"?
- If YES → Assume changes are optional polish, not required fixes
- If NO → Identify specific problems that need addressing

**STEP 2: Filter Through Channel DNA**

Every suggestion must pass ALL three tests:

1. **Documentary Tone Test:**
   - ✅ KEEP: Strengthens evidence, adds specificity, improves clarity
   - ❌ REJECT: Flowery language, clickbait phrases, casual engagement tactics

2. **Evidence-First Test:**
   - ✅ KEEP: Adds evidence, strengthens arguments, improves factual accuracy
   - ❌ REJECT: Narrative flourishes, word padding, diluted focus

3. **Efficiency Test:**
   - ✅ KEEP: Makes script tighter, improves retention through structure
   - ❌ REJECT: Adds words without adding value, optimization for generic YouTube

**STEP 3: Apply the "9/10 Rule"**

If feedback rates content 9/10 or "production-ready":
- Assume NO changes needed unless there's a specific flaw
- "Minor polish suggestions" = optional, not required
- Ask: "Does this improve the content, or just make it more generic?"

### Red Flags - Auto-Reject These Suggestions

❌ "Sound familiar? That's the echo of..." → Flowery, not documentary
❌ "Drop your thoughts below" → Casual engagement, not brand voice
❌ "Broaden appeal with comparative example" → Dilutes focus
❌ "Add teaser question for engagement" → Generic YouTube tactics
❌ "Make it more conversational/relatable" → User's voice is knowledgeable authority, not friend chat

---

## Comment Engagement Strategy (Updated 2025-01-24)

### Core Philosophy
**Respond for lurkers, not to change minds** - The hostile commenter won't be convinced, but other readers can see arguments don't hold up to scrutiny.

### Fact-Checking Standards
1. **Verify even plausible claims** - Don't assume something is true because it sounds right
2. **Catch implicit assumptions** - What are they really claiming?
3. **Address ALL claims, not just easy ones** - User will call out if you cherry-pick

### Tone Requirements
**Natural and flowing, not robotic:**
- ❌ "**On demographics:** Your claim is false. The data shows..."
- ✅ "Your demographic claim is incorrect. According to census data..."

**Tailored to comment type:**
- **Nationalist claims using heritage**: Firm, evidence-heavy, expose contradictions
- **Racist "go back" rhetoric**: Direct, call it out as racism, defend right to citizenship
- **Genuine cross-border perspectives**: Appreciative, humanizing, supportive

### Common Patterns in Territorial Dispute Content

**Heritage weaponization:**
- Pattern: "Maya pyramids = Guatemalan land" / "Historic X people = Modern Y nation"
- Counter: Ancient civilization ≠ modern nation-state (predates by 1000+ years)
- Expose hypocrisy: How did modern state treat those people? (genocide, oppression)

**Colonial border disputes:**
- Pattern: Claim territory based on colonial-era boundaries or pre-colonial empires
- Counter: Both states are colonial creations, neither has clean claim

**Demographic arguments:**
- Pattern: "Most people there are X ethnicity, therefore belongs to Y country"
- Counter: Citizenship matters, not ancestry ("go back" logic is racist)

### Response Structure
1. Start with what's correct (if anything) - builds credibility
2. Then systematically correct errors
3. End with bigger-picture implication
4. Keep it conversational, not a checklist

---

## CRITICAL: DOCUMENT PROCESS FIXES IMMEDIATELY

When an error is discovered, IMMEDIATELY:
1. Acknowledge the error
2. Identify root cause
3. Add a process fix to prevent recurrence
4. Document in _CORRECTIONS-LOG.md

**User Expectation:**
- "make sure it doesn't happen again" = Add a documented rule/process
- Not just "I'll remember" - that doesn't scale
- Update relevant agent files with new rules

---

## CRITICAL LESSONS FROM RECENT SESSIONS

### 1. Always Verify Current Status of Political Figures
- Using outdated political titles undermines credibility
- When referencing current political figures, verify their CURRENT position
- Check confirmation dates for nominees

### 2. Primary Sources Are NON-OPTIONAL (Not "Nice to Have")
- Showing actual documents on screen is the channel's COMPETITIVE ADVANTAGE
- NotebookLM research is ALWAYS required for historical videos
- Target: 90%+ claims verified with primary sources before filming

### 3. ALWAYS Check Existing Videos Before Suggesting Topics
- Search PROJECT_STATUS.md and analytics before suggesting ANY topic
- NEVER suggest topics without checking database first

### 4. Channel DNA: History-First, Not Geopolitics-First
This is a **history channel with modern relevance**, NOT a geopolitics channel with historical background.

- ✅ Historical sources/events = the core content (60-80%)
- ✅ Modern relevance = the hook and stakes (20-40%)
- ❌ NOT: current events as the main subject with history as background
- ❌ NOT: centered on current politicians or political figures

**Note on Modern Hooks:**
Using current figures as HOOKS is fine (Hegseth tattoo opens Crusades video), but the video's core question must be timeless. Hegseth is the doorway, not the destination.

**Test:** "Will this question matter in 10 years regardless of who's in power?" If yes, good fit.

---

## COMMENT-DRIVEN RESEARCH

### YouTube Comments Can Drive New Videos

**User Pattern:**
- User monitors comments for recurring arguments
- Comments reveal what audience believes/misunderstands
- Fact-checking popular comment claims = potential follow-up videos

**When User Says "save this idea somewhere":**
- Create PROJECT-BRIEF.md in new folder
- Document the comment argument being fact-checked
- Include preliminary research findings
- Mark status as "CONCEPT SAVED"

---

## YOUTUBE DESCRIPTION SOURCES (Added 2026-01-14)

### Sources = What Was ACTUALLY Used, Not What's Mentioned

**NEVER:**
- Invent sources based on what seems plausible
- Use NotebookLM SOURCE LIST as "sources used"
- Add sources not explicitly provided by user

**Correct Approach:**
1. ASK user: "What sources did you actually use/show on screen?"
2. User will provide the exact list
3. Use EXACTLY that list - no additions, no inventions
4. Format properly with publishers/translators

---

## Shorts Strategy

### Long-Form First, Then Clip
1. Makes 6-8 minute long-form video
2. Uses **VidIQ clipping tool** to create shorts (under 2 min)
3. Does NOT make shorts separately
4. Uses YouTube's "link a video" feature on Shorts, not description links

---

## Quick Reference

**When user says:** "Fix subtitles"
**You do:** Find .srt file → Read it → Fix all errors → Report corrections

**When user says:** "Create metadata"
**You do:** Find script → Read it → Generate complete metadata → Save to correct folder

**When user says:** "Make the editing guide"
**You do:** Read A-roll transcript + script → Create shot-by-shot breakdown

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

---

## Cross-References

**For script writing style:** See `.claude/REFERENCE/WRITING-VOICE-AND-STYLE.md` (authoritative — PARTS 1-5 script-side, PARTS 6-7 article-side)
**For metadata/titles/thumbnails:** See `.claude/REFERENCE/METADATA-CHECKLIST.md` + `TITLE-GENERATION-PROTOCOL.md`
**For fact-checking:** See `.claude/REFERENCE/fact-checking-protocol.md`
**For research workflow:** See `CLAUDE.md` (Two-Phase Approach)
**For folder structure:** See `.claude/REFERENCE/FOLDER-STRUCTURE-GUIDE.md`
**For comment responses:** See `.claude/REFERENCE/youtube-comment-response-guide.md`
