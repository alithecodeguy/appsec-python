"""Synthetic retention incident on the held candidate. Writes only disposable databases."""
import argparse
from contextlib import closing, redirect_stdout
from datetime import datetime, timezone
import hashlib
import io
import json
from pathlib import Path
import sqlite3
from tempfile import TemporaryDirectory

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from examples.ch23.authorization_service import AccessDenied, require_member, revoke_member, unit
from examples.ch27.export_crypto import Keyring, rotate_export
from examples.ch42 import capstone as app
from examples.ch42.fixtures import dummy_keyrings
from examples.ch43.check_evidence import main as check_candidate

BASE = 1795687200  # 2026-11-26 10:00:00Z, controlled scenario time, not incident discovery today.
JOB_FIELDS = ("id","requested_by","workspace_id","client_key","note_ids","created_at","expires_at",
              "closed_at","state","reserved","deleted_at","retain_until","cleanup_error","breached")


def utc(value):
    return datetime.fromtimestamp(value,timezone.utc).isoformat().replace("+00:00","Z")


def overdue(job, *, now, grace, payload_present):
    # Read-only policy assessment. grace is a reviewed exercise input, never client authority.
    if type(grace) is not int or grace < 0: raise ValueError("invalid grace")
    return payload_present and now > app.access_end(job)+grace


def backup_to(source,destination):
    if Path(destination).exists(): raise ValueError("Use a fresh quarantine path")
    with closing(sqlite3.connect(source,autocommit=True)) as src:
        with closing(sqlite3.connect(destination,autocommit=True)) as dst:
            src.backup(dst)


def count_payloads(path):
    with unit(path) as db:
        return db.execute("SELECT count(*) FROM encrypted_exports").fetchone()[0]


def authority_manifest(database):
    # Restricted in-memory current facts. No keys or payload bytes. Not an untrusted import format.
    with unit(database) as db:
        assert db.execute("SELECT count(*) FROM encrypted_exports").fetchone()[0] == 0
        jobs = [dict(row) for row in db.execute("SELECT * FROM jobs ORDER BY id")]
        assert all(j["state"] in app.TERMINAL and j["reserved"] == 0 for j in jobs)
        high = db.execute("SELECT seq FROM sqlite_sequence WHERE name='jobs'").fetchone()[0]
        return {"users":[tuple(r) for r in db.execute("SELECT id,active FROM users ORDER BY id")],
            "memberships":[tuple(r) for r in db.execute("SELECT * FROM memberships ORDER BY 1,2")],
            "jobs":jobs,"events":[tuple(r) for r in db.execute("SELECT * FROM export_events ORDER BY id")],
            "nonces":[tuple(r) for r in db.execute("SELECT * FROM used_nonces ORDER BY 1,2")],"job_high_water":high}


def reconcile_quarantine(database,current):
    # Deliberately narrow recovery: discard ALL restored temporary exports, preserve current terminal facts.
    # Caller must keep admission/delivery paused and authenticate the authoritative manifest in deployment.
    with unit(database,write=True) as db:
        db.execute("DELETE FROM result_slots")
        db.execute("DELETE FROM encrypted_exports")
        db.execute("DELETE FROM export_events")
        db.execute("DELETE FROM jobs")
        for user_id,active in current["users"]:
            changed = db.execute("UPDATE users SET active=? WHERE id=?",(active,user_id)).rowcount
            if changed != 1: raise ValueError("Unknown current identity")
        db.execute("DELETE FROM memberships")
        db.executemany("INSERT INTO memberships VALUES (?,?,?,?)",current["memberships"])
        # Field/table names are fixed local constants, not manifest-supplied identifiers.
        sql = "INSERT INTO jobs ("+",".join(JOB_FIELDS)+") VALUES ("+",".join("?" for _ in JOB_FIELDS)+")"
        db.executemany(sql,[tuple(job[field] for field in JOB_FIELDS) for job in current["jobs"]])
        db.executemany("INSERT INTO export_events VALUES (?,?,?,?,?,?,?)",current["events"])
        db.executemany("INSERT OR IGNORE INTO used_nonces VALUES (?,?)",current["nonces"])
        db.execute("UPDATE sqlite_sequence SET seq=max(seq,?) WHERE name='jobs'",(current["job_high_water"],))


