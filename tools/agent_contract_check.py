"""
Agent contract checker — validates output schema before/after Gemini retrofits.

Usage:
  # Validate a single output file against an agent's contract
  python tools/agent_contract_check.py --check <output-path> --agent wiki-researcher

  # Diff two outputs (pre vs post retrofit)
  python tools/agent_contract_check.py --baseline <pre-path> --check <post-path> --agent wiki-researcher

  # List registered contracts
  python tools/agent_contract_check.py --list
"""

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent

# Per-agent schema contracts: exact H2 anchor strings that must be present.
# Anchors are prefix-matched (e.g., "## ACADEMIC SOURCES" matches "## ACADEMIC SOURCES (From...)")
CONTRACTS = {
    "wiki-researcher": {
        "output_path_pattern": "_research/00-PRELIMINARY-BRIEF.md",
        "required_h2_anchors": [
            "## EXECUTIVE SUMMARY",
            "## TIMELINE",
            "## KEY FIGURES",
            "## CLAIMS TO VERIFY",
            "## STANDARD NARRATIVE",
            "## UNDEREXPLORED ANGLES",
            "## MODERN RELEVANCE HOOKS",
            "## COMPETITOR LANDSCAPE",
            "## ACADEMIC SOURCES",
            "## DEBATES & CONTROVERSIES",
            "## PRE-VERIFIED CLAIMS",
            "## RECOMMENDED NEXT STEPS",
        ],
        "required_header_fields": [
            "**Generated:**",
            "**Sources:**",
            "**Time saved:**",
        ],
    },
    "claims-extractor": {
        "output_path_pattern": "CLAIMS-TO-VERIFY.md",
        "required_h2_anchors": [
            "# Claims to Verify",
            "## CLAIM CATEGORIZATION",
            "## MAJOR OMISSIONS",
            "## VERIFICATION PRIORITY",
            "## RESEARCH STRATEGY",
            "## NOTEBOOKLM PROMPT RECOMMENDATIONS",
            "## SCRIPT PLANNING NOTES",
            "## ESTIMATED VERIFICATION TIME",
        ],
        "required_header_fields": [
            "**Source:**",
            "**Format:**",
            "**Thesis:**",
        ],
    },
    "competitor-gap": {
        "output_path_pattern": "_research/COMPETITOR-GAP-ANALYSIS.md",
        "required_h2_anchors": [
            "# Competitor Gap Analysis",
            "## COMPETITOR VIDEOS",
            "## STANDARD NARRATIVE",
            "## KEY FIGURES MENTIONED",
            "## PRIMARY SOURCE ADVANTAGE",
            "## YOUR UNIQUE ANGLES",
            "## COMPETITOR-ONLY TOPICS",
            "## AGENT ASSESSMENT",
            "## RECOMMENDATION",
        ],
        "required_header_fields": [],
    },
    "research-organizer": {
        "output_path_pattern": "01-VERIFIED-RESEARCH.md",
        "required_h2_anchors": [
            "# ",
        ],
        "required_header_fields": [],
    },
    "fact-checker": {
        "output_path_pattern": "FACT-CHECK-VERIFICATION.md",
        "required_h2_anchors": [
            "# FACT-CHECK VERIFICATION",
            "## EXECUTIVE SUMMARY",
            "## DETAILED VERIFICATION",
            "## COUNTER-EVIDENCE VERIFICATION",
            "## CRITICAL FIXES REQUIRED",
            "## SOURCE QUALITY ASSESSMENT",
            "## VERIFICATION CONFIDENCE",
            "## STEELMAN VERIFICATION",
        ],
        "required_header_fields": [
            "**Script Verified:**",
            "**Verification Date:**",
            "**Status:**",
        ],
    },
}


def extract_h2_sections(content: str) -> list[str]:
    return re.findall(r"^## .+", content, re.MULTILINE)


def check_file(path: Path, agent: str) -> tuple[bool, list[str]]:
    """Returns (passed, list_of_issues)."""
    if agent not in CONTRACTS:
        return False, [f"No contract registered for agent '{agent}'. Run --list to see available."]

    contract = CONTRACTS[agent]
    issues = []

    if not path.exists():
        return False, [f"Output file not found: {path}"]

    content = path.read_text(encoding="utf-8")
    h2_sections = extract_h2_sections(content)

    # Check required H2 anchors (prefix match)
    for anchor in contract["required_h2_anchors"]:
        matched = any(s.startswith(anchor) for s in h2_sections)
        if not matched:
            issues.append(f"MISSING section: '{anchor}'")

    # Check required header fields
    for field in contract.get("required_header_fields", []):
        if field not in content:
            issues.append(f"MISSING header field: '{field}'")

    return len(issues) == 0, issues


def diff_files(baseline: Path, check: Path, agent: str) -> tuple[bool, list[str]]:
    """Compare sections present in baseline vs check output."""
    _, baseline_issues = check_file(baseline, agent)
    passed, check_issues = check_file(check, agent)

    issues = []
    if baseline_issues:
        issues.append(f"Baseline itself has issues: {baseline_issues}")
    if check_issues:
        issues.extend(check_issues)

    # Surface anchor-level differences only (informational; section title variation is allowed
    # as long as required anchors are present — that's already covered by check_file).
    if baseline.exists() and check.exists():
        baseline_h2 = extract_h2_sections(baseline.read_text(encoding="utf-8"))
        check_h2 = extract_h2_sections(check.read_text(encoding="utf-8"))

        def to_anchors(sections, contract_anchors):
            return {a for s in sections for a in contract_anchors if s.startswith(a)}

        anchors = CONTRACTS[agent]["required_h2_anchors"]
        baseline_anchors = to_anchors(baseline_h2, anchors)
        check_anchors = to_anchors(check_h2, anchors)

        # Sections present in baseline but not in any required anchor (extra in baseline)
        baseline_extra = [s for s in baseline_h2 if not any(s.startswith(a) for a in anchors)]
        check_extra = [s for s in check_h2 if not any(s.startswith(a) for a in anchors)]

        if baseline_extra:
            print(f"  INFO: baseline had {len(baseline_extra)} extra sections beyond contract")
        if check_extra:
            print(f"  INFO: check has {len(check_extra)} extra sections beyond contract: {check_extra}")

    return len(issues) == 0, issues


def main():
    parser = argparse.ArgumentParser(description="Agent output schema checker")
    parser.add_argument("--agent", required=True, help="Agent name (e.g. wiki-researcher)")
    parser.add_argument("--check", help="Output file to validate")
    parser.add_argument("--baseline", help="Pre-retrofit baseline file for diff comparison")
    parser.add_argument("--list", action="store_true", help="List registered contracts")
    args = parser.parse_args()

    if args.list:
        print("Registered agent contracts:")
        for name, contract in CONTRACTS.items():
            n = len(contract["required_h2_anchors"])
            print(f"  {name}: {n} required sections")
        sys.exit(0)

    if not args.check:
        parser.error("--check <output-path> is required")

    check_path = Path(args.check)

    if args.baseline:
        baseline_path = Path(args.baseline)
        passed, issues = diff_files(baseline_path, check_path, args.agent)
        label = f"DIFF: {baseline_path.name} -> {check_path.name}"
    else:
        passed, issues = check_file(check_path, args.agent)
        label = f"CHECK: {check_path.name}"

    print(f"\n{label}")
    print(f"Agent: {args.agent}")
    print(f"Result: {'PASS' if passed else 'FAIL'}")

    if issues:
        print("\nIssues:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("All required sections present.")

    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()
