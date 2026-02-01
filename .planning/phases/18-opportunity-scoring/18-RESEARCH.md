# Phase 18: Opportunity Scoring & Orchestrator - Research

**Researched:** 2026-02-01
**Domain:** Multi-criteria decision making, lifecycle tracking, report generation
**Confidence:** HIGH

## Summary

Phase 18 is the final orchestrator for v1.3, combining outputs from Phases 15-17 (demand, competition, format filtering) into a single opportunity score. The core challenge is designing a scoring formula that balances multiple factors (demand, competition gap, production fit) while enforcing hard constraints (animation blocks, channel DNA violations) and tracking lifecycle state as topics progress from discovery to publication.

Research shows this is a well-understood problem domain (multi-criteria decision making) with established patterns. The standard approach uses weighted scoring with normalization, hard constraints as filters (not scores), and state machines for lifecycle tracking. Python has mature libraries for MCDM (pymcdm, python-statemachine), but for this phase's simplicity, direct implementation is recommended over library dependencies.

**Primary recommendation:** Use SAW (Simple Additive Weighting) with hard constraint pre-filtering, SQLite-backed state machine, and Markdown templating for reports.

## Standard Stack

### Core

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Python stdlib | 3.11+ | Core logic | No external dependencies needed for formula |
| SQLite3 | Built-in | State tracking | Already in use for database.py |
| Jinja2 | 3.1+ | Report templates | Industry standard for Markdown generation |

### Supporting

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| pymcdm | 1.1.3+ | MCDM algorithms | Only if formula complexity grows beyond SAW |
| python-statemachine | 2.5.0+ | State machines | Only if state transitions become complex |
| tabulate | 0.9+ | Table formatting | For CLI output (reports use Jinja2) |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Direct formula | pymcdm library | Library adds 5+ dependencies for a simple weighted sum |
| SQLite state | python-statemachine | Adds async complexity not needed for this use case |
| Jinja2 templates | f-strings | Templates separate logic from presentation, easier to maintain |

**Installation:**
```bash
pip install jinja2 tabulate
# Optional (only if needed later):
# pip install pymcdm python-statemachine
```

## Architecture Patterns

### Recommended Project Structure
```
tools/discovery/
├── database.py              # KeywordDB (existing)
├── demand.py                # DemandAnalyzer (Phase 15)
├── competition.py           # CompetitionAnalyzer (Phase 16)
├── format_filters.py        # Production constraints (Phase 17)
├── opportunity.py           # NEW: OpportunityScorer (Phase 18)
├── orchestrator.py          # NEW: OpportunityOrchestrator (Phase 18)
└── templates/
    └── opportunity_report.md.j2  # Markdown report template
```

### Pattern 1: Hard Constraints as Pre-Filters

**What:** Separate hard constraints (blockers) from scoring criteria. Filter first, score second.

**When to use:** When some criteria are absolute (animation required = 0 score regardless of demand).

**Example:**
```python
# Source: Multi-criteria decision making best practices
def score_opportunity(keyword_data: Dict) -> Optional[float]:
    """
    Calculate opportunity score with hard constraint filtering.

    Returns None if hard constraints violated, score 0-100 otherwise.
    """
    # STEP 1: Hard constraints (pre-filter)
    if keyword_data.get('is_production_blocked'):
        return None  # Animation required - don't score

    if violates_channel_dna(keyword_data['keyword']):
        return None  # Clickbait/news-first - don't score

    # STEP 2: Soft criteria (weighted scoring)
    demand_score = keyword_data['search_volume_proxy']  # 0-100
    gap_score = keyword_data['differentiation_score'] * 100  # 0-1 → 0-100
    fit_score = keyword_data['document_score'] * 25  # 0-4 → 0-100

    # Weighted average (customize weights based on validation)
    weights = {'demand': 0.4, 'gap': 0.3, 'fit': 0.3}

    opportunity_score = (
        demand_score * weights['demand'] +
        gap_score * weights['gap'] +
        fit_score * weights['fit']
    )

    return opportunity_score
```

### Pattern 2: Lifecycle State Machine in SQLite

