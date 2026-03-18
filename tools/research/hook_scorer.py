"""
Hook Variant Scorer — scores opening hooks against measured channel data.

Given a hook text, scores it on:
- Document Reveal framework completeness (anomaly, stakes, inciting_incident)
- Opening word patterns (specific number, shocking verb, abstract start)
- First evidence timing (attributed quote within ~90 seconds / ~225 words)
- Information gap strength
- Authority signal presence
- Title fulfillment (entity echo + promise-type alignment) — optional, requires title param
- Style recommendation (topic-type based, from HOOK-PATTERN-LIBRARY.md) — optional, requires topic_type param

Usage:
    from tools.research.hook_scorer import score_hook, rank_hooks
    score = score_hook(hook_text)
    score = score_hook(hook_text, title='Spain vs Portugal', topic_type='territorial')
    ranked = rank_hooks([hook_a, hook_b, hook_c, hook_d, hook_e])

Called by: /script --hooks
"""

import re
from pathlib import Path
from typing import Dict, List, Any, Optional


# ---------------------------------------------------------------------------
# Pattern library loader
# ---------------------------------------------------------------------------

def _load_pattern_library() -> Dict[str, Any]:
    """Load HOOK-PATTERN-LIBRARY.md and parse pattern sections.

    Returns dict keyed by pattern name with:
        - topic_types: list of topic types
        - examples: list of first-sentence strings
        - count: number of examples
        - confidence: 'high' (7+), 'low' (<5), or 'medium' (5-6)
    """
    # Resolve relative to repo root (this file is at tools/research/hook_scorer.py)
    repo_root = Path(__file__).resolve().parents[2]
    library_path = repo_root / '.claude' / 'REFERENCE' / 'HOOK-PATTERN-LIBRARY.md'

    if not library_path.exists():
        return {}

    try:
        text = library_path.read_text(encoding='utf-8')
    except Exception:
        return {}

    patterns: Dict[str, Any] = {}
    current_pattern = None
    in_examples = False
    topic_types: List[str] = []
    examples: List[str] = []

    for line in text.splitlines():
        # New pattern section
        m = re.match(r'^## Pattern:\s+(\S+)', line)
        if m:
            # Save previous pattern
            if current_pattern is not None:
                count = len(examples)
                patterns[current_pattern] = {
                    'topic_types': topic_types,
                    'examples': examples,
                    'count': count,
                    'confidence': _confidence_from_count(count),
                }
            current_pattern = m.group(1).strip()
            in_examples = False
            topic_types = []
            examples = []
            continue

        if current_pattern is None:
            continue

        # Topic type line
        tt_m = re.match(r'^\*\*Topic type:\*\*\s*(.+)', line)
        if tt_m:
            topic_types = [t.strip() for t in tt_m.group(1).split(',')]
            continue

        # Example block start
        if '### Examples' in line:
            in_examples = True
            continue

        # Trigger mechanism / end of examples
        if in_examples and line.startswith('### '):
            in_examples = False
            continue

        # Parse example lines: "N. Channel: X | Video: Y | Views: Z | First sentence: "text""
        if in_examples:
            fs_m = re.search(r'First sentence:\s+"([^"]+)"', line)
            if fs_m:
                examples.append(fs_m.group(1)[:150])

    # Save last pattern
    if current_pattern is not None:
        count = len(examples)
        patterns[current_pattern] = {
            'topic_types': topic_types,
            'examples': examples,
            'count': count,
            'confidence': _confidence_from_count(count),
        }

    return patterns


def _confidence_from_count(count: int) -> str:
    """Map example count to confidence level."""
    if count >= 7:
        return 'high'
    elif count >= 5:
        return 'medium'
    else:
        return 'low'


# ---------------------------------------------------------------------------
# Document Reveal framework detection
# ---------------------------------------------------------------------------

