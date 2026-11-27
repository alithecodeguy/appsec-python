class NoteDraft:
    def __init__(self, title: str) -> None:
        self.title = title

    def title_length(self) -> int:
        return len(self.title)


draft = NoteDraft(title="برنامه انتشار")
print(draft.title)
print(draft.title_length())
