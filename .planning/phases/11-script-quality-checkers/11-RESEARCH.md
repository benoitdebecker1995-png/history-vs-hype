# Phase 11: Script Quality Checkers - Research

**Researched:** 2026-01-28
**Domain:** Text analysis, NLP readability metrics, spoken delivery optimization
**Confidence:** HIGH

## Summary

Script quality checking for spoken delivery is a well-established domain with mature Python libraries. The standard approach combines readability metrics (Flesch-Kincaid, sentence length), NLP text analysis (spaCy for parsing), and pattern matching (regex for repetition). The channel's specific requirements (teleprompter delivery, educational content, rhetorical patterns) align well with existing text analysis capabilities.

Research reveals teleprompter readability has specific thresholds: sentences over 25-30 words cause stumbles, complex subordinate clauses create awkward pauses, and unnatural phrasing disrupts delivery flow. Educational scriptwriting best practices emphasize conversational tone, term definitions before use, and controlled repetition for emphasis (not redundancy).

The existing repository infrastructure (Python tools in `tools/`, JSON output, CLI interfaces) provides a clear architectural pattern. Script checkers should follow the same structure as `tools/youtube-analytics/` with standalone CLI tools that can be invoked by Claude.

**Primary recommendation:** Use spaCy for sentence parsing + textstat for readability metrics + custom pattern matching for channel-specific rules. Output annotated markdown with inline flags and summary report.

## Standard Stack

The established libraries/tools for text analysis and readability:

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| spaCy | 3.8+ (2025) | NLP parsing, sentence structure analysis | Industry standard for production NLP, actively maintained, fast C-level performance |
| textstat | Latest (2026) | Readability formulas (Flesch-Kincaid, etc.) | Most comprehensive Python library for readability metrics, supports 15+ formulas |
| en_core_web_sm | 3.8+ | English language model for spaCy | Lightweight model (13MB), sufficient for script analysis |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| py-readability-metrics | 1.4.4+ | Alternative readability library | If textstat missing specific formula |
| difflib | stdlib | Near-duplicate detection | For repetition matching (exact + fuzzy) |
| re (regex) | stdlib | Pattern matching | For channel-specific phrases ("Here's", scaffolding) |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| spaCy | NLTK | NLTK is older, slower, less accurate. spaCy is modern standard. |
| textstat | py-readability-metrics | Both work, but textstat has cleaner API and more formulas. |
| Custom repetition | TextRank/RAKE | Overkill for phrase counting. Simple difflib + regex sufficient. |

**Installation:**
```bash
pip install spacy textstat
python -m spacy download en_core_web_sm
```

## Architecture Patterns

### Recommended Project Structure
```
tools/
├── script-checkers/
│   ├── checkers/           # Individual checker modules
│   │   ├── __init__.py
│   │   ├── repetition.py   # SCRIPT-01: Repetition detection
│   │   ├── flow.py         # SCRIPT-02: Flow analyzer
│   │   ├── stumble.py      # SCRIPT-03: Teleprompter stumble test
│   │   └── scaffolding.py  # SCRIPT-04: Scaffolding counter
│   ├── cli.py              # Main CLI interface
│   ├── config.py           # Thresholds and configuration
│   ├── output.py           # Formatters (markdown, JSON)
│   └── requirements.txt
```

### Pattern 1: Modular Checker Classes
**What:** Each checker is an independent class with standard interface
**When to use:** Allows running checkers individually or combined
**Example:**
```python
# Source: Standard Python design patterns
class BaseChecker:
    def __init__(self, config):
        self.config = config

    def check(self, text: str) -> dict:
        """Returns {issues: [], stats: {}}"""
        raise NotImplementedError

    def format_inline(self, text: str, issues: list) -> str:
        """Returns text with inline annotations"""
        raise NotImplementedError

class RepetitionChecker(BaseChecker):
    def check(self, text: str) -> dict:
        # Find repeated phrases
        return {
            'issues': [
                {'line': 15, 'phrase': 'Here's what', 'count': 7, 'severity': 'warning'}
            ],
            'stats': {'total_phrases': 150, 'repeated': 12}
        }
```

