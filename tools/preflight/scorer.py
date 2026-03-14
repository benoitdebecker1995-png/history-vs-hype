"""
Pre-Flight Scorer — Core scoring engine.

Reads a project folder, runs 4 scoring gates (topic, script, title/metadata,
duration/format), and produces a composite score with actionable flags.

Every gate degrades gracefully: missing dependencies or data yield a neutral
score (50) with a note, never an exception.
"""

import re
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

WEIGHTS = {
    'topic': 0.20,
    'script': 0.25,
    'title': 0.25,
    'thumbnail': 0.15,
    'duration': 0.15,
}

WPM = 150  # words per minute for duration estimation

# Publishing day performance scores (source: channel analytics March 2026, n=40)
# Monday avg 9,689 views, Friday avg 54 views — update when data changes
DAY_SCORES = {
    'monday': 100, 'tuesday': 75, 'sunday': 70,
    'wednesday': 60, 'thursday': 55, 'saturday': 45, 'friday': 20,
}

# Evidence markers recognised in script text
EVIDENCE_RE = re.compile(
    r'\[B-ROLL[:\]]|\[MAP[:\]]|\[DOCUMENT|\[PRIMARY SOURCE|\[TEXT ON SCREEN'
    r'|page \d+|pp?\.\s*\d+|"[^"]{20,}"',
    re.IGNORECASE,
)

PULL_QUESTION_RE = re.compile(r'[^.!?]*\?\s*$', re.MULTILINE)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _read_file(path: Path) -> Optional[str]:
    """Read a file, return None if missing."""
    if not path.exists():
        return None
    try:
        return path.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        return path.read_text(encoding='cp1252')


def _find_script(project: Path) -> Optional[str]:
    """Return script text from the first existing script file."""
    for name in ('FINAL-SCRIPT.md', '02-SCRIPT-DRAFT.md', 'SCRIPT.md'):
        text = _read_file(project / name)
        if text:
            return text
    return None


def _find_metadata(project: Path) -> Optional[str]:
    """Return metadata text, searching multiple naming patterns."""
    # Try exact name first, then glob for variants like 06-YOUTUBE-METADATA.md
    text = _read_file(project / 'YOUTUBE-METADATA.md')
    if text:
        return text
    for f in sorted(project.glob('*YOUTUBE-METADATA*')):
        if f.suffix == '.md':
            return _read_file(f)
    for f in sorted(project.glob('*youtube-metadata*')):
        if f.suffix == '.md':
            return _read_file(f)
    return None


def _extract_titles(metadata: str) -> List[str]:
    """Pull title variants from YOUTUBE-METADATA.md.

    Handles two common formats:
    1. Code blocks:  ```\\nActual Title Text (55 chars)\\n```
    2. Bold inline:  1. **Actual Title Text** — description
    """
    titles = []
    in_title_section = False
    in_code_block = False
    lines = metadata.splitlines()

    for i, line in enumerate(lines):
        lower = line.strip().lower()
        if lower.startswith('## title') or lower.startswith('# title'):
            in_title_section = True
            continue
        if not in_title_section:
            continue
        # Stop at next major section (but not sub-headings like **Title 3:**)
        if re.match(r'^##\s+(?!title)', line, re.I):
            break

        stripped = line.strip()

        # Code-block titles: line inside ``` fences
        if stripped == '```':
            in_code_block = not in_code_block
            continue
        if in_code_block and stripped:
            # Strip trailing char-count annotations like "(55 chars)"
            clean = re.sub(r'\s*\(\d+\s*chars?\s*\)\s*$', '', stripped).strip()
            if clean and len(clean) > 10:
                titles.append(clean)
            continue

        # Bold inline: "1. **Title Text Here** — description"
        bold_match = re.match(
            r'^\d+\.\s*\*\*(.+?)\*\*',
            stripped,
        )
        if bold_match:
            candidate = bold_match.group(1).strip()
            # Filter out labels that aren't real titles
            if len(candidate) > 15 and not candidate.lower().startswith(('title ', 'option ')):
                # Strip trailing annotations like "— 58 chars ✅"
                candidate = re.sub(r'\s*[—–-]\s*\d+\s*chars.*$', '', candidate).strip()
                titles.append(candidate)

        # Blockquote titles: "> Title Text Here"
        if stripped.startswith('>'):
            candidate = stripped.lstrip('> ').strip()
            if len(candidate) > 15 and not candidate.lower().startswith(('title ', 'option ', '**')):
                titles.append(candidate)

    return titles


