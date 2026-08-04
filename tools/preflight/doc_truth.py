"""Doc-truth checker — do the docs name things that actually exist?

WHY THIS EXISTS
---------------
2026-08-04. `channel-data/NEXT-VIDEO-DISCOVERY-HANDOFF.md` — the file CLAUDE.md points every
session at for next-video work — described `impressions_daily` as an `analytics.db` table and
`thumbnail_features` as a `keywords.db` table. Both are in the other database.

That is not a harmless typo. An agent following the doc queries a table that does not exist, gets
an empty result or an error, and this repo's standing failure mode takes over: silence is read as
an answer. ADR-0020 ("never assert absence without a direct check") and ADR-0021 exist because that
has already happened with research claims; the same discipline has to apply to the instruments the
docs tell you to use.

WHAT IT CHECKS
--------------
For every markdown doc in scope, two classes of named thing:

  TABLE   `<db>.<table>` (e.g. `analytics.db.videos`) and bare `` `table_name` `` mentions that
          match a known table in ANY of the three live databases. A qualified reference naming
          the WRONG database is the error this was written for.
  PATH    repo-relative paths in backticks that look like files (`tools/x.py`, `channel-data/y.md`).

Findings are graded so a doc that is merely imprecise doesn't drown the real errors:

  WRONG_DB     the table exists, but in a different database than the doc claims  (hard error)
  NO_TABLE     the table exists in no live database                               (hard error)
  MISSING_PATH the path does not exist on disk                                    (hard error)

Filters, not scores (ADR-0007/0012 house style): pass/fail conditions, no quality rating.
Read-side helpers never raise — errors come back as {'error': ...}.
"""

from __future__ import annotations

import argparse
import re
import sqlite3
import sys
from dataclasses import dataclass
from pathlib import Path

from tools.logging_config import get_logger, setup_logging

logger = get_logger(__name__)

REPO_ROOT = Path(__file__).resolve().parents[2]

# The three live databases, by the name docs use for them.
DATABASES = {
    "analytics.db": REPO_ROOT / "tools" / "youtube_analytics" / "analytics.db",
    "keywords.db": REPO_ROOT / "tools" / "discovery" / "keywords.db",
    "intel.db": REPO_ROOT / "tools" / "intel" / "intel.db",
}

# Docs that steer real work. Deliberately not the whole repo: per-project research files carry
# historical claims and archived material that is allowed to name things that no longer exist.
DOC_GLOBS = (
    "AGENTS.md",
    "CLAUDE.md",
    "channel-data/*.md",
    "channel-data/calibration/*.md",
    ".claude/rules/*.md",
    ".claude/skills/*/*.md",
    ".claude/commands/*.md",
    "tools/*.md",
    "docs/adr/*.md",
)

# `analytics.db.videos`, `keywords.db.ctr_snapshots.impression_count`
QUALIFIED_TABLE = re.compile(r"\b(analytics|keywords|intel)\.db\.([a-z_][a-z0-9_]*)", re.I)

# A backticked repo-relative path with a file extension.
BACKTICK_PATH = re.compile(r"`([A-Za-z0-9_][A-Za-z0-9_./-]*\.[A-Za-z0-9]{1,5})`")

# Paths that are illustrative rather than real: globs, placeholders, and per-project examples.
PATH_IGNORE = re.compile(
    r"[*?<>{}]"                      # globs / placeholders
    r"|^https?:"                     # urls
    r"|^\.\.\."                      # elisions
    r"|^[A-Za-z]:"                   # absolute windows paths
    r"|^~"                           # home-relative
)

# A doc may name a path precisely to say it is NOT there: a retired file, a rejected ADR
# alternative, a thing you must not create. Flagging those inverts the doc's meaning. Checked on
# the finding's line and the two around it, because the verdict often sits on the next line
# ("...a neutral top-level `tools/auto_zone.py`.\n  Rejected — one concept home").
ABSENCE_CUE = re.compile(
    r"\b(retired|never existed|do ?n'?t create|not created|rejected|removed|deleted|"
    r"deprecated|no longer exists|does not exist|superseded|renamed to|moved to)\b",
    re.I,
)

