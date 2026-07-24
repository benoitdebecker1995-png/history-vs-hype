#!/usr/bin/env python3
"""
Topic-note miner — turns per-video `01-VERIFIED-RESEARCH.md` files into
concept-scoped topic notes under `.brain/topics/`.

Why this exists
---------------
Research in this repo is filed per VIDEO. That means knowledge dies when the
video ships: nothing compounds across projects, and `graphify-research` stays
sparse. This tool re-files the same verified claims by CONCEPT, so episode N+1
is cheaper than episode N.

The trinity (source / topic / argument) maps onto existing `.brain/` roots:
    `.brain/sources/`  source notes  — one per book/paper/document
    `.brain/topics/`   topic notes   — atomic claims, grouped by concept  (NEW)
    `.brain/threads/`  argument notes — our own synthesis (unchanged)

Fabrication guard
-----------------
Extraction is bulk-read work and is dispatched to Gemini Flash. Per the
historian Rule-1 / web-Gemini verbatim ban, NO model is trusted to produce
verbatim text. Every `verbatim` field is validated in code as an exact
substring of the originating research file; anything that fails is DROPPED and
logged. The extractor can therefore only ever COPY, never author.

Usage:
    python -m tools.brain.topic_mine scan
    python -m tools.brain.topic_mine extract [--only SLUG] [--limit N] [--model M]
    python -m tools.brain.topic_mine validate
    python -m tools.brain.topic_mine audit [--only SLUG] [--blocking-only]
    python -m tools.brain.topic_mine vocab [--unmapped]
    python -m tools.brain.topic_mine build [--dry-run]

`audit` is the write-time gate: it exits 1 when a dossier attributes a claim to
a retrieval tool ("NotebookLM") or a vague plural ("Multiple academic sources").
Those look sourced while being impossible to check, and they are how #35 and #34
shipped with untraceable claims. Run it before a dossier is called script-ready.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
import time
import unicodedata
from dataclasses import dataclass, field, asdict
from datetime import date
from pathlib import Path
from typing import Any, Iterable

from tools.logging_config import get_logger

logger = get_logger(__name__)

REPO = Path(__file__).resolve().parents[2]
VIDEO_ROOT = REPO / "video-projects"
BRAIN = REPO / ".brain"
TOPICS_DIR = BRAIN / "topics"
SOURCES_DIR = BRAIN / "sources"
EXTRACT_DIR = TOPICS_DIR / "_extracted"
REJECT_LOG = TOPICS_DIR / "_extracted" / "_rejected.jsonl"

RESEARCH_FILENAME = "01-VERIFIED-RESEARCH.md"
DEFAULT_MODEL = "gemini-2.5-flash"

#: Above this a claim is not atomic and cannot be recombined — reject it.
MAX_CLAIM_WORDS = 45
#: Above this it is merely verbose: keep the verified content, flag the debt.
#: Discarding real research over a word count would lose knowledge to a
#: formatting rule, which is the opposite of the point.
ATOMIC_CLAIM_WORDS = 32
MIN_VERBATIM_CHARS = 25

#: Free-tier Gemini allows ~20 requests/min. Pace deliberately rather than
#: discovering the ceiling through 429s, which cost more time than they save.
REQUEST_SPACING_S = 8.0
MAX_QUOTA_WAITS = 12
SCRATCH_CWD = Path(tempfile.gettempdir()) / "hvh-topic-mine"

STATUS_VALUES = {"verified", "partial", "unverified"}


# --------------------------------------------------------------------------
# Discovery
# --------------------------------------------------------------------------


@dataclass
class ResearchFile:
    """One per-video research file awaiting extraction."""

    slug: str
    lifecycle: str
    path: Path
    size: int

    @property
    def extract_path(self) -> Path:
        return EXTRACT_DIR / f"{self.slug}.json"

    @property
    def extracted(self) -> bool:
        return self.extract_path.exists()


def discover() -> list[ResearchFile]:
    """Find every `01-VERIFIED-RESEARCH.md` under video-projects/, largest first.

    Includes `_BACKLOG/` deliberately: parked projects still hold verified
    knowledge, and re-filing it by topic is exactly how it stops being lost.
    """
    found: list[ResearchFile] = []
    for path in VIDEO_ROOT.rglob(RESEARCH_FILENAME):
        rel = path.relative_to(VIDEO_ROOT)
        lifecycle = rel.parts[0]
        # Project dir is the first ancestor that is not `_research`.
        project_dir = path.parent
        if project_dir.name == "_research":
            project_dir = project_dir.parent
        found.append(
            ResearchFile(
                slug=project_dir.name,
                lifecycle=lifecycle,
                path=path,
                size=path.stat().st_size,
            )
        )
    found.sort(key=lambda r: r.size, reverse=True)
    return found


# --------------------------------------------------------------------------
# Extraction
# --------------------------------------------------------------------------

EXTRACTION_PROMPT = """You are a research archivist. Below is a verified-research
dossier for a single documentary video. Your ONLY job is to RE-FILE its
already-verified claims by TOPIC. You are copying, not authoring.

Return a single JSON object, no prose, no markdown fence:

{"claims": [
  {
    "claim": "<one atomic sentence, max 30 words, exactly ONE proposition, plain past-tense prose>",
    "topics": ["<kebab-case-concept>", "..."],
    "verbatim": "<EXACT character-for-character substring copied from the dossier, or null>",
    "source": "<the source attribution as written in the dossier: author, work, page>",
    "status": "verified|partial|unverified",
    "anchor": "<the exact heading line the claim sits under, copied verbatim>"
  }
]}

HARD RULES — violations are detected and discarded automatically:
1. `verbatim` MUST be copied character-for-character from the dossier text. Never
   reword, never repair, never complete an ellipsis. If you cannot copy it
   exactly, set it to null. Do NOT supply a quote from your own knowledge.
2. `source` MUST be attribution that already appears in the dossier. Never infer
   a page number, a year, or an edition that is not written there.
