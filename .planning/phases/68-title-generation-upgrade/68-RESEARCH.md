# Phase 68: Title Generation Upgrade - Research

**Researched:** 2026-03-17
**Domain:** Python — script/SRT parsing, entity extraction, title generation, scoring integration
**Confidence:** HIGH

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

**Script Extraction Strategy**
- Full script scan — scan entire script (not just opening) for title raw material
- All four material types extracted: specific numbers, document/treaty names, named contradictions (myth vs reality pairs), and named entities (people, places)
- Priority ranking: frequency + position weighting (mention count, bonus for appearing in opening/closing)
- Input types: both markdown scripts AND SRT subtitle files
- EntityExtractor from metadata.py already extracts people/places/documents — reuse and extend

**Versus Auto-Detection**
- Trigger: entities + explicit conflict markers — two named entities co-occurring with conflict language ("against", "disputed", "competed", "rivalry", "divided", "vs", etc.)
- Entity types: any named entities in opposition (countries, people, organizations, ideologies), not limited to countries

**Rejection Filters (SC3 REINTERPRETED)**
- NOT blind pattern-matching — SC3 reinterpreted as data-driven scoring, not hiding
- All candidates shown — titles with year/colon/the_x_that/question patterns get heavy score penalties and appear last with warning labels, but ARE shown to user
- Score via title_scorer — existing Phase 67 penalties (-50 for year, -50 for colon, -50 for the_x_that) serve as ranking signal, not as hide signal
- Penalized candidates show warning — e.g., "⚠️ #7 penalized: year in title (-15 CTR impact)"

**Candidate Generation**
- Volume: Claude's discretion based on script richness
- Pattern types actively generated: versus (when detected), declarative (always at least one), how/why, curiosity/paradox, plus any other angle that could get views
- Every candidate auto-scored — run through score_title() with --db and --topic before display
- Output format: ranked list with scores (replaces A/B/C table)
  - Each entry shows: rank, title, score, grade, pattern type
  - Penalized titles show warning explaining the penalty
  - Variable length — show whatever was generated, ranked best to worst

### Claude's Discretion
- Number of candidates to generate (proportional to script material richness)
- Versus weight in ranking (based on signal strength)
- Multi-entity pair selection strategy
- Myth vs reality versus framing (case by case)
- Internal generation algorithm (template-based, LLM-assisted, or hybrid)

### Deferred Ideas (OUT OF SCOPE)
None — discussion stayed within phase scope
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| TITLE-01 | `/publish --titles` reads the script and extracts specific numbers, document names, and contradictions as raw material for title candidates | EntityExtractor (entities.py) already extracts documents/places/people with mention counts; ScriptParser (parser.py) provides full-script section scanning; retitle_gen.py has a working SRT reader and number extractor pattern |
| TITLE-02 | Title generation produces versus and declarative variants as default output when topic has two competing entities | retitle_gen.py has `extract_actors_from_text()` and versus pattern generation; conflict marker detection pattern needs to be built on top of existing entity extraction |
| TITLE-03 | Tool auto-rejects titles with year (-46% CTR), colon (-28%), "The X That Y" (1.2% CTR), and question (-36%) patterns before presenting to user | CONTEXT.md reinterprets SC3 as score-based ranking not hiding; title_scorer.py `score_title()` already implements all four penalties as -50 hard rejects; format_result() renders penalty warnings |
</phase_requirements>

---

## Summary

Phase 68 upgrades `/publish --titles` from a template-based stub into a script-grounded generation engine. The current `MetadataGenerator._generate_title_variants()` in `tools/production/metadata.py` only reads the opening hook of the first section and produces exactly three fixed variants (A=mechanism, B=document, C=paradox) using naive string templates. It has no scoring integration, no SRT support, and no conflict detection.

The upgrade has three interlocking components: (1) a material extractor that scans the full script or SRT for specific numbers, document names, named contradictions, and entity pairs; (2) a candidate generator that converts that material into title candidates using proven patterns (versus, declarative, how/why, curiosity), auto-detecting versus format when conflict language co-occurs with entity pairs; and (3) a scorer that runs every candidate through the existing `score_title()` function and renders a ranked table replacing the A/B/C format.

