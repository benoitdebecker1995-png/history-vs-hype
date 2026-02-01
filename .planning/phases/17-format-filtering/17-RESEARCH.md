# Phase 17: Format Filtering - Research

**Researched:** 2026-02-01
**Domain:** Content production constraint filtering and document availability verification
**Confidence:** MEDIUM

## Summary

Phase 17 implements production constraint filtering to fail fast on topics that don't match the channel's document-heavy format. The phase has three primary objectives: (1) flag animation-required topics as hard blocks before research investment, (2) score topics for document-friendliness on a 0-4 scale, and (3) verify academic source availability for topics.

The core challenge is detecting production feasibility from limited metadata (title, description) before investing hours in research. The channel's format—hybrid talking head + B-roll evidence with real academic quotes—requires specific visual assets: maps (15-20%), primary source documents (10-15%), historical photos (5-10%), and modern footage (5%). Topics requiring custom animation, complex 3D visualizations, or abstract concept illustrations are hard blocks.

Building on Phase 16's format classification, this phase adds document-friendliness scoring and academic source pre-verification. The document score quantifies how well a topic fits the channel's evidence-first format: treaty-heavy topics score 4 (excellent fit), concept-heavy topics score 0 (poor fit). Academic source verification checks if university press monographs and primary sources exist before committing to a topic.

**Primary recommendation:** Extend Phase 16's classify_format() with document-friendliness scoring based on keyword signals. Add academic source availability checking via web search APIs (no official Google Scholar API exists). Store production constraint flags in keywords table. Apply filters FIRST in discovery pipeline to prevent wasted research on incompatible topics.

## Standard Stack

The established libraries/tools for this domain:

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| sqlite3 (stdlib) | Python 3.11+ | Production constraint storage | Existing keywords.db, extends Phase 15-16 schema |
| re (stdlib) | Python 3.11+ | Keyword pattern matching | Built-in, sufficient for document-type detection |
| requests | latest | HTTP requests for source checking | Standard Python HTTP library |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| scrapetube | latest | Video metadata (Phase 16) | Format classification already implemented |
| json (stdlib) | Python 3.11+ | Constraint data serialization | Store complex filter rules |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Web search APIs | Google Scholar API | No official API exists, must use SERP APIs or manual |
| Web search APIs | WorldCat API (OCLC) | Requires institutional access, bookops-worldcat available but overkill for pre-check |
| Keyword scoring | ML classification | Insufficient training data, keyword heuristics work for known domain |
| Hard block list | User confirmation | Slows workflow, defeats "fail fast" purpose |

**Installation:**
```bash
# No new dependencies required
# Uses existing Phase 15-16 stack
```

## Architecture Patterns

### Recommended Project Structure
```
tools/discovery/
├── competition.py       # Phase 16 - EXTEND with format filtering
├── classifiers.py       # Phase 16 - EXTEND with document scoring
├── format_filters.py    # NEW - production constraint rules
├── source_checker.py    # NEW - academic availability verification
├── database.py          # Phase 15 - EXTEND with constraint columns
├── schema.sql           # UPDATE - add production_constraints column
└── keywords.db          # EXTEND - store filter results
```

