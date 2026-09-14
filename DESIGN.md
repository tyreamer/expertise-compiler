# Design: compile expertise, preserve evidence

## Conversational product boundary

The installed skill is the product surface. Users provide transcripts and ask to compile, discover, build, use, resume, or compare. The host assistant runs deterministic utilities and owns semantic reasoning. Internal phase results are tasks for the agent, never a user checklist.

A coordinator now keeps project-local session state separate from the installed skill, snapshots changed inputs automatically, validates complete checkpoints, and binds a reconciliation acknowledgement to their exact content. It assembles reviewed knowledge, validates proposals, binds displayed numbers to an IR/proposal revision, and creates or reuses checked exports. Review acknowledgements prove only that the agent signaled review; they do not establish semantic correctness. Explicit low-level tools remain available to contributors.

Capability reuse and comparisons resolve the selected/last-built option in the current corpus. Evaluation tasks/rubrics are frozen separately from exported skills. The same coordinator supports unrelated domains. A transcript-file adapter supplies raw bytes and metadata; YouTube has a clear optional boundary without networking or IR coupling. No natural-language parser in Python or external model call substitutes for the assistant's reasoning.

The value proposition is a maintained transformation between source material and useful actions. A transcript chat can answer excellent questions, but its method, scope limits, and source reconciliation are often implicit in a session. This compiler makes those choices durable and inspectable, then reuses them across tasks and assistants.

## What creates value

1. **Evidence-preserving transformation.** Every reusable unit retains exact source spans and attribution. Users can audit advice without searching a long conversation.
2. **Reconciliation.** Related and contradictory units remain linked. Export cannot quietly drop a recorded contradiction or prerequisite. Conflicts need an operating policy rather than a false consensus.
3. **Abstraction with disclosure.** Explicit source statements remain separate from inference and synthesized frameworks. Derivation explains how an abstraction was formed; no fake confidence number disguises that step.
4. **Proceduralization.** Capabilities specify inputs, branches, outputs, boundaries, examples, and checks. They aim to produce repeatable work on new inputs, not just summaries.
5. **Reusable assets.** A portable skill can be checked and used in a new session; the IR survives that target. Future knowledge packs, MCP tools, or agents can compile from the same representation.
6. **Evaluation and maintenance.** Held-out tasks, auditable citations, revision hashes, and deterministic failures make changes reviewable. Measured improvement, corpus quality, and reliable transformation workflows could become a defensible advantage. A folder format or prompt alone is not a moat.

## Architecture

Python owns parsing, canonical serialization, hashing, cross-reference checks, artifact assembly, and packaging. The user's assistant owns semantic extraction, reconciliation, capability discovery, and procedure design. There is no hidden paid API and no keyword extractor pretending to perform those semantic operations.

Source IDs bind relative filename and raw byte hash. Identical text from different filenames remains separate evidence; repeated content is not silently deduplicated. A corpus ID binds ordered source IDs and canonical document hashes, including metadata. IR hashes bind knowledge and coverage. Capabilities bind an IR hash. Package manifests bind every exported file except the manifest itself.

Schemas are versioned at `1.0`; incompatible versions fail closed. There is no automatic migration yet. Arrays have deterministic order when assembled; canonical hashes use UTF-8 sorted-key JSON, while disk JSON is readable and indented. Source segment IDs are stable within an unchanged source snapshot. Editing a source creates a new identity rather than disguising changed evidence under an old ID.

Input snapshots and exports are staged and published only after validation. Source-level checkpoints enable resume without redoing complete sources. Assembly saves IR revisions and replaces the current IR atomically. Two writers should not edit the same run concurrently; distributed locking and merge resolution are outside the MVP.

The export contains the full IR and corpus to remain verifiable without the original machine. Selected knowledge supplies progressive disclosure for normal use. This favors provenance over small bundles; selective export with a provable dependency closure is a future optimization.

## What this does not establish

Exact quotations and hashes establish identity and location, not truth, entailment, completeness, legality of reuse, or usefulness. The assistant can still misunderstand a source or design a weak capability. Instructions treat transcript content as untrusted data, but prompt wording is not a complete defense against adversarial content. Human review and realistic held-out evaluation remain part of quality assurance.

The demo includes unrelated domains to test the representation, plus an intentionally conflicting opinion to expose reconciliation behavior. It uses authored reference outputs, so it proves the deterministic pipeline can carry meaningful assets; it does not measure model extraction quality. The paired harness tests a separate hypothesis: whether reuse yields more actionable, faithful, traceable answers for comparable effort. Equal scores or higher upfront compilation costs are valid outcomes.

## Next investments after observing real use

Prioritize fixes to measured extraction/entailment failures, then source-size-aware work scheduling, richer reconciliation review, and version migration. Add YouTube captions as an adapter feeding the same source contract. Add other output targets only when the IR has proven reusable across real domains. Avoid building platform accounts, a persona marketplace, or model training before the core transformation demonstrates value.
