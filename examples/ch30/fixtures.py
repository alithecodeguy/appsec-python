from dataclasses import dataclass

from examples.ch23.authorization_service import unit


@dataclass(frozen=True)
class NoteRecord:
    id: int
    workspace_id: int
    title: str


@dataclass(frozen=True)
class WorkspaceCase:
    alpha: int
    beta: int
    notes: tuple[NoteRecord, ...]


BASE_CASE = WorkspaceCase(1, 2, (
    NoteRecord(101, 1, "برنامه انتشار"),
    NoteRecord(202, 2, "Pricing review"),
))


def install_case(database, case):
    # Privileged fixture replacement, only in the disposable database created by the tests.
    assert case.alpha != case.beta
    assert len(case.notes) <= 8
    assert len({note.id for note in case.notes}) == len(case.notes)
    assert all(note.workspace_id in (case.alpha, case.beta) for note in case.notes)
    with unit(database, write=True) as db:
        for table in ("notes", "memberships", "users", "workspaces"):
            db.execute(f"DELETE FROM {table}")
        db.executemany("INSERT INTO workspaces VALUES (?,?)",
                       [(case.alpha, "Alpha"), (case.beta, "Beta")])
        db.executemany("INSERT INTO users VALUES (?,?,1)",
                       [(1, "Mina"), (2, "Ravi"), (3, "Lee")])
        db.executemany("INSERT INTO memberships VALUES (?,?,?,1)",
                       [(case.alpha, 1, "member"), (case.beta, 2, "member"),
                        (case.alpha, 3, "manager")])
        values = []
        for note in case.notes:
            owner = 1 if note.workspace_id == case.alpha else 2
            values.append((note.id, note.workspace_id, owner, note.title,
                           f"private body {note.id}", "open", 1, owner))
        db.executemany("INSERT INTO notes VALUES (?,?,?,?,?,?,?,?)", values)


def assert_note_rows(case, workspace_id, rows):
    # Independent oracle: derive expected records from the input, not the production query.
    expected = [
        {"id": note.id, "workspace_id": note.workspace_id, "title": note.title}
        for note in sorted(case.notes, key=lambda note: note.id)
        if note.workspace_id == workspace_id
    ]
    assert isinstance(rows, list)
    assert all(isinstance(row, dict) and set(row) == {"id", "workspace_id", "title"}
               for row in rows), "unexpected response fields"
    assert all(row["workspace_id"] == workspace_id for row in rows), "foreign workspace"
    assert rows == expected, (rows, expected)
