"""Small internal operating seam for the conversational History vs Hype workflow.

The user never needs to invoke this module.  It gives the conversational assistant
deterministic seams for active-project resolution, request-specific context, script-risk
selection, creator-language retrieval, attributable strategy evidence, package and
recommendation history, and non-Git milestone preservation.

Historical interpretation, writing, opportunity judgment, and analytics interpretation
remain model work.  Cold research and the legacy control plane are deliberately absent
from every default returned by this module.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sqlite3
import sys
import zipfile
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Optional

from tools.logging_config import get_logger, setup_logging

logger = get_logger(__name__)

REPO_ROOT = Path(__file__).resolve().parents[1]
ACTIVE_POINTER = "ACTIVE_PROJECT"
CHANNEL_STATE = "CHANNEL.md"
CHANNEL_SCOPE = "__channel__"
HOT_FILES = ("PROJECT.md", "RESEARCH.md", "SCRIPT.md")
CREATOR_MODEL = Path("channel-data") / "creator-model" / "OPERATING-MODEL.md"
VOICE_EVIDENCE = Path("channel-data") / "creator-model" / "VOICE-EVIDENCE.md"
KEYWORDS_DB = Path("tools") / "discovery" / "keywords.db"
ANALYTICS_DB = Path("tools") / "youtube_analytics" / "analytics.db"
INTEL_DB = Path("tools") / "intel" / "intel.db"


class ActiveProjectError(RuntimeError):
    """The active-project pointer cannot resolve to a valid hot project."""


@dataclass(frozen=True)
class ActiveProject:
    path: Path
    project: Path
    research: Path
    script: Path

    @property
    def slug(self) -> str:
        return self.path.name


def _inside(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def resolve_active_project(root: Path | str = REPO_ROOT) -> ActiveProject:
    """Resolve the one current project.  Raises visibly on ambiguity or stale state."""
    base = Path(root).resolve()
    pointer = base / ACTIVE_POINTER
    if not pointer.is_file():
        raise ActiveProjectError(f"missing {ACTIVE_POINTER} in {base}")
    raw = pointer.read_text(encoding="utf-8", errors="strict").strip()
    if not raw or "\n" in raw:
        raise ActiveProjectError(f"{ACTIVE_POINTER} must contain exactly one project path")
    path = (base / raw).resolve()
    projects_root = (base / "video-projects").resolve()
    if not _inside(path, projects_root) or any(part.lower() == "_cold" for part in path.parts):
        raise ActiveProjectError("active project must be a non-cold folder under video-projects")
    if not path.is_dir():
        raise ActiveProjectError(f"active project does not exist: {path}")
    files = {name: path / name for name in HOT_FILES}
    missing = [name for name, candidate in files.items() if not candidate.is_file()]
    if missing:
        raise ActiveProjectError("active project is missing hot files: " + ", ".join(missing))
    return ActiveProject(path, files["PROJECT.md"], files["RESEARCH.md"], files["SCRIPT.md"])


def estimate_tokens(text: str) -> int:
    """Stable, intentionally rough context estimate (four characters per token)."""
    return math.ceil(len(text) / 4)


def _terms(text: str) -> set[str]:
    return {
        term.casefold()
        for term in re.findall(r"[A-Za-zÀ-ÿ][A-Za-zÀ-ÿ0-9'-]{2,}", text)
        if term.casefold() not in {
            "the", "and", "that", "this", "with", "from", "what", "which", "about",
            "into", "does", "did", "was", "were", "have", "has", "for", "but",
        }
    }


def _voice_terms(text: str) -> set[str]:
    """Content-bearing terms for voice matching; discard common modal scaffolding."""
    return _terms(text) - {
        "can", "could", "should", "would", "will", "might", "must", "maybe",
        "then", "when", "where", "why", "how", "your", "you", "our", "they",
        "their", "them", "there", "here", "also", "just", "like",
    }


def _sections(text: str) -> list[tuple[str, str]]:
    matches = list(re.finditer(r"(?m)^##+\s+.+$", text))
    if not matches:
        return [("document", text)]
    sections = []
    preamble = text[: matches[0].start()].strip()
    if preamble:
        sections.append(("preamble", preamble))
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        sections.append((match.group(0).lstrip("# "), text[match.start():end].strip()))
    return sections


def select_research(text: str, query: str, limit: int = 6) -> str:
    """Return the most query-relevant hot research sections, never cold dossier text."""
    wanted = _terms(query)
    if not wanted:
        return text
    ranked = []
    for position, (heading, body) in enumerate(_sections(text)):
        heading_terms = _terms(heading)
        body_terms = _terms(body)
        score = 4 * len(wanted & heading_terms) + len(wanted & body_terms)
        if score:
            ranked.append((score, -position, body))
    ranked.sort(reverse=True)
    return "\n\n".join(row[2] for row in ranked[:limit])


_RISK_PATTERNS = {
    "quotation": re.compile(r'(^\s*>|[“”"]|\bquote[sd]?\b)', re.I),
    "number_or_date": re.compile(r"\b(?:\d{2,}|[IVX]{2,})\b"),
    "legal": re.compile(r"\b(law|legal|illegal|crime|criminal|statute|treaty|article|court|genocide)\b", re.I),
    "absolute": re.compile(r"\b(always|never|none|nobody|everyone|all historians|no historian|undisputed)\b", re.I),
    "attribution": re.compile(r"\b(says?|said|argues?|argued|writes?|wrote|claims?|claimed|according to)\b", re.I),
    "source_content": re.compile(
        r"\b(document|charter|manuscript|copy|codex|text|source|record|archive|colophon|version)\b"
        r".{0,45}\b(says?|shows?|records?|contains?|states?|dates?|identif(?:y|ies|ied)|"
        r"descend(?:s|ed)?|deriv(?:e|es|ed)|translate[sd]?|print(?:s|ed)?|disclos(?:e|es|ed))\b",
        re.I,
    ),
    "translation": re.compile(
        r"\b(translat(?:e|es|ed|ion)|original language|Greek source|Latin source|rendering)\b",
        re.I,
    ),
    "causal_or_motive": re.compile(
        r"\b(because|therefore|which is why|in order to|motive|intended|deliberately|"
        r"conscious(?:ly)?|to protect|to preserve|led to|caused)\b",
        re.I,
    ),
    "showability": re.compile(r"\[(?:SHOW|CARD|ON[- ]?SCREEN)(?::|\])", re.I),
}


def scan_claim_risks(text: str) -> list[dict]:
    """Select dangerous-if-wrong lines across a complete script; do not adjudicate them."""
    risks = []
    seen = set()
    for line_no, line in enumerate(text.splitlines(), 1):
        stripped = line.strip()
        if not stripped or stripped.startswith("<!--"):
            continue
        for category, pattern in _RISK_PATTERNS.items():
            if pattern.search(stripped) and (line_no, category) not in seen:
                seen.add((line_no, category))
                risks.append({"line": line_no, "category": category, "text": stripped[:280]})
    return risks


def _loaded(path: Path, content: str) -> dict:
    return {"file": path.name, "content": content, "estimated_tokens": estimate_tokens(content)}


def _virtual_loaded(name: str, payload: dict) -> dict:
    content = json.dumps(payload, indent=2, ensure_ascii=False)
    return {"file": name, "content": content, "estimated_tokens": estimate_tokens(content)}


def _creator_model_packet(root: Path, query: str, *, limit: int = 4) -> Optional[dict]:
    path = root / CREATOR_MODEL
    if not path.is_file():
        return None
    text = path.read_text(encoding="utf-8", errors="replace")
    selected = select_research(text, query, limit=limit) if query else text
    row = _loaded(path, selected)
    row["file"] = "OPERATING-MODEL.md (selected sections)" if query else "OPERATING-MODEL.md"
    return row


def _strategy_records(root: Path, scope: str) -> tuple[dict, dict]:
    """Read package chronology and scoped recommendation reasoning without migrating a DB."""
    db_path = root / KEYWORDS_DB
    package = {
        "source": str(db_path),
        "grain": "chronological package observations",
        "records": [],
    }
    ledger = {
        "source": str(db_path),
        "grain": "recommendation reasoning and later outcomes",
        "scope": "channel" if scope == CHANNEL_SCOPE else scope,
        "records": [],
    }
    if not db_path.is_file():
        package["status"] = "unavailable: keywords database missing"
        ledger["status"] = "unavailable: keywords database missing"
        return package, ledger
    try:
        from tools.discovery.performance_tracker import PerformanceTracker
        from tools.sqlite_access import connect_readonly

        connection = connect_readonly(db_path)
        connection.row_factory = sqlite3.Row
        try:
            tracker = PerformanceTracker(connection)
            package["records"] = (
                [] if scope == CHANNEL_SCOPE else tracker.get_package_versions(scope)
            )
            ledger["records"] = tracker.get_recommendations(scope)
        finally:
            connection.close()
        package["as_of"] = max(
            (row.get("recorded_at") or "" for row in package["records"]), default=None
        )
        ledger["as_of"] = max(
            (
                row.get("outcome_as_of") or row.get("recorded_at") or ""
                for row in ledger["records"]
            ),
            default=None,
        )
        if not package["records"]:
            package["status"] = "no package version recorded"
        if not ledger["records"]:
            ledger["status"] = "no recommendation recorded"
    except (OSError, sqlite3.Error) as exc:
        status = f"unavailable: {type(exc).__name__}"
        package["status"] = status
        ledger["status"] = status
    return package, ledger


_STRATEGY_STOP_TERMS = {
    "channel", "evidence", "growth", "history", "outcome", "package", "project",
    "recommendation", "strategy", "thumbnail", "title", "video", "viewer", "viewers",
}


def _market_evidence(root: Path, query: str) -> dict:
    """Return dated matching public signals, never an opportunity score."""
    db_path = root / INTEL_DB
    packet = {
        "source": str(db_path),
        "grain": "stored public competitor videos and comment signals",
        "query": query,
        "competitor_videos": [],
        "comment_signals": [],
        "known_gaps": [
            "foreign-language coverage is not identified by the current store",
            "source viability must be established from the project's research, not market data",
        ],
    }
    if not db_path.is_file():
        packet["status"] = "unavailable: market intelligence database missing"
        return packet
    wanted = sorted(
        (_terms(query) - _STRATEGY_STOP_TERMS), key=lambda term: (-len(term), term)
    )[:8]
    if not wanted:
        packet["status"] = "no specific topic terms supplied; no generic score substituted"
        return packet
    try:
        from tools.sqlite_access import connect_readonly

        connection = connect_readonly(db_path)
        connection.row_factory = sqlite3.Row
        try:
            packet["as_of"] = connection.execute(
                "SELECT MAX(last_refresh) FROM kb_meta"
            ).fetchone()[0]
            minimum_overlap = 2 if len(wanted) >= 2 else 1
            match_score = " + ".join(
                "CASE WHEN LOWER(v.title) LIKE ? THEN 1 ELSE 0 END" for _ in wanted
            )
            params = tuple(f"%{term.casefold()}%" for term in wanted)
            rows = connection.execute(
                f"""
                SELECT v.video_id, v.title, c.channel_name, v.published_at, v.views,
                       v.duration_seconds, v.is_outlier, v.outlier_ratio, v.fetched_at
                FROM competitor_videos v
                LEFT JOIN competitor_channels c ON c.channel_id = v.channel_id
                WHERE ({match_score}) >= ?
                ORDER BY COALESCE(v.is_outlier, 0) DESC,
                         COALESCE(v.views, 0) DESC,
                         v.published_at DESC
                LIMIT 8
                """,
                params + (minimum_overlap,),
            ).fetchall()
            packet["competitor_videos"] = [dict(row) for row in rows]

            comment_score = " + ".join(
                "CASE WHEN LOWER(s.text) LIKE ? THEN 1 ELSE 0 END" for _ in wanted
            )
            comment_rows = connection.execute(
                f"""
                SELECT s.video_id, s.text, s.likes, s.reply_count,
                       s.published_at, s.fetched_at
                FROM comment_signals s
                WHERE ({comment_score}) >= ?
                ORDER BY COALESCE(s.likes, 0) DESC, s.published_at DESC
                LIMIT 5
                """,
                params + (minimum_overlap,),
            ).fetchall()
            packet["comment_signals"] = [dict(row) for row in comment_rows]
        finally:
            connection.close()
        if not packet["competitor_videos"] and not packet["comment_signals"]:
            packet["status"] = "no matching stored public evidence; do not infer no demand"
    except (OSError, sqlite3.Error) as exc:
        packet["status"] = f"unavailable: {type(exc).__name__}"
    return packet


def _performance_evidence(root: Path, package: dict) -> dict:
    """Return attributable target metrics and a small same-topic cohort."""
    db_path = root / ANALYTICS_DB
    video_ids = [row.get("video_id") for row in package.get("records", []) if row.get("video_id")]
    video_id = video_ids[-1] if video_ids else None
    packet = {
        "source": str(db_path),
        "target_video_id": video_id,
        "target": None,
        "cohort": [],
        "cohort_rule": "up to five most recent other videos with the same stored topic type",
    }
    if not video_id:
        packet["status"] = "active project has no linked published video; outcome not yet observable"
        return packet
    if not db_path.is_file():
        packet["status"] = "unavailable: analytics database missing"
        return packet
    try:
        from tools.youtube_analytics.store import AnalyticsStore

        with AnalyticsStore.open_readonly(db_path) as store:
            rows = store.videos(order_by="published_at", descending=True)
            lifetime = store.lifetime_ctr_by_video()
        target = next((row for row in rows if row.get("video_id") == video_id), None)
        if target is None:
            packet["status"] = "linked video is absent from analytics"
            return packet

        def metric_row(row: dict) -> dict:
            ctr = lifetime.get(row["video_id"], {})
            return {
                "video_id": row["video_id"],
                "title": row.get("title"),
                "published_at": row.get("published_at"),
                "topic_type": row.get("topic_type"),
                "views": row.get("views"),
                "average_view_percentage": row.get("avg_view_percentage"),
                "subscribers_gained": row.get("subscribers_gained"),
                "metrics_as_of": row.get("metrics_fetched_at") or row.get("fetched_at"),
                "lifetime_impressions": ctr.get("impressions"),
                "lifetime_ctr_percent": ctr.get("ctr_percent"),
                "ctr_grain": ctr.get("grain"),
                "ctr_as_of": ctr.get("as_of"),
                "ctr_source": ctr.get("source_table"),
            }

        packet["target"] = metric_row(target)
        topic = target.get("topic_type")
        if topic:
            peers = [
                row for row in rows
                if row.get("video_id") != video_id and row.get("topic_type") == topic
            ][:5]
            packet["cohort"] = [metric_row(row) for row in peers]
        if not packet["cohort"]:
            packet["cohort_note"] = "no same-topic cohort is available; do not substitute a broad average"
    except (OSError, sqlite3.Error) as exc:
        packet["status"] = f"unavailable: {type(exc).__name__}"
    return packet


def _business_evidence(root: Path) -> dict:
    """Return a dated channel-health observation and state what is not tracked."""
    db_path = root / ANALYTICS_DB
    packet = {
        "source": str(db_path),
        "grain": "daily channel metrics, latest 28 calendar days in the store",
        "currency_target": "approximately EUR 2,000 per month",
        "known_gap": "revenue and sponsorship income are not tracked in this database",
    }
    if not db_path.is_file():
        packet["status"] = "unavailable: analytics database missing"
        return packet
    try:
        from tools.sqlite_access import connect_readonly

        connection = connect_readonly(db_path)
        connection.row_factory = sqlite3.Row
        try:
            row = connection.execute(
                """
                WITH latest AS (SELECT MAX(day) AS max_day FROM daily_channel)
                SELECT MIN(day) AS period_start, MAX(day) AS period_end,
                       SUM(views) AS views,
                       SUM(watch_time_minutes) AS watch_time_minutes,
                       SUM(subscribers_gained) AS subscribers_gained,
                       SUM(subscribers_lost) AS subscribers_lost,
                       MAX(fetched_at) AS as_of
                FROM daily_channel, latest
                WHERE day >= date(latest.max_day, '-27 days')
                  AND day <= latest.max_day
                """
            ).fetchone()
        finally:
            connection.close()
        packet["observation"] = dict(row) if row and row["period_end"] else None
        if packet["observation"] is None:
            packet["status"] = "no daily channel metrics available"
    except (OSError, sqlite3.Error) as exc:
        packet["status"] = f"unavailable: {type(exc).__name__}"
    return packet


def build_context(
    intent: str,
    *,
    query: str = "",
    root: Path | str = REPO_ROOT,
) -> dict:
    """Build the smallest useful hot packet for a conversational intent."""
    base = Path(root).resolve()
    active = resolve_active_project(base)
    channel_path = base / CHANNEL_STATE
    if not channel_path.is_file():
        raise ActiveProjectError(f"missing {CHANNEL_STATE} in {base}")
    channel_text = channel_path.read_text(encoding="utf-8", errors="replace")
    project_text = active.project.read_text(encoding="utf-8", errors="replace")
    research_text = active.research.read_text(encoding="utf-8", errors="replace")
    script_text = active.script.read_text(encoding="utf-8", errors="replace")
    normalized = intent.casefold().replace("-", "_").replace(" ", "_")
    loaded = []
    claim_risks = []
    voice_examples = []
    package_packet = None
    ledger_packet = None

    def strategy_records(scope: str = active.slug) -> tuple[dict, dict]:
        nonlocal package_packet, ledger_packet
        if scope == active.slug and package_packet is not None and ledger_packet is not None:
            return package_packet, ledger_packet
        package, ledger = _strategy_records(base, scope)
        if scope == active.slug:
            package_packet, ledger_packet = package, ledger
        return package, ledger

    if normalized in {"status", "next_action", "what_now"}:
        loaded.append(_loaded(active.project, project_text))
    elif normalized in {"channel", "channel_status", "growth"}:
        loaded.append(_loaded(channel_path, channel_text))
        model = _creator_model_packet(base, query or "growth channel identity collaboration", limit=4)
        if model:
            loaded.append(model)
    elif normalized in {"decision", "recommendation", "collaboration", "workflow"}:
        loaded.append(_loaded(channel_path, channel_text))
        model = _creator_model_packet(base, query or "decisions collaboration bottleneck", limit=4)
        if model:
            loaded.append(model)
        _, ledger = strategy_records(CHANNEL_SCOPE)
        loaded.append(_virtual_loaded("RECOMMENDATION-LEDGER.json", ledger))
    elif normalized in {"next_video", "opportunity", "topic_opportunity"}:
        loaded.append(_loaded(channel_path, channel_text))
        loaded.append(_loaded(active.project, project_text))
        model = _creator_model_packet(
            base,
            (query + " growth opportunity decisions commitment").strip(),
            limit=5,
        )
        if model:
            loaded.append(model)
        _, ledger = strategy_records(CHANNEL_SCOPE)
        loaded.append(
            _virtual_loaded("MARKET-EVIDENCE.json", _market_evidence(base, query or active.slug))
        )
        loaded.append(_virtual_loaded("RECOMMENDATION-LEDGER.json", ledger))
    elif normalized in {"packaging", "package", "title", "thumbnail"}:
        loaded.append(_loaded(active.project, project_text))
        loaded.append(_loaded(active.script, script_text))
        model = _creator_model_packet(
            base,
            (query + " packaging script production growth decisions").strip(),
            limit=5,
        )
        if model:
            loaded.append(model)
        package, ledger = strategy_records()
        loaded.append(_virtual_loaded("PACKAGE-HISTORY.json", package))
        loaded.append(_virtual_loaded("RECOMMENDATION-LEDGER.json", ledger))
        loaded.append(
            _virtual_loaded("MARKET-EVIDENCE.json", _market_evidence(base, query or active.slug))
        )
    elif normalized in {"business", "viability", "revenue"}:
        loaded.append(_loaded(channel_path, channel_text))
        model = _creator_model_packet(
            base,
            (query + " growth business channel identity viability money").strip(),
            limit=5,
        )
        if model:
            loaded.append(model)
        _, ledger = strategy_records(CHANNEL_SCOPE)
        loaded.append(_virtual_loaded("CHANNEL-BUSINESS-EVIDENCE.json", _business_evidence(base)))
        loaded.append(_virtual_loaded("RECOMMENDATION-LEDGER.json", ledger))
    elif normalized in {"performance", "analytics", "video_performance"}:
        loaded.append(_loaded(active.project, project_text))
        model = _creator_model_packet(
            base,
            (query + " experimentation outcome revised confidence packaging growth").strip(),
            limit=5,
        )
        if model:
            loaded.append(model)
        package, ledger = strategy_records()
        loaded.append(_virtual_loaded("PACKAGE-HISTORY.json", package))
        loaded.append(_virtual_loaded("RECOMMENDATION-LEDGER.json", ledger))
        loaded.append(
            _virtual_loaded("PERFORMANCE-EVIDENCE.json", _performance_evidence(base, package))
        )
    elif normalized in {"voice", "sounds_like_ai", "rewrite"}:
        loaded.append(_loaded(active.project, project_text))
        selected = select_research(script_text, query, limit=2) if query else script_text
        loaded.append(_loaded(active.script, selected))
        voice_examples = select_voice_examples(query or selected, root=root)
    elif normalized in {"disagreement", "research", "historiography"}:
        loaded.append(_loaded(active.project, project_text))
        selected = select_research(research_text, query)
        row = _loaded(active.research, selected)
        row["file"] = "RESEARCH.md (selected sections)" if query else "RESEARCH.md"
        loaded.append(row)
    else:
        # A safety/evidence/exhibit request first scans the complete script so a locally
        # plausible sentence cannot hide contradictions elsewhere in the argument.
        loaded.append(_loaded(active.project, project_text))
        loaded.append(_loaded(active.script, script_text))
        selected = select_research(research_text, query)
        row = _loaded(active.research, selected)
        row["file"] = "RESEARCH.md (selected sections)" if query else "RESEARCH.md"
        loaded.append(row)
        claim_risks = scan_claim_risks(script_text)

    return {
        "project": active.slug,
        "intent": normalized,
        "loaded": loaded,
        "estimated_tokens": sum(item["estimated_tokens"] for item in loaded),
        "claim_risks": claim_risks,
        "voice_examples": voice_examples,
        "excluded": [
            "legacy control plane",
            "cold research dossier",
            "superseded strategy and composite scores (quarantined from decisions)",
            "unrelated project files",
        ],
        "decision_policy": (
            "recommend in prose from attributable evidence; composite scores are never verdicts"
        ),
    }


def _paragraphs(path: Path) -> Iterable[str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    for paragraph in re.split(r"\n\s*\n", text):
        paragraph = paragraph.strip()
        if paragraph:
            yield paragraph


def _voice_windows(text: str, wanted: set[str], max_chars: int = 1200) -> list[str]:
    """Return compact sentence windows around matching language in a long raw entry."""
    if len(text) <= max_chars:
        return [text]
    sentences = [part.strip() for part in re.split(r"(?<=[.!?])\s+", text) if part.strip()]
    hits = [index for index, sentence in enumerate(sentences) if wanted & _voice_terms(sentence)]
    windows = []
    seen = set()
    for index in hits:
        start = max(0, index - 1)
        end = min(len(sentences), index + 2)
        while start > 0 and len(" ".join(sentences[start - 1:end])) <= max_chars:
            start -= 1
        while end < len(sentences) and len(" ".join(sentences[start:end + 1])) <= max_chars:
            end += 1
        window = " ".join(sentences[start:end])
        if window not in seen:
            seen.add(window)
            windows.append(window)
    return windows or [text[:max_chars]]


def select_voice_examples(
    passage: str,
    *,
    root: Path | str = REPO_ROOT,
    limit: int = 6,
) -> list[dict]:
    """Retrieve spontaneous and approved language only; model-authored doctrine is absent."""
    base = Path(root).resolve()
    active = resolve_active_project(base)
    wanted = _voice_terms(passage)
    candidates: list[tuple[int, int, Path, str, Optional[str], str]] = []
    paths = list((active.path / "_adlib").glob("*.md")) if (active.path / "_adlib").is_dir() else []
    creator_corpus = base / VOICE_EVIDENCE
    if creator_corpus.is_file():
        paths.append(creator_corpus)
    calibration = base / "channel-data" / "calibration" / "CALIBRATION-CORPUS.md"
    if calibration.is_file():
        paths.append(calibration)
    for path in paths:
        for paragraph in _paragraphs(path):
            lower = paragraph.casefold()
            if path.parent.name != "_adlib" and any(
                marker in lower
                for marker in ("cringe inventory", "banlist", "all stripped", "— cut", "withdrawn")
            ):
                continue
            spontaneous = path.parent.name == "_adlib" or "spontaneous" in lower or "ad-lib" in lower
            approved = "approved" in lower or "locked" in lower or "creator" in lower
            if not (spontaneous or approved):
                continue

            # Current-project ad-lib files are themselves primary voice evidence.  The
            # large calibration corpus is not: most paragraphs are analysis *about*
            # the voice.  From that corpus return only explicitly marked approved
            # wording or verbatim quoted fragments, never the surrounding doctrine.
            if path.parent.name == "_adlib":
                fragments = [(paragraph, None)]
            else:
                marked = re.match(
                    r"(?is)^\s*(approved|spontaneous|creator)"
                    r"(?:\s*\[([^\]]+)\])?\s*:\s*(.+)$",
                    paragraph,
                )
                fragments = (
                    [(marked.group(3), marked.group(2))]
                    if marked
                    else [(fragment, None) for fragment in re.findall(
                        r'[“"]([^“”"\n]{18,})[”"]', paragraph
                    )]
                )
            for fragment, locator in fragments:
                if locator == "A2-105":
                    continue
                routed_fragments = (
                    _voice_windows(fragment, wanted) if path == creator_corpus else [fragment]
                )
                for routed in routed_fragments:
                    overlap = len(wanted & _voice_terms(routed))
                    minimum_overlap = (
                        1
                        if path.parent.name == "_adlib"
                        else max(2, math.ceil(len(wanted) * 0.4))
                    )
                    if overlap < minimum_overlap:
                        continue
                    evidence = "spontaneous" if spontaneous else "approved"
                    priority = 3 if path.parent.name == "_adlib" else (2 if path == creator_corpus else 1)
                    candidates.append((overlap, priority, path, evidence, locator, routed[:1200]))
    candidates.sort(key=lambda row: (row[0], row[1], -len(row[5])), reverse=True)
    results = []
    for _, _, path, evidence, locator, paragraph in candidates[:limit]:
        row = {
            "source": str(path),
            "evidence": evidence,
            "factual_scope": "voice_only",
            "text": paragraph,
        }
        if locator:
            row["locator"] = locator
        results.append(row)
    return results


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def create_snapshot(
    label: str,
    *,
    root: Path | str = REPO_ROOT,
    now: Optional[str] = None,
) -> Path:
    """Create a hash-manifested hot-state snapshot independent of Git."""
    base = Path(root).resolve()
    active = resolve_active_project(base)
    stamp = now or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%M%SZ")
    safe_label = re.sub(r"[^a-z0-9-]+", "-", label.casefold()).strip("-") or "milestone"
    target_dir = base / "_migration-snapshots" / "active"
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / f"{stamp}-{active.slug}-{safe_label}.zip"
    files = [active.project, active.research, active.script]
    manifest = {
        "created_at": stamp,
        "label": label,
        "project": active.slug,
        "files": {path.name: _sha256(path) for path in files},
        "excludes": ["_cold", "_research", "legacy control plane", "credentials"],
    }
    with zipfile.ZipFile(target, "x", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in files:
            archive.write(path, arcname=path.name)
        archive.writestr("MANIFEST.json", json.dumps(manifest, indent=2))
    target.chmod(0o444)
    return target


def _record_package(args) -> dict:
    from tools.discovery.database import KeywordDB

    active = resolve_active_project(args.root)
    value = args.value
    source_path = None
    content_hash = None
    if args.kind == "thumbnail":
        candidate = Path(value)
        if not candidate.is_absolute():
            candidate = (active.path / candidate).resolve()
        if not candidate.is_file():
            return {"error": f"thumbnail does not exist: {candidate}"}
        source_path = str(candidate)
        content_hash = _sha256(candidate)
        value = candidate.name
    db = KeywordDB(args.db)
    try:
        return db.record_package_version(
            project_slug=active.slug,
            kind=args.kind,
            value=value,
            video_id=args.video_id,
            source_path=source_path,
            content_hash=content_hash,
            effective_at=args.effective_at,
            experiment_id=args.experiment_id,
            reason=args.reason,
        )
    finally:
        db.close()


def _record_recommendation(args) -> dict:
    from tools.discovery.database import KeywordDB

    active = resolve_active_project(args.root)
    channel_kinds = {"topic", "workflow", "business"}
    scope_name = args.scope or ("channel" if args.kind in channel_kinds else "project")
    scope = CHANNEL_SCOPE if scope_name == "channel" else active.slug
    db = KeywordDB(args.db)
    try:
        return db.record_recommendation(
            project_slug=scope,
            decision_kind=args.kind,
            recommendation=args.recommendation,
            rationale=args.rationale,
            predicted_mechanism=args.predicted_mechanism,
            expected_observation=args.expected_observation,
            decision_status=args.status,
            evidence_limitations=args.evidence_limitations,
            recorded_at=args.recorded_at,
        )
    finally:
        db.close()


def _record_recommendation_outcome(args) -> dict:
    from tools.discovery.database import KeywordDB

    db = KeywordDB(args.db)
    try:
        return db.record_recommendation_outcome(
            args.recommendation_id,
            args.outcome,
            args.revised_confidence,
            outcome_as_of=args.outcome_as_of,
        )
    finally:
        db.close()


def main(argv=None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="Internal active-project operations")
    parser.add_argument("--root", type=Path, default=REPO_ROOT)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--verbose", "-v", action="store_true")
    group.add_argument("--quiet", "-q", action="store_true")
    sub = parser.add_subparsers(dest="command", required=True)
    context = sub.add_parser("context")
    context.add_argument("intent")
    context.add_argument("--query", default="")
    risk = sub.add_parser("risk")
    risk.add_argument("--script", type=Path)
    voice = sub.add_parser("voice")
    voice.add_argument("passage")
    snapshot = sub.add_parser("snapshot")
    snapshot.add_argument("label")
    package = sub.add_parser("record-package")
    package.add_argument("kind", choices=("title", "thumbnail"))
    package.add_argument("value")
    package.add_argument("--video-id")
    package.add_argument("--effective-at")
    package.add_argument("--experiment-id")
    package.add_argument("--reason")
    package.add_argument("--db")
    recommendation = sub.add_parser("record-recommendation")
    recommendation.add_argument(
        "kind", choices=("topic", "package", "workflow", "research", "business", "other")
    )
    recommendation.add_argument("recommendation")
    recommendation.add_argument("rationale")
    recommendation.add_argument("predicted_mechanism")
    recommendation.add_argument("--expected-observation")
    recommendation.add_argument(
        "--status",
        choices=("proposed", "accepted", "rejected", "superseded", "reviewed"),
        default="proposed",
    )
    recommendation.add_argument("--evidence-limitations")
    recommendation.add_argument("--recorded-at")
    recommendation.add_argument("--scope", choices=("channel", "project"))
    recommendation.add_argument("--db")
    outcome = sub.add_parser("record-outcome")
    outcome.add_argument("recommendation_id", type=int)
    outcome.add_argument("outcome")
    outcome.add_argument("revised_confidence")
    outcome.add_argument("--outcome-as-of")
    outcome.add_argument("--db")
    args = parser.parse_args(argv)
    setup_logging(args.verbose, args.quiet)
    try:
        if args.command == "context":
            result = build_context(args.intent, query=args.query, root=args.root)
        elif args.command == "risk":
            active = resolve_active_project(args.root)
            path = args.script or active.script
            result = scan_claim_risks(path.read_text(encoding="utf-8", errors="replace"))
        elif args.command == "voice":
            result = select_voice_examples(args.passage, root=args.root)
        elif args.command == "snapshot":
            result = {"snapshot": str(create_snapshot(args.label, root=args.root))}
        elif args.command == "record-package":
            result = _record_package(args)
        elif args.command == "record-recommendation":
            result = _record_recommendation(args)
        else:
            result = _record_recommendation_outcome(args)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 1 if isinstance(result, dict) and "error" in result else 0
    except (ActiveProjectError, OSError, ValueError) as exc:
        logger.error("%s", exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())
