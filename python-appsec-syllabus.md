# Python for Application Security Engineers

**From your first Python program to the security review of a running service**

A private note belongs to one workspace. Who can read it? What happens after a member leaves? How would an engineer prove that the rule still works after a release? This book follows those questions from a few lines of Python to a working web application.

**Edition baseline** · CPython 3.12.14 · 27 November 2026

**Reader** · First-time programmers and engineers entering AppSec  
**Manuscript** · English Markdown

## Preface and reader's guide

Application security, or **AppSec**, is the work of making software protect the people and data that depend on it. You will learn Python by building **Casebook**, a small service for private team notes. In chapter 04 you can already make a simple access decision. In chapter 23 the same decision must hold across a page, an API response and a queued export.

### Where to begin

| If this describes you | Start here | Check before moving on |
| --- | --- | --- |
| This is my first program. | Read 01–12 in order. Use the platform-specific setup in 02. | Trace a decision on paper, then write and run a test for it. |
| I write code in another language. | Try the checkpoints for 04, 08 and 12. Read any chapters that explain a missed result. | Explain Python's truth values, shared state, imports and exceptions. |
| I know Python and am new to security. | Start at 13. Use the Python index when an example uses unfamiliar syntax. | Trace one request from the client to storage and identify who owns each check. |

You need a computer on which you can run Python, a text editor and permission to create local project files. Chapter 01 can be read and traced on paper. Chapter 02 covers installation. Internet access is useful for downloads. Core exercises use local data, test accounts and recorded responses. The cloud design exercise uses a policy document, so a paid account is optional.

### What you will be able to do

1. Write and test a Python program that turns imperfect input into useful records.
2. Design, implement and review security controls for a Python web service.
3. Read a tool finding, assess its effect and prove that a change fixes the issue.
4. Make a release decision and hand a colleague the evidence to check it.
5. Investigate a service incident and show that recovery restored the intended protections.

**Reading in a second language.** Read the question above a listing. Predict one result. Run it and explain the result in your own words. The glossary gives short definitions. Keep the English API spelling beside a translation in your notes so you can find the term in documentation.

## The running project

In **Casebook**, Alpha and Beta are separate customer workspaces. Mina is an Alpha member, Ravi is a Beta member and Lee manages Alpha. An anonymous visitor has no account. A worker builds exports in the background. All names, records and events in the exercises are fictional.

| Stage | What the reader builds | What the reader can inspect |
| --- | --- | --- |
| First scripts · 01–12 | A membership rule and note-file reader | Printed decisions, records and a test result |
| System boundaries · 13–20 | A local CLI, a database and the first web routes | Exit codes, stored rows and response contracts |
| Product controls · 21–28 | Login, private notes, attachments and a worker | Permission checks, limits and final database state |
| Verification and operations · 29–40 | A release gate, audit trail and review tool | Test reports, events and a prioritized queue |
| Independent review · 41–44 | A private workspace export | A decision record another engineer can verify |

**Recurring rule.** At the time of each read, the reader must be an active member of the note's workspace. A workspace manager has authority inside their own workspace. A queued export must check authorization again before it releases private data. Chapters 41–44 extend the rule to a new feature.

### How the manuscript is organized

Each chapter entry in this syllabus names a result, four sections, two example ideas and a practical check. The full chapter will add runnable listings, expected output, a guided exercise, independent practice, common mistakes and answers. Chapter numbers serve as stable locators while the manuscript is being written.

