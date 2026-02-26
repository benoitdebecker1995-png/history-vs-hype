# Phase 54: External Intelligence Synthesis - Research

**Researched:** 2026-02-26
**Domain:** Python CLI tooling — text parsing, script analysis, JSON storage, moderation scoring, markdown generation
**Confidence:** HIGH

---

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

**Prompt Generation Style:**
- Hybrid approach: deep script analysis for VidIQ keyword prompts, template-based for Gemini creative prompts
- Channel context: frame as a channel with no audience yet — avoid advice calibrated for established channels
- VidIQ target: all VidIQ prompts target the VidIQ Pro Coach chat function (not Keyword Inspector or other tools separately)
- Gemini scope: Claude's discretion — use it for whatever it excels at (likely creative ideation, hook angles, audience psychology)
- Competitor context: include competitor data from /intel (intel.db) to ground prompts in what works in the niche
- Don't include: channel's own proven patterns — let tools give fresh perspective without bias
- Auto-detect script length: if script fits VidIQ char limit → include full hook/intro text; if too long → auto-generate topic summary with key entities and claims
- Sequenced workflow: numbered steps with clear order — each prompt builds on previous response; copy-paste ready with instructions
- VidIQ prompt count: Claude's discretion based on VidIQ Pro Coach capabilities
- Focused for VidIQ, single for Gemini: multiple focused prompts for VidIQ, one comprehensive creative brief for Gemini
- Output saved to: `EXTERNAL-PROMPTS.md` in the video project folder
- Prompt versioning: automatic from intake quality — system infers prompt effectiveness from how much of the response was parseable/useful; no manual rating

**Intake Parsing:**
- Input method: copy-paste raw text directly into `/publish --intake`
- Auto-detection: parser identifies whether pasted text is keyword data, title suggestions, thumbnail concepts, etc. based on content patterns (no manual labeling)
- Session flow: one paste at a time with confirmation — system parses, confirms what it extracted, then prompts for next paste
- Storage: JSON file (`EXTERNAL-INTELLIGENCE.json`) in the video project folder

**Synthesis Ranking:**
- Conflict resolution: weigh each source by what it's good at, present recommendations with reasoning, let user decide
- Primary output: 3 distinct title+thumbnail pairings designed for A/B testing
- Variant labeling: each variant labeled by test hypothesis (e.g., "Variant A: Keyword-optimized", "Variant B: Curiosity gap", "Variant C: Authority angle")
- Full metadata package: 3 title+thumbnail pairings PLUS one optimized description and one tag set — complete publish-ready package
- Integration: complements existing `/publish --titles` workflow — adds external intelligence as additional input, doesn't replace it
- Cross-project learning: none for now — each project independent

**Content Moderation Scoring:**
- Scope: full metadata moderation — titles, description, tags, AND thumbnail concepts
- Inline with blueprints: each thumbnail variant includes moderation risk notes
- Safe alternatives: flag trigger words/imagery and suggest alternatives

**Thumbnail Blueprints:**
- Detail level: concept + composition guide (thirds, focal points, color palette, text overlay, asset types)
- Matched to variants: each of the 3 blueprints matched to its paired title variant
- No asset sourcing: describe what's needed, don't source specific URLs
- Text overlay guidance: placement, approximate word count, font style direction, contrast approach per variant
- Mobile considerations: Claude's discretion
- Channel patterns: don't enforce (e.g., map-focused) — treat each project fresh

**AI Thumbnail Generation:**
- Per-element guidance: each blueprint element tagged as AI-generatable or manual Photoshop work
- Available tools: VidIQ image generator + Napkin AI (Nanobanna)
- AI element scope: Claude's discretion per project based on topic sensitivity
- Copy-paste prompts: ready-to-paste image generation prompts for VidIQ/Napkin for each AI-generatable element

### Claude's Discretion

- VidIQ Pro Coach prompt count and focus areas
- Gemini prompt focus areas (creative ideation, hook angles, audience psychology)
- Mobile thumbnail considerations
- AI element scope per project based on topic sensitivity

