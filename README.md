# Expertise Compiler

Turn a folder of transcripts into **durable, source-traceable knowledge and reusable AI capabilities**. Local-first, MIT licensed, Python 3.10+, zero third-party runtime dependencies, and no model API calls.

The compiler is intended to outperform plain transcript Q&A on repeated tasks by producing reusable, provenance-preserving, capability-oriented artifacts: conditional procedures, conflict handling, clear boundaries, worked examples, and evidence you can audit. That is a product hypothesis to measure, not a claim that a skill always gives better answers. [The paired evaluation](docs/EVALUATION.md) lets you compare both approaches in your existing assistant.

```text
N transcript files → immutable source snapshot → versioned Expertise IR
                                                  ↓
                                      1–3 capability proposals
                                                  ↓
                                       portable Agent Skill
```

The **IR is the durable asset**. A skill is one export target. You can revise, reconcile, inspect, and reuse the knowledge without parsing the original captions again. This does not train model weights.

## Run the working demo

Clone the repository and open its folder:

```text
git clone https://github.com/tyreamer/expertise-compiler.git
cd expertise-compiler
```

These commands work in PowerShell, macOS, and Linux; use `python3` instead of `python` if your system requires it.

```text
python --version
python scripts/demo.py
python scripts/ec.py status workspace/demo-build/run
python scripts/ec.py validate workspace/demo-build/run
python workspace/demo-build/packages/container-herb-reviewer/checks/validate.py
python scripts/evaluate.py prepare
python -m unittest discover -s tests -v
```

The demo ingests four synthetic transcripts across gardening, photography, and debugging. It assembles 12 **authored fixture units**, including a synthesized framework and contradictory opinions, then builds three working packages. It does not pretend to automatically extract new knowledge without an assistant. Identical reruns resume; edited demo artifacts require a new `--output workspace/demo-v2` folder.

Inspect:

- `workspace/demo-build/run/ir.json`: full versioned knowledge and source coverage.
- `workspace/demo-build/run/capabilities.json`: three supported proposals.
- `workspace/demo-build/packages/container-herb-reviewer/SKILL.md`: executable review procedure.
- `workspace/demo-build/packages/handheld-blur-reviewer/SKILL.md`: conditional camera troubleshooting.
- `workspace/demo-build/packages/debug-experiment-planner/SKILL.md`: controlled debugging experiments.
- `workspace/demo-build/evaluation/`: self-contained baseline and compiled prompts.

## Compile your own transcripts with Codex or Claude Code

1. Open this repository as the working folder in Codex, or open a terminal here and start your existing Claude Code session. No global skill installation is necessary: explicitly ask it to read the local `SKILL.md`.
2. Put your UTF-8 `.txt`, `.md`, `.vtt`, or `.srt` files in a separate input folder, for example `workspace/input/`. Nested folders are supported. Keep the run output outside that input folder.
3. Give the assistant this request, replacing paths and the optional goal:

```text
Read ./SKILL.md and follow its compiler workflow. Ingest ./workspace/input
into ./workspace/my-corpus. Extract source-backed knowledge, reconcile it,
and propose no more than three useful capabilities. Preserve contradictory
advice and distinguish explicit knowledge from inference and synthesis.
Use the Python validators. My intended task is: [describe it, or omit this
sentence to discover capabilities]. If my goal is supported, build its
package in ./workspace/exports/CAPABILITY_ID and demonstrate it on a new task.
```

The assistant runs ingestion, writes extraction checkpoints, reconciles them, and writes a capability plan following `prompts/`. If no goal is specified, it will ask you to choose from the small proposal set. This is where your existing assistant supplies the reasoning; the command-line utilities only perform deterministic work.

To resume after interruption:

```text
Read ./SKILL.md. Resume ./workspace/my-corpus using the status command and
existing source checkpoints. Preserve completed work and finish validation
and the chosen package.
```

To use a generated capability, start a separate task/session and say:

```text
Read ./workspace/exports/CAPABILITY_ID/SKILL.md and its referenced knowledge
and evidence. Apply that capability to this input: [your new task].
```

