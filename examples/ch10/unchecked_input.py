from dataclasses import dataclass
import json


@dataclass
class OwnerInput:
    owner_id: int | None = None


payload = json.loads('{"owner_id": "42"}')
supplied = OwnerInput(owner_id=payload["owner_id"])
print(type(supplied.owner_id).__name__)