def _detect_framework(text: str) -> Dict[str, float]:
    """Detect Document Reveal framework elements in a hook.

    Returns dict with anomaly (0-15), stakes (0-15), inciting_incident (0-10).

    Anomaly: Specific year/number, named document/map, hyper-specific place in first ~30 words.
    Stakes: Systemic consequence language in first ~112 words.
    Inciting Incident: Turn/pivot language within first ~112 words.
    """
    words = text.split()
    first_30 = ' '.join(words[:30]).lower()
    first_30_raw = ' '.join(words[:30])
    first_112 = ' '.join(words[:112]).lower()

    # --- Anomaly (0-15) ---
    anomaly = 0.0

    # Specific 3-4 digit number (year) in first 30 words → strong signal
    if re.search(r'\b\d{3,4}\b', first_30):
        anomaly = 15.0
    # Named document keyword in first 30 words
    elif re.search(
        r'\b(?:map|document|treaty|telegram|decree|clause|statute|law|charter|agreement|line|letter)\b',
        first_30,
    ):
        anomaly = 15.0
    # Named entity (capitalized pair) in first 30 words
    elif re.search(r'[A-Z][a-z]+ [A-Z][a-z]+', first_30_raw):
        anomaly = 10.0
    # Any specific number in first 30 words (partial credit)
    elif re.search(r'\b\d+\b', first_30):
        anomaly = 10.0

    # --- Stakes (0-15) ---
    stakes_patterns = [
        r'which meant',
        r'this meant',
        r'this determined',
        r'this controlled',
        r'\bentire\b',
        r'\ball of\b',
        r'\bmillion\b',
        r'\bempire\b',
        r'shut off',
        r'\bresource\b',
        r'\bconsequence\b',
        r'\bcontrolled\b',
        r'systemic',
        r'determined the fate',
        r'fate of',
    ]
    stakes_hits = sum(1 for p in stakes_patterns if re.search(p, first_112))
    if stakes_hits >= 3:
        stakes = 15.0
    elif stakes_hits == 2:
        stakes = 10.0
    elif stakes_hits == 1:
        stakes = 7.0
    else:
        stakes = 0.0

    # --- Inciting Incident (0-10) ---
    inciting_patterns = [
        r'\bbut\b',
        r'\bexcept\b',
        r'\buntil\b',
        r'the problem was',
        r"that's when",
        r"here's what",
        r'what actually',
        r'\bunless\b',
        r'the twist',
        r'the catch',
        r'except (?:one|that)',
    ]
    inciting_hits = sum(1 for p in inciting_patterns if re.search(p, first_112))
    if inciting_hits >= 2:
        inciting_incident = 10.0
    elif inciting_hits == 1:
        inciting_incident = 7.0
    else:
        inciting_incident = 0.0

    return {
        'anomaly': anomaly,
        'stakes': stakes,
        'inciting_incident': inciting_incident,
    }


# ---------------------------------------------------------------------------
# Title fulfillment check
# ---------------------------------------------------------------------------

def _extract_title_entities(title: str) -> List[str]:
    """Extract key entities from a title using EntityExtractor if available."""
    try:
        from tools.production.entities import EntityExtractor
        extractor = EntityExtractor(use_spacy=False)
        entities = extractor.extract(title)
        return [e.text for e in entities]
    except Exception:
        pass

    # Fallback: extract capitalized words/pairs and filter stopwords
    stopwords = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'from', 'into', 'vs', 'vs.', 'how', 'why', 'what',
        'who', 'when', 'where', 'did', 'was', 'were', 'is', 'are', 'been',
        'that', 'this', 'which', 'they', 'their', 'its', 'our',
    }
    entities = []
    words = title.split()
    for w in words:
        clean = re.sub(r'[^a-zA-Z]', '', w)
        if clean and clean[0].isupper() and clean.lower() not in stopwords and len(clean) > 2:
            entities.append(clean)
    return entities


def _classify_promise_type(title: str) -> Optional[str]:
    """Categorize title by the type of promise it makes."""
    lower = title.lower()

    if re.search(r'\b(?:vs|versus|rivalry|divided|split|war|conflict)\b', lower):
        return 'conflict'

    if re.search(r'\b(?:law|treaty|telegram|document|statute|decree|map|charter|agreement)\b', lower):
        return 'document'

    if re.search(r'\b(?:myth|truth|real|actually|wasn\'t|never|wrong|fake|debunk)\b', lower):
        return 'myth-bust'

    if re.search(r'\b(?:how|why|what made|the reason|mechanism|works)\b', lower):
        return 'mechanism'

    return None


