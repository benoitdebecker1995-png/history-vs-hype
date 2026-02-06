# Phase 28: Pacing Analysis - Research

**Researched:** 2026-02-06
**Domain:** Script pacing analysis and readability metrics (Python)
**Confidence:** HIGH

## Summary

Phase 28 extends the existing script-checkers system with quantitative pacing analysis. The standard approach is to use Python's built-in `statistics` module for variance calculations, `textstat` library for readability scores (Flesch Reading Ease), spaCy for entity detection, and simple Unicode sparklines for energy visualization. The checker integrates into the existing CLI pattern following the BaseChecker interface.

Research shows that sentence length variance >15 words (standard deviation), Flesch Reading Ease drops >20 points between sections, and entity density >0.4 (40% proper nouns) are established thresholds for detecting pacing issues in educational content. Pattern interrupt guidelines recommend visual/content changes every 30-90 seconds to maintain viewer retention.

**Primary recommendation:** Use existing tools in the project (spaCy, statistics stdlib), add `textstat` for Flesch scores, implement sparklines with Unicode block characters (▁▂▃▄▅▆▇█), and follow the established checker pattern from stumble/flow/scaffolding checkers.

---

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

**Warning presentation:**
- **Default mode:** Problems-only summary (skip clean sections, show only flagged sections)
- **Verbose mode:** `--verbose` flag shows full section-by-section breakdown with all metrics
- **Root cause explanations:** Each warning includes WHY it's a problem (e.g., "high entity density (0.6) — too many proper nouns in sequence"), but NOT fix suggestions
- **Severity:** Score-based per section (0-100), no label categories (no WARNING/CRITICAL labels)
- **Final verdict:** PASS / NEEDS WORK / FAIL based on critical score thresholds — clear go/no-go before filming