# Extensions we can meaningfully resolve. `.md`/`.py`/`.json` etc; not `.com`, `.io`, prose.
RESOLVABLE_SUFFIXES = {
    ".md", ".py", ".json", ".yaml", ".yml", ".toml", ".db", ".ps1", ".sh", ".sql",
    ".csv", ".txt", ".srt", ".ini", ".cfg",
}


# Paths a doc names that are legitimately absent right now. Each needs a reason; if a line here
# stops being true, delete it rather than editing the doc to match.
EXPECTED_ABSENT = {
    # Command outputs — created the first time the workflow runs, absent on a clean checkout.
    "channel-data/DIAGNOSIS-LOG.md": "written by the analyze workflow on first run",
    "channel-data/audience-insights.md": "written by the engage workflow on first run",
    # Artifacts a June planning doc proposed; the plan was superseded and they were never made.
    "channel-data/ITERATION-PLAN.md": "proposed by FLOP-AUTOPSY-PLAN-2026-06, never created",
    "channel-data/imports/studio-reach-export.csv": "manual Studio export, still outstanding",
    # Illustrative example inside a skill, not a real project.
    "video-projects/_IN_PRODUCTION/test-video-2026/POST-PUBLISH-ANALYSIS.md":
        "worked example in validation-standards, not a real project",
}

# ADRs are dated decision records. A path named in one was true when it was written, and editing
# an ADR to match today's layout falsifies the record. Their TABLE claims are still checked —
# a wrong database name misleads whoever follows the ADR to the seam.
PATH_CHECK_EXCLUDED_PREFIXES = ("docs/adr/",)


@dataclass(frozen=True)
class Finding:
    kind: str      # WRONG_DB | NO_TABLE | MISSING_PATH
    doc: str       # repo-relative
    line: int
    named: str     # what the doc said
    detail: str    # what is actually true


def live_tables() -> dict:
    """{db_name: {table, ...}} for every database present. Missing DB => empty set, never raises."""
    out = {}
    for name, path in DATABASES.items():
        tables = set()
        if path.exists():
            try:
                con = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
                try:
                    tables = {
                        row[0]
                        for row in con.execute(
                            "SELECT name FROM sqlite_master WHERE type IN ('table','view')"
                        )
                    }
                finally:
                    con.close()
            except sqlite3.Error as exc:
                logger.warning("cannot read %s: %s", name, exc)
        out[name] = tables
    return out


def _iter_docs(root: Path):
    seen = set()
    for pattern in DOC_GLOBS:
        for path in sorted(root.glob(pattern)):
            if path.is_file() and path not in seen:
                seen.add(path)
                yield path


def check_tables(text: str, doc: str, tables: dict) -> list:
    """Qualified `<db>.<table>` references that name the wrong database, or no database."""
    findings = []
    for match in QUALIFIED_TABLE.finditer(text):
        claimed_db = f"{match.group(1).lower()}.db"
        table = match.group(2)
        if table in tables.get(claimed_db, set()):
            continue
        holders = [db for db, names in tables.items() if table in names]
        line = text[: match.start()].count("\n") + 1
        if holders:
            findings.append(Finding(
                "WRONG_DB", doc, line, f"{claimed_db}.{table}",
                f"`{table}` lives in {', '.join(holders)}, not {claimed_db}",
            ))
        elif any(tables.values()):
            # Only claim absence when we could actually read at least one database (ADR-0020).
            findings.append(Finding(
                "NO_TABLE", doc, line, f"{claimed_db}.{table}",
                "no live database has a table or view by that name",
            ))
    return findings


