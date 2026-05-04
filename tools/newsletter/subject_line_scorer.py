"""
Subject Line Scorer — Grades Substack subject lines against open-rate data.

Scores subject lines 0-100 based on email open-rate research and
Substack history/education niche patterns.

Data sources (collected 2026-03-26):
    - Character length: 36-50 chars = highest open rates (mobile truncation)
    - Word count: 6-10 words = highest open rates
    - "How to" opener: -57% fewer opens (salesso.com, salesgenie.com)
    - Curiosity gap: +19% over direct benefit (kaleighmoore.com)
    - Specific number: +12-15% bonus (salesgenie.com)
    - Contrarian framing: high engagement in education niche
    - Emojis: skip — academic tone mismatch for this channel
    - A/B testing: available at 200+ subscribers on Substack

    Niche comps (Substack history top 50):
    - Mastroianni (Experimental History): short contrarian, 6-10 words
    - Howes (Age of Invention): branded prefix + topic, ~8-12 words
    - Tooze (Chartbook): long academic, 12-20 words (trust play at scale)
    - Richardson: date-only (not replicable at <100K subscribers)
    - Greene (History Can't Hide): high-energy, curiosity-gap heavy

    At 0-1K subscribers, Mastroianni's pattern (short, contrarian, curiosity)
    outperforms Tooze's (long, academic) and Richardson's (date-only trust play).

Usage:
    python -m tools.newsletter.subject_line_scorer "Subject Line Here"
    python -m tools.newsletter.subject_line_scorer "Line A" "Line B" "Line C"
    python -m tools.newsletter.subject_line_scorer --file subjects.txt
"""

import re
import sys
from pathlib import Path
from tools.logging_config import get_logger

logger = get_logger(__name__)

# =============================================================================
# CONSTANTS — all derived from measured data
# =============================================================================

# Character length (mobile truncation data)
CHAR_SWEET_SPOT = (36, 50)      # highest open rates
CHAR_ACCEPTABLE = (25, 60)      # acceptable range
CHAR_GMAIL_CUTOFF = 70          # Gmail desktop truncation
CHAR_MOBILE_CUTOFF = 40         # iPhone/Gmail app truncation

# Word count
WORD_SWEET_SPOT = (6, 10)       # highest open rates
WORD_ACCEPTABLE = (4, 14)       # acceptable range

# Penalties
HOW_TO_PENALTY = -25            # "How to" openers: -57% fewer opens
COLON_PENALTY = -15             # brand prefix colons reduce curiosity gap
QUESTION_MARK_BONUS = 5         # questions slightly lift opens in edu niche
CLICKBAIT_PENALTY = -30         # spam trigger words

# Bonuses
CURIOSITY_GAP_BONUS = 15        # +19% measured lift
SPECIFIC_NUMBER_BONUS = 10      # +12-15% lift
CONTRARIAN_BONUS = 10           # high engagement in edu/history niche
VERDICT_BONUS = 8               # strong statement (Calm Prosecutor voice)
ACTIVE_VERB_BONUS = 5           # action verbs lift opens

# Base score
BASE_SCORE = 50

# AI slop / generic newsletter phrases
SLOP_PHRASES = [
    'deep dive', 'comprehensive guide', 'everything you need to know',
    'in this issue', 'this week in', 'weekly roundup', 'monthly digest',
    'let\'s explore', 'let\'s dive', 'unpacking', 'breaking down',
    'a closer look', 'what you missed', 'icymi',
]

# Clickbait / spam triggers
SPAM_TRIGGERS = [
    'shocking', 'you won\'t believe', 'mind-blowing', 'insane',
    'exposed', 'the truth about', 'act now', 'exclusive deal',
    'don\'t miss', 'last chance', 'free', 'limited time',
    'click here', 'subscribe now',
]

# Curiosity gap indicators
CURIOSITY_MARKERS = [
    r'\bnot\b.*\bbut\b',           # "not X but Y"
    r'\bisn\'t\b',                  # "X isn't what you think"
    r'\bwasn\'t\b',
    r'\bnever\b',                   # "The treaty nobody ever read"
    r'\bactually\b',                # "What X actually says"
    r'\breally\b',                  # "What really happened"
    r'\bwrong\b',                   # "Why everyone gets X wrong"
    r'\bmyth\b',                    # myth-busting signal
    r'\blie\b',
    r'\bhidden\b',
    r'\bforgotten\b',
    r'\bmissing\b',
    r'\bsecret\b',                  # borderline — OK for edu, bad if clickbait
    r'\bno one\b',
    r'\bnobody\b',
    r'\bstill\b',                   # "X is still Y" — modern relevance
]

# Contrarian framing indicators
CONTRARIAN_MARKERS = [
    r'\bboth\s+sides\b',
    r'\beveryone\s+gets\b',
    r'\bwhat\s+\w+\s+got\s+wrong\b',
    r'\bthe\s+opposite\b',
    r'\bbackwards\b',
    r'\bnot\s+what\s+you\s+think\b',
    r'\bisn\'t\s+what\b',
    r'\bwasn\'t\s+\w+\b',
    r'^no[,.]',                      # "No, X didn't Y"
    r'\bstop\b',
    r'\bforget\b',
]

