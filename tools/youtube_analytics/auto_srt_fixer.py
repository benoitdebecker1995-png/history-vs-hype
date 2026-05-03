"""
Auto-SRT Fixer for History vs Hype

Automatically detects and corrects common transcription errors in SRT files
by building a corrections dictionary from past SRT-FIXES.md files and
project-specific verified research documents.

Error types detected:
  - Garbled proper nouns (names of people, places, documents)
  - Geographic/technical term errors
  - Common word substitutions that change meaning
  - Spelling variants of the same proper noun

Data sources:
  - Past SRT-FIXES.md files (known corrections from manual reviews)
  - 01-VERIFIED-RESEARCH.md (project-specific proper nouns)
  - Fuzzy matching against the SRT text

Usage:
    python -m tools.youtube_analytics.auto_srt_fixer --project 43-india-pakistan-partition-2026
    python -m tools.youtube_analytics.auto_srt_fixer --srt path/to/file.srt
    python -m tools.youtube_analytics.auto_srt_fixer --project PROJECT --dry-run
    python -m tools.youtube_analytics.auto_srt_fixer --rebuild-cache

Output:
    SRT-FIXES.md (fix report) + [filename]_corrected.srt (corrected file)
"""

import argparse
import json
import re
import sys
from collections import defaultdict
from difflib import SequenceMatcher
from pathlib import Path
from typing import Optional

from tools.logging_config import get_logger, setup_logging

logger = get_logger(__name__)

# Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
PROJECTS_DIR = PROJECT_ROOT / "video-projects" / "_IN_PRODUCTION"
CACHE_PATH = Path(__file__).parent / "_srt_corrections.json"

# SRT patterns to skip (non-English, backups, already corrected)
SRT_SKIP_PATTERNS = [
    r"-es\.srt$",
    r"-farsi\.srt$",
    r"_fr\.srt$",
    r"_pt\.srt$",
    r"SPANISH",
    r"BACKUP",
    r"_corrected\.srt$",
]


# =========================================================================
# SRT PARSING (matches codebase pattern from script_srt_deviation.py)
# =========================================================================

def parse_srt(srt_path: Path) -> list[dict]:
    """Parse an SRT file into a list of subtitle blocks with metadata.

    Returns list of dicts:
        {'index': int, 'text': str, 'raw_text': str, 'start_ts': str,
         'end_ts': str, 'start_sec': float, 'end_sec': float}
    """
    # Try multiple encodings for Windows compatibility
    text = None
    for encoding in ('utf-8-sig', 'utf-8', 'cp1252', 'latin-1'):
        try:
            text = srt_path.read_text(encoding=encoding)
            break
        except (UnicodeDecodeError, UnicodeError):
            continue
    if text is None:
        text = srt_path.read_text(encoding='utf-8', errors='replace')
        logger.warning("Used lossy UTF-8 decoding for %s", srt_path.name)

    blocks = re.split(r'\n\n+', text.strip())
    subtitles = []

    for block in blocks:
        lines = block.strip().split('\n')
        if len(lines) < 3:
            continue

        # Parse index
        try:
            index = int(lines[0].strip())
        except ValueError:
            continue

        # Parse timestamp line
        ts_match = re.match(
            r'(\d{2}:\d{2}:\d{2}[,.]\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2}[,.]\d{3})',
            lines[1],
        )
        if not ts_match:
            continue

        start_ts = ts_match.group(1)
        end_ts = ts_match.group(2)

        start_sec = _ts_to_seconds(start_ts)
        end_sec = _ts_to_seconds(end_ts)

        # Join text lines, strip HTML tags
        raw_text = ' '.join(lines[2:])
        clean_text = re.sub(r'<[^>]+>', '', raw_text).strip()

        if clean_text:
            subtitles.append({
                'index': index,
                'text': clean_text,
                'raw_text': raw_text,
                'start_ts': start_ts,
                'end_ts': end_ts,
                'start_sec': start_sec,
                'end_sec': end_sec,
            })

    logger.debug("Parsed %d subtitle blocks from %s", len(subtitles), srt_path.name)
    return subtitles


def _ts_to_seconds(ts: str) -> float:
    """Convert HH:MM:SS,mmm or HH:MM:SS.mmm to seconds."""
    ts = ts.replace(',', '.')
    parts = ts.split(':')
    return int(parts[0]) * 3600 + int(parts[1]) * 60 + float(parts[2])


def _seconds_to_ts(sec: float) -> str:
    """Convert seconds back to HH:MM:SS,mmm format."""
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = sec % 60
    return f"{h:02d}:{m:02d}:{s:06.3f}".replace('.', ',')


# =========================================================================
# CORRECTIONS DICTIONARY
# =========================================================================

