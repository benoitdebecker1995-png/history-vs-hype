# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a content production repository for **History vs Hype**, a YouTube channel focused on evidence-based myth-busting about geopolitics, colonial history, border disputes, and ideological narratives. The channel uses academic research and primary sources to debunk historical myths that shape modern opinions, political beliefs, and territorial conflicts.

**Channel Stats:** 197 subscribers, 82K+ views, 590+ hours watch time, 30-35% average retention
**Target Audience:** Males 25-44, international (UK, Germany, Canada, US)
**Video Length:** As long as needed for topic (no arbitrary caps - optimize for watch time, not brevity)
**Format:** Hybrid talking head + B-roll evidence with real academic quotes

**Subscriber Trigger (VidIQ Validated Dec 2025):**
- Audience subscribes for "intellectual competence" - proving you understand SYSTEMS, not just narratives
- "How they deleted a country" (mechanism) > "Why they split" (politics)
- Logistics/legal/administrative angles outperform emotional/political angles for this demographic
- Overlap with RealLifeLore/Wendover audience (the "logistics of nations" crowd)

**Style Reference Models (Updated 2025-12-25):**
- **Kraut:** Deep causal chains, sweeping historical patterns, comparative analysis
- **Alex O'Connor (CosmicSkeptic):** Conversational authority, intellectual honesty, defining terms immediately
- **Knowing Better:** Forensic source verification, translation skepticism, steelmanning
- **Shaun:** Document-first argumentation, chronological precision
- **Fall of Civilizations:** Systems collapse framing, evidence stacking

**See:** `.claude/REFERENCE/STYLE-GUIDE.md` Part 5 (Creator Techniques) for detailed analysis

**Performance Insights:**
- Belize (10:57): 23,181 views, best performer = detailed territorial dispute
- JD Vance (6:16): 11.21% CTR, 42.6% retention = engagement efficiency benchmark
- Kraut's 30-45 min videos maintain strong engagement
- Strategy: Write as long as needed. Quality and completeness > arbitrary time targets

---

## Core Principles

