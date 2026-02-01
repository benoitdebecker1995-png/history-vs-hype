"""
Opportunity Scorer Module

Combines demand (Phase 15), competition (Phase 16), and format (Phase 17) data
into a single opportunity score using SAW (Simple Additive Weighting) formula.

Formula: score = (demand × w1) + (gap × w2) + (fit × w3)

Where:
- demand = search_volume_proxy (0-100)
- gap = differentiation_score (0-1, normalized to 0-100)
- fit = document_score (0-4, normalized to 0-100)

Hard constraints (animation required, channel DNA violations) filter BEFORE scoring.

Usage:
    from tools.discovery.opportunity import OpportunityScorer
    from tools.discovery.database import KeywordDB

    db = KeywordDB()
    scorer = OpportunityScorer(db)
    result = scorer.score_opportunity(keyword_id, demand_data, comp_data, constraints)

    if result['is_blocked']:
        print(f"Blocked: {result['block_reason']}")
    else:
        print(f"Score: {result['opportunity_score']} ({result['category']})")
"""

from typing import Dict, Optional, Any, Tuple
from datetime import datetime


# Channel DNA patterns - WARNING only (not hard blocks)
# For channels still building audience, these are advisory.
# Enable hard blocking via CHANNEL_DNA_BLOCK_ENABLED = True once audience is established.
CHANNEL_DNA_BLOCK_ENABLED = False  # Set True once you know what your audience wants

CHANNEL_DNA_VIOLATIONS = {
    'clickbait': [
        'secret', 'hidden', 'shocking', "you won't believe",
        "they don't want", 'conspiracy', 'revealed'
    ],
    'news_first': [
        'breaking:', 'latest', 'just announced', 'breaking news'
    ],
    'politician_focus': [
        'trump', 'biden', 'netanyahu', 'putin', 'xi jinping'
    ]
}


