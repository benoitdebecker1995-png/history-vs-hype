# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a content production repository for **History vs Hype**, a YouTube channel focused on evidence-based myth-busting about geopolitics, colonial history, and border disputes. The channel uses academic research and primary sources to debunk historical myths with modern political relevance.

**Channel Stats:** 197 subscribers, 82K+ views, 590+ hours watch time, 30-35% average retention
**Target Audience:** Males 25-44, international (UK, Germany, Canada, US)
**Video Length:** **6-8 minutes** (default for best engagement), 8-10 minutes for complex topics
**Format:** Hybrid talking head + B-roll evidence

**Performance Insights (Updated 2025-01-19):**
- Shorter videos (6-8 min) achieve higher CTR and retention per minute
- JD Vance (6:16): 11.21% CTR, 42.6% retention = efficiency benchmark
- Venezuela (10:33): 4.31% CTR, 36.5% retention (more views but lower engagement)
- Strategy: Default to concise, extend only when topic demands deeper explanation

## Core Principles

1. **Historical integrity above all** - Every claim must be verified with credible sources
2. **Evidence over opinion** - Show primary sources, not just text overlays
3. **Modern relevance** - Connect historical events to current developments (2023-2025)
4. **Academic balance** - Present multiple perspectives, acknowledge counter-evidence
5. **No oversimplification** - Maintain nuance while being accessible

## Content Production Workflow

### 1. Topic Selection
- Use VidIQ for trend analysis
- Focus on "colonial borders still killing people" angle
- Prioritize topics with modern news hooks

### 2. Script Development
- VidIQ generates initial draft
- Enhance with Claude Pro for better hooks and flow
- Script structure: Hook (0-0:45) → Context (0:45-2:00) → Deep-dive (2:00-8:00) → Modern connections (8:00-10:00) → CTA (10:00-12:00)

### 3. Fact-Checking (CRITICAL - UPDATED 2025-01-20)
- Every factual claim needs 2+ sources
- **Attributions require SPECIFIC sources** (video timestamp, tweet date, court filing)
- ❌ NEVER write "[Person] claimed X" without verifiable source
- ❌ NEVER assume something is true because it sounds plausible
- Academic sources prioritized
- Document all sources for citation
- **For fact-check videos**: Every claim about what someone said/did MUST have exact source
- See `fact-checking-protocol.md` for full process
- See `.claude/USER-PREFERENCES.md` section "NEVER INCLUDE UNVERIFIED CLAIMS"

### 4. Production
- Record talking head footage (multiple takes)
- Edit in DaVinci Resolve
- Add B-roll strategically (evidence, not decoration)
- Hybrid format: 60-70% talking head, 15-20% maps, 10-15% primary sources

### 5. YouTube Metadata & Publishing (UPDATED 2025-01-20)

**Title Requirements:**
- **Non-clickbait, documentary tone** - NOT "You won't BELIEVE..." or "SHOCKING..."
- **60-70 characters** - Mobile-friendly length
- **Factually accurate** - Don't claim things that didn't happen
- **Explicit about sensitive topics** - Use "Holocaust" if relevant, don't hide from subject
- **Examples:**
  - ✅ "Fact-Checking Nick Fuentes: Claims Tucker Didn't Raise"
  - ❌ "Nick Fuentes Told Tucker 'No Evidence' – Here Are the Nazi Documents" (clickbait-y)