**What:** Track opportunity lifecycle using database fields instead of full state machine library.

**When to use:** When states are simple and transitions are linear/few branches.

**Example:**
```python
# Source: Lightweight state tracking pattern
LIFECYCLE_STATES = [
    'DISCOVERED',      # Keyword found, not yet analyzed
    'ANALYZED',        # Opportunity score calculated
    'RESEARCHING',     # User started NotebookLM research
    'SCRIPTING',       # Script in progress
    'FILMED',          # Video filmed
    'PUBLISHED',       # Video live on YouTube
    'ARCHIVED'         # Published or abandoned
]

def transition_state(db: KeywordDB, keyword_id: int, new_state: str) -> Dict:
    """
    Transition keyword to new lifecycle state.

    Validates transition rules before updating.
    """
    current = db.get_lifecycle_state(keyword_id)

    # Validation rules
    valid_transitions = {
        'DISCOVERED': ['ANALYZED', 'ARCHIVED'],
        'ANALYZED': ['RESEARCHING', 'ARCHIVED'],
        'RESEARCHING': ['SCRIPTING', 'ARCHIVED'],
        'SCRIPTING': ['FILMED', 'ARCHIVED'],
        'FILMED': ['PUBLISHED', 'ARCHIVED'],
        'PUBLISHED': ['ARCHIVED'],
        'ARCHIVED': []
    }

    if new_state not in valid_transitions.get(current, []):
        return {'error': f'Invalid transition from {current} to {new_state}'}

    # Update state with timestamp
    db.set_lifecycle_state(keyword_id, new_state)
    return {'status': 'transitioned', 'from': current, 'to': new_state}
```

### Pattern 3: Orchestrator Aggregation

**What:** Single class that coordinates calls to all Phase 15-17 modules and combines results.

**When to use:** When multiple modules must be called in sequence with data aggregation.

**Example:**
```python
# Source: Facade pattern for complex subsystems
class OpportunityOrchestrator:
    """
    Orchestrate opportunity scoring across all phases.

    Aggregates: Demand (15) + Competition (16) + Format (17) → Opportunity (18)
    """

    def __init__(self, db: KeywordDB):
        self.db = db
        self.demand = DemandAnalyzer(db)
        self.competition = CompetitionAnalyzer()
        self.scorer = OpportunityScorer(db)

    def analyze_opportunity(self, keyword: str, force_refresh: bool = False) -> Dict:
        """
        Complete opportunity analysis pipeline.

        Returns comprehensive opportunity data or error dict.
        """
        # Phase 15: Demand analysis
        demand_data = self.demand.analyze_keyword(keyword, force_refresh)
        if 'error' in demand_data:
            return demand_data

        keyword_id = self.db.get_keyword(keyword)['id']

        # Phase 16: Competition analysis
        comp_data = self.competition.analyze_competition(keyword)
        if 'error' in comp_data:
            return comp_data

        # Phase 17: Production constraints
        constraints = self.db.get_production_constraints(keyword_id)
        if constraints is None:
            constraints = self._evaluate_constraints(keyword)

        # Phase 18: Opportunity scoring
        score_result = self.scorer.score_opportunity(
            keyword_id=keyword_id,
            demand_data=demand_data,
            competition_data=comp_data,
            constraints=constraints
        )

        return score_result
```

### Anti-Patterns to Avoid

