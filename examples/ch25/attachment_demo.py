from io import BytesIO
import json
from pathlib import Path
from tempfile import TemporaryDirectory

from examples.ch23.authorization_service import AccessDenied, revoke_member
from examples.ch25.attachments import MAX_BYTES, Rejected, initialize, inventory, retrieve, upload
from examples.ch25.archive_policy import review_manifest


with TemporaryDirectory(prefix="casebook-attachments-") as folder:
    database = Path(folder) / "casebook.sqlite3"
    root = Path(folder) / "private"
    initialize(database, root)

    def send(data, name="report.txt"):
        return upload(database, root, user_id=1, workspace_id=1, note_id=101,
                      display_name=name, media_type="text/plain", stream=BytesIO(data))

    first, second = send(b"Alpha report one\n"), send(b"Alpha report two\n")
    print("same display names:", [row["display_name"] for row in inventory(database, root)["rows"]])
    print("independent keys:", first != second)
    print("original bytes retained:", retrieve(database, root, user_id=1, key=first)[1] == b"Alpha report one\n")
    boundary = send(b"A" * MAX_BYTES)
    print("exact boundary stored:", len(retrieve(database, root, user_id=1, key=boundary)[1]))
    for label, data in (("over boundary", b"B" * (MAX_BYTES + 1)),
                        ("rejected text", b"valid prefix\x00rejected")):
        before = inventory(database, root)
        try:
            send(data)
        except Rejected as exc:
            print(label + ":", str(exc))
        else:
            raise AssertionError("Expected rejection")
        print("same stored inventory:", inventory(database, root) == before)
    state = inventory(database, root)
    print("final rows, objects, staged:", len(state["rows"]), len(state["objects"]), len(state["staging"]))
    try:
        retrieve(database, root, user_id=2, key=first)
    except AccessDenied:
        print("Ravi Alpha retrieval: denied")
    revoke_member(database, actor_id=3, workspace_id=1, target_user_id=1)
    try:
        retrieve(database, root, user_id=1, key=first)
    except AccessDenied:
        print("Mina after revocation: denied")
    manifest = [
        {"name":"report.txt", "kind":"file", "compressed":16, "expanded":32},
        {"name":"../outside.txt", "kind":"file", "compressed":8, "expanded":16},
        {"name":"team/link.txt", "kind":"symlink", "compressed":1, "expanded":1},
    ]
    print("manifest:", review_manifest(json.dumps(manifest).encode()))
