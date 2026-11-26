import json
from pathlib import Path
from tempfile import TemporaryDirectory

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from examples.ch23.authorization_service import AccessDenied, revoke_member
from examples.ch27.export_crypto import Keyring
from examples.ch28.export_queue import download, enqueue, initialize, inventory, process_request
from examples.ch28.two_workers import coordinated_workers

NOW = 1795683600  # Controlled service clock, not supplied by an API caller.

with TemporaryDirectory(prefix="casebook-queue-") as folder:
    database = Path(folder)/"jobs.sqlite3"
    initialize(database)
    keys = Keyring({"export-demo":AESGCM.generate_key(bit_length=256)}, "export-demo")
    request = enqueue(database, user_id=1, workspace_id=1, note_ids=[101], client_key="mina-001", now=NOW)
    outcomes = coordinated_workers(database, request_id=request, keyring=keys, now=NOW)
    print("both observed no result:", all(missing for missing, _ in outcomes))
    print("worker outcomes:", sorted(result for _, result in outcomes))
    stored = inventory(database)
    print("request state:", stored["export_requests"][0]["state"])
    print("slots, artifacts, nonces:", *(len(stored[name]) for name in ("export_slots","encrypted_exports","used_nonces")))
    repeat = enqueue(database, user_id=1, workspace_id=1, note_ids=[101], client_key="mina-001", now=NOW+1)
    print("same request ID on retry:", repeat == request)
    print("redelivery:", process_request(database, request_id=request, keyring=keys, now=NOW+1))
    print("redelivery leaves rows unchanged:", inventory(database) == stored)
    document = json.loads(download(database, user_id=1, request_id=request, keyring=keys, now=NOW+1))
    print("Mina export workspace:", document["workspace_id"])
    try:
        download(database, user_id=2, request_id=request, keyring=keys, now=NOW+1)
    except AccessDenied:
        print("Ravi Alpha download: denied")
    revoke_member(database, actor_id=3, workspace_id=1, target_user_id=1)
    try:
        download(database, user_id=1, request_id=request, keyring=keys, now=NOW+2)
    except AccessDenied:
        print("Mina after revocation: denied")
    print("release refusal leaves job/artifact rows unchanged:", inventory(database) == stored)
