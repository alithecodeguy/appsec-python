"""Local contract model, not an HTTP endpoint or authentication mechanism."""
from contextlib import closing, contextmanager
import json
import re
import sqlite3


class ContractError(Exception):
    def __init__(self, status, code):
        self.status = status
        self.code = code
        super().__init__(code)


def reject(status, code):
    raise ContractError(status, code)


def parse_object(body, content_type):
    if content_type.partition(";")[0].strip().lower() != "application/json":
        reject(415, "unsupported_media_type")
    if len(body) > 4096:
        reject(413, "body_too_large")

    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                reject(400, "invalid_json")
            result[key] = value
        return result

    def constant(value):
        reject(400, "invalid_json")

    try:
        payload = json.loads(body.decode("utf-8"), object_pairs_hook=pairs,
                             parse_constant=constant)
    except (UnicodeDecodeError, ValueError, RecursionError):
        reject(400, "invalid_json")
    if not isinstance(payload, dict):
        reject(400, "object_required")
    return payload


def positive_int(value):
    return type(value) is int and 1 <= value <= 2**63 - 1


def title_value(value):
    if (not isinstance(value, str) or not 1 <= len(value) <= 200
            or not value.strip() or any(ord(char) < 32 or 127 <= ord(char) <= 159
                                        or 0xD800 <= ord(char) <= 0xDFFF for char in value)):
        reject(422, "invalid_title")
    return value


@contextmanager
def write_transaction(path):
    with closing(sqlite3.connect(path, autocommit=True, timeout=2)) as db:
        db.row_factory = sqlite3.Row
        db.execute("PRAGMA foreign_keys = ON")
        db.execute("BEGIN IMMEDIATE")
        try:
            yield db
        except BaseException:
            db.execute("ROLLBACK")
            raise
        else:
            db.execute("COMMIT")


def seed(path):
    # Fresh synthetic database only: repeated setup fails instead of overwriting.
    statements = (
        "CREATE TABLE workspaces (id INTEGER PRIMARY KEY, name TEXT UNIQUE NOT NULL)",
        "CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT UNIQUE NOT NULL)",
        """CREATE TABLE memberships (
            workspace_id INTEGER REFERENCES workspaces(id),
            user_id INTEGER REFERENCES users(id),
            role TEXT NOT NULL CHECK(role IN ('member', 'manager')),
            active INTEGER NOT NULL CHECK(active IN (0, 1)),
            PRIMARY KEY(workspace_id, user_id))""",
        """CREATE TABLE notes (
            id INTEGER PRIMARY KEY, workspace_id INTEGER NOT NULL REFERENCES workspaces(id),
            owner_id INTEGER NOT NULL REFERENCES users(id), title TEXT NOT NULL,
            body TEXT NOT NULL, state TEXT NOT NULL CHECK(state IN ('open', 'archived')),
            version INTEGER NOT NULL CHECK(version > 0),
            updated_by INTEGER NOT NULL REFERENCES users(id))""",
        """CREATE TABLE export_requests (
            id INTEGER PRIMARY KEY, workspace_id INTEGER NOT NULL REFERENCES workspaces(id),
            requester_id INTEGER NOT NULL REFERENCES users(id), idem_key TEXT NOT NULL,
            request_json TEXT NOT NULL, response_json TEXT NOT NULL,
            state TEXT NOT NULL CHECK(state = 'queued'),
            UNIQUE(workspace_id, requester_id, idem_key))""",
    )
    with write_transaction(path) as db:
        for statement in statements:
            db.execute(statement)
        db.executemany("INSERT INTO workspaces VALUES (?, ?)", [(1, "Alpha"), (2, "Beta")])
        db.executemany("INSERT INTO users VALUES (?, ?)", [(1, "Mina"), (2, "Ravi"), (3, "Lee")])
        db.executemany("INSERT INTO memberships VALUES (?, ?, ?, ?)",
                       [(1, 1, "member", 1), (2, 2, "member", 1), (1, 3, "manager", 1)])
        db.executemany("INSERT INTO notes VALUES (?, ?, ?, ?, ?, ?, ?, ?)", [
            (101, 1, 1, "Release plan", "Alpha private fixture", "open", 1, 1),
            (202, 2, 2, "Pricing review", "Beta private fixture", "open", 1, 2),
        ])


def member(db, actor_id, workspace_id):
    # actor_id comes from the local test caller, never from a JSON field/header.
    if actor_id is None:
        reject(403, "access_denied")
    row = db.execute("""SELECT role FROM memberships
                        WHERE workspace_id = ? AND user_id = ? AND active = 1""",
                     (workspace_id, actor_id)).fetchone()
    if row is None:
        reject(404, "not_found")
    return row["role"]


