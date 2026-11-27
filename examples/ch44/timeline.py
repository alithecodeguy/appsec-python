"""Reorder the bounded, synthetic incident fixture; not a general production log importer."""
import argparse
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path",type=Path)
    args = parser.parse_args()
    with args.path.open("rb") as stream: raw = stream.read(1_000_001)
    if len(raw) > 1_000_000: raise ValueError("Fixture too large")
    rows = [json.loads(line) for line in raw.decode("utf-8").splitlines() if line]
    rows.sort(key=lambda row:(row["at"],0 if row["source"] == "application" else 1,row.get("event_id",0)))
    for row in rows:
        print(row["at_utc"],row["source"],row["outcome"])


if __name__ == "__main__":
    main()
