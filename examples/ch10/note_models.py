from dataclasses import dataclass, field, replace
from enum import Enum


class NoteState(Enum):
    DRAFT = "draft"
    PUBLISHED = "published"


@dataclass(frozen=True, kw_only=True)
class NoteDraft:
    workspace: str
    title: str
    owner_id: int | None = None
    body: str = field(default="", repr=False)
    state: NoteState = NoteState.DRAFT

    def __post_init__(self) -> None:
        if not isinstance(self.workspace, str):
            raise ValueError("workspace must be text")
        if self.workspace not in ("Alpha", "Beta"):
            raise ValueError("unknown workspace")
        if not isinstance(self.title, str):
            raise ValueError("title must be text")
        if not 1 <= len(self.title) <= 120 or not self.title.strip():
            raise ValueError("title must contain text within 120 code points")
        if self.owner_id is not None:
            if type(self.owner_id) is not int or not 1 <= self.owner_id <= 999999:
                raise ValueError("owner_id must be an integer from 1 to 999999")
        if not isinstance(self.body, str) or len(self.body) > 4096:
            raise ValueError("body must be text within 4096 code points")
        if not isinstance(self.state, NoteState):
            raise ValueError("state must be a NoteState")
        if self.state is NoteState.PUBLISHED and self.owner_id is None:
            raise ValueError("published note requires an owner")

    def publish(self) -> "NoteDraft":
        if self.state is not NoteState.DRAFT:
            raise ValueError("only a draft can be published")
        return replace(self, state=NoteState.PUBLISHED)
