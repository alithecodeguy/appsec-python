# Appendices

[Repository](../README.md) · [Contents](README.md#contents) · [Appendices](appendices.md) · [Indexes](indexes.md) · [References](references.md)

Use these four appendices while reading or repeating a lab. [Appendix A](#appendix-a-a-small-rule-three-ways-to-read-it) follows one decision from comparison to regression check. [Appendix B](#appendix-b-a-reference-shelf-for-python) helps locate language/API details. [Appendix C](#appendix-c-lab-notebook-and-answer-key) records a complete worked run and links to every chapter's solutions. [Appendix D](#appendix-d-standards-and-verification-map) connects verified external identifiers to specific controls and bounded evidence.

The edition baseline is **CPython 3.12.14**, with **Django 6.1.3** for web integration. The short appendix programs below actually ran on **CPython 3.12.14**; the database notebook used **SQLite 3.53.1**. Each chapter records its own runtime and unexecuted paths. The appendix does not upgrade an earlier example's evidence or lift the capstone's production HOLD.

## Appendix A. A small rule, three ways to read it

Mina is an active Alpha member. Ravi is an active Beta member. Lee manages Alpha only. The note we want to read belongs to Alpha. Predict the outcomes before running anything.

The full service rule requires a validated identity, an active account, a current active membership in the note's stored workspace and an allowed role/action/field contract. A stored export additionally belongs to its requester. Begin with a deliberately small projection, then restore those relevant facts as the model grows.

### Form 1: compare two values

Read [chapter 04's combined conditions](chapters/04.md#1-combine-the-facts-behind-a-decision) for the complete beginner decision. This first appendix file isolates only its workspace comparison. Identity, active membership and a recognized role are assumed by the fixture, not checked by equality.

Filename: `examples/appendices/values.py`.

```python
# A tiny comparison only: identity, active membership and a recognized role are assumed.
member_workspace = "Alpha"
note_workspace = "Alpha"

if member_workspace == note_workspace:
    print("Allow")
else:
    print("Deny")
```

From the repository root:

```shell
python -m examples.appendices.values
```

Expected output, also observed:

```text
Allow
```

`==` compares the values. The matching strings select the indented `print("Allow")` branch. Change only `member_workspace` to `"Beta"`: the result becomes `Deny`, because the `else` branch now runs. A manager in Beta would still fail this Alpha comparison.

This is not an application permission function. It does not establish who supplied either value, recognize an inactive account, load several memberships or protect an HTTP route. Those are explicit limits of the two-value teaching model.

### Form 2: give the decision a name

Use the actual [chapter 06 `may_read` contract](chapters/06.md#3-extract-the-access-decision-as-a-pure-operation). Preserve its five keyword-only inputs rather than replacing it with an incompatible two-argument helper.

Filename: `examples/appendices/rules.py`.

```python
def may_read(
    *,
    signed_in,
    membership_active,
    reader_workspace,
    note_workspace,
    role,
):
    """Return whether the supplied reader facts permit this note read."""
    if not signed_in:
        return False
    if not membership_active:
        return False
    if reader_workspace != note_workspace:
        return False
    return role in ("member", "manager")


if __name__ == "__main__":
    print("Mina", may_read(signed_in=True, membership_active=True,
        reader_workspace="Alpha", note_workspace="Alpha", role="member"))
    print("Ravi", may_read(signed_in=True, membership_active=True,
        reader_workspace="Beta", note_workspace="Alpha", role="member"))
```

Run:

```shell
python -m examples.appendices.rules
```

Expected output, also observed:

```text
Mina True
Ravi False
```

`def` names the operation. `return` supplies the boolean result. The `*` in the signature requires callers to name all five arguments. The `if __name__ == "__main__"` block runs the examples when invoked as a program; importing `may_read` does not print them.

An unknown role reaches the final tuple-membership test and returns false. A recognized manager must still pass sign-in, active membership and workspace equality. The caller supplies already validated facts. A correct pure function cannot make stale or forged facts current.

### Form 3: check a change over time

[Chapter 12's role cases](chapters/12.md#worked-example-1-test-the-access-rule-across-roles) use fresh facts and independent expectations. Its [unknown-role worked answer](chapters/12.md#exercise-3) explains why the other facts must stay valid so the test reaches the intended branch.

Filename: `examples/appendices/checks.py`.

```python
from examples.appendices.rules import may_read

facts = {"signed_in": True, "membership_active": True,
         "reader_workspace": "Alpha", "note_workspace": "Alpha", "role": "member"}

assert may_read(**facts)
facts["membership_active"] = False
assert not may_read(**facts)

# Keep the other facts valid so the unknown-role check actually reaches the role decision.
facts["membership_active"] = True
facts["role"] = "unknown"
assert not may_read(**facts)

facts["role"] = "manager"
facts["reader_workspace"] = "Beta"
assert not may_read(**facts)
```

Run:

```shell
python -m examples.appendices.checks
```

Expected and observed: **no output, exit status 0**. The first assertion allows active Mina. Changing the active-membership fact refuses the next call. The following checks separately reach unknown-role denial and cross-workspace manager denial.

Assertions are test observations, not production enforcement. Python optimization can disable them. The permission function uses ordinary `if`/`return` control flow, while the test states what that function must return. Run this learning check without `-O`.

The dictionary update is a model of changed facts, not a database revocation. [Chapter 23's complete rule](chapters/23.md#state-the-complete-read-rule) loads current account/membership from trusted records. [The notebook below](#a-worked-notebook-entry-revoke-then-read) makes that change in SQLite. [Chapter 42](chapters/42.md) checks it before worker creation and collection; [chapter 44](chapters/44.md) checks it again after an isolated restore.

**Table TA-01. Which question each form answers**

| Form | Question answered | What the next model must add |
| --- | --- | --- |
| Two values | Do these workspace values match? | Identity, active state, role and trusted data sources |
| Named function | Do all supplied facts satisfy this decision? | Current server-loaded records and complete object scope |
| Regression check | Does a changed fact produce the expected result? | Actual stored revocation, all entry points, output fields and final state |

## Appendix B. A reference shelf for Python

Start with the linked chapter's small example, then use the reference to resolve the precise API or language question. An API name is not a design policy: `Path` does not authorize a path, a type hint does not validate a request, and `await` does not turn blocking work into nonblocking work.

### Find the explanation by the task

**Table TB-01. Language and standard-library shelf**

| When you need to… | Read in the book | Then inspect |
| --- | --- | --- |
| Distinguish interpreter, environment and module | [02](chapters/02.md), [06](chapters/06.md), [13](chapters/13.md) | Executable/module paths, `python -m`, virtual environments and import locations |
| Compare values without changing them | [03](chapters/03.md), [04](chapters/04.md) | Equality, identity, truth values and boolean short-circuiting in [built-in types](https://docs.python.org/3.12/library/stdtypes.html) |
| Choose a collection and understand aliases | [05](chapters/05.md), [10](chapters/10.md) | Lists, tuples, sets, dictionaries, hashing and shallow copies in [built-in types](https://docs.python.org/3.12/library/stdtypes.html) |
| Design a callable contract | [06](chapters/06.md), [11](chapters/11.md) | Positional/keyword-only arguments, defaults, unpacking and return paths in the [control-flow tutorial](https://docs.python.org/3.12/tutorial/controlflow.html) |
| Describe shapes without assuming validation | [10](chapters/10.md), [29](chapters/29.md) | `Protocol`, union/alias notation and annotation limits in [`typing`](https://docs.python.org/3.12/library/typing.html) |
| Separate text, bytes and encoded representations | [07](chapters/07.md), [08](chapters/08.md) | `str.encode`, `bytes.decode`, decoding errors and explicit encodings; [text-encoding guidance](https://docs.python.org/3.12/library/io.html#text-encoding) for environment-dependent defaults |
| Read/write a controlled file | [08](chapters/08.md), [14](chapters/14.md), [25](chapters/25.md) | [`pathlib.Path`](https://docs.python.org/3.12/library/pathlib.html), open modes, context managers, limits and cleanup ownership |
| Parse JSON and reject unwanted structure | [08](chapters/08.md), [20](chapters/20.md), [26](chapters/26.md) | [`json`](https://docs.python.org/3.12/library/json.html), exact schema/duplicate-key rules and byte bounds before parsing |
| Follow an exception and its cleanup | [09](chapters/09.md), [12](chapters/12.md), [28](chapters/28.md) | Exception type/chaining, `try`/`finally`, context-manager exit and narrowly expected failure |
| Consume data incrementally | [11](chapters/11.md), [08](chapters/08.md), [28](chapters/28.md) | Iterators, generators, `yield`, bounded batches and ownership of unconsumed resources |
| Bind values and inspect rollback | [15](chapters/15.md), [23](chapters/23.md), [42](chapters/42.md) | [`sqlite3`](https://docs.python.org/3.12/library/sqlite3.html), placeholders, connection ownership, transactions and cursor results |
| Compare dates and elapsed durations | [22](chapters/22.md), [33](chapters/33.md), [36](chapters/36.md), [44](chapters/44.md) | Aware UTC values in [`datetime`](https://docs.python.org/3.12/library/datetime.html); monotonic elapsed budgets and injected clocks |
| Overlap work and stop it safely | [28](chapters/28.md), [42](chapters/42.md) | Threads/processes, barriers and [asyncio tasks/cancellation](https://docs.python.org/3.12/library/asyncio-task.html); database guarantees remain separate |
| Identify installed distributions and builds | [31](chapters/31.md), [32](chapters/32.md), [37](chapters/37.md), [43](chapters/43.md) | [`importlib.metadata`](https://docs.python.org/3.12/library/importlib.metadata.html), distribution/import names, entry points and artifact hashes |

For further language study, compare pattern matching with a decision table, composition with inheritance and a context manager with explicit cleanup. The book's existing rules are the comparison target: a different syntax must preserve their outcomes. On Python 3.12, default text encoding can depend on the environment and UTF-8 mode. Keep explicit encodings and validate actual bytes at a boundary.

### Framework and tool shelf

**Table TB-02. Choose a tool for a named check**

| Question | Chapters | Reference and evidence boundary |
| --- | --- | --- |
| How do I express related tests? | [12](chapters/12.md), [30](chapters/30.md) | [pytest parametrization](https://docs.pytest.org/en/stable/how-to/parametrize.html); fixtures and expected outcomes are not supplied by the tool |
| What does the Django client exercise? | [19](chapters/19.md), [24](chapters/24.md), [30](chapters/30.md), [42](chapters/42.md) | [Django 6.1 test tools](https://docs.djangoproject.com/en/6.1/topics/testing/tools/); distinguish client/middleware checks from browser and deployed proxy behavior |
| How do I select a maintained cryptographic operation? | [21](chapters/21.md), [22](chapters/22.md), [27](chapters/27.md) | Follow each chapter's password, token or AEAD library/reference and exact version; do not invent a substitute primitive |
| How do I interpret a warning rather than count it? | [29](chapters/29.md), [37](chapters/37.md), [38](chapters/38.md) | Source/rule/input path, tool coverage, confidence and an independent reproduction |
| How do I know which release was checked? | [32](chapters/32.md), [43](chapters/43.md) | Commit, artifact/configuration identity, report subject and explicit missing/skipped gates |
| How do I operate the result? | [33](chapters/33.md)–[36](chapters/36.md), [39](chapters/39.md)–[44](chapters/44.md) | Event/metric context, workload authority, retention inventory and a repeatable recovery handover |

A `stable` documentation link can change. Record actual package versions, commands and results with a lab run, and use the chapter's selected requirements for reproduction. A successful import, a tool's green summary and a complete release check are different facts. In the capstone, 20 core methods and three HTTP methods passed; [the release decision](chapters/43.md#apply-the-mandatory-gates-without-averaging-them) remains HOLD.

## Appendix C. Lab notebook and answer key

### A four-line template

Write a prediction before execution. Keep the following labels, even if each needs several sentences:

```text
input: fixture identity, workspace/object, starting values/state, intended change and source revision
prediction: expected return/output and exact final state, including refusal, retry or cleanup
observation: executable/version, command, actual output/status, inspected state and evidence location
explanation: decisive expression/query/boundary, why it differs or agrees, and what the run did not prove
```

For service exercises, record which values came from trusted identity/storage and which were client selectors. For retries/failures, inspect storage after the operation. For clocks, record the controlled time and boundary. For a release or incident decision, include the subject, owner, evidence kind and unresolved risk.

Do not store a real password, session token, key, private payload or full production database in an ordinary notebook. A digest identifies recorded bytes; it does not authenticate their collector or establish that the test was adequate.

### A worked notebook entry: revoke, then read

This completes the [chapter 23 revoke-then-read exercise](chapters/23.md#exercise-4) at its actual local SQLite boundary. Preserve `examples/ch23/authorization_service.py` and the repository layout. No Django, network service or crypto dependency is required.

**input:** A fresh fixture contains Mina/Alpha, Ravi/Beta and Lee as Alpha manager. Mina builds a requester-bound in-memory artifact of Alpha note `101` while active. Lee then commits Mina's Alpha membership revocation. The source notes must remain unchanged; a different workspace's permitted path must still work.

**prediction:** Mina's own retrieval is initially 200. Her stored active flag becomes 0. Both her next detail read and old-artifact retrieval become generic 404. Ravi can still read Beta, and Lee has no Beta authority. Revocation changes membership, not the note rows. This prediction would expose a permanently-denying implementation as well as an implementation that trusts the artifact's old permission.

Filename: `examples/appendices/notebook_demo.py`.

```python
from pathlib import Path
from tempfile import TemporaryDirectory

from examples.ch23.authorization_service import (
    build_export, detail_view, download_export, list_view, response,
    revoke_member, seed, snapshot,
)

with TemporaryDirectory(prefix="casebook-appendix-notebook-") as folder:
    database = Path(folder)/"casebook.sqlite3"
    seed(database)
    artifact = build_export(database, user_id=1, workspace_id=1, note_ids=[101])
    print("before own retrieval:", response(lambda: download_export(database, user_id=1, artifact=artifact))[0])
    notes_before = snapshot(database)["notes"]
    revoke_member(database, actor_id=3, workspace_id=1, target_user_id=1)
    membership = next(row for row in snapshot(database)["memberships"]
                      if row["workspace_id"] == 1 and row["user_id"] == 1)
    print("stored Mina active:", membership["active"])
    print("after detail:", detail_view(database, user_id=1, workspace_id=1, note_id=101)[0])
    print("after own artifact:", response(lambda: download_export(database, user_id=1, artifact=artifact))[0])
    print("Ravi Beta:", list_view(database, user_id=2, workspace_id=2)[0])
    print("Lee Beta:", list_view(database, user_id=3, workspace_id=2)[0])
    print("source notes unchanged:", snapshot(database)["notes"] == notes_before)
```

**observation:** From the repository root, `python -m examples.appendices.notebook_demo` ran on CPython **3.12.14** with SQLite **3.53.1**. The actual output matched:

```text
before own retrieval: 200
stored Mina active: 0
after detail: 404
after own artifact: 404
Ravi Beta: 200
Lee Beta: 404
source notes unchanged: True
```

**explanation:** `download_export` checks current stored membership before returning the trusted artifact payload. Creating that copy earlier did not create permanent collection authority. The stored membership observation connects the policy change to the refusal; the Beta positive path shows that the service is not simply broken for everyone. The temporary database is removed at the end.

The statuses are modeled local response tuples, not observed HTTP responses. The artifact is an in-process record, not the encrypted/durable capstone. This run does not prove browser identity, queue delivery, concurrent/in-flight interruption, deletion of the earlier copy or production isolation. See the [chapter 23 worked answer](chapters/23.md#exercise-4), [chapter 42 verification limits](chapters/42.md#verification-record-and-next-starting-state) and [chapter 44 recovery checks](chapters/44.md#verify-recovery-with-both-allowed-and-denied-paths) for the later boundaries.

### Hints by practice type

**Table TC-01. What to retain after each kind of exercise**

| Practice | First hint | Worked answer/evidence must include |
| --- | --- | --- |
| Trace a program | Identify the expression that can change the result | Initial/intermediate/final values and the selected branch |
| Correct a function | State one independent expected outcome first | Small change, intended failing check, corrected result and relevant boundary |
| Check stored behavior | Read current facts, not a cached permission claim | Allowed and denied cases, complete final rows and rollback/retry state |
| Review a design | Name each boundary and the authority crossing it | Control, owner, assumptions, evidence and explicit exclusions |
| Read a finding | Separate its claimed path from what source proves | Location, input/argument facts, disposition and regression or missing evidence |
| Decide a release | Identify the actual subject before reading green indicators | Mandatory control ledger, skips/missing reports, commit/artifact/configuration binding |
| Investigate/recover | Separate event time, observation time and effective policy time | UTC timeline, uncertainty, copy scope, current authority and recovery retests |

### Chapter solution directory

These links go to headings that exist in the completed manuscripts. Chapters 34–40 combine hints and worked answers; the others have a separate worked-answer section. Read the exercise and make a prediction before following its answer.

| Chapter | Solution section |
| --- | --- |
| [01. Your first program](chapters/01.md) | [Worked answers](chapters/01.md#worked-answers) |
| [02. Set up a workbench you can rebuild](chapters/02.md) | [Worked answers](chapters/02.md#worked-answers) |
| [03. Values, names and expressions](chapters/03.md) | [Worked answers](chapters/03.md#worked-answers) |
| [04. Decisions and repetition](chapters/04.md) | [Worked answers](chapters/04.md#worked-answers) |
| [05. Collections and shared state](chapters/05.md) | [Worked answers](chapters/05.md#worked-answers) |
| [06. Functions, modules and interfaces](chapters/06.md) | [Worked answers](chapters/06.md#worked-answers) |
| [07. Text, bytes and patterns](chapters/07.md) | [Worked answers](chapters/07.md#worked-answers) |
| [08. Files and structured records](chapters/08.md) | [Worked answers](chapters/08.md#worked-answers) |
| [09. Errors, debugging and cleanup](chapters/09.md) | [Worked answers](chapters/09.md#worked-answers) |
| [10. Types, classes and domain models](chapters/10.md) | [Worked answers](chapters/10.md#worked-answers) |
| [11. Iteration, decorators and bounded work](chapters/11.md) | [Worked answers](chapters/11.md#worked-answers) |
| [12. Repeatable tests and a reviewable change](chapters/12.md) | [Worked answers](chapters/12.md#worked-answers) |
| [13. Processes, settings and secrets](chapters/13.md) | [Worked answers](chapters/13.md#worked-answers) |
| [14. Command-line tools and child processes](chapters/14.md) | [Worked answers](chapters/14.md#worked-answers) |
| [15. Relational data and transactions](chapters/15.md) | [Worked answers](chapters/15.md#worked-answers) |
| [16. Networks, HTTP and TLS](chapters/16.md) | [Worked answers](chapters/16.md#worked-answers) |
| [17. Draw the system and its trust boundaries](chapters/17.md) | [Worked answers](chapters/17.md#worked-answers) |
| [18. Security requirements and private data](chapters/18.md) | [Worked answers](chapters/18.md#worked-answers) |
| [19. Build the Casebook web service](chapters/19.md) | [Worked answers](chapters/19.md#worked-answers) |
| [20. API contracts and business rules](chapters/20.md) | [Worked answers](chapters/20.md#worked-answers) |
| [21. Accounts, passwords and recovery](chapters/21.md) | [Worked answers](chapters/21.md#worked-answers) |
| [22. Sessions, tokens and federated identity](chapters/22.md) | [Worked answers](chapters/22.md#worked-answers) |
| [23. Authorization and tenant isolation](chapters/23.md) | [Worked answers](chapters/23.md#worked-answers) |
| [24. Templates, cookies and the browser](chapters/24.md) | [Worked answers](chapters/24.md#worked-answers) |
| [25. Uploads, archives and serialization](chapters/25.md) | [Worked answers](chapters/25.md#worked-answers) |
| [26. Outbound requests and integrations](chapters/26.md) | [Worked answers](chapters/26.md#worked-answers) |
| [27. Cryptographic choices and key management](chapters/27.md) | [Worked answers](chapters/27.md#worked-answers) |
| [28. Concurrency, queues and resource limits](chapters/28.md) | [Worked answers](chapters/28.md#worked-answers) |
| [29. Review Python changes and interpret static findings](chapters/29.md) | [Worked answers](chapters/29.md#worked-answers) |
| [30. Verify controls in running code](chapters/30.md) | [Worked answers](chapters/30.md#worked-answers) |
| [31. Dependencies and the software supply chain](chapters/31.md) | [Worked answers](chapters/31.md#worked-answers) |
| [32. CI checks and release evidence](chapters/32.md) | [Worked answers](chapters/32.md#worked-answers) |
| [33. Security logs and audit history](chapters/33.md) | [Worked answers](chapters/33.md#worked-answers) |
| [34. Metrics, traces and alert triage](chapters/34.md) | [Hints and worked answers](chapters/34.md#hints-and-worked-answers) |
| [35. Deployment, containers and infrastructure settings](chapters/35.md) | [Hints and worked answers](chapters/35.md#hints-and-worked-answers) |
| [36. Incident response, disclosure and recovery](chapters/36.md) | [Hints and worked answers](chapters/36.md#hints-and-worked-answers) |
| [37. Build a Python source-review tool](chapters/37.md) | [Hints and worked answers](chapters/37.md#hints-and-worked-answers) |
| [38. Normalize findings and prioritize work](chapters/38.md) | [Hints and worked answers](chapters/38.md#hints-and-worked-answers) |
| [39. Cloud identity and service boundaries](chapters/39.md) | [Hints and worked answers](chapters/39.md#hints-and-worked-answers) |
| [40. Run an application security program](chapters/40.md) | [Hints and worked answers](chapters/40.md#hints-and-worked-answers) |
| [41. Capstone I. Define a private export](chapters/41.md) | [Worked answers](chapters/41.md#worked-answers) |
| [42. Capstone II. Implement the controls](chapters/42.md) | [Worked answers](chapters/42.md#worked-answers) |
| [43. Capstone III. Review and release](chapters/43.md) | [Worked answers](chapters/43.md#worked-answers) |
| [44. Capstone IV. Operate, respond and hand over](chapters/44.md) | [Worked answers](chapters/44.md#worked-answers) |

The chapter's answer is a reference for its stated contract, not an answer to every possible production variant. In particular, the capstone's [design](chapters/41.md), [implementation](chapters/42.md), [held review](chapters/43.md) and [incident handover](chapters/44.md) preserve partial/unexecuted evidence. A new policy or environment needs new applicable checks.

## Appendix D. Standards and verification map

### Use the right kind of reference

A technical requirement, a risk category, a development practice, a weakness class and a severity vector do different jobs. The mapping below is a review aid, not a certification or an assertion that all requirements at an ASVS level have been assessed. Identifier wording/editions were checked against the primary sources linked here on **2026-11-27**.

**Table TD-01. Reference roles and editions**

| Reference | Edition/source used | What it helps select | What it does not establish |
| --- | --- | --- | --- |
| OWASP ASVS | [5.0.0 authorization source](https://raw.githubusercontent.com/OWASP/ASVS/v5.0.0/5.0/en/0x17-V8-Authorization.md), [5.0.0 data-protection source](https://raw.githubusercontent.com/OWASP/ASVS/v5.0.0/5.0/en/0x23-V14-Data-Protection.md) | Specific technical verification requirements | Conformance from one example or a section-level label |
| OWASP Top 10 | [2025 list](https://owasp.org/Top10/2025/) | Broad web-risk questions | A complete test specification or a vulnerability finding |
| OWASP API Security Top 10 | [2023 list](https://owasp.org/API-Security/editions/2023/en/0x11-t10/) | API object, field, resource and integration boundaries | Exhaustive authorization or platform coverage |
| OWASP Cheat Sheet Series | Living guidance linked from the relevant chapter | Practical design/implementation questions | A numeric requirement edition; do not invent cheat-sheet item IDs |
| NIST SSDF | [1.1, SP 800-218](https://csrc.nist.gov/pubs/sp/800/218/final), [official task definitions](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-218.pdf) | Repeatable development/review/evidence practices | An application permission policy or automatic release approval |
| OWASP SAMM | [Version 2 model](https://owaspsamm.org/model/) and named practice pages below | A measured improvement objective | An organizational maturity score from a teaching exercise |
| CWE / CVE / CVSS | Authoritative definitions and versioned severity specification below | Weakness classification / vulnerability record / severity description | Interchangeable labels or a complete local risk decision |

`CB-READ-01`, `CB-RETENTION-01`, `EXP-04` and `A41-05` are **local book identifiers**, not standard IDs. They carry product rules such as requester binding, active membership and exact retention periods. A standard helps frame the question; the local rule and applicable evidence decide this implementation's result.

### Verified ASVS requirements and bounded evidence

Use full identifiers such as `v5.0.0-8.2.2`, keeping the edition. The following summaries are paraphrases of the pinned source, not substitutes for its complete wording. “Supports” means a limited evidence link, not an ASVS pass.

**Table TD-02. Technical requirement to control/evidence**

| Verified ASVS 5.0.0 identifier | Check focus | Casebook control and evidence location | Scope/result limit |
| --- | --- | --- | --- |
| `v5.0.0-8.1.1` | Document function/object decisions | [23 access matrix](chapters/23.md#fill-the-same-matrix-for-every-read-path), [41 export matrices](chapters/41.md#fill-the-access-matrices) | Authored policy; documentation alone does not enforce it |
| `v5.0.0-8.2.1` | Explicit function permissions | [23 manager actions](chapters/23.md#administrative-access-still-needs-a-policy), [42 early expiry](chapters/42.md#preserve-the-original-clocks) | Local manager/member cases; local HTTP adapter checks passed; deployed controls remain unverified |
| `v5.0.0-8.2.2` | Explicit object/data permissions | [23 scoped reads](chapters/23.md#reuse-the-complete-scope), [42 core tests](chapters/42.md#test-the-implemented-boundaries) | Local Alpha/Beta/requester cases; no full deployed-path claim |
| `v5.0.0-8.2.3` | Explicit field permissions | [20 field contracts](chapters/20.md), [23 field decisions](chapters/23.md#function-object-and-field-decisions-are-different) | Exact allowlists/checks for selected responses and writes |
| `v5.0.0-8.3.1` | Trusted enforcement layer | [23 service scope](chapters/23.md#reuse-the-complete-scope), [42 trusted identity table](chapters/42.md#carry-chapter-41s-field-contract-into-code) | Fixture calls are not browser authentication |
| `v5.0.0-8.3.2` | Timely authorization changes | [23 next-request trace](chapters/23.md#show-exactly-what-the-next-request-sees), [42 revocation example](chapters/42.md#worked-example-2-revoke-between-queueing-and-collection) | Committed revocation before a new decision; no universal in-flight interruption |
| `v5.0.0-8.4.1` | Cross-tenant boundaries | [30 generated checks](chapters/30.md), [44 recovery probes](chapters/44.md#verify-recovery-with-both-allowed-and-denied-paths) | Keep positive cases; deployed browser/provider paths remain unexecuted |
| `v5.0.0-14.1.1` | Classify sensitive data | [18 inventory](chapters/18.md#3-data-inventory-purpose-minimization-retention-and-deletion), [41 copy inventory](chapters/41.md#classify-every-copy) | Authored classification, not inspection of an entire deployment |
| `v5.0.0-14.1.2` | Define protection obligations | [18 retention policy](chapters/18.md#work-through-one-retention-decision), [41 retention rule](chapters/41.md#expiry-and-deletion-clocks) | Durations are fictional product choices, not standard-mandated periods |
| `v5.0.0-14.2.4` | Implement documented protections | [27 key/encryption lab](chapters/27.md), [42 lifecycle tests](chapters/42.md), [44 copy-scope failures](chapters/44.md#define-copy-scope-before-declaring-removal-complete) | Local AEAD/deletion evidence; production custody/copies remain gaps |
| `v5.0.0-14.2.7` | Apply retention/removal classification | [18 retention checks](chapters/18.md#make-the-deletion-passfail-decision-observable), [44 timeline/copy checks](chapters/44.md#worked-example-1-rebuild-the-utc-timeline) | Failed/late state retained; scheduled provider removal not established |
| `v5.0.0-14.3.2` | Browser anti-caching response fields | [24 browser controls](chapters/24.md), [30 header evidence](chapters/30.md), [42 HTTP seam](chapters/42.md#supply-the-http-integration-seam-without-inventing-authentication) | Source policy/passive report is not observed browser enforcement; local capstone HTTP methods passed; browser deployment unverified |

For ASVS `8.3.2`, inspect its full treatment of changes and mitigating controls. Casebook's private-content policy requires current permission for a new read; an alert after disclosure would not satisfy that policy. For retention, neither an expired flag nor a live-row receipt proves every managed copy is absent.

### Risk categories: use the right year's identifier

The [OWASP Top 10:2025](https://owasp.org/Top10/2025/) labels below belong to **2025**, not the 2021 ordering. API labels belong to the separate **2023 API** list. These are selected questions, not coverage of both complete lists.

**Table TD-03. Risk category to concrete review question**

| Verified risk identifier | Question in this book | Chapter/evidence path |
| --- | --- | --- |
| `A01:2025` — Broken Access Control | Can a changed selector or old permission reach private content? | [23](chapters/23.md), [42](chapters/42.md), [44](chapters/44.md) allowed/denied and recovery probes |
| `A03:2025` — Software Supply Chain Failures | Which installed/build inputs belong to the actual candidate? | [31](chapters/31.md), [32](chapters/32.md), [43](chapters/43.md) metadata, hashes and missing-report gate |
| `A04:2025` — Cryptographic Failures | Is the operation appropriate, with protected keys and nonce history? | [27](chapters/27.md), [39](chapters/39.md), [43](chapters/43.md) local checks and custody blockers |
| `A05:2025` — Injection | Can external text become SQL/command syntax? | [14](chapters/14.md), [15](chapters/15.md), [29](chapters/29.md) argument/binding review |
| `A09:2025` — Security Logging and Alerting Failures | Is useful evidence protected, and can a failure be detected? | [33](chapters/33.md), [34](chapters/34.md), [44](chapters/44.md) source-labeled events and stale-flag detection |
| `A10:2025` — Mishandling of Exceptional Conditions | Do errors, cancellation and cleanup leave safe state? | [09](chapters/09.md), [28](chapters/28.md), [42](chapters/42.md) fault and rollback checks |
| `API1:2023` | Is this specific object within the caller's scope? | [20](chapters/20.md), [23](chapters/23.md) selectors and scoped queries |
| `API3:2023` | Which object fields may be read or changed? | [20](chapters/20.md), [23](chapters/23.md) exact request/response fields |
| `API4:2023` | Where are actual resource budgets enforced? | [25](chapters/25.md), [28](chapters/28.md), [42](chapters/42.md) byte/capacity boundaries |
| `API7:2023` | Which destination can the server actually contact? | [26](chapters/26.md) registry/fake refusal; network enforcement still separate |
| `API10:2023` | Are partner responses treated as bounded untrusted inputs? | [26](chapters/26.md) fake transport, schema/size and unchanged-state checks |

Primary source for the `API*` identifiers: [OWASP API Security Top 10, 2023](https://owasp.org/API-Security/editions/2023/en/0x11-t10/). A passing fake transport or local query does not by itself prove actual network/HTTP/provider controls.

### Development practices and improvement evidence

The SSDF task references below are verified in **SSDF 1.1 / SP 800-218**. The wording is a short review question, not a complete task definition. These mappings select evidence to inspect rather than claim organizational implementation.

**Table TD-04. Verified SSDF tasks**

| Identifier | Review question | Casebook evidence and limitation |
| --- | --- | --- |
| `PO.4.1` | Which security checks are required? | [40 required evidence](chapters/40.md#write-the-behavior-before-choosing-its-report), [43 mandatory gates](chapters/43.md#apply-the-mandatory-gates-without-averaging-them); authored criteria, not authenticated approvals |
| `PS.2.1` | Can an acquirer check release integrity? | [32 artifact/signature exercise](chapters/32.md), [43 commit/archive linkage](chapters/43.md#identify-the-candidate-before-reviewing-it); local unsigned capstone linkage is narrower than trusted release provenance |
| `PW.7.1` | Which review/analysis approach is appropriate? | [29 path review](chapters/29.md), [43 bounded source review](chapters/43.md#review-static-findings-as-claims-about-paths); illustrative findings are not executed scans |
| `PW.8.2` | Were scoped tests executed and findings retained? | [30](chapters/30.md), [42](chapters/42.md), [43 actual run](chapters/43.md#retain-observable-state-not-only-test-totals); keep skipped/missing results distinct |
| `RV.2.1` | What risk facts support the remediation choice? | [38 priority queue](chapters/38.md), [40 exception](chapters/40.md), [43 blockers](chapters/43.md#give-every-open-item-a-next-action); authored package/advisory fixtures remain fictional |
| `RV.3.1` | What caused the issue and what should change? | [36](chapters/36.md), [44 retrospective](chapters/44.md#a-short-advisory-and-retrospective); controlled synthetic causes, not real incident attribution |

Source: [official SSDF 1.1 PDF](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-218.pdf). These references supplement, rather than rename, chapter 40's practice-level `PO.1`, `PO.4`, `PW.8` and `RV.2` links.

**Table TD-05. SAMM version 2 practice names, not invented activity numbers**

| Verified named practice | Next improvement to consider | Book evidence |
| --- | --- | --- |
| [Strategy and Metrics](https://owaspsamm.org/model/governance/strategy-and-metrics/) | Define the cohort/denominator and decision a metric supports | [40 metrics and ownership](chapters/40.md) |
| [Defect Management](https://owaspsamm.org/model/implementation/defect-management/) | Preserve origins, owners and dispositions in one queue | [38](chapters/38.md), [40](chapters/40.md) |
| [Requirements-driven Testing](https://owaspsamm.org/model/verification/requirements-driven-testing/) | Link a control to permitted, denied and failure-path checks | [30](chapters/30.md), [41](chapters/41.md), [43](chapters/43.md) |
| [Incident Management](https://owaspsamm.org/model/operations/incident-management/) | Rehearse recovery and give each gap a next owner | [36](chapters/36.md), [44 handover](chapters/44.md#handover-another-engineer-can-run) |

No activity score or maturity level is assigned. A fictional roster and one release exercise do not establish how a real organization operates.

### Read CWE, CVE and CVSS precisely

**Table TD-06. Do not confuse classification with applicable vulnerability evidence**

| Reference | Verified meaning/use here | Evidence to inspect before deciding |
| --- | --- | --- |
| [CWE-89](https://cwe.mitre.org/data/definitions/89.html) | SQL-injection weakness class | Actual argument type/source, query construction and binding; [15](chapters/15.md), [29](chapters/29.md) |
| [CWE-862](https://cwe.mitre.org/data/definitions/862.html) | An authorization check is missing | Actor/resource/action path and the absent enforcement; [29](chapters/29.md) |
| [CWE-863](https://cwe.mitre.org/data/definitions/863.html) | Authorization is checked incorrectly | Why the implemented decision permits the wrong action/object; [23](chapters/23.md), [29](chapters/29.md) |
| [CWE-918](https://cwe.mitre.org/data/definitions/918.html) | Server-side request-forgery weakness | Destination influence and actual connection policy; [26](chapters/26.md) |
| [CVE Program](https://www.cve.org/ResourcesSupport/AllResources/CNARules/) | Identifiers/records for specific vulnerabilities | Actual record/advisory, product/version range, status and applicability; [31](chapters/31.md), [38](chapters/38.md), [43](chapters/43.md) |
| [CVSS v4.0](https://www.first.org/cvss/v4.0/specification-document) | Versioned technical severity representation | Full vector, score, source, metric group and assumptions; [38](chapters/38.md) distinguishes severity from action priority |

A CWE label does not prove a flaw exists. Choose the narrow supported classification after reviewing the path. A CVE record is not a severity score or proof that a similarly named installed package is affected. A CVSS score alone is not the local risk, exploit likelihood, remediation deadline or release decision. Preserve the version of the vector actually used; do not relabel an earlier record as v4.0.

`FICTIONAL-CH38-001` and `FICTIONAL-CH43-001` are authored exercise identifiers, **not CVE IDs**. The fictional affected-version examples say nothing about actual security of the real named library. Missing real advisory evidence remains missing in [chapter 43](chapters/43.md#worked-example-1-the-dependency-report-is-missing).

### A filled evidence record with an honest result

The following record indexes actual retained capstone facts. It is an authored mapping record, not a newly executed ASVS assessment, independent approval or evidence of deployed HTTP integration. Proposed owner names are the fictional roles from chapter 40.

```json
{
  "evidence_id":"APP-D-READ-01",
  "local_requirements":["CB-READ-01","EXP-01","EXP-04"],
  "standard_reference":"v5.0.0-8.2.2",
  "source_commit":"2c79fe0806a5a788e79afbd0adbc1c4a495a9a5d",
  "artifact_sha256":"ed326bc772909f0dbe064d454488190927593bf18671e6a3c67ac7f017523a5f",
  "implementation":"examples/ch42/capstone.py::collect",
  "report":"examples/ch43/evidence/candidate-run.json",
  "relevant_methods":[
    "test_A41_02_anonymous_cross_workspace_and_route_substitution",
    "test_A41_05_ready_revocation_deactivation_and_inaccessible_selection"
  ],
  "observed_scope":"local fixture identity, SQLite and selected object/revocation paths",
  "result":"local checks passed; production obligation partially verified",
  "gaps":["deployed identity and alternate release paths unverified","production custody and managed-copy controls unverified"],
  "proposed_owner":"Sam; Tess reviews evidence",
  "release_decision":"HOLD"
}
```

Read the [actual candidate run](../examples/ch43/evidence/candidate-run.json), [review ledger](../examples/ch43/release-decision.json) and [chapter 43 control map](chapters/43.md#map-every-mandatory-control). A source archive identifies its bytes; dependencies and hosting configuration remain separate subjects. The [chapter 44 report](../examples/ch44/evidence/verification.json) adds local recovery evidence without closing the production provider/custody/HTTP gaps.

When maintaining this map, check the edition and requirement wording first, then the implementation path, evidence subject, method/result, owner and limit. Update the mapping if any of those changes. Do not repair a missing report by changing its label to pass.

### Appendix verification record

The three membership forms and worked notebook ran with the recorded runtime. The chapter 06 function signature/body was preserved; the unknown-role case retained valid preceding facts. All 44 solution links and other local file/heading links were checked against the actual Markdown, and the JSON example was parsed and compared with the retained candidate identity/results.

ASVS 5.0.0 identifiers were checked against its versioned authorization/data-protection files. Top 10:2025 and API Top 10:2023 category codes were checked against their official lists; SSDF task codes against SP 800-218 version 1.1; SAMM names, CWE entries and CVSS version against their official sources. This is a verified cross-reference, not a fresh standards certification or a claim that every mapped requirement passed.

The appendix programs run on the tested CPython 3.12.14 baseline. Framework results are recorded in the relevant chapters. Earlier framework/provider/key-custody/retention gaps remain as recorded in the linked chapters. These appendices supply navigation and bounded learning evidence, not a production-readiness verdict.

---

[Repository](../README.md) · [Contents](README.md#contents) · [Appendices](appendices.md) · [Indexes](indexes.md) · [References](references.md)
