"""Claim-status checker — graded evidence discipline for research files.

WHY THIS EXISTS
---------------
The repo's research vocabulary was binary (✅ VERIFIED / ⏳ PENDING / ❌ FAILED). A binary
vocabulary forces premature commitment: the moment a researcher finds something, the only
available marks are "verified" or "pending", so they mark verified — and retract later.

On 2026-07-30, project #66 produced seven such reversals in one session (a claim marked
REFUTED then qualified; a "no text layer" conclusion that was a path bug; a duration finding
retracted for sample contamination; an availability claim taken from a search hit instead of
metadata; and a research "hinge" declared RESOLVED using one commission's data to adjudicate a
dispute about the reliability of that same commission's data).

None of those were dishonesty. All of them were a vocabulary with no evidence thresholds
attached. This module attaches them.

THE LADDER (each rung names what it costs to claim it)
------------------------------------------------------
  ASSERTED      Someone says it. No verification. (a model's output, a comment, a summary)
  SOURCED       Traced to a named source WITH a locator — but we have not opened it.
  INSPECTED     We opened the source and read the passage. Locator + date recorded.
  CORROBORATED  INSPECTED, plus a SECOND INDEPENDENT source agrees.
  CONTESTED     INSPECTED, and a named source disagrees. NOT a failure — most good history
                lives here, and saying so is the channel's whole product.
  SETTLED       CORROBORATED, plus the strongest opposing case has been read and answered.

BINDING RULES
-------------
  R1  Verdict words (REFUTED / PROVEN / RESOLVED / DISPROVED / CONFIRMED / SETTLED / ESTABLISHED)
      may only be applied to a claim at CORROBORATED or above.
  R2  CIRCULARITY: a claim cannot exceed INSPECTED if its only support comes from the same
      body/document whose reliability is what's in dispute. Mark `circular:` to declare it.
  R3  INSPECTED and above require a locator (page / section / archive ref / doc id).
  R4  SETTLED requires a named opposing case and where it was read (`opposed-by:`).
  R5  Nothing below CORROBORATED may go on screen.

Filters, not scores (ADR-0007/0012 house style): this returns pass/fail conditions. It does not
rate research quality. Read-side helpers never raise — errors come back as {'error': ...}.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from tools.logging_config import get_logger, safe_print, setup_logging  # noqa: E402

logger = get_logger(__name__)

LADDER = ["ASSERTED", "SOURCED", "INSPECTED", "CORROBORATED", "CONTESTED", "SETTLED"]
RANK = {s: i for i, s in enumerate(LADDER)}

# CONTESTED sits beside CORROBORATED in evidential weight, not above it.
WEIGHT = {
    "ASSERTED": 0,
    "SOURCED": 1,
    "INSPECTED": 2,
    "CONTESTED": 3,
    "CORROBORATED": 3,
    "SETTLED": 4,
}

VERDICT_WORDS = re.compile(
    r"\b(REFUTED|PROVEN|RESOLVED|DISPROVED|CONFIRMED|ESTABLISHED|SETTLED)\b"
)
STATUS_TAG = re.compile(r"\[(" + "|".join(LADDER) + r")\]")
# Page numbers may be arabic or roman: academic front matter (introductions,
# translators' prefaces) is roman-numbered, and those pages carry real quotations.
# The roman branch is the strict grammar, not just "letters from the roman set" —
# a loose [ivxlcdm]+ would read "p. civil" and "page did" as locators.
# The trailing (?![ivxlcdm]) is load-bearing twice over: it stops the numeral
# ending mid-token ("p. civil" -> "civ"), and because the strict grammar can match
# the empty string, it is also what prevents a zero-width match from passing.
_ROMAN = (
    r"(?=[ivxlcdm])m{0,3}(?:cm|cd|d?c{0,3})(?:xc|xl|l?x{0,3})"
    r"(?:ix|iv|v?i{0,3})(?![ivxlcdm])"
)
_PAGE_NO = r"(?:\d+|" + _ROMAN + r")"
LOCATOR = re.compile(
    r"(p\.\s*" + _PAGE_NO + r"|pp\.\s*" + _PAGE_NO + r"|page\s+" + _PAGE_NO + r"|"
    r"§|sec\.\s*\d+|ch\.\s*[IVXLC\d]+|"
    r"[A-Z]{2,4}\s*\d+/\d+|doc(ument)?\.?\s*\d+|archive|identifier|`[^`]+`)",
    re.I,
)
CIRCULAR = re.compile(r"circular\s*:", re.I)
OPPOSED = re.compile(r"opposed-by\s*:", re.I)
NEXT = re.compile(r"next\s*:\s*(.+?)(?:\s*\||$)", re.I)
NEXT_NONE = re.compile(r"next\s*:\s*none\b", re.I)

MIN_ON_SCREEN = "CORROBORATED"


def check_text(text: str, source_name: str = "<text>") -> Dict:
    """Check a research document. Never raises.

    Returns {'violations': [...], 'claims': N, 'by_status': {...}, 'verdict': 'PASS'|'FAIL'}
    """
    violations: List[Dict] = []
    by_status: Dict[str, int] = {s: 0 for s in LADDER}
    lines = text.splitlines()
    claims = 0

    for n, line in enumerate(lines, 1):
        tag = STATUS_TAG.search(line)
        if not tag:
            # A verdict word with no status tag anywhere on the line is itself a violation,
            # unless the line is prose *about* the ladder (contains "may only" / "requires").
            if VERDICT_WORDS.search(line) and not re.search(
                r"may only|requires|rule|ladder|vocabulary|R\d\b", line, re.I
            ):
                violations.append(
                    {
                        "line": n,
                        "rule": "R1",
                        "detail": "verdict word with no [STATUS] tag",
                        "text": line.strip()[:110],
                    }
                )
            continue

        claims += 1
        status = tag.group(1)
        by_status[status] += 1

        # R1 — verdict words need CORROBORATED-or-above weight
        if VERDICT_WORDS.search(line) and WEIGHT[status] < WEIGHT[MIN_ON_SCREEN]:
            violations.append(
                {
                    "line": n,
                    "rule": "R1",
                    "detail": f"verdict word at [{status}]; needs {MIN_ON_SCREEN}+",
                    "text": line.strip()[:110],
                }
            )

        # R2 — declared circularity caps at INSPECTED
        if CIRCULAR.search(line) and WEIGHT[status] > WEIGHT["INSPECTED"]:
            violations.append(
                {
                    "line": n,
                    "rule": "R2",
                    "detail": f"declared circular but marked [{status}]; caps at INSPECTED",
                    "text": line.strip()[:110],
                }
            )

        # R3 — INSPECTED+ needs a locator
        if WEIGHT[status] >= WEIGHT["INSPECTED"] and not LOCATOR.search(line):
            violations.append(
                {
                    "line": n,
                    "rule": "R3",
                    "detail": f"[{status}] with no locator (page/ref/id)",
                    "text": line.strip()[:110],
                }
            )

        # R4 — SETTLED needs a named opposing case
        if status == "SETTLED" and not OPPOSED.search(line):
            violations.append(
                {
                    "line": n,
                    "rule": "R4",
                    "detail": "[SETTLED] without `opposed-by:`",
                    "text": line.strip()[:110],
                }
            )

    return {
        "source": source_name,
        "claims": claims,
        "by_status": by_status,
        "violations": violations,
        "verdict": "FAIL" if violations else "PASS",
    }


def frontier(text: str, source_name: str = "<text>") -> Dict:
    """Definition of done for a research phase. Never raises.

    A research phase is NOT finished while any claim below CORROBORATED still has an
    available, untried route to raise it. Claims below CORROBORATED should therefore carry
    `next: <action>` — or `next: none — <reason>` to declare the thread genuinely closed.

    This exists because on 2026-07-30 research was reported as finished twice while
    obtainable sources remained unread; the owner had to ask "Why did you stop?" both times.

    Returns {'open': [...], 'closed': [...], 'untracked': [...], 'verdict': 'OPEN'|'COMPLETE'}
    """
    open_threads: List[Dict] = []
    closed: List[Dict] = []
    untracked: List[Dict] = []

    for n, line in enumerate(text.splitlines(), 1):
        tag = STATUS_TAG.search(line)
        if not tag:
            continue
        status = tag.group(1)
        if WEIGHT[status] >= WEIGHT[MIN_ON_SCREEN]:
            continue  # already strong enough; not a frontier item
        entry = {"line": n, "status": status, "text": line.strip()[:110]}
        if NEXT_NONE.search(line):
            closed.append(entry)
        elif (m := NEXT.search(line)):
            entry["next"] = m.group(1).strip()[:80]
            open_threads.append(entry)
        else:
            untracked.append(entry)

    return {
        "source": source_name,
        "open": open_threads,
        "closed": closed,
        "untracked": untracked,
        "verdict": "OPEN" if (open_threads or untracked) else "COMPLETE",
    }


def frontier_file(path: str) -> Dict:
    p = Path(path)
    if not p.exists():
        return {"error": f"no such file: {path}"}
    try:
        return frontier(p.read_text(encoding="utf-8", errors="replace"), str(p))
    except OSError as exc:
        return {"error": f"could not read {path}: {exc}"}


def format_frontier(res: Dict) -> str:
    if "error" in res:
        return f"ERROR: {res['error']}"
    out = [
        "=" * 72,
        "  RESEARCH FRONTIER  (is this phase actually finished?)",
        "=" * 72,
        f"  file: {res['source']}",
    ]
    if res["untracked"]:
        out.append(f"\n  UNTRACKED — below {MIN_ON_SCREEN}, no `next:` declared ({len(res['untracked'])}):")
        for e in res["untracked"]:
            out.append(f"    L{e['line']:<5} [{e['status']}] {e['text']}")
    if res["open"]:
        out.append(f"\n  OPEN THREADS ({len(res['open'])}):")
        for e in res["open"]:
            out.append(f"    L{e['line']:<5} [{e['status']}] next: {e['next']}")
    if res["closed"]:
        out.append(f"\n  CLOSED (declared `next: none`): {len(res['closed'])}")
    out.append(f"\n  VERDICT: {res['verdict']}")
    if res["verdict"] == "OPEN":
        out.append("  -> research is NOT finished. Do not report completion.")
    out.append("=" * 72)
    return "\n".join(out)


HYPE = {
    "superlative": re.compile(
        r"\b(strongest|biggest|greatest|best|most important|most valuable|single most|"
        r"decisive|definitive)\b",
        re.I,
    ),
    "awe": re.compile(
        r"\b(mother ?lode|crown jewel|spectacular|extraordinary|devastating|remarkable|"
        r"stunning|incredible|astonishing|superb|exceptional|goldmine|smoking gun)\b",
        re.I,
    ),
    "intensifier": re.compile(
        r"\b(genuinely|truly|utterly|absolutely|profoundly|enormously|hugely)\b", re.I
    ),
}
# House rule (CLAUDE.md § Calibration): at most ONE superlative claim per project.
SUPERLATIVE_BUDGET = 1


def tone(text: str, source_name: str = "<text>") -> Dict:
    """Count hyperbole in a written deliverable. A signal, not a gate. Never raises.

    Exists because on 2026-07-30 the owner wrote: "everything is the next best thing or the
    strongest find". Written files are countable even though chat is not — this closes half
    the gap, and the half it closes is the half that persists in the repo.
    """
    hits: Dict[str, List[Dict]] = {k: [] for k in HYPE}
    for n, line in enumerate(text.splitlines(), 1):
        if line.lstrip().startswith(("|", ">")) and "hype" in line.lower():
            continue  # don't flag this checker's own documentation
        for fam, rx in HYPE.items():
            for m in rx.finditer(line):
                hits[fam].append({"line": n, "term": m.group(0).lower(),
                                  "text": line.strip()[:90]})

    sup = len(hits["superlative"])
    over = sup > SUPERLATIVE_BUDGET
    return {
        "source": source_name,
        "counts": {k: len(v) for k, v in hits.items()},
        "hits": hits,
        "superlative_budget": SUPERLATIVE_BUDGET,
        "over_budget": over,
        "verdict": "OVER" if over else "OK",
    }


def format_tone(res: Dict) -> str:
    if "error" in res:
        return f"ERROR: {res['error']}"
    c = res["counts"]
    out = [
        "=" * 72,
        "  TONE CHECK  (signal, not a gate — hyperbole in written deliverables)",
        "=" * 72,
        f"  file: {res['source']}",
        f"  superlative {c['superlative']}  ·  awe {c['awe']}  ·  intensifier {c['intensifier']}",
        f"  budget: {res['superlative_budget']} superlative claim per project",
    ]
    for fam in ("superlative", "awe"):
        if res["hits"][fam]:
            out.append(f"\n  {fam.upper()}:")
            for h in res["hits"][fam][:12]:
                out.append(f"    L{h['line']:<5} \"{h['term']}\"  {h['text']}")
    out.append(f"\n  VERDICT: {res['verdict']}")
    if res["verdict"] == "OVER":
        out.append("  -> more than one superlative claim. Rank them; keep the one that changes")
        out.append("     the conclusion and state plainly what the others are.")
    out.append("=" * 72)
    return "\n".join(out)


def tone_file(path: str) -> Dict:
    p = Path(path)
    if not p.exists():
        return {"error": f"no such file: {path}"}
    try:
        return tone(p.read_text(encoding="utf-8", errors="replace"), str(p))
    except OSError as exc:
        return {"error": f"could not read {path}: {exc}"}


def check_file(path: str) -> Dict:
    """Check one file. Returns {'error': ...} rather than raising."""
    p = Path(path)
    if not p.exists():
        return {"error": f"no such file: {path}"}
    try:
        return check_text(p.read_text(encoding="utf-8", errors="replace"), str(p))
    except OSError as exc:
        return {"error": f"could not read {path}: {exc}"}


def format_report(result: Dict) -> str:
    if "error" in result:
        return f"ERROR: {result['error']}"
    out = [
        "=" * 72,
        "  CLAIM-STATUS CHECK  (filters — evidence thresholds, not a quality score)",
        "=" * 72,
        f"  file:   {result['source']}",
        f"  claims: {result['claims']}",
    ]
    counts = ", ".join(
        f"{s}={result['by_status'][s]}" for s in LADDER if result["by_status"][s]
    )
    out.append(f"  ladder: {counts or '(none tagged)'}")
    if result["violations"]:
        out.append(f"\n  VIOLATIONS ({len(result['violations'])}):")
        for v in result["violations"]:
            out.append(f"    L{v['line']:<5} [{v['rule']}] {v['detail']}")
            out.append(f"           {v['text']}")
    out.append(f"\n  VERDICT: {result['verdict']}")
    out.append("=" * 72)
    return "\n".join(out)


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(
        description="Claim-status checker — graded evidence discipline (ADR-0021)",
        epilog=(
            "Examples:\n"
            "  python -m tools.preflight.claim_status "
            "video-projects/_IN_PRODUCTION/66-.../01-VERIFIED-RESEARCH.md\n"
            "  python -m tools.preflight.claim_status --ladder\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("files", nargs="*", help="research markdown file(s) to check")
    ap.add_argument("--ladder", action="store_true", help="print the status ladder and exit")
    ap.add_argument(
        "--frontier",
        action="store_true",
        help="report unfinished threads instead of violations (definition of done)",
    )
    ap.add_argument(
        "--tone", action="store_true",
        help="count hyperbole in a written deliverable (signal, not a gate)",
    )
    g = ap.add_mutually_exclusive_group()
    g.add_argument("-v", "--verbose", action="store_true")
    g.add_argument("-q", "--quiet", action="store_true")
    args = ap.parse_args(argv)
    setup_logging(args.verbose, args.quiet)  # also hardens stdout against a narrow codepage

    # Every report below is printed via safe_print, not print. The reports echo raw
    # claim text, and the ladder doc below carries ✅ ⏳ ❌ — none of which cp1252 can
    # encode. This CLI's exit code is the completion gate in /research, so an
    # unprintable glyph must not become a research verdict. See configure_console_output.
    if args.ladder:
        safe_print(__doc__)
        return 0
    if not args.files:
        ap.error("give at least one file, or --ladder")

    failed = False
    for f in args.files:
        if args.tone:
            res = tone_file(f)
            safe_print(format_tone(res))
            if "error" in res:
                failed = True
        elif args.frontier:
            res = frontier_file(f)
            safe_print(format_frontier(res))
            if "error" in res or res["verdict"] == "OPEN":
                failed = True
        else:
            res = check_file(f)
            safe_print(format_report(res))
            if "error" in res or res["verdict"] == "FAIL":
                failed = True
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
