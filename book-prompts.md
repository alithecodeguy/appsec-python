# Prompts for writing Python for Application Security Engineers

Select **SOL 6.1** with **High** reasoning. Start with chapter 01. Copy one prompt at a time into a chat in this project. Each prompt names the files it needs, so you can start a fresh chat between chapters. If you work outside the project, attach the writing guide, the selected syllabus brief and any earlier chapter the prompt builds on.

Prompts 01–44 produce the chapters. Run 45–49 afterward so the contents, indexes and exhibit lists point to what was actually written. Each prompt saves Markdown and returns a short handoff in chat.

## Part I. First steps in Python

### 01. Your first program

```text
Use book-context.md and brief 01 in python-appsec-syllabus.md. Write the complete chapter to manuscript/chapters/01.md.
Let a beginner trace three lines on paper before installing anything. Show exactly which characters print when one word changes.
```

### 02. Set up a workbench you can rebuild

```text
Use book-context.md and brief 02 in python-appsec-syllabus.md. Write the complete chapter to manuscript/chapters/02.md.
Give separate Windows, macOS and Linux setup commands where they differ. Have the reader close the terminal and verify the same interpreter on reopening.
```

### 03. Values, names and expressions

```text
Use book-context.md and brief 03 in python-appsec-syllabus.md. Write the complete chapter to manuscript/chapters/03.md.
Trace the values and types of "0", 0 and None. Ask the reader to predict a quota decision before running it.
```

### 04. Decisions and repetition

```text
Use book-context.md and brief 04 in python-appsec-syllabus.md. Write the complete chapter to manuscript/chapters/04.md.
Build Mina's access decision step by step. Use a trace table for a visitor, a member and an unknown role.
```

## Part II. Give data a shape

### 05. Collections and shared state

```text
Use book-context.md and brief 05 in python-appsec-syllabus.md. Write the complete chapter to manuscript/chapters/05.md.
Group six notes into workspaces. Show how two users can accidentally share a mutable list and how to check the corrected result.
```

### 06. Functions, modules and interfaces

```text
Use book-context.md and brief 06 in python-appsec-syllabus.md. Write the complete chapter to manuscript/chapters/06.md.
Extract the access decision into one function. Import it from two small scripts and trace two calls with different users.
```

### 07. Text, bytes and patterns

```text
Use book-context.md and brief 07 in python-appsec-syllabus.md. Write the complete chapter to manuscript/chapters/07.md.
Reuse a Persian note title. Show its exact character and UTF-8 byte counts, then apply a documented policy to short identifiers.
```

### 08. Files and structured records

```text
Use book-context.md and brief 08 in python-appsec-syllabus.md. Write the complete chapter to manuscript/chapters/08.md.
Give the reader complete CSV and JSON fixtures, including a quoted comma, a non-English title and a missing field. Show the converted records.
```

## Part III. Write code another person can trust

### 09. Errors, debugging and cleanup

```text
Use book-context.md and brief 09 in python-appsec-syllabus.md. Write the complete chapter to manuscript/chapters/09.md.
Walk through a traceback from the last line upward. Distinguish an unreadable file from invalid JSON and show when cleanup happens.
```

### 10. Types, classes and domain models

```text
Use book-context.md and brief 10 in python-appsec-syllabus.md. Write the complete chapter to manuscript/chapters/10.md.
Build a note draft as a dataclass. Show which mistake a type checker can catch and where external input still needs a runtime check.
```

### 11. Iteration, decorators and bounded work

```text
Use book-context.md and brief 11 in python-appsec-syllabus.md. Write the complete chapter to manuscript/chapters/11.md.
Step through a generator as it reads three records. Then wrap a function with a timer and verify that its name survives.
```

### 12. Repeatable tests and a reviewable change

```text
Use book-context.md and brief 12 in python-appsec-syllabus.md. Write the complete chapter to manuscript/chapters/12.md.
Turn the quota boundary from earlier chapters into a failing pytest assertion, a small correction and a passing regression test.
```