def _hook_delivers_promise_type(hook_first_50: str, promise_type: str) -> bool:
    """Check if the hook's opening delivers on the title's promise type."""
    lower = hook_first_50.lower()

    if promise_type == 'conflict':
        # Two entities in opposition — needs at least two capitalized entities
        # and opposition framing
        capitalized = re.findall(r'[A-Z][a-z]+', hook_first_50)
        named_entities = [w for w in capitalized if len(w) > 2]
        has_two_entities = len(set(named_entities)) >= 2
        opposition_words = ['vs', 'versus', 'divided', 'split', 'controlled', 'against',
                            'rivalry', 'conflict', 'war', 'opposed']
        has_opposition = any(w in lower for w in opposition_words)
        return has_two_entities and has_opposition

    if promise_type == 'document':
        doc_words = ['map', 'document', 'treaty', 'law', 'decree', 'statute', 'charter',
                     'telegram', 'clause', 'line', 'agreement']
        return any(w in lower for w in doc_words)

    if promise_type == 'myth-bust':
        myth_words = ["you've heard", 'most people', 'standard answer', 'popular', 'believe',
                      'thought', 'assumed', 'they say', 'it\'s been', 'official']
        return any(w in lower for w in myth_words)

    if promise_type == 'mechanism':
        causal_words = ['because', 'which meant', 'thereby', 'led to', 'resulted in',
                        'caused', 'explains why', 'this is why', 'this is how']
        return any(w in lower for w in causal_words)

    return False


def _describe_hook_opening(hook_first_50: str) -> str:
    """Describe what the hook's opening is doing (for fix suggestion)."""
    lower = hook_first_50.lower()

    if any(w in lower for w in ['throughout history', 'for centuries', 'many people',
                                  'in order to', 'to understand', 'the history of']):
        return 'generic historical context'

    if re.search(r'\b\d{3,4}\b', lower):
        return 'a specific date/year'

    if re.search(r'[A-Z][a-z]+ [A-Z][a-z]+', hook_first_50):
        return 'named entities without framing'

    return 'contextual background'


def _check_fulfillment(text: str, title: str) -> Dict[str, Any]:
    """Check if hook fulfills the title's promises.

    Returns dict with:
        entity_echo: {passed: bool, matched_entities: list, title_entities: list}
        promise_type: {passed: bool, type: str}
        fix_suggestion: str (empty if all pass)
    """
    words = text.split()
    first_50_words = ' '.join(words[:50])
    first_50_lower = first_50_words.lower()

    # --- Entity echo ---
    title_entities = _extract_title_entities(title)
    matched = [e for e in title_entities if e.lower() in first_50_lower]
    entity_echo_passed = len(matched) > 0

    # --- Promise type ---
    promise_type = _classify_promise_type(title)
    if promise_type is None:
        promise_type_passed = True  # no detectable promise = no mismatch
    else:
        promise_type_passed = _hook_delivers_promise_type(first_50_words, promise_type)

    # --- Fix suggestion ---
    fix = ''
    if not entity_echo_passed or not promise_type_passed:
        entity_str = ', '.join(title_entities[:3]) if title_entities else 'key entities'
        hook_doing = _describe_hook_opening(first_50_words)

        if not entity_echo_passed and not promise_type_passed:
            fix = (
                f"Title promises {promise_type or 'specific content'} about "
                f"{entity_str}, but hook opens with {hook_doing}. "
                f"Try: name {entity_str} in the first sentence and open with "
                f"{'a specific number or date' if promise_type == 'conflict' else 'the document/event that creates the conflict'}."
            )
        elif not entity_echo_passed:
            fix = (
                f"Title mentions {entity_str} but hook doesn't name them in the "
                f"first 50 words. Try: start with a sentence that names "
                f"{entity_str} directly."
            )
        else:
            fix = (
                f"Title promises {promise_type} content but hook opens with "
                f"{hook_doing}. Try: open with "
                f"{'the conflict between the two sides' if promise_type == 'conflict' else 'the specific document or mechanism'}."
            )

    return {
        'entity_echo': {
            'passed': entity_echo_passed,
            'matched_entities': matched,
            'title_entities': title_entities,
        },
        'promise_type': {
            'passed': promise_type_passed,
            'type': promise_type,
        },
        'fix_suggestion': fix,
    }


# ---------------------------------------------------------------------------
# Style recommendation
# ---------------------------------------------------------------------------

# Topic type → recommended hook pattern mapping
TOPIC_STYLE_MAP = {
    'territorial': 'cold_fact',
    'ideological': 'myth_contradiction',
    'political_fact_check': 'specificity_bomb',
    'general': None,
}

