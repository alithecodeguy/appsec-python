import pytest

from access_rules import may_read


@pytest.fixture
def member_facts():
    return {
        "signed_in": True,
        "membership_active": True,
        "reader_workspace": "Alpha",
        "note_workspace": "Alpha",
        "role": "member",
    }


@pytest.mark.parametrize(
    "changes, expected",
    [
        ({"role": "member"}, True),
        ({"signed_in": False, "membership_active": False, "role": "visitor"}, False),
        ({"role": "unknown"}, False),
        ({"reader_workspace": "Beta"}, False),
        ({"membership_active": False}, False),
        ({"role": "manager"}, True),
        ({"role": "manager", "reader_workspace": "Beta"}, False),
    ],
    ids=["member", "visitor", "unknown", "other-workspace", "revoked", "manager", "other-manager"],
)
def test_read_permission(member_facts, changes, expected):
    member_facts.update(changes)
    before = member_facts.copy()

    allowed = may_read(**member_facts)

    assert allowed is expected
    assert member_facts == before