### Deferred Ideas (OUT OF SCOPE)

- Cross-project learning from synthesis recommendations vs actual CTR/view performance
- Photoshop Generative Fill integration
- Screenshot/OCR intake from VidIQ

</user_constraints>

---

## Summary

Phase 54 automates the manual VidIQ/Gemini metadata workflow that currently takes ~2 hours per video (documented for Gibraltar #35 and Vichy #37). The phase adds two new flags to `/publish`: `--prompts` (generates tailored, copy-paste-ready prompts for VidIQ Pro Coach and Gemini) and `--intake` (parses tool responses into structured JSON). A synthesis engine then merges internal and external intelligence into a ranked, publish-ready metadata package with moderation scoring and Photoshop-ready thumbnail blueprints.

The implementation is entirely Python-based, following existing patterns in `tools/production/`, `tools/intel/`, and `tools/research/nlm_ingest.py`. No new dependencies are required: the codebase already has `tools.production.parser.ScriptParser`, `tools.production.entities.EntityExtractor`, `tools.intel.query` (competitor data), and `tools.intel.kb_store.KBStore` (intel.db access). The storage model mirrors `EXTERNAL-INTELLIGENCE.json` — a simple JSON file per project, analogous to how `nlm_ingest.py` writes per-project review files.

The most architecturally novel piece is the auto-detection parser for intake: it must classify pasted free-text as keyword data, title suggestions, thumbnail concepts, or other categories without any manual labels. The model for this already exists in the codebase (`tools/research/nlm_ingest.py` does the same for NLM output), so the pattern is well-established.

**Primary recommendation:** Build three new Python modules in `tools/production/` — `prompt_generator.py`, `intake_parser.py`, `synthesis_engine.py` — and a new `external_synthesis/` subpackage only if complexity demands it. Wire them into the `/publish` command as `--prompts` and `--intake` flags. Use existing `ScriptParser` + `EntityExtractor` for script analysis; read intel.db via existing `KBStore` for competitor context.

---

## Standard Stack

### Core (all already in pyproject.toml / installed)

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| `re` (stdlib) | stdlib | Pattern matching for intake classification, content moderation | Already used throughout codebase |
| `json` (stdlib) | stdlib | EXTERNAL-INTELLIGENCE.json read/write | Already used in intel/production |
| `pathlib.Path` (stdlib) | stdlib | Project folder resolution | Already used across all modules |
| `dataclasses` (stdlib) | stdlib | Typed result containers | Already used (Entity, TitleVariant, SectionTiming) |
| `tools.production.parser.ScriptParser` | local | Parse script into Section objects | Already exists, already used by metadata.py |
| `tools.production.entities.EntityExtractor` | local | Extract places, people, documents, dates | Already exists |
| `tools.intel.kb_store.KBStore` | local | Read competitor data and outlier patterns from intel.db | Already exists |
| `tools.intel.query` | local | get_competitor_report(), get_niche_report(), get_outlier_report() | Already exists |

### Supporting

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| `tools.production.metadata.MetadataGenerator` | local | Re-use tone filter (_apply_tone_filter) and title variant logic | When filtering synthesized title candidates |
| `tools.intel.topic_vocabulary.classify_title` | local | Classify script topic cluster for targeted prompts | When generating VidIQ prompts — classify topic to target correct cluster |
| `tools.intel.topic_vocabulary.detect_formulas` | local | Identify title formulas from competitor data | When building prompt context |
| `datetime` (stdlib) | stdlib | Timestamp prompt files | Standard |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Custom regex-based intake classifier | spaCy NER or transformers | spaCy is already installed but overkill for classifying 5 response types; regex patterns are transparent and testable |
| JSON file per project (EXTERNAL-INTELLIGENCE.json) | New SQLite table in intel.db or keywords.db | Per-project JSON keeps external data with the project folder — matches existing pattern (vidiq-research.json, _NLM-REVIEW-*.md); simpler to inspect manually |
| New subpackage `tools/production/external_synthesis/` | Three files directly in `tools/production/` | Three flat files are sufficient for this scope; subpackage adds indirection without benefit |

**Installation:** No new packages required. All dependencies are already in `pyproject.toml`.

---

## Architecture Patterns

### Recommended Module Structure

```
tools/production/
├── parser.py          # existing — ScriptParser
├── entities.py        # existing — EntityExtractor
├── metadata.py        # existing — MetadataGenerator
├── editguide.py       # existing
├── broll.py           # existing
├── split_screen_guide.py  # existing
├── prompt_generator.py    # NEW — /publish --prompts
├── intake_parser.py       # NEW — /publish --intake
└── synthesis_engine.py    # NEW — /publish --synthesize (called by --intake after session)

Per-project files (in video project folder):
├── EXTERNAL-PROMPTS.md         # output of --prompts
└── EXTERNAL-INTELLIGENCE.json  # output of --intake sessions
```

### Pattern 1: Script Analysis → Prompt Generation

The `--prompts` flag reads the script, classifies the topic, detects key entities, and generates sequenced copy-paste prompts for VidIQ Pro Coach + one Gemini brief.

**Script analysis pipeline (reuse existing tools):**
```python
# Source: tools/production/parser.py + entities.py (existing)
from tools.production.parser import ScriptParser
from tools.production.entities import EntityExtractor
from tools.intel.kb_store import KBStore
from tools.intel.topic_vocabulary import classify_title, detect_formulas

parser = ScriptParser()
sections = parser.parse_file(script_path)

extractor = EntityExtractor()
entities = extractor.extract_from_sections(sections)

# Get competitor context for prompt grounding
store = KBStore()
# use get_competitor_videos(), get_niche_snapshot() for outlier patterns
```

**VidIQ character limit auto-detection:**
```python
VIDIQ_CHAR_LIMIT = 2000  # VidIQ Pro Coach has a practical limit

def _build_script_context(sections, entities) -> str:
    """Auto-adapts to VidIQ char limit."""
    hook_text = sections[0].content[:500] if sections else ""
    full_intro = "\n".join(s.content for s in sections[:2])

    if len(full_intro) <= VIDIQ_CHAR_LIMIT:
        return full_intro  # Include full hook/intro
    else:
        # Auto-summarize: topic + key entities + core claims
        places = [e.text for e in entities if e.entity_type == 'place'][:3]
        docs = [e.text for e in entities if e.entity_type == 'document'][:3]
        people = [e.text for e in entities if e.entity_type == 'person'][:3]
        return _generate_topic_summary(sections, places, docs, people)
```

**Prompt sequencing (numbered, copy-paste ready):**

VidIQ Pro Coach prompts should be sequenced so each builds on the previous response. Based on the Gibraltar/Vichy manual workflow and VidIQ Pro Coach capabilities, the recommended sequence is:

1. Keyword research prompt (primary keywords, search volume, competition landscape)
2. Title optimization prompt (feed back VidIQ's keyword suggestions, request title variants)
3. Tag strategy prompt (request tag set based on keywords + title selected)
4. Description optimization prompt (SEO-angle description opener)

Each prompt block should include explicit copy-paste instructions:
```
Step 1: Paste into VidIQ Pro Coach. Copy the full response.
[PROMPT TEXT]
---
```

**Gemini creative brief:** One comprehensive prompt covering creative angles VidIQ doesn't address — hook psychology, thumbnail concept angles, curiosity-gap framing, audience emotional triggers. Gemini is better at creative ideation than keyword science.

### Pattern 2: Intake Parser — Auto-Detection

The `--intake` flag accepts raw pasted text and must auto-classify it into one of 5 response types without user labels. This mirrors `nlm_ingest.py`'s approach of detecting structure from content signals.

**Response type classification signals:**

| Type | Detection Signals |
|------|------------------|
| `keyword_data` | Lines containing volume/competition numbers, "search volume", score patterns like "XX/100", keyword lists with metrics |
| `title_suggestions` | Numbered or bulleted title candidates, 40-70 char strings that read as YouTube titles, "Title:" prefix patterns |
| `thumbnail_concepts` | "Thumbnail", "visual", "background", color descriptors, compositional language (left/right, split, overlay) |
| `description_draft` | Multi-paragraph prose with YouTube-style structure (hook + sections + CTA), hashtag blocks |
| `tag_set` | Comma-separated short phrases, or a dense list of 15+ short keyword phrases |

**Detection uses regex scoring (confidence per type):**
```python
def classify_paste(text: str) -> dict:
    """
    Returns: {
        'type': str,  # 'keyword_data' | 'title_suggestions' | etc.
        'confidence': float,  # 0.0-1.0
        'parsed_items': list
    }
    """
```

**Session flow — one paste at a time:**
```
User: /publish --intake
System: "Ready for paste 1. Paste your first VidIQ/Gemini response and press Enter."
[user pastes]
System: "Detected: keyword data (8 keywords with metrics). Confirm? [y/n/edit]"
[user confirms]
System: "Saved to EXTERNAL-INTELLIGENCE.json. Paste 2 (or 'done' to synthesize)."
```

This matches the NLM ingest flow in `nlm_ingest.py` — parse → confirm → persist — which is already proven in production.

**EXTERNAL-INTELLIGENCE.json structure:**
```json
{
  "project": "35-gibraltar-treaty-utrecht-2026",
  "created": "2026-02-26T...",
  "prompt_version": "1",
  "sessions": [
    {
      "session_id": "s1",
      "source": "vidiq_pro_coach",
      "type": "keyword_data",
      "raw": "...",
      "parsed": {
        "keywords": [
          {"term": "gibraltar history", "volume": "12000", "competition": "45", "score": "67"}
        ]
      },
      "parseable_ratio": 0.85,
      "timestamp": "..."
    },
    {
      "session_id": "s2",
      "source": "vidiq_pro_coach",
      "type": "title_suggestions",
      "raw": "...",
      "parsed": {
        "titles": ["Spain's 300-Year Trap...", "The 1713 Document..."]
      },
      "parseable_ratio": 1.0,
      "timestamp": "..."
    },
    {
      "session_id": "s3",
      "source": "gemini",
      "type": "thumbnail_concepts",
      "raw": "...",
      "parsed": {
        "concepts": [
          {"label": "Cartographic Collision", "description": "Vertical split..."}
        ]
      },
      "parseable_ratio": 0.75,
      "timestamp": "..."
    }
  ]
}
```

**Prompt versioning via parseable_ratio:** Each session records `parseable_ratio` (fraction of text that was successfully classified into structured items). Across projects, this tracks which prompt templates produce higher ratios. No manual rating needed — emerges from parse quality.

### Pattern 3: Synthesis Engine

Reads `EXTERNAL-INTELLIGENCE.json` + internal script analysis + optional intel.db data, merges into 3 A/B title+thumbnail pairings.

**Source weighting by what each tool is good at:**

| Source | Weight For |
|--------|-----------|
| VidIQ keyword data | Keyword-optimized variant (highest search volume) |
| VidIQ title suggestions | Discovery-optimized variant |
| Gemini thumbnail/hook | Curiosity-gap and authority variants |
| Internal script analysis (ScriptParser + entities) | Factual accuracy, entity completeness |
| intel.db competitor patterns | Differentiation from competitor title formulas |

**Output structure (3 variants + full package):**
```markdown
## Variant A: Keyword-Optimized
**Title:** Spain's 300-Year Trap: Why They Can't Reclaim Gibraltar (55 chars)
**Moderation:** LOW RISK — no flagged terms
**Thumbnail Blueprint:**
- Concept: [description]
- Composition: Rule of thirds, focal points
- Color palette: [colors]
- Text overlay: "300-YEAR TRAP" — top-left, bold sans-serif, white on dark bg
- Mobile legibility: readable at 120px wide
- AI-generatable elements: [list with prompts]
- Manual Photoshop elements: [list]

## Variant B: Curiosity Gap
...

## Variant C: Authority Angle
...

## Recommended Description (Single Optimized)
...

## Tag Set (Single Optimized)
...
```

### Pattern 4: Content Moderation Scoring

Scan all titles, description, tags, and thumbnail text overlay suggestions for:
- YouTube policy trigger words (monetization flags)
- Topic-specific risks (Holocaust imagery, violent conflict imagery, political content)
- Character limits (title ≤ 70, tags ≤ 500 total chars, individual tags ≤ 30 chars)

**Risk levels:** LOW / MEDIUM / HIGH
**Flag pattern (from existing `metadata.py` CLICKBAIT_PATTERNS approach):**
```python
MODERATION_TRIGGERS = {
    'HIGH': ['genocide', 'massacre', 'holocaust', 'nazi', 'torture', 'execution'],
    'MEDIUM': ['coup', 'assassination', 'war crimes', 'atrocities', 'propaganda'],
    'LOW': ['colonial', 'occupation', 'disputed', 'controversial']
}
```

HIGH-risk terms don't mean "remove" — they mean "flag for user decision with alternatives offered." (Holocaust topics need real photos, not AI-generated imagery; that's a thumbnail blueprint note, not a block.)

### Anti-Patterns to Avoid

- **Blocking generation on missing intel.db:** If intel.db doesn't exist, degrade gracefully — generate prompts without competitor context, note that `/intel --refresh` would improve results. Match `publish.md` pattern: "If file does not exist, skip silently."
- **Requiring the user to label pastes:** Auto-detect type. User only confirms or corrects. Manual labeling defeats the purpose of `--intake`.
- **Generating EXTERNAL-PROMPTS.md without script analysis:** The VidIQ prompts are "tailored" because they include script-derived entities and topic summary. Generic prompts with no script context miss the whole point.
- **One giant function:** Each stage (script analysis, prompt building, intake parsing, synthesis) should be a separate class or function — mirrors the existing `ScriptParser` / `EntityExtractor` / `MetadataGenerator` separation in `tools/production/`.

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Script → structured sections | Custom markdown parser | `tools.production.parser.ScriptParser` | Already exists, handles all bracketed markers, produces Section objects with word counts |
| Entity extraction from script | Custom NER | `tools.production.entities.EntityExtractor` | Already handles places, people, documents, dates with domain keywords |
| Title tone filtering | Custom clickbait detector | `tools.production.metadata.MetadataGenerator._apply_tone_filter()` | Already handles CLICKBAIT_PATTERNS list and acronym preservation |
| Competitor data access | Direct sqlite3 queries | `tools.intel.kb_store.KBStore` | Already abstracts all intel.db queries with error-dict pattern |
| Project folder resolution | Custom path search | Glob-based lookup (existing pattern throughout codebase) | `/publish` already resolves project paths this way |

**Key insight:** 90% of the data pipeline already exists. Phase 54 is primarily about wiring three new modules that call existing tools, not building new capabilities from scratch.

---

## Common Pitfalls

### Pitfall 1: VidIQ Character Limit Assumption

**What goes wrong:** Generating prompts that include full 6,000-word scripts, which exceed VidIQ Pro Coach's character limit, causing truncation or errors on the VidIQ side.
**Why it happens:** The CONTEXT.md notes VidIQ has a character limit but doesn't specify it. The `--prompts` generator must auto-detect script length and switch to summary mode.
**How to avoid:** Define `VIDIQ_CHAR_LIMIT` as a constant (start with 2000 chars for script context block). Use the full hook/intro if it fits; fall back to auto-generated topic summary with key entities if not. Make the constant configurable so user can adjust if they discover the actual limit.
**Warning signs:** Generated EXTERNAL-PROMPTS.md contains a "script context" block longer than 2000 characters.

### Pitfall 2: Intake Parser Over-Confidence

**What goes wrong:** The auto-detector classifies a paste incorrectly (e.g., a title suggestions response classified as keyword data), and the user confirms without noticing, corrupting EXTERNAL-INTELLIGENCE.json.
**Why it happens:** VidIQ Pro Coach responses are free-form prose mixed with lists. A response about keywords may contain title examples; a title response may include keyword metrics.
**How to avoid:** Always show the user the classified type AND a preview of parsed items before saving. The session flow confirmation is the safety net: "Detected: keyword data (8 keywords). First keyword: 'gibraltar history (12,000 vol, 45 comp)'. Confirm? [y/n/edit]"
**Warning signs:** `parseable_ratio` below 0.5 on confirmed sessions.

### Pitfall 3: Synthesis Without Sufficient Intake

**What goes wrong:** User runs `--synthesize` after only one paste session (e.g., just title suggestions), and the synthesis engine produces low-quality output because it lacks keyword or thumbnail data.
**Why it happens:** `--synthesize` doesn't know what data it has until it reads EXTERNAL-INTELLIGENCE.json.
**How to avoid:** Synthesis engine checks data completeness before generating. If missing keyword data: "No keyword data found — VidIQ title variants will lack search volume grounding. Proceed anyway? [y/n]". Minimum: at least 1 session in EXTERNAL-INTELLIGENCE.json.
**Warning signs:** EXTERNAL-INTELLIGENCE.json `sessions` array is empty when `--synthesize` is invoked.

### Pitfall 4: Moderation Over-Flagging

**What goes wrong:** A legitimate academic topic like "Operation Condor" or "Vichy Statute des Juifs" gets flagged as HIGH risk at every turn, making the tool annoying rather than useful.
**Why it happens:** Simple keyword matching doesn't distinguish "The Nazi Party's legal strategy" (legitimate academic content) from genuinely problematic framing.
**How to avoid:** Moderation flags are informational, not blocking. HIGH risk = "flag with note and suggest alternatives" not "prevent generation." The note should be context-aware: "Contains 'Nazi' — YouTube may restrict monetization. Standard for historical/educational content. Thumbnail: use archival photos rather than AI-generated imagery."
**Warning signs:** User never uses moderation output because it flags every video.

### Pitfall 5: EXTERNAL-PROMPTS.md Becoming a Dump

**What goes wrong:** The generated prompt file becomes a 3-page wall of text that the user doesn't actually use because it's too complex to navigate quickly.
**Why it happens:** Prompt generation tries to be thorough without being usable.
**How to avoid:** Structure EXTERNAL-PROMPTS.md with clear numbered steps, explicit "Paste this into VidIQ Pro Coach" instructions, and a visual separator between each prompt block. The Gibraltar YOUTUBE-METADATA.md (14:00 video, manually done) is the benchmark for what good output looks like — it's navigable, scannable, and actionable.
**Warning signs:** EXTERNAL-PROMPTS.md is longer than 200 lines.

---

## Code Examples

Verified patterns from existing codebase:

### Script analysis (existing pattern from metadata.py)
```python
# Source: tools/production/metadata.py (existing)
from tools.production.parser import ScriptParser
from tools.production.entities import EntityExtractor

def analyze_script(script_path: str) -> dict:
    """Returns script sections + entities for prompt generation."""
    parser = ScriptParser()
    sections = parser.parse_file(script_path)

    extractor = EntityExtractor()
    entities = extractor.extract_from_sections(sections)

    total_words = sum(s.word_count for s in sections)

    return {
        'sections': sections,
        'entities': entities,
        'total_words': total_words,
        'hook': sections[0].content[:500] if sections else ""
    }
```

### Error-dict pattern (project standard, from tools/production/* throughout)
```python
# Source: existing pattern throughout codebase (ERR-02 standard)
def generate_prompts(project_path: str, script_path: str) -> dict:
    """Returns {'output_path': str} or {'error': str}."""
    try:
        # ...
        return {'output_path': str(output_path)}
    except FileNotFoundError as e:
        return {'error': f'prompt_generator.generate_prompts: script not found — {e}'}
    except Exception as e:
        return {'error': f'prompt_generator.generate_prompts: unexpected error — {e}'}
```

### Intel.db access (existing KBStore pattern)
```python
# Source: tools/intel/kb_store.py (existing)
from tools.intel.kb_store import KBStore

def get_competitor_context(db_path: str = None) -> dict:
    """Get competitor patterns for prompt grounding. Degrades gracefully."""
    from pathlib import Path
    _default = Path(__file__).parent.parent / "intel" / "intel.db"
    resolved = db_path or str(_default)

    if not Path(resolved).exists():
        return {'available': False, 'note': 'Run /intel --refresh for competitor context'}

    store = KBStore(resolved)
    outliers = store.get_competitor_videos(outliers_only=True, limit=10)
    niche = store.get_latest_niche_snapshot()

    if isinstance(outliers, dict) and 'error' in outliers:
        outliers = []

    return {
        'available': True,
        'outlier_titles': [v.get('title') for v in (outliers or [])],
        'niche_snapshot': niche
    }
```

### JSON file persistence (matches existing vidiq_workflow.py pattern)
```python
# Source: tools/discovery/vidiq_workflow.py (existing pattern)
import json
from pathlib import Path
from datetime import datetime, timezone

def load_or_create_intelligence(project_path: str) -> dict:
    """Load existing EXTERNAL-INTELLIGENCE.json or return empty scaffold."""
    p = Path(project_path) / "EXTERNAL-INTELLIGENCE.json"
    if p.exists():
        try:
            return json.loads(p.read_text(encoding='utf-8'))
        except json.JSONDecodeError:
            return _empty_scaffold(project_path)
    return _empty_scaffold(project_path)

def save_intelligence(data: dict, project_path: str) -> dict:
    """Save to EXTERNAL-INTELLIGENCE.json. Returns {'saved_to': str} or {'error': str}."""
    try:
        p = Path(project_path) / "EXTERNAL-INTELLIGENCE.json"
        p.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
        return {'saved_to': str(p)}
    except Exception as e:
        return {'error': f'save_intelligence: {e}'}
```

### Intake classification (pattern from nlm_ingest.py)
```python
# Source: pattern adapted from tools/research/nlm_ingest.py (existing)
import re

_KEYWORD_SIGNALS = [
    r'\b(?:search\s+volume|monthly\s+searches)\b',
    r'\b\d+\s*/\s*100\b',          # VidIQ score format
    r'\bcompetition[:\s]+\d+',
    r'\bvolume[:\s]+[\d,]+',
]

_TITLE_SIGNALS = [
    r'^[\d]+[\.\)]\s+[A-Z].{20,65}$',  # Numbered title list, 20-65 chars
    r'\bTitle[:\s]',
    r'^\d+\.\s+".{20,65}"',             # Quoted title list
]

def classify_response_type(text: str) -> tuple[str, float]:
    """
    Returns (type_name, confidence).
    Types: 'keyword_data', 'title_suggestions', 'thumbnail_concepts',
           'description_draft', 'tag_set', 'unknown'
    """
    scores = {}
    for rtype, patterns in [
        ('keyword_data', _KEYWORD_SIGNALS),
        ('title_suggestions', _TITLE_SIGNALS),
        # ... etc
    ]:
        score = sum(1 for p in patterns if re.search(p, text, re.MULTILINE | re.IGNORECASE))
        scores[rtype] = score / len(patterns)

    best = max(scores.items(), key=lambda x: x[1])
    if best[1] < 0.25:
        return 'unknown', best[1]
    return best[0], best[1]
```

---

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Manual VidIQ research workflow via `vidiq_workflow.py` (Keyword Inspector focus) | VidIQ Pro Coach chat prompts (broader, conversational) | CONTEXT.md decision | Old module targeted wrong VidIQ function; new module targets Pro Coach |
| Thumbnail strategy as unstructured notes in YOUTUBE-METADATA.md | Structured blueprint with per-element AI tagging | Phase 54 decision | Enables AI image generation prompts per element |
| No moderation scoring | Inline risk flags in synthesis output | Phase 54 decision | Prevents demonetization surprises |
| External tool responses manually typed into YOUTUBE-METADATA.md | Parsed JSON (EXTERNAL-INTELLIGENCE.json) → synthesis engine | Phase 54 decision | Machine-readable enables synthesis ranking |

**Deprecated/outdated:**
- `tools/discovery/vidiq_workflow.py` interactive data collection: targets VidIQ Keyword Inspector, not Pro Coach; its `parse_vidiq_response` simple key:value parser won't handle Pro Coach's rich prose responses. Phase 54 `intake_parser.py` supersedes it for the VidIQ workflow. The old module can remain for users who still use Keyword Inspector separately.

---

## Open Questions

1. **VidIQ Pro Coach actual character limit**
   - What we know: CONTEXT.md notes the limit exists and `--prompts` must auto-adapt
   - What's unclear: Exact character limit (2000? 4000? Token-based?)
   - Recommendation: Default to 2000 chars for script context. Make `VIDIQ_CHAR_LIMIT` a named constant so user can adjust after first production use. Document: "If VidIQ truncates your prompt, reduce VIDIQ_CHAR_LIMIT in tools/production/prompt_generator.py"

2. **`--synthesize` as separate flag or automatic after `--intake done`**
   - What we know: CONTEXT.md describes `--intake` session flow ending with 'done' → synthesize
   - What's unclear: Whether synthesis should be automatic after `done` or require explicit `--synthesize` flag
   - Recommendation: Auto-synthesize on 'done' in the `--intake` session flow. No separate flag needed — synthesis is the natural end of an intake session. Add `--synthesize` as an alias for re-running synthesis on existing EXTERNAL-INTELLIGENCE.json.

3. **Project path resolution for `--prompts` and `--intake`**
   - What we know: Other `/publish` flags accept optional project name as positional argument
   - What's unclear: Whether to accept project folder name or use interactive selection
   - Recommendation: Follow `/publish --metadata [project]` pattern exactly. Accept optional project slug. If not provided, prompt interactively (same as existing `/publish` behavior).

---

## Sources

### Primary (HIGH confidence)

- `G:/History vs Hype/tools/production/metadata.py` — MetadataGenerator, title variant logic, tone filter
- `G:/History vs Hype/tools/production/parser.py` — ScriptParser, Section dataclass, strip_for_teleprompter
- `G:/History vs Hype/tools/production/entities.py` — EntityExtractor, Entity dataclass
- `G:/History vs Hype/tools/intel/kb_store.py` — KBStore, intel.db schema (5 tables)
- `G:/History vs Hype/tools/intel/query.py` — All public query functions, error-dict pattern
- `G:/History vs Hype/tools/research/nlm_ingest.py` — NLMParser, paste-and-confirm session flow
- `G:/History vs Hype/tools/discovery/vidiq_workflow.py` — Existing VidIQ workflow, JSON save pattern
- `G:/History vs Hype/.claude/commands/publish.md` — /publish command flags, existing intelligence context patterns
- `G:/History vs Hype/video-projects/_IN_PRODUCTION/35-gibraltar-treaty-utrecht-2026/YOUTUBE-METADATA.md` — Real example of manually-created metadata (the benchmark for output quality)
- `G:/History vs Hype/.planning/phases/54-external-intelligence-synthesis/54-CONTEXT.md` — All user decisions

### Secondary (MEDIUM confidence)

- `G:/History vs Hype/.planning/REQUIREMENTS.md` — v5.1 requirements (ERR, LOG, CLI standards that new modules must follow)
- `G:/History vs Hype/.planning/STATE.md` — Phase order, accumulated decisions
- `G:/History vs Hype/tools/intel/competitor_patterns.py` — classify_all_videos pattern, topic cluster approach

---

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — all libraries are already installed and used in the codebase
- Architecture: HIGH — patterns directly mirror existing modules (nlm_ingest, vidiq_workflow, MetadataGenerator)
- Pitfalls: HIGH for char limit and over-flagging (confirmed from CONTEXT.md specifics); MEDIUM for intake classifier accuracy (depends on VidIQ Pro Coach output format, which will vary)

**Research date:** 2026-02-26
**Valid until:** 2026-03-26 (stable domain — no external API dependencies)