def build_corrections_from_fixes(fixes_paths: list[Path]) -> dict:
    """Parse SRT-FIXES.md files to extract known correction mappings.

    Returns dict with keys: known_corrections, name_patterns,
    geo_patterns, technical_patterns
    """
    corrections = {
        'known_corrections': {},   # exact: wrong -> right
        'name_patterns': {},       # wrong name -> right name
        'geo_patterns': {},        # wrong geo term -> right
        'technical_patterns': {},  # wrong technical term -> right
    }

    for path in fixes_paths:
        logger.info("Reading corrections from: %s", path.name)
        try:
            text = path.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            text = path.read_text(encoding='utf-8-sig')

        current_section = None

        for line in text.split('\n'):
            stripped = line.strip()

            # Detect section headers
            if '## CRITICAL FIXES' in stripped:
                current_section = 'known_corrections'
            elif '## NAME' in stripped or '## PROPER NOUN' in stripped:
                current_section = 'name_patterns'
            elif '## GEOGRAPHIC' in stripped or '## TECHNICAL' in stripped:
                current_section = 'geo_patterns'
            elif stripped.startswith('## '):
                current_section = None  # Other sections (FALSE START, etc.)
                continue

            if current_section is None:
                continue

            # Parse table rows: | ... | Current Text | Correct Text | ...
            if not stripped.startswith('|') or stripped.startswith('|--'):
                continue

            cells = [c.strip() for c in stripped.split('|')]
            # Filter empty cells from leading/trailing pipes
            cells = [c for c in cells if c]

            if len(cells) < 4:
                continue

            # Skip header rows
            if 'Current Text' in cells[2] or 'Correct Text' in cells[3]:
                continue
            if cells[2].startswith('---') or cells[3].startswith('---'):
                continue

            # Extract current text and correct text
            raw_current = _clean_table_cell(cells[2])
            raw_correct = _clean_table_cell(cells[3])

            # Handle slash-separated entries like:
            # "Fursopur Teghsil" / "fursopur" | "Ferozepur Tehsil" / "Ferozepur"
            current_parts = [_clean_table_cell(p) for p in raw_current.split(' / ')]
            correct_parts = [_clean_table_cell(p) for p in raw_correct.split(' / ')]

            for current_text, correct_text in zip(current_parts, correct_parts):
                if not current_text or not correct_text:
                    continue
                if current_text == correct_text:
                    continue

                # Store in appropriate category
                corrections[current_section][current_text] = correct_text

                # Also store individual words for fuzzy matching
                # e.g., "Kulledip Nair" -> extract "Kulledip" and "Nair"
                if current_section == 'name_patterns':
                    wrong_words = current_text.split()
                    right_words = correct_text.split()
                    for ww, rw in zip(wrong_words, right_words):
                        if ww.lower() != rw.lower() and len(ww) > 2:
                            corrections['name_patterns'][ww] = rw

    total = sum(len(v) for v in corrections.values())
    logger.info("Built corrections dictionary: %d total entries", total)
    for key, val in corrections.items():
        if val:
            logger.debug("  %s: %d entries", key, len(val))
    return corrections


def _clean_table_cell(cell: str) -> str:
    """Remove markdown formatting and quotes from a table cell."""
    cell = cell.strip()
    # Remove surrounding quotes
    cell = re.sub(r'^["\u201c]|["\u201d]$', '', cell)
    # Remove bold/italic
    cell = re.sub(r'\*+', '', cell)
    return cell.strip()


