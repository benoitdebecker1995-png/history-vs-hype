# Phase 36: Retention Science - Research

**Researched:** 2026-02-13
**Domain:** YouTube retention analytics, data-driven scriptwriting, pattern synthesis
**Confidence:** HIGH

## Summary

Retention Science synthesizes actionable retention patterns from published video data into a standardized playbook format. The phase builds on existing retention_mapper.py and section_diagnostics.py tools (shipped in Phase 35) to create STYLE-GUIDE.md Part 9 - a machine-readable retention playbook that script-writer-v2 agent can reference during generation.

The core technical challenge is pattern extraction: converting raw retention drop data into prescriptive scriptwriting rules. Research shows educational content averages 42.1% retention (top-tier niche), with 55% viewer loss by 60 seconds. Pattern detection must identify section-level characteristics (length, evidence density, modern relevance proximity) that correlate with retention outcomes.

Architectural approach: Extend existing Python analytics stack with pattern synthesis layer that updates STYLE-GUIDE.md Part 9 automatically as new videos publish. Use hardcoded voice pattern library (29 patterns from Part 6) as diagnostic recommendation engine. Implement predictive scoring by correlating section attributes with historical drop patterns.

**Primary recommendation:** Build incremental pattern synthesis pipeline that extends section_diagnostics.py with Part 9 writer, add retention scoring to script validation, implement auto-update trigger on new POST-PUBLISH-ANALYSIS.md creation.

## Standard Stack

### Core

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Python stdlib | 3.11-3.13 | Data processing, file I/O | Already project standard, no new dependencies |
| SQLite | 3.x | Retention data storage (analytics.db) | Already in use for keywords.db (PRAGMA user_version=27) |
| Markdown | - | STYLE-GUIDE.md Part 9 output format | Human-readable, agent-parseable, version-controllable |

### Supporting

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| json | stdlib | Pattern serialization, intermediate storage | Encoding extracted patterns before markdown conversion |
| statistics | stdlib | Average calculations, threshold detection | Calculating retention baselines, identifying outliers |
| pathlib | Path | File system traversal for POST-PUBLISH-ANALYSIS.md | Finding new published video data for auto-update |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Markdown playbook | JSON schema | JSON: machine-readable but not human-editable. Markdown: both readable and agent-parseable via existing Read tool |
| SQLite | Pandas DataFrame | Pandas adds 12MB dependency for simple aggregations. SQLite already in stack. |
| Python | R/Julia for stats | R/Julia better for advanced ML but overkill for pattern counting and threshold detection |

**Installation:**
No new dependencies required. Use existing Python 3.11-3.13 + stdlib.

## Architecture Patterns

### Recommended Project Structure

```
tools/youtube-analytics/
├── retention_mapper.py          # [EXISTS] Maps drops to script sections
├── section_diagnostics.py       # [EXISTS] Diagnoses drop causes, recommends patterns
├── feedback_queries.py          # [EXISTS] Queries pre-script insights
├── playbook_synthesizer.py      # [NEW] Generates Part 9 from aggregated data
├── retention_scorer.py          # [NEW] Scores script sections for predicted retention
└── auto_updater.py              # [NEW] Watches for new POST-PUBLISH-ANALYSIS, triggers synthesis

.claude/REFERENCE/
└── STYLE-GUIDE.md
    └── Part 9: Retention Playbook  # [NEW] Auto-generated, version-controlled
```

### Pattern 1: Incremental Pattern Synthesis

**What:** Generate playbook from accumulated retention data, not one-time export
**When to use:** After each new video publishes, re-synthesize Part 9 to incorporate new patterns
**Example:**

