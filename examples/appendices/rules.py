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


if __name__ == "__main__":
    print("Mina", may_read(signed_in=True, membership_active=True,
        reader_workspace="Alpha", note_workspace="Alpha", role="member"))
    print("Ravi", may_read(signed_in=True, membership_active=True,
        reader_workspace="Beta", note_workspace="Alpha", role="member"))