def verified_subject():
    root = Path(__file__).resolve().parents[2]
    with redirect_stdout(io.StringIO()): check_candidate()
    manifest = json.loads((root/"examples/ch43/evidence/candidate.json").read_text())
    # This rehearsal calls domain operations only after matching all committed candidate Python bytes.
    for name,digest in manifest["files_sha256"].items():
        if name.endswith(".py"):
            assert hashlib.sha256((root/name).read_bytes()).hexdigest() == digest,name
    decision = json.loads((root/"examples/ch43/release-decision.json").read_text())
    assert decision["decision"] == "HOLD"
    return {"source_commit":manifest["source_commit"],"artifact_sha256":manifest["artifact_sha256"],
            "production_decision":"HOLD"}


def run_scenario():
    subject = verified_subject()
    clock,keys = app.Clock(BASE),dummy_keyrings()
    observations,probes,states = [],[],{}
    controls = {"paused":False}
    def observe(outcome,**facts):
        observations.append({"source":"harness","at":clock(),"outcome":outcome,**facts})
    def record_probe(name,operation):
        try:
            payload = operation()
        except (AccessDenied,app.Problem) as exc:
            result = {"probe":name,"status":exc.status,"bytes_returned":0}
        else:
            document = json.loads(payload)
            result = {"probe":name,"status":200,"workspace_id":document["workspace_id"],
                      "note_ids":[r["id"] for r in document["notes"]]}
        probes.append(result)
        observe("controlled_collection",**result)
        return result
    def admit(database,**intent):
        if controls["paused"]: raise app.Problem(503,"rehearsal_paused")
        return app.request_export(database,clock=clock,**intent)
    def view(database):
        snapshot = app.snapshot(database)
        return {"jobs":[{f:j[f] for f in ("id","workspace_id","state","expires_at","closed_at","reserved",
                                        "deleted_at","retain_until","cleanup_error","breached")} for j in snapshot["jobs"]],
                "payload_rows":len(snapshot["encrypted_exports"]),"nonce_rows":len(snapshot["used_nonces"])}
    with TemporaryDirectory(prefix="casebook-ch44-") as folder:
        live,unsafe,restored = (Path(folder)/name for name in ("live.sqlite3","unsafe-backup.sqlite3","quarantine.sqlite3"))
        app.initialize(live)
        with unit(live) as db:
            originals = [tuple(r) for r in db.execute("SELECT * FROM notes ORDER BY id")]
        alpha = admit(live,user_id=1,workspace_id=1,body={"note_ids":[101]},client_key="alpha-incident")["job_id"]
        beta = admit(live,user_id=2,workspace_id=2,body={"note_ids":[202]},client_key="beta-control")["job_id"]
        clock.value = BASE+5
        app.work(live,workspace_id=1,job_id=alpha,keyrings=keys,clock=clock)
        clock.value = BASE+6
        app.work(live,workspace_id=2,job_id=beta,keyrings=keys,clock=clock)
        clock.value = BASE+7
        backup_to(live,unsafe)  # INTENTIONALLY WRONG policy fixture: includes temporary export payloads.
        observe("unsafe_backup_created",payload_rows=count_payloads(unsafe),backup_is_negative_control=True)
        clock.value = BASE+8
        old = keys[1]
        keys[1] = Keyring({**old.keys,"export-w1-rotation-demo":AESGCM.generate_key(bit_length=256)},"export-w1-rotation-demo")
        export_id = app.snapshot(live)["encrypted_exports"][0]["id"]
        rotate_export(live,export_id=export_id,keyring=keys[1])
        observe("dummy_key_rotation",nonce_rows=len(app.snapshot(live)["used_nonces"]))
        clock.value = BASE+10
        revoke_member(live,actor_id=3,workspace_id=1,target_user_id=1)
        observe("membership_revoked",workspace_id=1,user_id=1)
        clock.value = BASE+59
        record_probe("ravi_before_expiry",lambda:app.collect(live,user_id=2,workspace_id=2,job_id=beta,keyrings=keys,clock=clock))
        clock.value = BASE+60
        record_probe("mina_after_revocation",lambda:app.collect(live,user_id=1,workspace_id=1,job_id=alpha,keyrings=keys,clock=clock))
        record_probe("ravi_at_expiry",lambda:app.collect(live,user_id=2,workspace_id=2,job_id=beta,keyrings=keys,clock=clock))
        with unit(live,write=True) as db:
            db.execute("""CREATE TRIGGER fail_alpha_delete BEFORE DELETE ON encrypted_exports
                WHEN OLD.workspace_id=1 BEGIN SELECT RAISE(ABORT,'synthetic storage failure'); END""")
        clock.value = BASE+61
        assert app.cleanup(live,job_id=beta,clock=clock) == "deleted"
        clock.value = BASE+62
        assert app.cleanup(live,job_id=alpha,clock=clock) == "retry"
        states["first_cleanup_failure"] = view(live)
        clock.value = BASE+961  # One second beyond normal access end plus the 15-minute grace.
        alpha_row = app.snapshot(live)["jobs"][0]
        detection = {"overdue":overdue(alpha_row,now=clock(),grace=app.GRACE,payload_present=True),
                     "stored_breach_flag":alpha_row["breached"],"unsafe_backup_payloads":count_payloads(unsafe)}
        observe("retention_detected",**detection)
        controls["paused"] = True
        try: admit(live,user_id=2,workspace_id=2,body={"note_ids":[202]},client_key="paused")
        except app.Problem as exc: observe("admission_paused",status=exc.status)
        else: raise AssertionError("Containment harness did not stop admission")
        clock.value = BASE+962
        assert app.cleanup(live,job_id=alpha,clock=clock) == "retry"
        states["deadline_failure"] = view(live)
        clock.value = BASE+970
        with unit(live,write=True) as db: db.execute("DROP TRIGGER fail_alpha_delete")
        observe("synthetic_fault_removed")
        clock.value = BASE+971
        assert app.cleanup(live,job_id=alpha,clock=clock) == "deleted"
        states["live_repaired"] = view(live)
        clock.value = BASE+972
        current = authority_manifest(live)
        # Hash restricted current facts without retaining nonce values or private ownership rows in reports.
        normalized = {**current,"nonces":[[kid,nonce.hex()] for kid,nonce in current["nonces"]]}
        authority_digest = hashlib.sha256(json.dumps(normalized,sort_keys=True,separators=(",",":")).encode()).hexdigest()
        clock.value = BASE+973
        backup_to(unsafe,restored)
        with unit(restored) as db:
            stale_mina = require_member(db,1,1) == "member"
        states["quarantine_before_reconciliation"] = view(restored)
        observe("unsafe_restore_quarantined",stale_mina_active=stale_mina,restored_payload_rows=count_payloads(restored))
        # Diagnostic core probe only; there is no listener or user traffic on quarantine.
        record_probe("stale_restore_at_real_time",lambda:app.collect(restored,user_id=1,workspace_id=1,job_id=alpha,keyrings=keys,clock=clock))
        clock.value = BASE+974
        reconcile_quarantine(restored,current)
        states["quarantine_reconciled"] = view(restored)
        settled = app.snapshot(restored)
        assert app.cleanup(restored,job_id=alpha,clock=clock) == "deleted"
        assert app.snapshot(restored) == settled
        observe("current_facts_reconciled",restored_payload_rows=count_payloads(restored),nonce_rows=len(app.snapshot(restored)["used_nonces"]))
        clock.value = BASE+975
        record_probe("recovered_mina",lambda:app.collect(restored,user_id=1,workspace_id=1,job_id=alpha,keyrings=keys,clock=clock))
        record_probe("recovered_ravi_old_export",lambda:app.collect(restored,user_id=2,workspace_id=2,job_id=beta,keyrings=keys,clock=clock))
        record_probe("lee_beta",lambda:app.collect(restored,user_id=3,workspace_id=2,job_id=beta,keyrings=keys,clock=clock))
        record_probe("anonymous_alpha",lambda:app.collect(restored,user_id=None,workspace_id=1,job_id=alpha,keyrings=keys,clock=clock))
        controls["paused"] = False  # Limited local positive recovery test, NOT a production resume.
        fresh = admit(restored,user_id=2,workspace_id=2,body={"note_ids":[202]},client_key="fresh-beta")["job_id"]
        assert fresh > max(j["id"] for j in current["jobs"])
        assert app.work(restored,workspace_id=2,job_id=fresh,keyrings=keys,clock=clock) == "created"
        record_probe("recovered_ravi_fresh",lambda:app.collect(restored,user_id=2,workspace_id=2,job_id=fresh,keyrings=keys,clock=clock))
        record_probe("mina_beta_fresh",lambda:app.collect(restored,user_id=1,workspace_id=2,job_id=fresh,keyrings=keys,clock=clock))
        before = app.snapshot(restored)
        assert app.work(restored,workspace_id=2,job_id=fresh,keyrings=keys,clock=clock) == "duplicate"
        assert app.snapshot(restored) == before
        clock.value = BASE+976
        unsafe.unlink()  # Delete the known negative-control backup, not merely the restored live rows.
        observe("unsafe_backup_removed",backup_exists=unsafe.exists())
        clock.value = BASE+1035  # Fresh Beta result reaches its original 60-second lifetime.
        assert app.cleanup(restored,job_id=fresh,clock=clock) == "deleted"
        final = view(restored)
        with unit(restored) as db:
            assert [tuple(r) for r in db.execute("SELECT * FROM notes ORDER BY id")] == originals
            audit = [dict(r) for r in db.execute("SELECT * FROM export_events ORDER BY id")]
        copy_inventory = {"live_payload_rows":count_payloads(live),"restored_payload_rows":count_payloads(restored),
                          "unsafe_backup_exists":unsafe.exists()}
        timeline = [{"source":"application","at":row["at"],"event_id":row["id"],"job_id":row["job_id"],
                     "workspace_id":row["workspace_id"],"outcome":row["outcome"]} for row in audit] + observations
        timeline.sort(key=lambda row:(row["at"],0 if row["source"] == "application" else 1,row.get("event_id",0)))
        for row in timeline: row["at_utc"] = utc(row["at"])
        # Intentionally nonchronological fixture; readers must reconstruct UTC order, not trust file order.
        unsorted = timeline[::2]+timeline[1::2]
        proposal = {"proposal_only":True,"access_end":utc(BASE+60),"r1_grace_seconds":900,"proposed_grace_seconds":300,
                    "r1_delete_by":utc(BASE+960),"proposed_delete_by":utc(BASE+360),
                    "sample_at":utc(BASE+361),"r1_overdue":overdue(alpha_row,now=BASE+361,grace=900,payload_present=True),
                    "proposed_overdue":overdue(alpha_row,now=BASE+361,grace=300,payload_present=True)}
        return {"kind":"executed synthetic local rehearsal; no production incident or deployment",**subject,
                "scenario_origin_utc":utc(BASE),"detection":detection,"states":states,"probes":probes,
                "current_authority_manifest_sha256":authority_digest,"copy_inventory":copy_inventory,
                "final":final,"duplicate_unchanged":True,"cleanup_replay_unchanged":True,"source_notes_unchanged":True,
                "policy_change":proposal,"timeline_input":unsorted,"production_resume":False}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out",type=Path)
    args = parser.parse_args()
    if args.out is not None and args.out.exists(): raise ValueError("Use a new evidence directory")
    result = run_scenario()
    if args.out is not None:
        args.out.mkdir(parents=True,exist_ok=False)
        (args.out/"incident-evidence.json").write_text(json.dumps(result,indent=2)+"\n")
        (args.out/"audit-input.jsonl").write_text("".join(json.dumps(row)+"\n" for row in result["timeline_input"]))
    print("production decision:",result["production_decision"])
    print("overdue at detection; stored breach flag:",result["detection"]["overdue"],result["detection"]["stored_breach_flag"])
    print("unsafe backup payload rows:",result["detection"]["unsafe_backup_payloads"])
    print("live Alpha breach retained:",result["states"]["live_repaired"]["jobs"][0]["breached"])
    print("restored payloads before/after reconciliation:",result["states"]["quarantine_before_reconciliation"]["payload_rows"],result["states"]["quarantine_reconciled"]["payload_rows"])
    print("nonce history before/after reconciliation:",result["states"]["quarantine_before_reconciliation"]["nonce_rows"],result["states"]["quarantine_reconciled"]["nonce_rows"])
    print("recovery probes:",[(p["probe"],p["status"]) for p in result["probes"] if p["probe"].startswith("recovered_")])
    print("final managed payload rows:",result["copy_inventory"]["live_payload_rows"],result["copy_inventory"]["restored_payload_rows"])
    print("unsafe backup removed:",not result["copy_inventory"]["unsafe_backup_exists"])
    print("duplicate state unchanged:",result["duplicate_unchanged"])
    print("retention proposal only:",result["policy_change"]["proposal_only"])
    print("production resume:",result["production_resume"])


if __name__ == "__main__":
    main()
