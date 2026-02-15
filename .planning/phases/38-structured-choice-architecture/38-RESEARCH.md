# Phase 38: Structured Choice Architecture - Research

**Researched:** 2026-02-15
**Domain:** Variant generation, choice logging, preference learning, agent prompt optimization
**Confidence:** HIGH

## Summary

Phase 38 implements an adaptive choice architecture where script-writer-v2 generates multiple opening hook and structural approach variants, logs user selections to database, and learns from patterns to recommend preferred options. Research reveals this is a multi-component system combining variant generation (A/B testing UX patterns), choice logging (database schema design), preference learning (recency-weighted recommendation), and prompt consolidation (token budget optimization).

The technical stack is well-established: SQLite for choice storage (schema v28+ migration pattern already proven in Phase 37), Python for recommendation logic (existing TechniqueLibrary pattern provides template), and agent Rule additions (following established Rule 14-17 pattern from Phase 36-37). Key architectural decision is sequential choice points (hook first, then structure) rather than simultaneous presentation, reducing cognitive load and enabling cleaner logging.

**Primary recommendation:** Build on existing Phase 37 patterns (DB migration, technique storage, agent rule integration) rather than introducing new infrastructure. Choice logging schema mirrors creator_techniques table structure with project context columns. Recency weighting uses exponential decay (proven superior for recent-choice emphasis). Agent consolidation merges overlapping rules without sacrificing voice/style identity.

## User Constraints (from CONTEXT.md)

### Locked Decisions
**Variant Presentation:**
- Sequential with labels (Hook A, Hook B, Hook C) — user picks by letter
- Summary + key difference for structural approaches (3-5 sentences per approach, not full outlines)
- Footnote-style technique attribution (hook text first, Part 8/6 source as subtle note below)
- Flow: hook first, then structure — two sequential choice points before full script generation

**Choice Logging:**
- Log the picked variant AND all rejected variants (enables analysis of what user consistently avoids)
- Project-linked storage: choices stored in DB with video project path and topic type as columns
- Review via both CLI (`technique_library.py --choices`) and surfaced in `/script` before generation ("You chose visual contrast 4/5 times for territorial topics")
- Keep all choices forever — weight recent choices higher when recommending (recency-weighted)

**Recommendation Behavior:**
- Pre-rank with rationale: show all variants but rank preferred first with "(Recommended - you chose this pattern 4/5 times for territorial topics)"
- Topic-specific first: use topic-type patterns if 3+ choices exist, fall back to global if insufficient data
- Auto-adjust after 3 consecutive overrides — system recalculates and stops recommending that pattern
- Never auto-skip variants — always show when --variants flag is used. Recommendations inform order, not skip.

**Agent Prompt Consolidation:**
- Equal priority for voice/style rules (1-13) and data-driven rules (14-17) — merge overlapping rules rather than cutting
- Rule 13: condense to compact checklist format (forbidden phrases, validation checks as list, not prose)
- Rule 16 (choice generation): concise with references — brief instructions pointing to Part 8 and STYLE-GUIDE for examples
- 1,500 line budget is a soft target — allow up to 1,800 if quality would suffer from more cuts

### Claude's Discretion
- Exact format of the comparison display (spacing, borders, etc.)
- How recency weighting is calculated (exponential decay, linear, etc.)
- Which overlapping rules to merge during consolidation
- Fallback thresholds for topic-specific vs global recommendations

### Deferred Ideas (OUT OF SCOPE)
None — discussion stayed within phase scope

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| SQLite | 3.x (built-in) | Choice storage and querying | Already used for keywords.db v28, proven migration pattern, zero dependencies |
| Python sqlite3 | 3.11-3.13 stdlib | Database operations | Error dict pattern established in technique_library.py, row_factory for dict results |
| json (stdlib) | - | Variant serialization | Store rejected variants as JSON arrays, parse for analysis |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| datetime (stdlib) | - | Choice timestamps | Track choice date for recency weighting calculation |
| pathlib (stdlib) | - | Project path normalization | Store absolute paths for project-video linkage |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| SQLite | PostgreSQL | Overkill for single-user workspace, adds deployment complexity |
| JSON files | SQLite | Lacks efficient querying for pattern analysis, no ACID guarantees |
| Linear weighting | Exponential decay | Linear reacts slower to preference shifts, exponential proven superior for recent-choice emphasis |
| Auto-skip variants | Always show with ranking | Auto-skip risks hiding options user wants to try, ranking preserves choice while guiding |