def scoped_note(db, workspace_id, note_id):
    row = db.execute("SELECT * FROM notes WHERE workspace_id = ? AND id = ?",
                     (workspace_id, note_id)).fetchone()
    if row is None:
        reject(404, "not_found")
    return row


def note_response(row):
    fields = ("id", "workspace_id", "owner_id", "title", "state", "version", "updated_by")
    return {key: row[key] for key in fields}


def create_note(path, *, actor_id, workspace_id, payload):
    if not isinstance(payload, dict) or set(payload) != {"title"}:
        reject(422, "invalid_fields")
    title = title_value(payload["title"])
    with write_transaction(path) as db:
        member(db, actor_id, workspace_id)
        cursor = db.execute("""INSERT INTO notes
            (workspace_id, owner_id, title, body, state, version, updated_by)
            VALUES (?, ?, ?, '', 'open', 1, ?)""", (workspace_id, actor_id, title, actor_id))
        result = note_response(scoped_note(db, workspace_id, cursor.lastrowid))
    return 201, result


def update_note(path, *, actor_id, workspace_id, note_id, payload):
    if not isinstance(payload, dict):
        reject(422, "invalid_fields")
    if set(payload) - {"title", "state", "expected_version"}:
        reject(422, "invalid_fields")
    if not positive_int(payload.get("expected_version")) or not ({"title", "state"} & set(payload)):
        reject(422, "invalid_fields")
    if "title" in payload:
        title_value(payload["title"])
    if "state" in payload and payload["state"] not in ("open", "archived"):
        reject(422, "invalid_state")
    with write_transaction(path) as db:
        role = member(db, actor_id, workspace_id)
        row = scoped_note(db, workspace_id, note_id)
        if row["version"] != payload["expected_version"]:
            reject(409, "stale_version")
        if row["version"] == 2**63 - 1:
            reject(409, "version_exhausted")
        target = payload.get("state", row["state"])
        if row["state"] != "open" or ("state" in payload and target != "archived"):
            reject(409, "invalid_transition")
        if target == "archived" and role != "manager":
            reject(403, "action_denied")
        title = payload.get("title", row["title"])
        db.execute("""UPDATE notes SET title = ?, state = ?, version = version + 1,
                      updated_by = ? WHERE workspace_id = ? AND id = ?""",
                   (title, target, actor_id, workspace_id, note_id))
        result = note_response(scoped_note(db, workspace_id, note_id))
    return 200, result


def request_export(path, *, actor_id, workspace_id, key, payload):
    if not isinstance(key, str) or re.fullmatch(r"[A-Za-z0-9_-]{1,64}", key) is None:
        reject(422, "invalid_idempotency_key")
    if not isinstance(payload, dict) or set(payload) != {"note_ids"}:
        reject(422, "invalid_fields")
    ids = payload["note_ids"]
    if (not isinstance(ids, list) or not 1 <= len(ids) <= 10
            or not all(positive_int(item) for item in ids) or len(set(ids)) != len(ids)):
        reject(422, "invalid_note_ids")
    canonical = json.dumps({"note_ids": sorted(ids)}, separators=(",", ":"))
    with write_transaction(path) as db:
        member(db, actor_id, workspace_id)
        for note_id in ids:
            scoped_note(db, workspace_id, note_id)
        previous = db.execute("""SELECT request_json, response_json FROM export_requests
            WHERE workspace_id = ? AND requester_id = ? AND idem_key = ?""",
            (workspace_id, actor_id, key)).fetchone()
        if previous is not None:
            if previous["request_json"] != canonical:
                reject(409, "idempotency_conflict")
            result = json.loads(previous["response_json"])
        else:
            cursor = db.execute("""INSERT INTO export_requests
                (workspace_id, requester_id, idem_key, request_json, response_json, state)
                VALUES (?, ?, ?, ?, '{}', 'queued')""", (workspace_id, actor_id, key, canonical))
            result = {"job_id": cursor.lastrowid, "workspace_id": workspace_id, "state": "queued"}
            db.execute("UPDATE export_requests SET response_json = ? WHERE id = ?",
                       (json.dumps(result, separators=(",", ":")), cursor.lastrowid))
    return 202, result


def snapshot(path):
    # Privileged local evidence only; never return this from a public endpoint.
    with closing(sqlite3.connect(path, autocommit=True)) as db:
        db.row_factory = sqlite3.Row
        return {
            "notes": [dict(row) for row in db.execute("SELECT * FROM notes ORDER BY id")],
            "exports": [dict(row) for row in db.execute("SELECT * FROM export_requests ORDER BY id")],
        }
