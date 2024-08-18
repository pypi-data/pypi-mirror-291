import pytest
from time import sleep
from tictactoc import tictactoc


def test_tictoc():
    time_to_wait = 1
    tictactoc.tic()
    sleep(time_to_wait)
    assert pytest.approx(time_to_wait, 0.001) == tictactoc.toc()["total"]


def test_tictactoc():
    tac = 0.5
    toc = 0.34
    tictactoc.tic()
    sleep(tac)
    tictactoc.tac()
    sleep(toc)
    assert pytest.approx(tac + toc, 0.001) == tictactoc.toc()["total"]


def test_tictactoc2():
    tac = 0.3
    tac2 = 0.4
    toc = 0.2
    tictactoc.tic()
    sleep(tac)
    tictactoc.tac()
    sleep(tac2)
    tictactoc.tac()
    sleep(toc)
    assert pytest.approx(tac + tac2 + toc, 0.001) == tictactoc.toc()["total"]


def test_tictactoc_name():
    tac = 0.3
    tac2 = 0.4
    toc = 0.2
    tictactoc.tic("test")
    sleep(tac)
    tictactoc.tac("test")
    sleep(tac2)
    tictactoc.tac("test")
    sleep(toc)
    assert tictactoc.toc("test")["total"] == pytest.approx(
        tac + tac2 + toc, 0.001
    )


def test_clear_noname():
    first = 0.3
    second = 0.8
    tictactoc.tic()
    sleep(first)
    assert tictactoc.toc()["total"] == pytest.approx(first, 0.01)
    tictactoc.tic()
    sleep(second)
    assert tictactoc.toc()["total"] == pytest.approx(second, 0.01)


def test_stats():
    tac = 0.5
    tac2 = 0.2
    tac3 = 0.6
    toc = 0.1
    tictactoc.tic()
    sleep(tac)
    tictactoc.tac()
    sleep(tac2)
    tictactoc.tac()
    sleep(tac3)
    tictactoc.tac()
    sleep(toc)
    result = tictactoc.toc()
    assert result["total"] == pytest.approx(tac + tac2 + tac3 + toc, 0.01)
    assert result["steps"] == [
        pytest.approx(tac, 0.01),
        pytest.approx(tac2, 0.01),
        pytest.approx(tac3, 0.01),
        pytest.approx(toc, 0.01),
    ]


def test_active_timers():
    tictactoc.tic()
    tictactoc.tic("second timer")
    tictactoc.tic("another timer")

    active_timers = tictactoc.get_active_timers()
    assert active_timers == "__default, second timer, another timer"

    tictactoc.toc("second timer")
    active_timers = tictactoc.get_active_timers()
    assert active_timers == "__default, another timer"


def test_skip_toc():
    tictactoc.tic("my loop")

    my_loop = [1, 2]

    for element in my_loop:
        sleep(0.1)
        tictactoc.tac("my loop")

    result = tictactoc.toc("my loop", skip_toc=True)
    assert len(result["steps"]) == 2


def test_values_in_toc():
    tictactoc.tic()
    result = tictactoc.toc()
    assert "name" in result
    assert "total" in result
    assert "steps" in result
    assert len(result["name"]) > 0
    assert result["total"] >= 0
    assert len(result["steps"]) >= 0