3. `claim` is YOUR compression of what the dossier says — one proposition only.
   Strip video-production framing ("script note", "use this", "gold").
4. `anchor` must be a heading line that literally appears in the dossier.
5. `topics`: 1-3 concept slugs. Name the CONCEPT, not the country or the
   episode. Prefer transferable mechanisms — `uti-possidetis-juris`,
   `treaty-translation-discrepancy`, `concession-extraction`,
   `population-transfer`, `boundary-arbitration` — over
   `tripoli` or `article-11`. Reuse slugs across claims aggressively.
6. Skip: packaging notes, title ideas, retention/runtime notes, to-do items,
   source-acquisition wishlists, anything about making the video rather than
   about history.
7. Prefer 20-60 claims. Quality over exhaustiveness. Skip anything you cannot
   attribute.

DOSSIER (video: __SLUG__):
---
__BODY__
---
Return only the JSON object."""


def build_prompt(rf: ResearchFile) -> str:
    """Placeholders are substituted, not `.format`-ed — the template contains
    literal JSON braces that `str.format` would treat as fields."""
    body = rf.path.read_text(encoding="utf-8", errors="replace")
    return EXTRACTION_PROMPT.replace("__SLUG__", rf.slug).replace("__BODY__", body)


def _strip_fence(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```[a-zA-Z]*\n", "", text)
        text = re.sub(r"\n```\s*$", "", text)
    return text.strip()


def _first_json_object(text: str) -> str | None:
    """Return the first balanced {...} block, ignoring braces inside strings."""
    start = text.find("{")
    if start == -1:
        return None
    depth = 0
    in_str = False
    escape = False
    for i in range(start, len(text)):
        ch = text[i]
        if escape:
            escape = False
            continue
        if ch == "\\":
            escape = True
            continue
        if ch == '"':
            in_str = not in_str
            continue
        if in_str:
            continue
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return text[start : i + 1]
    return None


def gemini_bin() -> str:
    """Resolve the Gemini CLI. On Windows the npm shim is `gemini.cmd`, which
    bare `subprocess` will not find under the plain name."""
    for name in ("gemini", "gemini.cmd", "gemini.exe"):
        found = shutil.which(name)
        if found:
            return found
    raise RuntimeError("gemini CLI not found on PATH")


class RateLimited(RuntimeError):
    """Gemini refused on quota. Carries the server's own retry delay."""

    def __init__(self, message: str, retry_after: float):
        super().__init__(message)
        self.retry_after = retry_after


def _parse_retry_after(text: str) -> float | None:
    m = re.search(r"[Pp]lease retry in ([0-9.]+)s", text)
    return float(m.group(1)) if m else None


def _gemini_once(prompt: str, model: str, timeout: int) -> str:
    # Run from a scratch cwd: the Gemini CLI is agentic and will otherwise try
    # to index the whole repo as its workspace (1,600 PDFs, an EPERM on
    # .pytest_cache) on every single call.
    proc = subprocess.run(
        [gemini_bin(), "-m", model, "--yolo", "-o", "text"],
        input=prompt,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
        cwd=SCRATCH_CWD,
    )
    out = proc.stdout or ""
    if proc.returncode != 0:
        err = proc.stderr or ""
        if "429" in err or "exceeded your current quota" in err:
            raise RateLimited(
                f"gemini quota exceeded (model={model})",
                _parse_retry_after(err) or 60.0,
            )
        raise RuntimeError(f"gemini exited {proc.returncode}: {err[-600:]}")
    # The CLI exits 0 while printing a transport error to stdout.
    if "Error when talking to Gemini API" in out or not out.strip():
        raise RuntimeError(f"gemini transport error: {out.strip()[:300] or 'empty output'}")
    return out


def run_gemini(prompt: str, model: str, timeout: int = 900, attempts: int = 4) -> str:
    """Dispatch a bulk-read task to Gemini CLI headless (stdin for large inputs).

    Two distinct failure modes, handled differently: a quota refusal is not
    flakiness — retrying it faster makes it worse — so we honour the server's
    own `retry in Ns` and do not count it against the attempt budget. Transport
    errors get ordinary bounded backoff.
    """
    last: Exception | None = None
    attempt = 0
    quota_waits = 0
    while attempt < attempts:
        try:
            return _gemini_once(prompt, model, timeout)
        except RateLimited as exc:
            quota_waits += 1
            if quota_waits > MAX_QUOTA_WAITS:
                raise RuntimeError(
                    f"gemini quota exhausted after {quota_waits} waits — "
                    f"free-tier limit reached, resume later"
                ) from exc
            delay = exc.retry_after + 5
            logger.warning("gemini rate-limited; sleeping %.0fs (wait %d/%d)",
                           delay, quota_waits, MAX_QUOTA_WAITS)
            time.sleep(delay)
        except (RuntimeError, subprocess.TimeoutExpired) as exc:
            attempt += 1
            last = exc
            if attempt < attempts:
                delay = 10 * (2 ** (attempt - 1))
                logger.warning("gemini attempt %d/%d failed (%s); retrying in %ds",
                               attempt, attempts, exc, delay)
                time.sleep(delay)
    raise RuntimeError(f"gemini failed after {attempts} attempts: {last}")


def _dump_raw(rf: ResearchFile, raw: str) -> Path:
    """Keep the unparseable response on disk — never debug a batch job blind."""
    EXTRACT_DIR.mkdir(parents=True, exist_ok=True)
    path = EXTRACT_DIR / f"_raw-{rf.slug}.txt"
    path.write_text(raw, encoding="utf-8")
    return path


def _extract_attempt(rf: ResearchFile, model: str) -> list[dict]:
    raw = run_gemini(build_prompt(rf), model, attempts=1)
    blob = _first_json_object(_strip_fence(raw))
    if blob is None:
        _dump_raw(rf, raw)
        raise ValueError(f"no JSON object in Gemini output (raw dumped, {len(raw)} chars)")
    try:
        data = json.loads(blob)
    except json.JSONDecodeError as exc:
        _dump_raw(rf, raw)
        raise ValueError(f"malformed JSON from Gemini (raw dumped): {exc}") from exc
    claims = data.get("claims")
    if not isinstance(claims, list) or not claims:
        raise ValueError("payload has no usable `claims` list")
    return claims


