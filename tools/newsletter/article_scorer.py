"""
Article Scorer -- Grades newsletter articles against measurable quality rules.

Scores articles pass/warn/fail across 19 checks in 5 categories:
structure, style, rhythm, content, and formatting. (Style includes three
soft stop-slop imports — false agency, business jargon, throat-clearing —
that warn on overuse but never fail the grade.)

Usage:
    python -m tools.newsletter.article_scorer path/to/NEWSLETTER-ARTICLE.md
    python -m tools.newsletter.article_scorer path/to/NEWSLETTER-ARTICLE.md --json
"""

import json
import re
import sys
from pathlib import Path
from tools.logging_config import get_logger

logger = get_logger(__name__)


# =============================================================================
# CONSTANTS
# =============================================================================

WORD_COUNT_PASS = (1200, 3000)
WORD_COUNT_WARN_LOW = 1000
WORD_COUNT_WARN_HIGH = 3500

SECTION_COUNT_PASS = (4, 10)
SECTION_COUNT_WARN = (3, 11)

SECTION_LENGTH_MAX = 350
SECTION_LENGTH_WARN = 500  # 350-500 = warn, 500+ = fail

# Trailing metadata sections to strip before scoring the article body.
# These appear at the end of the markdown after the main article content.
_METADATA_HEADINGS = {
    'subject lines', 'slop check', 'structural notes',
}

AI_SLOP_PHRASES = [
    'delve',
    'tapestry',
    'nuanced',
    'multifaceted',
    'shed light on',
    'navigate the complexities',
    'a testament to',
    'pivotal',
    'crucial',
    'underscores the importance',
    'played a crucial role',
    # "landscape" handled separately (context-aware)
]

# Words that make "landscape" legitimate when within 3 words before it
_LANDSCAPE_SAFE_PREFIXES = {
    'political', 'urban', 'rural', 'natural', 'desert', 'mountain',
}

METADISCOURSE_PHRASES = [
    'in this article',
    'as we will see',
    "let's look at",
    'now we turn to',
    'it is worth noting',
    "here's the part",
    'but watch what happens',
    "the question isn't",
    "let's dive into",
    'without further ado',
]

QUALIFIER_PHRASES = [
    'a bit',
    'sort of',
    # "rather" handled separately (exclude "rather than")
    'in a sense',
    'to some extent',
    'it could be argued',
]

ZOMBIE_NOUN_PHRASES = [
    'the implementation of',
    'the establishment of',
    'the utilization of',
    'the facilitation of',
    'the optimization of',
    'the prioritization of',
]

# --- stop-slop imports (github.com/hardikpandya/stop-slop), 2026-06-25 ---
# Writing-side hygiene only, NOT spoken-voice rules (the spoken fingerprint lives
# in VOICE-PROFILE.md + voice_lint.py and is left untouched). Soft by design:
# these warn on OVERUSE and never fail the grade — the user's call, "useful
# sometimes, just not overused."
#
# False agency DELIBERATELY EXCLUDES document/source speech ("the treaty says",
# "the map shows", "the record shows") — putting the verdict on the primary
# document is the channel's core move, not slop. Only corporate/abstract agency
# is flagged.
FALSE_AGENCY_PHRASES = [
    'the data tells us', 'the data tells you', 'the numbers tell us',
    'the market rewards', 'the market punishes', 'the market decides',
    'the culture shifts', 'the conversation moves', 'the conversation shifts',
    'the conversation turns', 'the decision emerges', 'history teaches us',
    'the algorithm decides', 'the algorithm rewards', 'the moment demands',
]

# 'navigate' deliberately omitted (literal for canal/maritime history topics).
BUSINESS_JARGON_PHRASES = [
    'lean into', 'leaned into', 'leaning into', 'double down', 'doubled down',
    'circle back', 'deep dive', 'deep-dive', 'game-changer', 'game changer',
    'move the needle', 'on the same page', 'take a step back', 'stepping back',
    'moving forward', 'unpack',
]

# 'the real question is' omitted (legit analytical turn for this channel).
THROAT_CLEARING_PHRASES = [
    "here's the thing", 'the truth is', 'the uncomfortable truth is',
    'it turns out', 'the real problem is', 'the real issue is',
    'the real story is', 'let me be clear', 'make no mistake',
    'let that sink in', "i'll be honest", 'to be honest', 'let me be honest',
    'this matters because', "here's why that matters", 'at the end of the day',
    'the reality is', 'in a world where',
]


