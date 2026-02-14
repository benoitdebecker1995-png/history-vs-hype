# Phase 37: Creator Transcript Analysis - Research

**Researched:** 2026-02-14
**Domain:** Transcript analysis, pattern extraction, NLP for script structure, database design
**Confidence:** HIGH

## Summary

Phase 37 builds a creator technique library by analyzing 80+ existing transcripts in the `transcripts/` folder, extracting structural patterns (hooks, transitions, pacing, evidence presentation), synthesizing universal best practices across multiple successful creators, and surfacing these techniques during script generation.

The phase has three core technical domains: (1) **transcript parsing and pattern extraction** using regex and NLP to identify structural elements, (2) **cross-creator pattern synthesis** to identify universal best practices appearing in 3+ creators, and (3) **database storage and retrieval** to surface techniques during script generation via new STYLE-GUIDE.md Part 8.

**Primary recommendation:** Use Python's `re` module for structural pattern extraction (hooks, transitions, evidence markers), avoid heavyweight NLP frameworks (spaCy would require Python 3.11-3.13, adds unnecessary complexity), store extracted techniques in new `creator_techniques` table (schema v28), and generate STYLE-GUIDE.md Part 8 from cross-creator synthesis similar to how Part 9 is auto-generated from retention data.

## Standard Stack

### Core Libraries

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Python `re` | stdlib | Pattern extraction (hooks, transitions, evidence markers) | Built-in, zero dependencies, sufficient for structural patterns |
| Python `pathlib` | stdlib | Transcript file discovery and traversal | Standard modern Python file handling |
| Python `json` | stdlib | Serialize extracted patterns to database TEXT columns | Universal format for nested data in SQLite |
| `sqlite3` | stdlib | Database operations via existing KeywordDB | Already in use across all analytics tools |
| `statistics` | stdlib | Cross-creator pattern frequency analysis | Mean, stdev for identifying universal patterns (3+ creators) |

### Supporting Libraries

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| `collections.Counter` | stdlib | Count pattern occurrences per creator | Frequency analysis for synthesis |
| `typing` | stdlib | Type hints for maintainability | Error dict pattern consistency |
| `datetime` | stdlib | Timestamp extracted techniques | Database `created_at` fields |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Regex-only | spaCy NLP | spaCy requires Python 3.11-3.13 (incompatible with 3.14), overkill for structural patterns, adds ~500MB dependency. Use ONLY if semantic analysis needed beyond patterns. |
| Regex-only | NLTK | Heavyweight for tokenization we don't need, adds dependencies. Regex sufficient for hooks/transitions. |
| JSON in SQLite TEXT | New table per pattern type | Over-normalization. Patterns are hierarchical (category → technique → examples). JSON cleaner. |
| Regex patterns | LLM extraction (Claude API) | Expensive, slow for 80+ files, non-deterministic. Use regex for structural markers, LLM only for ambiguous cases. |

**Installation:**
```bash
# No installation needed - all stdlib
# If NLP becomes necessary later:
# pip install spacy==3.7.2 (Python 3.11-3.13 only)
```

## Architecture Patterns

### Recommended Project Structure

```
tools/youtube-analytics/
├── transcript_analyzer.py      # Pattern extraction from single transcript
├── pattern_synthesizer.py      # Cross-creator synthesis (3+ creators)
├── technique_library.py         # Database CRUD for creator_techniques table
├── test_transcript_analyzer.py
├── test_pattern_synthesizer.py
└── test_technique_library.py

transcripts/
├── Kraut/
│   ├── *.txt
│   └── *.vtt
├── Knowing Better/
├── Fall of Civilizations/
├── Historia Civilis/
├── Alex O'Connor/
└── [others]

.claude/REFERENCE/
└── STYLE-GUIDE.md              # Part 8 auto-generated from DB
```

### Pattern 1: Transcript Pattern Extraction Pipeline

