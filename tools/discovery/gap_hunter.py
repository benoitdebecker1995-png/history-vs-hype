"""
gap_hunter.py — sweep competitor comment sections for demand nobody is serving.

Every other discovery tool in this repo SCORES a candidate you already have
(`/greenlight --scan`, `packaging_intel.get_topic_viability`, `serp_title_study`,
`TOPIC-RUBRIC`). This one runs the inversion: it takes no topic as input and
GENERATES candidates by sweeping the tracked competitor set for questions the
shelf isn't answering.

Why comments and not search volume: search is ~5% of this channel's traffic, so
keyword volume is the wrong demand proxy (`channel-data/BREAKOUT-MECHANICS-2026-07.md`).
The one demand pocket the channel ever found (Panama) was found by comment-mining
1,711 comments — comment sections are the only signal that simultaneously proves
an audience exists (likes), proves supply is missing ("he skips the important
part"), and identifies the pocket ("as a Panamanian…").

Pipeline (spec: `channel-data/NEXT-VIDEO-DISCOVERY-HANDOFF.md` §5):
    Stage 1  harvest  — this module: fetch + tag + store comment signals
    Stage 2  cluster  — this module: likes-weighted term aggregation → digest
    Stage 3  supply   — existing `tools/preflight/serp_title_study.py`, per candidate
    Stage 4  identity — human/model judgment. Deliberately NOT automated.

⚠ HONESTY GUARD: this finds CANDIDATES, not winners. Serve size is not predictable
from anything this repo can measure (four predictors tested and killed, 2026-07-28).
The rank column informs; it never decides. Per ADR-0012, only filters decide.

Usage:
    CLI:
        python -m tools.discovery.gap_hunter --sweep --videos 40 --comments 200
        python -m tools.discovery.gap_hunter --digest
        python -m tools.discovery.gap_hunter --sweep --dry-run

    Python:
        from tools.discovery.gap_hunter import tag_comment, aggregate_signals
"""

import argparse
import json
import math
import re
import statistics
import sys
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

from tools.intel.kb_store import KBStore
from tools.logging_config import get_logger
from tools.youtube_analytics.comments import fetch_video_comments

logger = get_logger(__name__)

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DIGEST_PATH = REPO_ROOT / "channel-data" / "gap-hunter" / "HARVEST-DIGEST.md"

# ---------------------------------------------------------------------------
# Stage 1 — the signal taxonomy
# ---------------------------------------------------------------------------
# Three patterns, from the handoff. Kept as explicit phrase lists rather than
# a classifier: the phrases ARE the evidence, and they get quoted in the digest.

UNMET_SUPPLY_PATTERNS = [
    r"\bskip(?:s|ped|ping)\b", r"\bglosse[sd]? over\b", r"\bleft out\b",
    r"\bleaves out\b", r"\bdoesn'?t (?:mention|cover|explain|talk about)\b",
    r"\bdidn'?t (?:mention|cover|explain|talk about)\b",
    r"\bnever (?:mention|mentions|mentioned|explained|explains)\b",
    r"\bno ?(?:one|body) (?:ever )?(?:talks about|mentions|covers|explains)\b",
    r"\bnot enough people (?:know|talk)\b",
    r"\bwish (?:someone|somebody|a channel|you)\b",
    r"\b(?:would|i'?d) love (?:a|an|to see a) (?:video|documentary|deep ?dive)\b",
    r"\bplease (?:do|make|cover)\b", r"\byou should (?:do|make|cover)\b",
    r"\bdeserves? (?:its|it'?s|a|an) own (?:video|episode)\b",
    r"\bneeds? (?:its|it'?s) own (?:video|episode)\b",
    r"\black(?:s|ing)\b", r"\bmissing (?:a lot|the|some|key|important)\b",
    r"\bbarely (?:touche[sd]|scratche[sd]|mention)\b",
    r"\b(?:gets?|got) (?:this|it|that) wrong\b",
    r"\bnobody (?:explains|shows|talks)\b",
    r"\bwhat (?:actually|really) happened\b",
    r"\bthere'?s (?:more|much more) to (?:this|the) story\b",
]

# Pocket = a self-identifying national/diaspora voice. These are the comments
# that proved the Panama audience watches its own history in English.
POCKET_PATTERNS = [
    r"\b[Aa]s an? [A-Z][a-z]{3,}\b",        # "As a Panamanian…" — the demonym's capital is the signal
    r"\b[Aa]s someone (?:from|who lives in|born in)\b",
    r"\b(?:[Ii]'?m|[Ii] am|[Ii]m) (?:from|a) [A-Z][a-z]{3,}\b",
    r"\b[Mm]y (?:country|homeland|grandfather|grandmother|family|people)\b",
    r"\b[Hh]ere in [A-Z][a-z]{3,}\b",
    r"\b[Ii]n my country\b", r"\b[Ww]e (?:were|are) taught\b",
    r"\b[Nn]ever expected (?:to see|a video)\b",
    r"\b(?:[Rr]are|[Nn]ice|[Gg]reat) to see (?:a )?(?:video|content) about\b",
    r"\b[Ff]inally (?:someone|a video)\b",
    r"\b[Gg]reetings from\b", r"\b[Ll]ove from\b",
]