def _letter_grade(score: float) -> str:
    if score >= 90:
        return 'A'
    if score >= 80:
        return 'B+'
    if score >= 70:
        return 'B'
    if score >= 60:
        return 'C'
    if score >= 50:
        return 'D'
    return 'F'


def _verdict(score: float) -> str:
    if score >= 70:
        return 'READY'
    if score >= 50:
        return 'REVIEW'
    return 'NOT READY'


# ---------------------------------------------------------------------------
# Gate 1: Topic Score
# ---------------------------------------------------------------------------

def _score_topic(titles: List[str]) -> Dict[str, Any]:
    """Score topic using topic_scorer on all title variants, keep the best.

    Falls back to classify_topic_type baseline if topic_scorer is unavailable.
    """
    result: Dict[str, Any] = {'score': 50, 'topic_type': 'general', 'notes': []}

    # Try topic_scorer on every title variant, keep highest score
    try:
        from tools.intel.topic_scorer import score_topic
        best_score = -1
        for title in titles:
            ts = score_topic(title)
            if 'error' not in ts and ts.get('total_score', 0) > best_score:
                best_score = ts['total_score']
                result['score'] = min(100, max(0, round(best_score)))
                result['topic_type'] = ts.get('primary_cluster', 'general')
                result['grade'] = ts.get('grade', '')
                result['scored_title'] = title
                recs = ts.get('recommendations', {})
                if recs.get('comparable_outliers'):
                    result['comparable'] = recs['comparable_outliers'][:3]
        if best_score >= 0:
            return result
        result['notes'].append('topic_scorer returned errors for all titles')
    except Exception as e:
        result['notes'].append(f"topic_scorer unavailable: {e}")

    # Fallback: classify topic type and assign baseline score
    try:
        from tools.youtube_analytics.performance import classify_topic_type
        # Try all titles, pick best-scoring type
        best_baseline = 0
        for title in titles:
            topic_type = classify_topic_type(title)
            baselines = {
                'territorial': 70, 'colonial': 65, 'legal': 65,
                'ideological': 60, 'medieval': 55, 'politician': 55,
                'archaeological': 50, 'general': 45,
            }
            score = baselines.get(topic_type, 50)
            if score > best_baseline:
                best_baseline = score
                result['topic_type'] = topic_type
                result['score'] = score
        result['notes'].append('scored via topic-type baseline (no intel.db)')
    except Exception as e:
        result['notes'].append(f"classify_topic_type unavailable: {e}")

    return result


# ---------------------------------------------------------------------------
# Gate 2: Script Score
# ---------------------------------------------------------------------------

