"""Local partner access-token verifier, not a complete OIDC login client."""
import time

import jwt

from claims_policy import AUDIENCE, ISSUER, ClaimError, check_claims


class TokenRejected(Exception):
    pass


def verify_access_token(encoded, trusted_keys):
    if not isinstance(encoded, str) or len(encoded) > 8192:
        raise TokenRejected("invalid_token")
    try:
        header = jwt.get_unverified_header(encoded)
        # Header data is untrusted. It may select only an already trusted local key.
        if (set(header) - {"alg", "typ", "kid"}
                or header.get("alg") != "RS256" or header.get("typ") != "at+jwt"):
            raise TokenRejected("invalid_token")
        kid = header.get("kid")
        if not isinstance(kid, str) or kid not in trusted_keys:
            raise TokenRejected("invalid_token")
        claims = jwt.decode(
            encoded, trusted_keys[kid], algorithms=["RS256"],
            issuer=ISSUER, audience=AUDIENCE, leeway=0,
            options={"require": ["iss", "aud", "sub", "iat", "nbf", "exp", "jti",
                                 "client_id", "scope"], "strict_aud": True},
        )
        return check_claims(claims, int(time.time()))
    except (jwt.InvalidTokenError, ClaimError) as exc:
        raise TokenRejected("invalid_token") from exc