# ---------------------------------------------------------------------------
# The BARRIER axis (added 2026-07-29 after the owner interview)
# ---------------------------------------------------------------------------
# The channel's subject is ACCESS to the historical record. Four things block
# access, and WHICH ONE carries breakout demand is an open question — the owner
# explicitly declined to pre-commit and asked the sweep to answer it. So every
# signal comment gets tagged with the barrier it implies, and the digest ranks
# barriers the same way it ranks topics.
#
#   enclosure — "historians settled this and nobody told me"
#   language  — "the evidence isn't in English"
#   ideology  — "I was taught a story that turns out to be invented"
#   archive   — "there's a document and nobody has looked at it"
#   method    — "how do you actually know that?"  (the method-visibility fork)

DEMAND_PATTERNS: dict[str, list[str]] = {
    # ⚠ TIGHTENED 2026-07-29 after a false-positive audit of the first run.
    # "never heard" / "had no idea" / "mind blowing" are ordinary English idiom
    # ("I've never heard the narrator this angry", 14,865 likes) and they swamped
    # the class with jokes, inflating its like-average. Every pattern here must
    # encode WITHHELD KNOWLEDGE — schooling, curriculum, or access to scholarship
    # — not mere surprise.
    "enclosure": [
        r"\bnever (?:taught|been taught|learn(?:ed|t))\b",
        r"\b(?:don'?t|didn'?t|doesn'?t|won'?t) teach (?:this|that|us|you|any of this)\b",
        r"\bwhy (?:don'?t|didn'?t|isn'?t|wasn'?t)[^.?!]{0,40}\b(?:taught|teach)\b",
        r"\bnot taught in (?:school|schools|history class|university)\b",
        r"\b(?:should|ought to) be taught\b",
        r"\bin (?:my|our) (?:history )?(?:class|classes|textbook|textbooks|curriculum)\b",
        r"\btext ?books? (?:never|didn'?t|don'?t|leave|left|omit)\b",
        r"\bhow (?:did|do) i not know\b",
        r"\bwhy (?:did|does|do) (?:nobody|no one|nobody ever)[^.?!]{0,20}\btell\b",
        r"\bTIL\b",
        r"\b(?:history|classics|archaeolog\w*|medieval|ancient history) (?:degree|major|phd|postgrad)\b",
        r"\b(?:what|which) (?:book|books|papers?|sources?) (?:should i|can i|would you|do you recommend)\b",
        r"\bwhere can i (?:read|learn|find) (?:more|about)\b", r"\breading list\b",
        r"\bpaywall(?:ed)?\b", r"\bjstor\b", r"\bacademic (?:paper|article|journal|consensus)\b",
        r"\bpeer[- ]reviewed (?:paper|article|literature)\b",
    ],
    "language": [
        r"\bmistranslat", r"\btranslat(?:ion|ed|ing|e)\b",
        r"\bthe original (?:text|language|word|document|source)\b",
        r"\bin (?:the )?(?:original )?(?:latin|greek|arabic|hebrew|russian|german|french|spanish|dutch|polish|ukrainian|chinese|japanese|turkish|persian|portuguese|italian)\b",
        r"\bnot (?:available )?in english\b", r"\bonly (?:available )?in [A-Z][a-z]{3,}\b",
        r"\bno english (?:source|version|translation|coverage)\b",
        r"\bin my language\b", r"\bthe word (?:actually |literally )?means\b",
        r"\bnative speaker\b", r"\bspeak(?:s)? [A-Z][a-z]{3,} (?:and|so)\b",
    ],
    # ⚠ TIGHTENED 2026-07-29 in the same audit. Bare "narrative", "myth", "bias",
    # "agenda" and "textbooks" are how every comment section talks and inflated
    # this class into first place by sheer frequency. Kept patterns name a
    # DISTORTION OF THE RECORD, not a disagreement.
    "ideology": [
        r"\bpropaganda\b",
        r"\b(?:we|i) (?:were|was) taught\b", r"\bschool taught (?:me|us)\b",
        r"\brevisionis[tm]", r"\bwhitewash", r"\bbrainwash",
        r"\bnationalist (?:myth|propaganda|history|version)\b",
        r"\b(?:it'?s|that'?s|this is) (?:a |just a |literally a )?myth\b",
        r"\bmyth (?:that|of the|persists|invented)\b",
        r"\bhistory is written by\b", r"\bdenial(?:ism|ist)\b",
        r"\bpseudo[- ]?(?:history|histor\w+|archaeolog\w+|science)\b",
        r"\blost cause (?:myth|narrative|ideology)\b",
        r"\b(?:they|he|she|the government|the state) lied\b",
        r"\brewriting history\b", r"\berasing (?:our|its own|their) history\b",
    ],
    "archive": [
        r"\barchives?\b", r"\bdeclassified\b", r"\bprimary sources?\b",
        r"\bthe (?:actual|original) document\b", r"\bmanuscripts?\b",
        r"\bunpublished\b", r"\bdigiti[sz]ed\b", r"\brecords? (?:show|exist|were)\b",
        r"\bfoia\b", r"\bnational archives\b",
    ],
    "method": [
        r"\bhow do (?:we|you|they|historians|we actually) know\b",
        r"\bwhat'?s? (?:your|the) (?:source|evidence|citation)\b",
        r"\bsources?\?", r"\bcitations?\b", r"\bpeer[- ]review",
        r"\bhow (?:reliable|accurate) (?:is|are)\b",
        r"\bhistorians? (?:disagree|debate|argue)\b", r"\bhistoriograph",
        r"\bconsensus\b", r"\bevidence for (?:this|that)\b",
    ],
}

