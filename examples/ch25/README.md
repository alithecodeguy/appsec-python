# Chapter 25 attachment laboratory

[← Chapter 25](../../manuscript/chapters/25.md) · [All examples](../README.md) · [Tested versions](../../tested-versions.md)

Run from the repository root with Python 3.12 or later:

```shell
python -m examples.ch25.attachment_demo
python -m unittest -v examples.ch25.test_attachments
```

Requires unchanged `examples/ch23/authorization_service.py`. Uses standard-library
SQLite and a fresh private temporary storage tree. The edition targets Python
3.12.14. Publication and retrieval use POSIX hard links, modes and O_NOFOLLOW;
Windows needs a separately implemented storage backend, not a removed link check.
The archive example reviews JSON manifests only and does not extract archives.
No Django route, virus scanner, crash recovery or production storage is supplied.
