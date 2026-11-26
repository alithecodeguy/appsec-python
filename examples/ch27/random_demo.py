import secrets

# These are disposable examples, never application credentials or printed secrets.
identifier=secrets.token_urlsafe(16)
bearer_token=secrets.token_urlsafe(32)
webhook_key=secrets.token_bytes(32)
print("identifier has a value:",bool(identifier))
print("token has a value:",bool(bearer_token))
print("HMAC key bytes:",len(webhook_key))