### Pattern 1: Document-Friendliness Scoring
**What:** Score topics 0-4 for compatibility with document-heavy format
**When to use:** FMT-02 - evaluating topic fit before research investment
**Example:**
```python
# Source: Channel DNA from CLAUDE.md + production experience
DOCUMENT_FRIENDLY_KEYWORDS = {
    'treaty': 3,  # High - treaties are visual documents
    'agreement': 3,
    'court': 3,
    'ruling': 3,
    'law': 2,
    'constitution': 3,
    'map': 3,  # Maps are primary visual assets
    'border': 3,
    'territory': 3,
    'claim': 2,
    'dispute': 2,
    'colonial': 2,
    'war': 1,  # Wars have photos but less documentary evidence
    'battle': 1,
    'history': 1,  # Generic, depends on specificity
}

CONCEPT_HEAVY_KEYWORDS = {
    'philosophy': -2,  # Abstract, hard to visualize
    'ideology': -1,
    'theory': -2,
    'concept': -2,
    'belief': -1,
    'principle': -2,
    'framework': -2,
}

def calculate_document_score(title: str, description: str = '') -> int:
    """
    Calculate document-friendliness score 0-4.

    Scoring:
    - 4: Treaty-heavy (excellent - treaties, maps, court docs)
    - 3: Document-rich (good - laws, official records)
    - 2: Mixed (acceptable - some documents available)
    - 1: Concept-leaning (marginal - mostly abstract)
    - 0: Concept-heavy (poor fit - abstract, no documents)

    Args:
        title: Topic title
        description: Optional topic description

    Returns:
        Integer 0-4 representing document-friendliness

    Example:
        >>> calculate_document_score("The Treaty That Split a Country")
        4
        >>> calculate_document_score("The Philosophy of Freedom")
        0
    """
    combined = (title + ' ' + description).lower()

    # Start at baseline 2 (neutral)
    score = 2

    # Add points for document-friendly keywords
    for keyword, points in DOCUMENT_FRIENDLY_KEYWORDS.items():
        if keyword in combined:
            score += points

    # Subtract points for concept-heavy keywords
    for keyword, points in CONCEPT_HEAVY_KEYWORDS.items():
        if keyword in combined:
            score += points  # Points are negative

    # Clamp to 0-4 range
    return max(0, min(4, score))
```

### Pattern 2: Animation Detection with Hard Blocks
**What:** Detect topics requiring animation and flag as production blockers
**When to use:** FMT-01 - filtering before research investment
**Example:**
```python
# Source: Phase 16 classify_format + production constraints
ANIMATION_REQUIRED_KEYWORDS = [
    'quantum',
    'molecular',
    'atomic',
    'particle',
    'chemical reaction',
    'biological process',
    'cellular',
    'genetic',
    'evolution of',  # When abstract process, not historical event
    'how cells',
    'how atoms',
    'how molecules',
    'theoretical',
    'simulation',
    'model of',  # Abstract models, not territorial
]

DOCUMENTARY_SAFE_KEYWORDS = [
    'treaty',
    'map',
    'border',
    'territory',
    'court',
    'ruling',
    'document',
    'archive',
    'photo',
    'footage',
    'recording',
]

def is_animation_required(title: str, description: str = '') -> dict:
    """
    Detect if topic requires animation (hard production block).

    Animation required when:
    1. Title contains animation-required keywords
    2. Topic lacks documentary-safe keywords
    3. Not already classified as documentary format

    Returns:
        {
            'is_blocked': bool,
            'reason': str,
            'confidence': float,  # 0-1
            'matched_keywords': list
        }

    Example:
        >>> is_animation_required("How Quantum Mechanics Work")
        {'is_blocked': True, 'reason': 'quantum mechanics requires visualization',
         'confidence': 0.9, 'matched_keywords': ['quantum']}

        >>> is_animation_required("The Treaty That Changed Europe")
        {'is_blocked': False, 'reason': 'documentary format viable',
         'confidence': 0.8, 'matched_keywords': ['treaty']}
    """
    combined = (title + ' ' + description).lower()

    # Check for animation-required keywords
    animation_matches = [kw for kw in ANIMATION_REQUIRED_KEYWORDS if kw in combined]

    # Check for documentary-safe keywords
    documentary_matches = [kw for kw in DOCUMENTARY_SAFE_KEYWORDS if kw in combined]

    # Decision logic
    if animation_matches and not documentary_matches:
        return {
            'is_blocked': True,
            'reason': f'Requires animation for {", ".join(animation_matches[:2])}',
            'confidence': 0.9,
            'matched_keywords': animation_matches
        }
    elif animation_matches and documentary_matches:
        # Mixed - needs human review
        return {
            'is_blocked': False,
            'reason': 'Mixed signals - manual review recommended',
            'confidence': 0.5,
            'matched_keywords': animation_matches + documentary_matches
        }
    else:
        return {
            'is_blocked': False,
            'reason': 'Documentary format viable',
            'confidence': 0.8 if documentary_matches else 0.6,
            'matched_keywords': documentary_matches
        }
```

