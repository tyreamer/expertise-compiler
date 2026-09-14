# Propose at most three capabilities

Read `RUN/ir.json`, `schemas/capability.schema.json`, and `schemas/capabilities.schema.json`. Obtain `ir_hash` from `python scripts/ec.py status RUN`. Write `RUN/capabilities.json` with version, that hash, and one to three capability records.

For each proposal, identify a recurring user input, a transformation the evidence supports, an actionable output contract, and boundaries. Prefer review, diagnosis, planning, or guided execution over a generic "ask this expert" chatbot. State the practical reuse benefit in `rationale`, not an unmeasured accuracy claim.

Each capability needs a lowercase hyphenated ID, useful description, selected `unit_ids`, ordered `steps` with supporting IDs, boundaries, conflict policy, pre-response checks, and at least one synthetic worked example with its basis IDs. Include the transitive closure of related units, including contradictions, so packaging cannot hide counterevidence. If a requested capability lacks support, explain the missing evidence rather than inventing steps.

Limit the list to three across the corpus, not three per source. For a specified user goal, one good proposal is enough. If choosing among multiple supported goals is necessary, show the input/output/boundary of each and let the user choose. No numerical confidence or pretend automatic ranking.

Run `python scripts/ec.py discover RUN`. This command validates and displays your authored proposals; it is not a language-model substitute. `fixtures/demo_capabilities.json` illustrates complete records.