def _score_script(script_text: str) -> Dict[str, Any]:
    """Score script quality using checkers + evidence density."""
    result: Dict[str, Any] = {
        'score': 50,
        'issues': [],
        'pacing_verdict': 'SKIPPED',
        'evidence_density': 0.0,
        'notes': [],
    }

    # Truncate appendix sections; keep markers for evidence counting
    script_with_markers = _truncate_non_spoken(script_text)
    # Fully stripped version for word count / pacing
    script_text = _strip_non_spoken(script_text)

    words = script_text.split()
    word_count = len(words)
    if word_count < 50:
        result['notes'].append('Script too short to score')
        return result

    sub_scores: List[float] = []

    # --- Pacing ---
    try:
        from tools.script_checkers.config import Config
        from tools.script_checkers.checkers.pacing import PacingChecker
        cfg = Config()
        pc = PacingChecker(cfg)
        pacing = pc.check(script_text)
        stats = pacing.get('stats', {})
        avg = stats.get('average_score', 50)
        sub_scores.append(avg)
        result['pacing_verdict'] = stats.get('verdict', 'SKIPPED')
        if pacing.get('issues'):
            for iss in pacing['issues'][:3]:
                result['issues'].append(
                    f"Pacing: {iss.get('section', '?')} scored {iss.get('score', '?')}"
                )
    except Exception as e:
        result['notes'].append(f"PacingChecker: {e}")
        sub_scores.append(50)

    # --- Stumble ---
    try:
        from tools.script_checkers.config import Config
        from tools.script_checkers.checkers.stumble import StumbleChecker
        cfg = Config()
        sc = StumbleChecker(cfg)
        stumble = sc.check(script_text)
        stats = stumble.get('stats', {})
        total = stats.get('total_sentences', 1)
        flagged = stats.get('flagged_sentences', 0)
        stumble_score = max(0, 100 - (flagged / max(total, 1)) * 200)
        sub_scores.append(stumble_score)
        high_sev = [i for i in stumble.get('issues', []) if i.get('severity') == 'high']
        if high_sev:
            result['issues'].append(
                f"Stumble: {len(high_sev)} high-severity sentences"
            )
    except Exception as e:
        result['notes'].append(f"StumbleChecker: {e}")
        sub_scores.append(50)

    # --- Scaffolding ---
    try:
        from tools.script_checkers.config import Config
        from tools.script_checkers.checkers.scaffolding import ScaffoldingChecker
        cfg = Config()
        sc = ScaffoldingChecker(cfg)
        scaff = sc.check(script_text)
        sev = scaff.get('stats', {}).get('severity', 'ok')
        scaff_score = {'ok': 100, 'warning': 65, 'error': 30}.get(sev, 50)
        sub_scores.append(scaff_score)
        if sev != 'ok':
            result['issues'].append(
                f"Scaffolding: {sev} — {scaff['stats'].get('total_scaffolding', 0)} filler phrases"
            )
    except Exception as e:
        result['notes'].append(f"ScaffoldingChecker: {e}")
        sub_scores.append(50)

    # --- Evidence density (use marker-intact text for counting) ---
    evidence_hits = EVIDENCE_RE.findall(script_with_markers)
    result['evidence_density'] = round(len(evidence_hits) / max(word_count / 100, 1), 2)
    evidence_score = min(100, result['evidence_density'] * 30)  # ~3.3 per 100w = 100
    sub_scores.append(evidence_score)
    if result['evidence_density'] < 1.0:
        result['issues'].append(
            f"Low evidence density: {result['evidence_density']} markers per 100 words"
        )

    # --- Pull question in hook ---
    # NOTE: Channel data shows declarative hooks outperform question hooks
    # (declarative 3.8% CTR vs question 2.4%). A pull question is a bonus,
    # not a requirement. No penalty for declarative openings.
    hook_cutoff = max(1, int(word_count * 0.2))
    hook_text = ' '.join(words[:hook_cutoff])
    has_pull = bool(PULL_QUESTION_RE.search(hook_text))
    if has_pull:
        sub_scores.append(90)
        result['notes'].append('Pull question found in hook (bonus)')
    else:
        sub_scores.append(75)  # neutral — declarative is the channel's strong suit

    # --- Opening hook pattern (data-backed, March 2026) ---
    # High-retention (35%+) openings start with specific number or shocking verb
    # Low-retention (<25%) openings start with abstract context-setting
    first_50_words = ' '.join(words[:50]).lower()
    hook_score = 70  # default
    hook_notes = []

    # Positive: specific numbers in first 50 words
    if re.search(r'\b\d+\b', first_50_words):
        hook_score += 15
        hook_notes.append('Specific number in opening (good)')

    # Positive: shocking/active verbs
    shock_verbs = ['divided', 'split', 'stripped', 'destroyed', 'invaded',
                   'erased', 'killed', 'conquered', 'betrayed', 'weaponized',
                   'funded', 'signed away', 'blew', 'collapsed']
    if any(v in first_50_words for v in shock_verbs):
        hook_score += 15
        hook_notes.append('Shocking verb in opening (good)')

    # Negative: starts with abstract context
    abstract_starts = ['to understand', 'the concept', 'in order to', 'throughout history',
                       'for centuries', 'many people believe', 'it is often said']
    if any(first_50_words.startswith(a) for a in abstract_starts):
        hook_score -= 25
        result['issues'].append('Opening starts with abstract context (correlates with <25% retention)')

    # Negative: anecdote that delays the topic
    if re.search(r'^(in \d{4}|on [a-z]+ \d)', first_50_words) and not re.search(r'\b\d+\s+(countries|groups|people|million)', first_50_words):
        hook_score -= 10
        hook_notes.append('Opening may delay topic with date-first context')

    sub_scores.append(min(100, max(0, hook_score)))
    result['notes'].extend(hook_notes)

    result['score'] = round(sum(sub_scores) / len(sub_scores)) if sub_scores else 50
    return result


