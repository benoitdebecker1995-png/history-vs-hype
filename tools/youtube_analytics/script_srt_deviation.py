"""
Script-to-SRT Deviation Analysis Tool

Compares written scripts (02-SCRIPT-DRAFT.md / SCRIPT.md) against filmed SRT
transcriptions to find what was cut, added, or modified during filming, then
correlates those deviations with YouTube retention data.

Questions answered:
  - Which script sections get cut in filming? (= expendable content)
  - Which sections are ad-libbed / added? (= natural filmmaker instincts)
  - Do cuts cluster in high or low retention zones?
  - Do ad-libs correlate with retention bumps or drops?
  - What is the average script survival rate?

Data sources:
  - SCRIPT.md / 02-SCRIPT-DRAFT.md in video-projects/_IN_PRODUCTION/
  - *.srt files in the same project folders
  - _retention_cache/*.json (100-point retention curves)
  - analytics.db (video metadata, SRT-to-video mapping)

Usage:
    python -m tools.youtube_analytics.script_srt_deviation --report
    python -m tools.youtube_analytics.script_srt_deviation --cached
    python -m tools.youtube_analytics.script_srt_deviation --video PROJECT_SLUG
    python -m tools.youtube_analytics.script_srt_deviation --verbose

Output:
    channel-data/patterns/SCRIPT-SRT-DEVIATION-ANALYSIS.md
"""

import argparse
import json
import re
import sqlite3
import sys
from collections import defaultdict
from datetime import datetime, timezone
from difflib import SequenceMatcher
from pathlib import Path
from statistics import mean, median
from typing import Optional

from tools.logging_config import get_logger, setup_logging

logger = get_logger(__name__)

# Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
PROJECTS_DIR = PROJECT_ROOT / "video-projects" / "_IN_PRODUCTION"
DB_PATH = PROJECT_ROOT / "tools" / "youtube_analytics" / "analytics.db"
CACHE_DIR = PROJECT_ROOT / "tools" / "youtube_analytics" / "_retention_cache"
REPORT_PATH = PROJECT_ROOT / "channel-data" / "patterns" / "SCRIPT-SRT-DEVIATION-ANALYSIS.md"
DEVIATION_JSON = Path(__file__).parent / "_script_srt_deviations.json"

# Skip non-English / non-primary SRT patterns
SRT_SKIP_PATTERNS = [
    r"-es\.srt$",
    r"-farsi\.srt$",
    r"_fr\.srt$",
    r"_pt\.srt$",
    r"SPANISH",
    r"BACKUP",
    r"_CORRECTED",
]

# Script markdown elements to strip (not spoken aloud)
SCRIPT_STRIP_PATTERNS = [
    r"^\[.*?\]\s*$",             # Full-line B-roll/visual cues
    r"\[B-ROLL:.*?\]",           # Inline B-roll cues
    r"\[VISUAL:.*?\]",           # Visual cues
    r"\[TRANSITION:.*?\]",       # Transition cues
    r"\[Beat\]",                 # Beat markers
    r"\[CTA.*?\]",               # CTA markers
    r"\{.*?\}",                  # Retention triggers
    r"^>.*$",                    # Block quotes (on-screen text, not spoken)
    r"^//.*$",                   # Production notes
    r"^\*\*.*\*\*:?$",          # Bold-only lines (section labels)
    r"^---+$",                   # Horizontal rules
    r"^#+\s.*$",                 # Markdown headers
    r"^\|.*\|$",                 # Table rows
    r"^\*[^*].*\*$",             # Italic notes
    r"^\(.*\)\s*$",              # Parenthesized stage directions: (BACK TO CAMERA), (SHOW: ...)
]


# =========================================================================
# SCRIPT PARSING
# =========================================================================

