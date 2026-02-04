# Phase 23: B-Roll Generation - Research

**Researched:** 2026-02-03
**Domain:** Production asset generation, visual asset sourcing, shot list automation
**Confidence:** HIGH

## Summary

Phase 23 builds on Phase 22's entity extraction to generate actionable shot lists with source suggestions. Research reveals this is a **custom domain** with no standard production automation tools—users create manual checklists today. The opportunity is to automate what's currently a 2-4 hour manual process into a <5 minute generation task.

**Key insight:** B-roll generation is pattern-based. Users follow consistent structure (Priority 1 → Priority 2 → Priority 3, Maps → Documents → Portraits → Graphics), use specific source URLs (Wikimedia Commons, Archive.org, MapChart.net), and include DIY creation instructions when downloads aren't available.

**Primary recommendation:** Build a generator that takes extracted entities, classifies visual asset types, suggests source URLs using pattern matching, and outputs markdown checklists matching existing format. Focus on **source URL suggestion quality** over perfect entity-to-visual mapping.

## Standard Stack

### Core Libraries

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| **dataclasses** | stdlib | Data structures for shots | Python native, zero dependencies |
| **typing** | stdlib | Type annotations | Ensures correctness |
| **re** | stdlib | URL pattern matching | Built-in, reliable |
| **pathlib** | stdlib | File path handling | Modern Python standard |

### Supporting Libraries (Optional)

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| **requests** | 2.31+ | API calls (Wikimedia) | If implementing live URL verification |
| **urllib.parse** | stdlib | URL construction | For dynamic URL generation |

### Alternatives Considered

No direct alternatives exist—this is a custom domain. Generic asset management tools (Ralph, VFX pipeline tools) don't address shot list generation from script entities.

**Installation:**
```bash
# Core functionality requires no installation (stdlib only)
# Optional API features:
pip install requests
```

## Architecture Patterns

### Recommended Project Structure

```
tools/production/
├── parser.py              # Existing (Phase 22)
├── entities.py            # Existing (Phase 22)
├── broll.py               # NEW: Shot list generator
└── __init__.py            # Export BRollGenerator
```

### Pattern 1: Entity-to-Visual Type Mapping

**What:** Map extracted entity types to visual asset categories
**When to use:** Converting Phase 22 entities into shot requirements

**Mapping table (from existing files):**

| Entity Type | Visual Category | Priority | Example |
|-------------|----------------|----------|---------|
| `place` (city/landmark) | Historical Photo | High | "Lancaster House" → portrait photo |
| `place` (region/territory) | Map | Critical | "Chagos Archipelago" → custom map |
| `place` (maritime) | Strategic Map | Critical | "Diego Garcia" → base location map |
| `document` | Primary Source Document | Critical | "Höfle Telegram" → scanned document |
| `person` (with title) | Portrait | High | "Harold Wilson" → official photo |
| `date` (year range) | Timeline Graphic | Medium | "1965-2025" → DIY timeline |
| `organization` | Logo/Building | Medium | "UN" → logo or headquarters |

**Example:**
```python
# Source: Existing B-ROLL-DOWNLOAD-LINKS.md pattern analysis
def classify_visual_type(entity: Entity) -> str:
    """Classify entity into visual asset category."""
    if entity.entity_type == 'document':
        # Always primary source documents (CRITICAL priority)
        return 'primary_source_document'

    elif entity.entity_type == 'place':
        # Context-dependent: City → photo, Region → map
        place_lower = entity.normalized
        if any(word in place_lower for word in ['gulf', 'ocean', 'sea', 'strait']):
            return 'strategic_map'
        elif any(word in place_lower for word in ['island', 'archipelago', 'territory']):
            return 'map'
        else:
            return 'historical_photo'

    elif entity.entity_type == 'person':
        return 'portrait'

    elif entity.entity_type == 'date':
        return 'timeline_graphic'

    elif entity.entity_type == 'organization':
        return 'logo_or_building'

    else:
        return 'generic_illustration'
```

### Pattern 2: Source URL Pattern Matching

**What:** Generate source URLs using known patterns for common archives
**When to use:** Suggesting where to download assets

**Known URL patterns (from existing checklists):**

