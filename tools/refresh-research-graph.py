"""One-shot refresh of the research graph from archived research files.

Pipeline (zero Anthropic tokens, one Gemini Flash call):
1. Bundle all _ARCHIVED/published/*/01-VERIFIED-RESEARCH.md
2. Call gemini-2.5-flash with the saved extraction prompt
3. Strip code fences, validate JSON, patch dangling edges
4. Save .claude/REFERENCE/RESEARCH-GRAPH.json
5. Run graphify-out/research/build.py to regenerate graph.json + graph.html + report
6. Clear graphify-out/research/.needs_refresh marker

Usage:
    python tools/refresh-research-graph.py
    python tools/refresh-research-graph.py --skip-gemini   # rebuild from existing RESEARCH-GRAPH.json
"""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RESEARCH_DIR = ROOT / 'graphify-out' / 'research'
REFERENCE = ROOT / '.claude' / 'REFERENCE'
SKIP_GEMINI = '--skip-gemini' in sys.argv

PROMPT_PATH = RESEARCH_DIR / 'extract-prompt.txt'
GRAPH_JSON_PATH = REFERENCE / 'RESEARCH-GRAPH.json'
MARKER = RESEARCH_DIR / '.needs_refresh'


def step(msg):
    print(f'\n=== {msg} ===')


def run_gemini():
    step('Bundling archived research files')
    # Recursive glob — catches direct-child case AND `<slug>/_research/01-VERIFIED-RESEARCH.md`
    # (e.g. 45-manhattan-purchase-myth-2026 stores it in _research/).
    files = sorted((ROOT / 'video-projects' / '_ARCHIVED' / 'published').glob('**/01-VERIFIED-RESEARCH.md'))
    if not files:
        print('No archived research files found — nothing to do.')
        sys.exit(0)
    print(f'  {len(files)} files')

    bundle = tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete=False, suffix='.md')
    try:
        bundle.write(PROMPT_PATH.read_text(encoding='utf-8'))
        for f in files:
            # f.parent.name is the slug for direct-child case, but for the
            # `<slug>/_research/01-VERIFIED-RESEARCH.md` pattern we need to
            # walk up one more level.
            slug = f.parent.parent.name if f.parent.name == '_research' else f.parent.name
            bundle.write(f'\n\n=== VIDEO: {slug} ===\n\n')
            bundle.write(f.read_text(encoding='utf-8'))
        bundle.close()
        size_kb = Path(bundle.name).stat().st_size / 1024
        print(f'  bundle: {size_kb:.0f} KB')

        step('Calling Gemini 2.5 Flash')
        # Resolve gemini binary path explicitly — Windows subprocess can't find
        # the npm wrapper without the .cmd extension or a full path.
        gemini_bin = shutil.which('gemini')
        if not gemini_bin:
            print('  ERROR: `gemini` not found on PATH. Install via npm: npm i -g @google/gemini-cli')
            sys.exit(1)
        raw_out = tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete=False, suffix='.json')
        raw_out.close()
        with open(bundle.name, 'rb') as stdin:
            result = subprocess.run(
                [gemini_bin, '-m', 'gemini-2.5-flash', '--yolo', '-p',
                 'Follow the instructions at the top of this input. Output ONLY a single JSON object. No markdown fences, no commentary.'],
                stdin=stdin,
                stdout=open(raw_out.name, 'wb'),
                stderr=subprocess.PIPE,
                check=False,
            )
        if result.returncode != 0:
            print(f'  gemini failed: {result.stderr.decode(errors="replace")[:500]}')
            sys.exit(1)
        return Path(raw_out.name)
    finally:
        try:
            Path(bundle.name).unlink()
        except OSError:
            pass


