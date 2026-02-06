"""
Output Formatters for Script Quality Reports

Provides:
- OutputFormatter class with methods for markdown and JSON output
- Summary section generation
- Annotated script with inline [FLAG: ...] markers
"""

import json
from typing import Dict, List, Any


class OutputFormatter:
    """Format script checker results for display"""

    @staticmethod
    def format_summary(results: Dict[str, Any]) -> str:
        """
        Format summary section showing all checker results.

        Args:
            results: Dictionary with checker results
                {
                    'stumble': {'issues': [...], 'stats': {...}},
                    'scaffolding': {'issues': [...], 'stats': {...}}
                }

        Returns:
            Markdown-formatted summary
        """
        lines = ["# Script Quality Report", ""]
        lines.append("## Summary")
        lines.append("")

        for checker_name, data in results.items():
            if not data:
                continue

            issues = data.get('issues', [])
            stats = data.get('stats', {})

            # Count severity levels
            severity_counts = {}
            for issue in issues:
                sev = issue.get('severity', 'unknown')
                severity_counts[sev] = severity_counts.get(sev, 0) + 1

            # Format checker summary
            lines.append(f"### {checker_name.title()} Checker")
            lines.append(f"- **Total issues:** {len(issues)}")

            if severity_counts:
                for severity, count in sorted(severity_counts.items()):
                    emoji = {'high': '🔴', 'medium': '🟡', 'warning': '⚠️', 'ok': '✅'}.get(severity, '•')
                    lines.append(f"  - {emoji} {severity.title()}: {count}")

            # Add stats if available
            if stats:
                lines.append("- **Stats:**")
                for key, value in stats.items():
                    if isinstance(value, float):
                        lines.append(f"  - {key.replace('_', ' ').title()}: {value:.2f}")
                    else:
                        lines.append(f"  - {key.replace('_', ' ').title()}: {value}")

            lines.append("")

        return "\n".join(lines)

    @staticmethod
    def format_annotated_script(script: str, all_issues: Dict[str, List[Dict]]) -> str:
        """
        Format script with inline issue markers.

        Args:
            script: Original script text
            all_issues: Dictionary mapping checker names to issue lists
                {
                    'stumble': [
                        {'text': '...', 'reason': '...', 'severity': 'high'},
                        ...
                    ]
                }

        Returns:
            Annotated script with [FLAG: ...] markers
        """
        lines = ["## Annotated Script", ""]

        # Build list of all issues with positions
        annotations = []

        for checker_name, issues in all_issues.items():
            for issue in issues:
                # Extract text snippet to find in script
                text = issue.get('text', '')
                if not text:
                    continue

                # Find position in script
                pos = script.find(text)
                if pos == -1:
                    continue

                severity = issue.get('severity', 'unknown')
                reason = issue.get('reason', 'Issue detected')

                annotations.append({
                    'pos': pos,
                    'text': text,
                    'checker': checker_name,
                    'severity': severity,
                    'reason': reason
                })

        # Sort by position
        annotations.sort(key=lambda x: x['pos'])

        # Insert annotations (from end to start to preserve positions)
        annotated = script
        for ann in reversed(annotations):
            emoji = {'high': '🔴', 'medium': '🟡', 'warning': '⚠️'}.get(ann['severity'], '•')
            marker = f" [{emoji} FLAG: {ann['checker'].upper()} - {ann['reason']}]"

            # Insert after the flagged text
            insert_pos = ann['pos'] + len(ann['text'])
            annotated = annotated[:insert_pos] + marker + annotated[insert_pos:]

        lines.append(annotated)
        lines.append("")

        return "\n".join(lines)

    @staticmethod
    def format_full_report(script: str, results: Dict[str, Any], include_annotated: bool = True) -> str:
        """
        Generate complete report with summary and annotated script.

        Args:
            script: Original script text
            results: Checker results
            include_annotated: Whether to include annotated script (default True)

        Returns:
            Complete markdown report
        """
        sections = []

        # Summary section
        sections.append(OutputFormatter.format_summary(results))

        # Annotated script section (if requested)
        if include_annotated:
            all_issues = {}
            for checker_name, data in results.items():
                issues = data.get('issues', [])
                if issues:
                    all_issues[checker_name] = issues

            if all_issues:
                sections.append(OutputFormatter.format_annotated_script(script, all_issues))

        return "\n".join(sections)

    @staticmethod
    def format_json(results: Dict[str, Any]) -> str:
        """
        Format results as JSON.

        Args:
            results: Checker results

        Returns:
            JSON string
        """
        return json.dumps(results, indent=2)

    @staticmethod
    def format_pacing_report(pacing_result: Dict[str, Any], verbose: bool = False) -> str:
        """
        Format pacing analysis results as markdown report.

        Default mode shows problems-only (sections with score < 75).
        Verbose mode shows full section-by-section breakdown.

        Args:
            pacing_result: Pacing checker output dict with 'stats', 'issues', 'all_sections', 'advisories'
            verbose: If True, show full metrics table for all sections

        Returns:
            Markdown-formatted pacing report
        """
        stats = pacing_result.get('stats', {})
        verdict = stats.get('verdict', 'UNKNOWN')
        avg_score = stats.get('average_score', 0)
        energy_arc = stats.get('energy_arc', '')
        flat_zones = stats.get('flat_zones', [])
        flagged_count = stats.get('flagged_sections', 0)
        total_count = stats.get('total_sections', 0)

        lines = ["# Pacing Analysis", ""]

        # Handle SKIPPED verdict
        if verdict == 'SKIPPED':
            lines.append(f"**Verdict: {verdict}** — single-section script (no multi-section structure to analyze)")
            lines.append("")
            return "\n".join(lines)

        # Verdict and energy arc (always shown)
        lines.append(f"**Verdict: {verdict}** (avg score: {avg_score:.0f}/100)")
        if energy_arc:
            lines.append(f"**Energy arc:** {energy_arc}")
        lines.append("")

        # Short form for PASS with no verbose flag
        if verdict == 'PASS' and not verbose:
            lines.append("No sections flagged.")
            lines.append("")
            lines.append("---")
            lines.append(f"*{flagged_count} of {total_count} sections flagged | Threshold: score < 75*")
            lines.append("")
            return "\n".join(lines)

        # Verbose mode: show full metrics table
        if verbose:
            all_sections = pacing_result.get('all_sections', [])
            if all_sections:
                lines.append("## All Sections")
                lines.append("")
                lines.append("| Section | Score | Variance | Flesch | Flesch Delta | Entity Density |")
                lines.append("|---------|-------|----------|--------|--------------|----------------|")

                for section in all_sections:
                    name = section.get('section', 'Unknown')
                    score = section.get('score', 0)
                    variance = section.get('variance', 0)
                    flesch = section.get('flesch', 0)
                    flesch_delta = section.get('flesch_delta', 0)
                    entity_density = section.get('entity_density', 0)

                    # Format flesch_delta (em-dash for first section)
                    if flesch_delta == 0 and section == all_sections[0]:
                        delta_str = '—'
                    else:
                        delta_str = f"{flesch_delta:.1f}"

                    lines.append(f"| {name} | {score:.0f} | {variance:.1f} | {flesch:.1f} | {delta_str} | {entity_density:.2f} |")

                lines.append("")

        # Flagged sections (problems-only)
        issues = pacing_result.get('issues', [])
        if issues:
            lines.append("## Flagged Sections")
            lines.append("")

            for issue in issues:
                section_name = issue.get('section', 'Unknown')
                score = issue.get('score', 0)
                reasons = issue.get('reasons', [])

                lines.append(f"### Section: \"{section_name}\" (score: {score:.0f}/100)")

                for reason in reasons:
                    lines.append(f"- {reason}")

                lines.append("")

        # Energy notes (flat zones)
        if flat_zones:
            lines.append("## Energy Notes")
            for zone in flat_zones:
                lines.append(f"- {zone}")
            lines.append("")

        # Advisories (hooks, B-roll variety)
        advisories = pacing_result.get('advisories', [])
        if advisories:
            lines.append("## Advisories")
            for advisory in advisories:
                lines.append(f"- {advisory}")
            lines.append("")

        # Footer
        lines.append("---")
        lines.append(f"*{flagged_count} of {total_count} sections flagged | Threshold: score < 75*")
        lines.append("")

        return "\n".join(lines)
