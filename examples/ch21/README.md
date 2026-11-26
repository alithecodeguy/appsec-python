# Chapter 21: accounts and recovery

The recovery state laboratory requires Python 3.12 or later and uses only the
standard library. From this directory, use your learning environment's Python:

```shell
python recovery_demo.py
python -m unittest -v test_recovery
```

It checks synthetic state, expiry, single use and a revocation epoch. Opaque
password sentinels are not usable hashes. No authentication or real browser
session revocation is implemented by this model. The private outbox is a local
mailbox fixture, never a public token response.

The separate Django password example requires the pinned framework:

```shell
python -m pip install -r requirements.txt
python django_passwords.py
```

It uses an in-memory database and public fictional passwords. It adds no routes
to chapter 19. The edition targets CPython 3.15.2 and Django 6.1.3. Read the
chapter's verification record before interpreting expected Django output as a
recorded result.
