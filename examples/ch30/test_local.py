from itertools import product
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from examples.ch23.authorization_service import (
    AccessDenied, list_for_user, note_fields, require_member, revoke_member, seed, snapshot, unit,
)
from examples.ch30.fixtures import BASE_CASE, NoteRecord, WorkspaceCase, assert_note_rows, install_case
from examples.ch30.response_policy import ENFORCED_CSP, response_policy_failures


def global_list(database, *, user_id, workspace_id, limit=50):
    # Deliberately broken local candidate, never a route or a replacement production helper.
    with unit(database) as db:
        require_member(db, user_id, workspace_id)
        rows = db.execute("SELECT id, workspace_id, title, body FROM notes ORDER BY id LIMIT ?",
                          (limit,)).fetchall()
        return [note_fields(row) for row in rows]


class LocalVerificationTests(unittest.TestCase):
    def setUp(self):
        self.folder = TemporaryDirectory(prefix="casebook-ch30-local-")
        self.addCleanup(self.folder.cleanup)
        self.database = Path(self.folder.name) / "local.sqlite3"
        seed(self.database)
        install_case(self.database, BASE_CASE)

    def test_bounded_layouts_at_the_service_boundary(self):
        layouts = 0
        for alpha, beta in ((1, 2), (2, 1), (9, 3)):
            for size in range(5):
                for owners in product((alpha, beta), repeat=size):
                    case = WorkspaceCase(alpha, beta, tuple(
                        NoteRecord(101 + index, workspace, "برنامه انتشار")
                        for index, workspace in enumerate(owners)))
                    install_case(self.database, case)
                    before = snapshot(self.database)
                    for user, workspace in ((1, alpha), (2, beta), (3, alpha)):
                        rows = list_for_user(self.database, user_id=user,
                                             workspace_id=workspace, limit=50)
                        assert_note_rows(case, workspace, rows)
                    for user, workspace in ((1, beta), (2, alpha), (3, beta), (None, alpha)):
                        with self.assertRaises(AccessDenied):
                            list_for_user(self.database, user_id=user, workspace_id=workspace)
                    self.assertEqual(snapshot(self.database), before)
                    layouts += 1
        self.assertEqual(layouts, 93)

    def test_negative_control_leaks_despite_conforming_header_values(self):
        rows = global_list(self.database, user_id=1, workspace_id=1)
        self.assertEqual([row["id"] for row in rows], [101, 202])
        with self.assertRaises(AssertionError):
            assert_note_rows(BASE_CASE, 1, rows)
        headers = {"Cache-Control": "no-store", "Content-Security-Policy": ENFORCED_CSP}
        self.assertEqual(response_policy_failures(headers), [])

    def test_current_membership_changes_the_next_service_read(self):
        assert_note_rows(BASE_CASE, 1, list_for_user(self.database, user_id=1, workspace_id=1))
        revoke_member(self.database, actor_id=3, workspace_id=1, target_user_id=1)
        after_revocation = snapshot(self.database)
        with self.assertRaises(AccessDenied):
            list_for_user(self.database, user_id=1, workspace_id=1)
        self.assertEqual(snapshot(self.database), after_revocation)

    def test_supplied_report_only_observation_fails_enforcement_requirement(self):
        report = json.loads(Path(__file__).with_name("passive-report.json").read_text())
        self.assertEqual(report["provenance"], "authored teaching fixture")
        self.assertEqual(response_policy_failures(report["response"]["headers"]),
                         ["missing enforced Content-Security-Policy"])

    def test_exact_enforced_header_and_weaker_variants(self):
        headers = {"Cache-Control": "no-store", "Content-Security-Policy": ENFORCED_CSP}
        self.assertEqual(response_policy_failures(headers), [])
        for bad in (ENFORCED_CSP.replace("script-src 'none'", "script-src *"),
                    ENFORCED_CSP + "; script-src 'none'",
                    ENFORCED_CSP + "; script-src-elem *"):
            self.assertTrue(response_policy_failures(headers | {"Content-Security-Policy": bad}))

    def test_csp_does_not_replace_no_store(self):
        self.assertEqual(response_policy_failures({"Content-Security-Policy": ENFORCED_CSP}),
                         ["missing Cache-Control no-store"])


if __name__ == "__main__":
    unittest.main()