# ---------------------------------------------------------------------------
# Gate 3: Title / Metadata Score
# ---------------------------------------------------------------------------

def _score_title_metadata(metadata: str, titles: List[str], topic_type: str) -> Dict[str, Any]:
    """Score title variants and metadata completeness.

    Uses data-backed CTR patterns from 40-video analysis (March 2026):
      versus (5.5%) > declarative (3.8%) > how (3.8%) >> colon (2.6%)
      >> question (2.0%) >> the_x_that (1.2%)

    Title killers: year (-45.6%), numbers (-42.0%), question (-36.3%),
    colon (-28.1% CTR but +16.9% retention).
    """
    result: Dict[str, Any] = {
        'score': 50,
        'best_title': '',
        'predicted_ctr': '',
        'formulas': [],
        'title_pattern': '',
        'issues': [],
        'notes': [],
    }

    if not titles:
        result['issues'].append('No title variants found in YOUTUBE-METADATA.md')
        result['score'] = 20
        return result

    sub_scores: List[float] = []

    # --- Data-backed title pattern scoring (March 2026, n=40) ---
    def _classify_title_pattern(title: str) -> tuple:
        """Classify title and return (pattern, base_score, issues)."""
        t = title.lower()
        issues = []

        # Detect pattern
        pattern = 'declarative'
        if ' vs ' in t or ' vs. ' in t:
            pattern = 'versus'
        elif t.startswith('the ') and ' that ' in t:
            pattern = 'the_x_that'
        elif t.startswith('how '):
            pattern = 'how'
        elif t.startswith('why '):
            pattern = 'why'
        elif '?' in title:
            pattern = 'question'
        elif ':' in title:
            pattern = 'colon'

        # Pattern base scores (from own-channel CTR data)
        pattern_scores = {
            'versus': 95,       # 5.5% avg CTR
            'declarative': 75,  # 3.8% avg CTR
            'how': 75,          # 3.8% avg CTR
            'why': 55,          # 2.6% avg CTR
            'colon': 50,        # 2.6% avg CTR (but +17% retention)
            'question': 40,     # 2.0% avg CTR
            'the_x_that': 20,   # 1.2% avg CTR — NEVER USE
        }
        base = pattern_scores.get(pattern, 60)

        # Title killers (penalty flags)
        if re.search(r'\b(1[0-9]{3}|20[0-2][0-9])\b', title):
            issues.append(f'YEAR in title (-45.6% CTR): consider removing')
            base = max(10, base - 30)
        if re.search(r'\b\d+\b', title) and not re.search(r'\b(1[0-9]{3}|20[0-2][0-9])\b', title):
            # Numbers that aren't years — mild penalty
            pass  # numbers in "229 ethnic groups" can work for evidence-promise
        if '?' in title:
            issues.append('Question mark in title (-36.3% CTR)')

        if pattern == 'the_x_that':
            issues.append('"The [X] That [Verb]" pattern = 1.2% avg CTR — NEVER USE')

        return pattern, base, issues

    # Score all titles using title_scorer (DB-enriched when keywords.db available)
    db_path = None
    try:
        from tools.discovery.database import KeywordDB
        _db = KeywordDB()
        db_path = _db.db_path
        _db.close()
    except Exception:
        pass

    best_score = -1
    best_title = titles[0]
    best_pattern = 'unknown'

    # Try DB-enriched scoring via title_scorer first
    try:
        from tools.title_scorer import score_title as _score_title
        for t in titles:
            ts_result = _score_title(t, db_path=db_path)
            # Use the score directly from title_scorer (handles hard rejects etc.)
            ts_score = ts_result['score']
            if ts_score > best_score:
                best_score = ts_score
                best_title = t
                best_pattern = ts_result['pattern']
                # Propagate hard reject issues and suggestions
                issues_from_scorer = list(ts_result.get('hard_rejects', []))
                issues_from_scorer += [s for s in ts_result.get('suggestions', [])
                                       if 'Remove' in s or 'Replace' in s or 'Rewrite' in s]
                result['issues'] = issues_from_scorer
        if best_score >= 0:
            sub_scores.append(best_score)
            result['best_title'] = best_title
            result['title_pattern'] = best_pattern
    except Exception as e:
        result['notes'].append(f"title_scorer unavailable: {e} — using internal classifier")
        # Fallback to internal classifier
        for t in titles:
            pattern, score, pattern_issues = _classify_title_pattern(t)
            if score > best_score:
                best_score = score
                best_title = t
                best_pattern = pattern
                result['issues'] = pattern_issues
        sub_scores.append(best_score)
        result['best_title'] = best_title
        result['title_pattern'] = best_pattern

    # --- CTR prediction (TitleIntelligence, if available) ---
    try:
        from tools.youtube_analytics.title_intelligence import TitleIntelligence
        ti = TitleIntelligence()
        best_ctr = 0.0
        for t in titles:
            pred = ti.predict_ctr(t, topic_type=topic_type)
            if 'error' not in pred:
                ctr = pred.get('predicted_ctr', 0)
                if ctr > best_ctr:
                    best_ctr = ctr
        if best_ctr > 0:
            ctr_score = min(100, (best_ctr / 8.0) * 100)
            sub_scores.append(ctr_score)
            result['predicted_ctr'] = f"{best_ctr:.1f}%"
    except Exception as e:
        result['notes'].append(f"TitleIntelligence: {e}")

    # --- Title length ---
    tlen = len(best_title)
    if 40 <= tlen <= 65:
        sub_scores.append(100)
    elif 30 <= tlen < 40 or 65 < tlen <= 75:
        sub_scores.append(70)
        result['issues'].append(f"Title length {tlen} chars (optimal: 40-65)")
    else:
        sub_scores.append(40)
        result['issues'].append(f"Title length {tlen} chars (optimal: 40-65)")

    # --- Formula detection ---
    try:
        from tools.intel.topic_vocabulary import detect_formulas
        formulas = detect_formulas(best_title)
        result['formulas'] = formulas
    except Exception as e:
        result['notes'].append(f"detect_formulas: {e}")

    # --- Description length ---
    # Match from ## DESCRIPTION until the next H2 (## not ###) or end of file
    desc_match = re.search(r'^##\s*Description\b(.*?)(?=\n## (?!#)|\Z)', metadata, re.S | re.I | re.M)
    if desc_match:
        desc_text = desc_match.group(1)
        # Strip code fences so content inside ``` blocks is counted
        desc_text = re.sub(r'```\w*', '', desc_text)
        # Strip markdown headings (###) from word count
        desc_text = re.sub(r'^#{1,6}\s+.*$', '', desc_text, flags=re.M)
        desc_words = len(desc_text.split())
        if desc_words >= 200:
            sub_scores.append(100)
        elif desc_words >= 100:
            sub_scores.append(70)
            result['issues'].append(f"Description only {desc_words} words (target: 200+)")
        else:
            sub_scores.append(40)
            result['issues'].append(f"Description only {desc_words} words (target: 200+)")
    else:
        result['issues'].append('No description section found')
        sub_scores.append(30)

    # --- Publishing day check ---
    day_match = re.search(r'(?:Day|day)[:\s]*(\w+)', metadata)
    if day_match:
        day = day_match.group(1).strip().lower()
        day_score = DAY_SCORES.get(day, 55)
        sub_scores.append(day_score)
        if day == 'friday':
            result['issues'].append('Publishing Friday (avg 54 views) — move to Monday (avg 9,689)')
        elif day in ('saturday', 'wednesday', 'thursday'):
            result['notes'].append(f'Publishing {day.title()} — Monday has 23x more avg views')
    else:
        result['notes'].append('No publishing day specified in metadata')

    # --- Tag count ---
    # Only count tags inside code fences under ## Tags (ignore strategy tables)
    tag_match = re.search(r'^##\s*Tags\b(.*?)(?=\n## (?!#)|\Z)', metadata, re.S | re.I | re.M)
    if tag_match:
        tag_section = tag_match.group(1)
        code_block = re.search(r'```\w*\n(.*?)```', tag_section, re.S)
        tag_text = code_block.group(1) if code_block else tag_section
        tags = [t.strip() for t in tag_text.split(',') if t.strip()]
        tag_count = len(tags)
        if 15 <= tag_count <= 30:
            sub_scores.append(100)
        elif 10 <= tag_count < 15 or 30 < tag_count <= 40:
            sub_scores.append(70)
            result['issues'].append(f"Tag count {tag_count} (optimal: 15-30)")
        else:
            sub_scores.append(40)
            result['issues'].append(f"Tag count {tag_count} (optimal: 15-30)")
    else:
        result['issues'].append('No tags section found')
        sub_scores.append(30)

    result['score'] = round(sum(sub_scores) / len(sub_scores)) if sub_scores else 50
    return result


