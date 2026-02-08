# Phase 31: Feedback Loop Integration - Research

**Researched:** 2026-02-08
**Domain:** Feedback loop systems, markdown parsing, pattern extraction, recommendation engines
**Confidence:** HIGH

## Summary

Phase 31 implements a feedback loop system that automatically surfaces past performance insights during content creation. The system parses POST-PUBLISH-ANALYSIS markdown files, stores structured data in the existing Phase 27 database schema, and provides query interfaces for retrieving relevant insights. The core challenge is extracting semi-structured data from markdown files with varying formats and matching insights to current work contexts.

The technical implementation spans three areas: (1) markdown parsing using regex patterns for extraction (appropriate for known-structure documents with heuristic fallbacks), (2) database storage using existing section_feedback table and video_performance feedback columns, and (3) insight retrieval using topic-based matching with keyword similarity as secondary signal.

**Primary recommendation:** Use regex-based extraction for POST-PUBLISH-ANALYSIS parsing (known structure, controlled template) with graceful degradation for older files. Extend existing pattern_extractor.py functions for pattern comparison. Follow FEEDBACK_AVAILABLE flag pattern from Phase 29/30 for graceful imports.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

**Parsing Strategy:**
- Best-effort parsing for existing analysis files (regex/heuristic matching for known fields)
- Create canonical template for all future POST-PUBLISH-ANALYSIS files (consistent structure improves parsing over time)
- Extract both numeric metrics (CTR, retention rate, drop points, views, subscriber conversion) AND qualitative insights (what worked, what failed, lessons learned)
- Auto-parse when /analyze generates a new analysis file
- Backfill command to import all existing analysis files at once (`python feedback.py backfill`)

**Insight Surfacing:**
- Automatic preamble before script/prep/publish generation: show 3-5 relevant insights from past videos
- Matching strategy: category-specific insights first (by topic type), then 1-2 universal insights that apply to all videos (e.g., pacing patterns, engagement hooks)
- Keyword/entity similarity as secondary matching signal (overlapping entities between current topic and past videos)
- Surface insights during ALL creation commands: /script, /prep, and /publish — each gets category-appropriate insights
  - /script: content and pacing insights (retention drops, section structure, hook effectiveness)
  - /prep: production insights (B-roll density, edit pacing, visual evidence patterns)
  - /publish: CTR and title insights (which title formulas worked, thumbnail styles, metadata patterns)

**Pattern Extraction:**
- Compare both content attributes (topic type, angle, script length, entity density, section count) AND production attributes (thumbnail style, title formula, video length, pacing score, B-roll density)
- Store patterns in both database (for querying during /script) and markdown report (for human review)
- Database records for machine-readable querying, PATTERNS.md for browsable human review

**Query Interface:**
- Standalone CLI for power queries: `python feedback.py query --topic territorial --metric retention`
- Extend /patterns command with feedback data (aggregated insights view)
- Output: default table format for terminal, --markdown flag for full report (matches existing tool patterns like benchmarks.py)
- Query by individual video (`--video VIDEO_ID`) OR by category (`--topic territorial`) with different output for each

### Claude's Discretion

- Storage location: Claude picks best approach (likely extend keywords.db given Phase 27 section_feedback table already exists)
- Insight depth: Claude decides balance of numbers vs. qualitative based on available data
- Performance threshold: Claude determines what counts as "high-performing" (likely top quartile or above-average, adapting to ~10 video catalog)
- Pattern extraction trigger: Claude determines optimal timing (after each /analyze vs. periodic)
- Comparison views: Claude picks most useful presentation for query results (side-by-side vs. list)

### Deferred Ideas (OUT OF SCOPE)

None — discussion stayed within phase scope

</user_constraints>

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| sqlite3 | stdlib | Database storage | Already used in Phase 27, zero dependencies |
| re | stdlib | Regex parsing | Standard library, sufficient for known-structure markdown |
| pathlib | stdlib | File operations | Standard library path handling |
| json | stdlib | Store qualitative insights | Already used for discovery_issues/lessons_learned columns |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| datetime | stdlib | Timestamp tracking | Parse dates from analysis files |
| statistics | stdlib | Calculate averages/medians | Aggregate metrics across videos |
| typing | stdlib | Type hints | Function signatures |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| regex | markdown-it-py parser | Adds external dependency; overkill for controlled template format |
| regex | mistletoe parser | Spec-compliant but heavyweight for simple extraction |
| sqlite3 | pandas DataFrame | Would require pandas dependency; database better for incremental updates |