# =============================================================================
# PARSING HELPERS
# =============================================================================

def _strip_frontmatter(text: str) -> str:
    """Remove YAML frontmatter (--- delimited block at start of file)."""
    if text.startswith('---'):
        end = text.find('---', 3)
        if end != -1:
            return text[end + 3:].lstrip('\n')
    return text


def _split_body_and_metadata(text: str) -> tuple:
    """
    Split article into (body, metadata_sections).

    Metadata sections are identified by headings matching _METADATA_HEADINGS.
    Everything from the first metadata heading onward is metadata.
    Returns (body_text, metadata_text).
    """
    lines = text.split('\n')
    split_index = len(lines)

    for i, line in enumerate(lines):
        stripped = line.strip().lstrip('#').strip()
        stripped_lower = stripped.lower()
        # Check if any metadata keyword appears within the heading
        if any(h in stripped_lower for h in _METADATA_HEADINGS):
            split_index = i
            break

    body = '\n'.join(lines[:split_index])
    metadata = '\n'.join(lines[split_index:])
    return body, metadata


def _get_sections(body: str) -> list:
    """
    Parse markdown sections from body text.

    Returns list of dicts: {'heading': str, 'text': str, 'word_count': int}.
    Text before the first heading is included as a section with heading='(intro)'.
    """
    sections = []
    current_heading = '(intro)'
    current_lines = []

    for line in body.split('\n'):
        # Only treat ## headings as section breaks (not # title or ### sub-headings)
        if re.match(r'^##\s+', line) and not re.match(r'^###', line):
            # Save previous section
            text = '\n'.join(current_lines).strip()
            if text:
                words = len(text.split())
                sections.append({
                    'heading': current_heading,
                    'text': text,
                    'word_count': words,
                })
            current_heading = line.strip().lstrip('#').strip()
            current_lines = []
        else:
            current_lines.append(line)

    # Save final section
    text = '\n'.join(current_lines).strip()
    if text:
        words = len(text.split())
        sections.append({
            'heading': current_heading,
            'text': text,
            'word_count': words,
        })

    return sections


def _split_sentences(text: str) -> list:
    """
    Split text into sentences using simple regex.

    Splits on sentence-ending punctuation followed by whitespace and an
    uppercase letter, or end of string.
    """
    # Remove markdown headers, blockquotes, and list markers for clean splitting
    cleaned = re.sub(r'^#{1,6}\s+.*$', '', text, flags=re.MULTILINE)
    cleaned = re.sub(r'^>\s+', '', cleaned, flags=re.MULTILINE)

    # Split on ". ", "! ", "? " followed by uppercase or end of string
    raw = re.split(r'(?<=[.!?])\s+(?=[A-Z])', cleaned)

    # Filter out empty strings and very short fragments
    sentences = [s.strip() for s in raw if s.strip() and len(s.strip()) > 2]
    return sentences


def _count_words(text: str) -> int:
    """Count words in text, ignoring markdown formatting."""
    # Strip markdown headers, blockquote markers, emphasis
    cleaned = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)
    cleaned = re.sub(r'^>\s+', '', cleaned, flags=re.MULTILINE)
    cleaned = re.sub(r'[*_`\[\]()]', '', cleaned)
    return len(cleaned.split())


# =============================================================================
# INDIVIDUAL CHECKS
# =============================================================================

def _check_word_count(body: str) -> dict:
    """Check 1: Word count within target range."""
    count = _count_words(body)
    if WORD_COUNT_PASS[0] <= count <= WORD_COUNT_PASS[1]:
        status = 'pass'
    elif WORD_COUNT_WARN_LOW <= count < WORD_COUNT_PASS[0]:
        status = 'warn'
    elif WORD_COUNT_PASS[1] < count <= WORD_COUNT_WARN_HIGH:
        status = 'warn'
    else:
        status = 'fail'

    return {
        'name': 'Word count',
        'status': status,
        'detail': f'{count:,} (target: {WORD_COUNT_PASS[0]:,}-{WORD_COUNT_PASS[1]:,})',
        'value': count,
    }


