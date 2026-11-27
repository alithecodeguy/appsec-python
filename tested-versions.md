# Tested versions and reproduction

The book's language baseline is **CPython 3.12.14**. The local web examples use **Django 6.1.3** on that interpreter. These are the versions used for the recorded checks, rather than a separate aspirational target.

Install the exact package set from [requirements-tested.txt](requirements-tested.txt). It records the observed Python distributions, including transitive dependencies and build tools. It is a reproduction input for this learning environment, not an authenticated lock/SBOM or a claim that a deployment has been approved.

| Component | Tested version | Recorded boundary |
| --- | --- | --- |
| CPython | 3.12.14 | Local examples and test processes on macOS arm64 |
| SQLite | 3.53.1 | Engine loaded by this interpreter; check your own build |
| Django | 6.1.3 | Service checks, migrations/ORM, loopback health/private-route requests, password/session APIs and test-client integration |
| PyJWT | 2.15.1 | Local signatures plus issuer/audience/expiry policy under controlled clocks |
| Hypothesis | 6.170.17 | Generated HTTP isolation property and independently rechecked shrinking example |
| cryptography | 50.0.2 | Export AEAD and local signing/token fixtures |
| pytest | 9.2.0 | Chapter 12's 30 tests |
| mypy | 2.4.1 | Accepted narrowed result; intentional two-error rejection |
| packaging | 26.4 | Version/specifier examples and selected installed environment |
| pip / setuptools / wheel | 26.2.2 / 84.2.1 / 0.48.0 | Selected builder/install toolchain |
| Python OpenSSL | 3.5.8 | Interpreter TLS backend; no deployed TLS verification claim |
| cryptography OpenSSL | 4.0.3 | Separate cryptography backend; do not substitute Python's backend version |
| Git | 2.54.0 (Apple Git-157) | Source-candidate identity and local review tooling |
| Docker CLI / Compose | 29.8.1 / v5.5.1 | Chapter 35's offline manifest rendering/checks; no daemon/image/deployment claim |
| Mermaid | 12.3.0 | Chapter 17's syntax parsing; browser layout remains a separate check |

The current [verification report](examples/verification/current.json) retains 28 actual command results, package/native-library versions and tested-source hashes. It records **159 passing test methods**, the successful password/session/shrinking/loopback demonstrations, and the intended mypy refusal. A mypy exit status of 1 is expected only for the supplied deliberately incorrect file; the report checks that it contains the two intended errors.

From a shell with the selected interpreter available, create a fresh environment:

```shell
python3.12 --version
python3.12 -m venv .venv
./.venv/bin/python -m pip install -r requirements-tested.txt
./.venv/bin/python examples/verify_book.py
```

The first command must report `Python 3.12.14` for exact reproduction. Use the full path from chapter 02 if `python3.12` selects another interpreter. On PowerShell, select the base interpreter as explained in chapter 02, run `& $CasebookPython -m venv .venv`, then use `.\.venv\Scripts\python.exe` for the remaining Python commands. The Windows installation/shell procedures were not executed in the macOS run.

Each Django settings laboratory runs in its own process. Do not combine every Django test module into one process with incompatible global settings. The verifier uses fresh synthetic databases and an OS-selected loopback port; it does not operate a production database or send private data to an external service.

The separately built [chapter 43 candidate](examples/ch43/evidence/candidate.json) has **20 core and three HTTP passes**, with zero skips in its [candidate report](examples/ch43/evidence/candidate-run.json). Its executable-source archive is bound to an actual Git commit and checked against the working examples. The book's current narrative and local report are outside that executable-source allowlist.

Run the candidate and recovery checks from the repository root:

```shell
./.venv/bin/python -m examples.ch43.build_candidate --out /tmp/casebook-candidate-check
./.venv/bin/python -m examples.ch43.check_evidence
./.venv/bin/python -m unittest -v examples.ch44.test_recovery
```

The candidate collector replaces its three named ZIP/manifest/run files in the selected directory. The scratch output above leaves the book's reviewed evidence ledger intact; `check_evidence` checks that reviewed evidence. Replacing the reviewed candidate files requires a corresponding review and update of the ledger's subject/evidence hashes. A freshly collected report is not an authenticated approval. The release decision remains **HOLD** for real configuration/identity provisioning, protected persistent keys, workload/provider authority, applicable dependency/advisory evidence, scheduling, all managed copies and recovery/rollback readiness.

Browser-engine cookie/CORS/CSP behavior, deployed proxy/TLS, live identity-provider exchange, real scanner results, cloud enforcement and Windows execution remain distinct checks. An unexecuted tool illustration has no invented tested version. Consult the relevant chapter's verification scope and [references](manuscript/references.md) before extending a local result.
