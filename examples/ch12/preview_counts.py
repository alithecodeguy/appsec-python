from itertools import islice
from pathlib import Path

from note_streams import read_note_records


def count_records(path, *, limit=3):
    """Count at most limit JSON-line records."""
    if type(limit) is not int or limit < 0:
        raise ValueError("limit must be a nonnegative integer")
    with path.open("r", encoding="utf-8") as source:
        records = read_note_records(source)
        return sum(1 for record in islice(records, limit))


if __name__ == "__main__":
    print("Preview count", count_records(Path("notes.jsonl")))