### Pattern 2: Pipeline Architecture (Run All or Selective)
**What:** Main CLI orchestrates checkers based on flags
**When to use:** User control over which checks to run
**Example:**
```python
# Source: Based on tools/youtube-analytics/analyze.py pattern
def run_all_checks(script_path, config):
    results = {}

    if config.check_repetition:
        results['repetition'] = RepetitionChecker(config).check(script)
    if config.check_flow:
        results['flow'] = FlowChecker(config).check(script)
    if config.check_stumble:
        results['stumble'] = StumbleChecker(config).check(script)
    if config.check_scaffolding:
        results['scaffolding'] = ScaffoldingChecker(config).check(script)

    return results
```

### Pattern 3: Output Formats (Inline + Summary)
**What:** Generate both annotated script and summary report
**When to use:** Users want to see issues in context AND overview
**Example:**
```python
# Source: Standard practice in code linters (pylint, flake8)
def format_output(script, results, format='markdown'):
    if format == 'markdown':
        output = "# Script Quality Report\n\n"

        # Summary section
        output += "## Summary\n"
        for checker, data in results.items():
            output += f"- **{checker}**: {len(data['issues'])} issues\n"

        # Annotated script
        output += "\n## Annotated Script\n\n"
        output += add_inline_annotations(script, results)

        return output
```

### Pattern 4: Proportional Thresholds (Scale with Script Length)
**What:** Thresholds adjust based on video/script length
**When to use:** User requirement from CONTEXT.md
**Example:**
```python
# Source: Context requirement + teleprompter best practices
def calculate_threshold(script_length: int, base_threshold: float, scaling_factor: float = 1.0):
    """
    For scaffolding: base = 0.003 (3 per 1000 words)
    8-minute script (~1200 words) = 3.6 "Here's" allowed
    20-minute script (~3000 words) = 9 "Here's" allowed
    """
    return int(script_length * base_threshold * scaling_factor)
```

### Anti-Patterns to Avoid
- **Hard-coded thresholds:** Use config.py for all limits, don't embed magic numbers in checker code
- **Single output format:** Support both markdown and JSON, users have different needs
- **Ignoring context:** "Here's what the treaty says" (document reveal) vs "Here's another point" (filler) - need pattern awareness
- **Over-engineering:** Don't build ML-based semantic analysis when regex + NLP parsing suffices
- **Blocking script generation:** Checkers are advisory, not blockers. Present issues, don't prevent output.

## Don't Hand-Roll

Problems that look simple but have existing solutions:

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Readability formulas | Custom syllable counter + sentence parser | textstat library | Implements 15+ validated formulas (Flesch-Kincaid, Gunning Fog, SMOG), handles edge cases |
| Sentence boundary detection | Regex on periods | spaCy sentence segmentation | Handles abbreviations (U.S., Dr.), quotes, edge cases correctly |
| Part-of-speech tagging | Custom grammar rules | spaCy POS tagger | Pre-trained model, 95%+ accuracy, handles context |
| Near-duplicate detection | Custom string distance | difflib.SequenceMatcher | Optimized C implementation, handles fuzzy matching |
| Dependency parsing | Custom syntax trees | spaCy dependency parser | Identifies subordinate clauses, nested structures for stumble detection |

**Key insight:** Text analysis has 40+ years of NLP research. Mature libraries exist for every common task. Custom solutions will be slower, less accurate, and miss edge cases. Use established tools.

## Common Pitfalls

### Pitfall 1: Treating All Repetition as Bad
**What goes wrong:** Flagging rhetorical repetition (intentional emphasis) as errors
**Why it happens:** Simple phrase counting doesn't understand context
**How to avoid:**
- Pattern allowlists for rhetorical structures: "Not X. Not Y. Z." (fragment emphasis)
- Proximity rules: Repetition within 2 sentences = potential rhetorical device
- Manual review layer: Checkers flag, user decides if intentional
**Warning signs:** High false positive rate on well-written scripts

