"""Goal -> evidence-linked method -> actual saved work, with private collection reuse."""
from pathlib import Path
import shutil
import tempfile
from ec import (ROOT, VERSION, Invalid, assemble, digest, fingerprint, inventory, read, require, safe_child,
                text_write, validate_capability_data, validate_ir, validate_package, validate_schema,
                validate_sources, validate_units, write)
from collection_store import Library
from scoped_export import export_method, selected_excerpts
from workflow import checkpoint_state

GOAL_QUESTION = 'What are you hoping this helps you do? You can describe a task, share something you’re working on, or ask me to explore the material.'


def compiler_hash():
    return fingerprint({p.relative_to(ROOT).as_posix():digest(p.read_bytes()) for area in ('scripts','schemas','prompts')
                        for p in sorted((ROOT / area).rglob('*')) if p.is_file() and p.suffix in {'.py','.json','.md'}})


def render_result(brief, result, method):
    method_dir = 'method/' + method['capability']['capability_id']
    lines = ['# ' + brief['desired_result'], '', result['assessment'], '']
    for finding in result['findings']:
        lines += ['## ' + finding['priority'].title() + ': ' + finding['title'], finding['assessment'], '',
                  '**Proposed change:** ' + finding['proposed_change'], '',
                  'Evidence: ' + ', '.join(f'[{uid}]({method_dir}/references/knowledge.json)' for uid in finding['unit_ids']), '']
    if result['proposed_revision']: lines += ['## Proposed revision', result['proposed_revision'], '']
    if result['checklist']:
        lines += ['## Practical checklist', '']
        for step in result['checklist']:
            lines += ['- [ ] ' + step['action'] + ' — Done when: ' + step['done_when'],
                      '  Evidence: ' + ', '.join(f'[{uid}]({method_dir}/references/knowledge.json)' for uid in step['unit_ids'])]
    for field, title in [('disagreements','Source disagreements'),('limitations','Limits'),('unsupported','Not established by these sources'),('additional_general_advice','Additional general advice — not attributed to the sources')]:
        if result[field]: lines += ['', '## ' + title, ''] + ['- ' + value for value in result[field]]
    lines += ['', f'[Reusable method]({method_dir}/SKILL.md) · [Validation scope](validation.json)', '']
    return '\n'.join(lines)


def validate_result(result, brief_id, ir, method, target):
    validate_schema(result, 'work-result')
    require(result['brief_id'] == brief_id and result['ir_hash'] == fingerprint(ir) and result['method_hash'] == fingerprint(method), 'Result is stale for its brief, knowledge or method')
    require(result['target'] == target, 'Result target mismatch')
    chosen = set(method['capability']['unit_ids'])
    for item in result['findings'] + result['checklist']:
        require(set(item['unit_ids']) <= chosen, 'Result cites units outside its method')
    require(result['findings'] or result['checklist'] or result['unsupported'], 'Result contains no actionable findings, plan or supported limitation')
    require(target != 'checklist' or result['checklist'] or result['unsupported'], 'Checklist target has no plan')


