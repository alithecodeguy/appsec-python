from io import BytesIO
import json
import os
from pathlib import Path
import sqlite3
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from examples.ch23.authorization_service import AccessDenied
from examples.ch25.attachments import MAX_BYTES, Rejected, initialize, inventory, retrieve, upload
from examples.ch25.archive_policy import review_manifest


class AttachmentTests(unittest.TestCase):
    def setUp(self):
        self.folder = TemporaryDirectory(prefix="casebook-attachment-test-")
        self.addCleanup(self.folder.cleanup)
        self.database = Path(self.folder.name) / "casebook.sqlite3"
        self.root = Path(self.folder.name) / "private"
        initialize(self.database, self.root)

    def send(self, data, name="report.txt", stream=None):
        return upload(self.database, self.root, user_id=1, workspace_id=1, note_id=101,
                      display_name=name, media_type="text/plain",
                      stream=BytesIO(data) if stream is None else stream)

    def test_duplicate_display_names_retain_independent_bytes(self):
        first, second = self.send(b"one"), self.send(b"two")
        self.assertNotEqual(first, second)
        self.assertEqual(retrieve(self.database, self.root, user_id=1, key=first), ("report.txt", b"one"))
        self.assertEqual(retrieve(self.database, self.root, user_id=1, key=second), ("report.txt", b"two"))
        self.assertEqual(len(inventory(self.database, self.root)["objects"]), 2)

    def test_size_and_content_boundaries_leave_no_rejected_state(self):
        for size in (MAX_BYTES - 1, MAX_BYTES):
            key = self.send(b"A" * size)
            self.assertEqual(len(retrieve(self.database, self.root, user_id=1, key=key)[1]), size)
        for data in (b"A" * (MAX_BYTES + 1), b"prefix\x00bad", b"\x89PNG\r\n\x1a\n", b""):
            before = inventory(self.database, self.root)
            with self.assertRaises(Rejected):
                self.send(data)
            self.assertEqual(inventory(self.database, self.root), before)
            self.assertEqual(inventory(self.database, self.root)["staging"], [])

    def test_path_like_display_names_never_reach_storage(self):
        for name in ("../report.txt", "/report.txt", "dir\\report.txt", "C:report.txt", "bad\n.txt", "bad\ud800.txt"):
            before = inventory(self.database, self.root)
            with self.assertRaises(Rejected):
                self.send(b"data", name=name)
            self.assertEqual(inventory(self.database, self.root), before)

    def test_private_retrieval_and_unicode_name(self):
        key = self.send("گزارش".encode(), name="گزارش.txt")
        self.assertEqual(retrieve(self.database, self.root, user_id=1, key=key)[0], "گزارش.txt")
        for user in (None, 2):
            with self.assertRaises(AccessDenied):
                retrieve(self.database, self.root, user_id=user, key=key)

    def test_stream_failure_and_metadata_failure_cleanup(self):
        class BrokenStream:
            calls = 0
            def read(self, limit):
                self.calls += 1
                if self.calls == 1:
                    return b"partial"
                raise OSError("synthetic read failure")
        before = inventory(self.database, self.root)
        with self.assertRaises(OSError):
            self.send(b"", stream=BrokenStream())
        self.assertEqual(inventory(self.database, self.root), before)
        with sqlite3.connect(self.database) as db:
            db.execute("""CREATE TRIGGER fail_metadata BEFORE INSERT ON attachments
                          BEGIN SELECT RAISE(ABORT, 'synthetic metadata failure'); END""")
        with self.assertRaises(sqlite3.IntegrityError):
            self.send(b"valid")
        self.assertEqual(inventory(self.database, self.root), before)

    def test_key_collision_does_not_overwrite_or_remove_existing_file(self):
        with patch("examples.ch25.attachments.secrets.token_hex", return_value="a" * 32):
            key = self.send(b"original")
            before = inventory(self.database, self.root)
            with self.assertRaises(FileExistsError):
                self.send(b"replacement")
        self.assertEqual(inventory(self.database, self.root), before)
        self.assertEqual(retrieve(self.database, self.root, user_id=1, key=key)[1], b"original")

    def test_revocation_during_ingestion_prevents_publication(self):
        class RevokingStream(BytesIO):
            changed = False
            def read(inner, size):
                if not inner.changed:
                    with sqlite3.connect(self.database) as db:
                        db.execute("UPDATE memberships SET active=0 WHERE user_id=1 AND workspace_id=1")
                    inner.changed = True
                return super().read(size)
        with self.assertRaises(AccessDenied):
            self.send(b"", stream=RevokingStream(b"valid"))
        state = inventory(self.database, self.root)
        self.assertEqual((state["rows"], state["objects"], state["staging"]), ([], [], []))

    @unittest.skipUnless(hasattr(os, "O_NOFOLLOW"), "POSIX final-component link protection required")
    def test_final_symlink_is_not_followed_and_permissions_are_private(self):
        key = self.send(b"valid")
        target = Path(self.folder.name) / "outside.txt"
        target.write_bytes(b"outside secret")
        stored = self.root / "objects" / key
        self.assertEqual(stored.stat().st_mode & 0o777, 0o600)
        self.assertEqual(self.root.stat().st_mode & 0o777, 0o700)
        stored.unlink()
        stored.symlink_to(target)
        with self.assertRaises(OSError):
            retrieve(self.database, self.root, user_id=1, key=key)
        self.assertEqual(target.read_bytes(), b"outside secret")

    def test_manifest_policy_and_resource_budgets(self):
        def review(entries):
            return review_manifest(json.dumps(entries).encode())
        def entry(name, size=32, compressed=16, kind="file"):
            return dict(name=name, kind=kind, compressed=compressed, expanded=size)
        self.assertTrue(review([entry("report.txt"), entry("team/notes.txt")])["archive_accepted"])
        for candidate, reason in ((entry("../x.txt"), "unsafe_path"),
                                  (entry("a.txt", kind="symlink"), "not_regular_file"),
                                  (entry("a.zip"), "unsupported_entry"),
                                  (entry("a.txt", size=65), "entry_size"),
                                  (entry("a.txt", size=64, compressed=1), "expansion_ratio")):
            self.assertEqual(review([candidate])["entries"][0][1], reason)
        self.assertFalse(review([entry("a.txt"), entry("A.txt")])["archive_accepted"])
        total = review([entry("a.txt",64), entry("b.txt",64), entry("c.txt",1)])
        self.assertEqual(total["entries"][-1][1], "total_expansion")
        with self.assertRaises(ValueError):
            review([entry("a.txt", size=True)])
        with self.assertRaises(ValueError):
            review_manifest(b'[{"name":"a.txt","name":"b.txt"}]')


if __name__ == "__main__":
    unittest.main()
