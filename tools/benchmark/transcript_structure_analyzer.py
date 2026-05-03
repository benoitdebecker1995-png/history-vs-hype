"""
Competitor transcript structure analyzer.

Fetches transcripts for top-10 videos (by views) from 10 benchmark channels,
analyzes structural patterns (hooks, turns, closes, pacing), and generates
an aggregate report with actionable rules.

Usage:
    python -m tools.benchmark.transcript_structure_analyzer --fetch
    python -m tools.benchmark.transcript_structure_analyzer --analyze
    python -m tools.benchmark.transcript_structure_analyzer --report
"""

import argparse
import json
import math
import re
import statistics
import time
from collections import Counter, defaultdict
from pathlib import Path

BENCHMARK_DIR = Path("tools/benchmark")
RAW_DIR = BENCHMARK_DIR / "raw_data"
TRANSCRIPT_DIR = BENCHMARK_DIR / "transcripts"
REPORT_PATH = BENCHMARK_DIR / "TRANSCRIPT-STRUCTURE-ANALYSIS.md"

CHANNELS = [
    "wonderwhy",
    "kraut",
    "shaun",
    "caspianreport",
    "knowing_better",
    "three_arrows",
    "historia_civilis",
    "atun-shei_films",
    "tikhistory",
    "fall_of_civilizations",
]

# Mapping from JSON filename stem to display-friendly folder name
CHANNEL_DISPLAY = {
    "wonderwhy": "WonderWhy",
    "kraut": "Kraut",
    "shaun": "Shaun",
    "caspianreport": "CaspianReport",
    "knowing_better": "Knowing_Better",
    "three_arrows": "Three_Arrows",
    "historia_civilis": "Historia_Civilis",
    "atun-shei_films": "Atun-Shei_Films",
    "tikhistory": "TikHistory",
    "fall_of_civilizations": "Fall_of_Civilizations",
}

LANGUAGE_PRIORITIES = ["en", "en-GB", "en-US", "en-AU", "en-CA"]

# ---------- Date / entity regex ----------

YEAR_RE = re.compile(r'\b(\d{3,4})\s*(?:AD|BC|BCE|CE|B\.C\.|A\.D\.)?\b')
ORDINAL_DATE_RE = re.compile(
    r'\b(?:January|February|March|April|May|June|July|August|September|'
    r'October|November|December)\s+\d{1,2}(?:st|nd|rd|th)?,?\s*\d{2,4}\b',
    re.IGNORECASE,
)
NAMED_ENTITY_RE = re.compile(r'\b([A-Z][a-z]+(?:\s+(?:of|the|de|al|von|van)\s+)?[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b')
QUESTION_RE = re.compile(r'[^.!?]*\?')

# Turn-moment markers
TURN_MARKERS = [
    "but here's the thing",
    "but here's where",
    "here's where it gets",
    "here's the problem",
    "the problem is",
    "the problem was",
    "what nobody",
    "what most people don't",
    "what you might not",
    "the truth is",
    "the reality is",
    "the real reason",
    "in reality",
    "except that's not",
    "except it wasn't",
    "but that's not",
    "but it wasn't",
    "but none of this",
    "however,",
    "but there's a catch",
    "there's just one problem",
    "but wait",
    "and yet",
    "but in fact",
    "the catch is",
    "what actually happened",
    "so what went wrong",
    "so why did",
    "so why does",
    "but why",
    "the twist",
    "plot twist",
    "little did they know",
]

# Hook classification: myth-contradiction openers
MYTH_OPENERS = [
    "most people", "you've probably", "you might think", "you may have heard",
    "everyone knows", "we've all been told", "the story goes", "as the story goes",
    "conventional wisdom", "popular belief", "common belief", "it's commonly",
    "many people believe", "we're often told", "the popular narrative",
    "the standard story", "the usual story", "according to popular",
    "history tells us", "we all learned", "you were taught",
    "the myth", "the legend",
]

# Close-type markers
CLOSE_PREDICTION = ["will ", "future", "remains to be seen", "only time", "we'll see", "going forward"]
CLOSE_HUMAN_COST = ["lives", "died", "killed", "suffering", "victims", "lost their", "people who"]
CLOSE_PATTERN = ["pattern", "cycle", "repeats", "history shows", "time and again", "the lesson"]


# ==========================================================================
# FETCH
# ==========================================================================

COOKIE_FILE = Path.home() / "Downloads" / "www.youtube.com_cookies.txt"


def _fetch_via_ytdlp(vid_id: str, out_file: Path) -> bool:
    """Fetch transcript using yt-dlp with cookies. Returns True on success."""
    import subprocess
    import tempfile

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_prefix = Path(tmpdir) / vid_id
        cmd = [
            "yt-dlp",
            "--write-auto-sub", "--sub-format", "json3",
            "--sub-lang", "en-orig,en,en-GB",
            "--skip-download", "-f", "sb0",
            "-o", str(tmp_prefix),
            f"https://www.youtube.com/watch?v={vid_id}",
        ]
        if COOKIE_FILE.exists():
            cmd[1:1] = ["--cookies", str(COOKIE_FILE)]

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)

        # Find the downloaded json3 file
        json3_files = list(Path(tmpdir).glob(f"{vid_id}*.json3"))
        if not json3_files:
            return False

        # Convert json3 to our timestamp+text format
        with open(json3_files[0], encoding="utf-8") as f:
            data = json.load(f)

        lines = []
        for evt in data.get("events", []):
            if "segs" not in evt:
                continue
            start_s = evt.get("tStartMs", 0) / 1000
            text = "".join(seg.get("utf8", "") for seg in evt["segs"]).strip()
            text = text.replace("\n", " ")
            if text and not (text.startswith("[") and text.endswith("]")):
                lines.append(f"{start_s:.1f}\t{text}")

        if lines:
            out_file.write_text("\n".join(lines), encoding="utf-8")
            return True
        return False


