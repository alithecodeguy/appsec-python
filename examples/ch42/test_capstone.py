import asyncio
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import sqlite3
from tempfile import TemporaryDirectory
from threading import Event
import unittest

from examples.ch23.authorization_service import AccessDenied, build_export, revoke_member, unit
from examples.ch27.export_crypto import CannotOpen, MAX_PLAINTEXT
from examples.ch28.cancellation import cancellation_case
from examples.ch42.capstone import (
    Cancelled, Clock, GRACE, RETENTION, Problem, access_end, cleanup, collect, decode_message,
    expire, initialize, purge, request_export, snapshot, status, work,
)
from examples.ch42.fixtures import dummy_keyrings
from examples.ch42.workers import two_workers


class CapstoneTests(unittest.TestCase):
    def setUp(self):
        self.folder = TemporaryDirectory(prefix="casebook-capstone-test-")
        self.addCleanup(self.folder.cleanup)
        self.db = Path(self.folder.name)/"capstone.sqlite3"
        initialize(self.db)
        self.clock, self.keys = Clock(), dummy_keyrings()

    def request(self, **changes):
        values = dict(user_id=1,workspace_id=1,body={"note_ids":[101]},client_key="mina-001",clock=self.clock)
        return request_export(self.db, **(values | changes))

    def run_job(self, job_id, **changes):
        values = dict(workspace_id=1,job_id=job_id,keyrings=self.keys,clock=self.clock)
        return work(self.db, **(values | changes))

    def read(self, job_id, **changes):
        values = dict(user_id=1,workspace_id=1,job_id=job_id,keyrings=self.keys,clock=self.clock)
        return collect(self.db, **(values | changes))

    def end(self, job_id, **changes):
        return expire(self.db, **(dict(user_id=1,workspace_id=1,job_id=job_id,clock=self.clock) | changes))

    def audit_trigger(self, outcome):
        with unit(self.db,write=True) as db:
            db.execute(f"""CREATE TRIGGER fail_event BEFORE INSERT ON export_events
                WHEN NEW.outcome='{outcome}' BEGIN SELECT RAISE(ABORT,'synthetic audit failure'); END""")

    def add_notes(self):
        with unit(self.db,write=True) as db:
            for note_id in range(102,112):
                db.execute("""INSERT INTO notes SELECT ?,workspace_id,owner_id,title,body,state,version,updated_by
                    FROM notes WHERE id=101""", (note_id,))

    def test_A41_01_two_workspace_payloads_and_minimal_status(self):
        with unit(self.db) as db: original = [dict(r) for r in db.execute("SELECT * FROM notes ORDER BY id")]
        alpha = self.request()["job_id"]
        beta = self.request(user_id=2,workspace_id=2,body={"note_ids":[202]},client_key="ravi-001")["job_id"]
        self.assertEqual(self.run_job(alpha),"created")
        self.assertEqual(self.run_job(beta,workspace_id=2),"created")
        a,b = json.loads(self.read(alpha)),json.loads(self.read(beta,user_id=2,workspace_id=2))
        self.assertEqual((a["workspace_id"],b["workspace_id"]),(1,2))
        self.assertEqual(set(a),{"workspace_id","notes"})
        self.assertEqual(set(a["notes"][0]),{"id","workspace_id","title","body"})
        self.assertEqual((a["notes"][0]["body"],b["notes"][0]["body"]),("Alpha private fixture","Beta private fixture"))
        minimal = status(self.db,user_id=1,workspace_id=1,job_id=alpha,clock=self.clock)
        self.assertEqual(set(minimal),{"job_id","workspace_id","state","expires_at"})
        with unit(self.db) as db: self.assertEqual([dict(r) for r in db.execute("SELECT * FROM notes ORDER BY id")],original)
        stored = snapshot(self.db)
        self.assertNotEqual(stored["encrypted_exports"][0]["key_id"],stored["encrypted_exports"][1]["key_id"])

    def test_A41_02_anonymous_cross_workspace_and_route_substitution(self):
        alpha = self.request()["job_id"]
        self.run_job(alpha)
        before = snapshot(self.db)
        for user,workspace in ((None,1),(2,1),(1,2),(3,2)):
            with self.subTest(user=user,workspace=workspace):
                with self.assertRaises(AccessDenied): self.request(user_id=user,workspace_id=workspace)
                with self.assertRaises(AccessDenied): self.read(alpha,user_id=user,workspace_id=workspace)
                with self.assertRaises(AccessDenied): self.end(alpha,user_id=user,workspace_id=workspace)
        self.assertEqual(snapshot(self.db),before)

    def test_A41_03_validation_normalization_replay_and_conflict(self):
        self.add_notes()
        for body in ({"note_ids":[101,202]}, {"note_ids":[101],"requested_by":2},
                     {"note_ids":[True]}, {"note_ids":[]}, {"note_ids":[101,101]}, {"note_ids":None}):
            before = snapshot(self.db)
            with self.assertRaises((AccessDenied,Problem)): self.request(body=body)
            self.assertEqual(snapshot(self.db),before)
        receipt = self.request(body={"note_ids":[102,101]})
        self.clock.value += 1
        saved = snapshot(self.db)
        self.assertEqual(self.request(body={"note_ids":[101,102]}),receipt)
        self.assertEqual(snapshot(self.db),saved)
        with self.assertRaises(Problem) as error: self.request(body={"note_ids":[101]})
        self.assertEqual(error.exception.status,409)
        self.assertEqual(snapshot(self.db),saved)

    def test_A41_04_revoked_while_queued_then_restored_cannot_reopen(self):
        job = self.request()["job_id"]
        revoke_member(self.db,actor_id=3,workspace_id=1,target_user_id=1)
        self.assertEqual(self.run_job(job),"denied")
        saved = snapshot(self.db)
        self.assertEqual((saved["jobs"][0]["reserved"],len(saved["encrypted_exports"])),(0,0))
        with unit(self.db,write=True) as db: db.execute("UPDATE memberships SET active=1 WHERE user_id=1")
        self.assertEqual(self.run_job(job),"denied")
        self.assertEqual(snapshot(self.db),saved)
        with self.assertRaises(Problem) as error: self.read(job)
        self.assertEqual(error.exception.status,410)

    def test_A41_05_ready_revocation_deactivation_and_inaccessible_selection(self):
        job = self.request()["job_id"]
        self.run_job(job)
        self.read(job)  # An earlier authorized collection is not a cache exemption.
        saved = snapshot(self.db)
        for sql,undo in (("UPDATE memberships SET active=0 WHERE user_id=1","UPDATE memberships SET active=1 WHERE user_id=1"),
                         ("UPDATE users SET active=0 WHERE id=1","UPDATE users SET active=1 WHERE id=1"),
                         ("UPDATE notes SET workspace_id=2 WHERE id=101","UPDATE notes SET workspace_id=1 WHERE id=101")):
            with unit(self.db,write=True) as db: db.execute(sql)
            with self.assertRaises(AccessDenied): self.read(job)
            self.assertEqual(snapshot(self.db),saved)
            with unit(self.db,write=True) as db: db.execute(undo)

    def test_A41_06_07_exact_manager_and_member_expiry_matrix(self):
        a = self.request()["job_id"]
        self.run_job(a)
        lee = self.request(user_id=3,client_key="lee-001")["job_id"]
        self.run_job(lee)
        beta = self.request(user_id=2,workspace_id=2,body={"note_ids":[202]},client_key="ravi")["job_id"]
        self.run_job(beta,workspace_id=2)
        saved = snapshot(self.db)
        for operation in (lambda:self.read(a,user_id=3),lambda:self.end(lee),lambda:self.end(beta,user_id=3,workspace_id=2)):
            with self.assertRaises(AccessDenied): operation()
        self.assertEqual(snapshot(self.db),saved)
        self.assertEqual(self.end(a,user_id=3),"expired")
        once = snapshot(self.db)
        self.clock.value += 10
        self.end(a,user_id=3)
        self.assertEqual(snapshot(self.db),once)
        self.end(lee,user_id=3)
        self.end(beta,user_id=2,workspace_id=2)
        self.assertEqual([r["state"] for r in snapshot(self.db)["jobs"]],["expired"]*3)

    def test_A41_08_exact_expiry_no_cleanup_required_for_denial(self):
        job = self.request()["job_id"]
        self.run_job(job)
        original = snapshot(self.db)["jobs"][0]
        self.clock.value = original["expires_at"]-1
        self.assertTrue(self.read(job))
        saved = snapshot(self.db)
        self.clock.value += 1
        with self.assertRaises(Problem) as error: self.read(job)
        self.assertEqual(error.exception.status,410)
        self.assertEqual(snapshot(self.db),saved)
        self.assertEqual(status(self.db,user_id=1,workspace_id=1,job_id=job,clock=self.clock)["state"],"expired")
        self.assertEqual(snapshot(self.db)["jobs"][0]["state"],"ready")

    def test_A41_09_two_workers_one_result_and_stable_receipt(self):
        receipt = self.request()
        job = receipt["job_id"]
        results = two_workers(self.db,workspace_id=1,job_id=job,keyrings=self.keys,clock=self.clock)
        self.assertEqual([missing for missing,_ in results],[True,True])
        self.assertEqual(sorted(result for _,result in results),["created","duplicate"])
        saved = snapshot(self.db)
        self.assertEqual([len(saved[n]) for n in ("result_slots","encrypted_exports","used_nonces")],[1,1,1])
        self.assertEqual(self.request(),receipt)
        self.assertEqual(self.run_job(job),"duplicate")
        self.assertEqual(snapshot(self.db),saved)
        with unit(self.db,write=True) as db:
            with self.assertRaises(sqlite3.IntegrityError): db.execute("INSERT INTO result_slots(job_id) VALUES (?)",(job,))

    def test_A41_10_ready_audit_failure_rolls_back_and_retry_creates_once(self):
        job = self.request()["job_id"]
        self.audit_trigger("ready")
        before = snapshot(self.db)
        with self.assertRaises(sqlite3.IntegrityError): self.run_job(job)
        self.assertEqual(snapshot(self.db),before)
        with unit(self.db,write=True) as db: db.execute("DROP TRIGGER fail_event")
        self.assertEqual(self.run_job(job),"created")
        self.assertEqual(self.run_job(job),"duplicate")

    def test_A41_10_cooperative_stop_rolls_back_prepared_ciphertext(self):
        job = self.request()["job_id"]
        stop = Event()
        before = snapshot(self.db)
        with self.assertRaises(Cancelled): self.run_job(job,stop=stop,checkpoint=stop.set)
        self.assertEqual(snapshot(self.db),before)
        self.assertEqual(before["jobs"][0]["reserved"],1)  # Durable intent still pending, not acknowledged complete.
        self.assertEqual(self.run_job(job),"created")
        self.assertEqual(asyncio.run(cancellation_case())["remaining_files"],0)

    def test_A41_10_deletion_failure_keeps_capacity_and_records_deadline_breach(self):
        job = self.request()["job_id"]
        self.run_job(job)
        self.clock.value += 20
        self.end(job)
        with unit(self.db,write=True) as db:
            db.execute("""CREATE TRIGGER fail_delete BEFORE DELETE ON encrypted_exports
                BEGIN SELECT RAISE(ABORT,'synthetic storage failure'); END""")
        self.clock.value += GRACE+1
        self.assertEqual(cleanup(self.db,job_id=job,clock=self.clock),"retry")
        failed = snapshot(self.db)
        self.assertEqual((failed["jobs"][0]["reserved"],failed["jobs"][0]["deleted_at"],failed["jobs"][0]["breached"]),(1,None,1))
        self.assertEqual(len(failed["encrypted_exports"]),1)
        with self.assertRaises(Problem): self.read(job)
        end = access_end(failed["jobs"][0])
        with unit(self.db,write=True) as db: db.execute("DROP TRIGGER fail_delete")
        self.assertEqual(cleanup(self.db,job_id=job,clock=self.clock),"deleted")
        saved = snapshot(self.db)
        self.assertEqual((saved["jobs"][0]["reserved"],saved["jobs"][0]["breached"]),(0,1))
        self.assertEqual(access_end(saved["jobs"][0]),end)
        self.assertEqual([len(saved[n]) for n in ("result_slots","encrypted_exports","used_nonces")],[0,0,1])
        self.clock.value += 5
        cleanup(self.db,job_id=job,clock=self.clock)
        self.assertEqual(snapshot(self.db),saved)

    def test_A41_11_expiry_first_stops_late_publication(self):
        job = self.request()["job_id"]
        arrived,release = Event(),Event()
        def wait(_):
            arrived.set()
            if not release.wait(3): raise TimeoutError("test coordination")
        with ThreadPoolExecutor(max_workers=1) as pool:
            future = pool.submit(self.run_job,job,after_probe=wait)
            try:
                self.assertTrue(arrived.wait(3))
                self.end(job,user_id=3)
            finally: release.set()
            self.assertEqual(future.result(timeout=5),"expired")
        saved = snapshot(self.db)
        self.assertEqual((saved["jobs"][0]["state"],saved["jobs"][0]["reserved"]),("expired",0))
        self.assertEqual(saved["encrypted_exports"],[])

    def test_A41_11_publication_first_then_expiry_cannot_reopen(self):
        job = self.request()["job_id"]
        prepared,release,attempting = Event(),Event(),Event()
        def checkpoint():
            prepared.set()
            if not release.wait(3): raise TimeoutError("test coordination")
        def expire_other():
            attempting.set()
            return self.end(job,user_id=3)
        with ThreadPoolExecutor(max_workers=2) as pool:
            built = pool.submit(self.run_job,job,checkpoint=checkpoint)
            try:
                self.assertTrue(prepared.wait(3))
                ended = pool.submit(expire_other)
                self.assertTrue(attempting.wait(3))
            finally: release.set()
            self.assertEqual(built.result(timeout=5),"created")
            self.assertEqual(ended.result(timeout=5),"expired")
        self.assertEqual(self.run_job(job),"expired")
        with self.assertRaises(Problem): self.read(job)
        self.assertEqual((snapshot(self.db)["jobs"][0]["reserved"],len(snapshot(self.db)["encrypted_exports"])),(1,1))

    def test_A41_11_deadline_during_preparation_discards_new_ciphertext(self):
        job = self.request()["job_id"]
        self.assertEqual(self.run_job(job,checkpoint=lambda:setattr(self.clock,"value",self.clock.value+60)),"expired")
        saved = snapshot(self.db)
        self.assertEqual(saved["jobs"][0]["reserved"],0)
        for name in ("result_slots","encrypted_exports","used_nonces"): self.assertEqual(saved[name],[])

    def test_A41_12_message_shape_partition_and_terminal_replay(self):
        job = self.request()["job_id"]
        self.assertEqual(decode_message(json.dumps({"job_id":job}).encode()),job)
        for raw in (b'{"job_id":true}',b'{"job_id":1,"workspace_id":2}',b'{"job_id":1,"job_id":2}',b'x'*129):
            with self.assertRaises(Problem): decode_message(raw)
        before = snapshot(self.db)
        with self.assertRaises(Problem): self.run_job(job,workspace_id=2)
        self.assertEqual(snapshot(self.db),before)
        self.end(job)
        saved = snapshot(self.db)
        self.assertEqual(self.run_job(job),"expired")
        self.assertEqual(snapshot(self.db),saved)

    def test_A41_13_selection_pending_and_retained_reservations(self):
        self.add_notes()
        before = snapshot(self.db)
        with self.assertRaises(Problem): self.request(body={"note_ids":list(range(101,112))})
        self.assertEqual(snapshot(self.db),before)
        first = self.request(body={"note_ids":list(range(101,111))})["job_id"]
        with self.assertRaises(Problem) as error: self.request(client_key="pending")
        self.assertEqual(error.exception.status,429)
        self.run_job(first)
        second = self.request(client_key="second")["job_id"]
        self.run_job(second)
        before = snapshot(self.db)
        with self.assertRaises(Problem) as error: self.request(client_key="third")
        self.assertEqual(error.exception.status,429)
        self.assertEqual(snapshot(self.db),before)
        self.end(first)
        with self.assertRaises(Problem): self.request(client_key="third")  # Still retained.
        cleanup(self.db,job_id=first,clock=self.clock)
        self.assertIsInstance(self.request(client_key="third")["job_id"],int)

    def test_A41_13_exact_utf8_byte_boundary_and_one_over(self):
        for extra in (0,1):
            with self.subTest(extra=extra):
                path = Path(self.folder.name)/f"bytes-{extra}.sqlite3"
                initialize(path)
                with unit(path,write=True) as db: db.execute("UPDATE notes SET title=?,body='' WHERE id=101",("یادداشت آلفا",))
                base = len(build_export(path,user_id=1,workspace_id=1,note_ids=[101]).payload)
                with unit(path,write=True) as db: db.execute("UPDATE notes SET body=? WHERE id=101",("x"*(MAX_PLAINTEXT-base+extra),))
                job = request_export(path,user_id=1,workspace_id=1,body={"note_ids":[101]},client_key="bytes",clock=self.clock)["job_id"]
                result = work(path,workspace_id=1,job_id=job,keyrings=self.keys,clock=self.clock)
                saved = snapshot(path)
                if extra == 0:
                    self.assertEqual(result,"created")
                    self.assertEqual(len(collect(path,user_id=1,workspace_id=1,job_id=job,keyrings=self.keys,clock=self.clock)),4096)
                else:
                    self.assertEqual(result,"failed")
                    self.assertEqual(saved["jobs"][0]["reserved"],0)
                    for name in ("result_slots","encrypted_exports","used_nonces"): self.assertEqual(saved[name],[])

    def test_A41_14_collect_audit_and_cipher_integrity_failures_release_nothing(self):
        job = self.request()["job_id"]
        self.run_job(job)
        self.audit_trigger("collect_authorized")
        before = snapshot(self.db)
        with self.assertRaises(sqlite3.IntegrityError): self.read(job)
        with self.assertRaises(CannotOpen): self.read(job,keyrings={1:self.keys[2]})
        self.assertEqual(snapshot(self.db),before)
        with unit(self.db,write=True) as db:
            db.execute("DROP TRIGGER fail_event")
            cipher = before["encrypted_exports"][0]["ciphertext"]
            db.execute("UPDATE encrypted_exports SET ciphertext=?",(bytes([cipher[0]^1])+cipher[1:],))
        corrupted = snapshot(self.db)
        with self.assertRaises(CannotOpen): self.read(job)
        self.assertEqual(snapshot(self.db),corrupted)

    def test_A41_14_accept_expire_delete_event_failures_are_not_success(self):
        self.audit_trigger("accepted")
        before = snapshot(self.db)
        with self.assertRaises(sqlite3.IntegrityError): self.request()
        self.assertEqual(snapshot(self.db),before)
        with unit(self.db,write=True) as db: db.execute("DROP TRIGGER fail_event")
        job = self.request()["job_id"]
        self.run_job(job)
        self.audit_trigger("expired")
        before = snapshot(self.db)
        with self.assertRaises(sqlite3.IntegrityError): self.end(job)
        self.assertEqual(snapshot(self.db),before)
        with unit(self.db,write=True) as db: db.execute("DROP TRIGGER fail_event")
        self.end(job)
        self.audit_trigger("deleted")
        self.assertEqual(cleanup(self.db,job_id=job,clock=self.clock),"retry")
        self.assertIsNone(snapshot(self.db)["jobs"][0]["deleted_at"])
        self.assertEqual(len(snapshot(self.db)["encrypted_exports"]),1)

    def test_A41_15_purge_exact_retention_preserves_nonce_history_and_unique_ids(self):
        job = self.request()["job_id"]
        self.run_job(job)
        self.end(job)
        cleanup(self.db,job_id=job,clock=self.clock)
        deadline = snapshot(self.db)["jobs"][0]["retain_until"]
        self.clock.value = deadline-1
        self.assertFalse(purge(self.db,job_id=job,clock=self.clock))
        self.clock.value += 1
        self.assertTrue(purge(self.db,job_id=job,clock=self.clock))
        saved = snapshot(self.db)
        self.assertEqual([len(saved[n]) for n in ("jobs","result_slots","encrypted_exports","export_events","used_nonces")],[0,0,0,0,1])
        with self.assertRaises(Problem): self.run_job(job)
        self.assertGreater(self.request()["job_id"],job)


if __name__ == "__main__":
    unittest.main()