## Part IV. Python at system boundaries

### 13. Processes, settings and secrets

```text
Use book-context.md and brief 13 in python-appsec-syllabus.md. Write the complete chapter to manuscript/chapters/13.md.
Trace how a text setting becomes a boolean. Use a fake credential and check the exact diagnostic emitted when a required setting is missing.
```

### 14. Command-line tools and child processes

```text
Use book-context.md and brief 14 in python-appsec-syllabus.md. Write the complete chapter to manuscript/chapters/14.md.
Build a note-count CLI. Give concrete examples of stdout, stderr and exit codes, including a filename with spaces and a helper timeout.
```

### 15. Relational data and transactions

```text
Use book-context.md and brief 15 in python-appsec-syllabus.md. Write the complete chapter to manuscript/chapters/15.md.
Use two SQLite workspaces and a name containing an apostrophe. Inspect the stored rows after a successful transaction and a rollback.
```

### 16. Networks, HTTP and TLS

```text
Use book-context.md and brief 16 in python-appsec-syllabus.md. Write the complete chapter to manuscript/chapters/16.md.
Annotate a recorded request and response before writing a small client. Use a fixed destination and a fake transport for the timeout case.
```

## Part V. Design a small web application

### 17. Draw the system and its trust boundaries

```text
Use book-context.md and brief 17 in python-appsec-syllabus.md. Write the complete chapter to manuscript/chapters/17.md.
Use Mermaid to trace a note across the browser, service, database and export worker. Label two trust boundaries and state how each assumption can be checked.
```

### 18. Security requirements and private data

```text
Use book-context.md and brief 18 in python-appsec-syllabus.md. Write the complete chapter to manuscript/chapters/18.md.
Turn “notes are private” into a testable requirement. Work through one retention decision with a data owner, deadline and observable deletion result.
```

### 19. Build the Casebook web service

```text
Use book-context.md and brief 19 in python-appsec-syllabus.md. Write the complete chapter to manuscript/chapters/19.md.
Build the smallest runnable Django service for the chapter. Include a health route, two seeded workspaces and a test for anonymous access.
```

### 20. API contracts and business rules

```text
Use book-context.md and brief 20 in python-appsec-syllabus.md. Write the complete chapter to manuscript/chapters/20.md.
Specify a note update contract with client-owned and server-owned fields. Show the stored state after an invalid change and a repeated request.
```

## Part VI. Identity, permissions and the browser

### 21. Accounts, passwords and recovery

```text
Use book-context.md and brief 21 in python-appsec-syllabus.md. Write the complete chapter to manuscript/chapters/21.md.
Follow one fictional account through sign-in and recovery. Use Mermaid for the recovery flow and check expiry and single use with a controlled clock.
```

### 22. Sessions, tokens and federated identity

```text
Use book-context.md and brief 22 in python-appsec-syllabus.md. Write the complete chapter to manuscript/chapters/22.md.
Use a Mermaid sequence diagram to show what the browser, application and identity provider each receive. Include local verification cases for the wrong audience and an expired token.
```

### 23. Authorization and tenant isolation

```text
Use book-context.md and brief 23 in python-appsec-syllabus.md. Write the complete chapter to manuscript/chapters/23.md.
Follow the same Alpha/Beta permission matrix through list, detail and export. Show how a membership change affects the next request.
```

### 24. Templates, cookies and the browser

```text
Use book-context.md and brief 24 in python-appsec-syllabus.md. Write the complete chapter to manuscript/chapters/24.md.
Follow one private note from Django template to browser. Compare rendering, cookie behavior, CSRF checks, CORS and CSP using the syllabus table.
```

## Part VII. Files, services and concurrent work

### 25. Uploads, archives and serialization