def extract_proper_nouns_from_research(research_path: Path) -> dict[str, str]:
    """Extract proper nouns from a 01-VERIFIED-RESEARCH.md file.

    Returns a dict of lowercase_name -> correct_spelling for people,
    places, documents, and technical terms found in the research.
    """
    nouns = {}
    try:
        text = research_path.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        text = research_path.read_text(encoding='utf-8-sig')

    # Extract from source key table (Author names, book titles)
    source_key_names = set()
    for match in re.finditer(
        r'\|\s*\*\*(\w+)\*\*\s*\|\s*([^|]+)\|', text
    ):
        code = match.group(1)
        desc = match.group(2).strip()
        source_key_names.add(code)

        # Extract author names (before comma or first *)
        author_match = re.match(r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)', desc)
        if author_match:
            name = author_match.group(1)
            for part in name.split():
                if len(part) > 2:
                    nouns[part.lower()] = part

    # Extract capitalized proper nouns from the text body
    # Look for multi-word capitalized sequences (names, places)
    for match in re.finditer(r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)\b', text):
        phrase = match.group(1)
        # Skip common non-name phrases
        skip_phrases = {'Boundary Commission', 'Terms of Reference',
                        'Royal Assent', 'Muslim League', 'Verified Research',
                        'Source Key', 'Script Approach', 'East Punjab',
                        'New Delhi', 'Section Key'}
        if phrase not in skip_phrases:
            nouns[phrase.lower()] = phrase
            for word in phrase.split():
                if len(word) > 3:
                    nouns[word.lower()] = word

    # Extract specific geographic names
    for match in re.finditer(
        r'(?:Ferozepur|Ferozepore|Gurdaspur|Pathankot|Lahore|Simla|'
        r'Amritsar|Jammu|Kashmir|Srinagar|Sutlej|Ravi|Madhopur|'
        r'Bengal|Punjab|Calcutta|Mountbatten|Radcliffe|Beaumont|'
        r'Nehru|Jinnah|Abell|Jenkins|Christie|Ismay|Michel|'
        r'Nayar|Wolpert|Sadullah|Bharadwaj|Chatterji|Metcalf|'
        r'Tehsil|Secraphone|Banihal)', text
    ):
        word = match.group(0)
        nouns[word.lower()] = word

    # Extract terms in bold that appear after "VERIFIED:"
    for match in re.finditer(r'VERIFIED:\s*(.+?)$', text, re.MULTILINE):
        claim = match.group(1)
        # Pull out capitalized words from claim
        for word_match in re.finditer(r'\b([A-Z][a-z]{2,})\b', claim):
            word = word_match.group(1)
            if word not in ('The', 'And', 'But', 'For', 'Not', 'Was', 'Had',
                            'His', 'Her', 'Its', 'Are', 'Were', 'Has', 'Did',
                            'Commission', 'Evidence'):
                nouns[word.lower()] = word

    # Extract from direct quotes (between > markers)
    for match in re.finditer(r'^>\s*"(.+?)"', text, re.MULTILINE):
        quote = match.group(1)
        for word_match in re.finditer(r'\b([A-Z][a-z]{2,})\b', quote):
            word = word_match.group(1)
            if word not in ('The', 'And', 'But', 'For', 'Not'):
                nouns[word.lower()] = word

    logger.info("Extracted %d proper nouns from %s", len(nouns), research_path.name)
    return nouns


# =========================================================================
# FUZZY MATCHING
# =========================================================================

def find_fuzzy_matches(srt_text: str, correct_term: str,
                       threshold: float = 0.70) -> list[tuple[str, float]]:
    """Find words/phrases in SRT text that fuzzy-match a correct term.

    Uses strict filters to minimize false positives:
    - Single words must be >= 5 chars and share first or last letter
    - Multi-word phrases must have at least one word with >= 0.75 match
    - Common English words are excluded

    Returns list of (wrong_text, similarity_ratio) tuples.
    """
    matches = []
    correct_lower = correct_term.lower()
    correct_words = correct_term.split()
    n_words = len(correct_words)

    # For single-word terms: only match words of similar length
    if n_words == 1 and len(correct_term) >= 5:
        words = re.findall(r'\b\w+\b', srt_text)
        seen = set()
        for word in words:
            wl = word.lower()
            if wl in seen:
                continue
            seen.add(wl)
            if wl == correct_lower:
                continue  # Already correct

            # Length filter: within +/- 2 chars
            if abs(len(word) - len(correct_term)) > 2:
                continue

            # Must share first letter OR last 2 letters (transcription errors
            # tend to preserve word shape)
            if (wl[0] != correct_lower[0] and
                    wl[-2:] != correct_lower[-2:]):
                continue

            ratio = SequenceMatcher(None, wl, correct_lower).ratio()
            if ratio >= threshold and ratio < 1.0:
                # Final check: must be a plausible proper noun garble
                # (starts with capital in SRT, or correct_term is capitalized)
                if word[0].isupper() or correct_term[0].isupper():
                    matches.append((word, ratio))

    # For multi-word terms: stricter matching
    elif n_words > 1 and len(correct_term) >= 8:
        words = re.findall(r'\b\w+\b', srt_text)
        for i in range(len(words) - n_words + 1):
            window_words = words[i:i + n_words]
            window = ' '.join(window_words)
            if window.lower() == correct_lower:
                continue

            # At least one word must start with same letter as corresponding
            # correct word AND be a plausible garble (not just a different word)
            garble_count = 0
            for ww, cw in zip(window_words, correct_words):
                wl, cl = ww.lower(), cw.lower()
                if wl == cl:
                    continue  # exact match, not a garble
                word_ratio = SequenceMatcher(None, wl, cl).ratio()
                if word_ratio >= 0.60 and wl[0] == cl[0]:
                    garble_count += 1
                else:
                    # This word is completely different — not a transcription
                    # error, it's a different phrase entirely
                    garble_count = -999
                    break

            if garble_count <= 0:
                continue

            ratio = SequenceMatcher(
                None, window.lower(), correct_lower
            ).ratio()
            if ratio >= threshold and ratio < 1.0:
                matches.append((window, ratio))

    return matches


