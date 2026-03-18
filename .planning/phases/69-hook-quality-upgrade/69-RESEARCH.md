# Phase 69: Hook Quality Upgrade - Research

**Researched:** 2026-03-18
**Domain:** Python tool development — hook scoring, LLM-based text generation, CLI command extension
**Confidence:** HIGH

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

**Title-Fulfillment Check (HOOK-01)**
- Dual check: both entity echo AND promise-type alignment must pass
- Entity echo: at least one key entity from the title must appear in the hook's first ~50 words
- Promise-type match: categorize title promise (mechanism, document, conflict, myth-bust) and verify hook delivers the same type
- "Document Reveal" alignment: hook's specific anomaly should connect to title's systemic scope
- Title is a required parameter for the fulfillment check; without a title hook_scorer still works but skips fulfillment dimension
- Mismatch output: name the specific gap AND suggest a fix

**4-Layer Framework Integration (replaces current beat detection)**
- Replace _detect_beats() entirely with "Document Reveal" framework detection
- New structure elements: anomaly (specific document/map/detail), stakes connection (systemic consequence), inciting incident (the "turn" within ~45 seconds)
- Point distribution within existing 40-point beat_score budget is Claude's discretion
- Library categories (cold_fact, myth_contradiction, etc.) are preserved for style recommendation; framework = scoring structure, library = style vocabulary

