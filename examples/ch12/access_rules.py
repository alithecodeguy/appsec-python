def may_read(
    *,
    signed_in,
    membership_active,
    reader_workspace,
    note_workspace,
    role,
):
    """Return whether the supplied reader facts permit this note read."""
    if not signed_in:
        return False
    if not membership_active:
        return False
    if reader_workspace != note_workspace:
        return False
    return role in ("member", "manager")