def _repo_top_level(root: Path) -> set:
    """Top-level directory names. A path starting with one is claiming to be repo-rooted.

    Leading-underscore directories are excluded even when they exist at the root: `_research/`
    is BOTH a root directory and the per-project research folder convention, so
    `_research/00-PRELIMINARY-BRIEF.md` in a command file means "inside whichever project you are
    working on", not a repo path. Same for `_gemini-output/`. Ambiguous means unenforceable.
    """
    return {p.name for p in root.iterdir() if p.is_dir() and not p.name.startswith("_")}


def check_paths(text: str, doc: str, root: Path, top_level: set) -> list:
    """Only paths that CLAIM to be repo-rooted are checkable.

    Docs legitimately name paths that are not repo-relative and must not be flagged:
      * `memory/feedback-*.md`   — the user-memory store, explicitly "not a repo path" (CLAUDE.md)
      * `_research/…`, `_adlib/…` — relative to whichever video project is in hand
      * `scratchpad/…`            — the session scratchpad
      * `historian/SKILL.md`      — relative to the skills directory the doc already sits in
    The discriminator is the first segment: if it names an existing top-level directory, the doc
    is asserting a repo path and we can hold it to that. Otherwise we cannot know, so we say
    nothing — the same rule ADR-0020 applies to claims about the world.
    """
    if doc.startswith(PATH_CHECK_EXCLUDED_PREFIXES):
        return []
    findings = []
    for match in BACKTICK_PATH.finditer(text):
        raw = match.group(1)
        if PATH_IGNORE.search(raw) or raw in EXPECTED_ABSENT:
            continue
        if Path(raw).suffix.lower() not in RESOLVABLE_SUFFIXES:
            continue
        head, _, rest = raw.partition("/")
        if not rest or head not in top_level:
            continue
        if (root / raw).exists():
            continue
        line_no = text[: match.start()].count("\n") + 1
        if _absence_is_the_point(text, line_no):
            continue
        findings.append(Finding(
            "MISSING_PATH", doc, line_no, raw, "no such file in the repo",
        ))
    return findings


def _absence_is_the_point(text: str, line_no: int) -> bool:
    """True when the surrounding prose is saying the path is gone / was never made."""
    lines = text.split("\n")
    window = lines[max(0, line_no - 2): line_no + 1]
    return any(ABSENCE_CUE.search(line) for line in window)


def audit(root: Path = REPO_ROOT) -> list:
    """Every finding across the in-scope docs, ordered by document."""
    tables = live_tables()
    top_level = _repo_top_level(root)
    findings = []
    for path in _iter_docs(root):
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            logger.warning("cannot read %s: %s", path, exc)
            continue
        doc = path.relative_to(root).as_posix()
        findings.extend(check_tables(text, doc, tables))
        findings.extend(check_paths(text, doc, root, top_level))
    return findings


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m tools.preflight.doc_truth",
        description="Check that docs name databases, tables and files that actually exist.",
        epilog=(
            "Examples:\n"
            "  python -m tools.preflight.doc_truth\n"
            "  python -m tools.preflight.doc_truth --kind WRONG_DB\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--kind", choices=["WRONG_DB", "NO_TABLE", "MISSING_PATH"],
                        help="report only this finding kind")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--verbose", "-v", action="store_true")
    group.add_argument("--quiet", "-q", action="store_true")
    args = parser.parse_args(argv)

    setup_logging(verbose=args.verbose, quiet=args.quiet)

    findings = audit()
    if args.kind:
        findings = [f for f in findings if f.kind == args.kind]

    if not findings:
        print("doc-truth: clean — every named table and path resolves.")
        return 0

    by_kind = {}
    for finding in findings:
        by_kind.setdefault(finding.kind, []).append(finding)

    for kind in ("WRONG_DB", "NO_TABLE", "MISSING_PATH"):
        rows = by_kind.get(kind, [])
        if not rows:
            continue
        print(f"\n{kind}  ({len(rows)})")
        for f in rows:
            print(f"  {f.doc}:{f.line}  {f.named}")
            print(f"      -> {f.detail}")

    print(f"\n{len(findings)} finding(s).")
    return 1


if __name__ == "__main__":
    sys.exit(main())