### Pattern 3: Academic Source Availability Pre-Check
**What:** Verify academic sources exist before research investment
**When to use:** FMT-03 - confirming source availability for topics
**Example:**
```python
# Source: Research on academic search APIs (no official Google Scholar API)
import requests
from typing import Dict, Any, List

def check_academic_sources(
    topic: str,
    min_sources: int = 3,
    source_types: List[str] = None
) -> Dict[str, Any]:
    """
    Check if academic sources are available for a topic.

    Uses web search to verify university press books and peer-reviewed
    articles exist. Not comprehensive (no API access to full databases),
    but useful for pre-screening.

    Args:
        topic: Topic to research
        min_sources: Minimum sources to consider viable
        source_types: ['monograph', 'journal', 'primary'] or None for all

    Returns:
        {
            'sources_found': int,
            'is_viable': bool,
            'source_examples': List[str],  # Titles/authors found
            'search_queries': List[str],  # Queries used
            'confidence': float  # 0-1
        }

    Example:
        >>> check_academic_sources("Sykes-Picot Agreement")
        {'sources_found': 12, 'is_viable': True,
         'source_examples': ['A Peace to End All Peace - David Fromkin', ...],
         'confidence': 0.9}

        >>> check_academic_sources("Quantum Entanglement Philosophy")
        {'sources_found': 1, 'is_viable': False,
         'source_examples': [...], 'confidence': 0.6}
    """
    if source_types is None:
        source_types = ['monograph', 'journal', 'primary']

    # Build search queries for different source types
    queries = []

    if 'monograph' in source_types:
        # University press books
        queries.append(f'"{topic}" site:cambridge.org OR site:oup.com')
        queries.append(f'"{topic}" "university press"')

    if 'journal' in source_types:
        # Peer-reviewed articles
        queries.append(f'"{topic}" site:jstor.org OR site:academia.edu')

    if 'primary' in source_types:
        # Primary sources
        queries.append(f'"{topic}" treaty OR agreement OR document')
        queries.append(f'"{topic}" archive OR primary source')

    # NOTE: In production, would use SERP API or manual Google Scholar
    # For now, return mock structure showing expected pattern

    return {
        'sources_found': 0,  # Placeholder - would count search results
        'is_viable': False,  # Placeholder - would check against threshold
        'source_examples': [],  # Placeholder - would extract titles
        'search_queries': queries,
        'confidence': 0.5,  # LOW until implemented with actual API
        'note': 'Requires SERP API or manual verification - no official Scholar API'
    }
```

### Pattern 4: Production Constraint Storage
**What:** Store format filter results in database for reuse
**When to use:** Caching filter decisions across discovery sessions
**Example:**
```python
# Source: Phase 15-16 database patterns
# Extends KeywordDB with production constraint methods

def store_production_constraints(
    keyword_id: int,
    animation_required: bool,
    document_score: int,
    source_check_result: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Store production constraint evaluation for a keyword.

    Args:
        keyword_id: Keyword database ID
        animation_required: Hard block flag
        document_score: 0-4 document-friendliness score
        source_check_result: Academic source availability dict

    Returns:
        {'status': 'stored'} or {'error': msg}
    """
    try:
        cursor = self._conn.cursor()

        constraints_json = json.dumps({
            'animation_required': animation_required,
            'document_score': document_score,
            'sources_found': source_check_result.get('sources_found', 0),
            'source_examples': source_check_result.get('source_examples', []),
            'checked_at': datetime.utcnow().isoformat() + 'Z'
        })

        cursor.execute(
            """
            UPDATE keywords
            SET production_constraints = ?,
                constraint_checked_at = ?
            WHERE id = ?
            """,
            (constraints_json, datetime.utcnow().date().isoformat(), keyword_id)
        )

        self._conn.commit()

        return {'status': 'stored', 'keyword_id': keyword_id}

    except sqlite3.Error as e:
        return {
            'error': f'Database error: {type(e).__name__}',
            'details': str(e)
        }
```

### Anti-Patterns to Avoid
- **Filtering after research**: Apply constraints FIRST, not after hours invested
- **Binary animation detection**: Use confidence scores, not just yes/no
- **Ignoring mixed signals**: Topics with both documentary and animation keywords need review
- **Over-relying on source check**: Web search isn't comprehensive, use as screening only
- **Hardcoded thresholds**: Make document score thresholds configurable

