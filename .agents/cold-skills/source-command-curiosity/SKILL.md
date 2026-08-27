---
name: source-command-curiosity
description: "Evaluates a title's human psychology, curiosity gap and emotional stakes. Use when: judging or comparing candidate titles, or a title scores well mechanically but feels flat."
---

> **Codex note.** This is the Codex port of `.claude/commands/curiosity.md`, which stays canonical.
> The procedure below is that file verbatim. While running here: a `/name` reference is the
> `source-command-name` skill in `.agents/skills/`; "the Task tool" means spawning a Codex agent
> from `.codex/agents/`; "Claude" means you.

# /curiosity — Emotional Hook Scorer

**Purpose:** Evaluates a video title strictly on HUMAN PSYCHOLOGY and CURIOSITY, rather than analytical rules.

## Usage

```
/curiosity "Why Spain Didn't Civilize Peru: The 500-Year Lie"
```

## Instructions for the AI

When the user runs this command with a title, act as an expert YouTube packaging strategist.
Evaluate the provided title on these 3 dimensions (0-100 total score):

1. **Curiosity Gap (0-40 points):** Does it make the viewer ask a question they MUST know the answer to? (e.g. "The 500-Year Lie" creates a massive gap). Does it set up a clear paradox that can be resolved using the 5-second opening formula (Specific Subject + Common Belief + Contradiction)?
2. **The Stakes (0-40 points):** Does it imply a massive consequence or a shocking contradiction? Does it promise an "Exhibit A" document/mechanism?
3. **Conversational Tone (0-20 points):** Does it sound like a human talking (like a calm professor/Fig Tree style), rather than a textbook?

**Output Format:**

```markdown
## Curiosity Score: [Total]/100

**Curiosity Gap ([X]/40):** [Brief feedback]
**The Stakes ([X]/40):** [Brief feedback]
**Conversational Tone ([X]/20):** [Brief feedback]

**Final Verdict:** [1 sentence summarizing if this is emotionally compelling or too analytical]
```