### Pitfall 2: Ignoring Sentence Context for Stumble Detection
**What goes wrong:** Flagging long sentences that are actually easy to speak
**Why it happens:** Word count alone doesn't capture syntactic complexity
**How to avoid:**
- Use dependency parsing to identify nested clauses
- Long sentence with simple structure (list) = OK
- Short sentence with nested subordinates = stumble risk
- Example OK: "Britain controlled India, Egypt, Cyprus, Malta, and Sudan." (26 words, one clause)
- Example BAD: "Britain, which had controlled India since 1858, despite local resistance, decided..." (14 words, 2 nested clauses)
**Warning signs:** Users ignore length warnings because they're inaccurate

### Pitfall 3: Rigid Thresholds Across All Content
**What goes wrong:** 8-minute video flagged for 4 "Here's", 30-minute video passes with 4
**Why it happens:** Absolute limits don't scale with content length
**How to avoid:**
- Calculate per-1000-words rate
- STYLE-GUIDE.md says 2-4 per script, but that's for 8-12 minute videos (~1200-1800 words)
- Derive rate: 2.5 per 1500 words = 0.0017 per word = 1.7 per 1000 words
- Scale linearly for longer/shorter scripts
**Warning signs:** Users complain threshold doesn't match their script length

### Pitfall 4: Term Definition Detection Brittleness
**What goes wrong:** Checker misses terms used before definition or false-positives common words
**Why it happens:** Simple noun extraction treats all nouns as "technical terms"
**How to avoid:**
- Capitalized multi-word phrases likely proper nouns (people, places)
- Domain-specific vocabulary lists (geopolitics, history terms)
- Pattern: "X - [definition]" or "X, which is [definition]"
- Accept that 100% accuracy is impossible, aim for high-confidence flagging only
**Warning signs:** Flagging common words like "treaty" or "border" as undefined terms

### Pitfall 5: Not Matching STYLE-GUIDE Voice
**What goes wrong:** Checker flags patterns that are actually channel style
**Why it happens:** Generic scriptwriting rules differ from this channel's voice
**How to avoid:**
- Read STYLE-GUIDE.md thoroughly before setting rules
- Fragments for emphasis = ALLOWED ("Not a promise. Independence.")
- Casual asides = ALLOWED (1-2 per script)
- "Here's what X actually says" = SIGNATURE PHRASE, not filler
- Pattern allowlist for approved phrases
**Warning signs:** User overrides most warnings

### Pitfall 6: Performance on Long Scripts
**What goes wrong:** Analysis takes 10+ seconds on 30-minute script (5000+ words)
**Why it happens:** spaCy parsing is fast but not instant, repeated passes slow down
**How to avoid:**
- Parse once with spaCy, share parsed doc across checkers
- Cache intermediate results (sentence list, noun phrases)
- Use en_core_web_sm (13MB) not en_core_web_lg (560MB) - sufficient for script analysis
**Warning signs:** User frustration with slow tool

## Code Examples

Verified patterns from official sources:

### Readability Analysis with textstat
```python
# Source: https://pypi.org/project/textstat/
import textstat

def analyze_readability(text: str) -> dict:
    """Calculate multiple readability scores"""
    return {
        'flesch_reading_ease': textstat.flesch_reading_ease(text),
        'flesch_kincaid_grade': textstat.flesch_kincaid_grade(text),
        'avg_sentence_length': textstat.avg_sentence_length(text),
        'difficult_words': textstat.difficult_words(text),
        'syllable_count': textstat.syllable_count(text)
    }

# Flesch Reading Ease interpretation:
# 90-100: Very Easy (5th grade)
# 60-70: Standard (8th-9th grade)
# 30-50: Difficult (college)
# 0-30: Very Difficult (college graduate)
# Target for YouTube: 60-70
```

