---
deprecated: true
replaced_by: /engage --correction
---

> **DEPRECATED:** This command has been replaced by `/engage --correction`.
> Run `/help` to see current commands.

[Original content below for reference]
---

---
description: Document and publish corrections for video errors discovered post-publication
---

You are creating a systematic correction for an error discovered in a published History vs Hype video.

## Step 1: Document the Error

**Get error details from user:**
1. Which video has the error?
2. What was stated incorrectly?
3. What is the correct information?
4. How was it discovered? (comment, viewer email, your own review)

**Read the video script to confirm:**
```
- Use Glob to find: video-projects/**/SCRIPT.md OR *.srt
- Locate exact wording of error in script
- Confirm timestamp if available
```

## Step 2: Create Corrections Log Entry

**File location:** `video-projects/_CORRECTIONS-LOG.md`

**If file doesn't exist, create it with this format:**

```markdown
# Video Corrections Log

This file tracks errors discovered in published videos and how they were corrected.

## [Video Title] - [Publication Date]

### ERROR 1: [Short description]
**Timestamp:** [MM:SS]
**What was stated:** "[Exact quote from video]"
**What is correct:** "[Correct information]"
**Discovered by:** [Commenter name / Self-review / Viewer email]
**Date discovered:** [YYYY-MM-DD]
**Correction actions taken:**
- [ ] Pinned comment published
- [ ] Description updated
- [ ] Response template created
- [ ] Added to fact-check improvements

**Why this happened:**
[Brief analysis: Was it oversimplification? Outdated info? Research gap?]

**Lesson for future fact-checking:**
[What check would have caught this? E.g., "Add simplification detector for territorial claims"]

**Sources for correct information:**
- [Source 1 with link]
- [Source 2 with link]

---
```

[Content truncated for brevity - see original file for full content]