**What:** Parse transcript files, extract structural patterns (hooks, transitions, evidence markers, pacing), store in database with creator attribution.

**When to use:** Processing 80+ transcript files to build technique library.

**Example:**
```python
# Source: Existing pattern_extractor.py and section_diagnostics.py patterns
import re
from pathlib import Path
from typing import Dict, List, Any

def extract_opening_hook(transcript_text: str) -> Dict[str, Any]:
    """
    Identify opening hook patterns in first 60 seconds of transcript.

    Patterns to detect:
    - Visual contrast: "Show X → Show Y → State tension"
    - Current event: "[Date] → [Military action] → [Quote]"
    - Fact-check: "[Quote from figure] → I fact-checked"
    - Personal research: "[Dispute] → So, I read"
    - Escalation: "[Incident] → [X days later] → [Response]"
    """
    first_60_sec = get_first_n_seconds(transcript_text, 60)

    patterns = {
        'visual_contrast': bool(re.search(r'\b(now|instead|but)\b.*\b(see|shows?|displays?)\b', first_60_sec, re.I)),
        'fact_check_declaration': bool(re.search(r'\b(fact-check|I checked|I read|I found)\b', first_60_sec, re.I)),
        'current_event': bool(re.search(r'\b(today|yesterday|last week|this month)\b', first_60_sec, re.I)),
        'escalation_timeline': bool(re.search(r'\b(\d+ days? later|then|after that)\b', first_60_sec, re.I))
    }

    return {
        'category': 'opening_hook',
        'detected_patterns': [k for k, v in patterns.items() if v],
        'text_sample': first_60_sec[:200],
        'confidence': 'high' if sum(patterns.values()) > 0 else 'low'
    }

def extract_transitions(transcript_text: str) -> List[Dict[str, Any]]:
    """
    Identify transition patterns between sections.

    Patterns:
    - Causal chains: "consequently", "thereby", "which meant that"
    - Temporal jumps: "Now", "Fast forward to"
    - Pivots: "So how did we get here?", "But here's where it gets interesting"
    - Date breaks: Stand-alone dates as section markers
    """
    transitions = []

    # Causal chain markers
    causal_matches = re.finditer(
        r'\b(consequently|thereby|which meant that|this led to|as a result)\b',
        transcript_text,
        re.I
    )
    for match in causal_matches:
        transitions.append({
            'pattern_type': 'causal_chain',
            'text': get_context(transcript_text, match.start(), 100),
            'position': match.start()
        })

    # Temporal jumps
    temporal_matches = re.finditer(
        r'\b(Now|Fast forward|Years later|Meanwhile)\b[,:]',
        transcript_text
    )
    for match in temporal_matches:
        transitions.append({
            'pattern_type': 'temporal_jump',
            'text': get_context(transcript_text, match.start(), 100),
            'position': match.start()
        })

    # Pivot phrases
    pivot_matches = re.finditer(
        r'\b(So how did we get here|But here\'?s where it gets interesting|Look at what just happened)\b',
        transcript_text,
        re.I
    )
    for match in pivot_matches:
        transitions.append({
            'pattern_type': 'pivot_phrase',
            'text': get_context(transcript_text, match.start(), 100),
            'position': match.start()
        })

    return transitions

def extract_evidence_patterns(transcript_text: str) -> Dict[str, int]:
    """
    Count evidence presentation patterns.

    Markers:
    - Direct quotes: "Here's what X actually says"
    - Source citations: "According to", "page X"
    - Document reveals: "Notice this phrase", "Reading directly from"
    - Authority stacking: Multiple quotes for same claim
    """
    return {
        'direct_quotes': len(re.findall(r"Here'?s what .{1,50} actually says", transcript_text, re.I)),
        'according_to': len(re.findall(r'\baccording to\b', transcript_text, re.I)),
        'page_citations': len(re.findall(r'\bpage \d+\b', transcript_text, re.I)),
        'document_reveals': len(re.findall(r'\b(notice this|reading directly from)\b', transcript_text, re.I)),
        'quote_density': len(re.findall(r'["""].{10,}["""]', transcript_text)) / (len(transcript_text.split()) / 100)
    }

def analyze_transcript_file(file_path: Path) -> Dict[str, Any]:
    """
    Full analysis pipeline for single transcript.

    Returns:
        {
            'creator': 'Kraut',
            'video_title': 'How Vodka ruined Russia',
            'opening_hook': {...},
            'transitions': [...],
            'evidence_patterns': {...},
            'pacing': {...},
            'file_path': str(file_path)
        }
    """
    text = file_path.read_text(encoding='utf-8')
    creator = file_path.parent.name if file_path.parent.name != 'transcripts' else 'History vs Hype'

    return {
        'creator': creator,
        'video_title': file_path.stem,
        'opening_hook': extract_opening_hook(text),
        'transitions': extract_transitions(text),
        'evidence_patterns': extract_evidence_patterns(text),
        'pacing': analyze_pacing(text),
        'file_path': str(file_path),
        'analyzed_at': datetime.utcnow().isoformat()
    }
```