Generated folders use the [Agent Skills format](https://agentskills.io/specification): matching folder/name, YAML frontmatter, `SKILL.md`, and relative supporting references. Explicit local-file invocation works without relying on a particular app's automatic skill discovery settings.

## Manual workflow and metadata

```text
python scripts/ec.py ingest workspace/input workspace/my-corpus --metadata workspace/metadata.json
python scripts/ec.py status workspace/my-corpus
```

Omit `--metadata` when none is available. Its JSON object maps exact relative filenames to optional fields:

```json
{
  "lesson.vtt": {
    "title": "Lesson title",
    "creator": "Creator supplied by the user",
    "url": "https://www.youtube.com/watch?v=EXAMPLE",
    "caption_type": "manual"
  }
}
```

Unknown metadata remains null or `unknown`; filenames are never treated as proof of a title or creator. Markdown H1 headings may supply a title. Caption type is `manual`, `automatic`, `synthetic`, or `unknown`. Metadata keys referring to absent files fail validation.

Follow `prompts/extract.md` to create one `units/SOURCE_ID.json` checkpoint per source. Follow `prompts/reconcile.md`, then:

```text
python scripts/ec.py assemble workspace/my-corpus
python scripts/ec.py validate workspace/my-corpus
```

Follow `prompts/discover-capabilities.md` to write `capabilities.json` bound to the `ir_hash` printed by `status`, then:

```text
python scripts/ec.py discover workspace/my-corpus
python scripts/ec.py package workspace/my-corpus CAPABILITY_ID workspace/exports/CAPABILITY_ID
python scripts/ec.py validate-package workspace/exports/CAPABILITY_ID
```

`discover` validates and displays assistant-authored proposals. It does not use keyword scoring or an undisclosed model. If the assistant is unavailable, ingestion and validation still work; semantic compilation awaits your assistant or manual authoring.

## Durable artifacts and validation

| Artifact | What it preserves |
| --- | --- |
| `raw/` | Original transcript bytes, including duplicates and caption overlap |
| `sources/` | Stable source IDs, metadata, byte hashes, raw and normalized segments, speaker labels and available times |
| `corpus.json` | Source inventory and canonical document hashes |
| `units/` | Resumable source-level extraction checkpoints |
| `ir.json` and `history/` | Versioned knowledge units, relations, evidence, derivations, attribution, source coverage, and assembled revisions |
| `capabilities.json` | One to three plans tied to a particular IR hash |
| Exported skill | Instructions, selected knowledge, full IR and source corpus, evidence, synthetic examples, schemas, offline validator, file-hash manifest |

Supported unit types: concept, definition, principle, heuristic, procedure, framework, example, warning, failure_pattern, claim, opinion. `status` is explicit, inferred, or synthesized; it describes the transformation, not confidence or truth. Every unit has source/segment references and exact quotes. Cross-source synthesis retains all contributing evidence.

Validation rejects malformed schema data, duplicate JSON keys/IDs, unknown fields, absent segments, altered quotes, invalid attribution, stale source/IR bindings, missing related units, unresolved packaging structure, path escapes, and file tampering. It re-normalizes original bytes to detect edited segment text. The published schemas are Draft 2020-12; the dependency-free validator implements the exact subset used here and rejects unsupported schema keywords. Regenerate schema files with `python scripts/build_schemas.py` after intentionally changing the schema definitions.

Validation proves structural integrity and evidence location. It **does not prove** that an interpretation follows from its quote, that a source is correct, that extraction is exhaustive, or that a procedure is useful. Those require assistant/human review and held-out evaluation. Manifest hashes detect accidental changes; they are not cryptographic signatures or a security boundary against someone rewriting both data and validator.

## Compare against transcript chat

```text
python scripts/evaluate.py prepare
```

Paste `workspace/demo-build/evaluation/baseline-prompt.md` and `compiled-prompt.md` into two fresh sessions using the same model. These prompts are self-contained and also work in ChatGPT or Claude web chats; the compiler itself needs local Python and an assistant with file access, or manual saving of the assistant's JSON outputs.

Save the returned arrays as `workspace/baseline-responses.json` and `workspace/compiled-responses.json`:

```text
python scripts/evaluate.py score workspace/baseline-responses.json --arm baseline --output workspace/baseline-report.json
python scripts/evaluate.py score workspace/compiled-responses.json --arm compiled --output workspace/compiled-report.json
```

Compare structured decisions and citation errors, then manually rate faithfulness, actionability, conflict handling, and reuse using `fixtures/held-out/rubric.json`. Record setup time and corrections. A schema-valid answer is not necessarily a good answer; the harness never declares a quality win automatically. See [full evaluation protocol](docs/EVALUATION.md).

## Scope and current limits

- **Local-first:** utilities perform no network requests and have no paid API dependency. Your chosen assistant may use a hosted service or have subscription/usage limits; that service's processing is not made local by this repository. Use a local model-capable assistant if fully offline reasoning is required.
- **Transcript contract:** UTF-8 files are stable inputs. YouTube fetching is deliberately not implemented in this MVP. Supply transcripts and optional original URLs. No scraping, audio transcription, or SDK setup is needed.
- **Normalization:** SRT/VTT cues preserve available start/end times and leading voice tags; plain dumps support leading `MM:SS`/`HH:MM:SS` (optionally bracketed) and `Name:` labels. Missing times/speakers remain null. Multi-voice markup within a single cue is not diarized. Original bytes remain available. Plain paragraphs are not automatically split into arbitrary token-sized chunks.
- **Scale:** source checkpoints support interrupted work, but the MVP loads the corpus for validation and reconciliation. Very large corpora require staged assistant review and may exceed context/memory; there is no automatic retrieval index or parallel extraction scheduler.
- **Revisions:** ingestion publishes a complete snapshot or nothing. Changed inputs/metadata require a new run. Assembly saves content-addressed IR history; extraction edits between assemblies are not separately journaled. Package builds require a new destination and publish only after validation.
- **Packaging:** the full corpus accompanies every skill for independent verification, including sources outside the selected capability. Review that content before sharing. The MIT license covers this compiler and synthetic fixtures; importing material does not change its ownership or licensing.
- **No proof of superiority yet:** the demo is authored and the checker is deterministic. Actual paired model answers and human ratings remain to be collected.

See [DESIGN.md](DESIGN.md) for the product thesis and architectural tradeoffs. Contributions should include focused tests for changes to evidence, normalization, resume behavior, or package integrity.