_DEMAND_RES = {k: [re.compile(p, re.IGNORECASE) for p in v] for k, v in DEMAND_PATTERNS.items()}


def classify_demand(text: str) -> list[str]:
    """
    Tag which access barrier a comment implies. Pure function.

    A comment can hit several ("we were taught the Latin says X" = ideology +
    language). Returns [] when none fire.
    """
    if not text or len(text.strip()) < MIN_SIGNAL_CHARS:
        return []
    return [name for name, regexes in _DEMAND_RES.items()
            if any(rx.search(text) for rx in regexes)]


QUESTION_WORDS = r"(?:what|why|how|when|where|who|which|did|does|do|was|were|is|are|can|could|would|should)"
_QUESTION_RE = re.compile(rf"\b{QUESTION_WORDS}\b[^?]{{10,}}\?", re.IGNORECASE)

_UNMET_RES = [re.compile(p, re.IGNORECASE) for p in UNMET_SUPPLY_PATTERNS]
_POCKET_RES = [re.compile(p) for p in POCKET_PATTERNS]  # case-sensitive: needs the capital

MIN_SIGNAL_CHARS = 40  # "great video!" is not a signal


def tag_comment(text: str) -> tuple[list[str], list[str]]:
    """
    Tag one comment against the three signal patterns.

    Pure function — no I/O. This is the unit the tests pin.

    Args:
        text: Raw comment text

    Returns:
        (patterns, matched_phrases) — patterns is a subset of
        ['unmet_supply', 'pocket', 'question']; matched_phrases holds the actual
        substrings that fired, so the digest can quote the evidence.
        Both empty when the comment carries no signal.
    """
    if not text or len(text.strip()) < MIN_SIGNAL_CHARS:
        return [], []

    patterns: list[str] = []
    matched: list[str] = []

    for rx in _UNMET_RES:
        m = rx.search(text)
        if m:
            patterns.append("unmet_supply")
            matched.append(m.group(0))
            break

    for rx in _POCKET_RES:
        m = rx.search(text)
        if m:
            patterns.append("pocket")
            matched.append(m.group(0))
            break

    qm = _QUESTION_RE.search(text)
    if qm:
        patterns.append("question")
        matched.append(qm.group(0)[:120])

    return patterns, matched


# ---------------------------------------------------------------------------
# Stage 1 — seed selection + sweep
# ---------------------------------------------------------------------------