# =========================================================================
# FIX DETECTION
# =========================================================================

class SRTFix:
    """Represents a single correction to apply."""

    CRITICAL = "CRITICAL"
    NAME = "NAME"
    GEO_TECH = "GEO_TECH"
    FUZZY = "FUZZY"

    def __init__(self, sub_index: int, timestamp: str, current: str,
                 correct: str, category: str, confidence: float = 1.0,
                 source: str = "", notes: str = ""):
        self.sub_index = sub_index
        self.timestamp = timestamp
        self.current = current
        self.correct = correct
        self.category = category
        self.confidence = confidence
        self.source = source
        self.notes = notes

    def __repr__(self):
        return (f"SRTFix(#{self.sub_index} {self.timestamp}: "
                f"'{self.current}' -> '{self.correct}' [{self.category}])")


def detect_fixes(subtitles: list[dict], corrections: dict,
                 proper_nouns: dict[str, str],
                 fuzzy_threshold: float = 0.72) -> list[SRTFix]:
    """Scan subtitles against corrections dictionary and proper nouns.

    Returns list of SRTFix objects sorted by subtitle index.
    """
    fixes = []
    all_text = ' '.join(s['text'] for s in subtitles)

    # Build combined lookup of all known wrong -> right mappings
    exact_map = {}
    exact_map.update(corrections.get('known_corrections', {}))
    exact_map.update(corrections.get('name_patterns', {}))
    exact_map.update(corrections.get('geo_patterns', {}))
    exact_map.update(corrections.get('technical_patterns', {}))

    # Categorize each mapping
    category_map = {}
    for k in corrections.get('known_corrections', {}):
        category_map[k] = SRTFix.CRITICAL
    for k in corrections.get('name_patterns', {}):
        category_map[k] = SRTFix.NAME
    for k in corrections.get('geo_patterns', {}):
        category_map[k] = SRTFix.GEO_TECH
    for k in corrections.get('technical_patterns', {}):
        category_map[k] = SRTFix.GEO_TECH

    # Pass 1: Exact matches against known corrections
    for sub in subtitles:
        text = sub['text']
        for wrong, right in exact_map.items():
            # Case-insensitive search for the wrong text in this subtitle
            pattern = re.compile(re.escape(wrong), re.IGNORECASE)
            if pattern.search(text):
                fixes.append(SRTFix(
                    sub_index=sub['index'],
                    timestamp=sub['start_ts'],
                    current=wrong,
                    correct=right,
                    category=category_map.get(wrong, SRTFix.CRITICAL),
                    confidence=1.0,
                    source="Known correction (SRT-FIXES.md)",
                    notes="Exact match from past corrections",
                ))

    # Pass 2: Fuzzy matches against proper nouns from research
    if proper_nouns:
        # Build set of all correct terms present in text — skip those
        all_text_lower = all_text.lower()

        # Only fuzzy-match proper nouns that are likely to be garbled
        # (names of people, places, documents — not common English words)
        _COMMON_ENGLISH = {
            'the', 'and', 'but', 'for', 'not', 'was', 'had', 'his', 'her',
            'its', 'are', 'were', 'has', 'did', 'with', 'from', 'that',
            'this', 'what', 'when', 'where', 'which', 'while', 'there',
            'their', 'would', 'could', 'should', 'about', 'after', 'before',
            'between', 'through', 'during', 'being', 'other', 'first',
            'later', 'never', 'still', 'every', 'under', 'over', 'also',
            'only', 'just', 'then', 'than', 'more', 'most', 'many', 'much',
            'some', 'such', 'very', 'even', 'both', 'each', 'same', 'been',
            'have', 'into', 'they', 'them', 'will', 'said', 'made', 'like',
            'time', 'year', 'make', 'know', 'take', 'come', 'here', 'thing',
            'think', 'well', 'back', 'give', 'hand', 'took', 'went', 'those',
            'house', 'part', 'three', 'state', 'states', 'death', 'deaths',
            'line', 'land', 'road', 'meeting', 'office', 'making', 'asked',
            'asking', 'using', 'based', 'case', 'fact', 'find', 'found',
            'left', 'long', 'mean', 'need', 'next', 'point', 'right',
            'show', 'side', 'told', 'turn', 'used', 'want', 'work',
            'these', 'since', 'people', 'against', 'without', 'however',
            'because', 'nothing', 'single', 'either', 'neither', 'whether',
            'ever', 'draw', 'drew', 'soon', 'late', 'date', 'race', 'thin',
            'man', 'men', 'can', 'may', 'all', 'any',
            'estate', 'estates', 'direct', 'director', 'general', 'ministry',
            'minister', 'evidence', 'violence', 'decision', 'division',
            'qualification', 'consequence', 'consequences', 'communication',
            'communications', 'commission', 'commissions', 'democratic',
            'demographic', 'demographics', 'studied', 'studies', 'study',
            'refused', 'change', 'changed', 'changes', 'majority', 'major',
            'boundary', 'boundaries', 'independence', 'legitimate', 'grave',
            'clause', 'stated', 'meaning', 'window', 'thank', 'aware',
            'displace', 'displacement', 'rationale', 'geographic',
            'justified', 'justice', 'stake', 'stakes', 'valve', 'valley',
            'angle', 'recollections', 'collection',
        }

        # Deduplicate proper nouns: only keep unique terms, skip phrases
        # that are subsets of already-matched exact corrections
        exact_corrections_lower = {v.lower() for v in exact_map.values()}

        # For each proper noun, find fuzzy matches
        checked_pairs = set()
        for correct_lower, correct_term in proper_nouns.items():
            # Skip short terms and common English words
            if len(correct_term) < 5:
                continue
            if correct_term.lower() in _COMMON_ENGLISH:
                continue

            # Skip multi-word phrases where ALL words are common English
            correct_words = correct_term.split()
            if len(correct_words) > 1:
                all_common = all(
                    w.lower() in _COMMON_ENGLISH for w in correct_words
                )
                if all_common:
                    continue

            for sub in subtitles:
                text = sub['text']
                fuzzy_matches = find_fuzzy_matches(
                    text, correct_term, threshold=fuzzy_threshold
                )
                for wrong_text, ratio in fuzzy_matches:
                    pair_key = (wrong_text.lower(), correct_term.lower())
                    if pair_key in checked_pairs:
                        continue
                    checked_pairs.add(pair_key)

                    # Skip if the wrong text is itself a known correct term
                    if wrong_text.lower() in proper_nouns:
                        continue

                    # Skip common English words (single or multi-word)
                    if wrong_text.lower() in _COMMON_ENGLISH:
                        continue
                    wrong_words = wrong_text.split()
                    if len(wrong_words) > 1 and all(
                        w.lower() in _COMMON_ENGLISH for w in wrong_words
                    ):
                        continue

                    # Skip if the correction would replace correct text
                    # with a different-meaning term from research
                    # (e.g., "Radcliffe were" -> "Radcliffe Award" is not
                    # a transcription error, it's a different sentence)
                    if len(wrong_words) > 1 and len(correct_words) > 1:
                        # If the first or last word matches exactly, the
                        # remaining words must also be plausible garbles
                        shared_exact = sum(
                            1 for ww, cw in zip(wrong_words, correct_words)
                            if ww.lower() == cw.lower()
                        )
                        # If most words match exactly, the remaining
                        # difference is likely just grammar, not an error
                        if shared_exact >= len(wrong_words) - 1:
                            # Check if the differing word is a common word
                            for ww, cw in zip(wrong_words, correct_words):
                                if ww.lower() != cw.lower():
                                    if (ww.lower() in _COMMON_ENGLISH and
                                            cw.lower() in _COMMON_ENGLISH):
                                        skip = True
                                        break
                            else:
                                skip = False
                            if skip:
                                continue

                    fixes.append(SRTFix(
                        sub_index=sub['index'],
                        timestamp=sub['start_ts'],
                        current=wrong_text,
                        correct=correct_term,
                        category=SRTFix.FUZZY,
                        confidence=ratio,
                        source="Fuzzy match vs. verified research",
                        notes=f"Similarity: {ratio:.0%}",
                    ))

    # Deduplicate: keep highest-confidence fix for each (sub_index, current)
    seen = {}
    for fix in fixes:
        key = (fix.sub_index, fix.current.lower())
        if key not in seen or fix.confidence > seen[key].confidence:
            seen[key] = fix

    result = sorted(seen.values(), key=lambda f: f.sub_index)
    logger.info("Detected %d fixes across %d subtitles", len(result), len(subtitles))
    return result


