"""Synthetic recovery-state laboratory; no public routes or real mail delivery."""
from contextlib import closing, contextmanager
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import hashlib
import re
import secrets
import sqlite3


TTL_SECONDS = 15 * 60
PUBLIC_BODY = {"message": "If the account is eligible, recovery instructions will be sent."}
INVALID_BODY = {"error": "invalid_or_expired"}


@dataclass
class Clock:
    instant: datetime

    def now(self):
        if self.instant.tzinfo is None or self.instant.utcoffset() != timedelta(0):
            raise ValueError("Use an aware UTC clock")
        return int(self.instant.timestamp())

    def advance(self, seconds):
        if type(seconds) is not int or seconds < 0:
            raise ValueError("Advance by nonnegative whole seconds")
        self.instant += timedelta(seconds=seconds)


@dataclass(frozen=True)
class Delivery:
    account_id: int
    token: str


def token_digest(raw):
    return hashlib.sha256(raw.encode("ascii")).hexdigest()


@contextmanager
def transaction(path):
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


def seed(path, encoded_password="opaque-fixture-password-v1"):
    # The default is a test sentinel, not a usable password hash.
    with transaction(path) as db:
        db.execute("""CREATE TABLE accounts (
            id INTEGER PRIMARY KEY, email TEXT UNIQUE NOT NULL,
            active INTEGER NOT NULL CHECK(active IN (0, 1)),
            verified INTEGER NOT NULL CHECK(verified IN (0, 1)),
            password_hash TEXT NOT NULL, credential_revision INTEGER NOT NULL,
            session_epoch INTEGER NOT NULL)""")
        db.execute("""CREATE TABLE resets (
            digest TEXT PRIMARY KEY, account_id INTEGER NOT NULL REFERENCES accounts(id),
            issued_at INTEGER NOT NULL, expires_at INTEGER NOT NULL,
            issued_revision INTEGER NOT NULL, used_at INTEGER, revoked_at INTEGER)""")
        db.execute("INSERT INTO accounts VALUES (1, ?, 1, 1, ?, 1, 1)",
                   ("mina@example.test", encoded_password))


def request_reset(path, email, clock, outbox):
    # Fixture emails use exact ASCII spelling; this is not an email-normalization library.
    delivery = None
    with transaction(path) as db:
        row = db.execute("SELECT * FROM accounts WHERE email = ? AND active = 1 AND verified = 1",
                         (email,)).fetchone()
        if row is not None:
            raw = secrets.token_urlsafe(32)
            now = clock.now()
            db.execute("INSERT INTO resets VALUES (?, ?, ?, ?, ?, NULL, NULL)",
                       (token_digest(raw), row["id"], now, now + TTL_SECONDS,
                        row["credential_revision"]))
            delivery = Delivery(row["id"], raw)
    # A private local mailbox, not a field in the public response.
    if delivery is not None:
        outbox.append(delivery)
    return 202, dict(PUBLIC_BODY)


def complete_reset(path, raw, encoded_password, clock):
    # Trusted caller must validate the new password and obtain a library-produced hash first.
    # Tests pass an opaque sentinel. This function does not hash or check passwords.
    if not isinstance(encoded_password, str) or not encoded_password:
        raise ValueError("A validated replacement hash is required")
    if not isinstance(raw, str) or re.fullmatch(r"[A-Za-z0-9_-]{43}", raw) is None:
        return 400, dict(INVALID_BODY)
    with transaction(path) as db:
        now = clock.now()
        row = db.execute("""SELECT resets.*, accounts.active, accounts.verified,
                            accounts.credential_revision FROM resets
                            JOIN accounts ON accounts.id = resets.account_id
                            WHERE digest = ?""", (token_digest(raw),)).fetchone()
        if (row is None or not row["active"] or not row["verified"]
                or row["used_at"] is not None or row["revoked_at"] is not None
                or row["issued_revision"] != row["credential_revision"]
                or not row["issued_at"] <= now < row["expires_at"]):
            return 400, dict(INVALID_BODY)
        db.execute("""UPDATE accounts SET password_hash = ?,
                      credential_revision = credential_revision + 1,
                      session_epoch = session_epoch + 1 WHERE id = ?""",
                   (encoded_password, row["account_id"]))
        db.execute("UPDATE resets SET used_at = ? WHERE digest = ?", (now, row["digest"]))
        db.execute("""UPDATE resets SET revoked_at = ? WHERE account_id = ? AND digest != ?
                      AND used_at IS NULL AND revoked_at IS NULL""",
                   (now, row["account_id"], row["digest"]))
    return 200, {"message": "Password changed. Sign in again."}


def snapshot(path):
    # Privileged local evidence; never expose password hashes or token digests to support/public UI.
    with closing(sqlite3.connect(path, autocommit=True)) as db:
        db.row_factory = sqlite3.Row
        return {
            "accounts": [dict(row) for row in db.execute("SELECT * FROM accounts ORDER BY id")],
            "resets": [dict(row) for row in db.execute("SELECT * FROM resets ORDER BY digest")],
        }


def fresh_clock():
    return Clock(datetime(2026, 11, 26, 9, 0, 0, tzinfo=timezone.utc))
