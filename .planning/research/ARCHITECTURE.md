# Architecture Integration: v1.6 Click & Keep

**Domain:** YouTube Channel Analytics & Production Workflow Extension
**Researched:** 2026-02-06
**Confidence:** HIGH

---

## Executive Summary

**v1.6 Click & Keep integrates with existing architecture through data layer extensions, not major refactoring.**

The workspace already has:
- Analytics fetching (ctr.py, retention.py, performance.py)
- Database infrastructure (keywords.db with auto-migration pattern)
- Script quality checking (cli.py with checker orchestration)
- Production pipeline (parser.py with --package flag)

New features ADD capabilities to existing components:

1. **Thumbnail/Title A/B Tracking** → Extends `tools/discovery/database.py` schema + new `tools/youtube-analytics/thumbnail_tracker.py`
2. **Script Pacing Analysis** → Extends `tools/script-checkers/checkers/flow.py` + new pacing metrics module
3. **Post-Publish Feedback Loop** → New `tools/production/feedback_loader.py` + query integration in `/script` command
4. **Model Assignments Refresh** → Update YAML frontmatter in 13 `.claude/commands/*.md` files

**Build order:** Database schema first (enables parallel development), then trackers/analyzers, then feedback integration, finally model assignments.

---

## Current Architecture (v1.5 Baseline)

