"""
Daily modern-relevance hook hunter.

Reads channel-data/news-sources.yaml (RSS/Atom feeds) and scans the last
LOOKBACK_HOURS of articles. For each active project in
video-projects/_IN_PRODUCTION/, matches article title+summary against a
keyword list (either project_keyword_overrides in news-sources.yaml, or
auto-extracted from YOUTUBE-METADATA.md).

Any match becomes a candidate "modern relevance hook" — a current-event
anchor the script can open with or reference at the mid-point turn.

Outputs:
- channel-data/modern-relevance/YYYY-MM-DD.json   (machine-readable)
- channel-data/modern-relevance/YYYY-MM-DD.md     (human report)

CLI:
    python -m tools.routines.modern_relevance_scan
    python -m tools.routines.modern_relevance_scan --lookback-hours 48
"""

import argparse
import json
import re
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from urllib.request import Request, urlopen

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
SOURCES_FILE = REPO_ROOT / "channel-data" / "news-sources.yaml"
PRODUCTION_DIR = REPO_ROOT / "video-projects" / "_IN_PRODUCTION"
OUTPUT_DIR = REPO_ROOT / "channel-data" / "modern-relevance"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

USER_AGENT = "Mozilla/5.0 (compatible; HvHModernRelevance/1.0)"
ATOM_NS = "{http://www.w3.org/2005/Atom}"
LOOKBACK_HOURS_DEFAULT = 24
STOP_WORDS = {
    "that", "with", "they", "this", "from", "were", "have", "video",
    "their", "which", "about", "when", "your", "than", "what", "would",
    "there", "been", "will", "said", "into", "more", "also", "such",
    "over", "after", "these", "some", "because", "where", "those",
    "already", "country", "history", "between", "before", "through",
    "around", "without", "against", "should", "could", "might", "still",
}
# Words that come from YOUTUBE-METADATA.md file structure itself, not topic content
METADATA_BLOCKLIST = {
    "metadata", "youtube", "description", "title", "tags", "keywords",
    "thumbnail", "chapters", "timestamps", "category", "project", "status",
}


def fetch(url: str, timeout: int = 20) -> str:
    req = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="replace")


def parse_date(text: str) -> datetime | None:
    if not text:
        return None
    text = text.strip()
    try:
        return datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        pass
    try:
        dt = parsedate_to_datetime(text)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except (TypeError, ValueError):
        return None


def strip_tags(html: str) -> str:
    return re.sub(r"<[^>]+>", " ", html or "").strip()


def parse_feed(xml_text: str) -> list[dict]:
    """Handle both Atom and RSS 2.0."""
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        return []
    items = []
    # Atom
    for entry in root.findall(f"{ATOM_NS}entry"):
        title_el = entry.find(f"{ATOM_NS}title")
        summary_el = entry.find(f"{ATOM_NS}summary") or entry.find(f"{ATOM_NS}content")
        published_el = entry.find(f"{ATOM_NS}published") or entry.find(f"{ATOM_NS}updated")
        link_el = entry.find(f"{ATOM_NS}link")
        items.append({
            "title": (title_el.text or "").strip() if title_el is not None else "",
            "summary": strip_tags(summary_el.text) if summary_el is not None else "",
            "published": published_el.text if published_el is not None else "",
            "url": link_el.get("href") if link_el is not None else "",
        })
    # RSS 2.0
    for item in root.iter("item"):
        title_el = item.find("title")
        desc_el = item.find("description")
        pub_el = item.find("pubDate")
        link_el = item.find("link")
        items.append({
            "title": (title_el.text or "").strip() if title_el is not None else "",
            "summary": strip_tags(desc_el.text) if desc_el is not None else "",
            "published": pub_el.text if pub_el is not None else "",
            "url": (link_el.text or "").strip() if link_el is not None else "",
        })
    return items


def within_lookback(published: str, hours: int) -> bool:
    dt = parse_date(published)
    if dt is None:
        return True  # if we can't parse date, err on the side of including
    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
    return dt >= cutoff


def load_sources() -> dict:
    return yaml.safe_load(SOURCES_FILE.read_text(encoding="utf-8"))


def _clean_keyword(raw: str) -> str | None:
    kw = raw.strip().strip("*_`\"'").lower()
    kw = re.sub(r"\s+", " ", kw)
    if not kw or len(kw) < 4:
        return None
    # Reject keywords containing anything other than letters/numbers/spaces/hyphens
    if not re.fullmatch(r"[a-z0-9][a-z0-9 \-]{2,}", kw):
        return None
    if kw in STOP_WORDS or kw in METADATA_BLOCKLIST:
        return None
    return kw