### Pattern 2: Cross-Creator Synthesis

**What:** Identify techniques appearing in 3+ successful creators as universal best practices.

**When to use:** After extracting patterns from all transcripts, before generating Part 8.

**Example:**
```python
# Source: Similar to playbook_synthesizer.py pattern ranking
from collections import Counter
from statistics import mean
from typing import Dict, List, Any

def synthesize_universal_patterns(all_analyses: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Identify patterns appearing across multiple creators.

    Universal = appears in 3+ different creators.
    Confidence based on creator count.
    """
    # Group by creator
    by_creator = {}
    for analysis in all_analyses:
        creator = analysis['creator']
        if creator not in by_creator:
            by_creator[creator] = []
        by_creator[creator].append(analysis)

    # Track pattern occurrences across creators
    pattern_creators = {
        'opening_hooks': Counter(),
        'transitions': Counter(),
        'evidence': Counter()
    }

    for creator, analyses in by_creator.items():
        # Opening hooks this creator uses
        opening_patterns = set()
        for a in analyses:
            opening_patterns.update(a['opening_hook']['detected_patterns'])

        for pattern in opening_patterns:
            pattern_creators['opening_hooks'][pattern] += 1

        # Transitions this creator uses
        transition_types = set()
        for a in analyses:
            transition_types.update([t['pattern_type'] for t in a['transitions']])

        for pattern in transition_types:
            pattern_creators['transitions'][pattern] += 1

    # Extract universal patterns (3+ creators)
    universal = {
        'opening_hooks': [
            {'pattern': p, 'creator_count': count}
            for p, count in pattern_creators['opening_hooks'].items()
            if count >= 3
        ],
        'transitions': [
            {'pattern': p, 'creator_count': count}
            for p, count in pattern_creators['transitions'].items()
            if count >= 3
        ]
    }

    # Sort by creator count descending
    universal['opening_hooks'].sort(key=lambda x: x['creator_count'], reverse=True)
    universal['transitions'].sort(key=lambda x: x['creator_count'], reverse=True)

    return universal

def generate_style_guide_part8(universal_patterns: Dict[str, Any]) -> str:
    """
    Generate STYLE-GUIDE.md Part 8 from universal patterns.

    Similar to playbook_synthesizer.py Part 9 generation.
    """
    markdown = ["## Part 8: Creator Technique Library (Auto-Generated)", ""]
    markdown.append(f"**Last updated:** {datetime.utcnow().strftime('%Y-%m-%d')}")
    markdown.append(f"**Source:** Cross-creator analysis of {len(universal_patterns)} techniques")
    markdown.append("")

    markdown.append("### 8.1 Universal Opening Hooks")
    markdown.append("")
    markdown.append("Patterns appearing in 3+ successful creators:")
    markdown.append("")

    for hook in universal_patterns['opening_hooks']:
        markdown.append(f"**{hook['pattern'].replace('_', ' ').title()}** "
                       f"({hook['creator_count']} creators)")
        # Add formula, examples, when-to-use from DB
        markdown.append("")

    return "\n".join(markdown)
```

