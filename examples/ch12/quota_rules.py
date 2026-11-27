def can_add_note(*, current_count: int, note_limit: int = 3) -> bool:
    if type(current_count) is not int or current_count < 0:
        raise ValueError("current_count must be a nonnegative integer")
    if type(note_limit) is not int or note_limit < 1:
        raise ValueError("note_limit must be a positive integer")
    return current_count < note_limit
