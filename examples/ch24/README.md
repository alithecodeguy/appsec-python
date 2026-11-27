# Chapter 24 browser laboratory

Run from the repository root. Keep chapter 23's `authorization_service.py` at
`examples/ch23/authorization_service.py`; the browser lab imports it unchanged.
The edition targets CPython 3.12.14 and Django 6.1.3.

```shell
python -m pip install -r examples/ch24/requirements.txt
python -m unittest -v examples.ch24.test_browser
python -m examples.ch24.html_evidence
```

The nine Django tests use a fresh temporary database, real fixture sign-in and
`Client(enforce_csrf_checks=True)`. They are not browser-engine enforcement tests.
`html_evidence` parses hand-authored expected HTML and does not run Django.

For a disposable local HTTP browser demonstration on macOS/Linux:

```shell
CASEBOOK_LOCAL_HTTP=1 python -m examples.ch24.browser_lab init
CASEBOOK_LOCAL_HTTP=1 python -m examples.ch24.browser_lab runserver 127.0.0.1:8000 --noreload
```

On PowerShell, set `$env:CASEBOOK_LOCAL_HTTP="1"` before those module commands.
Visit `/accounts/login/` and use `mina`, `ravi` or `lee` with the public password
in `browser_lab.PASSWORD`. Alpha note is `/workspaces/1/notes/101/`; Beta note is
`/workspaces/2/notes/202/`. Initialization refuses an existing database.

The explicit local HTTP profile uses unprefixed cookies without Secure because
this is a loopback-only exercise with fictional credentials. The default/test
profile uses HTTPS requests and Secure cookies. Never deploy the HTTP fixture
profile or the public secret/password. The chapter records which checks ran.
