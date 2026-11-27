import json

import pytest


@pytest.fixture
def note_inventory(tmp_path):
    records = [
        {"id": 1, "workspace": "Alpha", "title": "Release plan"},
        {"id": 2, "workspace": "Beta", "title": "Pricing review"},
        {"id": 5, "workspace": "Alpha", "title": "برنامه انتشار"},
    ]
    text = "\n".join(json.dumps(record, ensure_ascii=False) for record in records)
    path = tmp_path / "notes.jsonl"
    path.write_text(text + "\ninvalid JSON\n", encoding="utf-8")
    return path