def extract_one(rf: ResearchFile, model: str, attempts: int = 4) -> dict[str, Any]:
    """Truncated responses are as common as transport errors on long dossiers,
    so the retry wraps the parse too — not just the call."""
    last: Exception | None = None
    claims: list[dict] = []
    for attempt in range(1, attempts + 1):
        try:
            claims = _extract_attempt(rf, model)
            break
        except (RuntimeError, ValueError, subprocess.TimeoutExpired) as exc:
            last = exc
            if attempt < attempts:
                delay = 5 * (2 ** (attempt - 1))
                logger.warning("extract %s attempt %d/%d failed (%s); retry in %ds",
                               rf.slug, attempt, attempts, exc, delay)
                time.sleep(delay)
    if not claims:
        raise RuntimeError(f"failed after {attempts} attempts: {last}")
    return {
        "video": rf.slug,
        "lifecycle": rf.lifecycle,
        "source_file": str(rf.path.relative_to(REPO)).replace("\\", "/"),
        "model": model,
        "extracted_at": date.today().isoformat(),
        "claims": claims,
    }


# --------------------------------------------------------------------------
# Validation — the fabrication guard
# --------------------------------------------------------------------------


def normalize(text: str) -> str:
    """Fold the differences that survive an honest copy/paste, and nothing else.

    Smart quotes, dashes, NBSP and runs of whitespace are normalized because a
    faithful copy can still trip on them. Words are never touched.
    """
    text = unicodedata.normalize("NFKC", text)
    for a, b in (
        ("‘", "'"), ("’", "'"), ("‚", "'"),
        ("“", '"'), ("”", '"'), ("„", '"'),
        ("–", "-"), ("—", "-"), ("−", "-"),
        (" ", " "), ("…", "..."),
    ):
        text = text.replace(a, b)
    # Markdown emphasis is medium formatting, not words: a model quoting a
    # dossier line drops the `**` almost every time. Removing only formatting
    # characters keeps the guard honest — a reworded quote still fails.
    text = re.sub(r"[*_`]+", "", text)
    return re.sub(r"\s+", " ", text).strip().lower()


def slugify(value: str) -> str:
    value = unicodedata.normalize("NFKD", str(value)).encode("ascii", "ignore").decode()
    value = re.sub(r"[^\w\s-]", "", value).strip().lower()
    value = re.sub(r"[\s_]+", "-", value)
    return re.sub(r"-{2,}", "-", value).strip("-")


@dataclass
class Claim:
    claim: str
    topics: list[str]
    source: str
    status: str
    video: str
    verbatim: str | None = None
    anchor: str | None = None
    verbatim_verified: bool = False
    #: True only when the matched text is a QUOTATION in the dossier (blockquote
    #: line or quote-wrapped), not the dossier's own summarising prose. Only
    #: quotations may be rendered as quotes downstream — see `is_quotation`.
    verbatim_is_quote: bool = False
    #: `citable` | `tertiary` | `vacuous` — see `classify_source`. Only citable
    #: claims count toward the cross-episode compounding metric.
    source_quality: str = "citable"
    flags: list[str] = field(default_factory=list)


@dataclass
class ValidationReport:
    kept: int = 0
    dropped: int = 0
    verbatim_ok: int = 0
    quotations: int = 0
    tertiary: int = 0
    vacuous: int = 0
    verbatim_stripped: int = 0
    flagged: int = 0
    reasons: dict[str, int] = field(default_factory=dict)

    def reject(self, reason: str) -> None:
        self.dropped += 1
        self.reasons[reason] = self.reasons.get(reason, 0) + 1


def is_quotation(verbatim: str, body_lines: list[str]) -> bool:
    """Distinguish a real quotation from the dossier's own summarising prose.

    An exact-substring match only proves the text came from the dossier — not
    that anyone said it. Rendering a research file's paraphrase inside quote
    marks would manufacture a quotation that no source ever uttered, which is
    the failure mode `/verify` 7.8 exists to catch. So a verbatim is treated as
    a quotation only when the dossier itself presents it as one: a `>` blockquote
    line, or text wrapped in quote marks.
    """
    stripped = verbatim.strip().strip("*_` ")
    if stripped.startswith('"') and stripped.rstrip(".").endswith('"'):
        return True
    target = normalize(verbatim)
    if not target:
        return False
    for line in body_lines:
        if not line.lstrip().startswith(">"):
            continue
        if target in normalize(line.lstrip().lstrip(">")):
            return True
    # Quoted run inside a bullet, e.g. Cathcart "did not read Arabic, ...".
    for line in body_lines:
        for quoted in re.findall(r'"([^"]{20,})"', line):
            if target in normalize(quoted) or normalize(quoted) in target:
                return True
    return False


#: Sources that name no one. A claim attributed to "multiple academic sources"
#: is unciteable — it looks sourced while being impossible to check.
VACUOUS_SOURCE = re.compile(
    r"^\W*(multiple|various|several|many|numerous|assorted|other|secondary)\b[^.]{0,40}?"
    r"\b(sources?|scholars?|works?|authors?|texts?|accounts?|references?)\b"
    r"|^\W*(ibid|op\.? ?cit|as above|see above|passim|internal|dossier)\W*\.?$"
    # A retrieval tool is not a source. "NotebookLM" names where we looked,
    # not who said it, and a source note for it would assert an authority
    # that does not exist.
    r"|^\W*(notebooklm|nlm|notebook|google|gemini)\b.{0,30}$",
    re.I,
)

#: Below this a source slug is almost always an artifact of free-text
#: attribution ("British Somaliland protectorate, 1960" -> `british-1960`)
#: rather than a real recurring source.
MIN_CLAIMS_FOR_SOURCE_NOTE = 2

