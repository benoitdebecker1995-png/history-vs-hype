# VidIQ + Claude Workflow (Token Optimization)

**Purpose:** Use VidIQ for research/comparison tasks to save Claude tokens. Bring results to Claude for integration.

---

## When to Use VidIQ (Not Claude)

| Task | Use VidIQ | Why |
|------|-----------|-----|
| Find outlier videos | ✅ | VidIQ has the data |
| Compare topic potential | ✅ | Subscriber conversion scores |
| Search volume/competition | ✅ | Built-in metrics |
| Competitor analysis | ✅ | Channel comparison tools |
| Time-sensitive opportunities | ✅ | Trending + anniversary search |

## When to Use Claude

| Task | Use Claude | Why |
|------|------------|-----|
| Filter VidIQ results through channel DNA | ✅ | Knows your values |
| Write prompts FOR VidIQ | ✅ | Faster than typing |
| Integrate insights into project files | ✅ | Knows file structure |
| Research after topic selected | ✅ | Web search + synthesis |
| NotebookLM prompt creation | ✅ | Knows your workflow |

---

## Workflow

### Step 1: Topic Discovery (VidIQ)

Copy-paste prompt to VidIQ:
```
Find outlier videos (5x+ channel average) from history channels (10k-500k subs)
about [TOPIC AREA]. Show: title, views, outlier ratio, thumbnail style.
Prioritize subscriber conversion over raw views.
```

### Step 2: Topic Comparison (VidIQ)

```
Compare subscriber growth potential for these concepts:
TOPIC A: [title]
TOPIC B: [title]
TOPIC C: [title]

Analyze: search volume, competition, audience overlap with Kraut/RealLifeLore,
evergreen ratio, subscriber conversion trigger.
Rank 1-3 with reasoning.
```

### Step 3: Bring Results to Claude

Paste VidIQ output. Say:
> "Save this to [project file] and update [relevant files]"

Claude will:
- Filter through channel DNA
- Flag clickbait suggestions to reject
- Update topic pipeline
- Create research plan if needed

---

## Example Prompts by Task

### Find Time-Sensitive Topics
```
Find outlier videos for [DATE/EVENT] that fit evidence-based history channel.
Filter for: treaties, legal events, sovereignty, border changes.
Exclude: celebrations, news commentary, current politicians.
```

### Compare Angles on Same Topic
```
I'm covering [TOPIC]. Compare these angles:
A: [Political/emotional angle]
B: [Legal/mechanism angle]
C: [Comparative angle]

Which has highest subscriber conversion for educated males 25-44?
```

### Blue Ocean Search
```
Find topics with high search volume but low competition from mid-sized
history channels (10k-500k subs). Focus on: [your niche keywords].
Show the gap between demand and supply.
```

---

## Token-Saving Rules

1. **Don't ask Claude to search** for outliers/trends - VidIQ has better data
2. **Don't ask Claude to compare** topic potential - VidIQ scores this
3. **DO ask Claude to filter** VidIQ output through channel values
4. **DO ask Claude to integrate** results into project files
5. **DO ask Claude for research** AFTER topic is selected

---

*Created: 2025-12-25*
