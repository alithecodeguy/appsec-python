"""Run the book's local checks in separate processes and retain actual results."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
from pathlib import Path
import platform
import re
import shutil
import sqlite3
import ssl
import subprocess
import sys
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[1]


def live19():
    """Use only a copied synthetic service and an OS-selected loopback port."""
    import contextlib
    import io
    import os
    from threading import Thread
    from urllib.error import HTTPError
    from urllib.request import urlopen
    from wsgiref.simple_server import WSGIRequestHandler, make_server

    with TemporaryDirectory(prefix="casebook-health-") as folder:
        service = Path(folder) / "service"
        shutil.copytree(ROOT / "examples/ch19", service,
                        ignore=shutil.ignore_patterns("__pycache__", "*.sqlite3", ".venv"))
        sys.path.insert(0, str(service))
        os.environ["DJANGO_SETTINGS_MODULE"] = "casebook.settings"
        import django
        django.setup()
        from django.core.management import call_command
        from django.core.wsgi import get_wsgi_application
        from django.db import connections
        from notes.models import Note, Workspace
        with contextlib.redirect_stdout(io.StringIO()):
            call_command("migrate", verbosity=0)
            call_command("loaddata", "demo", verbosity=0)
            exec(compile((service / "orm_demo.py").read_text(), "orm_demo.py", "exec"), {})
        assert set(Workspace.objects.values_list("name", flat=True)) == {"Alpha", "Beta"}
        assert set(Note.objects.values_list("id", flat=True)) == {101, 103, 202}

        class Quiet(WSGIRequestHandler):
            def log_message(self, *args):
                pass

        with make_server("127.0.0.1", 0, get_wsgi_application(), handler_class=Quiet) as server:
            worker = Thread(target=server.serve_forever, daemon=True)
            worker.start()
            try:
                address = f"http://127.0.0.1:{server.server_port}"
                with urlopen(address + "/health/", timeout=3) as response:
                    assert response.status == 200
                    assert json.load(response) == {"status": "ok"}
                try:
                    urlopen(address + "/notes/101/", timeout=3)
                except HTTPError as error:
                    assert error.code == 404
                    refused = error.read(4096)
                    assert b"Alpha private" not in refused and b"Release plan" not in refused
                else:
                    raise AssertionError("private route unexpectedly available")
            finally:
                server.shutdown()
                worker.join(timeout=3)
                connections.close_all()
        print(json.dumps({"health": 200, "anonymous_note": 404,
                          "workspace_rows": 2, "note_ids": [101, 103, 202],
                          "orm_and_http": "passed", "transport": "loopback HTTP; no TLS/browser claim"}))


def command_cases():
    cases = [
        ("mypy_accept", "examples/ch10", ["-m", "mypy", "--strict", "checked_types.py"], 0),
        ("mypy_refuse", "examples/ch10", ["-m", "mypy", "--strict", "bad_types.py"], 1),
        ("pytest12", "examples/ch12", ["-m", "pytest", "-q"], 0),
        ("django19_check", "examples/ch19", ["manage.py", "check"], 0),
        ("django19_migrations", "examples/ch19", ["manage.py", "makemigrations", "--check", "--dry-run"], 0),
        ("django19_tests", "examples/ch19", ["manage.py", "test", "notes", "-v", "2"], 0),
        ("django19_live", ".", ["examples/verify_book.py", "--live19"], 0),
        ("password21", "examples/ch21", ["django_passwords.py"], 0),
        ("recovery21", "examples/ch21", ["-m", "unittest", "-v", "test_recovery"], 0),
        ("claims22", "examples/ch22", ["-m", "unittest", "-v", "test_claims"], 0),
        ("jwt22", "examples/ch22", ["-m", "unittest", "-v", "test_jwt"], 0),
        ("sessions22", "examples/ch22", ["django_sessions.py"], 0),
        ("browser24", ".", ["-m", "unittest", "-v", "examples.ch24.test_browser"], 0),
        ("http30", ".", ["-m", "unittest", "-v", "examples.ch30.test_http"], 0),
        ("local30", ".", ["-m", "unittest", "-v", "examples.ch30.test_local"], 0),
        ("shrink30", ".", ["-m", "examples.ch30.shrink_demo"], 0),
        ("core42", ".", ["-m", "unittest", "-v", "examples.ch42.test_capstone"], 0),
        ("web42", ".", ["-m", "unittest", "-v", "examples.ch42.test_web"], 0),
    ]
    for number, module in [(20, "test_contract"), (23, "test_authorization"),
                           (25, "test_attachments"), (26, "test_integrations"),
                           (27, "test_crypto"), (28, "test_queue")]:
        directory = f"examples/ch{number}" if number in (20, 23) else "."
        name = module if number in (20, 23) else f"examples.ch{number}.{module}"
        cases.append((f"core{number}", directory, ["-m", "unittest", "-v", name], 0))
    for name in ("values", "rules", "checks", "notebook_demo"):
        cases.append((f"appendix_{name}", ".", ["-m", f"examples.appendices.{name}"], 0))
    return cases


def execute(case):
    name, directory, args, expected = case
    process = subprocess.run([sys.executable, *args], cwd=ROOT / directory,
                             text=True, capture_output=True, timeout=120)
    transcript = process.stdout + process.stderr
    counts = re.search(r"Ran (\d+) tests?", transcript)
    pytest_count = re.search(r"(\d+) passed", transcript) if name == "pytest12" else None
    success = process.returncode == expected
    if name == "mypy_refuse":
        success = success and "Found 2 errors" in transcript
    return name, {"command": ["python", *args], "cwd": directory,
                  "expected_exit": expected, "exit_code": process.returncode,
                  "matched_expectation": success,
                  "test_methods": int((counts or pytest_count)[1]) if counts or pytest_count else None,
                  "stdout": process.stdout, "stderr": process.stderr}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=ROOT / "examples/verification/current.json")
    parser.add_argument("--live19", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.live19:
        live19()
        return
    if platform.python_version() != "3.12.14":
        raise SystemExit("Exact reproduction requires CPython 3.12.14")
    for line in (ROOT / "requirements-tested.txt").read_text().splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        name, expected = line.split("==")
        if importlib.metadata.version(name) != expected:
            raise SystemExit(f"Install the tested requirement: {name}=={expected}")
    from cryptography.hazmat.backends import default_backend
    with ThreadPoolExecutor(max_workers=4) as pool:
        results = dict(pool.map(execute, command_cases()))
    versions = {dist.metadata["Name"]: dist.version for dist in importlib.metadata.distributions()}
    sources = {}
    sources["examples/verify_book.py"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    for number in (10, 12, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 30, 42):
        for path in sorted((ROOT / f"examples/ch{number}").rglob("*.py")):
            sources[str(path.relative_to(ROOT))] = hashlib.sha256(path.read_bytes()).hexdigest()
    report = {"record_kind": "actual local book verification", "collected_at_utc": datetime.now(timezone.utc).isoformat(),
              "runtime": {"python": platform.python_version(), "sqlite": sqlite3.sqlite_version,
                          "python_openssl": ssl.OPENSSL_VERSION,
                          "cryptography_openssl": default_backend().openssl_version_text()},
              "packages": dict(sorted(versions.items())), "commands": results, "sources_sha256": sources,
              "limits": ["macOS local fixtures and loopback HTTP only", "no Windows installer execution",
                         "no browser-engine CSP/CORS/cookie enforcement", "no hosted provider, key custody or production approval"]}
    args.out.parent.mkdir(exist_ok=True, parents=True)
    args.out.write_text(json.dumps(report, indent=2) + "\n")
    for name, result in results.items():
        print(name, "PASS" if result["matched_expectation"] else "FAIL", result["test_methods"] or "")
    if not all(result["matched_expectation"] for result in results.values()):
        raise SystemExit("One or more checks failed; inspect the retained report")


if __name__ == "__main__":
    main()
