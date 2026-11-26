import argparse
import json
from pathlib import Path
from tempfile import TemporaryDirectory

from examples.ch23.authorization_service import AccessDenied, revoke_member, unit
from examples.ch42.capstone import (
    Clock, GRACE, RETENTION, Problem, access_end, cleanup, collect, expire, initialize,
    purge, request_export, snapshot, work,
)
from examples.ch42.fixtures import dummy_keyrings
from examples.ch42.workers import two_workers


def run(stage):
    with TemporaryDirectory(prefix="casebook-ch42-demo-") as folder:
        database = Path(folder)/"capstone.sqlite3"
        initialize(database)
        clock,keys = Clock(),dummy_keyrings()
        def request(user=1,workspace=1,note=101,key="mina-001"):
            return request_export(database,user_id=user,workspace_id=workspace,body={"note_ids":[note]},client_key=key,clock=clock)
        receipt = request()
        job = receipt["job_id"]
        if stage == "admission":
            before = snapshot(database)
            print("same receipt:",request()==receipt)
            print("request rows and reserved slots:",len(before["jobs"]),sum(j["reserved"] for j in before["jobs"]))
            try: request(user=2)
            except AccessDenied: print("Ravi requests Alpha: denied")
            print("retry/refusal leave stored state unchanged:",snapshot(database)==before)
        elif stage == "worker":
            beta = request(user=2,workspace=2,note=202,key="ravi-001")["job_id"]
            outcomes = two_workers(database,workspace_id=1,job_id=job,keyrings=keys,clock=clock)
            work(database,workspace_id=2,job_id=beta,keyrings=keys,clock=clock)
            print("both workers observed no result:",all(missing for missing,_ in outcomes))
            print("worker outcomes:",sorted(result for _,result in outcomes))
            print("Alpha/Beta result rows:",len(snapshot(database)["encrypted_exports"]))
            for user,workspace,selected in ((1,1,job),(2,2,beta)):
                body=collect(database,user_id=user,workspace_id=workspace,job_id=selected,keyrings=keys,clock=clock)
                print("collected workspace and note:",workspace,json.loads(body)["notes"][0]["id"])
            before=snapshot(database)
            print("duplicate delivery:",work(database,workspace_id=1,job_id=job,keyrings=keys,clock=clock))
            print("duplicate state unchanged:",snapshot(database)==before)
            revoke_member(database,actor_id=3,workspace_id=1,target_user_id=1)
            try: collect(database,user_id=1,workspace_id=1,job_id=job,keyrings=keys,clock=clock)
            except AccessDenied: print("Mina after revocation: denied")
            print("refusal leaves stored export state unchanged:",snapshot(database)==before)
        else:
            work(database,workspace_id=1,job_id=job,keyrings=keys,clock=clock)
            clock.value += 60
            before=snapshot(database)
            try: collect(database,user_id=1,workspace_id=1,job_id=job,keyrings=keys,clock=clock)
            except Problem as exc: print("at exact expiry:",exc.status,exc.code)
            print("expiry gate needs no cleanup write:",snapshot(database)==before)
            with unit(database,write=True) as db:
                db.execute("""CREATE TRIGGER fail_delete BEFORE DELETE ON encrypted_exports
                    BEGIN SELECT RAISE(ABORT,'synthetic removal failure'); END""")
            clock.value += GRACE+1
            print("failed cleanup:",cleanup(database,job_id=job,clock=clock))
            stored=snapshot(database)
            row=stored["jobs"][0]
            print("state, reserved, payloads, breach:",row["state"],row["reserved"],len(stored["encrypted_exports"]),row["breached"])
            with unit(database,write=True) as db: db.execute("DROP TRIGGER fail_delete")
            print("cleanup retry:",cleanup(database,job_id=job,clock=clock))
            stored=snapshot(database)
            print("reserved, payloads, nonce history:",stored["jobs"][0]["reserved"],len(stored["encrypted_exports"]),len(stored["used_nonces"]))
            clock.value=stored["jobs"][0]["deleted_at"]+RETENTION
            print("purged at retention boundary:",purge(database,job_id=job,clock=clock))
            print("job ID never reused:",request()["job_id"]>job)


if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--stage",choices=("admission","worker","lifecycle","all"),default="all")
    chosen=parser.parse_args().stage
    for stage in (("admission","worker","lifecycle") if chosen=="all" else (chosen,)):
        print("["+stage+"]")
        run(stage)