**Installation:**
```bash
# No additional dependencies needed - all stdlib
```

## Architecture Patterns

### Recommended Module Structure
```
tools/youtube-analytics/
├── feedback.py              # Main orchestrator (NEW)
├── feedback_parser.py       # Markdown extraction (NEW)
├── feedback_queries.py      # Query interface (NEW)
├── analyze.py               # Modified to call parser
├── pattern_extractor.py     # Modified to include feedback
└── benchmarks.py            # Reference for CLI patterns
```

### Pattern 1: Graceful Import with Availability Flag
**What:** Module uses try/except to import feedback functionality, sets FEEDBACK_AVAILABLE flag
**When to use:** Any file that wants to optionally use feedback data without hard dependency
**Example:**
```python
# From analyze.py (existing pattern)
try:
    from feedback_parser import parse_analysis_file, store_feedback
    FEEDBACK_AVAILABLE = True
except ImportError:
    FEEDBACK_AVAILABLE = False

# Later in code
if FEEDBACK_AVAILABLE:
    store_feedback(analysis_data)
```

### Pattern 2: Best-Effort Regex Extraction
**What:** Parse markdown with known structure, use regex with fallbacks for older formats
**When to use:** Extracting data from POST-PUBLISH-ANALYSIS files
**Example:**
```python
# Extract retention from analysis markdown
retention_match = re.search(r'\*\*Average retention:\*\* ([\d.]+)%', content)
if retention_match:
    avg_retention = float(retention_match.group(1))
else:
    # Fallback: try older format or set None
    avg_retention = None
```

### Pattern 3: Database CRUD with Error Dict Pattern
**What:** All database methods return dicts with results or {'error': msg}
**When to use:** All KeywordDB methods (existing pattern from Phase 16)
**Example:**
```python
def store_video_feedback(self, video_id: str, feedback_data: dict) -> dict:
    """Store parsed feedback for a video."""
    try:
        cursor = self._conn.cursor()
        cursor.execute("""
            UPDATE video_performance
            SET retention_drop_point = ?,
                discovery_issues = ?,
                lessons_learned = ?
            WHERE video_id = ?
        """, (
            feedback_data.get('drop_point'),
            json.dumps(feedback_data.get('discovery_issues', [])),
            json.dumps(feedback_data.get('lessons_learned', [])),
            video_id
        ))
        self._conn.commit()
        return {'success': True, 'video_id': video_id}
    except sqlite3.Error as e:
        return {'error': f'Failed to store feedback: {e}'}
```

### Pattern 4: Topic-Based Insight Matching
**What:** Query database for videos in same topic_type, return top insights sorted by relevance
**When to use:** Surfacing insights before /script, /prep, /publish
**Example:**
```python
def get_relevant_insights(self, topic_type: str, limit: int = 5) -> dict:
    """Get insights from past videos in same topic category."""
    try:
        cursor = self._conn.cursor()
        cursor.execute("""
            SELECT video_id, title, lessons_learned, conversion_rate
            FROM video_performance
            WHERE topic_type = ? AND lessons_learned IS NOT NULL
            ORDER BY conversion_rate DESC
            LIMIT ?
        """, (topic_type, limit))

        rows = cursor.fetchall()
        insights = []
        for row in rows:
            lessons = json.loads(row[2]) if row[2] else []
            insights.append({
                'video_id': row[0],
                'title': row[1],
                'lessons': lessons,
                'conversion': row[3]
            })

        return {'insights': insights, 'count': len(insights)}
    except sqlite3.Error as e:
        return {'error': f'Query failed: {e}'}
```

### Anti-Patterns to Avoid
- **Over-parsing:** Don't try to extract every field perfectly. Use heuristics for older files, require canonical format for new ones.
- **Complex AST parsing:** Markdown parsers with full AST are overkill for known-structure extraction. Regex is appropriate here.
- **Synchronous bulk parsing:** Backfill command should process files incrementally with progress output, not all-at-once.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Markdown parsing (complex) | Custom recursive descent parser | markdown-it-py or mistletoe | Handle edge cases (nested structures, escaping) |
| Text similarity | Custom string distance algorithm | Existing keyword matching from Phase 16 | Already have entity extraction |
| Performance thresholds | Hardcoded percentiles | statistics.quantiles() | Adapts to catalog size |
| CLI argument parsing | Manual sys.argv parsing | argparse (used in benchmarks.py) | Consistent with existing tools |

