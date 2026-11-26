"""Application claim policy. This module does NOT verify JWT signatures."""
ISSUER = "https://idp.casebook.example/"
AUDIENCE = "https://api.casebook.example/"
CLIENT_ID = "casebook-partner"
MAX_LIFETIME = 300
FIXTURE_NOW = 1795683600  # 2026-11-26 09:00:00 UTC, synthetic time only.


class ClaimError(ValueError):
    pass


def check_claims(claims, now):
    # Only the maintained JWT verifier may treat a successful result as authenticated.
    if not isinstance(claims, dict):
        raise ClaimError("invalid_claims")
    if "cnf" in claims:
        raise ClaimError("unsupported_token_binding")
    if claims.get("iss") != ISSUER:
        raise ClaimError("wrong_issuer")
    if claims.get("aud") != AUDIENCE:
        raise ClaimError("wrong_audience")
    if claims.get("client_id") != CLIENT_ID:
        raise ClaimError("wrong_client")
    for name in ("sub", "jti"):
        if not isinstance(claims.get(name), str) or not 1 <= len(claims[name]) <= 200:
            raise ClaimError("invalid_subject_or_id")
    if claims.get("scope") != "notes:read":
        raise ClaimError("invalid_scope")
    for name in ("iat", "nbf", "exp"):
        if type(claims.get(name)) is not int:
            raise ClaimError("invalid_time_type")
    if not claims["iat"] <= claims["nbf"] < claims["exp"]:
        raise ClaimError("invalid_time_order")
    if claims["exp"] - claims["iat"] > MAX_LIFETIME:
        raise ClaimError("lifetime_too_long")
    if claims["iat"] > now or claims["nbf"] > now:
        raise ClaimError("not_yet_valid")
    if now >= claims["exp"]:
        raise ClaimError("expired")
    return claims["sub"]


def fixture_claims(**changes):
    # A dictionary fixture is not a signed token and authenticates nobody.
    claims = {
        "iss": ISSUER, "aud": AUDIENCE, "sub": "idp-mina-101",
        "client_id": CLIENT_ID, "scope": "notes:read", "jti": "fixture-access-001",
        "iat": FIXTURE_NOW - 10, "nbf": FIXTURE_NOW - 10, "exp": FIXTURE_NOW + 290,
    }
    claims.update(changes)
    return claims