**Edition note.** The language baseline is the tested **CPython 3.12.14** runtime. Web examples use **Django 6.1.3** on Python 3.12. The tested environment also pins pytest 9.2.0, mypy 2.4.1, PyJWT 2.15.1, Hypothesis 6.170.17 and cryptography 50.0.2. Use [the version record](tested-versions.md) and [tested requirements](requirements-tested.txt); browser, provider and production evidence remains separate. [Python release record](https://www.python.org/downloads/release/python-31214/) · [Django release record](https://docs.djangoproject.com/en/6.1/releases/6.1.3/)

## Contents

[Preface](#preface-and-readers-guide) · [Running project](#the-running-project) · [Lists of figures, tables and listings](#lists-of-figures-tables-and-code-listings) · [Practice and assessment](#practice-and-assessment)

**Part I · First steps in Python**

- [01 · Your first program][ch-01]
- [02 · Set up a workbench you can rebuild][ch-02]
- [03 · Values, names and expressions][ch-03]
- [04 · Decisions and repetition][ch-04]

**Part II · Give data a shape**

- [05 · Collections and shared state][ch-05]
- [06 · Functions, modules and interfaces][ch-06]
- [07 · Text, bytes and patterns][ch-07]
- [08 · Files and structured records][ch-08]

**Part III · Write code another person can trust**

- [09 · Errors, debugging and cleanup][ch-09]
- [10 · Types, classes and domain models][ch-10]
- [11 · Iteration, decorators and bounded work][ch-11]
- [12 · Repeatable tests and a reviewable change][ch-12]

**Part IV · Python at system boundaries**

- [13 · Processes, settings and secrets][ch-13]
- [14 · Command-line tools and child processes][ch-14]
- [15 · Relational data and transactions][ch-15]
- [16 · Networks, HTTP and TLS][ch-16]

**Part V · Design a small web application**

- [17 · Draw the system and its trust boundaries][ch-17]
- [18 · Security requirements and private data][ch-18]
- [19 · Build the Casebook web service][ch-19]
- [20 · API contracts and business rules][ch-20]

**Part VI · Identity, permissions and the browser**

- [21 · Accounts, passwords and recovery][ch-21]
- [22 · Sessions, tokens and federated identity][ch-22]
- [23 · Authorization and tenant isolation][ch-23]
- [24 · Templates, cookies and the browser][ch-24]

**Part VII · Files, services and concurrent work**

- [25 · Uploads, archives and serialization][ch-25]
- [26 · Outbound requests and integrations][ch-26]
- [27 · Cryptographic choices and key management][ch-27]
- [28 · Concurrency, queues and resource limits][ch-28]

**Part VIII · Review, verification and release**

- [29 · Review Python changes and interpret static findings][ch-29]
- [30 · Verify controls in running code][ch-30]
- [31 · Dependencies and the software supply chain][ch-31]
- [32 · CI checks and release evidence][ch-32]

**Part IX · Operate and recover a service**

- [33 · Security logs and audit history][ch-33]
- [34 · Metrics, traces and alert triage][ch-34]
- [35 · Deployment, containers and infrastructure settings][ch-35]
- [36 · Incident response, disclosure and recovery][ch-36]

**Part X · Build tools and lead reviews**

- [37 · Build a Python source-review tool][ch-37]
- [38 · Normalize findings and prioritize work][ch-38]
- [39 · Cloud identity and service boundaries][ch-39]
- [40 · Run an application security program][ch-40]

**Part XI · Capstone • A private workspace export**

- [41 · Capstone I • Define a private export][ch-41]
- [42 · Capstone II • Implement the controls][ch-42]
- [43 · Capstone III • Review and release][ch-43]
- [44 · Capstone IV • Operate, respond and hand over][ch-44]

### Back matter

[Appendix A · Sample listings](#appendix-a-a-small-rule-three-ways-to-read-it) · [Appendix B · Python reference shelf](#appendix-b-a-reference-shelf-for-python) · [Appendix C · Lab notebook and answer key](#appendix-c-lab-notebook-and-answer-key) · [Appendix D · Standards map](#appendix-d-standards-and-verification-map) · [Glossary](#glossary) · [Subject index](#subject-index) · [Python and tools index](#python-and-tools-index) · [Bibliography](#bibliography-and-edition-records)

## Lists of figures, tables and code listings

These are planned exhibits for the manuscript. Their identifiers stay stable when pagination changes. Chapter links open the relevant brief.

| Figure | What it will show | Chapter |
| --- | --- | --- |
| F01 | Where the shell hands a file to the interpreter | [02][ch-02] |
| F02 | The path of a note through Casebook's trust boundaries | [17][ch-17] |
| F03 | The separate browser, application and identity provider in sign-in | [22][ch-22] |
| F04 | A queued export with a permission change before delivery | [28][ch-28] |
| F05 | The path from reviewed commit to deployed artifact | [32][ch-32] |
| F06 | The events that establish the recovery timeline | [36][ch-36] |

| Table | What the reader will compare | Chapter |
| --- | --- | --- |
| T01 | Values before and after each decision | [04][ch-04] |
| T02 | A missing field, an empty string and a valid value | [08][ch-08] |
| T03 | Subjects, actions and objects in two workspaces | [23][ch-23] |
| T04 | What escaping, CSRF checks, CORS and CSP each control | [24][ch-24] |
| T05 | Hashing, message authentication, signatures and encryption | [27][ch-27] |
| T06 | Severity, exposure and ownership in a remediation queue | [38][ch-38] |

| Listing | What the code will demonstrate | Chapter |
| --- | --- | --- |
| L01 | A decision with an explicit default | [04][ch-04] |
| L02 | A streaming multilingual record reader | [08][ch-08] |
| L03 | A query with bound values and a workspace filter | [15][ch-15] |
| L04 | A permission-scoped query reused by two views | [23][ch-23] |
| L05 | An idempotent job with a database constraint | [28][ch-28] |
| L06 | An AST visitor that reports a precise source location | [37][ch-37] |

## Practice and assessment

**Study rhythm.** Treat a chapter as two sessions. In the first, read the model, trace the examples and write down a prediction. In the second, rebuild the main example from a blank file, change one condition and complete the practical check. Move on when you can explain the result without reading the answer. A design chapter uses a diagram, decision table or review note in place of a program.

| Milestone | Independent task | Evidence to keep |
| --- | --- | --- |
| After 12 | Add an unknown-role case to the membership rule. | A short diff, the expected answer and a repeatable test |
| After 20 | Add a title filter to the note inventory. | A parameterized query, a scoped result and an API contract |
| After 28 | Revoke a member while their export is queued. | The decisions at request and delivery, plus final stored state |
| After 36 | Decide whether to release an update after a failed audit check. | Release decision, matched events and a recovery check |
| After 40 | Hand another team a prioritized remediation queue. | Source references, deduplication decisions, owners and due dates |

### Capstone marking guide

| Area | Points | Evidence for full credit |
| --- | ---: | --- |
| Design | 20 | A reviewer can trace each privacy rule to a boundary, owner and check. |
| Implementation | 30 | Two workspaces remain isolated across reads and exports, including after revocation. |
| Verification | 25 | Tests cover ordinary use, denial, expiry, duplicate work and a failed dependency. |
| Release and recovery | 15 | The decision identifies the build, outstanding risks and a verified recovery step. |
| Handover | 10 | A colleague can repeat the checks and tell who owns each open item. |

The suggested pass mark is 80/100. An export that leaks a note across workspaces or remains available to a revoked member needs correction and a retest before the capstone passes. The chapter author provides hints and worked solutions for self-study. A reader can compare evidence against this rubric without an instructor.

## Part I. First steps in Python

Start with a three-line program and finish with a decision you can trace on paper.

### 01. Your first program

**Goal.** Make Python display a decision you can check by hand.

1. What a program does with input, steps and output
2. What runs a Python instruction and what a saved script contains
3. How to read a line of code, a string and a function call
4. What application security protects when a note is private

**Worked examples.** Print a note title and predict each character on screen. Change one quoted word and compare both runs.

**Practice check.** Label the input, instruction and output on a three-line example. Explain who should see a private note.

### 02. Set up a workbench you can rebuild

**Goal.** Run the same saved file twice from the intended Python environment.

1. Install CPython on Windows, macOS or Linux and locate the launcher
2. Distinguish the terminal, shell, editor and interactive Python prompt
3. Navigate folders, create a virtual environment and inspect the executable
4. Install Git if needed, start a local history and exclude generated files

**Worked examples.** Read the interpreter version from inside a script. Compare two interpreter paths when a package appears to be missing.

**Practice check.** Close the terminal, reopen the project and run the file again. Record the executable path, version and one clean Git commit.

### 03. Values, names and expressions

**Goal.** Represent a missing value, a count and a yes-or-no decision accurately.

1. Assignment, readable names, comments and indentation
2. Integers, floats, booleans, strings and `None`
3. Arithmetic, comparisons, equality and identity
4. Conversion, f-strings and the difference between a printed and a returned value

**Worked examples.** Compare the text "0" with the number 0. Calculate the remaining places in a three-note quota.

**Practice check.** Predict five expression results before running them. Explain why a missing count and a count of zero lead to different decisions.

### 04. Decisions and repetition

**Goal.** Trace the exact line that makes an access decision.

1. Boolean expressions and short-circuit evaluation
2. `if`, `elif` and `else` with an explicit default
3. `for` and `while` loops, `range`, `break` and `continue`
4. Trace tables, empty inputs and off-by-one boundaries

**Worked examples.** Decide whether a signed-in member belongs to a workspace. Trace the last admitted note at a quota boundary.

**Practice check.** Write a program that prints an answer for a member, a visitor and an unknown role. Compare the three lines with a handwritten decision table.

**Part checkpoint.** Run a saved script and correctly predict all three decisions in chapter 04.

## Part II. Give data a shape

Use collections, functions, text and files to turn notes into records.

### 05. Collections and shared state

**Goal.** Choose a collection that keeps the information a decision needs.

1. Lists, tuples, sets and dictionaries
2. Indexing, slicing, membership and lookup defaults
3. Mutation, copying, aliasing and nested values
4. Comprehensions, sorting and predictable output

**Worked examples.** Remove duplicate role names while counting memberships. Trace how two names for the same list can change two users' apparent roles.

**Practice check.** Group six synthetic notes by workspace. Check that adding a role to one user's collection leaves another user's roles intact.

### 06. Functions, modules and interfaces

**Goal.** Turn a rule into a reusable function with a clear contract.

1. Function signatures, arguments, return values and scope
2. Defaults, keyword-only parameters and mutable default traps
3. Pure decisions, side effects and explicit dependencies
4. Import paths, packages, the main guard and module shadowing

**Worked examples.** Extract a membership check from a printing loop. Import a local rules module and explain when its top-level lines run.

**Practice check.** Use one function from two small scripts. Call it twice with different users and show that the first call leaves no state behind.

### 07. Text, bytes and patterns

**Goal.** Follow a value from bytes on disk to readable text.

1. Unicode code points, UTF-8 and explicit encoding boundaries
2. Length in bytes and characters, normalization and identifier policy
3. String methods, splitting and joining
4. Regular expressions, full matches, raw strings and bounded inputs

**Worked examples.** Measure a Persian note title in characters and UTF-8 bytes. Parse a short ASCII workspace code with a bounded pattern.

**Practice check.** Read three identifiers under a written naming policy. For each one, show the accepted value or a clear rejection reason.

### 08. Files and structured records

**Goal.** Read, check and write a small collection of notes.

1. Relative and absolute paths with `pathlib`
2. Streaming files and closing them with a `with` block
3. JSON objects, arrays and types, CSV rows and quoting
4. Missing keys, empty files, schemas and explicit encodings

**Worked examples.** Read a UTF-8 note from a relative path. Import a CSV row whose quoted title contains a comma.

**Practice check.** Convert a fixture file into a JSON summary. Predict its row count, preserve its non-English title and explain what happens to a row with a missing field.

**Part checkpoint.** Import a multilingual note inventory and explain one rejected record.

## Part III. Write code another person can trust

Model data, handle failure and make repeated checks inexpensive.

### 09. Errors, debugging and cleanup

**Goal.** Explain a failure and leave the program in a known state.

1. Reading syntax errors and tracebacks from the last line upward
2. Narrow exception handlers, `raise` and exception chaining
3. Resource ownership, `finally` and context managers
4. Breakpoints, small reproductions of ordinary bugs and public error messages

**Worked examples.** Read a traceback from a missing settings file. Compare a malformed JSON record with a genuine file permission error.

**Practice check.** Handle two expected errors with distinct messages. Confirm that an unexpected programming error is still visible to the developer.

### 10. Types, classes and domain models

**Goal.** Make an invalid note state easy to spot in code review.

1. Type hints for collections, unions and optional values
2. Classes, instances, attributes and methods
3. Dataclasses, enums, composition and small interfaces
4. Static type checking, runtime validation and representation of sensitive fields

**Worked examples.** Model a note draft as a dataclass. Trace an optional owner ID from a parser through a type checker to a runtime check.

**Practice check.** Design a note state model and check one allowed transition. Demonstrate where an invalid external value is rejected.

### 11. Iteration, decorators and bounded work

**Goal.** Read common Python patterns found in service and tooling code.

1. Iterables, iterators, `yield` and lazy evaluation
2. Generator expressions, batching and stopping early
3. First-class functions, closures, decorators and `functools.wraps`
4. Choosing an ordinary function, a wrapper or a context manager

**Worked examples.** Count records without loading an entire file. Wrap a function with a timer that records duration without recording its arguments.

**Practice check.** Process only the first three records from a long input. Explain when each record is read and verify the wrapper preserves the function name.

### 12. Repeatable tests and a reviewable change

**Goal.** Turn a rule into a regression test another reader can run.

1. Arrange, act and assert with pytest
2. Fixtures, parametrization, temporary directories and exception checks
3. Unit and integration tests, test doubles and deterministic time
4. Git diff, branches, review comments and a small test-first change

**Worked examples.** Test the same membership rule across three roles. Replace a clock in an expiry test so the test has one stable answer.

**Practice check.** Submit a local diff for a quota boundary. Show the failing assertion before the correction and the passing command afterward.

**Part checkpoint.** Give a reviewer a patch and a deterministic test for the rule it changes.

## Part IV. Python at system boundaries

Follow data as it crosses into a process, a database or an HTTP response.

### 13. Processes, settings and secrets

**Goal.** Start a program with known settings and keep credentials out of its output.

1. Processes, environment inheritance and working directories
2. Configuration precedence, typed settings and startup validation
3. Secret stores, least privilege, rotation and development fixtures
4. Public diagnostics, redaction and configuration drift

**Worked examples.** Parse an environment value that contains the text "false". Check a missing service credential using a synthetic value in tests.

**Practice check.** Build a settings loader. Verify that a missing required setting stops startup and that its error names the setting without printing its value.

### 14. Command-line tools and child processes

**Goal.** Give a local tool a predictable input and error contract.

1. `argparse` subcommands, help and arguments
2. Standard input, standard output, standard error and exit codes
3. `subprocess` argument lists, executable selection and environment scope
4. Timeouts, output budgets, temporary files and cleanup

**Worked examples.** Write a note-count command whose output can feed another program. Pass a file name containing spaces as a single argument to a fixed helper.

**Practice check.** Deliver a CLI with documented success, input-error and timeout results. Check the exit code and both output streams in a test.

### 15. Relational data and transactions

**Goal.** Protect the meaning of a record when the database changes.

1. Tables, rows, keys, constraints and basic SQL
2. Parameter binding, identifiers and allowlisted query options
3. Joins, workspace filters and indexes
4. Transactions, rollback, migrations and the limits of SQLite demonstrations

**Worked examples.** Store the name O’Connor using a bound parameter. Roll back a note creation when its required audit row cannot be written.

**Practice check.** Write tests for workspace-scoped reads and an all-or-nothing update. Inspect the stored rows after both success and failure.

### 16. Networks, HTTP and TLS

**Goal.** Read a request and explain each decision a client makes.

1. Hosts, IP addresses, DNS, ports and TCP connections
2. HTTP methods, URLs, headers, status codes, bodies and media types
3. TLS certificate trust, hostnames and the client/server boundary
4. Time budgets, pagination, caching and error handling in Python clients

**Worked examples.** Read a recorded successful response and an empty response. Use a stub transport to see how a client reacts to a timeout.

**Practice check.** Annotate a recorded exchange and implement a bounded client for a fixed endpoint. Check timeout and unexpected content-type behavior.

**Part checkpoint.** Create a CLI, check its exit contract and explain where its inputs come from.

## Part V. Design a small web application

Identify users and data before building the first Django routes.

### 17. Draw the system and its trust boundaries

**Goal.** Explain where a private note travels and who can change it.

1. Assets, actors, data stores and entry points
2. Data-flow diagrams and trust boundaries
3. Threat modeling, assumptions and ordinary failure scenarios
4. Compare design options and record the owner of each control

**Worked examples.** Trace a note from browser to service to database. Explore what changes when a background worker handles an export.

**Practice check.** Draw the current design. Mark two boundaries and give each one an assumption, a risk, a control and a way to check the control.

### 18. Security requirements and private data

**Goal.** Translate a user's expectation into a measurable engineering requirement.

1. Confidentiality, integrity and availability in product language
2. Likelihood, impact, uncertainty and risk ownership
3. Data inventory, purpose, minimization, retention and deletion
4. Turn a design decision into an acceptance criterion and ASVS evidence

**Worked examples.** Turn “notes are private” into a two-workspace test. Decide which fields a support export needs and specify when they expire.

**Practice check.** Produce three requirements. Give each one a data owner, an observable result and a review date, including one deletion requirement.

### 19. Build the Casebook web service

**Goal.** Follow one request through a small Django application.

1. Project, application, settings, URL routes and views
2. Request and response objects, middleware order and validation points
3. Models, migrations, the object-relational mapper and request-scoped queries
4. Development settings, the Django test client and a private default

**Worked examples.** Serve a public health response and inspect its media type. Store a note through the ORM and check that its private contents have no public route.

**Practice check.** Create the health endpoint and seed two workspaces. Prove that an anonymous visitor can see health status and cannot read note content.

### 20. API contracts and business rules

**Goal.** Specify which inputs an endpoint accepts and which state changes it permits.

1. JSON request and response schemas, methods and status codes
2. Required, optional, unknown and server-owned fields
3. State machines, idempotency and replayed business operations
4. Pagination caps, API versioning, deprecation and inventory

**Worked examples.** Allow a client to set a title while the service sets the owner. Apply the same export request twice under one idempotency key.

**Practice check.** Specify who may update a note in the contract. Use a fixture identity for this exercise. Check an unknown field, an invalid transition and a repeated request against the expected record state.

**Part checkpoint.** Trace one privacy requirement from the diagram to an API contract.

## Part VI. Identity, permissions and the browser

Decide who a user is, what they may do and what a browser will enforce.

### 21. Accounts, passwords and recovery

**Goal.** Design sign-in and account recovery around the life of an account.

1. Registration, identity proofing assumptions and enumeration-resistant responses
2. Password hashing, salts, work factors and library-managed upgrades
3. Multi-factor authentication, passkeys and recovery options
4. Reauthentication, throttling, reset tokens and revocation

**Worked examples.** Use Django's password API to set and verify a synthetic password. Compare reset responses for a known and an unknown fixture account.

**Practice check.** Draw the recovery flow. Test expiry, single use and a stable public response, then describe what support staff may observe.

### 22. Sessions, tokens and federated identity

**Goal.** Choose an identity mechanism and explain its validation path.

1. Server-side sessions, cookie flags, rotation and logout
2. Opaque tokens, token storage and lifetime
3. OAuth 2.0 authorization and OpenID Connect identity, code flow and PKCE
4. JWT validation with maintained libraries, issuer, audience, expiry and key rotation

**Worked examples.** Trace a browser login through session rotation. Evaluate supplied token claims against a fixed issuer and audience policy.

**Practice check.** Write a decision record for browser sessions and a partner integration. Test expiry and the wrong audience using local fixtures and a configured verifier.

### 23. Authorization and tenant isolation

**Goal.** Enforce the same access rule across every way to reach a note.

1. Subjects, actions, objects, tenants and deny-by-default decisions
2. Roles, attributes, ownership and a permission matrix
3. Object-, field- and function-level checks in query and service layers
4. Admin actions, background jobs, caches and permission revocation

**Worked examples.** Let a member read an Alpha note while a Beta member receives the agreed denial. Remove a private field from an otherwise permitted response.

**Practice check.** Build a role-by-action test table for list, detail and export. Also prove that a revoked member loses access when the next request is handled.

### 24. Templates, cookies and the browser

**Goal.** Connect a server response to the security rules a browser applies.

1. HTML, templates, context-sensitive encoding and cross-site scripting (XSS)
2. Origins, the same-origin policy and cross-origin resource sharing (CORS)
3. Cookies, cross-site request forgery (CSRF) and framework checks
4. Content Security Policy (CSP), framing policy, caching and browser evidence

**Worked examples.** Render a title containing A & B and inspect the HTML and visible text. Check a cookie-authenticated form using Django's CSRF-enforcing test client.

**Practice check.** Write one browser-facing check for rendering and one for a state change. Explain which CORS setting, cookie setting and CSRF check affect each case.

**Part checkpoint.** Use two workspaces to test login, object access, rendering and a state change.

## Part VII. Files, services and concurrent work

Keep a rule true when work crosses a storage, network or worker boundary.

### 25. Uploads, archives and serialization

**Goal.** Accept an attachment while keeping its name, size and storage under application control.

1. Media types, file signatures and separate display and storage names
2. Path traversal prevention, symlinks, permissions and isolated storage
3. Archive entry policy, expansion budgets and cleanup on rejection
4. JSON, XML, YAML and pickle trust assumptions when rebuilding objects

**Worked examples.** Store two reports with the same display name under different internal keys. Read a supplied archive manifest and decide which entries meet a documented policy.

**Practice check.** Implement an attachment policy against synthetic files. Verify the size boundary, independent storage names, private retrieval and cleanup after rejection.

### 26. Outbound requests and integrations

**Goal.** Constrain where a service sends data and what it accepts back.

1. Server-side request forgery (SSRF) as a design risk and fixed destination registries
2. URL parsing, redirects, DNS changes and network egress policy
3. Verified TLS, timeouts, response limits and partner schema validation
4. Webhook authenticity, timestamp windows, duplicate delivery and secret rotation

**Worked examples.** Select a partner endpoint from a registry by ID. Feed a worker a repeated synthetic event and show that its business effect occurs once.

**Practice check.** Use a fake transport to check a refused redirect, an oversized reply and a duplicate webhook. State which boundary still requires network enforcement.

### 27. Cryptographic choices and key management

**Goal.** Select a standard tool for a named protection goal.

1. Randomness for identifiers and tokens with secrets
2. Digests, keyed message authentication codes (HMACs) and digital signatures
3. Authenticated encryption, associated data and nonce requirements
4. Key custody, separation, rotation, backup and algorithm migration

**Worked examples.** Compare a file digest with an authenticated message tag. Open a synthetic encrypted record with a maintained high-level library and handle verification failure.

**Practice check.** Specify how to verify a webhook and how to protect a stored export. Document key ownership and test a key change using dummy keys.

### 28. Concurrency, queues and resource limits

**Goal.** Keep a business rule true when two tasks run at the same time.

1. Threads, processes, `asyncio`, `await` and cancellation
2. Races, locks, database constraints and transaction boundaries
3. Queues, retries, idempotency and backpressure
4. Limits on time, bytes, parallel work and requests per tenant

**Worked examples.** Run two workers that claim the same export and observe the final database state. Cancel a long-running fixture task and check its cleanup.

**Practice check.** Write a deterministic two-worker test for one export per request. Name the database guarantee, the worker retry rule and the cleanup owner.

**Part checkpoint.** Justify a storage limit, a destination policy, a key choice and a retry rule.

## Part VIII. Review, verification and release

Support each release decision with a check and evidence of what ran.

### 29. Review Python changes and interpret static findings

**Goal.** Translate a suspicious code path into a precise review comment.

1. Manual review from entry point through data use and policy checks
2. Static application security testing (SAST), rule scope and taint-flow vocabulary
3. Reading Bandit and Semgrep findings against reviewed Python source
4. Confidence, false positives, fixes and regression coverage

**Worked examples.** Compare a rule finding with the actual argument type at its call site. Review an access-control change that affects a list view and an export worker.

**Practice check.** Write two review comments on a supplied diff. Give each a location, a concrete consequence, a correction and a test or a reason to close it.

### 30. Verify controls in running code

**Goal.** Choose evidence that answers a specific security question.

1. Integration and contract tests with Django's test client
2. Property-based checks with Hypothesis, generators and shrinking
3. Dynamic and interactive application security testing (DAST and IAST), coverage and limits
4. Read supplied passive reports and connect observations to requirements

**Worked examples.** Generate collections of notes and verify that every returned note belongs to the requested workspace. Compare a passive header observation with an asserted response policy.

**Practice check.** Build a verification matrix for three controls. Include a test result, one passive observation and one explicitly uncovered behavior.

### 31. Dependencies and the software supply chain

**Goal.** Find what ships and decide which dependency update matters.

1. Direct and transitive dependencies, build backends, wheels and source distributions
2. Pins, constraints, hashes, index selection and isolated builds
3. Software bill of materials (SBOM), advisory matching and software composition analysis (SCA)
4. Maintainer trust, provenance, reachability, update testing and rollback

**Worked examples.** Read a dependency tree and discover why an indirect package ships. Compare a supplied advisory's affected range with a locked version.

**Practice check.** Produce an inventory for a sample build. Link one update decision to an advisory, a compatibility test and an owner.

### 32. CI checks and release evidence

**Goal.** Turn a local security check into a repeatable release decision.

1. Continuous integration (CI), clean environments and reproducible commands
2. Jobs, artifacts, minimum token permissions and untrusted change boundaries
3. Combine tests, static analysis, dependency and secret-scan results
4. Gate policy, expiring exceptions, artifact signing and promotion by digest

**Worked examples.** Read a pipeline summary where one job never ran. Tie an approved artifact digest to its reviewed commit.

**Practice check.** Design a release gate with pass, fail and missing-result cases. Demonstrate that a skipped required job cannot produce an approval.

**Part checkpoint.** Trace a finding to a code change, a regression test and a release gate.

## Part IX. Operate and recover a service

Use events and configuration evidence to diagnose a problem and verify recovery.

### 33. Security logs and audit history

**Goal.** Record enough detail to investigate an action while protecting private data.

1. Structured events, severity, timestamps in UTC and correlation IDs
2. Actor, action, object and outcome in an audit event
3. Redaction, log injection prevention, access and retention
4. Delivery failures, buffering, monitoring and audit integrity

**Worked examples.** Create a denied-export event with no note body or token. Correlate two events from one request across a service and a worker.

**Practice check.** Define an event schema and test a redacted output sample. Specify how the application responds if a required audit record cannot be stored.

### 34. Metrics, traces and alert triage

**Goal.** Decide when an unusual number needs human attention.

1. Logs, metrics, traces and the question each answers
2. Counters, rates, percentiles, denominators and label cardinality
3. Baselines, alert thresholds, quiet traffic and false alarms
4. Runbooks, ownership and evidence that justifies escalation

**Worked examples.** Compare ten denied requests in two sets of very different traffic volume. Trace an export delay from a request ID to a queued job.

**Practice check.** Read a synthetic dashboard export, calculate a rate and write a triage note. Include one alternative explanation and the next evidence to collect.

### 35. Deployment, containers and infrastructure settings

**Goal.** Review the settings that shape the running service.

1. Build and runtime separation, immutable artifacts and non-root execution
2. Reverse proxies, forwarded headers, trusted hosts and TLS termination
3. Filesystem permissions, secret injection and network policy
4. Infrastructure as code (IaC), drift and a Django deployment review

**Worked examples.** Review a container manifest for its runtime identity. Trace which proxy is allowed to supply the original request scheme.

**Practice check.** Annotate a deployment manifest. Attach evidence for debug mode, process identity, host validation and one blocked unnecessary connection.

### 36. Incident response, disclosure and recovery

**Goal.** Guide a service from a credible report to a verified recovery.

1. Intake channels, triage, roles and severity
2. Evidence preservation, timelines, minimization and handover
3. Containment, credential rotation, restoration and backups
4. Coordinated disclosure, root cause, corrective actions and retesting

**Worked examples.** Build an event timeline from three redacted records. Compare a restored note count with a known backup manifest.

**Practice check.** Run a tabletop exercise for an exposed synthetic credential. Submit a timeline, containment decision, restoration check and a prevention task.

**Part checkpoint.** Hand over an incident timeline with a tested recovery step.

## Part X. Build tools and lead reviews

Use Python to review code and reports, then explain where engineering time should go.

### 37. Build a Python source-review tool

**Goal.** Package a small defensive tool that another engineer can understand and run.

1. Token streams, abstract syntax trees (ASTs) and source locations
2. `ast` visitors, aliases, scope and the limits of syntactic matching
3. `pyproject.toml`, console entry points and wheel contents
4. Stable output, exit contracts, fixture tests and tool documentation

**Worked examples.** Find debug settings in a supplied configuration module using an AST visitor. Compare how a name appears in a comment and in an assignment.

**Practice check.** Package the local checker. Run it on two supplied files, assert the expected locations and document one case its rule cannot decide.

### 38. Normalize findings and prioritize work

**Goal.** Turn several reports into a queue that an engineer can act on.

1. SARIF results, advisory identifiers and normalized finding records
2. Stable fingerprints, deduplication, suppressed items and reopening
3. CWE weakness classes, CVE identifiers, CVSS severity and contextual impact
4. Reachability, asset importance, compensating controls and remediation deadlines

**Worked examples.** Merge duplicate rows from two saved reports without losing their source references. Compare two equal-severity findings on differently exposed components.

**Practice check.** Publish a queue from fixture data. Give a reason, an owner and a next action for each of the top three findings.

### 39. Cloud identity and service boundaries

**Goal.** Review a design that crosses process and account boundaries.

1. Human and workload identities, short-lived credentials and scoped permissions
2. Object storage policies, private objects and expiring download grants
3. Shared responsibility, managed secrets and egress controls
4. Service-to-service identity, queue permissions and tenant-specific cache keys

**Worked examples.** Compare the permissions required by an upload worker and an export worker. Trace the lifetime of a private attachment download grant.

**Practice check.** Review a synthetic cloud policy and queue diagram. Produce a least-privilege access matrix and record the evidence needed to verify it.

### 40. Run an application security program

**Goal.** Turn individual fixes into decisions a product team can repeat.

1. Secure software development lifecycle (SSDLC) and design review triggers
2. Requirements, verification evidence, SSDF practices and SAMM maturity goals
3. Vulnerability intake, risk acceptance, service-level targets and ownership
4. Product-team coaching, risk communication and metrics with denominators

**Worked examples.** Compare two teams' overdue fixes relative to their release volume. Write a time-limited exception for a required control with a compensating measure.

**Practice check.** Create a one-release security plan with named owners, evidence and review dates. Explain one decision in language a product manager can use.

**Part checkpoint.** Package a checker and justify the next three items in a remediation queue.

## Part XI. Capstone. A private workspace export

Own one feature from its first requirement to the handover after an incident.

### 41. Capstone I. Define a private export

**Goal.** Agree on what an export means before implementing it.

1. Product brief, users and required behavior
2. Data-flow and threat model for export creation and delivery
3. Roles, data classification, trust assumptions and retention
4. Requirement IDs, test strategy and explicit exclusions

**Worked examples.** Discuss whether a departing member may download an old export. Compare granting download rights at request time and at retrieval time.

**Practice check.** Deliver a design brief and access matrix. A reviewer must be able to decide who can request, collect and expire an export in both workspaces.

### 42. Capstone II. Implement the controls

**Goal.** Deliver a working export feature with reviewable evidence.

1. Scoped database queries, ownership checks and minimal response fields
2. Worker authorization and storage key isolation
3. Idempotency, expiry, cancellation and failure cleanup
4. Unit, integration and deterministic concurrency tests

**Worked examples.** Create the same export twice with one request key. Revoke a member between queueing the export and its retrieval.

**Practice check.** Deliver a small patch and test results. Same-workspace access, cross-workspace denial, revocation and duplicate delivery must each have an observable result.

### 43. Capstone III. Review and release

**Goal.** Decide whether an identified build can ship.

1. Review the change against its requirements
2. Read static, dependency and configuration evidence
3. Inspect release gates, outstanding risk and rollback readiness
4. Produce an evidence index that another reviewer can follow

**Worked examples.** Decide how a missing dependency report changes release eligibility. Reassess a finding after identifying the installed version in the built artifact.

**Practice check.** Submit a release decision tied to a commit and artifact digest. Each mandatory control must link to evidence, an owner and its actual result.

### 44. Capstone IV. Operate, respond and hand over

**Goal.** Show that another engineer can operate and reassess the feature.

1. Interpret events for a delayed or wrongly retained export
2. Make a containment decision with incomplete information
3. Restore service and verify deletion and tenant boundaries
4. Write a concise advisory, retrospective and maintenance handover

**Worked examples.** Rebuild a UTC timeline from synthetic audit evidence. Compare the original acceptance tests with those needed after a retention change.

**Practice check.** Deliver an incident note, retest evidence and a handover. A second reader should be able to run the checks and identify the next owner of every open risk.

**Part checkpoint.** Hand another engineer a design, implementation, release decision and incident record they can verify.

## Appendix A. A small rule, three ways to read it

Mina belongs to Alpha. Ravi belongs to Beta. A note belongs to Alpha. Predict what each reader should see before you look at the output. These sample listings show the level of explanation expected in the book.

### Start with two values. Chapter 04

~~~python
member_workspace = "Alpha"
note_workspace = "Alpha"

if member_workspace == note_workspace:
    print("Allow")
else:
    print("Deny")
~~~

The output is `Allow`. Change the first value to `"Beta"` and the output becomes `Deny`. This first model gives each reader one workspace. Later chapters add multiple memberships and revocation.

### Give the rule a name. Chapter 06

~~~python
def may_read(active_workspaces, note_workspace):
    return note_workspace in active_workspaces

print(may_read({"Alpha"}, "Alpha"))
print(may_read({"Beta"}, "Alpha"))
~~~

The first line of output is `True`. The second is `False`. Here the caller supplies a set of current memberships. Chapter 23 makes the service responsible for loading those memberships from trusted records.

### Check a change over time. Chapter 12

~~~python
# Run below the may_read definition, in the same file.
active = {"Alpha"}
assert may_read(active, "Alpha")
active.remove("Alpha")
assert not may_read(active, "Alpha")
~~~

A successful run adds no output. If an assertion fails, Python reports the line. The assertions are learning checks. The application's permission decision belongs in ordinary control flow so it runs even when Python optimization disables assertions.

## Appendix B. A reference shelf for Python

| When you need to… | Read first | Then look up |
| --- | --- | --- |
| Choose a data representation | 03, 05, 10 | Built-in types, equality, hashing and mutability |
| Read or write bytes and text | 07, 08 | `str.encode`, `bytes.decode`, `open` and `pathlib.Path` |
| Interpret an error | 09, 12 | Exception hierarchy, chaining and `pytest.raises` |
| Limit memory or concurrent work | 11, 28 | Iterators, generators, task groups and cancellation |
| Follow imports or package a CLI | 02, 06, 31, 37 | Module search paths, entry points and wheel metadata |
| Model an interface | 06, 10 | Callable signatures, `Protocol`, type aliases and data classes |
| Compare timestamps or durations | 22, 33, 36 | Aware UTC datetimes and monotonic elapsed time |

**Further language study.** Once ordinary code is comfortable, compare pattern matching with a decision table, composition with inheritance, and a context manager with explicit cleanup. Explore the Python 3.12 text-encoding defaults alongside explicit file encodings in chapter 07. Check language changes against the versioned guide. [Python 3.12 changes](https://docs.python.org/3.12/whatsnew/3.12.html)

## Appendix C. Lab notebook and answer key

Use four lines for each run. Label them **input**, **prediction**, **observation** and **explanation**. Keep the command and version with the observation. If the result is a decision, add the identity and workspace. If the result is a file, describe the expected final state.

| Practice type | Hint to give first | What the worked answer must show |
| --- | --- | --- |
| Trace a program | Circle the expression that can change the result. | Values before and after the decision |
| Make a change | Name one observable behavior that must stay true. | A small diff and an independent check |
| Review a design | Identify who is trusted at each boundary. | Control, owner, evidence and residual risk |
| Investigate an event | Find the first timestamp and its source. | Timeline, uncertainty and recovery evidence |

**Example answer.** After revocation in Appendix A, the active set is empty. Membership is false and the second assertion passes. If the export worker still used the membership snapshot from the time the job was queued, the same test at the service boundary would need to change the stored membership before running the worker. Ask what state the worker actually reads.

## Appendix D. Standards and verification map

Use a standard to ask a precise question. Record its version, the relevant requirement or risk category, the implemented control and the evidence. The map gives chapter authors a starting point for selecting requirements and checking evidence.

| Reference | Question it helps answer | Where the reader uses it |
| --- | --- | --- |
| OWASP ASVS 5.0.0 | Which technical requirement should this control meet? | [18][ch-18], [23][ch-23], [30][ch-30], [43][ch-43] |
| OWASP Top 10:2025 | Which broad web application risks appear in this design? | [17][ch-17], [24][ch-24], [29][ch-29], [33][ch-33] |
| OWASP API Security Top 10 (2023) | Which API boundary, object or sensitive business flow needs attention? | [20][ch-20], [23][ch-23], [26][ch-26], [28][ch-28] |
| OWASP Cheat Sheet Series | What practical design questions should we review? | [21][ch-21]–[27][ch-27] |
| NIST SSDF 1.1 (SP 800-218) | Which development practice leaves repeatable evidence? | [31][ch-31], [32][ch-32], [36][ch-36], [40][ch-40] |
| OWASP SAMM | How can a team choose and measure its next improvement? | [38][ch-38], [40][ch-40] |
| CWE, CVE and CVSS | What class of weakness, named vulnerability or severity score are we discussing? | [29][ch-29], [31][ch-31], [38][ch-38] |

**Example evidence record.** Requirement `CB-READ-01` is a local book identifier. An active workspace member may read a private note. A member from a different workspace must receive the agreed denial and no private fields. The evidence is a two-workspace integration test and its recorded result for a named build. Add an exact ASVS requirement ID only after checking its wording and edition.

### Reading a finding precisely

| If the report contains… | What to record before deciding |
| --- | --- |
| A CWE category | The underlying weakness and where it might occur in the code |
| A CVE identifier | The advisory, affected package and affected version range |
| A CVSS score | Its version, vector, source and the environment assumptions |
| A tool rule or alert | Its location, evidence, limitations and a way to verify the correction |

## Glossary

Use these short meanings on a first reading. The chapter link gives the idea in context.

| Term | Working meaning | Chapter |
| --- | --- | --- |
| Actor | A person or service that takes an action. | [17][ch-17] |
| Artifact | A file produced by a build, such as a wheel or container image. | [32][ch-32] |
| Assertion | A check in a test that states what must be true. | [12][ch-12] |
| Asset | Something worth protecting, such as a private note. | [17][ch-17] |
| Authentication | Checking who a person or service is. | [21][ch-21] |
| Authorization | Deciding whether that identity may perform this action on this object. | [23][ch-23] |
| Boundary | A point where data crosses into a different area of trust or responsibility. | [17][ch-17] |
| Control | A design choice or check that reduces a particular risk. | [18][ch-18] |
| Evidence | An observable result that helps someone verify a claim. | [30][ch-30] |
| Fixture | Known data or setup used to make a test repeatable. | [12][ch-12] |
| Idempotency | A property that lets an operation be repeated with the same intended effect. | [20][ch-20] |
| Interpreter | The program that runs Python instructions. | [02][ch-02] |
| Invariant | A rule that must remain true across permitted changes. | [28][ch-28] |
| Regression test | A test kept to detect the return of an earlier problem. | [12][ch-12] |
| Repository | A project and the history of its saved changes. | [02][ch-02] |
| Risk | A possible loss considered together with its likelihood and impact. | [18][ch-18] |
| Scope | The part of a system or problem a decision covers. | [17][ch-17] |
| Tenant | A customer or workspace whose data and permissions the service keeps separate. | [23][ch-23] |
| Threat | Something that could cause harm to an asset. | [17][ch-17] |
| Vulnerability | A weakness that can allow harm to occur. | [29][ch-29] |

## Subject index

| Subject | Chapters |
| --- | --- |
| Access control | [23][ch-23], [42][ch-42] |
| Accounts and recovery | [21][ch-21], [22][ch-22] |
| Alerts and audit logs | [33][ch-33], [34][ch-34], [36][ch-36] |
| API contracts and inventory | [20][ch-20], [26][ch-26], [30][ch-30] |
| Archives and attachments | [25][ch-25], [39][ch-39] |
| Authentication | [21][ch-21], [22][ch-22], [39][ch-39] |
| Authorization | [04][ch-04], [23][ch-23], [42][ch-42] |
| Backup and restoration | [27][ch-27], [36][ch-36], [44][ch-44] |
| Browser security | [24][ch-24] |
| Business logic and rate limits | [20][ch-20], [28][ch-28] |
| Cache isolation | [23][ch-23], [39][ch-39] |
| Certificates and TLS | [16][ch-16], [26][ch-26], [35][ch-35] |
| CI and release gates | [32][ch-32], [43][ch-43] |
| Cloud identity | [39][ch-39] |
| Command execution | [14][ch-14] |
| Concurrency | [28][ch-28], [42][ch-42] |
| Configuration | [13][ch-13], [35][ch-35], [37][ch-37] |
| Containers | [35][ch-35] |
| Cryptography and key rotation | [21][ch-21], [26][ch-26], [27][ch-27] |
| CSRF and CORS | [24][ch-24] |
| Data classification and deletion | [18][ch-18], [41][ch-41], [44][ch-44] |
| Database constraints | [15][ch-15], [28][ch-28] |
| Debugging | [09][ch-09] |
| Dependencies and provenance | [31][ch-31], [32][ch-32] |
| Design review | [17][ch-17], [18][ch-18], [40][ch-40] |
| Disclosure | [36][ch-36] |
| Encoding and Unicode | [07][ch-07], [08][ch-08], [24][ch-24] |
| Error handling | [09][ch-09], [13][ch-13], [33][ch-33] |
| Evidence | [30][ch-30], [32][ch-32], [43][ch-43] |
| Exceptions to release rules | [32][ch-32], [40][ch-40] |
| Federated identity | [22][ch-22] |
| File paths and permissions | [08][ch-08], [14][ch-14], [25][ch-25] |
| Findings and triage | [29][ch-29], [38][ch-38] |
| Git and review | [02][ch-02], [12][ch-12], [29][ch-29] |
| HTTP | [16][ch-16], [19][ch-19], [20][ch-20] |
| Idempotency | [20][ch-20], [26][ch-26], [28][ch-28], [42][ch-42] |
| Incident response | [36][ch-36], [44][ch-44] |
| Injection prevention | [14][ch-14], [15][ch-15], [24][ch-24], [33][ch-33] |
| Input validation | [07][ch-07], [10][ch-10], [20][ch-20], [25][ch-25] |
| Integration tests | [12][ch-12], [19][ch-19], [30][ch-30] |
| Least privilege | [13][ch-13], [23][ch-23], [35][ch-35], [39][ch-39] |
| Metrics and denominators | [34][ch-34], [40][ch-40] |
| Multi-factor authentication | [21][ch-21] |
| OAuth and OpenID Connect | [22][ch-22] |
| Object-level access | [23][ch-23], [42][ch-42] |
| Packaging | [06][ch-06], [31][ch-31], [37][ch-37] |
| Parameter binding | [15][ch-15] |
| Password storage | [21][ch-21] |
| Privacy and retention | [18][ch-18], [33][ch-33], [44][ch-44] |
| Property-based tests | [30][ch-30] |
| Queues and retries | [26][ch-26], [28][ch-28], [42][ch-42] |
| Redaction | [13][ch-13], [33][ch-33] |
| Requirements | [18][ch-18], [41][ch-41] |
| Risk acceptance | [38][ch-38], [40][ch-40], [43][ch-43] |
| SBOM and SCA | [31][ch-31], [38][ch-38] |
| Secret management | [13][ch-13], [27][ch-27], [36][ch-36] |
| Serialization | [08][ch-08], [25][ch-25] |
| Sessions | [22][ch-22], [24][ch-24] |
| Source review and SAST | [29][ch-29], [37][ch-37] |
| SSRF | [26][ch-26] |
| Supply chain | [31][ch-31], [32][ch-32] |
| Telemetry | [33][ch-33], [34][ch-34] |
| Tenant isolation | [15][ch-15], [23][ch-23], [39][ch-39], [42][ch-42] |
| Test doubles | [12][ch-12], [16][ch-16], [26][ch-26] |
| Threat modeling | [17][ch-17], [41][ch-41] |
| Transactions | [15][ch-15], [28][ch-28] |
| Type hints | [10][ch-10] |
| Virtual environments | [02][ch-02] |
| Webhooks | [26][ch-26], [27][ch-27] |
| XSS and output encoding | [24][ch-24] |

## Python and tools index

| Name | Chapters |
| --- | --- |
| argparse | [14][ch-14] |
| ast and tokenize | [37][ch-37] |
| asyncio | [28][ch-28] |
| Bandit | [29][ch-29] |
| contextlib and with | [08][ch-08], [09][ch-09], [11][ch-11] |
| csv | [08][ch-08], [38][ch-38] |
| dataclasses and enum | [10][ch-10] |
| datetime and timezone | [33][ch-33], [36][ch-36] |
| dict, list, set and tuple | [05][ch-05] |
| Django ORM and migrations | [19][ch-19], [23][ch-23] |
| Django password APIs | [21][ch-21] |
| Django sessions and test client | [19][ch-19], [22][ch-22], [24][ch-24], [30][ch-30] |
| functools.wraps | [11][ch-11] |
| hashlib and hmac | [27][ch-27] |
| Hypothesis | [30][ch-30] |
| json | [08][ch-08], [20][ch-20], [38][ch-38] |
| logging | [33][ch-33] |
| os.environ | [13][ch-13] |
| pathlib | [08][ch-08], [25][ch-25] |
| pyproject.toml | [31][ch-31], [37][ch-37] |
| pytest | [12][ch-12], [30][ch-30] |
| re | [07][ch-07] |
| secrets | [21][ch-21], [27][ch-27] |
| Semgrep | [29][ch-29] |
| sqlite3 | [15][ch-15] |
| ssl | [16][ch-16], [26][ch-26] |
| subprocess | [14][ch-14] |
| tempfile | [14][ch-14], [25][ch-25] |
| typing | [10][ch-10] |
| venv and pip | [02][ch-02], [31][ch-31] |
| zipfile | [25][ch-25] |

## Bibliography and edition records

The edition records below were consulted on 26 November 2026. Use the versioned language and framework documentation for API behavior. Prefer the project's own release or specification when updating a chapter.

**Python.** Release number and date, supported branches, language reference, standard library and changes in the edition. [Python 3.12.14 release](https://www.python.org/downloads/release/python-31214/) · [Supported versions](https://devguide.python.org/versions/) · [Python 3.12 documentation](https://docs.python.org/3.12/) · [What's new](https://docs.python.org/3.12/whatsnew/3.12.html)

**Packaging and testing.** Build metadata, fixtures and property-based test design. [Python Packaging User Guide](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/) · [pytest documentation](https://docs.pytest.org/en/stable/) · [Hypothesis documentation](https://hypothesis.readthedocs.io/en/latest/)

**Django.** The selected 6.1.3 patch and the framework's documented security features. [Django 6.1.3 release notes](https://docs.djangoproject.com/en/6.1/releases/6.1.3/) · [Security in Django 6.1](https://docs.djangoproject.com/en/6.1/topics/security/)

**Application and API security.** Requirements, risk categories and implementation guidance. [OWASP ASVS](https://asvs.owasp.org/) · [OWASP Top 10:2025](https://top10.owasp.org/2025/) · [OWASP API Security Top 10 (2023)](https://owasp.org/API-Security/editions/2023/en/0x11-t10/) · [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/)

**Development programs.** Practices for building software securely and a model for measuring progress. [NIST SSDF 1.1](https://csrc.nist.gov/pubs/sp/800/218/final) · [OWASP SAMM](https://owaspsamm.org/model/)

**Weaknesses, advisories and severity.** Vocabulary for identifying, grouping and scoring findings. [MITRE CWE](https://cwe.mitre.org/) · [CVE Program](https://www.cve.org/) · [FIRST CVSS](https://www.first.org/cvss/)

**For authors.** Use [book-context.md](book-context.md) for shared conventions and [book-prompts.md](book-prompts.md) for the writing sequence.

[ch-01]: #01-your-first-program
[ch-02]: #02-set-up-a-workbench-you-can-rebuild
[ch-03]: #03-values-names-and-expressions
[ch-04]: #04-decisions-and-repetition
[ch-05]: #05-collections-and-shared-state
[ch-06]: #06-functions-modules-and-interfaces
[ch-07]: #07-text-bytes-and-patterns
[ch-08]: #08-files-and-structured-records
[ch-09]: #09-errors-debugging-and-cleanup
[ch-10]: #10-types-classes-and-domain-models
[ch-11]: #11-iteration-decorators-and-bounded-work
[ch-12]: #12-repeatable-tests-and-a-reviewable-change
[ch-13]: #13-processes-settings-and-secrets
[ch-14]: #14-command-line-tools-and-child-processes
[ch-15]: #15-relational-data-and-transactions
[ch-16]: #16-networks-http-and-tls
[ch-17]: #17-draw-the-system-and-its-trust-boundaries
[ch-18]: #18-security-requirements-and-private-data
[ch-19]: #19-build-the-casebook-web-service
[ch-20]: #20-api-contracts-and-business-rules
[ch-21]: #21-accounts-passwords-and-recovery
[ch-22]: #22-sessions-tokens-and-federated-identity
[ch-23]: #23-authorization-and-tenant-isolation
[ch-24]: #24-templates-cookies-and-the-browser
[ch-25]: #25-uploads-archives-and-serialization
[ch-26]: #26-outbound-requests-and-integrations
[ch-27]: #27-cryptographic-choices-and-key-management
[ch-28]: #28-concurrency-queues-and-resource-limits
[ch-29]: #29-review-python-changes-and-interpret-static-findings
[ch-30]: #30-verify-controls-in-running-code
[ch-31]: #31-dependencies-and-the-software-supply-chain
[ch-32]: #32-ci-checks-and-release-evidence
[ch-33]: #33-security-logs-and-audit-history
[ch-34]: #34-metrics-traces-and-alert-triage
[ch-35]: #35-deployment-containers-and-infrastructure-settings
[ch-36]: #36-incident-response-disclosure-and-recovery
[ch-37]: #37-build-a-python-source-review-tool
[ch-38]: #38-normalize-findings-and-prioritize-work
[ch-39]: #39-cloud-identity-and-service-boundaries
[ch-40]: #40-run-an-application-security-program
[ch-41]: #41-capstone-i-define-a-private-export
[ch-42]: #42-capstone-ii-implement-the-controls
[ch-43]: #43-capstone-iii-review-and-release
[ch-44]: #44-capstone-iv-operate-respond-and-hand-over
