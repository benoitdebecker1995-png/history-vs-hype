---
description: Translate legal/historical documents clause-by-clause with cross-checking, legal annotations, and surprise detection (Untranslated Evidence series)
model: sonnet
---

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
| `--language` | Source language | `--language french` |
| `--narrative` | Expected narrative for surprise detection | `--narrative "Treaty establishes border at river"` |
| `--skip-crosscheck` | Skip the cross-check step | |
| `--skip-annotations` | Skip the legal annotation step | |

---

## TRANSLATE WORKFLOW

### Step 1: Detect Document Structure

Run structure detection to identify clauses, articles, and sections:

```bash
python tools/translation/cli.py detect --file [document-path]
```

- Report to user: "Detected N sections: [section list]"
- If detection fails: **HALT** and report error to user. Do not continue.
- Store sections list for use in Steps 2-5.

### Step 2: Translate Each Clause (Claude Code Native)

For each detected section/clause (work through sequentially — one document at a time, no batch):

**2a. Build the translation payload:**

```bash
python -c "
import sys, json
sys.path.insert(0, 'tools/translation')
from translator import TranslationDataBuilder
builder = TranslationDataBuilder()
payload = builder.build_translation_payload(
    clause_text='[CLAUSE_BODY]',
    full_document='[FULL_DOCUMENT_TEXT]',
    source_language='[LANGUAGE]',
    clause_id='[CLAUSE_ID]',
    document_context='[DOCUMENT_CONTEXT_IF_ANY]'
)
print(json.dumps(payload))
"
```

**2b. Translate using Claude Code natively** (model: claude-sonnet-4-6):

Use the `system_prompt` and `user_prompt` from the payload to call Claude natively. This is a direct Claude Code LLM call — NOT a subprocess or API call.

**2c. Parse the response:**

```bash
python -c "
import sys, json
sys.path.insert(0, 'tools/translation')
from translator import TranslationDataBuilder
builder = TranslationDataBuilder()
result = builder.parse_response(
    response_text='[CLAUDE_RESPONSE_TEXT]',
    clause_id='[CLAUSE_ID]',
    original_text='[ORIGINAL_CLAUSE_TEXT]'
)
print(json.dumps(result))
"
```

**2d. Report progress:** "Translated clause N/M ([clause_id])"

**On translation failure at any clause:** **HALT AND ASK USER**

> "Translation failed for [clause_id]: [error]. Would you like to:
> 1. Retry this clause
> 2. Skip this clause and continue
> 3. Abort the translation
>
> What would you like to do?"

Wait for user response before continuing.

### Step 3: Cross-Check (if not --skip-crosscheck)

For each translated clause, get an independent translation from a secondary backend (DeepL or googletrans) and compare semantically.

**3a. Get secondary translation:**

```bash
python -c "
import sys, json
sys.path.insert(0, 'tools/translation')
from cross_checker import CrossChecker
checker = CrossChecker()
result = checker._translate_with_backend('[ORIGINAL_TEXT]', '[LANGUAGE]')
print(json.dumps(result))
"
```

**3b. Compare semantically** using Claude Code natively (model: claude-sonnet-4-6):

Ask Claude: "Are these two translations of the same [language] source text semantically equivalent? If not, what is the nature and severity of the difference?

Claude translation: [CLAUDE_TRANSLATION]
Secondary translation: [BACKEND_TRANSLATION]

Rate severity: 'minor' (word choice only) or 'significant' (meaning differs)."

**3c. If severity = 'significant': HALT AND ASK USER**

> "Cross-check found a significant discrepancy in [clause_id]:
>
> Claude's translation: [text]
> Secondary translation: [text]
> Difference: [explanation]
>
> Options:
> 1. Accept Claude's translation and continue
> 2. Use the secondary translation
> 3. Review manually (I'll pause here)
>
> What would you like to do?"

Wait for user response before continuing to the next clause.

### Step 4: Legal Annotation (if not --skip-annotations)

For each section, identify and annotate legal terminology, archaic terms, and jurisdiction-specific language.

For each section, call Claude natively (model: claude-sonnet-4-6) with this prompt:

> "Identify legal terms, archaic language, and jurisdiction-specific phrases in this translated clause. For each term:
> - Term: [original term]
> - Definition: [legal/historical definition]
> - Context: [why it matters for this document]
>
> Translation: [CLAUSE_TRANSLATION]
> Original: [CLAUSE_ORIGINAL]"

Attach annotations to the corresponding translation result.

### Step 5: Surprise Detection (if --narrative provided)

For each section, detect clauses that contradict or complicate the expected narrative.

Call Claude natively (model: claude-sonnet-4-6) with this prompt:

> "Given the expected narrative: '[NARRATIVE]'
>
> Does this translated clause contain any surprising, contradictory, or complicating content that challenges that narrative?
>
> Clause: [CLAUSE_TRANSLATION]
>
> Rate severity: 'none', 'minor', or 'high'. For 'high' severity, explain what makes this surprising."

Flag HIGH severity surprises to user immediately:
> "Surprise detected in [clause_id] (HIGH severity): [explanation]. Continuing..."

### Step 6: Format and Save Output

**6a. Format the complete translation:**

```bash
python -c "
import sys, json
sys.path.insert(0, 'tools/translation')
from formatter import Formatter
formatter = Formatter()
sections = [TRANSLATED_SECTIONS_LIST]
output = formatter.format_paired(sections, output_format='markdown')
print(output)
"
```

**6b. Save to project folder:**

Write formatted output to:
`video-projects/_IN_PRODUCTION/[project-folder]/[document-name]-TRANSLATION-FORMATTED.md`

**6c. Report completion:**

> "Translation pipeline complete!
> Output: [path to formatted file]
>
> Next steps:
> - Review the formatted translation in [path]
> - Run `/verify --translation [project]` for verification against scholarly sources
> - When ready: `/script --document-mode` to write the script with primary source integration"

---

## On Pipeline Failure

If any step fails (Step 1-6), **HALT immediately** and report to user:

> "Step N failed: [specific error message].
>
> Would you like to:
> 1. Retry this step
> 2. Skip this step and continue
> 3. Abort the translation
>
> What would you like to do?"

Do NOT auto-continue past errors. The accuracy of translated historical/legal documents is critical.

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

- This command replaces the standalone `python cli.py translate` workflow
- All LLM calls are made by Claude Code natively — no ANTHROPIC_API_KEY needed
- One document at a time — no batch mode
- Cross-check uses DeepL/googletrans for an independent translation + Claude for semantic comparison
- The Python tools (`translator.py`, `formatter.py`, `structure_detector.py`) handle pure data processing only
- The `TranslationDataBuilder` class in `translator.py` builds prompts and parses responses; Claude Code executes the LLM calls
