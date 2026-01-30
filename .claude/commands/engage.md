---
description: Comment responses, corrections, and feedback management (Post-production Phase 3)
model: sonnet
---

# /engage - Audience Engagement Entry Point

Respond to comments, publish corrections, or save valuable feedback. Everything for post-publication engagement.

## Usage

```
/engage                      # Interactive: asks what you need
/engage --respond [comment]  # Research and respond to a comment
/engage --correction [video] # Publish correction for an error
/engage --save [comment]     # Save insightful comment for future use
```

## Flags

| Flag | Purpose | Example |
|------|---------|---------|
| `--respond` | Research-backed comment response | `/engage --respond "Commenter claims X..."` |
| `--correction` | Document and publish video correction | `/engage --correction somaliland-2025` |
| `--save` | Save valuable comment for future | `/engage --save "Great source recommendation..."` |

---

## COMMENT RESPONSE (`--respond`)

Research and respond to YouTube comments using evidence-based public history communication.

### Core Philosophy

**You are not trying to change the commenter's mind.** You are:
1. Performing for the silent audience (lurkers)
2. Demonstrating historical methodology
3. Building trustworthiness through transparency
4. Correcting the record with evidence

### Step 1: Extract ALL Claims

Before anything else, list EVERY claim in the comment:

- **Explicit claims** (directly stated)
- **Implicit claims** (underlying assumptions)
- **Sources they cite** (have you read them?)
- **Questions they ask**

### Step 2: Classify Identity Stake

| Level | Indicators | Strategy |
|-------|------------|----------|
| **Low** | Genuine questions, curiosity | Deep engagement |
| **Medium** | Mild preference, cites sources | Tactical pivot |
| **High** | Emotional language, "us vs them" | Correct for lurkers |
| **Very High** | Personal attacks, trolling | Strategic silence |

### Step 3: Read Context

**Before researching:**
1. Find video script (what was actually said?)
2. Check existing verified research
3. Check VERIFIED-CLAIMS-DATABASE.md
4. Identify what needs verification

### Step 4: Verify Claims

**Check existing research FIRST** (avoid duplicate work)

**Verify YOUR claims too** - not just commenter's

**Save new research:** `research/[Topic]-Comment-Response-Research.md`

### Step 5: Use Response Template

**Template 1: Factual Correction (Low/Medium Stake)**
- Lead with FACT, not myth
- Provide alternative explanation
- Cite specific sources with page numbers
- 200-300 words

**Template 2: Contested Interpretation (Medium Stake)**
- Acknowledge shared value
- Present multiple valid interpretations
- Explain WHY historians disagree
- 300-400 words

**Template 3: Nationalist Bias (High Stake)**
- Validate FEELING, not claim
- Expose contradictions
- Redirect to evidence
- 400-500 words max

**Template 4: Genuine Question (Low Stake)**
- Direct answer
- Provide 2-3 sources
- Encourage further learning
- 250-350 words

### Step 6: Apply Channel Voice

**Tone requirements:**
- Professional but conversational
- Active voice ("I cite" not "is cited")
- Confident about evidence, humble about interpretation
- Natural and flowing
- Under 500 words (YouTube limit)

### Output

Present drafted response with:
- Sources used
- Identity stake classification
- Any judgment calls flagged

**If video error discovered:** Ask about running `/engage --correction`

---

## PUBLISH CORRECTION (`--correction`)

Document and publish corrections for video errors discovered post-publication.

### Step 1: Document the Error

Get details:
1. Which video has the error?
2. What was stated incorrectly?
3. What is the correct information?
4. How was it discovered?

Read script to confirm exact wording.

### Step 2: Create Corrections Log Entry

**File:** `video-projects/_CORRECTIONS-LOG.md`

```markdown
## [Video Title] - [Publication Date]

### ERROR 1: [Short description]
**Timestamp:** [MM:SS]
**What was stated:** "[Exact quote]"
**What is correct:** "[Correct information]"
**Discovered by:** [Source]
**Date discovered:** [YYYY-MM-DD]
**Correction actions taken:**
- [ ] Pinned comment published
- [ ] Description updated
- [ ] Response template created
- [ ] Added to fact-check improvements

**Why this happened:**
[Brief analysis]

**Lesson for future fact-checking:**
[What check would have caught this?]

**Sources for correct information:**
- [Source 1 with link]
- [Source 2 with link]
```

