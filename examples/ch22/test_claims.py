import unittest

from claims_policy import ClaimError, FIXTURE_NOW, check_claims, fixture_claims


class ClaimPolicyTests(unittest.TestCase):
    def test_valid_fixture(self):
        self.assertEqual(check_claims(fixture_claims(), FIXTURE_NOW), "idp-mina-101")

    def assert_refused(self, reason, claims, now=FIXTURE_NOW):
        with self.assertRaises(ClaimError) as caught:
            check_claims(claims, now)
        self.assertEqual(str(caught.exception), reason)

    def test_wrong_audience(self):
        self.assert_refused("wrong_audience", fixture_claims(aud="another-api"))
        self.assert_refused("wrong_audience", fixture_claims(aud=["https://api.casebook.example/"]))

    def test_expiry_boundary_with_controlled_time(self):
        claims = fixture_claims()
        self.assertEqual(check_claims(claims, claims["exp"] - 1), "idp-mina-101")
        self.assert_refused("expired", claims, claims["exp"])
        self.assert_refused("expired", claims, claims["exp"] + 1)
        self.assert_refused("expired", fixture_claims(iat=FIXTURE_NOW - 100,
                            nbf=FIXTURE_NOW - 100, exp=FIXTURE_NOW - 1))

    def test_issuer_and_client_are_fixed(self):
        self.assert_refused("wrong_issuer", fixture_claims(iss="https://other.example/"))
        self.assert_refused("wrong_client", fixture_claims(client_id="other-client"))

    def test_future_time_and_long_lifetime(self):
        self.assert_refused("not_yet_valid", fixture_claims(iat=FIXTURE_NOW + 1,
                            nbf=FIXTURE_NOW + 1, exp=FIXTURE_NOW + 301))
        self.assert_refused("lifetime_too_long", fixture_claims(exp=FIXTURE_NOW + 291))
        self.assert_refused("invalid_time_order", fixture_claims(exp=FIXTURE_NOW - 20))

    def test_time_types_are_strict_and_expiry_is_required(self):
        for value in (True, "1795683600", 1795683600.0, None):
            self.assert_refused("invalid_time_type", fixture_claims(exp=value))
        claims = fixture_claims()
        del claims["exp"]
        self.assert_refused("invalid_time_type", claims)

    def test_subject_and_scope_do_not_expand(self):
        self.assert_refused("invalid_subject_or_id", fixture_claims(sub=""))
        self.assert_refused("invalid_scope", fixture_claims(scope="notes:read notes:write"))
        self.assert_refused("invalid_subject_or_id", fixture_claims(jti=None))
        self.assert_refused("unsupported_token_binding", fixture_claims(cnf={"jkt": "fixture"}))


if __name__ == "__main__":
    unittest.main()
