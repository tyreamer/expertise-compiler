# Paired evaluation without model APIs

The benchmark asks whether a reusable capability helps on new tasks compared with attaching raw transcripts. It is not a benchmark of Python execution speed or whether a JSON file can be produced.

## Reproduce

1. Run `python scripts/demo.py`, then `python scripts/evaluate.py prepare`.
2. Start two fresh sessions with the same assistant/model/settings. Randomize which arm goes first. Give one only `workspace/demo-build/evaluation/baseline-prompt.md`; give the other only `compiled-prompt.md`. Both contain the same three held-out tasks and response contract. The baseline gets all original transcripts. The compiled arm gets the skill, selected knowledge with exact evidence, and a source-name map. Neither receives expected decisions or the scoring rubric.
3. Keep both sessions available across the task set so both can benefit from prior context. Do not give only one arm extra coaching or tools. Save both response JSON arrays unchanged. If a format repair is necessary, record it and use the same repair instruction for either arm.
4. Run `evaluate.py score RESPONSES --arm baseline` and the corresponding compiled command, as shown in README. Structural decision matches and quotation errors are deterministic. The scorer checks original source quotations in both arms and unit-to-evidence links in the compiled arm. Malformed response contracts fail with a nonzero exit status; incorrect decisions or citations appear in a report rather than masquerading as schema errors.
5. Blind the answer labels for human review where practical. Score the four 0–2 dimensions in `fixtures/held-out/rubric.json`. Check that prose actually agrees with its structured decisions. A response can game decision fields or cite an irrelevant but real quotation, so automatic scores alone are insufficient.
6. Record assistant/model, date, setup time, answer time, number of corrections, evidence-verification effort, and human ratings. Include compilation/setup cost when comparing first use, and amortize it transparently when comparing repeated use.

## Held-out cases

The task fixtures exercise a new damp-soil scenario with conflicting advice, an underdetermined symptom report, and an unsupported numeric request. None of these task texts are used as generated package examples. The authored demo capability does reflect the broad design objective of handling missing information and scope limits; these are small illustrative holdouts, not a large independently collected benchmark.

The expected damp-soil decision represents the chosen capability's disclosed operating policy. It is not botanical ground truth. A baseline that appropriately describes unresolved disagreement deserves credit in human review even if its structured action differs.

## Interpretation

Evidence of benefit would include fewer unsupported claims, better conditional next actions, more faithful conflict handling, lower effort to audit evidence, or more consistent repeated outputs. A tie, baseline win, or cost that outweighs reuse is informative. The scorer always reports `quality_win_established: false` because a numerical quality judgment requires paired answers and human review outside its structural remit.

No paired model run has been performed or invented for the repository. Unit tests for the scorer use explicitly synthetic response records to test error detection, not to demonstrate performance. To evaluate arbitrary corpora, collect domain-specific held-out tasks and expected criteria before compiling, then adapt the currently demo-specific scorer and response fields. Do not report this tiny gardening benchmark as a cross-domain accuracy result.
