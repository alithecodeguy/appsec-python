import json
from pathlib import Path
from tempfile import TemporaryDirectory

from examples.ch26.fake_partner import FakeTransport, Reply
from examples.ch26.integrations import (
    FIXTURE_KEYS,FIXTURE_NOW,Refused,handle_webhook,initialize,inventory,refresh_status,
)

FIXTURES = Path(__file__).parent / "fixtures"

with TemporaryDirectory(prefix="casebook-integration-") as folder:
    database = Path(folder) / "casebook.sqlite3"
    initialize(database)
    for label,reply in (
        ("redirect",Reply(302,headers=(("Location","http://127.0.0.1/internal"),))),
        ("oversized",Reply(body=b"x"*129)),
    ):
        transport=FakeTransport(reply)
        before=inventory(database)
        try:
            refresh_status(database,user_id=1,workspace_id=1,partner_id="reports",transport=transport,clock=lambda:0)
        except Refused as exc:
            print(label+":",str(exc))
        print("calls, closed, unchanged:",len(transport.calls),reply.closed,inventory(database)==before)
    reply=Reply(body=b'{"account_ref":"alpha-remote","status":"ok"}')
    print("accepted status:",refresh_status(database,user_id=1,workspace_id=1,partner_id="reports",
                                           transport=FakeTransport(reply),clock=lambda:0))
    headers=json.loads((FIXTURES/"report-ready.headers.json").read_text())
    raw=(FIXTURES/"report-ready.json").read_bytes()
    def deliver():
        return handle_webhook(database,raw=raw,partner_id=headers["partner_id"],timestamp=headers["timestamp"],
                              key_id=headers["key_id"],supplied_signature=headers["signature"],
                              keyrings=FIXTURE_KEYS,now=FIXTURE_NOW)
    print("first delivery:",deliver())
    saved=inventory(database)
    print("duplicate delivery:",deliver())
    print("same final state:",inventory(database)==saved)
    print("receipt rows, report rows:",len(saved["webhook_receipts"]),len(saved["reports"]))
    print("Alpha and Beta statuses:",[(r["workspace_id"],r["status"],r["refresh_count"]) for r in saved["partner_bindings"]])
