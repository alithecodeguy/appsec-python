import asyncio
import json
from pathlib import Path
import sqlite3
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from examples.ch23.authorization_service import AccessDenied, build_export, revoke_member, unit
from examples.ch27.export_crypto import Keyring, MAX_PLAINTEXT
from examples.ch28.cancellation import cancellation_case
from examples.ch28.export_queue import (
    IntentConflict, QueueFull, download, enqueue, initialize, inventory,
    process_request, run_with_retry,
)
from examples.ch28.two_workers import coordinated_workers
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier

NOW = 1795683600


class QueueTests(unittest.TestCase):
    def setUp(self):
        self.folder = TemporaryDirectory(prefix="casebook-queue-test-")
        self.addCleanup(self.folder.cleanup)
        self.db = Path(self.folder.name)/"jobs.sqlite3"
        initialize(self.db)
        self.keys = Keyring({"export-test":AESGCM.generate_key(bit_length=256)}, "export-test")

    def submit(self, **changes):
        values = dict(user_id=1, workspace_id=1, note_ids=[101], client_key="mina-001", now=NOW)
        return enqueue(self.db, **(values | changes))

    def process(self, request_id, **changes):
        return process_request(self.db, **(dict(request_id=request_id, keyring=self.keys, now=NOW) | changes))

    def read(self, request_id, **changes):
        return download(self.db, **(dict(user_id=1, request_id=request_id, keyring=self.keys, now=NOW) | changes))

    def test_two_workers_one_committed_export_and_stable_redelivery(self):
        request = self.submit()
        results = coordinated_workers(self.db, request_id=request, keyring=self.keys, now=NOW)
        self.assertEqual([missing for missing, _ in results], [True, True])
        self.assertEqual(sorted(outcome for _, outcome in results), ["created", "duplicate"])
        saved = inventory(self.db)
        self.assertEqual(saved["export_requests"][0]["state"], "ready")
        self.assertEqual([len(saved[name]) for name in ("export_slots","encrypted_exports","used_nonces")], [1,1,1])
        self.assertEqual(self.submit(now=NOW+1), request)
        self.assertEqual(self.process(request, now=NOW+1), "duplicate")
        self.assertEqual(inventory(self.db), saved)
        self.assertEqual(json.loads(self.read(request))["workspace_id"], 1)

    def test_constraint_negative_control_same_schedule_allows_two_claims(self):
        # Deliberately broken isolated claim fixture; never run the export pipeline on it.
        with unit(self.db, write=True) as db:
            db.execute("DROP TABLE export_slots")
            db.execute("""CREATE TABLE export_slots (
                request_id INTEGER NOT NULL REFERENCES export_requests(id),
                export_id INTEGER UNIQUE REFERENCES encrypted_exports(id))""")
        request = self.submit()
        gate = Barrier(2, timeout=5)
        def claim_only():
            with unit(self.db) as db:
                missing = db.execute("SELECT 1 FROM export_slots WHERE request_id=?", (request,)).fetchone() is None
            gate.wait()
            with unit(self.db, write=True) as db:
                db.execute("INSERT INTO export_slots (request_id) VALUES (?)", (request,))
            return missing
        with ThreadPoolExecutor(max_workers=2) as pool:
            futures = [pool.submit(claim_only) for _ in range(2)]
            self.assertEqual([future.result(timeout=10) for future in futures], [True,True])
        self.assertEqual(len(inventory(self.db)["export_slots"]), 2)

    def test_revoked_while_queued_creates_no_artifact(self):
        request = self.submit()
        revoke_member(self.db, actor_id=3, workspace_id=1, target_user_id=1)
        self.assertEqual(self.process(request), "denied")
        saved = inventory(self.db)
        self.assertEqual(saved["export_requests"][0]["error"], "access_denied")
        for name in ("export_slots","encrypted_exports","used_nonces"):
            self.assertEqual(saved[name], [])
        self.assertEqual(self.process(request), "denied")
        self.assertEqual(inventory(self.db), saved)
        with self.assertRaises(AccessDenied): self.read(request)

    def test_release_rechecks_membership_requester_and_expiry(self):
        request = self.submit()
        self.process(request)
        self.assertEqual(json.loads(self.read(request, now=NOW+59))["notes"][0]["id"], 101)
        saved = inventory(self.db)
        for user in (None,2,3):
            with self.assertRaises(AccessDenied): self.read(request, user_id=user)
        with self.assertRaises(AccessDenied): self.read(request, now=NOW+60)
        revoke_member(self.db, actor_id=3, workspace_id=1, target_user_id=1)
        with self.assertRaises(AccessDenied): self.read(request, now=NOW+1)
        self.assertEqual(inventory(self.db), saved)

    def test_expired_queued_request_is_terminal_without_output(self):
        request = self.submit()
        self.assertEqual(self.process(request, now=NOW+60), "expired")
        saved = inventory(self.db)
        self.assertEqual(saved["export_requests"][0]["state"], "expired")
        for name in ("export_slots","encrypted_exports","used_nonces"):
            self.assertEqual(saved[name], [])
        self.assertEqual(self.process(request, now=NOW+61), "expired")
        self.assertEqual(inventory(self.db), saved)

    def test_failed_ready_write_rolls_back_claim_ciphertext_and_nonce_then_retry_succeeds(self):
        request = self.submit()
        with unit(self.db, write=True) as db:
            db.execute("""CREATE TRIGGER fail_ready BEFORE UPDATE OF state ON export_requests
                WHEN NEW.state='ready' BEGIN SELECT RAISE(ABORT,'synthetic commit-unit failure'); END""")
        before = inventory(self.db)
        with self.assertRaises(sqlite3.IntegrityError): self.process(request)
        self.assertEqual(inventory(self.db), before)
        with unit(self.db, write=True) as db: db.execute("DROP TRIGGER fail_ready")
        self.assertEqual(self.process(request), "created")
        self.assertEqual(self.process(request), "duplicate")
        self.assertEqual(len(inventory(self.db)["encrypted_exports"]), 1)

    def test_admission_limits_scope_and_request_key_conflict(self):
        request = self.submit()
        before = inventory(self.db)
        with self.assertRaises(QueueFull): self.submit(client_key="mina-002")
        with self.assertRaises(AccessDenied): self.submit(user_id=2)
        with self.assertRaises(AccessDenied): self.submit(user_id=None)
        self.assertEqual(inventory(self.db), before)
        self.assertEqual(self.submit(), request)  # Retries do not consume another slot.
        with patch("examples.ch28.export_queue.MAX_PENDING", 1):
            with self.assertRaises(QueueFull):
                self.submit(user_id=2, workspace_id=2, note_ids=[202], client_key="ravi-001")
        beta = self.submit(user_id=2, workspace_id=2, note_ids=[202], client_key="ravi-001")
        self.assertNotEqual(beta, request)
        with unit(self.db, write=True) as db:
            db.execute("""INSERT INTO notes SELECT 102,workspace_id,owner_id,title,body,state,version,updated_by
                FROM notes WHERE id=101""")
        before = inventory(self.db)
        with self.assertRaises(IntentConflict): self.submit(note_ids=[101,102])
        self.assertEqual(inventory(self.db), before)

    def test_exact_byte_limit_and_one_byte_over(self):
        for extra in (0,1):
            with self.subTest(extra=extra):
                path = Path(self.folder.name)/f"limit-{extra}.sqlite3"
                initialize(path)
                with unit(path, write=True) as db:
                    db.execute("UPDATE notes SET title=?,body='' WHERE id=101", ("یادداشت آلفا",))
                base = len(build_export(path, user_id=1, workspace_id=1, note_ids=[101]).payload)
                with unit(path, write=True) as db:
                    db.execute("UPDATE notes SET body=? WHERE id=101", ("x"*(MAX_PLAINTEXT-base+extra),))
                request = enqueue(path, user_id=1, workspace_id=1, note_ids=[101], client_key="boundary", now=NOW)
                outcome = process_request(path, request_id=request, keyring=self.keys, now=NOW)
                saved = inventory(path)
                if extra == 0:
                    self.assertEqual(outcome, "created")
                    self.assertEqual(len(download(path, user_id=1, request_id=request, keyring=self.keys, now=NOW)), 4096)
                else:
                    self.assertEqual(outcome, "failed")
                    self.assertEqual(saved["export_requests"][0]["error"], "export_too_large")
                    for name in ("export_slots","encrypted_exports","used_nonces"):
                        self.assertEqual(saved[name], [])

    def test_bounded_busy_retry_does_not_retry_other_failures(self):
        pauses, calls = [], []
        def busy():
            calls.append(1)
            exc = sqlite3.OperationalError("synthetic busy")
            exc.sqlite_errorcode = sqlite3.SQLITE_BUSY
            raise exc
        with self.assertRaises(sqlite3.OperationalError): run_with_retry(busy, pause=pauses.append)
        self.assertEqual((len(calls), pauses), (3,[0.01,0.02]))
        def other():
            exc = sqlite3.OperationalError("synthetic nonbusy")
            exc.sqlite_errorcode = sqlite3.SQLITE_ERROR
            raise exc
        with self.assertRaises(sqlite3.OperationalError): run_with_retry(other, pause=pauses.append)
        self.assertEqual(pauses, [0.01,0.02])
        outcomes = iter([busy, lambda:"created"])
        self.assertEqual(run_with_retry(lambda:next(outcomes)(), pause=lambda _:None), "created")

    def test_cancelled_fixture_cleans_files_and_queue_accounting(self):
        self.assertEqual(asyncio.run(cancellation_case()), {
            "backpressure":True, "partial_exists":True, "cancelled":True,
            "remaining_files":0, "queued_ids":0,
        })


if __name__ == "__main__":
    unittest.main()