# =========================================================================
# OUTPUT: SRT-FIXES.MD
# =========================================================================

def generate_fixes_report(fixes: list[SRTFix], srt_path: Path,
                          project_slug: str = "") -> str:
    """Generate an SRT-FIXES.md report from detected fixes."""
    from datetime import datetime, timezone

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    lines = []
    lines.append(f"# SRT Fix List: {project_slug or srt_path.stem}")
    lines.append("")
    lines.append(f"**File:** `{srt_path.name}`")
    lines.append(f"**Generated:** {now} (auto-detected by auto_srt_fixer.py)")
    lines.append(f"**Status:** Review fixes below — high-confidence fixes applied automatically")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Group by category
    critical = [f for f in fixes if f.category == SRTFix.CRITICAL]
    names = [f for f in fixes if f.category == SRTFix.NAME]
    geo_tech = [f for f in fixes if f.category == SRTFix.GEO_TECH]
    fuzzy = [f for f in fixes if f.category == SRTFix.FUZZY]

    if critical:
        lines.append("## CRITICAL FIXES (Wrong word / changes meaning)")
        lines.append("")
        lines.append("| Sub # | Timestamp | Current Text | Correct Text | Confidence | Notes |")
        lines.append("|-------|-----------|-------------|--------------|------------|-------|")
        for f in critical:
            lines.append(
                f'| {f.sub_index} | {f.timestamp} | "{f.current}" '
                f'| "{f.correct}" | {f.confidence:.0%} | {f.notes} |'
            )
        lines.append("")

    if names:
        lines.append("## NAME/PROPER NOUN FIXES")
        lines.append("")
        lines.append("| Sub # | Timestamp | Current Text | Correct Text | Confidence | Notes |")
        lines.append("|-------|-----------|-------------|--------------|------------|-------|")
        for f in names:
            lines.append(
                f'| {f.sub_index} | {f.timestamp} | "{f.current}" '
                f'| "{f.correct}" | {f.confidence:.0%} | {f.notes} |'
            )
        lines.append("")

    if geo_tech:
        lines.append("## GEOGRAPHIC/TECHNICAL TERM FIXES")
        lines.append("")
        lines.append("| Sub # | Timestamp | Current Text | Correct Text | Confidence | Notes |")
        lines.append("|-------|-----------|-------------|--------------|------------|-------|")
        for f in geo_tech:
            lines.append(
                f'| {f.sub_index} | {f.timestamp} | "{f.current}" '
                f'| "{f.correct}" | {f.confidence:.0%} | {f.notes} |'
            )
        lines.append("")

    if fuzzy:
        lines.append("## FUZZY MATCHES (Review manually — may be false positives)")
        lines.append("")
        lines.append("| Sub # | Timestamp | Current Text | Suggested Correction | Confidence | Notes |")
        lines.append("|-------|-----------|-------------|---------------------|------------|-------|")
        for f in fuzzy:
            lines.append(
                f'| {f.sub_index} | {f.timestamp} | "{f.current}" '
                f'| "{f.correct}" | {f.confidence:.0%} | {f.notes} |'
            )
        lines.append("")

    if not fixes:
        lines.append("**No fixes detected.** SRT appears clean.")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append(f"**Total fixes:** {len(fixes)} "
                 f"({len(critical)} critical, {len(names)} name, "
                 f"{len(geo_tech)} geo/tech, {len(fuzzy)} fuzzy)")
    lines.append("")

    return '\n'.join(lines)


