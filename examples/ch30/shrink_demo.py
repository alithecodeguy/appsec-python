from pathlib import Path
from tempfile import TemporaryDirectory

from hypothesis import find, settings

from examples.ch23.authorization_service import seed
from examples.ch30.fixtures import install_case
from examples.ch30.strategies import workspace_cases
from examples.ch30.test_local import global_list


def leaks(case):
    with TemporaryDirectory(prefix="casebook-ch30-shrink-") as folder:
        database = Path(folder) / "notes.sqlite3"
        seed(database)
        install_case(database, case)
        rows = global_list(database, user_id=1, workspace_id=case.alpha)
        return any(row["workspace_id"] != case.alpha for row in rows)


if __name__ == "__main__":
    counterexample = find(workspace_cases(), leaks,
        settings=settings(max_examples=500, deadline=None, database=None, derandomize=True))
    print(counterexample)
    assert leaks(counterexample)
