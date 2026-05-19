"""Internal regex parser for POST-PUBLISH-ANALYSIS.md files.

Consolidates the two diverged parsers previously in:
  - tools/youtube_analytics/feedback_parser.py
  - tools/youtube_analytics/patterns.py

Field-name and unit decisions (see PostPublishReport docstring for the full contract):
  - Retention values stored as PERCENT (e.g. 28.1), matching the source markdown.
    Callers wanting the 0–1 form use PostPublishReport.avg_retention_fraction.
  - CTR stored as PERCENT (e.g. 4.2). Field name is `ctr_percent`; the legacy
    name `ctr` is exposed as a property on the dataclass.
  - Drop points stored as list of dicts (position_pct, viewers_lost_pct, location),
    matching the existing downstream shape used by PerformanceTracker.

Private module — callers use PostPublishStore, not these functions directly.
"""
from __future__ import annotations

import re
from typing import Any, Dict, List, Optional


def extract_video_id(content: str, filepath: str = "") -> Optional[str]:
    """Return the 11-char video ID from markdown header or filename, else None."""
    m = re.search(r"\*\*Video ID:\*\*\s*([\w-]+)", content)
    if m:
        return m.group(1)
    if filepath:
        m = re.search(r"POST-PUBLISH-ANALYSIS-([\w-]+)\.md", filepath)
        if m:
            return m.group(1)
    return None


def extract_title(content: str) -> Optional[str]:
    """Return the video title from `# Post-Publish Analysis: <title>` or generic H1."""
    m = re.search(r"^#\s+Post-Publish Analysis:\s*(.+)$", content, re.MULTILINE)
    if m:
        return m.group(1).strip()
    m = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
    if m:
        return m.group(1).strip()
    return None


def extract_analyzed_date(content: str) -> Optional[str]:
    """Return ISO timestamp from `**Analyzed:** ...` line, or None."""
    m = re.search(r"\*\*Analyzed:\*\*\s*(\S+)", content)
    return m.group(1) if m else None


def extract_metrics(content: str) -> Dict[str, Any]:
    """Extract numeric performance metrics.

    Returns a dict with these keys (None for missing values):
        avg_retention_pct, final_retention_pct, ctr_percent, impressions,
        views, watch_time_minutes, subscribers_gained
    """
    metrics: Dict[str, Any] = {
        "avg_retention_pct": None,
        "final_retention_pct": None,
        "ctr_percent": None,
        "impressions": None,
        "views": None,
        "watch_time_minutes": None,
        "subscribers_gained": None,
    }

    m = re.search(r"\*\*Average retention:\*\*\s*([\d.]+)%", content)
    if m:
        metrics["avg_retention_pct"] = float(m.group(1))

    m = re.search(r"\*\*Final retention:\*\*\s*([\d.]+)%", content)
    if m:
        metrics["final_retention_pct"] = float(m.group(1))

    # CTR — prefer header line, fall back to most recent CTR History row.
    m = re.search(r"\*\*CTR:\*\*\s*([\d.]+)%", content)
    if m:
        metrics["ctr_percent"] = float(m.group(1))
    else:
        history = re.findall(r"\|\s*\d{4}-\d{2}-\d{2}\s*\|\s*([\d.]+)%", content)
        if history:
            metrics["ctr_percent"] = float(history[-1])

    # Impressions — prefer header line, fall back to CTR History or perf table.
    m = re.search(r"\*\*Impressions:\*\*\s*([\d,]+)", content)
    if m:
        metrics["impressions"] = int(m.group(1).replace(",", ""))
    else:
        history = re.findall(
            r"\|\s*\d{4}-\d{2}-\d{2}\s*\|\s*[\d.]+%\s*\|\s*([\d,]+)", content
        )
        if history:
            metrics["impressions"] = int(history[-1].replace(",", ""))
        else:
            m = re.search(r"\|\s*Impressions\s*\|\s*([\d,]+)", content, re.IGNORECASE)
            if m:
                metrics["impressions"] = int(m.group(1).replace(",", ""))

    # Views from Performance table — "This Video" column.
    m = re.search(r"\|\s*Views\s*\|\s*([\d,]+)\s*\|", content)
    if m:
        metrics["views"] = int(m.group(1).replace(",", ""))

    # Watch time — patterns.py-style permissive match.
    m = re.search(r"\|\s*Watch Time.*?\|\s*([\d,]+)", content, re.IGNORECASE)
    if m:
        metrics["watch_time_minutes"] = float(m.group(1).replace(",", ""))

    m = re.search(r"\|\s*Subscribers\s*\|\s*\+?([\d,]+)\s*\|", content)
    if m:
        metrics["subscribers_gained"] = int(m.group(1).replace(",", ""))

    return metrics


def extract_lessons(content: str) -> Dict[str, List[str]]:
    """Return {'observations': [...], 'actionable': [...]} from Lessons section."""
    out: Dict[str, List[str]] = {"observations": [], "actionable": []}

    m = re.search(
        r"### Observations\s*\n\n(.*?)(?:\n\n###|\n\n\*\*|\Z)",
        content,
        re.DOTALL,
    )
    if m:
        lines = [ln.strip() for ln in m.group(1).split("\n") if ln.strip().startswith("-")]
        out["observations"] = [ln.lstrip("- ").strip() for ln in lines if ln]

    m = re.search(
        r"### Actionable Items\s*\n\n(.*?)(?:\n\n##|\Z)",
        content,
        re.DOTALL,
    )
    if m:
        lines = [ln.strip() for ln in m.group(1).split("\n") if ln.strip().startswith("-")]
        out["actionable"] = [
            re.sub(r"^-\s*\[[ x]\]\s*", "", ln).strip() for ln in lines if ln
        ]

    return out


def extract_drop_points(content: str) -> List[Dict[str, Any]]:
    """Return list of drop-off points: {position_pct, viewers_lost_pct, location}."""
    return [
        {
            "position_pct": int(m.group(1)),
            "viewers_lost_pct": float(m.group(2)),
            "location": m.group(3).strip(),
        }
        for m in re.finditer(
            r"\|\s*(\d+)%\s*\|\s*([\d.]+)%\s*dropped\s*\|\s*([^|]+)\s*\|",
            content,
        )
    ]


def extract_discovery_diagnosis(content: str) -> Optional[Dict[str, Optional[str]]]:
    """Return diagnosis dict from Discovery Diagnostics section, or None."""
    section = re.search(
        r"## Discovery Diagnostics\s*\n\n(.*?)(?:\n\n##|\Z)", content, re.DOTALL
    )
    if not section:
        return None
    text = section.group(1)

    diagnosis: Dict[str, Optional[str]] = {
        "summary": None,
        "primary_issue": None,
        "severity": None,
    }

    m = re.search(r"\*\*Diagnosis:\*\*\s*([^\n]+)", text)
    if m:
        diagnosis["summary"] = m.group(1).strip()

    m = re.search(r"\*\*Primary Issue:\*\*\s*([^(]+)(?:\(Severity:\s*(\w+)\))?", text)
    if m:
        diagnosis["primary_issue"] = m.group(1).strip()
        diagnosis["severity"] = m.group(2).strip() if m.group(2) else "UNKNOWN"

    return diagnosis if any(diagnosis.values()) else None