# ---------------------------------------------------------------------------
# Gate 4: Duration / Format Score
# ---------------------------------------------------------------------------

def _truncate_non_spoken(text: str) -> str:
    """Cut non-spoken sections (verification tables, asset checklists, etc.).

    Returns the script body with appendix sections removed but markers intact
    (needed for evidence counting).
    """
    for marker in (
        '## VISUAL ASSET CHECKLIST', '## VERIFICATION NOTES', '## WORD COUNT',
        '## SHORTS EXTRACTION', '## SOURCE', '## APPENDIX',
    ):
        idx = text.find(marker)
        if idx != -1:
            text = text[:idx]
    return text


def _strip_non_spoken(text: str) -> str:
    """Remove non-spoken content for word count / pacing.

    Truncates appendix sections, then strips stage directions, headings,
    and metadata lines so only spoken words remain.
    """
    text = _truncate_non_spoken(text)
    # Strip markdown stage directions and B-roll markers for word count
    text = re.sub(r'\[.*?\]', '', text)
    # Strip markdown headings (##) and horizontal rules (---)
    text = re.sub(r'^#{1,6}\s+.*$', '', text, flags=re.MULTILINE)
    text = re.sub(r'^---+\s*$', '', text, flags=re.MULTILINE)
    # Strip bold/italic metadata lines at top (e.g. **Based on:** ...)
    text = re.sub(r'^\*\*.*?\*\*.*$', '', text, flags=re.MULTILINE)
    return text


