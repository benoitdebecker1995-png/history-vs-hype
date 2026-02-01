"""
Video Classification Module

Keyword-based classification for competitor video format and content angle detection.
Used in Phase 16 competition analysis to filter and differentiate video strategies.

Usage:
    from classifiers import classify_format, classify_angles

    format_type = classify_format('Why Rome Fell', 'Kraut')  # 'documentary'
    angles = classify_angles('The Treaty That Changed Europe')  # ['legal', 'historical']
"""

from typing import List


# Channel keywords for format classification
ANIMATION_CHANNEL_KEYWORDS = [
    'kurzgesagt',
    'oversimplified',
    'infographics show',
    'simple history',
    'extra credits',
    'ted-ed',
    'minutephysics',
    'cgp grey',
    'casually explained',
    "sam o'nella",
    'alternate history hub',
    'feature history',
    'historia civilis'
]

DOCUMENTARY_CHANNEL_KEYWORDS = [
    'kraut',
    'knowing better',
    'shaun',
    'three arrows',
    'history matters',
    'reallifelore',
    'wendover',
    'caspian report',
    'johnny harris',
    'vox'
]

# Content angle keywords by category
ANGLE_KEYWORDS = {
    'political': [
        'politics', 'political', 'government', 'election', 'party', 'ideology',
        'left', 'right', 'liberal', 'conservative', 'democracy', 'authoritarian',
        'regime', 'president', 'prime minister', 'parliament', 'congress'
    ],
    'legal': [
        'treaty', 'law', 'legal', 'court', 'icj', 'ruling', 'jurisdiction',
        'sovereignty', 'international law', 'constitution', 'rights', 'claim',
        'dispute', 'agreement', 'accord', 'protocol', 'convention'
    ],
    'historical': [
        'history', 'historical', 'ancient', 'medieval', 'century', 'dynasty',
        'empire', 'kingdom', 'war', 'battle', 'civilization', 'colonial',
        'origin', 'rise', 'fall', 'era', 'age', 'period'
    ],
    'economic': [
        'economy', 'economic', 'trade', 'gdp', 'debt', 'money', 'currency',
        'market', 'industry', 'resources', 'oil', 'wealth', 'poverty',
        'development', 'infrastructure', 'sanctions'
    ],
    'geographic': [
        'border', 'territory', 'map', 'region', 'island', 'land', 'sea',
        'ocean', 'mountain', 'river', 'geography', 'location', 'area'
    ]
}


def classify_format(title: str, channel_name: str) -> str:
    """
    Classify video format as animation, documentary, or unknown.

    Uses channel name as primary signal (stronger indicator than title).
    Falls back to title keywords for animation detection if channel unknown.

    Args:
        title: Video title
        channel_name: Channel name

    Returns:
        'animation', 'documentary', or 'unknown'

    Examples:
        >>> classify_format('Why Rome Fell', 'Kraut')
        'documentary'
        >>> classify_format('History of Rome', 'Kurzgesagt')
        'animation'
        >>> classify_format('Random Video', 'Some Channel')
        'unknown'
    """
    title_lower = title.lower()
    channel_lower = channel_name.lower()

    # Check channel name first (strongest signal)
    for channel_keyword in DOCUMENTARY_CHANNEL_KEYWORDS:
        if channel_keyword in channel_lower:
            return 'documentary'

    for channel_keyword in ANIMATION_CHANNEL_KEYWORDS:
        if channel_keyword in channel_lower:
            return 'animation'

    # Fall back to title keywords for animation detection
    animation_title_keywords = ['animated', 'animation', 'cartoon', 'illustrated']
    for keyword in animation_title_keywords:
        if keyword in title_lower:
            return 'animation'

    return 'unknown'


def classify_angles(title: str) -> List[str]:
    """
    Classify video content angles based on title keywords.

    A video can have multiple angles (e.g., both 'legal' and 'historical').
    Returns ['general'] if no specific angle keywords found.

    Args:
        title: Video title

    Returns:
        List of angle categories: ['political', 'legal', 'historical', 'economic', 'geographic']
        or ['general'] if no matches

    Examples:
        >>> classify_angles('The Politics of Rome')
        ['political', 'historical']
        >>> classify_angles('The Treaty That Changed Europe')
        ['legal']
        >>> classify_angles('Random Title')
        ['general']
    """
    title_lower = title.lower()
    matched_angles = []

    # Check each angle category
    for angle_name, keywords in ANGLE_KEYWORDS.items():
        for keyword in keywords:
            if keyword in title_lower:
                matched_angles.append(angle_name)
                break  # One match per category is enough

    # Return general if no specific angles found
    if not matched_angles:
        return ['general']

    return matched_angles