def _check_section_count(sections: list) -> dict:
    """Check 2: Section count within target range."""
    # Exclude intro if it exists as a section
    count = len(sections)
    if SECTION_COUNT_PASS[0] <= count <= SECTION_COUNT_PASS[1]:
        status = 'pass'
    elif count == SECTION_COUNT_WARN[0] or SECTION_COUNT_PASS[1] < count <= SECTION_COUNT_WARN[1]:
        status = 'warn'
    else:
        status = 'fail'

    return {
        'name': 'Sections',
        'status': status,
        'detail': f'{count} (target: {SECTION_COUNT_PASS[0]}-{SECTION_COUNT_PASS[1]})',
        'value': count,
    }


def _check_section_length(sections: list) -> dict:
    """Check 3: Section length — pass ≤350w, warn 350-500w, fail 500w+."""
    over_warn = [s for s in sections if SECTION_LENGTH_MAX < s['word_count'] <= SECTION_LENGTH_WARN]
    over_fail = [s for s in sections if s['word_count'] > SECTION_LENGTH_WARN]

    if not over_warn and not over_fail:
        status = 'pass'
        detail = f'all under {SECTION_LENGTH_MAX} words'
    elif over_fail:
        status = 'fail'
        names = ', '.join(
            f'"{s["heading"]}": {s["word_count"]}w' for s in over_fail
        )
        detail = f'{len(over_fail)} section(s) over {SECTION_LENGTH_WARN} words ({names})'
    else:
        status = 'warn'
        names = ', '.join(
            f'"{s["heading"]}": {s["word_count"]}w' for s in over_warn
        )
        detail = f'{len(over_warn)} section(s) {SECTION_LENGTH_MAX}-{SECTION_LENGTH_WARN} words ({names})'

    return {
        'name': 'Section length',
        'status': status,
        'detail': detail,
        'value': len(over_warn) + len(over_fail),
    }


def _check_verdict_first(body: str) -> dict:
    """Check 4: 'Why it matters:' appears early in the article."""
    lower = body.lower()
    pos = lower.find('why it matters:')
    if pos == -1:
        return {
            'name': 'Verdict-first',
            'status': 'fail',
            'detail': '"Why it matters:" not found',
            'value': -1,
        }

    # Count words before the match
    words_before = len(body[:pos].split())
    if words_before <= 200:
        status = 'pass'
    elif words_before <= 400:
        status = 'warn'
    else:
        status = 'fail'

    return {
        'name': 'Verdict-first',
        'status': status,
        'detail': f'"Why it matters:" at word {words_before}',
        'value': words_before,
    }


def _check_axiom_anchors(body: str) -> dict:
    """Check 5: Has 'By the numbers:' or 'The big picture:'."""
    lower = body.lower()
    has_numbers = 'by the numbers:' in lower
    has_picture = 'the big picture:' in lower

    if has_numbers or has_picture:
        found = []
        if has_numbers:
            found.append('"By the numbers:"')
        if has_picture:
            found.append('"The big picture:"')
        return {
            'name': 'Axiom anchors',
            'status': 'pass',
            'detail': f'{", ".join(found)} found',
            'value': len(found),
        }

    return {
        'name': 'Axiom anchors',
        'status': 'warn',
        'detail': 'neither "By the numbers:" nor "The big picture:" found',
        'value': 0,
    }


def _check_em_dashes(body: str) -> dict:
    """Check 6: Em dash count in prose (excluding blockquote attributions)."""
    count = 0
    for line in body.split('\n'):
        stripped = line.strip()
        # Skip blockquote attribution lines ("> -- Author")
        if stripped.startswith('>') and ('\u2014' in stripped or ' -- ' in stripped):
            continue
        # Skip [PERSONAL] marker lines (user will rewrite these)
        if '[PERSONAL' in stripped:
            continue
        # Count em dashes (Unicode and ASCII-style " -- ")
        count += stripped.count('\u2014')
        count += len(re.findall(r' -- ', stripped))

    if count == 0:
        status = 'pass'
    elif count <= 2:
        status = 'warn'
    else:
        status = 'fail'

    return {
        'name': 'Em dashes',
        'status': status,
        'detail': f'{count} in prose',
        'value': count,
    }


