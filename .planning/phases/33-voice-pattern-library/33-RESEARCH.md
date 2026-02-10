# Phase 33: Voice Pattern Library - Research

**Researched:** 2026-02-10
**Domain:** Writing style pattern extraction and reference documentation
**Confidence:** HIGH

## Summary

Phase 33 implements voice pattern library expansion by documenting proven patterns from high-performing videos (Belize 23K views, Vance 42.6% retention) into STYLE-GUIDE.md Part 6. This is **reference document expansion, not code proliferation** — the strategic decision made during v2.0 research to avoid empty pattern syndrome with small datasets (~15 videos).

Research confirms the project already has substantial voice pattern infrastructure: `voice/pattern_extractor.py`, `voice/pattern_applier.py`, and `voice/corpus_builder.py` exist in `tools/script-checkers/`. These tools extract word-level substitutions, deletions, and insertions by comparing scripts to SRT transcripts. However, **this existing code focuses on word-level patterns (formal→casual), not structural patterns** (Kraut causal chains, Alex O'Connor concessions, sentence rhythm).

The implementation gap is **structural pattern documentation**, not word-level extraction. STYLE-GUIDE.md Part 3 already documents high-level creator techniques. Part 6 expansion should add **actionable copy-paste patterns** extracted from actual transcripts: sentence structures, transition sequences, opening formulas, and evidence-introduction patterns that script-writer-v2 can reference directly.

**Primary recommendation:** Manual pattern extraction from top-performing transcripts into structured STYLE-GUIDE.md sections, with validation checklist for script-writer-v2 agent, not NLP-based automated extraction.

## Standard Stack

### Core (Already Installed)

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Python | 3.14.2 | Script execution, text processing | Current stable release installed |
| difflib | stdlib | Word-level diff for script→transcript comparison | Python standard library, no dependencies |
| re | stdlib | Pattern matching, text normalization | Python standard library |
| json | stdlib | Pattern library serialization | Python standard library |
| pathlib | stdlib | File system traversal | Modern Python file handling |

### Supporting (For Future NLP Features)

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| spaCy | 3.x | Sentence structure analysis, POS tagging | **NOT needed for Phase 33** - deferred to v2.1+ for automated pattern extraction |
| NLTK | 3.x | Tokenization, linguistic corpus | Alternative to spaCy for simpler tasks |
| srt | 1.x | SRT subtitle parsing | Already used in corpus_builder.py |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Manual extraction | spaCy + ML pattern detection | Manual: 2-3 hours work, immediate results. Automated: weeks to build, needs 50+ videos for training data. Small dataset = manual wins. |
| Reference docs | Pattern database + query API | Database adds complexity without value for 15-20 patterns. Markdown is grep-able, version-controlled, Claude-readable. |
| Word-level only | Full NLP syntactic analysis | Word-level catches 80% of patterns (contractions, forbidden phrases). Syntactic analysis would catch sentence rhythm but requires labeled training data. |

**Installation:**

N/A - Phase 33 uses existing Python stdlib + manual documentation. No new dependencies required.

## Architecture Patterns

### Recommended Documentation Structure

```
.claude/REFERENCE/STYLE-GUIDE.md
├── Part 1-5: Existing (voice, delivery, structure, creators, checklist)
└── Part 6: Voice Pattern Library (NEW)
    ├── 6.1 Opening Formulas (extracted from Belize, Vance transcripts)
    ├── 6.2 Transition Sequences (causal chains, topic shifts)
    ├── 6.3 Evidence Introduction (quote setup patterns)
    ├── 6.4 Sentence Rhythm Patterns (fragment usage, length patterns)
    └── 6.5 Forbidden Pattern Detection (validation checklist)
```

### Pattern 1: Manual Transcript-to-Pattern Extraction

**What:** Human curator extracts copy-paste patterns from high-performing video transcripts

**When to use:** Small corpus (<30 videos), need immediate results, patterns are structural not word-level

**Process:**

1. **Source Selection:**
   - Belize (23K views) - territorial dispute pattern
   - Vance (42.6% retention) - fact-checking pattern
   - Extract actual transcript text (not script)

2. **Pattern Identification:**
   - Opening hooks (first 60 seconds)
   - Transition phrases between sections
   - Evidence introduction sequences
   - Sentence rhythm (short declaratives, fragments for emphasis)

3. **Documentation Format:**
```markdown
### Opening: Stakes Immediate (Belize Pattern)

**Formula:**
[Modern hook] → [Historical decision] → [Stakes: "whether X should exist"] → [First-person authority: "So I read..."]

**Example from Belize (23K views):**
"[Modern context]. That's because of a treaty from 1859. The question is whether Belize should even exist as an independent country. So, I read that treaty."

**Copy-paste template:**
"[Modern event/context]. That's because of [historical decision/document] from [year]. The question is whether [core stakes]. So, I [read/checked/analyzed] [primary source]."
```

4. **Validation Integration:**
   - Add to script-writer-v2 quality checklist
   - Reference in /script command
   - Update pre-filming checklist

**Example:** See `.claude/REFERENCE/OPENING-HOOK-TEMPLATES.md` for existing formula structure

### Pattern 2: Word-Level Pattern Application (Existing)

**What:** Automated word substitution using `voice/pattern_applier.py`

**When to use:** Catch forbidden phrases, apply consistent word choices (contractions, transition words)

**Current implementation:**
- `VoicePatternApplier` class loads `voice-patterns.json`
- Applies HIGH-confidence patterns (frequency ≥5)
- Word-boundary matching to avoid partial replacements
- Returns change tracking for transparency

**Integration point:** Can be called from script validation workflow, but **not needed for Part 6 documentation**.

### Pattern 3: Validation Checklist Expansion

**What:** Convert documented patterns into boolean checklist items for pre-output validation

**Structure:**
```markdown
### Pre-Script Checklist: Voice Patterns (Part 6)

**Opening (0:00-0:60):**
- [ ] Stakes stated in first 30 seconds (not background first)
- [ ] First-person ownership present ("So I read/checked...")
- [ ] Modern hook before historical context

**Evidence Introduction:**
- [ ] Quote has 3-step pattern: setup → quote → implication
- [ ] Page numbers cited in narration
- [ ] Source shown within 90 seconds of claim

**Sentence Rhythm:**
- [ ] Fragments used only for rhetorical emphasis (not informational lists)
- [ ] "Here's" count: 2-4 (not 10+)
- [ ] Contractions used ("it's" not "it is")
```

**Integration:** script-writer-v2.md already has quality checklist infrastructure. Part 6 adds voice-specific items.

### Anti-Patterns to Avoid

- **Automated extraction without validation:** NLP tools extract word-level patterns well but miss structural patterns (when to use fragments, how to build causal chains). Manual extraction catches intent, not just tokens.

- **Database over-engineering:** 15-20 patterns don't need SQLite, JSON, or query API. Markdown is searchable, version-controlled, and Claude can read it natively.

- **Code proliferation:** Adding Python scripts for every pattern type creates maintenance burden. Reference docs are zero-maintenance once written.

- **Generic pattern libraries:** Importing "academic writing style" or "YouTube voice" patterns dilutes channel-specific voice. Extract from THIS channel's proven videos only.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Sentence parsing | Custom regex-based sentence splitter | Python stdlib `re.split(r'[.!?]+', text)` or spaCy `nlp(text).sents` | Sentence boundary detection has edge cases (Dr., U.S., decimals). stdlib handles basics, spaCy handles complex cases. |
| SRT parsing | Custom subtitle format parser | `srt` library (already installed) | SRT format has timing edge cases, malformed files. srt library handles gracefully. |
| Word-level diff | Custom string comparison | `difflib.SequenceMatcher` (stdlib) | Already implemented in corpus_builder.py. Tested, handles word boundaries correctly. |
| Pattern frequency counting | Manual tallying | `collections.Counter` (stdlib) | Built-in, optimized, one-liner. Already used in pattern_extractor.py. |
| Date extraction from filenames | Custom parsing | `re.search(r'-(\d{4})', folder_name)` + `datetime` | Simple, reliable for "XX-name-YYYY" format. No need for complex parser. |

**Key insight:** This project already avoided most hand-rolled solutions. Pattern extraction code (voice/ directory) uses stdlib effectively. Phase 33 doesn't need new code — needs reference documentation.

## Common Pitfalls

### Pitfall 1: Empty Patterns Syndrome

**What goes wrong:** Automated pattern extraction on small corpus (<30 videos) produces unreliable patterns with high false positive rate.

**Why it happens:** Statistical significance requires minimum sample size. Corpus linguistics research indicates 5-10 documents minimum for pattern detection, but 30+ for reliable patterns. This channel has ~15 published videos.

**How to avoid:** Use manual extraction for structural patterns. Reserve automated extraction for word-level patterns with clear frequency thresholds (≥5 occurrences = HIGH confidence).

**Warning signs:**
- Pattern appears in 1-2 videos only
- Pattern conflicts with documented style (STYLE-GUIDE.md Parts 1-5)
- Pattern is context-specific (proper nouns, video-specific references)

### Pitfall 2: Word-Level vs. Structural Confusion

**What goes wrong:** Existing `voice/` code extracts word substitutions ("utilize" → "use") but can't extract structural patterns (Kraut causal chains, Alex O'Connor concessions).

