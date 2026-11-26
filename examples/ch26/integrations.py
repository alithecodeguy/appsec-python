"""Local integration contracts. No live HTTP adapter, queue or secret store."""
import hashlib
import hmac
import json
import re
import time
from types import MappingProxyType
from urllib.parse import urlencode, urlsplit

from examples.ch23.authorization_service import require_member, seed, unit

ENDPOINTS = MappingProxyType({"reports": "https://reports.partner.example/v1/status"})
MAX_REPLY = 128
MAX_EVENT = 512
WINDOW = 300
FIXTURE_NOW = 1795683600
# Public dummy keys. Real keys come from protected configuration, scoped to a partner.
FIXTURE_KEYS = {"reports": {"old": b"public-old-fixture-key-26", "new": b"public-new-fixture-key-26"}}


class Refused(ValueError):
    pass


def object_json(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise Refused("invalid_json")
            result[key] = value
        return result
    def constant(value):
        raise Refused("invalid_json")
    try:
        result = json.loads(raw.decode("utf-8"), object_pairs_hook=pairs, parse_constant=constant)
    except (ValueError, UnicodeDecodeError, RecursionError) as exc:
        raise Refused("invalid_json") from exc
    if not isinstance(result, dict):
        raise Refused("object_required")
    return result


def initialize(database):
    seed(database)
    with unit(database, write=True) as db:
        db.execute("""CREATE TABLE partner_bindings (
            workspace_id INTEGER NOT NULL REFERENCES workspaces(id), partner_id TEXT NOT NULL,
            account_ref TEXT NOT NULL, status TEXT NOT NULL, refresh_count INTEGER NOT NULL,
            PRIMARY KEY(workspace_id,partner_id), UNIQUE(partner_id,account_ref))""")
        db.execute("""CREATE TABLE webhook_receipts (
            partner_id TEXT NOT NULL, event_id TEXT NOT NULL, body_sha256 TEXT NOT NULL,
            PRIMARY KEY(partner_id,event_id))""")
        db.execute("""CREATE TABLE reports (
            partner_id TEXT NOT NULL, report_ref TEXT NOT NULL,
            workspace_id INTEGER NOT NULL REFERENCES workspaces(id),
            PRIMARY KEY(partner_id,report_ref))""")
        db.executemany("INSERT INTO partner_bindings VALUES (?,'reports',?,'unknown',0)",
                       [(1,"alpha-remote"), (2,"beta-remote")])


def endpoint(partner_id):
    if not isinstance(partner_id,str) or partner_id not in ENDPOINTS:
        raise Refused("unknown_partner")
    url = ENDPOINTS[partner_id]
    parsed = urlsplit(url)
    if (parsed.scheme != "https" or parsed.hostname != "reports.partner.example"
            or parsed.port not in (None,443) or parsed.username is not None
            or parsed.password is not None or parsed.path != "/v1/status"
            or parsed.query or parsed.fragment):
        raise Refused("invalid_registry")
    return url


def refresh_status(database, *, user_id, workspace_id, partner_id, transport, clock=time.monotonic):
    url = endpoint(partner_id)
    with unit(database) as db:
        require_member(db, user_id, workspace_id)
        binding = db.execute("SELECT account_ref FROM partner_bindings WHERE workspace_id=? AND partner_id=?",
                             (workspace_id,partner_id)).fetchone()
        if binding is None:
            raise Refused("missing_binding")
        account_ref = binding["account_ref"]
    target = url + "?" + urlencode({"account_ref": account_ref})
    started = clock()
    # Contract: adapter verifies TLS, refuses redirects, requests identity encoding,
    # applies timeout/body/header limits and controls proxy use. The fake proves none of TLS/DNS.
    with transport.get(target, timeout=2.0, max_bytes=MAX_REPLY) as reply:
        if 300 <= reply.status < 400:
            raise Refused("redirect_refused")
        if reply.status != 200:
            raise Refused("unexpected_status")
        types = [v for k,v in reply.headers if k.lower() == "content-type"]
        encodings = [v for k,v in reply.headers if k.lower() == "content-encoding"]
        if len(types) != 1 or types[0].partition(';')[0].strip().lower() != "application/json":
            raise Refused("unexpected_media_type")
        if encodings not in ([], ["identity"]):
            raise Refused("unsupported_encoding")
        body = reply.read(MAX_REPLY + 1)
        if len(body) > MAX_REPLY:
            raise Refused("reply_too_large")
        if clock() - started >= 3.0:
            raise Refused("deadline_exceeded")
        payload = object_json(body)
        if (set(payload) != {"account_ref","status"} or payload["account_ref"] != account_ref
                or payload["status"] not in ("ok","degraded")):
            raise Refused("invalid_partner_schema")
    # Never hold the application write transaction open during a network operation.
    with unit(database, write=True) as db:
        require_member(db, user_id, workspace_id)
        changed = db.execute("""UPDATE partner_bindings SET status=?, refresh_count=refresh_count+1
            WHERE workspace_id=? AND partner_id=? AND account_ref=?""",
            (payload["status"],workspace_id,partner_id,account_ref)).rowcount
        if changed != 1:
            raise Refused("binding_changed")
    return payload["status"]


def signature(secret, partner_id, timestamp, raw):
    message = b"casebook-webhook-v1\n" + partner_id.encode("ascii") + b"\n" + timestamp.encode("ascii") + b"." + raw
    return hmac.new(secret, message, hashlib.sha256).hexdigest()


def handle_webhook(database, *, partner_id, raw, timestamp, key_id, supplied_signature,
                   keyrings, now):
    if len(raw) > MAX_EVENT:
        raise Refused("event_too_large")
    keys = keyrings.get(partner_id, {})
    if (not isinstance(key_id,str) or key_id not in keys or not isinstance(timestamp,str)
            or re.fullmatch(r"0|[1-9][0-9]{0,11}",timestamp) is None
            or abs(now - int(timestamp)) > WINDOW
            or not isinstance(supplied_signature,str)
            or re.fullmatch(r"[0-9a-f]{64}",supplied_signature) is None):
        raise Refused("invalid_webhook")
    expected = signature(keys[key_id], partner_id, timestamp, raw)
    if not hmac.compare_digest(expected, supplied_signature):
        raise Refused("invalid_webhook")
    payload = object_json(raw)  # Verify exact bytes BEFORE deserialization.
    if (set(payload) != {"id","type","account_ref","report_ref"}
            or payload["type"] != "report.ready"
            or any(not isinstance(payload[field],str) or re.fullmatch(r"[A-Za-z0-9_-]{1,64}",payload[field]) is None
                   for field in ("id","account_ref","report_ref"))):
        raise Refused("invalid_event_schema")
    digest = hashlib.sha256(raw).hexdigest()
    with unit(database, write=True) as db:
        binding = db.execute("SELECT workspace_id FROM partner_bindings WHERE partner_id=? AND account_ref=?",
                             (partner_id,payload["account_ref"])).fetchone()
        if binding is None:
            raise Refused("unknown_binding")
        prior = db.execute("SELECT body_sha256 FROM webhook_receipts WHERE partner_id=? AND event_id=?",
                           (partner_id,payload["id"])).fetchone()
        if prior is not None:
            if prior["body_sha256"] != digest:
                raise Refused("event_id_conflict")
            return 200, {"received": True}
        report = db.execute("SELECT workspace_id FROM reports WHERE partner_id=? AND report_ref=?",
                            (partner_id,payload["report_ref"])).fetchone()
        if report is not None and report["workspace_id"] != binding["workspace_id"]:
            raise Refused("report_binding_conflict")
        if report is None:
            db.execute("INSERT INTO reports VALUES (?,?,?)",
                       (partner_id,payload["report_ref"],binding["workspace_id"]))
        db.execute("INSERT INTO webhook_receipts VALUES (?,?,?)",(partner_id,payload["id"],digest))
    return 200, {"received": True}


def inventory(database):
    # Privileged local evidence. Not a private-report retrieval endpoint.
    with unit(database) as db:
        return {table:[dict(row) for row in db.execute(f"SELECT * FROM {table} ORDER BY 1,2")]
                for table in ("partner_bindings","webhook_receipts","reports")}