**Description Structure:**
1. First 3 lines = Hook (what happened, what you're fact-checking)
2. Document explanations (what each primary source shows)
3. Timeline sections (for historical claims)
4. "Why this matters" conclusion
5. **Full source citations** with archival references
6. Additional resources (museums, archives, academic sources)

**Chapters:**
- Extract from SRT file timestamps
- Clear, descriptive chapter names

**Tags:**
- 15-20 tags
- Comma-separated format (ready to paste into YouTube)
- Include: person names, topic keywords, fact-checking terms, document names

**Workflow:**
- VidIQ helps with keywords, thumbnail concepts, optimization
- Balance VidIQ suggestions with documentary tone requirements
- Create complete package in `YOUTUBE-METADATA.md`

**Publishing:**
- Create thumbnail in Photoshop (documentary style, evidence-focused)
- Upload during optimal windows (Tuesday-Thursday, 9-11 AM EST)
- Monitor comments for first 24 hours

## Key Documentation Files

- **START-HERE.md** - Quick start guide and file overview
- **README.md** - Channel overview and directory structure
- **workflow-and-tools.md** - Complete production workflow and tool usage
- **History-vs-Hype_Master-Project-Template.md** - Comprehensive project template with NotebookLM prompts
- **fact-checking-protocol.md** - Source hierarchy and verification process
- **HYBRID_TALKING_HEAD_GUIDE.md** - Visual strategy for when to show face vs. B-roll
- **youtube-comment-response-guide.md** - Voice, tone, and response templates
- **analytics-and-strategy.md** - Performance data and growth strategy
- **sources-reference.md** - Academic library organized by topic
- **topics-list.md** - Video ideas and research links

## Research Workflow: Two-Phase Approach (CRITICAL - Updated 2025-01-25)

**This is the channel's competitive advantage.** Other history YouTubers stop at internet research. You go deeper with academic sources.

### Phase 1: Preliminary Internet Research
**Purpose:** Map the landscape and identify claims to verify

**Sources:**
- Wikipedia (for basic timeline)
- News articles (for modern relevance)
- Academic websites (.edu domains)
- Google Scholar (previews, not full texts yet)

**Output:**
- RESEARCH-SUMMARY.md with preliminary findings (all marked ❓)
- List of claims that need academic verification
- Understanding of the debate landscape

**Time:** 2-4 hours
**Cost:** Free

### Phase 2: NotebookLM Academic Verification
**Purpose:** Verify claims and get proper citations with academic sources

**Sources:**
- Academic books (download via university library or purchase)
- Primary documents (full text)
- Scholarly articles (full PDFs)

**Process:**
1. Create NOTEBOOKLM-RESEARCH-PLAN.md identifying specific books to download
2. Download 10-20 sources (prioritize free primary docs, 1-3 key academic books)
3. Upload to NotebookLM (max 50 sources per notebook, 25M words total)
4. Run targeted prompts to verify preliminary findings
5. Extract proper citations with page numbers
6. Get smoking gun quotes for B-roll

**Output:**
- Verified statistics with academic sources
- Proper citations: "According to Chris Wickham in *The Inheritance of Rome*, page 147..."
- Primary source quotes ready for on-screen display
- Academic authority competitors lack

**Time:** 1-2 weeks (source download + NotebookLM prompts)
**Cost:** $0-200 (university library + selective purchases)

### Why Both Phases Matter

**Competitor approach (Phase 1 only):**
"During the Dark Ages, literacy declined significantly according to historians..."

**Your approach (Phase 1 + Phase 2):**
"According to William V. Harris in *Ancient Literacy*, Roman literacy was around 10-15%. Chris Wickham's *The Inheritance of Rome* shows Early Medieval literacy dropped to 1-5%. Here's a Carolingian manuscript from 800 CE proving monks preserved classical texts..."

**Result:** You can cite specific books with page numbers, show primary sources on screen, and provide academic depth that builds trust and authority.

**NEVER skip Phase 2.** That's what makes your channel different.

## Script Writing Guidelines

### Structure
- 100-110 words per minute pacing
- Engagement trigger every 2 minutes
- Payoff-first: show modern consequences before explaining historical causes
- Use academic framing language, not political punditry

### Language to Avoid
- "X is occupying Y" → "X's military presence has fueled nationalist opposition"
- "Z destroyed the culture" → "Z's policies fragmented traditional systems while..."
- Absolutist language ("all historians agree," "always," "never")
- Conspiracy framing without documentation

### Required Elements
- Every major claim has source attribution
- Statistics are specific and sourced
- Counter-evidence is acknowledged
- Complexity is maintained (not oversimplified)
- Conclusion emphasizes why accurate history matters

## Fact-Checking Requirements

### Source Hierarchy (Tier 1 = Most Reliable)
1. Primary documents (treaties, census data, government archives)
2. Peer-reviewed academic publications
3. Expert historians specializing in the topic
4. Respected journalists with expertise
5. International organization reports
6. Declassified government documents (with context about bias)

### Pre-Production Checklist
- [ ] Every number has a source
- [ ] Every quote verified from original
- [ ] Contested claims clearly labeled
- [ ] At least 2 sources for each major point
- [ ] No logical fallacies in arguments

## Video Format Strategy

### Talking Head Usage (60-70% of video)
- Making arguments and interpretations
- Explaining causation
- Connecting historical events
- Asking rhetorical questions
- Building narrative
- Emotional emphasis

### B-Roll Usage (30-40% of video)
- **Maps (15-20%):** Geographic boundaries, territorial expansion, maritime zones
- **Primary sources (10-15%):** Treaty documents, diplomatic correspondence, official proclamations
- **Historical photos (5-10%):** Key figures, historical events, archaeological sites
- **Modern footage (5%):** Current events, news headlines, contemporary scenes

### The Golden Rule
**If the B-roll doesn't make your argument stronger, stay on camera.**

B-roll is evidence, not decoration. You are the authority making an argument, not just a narrator.

## Tool Stack

- **VidIQ Pro** - Topic research, script generation, clipping tool
- **Claude Pro** - Fact-checking, research, editing guidance
- **DaVinci Resolve** - Video editing
- **Photoshop** - Thumbnail creation
- **NotebookLM** - Source-grounded research

## File Organization

### Project Lifecycle Folders (CRITICAL)

**All video projects MUST be in lifecycle folders:**

- **`video-projects/_IN_PRODUCTION/`** - Active research and scripting
- **`video-projects/_READY_TO_FILM/`** - Finalized scripts ready for filming
- **`video-projects/_ARCHIVED/`** - Published or cancelled projects

**NEVER create loose folders in `video-projects/` root**

**Naming convention:** `video-projects/[lifecycle]/[number]-[topic-slug-year]/`

Example: `video-projects/_READY_TO_FILM/1-sykes-picot-2025/`

### Standard Files Within Projects

- `FINAL-SCRIPT.md` - Production-ready script
- `YOUTUBE-METADATA.md` - Title, description, tags, timestamps
- `B-ROLL-CHECKLIST.md` - Visual requirements
- `FACT-CHECK-VERIFICATION-SPREADSHEET.md` - Source verification
- `*.srt` - Subtitle files (often need fixing for name/timestamp errors)

### Claude Agent Configuration Files

**Important reference documents in `.claude/`:**

- **`FOLDER-STRUCTURE-GUIDE.md`** - Complete folder system rules (READ FIRST when creating files)
- **`USER-PREFERENCES.md`** - Working style, efficiency expectations, common tasks
- **`agents/`** - Specialized AI agents for scripting, analysis, orchestration
- **`commands/`** - Slash commands for common workflows

**Agents:**
- `video-orchestrator.md` - Coordinates full workflow
- `script-writer-v2.md` - Generates scripts with retention optimization
- `structure-checker-v2.md` - Analyzes scripts for retention issues

**Commands:**
- `/new-video` - Start new project with full workflow
- `/script` - Generate script from research
- `/youtube-metadata` - Create optimized metadata
- `/fix-subtitles` - Fix auto-transcription errors in .srt files
- `/fact-check` - Verify sources and claims

## Working with Scripts

When editing or creating scripts:
1. Always check fact-checking-protocol.md first
2. Verify all claims have sources
3. Maintain academic balance
4. Use Master Project Template for structure
5. Follow HYBRID_TALKING_HEAD_GUIDE for visual planning
6. Run completed scripts through NotebookLM fact-check prompt

## Common Tasks

### Creating a new video script
**Phase 1: Preliminary Research (Internet Sources)**
1. Conduct preliminary internet research (Wikipedia, news, academic sites)
2. Create RESEARCH-SUMMARY.md with preliminary findings (mark all claims ❓)
3. Identify what needs academic verification

**Phase 2: Academic Verification (NotebookLM)**
4. Create NOTEBOOKLM-RESEARCH-PLAN.md with specific academic books to download
5. Download sources (university library + selective purchases, $0-200)
6. Upload to NotebookLM and run targeted verification prompts
7. Extract verified statistics, proper citations, smoking gun quotes

**Phase 3: Script Writing**
8. Draft script using verified academic sources and proper citations
9. Write for conversational spoken delivery (contractions, natural dates, breath marks)
10. Follow "both extremes are wrong" structure
11. Include modern relevance connections every 90 seconds
12. Plan visual elements using Hybrid Talking Head Guide

**Phase 4: Final Verification**
13. Fact-check every claim has 2+ sources
14. Verify citations include page numbers where possible
15. Test script by reading aloud (conversational delivery check)

### Fact-checking an existing script
1. Review fact-checking-protocol.md
2. Identify all factual claims (numbers, dates, quotes, cause-effect)
3. Verify each claim has 2+ sources
4. Check contested information is labeled
5. Run NotebookLM fact-check prompt
6. Document all sources

### Responding to YouTube comments
1. Follow youtube-comment-response-guide.md
2. Lead with claim, then correction
3. Cite 2-4 credible sources
4. Be respectful on sensitive topics
5. Default CTA: "Full breakdown on YouTube. Sources in description."

## Performance Insights

### What Works
- Territorial disputes with modern news hooks (Essequibo: 1.9K views, 19 new subs)
- Political fact-checking (JD Vance: 936 views)
- Historical political myths (Stalin video performance)
- Modern relevance connections
- Evidence-based approach
- Strong retention (30-35% is excellent for 8-12 min educational videos)

### Topic Formula
"[Colonial/Historical Decision] from [X] years ago is still [causing deaths/conflicts/disputes] today"

## Channel Mission

Make academic research accessible while maintaining historical integrity. The goal is not entertainment or political commentary, but evidence-based education that reveals how distorted history fuels present-day conflicts.

**Quality over quantity, always.**

## Critical: Primary Source Accuracy for Fact-Checking Videos

When creating editing guides or production materials for fact-checking videos:

**ALWAYS ask clarifying questions about primary sources before writing:**
- What does each document actually record? (e.g., Höfle Telegram = train deportations, not death counts)
- What specific language/euphemisms are used? (e.g., Korher Report uses "Sonderbehandlung/SB" for killings)
- What is the exact historical context?

**NEVER assume you know what a document contains** - especially for:
- Nazi documents (telegrams, statistical reports, operational records)
- Historical treaties, petitions, declarations
- Court rulings, government documents
- Scientific studies

**Why this matters:**
- Holocaust/genocide videos require ABSOLUTE precision for credibility
- Fact-checking claims requires understanding what evidence actually proves
- Context changes interpretation (deportation records + death camp destinations = evidence of genocide)

**When in doubt:** Read the script first, ask questions, then create the guide.