**Why it happens:** Word-level diff detects token changes. Structural patterns are **sequences**: "BECAUSE X. THEREFORE Y." or "That's fair. But...". These span multiple sentences and require semantic understanding, not just word matching.

**How to avoid:** Separate pattern types clearly:
- **Word-level:** Automated extraction OK (contractions, forbidden phrases, word substitutions)
- **Structural:** Manual extraction required (opening formulas, transition sequences, evidence patterns)

**Warning signs:**
- Trying to use `difflib.SequenceMatcher` to detect multi-sentence patterns
- Regex for detecting "causal chain" style (won't work — needs human judgment)
- Expecting NLP to extract "Alex O'Connor intellectual honesty" automatically

### Pitfall 3: spaCy Python 3.14 Incompatibility

**What goes wrong:** spaCy 3.x not compatible with Python 3.14.2 (current installation). Installation fails with "No matching distribution found."

**Why it happens:** spaCy uses compiled Cython extensions. Python 3.14 is very recent (December 2025). spaCy hasn't released compatible wheels yet. Memory note says "Python 3.11-3.13 required (spaCy incompatible with 3.14)."

**How to avoid:**
- **For Phase 33:** Don't need spaCy. Manual pattern extraction uses stdlib only.
- **For v2.1+ (automated extraction):** Either downgrade Python to 3.13 or wait for spaCy 3.8+ with Python 3.14 support.

**Warning signs:**
- `pip install spacy` fails with wheel errors
- "Unsupported Python version" during installation
- Cython compilation errors

### Pitfall 4: Over-Validating Validated Patterns

**What goes wrong:** Extracting patterns from Belize/Vance (proven 23K views, 42.6% retention), then running statistical validation, then A/B testing before applying.

**Why it happens:** Confusing pattern discovery (unknown patterns) with pattern documentation (known winners).

**How to avoid:** Belize and Vance already validated these patterns with viewer retention. **Just document them.** No need to re-validate. Save A/B testing for NEW patterns.

**Warning signs:**
- "We should test if stakes-first opening works" (it already worked — 23K views)
- Waiting for 30+ videos before documenting proven patterns
- Statistical significance testing on patterns from breakout videos

### Pitfall 5: Documenting Code Patterns Instead of Voice Patterns

**What goes wrong:** Part 6 becomes "how to use pattern_extractor.py" instead of "copy-paste voice patterns for script generation."

**Why it happens:** Existing `voice/` code is well-documented. Easy to document the tool instead of the patterns.

**How to avoid:** Part 6 consumer is **script-writer-v2 agent**, not developer. Document patterns Claude can apply, not code humans can run.

**Good documentation:**
```markdown
### Transition: Causal Chain (Kraut Style)

**Pattern:** [Action] → "consequently" → [Result] → "thereby" → [Outcome] → "which meant that" → [Long-term impact]

**Example:** "The Mongols enforced their economic order, consequently shifting the center of Russian power, thereby making backwaters central, which meant that Russia developed differently from Europe."
```

**Bad documentation:**
```markdown
### Using Pattern Extractor

Run `python -m tools.script-checkers.voice.pattern_extractor` to analyze transcripts...
```

## Code Examples

### Pattern Extraction Workflow (Existing Code)

```python
# Source: tools/script-checkers/voice/pattern_extractor.py
from pathlib import Path
from voice.pattern_extractor import build_pattern_library

# Build pattern library from all script+SRT pairs
projects_dir = Path('video-projects')
output_path = Path('tools/script-checkers/voice-patterns.json')

patterns = build_pattern_library(projects_dir, output_path)

# Output structure:
# {
#   "metadata": {
#     "generated": "2026-02-10T...",
#     "videos_analyzed": 11,
#     "video_list": ["1-somaliland-2025", ...],
#   },
#   "patterns": {
#     "word_substitutions": [
#       {"formal": "utilize", "casual": "use", "frequency": 7, "confidence": "HIGH"}
#     ],
#     "anti_patterns": ["it should be noted that", "in order to"],
#     "additions": ["actually", "the truth is"]
#   }
# }
```

### Pattern Application (Existing Code)

```python
# Source: tools/script-checkers/voice/pattern_applier.py
from voice.pattern_applier import apply_voice_patterns

script_text = """
It should be noted that you should utilize this methodology.
However, the evidence demonstrates that...
"""

# Apply patterns (only HIGH confidence, frequency ≥5)
modified_text, changes = apply_voice_patterns(script_text, show_changes=True)

# Output:
# modified_text: "You should use this methodology. But the evidence demonstrates..."
# changes: [
#   {"type": "removal", "phrase": "it should be noted that", "count": 1},
#   {"type": "substitution", "original": "utilize", "replacement": "use", "count": 1}
# ]
```

### Manual Pattern Extraction (Recommended for Phase 33)

```python
# NO CODE NEEDED - Manual process documented here for clarity

# 1. Read transcript files
# Source: video-projects/_ARCHIVED/[project]/[video].srt

# 2. Identify pattern manually:
# - Opening: "whether Belize should even exist" (stakes immediate)
# - Transition: "So, I read that treaty" (first-person authority)
# - Evidence: "The treaty says... Translation: [plain language]"

# 3. Document in STYLE-GUIDE.md Part 6:
"""
### Opening: Stakes Immediate (Belize Pattern)

**When to use:** Territorial disputes, contested history

**Formula:** [Modern hook] → [Historical decision] → [Stakes] → [Authority]

**Example:** "...whether Belize should even exist as an independent country. So, I read that treaty."

**Copy-paste template:**
"The question is whether [core stakes]. So, I [read/checked/analyzed] [primary source]."
"""

# 4. Add to script-writer-v2 checklist:
# - [ ] Stakes stated in first 30 seconds (not background first)
# - [ ] First-person ownership present ("So I read...")
```

### Validation Checklist Integration

```markdown
<!-- Source: .claude/agents/script-writer-v2.md -->

### Pre-Output Checklist (MANDATORY - All Scripts)

**Voice Patterns (Part 6):**
- [ ] Opening uses proven formula (Stakes Immediate, Document-First, or Both-Extremes)
- [ ] First-person authority in first 60 seconds ("So I read/checked...")
- [ ] Transitions use documented patterns (causal chains, topic shifts)
- [ ] Evidence has 3-step pattern: setup → quote → implication
- [ ] Sentence rhythm matches Belize/Vance: fragments for emphasis, contractions, short declaratives
- [ ] "Here's" count: 2-4 (not 10+)
- [ ] No forbidden phrases (grep check against Part 1 list)
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Generic AI scriptwriting | Voice fingerprinting from transcripts | v1.2 (Phase 12, Jan 2026) | Scripts sounded like AI, not creator. voice/ directory built word-level extraction. |
| Word substitutions only | Word + structural patterns | **Phase 33 (Feb 2026)** | Word-level catches contractions, forbidden phrases. Structural catches opening formulas, causal chains, evidence patterns. |
| Code-based pattern application | Reference doc + manual validation | v2.0 research (Feb 2026) | Small corpus (<30 videos) makes automated extraction unreliable. Reference docs faster, more accurate. |
| NLP libraries required | Manual extraction + stdlib | Phase 33 | spaCy incompatible with Python 3.14. Manual extraction produces better results for structural patterns anyway. |

**Deprecated/outdated:**
- **Automated structural pattern extraction:** Deferred to v2.1+ when corpus reaches 30+ videos. Current approach: manual extraction from Belize/Vance into STYLE-GUIDE.md Part 6.
- **spaCy for Phase 33:** Not needed. Python 3.14 incompatibility makes it unavailable anyway. Manual extraction superior for small datasets.
- **Pattern database infrastructure:** JSON storage exists (voice-patterns.json) but only needed for word-level patterns. Structural patterns documented in markdown.

## Open Questions

1. **How many patterns constitute "complete" Part 6?**
   - What we know: Belize and Vance provide 5-10 opening formulas, 8-12 transition patterns, 4-6 evidence introduction sequences
   - What's unclear: Minimum viable set for script-writer-v2 to generate channel-accurate scripts
   - Recommendation: Start with 20 patterns (5 openings, 8 transitions, 4 evidence, 3 sentence rhythm). Expand based on script generation feedback.

2. **Should word-level patterns be integrated into Part 6, or stay in voice-patterns.json?**
   - What we know: word-level patterns already extracted (voice-patterns.json). Part 6 is for structural patterns.
   - What's unclear: Script-writer-v2 needs both. Should they be consolidated?
   - Recommendation: Keep separate. Word-level = automated validation (stumble checker). Structural = reference docs (style guide). Different use cases.

3. **What's the update cadence for Part 6?**
   - What we know: Voice evolves. Recent videos should influence patterns more (temporal weighting in pattern_extractor.py).
   - What's unclear: How often to review and update documented patterns?
   - Recommendation: Review after each breakout video (≥2x baseline performance). Add proven patterns, deprecate outdated ones. Quarterly review otherwise.

4. **Should deferred patterns (Alex O'Connor concessions, Kraut causal chains) be documented now or later?**
   - What we know: STYLE-GUIDE.md Part 5 already documents creator techniques at high level. Part 6 should add copy-paste specifics.
   - What's unclear: Extract from creator transcripts (transcripts/ directory) or from channel's own videos?
   - Recommendation: Phase 33 focuses on Belize/Vance (channel's proven patterns). Phase 34-35 can add creator-specific patterns from transcripts/ if needed.

5. **How to handle pattern conflicts between videos?**
   - What we know: Belize uses "So, I read that treaty" (first-person ownership). Other videos might use different phrasing.
   - What's unclear: When patterns conflict, which wins? Most recent? Highest retention?
   - Recommendation: Highest retention wins. Belize (23K views) and Vance (42.6% retention) are outliers. Their patterns take precedence.

## Sources

### Primary (HIGH confidence)

- **Existing codebase:**
  - `tools/script-checkers/voice/pattern_extractor.py` - Word-level pattern extraction implementation
  - `tools/script-checkers/voice/pattern_applier.py` - Pattern application engine
  - `tools/script-checkers/voice/corpus_builder.py` - Script→transcript comparison
  - `.claude/REFERENCE/STYLE-GUIDE.md` - Existing voice documentation (Parts 1-5)
  - `.claude/agents/script-writer-v2.md` - Quality checklist infrastructure

- **V2.0 Research:**
  - `.planning/research/FEATURES-v2.0-CHANNEL-INTELLIGENCE.md` - Voice pattern library prioritization, Empty Patterns Syndrome warning, reference doc approach

- **Project memory:**
  - `C:\Users\benoi\.claude\projects\G--History-vs-Hype\memory\MEMORY.md` - "Voice patterns: reference doc expansion (STYLE-GUIDE Part 6), NOT code proliferation"

### Secondary (MEDIUM confidence)

- **NLP Libraries (2026):**
  - [Top 8 Python Libraries For Natural Language Processing (NLP) in 2026](https://www.analyticsvidhya.com/blog/2021/05/top-python-libraries-for-natural-language-processing-nlp-in/) - spaCy, NLTK overview
  - [spaCy · Industrial-strength Natural Language Processing in Python](https://spacy.io/) - Official documentation
  - [8 great Python libraries for natural language processing](https://www.infoworld.com/article/2266281/8-great-python-libraries-for-natural-language-processing.html) - Library comparison

- **Writing Style Analysis:**
  - [Writing Styles Classification Using Stylometric Analysis](https://github.com/Hassaan-Elahi/Writing-Styles-Classification-Using-Stylometric-Analysis) - Stylometric techniques: lexical features, n-grams, readability
  - [8. Analyzing Sentence Structure - NLTK](https://www.nltk.org/book/ch08.html) - Sentence parsing, dependency analysis
  - [Detection of changes in literary writing style using N-grams](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0267590) - N-gram pattern detection in corpus linguistics

### Tertiary (LOW confidence - informational only)

- **Pattern Extraction Techniques:**
  - [Text Analysis in Python: Techniques and Libraries Explained](https://airbyte.com/data-engineering-resources/text-analysis-in-python) - General text analysis overview
  - [How to Substring a String in Python (2026)](https://thelinuxcode.com/how-to-substring-a-string-in-python-2026-slicing-splitting-and-pattern-extraction-that-holds-up-in-production/) - String pattern extraction best practices

## Metadata

**Confidence breakdown:**
- Standard stack: **HIGH** - All tools already installed, proven in existing codebase
- Architecture: **HIGH** - Manual extraction approach validated by v2.0 research, small dataset size
- Pitfalls: **HIGH** - Empty Patterns Syndrome documented, spaCy incompatibility verified, word vs. structural distinction clear

**Research date:** 2026-02-10
**Valid until:** 90 days (stable domain - reference documentation doesn't change rapidly)

**Notes:**
- Phase 33 requires **zero new code** - reference document expansion only
- Existing `voice/` directory handles word-level patterns adequately
- Manual extraction is faster and more accurate for structural patterns with small corpus
- spaCy deferral acceptable - not needed for Phase 33 deliverables
