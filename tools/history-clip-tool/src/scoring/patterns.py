"""
Pattern definitions for historical/academic content detection.
All patterns are explicit and documented for transparency.
"""

import re
from typing import List, Pattern

# ============================================================================
# EVIDENCE MARKERS - Patterns indicating academic rigor
# ============================================================================

# Primary source keywords (treaties, archives, official documents)
PRIMARY_SOURCE_KEYWORDS = [
    "treaty", "treaties",
    "census", "census data",
    "archival", "archive", "archives",
    "manuscript", "manuscripts",
    "document", "documents", "documentation",
    "court", "ruling", "judgment",
    "statute", "law", "legislation",
    "proclamation", "declaration",
    "charter", "constitution",
    "agreement", "accord",
    "protocol", "convention"
]

# Citation language patterns
CITATION_PATTERNS = [
    r"\baccording to\b",
    r"\bpage\s+\d+",
    r"\bchapter\s+\d+",
    r"\bvolume\s+\d+",
    r"\bin\s+[A-Z][a-z]+(?:'s)?\s+(?:book|study|work|analysis)",
    r"\b(?:the\s+)?historian\s+[A-Z]",
    r"\bprofessor\s+[A-Z]",
    r"\bstudy\s+by\b",
    r"\bresearch\s+by\b",
    r"\b(?:as|what)\s+\w+\s+(?:said|wrote|argued|claimed|described)"
]

# Date patterns (specific years and date ranges)
DATE_PATTERNS = [
    r"\b\d{3,4}\s*(?:CE|BCE|AD|BC)\b",  # e.g., "800 CE", "1916 AD"
    r"\b(?:1|2)\d{3}\b",  # Years: 1000-2999
    r"\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}",
    r"\b\d{1,2}(?:st|nd|rd|th)?\s+(?:century|Century)\b"
]

# Quantitative data patterns (statistics, percentages, specific numbers)
QUANTITATIVE_PATTERNS = [
    r"\b\d+(?:\.\d+)?%",  # Percentages
    r"\b\d+(?:,\d{3})*(?:\.\d+)?\s+(?:people|deaths|soldiers|civilians|troops)",
    r"\b(?:increased|decreased|grew|declined)\s+by\s+\d+",
    r"\b\d+(?:\.\d+)?x\s+(?:more|less|growth)",
    r"\broughly\s+\d+",
    r"\bapproximately\s+\d+",
    r"\babout\s+\d+(?:,\d{3})*"
]

# Legal/technical language
LEGAL_KEYWORDS = [
    "estoppel",
    "sovereignty", "sovereign",
    "jurisdiction", "jurisdictional",
    "territorial", "territory",
    "annexation", "annexed",
    "cession", "ceded",
    "maritime", "maritime zone",
    "border", "boundary", "frontier",
    "ratification", "ratified",
    "clause", "article", "provision"
]


# ============================================================================
# ARGUMENT STRUCTURE - Patterns indicating complete arguments
# ============================================================================

# Causal explanation language
CAUSAL_PATTERNS = [
    r"\bconsequently\b",
    r"\bthereby\b",
    r"\bthus\b",
    r"\btherefore\b",
    r"\bwhich\s+meant\s+that\b",
    r"\bas\s+a\s+result\b",
    r"\bthis\s+led\s+to\b",
    r"\bthis\s+caused\b",
    r"\bresulted\s+in\b",
    r"\bbecause\s+of\s+this\b"
]

# Myth-debunking patterns
DEBUNK_PATTERNS = [
    r"\bactually\b",
    r"\bin\s+reality\b",
    r"\bcontrary\s+to\s+(?:popular\s+)?belief\b",
    r"\bthe\s+myth\s+(?:that|of)\b",
    r"\bcommonly\s+believed\b",
    r"\bnot\s+true\s+that\b",
    r"\bevidence\s+shows\b",
    r"\bproves\s+(?:that|this)\b",
    r"\bdemonstrates\s+that\b"
]

