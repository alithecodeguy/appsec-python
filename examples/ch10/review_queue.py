from dataclasses import dataclass, field

from note_models import NoteDraft


@dataclass
class ReviewQueue:
    drafts: list[NoteDraft] = field(default_factory=list)


first_queue = ReviewQueue()
second_queue = ReviewQueue()
first_queue.drafts.append(NoteDraft(workspace="Alpha", title="Release plan"))

print("First queue", len(first_queue.drafts))
print("Second queue", len(second_queue.drafts))
print("Shared list", first_queue.drafts is second_queue.drafts)
