from datetime import datetime
import unittest

from examples.ch42 import capstone as app
from examples.ch44.rehearsal import BASE, overdue, run_scenario


class RecoveryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = run_scenario()  # One disposable incident; tests inspect its recorded results only.

    def test_held_subject_is_not_promoted_by_recovery(self):
        self.assertEqual(self.report["production_decision"],"HOLD")
        self.assertFalse(self.report["production_resume"])
        self.assertEqual(len(self.report["artifact_sha256"]),64)

    def test_timeline_distinguishes_effective_expiry_and_later_event(self):
        rows = self.report["timeline_input"]
        self.assertNotEqual([r["at"] for r in rows],sorted(r["at"] for r in rows))
        alpha_expired = [r for r in rows if r["source"] == "application" and r["job_id"] == 1 and r["outcome"] == "expired"]
        self.assertEqual(alpha_expired[0]["at"],BASE+62)
        self.assertEqual(self.report["states"]["first_cleanup_failure"]["jobs"][0]["closed_at"],BASE+60)
        for row in rows:
            self.assertEqual(int(datetime.fromisoformat(row["at_utc"].replace("Z","+00:00")).timestamp()),row["at"])

    def test_detector_does_not_trust_stale_breach_flag(self):
        self.assertEqual(self.report["detection"],{"overdue":True,"stored_breach_flag":0,"unsafe_backup_payloads":2})

    def test_failed_removal_keeps_copy_capacity_and_breach_survives_success(self):
        failed = self.report["states"]["deadline_failure"]
        repaired = self.report["states"]["live_repaired"]
        self.assertEqual((failed["payload_rows"],failed["jobs"][0]["reserved"]),(1,1))
        self.assertIsNone(failed["jobs"][0]["deleted_at"])
        self.assertEqual((repaired["payload_rows"],repaired["jobs"][0]["reserved"]),(0,0))
        self.assertEqual(repaired["jobs"][0]["breached"],1)
        self.assertEqual(repaired["jobs"][0]["deleted_at"],BASE+971)
        self.assertEqual(repaired["jobs"][0]["expires_at"],BASE+60)

    def test_backup_restore_is_quarantined_and_history_reconciled(self):
        before = self.report["states"]["quarantine_before_reconciliation"]
        after = self.report["states"]["quarantine_reconciled"]
        self.assertEqual((before["payload_rows"],before["nonce_rows"]),(2,2))
        self.assertEqual((after["payload_rows"],after["nonce_rows"]),(0,3))
        stale = next(r for r in self.report["timeline_input"] if r["outcome"] == "unsafe_restore_quarantined")
        self.assertTrue(stale["stale_mina_active"])
        self.assertEqual([j["deleted_at"] for j in after["jobs"]],[BASE+971,BASE+61])
        self.assertTrue(self.report["cleanup_replay_unchanged"])

    def test_recovery_checks_positive_tenant_path_and_negative_paths(self):
        probes = {r["probe"]:r for r in self.report["probes"]}
        expected = {"ravi_before_expiry":200,"mina_after_revocation":404,"ravi_at_expiry":410,
                    "stale_restore_at_real_time":410,"recovered_mina":404,"recovered_ravi_old_export":410,
                    "lee_beta":404,"anonymous_alpha":403,"recovered_ravi_fresh":200,"mina_beta_fresh":404}
        self.assertEqual({name:r["status"] for name,r in probes.items()},expected)
        self.assertEqual((probes["recovered_ravi_fresh"]["workspace_id"],probes["recovered_ravi_fresh"]["note_ids"]),(2,[202]))
        for name,row in probes.items():
            if row["status"] != 200: self.assertEqual(row["bytes_returned"],0,name)

    def test_duplicate_replay_and_local_copy_inventory(self):
        self.assertTrue(self.report["duplicate_unchanged"])
        self.assertTrue(self.report["source_notes_unchanged"])
        self.assertEqual(self.report["copy_inventory"],{"live_payload_rows":0,"restored_payload_rows":0,"unsafe_backup_exists":False})
        self.assertEqual(self.report["final"]["nonce_rows"],4)
        self.assertEqual([j["id"] for j in self.report["final"]["jobs"]],[1,2,3])

    def test_metadata_retention_is_not_reset_by_restore_or_retry(self):
        alpha,beta,_ = self.report["final"]["jobs"]
        self.assertEqual(alpha["retain_until"],BASE+971+app.RETENTION)
        self.assertEqual(beta["retain_until"],BASE+61+app.RETENTION)

    def test_shorter_retention_proposal_requires_earlier_detection(self):
        proposal = self.report["policy_change"]
        self.assertTrue(proposal["proposal_only"])
        self.assertFalse(proposal["r1_overdue"])
        self.assertTrue(proposal["proposed_overdue"])
        self.assertEqual(app.GRACE,900)  # The held candidate was NOT silently changed.
        job = self.report["states"]["first_cleanup_failure"]["jobs"][0]
        self.assertFalse(overdue(job,now=BASE+360,grace=300,payload_present=True))
        self.assertTrue(overdue(job,now=BASE+361,grace=300,payload_present=True))
        self.assertFalse(overdue(job,now=BASE+361,grace=300,payload_present=False))
        with self.assertRaises(ValueError): overdue(job,now=BASE+361,grace=True,payload_present=True)


if __name__ == "__main__":
    unittest.main()
