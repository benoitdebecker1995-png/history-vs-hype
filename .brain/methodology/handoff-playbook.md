# Gemini ↔ Claude Handoff Playbook

Extends the `/handoff` protocol from `GEMINI.md` with concrete invocation recipes.

## Base protocol (from GEMINI.md)

When switching between Claude and Gemini:
1. Update `HANDOFF.md` with current state
2. State exactly what was completed and what the other AI needs to do next
3. Baton signal: `READY FOR [CLAUDE/GEMINI]`

## When to invoke Gemini

| Situation | Route to |
|-----------|----------|
| Reading >50K tokens of source material | Gemini |
| Processing multiple full transcripts in one call | Gemini |
| Pre-greenlight landscape scan (50 competitor pages) | Gemini |
| Ingesting raw source into brain wiki format | Gemini |
| Quote-mining a full academic book/PDF | Gemini |
| Making a judgment call, producing a verdict, or writing a finished artifact | Claude |
| Anything touching script-writer-v2 or article-writer | Claude (Opus) |
| Anything requiring tools (file edits, git, bash) | Claude Code |

## How to invoke (headless)

**Standard:**
```bash
gemini --yolo -p "<your-prompt>" -o text > .brain/_inbox/<task>-<YYYY-MM-DD>.md
```

**For inputs >50KB (pipe via stdin):**
```bash
cat <input-file> | gemini --yolo -p "<your-prompt>" -o text > .brain/_inbox/<task>-<YYYY-MM-DD>.md
```

**Via Claude Code `/gemini` command:**
```
/gemini digest path/to/transcript.md
/gemini scan "Bakassi Peninsula Nigeria Cameroon"
/gemini quote-mine path/to/book.pdf
/gemini ingest ~/llm-brain/raw/research/topic.md
```

## Output staging convention

- ALL Gemini output goes to disk first: `.brain/_inbox/<task>-<date>.md` or `_gemini-output/<task>-<timestamp>.md`
- **Never pipe raw Gemini output back into Claude's context** — the point is to keep long-context reads on disk
- Claude reads a short summary or first 100 lines to verify schema, not the full document

## Review protocol

After Gemini writes output:
1. Read first 100 lines — verify schema matches expectation
2. Check: is it well-formed markdown? Does it have expected headers/fields?
3. If schema drift detected: retry once with tightened prompt
4. If retry fails: report to user — do NOT paper over the error or silently continue

## Failure handling

- Quota exhausted: note the reset window (~18 min), fall back to Sonnet for the task, schedule Gemini work for next session
- Auth failure: run `nlm login` or check Google AI Plan credentials in Gemini CLI settings
- Off-schema output: retry once, if still bad — surface the raw output to user for triage

---

## Recipe cards

### Recipe A: Competitor transcript digest

**Trigger:** You have a competitor video transcript and want to extract retention patterns.

**Input:** `path/to/transcript.md` (full video transcript, typically 8-15K tokens)

**Command:**
```bash
gemini --yolo -p "Extract from this transcript: (1) cold-open hook verbatim + classify as cold_fact/specificity_bomb/contextual_opening/question, (2) turn point with timestamp + technique, (3) retention beats every pattern interrupt with timestamp + type, (4) structural template as 3-5 sentence skeleton. Output as markdown with H2 sections." -o text < path/to/transcript.md > .brain/_inbox/digest-YYYY-MM-DD.md
```

**Claude's next step:** Read `.brain/_inbox/digest-YYYY-MM-DD.md` first 50 lines, verify schema, then use findings in `/competitor-gap` or `/patterns` analysis.

---

### Recipe B: Brain ingestion (raw → wiki)

**Trigger:** `.brain/_queue/` has raw content to process into wiki format.

**Input:** Raw source file (transcript, article, research dump)

**Command:**
```bash
cat .brain/_queue/<file>.md | gemini --yolo -p "This is a raw source for an LLM wiki. Extract: (1) entities as bullet list (person/place/treaty/document, <=20 words each), (2) concepts as bullet list (mechanisms/frameworks), (3) verbatim quotes worth saving with exact page numbers in blockquote format, (4) candidate cross-refs to existing wiki pages (treaty-of-tripoli, berlin-conference-1884, etc.). Output as markdown ready for wiki-ingest triage." -o text > .brain/_inbox/ingest-YYYY-MM-DD.md
```

**Claude's next step:** Run `/wiki-ingest` to triage the output into `~/llm-brain/wiki/` or `.brain/sources/`.

---

### Recipe C: Pre-greenlight landscape scan

**Trigger:** Evaluating a new topic before committing to research.

**Input:** Topic string

**Command:**
```bash
gemini --yolo -p "For the topic '<TOPIC>', list the top 20 YouTube videos by view count from channels like RealLifeLore, Wendover, Johnny Harris, Kraut, PolyMatter, CaspianReport. For each: title, channel, view count, thumbnail description (text overlay / map / face / object), publish date, hook type. Output as a markdown table sorted by views descending." -o text > .brain/_inbox/scan-<topic-slug>-YYYY-MM-DD.md
```

**Claude's next step:** Read table, score against `/greenlight` viability rules in `tools/PACKAGING_MANDATE.md`.

---

### Recipe D: Quote mining from academic source

**Trigger:** You have a PDF/text of an academic book and need verbatim quotes with page numbers.

**Input:** Source file (converted to text)

**Command:**
```bash
cat path/to/source.txt | gemini --yolo -p "Extract every verbatim quote that meets ALL: (a) <=40 words, (b) makes a single concrete claim, (c) has a citable page number, (d) would survive an earn-your-inclusion test (carries weight without surrounding context). Output as numbered blockquote list with '— Author, *Title*, p.NN' attribution." -o text > .brain/sources/<book-slug>.md
```

**Claude's next step:** Run article-writer Rule 5C citation grounding — round-trip each quote through the NotebookLM notebook before including in a draft.