class OpportunityScorer:
    """
    Calculate opportunity scores using weighted SAW formula.

    Hard constraints (animation required, channel DNA violations) filter
    BEFORE scoring. Blocked topics return score=None.

    Scoring uses configurable weights (default balanced across demand, gap, fit).
    """

    def __init__(self, db, weights: Optional[Dict[str, float]] = None):
        """
        Initialize opportunity scorer.

        Args:
            db: KeywordDB instance
            weights: Optional weight dict {'demand': float, 'gap': float, 'fit': float}
                     Default: demand=0.33, gap=0.33, fit=0.34

        Raises:
            ValueError: If weights don't sum to 1.0
        """
        self.db = db

        # Default weights (balanced, with slight preference for fit)
        self.weights = weights or {
            'demand': 0.33,
            'gap': 0.33,
            'fit': 0.34  # Slightly higher for channel focus on document-heavy
        }

        # Validate weights sum to 1.0
        total = sum(self.weights.values())
        if not (0.99 <= total <= 1.01):
            raise ValueError(f"Weights must sum to 1.0, got {total}")

    def _violates_channel_dna(self, keyword: str) -> Tuple[bool, str, str]:
        """
        Check if keyword violates channel DNA rules.

        Per CLAUDE.md Channel DNA:
        - No clickbait language ("secret", "hidden", "they don't want you to know")
        - No news-first framing ("Breaking:", "Why [Country] Just Did X")
        - No current politician as main subject (starting with politician name)

        Args:
            keyword: Keyword text to check

        Returns:
            Tuple of (is_violation: bool, violation_type: str, matched_keyword: str)

        Example:
            is_viol, vtype, matched = scorer._violates_channel_dna("secret history")
            # Returns: (True, 'clickbait', 'secret')
        """
        keyword_lower = keyword.lower()

        # Check clickbait keywords
        for word in CHANNEL_DNA_VIOLATIONS['clickbait']:
            if word in keyword_lower:
                return (True, 'clickbait', word)

        # Check news-first framing
        for pattern in CHANNEL_DNA_VIOLATIONS['news_first']:
            if pattern in keyword_lower:
                return (True, 'news_first', pattern)

        # Check politician focus (only if keyword STARTS WITH politician name)
        for politician in CHANNEL_DNA_VIOLATIONS['politician_focus']:
            if keyword_lower.startswith(politician):
                return (True, 'politician_focus', politician)

        return (False, '', '')

    def score_opportunity(
        self,
        keyword_id: int,
        demand_data: Dict,
        competition_data: Dict,
        constraints: Optional[Dict]
    ) -> Dict[str, Any]:
        """
        Calculate opportunity score from aggregated data.

        STEP 1: Hard constraints (pre-filter)
            - If constraints['is_production_blocked'] True: return score=None
            - If _violates_channel_dna(): return score=None

        STEP 2: Normalize inputs
            - demand_normalized = demand_data['search_volume_proxy'] (already 0-100)
            - gap_normalized = competition_data['differentiation_score'] * 100 (0-1 to 0-100)
            - fit_normalized = constraints['document_score'] * 25 (0-4 to 0-100)

        STEP 3: Calculate weighted SAW score
            - opportunity_score = sum(normalized * weight for each component)

        STEP 4: Categorize per RESEARCH.md thresholds
            - >=70: 'Excellent', >=50: 'Good', >=30: 'Fair', <30: 'Poor'

        STEP 5: Track max data_age_days across all inputs

        Args:
            keyword_id: Keyword ID from database
            demand_data: Demand analysis result from Phase 15
            competition_data: Competition analysis result from Phase 16
            constraints: Production constraints from Phase 17 (optional)

        Returns:
            {
                'keyword': str,
                'opportunity_score': float,  # 0-100 or None if blocked
                'category': str,  # 'Excellent', 'Good', 'Fair', 'Poor', 'Blocked'
                'is_blocked': bool,
                'block_reason': Optional[str],
                'components': {
                    'demand': {'raw': float, 'normalized': float, 'weight': float, 'contribution': float},
                    'gap': {...},
                    'fit': {...}
                },
                'warnings': List[str],
                'data_age_days': int
            }

        Example:
            result = scorer.score_opportunity(
                keyword_id=5,
                demand_data={'search_volume_proxy': 70, 'keyword': 'test'},
                competition_data={'differentiation_score': 0.8},
                constraints={'document_score': 3, 'is_production_blocked': False}
            )
            # Returns: {'opportunity_score': ~74, 'category': 'Excellent', ...}
        """
        keyword = demand_data['keyword']
        warnings = list(demand_data.get('warnings') or [])

        # STEP 1: HARD CONSTRAINTS (pre-filter)

        # Check production blocking (animation required)
        if constraints and constraints.get('is_production_blocked'):
            return {
                'keyword': keyword,
                'opportunity_score': None,
                'category': 'Blocked',
                'is_blocked': True,
                'block_reason': 'Animation required',
                'components': {},
                'warnings': warnings,
                'data_age_days': 0
            }

        # Check channel DNA violations (warning only unless blocking enabled)
        is_violation, vtype, matched = self._violates_channel_dna(keyword)
        if is_violation:
            if CHANNEL_DNA_BLOCK_ENABLED:
                return {
                    'keyword': keyword,
                    'opportunity_score': None,
                    'category': 'Blocked',
                    'is_blocked': True,
                    'block_reason': f'Channel DNA violation: {vtype} ("{matched}")',
                    'components': {},
                    'warnings': warnings,
                    'data_age_days': 0
                }
            else:
                # Advisory warning for channels still building audience
                warnings.append(f'Channel DNA advisory: {vtype} pattern detected ("{matched}") - consider if this fits your channel voice')

        # STEP 2: NORMALIZE INPUTS

        # Demand: autocomplete position proxy (already 0-100)
        demand_raw = demand_data.get('search_volume_proxy', 0)
        demand_normalized = demand_raw  # Already 0-100

        # Gap: differentiation score (0-1, scale to 0-100)
        gap_raw = competition_data.get('differentiation_score', 0)
        gap_normalized = gap_raw * 100

        # Fit: document score (0-4, scale to 0-100)
        fit_raw = constraints.get('document_score', 2) if constraints else 2
        fit_normalized = fit_raw * 25  # 0→0, 4→100

        # STEP 3: CALCULATE WEIGHTED SAW SCORE

        opportunity_score = (
            demand_normalized * self.weights['demand'] +
            gap_normalized * self.weights['gap'] +
            fit_normalized * self.weights['fit']
        )

        # STEP 4: CATEGORIZE

        if opportunity_score >= 70:
            category = 'Excellent'
        elif opportunity_score >= 50:
            category = 'Good'
        elif opportunity_score >= 30:
            category = 'Fair'
        else:
            category = 'Poor'

        # STEP 5: TRACK DATA AGE

        data_age_days = max(
            demand_data.get('data_age_days', 0),
            constraints.get('data_age_days', 0) if constraints else 0
        )

        # Add warning if data is stale
        if data_age_days > 7:
            warnings.append(f"Data is {data_age_days} days old (>7 days)")

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
                    'contribution': round(demand_normalized * self.weights['demand'], 1)
                },
                'gap': {
                    'raw': gap_raw,
                    'normalized': gap_normalized,
                    'weight': self.weights['gap'],
                    'contribution': round(gap_normalized * self.weights['gap'], 1)
                },
                'fit': {
                    'raw': fit_raw,
                    'normalized': fit_normalized,
                    'weight': self.weights['fit'],
                    'contribution': round(fit_normalized * self.weights['fit'], 1)
                }
            },
            'warnings': warnings,
            'data_age_days': data_age_days
        }

    def save_opportunity_score(self, keyword_id: int, score_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Save opportunity score to database and transition lifecycle state.

        Updates keywords table with opportunity_score_final and opportunity_category.
        Also saves detailed components to opportunity_scores table.
        Transitions lifecycle state to 'ANALYZED' if currently 'DISCOVERED'.

        Args:
            keyword_id: Keyword ID from database
            score_result: Result dict from score_opportunity()

        Returns:
            {'status': 'saved', 'keyword_id': int} on success
            {'error': msg} on failure

        Example:
            result = scorer.score_opportunity(5, demand_data, comp_data, constraints)
            save_result = scorer.save_opportunity_score(5, result)
        """
        try:
            cursor = self.db._conn.cursor()
            now = datetime.utcnow().date().isoformat()

            # Update keywords table with final score
            cursor.execute(
                """
                UPDATE keywords
                SET opportunity_score_final = ?,
                    opportunity_category = ?
                WHERE id = ?
                """,
                (score_result.get('opportunity_score'), score_result.get('category'), keyword_id)
            )

            # Save detailed components to opportunity_scores table
            if not score_result['is_blocked']:
                components = score_result['components']
                demand_score = components['demand']['normalized']
                gap_score = components['gap']['normalized']

                # Use opportunity_score as ratio for compatibility with existing table
                opportunity_ratio = score_result['opportunity_score'] / 100.0

                cursor.execute(
                    """
                    INSERT INTO opportunity_scores (keyword_id, demand_score, competition_score, opportunity_ratio, opportunity_category, calculated_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (keyword_id, demand_score, gap_score, opportunity_ratio, score_result['category'], now)
                )

            self.db._conn.commit()

            # Transition lifecycle state to ANALYZED if currently DISCOVERED
            current_state = self.db.get_lifecycle_state(keyword_id)
            if current_state == 'DISCOVERED':
                self.db.set_lifecycle_state(keyword_id, 'ANALYZED')

            return {'status': 'saved', 'keyword_id': keyword_id}

        except Exception as e:
            return {'error': 'Failed to save opportunity score', 'details': str(e)}