### System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     User Interface Layer                         │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  Slash Commands (.claude/commands/*.md)                    │  │
│  │  /research /script /verify /prep /analyze /patterns        │  │
│  └────────────────────────────────────────────────────────────┘  │
├─────────────────────────────────────────────────────────────────┤
│                     Application Layer                            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │  Discovery  │  │Script Check │  │ Production  │             │
│  │  (1800 LOC) │  │ (2600 LOC)  │  │  (800 LOC)  │             │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘             │
│         │                │                │                     │
│         │                │                │                     │
│  ┌──────┴────────────────┴────────────────┴──────┐             │
│  │  YouTube Analytics (7700 LOC)                 │             │
│  │  metrics.py, ctr.py, retention.py,            │             │
│  │  performance.py, pattern_extractor.py         │             │
│  └───────────────────────────────────────────────┘             │
├─────────────────────────────────────────────────────────────────┤
│                       Data Layer                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ keywords.db  │  │ Markdown     │  │  OAuth2      │          │
│  │ (SQLite)     │  │ Reports      │  │  token.json  │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
├─────────────────────────────────────────────────────────────────┤
│                    External Services                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ YouTube      │  │ YouTube      │  │  spaCy       │          │
│  │ Analytics v2 │  │ Data API v3  │  │  NLP Models  │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
```

### Component Responsibilities

| Component | Responsibility | Files |
|-----------|----------------|-------|
| **Slash Commands** | User-facing entry points, route to Python tools | `.claude/commands/*.md` (13 files) |
| **Discovery** | Keyword research, demand analysis, competition scoring | `tools/discovery/*.py` (14 files) |
| **Script Checkers** | Quality checks (stumble, scaffolding, repetition, flow) | `tools/script-checkers/*.py` (12 files) |
| **Production** | Script parsing, B-roll, edit guides, metadata | `tools/production/*.py` (6 files) |
| **YouTube Analytics** | Metrics fetching, retention analysis, pattern extraction | `tools/youtube-analytics/*.py` (11 files) |
| **Database** | Persistent storage, auto-migration schema | `tools/discovery/database.py` + `keywords.db` |
| **OAuth2** | YouTube API authentication | `credentials/token.json` managed by `auth.py` |

### Established Patterns

**1. Error Dict Pattern** (established v1.1)
```python
def fetch_data(video_id: str) -> Dict[str, Any]:
    try:
        # ... operation ...
        return {'status': 'ok', 'data': results}
    except Exception as e:
        return {'error': 'Failed to fetch', 'details': str(e)}
```
- **Used in:** All `tools/discovery/*.py`, `tools/youtube-analytics/*.py`
- **Why:** Graceful degradation, no exception propagation to CLI

**2. CLI + Python API Dual Interface** (established v1.2)
```python
def analyze_script(text: str, config: Config) -> Dict[str, Any]:
    # Core logic - callable from Python or CLI
    ...

def main():
    parser = argparse.ArgumentParser(...)
    # CLI wrapper around core function
```
- **Used in:** `cli.py`, `performance.py`, `competition.py`, all major modules
- **Why:** Supports both `/command` workflows and direct Python imports

**3. Auto-Migration Schema** (established v1.3)
```python
def _ensure_classification_columns(self):
    """Add Phase 16 columns if missing"""
    cursor = self._conn.cursor()
    cursor.execute("PRAGMA table_info(videos)")
    # Check if columns exist, add if missing
```
- **Used in:** `database.py` (`_ensure_*_columns` methods)
- **Why:** No manual migration scripts, zero-friction upgrades

**4. Lazy Loading for Optional Dependencies** (established v1.2)
```python
try:
    import spacy
    SPACY_AVAILABLE = True
except ImportError:
    SPACY_AVAILABLE = False
```
- **Used in:** `stumble.py`, `flow.py`, `performance.py`
- **Why:** Tools work without full dependency stack, graceful feature gates

**5. Markdown Report Output** (established v1.1)
```python
def generate_report(data: Dict) -> str:
    # Return markdown string
    return markdown_content

# Save to project folder
report_path = project_dir / 'POST-PUBLISH-ANALYSIS.md'
report_path.write_text(report, encoding='utf-8')
```
- **Used in:** `analyze.py`, `performance_report.py`, `pattern_extractor.py`
- **Why:** Human-readable, version-controllable, Claude-parseable

---

## v1.6 Architecture Extensions

### Feature 1: Thumbnail/Title A/B Tracking

**Integration Strategy:** Extend database schema + new tracking module + pattern analysis module

#### New Components

| Component | Purpose | LOC Estimate |
|-----------|---------|--------------|
| `tools/youtube-analytics/thumbnail_tracker.py` | Compute thumbnail hashes, store with CTR | ~200 LOC |
| `tools/youtube-analytics/thumbnail_patterns.py` | Cluster similar thumbnails, correlate CTR | ~300 LOC |
| Database schema extension | `thumbnail_variants` table in keywords.db | SQL migration |

#### Data Flow

```
1. User creates variants in Photoshop
   ├─ Thumbnail A.png
   ├─ Thumbnail B.png
   └─ Thumbnail C.png
        ↓
2. thumbnail_tracker.py computes perceptual hashes
   - average_hash (rough similarity, fast)
   - perceptual_hash (rotation/scale resistant)
   - difference_hash (edge detection)
        ↓
3. Store in thumbnail_variants table
   - video_id, variant_label ('A', 'B', 'C')
   - hash_avg, hash_phash, hash_dhash (16-char hex strings)
   - ctr_percent, impressions (from YouTube Analytics)
        ↓
4. ctr.py fetches CTR for video (EXISTING)
        ↓
5. thumbnail_patterns.py correlates hashes with CTR
   - Cluster by Hamming distance (similar thumbnails)
   - Report: "Map-focused (7 videos) avg 8.2% CTR"
```

#### Database Schema Extension

**New table: `thumbnail_variants`**
```sql
CREATE TABLE IF NOT EXISTS thumbnail_variants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    video_id TEXT NOT NULL,
    variant_label TEXT NOT NULL,  -- 'A', 'B', 'C'
    hash_avg TEXT,                 -- 16-char hex from average_hash
    hash_phash TEXT,               -- 16-char hex from perceptual_hash
    hash_dhash TEXT,               -- 16-char hex from difference_hash
    ctr_percent REAL,              -- From YouTube Analytics or manual entry
    impressions INTEGER,           -- From YouTube Analytics
    upload_date TEXT,              -- ISO 8601 timestamp
    thumbnail_path TEXT,           -- Relative path to image file
    is_active INTEGER DEFAULT 1,   -- Which variant is currently live
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(video_id, variant_label)
);

CREATE INDEX IF NOT EXISTS idx_thumbnail_video_id ON thumbnail_variants(video_id);
CREATE INDEX IF NOT EXISTS idx_thumbnail_active ON thumbnail_variants(is_active);
```

**Migration pattern (auto-runs on first import):**
```python
# In database.py
def _ensure_thumbnail_table(self):
    """Phase v1.6: Add thumbnail_variants table"""
    cursor = self._conn.cursor()
    cursor.execute("""
        SELECT name FROM sqlite_master
        WHERE type='table' AND name='thumbnail_variants'
    """)
    if cursor.fetchone() is None:
        # Execute CREATE TABLE SQL from above
        ...
```

#### Integration Points

**With existing `/analyze` command:**
```python
# In analyze.py (existing)
def analyze_video(video_id: str) -> Dict[str, Any]:
    # ... existing CTR fetch ...

    # NEW: Check for thumbnail variants
    from thumbnail_tracker import get_thumbnail_variants
    variants = get_thumbnail_variants(video_id)
    if variants:
        analysis['thumbnail_variants'] = variants
        analysis['thumbnail_recommendation'] = determine_best_variant(variants)
```

**With existing `/patterns` command:**
```python
# In patterns.py (existing)
def extract_patterns() -> Dict[str, Any]:
    # ... existing pattern extraction ...

    # NEW: Include thumbnail patterns
    from thumbnail_patterns import analyze_thumbnail_patterns
    patterns['thumbnail_patterns'] = analyze_thumbnail_patterns()
    # Returns: {'map_focused': {'count': 7, 'avg_ctr': 8.2}, ...}
```

#### CLI Entry Points

**New command: `/thumbnails` (optional convenience wrapper)**
```bash
# Track new thumbnail variant
python tools/youtube-analytics/thumbnail_tracker.py VIDEO_ID path/to/thumbnail.png --variant A

# Analyze patterns across all videos
python tools/youtube-analytics/thumbnail_patterns.py --report

# JSON output for programmatic use
python tools/youtube-analytics/thumbnail_patterns.py --json
```

**Integrated into existing `/analyze`:**
```bash
# Existing command automatically includes thumbnail analysis if variants exist
/analyze VIDEO_ID
```

---

### Feature 2: Script Pacing Analysis

**Integration Strategy:** Extend existing `flow.py` checker + new quantitative metrics module

#### New Components

| Component | Purpose | LOC Estimate |
|-----------|---------|--------------|
| `tools/script-checkers/checkers/pacing.py` | Quantitative pacing metrics (sentence variance, readability) | ~250 LOC |
| Extension to `cli.py` | Add `--pacing` flag | ~20 LOC |

#### Data Flow

```
1. User writes script → SCRIPT.md (EXISTING)
        ↓
2. parser.py extracts text (EXISTING)
        ↓
3. flow.py analyzes qualitatively (EXISTING)
   - Undefined terms
   - Abrupt transitions
        ↓
4. NEW: pacing.py analyzes quantitatively
   - Sentence length variance per 100-word window
   - Flesch Reading Ease delta between sections
   - Entity density per paragraph
        ↓
5. Output warnings in standard checker format
   [PACING WARNING: Lines 45-52 variance 18.3 > 15 - rushed delivery risk]
```

#### Pacing Metrics Implementation

```python
# tools/script-checkers/checkers/pacing.py

import spacy
import textstat
from typing import Dict, List, Any

def check_pacing(text: str, config: Config) -> Dict[str, Any]:
    """
    Detect pacing issues via quantitative metrics.

    Flags:
    - Sentence length variance > 15 (rushed delivery)
    - Flesch delta > 20 between sections (complexity spike)
    - Entity density > 0.4 per sentence (wall of nouns)

    Returns:
        {
            'issues': [
                {
                    'type': 'high_variance',
                    'severity': 'warning',
                    'line_start': 45,
                    'line_end': 52,
                    'variance': 18.3,
                    'message': 'Sentence rhythm inconsistent - may sound rushed'
                }
            ],
            'metrics': {
                'avg_sentence_length': 18.2,
                'sentence_variance': 12.1,
                'flesch_reading_ease': 62.3
            }
        }
    """
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)

    issues = []

    # 1. Sentence length variance per 100-word window
    windows = sliding_windows(doc, window_size=100)
    for window in windows:
        variance = calculate_sentence_variance(window)
        if variance > config.pacing_variance_threshold:  # Default: 15
            issues.append({
                'type': 'high_variance',
                'severity': 'warning',
                'line_start': window.start_line,
                'line_end': window.end_line,
                'variance': variance,
                'message': f'Sentence rhythm inconsistent (var={variance:.1f}) - may sound rushed'
            })

    # 2. Flesch Reading Ease delta between sections
    sections = split_by_headers(text)
    for i in range(len(sections) - 1):
        flesch_curr = textstat.flesch_reading_ease(sections[i])
        flesch_next = textstat.flesch_reading_ease(sections[i+1])
        delta = abs(flesch_curr - flesch_next)
        if delta > config.pacing_flesch_delta:  # Default: 20
            issues.append({
                'type': 'complexity_spike',
                'severity': 'warning',
                'section': i + 1,
                'delta': delta,
                'message': f'Readability drops {delta:.1f} points - complexity wall'
            })

    # 3. Entity density (nouns per sentence)
    for sent in doc.sents:
        entities = [token for token in sent if token.pos_ in ['PROPN', 'NOUN']]
        density = len(entities) / max(len(list(sent)), 1)
        if density > config.pacing_entity_density:  # Default: 0.4
            issues.append({
                'type': 'noun_wall',
                'severity': 'info',
                'line': sent.start_line,
                'density': density,
                'message': f'Dense nouns ({density:.1%}) - consider simplifying'
            })

    return {
        'issues': issues,
        'metrics': {
            'avg_sentence_length': calculate_avg_sentence_length(doc),
            'sentence_variance': calculate_overall_variance(doc),
            'flesch_reading_ease': textstat.flesch_reading_ease(text)
        }
    }
```

#### Integration with Existing Flow Checker

**Option A: Separate checker (recommended)**
```python
# In cli.py
checkers = {
    'stumble': check_stumble,
    'scaffolding': check_scaffolding,
    'repetition': check_repetition,
    'flow': check_flow,
    'pacing': check_pacing  # NEW
}

# Run with: python cli.py script.md --pacing
```

**Option B: Integrated into flow.py**
```python
# In flow.py
def check_flow(text: str, config: Config) -> Dict[str, Any]:
    # ... existing flow checks ...

    # Add pacing analysis
    from checkers.pacing import check_pacing
    pacing_results = check_pacing(text, config)

    results['pacing_issues'] = pacing_results['issues']
    results['pacing_metrics'] = pacing_results['metrics']

    return results
```

**Recommendation: Option A (separate checker)** for cleaner separation of concerns and optional execution.

#### Configuration Additions

```python
# In config.py
class Config:
    # ... existing config ...

    # Pacing thresholds (v1.6)
    pacing_variance_threshold: float = 15.0      # Sentence length variance
    pacing_flesch_delta: float = 20.0            # Readability drop between sections
    pacing_entity_density: float = 0.4           # Nouns per sentence threshold
```

---

### Feature 3: Post-Publish Feedback Loop

**Integration Strategy:** New parser module + database storage + query integration in `/script` command

#### New Components

| Component | Purpose | LOC Estimate |
|-----------|---------|--------------|
| `tools/production/feedback_loader.py` | Parse POST-PUBLISH-ANALYSIS markdown files | ~200 LOC |
| Extension to `/script` command | Query feedback before script generation | ~50 LOC |

#### Data Flow

```
1. /analyze generates POST-PUBLISH-ANALYSIS-{id}.md (EXISTING)
   Saved to: channel-data/analyses/*.md or project folder
        ↓
2. feedback_loader.py parses markdown
   - Extracts: CTR vs channel avg, retention drops, discovery issues
   - Parses structured sections: "## Lessons", "## Discovery Diagnostics"
        ↓
3. Stores in video_performance table (EXISTING TABLE from Phase 19)
   - New columns: retention_drop_points (JSON), discovery_issues (JSON)
        ↓
4. /script command queries feedback BEFORE script generation
   - "Similar videos had pacing issues at 3:15"
   - "Map thumbnails outperform face 2:1"
        ↓
5. Script generation incorporates lessons
   - Avoid patterns that caused drops
   - Replicate patterns that worked
```

#### Feedback Parser Implementation

```python
# tools/production/feedback_loader.py

from pathlib import Path
import re
import json
from typing import Dict, List, Any
from datetime import datetime

def parse_analysis_file(filepath: Path) -> Dict[str, Any]:
    """
    Parse POST-PUBLISH-ANALYSIS markdown file.

    Extracts:
    - Video ID from filename and frontmatter
    - CTR vs channel average (from Quick Summary)
    - Retention drop points (from Retention Analysis)
    - Discovery issues (from Discovery Diagnostics)
    - Lessons (from Lessons section)

    Returns:
        {
            'video_id': str,
            'analyzed_at': str (ISO 8601),
            'ctr_percent': float or None,
            'ctr_vs_avg': str ('above', 'below', 'at'),
            'retention_drop_points': [
                {'timestamp': '3:15', 'percentage': 42.3, 'severity': 'significant'}
            ],
            'discovery_issues': [
                {'issue': 'LOW_IMPRESSIONS', 'severity': 'HIGH', 'fix': '...'}
            ],
            'lessons': {
                'observations': [str],
                'actionable_items': [str]
            }
        }
        or {'error': msg}
    """
    try:
        content = filepath.read_text(encoding='utf-8')

        # Extract video ID from filename: POST-PUBLISH-ANALYSIS-{video_id}.md
        match = re.search(r'POST-PUBLISH-ANALYSIS-([a-zA-Z0-9_-]+)\.md', filepath.name)
        if not match:
            return {'error': 'Could not extract video ID from filename'}

        video_id = match.group(1)

        # Parse analyzed timestamp
        analyzed_match = re.search(r'\*\*Analyzed:\*\* (.+)', content)
        analyzed_at = analyzed_match.group(1) if analyzed_match else None

        # Extract CTR
        ctr_match = re.search(r'\*\*CTR:\*\* ([\d.]+)%', content)
        ctr_percent = float(ctr_match.group(1)) if ctr_match else None

        # Determine CTR vs average
        ctr_vs_avg = None
        if 'above channel average' in content.lower():
            ctr_vs_avg = 'above'
        elif 'below channel average' in content.lower():
            ctr_vs_avg = 'below'
        elif 'at channel average' in content.lower():
            ctr_vs_avg = 'at'

        # Parse retention drop points
        retention_section = extract_section(content, '## Retention Analysis')
        drop_points = parse_retention_drops(retention_section)

        # Parse discovery issues
        discovery_section = extract_section(content, '## Discovery Diagnostics')
        issues = parse_discovery_issues(discovery_section)

        # Parse lessons
        lessons_section = extract_section(content, '## Lessons')
        lessons = parse_lessons(lessons_section)

        return {
            'video_id': video_id,
            'analyzed_at': analyzed_at,
            'ctr_percent': ctr_percent,
            'ctr_vs_avg': ctr_vs_avg,
            'retention_drop_points': drop_points,
            'discovery_issues': issues,
            'lessons': lessons
        }

    except Exception as e:
        return {'error': f'Failed to parse {filepath.name}', 'details': str(e)}


def store_feedback(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Store parsed feedback in video_performance table.

    Extends Phase 19 table with JSON columns for structured data.
    """
    from tools.discovery.database import KeywordDB

    db = KeywordDB()

    # Ensure feedback columns exist (auto-migration)
    db._ensure_feedback_columns()

    cursor = db._conn.cursor()
    cursor.execute("""
        UPDATE video_performance
        SET
            retention_drop_points = ?,
            discovery_issues = ?,
            lessons_observations = ?,
            lessons_actionable = ?,
            feedback_updated_at = CURRENT_TIMESTAMP
        WHERE video_id = ?
    """, (
        json.dumps(data['retention_drop_points']),
        json.dumps(data['discovery_issues']),
        json.dumps(data['lessons'].get('observations', [])),
        json.dumps(data['lessons'].get('actionable_items', [])),
        data['video_id']
    ))

    db._conn.commit()
    db.close()

    return {'status': 'stored', 'video_id': data['video_id']}


def load_feedback_for_topic(topic_keywords: List[str]) -> Dict[str, Any]:
    """
    Query feedback for videos matching topic keywords.

    Used by /script command to find relevant past performance data.

    Args:
        topic_keywords: List of keywords (e.g., ['territorial', 'dispute'])

    Returns:
        {
            'relevant_videos': [
                {
                    'video_id': str,
                    'title': str,
                    'ctr_percent': float,
                    'retention_drop_points': list,
                    'lessons': dict
                }
            ],
            'patterns': {
                'avg_ctr': float,
                'common_drop_points': [str],  # e.g., ['3:15', '5:42']
                'successful_patterns': [str]
            }
        }
    """
    # Query video_performance table for matching topics
    # Aggregate patterns across similar videos
    ...
```

#### Database Schema Extension

**New columns in existing `video_performance` table:**
```sql
ALTER TABLE video_performance ADD COLUMN retention_drop_points TEXT;  -- JSON array
ALTER TABLE video_performance ADD COLUMN discovery_issues TEXT;       -- JSON array
ALTER TABLE video_performance ADD COLUMN lessons_observations TEXT;   -- JSON array
ALTER TABLE video_performance ADD COLUMN lessons_actionable TEXT;     -- JSON array
ALTER TABLE video_performance ADD COLUMN feedback_updated_at TEXT;    -- ISO timestamp
```

**Auto-migration in database.py:**
```python
def _ensure_feedback_columns(self):
    """Phase v1.6: Add feedback columns to video_performance"""
    cursor = self._conn.cursor()
    cursor.execute("PRAGMA table_info(video_performance)")
    columns = {row[1] for row in cursor.fetchall()}

    if 'retention_drop_points' not in columns:
        cursor.execute("ALTER TABLE video_performance ADD COLUMN retention_drop_points TEXT")
    if 'discovery_issues' not in columns:
        cursor.execute("ALTER TABLE video_performance ADD COLUMN discovery_issues TEXT")
    if 'lessons_observations' not in columns:
        cursor.execute("ALTER TABLE video_performance ADD COLUMN lessons_observations TEXT")
    if 'lessons_actionable' not in columns:
        cursor.execute("ALTER TABLE video_performance ADD COLUMN lessons_actionable TEXT")
    if 'feedback_updated_at' not in columns:
        cursor.execute("ALTER TABLE video_performance ADD COLUMN feedback_updated_at TEXT")

    self._conn.commit()
```

#### Integration with `/script` Command

**Extend `.claude/commands/script.md`:**

```markdown
## NEW: Query Past Performance (v1.6)

Before writing, query feedback from similar videos:

1. Identify topic type (territorial, ideological, legal)
2. Load feedback for similar videos
3. Display lessons:
   - **CTR patterns:** "Map thumbnails avg 8.2% vs face 4.1%"
   - **Retention warnings:** "3 videos had drop at 3:15 (pacing spike)"
   - **Discovery lessons:** "Videos with long-tail keywords got 2x impressions"

Ask user: "Apply these lessons to new script? (Y/n)"
```

**Python implementation in script-writer-v2 agent:**
```python
# At start of script generation workflow
from tools.production.feedback_loader import load_feedback_for_topic

topic_keywords = ['territorial', 'dispute']  # Derived from user input
feedback = load_feedback_for_topic(topic_keywords)

if feedback['relevant_videos']:
    print("\n## Past Performance Insights\n")
    print(f"Analyzed {len(feedback['relevant_videos'])} similar videos:")
    print(f"- Average CTR: {feedback['patterns']['avg_ctr']:.1f}%")

    if feedback['patterns']['common_drop_points']:
        print(f"- Common retention drops: {', '.join(feedback['patterns']['common_drop_points'])}")

    if feedback['patterns']['successful_patterns']:
        print("\nSuccessful patterns:")
        for pattern in feedback['patterns']['successful_patterns']:
            print(f"  - {pattern}")

    apply = input("\nApply these lessons? (Y/n): ")
    if apply.lower() != 'n':
        # Incorporate lessons into script generation prompts
        ...
```

---

### Feature 4: Model Assignment Refresh

**Integration Strategy:** Update YAML frontmatter in slash command files

#### Current State (Phase 13.1)

```yaml
# .claude/commands/script.md
---
description: Write, revise, review, or export scripts
model: opus
---
```

**Problem:** Uses tier names (haiku, sonnet, opus) instead of full model IDs. May work if Claude SDK aliases these, but unclear.

#### Target State (v1.6)

```yaml
# .claude/commands/script.md
---
description: Write, revise, review, or export scripts
model: claude-opus-4-6
---
```

#### Model ID Mapping

| Current (Phase 13.1) | Target (v1.6) | Model ID | Use Case |
|---------------------|---------------|----------|----------|
| `model: haiku` | `model: claude-haiku-4-5` | `claude-haiku-4-5-20250926` (inferred) | Simple tasks (6 files) |
| `model: sonnet` | `model: claude-sonnet-4-5` | `claude-sonnet-4-5-20250929` (confirmed) | Standard tasks (6 files) |
| `model: opus` | `model: claude-opus-4-6` | `claude-opus-4-6-20260205` (confirmed) | Complex creative (1 file) |

**Note:** Exact version timestamps (YYYYMMDD suffix) may vary. Use base IDs (claude-haiku-4-5) if SDK supports version-agnostic routing.

#### Files to Update (13 total)

**Haiku tier (6 files):**
- `.claude/commands/status.md`
- `.claude/commands/help.md`
- `.claude/commands/fix.md`
- `.claude/commands/sources.md`
- `.claude/commands/prep.md`
- `.claude/commands/discover.md`

**Sonnet tier (6 files):**
- `.claude/commands/verify.md`
- `.claude/commands/publish.md`
- `.claude/commands/engage.md`
- `.claude/commands/analyze.md`
- `.claude/commands/patterns.md`
- `.claude/commands/research.md`

**Opus tier (1 file):**
- `.claude/commands/script.md`

#### Verification Strategy

**Option 1: Direct model ID (recommended)**
```yaml
model: claude-sonnet-4-5
```
- Explicit, no ambiguity
- Requires SDK supports these IDs

**Option 2: Tier alias with fallback**
```yaml
model: sonnet  # Maps to current best Sonnet model
```
- Simpler, auto-upgrades to latest
- Requires SDK maintains tier mappings

**Recommendation:** Use Option 1 (full IDs) for explicit control, verify with small test before bulk update.

#### Integration with Agent System

**If `.claude/agents/*.md` files also have model assignments:**
- Follow same mapping (haiku → claude-haiku-4-5, etc.)
- Check if agents inherit from command model or specify independently
- Update agent docs if Phase 13.1-02 created agent-specific model fields

---

## Recommended Build Order

### Phase 1: Database Foundation (Week 1)
**Why first:** Enables parallel development of tracking and feedback modules

1. Extend `database.py` with auto-migration methods:
   - `_ensure_thumbnail_table()`
   - `_ensure_feedback_columns()`
2. Test migration on clean and existing databases
3. Verify error dict pattern maintained

**Deliverable:** Database schema ready, zero breaking changes to existing tools

---

### Phase 2A: Thumbnail Tracking (Week 2 - Parallel Track)
**Dependencies:** Phase 1 complete

1. Implement `thumbnail_tracker.py`:
   - Hash computation (ImageHash)
   - Database storage
   - CLI entry points
2. Test with sample thumbnail files
3. Integrate with existing `/analyze` command

**Deliverable:** Users can track thumbnail variants, hashes stored in database

---

### Phase 2B: Pacing Analysis (Week 2 - Parallel Track)
**Dependencies:** None (extends existing script-checkers)

1. Implement `checkers/pacing.py`:
   - Sentence variance calculation
   - Flesch delta detection
   - Entity density checks
2. Extend `cli.py` with `--pacing` flag
3. Add config thresholds to `config.py`
4. Test on existing scripts

**Deliverable:** Users can run pacing checks before filming

---

### Phase 3: Thumbnail Pattern Analysis (Week 3)
**Dependencies:** Phase 2A complete (need tracked thumbnails)

1. Implement `thumbnail_patterns.py`:
   - Hamming distance clustering
   - CTR correlation
   - Pattern reporting
2. Integrate with `/patterns` command
3. Test with real thumbnail history (requires 5+ tracked videos)

**Deliverable:** Users see which thumbnail styles correlate with high CTR

---

### Phase 4: Feedback Loop Integration (Week 3-4)
**Dependencies:** Phase 1 complete

1. Implement `feedback_loader.py`:
   - Markdown parsing
   - Database storage
   - Query functions
2. Extend `/script` command to query feedback
3. Test with existing analysis files in `channel-data/analyses/`

**Deliverable:** Script generation incorporates past performance lessons

---

### Phase 5: Model Assignment Refresh (Week 4)
**Dependencies:** None (independent update)

1. Verify model ID format with small test
2. Bulk update 13 command files
3. Test each command tier (haiku, sonnet, opus)
4. Update agent files if needed

**Deliverable:** All commands use current Claude 4.x model lineup

---

### Phase 6: Integration Testing (Week 4)
**Test scenarios:**

1. **New video workflow:**
   - Create script → Run pacing check → Film → Publish
   - Create thumbnails → Track variants → Analyze CTR → Extract patterns

2. **Feedback loop:**
   - Analyze published video → Parse feedback → Create new script → Verify lessons applied

3. **Cross-component:**
   - `/patterns` shows thumbnail patterns + script patterns
   - `/analyze` includes thumbnail variant comparison
   - `/script` queries feedback automatically

**Deliverable:** All v1.6 features integrated, zero regressions

---

## Data Flow Integration Points

### Creation → Analysis → Feedback Loop

```
┌─────────────────────────────────────────────────────────────┐
│  CREATION PHASE                                              │
├─────────────────────────────────────────────────────────────┤
│  /script (queries past feedback)                            │
│    ↓                                                         │
│  Script generated with lessons applied                      │
│    ↓                                                         │
│  /prep --package (generates B-roll, edit guide, metadata)   │
│    ↓                                                         │
│  Create thumbnails A/B/C in Photoshop                       │
│    ↓                                                         │
│  thumbnail_tracker.py (compute hashes, store variants)      │
└─────────────────────────────────────────────────────────────┘
                            ↓
                     [FILMING & PUBLISHING]
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  ANALYSIS PHASE                                              │
├─────────────────────────────────────────────────────────────┤
│  /analyze VIDEO_ID (fetches CTR, retention, comments)       │
│    ↓                                                         │
│  Generates POST-PUBLISH-ANALYSIS.md                         │
│    ↓                                                         │
│  feedback_loader.py (parses markdown)                       │
│    ↓                                                         │
│  Stores in video_performance table                          │
└─────────────────────────────────────────────────────────────┘
                            ↓
                    [PATTERN EXTRACTION]
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  LEARNING PHASE                                              │
├─────────────────────────────────────────────────────────────┤
│  /patterns (cross-video analysis)                           │
│    ↓                                                         │
│  thumbnail_patterns.py (correlate hashes with CTR)          │
│    ↓                                                         │
│  pattern_extractor.py (topic/angle patterns)                │
│    ↓                                                         │
│  Generates insights: "Map thumbnails avg 8.2% CTR"          │
└─────────────────────────────────────────────────────────────┘
                            ↓
                      [FEEDS BACK TO /script]
                            ↓
                      (loop continues)
```

### Database Query Patterns

**Thumbnail pattern query:**
```python
# In thumbnail_patterns.py
def get_ctr_by_visual_pattern():
    db = KeywordDB()
    cursor = db._conn.cursor()

    # Group thumbnails by perceptual hash similarity
    cursor.execute("""
        SELECT
            hash_phash,
            COUNT(*) as variant_count,
            AVG(ctr_percent) as avg_ctr,
            GROUP_CONCAT(video_id) as video_ids
        FROM thumbnail_variants
        WHERE is_active = 1 AND ctr_percent IS NOT NULL
        GROUP BY hash_phash
        ORDER BY avg_ctr DESC
    """)

    patterns = []
    for row in cursor.fetchall():
        # Cluster by Hamming distance to find visually similar groups
        ...

    return patterns
```

**Feedback query for topic:**
```python
# In feedback_loader.py
def load_feedback_for_topic(topic_keywords: List[str]):
    db = KeywordDB()
    cursor = db._conn.cursor()

    # Find videos matching topic keywords
    keyword_query = " OR ".join([f"title LIKE '%{kw}%'" for kw in topic_keywords])

    cursor.execute(f"""
        SELECT
            video_id,
            title,
            ctr_percent,
            retention_drop_points,
            lessons_observations,
            lessons_actionable
        FROM video_performance
        WHERE ({keyword_query})
        AND retention_drop_points IS NOT NULL
        ORDER BY conversion_rate DESC
        LIMIT 10
    """)

    # Aggregate patterns across results
    ...
```

---

## Anti-Patterns to Avoid

### Anti-Pattern 1: Breaking Existing Database Schema

**What people do:** Add columns with NOT NULL constraint without default value
```sql
ALTER TABLE video_performance ADD COLUMN new_field TEXT NOT NULL;
-- Breaks on existing rows
```

**Why it's wrong:** Existing tools crash when querying table

**Do this instead:** Use nullable columns with auto-migration
```python
def _ensure_feedback_columns(self):
    cursor.execute("ALTER TABLE video_performance ADD COLUMN new_field TEXT")
    # Nullable by default, no crash on existing data
```

### Anti-Pattern 2: Tight Coupling Between New and Existing Modules

**What people do:** Import thumbnail_tracker directly in analyze.py
```python
# In analyze.py
from thumbnail_tracker import get_variants  # Hard dependency
```

**Why it's wrong:** analyze.py now fails if thumbnail_tracker has import errors (e.g., ImageHash not installed)

**Do this instead:** Lazy import with graceful degradation
```python
# In analyze.py
try:
    from thumbnail_tracker import get_variants
    THUMBNAILS_AVAILABLE = True
except ImportError:
    THUMBNAILS_AVAILABLE = False

def analyze_video(video_id):
    # ... existing analysis ...

    if THUMBNAILS_AVAILABLE:
        variants = get_variants(video_id)
        # ... use variants ...
```

### Anti-Pattern 3: Storing Images in Database

**What people do:** Store thumbnail PNG as BLOB in SQLite
```sql
CREATE TABLE thumbnails (
    id INTEGER PRIMARY KEY,
    image_data BLOB  -- 500KB+ per image
);
```

**Why it's wrong:** Database bloat, slow queries, backup issues

**Do this instead:** Store file paths, keep images on filesystem
```sql
CREATE TABLE thumbnail_variants (
    id INTEGER PRIMARY KEY,
    thumbnail_path TEXT,  -- "Thumbnail A.png"
    hash_phash TEXT       -- 16-char hex string
);
```

### Anti-Pattern 4: Synchronous Feedback Loading on Every Script Generation

**What people do:** Parse all analysis files every time `/script` runs
```python
def generate_script():
    # Parse 30+ markdown files on every run
    for file in analysis_dir.glob('*.md'):
        parse_and_analyze(file)  # Slow
```

**Why it's wrong:** Script generation takes 10+ seconds before starting

**Do this instead:** Parse once when analysis is created, query database
```python
# In /analyze command (runs once per video)
feedback_loader.store_feedback(parsed_data)

# In /script command (runs many times)
feedback = db.query_feedback_for_topic(keywords)  # Fast SQL query
```

---

## Scaling Considerations

| Scale | Current | With v1.6 | Notes |
|-------|---------|-----------|-------|
| **10 videos** | All features work | All features work | Minimal data, patterns may be noisy |
| **50 videos** | Good performance | Good performance | Thumbnail patterns become meaningful |
| **200 videos** | Good performance | Possible SQLite query lag | Consider index optimization |
| **500+ videos** | N/A (channel at ~30) | May need query optimization | Add indexes on video_id, ctr_percent, is_active |

### Optimization Priorities

**1. First bottleneck: Thumbnail pattern clustering (200+ videos)**
- **Symptom:** `/patterns` command takes 5+ seconds
- **Fix:** Pre-compute clusters on `/analyze`, store cluster IDs in database
- **Cost:** 50 LOC, negligible complexity

**2. Second bottleneck: Feedback query with many keywords (500+ videos)**
- **Symptom:** `/script` feedback query takes 3+ seconds
- **Fix:** Full-text search index on title/description
- **Cost:** SQLite FTS5 extension, ~100 LOC

**Note:** Unlikely to hit these limits with current channel size (~30 videos). Optimize only when proven slow.

---

## Confidence Assessment

| Component | Confidence | Reason |
|-----------|------------|--------|
| Database extensions | **HIGH** | Follows established auto-migration pattern from v1.3-v1.5 |
| Thumbnail tracking | **HIGH** | ImageHash is mature library, perceptual hashing is proven technique |
| Pacing analysis | **HIGH** | textstat + spaCy are production-ready, metrics well-defined |
| Feedback loop | **HIGH** | Pure integration work, markdown parsing is straightforward |
| Model assignments | **MEDIUM** | Model IDs verified, but exact SDK routing pattern unconfirmed |
| Build order | **HIGH** | Parallelizable phases, clear dependency graph |
| Integration | **HIGH** | Extends existing patterns without breaking changes |

---

## Sources

**Architecture Patterns:**
- Existing codebase patterns (error dict, auto-migration, lazy loading) - verified via code inspection
- Python SQLite best practices - [SQLite Documentation](https://www.sqlite.org/lang_altertable.html)
- CLI design patterns - [Click documentation](https://click.palletsprojects.com/)

**Database Design:**
- SQLite JSON support - [JSON Functions](https://www.sqlite.org/json1.html)
- Database migration strategies - [Alembic Documentation](https://alembic.sqlalchemy.org/)

**Integration Patterns:**
- Plugin architecture - [Python Import System](https://docs.python.org/3/reference/import.html)
- Feature flags - [LaunchDarkly Best Practices](https://docs.launchdarkly.com/home/getting-started/feature-flags)

---

*Architecture research for: History vs Hype v1.6 Click & Keep*
*Researched: 2026-02-06*
*Confidence: HIGH*
