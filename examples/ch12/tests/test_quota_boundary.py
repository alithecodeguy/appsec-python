from quota_rules import can_add_note


def test_full_workspace_refuses_another_note():
    current_count = 3
    note_limit = 3

    allowed = can_add_note(current_count=current_count, note_limit=note_limit)

    assert allowed is False
