import atexit
import os
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from hypothesis import example, given, settings

# A dedicated process owns this settings module and this disposable database.
folder = TemporaryDirectory(prefix="casebook-ch30-http-")
atexit.register(folder.cleanup)
os.environ["CASEBOOK_CH24_DB"] = str(Path(folder.name) / "http.sqlite3")
os.environ.pop("CASEBOOK_LOCAL_HTTP", None)
from examples.ch24 import browser_lab as lab
from django.contrib.auth import get_user_model
from django.contrib.sessions.models import Session
from django.db import connections
from django.test import Client, override_settings

from examples.ch23.authorization_service import revoke_member, snapshot
from examples.ch30.fixtures import BASE_CASE, NoteRecord, WorkspaceCase, assert_note_rows, install_case
from examples.ch30.response_policy import response_policy_failures
from examples.ch30.strategies import workspace_cases


def signed_client(user_id):
    client = Client(enforce_csrf_checks=True)
    client.force_login(get_user_model().objects.get(pk=user_id))
    return client


class HttpVerificationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        lab.initialize()
        override = override_settings(ROOT_URLCONF="examples.ch30.verification_lab")
        override.enable()
        cls.addClassCleanup(override.disable)
        cls.addClassCleanup(connections.close_all)

    def reset_example(self, case):
        install_case(lab.DATABASE, case)
        Session.objects.all().delete()

    def setUp(self):
        self.reset_example(BASE_CASE)

    def test_status_json_fields_unicode_and_method_contract(self):
        client = signed_client(1)
        path = "/workspaces/1/notes/"
        before = snapshot(lab.DATABASE)
        response = client.get(path, secure=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        document = response.json()
        self.assertEqual(set(document), {"workspace_id", "notes"})
        self.assertEqual(document["workspace_id"], 1)
        assert_note_rows(BASE_CASE, 1, document["notes"])
        self.assertEqual(document["notes"][0]["title"], "برنامه انتشار")
        refused = client.options(path, secure=True)
        self.assertEqual(refused.status_code, 405)
        self.assertEqual(refused["Allow"], "GET")
        self.assertEqual(snapshot(lab.DATABASE), before)

    def test_other_workspace_anonymous_and_revoked_session(self):
        mina = signed_client(1)
        ravi = signed_client(2)
        before = snapshot(lab.DATABASE)
        self.assertEqual(ravi.get("/workspaces/1/notes/", secure=True).status_code, 404)
        self.assertEqual(Client().get("/workspaces/1/notes/", secure=True).status_code, 403)
        self.assertEqual(snapshot(lab.DATABASE), before)
        self.assertEqual(mina.get("/workspaces/1/notes/", secure=True).status_code, 200)
        revoke_member(lab.DATABASE, actor_id=3, workspace_id=1, target_user_id=1)
        after_revocation = snapshot(lab.DATABASE)
        self.assertEqual(mina.session["_auth_user_id"], "1")
        self.assertEqual(mina.get("/workspaces/1/notes/", secure=True).status_code, 404)
        self.assertEqual(snapshot(lab.DATABASE), after_revocation)

    @settings(max_examples=60, deadline=None, database=None, derandomize=True)
    @example(case=BASE_CASE)
    @example(case=WorkspaceCase(1, 2, ()))
    @example(case=WorkspaceCase(9, 3, (NoteRecord(1, 3, "Beta only"),)))
    @given(case=workspace_cases())
    def test_generated_lists_match_current_workspace(self, case):
        # unittest.setUp runs once for this method, not once per generated input.
        self.reset_example(case)
        before = snapshot(lab.DATABASE)
        for user, workspace in ((1, case.alpha), (2, case.beta), (3, case.alpha)):
            response = signed_client(user).get(f"/workspaces/{workspace}/notes/", secure=True)
            self.assertEqual(response.status_code, 200)
            document = response.json()
            self.assertEqual(set(document), {"workspace_id", "notes"})
            self.assertEqual(document["workspace_id"], workspace)
            assert_note_rows(case, workspace, document["notes"])
        for user, workspace in ((1, case.beta), (2, case.alpha), (3, case.beta)):
            response = signed_client(user).get(f"/workspaces/{workspace}/notes/", secure=True)
            self.assertEqual(response.status_code, 404)
        self.assertEqual(snapshot(lab.DATABASE), before)

    def test_response_policy_on_success_and_denials(self):
        mina = signed_client(1)
        responses = (
            (mina.get("/workspaces/1/notes/", secure=True), 200),
            (mina.get("/workspaces/2/notes/", secure=True), 404),
            (Client().get("/workspaces/1/notes/", secure=True), 403),
        )
        for response, expected_status in responses:
            self.assertEqual(response.status_code, expected_status)
            self.assertEqual(response_policy_failures(response.headers), [])


if __name__ == "__main__":
    unittest.main()
