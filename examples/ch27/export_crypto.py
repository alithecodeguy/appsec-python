"""Local encrypted-export laboratory. Keyring arguments are trusted service configuration."""
from dataclasses import dataclass, field
import json
import re
import secrets
from types import MappingProxyType

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from examples.ch23.authorization_service import (
    AccessDenied, build_export, require_member, seed, unit, visible_rows,
)

MAX_PLAINTEXT = 4096


class CannotOpen(ValueError):
    pass


@dataclass(frozen=True)
class Keyring:
    keys: dict = field(repr=False)
    active: str

    def __post_init__(self):
        copied = dict(self.keys)
        if (self.active not in copied or any(not isinstance(k,str) or re.fullmatch(r"[a-z0-9-]{1,32}",k) is None
                or not isinstance(v,bytes) or len(v) != 32 for k,v in copied.items())
                or len(set(copied.values())) != len(copied)):
            raise ValueError("Use distinct 256-bit keys with immutable key identifiers")
        object.__setattr__(self,"keys",MappingProxyType(copied))


def initialize(database):
    seed(database)
    with unit(database,write=True) as db:
        db.execute("""CREATE TABLE encrypted_exports (
            id INTEGER PRIMARY KEY, workspace_id INTEGER NOT NULL REFERENCES workspaces(id),
            requested_by INTEGER NOT NULL REFERENCES users(id), note_ids TEXT NOT NULL,
            format_version INTEGER NOT NULL, generation INTEGER NOT NULL,
            key_id TEXT NOT NULL, nonce BLOB NOT NULL, ciphertext BLOB NOT NULL)""")
        db.execute("""CREATE TABLE used_nonces (
            key_id TEXT NOT NULL, nonce BLOB NOT NULL, PRIMARY KEY(key_id,nonce))""")


def associated_data(record):
    if record["format_version"] != 1:
        raise CannotOpen("export_unavailable")
    context={"purpose":"casebook-private-export", "algorithm":"AES-256-GCM",
             **{field:record[field] for field in ("id","workspace_id","requested_by","note_ids",
                                                "format_version","generation","key_id")}}
    return json.dumps(context,sort_keys=True,separators=(",",":"),ensure_ascii=True).encode("ascii")


def encrypt(db,record,plaintext,keyring):
    if len(plaintext) > MAX_PLAINTEXT:
        raise ValueError("export_too_large")
    record={**record,"key_id":keyring.active}
    nonce=secrets.token_bytes(12)
    # Reserve before encrypting: a repeated key-ID/nonce pair refuses this operation.
    # All uses of this key must share this ledger/policy; it is not a global KMS allocator.
    db.execute("INSERT INTO used_nonces VALUES (?,?)",(keyring.active,nonce))
    ciphertext=AESGCM(keyring.keys[keyring.active]).encrypt(nonce,plaintext,associated_data(record))
    return keyring.active,nonce,ciphertext


def decrypt(record,keyring):
    if (record["key_id"] not in keyring.keys
            or not isinstance(record["nonce"],bytes) or len(record["nonce"]) != 12
            or not isinstance(record["ciphertext"],bytes)
            or not 16 <= len(record["ciphertext"]) <= MAX_PLAINTEXT+16):
        raise CannotOpen("export_unavailable")
    try:
        return AESGCM(keyring.keys[record["key_id"]]).decrypt(
            record["nonce"],record["ciphertext"],associated_data(record))
    except InvalidTag as exc:
        raise CannotOpen("export_unavailable") from exc


def authorize_record(db,record,user_id):
    require_member(db,user_id,record["workspace_id"])
    if user_id != record["requested_by"]:
        raise AccessDenied()
    ids=json.loads(record["note_ids"])  # Trusted stored intent, not a browser claim.
    if len(visible_rows(db,user_id=user_id,workspace_id=record["workspace_id"],note_ids=ids,limit=10)) != len(ids):
        raise AccessDenied()


def create_export(database,*,user_id,workspace_id,note_ids,keyring):
    artifact=build_export(database,user_id=user_id,workspace_id=workspace_id,note_ids=note_ids)
    with unit(database,write=True) as db:
        intent={"workspace_id":workspace_id,"requested_by":user_id,"note_ids":json.dumps(artifact.note_ids)}
        authorize_record(db,intent,user_id)  # Current permission again before storing a copy.
        cursor=db.execute("""INSERT INTO encrypted_exports
            (workspace_id,requested_by,note_ids,format_version,generation,key_id,nonce,ciphertext)
            VALUES (?,?,?,1,1,? ,X'',X'')""",
            (workspace_id,user_id,intent["note_ids"],keyring.active))
        record=dict(db.execute("SELECT * FROM encrypted_exports WHERE id=?",(cursor.lastrowid,)).fetchone())
        kid,nonce,ciphertext=encrypt(db,record,artifact.payload,keyring)
        db.execute("UPDATE encrypted_exports SET key_id=?,nonce=?,ciphertext=? WHERE id=?",
                   (kid,nonce,ciphertext,record["id"]))
    return record["id"]


def read_export(database,*,user_id,export_id,keyring):
    if user_id is None:
        raise AccessDenied(403,"access_denied")
    with unit(database) as db:
        row=db.execute("SELECT * FROM encrypted_exports WHERE id=?",(export_id,)).fetchone()
        if row is None:
            raise AccessDenied()
        record=dict(row)
        authorize_record(db,record,user_id)
        return decrypt(record,keyring)


def rotate_export(database,*,export_id,keyring):
    # Privileged internal maintenance, not a user-callable operation or a read grant.
    with unit(database,write=True) as db:
        row=db.execute("SELECT * FROM encrypted_exports WHERE id=?",(export_id,)).fetchone()
        if row is None:
            raise CannotOpen("export_unavailable")
        previous=dict(row)
        plaintext=decrypt(previous,keyring)  # Verify old record BEFORE any replacement.
        current={**previous,"generation":previous["generation"]+1}
        kid,nonce,ciphertext=encrypt(db,current,plaintext,keyring)
        changed=db.execute("""UPDATE encrypted_exports SET key_id=?,nonce=?,ciphertext=?,generation=?
            WHERE id=? AND generation=?""",
            (kid,nonce,ciphertext,current["generation"],export_id,previous["generation"])).rowcount
        if changed != 1:
            raise RuntimeError("export_generation_changed")


def inventory(database):
    # Privileged verifier/nonce inspection, never an HTTP response or log payload.
    with unit(database) as db:
        return {name:[dict(row) for row in db.execute(f"SELECT * FROM {name} ORDER BY 1,2")]
                for name in ("encrypted_exports","used_nonces")}
