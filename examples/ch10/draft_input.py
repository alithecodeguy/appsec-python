from note_models import NoteDraft


def parse_note_draft(payload: object) -> NoteDraft:
    if not isinstance(payload, dict):
        raise ValueError("draft input must be an object")
    for name in ("workspace", "title"):
        if name not in payload:
            raise ValueError(f"missing field {name}")
    if set(payload) - {"workspace", "title", "owner_id", "body"}:
        raise ValueError("unexpected fields")
    return NoteDraft(
        workspace=payload["workspace"],
        title=payload["title"],
        owner_id=payload.get("owner_id"),
        body=payload.get("body", ""),
    )