def _check_ai_slop(body: str) -> dict:
    """Check 7: AI slop phrases."""
    lower = body.lower()
    found = []

    for phrase in AI_SLOP_PHRASES:
        if phrase in lower:
            found.append(phrase)

    # Context-aware "landscape" check
    for match in re.finditer(r'\blandscape\b', lower):
        start = max(0, match.start() - 50)
        preceding = lower[start:match.start()]
        preceding_words = preceding.split()
        # Check if any safe prefix is within last 3 words
        last_words = preceding_words[-3:] if len(preceding_words) >= 3 else preceding_words
        if not any(w in _LANDSCAPE_SAFE_PREFIXES for w in last_words):
            found.append('landscape')

    count = len(found)
    if count == 0:
        status = 'pass'
    elif count == 1:
        status = 'warn'
    else:
        status = 'fail'

    detail_str = f'{count} phrases found'
    if found:
        detail_str += f' ({", ".join(found)})'

    return {
        'name': 'AI slop',
        'status': status,
        'detail': detail_str,
        'value': count,
    }


def _check_metadiscourse(body: str) -> dict:
    """Check 8: Metadiscourse phrases."""
    lower = body.lower()
    found = [p for p in METADISCOURSE_PHRASES if p in lower]
    count = len(found)

    if count == 0:
        status = 'pass'
    else:
        status = 'fail'

    detail_str = f'{count} phrases found'
    if found:
        detail_str += f' ({", ".join(found)})'

    return {
        'name': 'Metadiscourse',
        'status': status,
        'detail': detail_str,
        'value': count,
    }


def _check_qualifiers(body: str) -> dict:
    """Check 9: Qualifier phrases."""
    lower = body.lower()
    found = []

    for phrase in QUALIFIER_PHRASES:
        if phrase in lower:
            found.append(phrase)

    # "rather" check: count standalone "rather" but not "rather than"
    rather_standalone = len(re.findall(r'\brather\b(?!\s+than)', lower))
    if rather_standalone > 0:
        found.extend(['rather'] * rather_standalone)

    count = len(found)
    if count == 0:
        status = 'pass'
    elif count <= 2:
        status = 'warn'
    else:
        status = 'fail'

    detail_str = f'{count} found'
    if found:
        detail_str += f' ({", ".join(found)})'

    return {
        'name': 'Qualifiers',
        'status': status,
        'detail': detail_str,
        'value': count,
    }


def _check_zombie_nouns(body: str) -> dict:
    """Check 10: Zombie noun phrases."""
    lower = body.lower()
    found = [p for p in ZOMBIE_NOUN_PHRASES if p in lower]
    count = len(found)

    if count == 0:
        status = 'pass'
    else:
        status = 'warn'

    detail_str = f'{count} found'
    if found:
        detail_str += f' ({", ".join(found)})'

    return {
        'name': 'Zombie nouns',
        'status': status,
        'detail': detail_str,
        'value': count,
    }


def _count_phrase_hits(lower: str, phrases: list) -> list:
    """Return a flat list of every phrase occurrence, word-boundary matched.

    Word boundaries avoid substring false positives (e.g. 'unpack' won't fire
    inside 'unpackaged'); conservative by design (misses some inflections).
    """
    found = []
    for p in phrases:
        pat = r'\b' + re.escape(p) + r'\b'
        found.extend([p] * len(re.findall(pat, lower)))
    return found


def _soft_phrase_check(name: str, body: str, phrases: list) -> dict:
    """stop-slop soft check: pass at <=1 occurrence, warn on overuse, never fail."""
    found = _count_phrase_hits(body.lower(), phrases)
    count = len(found)
    status = 'pass' if count <= 1 else 'warn'
    detail = f'{count} found'
    if found:
        detail += f' ({", ".join(sorted(set(found)))})'
    return {'name': name, 'status': status, 'detail': detail, 'value': count}


def _check_false_agency(body: str) -> dict:
    """stop-slop: inanimate/abstract subjects performing human actions (soft)."""
    return _soft_phrase_check('False agency', body, FALSE_AGENCY_PHRASES)


def _check_business_jargon(body: str) -> dict:
    """stop-slop: business/blog jargon (lean into, deep dive, circle back) (soft)."""
    return _soft_phrase_check('Business jargon', body, BUSINESS_JARGON_PHRASES)


def _check_throat_clearing(body: str) -> dict:
    """stop-slop: throat-clearing / emphasis-crutch openers (soft)."""
    return _soft_phrase_check('Throat-clearing', body, THROAT_CLEARING_PHRASES)