All three components have strong existing foundations to build on. The entity extraction infrastructure (`EntityExtractor`, `ScriptParser`) is production-ready. The SRT reading pattern exists in `retitle_gen.py::get_opening_text()`. The actor/verb extraction and versus generation logic exists in `retitle_gen.py::thesis_to_titles()`. The scoring and ranking already works via `title_scorer.py`. Phase 68 is primarily integration and extension work, not net-new building.

**Primary recommendation:** Upgrade `_generate_title_variants()` in `metadata.py` by replacing its opening-only scan and fixed-3-variant logic with a new `TitleMaterialExtractor` class (full-script scan, SRT support, all four material types), a `TitleCandidateGenerator` class (pattern-based generation with versus auto-detection), and wiring `score_title()` into the output formatting. The new output format is a ranked table, not A/B/C.

---

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| `tools.production.entities.EntityExtractor` | existing | Extracts people, places, documents with mention counts and positions | Already production-tested; handles SRT-stripped text; returns Entity dataclass with `.mentions`, `.positions`, `.entity_type` |
| `tools.production.parser.ScriptParser` | existing | Parses markdown scripts into sections | Full-script section access; handles frontmatter, B-roll markers, word counts; returns `Section` objects with `.content`, `.start_line`, `.section_type` |
| `tools.title_scorer.score_title()` | Phase 67 | Scores each candidate 0-100 with pattern detection, penalties, bonuses, niche benchmarks | Returns full dict: score, grade, pattern, penalties, hard_rejects, niche_percentile_label |
| `tools.title_scorer.detect_pattern()` | Phase 67 | Classifies title pattern (versus, declarative, how_why, question, colon, the_x_that) | Used to label candidates in output table |
| `re` (stdlib) | stdlib | Regex for number extraction, conflict marker detection, SRT stripping | No dependencies needed |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| `tools.production.parser.strip_for_teleprompter()` | existing | Strips all markdown/B-roll markers before text scan | Preprocessing script text before number/contradiction extraction |
| `tools.title_scorer.has_year()`, `has_specific_number()`, `has_active_verb()` | Phase 67 | Detection helpers | Applying specificity bonus logic during candidate generation |
| `tools.benchmark_store.get_niche_score()` | Phase 67 | Niche benchmark data | Auto-passed to score_title() via db_path when available |
| `pathlib.Path` | stdlib | File path handling | SRT and script file discovery |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Regex-based number extraction | spaCy NER | spaCy adds dependency and startup cost; regex sufficient for cardinal numbers, percentages, dates-as-years |
| Extending `_generate_title_variants()` in place | New standalone module `tools/production/title_generator.py` | Standalone module is cleaner separation of concerns; easier to test; avoids bloating metadata.py further |
| Template-only generation | LLM-assisted candidate expansion | LLM adds latency and API cost; template + script material extraction produces grounded candidates without inference |

**Installation:** No new packages required — all dependencies are existing project modules and stdlib.

---

## Architecture Patterns

### Recommended Project Structure
```
tools/production/
├── title_generator.py   # NEW: TitleMaterialExtractor + TitleCandidateGenerator
├── metadata.py          # MODIFY: replace _generate_title_variants(), add --titles path
├── entities.py          # REUSE: EntityExtractor unchanged
├── parser.py            # REUSE: ScriptParser unchanged
```

### Pattern 1: Material Extraction — Full-Script Scan

**What:** Scan all sections (not just the opening) for four material types, applying frequency + position weighting.
**When to use:** Every time `/publish --titles` is invoked.
**Position weighting logic:** intro sections get a 2x bonus, conclusion sections get a 1.5x bonus; body sections count at face value.

```python
# Derived from EntityExtractor pattern in entities.py
# and retitle_gen.py number extraction pattern

def extract_title_material(sections, srt_text=None):
    """
    Returns dict:
      'numbers': [(value, context_sentence, weight), ...]
      'documents': [(Entity, weight), ...]
      'entities': [(Entity, weight), ...]
      'contradictions': [(myth_phrase, reality_phrase, weight), ...]
    """
    extractor = EntityExtractor()

    # Position weight map
    WEIGHTS = {'intro': 2.0, 'conclusion': 1.5, 'body': 1.0}

    entities_with_weight = []
    for section in sections:
        w = WEIGHTS.get(section.section_type, 1.0)
        section_entities = extractor.extract(section.content, section.start_line)
        for e in section_entities:
            entities_with_weight.append((e, e.mentions * w))

    # Merge entities (same normalized form), accumulate weighted scores
    # ... (deduplication logic matching EntityExtractor.extract_from_sections pattern)

    # Number extraction (non-year integers and percentages)
    numbers = _extract_numbers_with_context(full_text)

    # Contradiction extraction (myth vs reality pairs)
    contradictions = _extract_contradictions(full_text)

    return {'numbers': numbers, 'documents': docs, 'entities': ents,
            'contradictions': contradictions}
```