def fetch_transcripts():
    """Download transcripts for top-10 videos (by views) per channel.

    Uses youtube_transcript_api first, falls back to yt-dlp with cookies.
    """
    from youtube_transcript_api import YouTubeTranscriptApi

    api = YouTubeTranscriptApi()
    total_fetched = 0
    total_skipped = 0
    total_failed = 0
    api_blocked = False

    for channel_key in CHANNELS:
        display = CHANNEL_DISPLAY[channel_key]
        json_path = RAW_DIR / f"{channel_key}.json"
        if not json_path.exists():
            print(f"[SKIP] {display}: no raw_data JSON found")
            continue

        with open(json_path, encoding="utf-8") as f:
            data = json.load(f)

        videos = sorted(data.get("all_videos", []), key=lambda v: v.get("view_count", 0), reverse=True)[:10]
        out_dir = TRANSCRIPT_DIR / display
        out_dir.mkdir(parents=True, exist_ok=True)

        print(f"\n{'='*60}")
        print(f"[FETCH] {display} — {len(videos)} videos")
        print(f"{'='*60}")

        for i, vid in enumerate(videos):
            vid_id = vid["id"]
            title = vid.get("title", "?")
            out_file = out_dir / f"{vid_id}.txt"

            if out_file.exists():
                content = out_file.read_text(encoding="utf-8").strip()
                if not content.startswith("ERROR:") and len(content) > 100:
                    print(f"  [{i+1}/10] SKIP (exists): {title[:60]}")
                    total_skipped += 1
                    continue

            print(f"  [{i+1}/10] Fetching: {title[:60]}...", end=" ", flush=True)

            # Try youtube_transcript_api first (faster, no cookies needed)
            if not api_blocked:
                try:
                    transcript = api.fetch(vid_id, languages=LANGUAGE_PRIORITIES)
                    lines = []
                    for entry in transcript:
                        text = entry.text.strip()
                        if not text:
                            continue
                        lines.append(f"{entry.start:.1f}\t{text}")
                    out_file.write_text("\n".join(lines), encoding="utf-8")
                    print(f"OK-api ({len(lines)} lines)")
                    total_fetched += 1
                    time.sleep(2)
                    continue
                except Exception as e:
                    err_msg = str(e)[:200].lower()
                    if "blocking" in err_msg or "blocked" in err_msg or "429" in err_msg:
                        print("API blocked, switching to yt-dlp...", end=" ", flush=True)
                        api_blocked = True
                    else:
                        # Non-blocking error (e.g., no transcript available)
                        pass

            # Fallback: yt-dlp with cookies
            try:
                if _fetch_via_ytdlp(vid_id, out_file):
                    # Count lines in saved file
                    line_count = len(out_file.read_text(encoding="utf-8").strip().split("\n"))
                    print(f"OK-ytdlp ({line_count} lines)")
                    total_fetched += 1
                else:
                    print("FAIL: no English subs via yt-dlp")
                    out_file.write_text("ERROR: no English subtitles available", encoding="utf-8")
                    total_failed += 1
            except Exception as e:
                err_msg = str(e)[:120]
                print(f"FAIL: {err_msg}")
                out_file.write_text(f"ERROR: {err_msg}", encoding="utf-8")
                total_failed += 1

            time.sleep(3)

    print(f"\n{'='*60}")
    print(f"FETCH COMPLETE: {total_fetched} fetched, {total_skipped} skipped, {total_failed} failed")
    print(f"{'='*60}")


# ==========================================================================
# ANALYZE
# ==========================================================================

def load_transcript(path: Path) -> list[dict] | None:
    """Load a transcript file. Returns list of {start, text} or None if error/empty."""
    text = path.read_text(encoding="utf-8").strip()
    if text.startswith("ERROR:") or not text:
        return None
    entries = []
    for line in text.split("\n"):
        parts = line.split("\t", 1)
        if len(parts) == 2:
            try:
                entries.append({"start": float(parts[0]), "text": parts[1]})
            except ValueError:
                continue
    return entries if entries else None


def transcript_to_text(entries: list[dict]) -> str:
    """Join transcript entries into continuous text."""
    raw = " ".join(e["text"] for e in entries)
    # Clean transcript artifacts
    raw = re.sub(r'\[.*?\]', '', raw)  # Remove [Music], [Applause] etc
    raw = re.sub(r'\s+', ' ', raw).strip()
    return raw


def estimate_duration(entries: list[dict]) -> float:
    """Estimate video duration from last transcript entry."""
    if not entries:
        return 0
    return entries[-1]["start"] + 5  # rough: last entry + ~5s


def is_unpunctuated(text: str) -> bool:
    """Detect auto-generated transcripts that lack punctuation."""
    # If fewer than 1 sentence-ending punctuation per 500 chars, it's unpunctuated
    endings = len(re.findall(r'[.!?]', text[:2000]))
    return endings < (min(len(text), 2000) / 500)


def split_sentences(text: str) -> list[str]:
    """Split text into sentences. Handles unpunctuated auto-generated transcripts."""
    if is_unpunctuated(text):
        # For unpunctuated text, split on ~15-word chunks (avg sentence length)
        words = text.split()
        sents = []
        for i in range(0, len(words), 15):
            chunk = " ".join(words[i:i+15])
            if chunk.strip():
                sents.append(chunk)
        return sents
    sents = re.split(r'(?<=[.!?])\s+(?=[A-Z"])', text)
    return [s.strip() for s in sents if s.strip()]


def split_sentences_for_hook(text: str, entries: list[dict]) -> list[str]:
    """Split into sentences for hook analysis. Uses pause-based splitting for unpunctuated text."""
    if not is_unpunctuated(text):
        sents = re.split(r'(?<=[.!?])\s+(?=[A-Z"])', text)
        return [s.strip() for s in sents if s.strip()]

    # For unpunctuated: use transcript timing gaps as sentence boundaries
    # A gap > 1.5s between entries suggests a sentence break
    sents = []
    current = []
    for i, e in enumerate(entries):
        text_clean = e["text"].strip()
        # Skip music/sound markers
        if re.match(r'^\[.*\]$', text_clean):
            continue
        current.append(text_clean)
        if i + 1 < len(entries):
            gap = entries[i + 1]["start"] - e["start"]
            # Break on pauses > 1.5s or after accumulating enough words
            words_so_far = sum(len(c.split()) for c in current)
            if gap > 1.5 or words_so_far > 25:
                sents.append(" ".join(current))
                current = []
        else:
            sents.append(" ".join(current))

    return [s.strip() for s in sents if s.strip()]


def find_dates(text: str) -> list[tuple[int, str]]:
    """Find all year-like dates with their char position."""
    results = []
    for m in YEAR_RE.finditer(text):
        year = int(m.group(1))
        if 100 <= year <= 2030:
            results.append((m.start(), m.group(0)))
    for m in ORDINAL_DATE_RE.finditer(text):
        results.append((m.start(), m.group(0)))
    return sorted(results, key=lambda x: x[0])