def _check_verdict_sentences(body: str) -> dict:
    """Check 11: Count sentences with 5 or fewer words (not headers or fragments)."""
    sentences = _split_sentences(body)
    short = []
    for s in sentences:
        words = s.split()
        if len(words) > 5:
            continue
        # Skip fragments that are just list items or bold labels
        stripped = s.strip().rstrip('.')
        if stripped.startswith('**') or stripped.startswith('- '):
            continue
        # Skip single-word fragments
        if len(words) < 2:
            continue
        short.append(s)
    count = len(short)

    if count >= 4:
        status = 'pass'
    elif count >= 2:
        status = 'warn'
    else:
        status = 'fail'

    return {
        'name': 'Verdict sentences',
        'status': status,
        'detail': f'{count} (<=5 words each)',
        'value': count,
    }


def _check_rhythm_flatlines(body: str) -> dict:
    """Check 12: Detect 5+ consecutive sentences of similar length."""
    sentences = _split_sentences(body)
    if len(sentences) < 5:
        return {
            'name': 'Rhythm variety',
            'status': 'pass',
            'detail': 'too few sentences to flatline',
            'value': 0,
        }

    lengths = [len(s.split()) for s in sentences]
    flatline_count = 0

    i = 0
    while i <= len(lengths) - 5:
        window = lengths[i:i + 5]
        avg = sum(window) / len(window)
        if avg == 0:
            i += 1
            continue
        # Check if all within 20% of each other (use max/min ratio)
        min_len = min(window)
        max_len = max(window)
        if min_len > 0 and (max_len - min_len) / avg <= 0.20:
            flatline_count += 1
            i += 5  # Skip past this flatline
        else:
            i += 1

    if flatline_count == 0:
        status = 'pass'
        detail = 'no flatlines detected'
    elif flatline_count == 1:
        status = 'warn'
        detail = '1 flatline detected (5+ same-length sentences)'
    else:
        status = 'fail'
        detail = f'{flatline_count} flatlines detected'

    return {
        'name': 'Rhythm variety',
        'status': status,
        'detail': detail,
        'value': flatline_count,
    }


def _check_personal_markers(body: str) -> dict:
    """Check 13: [PERSONAL] marker count."""
    # Match both [PERSONAL] and [PERSONAL: ...]
    count = len(re.findall(r'\[PERSONAL[:\]]', body))

    if 2 <= count <= 3:
        status = 'pass'
    elif count == 1 or count == 4:
        status = 'warn'
    else:
        status = 'fail'

    return {
        'name': '[PERSONAL] markers',
        'status': status,
        'detail': str(count),
        'value': count,
    }


def _check_blockquotes(body: str) -> dict:
    """Check 14: Blockquoted source count."""
    # Count distinct blockquote blocks (consecutive > lines = 1 block)
    in_blockquote = False
    count = 0
    for line in body.split('\n'):
        if line.strip().startswith('>'):
            if not in_blockquote:
                count += 1
                in_blockquote = True
        else:
            in_blockquote = False

    if count >= 2:
        status = 'pass'
    elif count == 1:
        status = 'warn'
    else:
        status = 'fail'

    return {
        'name': 'Blockquoted sources',
        'status': status,
        'detail': str(count),
        'value': count,
    }


def _check_sources_section(full_text: str) -> dict:
    """Check 15: Has a Sources section."""
    # Check for Sources section: heading (## Sources), italic (*Sources:*), or bold (**Sources:**)
    patterns = [
        r'^#{1,6}\s+Sources',          # ## Sources
        r'^\*+Sources:?\*+',            # *Sources:* or **Sources:**
        r'^Sources:',                    # Plain Sources:
    ]
    for pattern in patterns:
        if re.search(pattern, full_text, re.MULTILINE | re.IGNORECASE):
            return {
                'name': 'Source citations',
                'status': 'pass',
                'detail': 'present',
                'value': 1,
            }

    return {
        'name': 'Source citations',
        'status': 'fail',
        'detail': 'no "Sources:" section found',
        'value': 0,
    }


