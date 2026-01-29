#!/usr/bin/env python3
"""
VidIQ Guided Workflow - Manual data collection prompts

Since VidIQ has no public API, this provides structured prompts
for manual data entry from VidIQ's web interface.

Part of Phase 13-03 (Discovery Tools - Metadata Integration)
"""

import argparse
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional


def generate_vidiq_prompts(topic: str, project_folder: Optional[str] = None) -> Dict:
    """
    Generate step-by-step VidIQ data collection prompts.

    Args:
        topic: Topic/keyword to research
        project_folder: Optional project folder path

    Returns:
        Dict with structured prompts for 3 steps
    """
    return {
        'topic': topic,
        'project_folder': project_folder,
        'timestamp': datetime.now().isoformat(),
        'steps': [
            {
                'step': 1,
                'title': 'Search Primary Keyword',
                'instructions': [
                    f'1. Go to VidIQ Keyword Inspector',
                    f'2. Search for: "{topic}"',
                    f'3. Record the following data:'
                ],
                'data_points': [
                    {
                        'field': 'search_volume',
                        'label': 'Search Volume',
                        'description': 'Monthly searches',
                        'example': '12000'
                    },
                    {
                        'field': 'competition',
                        'label': 'Competition Score',
                        'description': 'VidIQ competition rating (0-100)',
                        'example': '67'
                    },
                    {
                        'field': 'overall_score',
                        'label': 'Overall Score',
                        'description': 'VidIQ keyword score (0-100)',
                        'example': '54'
                    },
                    {
                        'field': 'trend',
                        'label': 'Trend',
                        'description': 'Growing, Stable, or Declining',
                        'example': 'Stable'
                    }
                ]
            },
            {
                'step': 2,
                'title': 'Check Related Keywords',
                'instructions': [
                    f'1. In VidIQ Keyword Inspector, scroll to "Related Keywords"',
                    f'2. Look for keywords with:',
                    f'   - High search volume (>1000/month)',
                    f'   - Low competition (<50)',
                    f'   - Relevant to your topic',
                    f'3. Record top 5-10 related keywords'
                ],
                'data_points': [
                    {
                        'field': 'related_keywords',
                        'label': 'Related Keywords',
                        'description': 'List of related keywords with their scores',
                        'example': 'medieval misconceptions (vol: 3200, comp: 45, score: 62)\nmedieval myths debunked (vol: 1800, comp: 52, score: 58)'
                    }
                ]
            },
            {
                'step': 3,
                'title': 'Analyze Competitors',
                'instructions': [
                    f'1. Search YouTube for: "{topic}"',
                    f'2. Click VidIQ browser extension on top 3-5 videos',
                    f'3. For each video, record:'
                ],
                'data_points': [
                    {
                        'field': 'competitor_videos',
                        'label': 'Competitor Videos',
                        'description': 'Top performing videos with their stats',
                        'example': 'Title: "Medieval History Explained"\nChannel: History Channel\nViews: 450K\nTags: medieval, history, middle ages\nVidIQ Score: 72'
                    }
                ]
            }
        ]
    }


def format_vidiq_prompts_markdown(prompts: Dict) -> str:
    """
    Format prompts as readable markdown.

    Args:
        prompts: Prompts from generate_vidiq_prompts()

    Returns:
        Formatted markdown string
    """
    lines = []
    lines.append(f"# VidIQ Research Workflow: {prompts['topic']}")
    lines.append("")
    lines.append(f"**Topic:** {prompts['topic']}")
    if prompts['project_folder']:
        lines.append(f"**Project:** {prompts['project_folder']}")
    lines.append(f"**Started:** {prompts['timestamp']}")
    lines.append("")
    lines.append("---")
    lines.append("")

    for step_data in prompts['steps']:
        lines.append(f"## Step {step_data['step']}: {step_data['title']}")
        lines.append("")

        # Instructions
        for instruction in step_data['instructions']:
            lines.append(instruction)
        lines.append("")

        # Data points
        lines.append("### Data to Collect")
        lines.append("")
        for point in step_data['data_points']:
            lines.append(f"**{point['label']}** (`{point['field']}`)")
            lines.append(f"- {point['description']}")
            lines.append(f"- Example: `{point['example']}`")
            lines.append("")

        lines.append("---")
        lines.append("")

    # Instructions for saving
    lines.append("## Saving Your Data")
    lines.append("")
    lines.append("After collecting data from all 3 steps:")
    lines.append("")
    lines.append("```bash")
    if prompts['project_folder']:
        lines.append(f'python vidiq_workflow.py "{prompts["topic"]}" --save --project-folder "{prompts["project_folder"]}"')
    else:
        lines.append(f'python vidiq_workflow.py "{prompts["topic"]}" --save')
    lines.append("```")
    lines.append("")
    lines.append("You'll be prompted to paste your collected data.")
    lines.append("")

    return '\n'.join(lines)


