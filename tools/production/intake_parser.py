"""
Intake Parser Module

Auto-classifies pasted VidIQ/Gemini response text into structured data types
and persists results to EXTERNAL-INTELLIGENCE.json per video project.

Supports 5 response types:
    keyword_data       — Keywords with volume/competition metrics
    title_suggestions  — Numbered title candidates
    thumbnail_concepts — Visual/compositional descriptions
    description_draft  — Multi-paragraph YouTube description prose
    tag_set            — Comma-separated keyword tags

Usage:
    from tools.production.intake_parser import classify_paste, save_session

    result = classify_paste(pasted_text)
    # {'type': 'keyword_data', 'confidence': 0.75, 'parsed_items': [...], 'preview': '...'}

    saved = save_session(project_path, 'vidiq_pro_coach', result, pasted_text)
    # {'saved_to': str, 'session_id': str} or {'error': str}
"""

import json
import re
from datetime import datetime, timezone
from pathlib import Path

from tools.logging_config import get_logger

logger = get_logger(__name__)


# ---------------------------------------------------------------------------
# Detection signal patterns (5 response types)
# ---------------------------------------------------------------------------

_KEYWORD_SIGNALS = [
    re.compile(r'\b(?:search\s+volume|monthly\s+searches)\b', re.IGNORECASE),
    re.compile(r'\b\d+\s*/\s*100\b'),
    re.compile(r'\bcompetition[:\s]+\d+', re.IGNORECASE),
    re.compile(r'\bvolume[:\s]+[\d,]+', re.IGNORECASE),
    re.compile(r'\bscore[:\s]+\d+', re.IGNORECASE),
    re.compile(r'\bkeyword\b', re.IGNORECASE),
]

_TITLE_SIGNALS = [
    re.compile(r'^\d+[\.\)]\s+[A-Z].{20,70}$', re.MULTILINE),
    re.compile(r'\bTitle[:\s]', re.IGNORECASE),
    re.compile(r'^\d+\.\s+".{20,70}"', re.MULTILINE),
    re.compile(r'\b\d{2,3}\s*(?:char|character)', re.IGNORECASE),
]

_THUMBNAIL_SIGNALS = [
    re.compile(r'\bthumbnail\b', re.IGNORECASE),
    re.compile(r'\bvisual\b', re.IGNORECASE),
    re.compile(r'\b(?:background|foreground)\b', re.IGNORECASE),
    re.compile(r'\b(?:composition|focal\s+point)\b', re.IGNORECASE),
    re.compile(r'\b(?:left|right|split|overlay)\b', re.IGNORECASE),
    re.compile(r'\bcolor\s*(?:palette|scheme)\b', re.IGNORECASE),
]

_DESCRIPTION_SIGNALS = [
    re.compile(r'^#{1,3}\s', re.MULTILINE),
    re.compile(r'#\w+'),  # hashtags
    re.compile(r'\b(?:subscribe|like\s+and|comment\s+below)\b', re.IGNORECASE),
    re.compile(r'\b(?:in\s+this\s+video|watch\s+next|learn\s+more)\b', re.IGNORECASE),
]

_TAG_SIGNALS = [
    # Detected by content structure rather than individual regexes
]


def classify_paste(text: str) -> dict:
    """Auto-classify pasted VidIQ/Gemini response text.

    Uses regex scoring across 5 response types. Best score wins.
    If best score < 0.25, returns 'unknown'.

    Args:
        text: Raw pasted text from VidIQ Pro Coach or Gemini.

    Returns:
        {
            'type': str,          # 'keyword_data' | 'title_suggestions' | etc.
            'confidence': float,  # 0.0-1.0
            'parsed_items': list, # Extracted structured items
            'preview': str        # Short preview for user confirmation
        }
    """
    if not text or not text.strip():
        return {
            'type': 'unknown',
            'confidence': 0.0,
            'parsed_items': [],
            'preview': 'Empty input',
        }

    text = text.strip()

    # Score each type
    scores = {}
    scores['keyword_data'] = _score_signals(text, _KEYWORD_SIGNALS)
    scores['title_suggestions'] = _score_signals(text, _TITLE_SIGNALS)
    scores['thumbnail_concepts'] = _score_signals(text, _THUMBNAIL_SIGNALS)
    scores['description_draft'] = _score_signals(text, _DESCRIPTION_SIGNALS)
    scores['tag_set'] = _score_tag_signals(text)

    logger.debug("Classification scores: %s", scores)

    # Best score wins
    best_type = max(scores, key=scores.get)
    best_score = scores[best_type]

    if best_score < 0.25:
        return {
            'type': 'unknown',
            'confidence': best_score,
            'parsed_items': [],
            'preview': f'Could not classify (best score: {best_score:.2f} for {best_type})',
        }

    # Parse items for the detected type
    parsed_items = _parse_items(text, best_type)
    preview = _build_preview(best_type, parsed_items)

    logger.info("Classified as %s (confidence: %.2f)", best_type, best_score)

    return {
        'type': best_type,
        'confidence': round(best_score, 2),
        'parsed_items': parsed_items,
        'preview': preview,
    }


