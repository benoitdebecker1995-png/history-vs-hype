"""
Folder-to-video matcher for the reconcile pipeline.

Two-tier matching strategy:
  Tier 1 (deterministic): read the AUTO:reconcile block in a folder's
    PROJECT-STATUS.md. If a Video ID is present, that's the match. No fuzz.
  Tier 2 (fuzzy): compute token-overlap score between folder slug and each
    candidate video title in analytics.db. Returns confidence-banded matches:
      >=0.85  -> high  (auto-propose)
      0.5-0.85 -> gray (user picks from top-N)
      <0.5    -> none  (folder stays where it is)

All stdlib. No external deps.
"""

from __future__ import annotations

import re
import sqlite3
from dataclasses import dataclass
from pathlib import Path


HIGH_CONFIDENCE = 0.85
GRAY_FLOOR = 0.5

# Common English stop-words plus channel-specific filler that never carries
# matching signal (years, generic operators, etc).
_STOPWORDS = {
    'the', 'a', 'an', 'and', 'or', 'but', 'for', 'of', 'to', 'in', 'on',
    'at', 'by', 'with', 'from', 'as', 'is', 'was', 'are', 'were', 'be',
    'been', 'being', 'this', 'that', 'these', 'those', 'it', 'its',
    'how', 'why', 'what', 'when', 'where', 'who', 'which',
    'video', 'documentary', 'history', 'episode', 'part',
}


_VIDEO_ID_RE = re.compile(r'\b([A-Za-z0-9_-]{11})\b')


@dataclass
class MatchCandidate:
    video_id: str
    title: str
    published_at: str
    score: float

    def confidence(self) -> str:
        if self.score >= HIGH_CONFIDENCE:
            return 'high'
        if self.score >= GRAY_FLOOR:
            return 'gray'
        return 'none'


def _tokenize(text: str) -> set[str]:
    """Lowercase + strip punctuation + split + drop stop-words.

    Numeric tokens kept (e.g. '1947' is signal in partition titles).
    """
    if not text:
        return set()
    cleaned = re.sub(r"[^\w\s]", " ", text.lower())
    tokens = {t for t in cleaned.split() if t and t not in _STOPWORDS}
    # Drop pure-digit years (2025, 2026) — they appear in every folder slug
    # and would inflate scores artificially. Keep other numerics.
    tokens = {t for t in tokens if not (t.isdigit() and len(t) == 4 and t.startswith('20'))}
    return tokens


def _token_overlap(a: set[str], b: set[str]) -> float:
    """Jaccard-like asymmetric overlap: how many of the slug's tokens
    appear in the title? Asymmetric on purpose — titles are typically
    longer than slugs, so symmetric Jaccard under-weights real matches.
    """
    if not a:
        return 0.0
    hits = len(a & b)
    return hits / len(a)


def score_pair(folder_slug: str, video_title: str) -> float:
    """Confidence score for a folder-slug ↔ video-title pairing.

    The folder slug is the stripped form (no leading number, no trailing year).
    See extract_topic_slug() in project_scanner.

    Range: 0.0 (no shared tokens) to 1.0 (every slug token appears in title).
    """
    slug_tokens = _tokenize(folder_slug)
    title_tokens = _tokenize(video_title)
    return _token_overlap(slug_tokens, title_tokens)


def extract_video_id_from_folder(folder: Path, known_ids: set[str] | None = None) -> str | None:
    """Tier 1: look for a Video ID inside a folder's documents.

    Checks PROJECT-STATUS.md, YOUTUBE-METADATA.md, POST-PUBLISH-ANALYSIS.md
    for an 11-char YouTube ID pattern. If known_ids is provided, returns the
    first candidate that matches a known YouTube ID (catches real IDs buried
    in prose alongside dozens of false-positive 11-char substrings).
    If known_ids is None, returns the first heuristically-plausible candidate.
    """
    if not folder.is_dir():
        return None
    for filename in ('PROJECT-STATUS.md', 'YOUTUBE-METADATA.md', 'POST-PUBLISH-ANALYSIS.md'):
        path = folder / filename
        if not path.exists():
            continue
        try:
            text = path.read_text(encoding='utf-8', errors='ignore')
        except OSError:
            continue
        for match in _VIDEO_ID_RE.finditer(text):
            candidate = match.group(1)
            # If we have known_ids, only return real matches — skip false positives
            if known_ids is not None:
                if candidate in known_ids:
                    return candidate
                continue
            # No known_ids — fall back to heuristic plausibility filter
            if candidate.isdigit():
                continue
            if candidate.isalpha() and candidate == candidate.lower():
                # 11-letter lowercase word — almost certainly prose
                continue
            return candidate
    return None


def load_videos(analytics_db: Path) -> list[dict]:
    """Read all videos from analytics.db. Returns list of dicts:
    {video_id, title, published_at}.
    """
    if not analytics_db.exists():
        return []
    try:
        conn = sqlite3.connect(str(analytics_db))
        cur = conn.cursor()
        cur.execute("SELECT video_id, title, published_at FROM videos")
        rows = cur.fetchall()
        conn.close()
    except sqlite3.Error:
        return []
    return [
        {'video_id': r[0], 'title': r[1] or '', 'published_at': r[2] or ''}
        for r in rows
    ]


def match_folder(
    folder: Path,
    folder_slug: str,
    videos: list[dict],
    known_ids: set[str] | None = None,
    top_n: int = 3,
) -> tuple[MatchCandidate | None, list[MatchCandidate]]:
    """Match a folder to its YouTube video.

    Args:
        folder: Path to the project folder (for Tier 1 file lookup)
        folder_slug: cleaned slug, e.g. 'gibraltar treaty utrecht'
        videos: list of {video_id, title, published_at} dicts
        known_ids: set of valid video IDs (used to validate Tier 1 extraction)
        top_n: how many candidates to return in the gray zone

    Returns:
        (best_match, candidates)
        - best_match: the highest-confidence match if its score >= HIGH_CONFIDENCE,
          OR a Tier 1 deterministic match. None otherwise.
        - candidates: top_n sorted by score descending. For interactive picking
          in the gray zone.
    """
    known_ids = known_ids or {v['video_id'] for v in videos}

    # Tier 1: deterministic ID extraction (validated against known_ids so prose
    # substrings like "publication" / "-conference" don't shadow the real ID)
    extracted_id = extract_video_id_from_folder(folder, known_ids=known_ids)
    if extracted_id and extracted_id in known_ids:
        for v in videos:
            if v['video_id'] == extracted_id:
                cand = MatchCandidate(
                    video_id=v['video_id'],
                    title=v['title'],
                    published_at=v['published_at'],
                    score=1.0,
                )
                return cand, [cand]

    # Tier 2: fuzzy scoring
    scored = []
    for v in videos:
        s = score_pair(folder_slug, v['title'])
        if s > 0:
            scored.append(MatchCandidate(
                video_id=v['video_id'],
                title=v['title'],
                published_at=v['published_at'],
                score=s,
            ))
    scored.sort(key=lambda c: c.score, reverse=True)
    top = scored[:top_n]

    if top and top[0].score >= HIGH_CONFIDENCE:
        return top[0], top
    return None, top
