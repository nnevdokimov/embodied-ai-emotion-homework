"""Independent stdlib regression checks and submission-file integrity."""
import csv
import argparse
import hashlib
import json
import math
from collections import defaultdict, deque
from pathlib import Path

BASE = Path(__file__).resolve().parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--write-manifest', action='store_true', help='Record current hashes after numerical checks pass.')
args = parser.parse_args()

def read(path):
    with path.open(newline='') as f:
        return list(csv.DictReader(f))

node_records = read(BASE / 'data/concepts.csv')
ids = {n['id'] for n in node_records}
assert len(node_records) == len(ids) == 25
assert sum(n['origin'] == 'HA0 Emotion inventory' for n in node_records) == 20
assert len((BASE / 'interpretation.md').read_text().split()) == 300

variants = {
    'baseline': BASE / 'edges.csv',
    'added': BASE / 'results/edges_added.csv',
    'removed': BASE / 'results/edges_removed.csv',
}
metrics = {}
edge_sets = {}

def same(actual, expected):
    if expected is None:
        assert actual == 'NA', actual
    else:
        assert math.isclose(float(actual), expected, abs_tol=1e-12), (actual, expected)

for stage, path in variants.items():
    rows = read(path)
    assert len(rows) == (30 if stage == 'added' else 27)
    edge_sets[stage] = {(r['source'], r['target'], r['type']) for r in rows}
    assert len(rows) == len(edge_sets[stage])
    parents, children = defaultdict(list), defaultdict(list)
    for row in rows:
        assert row['source'] in ids and row['target'] in ids
        assert row['provenance'] and row['evidence']
        assert row['annotation_origin'] == ('sourced' if row['type'] == 'is_a' else 'generated')
        if row['type'] == 'is_a':
            parents[row['target']].append(row['source'])
            children[row['source']].append(row['target'])

    def root_paths(node, stack=()):
        assert node not in stack, ('cycle', stack, node)
        if node == 'entity':
            return [('entity',)]
        return [p+(node,) for parent in parents[node] for p in root_paths(parent, stack+(node,))]

    paths = {n: root_paths(n) for n in ids}
    desc = {}
    for node in ids:
        seen = set()
        pending = deque(children[node])
        while pending:
            child = pending.popleft()
            if child in seen:
                continue
            seen.add(child)
            pending.extend(children[child])
        desc[node] = len(seen)
    reachable = {n for n in ids if paths[n]}
    D = max(min(len(p)-1 for p in paths[n]) for n in reachable)
    M = max(desc[n] for n in reachable)
    expected = {}
    for n in ids:
        ds = [len(p)-1 for p in paths[n]]
        expected[n] = {
            'depth_min': min(ds) if ds else None, 'depth_max': max(ds) if ds else None,
            'descendants': desc[n], 'root_path_count': len(ds), 'parent_count': len(parents[n]),
            'S_depth': min(ds)/D if ds else None,
            'S_depth_max': max(ds)/D if ds else None,
            'S_breadth': 1-math.log1p(desc[n])/math.log1p(M) if ds else None,
            'normalizer_depth': D, 'normalizer_descendants': M,
        }
    saved = {r['id']: r for r in read(BASE / f'results/specificity_{stage}.csv')}
    assert set(saved) == ids
    for node in ids:
        assert (saved[node]['reachable'] == 'True') == (node in reachable)
        assert set(filter(None, saved[node]['parents'].split('; '))) == set(parents[node])
        for column, value in expected[node].items():
            same(saved[node][column], value)
    metrics[stage] = expected
    print(stage, 'independent verification:', len(reachable), 'reachable; normalizers', D, M)

operations = read(BASE / 'data/perturbations.csv')
adds = {(r['source'], r['target'], r['type']) for r in operations if r['operation'] == 'add'}
removes = {(r['source'], r['target'], r['type']) for r in operations if r['operation'] == 'remove'}
assert len(adds) == len(removes) == 3
assert edge_sets['added'] - edge_sets['baseline'] == adds
assert edge_sets['added'] - edge_sets['removed'] == removes

comparison_rows = read(BASE / 'perturbation.csv')
assert len(comparison_rows) == 75
assert len({(r['comparison'], r['id']) for r in comparison_rows}) == 75
for row in comparison_rows:
    before_name, after_name = row['comparison'].split(' → ')
    node = row['id']
    a, b = metrics[before_name][node], metrics[after_name][node]
    both = a['S_depth'] is not None and b['S_depth'] is not None
    status = ('connected' if both else 'newly reachable' if b['S_depth'] is not None else 'disconnected' if a['S_depth'] is not None else 'still disconnected')
    assert row['status'] == status
    for metric in ['S_depth', 'S_breadth']:
        same(row[metric+'_before'], a[metric])
        same(row[metric+'_after'], b[metric])
        same(row['delta_'+metric], b[metric]-a[metric] if both else None)
    changed = both and (abs(b['S_depth']-a['S_depth']) > .1+1e-12 or abs(b['S_breadth']-a['S_breadth']) > .1+1e-12)
    assert (row['moved_over_0_1'] == 'True') == changed
    same(row['delta_depth_fixed_scale'], (b['depth_min']-a['depth_min'])/6 if both else None)
    same(row['delta_breadth_fixed_scale'], (math.log1p(a['descendants'])-math.log1p(b['descendants']))/math.log1p(23) if both else None)

