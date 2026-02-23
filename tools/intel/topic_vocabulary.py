"""
topic_vocabulary.py — Single source of truth for topic classification

Provides unified topic clusters and title formula detection used by both
competitor_patterns.py and topic_scorer.py. Replaces the ad-hoc topic
keywords in pattern_analyzer.py with a richer, channel-DNA-aligned taxonomy.

Public API:
    classify_title(title, description='') -> list[str]
    primary_topic(title, description='') -> str
    detect_formulas(title) -> list[str]
"""

import re

# ---------------------------------------------------------------------------
# Unified topic clusters (channel-DNA aligned)
# ---------------------------------------------------------------------------

UNIFIED_TOPICS: dict[str, list[str]] = {
    "territorial": [
        "border", "territory", "territorial", "boundary", "dispute", "claim",
        "island", "sea", "ocean", "strait", "canal", "zone", "sovereignty",
        "annexation", "annex", "occupation", "occupied", "enclave",
    ],
    "ideological": [
        "myth", "truth", "real", "actually", "really", "fact", "debunk",
        "misconception", "lie", "propaganda", "narrative", "belief",
    ],
    "colonial": [
        "colonial", "colonialism", "colony", "settler", "independence",
        "empire", "imperial", "imperialism", "conquest", "partition",
        "decolonization", "mandate", "protectorate",
    ],
    "politician": [
        "president", "minister", "politician", "election", "vote",
        "government", "congress", "parliament", "senator", "dictator",
        "regime", "policy",
    ],
    "archaeological": [
        "archaeology", "archaeological", "excavation", "artifact", "ruins",
        "ancient", "bronze age", "iron age", "neolithic", "fossil",
    ],
    "medieval": [
        "medieval", "middle ages", "feudal", "crusade", "knight", "castle",
        "byzantine", "carolingian", "viking", "saxon", "norman",
    ],
    "legal": [
        "treaty", "law", "legal", "court", "icj", "ruling", "clause",
        "convention", "constitution", "statute", "jurisdiction", "arbitration",
    ],
    "war": [
        "war", "battle", "invasion", "conflict", "military", "siege",
        "weapon", "army", "navy", "soldier", "warfare", "front",
    ],
    "revolution": [
        "revolution", "revolt", "uprising", "liberation", "coup",
        "overthrow", "insurrection", "rebellion",
    ],
    "religion": [
        "religion", "church", "christian", "islam", "muslim", "jewish",
        "faith", "pope", "mosque", "temple", "scripture", "bible", "quran",
    ],
    "trade": [
        "trade", "silk road", "spice", "merchant", "economy", "commerce",
        "tariff", "sanction", "embargo", "export", "import",
    ],
}

# ---------------------------------------------------------------------------
# Title formula patterns (regex-based)
# ---------------------------------------------------------------------------

TITLE_FORMULAS: dict[str, re.Pattern] = {
    "question":    re.compile(r"\?"),
    "how_why":     re.compile(r"\b(?:how|why)\b", re.IGNORECASE),
    "list":        re.compile(r"\b\d+\s+(?:ways|reasons|things|facts|tips|secrets|steps)\b", re.IGNORECASE),
    "colon_split": re.compile(r"[:\u2014\u2013]"),
    "quote":       re.compile(r'["\u201c\u201d\u2018\u2019]'),
}


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def classify_title(title: str, description: str = "") -> list[str]:
    """
    Return all matching topic cluster names for a title + optional description.

    Searches title first (higher signal), then description for additional matches.
    Returns empty list if nothing matches.
    """
    combined = f"{title} {description}".lower()
    matched = []
    for topic, keywords in UNIFIED_TOPICS.items():
        if any(kw in combined for kw in keywords):
            matched.append(topic)
    return matched


def primary_topic(title: str, description: str = "") -> str:
    """
    Return the single best topic cluster, or 'general' if none match.

    Prioritises title-only matches over description matches.
    """
    # Try title alone first
    title_lower = title.lower()
    for topic, keywords in UNIFIED_TOPICS.items():
        if any(kw in title_lower for kw in keywords):
            return topic
    # Fall back to description
    if description:
        desc_lower = description.lower()
        for topic, keywords in UNIFIED_TOPICS.items():
            if any(kw in desc_lower for kw in keywords):
                return topic
    return "general"


def detect_formulas(title: str) -> list[str]:
    """
    Return all title formula patterns detected in the title.

    Returns ['other'] if no patterns match.
    """
    matched = []
    for name, pattern in TITLE_FORMULAS.items():
        if pattern.search(title):
            matched.append(name)
    return matched or ["other"]
