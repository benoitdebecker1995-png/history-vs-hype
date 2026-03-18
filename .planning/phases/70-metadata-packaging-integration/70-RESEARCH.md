# Phase 70: Metadata & Packaging Integration - Research

**Researched:** 2026-03-18
**Domain:** Python tooling — metadata generation, thumbnail concept generation, coherence checking, CLICKBAIT_PATTERNS consolidation
**Confidence:** HIGH — all findings from direct code inspection of the existing codebase

---

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

**Description Template Enforcement (META-01)**
- First sentence: Keyword-stuffed SEO line — lead with primary search keyword + topic type, optimized for YouTube search results (not rephrased hook)
- Source citations: Auto-extracted from script body — parse actual academic citations (author names, book titles, page numbers) instead of [PLACEHOLDER]
- Timestamps/chapters: From SectionTiming (150 WPM via EditGuideGenerator) — existing _generate_chapters() pattern
- Missing element enforcement: Flag with ⚠️ warnings listing what's missing. Output the description anyway but append warnings. Not a hard block

**Thumbnail Concept Generation (META-02)**
- Specificity level: Script-grounded specifics — extract actual documents, maps, entities from script (reuse TitleMaterialExtractor) and name them in concepts
- Pattern selection: Topic-adaptive — Claude auto-detects topic type from script, picks best 3 patterns for that topic. Not fixed to split-map/document-on-map/geo+evidence for every video
- Validation: Auto-check each concept via thumbnail_checker.py — show ✅/⚠️ per concept
- Always 3 concepts — pattern mix varies by topic type

**Metadata Coherence Check (META-03)**
- Hook element definition: Shared entity/keyword — extract primary entity from title, check it appears in thumbnail concept text AND description first sentence
- Display format: Per-element pass/fail — show each pair (title↔thumb, title↔desc, thumb↔desc) as pass/fail with specific missing entity named
- Trigger: Auto after /publish — runs at end of /publish output after all sections generated
- Title input: Check ALL title candidates — show coherence count (3/3, 2/3, 1/3) as column in ranked table
- Detail level: Summary count in title table, detailed breakdown below for candidates with mismatches only
- Ranking impact: Annotation only — coherence does NOT influence title ranking

**CLICKBAIT_PATTERNS Reconciliation**
- Single source: Move CLICKBAIT_PATTERNS to title_scorer.py as authoritative source. metadata.py imports from title_scorer — delete local CLICKBAIT_PATTERNS list
- Scope: Clickbait filtering applies to titles only — not descriptions, tags, or thumbnail text
- Tone unification: Merge active_verbs (positive signal) and CLICKBAIT_PATTERNS (negative signal) into a single tone scoring system in title_scorer.py. Clickbait = negative score, active verbs = positive score

**Output Structure**
- File output: Everything written to YOUTUBE-METADATA.md — including coherence check results and description warnings
- Section order: Titles → Description → Chapters → Tags → Thumbnail Concepts → 🔗 Coherence Check → VidIQ Research Notes [placeholder]

**/publish Flag Surface**
- Default mode: All-in-one — running /publish with no flags generates full bundle
- Individual flags: --titles, --thumbs, --desc still work for single-section generation
- --topic flag: Yes — overrides auto-detection for thumbnail pattern selection and coherence check

### Claude's Discretion
- Which 3 thumbnail patterns to generate per topic type
- Source citation extraction regex/heuristics
- ALLOWED_ACRONYMS placement (title_scorer.py or shared)
- SEO first-line keyword density and phrasing
- How to detect "primary entity" from title for coherence check

### Deferred Ideas (OUT OF SCOPE)
None — discussion stayed within phase scope
</user_constraints>

---

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| META-01 | `/publish` enforces description template: keyword-rich first sentence + specific document/claim + source citations + timestamps | Found: `_generate_description()` in metadata.py currently produces placeholder citations. Needs: SEO first-line generator, citation regex, ⚠️ warning appender. SectionTiming + `_generate_chapters()` already work. |
| META-02 | Thumbnail concept generator reads script, outputs 3 concepts with specific visual elements | Found: TitleMaterialExtractor already extracts documents/entities/places. thumbnail_checker.py's check_thumbnail() can validate generated text concepts. synthesis_engine.py's `_build_thumbnail_blueprint()` has partial pattern. |
| META-03 | Metadata bundle coherence check verifies title + thumbnail concept + description all reference the same hook element | Found: format_title_candidates() produces the ranked table that needs the Coherence column. EntityExtractor identifies entities. The check runs last in generate_metadata_draft(). |
</phase_requirements>

---

## Summary