### Sentence Complexity with spaCy
```python
# Source: https://spacy.io/usage/linguistic-features
import spacy

nlp = spacy.load("en_core_web_sm")

def find_complex_sentences(text: str, max_words: int = 25) -> list:
    """Identify sentences with stumble risk"""
    doc = nlp(text)
    complex_sentences = []

    for sent in doc.sents:
        word_count = len([t for t in sent if not t.is_punct])

        # Count subordinate clauses (advcl, acl, relcl)
        sub_clauses = len([t for t in sent if t.dep_ in ('advcl', 'acl', 'relcl')])

        if word_count > max_words or sub_clauses >= 2:
            complex_sentences.append({
                'text': sent.text,
                'word_count': word_count,
                'sub_clauses': sub_clauses,
                'severity': 'high' if word_count > 30 else 'medium'
            })

    return complex_sentences
```

### Repetition Detection with difflib
```python
# Source: https://docs.python.org/3/library/difflib.html
from difflib import SequenceMatcher
import re

def find_repeated_phrases(text: str, min_length: int = 3, threshold: float = 0.8) -> list:
    """Find exact and near-duplicate phrases"""
    # Extract phrases (3+ words)
    sentences = re.split(r'[.!?]+', text)
    phrases = []

    for sent in sentences:
        words = sent.strip().split()
        for i in range(len(words) - min_length + 1):
            phrase = ' '.join(words[i:i+min_length])
            phrases.append(phrase.lower())

    # Find duplicates
    repetitions = {}
    for i, phrase1 in enumerate(phrases):
        for j, phrase2 in enumerate(phrases[i+1:], start=i+1):
            similarity = SequenceMatcher(None, phrase1, phrase2).ratio()
            if similarity >= threshold:
                key = phrase1 if len(phrase1) <= len(phrase2) else phrase2
                repetitions[key] = repetitions.get(key, 1) + 1

    return [{'phrase': k, 'count': v} for k, v in repetitions.items() if v > 2]
```

### Scaffolding Counter with Regex
```python
# Source: Custom, based on STYLE-GUIDE.md requirements
import re

def count_scaffolding(text: str, script_length: int) -> dict:
    """Count scaffolding phrases and check against threshold"""

    patterns = {
        "here's": r"\bhere'?s\b",
        "now": r"\bnow\b",  # Filter: sentence-initial only
        "so": r"\bso\b",    # Filter: sentence-initial only
    }

    counts = {}
    instances = {}

    for name, pattern in patterns.items():
        matches = re.finditer(pattern, text, re.IGNORECASE)
        instances[name] = [m.start() for m in matches]
        counts[name] = len(instances[name])

    # Calculate threshold (2-4 for ~1500 words = 0.002 per word)
    words = len(text.split())
    base_rate = 0.002
    threshold = int(words * base_rate)

    return {
        'counts': counts,
        'threshold': threshold,
        'exceeded': counts['here\'s'] > threshold * 2,  # 2x threshold = warning
        'severity': 'high' if counts['here\'s'] > threshold * 3 else 'medium'
    }
```