**Threshold calibration:**
- **Source:** Generic defaults from readability/pacing research (not calibrated to user's corpus)
- **Strictness:** Moderate — use the planned thresholds as-is (sentence variance >15, Flesch delta >20, entity density >0.4)
- **Configurability:** Claude's discretion — fit the existing checker architecture pattern
- **Section length:** NOT a scoring factor — length is a style choice for this channel (Kraut runs 30-45 min). Only flag internal pacing issues within sections.

**Energy arc visualization:**
- **Format:** ASCII sparkline chart showing energy/complexity per section (e.g., `▇▅▃▆█▄▂`)
- **Flat zone detection:** Flag monotone stretches — 3+ consecutive sections with similar scores trigger "energy plateau, consider pattern interrupt" advisory
- **Ideal arc comparison:** Claude's discretion — determine if a reference arc adds value
- **Placement in output:** Claude's discretion — place where it flows best with the rest of the report

**Modern relevance / pattern interrupt detection:**
- **Enforcement level:** Advisory only — note the guidelines but don't score or flag as errors. These are creative choices, not mechanical rules.
- **Hook detection method:** Combined keyword heuristic + B-roll marker proxy (time markers like "today", "2024", "still", "currently" + B-roll markers like [NEWS CLIP], [MODERN MAP])
- **Pattern interrupt detection:** Claude's discretion — pick the most reliable approach
- **Severity:** Claude's discretion — determine how to weight missing hooks (separate advisory line vs integrated into score)

### Claude's Discretion
- Configurability approach (config file vs hardcoded vs CLI flags)
- Energy arc placement in output
- Ideal arc comparison inclusion
- Pattern interrupt detection method
- Hook/interrupt severity weighting
- Exact score thresholds for PASS/NEEDS WORK/FAIL verdict

### Specific Requirements
- Must integrate with existing `cli.py` following the established checker pattern (like stumble, scaffolding, repetition, flow checkers)
- The `--pacing` flag on cli.py should invoke this checker
- Section parsing should reuse the production parser from Phase 22 (`tools/production/parser.py`) for consistent section detection
- Channel writes long-form scripts (10-45 min videos) — the checker must handle scripts of any length without false-flagging length itself

### Deferred Ideas (OUT OF SCOPE)
None — discussion stayed within phase scope

</user_constraints>

---

## Standard Stack

The established libraries/tools for pacing analysis in Python:

### Core Dependencies (Already in Project)

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| spaCy | 3.x | NER/POS tagging for entity detection | Already used by flow/stumble checkers, proven NLP foundation |
| statistics | stdlib | Sentence length variance (stdev) | Python standard library, no dependencies |
| production.parser | local | Section parsing from Phase 22 | Consistent section detection across tools |

### New Dependencies (Add to Project)

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| textstat | 0.7.x | Flesch Reading Ease calculation | Industry-standard readability metrics, actively maintained |

### Supporting (No Additional Install)

| Tool | Version | Purpose | When to Use |
|------|---------|---------|-------------|
| Unicode block chars | builtin | Sparkline visualization (▁▂▃▄▅▆▇█) | Energy arc display, no library needed |
| re (regex) | stdlib | Pattern detection for hooks/interrupts | Keyword/marker detection |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| textstat | Manual syllable counting | textstat is battle-tested with edge cases handled |
| Unicode sparklines | sparklines library (PyPI) | Adding dependency for simple 8-char visualization is overkill |
| Custom entity detection | Use spaCy's built-in NER | spaCy already loaded, no reason to duplicate |

**Installation:**
```bash
pip install textstat
# spaCy already installed from existing checkers
# python -m spacy download en_core_web_sm (already done)
```

---

## Architecture Patterns

### Recommended Project Structure
```
tools/script-checkers/
├── checkers/
│   ├── __init__.py           # Import PacingChecker
│   ├── pacing.py            # NEW: PacingChecker implementation
│   ├── stumble.py           # Existing pattern reference
│   └── flow.py              # Existing pattern reference
├── cli.py                   # Add --pacing flag handler
├── config.py                # Add pacing thresholds
└── output.py                # Extend for section-level reporting
```

### Pattern 1: BaseChecker Implementation (Mandatory)

**What:** All checkers inherit from `BaseChecker` and implement required interface
**When to use:** For all new checkers (established pattern from Phases 16-19)

**Example:**
```python
# Source: tools/script-checkers/checkers/stumble.py (lines 15-45)
from checkers import BaseChecker

class PacingChecker(BaseChecker):
    """Detect script pacing and complexity issues"""

    def __init__(self, config):
        super().__init__(config)
        self._nlp = None  # Lazy load spaCy

    @property
    def name(self) -> str:
        return "pacing"

    @property
    def nlp(self):
        """Lazy-load spaCy model to avoid import overhead"""
        if self._nlp is None:
            try:
                import spacy
                self._nlp = spacy.load("en_core_web_sm")
            except OSError:
                raise RuntimeError(
                    "spaCy model 'en_core_web_sm' not found. "
                    "Install with: python -m spacy download en_core_web_sm"
                )
        return self._nlp

    def check(self, text: str) -> Dict[str, Any]:
        """
        Analyze text for pacing issues.

        Returns:
            {
                'issues': [
                    {
                        'section': 'Section Name',
                        'score': 75,  # 0-100
                        'metrics': {
                            'sentence_variance': 18.2,
                            'flesch_score': 45.3,
                            'flesch_delta': -25.0,
                            'entity_density': 0.48
                        },
                        'reasons': [
                            'high sentence variance (18.2) — inconsistent pacing',
                            'flesch drop of 25 points — sudden complexity spike',
                            'entity density (0.48) — too many proper nouns'
                        ]
                    }
                ],
                'stats': {
                    'total_sections': 8,
                    'flagged_sections': 2,
                    'energy_arc': '▇▅▃▆█▄▂▃',
                    'flat_zones': 1,
                    'verdict': 'NEEDS WORK'
                }
            }
        """
```

### Pattern 2: Section-Level Analysis with Production Parser

**What:** Reuse `tools/production/parser.py` for consistent section detection
**When to use:** Any analysis that needs to understand script structure

**Example:**
```python
# Source: tools/production/parser.py (lines 162-180)
from tools.production.parser import ScriptParser

def check(self, text: str) -> Dict[str, Any]:
    parser = ScriptParser()
    sections = parser.parse_text(text)  # Returns List[Section]

    issues = []
    section_scores = []

    for section in sections:
        # Section object has:
        # - heading: str
        # - content: str (raw markdown)
        # - word_count: int (spoken words only)
        # - section_type: 'intro' | 'body' | 'conclusion'

        metrics = self._analyze_section(section.content)
        score = self._calculate_score(metrics)
        section_scores.append(score)

        if score < self.config.pacing_pass_threshold:
            issues.append({
                'section': section.heading,
                'score': score,
                'metrics': metrics,
                'reasons': self._explain_issues(metrics)
            })
```

### Pattern 3: Lazy-Loaded Dependencies

**What:** Import heavy libraries (textstat, spaCy) only when check() is called
**When to use:** Avoids startup overhead when checker not used

**Example:**
```python
# Don't do this (slows all CLI invocations):
import textstat  # At module level

# Do this (only loads when --pacing used):
def _calculate_flesch(self, text: str) -> float:
    import textstat  # Lazy import
    return textstat.flesch_reading_ease(text)
```

### Pattern 4: Problems-Only Default Output

**What:** Default output skips clean sections, verbose mode shows all
**When to use:** User wants actionable feedback, not congratulations

**Example:**
```python
def format_output(self, issues, stats, verbose=False):
    output = []

    if verbose:
        # Show ALL sections with metrics
        for section, metrics in all_sections:
            output.append(f"## {section.heading}")
            output.append(f"Score: {metrics['score']}/100")
            # ... all metrics
    else:
        # Show ONLY flagged sections
        if not issues:
            output.append("✅ No pacing issues detected")
        else:
            output.append(f"⚠️ {len(issues)} sections need attention:")
            for issue in issues:
                output.append(f"\n## {issue['section']} (Score: {issue['score']}/100)")
                for reason in issue['reasons']:
                    output.append(f"  - {reason}")
```

### Anti-Patterns to Avoid

- **Don't score section length:** User decision clearly states "length is a style choice" — only flag internal complexity, not duration
- **Don't provide fix suggestions:** User wants root cause explanations, not prescriptive rewrites
- **Don't use severity labels (WARNING/CRITICAL):** User wants numeric scores (0-100) only
- **Don't analyze without sections:** Parser is mandatory for consistent structure detection

---

## Don't Hand-Roll

Problems that look simple but have existing solutions:

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Flesch Reading Ease | Custom formula with syllable counting | `textstat.flesch_reading_ease()` | Handles edge cases (abbreviations, compound words, non-ASCII) |
| Sentence variance | Manual mean calculation loop | `statistics.stdev(sentence_lengths)` | Handles empty lists, provides population vs sample stdev |
| Entity detection | Regex for capitalized words | spaCy NER with POS tagging | Distinguishes proper nouns from sentence-initial caps, acronyms |
| Sparkline generation | Custom Unicode mapping | Simple `map_to_blocks()` function with 8 chars | No library needed, 10 lines of code |
| Section parsing | Regex for markdown headers | `ScriptParser.parse_text()` | Consistent with production tools, handles frontmatter/comments |

**Key insight:** Readability research has decades of edge-case handling. Don't reinvent syllable counting, sentence boundary detection, or readability formulas.

---

## Common Pitfalls

### Pitfall 1: False-Flagging Academic Writing as "Too Complex"

**What goes wrong:** User's channel uses proper nouns heavily (historical figures, treaties, places). A simple entity density check flags legitimate academic terminology as "wall of nouns."

**Why it happens:** Generic thresholds (entity density >0.4) don't account for domain-specific vocabulary requirements.

**How to avoid:**
- Use thresholds as warnings, not errors
- Provide context in explanation: "High entity density (0.48) — many proper nouns in sequence. This may be intentional for historical accuracy."
- Don't penalize proper citation style

**Warning signs:** Every section with academic quotes gets flagged.

### Pitfall 2: Flesch Score Misinterpretation

**What goes wrong:** Flesch Reading Ease is designed for general audience content. Academic/technical content naturally scores lower (30-50 range). Flagging "low Flesch score" makes no sense for this channel.

**Why it happens:** Flesch formula penalizes long words and sentences, which are common in precise historical writing.

**How to avoid:**
- Focus on **Flesch delta** (change between sections), not absolute score
- Flag sudden drops (>20 points), not low scores
- User decision specifies "Flesch delta >20" not "Flesch score <60"

**Warning signs:** All sections flagged despite consistent complexity.

### Pitfall 3: Not Handling Headerless Scripts

**What goes wrong:** Some scripts may lack H2 headers (single-section scripts). Parser returns single "Untitled" section. Pacing analysis needs to handle this gracefully.

**Why it happens:** Assuming all scripts have multi-section structure.

**How to avoid:**
```python
sections = parser.parse_text(text)
if len(sections) == 1:
    # Single section — can't calculate Flesch delta or energy arc
    return {
        'issues': [],
        'stats': {
            'verdict': 'SKIPPED',
            'reason': 'Single-section script (no structure to analyze)'
        }
    }
```

**Warning signs:** Division by zero, index errors on single-section scripts.

### Pitfall 4: Ignoring B-Roll Markers in Word Count

**What goes wrong:** ScriptParser already strips B-roll markers (`[B-ROLL: ...]`, `[MAP: ...]`) from word counts. If you re-parse with different logic, counts won't match production tools.

**Why it happens:** Implementing custom content extraction instead of using parser's `section.content`.

**How to avoid:** Always use `ScriptParser` for content extraction. Don't write custom markdown strippers.

**Warning signs:** Word counts differ from production tools, entity density calculated on markers.

### Pitfall 5: Sparkline Scaling Edge Cases

**What goes wrong:** If all sections have identical scores (e.g., all 50/100), sparkline shows flat line. If one section is 100 and rest are 0, sparkline loses nuance.

**Why it happens:** Simple min-max scaling without handling edge cases.

**How to avoid:**
```python
def generate_sparkline(scores: List[float]) -> str:
    if not scores:
        return ""
    if len(set(scores)) == 1:  # All identical
        return "▄" * len(scores)  # Mid-level bar

    min_score = min(scores)
    max_score = max(scores)
    blocks = "▁▂▃▄▅▆▇█"

    # Normalize to 0-7 range
    normalized = [
        int((s - min_score) / (max_score - min_score) * 7)
        for s in scores
    ]
    return "".join(blocks[n] for n in normalized)
```

**Warning signs:** Empty sparklines, all same character.

---

## Code Examples

Verified patterns from official sources and existing codebase:

### Flesch Reading Ease Calculation

```python
# Source: textstat library (https://textstat.org/)
import textstat

def calculate_flesch(text: str) -> float:
    """
    Calculate Flesch Reading Ease score.

    Formula: 206.835 - 1.015 × (words/sentences) - 84.6 × (syllables/words)

    Score interpretation:
    - 90-100: Very easy (5th grade)
    - 60-70: Plain English (8th-9th grade)
    - 30-50: College level
    - 0-30: Very difficult (college graduate)

    Returns:
        Float score (higher = easier to read)
    """
    return textstat.flesch_reading_ease(text)

# Example usage
text = "This is a simple sentence. This is another one."
score = calculate_flesch(text)  # Returns ~90 (very easy)
```

### Sentence Length Variance

```python
# Source: Python statistics module (https://docs.python.org/3/library/statistics.html)
import statistics

def calculate_sentence_variance(text: str, nlp) -> float:
    """
    Calculate standard deviation of sentence lengths.

    Threshold (user decision): variance > 15 words = inconsistent pacing

    Args:
        text: Script text
        nlp: spaCy model instance

    Returns:
        Standard deviation of sentence word counts
    """
    doc = nlp(text)
    sentence_lengths = []

    for sent in doc.sents:
        # Count words (exclude punctuation/spaces)
        words = [t for t in sent if not t.is_punct and not t.is_space]
        sentence_lengths.append(len(words))

    if len(sentence_lengths) < 2:
        return 0.0  # Need at least 2 sentences

    return statistics.stdev(sentence_lengths)

# Example
variance = calculate_sentence_variance(section_text, nlp)
if variance > 15:
    issue = f"high sentence variance ({variance:.1f}) — inconsistent pacing"
```

### Entity Density Detection

```python
# Source: spaCy NER (https://spacy.io/usage/linguistic-features)
def calculate_entity_density(text: str, nlp) -> float:
    """
    Calculate ratio of proper nouns to total words.

    Threshold (user decision): density > 0.4 (40%) = wall of proper nouns

    Uses spaCy POS tagging to identify PROPN (proper nouns).
    More accurate than simple capitalization check.

    Returns:
        Float ratio (0.0 to 1.0)
    """
    doc = nlp(text)

    # Count proper nouns (PROPN tag)
    proper_nouns = [token for token in doc if token.pos_ == "PROPN"]

    # Count total words (exclude punctuation/spaces)
    total_words = [token for token in doc if not token.is_punct and not token.is_space]

    if len(total_words) == 0:
        return 0.0

    return len(proper_nouns) / len(total_words)

# Example
density = calculate_entity_density(section_text, nlp)
if density > 0.4:
    issue = f"entity density ({density:.2f}) — too many proper nouns"
```

### Sparkline Generation

```python
# Source: Unicode block characters standard
def generate_sparkline(scores: List[float]) -> str:
    """
    Generate ASCII sparkline from section scores.

    Uses Unicode block characters: ▁▂▃▄▅▆▇█

    Args:
        scores: List of section scores (0-100)

    Returns:
        Sparkline string (one char per section)
    """
    if not scores:
        return ""

    # Handle edge case: all scores identical
    if len(set(scores)) == 1:
        return "▄" * len(scores)  # Mid-level

    min_score = min(scores)
    max_score = max(scores)
    blocks = "▁▂▃▄▅▆▇█"

    # Map scores to 0-7 index range
    normalized = []
    for score in scores:
        # Normalize to 0-1, then scale to 0-7
        ratio = (score - min_score) / (max_score - min_score)
        index = min(int(ratio * 7), 7)  # Clamp to 0-7
        normalized.append(index)

    return "".join(blocks[n] for n in normalized)

# Example
scores = [60, 75, 50, 80, 45, 70, 65]
arc = generate_sparkline(scores)  # Returns: "▃▆▂▇▁▅▄"
```

### Pattern Interrupt Detection (Keyword Heuristic)

```python
# Source: User requirements (CONTEXT.md)
import re

def detect_modern_hooks(text: str) -> List[int]:
    """
    Detect modern relevance hooks using keyword + B-roll marker heuristic.

    User decision: Advisory only, not scored.

    Keywords: today, 2024, 2025, 2026, still, currently, now
    B-roll markers: [NEWS CLIP], [MODERN MAP], [CURRENT]

    Returns:
        List of character positions where hooks appear
    """
    # Time markers
    time_markers = r'\b(today|2024|2025|2026|still|currently|now)\b'

    # B-roll markers (case-insensitive)
    broll_markers = r'\[(NEWS|MODERN|CURRENT)[^\]]*\]'

    hooks = []

    # Find all matches
    for match in re.finditer(time_markers, text, re.IGNORECASE):
        hooks.append(match.start())

    for match in re.finditer(broll_markers, text, re.IGNORECASE):
        hooks.append(match.start())

    return sorted(hooks)

# Check for gaps > 150 words (user guideline: hook every 90 seconds)
# At 150 WPM speaking rate, 150 words ≈ 60 seconds
def check_hook_gaps(text: str) -> List[str]:
    """Advisory: Flag long stretches without modern hooks"""
    hooks = detect_modern_hooks(text)
    words = text.split()

    if len(hooks) == 0:
        return ["No modern relevance hooks detected"]

    # Calculate word gaps between hooks
    # (Simplified - production version needs word position mapping)
    advisories = []
    if len(hooks) < len(words) / 150:
        advisories.append("Consider adding modern hooks every ~90 seconds")

    return advisories
```

### Flat Zone Detection

```python
def detect_flat_zones(scores: List[float], threshold: int = 3) -> List[str]:
    """
    Detect monotone stretches in energy arc.

    User decision: 3+ consecutive sections with similar scores = flag

    Args:
        scores: Section scores (0-100)
        threshold: Consecutive sections to trigger warning

    Returns:
        List of warnings
    """
    if len(scores) < threshold:
        return []

    warnings = []
    flat_start = None

    for i in range(len(scores) - 1):
        # Similar = within 10 points
        if abs(scores[i] - scores[i + 1]) < 10:
            if flat_start is None:
                flat_start = i
        else:
            # End of flat zone
            if flat_start is not None:
                flat_length = i - flat_start + 1
                if flat_length >= threshold:
                    warnings.append(
                        f"Energy plateau detected: sections {flat_start + 1}-{i + 1} "
                        f"have similar complexity. Consider pattern interrupt."
                    )
                flat_start = None

    # Check final zone
    if flat_start is not None:
        flat_length = len(scores) - flat_start
        if flat_length >= threshold:
            warnings.append(
                f"Energy plateau detected: sections {flat_start + 1}-{len(scores)} "
                f"have similar complexity. Consider pattern interrupt."
            )

    return warnings
```

---

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Manual readability testing | Automated textstat metrics | 2010s | Instant feedback vs hours of testing |
| Absolute Flesch scores | Flesch delta between sections | 2020s | Context-aware complexity changes |
| Word count only | Multi-metric scoring (variance + Flesch + entities) | 2025 | Holistic pacing view |
| Severity labels (WARNING/ERROR) | Numeric scores (0-100) | This project (Phase 28) | Clear go/no-go thresholds |

**Deprecated/outdated:**
- Gunning Fog Index: Less reliable than Flesch for spoken content
- Manual syllable counting: textstat handles edge cases
- Regex-based entity detection: spaCy NER far more accurate

---

## Open Questions

Things that couldn't be fully resolved:

1. **Exact PASS/NEEDS WORK/FAIL thresholds**
   - What we know: User wants score-based verdicts (0-100 scale)
   - What's unclear: Exact cutoffs (e.g., <60 = FAIL, 60-80 = NEEDS WORK, >80 = PASS)
   - Recommendation: Start with 50/75 thresholds, tune after user testing. Mark as Claude's discretion.

2. **Ideal arc comparison value**
   - What we know: User wants flat zone detection
   - What's unclear: Whether showing "ideal arc" (e.g., "▃▅▇▇▅▃" pyramid) adds value
   - Recommendation: Skip for MVP. Add if user requests after seeing basic arc visualization.

3. **Hook severity weighting**
   - What we know: Hook detection is advisory only, not scored
   - What's unclear: Should missing hooks reduce overall score slightly, or remain fully separate?
   - Recommendation: Keep fully separate (advisory section). User decision says "advisory only."

4. **Configuration approach**
   - What we know: Thresholds need to be stored (variance >15, Flesch delta >20, entity density >0.4)
   - What's unclear: Config file, hardcoded in config.py, or CLI flags?
   - Recommendation: Add to `config.py` following existing pattern (see `scaffolding_base_rate`, `stumble_max_words`). Matches project architecture.

---

## Sources

### Primary (HIGH confidence)
- [Python statistics module documentation](https://docs.python.org/3/library/statistics.html) - stdev() implementation
- [textstat PyPI](https://pypi.org/project/textstat/) - Flesch Reading Ease calculation
- [textstat documentation](https://textstat.org/) - Readability metrics API
- [spaCy NER documentation](https://spacy.io/usage/linguistic-features) - Entity recognition and POS tagging
- [spaCy API EntityRecognizer](https://spacy.io/api/entityrecognizer) - Named entity recognition component
- Existing codebase:
  - `tools/script-checkers/checkers/stumble.py` - BaseChecker pattern
  - `tools/script-checkers/checkers/flow.py` - spaCy integration pattern
  - `tools/script-checkers/config.py` - Threshold configuration pattern
  - `tools/production/parser.py` - Section parsing implementation

### Secondary (MEDIUM confidence)
- [Flesch Reading Ease formula guide (Readable)](https://readable.com/readability/flesch-reading-ease-flesch-kincaid-grade-level/) - Formula explanation and interpretation
- [Flesch-Kincaid Wikipedia](https://en.wikipedia.org/wiki/Flesch%E2%80%93Kincaid_readability_tests) - Historical context and formula
- [Sentence length variance research (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC9955962/) - Just Noticeable Difference thresholds (1.5-1.6 words)
- [Sentence length and pacing (Virtual Writing Tutor)](https://blog.virtualwritingtutor.com/sentence-length-and-variance/) - Variance impact on readability
- [Pattern interrupt retention research (Diana Briceno)](https://www.dianabriceno.com/pattern-interrupt-for-viewer-retention/) - 30-second recommendation
- [Pattern interrupt techniques (LightningIM)](https://lightningim.com/digital-tools/12-powerful-pattern-interrupt-video-editing-techniques-that-boost-engagement/) - 3-5 second intervals for retention
- [YouTube retention strategies (AIR Media-Tech)](https://air.io/en/youtube-hacks/advanced-retention-editing-cutting-patterns-that-keep-viewers-past-minute-8) - Editing patterns for 8+ minute videos

### Tertiary (LOW confidence)
- Generic readability advice (various blogs) - Not domain-specific to script analysis

---

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - textstat and spaCy are industry-standard, verified from official docs
- Architecture: HIGH - Existing checker pattern well-established in codebase
- Thresholds: MEDIUM - Generic research-based defaults, not calibrated to user's corpus
- Pitfalls: HIGH - Derived from existing checker implementations and user constraints

**Research date:** 2026-02-06
**Valid until:** 90 days (stable domain - readability formulas don't change rapidly)