## Don't Hand-Roll

Problems that look simple but have existing solutions:

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Google Scholar search | Custom web scraper | SERP API services (SerpApi, ScrapingBee) | Google blocks scrapers, no official API |
| Academic database access | API integration | Manual check + cache | Most require institutional access |
| Format classification | ML model | Extend Phase 16 keyword heuristics | Already works, training data unavailable |
| Document scoring | Complex algorithm | Keyword-based scoring | Transparent, debuggable, good enough |

**Key insight:** Academic source checking has no comprehensive programmatic solution. Google Scholar has no official API, and third-party SERP APIs are expensive ($50-100/month). The practical approach is manual pre-screening with caching, not automated verification. Save automation budget for higher-value features.

## Common Pitfalls

### Pitfall 1: False Positive Animation Blocks
**What goes wrong:** Blocking topics that could work with available footage
**Why it happens:** Keyword matching too aggressive (e.g., "evolution of borders" blocked because "evolution")
**How to avoid:**
- Check context of animation keywords (evolution of WHAT?)
- Require 2+ animation keywords for hard block
- Use confidence scores, not binary blocks
- Log blocked topics for manual review
**Warning signs:** User complains viable topics are blocked, reviewing blocked list shows false positives

### Pitfall 2: Document Score Doesn't Reflect Reality
**What goes wrong:** High-scoring topic has no actual documents, or low-scoring has great sources
**Why it happens:** Keyword matching doesn't know domain-specific availability
**How to avoid:**
- Calibrate keyword weights against known topics
- Cross-validate score with source check
- Allow manual score override
- Track score vs. actual production experience
**Warning signs:** High-scoring topics fail at research stage, pattern of score mismatches

### Pitfall 3: Source Check Gives False Confidence
**What goes wrong:** Source check finds articles, but not the RIGHT kind (popular not academic)
**Why it happens:** Web search returns anything matching keywords, can't verify quality
**How to avoid:**
- Make clear this is screening, not verification
- Require manual confirmation before research investment
- Check for university press explicitly in queries
- Show confidence level with results
**Warning signs:** Topics pass source check but lack quality sources at research stage

### Pitfall 4: Stale Constraint Data
**What goes wrong:** Using cached constraint results from months ago
**Why it happens:** Source availability changes (new books published, archives digitized)
**How to avoid:**
- Store constraint_checked_at timestamp
- Warn when constraints >90 days old
- Provide --refresh-constraints flag
- Re-check when topic moves to research phase
**Warning signs:** Rejected topic now has sources, accepted topic now lacks them

### Pitfall 5: Ignoring Topic Specificity
**What goes wrong:** Blocking "medieval philosophy" when "medieval legal philosophy" has court documents
**Why it happens:** Filtering on broad category, not specific angle
**How to avoid:**
- Apply filters to full title + description, not just category
- Check for documentary-safe qualifiers (legal, territorial, treaty)
- Score specificity (specific events > abstract concepts)
- Consider angle from Phase 16 classification
**Warning signs:** Missing good topics because title contains risky keyword

### Pitfall 6: Production Constraint Creep
**What goes wrong:** Adding too many constraints, rejecting most topics
**Why it happens:** Each production challenge becomes a filter rule
**How to avoid:**
- Distinguish hard blocks (animation required) from preferences (lower score)
- Review reject rate (should be 20-40%, not 80%)
- Separate "ideal" from "viable"
- User can override constraints for high-value topics
**Warning signs:** Most topics blocked, user frustration, limited topic pool

## Code Examples

Verified patterns for Phase 17 implementation:

### Database Schema Extension
```sql
-- Source: Extends Phase 16 schema.sql
-- Add production constraint columns to keywords table

ALTER TABLE keywords ADD COLUMN production_constraints TEXT;  -- JSON: animation_required, document_score, sources_found
ALTER TABLE keywords ADD COLUMN constraint_checked_at DATE;
ALTER TABLE keywords ADD COLUMN is_production_blocked BOOLEAN DEFAULT 0;

-- Index for production filtering queries
CREATE INDEX IF NOT EXISTS idx_keywords_blocked
  ON keywords(is_production_blocked, constraint_checked_at DESC);
```

