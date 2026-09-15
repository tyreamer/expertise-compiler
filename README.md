# Expertise Compiler

**Compile human expertise into reusable building blocks for AI.** Expertise Compiler turns trusted content into structured, source-backed knowledge, reasoning patterns and methods that can be rebuilt for different goals. The durable expertise representation is the asset; a skill, reviewer, lesson or workflow is one way to use it.

Built primarily for AI engineers, developers, architects, consultants, agencies, creators and teams building AI workflows. **Digital person platforms package the person. Expertise Compiler packages reusable pieces of the expertise.** You can use a person's reasoning without recreating their personality.

**One corpus, multiple independent builds, preserved evidence.** [Product north star](NORTH_STAR.md) · [Architecture and current limits](DESIGN.md)

**You don't need to know what to build.** Give Expertise Compiler content you think is valuable. It examines the knowledge, methods, judgment, procedures, examples and criteria inside, then shows the strongest supported things that material can become.

The current conversational interface is a Codex/Claude Code skill that runs the local compiler. Install that interface, then tell your AI:

> Here are some transcripts I think are valuable. I don't know what I want to build. Save them and show me the most useful things they could become. Recommend what to build first.

Or bring a task you already have:

> Save these as Leadership. Use them to review this message before I send it to my team.

Or point it at a folder:

> Use the transcripts in ./input to review my plan in ./plan.md. Preserve my original and save an improved version with the reasons for your changes.

With a goal, your assistant applies supported methods and produces the useful result: a draft, review, decision analysis, plan, guided procedure, lesson or source-backed answer. Without a goal, it produces a concise, ranked **Capability Map**. You do not choose compiler stages, intent labels or asset types. **“Just save for later”** remains a valid path and does not force discovery.

## See what your content can become

A Capability Map explains each opportunity's problem, input, transformation, output, source support, repeat-use value and limits. It assesses whether a reusable method adds value beyond ordinary transcript Q&A. A fact-heavy collection may support reference and learning while lacking the procedures needed for a reliable reviewer.

```text
Your transcript collection
          ↓
Durable expertise + source evidence
          ↓
Capability Map: strongest supported opportunities
          ↓
“Build #2”
          ↓
Ready-to-use method with evidence and an example
```

For example, our small synthetic photography fixture supports a **Portrait Troubleshooting Guide** and **Portrait Critic** for focus and motion blur. It does not establish a lighting coach or general visual evaluator. Sales and architecture fixtures use the same discovery logic, with different evidence. These are authored examples, not live effectiveness benchmarks. [Fixture examples and validation limits](fixtures/opportunities/README.md).

Choose the useful capability first. The compiler carries its evidence, boundaries and input/output contract directly into the build. Text methods are available now; skill export is optional. Other runtime formats are marked as future possibilities, never presented as delivered agents or services.

Maps are saved against source, knowledge, compiler and discovery versions. Ask **“What changed in the Capability Map after adding these sources?”** to compare new opportunities, changed support and disagreements. Earlier maps remain inspectable. The map is a replaceable interpretation; it never overwrites the underlying expertise.

## Why this exists

Transcripts are information. Expertise Compiler turns their methods, procedures, examples, disagreements, and limitations into capabilities you can use again.

The most valuable output is work you can act on. A collection about a subject can support writing, critique, decisions, guided work or learning when its sources provide sufficient methods. Underneath the result is a reusable method with traceable evidence, clear limits and preserved disagreements. Source statements stay distinct from AI inference and private context. The archive can support tomorrow's different goal without starting from scratch.

```text
Source collection → durable expertise IR → Capability Map (if exploring)
                                              ↓
                                   selected / user build intent
                                              ↓
                              select / extend relevant expertise
                                              ↓
                                  compiled method / capability
                                              ↓
                                        target artifact
                                              ↓
                                      validate / evaluate
                                              ↓
                                        portable output
```

**No model API key. No hosted compiler service. Your existing AI does the reasoning.** The underlying knowledge remains yours to inspect and reuse beyond a single skill.

The long-term model supports independent builds such as decision frameworks, interview-questioning methods, style profiles that exclude opinions, reviewers, coaches and evaluation suites from the same collection. The target taxonomy is open. Today the implementation provides eight goal contracts, structured text results and optional Agent Skills export; it does not yet implement arbitrary target plugins or enforce expertise-component exclusions as structured policy.

## Use the current skill interface

### Codex

Send Codex this message:

> Use $skill-installer to install the repository root at https://github.com/tyreamer/expertise-compiler as a personal skill named expertise-compiler, including its supporting files.

Codex's installer supports skills from other repositories. Restart Codex if the skill does not appear after installation. [Official installation guidance](https://learn.chatgpt.com/docs/build-skills).

### Claude Code

Send Claude Code this message:

