# Writing guide for Python for Application Security Engineers

Use the selected chapter brief in [the syllabus](python-appsec-syllabus.md) and its prompt in [the prompt pack](book-prompts.md). The brief supplies the goal, four sections, two worked examples and a practice check. Read earlier manuscript sections only when the current example builds on their code or decisions.

## Reader and language

Write for someone who may be learning both programming and technical English. Begin with a question the reader can answer by the end. Use short sentences, familiar verbs and consistent names. Define each technical term when it first matters. Preserve the exact spelling of commands, APIs and error messages.

For example, Mina signs in successfully and then tries to open a Beta note. Signing in establishes who Mina is (**authentication**). The service still has to decide whether she may read this particular note (**authorization**).

## Edition and running project

- The tested language baseline is **CPython 3.12.14**. Web examples use **Django 6.1.3** on that interpreter. Use the exact tested packages in [requirements-tested.txt](requirements-tested.txt) and the commands/results in [tested-versions.md](tested-versions.md). Record exact versions and the boundary actually exercised; a passing local test does not establish browser or deployment behavior.
- Casebook stores private team notes. Mina belongs to Alpha, Ravi belongs to Beta and Lee manages Alpha. A visitor is anonymous. Use fictional records, including a non-English title when encoding matters.
- A reader must be an active member of the note's workspace at the time of a read. Lee manages only Alpha. A background export checks current permission again before it releases private data. Chapters 41–44 build and verify this feature.
- Begin with standalone Python. Introduce pytest in chapter 12, SQLite in 15, Django in 19 and a background worker in 28. Early examples may use a set of memberships. Later service examples load memberships from trusted records.
- Reuse established file paths, function signatures and fixtures. When an example depends on earlier work, give the chapter, filename and smallest starting state needed to follow it.

## What belongs in a chapter

1. Open with the practical question, prerequisites and learning outcomes. Introduce syntax before asking the reader to use it.
2. Teach all four sections and develop both examples from the brief. Start with the smallest useful input. Ask for a prediction, show the result and explain the line or decision that produced it. Include a boundary or failure that changes the outcome.
3. Make listings copyable. Supply imports, filenames, fixture data, the run command and expected output. For design chapters, give an equally concrete artifact such as a permission matrix with filled-in decisions.
4. Give a guided lab and independent practice. End the practice with the syllabus checkpoint. Put hints and worked answers after the exercises. Explain why the answer works and how the reader can check it.
5. Close with a short recap and primary sources for consequential technical claims. Use stable exhibit IDs from the syllabus where assigned. Caption additional exhibits with unique chapter-based IDs, such as F23-01.

## Evidence and diagrams

Run examples when the environment supports them. Report what ran, the exact runtime and any untested listing in the chat handoff. In the manuscript, distinguish expected output from a recorded result. Use local code, synthetic data and recorded reports for security exercises. For permissions, show both a permitted reader and a reader from another workspace. For a failed write or a retried job, inspect the final stored state.

Write all drafts as ordinary Markdown. Use fenced `mermaid` blocks when a diagram helps the reader follow a branch, trust boundary or sequence. Give the diagram a caption and explain what to notice. Use a Markdown table for exact mappings. A4 page size and monospace typography belong to the final PDF stage.

## Saving a draft

Save chapter NN as `manuscript/chapters/NN.md`, using its two-digit number and exact syllabus title in the heading. Create the parent directory when needed. Keep runnable listings in the Markdown so each draft can be used on its own. In chat, report the saved path, any verification gap and the starting state the next chapter needs. Keep the handoff brief.
