from datetime import datetime, timedelta, timezone

import pytest

from expiry import token_expired


@pytest.mark.parametrize("offset, expected", [(-1, False), (0, True), (1, True)])
def test_expiry_boundary(offset, expected):
    expiry = datetime(2026, 11, 26, 12, 0, tzinfo=timezone.utc)
    instant = expiry + timedelta(seconds=offset)

    def fixed_clock():
        return instant

    assert token_expired(expiry, clock=fixed_clock) is expected


def test_naive_expiry_is_rejected():
    expiry = datetime(2026, 11, 26, 12, 0)
    with pytest.raises(ValueError, match="expires_at must be timezone-aware"):
        token_expired(expiry)


def test_naive_clock_result_is_rejected():
    expiry = datetime(2026, 11, 26, 12, 0, tzinfo=timezone.utc)

    def naive_clock():
        return datetime(2026, 11, 26, 12, 0)

    with pytest.raises(ValueError, match="clock must return a timezone-aware datetime"):
        token_expired(expiry, clock=naive_clock)
