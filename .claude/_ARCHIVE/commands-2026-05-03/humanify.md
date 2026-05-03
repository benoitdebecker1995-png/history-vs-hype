---
description: Rewrite AI-generated text in the creator's natural voice using WRITING-VOICE-AND-STYLE.md PART 1
model: opus
---

# /humanify - Voice Profile Rewrite Pass

Take an existing draft (script or article) and rewrite it to sound like the creator actually wrote it. Uses `.claude/REFERENCE/WRITING-VOICE-AND-STYLE.md` PART 1 (Core Voice) as the authoritative voice reference.

## Usage

```
/humanify [project]              # Interactive: find draft, rewrite section by section
/humanify [project] --article    # Rewrite newsletter article draft
/humanify [project] --script     # Rewrite script draft
/humanify [project] --section N  # Rewrite only section N of the draft
```

## How It Works

This is a VOICE pass, not a structural pass. The structure, arguments, evidence, and quotes stay the same. Only the voice changes.

### Step 1: Read the voice profile

Read `.claude/REFERENCE/WRITING-VOICE-AND-STYLE.md` PART 1 (Core Voice) in full. This is the creator's actual speech patterns captured from voice samples and tested against corrections. Every rewrite decision must trace back to a specific rule in PART 1.

### Step 2: Find the draft

```
Glob for the project folder in video-projects/
Read the target file:
  --script  → 02-SCRIPT-DRAFT.md
  --article → NEWSLETTER-ARTICLE.md (or similar)
```

If no flag given, ask whether this is a script or article.

### Step 3: Rewrite section by section

Go through each section and apply these voice profile checks (in priority order):

**Word choice:**
- [ ] Simplify verbs — "published" → "wrote", "examined" → "looked at", "selected" → "picked"
- [ ] BUT keep specificity when it does argumentative work — don't flatten "randomly inventing a large number" to "making it up"
- [ ] Casual precision — "significantly" → "a lot more", "approximately" → "about"

**Explaining things:**
- [ ] Every jargon term defined inline on first use
- [ ] Titles/epithets explained by function before naming — what did they DO to earn it?
- [ ] Cultural references introduced by function, not location — what do people USE it for?
- [ ] Time comparisons use specific events AND do argumentative work (only when scale is hard to grasp)
- [ ] Numbers attributed to sources — WHO counted?

**Sentence structure:**
- [ ] One idea per sentence — split compound clauses
- [ ] BUT don't over-fragment into staccato beats — combine when beats belong together
- [ ] Active voice, people as subjects — "France signed" not "the treaty was signed"
- [ ] Narrate, don't list — verbs showing things happening, not nouns listing things that happened
- [ ] Name the pathway, not "everyone knows" — how did people actually encounter this?

**Delivery:**
- [ ] Setup lines before quotes direct attention, don't judge quality
- [ ] Trust the reader to feel the surprise — "not X, but Y" structure, no commentary
- [ ] Let stats make the argument — don't editorialize about character
- [ ] The text must survive its own methodology — don't reinforce what you're debunking

**For articles specifically:**
- [ ] Adapt spoken patterns for the page — same voice, different rhythm
- [ ] Don't import staccato spoken rhythms into prose — translate, don't transcribe
- [ ] Em dash rules from WRITING-VOICE-AND-STYLE.md PART 6 still apply (no em dashes in article prose)
- [ ] Metadiscourse rules still apply — voice profile doesn't override "kill on sight" phrases

### Step 4: Present changes

For each section, show:
1. The original text
2. The rewritten text
3. What changed and which voice profile rule drove each change

Work one section at a time. Wait for user feedback before moving to the next. The user may correct the rewrite, and those corrections feed back into the voice profile.

### Step 5: Update voice profile if corrected

If the user corrects a rewrite, update `.claude/REFERENCE/WRITING-VOICE-AND-STYLE.md` PART 1 with the new pattern. This is how the voice profile improves over time.

## What This Does NOT Do

- Change the structure or argument of the draft
- Add or remove evidence, quotes, or sources
- Change the order of sections
- Add features, CTAs, or content not in the original
- Override WRITING-VOICE-AND-STYLE.md PART 3-4 structural rules (myth-first, turn placement, duration cap)
- Override WRITING-VOICE-AND-STYLE.md PART 6 structural rules (Minto pyramid, Smart Brevity, etc.)

This is a voice-only pass. Structure stays. Voice changes.
