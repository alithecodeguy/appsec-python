from dataclasses import asdict

from note_models import NoteDraft

draft = NoteDraft(
    workspace="Alpha",
    title="برنامه انتشار",
    owner_id=42,
    body="Private release details",
)
published = draft.publish()

print("Original state", draft.state.value)
print("New state", published.state.value)
print("Same instance", draft is published)
print("Body shown in repr", "Private release details" in repr(draft))
print("Body included by asdict", "body" in asdict(draft))
