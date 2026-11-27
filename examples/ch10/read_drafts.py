import json
from pathlib import Path

from draft_input import parse_note_draft

with Path("drafts.json").open("r", encoding="utf-8") as source:
    payloads = json.load(source)
if not isinstance(payloads, list):
    raise ValueError("draft file must contain a list")

for number, payload in enumerate(payloads, start=1):
    try:
        draft = parse_note_draft(payload)
    except ValueError as error:
        print(number, "Rejected", str(error))
    else:
        print(number, "Accepted", draft.owner_id, draft.state.value)
