---
name: source-command-translate
description: "Clause-by-clause translation of legal or historical documents with cross-checking, legal annotations and surprise detection. Use when: working on an Untranslated Evidence episode, or a primary source needs a defensible translation with a published PDF."
---

> **Codex note.** This is the Codex port of `.claude/commands/translate.md`, which stays canonical.
> The procedure below is that file verbatim. While running here: a `/name` reference is the
> `source-command-name` skill in `.agents/skills/`; "the Task tool" means spawning a Codex agent
> from `.codex/agents/`; "Claude" means you.

# /translate - Document Translation Pipeline

Translate legal/historical documents clause-by-clause with cross-checking, legal annotations, and surprise detection. All LLM calls are made by Claude Code natively — no API key needed.

## Usage

```
/translate [project-folder] --file [document-path] --language [source-language]
/translate [project-folder] --file [document-path] --language [source-language] --narrative "expected narrative"
```

## Flags

| Flag | Purpose | Example |
|------|---------|---------|
| `--file` | Path to document file | `--file treaty.txt` |
| `--language` | Source language | `--language ukrainian` |
| `--narrative` | Expected narrative for surprise detection | `--narrative "Treaty establishes border at river"` |
| `--skip-crosscheck` | Skip the cross-check step | |
| `--skip-annotations` | Skip the legal annotation step | |

---

## Architecture (READ FIRST)

The pipeline was **consolidated (TRAN-PIPE)** into a single module. There are no longer separate `structure_detector.py` / `cross_checker.py` / `legal_annotator.py` / `surprise_detector.py` / `formatter.py` files — all of those are now **classes embedded in `tools/translation/pipeline.py`**.

**Import map (use these — the old standalone-module imports are gone):**

```python
from tools.translation.pipeline import (
    DocumentTranslationPipeline,   # orchestrator — builds every stage's payloads
    StructureDetector, CrossChecker, LegalAnnotator, SurpriseDetector, Formatter,
)
from tools.translation.translator import TranslationDataBuilder   # parse LLM responses
```

**The Python layer builds payloads; Claude Code executes the LLM calls natively.** Each stage returns a `{clause_id, system_prompt, user_prompt}` payload. Claude runs `system_prompt` + `user_prompt` (model: claude-sonnet-4-6), then a `parse_*` method turns the response back into structured data.

**Run the CLI as a module** (relative imports — `python tools/translation/cli.py …` fails with `ModuleNotFoundError: No module named 'tools'`):

```bash
python -m tools.translation.cli detect --file [document-path] --json   # structure only, standalone
python -m tools.translation.cli smoketest                              # health check, no credentials
```

---

## TRANSLATE WORKFLOW

Work through **one document at a time** — no batch mode. Carry a single `sections` list through all steps: each step enriches the same section dicts (`translation`, `notes`, `footnotes`, cross-check/surprise verdicts), and Step 6 formats them.

### Step 1 — Detect structure + build translation payloads

```bash
python - <<'PY'
from tools.translation.pipeline import DocumentTranslationPipeline
text = open('[document-path]', encoding='utf-8').read().strip()
pipe = DocumentTranslationPipeline(project_dir='[project-folder]')
res = pipe.run_pipeline(text, source_language='[language]', stages=['detect', 'translate'])
# res['detected_structure']['sections'] = the clause list
# res['sections'][i]['translation_payload'] = {clause_id, original, system_prompt, user_prompt}
PY
```

- Report to user: `"Detected N sections: [heading list]"`.
- If `res['error']` is set: **HALT** and report. Do not continue.
- `run_pipeline(..., stages=['detect','translate'])` returns each section with a `translation_payload`. (Downstream cross-check/annotate/surprise payloads read `section['translation']`, which is empty until Step 2 fills it — so build those in Steps 3–5 **after** translating, not in this call.)

### Step 2 — Translate each clause (Claude Code native)

For each section, execute `section['translation_payload']` natively (model: claude-sonnet-4-6): feed `system_prompt` + `user_prompt` to Claude, then parse:

```python
from tools.translation.translator import TranslationDataBuilder
builder = TranslationDataBuilder()
parsed = builder.parse_response(response_text='[CLAUDE_RESPONSE]', clause_id='[ID]', original_text='[CLAUSE_BODY]')
# → {'clause_id','original','translation','notes'}
section['original']    = section['body']
section['translation'] = parsed['translation']
section['notes']       = parsed['notes']
```

- Report progress: `"Translated clause N/M ([clause_id])"`.
- **On translation failure at any clause — HALT AND ASK USER** (retry / skip / abort). Wait for the reply.

### Step 3 — Cross-check (if not `--skip-crosscheck`)

⚠ **No external MT engine is wired.** The consolidated `CrossChecker` has no `_translate_with_backend` and `run_pipeline` passes an empty `backend_translation`; there is no DeepL/googletrans call. So the cross-check is a **Claude dual-pass self-consistency review**: Claude produces a second, independent literal translation of the clause, then compares the two. For load-bearing verbatims (esp. non-English cards going on screen) the **authoritative fidelity gate is the human Check-A**, not this step. Say so in the output.