#: Tertiary reference works. Fine as scaffolding, never as on-screen provenance.
TERTIARY_SOURCE = re.compile(
    r"\b(wikipedia|wikimedia|britannica|encyclopa?edia|wiktionary|"
    r"encarta|infoplease|history\.com)\b",
    re.I,
)


def classify_source(source: str) -> str:
    """Grade an attribution: `citable`, `tertiary`, or `vacuous`.

    Rule 2 proves the attribution came from the dossier; it cannot tell whether
    the attribution is worth anything. A Phase-1 Wikipedia brief and a
    NotebookLM-verified dossier both pass Rule 2, and merging them silently
    would let scaffolding masquerade as verified research in the same note.
    """
    if not source.strip() or VACUOUS_SOURCE.match(source):
        return "vacuous"
    if TERTIARY_SOURCE.search(source):
        return "tertiary"
    return "citable"


def source_tokens(source: str) -> list[str]:
    """Distinctive tokens (surnames, years) that must be present in the dossier."""
    years = re.findall(r"\b(1[5-9]\d{2}|20[0-2]\d)\b", source)
    names = [w for w in re.findall(r"\b[A-Z][a-zA-ZÀ-ɏ'\-]{3,}", source)]
    return years[:2] + names[:3]


def validate_payload(
    payload: dict[str, Any], report: ValidationReport, rejects: list[dict]
) -> list[Claim]:
    """Read the dossier this payload came from and enforce the copy-only contract."""
    body = (REPO / payload["source_file"]).read_text(encoding="utf-8", errors="replace")
    return validate_claims(payload["claims"], body, payload["video"], report, rejects)


def validate_claims(
    raw_claims: Iterable[Any],
    body: str,
    video: str,
    report: ValidationReport,
    rejects: list[dict],
) -> list[Claim]:
    """Enforce the copy-only contract against `body`. Anything unverifiable is
    dropped or has its unverifiable part stripped — never silently passed."""
    body_norm = normalize(body)
    body_lines = body.splitlines()
    # Models routinely echo a heading without its `###` prefix — compare on the
    # heading text alone so a faithful copy is not rejected on punctuation.
    headings = {
        normalize(h.lstrip("# ").strip())
        for h in re.findall(r"^#{1,6} .*$", body, re.M)
    }

    kept: list[Claim] = []
    for raw in raw_claims:
        if not isinstance(raw, dict):
            report.reject("not-an-object")
            continue

        text = str(raw.get("claim", "")).strip()
        if not text:
            report.reject("empty-claim")
            continue
        words = len(text.split())
        if words > MAX_CLAIM_WORDS:
            report.reject("claim-not-atomic")
            rejects.append({"video": video, "reason": "claim-not-atomic", "claim": text})
            continue

        source = str(raw.get("source", "")).strip()
        if not source or source.lower() in {"null", "none", "n/a", "unknown"}:
            report.reject("no-source")
            rejects.append({"video": video, "reason": "no-source", "claim": text})
            continue

        # Rule 2: attribution must already exist in the dossier.
        tokens = source_tokens(source)
        if tokens and not any(normalize(t) in body_norm for t in tokens):
            report.reject("source-not-in-dossier")
            rejects.append(
                {"video": video, "reason": "source-not-in-dossier",
                 "claim": text, "source": source}
            )
            continue

        quality = classify_source(source)
        if quality == "tertiary":
            report.tertiary += 1
        elif quality == "vacuous":
            report.vacuous += 1

        status = str(raw.get("status", "")).strip().lower()
        if status not in STATUS_VALUES:
            status = "unverified"
        # A tertiary or unciteable attribution cannot support a "verified"
        # claim no matter what the dossier called it.
        if quality != "citable" and status == "verified":
            status = "partial"

        topics = [slugify(t) for t in (raw.get("topics") or []) if slugify(str(t))]
        if not topics:
            report.reject("no-topic")
            rejects.append({"video": video, "reason": "no-topic", "claim": text})
            continue
        topics = topics[:3]

        flags: list[str] = []
        if words > ATOMIC_CLAIM_WORDS:
            flags.append("verbose")

        # Rule 1: verbatim must be an exact copy, or it does not survive.
        verbatim = raw.get("verbatim")
        verbatim = str(verbatim).strip() if verbatim else ""
        verbatim_verified = False
        verbatim_is_quote = False
        if verbatim:
            if len(verbatim) < MIN_VERBATIM_CHARS:
                verbatim = ""
            elif normalize(verbatim) in body_norm:
                verbatim_verified = True
                verbatim_is_quote = is_quotation(verbatim, body_lines)
                report.verbatim_ok += 1
                if verbatim_is_quote:
                    report.quotations += 1
            else:
                # Fabricated or repaired quote. Drop the quote, keep the claim.
                rejects.append(
                    {"video": video, "reason": "verbatim-not-in-dossier",
                     "claim": text, "verbatim": verbatim[:300]}
                )
                verbatim = ""
                report.verbatim_stripped += 1
                flags.append("verbatim-stripped")

        anchor = str(raw.get("anchor", "")).strip().lstrip("# ").strip() or None
        if anchor and normalize(anchor) not in headings:
            anchor = None
            flags.append("anchor-unresolved")

        if flags:
            report.flagged += 1
        report.kept += 1
        kept.append(
            Claim(
                claim=text,
                topics=topics,
                source=source,
                status=status,
                video=video,
                verbatim=verbatim or None,
                anchor=anchor,
                verbatim_verified=verbatim_verified,
                verbatim_is_quote=verbatim_is_quote,
                source_quality=quality,
                flags=flags,
            )
        )
    return kept