# Score threshold for pattern library confidence
_HIGH_CONFIDENCE_MIN = 7
_LOW_CONFIDENCE_MAX = 4


def _detect_hook_style(text: str, pattern_library: Dict[str, Any]) -> str:
    """Detect what style a hook is using based on its opening.

    Returns pattern name or 'unknown'.
    """
    words = text.split()
    first_30_lower = ' '.join(words[:30]).lower()
    first_30_raw = ' '.join(words[:30])

    # cold_fact: specific year/number in first sentence
    if re.search(r'\b\d{3,4}\b', first_30_lower):
        return 'cold_fact'

    # specificity_bomb: named place or document (no number required)
    if re.search(r'[A-Z][a-z]+ [A-Z][a-z]+', first_30_raw):
        return 'specificity_bomb'

    # myth_contradiction: standard answer / most people framing
    lower_all = text[:300].lower()
    myth_signals = ['standard answer', 'most people', "you've heard", 'popular version',
                    'textbook', 'the myth', 'everyone thinks', 'you\'d think']
    if any(s in lower_all for s in myth_signals):
        return 'myth_contradiction'

    # contextual_opening: philosophical question or broad framing
    if re.search(r'\b(?:throughout history|for centuries|many people|it is often|history of|what makes|what ties)\b',
                 first_30_lower):
        return 'contextual_opening'

    return 'unknown'


def _build_style_recommendation(
    text: str,
    topic_type: str,
    pattern_library: Dict[str, Any],
) -> Dict[str, Any]:
    """Build style recommendation for the given topic type.

    Returns dict with:
        recommended: str or None
        confidence: 'high' | 'medium' | 'low' | 'none'
        examples: list of example first sentences
        score_modifier: int (+5, -5, or 0)
        detected_style: str
    """
    recommended = TOPIC_STYLE_MAP.get(topic_type)

    if not recommended:
        return {
            'recommended': None,
            'confidence': 'none',
            'examples': [],
            'score_modifier': 0,
            'detected_style': 'unknown',
        }

    # Get pattern data
    pattern_data = pattern_library.get(recommended, {})
    count = pattern_data.get('count', 0)
    confidence = pattern_data.get('confidence', 'low') if pattern_data else 'low'
    examples = pattern_data.get('examples', [])[:3]

    # Detect what style the hook is actually using
    detected_style = _detect_hook_style(text, pattern_library)

    # Score modifier — only applies at HIGH confidence (7+ examples)
    score_modifier = 0
    if confidence == 'high':
        if detected_style == recommended:
            score_modifier = 5
        else:
            score_modifier = -5
    # LOW confidence (<5 examples) → advisory only, no score change

    return {
        'recommended': recommended,
        'confidence': confidence,
        'examples': examples,
        'score_modifier': score_modifier,
        'detected_style': detected_style,
    }


# ---------------------------------------------------------------------------
# Topic detection from script content
# ---------------------------------------------------------------------------

TOPIC_KEYWORDS = {
    'territorial': [
        'border', 'territory', 'territorial', 'frontier', 'boundary', 'dispute',
        'treaty', 'map', 'land', 'claim', 'occupation', 'sovereignty', 'zone',
        'region', 'demarcation', 'partition', 'annexation', 'secession', 'colony',
        'colonial', 'empire', 'mandate', 'protectorate',
    ],
    'ideological': [
        'myth', 'ideology', 'propaganda', 'narrative', 'belief', 'misconception',
        'revisionism', 'nationalism', 'religion', 'culture', 'identity', 'politics',
        'movement', 'manifesto', 'doctrine', 'philosophy', 'tradition', 'ideology',
        'perception', 'rhetoric',
    ],
    'political_fact_check': [
        'parliament', 'congress', 'legislation', 'bill', 'vote', 'election',
        'administration', 'policy', 'government', 'president', 'minister',
        'senator', 'ruling', 'statute', 'law', 'constitution', 'judicial',
        'court', 'verdict', 'decree', 'executive', 'sanction',
    ],
}


def detect_topic_from_script(text: str) -> str:
    """Detect topic type from script text via keyword matching.

    Checks first 2000 characters. Returns 'territorial', 'ideological',
    'political_fact_check', or 'general'.

    Exported for use by /script --hooks command (Plan 02).
    """
    if not text:
        return 'general'

    sample = text[:2000].lower()
    scores: Dict[str, int] = {k: 0 for k in TOPIC_KEYWORDS}

    for topic, keywords in TOPIC_KEYWORDS.items():
        for kw in keywords:
            scores[topic] += len(re.findall(r'\b' + re.escape(kw) + r'\b', sample))

    best_topic = max(scores, key=lambda k: scores[k])
    if scores[best_topic] == 0:
        return 'general'

    return best_topic