def select_seed_videos(
    store: KBStore,
    limit: int = 40,
    min_views: int = 50_000,
    published_after: str | None = None,
    skip_swept: bool = True,
) -> list[dict]:
    """
    Choose which competitor videos to mine, highest outlier_ratio first.

    High-performing recent videos are where an engaged audience actually is —
    a comment thread on a 300-view video proves nothing about demand.

    Args:
        store:           KBStore over intel.db
        limit:           Max videos to return
        min_views:       View floor
        published_after: ISO date string; defaults to 24 months ago
        skip_swept:      Exclude videos already in comment_sweeps

    Returns:
        List of dicts (video_id, channel_id, channel_name, title, views,
        outlier_ratio, published_at); [] on error.
    """
    if published_after is None:
        published_after = (datetime.now(timezone.utc) - timedelta(days=730)).strftime("%Y-%m-%d")

    try:
        conn = store._connect()
        rows = conn.execute(
            """SELECT v.video_id, v.channel_id, c.channel_name, v.title, v.views,
                      v.outlier_ratio, v.published_at, v.duration_seconds
               FROM competitor_videos v
               LEFT JOIN competitor_channels c ON c.channel_id = v.channel_id
               WHERE v.views >= ?
                 AND v.published_at >= ?
                 AND (v.duration_seconds IS NULL OR v.duration_seconds >= 180)
               ORDER BY COALESCE(v.outlier_ratio, 0) DESC, v.views DESC""",
            (min_views, published_after),
        ).fetchall()
        conn.close()
    except Exception as exc:  # read-side helper: never raise
        logger.error("select_seed_videos failed: %s", exc)
        return []

    swept = set(store.get_swept_video_ids()) if skip_swept else set()
    out = []
    for r in rows:
        if r["video_id"] in swept:
            continue
        out.append(dict(r))
        if len(out) >= limit:
            break
    return out


def sweep_videos(
    videos: list[dict],
    store: KBStore,
    max_comments: int = 200,
    dry_run: bool = False,
) -> dict:
    """
    Stage 1: fetch each video's comments, tag them, persist the signals.

    Uses the YouTube Data API (`comments.fetch_video_comments`), NOT yt-dlp —
    yt-dlp is bot-walled for comments on this machine.

    Args:
        videos:       Rows from select_seed_videos()
        store:        KBStore over intel.db
        max_comments: Comments per video (API returns relevance-ordered)
        dry_run:      Tag and count but write nothing

    Returns:
        {'videos_swept': N, 'comments_fetched': N, 'signals_found': N,
         'failures': [{'video_id':…, 'error':…}]}
    """
    totals = {"videos_swept": 0, "comments_fetched": 0, "signals_found": 0, "failures": []}

    for v in videos:
        vid = v["video_id"]
        comments = fetch_video_comments(vid, max_comments=max_comments)
        if isinstance(comments, dict) and "error" in comments:
            logger.warning("skip %s: %s", vid, comments["error"])
            totals["failures"].append({"video_id": vid, "error": comments["error"]})
            continue

        signals = []
        for c in comments:
            patterns, matched = tag_comment(c.get("text", ""))
            demand = classify_demand(c.get("text", ""))
            # Either axis qualifies: "why isn't this taught" carries no
            # unmet/pocket/question phrasing but is exactly the demand we're after.
            if not patterns and not demand:
                continue
            signals.append({
                "comment_id": c.get("comment_id") or f"{vid}:{len(signals)}",
                "video_id": vid,
                "channel_id": v.get("channel_id"),
                "author": c.get("author"),
                "text": c.get("text", "")[:2000],
                "likes": c.get("likes", 0),
                "reply_count": c.get("reply_count", 0),
                "published_at": c.get("published_at"),
                "patterns": patterns,
                "matched_phrases": matched,
                "demand_types": demand,
            })

        totals["videos_swept"] += 1
        totals["comments_fetched"] += len(comments)
        totals["signals_found"] += len(signals)
        logger.info("%s — %d comments, %d signals — %s",
                    vid, len(comments), len(signals), (v.get("title") or "")[:60])

        if dry_run:
            continue
        saved = store.save_comment_signals(signals)
        if "error" in saved:
            totals["failures"].append({"video_id": vid, "error": saved["error"]})
            continue
        store.record_comment_sweep(vid, v.get("channel_id"), len(comments), len(signals))

    return totals


# ---------------------------------------------------------------------------
# Stage 2 — cluster
# ---------------------------------------------------------------------------
# Mechanical clustering only: proper-noun n-grams, likes-weighted, cross-video
# counted. It narrows ~20k comments to ~30 terms and ~200 quotable comments.
# Turning those into a topic candidate is judgment work and stays with the reader.

_PROPER_NOUN_RE = re.compile(r"\b([A-Z][a-z]{2,}(?:[ -][A-Z][a-z]{2,}){0,2})\b")

