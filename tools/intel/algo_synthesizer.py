"""
algo_synthesizer.py — Algorithm knowledge synthesizer for the YouTube Intelligence Engine

Two-mode design:
    1. Text-analysis mode (primary):  keyword extraction + sentence scoring — runs
       purely in Python with no external dependencies.  This is what refresh.py calls.

    2. LLM mode (agent context):      SYNTHESIS_PROMPT constant is available so the
       /intel command can pass scraped text to Claude Code's LLM layer and receive a
       fully structured JSON algorithm model.

JSON output schema (both modes):
    {
      "signal_weights":       {ctr, avd, satisfaction, session_continuation, upload_consistency},
      "pipeline_mechanics":   {browse_feed, search, suggested},
      "longform_specific":    [str, ...],
      "satisfaction_signals": [str, ...],
      "avd_thresholds":       str | null,
      "ctr_thresholds":       str | null,
      "small_channel_notes":  str | null,
      "sources_used":         [str, ...],
      "confidence":           "high" | "medium" | "low",
      "synthesis_date":       str  (ISO date),
    }

All public functions follow the error-dict pattern: return {'error': msg} on failure,
never raise.
"""

import re
from datetime import datetime, timezone

# ---------------------------------------------------------------------------
# LLM Synthesis Prompt (used by /intel command in Claude Code agent context)
# ---------------------------------------------------------------------------

SYNTHESIS_PROMPT = """You are analyzing YouTube algorithm documentation from official and authoritative sources.

SCRAPED CONTENT (use ONLY this, ignore your training data):
{scraped_text}

Extract and structure the following as JSON:
{{
  "signal_weights": {{
    "ctr": "very_high|high|medium|low",
    "avd": "very_high|high|medium|low",
    "satisfaction": "very_high|high|medium|low",
    "session_continuation": "very_high|high|medium|low",
    "upload_consistency": "very_high|high|medium|low"
  }},
  "pipeline_mechanics": {{
    "browse_feed": "how it works for longform, 1-2 sentences",
    "search": "how it works for longform, 1-2 sentences",
    "suggested": "how it works for longform, 1-2 sentences"
  }},
  "longform_specific": ["insight1", "insight2"],
  "satisfaction_signals": ["signal1", "signal2"],
  "avd_thresholds": "any specific % thresholds mentioned",
  "ctr_thresholds": "any specific % thresholds mentioned",
  "small_channel_notes": "any mentions of small channel behavior",
  "sources_used": ["source1", "source2"],
  "confidence": "high|medium|low",
  "synthesis_date": "{date}"
}}

Rules:
- ONLY use information from the scraped content above
- Ignore your training knowledge about the YouTube algorithm
- Note the publication date of each source when constructing insights
- If sources conflict, note both and mark confidence as low
- If information is absent, use null, not assumptions
- Longform means 10+ minute videos; exclude all Shorts guidance
- Flag any conflicting claims across sources in the relevant fields
"""

# ---------------------------------------------------------------------------
# Keyword lists for text-analysis mode
# ---------------------------------------------------------------------------

# Signal keywords: (signal_name, [terms that suggest it's HIGH priority])
_SIGNAL_KEYWORDS = {
    "ctr": [
        "click-through rate", "ctr", "thumbnail", "title", "click through",
        "impressions", "click rate",
    ],
    "avd": [
        "average view duration", "avd", "watch time", "retention", "average duration",
        "watch percentage", "average watch",
    ],
    "satisfaction": [
        "satisfaction", "viewer satisfaction", "survey", "post-watch survey",
        "wss", "qcr", "rd", "vli", "happy", "quality", "viewer experience",
    ],
    "session_continuation": [
        "session", "session continuation", "watch next", "suggested", "follow-up",
        "binge", "session watch time",
    ],
    "upload_consistency": [
        "consistency", "upload schedule", "regular", "frequency", "consistent uploads",
    ],
}

