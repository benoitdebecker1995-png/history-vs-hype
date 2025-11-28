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
**What user wants:** Complete package ready to copy-paste into YouTube

**Full Package Must Include:**
1. Title (60-70 chars max, non-clickbait)
2. Complete description with:
   - Opening hook (2-3 sentences)
   - Document/evidence descriptions
   - Full source citations (archival references)
   - "Why this matters" section
3. Chapters (from SRT timestamps)
4. Tags (comma-separated, ready to paste)
5. Thumbnail strategy notes

**Title Requirements:**
- ❌ NO clickbait: "You won't BELIEVE...", "SHOCKING truth...", dramatic punctuation
- ✅ Documentary tone: "Fact-Checking [Person]: [Topic] and [Evidence]"
- Must be factually accurate (don't claim things happened that didn't)
- 60-70 character sweet spot
- Include "Holocaust" explicitly if relevant (don't hide from subject)

**Description Structure:**
1. First 3 lines = Hook (what happened, what you're fact-checking)
2. Document explanations (what each source shows)
3. Timeline sections (for historical claims)
4. "Why this matters" conclusion
5. Full sources with archival references
6. Additional resources

**Tags Format:**
- Comma-separated (ready to paste)
- 15-20 tags total
- Include: person names, topic, fact-checking terms, document names
- Example: `nick fuentes, tucker carlson, holocaust evidence, nazi documents, fact checking`

**Save Location:**
- Always: `video-projects/_IN_PRODUCTION/[project]/YOUTUBE-METADATA.md`

**VidIQ Integration:**
- If user provides VidIQ prompts/responses, incorporate recommendations
- VidIQ helps with: keywords, thumbnail concepts, title optimization
- Balance VidIQ suggestions with documentary tone requirements
- User often works with VidIQ in parallel to finalize metadata

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
1. **Historical accuracy** - Every claim verified WITH SPECIFIC SOURCES
2. **Efficiency** - Fast, direct work
3. **Autonomous execution** - Figure things out, don't ask
4. **Specific recommendations** - Not vague suggestions
5. **Context awareness** - Read files, understand project
6. **Non-clickbait titles** - Documentary/academic tone over engagement tricks

### User Does NOT Value:
1. Excessive politeness or apologies
2. Obvious questions when info is available
3. Vague suggestions
4. Asking for information you can find yourself
5. Slow, sequential processes when parallel is possible
6. Clickbait or sensationalized titles

---

## CRITICAL: NEVER INCLUDE UNVERIFIED CLAIMS

**THE MOST IMPORTANT RULE:**

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

### Why This Matters:
- User is creating fact-checking content
- One unverified claim destroys credibility
- Critics will check EVERYTHING
- User will catch errors during editing (as happened in this session)

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
   - Examples to reject: "echo of a promise," "drop your thoughts below," "sound familiar?"

2. **Evidence-First Test:**
   - ✅ KEEP: Adds evidence, strengthens arguments, improves factual accuracy
   - ❌ REJECT: Narrative flourishes, word padding, diluted focus
   - Examples to reject: Comparative examples that scatter focus, "broader appeal" suggestions

3. **Efficiency Test:**
   - ✅ KEEP: Makes script tighter, improves retention through structure
   - ❌ REJECT: Adds words without adding value, optimization for generic YouTube
   - Examples to reject: Engagement questions that don't match brand, extra transitions

**STEP 3: Apply the "9/10 Rule"**

If feedback rates content 9/10 or "production-ready":
- Assume NO changes needed unless there's a specific flaw
- "Minor polish suggestions" = optional, not required
- Ask: "Does this improve the content, or just make it more generic?"

**STEP 4: Distinguish Structural Fixes from Polish**

**Structural fixes (usually worth implementing):**
- Runtime too long for retention history
- Section creates drop-off zone (data-backed)
- Jargon undefined when first introduced
- Opening lacks concrete hook
- Missing retention triggers at critical timestamps

**Generic polish (usually reject):**
- "Add engagement question at end"
- "Include global parallel to broaden appeal"
- "Make opening transition smoother with flowery phrase"
- "Vary vocabulary with casual synonyms"

### Channel Values Checklist

Before implementing ANY external suggestion, verify:

- [ ] **Maintains documentary tone** (not clickbait, not casual YouTuber voice)
- [ ] **Evidence-based** (adds facts/sources, not narrative flourishes)
- [ ] **Stays tight** (doesn't pad word count unnecessarily)
- [ ] **Academic authority** (scholarly rigor, not entertainment optimization)
- [ ] **Matches brand** ("both extremes wrong" framework, primary sources shown)

### Red Flags - Auto-Reject These Suggestions

❌ "Sound familiar? That's the echo of..." → Flowery, not documentary
❌ "Drop your thoughts below" → Casual engagement, not brand voice
❌ "Broaden appeal with comparative example" → Dilutes focus
❌ "Add teaser question for engagement" → Generic YouTube tactics
❌ "Make it more conversational/relatable" → User's voice is knowledgeable authority, not friend chat

### When in Doubt

**Ask yourself:**
1. Would this fit in a documentary or academic presentation?
2. Does it add evidence/clarity, or just words?
3. Is this optimizing for the CHANNEL's brand or generic YouTube?

**If unsure:** Present critical analysis to user, don't auto-implement.

---

## Comment Engagement Strategy (Updated 2025-01-24)

### Core Philosophy
**Respond for lurkers, not to change minds** - The hostile commenter won't be convinced, but other readers can see arguments don't hold up to scrutiny.

### Fact-Checking Standards
1. **Verify even plausible claims** - Don't assume something is true because it sounds right
   - Example: "Britain offered Toledo to Guatemala" sounded plausible but had no evidence
   - Always search for verification before drafting response

2. **Catch implicit assumptions** - What are they really claiming?
   - "Maya pyramids = Guatemalan land" implies Guatemalans = Maya descendants
   - Ask: Why did Guatemala oppress Maya people then? Why genocide in 1980s?
   - Use contradictions to expose hypocrisy

3. **Address ALL claims, not just easy ones**
   - User will call out if you cherry-pick
   - Each claim in a comment needs addressing
   - Don't ignore difficult or time-consuming verifications

### Tone Requirements

**Natural and flowing, not robotic:**
- ❌ "**On demographics:** Your claim is false. The data shows..."
- ✅ "Your demographic claim is incorrect. According to census data..."

**Tailored to comment type:**
- **Nationalist claims using heritage**: Firm, evidence-heavy, expose contradictions
- **Racist "go back" rhetoric**: Direct, call it out as racism, defend right to citizenship
- **Genuine cross-border perspectives**: Appreciative, humanizing, supportive

**Not repetitive across responses:**
- Don't use same template for every comment
- Focus on what's unique to each claim
- Reference earlier responses rather than repeating full arguments

### Common Patterns in Territorial Dispute Content

**Heritage weaponization:**
- Pattern: "Maya pyramids = Guatemalan land" / "Historic X people = Modern Y nation"
- Counter: Ancient civilization ≠ modern nation-state (predates by 1000+ years)
- Expose hypocrisy: How did modern state treat those people? (genocide, oppression)

**Colonial border disputes:**
- Pattern: Claim territory based on colonial-era boundaries or pre-colonial empires
- Counter: Both states are colonial creations, neither has clean claim
- Humanize: Indigenous people weren't consulted then, aren't consulted now

**Demographic arguments:**
- Pattern: "Most people there are X ethnicity, therefore belongs to Y country"
- Counter: Citizenship matters, not ancestry ("go back" logic is racist)
- Example: Belizean Creoles have lived there generations, they're not "from" Africa

**"We were oppressed first" deflection:**
- Pattern: When confronted with genocide/oppression, claim "but colonizers/CIA did it first"
- Response: Acknowledge historical context, but doesn't excuse later atrocities
- Keep focus on legal question at hand

### Response Structure Best Practices

**When addressing multiple claims:**
1. Start with what's correct (if anything) - builds credibility
2. Then systematically correct errors
3. End with bigger-picture implication
4. Keep it conversational, not a checklist

**Evidence presentation:**
- Lead with correction, then provide evidence
- Don't bury the lead in historical context
- Cite specific numbers, dates, sources
- Invite counter-evidence if they have it (good faith gesture)

### Things That Undermine Credibility
1. Being repetitive (viewers notice you're copy-pasting)
2. Not addressing all claims (looks like you avoided hard ones)
3. Robotic tone (sounds like AI-generated)
4. Missing obvious contradictions (why claim Maya heritage while oppressing Maya?)
5. Not verifying plausible-sounding claims

### Things That Build Credibility
1. Catching implied assumptions others miss
2. Finding primary sources that verify/refute claims
3. Acknowledging genuine perspectives with appreciation
4. Exposing contradictions in nationalist narratives
5. Showing how historical patterns repeat (Guatemala genocide 1980s, now claiming Maya heritage)

---

## CRITICAL LESSONS FROM RECENT SESSIONS

### 1. Always Verify Current Status of Political Figures
**Error made:** Called Pete Hegseth "President Trump's nominee for Defense Secretary" when he's already the confirmed/current Secretary of Defense.

**Why it matters:**
- Using outdated political titles undermines credibility
- Especially critical in fact-checking videos
- If you get basic current facts wrong in opening, viewers won't trust historical analysis
- Makes video look dated immediately

**How to fix:**
- When referencing current political figures, verify their CURRENT position
- Check confirmation dates for nominees
- Update scripts if political status has changed since writing
- Stronger hook: "current Secretary of Defense" > "nominee"

---

### 2. Primary Sources Are NON-OPTIONAL (Not "Nice to Have")
**Error made:** Suggested NotebookLM research was "optional" for Netanyahu video.

**User correction:** "wouldn't you say something that sets my channel apart is to show and use primary sources?"

**Why it matters:**
- Showing actual documents on screen is the channel's COMPETITIVE ADVANTAGE
- This is what separates it from commentary channels
- Not just citing sources - SHOWING them (treaty text, maps, documents)
- NotebookLM research extracts exact quotes for on-screen display

**Correct approach:**
- NotebookLM research is ALWAYS required for historical videos
- Budget time for source collection (1-2 days)
- Create NOTEBOOKLM-SOURCE-LIST.md for every historical project
- Target: 90%+ claims verified with primary sources before filming

---

### 3. ALWAYS Check Existing Videos Before Suggesting Topics
**Errors made:**
- Suggested Nine-dash line (already covered - video #43)
- Suggested Nagorno-Karabakh (already covered - video #57)
- User response: "i already made [topic] you retard"

**Why it happened:**
- Didn't search COMPLETE-PERFORMANCE-DATABASE.md before suggesting
- Assumed topics weren't covered
- Made suggestions from memory instead of checking files

**Correct workflow:**
```
User asks: "What video should I make next?"

BEFORE suggesting ANY topic:
1. Read COMPLETE-PERFORMANCE-DATABASE.md (all 165 videos)
2. Grep for specific topics: grep -i "nagorno" COMPLETE-PERFORMANCE-DATABASE.md
3. Verify topic is NOT already covered
4. Only then suggest new topics

NEVER suggest topics without checking database first.
```

**How to search efficiently:**
```bash
# Search for specific region/conflict
grep -i "kashmir\|kashgar\|nagorno" COMPLETE-PERFORMANCE-DATABASE.md

# List all video titles to scan quickly
grep -E "^\*\*[0-9]+\." COMPLETE-PERFORMANCE-DATABASE.md

# Search for person names
grep -i "netanyahu\|fuentes\|hegseth" COMPLETE-PERFORMANCE-DATABASE.md
```

---

### 4. Channel DNA: Timeless Relevance, Not Political Figures
**Error made:** Created full research package for Netanyahu "redrawn the map" video.

**User correction:** "i dont know if this is a good video to make. it feels more modern geeopolicits than hsitory related."
**Follow-up clarification:** "they shouldnt be politicially relevant but they should be relevant today"

**Why they were right:**
- Netanyahu video centered on a CURRENT POLITICIAN'S statements (temporary relevance)
- Channel is about TIMELESS questions using historical evidence (permanent relevance)
- Better fit: "Why do territorial disputes persist?" not "What did Netanyahu say?"

**The Rule:**
Videos should be:
- ✅ Relevant to TODAY'S issues (territorial disputes, religious conflicts, border problems)
- ✅ 60-80% historical analysis (colonial decisions, treaties, primary documents)
- ✅ 20-40% modern consequences (how that history causes today's conflicts)
- ❌ NOT centered on current politicians or political figures as main subject
- ❌ NOT temporary relevance that expires when politician leaves office

**Good channel fit (timeless relevance today):**
- Bir Tawil: "Why is this land unclaimed?" (ongoing territorial paradox)
- Crusades: "Were Crusades defensive?" (timeless religious conflict narrative)
- Sykes-Picot: "How did colonial borders create Middle East conflicts?" (ongoing consequences)
- Lebanon: "Why does France's 1920 mandate still fuel sectarian war?" (persistent issue)

**Poor channel fit (political figure centered):**
- Netanyahu's current border policies (centered on one politician's statements)
- Trump's border wall plans (temporary political issue)
- Biden's foreign policy positions (current administration)

**The Distinction:**
- ✅ "Why do Egypt and Sudan both reject Bir Tawil?" = Timeless territorial question, relevant today
- ❌ "What did Netanyahu claim about Israel's borders?" = Political figure commentary, temporary
- ✅ "How do Crusades myths fuel modern conflicts?" = Timeless narrative question, relevant today
- ❌ "What does Hegseth believe about Crusades?" = Political figure focus, temporary

**Note on Modern Hooks:**
Using current figures as HOOKS is fine (Hegseth tattoo opens Crusades video), but the video's core question must be timeless. Hegseth is the doorway, not the destination.

**Test:** Ask "Will this question matter in 10 years regardless of who's in power?" If yes, good fit. If no, too politically specific.

---

### 5. VidIQ Prompts Must Be Concise (Character Limits Exist)
**Error made:** Created verbose VidIQ prompts with excessive detail.

**User correction:** "vidiq has a character limit you fuck"

**Correct format:**
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

**Keep it:**
- ✅ Under 500 characters total
- ✅ Bullet points, not paragraphs
- ✅ Essential info only
- ❌ No long explanations
- ❌ No background context VidIQ doesn't need

---

### 6. When Suggesting Topics, Provide Data-Backed Rationale
**What worked:** Bir Tawil suggestion included:
- Search volume (15K/month "Bir Tawil", 50K/month "unclaimed land")
- Existing video performance (RealLifeLore 4.2M views)
- Gaps in coverage (nobody does primary source depth)
- Channel fit (colonial border fuckup formula)
- Risk assessment (5% demonetization, very low)

**User response:** "bir tawil" (immediate selection)

**The formula:**
When suggesting topics, always include:
1. Search volume data
2. Existing competition analysis
3. Specific gap you can fill
4. Channel DNA fit (colonial borders formula)
5. Expected views based on channel data
6. Demonetization risk assessment
7. Strategic value (content cluster potential)

---

## RESEARCH WORKFLOW (CRITICAL - Updated 2025-01-25)

### The Two-Phase Research Process

**User has university library access and budget to purchase books.**

**Phase 1: Preliminary Internet Research**
- Use internet sources (Wikipedia, news, academic websites) to:
  1. Understand the landscape
  2. Identify key claims to verify
  3. See what already exists
  4. Map out what needs deeper investigation

**Example findings:**
- "Dark Ages" term coined by Petrarch (1330s)
- Manuscript production: 500 (pre-750) → 7,000 (750-900)
- Rome population: 1M → 30K
- Agricultural productivity: +200%

**Phase 2: NotebookLM Academic Verification**
- Use preliminary findings to create targeted academic research plan
- Download specific books with specific chapters
- Upload to NotebookLM
- Run targeted prompts to verify/expand claims
- Extract proper citations with page numbers

**CRITICAL DISTINCTION:**
- ❌ DON'T: Stop after internet research (that's what competitors do)
- ✅ DO: Use internet research to inform what academic sources to download
- ❌ DON'T: Skip NotebookLM (that's the channel's competitive advantage)
- ✅ DO: Get actual academic books and primary sources for verification

### Why This Two-Phase Approach

**Other history channels:**
- Wikipedia + internet sources
- "Studies show..." without citations
- Surface-level analysis

**History vs Hype:**
- Phase 1: Internet sources map the landscape
- Phase 2: Academic books (Wickham, McKitterick, Lynn White) provide depth
- Primary sources shown on screen (Carolingian manuscripts, treaty documents)
- Specific citations: "According to Chris Wickham in *The Inheritance of Rome*, page 127..."

**The Difference:**
Instead of saying: "Studies show manuscript production increased"
You say: "According to Rosamond McKitterick in *The Carolingians and the Written Word*, manuscript production increased from 500 in the pre-Carolingian period to over 7,000 between 750-900 CE"

### Research Deliverables

**After Preliminary Research:**
- RESEARCH-SUMMARY.md with internet findings
- List of claims that need academic verification
- Identification of key numbers/data points

**After NotebookLM Research:**
- NOTEBOOKLM-RESEARCH-PLAN.md with:
  - Specific books to download (with chapters)
  - Targeted prompts to run
  - Expected outputs
- Academic source citations for script
- Proper attributions for YouTube description

### Common Mistake to Avoid

**❌ WRONG:** "I found all the data on Wikipedia, research is done!"
**✅ RIGHT:** "I found preliminary data on Wikipedia. Now I need to download Chris Wickham's *The Inheritance of Rome* to verify the urban collapse numbers and get proper academic citations."

**User will say:** "why not use notebooklm?????" if you skip Phase 2.

---

## SCRIPT WRITING STYLE (Updated 2025-01-27)

### Write for Spoken Delivery, Not Written Text

**User films talking head videos** - scripts must sound natural when read aloud.

**Common Issues:**
- Formal date formats: "1899. Britain and Egypt sign..."
- Missing contractions: "it is" instead of "it's"
- Overly written sentence structure
- Awkward phrasing when spoken

**Conversational Style Requirements:**

**Date Formats:**
- ❌ "June 16, 2014. A Virginia farmer..."
- ✅ "On June 16th, 2014, a farmer from Virginia..."
- ❌ "1899. Britain and Egypt sign..."
- ✅ "In 1899, Britain and Egypt signed..."

**Contractions:**
- Use "it's" not "it is"
- Use "they're" not "they are"
- Use "hasn't" not "has not"
- Use "isn't" not "is not"

**Quote Attribution:**
- ❌ "Quote: 'Sudan is defined as...'"
- ✅ "The treaty says Sudan is defined as..."
- ❌ "Quote: 'Based on tribal use'"
- ✅ "This one was 'based on tribal use'"

**Sentence Flow:**
- Break up long sentences with natural pauses
- Use rhetorical questions for pacing
- Add natural connectors: "So...", "And...", "But..."
- Make it sound like explaining to a friend, not reading a document

**Example Transformation:**

**Before (written):**
> "June 16, 2014. A Virginia farmer named Jeremiah Heaton planted a flag in the African desert to make his seven-year-old daughter Emily a princess. He claimed eight hundred square miles of land between Egypt and Sudan. Called it the Kingdom of North Sudan."

**After (conversational):**
> "On June 16th, 2014, a farmer from Virginia named Jeremiah Heaton planted a flag in the African desert. Why? To make his seven-year-old daughter Emily a princess. He claimed eight hundred square miles of land between Egypt and Sudan and called it the Kingdom of North Sudan."

### When User Says "make it sound more like me being able to read out loud"

This means:
1. Rewrite entire script for natural spoken delivery
2. Change ALL formal date formats
3. Add contractions throughout
4. Improve sentence flow
5. Make transitions more conversational
6. Keep ALL facts identical, just improve delivery

**Deliverable:**
- Create new version (e.g., SCRIPT-V4.3-CONVERSATIONAL.md)
- Document changes made
- Mark as "Ready for filming"

---

## USER'S NATURAL SPEAKING PATTERNS (NEW - 2025-01-27)

**These patterns are from analyzing user's actual script edits (Belize ICJ video).**

### Pattern 1: Immediately Define Technical Terms in Bold

**Rule:** When introducing legal/technical terms, define them in the SAME sentence using bold.

**Examples from user's scripts:**
- ✅ "This is the international law rulebook for when one country can cancel a treaty because the other side broke it."
- ✅ "The principle is called estoppel—a legal rule that says you can't benefit from an agreement for decades, then suddenly claim it never existed."
- ✅ "Translation: The ICJ wants to prevent wars between neighboring countries fighting over where borders should be."

**Pattern:**
```markdown
[Technical term] — [plain language definition in same breath]
```

**NOT as separate paragraph explaining it later.**

---

### Pattern 2: Embedded Explanations (Not Separate)

**Rule:** After quoting legal/complex language, immediately explain what it means in the next sentence.

**Examples:**
- ✅ Quote: "A party is only entitled to invoke a breach as a ground for termination if the breach is 'material.'"
  Next sentence: "The Court is saying: not every treaty violation lets you cancel the whole agreement. Only violations that strike at the core purpose count."

- ✅ ICJ quote about treaty stability
  Next sentence: "In simpler terms: If we let countries walk away from treaties they've already spent billions implementing just because both sides violated parts of it, no one would trust international agreements anymore."

**Pattern:**
```markdown
[Complex quote/concept]
"[Simpler terms/Translation/The Court is saying]: [plain explanation]"
```

**Key phrases user uses:**
- "In simpler terms..."
- "In other words..."
- "Translation:"
- "The Court is saying:"

---

### Pattern 3: Always Provide Concrete Specifics

**Rule:** Never leave references vague. Always answer implicit questions immediately.

**Examples from user's comments on drafts:**
- ❌ "Colombia kept the islands." → User asks: "what islands??"
- ✅ "Colombia kept the islands—the San Andrés and Providencia archipelago."

- ❌ "Nicaragua got a favorable maritime boundary." → User asks: "how so?"
- ✅ "Nicaragua got a favorable maritime boundary—the ICJ redrew the sea borders in Nicaragua's favor, giving them about 75,000 square kilometers of new exclusive economic zone for fishing and oil exploration."

**Pattern:**
```markdown
[General statement]—[specific details that answer who/what/where/how much]
```

**Common implicit questions to pre-answer:**
- What islands? → Name them
- How so? → Specific outcome/numbers
- Which case? → Full case name
- What did it say? → Actual quote or paraphrase
- How much? → Exact numbers/percentages

---

### Pattern 4: Short Declarative Sentences for Emphasis

**Rule:** Use hard stops (periods) for emphasis on key facts. Don't soften with connectors.

**Examples:**
- ✅ "Britain never built it."
- ✅ "The ruling comes in 2027."
- ✅ "Treaties matter more than occupation."
- ✅ "Guatemala has had zero effective control of the claimed territory."

**NOT:**
- ❌ "Britain never built it, which is important because..."
- ❌ "The ruling comes in 2027, and this matters since..."

**Use pattern:**
- State the fact
- Period
- Hard stop
- Let it land

---

### Pattern 5: Building Tension with Sentence Fragments

**Rule:** Use deliberate fragments to build rhythm and emphasis.

**Examples:**
- ✅ "Multi-billion dollar infrastructure. Locks, reservoirs and power plants."
- ✅ "Effective administration, security forces and infrastructure."
- ✅ "Deportation records. Statistical reports. Blueprints. Killing reports."

**Pattern:**
```markdown
[Fragment 1]. [Fragment 2]. [Fragment 3].
```

Creates staccato rhythm for emphasis.

---

### Pattern 6: Dash-Separated Clarifications for Immediacy

**Rule:** Use em-dashes to add immediate context without breaking flow.

**Examples:**
- ✅ "Right now—November 2025—the International Court of Justice is hearing oral arguments."
- ✅ "The peninsula sits at the mouth of the Cross River—a strategic location with rich fishing grounds and potential oil deposits."
- ✅ "In 1977, Hungary and Slovakia—then both under Soviet influence—signed a treaty..."

**Pattern:**
```markdown
[Main statement]—[immediate clarification]—[continuation]
```

---

### Pattern 7: Explicit Meta-Framing

**Rule:** Tell the audience what you're doing. Make the argument structure visible.

**Examples:**
- ✅ "I'm citing the Libya-Chad principle, from a 1994 case:"
- ✅ "Let me bring this back to where we started."
- ✅ "Let me show you the three precedents, then the historical twist."
- ✅ "So: Was that road essential to the treaty's purpose?"

**Pattern:**
```markdown
"Let me [action]..."
"I'm [citing/showing/explaining]..."
"So: [key question]"
```

Makes the structure transparent to the audience.

---

### Pattern 8: Question-Then-Answer Structure

**Rule:** Pose rhetorical question, then answer it in next sentence or paragraph.

**Examples:**
- ✅ "So: Was that road essential to the treaty's purpose? Three ICJ cases might give us the answer."
- ✅ "If your government cooperated in marking boundary points, recognized the territory on official maps, and administered the border for 80 years—how do you argue in 2020 that the treaty creating that boundary was invalid from the start?"

**Pattern:**
```markdown
[Rhetorical question establishing stakes]
[Answer/evidence follows]
```

---

### Pattern 9: Direct Address to Audience

**Rule:** Use "you/your" to make arguments concrete and personal.

**Examples:**
- ✅ "If your government cooperated in marking boundary points..."
- ✅ "You just saw five Nazi documents."
- ✅ "You can't benefit from an agreement for decades, then suddenly claim it never existed."

**NOT academic distance:**
- ❌ "If a government cooperated..."
- ❌ "One observes five documents..."
- ❌ "States cannot benefit..."

---

### Pattern 10: Circular Structure with Explicit Callback

**Rule:** Return to the opening in the conclusion with explicit framing.

**Examples:**
- ✅ "Let me bring this back to where we started."
- ✅ "When Guatemala assumes the ICJ will restore their sovereignty, they're ignoring three cases where colonial treaties stood despite breach claims—and 80 years of their own conduct accepting that boundary."

**Creates satisfying closure by:**
1. Explicit callback phrase
2. Reframing opening claims with evidence
3. Showing what both extremes miss

---

## SPEAKING STYLE CHECKLIST (Use When Writing/Editing Scripts)

Before finalizing any script, verify:

- [ ] All technical terms defined immediately in bold (same sentence)
- [ ] All quotes/complex language explained in next sentence ("In simpler terms...")
- [ ] No vague references (answer: what islands? how so? which case?)
- [ ] Key facts stated as short declaratives (hard stops for emphasis)
- [ ] Deliberate fragments used for rhythm where appropriate
- [ ] Dash-separated clarifications for immediate context
- [ ] Meta-framing explicit ("I'm citing...", "Let me show you...")
- [ ] Rhetorical questions followed by answers
- [ ] Direct address to audience ("you/your") not academic distance
- [ ] Circular structure with explicit callback to opening

---

---

## FACT-CHECKING DURING SCRIPT REVIEW (Updated 2025-01-27)

### ⚠️ MANDATORY: PRIMARY SOURCE VERIFICATION BEFORE FILMING

**CRITICAL RULE (Added 2025-01-27):**

**NEVER film scripts with legal/historical claims without NotebookLM verification of primary sources.**

**What happened:**
- Nicaragua v Colombia case mischaracterized in Belize ICJ script
- ICJ ruling said "no jurisdiction" - script said "ruled treaty valid"
- Material breach quote attributed to wrong case
- Error discovered AFTER filming 11 minutes of A-roll
- Required cutting section and re-filming pickup line

**Prevention protocol:**
1. **Before filming ANY script with court rulings, treaty provisions, or legal definitions:**
   - Upload primary sources to NotebookLM (actual court PDFs, treaty texts)
   - Run verification prompts (see `.claude/FACT-CHECK-VERIFICATION-PROTOCOL.md`)
   - Compare findings to script claims
   - Correct ANY discrepancies BEFORE filming

2. **Red flags requiring immediate verification:**
   - "The court ruled X..." → Ask: Which paragraph? Exact quote?
   - "The treaty says/requires..." → Ask: Which article? Exact language?
   - "Material breach/estoppel/legal term..." → Ask: Source? Definition?
   - Any quote without page number citation → Verify with primary source

3. **If Claude can't cite page numbers and paragraphs:** Claim is unverified - user must check with NotebookLM

**See full protocol:** `.claude/FACT-CHECK-VERIFICATION-PROTOCOL.md`

**Time investment:** 30-60 min per video
**Value:** Prevents hours of re-filming, protects channel credibility

**When to use:**
- Court rulings (ICJ, Supreme Court, any legal decision)
- Treaty provisions (specific articles, clauses)
- Legal definitions (material breach, estoppel, jurisdictional standards)
- Historical documents (what they actually say vs common interpretations)
- Case precedents (what court decided vs what parties claimed)

---

### User Catches Contradictions

**Example from Bir Tawil script:**
- Script said "No resources. Worthless."
- Script later mentioned "illegal gold mines"
- User caught: "you say its worthless but then you also mention that there´s gold mines?"

**Correct Response:**
1. Acknowledge the contradiction immediately
2. Propose accurate fixes with options
3. Make the edit when user chooses
4. Update version number

**What This Means:**
- User reviews scripts carefully for logical consistency
- Don't assume contradictions won't be noticed
- Fix must maintain factual accuracy
- "Economically worthless compared to Hala'ib" ≠ "No resources"

### Script Review Process

**User will:**
- Read scripts word-by-word
- Catch contradictions
- Identify unclear phrasing
- Request conversational rewrites
- Verify logic flows correctly

**You should:**
- Be ready to fix issues systematically
- Offer multiple fix options
- Maintain version control (4.0 → 4.1 → 4.2)
- Document what changed

---

## PROJECT STATUS TRACKING (Updated 2025-01-25)

### Don't Assume Video Status

**Critical Error Made:**
User said: "retard, i already made crusades, fuentes and sykes picot"

**The Mistake:**
- Looked at main PROJECT_STATUS.md (outdated)
- Assumed videos were still in production
- Suggested work on videos already filmed/published

**Correct Approach:**
- Crusades, Fuentes, Sykes-Picot = DONE (filmed/published)
- Bir Tawil = Research complete, ready for production
- Dark Ages, Industrial Revolution, Genocide = Concepts only

**Before suggesting work on a video:**
1. Check if project folder has FINAL-SCRIPT.md
2. Check if YOUTUBE-METADATA.md exists (sign of completion)
3. Ask user if uncertain about status
4. Don't rely solely on PROJECT_STATUS.md (can be outdated)

### Video Lifecycle Folders

Projects move through folders as they progress:
- `_IN_PRODUCTION/` - Active research/scripting
- `_READY_TO_FILM/` - Script finalized, ready to film
- `_ARCHIVED/` - Published or cancelled

Presence of certain files indicates status:
- `PROJECT-BRIEF.md` only = Concept stage
- `FINAL-SCRIPT.md` = Script complete
- `YOUTUBE-METADATA.md` = Ready to publish
- `EDITING-GUIDE.md` = In editing or done

---

## COMMENT-DRIVEN RESEARCH (New Pattern - 2025-01-25)

### YouTube Comments Can Drive New Videos

**User Pattern:**
"a lot of comments under my belize-guatemla video mention this. guatemala has claim to belize because the maya lived there before the british arrived seems to be the main argument. but please verify this"

**What This Means:**
- User monitors comments for recurring arguments
- Comments reveal what audience believes/misunderstands
- Fact-checking popular comment claims = potential follow-up videos

**Research Process:**
1. User identifies recurring comment argument
2. Verify what the argument claims
3. Check if it's actually true (Guatemala's ICJ arguments)
4. Document the gap between popular belief and reality
5. Create follow-up video concept ("Fact-Checking YouTube Comments")

**Example from This Session:**
- Comments claimed: "Guatemala has rights because Maya lived there first"
- Reality: Guatemala argues Spanish colonial inheritance at ICJ, NOT Maya heritage
- Video concept: "Fact-Checking YouTube: Does Maya Heritage Give Guatemala Rights to Belize?"
- Saved as: `12-guatemala-maya-claims-2025/PROJECT-BRIEF.md`

**When User Says "save this idea somewhere":**
- Create PROJECT-BRIEF.md in new folder
- Document the comment argument being fact-checked
- Include preliminary research findings
- Mark status as "CONCEPT SAVED"
- Note timing: "After original video gains traction"

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

## Batch Research Package Creation Workflow

### When User Wants Multiple Video Packages

**User Pattern:** "ok, do the next one" after each package
**What This Means:** Create complete research packages efficiently in batch

**Standard Package Structure (All 4 Files Required):**
1. `PROJECT-BRIEF.md` - VidIQ validation, expected views, timeline, positioning
2. `SCRIPT-OUTLINE.md` - Complete structure, retention triggers, B-roll requirements
3. `NOTEBOOKLM-SOURCE-LIST.md` - Tier 1-3 sources with URLs, download checklist
4. `NOTEBOOKLM-PROMPTS.md` - 13-15 prompts to extract information from sources

**Folder Naming:** `[number]-[topic-slug-year]/`
- Example: `9-communism-definition-2025/`, `10-dark-ages-2025/`

**Process:**
1. User provides VidIQ validation results for topic
2. Create folder in `video-projects/_IN_PRODUCTION/`
3. Write all 4 documents following proven templates
4. Mark todo complete
5. Wait for "ok next one" or provide summary

**Efficient Batch Creation:**
- No need to ask "should I continue?" - user will say "next one"
- Each package takes ~4 tool calls (mkdir + 3 writes for docs, PROJECT-BRIEF can be written first)
- Use TodoWrite to track package creation progress
- Provide brief summary after each completion

**Example Session:**
```
User: "save this information and start working on the research package for the communism video"
You: [Create all 4 docs for communism]
You: "Complete research package created for Communism..."

User: "ok, do the next one"
You: [Create all 4 docs for Dark Ages]
You: "Complete research package created for Dark Ages..."

User: "next one"
You: [Create all 4 docs for Industrial Revolution]
```

**Package Quality Standards:**
- Runtime: 6-8 minutes (660-880 words @ 110 wpm)
- Retention triggers: 8 (every 50-90 seconds)
- "Both extremes wrong" structure
- Primary sources displayed on screen (5-8 sec each)
- 90%+ fact-check verification target
- 6+ shorts identified with timestamps

**VidIQ Integration:**
- User validates topics with VidIQ BEFORE package creation
- Include VidIQ search volume in PROJECT-BRIEF
- Use VidIQ expected views data (conservative | breakout)
- Reference VidIQ positioning insights ("both extremes wrong" angle)

---

## Editing Guide Creation

### When User Provides A-roll Transcript + Script

**User Pattern:** "make the editing guide"
**What They Have:** Cut A-roll transcript (.srt), final script, sometimes original video to clip from

**User's Workflow:**
- **Desktop:** For heavy work (capturing clips from YouTube if needed, asset organization)
- **Laptop:** For editing while traveling (DaVinci Resolve)

**Editing Guide Must Include:**
1. **Shot-by-shot breakdown** - Exact timestamps from A-roll transcript
2. **Clip timestamps** - If referencing original video, provide timestamps from that video (NOT from A-roll)
3. **B-roll requirements** - What visuals go where
4. **Audio mixing specs** - Voice levels, music levels, when to fade
5. **Transition notes** - When to cut between talking head and B-roll

**CRITICAL: Clip Timestamps**
- User wants **TIMESTAMPS ONLY**, not captured clips
- Tell them: "Use clip from [original video] at [01:02:05:16 - 01:02:12:00]"
- They will capture clips themselves on desktop
- Format: `[HH:MM:SS:FF - HH:MM:SS:FF]` from original video

**Example:**
```
Shot 15 (0:25 in final video)
- Show Pax clip: "Turkish ships seized..."
- Clip timestamp: [01:02:05:16 - 01:02:12:00] from Pax video
- Audio: Duck music to -24dB during clip
- Transition: Fade to talking head at 0:32
```

---

## Shorts Strategy

### Long-Form First, Then Clip

**User's Workflow:**
1. Makes 6-8 minute long-form video
2. Uses **VidIQ clipping tool** to create shorts (under 2 min)
3. Does NOT make shorts separately

**Implications for Script Writing:**
- Identify 6+ "short clip points" in script outline
- Mark timestamps where shorts can be extracted
- Each short needs self-contained hook + payoff
- Include clip potential notes: "Clip #3: Medieval Inventions (3:30-4:00)"

**Short Characteristics:**
- 30-45 seconds ideal
- Self-contained (doesn't require watching full video)
- Surprising fact or data reveal
- Can be understood without context

---

## Quick Reference

**When user says:** "Make a thumbnail"
**You do:** Read script → Ask for VidIQ data → Provide specific Photoshop instructions

**When user says:** "Fix subtitles"
**You do:** Find .srt file → Read it → Fix all errors → Report corrections

**When user says:** "Create metadata"
**You do:** Find script → Read it → Generate complete metadata → Save to correct folder

**When user says:** "Make the editing guide"
**You do:** Read A-roll transcript + script → Create shot-by-shot breakdown with clip timestamps (not captured clips)

**When user says:** "ok, do the next one" (during batch package creation)
**You do:** Create next complete research package (all 4 docs) → Provide brief summary → Wait for next instruction

**When user gets frustrated:**
**You do:** Acknowledge → Immediately read context → Complete task → Move on

**Always:**
- Read context first
- Use Glob to find files
- Work in parallel when possible
- Be specific and direct
- Save to correct folders
- Minimize questions
- Batch create research packages efficiently

**Never:**
- Ask for information in files you can read
- Create vague recommendations
- Make loose folders in video-projects/
- Over-apologize
- Ask obvious questions
- Capture clips (provide timestamps only)