Phase 70 is a pure Python tooling upgrade with no new external dependencies. The codebase already has all the raw ingredients: `TitleMaterialExtractor` can supply documents and entities for thumbnail concepts, `thumbnail_checker.check_thumbnail()` can validate generated concept text, `EntityExtractor` can find the primary entity for coherence checking, and `_generate_chapters()` already handles SectionTiming. The work is wiring these pieces together inside `MetadataGenerator` and adding three new capabilities: description template enforcement (META-01), script-grounded thumbnail concept generation (META-02), and cross-bundle coherence checking (META-03).

The CLICKBAIT_PATTERNS reconciliation is a straightforward refactor: move the list from metadata.py to title_scorer.py, add a module-level export, update metadata.py to import from title_scorer. ALLOWED_ACRONYMS moves with it.

The biggest design decision is how to extract the "primary entity" from a title string for coherence matching. The title may not contain the same surface form as the entity extracted from the script, so fuzzy substring matching (lowercase containment) is more reliable than exact equality. This is the coherence check's main fragility point.

**Primary recommendation:** Implement all three META requirements inside `MetadataGenerator` in metadata.py, using `TitleMaterialExtractor` as the shared extraction layer, `thumbnail_checker.check_thumbnail()` as the per-concept validator, and a new `_coherence_check()` method that operates on the already-generated title candidates, thumbnail concepts, and description first line.

---

## Standard Stack

### Core (no new dependencies)

| Module | Location | Purpose | Why Standard |
|--------|----------|---------|--------------|
| `MetadataGenerator` | `tools/production/metadata.py` | Main class to upgrade | Already the /publish backend |
| `TitleMaterialExtractor` | `tools/production/title_generator.py` | Extract docs/entities/numbers from script | Already used for title generation in Phase 68 |
| `EntityExtractor` | `tools/production/entities.py` | Extract people/places/organizations | Used throughout production pipeline |
| `check_thumbnail` | `tools/preflight/thumbnail_checker.py` | Validate generated thumbnail concept text | Already enforces PACKAGING_MANDATE rules |
| `score_title` | `tools/title_scorer.py` | Title scoring (already wired in Phase 68) | Authoritative title scorer |
| `format_title_candidates` | `tools/production/title_generator.py` | Ranked table output (Phase 68 output) | Already produces table; needs Coherence column |
| `SectionTiming`, `format_time` | `tools/production/editguide.py` | Timestamp generation | Already used in `_generate_chapters()` |

### No New Pip Dependencies Required

State.md notes: "One new dependency in v7.0: Pillow>=10.0.0 in [thumbnails] extras in pyproject.toml (Phase 70)" — however, thumbnail concept generation is text-based (concept descriptions, not actual image creation). Pillow is NOT needed for Phase 70's text-based approach. If Pillow was anticipated for image analysis, that is out of scope per CONTEXT.md.

**Installation:** None required. All imports are already available.

---

## Architecture Patterns

### Recommended Project Structure

No new files required. All changes in:
```
tools/
├── title_scorer.py              # +CLICKBAIT_PATTERNS export, +ALLOWED_ACRONYMS, tone unification
├── production/
│   ├── metadata.py              # Major upgrade — all three META requirements
│   └── title_generator.py      # +coherence column in format_title_candidates()
```

### Pattern 1: Description Template Enforcement (META-01)

**What:** `_generate_description()` is rewritten to produce a structured description with (a) SEO first line, (b) auto-extracted citations, (c) auto-generated chapters, and (d) ⚠️ warning block appended if elements are missing.

**SEO First Line Generation:**
- Extract primary keyword from script: highest-weight entity from `TitleMaterialExtractor` (first `entities` entry) combined with topic type label
- Format: `"{primary_keyword} — a primary-source analysis of {topic_description}."`
- Topic type detected via `classify_topic_type()` from `tools/youtube_analytics.performance` (same as title_scorer.py does)

**Citation Extraction:**
The script body contains academic citations in patterns like:
- `"According to [Author] in [Title], page [N]..."`
- `"[Author]'s [Book Title] (page [N])..."`
- `"[Author], [Book Title], p. [N]"`

