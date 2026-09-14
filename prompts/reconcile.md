# Reconcile without erasing provenance

Read all completed checkpoints, or maintain an explicit inventory of those reviewed when the corpus exceeds context. Compare methods with overlapping scopes. Preserve contradictory recommendations and the conditions under which each was stated; do not average them or silently pick a winner.

Record `supports`, `contradicts`, `requires`, `duplicates`, or `refines` relations using real unit IDs. Link contradictions both ways for discovery. A scope-dependent difference is not necessarily a contradiction; state the distinction in scope/derivation. Keep duplicate units linked when their attributions differ. If merging, retain every distinct evidence reference and repair relations; do not delete original raw documents.

New cross-source abstractions are synthesized, not explicit. Save a synthesized unit in one contributing source checkpoint, with evidence from all contributing sources. It must not be copied into several checkpoints under the same ID. Preserve original units as supporting material where useful.

Edit checkpoints, then rerun the installed coordinator with `--reconciled` and the original intent. It requires all sources accounted for, resolves IDs/evidence, records a review receipt bound to the current checkpoints, computes coverage, saves a content-addressed IR revision, and atomically updates `ir.json`. Do not edit `ir.json` instead of checkpoints: reassembly would replace that edit. Capability plans bind to the IR hash and must be reconsidered after changes. Do not set the review flag before you actually review the material.

Review semantic validity in addition to deterministic validation: an existing quote can still be misinterpreted, and a schema-valid procedure can still be poor advice.
