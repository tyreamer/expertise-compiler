# Conversational acceptance protocol

These are behavioral acceptance cases, not claims of live model performance. Automated tests replay deterministic state transitions with explicitly authored semantic checkpoints; a real assistant still needs to interpret and perform the reasoning tasks.

Install a clean copy into a temporary skill location, open a separate project with the fixture inputs, and confirm natural-language discovery. In a real Codex/Claude Code session, do not instruct the assistant to read SKILL.md or expose internal commands. Record whether it activates, performs the complete loop, and produces a useful answer. Run the same flow in both clients when available; shell-only tests cannot certify a client's natural-language skill matching.

## Photography

1. “Compile ./fixtures/photography.” The assistant reads the transcript and completes the reasoning itself, then offers up to three grounded capabilities. A single strong option is fine.
2. “What useful capabilities can this corpus support?” It explains a narrow handheld blur/focus review. It must not claim coverage of composition or commercial pricing.
3. “Build the photo critique capability.” It maps the phrase to the supported option, states the limitation, and builds it without asking for an internal identifier.
4. “Use that capability on this held-out example: a ceramic bowl is blurry but lettering behind it is sharp.” It examines focus rather than treating a faster shutter as a universal fix.
5. “Compare it against raw transcript chat.” It prepares matched new tasks and separate expected answers. Without isolated sessions it hands over two ready-to-paste prompts, not a terminal checklist.

## Debugging

Repeat with `./fixtures/debugging`: discover a debugging experiment planner, build the strongest supported capability, and apply it to an importer with an intermittent missing row and no known reproducer. Expect a small reproducible input and expected/actual outputs before an invented patch. An ineffective change should be reverted before the next hypothesis; a single passing test is not a universal guarantee.

`fixtures/flows/conversations.json` is the machine-readable conversation contract. Domain task/rubric files supply new synthetic examples. The narrow domain folders duplicate the original small transcript fixtures solely to make the natural input paths usable; no IR logic depends on those folder names.

## Interruptions, changes, and evidence

- Interrupt after one completed source and resume. Completed evidence remains; only missing/bad checkpoints need work.
- Edit a checkpoint after reconciliation. The coordinator requires another review before building.
- Change the proposal order after displaying numbers. An old “build 2” must get a refreshed list rather than the wrong skill.
- Add/change a transcript. A new snapshot appears; prior source evidence remains unchanged.
- Give untimed text. Do not manufacture a recording duration.
- Supply only an unsupported YouTube link. Explain the adapter limitation and request exported transcripts without a network/audio fallback.
- Use an installed skill from a different project with spaces in paths. Work belongs to that project, not the installation.
- Ask for a capability unsupported by the material. Explain the gap, rather than manufacturing three weak skills.

Pass criteria: conversational intent leads to usable grounded assets without user-run commands; evidence, synthesis labels, conflicts, and limits survive. Mark client-level activation and answer quality as untested until a real session has been observed.