def parse_vidiq_response(response_text: str, step: int) -> Dict:
    """
    Parse user's pasted VidIQ data.

    Basic parser - accepts key:value format.

    Args:
        response_text: User's pasted data
        step: Which step (1, 2, or 3)

    Returns:
        Parsed data dict
    """
    data = {'step': step, 'raw': response_text}

    # Simple key:value parser
    for line in response_text.strip().split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip().lower().replace(' ', '_')
            value = value.strip()
            data[key] = value

    return data


def save_vidiq_data(topic: str, data: Dict, project_folder: Optional[str] = None) -> str:
    """
    Save VidIQ data to JSON file.

    Args:
        topic: Topic researched
        data: Collected data
        project_folder: Optional project folder

    Returns:
        Path to saved file
    """
    # Determine save location
    if project_folder:
        project_path = Path(project_folder)
        save_path = project_path / 'vidiq-research.json'
    else:
        # Fallback to channel-data
        save_path = Path('channel-data') / 'vidiq-research' / f'{topic.replace(" ", "-")}.json'
        save_path.parent.mkdir(parents=True, exist_ok=True)

    # Add metadata
    output = {
        'topic': topic,
        'timestamp': datetime.now().isoformat(),
        'project_folder': project_folder,
        'data': data
    }

    # Save
    with open(save_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2)

    return str(save_path)


def interactive_data_collection(topic: str, project_folder: Optional[str] = None) -> Dict:
    """
    Interactively collect VidIQ data from user.

    Args:
        topic: Topic to research
        project_folder: Optional project folder

    Returns:
        Collected data dict
    """
    prompts = generate_vidiq_prompts(topic, project_folder)
    collected_data = {}

    print(f"\nVidIQ Research: {topic}")
    print("=" * 60)

    for step_data in prompts['steps']:
        print(f"\n### Step {step_data['step']}: {step_data['title']}")
        print()

        for instruction in step_data['instructions']:
            print(instruction)
        print()

        print("Data to collect:")
        for point in step_data['data_points']:
            print(f"  - {point['label']}: {point['description']}")
        print()

        input(f"Press Enter when you've collected Step {step_data['step']} data...")

        print(f"\nPaste your data for Step {step_data['step']} (press Ctrl+D or Ctrl+Z when done):")
        print("Format: key: value (one per line)")
        print()

        lines = []
        try:
            while True:
                line = input()
                lines.append(line)
        except EOFError:
            pass

        response_text = '\n'.join(lines)
        step_data_parsed = parse_vidiq_response(response_text, step_data['step'])
        collected_data[f'step_{step_data["step"]}'] = step_data_parsed

    return collected_data


def main():
    parser = argparse.ArgumentParser(
        description='VidIQ guided workflow for manual data collection',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate research prompts
  python vidiq_workflow.py "medieval history"

  # Generate prompts for specific project
  python vidiq_workflow.py "dark ages myth" --project-folder "video-projects/_IN_PRODUCTION/19-flat-earth-medieval-2025"

  # Interactive data collection
  python vidiq_workflow.py "medieval history" --save

  # Save to specific project
  python vidiq_workflow.py "dark ages myth" --save --project-folder "video-projects/_IN_PRODUCTION/19-flat-earth-medieval-2025"
        """
    )

    parser.add_argument('topic', help='Topic/keyword to research')
    parser.add_argument('--project-folder', help='Project folder path')
    parser.add_argument('--save', action='store_true', help='Interactive data collection mode')
    parser.add_argument('--json', action='store_true', help='Output prompts as JSON')

    args = parser.parse_args()

    if args.save:
        # Interactive collection
        print("\n" + "="*60)
        print("VidIQ Guided Workflow - Interactive Data Collection")
        print("="*60)
        print("\nThis will guide you through collecting VidIQ data manually.")
        print("Have VidIQ open in your browser before starting.")
        print()

        data = interactive_data_collection(args.topic, args.project_folder)
        save_path = save_vidiq_data(args.topic, data, args.project_folder)

        print(f"\n\nData saved to: {save_path}")

    else:
        # Generate prompts only
        prompts = generate_vidiq_prompts(args.topic, args.project_folder)

        if args.json:
            print(json.dumps(prompts, indent=2))
        else:
            print(format_vidiq_prompts_markdown(prompts))


if __name__ == '__main__':
    main()
