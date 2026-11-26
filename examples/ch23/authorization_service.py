"""Local authorization laboratory: trusted fixture identities, no HTTP authentication."""
from contextlib import closing, contextmanager
from dataclasses import dataclass
import json
import sqlite3


class AccessDenied(PermissionError):
    def __init__(self, status=404, code="not_found"):
        self.status = status
        self.code = code
        super().__init__(code)


def positive_id(value):
    return type(value) is int and 1 <= value <= 2**63 - 1


@contextmanager
def unit(path, *, write=False):
    with closing(sqlite3.connect(path, autocommit=True, timeout=2)) as db:
        db.row_factory = sqlite3.Row
        db.execute("PRAGMA foreign_keys = ON")
        db.execute("BEGIN IMMEDIATE" if write else "BEGIN")
        try:
            yield db
        except BaseException:
            db.execute("ROLLBACK")
            raise
        else:
            db.execute("COMMIT")


def seed(path):
    with unit(path, write=True) as db:
        for statement in (
            "CREATE TABLE workspaces (id INTEGER PRIMARY KEY, name TEXT UNIQUE NOT NULL)",
            "CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT NOT NULL, active INTEGER NOT NULL CHECK(active IN (0,1)))",
            """CREATE TABLE memberships (
                workspace_id INTEGER NOT NULL REFERENCES workspaces(id),
                user_id INTEGER NOT NULL REFERENCES users(id),
                role TEXT NOT NULL CHECK(role IN ('member','manager')),
                active INTEGER NOT NULL CHECK(active IN (0,1)),
                PRIMARY KEY(workspace_id,user_id))""",
            """CREATE TABLE notes (
                id INTEGER PRIMARY KEY, workspace_id INTEGER NOT NULL REFERENCES workspaces(id),
                owner_id INTEGER NOT NULL REFERENCES users(id), title TEXT NOT NULL,
                body TEXT NOT NULL, state TEXT NOT NULL, version INTEGER NOT NULL,
                updated_by INTEGER NOT NULL REFERENCES users(id))""",
        ):
            db.execute(statement)
        db.executemany("INSERT INTO workspaces VALUES (?,?)", [(1, "Alpha"), (2, "Beta")])
        db.executemany("INSERT INTO users VALUES (?,?,1)", [(1, "Mina"), (2, "Ravi"), (3, "Lee")])
        db.executemany("INSERT INTO memberships VALUES (?,?,?,1)",
                       [(1, 1, "member"), (2, 2, "member"), (1, 3, "manager")])
        db.executemany("INSERT INTO notes VALUES (?,?,?,?,?,?,?,?)", [
            (101, 1, 1, "Release plan", "Alpha private fixture", "open", 1, 1),
            (202, 2, 2, "Pricing review", "Beta private fixture", "open", 1, 2),
        ])


def require_member(db, user_id, workspace_id):
    if user_id is None:
        raise AccessDenied(403, "access_denied")
    if not positive_id(user_id) or not positive_id(workspace_id):
        raise AccessDenied()
    row = db.execute("""SELECT m.role FROM memberships AS m
        JOIN users AS u ON u.id = m.user_id AND u.active = 1
        WHERE m.workspace_id = ? AND m.user_id = ? AND m.active = 1
          AND m.role IN ('member','manager')""", (workspace_id, user_id)).fetchone()
    if row is None:
        raise AccessDenied()
    return row["role"]


# Reuse this complete authorization scope, never a global evaluated list of notes.
VISIBLE_SQL = """SELECT n.id, n.workspace_id, n.title, n.body FROM notes AS n
    JOIN memberships AS m ON m.workspace_id = n.workspace_id AND m.user_id = ?
        AND m.active = 1 AND m.role IN ('member','manager')
    JOIN users AS u ON u.id = m.user_id AND u.active = 1
    WHERE n.workspace_id = ?"""


def visible_rows(db, *, user_id, workspace_id, note_ids=None, limit=20):
    sql = VISIBLE_SQL
    parameters = [user_id, workspace_id]
    if note_ids is not None:
        # Only placeholder syntax is generated. Each identifier remains a bound value.
        sql += " AND n.id IN (" + ",".join("?" for _ in note_ids) + ")"
        parameters.extend(note_ids)
    sql += " ORDER BY n.id LIMIT ?"
    parameters.append(limit)
    return [dict(row) for row in db.execute(sql, parameters)]