def validate_build(folder, collection=None):
    folder = Path(folder).resolve()
    manifest = read(folder / 'manifest.json'); validate_schema(manifest, 'goal-build')
    require(folder.name == manifest['build_id'], 'Build identity mismatch')
    require(manifest['files'] == inventory(folder), 'Build file inventory/hash mismatch')
    collection = Path(collection) if collection else folder.parent.parent
    data = read(collection / 'collection.json'); validate_schema(data, 'collection')
    require(data['collection_id'] == manifest['collection_id'], 'Build collection mismatch')
    revision = next((r for r in data['revisions'] if r['revision_id'] == manifest['source_revision']), None)
    require(revision is not None and revision['corpus_id'] == manifest['corpus_id'], 'Missing build source revision')
    run = safe_child(collection, revision['run'])
    ir = validate_ir(run, safe_child(collection, manifest['knowledge_path']))
    require(fingerprint(ir) == manifest['ir_hash'], 'Knowledge revision hash mismatch')
    brief = read(folder / 'brief.json'); validate_schema(brief, 'brief')
    method = read(folder / 'method.json'); validate_schema(method, 'goal-method')
    result = read(folder / 'result.json')
    require(fingerprint(brief) == manifest['brief_hash'] and manifest['brief_id'] == 'brief-' + fingerprint(brief)[:24], 'Brief identity mismatch')
    require(method['brief_id'] == manifest['brief_id'] and method['ir_hash'] == manifest['ir_hash'] and fingerprint(method) == manifest['method_hash'], 'Method identity mismatch')
    validate_capability_data(ir, {'schema_version':VERSION,'ir_hash':fingerprint(ir),'capabilities':[method['capability']]})
    validate_result(result, manifest['brief_id'], ir, method, manifest['target'])
    require(fingerprint(result) == manifest['result_hash'], 'Result hash mismatch')
    require((folder / 'result.md').read_text(encoding='utf-8') == render_result(brief,result,method), 'Rendered result differs from reviewed content')
    exported = folder / 'method'
    # Skill format requires its directory name to match its capability ID.
    require({p.name for p in exported.iterdir()} == {method['capability']['capability_id']}, 'Unexpected method directory')
    exported = exported / method['capability']['capability_id']
    export_manifest = validate_package(exported)
    require(export_manifest['ir_hash'] == manifest['ir_hash'] and export_manifest['corpus_id'] == manifest['corpus_id'], 'Export revision mismatch')
    require(read(exported / 'capability.json') == method['capability'], 'Saved reusable method mismatch')
    selected = [u for u in ir['units'] if u['unit_id'] in method['capability']['unit_ids']]
    require(read(exported / 'references/knowledge.json') == selected, 'Export evidence differs from private audit knowledge')
    _, docs, segments = validate_sources(run)
    require(read(exported / 'sources/excerpts.json') == selected_excerpts(selected,docs,segments), 'Export source metadata differs from private originals')
    report = read(folder / 'validation.json')
    require(report['structural_integrity'] == 'passed' and report['source_evidence_linkage'] == 'passed', 'Missing integrity/evidence status')
    require(report['semantic_review']['status'] == 'assistant-reviewed' and report['semantic_review']['result_hash'] == manifest['result_hash'], 'Missing bound semantic review acknowledgement')
    require(report['effectiveness_testing'] == 'not-run', 'Build cannot claim effectiveness from integrity checks')
    return {'valid':True,'structural_integrity':'passed','source_evidence_linkage':'passed',
            'semantic_review':'assistant-reviewed; not independently verified','effectiveness_testing':'not-run'}


