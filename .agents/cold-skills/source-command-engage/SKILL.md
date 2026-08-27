---
name: source-command-engage
description: "Drafts comment responses, corrections and feedback handling in the channel's voice. Use when: replying to YouTube comments, handling a correction after publish, or triaging viewer feedback."
---

> **Codex note.** This is the Codex port of `.claude/commands/engage.md`, which stays canonical.
> The procedure below is that file verbatim. While running here: a `/name` reference is the
> `source-command-name` skill in `.agents/skills/`; "the Task tool" means spawning a Codex agent
> from `.codex/agents/`; "Claude" means you.

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

### How it works: spawn the `comment-responder` agent

`--respond` delegates to the **`comment-responder`** agent (`.claude/agents/comment-responder.md`), which runs the full pipeline: classify **posture** (Interlocutor / Drive-by / Question / Troll) → extract every claim → fact-check **notebook-first** (verifying our own claims too) → **steelman** → draft in the channel's accessible-historian voice (**sources named in prose, no citation dump** for discussion replies) → advisory Gemini voice pass → return the ready-to-post reply + a behind-the-scenes audit trail.

Spawn it with the pasted comment (or the whole thread) and which video it's on:

```
Task(subagent_type="comment-responder", model="opus",
  prompt="Reply to this comment on [video/slug]: '[comment text, incl. our prior reply if a thread]'. [any steer]")
```

Use `model="sonnet"` for a simple Drive-by/Question. The full spec — posture taxonomy, the discussion-vs-debunk sourcing split, the voice rules and AI-tell ban — lives in `.claude/REFERENCE/youtube-comment-response-guide.md`.

**The agent may recommend NOT replying** (troll / not worth it). That's a valid outcome — don't override it into an essay.

**If a video error surfaces during the check:** run `/engage --correction`.

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
