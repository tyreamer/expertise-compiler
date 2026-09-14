# Expertise Compiler

**Turn transcripts into reusable, source-backed AI capabilities.**

Install it once as a skill, then tell your AI:

> Compile these transcripts.

Or point it at a folder:

> Compile the transcripts in ./input and tell me the most useful capabilities this material can support.

Your assistant does the work and offers a small number of useful capabilities. Say **“Build capability 2”**, then **“Use it on this problem.”** No terminal workflow to learn.

## Why this exists

Transcripts are information. Expertise Compiler turns their methods, procedures, examples, disagreements, and limitations into capabilities you can use again.

Instead of reconstructing advice in every chat, you get a reusable method with traceable evidence, clear limits, and an explanation of where sources disagree. Source statements stay distinct from AI inference and synthesis.

```text
Transcripts
    ↓
Expertise Compiler
    ↓
Structured Expertise
    ↓
Reusable AI Capabilities
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
| “Compile these transcripts.” | Your assistant reads the supplied material and proposes 1–3 useful capabilities. |
| “What can I build from this content?” | It explains supported uses and meaningful gaps. |
| “Build the strongest capabilities.” | It selects and builds up to three supported capabilities. |
| “Build capability 2.” | It builds the option from the list you were shown. |
| “Use that capability on this problem…” | It applies the method, with source-backed reasoning and limits. |
| “Resume the compilation.” | It continues saved work in this project. |
| “Compare this capability against raw transcript chat.” | It prepares matched new tasks and helps assess the results. |

For example, photography transcripts might support a **Handheld Blur Reviewer** that checks focus before suggesting shutter changes. The assistant explains what it can do, what the sources do not establish, and where the resulting skill is saved. It does not promise a full photography expert from a few narrow lessons.

Once your capability is ready, send a real task or ask for a worked example. Your assistant validates and uses it for you. The resulting skill folder is portable, and its evidence travels with it.

## What you need

Use local Codex or Claude Code with permission to read files and run local tools. A local Python 3.10+ runtime is needed underneath; your assistant checks for it and helps with setup if missing. There are no additional Python packages to install for normal use.

Supply UTF-8 `.txt`, `.md`, `.vtt`, or `.srt` transcripts as accessible attachments or a folder. YouTube fetching is not implemented yet; exported transcripts work now, and original video URLs can be preserved with them.

Work stays in your local project. Your chosen AI service may still process content remotely and have subscription or usage limits. A plain web chat without local file/tool access cannot run the installed compiler autonomously, though comparison prompts can be used there.

## Built to earn its value

The goal is better repeated work than attaching transcripts and asking questions: durable methods, preserved evidence, honest scope, reconciled disagreement, and portable skills. That improvement should be measured, not assumed.

Ask for a comparison to prepare matched tasks for raw transcripts and the compiled capability. Independent fresh sessions may be needed; the assistant prepares the material and processes the answers. A tie is a valid result. [How comparisons work](docs/EVALUATION.md).

MIT licensed. Synthetic examples cover gardening, photography, and debugging. Imported source material retains its ownership and licensing.

## For contributors

[Development and tests](docs/DEVELOPING.md) · [Internal command reference](docs/CLI.md) · [Architecture](DESIGN.md) · [Conversational acceptance flows](docs/ASSISTANT-FLOWS.md)
