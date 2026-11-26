"""POSIX local attachment laboratory; no HTTP endpoint or antivirus claim."""
import hashlib
import os
from pathlib import Path
import re
import secrets
import stat
import tempfile

from examples.ch23.authorization_service import AccessDenied, require_member, seed, unit, visible_rows

MAX_BYTES = 64
CHUNK_BYTES = 16


class Rejected(ValueError):
    pass


def initialize(database, root):
    # Fresh, service-owned paths only. Uploaders must not control these directories.
    root.mkdir(mode=0o700)
    (root / "staging").mkdir(mode=0o700)
    (root / "objects").mkdir(mode=0o700)
    seed(database)
    with unit(database, write=True) as db:
        db.execute("""CREATE TABLE attachments (
            key TEXT PRIMARY KEY, workspace_id INTEGER NOT NULL REFERENCES workspaces(id),
            note_id INTEGER NOT NULL REFERENCES notes(id), uploaded_by INTEGER NOT NULL REFERENCES users(id),
            display_name TEXT NOT NULL, media_type TEXT NOT NULL, size INTEGER NOT NULL,
            sha256 TEXT NOT NULL)""")


def authorize(db, user_id, workspace_id, note_id):
    require_member(db, user_id, workspace_id)
    if not visible_rows(db, user_id=user_id, workspace_id=workspace_id, note_ids=[note_id], limit=1):
        raise AccessDenied()


def upload(database, root, *, user_id, workspace_id, note_id, display_name, media_type, stream):
    with unit(database) as db:
        authorize(db, user_id, workspace_id, note_id)
    if (not isinstance(display_name, str) or not 1 <= len(display_name) <= 80
            or display_name in (".", "..") or any(c in display_name for c in '/\\:')
            or any(ord(c) < 32 or 127 <= ord(c) <= 159 or 0xD800 <= ord(c) <= 0xDFFF for c in display_name)
            or not display_name.endswith(".txt")):
        raise Rejected("invalid_display_name")
    if media_type != "text/plain":
        raise Rejected("unsupported_media_type")
    descriptor, temporary = tempfile.mkstemp(prefix="incoming-", dir=root / "staging")
    temporary = Path(temporary)
    final = None
    published = False
    try:
        size = 0
        with os.fdopen(descriptor, "wb") as destination:
            while True:
                chunk = stream.read(min(CHUNK_BYTES, MAX_BYTES - size + 1))
                if not chunk:
                    break
                if not isinstance(chunk, bytes):
                    raise Rejected("binary_stream_required")
                if size + len(chunk) > MAX_BYTES:
                    raise Rejected("too_large")
                destination.write(chunk)
                size += len(chunk)
        if size == 0:
            raise Rejected("empty_file")
        data = temporary.read_bytes()  # Bounded by MAX_BYTES, not an unbounded upload read.
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise Rejected("invalid_utf8") from exc
        if any(ord(c) < 32 and c not in "\t\r\n" or 127 <= ord(c) <= 159 for c in text):
            raise Rejected("invalid_text")
        key = secrets.token_hex(16)
        final = root / "objects" / key
        # Hard-link publication refuses an existing key, including a pre-existing symlink.
        # Staging and objects are service-owned directories on the same filesystem.
        with unit(database, write=True) as db:
            authorize(db, user_id, workspace_id, note_id)  # Current permission after ingestion.
            os.link(temporary, final)
            published = True
            db.execute("INSERT INTO attachments VALUES (?,?,?,?,?,?,?,?)",
                       (key, workspace_id, note_id, user_id, display_name, "text/plain", size,
                        hashlib.sha256(data).hexdigest()))
        return key
    except BaseException:
        if published:
            final.unlink()  # Compensate for this attempt only; never delete an older collision.
        raise
    finally:
        temporary.unlink()  # Cleanup failures propagate; do not silently claim clean state.


def retrieve(database, root, *, user_id, key):
    if user_id is None:
        raise AccessDenied(403, "access_denied")
    if not isinstance(key, str) or re.fullmatch(r"[0-9a-f]{32}", key) is None:
        raise AccessDenied()
    with unit(database) as db:
        row = db.execute("SELECT * FROM attachments WHERE key=?", (key,)).fetchone()
        if row is None:
            raise AccessDenied()
        authorize(db, user_id, row["workspace_id"], row["note_id"])
        # O_NOFOLLOW protects the final component. Parent directories must remain trusted.
        descriptor = os.open(root / "objects" / key, os.O_RDONLY | os.O_NOFOLLOW)
        with os.fdopen(descriptor, "rb") as source:
            if not stat.S_ISREG(os.fstat(source.fileno()).st_mode):
                raise Rejected("not_regular_file")
            data = source.read(MAX_BYTES + 1)
        if len(data) != row["size"] or hashlib.sha256(data).hexdigest() != row["sha256"]:
            raise Rejected("stored_content_mismatch")
        return row["display_name"], data


def inventory(database, root):
    # Privileged local inspection only, not a list endpoint for arbitrary callers.
    with unit(database) as db:
        rows = [dict(row) for row in db.execute("SELECT * FROM attachments ORDER BY rowid")]
    return {"rows": rows, "objects": sorted(p.name for p in (root / "objects").iterdir()),
            "staging": sorted(p.name for p in (root / "staging").iterdir())}
