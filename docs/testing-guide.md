# Expertise Compiler: alpha testing guide

Bring material you trust. You don't need to know what to build: Expertise Compiler should show you its strongest supported opportunities, then build one you choose. If you already have a task, bring it too. The underlying expertise, evidence and methods should remain reusable for future work.

We're testing whether that saves effort and improves your work compared with attaching transcripts to an ordinary AI conversation. We haven't established that advantage yet. Honest failures and reasons you wouldn't use it again are especially useful feedback.

## Before you start

For the capture-first pilot, use the [iPhone Shortcut live test](iphone-shortcut.md#exact-first-live-test-from-your-iphone). It separately measures saving, sync and import before asking for processing. A URL-only capture is expected to remain unavailable for content-based work; that is different from a failed save. The rest of this guide tests discovery and useful outcomes once enough content is actually available.

Use local Codex or Claude Code with access to your project files and local tools. Follow the [installation instructions](../README.md#use-the-current-skill-interface); your assistant should handle setup, including checking Python 3.10+. You should not need to run compiler commands or edit JSON. If you already have an installation, ask the facilitator to verify its version before testing; the installer preserves differing existing installations instead of silently updating them.

Choose one project folder and keep using it throughout the test. Start with a small collection, such as 2–5 transcripts, so you can judge whether the assistant interpreted them correctly. This is a suggested pilot size, not a product limit. Supply UTF-8 `.txt`, `.md`, `.vtt` or `.srt` files. Links and playlists alone won't work yet; neither will raw audio, video, PDFs or slide decks. Ask the facilitator for help preparing text and include that preparation time in your feedback.

Use material you are authorized to process. For client or internal content, follow your organization's rules and redact where needed. Files are stored locally, but your chosen AI service may process their contents remotely. A plain web chat without local file and tool access cannot run this compiler autonomously.

## 1. Discover what your content can become

For the discovery test, give a normal user this exact prompt with their transcript files:

> Use Expertise Compiler with these transcripts. I think this material is valuable, but I don't know what I want to build. Save it as My Test Collection, show me the strongest things it could become, and recommend what to build first. Explain what I would give each one, what I would get back, and the important limits.

Check whether the ranked Capability Map helps you understand useful possibilities without having to choose technical formats. Does it explain why the sources support each opportunity? Are the ideas distinct and realistic, or attractive names for unsupported promises? A narrow map or an honest gap is better than five invented agents.

Reply **“Build #2”** (or name the opportunity you prefer). The assistant should build that saved opportunity directly, without asking you to translate it into an artifact type or resupply the sources. A reusable reviewer can be built before you supply a specific draft to review. Then try the finished method on real work and judge that result too.

If you already have a goal, you can bypass discovery:

Tell your assistant what you're trying to accomplish and what a useful result would look like. For example:

> Use Expertise Compiler to save these transcripts as Client Onboarding. I'm preparing a handoff for a new team member. Use the training to review my draft in ./handoff.md for missing steps and unclear responsibilities. Give me an improved handoff with reasons for the changes. Flag anything the training doesn't establish.

Use your own words. Share relevant context, a draft or decision if you have one, and any constraints or things to exclude. You don't need to pick a capability type or know compiler terminology. The assistant should ask focused questions only when it needs more information.

Some starting points for different kinds of work:

| Your work | A possible real task |
| --- | --- |
| Building with AI | Apply tutorial methods to review a design you're implementing; optionally export the method as a skill afterward. |
| Consulting or agency work | Use training content to improve an actual client handoff or SOP. |
| Creating or teaching | Use your own course transcripts to develop a lesson and exercise for a specific audience. |
| Knowledge-heavy professional work | Apply trusted training to a decision, plan or work product you already need to complete. |

These are examples, not a menu or guaranteed outcomes. The assistant should explain when your sources don't support the requested work. Current outputs include structured text results and optional skill exports; standalone agent exports and persistent coaching services are not available.

## 2. Check the first result

Read the actual deliverable, not just the completion message. Would you use it? What would you have to change first?

Check at least two important conclusions against their cited passages. Look for missing conditions, exceptions or disagreements. Can you tell what the source said from what the assistant inferred? If something is wrong, record the original result, the cited evidence and your correction. Corrections can be discussed in the session, but automatic correction propagation across future builds is not implemented yet.

The assistant should link to saved work and explain what was validated. A passing validator checks structure and evidence references; it does not prove the interpretation is correct or the result is useful.

## 3. Come back with different work

Start a fresh assistant session in the **same project folder**. Name the saved collection and describe a different goal. For example, use the onboarding training to create a new starter's first-week checklist after reviewing the handoff.

Don't reattach the original transcripts. Check whether the assistant finds the collection, reuses its expertise and produces the new result. It may need to read archived sources again for knowledge the first task didn't require. That is different from asking you to upload everything again.

Record any repeated explanation, missing context or manual help. Collections are project-local; opening an unrelated project is not expected to find them automatically.

## 4. Change the source material

Add one relevant transcript, or supply a revised file and explicitly ask to replace its earlier version. Ask what changed and rerun an affected task.

Check whether the new result accounts for the change and whether the earlier result remains available. Also ask “What changed in the Capability Map after adding these sources?” Check the explanation against the material: new support, weakened ideas and disagreements should remain visible, and the earlier map should remain available. If no relevant conclusion should change, saying so is a valid outcome. Record stale advice, lost history or repeated setup work.

## 5. Compare with ordinary transcript chat

Use a separate conversation with the same model where practical. Give it the same complete sources, real task, constraints and requested result, but don't give it the compiler's extracted knowledge, method or answer. Let both approaches retain their own saved context for later tasks. Don't make the baseline start from scratch each time while allowing only the compiler to remember.

Repeat the different-goal and source-update tasks in both approaches. Record initial setup and preparation separately from later effort. If possible, have someone review the answers without knowing which approach produced them. A small pilot provides observations, not proof of general superiority.

| Compare | What to record |
| --- | --- |
| Usability | Setup problems, questions you couldn't answer, facilitator help required |
| Useful work | Whether you'd use the result and the edits still needed |
| Faithfulness | Unsupported statements, missed conditions, lost disagreements, incorrect citations |
| Effort | Approximate minutes and corrections for first use, reuse and updates in each approach |
| Return value | Whether you'd bring another task or collection, and why |

The [evaluation protocol](EVALUATION.md) has more detail if you want a structured comparison. Ask the assistant to handle its mechanics.

## Share your feedback

Send this short report to the person who invited you. You can omit confidential material; include sanitized examples only when permitted. Don't upload your whole `.expertise-compiler` folder—it contains original content and private work.

```text
Assistant/client and model:
Compiler version or commit (ask the facilitator if unknown):
Material: domain, file count, approximate length:
My initial goal, if any, and what success meant:
Capability Map: useful opportunities? Unsupported suggestions? Clear inputs/outputs?
Selected opportunity: did it build directly without an asset-type question?
Setup/preparation effort and help needed:
First result: usable / usable after edits / not usable, because:
One interpretation or evidence problem, if any:
Fresh-session second task: found the collection? Re-upload needed?
Source update: reflected correctly? Earlier result and map still available?
Comparison with ordinary chat: better / similar / worse / not run:
Approximate effort for each approach: first task / second task / update:
Would I use this again for actual work? Why or why not?
Biggest friction or missing capability:
```

If a step fails, save the error or a sanitized excerpt and tell the facilitator. Don't spend the session debugging internals. An unfinished test still gives us useful evidence.

## For the facilitator

Start with one tester from each group, then expand after addressing recurring blockers. Verify a fresh installation and a complete live run in each supported client before presenting setup as reliable. Record the tested commit and model; automated fixture tests don't certify live assistant behavior. Use the [acceptance protocol](UNIVERSAL-ACCEPTANCE.md) for detailed checks.

Observe before helping and record every intervention. A facilitator-rescued run is not an independent success. Collect first-use, reuse and update results separately, and don't infer market demand from package validation or polite feedback. The strongest signal is that someone completes meaningful work and voluntarily returns with another task because the saved expertise makes it easier.