# Words that pass the capitalisation test but carry no topic information.
_TERM_STOPLIST = {
    "the", "this", "that", "these", "those", "there", "then", "they", "them",
    "and", "but", "for", "not", "you", "your", "yours", "with", "what", "when",
    "where", "which", "who", "why", "how", "was", "were", "are", "his", "her",
    "him", "she", "its", "our", "out", "all", "also", "any", "can", "did",
    "does", "great", "good", "video", "videos", "youtube", "channel", "thanks",
    "thank", "please", "love", "well", "just", "like", "really", "actually",
    "history", "historical", "documentary", "content", "episode", "part",
    "edit", "sorry", "yeah", "yes", "lol", "haha", "god", "man", "people",
    "one", "two", "three", "first", "second", "last", "next", "still", "even",
    "some", "many", "most", "much", "more", "less", "very", "every", "never",
    "always", "would", "could", "should", "about", "after", "before", "because",
    "however", "though", "since", "while", "back", "made", "make", "take",
    "come", "know", "think", "want", "need", "look", "used", "using", "into",
    "over", "under", "same", "other", "another", "such", "than", "here",
    "today", "now", "new", "old", "long", "little", "big", "world", "war",
    "country", "countries", "government", "state", "states", "day", "year",
    "years", "time", "times", "point", "fact", "facts", "true", "truth",
    "example", "case", "way", "thing", "things", "lot", "bit", "sure",
    "interesting", "amazing", "excellent", "best", "better", "wrong", "right",
    "mr", "dr", "sir", "guy", "guys", "bro", "dude", "okay", "hey",
    "nobody", "everyone", "everybody", "someone", "somebody", "anyone",
    "watching", "watched", "subscribed", "comment", "comments", "algorithm",
}


def _extract_terms(text: str) -> set[str]:
    """
    Proper-noun phrases from one comment.

    Sentence-initial capitals mean a match often arrives glued to a stopword
    ("The Essequibo" in one comment, "Essequibo" in the next). Leading and
    trailing stopwords are stripped so the same topic clusters as one term, and
    multi-word phrases also contribute their informative component words so
    "Panama Canal" and "Panama" don't sit in separate buckets.
    """
    terms = set()
    for m in _PROPER_NOUN_RE.finditer(text):
        words = m.group(1).strip().split()

        while words and words[0].lower() in _TERM_STOPLIST:
            words.pop(0)
        while words and words[-1].lower() in _TERM_STOPLIST:
            words.pop()
        if not words:
            continue

        informative = [w for w in words if len(w) >= 4]
        if not informative:
            continue

        terms.add(" ".join(words))
        if len(words) > 1:
            terms.update(informative)
    return terms


def aggregate_barriers(signals: list[dict]) -> list[dict]:
    """
    Rank the access barriers by likes-weighted demand.

    This is the axis the owner asked the sweep to decide (2026-07-29): which
    kind of barrier — enclosure, language, ideology, archive, method — actually
    draws an audience, rather than which topic.

    `per_1k_comments` normalises by how many signals each barrier could have
    come from, because a barrier that fires rarely but pulls heavy likes is a
    different animal from one that fires constantly on cheap comments.

    Returns one row per barrier, sorted by weight desc; [] when nothing is tagged.
    """
    total = len(signals) or 1
    acc: dict[str, dict] = defaultdict(lambda: {
        "weight": 0.0, "comments": 0, "likes": 0, "like_list": [], "videos": set(),
        "channels": set(), "examples": [],
    })

    for s in signals:
        likes = s.get("likes", 0) or 0
        for barrier in s.get("demand_types", []):
            a = acc[barrier]
            a["weight"] += math.log1p(likes)
            a["comments"] += 1
            a["likes"] += likes
            a["like_list"].append(likes)
            a["videos"].add(s.get("video_id"))
            a["channels"].add(s.get("channel_name") or s.get("channel_id"))
            if len(a["examples"]) < 12:
                a["examples"].append({
                    "likes": likes,
                    "text": (s.get("text") or "").replace("\n", " ")[:300],
                    "video_title": s.get("video_title"),
                    "channel_name": s.get("channel_name"),
                })

    out = []
    for barrier, a in acc.items():
        lk = sorted(a["like_list"])
        out.append({
            "barrier": barrier,
            "weight": round(a["weight"], 2),
            "comments": a["comments"],
            "share_of_signals": round(100 * a["comments"] / total, 1),
            "total_likes": a["likes"],
            # Mean is reported ONLY next to median and p90. Measured 2026-07-29:
            # every barrier's mean is outlier-driven (medians 1-5, means 29-176;
            # 'archive' scored 176 on the back of a single 10,104-like comment).
            # Ranking barriers by like-average is not safe — rank by frequency.
            "mean_likes": round(a["likes"] / a["comments"], 1) if a["comments"] else 0,
            "median_likes": statistics.median(lk) if lk else 0,
            "p90_likes": lk[int(0.9 * len(lk))] if lk else 0,
            "videos": len(a["videos"]),
            "channels": len(a["channels"]),
            "per_1k_comments": round(1000 * a["comments"] / total, 1),
            "examples": sorted(a["examples"], key=lambda e: -e["likes"]),
        })
    out.sort(key=lambda d: -d["comments"])
    return out