def parse_script(script_path: Path) -> list[str]:
    """
    Parse a script markdown file into a list of spoken sentences.

    Strips all markdown formatting, B-roll cues, production notes,
    and non-spoken elements. Returns clean sentences as they would
    be read from a teleprompter.
    """
    text = script_path.read_text(encoding='utf-8')
    lines = text.split('\n')

    # Skip metadata block at top (everything before first ---)
    content_start = 0
    found_first_rule = False
    for i, line in enumerate(lines):
        if line.strip() == '---':
            if found_first_rule:
                content_start = i + 1
                break
            found_first_rule = True

    lines = lines[content_start:]

    # Strip non-spoken elements
    compiled = [re.compile(p, re.MULTILINE) for p in SCRIPT_STRIP_PATTERNS]
    cleaned = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue

        # Skip lines matching any strip pattern
        skip = False
        for pattern in compiled:
            if pattern.match(stripped):
                skip = True
                break
        if skip:
            continue

        # Remove inline markdown formatting
        cleaned_line = stripped
        cleaned_line = re.sub(r'\*\*(.*?)\*\*', r'\1', cleaned_line)  # Bold
        cleaned_line = re.sub(r'\*(.*?)\*', r'\1', cleaned_line)       # Italic
        cleaned_line = re.sub(r'\[B-ROLL:.*?\]', '', cleaned_line)     # Inline B-roll
        cleaned_line = re.sub(r'\[VISUAL:.*?\]', '', cleaned_line)     # Inline visual
        cleaned_line = re.sub(r'\[TRANSITION:.*?\]', '', cleaned_line)
        cleaned_line = re.sub(r'\{.*?\}', '', cleaned_line)            # Inline triggers
        cleaned_line = cleaned_line.strip()

        if cleaned_line and len(cleaned_line) > 5:
            cleaned.append(cleaned_line)

    # Split into sentences
    sentences = []
    for line in cleaned:
        # Split on sentence boundaries
        parts = re.split(r'(?<=[.!?])\s+', line)
        for part in parts:
            part = part.strip()
            if part and len(part) > 10:
                sentences.append(part)

    logger.debug("Parsed %d sentences from %s", len(sentences), script_path.name)
    return sentences


# =========================================================================
# SRT PARSING
# =========================================================================

def parse_srt(srt_path: Path) -> list[dict]:
    """Parse an SRT into this module's {text,start_sec,end_sec} shape.

    Thin adapter over the canonical parser (tools.subtitles, ADR-0010).
    """
    from tools.subtitles import parse as _parse
    subtitles = [
        {"text": c.text, "start_sec": c.start, "end_sec": c.end}
        for c in _parse(srt_path)
    ]
    logger.debug("Parsed %d subtitle blocks from %s", len(subtitles), srt_path.name)
    return subtitles


def srt_to_sentences(subtitles: list[dict]) -> list[dict]:
    """
    Join subtitle blocks into sentences based on punctuation.

    Returns list of dicts: {'text': str, 'start_sec': float, 'end_sec': float}
    """
    if not subtitles:
        return []

    sentences = []
    current_text = ''
    current_start = subtitles[0]['start_sec']

    for sub in subtitles:
        if current_text:
            current_text += ' ' + sub['text']
        else:
            current_text = sub['text']
            current_start = sub['start_sec']

        # Check if this subtitle ends a sentence
        if re.search(r'[.!?]["\']*\s*$', sub['text']):
            sentences.append({
                'text': current_text.strip(),
                'start_sec': current_start,
                'end_sec': sub['end_sec'],
            })
            current_text = ''

    # Don't lose trailing text
    if current_text.strip():
        sentences.append({
            'text': current_text.strip(),
            'start_sec': current_start,
            'end_sec': subtitles[-1]['end_sec'],
        })

    return sentences


# =========================================================================
# TEXT COMPARISON
# =========================================================================