def load_or_create_intelligence(project_path: str) -> dict:
    """Load existing EXTERNAL-INTELLIGENCE.json or return empty scaffold.

    Args:
        project_path: Path to the video project folder.

    Returns:
        Intelligence data dict (loaded or fresh scaffold).
    """
    p = Path(project_path) / "EXTERNAL-INTELLIGENCE.json"
    if p.exists():
        try:
            data = json.loads(p.read_text(encoding='utf-8'))
            logger.debug("Loaded existing intelligence: %s (%d sessions)", p, len(data.get('sessions', [])))
            return data
        except json.JSONDecodeError as e:
            logger.warning("Corrupt EXTERNAL-INTELLIGENCE.json, creating fresh: %s", e)
            return _empty_scaffold(project_path)
    return _empty_scaffold(project_path)


def save_session(project_path: str, source: str, classified: dict, raw_text: str) -> dict:
    """Append a classified session to EXTERNAL-INTELLIGENCE.json.

    Args:
        project_path: Path to the video project folder.
        source: 'vidiq_pro_coach' or 'gemini'.
        classified: Output of classify_paste().
        raw_text: Original pasted text (preserved for re-parsing).

    Returns:
        {'saved_to': str, 'session_id': str} on success, {'error': str} on failure.
    """
    try:
        data = load_or_create_intelligence(project_path)

        # Auto-increment session ID
        session_count = len(data.get('sessions', []))
        session_id = f"s{session_count + 1}"

        # Calculate parseable ratio
        parsed_count = len(classified.get('parsed_items', []))
        estimated_total = _estimate_total_items(raw_text, classified.get('type', 'unknown'))
        parseable_ratio = round(parsed_count / max(estimated_total, 1), 2)

        session = {
            'session_id': session_id,
            'source': source,
            'type': classified.get('type', 'unknown'),
            'raw': raw_text,
            'parsed': _structure_parsed(classified.get('type', 'unknown'), classified.get('parsed_items', [])),
            'parseable_ratio': parseable_ratio,
            'timestamp': datetime.now(timezone.utc).isoformat(),
        }

        data['sessions'].append(session)

        # Write to file
        out_path = Path(project_path) / "EXTERNAL-INTELLIGENCE.json"
        out_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')

        logger.info("Saved session %s (%s) to %s", session_id, classified.get('type'), out_path.name)

        return {'saved_to': str(out_path), 'session_id': session_id}

    except Exception as e:
        return {'error': f'intake_parser.save_session: {e}'}


# ---------------------------------------------------------------------------
# Scoring helpers
# ---------------------------------------------------------------------------

def _score_signals(text: str, signals: list) -> float:
    """Score how many signal patterns match in the text."""
    if not signals:
        return 0.0
    hits = sum(1 for pattern in signals if pattern.search(text))
    return hits / len(signals)


