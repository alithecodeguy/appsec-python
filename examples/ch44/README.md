# Chapter 44 retention and recovery rehearsal

Run from the repository root with Python 3.12+ and chapter 42's core dependency:

```shell
python -m examples.ch43.check_evidence
python -m examples.ch44.rehearsal --out /tmp/casebook-ch44-new-evidence
python -m examples.ch44.timeline /tmp/casebook-ch44-new-evidence/audit-input.jsonl
python -m unittest -v examples.ch44.test_recovery
```

The output directory must not exist. All operational databases and dummy keys
are disposable. The full backup is an intentionally wrong negative fixture,
created only under TemporaryDirectory and removed before the rehearsal returns.
Reports contain synthetic metadata and counts, not ciphertext, key bytes or note
bodies. evidence/ retains the manuscript run and its deliberately shuffled log.

The scenario verifies the chapter 43 candidate identities and current workspace
Python hashes before calling domain operations. It does not edit the held source
or decision, deploy, send a notification, change real membership, or provide a
general-purpose recovery API. Quarantine reconciliation trusts only the fixture's
in-memory current facts, discards all restored temporary outputs, and preserves
current authorization/terminal metadata and the union of nonce history.

The existing encrypted keys remain in one process for this exercise. No provider
key recovery, production backup exclusion, filesystem forensic erasure, global
traffic pause, scheduled maintenance or HTTP integration is claimed. Production
remains HOLD. The five-minute removal proposal is arithmetic/test planning only;
the held candidate's 15-minute policy is unchanged.
