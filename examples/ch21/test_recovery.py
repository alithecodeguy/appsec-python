from pathlib import Path
from tempfile import TemporaryDirectory
import sqlite3
import unittest

from recovery_lab import complete_reset, fresh_clock, request_reset, seed, snapshot, token_digest


class RecoveryTests(unittest.TestCase):
    def setUp(self):
        self.folder = TemporaryDirectory(prefix="casebook-recovery-test-")
        self.addCleanup(self.folder.cleanup)
        self.path = Path(self.folder.name) / "recovery.sqlite3"
        seed(self.path)
        self.clock = fresh_clock()
        self.outbox = []

    def issue(self):
        request_reset(self.path, "mina@example.test", self.clock, self.outbox)
        return self.outbox[-1].token

    def assert_invalid_unchanged(self, token):
        before = snapshot(self.path)
        result = complete_reset(self.path, token, "must-not-be-stored", self.clock)
        self.assertEqual(result, (400, {"error": "invalid_or_expired"}))
        self.assertEqual(snapshot(self.path), before)

    def test_known_unknown_and_ineligible_have_same_public_response(self):
        known = request_reset(self.path, "mina@example.test", self.clock, self.outbox)
        unknown = request_reset(self.path, "missing@example.test", self.clock, self.outbox)
        self.assertEqual(known, unknown)
        self.assertEqual(known[0], 202)
        self.assertEqual(len(self.outbox), 1)
        for field in ("active", "verified"):
            with sqlite3.connect(self.path) as db:
                db.execute("UPDATE accounts SET active = 1, verified = 1")
                db.execute(f"UPDATE accounts SET {field} = 0")  # Fixed test-owned identifiers only.
            self.assertEqual(request_reset(self.path, "mina@example.test", self.clock, self.outbox), known)
        self.assertEqual(len(self.outbox), 1)
        self.assertEqual(len(snapshot(self.path)["resets"]), 1)

    def test_request_does_not_change_password_or_session_epoch(self):
        before = snapshot(self.path)["accounts"]
        token = self.issue()
        after = snapshot(self.path)
        self.assertEqual(after["accounts"], before)
        self.assertEqual(after["resets"][0]["digest"], token_digest(token))
        self.assertNotIn(token, repr(after))

    def test_just_before_expiry_succeeds_and_replay_does_not_write(self):
        token = self.issue()
        self.clock.advance(899)
        result = complete_reset(self.path, token, "opaque-fixture-password-v2", self.clock)
        self.assertEqual(result[0], 200)
        saved = snapshot(self.path)
        account = saved["accounts"][0]
        self.assertEqual((account["password_hash"], account["credential_revision"], account["session_epoch"]),
                         ("opaque-fixture-password-v2", 2, 2))
        self.assertEqual(saved["resets"][0]["used_at"], self.clock.now())
        self.assert_invalid_unchanged(token)

    def test_exact_expiry_and_after_expiry_refuse_without_writes(self):
        for elapsed in (900, 901):
            with self.subTest(elapsed=elapsed):
                token = self.issue()
                self.clock.advance(elapsed)
                self.assert_invalid_unchanged(token)

    def test_malformed_and_unknown_tokens_have_same_failure(self):
        for token in (None, "", "invalid", "A" * 43):
            with self.subTest(token=token):
                self.assert_invalid_unchanged(token)

    def test_success_revokes_other_outstanding_links(self):
        first = self.issue()
        second = self.issue()
        self.assertNotEqual(first, second)
        self.assertEqual(complete_reset(self.path, first, "opaque-v2", self.clock)[0], 200)
        saved = snapshot(self.path)
        other = next(row for row in saved["resets"] if row["digest"] == token_digest(second))
        self.assertEqual(other["revoked_at"], self.clock.now())
        self.assert_invalid_unchanged(second)

    def test_changed_credential_or_disabled_account_invalidates_old_link(self):
        token = self.issue()
        with sqlite3.connect(self.path) as db:
            db.execute("UPDATE accounts SET credential_revision = credential_revision + 1")
        self.assert_invalid_unchanged(token)
        token = self.issue()
        with sqlite3.connect(self.path) as db:
            db.execute("UPDATE accounts SET active = 0")
        self.assert_invalid_unchanged(token)

    def test_missing_validated_replacement_does_not_consume_link(self):
        token = self.issue()
        before = snapshot(self.path)
        with self.assertRaises(ValueError):
            complete_reset(self.path, token, "", self.clock)
        self.assertEqual(snapshot(self.path), before)
        self.assertEqual(complete_reset(self.path, token, "opaque-v2", self.clock)[0], 200)

    def test_storage_failure_rolls_back_password_and_token_state(self):
        token = self.issue()
        with sqlite3.connect(self.path) as db:
            db.execute("""CREATE TRIGGER fail_use BEFORE UPDATE OF used_at ON resets
                          BEGIN SELECT RAISE(ABORT, 'synthetic failure'); END""")
        before = snapshot(self.path)
        with self.assertRaises(sqlite3.IntegrityError):
            complete_reset(self.path, token, "must-not-be-stored", self.clock)
        self.assertEqual(snapshot(self.path), before)


if __name__ == "__main__":
    unittest.main()
