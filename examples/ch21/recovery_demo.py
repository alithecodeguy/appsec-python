from pathlib import Path
from tempfile import TemporaryDirectory

from recovery_lab import complete_reset, fresh_clock, request_reset, seed, snapshot


with TemporaryDirectory(prefix="casebook-recovery-") as folder:
    path = Path(folder) / "recovery.sqlite3"
    seed(path)
    clock = fresh_clock()
    outbox = []
    known = request_reset(path, "mina@example.test", clock, outbox)
    token = outbox[-1].token
    unknown = request_reset(path, "missing@example.test", clock, outbox)
    print("same public response:", known == unknown)
    print("public status:", known[0])
    print("private deliveries:", len(outbox))
    before = snapshot(path)
    print("before:", before["accounts"][0]["credential_revision"],
          before["accounts"][0]["session_epoch"])
    clock.advance(899)
    print("before expiry:", complete_reset(path, token, "opaque-fixture-password-v2", clock)[0])
    accepted = snapshot(path)
    account = accepted["accounts"][0]
    print("after:", account["credential_revision"], account["session_epoch"])
    print("token consumed:", accepted["resets"][0]["used_at"] == clock.now())
    print("replay:", complete_reset(path, token, "must-not-be-stored", clock))
    print("unchanged after replay:", snapshot(path) == accepted)
    request_reset(path, "mina@example.test", clock, outbox)
    expires = outbox[-1].token
    clock.advance(900)
    boundary = snapshot(path)
    print("exact expiry:", complete_reset(path, expires, "must-not-be-stored", clock))
    print("unchanged at expiry:", snapshot(path) == boundary)
