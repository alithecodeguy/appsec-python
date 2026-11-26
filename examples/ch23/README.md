# Chapter 23: authorization laboratory

From this directory, use your learning environment's Python (3.12 or later):

```shell
python authorization_demo.py
python -m unittest -v test_authorization
```

The edition targets CPython 3.15.2. This standard-library model uses fresh
SQLite databases and trusted fixture identities. It preserves the Alpha/Beta
records from chapters 15 and 19–20 without modifying those files or schemas.
`list_view` and `detail_view` model contract responses; they are not HTTP routes.

Exports are bounded, in-memory artifacts for permission tests. They are neither
chapter 20's queued acceptance API nor the later durable worker. Authentication,
Django integration, real HTTP caches, durable artifacts and concurrent release
ordering require separate integration evidence. The chapter includes full source,
a permission matrix, exercises, answers and the actual verification record.
