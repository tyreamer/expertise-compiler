# Expertise Compiler

**Give your AI source material and tell it what you're trying to accomplish.** It applies relevant methods to your actual work, saves the sources and reasoning, and lets you use the same collection for different goals later.

Install it once as a skill, then tell your AI:

> Use these sources to improve this proposal. It's for a small business with a limited budget. Identify missing requirements and propose concrete changes. Save the sources as Product Research.

Or point it at a folder:

> Use the transcripts in ./input to review my plan in ./plan.md. Preserve my original and save an improved version with the reasons for your changes.

Your assistant saves the goal, applies the supported methods, and returns an assessment, prioritized findings, concrete changes, and links to the saved result and reusable method. You do not choose compiler stages or fill out forms. If you supply only sources, it asks what you hope to accomplish; **“save for later”** and **“explore what's useful”** are valid answers.

## Why this exists

Transcripts are information. Expertise Compiler turns their methods, procedures, examples, disagreements, and limitations into capabilities you can use again.

The most valuable output is work you can act on: a reviewed proposal, improved plan, or practical checklist. Underneath it is a reusable method with traceable evidence, clear limits and preserved disagreements. Source statements stay distinct from AI inference and your private context. The archive can support tomorrow's different goal without starting from scratch.

```text
Named source collection → durable, evidence-linked knowledge
                                      + your goal and work
                                      ↓
                         useful result + reusable method
```

**No model API key. No hosted compiler service. Your existing AI does the reasoning.** The underlying knowledge remains yours to inspect and reuse beyond a single skill.

## Install once

### Codex

Send Codex this message:

> Use $skill-installer to install the repository root at https://github.com/tyreamer/expertise-compiler as a personal skill named expertise-compiler, including its supporting files.

Codex's installer supports skills from other repositories. Restart Codex if the skill does not appear after installation. [Official installation guidance](https://learn.chatgpt.com/docs/build-skills).

### Claude Code

Send Claude Code this message:

> Install https://github.com/tyreamer/expertise-compiler as my personal expertise-compiler skill. Download and review the repository, then use its bundled installer to copy the complete skill to ~/.claude/skills/expertise-compiler. Preserve any existing installation.

Claude Code discovers personal skills in that folder and can invoke them from matching natural-language requests. [Official skill guidance](https://code.claude.com/docs/en/skills).

The assistant handles downloading and copying; you do not need to clone the repository or manually load SKILL.md. Your environment may ask for file-access permission. [Installation details and troubleshooting](docs/INSTALLATION.md).

## Talk to it

| Say this | What happens |
| --- | --- |
| “Use these sources to improve this proposal.” | Reviews the actual proposal and saves concrete changes with evidence and limits. |
| “Save these as Product Research for later.” | Archives originals and metadata without forcing a skill or goal. |
| “Apply the same approach to this new draft.” | Saves a new brief and result using relevant existing knowledge. |
| “Use Product Research to make a checklist instead.” | Reuses knowledge or rereads archived sources when the new goal needs more. |
| “Add these sources and show me what changes.” | Preserves earlier versions, adds sources and revisits the current task. |
| “Turn what we used into a reusable agent skill.” | Exports the method and relevant evidence excerpts locally. |
| “Explore what's useful in this collection.” | Explains a few supported possibilities and meaningful gaps. |
| “Compare this with ordinary transcript chat.” | Prepares a fair comparison of quality and effort across first use, reuse and updates. |

For example, photography transcripts might support a **Handheld Blur Reviewer** that checks focus before suggesting shutter changes. The assistant explains what it can do, what the sources do not establish, and where the resulting skill is saved. It does not promise a full photography expert from a few narrow lessons.

The task is completed in the same workflow. A source-specific method remains available for the next task; a new goal is not permanently tied to the first method or output format.

## Saved locally, reusable later

Your project's `.expertise-compiler/library.json` maps readable collection names to stable IDs. Collections preserve original files, source metadata, normalized segments, extraction notes, knowledge revisions, private briefs and immutable completed builds. Each result is bound to its sources, knowledge, brief, method, output target and compiler fingerprint. Interrupted work resumes from saved checkpoints. Existing runs can be adopted without modifying their original folders.

Ordinary skill exports contain selected knowledge and relevant quotations. They exclude full raw transcripts, unrelated source documents and private briefs/work products. The full audit material stays in the collection. Exporting locally does not publish or globally install anything, and citations do not establish permission to share. Ask your assistant explicitly when you want to export or install a method.

## What you need

Use local Codex or Claude Code with permission to read files and run local tools. A local Python 3.10+ runtime is needed underneath; your assistant checks for it and helps with setup if missing. There are no additional Python packages to install for normal use.

Supply UTF-8 `.txt`, `.md`, `.vtt`, or `.srt` transcripts as accessible attachments or a folder. YouTube fetching is not implemented yet; exported transcripts work now, and original video URLs can be preserved with them.

Work stays in your local project. Your chosen AI service may still process content remotely and have subscription or usage limits. A plain web chat without local file/tool access cannot run the installed compiler autonomously, though comparison prompts can be used there.

## Built to earn its value

The goal is better repeated work than attaching transcripts and asking questions: durable methods, preserved evidence, honest scope, reconciled disagreement, and portable skills. That improvement should be measured, not assumed.

Ask for a comparison with the same sources, goal, constraints and access to persistent context. Measure quality, corrections, setup, reuse and update effort. Comparable quality with substantially less repeated effort can be valuable. No live effectiveness result is claimed. Passing package validation proves integrity and evidence linkage, not sound judgment or superiority. [How comparisons work](docs/EVALUATION.md).

MIT licensed. Synthetic examples cover gardening, photography, and debugging. Imported source material retains its ownership and licensing.

## For contributors

[Development and tests](docs/DEVELOPING.md) · [Internal command reference](docs/CLI.md) · [Architecture](DESIGN.md) · [Conversational acceptance flows](docs/ASSISTANT-FLOWS.md)