### Step 3: Generate Pinned Correction Comment

```markdown
**CORRECTION**

At [timestamp], I stated "[incorrect information]." This was [oversimplified/incorrect/outdated].

[Correct information with specific details]

Thank you to [commenter name if applicable] for the correction.

Sources:
- [Source 1](link)
- [Source 2](link)
```

**Keep under 300 words.**

### Step 4: Update Video Description

Add at top of description:

```
CORRECTION: [Brief error description]. See pinned comment for details.
```

### Step 5: Create Response Template

For similar future comments:

**File:** `video-projects/[project]/COMMENT-RESPONSE-TEMPLATE.md`

### Step 6: Add to Fact-Check Improvements

**File:** `.claude/FACT-CHECK-IMPROVEMENTS.md`

Document:
- Error type (territorial simplification, temporal inaccuracy, etc.)
- Root cause
- New check to add

### Output

Present complete package:
1. Corrections log entry
2. Pinned comment draft
3. Updated description section
4. Response template
5. Fact-check improvement entry

---

## SAVE COMMENT (`--save`)

Save insightful comments for future research or video ideas.

### Comment Categories

| Category | Examples |
|----------|----------|
| **Research Lead** | Book recommendations, archival sources, expert contacts |
| **Video Idea** | Topic suggestions, unexplored angles, gaps |
| **Viewer Insight** | What resonated, what confused, what interests people |
| **Expert Correction** | Academic/professional corrections with sources |

### Save Format

**File:** `channel-data/saved-comments/[category]-comments.md`

```markdown
## [Video Title] - [Commenter Name] - [Date]

**Comment:**
> [Full comment text, quoted]

**Why saved:**
[What makes this worth saving?]

**Potential use:**
[How might this be useful later?]

**Follow-up action:**
- [ ] [Specific action needed]
- [ ] [Link to research if created]

**Link to comment:** [YouTube URL]
```

### Cross-Reference

- **Research lead** → Add to `research/[topic]-sources-to-investigate.md`
- **Video idea** → Add to topic ideas list
- **Expert correction** → Link to corrections log, update verified claims
- **Viewer insight** → Add to `channel-data/audience-insights.md`

### File Organization

```
channel-data/
└── saved-comments/
    ├── research-leads.md
    ├── video-ideas.md
    ├── viewer-insights.md
    └── expert-corrections.md
```

---

## Time Investment Framework

| Tier | Priority | Time | Examples |
|------|----------|------|----------|
| **1** | 24 hours | 15-30 min | 10+ likes, source-based, engaged viewers |
| **2** | 1 week | 5-15 min | Thoughtful without sources, follow-ups |
| **3** | Optional | Heart only | Simple thanks, old videos, trolls |

**Weekly budget:** 2-4 hours total

---

## Key Principles

1. **Alternative explanations over negation** - Fill mental gaps, don't just say "wrong"
2. **Fact-first headlines** - Don't repeat myth to debunk it
3. **Source transparency** - Always cite with page numbers
4. **Intellectual humility** - Admit errors gracefully
5. **Engage within 24-48 hours** - 189% higher retention for active channels

---

## Integration with Channel Workflow

**Before responding:**
1. Check video script
2. Check existing verified research
3. Check verified claims database

**After responding:**
1. Save new research for reuse
2. Update verified claims database
3. Document video errors if found
4. Run `/engage --correction` if needed

---

## Reference Files

- **Comment response guide:** `.claude/REFERENCE/youtube-comment-response-guide.md`
- **Corrections log:** `video-projects/_CORRECTIONS-LOG.md`
- **Verified claims:** `.claude/VERIFIED-CLAIMS-DATABASE.md`

---

## Absorbed Commands

This command consolidates functionality from:
- `/respond-to-comment` - Research-backed comment responses
- `/publish-correction` - Error documentation and correction
- `/save-comment` - Valuable feedback preservation

All original functionality preserved through flags.