# =========================================================================
# OUTPUT: CORRECTED SRT
# =========================================================================

def apply_fixes_to_srt(srt_path: Path, fixes: list[SRTFix],
                       min_confidence: float = 0.80) -> str:
    """Apply fixes to an SRT file and return corrected text.

    Only applies fixes with confidence >= min_confidence.
    """
    # Read original file with encoding detection
    text = None
    for encoding in ('utf-8-sig', 'utf-8', 'cp1252', 'latin-1'):
        try:
            text = srt_path.read_text(encoding=encoding)
            break
        except (UnicodeDecodeError, UnicodeError):
            continue
    if text is None:
        text = srt_path.read_text(encoding='utf-8', errors='replace')

    # Build a list of replacements to apply, sorted by length (longest first)
    # to avoid partial replacements
    replacements = []
    seen_pairs = set()
    for fix in fixes:
        if fix.confidence >= min_confidence:
            pair = (fix.current, fix.correct)
            if pair not in seen_pairs:
                seen_pairs.add(pair)
                replacements.append(pair)

    # Sort by length of wrong text (longest first) to prevent partial matches
    replacements.sort(key=lambda r: len(r[0]), reverse=True)

    # Filter out replacements where the wrong text is a substring of
    # the correct text of another replacement (prevents cascading, e.g.,
    # "Abel" -> "Abell" where "Abel" is a substring of "Abell")
    filtered = []
    all_correct = {r[1] for r in replacements}
    for wrong, right in replacements:
        # Check if wrong is a substring of any correct text
        is_substring = False
        for correct_val in all_correct:
            if wrong != correct_val and wrong in correct_val:
                is_substring = True
                break
        if is_substring:
            # Use word-boundary matching to avoid substring issues
            filtered.append((wrong, right, True))  # needs_boundary=True
        else:
            filtered.append((wrong, right, False))

    applied = 0
    for wrong, right, needs_boundary in filtered:
        if needs_boundary:
            # Use word boundaries to prevent matching within already-replaced text
            pattern = re.compile(
                r'\b' + re.escape(wrong) + r'\b', re.IGNORECASE
            )
        else:
            pattern = re.compile(re.escape(wrong), re.IGNORECASE)

        new_text, count = pattern.subn(right, text)
        if count > 0:
            text = new_text
            applied += count
            logger.debug("Applied: '%s' -> '%s' (%d occurrences)", wrong, right, count)

    logger.info("Applied %d replacements to SRT", applied)
    return text