```python
# playbook_synthesizer.py
def synthesize_part9(min_confidence_videos=3):
    """
    Generate STYLE-GUIDE.md Part 9 from retention database.

    Aggregates:
    - Section-level drop patterns (retention_mapper + section_diagnostics)
    - Topic-specific patterns (feedback_queries topic insights)
    - Voice pattern effectiveness (which Part 6 patterns correlated with retention)

    Returns:
        Markdown text for Part 9 with sections:
        - Opening retention rules (first 60 sec patterns)
        - Section pacing guidelines (length × evidence density × drop correlation)
        - Modern relevance proximity rules (gap tolerance before drop)
        - Voice pattern effectiveness ranking (Part 6 patterns sorted by retention impact)
    """
    db = KeywordDB()

    # Get all videos with retention data
    videos = db.get_videos_with_retention()

    # Extract patterns
    opening_patterns = extract_opening_patterns(videos)
    pacing_guidelines = calculate_pacing_thresholds(videos)
    relevance_rules = extract_modern_relevance_gaps(videos)
    pattern_rankings = rank_voice_patterns(videos)

    # Build Part 9 markdown
    part9_text = format_part9_markdown({
        'opening': opening_patterns,
        'pacing': pacing_guidelines,
        'relevance': relevance_rules,
        'patterns': pattern_rankings,
        'confidence': calculate_confidence(len(videos), min_confidence_videos)
    })

    return part9_text
```

### Pattern 2: Retention Scoring for Prediction

**What:** Score script sections BEFORE filming based on historical drop patterns
**When to use:** During `/script` generation, flag risky sections proactively
**Example:**

```python
# retention_scorer.py
def score_section_retention(section_text, section_type, topic_type):
    """
    Predict retention risk for script section.

    Correlates section attributes with historical drops:
    - Length (word count) vs topic_type avg
    - Evidence density (quotes per 100 words)
    - Modern relevance proximity (words since last "today"/"2026" mention)
    - Voice pattern presence (which Part 6 patterns detected)

    Args:
        section_text: Script section content
        section_type: 'intro', 'body', 'conclusion'
        topic_type: 'territorial', 'ideological', etc.

    Returns:
        {
            'score': float (0.0-1.0, higher = better retention predicted),
            'risk_level': 'LOW' | 'MEDIUM' | 'HIGH',
            'warnings': [
                {'issue': 'Section length 250 words exceeds territorial avg 180',
                 'recommendation': 'Split into 2 sections or add pattern interrupt'},
                ...
            ]
        }
    """
    db = KeywordDB()

    # Calculate section attributes
    word_count = len(section_text.split())
    evidence_density = count_quotes(section_text) / (word_count / 100)
    modern_relevance_gap = words_since_modern_mention(section_text)
    voice_patterns = detect_voice_patterns(section_text)

    # Get topic baseline from past videos
    baseline = db.get_topic_baseline(topic_type)

    # Calculate deviation scores
    length_deviation = abs(word_count - baseline['avg_section_length']) / baseline['std_dev']
    evidence_deviation = abs(evidence_density - baseline['avg_evidence_density'])
    relevance_penalty = max(0, modern_relevance_gap - 150) / 50  # Penalty if >150 words

    # Pattern bonus
    pattern_bonus = sum([0.1 for p in voice_patterns if p in baseline['high_retention_patterns']])

    # Composite score
    raw_score = 1.0 - (length_deviation * 0.3 + evidence_deviation * 0.2 + relevance_penalty * 0.3) + pattern_bonus
    score = max(0.0, min(1.0, raw_score))

    # Generate warnings
    warnings = []
    if length_deviation > 1.5:
        warnings.append({
            'issue': f'Section length {word_count} words exceeds {topic_type} avg {baseline["avg_section_length"]}',
            'recommendation': 'Split into 2 sections or add pattern interrupt (STYLE-GUIDE Part 6.4)'
        })
    if modern_relevance_gap > 150:
        warnings.append({
            'issue': f'{modern_relevance_gap} words since modern relevance mention',
            'recommendation': 'Add "which is why today..." bridge (STYLE-GUIDE Part 2)'
        })

    return {
        'score': score,
        'risk_level': 'HIGH' if score < 0.5 else 'MEDIUM' if score < 0.7 else 'LOW',
        'warnings': warnings
    }
```

### Pattern 3: Auto-Update Trigger

**What:** Automatically re-synthesize Part 9 when new POST-PUBLISH-ANALYSIS.md created
**When to use:** After publishing video, retention data added to database triggers playbook update
**Example:**