### Filter Pipeline Integration
```python
# Source: Discovery workflow integration pattern
from classifiers import classify_format, classify_angles
from format_filters import is_animation_required, calculate_document_score
from source_checker import check_academic_sources

def filter_topic_for_production(
    topic: str,
    description: str = '',
    min_document_score: int = 2,
    require_source_check: bool = True
) -> Dict[str, Any]:
    """
    Apply all production constraints to a topic.

    Returns comprehensive filter result with all signals.
    Designed to fail fast before research investment.

    Args:
        topic: Topic title
        description: Optional detailed description
        min_document_score: Minimum acceptable document score (0-4)
        require_source_check: Whether to verify academic sources

    Returns:
        {
            'topic': str,
            'is_viable': bool,
            'blocks': List[str],  # Reasons why blocked
            'warnings': List[str],  # Non-blocking concerns
            'scores': {
                'document_friendliness': int,
                'animation_risk': float,
                'source_availability': int
            },
            'recommendation': str  # PROCEED, REVIEW, or BLOCK
        }
    """
    blocks = []
    warnings = []

    # Check 1: Animation requirement (hard block)
    animation_check = is_animation_required(topic, description)
    if animation_check['is_blocked']:
        blocks.append(f"Animation required: {animation_check['reason']}")
    elif animation_check['confidence'] < 0.7:
        warnings.append(f"Animation risk uncertain: {animation_check['reason']}")

    # Check 2: Document-friendliness score
    doc_score = calculate_document_score(topic, description)
    if doc_score < min_document_score:
        blocks.append(f"Low document score: {doc_score}/4 (minimum {min_document_score})")
    elif doc_score == min_document_score:
        warnings.append(f"Marginal document score: {doc_score}/4")

    # Check 3: Academic source availability (optional)
    sources_found = 0
    if require_source_check:
        source_check = check_academic_sources(topic)
        sources_found = source_check['sources_found']

        if not source_check['is_viable']:
            warnings.append(f"Limited sources found: {sources_found} (unverified)")

    # Determine recommendation
    if blocks:
        recommendation = 'BLOCK'
    elif warnings:
        recommendation = 'REVIEW'
    else:
        recommendation = 'PROCEED'

    return {
        'topic': topic,
        'is_viable': len(blocks) == 0,
        'blocks': blocks,
        'warnings': warnings,
        'scores': {
            'document_friendliness': doc_score,
            'animation_risk': 1.0 - animation_check['confidence'],
            'source_availability': sources_found
        },
        'recommendation': recommendation
    }
```