def reclassify_stored_signals(store: KBStore, batch: int = 1_000_000) -> dict:
    """
    Re-run both taggers over comment text already in intel.db.

    Lets a pattern change be applied to the existing corpus without spending
    API quota re-fetching. Does NOT recover comments that were discarded by an
    earlier, narrower admission rule — for those, re-sweep with skip_swept=False.

    `batch` is a safety ceiling, not a page size: a partial reclassify leaves
    the corpus in a mixed state where some rows carry old tags and some new,
    which silently corrupts any cross-tab computed over it. So the default is
    effectively unbounded and hitting the ceiling is reported as an error rather
    than a success.

    Returns {'reclassified': N} or {'error': str}.
    """
    rows = store.get_comment_signals(limit=batch)
    if not rows:
        return {"error": "no stored signals to reclassify"}
    if len(rows) >= batch:
        return {
            "error": f"refusing a partial reclassify: hit the {batch}-row ceiling, so some rows "
                     "would keep stale tags and the corpus would be internally inconsistent. "
                     "Re-run with a higher --batch."
        }

    updated = []
    for r in rows:
        patterns, matched = tag_comment(r.get("text", ""))
        updated.append({
            "comment_id": r["comment_id"], "video_id": r["video_id"],
            "channel_id": r.get("channel_id"), "author": r.get("author"),
            "text": r.get("text", ""), "likes": r.get("likes", 0),
            "reply_count": r.get("reply_count", 0), "published_at": r.get("published_at"),
            "patterns": patterns or r.get("patterns", []),
            "matched_phrases": matched or r.get("matched_phrases", []),
            "demand_types": classify_demand(r.get("text", "")),
        })

    saved = store.save_comment_signals(updated)
    if "error" in saved:
        return saved
    return {"reclassified": saved["saved"]}


def aggregate_signals(signals: list[dict], min_videos: int = 2, top_n: int = 40) -> list[dict]:
    """
    Stage 2: cluster signal comments into candidate terms and rank them.

    Ranking is a transparent, likes-weighted heuristic — NOT a predictor of
    performance. Its only job is ordering a shortlist for human reading.

        weight = Σ log1p(likes) over the comments carrying the term
        rank   = weight × (1 + 0.5·(distinct_videos − 1)) × (1 + 0.5·pocket_share)

    Cross-video recurrence is boosted because a question asked under several
    different channels is stronger evidence than one busy thread.

    Args:
        signals:    Rows from KBStore.get_comment_signals()
        min_videos: Drop terms appearing under fewer than N distinct videos
        top_n:      Max terms returned

    Returns:
        List of dicts sorted by rank desc:
        {term, weight, rank, comments, videos, channels, pocket_hits,
         unmet_hits, question_hits, examples[]}
    """
    acc: dict[str, dict] = defaultdict(lambda: {
        "weight": 0.0, "comments": 0, "videos": set(), "channels": set(),
        "pocket_hits": 0, "unmet_hits": 0, "question_hits": 0, "examples": [],
    })

    for s in signals:
        text = s.get("text", "")
        pats = s.get("patterns", [])
        likes = s.get("likes", 0) or 0
        for term in _extract_terms(text):
            a = acc[term]
            a["weight"] += math.log1p(likes)
            a["comments"] += 1
            a["videos"].add(s.get("video_id"))
            a["channels"].add(s.get("channel_name") or s.get("channel_id"))
            if "pocket" in pats:
                a["pocket_hits"] += 1
            if "unmet_supply" in pats:
                a["unmet_hits"] += 1
            if "question" in pats:
                a["question_hits"] += 1
            if len(a["examples"]) < 5:
                a["examples"].append({
                    "likes": likes,
                    "text": text.replace("\n", " ")[:300],
                    "video_title": s.get("video_title"),
                    "channel_name": s.get("channel_name"),
                    "patterns": pats,
                })

    out = []
    for term, a in acc.items():
        n_videos = len(a["videos"])
        if n_videos < min_videos:
            continue
        pocket_share = a["pocket_hits"] / a["comments"] if a["comments"] else 0.0
        rank = a["weight"] * (1 + 0.5 * (n_videos - 1)) * (1 + 0.5 * pocket_share)
        out.append({
            "term": term,
            "weight": round(a["weight"], 2),
            "rank": round(rank, 2),
            "comments": a["comments"],
            "videos": n_videos,
            "channels": len(a["channels"]),
            "pocket_hits": a["pocket_hits"],
            "unmet_hits": a["unmet_hits"],
            "question_hits": a["question_hits"],
            "examples": sorted(a["examples"], key=lambda e: -e["likes"]),
        })

    out.sort(key=lambda d: -d["rank"])
    return out[:top_n]


