from examples.appendices.rules import may_read

facts = {"signed_in": True, "membership_active": True,
         "reader_workspace": "Alpha", "note_workspace": "Alpha", "role": "member"}

assert may_read(**facts)
facts["membership_active"] = False
assert not may_read(**facts)

# Keep the other facts valid so the unknown-role check actually reaches the role decision.
facts["membership_active"] = True
facts["role"] = "unknown"
assert not may_read(**facts)

facts["role"] = "manager"
facts["reader_workspace"] = "Beta"
assert not may_read(**facts)