- **Scoring blocked topics:** Don't assign scores to animation-required topics. Filter them completely (score = None, not 0).
- **Ignoring data age:** Always check `data_age_days` fields. Stale data (>7 days) should trigger warnings.
- **Complex weighted formulas without validation:** Start simple (equal weights), iterate based on actual video performance.
- **State transitions without validation:** Always validate state changes (can't go from DISCOVERED to PUBLISHED).

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Multi-criteria scoring | Custom weighted algorithm | SAW formula pattern | Well-tested, simple to validate |
| Markdown generation | String concatenation | Jinja2 templates | Maintainable, separates logic from presentation |
| State validation | Ad-hoc if/else chains | Transition map dictionary | Declarative, easy to extend |
| Report formatting | Manual table building | tabulate library | Handles edge cases (column width, alignment) |

**Key insight:** The scoring formula is simple enough to implement directly. Don't add MCDM library complexity unless formula needs TOPSIS, AHP, or other advanced methods.

## Common Pitfalls

### Pitfall 1: Treating All Criteria as Scores

**What goes wrong:** Animation requirement gets scored as 0 instead of filtered, skewing averages.

**Why it happens:** Confusion between soft criteria (scoreable) and hard constraints (blockers).

**How to avoid:** Pre-filter hard constraints before scoring. Return `None` for blocked topics, not 0.

**Warning signs:**
- Opportunity reports include animation-required topics with low scores
- Average scores drop when animation topics are included
- User wastes time investigating blocked topics

### Pitfall 2: Stale Data Aggregation

**What goes wrong:** Combining 1-day-old demand data with 30-day-old competition data produces misleading scores.

**Why it happens:** Not checking `data_age_days` when aggregating across phases.

**How to avoid:**
- Track max data age across all inputs
- Warn when any input exceeds 7 days
- Provide `--refresh` flag to force all sources

**Warning signs:**
- User questions why scores change when re-running without `--refresh`
- Scores don't reflect recent competition changes
- Warnings about stale data are ignored in reports

### Pitfall 3: Unweighted Formula

**What goes wrong:** Treating demand and fit equally when channel priorities differ.

**Why it happens:** Starting with `(demand + gap + fit) / 3` without considering business priorities.

**How to avoid:**
- Define initial weights based on channel strategy (e.g., fit > demand for niche focus)
- Document weight assumptions in code comments
- Plan for weight adjustment based on validation results (Phase v1.4)

**Warning signs:**
- High-scoring topics don't align with user's intuition
- Topics with poor fit but high demand score well
- User overrides many top recommendations

### Pitfall 4: Missing Lifecycle Transitions

**What goes wrong:** Keyword state stuck in RESEARCHING after script is written.

**Why it happens:** No mechanism to update state when work progresses.

**How to avoid:**
- Provide CLI command to update state: `python orchestrator.py transition <keyword> SCRIPTING`
- Document state meanings and transition triggers
- Consider auto-detection (if script file exists → SCRIPTING)

**Warning signs:**
- Multiple keywords in RESEARCHING state with completed scripts
- User confusion about what "RESEARCHING" means
- No way to filter to "ready to script" topics

### Pitfall 5: Non-Reproducible Scores

**What goes wrong:** Running same keyword twice gives different scores.

**Why it happens:** Not caching intermediate results, fetching fresh API data each run.

**How to avoid:**
- Cache all Phase 15-17 outputs to database with timestamps
- Only re-fetch if `--refresh` flag or data too old
- Include data freshness in report

**Warning signs:**
- Scores fluctuate between runs without external changes
- API rate limits hit during scoring
- No audit trail of why score changed

## Code Examples

### Opportunity Scoring Formula

```python
# Source: SAW (Simple Additive Weighting) pattern
from typing import Dict, Optional, Any

class OpportunityScorer:
    """
    Calculate opportunity scores using weighted SAW formula.

    Formula: score = (demand × w1) + (gap × w2) + (fit × w3)

    Where:
    - demand = search_volume_proxy (0-100)
    - gap = differentiation_score (0-1, normalized to 0-100)
    - fit = document_score (0-4, normalized to 0-100)

    Weights default to balanced (0.33 each) but configurable.
    """

    def __init__(self, db, weights: Optional[Dict[str, float]] = None):
        self.db = db

        # Default weights (can override for experimentation)
        self.weights = weights or {
            'demand': 0.33,
            'gap': 0.33,
            'fit': 0.34  # Slightly higher for channel focus on document-heavy
        }

        # Validate weights sum to 1.0
        total = sum(self.weights.values())
        if not (0.99 <= total <= 1.01):
            raise ValueError(f"Weights must sum to 1.0, got {total}")

    def score_opportunity(
        self,
        keyword_id: int,
        demand_data: Dict,
        competition_data: Dict,
        constraints: Dict
    ) -> Dict[str, Any]:
        """
        Calculate opportunity score from aggregated data.

        Returns:
            {
                'keyword': str,
                'opportunity_score': float,  # 0-100 or None if blocked
                'category': str,  # 'Excellent', 'Good', 'Fair', 'Poor'
                'is_blocked': bool,
                'block_reason': str,
                'components': {
                    'demand': {'raw': float, 'normalized': float, 'weight': float},
                    'gap': {...},
                    'fit': {...}
                },
                'warnings': List[str],
                'data_age_days': int
            }
        """
        keyword = demand_data['keyword']
        warnings = list(demand_data.get('warnings') or [])

        # HARD CONSTRAINTS (pre-filter)
        if constraints and constraints.get('is_production_blocked'):
            return {
                'keyword': keyword,
                'opportunity_score': None,
                'category': 'Blocked',
                'is_blocked': True,
                'block_reason': 'Animation required',
                'warnings': warnings
            }

        if self._violates_channel_dna(keyword):
            return {
                'keyword': keyword,
                'opportunity_score': None,
                'category': 'Blocked',
                'is_blocked': True,
                'block_reason': 'Channel DNA violation (clickbait/news-first)',
                'warnings': warnings
            }

        # SOFT CRITERIA (scoring)

        # Demand: autocomplete position proxy (already 0-100)
        demand_raw = demand_data.get('search_volume_proxy', 0)
        demand_normalized = demand_raw  # Already 0-100

        # Gap: differentiation score (0-1, scale to 0-100)
        gap_raw = competition_data.get('differentiation_score', 0)
        gap_normalized = gap_raw * 100

        # Fit: document score (0-4, scale to 0-100)
        fit_raw = constraints.get('document_score', 2) if constraints else 2
        fit_normalized = fit_raw * 25  # 0→0, 4→100

        # Weighted score
        opportunity_score = (
            demand_normalized * self.weights['demand'] +
            gap_normalized * self.weights['gap'] +
            fit_normalized * self.weights['fit']
        )

        # Categorize
        if opportunity_score >= 70:
            category = 'Excellent'
        elif opportunity_score >= 50:
            category = 'Good'
        elif opportunity_score >= 30:
            category = 'Fair'
        else:
            category = 'Poor'

        # Track data age
        data_age_days = max(
            demand_data.get('data_age_days', 0),
            competition_data.get('fetched_at', ''),  # Would need parsing
            constraints.get('data_age_days', 0) if constraints else 0
        )

        return {
            'keyword': keyword,
            'opportunity_score': round(opportunity_score, 1),
            'category': category,
            'is_blocked': False,
            'block_reason': None,
            'components': {
                'demand': {
                    'raw': demand_raw,
                    'normalized': demand_normalized,
                    'weight': self.weights['demand'],
                    'contribution': demand_normalized * self.weights['demand']
                },
                'gap': {
                    'raw': gap_raw,
                    'normalized': gap_normalized,
                    'weight': self.weights['gap'],
                    'contribution': gap_normalized * self.weights['gap']
                },
                'fit': {
                    'raw': fit_raw,
                    'normalized': fit_normalized,
                    'weight': self.weights['fit'],
                    'contribution': fit_normalized * self.weights['fit']
                }
            },
            'warnings': warnings,
            'data_age_days': data_age_days
        }

    def _violates_channel_dna(self, keyword: str) -> bool:
        """
        Check if keyword violates channel DNA rules.

        Per CLAUDE.md Channel DNA:
        - No clickbait language ("secret", "hidden", "they don't want you to know")
        - No news-first framing ("Why [Country] Just Did X")
        - No current politician as main subject
        """
        keyword_lower = keyword.lower()

        # Clickbait keywords
        clickbait = ['secret', 'hidden', 'shocking', 'you won\'t believe',
                     'they don\'t want', 'conspiracy']
        if any(word in keyword_lower for word in clickbait):
            return True

        # News-first framing
        news_patterns = ['why [country] just', 'breaking:', 'latest', 'just announced']
        if any(pattern in keyword_lower for pattern in news_patterns):
            return True

        # Current politicians (2026)
        current_politicians = ['trump', 'biden', 'netanyahu', 'putin', 'xi jinping']
        # Only block if politician is the main subject (not just mentioned)
        if keyword_lower.startswith(tuple(current_politicians)):
            return True

        return False
```

### Markdown Report Generation

```python
# Source: Jinja2 templating best practices
from jinja2 import Environment, FileSystemLoader
from pathlib import Path

def generate_opportunity_report(
    opportunity_data: Dict,
    output_path: Optional[str] = None
) -> str:
    """
    Generate Markdown opportunity report from scored data.

    Template includes:
    - Opportunity score with visual bar
    - Component breakdown (demand, gap, fit)
    - Competition analysis
    - Production constraints
    - Recommended next steps

    Args:
        opportunity_data: Complete opportunity analysis result
        output_path: Optional file path to write report

    Returns:
        Rendered Markdown string
    """
    # Load template
    template_dir = Path(__file__).parent / 'templates'
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template('opportunity_report.md.j2')

    # Add helper functions to template context
    def score_bar(score: float, max_length: int = 20) -> str:
        """Generate ASCII progress bar for score."""
        if score is None:
            return '░' * max_length
        filled = int((score / 100) * max_length)
        return '█' * filled + '░' * (max_length - filled)

    def format_percent(value: float) -> str:
        """Format percentage with sign."""
        return f"{value:+.1f}%"

    # Render template
    markdown = template.render(
        data=opportunity_data,
        score_bar=score_bar,
        format_percent=format_percent
    )

    # Write to file if path provided
    if output_path:
        Path(output_path).write_text(markdown, encoding='utf-8')

    return markdown
```

### Lifecycle State Tracking

```python
# Source: State machine pattern (lightweight implementation)
from typing import Dict, List, Optional
from datetime import datetime

class LifecycleTracker:
    """
    Track keyword lifecycle state in database.

    States: DISCOVERED → ANALYZED → RESEARCHING → SCRIPTING → FILMED → PUBLISHED → ARCHIVED

    Uses SQLite for persistence (no external state machine library needed).
    """

    STATES = [
        'DISCOVERED',
        'ANALYZED',
        'RESEARCHING',
        'SCRIPTING',
        'FILMED',
        'PUBLISHED',
        'ARCHIVED'
    ]

    TRANSITIONS = {
        'DISCOVERED': ['ANALYZED', 'ARCHIVED'],
        'ANALYZED': ['RESEARCHING', 'ARCHIVED'],
        'RESEARCHING': ['SCRIPTING', 'ARCHIVED'],
        'SCRIPTING': ['FILMED', 'ARCHIVED'],
        'FILMED': ['PUBLISHED', 'ARCHIVED'],
        'PUBLISHED': ['ARCHIVED'],
        'ARCHIVED': []
    }

    def __init__(self, db):
        self.db = db

    def get_state(self, keyword_id: int) -> str:
        """Get current lifecycle state for keyword."""
        result = self.db._conn.execute(
            "SELECT lifecycle_state FROM keywords WHERE id = ?",
            (keyword_id,)
        ).fetchone()

        return result[0] if result else 'DISCOVERED'

    def transition(self, keyword_id: int, new_state: str) -> Dict:
        """
        Transition keyword to new state with validation.

        Returns:
            {'status': 'transitioned', 'from': str, 'to': str, 'timestamp': str}
            or {'error': str} if invalid transition
        """
        if new_state not in self.STATES:
            return {'error': f'Invalid state: {new_state}'}

        current_state = self.get_state(keyword_id)

        # Validate transition
        allowed = self.TRANSITIONS.get(current_state, [])
        if new_state not in allowed:
            return {
                'error': f'Invalid transition from {current_state} to {new_state}',
                'allowed': allowed
            }

        # Update database
        timestamp = datetime.utcnow().isoformat()
        self.db._conn.execute(
            """
            UPDATE keywords
            SET lifecycle_state = ?,
                lifecycle_updated_at = ?
            WHERE id = ?
            """,
            (new_state, timestamp, keyword_id)
        )
        self.db._conn.commit()

        # Log transition
        self.db._conn.execute(
            """
            INSERT INTO lifecycle_history (keyword_id, from_state, to_state, transitioned_at)
            VALUES (?, ?, ?, ?)
            """,
            (keyword_id, current_state, new_state, timestamp)
        )
        self.db._conn.commit()

        return {
            'status': 'transitioned',
            'from': current_state,
            'to': new_state,
            'timestamp': timestamp
        }

    def get_by_state(self, state: str, limit: int = 50) -> List[Dict]:
        """Get all keywords in a specific lifecycle state."""
        results = self.db._conn.execute(
            """
            SELECT k.*, o.opportunity_score, o.opportunity_category
            FROM keywords k
            LEFT JOIN opportunity_scores o ON k.id = o.keyword_id
            WHERE k.lifecycle_state = ?
            ORDER BY o.opportunity_score DESC NULLS LAST
            LIMIT ?
            """,
            (state, limit)
        ).fetchall()

        return [dict(row) for row in results]
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| TOPSIS scoring | SAW for simplicity | 2020s | Simpler implementation, easier validation |
| Full state machine library | Database state tracking | Ongoing | Fewer dependencies, simpler for linear flows |
| Manual report formatting | Jinja2 templates | Industry standard | Maintainable, testable templates |
| Scoring all topics | Hard constraint pre-filtering | Best practice | Prevents wasted effort on blocked topics |

**Deprecated/outdated:**
- **AHP (Analytic Hierarchy Process):** Too complex for 4 criteria, requires pairwise comparisons
- **Async state machines:** Overkill for sequential, user-driven transitions

## Open Questions

Things that couldn't be fully resolved:

1. **Optimal weight distribution**
   - What we know: Equal weights (0.33 each) is safe starting point
   - What's unclear: Whether demand should outweigh fit or vice versa
   - Recommendation: Start equal, adjust after 10-20 videos published (validation loop in v1.4)

2. **Data freshness thresholds**
   - What we know: 7 days is standard for trend data
   - What's unclear: Should competition data have shorter refresh cycle (24 hours)?
   - Recommendation: Use 7 days consistently for v1.3, revisit if competition changes rapidly

3. **State transition automation**
   - What we know: Manual transitions prevent errors
   - What's unclear: Could file existence auto-trigger states (script.md → SCRIPTING)?
   - Recommendation: Keep manual for v1.3, consider auto-detection in v1.4

4. **Channel DNA rule completeness**
   - What we know: Core patterns identified (clickbait, news-first, politician-focus)
   - What's unclear: Are there edge cases not covered?
   - Recommendation: Start with documented patterns, expand based on user feedback

## Sources

### Primary (HIGH confidence)
- [Multi-Criteria Decision Making in Python - Sustainability Methods](https://sustainabilitymethods.org/index.php/Multi-Criteria_Decision_Making_in_Python) - MCDM overview
- [pymcdm library on PyPI](https://pypi.org/project/pymcdm/) - Python MCDM implementation
- [python-statemachine documentation](https://python-statemachine.readthedocs.io/en/latest/readme.html) - State machine patterns

### Secondary (MEDIUM confidence)
- [Opportunity Scoring Model - Product Management](https://www.productlift.dev/glossary/opportunity-scoring-model) - Industry formula patterns
- [Opportunity Scorecard Framework](https://www.businessinitiative.org/business-tips/opportunity-scorecard-ranking-ideas-market-size-fit-competition/) - Multi-criteria scoring
- [State Pattern in Python](https://auth0.com/blog/state-pattern-in-python/) - Implementation patterns

### Tertiary (LOW confidence)
- Existing codebase patterns (database.py, demand.py, competition.py) - Verified via code reading

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - Libraries well-documented, widely used
- Architecture: HIGH - Patterns proven in codebase (database.py) and industry
- Pitfalls: HIGH - Based on MCDM best practices and domain knowledge
- Scoring formula: MEDIUM - Weights need validation with real data

**Research date:** 2026-02-01
**Valid until:** 2026-03-01 (30 days - stable domain)