def _check_subject_lines(metadata: str, full_text: str) -> dict:
    """Check 16: Subject line section with 3+ options."""
    # Look for subject line section in metadata or full text
    combined = metadata if metadata.strip() else full_text
    lower = combined.lower()

    # Find the subject lines section
    match = re.search(r'#{1,6}\s+(?:\d+\s+)?subject\s+lines?', lower)
    if not match:
        return {
            'name': 'Subject lines',
            'status': 'fail',
            'detail': '0 options (no section found)',
            'value': 0,
        }

    # Count lines that look like subject line options (numbered or bulleted)
    section_start = match.end()
    remaining = combined[section_start:]

    # Find the next heading or end of text
    next_heading = re.search(r'^#{1,6}\s+', remaining, re.MULTILINE)
    if next_heading:
        section_text = remaining[:next_heading.start()]
    else:
        section_text = remaining

    # Count option lines (numbered: "1.", "2." or bulleted: "- ", "* " or table rows: "| 1 |")
    options = re.findall(
        r'^\s*(?:\d+[.)]\s+|- |\* |\|\s*\d+\s*\|)',
        section_text,
        re.MULTILINE,
    )
    count = len(options)

    if count >= 3:
        status = 'pass'
    elif count >= 1:
        status = 'warn'
    else:
        status = 'fail'

    return {
        'name': 'Subject lines',
        'status': status,
        'detail': f'{count} options',
        'value': count,
    }


# =============================================================================
# SCORING ENGINE
# =============================================================================

def score_article(filepath: str) -> dict:
    """
    Score a newsletter article against all quality checks.

    Args:
        filepath: Path to markdown article file.

    Returns:
        Dict with 'filename', 'checks' (list of check results),
        'passed', 'warnings', 'failures', and 'grade'.
    """
    path = Path(filepath)
    if not path.exists():
        logger.error("File not found: %s", filepath)
        return {'error': f'File not found: {filepath}'}

    raw = path.read_text(encoding='utf-8')
    text = _strip_frontmatter(raw)
    body, metadata = _split_body_and_metadata(text)
    sections = _get_sections(body)

    checks = []

    # Structure checks
    checks.append(_check_word_count(body))
    checks.append(_check_section_count(sections))
    checks.append(_check_section_length(sections))
    checks.append(_check_verdict_first(body))
    checks.append(_check_axiom_anchors(body))

    # Style checks
    checks.append(_check_em_dashes(body))
    checks.append(_check_ai_slop(body))
    checks.append(_check_metadiscourse(body))
    checks.append(_check_qualifiers(body))
    checks.append(_check_zombie_nouns(body))
    # stop-slop soft imports (warn-on-overuse, never fail)
    checks.append(_check_false_agency(body))
    checks.append(_check_business_jargon(body))
    checks.append(_check_throat_clearing(body))

    # Rhythm checks
    checks.append(_check_verdict_sentences(body))
    checks.append(_check_rhythm_flatlines(body))

    # Content checks
    checks.append(_check_personal_markers(body))
    checks.append(_check_blockquotes(body))
    checks.append(_check_sources_section(text))

    # Formatting checks
    checks.append(_check_subject_lines(metadata, text))

    # Tally results
    passed = sum(1 for c in checks if c['status'] == 'pass')
    warnings = sum(1 for c in checks if c['status'] == 'warn')
    failures = sum(1 for c in checks if c['status'] == 'fail')

    # Grading
    if failures == 0 and warnings <= 2:
        grade = 'A'
    elif failures == 0:
        grade = 'B'
    elif failures == 1:
        grade = 'C'
    elif failures == 2:
        grade = 'D'
    else:
        grade = 'F'

    return {
        'filename': path.name,
        'filepath': str(path),
        'checks': checks,
        'passed': passed,
        'warnings': warnings,
        'failures': failures,
        'total': len(checks),
        'grade': grade,
    }


# =============================================================================
# OUTPUT FORMATTING
# =============================================================================

_STATUS_ICONS = {
    'pass': '\u2705',  # green checkmark
    'warn': '\u26a0\ufe0f ',  # warning sign (with extra space for alignment)
    'fail': '\u274c',  # red X
}

# Category groupings for display
_CATEGORIES = [
    ('STRUCTURE', ['Word count', 'Sections', 'Section length',
                   'Verdict-first', 'Axiom anchors']),
    ('STYLE', ['Em dashes', 'AI slop', 'Metadiscourse',
               'Qualifiers', 'Zombie nouns',
               'False agency', 'Business jargon', 'Throat-clearing']),
    ('RHYTHM', ['Verdict sentences', 'Rhythm variety']),
    ('CONTENT', ['[PERSONAL] markers', 'Blockquoted sources',
                 'Source citations']),
    ('FORMATTING', ['Subject lines']),
]