### Pattern 2: SRT Input Support

**What:** Parse SRT subtitle files as an alternative to markdown scripts.
**When to use:** When retitling published videos that have SRT but no project SCRIPT.md.
**SRT parsing pattern:** Already implemented in `retitle_gen.py::get_opening_text()` — strip sequence numbers, timestamps (`\d{2}:\d{2}:\d{2}`), HTML tags; join remaining lines.

```python
# Source: retitle_gen.py lines 248-267 (proven SRT reader pattern)
def read_srt_as_text(srt_path: Path) -> str:
    raw = srt_path.read_text(encoding='utf-8')
    lines = []
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        if re.match(r'^\d+$', line):          # sequence number
            continue
        if re.match(r'\d{2}:\d{2}:\d{2}', line):  # timestamp
            continue
        line = re.sub(r'<[^>]+>', '', line)   # HTML tags
        lines.append(line)
    return ' '.join(lines)
```

### Pattern 3: Versus Auto-Detection

**What:** Detect when two named entities co-occur with conflict language to trigger versus variant generation.
**When to use:** After entity extraction; if signal is strong (multiple conflict markers near entity pair), versus is the primary recommendation; if weak, it is one option among equals.

```python
# Conflict markers from CONTEXT.md decision
CONFLICT_MARKERS = [
    'against', 'disputed', 'competed', 'rivalry', 'divided', 'vs',
    'versus', 'conflict', 'war', 'battle', 'claim', 'claimed',
    'rejected', 'contested', 'opposed', 'split', 'tension'
]

def detect_versus_signal(entities, full_text) -> tuple[str, str, float]:
    """
    Returns (entity_a, entity_b, signal_strength 0.0-1.0).
    signal_strength > 0.5 = strong (versus is primary recommendation).
    signal_strength <= 0.5 = weak (versus is one option among equals).
    Returns ('', '', 0.0) if no versus signal found.
    """
    # Find place/person/org entity pairs
    # Check co-occurrence within N words with conflict language
    # Score based on: number of co-occurrences, frequency of conflict markers,
    # presence in title/opening (position bonus)
```

### Pattern 4: Candidate Generation + Scoring Pipeline

**What:** Generate candidates from extracted material, score each, render ranked table.
**When to use:** After material extraction + versus detection.

```python
# Output format from CONTEXT.md specifics
def format_title_candidates(candidates: list[dict]) -> str:
    """
    candidates: list of score_title() result dicts with added 'warning' key
    Returns markdown table ranked by score.
    """
    lines = ["## Title Candidates (ranked by score)", ""]
    lines.append("| # | Title | Score | Grade | Pattern |")
    lines.append("|---|-------|-------|-------|---------|")

    for i, c in enumerate(sorted(candidates, key=lambda x: -x['score']), 1):
        lines.append(f"| {i} | {c['title']} | {c['score']} | {c['grade']} | {c['pattern']} |")

    # Warnings for penalized candidates (below the table)
    for i, c in enumerate(sorted(candidates, key=lambda x: -x['score']), 1):
        if c.get('hard_rejects'):
            for reason in c['hard_rejects']:
                lines.append(f"\n⚠️ #{i} penalized: {reason}")

    return '\n'.join(lines)
```

### Pattern 5: Number Extraction (non-year integers)

**What:** Extract specific numbers from script body for title specificity bonus.
**Logic:** Reuse `has_year()` exclusion logic from title_scorer; extract bare integers and percentages with surrounding context sentence.

