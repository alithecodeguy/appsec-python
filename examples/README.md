# Runnable examples

[Repository](../README.md) · [Book contents](../manuscript/README.md#contents) · [Tested versions](../tested-versions.md)

The book combines listings you create yourself with selected runnable companions. A directory is included only for the chapters below. For other chapters, create the named files from the listings and use the stated starting state. Some examples intentionally show a defect before its correction; read the expected outcome before running a command.

## Choose a lab

| Chapter | Companion |
| --- | --- |
| [10. Types, classes and domain models](../manuscript/chapters/10.md) | [Files and run instructions](ch10/README.md) |
| [12. Repeatable tests and a reviewable change](../manuscript/chapters/12.md) | [Files and run instructions](ch12/README.md) |
| [19. Build the Casebook web service](../manuscript/chapters/19.md) | [Files and run instructions](ch19/README.md) |
| [20. API contracts and business rules](../manuscript/chapters/20.md) | [Files and run instructions](ch20/README.md) |
| [21. Accounts, passwords and recovery](../manuscript/chapters/21.md) | [Files and run instructions](ch21/README.md) |
| [22. Sessions, tokens and federated identity](../manuscript/chapters/22.md) | [Files and run instructions](ch22/README.md) |
| [23. Authorization and tenant isolation](../manuscript/chapters/23.md) | [Files and run instructions](ch23/README.md) |
| [24. Templates, cookies and the browser](../manuscript/chapters/24.md) | [Files and run instructions](ch24/README.md) |
| [25. Uploads, archives and serialization](../manuscript/chapters/25.md) | [Files and run instructions](ch25/README.md) |
| [26. Outbound requests and integrations](../manuscript/chapters/26.md) | [Files and run instructions](ch26/README.md) |
| [27. Cryptographic choices and key management](../manuscript/chapters/27.md) | [Files and run instructions](ch27/README.md) |
| [28. Concurrency, queues and resource limits](../manuscript/chapters/28.md) | [Files and run instructions](ch28/README.md) |
| [30. Verify controls in running code](../manuscript/chapters/30.md) | [Files and run instructions](ch30/README.md) |
| [42. Capstone II. Implement the controls](../manuscript/chapters/42.md) | [Files and run instructions](ch42/README.md) |
| [43. Capstone III. Review and release](../manuscript/chapters/43.md) | [Files and run instructions](ch43/README.md) |
| [44. Capstone IV. Operate, respond and hand over](../manuscript/chapters/44.md) | [Files and run instructions](ch44/README.md) |

The [appendix programs](appendices/) support [Appendix A and the worked lab notebook](../manuscript/appendices.md). The [verification report](verification/current.json) retains the recorded commands, runtime and source hashes.

## Set up and run

Start with [chapter 02](../manuscript/chapters/02.md) for installation. Use the exact edition environment and commands in [tested-versions.md](../tested-versions.md) when reproducing recorded results. Installing the full [tested package set](../requirements-tested.txt) is optional when a chapter uses only the standard library.

Read a companion's README before running it. Some commands run inside that chapter's directory; others run from the repository root. Run Django settings laboratories in separate Python processes. Use the virtual environment's explicit Python executable or activate it before using a command spelled `python`.

The early `casebook-learning` folder is your own exercise workspace. It is separate from this book checkout. Clone the book to use its companion files, and keep your exercise files in the workspace described by the chapter.

## Reproduce the recorded checks

From the repository root, after installing the tested environment:

```shell
./.venv/bin/python examples/verify_book.py --out /tmp/casebook-book-verification.json
```

The verifier requires the exact CPython patch and package versions. It runs separate processes, including the intentional mypy rejection, and writes the results to the selected file. The scratch output path above preserves the edition's retained report. See [tested-versions.md](../tested-versions.md) for candidate and recovery checks.

These labs use fictional data and disposable local state. They do not form one production application. The capstone's [release decision](ch43/release-decision.json) remains HOLD; browser-engine enforcement, real providers and deployment controls require separate evidence.
