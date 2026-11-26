import atexit
import os
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

# Import this standalone settings module in its own test process, before other Django settings.
folder = TemporaryDirectory(prefix="casebook-browser-test-")
atexit.register(folder.cleanup)
os.environ["CASEBOOK_CH24_DB"] = str(Path(folder.name) / "browser.sqlite3")
os.environ.pop("CASEBOOK_LOCAL_HTTP", None)
from examples.ch24 import browser_lab as lab
from examples.ch24.html_evidence import PageEvidence
from examples.ch23.authorization_service import revoke_member, seed, snapshot, unit
from django.contrib.sessions.models import Session
from django.db import connections
from django.test import Client


class BrowserTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        lab.initialize()

    @classmethod
    def tearDownClass(cls):
        connections.close_all()

    def setUp(self):
        # Reset only this newly created, named test database's synthetic note tables.
        with unit(lab.DATABASE, write=True) as db:
            for table in ("notes", "memberships", "users", "workspaces"):
                db.execute(f"DROP TABLE {table}")
        seed(lab.DATABASE)
        lab.title_fixture()
        Session.objects.all().delete()
        self.client = Client(enforce_csrf_checks=True)

    def page(self, response):
        parsed = PageEvidence()
        parsed.feed(response.content.decode("utf-8"))
        return parsed

    def login(self, username="mina"):
        page = self.client.get("/accounts/login/", secure=True)
        token = self.page(page).inputs["csrfmiddlewaretoken"]
        response = self.client.post("/accounts/login/", {
            "username": username, "password": lab.PASSWORD, "csrfmiddlewaretoken": token,
        }, secure=True, HTTP_ORIGIN="https://testserver")
        self.assertEqual(response.status_code, 302)
        return response

    def form(self, workspace=1, note=101):
        page = self.client.get(f"/workspaces/{workspace}/notes/{note}/", secure=True)
        self.assertEqual(page.status_code, 200)
        return self.page(page).inputs

    def post(self, fields, workspace=1, note=101, origin="https://testserver"):
        return self.client.post(f"/workspaces/{workspace}/notes/{note}/title/", fields,
                                secure=True, HTTP_ORIGIN=origin)

    def test_login_requires_csrf_and_private_reads_require_identity(self):
        before = snapshot(lab.DATABASE)
        denied = self.client.post("/accounts/login/", {"username": "mina", "password": lab.PASSWORD},
                                  secure=True, HTTP_ORIGIN="https://testserver")
        self.assertEqual(denied.status_code, 403)
        self.assertEqual(self.client.get("/workspaces/1/notes/101/", secure=True).status_code, 403)
        self.assertEqual(snapshot(lab.DATABASE), before)

    def test_real_login_and_two_workspace_object_matrix(self):
        for username, allowed, denied in (("mina", (1,101), (2,202)),
                                          ("ravi", (2,202), (1,101)),
                                          ("lee", (1,101), (2,202))):
            self.client = Client(enforce_csrf_checks=True)
            self.login(username)
            self.assertEqual(self.client.get(f"/workspaces/{allowed[0]}/notes/{allowed[1]}/", secure=True).status_code, 200)
            response = self.client.get(f"/workspaces/{denied[0]}/notes/{denied[1]}/", secure=True)
            self.assertEqual(response.status_code, 404)
            self.assertNotIn(b"private fixture", response.content)

    def test_escaped_source_and_parsed_text(self):
        self.login()
        page = self.client.get("/workspaces/1/notes/101/", secure=True)
        self.assertEqual(page["Content-Type"], "text/html; charset=utf-8")
        self.assertIn(b'<h1 id="note-title">A &amp; B</h1>', page.content)
        self.assertEqual(self.page(page).title_text, "A & B")
        self.assertEqual(self.page(page).inputs["title"], "A & B")
        with unit(lab.DATABASE, write=True) as db:
            db.execute("UPDATE notes SET title=? WHERE id=101", ('<img src=x onerror="alert(1)">',))
        page = self.client.get("/workspaces/1/notes/101/", secure=True)
        parsed = self.page(page)
        self.assertEqual(parsed.title_text, '<img src=x onerror="alert(1)">')
        self.assertEqual(parsed.active_tags, [])
        self.assertNotIn(b"<img", page.content)

    def test_missing_token_refuses_with_valid_session_and_no_write(self):
        self.login()
        fields = self.form()
        before = snapshot(lab.DATABASE)
        denied = self.post({"title": "Must not save", "expected_version": fields["expected_version"]})
        self.assertEqual(denied.status_code, 403)
        self.assertEqual(snapshot(lab.DATABASE), before)

    def test_wrong_origin_refuses_even_with_valid_token(self):
        self.login()
        fields = self.form()
        before = snapshot(lab.DATABASE)
        denied = self.post({**fields, "title": "Must not save"}, origin="https://other.example")
        self.assertEqual(denied.status_code, 403)
        self.assertEqual(snapshot(lab.DATABASE), before)
        accepted = self.client.post("/workspaces/1/notes/101/title/",
                                    {**fields, "title": "Allowed same-origin referer"},
                                    secure=True, HTTP_REFERER="https://testserver/workspaces/1/notes/101/")
        self.assertEqual(accepted.status_code, 303)
        self.assertEqual(snapshot(lab.DATABASE)["notes"][0]["version"], 2)

    def test_valid_change_and_stale_repeat_inspect_stored_state(self):
        self.login()
        fields = {**self.form(), "title": "A & B — reviewed"}
        before = snapshot(lab.DATABASE)
        accepted = self.post(fields)
        self.assertEqual(accepted.status_code, 303)
        after = snapshot(lab.DATABASE)
        note = after["notes"][0]
        self.assertEqual((note["title"], note["version"], note["owner_id"], note["updated_by"]),
                         ("A & B — reviewed", 2, 1, 1))
        self.assertEqual(note["body"], before["notes"][0]["body"])
        self.assertEqual(after["notes"][1], before["notes"][1])
        self.assertEqual(self.post(fields).status_code, 409)
        self.assertEqual(snapshot(lab.DATABASE), after)

    def test_valid_csrf_does_not_authorize_another_workspace(self):
        self.login("ravi")
        fields = {**self.form(2,202), "title": "Denied Alpha change"}
        before = snapshot(lab.DATABASE)
        self.assertEqual(self.post(fields).status_code, 404)
        self.assertEqual(snapshot(lab.DATABASE), before)

    def test_revocation_affects_next_get_and_post_with_same_session(self):
        self.login()
        fields = {**self.form(), "title": "Denied after revocation"}
        revoke_member(lab.DATABASE, actor_id=3, workspace_id=1, target_user_id=1)
        before = snapshot(lab.DATABASE)
        self.assertEqual(self.client.session["_auth_user_id"], "1")
        self.assertEqual(self.client.get("/workspaces/1/notes/101/", secure=True).status_code, 404)
        self.assertEqual(self.post(fields).status_code, 404)
        self.assertEqual(snapshot(lab.DATABASE), before)

    def test_headers_cookie_flags_and_absent_cors_permission(self):
        self.login()
        page = self.client.get("/workspaces/1/notes/101/", secure=True, HTTP_ORIGIN="https://other.example")
        self.assertEqual(page.status_code, 200)  # Test client does not enforce browser CORS.
        self.assertNotIn("Access-Control-Allow-Origin", page)
        self.assertEqual(page["Cache-Control"], "no-store")
        self.assertEqual(page["X-Frame-Options"], "DENY")
        self.assertEqual(page["Referrer-Policy"], "same-origin")
        self.assertEqual(page["X-Content-Type-Options"], "nosniff")
        for directive in ("default-src 'none'", "form-action 'self'", "frame-ancestors 'none'"):
            self.assertIn(directive, page["Content-Security-Policy"])
        cookie = self.client.cookies[lab.settings.SESSION_COOKIE_NAME]
        self.assertTrue(cookie["secure"])
        self.assertTrue(cookie["httponly"])
        self.assertEqual(cookie["samesite"], "Lax")
        self.assertEqual(cookie["path"], "/")
        self.assertFalse(cookie["domain"])
        probe = self.client.get("/csp-probe/", secure=True)
        self.assertIn(b"<script>", probe.content)
        self.assertIn("script-src 'none'", probe["Content-Security-Policy"])


if __name__ == "__main__":
    unittest.main()