def work(*, project='.', input=None, metadata=None, collection=None, name=None, action='work', brief=None,
         target=None, adopt=None, reconciled=False, reviewed=False):
    project = Path(project).resolve(); library = Library(project)
    path = lambda value: (project / value).resolve() if value else None
    if action == 'list': return {'phase':'collections','collections':library.index['collections']}
    if input or adopt:
        folder, data = library.archive(str(path(input)) if input else None, name=name, collection=collection,
                                       metadata=path(metadata), adopt=path(adopt), add=action == 'add')
    else:
        resolved = library.resolve(collection)
        if not resolved: return {'phase':'needs_sources','message':'Give me source files or select a saved collection.'}
        folder, data = resolved
    library.save(folder,data)
    run = library.run(folder,data); corpus, docs, segments = validate_sources(run)
    state_path = folder / 'conversation.json'
    state = read(state_path) if state_path.exists() else {}
    def respond(phase, **kwargs):
        return {'phase':phase,'collection':data['name'],'collection_id':data['collection_id'],
                'collection_location':str(folder),'source_revision':data['active_revision'],'run':str(run),**kwargs}
    if action in {'save','add'} and brief is None:
        return respond('archived', transcripts=len(docs), message='Sources saved locally; no method or skill was forced.',
                       revision_count=len(data['revisions']))
    if action == 'export':
        require(state.get('last_build'), 'There is no completed method to export yet')
        build = safe_child(folder,state['last_build']); validate_build(build)
        method = read(build / 'method.json')['capability']
        source = build / 'method' / method['capability_id']
        destination = library.root / 'exports' / build.name / method['capability_id']
        if not destination.exists():
            destination.parent.mkdir(parents=True, exist_ok=True); shutil.copytree(source,destination)
        validate_package(destination)
        return respond('exported', skill=str(destination / 'SKILL.md'), limits='Relevant excerpts included; no full originals, brief or work product. Review before sharing. Nothing was published or installed globally.')
    if brief:
        brief_data = read(path(brief)); validate_schema(brief_data,'brief')
        brief_id = 'brief-' + fingerprint(brief_data)[:24]
        write(folder / 'briefs' / f'{brief_id}.json', brief_data)
        if brief_id not in data['briefs']: data['briefs'].append(brief_id)
        state.update(brief_id=brief_id,target=target or 'review',goal_question_asked=False)
        library.save(folder,data); write(state_path,state)
    elif not state.get('brief_id') and action != 'explore':
        asked = state.get('goal_question_asked',False)
        state['goal_question_asked'] = True; write(state_path,state)
        return respond('needs_goal',message=None if asked else GOAL_QUESTION,already_asked=asked)
    if action == 'explore':
        from workflow import compile_workflow
        result = compile_workflow(output=str(run),project=project,intent='discover',reconciled=reconciled)
        if result['phase'] == 'choose': result['phase'] = 'explored'
        return {**respond(result['phase']),**result}
    brief_id = state['brief_id']; target = target or state.get('target','review'); state['target']=target; write(state_path,state)
    brief_data = read(folder / 'briefs' / f'{brief_id}.json')
    if target == 'review' and not brief_data['work']['text'].strip():
        return respond('needs_work',message='Share the work you want reviewed so I can apply the sources to it.')
    draft = folder / 'requests' / brief_id / data['active_revision'] / target
    draft.mkdir(parents=True,exist_ok=True)
    baseline_path = draft / 'baseline.json'
    if not baseline_path.exists():
        old = validate_ir(run) if (run / 'ir.json').exists() else {'units':[]}
        if not old['units']:
            for revision in reversed(data['revisions']):
                prior = safe_child(folder, revision['run'])
                if prior != run and (prior / 'ir.json').exists():
                    old = validate_ir(prior)
                    break
        write(baseline_path,{'units':{u['unit_id']:fingerprint(u) for u in old['units']},'source_passes':[]})
    def task(phase, prompt='goal-work.md', **extra):
        return respond(phase,agent_task={'prompt':str(ROOT / 'prompts' / prompt), 'brief':str(folder / 'briefs' / f'{brief_id}.json'),
                                        'target':target,'draft':str(draft),**extra})
    parts, units, pending, errors = checkpoint_state(run,corpus,docs,segments)
    if pending or errors: return task('extract','extract.md',pending_sources=pending,repairs=errors)
    if not units: return task('unsupported',reason='No supported knowledge extracted; explain the limitation without inventing a method.')
    try: validate_units(units,docs,segments)
    except Invalid as exc: return task('repair_extraction','reconcile.md',reason=str(exc))
    checkpoint_hash = fingerprint(parts); receipt_path=run / 'reconciliation.json'
    receipt=read(receipt_path) if receipt_path.exists() else {}
    if reconciled: write(receipt_path,{'schema_version':VERSION,'checkpoint_hash':checkpoint_hash}); receipt=read(receipt_path)
    if receipt != {'schema_version':VERSION,'checkpoint_hash':checkpoint_hash}: return task('reconcile','reconcile.md')
    ir = assemble(run); ir_hash=fingerprint(ir)
    coverage_path=draft / 'coverage.json'
    if not coverage_path.exists(): return task('assess_coverage',ir=str(run / 'ir.json'),ir_hash=ir_hash,brief_id=brief_id)
    coverage=read(coverage_path); validate_schema(coverage,'coverage-assessment')
    if coverage['brief_id'] != brief_id or coverage['ir_hash'] != ir_hash:
        return task('assess_coverage',ir=str(run / 'ir.json'),ir_hash=ir_hash,brief_id=brief_id,reason='Knowledge or goal changed; reassess sufficiency.')
    require(set(coverage['source_ids']) <= set(docs),'Coverage assessment cites unknown sources')
    write(draft / 'coverage-history' / f'{fingerprint(coverage)}.json',coverage)
    if coverage['decision'] == 'extend':
        require(coverage['source_ids'],'Another source pass needs source IDs')
        baseline=read(baseline_path)
        baseline['source_passes']=sorted(set(baseline['source_passes']) | set(coverage['source_ids'])); write(baseline_path,baseline)
        return task('extend_sources',sources=[str(run / f'sources/{sid}.json') for sid in coverage['source_ids']],
                    reason=coverage['reason'],instruction='Revisit these archived sources, extend checkpoints where supported, reconcile changes, then reassess coverage. Preserve existing evidence.')
    method_path=draft / 'method.json'
    if not method_path.exists(): return task('design_method',ir=str(run / 'ir.json'),ir_hash=ir_hash,brief_id=brief_id)
    method=read(method_path); validate_schema(method,'goal-method')
    if method['brief_id'] != brief_id or method['ir_hash'] != ir_hash: return task('design_method',ir_hash=ir_hash,brief_id=brief_id,reason='Method is stale for the goal or knowledge.')
    validate_capability_data(ir,{'schema_version':VERSION,'ir_hash':ir_hash,'capabilities':[method['capability']]})
    original=brief_data['work']['text']
    require(len(original.strip()) < 40 or original not in str(method['capability']), 'Reusable method copied the user work; use a synthetic example instead')
    result_path=draft / 'result.json'
    if not result_path.exists(): return task('apply_method',ir_hash=ir_hash,brief_id=brief_id,method_hash=fingerprint(method),method=str(method_path))
    result=read(result_path)
    try: validate_result(result,brief_id,ir,method,target)
    except Invalid as exc: return task('apply_method',ir_hash=ir_hash,brief_id=brief_id,method_hash=fingerprint(method),reason=str(exc))
    binding={'brief':fingerprint(brief_data),'method':fingerprint(method),'result':fingerprint(result),'ir':ir_hash}
    review_path=draft / 'semantic-review.json'
    if reviewed: write(review_path,binding)
    if not review_path.exists() or read(review_path) != binding: return task('review_result',instruction='Review the actual result against the brief and source evidence, then acknowledge with --reviewed. This is not independent effectiveness testing.')
    build_id='build-'+fingerprint({**binding,'target':target,'compiler':compiler_hash()})[:24]
    destination=folder / 'builds' / build_id
    if not destination.exists():
        destination.parent.mkdir(parents=True,exist_ok=True)
        temp=Path(tempfile.mkdtemp(prefix='.build-',dir=destination.parent))
        staging=temp / build_id; staging.mkdir()
        try:
            write(staging / 'brief.json',brief_data); write(staging / 'method.json',method); write(staging / 'result.json',result)
            cap=method['capability']; export_method(run,ir,cap,staging / 'method' / cap['capability_id'])
            # Render links into the method's actual named directory.
            text_write(staging / 'result.md',render_result(brief_data,result,method))
            baseline=read(baseline_path); now={u['unit_id']:fingerprint(u) for u in ir['units']}
            report={'structural_integrity':'passed','source_evidence_linkage':'passed',
                    'semantic_review':{'status':'assistant-reviewed','result_hash':fingerprint(result),'independent':False},
                    'effectiveness_testing':'not-run','coverage':coverage,
                    'reuse':{'reused_units':[k for k,v in now.items() if baseline['units'].get(k)==v],
                             'new_units':sorted(set(now)-set(baseline['units'])),
                             'changed_units':[k for k,v in now.items() if k in baseline['units'] and baseline['units'][k]!=v],
                             'source_passes_requested':baseline['source_passes'],'unsupported':coverage['unsupported']}}
            write(staging / 'validation.json',report)
            manifest={'schema_version':VERSION,'build_id':build_id,'collection_id':data['collection_id'],'source_revision':data['active_revision'],
                      'corpus_id':corpus['corpus_id'],'ir_hash':ir_hash,'knowledge_path':(run / 'history' / f'{ir_hash}.json').relative_to(folder).as_posix(),
                      'brief_id':brief_id,'brief_hash':fingerprint(brief_data),'method_hash':fingerprint(method),'result_hash':fingerprint(result),
                      'target':target,'compiler_hash':compiler_hash(),'files':inventory(staging)}
            write(staging / 'manifest.json',manifest)
            validate_build(staging, collection=folder)
            staging.rename(destination)
        finally:
            if temp.exists(): shutil.rmtree(temp)
    try: verification=validate_build(destination)
    except Exception:
        # A failed build is preserved for diagnosis, never announced as completed.
        raise
    if build_id not in data['builds']: data['builds'].append(build_id)
    library.save(folder,data)
    state['last_build']=destination.relative_to(folder).as_posix(); write(state_path,state)
    return respond('complete',result=str(destination / 'result.md'),method=str(destination / 'method' / method['capability']['capability_id'] / 'SKILL.md'),
                   build=str(destination),validation=verification,limits=result['limitations'],unsupported=result['unsupported'])