**Key insight:** For controlled-format markdown (POST-PUBLISH-ANALYSIS), regex extraction is simpler and more maintainable than full markdown parsing. For arbitrary markdown, use a library.

## Common Pitfalls

### Pitfall 1: Assuming Consistent Markdown Format
**What goes wrong:** Older POST-PUBLISH-ANALYSIS files may have different section names, ordering, or formatting
**Why it happens:** analyze.py template evolved over time
**How to avoid:** Use heuristic fallbacks. Search for patterns like `retention.*(\d+\.?\d*)%` instead of exact strings
**Warning signs:** Parser returns None for fields that visually exist in markdown

### Pitfall 2: JSON Column Null Handling
**What goes wrong:** Reading JSON from database returns None for null values, breaking json.loads()
**Why it happens:** SQLite NULL is different from JSON null
**How to avoid:** Always check `if column_value is not None` before `json.loads(column_value)`
**Warning signs:** TypeError: the JSON object must be str, bytes or bytearray, not NoneType

### Pitfall 3: Performance Threshold Brittleness
**What goes wrong:** Hardcoded "top quartile" breaks when catalog has <4 videos
**Why it happens:** Assuming minimum catalog size
**How to avoid:** Use adaptive thresholds: `quantiles([0.75])` with try/except, fall back to above-average
**Warning signs:** StatisticsError: must have at least four data points

### Pitfall 4: Stale Insight Attribution
**What goes wrong:** Surfaced insights reference deleted or moved video projects
**Why it happens:** Video folders get archived, renamed, or deleted
**How to avoid:** Include video_id and title in insight display, not just folder paths
**Warning signs:** User sees insight but can't find referenced video

### Pitfall 5: Over-Matching Insights
**What goes wrong:** Every video gets same generic insights ("improve retention")
**Why it happens:** Too broad matching (all videos vs. topic-specific)
**How to avoid:** Prioritize topic_type match first, then keyword overlap, limit to 3-5 insights
**Warning signs:** User feedback that insights aren't helpful

## Code Examples

Verified patterns from existing codebase:

### Parsing POST-PUBLISH-ANALYSIS Markdown
```python
# Source: analyze.py format_analysis_markdown() shows output structure
def parse_analysis_markdown(filepath: str) -> dict:
    """
    Parse POST-PUBLISH-ANALYSIS markdown file into structured data.

    Extracts:
    - video_id from header
    - numeric metrics (retention, CTR, views)
    - qualitative insights (observations, actionable items)
    - drop-off points

    Returns dict with extracted fields or {'error': msg}
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract video ID
        video_id_match = re.search(r'\*\*Video ID:\*\* (\w+)', content)
        video_id = video_id_match.group(1) if video_id_match else None

        # Extract retention metrics
        avg_ret_match = re.search(r'\*\*Average retention:\*\* ([\d.]+)%', content)
        avg_retention = float(avg_ret_match.group(1)) if avg_ret_match else None

        # Extract CTR if available
        ctr_match = re.search(r'\*\*CTR:\*\* ([\d.]+)%', content)
        ctr = float(ctr_match.group(1)) if ctr_match else None

        # Extract lessons (observations and actionable items)
        observations = []
        obs_section = re.search(r'### Observations\n\n(.*?)\n\n', content, re.DOTALL)
        if obs_section:
            obs_lines = obs_section.group(1).split('\n')
            observations = [line.strip('- ').strip() for line in obs_lines if line.strip()]

        actionable = []
        action_section = re.search(r'### Actionable Items\n\n(.*?)\n\n', content, re.DOTALL)
        if action_section:
            action_lines = action_section.group(1).split('\n')
            actionable = [line.strip('- [ ] ').strip() for line in action_lines if line.strip()]

        # Extract drop-off point (first/biggest)
        drop_match = re.search(r'\| (\d+)% \| ([\d.]+)% dropped', content)
        drop_point = int(drop_match.group(1)) if drop_match else None

        return {
            'video_id': video_id,
            'avg_retention': avg_retention,
            'ctr': ctr,
            'observations': observations,
            'actionable': actionable,
            'drop_point': drop_point,
            'parsed_at': datetime.utcnow().isoformat()
        }

    except Exception as e:
        return {'error': f'Parse failed: {e}', 'filepath': filepath}
```

