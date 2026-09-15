# Infer the goal, then produce the useful outcome

The host assistant interprets natural language using the conversation and saved context. Python validates and routes the resulting intent; it is not a keyword classifier. Persist `intent` and `intent_reason` with the objective, context, constraints, work, desired_result and inferable success_criteria. These fields are internal. Do not ask the user to choose one of eight labels.

| Internal intent | Meaning | Useful result |
| --- | --- | --- |
| create | Write, design or build something new | A finished original deliverable, with evidence-backed design rationale where useful |
| review | Evaluate existing work | Assessment and prioritized feedback against relevant criteria |
| improve | Change existing work for the better | A revised version and explanation of material changes |
| decide | Choose among alternatives | Comparable options, criteria, tradeoffs and a conditional recommendation or evidence-based deferral |
| plan | Organize future work | Ordered steps, dependencies, checkpoints and completion criteria |
| do | Guide performance of a task | The next executable step, required observations, stopping conditions and checks |
| learn | Develop understanding and assess it | Explanation, example, exercise and a way to assess the learner's answer |
| reference | Answer from the collection | Direct answer, relevant evidence, conflicts and limits |

Distinguish “review my study plan” (review) from “teach me how to plan” (learn), and “design a learning exercise” (create) from “help me choose between courses” (decide). Choose by requested outcome, not domain nouns. For a mixed goal, pick the primary outcome and include supporting sections. Ask only if a material ambiguity cannot be resolved from context.

For review/improve, read the actual work. For create, do not require an existing draft. For a decision, infer options already supplied; if essential options or constraints are absent ask only for those. For plan/do, distinguish future steps from actions actually executed. For learn, adapt to the stated level, ask a useful diagnostic if necessary, and wait for responses before claiming understanding or proficiency. For reference, answer directly without manufacturing an elaborate procedure.

## Evidence and result contract

Read `schemas/outcome.schema.json`. New results use schema_version `1.1`, bound brief_id, ir_hash, method_hash and target equal to brief.intent. Give a summary and typed sections: deliverable, assessment, revision, options, recommendation, steps, lesson, exercise, feedback or answer. Each section has title, content, unit_ids and status.

Source-derived sections must cite real method units and distinguish explicit, inferred and synthesized. Original creative content has status original; its citations, if present, explain influence and are not claims the source authored it. User context is labeled user_context. Keep unsupported judgments, disagreements, limitations and additional general advice separate. A mixed section should be split so source evidence is not confused with the user's preferences or invented work.

Required section kinds are in `scripts/outcomes.py`. An unsupported request may instead return a specific limitation; never fill a required kind with invented facts. Deterministic section checks cannot establish semantic sufficiency. The assistant must review whether the answer actually meets the goal and whether evidence supports its conclusions.

Collections, IR, briefs, methods, results and exports have separate identities. Reuse the IR across intents. If new criteria or context require details not extracted before, request a targeted source pass and extend checkpoints. Never relabel a CREATE method as REVIEW without examining whether it supplies evaluative criteria.
