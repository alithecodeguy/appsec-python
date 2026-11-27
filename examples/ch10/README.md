# Chapter 10 models and type checking

[← Chapter 10](../../manuscript/chapters/10.md) · [All examples](../README.md) · [Tested versions](../../tested-versions.md)

Use Python 3.12.14 and mypy 2.4.1 from the root tested requirements. Run from this directory:

```shell
python -m mypy --strict checked_types.py
python -m mypy --strict bad_types.py
python checked_types.py
```

The first command passes. The second intentionally exits 1 with two errors: an incompatible owner argument and an optional integer return. The book explains the correction. These are learning fixtures, not a claim that annotations validate external JSON or authorize a workspace.