### Storing Feedback in Database
```python
# Source: Phase 27 schema (video_performance feedback columns)
def store_video_feedback(self, video_id: str, feedback_data: dict) -> dict:
    """
    Store parsed feedback in video_performance table.

    Args:
        video_id: YouTube video ID
        feedback_data: Dict from parse_analysis_markdown()

    Returns:
        {'success': True} or {'error': msg}
    """
    try:
        cursor = self._conn.cursor()

        # Prepare JSON fields
        discovery_issues = feedback_data.get('discovery_issues', [])
        lessons = {
            'observations': feedback_data.get('observations', []),
            'actionable': feedback_data.get('actionable', [])
        }

        cursor.execute("""
            UPDATE video_performance
            SET retention_drop_point = ?,
                discovery_issues = ?,
                lessons_learned = ?
            WHERE video_id = ?
        """, (
            feedback_data.get('drop_point'),
            json.dumps(discovery_issues) if discovery_issues else None,
            json.dumps(lessons),
            video_id
        ))

        self._conn.commit()

        if cursor.rowcount == 0:
            return {'error': f'No video_performance record found for {video_id}'}

        return {'success': True, 'video_id': video_id}

    except sqlite3.Error as e:
        return {'error': f'Database error: {e}'}
```

### Retrieving Relevant Insights
```python
# Source: Combining pattern_extractor.py aggregation with topic filtering
def get_insights_for_topic(self, topic_type: str, limit: int = 5) -> dict:
    """
    Retrieve insights from high-performing videos in same topic category.

    Args:
        topic_type: Topic category ('territorial', 'ideological', etc.)
        limit: Max number of insights to return

    Returns:
        {'insights': [...], 'count': N} or {'error': msg}
    """
    try:
        cursor = self._conn.cursor()

        # Get performance threshold (above average for topic)
        cursor.execute("""
            SELECT AVG(conversion_rate)
            FROM video_performance
            WHERE topic_type = ? AND conversion_rate IS NOT NULL
        """, (topic_type,))

        row = cursor.fetchone()
        threshold = row[0] if row and row[0] else 0

        # Fetch videos above threshold with feedback
        cursor.execute("""
            SELECT
                video_id,
                title,
                lessons_learned,
                conversion_rate,
                retention_drop_point
            FROM video_performance
            WHERE topic_type = ?
                AND lessons_learned IS NOT NULL
                AND conversion_rate >= ?
            ORDER BY conversion_rate DESC
            LIMIT ?
        """, (topic_type, threshold, limit))

        rows = cursor.fetchall()
        insights = []

        for row in rows:
            lessons = json.loads(row[2]) if row[2] else {'observations': [], 'actionable': []}
            insights.append({
                'video_id': row[0],
                'title': row[1][:60],  # Truncate for display
                'observations': lessons.get('observations', []),
                'actionable': lessons.get('actionable', []),
                'conversion': row[3],
                'drop_point': row[4]
            })

        return {
            'insights': insights,
            'count': len(insights),
            'topic': topic_type,
            'threshold': threshold
        }

    except sqlite3.Error as e:
        return {'error': f'Query failed: {e}'}
```