def _score_tag_signals(text: str) -> float:
    """Score tag-set likelihood based on structural signals."""
    # Tags are comma-separated short phrases
    lines = text.strip().split('\n')
    non_empty_lines = [l.strip() for l in lines if l.strip()]

    if not non_empty_lines:
        return 0.0

    score = 0.0
    checks = 0

    # Check 1: High comma density in first non-empty line or full text
    full_text = " ".join(non_empty_lines)
    comma_count = full_text.count(',')
    word_count = len(full_text.split())
    if word_count > 0:
        comma_ratio = comma_count / word_count
        if comma_ratio > 0.1:
            score += 1
        checks += 1

    # Check 2: 15+ items when split by comma
    items = [i.strip() for i in full_text.split(',') if i.strip()]
    if len(items) >= 15:
        score += 1
    checks += 1

    # Check 3: Short average phrase length (tags are typically 1-4 words)
    if items:
        avg_words = sum(len(i.split()) for i in items) / len(items)
        if avg_words <= 4:
            score += 1
        checks += 1

    # Check 4: Few line breaks relative to commas (tags are usually on 1-3 lines)
    if comma_count > 0 and len(non_empty_lines) <= 5:
        score += 1
    checks += 1

    return score / max(checks, 1)


# ---------------------------------------------------------------------------
# Item parsers
# ---------------------------------------------------------------------------

def _parse_items(text: str, response_type: str) -> list:
    """Parse structured items from text based on detected type."""
    parsers = {
        'keyword_data': _parse_keywords,
        'title_suggestions': _parse_titles,
        'thumbnail_concepts': _parse_thumbnails,
        'description_draft': _parse_description,
        'tag_set': _parse_tags,
    }
    parser = parsers.get(response_type)
    if parser:
        return parser(text)
    return []


def _parse_keywords(text: str) -> list:
    """Extract keyword + metric pairs."""
    keywords = []
    lines = text.split('\n')

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Try patterns: "keyword — volume: X, competition: Y"
        # Or: "keyword (X/100)" or "keyword: volume X"
        # Be flexible — VidIQ output varies

        # Pattern 1: Lines with numbers that look like metrics
        volume_match = re.search(r'(?:volume|vol)[:\s]*[\s]*([\d,]+)', line, re.IGNORECASE)
        comp_match = re.search(r'(?:competition|comp)[:\s]*[\s]*([\d,]+)', line, re.IGNORECASE)
        score_match = re.search(r'(?:score)[:\s]*[\s]*([\d]+(?:/\d+)?)', line, re.IGNORECASE)

        if volume_match or comp_match or score_match:
            # Extract the keyword term (text before the first metric)
            term = re.split(r'[\-\|:]', line)[0].strip()
            # Clean up numbering
            term = re.sub(r'^\d+[\.\)]\s*', '', term).strip()
            term = re.sub(r'\*+', '', term).strip()

            if term and len(term) > 1:
                keywords.append({
                    'term': term,
                    'volume': volume_match.group(1) if volume_match else '',
                    'competition': comp_match.group(1) if comp_match else '',
                    'score': score_match.group(1) if score_match else '',
                })

    return keywords


def _parse_titles(text: str) -> list:
    """Extract title strings."""
    titles = []
    lines = text.split('\n')

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Pattern: numbered list items that look like titles
        # "1. Spain's 300-Year Trap..." or "1) The Treaty That..."
        match = re.match(r'^\d+[\.\)]\s*["\']?(.{20,80}?)["\']?\s*$', line)
        if match:
            title = match.group(1).strip().strip('"\'')
            titles.append({
                'title': title,
                'char_count': len(title),
            })
            continue

        # Pattern: "Title: ..." or "**Title:** ..."
        match = re.match(r'^(?:\*\*)?Title(?:\*\*)?[:\s]+["\']?(.{20,80}?)["\']?\s*$', line, re.IGNORECASE)
        if match:
            title = match.group(1).strip().strip('"\'')
            titles.append({
                'title': title,
                'char_count': len(title),
            })

    return titles


def _parse_thumbnails(text: str) -> list:
    """Extract thumbnail concept descriptions."""
    concepts = []

    # Split by numbered items or bold headers
    sections = re.split(r'(?:^|\n)(?:\d+[\.\)]\s*|\*\*[^*]+\*\*[:\s]*)', text)

    for i, section in enumerate(sections):
        section = section.strip()
        if not section or len(section) < 20:
            continue

        # Check if this section mentions visual/thumbnail concepts
        if re.search(r'\b(?:thumbnail|visual|image|photo|color|composition|background|text\s+overlay)\b', section, re.IGNORECASE):
            # Try to extract a label from the first line
            first_line = section.split('\n')[0].strip()
            label = first_line[:60] if len(first_line) > 60 else first_line
            label = re.sub(r'[*_#]', '', label).strip()

            concepts.append({
                'label': label or f'Concept {len(concepts) + 1}',
                'description': section[:500],
            })

    return concepts