# ---------------------------------------------------------------------------
# Main scoring function
# ---------------------------------------------------------------------------

def score_hook(
    text: str,
    label: str = '',
    title: Optional[str] = None,
    topic_type: Optional[str] = None,
) -> Dict[str, Any]:
    """Score a single hook against channel data patterns.

    Args:
        text: The hook text to score.
        label: Optional label for display.
        title: Video title — enables fulfillment check (entity echo + promise type).
        topic_type: Topic type — enables style recommendation. One of:
            'territorial', 'ideological', 'political_fact_check', 'general'.

    Returns dict with:
        - total_score (0-100)
        - framework_score (0-40) — Document Reveal framework
        - framework: {anomaly: float, stakes: float, inciting_incident: float}
        - pattern_score (0-30) — opening word patterns
        - authority_score (0-15) — first-person research signal
        - gap_score (0-15) — information gap strength
        - issues: list of problems
        - strengths: list of positives
        - fulfillment (only when title provided): entity echo + promise type results
        - style_recommendation (only when topic_type provided): style + confidence + examples
    """
    result: Dict[str, Any] = {
        'label': label,
        'total_score': 0,
        'framework_score': 0,
        'framework': {},
        'pattern_score': 0,
        'authority_score': 0,
        'gap_score': 0,
        'issues': [],
        'strengths': [],
    }

    if not text or len(text.split()) < 20:
        result['issues'].append('Hook too short to evaluate')
        return result

    lower = text.lower()
    words = text.split()
    first_50 = ' '.join(words[:50]).lower()

    # Load pattern library (needed for style recommendation)
    pattern_library = _load_pattern_library()

    # --- Framework score (0-40) — replaces beat_score ---
    framework = _detect_framework(text)
    result['framework'] = framework
    framework_score = int(framework['anomaly'] + framework['stakes'] + framework['inciting_incident'])
    framework_score = max(0, min(40, framework_score))
    result['framework_score'] = framework_score

    # Strengths / issues for framework elements
    if framework['anomaly'] >= 10:
        result['strengths'].append('Anomaly: specific number/document in opening')
    else:
        result['issues'].append('Missing anomaly: add specific year, number, or named document in first 30 words')

    if framework['stakes'] >= 7:
        result['strengths'].append('Stakes: systemic consequence language present')
    else:
        result['issues'].append('Missing stakes: add consequence language ("which meant", "entire", "million")')

    if framework['inciting_incident'] >= 7:
        result['strengths'].append('Inciting incident: pivot language present')
    else:
        result['issues'].append('Missing inciting incident: add pivot language ("but", "except", "the problem was")')

    # --- Pattern score (0-30) ---
    pattern = 0

    # Specific number in first 50 words (+10)
    if re.search(r'\b\d+\b', first_50):
        pattern += 10
        result['strengths'].append('Specific number in opening')

    # Shocking/active verb (+10)
    shock_verbs = [
        'divided', 'split', 'stripped', 'destroyed', 'invaded',
        'erased', 'killed', 'conquered', 'betrayed', 'weaponized',
        'funded', 'signed away', 'collapsed', 'drew', 'forced',
        'imposed', 'expelled', 'suppressed', 'deleted', 'ignored',
    ]
    if any(v in first_50 for v in shock_verbs):
        pattern += 10
        result['strengths'].append('Shocking verb in opening')

    # Visual/concrete detail (+10)
    visual_patterns = [
        r'open a (?:map|document|language|chart|graph|image)',
        r'look at', r'this document', r'this map',
        r'\[b-roll', r'\[visual', r'\[map', r'on screen',
        r'zoom in', r'language map', r'here is the', r'here\'s the',
    ]
    if any(re.search(p, lower) for p in visual_patterns):
        pattern += 10
        result['strengths'].append('Visual/concrete detail in opening')

    # Negative: abstract start (-15)
    abstract_starts = [
        'to understand', 'the concept', 'in order to', 'throughout history',
        'for centuries', 'many people believe', 'it is often said',
        'history is', 'the history of',
    ]
    if any(first_50.startswith(a) for a in abstract_starts):
        pattern -= 15
        result['issues'].append('Opens with abstract context (correlates with <25% retention)')

    result['pattern_score'] = max(0, min(30, pattern))

    # --- Authority score (0-15) ---
    authority = 0
    authority_patterns = [
        r'so i ', r'i read', r'i went to', r'i found', r'i checked',
        r'i pulled', r'i looked at', r'i actually',
    ]
    if any(re.search(p, lower) for p in authority_patterns):
        authority += 10
        result['strengths'].append('First-person authority signal')
    else:
        result['issues'].append('No first-person authority marker (I read/found/checked)')

    # Academic source named
    if re.search(r'(?:according to|writes that|writes in|argues that|notes that)', lower):
        authority += 5
        result['strengths'].append('Named academic source')

    result['authority_score'] = min(15, authority)

    # --- Information gap score (0-15) ---
    gap = 0

    # Question that creates curiosity
    if '?' in text:
        gap += 5

    # Contradiction that opens a gap
    gap_phrases = [
        r'that answer is incomplete', r'both .* wrong', r'here\'s the part',
        r'nobody .* mention', r'usually gets left out', r'the rest of the story',
        r'but .*didn\'t', r'but .*couldn\'t', r'but .*wasn\'t',
    ]
    if any(re.search(p, lower) for p in gap_phrases):
        gap += 10
        result['strengths'].append('Strong information gap')
    elif framework['inciting_incident'] > 0:
        # Inciting incident implies an information gap
        gap += 5

    result['gap_score'] = min(15, gap)

    # --- Base total ---
    base_total = (
        result['framework_score']
        + result['pattern_score']
        + result['authority_score']
        + result['gap_score']
    )

    # --- Style recommendation (optional) ---
    if topic_type is not None:
        style_rec = _build_style_recommendation(text, topic_type, pattern_library)
        result['style_recommendation'] = style_rec
        # Apply score modifier (high confidence only, capped at 0-100)
        base_total += style_rec['score_modifier']

    # Cap total at 0-100
    result['total_score'] = max(0, min(100, base_total))

    # --- Fulfillment check (optional) ---
    if title is not None:
        result['fulfillment'] = _check_fulfillment(text, title)

    return result