def _score_duration(script_text: str) -> Dict[str, Any]:
    """Score duration and B-roll density."""
    spoken_text = _strip_non_spoken(script_text)
    words = spoken_text.split()
    word_count = len(words)
    est_minutes = round(word_count / WPM, 1)

    # Duration scoring — generous for long videos (channel has no length cap;
    # Kraut runs 30-45 min successfully). Penalise only very short videos.
    if 8 <= est_minutes <= 13:
        dur_score = 100
    elif 13 < est_minutes <= 20:
        dur_score = 85
    elif 20 < est_minutes <= 30:
        dur_score = 70
    elif 7 <= est_minutes < 8 or est_minutes > 30:
        dur_score = 60
    elif 4 <= est_minutes < 7:
        dur_score = 50
    else:
        dur_score = 35

    # B-roll marker density
    broll_markers = len(EVIDENCE_RE.findall(script_text))
    # Estimate sections by heading count
    section_count = max(1, len(re.findall(r'^##\s', script_text, re.MULTILINE)))
    broll_per_section = broll_markers / section_count
    broll_ratio = round(min(1.0, broll_per_section / 4), 2)  # 4+ per section = 1.0

    broll_score = min(100, broll_ratio * 100)

    composite = round(dur_score * 0.6 + broll_score * 0.4)

    issues = []
    if est_minutes < 8:
        issues.append(f"Short duration (~{est_minutes} min) — under 8 min sweet spot")
    elif est_minutes > 20:
        issues.append(f"Long duration (~{est_minutes} min) — ensure pacing stays tight")
    if broll_ratio < 0.25:
        issues.append(f"Low B-roll density ({broll_ratio:.0%}) — add visual markers")

    return {
        'score': composite,
        'estimated_minutes': est_minutes,
        'word_count': word_count,
        'broll_ratio': broll_ratio,
        'issues': issues,
    }


