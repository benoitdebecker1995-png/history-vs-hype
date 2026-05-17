"""
Title Scorer -- Standalone reference implementation of the History YouTube
Packaging System methodology.

No external dependencies beyond Python stdlib. Implements every rule from
PACKAGING-SYSTEM.md (Sections 2-4) so buyers can run the system end-to-end
on day one.

Usage:
    python title_scorer_standalone.py "Your Title Here"
    python title_scorer_standalone.py "Title A" "Title B" "Title C"
    python title_scorer_standalone.py --file titles.txt

Calibration:
    The PATTERN_SCORES below are calibrated to a 47-video history channel.
    After 30 days of your own CTR data, replace them per Section 8 of the guide:
        your_score = (your_pattern_avg_ctr / your_overall_avg_ctr) * 50

Version 1.0 — 2026-05-08
"""

import re
import sys
import argparse
from pathlib import Path

# Force UTF-8 stdout on Windows (em-dashes, smart quotes render correctly)
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except (AttributeError, Exception):
        pass


# =============================================================================
# PATTERN SCORES — Calibrate to your own channel after 30 days of data
# (See PACKAGING-SYSTEM.md Section 8)
# =============================================================================

PATTERN_SCORES = {
    'versus':      75,   # ~3.7% CTR (n=4 reference)
    'declarative': 65,   # 3.8% CTR (n=19 — most reliable)
    'how_why':     55,   # 3.3% CTR (n=5)
    'question':    45,   # 2.4% CTR (n=1, low confidence)
    'colon':       30,   # 2.3% CTR (penalty confirmed)
    'the_x_that':  10,   # ~1.2% CTR (worst pattern)
}

# =============================================================================
# Hard rejects and modifiers (PACKAGING-SYSTEM.md Section 3)
# =============================================================================

YEAR_PENALTY = -50           # Year as topic label = HARD REJECT
YEAR_PENALTY_HOOK = -10      # Year as hook ("Invented in 1828")
COLON_PENALTY = -50          # "Topic: Subtitle" = HARD REJECT
COLON_PENALTY_VERSUS = -10   # Colon after versus ("X vs Y: Stakes")
THE_X_THAT_PENALTY = -50     # HARD REJECT — worst pattern

LENGTH_SWEET_SPOT = (35, 70)
LENGTH_PENALTY_SHORT = -5
LENGTH_PENALTY_LONG = -10

# Bonus signals (PACKAGING-SYSTEM.md Section 4)
SPECIFIC_NUMBER_BONUS = 10
ACTIVE_VERB_BONUS = 5
SCALE_WORD_BONUS = 5
TWO_SENTENCE_BONUS = 5
EVIDENCE_PROMISE_BONUS = 10  # Top channel signal
ENTITY_BONUS = 5
CONTROVERSY_BONUS = 5

# Word lists (calibrate to your topic and voice)
SCALE_WORDS = {
    'every', 'all', 'entire', 'whole', 'century', 'centuries',
    'forever', 'million', 'billion', 'thousand', 'empire', 'world',
    'continent', 'civilization', 'generation', 'generations',
}

ACTIVE_VERBS = [
    'destroyed', 'erased', 'redrew', 'deleted', 'stole', 'conquered',
    'invaded', 'betrayed', 'exposed', 'revealed', 'weaponized', 'carved',
    'divided', 'partitioned', 'annexed', 'ruled', 'fought', 'claimed',
    'debunked', 'proved', 'disproved', 'lied', 'fabricated',
]

EVIDENCE_PHRASES = [
    "here's", "the evidence", "the proof", "the documents",
    "documents prove", "documents show", "primary source",
    "the receipt", "every receipt", "we found", "we read",
    "the original", "the actual", "word for word",
]

CONTROVERSY_WORDS = [
    'myth', 'lie', 'fake', 'hoax', 'claims', 'claim',
    'debunk', 'destroy', 'narrative', 'propaganda',
    'secret', 'hidden', 'nobody', 'sacrifice',
    'walked back', 'phantom', 'illegal',
]

CLICKBAIT_PATTERNS = [
    'SHOCKING', "You won't believe", "You won't BELIEVE",
    'This will BLOW your mind', "What THEY don't want you to know",
    'INSANE', 'MIND-BLOWING', 'EXPOSED', 'The TRUTH About',
    'DESTROYED by Facts', 'Top 10', '5 Reasons Why',
    "3 Things You Didn't Know", 'LIED About',
]


# =============================================================================
# Pattern detection (Section 2 — order matters; first match wins)
# =============================================================================

def detect_pattern(title: str) -> str:
    t = title.lower()
    if re.search(r'\bvs\.?\b|\bversus\b', t):
        return 'versus'
    if re.search(r'^the\s+(?:\w+\s+){0,2}\w+\s+that\s+', t):
        return 'the_x_that'
    if ':' in title:
        return 'colon'
    if title.strip().endswith('?'):
        return 'question'
    if re.search(r'^(how|why)\b', t):
        return 'how_why'
    return 'declarative'