```python
# Source: title_scorer.py has_specific_number() + retitle_gen.py number extraction
def _extract_numbers_with_context(text: str) -> list[tuple]:
    """Extract (number_str, context_sentence) for non-year integers >= 2."""
    results = []
    # Find integers not preceded/followed by year context
    for match in re.finditer(r'\b(\d[\d,]*)\b', text):
        num_str = match.group(1)
        num = int(num_str.replace(',', ''))
        if 1000 <= num <= 2099:   # skip years
            continue
        if num < 2:               # skip 0 and 1 (too generic)
            continue
        # Extract surrounding sentence
        start = text.rfind('.', 0, match.start()) + 1
        end = text.find('.', match.end())
        context = text[start:end if end != -1 else match.end() + 80].strip()
        results.append((num_str, context))
    return results
```

### Pattern 6: Contradiction Extraction

**What:** Find myth vs reality oppositions in script text for title material.
**Logic:** Look for sentences with negation + assertion patterns ("X didn't... actually", "contrary to...", "despite claims...", "never... in fact").

```python
# Derived from retitle_gen.py extract_thesis() pattern
NEGATION_PATTERNS = [
    r'(?:never|not|didn\'t|wasn\'t|weren\'t|couldn\'t)\b.{5,60}\bbut\b',
    r'contrary to\b.{5,60}',
    r'despite\b.{5,60}',
    r'the myth\b.{5,60}',
    r'what .{3,30} gets wrong\b',
    r'(?:actually|in fact|in reality)\b.{5,60}',
]
```

### Anti-Patterns to Avoid

- **Reading only opening section:** Current `_generate_title_variants()` only reads `sections[0].content` — misses documents and contradictions that appear in body sections.
- **Hard-rejecting penalized titles:** CONTEXT.md explicitly overrides SC3 — show all candidates ranked by score, add warning labels; never silently drop.
- **Generating titles from topic-level knowledge:** Both `retitle.md` and CONTEXT.md are explicit — titles must emerge from the actual script content (specific numbers, document names, entity pairs), not generic topic framing.
- **Conflating SRT reading with full extraction:** SRT files lack section structure (no H2 headings); treat as a flat text blob and apply entity extraction on the full text, not section-by-section.
- **Using the old A/B/C TitleVariant dataclass for output:** Phase 68 replaces this with a ranked table. The `TitleVariant` dataclass can be retired or left unused.

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Entity extraction | Custom NER or regex from scratch | `EntityExtractor` from entities.py | Already handles documents, places, people, dates, organizations with deduplication and mention counting |
| Title pattern detection | Custom pattern classifier | `detect_pattern()` from title_scorer.py | Covers all six patterns including the_x_that edge cases |
| Title scoring | Custom score formula | `score_title()` from title_scorer.py | Phase 67 calibrated with real CTR data, niche benchmarks, topic-type thresholds |
| Script text cleaning | Custom markdown stripper | `strip_for_teleprompter()` from parser.py | Already strips all B-roll markers, frontmatter, markdown formatting |
| SRT parsing | New SRT library | Pattern from retitle_gen.py lines 248-267 | Simple line-by-line regex sufficient; no external library needed |
| Actor/entity-to-title-subject conversion | New mapping | `ACTOR_DISPLAY` dict + `extract_actors_from_text()` from retitle_gen.py | 30+ actor normalizations already built and tested |

**Key insight:** Nearly every component needed already exists in the codebase. Phase 68 is an integration task, not a build task. The risk is re-implementing what's already there rather than importing and extending it.

---

## Common Pitfalls

### Pitfall 1: SRT Position Weighting Has No Section Boundaries

**What goes wrong:** SRT files don't have H2 headings, so `section_type` is always 'body' — the position bonus for 'intro' and 'conclusion' sections never fires.
**Why it happens:** `ScriptParser` infers section types from headings; SRT is flat text.
**How to avoid:** For SRT input, apply a positional heuristic: first 20% of words = "intro weight", last 20% = "conclusion weight", middle = "body weight". Split the raw SRT text by word count, not sections.
**Warning signs:** All extracted entities have the same weight despite one appearing in the opening statement.

### Pitfall 2: Entity False Positives in Title Generation

**What goes wrong:** EntityExtractor extracts script production markers as entities (e.g., "B-ROLL" as an organization, or section headings as place names).
**Why it happens:** Even though `MARKER_PATTERNS` strips most B-roll annotations, some residual text can match entity patterns.
**How to avoid:** Run `strip_for_teleprompter()` on section content before passing to EntityExtractor for title material extraction (already handles all known marker patterns).
**Warning signs:** Candidates appear with "B-Roll" or "VO" in them.

