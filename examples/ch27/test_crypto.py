import json
from pathlib import Path
import sqlite3
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from examples.ch23.authorization_service import AccessDenied,revoke_member,unit
from examples.ch26.integrations import (
    FIXTURE_KEYS,FIXTURE_NOW,Refused,handle_webhook,initialize as initialize_events,inventory as event_inventory,signature,
)
from examples.ch27.export_crypto import (
    CannotOpen,Keyring,create_export,decrypt,initialize,inventory,read_export,rotate_export,
)


class CryptoTests(unittest.TestCase):
    def setUp(self):
        self.folder=TemporaryDirectory(prefix="casebook-crypto-test-")
        self.addCleanup(self.folder.cleanup)
        self.db=Path(self.folder.name)/"casebook.sqlite3"
        initialize(self.db)
        self.old,self.new=AESGCM.generate_key(bit_length=256),AESGCM.generate_key(bit_length=256)
        self.first=Keyring({"export-old":self.old},"export-old")
        self.overlap=Keyring({"export-old":self.old,"export-new":self.new},"export-new")
        self.new_only=Keyring({"export-new":self.new},"export-new")
        self.export=create_export(self.db,user_id=1,workspace_id=1,note_ids=[101],keyring=self.first)

    def read(self,ring=None,user=1):
        return read_export(self.db,user_id=user,export_id=self.export,keyring=ring or self.first)

    def test_round_trip_permissions_and_revocation(self):
        plaintext=self.read()
        self.assertEqual(json.loads(plaintext)["notes"][0]["body"],"Alpha private fixture")
        self.assertNotIn(plaintext,inventory(self.db)["encrypted_exports"][0]["ciphertext"])
        for user in (None,2,3):
            with self.assertRaises(AccessDenied): self.read(user=user)
        before=inventory(self.db)
        revoke_member(self.db,actor_id=3,workspace_id=1,target_user_id=1)
        with self.assertRaises(AccessDenied): self.read()
        self.assertEqual(inventory(self.db),before)

    def test_wrong_key_nonce_ciphertext_and_context_fail_without_writes(self):
        record=inventory(self.db)["encrypted_exports"][0]
        wrong=Keyring({"export-old":self.new},"export-old")
        before=inventory(self.db)
        with self.assertRaises(CannotOpen): self.read(wrong)
        for field,value in (("workspace_id",2),("requested_by",3),("generation",2),
                            ("key_id","unknown"),("nonce",b""),("ciphertext",b"short"),
                            ("nonce","not-byte-data"),("ciphertext","not-byte-data"),
                            ("nonce",bytes([record["nonce"][0]^1])+record["nonce"][1:]),
                            ("ciphertext",bytes([record["ciphertext"][0]^1])+record["ciphertext"][1:])):
            with self.subTest(field=field),self.assertRaises(CannotOpen):
                decrypt({**record,field:value},self.first)
        self.assertEqual(inventory(self.db),before)

    def test_cross_record_ciphertext_substitution_fails(self):
        other=create_export(self.db,user_id=2,workspace_id=2,note_ids=[202],keyring=self.first)
        record,second=inventory(self.db)["encrypted_exports"]
        with unit(self.db,write=True) as db:
            db.execute("UPDATE encrypted_exports SET nonce=?,ciphertext=? WHERE id=?",
                       (second["nonce"],second["ciphertext"],self.export))
        before=inventory(self.db)
        with self.assertRaises(CannotOpen): self.read()
        self.assertEqual(inventory(self.db),before)

    def test_rotation_migrates_before_retiring_old_key(self):
        plaintext=self.read()
        old_record=inventory(self.db)["encrypted_exports"][0]
        with self.assertRaises(CannotOpen): self.read(self.new_only)
        rotate_export(self.db,export_id=self.export,keyring=self.overlap)
        current=inventory(self.db)["encrypted_exports"][0]
        self.assertEqual((current["key_id"],current["generation"]),("export-new",2))
        self.assertNotEqual(current["nonce"],old_record["nonce"])
        self.assertEqual(self.read(self.new_only),plaintext)
        with self.assertRaises(CannotOpen): decrypt(old_record,self.new_only)

    def test_reused_nonce_is_refused_before_new_ciphertext_is_committed(self):
        nonce=inventory(self.db)["encrypted_exports"][0]["nonce"]
        before=inventory(self.db)
        with patch("examples.ch27.export_crypto.secrets.token_bytes",return_value=nonce):
            with self.assertRaises(sqlite3.IntegrityError):
                create_export(self.db,user_id=1,workspace_id=1,note_ids=[101],keyring=self.first)
        self.assertEqual(inventory(self.db),before)
        with self.assertRaises(ValueError): Keyring({"old":self.old,"alias":self.old},"alias")

    def test_failed_rotation_preserves_old_ciphertext_and_nonce_ledger(self):
        with unit(self.db,write=True) as db:
            db.execute("""CREATE TRIGGER fail_replace BEFORE UPDATE ON encrypted_exports
                          BEGIN SELECT RAISE(ABORT,'synthetic migration failure'); END""")
        before=inventory(self.db)
        plaintext=self.read()
        with self.assertRaises(sqlite3.IntegrityError):
            rotate_export(self.db,export_id=self.export,keyring=self.overlap)
        self.assertEqual(inventory(self.db),before)
        self.assertEqual(self.read(),plaintext)

    def test_bad_tag_blocks_rotation_and_unknown_format_has_no_fallback(self):
        record=inventory(self.db)["encrypted_exports"][0]
        with self.assertRaises(CannotOpen): decrypt({**record,"format_version":99},self.first)
        with unit(self.db,write=True) as db:
            db.execute("UPDATE encrypted_exports SET ciphertext=? WHERE id=?",(b"x"*32,self.export))
        before=inventory(self.db)
        with self.assertRaises(CannotOpen): rotate_export(self.db,export_id=self.export,keyring=self.overlap)
        self.assertEqual(inventory(self.db),before)

    def test_webhook_key_change_preserves_authentication_and_duplicate_policy(self):
        path=Path(self.folder.name)/"events.sqlite3"
        initialize_events(path)
        raw=(Path(__file__).parents[1]/"ch26/fixtures/report-ready.json").read_bytes()
        def deliver(body,kid,keys):
            stamp=str(FIXTURE_NOW)
            return handle_webhook(path,partner_id="reports",raw=body,timestamp=stamp,key_id=kid,
                supplied_signature=signature(FIXTURE_KEYS["reports"][kid],"reports",stamp,raw),
                keyrings=keys,now=FIXTURE_NOW)
        self.assertEqual(deliver(raw,"old",FIXTURE_KEYS)[0],200)
        saved=event_inventory(path)
        new_only={"reports":{"new":FIXTURE_KEYS["reports"]["new"]}}
        with self.assertRaises(Refused): deliver(raw+b" ","old",FIXTURE_KEYS)
        with self.assertRaises(Refused): deliver(raw,"old",new_only)
        self.assertEqual(deliver(raw,"new",new_only)[0],200)
        self.assertEqual(event_inventory(path),saved)


if __name__=="__main__":
    unittest.main()