def char_pos_to_seconds(pos: int, entries: list[dict], full_text: str) -> float:
    """Approximate the timestamp for a character position in the joined text."""
    # Build cumulative character positions per entry
    cum = 0
    for e in entries:
        clean = re.sub(r'\[.*?\]', '', e["text"])
        clean = re.sub(r'\s+', ' ', clean).strip()
        end = cum + len(clean) + 1  # +1 for space
        if pos <= end:
            return e["start"]
        cum = end
    return entries[-1]["start"] if entries else 0


def classify_hook(first_3_sentences: str) -> str:
    """Classify hook type based on first 3 sentences.

    Works on both punctuated and unpunctuated (auto-generated) transcripts.
    """
    lower = first_3_sentences.lower().strip()

    # Strip common greetings to get to real content
    greeting_stripped = re.sub(
        r'^(hello|hey|hi)[\s,]*(everyone|there|guys)?[\s,]*(today|so|now)?[\s,]*',
        '', lower
    ).strip()

    # Use greeting-stripped version for classification but keep original for fallback
    check_text = greeting_stripped if greeting_stripped else lower

    # 1) Myth contradiction: starts with common belief phrasing
    for opener in MYTH_OPENERS:
        # Check first ~100 chars after greeting
        if opener in check_text[:150]:
            return "myth_contradiction"

    # Also check for question-then-contradict pattern ("have you ever wondered")
    if re.match(r'^(have you ever|did you know|have you heard|do you know)', check_text):
        return "myth_contradiction"

    # 2) Cold fact: opens with a specific date, year, or measurement
    first_100 = first_3_sentences[:200]
    if YEAR_RE.search(first_100[:100]):
        return "cold_fact"
    if re.search(r'\b\d{1,3}(?:,\d{3})+\b', first_100[:100]):  # Large numbers
        return "cold_fact"
    if re.search(r'\b\d+\s*(?:percent|%|million|billion|thousand|km|miles|square|centuries?|years?)\b',
                 first_100[:150], re.IGNORECASE):
        return "cold_fact"
    # "Nth century" pattern
    if re.search(r'\b\d+(?:st|nd|rd|th)\s+centur', first_100[:150], re.IGNORECASE):
        return "cold_fact"
    # "in [year]" or "in the year" pattern (works lowercase)
    if re.search(r'\bin (?:the year\s+)?\d{3,4}\b', first_100[:100]):
        return "cold_fact"

    # 3) Specificity bomb: opens with specific named person, place, or document
    # Works on lowercased text by looking for known entity patterns
    specificity_patterns = [
        r'\b(?:king|queen|emperor|president|general|captain|minister|pope|sultan|shah|czar|tsar)\s+\w+',
        r'\b(?:treaty|battle|siege|act|law|decree|charter) of \w+',
        r'\b(?:in|near|from|at) (?:the )?(?:city|town|port|island|coast|river|mountain) of \w+',
        # Place name patterns (the X of Y)
        r'\bthe (?:republic|kingdom|empire|colony|province|state|city) of \w+',
    ]
    # Also try capitalized entity regex on the original text (works for punctuated transcripts)
    entities = NAMED_ENTITY_RE.findall(first_3_sentences[:200])
    specificity_hits = len(entities)

    for pat in specificity_patterns:
        if re.search(pat, check_text[:200], re.IGNORECASE):
            specificity_hits += 1

    if specificity_hits >= 2:
        return "specificity_bomb"

    # 4) Check if it starts with a concrete scene/location ("somewhere", "there's a", "this is the")
    if re.match(r'^(somewhere|there\'?s a|this is the|imagine|picture)', check_text):
        return "specificity_bomb"

    # Default: contextual opening
    return "contextual_opening"


def find_turn_moment(text: str, entries: list[dict], duration: float) -> tuple[float | None, str | None]:
    """Find the narrative turn moment. Returns (seconds, description) or (None, None)."""
    lower = text.lower()
    best_pos = None
    best_marker = None

    # Only look for turns after 30% of the text
    min_pos = int(len(text) * 0.15)

    for marker in TURN_MARKERS:
        idx = lower.find(marker, min_pos)
        if idx != -1:
            if best_pos is None or idx < best_pos:
                best_pos = idx
                best_marker = marker

    if best_pos is None:
        return None, None

    # Extract context around the turn
    start = max(0, best_pos - 20)
    end = min(len(text), best_pos + 120)
    context = text[start:end].strip()

    seconds = char_pos_to_seconds(best_pos, entries, text)
    return seconds, context


def classify_close(last_50_words: str) -> str:
    """Classify closing type."""
    lower = last_50_words.lower()

    if lower.rstrip().endswith("?"):
        return "open_question"

    for kw in CLOSE_PREDICTION:
        if kw in lower:
            return "prediction"

    for kw in CLOSE_HUMAN_COST:
        if kw in lower:
            return "human_cost"

    for kw in CLOSE_PATTERN:
        if kw in lower:
            return "pattern_reveal"

    return "boilerplate"


def count_source_citations(text: str) -> int:
    """Count explicit source citations (e.g., 'according to X', 'X writes that')."""
    patterns = [
        r'according to\b',
        r'as\s+\w+\s+(?:writes?|wrote|notes?|noted|argues?|argued|explains?|explained|observed?|stated?)\b',
        r'\bwrites?\s+(?:in|that)\b',
        r'\bwrote\s+(?:in|that)\b',
        r'\bnotes?\s+(?:in|that)\b',
        r'in (?:his|her|their) (?:book|work|article|paper|study)\b',
        r'published in\b',
        r'quote\b',
        r'I quote\b',
    ]
    count = 0
    for pat in patterns:
        count += len(re.findall(pat, text, re.IGNORECASE))
    return count


def count_documents_mentioned(text: str) -> int:
    """Count mentions of documents, treaties, laws, etc."""
    patterns = [
        r'\b(?:treaty|accord|agreement|convention|declaration|constitution|charter|statute|act|law|code|edict|decree|bill|resolution|protocol|manifest|proclamation)\s+(?:of|on)\b',
        r'\bArticle\s+\d+',
        r'\bSection\s+\d+',
        r'\bChapter\s+\d+',
    ]
    count = 0
    for pat in patterns:
        count += len(re.findall(pat, text, re.IGNORECASE))
    return count


