---
description: YouTube Intelligence Engine — query algorithm knowledge, competitor data, and niche patterns
model: sonnet
---

# /intel - YouTube Intelligence Engine Query Interface

Query the YouTube Intelligence knowledge base for algorithm mechanics, competitor activity, niche patterns, and outlier videos.

## Usage

```
/intel                          — Full intelligence report (algo + competitors + niche)
/intel --algo                   — Algorithm mechanics summary
/intel --competitors            — Competitor channel activity and recent uploads
/intel --outliers               — Viral/outlier videos detected (>= 3x channel median)
/intel --niche                  — Niche format and pattern analysis
/intel --patterns               — Competitor topic cluster + title formula performance + gap analysis
/intel --score "topic title"    — Score a topic idea 0-100 (own channel + competitor + algo + trending + gap)
/intel --refresh                — Force refresh (runs full 10-phase pipeline)
/intel --add-channel CHANNEL_ID NAME CATEGORY  — Add channel to tracking list
/intel --query "question"       — Natural language query against KB
```

## Flags

| Flag | Purpose | Example |
|------|---------|---------|
| *(no flags)* | Full intelligence report | `/intel` |
| `--algo` | Algorithm signal weights, pipeline mechanics, longform insights | `/intel --algo` |
| `--competitors` | Tracked channel table + recent uploads | `/intel --competitors` |
| `--outliers` | Viral outlier videos detected at >= 3x channel median | `/intel --outliers` |
| `--niche` | Duration distribution, title formulas, trending topics | `/intel --niche` |
| `--patterns` | Topic cluster performance, title formula analysis, gap opportunities | `/intel --patterns` |
| `--score` | Score a topic idea 0-100 with 5-component breakdown | `/intel --score "How Britain Lost the Falklands"` |
| `--refresh` | Force full refresh regardless of staleness | `/intel --refresh` |
| `--add-channel` | Add channel to competitor tracking | `/intel --add-channel UCxxxxxx "Channel Name" style-match` |
| `--query` | Natural language question against KB | `/intel --query "what title formulas work best?"` |

**CATEGORY values for --add-channel:** `style-match` (closest peers), `broad-history` (educational history), `geopolitics` (current affairs / territorial)

---

## COMMAND FLOW

### Step 0: Check if intel.db exists

Before any operation, verify the database is initialized:

```python
import sys
sys.path.insert(0, '.')
from tools.intel.kb_store import KBStore
from pathlib import Path
db_exists = Path('tools/intel/intel.db').exists()
```

If `intel.db` does not exist: Inform user the knowledge base is not initialized, then run an initial refresh automatically (same as `--refresh`).

### Step 1: Route by flag

---

### NO FLAGS — Full Intelligence Report

Read and display `channel-data/youtube-intelligence.md` in full:

```python
import sys
sys.path.insert(0, '.')
from tools.intel.query import get_full_report
print(get_full_report())
```

Display the returned Markdown directly. Do not summarize — show the full report.

---

### --refresh — Force Full Refresh

Run the complete 10-phase refresh pipeline:

```python
import sys
sys.path.insert(0, '.')
from tools.intel.refresh import run_refresh, get_refresh_summary
result = run_refresh(force=True)
summary = get_refresh_summary(result)
print(summary)
```

Display the refresh summary including:
- Phases completed / failed
- Channels fetched
- Videos saved
- Outliers detected
- KB export status

After refresh completes, display the full report (same as no-flags mode).

---

### --algo — Algorithm Mechanics

```python
import sys
sys.path.insert(0, '.')
from tools.intel.query import get_algo_summary
print(get_algo_summary())
```

---

### --competitors — Competitor Channel Activity

```python
import sys
sys.path.insert(0, '.')
from tools.intel.query import get_competitor_report
print(get_competitor_report())
```

---

### --outliers — Viral/Outlier Video Detection

```python
import sys
sys.path.insert(0, '.')
from tools.intel.query import get_outlier_report
print(get_outlier_report())
```

---

### --niche — Niche Format and Pattern Analysis

```python
import sys
sys.path.insert(0, '.')
from tools.intel.query import get_niche_report
print(get_niche_report())
```

---

### --patterns — Competitor Topic Cluster + Formula + Gap Analysis

```python
import sys
sys.path.insert(0, '.')
from tools.intel.query import get_pattern_report
print(get_pattern_report())
```

Displays:
1. **Topic Cluster Performance** — avg views, outlier rate, avg duration per cluster
2. **Title Formula Performance** — which formulas (how/why, question, colon-split) drive highest views
3. **Gap Opportunities** — topics competitors cover heavily but you don't (yet)
4. **Top Outlier Videos by Cluster** — highest-performing videos per topic

