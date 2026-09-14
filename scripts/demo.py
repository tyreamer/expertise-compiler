"""Offline demo using explicitly authored fixture knowledge, never simulated extraction."""
import argparse
from pathlib import Path
from ec import ROOT, VERSION, assemble, fingerprint, ingest, package, read, require, validate_capabilities, validate_package, validate_sources, write


def build(base):
    base = Path(base)
    run = base / 'run'
    ingest(ROOT / 'fixtures' / 'transcripts', run, ROOT / 'fixtures' / 'metadata.json')
    corpus, docs, _ = validate_sources(run)
    by_name = {d['filename']: d for d in docs.values()}
    parts = {sid: [] for sid in docs}
    for spec in read(ROOT / 'fixtures' / 'demo_knowledge.json'):
        doc = by_name[spec['filename']]
        ev = []
        attrs = []
        for ref in [spec] + spec.get('extra_evidence', []):
            source = by_name[ref['filename']]
            seg = source['segments'][ref['segment']-1]
            ev.append({'source_id': source['source_id'], 'segment_id': seg['segment_id'], 'quote': seg['text']})
            name = seg['speaker'] or source['creator']
            attr = {'source_id': source['source_id'], 'name': name}
            if name and attr not in attrs: attrs.append(attr)
        unit = {'schema_version': VERSION, 'unit_id': spec['unit_id'], 'type': spec['type'],
                'status': spec.get('status', 'explicit'), 'title': spec['unit_id'].replace('-', ' ').capitalize(),
                'statement': spec['statement'], 'scope': 'Synthetic teaching material; apply only within the conditions stated in its evidence.',
                'derivation': spec.get('derivation', ''), 'evidence': ev, 'attribution': attrs, 'relations': spec.get('relations', [])}
        parts[doc['source_id']].append(unit)
    for sid, units in parts.items():
        data = {'schema_version': VERSION, 'corpus_id': corpus['corpus_id'], 'source_id': sid,
                'note': 'Authored demo checkpoint. Markdown title is metadata, not actionable knowledge.', 'units': units}
        existing = run / 'units' / f'{sid}.json'
        require(not existing.exists() or read(existing) == data, 'Demo checkpoint edited; use a new output directory')
        write(existing, data)
    ir = assemble(run)
    caps = {'schema_version': VERSION, 'ir_hash': fingerprint(ir), 'capabilities': read(ROOT / 'fixtures' / 'demo_capabilities.json')}
    existing = run / 'capabilities.json'
    require(not existing.exists() or read(existing) == caps, 'Demo capabilities changed; choose a new output directory')
    write(existing, caps)
    validate_capabilities(run)
    for cap in caps['capabilities']:
        output = base / 'packages' / cap['capability_id']
        if output.exists():
            manifest = validate_package(output)
            require(manifest['ir_hash'] == fingerprint(ir), 'Demo package is stale; choose a new output directory')
        else:
            package(run, cap['capability_id'], output)
    return run


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output', default='workspace/demo-build')
    args = p.parse_args()
    run = build(args.output)
    print(f'Demo valid: {run}\n12 authored units; 3 capabilities. No model was called.\nNext: python scripts/evaluate.py prepare --demo ' + str(Path(args.output)))