def analyze_single(vid_id: str, channel_display: str, channel_key: str, metadata: dict) -> dict | None:
    """Analyze a single transcript and return structured JSON."""
    transcript_path = TRANSCRIPT_DIR / channel_display / f"{vid_id}.txt"
    if not transcript_path.exists():
        return None

    entries = load_transcript(transcript_path)
    if not entries:
        return None

    text = transcript_to_text(entries)
    if len(text) < 200:
        return None

    duration = metadata.get("duration", 0) or estimate_duration(entries)
    words = text.split()
    word_count = len(words)
    sentences = split_sentences(text)
    duration_minutes = duration / 60 if duration > 0 else 1

    # --- Hook analysis ---
    first_50_words = " ".join(words[:50])
    # Use pause-based sentence splitting for hook analysis (handles unpunctuated)
    hook_sentences = split_sentences_for_hook(text, entries)
    first_sentence = hook_sentences[0] if hook_sentences else ""
    first_3_sents = " ".join(hook_sentences[:3]) if len(hook_sentences) >= 3 else text[:500]

    # Time to first date
    dates = find_dates(text)
    first_date_seconds = None
    if dates:
        first_date_seconds = char_pos_to_seconds(dates[0][0], entries, text)

    # Time to first named entity
    ent_match = NAMED_ENTITY_RE.search(text[:2000])
    first_entity_seconds = None
    if ent_match:
        first_entity_seconds = char_pos_to_seconds(ent_match.start(), entries, text)

    hook_type = classify_hook(first_3_sents)

    # First 60 seconds text
    first_60s_text = " ".join(e["text"] for e in entries if e["start"] <= 60).lower()
    opens_with_question = "?" in (sentences[0] if sentences else "")
    opens_with_document = bool(re.search(r'\b(?:document|treaty|letter|manuscript|decree|statute|law|act|article)\b', first_60s_text, re.IGNORECASE))
    first_person = bool(re.search(r'\bI\b', first_60s_text))

    # --- Structure analysis ---
    # Sections: rough heuristic — look for long pauses (>3s gap) or topic shifts
    section_count = 1
    for i in range(1, len(entries)):
        gap = entries[i]["start"] - entries[i-1]["start"]
        if gap > 8:  # >8 second gap = likely new section
            section_count += 1

    # Turn moment
    turn_seconds, turn_desc = find_turn_moment(text, entries, duration)

    # Chronological vs thematic
    date_positions = [d[0] / max(len(text), 1) for d in dates]
    if len(date_positions) >= 3:
        # If dates appear in roughly increasing order of position, it's chronological
        increasing = sum(1 for i in range(len(date_positions)-1) if date_positions[i] < date_positions[i+1])
        ratio = increasing / (len(date_positions) - 1)
        if ratio > 0.7:
            structure_type = "chronological"
        elif ratio < 0.4:
            structure_type = "thematic"
        else:
            structure_type = "hybrid"
    else:
        structure_type = "thematic"  # not enough dates to tell

    documents = count_documents_mentioned(text)
    citations = count_source_citations(text)
    questions = len(QUESTION_RE.findall(text))

    # History vs analysis ratio (rough: sentences with dates/entities = history, others = analysis)
    history_sents = 0
    for s in sentences:
        if YEAR_RE.search(s) or len(NAMED_ENTITY_RE.findall(s)) >= 2:
            history_sents += 1
    pct_history = round(history_sents / max(len(sentences), 1) * 100, 1)

    # --- Close analysis ---
    last_50_words = " ".join(words[-50:]) if len(words) >= 50 else text
    last_sentence = sentences[-1] if sentences else ""
    has_cta = bool(re.search(r'\b(?:subscribe|like|comment|click|bell|notification|share|check out|link|description)\b', last_50_words, re.IGNORECASE))
    has_future_tease = bool(re.search(r'\b(?:next (?:video|time|episode|week)|part (?:two|2|three|3)|coming soon|stay tuned|upcoming)\b', last_50_words, re.IGNORECASE))
    ends_with_question = last_sentence.strip().endswith("?")
    close_type = classify_close(last_50_words)

    # --- Pacing ---
    wpm = round(word_count / duration_minutes, 1) if duration_minutes > 0 else 0
    date_freq = round(len(dates) / duration_minutes, 2) if duration_minutes > 0 else 0
    avg_sent_len = round(statistics.mean(len(s.split()) for s in sentences), 1) if sentences else 0

    return {
        "video_id": vid_id,
        "channel": channel_display,
        "title": metadata.get("title", ""),
        "views": metadata.get("view_count", 0),
        "duration_seconds": round(duration),
        "word_count": word_count,
        "hook": {
            "first_50_words": first_50_words,
            "first_sentence": first_sentence,
            "seconds_to_first_date": round(first_date_seconds, 1) if first_date_seconds is not None else None,
            "seconds_to_first_named_entity": round(first_entity_seconds, 1) if first_entity_seconds is not None else None,
            "hook_type": hook_type,
            "opens_with_question": opens_with_question,
            "opens_with_document": opens_with_document,
            "first_person_in_first_60s": first_person,
        },
        "structure": {
            "total_sections": section_count,
            "seconds_to_first_historical_date": round(first_date_seconds, 1) if first_date_seconds is not None else None,
            "seconds_to_turn_moment": round(turn_seconds, 1) if turn_seconds is not None else None,
            "turn_moment_description": turn_desc,
            "percent_history_vs_analysis": pct_history,
            "chronological_vs_thematic": structure_type,
            "documents_mentioned": documents,
            "explicit_source_citations": citations,
            "questions_posed_to_viewer": questions,
        },
        "close": {
            "last_50_words": last_50_words,
            "has_cta": has_cta,
            "has_future_tease": has_future_tease,
            "ends_with_question": ends_with_question,
            "close_type": close_type,
        },
        "pacing": {
            "words_per_minute": wpm,
            "date_frequency_per_minute": date_freq,
            "avg_sentence_length": avg_sent_len,
        },
    }