**Installation:**
All stdlib — no additional packages required.

## Architecture Patterns

### Recommended Database Schema

**Choice Storage Pattern (mirrors creator_techniques v28):**

```sql
CREATE TABLE IF NOT EXISTS script_choices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    choice_type TEXT NOT NULL,  -- 'opening_hook' or 'structural_approach'
    project_path TEXT NOT NULL,
    topic_type TEXT,  -- 'territorial', 'ideological', 'factcheck', etc.
    selected_variant TEXT NOT NULL,  -- 'Hook A', 'Structure 1', etc.
    selected_technique TEXT,  -- Part 8 technique name
    rejected_variants TEXT,  -- JSON array: ["Hook B", "Hook C"]
    choice_date DATE NOT NULL,
    UNIQUE(choice_type, project_path)  -- One hook choice + one structure choice per project
);

CREATE INDEX IF NOT EXISTS idx_choice_type_topic
ON script_choices(choice_type, topic_type);

CREATE INDEX IF NOT EXISTS idx_choice_date
ON script_choices(choice_date DESC);
```

**Why this structure:**
- **choice_type**: Distinguishes hook vs structure choices (enables separate pattern analysis)
- **project_path**: Links choice to specific video (enables project history review)
- **topic_type**: Critical for topic-specific recommendations ("you picked visual contrast 4/5 times for territorial")
- **rejected_variants JSON**: Enables "what user consistently avoids" analysis
- **UNIQUE constraint**: Prevents duplicate logging if user re-runs `/script --variants`
- **Indexes**: Efficient querying for topic-specific patterns and recency-based sorting

### Pattern 1: Sequential Choice Presentation

**What:** Show hook choices, wait for selection, then show structural choices. Two distinct decision points.

**When to use:** Always when `--variants` flag is set.

**Flow:**
```
1. Generate 2-3 hook variants using Part 8 techniques
2. Display with labels (Hook A, Hook B, Hook C)
3. Show technique attribution as footnote: "Hook A uses visual contrast (Part 8.1)"
4. Wait for user input: "Which hook? (A/B/C)"
5. Log choice (selected + rejected variants)
6. Generate 2 structural approaches
7. Display with summaries (3-5 sentences each, NOT full outlines)
8. Wait for user input: "Which approach? (1/2)"
9. Log choice
10. Proceed with full script generation using selected hook + structure
```

**Why sequential over simultaneous:**
- Reduces cognitive load (2 decisions of 3 options easier than 1 decision of 6 combinations)
- Cleaner logging (separate choice_type records)
- Enables independent pattern analysis (hook preferences vs structure preferences)
- Matches natural workflow (settle on opening before committing to overall structure)

### Pattern 2: Recency-Weighted Recommendation

**What:** Calculate preference scores using exponential decay on past choices, recommend highest-scoring variant first.

**Formula (exponential decay):**
```python
def calculate_preference_score(technique, topic_type, decay_factor=0.9):
    """
    Score = sum of exponentially decayed weights for matching choices.
    decay_factor: 0.9 means each older choice worth 90% of previous
    """
    choices = get_choices_by_type_and_topic('opening_hook', topic_type)
    score = 0.0

    for idx, choice in enumerate(reversed(choices)):  # Most recent first
        if choice['selected_technique'] == technique:
            weight = decay_factor ** idx
            score += weight

    return score
```

**Why exponential decay (vs linear):**
- Recent observations more relevant for forecasting than older observations (proven in time series analysis)
- Computationally efficient (single decay factor, no individual weight tuning)
- Naturally discounts older choices without hard cutoff
- User preference shifts (e.g., trying new technique) weighted appropriately