def _parse_description(text: str) -> list:
    """Extract description as a single prose item."""
    word_count = len(text.split())
    return [{
        'text': text.strip(),
        'word_count': word_count,
    }]


def _parse_tags(text: str) -> list:
    """Extract comma-separated tags."""
    # Join all lines and split by comma
    full_text = " ".join(text.strip().split('\n'))
    items = [t.strip().strip('"\'') for t in full_text.split(',') if t.strip()]

    # Filter out items that are too long to be tags
    tags = []
    for item in items:
        clean = re.sub(r'^[\d\.\)\-\*]+\s*', '', item).strip()
        if clean and len(clean) <= 60:
            tags.append({'tag': clean})

    return tags


# ---------------------------------------------------------------------------
# Preview helpers
# ---------------------------------------------------------------------------

def _build_preview(response_type: str, parsed_items: list) -> str:
    """Build a short preview string for user confirmation."""
    count = len(parsed_items)

    if response_type == 'keyword_data':
        if parsed_items:
            first = parsed_items[0]
            vol = f", {first['volume']} vol" if first.get('volume') else ""
            comp = f", {first['competition']} comp" if first.get('competition') else ""
            return f"{count} keywords detected. First: '{first['term']}{vol}{comp}'"
        return "0 keywords detected"

    elif response_type == 'title_suggestions':
        if parsed_items:
            first = parsed_items[0]['title']
            return f"{count} titles detected. First: '{first[:50]}'"
        return "0 titles detected"

    elif response_type == 'thumbnail_concepts':
        if parsed_items:
            first = parsed_items[0]['label']
            return f"{count} concepts detected. First: '{first[:50]}'"
        return "0 concepts detected"

    elif response_type == 'description_draft':
        if parsed_items:
            wc = parsed_items[0]['word_count']
            return f"Description draft ({wc} words)"
        return "Empty description"

    elif response_type == 'tag_set':
        if parsed_items:
            first_three = [t['tag'] for t in parsed_items[:3]]
            return f"{count} tags detected. First 3: '{', '.join(first_three)}'"
        return "0 tags detected"

    return f"{count} items detected"


# ---------------------------------------------------------------------------
# JSON persistence helpers
# ---------------------------------------------------------------------------

def _empty_scaffold(project_path: str) -> dict:
    """Create empty EXTERNAL-INTELLIGENCE.json scaffold."""
    project_name = Path(project_path).name
    return {
        'project': project_name,
        'created': datetime.now(timezone.utc).isoformat(),
        'sessions': [],
    }


def _structure_parsed(response_type: str, parsed_items: list) -> dict:
    """Structure parsed items under appropriate key for JSON storage."""
    key_map = {
        'keyword_data': 'keywords',
        'title_suggestions': 'titles',
        'thumbnail_concepts': 'concepts',
        'description_draft': 'description',
        'tag_set': 'tags',
    }
    key = key_map.get(response_type, 'items')
    return {key: parsed_items}


def _estimate_total_items(raw_text: str, response_type: str) -> int:
    """Estimate total items in raw text for parseable_ratio calculation."""
    lines = [l.strip() for l in raw_text.split('\n') if l.strip()]

    if response_type == 'keyword_data':
        # Count lines with numbers (likely keyword rows)
        return max(sum(1 for l in lines if re.search(r'\d', l)), 1)

    elif response_type == 'title_suggestions':
        # Count numbered items
        return max(sum(1 for l in lines if re.match(r'^\d+[\.\)]', l)), 1)

    elif response_type == 'thumbnail_concepts':
        # Count concept sections (numbered or bold headers)
        return max(sum(1 for l in lines if re.match(r'^(?:\d+[\.\)]|\*\*)', l)), 1)

    elif response_type == 'description_draft':
        return 1  # Always 1 description

    elif response_type == 'tag_set':
        # Count comma-separated items
        full = " ".join(lines)
        return max(len([t for t in full.split(',') if t.strip()]), 1)

    return max(len(lines), 1)
