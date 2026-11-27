from note_models import NoteDraft


def require_owner(draft: NoteDraft) -> int:
    owner_id = draft.owner_id
    if owner_id is None:
        raise ValueError("owner is not assigned")
    return owner_id


draft = NoteDraft(workspace="Alpha", title="Release plan", owner_id=42)
print(require_owner(draft))
