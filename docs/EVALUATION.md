# Compare a capability with transcript chat

Tell your assistant:

> Compare this capability against just using the raw transcripts.

It prepares the comparison, saves the material, and checks the returned answers. You do not need a command line.

This is not yet an automatically executed baseline → refinement → release loop. Independent runs and human semantic review must be coordinated, and corrections/rebuilds are assistant-led. Existing artifact validation does not automatically certify behavioral effectiveness. The [concept-validation testing guide](testing-guide.md) defines participant groups, paired tasks, refinement holdouts and proposed decision gates for testing this loop before automating it.

Both approaches receive identical new tasks, the same user goal/constraints and full original transcripts. The compiled arm additionally receives its reusable method and selected evidence. Both may create and retain notes, context and methods in separate workspaces. Expected answers stay separate from both prompts. The baseline is allowed to use ordinary chat well; it is not forced to forget earlier work.

The comparison looks for useful next actions, faithful advice, appropriate handling of gaps and disagreement, traceable evidence, and consistent reuse. Setup effort and corrections matter too: compilation has an upfront cost.

## Three stages, with persistent context

1. **Initial task:** review the same previously unseen work against the same goal. Count compiler installation/setup and extraction time; count baseline source preparation and organization too.
2. **Reuse:** give both arms a new draft or a new checklist goal. Preserve each arm's own prior notes and context. Measure how much the user must restate, repair or verify.
3. **Update:** add the same source to both workspaces, ask for a revised result, and measure update work and whether outdated advice was corrected. Keep earlier results available in both arms.

Before running, freeze tasks and rating criteria, record model/settings and source revision, and agree what difference in effort would matter to the user. For example, define a quality floor of no critical unsupported recommendation, then compare total user effort over all three stages. This is a proposed criterion, not a reported outcome.

The harness creates `effort.json` with six empty observations: baseline/compiled × initial/reuse/update. Record active user minutes, assistant minutes, user messages, corrections, a human quality rating and notes. Use the same rating scale in both arms; define it before viewing answers. Leave unknown values null. Include manual evidence-checking time and failed attempts. Report quality and effort separately; comparable quality with materially less repeated effort can be a useful result. No automatic winner is inferred from these fields.

## Fresh sessions matter

An assistant that already read the compiled method cannot pretend to be an uninformed baseline. When independent sessions are available and authorized, it can coordinate them. Otherwise it gives you two ready-to-paste prompts for fresh chats using the same model. Return their answers and it will handle checking. This context-isolation handoff does not require you to run scripts.

Assistant-created cases are labeled as such. Supplied independent holdouts provide stronger evidence. Worked examples are not presented as fresh evaluation tasks. Expected answers are frozen before either approach is tested.

## Read results honestly

Checks identify wrong structured decisions, missing quotations, and broken evidence links. A real quote can still be irrelevant to the advice, so meaning and scope also need review. A tie or baseline win is useful feedback. No automatic score establishes superiority.

Gardening, photography, and debugging fixtures illustrate the process; they are not a broad accuracy benchmark. No live paired-model performance result is claimed. See [contributor instructions](DEVELOPING.md) and the [internal evaluation guide](../prompts/evaluate.md) for details.
