import json
from pathlib import Path
import sqlite3
from tempfile import TemporaryDirectory
import unittest

from examples.ch23.authorization_service import AccessDenied
from examples.ch26.fake_partner import FakeTransport,Reply
from examples.ch26.integrations import (
    FIXTURE_KEYS,FIXTURE_NOW,MAX_REPLY,Refused,handle_webhook,initialize,inventory,refresh_status,signature,
)

FIXTURES=Path(__file__).parent/"fixtures"


class IntegrationTests(unittest.TestCase):
    def setUp(self):
        self.folder=TemporaryDirectory(prefix="casebook-integration-test-")
        self.addCleanup(self.folder.cleanup)
        self.db=Path(self.folder.name)/"casebook.sqlite3"
        initialize(self.db)
        self.raw=(FIXTURES/"report-ready.json").read_bytes()
        self.headers=json.loads((FIXTURES/"report-ready.headers.json").read_text())

    def refresh(self,reply,user=1,clock=lambda:0):
        fake=FakeTransport(reply)
        result=refresh_status(self.db,user_id=user,workspace_id=1,partner_id="reports",transport=fake,clock=clock)
        return result,fake

    def deliver(self,raw=None,kid="old",keys=FIXTURE_KEYS,timestamp=None,tag=None):
        raw=self.raw if raw is None else raw
        timestamp=str(FIXTURE_NOW) if timestamp is None else timestamp
        if tag is None:
            tag=signature(FIXTURE_KEYS["reports"][kid],"reports",timestamp,raw)
        return handle_webhook(self.db,partner_id="reports",raw=raw,timestamp=timestamp,key_id=kid,
                              supplied_signature=tag,keyrings=keys,now=FIXTURE_NOW)

    def test_redirect_and_oversize_close_and_preserve_state(self):
        for reply,reason in ((Reply(307,headers=(("Location","http://127.0.0.1/"),)),"redirect_refused"),
                             (Reply(body=b"x"*129),"reply_too_large")):
            before=inventory(self.db)
            fake=FakeTransport(reply)
            with self.assertRaisesRegex(Refused,reason):
                refresh_status(self.db,user_id=1,workspace_id=1,partner_id="reports",transport=fake,clock=lambda:0)
            self.assertEqual(len(fake.calls),1)
            self.assertTrue(reply.closed)
            self.assertEqual(inventory(self.db),before)
        self.assertEqual(reply.read_requests,[MAX_REPLY+1])

    def test_valid_partner_and_permission_prevent_cross_workspace_call(self):
        result,fake=self.refresh(Reply(body=b'{"account_ref":"alpha-remote","status":"ok"}'))
        self.assertEqual(result,"ok")
        self.assertEqual(fake.calls,[("https://reports.partner.example/v1/status?account_ref=alpha-remote",2.0,128)])
        denied=FakeTransport(Reply())
        with self.assertRaises(AccessDenied):
            refresh_status(self.db,user_id=2,workspace_id=1,partner_id="reports",transport=denied)
        self.assertEqual(denied.calls,[])

    def test_schema_deadline_timeout_and_unknown_partner_do_not_write(self):
        before=inventory(self.db)
        for body in (b'{"account_ref":"beta-remote","status":"ok"}',b'{"account_ref":"alpha-remote","status":"ok","role":"manager"}'):
            with self.assertRaises(Refused): self.refresh(Reply(body=body))
        ticks=iter((0.0,3.0))
        with self.assertRaisesRegex(Refused,"deadline_exceeded"):
            self.refresh(Reply(body=b'{"account_ref":"alpha-remote","status":"ok"}'),clock=lambda:next(ticks))
        with self.assertRaises(TimeoutError): self.refresh(TimeoutError("synthetic timeout"))
        fake=FakeTransport(Reply())
        with self.assertRaises(Refused):
            refresh_status(self.db,user_id=1,workspace_id=1,partner_id="http://127.0.0.1",transport=fake)
        self.assertEqual(fake.calls,[])
        self.assertEqual(inventory(self.db),before)
        body=b'{"account_ref":"alpha-remote","status":"ok"}'
        self.assertEqual(self.refresh(Reply(body=body+b" "*(MAX_REPLY-len(body))))[0],"ok")

    def test_stored_signed_fixture_and_duplicate_have_one_effect(self):
        self.assertEqual(self.deliver(tag=self.headers["signature"]),(200,{"received":True}))
        before=inventory(self.db)
        self.assertEqual(self.deliver(),(200,{"received":True}))
        self.assertEqual(inventory(self.db),before)
        self.assertEqual((len(before["reports"]),len(before["webhook_receipts"])),(1,1))

    def test_authenticity_window_and_rotation(self):
        before=inventory(self.db)
        for timestamp in (str(FIXTURE_NOW-301),str(FIXTURE_NOW+301)):
            with self.assertRaises(Refused): self.deliver(timestamp=timestamp)
        with self.assertRaises(Refused): self.deliver(tag="0"*64)
        with self.assertRaises(Refused): self.deliver(raw=self.raw+b" ",tag=self.headers["signature"])
        only_new={"reports":{"new":FIXTURE_KEYS["reports"]["new"]}}
        with self.assertRaises(Refused): self.deliver(keys=only_new)
        self.assertEqual(inventory(self.db),before)
        self.assertEqual(self.deliver(kid="new",keys=only_new)[0],200)
        self.assertEqual(self.deliver(timestamp=str(FIXTURE_NOW-300),kid="new",keys=only_new)[0],200)

    def test_event_collision_and_unknown_binding_leave_state_unchanged(self):
        self.deliver()
        before=inventory(self.db)
        payload=json.loads(self.raw)
        payload["report_ref"]="different-report"
        with self.assertRaisesRegex(Refused,"event_id_conflict"):
            self.deliver(raw=json.dumps(payload).encode())
        payload["account_ref"]="unregistered"
        with self.assertRaises(Refused): self.deliver(raw=json.dumps(payload).encode())
        self.assertEqual(inventory(self.db),before)

    def test_business_key_prevents_same_report_under_new_event_id(self):
        self.deliver()
        payload=json.loads(self.raw)
        payload["id"]="evt-alpha-002"
        self.deliver(raw=json.dumps(payload).encode())
        saved=inventory(self.db)
        self.assertEqual((len(saved["webhook_receipts"]),len(saved["reports"])),(2,1))

    def test_receipt_failure_rolls_back_business_effect(self):
        with sqlite3.connect(self.db) as db:
            db.execute("""CREATE TRIGGER fail_receipt BEFORE INSERT ON webhook_receipts
                          BEGIN SELECT RAISE(ABORT,'synthetic receipt failure'); END""")
        before=inventory(self.db)
        with self.assertRaises(sqlite3.IntegrityError): self.deliver()
        self.assertEqual(inventory(self.db),before)


if __name__=="__main__":
    unittest.main()