```python
# auto_updater.py
import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class PlaybookUpdater(FileSystemEventHandler):
    """Watch for new POST-PUBLISH-ANALYSIS.md files, trigger Part 9 synthesis."""

    def on_created(self, event):
        if event.is_directory:
            return

        path = Path(event.src_path)
        if path.name == 'POST-PUBLISH-ANALYSIS.md':
            print(f"New analysis detected: {path}")

            # Extract video data, update database (already handled by /engage --correction)
            # Then re-synthesize Part 9
            from playbook_synthesizer import synthesize_part9, write_part9_to_style_guide

            part9_text = synthesize_part9(min_confidence_videos=3)
            write_part9_to_style_guide(part9_text)

            print("Part 9 updated in STYLE-GUIDE.md")

def watch_for_new_analyses(project_root):
    """Start file watcher for POST-PUBLISH-ANALYSIS.md creation."""
    observer = Observer()
    observer.schedule(PlaybookUpdater(), str(project_root / 'video-projects'), recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
```

### Anti-Patterns to Avoid

- **One-time export playbook:** Playbook must update incrementally as new videos publish, not manual regeneration
- **Over-fitting to outliers:** Require minimum 3 videos before establishing topic-specific pattern (use channel average otherwise)
- **Ignoring confidence levels:** Part 9 must flag LOW confidence patterns (e.g., "ideological opening patterns: 2 videos, LOW confidence")
- **Static thresholds:** Retention "good/bad" thresholds must adapt per topic_type (territorial avg ≠ ideological avg)
- **Breaking STYLE-GUIDE structure:** Part 9 must follow existing markdown structure (Part 1-7 already exist, don't renumber)

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Pattern detection from text | Custom NLP/regex for voice pattern detection | Hardcoded pattern library from STYLE-GUIDE Part 6 | 29 patterns already documented, validated by high-performing videos. Detection = simple substring matching ("consequently", "thereby", etc.) |
| Retention graph parsing | Computer vision to parse YouTube retention graphs | retention_mapper.py with manual percentage-position input | YouTube Analytics API returns percentage-based positions, not images. Mapper already converts to script sections. |
| Statistical outlier detection | Custom z-score / IQR algorithms | Python statistics.mean() + simple threshold (1.5× std dev) | Dataset too small (<50 videos) for advanced outlier detection. Simple threshold sufficient. |
| Markdown generation | Custom template engine | f-strings with hardcoded structure | Part 9 structure is fixed. f-strings simpler than Jinja2 for single template. |
| File watching | Polling loop checking mtime | watchdog library for filesystem events | watchdog is stdlib-adjacent (pure Python), handles edge cases (rapid writes, network drives) |

**Key insight:** This isn't a machine learning problem (yet). With <50 videos, pattern extraction is threshold-based aggregation. Hardcode voice pattern library, use simple statistics, regenerate on publish. ML becomes relevant at 200+ videos.

## Common Pitfalls

### Pitfall 1: Conflating Retention Position with Script Position

**What goes wrong:** Retention drop at "45% video position" mapped to wrong script section because video has multiple cuts/b-roll sections not in script

**Why it happens:** retention_mapper.py uses fixed 150 WPM to estimate timestamps, but actual video pacing varies (talking head vs b-roll montage)

**How to avoid:**
1. Use actual video duration from YouTube Analytics, not word-count estimate
2. Map retention % to actual timestamp first: `drop_timestamp = video_duration * drop_position`
3. Then map timestamp to script section using cumulative word counts
4. Flag low-confidence mappings where word-count-based estimate diverges >15 sec from actual duration

**Warning signs:** Section diagnostics blaming wrong sections (e.g., reporting drop in "Conclusion" when user knows it was mid-video)

### Pitfall 2: Over-Indexing on Single-Video Patterns

**What goes wrong:** Territorial video with 12% drop at treaty section → playbook says "NEVER show treaties for >30 seconds"

**Why it happens:** Small sample size + no control for confounding factors (that video also had audio issue, long section, no pattern interrupt)

**How to avoid:**
1. Require minimum 3 videos before establishing topic-specific pattern
2. Use channel-wide average as fallback for topics <3 videos
3. Flag confidence level in Part 9: "territorial treaty sections: 2 videos, LOW confidence"
4. Cross-reference with voice pattern effectiveness: did high-retention videos also show treaties? If yes, treaty ≠ problem, execution = problem

**Warning signs:** Playbook rules contradicting STYLE-GUIDE Parts 1-7 (e.g., "don't show primary sources" contradicts core channel differentiator)

### Pitfall 3: Static Playbook Becoming Stale

**What goes wrong:** Part 9 generated once in Jan 2026, never updated. By Jun 2026, channel has 20 new videos but playbook reflects old 10-video dataset

**Why it happens:** No auto-update trigger, manual regeneration friction

**How to avoid:**
1. Implement auto-update trigger (Pattern 3 above) watching for POST-PUBLISH-ANALYSIS.md
2. Add "Last updated" timestamp to Part 9 header
3. Surface staleness warning in /script preamble if Part 9 >60 days old
4. Make synthesis fast (<5 sec) so auto-update doesn't block workflow

**Warning signs:** Script-writer-v2 recommendations feeling outdated, retention improvements not reflected in playbook

### Pitfall 4: Ignoring Topic-Type Variation

**What goes wrong:** Playbook says "sections should average 150 words" based on territorial videos, but ideological videos naturally run longer (250 words avg)

**Why it happens:** Aggregating across all videos without topic_type stratification

**How to avoid:**
1. Calculate baselines PER topic_type (territorial, ideological, legal, colonial, general)
2. Use topic-specific threshold in retention_scorer.py
3. Fall back to channel average only when topic <3 videos
4. Document topic variation in Part 9 (table showing territorial avg vs ideological avg)

**Warning signs:** Retention scorer flagging high-performing sections as "too long" because wrong baseline

### Pitfall 5: Retention Warnings Ignored During Script Generation

**What goes wrong:** retention_scorer.py generates warnings, but script-writer-v2 doesn't act on them (warnings buried in logs, not surfaced in generation context)

**Why it happens:** Warnings generated post-generation during validation, not during active generation

**How to avoid:**
1. Integrate retention scoring INTO script-writer-v2 generation loop, not just post-validation
2. Add to script-writer-v2 Rule 14: "After writing each section, run retention_scorer.py and revise if HIGH risk"
3. Surface warnings in /script output: "⚠️ Section 3 scored 0.45 (HIGH risk) - recommend split or pattern interrupt"
4. Make warnings actionable with specific STYLE-GUIDE pattern references

**Warning signs:** Scripts still triggering same retention drops as past videos despite warnings

## Code Examples

Verified patterns from existing codebase:

### Pattern Detection from section_diagnostics.py

```python
# Source: G:/History vs Hype/tools/youtube-analytics/section_diagnostics.py (lines 284-292)
# Check for missing causal chains
causal_connectors = ['consequently', 'thereby', 'which meant that', 'as a result', 'which created']
if not any(connector in text_lower for connector in causal_connectors):
    root_causes.append('Missing causal chain - sequence without causation')
    recommendations.append({
        'fix': 'Add causal chain to show WHY things happened, not just WHAT',
        'pattern': 'Kraut-Style Causal Chain',
        'pattern_ref': 'STYLE-GUIDE.md Part 6.2 Pattern 1',
        'insertion_hint': 'After describing event, add: "which meant that [consequence], consequently [implication]."'
    })
```

### Topic-Specific Insights from feedback_queries.py

```python
# Source: G:/History vs Hype/tools/youtube-analytics/feedback_queries.py (lines 686-704)
topic_patterns = {
    'territorial': [
        'Use zero-impact moments for dramatic numerical reveals (STYLE-GUIDE Part 6.4 Pattern 2)',
        'Show treaties/maps on screen rather than describing (STYLE-GUIDE Part 3)'
    ],
    'ideological': [
        'Apply intellectual honesty pattern when addressing opposing views (STYLE-GUIDE Part 6.2 Pattern 1)',
        'Use causal chains to show historical consequences (STYLE-GUIDE Part 6.1 Pattern 3)'
    ],
    'legal': [
        'Display legal documents as primary evidence (STYLE-GUIDE Part 3)',
        'Use precise legal terminology with immediate definitions (STYLE-GUIDE Part 6.1 Pattern 5)'
    ]
}
```

### Retention Mapping from retention_mapper.py

```python
# Source: G:/History vs Hype/tools/youtube-analytics/retention_mapper.py (lines 43-76)
def map_retention_to_sections(drop_off_points, sections, wpm=150):
    """
    Map retention drop points to specific script sections.
    Converts YouTube's percentage-based positions to script sections using word-count timing.
    """
    if not drop_off_points or not sections:
        return []

    # Calculate total words
    total_words = sum(s.word_count for s in sections)
    if total_words == 0:
        return []

    # Calculate cumulative word percentages for each section
    cumulative = []
    running_total = 0

    for section in sections:
        start_pct = running_total / total_words
        end_pct = (running_total + section.word_count) / total_words

        cumulative.append({
            'section': section,
            'start_pct': start_pct,
            'end_pct': end_pct,
            'start_word': running_total,
            'end_word': running_total + section.word_count
        })

        running_total += section.word_count
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Manual retention review (watch retention graph, guess causes) | retention_mapper.py + section_diagnostics.py (automated drop-to-section mapping + pattern recommendations) | Phase 35 (2026-02-11) | Replaces manual guessing with data-driven diagnosis |
| Static scriptwriting rules (STYLE-GUIDE Parts 1-7 never change) | Dynamic playbook (Part 9 updates as new videos publish) | Phase 36 (2026-02 - this phase) | Playbook evolves with channel performance data |
| Post-filming retention analysis only | Pre-filming predictive scoring + post-filming analysis | Phase 36 (2026-02 - this phase) | Catch retention risks BEFORE filming |
| WebSearch for "YouTube retention best practices" | Channel-specific retention patterns from own data | Phase 36 (2026-02 - this phase) | Generic advice → channel DNA-specific guidance |

**Key shift (2026):** Educational content retention optimization moving from generic best practices to channel-specific pattern synthesis. Research shows 42.1% avg retention for educational how-to's, but History vs Hype averages 30-35%. Playbook must encode what works for THIS channel's audience (males 25-44, intellectual competence seekers), not generic edu-content.

**Deprecated/outdated:**
- Manual retention graph interpretation: retention_mapper.py automates position-to-section mapping
- One-size-fits-all pacing rules: Topic-type stratification required (territorial ≠ ideological pacing)
- "Never show X" absolute rules: Context-dependent (treaties work when shown, not read aloud)

## Open Questions

1. **Confidence threshold for pattern promotion**
   - What we know: Current code uses "2 occurrences = pattern" for failure patterns, higher threshold for success patterns
   - What's unclear: Optimal threshold for promoting pattern from "observed" to "prescriptive rule" in Part 9
   - Recommendation: Start with 3 videos minimum, flag as LOW confidence until 5 videos. Re-evaluate at 50 total videos.

2. **Voice pattern attribution**
   - What we know: 29 voice patterns hardcoded in section_diagnostics.py, recommendations map drops to patterns
   - What's unclear: How to measure which Part 6 patterns CAUSED retention improvement (correlation vs causation)
   - Recommendation: Phase 36 focuses on correlation (pattern presence × retention outcome). Causal inference requires A/B testing (defer to future phase).

3. **Retention score calibration**
   - What we know: Educational content averages 42.1% retention, History vs Hype averages 30-35%
   - What's unclear: What retention score (0.0-1.0) should map to "acceptable" for this channel?
   - Recommendation: Use channel's own 30-35% as baseline, not generic 42.1%. Score >0.7 = "likely to match channel avg", >0.85 = "likely outlier-level retention".

4. **Modern relevance gap tolerance**
   - What we know: Viewers drop when >90 seconds pass without connecting to present (STYLE-GUIDE Part 2)
   - What's unclear: Does this vary by topic_type? Do ideological videos tolerate longer historical sections?
   - Recommendation: Measure per topic_type. Hypothesis: territorial videos need modern relevance every 60-90 sec (maps = visual anchors), ideological can run 120 sec (causal chains maintain engagement).

5. **Playbook update frequency**
   - What we know: Auto-update triggers on POST-PUBLISH-ANALYSIS.md creation
   - What's unclear: Should synthesis run immediately (blocking) or queued (async)? How to handle rapid successive publishes?
   - Recommendation: Queue synthesis with 5-minute debounce. If multiple videos publish same day, batch update once after last publish.

## Sources

### Primary (HIGH confidence)

- **Existing codebase:**
  - `G:/History vs Hype/tools/youtube-analytics/retention_mapper.py` - retention position to script section mapping
  - `G:/History vs Hype/tools/youtube-analytics/section_diagnostics.py` - 29 hardcoded voice patterns, diagnostic logic
  - `G:/History vs Hype/tools/youtube-analytics/feedback_queries.py` - topic-specific pattern suggestions, pre-script insights
  - `G:/History vs Hype/.claude/REFERENCE/STYLE-GUIDE.md` - Parts 1-7 structure, voice pattern library (Part 6)
  - `G:/History vs Hype/.claude/agents/script-writer-v2.md` - Agent consuming playbook, Rule 14 references Part 6

- **Official Python documentation:**
  - Python 3.11-3.13 stdlib (json, statistics, pathlib) - standard library usage patterns
  - SQLite PRAGMA user_version - database versioning (already at version 27 in project)

### Secondary (MEDIUM confidence)

- [Beyond Views: The 2025 State of YouTube Audience Retention | Retention Rabbit](https://www.retentionrabbit.com/blog/2025-youtube-audience-retention-benchmark-report) - Educational How-To's: 42.1% average retention benchmark (2026-02-13 access)

- [YouTube Audience Retention 2026: Benchmarks, Analysis & How to Improve](https://socialrails.com/blog/youtube-audience-retention-complete-guide) - 55% viewer loss by 60 seconds, 8-second consideration window (2026-02-13 access)

- [How To Skyrocket Your YouTube Retention With the Right Video Script](https://www.videodeck.co/blog/how-to-skyrocket-your-youtube-retention-with-the-right-video-script) - 110-150 WPM optimal pacing for educational content (2026-02-13 access)

- [The Retention Playbook: Reducing Churn with Proactive AI Video Content](https://advids.co/insights/the-retention-playbook-reducing-churn-with-proactive-ai-video-content) - Generative AI for automated playbook generation, near-zero marginal cost (2026-02-13 access)

- [Customer Retention AI: Advanced Marketing Analytics 2026](https://www.roboticmarketer.com/how-customer-retention-ai-will-transform-marketing-automation-in-2026/) - Predictive models for retention risk, automated content triggers (2026-02-13 access)

### Tertiary (LOW confidence - WebSearch only)

- [How to Increase Retention & Watch-Time on your Shorts](https://virvid.ai/blog/ai-shorts-increase-retention-watch-time) - 50-60% drop in first 3 seconds for Shorts (not directly applicable to 8-12 min longform, but validates early-drop pattern)

- [Machine Learning PoC for Retention Prediction in a Mobile Game](https://indatalabs.com/resources/retention-prediction) - 92% accuracy churn prediction (gaming context, shows ML feasibility but dataset size mismatch for current phase)

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - No new dependencies, existing Python stdlib + SQLite architecture
- Architecture patterns: HIGH - Extends proven retention_mapper.py + section_diagnostics.py patterns from Phase 35
- Code examples: HIGH - Extracted from shipped production code (Phase 35 tools)
- Retention benchmarks: MEDIUM - Generic educational content benchmarks (42.1%) verified, but channel-specific baselines require own data
- Predictive scoring approach: MEDIUM - Statistical correlation approach validated for <50 video datasets, ML approach deferred until 200+ videos
- Pitfalls: HIGH - Based on known issues from existing retention_mapper.py (fixed 150 WPM assumption) and small-sample statistical risks

**Research date:** 2026-02-13
**Valid until:** 60 days (2026-04-14) for technical patterns, 30 days for retention benchmarks (YouTube ecosystem evolves rapidly)

**Critical dependencies:**
- Retention_mapper.py and section_diagnostics.py remain stable (no breaking changes)
- STYLE-GUIDE.md Part 6 voice pattern library remains authoritative (29 patterns hardcoded in diagnostics)
- POST-PUBLISH-ANALYSIS.md format stable for auto-update trigger parsing
- SQLite PRAGMA user_version migration path documented if schema changes needed