# ---------------------------------------------------------------------------
# Digest (dual-write: DB is truth, markdown is regenerated every run)
# ---------------------------------------------------------------------------

def write_digest(store: KBStore, path: Path | None = None, top_n: int = 40) -> dict:
    """
    Regenerate the human-readable harvest digest from intel.db.

    Returns {'path': str, 'terms': N, 'signals': N} or {'error': str}.
    """
    path = Path(path) if path else DEFAULT_DIGEST_PATH
    # Read the WHOLE corpus. get_comment_signals orders by likes DESC, so any
    # limit below the row count silently drops the low-like tail and inflates
    # every median and share in the barrier table.
    limit = 1_000_000
    signals = store.get_comment_signals(limit=limit)
    if not signals:
        return {"error": "no comment signals in intel.db — run --sweep first"}
    if len(signals) >= limit:
        return {"error": f"corpus exceeds the {limit}-row read ceiling; stats would be truncated"}

    terms = aggregate_signals(signals, top_n=top_n)

    by_pattern = {"unmet_supply": [], "pocket": [], "question": []}
    for s in signals:
        for p in s.get("patterns", []):
            if p in by_pattern:
                by_pattern[p].append(s)

    lines = [
        "# GAP-HUNTER HARVEST DIGEST",
        "",
        f"*Generated {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')} by "
        "`python -m tools.discovery.gap_hunter --digest`. Regenerated on every run — "
        "`intel.db.comment_signals` is the store, this file is a view.*",
        "",
        f"**{len(signals)} signal comments** across "
        f"**{len({s['video_id'] for s in signals})} competitor videos** / "
        f"**{len({s.get('channel_name') for s in signals})} channels**.",
        "",
        "> ⚠ **Rank informs, it does not decide.** This is a likes-weighted term count, "
        "not a performance predictor — serve size is not predictable from anything this repo "
        "can measure (four predictors tested and killed, `BREAKOUT-MECHANICS-2026-07.md` §5b). "
        "Stage 3 (live SERP supply check) and Stage 4 (identity + cold-parse gate) are what "
        "actually eliminate candidates.",
        "",
        "---",
        "",
        "## 0. Which BARRIER has demand — the open question",
        "",
        "*The channel's subject is access to the historical record. Four things block access. "
        "Which one draws an audience was left open at the 2026-07-29 interview for the sweep to "
        "answer. **Rank by frequency, not by likes** — measured 2026-07-29, every barrier's mean "
        "is outlier-driven (medians 1–5, means 29–176; `archive` hit 176 on ONE 10,104-like "
        "comment). The mean column is kept only so the gap to the median stays visible.*",
        "",
        "| barrier | comments | share | per 1k | median likes | p90 | mean ⚠ | videos | channels |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    barriers = aggregate_barriers(signals)
    for b in barriers:
        lines.append(
            f"| **{b['barrier']}** | {b['comments']} | {b['share_of_signals']}% | "
            f"{b['per_1k_comments']} | {b['median_likes']} | {b['p90_likes']} | {b['mean_likes']} | "
            f"{b['videos']} | {b['channels']} |"
        )
    lines += ["", "### What each barrier's demand actually sounds like", ""]
    for b in barriers:
        lines.append(f"**{b['barrier']}** — {b['comments']} comments, {b['total_likes']:,} likes")
        for ex in b["examples"][:4]:
            lines.append(f"- *({ex['likes']} likes)* \"{ex['text']}\" "
                         f"— *{ex['channel_name']}: {ex['video_title']}*")
        lines.append("")

    lines += [
        "---",
        "",
        "## 1. Candidate terms — likes-weighted, cross-video",
        "",
        "| # | term | rank | comments | videos | channels | pocket | unmet | question |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for i, t in enumerate(terms, 1):
        lines.append(
            f"| {i} | {t['term']} | {t['rank']} | {t['comments']} | {t['videos']} | "
            f"{t['channels']} | {t['pocket_hits']} | {t['unmet_hits']} | {t['question_hits']} |"
        )

    lines += ["", "---", "", "## 2. Top terms with their evidence", ""]
    for t in terms[:15]:
        lines.append(f"### {t['term']} — rank {t['rank']} · {t['videos']} videos · "
                     f"{t['pocket_hits']} pocket / {t['unmet_hits']} unmet / {t['question_hits']} question")
        for ex in t["examples"][:3]:
            tags = ",".join(ex["patterns"])
            lines.append(f"- *({ex['likes']} likes · {tags})* \"{ex['text']}\" "
                         f"— under **{ex['channel_name']}**: {ex['video_title']}")
        lines.append("")

    lines += ["---", "", "## 3. Highest-liked raw signals by pattern", ""]
    for pattern, label in [
        ("unmet_supply", "Unmet supply — the shelf isn't answering this"),
        ("pocket", "Pocket — a self-identifying national/diaspora voice"),
        ("question", "Question — asked, with likes behind it"),
    ]:
        rows = sorted(by_pattern[pattern], key=lambda s: -(s.get("likes") or 0))[:25]
        lines.append(f"### {label} ({len(by_pattern[pattern])} total)")
        lines.append("")
        for s in rows:
            txt = (s.get("text") or "").replace("\n", " ")[:280]
            lines.append(f"- **{s.get('likes', 0)} likes** — \"{txt}\" "
                         f"— *{s.get('channel_name')}: {s.get('video_title')}*")
        lines.append("")

    lines += [
        "---",
        "",
        "## Next steps",
        "",
        "1. Read §2 and §3 and cluster by judgment into 3–6 topic candidates.",
        "2. **Stage 3 — supply check** each candidate against the live shelf: "
        "`python -m tools.preflight.serp_title_study --slug <slug> --query \"<query>\"`",
        "3. **Stage 4 — identity gate** (judgment, never a score): channel-DNA test "
        "(\"matters in 10 years regardless of who's in power\") + cold-parse test "
        "(\"a stranger understands why the title matters with zero prior knowledge\").",
        "4. Survivors go through `/greenlight`, then `tools/TOPIC-RUBRIC.md` if 2+ remain.",
        "",
    ]

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")
    return {"path": str(path), "terms": len(terms), "signals": len(signals)}


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Sweep competitor comment sections for demand nobody is serving.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  # Stage 1 — mine 40 high-performing competitor videos, 200 comments each
  python -m tools.discovery.gap_hunter --sweep --videos 40 --comments 200

  # See which videos would be swept, and what the tagger finds, writing nothing
  python -m tools.discovery.gap_hunter --sweep --videos 5 --dry-run

  # Stage 2 — regenerate the digest from what's already stored
  python -m tools.discovery.gap_hunter --digest

  # Re-mine videos already swept (e.g. after changing the patterns)
  python -m tools.discovery.gap_hunter --sweep --no-skip-swept
""",
    )
    parser.add_argument("--sweep", action="store_true", help="Run Stage 1 harvest")
    parser.add_argument("--digest", action="store_true", help="Run Stage 2 and write the digest")
    parser.add_argument("--reclassify", action="store_true",
                        help="Re-tag stored comment text after a pattern change (no API calls)")
    parser.add_argument("--batch", type=int, default=1_000_000, metavar="N",
                        help="Safety ceiling on rows reclassified in one pass (default 1000000)")
    parser.add_argument("--videos", type=int, default=40, metavar="N", help="Videos to sweep (default 40)")
    parser.add_argument("--comments", type=int, default=200, metavar="N", help="Comments per video (default 200)")
    parser.add_argument("--min-views", type=int, default=50_000, metavar="N", help="View floor for seeds (default 50000)")
    parser.add_argument("--since", metavar="YYYY-MM-DD", help="Only seed videos published on/after this date")
    parser.add_argument("--no-skip-swept", action="store_true", help="Re-mine videos already swept")
    parser.add_argument("--dry-run", action="store_true", help="Fetch and tag but write nothing")
    parser.add_argument("--out", metavar="PATH", help="Digest output path")

    verbosity = parser.add_mutually_exclusive_group()
    verbosity.add_argument("--verbose", "-v", action="store_true", help="Show debug output on stderr")
    verbosity.add_argument("--quiet", "-q", action="store_true", help="Only show errors on stderr")

    args = parser.parse_args(argv)

    from tools.logging_config import setup_logging
    setup_logging(args.verbose, args.quiet)

    if not args.sweep and not args.digest and not args.reclassify:
        parser.error("nothing to do — pass --sweep, --reclassify and/or --digest")

    store = KBStore()

    if args.reclassify:
        result = reclassify_stored_signals(store, batch=args.batch)
        print(json.dumps(result, indent=2))
        if "error" in result:
            return 1

    if args.sweep:
        seeds = select_seed_videos(
            store,
            limit=args.videos,
            min_views=args.min_views,
            published_after=args.since,
            skip_swept=not args.no_skip_swept,
        )
        if not seeds:
            print(json.dumps({"error": "no seed videos matched — is intel.db populated?"}, indent=2))
            return 1
        logger.info("sweeping %d videos", len(seeds))
        result = sweep_videos(seeds, store, max_comments=args.comments, dry_run=args.dry_run)
        print(json.dumps(result, indent=2))

    if args.digest:
        result = write_digest(store, Path(args.out) if args.out else None)
        print(json.dumps(result, indent=2))
        if "error" in result:
            return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
