from pathlib import Path
from tempfile import TemporaryDirectory

from contract_store import ContractError, create_note, request_export, seed, snapshot, update_note


def show_note(path, label):
    row = snapshot(path)["notes"][0]
    print(label, (row["id"], row["workspace_id"], row["owner_id"], row["title"],
                  row["state"], row["version"], row["updated_by"]))


def denied(label, operation):
    try:
        operation()
    except ContractError as exc:
        print(label, exc.status, exc.code)
    else:
        raise AssertionError("Expected contract refusal")


def main():
    with TemporaryDirectory(prefix="casebook-contract-") as folder:
        path = Path(folder) / "contract.sqlite3"
        seed(path)
        show_note(path, "initial:")
        before = snapshot(path)
        denied("unknown:", lambda: update_note(path, actor_id=1, workspace_id=1, note_id=101,
                payload={"title": "Wrong", "titel": "typo", "expected_version": 1}))
        print("unchanged after unknown:", snapshot(path) == before)
        denied("server field:", lambda: update_note(path, actor_id=1, workspace_id=1, note_id=101,
                payload={"owner_id": 2, "title": "Wrong", "expected_version": 1}))
        print("unchanged after server field:", snapshot(path) == before)
        status, created = create_note(path, actor_id=1, workspace_id=1,
                                      payload={"title": "برنامه انتشار"})
        print("created:", status, created["id"], created["owner_id"], created["title"])
        patch = {"title": "Release plan v2", "expected_version": 1}
        print("update:", update_note(path, actor_id=3, workspace_id=1, note_id=101, payload=patch)[0])
        show_note(path, "stored:")
        accepted = snapshot(path)
        denied("repeat patch:", lambda: update_note(path, actor_id=3, workspace_id=1,
                                                    note_id=101, payload=patch))
        print("unchanged after repeat:", snapshot(path) == accepted)
        denied("transition:", lambda: update_note(path, actor_id=3, workspace_id=1, note_id=101,
                                                 payload={"state": "open", "expected_version": 2}))
        show_note(path, "after invalid transition:")
        print("unchanged after transition:", snapshot(path) == accepted)
        denied("Ravi to Alpha:", lambda: update_note(path, actor_id=2, workspace_id=1,
                                                    note_id=101, payload=patch))
        first = request_export(path, actor_id=1, workspace_id=1, key="export-001",
                               payload={"note_ids": [101]})
        stored = snapshot(path)
        second = request_export(path, actor_id=1, workspace_id=1, key="export-001",
                                payload={"note_ids": [101]})
        print("export:", first)
        print("same reply:", second == first)
        print("same stored rows:", snapshot(path) == stored)
        print("job rows:", len(snapshot(path)["exports"]))
        denied("changed replay:", lambda: request_export(path, actor_id=1, workspace_id=1,
                key="export-001", payload={"note_ids": [101, created["id"]]}))
        print("unchanged after conflict:", snapshot(path) == stored)


if __name__ == "__main__":
    main()