# Comparative analysis patterns
COMPARISON_PATTERNS = [
    r"\bwhile\s+(?:in\s+)?[A-Z]\w+[,\s]+(?:in\s+)?[A-Z]\w+\b",  # "while in Europe, in Russia"
    r"\bwhereas\b",
    r"\bin\s+contrast\b",
    r"\bon\s+the\s+other\s+hand\b",
    r"\bdifferent\s+from\b",
    r"\bunlike\b",
    r"\bcompared\s+to\b"
]

# Conclusion/synthesis signals
CONCLUSION_PATTERNS = [
    r"\bthis\s+is\s+why\b",
    r"\bwhat\s+this\s+(?:means|shows|tells\s+us)\b",
    r"\bthe\s+key\s+(?:point|takeaway|lesson)\b",
    r"\bin\s+(?:summary|conclusion)\b",
    r"\bultimately\b",
    r"\bthe\s+bottom\s+line\b",
    r"\bwhat\s+really\s+matters\b"
]


# ============================================================================
# PENALTIES - Patterns indicating non-academic content
# ============================================================================

# Clickbait language
CLICKBAIT_WORDS = [
    "SHOCKING", "SHOCKED", "SHOCK",
    "SECRET", "SECRETS", "HIDDEN",
    "they don't want you to know",
    "you won't believe",
    "INSANE", "CRAZY", "WILD",
    "DESTROYED", "DESTROYS", "ANNIHILATED",
    "EPIC", "LEGENDARY",
    "MIND-BLOWING", "MIND-BLOWN",
    "UNBELIEVABLE", "INCREDIBLE",
    "this changes everything"
]

# Emotional exaggeration (unless clearly quoting)
EXAGGERATION_PATTERNS = [
    r"\bcompletely\s+(?:destroyed|annihilated|obliterated|eradicated)\b",
    r"\btotally\s+(?:changed|transformed|revolutionized)\b",
    r"\bforever\s+(?:changed|altered|ruined)\b",
]

# Vague attribution (red flag for unverified claims)
VAGUE_ATTRIBUTION = [
    r"\bsome\s+(?:say|claim|believe|think)\b",
    r"\bmany\s+(?:people\s+)?(?:say|claim|believe|think)\b",
    r"\bexperts\s+say\b",  # (without naming the expert)
    r"\bhistorians\s+(?:say|believe)\b",  # (without naming which historians)
    r"\bit'?s\s+(?:said|claimed|believed)\s+that\b"
]


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def compile_patterns(pattern_list: List[str]) -> List[Pattern]:
    """Compile regex patterns with case-insensitive flag."""
    return [re.compile(p, re.IGNORECASE) for p in pattern_list]


def contains_any_keyword(text: str, keywords: List[str]) -> bool:
    """Check if text contains any keyword (case-insensitive)."""
    text_lower = text.lower()
    return any(keyword.lower() in text_lower for keyword in keywords)


def count_pattern_matches(text: str, patterns: List[Pattern]) -> int:
    """Count total pattern matches in text."""
    return sum(len(pattern.findall(text)) for pattern in patterns)


def find_pattern_matches(text: str, patterns: List[Pattern]) -> List[str]:
    """Find all pattern matches and return them."""
    matches = []
    for pattern in patterns:
        matches.extend(pattern.findall(text))
    return matches


# Compile all patterns at module load
CITATION_COMPILED = compile_patterns(CITATION_PATTERNS)
DATE_COMPILED = compile_patterns(DATE_PATTERNS)
QUANTITATIVE_COMPILED = compile_patterns(QUANTITATIVE_PATTERNS)
CAUSAL_COMPILED = compile_patterns(CAUSAL_PATTERNS)
DEBUNK_COMPILED = compile_patterns(DEBUNK_PATTERNS)
COMPARISON_COMPILED = compile_patterns(COMPARISON_PATTERNS)
CONCLUSION_COMPILED = compile_patterns(CONCLUSION_PATTERNS)
EXAGGERATION_COMPILED = compile_patterns(EXAGGERATION_PATTERNS)
VAGUE_ATTRIBUTION_COMPILED = compile_patterns(VAGUE_ATTRIBUTION)
