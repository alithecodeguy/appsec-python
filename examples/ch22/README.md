# Chapter 22: sessions and token verification

Use your learning environment's Python from this directory. The edition targets
CPython 3.12.14; the chapter records the actual available verification runtime.

```shell
python -m unittest -v test_claims
python -m pip install -r requirements.txt
python -m unittest -v test_jwt
python django_sessions.py
```

`test_claims` needs only the standard library. It checks dictionaries against a
local policy and does not authenticate a JWT. `test_jwt` requires PyJWT and
cryptography, signs local fixtures and verifies signatures plus claims with a
frozen test clock. The Django example uses real session APIs with an in-memory
database. Neither example adds routes to chapter 19 or contacts an identity
provider. The chapter records passing local token/session checks and separate provider/browser limits.
