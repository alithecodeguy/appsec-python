# Chapter 19: Casebook service

From this directory, using the book's CPython 3.15.2 baseline:

```shell
python3.15 -m venv .venv
./.venv/bin/python -m pip install -r requirements.txt
./.venv/bin/python manage.py check
./.venv/bin/python manage.py migrate
./.venv/bin/python manage.py loaddata demo
./.venv/bin/python manage.py test notes -v 2
./.venv/bin/python manage.py runserver 127.0.0.1:8000 --noreload
```

In a second terminal:

```shell
curl -i http://127.0.0.1:8000/health/
curl -i http://127.0.0.1:8000/notes/101/
```

Expect `200` with `application/json` and `{"status": "ok"}` for health;
expect `404` without private fields for the note. Only `/health/` is routed.
Health checks process liveness, not database readiness.

The seed has Alpha (`1`), Beta (`2`), Alpha note `101`, and Beta note `202`.
It is synthetic and separate from chapter 15's standalone SQLite database.
Reloading `demo` overwrites these four fixture records and does not remove
other records. Never use it against real data.

Run the ORM example once after seeding:

```shell
./.venv/bin/python manage.py shell < orm_demo.py
```

It creates multilingual note `103`. A second run fails validation because that
ID already exists. The chapter explains this boundary and a controlled cleanup.

On Windows use `py -3.15 -m venv .venv`, then replace `./.venv/bin/python`
with `.\.venv\Scripts\python.exe`. Pipe the demo with
`Get-Content -Encoding utf8 orm_demo.py | .\.venv\Scripts\python.exe manage.py shell`.

This is a local development exercise: no accounts, membership model, private
HTTP endpoint, admin, templates, worker or production configuration. The local
key is deliberately public. `DEBUG=False` gives generic missing-route responses.
The chapter includes every source file and the verification limitations.