def parse_and_clean(raw_path):
    step('Cleaning Gemini output')
    text = raw_path.read_text(encoding='utf-8')
    # Strip ```json ... ``` fences if present
    lines = text.splitlines()
    if lines and lines[0].strip().startswith('```'):
        lines = lines[1:]
    if lines and lines[-1].strip() == '```':
        lines = lines[:-1]
    # Strip any duplicated second JSON object (Flash sometimes repeats)
    cleaned = '\n'.join(lines)
    # Find the end of the first valid JSON object via balanced braces
    depth = 0
    end = -1
    in_str = False
    esc = False
    for i, ch in enumerate(cleaned):
        if esc:
            esc = False
            continue
        if ch == '\\' and in_str:
            esc = True
            continue
        if ch == '"':
            in_str = not in_str
            continue
        if in_str:
            continue
        if ch == '{':
            depth += 1
        elif ch == '}':
            depth -= 1
            if depth == 0:
                end = i + 1
                break
    if end > 0:
        cleaned = cleaned[:end]
    d = json.loads(cleaned)
    print(f'  parsed: entities={len(d.get("entities", []))} scholars={len(d.get("scholars", []))} edges={len(d.get("edges", []))} citations={len(d.get("citations", []))} bridges={len(d.get("bridges", []))}')
    return d


def patch_and_save(d):
    step('Patching dangling edges + bridges')
    entity_ids = {e['id'] for e in d.get('entities', [])}
    scholar_ids = {s['id'] for s in d.get('scholars', [])}
    all_ids = entity_ids | scholar_ids

    missing = set()
    for e in d.get('edges', []):
        for k in ('source_id', 'target_id'):
            if e[k] not in all_ids:
                missing.add(e[k])

    stubs = []
    for mid in sorted(missing):
        label = mid.replace('_', ' ').title()
        stubs.append({
            'id': mid,
            'label': label,
            'type': 'concept',
            'role': '[stub: referenced by edges but not declared by Gemini]',
            'videos': []
        })
    d['entities'].extend(stubs)
    print(f'  added {len(stubs)} stub entities')

    before = len(d.get('bridges', []))
    d['bridges'] = [b for b in d.get('bridges', []) if len(b.get('videos', [])) >= 2]
    print(f'  dropped {before - len(d["bridges"])} single-video bridges')

    from datetime import date
    d['_meta'] = {
        'generated_by': 'Gemini 2.5 Flash via tools/refresh-research-graph.py',
        'generated_at': date.today().isoformat(),
        'corpus': f'{len(d.get("videos", []))} _ARCHIVED/published/01-VERIFIED-RESEARCH.md files',
        'caveats': 'T3 synthesis. Verify quote attributions before script use. Stub entities flagged in role field.',
        'actual_counts': {
            'entities': len(d.get('entities', [])),
            'scholars': len(d.get('scholars', [])),
            'edges': len(d.get('edges', [])),
            'citations': len(d.get('citations', [])),
            'bridges': len(d.get('bridges', [])),
            'videos': len(d.get('videos', [])),
        }
    }
    GRAPH_JSON_PATH.write_text(json.dumps(d, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f'  saved {GRAPH_JSON_PATH}')


def rebuild_graph():
    step('Rebuilding graphify research graph')
    pyfile = ROOT / 'graphify-out' / '.graphify_python'
    py = pyfile.read_text(encoding='utf-8').strip()
    build = RESEARCH_DIR / 'build.py'
    result = subprocess.run([py, str(build)], capture_output=True, text=True, encoding='utf-8')
    print(result.stdout)
    if result.returncode != 0:
        print(f'  build failed: {result.stderr[:500]}')
        sys.exit(1)


def clear_marker():
    if MARKER.exists():
        MARKER.unlink()
        print(f'  cleared {MARKER}')


def main():
    if not SKIP_GEMINI:
        raw = run_gemini()
        try:
            d = parse_and_clean(raw)
        except json.JSONDecodeError as e:
            print(f'JSON parse failed: {e}')
            print(f'  raw output kept at {raw} for inspection')
            sys.exit(1)
        raw.unlink()
        patch_and_save(d)
    else:
        print('Skipping Gemini call, using existing RESEARCH-GRAPH.json')

    rebuild_graph()
    clear_marker()
    print('\nDone. Open graphify-out/research/graph.html in browser, or use query.py.')


if __name__ == '__main__':
    main()
