"""Bounded local queue laboratory; all caller identities and keyrings are trusted inputs."""
import json
import re
import sqlite3
import time

from examples.ch23.authorization_service import (
    AccessDenied, export_selection, selected_rows, unit,
)
from examples.ch27.export_crypto import (
    MAX_PLAINTEXT, authorize_record, decrypt, encrypt,
    initialize as initialize_crypto,
)

MAX_PENDING = 2
MAX_TENANT_PENDING = 1
LIFETIME = 60


class QueueFull(ValueError):
    pass


class IntentConflict(ValueError):
    pass


def initialize(database):
    initialize_crypto(database)
    with unit(database, write=True) as db:
        db.execute("""CREATE TABLE export_requests (
            id INTEGER PRIMARY KEY,
            requested_by INTEGER NOT NULL REFERENCES users(id),
            workspace_id INTEGER NOT NULL REFERENCES workspaces(id),
            client_key TEXT NOT NULL, note_ids TEXT NOT NULL,
            expires_at INTEGER NOT NULL,
            state TEXT NOT NULL CHECK(state IN ('queued','ready','denied','expired','failed')),
            error TEXT,
            UNIQUE(requested_by,workspace_id,client_key))""")
        db.execute("""CREATE TABLE export_slots (
            request_id INTEGER NOT NULL PRIMARY KEY REFERENCES export_requests(id),
            export_id INTEGER UNIQUE REFERENCES encrypted_exports(id))""")


def enqueue(database, *, user_id, workspace_id, note_ids, client_key, now):
    ids = export_selection(note_ids)
    if not isinstance(client_key, str) or re.fullmatch(r"[A-Za-z0-9_-]{1,40}", client_key) is None:
        raise ValueError("invalid_request_key")
    encoded = json.dumps(ids)
    with unit(database, write=True) as db:
        selected_rows(db, user_id=user_id, workspace_id=workspace_id, note_ids=ids)
        prior = db.execute("""SELECT * FROM export_requests
            WHERE requested_by=? AND workspace_id=? AND client_key=?""",
            (user_id, workspace_id, client_key)).fetchone()
        if prior is not None:
            if prior["note_ids"] != encoded:
                raise IntentConflict("request_key_reused_with_different_selection")
            return prior["id"]  # Retry keeps the original deadline and state.
        total = db.execute("SELECT count(*) FROM export_requests WHERE state='queued'").fetchone()[0]
        tenant = db.execute("""SELECT count(*) FROM export_requests
            WHERE state='queued' AND workspace_id=?""", (workspace_id,)).fetchone()[0]
        if total >= MAX_PENDING or tenant >= MAX_TENANT_PENDING:
            raise QueueFull("queue_full")
        return db.execute("""INSERT INTO export_requests
            (requested_by,workspace_id,client_key,note_ids,expires_at,state)
            VALUES (?,?,?,?,?,'queued')""",
            (user_id, workspace_id, client_key, encoded, now + LIFETIME)).lastrowid


def probe(database, request_id):
    # Diagnostic only. This observation is deliberately NOT used as a claim.
    with unit(database) as db:
        return db.execute("SELECT 1 FROM export_slots WHERE request_id=?", (request_id,)).fetchone() is None


def process_request(database, *, request_id, keyring, now, after_probe=None):
    missing = probe(database, request_id)  # Connection/transaction closes before the test barrier.
    if after_probe is not None:
        after_probe(missing)  # Trusted test coordination only; never run under the write lock.
    with unit(database, write=True) as db:
        row = db.execute("SELECT * FROM export_requests WHERE id=?", (request_id,)).fetchone()
        if row is None:
            raise ValueError("unknown_request")
        request = dict(row)
        if request["state"] in ("denied", "expired", "failed"):
            return request["state"]
        won = db.execute("""INSERT INTO export_slots (request_id) VALUES (?)
            ON CONFLICT(request_id) DO NOTHING RETURNING request_id""", (request_id,)).fetchone()
        if won is None:
            return "duplicate"  # The winning transaction committed slot, artifact and ready state together.
        def refuse(state, error):
            db.execute("DELETE FROM export_slots WHERE request_id=?", (request_id,))
            db.execute("UPDATE export_requests SET state=?,error=? WHERE id=?", (state, error, request_id))
            return state
        if now >= request["expires_at"]:
            return refuse("expired", "deadline_reached")
        try:
            rows = selected_rows(db, user_id=request["requested_by"], workspace_id=request["workspace_id"],
                                 note_ids=json.loads(request["note_ids"]))
        except AccessDenied:
            return refuse("denied", "access_denied")
        payload = json.dumps({"workspace_id":request["workspace_id"], "notes":rows},
                             ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        if len(payload) > MAX_PLAINTEXT:
            return refuse("failed", "export_too_large")
        cursor = db.execute("""INSERT INTO encrypted_exports
            (workspace_id,requested_by,note_ids,format_version,generation,key_id,nonce,ciphertext)
            VALUES (?,?,?,1,1,?,X'',X'')""",
            (request["workspace_id"], request["requested_by"], request["note_ids"], keyring.active))
        record = dict(db.execute("SELECT * FROM encrypted_exports WHERE id=?", (cursor.lastrowid,)).fetchone())
        kid, nonce, ciphertext = encrypt(db, record, payload, keyring)
        db.execute("UPDATE encrypted_exports SET key_id=?,nonce=?,ciphertext=? WHERE id=?",
                   (kid, nonce, ciphertext, record["id"]))
        db.execute("UPDATE export_slots SET export_id=? WHERE request_id=?", (record["id"], request_id))
        db.execute("UPDATE export_requests SET state='ready',error=NULL WHERE id=?", (request_id,))
        return "created"


def download(database, *, user_id, request_id, keyring, now):
    with unit(database) as db:
        request = db.execute("SELECT * FROM export_requests WHERE id=?", (request_id,)).fetchone()
        if (request is None or user_id is None or user_id != request["requested_by"]
                or request["state"] != "ready" or now >= request["expires_at"]):
            raise AccessDenied()
        row = db.execute("""SELECT e.* FROM encrypted_exports AS e
            JOIN export_slots AS s ON s.export_id=e.id WHERE s.request_id=?""", (request_id,)).fetchone()
        if row is None:
            raise AccessDenied()
        record = dict(row)
        authorize_record(db, record, user_id)  # Fresh membership/visibility check at release.
        return decrypt(record, keyring)


def run_with_retry(operation, *, pause=time.sleep):
    # One delivery: at most three attempts. Persistent scheduling/dead-letter ownership is external.
    for attempt in range(3):
        try:
            return operation()
        except sqlite3.OperationalError as exc:
            if (getattr(exc, "sqlite_errorcode", -1) & 255) != sqlite3.SQLITE_BUSY or attempt == 2:
                raise
            pause(0.01 * (attempt + 1))


def inventory(database):
    # Privileged test snapshot, never an API or a log payload.
    with unit(database) as db:
        names = ("export_requests", "export_slots", "encrypted_exports", "used_nonces")
        return {name:[dict(row) for row in db.execute(f"SELECT * FROM {name} ORDER BY 1")]
                for name in names}