```python
# Wikimedia Commons search URLs
def get_wikimedia_search_url(search_term: str) -> str:
    """Generate Wikimedia Commons search URL."""
    from urllib.parse import quote
    base = "https://commons.wikimedia.org/wiki/Special:Search"
    return f"{base}?search={quote(search_term)}&title=Special:Search"

# Archive.org search URLs
def get_archive_search_url(search_term: str) -> str:
    """Generate Archive.org search URL."""
    from urllib.parse import quote
    return f"https://archive.org/search.php?query={quote(search_term)}"

# MapChart.net (no search, direct link to tool)
def get_mapchart_url() -> str:
    """MapChart.net base URL for custom maps."""
    return "https://www.mapchart.net/world.html"

# Library of Congress
def get_loc_search_url(search_term: str) -> str:
    """Generate Library of Congress search URL."""
    from urllib.parse import quote
    return f"https://www.loc.gov/search/?q={quote(search_term)}&fa=partof:maps"
```

**Archive priority by topic (from asset-sources-database.md):**

| Topic Category | Primary Archive | Secondary Archive | Tertiary |
|----------------|----------------|-------------------|----------|
| Colonial history | UK National Archives | Gallica (French Library) | Archive.org |
| Treaties/legal | Avalon Project (Yale) | UN Treaty Collection | ICJ website |
| Holocaust/WWII | Yad Vashem | USHMM | Nuremberg docs |
| Medieval | British Library | Bibliothèque nationale | Wikimedia Commons |
| US history | Library of Congress | National Archives | Archive.org |

### Pattern 3: Priority Tier Assignment

**What:** Assign Priority 1/2/3 based on entity importance
**When to use:** Organizing shot list by critical path

**Priority rules (derived from existing checklists):**

```python
def assign_priority(entity: Entity, visual_type: str) -> int:
    """
    Assign priority tier (1=Critical, 2=High, 3=Nice-to-have).

    Rules:
    - Documents mentioned 3+ times: Priority 1
    - Places in intro/conclusion: Priority 1
    - People with 5+ mentions: Priority 1
    - Maps for territorial disputes: Priority 1
    - Timeline graphics: Priority 2
    - Portraits (1-2 mentions): Priority 2
    - Generic illustrations: Priority 3
    """
    # Critical: Primary source documents
    if visual_type == 'primary_source_document':
        return 1 if entity.mentions >= 3 else 2

    # Critical: Maps for main topics
    if visual_type in ['map', 'strategic_map']:
        return 1 if entity.mentions >= 5 else 2

    # High: Key people
    if visual_type == 'portrait':
        return 1 if entity.mentions >= 5 else 2

    # Medium: Graphics and timelines
    if visual_type in ['timeline_graphic', 'logo_or_building']:
        return 2

    # Nice-to-have: Everything else
    return 3
```

### Pattern 4: DIY Instructions Generation

**What:** When downloads aren't available, provide creation instructions
**When to use:** Maps, timelines, quote cards (user creates these)

**Template structure (from existing files):**

```python
DIY_INSTRUCTIONS = {
    'map': """**DIY Instructions (MapChart.net):**
1. Go to MapChart.net
2. Select world/regional map template
3. Click countries/regions to highlight
4. Add labels: [specific labels]
5. Color code: [color scheme]
6. Export as PNG (1920x1080)""",

    'timeline_graphic': """**DIY Instructions (Canva/PowerPoint):**
1. Create horizontal timeline (1920x1080)
2. Mark key dates: [dates from entity]
3. Add event labels: [events]
4. Color code by category
5. Export as high-res PNG""",

    'quote_card': """**DIY Instructions (Canva):**
1. Open Canva → Search "Quote"
2. Select dark/professional template
3. Insert quote text: [quote]
4. Add source attribution: [citation]
5. Export as PNG (1920x1080)"""
}
```

### Anti-Patterns to Avoid