**/script --hooks Command**
- Dual function: score existing hook AND generate alternative variants
- Input: script path + title via --title flag; title required for fulfillment check
- Existing hook extraction: read first ~300 words of script
- Always generate alternatives; urgency level based on existing hook score (thresholds Claude's discretion)
- Topic type: auto-detect from script content, --topic flag overrides (same pattern as Phase 67)

**Hook Variant Generation**
- LLM-generated from script material, not template-based
- Variant count: Claude's discretion based on script richness
- Style coverage: lead with recommended style for topic type, then include others
- Variant length: Claude's discretion per style
- Output: spoken text only (no [VISUAL] or [AUDIO] cues)
- Every variant auto-scored against upgraded hook_scorer

**Style Recommendation (HOOK-02)**
- Recommendation banner at top of output with 2-3 first-sentence examples from HOOK-PATTERN-LIBRARY.md, shown BEFORE the score
- Format: "Topic type: territorial → Recommended style: cold_fact" + real examples with view counts
- Score impact: +5 when matching and library has 7+ examples (advisory-only when <5); -5 penalty for mismatch at high confidence
- Topic-to-style mapping: territorial → cold_fact, ideological → myth_contradiction, political_fact_check → specificity_bomb

### Claude's Discretion
- Framework-to-score point distribution (anomaly/stakes/inciting incident within 40-point budget)
- Number of hook variants to generate
- Variant length per style
- Urgency flag score thresholds
- Detection patterns for anomaly, stakes connection, and inciting incident
- Topic auto-detection keyword lists

### Deferred Ideas (OUT OF SCOPE)
- HOOK-03: 4-beat completeness check (future requirement)
- HOOK-04: "Authority stack" hook template
- [VISUAL]/[AUDIO] cue generation for hooks (belongs in /prep)
- script-writer-v2 Rule 19 update (separate task)
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| HOOK-01 | Hook scorer verifies first sentence/5 seconds matches the title's promise (catches the 17% dropout from title-fulfillment mismatch) | Entity echo via EntityExtractor from metadata.py; promise-type classification via keyword matching; mismatch reporting pattern from Phase 67 gap_message design |
| HOOK-02 | Hook generator recommends style based on topic type (cold_fact for territorial, myth-contradiction for ideological, specific-claim for political fact-check) | HOOK-PATTERN-LIBRARY.md has programmatic parsing format; topic-to-style mapping confirmed by niche-hook-patterns.md topic distribution data; confidence-based scoring follows Phase 67 benchmark_store fallback pattern |
</phase_requirements>

---

## Summary

Phase 69 upgrades `tools/research/hook_scorer.py` and implements the `/script --hooks` command end-to-end. Two work streams run independently: (1) replacing the existing 4-beat detection with the user's 3-element "Document Reveal" framework and adding title-fulfillment and style-recommendation dimensions to the scorer, and (2) building the CLI command that extracts a script's opening hook, calls the upgraded scorer, generates LLM-written alternative variants, auto-scores each, and presents the ranked output.

The codebase provides strong foundations. The Phase 68 TitleMaterialExtractor already extracts entities, numbers, and contradictions from scripts — the same material drives hook fulfillment checks. EntityExtractor (metadata.py/entities.py) handles title entity extraction. The HOOK-PATTERN-LIBRARY.md is explicitly formatted for programmatic parsing. The topic-type detection keyword pattern from title_scorer.py is directly extensible to script-content detection. No new third-party dependencies are required.

The main design decision is point allocation within the 40-point beat_score budget between anomaly, stakes, and inciting_incident. A balanced 15/15/10 split is defensible: the anomaly and stakes elements correspond to the "cold_fact + myth" two-beat opening sequence (historically the highest-value beats in engagement data), while inciting_incident is the payoff pivot. The command outputs spoken text variants only; all visual staging belongs in /prep.

**Primary recommendation:** Build hook_scorer.py upgrade and /script --hooks command as two separate plan files. Plan 01 upgrades the scorer module (framework replacement + fulfillment + style recommendation + tests). Plan 02 implements the CLI command that calls the upgraded scorer.

---

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Python stdlib (re, typing) | 3.12 | Pattern matching for framework detection | Already the only dependency in hook_scorer.py |
| tools.production.parser.ScriptParser | existing | Extract hook text (~300 words) from script | Already used in /script command; confirmed working |
| tools.production.entities.EntityExtractor | existing | Extract entities from title for fulfillment check | Confirmed in metadata.py — designed for exactly this |
| tools.production.title_generator.TitleMaterialExtractor | existing Phase 68 | Extract specific numbers, documents, contradictions | Identical material needed for hook variant generation |
| tools.title_scorer.detect_pattern | existing | Topic type detection keyword logic | Direct extension of Phase 67 pattern |
| unittest + unittest.mock | stdlib | Tests — no new framework needed | Established pattern in tests/unit/ |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| pathlib.Path | stdlib | Script path resolution | Same pattern as all other tools |
| json | stdlib | Structured output for programmatic consumers | Only if CLI needs machine-readable output flag |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| EntityExtractor for title parsing | Manual regex | EntityExtractor already handles people/places/documents; regex would duplicate logic |
| Extending hook_scorer.py | New file | Single module keeps scorer interface stable; external callers unaffected |
| Template-based variants | LLM generation | Context.md mandates LLM generation from script material (same philosophy as Phase 68 title candidates) |

**Installation:** No new packages required.

---

## Architecture Patterns

### Recommended Module Structure

```
tools/research/hook_scorer.py      # Upgraded: replace _detect_beats, add fulfillment + style dims
tests/unit/test_hook_scorer.py     # New: tests for all upgraded dimensions
.claude/commands/script.md         # Updated: --hooks flag description (variant count, --title flag)
```

### Pattern 1: Scorer Dimension Extension (same pattern as Phase 67)

**What:** Add new scoring dimensions as additive keys to the existing result dict. Existing keys unchanged. New dimensions have their own max budget and are summed into total_score.

**When to use:** Any time a new evaluation axis is added to an existing scorer.

**Example (from existing hook_scorer.py pattern):**
```python
# Source: tools/research/hook_scorer.py (current structure)
result: Dict[str, Any] = {
    'label': label,
    'total_score': 0,
    'beat_score': 0,        # was 0-40, will be replaced by framework_score
    'pattern_score': 0,
    'authority_score': 0,
    'gap_score': 0,
    # NEW dimensions added without renaming existing keys:
    'fulfillment_score': 0,    # 0-10 (additive)
    'style_score': 0,          # -5 to +5 (additive)
    'framework': {},           # replaces 'beats'
    'fulfillment': {},         # entity echo + promise type results
    'style_recommendation': {},
    'issues': [],
    'strengths': [],
}
```

### Pattern 2: Framework-Based Detection (replaces _detect_beats)

**What:** Replace the 4 boolean beat flags with 3 float-scored elements: anomaly, stakes, inciting_incident. Each maps to a point allocation within 40-point budget.

**When to use:** Scoring a hook for quality of its structural progression.

**Proposed point allocation (Claude's discretion applied):**
```python
# anomaly: 0-15 pts — specific localized detail (map line, telegram, redacted sentence)
# stakes:  0-15 pts — systemic consequence connection
# inciting_incident: 0-10 pts — turn/pivot within ~45 seconds (~112 words)
FRAMEWORK_WEIGHTS = {
    'anomaly': 15,
    'stakes': 15,
    'inciting_incident': 10,
}
```

Detection signals:
- **anomaly**: specific year/number in first 30 words, named document/map, hyper-specific place
- **stakes**: physical consequence language ("which meant", "this determined", "controlled", "shut off", "resource"), systemic scale words ("empire", "entire", "all of", "million")
- **inciting_incident**: turn/pivot language within first 112 words ("but", "except", "until", "the problem was", "that's when", "here's what", "what actually")

### Pattern 3: Entity Echo Check (HOOK-01)

**What:** Extract entities from title using EntityExtractor, then check if at least one appears in the hook's first 50 words. Case-insensitive substring match is sufficient.

**When to use:** Any time a title is passed to score_hook().

**Example:**
```python
# Source: adapted from tools/production/entities.py EntityExtractor pattern
from tools.production.entities import EntityExtractor

def _check_entity_echo(title: str, hook_text: str) -> Dict[str, Any]:
    extractor = EntityExtractor(use_spacy=False)
    entities = extractor.extract(title)
    first_50 = ' '.join(hook_text.split()[:50]).lower()
    matched = [e for e in entities if e.text.lower() in first_50]
    return {
        'passed': bool(matched),
        'matched_entities': [e.text for e in matched],
        'title_entities': [e.text for e in entities],
    }
```

### Pattern 4: Promise-Type Classification (HOOK-01)

**What:** Classify the title's promise type (mechanism/document/conflict/myth-bust) by keyword matching, then verify the hook's first 50 words contain language of the same type.

**Promise types and title signals:**
```
mechanism:   "how", "why", "what made", "the reason"
document:    "law", "treaty", "telegram", "document", "statute", "decree", "map"
conflict:    "vs", "versus", "war", "rivalry", "divided", "split between"
myth-bust:   "myth", "truth", "real", "actually", "wasn't", "never"
```

**Hook signals per type:**
```
mechanism:  causal language ("because", "which meant", "thereby", "led to")
document:   named document/object in first 50 words
conflict:   two entities in opposition within first 50 words
myth-bust:  existing-belief language ("you've heard", "most people", "standard answer")
```

### Pattern 5: Style Recommendation with Confidence-Based Scoring

**What:** Read HOOK-PATTERN-LIBRARY.md at runtime, count examples per pattern per topic type, apply score modifier based on confidence level.

**When to use:** Called at start of score_hook() when topic_type is provided.

**Confidence thresholds (from HOOK-PATTERN-LIBRARY.md data):**
```
Pattern examples in library:
- cold_fact:           7 examples → HIGH confidence (≥7)
- contextual_opening:  8 examples → HIGH confidence (≥7)
- myth_contradiction:  4 examples → LOW confidence (<5)
- specificity_bomb:    3 examples → LOW confidence (<5)
- authority_challenge: 0 examples → NO DATA

Score modifiers:
- HIGH confidence + style matches recommendation: +5
- HIGH confidence + style mismatches:             -5
- LOW confidence (< 5 examples):                  advisory-only, no score impact
```

**Topic-to-style mapping (from niche-hook-patterns.md topic distributions):**
```python
TOPIC_STYLE_MAP = {
    'territorial':          'cold_fact',          # 6/7 cold_fact examples are territorial
    'ideological':          'myth_contradiction',  # mapped per CONTEXT.md
    'political_fact_check': 'specificity_bomb',   # mapped per CONTEXT.md
    'general':              None,                 # no recommendation
}
```

### Pattern 6: /script --hooks CLI Command

**What:** CLI entry point that reads a script file, extracts the opening ~300 words, calls score_hook(), generates LLM-written variants via Claude invocation, scores each variant, and displays ranked output.

**Dual-function flow:**
```
1. Locate script (glob for SCRIPT.md in project folder)
2. Extract first ~300 words using strip_for_teleprompter() + word split
3. Load topic_type: auto-detect from script content (keyword match), --topic overrides
4. Call upgraded score_hook(existing_hook, title=title, topic_type=topic_type)
5. Show style recommendation banner (from score result)
6. Show existing hook score
7. Determine urgency flag from score (thresholds TBD at implementation)
8. Generate N variants (N = script richness heuristic) via LLM:
   - Lead with recommended style for topic type
   - Include 2-3 other style variants
   - Use "Document Reveal" framework as generation guidance
   - Brand voice: "Forensic, intelligent, skeptical. Bureaucratic Horror."
9. Auto-score each variant
10. Display ranked comparison table
```

### Anti-Patterns to Avoid

- **Importing hook_scorer from inside script-writer-v2 agent:** Hook scoring runs after agent generation, not inside — this is an existing architectural decision (STATE.md: "Hook scoring runs after agent generation, not inside the agent"). Never add score_hook() calls inside script generation.
- **Regenerating HOOK-PATTERN-LIBRARY.md in tests:** Read the file at runtime; don't cache or embed its content in code. The library is intentionally a human-editable file.
- **Hard-blocking on missing title:** score_hook() must work without a title (skip fulfillment dimension). Never raise an exception when title is None.
- **Visual/audio cues in generated variants:** Spoken text only. [VISUAL] and [AUDIO] belong in /prep command, explicitly deferred.

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Entity extraction from title | Regex named entity parser | EntityExtractor (use_spacy=False) | Already handles people/places/documents; use_spacy=False avoids spaCy dependency |
| Script section parsing | Manual line-by-line reader | ScriptParser.parse_file() | Handles YAML frontmatter, markdown headings, B-roll markers correctly |
| Script text cleaning | Manual strip functions | strip_for_teleprompter() | Already tested; handles all bracketed markers |
| Number/document extraction for variants | New extractor | TitleMaterialExtractor | Phase 68 already extracts the same material needed for hook generation |
| Topic keyword detection | New keyword list | Extend title_scorer.detect_pattern() keyword lists | Same detection logic; avoids two divergent keyword inventories |
| Test scaffolding | New pytest config | Existing tests/unit/ pattern with unittest + patch | All Phase 67/68 tests use this pattern; pytest discovers them automatically |

**Key insight:** The Phase 67/68 architecture anticipated Phase 69. EntityExtractor, ScriptParser, TitleMaterialExtractor, and the topic detection pattern are all reusable without modification.

---

## Common Pitfalls

### Pitfall 1: Breaking Existing score_hook() Callers
**What goes wrong:** Adding required parameters (title, topic_type) to score_hook() breaks the /script --hooks command documented in script.md which calls score_hook() without them.
**Why it happens:** Scorer upgrade adds new parameters but doesn't default them to None.
**How to avoid:** All new parameters must have None defaults. score_hook(text, label='', title=None, topic_type=None). Fulfillment check is skipped when title is None; style recommendation skipped when topic_type is None.
**Warning signs:** Any test importing score_hook with 1-2 positional args fails.

### Pitfall 2: Total Score Exceeds 100
**What goes wrong:** Adding fulfillment_score (0-10) and style_score (-5/+5) to existing 100-point budget pushes total above 100 or creates inconsistent max.
**Why it happens:** Additive dimensions without budget reconciliation.
**How to avoid:** Two options — (a) cap total at 100 with min/max, or (b) document new max as 115 and update grade thresholds proportionally. Option (a) is simpler and preserves backward compat for any threshold checks. Apply min(115, max(0, total)) or simply reframe: fulfillment and style are displayed as separate columns, not added to the headline score.
**Recommended approach:** Keep headline score as original 100-point total. Fulfillment and style display as separate pass/fail flags rather than points. This keeps score meaning stable and matches the CONTEXT.md output requirements (fulfillment = pass/fail flag, style = recommendation banner — neither is described as a point addition).

### Pitfall 3: HOOK-PATTERN-LIBRARY.md Parse Failures
**What goes wrong:** Parser breaks when pattern sections have varying whitespace or the "authority_challenge" pattern has zero examples.
**Why it happens:** Brittle regex on the library format.
**How to avoid:** Parse the file by section delimiter `## Pattern:` and handle the "No verified examples" case explicitly. The library's usage notes document the exact grep target: `## Pattern: {name}`.

### Pitfall 4: First ~300 Words Include Markdown/B-roll Markers
**What goes wrong:** Hook text extracted for scoring contains `[B-ROLL: ...]` or `**[ON-CAMERA]**` markers, poisoning pattern detection.
**Why it happens:** Naive word-split on raw SCRIPT.md.
**How to avoid:** Always run strip_for_teleprompter() before taking the first 300 words. This is established in the existing /script --hooks description in script.md.

### Pitfall 5: Entity Echo False Positives from Short Titles
**What goes wrong:** Title "Haiti" matches "Haiti" mentioned in a geographic context sentence, producing a false pass even though the hook opens with unrelated content.
**Why it happens:** Substring matching on common proper nouns.
**How to avoid:** The dual-check design (entity echo AND promise-type alignment) handles this — a hook that mentions Haiti but opens with generic context will fail the promise-type check even if it passes entity echo. Document this in the scorer's docstring.

### Pitfall 6: intel.db Migration Mentioned in STATE.md
**What goes wrong:** STATE.md notes "intel.db schema version 2 — Phase 69 will migrate to v3 (competitor_hooks table)". A plan implementing hook_scorer.py may inadvertently skip this.
**Why it happens:** STATE.md migration note is easy to miss.
**How to avoid:** The migration is only needed if hook variants are persisted to intel.db. CONTEXT.md does not specify persistence — variants are output to terminal. If logging is added later (BENCH-05 future requirement), the migration belongs there. Phase 69 plans should NOT include the intel.db migration unless CONTEXT.md explicitly requires it.

---

## Code Examples

### Upgraded score_hook() Signature
```python
# Source: tools/research/hook_scorer.py (Phase 69 target)
def score_hook(
    text: str,
    label: str = '',
    title: Optional[str] = None,       # NEW: for HOOK-01 fulfillment check
    topic_type: Optional[str] = None,  # NEW: for HOOK-02 style recommendation
) -> Dict[str, Any]:
    """Score a single hook against channel data patterns.

    Returns dict with:
        - total_score (0-100)         — unchanged
        - framework_score (0-40)      — replaces beat_score
        - pattern_score (0-30)        — unchanged
        - authority_score (0-15)      — unchanged
        - gap_score (0-15)            — unchanged
        - framework: {anomaly, stakes, inciting_incident} — replaces beats
        - fulfillment: {passed, entity_echo, promise_type} — NEW (omitted if title=None)
        - style_recommendation: {...} — NEW (omitted if topic_type=None)
        - issues: list of problems
        - strengths: list of positives
    """
```

### Framework Detection Skeleton
```python
# Source: architectural decision — maps to existing beat_score budget
def _detect_framework(text: str) -> Dict[str, Any]:
    """Detect Document Reveal framework elements in hook text."""
    words = text.split()
    first_30 = ' '.join(words[:30]).lower()
    first_112 = ' '.join(words[:112]).lower()  # ~45 seconds at 150wpm

    # Anomaly: specific localized detail
    has_anomaly = bool(
        re.search(r'\b\d{3,4}\b', first_30)          # year/number
        or re.search(r'[A-Z][a-z]+ [A-Z][a-z]+', ' '.join(words[:30]))  # named entity
        or re.search(r'(?:map|document|telegram|treaty|decree|clause|line)', first_30)
    )

    # Stakes: systemic consequence language
    stakes_patterns = [
        r'which meant', r'this (?:meant|determined|controlled)',
        r'entire', r'all of', r'million', r'empire',
        r'shut off', r'resource', r'consequence',
    ]
    has_stakes = any(re.search(p, first_112) for p in stakes_patterns)

    # Inciting incident: turn/pivot within ~45 seconds
    pivot_patterns = [
        r'\bbut\b', r'\bexcept\b', r'\buntil\b',
        r'the problem was', r'that\'s when', r'here\'s what',
        r'what actually', r'except ', r'unless ',
    ]
    has_inciting = any(re.search(p, first_112) for p in pivot_patterns)

    return {
        'anomaly': has_anomaly,
        'stakes': has_stakes,
        'inciting_incident': has_inciting,
    }
```

### HOOK-PATTERN-LIBRARY.md Parser
```python
# Source: Usage Notes section of .claude/REFERENCE/HOOK-PATTERN-LIBRARY.md
def _load_pattern_library(library_path: str) -> Dict[str, Any]:
    """Parse HOOK-PATTERN-LIBRARY.md into pattern data dict."""
    from pathlib import Path
    text = Path(library_path).read_text(encoding='utf-8')
    patterns = {}
    # Section delimiter documented in library Usage Notes
    for section in re.split(r'^## Pattern: ', text, flags=re.MULTILINE):
        if not section.strip():
            continue
        name = section.split('\n')[0].strip()
        topic_match = re.search(r'\*\*Topic type:\*\* (.+)', section)
        # Count numbered examples
        example_count = len(re.findall(r'^\d+\.', section, re.MULTILINE))
        if name == 'authority_challenge' or example_count == 0:
            patterns[name] = {'topics': [], 'count': 0, 'examples': []}
            continue
        topics = [t.strip() for t in topic_match.group(1).split(',')] if topic_match else []
        # Extract first sentences from numbered list
        examples = re.findall(r'First sentence: "([^"]+)"', section)
        patterns[name] = {'topics': topics, 'count': example_count, 'examples': examples[:3]}
    return patterns
```

### Topic Auto-Detection for Script Content
```python
# Source: extended from tools/title_scorer.detect_pattern() keyword approach (Phase 67)
TOPIC_KEYWORDS = {
    'territorial': [
        'border', 'territory', 'dispute', 'sovereignty', 'map', 'treaty',
        'island', 'colony', 'colonize', 'independence', 'annexed', 'partition',
        'demarcation', 'claim', 'occupied',
    ],
    'ideological': [
        'myth', 'propaganda', 'ideology', 'narrative', 'belief', 'religion',
        'race', 'nationalist', 'revisionist', 'debunk', 'misconception',
    ],
    'political_fact_check': [
        'politician', 'policy', 'election', 'legislation', 'law', 'ruling',
        'court', 'verdict', 'document', 'archive', 'declassified',
    ],
}

def detect_topic_from_script(text: str) -> str:
    """Auto-detect topic type from script content — extends Phase 67 title detection."""
    lower = text[:2000].lower()  # Sample first ~2000 chars
    scores = {topic: sum(1 for kw in kws if kw in lower)
              for topic, kws in TOPIC_KEYWORDS.items()}
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else 'general'
```

---

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| 4-beat boolean detection (cold_fact/myth/contradiction/payoff) | Document Reveal framework (anomaly/stakes/inciting_incident) | Phase 69 | Aligns scoring with user's actual writing framework; reduces false positives from broad contradiction keyword matching |
| Template-based hook generation (5 fixed templates A-E) | LLM generation from script material using framework as guidance | Phase 69 | Hooks grounded in actual script content, not generic templates |
| No title-to-hook alignment check | Dual fulfillment check (entity echo + promise type) | Phase 69 | Catches the specific "17% dropout from title-fulfillment mismatch" cited in HOOK-01 requirement |
| No topic-type recommendation | Style recommendation banner with confidence-based modifier | Phase 69 | Territorial hooks get cold_fact guidance backed by 6/7 data points |

**Deprecated/outdated:**
- `_detect_beats()` function: replaced by `_detect_framework()`. The 'beats' key in result dict becomes 'framework'.
- `beat_score` result key: renamed to `framework_score` for clarity. Any external code using `result['beat_score']` will break — check usages before removing.

---

## Open Questions

1. **beat_score key rename vs backward compat**
   - What we know: `score_hook()` is called in the `/script --hooks` process (script.md) and in `rank_hooks()`. The CLI format_hook_ranking() references `sum(h['beats'].values())`.
   - What's unclear: Are there other callers outside the tested files?
   - Recommendation: Search codebase for 'beat_score' and 'beats' key references before renaming. If only used in hook_scorer.py itself and its tests, rename freely. If used in script.md command flow, maintain backward compat alias.

2. **intel.db v3 migration**
   - What we know: STATE.md documents "Phase 69 will migrate to v3 (competitor_hooks table)"
   - What's unclear: CONTEXT.md makes no mention of DB persistence for hook variants
   - Recommendation: Do NOT include intel.db migration in Phase 69. Variants output to terminal only. Migration belongs in a future persistence phase (BENCH-05).

3. **LLM variant generation mechanism**
   - What we know: "LLM-generated from script material" is the requirement; "Document Reveal" framework is the generation guidance
   - What's unclear: Whether Claude is invoked via subprocess, MCP, or the generation is described as instructions for the human operator of /script --hooks
   - Recommendation: In the context of Claude Code slash commands, "LLM generation" means Claude reads the script and generates variants directly as part of the /script --hooks command execution. No subprocess needed — Claude IS the executor. The plan should document the generation prompt structure as a system instruction.

---

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | pytest (auto-discovers unittest.TestCase) |
| Config file | pyproject.toml (inferred from existing test runs) |
| Quick run command | `python -m pytest tests/unit/test_hook_scorer.py -x -q` |
| Full suite command | `python -m pytest tests/ -q` |

### Phase Requirements → Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| HOOK-01 | Entity echo detects title entity in first 50 words | unit | `python -m pytest tests/unit/test_hook_scorer.py::TestFulfillmentCheck::test_entity_echo_pass -x` | Wave 0 |
| HOOK-01 | Entity echo fails when title entity absent from hook | unit | `python -m pytest tests/unit/test_hook_scorer.py::TestFulfillmentCheck::test_entity_echo_fail -x` | Wave 0 |
| HOOK-01 | Promise-type mismatch detected and specific fix suggested | unit | `python -m pytest tests/unit/test_hook_scorer.py::TestFulfillmentCheck::test_promise_type_mismatch -x` | Wave 0 |
| HOOK-01 | score_hook() with title=None skips fulfillment dimension | unit | `python -m pytest tests/unit/test_hook_scorer.py::TestScoreHook::test_no_title_skips_fulfillment -x` | Wave 0 |
| HOOK-02 | territorial topic → cold_fact recommendation in output | unit | `python -m pytest tests/unit/test_hook_scorer.py::TestStyleRecommendation::test_territorial_recommends_cold_fact -x` | Wave 0 |
| HOOK-02 | ideological topic → myth_contradiction recommendation | unit | `python -m pytest tests/unit/test_hook_scorer.py::TestStyleRecommendation::test_ideological_recommends_myth_contradiction -x` | Wave 0 |
| HOOK-02 | Low-confidence pattern (< 5 examples) → advisory only, no score change | unit | `python -m pytest tests/unit/test_hook_scorer.py::TestStyleRecommendation::test_low_confidence_no_score_impact -x` | Wave 0 |
| HOOK-01+02 | score_hook() without title still returns valid total_score | unit | `python -m pytest tests/unit/test_hook_scorer.py::TestScoreHook::test_backward_compat_no_title -x` | Wave 0 |

### Sampling Rate
- **Per task commit:** `python -m pytest tests/unit/test_hook_scorer.py -x -q`
- **Per wave merge:** `python -m pytest tests/ -q`
- **Phase gate:** Full suite green before `/gsd:verify-work`

### Wave 0 Gaps
- [ ] `tests/unit/test_hook_scorer.py` — covers all HOOK-01 and HOOK-02 unit requirements above
- [ ] `tests/unit/test_hook_scorer.py` — note: file does NOT currently exist; must be created in Plan 01

*(Existing test infrastructure: pytest, conftest.py, tests/unit/ all present and confirmed working via `23 passed` run.)*

---

## Sources

### Primary (HIGH confidence)
- `tools/research/hook_scorer.py` — full source read; existing function signatures, scoring budget, beat detection logic
- `.claude/REFERENCE/HOOK-PATTERN-LIBRARY.md` — full source read; pattern counts, topic distributions, programmatic parse format
- `channel-data/niche-hook-patterns.md` — full source read; topic distribution data per pattern
- `.planning/phases/69-hook-quality-upgrade/69-CONTEXT.md` — authoritative decisions document
- `tools/production/entities.py` (interface via 68-01-PLAN.md) — EntityExtractor API confirmed
- `tools/production/parser.py` — ScriptParser and strip_for_teleprompter confirmed
- `tools/production/title_generator.py` — TitleMaterialExtractor pattern confirmed reusable
- `tools/title_scorer.py` — detect_pattern() keyword approach confirmed extensible
- `.planning/STATE.md` — architectural constraints (hook scoring runs after generation, intel.db v3 note)

### Secondary (MEDIUM confidence)
- `.claude/commands/script.md` — /script --hooks existing behavior documented; variant generation described as 5 template-based variants (Phase 69 replaces with LLM-based)
- `tests/unit/test_title_generator.py` — established test pattern for this codebase confirmed via file read and live test run (23 passed)

### Tertiary (LOW confidence)
- None — all key findings verified against source files

---

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — all tools read directly from source files; no new dependencies
- Architecture: HIGH — patterns derived from existing Phase 67/68 code, directly extensible
- Pitfalls: HIGH — all identified from reading actual code + STATE.md + CONTEXT.md decisions

**Research date:** 2026-03-18
**Valid until:** 2026-04-18 (stable codebase — no fast-moving external dependencies)