### Pattern 3: Database Integration with Schema v28

**What:** Store extracted techniques in new `creator_techniques` table, migrate schema to v28.

**When to use:** Permanent storage for searchable technique library.

**Example:**
```python
# Source: Existing database.py migration patterns
def _ensure_creator_techniques_table(self):
    """
    Migrate to schema v28: creator_techniques table.

    Follows existing migration pattern from database.py.
    """
    cursor = self._conn.cursor()

    # Check current schema version
    cursor.execute("PRAGMA user_version")
    version = cursor.fetchone()[0]

    if version < 28:
        # Create creator_techniques table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS creator_techniques (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                technique_category TEXT NOT NULL,
                technique_name TEXT NOT NULL,
                formula TEXT,
                when_to_use TEXT,
                creator_examples TEXT,
                creator_count INTEGER DEFAULT 1,
                is_universal BOOLEAN DEFAULT 0,
                style_guide_ref TEXT,
                created_at DATE NOT NULL,
                UNIQUE(technique_category, technique_name)
            )
        """)

        cursor.execute("CREATE INDEX IF NOT EXISTS idx_techniques_category "
                      "ON creator_techniques(technique_category)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_techniques_universal "
                      "ON creator_techniques(is_universal DESC, creator_count DESC)")

        # Update schema version
        cursor.execute("PRAGMA user_version = 28")
        self._conn.commit()

def add_technique(
    self,
    category: str,
    name: str,
    formula: str,
    when_to_use: str,
    creator_examples: List[Dict[str, str]],
    is_universal: bool = False
) -> Dict[str, Any]:
    """
    Add or update creator technique in database.

    Args:
        category: 'opening_hook', 'transition', 'evidence', etc.
        name: 'visual_contrast_hook', 'causal_chain', etc.
        formula: Template pattern string
        when_to_use: Guidance for when to apply
        creator_examples: [{'creator': 'Kraut', 'video': '...', 'text': '...'}]
        is_universal: True if appears in 3+ creators

    Returns:
        {'technique_id': int, 'action': 'inserted'|'updated'}
        {'error': msg} on failure
    """
    try:
        cursor = self._conn.cursor()
        examples_json = json.dumps(creator_examples)
        creator_count = len(set(ex['creator'] for ex in creator_examples))

        cursor.execute("""
            INSERT INTO creator_techniques
            (technique_category, technique_name, formula, when_to_use,
             creator_examples, creator_count, is_universal, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(technique_category, technique_name) DO UPDATE SET
                formula = excluded.formula,
                when_to_use = excluded.when_to_use,
                creator_examples = excluded.creator_examples,
                creator_count = excluded.creator_count,
                is_universal = excluded.is_universal
        """, (category, name, formula, when_to_use, examples_json,
              creator_count, is_universal, datetime.utcnow().date().isoformat()))

        self._conn.commit()

        return {
            'technique_id': cursor.lastrowid,
            'action': 'inserted' if cursor.rowcount == 1 else 'updated'
        }

    except sqlite3.Error as e:
        return {'error': f'Database error: {str(e)}'}
```

### Pattern 4: Script-Writer-v2 Integration

**What:** Update script-writer-v2.md to read Part 8 and apply techniques during generation (new Rule 17).

**When to use:** After Part 8 exists with techniques.

