---
deprecated: true
replaced_by: /engage --save
---

> **DEPRECATED:** This command has been replaced by `/engage --save`.
> Run `/help` to see current commands.

[Original content below for reference]
---

---
description: Save insightful YouTube comments for future research or video ideas
---

You are saving an insightful YouTube comment from a History vs Hype video for future reference.

## Purpose

Some comments provide:
- Research leads (books, sources, expert perspectives)
- Video ideas (topics to explore, angles to investigate)
- Viewer insights (what resonates, what confuses, what interests people)
- Expert corrections (from academics, locals, subject matter experts)

Instead of losing these in the YouTube comment section, save them for later use.

## Step 1: Classify the Comment's Value

**Ask user which category:**

**Research Lead:**
- Commenter suggests specific sources, books, or documents
- Points to archival materials or databases
- Provides expert contact or institutional resource

**Video Idea:**
- Suggests related topic worth investigating
- Points out unexplored angle on existing topic
- Identifies gap in coverage

**Viewer Insight:**
- Reveals what part of video was most impactful
- Shows what wasn't clear (need better explanation)
- Demonstrates audience interest level in specific aspect

**Expert Correction:**
- Commenter has specialized knowledge (academic, local, professional)
- Provides correction with credible sources
- Offers alternative interpretation with reasoning

## Step 2: Save to Appropriate Location

**File location:** `channel-data/saved-comments/[CATEGORY]-comments.md`

**Create file structure if doesn't exist:**

```markdown
# [Category] Comments

Insightful comments saved from YouTube for future use.

---

## [Video Title] - [Commenter Name] - [Date]

**Comment:**
> [Full comment text, quoted]

**Why saved:**
[Brief note on value--what makes this worth saving?]

**Potential use:**
[How might this be useful later?]

**Follow-up action:**
- [ ] [Specific action if needed, e.g., "Research recommended book"]
- [ ] [Link to research file if created]
- [ ] [Add to topic ideas list if video idea]

**Link to comment:** [YouTube comment URL if available]

---
```

[Content truncated for brevity - see original file for full content]