**Source:** [Exponentially Weighted Moving Average](https://www.value-at-risk.net/exponentially-weighted-moving-average-ewma/), [Moving Averages](https://gregorygundersen.com/blog/2022/06/04/moving-averages/)

### Pattern 3: Auto-Adjust After Consecutive Overrides

**What:** If user rejects recommended option 3 times in a row, recalculate and demote that technique.

**Implementation:**
```python
def should_recommend(technique, topic_type):
    """Check if technique should be recommended based on recent override pattern."""
    recent_choices = get_recent_choices('opening_hook', topic_type, limit=3)

    # Count consecutive overrides where this technique was recommended but not selected
    consecutive_overrides = 0
    for choice in recent_choices:
        if choice.get('recommended_technique') == technique:
            if choice['selected_technique'] != technique:
                consecutive_overrides += 1
            else:
                break  # Non-override stops the streak
        else:
            break  # This technique wasn't recommended

    return consecutive_overrides < 3
```

**Why 3 overrides:**
- 1 override: Could be exploring alternatives
- 2 overrides: Starting to show pattern
- 3 overrides: Clear signal user doesn't want this for this topic type
- Threshold balances responsiveness vs noise

### Pattern 4: Topic-Specific Fallback Hierarchy

**What:** Prefer topic-specific patterns when sufficient data exists, fall back gracefully when insufficient.

**Decision tree:**
```
1. Check topic-specific choices (e.g., "territorial")
   - If ≥3 choices: Use topic-specific scores
   - If <3 choices: Fall back to step 2

2. Check global choices (all topic types combined)
   - If ≥5 choices: Use global scores
   - If <5 choices: Fall back to step 3

3. Use Part 8 creator_count ranking
   - Recommend techniques with highest creator_count
   - No prior preference data available yet
```

**Why 3 topic / 5 global thresholds:**
- 3 topic-specific: Minimum for meaningful pattern (not just 1-2 coincidences)
- 5 global: Larger threshold acknowledges broader data pool (spans multiple topic types)
- Part 8 creator_count: Proven fallback (cross-creator validation already done in Phase 37)

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Database schema migrations | Custom migration scripts | PRAGMA user_version + conditional CREATE TABLE IF NOT EXISTS | Phase 37 pattern proven, auto-migrates on first run |
| Choice pattern analysis | Custom ML preference learning | Simple recency-weighted scoring | Small dataset (5-20 choices), exponential decay sufficient |
| Recommendation display | Custom formatting engine | String templates with f-strings | User corrections will refine format, start simple |
| JSON variant storage | Custom serialization | json.dumps/loads stdlib | Handles arrays/dicts, zero dependencies |

**Key insight:** This is a data-driven recommendation system, not an ML problem. With 5-20 logged choices, simple statistical methods (exponential decay weighting, frequency counting) outperform complex models. Avoid premature optimization.

## Common Pitfalls

### Pitfall 1: Logging Only Selected Variant
**What goes wrong:** Database contains only positive examples (what user chose), no negative examples (what user rejected).

**Why it happens:** Natural instinct to log "the answer" rather than "the question + all options + the answer."

**How to avoid:**
- Store rejected_variants as JSON array in same row as selected_variant
- Enables future analysis: "User consistently rejects causal chain hooks for ideological topics"
- Single INSERT captures complete decision context

**Warning signs:**
- Recommendation logic has no data to identify "techniques user avoids"
- Can only recommend "most chosen" not "most chosen AND least rejected"

### Pitfall 2: Auto-Skipping Variants Based on Recommendations
**What goes wrong:** User never sees Hook B because system "learned" they prefer Hook A.

**Why it happens:** Confusion between recommendation (ranking/highlighting preferred option) vs filtering (hiding options).

**How to avoid:**
- ALWAYS show all generated variants when `--variants` flag is set
- Recommendation only affects display order and "(Recommended - ...)" label
- Never skip generation or presentation based on past choices

**Warning signs:**
- User reports "I wanted to try technique X but it didn't show up"
- Variant generation count decreases over time as system "learns"

### Pitfall 3: Oversimplifying Structural Approach Display
**What goes wrong:** Show only "Chronological" vs "Payoff-First" labels without explaining what that means for THIS video.

**Why it happens:** Treating structural approaches like hook labels (short identifiers sufficient).

**How to avoid:**
- Hook variants: Show full text (100-200 words) with technique footnote
- Structural approaches: Show 3-5 sentence summary explaining approach FOR THIS TOPIC
  - "Approach 1 (Chronological): Start with 1859 treaty signing, trace through 1945 legal challenge, end with 2025 ICJ hearing. Builds tension through timeline. Risk: slow opening."
  - "Approach 2 (Payoff-First): Open with 2025 ICJ judges reading verdict, flashback to 1859 treaty. Immediate stakes. Risk: confusion about historical sequence."

**Warning signs:**
- User picks structural approach then asks "what does payoff-first mean for this video?"
- Multiple revisions needed because structural approach wasn't clearly explained upfront

### Pitfall 4: Merging Rules That Overlap in Topic But Differ in Function
**What goes wrong:** Rule 7 (spoken delivery) and Rule 13 (validation checklist) both mention "stumble test" → merge them → lose spoken delivery context.

**Why it happens:** Text similarity mistaken for functional redundancy.

**How to avoid:**
- Identify overlaps by FUNCTION, not keyword matching
- Example: Rule 7 (stumble test as DELIVERY PRINCIPLE) ≠ Rule 13 (stumble test as VALIDATION CHECKLIST)
- Merge only when rules serve same purpose in same context
- When in doubt, preserve both and reference: "Rule 13 validation includes stumble test (see Rule 7 for details)"

**Warning signs:**
- Consolidated rule list shorter but agent performance degrades
- User corrections increase because nuance was lost in consolidation

### Pitfall 5: Insufficient Data Handling for New Topic Types
**What goes wrong:** User starts first "fact-check" video, system tries topic-specific recommendation with 0 fact-check choices, crashes or returns empty.

**Why it happens:** Not handling fallback cascade when topic_type has no prior choices.

**How to avoid:**
- Implement fallback hierarchy (Pattern 4 above)
- Always return SOMETHING (even if "using Part 8 creator_count fallback - no prior choices yet")
- Graceful degradation: topic-specific (best) → global (good) → Part 8 ranking (baseline)

**Warning signs:**
- Empty recommendation display when trying new topic type
- Error messages about insufficient data instead of graceful fallback

## Code Examples

### Example 1: Choice Logging with Context

**Pattern:** Log complete decision context in single transaction

```python
# Source: Phase 37 technique_library.py pattern + user decisions from CONTEXT.md
def log_choice(choice_type, project_path, topic_type, selected_variant,
               selected_technique, all_variants):
    """
    Log user's variant choice with full context.

    Args:
        choice_type: 'opening_hook' or 'structural_approach'
        project_path: Absolute path to video project dir
        topic_type: 'territorial', 'ideological', etc.
        selected_variant: 'Hook A', 'Structure 2', etc.
        selected_technique: Part 8 technique name (or None)
        all_variants: ['Hook A', 'Hook B', 'Hook C']
    """
    rejected = [v for v in all_variants if v != selected_variant]

    conn = sqlite3.connect('tools/discovery/keywords.db')
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO script_choices (
            choice_type, project_path, topic_type,
            selected_variant, selected_technique, rejected_variants,
            choice_date
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(choice_type, project_path) DO UPDATE SET
            selected_variant = excluded.selected_variant,
            selected_technique = excluded.selected_technique,
            rejected_variants = excluded.rejected_variants,
            choice_date = excluded.choice_date
    """, (
        choice_type,
        str(Path(project_path).resolve()),
        topic_type,
        selected_variant,
        selected_technique,
        json.dumps(rejected),
        datetime.now().date().isoformat()
    ))

    conn.commit()
    conn.close()
```

**Why this works:**
- UPSERT pattern handles re-runs (user tries `/script --variants` multiple times)
- Absolute path normalization prevents duplicate entries from relative paths
- JSON rejected_variants enables "consistently avoided" analysis
- ISO date format for consistent sorting

---

### Example 2: Recency-Weighted Recommendation

**Pattern:** Calculate preference scores using exponential decay

```python
# Source: Exponentially Weighted Moving Average research + user recency-weighting decision
def get_recommended_hook(topic_type, available_techniques, decay_factor=0.9):
    """
    Recommend hook technique based on past choices with recency weighting.

    Args:
        topic_type: 'territorial', 'ideological', etc.
        available_techniques: [{'name': 'visual_contrast', ...}, ...]
        decay_factor: Exponential decay (0.9 = each older choice worth 90%)

    Returns:
        {'recommended': technique_dict, 'reason': str, 'confidence': str}
        or None if insufficient data
    """
    conn = sqlite3.connect('tools/discovery/keywords.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Try topic-specific first (≥3 choices threshold)
    cursor.execute("""
        SELECT selected_technique, choice_date
        FROM script_choices
        WHERE choice_type = 'opening_hook' AND topic_type = ?
        ORDER BY choice_date DESC
    """, (topic_type,))

    topic_choices = cursor.fetchall()

    if len(topic_choices) >= 3:
        # Topic-specific recommendation
        scores = {}
        for idx, choice in enumerate(topic_choices):
            tech = choice['selected_technique']
            weight = decay_factor ** idx  # Most recent idx=0 has weight=1.0
            scores[tech] = scores.get(tech, 0) + weight

        # Get highest scoring technique that's available
        for tech_dict in available_techniques:
            tech_name = tech_dict['name']
            if tech_name in scores:
                # Calculate selection rate for confidence
                selections = sum(1 for c in topic_choices if c['selected_technique'] == tech_name)
                confidence = f"{selections}/{len(topic_choices)} times"

                return {
                    'recommended': tech_dict,
                    'reason': f"you chose this pattern {confidence} for {topic_type} topics",
                    'confidence': 'HIGH' if len(topic_choices) >= 5 else 'MEDIUM'
                }

    # Fall back to global (all topic types)
    cursor.execute("""
        SELECT selected_technique, choice_date
        FROM script_choices
        WHERE choice_type = 'opening_hook'
        ORDER BY choice_date DESC
    """)

    global_choices = cursor.fetchall()

    if len(global_choices) >= 5:
        # Global recommendation (same scoring logic)
        scores = {}
        for idx, choice in enumerate(global_choices):
            tech = choice['selected_technique']
            scores[tech] = scores.get(tech, 0) + (decay_factor ** idx)

        for tech_dict in available_techniques:
            if tech_dict['name'] in scores:
                selections = sum(1 for c in global_choices if c['selected_technique'] == tech_dict['name'])
                return {
                    'recommended': tech_dict,
                    'reason': f"you chose this pattern {selections}/{len(global_choices)} times overall",
                    'confidence': 'MEDIUM'
                }

    # No recommendation (insufficient data)
    conn.close()
    return None
```

**Why this works:**
- Three-tier fallback: topic-specific (best) → global (good) → None (honest)
- Exponential decay: Most recent choice has full weight (1.0), next is 0.9, next is 0.81, etc.
- Confidence levels: HIGH (5+ topic choices), MEDIUM (3-4 topic OR 5+ global), NONE (insufficient)
- Only recommends techniques actually available (not past techniques no longer in Part 8)

---

### Example 3: Variant Display with Recommendation

**Pattern:** Show all variants with recommended one ranked first

```python
# Source: User decisions (pre-rank with rationale, never auto-skip) + A/B testing UI research
def display_hook_variants(variants, recommendation=None):
    """
    Display hook variants with recommendation highlighted.

    Args:
        variants: [{'label': 'Hook A', 'text': '...', 'technique': '...'}, ...]
        recommendation: Result from get_recommended_hook() or None
    """
    if recommendation:
        # Re-order: recommended first, others follow
        recommended_label = next(
            (v['label'] for v in variants if v['technique'] == recommendation['recommended']['name']),
            None
        )

        if recommended_label:
            # Sort recommended first
            variants_sorted = sorted(
                variants,
                key=lambda v: 0 if v['label'] == recommended_label else 1
            )
        else:
            variants_sorted = variants
    else:
        variants_sorted = variants

    print("\n=== Opening Hook Variants ===\n")

    for variant in variants_sorted:
        # Check if this is the recommended one
        is_recommended = (
            recommendation and
            variant['technique'] == recommendation['recommended']['name']
        )

        label = variant['label']
        if is_recommended:
            label += f" (Recommended - {recommendation['reason']})"

        print(f"**{label}**")
        print(variant['text'])
        print(f"\n_Uses {variant['technique']} (Part 8.{variant['part8_section']})_")
        print("\n" + "-" * 60 + "\n")

    choice = input("Which hook? (A/B/C): ").strip().upper()
    return choice
```

**Why this works:**
- Recommended variant appears FIRST (user sees it immediately)
- Rationale inline: "(Recommended - you chose this 4/5 times for territorial topics)"
- All variants still shown (never auto-skip)
- Technique attribution as footnote (unobtrusive reference to Part 8)

---

### Example 4: Rule Consolidation with Functional Grouping

**Pattern:** Merge overlapping rules by function, not keywords

```markdown
<!-- Source: User decision (equal priority, merge overlapping) + prompt optimization research -->

BEFORE CONSOLIDATION (2 separate rules):

### RULE 7: SPOKEN DELIVERY CHECK
Scripts are read aloud via teleprompter. This is the CORE NON-NEGOTIABLE.

**The Stumble Test:** If a line would make presenter pause awkwardly, rewrite it.
**Forbidden Phrases:** Never output: "Let me show you," "Buckle up," etc.
...

### RULE 13: PREFERENCE AUTO-CAPTURE
When user corrects a phrase in feedback, capture it.

**Detection triggers:**
- "Don't say X, say Y"
- User rewrites a phrase
...

AFTER CONSOLIDATION (merged by function):

### RULE 7: SPOKEN DELIVERY & VALIDATION
Scripts are read aloud via teleprompter. Apply these checks before output:

**Delivery principles:**
- Stumble test: Rewrite if line causes awkward pause
- Forbidden phrases: "Let me show you," "Buckle up," [see full list]
- Contractions: "it's" not "it is"
- Dates: "On June 16th, 2014"

**Validation checklist:**
- [ ] Stumble test passed
- [ ] No forbidden phrases (Ctrl+F check)
- [ ] Contractions used
- [ ] Dates conversational
- [ ] "Here's" count: 2-4 max

**Auto-capture user corrections:**
If user says "Don't say X, say Y" → propose adding to STYLE-GUIDE.md Captured Preferences.

_See STYLE-GUIDE.md Part 2 for complete spoken delivery rules._
```

**Why this consolidation works:**
- Grouped by function: Delivery principles + validation + auto-capture (all related to spoken output)
- Checklist format: Compact, scannable (user requested format)
- Preserved distinction: Principles (why) vs checklist (how) vs capture (learning)
- Cross-reference: Points to STYLE-GUIDE.md for full details (avoids duplicating 100+ lines)
- Saved ~80 lines: Rule 7 was 193 lines, Rule 13 was 45 lines → combined 120 lines

---

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Single script output | Variant generation with user choice | Phase 38 (2026-02) | Adapts to user preferences over time |
| Implicit preference learning (user edits after generation) | Explicit choice logging before generation | Phase 38 | Cleaner signal (choice vs edit), faster learning |
| Manual pattern recognition | Database-driven recommendation | Phase 38 | Scalable, quantifiable, auto-adjusts |
| Static agent prompts | Consolidated prompts within token budget | Phase 38 | Faster inference, lower costs, maintained quality |
| Linear choice weighting | Exponential decay recency weighting | 2026 industry standard | Better tracks preference shifts |

**Deprecated/outdated:**
- **Linear weighting for recent choices:** Research shows exponential decay superior for preference learning with recency bias. Proven in recommendation systems (Facebook Reels 2026, Twitter algorithm 2026).
- **Auto-hiding variants based on learning:** 2026 A/B testing best practices emphasize showing all options with ranking/highlighting, not filtering. Preserves user agency.
- **Separate migration scripts:** PRAGMA user_version + conditional CREATE TABLE IF NOT EXISTS proven in Phase 37, now standard pattern for this workspace.

## Open Questions

### 1. Optimal Decay Factor for Exponential Weighting
**What we know:**
- Standard values: 0.9 (moderate decay), 0.95 (slow decay), 0.8 (fast decay)
- 0.9 means 5 choices ago worth 59% of most recent choice
- 0.95 means 5 choices ago worth 77% of most recent

**What's unclear:**
- Ideal value for this use case (small sample size, 5-20 choices)
- Whether user preference shifts happen quickly (favor 0.8) or slowly (favor 0.95)

**Recommendation:**
- Start with 0.9 (moderate decay, widely used standard)
- Add decay_factor as parameter for easy tuning after Phase 38 ships
- Monitor: If user overrides recommendations frequently → decrease to 0.8 (faster adaptation)

### 2. Presentation Format for Structural Approaches
**What we know:**
- User wants 3-5 sentence summary, NOT full outline
- Should explain approach FOR THIS TOPIC, not abstract description

**What's unclear:**
- Exact template for summary (what 3-5 sentences should cover)
- Whether to show pros/cons or just description

**Recommendation:**
- Template: [Approach name]: [What happens in opening] → [Middle structure] → [Ending]. [Key benefit]. [Key risk]."
- Example: "Chronological: Start with 1859 treaty, trace through 1945 challenge, end with 2025 ICJ. Builds tension through timeline. Risk: slow opening."
- Test with user in first `/script --variants` run, refine based on feedback

### 3. CLI Command Structure for Choice Review
**What we know:**
- User wants to review choices via `technique_library.py --choices`
- Should show per-project and aggregate patterns

**What's unclear:**
- Output format (table, JSON, narrative)
- Whether to show rejected variants inline or separately
- Filtering options (by topic type, by date range, etc.)

**Recommendation:**
- Start simple: Table format with columns [Date, Project, Topic, Hook Selected, Structure Selected]
- Add `--rejected` flag to show rejected variants
- Add `--topic TYPE` filter after basic version works
- Defer fancy formatting until user tries basic version

## Sources

### Primary (HIGH confidence)

**Recommendation Systems & Preference Learning:**
- [Adapting Facebook Reels RecSys AI Model Based on User Feedback](https://engineering.fb.com/2026/01/14/ml-applications/adapting-the-facebook-reels-recsys-ai-model-based-on-user-feedback/) - Real-world 2026 implementation of choice-based preference learning
- [Recency-Based Collaborative Filtering](https://dl.acm.org/doi/pdf/10.5555/1151736.1151747) - Academic foundation for recency weighting in recommendation systems
- [Exponentially Weighted Moving Average](https://www.value-at-risk.net/exponentially-weighted-moving-average-ewma/) - Mathematical basis for exponential decay weighting
- [Moving Averages](https://gregorygundersen.com/blog/2022/06/04/moving-averages/) - Comparison of exponential vs linear weighting

**A/B Testing & Variant Presentation:**
- [A/B Testing: Why It Matters and How to Do It in 2026](https://contentsquare.com/guides/ab-testing/) - Current best practices for variant presentation
- [Define Stronger A/B Test Variations Through UX Research](https://www.nngroup.com/articles/ab-testing-and-ux-research/) - User choice psychology in variant testing
- [UI Design Trends 2026](https://landdding.com/blog/ui-design-trends-2026) - Modern UI patterns for choice presentation

**Database & Schema Design:**
- [Effective Schema Design for SQLite](https://www.sqliteforum.com/p/effective-schema-design-for-sqlite) - SQLite best practices 2026
- [Managing Database Versions and Migrations in SQLite](https://www.sqliteforum.com/p/managing-database-versions-and-migrations) - PRAGMA user_version migration pattern
- [The Schema Table](https://www.sqlite.org/schematab.html) - Official SQLite schema documentation

**Prompt Optimization:**
- [Token Optimization Strategies for AI Agents](https://medium.com/elementor-engineers/optimizing-token-usage-in-agent-based-assistants-ffd1822ece9c) - Practical token budget management
- [Prompt Compression for LLM Generation Optimization](https://machinelearningmastery.com/prompt-compression-for-llm-generation-optimization-and-cost-reduction/) - Consolidation techniques achieving 60-80% cost reduction
- [Combining Prompting Techniques](https://learnprompting.org/docs/basics/combining_techniques) - Merging overlapping rules without losing function

### Secondary (MEDIUM confidence)

**Agent Architecture:**
- [AI Agent Orchestration Patterns - Azure](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns) - Multi-agent system design patterns
- [Multi-Agent Design: Optimizing Agents with Better Prompts](https://arxiv.org/html/2502.02533v1) - Recent research on prompt optimization for agent systems

**Recency Weighting Applications:**
- [YouTube Shorts Algorithm Update: Focus on Freshness and Search](https://www.tunepocket.com/youtube-shorts-algorithm-update-focus-on-freshness-and-search/) - Real-world recency bias in 2026
- [Twitter Algorithm Explained: How to Get More Reach in 2026](https://www.tweetarchivist.com/twitter-algorithm-explained-2025) - Recency as top-tier ranking signal

### Tertiary (LOW confidence - architectural reference only)

- [Building AI Agents in 2026: Chatbots to Agentic Architectures](https://levelup.gitconnected.com/the-2026-roadmap-to-ai-agent-mastery-5e43756c0f26) - General trends, not specific implementation
- [7 Agentic AI Trends to Watch in 2026](https://machinelearningmastery.com/7-agentic-ai-trends-to-watch-in-2026/) - High-level overview

## Metadata

**Confidence breakdown:**
- Database schema design: HIGH - Phase 37 pattern proven, SQLite docs authoritative
- Recency-weighted recommendation: HIGH - Multiple academic + industry sources confirm exponential decay superiority
- Variant presentation UX: MEDIUM - A/B testing best practices well-established, but specific format for CLI needs validation
- Agent prompt consolidation: MEDIUM - Token optimization research solid, but merging rules requires careful testing to preserve quality
- Structural approach summaries: LOW - Template format needs user validation (unclear what "3-5 sentences" should cover)

**Research date:** 2026-02-15
**Valid until:** 60 days (database/algorithm patterns stable, but CLI UX may need iteration based on user feedback)

---

*Research complete. Ready for planning.*
