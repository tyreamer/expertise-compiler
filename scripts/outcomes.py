"""Domain-independent outcome contracts; the host assistant infers intent."""
from ec import require, validate_schema, fingerprint

INTENTS = ('create','review','improve','decide','plan','do','learn','reference')
REQUIRED = {
    'create': {'deliverable'}, 'review': {'assessment'}, 'improve': {'revision'},
    'decide': {'options','recommendation'}, 'plan': {'steps'}, 'do': {'steps'},
    'learn': {'lesson','exercise'}, 'reference': {'answer'},
}
GUIDANCE = {
    'create': 'Produce the requested original deliverable; label original content separately from source claims.',
    'review': 'Assess the actual work against relevant source criteria, with prioritized actionable feedback.',
    'improve': 'Provide an improved version and explain material changes; preserve the original.',
    'decide': 'Compare the real options against relevant criteria, state tradeoffs and a conditional recommendation or a reason to defer.',
    'plan': 'Give ordered actionable steps, dependencies, checkpoints and observable completion criteria.',
    'do': 'Guide the next actionable step, required inputs, checks and stopping conditions. Do not claim an action was executed without evidence.',
    'learn': 'Teach at the learner\'s level, supply an exercise and assessment criteria, and wait for their response before claiming mastery.',
    'reference': 'Answer the actual question with source-linked statements, disagreements and limits; do not force an unrelated procedure.',
}


def validate_outcome(result, brief_id, ir, method, target):
    validate_schema(result,'outcome')
    require(result['brief_id']==brief_id and result['ir_hash']==fingerprint(ir)
            and result['method_hash']==fingerprint(method), 'Outcome is stale for its brief, knowledge or method')
    require(result['target']==target, 'Outcome target mismatch')
    chosen=set(method['capability']['unit_ids'])
    kinds={s['kind'] for s in result['sections']}
    require(REQUIRED[target] <= kinds or result['unsupported'], 'Missing useful outcome sections for '+target)
    for section in result['sections']:
        require(set(section['unit_ids']) <= chosen, 'Outcome cites units outside its method')
        if section['status'] in {'explicit','inferred','synthesized'}:
            require(section['unit_ids'], 'Source-derived outcome section needs evidence')


def render_outcome(brief,result):
    lines=['# '+brief['desired_result'],'',result['summary'],'']
    for section in result['sections']:
        lines += ['## '+section['title'],'',section['content'],'',
                  'Basis: '+section['status']+'.']
        if section['unit_ids']:
            lines += ['Evidence: '+', '.join(f'[{uid}](references/knowledge.json)' for uid in section['unit_ids'])]
        lines.append('')
    for key,title in [('disagreements','Source disagreements'),('limitations','Limits'),('unsupported','Not established'),('additional_general_advice','Additional general advice — not source evidence')]:
        if result[key]: lines += ['## '+title,'']+['- '+v for v in result[key]]+['']
    lines += ['[Saved method](method.md) · [Validation scope](validation.json)','']
    return '\n'.join(lines)


def render_method(cap):
    lines=['# '+cap['title'],'',cap['description'],'','Inputs: '+cap['inputs'],'','Result: '+cap['output_contract'],'']
    for step in cap['steps']:
        lines += ['- '+step['instruction'],'  Evidence: '+', '.join(f'[{uid}](references/knowledge.json)' for uid in step['unit_ids'])]
    lines += ['','## Limits','']+['- '+v for v in cap['boundaries']]
    if cap['conflict_policy']: lines += ['',cap['conflict_policy']]
    lines += ['','[Source excerpts](sources/excerpts.json)','']
    return '\n'.join(lines)
