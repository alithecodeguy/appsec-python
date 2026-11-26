from datetime import datetime, timezone
import unittest
from unittest.mock import patch

import jwt
from cryptography.hazmat.primitives.asymmetric import rsa

from claims_policy import FIXTURE_NOW, fixture_claims
from jwt_verifier import TokenRejected, verify_access_token


class FrozenDateTime(datetime):
    @classmethod
    def now(cls, tz=None):
        return datetime.fromtimestamp(FIXTURE_NOW, tz=tz or timezone.utc)


class JWTTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Ephemeral private keys remain in this test process; no provider is contacted.
        cls.old_private = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        cls.new_private = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        cls.keys = {"old": cls.old_private.public_key(), "new": cls.new_private.public_key()}

    def setUp(self):
        # Freeze only test clocks; all library signature/issuer/audience/time checks stay enabled.
        self.library_clock = patch("jwt.api_jwt.datetime", FrozenDateTime)
        self.policy_clock = patch("jwt_verifier.time.time", return_value=FIXTURE_NOW)
        self.library_clock.start()
        self.policy_clock.start()
        self.addCleanup(self.library_clock.stop)
        self.addCleanup(self.policy_clock.stop)

    def signed(self, claims=None, private=None, kid="old", typ="at+jwt"):
        return jwt.encode(fixture_claims() if claims is None else claims,
                          self.old_private if private is None else private, algorithm="RS256",
                          headers={"kid": kid, "typ": typ})

    def test_valid_signature_and_claims(self):
        self.assertEqual(verify_access_token(self.signed(), self.keys), "idp-mina-101")

    def test_signed_wrong_audience_is_refused(self):
        with self.assertRaises(TokenRejected):
            verify_access_token(self.signed(fixture_claims(aud="another-api")), self.keys)

    def test_signed_expired_and_exact_expiry_are_refused(self):
        for expiry in (FIXTURE_NOW - 1, FIXTURE_NOW):
            claims = fixture_claims(iat=FIXTURE_NOW - 100, nbf=FIXTURE_NOW - 100, exp=expiry)
            with self.subTest(expiry=expiry), self.assertRaises(TokenRejected):
                verify_access_token(self.signed(claims), self.keys)

    def test_wrong_signature_and_unknown_key_are_refused(self):
        with self.assertRaises(TokenRejected):
            verify_access_token(self.signed(private=self.new_private), self.keys)
        with self.assertRaises(TokenRejected):
            verify_access_token(self.signed(kid="unknown"), self.keys)

    def test_key_rotation_accepts_overlap_then_refuses_retired_key(self):
        old_token = self.signed()
        new_token = self.signed(private=self.new_private, kid="new")
        self.assertEqual(verify_access_token(old_token, self.keys), "idp-mina-101")
        self.assertEqual(verify_access_token(new_token, self.keys), "idp-mina-101")
        retired = {"new": self.new_private.public_key()}
        with self.assertRaises(TokenRejected):
            verify_access_token(old_token, retired)
        self.assertEqual(verify_access_token(new_token, retired), "idp-mina-101")

    def test_wrong_type_issuer_and_missing_expiry_are_refused(self):
        bad_claims = fixture_claims()
        del bad_claims["exp"]
        for token in (self.signed(typ="JWT"),
                      self.signed(fixture_claims(iss="https://other.example/")),
                      self.signed(bad_claims),
                      jwt.encode(fixture_claims(), self.old_private, algorithm="RS256",
                                 headers={"kid": "old", "typ": "at+jwt",
                                          "jku": "https://untrusted.example/keys"})):
            with self.assertRaises(TokenRejected):
                verify_access_token(token, self.keys)


if __name__ == "__main__":
    unittest.main()
