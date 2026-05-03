---
description: Article draft-critique-rewrite loop using NotebookLM as trained critic
model: opus
---

# /workshop - Newsletter Article Workshop

Collaborative editing loop: Claude drafts article → NotebookLM critiques against 19 real human articles → User weighs in → NotebookLM suggests rewrites → Claude picks the best → Final output.

**This is for ARTICLES only.** The Article Workshop notebook contains 19 real human articles (Wyman, Devereaux, Howes, Graeber, deBoer, Sayare, Hoel, etc.) plus the Lopate and Best American Essays anthologies. It knows nothing about video production — scripts have their own pipeline (`/script` + structure-checker-v2).

## Usage

```
/workshop [project]              # Interactive: pick project, write + workshop article
/workshop --section [project]    # Workshop a specific section only
/workshop --critique [project]   # Skip draft, critique existing article
/workshop --rewrite [project]    # Jump to rewrite suggestions for a flagged section
```

## Flags

| Flag | Purpose |
|------|---------|
| (default) | Full article workshop loop: draft → critique → rewrite → final |
| `--section` | Workshop one section (paste or point to it) |
| `--critique` | Critique an existing NEWSLETTER-ARTICLE.md |
| `--rewrite` | Get 3 rewrite options for a specific section |

---

## THE WORKSHOP LOOP

### Step 0: Setup

```
Notebook ID: 3ccc9c87-3ea7-41c4-9516-718f73a5efd0

Verify NotebookLM auth:
- Try a test query. If auth expired, tell user to run: nlm login

Find the project:
- Glob for project folder in video-projects/_IN_PRODUCTION/ or _READY_TO_FILM/
- Read the draft (NEWSLETTER-ARTICLE.md) if it exists
- Read 02-SCRIPT-DRAFT.md or 01-VERIFIED-RESEARCH.md for source material
```

### Step 1: DRAFT (Skip if --critique or --rewrite)

Spawn the article-writer agent (`.claude/agents/article-writer.md`) to produce the best first draft.

Read the full agent file and all its referenced style files before writing. Save the draft as NEWSLETTER-ARTICLE.md in the project folder.

### Step 2: CRITIQUE — Send to NotebookLM

Extract the 4 most important sections from the draft:
1. **Opening** (first 2-3 paragraphs)
2. **Weakest transition** (identify the roughest section break)
3. **Key evidence section** (the section with the strongest claim)
4. **Closing** (last 2-3 paragraphs)

For EACH section, query NotebookLM:

```
Query template:
"Here is a draft [opening/transition/evidence section/closing] for a History vs Hype newsletter article.
Critique it using the CRITIQUE PROTOCOL note. Compare against the real articles in this notebook.
Score 1-10 and tell me specifically what would move it to a 9.

[Paste the section text]"
```

Use `mcp__notebooklm__notebook_query` with notebook_id `3ccc9c87-3ea7-41c4-9516-718f73a5efd0`.
Use the same conversation_id across all queries in one workshop session to maintain context.

### Step 3: PRESENT — Show the user

Present the critique results:

```markdown
## Workshop Critique

### Opening (Score: X/10)
[NotebookLM's feedback — key points only, not the full response]
**My take:** [Your own assessment — agree/disagree/add context]

### Weakest Transition (Score: X/10)
[NotebookLM's feedback]
**My take:** [Your assessment]

### Key Evidence Section (Score: X/10)
[NotebookLM's feedback]
**My take:** [Your assessment]

### Closing (Score: X/10)
[NotebookLM's feedback]
**My take:** [Your assessment]

## What do you think? Any sections you want to keep as-is? Anything that feels off?
```

WAIT for user input. Do NOT proceed to rewrites without the user's opinion.

### Step 4: REWRITE — Get NotebookLM suggestions

Based on the user's feedback, query NotebookLM for rewrite suggestions on the sections that need work:

```
Query template:
"Using the REWRITE PROTOCOL note, give me 3 rewrite options for this [opening/transition/evidence/closing].
Each option should use a different technique from the real articles in this notebook.
For each: name the technique, show a source quote, give me the rewrite, and explain why it's better.

The user's feedback on this section: [paste user's comments]

Current draft:
[Paste the section text]"
```

### Step 5: PICK — Suggest the best option

Present the 3 rewrite options to the user. Add your recommendation:

```markdown
## Rewrite Options for [Section]

### Option A: [Technique Name] (Recommended)
[The rewrite]
> Source model: "[exact quote]" — [Author]
**Why:** [One sentence]

### Option B: [Technique Name]
[The rewrite]
> Source model: "[exact quote]" — [Author]
**Why:** [One sentence]

### Option C: [Technique Name]
[The rewrite]
> Source model: "[exact quote]" — [Author]
**Why:** [One sentence]

**I'd go with Option [X] because [reason]. Want me to integrate it, or do you prefer a different one?**
```

WAIT for user input.

### Step 6: INTEGRATE — Produce final draft

Take the user's chosen rewrites and integrate them into the full draft. Ensure:
- Voice consistency across rewritten and untouched sections
- Transitions still flow after section replacements
- No orphaned references to removed text

Save the updated NEWSLETTER-ARTICLE.md.

### Step 7: FINAL CHECK — One last NotebookLM pass

Query NotebookLM with the final complete draft:

```
"Here is the final draft of a History vs Hype newsletter article.
Read it as a whole piece. Using the CRITIQUE PROTOCOL, give me:
1. Overall score (1-10)
2. The single weakest sentence
3. The single strongest sentence
4. Does this read like one of the real human articles in this notebook? Why or why not?"
```

Present the final score and any last fixes. Done.

---

## QUICK MODE: /workshop --section

For workshopping a single section without the full loop:

1. User pastes or identifies the section
2. Send to NotebookLM for critique (Step 2)
3. Present critique + your take (Step 3)
4. Ask if they want rewrite suggestions
5. If yes, run Step 4-5
6. Integrate and done

---

## QUICK MODE: /workshop --critique

For when an article draft already exists:

1. Find and read the existing NEWSLETTER-ARTICLE.md
2. Skip Step 1, go straight to Step 2 (Critique)
3. Continue the loop from there

---

## NOTES

- The Article Workshop notebook (3ccc9c87) contains 19 real human articles, the article-writing extracted patterns (now in WRITING-VOICE-AND-STYLE.md PART 7), and 3 instruction notes (CRITIQUE PROTOCOL, REWRITE PROTOCOL, QUICK REFERENCE).
- Always use the same conversation_id within one workshop session so NotebookLM retains context.
- If NotebookLM auth expires mid-session, tell the user to run `nlm login` in the terminal.
- WRITING-VOICE-AND-STYLE.md PART 1 (Core Voice) wins over any NotebookLM suggestion for phrasing choices.
- NotebookLM is the CRITIC. Claude is the WRITER. The user is the EDITOR. Don't blur the roles.
- When NotebookLM and Claude disagree, present both views and let the user decide.
- Critique focuses on: opening, transitions, evidence-as-narrative, rhythm, voice-fit, and closing.
- This command does NOT touch scripts. Scripts use `/script` + structure-checker-v2 + the competitor video notebook.
