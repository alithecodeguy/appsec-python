from note_models import NoteDraft

draft = NoteDraft(workspace="Alpha", title="Release plan", owner_id="42")


def require_owner(draft: NoteDraft) -> int:
    return draft.owner_id
