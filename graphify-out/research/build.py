"""Transform RESEARCH-GRAPH.json -> graphify schema -> build/cluster/render."""
import json
from pathlib import Path

# ---- Load source ----
SRC = Path(r'D:\History vs Hype\.claude\REFERENCE\RESEARCH-GRAPH.json')
OUT_DIR = Path(r'D:\History vs Hype\graphify-out\research')
OUT_DIR.mkdir(parents=True, exist_ok=True)

src = json.loads(SRC.read_text(encoding='utf-8'))

# ---- Build graphify-schema extraction ----
# Each entity/scholar -> node. Citations -> node attributes (joined onto entity_refs).
# Edges -> graphify edges. Bridges -> hyperedges. videos[] -> source_file (use first).

# Build citation lookup by entity ref so we can attach quote evidence
cit_by_entity = {}
for c in src.get('citations', []):
    for eid in c.get('entity_refs', []) or []:
        cit_by_entity.setdefault(eid, []).append(c)

nodes = []
nodes_by_id = {}

def make_node(item, node_type, source_file_videos):
    nid = item['id']
    if nid in nodes_by_id:
        return
    label = item.get('label') or item.get('name') or nid
    source_file = (source_file_videos or ['unknown'])[0] + '.md'
    node = {
        'id': nid,
        'label': label,
        'file_type': 'rationale',
        'source_file': source_file,
        'source_location': None,
        'source_url': None,
        'captured_at': None,
        'author': None,
        'contributor': None,
        # Custom attributes preserved through graphify build:
        'entity_type': node_type,
        'role': item.get('role') or item.get('main_work') or '',
        'videos': item.get('videos', []),
        'cites': [c['quote'][:120] + ('...' if len(c.get('quote',''))>120 else '') for c in cit_by_entity.get(nid, [])],
    }
    nodes.append(node)
    nodes_by_id[nid] = node

for e in src.get('entities', []):
    make_node(e, e.get('type', 'concept'), e.get('videos'))
for s in src.get('scholars', []):
    make_node(s, 'scholar', s.get('videos'))

# Edges (graphify relations whitelist: calls|implements|references|cites|conceptually_related_to|
# shares_data_with|semantically_similar_to|rationale_for). Map ours to nearest.
RELATION_MAP = {
    'appears_with': 'conceptually_related_to',
    'cites': 'cites',
    'invokes': 'references',
    'debunks': 'references',
    'grounds_claim_in': 'references',
    'bridges': 'conceptually_related_to',
}

edges = []
for e in src.get('edges', []):
    src_id = e['source_id']
    tgt_id = e['target_id']
    if src_id not in nodes_by_id or tgt_id not in nodes_by_id:
        continue  # safety; we already stubbed dangling, but double-check
    conf = e.get('confidence', 'EXTRACTED')
    score = 1.0 if conf == 'EXTRACTED' else 0.85
    edges.append({
        'source': src_id,
        'target': tgt_id,
        'relation': RELATION_MAP.get(e.get('relation', ''), 'conceptually_related_to'),
        'confidence': conf,
        'confidence_score': score,
        'source_file': (e.get('videos', ['unknown']) or ['unknown'])[0] + '.md',
        'source_location': None,
        'weight': 1.0,
        'evidence': e.get('evidence', ''),
    })

# Bridges -> hyperedges (3+ nodes participating in one named connection)
hyperedges = []
for b in src.get('bridges', []):
    valid_nodes = [n for n in b.get('key_entities', []) if n in nodes_by_id]
    if len(valid_nodes) >= 2:
        hyperedges.append({
            'id': b['id'],
            'label': b['label'],
            'nodes': valid_nodes,
            'relation': 'participate_in',
            'confidence': 'EXTRACTED',
            'confidence_score': 0.95,
            'source_file': 'bridge:' + b['id'],
            'description': b.get('description', ''),
            'videos': b.get('videos', []),
        })

extraction = {
    'nodes': nodes,
    'edges': edges,
    'hyperedges': hyperedges,
    'input_tokens': 0,
    'output_tokens': 0,
}

(OUT_DIR / '.graphify_extract.json').write_text(json.dumps(extraction, indent=2, ensure_ascii=False), encoding='utf-8')
print(f'Extraction: {len(nodes)} nodes, {len(edges)} edges, {len(hyperedges)} hyperedges')

# ---- Build graph, cluster, analyze ----
from graphify.build import build_from_json
from graphify.cluster import cluster, score_all
from graphify.analyze import god_nodes, surprising_connections, suggest_questions
from graphify.export import to_html, to_json
from graphify.report import generate

G = build_from_json(extraction)
print(f'Graph: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges')

communities = cluster(G)
cohesion = score_all(G, communities)
print(f'Communities: {len(communities)}')

gods = god_nodes(G)
surprises = surprising_connections(G, communities)

# ---- Label communities by looking at entity_type + topic of member nodes ----
# Compute a label for each community from the most-connected node's label, scoped to its members
labels = {}
for cid, member_ids in communities.items():
    if not member_ids:
        labels[cid] = f'Community {cid}'
        continue
    # Pick node with most edges in the community as the seed name
    seed = max(member_ids, key=lambda n: G.degree(n))
    seed_label = G.nodes[seed].get('label', seed)
    # Shorten label
    short = seed_label.split(' (')[0]
    labels[cid] = f'{short} cluster'

# ---- Detection metadata for report generator ----
detection = {
    'total_files': len(src.get('videos', [])),
    'total_words': 22500000,
    'needs_graph': True,
    'warning': None,
    'files': {
        'code': [],
        'document': [v['slug'] + '.md' for v in src.get('videos', [])],
        'paper': [],
        'image': [],
        'video': [],
    }
}
tokens = {'input': 0, 'output': 0}

questions = suggest_questions(G, communities, labels)

# ---- Generate outputs ----
report = generate(G, communities, cohesion, labels, gods, surprises, detection, tokens,
                  str(SRC), suggested_questions=questions)
(OUT_DIR / 'GRAPH_REPORT.md').write_text(report, encoding='utf-8')
print(f'Report: {OUT_DIR / "GRAPH_REPORT.md"}')

to_json(G, communities, str(OUT_DIR / 'graph.json'))
print(f'graph.json: {OUT_DIR / "graph.json"}')

if G.number_of_nodes() <= 5000:
    to_html(G, communities, str(OUT_DIR / 'graph.html'), community_labels=labels)
    print(f'graph.html: {OUT_DIR / "graph.html"}')

# Save labels + analysis for any later re-rendering
(OUT_DIR / '.labels.json').write_text(
    json.dumps({str(k): v for k, v in labels.items()}, ensure_ascii=False), encoding='utf-8')
(OUT_DIR / '.analysis.json').write_text(json.dumps({
    'communities': {str(k): v for k, v in communities.items()},
    'cohesion': {str(k): v for k, v in cohesion.items()},
    'gods': gods,
    'surprises': surprises,
    'questions': questions,
}, indent=2, ensure_ascii=False), encoding='utf-8')

print()
print('=== Top community labels ===')
for cid in sorted(communities, key=lambda c: -len(communities[c]))[:8]:
    print(f'  [{cid}] {labels[cid]} ({len(communities[cid])} nodes, cohesion {cohesion.get(cid, 0):.2f})')

print('\n=== God nodes (real, top 5) ===')
for n in gods[:5]:
    print(f'  {n}')

print('\n=== Surprising connections (top 5) ===')
for s in surprises[:5]:
    print(f'  {s}')