- **❌ AI-generated download links:** Don't fabricate specific URLs (e.g., exact Wikimedia file paths) without verification
- **❌ Hardcoded entity mappings:** Don't create giant if/else chains for specific entities—use pattern matching
- **❌ Ignoring existing file format:** Users expect specific markdown structure (Priority sections, checkboxes, URLs)
- **❌ Over-automation:** Don't try to auto-download assets—provide links and instructions, let user curate

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| URL validation | Custom HTTP checker | `requests.head()` with timeout | Handles redirects, SSL, timeouts correctly |
| Markdown formatting | String concatenation | Template literals with `.format()` | Readable, maintainable |
| Entity deduplication | Custom merge logic | Existing `EntityExtractor` normalization | Already handles "the X" → "X" |
| File path handling | String manipulation | `pathlib.Path` | Cross-platform, safe |

**Key insight:** The complexity is in **domain knowledge** (which archive for which topic), not technical implementation.

## Common Pitfalls

### Pitfall 1: Fabricating Specific Asset URLs

**What goes wrong:** Generator creates exact URLs like `https://commons.wikimedia.org/wiki/File:Harold_Wilson_1965.jpg` that don't exist

**Why it happens:** Trying to be too helpful without verification

**How to avoid:**
- Provide **search URLs** (pattern-based, always valid)
- OR provide **exact URLs** only for known-stable resources (e.g., ICJ case pages)
- Include fallback instructions: "Search: [entity name]"

**Warning signs:**
- Unit tests fail when URLs return 404
- Users complain about broken links

### Pitfall 2: Ignoring Topic Context

**What goes wrong:** Suggesting Wikimedia Commons for Holocaust documents instead of Yad Vashem/USHMM

**Why it happens:** Not using topic-aware archive selection

**How to avoid:**
- Detect script topic from entities (if "Holocaust", "Nazi", "concentration camp" → specialized archives)
- Use fallback chain: Specialized archive → General archive → DIY

**Detection:**
```python
def detect_topic_category(entities: List[Entity]) -> str:
    """Infer script topic from entity keywords."""
    keywords = [e.normalized for e in entities]

    if any(w in keywords for w in ['holocaust', 'nazi', 'concentration', 'genocide']):
        return 'holocaust'
    elif any(w in keywords for w in ['treaty', 'icj', 'ruling', 'court']):
        return 'legal'
    elif any(w in keywords for w in ['medieval', 'crusade', 'manuscript']):
        return 'medieval'
    # ... etc
    return 'general'
```

### Pitfall 3: Wrong Priority Assignment

**What goes wrong:** Putting generic illustrations as Priority 1, critical documents as Priority 3

**Why it happens:** Not understanding user workflow (shoot → edit → polish)

**How to avoid:**
- Priority 1 = Can't film without (opening hook visuals, key documents)
- Priority 2 = Needed for editing (portraits, maps)
- Priority 3 = Polish during final edit (transitions, generic B-roll)

**Verification:** Count Priority 1 assets—should be 5-10 items, not 30

### Pitfall 4: Massive Generated Checklists

**What goes wrong:** 100+ item checklists from extracting every single entity mention

**Why it happens:** Not deduplicating or filtering low-importance entities

**How to avoid:**
- Filter entities with <2 mentions (unless primary sources)
- Deduplicate by normalized form (already done by `EntityExtractor`)
- Cap checklist at ~30-40 items total

## Code Examples

### Example 1: Generate Shot from Entity

```python
# Source: Pattern derived from existing B-ROLL-DOWNLOAD-LINKS.md files
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Shot:
    """A B-roll shot with source suggestions."""
    entity: str              # Entity text (e.g., "Harold Wilson")
    visual_type: str         # Category (e.g., "portrait")
    priority: int            # 1=Critical, 2=High, 3=Nice-to-have
    source_urls: List[str]   # Download/search URLs
    diy_instructions: Optional[str] = None
    section_references: List[str] = None  # Which script sections need this

def entity_to_shot(entity: Entity, topic: str = 'general') -> Shot:
    """Convert entity to shot with source suggestions."""
    visual_type = classify_visual_type(entity)
    priority = assign_priority(entity, visual_type)

    # Generate source URLs
    urls = get_source_urls(entity, visual_type, topic)

    # DIY instructions for created assets
    diy = None
    if visual_type in ['map', 'timeline_graphic', 'quote_card']:
        diy = DIY_INSTRUCTIONS.get(visual_type, '').format(entity=entity.text)

    return Shot(
        entity=entity.text,
        visual_type=visual_type,
        priority=priority,
        source_urls=urls,
        diy_instructions=diy
    )
```

