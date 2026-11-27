# Python for Application Security Engineers

**From your first Python program to the security review of a running service**

By **AliTheCodeGuy**

**Edition:** 27 November 2026 · **CPython 3.12.14** · **Django 6.1.3**

[Preface](#preface) · [Choose a reading route](#choose-a-reading-route) · [Contents](#contents) · [Figures](#list-of-figures) · [Tables](#list-of-tables) · [Listings](#list-of-listings) · [Back matter](#back-matter)

## Preface

A private note belongs to Alpha. Mina can read it today. If Lee removes her membership while an export waits in a queue, may that export still release the note tomorrow? What would count as evidence that the answer is correct?

This book teaches Python through those questions. Application security, or **AppSec**, means making software protect the people and data that depend on it. You will start with text and a few instructions, then learn to turn a rule into code, a test, a design decision and an operational check. You do not need previous programming experience to begin chapter 01.

The running project is **Casebook**, a service for private team notes. Mina belongs to **Alpha**. Ravi belongs to **Beta**. Lee manages **Alpha only**. An anonymous visitor has no account. The names, notes, credentials, partner events and incidents are fictional. A reader needs current active membership in the note's stored workspace at the time of a read. Manager status does not cross a workspace boundary. A stored export also needs the correct requester and current release authority.

The examples develop that rule in stages. An early pure function receives supplied facts; a later service loads trusted account and membership records. Some chapters use separate small laboratories rather than extending one installed application. Keep the filenames, starting state and working directory named by each chapter. Passing a value such as `user_id=1` in a fixture is not a replacement for browser authentication.

Read each example with a prediction. Write down the input, expected result and final state; run the stated command; then explain the line or boundary that determined the result. For a refused write, retry or cleanup failure, inspect what remains in storage. Try the independent practice before following the worked answer. The [lab notebook and solution directory](appendices.md#appendix-c-lab-notebook-and-answer-key) gives a repeatable way to keep that evidence.

The prose uses short explanations and keeps API names in their original spelling. If English is a second language, explain an example in your own words and keep the exact English term beside your translation. Use the [glossary](indexes.md#glossary) when a word is new, the [subject index](indexes.md#subject-index) for a security question, and the [Python API and tools index](indexes.md#python-api-and-tools-index) for a code name.

## Choose a reading route

| Reader | Route | Check before moving on |
| --- | --- | --- |
| First program, or little confidence with code | Read chapters [01](chapters/01.md)–[12](chapters/12.md) in order. Chapter 01 can be traced on paper; [02](chapters/02.md) sets up the interpreter. Continue through Parts IV–XI. | [Trace three access decisions](chapters/04.md#practice-check-print-three-decisions), [convert the two file fixtures](chapters/08.md#practice-check-preserve-and-explain), then [produce a correction with a repeatable test](chapters/12.md#practice-check-submit-a-quota-regression-diff). |
| Experienced in another language | Try the checkpoints in [04](chapters/04.md), [08](chapters/08.md) and [12](chapters/12.md). Use [05](chapters/05.md)–[11](chapters/11.md) for missed Python details, then continue at [13](chapters/13.md). | Explain truth values, aliasing, mutable defaults, imports, text/bytes and exception cleanup. A familiar syntax is not evidence that these decisions match your first language. |
| Comfortable with Python, new to AppSec | Start at [13](chapters/13.md). Read the design in [17](chapters/17.md)–[18](chapters/18.md) before the service and controls in [19](chapters/19.md)–[28](chapters/28.md). Continue through verification, operations and the capstone. | Trace one identity and one private object across each boundary. State where current membership, limits and release authority are checked. |
| Already reviewing Python services | Use the [subject index](indexes.md#subject-index), [verification chapter](chapters/30.md) and [standards map](appendices.md#appendix-d-standards-and-verification-map) to locate a question. Attempt [41](chapters/41.md#the-learners-private-export-brief) before reading the worked capstone. | Check the exact implementation/report subject and its limits. Use the preceding chapters when a capstone dependency or assumption is unfamiliar. |

For self-study, use a chapter as two sessions: first understand and predict; then rebuild or change one case and check it independently. A design chapter produces a concrete matrix, diagram or decision record instead of requiring a running server. Each part's last chapter has a checkpoint. The capstone asks for a complete evidence handover rather than a claim based on a green test total.

## Before running the examples

Use the [tested versions and reproduction guide](../tested-versions.md) and [pinned learning requirements](../requirements-tested.txt). Chapter 02 explains interpreter selection and virtual environments. Follow the chapter's command location; separate Django settings laboratories need separate Python processes. A paid cloud account is not required for the policy/model exercises.

The verification records distinguish executed local checks from authored inputs, expected procedures and untested environments. Browser-engine enforcement, hosted identity exchange, provider permissions and production key/storage controls need their own evidence. The capstone's local tests pass, while its [production decision remains HOLD](chapters/43.md#apply-the-mandatory-gates-without-averaging-them) for the controls named in that review. Treat the examples as learning services with synthetic data.

## Contents

Read the chapters below in this order unless you have used the route checks above. Each part introduces the result you will build or inspect; each link uses the title in the completed chapter.

### Part I. First steps in Python

Begin with a short program and a prediction. Learn what runs the file, how names refer to values, and how branches and loops turn facts into decisions. Finish by tracing an allowed member, another workspace and an anonymous visitor.

- [01. Your first program](chapters/01.md)
- [02. Set up a workbench you can rebuild](chapters/02.md)
- [03. Values, names and expressions](chapters/03.md)
- [04. Decisions and repetition](chapters/04.md)

### Part II. Give data a shape

Choose collections, separate reusable functions from printing, and follow text across an encoding boundary. Read CSV and JSON into one checked record shape. Shared mutable objects, missing fields and byte limits become observable behavior rather than surprising output.

- [05. Collections and shared state](chapters/05.md)
- [06. Functions, modules and interfaces](chapters/06.md)
- [07. Text, bytes and patterns](chapters/07.md)
- [08. Files and structured records](chapters/08.md)

### Part III. Write code another person can trust

Read errors, give cleanup an owner, model data and consume streams within clear budgets. Then turn a product rule into a failing test, correct it and retain the regression. This part ends with a focused change another reader can inspect.

- [09. Errors, debugging and cleanup](chapters/09.md)
- [10. Types, classes and domain models](chapters/10.md)
- [11. Iteration, decorators and bounded work](chapters/11.md)
- [12. Repeatable tests and a reviewable change](chapters/12.md)

### Part IV. Python at system boundaries

Take Python across process, configuration, command-line, database and network boundaries. Separate strings from settings, arguments from shell syntax, SQL values from identifiers, and transport protection from permission. Inspect exit codes, stored rows and bounded response handling.

- [13. Processes, settings and secrets](chapters/13.md)
- [14. Command-line tools and child processes](chapters/14.md)
- [15. Relational data and transactions](chapters/15.md)
- [16. Networks, HTTP and TLS](chapters/16.md)

### Part V. Design a small web application

Draw the private-data paths and assign each check to an owner before adding web routes. Turn privacy and retention into testable requirements. Build the smallest Django service, then specify accepted fields, state changes, failures and repeated API operations.

- [17. Draw the system and its trust boundaries](chapters/17.md)
- [18. Security requirements and private data](chapters/18.md)
- [19. Build the Casebook web service](chapters/19.md)
- [20. API contracts and business rules](chapters/20.md)

### Part VI. Identity, permissions and the browser

Follow Mina through password verification, recovery, sessions and token validation. Carry the same Alpha/Beta matrix through each private read. Follow a note from template to response, and separate rendering, cookies, CSRF, CORS and CSP by what each actually controls.

- [21. Accounts, passwords and recovery](chapters/21.md)
- [22. Sessions, tokens and federated identity](chapters/22.md)
- [23. Authorization and tenant isolation](chapters/23.md)
- [24. Templates, cookies and the browser](chapters/24.md)

### Part VII. Files, services and concurrent work

Accept attachments under bounded content/storage rules, and treat partner requests and webhook deliveries as separate trust decisions. Choose cryptographic operations for named jobs. Coordinate workers and use database constraints to preserve one committed effect despite retries or overlapping work.

- [25. Uploads, archives and serialization](chapters/25.md)
- [26. Outbound requests and integrations](chapters/26.md)
- [27. Cryptographic choices and key management](chapters/27.md)
- [28. Concurrency, queues and resource limits](chapters/28.md)

### Part VIII. Review, verification and release

Trace a change from input to data use, interpret findings and check the claim at the right boundary. Use integration and generated tests, inspect installed dependencies, and bind required checks to the artifact being considered. Missing evidence stays visible at the release gate.

- [29. Review Python changes and interpret static findings](chapters/29.md)
- [30. Verify controls in running code](chapters/30.md)
- [31. Dependencies and the software supply chain](chapters/31.md)
- [32. CI checks and release evidence](chapters/32.md)

### Part IX. Operate and recover a service

Record useful audit facts without copying private content. Interpret rates, traces and alerts with their populations and limits. Review deployment authority, then preserve evidence, contain an incident and verify that recovery restores the intended protections.

- [33. Security logs and audit history](chapters/33.md)
- [34. Metrics, traces and alert triage](chapters/34.md)
- [35. Deployment, containers and infrastructure settings](chapters/35.md)
- [36. Incident response, disclosure and recovery](chapters/36.md)

### Part X. Build tools and lead reviews

Package a small source-review tool and explain what its syntax rule can and cannot establish. Normalize findings without losing their origins, separate workload authority from requester authority, and give requirements, risk decisions and improvement work clear owners.

- [37. Build a Python source-review tool](chapters/37.md)
- [38. Normalize findings and prioritize work](chapters/38.md)
- [39. Cloud identity and service boundaries](chapters/39.md)
- [40. Run an application security program](chapters/40.md)

### Part XI. Capstone. A private workspace export

Attempt the export brief before reading the worked design. Implement request, worker, collection and expiry controls; test current permission, duplicate delivery and final state. Review the actual candidate, then rehearse a retention incident and a handover another engineer can repeat.

- [41. Capstone I. Define a private export](chapters/41.md)
- [42. Capstone II. Implement the controls](chapters/42.md)
- [43. Capstone III. Review and release](chapters/43.md)
- [44. Capstone IV. Operate, respond and hand over](chapters/44.md)

### Back matter

- [Appendix A. A small rule, three ways to read it](appendices.md#appendix-a-a-small-rule-three-ways-to-read-it) — comparison, named function and a check after changed facts.
- [Appendix B. A reference shelf for Python](appendices.md#appendix-b-a-reference-shelf-for-python) — find the language, API or tool explanation by the task.
- [Appendix C. Lab notebook and answer key](appendices.md#appendix-c-lab-notebook-and-answer-key) — a worked stored-revocation run and links to all chapter solutions.
- [Appendix D. Standards and verification map](appendices.md#appendix-d-standards-and-verification-map) — versioned standard identifiers, controls and bounded evidence.
- [Glossary](indexes.md#glossary) — alphabetical plain-English meanings.
- [Subject index](indexes.md#subject-index) — security and engineering topics across the book.
- [Python API and tools index](indexes.md#python-api-and-tools-index) — exact code and tool names.
- [Bibliography and edition records](references.md) — primary sources grouped by subject and the versions used for examples.

## Using the exhibit lists

The directories below are taken from the **completed chapters and appendices**, in reading order. They do not repeat the syllabus's planned exhibits. Existing captions and IDs are preserved. Locators open an existing chapter section; they are not page numbers or invented caption anchors.

The figure list covers the captioned diagrams. The table list includes every Markdown table in those chapters and appendices, including unnumbered practice/glossary tables and exhibits labeled `D…`. An unnumbered row uses its existing section and first column headings to identify the table. The listing list covers captioned listings, labeled code/data exhibits, fixtures, results and complete named file blocks. Short inline fragments, run commands and expected-output blocks stay with their parent section rather than receiving invented listing numbers. Navigation tables in this entry point, the indexes and the bibliography are not cataloged as teaching exhibits.

## List of figures

15 entries in chapter and appendix order.

| ID or form | Caption, section or file | Locator |
| --- | --- | --- |
| Figure F01 | How the shell reaches a saved script | [Chapter 02 · Follow a command to the script it runs](chapters/02.md#follow-a-command-to-the-script-it-runs) |
| Figure F02 | The path of a note through Casebook's trust boundaries | [Chapter 17 · 2. Data-flow diagrams and trust boundaries](chapters/17.md#2-data-flow-diagrams-and-trust-boundaries) |
| Figure F17-01 | A private-note read with an authorization branch | [Chapter 17 · Worked example 1: follow one browser read](chapters/17.md#worked-example-1-follow-one-browser-read) |
| Figure F17-02 | Recheck authority after the job has waited | [Chapter 17 · Worked example 2: move an export to a worker](chapters/17.md#worked-example-2-move-an-export-to-a-worker) |
| Figure F19-01 | Request handling with a route decision | [Chapter 19 · 2. Request and response objects, middleware order and validation points](chapters/19.md#2-request-and-response-objects-middleware-order-and-validation-points) |
| Figure F21-01 | Proposed recovery flow, including controls still awaiting integration | [Chapter 21 · Draw the whole recovery path](chapters/21.md#draw-the-whole-recovery-path) |
| Figure F03 | The separate browser, application and identity provider in sign-in | [Chapter 22 · Follow what each component receives](chapters/22.md#follow-what-each-component-receives) |
| Figure F04 | A queued export with a permission change before delivery | [Chapter 28 · Permission can change while work waits](chapters/28.md#permission-can-change-while-work-waits) |
| Figure F05 | The path from reviewed commit to deployed artifact | [Chapter 32 · Build once and test that artifact](chapters/32.md#build-once-and-test-that-artifact) |
| Figure F33-01 | Local recording and collector delivery have separate failure boundaries | [Chapter 33 · 4. Delivery failures, buffering, monitoring and audit integrity](chapters/33.md#4-delivery-failures-buffering-monitoring-and-audit-integrity) |
| Figure F35-01 | The boundaries that make the scheme claim meaningful | [Chapter 35 · Starting state and scope](chapters/35.md#starting-state-and-scope) |
| Figure F06 | The events that establish the recovery timeline | [Chapter 36 · Worked example 1: three redacted records become a UTC timeline](chapters/36.md#worked-example-1-three-redacted-records-become-a-utc-timeline) |
| Figure F39-01 | Separate admission, queues and worker destinations | [Chapter 39 · Trace the job without trusting its payload as authority](chapters/39.md#trace-the-job-without-trusting-its-payload-as-authority) |
| Figure F41-01 | Private-export boundaries and data stores | [Chapter 41 · 2. Data-flow and threat model for export creation and delivery](chapters/41.md#2-data-flow-and-threat-model-for-export-creation-and-delivery) |
| Figure F44-01 | Quarantine before any local positive-path recovery test | [Chapter 44 · Restore bytes, then reconcile authority](chapters/44.md#restore-bytes-then-reconcile-authority) |

## List of tables

324 entries in chapter and appendix order.

| ID or form | Caption, section or file | Locator |
| --- | --- | --- |
| Table T01-01 | A paper trace of the first program | [Chapter 01 · 1. Follow input, steps and output](chapters/01.md#1-follow-input-steps-and-output) |
| Unnumbered table | Where is the input? — Input data / Instruction that uses it | [Chapter 01 · Where is the input?](chapters/01.md#where-is-the-input) |
| Table T01-02 | The parts of a call | [Chapter 01 · 3. Read strings and function calls](chapters/01.md#3-read-strings-and-function-calls) |
| Unnumbered table | Worked example 1. Predict every character in a title — Position / Character | [Chapter 01 · Worked example 1. Predict every character in a title](chapters/01.md#worked-example-1-predict-every-character-in-a-title) |
| Table T01-03 | Comparing the two runs | [Chapter 01 · Worked example 2. Change one quoted word](chapters/01.md#worked-example-2-change-one-quoted-word) |
| Table T01-04 | Human decisions for an Alpha note | [Chapter 01 · 4. Explain what a private note needs to protect](chapters/01.md#4-explain-what-a-private-note-needs-to-protect) |
| Unnumbered table | Three questions an engineer asks — Question / Casebook example | [Chapter 01 · Three questions an engineer asks](chapters/01.md#three-questions-an-engineer-asks) |
| Unnumbered table | Hints — Task / First hint | [Chapter 01 · Hints](chapters/01.md#hints) |
| Unnumbered table | Practice check — Line / Input data | [Chapter 01 · Practice check](chapters/01.md#practice-check) |
| Unnumbered table | Glossary — Term / Meaning in this chapter | [Chapter 01 · Glossary](chapters/01.md#glossary) |
| Table T02-01 | Where to perform each action | [Chapter 02 · 2. Tell the tools and prompts apart](chapters/02.md#2-tell-the-tools-and-prompts-apart) |
| Table T02-02 | An illustrative comparison on macOS | [Chapter 02 · Worked example 2. A package seems to be missing](chapters/02.md#worked-example-2-a-package-seems-to-be-missing) |
| Unnumbered table | Install or locate Git — Platform / Installation route | [Chapter 02 · Install or locate Git](chapters/02.md#install-or-locate-git) |
| Unnumbered table | Troubleshooting by observation — Observation / What to inspect next | [Chapter 02 · Troubleshooting by observation](chapters/02.md#troubleshooting-by-observation) |
| Unnumbered table | Hints — Task / First hint | [Chapter 02 · Hints](chapters/02.md#hints) |
| Unnumbered table | Glossary — Term / Meaning in this chapter | [Chapter 02 · Glossary](chapters/02.md#glossary) |
| Table T03-01 | Tracking the name through the calculation | [Chapter 03 · 1. Give values readable names](chapters/03.md#1-give-values-readable-names) |
| Table T03-02 | Five types you will use immediately | [Chapter 03 · 2. Distinguish the value from its type](chapters/03.md#2-distinguish-the-value-from-its-type) |
| Table T03-03 | The meaning of the three inputs | [Chapter 03 · Worked example 1. Follow `"0"`, `0` and `None`](chapters/03.md#worked-example-1-follow-0-0-and-none) |
| Table T03-04 | Arithmetic expressions | [Chapter 03 · 3. Calculate and compare](chapters/03.md#3-calculate-and-compare) |
| Table T03-05 | Comparison operators | [Chapter 03 · Compare values deliberately](chapters/03.md#compare-values-deliberately) |
| Table T03-06 | Tracing the quota calculation | [Chapter 03 · Worked example 2. Predict a three-note quota](chapters/03.md#worked-example-2-predict-a-three-note-quota) |
| Unnumbered table | Follow the boundary and the invalid cases — Supplied count / Arithmetic or comparison result | [Chapter 03 · Follow the boundary and the invalid cases](chapters/03.md#follow-the-boundary-and-the-invalid-cases) |
| Unnumbered table | Hints — Task / First hint | [Chapter 03 · Hints](chapters/03.md#hints) |
| Unnumbered table | Practice check — Expression / Value | [Chapter 03 · Practice check](chapters/03.md#practice-check) |
| Unnumbered table | Glossary — Term / Meaning in this chapter | [Chapter 03 · Glossary](chapters/03.md#glossary) |
| Unnumbered table | 1. Combine the facts behind a decision — Expression / Result for boolean operands | [Chapter 04 · 1. Combine the facts behind a decision](chapters/04.md#1-combine-the-facts-behind-a-decision) |
| Unnumbered table | Worked example 1. Decide whether Mina may read the note — Condition reached for Mina / Value | [Chapter 04 · Worked example 1. Decide whether Mina may read the note](chapters/04.md#worked-example-1-decide-whether-mina-may-read-the-note) |
| Table T01 | Values before and after each access decision | [Chapter 04 · Trace a visitor, a member and an unknown role](chapters/04.md#trace-a-visitor-a-member-and-an-unknown-role) |
| Table T04-01 | Count before and after each request | [Chapter 04 · Worked example 2. The last admitted note](chapters/04.md#worked-example-2-the-last-admitted-note) |
| Unnumbered table | Hints — Task / First hint | [Chapter 04 · Hints](chapters/04.md#hints) |
| Unnumbered table | Exercise 3 — Range / Supplied integers | [Chapter 04 · Exercise 3](chapters/04.md#exercise-3) |
| Unnumbered table | Practice check — Fixture / First selected branch | [Chapter 04 · Practice check](chapters/04.md#practice-check) |
| Unnumbered table | Glossary — Term / Meaning in this chapter | [Chapter 04 · Glossary](chapters/04.md#glossary) |
| Table T05-01 | Four collection choices | [Chapter 05 · 1. Choose a collection for the information you need](chapters/05.md#1-choose-a-collection-for-the-information-you-need) |
| Table T05-02 | References before and after the mutation | [Chapter 05 · Worked example 2. Two users share one role list](chapters/05.md#worked-example-2-two-users-share-one-role-list) |
| Table T05-03 | Group membership after each input record | [Chapter 05 · Group all six notes](chapters/05.md#group-all-six-notes) |
| Unnumbered table | Hints — Task / First hint | [Chapter 05 · Hints](chapters/05.md#hints) |
| Unnumbered table | Glossary — Term / Meaning in this chapter | [Chapter 05 · Glossary](chapters/05.md#glossary) |
| Table T06-01 | Two calls to the same calculation | [Chapter 06 · 1. Define a function and trace its calls](chapters/06.md#1-define-a-function-and-trace-its-calls) |
| Unnumbered table | Predict a mutable default across calls — Moment / Default list contents | [Chapter 06 · Predict a mutable default across calls](chapters/06.md#predict-a-mutable-default-across-calls) |
| Table T06-02 | Contract for `may_read` | [Chapter 06 · 3. Extract the access decision as a pure operation](chapters/06.md#3-extract-the-access-decision-as-a-pure-operation) |
| Table T06-03 | Two calls within one interpreter run | [Chapter 06 · Import the rule and keep printing in the caller](chapters/06.md#import-the-rule-and-keep-printing-in-the-caller) |
| Unnumbered table | Hints — Task / First hint | [Chapter 06 · Hints](chapters/06.md#hints) |
| Unnumbered table | Glossary — Term / Meaning in this chapter | [Chapter 06 · Glossary](chapters/06.md#glossary) |
| Unnumbered table | 1. Follow text across an encoding boundary — Operation / Input type | [Chapter 07 · 1. Follow text across an encoding boundary](chapters/07.md#1-follow-text-across-an-encoding-boundary) |
| Table T07-01 | Accounting for every part of the title | [Chapter 07 · Worked example 1. Measure the Persian note title](chapters/07.md#worked-example-1-measure-the-persian-note-title) |
| Unnumbered table | Separate display names from short codes — Short code / Existing workspace name | [Chapter 07 · Separate display names from short codes](chapters/07.md#separate-display-names-from-short-codes) |
| Table T07-02 | Workspace code policy, version 1 | [Chapter 07 · 4. Validate a bounded identifier with a full match](chapters/07.md#4-validate-a-bounded-identifier-with-a-full-match) |
| Unnumbered table | Read the pattern before using it — Pattern part / Meaning | [Chapter 07 · Read the pattern before using it](chapters/07.md#read-the-pattern-before-using-it) |
| Table T07-03 | Additional policy decisions | [Chapter 07 · Trace boundary and reserved-name cases](chapters/07.md#trace-boundary-and-reserved-name-cases) |
| Unnumbered table | Hints — Task / First hint | [Chapter 07 · Hints](chapters/07.md#hints) |
| Unnumbered table | Glossary — Term / Meaning in this chapter | [Chapter 07 · Glossary](chapters/07.md#glossary) |
| Unnumbered table | 1. Locate a file with `pathlib` — Expression / Meaning | [Chapter 08 · 1. Locate a file with `pathlib`](chapters/08.md#1-locate-a-file-with-pathlib) |
| Unnumbered table | Choose read and write modes deliberately — Mode / Behavior relevant to this chapter | [Chapter 08 · Choose read and write modes deliberately](chapters/08.md#choose-read-and-write-modes-deliberately) |
| Unnumbered table | JSON fixture with an absent key — JSON representation / Python result | [Chapter 08 · JSON fixture with an absent key](chapters/08.md#json-fixture-with-an-absent-key) |
| Table T08-01 | Inventory schema for this exercise | [Chapter 08 · 4. Validate and convert into one record shape](chapters/08.md#4-validate-and-convert-into-one-record-shape) |
| Unnumbered table | Distinguish an empty inventory from an empty file — Input / Result under this exercise's policy | [Chapter 08 · Distinguish an empty inventory from an empty file](chapters/08.md#distinguish-an-empty-inventory-from-an-empty-file) |
| Unnumbered table | Hints — Task / First hint | [Chapter 08 · Hints](chapters/08.md#hints) |
| Unnumbered table | Glossary — Term / Meaning in this chapter | [Chapter 08 · Glossary](chapters/08.md#glossary) |
| Table T09-01 | Reading the missing-file traceback upward | [Chapter 09 · Worked example 1. A missing settings file](chapters/09.md#worked-example-1-a-missing-settings-file) |
| Unnumbered table | Readability, encoding and syntax are separate checks — Failure / Typical exception | [Chapter 09 · Readability, encoding and syntax are separate checks](chapters/09.md#readability-encoding-and-syntax-are-separate-checks) |
| Table T09-02 | Cleanup ownership | [Chapter 09 · Observe cleanup after success, parsing failure and opening failure](chapters/09.md#observe-cleanup-after-success-parsing-failure-and-opening-failure) |
| Unnumbered table | 4. Reduce a bug and inspect it with a breakpoint — Debugger command / What to inspect | [Chapter 09 · 4. Reduce a bug and inspect it with a breakpoint](chapters/09.md#4-reduce-a-bug-and-inspect-it-with-a-breakpoint) |
| Unnumbered table | Match the error message to its reader — Audience / Example information | [Chapter 09 · Match the error message to its reader](chapters/09.md#match-the-error-message-to-its-reader) |
| Unnumbered table | Hints — Task / First hint | [Chapter 09 · Hints](chapters/09.md#hints) |
| Unnumbered table | Glossary — Term / Meaning in this chapter | [Chapter 09 · Glossary](chapters/09.md#glossary) |
| Unnumbered table | 1. Describe an interface with type hints — Annotation / How to read it | [Chapter 10 · 1. Describe an interface with type hints](chapters/10.md#1-describe-an-interface-with-type-hints) |
| Table T10-01 | Draft model policy | [Chapter 10 · Worked example 1. Build the complete draft dataclass](chapters/10.md#worked-example-1-build-the-complete-draft-dataclass) |
| Unnumbered table | Verify the allowed transition and unchanged original — Operation / Expected outcome | [Chapter 10 · Verify the allowed transition and unchanged original](chapters/10.md#verify-the-allowed-transition-and-unchanged-original) |
| Table T10-02 | Following the owner value through the boundary | [Chapter 10 · Worked example 2. From JSON owner to a checked model](chapters/10.md#worked-example-2-from-json-owner-to-a-checked-model) |
| Unnumbered table | Hints — Task / First hint | [Chapter 10 · Hints](chapters/10.md#hints) |
| Unnumbered table | Glossary — Term / Meaning in this chapter | [Chapter 10 · Glossary](chapters/10.md#glossary) |
| Table T11-01 | The three requests and suspension points | [Chapter 11 · Worked example 1. Request exactly three records](chapters/11.md#worked-example-1-request-exactly-three-records) |
| Unnumbered table | 4. Match the tool to the responsibility — Need / Suitable tool in this chapter | [Chapter 11 · 4. Match the tool to the responsibility](chapters/11.md#4-match-the-tool-to-the-responsibility) |
| Unnumbered table | Hints — Task / First hint | [Chapter 11 · Hints](chapters/11.md#hints) |
| Unnumbered table | Glossary — Term / Meaning in this chapter | [Chapter 11 · Glossary](chapters/11.md#glossary) |
| Unnumbered table | 1. Arrange, act and assert with pytest — Step / Question | [Chapter 12 · 1. Arrange, act and assert with pytest](chapters/12.md#1-arrange-act-and-assert-with-pytest) |
| Unnumbered table | 4. Give a reviewer a focused change and evidence — Area / Cases in this chapter | [Chapter 12 · 4. Give a reviewer a focused change and evidence](chapters/12.md#4-give-a-reviewer-a-focused-change-and-evidence) |
| Unnumbered table | Hints — Task / First hint | [Chapter 12 · Hints](chapters/12.md#hints) |
| Unnumbered table | Glossary — Term / Meaning in this chapter | [Chapter 12 · Glossary](chapters/12.md#glossary) |
| Table T13-01 | Sources and validation for this chapter | [Chapter 13 · 2. Configuration precedence, typed settings and startup validation](chapters/13.md#2-configuration-precedence-typed-settings-and-startup-validation) |
| Table T13-02 | The conversion path | [Chapter 13 · Trace each value and type](chapters/13.md#trace-each-value-and-type) |
| Table T13-03 | A credential delivery and replacement plan | [Chapter 13 · 3. Secret stores, least privilege, rotation and development fixtures](chapters/13.md#3-secret-stores-least-privilege-rotation-and-development-fixtures) |
| Table T14-01 | The command surface | [Chapter 14 · 1. `argparse` subcommands, help and arguments](chapters/14.md#1-argparse-subcommands-help-and-arguments) |
| Table T14-02 | The note-count result contract | [Chapter 14 · 2. Standard input, standard output, standard error and exit codes](chapters/14.md#2-standard-input-standard-output-standard-error-and-exit-codes) |
| Table T14-03 | Budgets and their limits | [Chapter 14 · Account for each resource](chapters/14.md#account-for-each-resource) |
| Table T15-01 | The starting records | [Chapter 15 · 1. Tables, rows, keys, constraints and basic SQL](chapters/15.md#1-tables-rows-keys-constraints-and-basic-sql) |
| Table T15-02 | Expected fixture reads | [Chapter 15 · Trace a read across the workspace boundary](chapters/15.md#trace-a-read-across-the-workspace-boundary) |
| Table T16-01 | Questions at each layer | [Chapter 16 · 1. Hosts, IP addresses, DNS, ports and TCP connections](chapters/16.md#1-hosts-ip-addresses-dns-ports-and-tcp-connections) |
| Table T16-02 | The URL components | [Chapter 16 · 2. HTTP methods, URLs, headers, status codes, bodies and media types](chapters/16.md#2-http-methods-urls-headers-status-codes-bodies-and-media-types) |
| Table T16-03 | Request annotations | [Chapter 16 · Worked example 1: annotate the recording first](chapters/16.md#worked-example-1-annotate-the-recording-first) |
| Table T16-04 | Response annotations | [Chapter 16 · Worked example 1: annotate the recording first](chapters/16.md#worked-example-1-annotate-the-recording-first) |
| Table T16-05 | Accepted data and resource budgets | [Chapter 16 · 4. Time budgets, pagination, caching and error handling in Python clients](chapters/16.md#4-time-budgets-pagination-caching-and-error-handling-in-python-clients) |
| Table T16-06 | Expected replay results | [Chapter 16 · Replay the recordings and inject a timeout](chapters/16.md#replay-the-recordings-and-inject-a-timeout) |
| Table T17-01 | People, workspaces and records used in this chapter | [Chapter 17 · Keep the established fixture](chapters/17.md#keep-the-established-fixture) |
| Table T17-02 | Asset and store inventory | [Chapter 17 · Inventory what needs protection](chapters/17.md#inventory-what-needs-protection) |
| Table T17-03 | Entry point inventory | [Chapter 17 · Name the entry points](chapters/17.md#name-the-entry-points) |
| Table T17-04 | Design status at the start of Part V | [Chapter 17 · Separate existing code from planned components](chapters/17.md#separate-existing-code-from-planned-components) |
| Table T17-05 | Trace the values and their sources | [Chapter 17 · Worked example 1: follow one browser read](chapters/17.md#worked-example-1-follow-one-browser-read) |
| Table T17-06 | Two boundary records with concrete checks | [Chapter 17 · Record boundary assumptions where they can be challenged](chapters/17.md#record-boundary-assumptions-where-they-can-be-challenged) |
| Table T17-07 | Export scenarios and required observable outcomes | [Chapter 17 · Predict the result at each point in time](chapters/17.md#predict-the-result-at-each-point-in-time) |
| Table T17-08 | Failure review | [Chapter 17 · Include ordinary failures](chapters/17.md#include-ordinary-failures) |
| Table T17-09 | Synchronous and background export options | [Chapter 17 · 4. Compare design options and record the owner of each control](chapters/17.md#4-compare-design-options-and-record-the-owner-of-each-control) |
| Exhibit D17-02 | Casebook design record | [Chapter 17 · Write a short decision record](chapters/17.md#write-a-short-decision-record) |
| Table T17-10 | Control ownership and evidence register | [Chapter 17 · Assign each control and check its status](chapters/17.md#assign-each-control-and-check-its-status) |
| Unnumbered table | Keep an honest evidence note — Evidence state / Example | [Chapter 17 · Keep an honest evidence note](chapters/17.md#keep-an-honest-evidence-note) |
| Table T18-01 | Improve an imprecise statement | [Chapter 18 · Give a requirement a shape](chapters/18.md#give-a-requirement-a-shape) |
| Exhibit D18-01 | Requirement `CB-READ-01` | [Chapter 18 · Worked example 1: turn “notes are private” into a two-workspace test](chapters/18.md#worked-example-1-turn-notes-are-private-into-a-two-workspace-test) |
| Table T18-02 | Acceptance matrix for `CB-READ-01` | [Chapter 18 · Worked example 1: turn “notes are private” into a two-workspace test](chapters/18.md#worked-example-1-turn-notes-are-private-into-a-two-workspace-test) |
| Table T18-03 | A small risk register | [Chapter 18 · 2. Likelihood, impact, uncertainty and risk ownership](chapters/18.md#2-likelihood-impact-uncertainty-and-risk-ownership) |
| Table T18-04 | Field decisions for the diagnostic artifact | [Chapter 18 · Worked example 2: choose the fields for a support export](chapters/18.md#worked-example-2-choose-the-fields-for-a-support-export) |
| Exhibit D18-03 | Retention decision `CB-RETENTION-01` | [Chapter 18 · Work through one retention decision](chapters/18.md#work-through-one-retention-decision) |
| Table T18-05 | Scope of the retention claim | [Chapter 18 · Give every copy a separate inventory row](chapters/18.md#give-every-copy-a-separate-inventory-row) |
| Table T18-06 | The three-requirement handoff | [Chapter 18 · 4. Turn a design decision into an acceptance criterion and ASVS evidence](chapters/18.md#4-turn-a-design-decision-into-an-acceptance-criterion-and-asvs-evidence) |
| Table T18-07 | Acceptance evidence for retention | [Chapter 18 · Make the deletion pass/fail decision observable](chapters/18.md#make-the-deletion-passfail-decision-observable) |
| Table T18-08 | Selected ASVS 5.0.0 mappings | [Chapter 18 · Map selected controls to a pinned standard](chapters/18.md#map-selected-controls-to-a-pinned-standard) |
| Table T19-01 | Files and responsibilities | [Chapter 19 · Establish the smallest starting state](chapters/19.md#establish-the-smallest-starting-state) |
| Table T19-02 | Validation points and their limits | [Chapter 19 · Place checks where their facts become available](chapters/19.md#place-checks-where-their-facts-become-available) |
| Table T19-03 | Product rule versus this chapter's implemented HTTP surface | [Chapter 19 · Keep future queries local to a request](chapters/19.md#keep-future-queries-local-to-a-request) |
| Table T19-04 | Diagnose a failed first run | [Chapter 19 · Common failures and what they mean](chapters/19.md#common-failures-and-what-they-mean) |
| Exhibit D19-01 | A small evidence record to fill | [Chapter 19 · Guided lab: demonstrate the boundary from a fresh start](chapters/19.md#guided-lab-demonstrate-the-boundary-from-a-fresh-start) |
| Table T20-01 | Proposed operations and representations | [Chapter 20 · Begin with one update](chapters/20.md#begin-with-one-update) |
| Table T20-02 | Contract failures | [Chapter 20 · Define failures before writing a view](chapters/20.md#define-failures-before-writing-a-view) |
| Table T20-03 | Field ownership for note creation and update | [Chapter 20 · 2. Required, optional, unknown and server-owned fields](chapters/20.md#2-required-optional-unknown-and-server-owned-fields) |
| Table T20-04 | Update authorization and state policy | [Chapter 20 · Define who may update](chapters/20.md#define-who-may-update) |
| Table T20-05 | Note transitions | [Chapter 20 · 3. State machines, idempotency and replayed business operations](chapters/20.md#3-state-machines-idempotency-and-replayed-business-operations) |
| Exhibit D20-02 | Export acceptance contract | [Chapter 20 · Worked example 2: submit one export twice](chapters/20.md#worked-example-2-submit-one-export-twice) |
| Table T20-06 | Stored Alpha note `101` after each decision | [Chapter 20 · A demonstration with final stored state](chapters/20.md#a-demonstration-with-final-stored-state) |
| Exhibit D20-03 | Proposed list contract; not implemented by the laboratory | [Chapter 20 · Bound collection requests](chapters/20.md#bound-collection-requests) |
| Exhibit D20-04 | Casebook inventory after this chapter | [Chapter 20 · Keep an honest inventory](chapters/20.md#keep-an-honest-inventory) |
| Exhibit D20-05 | Evidence record | [Chapter 20 · Guided lab: prove acceptance, refusal and replay](chapters/20.md#guided-lab-prove-acceptance-refusal-and-replay) |
| Table T21-01 | Mina's account lifecycle and the evidence behind each step | [Chapter 21 · 1. Registration, identity proofing assumptions and enumeration-resistant responses](chapters/21.md#1-registration-identity-proofing-assumptions-and-enumeration-resistant-responses) |
| Table T21-02 | Authentication is still followed by authorization | [Chapter 21 · Upgrades need a persistence path](chapters/21.md#upgrades-need-a-persistence-path) |
| Table T21-03 | Options for a future Mina account with MFA | [Chapter 21 · Choose the fallback while choosing the primary authenticator](chapters/21.md#choose-the-fallback-while-choosing-the-primary-authenticator) |
| Exhibit D21-01 | Abuse-control acceptance decisions; not implemented in the laboratories | [Chapter 21 · Define abuse controls before exposing recovery](chapters/21.md#define-abuse-controls-before-exposing-recovery) |
| Exhibit D21-02 | Recovery token and completion policy | [Chapter 21 · A recovery token is a credential](chapters/21.md#a-recovery-token-is-a-credential) |
| Table T21-04 | Stored state after the important boundaries | [Chapter 21 · Worked example 2: known versus unknown, then expiry and reuse](chapters/21.md#worked-example-2-known-versus-unknown-then-expiry-and-reuse) |
| Exhibit D21-03 | Proposed observation and authority policy | [Chapter 21 · What may support staff observe?](chapters/21.md#what-may-support-staff-observe) |
| Table T22-01 | Proposed session-cookie settings over HTTPS | [Chapter 22 · Make cookie behavior explicit](chapters/22.md#make-cookie-behavior-explicit) |
| Table T22-02 | Expected session state across Mina's sign-in | [Chapter 22 · Rotate at the change in authority](chapters/22.md#rotate-at-the-change-in-authority) |
| Table T22-03 | Token forms and validation ownership | [Chapter 22 · 2. Opaque tokens, token storage and lifetime](chapters/22.md#2-opaque-tokens-token-storage-and-lifetime) |
| Table T22-04 | Information visible in this proposed flow | [Chapter 22 · Follow what each component receives](chapters/22.md#follow-what-each-component-receives) |
| Exhibit D22-01 | Partner API token profile | [Chapter 22 · Fix the verification policy before reading a token](chapters/22.md#fix-the-verification-policy-before-reading-a-token) |
| Table T22-05 | Claim-policy observations | [Chapter 22 · Worked example 2: a fixed recipient and a fixed clock](chapters/22.md#worked-example-2-a-fixed-recipient-and-a-fixed-clock) |
| Exhibit D22-02 | Decision `CB-IDENTITY-22` | [Chapter 22 · Decision record: browser sessions and a partner integration](chapters/22.md#decision-record-browser-sessions-and-a-partner-integration) |
| Table T22-06 | Identity success is followed by current workspace checks | [Chapter 22 · Decision record: browser sessions and a partner integration](chapters/22.md#decision-record-browser-sessions-and-a-partner-integration) |
| Exhibit D22-03 | Evidence sheet | [Chapter 22 · Guided lab: separate policy evidence from protocol evidence](chapters/22.md#guided-lab-separate-policy-evidence-from-protocol-evidence) |
| Table T23-01 | Name the decision before writing a condition | [Chapter 23 · 1. Subjects, actions, objects, tenants and deny-by-default decisions](chapters/23.md#1-subjects-actions-objects-tenants-and-deny-by-default-decisions) |
| Table T03 | Subjects, actions and objects in two workspaces | [Chapter 23 · Fill the same matrix for every read path](chapters/23.md#fill-the-same-matrix-for-every-read-path) |
| Table T23-02 | Explicit read representations | [Chapter 23 · Function, object and field decisions are different](chapters/23.md#function-object-and-field-decisions-are-different) |
| Exhibit D23-01 | Entry-point coverage checklist with concrete decisions | [Chapter 23 · Administrative access still needs a policy](chapters/23.md#administrative-access-still-needs-a-policy) |
| Table T23-03 | Committed revocation and the next local read | [Chapter 23 · Show exactly what the next request sees](chapters/23.md#show-exactly-what-the-next-request-sees) |
| Exhibit D23-02 | Evidence record to retain | [Chapter 23 · Guided lab: carry one matrix through every path](chapters/23.md#guided-lab-carry-one-matrix-through-every-path) |
| Table T24-01 | Companion files | [Chapter 24 · Starting files and a private laboratory](chapters/24.md#starting-files-and-a-private-laboratory) |
| Table T24-02 | Context determines the protection | [Chapter 24 · Worked example 1: `A & B` through source and text](chapters/24.md#worked-example-1-a--b-through-source-and-text) |
| Table T24-03 | Compare origins with `https://casebook.example` | [Chapter 24 · 2. Origins, the same-origin policy and cross-origin resource sharing](chapters/24.md#2-origins-the-same-origin-policy-and-cross-origin-resource-sharing) |
| Table T24-04 | Cookie decisions for the default HTTPS/test profile | [Chapter 24 · Cookie flags solve specific problems](chapters/24.md#cookie-flags-solve-specific-problems) |
| Table T24-05 | Expected stored state for the successful and failed form cases | [Chapter 24 · Inspect the final row, not only the response](chapters/24.md#inspect-the-final-row-not-only-the-response) |
| Table T04 | What escaping, cookies, CSRF checks, CORS and CSP each control | [Chapter 24 · Compare the controls in one table](chapters/24.md#compare-the-controls-in-one-table) |
| Exhibit D24-01 | Evidence layers | [Chapter 24 · Separate server evidence from browser evidence](chapters/24.md#separate-server-evidence-from-browser-evidence) |
| Exhibit D24-02 | Browser-boundary evidence record | [Chapter 24 · Guided lab: one note and one state change](chapters/24.md#guided-lab-one-note-and-one-state-change) |
| Exhibit D25-01 | Attachment policy `CB-ATTACH-25` | [Chapter 25 · Choose a small content policy before accepting bytes](chapters/25.md#choose-a-small-content-policy-before-accepting-bytes) |
| Table T25-01 | Storage layout and ownership | [Chapter 25 · State the storage trust boundary](chapters/25.md#state-the-storage-trust-boundary) |
| Table T25-02 | Lifecycle and compensating cleanup | [Chapter 25 · Stage, validate, publish and record](chapters/25.md#stage-validate-publish-and-record) |
| Exhibit D25-02 | Archive preflight policy | [Chapter 25 · Worked example 2: review a supplied manifest](chapters/25.md#worked-example-2-review-a-supplied-manifest) |
| Table T25-03 | What remains stored after each operation | [Chapter 25 · Run both worked examples and inspect the size boundary](chapters/25.md#run-both-worked-examples-and-inspect-the-size-boundary) |
| Table T25-04 | Choose the reconstruction boundary | [Chapter 25 · 4. JSON, XML, YAML and pickle trust assumptions when rebuilding objects](chapters/25.md#4-json-xml-yaml-and-pickle-trust-assumptions-when-rebuilding-objects) |
| Exhibit D25-03 | Attachment evidence record | [Chapter 25 · Guided lab: verify every boundary against final state](chapters/25.md#guided-lab-verify-every-boundary-against-final-state) |
| Exhibit D26-01 | Registry and workspace bindings | [Chapter 26 · 1. Server-side request forgery as a design risk and fixed destination registries](chapters/26.md#1-server-side-request-forgery-as-a-design-risk-and-fixed-destination-registries) |
| Table T26-01 | Which layer enforces which destination fact? | [Chapter 26 · DNS can change the effective destination](chapters/26.md#dns-can-change-the-effective-destination) |
| Exhibit D26-02 | Partner reply contract | [Chapter 26 · 3. Verified TLS, timeouts, response limits and partner schema validation](chapters/26.md#3-verified-tls-timeouts-response-limits-and-partner-schema-validation) |
| Exhibit D26-03 | Webhook protocol decisions | [Chapter 26 · Verify the bytes that arrived](chapters/26.md#verify-the-bytes-that-arrived) |
| Table T26-02 | Final-state ledger for the demonstration | [Chapter 26 · Run the trace through final state](chapters/26.md#run-the-trace-through-final-state) |
| Exhibit D26-04 | Evidence record | [Chapter 26 · Guided lab: prove the integration boundaries](chapters/26.md#guided-lab-prove-the-integration-boundaries) |
| Table T05 | Hashing, message authentication, signatures and encryption | [Chapter 27 · 2. Digests, keyed message authentication codes (HMACs) and digital signatures](chapters/27.md#2-digests-keyed-message-authentication-codes-hmacs-and-digital-signatures) |
| Table T27-01 | Webhook verification contract | [Chapter 27 · Concrete job A: authenticate the webhook](chapters/27.md#concrete-job-a-authenticate-the-webhook) |
| Table T27-02 | Final webhook state across the key change | [Chapter 27 · Webhook key rotation trace](chapters/27.md#webhook-key-rotation-trace) |
| Table T27-03 | Small encrypted-record contract | [Chapter 27 · Concrete job B: protect a stored export](chapters/27.md#concrete-job-b-protect-a-stored-export) |
| Table T27-04 | Ownership and custody decisions for the two jobs | [Chapter 27 · 4. Key custody, separation, rotation, backup and algorithm migration](chapters/27.md#4-key-custody-separation-rotation-backup-and-algorithm-migration) |
| Table T27-05 | Export final-state ledger | [Chapter 27 · Run both jobs through their boundaries](chapters/27.md#run-both-jobs-through-their-boundaries) |
| Table T28-01 | Execution choices and their boundaries | [Chapter 28 · 1. Threads, processes, asyncio, await and cancellation](chapters/28.md#1-threads-processes-asyncio-await-and-cancellation) |
| Table T28-02 | Why a preliminary read is not a claim | [Chapter 28 · 2. Races, locks, database constraints and transaction boundaries](chapters/28.md#2-races-locks-database-constraints-and-transaction-boundaries) |
| Table T28-03 | Python, database and application guarantees | [Chapter 28 · Worked example 1: two observers, one committed export](chapters/28.md#worked-example-1-two-observers-one-committed-export) |
| Table T28-04 | Final stored state, including failure branches | [Chapter 28 · Inspect the complete trace](chapters/28.md#inspect-the-complete-trace) |
| Table T28-05 | Cleanup owners | [Chapter 28 · Worked example 2: cancel a long-running fixture and inspect cleanup](chapters/28.md#worked-example-2-cancel-a-long-running-fixture-and-inspect-cleanup) |
| Table T28-06 | Concrete budgets and their scope | [Chapter 28 · 4. Limits on time, bytes, parallel work and requests per tenant](chapters/28.md#4-limits-on-time-bytes-parallel-work-and-requests-per-tenant) |
| Table T29-01 | The paths a reviewer must establish | [Chapter 29 · Trace each entry point, including unchanged code](chapters/29.md#trace-each-entry-point-including-unchanged-code) |
| Table T29-02 | Vocabulary for reading a data-flow claim | [Chapter 29 · 2. SAST, rule scope and taint-flow vocabulary](chapters/29.md#2-sast-rule-scope-and-taint-flow-vocabulary) |
| Table T29-03 | Selected finding cards for the candidate source | [Chapter 29 · Two supplied static findings](chapters/29.md#two-supplied-static-findings) |
| Table T29-04 | Decisions supported by this packet | [Chapter 29 · 4. Confidence, false positives, fixes and regression coverage](chapters/29.md#4-confidence-false-positives-fixes-and-regression-coverage) |
| Table T29-05 | Checks and their limits | [Chapter 29 · Select regression checks that answer the claim](chapters/29.md#select-regression-checks-that-answer-the-claim) |
| Table T30-01 | Files and dependencies | [Chapter 30 · Starting state and laboratory files](chapters/30.md#starting-state-and-laboratory-files) |
| Table T30-02 | Requirements for this laboratory | [Chapter 30 · State three requirements precisely](chapters/30.md#state-three-requirements-precisely) |
| Table T30-03 | Evidence methods and their boundaries | [Chapter 30 · 3. DAST, IAST, coverage and limits](chapters/30.md#3-dast-iast-coverage-and-limits) |
| Table T30-04 | Read only the claim the fixture supports | [Chapter 30 · Worked example: present does not mean enforced](chapters/30.md#worked-example-present-does-not-mean-enforced) |
| Table T30-05 | Filled verification matrix for this draft | [Chapter 30 · Build a verification matrix for three controls](chapters/30.md#build-a-verification-matrix-for-three-controls) |
| Table T31-01 | Laboratory files | [Chapter 31 · Starting state and files](chapters/31.md#starting-state-and-files) |
| Table T31-02 | Read the sample dependency tree as relationships | [Chapter 31 · 1. Direct and transitive dependencies, build backends, wheels and source distributions](chapters/31.md#1-direct-and-transitive-dependencies-build-backends-wheels-and-source-distributions) |
| Table T31-03 | Controls with different jobs | [Chapter 31 · 2. Pins, constraints, hashes, index selection and isolated builds](chapters/31.md#2-pins-constraints-hashes-index-selection-and-isolated-builds) |
| Table T31-04 | Recorded build results | [Chapter 31 · Build two environments and preserve negative results](chapters/31.md#build-two-environments-and-preserve-negative-results) |
| Table T31-05 | What the recorded inventories contain | [Chapter 31 · Worked example 1: follow the indirect package into installed code](chapters/31.md#worked-example-1-follow-the-indirect-package-into-installed-code) |
| Table T31-06 | Exact before-build trace recorded locally | [Chapter 31 · Worked example 1: follow the indirect package into installed code](chapters/31.md#worked-example-1-follow-the-indirect-package-into-installed-code) |
| Table T31-07 | Filled decision for FICTIONAL-CH31-001 | [Chapter 31 · Make the update decision concrete](chapters/31.md#make-the-update-decision-concrete) |
| Table T32-01 | New files | [Chapter 32 · Starting state and files](chapters/32.md#starting-state-and-files) |
| Table T32-02 | Identities used by the gate | [Chapter 32 · Name the identities before reading the colors](chapters/32.md#name-the-identities-before-reading-the-colors) |
| Table T32-03 | Concrete job and authority separation | [Chapter 32 · 2. Jobs, artifacts, minimum token permissions and untrusted changes](chapters/32.md#2-jobs-artifacts-minimum-token-permissions-and-untrusted-changes) |
| Table T32-04 | Check roles and evidence in this laboratory | [Chapter 32 · 3. Combine tests, static analysis, dependency and secret-check results](chapters/32.md#3-combine-tests-static-analysis-dependency-and-secret-check-results) |
| Table T32-05 | Read the skipped-job case precisely | [Chapter 32 · Worked example 1: one required job never ran](chapters/32.md#worked-example-1-one-required-job-never-ran) |
| Table T32-06 | Decision policy before implementation | [Chapter 32 · 4. Gate policy, expiring exceptions, signing and promotion by digest](chapters/32.md#4-gate-policy-expiring-exceptions-signing-and-promotion-by-digest) |
| Table T32-07 | Passed, failed and incomplete cases for that same subject | [Chapter 32 · Inspect the recorded release decisions](chapters/32.md#inspect-the-recorded-release-decisions) |
| Table T32-08 | Follow one finding through the release evidence | [Chapter 32 · Part checkpoint: finding, correction, regression and gate](chapters/32.md#part-checkpoint-finding-correction-regression-and-gate) |
| Table T33-01 | Audit requirements for the illustrated export path | [Chapter 33 · Starting state and the required-audit policy](chapters/33.md#starting-state-and-the-required-audit-policy) |
| Table T33-02 | Laboratory files | [Chapter 33 · Files and isolated setup](chapters/33.md#files-and-isolated-setup) |
| Table T33-03 | Audit schema version 1 | [Chapter 33 · Define a small schema before emitting events](chapters/33.md#define-a-small-schema-before-emitting-events) |
| Table T33-04 | Correlated facts actually stored in the fixture | [Chapter 33 · Worked example 2: correlate service acceptance with worker denial](chapters/33.md#worked-example-2-correlate-service-acceptance-with-worker-denial) |
| Table T33-05 | Redaction choices in this event schema | [Chapter 33 · Allowlist content instead of trying to mask everything afterwards](chapters/33.md#allowlist-content-instead-of-trying-to-mask-everything-afterwards) |
| Table T33-06 | Proposed production access boundaries | [Chapter 33 · Restrict readers and retention authority](chapters/33.md#restrict-readers-and-retention-authority) |
| Table T33-07 | Required-record and delivery-failure decisions | [Chapter 33 · Decide what a failure means before returning success](chapters/33.md#decide-what-a-failure-means-before-returning-success) |
| Table T34-01 | Select evidence for the question | [Chapter 34 · Start with a question](chapters/34.md#start-with-a-question) |
| Table T34-02 | Exact counts in two synthetic 600-second windows | [Chapter 34 · Worked example 1: the same ten denials](chapters/34.md#worked-example-1-the-same-ten-denials) |
| Table T34-03 | Proposed measurements; these are not installed collectors | [Chapter 34 · Keep labels bounded](chapters/34.md#keep-labels-bounded) |
| Table T34-04 | Authored training rules and their owners | [Chapter 34 · A deliberately small alert policy](chapters/34.md#a-deliberately-small-alert-policy) |
| Table T34-05 | Blocked request timeline and current snapshots | [Chapter 34 · Worked example 2: request 1 is still queued](chapters/34.md#worked-example-2-request-1-is-still-queued) |
| Table T34-06 | Same symptom, different evidence | [Chapter 34 · Worked example 2: request 1 is still queued](chapters/34.md#worked-example-2-request-1-is-still-queued) |
| Table T34-07 | A reviewable decision for the blocked fixture | [Chapter 34 · Filled-in triage note](chapters/34.md#filled-in-triage-note) |
| Table T35-01 | Evidence layers for runtime identity | [Chapter 35 · Worked example 1: which user wins?](chapters/35.md#worked-example-1-which-user-wins) |
| Table T35-02 | Original scheme through the reviewed path | [Chapter 35 · Worked example 2: who supplied `https`?](chapters/35.md#worked-example-2-who-supplied-https) |
| Table T35-03 | Host preparation contract for this Linux deployment | [Chapter 35 · Give each writable path a reason](chapters/35.md#give-each-writable-path-a-reason) |
| Table T35-04 | Filled-in review record for the authoring run | [Chapter 35 · Attach evidence for one blocked connection](chapters/35.md#attach-evidence-for-one-blocked-connection) |
| Table T36-01 | State with different recovery responsibilities | [Chapter 36 · Scenario and laboratory boundary](chapters/36.md#scenario-and-laboratory-boundary) |
| Table T36-02 | Filled-in intake record | [Chapter 36 · Accept the report without making another exposure](chapters/36.md#accept-the-report-without-making-another-exposure) |
| Table T36-03 | Roles and concrete decisions | [Chapter 36 · Assign authority before making changes](chapters/36.md#assign-authority-before-making-changes) |
| Table T36-04 | Interpreted timeline, with claims kept separate | [Chapter 36 · Worked example 1: three redacted records become a UTC timeline](chapters/36.md#worked-example-1-three-redacted-records-become-a-utc-timeline) |
| Table T36-05 | Before deletion, damaged state and restored candidate | [Chapter 36 · Worked example 2: compare the candidate with the known backup](chapters/36.md#worked-example-2-compare-the-candidate-with-the-known-backup) |
| Table T36-06 | Stored-state evidence around promotion | [Chapter 36 · Inspect the failure state, not just the message](chapters/36.md#inspect-the-failure-state-not-just-the-message) |
| Table T36-07 | Corrective actions with an acceptance check | [Chapter 36 · Separate cause, contributing authority and proof of repair](chapters/36.md#separate-cause-contributing-authority-and-proof-of-repair) |
| Table T36-08 | Filled-in local handover | [Chapter 36 · A concrete recovery handover](chapters/36.md#a-concrete-recovery-handover) |
| Table T37-01 | The authored debug rules | [Chapter 37 · Project and rule contract](chapters/37.md#project-and-rule-contract) |
| Table T37-02 | Files and their roles | [Chapter 37 · Project and rule contract](chapters/37.md#project-and-rule-contract) |
| Table T37-03 | Why equal-looking text has different meaning | [Chapter 37 · Worked example 2: the same name in a comment and an assignment](chapters/37.md#worked-example-2-the-same-name-in-a-comment-and-an-assignment) |
| Table T37-04 | Boundaries a reviewer must know | [Chapter 37 · Recognized uncertainty and blind spots differ](chapters/37.md#recognized-uncertainty-and-blind-spots-differ) |
| Table T37-05 | Expected members of this pinned example build | [Chapter 37 · Build and inspect the wheel](chapters/37.md#build-and-inspect-the-wheel) |
| Table T37-06 | Process exit contract | [Chapter 37 · Stable output is part of the tool](chapters/37.md#stable-output-is-part-of-the-tool) |
| Table T37-07 | Disposition for the two supplied files | [Chapter 37 · Turn output into a bounded review decision](chapters/37.md#turn-output-into-a-bounded-review-decision) |
| Table T38-01 | Information with different responsibilities | [Chapter 38 · Normalize meaning without discarding the original](chapters/38.md#normalize-meaning-without-discarding-the-original) |
| Table T38-02 | Exact source-reference mapping | [Chapter 38 · Worked example 1: merge the duplicate without losing its origins](chapters/38.md#worked-example-1-merge-the-duplicate-without-losing-its-origins) |
| Table T38-03 | Selected lifecycle rules | [Chapter 38 · Suppression is a recorded decision, not disappearance](chapters/38.md#suppression-is-a-recorded-decision-not-disappearance) |
| Table T38-04 | Classification, identity, severity and response | [Chapter 38 · 3. CWE weakness classes, CVE identifiers, CVSS severity and contextual impact](chapters/38.md#3-cwe-weakness-classes-cve-identifiers-cvss-severity-and-contextual-impact) |
| Table T06 | Severity, exposure and ownership in a remediation queue | [Chapter 38 · Worked example 2: equal severity, different exposure](chapters/38.md#worked-example-2-equal-severity-different-exposure) |
| Table T38-05 | Action deadlines and conditional remediation targets | [Chapter 38 · Deadlines are authored policy decisions](chapters/38.md#deadlines-are-authored-policy-decisions) |
| Table T39-01 | Identity and authority at different boundaries | [Chapter 39 · A service has an identity of its own](chapters/39.md#a-service-has-an-identity-of-its-own) |
| Table T39-02 | Least-privilege comparison for the selected worker design | [Chapter 39 · Worked example 1: two workers, two permission sets](chapters/39.md#worked-example-1-two-workers-two-permission-sets) |
| Table T39-03 | UTC grant trace | [Chapter 39 · Worked example 2: follow the private grant's lifetime](chapters/39.md#worked-example-2-follow-the-private-grants-lifetime) |
| Table T39-04 | Stored state and the decision it supports | [Chapter 39 · Revocation changes access, not necessarily stored data](chapters/39.md#revocation-changes-access-not-necessarily-stored-data) |
| Table T39-05 | Responsibilities to assign in the design review | [Chapter 39 · Managed infrastructure does not choose the tenant](chapters/39.md#managed-infrastructure-does-not-choose-the-tenant) |
| Table T39-06 | Different clocks govern different decisions | [Chapter 39 · Keep the clocks separate](chapters/39.md#keep-the-clocks-separate) |
| Table T39-07 | Review artifact and required verification evidence | [Chapter 39 · Evidence needed to approve a real policy](chapters/39.md#evidence-needed-to-approve-a-real-policy) |
| Table T40-01 | Fictional release roster | [Chapter 40 · Give work and decisions named owners](chapters/40.md#give-work-and-decisions-named-owners) |
| Table T40-02 | Design review triggers and requested evidence | [Chapter 40 · Trigger review from changes to a boundary](chapters/40.md#trigger-review-from-changes-to-a-boundary) |
| Table T40-03 | One-release plan and review dates, all UTC | [Chapter 40 · A release calendar with outputs](chapters/40.md#a-release-calendar-with-outputs) |
| Table T40-04 | Required evidence for this release decision | [Chapter 40 · Write the behavior before choosing its report](chapters/40.md#write-the-behavior-before-choosing-its-report) |
| Table T40-05 | Selected SSDF practice links, with authored release evidence | [Chapter 40 · Use frameworks to organize improvement](chapters/40.md#use-frameworks-to-organize-improvement) |
| Table T40-06 | Small improvement goals, not claimed maturity levels | [Chapter 40 · Use frameworks to organize improvement](chapters/40.md#use-frameworks-to-organize-improvement) |
| Table T40-07 | Top-three handover for this release | [Chapter 40 · Keep the queue connected to action](chapters/40.md#keep-the-queue-connected-to-action) |
| Table T40-08 | Completed fictional exception record | [Chapter 40 · Worked example: a time-limited exception to a required control](chapters/40.md#worked-example-a-time-limited-exception-to-a-required-control) |
| Table T40-09 | Same overdue count, different denominators | [Chapter 40 · Worked example: four overdue items in each team](chapters/40.md#worked-example-four-overdue-items-in-each-team) |
| Table T40-10 | Useful measures and their limits | [Chapter 40 · What the numbers justify](chapters/40.md#what-the-numbers-justify) |
| Table T40-11 | Evaluated exercise decisions | [Chapter 40 · Execute the arithmetic and record checks](chapters/40.md#execute-the-arithmetic-and-record-checks) |
| Table T40-12 | A concrete Part X bundle | [Chapter 40 · Part-checkpoint handover](chapters/40.md#part-checkpoint-handover) |
| Table T41-01 | Learner fixture | [Chapter 41 · Your assignment](chapters/41.md#your-assignment) |
| Table T41-02 | Filled product decisions | [Chapter 41 · Worked design: `CB-EXPORT-41`, revision 1](chapters/41.md#worked-design-cb-export-41-revision-1) |
| Table T41-03 | Input and ownership contract | [Chapter 41 · Client-owned and server-owned values](chapters/41.md#client-owned-and-server-owned-values) |
| Table T41-04 | Proposed route inventory | [Chapter 41 · Client-owned and server-owned values](chapters/41.md#client-owned-and-server-owned-values) |
| Table T41-05 | Threats, responses and planned observations | [Chapter 41 · Identify concrete failures before choosing a library](chapters/41.md#identify-concrete-failures-before-choosing-a-library) |
| Table T41-06 | Alpha decisions | [Chapter 41 · Fill the access matrices](chapters/41.md#fill-the-access-matrices) |
| Table T41-07 | Beta decisions | [Chapter 41 · Fill the access matrices](chapters/41.md#fill-the-access-matrices) |
| Table T41-08 | Service decisions | [Chapter 41 · Fill the access matrices](chapters/41.md#fill-the-access-matrices) |
| Table T41-09 | Departure trace for M-A | [Chapter 41 · Worked example 1: a departing member's old export](chapters/41.md#worked-example-1-a-departing-members-old-export) |
| Table T41-10 | Export data inventory | [Chapter 41 · Classify every copy](chapters/41.md#classify-every-copy) |
| Table T41-11 | Retention decision `CB-EXPORT-RET-41` | [Chapter 41 · Expiry and deletion clocks](chapters/41.md#expiry-and-deletion-clocks) |
| Table T41-12 | Grant decision comparison | [Chapter 41 · Worked example 2: grant rights at request time or at collection time?](chapters/41.md#worked-example-2-grant-rights-at-request-time-or-at-collection-time) |
| Table T41-13 | Requirements and proposed responsibility | [Chapter 41 · 4. Requirement IDs, test strategy and explicit exclusions](chapters/41.md#4-requirement-ids-test-strategy-and-explicit-exclusions) |
| Table T41-14 | Acceptance cases and final-state evidence | [Chapter 41 · Planned acceptance ledger](chapters/41.md#planned-acceptance-ledger) |
| Table T41-15 | Trust assumptions to verify or constrain | [Chapter 41 · Explicit assumptions and exclusions](chapters/41.md#explicit-assumptions-and-exclusions) |
| Table T42-01 | Four reviewable increments | [Chapter 42 · The increments and their stopping points](chapters/42.md#the-increments-and-their-stopping-points) |
| Table T42-02 | Three kinds of identity | [Chapter 42 · Carry chapter 41's field contract into code](chapters/42.md#carry-chapter-41s-field-contract-into-code) |
| Table T42-03 | Admission/retry ledger | [Chapter 42 · Worked example 1: create the same export twice with one request key](chapters/42.md#worked-example-1-create-the-same-export-twice-with-one-request-key) |
| Table T42-04 | Two revocation positions, different stored results | [Chapter 42 · Worked example 2: revoke between queueing and collection](chapters/42.md#worked-example-2-revoke-between-queueing-and-collection) |
| Table T42-05 | Lifecycle stage's final-state ledger | [Chapter 42 · Run all three increments](chapters/42.md#run-all-three-increments) |
| Table T42-06 | Chapter 41 evidence disposition | [Chapter 42 · Keep the acceptance ledger honest](chapters/42.md#keep-the-acceptance-ledger-honest) |
| Table T43-01 | What each label means | [Chapter 43 · Evidence labels used throughout](chapters/43.md#evidence-labels-used-throughout) |
| Table T43-02 | Actual candidate identity | [Chapter 43 · Identify the candidate before reviewing it](chapters/43.md#identify-the-candidate-before-reviewing-it) |
| Table T43-03 | Mandatory requirement-to-evidence index | [Chapter 43 · Map every mandatory control](chapters/43.md#map-every-mandatory-control) |
| Table T43-04 | Selected ACTUAL-RUN outcomes from the candidate | [Chapter 43 · Retain observable state, not only test totals](chapters/43.md#retain-observable-state-not-only-test-totals) |
| Table T43-05 | Source observations and their dispositions | [Chapter 43 · Review static findings as claims about paths](chapters/43.md#review-static-findings-as-claims-about-paths) |
| Table T43-06 | ACTUAL-RUN inventory facts | [Chapter 43 · Check what the artifact and run actually contain](chapters/43.md#check-what-the-artifact-and-run-actually-contain) |
| Table T43-07 | Dependency-gate exercise; other gates assumed complete only in these rows | [Chapter 43 · Worked example 1: the dependency report is missing](chapters/43.md#worked-example-1-the-dependency-report-is-missing) |
| Table T43-08 | Version reassessment and the artifact boundary | [Chapter 43 · Worked example 2: reassess a finding after identifying the installed version](chapters/43.md#worked-example-2-reassess-a-finding-after-identifying-the-installed-version) |
| Table T43-09 | Actual production decision ledger | [Chapter 43 · Apply the mandatory gates without averaging them](chapters/43.md#apply-the-mandatory-gates-without-averaging-them) |
| Table T43-10 | Release blockers and closure criteria | [Chapter 43 · Give every open item a next action](chapters/43.md#give-every-open-item-a-next-action) |
| Table T43-11 | Retained evidence index | [Chapter 43 · Keep a navigable record](chapters/43.md#keep-a-navigable-record) |
| Table T44-01 | Identity carried forward from chapter 43 | [Chapter 44 · The subject and starting state](chapters/44.md#the-subject-and-starting-state) |
| Table T44-02 | Reconstructed synthetic timeline, all on 2026-11-26 UTC | [Chapter 44 · Worked example 1: rebuild the UTC timeline](chapters/44.md#worked-example-1-rebuild-the-utc-timeline) |
| Table T44-03 | Assessment at detection | [Chapter 44 · Separate confirmed facts from unknowns](chapters/44.md#separate-confirmed-facts-from-unknowns) |
| Table T44-04 | Containment decision record | [Chapter 44 · Keep the privacy gate while reducing work](chapters/44.md#keep-the-privacy-gate-while-reducing-work) |
| Table T44-05 | Managed-copy observations | [Chapter 44 · Define copy scope before declaring removal complete](chapters/44.md#define-copy-scope-before-declaring-removal-complete) |
| Table T44-06 | Recovery inputs and resulting checks | [Chapter 44 · Reconcile the facts that must not roll back](chapters/44.md#reconcile-the-facts-that-must-not-roll-back) |
| Table T44-07 | Executed recovery probes | [Chapter 44 · Verify recovery with both allowed and denied paths](chapters/44.md#verify-recovery-with-both-allowed-and-denied-paths) |
| Table T44-08 | Original acceptance checks and required additions | [Chapter 44 · Worked example 2: compare tests after a retention change](chapters/44.md#worked-example-2-compare-tests-after-a-retention-change) |
| Table T44-09 | Retrospective actions, proposed fictional owners | [Chapter 44 · A short advisory and retrospective](chapters/44.md#a-short-advisory-and-retrospective) |
| Unnumbered table | Handover another engineer can run — Open item / Next responsible role | [Chapter 44 · Handover another engineer can run](chapters/44.md#handover-another-engineer-can-run) |
| Table T44-10 | Completion is scoped | [Chapter 44 · Separate three decisions](chapters/44.md#separate-three-decisions) |
| Table TA-01 | Which question each form answers | [Appendix · Form 3: check a change over time](appendices.md#form-3-check-a-change-over-time) |
| Table TB-01 | Language and standard-library shelf | [Appendix · Find the explanation by the task](appendices.md#find-the-explanation-by-the-task) |
| Table TB-02 | Choose a tool for a named check | [Appendix · Framework and tool shelf](appendices.md#framework-and-tool-shelf) |
| Table TC-01 | What to retain after each kind of exercise | [Appendix · Hints by practice type](appendices.md#hints-by-practice-type) |
| Unnumbered table | Chapter solution directory — Chapter / Solution section | [Appendix · Chapter solution directory](appendices.md#chapter-solution-directory) |
| Table TD-01 | Reference roles and editions | [Appendix · Use the right kind of reference](appendices.md#use-the-right-kind-of-reference) |
| Table TD-02 | Technical requirement to control/evidence | [Appendix · Verified ASVS requirements and bounded evidence](appendices.md#verified-asvs-requirements-and-bounded-evidence) |
| Table TD-03 | Risk category to concrete review question | [Appendix · Risk categories: use the right year's identifier](appendices.md#risk-categories-use-the-right-years-identifier) |
| Table TD-04 | Verified SSDF tasks | [Appendix · Development practices and improvement evidence](appendices.md#development-practices-and-improvement-evidence) |
| Table TD-05 | SAMM version 2 practice names, not invented activity numbers | [Appendix · Development practices and improvement evidence](appendices.md#development-practices-and-improvement-evidence) |
| Table TD-06 | Do not confuse classification with applicable vulnerability evidence | [Appendix · Read CWE, CVE and CVSS precisely](appendices.md#read-cwe-cve-and-cvss-precisely) |

## List of listings

287 entries in chapter and appendix order.

| ID or form | Caption, section or file | Locator |
| --- | --- | --- |
| Listing L01-01 | A three-line display for a fictional note | [Chapter 01 · 1. Follow input, steps and output](chapters/01.md#1-follow-input-steps-and-output) |
| Listing L01-02 | The same display with a different title | [Chapter 01 · Worked example 2. Change one quoted word](chapters/01.md#worked-example-2-change-one-quoted-word) |
| Listing L01-03 | An empty title | [Chapter 01 · A boundary case. Empty text](chapters/01.md#a-boundary-case-empty-text) |
| Listing L02-01 | The first script saved on your computer | [Chapter 02 · Save and run the first script](chapters/02.md#save-and-run-the-first-script) |
| Listing L02-02 | Inspecting the interpreter from inside a script | [Chapter 02 · Worked example 1. Ask the running interpreter to identify itself](chapters/02.md#worked-example-1-ask-the-running-interpreter-to-identify-itself) |
| Listing L02-03 | Ignore patterns for the learning repository | [Chapter 02 · Decide which files belong in history](chapters/02.md#decide-which-files-belong-in-history) |
| Listing L03-01 | Assigning and reassigning names | [Chapter 03 · 1. Give values readable names](chapters/03.md#1-give-values-readable-names) |
| Listing L03-02 | Making types visible | [Chapter 03 · Worked example 1. Follow `"0"`, `0` and `None`](chapters/03.md#worked-example-1-follow-0-0-and-none) |
| Listing L03-03 | Three values tested as booleans | [Chapter 03 · Truth values answer a different question](chapters/03.md#truth-values-answer-a-different-question) |
| Listing L03-04 | Remaining places and a quota result | [Chapter 03 · Worked example 2. Predict a three-note quota](chapters/03.md#worked-example-2-predict-a-three-note-quota) |
| Listing L03-05 | Inspecting a floating-point sum | [Chapter 03 · Floats have representation limits](chapters/03.md#floats-have-representation-limits) |
| Listing L03-06 | Interpreting text as a count | [Chapter 03 · 4. Convert, format and keep returned values](chapters/03.md#4-convert-format-and-keep-returned-values) |
| Listing L03-07 | A readable quota report | [Chapter 03 · Build readable messages with f-strings](chapters/03.md#build-readable-messages-with-f-strings) |
| Listing L03-08 | Capturing the return value of `print` | [Chapter 03 · A function can display one thing and return another](chapters/03.md#a-function-can-display-one-thing-and-return-another) |
| Listing L03-09 | Five expressions to predict | [Chapter 03 · Practice check. Predict five expressions](chapters/03.md#practice-check-predict-five-expressions) |
| Listing L04-01 | The conditions for Mina's request | [Chapter 04 · Build Mina's result one fact at a time](chapters/04.md#build-minas-result-one-fact-at-a-time) |
| Listing L04-02 | Skipping a comparison when the count is missing | [Chapter 04 · Short-circuit evaluation](chapters/04.md#short-circuit-evaluation) |
| Listing L04-03 | Choosing which message to display | [Chapter 04 · 2. Select a branch with an explicit default](chapters/04.md#2-select-a-branch-with-an-explicit-default) |
| Listing L04-04 | A read decision with reasons | [Chapter 04 · Worked example 1. Decide whether Mina may read the note](chapters/04.md#worked-example-1-decide-whether-mina-may-read-the-note) |
| Listing L04-05 | Three local inspection attempts | [Chapter 04 · Count repetitions with `for` and `range`](chapters/04.md#count-repetitions-with-for-and-range) |
| Listing L04-06 | Filling the last quota place | [Chapter 04 · Change state with `while`](chapters/04.md#change-state-with-while) |
| Listing L04-07 | Distinguishing a skipped item from a stopped loop | [Chapter 04 · Stop with `break` and skip with `continue`](chapters/04.md#stop-with-break-and-skip-with-continue) |
| Listing L04-08 | Two requests near a three-note limit | [Chapter 04 · Worked example 2. The last admitted note](chapters/04.md#worked-example-2-the-last-admitted-note) |
| Listing L04-09 | Repeating the read decision for three fixtures | [Chapter 04 · Run the three access scenarios in one file](chapters/04.md#run-the-three-access-scenarios-in-one-file) |
| Listing L05-01 | Inspecting four collection shapes | [Chapter 05 · Read the literal forms](chapters/05.md#read-the-literal-forms) |
| Listing L05-02 | Removing duplicate role names | [Chapter 05 · Preserve the meaning of duplicate values](chapters/05.md#preserve-the-meaning-of-duplicate-values) |
| Listing L05-03 | Indexing, slicing and membership | [Chapter 05 · 2. Retrieve values without hiding missing information](chapters/05.md#2-retrieve-values-without-hiding-missing-information) |
| Listing L05-04 | A missing key and an explicit missing value | [Chapter 05 · Look up a field and keep absence distinct](chapters/05.md#look-up-a-field-and-keep-absence-distinct) |
| Listing L05-05 | The shared-list mistake | [Chapter 05 · Worked example 2. Two users share one role list](chapters/05.md#worked-example-2-two-users-share-one-role-list) |
| Listing L05-06 | Independent role collections | [Chapter 05 · Create separate lists and check the result](chapters/05.md#create-separate-lists-and-check-the-result) |
| Listing L05-07 | Separate records with a shared nested list | [Chapter 05 · A shallow copy still shares nested objects](chapters/05.md#a-shallow-copy-still-shares-nested-objects) |
| Listing L05-08 | Copying at the boundary that needs independence | [Chapter 05 · A shallow copy still shares nested objects](chapters/05.md#a-shallow-copy-still-shares-nested-objects) |
| Listing L05-09 | Selecting and ordering note identifiers | [Chapter 05 · 4. Transform and group records with predictable output](chapters/05.md#4-transform-and-group-records-with-predictable-output) |
| Listing L05-10 | Grouping a six-note inventory | [Chapter 05 · Group all six notes](chapters/05.md#group-all-six-notes) |
| Listing L06-01 | Naming the quota calculation | [Chapter 06 · 1. Define a function and trace its calls](chapters/06.md#1-define-a-function-and-trace-its-calls) |
| Listing L06-02 | A local reassignment | [Chapter 06 · Read local scope](chapters/06.md#read-local-scope) |
| Listing L06-03 | A default for a quota calculation | [Chapter 06 · 2. Make arguments and defaults explicit](chapters/06.md#2-make-arguments-and-defaults-explicit) |
| Listing L06-04 | A role list that survives between calls | [Chapter 06 · Predict a mutable default across calls](chapters/06.md#predict-a-mutable-default-across-calls) |
| Listing L06-05 | Independent results from a role helper | [Chapter 06 · Create the result within each call](chapters/06.md#create-the-result-within-each-call) |
| Listing L06-06 | The reusable read rule | [Chapter 06 · Worked example 1. Extract the rule from the printing loop](chapters/06.md#worked-example-1-extract-the-rule-from-the-printing-loop) |
| Listing L06-07 | One printing loop with two readers | [Chapter 06 · Import the rule and keep printing in the caller](chapters/06.md#import-the-rule-and-keep-printing-in-the-caller) |
| Listing L06-08 | Reporting two decisions in reverse order | [Chapter 06 · Use the same module from a second script](chapters/06.md#use-the-same-module-from-a-second-script) |
| Listing L06-09 | A module that announces when it runs | [Chapter 06 · Worked example 2. Observe top-level execution](chapters/06.md#worked-example-2-observe-top-level-execution) |
| Listing L06-10 | Importing a module twice in one run | [Chapter 06 · Worked example 2. Observe top-level execution](chapters/06.md#worked-example-2-observe-top-level-execution) |
| Listing L06-11 | A main guard for the rules module | [Chapter 06 · Give the rules module a direct-run message](chapters/06.md#give-the-rules-module-a-direct-run-message) |
| Listing L07-01 | Code points and UTF-8 bytes | [Chapter 07 · Worked example 1. Measure the Persian note title](chapters/07.md#worked-example-1-measure-the-persian-note-title) |
| Listing L07-02 | A title crossing the file boundary | [Chapter 07 · Store those bytes, then decode the file](chapters/07.md#store-those-bytes-then-decode-the-file) |
| Listing L07-03 | Slicing text and bytes | [Chapter 07 · A byte slice can cut through a letter](chapters/07.md#a-byte-slice-can-cut-through-a-letter) |
| Listing L07-04 | Two representations of an accented letter | [Chapter 07 · Normalization can change the representation](chapters/07.md#normalization-can-change-the-representation) |
| Listing L07-05 | Inspecting text cleanup | [Chapter 07 · 3. Transform text under a stated policy](chapters/07.md#3-transform-text-under-a-stated-policy) |
| Listing L07-06 | Keeping empty fields visible | [Chapter 07 · Split fields and join a report](chapters/07.md#split-fields-and-join-a-report) |
| Listing L07-07 | A code validator with explicit reasons | [Chapter 07 · Worked example 2. Validate three short codes](chapters/07.md#worked-example-2-validate-three-short-codes) |
| Listing L07-08 | Accepted text and two rejected inputs | [Chapter 07 · Worked example 2. Validate three short codes](chapters/07.md#worked-example-2-validate-three-short-codes) |
| Listing L08-01 | Reading a title from a relative path | [Chapter 08 · Worked example 1. Read the Persian title as UTF-8 text](chapters/08.md#worked-example-1-read-the-persian-title-as-utf-8-text) |
| Fixture F08-01 | Three candidate CSV records | [Chapter 08 · CSV fixture with a quoted comma](chapters/08.md#csv-fixture-with-a-quoted-comma) |
| Listing L08-02 | Inspecting the parsed CSV rows | [Chapter 08 · CSV fixture with a quoted comma](chapters/08.md#csv-fixture-with-a-quoted-comma) |
| Fixture F08-02 | The same three candidates as JSON | [Chapter 08 · JSON fixture with an absent key](chapters/08.md#json-fixture-with-an-absent-key) |
| Listing L08-03 | Inspecting the JSON types and missing key | [Chapter 08 · JSON fixture with an absent key](chapters/08.md#json-fixture-with-an-absent-key) |
| Listing L08-04 | Shared validation and CSV adaptation | [Chapter 08 · Put the common checks in one module](chapters/08.md#put-the-common-checks-in-one-module) |
| Listing L08-05 | A complete small-inventory converter | [Chapter 08 · Convert both fixture files and write their summaries](chapters/08.md#convert-both-fixture-files-and-write-their-summaries) |
| Result R08-01 | The complete summary for either fixture | [Chapter 08 · Inspect the converted records](chapters/08.md#inspect-the-converted-records) |
| Listing L09-01 | Following a failed open through two functions | [Chapter 09 · Worked example 1. A missing settings file](chapters/09.md#worked-example-1-a-missing-settings-file) |
| Listing L09-02 | Loading a UTF-8 JSON document | [Chapter 09 · Keep file loading in one small function](chapters/09.md#keep-file-loading-in-one-small-function) |
| Listing L09-03 | Reporting expected input failures | [Chapter 09 · Give different failures different outcomes](chapters/09.md#give-different-failures-different-outcomes) |
| Listing L09-04 | Preserving a cause while adding context | [Chapter 09 · Raise a failure with application context](chapters/09.md#raise-a-failure-with-application-context) |
| Listing L09-05 | When a file is closed during error handling | [Chapter 09 · Observe cleanup after success, parsing failure and opening failure](chapters/09.md#observe-cleanup-after-success-parsing-failure-and-opening-failure) |
| Listing L09-06 | Distinguishing access refusal from JSON syntax | [Chapter 09 · Worked example 2. A genuine file permission refusal](chapters/09.md#worked-example-2-a-genuine-file-permission-refusal) |
| Listing L09-07 | Publishing a completed JSON document | [Chapter 09 · Preserve a previous summary until its replacement is ready](chapters/09.md#preserve-a-previous-summary-until-its-replacement-is-ready) |
| Listing L09-08 | Checking final state after a failed write | [Chapter 09 · Preserve a previous summary until its replacement is ready](chapters/09.md#preserve-a-previous-summary-until-its-replacement-is-ready) |
| Listing L09-09 | Pausing before a record check | [Chapter 09 · 4. Reduce a bug and inspect it with a breakpoint](chapters/09.md#4-reduce-a-bug-and-inspect-it-with-a-breakpoint) |
| Listing L10-01 | A class with an attribute and a method | [Chapter 10 · 2. Give related values an instance](chapters/10.md#2-give-related-values-an-instance) |
| Listing L10-02 | A validated dataclass and its transition | [Chapter 10 · Worked example 1. Build the complete draft dataclass](chapters/10.md#worked-example-1-build-the-complete-draft-dataclass) |
| Listing L10-03 | Publishing a draft with an owner | [Chapter 10 · Verify the allowed transition and unchanged original](chapters/10.md#verify-the-allowed-transition-and-unchanged-original) |
| Listing L10-04 | A wrong argument and an unresolved optional value | [Chapter 10 · Give the checker two mistakes to find](chapters/10.md#give-the-checker-two-mistakes-to-find) |
| Listing L10-05 | Requiring an owner deliberately | [Chapter 10 · Narrow the optional value before returning it](chapters/10.md#narrow-the-optional-value-before-returning-it) |
| Listing L10-06 | Independent queues of draft models | [Chapter 10 · Compose models without sharing mutable defaults](chapters/10.md#compose-models-without-sharing-mutable-defaults) |
| Listing L10-07 | A hint-only dataclass receives dynamic data | [Chapter 10 · 4. Check external input at runtime](chapters/10.md#4-check-external-input-at-runtime) |
| Listing L10-08 | Parsing an external draft record | [Chapter 10 · Worked example 2. From JSON owner to a checked model](chapters/10.md#worked-example-2-from-json-owner-to-a-checked-model) |
| Listing L10-09 | Reading and reporting three draft candidates | [Chapter 10 · Worked example 2. From JSON owner to a checked model](chapters/10.md#worked-example-2-from-json-owner-to-a-checked-model) |
| Listing L11-01 | Consuming an iterator once | [Chapter 11 · 1. Follow one item through an iterator](chapters/11.md#1-follow-one-item-through-an-iterator) |
| Fixture F11-01 | A small inventory for tracing a longer stream | [Chapter 11 · A generator pauses at `yield`](chapters/11.md#a-generator-pauses-at-yield) |
| Listing L11-02 | A generator over a text stream | [Chapter 11 · Bound each read and yield one parsed object](chapters/11.md#bound-each-read-and-yield-one-parsed-object) |
| Listing L11-03 | Stepping through the generator by hand | [Chapter 11 · Worked example 1. Request exactly three records](chapters/11.md#worked-example-1-request-exactly-three-records) |
| Listing L11-04 | A limited counting function | [Chapter 11 · Count without collecting the entire inventory](chapters/11.md#count-without-collecting-the-entire-inventory) |
| Listing L11-05 | Limiting selected results or limiting input reads | [Chapter 11 · Put the limit at the intended boundary](chapters/11.md#put-the-limit-at-the-intended-boundary) |
| Listing L11-06 | Three records in batches of two | [Chapter 11 · Batch only the permitted input](chapters/11.md#batch-only-the-permitted-input) |
| Listing L11-07 | A timing decorator with preserved metadata | [Chapter 11 · Worked example 2. Measure duration without recording arguments](chapters/11.md#worked-example-2-measure-duration-without-recording-arguments) |
| Listing L11-08 | Timing the consuming function | [Chapter 11 · Verify the original name after wrapping](chapters/11.md#verify-the-original-name-after-wrapping) |
| Listing L11-09 | A context-managed record stream | [Chapter 11 · Give a stream a managed lifetime](chapters/11.md#give-a-stream-a-managed-lifetime) |
| Listing L12-01 | The quota exercise's starting point | [Chapter 12 · Prepare the deliberately faulty quota function](chapters/12.md#prepare-the-deliberately-faulty-quota-function) |
| Listing L12-02 | The failing boundary test | [Chapter 12 · Write the boundary expectation first](chapters/12.md#write-the-boundary-expectation-first) |
| Listing L12-03 | The corrected boundary | [Chapter 12 · Correct the implementation and retain the test](chapters/12.md#correct-the-implementation-and-retain-the-test) |
| Listing L12-04 | A quota table and invalid-input checks | [Chapter 12 · Check the quota neighborhood and expected exceptions](chapters/12.md#check-the-quota-neighborhood-and-expected-exceptions) |
| Listing L12-05 | Fresh member facts for each permission case | [Chapter 12 · Worked example 1. Test the access rule across roles](chapters/12.md#worked-example-1-test-the-access-rule-across-roles) |
| Listing L12-06 | A shared file fixture for preview tests | [Chapter 12 · Create a file inside a test-owned directory](chapters/12.md#create-a-file-inside-a-test-owned-directory) |
| Listing L12-07 | Checking the preview's actual read boundary | [Chapter 12 · Create a file inside a test-owned directory](chapters/12.md#create-a-file-inside-a-test-owned-directory) |
| Listing L12-08 | An expiry check with an explicit clock dependency | [Chapter 12 · Worked example 2. Replace a clock in an expiry check](chapters/12.md#worked-example-2-replace-a-clock-in-an-expiry-check) |
| Listing L12-09 | Before, at and after expiry without waiting | [Chapter 12 · Worked example 2. Replace a clock in an expiry check](chapters/12.md#worked-example-2-replace-a-clock-in-an-expiry-check) |
| Listing L12-10 | Deterministic duration and preserved metadata | [Chapter 12 · Control an existing timing wrapper](chapters/12.md#control-an-existing-timing-wrapper) |
| Listing L13-01 | Observe a process without dumping its environment | [Chapter 13 · Observe only the setting you need](chapters/13.md#observe-only-the-setting-you-need) |
| Listing L13-02 | Truth testing does not parse a word | [Chapter 13 · Worked example 1: why `bool("false")` enables a flag](chapters/13.md#worked-example-1-why-boolfalse-enables-a-flag) |
| Listing L13-03 | A small settings boundary | [Chapter 13 · Convert once, before starting work](chapters/13.md#convert-once-before-starting-work) |
| Listing L13-04 | Parse a synthetic environment | [Chapter 13 · Trace each value and type](chapters/13.md#trace-each-value-and-type) |
| Listing L13-05 | Validate before starting the application | [Chapter 13 · Worked example 2: reject a missing service credential](chapters/13.md#worked-example-2-reject-a-missing-service-credential) |
| Listing L13-06 | A deterministic missing-setting probe | [Chapter 13 · Worked example 2: reject a missing service credential](chapters/13.md#worked-example-2-reject-a-missing-service-credential) |
| Listing L13-07 | Settings and startup regression tests | [Chapter 13 · Assert the whole output contract](chapters/13.md#assert-the-whole-output-contract) |
| Listing L14-01 | A three-note fixture | [Chapter 14 · Define the input before counting it](chapters/14.md#define-the-input-before-counting-it) |
| Listing L14-02 | Bounded input and one shared counting rule | [Chapter 14 · Define the input before counting it](chapters/14.md#define-the-input-before-counting-it) |
| Listing L14-03 | A count subcommand with separate result streams | [Chapter 14 · Assemble the CLI](chapters/14.md#assemble-the-cli) |
| Listing L14-04 | The fixed helper | [Chapter 14 · 3. `subprocess` argument lists, executable selection and environment scope](chapters/14.md#3-subprocess-argument-lists-executable-selection-and-environment-scope) |
| Listing L14-05 | Launch and validate one bounded helper | [Chapter 14 · 3. `subprocess` argument lists, executable selection and environment scope](chapters/14.md#3-subprocess-argument-lists-executable-selection-and-environment-scope) |
| Listing L14-06 | A deterministic timeout demonstration | [Chapter 14 · Demonstrate a timeout without hoping a normal count runs slowly](chapters/14.md#demonstrate-a-timeout-without-hoping-a-normal-count-runs-slowly) |
| Listing L14-07 | Success, input errors, helper timeout and cleanup tests | [Chapter 14 · Test the process boundary](chapters/14.md#test-the-process-boundary) |
| Listing L15-01 | The database schema and synthetic seed records | [Chapter 15 · Make transaction behavior explicit](chapters/15.md#make-transaction-behavior-explicit) |
| Listing L15-02 | Names supplied as bound values | [Chapter 15 · Worked example 1: store O’Connor and O'Connor](chapters/15.md#worked-example-1-store-oconnor-and-oconnor) |
| Listing L03 | Queries with bound values and a workspace filter | [Chapter 15 · 3. Joins, workspace filters and indexes](chapters/15.md#3-joins-workspace-filters-and-indexes) |
| Listing L15-03 | Inspect committed rows after each transaction | [Chapter 15 · Worked example 2: inspect success and rollback from a new connection](chapters/15.md#worked-example-2-inspect-success-and-rollback-from-a-new-connection) |
| Listing L15-04 | A versioned SQLite migration | [Chapter 15 · Move the schema forward with a migration](chapters/15.md#move-the-schema-forward-with-a-migration) |
| Listing L15-05 | Workspace boundaries and transaction regression tests | [Chapter 15 · Tests must inspect the stored rows](chapters/15.md#tests-must-inspect-the-stored-rows) |
| Exhibit R16-01 | Recorded request | [Chapter 16 · Worked example 1: annotate the recording first](chapters/16.md#worked-example-1-annotate-the-recording-first) |
| Exhibit R16-02 | Recorded successful response | [Chapter 16 · Worked example 1: annotate the recording first](chapters/16.md#worked-example-1-annotate-the-recording-first) |
| Exhibit R16-03 | Recorded empty response | [Chapter 16 · Worked example 1: annotate the recording first](chapters/16.md#worked-example-1-annotate-the-recording-first) |
| Listing L16-01 | A bounded client for one fixed resource | [Chapter 16 · Parse the response and bound pagination](chapters/16.md#parse-the-response-and-bound-pagination) |
| Listing L16-02 | Recorded data and a deterministic transport | [Chapter 16 · Replay the recordings and inject a timeout](chapters/16.md#replay-the-recordings-and-inject-a-timeout) |
| Listing L16-03 | A local replay command | [Chapter 16 · Replay the recordings and inject a timeout](chapters/16.md#replay-the-recordings-and-inject-a-timeout) |
| Listing L16-04 | A fixed HTTPS transport | [Chapter 16 · A real HTTPS adapter, with the same fixed destination](chapters/16.md#a-real-https-adapter-with-the-same-fixed-destination) |
| Listing L16-05 | HTTP client regression tests | [Chapter 16 · Verify decisions without a network](chapters/16.md#verify-decisions-without-a-network) |
| Exhibit D17-01 | A filled-in export intent | [Chapter 17 · Worked example 2: move an export to a worker](chapters/17.md#worked-example-2-move-an-export-to-a-worker) |
| Listing L18-01 | Privacy acceptance checks at the repository boundary | [Chapter 18 · Run the existing repository against the requirement](chapters/18.md#run-the-existing-repository-against-the-requirement) |
| Exhibit D18-02 | The agreed synthetic payload | [Chapter 18 · Worked example 2: choose the fields for a support export](chapters/18.md#worked-example-2-choose-the-fields-for-a-support-export) |
| Listing L18-02 | An observable local retention fixture | [Chapter 18 · Observe expiry, a failed deletion and a successful retry locally](chapters/18.md#observe-expiry-a-failed-deletion-and-a-successful-retry-locally) |
| Exhibit E18-01 | A filled local evidence record | [Chapter 18 · Record what the evidence proves](chapters/18.md#record-what-the-evidence-proves) |
| Listing L19-01 | The dependency and command entry point | [Chapter 19 · Establish the smallest starting state](chapters/19.md#establish-the-smallest-starting-state) |
| Unnumbered file | `manage.py` | [Chapter 19 · Establish the smallest starting state](chapters/19.md#establish-the-smallest-starting-state) |
| Listing L19-02 | Local development configuration with generic errors | [Chapter 19 · Settings are executable Python](chapters/19.md#settings-are-executable-python) |
| Listing L19-03 | The only public route and its view | [Chapter 19 · Worked example 1: a public health response](chapters/19.md#worked-example-1-a-public-health-response) |
| Unnumbered file | `notes/views.py` | [Chapter 19 · Worked example 1: a public health response](chapters/19.md#worked-example-1-a-public-health-response) |
| Listing L19-04 | Store notes without publishing them | [Chapter 19 · 3. Models, migrations, the ORM and request-scoped queries](chapters/19.md#3-models-migrations-the-orm-and-request-scoped-queries) |
| Listing L19-05 | The initial migration | [Chapter 19 · Apply schema changes with migrations](chapters/19.md#apply-schema-changes-with-migrations) |
| Listing L19-06 | Two workspaces and their private notes | [Chapter 19 · Seed two workspaces](chapters/19.md#seed-two-workspaces) |
| Listing L19-07 | A trusted local storage exercise | [Chapter 19 · Worked example 2: store a note through the ORM, then check the HTTP boundary](chapters/19.md#worked-example-2-store-a-note-through-the-orm-then-check-the-http-boundary) |
| Listing L19-08 | Evidence for public health and anonymous refusal | [Chapter 19 · 4. Development settings, the test client and a private default](chapters/19.md#4-development-settings-the-test-client-and-a-private-default) |
| Exhibit D20-01 | Proposed update request | [Chapter 20 · Begin with one update](chapters/20.md#begin-with-one-update) |
| Listing L20-01 | Update request schema | [Chapter 20 · A machine-readable shape, with explicit limits](chapters/20.md#a-machine-readable-shape-with-explicit-limits) |
| Listing L20-02 | Executable contracts and trusted fixture records | [Chapter 20 · Run the contract laboratory](chapters/20.md#run-the-contract-laboratory) |
| Listing L20-03 | Inspect accepted, invalid and repeated requests | [Chapter 20 · A demonstration with final stored state](chapters/20.md#a-demonstration-with-final-stored-state) |
| Listing L20-04 | Contract regression checks | [Chapter 20 · Repeatable tests, including rollback](chapters/20.md#repeatable-tests-including-rollback) |
| Unnumbered file | `requirements.txt` | [Chapter 21 · Worked example 1: set and verify one synthetic password with Django](chapters/21.md#worked-example-1-set-and-verify-one-synthetic-password-with-django) |
| Listing L21-01 | Real Django password APIs in a separate in-memory database | [Chapter 21 · Worked example 1: set and verify one synthetic password with Django](chapters/21.md#worked-example-1-set-and-verify-one-synthetic-password-with-django) |
| Listing L21-02 | Recovery state, a private mailbox and an injected clock | [Chapter 21 · Worked example 2: known versus unknown, then expiry and reuse](chapters/21.md#worked-example-2-known-versus-unknown-then-expiry-and-reuse) |
| Listing L21-03 | A recovery walkthrough without printing secrets | [Chapter 21 · Worked example 2: known versus unknown, then expiry and reuse](chapters/21.md#worked-example-2-known-versus-unknown-then-expiry-and-reuse) |
| Listing L21-04 | Controlled-clock and final-state tests | [Chapter 21 · Prove the refusal does not hide a write](chapters/21.md#prove-the-refusal-does-not-hide-a-write) |
| Unnumbered file | `requirements.txt` | [Chapter 22 · Worked example 1: trace login, rotation, recovery invalidation and logout](chapters/22.md#worked-example-1-trace-login-rotation-recovery-invalidation-and-logout) |
| Listing L22-01 | Django session APIs with an isolated database | [Chapter 22 · Worked example 1: trace login, rotation, recovery invalidation and logout](chapters/22.md#worked-example-1-trace-login-rotation-recovery-invalidation-and-logout) |
| Listing L22-02 | Application claim policy and synthetic claims | [Chapter 22 · Worked example 2: a fixed recipient and a fixed clock](chapters/22.md#worked-example-2-a-fixed-recipient-and-a-fixed-clock) |
| Listing L22-03 | Local wrong-audience and expiry cases | [Chapter 22 · Worked example 2: a fixed recipient and a fixed clock](chapters/22.md#worked-example-2-a-fixed-recipient-and-a-fixed-clock) |
| Listing L22-04 | A configured access-token verifier | [Chapter 22 · Verify the signed bytes and required claims together](chapters/22.md#verify-the-signed-bytes-and-required-claims-together) |
| Listing L22-05 | Signed-token verification cases and key overlap | [Chapter 22 · Test real local signatures when the dependency is available](chapters/22.md#test-real-local-signatures-when-the-dependency-is-available) |
| Listing L04 | A permission-scoped query reused by two views | [Chapter 23 · Reuse the complete scope](chapters/23.md#reuse-the-complete-scope) |
| Listing L23-01 | The same identities before and after revocation | [Chapter 23 · Run the complete trace](chapters/23.md#run-the-complete-trace) |
| Listing L23-02 | Matrix, field, function and next-request checks | [Chapter 23 · Make the role-by-action table executable](chapters/23.md#make-the-role-by-action-table-executable) |
| Listing L24-01 | The private note template | [Chapter 24 · Let the template preserve the context](chapters/24.md#let-the-template-preserve-the-context) |
| Listing L24-02 | Source and parsed-text evidence | [Chapter 24 · Inspect expected HTML without pretending it came from Django](chapters/24.md#inspect-expected-html-without-pretending-it-came-from-django) |
| Unnumbered file | `examples/ch24/requirements.txt` | [Chapter 24 · Configure the real framework boundary](chapters/24.md#configure-the-real-framework-boundary) |
| Listing L24-03 | Isolated Django configuration, views and synthetic seed | [Chapter 24 · Configure the real framework boundary](chapters/24.md#configure-the-real-framework-boundary) |
| Listing L24-04 | A sign-in form that uses the framework CSRF tag | [Chapter 24 · Configure the real framework boundary](chapters/24.md#configure-the-real-framework-boundary) |
| Listing L24-05 | Prepared rendering, CSRF, object-access and stored-state checks | [Chapter 24 · Enable CSRF enforcement in the test client](chapters/24.md#enable-csrf-enforcement-in-the-test-client) |
| Listing L25-01 | Bounded private attachment storage | [Chapter 25 · Stage, validate, publish and record](chapters/25.md#stage-validate-publish-and-record) |
| Listing L25-02 | Manifest parsing and preflight decisions | [Chapter 25 · Worked example 2: review a supplied manifest](chapters/25.md#worked-example-2-review-a-supplied-manifest) |
| Listing L25-03 | Duplicate labels, exact limits and rejected state | [Chapter 25 · Run both worked examples and inspect the size boundary](chapters/25.md#run-both-worked-examples-and-inspect-the-size-boundary) |
| Listing L25-04 | Boundary, privacy, link and failure checks | [Chapter 25 · Repeatable tests: inspect files and rows together](chapters/25.md#repeatable-tests-inspect-files-and-rows-together) |
| Listing L26-01 | Registry, reply checks and authenticated event application | [Chapter 26 · Prepare the executable contracts](chapters/26.md#prepare-the-executable-contracts) |
| Listing L26-02 | Fake transport and explicit response closure | [Chapter 26 · Prepare the executable contracts](chapters/26.md#prepare-the-executable-contracts) |
| Unnumbered file | `examples/ch26/fixtures/report-ready.json` | [Chapter 26 · Store the webhook bytes and signing metadata](chapters/26.md#store-the-webhook-bytes-and-signing-metadata) |
| Unnumbered file | `examples/ch26/fixtures/report-ready.headers.json` | [Chapter 26 · Store the webhook bytes and signing metadata](chapters/26.md#store-the-webhook-bytes-and-signing-metadata) |
| Listing L26-03 | Redirect, oversized response and repeated stored event | [Chapter 26 · Run the trace through final state](chapters/26.md#run-the-trace-through-final-state) |
| Listing L26-04 | Local refusal, replay, rotation and rollback evidence | [Chapter 26 · Repeatable tests and what they prove](chapters/26.md#repeatable-tests-and-what-they-prove) |
| Unnumbered file | `examples/ch27/requirements.txt` | [Chapter 27 · Starting state and files](chapters/27.md#starting-state-and-files) |
| Listing L27-01 | Generate disposable values without exposing them | [Chapter 27 · A small prediction](chapters/27.md#a-small-prediction) |
| Listing L27-02 | Bounded encrypted storage and atomic key migration | [Chapter 27 · Worked example 2: open, reject and rotate one private record](chapters/27.md#worked-example-2-open-reject-and-rotate-one-private-record) |
| Listing L27-03 | Digest comparison, webhook key change and export migration | [Chapter 27 · Run both jobs through their boundaries](chapters/27.md#run-both-jobs-through-their-boundaries) |
| Listing L27-04 | Failure, separation, rotation and unchanged-state assertions | [Chapter 27 · Repeatable verification](chapters/27.md#repeatable-verification) |
| Unnumbered file | `examples/ch28/requirements.txt` | [Chapter 28 · Starting state and files](chapters/28.md#starting-state-and-files) |
| Listing L05 | An idempotent job with a database constraint | [Chapter 28 · Worked example 1: two observers, one committed export](chapters/28.md#worked-example-1-two-observers-one-committed-export) |
| Listing L28-01 | Coordinate the two diagnostic reads | [Chapter 28 · Worked example 1: two observers, one committed export](chapters/28.md#worked-example-1-two-observers-one-committed-export) |
| Listing L28-02 | Two-worker success, redelivery and revoked release | [Chapter 28 · Inspect the complete trace](chapters/28.md#inspect-the-complete-trace) |
| Listing L28-03 | Event-controlled cancellation and cleanup | [Chapter 28 · Worked example 2: cancel a long-running fixture and inspect cleanup](chapters/28.md#worked-example-2-cancel-a-long-running-fixture-and-inspect-cleanup) |
| Listing L28-04 | Deterministic schedule, rollback, permissions and cleanup | [Chapter 28 · Repeatable tests and evidence](chapters/28.md#repeatable-tests-and-evidence) |
| Listing L29-01 | Supplied change for review | [Chapter 29 · 1. Manual review from entry point through data use and policy checks](chapters/29.md#1-manual-review-from-entry-point-through-data-use-and-policy-checks) |
| Unnumbered file | `examples/ch29/review-rule.yml` | [Chapter 29 · Two supplied static findings](chapters/29.md#two-supplied-static-findings) |
| Listing L29-02 | Inspect values at the suspect boundary | [Chapter 29 · Worked example 1: compare the warning with the actual argument type](chapters/29.md#worked-example-1-compare-the-warning-with-the-actual-argument-type) |
| Listing L29-03 | Trace visible output and committed worker state | [Chapter 29 · Worked example 2: one helper, two authorization regressions](chapters/29.md#worked-example-2-one-helper-two-authorization-regressions) |
| Listing L29-04 | Regression checks for the reviewed change | [Chapter 29 · Select regression checks that answer the claim](chapters/29.md#select-regression-checks-that-answer-the-claim) |
| Unnumbered file | `examples/ch30/requirements.txt` | [Chapter 30 · Starting state and laboratory files](chapters/30.md#starting-state-and-laboratory-files) |
| Listing L30-01 | JSON list adapter for the existing browser laboratory | [Chapter 30 · Add the HTTP boundary without replacing authorization](chapters/30.md#add-the-http-boundary-without-replacing-authorization) |
| Listing L30-02 | Fixture records, trusted relationships and expected rows | [Chapter 30 · Define fixture records and an independent oracle](chapters/30.md#define-fixture-records-and-an-independent-oracle) |
| Listing L30-03 | Generate two workspace records and a note collection | [Chapter 30 · Describe the input domain with strategies](chapters/30.md#describe-the-input-domain-with-strategies) |
| Listing L30-04 | HTTP contracts and the generated tenant-isolation property | [Chapter 30 · Exercise the property through Django](chapters/30.md#exercise-the-property-through-django) |
| Listing L30-05 | Find a small counterexample against the broken reader | [Chapter 30 · Shrink a failure without shrinking away the relationship](chapters/30.md#shrink-a-failure-without-shrinking-away-the-relationship) |
| Listing L30-06 | Supplied passive response metadata | [Chapter 30 · Worked example: present does not mean enforced](chapters/30.md#worked-example-present-does-not-mean-enforced) |
| Listing L30-07 | Compare normalized headers with the required policy | [Chapter 30 · Assert the required response policy](chapters/30.md#assert-the-required-response-policy) |
| Listing L30-08 | Local executable checks and an intentionally leaking reader | [Chapter 30 · Run the bounded checks and compare the independent controls](chapters/30.md#run-the-bounded-checks-and-compare-the-independent-controls) |
| Unnumbered file | `examples/ch31/tools.txt` | [Chapter 31 · Starting state and files](chapters/31.md#starting-state-and-files) |
| Listing L31-01 | Authored source fixtures for three local wheels | [Chapter 31 · Create the smallest source fixture](chapters/31.md#create-the-smallest-source-fixture) |
| Listing L31-02 | Compatibility and regression checks through the client | [Chapter 31 · Retain a useful application contract](chapters/31.md#retain-a-useful-application-contract) |
| Listing L31-03 | Offline sample build and evidence driver | [Chapter 31 · Build two environments and preserve negative results](chapters/31.md#build-two-environments-and-preserve-negative-results) |
| Listing L31-04 | Capture the installed sample and verify the artifact chain | [Chapter 31 · Worked example 1: follow the indirect package into installed code](chapters/31.md#worked-example-1-follow-the-indirect-package-into-installed-code) |
| Listing L31-05 | Fictional advisory with a reproducible local regression | [Chapter 31 · Worked example 2: compare the advisory range with the selected version](chapters/31.md#worked-example-2-compare-the-advisory-range-with-the-selected-version) |
| Listing L31-06 | Trace the installed parent edge and match the fictional range | [Chapter 31 · Worked example 2: compare the advisory range with the selected version](chapters/31.md#worked-example-2-compare-the-advisory-range-with-the-selected-version) |
| Unnumbered file | `examples/ch32/requirements.txt` | [Chapter 32 · Starting state and files](chapters/32.md#starting-state-and-files) |
| Listing L32-01 | Bound fixture records and a scoped exception example | [Chapter 32 · Define a normalized result without hiding its provenance](chapters/32.md#define-a-normalized-result-without-hiding-its-provenance) |
| Listing L32-02 | Explicit gate with default refusal for incomplete evidence | [Chapter 32 · Evaluate from the protected required set](chapters/32.md#evaluate-from-the-protected-required-set) |
| Listing L32-03 | One commit, one artifact and six evidence scenarios | [Chapter 32 · Worked example 2: tie an approved artifact to its commit](chapters/32.md#worked-example-2-tie-an-approved-artifact-to-its-commit) |
| Listing L32-04 | Sign a scoped approval and promote its exact digest | [Chapter 32 · Verify authority and bytes before copying](chapters/32.md#verify-authority-and-bytes-before-copying) |
| Listing L32-05 | Gate and signed-promotion regression tests | [Chapter 32 · Repeatable verification](chapters/32.md#repeatable-verification) |
| Unnumbered file | `examples/ch33/requirements.txt` | [Chapter 33 · Files and isolated setup](chapters/33.md#files-and-isolated-setup) |
| Listing L33-01 | Controlled event construction and single-record JSON encoding | [Chapter 33 · Choose severity for investigation, not accusation](chapters/33.md#choose-severity-for-investigation-not-accusation) |
| Listing L33-02 | Audit hooks in the copied queue transaction | [Chapter 33 · Put the audit append inside the business transaction](chapters/33.md#put-the-audit-append-inside-the-business-transaction) |
| Listing L33-03 | Audited service and worker facade | [Chapter 33 · Put the audit append inside the business transaction](chapters/33.md#put-the-audit-append-inside-the-business-transaction) |
| Listing L33-04 | Required outbox insert, bounded relay and local collector | [Chapter 33 · Store explicitly and keep delivery state separate from content](chapters/33.md#store-explicitly-and-keep-delivery-state-separate-from-content) |
| Listing L33-05 | Exact audit output and final state after failure | [Chapter 33 · Run the correlated denial and required-store failure](chapters/33.md#run-the-correlated-denial-and-required-store-failure) |
| Listing L33-06 | Redaction, rollback, delivery and release regressions | [Chapter 33 · Repeatable verification](chapters/33.md#repeatable-verification) |
| Unnumbered file | `examples/ch34/dashboard.json` | [Chapter 34 · The synthetic dashboard export](chapters/34.md#the-synthetic-dashboard-export) |
| Unnumbered file | `examples/ch34/triage.py` | [Chapter 34 · Calculate and classify](chapters/34.md#calculate-and-classify) |
| Unnumbered file | `examples/ch34/test_triage.py` | [Chapter 34 · Regression checks for decisions that could mislead a reviewer](chapters/34.md#regression-checks-for-decisions-that-could-mislead-a-reviewer) |
| Unnumbered file | `examples/ch35/Dockerfile` | [Chapter 35 · A parameterized build, with explicit external inputs](chapters/35.md#a-parameterized-build-with-explicit-external-inputs) |
| Unnumbered file | `examples/ch35/wsgi.py` | [Chapter 35 · A parameterized build, with explicit external inputs](chapters/35.md#a-parameterized-build-with-explicit-external-inputs) |
| Unnumbered file | `examples/ch35/compose.json` | [Chapter 35 · The reviewed container manifest](chapters/35.md#the-reviewed-container-manifest) |
| Unnumbered file | `examples/ch35/deployment.py` | [Chapter 35 · Host, scheme and identity are different claims](chapters/35.md#host-scheme-and-identity-are-different-claims) |
| Unnumbered file | `examples/ch35/settings_production.py` | [Chapter 35 · Host, scheme and identity are different claims](chapters/35.md#host-scheme-and-identity-are-different-claims) |
| Unnumbered file | `examples/ch35/nginx.conf` | [Chapter 35 · Worked example 2: who supplied `https`?](chapters/35.md#worked-example-2-who-supplied-https) |
| Unnumbered file | `examples/ch35/gunicorn.conf.py` | [Chapter 35 · Worked example 2: who supplied `https`?](chapters/35.md#worked-example-2-who-supplied-https) |
| Unnumbered file | `examples/ch35/probe_egress.py` | [Chapter 35 · Block an unnecessary connection with evidence](chapters/35.md#block-an-unnecessary-connection-with-evidence) |
| Unnumbered file | `examples/ch35/review_manifest.py` | [Chapter 35 · Reproduce the offline review](chapters/35.md#reproduce-the-offline-review) |
| Unnumbered file | `examples/ch35/test_review.py` | [Chapter 35 · Tests of the offline boundary](chapters/35.md#tests-of-the-offline-boundary) |
| Unnumbered file | `examples/ch35/check_django.py` | [Chapter 35 · Establish the runtime identity and loaded settings](chapters/35.md#establish-the-runtime-identity-and-loaded-settings) |
| Unnumbered file | `examples/ch36/timeline.json` | [Chapter 36 · Worked example 1: three redacted records become a UTC timeline](chapters/36.md#worked-example-1-three-redacted-records-become-a-utc-timeline) |
| Unnumbered file | `examples/ch36/timeline.py` | [Chapter 36 · Worked example 1: three redacted records become a UTC timeline](chapters/36.md#worked-example-1-three-redacted-records-become-a-utc-timeline) |
| Unnumbered file | `examples/ch36/known-backup-manifest.json` | [Chapter 36 · Worked example 2: compare the candidate with the known backup](chapters/36.md#worked-example-2-compare-the-candidate-with-the-known-backup) |
| Unnumbered file | `examples/ch36/incident_lab.py` | [Chapter 36 · Run the local response and recovery](chapters/36.md#run-the-local-response-and-recovery) |
| Unnumbered file | `examples/ch36/build_metadata.py` | [Chapter 36 · Separate cause, contributing authority and proof of repair](chapters/36.md#separate-cause-contributing-authority-and-proof-of-repair) |
| Unnumbered file | `examples/ch36/test_incident.py` | [Chapter 36 · Run regression checks that can change the decision](chapters/36.md#run-regression-checks-that-can-change-the-decision) |
| Unnumbered file | `examples/ch37/fixtures/literal_debug.py` | [Chapter 37 · Worked example 1: find the assignment in a supplied module](chapters/37.md#worked-example-1-find-the-assignment-in-a-supplied-module) |
| Unnumbered file | `examples/ch37/inspect_syntax.py` | [Chapter 37 · Worked example 2: the same name in a comment and an assignment](chapters/37.md#worked-example-2-the-same-name-in-a-comment-and-an-assignment) |
| Listing L06 | An AST visitor that reports a precise source location | [Chapter 37 · 2. AST visitors, aliases, scope and the limits of syntactic matching](chapters/37.md#2-ast-visitors-aliases-scope-and-the-limits-of-syntactic-matching) |
| Unnumbered file | `examples/ch37/fixtures/dynamic_debug.py` | [Chapter 37 · An example the rule cannot decide](chapters/37.md#an-example-the-rule-cannot-decide) |
| Unnumbered file | `examples/ch37/src/casebook_check/__init__.py` | [Chapter 37 · Turn functions into a small installable tool](chapters/37.md#turn-functions-into-a-small-installable-tool) |
| Unnumbered file | `examples/ch37/src/casebook_check/cli.py` | [Chapter 37 · Give the command a predictable protocol](chapters/37.md#give-the-command-a-predictable-protocol) |
| Unnumbered file | `examples/ch37/src/casebook_check/__main__.py` | [Chapter 37 · Give the command a predictable protocol](chapters/37.md#give-the-command-a-predictable-protocol) |
| Unnumbered file | `examples/ch37/pyproject.toml` | [Chapter 37 · Give the command a predictable protocol](chapters/37.md#give-the-command-a-predictable-protocol) |
| Unnumbered file | `examples/ch37/verify_wheel.py` | [Chapter 37 · Build and inspect the wheel](chapters/37.md#build-and-inspect-the-wheel) |
| Unnumbered file | `examples/ch37/verify_install.py` | [Chapter 37 · Install the wheel and test the entry points](chapters/37.md#install-the-wheel-and-test-the-entry-points) |
| Unnumbered file | `examples/ch37/tests/test_checker.py` | [Chapter 37 · Tests should challenge the rule boundary](chapters/37.md#tests-should-challenge-the-rule-boundary) |
| Unnumbered file | `examples/ch37/README.md` | [Chapter 37 · Give another engineer a usable README](chapters/37.md#give-another-engineer-a-usable-readme) |
| Unnumbered file | `examples/ch38/reports/local.json` | [Chapter 38 · The saved chapter 37 report](chapters/38.md#the-saved-chapter-37-report) |
| Unnumbered file | `examples/ch38/reports/second.sarif` | [Chapter 38 · The second report and the supported SARIF subset](chapters/38.md#the-second-report-and-the-supported-sarif-subset) |
| Unnumbered file | `examples/ch38/catalog.json` | [Chapter 38 · Context and bindings for this exercise](chapters/38.md#context-and-bindings-for-this-exercise) |
| Unnumbered file | `examples/ch38/prior.json` | [Chapter 38 · Suppression is a recorded decision, not disappearance](chapters/38.md#suppression-is-a-recorded-decision-not-disappearance) |
| Unnumbered file | `examples/ch38/queue_review.py` | [Chapter 38 · The executable merge and publication](chapters/38.md#the-executable-merge-and-publication) |
| Unnumbered file | `examples/ch38/test_queue_review.py` | [Chapter 38 · Test the decisions and the failure state](chapters/38.md#test-the-decisions-and-the-failure-state) |
| Unnumbered file | `examples/ch39/policy.json` | [Chapter 39 · A synthetic policy you can inspect](chapters/39.md#a-synthetic-policy-you-can-inspect) |
| Unnumbered file | `examples/ch39/workload_policy.py` | [Chapter 39 · A synthetic policy you can inspect](chapters/39.md#a-synthetic-policy-you-can-inspect) |
| Unnumbered file | `examples/ch39/grant_lab.py` | [Chapter 39 · Complete local laboratory](chapters/39.md#complete-local-laboratory) |
| Unnumbered file | `examples/ch39/test_cloud.py` | [Chapter 39 · Test the boundaries](chapters/39.md#test-the-boundaries) |
| Unnumbered file | `examples/ch40/release.json` | [Chapter 40 · Check the records without pretending to assess the risk automatically](chapters/40.md#check-the-records-without-pretending-to-assess-the-risk-automatically) |
| Unnumbered file | `examples/ch40/metrics.json` | [Chapter 40 · Worked example: four overdue items in each team](chapters/40.md#worked-example-four-overdue-items-in-each-team) |
| Unnumbered file | `examples/ch40/program_review.py` | [Chapter 40 · Execute the arithmetic and record checks](chapters/40.md#execute-the-arithmetic-and-record-checks) |
| Unnumbered file | `examples/ch40/test_program_review.py` | [Chapter 40 · Regression checks for the review routine](chapters/40.md#regression-checks-for-the-review-routine) |
| Unnumbered file | `examples/ch42/requirements.txt` | [Chapter 42 · What the patch contains](chapters/42.md#what-the-patch-contains) |
| Listing L42-01 | Admission, worker publication, release and lifecycle units | [Chapter 42 · The complete local service](chapters/42.md#the-complete-local-service) |
| Listing L42-02 | Independent disposable fixture keyrings | [Chapter 42 · Keep purpose and workspace keys separate](chapters/42.md#keep-purpose-and-workspace-keys-separate) |
| Listing L42-03 | Two deliveries of the same durable request | [Chapter 42 · Coordinate the dangerous schedule](chapters/42.md#coordinate-the-dangerous-schedule) |
| Listing L42-04 | Synthetic end-to-end traces with final-state checks | [Chapter 42 · Run all three increments](chapters/42.md#run-all-three-increments) |
| Listing L42-05 | Core verification against stored state | [Chapter 42 · Test the implemented boundaries](chapters/42.md#test-the-implemented-boundaries) |
| Unnumbered file | `examples/ch42/requirements-web.txt` | [Chapter 42 · Supply the HTTP integration seam without inventing authentication](chapters/42.md#supply-the-http-integration-seam-without-inventing-authentication) |
| Listing L42-06 | Optional Django session/CSRF adapter | [Chapter 42 · Supply the HTTP integration seam without inventing authentication](chapters/42.md#supply-the-http-integration-seam-without-inventing-authentication) |
| Listing L42-07 | Optional HTTP tests with explicit missing-dependency status | [Chapter 42 · Supply the HTTP integration seam without inventing authentication](chapters/42.md#supply-the-http-integration-seam-without-inventing-authentication) |
| Listing L43-01 | Committed-source archive and extracted-candidate collector | [Chapter 43 · Build and exercise the identified source artifact](chapters/43.md#build-and-exercise-the-identified-source-artifact) |
| Listing L43-02 | Evidence consistency without pretending to approve release | [Chapter 43 · Verify the local links](chapters/43.md#verify-the-local-links) |
| Unnumbered file | `examples/ch44/requirements.txt` | [Chapter 44 · The subject and starting state](chapters/44.md#the-subject-and-starting-state) |
| Listing L44-01 | Read the bounded, synthetic timeline fixture | [Chapter 44 · Worked example 1: rebuild the UTC timeline](chapters/44.md#worked-example-1-rebuild-the-utc-timeline) |
| Listing L44-02 | Retention detection, isolated restore and controlled retests | [Chapter 44 · The complete rehearsal](chapters/44.md#the-complete-rehearsal) |
| Listing L44-03 | State, timeline, boundary and recovery assertions | [Chapter 44 · Repeatable recovery tests](chapters/44.md#repeatable-recovery-tests) |
| Unnumbered file | `examples/appendices/values.py` | [Appendix · Form 1: compare two values](appendices.md#form-1-compare-two-values) |
| Unnumbered file | `examples/appendices/rules.py` | [Appendix · Form 2: give the decision a name](appendices.md#form-2-give-the-decision-a-name) |
| Unnumbered file | `examples/appendices/checks.py` | [Appendix · Form 3: check a change over time](appendices.md#form-3-check-a-change-over-time) |
| Unnumbered file | `examples/appendices/notebook_demo.py` | [Appendix · A worked notebook entry: revoke, then read](appendices.md#a-worked-notebook-entry-revoke-then-read) |
