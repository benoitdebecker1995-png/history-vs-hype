---
description: Convert scripts to articles, write original articles, or get editing feedback (Newsletter)
model: opus
---

# /newsletter - Newsletter Article Pipeline

Convert existing video scripts into Substack articles, write original articles from verified research, score articles against the quality gate, or get editing feedback on drafts.

## Usage

```
/newsletter                          # Interactive: pick a project and mode
/newsletter --convert [project]      # Convert script to article
/newsletter --write [project]        # Write original article from verified research
/newsletter --edit [project]         # Get feedback on a draft you wrote
/newsletter --score [project]        # Run automated quality gate scorer
/newsletter --subjects [project]     # Generate subject line variants only
/newsletter --package [project]      # Package translated document as paid-tier PDF
```

## Flags

| Flag | Purpose | Example |
|------|---------|---------|
| `--convert` | Convert existing SCRIPT.md to newsletter article | `/newsletter --convert 41-treaty-tordesillas-2026` |
| `--write` | Write original article from 01-VERIFIED-RESEARCH.md | `/newsletter --write 49-code-noir-untranslated-2026` |
| `--edit` | Get Calm Prosecutor feedback on your rough draft | `/newsletter --edit 41-treaty-tordesillas-2026` |
| `--score` | Run automated quality gate (16 checks) | `/newsletter --score 41-treaty-tordesillas-2026` |
| `--subjects` | Generate 5 subject lines for existing article | `/newsletter --subjects 41-treaty-tordesillas-2026` |
| `--package` | Package translated document as paid PDF | `/newsletter --package 37-untranslated-vichy-statut-juifs-2026` |

---

## CONVERT MODE (`--convert`)

Convert an existing video script into a newsletter article using the article-writer agent.

### Step 1: Find the script

```
Glob for the project folder in video-projects/_IN_PRODUCTION/
Read SCRIPT.md, 02-SCRIPT-DRAFT.md, or FINAL-SCRIPT.md (whichever exists)
```

### Step 2: Read the style references

```
Read .claude/REFERENCE/WRITING-VOICE-AND-STYLE.md (PARTS 1, 2, 6, 7)
```

### Step 3: Launch article-writer agent in CONVERT mode

Pass the full script to the article-writer agent with these instructions:

```
MODE: CONVERT
INPUT: [full script text]
PROJECT: [project slug]

Convert this video script into a newsletter article following all rules in your agent definition.
Read .claude/REFERENCE/WRITING-VOICE-AND-STYLE.md PARTS 6-7 before writing.

CRITICAL REMINDERS:
- Verdict in paragraph 1 (Minto Pyramid, not bottom-up)
- SCQA opening: Situation, Complication, Question, Answer
- Zero metadiscourse (Pinker)
- Evidence as narrative, not citation (Bryson/Graeber/Howes)
- Verdict sentences under 5 words after evidence builds
- No em dashes in prose
- 2-3 [PERSONAL] markers at emotional peaks
- Blockquote all primary sources
- Stay at the crime scene for the ending (no TED Talk leaps)
- All facts must be traceable to the input script
```

### Step 4: Save output

Save the article to the project folder as `NEWSLETTER-ARTICLE.md`

### Step 5: Run the quality gate

```bash
python -m tools.newsletter.article_scorer [path to NEWSLETTER-ARTICLE.md]
```

Display the scorer output. If any FAIL results, fix them before showing to user.

### Step 6: Generate packaging (subject lines + SEO metadata)

Generate 5 subject line candidates and score them:
```bash
python -m tools.newsletter.subject_line_scorer "Line 1" "Line 2" "Line 3" "Line 4" "Line 5"
```

For the top scorer, also generate:
- **Subtitle** (under 100 chars, complements subject, contains keyword)
- **SEO title** (under 60 chars, keyword-explicit)
- **Meta description** (under 155 chars, works as Google snippet)
- **URL slug** (under 60 chars, keyword + hyphens)

See `.claude/REFERENCE/NEWSLETTER-METADATA-CHECKLIST.md` for full checklist.

### Step 7: Show the user

