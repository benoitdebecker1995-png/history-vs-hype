"""BFS query against the research graph. Token-saving alternative to grep/load.

Usage:
    python graphify-out/research/query.py "uti possidetis"
    python graphify-out/research/query.py "flat earth" --depth 2
    python graphify-out/research/query.py "Hochschild" --max-nodes 25
    python graphify-out/research/query.py --list-entities
    python graphify-out/research/query.py --bridge uti_possidetis
"""
import json
import sys
from collections import deque
from pathlib import Path

HERE = Path(__file__).parent
GRAPH = json.loads((HERE / 'graph.json').read_text(encoding='utf-8'))
EXTRACT = json.loads((HERE / '.graphify_extract.json').read_text(encoding='utf-8'))

# Build node + edge lookups (the to_json format uses links[] for edges)
NODES = {n['id']: n for n in GRAPH['nodes']}
LINKS = GRAPH.get('links') or GRAPH.get('edges') or []
ADJ = {nid: [] for nid in NODES}
for e in LINKS:
    s, t = e['source'], e['target']
    if s in ADJ and t in ADJ:
        ADJ[s].append((t, e))
        ADJ[t].append((s, e))  # undirected for query

# Reattach extraction-only attrs (entity_type, role, videos, cites) which to_json strips
EXTRACT_NODES = {n['id']: n for n in EXTRACT['nodes']}

def enrich(nid):
    base = dict(NODES.get(nid, {}))
    ex = EXTRACT_NODES.get(nid, {})
    for k in ('entity_type', 'role', 'videos', 'cites'):
        if k in ex:
            base[k] = ex[k]
    return base


def match_nodes(query):
    q = query.lower()
    hits = []
    for nid, n in NODES.items():
        label = (n.get('label') or '').lower()
        if q in label or q in nid.lower():
            hits.append(nid)
    # rank by label-prefix match first, then degree
    hits.sort(key=lambda nid: (
        0 if (NODES[nid].get('label','').lower().startswith(q)) else 1,
        -len(ADJ[nid]),
    ))
    return hits


def bfs(seed_ids, max_depth=2, max_nodes=30):
    visited = {nid: 0 for nid in seed_ids}
    queue = deque((nid, 0) for nid in seed_ids)
    while queue and len(visited) < max_nodes:
        nid, depth = queue.popleft()
        if depth >= max_depth:
            continue
        for neighbor, _edge in ADJ.get(nid, []):
            if neighbor not in visited and len(visited) < max_nodes:
                visited[neighbor] = depth + 1
                queue.append((neighbor, depth + 1))
    return visited


def render(visited, query):
    out = [f'# Query: "{query}"  ({len(visited)} nodes)\n']
    # Show seeds (depth=0) first
    for depth in sorted(set(visited.values())):
        out.append(f'## Depth {depth}')
        for nid, d in visited.items():
            if d != depth:
                continue
            n = enrich(nid)
            vids = ', '.join(n.get('videos') or [])
            line = f"- **{n.get('label', nid)}** [{n.get('entity_type','?')}] — {n.get('role','')}"
            if vids:
                line += f"\n  Videos: {vids}"
            if n.get('cites'):
                for c in n['cites'][:3]:
                    line += f"\n  > {c}"
            out.append(line)
        out.append('')
    # Show edges between visited nodes
    edges_shown = set()
    edge_lines = []
    for e in LINKS:
        s, t = e['source'], e['target']
        if s in visited and t in visited:
            key = (min(s, t), max(s, t), e.get('relation', ''))
            if key in edges_shown:
                continue
            edges_shown.add(key)
            ev = e.get('evidence', '')
            edge_lines.append(f"- {NODES[s].get('label', s)} --[{e.get('relation','?')}]--> {NODES[t].get('label', t)}"
                              + (f"\n  {ev}" if ev else ""))
    if edge_lines:
        out.append('## Edges within subgraph')
        out.extend(edge_lines)
    return '\n'.join(out)


def list_entities():
    rows = []
    for nid, n in NODES.items():
        ex = EXTRACT_NODES.get(nid, {})
        rows.append((ex.get('entity_type', '?'), n.get('label', nid), len(ADJ[nid]), ', '.join(ex.get('videos', []) or [])))
    rows.sort(key=lambda r: (r[0], -r[2]))
    for t, label, deg, vids in rows:
        print(f"  [{t:>16}] {label} ({deg} edges)  videos: {vids}")


def show_bridge(bridge_id):
    for h in EXTRACT.get('hyperedges', []):
        if h['id'] == bridge_id:
            print(f"# Bridge: {h['label']}\n")
            print(h.get('description', ''))
            print(f"\nVideos: {', '.join(h.get('videos', []))}\n")
            print('Key entities:')
            for nid in h.get('nodes', []):
                n = enrich(nid)
                print(f"  - {n.get('label')} — {n.get('role','')}")
            return
    print(f'No bridge with id {bridge_id}. Available:')
    for h in EXTRACT.get('hyperedges', []):
        print(f"  {h['id']} — {h['label']}")


def main():
    args = sys.argv[1:]
    if not args or args[0] in ('-h', '--help'):
        print(__doc__)
        return
    if args[0] == '--list-entities':
        list_entities()
        return
    if args[0] == '--bridge':
        show_bridge(args[1] if len(args) > 1 else '')
        return
    # Parse --depth / --max-nodes flags
    depth = 2
    max_nodes = 30
    query_parts = []
    i = 0
    while i < len(args):
        if args[i] == '--depth':
            depth = int(args[i+1]); i += 2
        elif args[i] == '--max-nodes':
            max_nodes = int(args[i+1]); i += 2
        else:
            query_parts.append(args[i]); i += 1
    query = ' '.join(query_parts)
    seeds = match_nodes(query)
    if not seeds:
        print(f'No nodes matched "{query}". Try --list-entities to browse.')
        return
    seeds = seeds[:3]  # take top 3 matches
    visited = bfs(seeds, max_depth=depth, max_nodes=max_nodes)
    print(render(visited, query))


if __name__ == '__main__':
    main()
