# Chapter 26: integration contracts

[← Chapter 26](../../manuscript/chapters/26.md) · [All examples](../README.md) · [Tested versions](../../tested-versions.md)

From the repository root, with Python 3.12 or later:

```shell
python -m examples.ch26.integration_demo
python -m unittest -v examples.ch26.test_integrations
```

Requires unchanged `examples/ch23/authorization_service.py`. Uses fresh temporary
SQLite databases, a fake HTTP transport, stored raw JSON/header fixtures and
public dummy HMAC keys. The fixture timestamp is fixed, not the current clock.
No live network, real webhook provider or queue is contacted. The custom fixture
signature envelope is not a provider SDK/protocol. The edition targets Python
3.12.14; the chapter records actual checks and network-enforcement gaps.
