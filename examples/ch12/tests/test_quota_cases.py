import pytest

from quota_rules import can_add_note


@pytest.mark.parametrize(
    "current_count, expected",
    [(0, True), (2, True), (3, False), (4, False)],
)
def test_quota_capacity(current_count, expected):
    assert can_add_note(current_count=current_count, note_limit=3) is expected


@pytest.mark.parametrize("current_count", [None, -1, True, "2", 2.5])
def test_invalid_count_is_rejected(current_count):
    with pytest.raises(ValueError, match="current_count must be a nonnegative integer"):
        can_add_note(current_count=current_count)


@pytest.mark.parametrize("note_limit", [0, None, True])
def test_invalid_limit_is_rejected(note_limit):
    with pytest.raises(ValueError, match="note_limit must be a positive integer"):
        can_add_note(current_count=2, note_limit=note_limit)