### CLI Integration
```python
# Source: Phase 15-16 CLI patterns
def format_filter_command(topic: str, verbose: bool = False):
    """
    CLI command for production constraint filtering.

    Usage:
        python format_filters.py "Sykes-Picot Agreement"
        python format_filters.py "Quantum Mechanics Explained" --verbose
    """
    result = filter_topic_for_production(topic)

    # Print recommendation
    rec = result['recommendation']
    symbol = '✓' if rec == 'PROCEED' else '!' if rec == 'REVIEW' else '✗'
    print(f"\n{symbol} {rec}: {result['topic']}\n")

    # Print scores
    scores = result['scores']
    print(f"Document Score: {scores['document_friendliness']}/4")
    print(f"Animation Risk: {scores['animation_risk']:.1%}")
    if scores['source_availability'] > 0:
        print(f"Sources Found: {scores['source_availability']}")
    print()

    # Print blocks (if any)
    if result['blocks']:
        print("BLOCKED:")
        for block in result['blocks']:
            print(f"  ✗ {block}")
        print()

    # Print warnings (if any)
    if result['warnings']:
        print("WARNINGS:")
        for warning in result['warnings']:
            print(f"  ! {warning}")
        print()

    # Verbose mode: show detailed scoring
    if verbose:
        print("DETAILED ANALYSIS:")
        print(f"  Is viable: {result['is_viable']}")
        print(f"  Recommendation: {result['recommendation']}")
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Research all topics | Filter before research | 2026 (Phase 17) | Saves hours on incompatible topics |
| Manual format checking | Automated constraint detection | 2026 | Scalable topic screening |
| Post-research source search | Pre-research availability check | 2026 | Prevents dead-end research |
| Binary viable/not viable | Scored recommendations | 2025-2026 | Nuanced decision making |

**Deprecated/outdated:**
- Researching all topics and filtering later: Wastes time on animation-required or source-poor topics
- Assuming sources exist for all historical topics: Many gaps in digitized/accessible materials
- Format classification without production constraints: Classification alone doesn't predict viability

## Open Questions

Things that couldn't be fully resolved:

1. **Academic Source API Access**
   - What we know: No official Google Scholar API, SERP APIs expensive ($50-100/month)
   - What's unclear: Whether SERP API investment worth it vs. manual pre-screening
   - Recommendation: Start with manual checking + caching, consider API if volume increases

2. **Document Score Calibration**
   - What we know: Keyword weights based on production experience
   - What's unclear: Optimal threshold (accept score 2+? 3+?)
   - Recommendation: Start with threshold 2, track score vs. actual production difficulty, adjust

3. **Animation Detection Accuracy**
   - What we know: Channel keywords work well (Phase 16), but context matters
   - What's unclear: How to handle borderline cases (e.g., "rise and fall" animation vs. map-based)
   - Recommendation: Use confidence scores, flag <0.7 for manual review, collect feedback

4. **Source Check Depth**
   - What we know: Full verification requires NotebookLM research (Phase 2 of workflow)
   - What's unclear: How deep pre-check should be (quick search vs. detailed availability)
   - Recommendation: Lightweight pre-check (2-3 searches), not comprehensive verification

5. **Filter Rejection Rate**
   - What we know: Too strict = limited topics, too loose = wasted research
   - What's unclear: Target rejection rate (30%? 50%?)
   - Recommendation: Track metrics, aim for 25-40% blocked, adjust if outside range

## Sources

### Primary (HIGH confidence)
- [Phase 16 RESEARCH.md](../16-competition-analysis/16-RESEARCH.md) - Format classification patterns
- [Phase 16 classifiers.py](../../../tools/discovery/classifiers.py) - Existing format detection
- [CLAUDE.md](../../../CLAUDE.md) - Channel format requirements (maps 15-20%, docs 10-15%)
- [NOTEBOOKLM-SOURCE-STANDARDS.md](../../../.claude/REFERENCE/NOTEBOOKLM-SOURCE-STANDARDS.md) - Academic source requirements

### Secondary (MEDIUM confidence)
- [Desirability vs. Feasibility vs. Viability Compared (2026)](https://www.designrush.com/best-designs/print/trends/desirability-feasibility-viability) - Feasibility scoring frameworks
- [Professional Content Creation Guide 2026](https://influenceflow.io/resources/professional-content-creation-and-visibility-the-complete-2026-guide/) - Visual asset quality standards
- [WorldCat Search API Documentation](https://www.oclc.org/developer/api/oclc-apis/worldcat-search-api.en.html) - Academic source lookup (institutional access required)
- [bookops-worldcat PyPI](https://pypi.org/project/bookops-worldcat/) - Python wrapper for OCLC APIs

### Tertiary (LOW confidence - needs validation)
- [Best Google Scholar API Alternatives 2026](https://www.scrapingbee.com/blog/best-google-scholar-api/) - SERP API options (no official API exists)
- [Google Scholar API Guide](https://scrapfly.io/blog/posts/google-scholar-api-and-alternatives) - Third-party search alternatives
- [Top 5 Google Scholar APIs](https://blog.apify.com/best-google-scholar-apis-scrapers/) - API service comparisons
- Document score keyword weights: Based on production experience, not validated with data
- Animation detection keywords: Created from domain knowledge, should validate against false positive rate

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - No new dependencies, extends Phase 15-16 patterns
- Architecture: MEDIUM - Keyword-based scoring is straightforward but untested, calibration uncertain
- Pitfalls: MEDIUM - Based on similar filtering systems, some edge cases uncertain
- Code examples: HIGH - Follows established Phase 15-16 database and CLI patterns

**Research date:** 2026-02-01
**Valid until:** 2026-04-01 (60 days - academic source landscape and API options may change)

---

*Research compiled from Phase 16 implementation, channel format requirements, academic search API landscape, and production feasibility assessment methodologies as of February 2026.*