# =========================================================================
# CACHE
# =========================================================================

def save_corrections_cache(corrections: dict) -> None:
    """Save corrections dictionary to JSON cache."""
    CACHE_PATH.write_text(
        json.dumps(corrections, indent=2, ensure_ascii=False),
        encoding='utf-8',
    )
    logger.info("Saved corrections cache to %s", CACHE_PATH.name)


def load_corrections_cache() -> Optional[dict]:
    """Load corrections dictionary from JSON cache, if it exists."""
    if not CACHE_PATH.exists():
        return None
    try:
        data = json.loads(CACHE_PATH.read_text(encoding='utf-8'))
        total = sum(len(v) for v in data.values() if isinstance(v, dict))
        logger.info("Loaded %d corrections from cache", total)
        return data
    except (json.JSONDecodeError, KeyError) as e:
        logger.warning("Cache corrupted, rebuilding: %s", e)
        return None


# =========================================================================
# PROJECT DISCOVERY
# =========================================================================

def find_project_dir(project_slug: str) -> Optional[Path]:
    """Find a project directory by slug."""
    # Try exact match
    exact = PROJECTS_DIR / project_slug
    if exact.is_dir():
        return exact

    # Try partial match
    for d in PROJECTS_DIR.iterdir():
        if d.is_dir() and project_slug in d.name:
            return d

    return None


def find_srt_files(project_dir: Path) -> list[Path]:
    """Find primary SRT files in a project directory (skip non-English, backups)."""
    srt_files = list(project_dir.glob('*.srt'))
    compiled = [re.compile(p, re.IGNORECASE) for p in SRT_SKIP_PATTERNS]

    result = []
    for srt in srt_files:
        skip = False
        for pattern in compiled:
            if pattern.search(srt.name):
                skip = True
                break
        if not skip:
            result.append(srt)

    return result


def find_all_srt_fixes() -> list[Path]:
    """Find all SRT-FIXES.md files across all projects."""
    return list(PROJECTS_DIR.glob('*/SRT-FIXES.md'))


def find_verified_research(project_dir: Path) -> Optional[Path]:
    """Find the verified research file for a project."""
    candidates = [
        project_dir / '01-VERIFIED-RESEARCH.md',
        project_dir / 'VERIFIED-RESEARCH.md',
    ]
    for c in candidates:
        if c.exists():
            return c
    # Try glob
    results = list(project_dir.glob('*VERIFIED-RESEARCH*'))
    return results[0] if results else None


# =========================================================================
# MAIN
# =========================================================================

