**Handover: `HAND44-01`, for a second engineer.**

**Starting point.** Production remains HOLD for `CB-EXPORT-RC43-01`. Use the chapter 43 commit/digest and evidence index. The chapter 44 incident is a controlled local rehearsal on matching candidate Python bytes; the implementation and release decision were not edited. Application keys, test databases and the intentionally unsafe backup are disposable.

**Prerequisites.** Run from the repository root in a Python 3.12+ learning environment with `cryptography==50.0.2`. Preserve chapter 23, 27, 28, 42 and 43 files and the Git repository containing the recorded candidate commit. A copied source folder without that commit object cannot satisfy the candidate check. The local Python/Django checks are recorded in the current verification report; deployment integration still needs its own evidence. Do not pass a production database path to these helpers; the CLI creates its own temporary databases and accepts only an output path for payload-free evidence.

**Repeat the checks.** Use a new output directory:

```shell
python -m examples.ch43.check_evidence
python -m examples.ch44.rehearsal --out /tmp/casebook-ch44-handover
python -m examples.ch44.timeline /tmp/casebook-ch44-handover/audit-input.jsonl
python -m unittest -v examples.ch44.test_recovery
```

If the output directory exists, choose a new path. If candidate/hash checks fail, stop and determine which subject changed; do not rewrite evidence hashes to make it pass. If the dependency is absent, install from your approved learning source before repeating. No network or provider action belongs to this rehearsal.

**Expected observations.** The held decision stays HOLD. At detection, overdue is true while the stored flag is zero. The negative backup contains two export rows. Quarantine starts with two payload rows and two nonce entries; reconciliation produces zero payload rows and three nonce entries. Mina's recovered request is 404; Ravi's old export is 410; Ravi's fresh Beta export is 200. Duplicate work is unchanged. Final live and restored payload-row counts are zero; the unsafe backup is absent. All nine recovery methods should pass.

**Evidence to read.** `incident-evidence.json` contains scenario facts, safe state summaries and probes; `audit-input.jsonl` deliberately interleaves application and harness evidence out of time order. The timeline tool orders their UTC display. `verification.json` records the actual method results/runtime and source hashes. These are unsigned synthetic local records, not production forensic custody or approval.

**Stop conditions.** Do not resume even the local positive-path rehearsal until restored temporary exports are removed and current authority is reconciled. Investigate changed expiry/closure/deletion times, missing nonce history, reused job identities, a cross-workspace response, unexpected payload copies or a failed required event. Keep deployment paused/held until its actual incident/release authority has adequate evidence. A successful source-hash check alone does not establish that authority.

**Ownership and closure criteria.** Names below are proposed fictional roles, not messages or accepted tickets.

| Open item | Next responsible role | Required closure evidence |
| --- | --- | --- |
| Scheduled deletion and independent overdue detection | Owen, platform | Actual dispatcher/monitor coverage and fixed-deadline failure/escalation test |
| Backup/version/replica exclusion | Owen, storage; Dana, recovery | Managed-copy inventory and restore drill proving temporary outputs are not revived |
| Trusted current authority during restore | Dana with Sam | Authenticated current membership/terminal source; reconciliation under quarantine and negative reads |
| Persistent scoped keys and nonce/history recovery | Owen | Restart/restore decryption and denied-scope tests with protected key custody |
| Deployed identity/TLS/proxy and private release paths | Sam | Actual hosting/configuration evidence, with deployed revoked/expired and alternate-path denial |
| Final dependency/configuration/build review | Owen with Tess | Actual final-subject inventory, advisory/configuration evidence and applicable dispositions |
| Five-minute removal proposal | Nora, data policy; Sam/Owen implement | Reviewed policy/version transition and new boundary/copy/restore tests before adoption |
| Incident/release reassessment | Tess with the actual authorized release roles | Current bound evidence, remaining risk and an explicit decision; production HOLD is not silently lifted |

**Record lifecycle.** Treat incident metadata as restricted evidence with an approved incident purpose/retention, separate from application receipts' seven days. This fixture does not choose a real incident-record retention period. Do not preserve payload backups or key dumps as a convenient incident attachment. Do not call row removal physical-media erasure. Attach the actual subject, method, result, time and next owner when handing this record onward.
