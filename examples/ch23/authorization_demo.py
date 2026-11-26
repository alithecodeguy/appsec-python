import json
from pathlib import Path
from tempfile import TemporaryDirectory

from authorization_service import (
    build_export, detail_view, download_export, list_view, response, revoke_member, seed, snapshot,
)


with TemporaryDirectory(prefix="casebook-authorization-") as folder:
    path = Path(folder) / "authorization.sqlite3"
    seed(path)
    print("Mina Alpha list:", list_view(path, user_id=1, workspace_id=1))
    print("Mina Alpha detail:", detail_view(path, user_id=1, workspace_id=1, note_id=101))
    print("Ravi Alpha detail:", detail_view(path, user_id=2, workspace_id=1, note_id=101))
    print("Ravi Beta list:", list_view(path, user_id=2, workspace_id=2))
    print("Lee Beta list:", list_view(path, user_id=3, workspace_id=2))
    print("visitor Alpha:", list_view(path, user_id=None, workspace_id=1))
    artifact = build_export(path, user_id=1, workspace_id=1, note_ids=[101])
    print("Mina own export:", json.loads(download_export(path, user_id=1, artifact=artifact)))
    print("Lee downloads Mina export:", response(lambda: download_export(path, user_id=3, artifact=artifact)))
    notes_before = snapshot(path)["notes"]
    revoke_member(path, actor_id=3, workspace_id=1, target_user_id=1)
    print("stored Mina membership:", snapshot(path)["memberships"][0])
    print("next list:", list_view(path, user_id=1, workspace_id=1))
    print("next detail:", detail_view(path, user_id=1, workspace_id=1, note_id=101))
    print("next export build:", response(lambda: build_export(path, user_id=1, workspace_id=1, note_ids=[101])))
    print("cached export download:", response(lambda: download_export(path, user_id=1, artifact=artifact)))
    print("notes unchanged by revocation:", snapshot(path)["notes"] == notes_before)
    print("Lee still reads Alpha:", detail_view(path, user_id=3, workspace_id=1, note_id=101)[0])
    print("Ravi still reads Beta:", detail_view(path, user_id=2, workspace_id=2, note_id=202)[0])