Regex approach (Claude's discretion per CONTEXT.md):
```python
CITATION_PATTERNS = [
    r'(?:According to|per)\s+([A-Z][a-z]+(?:\s+[A-Z]\.?\s*[A-Za-z]+)?)\s+in\s+(["\*]?[A-Z][^,\n]+?["\*]?),\s*(?:page|p\.?)\s*(\d+)',
    r'([A-Z][a-z]+(?:\s+[A-Z]\.?\s*[A-Za-z]+)?)[\'s]*\s+["\*]([^"\*\n]+)["\*][,\s]+(?:\(?page|p\.?)\s*(\d+)',
]
# Yield: "Author, *Title*, p. N"
```

**Warning Block:**
```python
warnings = []
if not citations_found:
    warnings.append("No source citations found in script")
if not timings:
    warnings.append("No timestamps (no SectionTiming data)")
if not seo_keywords_detected:
    warnings.append("SEO first line keyword unclear — verify primary keyword")

if warnings:
    desc += "\n\n⚠️ MISSING ELEMENTS:\n" + "\n".join(f"• {w}" for w in warnings)
```

**When to use:** Every time `_generate_description()` is called. Warnings are always appended when elements are missing; description is always output.

### Pattern 2: Thumbnail Concept Generation (META-02)

**What:** New `_generate_thumbnail_concepts()` method in `MetadataGenerator`. Takes `sections`, `entities`, and optional `topic_type`. Returns a formatted string of 3 thumbnail concept descriptions with ✅/⚠️ validation results.

**Topic-Adaptive Pattern Selection:**

The 3 thumbnail patterns per topic type (Claude's discretion):

| Topic Type | Concept A | Concept B | Concept C |
|------------|-----------|-----------|-----------|
| territorial | split-map-conflict | document-on-map | geo-plus-evidence |
| ideological | myth-vs-reality | document-reveal | timeline-contrast |
| political_fact_check | document-on-map | quote-vs-reality | map-timeline |
| general | split-map-conflict | document-on-map | geo-plus-evidence |

**Script-Grounded Specifics:**
Use `TitleMaterialExtractor.extract_from_sections(sections)` to get:
- `material['documents']` — specific document names (e.g., "Treaty of Tordesillas")
- `material['entities']` — place names, people (e.g., "Atlantic Ocean", "Spain", "Portugal")
- `material['numbers']` — specific numbers (e.g., "370 leagues")

Build concept text by slotting extracted values into pattern templates:
```python
# split-map-conflict template
# Generic: "Map of [region] split by [boundary], [color_A] vs [color_B], no text overlay"
# Script-grounded: "Map of Atlantic Ocean split at 370 leagues west of Cape Verde, Spain (gold/warm) vs Portugal (blue/cool), no text overlay"
```

**Validation via thumbnail_checker.check_thumbnail():**
```python
from tools.preflight.thumbnail_checker import check_thumbnail
result = check_thumbnail(concept_text)
badge = "✅" if result['verdict'] == 'PASS' else "⚠️"
# Display: "**Concept A** {badge} ({result['score']}/100)"
```

**Output format:**
```markdown
## Thumbnail Concepts

**Concept A** ✅ (85/100) — Split-Map Conflict
Map of Atlantic Ocean split at 370 leagues west of Cape Verde. Spain (warm gold) left half, Portugal (cool blue) right half. Red dividing line. No text overlay.

**Concept B** ✅ (90/100) — Document on Map
Treaty of Tordesillas manuscript overlaid on faded Atlantic map. Line of demarcation drawn in red ink visible on document. No face, no text overlay.

**Concept C** ⚠️ (65/100) — Geo + Evidence
Spain and Portugal flags as geographic overlays on 1494 world map. Document fragment bottom-right corner.
Issues: NO COLOR CONTRAST detected
```

### Pattern 3: Metadata Coherence Check (META-03)

**What:** New `_coherence_check()` method in `MetadataGenerator`. Runs after all sections are generated. Checks each title candidate's primary entity against thumbnail concept text and description first sentence.

**Primary Entity Extraction from Title:**
The title string itself is the input. Strategy:
1. Use `EntityExtractor` on the title text — but titles are short so this is unreliable
2. Better: use `TitleMaterialExtractor` material already computed — the top entity by weight IS the primary entity
3. Fallback: take the longest capitalized noun phrase in the title

**Cross-section matching (lowercase containment):**
```python
def _entity_in_text(entity: str, text: str) -> bool:
    return entity.lower() in text.lower()

# Per title candidate:
in_desc = _entity_in_text(primary_entity, desc_first_line)
in_thumb = any(_entity_in_text(primary_entity, concept) for concept in concepts)
coherence_count = sum([True, in_desc, in_thumb])  # title always counts as 1
```

**Coherence column in title table (update format_title_candidates):**
```python
# New signature:
def format_title_candidates(candidates, thumbnail_concepts=None, desc_first_line=None) -> str:
# When thumbnail_concepts and desc_first_line provided, adds Coherence column
# | # | Title | Score | Grade | Pattern | Coherence |
# | 1 | Spain vs Portugal... | 78 | B+ | versus | 3/3 ✅ |
```

**Detail section below the table (only for mismatches):**
```markdown
## 🔗 Coherence Detail

### #2: How Two Countries...
✅ Title ↔ Description: "countries" found in description first line
❌ Title ↔ Thumbnail: "countries" not found in any thumbnail concept
✅ Thumbnail ↔ Description
```

### Pattern 4: CLICKBAIT_PATTERNS Consolidation

**What:** Move `CLICKBAIT_PATTERNS` and `ALLOWED_ACRONYMS` from metadata.py to title_scorer.py. Add module-level exports. Update metadata.py to import from title_scorer. Merge active_verbs list (positive signal) with CLICKBAIT_PATTERNS (negative signal) into unified `_TONE_SIGNALS` dict.

**title_scorer.py additions:**
```python
# Moved from metadata.py — now authoritative source
CLICKBAIT_PATTERNS = [
    'SHOCKING', "You won't believe", ...
]

ALLOWED_ACRONYMS = [
    'ICJ', 'UN', 'CIA', ...
]

# Unified tone scoring (new):
_TONE_SIGNALS = {
    'positive': [  # was: active_verbs list in has_active_verb()
        'destroyed', 'erased', 'redrew', ...
    ],
    'negative': CLICKBAIT_PATTERNS,
}

def compute_tone_score(title: str) -> int:
    """Returns +5 for active verb, -10 per clickbait pattern found."""
    score = 0
    t = title.lower()
    if any(v in t for v in _TONE_SIGNALS['positive']):
        score += ACTIVE_VERB_BONUS  # +5 already defined
    for pattern in _TONE_SIGNALS['negative']:
        if pattern.lower() in t:
            score -= 10
    return score
```

**metadata.py import update:**
```python
from tools.title_scorer import CLICKBAIT_PATTERNS, ALLOWED_ACRONYMS
# Delete local CLICKBAIT_PATTERNS and ALLOWED_ACRONYMS definitions
```

### Pattern 5: generate_metadata_draft() — New Output Order

Current order: Titles → Description → Chapters → Tags → Thumbnail Concepts (placeholder) → VidIQ

New order (per CONTEXT.md decisions):
```python
def generate_metadata_draft(self, sections, entities, timings, topic_type=None) -> str:
    # 1. Generate all components
    material = TitleMaterialExtractor().extract_from_sections(sections)
    title_candidates = self._generate_title_variants(sections, entities, topic_type)
    description = self._generate_description(sections, entities, timings, material)
    chapters = self._generate_chapters(timings)
    tags = self._generate_tags(entities, sections)
    thumbnail_concepts = self._generate_thumbnail_concepts(material, entities, topic_type)
    coherence_section = self._coherence_check(title_candidates, thumbnail_concepts, description)

    # 2. Re-format title table with coherence column
    title_section = format_title_candidates(
        title_candidates,
        thumbnail_concepts=thumbnail_concepts,
        desc_first_line=description.splitlines()[0],
    )

    # 3. Assemble in new order
    # Titles → Description → Chapters → Tags → Thumbnail Concepts → 🔗 Coherence Check → VidIQ Notes
```

### Pattern 6: --topic Flag in /publish Command

The `/publish` command must pass `topic_type` through to `MetadataGenerator`. Pattern from Phase 67/69:

```python
# /publish command reads --topic flag
# Passes to MetadataGenerator:
generator = MetadataGenerator(project_name=project, db_path=db_path)
metadata = generator.generate_metadata_draft(
    sections=sections,
    entities=entities,
    timings=timings,
    topic_type=args.topic,  # None = auto-detect
)
```

`generate_metadata_draft()` signature must add `topic_type: Optional[str] = None`.

### Anti-Patterns to Avoid

- **Blocking on missing elements:** Description is output even if citations missing — warnings appended, not exceptions raised. Never hard-block the pipeline.
- **Exact string matching for coherence:** Primary entity "Spain" appears in title as "Spain", in description as "Spanish", in thumbnail as "Spain". Use `entity.lower() in text.lower()` substring, not equality.
- **Pillow/image generation:** Thumbnail concepts are text descriptions for Photoshop, not actual image files. No image library needed.
- **Recomputing TitleMaterial twice:** Call `TitleMaterialExtractor.extract_from_sections()` once at the top of `generate_metadata_draft()` and pass the result to `_generate_thumbnail_concepts()` and `_generate_description()`. Do not call it inside each helper method.
- **Adding coherence score to title ranking:** CONTEXT.md is explicit — coherence is annotation only, does not change sort order.

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Thumbnail concept validation | Custom rule checker | `thumbnail_checker.check_thumbnail()` | Already implements all PACKAGING_MANDATE rules with MAP_SIGNALS, FACE_SIGNALS, TEXT_OVERLAY_SIGNALS |
| Entity extraction from script | New NER system | `TitleMaterialExtractor.extract_from_sections()` + `EntityExtractor` | Already handles position weighting, document patterns, Treaty-of-X patterns |
| Title pattern detection | New regex | `detect_pattern()` in title_scorer.py | Already handles versus/colon/how_why/etc. with tested logic |
| Topic type detection | New classifier | `classify_topic_type()` from `tools.youtube_analytics.performance` | Used in title_scorer.py already; same function for consistency |

---

## Common Pitfalls

### Pitfall 1: format_title_candidates() Signature Change Breaks Phase 68 Callers

**What goes wrong:** `format_title_candidates()` is called in `metadata.py` with `format_title_candidates(title_candidates)`. Adding coherence parameters must not break the existing single-argument call path.

**Why it happens:** Phase 68 locked the interface for this function.

**How to avoid:** Make the new parameters optional with `None` defaults:
```python
def format_title_candidates(
    candidates: List[Dict],
    thumbnail_concepts: Optional[List[str]] = None,
    desc_first_line: Optional[str] = None,
) -> str:
    # When thumbnail_concepts and desc_first_line are None, output without Coherence column
    # Exact same output as Phase 68 when called with 1 argument
```

**Warning signs:** Tests for Phase 68 pass with old call signature; add new tests for the enriched call path.

### Pitfall 2: Citation Regex Misses Real Citations, Falsely Warns

**What goes wrong:** The ⚠️ warning fires "No source citations found" on a script that has many citations, because the regex doesn't match the exact citation format used in the script.

**Why it happens:** Citation formats vary — "According to X in Y, page N", "X (Y, p. N)", "X's Y shows...", "[QUOTE ON SCREEN: X]".

**How to avoid:** Test the citation regex against real scripts from the project. Look at actual SCRIPT.md files in `video-projects/_IN_PRODUCTION/` to catalog the citation patterns used. The regex should be permissive — false positives (detecting non-citations) are less harmful than false negatives (missing real citations and showing spurious warnings).

Also: use a secondary signal — if DOCUMENT entities are found in the script AND "page" or "p." appears near them, citations are likely present.

### Pitfall 3: Thumbnail Concept Text Fails thumbnail_checker Because It Mentions "No Face"

**What goes wrong:** A generated concept description like "Map of Atlantic, no face, no text overlay" triggers `_has_signal()` for FACE_SIGNALS because "face" is in the text.

**Why it happens:** `thumbnail_checker.py` already handles this via `exclude_negated=True` in `_has_signal()` for FACE_SIGNALS and TEXT_OVERLAY_SIGNALS. The negation check looks for "no" prefix within 10 characters.

**How to avoid:** Phrase generated concepts consistently: "No text overlay, no face" (with "no" immediately before the signal word). The thumbnail_checker already handles this pattern correctly. Always end concepts with "No text overlay." to get the PASS on that rule.

### Pitfall 4: Coherence Primary Entity Extracts Wrong Word from Title

**What goes wrong:** For title "Spain vs Portugal: How Two Countries Divided the World", the primary entity extracted might be "World" (last capitalized noun) instead of "Spain" or "Portugal".

**Why it happens:** Simple heuristics on title strings are fragile.

**How to avoid:** Primary entity comes from `TitleMaterialExtractor` material, not from the title string directly. The top `entities` entry by weight is the primary entity from the full script — this is the entity that SHOULD appear in title, thumbnail, and description. Use this script-derived entity for coherence checking, not a title-parsed entity.

The coherence check then asks: "Does the title contain the script's primary entity?" rather than "Does the script contain a title-parsed entity?" This is more stable.

### Pitfall 5: generate_metadata_draft() Signature Change Requires Command Update

**What goes wrong:** Adding `topic_type=None` to `generate_metadata_draft()` works when called from code, but the `/publish` command documentation in `.claude/commands/publish.md` doesn't reflect the new `--topic` flag, so Claude never passes it.

**Why it happens:** The command definition is separate from the Python implementation.

**How to avoid:** The plan for Phase 70 must include updating `.claude/commands/publish.md` to document the `--topic` flag and show how to pass it to `MetadataGenerator`. This is a documentation change, not code-only.

---

## Code Examples

### Coherence Check — Full Method Skeleton

```python
# In MetadataGenerator, tools/production/metadata.py
def _coherence_check(
    self,
    candidates: List[dict],
    thumbnail_concepts_text: str,
    description: str,
) -> str:
    """
    Check title↔thumb↔desc coherence for each title candidate.
    Returns formatted markdown section.
    """
    if not candidates:
        return ""

    # Primary entity = top-weight entity from script material
    # (computed once in generate_metadata_draft and passed in, or re-extracted here)
    # For simplicity, re-extract from first candidate's title using material already cached
    primary_entity = self._primary_entity  # set on self during generate_metadata_draft

    desc_first_line = description.splitlines()[0] if description else ""

    # Parse thumbnail concepts into list of concept strings
    concepts = re.findall(
        r'\*\*Concept [A-C]\*\*.*?\n(.*?)(?=\*\*Concept|\Z)',
        thumbnail_concepts_text,
        re.DOTALL
    )

    detail_lines = []

    for i, candidate in enumerate(candidates, start=1):
        title = candidate.get("title", "")
        # Use script primary entity, not title-parsed entity
        entity = primary_entity or title  # fallback to full title

        in_title = entity.lower() in title.lower()  # always True when entity from script
        in_desc = entity.lower() in desc_first_line.lower()
        in_thumb = any(entity.lower() in c.lower() for c in concepts)

        count = sum([in_title, in_desc, in_thumb])
        badge = "✅" if count == 3 else ("⚠️" if count == 2 else "❌")

        # Store coherence result back into candidate dict for column display
        candidate["coherence"] = f"{count}/3 {badge}"

        # Only add detail section for mismatches
        if count < 3:
            detail_lines.append(f"\n### #{i}: {title}")
            detail_lines.append(f"{'✅' if in_title else '❌'} Title contains primary entity")
            detail_lines.append(f"{'✅' if in_desc else '❌'} Title ↔ Description: '{entity}' {'found' if in_desc else 'NOT found'} in description first line")
            detail_lines.append(f"{'✅' if in_thumb else '❌'} Title ↔ Thumbnail: '{entity}' {'found' if in_thumb else 'NOT found'} in any thumbnail concept")

    lines = ["", "---", "", "## 🔗 Coherence Check"]
    if detail_lines:
        lines.append("\n### Mismatches (full detail)")
        lines.extend(detail_lines)
    else:
        lines.append("\n✅ All title candidates share primary entity with thumbnail and description.")

    return "\n".join(lines)
```

### Citation Extraction Regex

```python
# In MetadataGenerator._generate_description()
CITATION_PATTERNS = [
    # "According to Chris Wickham in The Inheritance of Rome, page 147"
    re.compile(
        r'(?:According to|per)\s+'
        r'([A-Z][a-z]+(?:\s+[A-Z]\.?\s*[A-Za-z]+)*)\s+'
        r'in\s+[*"]?([A-Z][^,\n"*]+?)[*"]?,\s*'
        r'(?:pages?|pp?\.)\s*(\d+)',
        re.IGNORECASE
    ),
    # "Harris's Ancient Literacy, p. 23"
    re.compile(
        r'([A-Z][a-z]+(?:\'s)?)\s+'
        r'[*"]([A-Z][^"*\n]{3,60})[*"],\s*'
        r'(?:pages?|pp?\.)\s*(\d+)',
        re.IGNORECASE
    ),
]

def _extract_citations(self, sections: List[Section]) -> List[str]:
    full_text = " ".join(s.content for s in sections)
    citations = []
    seen = set()
    for pattern in CITATION_PATTERNS:
        for m in pattern.finditer(full_text):
            author = m.group(1).strip()
            book = m.group(2).strip()
            page = m.group(3).strip()
            citation = f"{author}, *{book}*, p. {page}"
            if citation.lower() not in seen:
                seen.add(citation.lower())
                citations.append(citation)
    return citations
```

### Thumbnail Concept Generation — Topic-Adaptive Templates

```python
# In MetadataGenerator._generate_thumbnail_concepts()
THUMBNAIL_PATTERNS = {
    'territorial': ['split_map_conflict', 'document_on_map', 'geo_plus_evidence'],
    'ideological': ['myth_vs_reality', 'document_reveal', 'timeline_contrast'],
    'political_fact_check': ['document_on_map', 'quote_vs_reality', 'map_timeline'],
    'general': ['split_map_conflict', 'document_on_map', 'geo_plus_evidence'],
}

def _fill_template(self, pattern: str, material: dict, entities: List[Entity]) -> str:
    """Fill a thumbnail pattern template with script-specific elements."""
    # Extract primary place, document, and number
    primary_place = next(
        (e.text for e, _ in material.get('entities', [])
         if hasattr(e, 'entity_type') and e.entity_type == 'place'),
        "the disputed region"
    )
    primary_doc = next(
        (e.text for e, _ in material.get('documents', [])),
        None
    )
    primary_number = next(
        (n for n, _ in material.get('numbers', [])),
        None
    )

    if pattern == 'split_map_conflict':
        base = f"Map of {primary_place} split down the middle. "
        if primary_number:
            base += f"Dividing line at {primary_number}. "
        base += "Warm (gold/red) vs cool (blue) color halves. No face, no text overlay."
        return base
    elif pattern == 'document_on_map':
        doc_str = primary_doc or "primary source document"
        return (
            f"{doc_str} overlaid on faded map of {primary_place}. "
            "Document edges visible, handwritten text legible. "
            "No face, no text overlay."
        )
    # ... other patterns
```

### CLICKBAIT_PATTERNS Move — title_scorer.py

```python
# Add to title_scorer.py (moved from metadata.py)

# Clickbait patterns (authoritative source — metadata.py imports from here)
CLICKBAIT_PATTERNS = [
    'SHOCKING', "You won't believe", "You won't BELIEVE",
    'This will BLOW your mind', "What THEY don't want you to know",
    'INSANE', 'MIND-BLOWING', 'EXPOSED', 'The TRUTH About',
    'DESTROYED by Facts', 'What IT Really Means', 'How THIS Changed',
    'Top 10', '5 Reasons Why', '3 Things You Didn\'t Know',
    'LIED About', 'The Truth They HID'
]

# Allowed acronyms (not clickbait even though all-caps)
ALLOWED_ACRONYMS = [
    'ICJ', 'UN', 'CIA', 'AU', 'EU', 'NATO', 'UNESCO', 'WHO',
    'IMF', 'USSR', 'UK', 'US', 'USA', 'WTO', 'ICC', 'ECHR',
    'OPEC', 'BRICS', 'ASEAN', 'OAS', 'FCDO', 'BIOT', 'PDF',
    'DIY', 'GPS', 'GDP', 'CEO', 'FBI', 'NSA', 'NASA'
]

# Updated metadata.py imports:
# from tools.title_scorer import CLICKBAIT_PATTERNS, ALLOWED_ACRONYMS
# (delete local definitions)
```

---

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Manual thumbnail concept section ("PLACEHOLDER: To be added manually") | Script-grounded, auto-generated 3-concept section with ✅/⚠️ per concept | Phase 70 | User immediately knows which concepts comply with PACKAGING_MANDATE |
| Source citations placeholder string | Auto-extracted from script body with ⚠️ warning if none found | Phase 70 | Eliminates forgotten-citations publishing failures |
| CLICKBAIT_PATTERNS defined in two places | Single source in title_scorer.py, metadata.py imports | Phase 70 | Prevents drift between the two lists |
| Title table without coherence signal | Title table with Coherence column (3/3, 2/3, 1/3) | Phase 70 | User can see at a glance which titles are fully aligned with packaging |

**Deprecated/outdated:**
- `[PLACEHOLDER: To be added manually based on video content]` in thumbnail section — replaced by generated concepts
- `[PLACEHOLDER: Add academic sources from script]` in description — replaced by extracted citations or ⚠️ warning
- Local `CLICKBAIT_PATTERNS` in metadata.py — replaced by import from title_scorer.py

---

## Open Questions

1. **SEO first-line topic label phrasing**
   - What we know: First line should be "keyword-rich" and "optimized for YouTube search results"
   - What's unclear: What exact phrasing for the topic type label? "a primary-source analysis"? "a document-based history of"? "a fact-check of"?
   - Recommendation: Default to "{primary_entity} — {topic_verb} {topic_label}" where topic_verb is "fact-check of" for political_fact_check, "territorial history of" for territorial, "myth-busting" for ideological. Claude's discretion per CONTEXT.md.

2. **Coherence entity when title has no clear primary entity**
   - What we know: Primary entity comes from TitleMaterialExtractor's top-weight entity
   - What's unclear: What if top entity is a year or a generic word?
   - Recommendation: Filter out `entity_type == 'date'` and entities shorter than 4 chars. If still None, skip coherence check and show "⚠️ No primary entity detected for coherence check."

3. **thumbnail_checker.check_thumbnail() with generated text vs. user-written text**
   - What we know: The checker was designed for user-written YOUTUBE-METADATA.md sections, not machine-generated concept strings
   - What's unclear: Will the MAP_SIGNALS list reliably fire on generated concepts that describe geographic elements in unfamiliar ways?
   - Recommendation: After generating each concept, add a MAP_SIGNALS keyword explicitly at the end if geographic content is present (e.g., always include "map" or "geographic" in the concept string). The generator controls the output text so it can guarantee signal words are present.

---

## Validation Architecture

`workflow.nyquist_validation` is absent from `.planning/config.json` — treat as enabled.

### Test Framework

| Property | Value |
|----------|-------|
| Framework | pytest (used throughout the codebase) |
| Config file | None detected — tests run via `python -m pytest tests/` |
| Quick run command | `python -m pytest tests/test_metadata.py tests/test_title_generator.py -x -q` |
| Full suite command | `python -m pytest tests/ -q` |

### Phase Requirements → Test Map

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| META-01 | Description first line contains primary keyword, not rephrased hook | unit | `pytest tests/test_metadata.py::test_description_seo_first_line -x` | ❌ Wave 0 |
| META-01 | Citation regex extracts author/title/page from script text | unit | `pytest tests/test_metadata.py::test_citation_extraction -x` | ❌ Wave 0 |
| META-01 | Missing citations appends ⚠️ warning; output still produced | unit | `pytest tests/test_metadata.py::test_description_warns_missing_citations -x` | ❌ Wave 0 |
| META-02 | 3 thumbnail concepts generated for territorial topic | unit | `pytest tests/test_metadata.py::test_thumbnail_three_concepts_territorial -x` | ❌ Wave 0 |
| META-02 | Concept text contains script-extracted entity names, not generic placeholders | unit | `pytest tests/test_metadata.py::test_thumbnail_concepts_are_grounded -x` | ❌ Wave 0 |
| META-02 | Each concept has ✅ or ⚠️ from thumbnail_checker | unit | `pytest tests/test_metadata.py::test_thumbnail_concepts_validated -x` | ❌ Wave 0 |
| META-03 | Coherence column appears in title table | unit | `pytest tests/test_title_generator.py::test_format_title_candidates_coherence_column -x` | ❌ Wave 0 |
| META-03 | Title with matching entity shows 3/3; title with mismatch shows 2/3 | unit | `pytest tests/test_metadata.py::test_coherence_check_counts -x` | ❌ Wave 0 |
| META-03 | Detail section only shown for mismatching candidates | unit | `pytest tests/test_metadata.py::test_coherence_detail_only_mismatches -x` | ❌ Wave 0 |
| CLICKBAIT | metadata.py imports CLICKBAIT_PATTERNS from title_scorer | unit | `pytest tests/test_metadata.py::test_clickbait_import_from_title_scorer -x` | ❌ Wave 0 |

### Sampling Rate

- **Per task commit:** `python -m pytest tests/test_metadata.py tests/test_title_generator.py -x -q`
- **Per wave merge:** `python -m pytest tests/ -q`
- **Phase gate:** Full suite green before `/gsd:verify-work`

### Wave 0 Gaps

- [ ] `tests/test_metadata.py` — covers META-01, META-02, META-03, CLICKBAIT migration (7 new test functions)
- [ ] `tests/test_title_generator.py` — add `test_format_title_candidates_coherence_column` (1 new test function, existing file likely exists)

Check if `tests/test_metadata.py` exists:
```bash
ls tests/test_metadata.py 2>/dev/null || echo "MISSING"
```

---

## Sources

### Primary (HIGH confidence)

- Direct code inspection — `tools/production/metadata.py` (full file, 574 lines) — existing `_generate_description()`, `_generate_chapters()`, `CLICKBAIT_PATTERNS`
- Direct code inspection — `tools/title_scorer.py` (full file, 633 lines) — `PATTERN_SCORES`, `has_active_verb()`, `ALLOWED_ACRONYMS` absent (currently only in metadata.py)
- Direct code inspection — `tools/production/title_generator.py` (full file, 806 lines) — `TitleMaterialExtractor`, `format_title_candidates()`
- Direct code inspection — `tools/preflight/thumbnail_checker.py` (full file, 333 lines) — `check_thumbnail()`, `MAP_SIGNALS`, `FACE_SIGNALS`, `_has_signal(exclude_negated=True)`
- Direct code inspection — `tools/production/entities.py` (full file, 470 lines) — `EntityExtractor`, `Entity` dataclass
- `.planning/phases/70-metadata-packaging-integration/70-CONTEXT.md` — locked decisions and output structure
- `.planning/phases/68-title-generation-upgrade/68-02-PLAN.md` — `format_title_candidates()` interface
- `.planning/STATE.md` — Pillow dependency note, Phase 68/69 decision history

### Secondary (MEDIUM confidence)

- `.claude/commands/publish.md` — current `/publish` command structure and flag list (for understanding what the command documentation update must include)

---

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — all modules inspected directly, no external dependencies needed
- Architecture: HIGH — all patterns derived from existing code; new methods follow identical patterns to Phase 68 additions
- Pitfalls: HIGH — all pitfalls derived from actual code inspection of the modules being changed, not theoretical

**Research date:** 2026-03-18
**Valid until:** Stable — no fast-moving external dependencies. Valid until the Python modules in tools/production/ are significantly restructured.
