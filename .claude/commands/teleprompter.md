# /teleprompter - Export Script for Filming

Export a SCRIPT.md to clean teleprompter-ready text.

## Usage

```
/teleprompter [project-path]
```

If no path provided, auto-detect from current context.

## What It Does

1. Reads SCRIPT.md from project folder
2. Strips all markdown formatting (`#`, `**`, `[]`, etc.)
3. Strips B-roll notes (`[B-ROLL: ...]`)
4. Strips source citations (`[SOURCE: ...]`)
5. Strips metadata (target length, framing notes)
6. Preserves paragraph breaks for pacing
7. Outputs to SCRIPT-TELEPROMPTER.txt in same folder

## Output

- **File:** `SCRIPT-TELEPROMPTER.txt`
- **Format:** Plain text, clean paragraphs
- **Content:** Spoken words only

## Example

```
/teleprompter video-projects/_IN_PRODUCTION/30-belavezha-accords-2025
```

Creates: `video-projects/_IN_PRODUCTION/30-belavezha-accords-2025/SCRIPT-TELEPROMPTER.txt`

## Process

```python
import re

def export_teleprompter(script_path):
    with open(script_path, 'r') as f:
        content = f.read()

    # Remove YAML frontmatter if present
    content = re.sub(r'^---.*?---\s*', '', content, flags=re.DOTALL)

    # Remove markdown headers
    content = re.sub(r'^#{1,6}\s+.*$', '', content, flags=re.MULTILINE)

    # Remove B-roll notes
    content = re.sub(r'\[B-ROLL:.*?\]', '', content)

    # Remove source citations
    content = re.sub(r'\[SOURCE:.*?\]', '', content)

    # Remove bold/italic markdown
    content = re.sub(r'\*\*(.*?)\*\*', r'\1', content)
    content = re.sub(r'\*(.*?)\*', r'\1', content)

    # Remove horizontal rules
    content = re.sub(r'^---+$', '', content, flags=re.MULTILINE)

    # Clean up multiple newlines
    content = re.sub(r'\n{3,}', '\n\n', content)

    # Strip leading/trailing whitespace
    content = content.strip()

    return content
```

## Reports

After export, reports:
- Word count
- Estimated runtime (words / 150)
- Output file location