def run_analysis():
    """Analyze all downloaded transcripts."""
    total_analyzed = 0
    total_skipped = 0

    for channel_key in CHANNELS:
        display = CHANNEL_DISPLAY[channel_key]
        json_path = RAW_DIR / f"{channel_key}.json"
        if not json_path.exists():
            continue

        with open(json_path, encoding="utf-8") as f:
            data = json.load(f)

        # Top 10 by views
        videos = sorted(data.get("all_videos", []), key=lambda v: v.get("view_count", 0), reverse=True)[:10]
        vid_map = {v["id"]: v for v in videos}

        channel_dir = TRANSCRIPT_DIR / display
        if not channel_dir.exists():
            print(f"[SKIP] {display}: no transcript directory")
            continue

        print(f"\n[ANALYZE] {display}")
        for vid in videos:
            vid_id = vid["id"]
            analysis_path = channel_dir / f"{vid_id}_analysis.json"

            result = analyze_single(vid_id, display, channel_key, vid)
            if result:
                with open(analysis_path, "w", encoding="utf-8") as f:
                    json.dump(result, f, indent=2, ensure_ascii=False)
                print(f"  OK: {vid.get('title', vid_id)[:60]}")
                total_analyzed += 1
            else:
                print(f"  SKIP (no transcript): {vid.get('title', vid_id)[:60]}")
                total_skipped += 1

    print(f"\nANALYSIS COMPLETE: {total_analyzed} analyzed, {total_skipped} skipped")


# ==========================================================================
# REPORT
# ==========================================================================

def load_all_analyses() -> list[dict]:
    """Load all _analysis.json files."""
    results = []
    for channel_dir in sorted(TRANSCRIPT_DIR.iterdir()):
        if not channel_dir.is_dir():
            continue
        for f in sorted(channel_dir.glob("*_analysis.json")):
            with open(f, encoding="utf-8") as fh:
                results.append(json.load(fh))
    return results


def load_channel_metadata() -> dict:
    """Load subscriber counts from raw_data."""
    meta = {}
    for channel_key in CHANNELS:
        json_path = RAW_DIR / f"{channel_key}.json"
        if json_path.exists():
            with open(json_path, encoding="utf-8") as f:
                data = json.load(f)
            display = CHANNEL_DISPLAY[channel_key]
            # Get subscriber count from first video's metadata
            vids = data.get("all_videos", [])
            sub_count = vids[0].get("channel_subscriber_count", 0) if vids else 0
            median_views = data.get("median_views", 0)
            meta[display] = {"subscribers": sub_count, "median_views": median_views}
    return meta


def safe_median(values):
    return round(statistics.median(values), 1) if values else 0


def safe_mean(values):
    return round(statistics.mean(values), 1) if values else 0


def correlation(xs, ys):
    """Pearson correlation coefficient."""
    if len(xs) < 5 or len(ys) < 5:
        return None
    n = len(xs)
    mx, my = statistics.mean(xs), statistics.mean(ys)
    sx = math.sqrt(sum((x - mx)**2 for x in xs) / n)
    sy = math.sqrt(sum((y - my)**2 for y in ys) / n)
    if sx == 0 or sy == 0:
        return None
    cov = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / n
    return round(cov / (sx * sy), 3)


