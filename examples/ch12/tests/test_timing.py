import pytest

from preview_counts import count_records
import timing


@pytest.fixture
def fixed_counter(monkeypatch):
    readings = iter((10.0, 10.25))

    def counter():
        return next(readings)

    monkeypatch.setattr(timing, "perf_counter", counter)


def test_timed_preview_preserves_result_and_metadata(
    note_inventory, fixed_counter, capsys
):
    wrapped = timing.timed(count_records)

    result = wrapped(note_inventory, limit=3)

    assert result == 3
    assert wrapped.__name__ == "count_records"
    assert wrapped.__doc__ == count_records.__doc__
    assert wrapped.__wrapped__ is count_records
    captured = capsys.readouterr()
    assert captured.out == "count_records duration_seconds=0.250000\n"
    assert captured.err == ""


def test_timer_preserves_the_operation_error(fixed_counter, capsys):
    failure = ValueError("synthetic operation failure")

    def failing_operation():
        raise failure

    wrapped = timing.timed(failing_operation)
    with pytest.raises(ValueError) as raised:
        wrapped()

    assert raised.value is failure
    assert capsys.readouterr().out == "failing_operation duration_seconds=0.250000\n"