# ---------------------------------------------------------------------------
# View range prediction
# ---------------------------------------------------------------------------

def _predict_views(topic_type: str, composite: float) -> Dict[str, Any]:
    """Rough view-range prediction based on topic type + composite score."""
    # Baseline medians from channel performance data
    baselines = {
        'territorial': 2000, 'colonial': 1200, 'legal': 1000,
        'ideological': 800, 'medieval': 600, 'politician': 900,
        'archaeological': 500, 'general': 400,
    }
    base = baselines.get(topic_type, 500)

    # Scale by composite: 80+ gets 1.2x, 50 gets 0.6x, linear between
    multiplier = 0.6 + (composite - 50) * (0.6 / 50) if composite <= 80 else 1.2
    multiplier = max(0.3, min(1.5, multiplier))

    mid = round(base * multiplier)
    return {
        'views_low': round(mid * 0.5),
        'views_high': round(mid * 1.5),
        'based_on': f"{topic_type} baseline + {_letter_grade(composite)}-grade composite",
    }


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def run_preflight(project_path: str) -> Dict[str, Any]:
    """
    Run full pre-flight scoring on a project folder.

    Args:
        project_path: Path to video project folder (e.g.
            "video-projects/_IN_PRODUCTION/40-berlin-conference-1884-2026")

    Returns:
        Scorecard dict with composite_score, grade, gates, verdict, flags,
        and predicted_range.
    """
    project = Path(project_path)
    if not project.is_dir():
        return {'error': f"Project folder not found: {project_path}"}

    script_text = _find_script(project)
    metadata_text = _find_metadata(project)

    flags: List[str] = []
    notes: List[str] = []

    # --- Extract titles from metadata ---
    titles: List[str] = []
    if metadata_text:
        titles = _extract_titles(metadata_text)

    # Build title list for topic scoring (folder name as fallback)
    topic_titles = titles if titles else [project.name.replace('-', ' ')]

    # --- Gate 1: Topic ---
    topic_result = _score_topic(topic_titles)
    topic_type = topic_result.get('topic_type', 'general')

    # --- Gate 2: Script ---
    if script_text:
        script_result = _score_script(script_text)
    else:
        script_result = {
            'score': 0, 'issues': ['No script file found'], 'notes': [],
            'pacing_verdict': 'SKIPPED', 'evidence_density': 0,
        }
        flags.append('No script file (02-SCRIPT-DRAFT.md or FINAL-SCRIPT.md)')

    # --- Gate 3: Title / Metadata ---
    if metadata_text:
        title_result = _score_title_metadata(metadata_text, titles, topic_type)
    else:
        title_result = {
            'score': 0, 'best_title': '', 'predicted_ctr': '',
            'formulas': [], 'issues': ['No YOUTUBE-METADATA.md found'], 'notes': [],
        }
        flags.append('No YOUTUBE-METADATA.md')

    # --- Gate 4: Thumbnail ---
    try:
        from tools.preflight.thumbnail_checker import check_project
        thumbnail_result = check_project(str(project))
    except Exception as e:
        thumbnail_result = {
            'score': 50, 'verdict': 'SKIPPED',
            'issues': [f'thumbnail_checker unavailable: {e}'],
            'passes': [],
        }

    # --- Gate 5: Duration / Format ---
    if script_text:
        duration_result = _score_duration(script_text)
    else:
        duration_result = {
            'score': 0, 'estimated_minutes': 0, 'word_count': 0,
            'broll_ratio': 0, 'issues': ['No script to measure'],
        }

    # --- Composite ---
    composite = round(
        topic_result['score'] * WEIGHTS['topic']
        + script_result['score'] * WEIGHTS['script']
        + title_result['score'] * WEIGHTS['title']
        + thumbnail_result['score'] * WEIGHTS['thumbnail']
        + duration_result['score'] * WEIGHTS['duration']
    )

    # Collect all flags from sub-gates
    for gate in (script_result, title_result, thumbnail_result, duration_result):
        flags.extend(gate.get('issues', []))

    # Channel averages (best-effort)
    channel_avg = {}
    try:
        from tools.discovery.database import KeywordDB
        db = KeywordDB()
        perfs = db.get_all_video_performance(limit=50)
        db.close()
        if perfs and not isinstance(perfs, dict):
            views = [p['views'] for p in perfs if p.get('views')]
            if views:
                channel_avg['avg_views'] = round(sum(views) / len(views))
                channel_avg['sample_size'] = len(views)
    except Exception:
        pass

    return {
        'composite_score': composite,
        'grade': _letter_grade(composite),
        'gates': {
            'topic': {
                'score': topic_result['score'],
                'topic_type': topic_type,
                'notes': topic_result.get('notes', []),
            },
            'script': {
                'score': script_result['score'],
                'issues': script_result.get('issues', []),
                'pacing_verdict': script_result.get('pacing_verdict', 'SKIPPED'),
                'evidence_density': script_result.get('evidence_density', 0),
                'notes': script_result.get('notes', []),
            },
            'title': {
                'score': title_result['score'],
                'best_title': title_result.get('best_title', ''),
                'predicted_ctr': title_result.get('predicted_ctr', ''),
                'formulas': title_result.get('formulas', []),
                'issues': title_result.get('issues', []),
                'notes': title_result.get('notes', []),
            },
            'thumbnail': {
                'score': thumbnail_result['score'],
                'verdict': thumbnail_result.get('verdict', 'SKIPPED'),
                'issues': thumbnail_result.get('issues', []),
                'passes': thumbnail_result.get('passes', []),
            },
            'duration': {
                'score': duration_result['score'],
                'estimated_minutes': duration_result.get('estimated_minutes', 0),
                'word_count': duration_result.get('word_count', 0),
                'broll_ratio': duration_result.get('broll_ratio', 0),
                'issues': duration_result.get('issues', []),
            },
        },
        'verdict': _verdict(composite),
        'flags': flags,
        'predicted_range': _predict_views(topic_type, composite),
        'channel_avg': channel_avg,
    }


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    import json
    # Ensure project root is on sys.path so `from tools.xxx` imports work
    _root = Path(__file__).resolve().parent.parent.parent
    if str(_root) not in sys.path:
        sys.path.insert(0, str(_root))
    if len(sys.argv) < 2:
        print("Usage: python -m tools.preflight.scorer <project_path>")
        sys.exit(1)
    result = run_preflight(sys.argv[1])
    print(json.dumps(result, indent=2))