### Example 2: Topic-Aware Source URL Selection

```python
# Source: asset-sources-database.md archive hierarchy
ARCHIVE_HIERARCHY = {
    'holocaust': [
        ('Yad Vashem', 'https://www.yadvashem.org/archive/search'),
        ('USHMM', 'https://collections.ushmm.org'),
        ('Wikimedia Commons', get_wikimedia_search_url)
    ],
    'legal': [
        ('ICJ Cases', 'https://www.icj-cij.org/search'),
        ('Avalon Project', 'https://avalon.law.yale.edu/search'),
        ('UN Treaty Collection', 'https://treaties.un.org/Pages/AdvanceSearch.aspx')
    ],
    'medieval': [
        ('British Library', 'https://www.bl.uk/manuscripts/'),
        ('Gallica (BnF)', 'https://gallica.bnf.fr/accueil/en/content/accueil-en'),
        ('Wikimedia Commons', get_wikimedia_search_url)
    ],
    'general': [
        ('Wikimedia Commons', get_wikimedia_search_url),
        ('Archive.org', get_archive_search_url),
        ('Library of Congress', get_loc_search_url)
    ]
}

def get_source_urls(entity: Entity, visual_type: str, topic: str) -> List[str]:
    """Get source URLs based on visual type and topic."""
    archives = ARCHIVE_HIERARCHY.get(topic, ARCHIVE_HIERARCHY['general'])
    urls = []

    for archive_name, url_or_func in archives:
        if callable(url_or_func):
            # Dynamic search URL
            search_term = entity.text
            urls.append(url_or_func(search_term))
        else:
            # Static archive base URL
            urls.append(url_or_func)

    # Special case: Maps → MapChart.net first
    if visual_type in ['map', 'strategic_map']:
        urls.insert(0, get_mapchart_url())

    return urls[:3]  # Top 3 sources
```

### Example 3: Generate Markdown Checklist Section