```python
from tools.translation.pipeline import CrossChecker
cc = CrossChecker()   # optionally CrossChecker(deepl_api_key=...) if DEEPL_AUTH_KEY is ever set
payload = cc.build_comparison_payload(
    claude_translation=section['translation'],
    backend_translation='[CLAUDE_SECOND_PASS]',   # independent native re-translation
    original_text=section['body'],
    clause_id=section['id'],
    source_language='[language]',
    backend='claude-dual-pass',
)
# execute payload natively, then:
verdict = cc.parse_comparison_response(response_text='[CLAUDE_RESPONSE]', clause_id=section['id'])
section['cross_check'] = verdict   # {has_discrepancy, severity, explanation, recommendation}
```

- **If `verdict['severity'] == 'significant'` — HALT AND ASK USER** (accept Claude's / use the second pass / review manually). Wait for the reply.

### Step 4 — Legal annotation (if not `--skip-annotations`)

```python
from tools.translation.pipeline import LegalAnnotator
ann = LegalAnnotator()
payload = ann.build_annotation_payload(
    clause_text=section['body'], translation=section['translation'],
    clause_id=section['id'], source_language='[language]',
)
# execute payload natively, then:
result = ann.parse_annotation_response(response_text='[CLAUDE_RESPONSE]', clause_id=section['id'])
section['footnotes'] = result['footnotes']   # Formatter renders these under the clause
```

### Step 5 — Surprise detection (if `--narrative` provided)

```python
from tools.translation.pipeline import SurpriseDetector
sd = SurpriseDetector()
payload = sd.build_surprise_payload(
    clause_text=section['body'], translation=section['translation'],
    narrative_baseline='[NARRATIVE]', clause_id=section['id'], source_language='[language]',
)
# execute payload natively, then:
surprise = sd.parse_surprise_response(response_text='[CLAUDE_RESPONSE]', clause_id=section['id'],
                                      original=section['body'], translation=section['translation'])
section['surprise'] = surprise
```

- Flag `severity in ('major','notable')` to the user immediately:
  > "Surprise detected in [clause_id] ([severity]): [explanation]."

  (A predicate/attribution mismatch on an on-screen card — e.g. "the Polish *element*" vs "population", or "resurrected Poland" vs the document's actual named enemy — surfaces here.)

### Step 6 — Format and save

```python
from tools.translation.pipeline import Formatter
out = Formatter().format_paired(sections, output_format='markdown')
# Formatter reads section['heading'], section['original'], section['translation'],
# and section['footnotes'] (or section['notes']).
open('video-projects/_IN_PRODUCTION/[project-folder]/[document-name]-TRANSLATION-FORMATTED.md',
     'w', encoding='utf-8').write(out)
```

Report completion:

> "Translation pipeline complete. Output: [path]
> Non-English on-screen cards are DRAFTS — route through the native-speaker **Check-A** before any card locks.
> Next: `/verify --translation [project]`, then `/script --document-mode`."

---

## On Pipeline Failure

If any step fails, **HALT immediately** and report:

> "Step N failed: [error]. Options: 1) Retry 2) Skip 3) Abort. What would you like to do?"

Do NOT auto-continue past errors. Translated historical/legal documents are load-bearing on screen.

---

## Model Selection Per Step

| Step | Model | Reasoning |
|------|-------|-----------|
| Step 2: Translation | claude-sonnet-4-6 | Nuanced legal/historical language requires quality |
| Step 3: Cross-check comparison | claude-sonnet-4-6 | Semantic comparison accuracy |
| Step 4: Legal annotation | claude-sonnet-4-6 | Legal terminology expertise |
| Step 5: Surprise detection | claude-sonnet-4-6 | Contextual reasoning about narratives |

---

## Notes

- Pipeline entry point: `DocumentTranslationPipeline` in `tools/translation/pipeline.py` (all stage classes consolidated there).
- `TranslationDataBuilder` lives in `tools/translation/translator.py` (payload build + response parse for the translate stage).
- `cli.py` exposes only the credential-free `detect` and `smoketest`; the LLM stages run through this command. Invoke the CLI as a module: `python -m tools.translation.cli …`.
- Health check: `python -m tools.translation.cli smoketest` (expects 4/4).
- All LLM calls are made by Claude Code natively — no ANTHROPIC_API_KEY needed.
- One document at a time — no batch mode.
- **Cross-check is Claude-only** (no external engine wired) — the human Check-A is the real fidelity gate for on-screen verbatims. For a worked pass, see `video-projects/_IN_PRODUCTION/62-volhynia-massacre-untranslated-2026/_research/translations/` (the 2026-07-24 UA pass: source `.txt`s → `UA-CARD-VERBATIMS-TRANSLATION-2026-07-24.md`).