# Active verbs (history/evidence niche)
ACTIVE_VERBS = [
    'destroyed', 'erased', 'redrew', 'deleted', 'stole', 'conquered',
    'divided', 'broke', 'killed', 'buried', 'forged', 'invented',
    'rewrote', 'silenced', 'burned', 'sold', 'bought', 'lost',
    'found', 'proved', 'disproved', 'debunked', 'translated',
    'read', 'uncovered', 'measured',
]

# Verdict indicators (Calm Prosecutor voice)
VERDICT_MARKERS = [
    r'^the\s+\w+\s+(was|is|were)\s+',       # "The treaty was a fraud"
    r'(was|is)\s+(a\s+)?(lie|fraud|myth|fake|forgery)',
    r'\bdidn\'t\b',                          # "X didn't happen"
    r'\bnever\s+(happened|existed|worked)',
    r'\bwas\s+wrong\b',
]


# =============================================================================
# SCORING FUNCTIONS
# =============================================================================

def _score_length(subject: str) -> tuple[int, list[str]]:
    """Score character and word length. Returns (score_delta, warnings)."""
    delta = 0
    warnings = []
    chars = len(subject)
    words = len(subject.split())

    # Character length
    if CHAR_SWEET_SPOT[0] <= chars <= CHAR_SWEET_SPOT[1]:
        delta += 10
    elif CHAR_ACCEPTABLE[0] <= chars <= CHAR_ACCEPTABLE[1]:
        delta += 3
    elif chars > CHAR_GMAIL_CUTOFF:
        delta -= 15
        warnings.append(f"TRUNCATED on all clients ({chars} chars > {CHAR_GMAIL_CUTOFF} Gmail limit)")
    elif chars > CHAR_MOBILE_CUTOFF:
        delta -= 5
        warnings.append(f"Truncated on mobile ({chars} chars > {CHAR_MOBILE_CUTOFF} iPhone limit)")
    elif chars < CHAR_ACCEPTABLE[0]:
        delta -= 5
        warnings.append(f"Very short ({chars} chars) — may lack context")

    # Word count
    if WORD_SWEET_SPOT[0] <= words <= WORD_SWEET_SPOT[1]:
        delta += 10
    elif WORD_ACCEPTABLE[0] <= words <= WORD_ACCEPTABLE[1]:
        delta += 3
    elif words > WORD_ACCEPTABLE[1]:
        delta -= 10
        warnings.append(f"Too many words ({words}) — sweet spot is {WORD_SWEET_SPOT[0]}-{WORD_SWEET_SPOT[1]}")
    elif words < WORD_ACCEPTABLE[0]:
        delta -= 5
        warnings.append(f"Very few words ({words}) — may not convey enough")

    return delta, warnings


def _score_patterns(subject: str) -> tuple[int, list[str], list[str]]:
    """Score pattern matches. Returns (score_delta, warnings, bonuses)."""
    delta = 0
    warnings = []
    bonuses = []
    lower = subject.lower()

    # === PENALTIES ===

    # "How to" opener: -57% fewer opens
    if re.match(r'^how\s+to\b', lower):
        delta += HOW_TO_PENALTY
        warnings.append('"How to" opener: -57% fewer opens (move to subtitle or body)')

    # Colon (brand prefix pattern)
    if ':' in subject:
        delta += COLON_PENALTY
        warnings.append("Colon splits attention — integrate brand into voice, not prefix")

    # Clickbait / spam triggers
    for trigger in SPAM_TRIGGERS:
        if trigger in lower:
            delta += CLICKBAIT_PENALTY
            warnings.append(f"Spam trigger: '{trigger}' — kills deliverability + trust")
            break  # one penalty is enough

    # AI slop / generic newsletter phrases
    for phrase in SLOP_PHRASES:
        if phrase in lower:
            delta -= 15
            warnings.append(f"Generic newsletter phrase: '{phrase}' — doesn't signal academic authority")
            break

    # Year in subject line (same penalty as YouTube titles)
    if re.search(r'\b(1[0-9]{3}|20[0-2][0-9])\b', subject):
        # Only penalize if it's the FOCUS — dates embedded in quotes/context are OK
        year_match = re.search(r'\b(1[0-9]{3}|20[0-2][0-9])\b', subject)
        if year_match:
            pos = year_match.start() / max(len(subject), 1)
            if pos < 0.3:  # year in first third = likely focus
                delta -= 10
                warnings.append("Year in first third — front-load the mystery, not the date")

    # === BONUSES ===

    # Curiosity gap
    curiosity_hits = sum(1 for m in CURIOSITY_MARKERS if re.search(m, lower))
    if curiosity_hits >= 2:
        delta += CURIOSITY_GAP_BONUS
        bonuses.append(f"Strong curiosity gap ({curiosity_hits} markers)")
    elif curiosity_hits == 1:
        delta += CURIOSITY_GAP_BONUS // 2
        bonuses.append("Mild curiosity gap")

    # Specific number
    if re.search(r'\b\d+[,%]?\b', subject) and not re.search(r'\b(1[0-9]{3}|20[0-2][0-9])\b', subject):
        delta += SPECIFIC_NUMBER_BONUS
        bonuses.append("Specific number — +12-15% open rate lift")

    # Contrarian framing
    contrarian_hits = sum(1 for m in CONTRARIAN_MARKERS if re.search(m, lower))
    if contrarian_hits >= 1:
        delta += CONTRARIAN_BONUS
        bonuses.append("Contrarian framing — high engagement in edu niche")

    # Active verb
    for verb in ACTIVE_VERBS:
        if re.search(rf'\b{verb}\w*\b', lower):
            delta += ACTIVE_VERB_BONUS
            bonuses.append(f"Active verb: '{verb}'")
            break  # one bonus is enough

    # Verdict / strong statement
    for pattern in VERDICT_MARKERS:
        if re.search(pattern, lower):
            delta += VERDICT_BONUS
            bonuses.append("Verdict statement — Calm Prosecutor voice")
            break

    # Question mark (mild lift in edu niche)
    if '?' in subject:
        delta += QUESTION_MARK_BONUS
        bonuses.append("Question format — mild open-rate lift")

    return delta, warnings, bonuses


