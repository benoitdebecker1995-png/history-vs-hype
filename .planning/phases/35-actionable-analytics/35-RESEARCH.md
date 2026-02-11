# Phase 35: Actionable Analytics - Research

**Researched:** 2026-02-11
**Domain:** Analytics presentation, retention-to-script mapping, diagnostic systems
**Confidence:** HIGH

## Summary

Phase 35 transforms raw analytics into concrete production recommendations. The technical challenge is mapping YouTube's percentage-based retention curve (0-100% through video) back to actual script sections using word-count-based timing estimates, then diagnosing WHY retention drops and WHAT to fix using voice pattern library and channel DNA references.

The existing tools provide the foundation: `retention.py` fetches retention curves, `parser.py` breaks scripts into sections, `feedback.py` stores lessons from past videos, and `STYLE-GUIDE.md Part 6` documents 22 voice patterns. Phase 35 integrates these into an actionable workflow that surfaces insights proactively before `/script` generation (ACTN-04), not just in post-mortem reports.

**Primary recommendation:** Build retention-to-script mapper as core module, extend `analyze.py` to generate section-specific diagnoses referencing voice patterns, create pre-script insight surfacing in `/script` command, add topic strategy aggregator using existing performance database.

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Python 3.11-3.13 | 3.11+ | Runtime environment | Project requirement (spaCy compatibility) |
| sqlite3 | Built-in | Database access | Already used for keywords.db throughout project |
| Existing tools/youtube-analytics/*.py | Current | YouTube Analytics integration | Already provides retention curves, metrics, benchmarks |
| Existing tools/production/parser.py | Current | Script section parsing | Already parses scripts into H2 sections with word counts |
| Existing tools/discovery/database.py (KeywordDB) | Current | Feedback storage | Phase 31 feedback loop infrastructure |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| json | Built-in | Voice patterns data | Reading STYLE-GUIDE.md Part 6 references |
| datetime | Built-in | Timestamp handling | Retention curve to script section timing |
| pathlib | Built-in | File system operations | Finding project folders, script files |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Word-count timing | Video metadata timestamps | YouTube API doesn't provide per-section retention timestamps, only percentage-based curve |
| Custom retention fetcher | Use existing retention.py | No reason to duplicate - retention.py already works |
| New database tables | Extend feedback table | feedback table already stores drop_points and observations - just need better structure |

**Installation:**
```bash
# No new dependencies needed - uses existing project stack
cd tools/youtube-analytics
python -m pip list | grep -E "sqlite3|json"  # Verify built-ins available
```

## Architecture Patterns

### Recommended Project Structure
```
tools/youtube-analytics/
├── retention_mapper.py         # NEW - Maps retention curve % to script sections
├── section_diagnostics.py      # NEW - Diagnoses WHY sections lost viewers
├── topic_strategy.py           # NEW - Aggregates performance by topic type
├── analyze.py                  # EXTEND - Add section-level recommendations
├── feedback_queries.py         # EXTEND - Pre-script insight surfacing
└── retention.py                # EXISTING - Already fetches retention curves

tools/production/
└── parser.py                   # EXISTING - Already parses script sections

.claude/commands/
├── analyze.md                  # EXTEND - Document new section-level output
└── script.md                   # EXTEND - Auto-surface insights before generation
```

### Pattern 1: Retention-to-Script Mapping
**What:** Convert YouTube's percentage-based retention curve to script section boundaries using word-count-based timing estimates.

**When to use:** Whenever analyzing retention drops for a published video with available script.

**Example:**
```python
# retention_mapper.py
from tools.production.parser import ScriptParser
from tools.youtube_analytics.retention import get_retention_data

def map_retention_to_sections(video_id: str, script_path: str) -> list:
    """
    Map retention drop points to specific script sections.

    Args:
        video_id: YouTube video ID
        script_path: Path to script markdown file

    Returns:
        List of dicts:
        [
            {
                'section': 'Introduction',
                'drop_position': 0.12,  # 12% through video
                'drop_magnitude': 0.08,  # 8% of viewers lost
                'word_range': (0, 150),
                'estimated_timestamp': '0:00-0:45',
                'section_content_preview': 'First 50 words...'
            }
        ]
    """
    # 1. Get retention curve from YouTube Analytics API
    retention = get_retention_data(video_id)
    drop_points = retention['drop_off_points']

    # 2. Parse script into sections with word counts
    parser = ScriptParser()
    sections = parser.parse_file(script_path)

    # 3. Calculate cumulative word positions
    total_words = sum(s.word_count for s in sections)
    cumulative = []
    running_total = 0
    for section in sections:
        start_pct = running_total / total_words
        end_pct = (running_total + section.word_count) / total_words
        cumulative.append({
            'section': section,
            'start_pct': start_pct,
            'end_pct': end_pct
        })
        running_total += section.word_count

    # 4. Match drops to sections
    mapped_drops = []
    for drop in drop_points:
        position = drop['position']  # 0.0-1.0

        # Find which section this drop falls in
        for item in cumulative:
            if item['start_pct'] <= position < item['end_pct']:
                mapped_drops.append({
                    'section': item['section'].heading,
                    'drop_position': position,
                    'drop_magnitude': drop['drop'],
                    'word_range': (
                        int(item['start_pct'] * total_words),
                        int(item['end_pct'] * total_words)
                    ),
                    'estimated_timestamp': drop['timestamp_hint'],
                    'section_content_preview': item['section'].content[:50] + '...'
                })
                break

    return mapped_drops
```

**Why this works:**
- YouTube API provides retention at percentage points (0%, 5%, 10%...)
- Scripts have word counts per section
- Assumes ~150 words per minute speaking rate
- Maps percentage → word position → section boundary

**Limitations:**
- Assumes constant speaking rate (user may speak faster/slower in different sections)
- B-roll sections may have lower word density
- Opening/closing may have non-linear pacing
- **Good enough for diagnostic purposes** - user can see "drop in Section 3" and investigate

### Pattern 2: Root Cause Diagnosis with Pattern References
**What:** Diagnose WHY retention dropped by analyzing section content against known anti-patterns and suggesting fixes from voice pattern library.

**When to use:** After mapping retention drops to sections - provides actionable recommendations.

**Example:**
```python
# section_diagnostics.py
import json
from pathlib import Path

def load_voice_patterns():
    """Load voice patterns from STYLE-GUIDE.md Part 6."""
    # In practice, would parse markdown or load from structured JSON
    return {
        'causal_chains': {
            'pattern': 'Consequently, thereby, which meant that',
            'purpose': 'Show causation, not just sequence'
        },
        'intellectual_honesty': {
            'pattern': "That's fair. But...",
            'purpose': 'Concede valid points before rebutting'
        },
        'zero_impact': {
            'pattern': 'How many? Zero.',
            'purpose': 'Dramatic numerical reveals'
        },
        # ... 19 more patterns from STYLE-GUIDE.md Part 6
    }

def diagnose_section_drop(section_text: str, drop_magnitude: float) -> dict:
    """
    Diagnose why viewers dropped off in this section.

    Returns:
        {
            'root_causes': ['Abstract opening', 'No causal chain'],
            'recommendations': [
                'Start section with concrete date/place/document (see STYLE-GUIDE.md Part 3)',
                'Add causal chain pattern: "which meant that" (see Part 6 Pattern 3)'
            ],
            'pattern_references': ['causal_chains', 'concrete_openings']
        }
    """
    patterns = load_voice_patterns()
    root_causes = []
    recommendations = []
    pattern_refs = []

    # Check for common anti-patterns
    if section_text[:50].lower().startswith(('the concept', 'the idea', 'to understand')):
        root_causes.append('Abstract opening - no concrete anchor')
        recommendations.append(
            'Start with concrete date/place/document instead of abstraction '
            '(see STYLE-GUIDE.md Part 3 Rule 6)'
        )
        pattern_refs.append('concrete_openings')

    if 'consequently' not in section_text.lower() and 'thereby' not in section_text.lower():
        root_causes.append('Missing causal chain - sequence without causation')
        recommendations.append(
            f"Add causal chain: {patterns['causal_chains']['pattern']} "
            f"(see STYLE-GUIDE.md Part 6 Pattern 3)"
        )
        pattern_refs.append('causal_chains')

    if drop_magnitude > 0.10:  # Major drop (>10%)
        root_causes.append('Major engagement loss - likely pacing issue')
        recommendations.append(
            'Consider adding pattern interrupt: rhetorical question, '
            'document reveal, or zero-impact moment '
            '(see STYLE-GUIDE.md Part 6 Patterns 8, 15)'
        )
        pattern_refs.append('pattern_interrupts')

    return {
        'root_causes': root_causes,
        'recommendations': recommendations,
        'pattern_references': pattern_refs,
        'severity': 'HIGH' if drop_magnitude > 0.10 else 'MEDIUM'
    }
```

**Why this works:**
- References actual voice patterns user already documented
- Provides specific line-level guidance ("add causal chain here")
- Points to exact STYLE-GUIDE.md section for reference
- Uses severity levels to prioritize fixes

### Pattern 3: Pre-Script Insight Surfacing
**What:** Before `/script` generation, automatically surface relevant past performance insights for this topic type.

**When to use:** At start of `/script` command execution - before gathering requirements.

**Example:**
```python
# Extension to feedback_queries.py
def get_insights_for_script_prep(topic_type: str, limit: int = 5) -> dict:
    """
    Get pre-script insights for a topic type.

    Surfaces retention lessons and voice pattern usage from past videos.

    Args:
        topic_type: 'territorial', 'ideological', 'colonial', 'legal', 'general'
        limit: Max number of past videos to reference

    Returns:
        {
            'topic_type': 'territorial',
            'past_video_count': 3,
            'retention_lessons': [
                {
                    'lesson': 'Territorial videos lost viewers during treaty text sections',
                    'recommendation': 'Show treaty on screen, don\'t read aloud',
                    'source_video': 'Bir Tawil (2025-01-15)'
                }
            ],
            'voice_pattern_successes': [
                {
                    'pattern': 'zero_impact',
                    'usage': 'Used in 3/3 territorial videos',
                    'correlation': 'Higher retention in sections with zero-impact'
                }
            ],
            'display_summary': 'Based on 3 territorial videos...'
        }
    """
    # Query feedback table for past videos matching topic_type
    db = KeywordDB()
    feedback = db.get_topic_feedback(topic_type, limit=limit)

    # Aggregate retention lessons
    retention_lessons = []
    for video in feedback:
        if video.get('drop_points'):
            biggest_drop = max(video['drop_points'], key=lambda d: d['magnitude'])
            retention_lessons.append({
                'lesson': f"Lost {biggest_drop['magnitude']*100:.0f}% viewers at {biggest_drop['section']}",
                'recommendation': biggest_drop.get('diagnosis', {}).get('recommendations', ['Review section'])[0],
                'source_video': f"{video['title']} ({video['published_date']})"
            })

    # Aggregate pattern successes
    # (Would require pattern usage tracking - Phase 33 scope)
    pattern_successes = []

    db.close()

    return {
        'topic_type': topic_type,
        'past_video_count': len(feedback),
        'retention_lessons': retention_lessons,
        'voice_pattern_successes': pattern_successes,
        'display_summary': f"Based on {len(feedback)} {topic_type} videos..."
    }
```

**Integration point:** `/script` command calls this BEFORE asking user for topic details.

### Pattern 4: Topic Strategy Aggregation
**What:** Aggregate performance across topic types to show which formats work best with concrete next steps.

**When to use:** When user requests topic recommendations or performance analysis.

**Example:**
```python
# topic_strategy.py
from database import KeywordDB

def generate_topic_strategy_report() -> dict:
    """
    Aggregate performance by topic type and generate recommendations.

    Returns:
        {
            'best_performing_topics': [
                {
                    'topic': 'territorial',
                    'avg_retention': 0.34,
                    'avg_conversion': 0.42,
                    'video_count': 5,
                    'recommendation': 'Double down on territorial disputes - 34% retention, 0.42% conversion'
                }
            ],
            'worst_performing_topics': [...],
            'concrete_next_steps': [
                'Prioritize territorial disputes in research pipeline',
                'Apply territorial voice patterns (zero-impact, treaty display) to legal videos'
            ],
            'pipeline_suggestions': [
                {'topic': 'Bir Tawil follow-up', 'reasoning': 'Territorial + high past performance'}
            ]
        }
    """
    db = KeywordDB()

    # Query all video performance
    all_videos = db.get_all_video_performance(limit=500)

    # Group by topic_type
    by_topic = {}
    for video in all_videos:
        topic = video.get('topic_type', 'general')
        if topic not in by_topic:
            by_topic[topic] = []
        by_topic[topic].append(video)

    # Calculate averages
    topic_stats = []
    for topic, videos in by_topic.items():
        avg_retention = sum(v.get('avg_retention', 0) for v in videos) / len(videos)
        avg_conversion = sum(v.get('conversion_rate', 0) for v in videos) / len(videos)
        topic_stats.append({
            'topic': topic,
            'avg_retention': avg_retention,
            'avg_conversion': avg_conversion,
            'video_count': len(videos),
            'recommendation': f"{'Double down' if avg_retention > 0.30 else 'Reconsider'} on {topic} - {avg_retention*100:.0f}% retention, {avg_conversion:.2f}% conversion"
        })

    # Sort by performance
    topic_stats.sort(key=lambda t: t['avg_retention'], reverse=True)

    best = topic_stats[:2]
    worst = topic_stats[-2:]

    # Generate concrete next steps
    next_steps = []
    if best:
        next_steps.append(f"Prioritize {best[0]['topic']} disputes in research pipeline")
        next_steps.append(f"Apply {best[0]['topic']} voice patterns to other topics")

    db.close()

    return {
        'best_performing_topics': best,
        'worst_performing_topics': worst,
        'concrete_next_steps': next_steps,
        'pipeline_suggestions': []  # Would integrate with /discover suggestions
    }
```

### Anti-Patterns to Avoid

- **Don't hand-roll retention curve parsing:** Use existing `retention.py` - it already handles API pagination, error handling, and data formatting
- **Don't create new feedback storage tables:** Extend existing `video_feedback` table from Phase 31 - adding structured JSON for section-level diagnoses
- **Don't try to get per-section retention from YouTube API:** API only provides percentage-based curve - word-count mapping is the correct approach
- **Don't ignore existing voice pattern library:** STYLE-GUIDE.md Part 6 has 22 documented patterns - reference these in diagnostics instead of creating new terminology
- **Don't make recommendations generic:** "Improve retention" is useless - "Add causal chain at line 47: 'which meant that...'" is actionable

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| YouTube retention API integration | Custom OAuth + HTTP client | Existing `retention.py` | Already handles auth, error handling, pagination |
| Script section parsing | Regex markdown parser | Existing `parser.py` (ScriptParser class) | Handles frontmatter, H2 detection, word counts, marker exclusion |
| Feedback storage | New database schema | Extend `video_feedback` table (Phase 31) | Already has video_id, observations, actionable fields |
| Voice pattern reference | Custom pattern documentation | STYLE-GUIDE.md Part 6 (22 patterns) | Already documented, user-approved, referenced in workflows |
| Topic classification | New ML classifier | Existing TAG_VOCABULARY in `performance.py` | Simple keyword matching sufficient for 7 topic types |

**Key insight:** Phase 35 is an INTEGRATION phase, not a BUILD phase. The components exist - retention fetching, script parsing, feedback storage, pattern library. Phase 35's value is connecting them into actionable workflows.

## Common Pitfalls

### Pitfall 1: Assuming YouTube API Provides Per-Section Retention
**What goes wrong:** You try to fetch "retention at timestamp 3:45" directly from YouTube Analytics API.

**Why it happens:** YouTube Studio UI shows retention graph with time-based X-axis, so developers assume API returns timestamps.

**How to avoid:**
- YouTube Analytics API returns `elapsedVideoTimeRatio` (0.0-1.0), NOT timestamps
- Always map percentage → word count → section
- Accept ~15 second granularity (can't pinpoint exact sentence)

**Warning signs:**
- API calls with `dimensions='timestamp'` fail
- Trying to fetch "retention at 3:45" returns errors
- Documentation says "elapsedVideoTimeRatio" but code uses "timestamp"

### Pitfall 2: Over-Engineering Causation Detection
**What goes wrong:** Building ML classifier to detect why retention dropped instead of using heuristics.

**Why it happens:** Desire for "perfect" root cause analysis.

**How to avoid:**
- Start with simple pattern matching (is section opening abstract? is causal chain present?)
- Reference existing STYLE-GUIDE.md rules as diagnostic criteria
- Accept that user will review recommendations - doesn't need to be 100% accurate
- **Good enough is better than perfect** - user wants actionable suggestions, not research paper

**Warning signs:**
- Adding NLP libraries for sentiment analysis
- Training models on past video transcripts
- Spending >2 days on diagnostic logic

### Pitfall 3: Creating Insights That Don't Surface Proactively
**What goes wrong:** Building great analytics reports that sit unused because they require manual lookup.

**Why it happens:** Focusing on report generation without integrating into production workflow.

**How to avoid:**
- ACTN-04 requirement: insights MUST surface before `/script` generation
- Modify `/script` command to call `get_insights_for_script_prep()` automatically
- Display insights at TOP of response before gathering requirements
- Make insights OPT-OUT, not OPT-IN

**Warning signs:**
- User must remember to run separate command to see insights
- Insights only appear in POST-PUBLISH-ANALYSIS.md
- No integration with `/script` command

### Pitfall 4: Generic Recommendations Without Line Numbers
**What goes wrong:** Diagnostic says "Add causal chain" without specifying where.

**Why it happens:** Analyzing section as whole instead of identifying specific insertion points.

**How to avoid:**
- Parse section content for logical insertion points (after definitions, before examples)
- Reference specific sentences: "After line 23 ('The treaty defined borders'), add: 'which meant that...'"
- Include 20-word context window so user knows exact location
- Provide BEFORE/AFTER examples when possible

**Warning signs:**
- Recommendations say "improve section" without specifics
- User asks "where should I add this?"
- No line numbers or content quotes in diagnostics

### Pitfall 5: Empty Patterns Syndrome
**What goes wrong:** With only ~15 videos, statistical patterns may be unreliable.

**Why it happens:** Small sample size + high variance in topics.

**How to avoid:**
- Flag low-confidence insights when sample size < 3 videos for topic type
- Combine similar topics (territorial + legal = "document-heavy")
- Focus on QUALITATIVE patterns (what worked once) not STATISTICAL (what works 80% of time)
- Be honest: "Based on 2 territorial videos (low confidence)"

**Warning signs:**
- Insights claim "X always causes Y" with n=2
- Contradictory recommendations from different videos
- No sample size warnings in output

## Code Examples

Verified patterns from existing codebase:

### Retention Drop Detection (Existing Pattern)
```python
# From tools/youtube-analytics/retention.py (lines 134-176)
def find_drop_off_points(data_points, threshold=0.05):
    """
    Identify significant drop-off points in retention curve.

    A drop-off occurs when retention decreases by more than the threshold
    between consecutive data points.
    """
    drop_offs = []

    if len(data_points) < 2:
        return drop_offs

    for i in range(1, len(data_points)):
        prev = data_points[i - 1]
        curr = data_points[i]

        # Calculate delta (negative means viewers left)
        delta = curr["retention"] - prev["retention"]

        # Flag if drop exceeds threshold
        if delta < -threshold:
            drop_offs.append({
                "position": curr["position"],
                "retention_before": prev["retention"],
                "retention_after": curr["retention"],
                "drop": abs(delta),
                "timestamp_hint": _get_position_hint(curr["position"])
            })

    return drop_offs
```

**Usage:** This pattern is already production-ready. Phase 35 extends it by mapping `position` to script sections.

### Script Section Parsing (Existing Pattern)
```python
# From tools/production/parser.py (lines 162-180)
class ScriptParser:
    """Parses markdown script files into structured sections."""

    def parse_file(self, path: Path) -> List[Section]:
        """
        Parse a script file into sections.

        Returns:
            List of Section objects with:
            - heading: H2 heading text
            - content: Full text content
            - word_count: Spoken words only (excludes markers)
            - start_line: Line number
            - section_type: 'intro', 'body', 'conclusion'
        """
        path = Path(path)
        text = path.read_text(encoding='utf-8')
        return self.parse_text(text)
```

**Usage:** Already handles H2 detection, word counting (excluding B-roll markers), and section type inference. Phase 35 uses this to calculate section boundaries.

### Feedback Storage (Existing Pattern)
```python
# From tools/discovery/database.py (Phase 31)
class KeywordDB:
    def store_video_feedback(self, video_id: str, feedback: dict) -> dict:
        """
        Store feedback insights from POST-PUBLISH-ANALYSIS.md

        Args:
            feedback: {
                'biggest_drop_position': float,  # 0.0-1.0
                'observations': [str],
                'actionable': [str],
                'discovery': dict
            }

        Returns:
            {'status': 'inserted'/'updated', 'video_id': str}
        """
        # Existing implementation stores feedback
        # Phase 35 extends to include section-level diagnoses
```

**Usage:** Already stores video-level insights. Phase 35 extends schema to include section-level drop analysis.

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Post-mortem analytics reports | Proactive insight surfacing before creation | Phase 31 (feedback loop) + Phase 35 (pre-script) | Prevents repeating mistakes instead of documenting them |
| Generic "improve retention" advice | Section-specific recommendations with pattern references | Phase 33 (voice patterns) + Phase 35 (diagnostics) | Actionable at line level, not video level |
| Manual correlation of retention → script | Automated retention-to-section mapping | Phase 35 | Saves 30+ minutes per video analysis |
| Separate analytics + production workflows | Integrated feedback into production commands | Phase 31 foundations + Phase 35 integration | Insights surface where they're needed, not buried in reports |

**Deprecated/outdated:**
- **Manual retention spreadsheets:** Replaced by automated retention.py + mapper
- **Generic analytics dashboards:** Replaced by actionable diagnostics with script context
- **Post-publish-only analysis:** Replaced by pre-script insight surfacing

## Open Questions

1. **Word-count timing accuracy**
   - What we know: User speaks ~150 words/minute average, but varies by section
   - What's unclear: Should we use fixed rate or try to estimate per-section rates?
   - Recommendation: Start with fixed 150 WPM, add variance later if user feedback indicates major inaccuracy

2. **Voice pattern usage tracking**
   - What we know: STYLE-GUIDE.md Part 6 documents 22 patterns
   - What's unclear: Should Phase 35 track which patterns were used in each section of past scripts?
   - Recommendation: Defer to Phase 33 (voice pattern library implementation) - Phase 35 references patterns, Phase 33 tracks usage

3. **Confidence thresholds for small datasets**
   - What we know: ~15 videos published, variable topics
   - What's unclear: At what sample size do topic-level insights become reliable?
   - Recommendation: Flag insights as "low confidence" when n < 3 videos, combine similar topics when possible

4. **Integration timing with /script command**
   - What we know: Need to surface insights BEFORE gathering requirements
   - What's unclear: Should insights be mandatory display or can user skip if irrelevant?
   - Recommendation: Always display if available (automatic), but keep brief (3-5 bullet points max)

## Sources

### Primary (HIGH confidence)
- Existing codebase analysis:
  - `tools/youtube-analytics/retention.py` - Retention curve fetching (verified functional)
  - `tools/youtube-analytics/analyze.py` - Post-publish orchestration (verified functional)
  - `tools/youtube-analytics/feedback.py` - Feedback storage (Phase 31, verified functional)
  - `tools/production/parser.py` - Script section parsing (verified functional)
  - `.claude/REFERENCE/STYLE-GUIDE.md` - Voice pattern library documentation (22 patterns)
  - `.claude/commands/analyze.md` - Current `/analyze` command specification
  - `.claude/commands/script.md` - Current `/script` command specification

### Secondary (MEDIUM confidence)
- Web research (2026 trends):
  - [YouTube Audience Retention 2026 Guide](https://socialrails.com/blog/youtube-audience-retention-complete-guide) - First 30 seconds critical, retention determines ranking
  - [YouTube Retention Graphs Explained](https://www.opus.pro/blog/youtube-retention-graphs-explained) - Pattern detection methodology
  - [Google Analytics Actionable Insights 2026](https://almcorp.com/blog/google-analytics-actionable-insights-complete-guide-2026/) - Actionable vs descriptive analytics
  - [Customer Retention Analytics Guide](https://www.sarasanalytics.com/blog/customer-retention-analytics) - Root cause analysis patterns

### Tertiary (LOW confidence)
- Phase 35 requirements document - Goals and success criteria (project-specific, not externally verified)

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - Uses existing project dependencies, no new libraries needed
- Architecture: HIGH - Extends proven patterns from Phases 8-31, follows existing conventions
- Pitfalls: HIGH - Based on YouTube API documentation limitations and small dataset realities

**Research date:** 2026-02-11
**Valid until:** 60 days (stable domain - YouTube Analytics API changes infrequently, retention analysis patterns mature)

---

## Key Takeaways for Planning

1. **Don't rebuild existing tools** - retention.py, parser.py, feedback storage all exist and work
2. **Integration > Innovation** - Phase 35's value is connecting pieces, not creating new infrastructure
3. **Actionable = Specific** - "Add causal chain at line 47" not "improve section"
4. **Proactive > Reactive** - Surface insights BEFORE script generation (ACTN-04 critical requirement)
5. **Accept limitations** - Word-count timing is approximate, small dataset means low confidence for some insights
6. **Reference existing patterns** - STYLE-GUIDE.md Part 6 is authoritative, diagnostics should point to it

**Planning priority:** Focus on retention_mapper.py (core integration piece) and section_diagnostics.py (actionable recommendations). Extend existing files rather than creating parallel systems.
