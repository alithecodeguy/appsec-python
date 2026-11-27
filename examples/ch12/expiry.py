from collections.abc import Callable
from datetime import datetime, timezone


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def token_expired(
    expires_at: datetime,
    *,
    clock: Callable[[], datetime] = utc_now,
) -> bool:
    if expires_at.tzinfo is None or expires_at.utcoffset() is None:
        raise ValueError("expires_at must be timezone-aware")
    now = clock()
    if now.tzinfo is None or now.utcoffset() is None:
        raise ValueError("clock must return a timezone-aware datetime")
    return now >= expires_at