def extract_keywords_from_metadata(text: str) -> list[str]:
    """Pull keywords from YOUTUBE-METADATA.md.

    Supports two formats:
      1. YAML-ish bullet list:   tags:\n  - foo\n  - bar
      2. Inline comma list:      **Keywords:** foo, bar, baz

    We intentionally do NOT auto-extract from prose — that yields generic noise.
    If a project lacks a keywords block, add one or use news-sources.yaml overrides.
    """
    keywords: list[str] = []
    # Normalise: strip markdown emphasis markers so **Keywords:** == Keywords:
    normalised = re.sub(r"\*+", "", text)

    # Format 1: bullet list under tags:/keywords:
    for m in re.finditer(
        r"(?:^|\n)\s*(?:tags|keywords)\s*[:]\s*\n((?:\s*[-*]\s*.+\n?)+)",
        normalised, re.I,
    ):
        for line in m.group(1).splitlines():
            kw = _clean_keyword(re.sub(r"^\s*[-*]\s*", "", line))
            if kw:
                keywords.append(kw)

    # Format 2: inline "Keywords: foo, bar, baz" on a single line
    for m in re.finditer(
        r"(?:^|\n)\s*(?:tags|keywords)\s*[:]\s*([^\n]+)",
        normalised, re.I,
    ):
        inline = m.group(1).strip()
        if not inline or inline.lstrip().startswith(("-", "*")):
            continue
        for part in re.split(r"[,;|]", inline):
            kw = _clean_keyword(part)
            if kw:
                keywords.append(kw)

    return sorted(set(keywords))


def active_projects(overrides: dict) -> list[dict]:
    projects = []
    if not PRODUCTION_DIR.exists():
        return projects
    for project_dir in PRODUCTION_DIR.iterdir():
        if not project_dir.is_dir():
            continue
        slug = project_dir.name
        if slug in overrides:
            keywords = [k.lower() for k in overrides[slug]]
        else:
            metadata = project_dir / "YOUTUBE-METADATA.md"
            if not metadata.exists():
                continue
            keywords = extract_keywords_from_metadata(
                metadata.read_text(encoding="utf-8", errors="replace")
            )
        if keywords:
            projects.append({"slug": slug, "keywords": keywords})
    return projects


def match_article(article: dict, keywords: list[str]) -> list[str]:
    haystack = f"{article['title']} {article['summary']}".lower()
    matched = [kw for kw in keywords if kw in haystack]
    return matched


def scan(lookback_hours: int) -> dict:
    config = load_sources()
    sources = config.get("sources", [])
    overrides = config.get("project_keyword_overrides", {}) or {}
    projects = active_projects(overrides)

    all_articles: list[dict] = []
    errors: list[dict] = []

    for src in sources:
        try:
            xml_text = fetch(src["url"])
        except Exception as e:
            errors.append({"source": src["name"], "error": f"{type(e).__name__}: {e}"})
            continue
        for item in parse_feed(xml_text):
            if not within_lookback(item["published"], lookback_hours):
                continue
            all_articles.append({**item, "source": src["name"], "category": src.get("category", "")})

    # Match articles against each project
    project_hits: dict[str, list[dict]] = {p["slug"]: [] for p in projects}
    for project in projects:
        for article in all_articles:
            matched = match_article(article, project["keywords"])
            if matched:
                project_hits[project["slug"]].append({**article, "matched_keywords": matched})

    return {
        "scanned_sources": len(sources) - len(errors),
        "total_articles": len(all_articles),
        "projects": projects,
        "hits": project_hits,
        "errors": errors,
    }


def render_report(today_str: str, result: dict) -> str:
    total_hits = sum(len(v) for v in result["hits"].values())
    lines = [
        f"# Modern-Relevance Scan — {today_str}",
        "",
        f"**Feeds scanned:** {result['scanned_sources']}",
        f"**Articles in window:** {result['total_articles']}",
        f"**Active projects:** {len(result['projects'])}",
        f"**Total matched hooks:** {total_hits}",
        f"**Errors:** {len(result['errors'])}",
        "",
    ]
    if total_hits == 0:
        lines.append("_No matches today. No new modern-relevance hooks surfaced._")
        lines.append("")

    for project in result["projects"]:
        slug = project["slug"]
        hits = result["hits"].get(slug, [])
        lines.append(f"## {slug}")
        lines.append(f"_Keywords: {', '.join(project['keywords'])}_")
        lines.append("")
        if not hits:
            lines.append("No hits today.")
            lines.append("")
            continue
        for h in hits:
            lines.append(f"### {h['title']}")
            lines.append(f"- **Source:** {h['source']} ({h.get('category', '')})")
            lines.append(f"- **Published:** {h.get('published', '')}")
            lines.append(f"- **URL:** {h.get('url', '')}")
            lines.append(f"- **Matched keywords:** {', '.join(h['matched_keywords'])}")
            if h.get("summary"):
                snippet = h["summary"][:300].replace("\n", " ")
                lines.append(f"- **Snippet:** {snippet}...")
            lines.append("")

    if result["errors"]:
        lines.append("## Errors")
        lines.append("")
        for e in result["errors"]:
            lines.append(f"- {e['source']}: {e['error']}")
        lines.append("")
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--lookback-hours", type=int, default=LOOKBACK_HOURS_DEFAULT)
    args = parser.parse_args()

    today = datetime.now().date().isoformat()
    print(f"Scanning news feeds (last {args.lookback_hours}h)...")
    result = scan(args.lookback_hours)

    (OUTPUT_DIR / f"{today}.json").write_text(
        json.dumps(result, indent=2), encoding="utf-8"
    )
    report = render_report(today, result)
    report_path = OUTPUT_DIR / f"{today}.md"
    report_path.write_text(report, encoding="utf-8")

    total_hits = sum(len(v) for v in result["hits"].values())
    print(f"Report: {report_path}")
    print(f"Matched hooks: {total_hits}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