def normalize_for_comparison(text: str) -> str:
    """Normalize text for fuzzy comparison."""
    text = text.lower()
    text = re.sub(r"[''\".,!?:;\-\u2014\u2013()]", ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def find_best_match(needle: str, haystack: list[str], threshold: float = 0.45) -> tuple[int, float]:
    """
    Find the best matching sentence in haystack for needle.

    Returns (index, similarity_score). Returns (-1, 0.0) if no match above threshold.
    """
    needle_norm = normalize_for_comparison(needle)
    if not needle_norm:
        return -1, 0.0

    best_idx = -1
    best_score = 0.0

    for i, candidate in enumerate(haystack):
        cand_norm = normalize_for_comparison(candidate)
        if not cand_norm:
            continue

        # Quick token overlap pre-filter for speed
        needle_tokens = set(needle_norm.split())
        cand_tokens = set(cand_norm.split())
        if needle_tokens and cand_tokens:
            token_overlap = len(needle_tokens & cand_tokens) / max(len(needle_tokens), len(cand_tokens))
            if token_overlap < 0.2:
                continue

        score = SequenceMatcher(None, needle_norm, cand_norm).ratio()
        if score > best_score:
            best_score = score
            best_idx = i

    if best_score >= threshold:
        return best_idx, best_score
    return -1, 0.0


def classify_deviations(
    script_sentences: list[str],
    srt_sentences: list[dict],
) -> dict:
    """
    Compare script sentences against SRT sentences and classify deviations.

    Returns dict with:
      - kept: list of {script, srt, similarity, srt_position}
      - cut: list of {script, index}
      - added: list of {srt, srt_position}
      - modified: list of {script, srt, similarity, srt_position}
      - stats: {total_script, total_srt, kept_count, cut_count, added_count, modified_count}
    """
    srt_texts = [s['text'] for s in srt_sentences]
    srt_matched = set()

    kept = []
    cut = []
    modified = []

    # For each script sentence, find best SRT match
    for i, script_sent in enumerate(script_sentences):
        match_idx, score = find_best_match(script_sent, srt_texts)

        if match_idx >= 0 and match_idx not in srt_matched:
            srt_matched.add(match_idx)
            entry = {
                'script': script_sent,
                'srt': srt_texts[match_idx],
                'similarity': score,
                'srt_start': srt_sentences[match_idx]['start_sec'],
                'srt_end': srt_sentences[match_idx]['end_sec'],
                'script_index': i,
                'srt_index': match_idx,
            }
            if score >= 0.80:
                kept.append(entry)
            else:
                modified.append(entry)
        else:
            cut.append({
                'script': script_sent,
                'script_index': i,
            })

    # SRT sentences with no script match = added/ad-libbed
    added = []
    for j, srt_sent in enumerate(srt_sentences):
        if j not in srt_matched:
            added.append({
                'srt': srt_sent['text'],
                'srt_start': srt_sent['start_sec'],
                'srt_end': srt_sent['end_sec'],
                'srt_index': j,
            })

    total_script = len(script_sentences)
    total_srt = len(srt_sentences)

    stats = {
        'total_script_sentences': total_script,
        'total_srt_sentences': total_srt,
        'kept_count': len(kept),
        'cut_count': len(cut),
        'added_count': len(added),
        'modified_count': len(modified),
        'survival_rate': (len(kept) + len(modified)) / total_script * 100 if total_script > 0 else 0,
        'addition_rate': len(added) / total_srt * 100 if total_srt > 0 else 0,
    }

    return {
        'kept': kept,
        'cut': cut,
        'added': added,
        'modified': modified,
        'stats': stats,
    }


# =========================================================================
# RETENTION CORRELATION
# =========================================================================

def load_retention_curve(video_id: str) -> Optional[list[float]]:
    """Load 100-point retention curve from cache."""
    cache_file = CACHE_DIR / f"{video_id}.json"
    if not cache_file.exists():
        return None

    with open(cache_file, 'r') as f:
        data = json.load(f)

    # Cache format: data_points = [{position, retention, relative}, ...]
    data_points = data.get('data_points', [])
    if len(data_points) == 100:
        return [dp['retention'] for dp in data_points]

    # Fallback: direct retention_curve key
    curve = data.get('retention_curve', [])
    if len(curve) == 100:
        return curve

    return None


def position_to_retention(position_sec: float, duration_sec: float, curve: list[float]) -> Optional[float]:
    """Map a timestamp position to the retention curve value."""
    if duration_sec <= 0 or not curve:
        return None

    pct = position_sec / duration_sec
    index = min(int(pct * 100), 99)
    return curve[index]


def correlate_with_retention(
    deviations: dict,
    video_id: str,
    duration_sec: float,
) -> dict:
    """
    Correlate deviation positions with retention data.

    Returns enhanced deviations dict with retention values.
    """
    curve = load_retention_curve(video_id)
    if not curve:
        logger.debug("No retention curve for %s", video_id)
        return deviations

    avg_retention = mean(curve)

    # Add retention to kept items
    for item in deviations['kept']:
        mid_sec = (item['srt_start'] + item['srt_end']) / 2
        ret = position_to_retention(mid_sec, duration_sec, curve)
        item['retention'] = ret

    # Add retention to modified items
    for item in deviations['modified']:
        mid_sec = (item['srt_start'] + item['srt_end']) / 2
        ret = position_to_retention(mid_sec, duration_sec, curve)
        item['retention'] = ret

    # Add retention to added items
    for item in deviations['added']:
        mid_sec = (item['srt_start'] + item['srt_end']) / 2
        ret = position_to_retention(mid_sec, duration_sec, curve)
        item['retention'] = ret

    # Compute retention for zones where cuts happened (use surrounding SRT positions)
    # For cuts, we approximate by looking at adjacent kept/modified items
    for item in deviations['cut']:
        idx = item['script_index']
        # Find nearest kept/modified items by script index
        neighbors = []
        for k in deviations['kept'] + deviations['modified']:
            if abs(k['script_index'] - idx) <= 3 and k.get('retention') is not None:
                neighbors.append(k['retention'])
        item['surrounding_retention'] = mean(neighbors) if neighbors else None

    deviations['avg_retention'] = avg_retention
    deviations['has_retention'] = True

    return deviations


# =========================================================================
# PROJECT DISCOVERY
# =========================================================================

def _should_skip_srt(name: str) -> bool:
    """Check if SRT filename should be skipped."""
    for pattern in SRT_SKIP_PATTERNS:
        if re.search(pattern, name, re.IGNORECASE):
            return True
    return False


def find_project_pairs() -> list[dict]:
    """
    Find all projects with both a script and an English SRT file.

    Returns list of dicts: {project, script_path, srt_path, slug}
    """
    pairs = []

    for project_dir in sorted(PROJECTS_DIR.iterdir()):
        if not project_dir.is_dir():
            continue

        # Find script
        script_path = None
        for name in ['02-SCRIPT-DRAFT.md', 'SCRIPT.md', 'SCRIPT-PART1.md', 'FINAL-SCRIPT.md']:
            candidate = project_dir / name
            if candidate.exists():
                script_path = candidate
                break

        if not script_path:
            continue

        # Find primary English SRT
        srt_path = None
        for srt in project_dir.glob('*.srt'):
            if not _should_skip_srt(srt.name):
                srt_path = srt
                break

        if not srt_path:
            continue

        pairs.append({
            'project': project_dir.name,
            'script_path': script_path,
            'srt_path': srt_path,
            'slug': project_dir.name,
        })

    logger.info("Found %d project pairs with script + SRT", len(pairs))
    return pairs


def get_video_id_for_project(project_slug: str) -> Optional[str]:
    """Look up video ID from analytics.db using the SRT-to-video mapping."""
    # Import the mapping function from retention_analysis
    try:
        from tools.youtube_analytics.retention_analysis import build_srt_mapping
        mapping = build_srt_mapping()
        # mapping is {video_id: srt_path}
        # We need reverse: find video_id whose srt_path is in this project
        for vid_id, srt_path in mapping.items():
            if project_slug in str(srt_path):
                return vid_id
    except Exception as e:
        logger.debug("Could not load SRT mapping: %s", e)

    return None


def get_video_metadata(video_id: str) -> Optional[dict]:
    """Get video metadata from analytics.db."""
    if not DB_PATH.exists():
        return None
    from tools.youtube_analytics.store import AnalyticsStore
    with AnalyticsStore.open(DB_PATH) as store:
        v = store.video(video_id)
    if not v:
        return None
    keep = ('video_id', 'title', 'duration_seconds', 'views', 'topic_type')
    return {k: v[k] for k in keep}


# =========================================================================
# ANALYSIS
# =========================================================================

def analyze_project(
    script_path: Path,
    srt_path: Path,
    video_id: Optional[str] = None,
    duration_sec: Optional[float] = None,
) -> dict:
    """
    Run full deviation analysis for a single project.

    Returns analysis dict with deviations, stats, and retention correlations.
    """
    script_sentences = parse_script(script_path)
    subtitles = parse_srt(srt_path)

    # Normalize SRT timestamps: some SRTs start at 01:00:00 (timeline offset)
    if subtitles and subtitles[0]['start_sec'] >= 3500:
        offset = subtitles[0]['start_sec']
        for sub in subtitles:
            sub['start_sec'] -= offset
            sub['end_sec'] -= offset

    srt_sentences = srt_to_sentences(subtitles)

    logger.info("  Script: %d sentences | SRT: %d sentences", len(script_sentences), len(srt_sentences))

    deviations = classify_deviations(script_sentences, srt_sentences)

    # Correlate with retention if we have the video ID
    if video_id and duration_sec:
        deviations = correlate_with_retention(deviations, video_id, duration_sec)

    return deviations


def analyze_all_projects() -> list[dict]:
    """
    Analyze all projects with script+SRT pairs.

    Returns list of project analysis dicts.
    """
    pairs = find_project_pairs()
    results = []

    for pair in pairs:
        logger.info("Analyzing %s...", pair['project'])

        # Look up video ID and metadata
        video_id = get_video_id_for_project(pair['slug'])
        duration_sec = None
        meta = None

        if video_id:
            meta = get_video_metadata(video_id)
            if meta:
                duration_sec = meta.get('duration_seconds')

        try:
            analysis = analyze_project(
                pair['script_path'],
                pair['srt_path'],
                video_id=video_id,
                duration_sec=duration_sec,
            )
        except Exception as e:
            logger.warning("  Error analyzing %s: %s", pair['project'], e)
            continue

        result = {
            'project': pair['project'],
            'script_path': str(pair['script_path']),
            'srt_path': str(pair['srt_path']),
            'video_id': video_id,
            'title': meta.get('title') if meta else None,
            'topic_type': meta.get('topic_type') if meta else None,
            'duration_sec': duration_sec,
            'views': meta.get('views') if meta else None,
            'stats': analysis['stats'],
            'has_retention': analysis.get('has_retention', False),
        }

        # Store detailed deviations for per-project drilldown
        result['deviations'] = {
            'kept_count': len(analysis['kept']),
            'cut_count': len(analysis['cut']),
            'added_count': len(analysis['added']),
            'modified_count': len(analysis['modified']),
            'cut_examples': [c['script'][:100] for c in analysis['cut'][:5]],
            'added_examples': [a['srt'][:100] for a in analysis['added'][:5]],
            'modified_examples': [
                {'script': m['script'][:80], 'srt': m['srt'][:80], 'sim': m['similarity']}
                for m in analysis['modified'][:5]
            ],
        }

        # Retention correlations
        if analysis.get('has_retention'):
            avg_ret = analysis['avg_retention']

            # Retention at kept sections
            kept_rets = [k['retention'] for k in analysis['kept'] if k.get('retention') is not None]
            # Retention at added sections
            added_rets = [a['retention'] for a in analysis['added'] if a.get('retention') is not None]
            # Retention at modified sections
            mod_rets = [m['retention'] for m in analysis['modified'] if m.get('retention') is not None]
            # Surrounding retention at cut points
            cut_surround = [c['surrounding_retention'] for c in analysis['cut'] if c.get('surrounding_retention') is not None]

            result['retention'] = {
                'avg_overall': avg_ret,
                'avg_at_kept': mean(kept_rets) if kept_rets else None,
                'avg_at_added': mean(added_rets) if added_rets else None,
                'avg_at_modified': mean(mod_rets) if mod_rets else None,
                'avg_surrounding_cuts': mean(cut_surround) if cut_surround else None,
                'n_kept': len(kept_rets),
                'n_added': len(added_rets),
                'n_modified': len(mod_rets),
                'n_cut_surround': len(cut_surround),
            }

        results.append(result)

    return results


# =========================================================================
# REPORT GENERATION
# =========================================================================

def generate_report(results: list[dict]) -> str:
    """Generate the full deviation analysis markdown report."""
    now = datetime.now(timezone.utc).strftime('%Y-%m-%d')

    lines = []
    lines.append("# Script-to-SRT Deviation Analysis")
    lines.append("")
    lines.append(f"**Generated:** {now}")
    lines.append(f"**Projects analyzed:** {len(results)}")
    lines.append("")

    # ---- Section 1: Per-Project Summary ----
    lines.append("## 1. Per-Project Deviation Summary")
    lines.append("")
    lines.append("| # | Project | Script Sents | SRT Sents | Kept | Cut | Added | Modified | Survival % |")
    lines.append("|---|---------|------------:|----------:|-----:|----:|------:|---------:|-----------:|")

    for i, r in enumerate(results, 1):
        s = r['stats']
        lines.append(
            f"| {i} | {r['project'][:35]} "
            f"| {s['total_script_sentences']} | {s['total_srt_sentences']} "
            f"| {s['kept_count']} | {s['cut_count']} | {s['added_count']} "
            f"| {s['modified_count']} | {s['survival_rate']:.0f}% |"
        )
    lines.append("")

    # ---- Section 2: Aggregate Statistics ----
    lines.append("## 2. Aggregate Statistics")
    lines.append("")

    survival_rates = [r['stats']['survival_rate'] for r in results]
    addition_rates = [r['stats']['addition_rate'] for r in results]
    cut_counts = [r['stats']['cut_count'] for r in results]
    added_counts = [r['stats']['added_count'] for r in results]

    if survival_rates:
        lines.append(f"- **Average script survival rate:** {mean(survival_rates):.1f}% (median: {median(survival_rates):.1f}%)")
        lines.append(f"- **Average addition rate:** {mean(addition_rates):.1f}% of SRT content is ad-libbed")
        lines.append(f"- **Average cuts per video:** {mean(cut_counts):.1f} sentences")
        lines.append(f"- **Average additions per video:** {mean(added_counts):.1f} sentences")
    lines.append("")

    # ---- Section 3: Survival by Topic Type ----
    lines.append("## 3. Survival Rate by Topic Type")
    lines.append("")

    topic_survival = defaultdict(list)
    for r in results:
        topic = r.get('topic_type', 'unknown') or 'unknown'
        topic_survival[topic].append(r['stats']['survival_rate'])

    lines.append("| Topic Type | n | Avg Survival % | Min | Max |")
    lines.append("|------------|--:|--------------:|----:|----:|")

    for topic in sorted(topic_survival.keys()):
        rates = topic_survival[topic]
        lines.append(
            f"| {topic} | {len(rates)} "
            f"| {mean(rates):.1f}% | {min(rates):.0f}% | {max(rates):.0f}% |"
        )
    lines.append("")

    # ---- Section 4: What Gets Cut (Examples) ----
    lines.append("## 4. What Gets Cut (Most Common Patterns)")
    lines.append("")
    lines.append("Example sentences from scripts that did not appear in the final SRT.")
    lines.append("")

    all_cuts = []
    for r in results:
        for example in r['deviations']['cut_examples']:
            all_cuts.append({'project': r['project'], 'text': example})

    if all_cuts:
        for i, c in enumerate(all_cuts[:20], 1):
            lines.append(f"{i}. **{c['project'][:25]}:** \"{c['text']}\"")
        lines.append("")
        lines.append(f"*{sum(r['stats']['cut_count'] for r in results)} total cut sentences across {len(results)} projects.*")
    else:
        lines.append("No cuts detected.")
    lines.append("")

    # ---- Section 5: What Gets Added (Examples) ----
    lines.append("## 5. What Gets Added (Ad-libs)")
    lines.append("")
    lines.append("Content in the SRT that was NOT in the script — improvised during filming.")
    lines.append("")

    all_adds = []
    for r in results:
        for example in r['deviations']['added_examples']:
            all_adds.append({'project': r['project'], 'text': example})

    if all_adds:
        for i, a in enumerate(all_adds[:20], 1):
            lines.append(f"{i}. **{a['project'][:25]}:** \"{a['text']}\"")
        lines.append("")
        lines.append(f"*{sum(r['stats']['added_count'] for r in results)} total added sentences across {len(results)} projects.*")
    else:
        lines.append("No additions detected.")
    lines.append("")

    # ---- Section 6: Modifications (Script vs SRT Differences) ----
    lines.append("## 6. Modifications (Script Changed During Filming)")
    lines.append("")

    all_mods = []
    for r in results:
        for m in r['deviations']['modified_examples']:
            all_mods.append({
                'project': r['project'],
                'script': m['script'],
                'srt': m['srt'],
                'similarity': m['sim'],
            })

    if all_mods:
        lines.append("| # | Project | Script Version | Filmed Version | Similarity |")
        lines.append("|---|---------|----------------|----------------|----------:|")
        for i, m in enumerate(all_mods[:15], 1):
            lines.append(
                f"| {i} | {m['project'][:20]} "
                f"| {m['script'][:50]}... | {m['srt'][:50]}... | {m['similarity']:.0%} |"
            )
    else:
        lines.append("No significant modifications detected.")
    lines.append("")

    # ---- Section 7: Retention Correlation ----
    lines.append("## 7. Retention Correlation")
    lines.append("")
    lines.append("How do deviations correlate with viewer retention?")
    lines.append("")

    ret_results = [r for r in results if r.get('retention')]

    if ret_results:
        # Aggregate retention data
        kept_rets = []
        added_rets = []
        mod_rets = []
        cut_surrounds = []

        for r in ret_results:
            ret = r['retention']
            if ret.get('avg_at_kept') is not None:
                kept_rets.append(ret['avg_at_kept'])
            if ret.get('avg_at_added') is not None:
                added_rets.append(ret['avg_at_added'])
            if ret.get('avg_at_modified') is not None:
                mod_rets.append(ret['avg_at_modified'])
            if ret.get('avg_surrounding_cuts') is not None:
                cut_surrounds.append(ret['avg_surrounding_cuts'])

        lines.append("| Deviation Type | n (videos) | Avg Retention at Position | Interpretation |")
        lines.append("|----------------|----------:|--------------------------:|----------------|")

        if kept_rets:
            lines.append(f"| Kept (script = SRT) | {len(kept_rets)} | {mean(kept_rets):.3f} | Baseline — script held |")
        if mod_rets:
            lines.append(f"| Modified (reworded) | {len(mod_rets)} | {mean(mod_rets):.3f} | Rewording effect |")
        if added_rets:
            lines.append(f"| Added (ad-lib) | {len(added_rets)} | {mean(added_rets):.3f} | Improvisation effect |")
        if cut_surrounds:
            lines.append(f"| Cut zones (surrounding) | {len(cut_surrounds)} | {mean(cut_surrounds):.3f} | Where cuts happened |")
        lines.append("")

        # Delta analysis
        if kept_rets and added_rets:
            kept_avg = mean(kept_rets)
            added_avg = mean(added_rets)
            delta = added_avg - kept_avg
            direction = "higher" if delta > 0 else "lower"
            lines.append(f"**Ad-lib retention delta:** {delta:+.3f} ({direction} than scripted sections)")
            lines.append("")

        if kept_rets and cut_surrounds:
            kept_avg = mean(kept_rets)
            cut_avg = mean(cut_surrounds)
            delta = cut_avg - kept_avg
            direction = "higher" if delta > 0 else "lower"
            lines.append(f"**Cut zone retention delta:** {delta:+.3f} ({direction} than kept sections)")
            lines.append("")

    else:
        lines.append("No retention data available for analyzed projects. Run `retention_analysis.py` first.")
        lines.append("")

    # ---- Section 8: Interpreted Findings ----
    lines.append("## Interpreted Findings")
    lines.append("")

    findings = _generate_findings(results, ret_results)
    for f in findings:
        lines.append(f"- {f}")
    lines.append("")

    # Footer
    lines.append("---")
    lines.append(f"*Generated by `script_srt_deviation.py` on {now}. "
                 f"Data covers {len(results)} projects with script+SRT pairs.*")

    return "\n".join(lines)


def _generate_findings(results: list[dict], ret_results: list[dict]) -> list[str]:
    """Generate actionable interpreted findings."""
    findings = []

    if not results:
        return ["No data to analyze."]

    survival_rates = [r['stats']['survival_rate'] for r in results]
    avg_survival = mean(survival_rates)

    findings.append(
        f"**Average script survival rate: {avg_survival:.0f}%.** "
        f"On average, {100 - avg_survival:.0f}% of scripted sentences are cut or replaced during filming."
    )

    # Highest and lowest survival
    by_survival = sorted(results, key=lambda r: r['stats']['survival_rate'])
    lowest = by_survival[0]
    highest = by_survival[-1]
    findings.append(
        f"**Most faithful to script:** {highest['project'][:30]} ({highest['stats']['survival_rate']:.0f}% survival). "
        f"**Most divergent:** {lowest['project'][:30]} ({lowest['stats']['survival_rate']:.0f}%)."
    )

    # Addition rate
    addition_rates = [r['stats']['addition_rate'] for r in results]
    avg_addition = mean(addition_rates)
    findings.append(
        f"**Ad-lib rate: {avg_addition:.0f}%** of final video content is improvised (not in the script)."
    )

    # Topic type patterns
    topic_survival = defaultdict(list)
    for r in results:
        topic = r.get('topic_type', 'unknown') or 'unknown'
        topic_survival[topic].append(r['stats']['survival_rate'])

    if len(topic_survival) >= 2:
        best_topic = max(topic_survival.items(), key=lambda x: mean(x[1]))
        worst_topic = min(topic_survival.items(), key=lambda x: mean(x[1]))
        if best_topic[0] != worst_topic[0]:
            findings.append(
                f"**{best_topic[0]} scripts survive best** ({mean(best_topic[1]):.0f}% avg). "
                f"**{worst_topic[0]} scripts diverge most** ({mean(worst_topic[1]):.0f}%)."
            )

    # Retention findings
    if ret_results:
        kept_rets = [r['retention']['avg_at_kept'] for r in ret_results if r['retention'].get('avg_at_kept')]
        added_rets = [r['retention']['avg_at_added'] for r in ret_results if r['retention'].get('avg_at_added')]

        if kept_rets and added_rets:
            kept_avg = mean(kept_rets)
            added_avg = mean(added_rets)
            delta = added_avg - kept_avg

            if abs(delta) > 0.01:
                if delta > 0:
                    findings.append(
                        f"**Ad-libs have HIGHER retention** ({added_avg:.3f} vs {kept_avg:.3f}, delta {delta:+.3f}). "
                        f"Improvised content holds viewers better than scripted content."
                    )
                else:
                    findings.append(
                        f"**Ad-libs have LOWER retention** ({added_avg:.3f} vs {kept_avg:.3f}, delta {delta:+.3f}). "
                        f"Sticking to the script correlates with better retention."
                    )
            else:
                findings.append(
                    f"**No meaningful retention difference** between scripted ({kept_avg:.3f}) "
                    f"and ad-libbed ({added_avg:.3f}) content (delta {delta:+.3f})."
                )

    # Rule 21 implication
    cut_pcts = [r['stats']['cut_count'] / r['stats']['total_script_sentences'] * 100
                for r in results if r['stats']['total_script_sentences'] > 0]
    if cut_pcts:
        avg_cut_pct = mean(cut_pcts)
        findings.append(
            f"**Filming cuts {avg_cut_pct:.0f}% of scripted content on average.** "
            f"Rule 21's +25% buffer {'is justified' if avg_cut_pct >= 15 else 'may be too generous — actual cuts are lower'}."
        )

    return findings


# =========================================================================
# CLI
# =========================================================================

def main():
    parser = argparse.ArgumentParser(
        description='Script-to-SRT deviation analysis with retention correlation.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  python -m tools.youtube_analytics.script_srt_deviation --report
  python -m tools.youtube_analytics.script_srt_deviation --video 30-belavezha-accords-2025
  python -m tools.youtube_analytics.script_srt_deviation --cached""",
    )
    parser.add_argument('--report', action='store_true',
                        help='Generate full report to channel-data/patterns/')
    parser.add_argument('--cached', action='store_true',
                        help='Use cached deviation data (skip re-analysis)')
    parser.add_argument('--video', type=str, default=None,
                        help='Single project slug for detailed analysis')

    verbosity = parser.add_mutually_exclusive_group()
    verbosity.add_argument('--verbose', '-v', action='store_true',
                           help='Verbose logging')
    verbosity.add_argument('--quiet', '-q', action='store_true',
                           help='Suppress info logging')

    args = parser.parse_args()
    setup_logging(args.verbose, args.quiet)

    # Default to --report if no action specified
    if not args.report and not args.video:
        args.report = True

    if args.cached and DEVIATION_JSON.exists():
        logger.info("Loading cached deviation data...")
        with open(DEVIATION_JSON, 'r', encoding='utf-8') as f:
            results = json.load(f)
    elif args.video:
        # Single project mode
        pairs = find_project_pairs()
        match = [p for p in pairs if args.video in p['project']]
        if not match:
            logger.error("No matching project found for '%s'", args.video)
            sys.exit(1)

        pair = match[0]
        logger.info("Analyzing %s...", pair['project'])

        video_id = get_video_id_for_project(pair['slug'])
        duration_sec = None
        if video_id:
            meta = get_video_metadata(video_id)
            if meta:
                duration_sec = meta.get('duration_seconds')

        analysis = analyze_project(
            pair['script_path'], pair['srt_path'],
            video_id=video_id, duration_sec=duration_sec,
        )

        # Print detailed single-project output
        s = analysis['stats']
        print(f"\n=== {pair['project']} ===")
        print(f"Script sentences: {s['total_script_sentences']}")
        print(f"SRT sentences:    {s['total_srt_sentences']}")
        print(f"Kept:             {s['kept_count']} ({s['survival_rate']:.0f}%)")
        print(f"Cut:              {s['cut_count']}")
        print(f"Added:            {s['added_count']} ({s['addition_rate']:.0f}%)")
        print(f"Modified:         {s['modified_count']}")

        if analysis['cut']:
            print(f"\n--- CUT from script ({len(analysis['cut'])} sentences) ---")
            for c in analysis['cut'][:10]:
                print(f"  - \"{c['script'][:100]}\"")

        if analysis['added']:
            print(f"\n--- ADDED in filming ({len(analysis['added'])} sentences) ---")
            for a in analysis['added'][:10]:
                print(f"  - \"{a['srt'][:100]}\"")

        if analysis['modified']:
            print(f"\n--- MODIFIED ({len(analysis['modified'])} sentences) ---")
            for m in analysis['modified'][:10]:
                print(f"  Script: \"{m['script'][:80]}\"")
                print(f"  SRT:    \"{m['srt'][:80]}\"")
                print(f"  Similarity: {m['similarity']:.0%}")
                print()

        return

    else:
        # Full analysis
        results = analyze_all_projects()

        # Cache results (without full deviation text to keep JSON manageable)
        with open(DEVIATION_JSON, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False, default=str)
        logger.info("Cached deviation data to %s", DEVIATION_JSON)

    if args.report or not args.video:
        report = generate_report(results)

        REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(REPORT_PATH, 'w', encoding='utf-8') as f:
            f.write(report)
        logger.info("Report saved to %s", REPORT_PATH)

        print(report)


if __name__ == '__main__':
    main()