def _grade(score: int) -> str:
    """Convert score to letter grade."""
    if score >= 85:
        return 'A'
    elif score >= 70:
        return 'B'
    elif score >= 55:
        return 'C'
    elif score >= 40:
        return 'D'
    else:
        return 'F'


def _mobile_preview(subject: str) -> str:
    """Show what the subject looks like on mobile (40-char truncation)."""
    if len(subject) <= CHAR_MOBILE_CUTOFF:
        return subject
    return subject[:CHAR_MOBILE_CUTOFF - 3] + '...'


# =============================================================================
# PUBLIC API
# =============================================================================

def score_subject_line(subject: str) -> dict:
    """
    Score a single subject line.

    Returns:
        dict with keys: subject, score, grade, mobile_preview,
                        char_count, word_count, warnings, bonuses
    """
    subject = subject.strip()
    if not subject:
        return {'subject': '', 'score': 0, 'grade': 'F', 'warnings': ['Empty subject line']}

    score = BASE_SCORE

    length_delta, length_warnings = _score_length(subject)
    pattern_delta, pattern_warnings, pattern_bonuses = _score_patterns(subject)

    score += length_delta + pattern_delta
    score = max(0, min(100, score))

    return {
        'subject': subject,
        'score': score,
        'grade': _grade(score),
        'mobile_preview': _mobile_preview(subject),
        'char_count': len(subject),
        'word_count': len(subject.split()),
        'warnings': length_warnings + pattern_warnings,
        'bonuses': pattern_bonuses,
    }


def score_batch(subjects: list[str]) -> list[dict]:
    """Score multiple subject lines and return sorted by score descending."""
    results = [score_subject_line(s) for s in subjects if s.strip()]
    results.sort(key=lambda r: r['score'], reverse=True)
    return results


def format_result(result: dict, rank: int = None) -> str:
    """Format a single result for display."""
    lines = []
    prefix = f"#{rank} " if rank else ""
    lines.append(f"{prefix}{result['grade']} ({result['score']}/100): {result['subject']}")
    lines.append(f"   {result['char_count']} chars, {result['word_count']} words | Mobile: \"{result['mobile_preview']}\"")

    if result.get('bonuses'):
        for b in result['bonuses']:
            lines.append(f"   + {b}")
    if result.get('warnings'):
        for w in result['warnings']:
            lines.append(f"   - {w}")

    return '\n'.join(lines)


def format_batch(results: list[dict]) -> str:
    """Format batch results for display."""
    lines = []
    for i, r in enumerate(results, 1):
        lines.append(format_result(r, rank=i))
        lines.append('')
    return '\n'.join(lines)


# =============================================================================
# CLI
# =============================================================================

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='Subject Line Scorer — History vs Hype Newsletter',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            'Examples:\n'
            '  python -m tools.newsletter.subject_line_scorer "The Treaty Nobody Read"\n'
            '  python -m tools.newsletter.subject_line_scorer "Line A" "Line B" "Line C"\n'
            '  python -m tools.newsletter.subject_line_scorer --file subjects.txt\n'
        ),
    )
    parser.add_argument('subjects', nargs='*', help='Subject line(s) to score')
    parser.add_argument('--file', '-f', help='File with one subject line per line')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    args = parser.parse_args()

    subjects = list(args.subjects) if args.subjects else []

    if args.file:
        path = Path(args.file)
        if not path.exists():
            logger.error(f"File not found: {args.file}")
            sys.exit(1)
        subjects.extend(line.strip() for line in path.read_text(encoding='utf-8').splitlines() if line.strip())

    if not subjects:
        parser.print_help()
        sys.exit(1)

    results = score_batch(subjects)

    if args.json:
        import json
        print(json.dumps(results, indent=2))
    else:
        print(format_batch(results))


if __name__ == '__main__':
    main()