def format_result(result: dict) -> str:
    """Format scoring result as a human-readable report."""
    if 'error' in result:
        return f"ERROR: {result['error']}"

    lines = []
    sep = '\u2550' * 35

    lines.append(f'ARTICLE QUALITY GATE: {result["filename"]}')
    lines.append(sep)
    lines.append('')

    # Build a lookup from check name to check result
    check_map = {c['name']: c for c in result['checks']}

    for category, check_names in _CATEGORIES:
        lines.append(category)
        for name in check_names:
            check = check_map.get(name)
            if check is None:
                continue
            icon = _STATUS_ICONS.get(check['status'], '?')
            lines.append(f'  {icon} {check["name"]}: {check["detail"]}')
        lines.append('')

    lines.append(sep)
    lines.append(
        f'SCORE: {result["passed"]}/{result["total"]} passed | '
        f'{result["warnings"]} warning(s) | {result["failures"]} failure(s)'
    )
    lines.append(f'GRADE: {result["grade"]}')
    lines.append(sep)

    return '\n'.join(lines)


# =============================================================================
# CLI
# =============================================================================

def _run_batch() -> int:
    """Score all NEWSLETTER-ARTICLE.md files and print summary table."""
    import glob as globmod

    pattern = 'video-projects/**/NEWSLETTER-ARTICLE.md'
    files = sorted(globmod.glob(pattern, recursive=True))

    if not files:
        print('No NEWSLETTER-ARTICLE.md files found.')
        return 1

    results = []
    for f in files:
        r = score_article(f)
        if 'error' not in r:
            results.append(r)

    if not results:
        print('All files errored.')
        return 1

    # Print individual reports
    for r in results:
        print()
        print(format_result(r))

    # Print summary table
    sep = '\u2550' * 60
    print()
    print(sep)
    print('BATCH SUMMARY')
    print(sep)
    print(f'{"File":<45} {"Grade":>5} {"P":>3} {"W":>3} {"F":>3}')
    print('-' * 60)
    for r in results:
        # Shorten path: just project folder + filename
        short = '/'.join(Path(r['filepath']).parts[-3:])
        if len(short) > 44:
            short = '...' + short[-41:]
        print(f'{short:<45} {r["grade"]:>5} {r["passed"]:>3} {r["warnings"]:>3} {r["failures"]:>3}')
    print('-' * 60)

    grades = [r['grade'] for r in results]
    print(f'Total: {len(results)} articles | '
          f'A: {grades.count("A")} B: {grades.count("B")} '
          f'C: {grades.count("C")} D: {grades.count("D")} F: {grades.count("F")}')
    print(sep)

    # Exit 0 if all A/B, else 1
    return 0 if all(g in ('A', 'B') for g in grades) else 1


def main():
    """CLI entry point."""
    import argparse
    from tools.logging_config import setup_logging

    parser = argparse.ArgumentParser(
        description='Article Scorer -- History vs Hype Newsletter',
        epilog=(
            'Examples:\n'
            '  python -m tools.newsletter.article_scorer path/to/NEWSLETTER-ARTICLE.md\n'
            '  python -m tools.newsletter.article_scorer article.md --json\n'
            '  python -m tools.newsletter.article_scorer --all\n'
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument('file', nargs='?', help='Path to markdown article file')
    parser.add_argument(
        '--all',
        action='store_true',
        dest='score_all',
        help='Score all NEWSLETTER-ARTICLE.md files and print summary table',
    )
    parser.add_argument(
        '--json',
        action='store_true',
        dest='json_output',
        help='Output machine-readable JSON instead of formatted report',
    )
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose logging')
    parser.add_argument('-q', '--quiet', action='store_true', help='Suppress non-error logs')

    args = parser.parse_args()
    setup_logging(args.verbose, args.quiet)

    if args.score_all:
        sys.exit(_run_batch())

    if not args.file:
        parser.error('file is required unless --all is used')

    result = score_article(args.file)

    if 'error' in result:
        logger.error(f"{result['error']}")
        sys.exit(1)

    if args.json_output:
        print(json.dumps(result, indent=2))
    else:
        print()
        print(format_result(result))
        print()

    # Exit code: 0 for A/B, 1 for C/D/F
    if result['grade'] in ('A', 'B'):
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == '__main__':
    main()