def note_fields(row, *, body=False):
    fields = ("id", "workspace_id", "title", "body") if body else ("id", "workspace_id", "title")
    return {field: row[field] for field in fields}


def list_for_user(path, *, user_id, workspace_id, limit=20):
    if type(limit) is not int or not 1 <= limit <= 50:
        raise ValueError("limit must be an integer from 1 to 50")
    with unit(path) as db:
        require_member(db, user_id, workspace_id)
        rows = visible_rows(db, user_id=user_id, workspace_id=workspace_id, limit=limit)
        return [note_fields(row) for row in rows]


def detail_for_user(path, *, user_id, workspace_id, note_id):
    with unit(path) as db:
        require_member(db, user_id, workspace_id)
        if not positive_id(note_id):
            raise AccessDenied()
        rows = visible_rows(db, user_id=user_id, workspace_id=workspace_id,
                            note_ids=[note_id], limit=1)
        if not rows:
            raise AccessDenied()
        return note_fields(rows[0], body=True)


def export_selection(note_ids):
    if (not isinstance(note_ids, (list, tuple)) or not 1 <= len(note_ids) <= 10
            or not all(positive_id(value) for value in note_ids)
            or len(set(note_ids)) != len(note_ids)):
        raise ValueError("select 1 to 10 distinct positive note IDs")
    return tuple(sorted(note_ids))


@dataclass(frozen=True)
class Artifact:
    # Trusted in-process record only; never construct it from a browser or queue payload.
    requested_by: int
    workspace_id: int
    note_ids: tuple[int, ...]
    payload: bytes


def selected_rows(db, *, user_id, workspace_id, note_ids):
    require_member(db, user_id, workspace_id)
    rows = visible_rows(db, user_id=user_id, workspace_id=workspace_id,
                        note_ids=note_ids, limit=10)
    if len(rows) != len(note_ids):
        raise AccessDenied()  # No partial export if any selected note is inaccessible.
    return rows


def build_export(path, *, user_id, workspace_id, note_ids):
    ids = export_selection(note_ids)
    with unit(path) as db:
        rows = selected_rows(db, user_id=user_id, workspace_id=workspace_id, note_ids=ids)
        document = {"workspace_id": workspace_id,
                    "notes": [note_fields(row, body=True) for row in rows]}
        payload = json.dumps(document, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        return Artifact(user_id, workspace_id, ids, payload)


def download_export(path, *, user_id, artifact):
    # artifact must come from trusted service-managed storage, not client-supplied metadata.
    with unit(path) as db:
        require_member(db, user_id, artifact.workspace_id)
        if user_id != artifact.requested_by:
            raise AccessDenied()
        selected_rows(db, user_id=user_id, workspace_id=artifact.workspace_id,
                      note_ids=artifact.note_ids)
        return artifact.payload


def revoke_member(path, *, actor_id, workspace_id, target_user_id):
    if not positive_id(target_user_id):
        raise AccessDenied()
    with unit(path, write=True) as db:
        if require_member(db, actor_id, workspace_id) != "manager":
            raise AccessDenied(403, "action_denied")
        changed = db.execute("""UPDATE memberships SET active = 0
            WHERE workspace_id = ? AND user_id = ? AND role = 'member' AND active = 1""",
            (workspace_id, target_user_id)).rowcount
        if changed != 1:
            raise AccessDenied()


def response(operation):
    # Models the selected contract status/body; it is not an HttpResponse or HTTP server.
    try:
        return 200, operation()
    except AccessDenied as exc:
        return exc.status, {"error": {"code": exc.code}}


def list_view(path, *, user_id, workspace_id, limit=20):
    return response(lambda: list_for_user(path, user_id=user_id, workspace_id=workspace_id, limit=limit))


def detail_view(path, *, user_id, workspace_id, note_id):
    return response(lambda: detail_for_user(path, user_id=user_id, workspace_id=workspace_id, note_id=note_id))


def snapshot(path):
    # Privileged local evidence, not an API response or a support screen.
    with unit(path) as db:
        return {name: [dict(row) for row in db.execute(f"SELECT * FROM {name} ORDER BY 1,2")]
                for name in ("workspaces", "users", "memberships", "notes")}