---

### --score "topic title" — Score a Topic Idea 0-100

Parse the topic text from the user's command (everything after `--score`).

```python
import sys
sys.path.insert(0, '.')
from tools.intel.query import get_topic_score
print(get_topic_score('<TOPIC_TEXT>'))
```

Displays:
1. **Total score** (0-100) with letter grade (A-F)
2. **5-component breakdown** — Own Channel (30%), Competitor Signal (30%), Algorithm Alignment (20%), Trending (10%), Gap Opportunity (10%)
3. **Recommendations** — target duration, title formula suggestions, comparable outlier videos

Multiple topics can be scored in sequence: `/intel --score "topic 1" --score "topic 2"`

---

### --add-channel CHANNEL_ID NAME CATEGORY — Add Competitor Channel

Parse the three arguments after `--add-channel` from the user's command.

```python
import sys
sys.path.insert(0, '.')
from tools.intel.query import add_competitor_channel

# Extract from user command: CHANNEL_ID, NAME, CATEGORY
result = add_competitor_channel(
    channel_id='<CHANNEL_ID>',
    channel_name='<NAME>',
    category='<CATEGORY>',  # style-match | broad-history | geopolitics
)
print(result)
```

Display confirmation message. Suggest running `/intel --refresh` to immediately fetch that channel's videos.

---

### --query "question" — Natural Language Query

Use `channel-data/youtube-intelligence.md` as context to answer the user's question.

**Step 1:** Read the KB:

```python
from pathlib import Path
kb_content = Path('channel-data/youtube-intelligence.md').read_text(encoding='utf-8')
```

**Step 2:** Answer the question using the KB as context.

Treat the question as a request for intelligence analysis. Use the data in the KB to give a concrete, actionable answer. Do not invent data — reference specific numbers, patterns, or observations from the KB.

**Example:**
> `/intel --query "what are the most common title formulas competitors use?"`
> Answer should reference the Title Formulas table from the Niche Patterns section.

If the KB is empty, inform user to run `/intel --refresh` first.

---

### LLM-Enhanced Algorithm Synthesis (on --refresh)

After `run_refresh()` completes, the system can produce a higher-quality algorithm synthesis using Claude's language understanding. This is the "deep algorithm mechanics" mode.

After text-analysis synthesis completes:

1. Read the scraped algorithm content collected during Phase 1 of the refresh
2. Use the SYNTHESIS_PROMPT constant from algo_synthesizer.py as a guide
3. Produce a structured synthesis covering:
   - Signal weights with confidence levels
   - Pipeline mechanics (browse, search, suggested)
   - Longform-specific insights (what changes at 8+ min, 20+ min)
   - Satisfaction signals (surveys, post-watch questionnaires)
   - Actionable thresholds (what CTR%, AVD% matters)
4. Call `store.save_algo_snapshot()` with the enhanced model
5. Re-export the KB: `export_kb_to_markdown()`

**Implementation:**

```python
import sys
sys.path.insert(0, '.')
from tools.intel.algo_synthesizer import SYNTHESIS_PROMPT
from tools.intel.kb_store import KBStore
from tools.intel.kb_exporter import export_kb_to_markdown

# SYNTHESIS_PROMPT contains the instruction for structured synthesis
# Use scraped content (from run_refresh result) + SYNTHESIS_PROMPT
# to produce enhanced algorithm model, then save and re-export
```

This LLM enhancement step runs only on `--refresh` (not for query-only operations).

---

## STALENESS STATUS

Always show staleness status at the bottom of every response:

```python
import sys
sys.path.insert(0, '.')
from tools.intel.query import get_staleness_status
print(get_staleness_status())
```

Format: `Last refreshed: YYYY-MM-DD (N days ago)` or `Last refreshed: never`

If stale (>= 7 days), append: `(STALE — run /intel --refresh)`

---

## ERROR HANDLING

- `intel.db missing` → Run initial refresh automatically
- `youtube-intelligence.md missing` → Run refresh, then display
- `KBStore errors` → Display error message, suggest refresh
- `refresh errors` → Show which phases succeeded/failed, continue with available data

---

## REFERENCE FILES

- **KB snapshot:** `channel-data/youtube-intelligence.md` (auto-generated, do not edit)
- **Query interface:** `tools/intel/query.py`
- **Refresh orchestrator:** `tools/intel/refresh.py`
- **Storage layer:** `tools/intel/kb_store.py`
- **Channel config:** `tools/intel/competitor_channels.json`