Display:
- The article (or first 50 lines + "saved to [path]")
- The ranked subject lines with scores
- The SEO metadata (subtitle, SEO title, meta description, URL slug)
- The quality gate results
- Any [RESEARCH NAME] suggestions
- Reminder: "Edit this yourself: add your voice at every [PERSONAL] marker. Read it aloud. Then publish."

---

## WRITE MODE (`--write`)

Write an original article from verified research.

### Step 1: Find research

```
Glob for 01-VERIFIED-RESEARCH.md in the project folder
If not found, check for any *RESEARCH*.md files
```

### Step 2: Read the style references

```
Read .claude/REFERENCE/WRITING-VOICE-AND-STYLE.md (PARTS 1, 2, 6, 7)
```

### Step 3: Launch article-writer agent in WRITE mode

```
MODE: WRITE
INPUT: [full verified research text]
PROJECT: [project slug]

Write an original newsletter article from this verified research following all rules in your agent definition.
Read .claude/REFERENCE/WRITING-VOICE-AND-STYLE.md PARTS 6-7 before writing.
```

### Step 4-6: Same as CONVERT mode

---

## EDIT MODE (`--edit`)

Get feedback on a draft the user wrote themselves.

### Step 1: Find the draft

```
Read NEWSLETTER-ARTICLE.md or ARTICLE-DRAFT.md in the project folder
If not found, ask the user to paste their draft
```

### Step 2: Read the style references

```
Read .claude/REFERENCE/WRITING-VOICE-AND-STYLE.md PARTS 6-7
```

### Step 3: Run the automated scorer first

```bash
python -m tools.newsletter.article_scorer [path to article]
```

### Step 4: Run the 10-rule Calm Prosecutor check

Check the draft against all 10 Calm Prosecutor rules:

| # | Rule | Source | Check |
|---|------|--------|-------|
| 1 | Evidence over activities | Pinker | Am I pointing at evidence or at myself? |
| 2 | Moral confusion | Graeber | Did I find contradictory beliefs held simultaneously? |
| 3 | Ultimate explanations | Diamond | Did I push causation deep enough? |
| 4 | Imagined orders | Harari | Did I identify the shared fiction at work? |
| 5 | Artifact anchoring | Frankopan | Is there a physical object grounding the abstract? |
| 6 | Unburdening suffering | Mukherjee | Did I name the human cost before analyzing? |
| 7 | Revealing metaphor | Dawkins | Is there a metaphor that shocks into new seeing? |
| 8 | Verdict sentences | Bryson | Are there short punches after evidence dumps? |
| 9 | Trends vs drama | Rosling | Did I separate long-term patterns from immediate events? |
| 10 | Curse of Knowledge | Pinker | Am I explaining for intelligent non-experts? |

### Step 5: Run the CRIBS Audit

For each section, tag it:
- **C** (Confusing) - Rewrite for the intelligent non-expert
- **R** (Repeated) - Cut the weaker version
- **I** (Interesting) - Keep, verify it earns its place
- **B** (Boring) - Delete or rewrite as narrative
- **S** (Surprising) - Double down

### Step 6: Run the Reframe Test

> "Most readers assume _____, but the evidence shows _____."

If the first blank can't be filled with a real belief, the reframe fails.

### Step 7: Provide feedback

For each issue found:
1. Quote the exact sentence
2. Name which rule it violates (with author)
3. Suggest a rewrite the user can learn from

Also provide:
- The single strongest paragraph (and why)
- The single weakest paragraph (and why)
- Which model author's technique to try next
- AI-slop check: flag any generated-sounding phrases
- Overall verdict: "sounds like you" or "sounds like a machine" (be honest)

---

## SCORE MODE (`--score`)

Run the automated quality gate only, without generating or editing content.

### Step 1: Find the article

```
Glob for NEWSLETTER-ARTICLE.md in the project folder
```

### Step 2: Run the scorer

```bash
python -m tools.newsletter.article_scorer [path to NEWSLETTER-ARTICLE.md]
```

### Step 3: Display results

Show the full scorer output. If failures exist, list the specific fixes needed.

