"""
Thumbnail Checker — enforces thumbnail rules validated by niche benchmark.

Rules based on visual classification of 650 thumbnails across 14 edu/history channels
(classified 2026-03-20) — see tools/benchmark/THUMBNAIL-NICHE-ANALYSIS.md.

Channels grouped by content match to History vs Hype:
- CLOSEST (myth-busting+sources): Knowing Better, Three Arrows, Shaun, Kraut, WonderWhy
- CONTENT MATCH (history+docs): Atun-Shei Films, TIKhistory
- GEO FORMAT: CaspianReport, RealLifeLore
- ANIMATED: History Matters, Kings and Generals, Historia Civilis
- DIFFERENT MODEL: Fall of Civilizations, Toldinstone

Key findings (650 thumbnails, 14 channels):
- Text overlay: 87% of niche uses text → MANDATORY (only no-text channel = lowest performer)
- No talking-head face: 0% of niche → MANDATORY (faces OK as historical/subject photos)
- Maps: 31% overall, but topic-dependent:
  - Geo/territorial channels: 88% maps → use maps for border/territorial topics
  - Myth-busting channels (closest matches): 14% maps → maps optional for ideological topics
- Arrows/icons: 14% of niche (was 51% — inflated by geo channels) → OPTIONAL

Usage:
    python -m tools.preflight.thumbnail_checker "video-projects/_IN_PRODUCTION/21-haiti-independence-debt-2025"
    python -m tools.preflight.thumbnail_checker --text "Map of Indian subcontinent, bold text 'TWO CODED WORDS', arrows pointing to Ferozepore"
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from tools.logging_config import get_logger, setup_logging

logger = get_logger(__name__)

# ---------------------------------------------------------------------------
# Rules from niche benchmark (650 videos, 14 channels, classified 2026-03-20)
# See: tools/benchmark/THUMBNAIL-NICHE-ANALYSIS.md
# ---------------------------------------------------------------------------

# Text overlay: 87% of niche uses text (650 videos) → MANDATORY
# No talking-head face: 0% of niche uses selfie/talking head → MANDATORY
#   (historical/subject photos OK — 27% of closest matches use them)
# Maps: 31% overall, 88% in geo channels, 14% in myth-busting channels → TOPIC-DEPENDENT
# Arrows/icons: 14% of niche → OPTIONAL (concentrated in geo channels)

# Positive signals: geographic elements (TOPIC-DEPENDENT — 88% of geo channels, 14% of myth-busting)
MAP_SIGNALS = [
    'map', 'border', 'territory', 'satellite', 'geographic',
    'terrain', '3d map', '3d render',
    'atlantic', 'pacific', 'mediterranean', 'caribbean', 'ocean',
    'continent', 'region', 'hemisphere', 'coast', 'island',
    'arrows', 'split', 'divided', 'color contrast', 'opposing sides',
    'split-map', 'map overlay', 'document overlay', 'maritime', 'zone', 'boundary',
]

# Negative signals: talking-head faces (FORBIDDEN — 0% of niche uses selfie/talking head)
# Historical/subject photos are OK (27% of closest matches use them)
TALKING_HEAD_SIGNALS = [
    'selfie', 'talking head', 'presenter', 'host', 'youtuber',
    'headshot', 'webcam',
]

# Neutral: historical/subject face photos (acceptable in myth-busting thumbnails)
SUBJECT_FACE_SIGNALS = [
    'historical photo', 'historical figure', 'portrait of',
    'photo of', 'subject', 'target',
]

# Positive signals: text overlay (MANDATORY — 87% of niche uses text)
# Best practice: 2-4 word emotional phrase, NOT the full title
# WonderWhy style: "WHY IRELAND SPLIT", topic label
# Knowing Better style: single topic word "Neoslavery", "Pilgrims"
# CaspianReport style: "RED LINES CROSSED" (geo channels)
TEXT_OVERLAY_SIGNALS = [
    'text overlay', 'text on thumbnail', 'title text', 'bold text',
    'large text', 'font', 'typography', 'word overlay',
    'text:', 'overlay text', 'banner text', 'text block',
]

# Positive signals: arrows and icons (OPTIONAL — 14% of niche, concentrated in geo channels)
ARROW_ICON_SIGNALS = [
    'arrow', 'arrows', 'x mark', 'cross mark', 'red x',
    'flag icon', 'flag badge', 'flag overlay', 'flag pin',
    'military icon', 'icon', 'marker', 'pointer',
]

STOCK_SIGNALS = [
    'stock photo', 'stock image', 'generic', 'shutterstock',
    'getty', 'istock', 'pexels', 'unsplash',
]

DOCUMENT_ONLY_SIGNALS = [
    'document only', 'document-only', 'just the document',
    'paper only', 'letter only',
]


def _extract_thumbnail_section(metadata: str) -> Optional[str]:
    """Extract the ## THUMBNAIL section from YOUTUBE-METADATA.md.

    Filters out "DO NOT USE" / "Forbidden" sub-sections and competitor
    differentiation tables, which contain negative examples that would
    trigger false positives.
    """
    lines = metadata.splitlines()
    in_section = False
    in_exclusion = False
    section_lines = []

    for line in lines:
        stripped = line.strip().lower()
        if stripped.startswith('## thumbnail'):
            in_section = True
            continue
        if in_section and re.match(r'^##\s+(?!thumbnail)', line, re.I):
            break
        if not in_section:
            continue

        # Skip "DO NOT USE" / "Forbidden" sub-sections
        if 'do not use' in stripped or 'forbidden' in stripped:
            in_exclusion = True
            continue
        # End exclusion at next sub-heading or concept
        if in_exclusion and (stripped.startswith('**concept') or stripped.startswith('**packaging')
                            or stripped.startswith('---')):
            in_exclusion = False
        if in_exclusion:
            continue

        section_lines.append(line)

    if not section_lines:
        return None
    return '\n'.join(section_lines)


def _has_signal(text: str, signals: List[str], exclude_negated: bool = False) -> Tuple[bool, List[str]]:
    """Check if text contains any of the signal phrases.

    Args:
        exclude_negated: If True, skip matches preceded by "no ", "no\n", "not ", "without "
    """
    lower = text.lower()
    found = []
    for s in signals:
        idx = lower.find(s)
        if idx == -1:
            continue
        if exclude_negated:
            # Check if preceded by negation
            prefix = lower[max(0, idx - 10):idx].strip()
            if prefix.endswith(('no', 'not', 'without', "don't", "doesn't", 'never', 'must not')):
                continue
        found.append(s)
    return bool(found), found


def check_thumbnail(text: str, is_person_focused: bool = False,
                    is_territorial: bool = False) -> Dict:
    """Check thumbnail concept text against niche-validated rules.

    Rules based on visual classification of 650 thumbnails across 14 edu/history
    channels (2026-03-20). See tools/benchmark/THUMBNAIL-NICHE-ANALYSIS.md.

    Args:
        text: Thumbnail concept description (from YOUTUBE-METADATA.md or direct input)
        is_person_focused: True if the video IS about a specific person (face exception)
        is_territorial: True if the video is about border disputes, territorial claims,
                       or geographic topics (makes map element more important)

    Returns:
        Dict with score (0-100), verdict, issues, and passes.
    """
    lower = text.lower()
    issues: List[str] = []
    passes: List[str] = []
    score = 100  # Start at 100, deduct for violations

    # Auto-detect territorial topic from text
    territorial_signals = ['border', 'territory', 'dispute', 'claim', 'treaty',
                           'partition', 'colonial', 'island', 'maritime', 'annex']
    if not is_territorial:
        is_territorial = any(s in lower for s in territorial_signals)

    # --- RULE 1: Text overlay (MANDATORY — 87% of niche, n=650) ---
    # 87% of niche uses text, including 87% of closest content matches.
    # Only no-text channel (Toldinstone, 20% text) has lowest median views (111K).
    # Best: 2-4 word phrase. NOT the full title.
    has_text, text_matches = _has_signal(text, TEXT_OVERLAY_SIGNALS, exclude_negated=True)
    if has_text:
        passes.append(f"Text overlay present (87% of niche, n=650): {', '.join(text_matches[:2])}")
        score += 5  # Small bonus
    else:
        if 'no text' in lower:
            issues.append("NO TEXT OVERLAY — 87% of niche uses text (n=650). Add 2-4 word phrase. "
                          "E.g. 'BORDER ERASED', 'THE MEMO', 'WHY HERE?'")
            score -= 15
        else:
            issues.append("MISSING TEXT OVERLAY — Add 2-4 word phrase on thumbnail. "
                          "WonderWhy style: 'WHY IRELAND SPLIT'. Knowing Better style: single topic word.")
            score -= 10

    # --- RULE 1b: Text length check (12-char hard limit) ---
    # Thumbnails with under 12 text characters significantly outperform.
    # "ELIMINATE SALIENT" (17 chars) failed 2-second comprehension in Ferozepur test.
    text_overlay_match = re.search(
        r'["\u201c]([^"\u201d]+)["\u201d]',  # Extract quoted text overlay
        text
    )
    if text_overlay_match:
        overlay_text = text_overlay_match.group(1).strip()
        char_count = len(overlay_text)
        if char_count > 12:
            issues.append(f"TEXT TOO LONG — \"{overlay_text}\" is {char_count} chars (max 12). "
                          "Shorten to 1-2 words. Ferozepur lesson: jargon + long text fails comprehension.")
            score -= 10
        elif char_count <= 7:
            passes.append(f"Text overlay \"{overlay_text}\" is {char_count} chars (excellent — under 7)")
            score += 3
        else:
            passes.append(f"Text overlay \"{overlay_text}\" is {char_count} chars (under 12 limit)")

    # --- RULE 2: No talking-head face (0% of niche uses selfie/talking head) ---
    # Historical/subject photos are acceptable (27% of closest matches use them)
    has_talking_head, th_matches = _has_signal(text, TALKING_HEAD_SIGNALS, exclude_negated=True)
    has_subject_face, sf_matches = _has_signal(text, SUBJECT_FACE_SIGNALS, exclude_negated=True)
    # Also check generic 'face' signal
    has_generic_face = 'face' in lower and not any(
        lower[max(0, lower.find('face') - 10):lower.find('face')].strip().endswith(neg)
        for neg in ('no', 'not', 'without', "don't", 'never')
    )

    if has_talking_head:
        issues.append(f"TALKING HEAD — 0% of edu/history niche uses selfie/talking head (n=650): {', '.join(th_matches)}")
        score -= 30
    elif has_subject_face or (has_generic_face and is_person_focused):
        passes.append("Historical/subject face photo (acceptable — 27% of closest matches use subject photos)")
    elif has_generic_face and not is_person_focused:
        issues.append("FACE DETECTED — Specify if this is a historical/subject photo (OK) or creator face (not OK)")
        score -= 10
    else:
        passes.append("No talking-head face (0% of niche norm)")

    # --- RULE 3: Geographic/map element (TOPIC-DEPENDENT) ---
    # Territorial topics: 88% of geo channels use maps → strongly recommended
    # Myth-busting topics: 14% of closest matches use maps → optional
    has_map, map_matches = _has_signal(text, MAP_SIGNALS)
    if has_map:
        passes.append(f"Map/geographic element detected: {', '.join(map_matches[:3])}")
    elif is_territorial:
        issues.append("NO MAP FOR TERRITORIAL TOPIC — Geo channels use maps 88% of the time. "
                      "Territorial/border topics should have map-first thumbnails.")
        score -= 20
    else:
        # For non-territorial topics, map is optional — myth-busting channels only use maps 14%
        passes.append("No map (acceptable for non-territorial topic — myth-busting channels average 14% map usage)")

    # --- RULE 4: Arrows/icons (OPTIONAL — 14% of niche) ---
    has_arrows, arrow_matches = _has_signal(text, ARROW_ICON_SIGNALS)
    if has_arrows:
        passes.append(f"Arrows/icons detected: {', '.join(arrow_matches[:2])}")
    # No penalty — arrows are optional (14% of niche, concentrated in geo channels)

    # --- RULE 5: No stock photography ---
    has_stock, stock_matches = _has_signal(text, STOCK_SIGNALS)
    if has_stock:
        issues.append(f"STOCK IMAGERY — Use custom maps/documents instead: {', '.join(stock_matches)}")
        score -= 15

    # --- RULE 6: No document-only (must pair with geographic context) ---
    has_doc_only, doc_matches = _has_signal(text, DOCUMENT_ONLY_SIGNALS)
    if has_doc_only:
        issues.append("DOCUMENT-ONLY — Pair documents with geographic context (map + document overlay)")
        score -= 15

    # --- RULE 7: Color contrast ---
    contrast_signals = ['color contrast', 'two colors', 'opposing', 'split',
                        'warm', 'cool', 'red', 'blue', 'gold', 'faded',
                        'rich', 'drained', 'bright', 'dark']
    has_contrast, contrast_matches = _has_signal(text, contrast_signals)
    if has_contrast:
        passes.append(f"Color contrast detected: {', '.join(contrast_matches[:3])}")
    else:
        issues.append("NO COLOR CONTRAST — Use two distinct colors showing opposing sides")
        score -= 10

    # --- RULE 8: Clean composition ---
    busy_signals = ['busy', 'cluttered', 'complex background', 'many elements',
                    'collage', 'montage']
    has_busy, _ = _has_signal(text, busy_signals)
    if has_busy:
        issues.append("BUSY COMPOSITION — Simplify to clean, high-contrast geographic view")
        score -= 10

    # --- Check for 3-concept structure ---
    concept_count = len(re.findall(r'concept [abc]|option [abc]|thumbnail [abc]|\*\*[abc]\*\*',
                                    lower))
    if concept_count >= 2:
        passes.append(f"{concept_count} thumbnail concepts provided (A/B testing ready)")
    elif concept_count == 0:
        issues.append("SINGLE CONCEPT — Create 3 concepts for A/B testing")

    # Clamp score
    score = max(0, min(100, score))

    # Verdict
    if score >= 80:
        verdict = "PASS"
    elif score >= 60:
        verdict = "REVIEW"
    else:
        verdict = "FAIL"

    return {
        'score': score,
        'verdict': verdict,
        'issues': issues,
        'passes': passes,
        'text_analyzed': text[:200] + '...' if len(text) > 200 else text,
    }


def check_project(project_path: str, is_person_focused: bool = False,
                   is_territorial: bool = False) -> Dict:
    """Check thumbnail from a project's YOUTUBE-METADATA.md."""
    project = Path(project_path)

    # Find metadata file (try multiple naming patterns)
    metadata_text = None
    for pattern in ['*YOUTUBE-METADATA*', '*youtube-metadata*', '*METADATA*']:
        for f in project.glob(pattern):
            if f.suffix == '.md':
                try:
                    metadata_text = f.read_text(encoding='utf-8')
                except UnicodeDecodeError:
                    metadata_text = f.read_text(encoding='cp1252')
                break
        if metadata_text:
            break

    if not metadata_text:
        return {
            'score': 0,
            'verdict': 'MISSING',
            'issues': ['No YOUTUBE-METADATA.md found — create thumbnail concepts before filming'],
            'passes': [],
            'text_analyzed': '',
        }

    thumb_section = _extract_thumbnail_section(metadata_text)
    if not thumb_section:
        return {
            'score': 0,
            'verdict': 'MISSING',
            'issues': ['No ## THUMBNAIL section in YOUTUBE-METADATA.md — add thumbnail concepts'],
            'passes': [],
            'text_analyzed': '',
        }

    return check_thumbnail(thumb_section, is_person_focused, is_territorial)


