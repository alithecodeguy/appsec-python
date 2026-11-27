from hypothesis import strategies as st

from examples.ch30.fixtures import NoteRecord, WorkspaceCase


@st.composite
def workspace_cases(draw):
    alpha, beta = draw(st.lists(st.integers(min_value=1, max_value=20),
                                min_size=2, max_size=2, unique=True))
    rows = draw(st.lists(
        st.tuples(
            st.integers(min_value=1, max_value=10_000),
            st.sampled_from((alpha, beta)),
            st.text(alphabet="abcABC<&>برنامهانتشار", min_size=1, max_size=24),
        ),
        unique_by=lambda row: row[0],
        min_size=0,
        max_size=8,
    ))
    return WorkspaceCase(alpha, beta, tuple(NoteRecord(*row) for row in rows))
