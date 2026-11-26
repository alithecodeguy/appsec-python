from pathlib import Path
from tempfile import TemporaryDirectory
import sqlite3
import unittest

from contract_store import (
    ContractError, create_note, parse_object, request_export, seed, snapshot, update_note,
)


class ContractTests(unittest.TestCase):
    def setUp(self):
        self.folder = TemporaryDirectory(prefix="casebook-contract-test-")
        self.addCleanup(self.folder.cleanup)
        self.path = Path(self.folder.name) / "contract.sqlite3"
        seed(self.path)

    def patch(self, payload, actor=1, workspace=1, note=101):
        return update_note(self.path, actor_id=actor, workspace_id=workspace,
                           note_id=note, payload=payload)

    def export(self, payload, actor=1, workspace=1, key="export-001"):
        return request_export(self.path, actor_id=actor, workspace_id=workspace,
                              key=key, payload=payload)

    def assert_refused(self, status, code, operation):
        before = snapshot(self.path)
        with self.assertRaises(ContractError) as caught:
            operation()
        self.assertEqual((caught.exception.status, caught.exception.code), (status, code))
        self.assertEqual(snapshot(self.path), before)

    def test_json_boundary(self):
        self.assertEqual(parse_object('{"title":"برنامه"}'.encode(), "application/json"),
                         {"title": "برنامه"})
        for body, media, status, code in (
            (b"{}", "text/plain", 415, "unsupported_media_type"),
            (b" " * 4097, "application/json", 413, "body_too_large"),
            (b'{"title":"A","title":"B"}', "application/json", 400, "invalid_json"),
            (b'{"x":NaN}', "application/json", 400, "invalid_json"),
            (b"\xff", "application/json", 400, "invalid_json"),
            (b"[", "application/json", 400, "invalid_json"),
            (b"[]", "application/json", 400, "object_required"),
        ):
            with self.subTest(body=body[:30]):
                self.assert_refused(status, code, lambda: parse_object(body, media))

    def test_create_derives_owner_and_update_preserves_it(self):
        status, created = create_note(self.path, actor_id=1, workspace_id=1,
                                      payload={"title": "برنامه انتشار"})
        self.assertEqual((status, created["owner_id"]), (201, 1))
        status, edited = self.patch({"title": "Edited by Lee", "expected_version": 1},
                                    actor=3, note=created["id"])
        self.assertEqual((status, edited["owner_id"], edited["updated_by"]), (200, 1, 3))
        stored = next(row for row in snapshot(self.path)["notes"] if row["id"] == created["id"])
        self.assertEqual((stored["title"], stored["body"], stored["version"]), ("Edited by Lee", "", 2))

    def test_fields_and_types_are_strict(self):
        for payload in (
            {}, {"expected_version": 1}, {"title": "A"},
            {"title": "A", "expected_version": True},
            {"title": "A", "expected_version": 1.0},
            {"title": "A", "expected_version": 2**63},
            {"title": "A", "expected_version": 1, "titel": "B"},
            {"title": "A", "expected_version": 1, "owner_id": 2},
            {"title": "A", "expected_version": 1, "workspace_id": 2},
        ):
            with self.subTest(payload=payload):
                self.assert_refused(422, "invalid_fields", lambda: self.patch(payload))
        for title in (None, "", " ", "A" * 201, "line\nbreak", "\ud800"):
            with self.subTest(title=repr(title)):
                self.assert_refused(422, "invalid_title",
                                    lambda: self.patch({"title": title, "expected_version": 1}))

    def test_permission_matrix_and_current_membership(self):
        for actor, workspace, note, status in ((None, 1, 101, 403), (2, 1, 101, 404),
                                              (3, 2, 202, 404), (1, 1, 202, 404)):
            code = "access_denied" if actor is None else "not_found"
            self.assert_refused(status, code, lambda: self.patch(
                {"title": "Denied", "expected_version": 1}, actor, workspace, note))
        self.assertEqual(self.patch({"title": "Alpha allowed", "expected_version": 1})[0], 200)
        self.assertEqual(self.patch({"title": "Beta allowed", "expected_version": 1}, 2, 2, 202)[0], 200)
        with sqlite3.connect(self.path) as db:
            db.execute("UPDATE memberships SET active = 0 WHERE user_id = 1 AND workspace_id = 1")
        self.assert_refused(404, "not_found", lambda: self.patch(
            {"title": "After revocation", "expected_version": 2}))

    def test_stale_repeat_and_invalid_transition_leave_full_state_unchanged(self):
        patch = {"title": "Release plan v2", "expected_version": 1}
        self.patch(patch)
        self.assert_refused(409, "stale_version", lambda: self.patch(patch))
        self.assert_refused(409, "invalid_transition", lambda: self.patch(
            {"title": "Must not leak through", "state": "open", "expected_version": 2}, actor=3))
        self.assertEqual(snapshot(self.path)["notes"][0]["title"], "Release plan v2")
        with sqlite3.connect(self.path) as db:
            db.execute("UPDATE notes SET version = ? WHERE id = 101", (2**63 - 1,))
        self.assert_refused(409, "version_exhausted", lambda: self.patch(
            {"title": "Beyond the version range", "expected_version": 2**63 - 1}))

    def test_archive_is_manager_only_and_terminal(self):
        self.assert_refused(403, "action_denied", lambda: self.patch(
            {"state": "archived", "expected_version": 1}))
        self.patch({"state": "archived", "expected_version": 1}, actor=3)
        for payload in ({"state": "open", "expected_version": 2},
                        {"title": "Late edit", "expected_version": 2}):
            self.assert_refused(409, "invalid_transition", lambda: self.patch(payload, actor=3))
        self.assertEqual(snapshot(self.path)["notes"][0]["state"], "archived")

    def test_export_replay_conflict_and_key_scope(self):
        first = self.export({"note_ids": [101]})
        before = snapshot(self.path)
        self.assertEqual(self.export({"note_ids": [101]}), first)
        self.assertEqual(snapshot(self.path), before)
        extra = create_note(self.path, actor_id=1, workspace_id=1, payload={"title": "Extra"})[1]
        self.assert_refused(409, "idempotency_conflict", lambda: self.export(
            {"note_ids": [101, extra["id"]]}))
        beta = self.export({"note_ids": [202]}, actor=2, workspace=2)
        self.assertNotEqual(first[1]["job_id"], beta[1]["job_id"])
        self.assertEqual(len(snapshot(self.path)["exports"]), 2)

    def test_export_canonical_order_and_bounds(self):
        extra = create_note(self.path, actor_id=1, workspace_id=1, payload={"title": "Extra"})[1]
        first = self.export({"note_ids": [101, extra["id"]]})
        self.assertEqual(self.export({"note_ids": [extra["id"], 101]}), first)
        for ids in ([], [True], [101, 101], list(range(1, 12)), [2**63]):
            self.assert_refused(422, "invalid_note_ids", lambda: self.export({"note_ids": ids}))
        self.assert_refused(422, "invalid_idempotency_key", lambda: self.export(
            {"note_ids": [101]}, key="bad key"))
        self.assert_refused(404, "not_found", lambda: self.export({"note_ids": [202]}))

    def test_replay_rechecks_permission(self):
        self.export({"note_ids": [101]})
        with sqlite3.connect(self.path) as db:
            db.execute("UPDATE memberships SET active = 0 WHERE user_id = 1 AND workspace_id = 1")
        self.assert_refused(404, "not_found", lambda: self.export({"note_ids": [101]}))

    def test_failure_before_receipt_completion_rolls_back_job_and_key(self):
        with sqlite3.connect(self.path) as db:
            db.execute("""CREATE TRIGGER fail_reply BEFORE UPDATE OF response_json ON export_requests
                          BEGIN SELECT RAISE(ABORT, 'synthetic receipt failure'); END""")
        before = snapshot(self.path)
        with self.assertRaises(sqlite3.IntegrityError):
            self.export({"note_ids": [101]})
        self.assertEqual(snapshot(self.path), before)


if __name__ == "__main__":
    unittest.main()
