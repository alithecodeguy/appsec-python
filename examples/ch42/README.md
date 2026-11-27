# Chapter 42 private-export capstone

Run from the repository root with Python 3.12 or later. Preserve chapters 23,
27 and 28. No earlier file or database needs modification.

```shell
python -m pip install -r examples/ch42/requirements.txt
python -m examples.ch42.demo --stage admission
python -m examples.ch42.demo --stage worker
python -m examples.ch42.demo --stage lifecycle
python -m unittest -v examples.ch42.test_capstone
```

Each demo stage creates a disposable SQLite database, independent dummy AES keys
for Alpha/Beta, and a controlled clock. No keys or private payload bytes print.
Core operations run in short SQLite transactions. A stop request rolls preparation
back and leaves durable intent queued. No background daemon or live broker is
installed: tests/demos explicitly deliver stored job IDs to worker threads.

The optional Django session/CSRF adapter is a separate integration test seam:

```shell
python -m pip install -r examples/ch42/requirements-web.txt
python -m unittest -v examples.ch42.test_web
```

Run that suite in its own interpreter because it configures Django settings.
It uses force_login to create a framework test session, not an X-User-ID header.
It is not a standalone deployed login server. Dummy keys are process-local and
cannot support persistent service restarts. The adapter must be integrated with
reviewed authentication, persistent key custody and actual hosting controls.

Recorded locally: 20 core methods and three Django HTTP methods passed on Python
3.12.14 and Django 6.1.3, with zero skips. Deployed HTTP/TLS, provider workload controls,
backup exclusion/restore and removal of object versions/replicas were not tested.
See verification.json and manuscript/chapters/42.md for evidence and limits.
The local SQL deletion result is not forensic erasure or a provider deletion claim.
