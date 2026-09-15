# Internal operator guide: finish the goal

The assistant performs these operations. Paths below resolve against PROJECT unless prefixed SKILL_ROOT. Quote shell arguments; never interpolate source text into shell commands.

## Brief and collection

Write a UTF-8 JSON brief in PROJECT/.expertise-compiler/inbox using `schemas/brief.schema.json`. Required: schema_version "1.0", objective, context (empty if absent), constraints (array), work {label,text}, desired_result, success_criteria (nonempty array). Infer usefulness criteria from the task; record consequential assumptions in context. Preserve supplied work verbatim, or read the supplied text file and put its content into work.text and name into work.label. This private snapshot is not source evidence. Users do not write JSON.

Start with absolute paths:

```text
python SKILL_ROOT/scripts/ec.py work --project PROJECT --input INPUT --name "Product Research" --brief BRIEF
```

Add `--target checklist` for a plan/checklist. Review without work returns needs_work; ask only for that missing work. No goal: omit --brief; needs_goal returns the question and persists that it was asked. Save-only: --action save, no brief. Explore-only: --action explore, no brief; follow extraction/discovery and stop at explored without forcing a build.

After ingestion, omit --input, --name, --adopt and --brief on continuation calls. Continue `work --project PROJECT --collection "Product Research"`. Active brief and target survive interruptions. Do not repeat ingestion on each stage.

New task: save a new brief and pass --brief with existing --collection. Source additions: --input INPUT --collection NAME --action add; then resume work for the active goal if changed results were requested. Explain old/new result differences, not just source counts. Rebuild: --action rebuild. Identical inputs are idempotent; changed knowledge, brief, target or compiler creates a new build.

List names with `work --action list`. Adopt with `work --adopt OLD_RUN --name NAME --action save`; the old run is untouched. Read legacy `.expertise-compiler/session.json` to locate prior runs when needed, never erase them.

## Complete returned agent tasks

Returned run/draft/brief paths are authoritative. Read schemas from SKILL_ROOT/schemas. Stay in the work coordinator even when an older semantic guide mentions the legacy compile command.

1. **extract / repair_extraction:** follow [extract.md](extract.md). Use the brief to guide relevance but keep user context out of knowledge. Preserve existing units. Save complete source checkpoints in RUN/units; notes describe reviewed coverage and omissions.
2. **reconcile:** follow [reconcile.md](reconcile.md), then continue work with --reconciled. Read relevant methods/conflicts before acknowledging. Checkpoint changes invalidate this receipt.
3. **assess_coverage:** inspect IR against the brief. Write DRAFT/coverage.json per coverage-assessment schema, with returned brief_id/ir_hash. decision is reuse when sufficient, extend for a targeted pass; explain reason and unsupported requests. For extend provide real source_ids. Processing every source does not prove exhaustive extraction.
4. **extend_sources:** reread specified archived sources and extend checkpoints without deleting prior evidence. Reconcile, then rewrite coverage against the new IR hash. If rereading adds nothing, switch to reuse with honest unsupported limits. Coverage history and requested passes are preserved.
5. **design_method:** write DRAFT/method.json per goal-method schema: schema_version, returned brief_id/ir_hash, capability object. Read capability.schema.json and [compile-skill.md](compile-skill.md). Reuse a previous build's method when appropriate. Include required/contradictory evidence closure. Use synthetic examples, never private user work. Keep method source-specific and relevant to the goal.
6. **apply_method:** read actual work and method. Write DRAFT/result.json per work-result schema with returned brief_id/ir_hash/method_hash. Give direct assessment, findings ordered high to low priority, concrete changes, optional proposed_revision, checklist actions with observable done_when criteria, disagreements, limitations and unsupported judgments. Source-derived findings and checklist entries cite method unit_ids. Keep additional_general_advice separate. For a checklist supply practical steps; for review improve the actual text, not merely summarize methods. Save revisions separately from the original.
7. **review_result:** inspect result, evidence and brief together for entailment, scope, inference labels, actionable changes, privacy and disagreements. Repair, rerun, and only then acknowledge with --reviewed. This is assistant review, not independent evaluation.
8. **complete:** saved artifacts exist and validate. When reopening, use `ec.py validate-build BUILD`. Lead with useful findings and clickable result/method links. Failed validation is not completion.

No useful knowledge returns unsupported: explain the limitation; do not claim a compiled result. The archive remains available.

## Reuse, export and evaluation

Collections live at PROJECT/.expertise-compiler/collections/ID. collection.json maps source revisions, briefs and builds. Sources retain raw files, canonical documents, checkpoints and IR history. Builds retain brief, method, result and provenance bindings. requests contains resumable drafts, not completion artifacts. validation.json records reused/new/changed knowledge and unsupported requests.

The method inside a private build is scoped but is not automatically shared or installed. On explicit request, `work --action export` copies only the method to the local exports directory. Package validation checks selected evidence/internal integrity; validate-build also checks against private originals and full IR. Briefs, drafts and unrelated transcripts stay out of ordinary exports. Review semantic privacy too: schemas cannot detect a private detail paraphrased into a method.

For comparisons follow [evaluate.md](evaluate.md) and [the protocol](../docs/EVALUATION.md). Supply the build brief as shared context to prepare_comparison, with its matching source/IR revision. Give both arms full source access and permission to retain context; conceal a frozen rubric. Track actual effort and leave unmeasured values empty.
