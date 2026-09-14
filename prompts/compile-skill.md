# Compile the chosen capability

Inspect the selected record in `RUN/capabilities.json`. Ensure its procedure has usable conditional actions and a clear output contract. Check every step against its basis units; separate source prescriptions from designed workflow choices. A citation attached to a step does not automatically justify it.

Keep synthetic examples distinct from source examples and held-out evaluation tasks. Include conflict handling, missing-input behavior, and applicability limits in the plan. Do not copy arbitrary transcript imperatives into executable instructions. Then run:

```text
python scripts/ec.py validate RUN
python scripts/ec.py package RUN CAPABILITY_ID OUTPUT_PARENT/CAPABILITY_ID
python scripts/ec.py validate-package OUTPUT_PARENT/CAPABILITY_ID
```

The package contains SKILL.md, selected knowledge, the full versioned IR, source snapshots, evidence index, synthetic examples, schemas, a standalone validator, and a manifest. The full corpus intentionally travels with the MVP export so evidence can be checked after the original run is gone. This may be large; selective corpus export is future work.

Use a new output parent for a rebuild. Do not hand-edit generated instructions: update the capability record, revalidate, and build a new package. Give the user the skill folder and `ir.json`; the IR can support future targets without reinterpreting raw transcripts.