---

## SUBJECTS MODE (`--subjects`)

Generate subject lines only (for an existing article).

### Step 1: Read the article

```
Read NEWSLETTER-ARTICLE.md in the project folder
```

### Step 2: Read the metadata checklist

```
Read .claude/REFERENCE/NEWSLETTER-METADATA-CHECKLIST.md (subject line section)
```

### Step 3: Generate 5 subject lines

Use these techniques (one per line):
- Data Confrontation (Rosling): lead with a surprising number
- Familiar Made Strange (Harari): invert an assumption
- Contrarian Verdict (Graeber): state the conclusion as a provocation
- Evidence Reveal: "I translated/read/found the [document] that [surprise]"
- Specific Number + Mystery: "[number] [things] and [unresolved question]"

Rules (from open-rate data):
- 6-10 words, 36-50 characters (sweet spot)
- No "How to" opener (-57% fewer opens)
- No colon (kills curiosity gap)
- No year in first third (front-load mystery, not date)
- No em dashes
- Curiosity gap marker required ("never," "actually," "wrong," "myth," "nobody")

### Step 4: Score with subject_line_scorer

```bash
python -m tools.newsletter.subject_line_scorer "Line 1" "Line 2" "Line 3" "Line 4" "Line 5"
```

Display the ranked results. Recommend the top scorer but note if a lower-scoring line has better brand fit.

### Step 5: Generate subtitle + SEO fields

For the top subject line, also generate:
- **Subtitle** (under 100 chars, complements subject, contains target keyword)
- **SEO title** (under 60 chars, keyword-explicit — can differ from email subject)
- **Meta description** (under 155 chars, complete sentence, works as Google snippet)
- **URL slug** (under 60 chars, keyword + hyphens, no stop words)

---

## PACKAGE MODE (`--package`)

Package a translated primary source document as a paid-tier PDF.

### Step 1: Find translation files

```
Glob for translated documents, SRT files, or translation outputs in the project folder
Check for any *translation*.md, *TRANSLATION*.md, or annotated documents
```

### Step 2: Generate PDF packaging

Create a document with:
1. **Cover page**: Title, original language, date, translator credit, one-sentence importance
2. **Historical context** (500 words max): What was happening, who wrote it, who was affected (name real people)
3. **Translation notes**: Surprises, untranslatable terms, ambiguities, choices made
4. **Reading guide**: Key clauses, "I never realized this" moments, what shocks a modern reader
5. **Modern relevance**: Connection to something measurable today
6. **Further reading**: 3-5 university press sources

### Step 3: Save as `PAID-PDF-PACKAGE.md` in the project folder

---

## ARTICLE CONVERSION PRIORITY (Best scripts to convert first)

| Rank | Project | Topic | Why it converts well |
|------|---------|-------|---------------------|
| 1 | 41-treaty-tordesillas-2026 | Systems/mechanism | DONE. Self-contained, data-driven, 4 clean acts |
| 2 | 4-crusades-fact-check-2025 | Myth-busting | Primary source quotes, modern hook (Hegseth) |
| 3 | 10-dark-ages-2025 | Myth-busting | Perfect article length, data-heavy |
| 4 | 21-haiti-independence-debt-2025 | Financial extraction | Heist narrative, serializable (4 parts) |
| 5 | 37-untranslated-vichy-statut-juifs-2026 | Translation | First paid PDF product candidate |

---

## QUALITY REMINDERS

- **NEVER fabricate** scenes, characters, or sensory details
- **ALWAYS keep** every quote, citation, and page number from the source
- **Flag [PERSONAL]** markers: the user MUST add their own voice (this is the anti-slop layer)
- **Flag [RESEARCH NAME]**: suggest where a real named individual would strengthen the passage
- **Blockquote** all primary sources: these are the article's visual "B-roll"
- **No em dashes** in prose. Commas, periods, colons, parentheses only.
- The user is LEARNING to write articles. Guide, don't replace. Mark what they should rewrite themselves.
- **Run the scorer** (`python -m tools.newsletter.article_scorer`) on every article before showing to user