### Term Definition Detection
```python
# Source: Custom NLP pattern, based on spaCy
def find_undefined_terms(text: str) -> list:
    """Detect technical terms used before definition"""
    doc = nlp(text)

    # Extract proper nouns and capitalized phrases (potential terms)
    terms = []
    for chunk in doc.noun_chunks:
        # Capitalized multi-word = potential term
        if chunk.text[0].isupper() and len(chunk.text.split()) > 1:
            terms.append({
                'term': chunk.text,
                'first_position': chunk.start_char,
                'has_definition': check_for_definition(chunk, doc)
            })

    undefined = [t for t in terms if not t['has_definition']]
    return undefined

def check_for_definition(chunk, doc) -> bool:
    """Check if term followed by definition pattern"""
    # Pattern: "X - [definition]" or "X, which is [definition]"
    next_tokens = doc[chunk.end:chunk.end+10]

    for token in next_tokens:
        if token.text in ('-', '—') or token.lemma_ == 'be':
            return True
    return False
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Manual script review | AI-assisted quality checking | 2023-2024 | Tools like Descript, BIGVU added AI script optimization |
| Single readability metric | Multiple formula consensus | Ongoing | textstat provides 15+ metrics, no single formula is "correct" |
| Word-count-only limits | Syntax-aware complexity | 2020s | spaCy dependency parsing detects actual stumble risks |
| Hard-coded thresholds | Adaptive/proportional limits | User requirement | Scales with script length, reduces false positives |

**Deprecated/outdated:**
- NLTK for production NLP: spaCy has replaced it as standard (faster, more accurate)
- Flesch-Kincaid alone: Use multiple metrics for consensus
- Manual syllable counting: textstat handles edge cases better than custom code

## Open Questions

1. **Rhetorical Repetition Detection Accuracy**
   - What we know: Can use proximity rules (repetition within 2 sentences) as heuristic
   - What's unclear: How to distinguish ALL rhetorical patterns from redundancy automatically
   - Recommendation: Start with simple proximity rules + manual allowlist. Accept 80% accuracy, user reviews flags.

2. **Domain-Specific Term Lists**
   - What we know: History/geopolitics has specialized vocabulary (estoppel, Basij, bonyads)
   - What's unclear: Should we maintain a curated term list or use generic capitalization heuristic?
   - Recommendation: Start with capitalization heuristic. If false positives high, add manual term list in config.

3. **Integration with Script Generation**
   - What we know: User wants automatic execution when /script generates output
   - What's unclear: How tightly to couple checkers with scriptwriting agent
   - Recommendation: Keep checkers as standalone tools. Scriptwriting agent calls CLI after generation. Loose coupling allows independent use.

4. **CTR/Retention Integration**
   - What we know: Phase 12 (Voice Fingerprinting) will learn from user patterns
   - What's unclear: Data format for lessons learned ("user accepts 5 'Here's' in 20-min videos")
   - Recommendation: Output checker results to JSON. Phase 12 can analyze historical accepts/rejects to update thresholds.

## Sources

### Primary (HIGH confidence)
- [spaCy Official Documentation](https://spacy.io/) - NLP library capabilities
- [textstat PyPI](https://pypi.org/project/textstat/) - Readability metrics
- [py-readability-metrics Documentation](https://py-readability-metrics.readthedocs.io/) - Alternative readability library
- [Python difflib Documentation](https://docs.python.org/3/library/difflib.html) - Sequence matching
- [Readability Guidelines](http://readabilityguidelines.wikidot.com/sentence-length) - Sentence length thresholds (25-30 words)
- [Teleprompter.com Tools](https://www.teleprompter.com/tools/script-timer) - Teleprompter readability analysis

### Secondary (MEDIUM confidence)
- [YouTube Scriptwriting Best Practices (VidIQ, 2026)](https://vidiq.com/blog/post/write-youtube-video-script/) - Educational content structure
- [Educational Video Scriptwriting (Teachers Institute)](https://teachers.institute/designing-courseware/scriptwriting-educational-videos-masterclass/) - Pedagogical patterns
- [Rhetorical Repetition Analysis](https://polgovpro.blog/2024/07/25/rhetorical-repetition-reiteration-and-redundancy/) - Distinguishing rhetorical vs redundant repetition
- [NLP Text Repetition Detection Research (Apple ML, 2025)](https://machinelearning.apple.com/research/analyzing-mitigating-repetitions) - Neural text generation repetition analysis

### Tertiary (LOW confidence)
- WebSearch results on AI scriptwriting tools (multiple sources) - General landscape, not specific implementation guidance

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - spaCy and textstat are industry standards, well-documented, actively maintained
- Architecture: HIGH - Python CLI patterns verified from existing tools/ directory
- Readability thresholds: HIGH - 25-30 word sentence limits verified across multiple sources
- Repetition detection: MEDIUM - Rhetorical vs redundant distinction requires judgment, not fully automatable
- Term definition detection: MEDIUM - NLP patterns can identify candidates, but false positives likely
- Integration patterns: HIGH - CLI-based tool invocation matches existing repository patterns

**Research date:** 2026-01-28
**Valid until:** 90 days (April 2026) - NLP libraries stable, teleprompter best practices unlikely to change