def load_validated() -> tuple[list[Claim], ValidationReport]:
    report = ValidationReport()
    rejects: list[dict] = []
    claims: list[Claim] = []
    for path in sorted(EXTRACT_DIR.glob("*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        claims.extend(validate_payload(payload, report, rejects))
    if rejects:
        REJECT_LOG.parent.mkdir(parents=True, exist_ok=True)
        with REJECT_LOG.open("w", encoding="utf-8") as fh:
            for r in rejects:
                fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    return claims, report


# --------------------------------------------------------------------------
# Audit — catch tool-as-source at write time, not two episodes later
# --------------------------------------------------------------------------

#: Document-metadata lines describe the DOSSIER, not a claim. "Phase: 2
#: (Academic Verification - NotebookLM Complete)" records which tool ran the
#: research pass; it is not an attribution and must not be flagged.
METADATA_LABEL = re.compile(
    r"^\s*[-*]?\s*\**\s*(phase|status|completion|progress|updated|date"
    r"|verification rate|research phase|purpose|scope|video angle|notebook"
    r"|notebooklm|verification key|last updated)[^:]{0,30}[:—-]",
    re.I,
)


#: An explicit tier label means the dossier is already being honest about
#: leaning on a tertiary work. Flagging that would train people to HIDE
#: tertiary sources rather than label them — the opposite of what we want.
TIER_LABELLED = re.compile(r"\btier\s*[123]\b|\[T[123]\]|\bT[123]\b", re.I)

#: An archive that HOSTS a primary document is not a tertiary source. A
#: Wikimedia-hosted facsimile of a 1941 decree is a scan of the real thing.
ARCHIVE_HOST = re.compile(
    r"\b(commons|wikimedia|facsimile|scan|hosted|archive\.org|pd-|public domain)\b", re.I
)

#: `historian/WEB-POLICY.md` permits freely-accessible web sources (news,
#: Wikipedia, transcripts) **with the source URL captured inline**. So a
#: tertiary cite carrying a link is policy-compliant; the violation is the
#: uncheckable bare mention. Match the house rule rather than inventing a
#: stricter one the corpus was never written against.
HAS_URL = re.compile(r"https?://|\bwww\.", re.I)


@dataclass
class AuditFinding:
    video: str
    path: str
    line_no: int
    kind: str
    line: str


def attribution_segments(line: str) -> list[str]:
    """Pull the attribution-bearing parts out of a dossier line.

    `classify_source` is a FIELD-level classifier — its patterns are anchored to
    the start of a bare attribution string. Running it against a whole line
    silently matches nothing, because in practice attributions live inside table
    cells (`| 1704 attack dates | ... | Multiple NLM sources | ✅ |`) or behind a
    label (`**Sources:** Multiple academic sources confirm`). Extract those
    segments first, then classify each one properly.
    """
    # Quoted text is usually the myth being debunked, not our attribution — #57
    # quotes "Multiple older source maps which have not survived" while refuting it.
    line = re.sub(r'"[^"]*"|“[^”]*”', " ", line)

    segments: list[str] = []
    if "|" in line:
        segments += [c.strip() for c in line.split("|")]
    label = re.match(r"^\s*[-*]?\s*\**\s*sources?\s*\**\s*[:—-]\s*(.+)$", line, re.I)
    if label:
        segments.append(label.group(1).strip())
    # Trailing attribution after an em/en dash: "... — Multiple academic sources"
    for part in re.split(r"\s[—–]\s|\s--\s", line):
        segments.append(part.strip())
    return [s.strip(" *_`") for s in segments if s.strip(" *_`")]


def audit_dossier(path: Path, video: str) -> list[AuditFinding]:
    """Flag attributions that name a tool, a vague plural, or a tertiary work."""
    findings: list[AuditFinding] = []
    for i, raw in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#") or METADATA_LABEL.match(line):
            continue

        kind = None
        for seg in attribution_segments(line):
            quality = classify_source(seg)
            if quality == "vacuous":
                # A tool or a vague plural is never a legitimate attribution.
                kind = "tool-or-vague-plural"
                break
            if (
                quality == "tertiary"
                and not TIER_LABELLED.search(line)
                and not ARCHIVE_HOST.search(line)
                and not HAS_URL.search(line)
            ):
                kind = "unlabelled-tertiary"
        if kind is None:
            continue
        findings.append(
            AuditFinding(video, str(path.relative_to(REPO)).replace("\\", "/"),
                         i, kind, line[:160])
        )
    return findings


def cmd_audit(args: argparse.Namespace) -> int:
    files = discover()
    if args.only:
        files = [f for f in files if args.only in f.slug]
    findings: list[AuditFinding] = []
    for rf in files:
        findings.extend(audit_dossier(rf.path, rf.slug))

    blocking = [f for f in findings if f.kind == "tool-or-vague-plural"]
    advisory = [f for f in findings if f.kind != "tool-or-vague-plural"]

    def show(rows: list[AuditFinding]) -> None:
        by_video: dict[str, list[AuditFinding]] = {}
        for f in rows:
            by_video.setdefault(f.video, []).append(f)
        for video in sorted(by_video, key=lambda v: -len(by_video[v])):
            group = by_video[video]
            print(f"  {video}  ({len(group)})")
            for f in group[: args.max_per_file]:
                print(f"    {f.path}:{f.line_no}")
                print(f"        {f.line}")
            if len(group) > args.max_per_file:
                print(f"    … {len(group) - args.max_per_file} more")
            print()

    if blocking:
        print(f"❌ BLOCKING — {len(blocking)} attribution(s) name a tool or a vague plural\n")
        print("  A retrieval tool is not a source, and \"multiple academic sources\"")
        print("  names no one. These look sourced while being impossible to check.")
        print("  Trace each to the book or document it actually came from.\n")
        show(blocking)

    if advisory and not args.blocking_only:
        print(f"⚠️  ADVISORY — {len(advisory)} tertiary cite(s) without an inline URL\n")
        print("  `historian/WEB-POLICY.md` allows Wikipedia and news for modern")
        print("  anchors WITH the URL captured inline. These lack one on the same")
        print("  line — often fine (a nearby line carries it), so this never blocks.\n")
        show(advisory)

    if not blocking:
        print(f"✅ {len(files)} dossier(s) — no tool-as-source attributions")
    return 1 if blocking else 0


# --------------------------------------------------------------------------
# Taxonomy — the judgment layer
# --------------------------------------------------------------------------

TAXONOMY_PATH = TOPICS_DIR / "_taxonomy.json"


def load_taxonomy() -> tuple[dict[str, str], dict[str, str]]:
    """Return (alias -> canonical slug, canonical slug -> display title).

    Extraction invents a fresh slug per dossier, so the raw vocabulary explodes
    (~4 topics per claim, barely any reuse). Folding those into concepts is the
    one step that must NOT be automated — deciding that
    `colonial-boundary-inheritance` and `uti-possidetis-juris` are the same idea
    is the editorial call the whole exercise exists to make. Unmapped slugs
    survive as provisional rather than being guessed at.
    """
    if not TAXONOMY_PATH.exists():
        return {}, {}
    data = json.loads(TAXONOMY_PATH.read_text(encoding="utf-8"))
    alias_map: dict[str, str] = {}
    titles: dict[str, str] = {}
    for canonical, spec in data.get("canonical", {}).items():
        canonical = slugify(canonical)
        titles[canonical] = spec.get("title") or canonical.replace("-", " ").title()
        alias_map[canonical] = canonical
        for alias in spec.get("aliases", []):
            alias_map[slugify(alias)] = canonical
    return alias_map, titles


def collect_vocabulary() -> dict[str, dict[str, Any]]:
    """Raw topic slugs with usage counts — the input to taxonomy authoring."""
    claims, _ = load_validated()
    vocab: dict[str, dict[str, Any]] = {}
    for c in claims:
        for t in c.topics:
            entry = vocab.setdefault(t, {"claims": 0, "videos": set()})
            entry["claims"] += 1
            entry["videos"].add(c.video)
    return vocab


def cmd_vocab(args: argparse.Namespace) -> int:
    vocab = collect_vocabulary()
    alias_map, _ = load_taxonomy()
    rows = sorted(vocab.items(), key=lambda kv: (-kv[1]["claims"], kv[0]))
    if args.unmapped:
        rows = [(s, v) for s, v in rows if s not in alias_map]
    if args.json:
        print(json.dumps(
            {s: {"claims": v["claims"], "videos": sorted(v["videos"])} for s, v in rows},
            indent=1, ensure_ascii=False,
        ))
        return 0
    mapped = sum(1 for s in vocab if s in alias_map)
    print(f"{len(vocab)} raw slugs · {mapped} mapped · {len(vocab)-mapped} unmapped\n")
    for slug, v in rows:
        print(f"{v['claims']:4d}  {len(v['videos']):2d}ep  {slug}")
    return 0


# --------------------------------------------------------------------------
# Build — render topic + source notes
# --------------------------------------------------------------------------

STATUS_MARK = {"verified": "✅", "partial": "⏳", "unverified": "❓"}


def source_slug(source: str) -> str:
    """Collapse an attribution string to a stable source-note slug."""
    year = re.search(r"\b(1[5-9]\d{2}|20[0-2]\d)\b", source)
    name = re.search(r"\b([A-Z][a-zA-ZÀ-ɏ'\-]{3,})", source)
    parts = [p for p in (name.group(1) if name else None, year.group(1) if year else None) if p]
    return slugify("-".join(parts)) if parts else slugify(source)[:60]


def render_topic_note(
    slug: str,
    claims: list[Claim],
    title: str | None = None,
    provisional: bool = False,
    linkable: set[str] | None = None,
) -> str:
    """`linkable` is the set of source slugs that actually got a note. A claim
    whose attribution is free text ("Treaty text itself (Tier 1)") produces a
    junk slug; linking it would point at a page that does not exist and imply a
    source note we never wrote. Those render as plain text instead."""
    videos = sorted({c.video for c in claims})
    linkable = linkable if linkable is not None else set()
    sources = sorted({source_slug(c.source) for c in claims} & linkable)
    title = title or slug.replace("-", " ").title()

    lines = [
        "---",
        "type: topic",
        f"slug: {slug}",
        f"title: {title}",
        f"status: {'provisional' if provisional else 'canonical'}",
        f"claims: {len(claims)}",
        f"sources: {len(sources)}",
        f"videos: {len(videos)}",
        f"updated: {date.today().isoformat()}",
        "generated_by: tools/brain/topic_mine.py",
        "---",
        "",
        f"# {title}",
        "",
    ]
    if provisional:
        lines += [
            "> **Provisional topic** — this slug came straight out of extraction and",
            "> has not been folded into the taxonomy yet. It may duplicate a canonical",
            "> topic under a different name. Fold it in `_taxonomy.json`.",
            "",
        ]
    lines += [
        "> Topic note. Atomic claims re-filed from per-video verified research.",
        "> Each claim carries its attribution and the episode that verified it.",
        "> Generated — edit `01-VERIFIED-RESEARCH.md` upstream, or promote a claim",
        "> into `.brain/threads/` if it becomes your own argument.",
        "",
        "## Claims",
        "",
    ]

    def emit(group: list[Claim]) -> None:
        by_video: dict[str, list[Claim]] = {}
        for c in group:
            by_video.setdefault(c.video, []).append(c)
        for video in sorted(by_video):
            lines.append(f"### via [[{video}]]")
            lines.append("")
            for c in by_video[video]:
                mark = STATUS_MARK.get(c.status, "❓")
                sslug = source_slug(c.source)
                cite = f" · [[src-{sslug}]]" if sslug in linkable else ""
                lines.append(f"- {mark} {c.claim} — {c.source}{cite}")
                # Only dossier QUOTATIONS are rendered as quotes. Dossier prose
                # that matched exactly is still not something anyone said, so it
                # stays out of quote marks rather than being laundered into one.
                if c.verbatim and c.verbatim_is_quote:
                    quoted = c.verbatim.replace("\n", " ").strip().strip('"')
                    lines.append(f'  > "{quoted}"')
                if c.anchor:
                    lines.append(f"  · anchor: `{c.anchor.lstrip('# ').strip()}`")
            lines.append("")

    citable = [c for c in claims if c.source_quality == "citable"]
    weak = [c for c in claims if c.source_quality != "citable"]

    emit(citable)
    if not citable:
        lines += ["*(no citable claims — everything below is scaffolding)*", ""]

    if weak:
        lines += [
            "## Not citable",
            "",
            "Attributed to a tertiary reference work or to no one in particular",
            "(\"multiple academic sources\"). Usable as a lead, never as on-screen",
            "provenance — trace it to a real source before it goes near a script.",
            "",
        ]
        emit(weak)

    lines += ["## Sources", ""]
    lines += [f"- [[src-{s}]]" for s in sources] or ["*(no recurring source notes)*"]
    lines += ["", "## Episodes", ""]
    lines += [f"- [[{v}]]" for v in videos]
    lines.append("")
    return "\n".join(lines)


def render_source_note(slug: str, claims: list[Claim]) -> str:
    attributions = sorted({c.source for c in claims})
    topics = sorted({t for c in claims for t in c.topics})
    videos = sorted({c.video for c in claims})
    quotes = [c for c in claims if c.verbatim and c.verbatim_is_quote]

    lines = [
        "---",
        "type: source",
        f"slug: src-{slug}",
        f"claims: {len(claims)}",
        f"topics: {len(topics)}",
        f"updated: {date.today().isoformat()}",
        "generated_by: tools/brain/topic_mine.py",
        "---",
        "",
        f"# {slug.replace('-', ' ').title()}",
        "",
        "> Source note. What this source is cited for, across every episode.",
        "> Immutable: this is what they said, not what we concluded.",
        "",
        "## Attributions as filed",
        "",
    ]
    lines += [f"- {a}" for a in attributions]

    if quotes:
        lines += ["", "## Verified verbatim", ""]
        for c in quotes:
            lines.append(f'> "{c.verbatim.strip().strip(chr(34))}"')
            lines.append(f"> — {c.source} · via [[{c.video}]]")
            lines.append("")

    lines += ["## Topics this source supports", ""]
    lines += [f"- [[{t}]]" for t in topics]
    lines += ["", "## Episodes", ""]
    lines += [f"- [[{v}]]" for v in videos]
    lines.append("")
    return "\n".join(lines)


def _topic_rows(topics: dict[str, list[Claim]], slugs: Iterable[str]) -> list[str]:
    ranked = sorted(
        ((s, topics[s]) for s in slugs),
        key=lambda kv: (-len({c.video for c in kv[1]}), -len(kv[1]), kv[0]),
    )
    rows = ["| Topic | Claims | Episodes | Sources |", "|---|---|---|---|"]
    for slug, claims in ranked:
        vids = len({c.video for c in claims})
        srcs = len({source_slug(c.source) for c in claims})
        rows.append(f"| [[{slug}]] | {len(claims)} | {vids} | {srcs} |")
    return rows


def render_index(
    topics: dict[str, list[Claim]],
    sources: dict[str, list[Claim]],
    provisional: set[str] | None = None,
) -> str:
    provisional = provisional or set()
    canonical = [s for s in topics if s not in provisional]
    # Compounding is measured on citable claims only — two Wikipedia mentions
    # of the same concept is not knowledge accumulating.
    cross = [
        s for s in topics
        if len({c.video for c in topics[s] if c.source_quality == "citable"}) > 1
    ]
    lines = [
        "---",
        "type: index",
        f"updated: {date.today().isoformat()}",
        "generated_by: tools/brain/topic_mine.py",
        "---",
        "",
        "# Topic Index",
        "",
        f"{len(topics)} topics ({len(canonical)} canonical, {len(provisional)} provisional) · "
        f"{len(sources)} sources · {sum(len(v) for v in topics.values())} claim-links, "
        f"mined from per-video `01-VERIFIED-RESEARCH.md`.",
        "",
        "## Cross-episode topics",
        "",
        "Where knowledge is actually compounding — the same concept verified from",
        "more than one dossier. These are the cheapest places to start the next script,",
        "and the honest measure of whether this layer is earning its keep.",
        "",
    ]
    lines += _topic_rows(topics, cross) if cross else ["*(none yet)*"]

    if canonical:
        lines += ["", "## Canonical topics", ""]
        lines += _topic_rows(topics, canonical)
    if provisional:
        lines += [
            "",
            "## Provisional topics",
            "",
            "Straight out of extraction, not yet folded into `_taxonomy.json`.",
            "Expect duplicates under different names.",
            "",
        ]
        lines += _topic_rows(topics, sorted(provisional))
    lines.append("")
    return "\n".join(lines)


def build(dry_run: bool = False) -> dict[str, Any]:
    claims, report = load_validated()
    alias_map, titles = load_taxonomy()

    # Fold each claim's topics to canonical form ONCE, in place. Source notes
    # also link topics, so leaving raw slugs on the claim would emit links to
    # note names that the fold renamed out of existence.
    provisional: set[str] = set()
    for c in claims:
        folded: list[str] = []
        for raw in c.topics:
            slug = alias_map.get(raw, raw)
            if raw not in alias_map:
                provisional.add(slug)
            if slug not in folded:
                folded.append(slug)
        c.topics = folded

    topics: dict[str, list[Claim]] = {}
    for c in claims:
        for slug in c.topics:
            topics.setdefault(slug, []).append(c)
    # A claim can reach the same canonical topic via two aliases — dedupe.
    for slug, group in topics.items():
        seen: set[tuple[str, str]] = set()
        deduped = []
        for c in group:
            key = (c.video, c.claim)
            if key not in seen:
                seen.add(key)
                deduped.append(c)
        topics[slug] = deduped

    all_sources: dict[str, list[Claim]] = {}
    for c in claims:
        # "Multiple academic sources" is not a source; giving it a note would
        # manufacture an authority that does not exist.
        if c.source_quality == "vacuous":
            continue
        all_sources.setdefault(source_slug(c.source), []).append(c)
    # Free-text attributions produce a long tail of one-off slugs. Writing a
    # note per singleton would fill `.brain/sources/` with hundreds of stubs
    # that look authoritative and carry one line each — worse than not writing
    # them. The claims keep their attribution inline either way.
    sources = {
        k: v for k, v in all_sources.items() if len(v) >= MIN_CLAIMS_FOR_SOURCE_NOTE
    }

    stats = {
        "claims": len(claims),
        "topics": len(topics),
        "canonical_topics": len(topics) - len(provisional),
        "provisional_topics": len(provisional),
        "sources": len(sources),
        "attributions_total": len(all_sources),
        "attributions_singleton": len(all_sources) - len(sources),
        "cross_episode_topics": sum(
            1 for v in topics.values()
            if len({c.video for c in v if c.source_quality == "citable"}) > 1
        ),
        "tertiary_claims": sum(1 for c in claims if c.source_quality == "tertiary"),
        "vacuous_claims": sum(1 for c in claims if c.source_quality == "vacuous"),
        "validation": asdict(report),
    }
    if dry_run:
        return stats

    TOPICS_DIR.mkdir(parents=True, exist_ok=True)
    SOURCES_DIR.mkdir(parents=True, exist_ok=True)
    # Notes are fully derived — clear stale ones so a renamed or folded topic
    # does not linger as a ghost file that still looks authoritative.
    for old in list(TOPICS_DIR.glob("*.md")) + list(SOURCES_DIR.glob("src-*.md")):
        old.unlink()
    for slug, group in topics.items():
        (TOPICS_DIR / f"{slug}.md").write_text(
            render_topic_note(
                slug, group, titles.get(slug), slug in provisional, set(sources)
            ),
            encoding="utf-8",
        )
    for slug, group in sources.items():
        (SOURCES_DIR / f"src-{slug}.md").write_text(
            render_source_note(slug, group), encoding="utf-8"
        )
    (TOPICS_DIR / "INDEX.md").write_text(
        render_index(topics, sources, provisional), encoding="utf-8"
    )
    return stats


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------


def cmd_scan(_: argparse.Namespace) -> int:
    files = discover()
    total = sum(f.size for f in files)
    done = sum(1 for f in files if f.extracted)
    print(f"{len(files)} research files · {total/1024:.0f} KB · {done} already extracted\n")
    for f in files:
        mark = "✓" if f.extracted else " "
        print(f" {mark} {f.size/1024:7.1f} KB  {f.lifecycle:<20} {f.slug}")
    return 0


def cmd_extract(args: argparse.Namespace) -> int:
    EXTRACT_DIR.mkdir(parents=True, exist_ok=True)
    files = discover()
    if args.only:
        files = [f for f in files if args.only in f.slug]
    if not args.force:
        files = [f for f in files if not f.extracted]
    if args.limit:
        files = files[: args.limit]

    if not files:
        print("nothing to extract")
        return 0

    SCRATCH_CWD.mkdir(parents=True, exist_ok=True)
    ok = fail = 0
    for i, rf in enumerate(files, 1):
        if i > 1:
            time.sleep(REQUEST_SPACING_S)
        print(f"[{i}/{len(files)}] {rf.slug} ({rf.size/1024:.0f} KB) ... ", end="", flush=True)
        try:
            payload = extract_one(rf, args.model)
        except Exception as exc:  # noqa: BLE001 — report, never silently skip
            fail += 1
            print(f"FAILED: {type(exc).__name__}: {exc}")
            logger.error("extraction failed for %s: %s", rf.slug, exc)
            continue
        rf.extract_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8"
        )
        ok += 1
        print(f"{len(payload['claims'])} claims")
    print(f"\nextracted {ok} · failed {fail}")
    return 1 if fail and not ok else 0


def cmd_validate(_: argparse.Namespace) -> int:
    claims, report = load_validated()
    print(f"kept {report.kept} · dropped {report.dropped} · flagged {report.flagged}")
    print(f"verbatim verified {report.verbatim_ok} · stripped {report.verbatim_stripped} "
          f"· real quotations {report.quotations}")
    print(f"source quality: tertiary {report.tertiary} · unciteable {report.vacuous}")
    if report.reasons:
        print("\ndrop reasons:")
        for reason, n in sorted(report.reasons.items(), key=lambda kv: -kv[1]):
            print(f"  {n:5d}  {reason}")
    if REJECT_LOG.exists():
        print(f"\nrejects logged: {REJECT_LOG.relative_to(REPO)}")
    return 0


def cmd_build(args: argparse.Namespace) -> int:
    stats = build(dry_run=args.dry_run)
    print(json.dumps(stats, indent=2))
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("scan", help="list research files and extraction status").set_defaults(func=cmd_scan)

    p_ex = sub.add_parser("extract", help="dispatch bulk extraction to Gemini")
    p_ex.add_argument("--only", help="substring match on project slug")
    p_ex.add_argument("--limit", type=int, help="max files this run")
    p_ex.add_argument("--model", default=DEFAULT_MODEL)
    p_ex.add_argument("--force", action="store_true", help="re-extract already-done files")
    p_ex.set_defaults(func=cmd_extract)

    sub.add_parser("validate", help="run the fabrication guard, report only").set_defaults(func=cmd_validate)

    p_a = sub.add_parser("audit", help="flag attributions that name a tool instead of a source")
    p_a.add_argument("--only", help="substring match on project slug")
    p_a.add_argument("--max-per-file", type=int, default=6, dest="max_per_file")
    p_a.add_argument("--blocking-only", action="store_true", dest="blocking_only",
                     help="suppress the advisory tertiary section")
    p_a.set_defaults(func=cmd_audit)

    p_v = sub.add_parser("vocab", help="raw topic slugs by frequency (input to taxonomy authoring)")
    p_v.add_argument("--unmapped", action="store_true", help="only slugs absent from _taxonomy.json")
    p_v.add_argument("--json", action="store_true")
    p_v.set_defaults(func=cmd_vocab)

    p_b = sub.add_parser("build", help="render topic + source notes")
    p_b.add_argument("--dry-run", action="store_true")
    p_b.set_defaults(func=cmd_build)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
