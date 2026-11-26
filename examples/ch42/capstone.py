"""CB-EXPORT-41 revision 1: isolated local service, no caller-supplied identity authority."""
from dataclasses import dataclass
import json
import re
import sqlite3

from examples.ch23.authorization_service import (
    AccessDenied, export_selection, positive_id, require_member, selected_rows, unit,
)
from examples.ch27.export_crypto import (
    MAX_PLAINTEXT, CannotOpen, authorize_record, decrypt, encrypt, initialize as initialize_crypto,
)

POLICY = "CB-EXPORT-41-r1"
LIFETIME, GRACE, RETENTION = 60, 900, 7*86400
TERMINAL = {"denied", "failed", "expired"}


class Problem(ValueError):
    def __init__(self, status, code):
        self.status, self.code = status, code
        super().__init__(code)


class Cancelled(Exception):
    pass


@dataclass
class Clock:
    value: int = 1795687200  # 2026-11-26 10:00:00 UTC, exercise time only.
    def __call__(self):
        return self.value


def initialize(database):
    initialize_crypto(database)  # Fresh path only; preserves chapter 23's seed.
    with unit(database, write=True) as db:
        db.execute("""CREATE TABLE jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            requested_by INTEGER NOT NULL REFERENCES users(id),
            workspace_id INTEGER NOT NULL REFERENCES workspaces(id),
            client_key TEXT NOT NULL, note_ids TEXT NOT NULL,
            created_at INTEGER NOT NULL, expires_at INTEGER NOT NULL, closed_at INTEGER,
            state TEXT NOT NULL CHECK(state IN ('queued','ready','denied','failed','expired')),
            reserved INTEGER NOT NULL CHECK(reserved IN (0,1)),
            deleted_at INTEGER, retain_until INTEGER, cleanup_error TEXT,
            breached INTEGER NOT NULL DEFAULT 0 CHECK(breached IN (0,1)),
            UNIQUE(requested_by,workspace_id,client_key))""")
        db.execute("""CREATE TABLE result_slots (
            job_id INTEGER NOT NULL PRIMARY KEY REFERENCES jobs(id),
            export_id INTEGER UNIQUE REFERENCES encrypted_exports(id))""")
        db.execute("""CREATE TABLE export_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT, job_id INTEGER NOT NULL REFERENCES jobs(id),
            workspace_id INTEGER NOT NULL, actor TEXT NOT NULL, outcome TEXT NOT NULL,
            at INTEGER NOT NULL, policy TEXT NOT NULL)""")


def event(db, job, actor, outcome, at):
    db.execute("INSERT INTO export_events (job_id,workspace_id,actor,outcome,at,policy) VALUES (?,?,?,?,?,?)",
               (job["id"], job["workspace_id"], actor, outcome, at, POLICY))


def access_end(job):
    return min(job["expires_at"], job["closed_at"] if job["closed_at"] is not None else job["expires_at"])


def effective_state(job, now):
    return "expired" if job["state"] not in TERMINAL and now >= access_end(job) else job["state"]


def authorized_job(db, user_id, workspace_id, job_id, *, manager=False):
    role = require_member(db, user_id, workspace_id)
    if not positive_id(job_id):
        raise AccessDenied()
    row = db.execute("SELECT * FROM jobs WHERE id=? AND workspace_id=?", (job_id, workspace_id)).fetchone()
    if row is None or (row["requested_by"] != user_id and not (manager and role == "manager")):
        raise AccessDenied()
    return dict(row)


def request_export(database, *, user_id, workspace_id, body, client_key, clock):
    with unit(database, write=True) as db:
        require_member(db, user_id, workspace_id)
        if (not isinstance(body, dict) or set(body) != {"note_ids"}
                or not isinstance(body["note_ids"], list) or not isinstance(client_key, str)
                or re.fullmatch(r"[A-Za-z0-9_-]{1,40}", client_key) is None):
            raise Problem(400, "invalid_request")
        try:
            ids = export_selection(body["note_ids"])
        except ValueError as exc:
            raise Problem(400, "invalid_request") from exc
        selected_rows(db, user_id=user_id, workspace_id=workspace_id, note_ids=ids)
        encoded = json.dumps(ids)
        prior = db.execute("""SELECT * FROM jobs WHERE requested_by=? AND workspace_id=? AND client_key=?""",
                           (user_id, workspace_id, client_key)).fetchone()
        if prior is not None:
            if prior["note_ids"] != encoded:
                raise Problem(409, "request_conflict")
            return {"job_id":prior["id"], "workspace_id":workspace_id, "state":"queued"}
        counts = db.execute("""SELECT count(*),coalesce(sum(workspace_id=?),0) FROM jobs
            WHERE state='queued'""", (workspace_id,)).fetchone()
        held = db.execute("""SELECT count(*),coalesce(sum(workspace_id=?),0) FROM jobs
            WHERE reserved=1""", (workspace_id,)).fetchone()
        if counts[0] >= 2 or counts[1] >= 1 or held[0] >= 4 or held[1] >= 2:
            raise Problem(429, "capacity_exhausted")
        now = clock()  # Service clock sampled after acquiring the transaction, never request JSON.
        job_id = db.execute("""INSERT INTO jobs
            (requested_by,workspace_id,client_key,note_ids,created_at,expires_at,state,reserved)
            VALUES (?,?,?,?,?,?,'queued',1)""",
            (user_id,workspace_id,client_key,encoded,now,now+LIFETIME)).lastrowid
        job = dict(db.execute("SELECT * FROM jobs WHERE id=?", (job_id,)).fetchone())
        event(db, job, f"user:{user_id}", "accepted", now)
        return {"job_id":job_id, "workspace_id":workspace_id, "state":"queued"}