# ---------------------------------------------------------------------------
# Ranking and formatting
# ---------------------------------------------------------------------------

def rank_hooks(
    hooks: List[Dict[str, str]],
    title: Optional[str] = None,
    topic_type: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Score and rank multiple hook variants.

    Args:
        hooks: list of dicts with 'label' and 'text' keys
        title: optional title for fulfillment check (passed through to score_hook)
        topic_type: optional topic type for style recommendation

    Returns:
        List of scored hooks sorted by total_score descending
    """
    scored = []
    for hook in hooks:
        result = score_hook(
            hook['text'],
            label=hook.get('label', ''),
            title=title,
            topic_type=topic_type,
        )
        result['text_preview'] = ' '.join(hook['text'].split()[:30]) + '...'
        scored.append(result)

    scored.sort(key=lambda x: x['total_score'], reverse=True)

    # Add rank
    for i, s in enumerate(scored, 1):
        s['rank'] = i

    return scored


def format_hook_ranking(ranked: List[Dict[str, Any]]) -> str:
    """Format ranked hooks as a comparison table.

    Shows Framework column (not Beats). Includes fulfillment and style
    recommendation columns when present.
    """
    has_fulfillment = any('fulfillment' in h for h in ranked)
    has_style = any('style_recommendation' in h for h in ranked)

    # Build header
    header_cols = ['Rank', 'Label', 'Score', 'Framework', 'Pattern', 'Authority', 'Gap', 'Key Issue']
    if has_fulfillment:
        header_cols.insert(4, 'Fulfillment')
    if has_style:
        header_cols.insert(4 if not has_fulfillment else 5, 'Style')

    sep = ['------' for _ in header_cols]
    lines = [
        '# Hook Variant Comparison',
        '',
        '| ' + ' | '.join(header_cols) + ' |',
        '| ' + ' | '.join(sep) + ' |',
    ]

    for h in ranked:
        framework_str = f"{h['framework_score']}/40"
        issue = h['issues'][0] if h['issues'] else 'None'
        if len(issue) > 40:
            issue = issue[:37] + '...'

        row_parts = [
            str(h['rank']),
            h['label'],
            f"**{h['total_score']}**",
            framework_str,
            str(h['pattern_score']),
            str(h['authority_score']),
            str(h['gap_score']),
        ]

        if has_fulfillment:
            f_data = h.get('fulfillment', {})
            entity_ok = 'Y' if f_data.get('entity_echo', {}).get('passed') else 'N'
            promise_ok = 'Y' if f_data.get('promise_type', {}).get('passed') else 'N'
            row_parts.insert(3, f"E:{entity_ok} P:{promise_ok}")

        if has_style:
            s_data = h.get('style_recommendation', {})
            rec = s_data.get('recommended') or 'none'
            mod = s_data.get('score_modifier', 0)
            mod_str = f"+{mod}" if mod > 0 else str(mod)
            idx = 4 if has_fulfillment else 3
            row_parts.insert(idx, f"{rec}({mod_str})")

        row_parts.append(issue)
        lines.append('| ' + ' | '.join(row_parts) + ' |')

    lines.extend(['', '---', ''])

    # Detailed breakdown for top 3
    for h in ranked[:3]:
        lines.append(f"## {h['label']} (Score: {h['total_score']}/100)")
        lines.append('')
        lines.append(f"**Preview:** {h['text_preview']}")
        lines.append('')
        if h['strengths']:
            lines.append(f"**Strengths:** {', '.join(h['strengths'])}")
        if h['issues']:
            lines.append(f"**Issues:** {', '.join(h['issues'])}")
        lines.append('')

        # Framework breakdown
        fw = h.get('framework', {})
        fw_str = (
            f"Anomaly: {fw.get('anomaly', 0):.0f}/15 | "
            f"Stakes: {fw.get('stakes', 0):.0f}/15 | "
            f"Inciting: {fw.get('inciting_incident', 0):.0f}/10"
        )
        lines.append(f"**Framework:** {fw_str}")

        # Fulfillment breakdown
        if 'fulfillment' in h:
            ful = h['fulfillment']
            echo = ful['entity_echo']
            ptype = ful['promise_type']
            lines.append(
                f"**Fulfillment:** Entity echo {'PASS' if echo['passed'] else 'FAIL'} "
                f"({', '.join(echo['matched_entities']) or 'none'}) | "
                f"Promise type {'PASS' if ptype['passed'] else 'FAIL'} ({ptype.get('type', 'N/A')})"
            )
            if ful.get('fix_suggestion'):
                lines.append(f"**Fix:** {ful['fix_suggestion']}")

        # Style recommendation
        if 'style_recommendation' in h:
            sr = h['style_recommendation']
            lines.append(
                f"**Style:** Recommended {sr.get('recommended', 'none')} "
                f"({sr.get('confidence', 'none')} confidence) | "
                f"Detected {sr.get('detected_style', 'unknown')} | "
                f"Modifier: {sr.get('score_modifier', 0):+d}"
            )

        lines.append('')

    # Recommendation
    winner = ranked[0]
    lines.append('---')
    lines.append('')
    lines.append(f"**Recommended:** {winner['label']} (score {winner['total_score']})")
    if winner['issues']:
        lines.append(f"**Fix before using:** {winner['issues'][0]}")

    return '\n'.join(lines)


# ---------------------------------------------------------------------------
# CLI test
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    # Quick test with the Brazil hook
    test_hook = """
Open a language map of South America. Every country speaks Spanish. Except one.

And the border between Spanish and Portuguese South America isn't a mountain range or a river. It follows an almost perfect north-south line.

That line is a treaty. Signed on June 7th, 1494, in a small Spanish town called Tordesillas. Two countries drew a line through a world they'd never mapped.

The standard answer is: that's why Brazil speaks Portuguese. The pope drew a line. Portugal got the east. Done.

That answer is incomplete. Because in 1494, nobody could actually measure where that line was. Because most of modern Brazil sits on the wrong side of it. And because the people living there weren't speaking Portuguese anyway — until a government decree in 1757 forced them to.

Here's what actually happened. It starts with a wind pattern. And a compromise that accidentally included a continent nobody in Europe knew existed.
"""
    result = score_hook(test_hook, label='Brazil Hook (Current)',
                        title='Why Brazil Speaks Portuguese', topic_type='territorial')
    import json
    print(json.dumps(result, indent=2))