1. **Historical integrity above all** - Every claim must be verified with credible sources
2. **Real quotes over summaries** - Word-for-word quotes from academic sources with page numbers (the competitive advantage)
3. **Modern relevance** - Connect historical events to current developments (2023-2025)
4. **Academic balance** - Present multiple perspectives, acknowledge counter-evidence (Alex O'Connor intellectual honesty)
5. **Deep causal chains** - Explain WHY things happened, not just WHAT (Kraut-style: "consequently," "thereby," "which meant that")
6. **No oversimplification** - Maintain nuance while being accessible

---

## Quick Start Commands

### Production Workflow
- `/new-video-verified` - Start new video with 3-phase verified workflow
- `/script` - Generate script from research
- `/fact-check` - Run academic peer review with simplification detection
- `/youtube-metadata` - Create optimized metadata (VidIQ auto-filtered)
- `/fix-subtitles` - Fix auto-transcription errors in .srt files

### Post-Publication & Engagement
- `/respond-to-comment` - Research and respond to YouTube comments with fact-checked answers
- `/publish-correction` - Document and publish corrections for post-publication errors
- `/save-comment` - Save insightful comments for future research or video ideas

### Analysis & Tools
- `/extract-claims` - Extract claims from YouTube transcript for fact-checking
- `/edit-guide` - Generate shot-by-shot visual staging guide + B-roll download links
- `/zero-budget-assets` - Create DIY B-roll guide with free tools
- `/evaluate-feedback` - Evaluate external optimization feedback against channel values

### Optimization & Testing (NEW)
- `/test-titles` - Generate 5-10 title variants for VidIQ A/B testing
- `/clip-suggestions` - Identify 3-5 clip-worthy moments for Shorts/TikTok

**For comprehensive workflow:** See `START-HERE.md`

---

## File Organization (CRITICAL)

### Project Lifecycle Folders

**All video projects MUST be in lifecycle folders:**

- **`video-projects/_IN_PRODUCTION/`** - Active research and scripting
- **`video-projects/_READY_TO_FILM/`** - Finalized scripts ready for filming
- **`video-projects/_ARCHIVED/`** - Published or cancelled projects

**NEVER create loose folders in `video-projects/` root**

**Naming convention:** `video-projects/[lifecycle]/[number]-[topic-slug-year]/`

Example: `video-projects/_READY_TO_FILM/1-sykes-picot-2025/`

### Before Creating Any File

1. Read `PROJECT_STATUS.md` to understand current state
2. Use Glob to find existing project folder
3. Confirm folder is in correct lifecycle stage
4. Verify you're not creating a loose folder in root
5. Use exact path from Glob results
6. Save with standard naming convention

**See:** `.claude/FOLDER-STRUCTURE-GUIDE.md` for complete folder system rules

### Standard Files Within Projects

**Research & Development:**
- `01-VERIFIED-RESEARCH.md` - Single source of truth for verified facts
- `02-SCRIPT-DRAFT.md` - Production-ready script
- `03-FACT-CHECK-VERIFICATION.md` - Final quality gate before filming
- `PROJECT-STATUS.md` - Track progress

**Production Ready:**
- `FINAL-SCRIPT.md` - The one to film from
- `YOUTUBE-METADATA.md` - Title, description, tags, timestamps
- `B-ROLL-CHECKLIST.md` - Visual requirements
- `FACT-CHECK-VERIFICATION-SPREADSHEET.md` - Source verification
- `EDITING-GUIDE-SHOT-BY-SHOT.md` - Visual staging

**Post-Production:**
- `*.srt` - Subtitle files (often need fixing for name/timestamp errors)

---

## Research Workflow: Two-Phase Approach (CRITICAL)

**This is the channel's competitive advantage.** Other history YouTubers stop at internet research. You go deeper with academic sources.

### Phase 1: Preliminary Internet Research
**Purpose:** Map the landscape and identify claims to verify

**Sources:**
- Wikipedia (for basic timeline)
- News articles (for modern relevance)
- Academic websites (.edu domains)
- Google Scholar (previews, not full texts yet)

**Output:**
- Preliminary findings (all marked ❓)
- List of claims that need academic verification
- Understanding of the debate landscape

**Time:** 2-4 hours | **Cost:** Free

### Phase 2: NotebookLM Academic Verification
**Purpose:** Verify claims and get proper citations with academic sources

**Academic Quality Standards (UPDATED 2025-12-31):**
- **University press publications ONLY** - Cambridge, Oxford, Chicago, Harvard, Yale, etc.
- **Top-tier scholars** - Leading authorities (endowed chairs, major universities)
- **Critical editions** - Primary sources with scholarly apparatus
- **Price is NOT a constraint** - Budget is UNLIMITED for quality academic sources

**Sources:**
- Academic monographs from university presses ($40-60 each)
- Primary documents in critical editions (full text with commentary)
- Peer-reviewed journal articles (full PDFs)
- NO popular history unless supplementary

**NotebookLM Features to Leverage (Gemini 2.0 Flash):**
- **2M token context window** - Upload all 20+ sources simultaneously
- **Customized Audio Overviews** - Click "Customize" before generating, give specific instructions to AI podcast hosts
- **Interactive Mode** - Talk with podcast hosts in real-time to clarify points
- **Citation Grounding** - Every answer includes clickable citations to exact page numbers
- **Study Guides** - Generate for dense 500+ page academic texts
- **Save to Notes** - Pin responses and build VERIFIED-RESEARCH.md incrementally

**Process:**
1. Create NOTEBOOKLM-SOURCE-LIST.md identifying specific books to download
2. Download 10-20 academic sources (use university library + purchases as needed)
3. Upload to NotebookLM with organized naming: `[P1] Source-Name.pdf`, `[A1] Author-Book.pdf`
4. Generate **customized audio overviews** for each notebook (Act 1, Act 2, Act 3)
5. Run targeted chat prompts to verify specific claims
6. Click citation links to get exact page numbers
7. Use Interactive Mode to clarify confusing points
8. Save verified quotes to notes

**Output:**
- Verified statistics with academic sources and page numbers
- Proper citations: "According to Chris Wickham in *The Inheritance of Rome*, page 147..."
- Primary source quotes ready for on-screen display
- Academic authority competitors lack

**Time:** 1-2 weeks (source download + NotebookLM research) | **Cost:** Unlimited (buy what you need)

**See:** `.claude/REFERENCE/NOTEBOOKLM-SOURCE-STANDARDS.md` for complete NotebookLM best practices

### Why Both Phases Matter

**Competitor approach (Phase 1 only):**
"During the Dark Ages, literacy declined significantly according to historians..."

**Your approach (Phase 1 + Phase 2):**
"According to William V. Harris in *Ancient Literacy*, Roman literacy was around 10-15%. Chris Wickham's *The Inheritance of Rome* shows Early Medieval literacy dropped to 1-5%. Here's a Carolingian manuscript from 800 CE proving monks preserved classical texts..."

**NEVER skip Phase 2.** That's what makes your channel different.

---

## Verified Workflow (3-Phase System)

**The Problem:** Old workflow led to errors (Fuentes script had 2 errors, wasted 3 hours rewriting)

**The Solution:** Verify facts BEFORE writing, not after

### PHASE 1: Research + Verification (Simultaneous)
**File:** `01-VERIFIED-RESEARCH.md` (single source of truth)

As you research with NotebookLM, immediately verify each fact:
- ✅ VERIFIED - Ready to use in script
- ⏳ RESEARCHING - Still checking sources
- ❌ UNVERIFIABLE - Don't use

**Quality Gate:** Can't proceed to Phase 2 until 90%+ claims verified

### PHASE 2: Script Writing (From Verified Facts Only)
**File:** `02-SCRIPT-DRAFT.md`

**Rule:** ONLY use facts from `01-VERIFIED-RESEARCH.md`

If you need a fact that's not verified → STOP → Go verify it first

**Self-Check Before Calling "Final":**
- Every fact references VERIFIED-RESEARCH.md
- No claims without verification
- All quotes exact word-for-word
- All numbers match verified table
- Read out loud - no awkward phrasing

### PHASE 3: Final Verification (Cross-Check)
**File:** `03-FACT-CHECK-VERIFICATION.md`

Cross-check every line of script against VERIFIED-RESEARCH.md

**Verdict:** ✅ APPROVED FOR FILMING or ❌ NEEDS REVISION

**Time Savings:** 5.5 hours (new) vs. 9 hours (old) = 39% faster with zero errors

---

## Script Writing Guidelines

**Authoritative Reference:** `.claude/REFERENCE/STYLE-GUIDE.md`

### Quick Summary

**Core Non-Negotiable:** Scripts are read aloud via teleprompter. They must sound natural when spoken.

**Voice:** "Calm Prosecutor" - emotionally low, intellectually high. Evidence-based referee between opposing camps.

**Key Rules:**
- Real quotes with page numbers (not summaries)
- Primary sources displayed ON SCREEN
- Define every term immediately
- "Here's" usage: 2-4 per script max
- Contractions: "it's" not "it is"
- Dates: "On June 16th, 2014" not "June 16, 2014"

**Creator Models:** Kraut (causal chains), Alex O'Connor (intellectual honesty), Shaun (document-first), Knowing Better (source verification)

**For complete style rules, voice patterns, and quality checklist, see [STYLE-GUIDE.md](.claude/REFERENCE/STYLE-GUIDE.md).**

### Structure
- Videos as long as needed (no arbitrary caps)
- Modern relevance connection every 90 seconds
- Pattern interrupt every 2-3 minutes
- Deep causal chains throughout (explain WHY, not just WHAT)
- Payoff-first: show modern consequences before explaining historical causes
- Use academic framing language, not political punditry

### Language to Avoid
- "X is occupying Y" → "X's military presence has fueled nationalist opposition"
- "Z destroyed the culture" → "Z's policies fragmented traditional systems while..."
- Absolutist language ("all historians agree," "always," "never")
- Conspiracy framing without documentation

### Required Elements
- Every major claim has word-for-word quote with page number
- Statistics are specific and sourced (real quotes, not summaries)
- Counter-evidence is acknowledged (Alex O'Connor intellectual honesty)
- Complexity is maintained (not oversimplified)
- Deep causal chains explaining mechanisms (Kraut-style)
- Conclusion emphasizes why accurate history matters

---

## Fact-Checking Requirements

### Source Hierarchy (Tier 1 = Most Reliable)

**Tier 1:**
1. Primary documents (treaties, census data, government archives)
2. Peer-reviewed academic publications (prioritize 2010-present)
3. Expert historians specializing in the topic

**Tier 2:**
4. Respected journalists with expertise
5. International organization reports
6. Declassified government documents (with context about bias)

**Tier 3:**
7. Credible news sources (for modern events, verify with multiple sources)
8. Documentary evidence (verify authenticity and context)

### Modern Consensus Priority (2010-Present)
- For secondary scholarship: prioritize 2010-present sources
- Pre-2010 classic works: Note as "foundational" and verify against recent scholarship
- Primary sources: Timeless (no recency check needed)

### Pre-Production Checklist
- [ ] Every number has a source
- [ ] Every quote verified from original
- [ ] Contested claims clearly labeled
- [ ] At least 2 sources for each major point
- [ ] No logical fallacies in arguments
- [ ] **Simplification check complete** (all 🔴 CRITICAL flags resolved)
- [ ] Territorial claims have specific boundaries/percentages
- [ ] Present-tense statements have temporal accuracy
- [ ] Attributions have specific sources (timestamp, document, date)

### CRITICAL: NEVER Include Unverified Claims

**What Counts as Verified:**
- ✅ Video timestamp: "In his 2019 video at 3:45..."
- ✅ Tweet with date: "April 16, 2025 tweet..."
- ✅ Court document: "In court filing 21-CR-175..."
- ✅ Published interview: "During BBC interview on [date]..."

**What Does NOT Count:**
- ❌ "Fuentes has claimed..." (when? where?)
- ❌ "January 6 defendants cited Founding Fathers in court" (which defendants? which cases?)
- ❌ "He said X" (find the actual quote with source)

**If You Can't Verify:**
1. Don't include it - better to leave out than get wrong
2. Flag it: "NEEDS VERIFICATION: [claim]"
3. Ask user: "Do you have source for [specific claim]?"

**NEVER assume something is true because it sounds plausible.**

### Primary Source Verification Before Filming

**MANDATORY for scripts with legal/historical claims:**

Before filming ANY script with court rulings, treaty provisions, or legal definitions:
1. Upload primary sources to NotebookLM (actual court PDFs, treaty texts)
2. Run verification prompts
3. Compare findings to script claims
4. Correct ANY discrepancies BEFORE filming

**Red flags requiring immediate verification:**
- "The court ruled X..." → Ask: Which paragraph? Exact quote?
- "The treaty says/requires..." → Ask: Which article? Exact language?
- "Material breach/estoppel/legal term..." → Ask: Source? Definition?
- Any quote without page number citation → Verify with primary source

**Time investment:** 30-60 min per video
**Value:** Prevents hours of re-filming, protects channel credibility

**See:** `.claude/REFERENCE/fact-checking-protocol.md` for complete process

---

## Visual Source Presentation (Channel Differentiator)

**The channel's core differentiator:** Showing primary sources ON SCREEN, not just citing them verbally.

### Why This Matters

**Most history channels:**
- Narrator: "Historians say the USSR grew rapidly"
- B-roll: Stock footage of factories, generic historical images
- Problem: Viewer must trust narrator

**This channel:**
- Narrator: "Robert Allen analyzed Soviet GDP data showing 4.1x growth 1928-1970"
- B-roll: Display the actual GDP statistical table Allen used
- Result: Viewer sees the evidence, can evaluate the interpretation themselves

**This is "democratizing historical methodology":**
- Academics read primary sources in archives → You show them on screen
- Academics cite evidence in footnotes → You display evidence as B-roll
- Academics allow peer review → Viewers can verify claims visually

### Talking Head vs. B-Roll Strategy

**Talking Head Usage (60-70% of video):**
- Making arguments and interpretations
- Explaining causation
- Connecting historical events
- Asking rhetorical questions
- Building narrative
- Emotional emphasis

**B-Roll Usage (30-40% of video):**
- **Maps (15-20%):** Geographic boundaries, territorial expansion, maritime zones
- **Primary sources (10-15%):** Treaty documents, diplomatic correspondence, official proclamations
- **Historical photos (5-10%):** Key figures, historical events, archaeological sites
- **Modern footage (5%):** Current events, news headlines, contemporary scenes

**The Golden Rule:** If the B-roll doesn't make your argument stronger, stay on camera.

B-roll is evidence, not decoration. You are the authority making an argument, not just a narrator.

**See:** `.claude/REFERENCE/HYBRID_TALKING_HEAD_GUIDE.md` for visual planning details

---

## YouTube Metadata & Publishing

### Title Requirements (Non-Clickbait, Documentary Tone)
- **60-70 characters** - Mobile-friendly length
- **Factually accurate** - Don't claim things that didn't happen
- **Explicit about sensitive topics** - Use "Holocaust" if relevant, don't hide from subject
- **NOT clickbait** - NOT "You won't BELIEVE..." or "SHOCKING..."

**Examples:**
- ✅ "Fact-Checking Nick Fuentes: Claims Tucker Didn't Raise"
- ❌ "Nick Fuentes Told Tucker 'No Evidence' – Here Are the Nazi Documents" (clickbait-y)

### Description Structure
1. First 3 lines = Hook (what happened, what you're fact-checking)
2. Document explanations (what each primary source shows)
3. Timeline sections (for historical claims)
4. "Why this matters" conclusion
5. **Full source citations** with archival references
6. Additional resources (museums, archives, academic sources)

### Tags
- 15-20 tags
- Comma-separated format (ready to paste into YouTube)
- Include: person names, topic keywords, fact-checking terms, document names

### Chapters
- Extract from SRT file timestamps
- Clear, descriptive chapter names

### VidIQ Integration
- VidIQ helps with keywords, thumbnail concepts, optimization
- Balance VidIQ suggestions with documentary tone requirements
- Create complete package in `YOUTUBE-METADATA.md`

### Publishing
- Create thumbnail in Photoshop (documentary style, evidence-focused)
- Upload during optimal windows (Tuesday-Thursday, 9-11 AM EST)
- Monitor comments for first 24 hours

---

## Working Style & User Preferences

### Communication Style
- **Be direct and efficient** - No unnecessary pleasantries, get straight to the point
- **Read first, ask later** - If user mentions a file exists, find and read it BEFORE asking questions
- **Use parallel tool calls** - When multiple independent reads/searches are needed, do them simultaneously
- **Find files autonomously** - Use Glob to locate files instead of asking

### Common Mistakes to Avoid
1. **Asking for information in files you can read** - Use Glob/Read to find it yourself
2. **Creating loose folders in video-projects/** - Always use lifecycle folders
3. **Not checking existing video database** - Search COMPLETE-PERFORMANCE-DATABASE.md before suggesting topics
4. **Including unverified claims** - Every attribution needs specific source

### When User Gets Frustrated
**Signs:** Direct language, pointing out obvious context you should have seen

**Response:**
1. Acknowledge: "You're right, let me read the script"
2. Immediately fix: Use tools to get the information
3. Complete task: Do what was asked
4. Don't over-apologize: User wants results, not apologies

**See:** `.claude/USER-PREFERENCES.md` for complete working style guide

---

## Tool Stack

- **VidIQ Pro** - Topic research, script generation, clipping tool
- **NotebookLM (Gemini 2.0 Flash)** - Source-grounded academic research
  - 2M token context window (50 sources, 25M words total)
  - Customized Audio Overviews with Interactive Mode
  - Citation grounding with clickable page numbers
  - Study guides for dense academic texts
  - Multi-format upload (PDF, audio, URL, Google Drive)
- **DaVinci Resolve** - Video editing
- **Photoshop** - Thumbnail creation
- **Claude Code** - Fact-checking, research, scripting assistance

---

## Key Documentation Files

**Quick Start:**
- `START-HERE.md` - Quick start guide and file overview
- `VERIFIED-WORKFLOW-QUICK-REFERENCE.md` - One-page workflow with checklists

**Core Workflows:**
- `.claude/REFERENCE/fact-checking-protocol.md` - Source hierarchy and verification process

**Style:**
- `.claude/REFERENCE/STYLE-GUIDE.md` - **Authoritative style reference** (voice, delivery, patterns, checklist)
- `.claude/REFERENCE/OPENING-HOOK-TEMPLATES.md` - Opening templates
- `.claude/REFERENCE/CLOSING-SYNTHESIS-TEMPLATES.md` - Closing templates

**Reference:**
- `.claude/REFERENCE/FOLDER-STRUCTURE-GUIDE.md` - Complete folder system rules
- `.claude/USER-PREFERENCES.md` - Working style, efficiency expectations, common tasks
- `.claude/REFERENCE/HYBRID_TALKING_HEAD_GUIDE.md` - Visual strategy for when to show face vs. B-roll
- `.claude/REFERENCE/youtube-comment-response-guide.md` - Voice, tone, and response templates

**Advanced:**
- `.claude/ACADEMIC-PEER-REVIEW-PROTOCOL.md` - Journal-level verification for high-stakes topics
- `YOUTUBE-TRANSCRIPT-SETUP.md` - Extract claims from competitor videos

**Quality Control:**
- `.claude/FACT-CHECK-SIMPLIFICATION-RULES.md` - 8 rules to prevent oversimplification errors
- `.claude/VERIFIED-CLAIMS-DATABASE.md` - Reusable fact-checked claims across videos
- `.claude/VIDIQ-CHANNEL-DNA-FILTER.md` - Auto-filter VidIQ suggestions for documentary tone

**Post-Publication:**
- `video-projects/_CORRECTIONS-LOG.md` - Track errors and lessons learned
- `.claude/FACT-CHECK-IMPROVEMENTS.md` - System improvements from discovered errors
- `channel-data/saved-comments/` - Valuable viewer feedback organized by category

---

## Specialized Agents

**Available via Task tool:**

- `video-orchestrator` - Coordinates full workflow from topic to finished script
- `script-writer-v2` - Writes retention-optimized scripts using Kraut/Alex O'Connor style patterns with real quotes
- `structure-checker-v2` - Analyzes scripts for retention issues, predicts dropout points
- `fact-checker` - Verifies sources using tier-based system
- `claims-extractor` - Extracts factual claims from transcripts for systematic fact-checking
- `diy-asset-creator` - Creates zero-budget DIY guides for B-roll assets

**See:** `.claude/agents/` for complete agent documentation

---

## Performance Insights

### What Works

**VidIQ Validated Performance Data (2025-12-04):**

| Content Type | Performance | Views | Example |
|--------------|-------------|-------|---------|
| Territorial disputes | **12x baseline** | 1,905 | Essequibo |
| Political figure fact-checks | 1x baseline | 936 | JD Vance |

| Thumbnail Type | VidIQ Score | Actual Views | Performance |
|----------------|-------------|--------------|-------------|
| Map-focused | 72 | 1,905 | **26x better** |
| Face-focused | 85+ | ~73 | Baseline |

**Key insight:** VidIQ scores don't predict this channel's performance. 83-scored title got 21x more views than 97-scored title.

**What performs:**
- Territorial disputes with modern news hooks (Essequibo: 1.9K views, 19 new subs)
- Political fact-checking (JD Vance: 936 views)
- Historical political myths
- Modern relevance connections
- Evidence-based approach
- Strong retention (30-35% is excellent for 8-12 min educational videos)
- Map/evidence thumbnails (despite lower VidIQ scores)

### Topic Formula

**Territorial:** "[Colonial/Historical Decision] from [X] years ago is still [causing deaths/conflicts/disputes] today"

**Ideological:** "[Historical myth] is still shaping [modern political belief/debate/movement] today"

**Examples:**
- Territorial: "Sykes-Picot from 1916 is still causing Middle East conflicts today"
- Ideological: "The 'Dark Ages' myth is still shaping narratives about Western civilization today"
- Ideological: "The 'Crusades were defensive' claim is still justifying religious conflict narratives today"

### Outlier-Validated Topic Patterns (Dec 2025)

**Pattern 1: "The Map They Ignored"** (9-10x outlier potential)
- Show the document/map that existed BEFORE the current borders
- Contrast: "This is what [power] agreed to. This is what they drew instead."
- Example: "The 1919 King-Crane Commission Map vs. Sykes-Picot"
- Why it works: Visual "what if" grounded in real documents, not speculation

**Pattern 2: "Legal Fiction Exposed"** (4-7x outlier potential)
- Focus on active legal disputes with economic consequences TODAY
- Show the treaty clause, court filing, or legal status
- Example: "Antarctica: The Treaty Clause That Expires in 2048"
- Why it works: Appeals to educated professionals, concrete stakes

**Pattern 3: "The Specific Site"** (4x outlier potential)
- Instead of broad topic, focus on ONE location as microcosm
- Example: One disputed church, one border crossing, one treaty line
- Why it works: Specificity beats broad. "The Temple Mount's Legal Status" > "Middle East conflicts"

**Pattern 4: "Deadline Approaching"** (High urgency)
- Treaties expiring, votes happening, cases being decided
- Example: "Belize-Guatemala: The 2027 ICJ Ruling"
- Why it works: Creates natural urgency without clickbait

**Patterns to AVOID (VidIQ suggests, but violates channel DNA):**
- ❌ "Secret" / "Hidden" / "They don't want you to know" (clickbait language)
- ❌ News-first framing ("Why [Country] Just Did X")
- ❌ Current politician as main subject
- ❌ Speculative "what if" without documentary evidence

### Channel DNA: History-First, Not Geopolitics-First

**The Core Principle:** This is a history channel with modern relevance, NOT a geopolitics channel with historical background.

**What this means:**
- ✅ Historical sources/events = the core content (60-80%)
- ✅ Modern relevance = the hook and stakes (20-40%)
- ❌ NOT: current events as the main subject with history as background
- ❌ NOT: news commentary that happens to mention history
- ❌ NOT: centered on current politicians or political figures

**The right balance:**
- "This medieval manuscript shows X, and that myth still shapes how people think about Y today" ✅
- "This 1859 treaty created a dispute that's being decided by the ICJ right now" ✅
- "Here's what Netanyahu said last week, and here's some historical context" ❌
- "Breaking down the latest ICJ ruling with some history" ❌

**Good fit - Territorial (history → modern conflicts):**
- Bir Tawil: "Why is this land unclaimed?" (colonial border decisions → ongoing paradox)
- Sykes-Picot: "How did colonial borders create Middle East conflicts?" (1916 treaty → ongoing consequences)
- Belize-Guatemala: "What do ICJ precedents tell us?" (legal history → 2027 ruling)

**Good fit - Ideological (historical myths → modern beliefs):**
- Library of Alexandria: "Did one fire destroy all ancient knowledge?" (ancient sources → "religion vs science" debates)
- Dark Ages: "Was Europe really backward for 1,000 years?" (medieval manuscripts → Western civilization narratives)
- Crusades: "Were Crusades defensive?" (primary chronicles → modern religious conflict framing)
- Communism definition: "What does communism actually mean?" (historical texts → political debate)

**Poor fit (news-first or political figure centered):**
- Netanyahu's current border policies (politician's statements as main subject)
- "What the latest ICJ ruling means" (news commentary)
- Trump's border wall plans (temporary political issue)

**Test 1:** Ask "Is the historical source/event the main content, or just background for current events?" If the latter, wrong balance.

**Test 2:** Ask "Will this question matter in 10 years regardless of who's in power?" If yes, good fit. If no, too politically specific.

**Hook Strength Test:** Ask "What modern belief, movement, or debate does this myth currently fuel?" The stronger the connection to active discourse, the better the topic.

---

## Channel Mission

Make academic research accessible while maintaining historical integrity. The goal is not entertainment or political commentary, but evidence-based education that reveals how distorted history fuels present-day conflicts AND modern ideological beliefs.

**Core insight:** Bad history does work in the present. People use historical myths to justify territorial claims, political movements, religious narratives, and ideological positions. This channel corrects the record with primary sources.

**Quality over quantity, always.**

---

## Critical Reminders

1. **NEVER skip Phase 2 (NotebookLM research)** - That's the competitive advantage
2. **ACADEMIC SOURCES ONLY** - University presses (Cambridge, Oxford, Chicago, Harvard), top scholars, critical editions. Price is NOT a constraint (budget is UNLIMITED)
3. **Use REAL QUOTES, not summaries** - Word-for-word from academic sources with page numbers from NotebookLM citations
4. **Primary sources are NON-OPTIONAL** - Showing documents on screen sets the channel apart
5. **Videos as long as needed** - No arbitrary length caps (Kraut runs 30-45 min)
6. **Read STYLE-GUIDE.md before writing scripts** - Authoritative voice, delivery, patterns, checklist
7. **Write for spoken delivery** - Conversational tone, contractions, natural phrasing
8. **Deep causal chains** - Explain WHY things happened (consequently, thereby, which meant that)
9. **Intellectual honesty** - Acknowledge what opposing side gets right (Alex O'Connor style)
10. **Single source of truth** - 01-VERIFIED-RESEARCH.md, not multiple conflicting documents
11. **Quality gates prevent progression** - Can't write until 90% verified, can't film until 100% cross-checked
12. **Use NotebookLM features** - Customized Audio Overviews, Interactive Mode, citation links for page numbers
13. **Filter external feedback through channel DNA** - Documentary tone over generic YouTube optimization
14. **Run simplification detection on ALL scripts** - Territorial claims need boundaries, present-tense needs temporal accuracy
15. **Check VERIFIED-CLAIMS-DATABASE before researching** - Avoid re-researching same facts across videos
16. **Document corrections systematically** - Use /publish-correction for post-publication errors
17. **HOW > WHY for subscriber growth** - Show mechanisms/logistics, not just political reasons
18. **Academic-level sources for NotebookLM** - See `.claude/REFERENCE/NOTEBOOKLM-SOURCE-STANDARDS.md`

---

## For More Information

- Slash command definitions: `.claude/commands/`
- Skill documentation: `.claude/skills/`
- Agent configurations: `.claude/agents/`

**New (Dec 2025):**
- **Style Guide (authoritative):** `.claude/REFERENCE/STYLE-GUIDE.md`
- VidIQ workflow: `.claude/VIDIQ-WORKFLOW.md`
- Topic ideas pipeline: `.claude/OUTLIER-TOPIC-IDEAS.md`
- Source standards: `.claude/NOTEBOOKLM-SOURCE-STANDARDS.md`
- Creator transcripts: `transcripts/` (Kraut, Knowing Better, Shaun, etc.)
- **Competitor title database:** `channel-data/COMPETITOR-TITLE-DATABASE.md` (title formulas, VidIQ analysis)
- **Script structure analysis:** `channel-data/SCRIPT-STRUCTURE-ANALYSIS.md` (opening formulas, transcript breakdowns)
- **YouTube transcript extractor:** `get-transcript.py` (automatic transcript fetching)

**Ready to create your next video?** Start with `/new-video-verified`
