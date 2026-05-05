# Gemini ↔ Claude Model Routing (Project-Scoped)

Extends `~/llm-brain/wiki/concepts/gemini-claude-routing.md` with project-specific agent assignments and the model-budget guardrail rule.

## Model tier policy

| Tier | When to use |
|------|-------------|
| **Opus** | Voice-tuned writing, extended thinking, high-stakes judgment. Script-writer, article-writer, structure-checker. |
| **Sonnet** | Orchestration, multi-rule synthesis, research reasoning. Most commands and mid-complexity agents. |
| **Haiku** | Extractive tasks, classification, mechanical edits, schema validation. Pure readers and formatters. |
| **Gemini** | Bulk reading, multi-document context (1M+ tokens), multimodal at scale. Any task consuming >50K tokens of source. |

## Per-agent assignments

| Agent | Assigned Model | Rationale |
|-------|---------------|-----------|
| `script-writer-v2` | **Opus** | 40+ rules, voice-tuned, extended thinking, high-stakes creative output |
| `article-writer` | **Opus** | Voice + NotebookLM citation grounding loop; judgment-heavy |
| `structure-checker-v2` | **Opus** | Extended thinking on retention science; constraint A-BB evaluation |
| `thumbnail-critic` | **Sonnet** | Rubric-scoring against playbook, not generation; Sonnet sufficient |
| `fact-checker` | **Sonnet** | Verdict logic (✅/⏳/❌); bulk source reading offloaded to Gemini |
| `research-organizer` | **Sonnet** | Orchestration; Wikipedia/news/abstract phases offloaded to Gemini |
| `claims-extractor` | **Haiku** | Pure extraction with output schema; cheapest option, no judgment needed |
| `wiki-researcher` | **Haiku** | Brief assembly; Gemini reads the URLs, Haiku formats the structured output |
| `competitor-gap` | **Sonnet** | Gap reasoning vs your script (judgment); transcript ingestion offloaded to Gemini |
| `diy-asset-creator` | **Haiku** | Step-list generation against templates; mechanical |

## Model-budget guardrail

Any executor session that finds itself running **Opus** on a task assigned to Sonnet or Haiku in the execution plan table MUST switch model before continuing:

```
/model sonnet    ← for orchestration, synthesis, research
/model haiku     ← for extraction, file edits, classification
```

Documented here so future sessions inherit the rule. Violation cost: ~10x token premium for no quality gain.

## Gemini dispatch

Headless command: `.claude/commands/gemini.md`
Four task types:
- `digest <transcript-path>` — competitor transcript → hooks/retention/structure
- `ingest <raw-path>` — `~/llm-brain/raw/` or `.brain/_queue/` → wiki page candidates
- `scan <topic>` — pre-greenlight landscape → competitor table
- `quote-mine <source-path>` — academic source → verbatim quotes with page numbers

Output always goes to disk (`.brain/_inbox/` or `_gemini-output/`). Never pipe raw Gemini output back into Claude context.

## Quota notes

Gemini CLI free tier has per-model rate limits (~18-min reset window observed 2026-05-05). Plan calls accordingly:
- Don't fire multiple Gemini calls in tight succession
- For bulk batch work, use `/brain-ingest-batch` which handles rate-limit retries
- If quota exhausted, fall back to Sonnet for the session and schedule Gemini work for next window
