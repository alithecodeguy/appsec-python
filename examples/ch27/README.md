# Chapter 27 cryptographic laboratory

Run from the repository root using Python 3.12 or later:

```shell
python -m pip install -r examples/ch27/requirements.txt
python -m examples.ch27.random_demo
python -m examples.ch27.crypto_demo
python -m unittest -v examples.ch27.test_crypto
```

Requires unchanged chapter 23 and 26 modules and chapter 26's stored webhook
fixture. Uses fresh temporary SQLite databases, public dummy HMAC keys and
fresh disposable AES-GCM keys. No production keys are accessed or changed.

The local nonce ledger, associated-data wrapper and migration demonstrate a
bounded record protocol, not a general encrypted file format or KMS. Authorization
remains mandatory. The chapter records runtime versions and verification limits.