# Pipeline keywords
_PIPELINE_KEYWORDS = {
    "browse_feed": [
        "browse", "home feed", "homepage", "home page", "browse feed",
        "personalized", "subscription feed", "recommended",
    ],
    "search": [
        "search", "search results", "seo", "keyword", "search traffic",
        "discovery via search",
    ],
    "suggested": [
        "suggested", "up next", "recommended video", "sidebar", "end screen",
        "what to watch next", "similar video",
    ],
}

# Longform signals
_LONGFORM_KEYWORDS = [
    "longform", "long-form", "long form", "10 minute", "10+ minute", "20 minute",
    "30 minute", "deep dive", "documentary", "in-depth", "long video",
    "watch time benefit", "watch hours",
]

# Satisfaction signal named types
_SATISFACTION_SIGNAL_KEYWORDS = [
    "wss", "qcr", "rd", "vli", "post-watch survey", "viewer satisfaction score",
    "quality control rating", "repeat demand", "viewer loyalty index",
    "like", "dislike", "share", "survey response",
]

# AVD/CTR threshold patterns
_THRESHOLD_PATTERN = re.compile(
    r"(\d+(?:\.\d+)?)\s*%\s*(?:avd|ctr|click.through|average view duration|retention)",
    re.IGNORECASE,
)
_CTR_THRESHOLD_PATTERN = re.compile(
    r"(\d+(?:\.\d+)?)\s*%\s*(?:ctr|click.through rate|click rate)",
    re.IGNORECASE,
)
_AVD_THRESHOLD_PATTERN = re.compile(
    r"(\d+(?:\.\d+)?)\s*%\s*(?:avd|average view duration|retention|watch)",
    re.IGNORECASE,
)

# Small channel keywords
_SMALL_CHANNEL_KEYWORDS = [
    "small channel", "new channel", "low subscriber", "growing channel",
    "emerging creator", "small creator", "starting out", "new creator",
]


def _now_date() -> str:
    """Return current UTC date as YYYY-MM-DD string."""
    return datetime.now(timezone.utc).date().isoformat()


def _count_keyword_hits(text: str, keywords: list) -> int:
    """Count how many distinct keywords appear in text (case-insensitive)."""
    text_lower = text.lower()
    return sum(1 for kw in keywords if kw.lower() in text_lower)


def _extract_sentences_with_keywords(text: str, keywords: list, max_sentences: int = 3) -> list:
    """
    Extract up to max_sentences sentences that contain at least one keyword.

    Returns list of cleaned sentence strings.
    """
    # Split on sentence boundaries (period, exclamation, question mark + space/newline)
    sentences = re.split(r"(?<=[.!?])\s+", text)
    hits = []
    text_lower = text.lower()
    for sent in sentences:
        sent_lower = sent.lower()
        if any(kw.lower() in sent_lower for kw in keywords):
            clean = sent.strip()
            if len(clean) > 20:  # Skip very short fragments
                hits.append(clean)
        if len(hits) >= max_sentences:
            break
    return hits


def _score_signal(text: str, keywords: list) -> str:
    """
    Map keyword hit count to a priority level.

    Returns: 'very_high' | 'high' | 'medium' | 'low'
    """
    hits = _count_keyword_hits(text, keywords)
    if hits >= 4:
        return "very_high"
    if hits >= 2:
        return "high"
    if hits >= 1:
        return "medium"
    return "low"


def _extract_thresholds(text: str) -> tuple:
    """
    Attempt to extract specific AVD and CTR percentage thresholds from text.

    Returns:
        (avd_threshold_str, ctr_threshold_str) — each may be None if not found.
    """
    avd_matches = _AVD_THRESHOLD_PATTERN.findall(text)
    ctr_matches = _CTR_THRESHOLD_PATTERN.findall(text)

    avd_str = f"{avd_matches[0]}% average view duration mentioned" if avd_matches else None
    ctr_str = f"{ctr_matches[0]}% CTR mentioned" if ctr_matches else None
    return avd_str, ctr_str


