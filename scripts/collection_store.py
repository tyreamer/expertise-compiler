"""Private local collections layered on immutable source snapshots and IR history."""
from pathlib import Path
import shutil
import tempfile
import uuid
from ec import VERSION, digest, ingest, read, require, safe_child, validate_schema, validate_sources, write
from ingestors import adapter_for


class Library:
    def __init__(self, project):
        self.project = Path(project).resolve()
        self.root = self.project / '.expertise-compiler'
        self.path = self.root / 'library.json'
        self.index = read(self.path) if self.path.exists() else {'schema_version':VERSION,'collections':[], 'active_collection':None}
        require(type(self.index) is dict and self.index.get('schema_version') == VERSION and type(self.index.get('collections')) is list, 'Malformed collection library')
        seen_ids, seen_names = set(), set()
        for entry in self.index['collections']:
            require(type(entry) is dict and set(entry) == {'collection_id','name','path'} and
                    all(type(v) is str and v.strip() for v in entry.values()), 'Malformed collection entry')
            require(entry['collection_id'] not in seen_ids and entry['name'].casefold() not in seen_names, 'Duplicate collection identity')
            safe_child(self.root,entry['path'])
            seen_ids.add(entry['collection_id']); seen_names.add(entry['name'].casefold())
        require(self.index.get('active_collection') is None or self.index['active_collection'] in seen_ids, 'Unknown active collection')

    def resolve(self, selector=None):
        selector = selector or self.index.get('active_collection')
        if not selector: return None
        hits = [c for c in self.index['collections'] if selector.casefold() in {c['name'].casefold(),c['collection_id'].casefold()}]
        require(len(hits) == 1, 'Collection name is missing or ambiguous')
        folder = safe_child(self.root, hits[0]['path'])
        data = read(folder / 'collection.json'); validate_schema(data, 'collection')
        require(data['collection_id'] == hits[0]['collection_id'], 'Collection identity mismatch')
        revisions = [r['revision_id'] for r in data['revisions']]
        require(len(revisions) == len(set(revisions)) and data['active_revision'] in revisions, 'Malformed source revisions')
        return folder, data

    def save(self, folder, data):
        validate_schema(data, 'collection')
        write(folder / 'collection.json', data)
        entry = {'collection_id':data['collection_id'],'name':data['name'],'path':folder.relative_to(self.root).as_posix()}
        self.index['collections'] = [c for c in self.index['collections'] if c['collection_id'] != data['collection_id']] + [entry]
        self.index['active_collection'] = data['collection_id']
        write(self.path, self.index)

    def archive(self, input=None, *, name=None, collection=None, metadata=None, adopt=None, add=False):
        existing = self.resolve(collection) if collection else None
        if existing:
            folder, data = existing
            require(add or adopt is not None, 'Adding material to an existing collection needs the add action')
        else:
            name = name or (Path(input or adopt).name.replace('-', ' ').replace('_', ' ').title() + ' Sources')
            require(not any(c['name'].casefold() == name.casefold() for c in self.index['collections']), 'That collection name already exists; use add or select it')
            cid = 'collection-' + uuid.uuid4().hex[:16]
            folder = self.root / 'collections' / cid
            data = {'schema_version':VERSION,'collection_id':cid,'name':name,'active_revision':'pending','revisions':[],'briefs':[],'builds':[]}
        folder.mkdir(parents=True, exist_ok=True)
        previous = self.run(folder, data) if data['revisions'] else None
        with tempfile.TemporaryDirectory(prefix='.archive-', dir=folder) as temporary:
            temp = Path(temporary)
            if adopt:
                original = Path(adopt).resolve()
                validate_sources(original)
                require(not any(p.is_symlink() for p in original.rglob('*')), 'Cannot adopt symlinked run content')
                candidate = temp / 'run'
                shutil.copytree(original, candidate)
            else:
                records = {}
                if previous:
                    _, docs, _ = validate_sources(previous)
                    for doc in docs.values():
                        records[doc['filename']] = ((previous / doc['raw_path']).read_bytes(),
                                                   {k:doc[k] for k in ('title','creator','url','caption_type')})
                for record in adapter_for(input).collect(metadata):
                    filename = record.filename
                    if filename in records:
                        if records[filename][0] == record.raw: continue
                        filename = '_imports/' + digest(record.raw)[:16] + '/' + filename
                    records[filename] = (record.raw, record.metadata)
                inputs = temp / 'inputs'; inputs.mkdir()
                meta = {}
                for filename, (raw, m) in records.items():
                    target = safe_child(inputs, filename); target.parent.mkdir(parents=True, exist_ok=True); target.write_bytes(raw)
                    meta[filename] = m
                write(temp / 'metadata.json', meta)
                candidate = temp / 'run'
                ingest(inputs, candidate, temp / 'metadata.json')
            corpus, docs, _ = validate_sources(candidate)
            revision_id = 'source-' + corpus['corpus_id'].split('-')[1][:24]
            destination = folder / 'sources' / revision_id
            if destination.exists():
                require(validate_sources(destination)[0] == corpus, 'Source revision identity collision')
            else:
                destination.parent.mkdir(parents=True, exist_ok=True)
                if previous and not adopt:
                    for path in (previous / 'units').glob('*.json'):
                        part = read(path)
                        if part.get('source_id') in docs:
                            part['corpus_id'] = corpus['corpus_id']
                            write(candidate / 'units' / path.name, part)
                candidate.rename(destination)
            if revision_id not in {r['revision_id'] for r in data['revisions']}:
                data['revisions'].append({'revision_id':revision_id,'corpus_id':corpus['corpus_id'],'run':destination.relative_to(folder).as_posix()})
            data['active_revision'] = revision_id
            self.save(folder, data)
        return folder, data

    @staticmethod
    def run(folder, data):
        revision = next(r for r in data['revisions'] if r['revision_id'] == data['active_revision'])
        return safe_child(folder, revision['run'])