```python
# Source: Existing B-ROLL-DOWNLOAD-LINKS.md format analysis
def generate_markdown_section(shots: List[Shot], priority: int) -> str:
    """Generate markdown section for a priority tier."""
    priority_labels = {1: 'CRITICAL', 2: 'HIGH VALUE', 3: 'SUPPLEMENTARY'}
    label = priority_labels[priority]

    # Filter shots by priority
    tier_shots = [s for s in shots if s.priority == priority]
    if not tier_shots:
        return ''

    # Group by visual type
    by_type = {}
    for shot in tier_shots:
        by_type.setdefault(shot.visual_type, []).append(shot)

    lines = [f"## PRIORITY {priority}: {label}\n"]

    for visual_type, shots_of_type in sorted(by_type.items()):
        type_label = visual_type.replace('_', ' ').title()
        lines.append(f"\n### {type_label}\n")

        for shot in shots_of_type:
            lines.append(f"**Asset:** {shot.entity}")

            # Source URLs
            for url in shot.source_urls:
                lines.append(f"- **Source:** {url}")

            # DIY instructions
            if shot.diy_instructions:
                lines.append(f"\n{shot.diy_instructions}\n")

            # Checkbox
            lines.append("- [ ] Downloaded/Created\n")

    return '\n'.join(lines)
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Manual checklist creation (2-4 hours) | Phase 23 generator (<5 min) | 2026-02 (this phase) | 95% time reduction |
| Generic "find images" guidance | Topic-specific archive suggestions | 2025-12 (asset-sources-database.md) | Higher quality assets |
| No priority system | Priority 1/2/3 tiers | 2025-12 | Clearer production workflow |
| Hardcoded URLs | Search URL patterns | 2026-02 (this phase) | Maintainable, future-proof |

**Deprecated/outdated:**
- Manual B-roll planning: Time-consuming, inconsistent format
- One-size-fits-all source suggestions: Topic-aware is better

**Current best practice:**
- Generate from entities (Phase 22 output)
- Organize by priority tiers
- Provide search URLs + DIY instructions
- Match existing markdown format

## Open Questions

### Question 1: How to handle entities appearing in multiple sections?

**What we know:** Entities can appear in intro, multiple body sections, conclusion
**What's unclear:** Should shot list show all section references or just count mentions?
**Recommendation:** Show section references for Priority 1 assets (helps editor place B-roll), just count for Priority 2/3

### Question 2: DIY instruction verbosity

**What we know:** Users need creation instructions for maps, timelines, graphics
**What's unclear:** How detailed should instructions be? (5 steps vs. 15 steps?)
**Recommendation:** Start with 5-7 step templates, iterate based on user feedback

### Question 3: Wikimedia Commons API integration

**What we know:** Wikimedia has REST API for file search ([API Portal](https://api.wikimedia.org/wiki/Reusing_free_images_and_media_files_with_Python))
**What's unclear:** Worth the complexity vs. search URLs?
**Recommendation:** Phase 23.1—search URLs (simple, always works). Phase 23.2—optional API integration for live file suggestions

## Sources

### Primary (HIGH confidence)

- **Existing B-roll files analysis:**
  - `video-projects/_IN_PRODUCTION/14-chagos-islands-2025/B-ROLL-DOWNLOAD-LINKS.md`
  - `video-projects/_IN_PRODUCTION/19-flat-earth-medieval-2025/B-ROLL-DOWNLOAD-LINKS.md`
  - `video-projects/_IN_PRODUCTION/4-crusades-fact-check-2025/B-ROLL-CHECKLIST.md`
  - Pattern: Priority tiers, source URLs, DIY instructions, checkboxes

- **Asset sourcing reference:**
  - `.claude/REFERENCE/asset-sources-database.md`
  - Archive hierarchy, topic-specific sources, MapChart.net workflow

- **Phase 22 entity extraction:**
  - `tools/production/entities.py` (Entity dataclass)
  - `tools/production/parser.py` (Section dataclass)

### Secondary (MEDIUM confidence)

- [Wikimedia Commons API documentation](https://api.wikimedia.org/wiki/Reusing_free_images_and_media_files_with_Python) - Official Python examples for image search/download
- [MediaWiki API reference](https://www.mediawiki.org/wiki/API:Images) - Image metadata queries
- [Archive.org search API](https://archive.org/developers/searches.html) - Programmatic search (not verified)

### Tertiary (LOW confidence)

- [GitHub video-metadata topic](https://github.com/topics/video-metadata) - Generic video asset tools (not production-specific)
- [Shotstack Python SDK](https://github.com/shotstack/shotstack-sdk-python) - Cloud video API (different use case)

## Metadata

**Confidence breakdown:**
- Pattern analysis (file structure, URL patterns, priority rules): **HIGH** - Derived from 5+ real production files
- Archive hierarchy: **HIGH** - Documented in asset-sources-database.md
- Topic detection heuristics: **MEDIUM** - Inferred from patterns, needs validation
- DIY instruction templates: **MEDIUM** - Based on existing examples, may need iteration
- API integration value: **LOW** - Search URLs sufficient, API is nice-to-have

**Research date:** 2026-02-03
**Valid until:** 60 days (stable patterns, but new archives may emerge)

---

## Implementation Strategy Recommendation

**Phase 23.1 (MVP - 2-3 hours):**
1. Build `BRollGenerator` class taking `List[Entity]` → `List[Shot]`
2. Implement entity → visual type classification
3. Generate search URLs using pattern matching
4. Output markdown matching existing format
5. Test with 3 existing scripts (verify output matches manual checklists)

**Phase 23.2 (Enhancement - optional):**
1. Add topic detection from entity keywords
2. Implement topic-aware archive selection
3. Add section reference tracking (which sections mention each entity)
4. Refine DIY instruction templates

**Success criteria:**
- Generated checklist matches existing file structure (Priority 1/2/3, sections, checkboxes)
- Source URLs are valid (search patterns, not fabricated file paths)
- Priority 1 assets = 5-10 items (filmable set)
- User can generate checklist in <30 seconds vs. 2-4 hours manual

**Risk mitigation:**
- Start with search URLs (safe), defer API integration
- Use existing entity extraction (no new NLP complexity)
- Match proven format (low adoption friction)
