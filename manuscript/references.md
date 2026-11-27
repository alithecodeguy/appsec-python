# References and edition records

[Repository](../README.md) · [Contents](README.md#contents) · [Appendices](appendices.md) · [Indexes](indexes.md) · [References](references.md)

Which primary source supports the explanation, and which environment produced the result? This bibliography groups the sources actually cited in chapters 01–44 and the appendices. “Cited in” links lead to a section containing the citation. Duplicate document/fragment links are consolidated into one work record.

Source addresses and publication identities were checked on **2026-11-27**. “Retrieved” means the publisher's named document was available for inspection. It does not mean every statement or API was independently retested. The CVE HTML-access limitation is stated at the end.

## Tested edition baseline

The book uses **CPython 3.12.14** and **Django 6.1.3** for its local web examples. The complete observed package set is in [requirements-tested.txt](../requirements-tested.txt), and [tested-versions.md](../tested-versions.md) gives reproduction commands and native-library limits. These are the tested versions for this edition.

| Component | Tested version | Actual evidence and boundary |
| --- | --- | --- |
| CPython | 3.12.14 | The [current report](../examples/verification/current.json) records the interpreter and command results. Python 3.12 documentation URLs follow the maintained branch and may describe a later patch; the execution record identifies the exact tested patch. |
| Django | 6.1.3 | Chapter [19](chapters/19.md#verification-record) passed nine methods, migrations/schema checks, ORM work and real loopback health/private-route requests. Chapters [21](chapters/21.md#verification-record), [22](chapters/22.md#verification-record), [24](chapters/24.md#verification-record), [30](chapters/30.md#verification-record) and [42](chapters/42.md#verification-record-and-next-starting-state) record their actual framework checks. No deployed TLS/proxy/browser claim follows. |
| SQLite | 3.53.1 | Engine loaded by the tested interpreter. Core, refusal, retry and recovery checks inspect stored rows. Other Python builds may bundle another SQLite version. |
| cryptography | 50.0.2 | AEAD/signature fixtures and signed JWT tests ran with this distribution. The cited AEAD, Ed25519 and RSA API pages are versioned 50.0.2 references. Keys are disposable learning keys, not production custody. |
| PyJWT | 2.15.1 | Chapter 22's six signed-token methods passed with controlled clocks, including wrong audience and exact/expired time. Seven separate dictionary-policy methods passed too; those alone are not signature verification. |
| Hypothesis | 6.170.17 | Chapter 30's four HTTP/property methods and shrinking demonstration ran; six service/report methods separately passed, including 93 bounded layouts. Method counts are not inferred from a `max_examples` setting. |
| pytest | 9.2.0 | Chapter [12](chapters/12.md#verification-record) passed 30 tests. |
| mypy | 2.4.1 | Chapter [10](chapters/10.md#verification-record) accepted the narrowed result and intentionally rejected the incorrect file with two errors. The report treats the intended exit status 1 as an expected observation. |
| pip / setuptools / wheel | 26.2.2 / 84.2.1 / 0.48.0 | Selected tested toolchain; all installed distribution versions are recorded. A moving pip `stable` page is not a frozen manual for that exact executable. |
| packaging | 26.4 | Tested package/version comparisons and selected installed environment; fictional advisories remain fictional. |
| OpenSSL | Python: 3.5.8; cryptography: 4.0.3 | Separate observed native backends. A library version does not establish a deployed connection's trust policy or certificate result. |
| Git | 2.54.0 (Apple Git-157) | Candidate source selection and local identity checks. |
| Docker / Compose | 29.8.1 / v5.5.1 | Chapter 35's offline rendering/static checks; no built or running deployment is claimed. |
| Mermaid | 12.3.0 | Chapter 17's syntax checks. Browser rendering remains outside the recorded parser result. |

The current book verifier retains **28 commands and 159 passing test methods**, plus the successful password, session, shrinking, loopback and appendix demonstrations. The separately extracted [candidate report](../examples/ch43/evidence/candidate-run.json) records **20 core passes and three HTTP passes**, with zero skips. Chapter [44's report](../examples/ch44/evidence/verification.json) records nine passing recovery methods. Reports name their own subject and scope; do not add overlapping method counts and present them as unique coverage.

The production release decision remains **HOLD** for actual configuration/identity provisioning, persistent key custody, provider/workload authority, applicable advisory evidence, scheduling, managed-copy removal and recovery/rollback readiness. A local framework pass does not close those controls. Unexecuted Bandit/Semgrep/ZAP/IAST and deployment illustrations have no invented tested tool version. The uv/platform installation instructions are documented bootstrap procedures; Windows installation was not executed in the macOS checks.

## How to use the source records

Repeated URLs, fragments and trailing-slash variants appear once per document. A tagged ASVS file's GitHub view and raw text are one work with two access routes. The NIST SSDF landing page and PDF are one publication. Chapter citations retain all uses without copying the same bibliography record into several subjects.

Standards keep their own editions: **ASVS 5.0.0**, **Top 10:2025**, **API Security Top 10:2023**, **SSDF 1.1 / SP 800-218**, **SAMM version 2**, **SARIF 2.1.0**, **CVSS v4.0**, and the specifically numbered RFCs. Living guidance and drafts are labeled separately. The [appendix standards map](appendices.md#appendix-d-standards-and-verification-map) supplies bounded requirement-to-evidence links; it does not claim certification or a maturity score.

Project documentation is primary evidence for the project's contracts, not proof that an application used them correctly. Authored fixture packages, `FICTIONAL-CH…` advisories, dashboards, scan cards and `CB-…` rules are local teaching inputs, not verified public releases, CVEs or standard identifiers. A moving source should be rechecked when updating the environment or examples.

## Primary sources by subject

### Language and workbench

Python syntax, types, text, imports, environment setup, Git and diagram notation.

| Primary source | Edition and retrieval record | Cited in |
| --- | --- | --- |
| Python project: [15. Floating-Point Arithmetic: Issues and Limitations](https://docs.python.org/3.12/tutorial/floatingpoint.html) | Python 3.12 maintained documentation branch. Retrieved. | [03](chapters/03.md#floats-have-representation-limits) |
| Python project: [2. Lexical analysis](https://docs.python.org/3.12/reference/lexical_analysis.html) | Python 3.12 maintained documentation branch. Retrieved. | [03](chapters/03.md#choose-a-name-that-explains-the-value) |
| Python project: [3. An Informal Introduction to Python](https://docs.python.org/3.12/tutorial/introduction.html) | Python 3.12 maintained documentation branch. Retrieved. | [01](chapters/01.md#further-reading), [03](chapters/03.md#further-reading) |
| Python project: [4. Execution model](https://docs.python.org/3.12/reference/executionmodel.html) | Python 3.12 maintained documentation branch. Retrieved. | [06](chapters/06.md#read-local-scope) |
| Python project: [4. More Control Flow Tools](https://docs.python.org/3.12/tutorial/controlflow.html) | Python 3.12 maintained documentation branch. Retrieved. | [04](chapters/04.md#stop-with-break-and-skip-with-continue), [06](chapters/06.md#create-the-result-within-each-call), [Appendix](appendices.md#find-the-explanation-by-the-task) |
| Python project: [4. Using Python on Windows](https://docs.python.org/3.12/using/windows.html) | Python 3.12 maintained documentation branch. Retrieved. | [02](chapters/02.md#windows-setup-with-powershell) |
| Python project: [5. Data Structures](https://docs.python.org/3.12/tutorial/datastructures.html) | Python 3.12 maintained documentation branch. Retrieved. | [05](chapters/05.md#further-reading) |
| Python project: [5. The import system](https://docs.python.org/3.12/reference/import.html) | Python 3.12 maintained documentation branch. Retrieved. | [06](chapters/06.md#worked-example-2-observe-top-level-execution) |
| Python project: [5. Using Python on a Mac](https://docs.python.org/3.12/using/mac.html) | Python 3.12 maintained documentation branch. Retrieved. | [02](chapters/02.md#macos-setup-with-terminal) |
| Python project: [6. Expressions](https://docs.python.org/3.12/reference/expressions.html) | Python 3.12 maintained documentation branch. Retrieved. | [03](chapters/03.md#compare-values-deliberately), [04](chapters/04.md#group-the-rule-so-its-meaning-stays-visible), [05](chapters/05.md#4-transform-and-group-records-with-predictable-output), [11](chapters/11.md#batch-only-the-permitted-input) |
| Python project: [6. Modules](https://docs.python.org/3.12/tutorial/modules.html) | Python 3.12 maintained documentation branch. Retrieved. | [06](chapters/06.md#understand-where-an-import-finds-a-file) |
| Python project: [7. Input and Output](https://docs.python.org/3.12/tutorial/inputoutput.html) | Python 3.12 maintained documentation branch. Retrieved. | [03](chapters/03.md#build-readable-messages-with-f-strings), [08](chapters/08.md#2-own-the-open-file-with-a-with-block) |
| Python project: [8. Compound statements](https://docs.python.org/3.12/reference/compound_stmts.html) | Python 3.12 maintained documentation branch. Retrieved. | [04](chapters/04.md#further-reading), [08](chapters/08.md#2-own-the-open-file-with-a-with-block), [09](chapters/09.md#observe-cleanup-after-success-parsing-failure-and-opening-failure) |
| Python project: [8. Errors and Exceptions](https://docs.python.org/3.12/tutorial/errors.html) | Python 3.12 maintained documentation branch. Retrieved. | [09](chapters/09.md#worked-example-1-a-missing-settings-file) |
| Python project: [9. Classes](https://docs.python.org/3.12/tutorial/classes.html) | Python 3.12 maintained documentation branch. Retrieved. | [10](chapters/10.md#2-give-related-values-an-instance), [11](chapters/11.md#worked-example-1-request-exactly-three-records) |
| Python project: [__main__ — Top-level code environment](https://docs.python.org/3.12/library/__main__.html) | Python 3.12 maintained documentation branch. Retrieved. | [06](chapters/06.md#worked-example-2-observe-top-level-execution) |
| Python project: [Built-in Exceptions](https://docs.python.org/3.12/library/exceptions.html) | Python 3.12 maintained documentation branch. Retrieved. | [09](chapters/09.md#readability-encoding-and-syntax-are-separate-checks) |
| Python project: [Built-in Functions](https://docs.python.org/3.12/library/functions.html) | Python 3.12 maintained documentation branch. Retrieved. | [01](chapters/01.md#3-read-strings-and-function-calls), [03](chapters/03.md#4-convert-format-and-keep-returned-values), [08](chapters/08.md#csv-fixture-with-a-quoted-comma) |
| Python project: [Built-in Types](https://docs.python.org/3.12/library/stdtypes.html) | Python 3.12 maintained documentation branch. Retrieved. | [03](chapters/03.md#truth-values-answer-a-different-question), [05](chapters/05.md#look-up-a-field-and-keep-absence-distinct), [07](chapters/07.md#split-fields-and-join-a-report), [13](chapters/13.md#primary-sources), [Appendix](appendices.md#find-the-explanation-by-the-task) |
| Python project: [copy — Shallow and deep copy operations](https://docs.python.org/3.12/library/copy.html) | Python 3.12 maintained documentation branch. Retrieved. | [05](chapters/05.md#a-shallow-copy-still-shares-nested-objects) |
| Python project: [dataclasses — Data Classes](https://docs.python.org/3.12/library/dataclasses.html) | Python 3.12 maintained documentation branch. Retrieved. | [10](chapters/10.md#worked-example-1-build-the-complete-draft-dataclass), [13](chapters/13.md#primary-sources) |
| Python project: [enum — Support for enumerations](https://docs.python.org/3.12/library/enum.html) | Python 3.12 maintained documentation branch. Retrieved. | [10](chapters/10.md#worked-example-1-build-the-complete-draft-dataclass) |
| Mermaid project: [Flowcharts Syntax](https://mermaid.js.org/syntax/flowchart.html) | Living maintainer documentation / guidance. Retrieved. | [17](chapters/17.md#primary-sources) |
| Python project: [functools — Higher-order functions and operations on callable objects](https://docs.python.org/3.12/library/functools.html) | Python 3.12 maintained documentation branch. Retrieved. | [11](chapters/11.md#worked-example-2-measure-duration-without-recording-arguments) |
| Git project: [Git - First-Time Git Setup](https://git-scm.com/book/en/v2/Getting-Started-First-Time-Git-Setup) | Living maintainer documentation / guidance. Retrieved. | [02](chapters/02.md#initialize-the-learning-repository) |
| Git project: [Git - git-archive Documentation](https://git-scm.com/docs/git-archive) | Living maintainer documentation / guidance. Retrieved. | [32](chapters/32.md#build-once-and-test-that-artifact) |
| Git project: [Git - git-diff Documentation](https://git-scm.com/docs/git-diff) | Living maintainer documentation / guidance. Retrieved. | [12](chapters/12.md#inspect-the-regression-patch) |
| Git project: [Git - git-init Documentation](https://git-scm.com/docs/git-init) | Living maintainer documentation / guidance. Retrieved. | [02](chapters/02.md#initialize-the-learning-repository) |
| Git project: [Git - git-switch Documentation](https://git-scm.com/docs/git-switch) | Living maintainer documentation / guidance. Retrieved. | [12](chapters/12.md#inspect-the-regression-patch) |
| Git project: [Git - gitignore Documentation](https://git-scm.com/docs/gitignore) | Living maintainer documentation / guidance. Retrieved. | [02](chapters/02.md#decide-which-files-belong-in-history) |
| Git project: [Git - Installing Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) | Living maintainer documentation / guidance. Retrieved. | [02](chapters/02.md#install-or-locate-git) |
| Git project: [Git - Recording Changes to the Repository](https://git-scm.com/book/en/v2/Git-Basics-Recording-Changes-to-the-Repository) | Living maintainer documentation / guidance. Retrieved. | [02](chapters/02.md#decide-which-files-belong-in-history) |
| Astral: [Installation](https://docs.astral.sh/uv/getting-started/installation/) | Living maintainer documentation / guidance. Retrieved. | [02](chapters/02.md#1-install-python-and-locate-its-launcher) |
| Astral: [Installing and managing Python](https://docs.astral.sh/uv/guides/install-python/) | Living maintainer documentation / guidance. Retrieved. | [02](chapters/02.md#linux-setup-with-a-terminal) |
| Python project: [itertools — Functions creating iterators for efficient looping](https://docs.python.org/3.12/library/itertools.html) | Python 3.12 maintained documentation branch. Retrieved. | [11](chapters/11.md#batch-only-the-permitted-input) |
| Python project: [Python Release Python 3.12.14 — Python.org](https://www.python.org/downloads/release/python-31214/) | 3.12.14 release record. Retrieved. | [02](chapters/02.md#1-install-python-and-locate-its-launcher), [19](chapters/19.md#primary-sources) |
| Astral: [Python versions](https://docs.astral.sh/uv/concepts/python-versions/) | Living maintainer documentation / guidance. Retrieved. | [02](chapters/02.md#1-install-python-and-locate-its-launcher) |
| Python project: [re — Regular expression operations](https://docs.python.org/3.12/library/re.html) | Python 3.12 maintained documentation branch. Retrieved. | [07](chapters/07.md#read-the-pattern-before-using-it) |
| Mermaid project: [Sequence diagrams](https://mermaid.js.org/syntax/sequenceDiagram.html) | Living maintainer documentation / guidance. Retrieved. | [17](chapters/17.md#primary-sources) |
| Python project: [Sorting Techniques](https://docs.python.org/3.12/howto/sorting.html) | Python 3.12 maintained documentation branch. Retrieved. | [05](chapters/05.md#4-transform-and-group-records-with-predictable-output) |
| Python project: [sys — System-specific parameters and functions](https://docs.python.org/3.12/library/sys.html) | Python 3.12 maintained documentation branch. Retrieved. | [02](chapters/02.md#worked-example-1-ask-the-running-interpreter-to-identify-itself), [13](chapters/13.md#primary-sources), [14](chapters/14.md#primary-sources) |
| Python project: [Unicode HOWTO](https://docs.python.org/3.12/howto/unicode.html) | Python 3.12 maintained documentation branch. Retrieved. | [07](chapters/07.md#store-those-bytes-then-decode-the-file) |
| Python project: [unicodedata — Unicode Database](https://docs.python.org/3.12/library/unicodedata.html) | Python 3.12 maintained documentation branch. Retrieved. | [07](chapters/07.md#normalization-can-change-the-representation) |
| Python project: [venv — Creation of virtual environments](https://docs.python.org/3.12/library/venv.html) | Python 3.12 maintained documentation branch. Retrieved. | [02](chapters/02.md#3-create-a-project-environment-and-inspect-it) |

### Files, formats, processes and concurrency

Standard-library contracts for I/O, external formats, resource ownership and overlapping work.

| Primary source | Edition and retrieval record | Cited in |
| --- | --- | --- |
| Python project: [1. Command line and environment](https://docs.python.org/3.12/using/cmdline.html) | Python 3.12 maintained documentation branch. Retrieved. | [14](chapters/14.md#primary-sources) |
| Python project: [argparse — Parser for command-line options, arguments and subcommands](https://docs.python.org/3.12/library/argparse.html) | Python 3.12 maintained documentation branch. Retrieved. | [14](chapters/14.md#primary-sources), [37](chapters/37.md#stable-output-is-part-of-the-tool) |
| Python project: [concurrent.futures — Launching parallel tasks](https://docs.python.org/3.12/library/concurrent.futures.html) | Python 3.12 maintained documentation branch. Retrieved. | [28](chapters/28.md#primary-sources), [42](chapters/42.md#primary-sources) |
| Python project: [contextlib — Utilities for with-statement contexts](https://docs.python.org/3.12/library/contextlib.html) | Python 3.12 maintained documentation branch. Retrieved. | [11](chapters/11.md#give-a-stream-a-managed-lifetime), [20](chapters/20.md#primary-sources) |
| Python project: [Coroutines and Tasks](https://docs.python.org/3.12/library/asyncio-task.html) | Python 3.12 maintained documentation branch. Retrieved. | [28](chapters/28.md#primary-sources), [Appendix](appendices.md#find-the-explanation-by-the-task) |
| Python project: [csv — CSV File Reading and Writing](https://docs.python.org/3.12/library/csv.html) | Python 3.12 maintained documentation branch. Retrieved. | [08](chapters/08.md#csv-fixture-with-a-quoted-comma) |
| OWASP: [Error Handling](https://cheatsheetseries.owasp.org/cheatsheets/Error_Handling_Cheat_Sheet.html) | Living maintainer documentation / guidance. Retrieved. | [09](chapters/09.md#match-the-error-message-to-its-reader) |
| Python project: [io — Core tools for working with streams](https://docs.python.org/3.12/library/io.html) | Python 3.12 maintained documentation branch. Retrieved. | [Appendix](appendices.md#find-the-explanation-by-the-task) |
| Python project: [json — JSON encoder and decoder](https://docs.python.org/3.12/library/json.html) | Python 3.12 maintained documentation branch. Retrieved. | [08](chapters/08.md#json-fixture-with-an-absent-key), [20](chapters/20.md#primary-sources), [25](chapters/25.md#primary-sources), [26](chapters/26.md#primary-sources), [33](chapters/33.md#choose-severity-for-investigation-not-accusation), [Appendix](appendices.md#find-the-explanation-by-the-task) |
| Python project: [os — Miscellaneous operating system interfaces](https://docs.python.org/3.12/library/os.html) | Python 3.12 maintained documentation branch. Retrieved. | [09](chapters/09.md#worked-example-2-a-genuine-file-permission-refusal), [13](chapters/13.md#primary-sources), [25](chapters/25.md#primary-sources) |
| Python project: [pathlib — Object-oriented filesystem paths](https://docs.python.org/3.12/library/pathlib.html) | Python 3.12 maintained documentation branch. Retrieved. | [07](chapters/07.md#store-those-bytes-then-decode-the-file), [08](chapters/08.md#worked-example-1-read-the-persian-title-as-utf-8-text), [13](chapters/13.md#primary-sources), [18](chapters/18.md#primary-sources), [Appendix](appendices.md#find-the-explanation-by-the-task) |
| Python project: [pickle — Python object serialization](https://docs.python.org/3.12/library/pickle.html) | Python 3.12 maintained documentation branch. Retrieved. | [25](chapters/25.md#primary-sources) |
| Python project: [Queues](https://docs.python.org/3.12/library/asyncio-queue.html) | Python 3.12 maintained documentation branch. Retrieved. | [28](chapters/28.md#primary-sources) |
| Python project: [subprocess — Subprocess management](https://docs.python.org/3.12/library/subprocess.html) | Python 3.12 maintained documentation branch. Retrieved. | [14](chapters/14.md#primary-sources) |
| Python project: [tempfile — Generate temporary files and directories](https://docs.python.org/3.12/library/tempfile.html) | Python 3.12 maintained documentation branch. Retrieved. | [09](chapters/09.md#observe-cleanup-after-success-parsing-failure-and-opening-failure), [14](chapters/14.md#primary-sources), [18](chapters/18.md#primary-sources), [25](chapters/25.md#primary-sources) |
| Python project: [threading — Thread-based parallelism](https://docs.python.org/3.12/library/threading.html) | Python 3.12 maintained documentation branch. Retrieved. | [28](chapters/28.md#primary-sources), [42](chapters/42.md#primary-sources) |
| Python project: [time — Time access and conversions](https://docs.python.org/3.12/library/time.html) | Python 3.12 maintained documentation branch. Retrieved. | [11](chapters/11.md#worked-example-2-measure-duration-without-recording-arguments), [16](chapters/16.md#primary-sources) |
| Python project: [XML Processing Modules](https://docs.python.org/3.12/library/xml.html) | Python 3.12 maintained documentation branch. Retrieved. | [25](chapters/25.md#primary-sources) |
| Python project: [zipfile — Work with ZIP archives](https://docs.python.org/3.12/library/zipfile.html) | Python 3.12 maintained documentation branch. Retrieved. | [25](chapters/25.md#primary-sources) |

### Testing and source analysis

Test libraries, type checking, source inspection and bounded scanner guidance.

| Primary source | Edition and retrieval record | Cited in |
| --- | --- | --- |
| Hypothesis project: [API Reference](https://hypothesis.readthedocs.io/en/latest/reference/api.html) | Moving latest; retrieved header 6.170.17. Retrieved. | [30](chapters/30.md#shrink-a-failure-without-shrinking-away-the-relationship) |
| Python project: [ast — Abstract Syntax Trees](https://docs.python.org/3.12/library/ast.html) | Python 3.12 maintained documentation branch. Retrieved. | [37](chapters/37.md#worked-example-2-the-same-name-in-a-comment-and-an-assignment) |
| Bandit: [B608: hardcoded_sql_expressions](https://bandit.readthedocs.io/en/latest/plugins/b608_hardcoded_sql_expressions.html) | Living maintainer documentation / guidance. Retrieved. | [29](chapters/29.md#two-supplied-static-findings) |
| pytest project: [Get Started](https://docs.pytest.org/en/stable/getting-started.html) | Living maintainer documentation / guidance. Retrieved. | [12](chapters/12.md#install-pytest-in-the-learning-environment) |
| Bandit: [Getting Started](https://bandit.readthedocs.io/en/latest/start.html) | Living maintainer documentation / guidance. Retrieved. | [29](chapters/29.md#primary-sources) |
| mypy project: [Getting started](https://mypy.readthedocs.io/en/stable/getting_started.html) | Moving stable; 2.4.1 is the locally tested checker version. Retrieved. | [10](chapters/10.md#give-the-checker-two-mistakes-to-find) |
| pytest project: [How to capture stdout/stderr output](https://docs.pytest.org/en/stable/how-to/capture-stdout-stderr.html) | Living maintainer documentation / guidance. Retrieved. | [13](chapters/13.md#primary-sources) |
| pytest project: [How to monkeypatch/mock modules and environments](https://docs.pytest.org/en/stable/how-to/monkeypatch.html) | Living maintainer documentation / guidance. Retrieved. | [12](chapters/12.md#control-an-existing-timing-wrapper), [13](chapters/13.md#primary-sources) |
| pytest project: [How to parametrize fixtures and test functions](https://docs.pytest.org/en/stable/how-to/parametrize.html) | Living maintainer documentation / guidance. Retrieved. | [12](chapters/12.md#check-the-quota-neighborhood-and-expected-exceptions), [Appendix](appendices.md#framework-and-tool-shelf) |
| pytest project: [How to use fixtures](https://docs.pytest.org/en/stable/how-to/fixtures.html) | Living maintainer documentation / guidance. Retrieved. | [12](chapters/12.md#worked-example-1-test-the-access-rule-across-roles) |
| pytest project: [How to use temporary directories and files in tests](https://docs.pytest.org/en/stable/how-to/tmp_path.html) | Living maintainer documentation / guidance. Retrieved. | [12](chapters/12.md#create-a-file-inside-a-test-owned-directory) |
| pytest project: [How to write and report assertions in tests](https://docs.pytest.org/en/stable/how-to/assert.html) | Living maintainer documentation / guidance. Retrieved. | [12](chapters/12.md#write-the-boundary-expectation-first) |
| OWASP: [Interactive Application Security Testing (IAST) - OWASP DevSecOps Guideline](https://owasp.github.io/DevSecOpsGuideline/2-Process/2-4-Test/2-4-1-Interactive-Application-Security-Testing/) | Living maintainer documentation / guidance. Retrieved. | [30](chapters/30.md#3-dast-iast-coverage-and-limits) |
| Hypothesis project: [Introduction to Hypothesis](https://hypothesis.readthedocs.io/en/latest/tutorial/introduction.html) | Moving latest; retrieved header 6.170.17. Retrieved. | [30](chapters/30.md#primary-sources) |
| Python project: [pdb — The Python Debugger](https://docs.python.org/3.12/library/pdb.html) | Python 3.12 maintained documentation branch. Retrieved. | [09](chapters/09.md#4-reduce-a-bug-and-inspect-it-with-a-breakpoint) |
| Hypothesis project: [Replaying failed tests](https://hypothesis.readthedocs.io/en/latest/tutorial/replaying-failures.html) | Moving latest; retrieved header 6.170.17. Retrieved. | [30](chapters/30.md#shrink-a-failure-without-shrinking-away-the-relationship) |
| Semgrep: [Rule structure syntax - Semgrep](https://docs.semgrep.dev/writing-rules/rule-syntax) | Living maintainer documentation / guidance. Retrieved. | [29](chapters/29.md#two-supplied-static-findings) |
| OWASP: [Source Code Analysis Tools](https://community.owasp.org/Source_Code_Analysis_Tools) | Living maintainer documentation / guidance. Retrieved. | [29](chapters/29.md#2-sast-rule-scope-and-taint-flow-vocabulary) |
| Hypothesis project: [Strategies Reference](https://hypothesis.readthedocs.io/en/latest/reference/strategies.html) | Moving latest; retrieved header 6.170.17. Retrieved. | [30](chapters/30.md#describe-the-input-domain-with-strategies) |
| Semgrep: [Taint analysis overview - Semgrep](https://docs.semgrep.dev/writing-rules/data-flow/taint-mode/overview) | Living maintainer documentation / guidance. Retrieved. | [29](chapters/29.md#2-sast-rule-scope-and-taint-flow-vocabulary) |
| Python project: [tokenize — Tokenizer for Python source](https://docs.python.org/3.12/library/tokenize.html) | Python 3.12 maintained documentation branch. Retrieved. | [37](chapters/37.md#worked-example-2-the-same-name-in-a-comment-and-an-assignment) |
| mypy project: [Type narrowing](https://mypy.readthedocs.io/en/stable/type_narrowing.html) | Moving stable; 2.4.1 is the locally tested checker version. Retrieved. | [10](chapters/10.md#narrow-the-optional-value-before-returning-it) |
| Python project: [typing — Support for type hints](https://docs.python.org/3.12/library/typing.html) | Python 3.12 maintained documentation branch. Retrieved. | [10](chapters/10.md#distinguish-static-information-from-runtime-enforcement), [29](chapters/29.md#worked-example-1-compare-the-warning-with-the-actual-argument-type), [Appendix](appendices.md#find-the-explanation-by-the-task) |
| Python project: [unittest — Unit testing framework](https://docs.python.org/3.12/library/unittest.html) | Python 3.12 maintained documentation branch. Retrieved. | [20](chapters/20.md#primary-sources), [21](chapters/21.md#primary-sources) |
| OWASP: [Vulnerability Scanning Tools](https://community.owasp.org/Vulnerability_Scanning_Tools) | Living maintainer documentation / guidance. Retrieved. | [30](chapters/30.md#3-dast-iast-coverage-and-limits) |
| ZAP project: [ZAP – Passive Scanner Add-on](https://www.zaproxy.org/docs/desktop/addons/passive-scanner/) | Living maintainer documentation / guidance. Retrieved. | [30](chapters/30.md#3-dast-iast-coverage-and-limits) |

### Relational data and transactions

The Python driver and SQLite documentation; upstream SQLite pages are living documentation, not a snapshot of the recorded engine build.

| Primary source | Edition and retrieval record | Cited in |
| --- | --- | --- |
| SQLite project: [ALTER TABLE](https://www.sqlite.org/lang_altertable.html) | Living maintainer documentation / guidance. Retrieved. | [15](chapters/15.md#primary-sources) |
| SQLite project: [Atomic Commit In SQLite](https://www.sqlite.org/atomiccommit.html) | Living maintainer documentation / guidance. Retrieved. | [33](chapters/33.md#4-delivery-failures-buffering-monitoring-and-audit-integrity) |
| SQLite project: [CREATE TABLE](https://www.sqlite.org/lang_createtable.html) | Living maintainer documentation / guidance. Retrieved. | [15](chapters/15.md#primary-sources), [20](chapters/20.md#primary-sources) |
| SQLite project: [EXPLAIN QUERY PLAN](https://www.sqlite.org/eqp.html) | Living maintainer documentation / guidance. Retrieved. | [15](chapters/15.md#primary-sources) |
| SQLite project: [Isolation In SQLite](https://www.sqlite.org/isolation.html) | Living maintainer documentation / guidance. Retrieved. | [23](chapters/23.md#primary-sources), [28](chapters/28.md#primary-sources) |
| SQLite project: [Pragma statements supported by SQLite](https://www.sqlite.org/pragma.html) | Living maintainer documentation / guidance. Retrieved. | [15](chapters/15.md#primary-sources) |
| SQLite project: [Query Planning](https://www.sqlite.org/queryplanner.html) | Living maintainer documentation / guidance. Retrieved. | [15](chapters/15.md#primary-sources) |
| SQLite project: [Quirks, Caveats, and Gotchas In SQLite](https://www.sqlite.org/quirks.html) | Living maintainer documentation / guidance. Retrieved. | [15](chapters/15.md#primary-sources) |
| SQLite project: [Savepoints](https://www.sqlite.org/lang_savepoint.html) | Living maintainer documentation / guidance. Retrieved. | [42](chapters/42.md#primary-sources) |
| SQLite project: [SQLite Autoincrement](https://www.sqlite.org/autoinc.html) | Living maintainer documentation / guidance. Retrieved. | [42](chapters/42.md#primary-sources) |
| SQLite project: [SQLite Backup API](https://www.sqlite.org/backup.html) | Living maintainer documentation / guidance. Retrieved. | [36](chapters/36.md#worked-example-2-compare-the-candidate-with-the-known-backup), [44](chapters/44.md#primary-sources) |
| SQLite project: [SQLite Foreign Key Support](https://www.sqlite.org/foreignkeys.html) | Living maintainer documentation / guidance. Retrieved. | [15](chapters/15.md#primary-sources) |
| Python project: [sqlite3 — DB-API 2.0 interface for SQLite databases](https://docs.python.org/3.12/library/sqlite3.html) | Python 3.12 maintained documentation branch. Retrieved. | [15](chapters/15.md#primary-sources), [20](chapters/20.md#primary-sources), [21](chapters/21.md#primary-sources), [23](chapters/23.md#primary-sources), [25](chapters/25.md#primary-sources), [26](chapters/26.md#primary-sources), [28](chapters/28.md#primary-sources), [29](chapters/29.md#worked-example-1-compare-the-warning-with-the-actual-argument-type), [36](chapters/36.md#worked-example-2-compare-the-candidate-with-the-known-backup), [42](chapters/42.md#primary-sources), [44](chapters/44.md#primary-sources), [Appendix](appendices.md#find-the-explanation-by-the-task) |
| SQLite project: [The ON CONFLICT Clause](https://www.sqlite.org/lang_conflict.html) | Living maintainer documentation / guidance. Retrieved. | [28](chapters/28.md#primary-sources) |
| SQLite project: [Transaction](https://www.sqlite.org/lang_transaction.html) | Living maintainer documentation / guidance. Retrieved. | [15](chapters/15.md#primary-sources), [20](chapters/20.md#primary-sources), [23](chapters/23.md#primary-sources), [26](chapters/26.md#primary-sources), [28](chapters/28.md#primary-sources), [33](chapters/33.md#4-delivery-failures-buffering-monitoring-and-audit-integrity), [42](chapters/42.md#primary-sources) |
| SQLite project: [UPSERT](https://www.sqlite.org/lang_upsert.html) | Living maintainer documentation / guidance. Retrieved. | [28](chapters/28.md#primary-sources), [42](chapters/42.md#primary-sources) |

### Django service and browser integration

All Django sources below use the cited 6.1 documentation branch. Only the 6.1.3 release note is a patch-specific release record.

| Primary source | Edition and retrieval record | Cited in |
| --- | --- | --- |
| Django project: [Built-in template tags and filters](https://docs.djangoproject.com/en/6.1/ref/templates/builtins/) | 6.1 branch. Retrieved. | [24](chapters/24.md#primary-sources) |
| Django project: [Clickjacking Protection](https://docs.djangoproject.com/en/6.1/ref/clickjacking/) | 6.1 branch. Retrieved. | [24](chapters/24.md#primary-sources) |
| Django project: [Content Security Policy](https://docs.djangoproject.com/en/6.1/ref/csp/) | 6.1 branch. Retrieved. | [24](chapters/24.md#primary-sources), [30](chapters/30.md#worked-example-present-does-not-mean-enforced) |
| Django project: [Cross Site Request Forgery protection](https://docs.djangoproject.com/en/6.1/ref/csrf/) | 6.1 branch. Retrieved. | [24](chapters/24.md#primary-sources), [42](chapters/42.md#primary-sources) |
| Django project: [Database transactions](https://docs.djangoproject.com/en/6.1/topics/db/transactions/) | 6.1 branch. Retrieved. | [23](chapters/23.md#primary-sources) |
| Django project: [Deployment checklist](https://docs.djangoproject.com/en/6.1/howto/deployment/checklist/) | 6.1 branch. Retrieved. | [19](chapters/19.md#primary-sources), [35](chapters/35.md#primary-sources) |
| Django project: [Django 6.1.3 release notes](https://docs.djangoproject.com/en/6.1/releases/6.1.3/) | 6.1.3 release note. Retrieved. | [19](chapters/19.md#primary-sources) |
| Django project: [File Uploads](https://docs.djangoproject.com/en/6.1/topics/http/file-uploads/) | 6.1 branch. Retrieved. | [25](chapters/25.md#primary-sources) |
| Django project: [How to provide initial data for models](https://docs.djangoproject.com/en/6.1/howto/initial-data/) | 6.1 branch. Retrieved. | [19](chapters/19.md#primary-sources) |
| Django project: [How to use Django’s Content Security Policy](https://docs.djangoproject.com/en/6.1/howto/csp/) | 6.1 branch. Retrieved. | [24](chapters/24.md#primary-sources) |
| Django project: [How to use sessions](https://docs.djangoproject.com/en/6.1/topics/http/sessions/) | 6.1 branch. Retrieved. | [22](chapters/22.md#primary-sources) |
| Django project: [Making queries](https://docs.djangoproject.com/en/6.1/topics/db/queries/) | 6.1 branch. Retrieved. | [19](chapters/19.md#primary-sources), [23](chapters/23.md#primary-sources) |
| Django project: [Middleware](https://docs.djangoproject.com/en/6.1/topics/http/middleware/) | 6.1 branch. Retrieved. | [19](chapters/19.md#primary-sources) |
| Django project: [Migrations](https://docs.djangoproject.com/en/6.1/topics/migrations/) | 6.1 branch. Retrieved. | [19](chapters/19.md#primary-sources) |
| Django project: [Model instance reference](https://docs.djangoproject.com/en/6.1/ref/models/instances/) | 6.1 branch. Retrieved. | [19](chapters/19.md#primary-sources) |
| Django project: [Models](https://docs.djangoproject.com/en/6.1/topics/db/models/) | 6.1 branch. Retrieved. | [19](chapters/19.md#primary-sources) |
| Django project: [Password management in Django](https://docs.djangoproject.com/en/6.1/topics/auth/passwords/) | 6.1 branch. Retrieved. | [21](chapters/21.md#primary-sources) |
| Django project: [QuerySet API reference](https://docs.djangoproject.com/en/6.1/ref/models/querysets/) | 6.1 branch. Retrieved. | [23](chapters/23.md#primary-sources) |
| Django project: [Request and response objects](https://docs.djangoproject.com/en/6.1/ref/request-response/) | 6.1 branch. Retrieved. | [19](chapters/19.md#primary-sources), [20](chapters/20.md#primary-sources) |
| Django project: [Settings](https://docs.djangoproject.com/en/6.1/ref/settings/) | 6.1 branch. Retrieved. | [35](chapters/35.md#host-scheme-and-identity-are-different-claims) |
| Django project: [Testing tools](https://docs.djangoproject.com/en/6.1/topics/testing/tools/) | 6.1 branch. Retrieved. | [19](chapters/19.md#primary-sources), [24](chapters/24.md#primary-sources), [30](chapters/30.md#know-what-the-client-exercises), [42](chapters/42.md#primary-sources), [Appendix](appendices.md#framework-and-tool-shelf) |
| Django project: [The Django admin site](https://docs.djangoproject.com/en/6.1/ref/contrib/admin/) | 6.1 branch. Retrieved. | [23](chapters/23.md#primary-sources) |
| Django project: [The Django template language](https://docs.djangoproject.com/en/6.1/ref/templates/language/) | 6.1 branch. Retrieved. | [24](chapters/24.md#primary-sources) |
| Django project: [Using the Django authentication system](https://docs.djangoproject.com/en/6.1/topics/auth/default/) | 6.1 branch. Retrieved. | [21](chapters/21.md#primary-sources), [22](chapters/22.md#primary-sources) |
| Django project: [View decorators](https://docs.djangoproject.com/en/6.1/topics/http/decorators/) | 6.1 branch. Retrieved. | [19](chapters/19.md#primary-sources) |
| Django project: [Writing your first Django app, part 1](https://docs.djangoproject.com/en/6.1/intro/tutorial01/) | 6.1 branch. Retrieved. | [19](chapters/19.md#primary-sources) |

### HTTP, networking and browser standards

Published RFCs, living browser standards and the separately labeled cookie/CSP drafts.

| Primary source | Edition and retrieval record | Cited in |
| --- | --- | --- |
| W3C: [Content Security Policy Level 3](https://www.w3.org/TR/CSP3/) | Level 3 Working Draft; not a W3C Recommendation. Retrieved. | [24](chapters/24.md#primary-sources), [30](chapters/30.md#worked-example-present-does-not-mean-enforced) |
| IETF HTTP Working Group: [Cookies: HTTP State Management Mechanism](https://httpwg.org/http-extensions/draft-ietf-httpbis-rfc6265bis.html) | Internet-Draft, latest; dated 2026-11-23, not an approved replacement RFC. Retrieved. | [24](chapters/24.md#primary-sources) |
| IANA: [Example Domains](https://www.iana.org/help/example-domains) | Living maintainer documentation / guidance. Retrieved. | [16](chapters/16.md#primary-sources) |
| WHATWG: [Fetch Standard](https://fetch.spec.whatwg.org/) | Living Standard. Retrieved. | [24](chapters/24.md#primary-sources) |
| WHATWG: [HTML Standard](https://html.spec.whatwg.org/multipage/browsers.html) | Living Standard. Retrieved. | [24](chapters/24.md#primary-sources) |
| Python project: [http.client — HTTP protocol client](https://docs.python.org/3.12/library/http.client.html) | Python 3.12 maintained documentation branch. Retrieved. | [16](chapters/16.md#primary-sources) |
| RFC Editor / IETF: [RFC 1034: Domain Names — Concepts and Facilities](https://www.rfc-editor.org/rfc/rfc1034.html) | Published RFC; use the numbered document. Retrieved. | [16](chapters/16.md#primary-sources) |
| RFC Editor / IETF: [RFC 5789: PATCH Method for HTTP](https://www.rfc-editor.org/rfc/rfc5789.html) | Published RFC; use the numbered document. Retrieved. | [20](chapters/20.md#primary-sources) |
| RFC Editor / IETF: [RFC 6265: HTTP State Management Mechanism](https://www.rfc-editor.org/rfc/rfc6265.html) | Published RFC; use the numbered document. Retrieved. | [24](chapters/24.md#primary-sources) |
| RFC Editor / IETF: [RFC 8259: The JavaScript Object Notation (JSON) Data Interchange Format](https://www.rfc-editor.org/rfc/rfc8259.html) | Published RFC; use the numbered document. Retrieved. | [16](chapters/16.md#primary-sources), [20](chapters/20.md#primary-sources) |
| RFC Editor / IETF: [RFC 8446: The Transport Layer Security (TLS) Protocol Version 1.3](https://www.rfc-editor.org/rfc/rfc8446.html) | Published RFC; use the numbered document. Retrieved. | [16](chapters/16.md#primary-sources) |
| RFC Editor / IETF: [RFC 9110: HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110.html) | Published RFC; use the numbered document. Retrieved. | [16](chapters/16.md#primary-sources), [20](chapters/20.md#primary-sources) |
| RFC Editor / IETF: [RFC 9111: HTTP Caching](https://www.rfc-editor.org/rfc/rfc9111.html) | Published RFC; use the numbered document. Retrieved. | [16](chapters/16.md#primary-sources), [24](chapters/24.md#primary-sources) |
| RFC Editor / IETF: [RFC 9293: Transmission Control Protocol (TCP)](https://www.rfc-editor.org/rfc/rfc9293.html) | Published RFC; use the numbered document. Retrieved. | [16](chapters/16.md#primary-sources) |
| IANA: [Special-Use Domain Names](https://www.iana.org/assignments/special-use-domain-names/special-use-domain-names.xhtml) | Living maintainer documentation / guidance. Retrieved. | [16](chapters/16.md#primary-sources) |
| Python project: [ssl — TLS/SSL wrapper for socket objects](https://docs.python.org/3.12/library/ssl.html) | Python 3.12 maintained documentation branch. Retrieved. | [16](chapters/16.md#primary-sources) |
| Python project: [urllib.parse — Parse URLs into components](https://docs.python.org/3.12/library/urllib.parse.html) | Python 3.12 maintained documentation branch. Retrieved. | [16](chapters/16.md#primary-sources) |
| Python project: [urllib.request — Extensible library for opening URLs](https://docs.python.org/3.12/library/urllib.request.html) | Python 3.12 maintained documentation branch. Retrieved. | [26](chapters/26.md#primary-sources) |

### Accounts, identity and cryptography

Authentication guidance, token protocols, maintained cryptographic APIs and key-management guidance.

| Primary source | Edition and retrieval record | Cited in |
| --- | --- | --- |
| PyJWT project: [API Reference](https://pyjwt.readthedocs.io/en/2.15.1/api.html) | 2.15.1 API documentation. Retrieved. | [22](chapters/22.md#primary-sources) |
| PyCA: [Authenticated encryption](https://cryptography.io/en/50.0.2/hazmat/primitives/aead/) | 50.0.2 API documentation. Retrieved. | [27](chapters/27.md#primary-sources), [28](chapters/28.md#primary-sources), [41](chapters/41.md#primary-sources), [42](chapters/42.md#primary-sources) |
| OWASP: [Authentication](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html) | Living maintainer documentation / guidance. Retrieved. | [21](chapters/21.md#primary-sources) |
| OWASP: [Cryptographic Storage](https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html) | Living maintainer documentation / guidance. Retrieved. | [27](chapters/27.md#primary-sources) |
| PyCA: [Ed25519 signing](https://cryptography.io/en/50.0.2/hazmat/primitives/asymmetric/ed25519/) | 50.0.2 API documentation. Retrieved. | [27](chapters/27.md#primary-sources), [32](chapters/32.md#verify-authority-and-bytes-before-copying) |
| OpenID Foundation: [Final: OpenID Connect Core 1.0 incorporating errata set 2](https://openid.net/specs/openid-connect-core-1_0.html) | Living maintainer documentation / guidance. Retrieved. | [22](chapters/22.md#primary-sources) |
| OWASP: [Forgot Password](https://cheatsheetseries.owasp.org/cheatsheets/Forgot_Password_Cheat_Sheet.html) | Living maintainer documentation / guidance. Retrieved. | [21](chapters/21.md#primary-sources) |
| Python project: [hashlib — Secure hashes and message digests](https://docs.python.org/3.12/library/hashlib.html) | Python 3.12 maintained documentation branch. Retrieved. | [21](chapters/21.md#primary-sources), [27](chapters/27.md#primary-sources) |
| Python project: [hmac — Keyed-Hashing for Message Authentication](https://docs.python.org/3.12/library/hmac.html) | Python 3.12 maintained documentation branch. Retrieved. | [26](chapters/26.md#primary-sources), [27](chapters/27.md#primary-sources) |
| OWASP: [Key Management](https://cheatsheetseries.owasp.org/cheatsheets/Key_Management_Cheat_Sheet.html) | Living maintainer documentation / guidance. Retrieved. | [27](chapters/27.md#primary-sources), [44](chapters/44.md#primary-sources) |
| OWASP: [Multifactor Authentication](https://cheatsheetseries.owasp.org/cheatsheets/Multifactor_Authentication_Cheat_Sheet.html) | Living maintainer documentation / guidance. Retrieved. | [21](chapters/21.md#primary-sources) |
| RFC Editor / IETF: [RFC 7009: OAuth 2.0 Token Revocation](https://www.rfc-editor.org/rfc/rfc7009.html) | Published RFC; use the numbered document. Retrieved. | [22](chapters/22.md#primary-sources) |
| RFC Editor / IETF: [RFC 7519: JSON Web Token (JWT)](https://www.rfc-editor.org/rfc/rfc7519.html) | Published RFC; use the numbered document. Retrieved. | [22](chapters/22.md#primary-sources) |
| RFC Editor / IETF: [RFC 7636: Proof Key for Code Exchange by OAuth Public Clients](https://www.rfc-editor.org/rfc/rfc7636.html) | Published RFC; use the numbered document. Retrieved. | [22](chapters/22.md#primary-sources) |
| RFC Editor / IETF: [RFC 7662: OAuth 2.0 Token Introspection](https://www.rfc-editor.org/rfc/rfc7662.html) | Published RFC; use the numbered document. Retrieved. | [22](chapters/22.md#primary-sources) |
| RFC Editor / IETF: [RFC 8725: JSON Web Token Best Current Practices](https://www.rfc-editor.org/rfc/rfc8725.html) | Published RFC; use the numbered document. Retrieved. | [22](chapters/22.md#primary-sources) |
| RFC Editor / IETF: [RFC 9700: Best Current Practice for OAuth 2.0 Security](https://www.rfc-editor.org/rfc/rfc9700.html) | Published RFC; use the numbered document. Retrieved. | [22](chapters/22.md#primary-sources) |
| PyCA: [RSA](https://cryptography.io/en/50.0.2/hazmat/primitives/asymmetric/rsa/) | 50.0.2 API documentation. Retrieved. | [22](chapters/22.md#primary-sources) |
| Python project: [secrets — Generate secure random numbers for managing secrets](https://docs.python.org/3.12/library/secrets.html) | Python 3.12 maintained documentation branch. Retrieved. | [21](chapters/21.md#primary-sources), [27](chapters/27.md#primary-sources), [39](chapters/39.md#complete-local-laboratory) |
| NIST: [SP 800-38D, Recommendation for Block Cipher Modes of Operation: Galois/Counter Mode (GCM) and GMAC — CSRC](https://csrc.nist.gov/pubs/sp/800/38/d/final) | SP 800-38D, final (2007); retain its revision identity. Retrieved. | [27](chapters/27.md#primary-sources) |
| NIST: [SP 800-63B-4: Authentication and Authenticator Management](https://pages.nist.gov/800-63-4/sp800-63b.html) | SP 800-63B-4, final (2025). Retrieved. | [21](chapters/21.md#primary-sources) |
| W3C: [Web Authentication: An API for accessing Public Key Credentials - Level 3](https://www.w3.org/TR/webauthn-3/) | Level 3 Recommendation, 2026-08-25. Retrieved. | [21](chapters/21.md#primary-sources) |

### Uploads, webhooks and outbound integrations

Application policies and provider protocols. The synthetic webhook envelope in the book is not the Stripe protocol.

| Primary source | Edition and retrieval record | Cited in |
| --- | --- | --- |
| OWASP: [File Upload](https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html) | Living maintainer documentation / guidance. Retrieved. | [25](chapters/25.md#primary-sources) |
| JSON Schema project: [JSON Schema - object](https://json-schema.org/understanding-json-schema/reference/object) | Living maintainer documentation / guidance. Retrieved. | [20](chapters/20.md#primary-sources) |
| PyYAML project: [PyYAML Documentation](https://pyyaml.org/wiki/PyYAMLDocumentation) | Living maintainer documentation / guidance. Retrieved. | [25](chapters/25.md#primary-sources) |
| Stripe: [Receive Stripe events in your webhook endpoint](https://docs.stripe.com/webhooks) | Living maintainer documentation / guidance. Retrieved. | [26](chapters/26.md#primary-sources) |
| OWASP: [Server Side Request Forgery Prevention](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html) | Living maintainer documentation / guidance. Retrieved. | [26](chapters/26.md#primary-sources) |

### Threat models, authorization and private data

Design guidance and selected verification requirements; a citation alone is not a conformance result.

| Primary source | Edition and retrieval record | Cited in |
| --- | --- | --- |
| OWASP: [API1:2023 Broken Object Level Authorization - OWASP API Security Top 10](https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/) | 2023 API risk-category edition. Retrieved. | [23](chapters/23.md#primary-sources) |
| OWASP: [API3:2023 Broken Object Property Level Authorization - OWASP API Security Top 10](https://owasp.org/API-Security/editions/2023/en/0xa3-broken-object-property-level-authorization/) | 2023 API risk-category edition. Retrieved. | [20](chapters/20.md#primary-sources), [23](chapters/23.md#primary-sources) |
| OWASP: [API5:2023 Broken Function Level Authorization - OWASP API Security Top 10](https://owasp.org/API-Security/editions/2023/en/0xa5-broken-function-level-authorization/) | 2023 API risk-category edition. Retrieved. | [23](chapters/23.md#primary-sources) |
| OWASP: [API9:2023 Improper Inventory Management - OWASP API Security Top 10](https://owasp.org/API-Security/editions/2023/en/0xa9-improper-inventory-management/) | 2023 API risk-category edition. Retrieved. | [20](chapters/20.md#primary-sources) |
| OWASP: [ASVS 5.0.0, V14 Data Protection (tagged GitHub view)](https://github.com/OWASP/ASVS/blob/v5.0.0/5.0/en/0x23-V14-Data-Protection.md); [ASVS 5.0.0, V14 Data Protection (tagged raw text)](https://raw.githubusercontent.com/OWASP/ASVS/v5.0.0/5.0/en/0x23-V14-Data-Protection.md) | Pinned ASVS v5.0.0 tag. Retrieved. | [18](chapters/18.md#primary-sources), [Appendix](appendices.md#use-the-right-kind-of-reference) |
| OWASP: [ASVS 5.0.0, V8 Authorization](https://raw.githubusercontent.com/OWASP/ASVS/v5.0.0/5.0/en/0x17-V8-Authorization.md) | Pinned ASVS v5.0.0 tag. Retrieved. | [Appendix](appendices.md#use-the-right-kind-of-reference) |
| OWASP: [Authorization](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html) | Living maintainer documentation / guidance. Retrieved. | [04](chapters/04.md#worked-example-1-decide-whether-mina-may-read-the-note), [17](chapters/17.md#primary-sources), [18](chapters/18.md#primary-sources), [23](chapters/23.md#primary-sources), [29](chapters/29.md#4-confidence-false-positives-fixes-and-regression-coverage), [41](chapters/41.md#primary-sources), [43](chapters/43.md#primary-sources), [44](chapters/44.md#primary-sources) |
| OWASP: [Insecure Direct Object Reference Prevention](https://cheatsheetseries.owasp.org/cheatsheets/Insecure_Direct_Object_Reference_Prevention_Cheat_Sheet.html) | Living maintainer documentation / guidance. Retrieved. | [41](chapters/41.md#primary-sources) |
| OWASP: [Overview — OWASP Application Security Verification Standard](https://asvs.owasp.org/) | Living project overview; exact mappings use the pinned sources below. Retrieved. | [18](chapters/18.md#primary-sources) |
| OWASP: [OWASP Threat Modeling Project](https://owasp.org/www-project-threat-modeling/) | Living maintainer documentation / guidance. Retrieved. | [17](chapters/17.md#primary-sources) |
| OWASP: [OWASP Top 10 API Security Risks – 2023 - OWASP API Security Top 10](https://owasp.org/API-Security/editions/2023/en/0x11-t10/) | 2023 API risk-category edition. Retrieved. | [Appendix](appendices.md#use-the-right-kind-of-reference) |
| OWASP: [OWASP Top 10:2025](https://owasp.org/Top10/2025/) | 2025 risk-category edition. Retrieved. | [Appendix](appendices.md#use-the-right-kind-of-reference) |
| OWASP: [Threat Modeling](https://cheatsheetseries.owasp.org/cheatsheets/Threat_Modeling_Cheat_Sheet.html) | Living maintainer documentation / guidance. Retrieved. | [41](chapters/41.md#primary-sources) |
| OWASP: [Threat Modeling](https://owasp.org/www-community/Threat_Modeling) | Living maintainer documentation / guidance. Retrieved. | [17](chapters/17.md#primary-sources) |
| OWASP: [User Privacy Protection](https://cheatsheetseries.owasp.org/cheatsheets/User_Privacy_Protection_Cheat_Sheet.html) | Living maintainer documentation / guidance. Retrieved. | [18](chapters/18.md#primary-sources) |

### Packaging, dependencies and provenance

Build/distribution formats, installer contracts and component/provenance models. Custom teaching inventories are not automatically standard SBOMs.

| Primary source | Edition and retrieval record | Cited in |
| --- | --- | --- |
| pip project: [Build System Interface](https://pip.pypa.io/en/stable/reference/build-system/) | Moving stable; current documentation is not a patch-specific manual for the tested pip 26.2.2. Retrieved. | [31](chapters/31.md#distinguish-three-kinds-of-isolation) |
| PyPA: [Core metadata specifications](https://packaging.python.org/en/latest/specifications/core-metadata/) | Living maintainer documentation / guidance. Retrieved. | [43](chapters/43.md#primary-sources) |
| PyPA: [Entry points specification](https://packaging.python.org/en/latest/specifications/entry-points/) | Living maintainer documentation / guidance. Retrieved. | [37](chapters/37.md#give-the-command-a-predictable-protocol) |
| Python project: [importlib.metadata – Accessing package metadata](https://docs.python.org/3.12/library/importlib.metadata.html) | Python 3.12 maintained documentation branch. Retrieved. | [43](chapters/43.md#primary-sources), [Appendix](appendices.md#find-the-explanation-by-the-task) |
| PyPA: [Install packages in a virtual environment using pip and venv](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/) | Living maintainer documentation / guidance. Retrieved. | [02](chapters/02.md#activation-is-a-convenience) |
| pip project: [Installation Report](https://pip.pypa.io/en/stable/reference/installation-report/) | Moving stable; current documentation is not a patch-specific manual for the tested pip 26.2.2. Retrieved. | [31](chapters/31.md#worked-example-1-follow-the-indirect-package-into-installed-code) |
| OpenSSF / OSV: [Open Source Vulnerability format - Open Source Vulnerability schema](https://ossf.github.io/osv-schema/) | Living maintainer documentation / guidance. Retrieved. | [31](chapters/31.md#worked-example-2-compare-the-advisory-range-with-the-selected-version) |
| OWASP: [OWASP Software Component Verification Standard](https://owasp.org/www-project-software-component-verification-standard/) | Living maintainer documentation / guidance. Retrieved. | [43](chapters/43.md#primary-sources) |
| pip project: [pip inspect](https://pip.pypa.io/en/stable/cli/pip_inspect/) | Moving stable; current documentation is not a patch-specific manual for the tested pip 26.2.2. Retrieved. | [43](chapters/43.md#primary-sources) |
| pip project: [pip inspect JSON output specification](https://pip.pypa.io/en/stable/reference/inspect-report/) | Moving stable; current documentation is not a patch-specific manual for the tested pip 26.2.2. Retrieved. | [31](chapters/31.md#worked-example-1-follow-the-indirect-package-into-installed-code) |
| pip project: [pip install](https://pip.pypa.io/en/stable/cli/pip_install/) | Moving stable; current documentation is not a patch-specific manual for the tested pip 26.2.2. Retrieved. | [31](chapters/31.md#make-source-selection-explicit) |
| PyPA: [pyproject.toml specification](https://packaging.python.org/en/latest/specifications/pyproject-toml/) | Living maintainer documentation / guidance. Retrieved. | [31](chapters/31.md#know-which-artifact-you-are-reading) |
| pip project: [Secure installs](https://pip.pypa.io/en/stable/topics/secure-installs/) | Moving stable; current documentation is not a patch-specific manual for the tested pip 26.2.2. Retrieved. | [31](chapters/31.md#read-a-hashed-lock-as-a-reviewed-selection) |
| SLSA project: [SLSA • Build: Verifying artifacts](https://slsa.dev/spec/v1.2/verifying-artifacts) | SLSA v1.2 specification. Retrieved. | [32](chapters/32.md#verify-authority-and-bytes-before-copying) |
| SLSA project: [SLSA • Provenance](https://slsa.dev/spec/v1.2/provenance) | SLSA v1.2 specification. Retrieved. | [31](chapters/31.md#keep-identity-integrity-and-provenance-distinct), [43](chapters/43.md#primary-sources) |
| PyPA: [Source distribution format](https://packaging.python.org/en/latest/specifications/source-distribution-format/) | Living maintainer documentation / guidance. Retrieved. | [31](chapters/31.md#know-which-artifact-you-are-reading) |
| OWASP CycloneDX: [Specification Overview — CycloneDX](https://cyclonedx.org/specification/overview/) | Living maintainer documentation / guidance. Retrieved. | [31](chapters/31.md#3-sbom-advisory-matching-and-software-composition-analysis) |
| PyPA packaging: [Specifiers - Packaging](https://packaging.pypa.io/en/stable/specifiers.html) | Living maintainer documentation / guidance. Retrieved. | [31](chapters/31.md#worked-example-2-compare-the-advisory-range-with-the-selected-version) |
| pip project: [User Guide](https://pip.pypa.io/en/stable/user_guide/) | Moving stable; current documentation is not a patch-specific manual for the tested pip 26.2.2. Retrieved. | [31](chapters/31.md#2-pins-constraints-hashes-index-selection-and-isolated-builds) |
| PyPA: [Version specifiers](https://packaging.python.org/en/latest/specifications/version-specifiers/) | Living maintainer documentation / guidance. Retrieved. | [31](chapters/31.md#worked-example-2-compare-the-advisory-range-with-the-selected-version), [43](chapters/43.md#primary-sources) |
| PyPA: [Wheel distribution format](https://packaging.python.org/en/latest/specifications/binary-distribution-format/) | Living maintainer documentation / guidance. Retrieved. | [31](chapters/31.md#know-which-artifact-you-are-reading), [37](chapters/37.md#build-and-inspect-the-wheel) |
| PyPA: [Writing your pyproject.toml](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/) | Living maintainer documentation / guidance. Retrieved. | [37](chapters/37.md#give-the-command-a-predictable-protocol) |

### CI and release workflows

GitHub platform guidance. The book does not claim a hosted workflow ran merely because a workflow fragment is shown.

| Primary source | Edition and retrieval record | Cited in |
| --- | --- | --- |
| GitHub: [Evaluate expressions in workflows and actions](https://docs.github.com/en/actions/reference/workflows-and-actions/expressions) | Living maintainer documentation / guidance. Retrieved. | [32](chapters/32.md#schedule-the-gate-even-when-an-upstream-job-fails) |
| GitHub: [Secure use reference](https://docs.github.com/en/actions/reference/security/secure-use) | Living maintainer documentation / guidance. Retrieved. | [32](chapters/32.md#2-jobs-artifacts-minimum-token-permissions-and-untrusted-changes) |
| GitHub: [Use GITHUB_TOKEN for authentication in workflows](https://docs.github.com/en/actions/tutorials/authenticate-with-github_token) | Living maintainer documentation / guidance. Retrieved. | [32](chapters/32.md#2-jobs-artifacts-minimum-token-permissions-and-untrusted-changes) |
| GitHub: [Using artifact attestations to establish provenance for builds](https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations) | Living maintainer documentation / guidance. Retrieved. | [32](chapters/32.md#2-jobs-artifacts-minimum-token-permissions-and-untrusted-changes) |
| GitHub: [Using conditions to control job execution](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/control-jobs-with-conditions) | Living maintainer documentation / guidance. Retrieved. | [32](chapters/32.md#schedule-the-gate-even-when-an-upstream-job-fails) |
| GitHub: [Workflow artifacts](https://docs.github.com/en/actions/concepts/workflows-and-actions/workflow-artifacts) | Living maintainer documentation / guidance. Retrieved. | [32](chapters/32.md#2-jobs-artifacts-minimum-token-permissions-and-untrusted-changes) |
| GitHub: [Workflow syntax for GitHub Actions](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax) | Living maintainer documentation / guidance. Retrieved. | [32](chapters/32.md#schedule-the-gate-even-when-an-upstream-job-fails) |

### Logs, metrics and reliability

Event representation, observability signals and operational decision methods.

| Primary source | Edition and retrieval record | Cited in |
| --- | --- | --- |
| Python project: [datetime — Basic date and time types](https://docs.python.org/3.12/library/datetime.html) | Python 3.12 maintained documentation branch. Retrieved. | [18](chapters/18.md#primary-sources), [21](chapters/21.md#primary-sources), [34](chapters/34.md#primary-sources), [36](chapters/36.md#primary-sources), [Appendix](appendices.md#find-the-explanation-by-the-task) |
| Google SRE authors: [Google SRE - Prometheus Alerting: Turn SLOs into Alerts](https://sre.google/workbook/alerting-on-slos/) | Living maintainer documentation / guidance. Retrieved. | [34](chapters/34.md#a-deliberately-small-alert-policy) |
| Prometheus project: [Histograms and summaries — Prometheus](https://prometheus.io/docs/practices/histograms/) | Living maintainer documentation / guidance. Retrieved. | [34](chapters/34.md#percentiles-describe-a-distribution) |
| Prometheus project: [Instrumentation — Prometheus](https://prometheus.io/docs/practices/instrumentation/) | Living maintainer documentation / guidance. Retrieved. | [34](chapters/34.md#define-the-counted-population-first) |
| OWASP: [Logging](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html) | Living maintainer documentation / guidance. Retrieved. | [33](chapters/33.md#1-structured-events-severity-utc-timestamps-and-correlation-ids), [44](chapters/44.md#primary-sources) |
| Python project: [logging — Logging facility for Python](https://docs.python.org/3.12/library/logging.html) | Python 3.12 maintained documentation branch. Retrieved. | [33](chapters/33.md#prevent-one-input-from-becoming-two-apparent-records) |
| Python project: [logging.handlers — Logging handlers](https://docs.python.org/3.12/library/logging.handlers.html) | Python 3.12 maintained documentation branch. Retrieved. | [33](chapters/33.md#prevent-one-input-from-becoming-two-apparent-records) |
| OpenTelemetry: [Logs Data Model — OpenTelemetry](https://opentelemetry.io/docs/specs/otel/logs/data-model/) | Living maintainer documentation / guidance. Retrieved. | [33](chapters/33.md#use-utc-without-pretending-clocks-establish-causality) |
| Python project: [statistics — Mathematical statistics functions](https://docs.python.org/3.12/library/statistics.html) | Python 3.12 maintained documentation branch. Retrieved. | [34](chapters/34.md#primary-sources) |
| OpenTelemetry: [Traces — OpenTelemetry](https://opentelemetry.io/docs/concepts/signals/traces/) | Living maintainer documentation / guidance. Retrieved. | [34](chapters/34.md#three-identifiers-with-three-jobs) |

### Cloud, containers and deployment

Provider and runtime documentation. Local policy fixtures and Compose rendering do not establish deployed enforcement.

| Primary source | Edition and retrieval record | Cited in |
| --- | --- | --- |
| AWS: [Amazon SQS API permissions: Actions and resource reference - Amazon Simple Queue Service](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-api-permissions-reference.html) | Living maintainer documentation / guidance. Retrieved. | [39](chapters/39.md#trace-the-job-without-trusting-its-payload-as-authority) |
| AWS: [Amazon SQS visibility timeout - Amazon Simple Queue Service](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-visibility-timeout.html) | Living maintainer documentation / guidance. Retrieved. | [39](chapters/39.md#keep-the-clocks-separate) |
| AWS: [Blocking public access to your Amazon S3 storage - Amazon Simple Storage Service](https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-control-block-public-access.html) | Living maintainer documentation / guidance. Retrieved. | [39](chapters/39.md#a-private-object-still-needs-a-release-policy) |
| Docker: [Building best practices](https://docs.docker.com/build/building/best-practices/) | Living maintainer documentation / guidance. Retrieved. | [35](chapters/35.md#separate-two-kinds-of-authority) |
| Docker: [Define services in Docker Compose](https://docs.docker.com/reference/compose-file/services/) | Living maintainer documentation / guidance. Retrieved. | [35](chapters/35.md#primary-sources) |
| AWS: [Download and upload objects with presigned URLs - Amazon Simple Storage Service](https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-presigned-url.html) | Living maintainer documentation / guidance. Retrieved. | [39](chapters/39.md#a-private-object-still-needs-a-release-policy) |
| Docker: [Frequently asked questions about Docker Compose](https://docs.docker.com/compose/support-and-feedback/faq/) | Living maintainer documentation / guidance. Retrieved. | [35](chapters/35.md#the-reviewed-container-manifest) |
| AWS: [GetObject - Amazon S3](https://docs.aws.amazon.com/AmazonS3/latest/API/API_GetObject.html) | Living maintainer documentation / guidance. Retrieved. | [39](chapters/39.md#a-private-object-still-needs-a-release-policy) |
| NGINX project: [How nginx processes a request](https://nginx.org/en/docs/http/request_processing.html) | Living maintainer documentation / guidance. Retrieved. | [35](chapters/35.md#worked-example-2-who-supplied-https) |
| NGINX project: [Module ngx_http_proxy_module](https://nginx.org/en/docs/http/ngx_http_proxy_module.html) | Living maintainer documentation / guidance. Retrieved. | [35](chapters/35.md#primary-sources) |
| Linux man-pages project: [network_namespaces(7) - Linux manual page](https://man7.org/linux/man-pages/man7/network_namespaces.7.html) | Living maintainer documentation / guidance. Retrieved. | [35](chapters/35.md#primary-sources) |
| Docker: [None network driver](https://docs.docker.com/engine/network/drivers/none/) | Living maintainer documentation / guidance. Retrieved. | [35](chapters/35.md#block-an-unnecessary-connection-with-evidence) |
| AWS: [Policy evaluation logic - AWS Identity and Access Management](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html) | Living maintainer documentation / guidance. Retrieved. | [39](chapters/39.md#a-synthetic-policy-you-can-inspect) |
| AWS: [Presigned URLs - Boto3 1.43.122 documentation](https://docs.aws.amazon.com/boto3/latest/guide/s3-presigned-urls.html) | Living maintainer documentation / guidance. Retrieved. | [39](chapters/39.md#a-private-object-still-needs-a-release-policy) |
| Docker: [Secrets](https://docs.docker.com/reference/compose-file/secrets/) | Living maintainer documentation / guidance. Retrieved. | [35](chapters/35.md#inject-secrets-at-runtime) |
| OWASP: [Secrets Management](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html) | Living maintainer documentation / guidance. Retrieved. | [13](chapters/13.md#primary-sources), [36](chapters/36.md#make-containment-observable) |
| AWS: [Security best practices in IAM - AWS Identity and Access Management](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html) | Living maintainer documentation / guidance. Retrieved. | [39](chapters/39.md#a-service-has-an-identity-of-its-own) |
| Gunicorn project: [Settings - Gunicorn](https://gunicorn.org/reference/settings/) | Living maintainer documentation / guidance. Retrieved. | [35](chapters/35.md#worked-example-2-who-supplied-https) |
| AWS: [Shared Responsibility Model - Amazon Web Services (AWS)](https://aws.amazon.com/compliance/shared-responsibility-model/) | Living maintainer documentation / guidance. Retrieved. | [39](chapters/39.md#managed-infrastructure-does-not-choose-the-tenant) |
| Linux man-pages project: [unix(7) - Linux manual page](https://man7.org/linux/man-pages/man7/unix.7.html) | Living maintainer documentation / guidance. Retrieved. | [35](chapters/35.md#give-each-writable-path-a-reason) |

### Incidents, development practices and finding classification

Incident response, improvement models and precise weakness/vulnerability/severity vocabulary.

| Primary source | Edition and retrieval record | Cited in |
| --- | --- | --- |
| CVE Program: [CVE List, official CVE JSON 5 repository](https://github.com/CVEProject/cvelistV5) | Living maintainer documentation / guidance. Retrieved. | [38](chapters/38.md#3-cwe-weakness-classes-cve-identifiers-cvss-severity-and-contextual-impact) |
| CVE Program: [CVE Numbering Authority Operational Rules][cve-cna] | Living rules page; direct HTML content only partially retrieved. Partial HTML; see access note. | [Appendix](appendices.md#read-cwe-cve-and-cvss-precisely) |
| FIRST: [CVSS v4.0 Specification Document](https://www.first.org/cvss/v4.0/specification-document) | CVSS v4.0 specification. Retrieved. | [38](chapters/38.md#keep-a-real-scores-provenance), [Appendix](appendices.md#read-cwe-cve-and-cvss-precisely) |
| CWE Program: [CWE - About CWE](https://cwe.mitre.org/about/index.html) | Living definition; keep the specific CWE identifier. Retrieved. | [38](chapters/38.md#3-cwe-weakness-classes-cve-identifiers-cvss-severity-and-contextual-impact) |
| CWE Program: [CWE - CWE-22: Improper Limitation of a Pathname to a Restricted Directory (5.0)](https://cwe.mitre.org/data/definitions/22.html) | Living definition; keep the specific CWE identifier. Retrieved. | [38](chapters/38.md#3-cwe-weakness-classes-cve-identifiers-cvss-severity-and-contextual-impact) |
| CWE Program: [CWE - CWE-489: Active Debug Code (5.0)](https://cwe.mitre.org/data/definitions/489.html) | Living definition; keep the specific CWE identifier. Retrieved. | [38](chapters/38.md#3-cwe-weakness-classes-cve-identifiers-cvss-severity-and-contextual-impact) |
| CWE Program: [CWE - CWE-862: Missing Authorization (5.0)](https://cwe.mitre.org/data/definitions/862.html) | Living definition; keep the specific CWE identifier. Retrieved. | [29](chapters/29.md#4-confidence-false-positives-fixes-and-regression-coverage), [Appendix](appendices.md#read-cwe-cve-and-cvss-precisely) |
| CWE Program: [CWE - CWE-863: Incorrect Authorization (5.0)](https://cwe.mitre.org/data/definitions/863.html) | Living definition; keep the specific CWE identifier. Retrieved. | [Appendix](appendices.md#read-cwe-cve-and-cvss-precisely) |
| CWE Program: [CWE - CWE-89: Improper Neutralization of Special Elements used in an SQL Command (5.0)](https://cwe.mitre.org/data/definitions/89.html) | Living definition; keep the specific CWE identifier. Retrieved. | [29](chapters/29.md#primary-sources), [Appendix](appendices.md#read-cwe-cve-and-cvss-precisely) |
| CWE Program: [CWE - CWE-918: Server-Side Request Forgery (5.0)](https://cwe.mitre.org/data/definitions/918.html) | Living definition; keep the specific CWE identifier. Retrieved. | [Appendix](appendices.md#read-cwe-cve-and-cvss-precisely) |
| OWASP SAMM: [Defect Management](https://owaspsamm.org/model/implementation/defect-management/) | Version 2 model / living practice page. Retrieved. | [40](chapters/40.md#use-frameworks-to-organize-improvement), [Appendix](appendices.md#development-practices-and-improvement-evidence) |
| OWASP SAMM: [Incident Management](https://owaspsamm.org/model/operations/incident-management/) | Version 2 model / living practice page. Retrieved. | [Appendix](appendices.md#development-practices-and-improvement-evidence) |
| OWASP SAMM: [Requirements-driven Testing](https://owaspsamm.org/model/verification/requirements-driven-testing/) | Version 2 model / living practice page. Retrieved. | [40](chapters/40.md#use-frameworks-to-organize-improvement), [Appendix](appendices.md#development-practices-and-improvement-evidence) |
| NIST: [SSDF 1.1 publication record](https://csrc.nist.gov/pubs/sp/800/218/final); [SP 800-218 PDF](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-218.pdf) | SSDF 1.1 / SP 800-218, final (2022). Retrieved. | [40](chapters/40.md#use-frameworks-to-organize-improvement), [43](chapters/43.md#primary-sources), [Appendix](appendices.md#use-the-right-kind-of-reference) |
| NIST: [SP 800-61 Rev. 3, Incident Response Recommendations and Considerations for Cybersecurity Risk Management: A CSF 2.0 Community Profile — CSRC](https://csrc.nist.gov/pubs/sp/800/61/r3/final) | SP 800-61 Rev. 3, final (2025). Retrieved. | [36](chapters/36.md#assign-authority-before-making-changes), [44](chapters/44.md#primary-sources) |
| OASIS: [Static Analysis Results Interchange Format (SARIF) Version 2.1.0](https://docs.oasis-open.org/sarif/sarif/v2.1.0/os/sarif-v2.1.0-os.html) | SARIF 2.1.0, OASIS Standard. Retrieved. | [38](chapters/38.md#the-second-report-and-the-supported-sarif-subset) |
| OWASP SAMM: [Strategy and Metrics](https://owaspsamm.org/model/governance/strategy-and-metrics/) | Version 2 model / living practice page. Retrieved. | [40](chapters/40.md#use-frameworks-to-organize-improvement), [Appendix](appendices.md#development-practices-and-improvement-evidence) |
| CERT/CC: [The CERT Guide to Coordinated Vulnerability Disclosure - CERT® Guide to Coordinated Vulnerability Disclosure](https://certcc.github.io/CERT-Guide-to-CVD/) | Living maintainer documentation / guidance. Retrieved. | [36](chapters/36.md#coordinate-facts-and-audiences) |
| OWASP SAMM: [The Model](https://owaspsamm.org/model/) | Version 2 model / living practice page. Retrieved. | [40](chapters/40.md#use-frameworks-to-organize-improvement), [Appendix](appendices.md#use-the-right-kind-of-reference) |

## Access limits and maintenance notes

The original [CVE CNA Rules citation][cve-cna] returned a JavaScript-only notice during direct retrieval. Its complete HTML rule text was therefore **not directly verified**. An official search result and the [CVE Program's maintained rule source](https://github.com/CVEProject/cve-documents/blob/master/CNA_Rules.md) identify and expose the rules. That repository is an **access/verification alternative added for this check**, not an additional work claimed to have been cited by an earlier chapter. No CNA clause number or operational-conformance claim is inferred from the inaccessible HTML.

All other cited document addresses returned readable publisher content. This checks availability and identity on the recorded date, not permanent availability, archived content hashes, every external fragment or every linked technical claim. In particular, `latest`, `stable`, provider documentation and draft URLs remain mutable. The CSP Level 3 page is a **Working Draft**; the HTTPWG cookie source is an **Internet-Draft**, while WebAuthn Level 3 is labeled a **Recommendation**. Do not silently relabel them all as final standards.

The tested edition ran the suites and demonstrations named in the current reports, including the Django, PyJWT and Hypothesis integrations. Those local results do not establish hosted providers, browser-engine enforcement, Windows execution or production approval. Unexecuted scanner/deployment illustrations remain explicitly outside the tested tool inventory.

For an update, retain the source's owner and edition, its chapter citation, actual environment identity, command/report and unresolved limit. Update a moving documentation reference only after checking the affected examples. Replacing an expected version string or an unavailable-source label does not create execution evidence.

[cve-cna]: https://www.cve.org/ResourcesSupport/AllResources/CNARules/

---

[Repository](../README.md) · [Contents](README.md#contents) · [Appendices](appendices.md) · [Indexes](indexes.md) · [References](references.md)