def generate_report():
    """Generate aggregate markdown report."""
    analyses = load_all_analyses()
    if not analyses:
        print("No analyses found. Run --analyze first.")
        return

    channel_meta = load_channel_metadata()
    print(f"Loaded {len(analyses)} video analyses across {len(set(a['channel'] for a in analyses))} channels")

    # Group by channel
    by_channel = defaultdict(list)
    for a in analyses:
        by_channel[a["channel"]].append(a)

    lines = []
    lines.append("# Competitor Transcript Structure Analysis")
    lines.append("")
    lines.append(f"**Generated:** 2026-03-23 | **Videos analyzed:** {len(analyses)} | "
                 f"**Channels:** {len(by_channel)}")
    lines.append("")
    lines.append("---")
    lines.append("")

    # ---- Section 1: Per-channel profiles ----
    lines.append("## 1. Per-Channel Structural Profiles")
    lines.append("")

    for ch_name in sorted(by_channel.keys()):
        vids = by_channel[ch_name]
        meta = channel_meta.get(ch_name, {})
        subs = meta.get("subscribers", 0)

        hook_types = Counter(v["hook"]["hook_type"] for v in vids)
        structures = Counter(v["structure"]["chronological_vs_thematic"] for v in vids)
        close_types = Counter(v["close"]["close_type"] for v in vids)

        date_times = [v["hook"]["seconds_to_first_date"] for v in vids if v["hook"]["seconds_to_first_date"] is not None]
        turn_times = [v["structure"]["seconds_to_turn_moment"] for v in vids if v["structure"]["seconds_to_turn_moment"] is not None]
        turn_pcts = []
        for v in vids:
            if v["structure"]["seconds_to_turn_moment"] and v["duration_seconds"] > 0:
                turn_pcts.append(round(v["structure"]["seconds_to_turn_moment"] / v["duration_seconds"] * 100, 1))

        citations = [v["structure"]["explicit_source_citations"] for v in vids]
        wpms = [v["pacing"]["words_per_minute"] for v in vids]

        lines.append(f"### {ch_name}")
        lines.append(f"- **Subscribers:** {subs:,}" if subs else "- **Subscribers:** unknown")
        lines.append(f"- **Videos analyzed:** {len(vids)}")
        lines.append(f"- **Avg duration:** {safe_mean([v['duration_seconds'] for v in vids]):.0f}s "
                     f"({safe_mean([v['duration_seconds'] for v in vids])/60:.1f} min)")
        lines.append(f"- **Avg WPM:** {safe_mean(wpms)}")
        lines.append(f"- **Hook types:** {dict(hook_types.most_common())}")
        lines.append(f"- **Structure:** {dict(structures.most_common())}")
        lines.append(f"- **Close types:** {dict(close_types.most_common())}")
        lines.append(f"- **Avg time to first date:** {safe_mean(date_times):.1f}s" if date_times else "- **Avg time to first date:** N/A")
        lines.append(f"- **Avg time to turn:** {safe_mean(turn_times):.0f}s ({safe_mean(turn_pcts):.1f}% of runtime)" if turn_times else "- **Avg time to turn:** not detected")
        lines.append(f"- **Avg source citations:** {safe_mean(citations)}")
        lines.append(f"- **Avg documents mentioned:** {safe_mean([v['structure']['documents_mentioned'] for v in vids])}")
        lines.append("")

        # Best hook example
        top_vid = max(vids, key=lambda v: v["views"])
        lines.append(f"  **Top video hook** ({top_vid['views']:,} views): *{top_vid['title'][:70]}*")
        lines.append(f"  > {top_vid['hook']['first_sentence'][:200]}")
        lines.append("")

    # ---- Section 2: Cross-channel outlier analysis ----
    lines.append("---")
    lines.append("")
    lines.append("## 2. What Outlier Videos Do Differently")
    lines.append("")
    lines.append("Comparing top-quartile vs bottom-quartile videos *within each channel* "
                 "(normalized by channel median views).")
    lines.append("")

    # Split each channel's videos into top/bottom half by view ratio
    top_q = []
    bottom_q = []
    for ch_name, vids in by_channel.items():
        if len(vids) < 4:
            continue
        sorted_vids = sorted(vids, key=lambda v: v["views"], reverse=True)
        mid = len(sorted_vids) // 2
        top_q.extend(sorted_vids[:mid])
        bottom_q.extend(sorted_vids[mid:])

    if top_q and bottom_q:
        def compare_metric(label, extract, fmt=".1f"):
            top_vals = [extract(v) for v in top_q if extract(v) is not None]
            bot_vals = [extract(v) for v in bottom_q if extract(v) is not None]
            if top_vals and bot_vals:
                t = safe_mean(top_vals)
                b = safe_mean(bot_vals)
                diff = t - b
                sign = "+" if diff > 0 else ""
                lines.append(f"| {label} | {format(t, fmt)} | {format(b, fmt)} | {sign}{format(diff, fmt)} |")

        lines.append("| Metric | Top half | Bottom half | Delta |")
        lines.append("|--------|----------|-------------|-------|")
        compare_metric("WPM", lambda v: v["pacing"]["words_per_minute"])
        compare_metric("Time to first date (s)", lambda v: v["hook"]["seconds_to_first_date"])
        compare_metric("Time to turn (s)", lambda v: v["structure"]["seconds_to_turn_moment"])
        compare_metric("Turn % of runtime", lambda v: (v["structure"]["seconds_to_turn_moment"] / v["duration_seconds"] * 100) if v["structure"]["seconds_to_turn_moment"] and v["duration_seconds"] > 0 else None)
        compare_metric("Source citations", lambda v: v["structure"]["explicit_source_citations"])
        compare_metric("Documents mentioned", lambda v: v["structure"]["documents_mentioned"])
        compare_metric("Questions posed", lambda v: v["structure"]["questions_posed_to_viewer"])
        compare_metric("Avg sentence length", lambda v: v["pacing"]["avg_sentence_length"])
        compare_metric("% history vs analysis", lambda v: v["structure"]["percent_history_vs_analysis"])
        compare_metric("Date frequency/min", lambda v: v["pacing"]["date_frequency_per_minute"])
        lines.append("")

    # ---- Section 3: Hook type distribution ----
    lines.append("---")
    lines.append("")
    lines.append("## 3. Hook Type Distribution & View Correlation")
    lines.append("")

    hook_groups = defaultdict(list)
    for a in analyses:
        hook_groups[a["hook"]["hook_type"]].append(a)

    lines.append("| Hook Type | Count | Avg Views | Avg Normalized Views | Example |")
    lines.append("|-----------|-------|-----------|---------------------|---------|")

    for ht in ["cold_fact", "myth_contradiction", "specificity_bomb", "contextual_opening"]:
        vids = hook_groups.get(ht, [])
        if not vids:
            lines.append(f"| {ht} | 0 | — | — | — |")
            continue
        avg_views = safe_mean([v["views"] for v in vids])
        # Normalize: views / channel subscriber count
        norm_views = []
        for v in vids:
            subs = channel_meta.get(v["channel"], {}).get("subscribers", 1) or 1
            norm_views.append(v["views"] / subs)
        avg_norm = safe_mean(norm_views)
        example = max(vids, key=lambda v: v["views"])
        lines.append(f"| {ht} | {len(vids)} | {avg_views:,.0f} | {avg_norm:.1f}x subs | {example['title'][:50]} |")

    lines.append("")

    # ---- Section 4: Opening word patterns ----
    lines.append("---")
    lines.append("")
    lines.append("## 4. Opening Word Patterns: Top vs Bottom Quartile")
    lines.append("")

    if top_q and bottom_q:
        def first_words(vids, label):
            lines.append(f"**{label} ({len(vids)} videos):**")
            lines.append("")
            # Collect first sentences
            for v in sorted(vids, key=lambda x: x["views"], reverse=True)[:10]:
                views = v["views"]
                lines.append(f"- ({views:,} views) *\"{v['hook']['first_sentence'][:150]}\"*")
            lines.append("")

        first_words(top_q, "Top half openers")
        first_words(bottom_q, "Bottom half openers")

        # Word frequency analysis
        def word_freq(vids):
            words = Counter()
            for v in vids:
                for w in v["hook"]["first_50_words"].lower().split():
                    w = re.sub(r'[^a-z]', '', w)
                    if w and len(w) > 2:
                        words[w] += 1
            return words

        top_words = word_freq(top_q)
        bot_words = word_freq(bottom_q)

        # Find words disproportionately in top vs bottom
        lines.append("**Distinctive opening words (top half vs bottom half):**")
        lines.append("")
        all_words = set(top_words.keys()) | set(bot_words.keys())
        ratios = []
        for w in all_words:
            t = top_words.get(w, 0) / max(len(top_q), 1)
            b = bot_words.get(w, 0) / max(len(bottom_q), 1)
            if t > 0.15 and t > b * 1.5:
                ratios.append((w, t, b, t / max(b, 0.01)))
        ratios.sort(key=lambda x: x[3], reverse=True)
        for w, t, b, r in ratios[:10]:
            lines.append(f"- **\"{w}\"**: {t:.0%} of top openers vs {b:.0%} of bottom ({r:.1f}x)")
        lines.append("")

    # ---- Section 5: Correlations ----
    lines.append("---")
    lines.append("")
    lines.append("## 5. Structural Correlations with Views")
    lines.append("")
    lines.append("Views normalized by channel subscriber count to enable cross-channel comparison.")
    lines.append("")

    norm_views = []
    for a in analyses:
        subs = channel_meta.get(a["channel"], {}).get("subscribers", 1) or 1
        norm_views.append(a["views"] / subs)

    correlations = []

    def add_corr(label, extractor):
        vals = [(extractor(a), nv) for a, nv in zip(analyses, norm_views) if extractor(a) is not None]
        if len(vals) >= 10:
            xs, ys = zip(*vals)
            r = correlation(list(xs), list(ys))
            if r is not None:
                correlations.append((label, r, len(vals)))

    add_corr("Time to first date (s)", lambda a: a["hook"]["seconds_to_first_date"])
    add_corr("Time to first entity (s)", lambda a: a["hook"]["seconds_to_first_named_entity"])
    add_corr("Time to turn (s)", lambda a: a["structure"]["seconds_to_turn_moment"])
    add_corr("Turn % of runtime", lambda a: (a["structure"]["seconds_to_turn_moment"] / a["duration_seconds"] * 100) if a["structure"]["seconds_to_turn_moment"] and a["duration_seconds"] > 0 else None)
    add_corr("WPM", lambda a: a["pacing"]["words_per_minute"])
    add_corr("Source citations", lambda a: a["structure"]["explicit_source_citations"])
    add_corr("Documents mentioned", lambda a: a["structure"]["documents_mentioned"])
    add_corr("Questions posed", lambda a: a["structure"]["questions_posed_to_viewer"])
    add_corr("Avg sentence length", lambda a: a["pacing"]["avg_sentence_length"])
    add_corr("Date frequency/min", lambda a: a["pacing"]["date_frequency_per_minute"])
    add_corr("% history content", lambda a: a["structure"]["percent_history_vs_analysis"])
    add_corr("Duration (s)", lambda a: a["duration_seconds"])

    correlations.sort(key=lambda x: abs(x[1]), reverse=True)

    lines.append("| Metric | r (Pearson) | n | Interpretation |")
    lines.append("|--------|-------------|---|----------------|")
    for label, r, n in correlations:
        if abs(r) >= 0.3:
            interp = "**STRONG**" if abs(r) >= 0.5 else "**MODERATE**"
        elif abs(r) >= 0.15:
            interp = "Weak"
        else:
            interp = "None"
        direction = "+" if r > 0 else "-" if r < 0 else "~"
        lines.append(f"| {label} | {r:+.3f} | {n} | {interp} ({direction}) |")
    lines.append("")

    # ---- Section 6: Turn moment placement ----
    lines.append("---")
    lines.append("")
    lines.append("## 6. Turn Moment Placement")
    lines.append("")

    turn_data = [(a, a["structure"]["seconds_to_turn_moment"] / a["duration_seconds"] * 100)
                 for a in analyses
                 if a["structure"]["seconds_to_turn_moment"] and a["duration_seconds"] > 0]

    if turn_data:
        lines.append(f"**Detected turns in {len(turn_data)}/{len(analyses)} videos.**")
        lines.append("")

        # Bucket by placement
        buckets = {"15-25%": [], "25-35%": [], "35-45%": [], "45-55%": [], "55%+": []}
        for a, pct in turn_data:
            if pct < 25:
                buckets["15-25%"].append(a)
            elif pct < 35:
                buckets["25-35%"].append(a)
            elif pct < 45:
                buckets["35-45%"].append(a)
            elif pct < 55:
                buckets["45-55%"].append(a)
            else:
                buckets["55%+"].append(a)

        lines.append("| Placement | Count | Avg Norm Views | Example Turn |")
        lines.append("|-----------|-------|---------------|-------------|")
        for bucket, vids in buckets.items():
            if not vids:
                lines.append(f"| {bucket} | 0 | — | — |")
                continue
            nvs = []
            for v in vids:
                subs = channel_meta.get(v["channel"], {}).get("subscribers", 1) or 1
                nvs.append(v["views"] / subs)
            avg_nv = safe_mean(nvs)
            ex = max(vids, key=lambda v: v["views"])
            turn_text = (ex["structure"]["turn_moment_description"] or "")[:80]
            lines.append(f"| {bucket} | {len(vids)} | {avg_nv:.1f}x | \"{turn_text}\" |")
        lines.append("")

        # Best turn examples
        lines.append("**Notable turn moments (from highest-viewed videos):**")
        lines.append("")
        for a, pct in sorted(turn_data, key=lambda x: x[0]["views"], reverse=True)[:8]:
            lines.append(f"- **{a['title'][:60]}** ({a['views']:,} views, turn at {pct:.0f}%)")
            lines.append(f"  > \"{a['structure']['turn_moment_description'][:150]}\"")
        lines.append("")

    # ---- Section 7: Close type distribution ----
    lines.append("---")
    lines.append("")
    lines.append("## 7. Close Type Distribution")
    lines.append("")

    close_groups = defaultdict(list)
    for a in analyses:
        close_groups[a["close"]["close_type"]].append(a)

    lines.append("| Close Type | Count | % | Avg Norm Views | Has CTA % | Example |")
    lines.append("|------------|-------|---|---------------|-----------|---------|")
    for ct in ["open_question", "prediction", "human_cost", "pattern_reveal", "boilerplate"]:
        vids = close_groups.get(ct, [])
        if not vids:
            continue
        pct = round(len(vids) / len(analyses) * 100, 1)
        nvs = []
        for v in vids:
            subs = channel_meta.get(v["channel"], {}).get("subscribers", 1) or 1
            nvs.append(v["views"] / subs)
        cta_pct = round(sum(1 for v in vids if v["close"]["has_cta"]) / len(vids) * 100, 1)
        ex = max(vids, key=lambda v: v["views"])
        lines.append(f"| {ct} | {len(vids)} | {pct}% | {safe_mean(nvs):.1f}x | {cta_pct}% | {ex['title'][:40]} |")
    lines.append("")

    # ---- Section 8: Actionable rules ----
    lines.append("---")
    lines.append("")
    lines.append("## 8. Actionable Rules for script-writer-v2")
    lines.append("")
    lines.append("*Only rules with n >= 10 support.*")
    lines.append("")

    rules = []

    # Rule: Hook type
    for ht, vids in hook_groups.items():
        if len(vids) >= 10:
            nvs = []
            for v in vids:
                subs = channel_meta.get(v["channel"], {}).get("subscribers", 1) or 1
                nvs.append(v["views"] / subs)
            rules.append((ht, len(vids), safe_mean(nvs)))

    if rules:
        rules.sort(key=lambda x: x[2], reverse=True)
        lines.append("### Hook types by performance")
        lines.append("")
        for ht, n, avg_nv in rules:
            lines.append(f"- **{ht}** (n={n}): {avg_nv:.1f}x subscriber count avg views")
        lines.append("")

    # Rule: Time to first date
    date_vals = [a["hook"]["seconds_to_first_date"] for a in analyses if a["hook"]["seconds_to_first_date"] is not None]
    if len(date_vals) >= 10:
        lines.append(f"### Time to first date")
        lines.append(f"- Median: {safe_median(date_vals):.0f}s | Mean: {safe_mean(date_vals):.0f}s")
        lines.append(f"- **RULE:** Introduce a specific date or number within the first {safe_median(date_vals):.0f} seconds to anchor the viewer.")
        lines.append("")

    # Rule: Turn moment
    if len(turn_data) >= 10:
        turn_pcts_all = [pct for _, pct in turn_data]
        lines.append(f"### Turn moment placement")
        lines.append(f"- Median: {safe_median(turn_pcts_all):.0f}% of runtime | Mean: {safe_mean(turn_pcts_all):.0f}%")
        lines.append(f"- **RULE:** Place the narrative turn (reframe, hidden actor, irony) at {safe_median(turn_pcts_all):.0f}-{safe_mean(turn_pcts_all):.0f}% of the video.")
        lines.append("")

    # Rule: Source citations
    cite_vals = [a["structure"]["explicit_source_citations"] for a in analyses]
    if len(cite_vals) >= 10:
        top_cite = [a["structure"]["explicit_source_citations"] for a in top_q] if top_q else []
        bot_cite = [a["structure"]["explicit_source_citations"] for a in bottom_q] if bottom_q else []
        lines.append(f"### Source citations")
        lines.append(f"- Overall median: {safe_median(cite_vals)}")
        if top_cite and bot_cite:
            lines.append(f"- Top half avg: {safe_mean(top_cite)} vs bottom half: {safe_mean(bot_cite)}")
        lines.append("")

    # Rule: Close type
    cta_rate = sum(1 for a in analyses if a["close"]["has_cta"]) / max(len(analyses), 1)
    lines.append(f"### Close patterns")
    lines.append(f"- CTA rate across niche: {cta_rate:.0%}")
    lines.append(f"- Most common close: {Counter(a['close']['close_type'] for a in analyses).most_common(1)[0][0]}")
    lines.append("")

    # Rule: Structure type
    struct_dist = Counter(a["structure"]["chronological_vs_thematic"] for a in analyses)
    lines.append(f"### Narrative structure")
    lines.append(f"- Distribution: {dict(struct_dist.most_common())}")
    lines.append("")

    # Rule: WPM
    all_wpms = [a["pacing"]["words_per_minute"] for a in analyses if a["pacing"]["words_per_minute"] > 0]
    if len(all_wpms) >= 10:
        lines.append(f"### Pacing")
        lines.append(f"- Niche WPM range: {min(all_wpms):.0f}-{max(all_wpms):.0f} | Median: {safe_median(all_wpms):.0f}")
        lines.append("")

    # Rule: Questions
    q_vals = [a["structure"]["questions_posed_to_viewer"] for a in analyses]
    if len(q_vals) >= 10:
        lines.append(f"### Questions to viewer")
        lines.append(f"- Median: {safe_median(q_vals):.0f} per video | Mean: {safe_mean(q_vals):.0f}")
        dur_mins = [a["duration_seconds"]/60 for a in analyses if a["duration_seconds"] > 0]
        q_per_min = [q/d for q, d in zip(q_vals, dur_mins) if d > 0]
        if q_per_min:
            lines.append(f"- Per minute: {safe_mean(q_per_min):.2f}")
        lines.append("")

    # ---- Section 9: Example hooks by type ----
    lines.append("---")
    lines.append("")
    lines.append("## 9. Example Hooks by Type (From Transcripts)")
    lines.append("")

    for ht in ["cold_fact", "myth_contradiction", "specificity_bomb", "contextual_opening"]:
        vids = hook_groups.get(ht, [])
        if not vids:
            continue
        lines.append(f"### {ht} ({len(vids)} videos)")
        lines.append("")
        for v in sorted(vids, key=lambda x: x["views"], reverse=True)[:5]:
            lines.append(f"**{v['channel']}** — *{v['title'][:60]}* ({v['views']:,} views)")
            lines.append(f"> {v['hook']['first_sentence'][:300]}")
            lines.append("")

    # ---- Appendix: All video data ----
    lines.append("---")
    lines.append("")
    lines.append("## Appendix: All Analyzed Videos")
    lines.append("")
    lines.append("| Channel | Title | Views | Hook | Turn (%) | Close | WPM |")
    lines.append("|---------|-------|-------|------|----------|-------|-----|")

    for a in sorted(analyses, key=lambda x: x["views"], reverse=True):
        turn_pct = ""
        if a["structure"]["seconds_to_turn_moment"] and a["duration_seconds"] > 0:
            turn_pct = f"{a['structure']['seconds_to_turn_moment']/a['duration_seconds']*100:.0f}%"
        lines.append(
            f"| {a['channel']} | {a['title'][:40]} | {a['views']:,} | {a['hook']['hook_type']} | "
            f"{turn_pct} | {a['close']['close_type']} | {a['pacing']['words_per_minute']:.0f} |"
        )
    lines.append("")

    report = "\n".join(lines)
    REPORT_PATH.write_text(report, encoding="utf-8")
    print(f"\nReport written to {REPORT_PATH} ({len(lines)} lines)")


# ==========================================================================
# MAIN
# ==========================================================================

def main():
    parser = argparse.ArgumentParser(description="Competitor transcript structure analyzer")
    parser.add_argument("--fetch", action="store_true", help="Download transcripts (slow, rate-limited)")
    parser.add_argument("--analyze", action="store_true", help="Analyze transcripts into per-video JSONs")
    parser.add_argument("--report", action="store_true", help="Generate aggregate markdown report")
    args = parser.parse_args()

    if not any([args.fetch, args.analyze, args.report]):
        parser.print_help()
        return

    if args.fetch:
        fetch_transcripts()
    if args.analyze:
        run_analysis()
    if args.report:
        generate_report()


if __name__ == "__main__":
    main()
