# Chapter 20 contract laboratory

[← Chapter 20](../../manuscript/chapters/20.md) · [All examples](../README.md) · [Tested versions](../../tested-versions.md)

This local, standard-library model specifies proposed API behavior. It does not
add HTTP routes to chapter 19 and does not authenticate fixture users.
It requires Python 3.12 or later for explicit SQLite `autocommit` configuration;
the book targets CPython 3.12.14.

From this directory, use your learning environment's Python:

```shell
python contract_demo.py
python -m unittest -v test_contract
```

Both commands create fresh temporary databases. They retain chapter 19's seeded
workspace and note identifiers and add contract-only ownership, state, version,
membership and export-receipt records. No existing database is modified.

The chapter contains the full source, contract tables, expected demo output,
worked answers and actual verification record. `snapshot()` is a privileged local
evidence helper and must never be exposed as a public response.
