# Internal command reference

These commands are for the assistant, contributors, and advanced debugging. Normal users install the skill and talk to it; see [README](../README.md). Run from a user's project and resolve the installed scripts by absolute path. Relative input/output/metadata paths resolve against `--project` for the coordinator.

## Goal coordinator

```text
python /path/to/expertise-compiler/scripts/ec.py work --project . --input ./input --name "Product Research" --brief ./.expertise-compiler/inbox/brief.json
python /path/to/expertise-compiler/scripts/ec.py work --project . --collection "Product Research"
python /path/to/expertise-compiler/scripts/ec.py work --project . --collection "Product Research" --reconciled
python /path/to/expertise-compiler/scripts/ec.py work --project . --collection "Product Research" --reviewed
python /path/to/expertise-compiler/scripts/ec.py work --project . --collection "Product Research" --brief NEW_BRIEF --target checklist
python /path/to/expertise-compiler/scripts/ec.py work --project . --input ./more --collection "Product Research" --action add
python /path/to/expertise-compiler/scripts/ec.py work --project . --input ./input --name "Leadership" --action prepare
python /path/to/expertise-compiler/scripts/ec.py work --project . --collection "Leadership" --action inspect
python /path/to/expertise-compiler/scripts/ec.py work --project . --collection "Leadership" --action remove --remove lesson.txt
python /path/to/expertise-compiler/scripts/ec.py work --project . --collection "Leadership" --action replace --input ./updated
python /path/to/expertise-compiler/scripts/ec.py work --project . --collection "Leadership" --action compare
python /path/to/expertise-compiler/scripts/ec.py work --project . --collection "Leadership" --action archive
python /path/to/expertise-compiler/scripts/ec.py work --project . --collection "Leadership" --action restore
python /path/to/expertise-compiler/scripts/ec.py work --project . --action list
python /path/to/expertise-compiler/scripts/ec.py work --project . --collection "Product Research" --action export
python /path/to/expertise-compiler/scripts/ec.py validate-build BUILD_FOLDER
```

Use --action save to archive without a goal, --action explore for optional discovery, and --adopt OLD_RUN to copy an existing run. Do not repeat --input on continuation calls. The assistant saves briefs from conversation, handles returned tasks and acknowledges actual review; users do not operate this CLI. [Complete phase contract](../prompts/goal-work.md).

New briefs record lowercase intent (create/review/improve/decide/plan/do/learn/reference) and intent_reason; target is inferred from that saved field. --target checklist is retained for legacy briefs only. New typed results use outcome schema 1.1 and save a readable method, not an automatic skill package. --action prepare extracts and reconciles knowledge without a goal, result or skill. --action save only preserves sources.

Compare explicit source revisions with --before/--after; compare historical knowledge in those snapshots with --before-knowledge/--after-knowledge hashes. The assistant resolves these from manifests; users need not know them. Removing a source retains historical originals. Replacing same-named input changes the active source; adding a different version retains both. Archived collections remain listable and can be restored or explicitly used by name.

## Legacy capability coordinator

```text
python /path/to/expertise-compiler/scripts/ec.py compile ./input --project .
python /path/to/expertise-compiler/scripts/ec.py compile --project .
python /path/to/expertise-compiler/scripts/ec.py compile --project . --reconciled
python /path/to/expertise-compiler/scripts/ec.py compile --project . --intent discover
python /path/to/expertise-compiler/scripts/ec.py compile --project . --intent build --select 2
python /path/to/expertise-compiler/scripts/ec.py compile --project . --intent build --build-all
python /path/to/expertise-compiler/scripts/ec.py compile --project . --intent use
python /path/to/expertise-compiler/scripts/ec.py compile --project . --intent compare
python /path/to/expertise-compiler/scripts/ec.py compile --project . --run workspace/existing-run
```

Quote paths containing spaces. Replace `python` with the discovered interpreter where necessary. The operator interprets natural-language intent; the coordinator takes explicit arguments and returns a structured phase. [Phase contract](../prompts/operate.md).

Optional `INPUT OUTPUT` positionals override the run location; OUTPUT must be inside PROJECT and outside INPUT. With no input, the saved project session resumes. `--run` adopts an existing run. `--metadata` supplies a JSON filename-to-metadata map. `--tasks` and `--rubric` choose an evaluation suite for `--intent compare`.

The coordinator stops at reasoning boundaries for the **agent**, not the user. Extraction/checkpoint repair, reconciliation, discovery, and answer generation require the host assistant. `--reconciled` attests a review bound to the current checkpoints; changed checkpoints invalidate it. No model process, API, or keyword pseudo-extractor is called.

## Low-level utilities retained for development

```text
python scripts/ec.py ingest workspace/input workspace/my-corpus --metadata workspace/metadata.json
python scripts/ec.py status workspace/my-corpus
python scripts/ec.py assemble workspace/my-corpus
python scripts/ec.py validate workspace/my-corpus
python scripts/ec.py discover workspace/my-corpus
python scripts/ec.py package workspace/my-corpus CAPABILITY_ID workspace/exports/CAPABILITY_ID
python scripts/ec.py validate-package workspace/exports/CAPABILITY_ID
```

Low-level paths resolve against the process working directory. `assemble` deliberately bypasses the coordinator's review receipt for contributors; the installed skill uses the coordinator. Direct manual assembly cannot certify that semantic review occurred.

Metadata maps exact relative filenames to optional `title`, `creator`, `url`, and `caption_type`:

```json
{"lesson.vtt":{"title":"Provided title","creator":"Provided name","url":"https://www.youtube.com/watch?v=EXAMPLE","caption_type":"manual"}}
```

Caption type is `manual`, `automatic`, `synthetic`, or `unknown`; absent titles/creators/URLs remain null, except Markdown H1 titles. All bytes must decode as UTF-8. Original files and normalized segments remain available. SRT/VTT preserve cue times and leading voice labels; plain dumps recognize common timestamp/speaker prefixes. No timing or diarization is invented. Malformed captions fail rather than silently dropping content.

## Demo and comparison

```text
python scripts/demo.py --output workspace/demo-current
python scripts/evaluate.py prepare --demo workspace/demo-current
python scripts/evaluate.py score workspace/baseline.json --arm baseline --run workspace/demo-current/run --evaluation workspace/demo-current/evaluation
python scripts/evaluate.py score workspace/compiled.json --arm compiled --run workspace/demo-current/run --evaluation workspace/demo-current/evaluation
```

The demo uses authored synthetic knowledge, not automated semantic extraction. Use a new output directory after changing demo content. The generalized coordinator prepares comparisons for any capability with an authored suite. The old default gardening scorer remains for compatibility; pass `--evaluation` to check the frozen, corpus-bound suite. Structural failures return errors; incorrect decisions/citations appear in reports. No score declares a quality win.