# =============================================================================
# Detection helpers
# =============================================================================

def has_year(title: str) -> bool:
    return bool(re.search(r'\b(1[0-9]{3}|20[0-2][0-9])\b', title))


def year_is_hook(title: str) -> bool:
    """Year used as hook (mild penalty) vs topic label (hard reject)."""
    t = title.lower()
    hook_patterns = [
        r'(?:invented|created|started|began|built|written|signed|passed|founded)\s+in\s+\d{4}',
        r'(?:since|from|after|before|until)\s+\d{4}',
        r'\d+-year-old',
        r'for\s+\d+\s+years?',
        r'\d+\s+years?\s+(?:of|ago|later|old)',
    ]
    return any(re.search(p, t) for p in hook_patterns)


def colon_is_versus_stakes(title: str) -> bool:
    """Colon after versus framing = stakes, mild penalty only."""
    colon_pos = title.find(':')
    if colon_pos < 0:
        return False
    before = title[:colon_pos].lower()
    return bool(re.search(r'\bvs\.?\b|\bversus\b', before))


def has_specific_number(title: str) -> bool:
    """Specific numbers but NOT years or duration adjectives."""
    no_years = re.sub(r'\b(1[0-9]{3}|20[0-2][0-9])\b', '', title)
    no_duration_adj = re.sub(r'\b\d+-[Yy]ear-?\w*', '', no_years)
    return bool(re.search(r'\b\d+\b', no_duration_adj))


def has_active_verb(title: str) -> bool:
    t = title.lower()
    return any(v in t for v in ACTIVE_VERBS)


def has_evidence_promise(title: str) -> bool:
    """Top CTR signal — explicit evidence/proof/documents promise."""
    t = title.lower()
    return any(p in t for p in EVIDENCE_PHRASES)


def has_named_entity(title: str) -> bool:
    """Country, leader, or org. Calibrate this list to your channel's beat."""
    entity_pattern = (
        r"\b(?:France|Spain|Portugal|Turkey|Greece|Iran|Venezuela|Guyana|"
        r"Israel|Palestine|Russia|China|Morocco|Cyprus|Kashmir|Peru|Belize|"
        r"Guatemala|Georgia|Haiti|Armenia|Kosovo|Britain|Germany|Italy|"
        r"Mexico|Brazil|Argentina|Colombia|Egypt|Syria|Iraq|Afghanistan|"
        r"NATO|USSR|CIA|KGB|UN|EU|NASA|Vatican|Mossad)\b"
    )
    return bool(re.search(entity_pattern, title))


def has_controversy_frame(title: str) -> bool:
    t = title.lower()
    return any(w in t for w in CONTROVERSY_WORDS)


def has_two_sentences(title: str) -> bool:
    """Period in middle, with 3+ lowercase chars before to exclude abbreviations."""
    return bool(re.search(r'(?<=[a-z]{3})\.\s+[A-Z]', title))


def has_scale_word(title: str) -> bool:
    return bool(set(title.lower().split()) & SCALE_WORDS)


def has_clickbait(title: str) -> bool:
    return any(p.lower() in title.lower() for p in CLICKBAIT_PATTERNS)


# =============================================================================
# Main scoring function
# =============================================================================

