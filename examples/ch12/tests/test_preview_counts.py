import json

import pytest

from preview_counts import count_records


def test_three_record_preview_stops_before_bad_fourth(note_inventory):
    assert count_records(note_inventory, limit=3) == 3


def test_requesting_four_reaches_invalid_json(note_inventory):
    with pytest.raises(json.JSONDecodeError):
        count_records(note_inventory, limit=4)


def test_zero_limit_does_not_parse_first_record(note_inventory):
    note_inventory.write_text("invalid JSON\n", encoding="utf-8")
    assert count_records(note_inventory, limit=0) == 0