def print_report(result: Dict) -> None:
    """Print human-readable thumbnail check report."""
    verdict = result['verdict']
    score = result['score']

    # Color coding for terminal
    colors = {'PASS': '\033[32m', 'REVIEW': '\033[33m', 'FAIL': '\033[31m', 'MISSING': '\033[31m'}
    reset = '\033[0m'

    if sys.stderr.isatty():
        v_display = f"{colors.get(verdict, '')}{verdict}{reset}"
    else:
        v_display = verdict

    print(f"\n{'=' * 60}")
    print(f"  THUMBNAIL CHECK")
    print(f"{'=' * 60}")
    print(f"\n  Verdict: {v_display} ({score}/100)")

    if result['passes']:
        print(f"\n  PASSES:")
        for p in result['passes']:
            print(f"    + {p}")

    if result['issues']:
        print(f"\n  ISSUES:")
        for issue in result['issues']:
            print(f"    ! {issue}")

    print(f"\n{'=' * 60}\n")


def main():
    parser = argparse.ArgumentParser(
        description="Check thumbnail concept against PACKAGING_MANDATE rules"
    )
    parser.add_argument("project", nargs='?', help="Project folder path")
    parser.add_argument("--text", help="Direct thumbnail description text to check")
    parser.add_argument("--person-focused", action="store_true",
                        help="Video is about a specific person (allows face)")
    parser.add_argument("--territorial", action="store_true",
                        help="Video is about territorial/border disputes (makes map more important)")
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("-q", "--quiet", action="store_true")
    args = parser.parse_args()

    setup_logging(args.verbose, args.quiet)

    if args.text:
        result = check_thumbnail(args.text, args.person_focused, getattr(args, 'territorial', False))
    elif args.project:
        result = check_project(args.project, args.person_focused, getattr(args, 'territorial', False))
    else:
        parser.print_help()
        sys.exit(1)

    print_report(result)

    # Exit code: 0=PASS, 1=REVIEW, 2=FAIL/MISSING
    exit_codes = {'PASS': 0, 'REVIEW': 1, 'FAIL': 2, 'MISSING': 2}
    sys.exit(exit_codes.get(result['verdict'], 2))


if __name__ == '__main__':
    main()
