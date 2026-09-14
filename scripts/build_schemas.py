"""Regenerate checked-in Draft 2020-12 schemas; no runtime dependencies."""
from pathlib import Path
from ec import TYPES, VERSION, write

S = {'type': 'string', 'minLength': 1}
NULL_S = {'type': ['string', 'null'], 'minLength': 1}
ID = {'type': 'string', 'pattern': '^[a-z0-9]+(?:-[a-z0-9]+)*$', 'maxLength': 64}
HASH = {'type': 'string', 'pattern': '^[a-f0-9]{64}$'}
SID = {'type': 'string', 'pattern': '^src-[a-f0-9]{24}$'}
CID = {'type': 'string', 'pattern': '^corpus-[a-f0-9]{64}$'}
EMPTY = {'type': 'string'}
V = {'const': VERSION, 'type': 'string'}


def obj(**props):
    return {'type': 'object', 'properties': props, 'required': list(props), 'additionalProperties': False}


def arr(item, minimum=0, maximum=None):
    result = {'type': 'array', 'items': item, 'minItems': minimum, 'uniqueItems': True}
    if maximum is not None: result['maxItems'] = maximum
    return result


evidence = obj(source_id=SID, segment_id={'type': 'string', 'pattern': '^seg-[0-9]{6}$'}, quote=S)
unit = obj(schema_version=V, unit_id=ID, type={'enum': TYPES}, status={'enum': ['explicit', 'inferred', 'synthesized']},
           title=S, statement=S, scope=S, derivation=EMPTY, evidence=arr(evidence, 1),
           attribution=arr(obj(source_id=SID, name=S)),
           relations=arr(obj(kind={'enum': ['supports', 'contradicts', 'requires', 'duplicates', 'refines']}, target=ID)))
capability = obj(schema_version=V, capability_id=ID, title=S, description={**S, 'maxLength': 1024},
                 rationale=S, inputs=S, output_contract=S, unit_ids=arr(ID, 1),
                 steps=arr(obj(instruction=S, unit_ids=arr(ID, 1)), 1), boundaries=arr(S, 1),
                 conflict_policy=EMPTY, checks=arr(S, 1),
                 examples=arr(obj(input=S, output=S, unit_ids=arr(ID, 1), status={'const': 'synthetic'}), 1))
schemas = {
    'source': obj(schema_version=V, source_id=SID, filename=S, title=NULL_S, creator=NULL_S,
                  url={'type': ['string', 'null'], 'pattern': '^https?://[^\\s/?#]+(?:[/?#][^\\s]*)?$'},
                  caption_type={'enum': ['unknown', 'manual', 'automatic', 'synthetic']}, content_hash=HASH,
                  raw_path=S, segments=arr(obj(segment_id={'type': 'string', 'pattern': '^seg-[0-9]{6}$'},
                      start={'type': ['number', 'null'], 'minimum': 0}, end={'type': ['number', 'null'], 'minimum': 0},
                      speaker=NULL_S, text=S, raw_text=S), 1)),
    'corpus': obj(schema_version=V, corpus_id=CID, sources=arr(obj(source_id=SID, path=S, document_hash=HASH), 1)),
    'knowledge-unit': unit,
    'extraction': obj(schema_version=V, corpus_id=CID, source_id=SID, note=EMPTY, units=arr(unit)),
    'ir': obj(schema_version=V, corpus_id=CID, units=arr(unit, 1),
              coverage=arr(obj(source_id=SID, unit_ids=arr(ID), note=EMPTY), 1)),
    'capability': capability,
    'capabilities': obj(schema_version=V, ir_hash=HASH, capabilities=arr(capability, 1, 3)),
    'discovery-assessment': obj(schema_version=V, ir_hash=HASH, no_capability_reason=EMPTY,
                                weakly_supported=arr(obj(topic=S, reason=S, unit_ids=arr(ID)), maximum=3)),
    'manifest': obj(schema_version=V, capability_id=ID, corpus_id=CID, ir_hash=HASH, files={'type': 'object'}),
}
schemas['session'] = obj(schema_version=V, active_run=S,
                         last_built=obj(run=S, capability_id=ID),
                         pending_request=obj(run=S, intent={'enum':['compile','discover','build','use','compare']},
                                             select={'type':['string','null']}, build_all={'type':'boolean'}))
schemas['session']['required'] = ['schema_version', 'active_run']

if __name__ == '__main__':
    for name, schema in schemas.items():
        write(Path(__file__).resolve().parent.parent / 'schemas' / f'{name}.schema.json',
              {'$schema': 'https://json-schema.org/draft/2020-12/schema', 'title': name, **schema})
    print(f'Wrote {len(schemas)} schemas')
