from pathlib import Path
from tempfile import TemporaryDirectory

from examples.ch23.authorization_service import (
    build_export, detail_view, download_export, list_view, response,
    revoke_member, seed, snapshot,
)

with TemporaryDirectory(prefix="casebook-appendix-notebook-") as folder:
    database = Path(folder)/"casebook.sqlite3"
    seed(database)
    artifact = build_export(database, user_id=1, workspace_id=1, note_ids=[101])
    print("before own retrieval:", response(lambda: download_export(database, user_id=1, artifact=artifact))[0])
    notes_before = snapshot(database)["notes"]
    revoke_member(database, actor_id=3, workspace_id=1, target_user_id=1)
    membership = next(row for row in snapshot(database)["memberships"]
                      if row["workspace_id"] == 1 and row["user_id"] == 1)
    print("stored Mina active:", membership["active"])
    print("after detail:", detail_view(database, user_id=1, workspace_id=1, note_id=101)[0])
    print("after own artifact:", response(lambda: download_export(database, user_id=1, artifact=artifact))[0])
    print("Ravi Beta:", list_view(database, user_id=2, workspace_id=2)[0])
    print("Lee Beta:", list_view(database, user_id=3, workspace_id=2)[0])
    print("source notes unchanged:", snapshot(database)["notes"] == notes_before)
