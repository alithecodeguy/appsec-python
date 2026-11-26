import json
from pathlib import Path
import sqlite3
from tempfile import TemporaryDirectory
import unittest

from authorization_service import (
    AccessDenied, build_export, detail_view, download_export, detail_for_user, list_for_user,
    list_view, revoke_member, seed, snapshot,
)


class AuthorizationTests(unittest.TestCase):
    def setUp(self):
        self.folder = TemporaryDirectory(prefix="casebook-authorization-test-")
        self.addCleanup(self.folder.cleanup)
        self.path = Path(self.folder.name) / "authorization.sqlite3"
        seed(self.path)

    def assert_denied_unchanged(self, status, operation):
        before = snapshot(self.path)
        with self.assertRaises(AccessDenied) as caught:
            operation()
        self.assertEqual(caught.exception.status, status)
        self.assertEqual(snapshot(self.path), before)

    def test_same_matrix_across_list_detail_export_and_own_download(self):
        cases = (
            (1, 1, 101, True), (1, 2, 202, False),
            (2, 1, 101, False), (2, 2, 202, True),
            (3, 1, 101, True), (3, 2, 202, False),
            (None, 1, 101, False), (None, 2, 202, False),
        )
        for user, workspace, note, allowed in cases:
            with self.subTest(user=user, workspace=workspace):
                operations = (
                    lambda: list_for_user(self.path, user_id=user, workspace_id=workspace),
                    lambda: detail_for_user(self.path, user_id=user, workspace_id=workspace, note_id=note),
                    lambda: build_export(self.path, user_id=user, workspace_id=workspace, note_ids=[note]),
                )
                if not allowed:
                    expected_status = 403 if user is None else 404
                    expected_body = {"error": {"code": "access_denied" if user is None else "not_found"}}
                    self.assertEqual(list_view(self.path, user_id=user, workspace_id=workspace),
                                     (expected_status, expected_body))
                    self.assertEqual(detail_view(self.path, user_id=user, workspace_id=workspace,
                                                 note_id=note), (expected_status, expected_body))
                    for operation in operations:
                        self.assert_denied_unchanged(expected_status, operation)
                    continue
                summaries, detail, artifact = [operation() for operation in operations]
                self.assertEqual([row["id"] for row in summaries], [note])
                self.assertEqual(detail["workspace_id"], workspace)
                document = json.loads(download_export(self.path, user_id=user, artifact=artifact))
                self.assertEqual(document["workspace_id"], workspace)
                self.assertEqual([row["id"] for row in document["notes"]], [note])
                self.assertEqual(document["notes"][0], detail)

    def test_summary_field_allowlist_preserves_private_detail_and_storage(self):
        before = snapshot(self.path)
        summary = list_for_user(self.path, user_id=1, workspace_id=1)[0]
        detail = detail_for_user(self.path, user_id=1, workspace_id=1, note_id=101)
        self.assertEqual(set(summary), {"id", "workspace_id", "title"})
        self.assertNotIn("Alpha private fixture", json.dumps(summary))
        self.assertEqual(detail["body"], "Alpha private fixture")
        self.assertEqual(snapshot(self.path), before)

    def test_cross_workspace_id_substitution_and_mixed_export_are_denied(self):
        self.assert_denied_unchanged(404, lambda: detail_for_user(
            self.path, user_id=1, workspace_id=1, note_id=202))
        self.assert_denied_unchanged(404, lambda: build_export(
            self.path, user_id=1, workspace_id=1, note_ids=[101, 202]))
        self.assert_denied_unchanged(404, lambda: detail_for_user(
            self.path, user_id=1, workspace_id=1, note_id=999))

    def test_cached_artifact_is_requester_bound(self):
        artifact = build_export(self.path, user_id=1, workspace_id=1, note_ids=[101])
        self.assert_denied_unchanged(404, lambda: download_export(self.path, user_id=3, artifact=artifact))
        self.assert_denied_unchanged(404, lambda: download_export(self.path, user_id=2, artifact=artifact))
        self.assert_denied_unchanged(403, lambda: download_export(self.path, user_id=None, artifact=artifact))

    def test_committed_revocation_affects_next_request_and_cached_download(self):
        self.assertEqual(list_view(self.path, user_id=1, workspace_id=1)[0], 200)
        artifact = build_export(self.path, user_id=1, workspace_id=1, note_ids=[101])
        notes = snapshot(self.path)["notes"]
        revoke_member(self.path, actor_id=3, workspace_id=1, target_user_id=1)
        self.assertEqual(snapshot(self.path)["memberships"][0]["active"], 0)
        for operation in (
            lambda: list_for_user(self.path, user_id=1, workspace_id=1),
            lambda: detail_for_user(self.path, user_id=1, workspace_id=1, note_id=101),
            lambda: build_export(self.path, user_id=1, workspace_id=1, note_ids=[101]),
            lambda: download_export(self.path, user_id=1, artifact=artifact),
        ):
            self.assert_denied_unchanged(404, operation)
        self.assertEqual(snapshot(self.path)["notes"], notes)
        self.assertEqual(detail_for_user(self.path, user_id=3, workspace_id=1, note_id=101)["id"], 101)
        self.assertEqual(detail_for_user(self.path, user_id=2, workspace_id=2, note_id=202)["id"], 202)

    def test_manager_action_is_function_and_workspace_scoped(self):
        self.assert_denied_unchanged(403, lambda: revoke_member(
            self.path, actor_id=1, workspace_id=1, target_user_id=1))
        self.assert_denied_unchanged(404, lambda: revoke_member(
            self.path, actor_id=3, workspace_id=2, target_user_id=2))
        self.assert_denied_unchanged(404, lambda: revoke_member(
            self.path, actor_id=3, workspace_id=1, target_user_id=2))

    def test_inactive_account_is_denied_even_with_active_membership(self):
        with sqlite3.connect(self.path) as db:
            db.execute("UPDATE users SET active = 0 WHERE id = 1")
        self.assert_denied_unchanged(404, lambda: list_for_user(self.path, user_id=1, workspace_id=1))

    def test_owner_field_does_not_grant_cross_workspace_access(self):
        with sqlite3.connect(self.path) as db:
            db.execute("UPDATE notes SET owner_id = 2 WHERE id = 101")
        self.assert_denied_unchanged(404, lambda: detail_for_user(
            self.path, user_id=2, workspace_id=1, note_id=101))

    def test_empty_authorized_list_and_generic_denials(self):
        with sqlite3.connect(self.path) as db:
            db.execute("DELETE FROM notes WHERE id = 101")
        self.assertEqual(list_view(self.path, user_id=1, workspace_id=1), (200, []))
        self.assertEqual(detail_view(self.path, user_id=1, workspace_id=1, note_id=101),
                         detail_view(self.path, user_id=2, workspace_id=1, note_id=101))

    def test_bounds_and_unicode_export(self):
        for limit in (0, 51, True):
            with self.assertRaises(ValueError):
                list_for_user(self.path, user_id=1, workspace_id=1, limit=limit)
        for selection in ([], [101, 101], [True], list(range(1, 12))):
            with self.assertRaises(ValueError):
                build_export(self.path, user_id=1, workspace_id=1, note_ids=selection)
        with sqlite3.connect(self.path) as db:
            db.execute("UPDATE notes SET title = ? WHERE id = 101", ("برنامه انتشار",))
        artifact = build_export(self.path, user_id=1, workspace_id=1, note_ids=[101])
        self.assertEqual(json.loads(download_export(self.path, user_id=1, artifact=artifact))
                         ["notes"][0]["title"], "برنامه انتشار")

    def test_failed_membership_write_rolls_back(self):
        with sqlite3.connect(self.path) as db:
            db.execute("""CREATE TRIGGER refuse_revoke BEFORE UPDATE OF active ON memberships
                          BEGIN SELECT RAISE(ABORT, 'synthetic membership failure'); END""")
        before = snapshot(self.path)
        with self.assertRaises(sqlite3.IntegrityError):
            revoke_member(self.path, actor_id=3, workspace_id=1, target_user_id=1)
        self.assertEqual(snapshot(self.path), before)
        self.assertEqual(list_view(self.path, user_id=1, workspace_id=1)[0], 200)


if __name__ == "__main__":
    unittest.main()