**Example:**
```markdown
### RULE 17: CREATOR TECHNIQUE LIBRARY (Added 2026-02-14)

**Apply universal techniques from STYLE-GUIDE.md Part 8 during script generation.**

**Part 8 contains techniques extracted from 80+ creator transcripts:**
- Opening hooks (visual contrast, fact-check declaration, escalation)
- Transitions (causal chains, temporal jumps, pivots)
- Evidence presentation (direct quotes, source citations, document reveals)
- Pacing patterns (pattern interrupts, rhythm breaks)

**Usage:**
1. Read Part 8 before script generation (same as Parts 1-7, 9)
2. Select 2-3 relevant techniques per script section type
3. Apply technique formulas with script-specific content
4. Reference technique in comment: `<!-- Part 8.1: Visual Contrast Hook -->`

**Example - Opening hook selection:**
```
Section type: intro
Topic type: territorial
Technique: Part 8.1 Visual Contrast Hook
Formula: [Show visual A] → [Show visual B] → [State tension]

Applied:
"Open a map of Central America, you see Belize, a small country on the Caribbean coast.
Now open a Guatemalan map. Belize disappears, instead you see 'Territorio de Belize.'
Guatemala claims this entire country as their own."
```

**Don't force-fit techniques.** If no Part 8 technique naturally applies, use Parts 1-7 core principles.
```

### Anti-Patterns to Avoid

- **Over-extraction:** Don't extract every phrase as a "pattern". Focus on structural elements (hooks, transitions, evidence markers) that appear across multiple videos. Pattern = appears 3+ times.

- **Creator-specific quirks as universal:** Don't mark technique as universal if only 1-2 creators use it. Universal = 3+ creators minimum.

- **Ignoring existing Part 6:** Part 6 already has 29 voice patterns. Part 8 should complement (creator-validated examples), not duplicate. If pattern exists in Part 6, add creator examples to existing entry.

- **Manual STYLE-GUIDE editing:** Part 8 should be auto-generated from database (like Part 9) to stay in sync with creator_techniques table. Don't manually edit Part 8.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Transcript parsing (.srt, .vtt formats) | Custom parser | Regex for SRT (`\d+\n\d{2}:\d{2}.*\n(.+)`), read .txt directly | SRT format is simple: index, timestamp, text. Regex sufficient. |
| Pattern frequency analysis | Custom counter logic | `collections.Counter` | Built-in, tested, faster than manual counting |
| Schema migration system | New migration framework | Existing `PRAGMA user_version` pattern in database.py | Already works for v1-27, use same approach for v28 |
| NLP for structural patterns | spaCy/NLTK pipelines | Regex for markers ("consequently", "according to", "here's what") | Structural patterns = keyword/phrase matching. NLP overkill for this. |
| Cross-creator similarity scoring | TF-IDF/cosine similarity | Simple threshold (3+ creators have pattern) | Don't need fuzzy matching. Either creator uses "consequently" or doesn't. |

**Key insight:** Transcript analysis for structural patterns is simpler than semantic NLP. Use regex for keywords, avoid heavyweight frameworks.

## Common Pitfalls

### Pitfall 1: Python Version Incompatibility with spaCy

**What goes wrong:** Installing spaCy 3.x fails on Python 3.14+ because spaCy requires 3.11-3.13.

**Why it happens:** Memory mentions "Python 3.11-3.13 required (spaCy incompatible with 3.14)". User's environment may have Python 3.14.

**How to avoid:** Don't use spaCy unless semantic analysis becomes necessary. Regex sufficient for structural patterns (hooks, transitions). If NLP required later, pin Python to 3.13 in requirements.

**Warning signs:** ImportError for spaCy, pip installation failures mentioning Python version.

### Pitfall 2: Transcript Format Heterogeneity

**What goes wrong:** Parser assumes all transcripts are .txt format, breaks on .srt/.vtt files with timecodes.

**Why it happens:** Transcripts folder has mixed formats (.txt, .srt, .vtt). SRT/VTT have timecodes that pollute text extraction.

**How to avoid:**
- Detect format by file extension
- For .srt/.vtt: Strip timecodes with regex before analysis
- For .txt: Read directly
- Store original format in database for reproducibility