def status(database, *, user_id, workspace_id, job_id, clock):
    with unit(database) as db:
        job = authorized_job(db, user_id, workspace_id, job_id)
        return {"job_id":job_id, "workspace_id":workspace_id,
                "state":effective_state(job,clock()), "expires_at":job["expires_at"]}


def close_job(db, job, state, now, actor):
    if job["state"] in TERMINAL:
        return job["state"]
    end = min(now, access_end(job))
    artifact = db.execute("SELECT export_id FROM result_slots WHERE job_id=?", (job["id"],)).fetchone()
    exists = artifact is not None and artifact["export_id"] is not None
    if not exists:
        db.execute("DELETE FROM result_slots WHERE job_id=?", (job["id"],))
    db.execute("""UPDATE jobs SET state=?,closed_at=?,reserved=?,retain_until=? WHERE id=?""",
               (state,end,int(exists),None if exists else end+RETENTION,job["id"]))
    event(db, job, actor, state, now)
    return state


def decode_message(raw):
    if not isinstance(raw, bytes) or len(raw) > 128:
        raise Problem(400, "invalid_message")
    def pairs(items):
        result = {}
        for key,value in items:
            if key in result: raise ValueError("duplicate key")
            result[key] = value
        return result
    try:
        message = json.loads(raw.decode("utf-8"), object_pairs_hook=pairs)
    except (ValueError, UnicodeDecodeError, RecursionError) as exc:
        raise Problem(400, "invalid_message") from exc
    if not isinstance(message,dict) or set(message) != {"job_id"} or not positive_id(message["job_id"]):
        raise Problem(400, "invalid_message")
    return message["job_id"]


def work(database, *, workspace_id, job_id, keyrings, clock, after_probe=None, checkpoint=None, stop=None):
    # workspace_id and keyrings come from trusted worker configuration, not its message.
    if not positive_id(workspace_id) or not positive_id(job_id) or workspace_id not in keyrings:
        raise Problem(404, "not_found")
    with unit(database) as db:
        missing = db.execute("SELECT 1 FROM result_slots WHERE job_id=?", (job_id,)).fetchone() is None
    if after_probe is not None: after_probe(missing)  # Test hook outside the write transaction.
    with unit(database, write=True) as db:
        row = db.execute("SELECT * FROM jobs WHERE id=? AND workspace_id=?", (job_id,workspace_id)).fetchone()
        if row is None: raise Problem(404, "not_found")
        job, now = dict(row), clock()
        if job["state"] in TERMINAL: return job["state"]
        if now >= access_end(job): return close_job(db,job,"expired",now,"worker")
        db.execute("SAVEPOINT preparation")
        won = db.execute("""INSERT INTO result_slots (job_id) VALUES (?)
            ON CONFLICT(job_id) DO NOTHING RETURNING job_id""", (job_id,)).fetchone()
        if won is None:
            db.execute("RELEASE preparation")
            return "duplicate"
        def refuse(state):
            db.execute("ROLLBACK TO preparation")
            db.execute("RELEASE preparation")
            return close_job(db,job,state,clock(),"worker")
        try:
            rows = selected_rows(db, user_id=job["requested_by"], workspace_id=job["workspace_id"],
                                 note_ids=json.loads(job["note_ids"]))
        except AccessDenied:
            return refuse("denied")
        payload = json.dumps({"workspace_id":workspace_id,"notes":rows},
                             ensure_ascii=False,separators=(",",":")).encode("utf-8")
        if len(payload) > MAX_PLAINTEXT: return refuse("failed")
        keyring = keyrings[workspace_id]
        export_id = db.execute("""INSERT INTO encrypted_exports
            (workspace_id,requested_by,note_ids,format_version,generation,key_id,nonce,ciphertext)
            VALUES (?,?,?,1,1,?,X'',X'')""",
            (workspace_id,job["requested_by"],job["note_ids"],keyring.active)).lastrowid
        record = dict(db.execute("SELECT * FROM encrypted_exports WHERE id=?", (export_id,)).fetchone())
        kid,nonce,ciphertext = encrypt(db,record,payload,keyring)
        db.execute("UPDATE encrypted_exports SET key_id=?,nonce=?,ciphertext=? WHERE id=?",
                   (kid,nonce,ciphertext,export_id))
        if checkpoint is not None: checkpoint()  # Test-controlled stop/time change; no external I/O in production.
        if stop is not None and stop.is_set(): raise Cancelled("preparation_cancelled")
        if clock() >= access_end(job): return refuse("expired")
        db.execute("UPDATE result_slots SET export_id=? WHERE job_id=?", (export_id,job_id))
        db.execute("RELEASE preparation")
        changed = db.execute("UPDATE jobs SET state='ready' WHERE id=? AND state='queued'", (job_id,)).rowcount
        if changed != 1: raise RuntimeError("publication_conflict")
        event(db,job,"worker","ready",clock())
        return "created"