def _extract_small_channel_note(text: str) -> str | None:
    """Extract the first sentence mentioning small channels, or None."""
    sentences = _extract_sentences_with_keywords(text, _SMALL_CHANNEL_KEYWORDS, max_sentences=1)
    return sentences[0] if sentences else None


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def synthesize_with_text_analysis(scraped_results: list) -> dict:
    """
    Synthesize algorithm knowledge from scraped results using keyword analysis.

    This is the primary mode for automated refresh (no LLM required).
    SYNTHESIS_PROMPT is used by the /intel command for LLM-powered synthesis.

    Args:
        scraped_results: List of dicts from algo_scraper.scrape_all_sources().
                         Each should have 'source', 'content', and optionally 'authority'.
                         Results with 'error' key are skipped.

    Returns:
        {
            'algorithm_model': dict,   # Full structured model (same schema as LLM mode)
            'signal_weights':  dict,   # Extracted signal weights
            'longform_insights': list, # Longform-specific insight sentences
            'confidence': str,         # 'high' | 'medium' | 'low'
            'sources_used': list,      # Source names that contributed content
        }
        or {'error': str}
    """
    # Filter to successful results only
    successful = [r for r in scraped_results if "error" not in r and r.get("content")]

    if not successful:
        return {"error": "No algorithm sources available for synthesis"}

    # Combine all content into a single text block for analysis
    combined_text = "\n\n".join(
        f"=== SOURCE: {r.get('source', 'unknown')} ===\n{r.get('content', '')}"
        for r in successful
    )
    sources_used = [r.get("source", "unknown") for r in successful]

    # --- Signal weights ---
    signal_weights = {
        signal: _score_signal(combined_text, keywords)
        for signal, keywords in _SIGNAL_KEYWORDS.items()
    }

    # --- Pipeline mechanics ---
    pipeline_mechanics = {}
    for pipeline, keywords in _PIPELINE_KEYWORDS.items():
        sentences = _extract_sentences_with_keywords(combined_text, keywords, max_sentences=1)
        if sentences:
            pipeline_mechanics[pipeline] = sentences[0][:200]  # Trim for conciseness
        else:
            pipeline_mechanics[pipeline] = None

    # --- Longform insights ---
    longform_insights = _extract_sentences_with_keywords(
        combined_text, _LONGFORM_KEYWORDS, max_sentences=5
    )

    # --- Satisfaction signals ---
    satisfaction_signals = _extract_sentences_with_keywords(
        combined_text, _SATISFACTION_SIGNAL_KEYWORDS, max_sentences=4
    )

    # --- Thresholds ---
    avd_threshold, ctr_threshold = _extract_thresholds(combined_text)

    # --- Small channel notes ---
    small_channel_notes = _extract_small_channel_note(combined_text)

    # --- Confidence: based on number of high-authority sources ---
    high_auth = sum(1 for r in successful if r.get("authority") in ("high", "highest"))
    if high_auth >= 2:
        confidence = "medium"  # Text analysis is always at most 'medium' (not LLM)
    elif high_auth >= 1:
        confidence = "medium"
    else:
        confidence = "low"

    algorithm_model = {
        "signal_weights": signal_weights,
        "pipeline_mechanics": pipeline_mechanics,
        "longform_specific": longform_insights,
        "satisfaction_signals": satisfaction_signals,
        "avd_thresholds": avd_threshold,
        "ctr_thresholds": ctr_threshold,
        "small_channel_notes": small_channel_notes,
        "sources_used": sources_used,
        "confidence": confidence,
        "synthesis_date": _now_date(),
    }

    return {
        "algorithm_model": algorithm_model,
        "signal_weights": signal_weights,
        "longform_insights": longform_insights,
        "confidence": confidence,
        "sources_used": sources_used,
    }
