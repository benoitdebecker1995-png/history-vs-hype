"""Import a manual YouTube Studio CSV export into analytics.db.

The Analytics API does not expose CTR for this channel, so lifetime / custom-range
CTR only exists via a manual Studio "Advanced mode → Export" CSV. This loads that
file into studio_ctr_imports / studio_ctr_rows (schema v5), separately from the
rolling Reporting metric in videos.ctr_percent — they are different measurements.

Key rules (Codex spec §1.D):
  - `--as-of` is REQUIRED; measurement time is never inferred from file mtime.
  - date-range imports require `--start` and `--end`.
  - each CSV is content-hashed, so re-importing the same file is idempotent.
  - headers, duplicate video_ids, non-negative impressions and CTR range validated.
  - unmatched rows (video_id not in the videos table) are stored but reported.

Usage:
    python -m tools.youtube_analytics.studio_import <csv> --as-of 2026-07-23
    python -m tools.youtube_analytics.studio_import <csv> --as-of 2026-07-23 \\
        --surface browse --start 2026-06-25 --end 2026-07-23
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from tools.logging_config import get_logger
from tools.youtube_analytics.store import ANALYTICS_DB, AnalyticsStore
from tools.youtube_analytics.growth_data import ensure_schema

logger = get_logger(__name__)

_ID_COL = "Content"
_TITLE_COL = "Video title"
_IMPR_COL = "Impressions"
_CTR_COL = "Impressions click-through rate (%)"
_REQUIRED = {_ID_COL, _IMPR_COL, _CTR_COL}
_VALID_SURFACES = {"overall", "browse", "suggested", "search", "other"}


class StudioImportError(ValueError):
    """Raised for a malformed CSV or invalid arguments — nothing is written."""


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_studio_csv(path: Path) -> List[Dict[str, Any]]:
    """Parse + validate the CSV into row dicts. Skips the Total row. Pure — no DB.

    Raises StudioImportError on a missing header, duplicate video_id, negative
    impressions, or a CTR outside [0, 100].
    """
    with open(path, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        headers = set(reader.fieldnames or [])
        missing = _REQUIRED - headers
        if missing:
            raise StudioImportError(f"CSV missing required columns: {sorted(missing)}")

        rows: List[Dict[str, Any]] = []
        seen: set = set()
        for raw in reader:
            vid = (raw.get(_ID_COL) or "").strip()
            if not vid or vid.lower() == "total":
                continue
            if vid in seen:
                raise StudioImportError(f"duplicate video_id in CSV: {vid}")
            seen.add(vid)
            try:
                impr = int(float((raw.get(_IMPR_COL) or "0").replace(",", "")))
                ctr = float((raw.get(_CTR_COL) or "0").replace(",", ""))
            except ValueError as e:
                raise StudioImportError(f"non-numeric impressions/CTR for {vid}: {e}")
            if impr < 0:
                raise StudioImportError(f"negative impressions for {vid}: {impr}")
            if not (0.0 <= ctr <= 100.0):
                raise StudioImportError(f"CTR out of range for {vid}: {ctr}")
            rows.append({
                "video_id": vid,
                "video_title": (raw.get(_TITLE_COL) or "").strip() or None,
                "impressions": impr,
                "ctr_percent": ctr,
            })
    if not rows:
        raise StudioImportError("no data rows found (only Total / empty?)")
    return rows


def import_studio_csv(
    csv_path: Path,
    *,
    as_of: str,
    surface: str = "overall",
    start: Optional[str] = None,
    end: Optional[str] = None,
    analytics_db: Path = ANALYTICS_DB,
) -> Dict[str, Any]:
    """Import one Studio CSV. Idempotent by content hash. Returns a summary dict.

    Does not overwrite videos.ctr_percent (rolling) — Studio lifetime/range is a
    separate measurement stored in its own tables.
    """
    csv_path = Path(csv_path)
    if surface not in _VALID_SURFACES:
        raise StudioImportError(f"surface must be one of {sorted(_VALID_SURFACES)}")
    window_kind = "date_range" if (start or end) else "lifetime"
    if window_kind == "date_range" and not (start and end):
        raise StudioImportError("date-range imports require both --start and --end")

    rows = parse_studio_csv(csv_path)
    sha = _sha256(csv_path)

    import sqlite3
    conn = sqlite3.connect(str(analytics_db))
    ensure_schema(conn)   # make sure v5 tables exist
    conn.close()

    with AnalyticsStore.open(analytics_db) as store:
        if store.studio_import_exists(sha):
            logger.info("CSV already imported (sha %s…) — skipping.", sha[:12])
            return {"status": "duplicate", "sha256": sha, "rows": len(rows)}

        known = set(store.videos_by_id([r["video_id"] for r in rows]).keys())
        unmatched = [r["video_id"] for r in rows if r["video_id"] not in known]

        import_id = store.insert_studio_import(
            source_sha256=sha, source_filename=csv_path.name, exported_at=as_of,
            imported_at=datetime.now(timezone.utc).isoformat(), window_kind=window_kind,
            period_start=start, period_end=end, surface=surface, rows=rows,
            unmatched_count=len(unmatched),
        )
        store.commit()

    if unmatched:
        logger.warning("%d/%d rows did not match a known video: %s",
                       len(unmatched), len(rows), ", ".join(unmatched[:10]))
    return {
        "status": "imported", "import_id": import_id, "sha256": sha,
        "rows": len(rows), "matched": len(rows) - len(unmatched),
        "unmatched": len(unmatched), "surface": surface,
        "window_kind": window_kind, "as_of": as_of,
    }


def main(argv: Optional[List[str]] = None) -> int:
    p = argparse.ArgumentParser(description="Import a YouTube Studio CSV export.")
    p.add_argument("csv", type=Path)
    p.add_argument("--as-of", required=True,
                   help="Measurement date (YYYY-MM-DD). Required — never inferred.")
    p.add_argument("--surface", default="overall", choices=sorted(_VALID_SURFACES))
    p.add_argument("--start", default=None, help="Date-range start (with --end)")
    p.add_argument("--end", default=None, help="Date-range end (with --start)")
    args = p.parse_args(argv)
    try:
        result = import_studio_csv(
            args.csv, as_of=args.as_of, surface=args.surface,
            start=args.start, end=args.end,
        )
    except StudioImportError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2
    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