### Pitfall 3: Versus Signal on Incidental Co-occurrence

**What goes wrong:** Two entity names both appear in a diplomatic history script (e.g., "France" and "Germany" each mentioned once in historical context) trigger versus framing inappropriately.
**Why it happens:** Simple co-occurrence matching without requiring actual conflict language proximity.
**How to avoid:** Require conflict language within a window of N words from the entity pair, not just in the same document. Tune signal_strength threshold (CONTEXT.md: weak signal = one option among equals, not primary recommendation).
**Warning signs:** Versus variant is generated for a script that's clearly not a two-sides story.

### Pitfall 4: Year Stripping Breaking Document Names

**What goes wrong:** A document like "Treaty of Utrecht 1713" gets its year stripped, producing just "Treaty of Utrecht" — less specific as title material.
**Why it happens:** Year-stripping regex (`\b(1[0-9]{3}|20[0-2][0-9])\b`) targets any four-digit year.
**How to avoid:** Year-strip only at title generation time (when building candidate strings), not during material extraction. Store original document names with years in the material dict; strip years only when building actual title string candidates.
**Warning signs:** Document entities lose their year suffix in the raw material extraction phase.

### Pitfall 5: Output Format Backward Compatibility

**What goes wrong:** The existing `/publish --titles` command writes to `YOUTUBE-METADATA.md` using the A/B/C table format. Changing the format breaks existing published video files.
**Why it happens:** `generate_metadata_draft()` uses a fixed header "## Title A/B/C Test Variants" and the `TitleVariant` dataclass.
**How to avoid:** Replace the A/B/C section header with "## Title Candidates (ranked by score)" when `--titles` is the caller. For `--metadata` (full metadata), the same ranked table can replace A/B/C. No YOUTUBE-METADATA.md files from prior videos are affected (they're already written; only future runs matter).
**Warning signs:** Users report the publish command broke after the upgrade.

### Pitfall 6: score_title() Called Without db_path and topic_type

**What goes wrong:** Scoring in static mode (no DB, no topic type) uses general thresholds. The Context says "auto-score with --db and --topic".
**Why it happens:** `score_title()` defaults to static mode when called without args.
**How to avoid:** In the new generation pipeline, always attempt to load `keywords.db` path (same pattern as title_scorer CLI: `Path(__file__).parent / 'discovery' / 'keywords.db'`) and auto-detect topic from script content using `classify_topic_type()` from performance.py. Fall back gracefully if DB missing.
**Warning signs:** All scores are low/uniform for scripts that have rich CTR data in the DB.

---

## Code Examples

### Full Material Extraction Call Chain

```python
# Source: entities.py + parser.py integration (established pattern in parser.py __main__)
from tools.production.parser import ScriptParser, strip_for_teleprompter
from tools.production.entities import EntityExtractor

parser = ScriptParser()
extractor = EntityExtractor()

# For markdown scripts
sections = parser.parse_file(script_path)
entities = extractor.extract_from_sections(sections)

# For SRT files — flat text, no sections
srt_text = read_srt_as_text(srt_path)
srt_entities = extractor.extract(srt_text, base_line=1)
```

### Score and Rank Candidates

```python
# Source: title_scorer.py score_title() — Phase 67 interface
from tools.title_scorer import score_title, detect_pattern

db_path = str(Path('tools/discovery/keywords.db')) if Path('tools/discovery/keywords.db').exists() else None

candidates = ["Spain vs Portugal. Who Divided the World.", "How Two Countries Split the Ocean"]
results = []
for title in candidates:
    r = score_title(title, db_path=db_path, topic_type='territorial')
    results.append(r)

results.sort(key=lambda x: -x['score'])
```

### Conflict Marker Co-occurrence Check

```python
# Pattern for versus auto-detection (CONTEXT.md decision)
# Co-occurrence window: within 100 words of each entity mention
CONFLICT_MARKERS = [
    'against', 'disputed', 'competed', 'rivalry', 'divided', 'vs',
    'versus', 'conflict', 'war', 'battle', 'claim', 'claimed',
    'rejected', 'contested', 'opposed', 'split', 'tension'
]

def _co_occurrence_score(entity_a: str, entity_b: str, text: str) -> float:
    """Return 0.0-1.0 signal strength for entity pair conflict co-occurrence."""
    words = text.lower().split()
    hits = 0
    for i, word in enumerate(words):
        window = words[max(0, i-50):i+50]
        window_text = ' '.join(window)
        if entity_a.lower() in window_text and entity_b.lower() in window_text:
            for marker in CONFLICT_MARKERS:
                if marker in window_text:
                    hits += 1
                    break
    return min(1.0, hits / 3.0)  # 3+ hits = full signal
```

---

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Fixed 3-variant A/B/C table | Ranked N-candidate table with scores | Phase 68 | Users see scoring context; no arbitrary A/B/C labels |
| Opening-only scan (first section only) | Full-script scan with position weighting | Phase 68 | Document names and contradictions in body sections are now captured |
| No scoring in generation step | Auto-score via score_title() before display | Phase 68 | All candidates pre-ranked; user sees quality signal |
| Templates with entity slot-filling | Material-grounded generation from actual script numbers/names | Phase 68 | Title candidates reference actual script specifics, not topic-level framing |
| Hard block on penalized patterns | Show with warning label, ranked last | Phase 68 (CONTEXT.md reinterpretation) | User retains final decision; tool signals risk without removing options |

**Deprecated/outdated:**
- `TitleVariant` dataclass (variant='A'/'B'/'C'): replaced by score_title() result dict with ranking index
- `_generate_mechanism_title()`, `_generate_document_title()`, `_generate_paradox_title()`: replaced by `TitleCandidateGenerator` pattern-based methods
- "## Title A/B/C Test Variants" output header: replaced by "## Title Candidates (ranked by score)"
- "**Recommendation:** Test A vs B first. Use C if neither performs." footer line: replaced by score-based ranking with penalty warnings

---

## Open Questions

1. **Where does the new title generation code live?**
   - What we know: CONTEXT.md says "upgrade, not replacement" for `_generate_title_variants()`
   - What's unclear: Whether to add a new `tools/production/title_generator.py` module or extend `metadata.py` in place
   - Recommendation: New `title_generator.py` module with `TitleMaterialExtractor` and `TitleCandidateGenerator` classes; `metadata.py` imports and delegates to it. Keeps metadata.py focused on output formatting; makes title_generator.py independently testable.

2. **How is `/publish --titles` invoked — as a command handler or via MetadataGenerator?**
   - What we know: `publish.md` calls `MetadataGenerator` for `--metadata`; `--titles` is a separate flag
   - What's unclear: Whether `--titles` already has a distinct code path or shares `generate_metadata_draft()`
   - Recommendation: Plan should add a dedicated `generate_title_candidates(sections, entities, db_path, topic_type)` method callable from both `--titles` (standalone) and `--metadata` (embedded in full metadata package).

3. **How many candidates is "enough" for a rich vs. thin script?**
   - What we know: CONTEXT.md says "Claude's discretion based on script richness"; output format example shows 4 candidates
   - Recommendation: Minimum 3 (one per primary pattern: versus/declarative/how_why); maximum ~10. Thin scripts (< 3 extractable material items) = 3-5; rich scripts (5+ numbers, 2+ documents, named conflict) = 7-10.

---

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | pytest (existing, version in pyproject.toml) |
| Config file | `pytest.ini` or `pyproject.toml [tool.pytest]` |
| Quick run command | `python -m pytest tests/unit/test_title_generator.py -x -q` |
| Full suite command | `python -m pytest tests/ -q` |

### Phase Requirements → Test Map

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| TITLE-01 | Extracts specific number from script body | unit | `pytest tests/unit/test_title_generator.py::test_extracts_number_from_body -x` | ❌ Wave 0 |
| TITLE-01 | Extracts document name from script body | unit | `pytest tests/unit/test_title_generator.py::test_extracts_document_name -x` | ❌ Wave 0 |
| TITLE-01 | Extracts named contradiction (myth vs reality) | unit | `pytest tests/unit/test_title_generator.py::test_extracts_contradiction -x` | ❌ Wave 0 |
| TITLE-01 | SRT input produces same material types as markdown input | unit | `pytest tests/unit/test_title_generator.py::test_srt_input_extracts_material -x` | ❌ Wave 0 |
| TITLE-01 | Position weighting boosts intro/conclusion entities | unit | `pytest tests/unit/test_title_generator.py::test_position_weighting -x` | ❌ Wave 0 |
| TITLE-02 | Two named entities + conflict marker triggers versus variant | unit | `pytest tests/unit/test_title_generator.py::test_versus_auto_detection -x` | ❌ Wave 0 |
| TITLE-02 | Declarative variant always generated | unit | `pytest tests/unit/test_title_generator.py::test_declarative_always_generated -x` | ❌ Wave 0 |
| TITLE-02 | Weak versus signal = one option, not primary recommendation | unit | `pytest tests/unit/test_title_generator.py::test_versus_weak_signal_not_primary -x` | ❌ Wave 0 |
| TITLE-03 | Year-containing candidate appears last with warning | unit | `pytest tests/unit/test_title_generator.py::test_year_candidate_ranked_last -x` | ❌ Wave 0 |
| TITLE-03 | Colon candidate appears last with warning | unit | `pytest tests/unit/test_title_generator.py::test_colon_candidate_ranked_last -x` | ❌ Wave 0 |
| TITLE-03 | All candidates appear in output (none silently dropped) | unit | `pytest tests/unit/test_title_generator.py::test_all_candidates_shown -x` | ❌ Wave 0 |
| TITLE-03 | Output format is ranked table (not A/B/C) | unit | `pytest tests/unit/test_title_generator.py::test_output_is_ranked_table -x` | ❌ Wave 0 |

### Sampling Rate
- **Per task commit:** `python -m pytest tests/unit/test_title_generator.py -x -q`
- **Per wave merge:** `python -m pytest tests/ -q`
- **Phase gate:** Full suite green before `/gsd:verify-work`

### Wave 0 Gaps
- [ ] `tests/unit/test_title_generator.py` — covers TITLE-01, TITLE-02, TITLE-03 (all 12 tests above)
- [ ] `tools/production/title_generator.py` — the module under test (must exist before tests pass)

*(Existing test infrastructure: `tests/` directory, `pytest`, `tests/conftest.py` with `tmp_script` fixture — all exist. Only the new module and its test file are gaps.)*

---

## Sources

### Primary (HIGH confidence)
- `tools/production/metadata.py` — current `_generate_title_variants()` implementation, `TitleVariant` dataclass, `CLICKBAIT_PATTERNS`, `_apply_tone_filter()`
- `tools/production/entities.py` — `EntityExtractor`, `Entity` dataclass, `DOCUMENT_KEYWORDS`, `KNOWN_PLACES`, marker stripping
- `tools/production/parser.py` — `ScriptParser`, `Section` dataclass, `strip_for_teleprompter()`, section type inference
- `tools/title_scorer.py` — `score_title()`, `detect_pattern()`, `has_year()`, `has_specific_number()`, `has_active_verb()`, `PATTERN_SCORES`, penalty constants, `format_result()`
- `tools/retitle_gen.py` — `get_opening_text()` (SRT reader pattern), `extract_thesis()`, `thesis_to_titles()`, `extract_actors_from_text()`, `CONFLICT_MARKERS` pattern, `_clean_claim()`
- `.planning/phases/68-title-generation-upgrade/68-CONTEXT.md` — all locked decisions and implementation specifics

### Secondary (MEDIUM confidence)
- `.planning/REQUIREMENTS.md` — TITLE-01/02/03 requirement text (original SC3 wording before CONTEXT.md reinterpretation)
- `.claude/commands/publish.md` — `/publish --titles` invocation path, Gate 1 scoring gate
- `.claude/commands/retitle.md` — SRT-first instruction, scoring threshold rules

### Tertiary (LOW confidence)
- None — all findings verified from source code and project documents.

---

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — all components identified from existing source code, no guessing
- Architecture: HIGH — pattern extends proven existing modules (EntityExtractor, ScriptParser, score_title)
- Pitfalls: HIGH — derived from direct code inspection of edge cases in entities.py, title_scorer.py, retitle_gen.py

**Research date:** 2026-03-17
**Valid until:** 2026-04-17 (stable — no external dependencies; all findings from local source code)
