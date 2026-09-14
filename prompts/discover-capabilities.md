# Propose at most three capabilities

Read `RUN/ir.json`, `schemas/capability.schema.json`, and `schemas/capabilities.schema.json`. Obtain `ir_hash` from `python scripts/ec.py status RUN`. Write `RUN/capabilities.json` with version, that hash, and one to three capability records.

For each proposal, identify a recurring user input, a transformation the evidence supports, an actionable output contract, and boundaries. Prefer review, diagnosis, planning, or guided execution over a generic "ask this expert" chatbot. State the practical reuse benefit in `rationale`, not an unmeasured accuracy claim.

Each capability needs a lowercase hyphenated ID, useful description, selected `unit_ids`, ordered `steps` with supporting IDs, boundaries, conflict policy, pre-response checks, and at least one synthetic worked example with its basis IDs. Include the transitive closure of related units, including contradictions, so packaging cannot hide counterevidence. If a requested capability lacks support, explain the missing evidence rather than inventing steps.

Limit the list to three across the corpus, not three per source. For a specified user goal, one good proposal is enough. If choosing among multiple supported goals is necessary, show the input/output/boundary of each and let the user choose. No numerical confidence or pretend automatic ranking.

If the user delegated strongest-capability selection, rank your small set by usefulness for their material and proceed to build it. If they asked for a particular goal, do not require them to select it again.

Optional `RUN/discovery-assessment.json` follows `schemas/discovery-assessment.schema.json`: version, current `ir_hash`, `no_capability_reason` (empty when capabilities are supported), and up to three `weakly_supported` topic/reason/unit_ids entries. Include real requested scope gaps, not invented weak topics. If the IR has knowledge but supports no useful capability, write a nonempty `no_capability_reason` rather than fabricating a plan. A current nonempty reason prevents packaging even if an older proposal file exists. Clear that reason when supported plans are subsequently authored.

Rerun the installed coordinator with the original intent. It validates the plans and presents or builds them. `fixtures/demo_capabilities.json` illustrates complete records. Commands and schema repair remain your responsibility, not the user's.