### CLI Query Interface
```python
# Source: benchmarks.py CLI pattern (argparse with subcommands)
def main():
    """CLI entry point for feedback queries."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Query feedback insights from past video performance',
        epilog="""
Examples:
  python feedback.py backfill               Import all analysis files
  python feedback.py query --topic territorial  Show territorial insights
  python feedback.py query --video VIDEO_ID    Show specific video feedback
  python feedback.py patterns --markdown    Generate patterns report
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Command to run')

    # Backfill command
    backfill_parser = subparsers.add_parser('backfill', help='Parse all analysis files')
    backfill_parser.add_argument('--force', action='store_true', help='Re-parse existing records')

    # Query command
    query_parser = subparsers.add_parser('query', help='Query insights')
    query_parser.add_argument('--topic', help='Filter by topic type')
    query_parser.add_argument('--video', help='Get feedback for specific video')
    query_parser.add_argument('--metric', help='Filter by metric (retention, ctr)')
    query_parser.add_argument('--markdown', action='store_true', help='Output as markdown')

    # Patterns command
    patterns_parser = subparsers.add_parser('patterns', help='Generate patterns report')
    patterns_parser.add_argument('--markdown', action='store_true', help='Save as markdown')

    args = parser.parse_args()

    if args.command == 'backfill':
        result = backfill_analysis_files(force=args.force)
        print(f"Processed {result['processed']} files, {result['errors']} errors")

    elif args.command == 'query':
        if args.video:
            result = query_video_feedback(args.video)
        elif args.topic:
            result = query_topic_insights(args.topic, metric=args.metric)
        else:
            parser.error("Specify either --video or --topic")

        if args.markdown:
            print(format_query_markdown(result))
        else:
            print(format_query_terminal(result))

    elif args.command == 'patterns':
        result = generate_feedback_patterns()
        if args.markdown:
            save_patterns_markdown(result)
        else:
            print(format_patterns_terminal(result))

    else:
        parser.print_help()

if __name__ == '__main__':
    main()
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Manual review of past videos | Automated feedback loop | Phase 31 (2026) | Reduces research time, surfaces patterns |
| Insights in analyst's memory | Database-stored lessons | Phase 31 (2026) | Searchable, attributable insights |
| One-off analysis files | Structured feedback data | Phase 31 (2026) | Enables pattern extraction |

**Deprecated/outdated:**
- N/A (new functionality)

## Open Questions

1. **Should section_feedback table be populated?**
   - What we know: Phase 27 created the table for retention per section
   - What's unclear: POST-PUBLISH-ANALYSIS doesn't include per-section retention currently
   - Recommendation: Leave section_feedback empty for now. Future enhancement can add per-section extraction if analyze.py format changes.

2. **How to handle multi-variant attribution?**
   - What we know: Some videos have multiple thumbnail/title variants tested
   - What's unclear: Should insights attribute to specific variant or aggregate?
   - Recommendation: Store insights at video level (video_performance table), not variant level. Phase 30 benchmarks handle variant-specific CTR.

3. **What counts as "high-performing"?**
   - What we know: Small catalog (~10 videos) makes percentiles unreliable
   - What's unclear: Above-average vs top quartile vs absolute threshold
   - Recommendation: Use above-average for topic_type (adaptive), with fallback to above-channel-average if topic has <3 videos.

## Sources

### Primary (HIGH confidence)
- Phase 27 database schema (G:/History vs Hype/.planning/phases/27-database-foundation/27-01-PLAN.md) - Confirmed table structure
- Phase 30 benchmarks.py (G:/History vs Hype/tools/youtube-analytics/benchmarks.py) - CLI patterns, query structure
- Phase 20 pattern_extractor.py (G:/History vs Hype/tools/youtube-analytics/pattern_extractor.py) - Aggregation functions
- analyze.py (G:/History vs Hype/tools/youtube-analytics/analyze.py) - POST-PUBLISH-ANALYSIS format, FEEDBACK_AVAILABLE pattern

### Secondary (MEDIUM confidence)
- [Introducing Python's Parse: The Ultimate Alternative to Regular Expressions](https://towardsdatascience.com/introducing-pythons-parse-the-ultimate-alternative-to-regular-expressions-3ae07e51b753/) - Regex vs parser libraries
- [Building a python CLI tool to extract the TOC from markdown files](https://towardsdatascience.com/building-a-python-cli-tool-to-extract-the-toc-from-markdown-files-ab5a7b9d07f2/) - Markdown extraction patterns
- [Handling Feedback Loops in Recommender Systems](https://towardsdatascience.com/handling-feedback-loops-in-recommender-systems-deep-bayesian-bandits-e83f34e2566a/) - Feedback loop concepts

### Tertiary (LOW confidence)
- [mistletoe GitHub](https://github.com/miyuchina/mistletoe) - Alternative markdown parser (not recommended for this use case)
- [markdown-it-py GitHub](https://github.com/executablebooks/markdown-it-py) - CommonMark parser (heavyweight for controlled format)

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - All stdlib, verified in existing codebase
- Architecture: HIGH - Follows existing KeywordDB patterns, graceful import pattern from Phase 29/30
- Pitfalls: MEDIUM - Predicted based on similar parsing/database work, not observed in this specific context

**Research date:** 2026-02-08
**Valid until:** 90 days (stable domain - stdlib patterns don't change rapidly)
