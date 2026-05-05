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
    # Add contracts here as each agent is schema-locked:
    # "claims-extractor": { ... },
    # "competitor-gap": { ... },
    # "research-organizer": { ... },
    # "fact-checker": { ... },
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

    # Surface sections in baseline not in check (regressions)
    if baseline.exists() and check.exists():
        baseline_h2 = set(extract_h2_sections(baseline.read_text(encoding="utf-8")))
        check_h2 = set(extract_h2_sections(check.read_text(encoding="utf-8")))
        dropped = baseline_h2 - check_h2
        added = check_h2 - baseline_h2
        if dropped:
            for s in sorted(dropped):
                issues.append(f"DROPPED section (regression): '{s}'")
        if added:
            for s in sorted(added):
                print(f"  INFO: new section added: '{s}'")

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
        label = f"DIFF: {baseline_path.name} → {check_path.name}"
    else:
        passed, issues = check_file(check_path, args.agent)
        label = f"CHECK: {check_path.name}"

    print(f"\n{label}")
    print(f"Agent: {args.agent}")
    print(f"Result: {'PASS' if passed else 'FAIL'}")

    if issues:
        print("\nIssues:")
        for issue in issues:
            print(f"  • {issue}")
    else:
        print("All required sections present.")

    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()