def score_title(title: str) -> dict:
    """
    Score a title 0-100. Returns dict with full breakdown.
    Static mode — no DB or external data dependencies.
    """
    title = title.strip()
    pattern = detect_pattern(title)
    base = PATTERN_SCORES.get(pattern, 50)

    penalties = []
    bonuses = []
    hard_rejects = []

    # Hard reject 1: YEAR
    if has_year(title):
        if year_is_hook(title):
            penalties.append(('Year (hook usage)', YEAR_PENALTY_HOOK))
        else:
            hard_rejects.append('YEAR as topic label — costs 46% CTR. Move to description.')
            penalties.append(('HARD REJECT: Year', YEAR_PENALTY))

    # Hard reject 2: COLON
    if ':' in title:
        if colon_is_versus_stakes(title):
            penalties.append(('Colon after versus (stakes)', COLON_PENALTY_VERSUS))
        else:
            hard_rejects.append('COLON detected — costs 28% CTR. Use em-dash or period.')
            penalties.append(('HARD REJECT: Colon', COLON_PENALTY if pattern == 'colon' else COLON_PENALTY // 2))

    # Hard reject 3: THE X THAT Y
    if pattern == 'the_x_that':
        hard_rejects.append('"THE X THAT Y" — worst pattern (~1.2% CTR). Rewrite completely.')
        penalties.append(('HARD REJECT: The X That Y', THE_X_THAT_PENALTY))

    # Clickbait penalty
    if has_clickbait(title):
        penalties.append(('Clickbait phrase detected', -10))

    # Length
    length = len(title)
    if length < LENGTH_SWEET_SPOT[0]:
        penalties.append((f'Too short ({length} chars, need 35+)', LENGTH_PENALTY_SHORT))
    elif length > LENGTH_SWEET_SPOT[1]:
        penalties.append((f'Too long ({length} chars, max 70)', LENGTH_PENALTY_LONG))

    # Bonuses
    if has_specific_number(title):
        bonuses.append(('Specific number', SPECIFIC_NUMBER_BONUS))
    if has_active_verb(title):
        bonuses.append(('Active verb', ACTIVE_VERB_BONUS))
    if has_scale_word(title):
        bonuses.append(('Scale word (1.33x outlier lift)', SCALE_WORD_BONUS))
    if has_two_sentences(title):
        bonuses.append(('Two-sentence formula (11% outlier rate)', TWO_SENTENCE_BONUS))
    if has_evidence_promise(title):
        bonuses.append(('Evidence promise (top CTR signal)', EVIDENCE_PROMISE_BONUS))
    if has_named_entity(title):
        bonuses.append(('Named entity', ENTITY_BONUS))
    if has_controversy_frame(title):
        bonuses.append(('Controversy/myth-busting frame', CONTROVERSY_BONUS))

    # Final score
    total_penalties = sum(p[1] for p in penalties)
    total_bonuses = sum(b[1] for b in bonuses)
    final = max(0, min(100, base + total_penalties + total_bonuses))

    # Grade
    if hard_rejects:
        grade = 'REJECTED'
    elif final >= 85:
        grade = 'A'
    elif final >= 70:
        grade = 'B'
    elif final >= 60:
        grade = 'C'
    elif final >= 45:
        grade = 'D'
    else:
        grade = 'F'

    # Suggestions
    suggestions = []
    if has_year(title) and not year_is_hook(title):
        suggestions.append('Remove year — 46% CTR penalty')
    if ':' in title and not colon_is_versus_stakes(title):
        suggestions.append('Replace colon with em-dash or period — 28% CTR penalty')
    if pattern == 'the_x_that':
        suggestions.append('Rewrite — "The X That Y" is the worst pattern (~1.2% CTR)')
    if length > 70:
        suggestions.append(f'Shorten to under 70 chars (currently {length}) — mobile truncation')
    if not has_specific_number(title) and not has_active_verb(title):
        suggestions.append('Add a specific number or active verb for more punch')
    if pattern == 'declarative' and not has_evidence_promise(title):
        suggestions.append('Consider adding evidence promise ("Here\'s the evidence/proof/documents")')

    return {
        'title': title,
        'score': final,
        'grade': grade,
        'pattern': pattern,
        'length': length,
        'base_score': base,
        'penalties': penalties,
        'bonuses': bonuses,
        'hard_rejects': hard_rejects,
        'suggestions': suggestions,
    }


def format_result(result: dict) -> str:
    lines = []

    if result['hard_rejects']:
        lines.append("  " + "!" * 50)
        lines.append("  *** REJECTED — DO NOT PUBLISH ***")
        lines.append("  " + "!" * 50)
        for reason in result['hard_rejects']:
            lines.append(f"  REASON: {reason}")
        lines.append("")

    lines.extend([
        f"  Title:   {result['title']}",
        f"  Score:   {result['score']}/100 ({result['grade']})",
        f"  Pattern: {result['pattern']} (base: {result['base_score']})",
        f"  Length:  {result['length']} chars",
    ])

    for desc, val in result['penalties']:
        lines.append(f"  Penalty: {desc} ({val:+d})")
    for desc, val in result['bonuses']:
        lines.append(f"  Bonus:   {desc} ({val:+d})")

    if result['suggestions']:
        lines.append("  Fix:")
        for s in result['suggestions']:
            lines.append(f"    - {s}")

    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(
        description='Title Scorer — History YouTube Packaging System v1.0',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            'Examples:\n'
            '  python title_scorer_standalone.py "France Forced Haiti to Pay"\n'
            '  python title_scorer_standalone.py "Title A" "Title B" "Title C"\n'
            '  python title_scorer_standalone.py --file titles.txt\n'
        ),
    )
    parser.add_argument('titles', nargs='*', help='Title candidates to score')
    parser.add_argument('--file', help='File with one title per line')
    args = parser.parse_args()

    titles = []
    if args.file:
        path = Path(args.file)
        if not path.exists():
            print(f"ERROR: File not found: {args.file}")
            sys.exit(1)
        titles = [line.strip() for line in path.read_text(encoding='utf-8').splitlines() if line.strip()]
    elif args.titles:
        titles = args.titles

    if not titles:
        parser.print_help()
        sys.exit(0)

    results = [score_title(t) for t in titles]
    results.sort(key=lambda x: -x['score'])

    print("\n" + "=" * 60)
    print("  HISTORY YOUTUBE PACKAGING SYSTEM — TITLE SCORER v1.0")
    print("=" * 60)

    for i, r in enumerate(results, 1):
        print(f"\n  #{i}")
        print(format_result(r))

    if len(results) > 1:
        print("\n" + "-" * 60)
        print(f"  WINNER: {results[0]['title']}")
        print(f"  Score:  {results[0]['score']}/100 ({results[0]['grade']})")

    print()


if __name__ == '__main__':
    main()