> Install https://github.com/tyreamer/expertise-compiler as my personal expertise-compiler skill. Download and review the repository, then use its bundled installer to copy the complete skill to ~/.claude/skills/expertise-compiler. Preserve any existing installation.

Claude Code discovers personal skills in that folder and can invoke them from matching natural-language requests. [Official skill guidance](https://code.claude.com/docs/en/skills).

The assistant handles downloading and copying; you do not need to clone the repository or manually load SKILL.md. Your environment may ask for file-access permission. [Installation details and troubleshooting](docs/INSTALLATION.md).

## Start with your actual work

Bring material you trust and explain what you want to accomplish. You do not need to know which capability or output format to choose.

> Save these transcripts as Client Onboarding. I'm preparing a handoff for a new team member. Use the training to review my draft in ./handoff.md for missing steps and unclear responsibilities. A useful result would be an improved handoff with the reasons for each change. Flag anything the training doesn't establish.

In your own words, tell the assistant what you're working on, provide the relevant material or draft, and describe what would make the result useful. Include constraints or exclusions when they matter. These are conversational details, not required form fields; the assistant should use the context already available and ask only for missing information that affects the work.

If you don't have a task yet, supplying valuable content is enough: the assistant discovers supported opportunities. You can also simply ask it to save the sources for later without producing an output.

The assistant should deliver usable work, explain its evidence and limits, and save the underlying expertise for reuse. Tomorrow, reopen the same project and describe a different task using that named collection. You shouldn't have to reattach the sources or commit to the first output format. Ask for a skill export only when you need one.

**Trying the alpha?** Follow the [testing guide](docs/testing-guide.md) to test a real task, reuse your collection and compare the effort with ordinary transcript chat.

## Saved locally, reusable later

Your project's `.expertise-compiler/library.json` maps readable collection names to stable IDs. Collections preserve original files, source metadata, normalized segments, extraction notes, knowledge revisions, private briefs and immutable completed builds. Each result is bound to its sources, knowledge, brief, method, output target and compiler fingerprint. Interrupted work resumes from saved checkpoints. Existing runs can be adopted without modifying their original folders.

Ask **“What collections do I have?”**, **“What's in Leadership?”**, or **“What changed after adding these sources?”** You can add, replace or remove sources, compare revisions, archive collections and restore them later. Removal changes the active revision; historical sources and results remain available. A new goal, source revision or knowledge revision produces a new build when its content changes. Opening the same project in a new session gives the assistant access to its saved collections; collections are not automatically available in unrelated projects or globally installed.

The collection is not a skill, the skill is not the IR, and the result is not the method. New results save a readable method and relevant evidence underneath. No skill package is created until you ask to export it. “Just save for later” stores originals without claiming knowledge extraction; “Save these as Leadership” also prepares knowledge, and the assistant reports exactly what completed.

Ordinary skill exports contain selected knowledge and relevant quotations. They exclude full raw transcripts, unrelated source documents and private briefs/work products. The full audit material stays in the collection. Exporting locally does not publish or globally install anything, and citations do not establish permission to share. Ask your assistant explicitly when you want to export or install a method.

## What you need

Use local Codex or Claude Code with permission to read files and run local tools. A local Python 3.10+ runtime is needed underneath; your assistant checks for it and helps with setup if missing. There are no additional Python packages to install for normal use.

Supply UTF-8 `.txt`, `.md`, `.vtt`, or `.srt` transcripts as accessible attachments or a folder. YouTube fetching is not implemented yet; exported transcripts work now, and original video URLs can be preserved with them.

Work stays in your local project. Your chosen AI service may still process content remotely and have subscription or usage limits. A plain web chat without local file/tool access cannot run the installed compiler autonomously, though comparison prompts can be used there.

## Built to earn its value

The long-term value is faithful decomposition of expertise, conditions and exceptions, preserved disagreements, evidence, corrections, reuse and testing behavior across builds. Ingestion and asset generation alone are not the differentiation. The next quality direction is to let users correct an interpretation once and carry that correction into future builds and regression tests; that correction loop is not implemented yet.

Ask for a comparison with the same sources, goal, constraints and access to persistent context. Measure quality, corrections, setup, reuse and update effort. Comparable quality with substantially less repeated effort can be valuable. No live effectiveness result is claimed. Passing package validation proves integrity and evidence linkage, not sound judgment or superiority. [How comparisons work](docs/EVALUATION.md).

MIT licensed. Synthetic acceptance fixtures cover comedy, photography, business, debugging, architecture and education, using the same compiler logic. Earlier gardening fixtures remain. Imported source material retains its ownership and licensing. No broad live assistant effectiveness result is claimed.

## For contributors

[Development and tests](docs/DEVELOPING.md) · [Internal command reference](docs/CLI.md) · [Architecture](DESIGN.md) · [Conversational acceptance flows](docs/ASSISTANT-FLOWS.md)

[First live cross-domain test](docs/UNIVERSAL-ACCEPTANCE.md)
