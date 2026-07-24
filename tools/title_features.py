"""Title structure — the one place a title string becomes structural features.

Canonical home for *how a title is phrased*: its structural pattern (versus,
the_x_that, colon, question, how_why, declarative) and the feature predicates
that scoring and analytics read (year, specific number, named entity, evidence
promise, controversy frame, active verb).

This is NOT topic classification ("what the video is about" — territorial /
ideological / colonial). That is a separate concept and lives elsewhere
(growth_data.classify_title, intel.topic_vocabulary). Do not add topic rules here.

Pure `str -> features`: no DB, no scoring, no I/O. `title_scorer.py` holds the
scoring on top and imports these as its canonical logic; the analytics
pattern-classifier copies (ctr_by_source_analysis, traffic_analysis,
build_deliverables) delegate here too, so the taxonomy is defined once.

See ADR-0009.
"""
import re

# Strong active verbs that signal a concrete claim (shared by scoring + analytics).
ACTIVE_VERBS = [
    'destroyed', 'erased', 'redrew', 'deleted', 'stole', 'conquered',
    'invaded', 'betrayed', 'exposed', 'revealed', 'weaponized', 'carved',
    'divided', 'partitioned', 'annexed', 'ruled', 'fought', 'claimed',
    'debunked', 'proved', 'disproved', 'lied', 'fabricated',
]

_YEAR_RE = re.compile(r'\b(1[0-9]{3}|20[0-2][0-9])\b')


def pattern(title: str) -> str:
    """Detect which structural title pattern this matches.

    One of: versus, the_x_that, colon, question, how_why, declarative.
    Checked in priority order — versus and the_x_that before colon so
    "X vs Y: Stakes" reads as versus and "The Treaty That ..." as the_x_that.
    """
    t = title.lower()

    # versus pattern: "X vs Y", "X versus Y"
    if re.search(r'\bvs\.?\b|\bversus\b', t):
        return 'versus'

    # the_x_that pattern: "The [1-3 words] That [Verb]"
    if re.search(r'^the\s+(?:\w+\s+){0,2}\w+\s+that\s+', t):
        return 'the_x_that'

    # colon pattern
    if ':' in title:
        return 'colon'

    # question pattern
    if title.strip().endswith('?'):
        return 'question'

    # how/why pattern
    if re.search(r'^(how|why)\b', t):
        return 'how_why'

    return 'declarative'


def has_year(title: str) -> bool:
    """Check if title contains a 4-digit year."""
    return bool(_YEAR_RE.search(title))


def has_specific_number(title: str) -> bool:
    """Check for specific numbers (not years) that create real specificity.

    Excludes duration-as-adjective patterns like "200-Year-Old" or "500-Year"
    which don't create the same specificity as "5 Myths" or "122 Years of French
    Extraction". Duration adjectives are vague scale markers, not concrete data
    points.
    """
    # Remove years first
    no_years = _YEAR_RE.sub('', title)
    # Remove duration-as-adjective patterns (e.g., "200-Year-Old", "500-Year Lie")
    no_duration_adj = re.sub(r'\b\d+-[Yy]ear-?\w*', '', no_years)
    return bool(re.search(r'\b\d+\b', no_duration_adj))


def has_active_verb(title: str) -> bool:
    """Check for strong active verbs."""
    t = title.lower()
    return any(v in t for v in ACTIVE_VERBS)


def has_evidence_promise(title: str) -> bool:
    """Detect evidence/proof promise language — strongest CTR signal on this channel.

    Top CTR titles: "Here's the Evidence" (9.5%), "Here's Who Did It" (3.7%),
    "The Documents Prove It", "Primary Sources Destroy".
    """
    t = title.lower()
    evidence_phrases = [
        "here's", "the evidence", "the proof", "the documents",
        "documents prove", "documents show", "primary source",
        "the receipt", "every receipt", "we found", "we read",
        "the original", "the actual", "word for word",
    ]
    return any(p in t for p in evidence_phrases)


def has_named_entity(title: str) -> bool:
    """Detect named countries, leaders, or orgs that create specificity.

    Titles with named entities get more impressions (YouTube knows who to show
    them to). Top performers all name specific countries or political figures.
    """
    entity_signals = [
        r"\b(?:France|Spain|Portugal|Turkey|Greece|Iran|Venezuela|Guyana|"
        r"Israel|Palestine|Russia|China|Morocco|Cyprus|Kashmir|Peru|"
        r"Georgia|Haiti|Armenia|Kosovo|NATO|USSR|CIA|KGB|UN|EU|"
        r"Trump|Vance|Stalin|Petain|Lagertha|Sykes|Picot)\b",
    ]
    return any(re.search(p, title) for p in entity_signals)


def has_controversy_frame(title: str) -> bool:
    """Detect accusation/myth-busting framing that signals conflict/tension.

    Top CTR: "Claims Christians Found Child Sacrifice" (9.5%), "Started With a
    Lie" (5.1%), "Destroy the Narrative" (5.4%), "Weaponized Palestine" (5.5%).
    """
    t = title.lower()
    controversy_words = [
        'myth', 'lie', 'fake', 'hoax', 'claims', 'claim',
        'debunk', 'destroy', 'narrative', 'propaganda',
        'secret', 'hidden', 'nobody', 'sacrifice',
        'walked back', 'phantom', 'illegal',
    ]
    return any(w in t for w in controversy_words)