**Warning signs:** Extracted "patterns" contain timecodes like "01:00:00,166", pattern detection fails.

**Example fix:**
```python
def read_transcript(file_path: Path) -> str:
    """Read transcript and strip format-specific metadata."""
    text = file_path.read_text(encoding='utf-8')

    if file_path.suffix == '.srt':
        # Remove SRT format: index, timestamp, HTML tags
        text = re.sub(r'\d+\n\d{2}:\d{2}:\d{2},\d+ --> \d{2}:\d{2}:\d{2},\d+\n', '', text)
        text = re.sub(r'<[^>]+>', '', text)  # Remove HTML tags
    elif file_path.suffix == '.vtt':
        # Remove VTT format: WEBVTT header, timestamps
        text = re.sub(r'WEBVTT\n\n', '', text)
        text = re.sub(r'\d{2}:\d{2}:\d{2}\.\d+ --> \d{2}:\d{2}:\d{2}\.\d+\n', '', text)
        text = re.sub(r'<[^>]+>', '', text)

    # Clean up multiple newlines
    text = re.sub(r'\n{3,}', '\n\n', text)

    return text
```

### Pitfall 3: Creator Folder Structure Assumptions

**What goes wrong:** Code assumes all transcripts are in `transcripts/Creator Name/*.txt` subfolders, breaks on flat files in `transcripts/` root.

**Why it happens:** Current structure has mixed organization (some in subfolders like `Kraut/`, some in root like `belize-guatemala-dispute.srt`).

**How to avoid:**
- Check if file is in subfolder → use folder name as creator
- If file is in root → extract creator from filename or mark as 'History vs Hype' (own videos)
- Don't assume subfolder structure exists

**Warning signs:** Creator attribution is 'transcripts' instead of actual creator name.

**Example fix:**
```python
def get_creator_name(file_path: Path) -> str:
    """Extract creator name from file path."""
    if file_path.parent.name == 'transcripts':
        # File in root - assume it's own video
        return 'History vs Hype'
    else:
        # File in subfolder - use folder name
        return file_path.parent.name
```

### Pitfall 4: Over-Normalization of Technique Storage

**What goes wrong:** Creating separate tables for technique_categories, technique_examples, technique_creators leads to complex JOINs and slow queries.

**Why it happens:** Trying to avoid JSON in SQLite by over-normalizing.

**How to avoid:** Use JSON for hierarchical data (creator_examples list). SQLite handles JSON fine for read-mostly workloads. Avoid JOIN complexity.

**Warning signs:** 5+ table schema for simple technique storage, slow queries for retrieving techniques by category.

### Pitfall 5: Ignoring Existing Part 6 Patterns

**What goes wrong:** Part 8 duplicates patterns already in Part 6 (29 patterns across 6 categories).

**Why it happens:** Not reading Part 6 before extraction, treating every creator pattern as "new".

**How to avoid:**
- Load Part 6 patterns before synthesis
- If extracted pattern matches Part 6 entry → add creator examples to existing pattern metadata, don't create duplicate
- Part 8 should be "creator-validated examples of Part 6 patterns" + any net-new patterns not in Part 6

**Warning signs:** Part 8 has "Causal Chain" pattern when Part 6.2 already has "Kraut-Style Causal Chain".

## Code Examples

Verified patterns from existing codebase:

### Pattern Extraction (from section_diagnostics.py)

