---
description: Dispatch a bulk-read task to Gemini CLI (headless) and capture output to a file. Use for transcripts, source digestion, competitor scans, brain ingestion.
---

# /gemini — offload bulk-read to Gemini

Routes long-context reading tasks to `gemini -p` headless, freeing Claude's context for judgment/writing.

**Routing rules:** see `~/llm-brain/wiki/concepts/gemini-claude-routing.md`. Default: bulk-read → Gemini, judgment/writing → Claude.

## Args

`$ARGUMENTS` — free-form. Expected shape: `<task-type> <input-path-or-topic> [--out <output-path>]`

Task types:
- `digest <transcript-path>` — extract hooks, retention beats, structural patterns from a competitor video transcript
- `ingest <raw-path>` — convert `~/llm-brain/raw/...` source into wiki page candidates (concepts/entities/quotes)
- `scan <topic>` — pre-greenlight landscape: competitor titles/thumbnails/descriptions for a topic, structured table out
- `quote-mine <source-path>` — pull verbatim quote candidates with page numbers from a long source
- `freeform <prompt>` — pass-through for anything else

## Procedure

1. Parse `$ARGUMENTS`. If unclear, ask one clarifying question (max).
2. Build the Gemini prompt from a per-task-type template (see below). Include exact output schema so the result is parseable.
3. Resolve `--out`. Default: `_gemini-output/<task-type>-<timestamp>.md` inside the current project (or `~/llm-brain/_queue/` for `ingest`).
4. Invoke headless: `gemini -p "<prompt>" --yolo -o text > <out-path>` via Bash. For inputs > 50KB, pipe via stdin: `cat <input> | gemini -p "<prompt>" --yolo > <out-path>`.
5. Read first ~100 lines of output to verify it's well-formed (not an error/auth failure).
6. Report: output path, line count, one-line summary. Do NOT dump full output into Claude's context — the whole point is to keep it on disk for the user / next step to consume.

## Task templates

**digest:** "Extract from this transcript: (1) cold-open hook (verbatim first 30s + classify: cold_fact / specificity_bomb / contextual_opening / question), (2) turn point (timestamp + technique), (3) retention beats (every pattern interrupt, with timestamp + type), (4) structural template (3-5 sentence skeleton). Output as markdown with H2 sections."

**ingest:** "This is a raw source for an LLM wiki at ~/llm-brain/. Extract: (1) entities (people/places/treaties/documents — one bullet each, ≤20 words), (2) concepts (mechanisms/frameworks — one bullet each), (3) verbatim quotes worth saving (with exact page numbers, blockquote format), (4) candidate cross-references to existing wiki pages. Output as markdown ready for `/wiki-ingest` triage."

**scan:** "For the topic '<topic>', list the top 20 YouTube videos by view count from comparable channels (RealLifeLore, Wendover, Johnny Harris, Kraut, etc.). For each: title, channel, views, thumbnail description (text overlay / map / face / object), publish date, hook type. Output as a markdown table sorted by views descending."

**quote-mine:** "Extract every verbatim quote from this source that meets ALL: (a) ≤40 words, (b) makes a single concrete claim, (c) has a citable page number, (d) would survive an 'earn-your-inclusion' test (orphan-quote test: does it carry weight without surrounding context). Output as numbered blockquote list with `— Author, *Title*, p.NN` attribution."

## Reminders

- Don't read the full Gemini output back into Claude's context unless the next step needs it. Report path + summary.
- If Gemini output is malformed (auth failure, truncated, off-schema), retry once with a tightened prompt; if still bad, report the failure to the user — don't paper over it.
- This command writes files; warn the user before running if the project is in a sensitive state (mid-commit, unstaged changes the user might not want stomped).