```text
Use book-context.md and brief 25 in python-appsec-syllabus.md. Write the complete chapter to manuscript/chapters/25.md.
Use two attachments with the same display name. Show what gets stored or cleaned up at the size boundary and after a rejected file.
```

### 26. Outbound requests and integrations

```text
Use book-context.md and brief 26 in python-appsec-syllabus.md. Write the complete chapter to manuscript/chapters/26.md.
Use a fake partner transport and stored webhook fixtures. Trace a refused redirect, an oversized response and duplicate delivery through to final state.
```

### 27. Cryptographic choices and key management

```text
Use book-context.md and brief 27 in python-appsec-syllabus.md. Write the complete chapter to manuscript/chapters/27.md.
Choose primitives for two concrete jobs: authenticate a webhook and protect a stored export. Use maintained libraries, dummy keys and a rotation example.
```

### 28. Concurrency, queues and resource limits

```text
Use book-context.md and brief 28 in python-appsec-syllabus.md. Write the complete chapter to manuscript/chapters/28.md.
Use two coordinated workers and a database constraint for the export example. Explain which guarantee comes from Python and which comes from the database.
```

## Part VIII. Review, verification and release

### 29. Review Python changes and interpret static findings

```text
Use book-context.md and brief 29 in python-appsec-syllabus.md. Write the complete chapter to manuscript/chapters/29.md.
Review a supplied Python diff and two static findings. Show how a reviewer can establish the actual code path, suggest a fix and select a regression check.
```

### 30. Verify controls in running code

```text
Use book-context.md and brief 30 in python-appsec-syllabus.md. Write the complete chapter to manuscript/chapters/30.md.
Generate workspace records with Hypothesis and test a tenant-isolation property. Compare that evidence with a passive observation and identify what neither covers.
```

### 31. Dependencies and the software supply chain

```text
Use book-context.md and brief 31 in python-appsec-syllabus.md. Write the complete chapter to manuscript/chapters/31.md.
Follow an indirect dependency from a lock record into a sample build. Use a sourced advisory or clearly labeled fictional data for the update decision.
```

### 32. CI checks and release evidence

```text
Use book-context.md and brief 32 in python-appsec-syllabus.md. Write the complete chapter to manuscript/chapters/32.md.
Trace one commit to one artifact. Work through passed, failed and missing check results and show the release decision for each.
```

## Part IX. Operate and recover a service

### 33. Security logs and audit history

```text
Use book-context.md and brief 33 in python-appsec-syllabus.md. Write the complete chapter to manuscript/chapters/33.md.
Correlate a denied export across service and worker events. Show the exact redacted audit record and the decision if recording it fails.
```

### 34. Metrics, traces and alert triage

```text
Use book-context.md and brief 34 in python-appsec-syllabus.md. Write the complete chapter to manuscript/chapters/34.md.
Calculate denial rates from two traffic volumes. Use a request ID and queue evidence to decide whether a delay calls for escalation.
```

### 35. Deployment, containers and infrastructure settings

```text
Use book-context.md and brief 35 in python-appsec-syllabus.md. Write the complete chapter to manuscript/chapters/35.md.
Review a small container and reverse-proxy configuration. Explain which checks establish runtime identity, trusted hosts and the original request scheme.
```

### 36. Incident response, disclosure and recovery

```text
Use book-context.md and brief 36 in python-appsec-syllabus.md. Write the complete chapter to manuscript/chapters/36.md.
Use a synthetic credential incident. Reconstruct a UTC timeline and give the reader concrete evidence for containment, restoration and retesting.
```

## Part X. Build tools and lead reviews

### 37. Build a Python source-review tool

```text
Use book-context.md and brief 37 in python-appsec-syllabus.md. Write the complete chapter to manuscript/chapters/37.md.
Build a small Python AST checker for local configuration files. Include the package entry point, two fixtures and an example the rule cannot decide.
```

### 38. Normalize findings and prioritize work