```python
# Source: tools/youtube-analytics/section_diagnostics.py load_voice_patterns()
def load_voice_patterns():
    """
    Load voice patterns from STYLE-GUIDE.md Part 6.

    Returns dict organized by category with 29 patterns total.
    """
    return {
        'openings': {
            'visual_contrast_hook': {
                'name': 'Visual Contrast Hook',
                'formula': '[Show visual A] → [Show visual B] → [State tension]',
                'when': 'Territorial disputes with map changes',
                'style_guide_ref': 'Part 6.1 Pattern 1'
            },
            # ... 4 more opening patterns
        },
        'transitions': {
            'causal_chain': {
                'name': 'Kraut-Style Causal Chain',
                'formula': '[Event A] → consequently/thereby/which meant that → [Result B]',
                'when': 'Explaining multi-step causation',
                'style_guide_ref': 'Part 6.2 Pattern 1'
            },
            # ... 7 more transition patterns
        },
        # ... evidence, rhythm, closings, additional categories
    }
```

### Database Pattern (from database.py)

```python
# Source: tools/discovery/database.py migration pattern
def _ensure_feedback_tables(self):
    """Phase 27 migration: feedback storage."""
    cursor = self._conn.cursor()

    # Check schema version
    cursor.execute("PRAGMA user_version")
    version = cursor.fetchone()[0]

    if version < 27:
        # Add columns to existing table
        cursor.execute("ALTER TABLE video_performance ADD COLUMN retention_drop_point INTEGER")
        cursor.execute("ALTER TABLE video_performance ADD COLUMN discovery_issues TEXT")
        cursor.execute("ALTER TABLE video_performance ADD COLUMN lessons_learned TEXT")

        # Create new table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS section_feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                video_id TEXT NOT NULL,
                section_name TEXT NOT NULL,
                retention_percent REAL,
                notes TEXT,
                created_at DATE,
                FOREIGN KEY (video_id) REFERENCES video_performance(video_id)
            )
        """)

        cursor.execute("CREATE INDEX IF NOT EXISTS idx_section_feedback_video "
                      "ON section_feedback(video_id)")

        # Update version
        cursor.execute("PRAGMA user_version = 27")
        self._conn.commit()
```

### Synthesis Pattern (from playbook_synthesizer.py)