def collect(database, *, user_id, workspace_id, job_id, keyrings, clock):
    # Write unit also makes the required local decision event part of successful release authorization.
    with unit(database, write=True) as db:
        job = authorized_job(db,user_id,workspace_id,job_id)
        selected_rows(db,user_id=user_id,workspace_id=workspace_id,note_ids=json.loads(job["note_ids"]))
        state = effective_state(job,clock())
        if state in TERMINAL or job["deleted_at"] is not None: raise Problem(410,"export_unavailable")
        if state != "ready": raise Problem(409,"export_not_ready")
        row = db.execute("""SELECT e.* FROM encrypted_exports AS e
            JOIN result_slots AS s ON s.export_id=e.id WHERE s.job_id=?""", (job_id,)).fetchone()
        if row is None or workspace_id not in keyrings: raise CannotOpen("export_unavailable")
        record = dict(row)
        if (record["workspace_id"] != workspace_id or record["requested_by"] != user_id
                or record["note_ids"] != job["note_ids"]):
            raise CannotOpen("export_unavailable")
        authorize_record(db,record,user_id)
        plaintext = decrypt(record,keyrings[workspace_id])
        now = clock()
        if now >= access_end(job): raise Problem(410,"export_unavailable")
        event(db,job,f"user:{user_id}","collect_authorized",now)
        return plaintext  # Context manager commits the event before the caller gets these bytes.


def expire(database, *, user_id, workspace_id, job_id, clock):
    with unit(database, write=True) as db:
        job = authorized_job(db,user_id,workspace_id,job_id,manager=True)
        return close_job(db,job,"expired",clock(),f"user:{user_id}")


def cleanup(database, *, job_id, clock):
    # Privileged maintenance. No keyring/decrypt operation and no caller-provided storage locator.
    try:
        with unit(database, write=True) as db:
            row = db.execute("SELECT * FROM jobs WHERE id=?", (job_id,)).fetchone()
            if row is None: return "missing"
            job, now = dict(row), clock()
            if job["state"] not in TERMINAL:
                if now < access_end(job): return "not_due"
                close_job(db,job,"expired",now,"cleanup")
                job = dict(db.execute("SELECT * FROM jobs WHERE id=?", (job_id,)).fetchone())
            if job["deleted_at"] is not None: return "deleted"
            slot = db.execute("SELECT export_id FROM result_slots WHERE job_id=?", (job_id,)).fetchone()
            if slot is None: return "no_payload"
            db.execute("DELETE FROM result_slots WHERE job_id=?", (job_id,))
            db.execute("DELETE FROM encrypted_exports WHERE id=?", (slot["export_id"],))
            db.execute("""UPDATE jobs SET reserved=0,deleted_at=?,retain_until=?,cleanup_error=NULL,
                breached=max(breached,?) WHERE id=?""",
                (now,now+RETENTION,int(now > access_end(job)+GRACE),job_id))
            event(db,job,"cleanup","deleted",now)
            return "deleted"
    except sqlite3.Error:
        # The local deletion/receipt unit rolled back. Record retry-required, if storage is usable.
        with unit(database, write=True) as db:
            row = db.execute("SELECT * FROM jobs WHERE id=?", (job_id,)).fetchone()
            if row is None: raise
            job, now = dict(row), clock()
            if job["state"] not in TERMINAL and now >= access_end(job):
                close_job(db,job,"expired",now,"cleanup")
                job = dict(db.execute("SELECT * FROM jobs WHERE id=?", (job_id,)).fetchone())
            db.execute("UPDATE jobs SET cleanup_error='retry_required',breached=max(breached,?) WHERE id=?",
                       (int(now > access_end(job)+GRACE),job_id))
            event(db,job,"cleanup","delete_failed",now)
        return "retry"


def purge(database, *, job_id, clock):
    with unit(database, write=True) as db:
        job = db.execute("SELECT * FROM jobs WHERE id=?", (job_id,)).fetchone()
        if job is None: return False
        if job["reserved"] or job["retain_until"] is None or clock() < job["retain_until"]: return False
        db.execute("DELETE FROM export_events WHERE job_id=?", (job_id,))
        db.execute("DELETE FROM result_slots WHERE job_id=?", (job_id,))
        db.execute("DELETE FROM jobs WHERE id=?", (job_id,))
        return True  # AUTOINCREMENT preserves the job-ID high-water mark; nonce history remains.


def snapshot(database):
    # Full privileged test evidence; never publish, serve, or log these rows.
    with unit(database) as db:
        names = ("jobs","result_slots","encrypted_exports","used_nonces","export_events")
        return {name:[dict(row) for row in db.execute(f"SELECT * FROM {name} ORDER BY 1")]
                for name in names}
