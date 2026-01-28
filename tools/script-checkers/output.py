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