```text
Use book-context.md and brief 38 in python-appsec-syllabus.md. Write the complete chapter to manuscript/chapters/38.md.
Merge two saved reports while preserving their origins. Prioritize three findings using exposure and ownership, then explain a decision that severity alone would miss.
```

### 39. Cloud identity and service boundaries

```text
Use book-context.md and brief 39 in python-appsec-syllabus.md. Write the complete chapter to manuscript/chapters/39.md.
Compare the permissions of an upload worker and an export worker. Trace the lifetime of a private download grant and its implications for revocation.
```

### 40. Run an application security program

```text
Use book-context.md and brief 40 in python-appsec-syllabus.md. Write the complete chapter to manuscript/chapters/40.md.
Turn one release into a small security program. Give owners, evidence, review dates and a worked risk-acceptance decision written for a product manager.
```

## Part XI. Capstone. A private workspace export

### 41. Capstone I. Define a private export

```text
Use book-context.md and brief 41 in python-appsec-syllabus.md. Write the complete chapter to manuscript/chapters/41.md.
Write the learner's private-export brief, then a worked design. Use the two workspaces to decide who can request, collect and expire an export.
```

### 42. Capstone II. Implement the controls

```text
Use book-context.md and brief 42 in python-appsec-syllabus.md. Write the complete chapter to manuscript/chapters/42.md.
Build on chapter 41. Implement the export in runnable increments and verify isolation, revocation, expiry and duplicate delivery against stored state.
```

### 43. Capstone III. Review and release

```text
Use book-context.md and brief 43 in python-appsec-syllabus.md. Write the complete chapter to manuscript/chapters/43.md.
Use the chapter 42 implementation as the release candidate. Trace each mandatory control to actual or clearly labeled example evidence and justify a release decision.
```

### 44. Capstone IV. Operate, respond and hand over

```text
Use book-context.md and brief 44 in python-appsec-syllabus.md. Write the complete chapter to manuscript/chapters/44.md.
Continue from chapter 43. Work through a retention incident, recovery checks and a handover that a second engineer could follow.
```

## Complete the manuscript

### 45. Appendices A–D

```text
Use book-context.md and the four appendix briefs in python-appsec-syllabus.md. Read the relevant completed examples and exercises. Write manuscript/appendices.md with four sections: the membership rule in three forms, a Python reference shelf, a lab notebook with a worked answer and links to the chapter solutions, and a standards-to-evidence map. Use actual chapter links and verified standard identifiers.
```

### 46. Glossary, subject index and Python index

```text
Use book-context.md and the completed chapter headings, examples and appendices. Write manuscript/indexes.md with an alphabetical plain-English glossary, a subject index and a separate Python API and tools index. Use the syllabus indexes as seeds. Link entries to sections that actually teach the term. Check the relative links.
```

### 47. Bibliography and edition notes

```text
Use book-context.md and the references actually cited in manuscript/chapters and manuscript/appendices.md. Write manuscript/references.md. Group primary sources by subject, consolidate duplicate links and distinguish the edition baseline from the versions actually used for examples. Flag any source or version you cannot verify in the chat handoff.
```

### 48. Cover text, preface and contents

```text
Use book-context.md, the syllabus and the finished manuscript. Write manuscript/README.md as the book's entry point. Include the title and edition, preface, beginner and experienced-reader routes, a short introduction to each part, linked contents in reading order, and lists of the figures, tables and listings that actually appear. Link to the chapters, appendices, indexes and bibliography. Use plain Markdown and chapter or section links for locators.
```

### 49. Final content review

```text
Use book-context.md and python-appsec-syllabus.md to review the completed Markdown manuscript. Check the 44 chapters against their briefs, follow the access rule from chapter 04 through the capstone, and verify exercise answers, exhibit references, Mermaid syntax and internal links. Check runnable listings where possible and prioritize examples changed by a correction. Fix concrete errors in the manuscript files. Report the changes and any unresolved verification gaps briefly in chat.
```