```python
# Source: tools/youtube-analytics/playbook_synthesizer.py
def synthesize_part9(db: KeywordDB) -> str:
    """
    Generate STYLE-GUIDE.md Part 9 from retention data.

    Similar approach for Part 8 creator techniques.
    """
    videos = get_all_video_retention_data()

    opening_patterns = extract_opening_patterns(videos)
    transition_patterns = extract_transition_patterns(videos)

    markdown = ["## Part 9: Retention Playbook (Auto-Generated)", ""]
    markdown.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d')}")
    markdown.append("")

    # Add sections for each pattern type
    # ...

    return "\n".join(markdown)

def write_part9_to_style_guide(content: str, style_guide_path: Path):
    """Update STYLE-GUIDE.md Part 9 in-place."""
    guide = style_guide_path.read_text(encoding='utf-8')

    # Find Part 9 boundaries
    start = guide.find("## Part 9:")
    end = guide.find("\n## Part", start + 1)

    if start == -1:
        # Part 9 doesn't exist - append
        guide += f"\n\n{content}"
    else:
        # Replace existing Part 9
        if end == -1:
            end = len(guide)
        guide = guide[:start] + content + guide[end:]

    style_guide_path.write_text(guide, encoding='utf-8')
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Manual pattern documentation | Auto-generated from transcript analysis | Phase 37 (2026-02) | Part 8 stays in sync with creator techniques DB |
| Part 6 patterns from memory | Part 6 + Part 8 creator-validated examples | Phase 37 | Concrete examples from successful videos |
| spaCy for all text analysis | Regex for structural patterns, spaCy only for semantic | 2025+ best practice | Avoid unnecessary dependencies |
| Flat file storage for patterns | Database with searchable categories | Phase 37 | Script-writer can query by section type |

**Deprecated/outdated:**
- **Heavy NLP for pattern extraction:** Regex sufficient for structural markers (hooks, transitions). Use NLP only for semantic similarity (not needed here).
- **Manual STYLE-GUIDE Part 8 editing:** Should be auto-generated like Part 9 to prevent drift from database.

## Open Questions

1. **Should Part 8 replace or complement Part 6?**
   - What we know: Part 6 has 29 patterns, Part 8 extracts from 80+ transcripts
   - What's unclear: Overlap strategy - merge into Part 6 or keep separate?
   - Recommendation: Keep Part 6 (authoritative patterns), Part 8 adds creator examples. Cross-reference: "See Part 6.2 Pattern 1 for formula, Part 8.2 for Kraut/Shaun examples"

2. **What's the threshold for "universal" pattern?**
   - What we know: 3+ creators is mentioned in requirements
   - What's unclear: Should frequency within each creator matter? (e.g., Kraut uses causal chains 50x vs. 2x)
   - Recommendation: Binary threshold (3+ creators use pattern = universal). Frequency tracked but not used for universal designation.

3. **How to handle creator-specific innovations?**
   - What we know: Some techniques may be unique to 1-2 creators but highly effective
   - What's unclear: Store in database but mark as non-universal? Separate section in Part 8?
   - Recommendation: Store all extracted techniques (even 1-creator patterns) in DB with `is_universal=False`. Part 8 only shows universal (3+), but database preserves all for future analysis.

4. **Should transcript analysis be one-time or continuous?**
   - What we know: Initial run on 80+ existing transcripts
   - What's unclear: Re-analyze periodically as new creator videos added?
   - Recommendation: One-time for Phase 37. Add re-analysis command for future use: `python transcript_analyzer.py --update-all`

## Sources

### Primary (HIGH confidence)

- **Existing codebase patterns:**
  - `tools/youtube-analytics/section_diagnostics.py` - Pattern detection logic (29 voice patterns)
  - `tools/youtube-analytics/playbook_synthesizer.py` - Part 9 generation pattern
  - `tools/youtube-analytics/pattern_extractor.py` - Pattern ranking logic
  - `tools/discovery/database.py` - Schema migration pattern (PRAGMA user_version)
  - `.claude/REFERENCE/STYLE-GUIDE.md` - Parts 1-9 structure

- **Transcript inventory:**
  - 83 total transcript files (64 in root + 19 in subfolders)
  - Formats: .txt (plain text), .srt (SubRip with timecodes), .vtt (WebVTT with timecodes)
  - Creators: Kraut, Knowing Better, Fall of Civilizations, Historia Civilis, Alex O'Connor, plus own videos
  - Current database: schema v27 (keywords.db with PRAGMA user_version)

### Secondary (MEDIUM confidence)

- [Text Analysis in Python: Techniques and Libraries](https://airbyte.com/data-engineering-resources/text-analysis-in-python) - Python text analysis best practices
- [NLP Libraries in Python - GeeksforGeeks](https://www.geeksforgeeks.org/nlp/nlp-libraries-in-python/) - NLTK, spaCy comparison
- [spaCy documentation](https://spacy.io/) - Industrial-strength NLP (Python 3.11-3.13 only)
- [YouTube Audience Retention Guide](https://socialrails.com/blog/youtube-audience-retention-complete-guide) - 40-60% retention benchmarks, 30-second retention importance

### Tertiary (LOW confidence)

- [Regex Data Extraction - Medium](https://medium.com/@kapoorchinmay231/regex-data-extraction-using-python-pattern-detection-for-files-fundamental-overview-e0f1342ddc9c) - Regex extraction patterns
- [Python RegEx - W3Schools](https://www.w3schools.com/python/python_regex.asp) - Basic regex tutorial

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - All stdlib, verified in existing codebase
- Architecture: HIGH - Follows existing patterns (playbook_synthesizer, database migrations)
- Pitfalls: HIGH - Derived from memory notes and codebase inspection
- Transcript parsing: MEDIUM - Regex patterns verified manually, edge cases possible

**Research date:** 2026-02-14
**Valid until:** 2026-03-14 (30 days - stable domain, stdlib only)