assert metrics['baseline']['feeling']['descendants'] == 12
assert metrics['added']['panic']['depth_min'] == 5 and metrics['added']['panic']['depth_max'] == 6
assert sum(r['S_depth'] is None for r in metrics['removed'].values()) == 8
assert math.isclose(metrics['removed']['mood']['S_depth']-metrics['added']['mood']['S_depth'], 1/3)
assert metrics['removed']['mood']['depth_min'] == metrics['added']['mood']['depth_min']
nb = json.loads((BASE / 'HA2_network.ipynb').read_text())
intro = ''.join(nb['cells'][0]['source'])
for person in ['Nikolay Evdokimov', 'Aleksandr Mandrov', 'Ivan Tsarikov', 'Egor Antonov']:
    assert person in intro
code_cells = [c for c in nb['cells'] if c['cell_type'] == 'code']
assert all(c['execution_count'] is not None for c in code_cells)
assert not any(o['output_type'] == 'error' for c in code_cells for o in c['outputs'])
assert sum('image/png' in o.get('data', {}) for c in code_cells for o in c['outputs']) == 3
print('Verified: 25 nodes, three typed layers, 3 additions/3 removals, 75 comparisons, 300 words, 4 team members, 3 plots.')


# Regression cases: exact edits, fixed-root coverage, and association invariance.
assert adds == {('symptom', 'scar', 'is_a'), ('emotion', 'panic', 'is_a'), ('anxiety', 'freeze', 'associated_with')}
assert removes == {('fear', 'panic', 'is_a'), ('feeling', 'emotion', 'is_a'), ('emotion', 'panic', 'is_a')}
assert {n for n, m in metrics['removed'].items() if m['S_depth'] is None} == {'emotion', 'fear', 'anger', 'joy', 'panic', 'rage', 'anxiety', 'resentment'}
association_only = edge_sets['baseline'] | {e for e in adds if e[2] != 'is_a'}
assert {e for e in association_only if e[2] == 'is_a'} == {e for e in edge_sets['baseline'] if e[2] == 'is_a'}
with (BASE / 'data/HA0_Emotion.csv').open(encoding='utf-8-sig', newline='') as stream:
    ha0 = {r['term']: r for r in csv.DictReader(stream, delimiter=';')}
exported = {r['id']: r for r in read(BASE / 'nodes.csv')}
for row in node_records:
    assert row['id'] in exported
    if row['id'] in ha0:
        for field in ['uncertain', 'uncertainty_note']:
            assert row[field] == ha0[row['id']][field] == exported[row['id']][field]
for row in read(BASE / 'results/coverage_summary.csv'):
    expected_n = 24 if row['scope'] == 'all reachable nodes' else 19
    assert int(row['reachable_nodes']) == expected_n
    assert int(row['leaves']) == 15
    same(row['leaf_fraction'], 15/expected_n)

# Notebook hashes cover source cells, excluding execution timing and output metadata.
def file_records():
    records = {}
    for path in sorted(BASE.rglob('*')):
        rel = path.relative_to(BASE)
        if not path.is_file() or path.is_symlink() or any(p.startswith('.') or p == '__pycache__' for p in rel.parts):
            continue
        if rel.as_posix() == 'manifest.json':
            continue
        mode = 'bytes'
        data = path.read_bytes()
        if path.suffix == '.ipynb':
            cells = json.loads(data)['cells']
            source = [{'cell_type': c['cell_type'], 'source': ''.join(c['source'])} for c in cells]
            data = json.dumps(source, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')
            mode = 'notebook_source'
        records[rel.as_posix()] = {'mode': mode, 'sha256': hashlib.sha256(data).hexdigest()}
    return records

current = file_records()
manifest_path = BASE / 'manifest.json'
if args.write_manifest:
    manifest_path.write_text(json.dumps({'format': 1, 'files': current}, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
else:
    recorded = json.loads(manifest_path.read_text(encoding='utf-8'))
    assert recorded['format'] == 1
    assert set(recorded['files']) == set(current), 'The submission file list has changed.'
    for name, details in current.items():
        assert recorded['files'][name] == details, f'Changed file: {name}'
print(f'Integrity verified: {len(current)} files; notebook source, all data, outputs and both peer reviews.')
