"""Optional adapter tests, run in a separate interpreter from other Django lab settings."""
import importlib.util
import json
import os
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

HAS_DJANGO = importlib.util.find_spec("django") is not None
if HAS_DJANGO:
    AUTH_FOLDER = TemporaryDirectory(prefix="casebook-ch42-auth-")
    os.environ["CASEBOOK_CH42_AUTH_DB"] = str(Path(AUTH_FOLDER.name)/"auth.sqlite3")
    from examples.ch42 import web
    from examples.ch42.capstone import Clock, initialize, snapshot, work
    from django.contrib.auth import get_user_model
    from django.core.management import call_command
    from django.db import connections
    from django.test import Client


@unittest.skipUnless(HAS_DJANGO,"Django 6.1.3 unavailable; HTTP/CSRF checks NOT executed")

class WebTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        call_command("migrate",verbosity=0)
        cls.users = {}
        for pk,name in ((1,"mina"),(2,"ravi"),(3,"lee")):
            user = get_user_model().objects.create_user(pk=pk,username=name)
            user.set_unusable_password()
            user.save()
            cls.users[pk] = user

    @classmethod
    def tearDownClass(cls):
        connections.close_all()
        AUTH_FOLDER.cleanup()

    def setUp(self):
        self.folder = TemporaryDirectory(prefix="casebook-ch42-web-")
        self.addCleanup(self.folder.cleanup)
        web.DATABASE = Path(self.folder.name)/"capstone.sqlite3"
        initialize(web.DATABASE)
        web.clock = Clock()
        self.client = Client(enforce_csrf_checks=True)
        self.client.force_login(self.users[1])  # Real test session; no identity header.
        self.token = self.client.get("/api/csrf/",secure=True).json()["token"]
        self.base = "/api/v1/workspaces/1/exports/"

    def post(self,path,body,**headers):
        return self.client.post(path,data=json.dumps(body),content_type="application/json",secure=True,
            HTTP_X_CSRFTOKEN=self.token,HTTP_ORIGIN="https://testserver",**headers)

    def create(self):
        response = self.post(self.base,{"note_ids":[101]},HTTP_IDEMPOTENCY_KEY="web-001")
        self.assertEqual(response.status_code,202)
        return response.json()["job_id"]

    def test_A41_14_csrf_duplicate_json_methods_and_no_store(self):
        before = snapshot(web.DATABASE)
        denied = self.client.post(self.base,data='{"note_ids":[101]}',content_type="application/json",secure=True)
        self.assertEqual(denied.status_code,403)
        self.assertEqual(snapshot(web.DATABASE),before)
        wrong = self.client.get(self.base,secure=True)
        self.assertEqual((wrong.status_code,wrong["Allow"],wrong["Cache-Control"]),(405,"POST","no-store"))
        duplicate = self.client.post(self.base,data='{"note_ids":[101],"note_ids":[202]}',
            content_type="application/json",secure=True,HTTP_X_CSRFTOKEN=self.token,
            HTTP_ORIGIN="https://testserver",HTTP_IDEMPOTENCY_KEY="web-001")
        self.assertEqual(duplicate.status_code,400)
        self.assertEqual(snapshot(web.DATABASE),before)

    def test_A41_01_02_09_session_replay_content_and_cross_workspace(self):
        job = self.create()
        original = snapshot(web.DATABASE)
        self.assertEqual(self.create(),job)
        self.assertEqual(snapshot(web.DATABASE),original)
        work(web.DATABASE,workspace_id=1,job_id=job,keyrings=web.KEYRINGS,clock=web.clock)
        path = self.base+f"{job}/content/"
        allowed = self.client.get(path,secure=True)
        self.assertEqual(allowed.status_code,200)
        self.assertEqual(allowed.json()["workspace_id"],1)
        self.assertEqual(allowed["Cache-Control"],"no-store")
        self.assertIn("attachment",allowed["Content-Disposition"])
        self.client.force_login(self.users[2])
        saved = snapshot(web.DATABASE)
        denied = self.client.get(path,secure=True)
        self.assertEqual((denied.status_code,denied.json()),(404,{"error":{"code":"not_found"}}))
        self.assertEqual(snapshot(web.DATABASE),saved)
        visitor = Client(enforce_csrf_checks=True).get(path,secure=True)
        self.assertEqual(visitor.status_code,403)

    def test_A41_07_08_expire_post_and_clock_boundary(self):
        job = self.create()
        work(web.DATABASE,workspace_id=1,job_id=job,keyrings=web.KEYRINGS,clock=web.clock)
        content,ending = self.base+f"{job}/content/",self.base+f"{job}/expire/"
        self.assertEqual(self.client.get(ending,secure=True).status_code,405)
        self.assertEqual(self.post(ending,{}).status_code,204)
        saved = snapshot(web.DATABASE)
        self.assertEqual(self.post(ending,{}).status_code,204)
        self.assertEqual(snapshot(web.DATABASE),saved)
        self.assertEqual(self.client.get(content,secure=True).status_code,410)
        self.assertEqual(snapshot(web.DATABASE),saved)


if __name__ == "__main__":
    unittest.main()
