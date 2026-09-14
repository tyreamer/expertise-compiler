# Compare a capability with transcript chat

Tell your assistant:

> Compare this capability against just using the raw transcripts.

It prepares the comparison, saves the material, and checks the returned answers. You do not need a command line.

Both approaches receive identical new tasks and answer requirements. One gets the original transcripts; the other gets the reusable method, worked examples, and selected evidence. Expected answers stay separate from both prompts.

The comparison looks for useful next actions, faithful advice, appropriate handling of gaps and disagreement, traceable evidence, and consistent reuse. Setup effort and corrections matter too: compilation has an upfront cost.

## Fresh sessions matter

An assistant that already read the compiled method cannot pretend to be an uninformed baseline. When independent sessions are available and authorized, it can coordinate them. Otherwise it gives you two ready-to-paste prompts for fresh chats using the same model. Return their answers and it will handle checking. This context-isolation handoff does not require you to run scripts.

Assistant-created cases are labeled as such. Supplied independent holdouts provide stronger evidence. Worked examples are not presented as fresh evaluation tasks. Expected answers are frozen before either approach is tested.

## Read results honestly

Checks identify wrong structured decisions, missing quotations, and broken evidence links. A real quote can still be irrelevant to the advice, so meaning and scope also need review. A tie or baseline win is useful feedback. No automatic score establishes superiority.

Gardening, photography, and debugging fixtures illustrate the process; they are not a broad accuracy benchmark. No live paired-model performance result is claimed. See [contributor instructions](DEVELOPING.md) and the [internal evaluation guide](../prompts/evaluate.md) for details.