def run(project_slug: Optional[str] = None, srt_path: Optional[str] = None,
        dry_run: bool = False, rebuild_cache: bool = False,
        fuzzy_threshold: float = 0.78, min_confidence: float = 0.80) -> dict:
    """Main entry point.

    Returns dict with keys: fixes, report_path, corrected_path, stats
    """
    # Step 1: Build or load corrections dictionary
    corrections = None
    if not rebuild_cache:
        corrections = load_corrections_cache()

    if corrections is None:
        fixes_files = find_all_srt_fixes()
        if fixes_files:
            logger.info("Found %d SRT-FIXES.md files", len(fixes_files))
            corrections = build_corrections_from_fixes(fixes_files)
        else:
            logger.warning("No SRT-FIXES.md files found — starting with empty dictionary")
            corrections = {
                'known_corrections': {},
                'name_patterns': {},
                'geo_patterns': {},
                'technical_patterns': {},
            }
        save_corrections_cache(corrections)

    if rebuild_cache and not project_slug and not srt_path:
        logger.info("Cache rebuilt. Use --project or --srt to scan a file.")
        return {'fixes': [], 'stats': {'total': 0}}

    # Step 2: Locate project and SRT file
    project_dir = None
    target_srt = None

    if srt_path:
        target_srt = Path(srt_path)
        if not target_srt.exists():
            logger.error("SRT file not found: %s", srt_path)
            sys.exit(1)
        project_dir = target_srt.parent

    elif project_slug:
        project_dir = find_project_dir(project_slug)
        if not project_dir:
            logger.error("Project not found: %s", project_slug)
            sys.exit(1)

        srt_files = find_srt_files(project_dir)
        if not srt_files:
            logger.error("No SRT files found in %s", project_dir)
            sys.exit(1)

        if len(srt_files) > 1:
            logger.info("Multiple SRT files found, processing all:")
            for s in srt_files:
                logger.info("  - %s", s.name)

        target_srt = srt_files[0]  # Process first one

    else:
        logger.error("Must specify --project or --srt")
        sys.exit(1)

    logger.info("Processing: %s", target_srt.name)

    # Step 3: Extract project-specific proper nouns
    proper_nouns = {}
    if project_dir:
        research = find_verified_research(project_dir)
        if research:
            proper_nouns = extract_proper_nouns_from_research(research)
        else:
            logger.warning("No verified research found for project — "
                           "using only known corrections")

    # Step 4: Parse SRT and detect fixes
    subtitles = parse_srt(target_srt)
    if not subtitles:
        logger.error("No subtitles parsed from %s", target_srt.name)
        sys.exit(1)

    fixes = detect_fixes(
        subtitles, corrections, proper_nouns,
        fuzzy_threshold=fuzzy_threshold,
    )

    # Step 5: Generate report
    slug = project_slug or target_srt.stem
    report = generate_fixes_report(fixes, target_srt, slug)

    stats = {
        'total': len(fixes),
        'critical': len([f for f in fixes if f.category == SRTFix.CRITICAL]),
        'name': len([f for f in fixes if f.category == SRTFix.NAME]),
        'geo_tech': len([f for f in fixes if f.category == SRTFix.GEO_TECH]),
        'fuzzy': len([f for f in fixes if f.category == SRTFix.FUZZY]),
        'subtitles_scanned': len(subtitles),
    }

    print(f"\n{'=' * 60}")
    print(f"AUTO-SRT FIXER RESULTS: {target_srt.name}")
    print(f"{'=' * 60}")
    print(f"Subtitles scanned: {stats['subtitles_scanned']}")
    print(f"Total fixes found: {stats['total']}")
    print(f"  Critical:    {stats['critical']}")
    print(f"  Name:        {stats['name']}")
    print(f"  Geo/Tech:    {stats['geo_tech']}")
    print(f"  Fuzzy:       {stats['fuzzy']}")

    result = {'fixes': fixes, 'stats': stats}

    if dry_run:
        print(f"\n--- DRY RUN (no files written) ---\n")
        print(report)
        return result

    # Step 6: Write outputs
    report_path = project_dir / 'SRT-FIXES-AUTO.md'
    report_path.write_text(report, encoding='utf-8')
    print(f"\nFix report:    {report_path}")
    result['report_path'] = str(report_path)

    # Generate corrected SRT
    corrected_text = apply_fixes_to_srt(
        target_srt, fixes, min_confidence=min_confidence,
    )
    corrected_name = target_srt.stem + '_corrected' + target_srt.suffix
    corrected_path = target_srt.parent / corrected_name
    corrected_path.write_text(corrected_text, encoding='utf-8')
    print(f"Corrected SRT: {corrected_path}")
    result['corrected_path'] = str(corrected_path)

    return result


def main():
    parser = argparse.ArgumentParser(
        description="Auto-detect and fix SRT transcription errors",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m tools.youtube_analytics.auto_srt_fixer --project 43-india-pakistan-partition-2026
  python -m tools.youtube_analytics.auto_srt_fixer --project 43-india --dry-run
  python -m tools.youtube_analytics.auto_srt_fixer --srt path/to/file.srt
  python -m tools.youtube_analytics.auto_srt_fixer --rebuild-cache
        """,
    )
    parser.add_argument('--project', '-p', type=str,
                        help='Project slug (or partial match)')
    parser.add_argument('--srt', type=str,
                        help='Direct path to SRT file')
    parser.add_argument('--dry-run', '-n', action='store_true',
                        help='Show fixes without writing files')
    parser.add_argument('--rebuild-cache', action='store_true',
                        help='Rebuild corrections cache from SRT-FIXES.md files')
    parser.add_argument('--fuzzy-threshold', type=float, default=0.78,
                        help='Fuzzy match threshold (0.0-1.0, default: 0.78)')
    parser.add_argument('--min-confidence', type=float, default=0.80,
                        help='Min confidence to auto-apply fix (default: 0.80)')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Verbose logging')
    parser.add_argument('--quiet', '-q', action='store_true',
                        help='Quiet mode (errors only)')

    args = parser.parse_args()
    setup_logging(args.verbose, args.quiet)

    run(
        project_slug=args.project,
        srt_path=args.srt,
        dry_run=args.dry_run,
        rebuild_cache=args.rebuild_cache,
        fuzzy_threshold=args.fuzzy_threshold or 0.78,
        min_confidence=args.min_confidence,
    )


if __name__ == '__main__':
    main()
