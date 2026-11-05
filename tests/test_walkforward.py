from backtester.walkforward import make_windows


def test_make_windows_basic():
    expected = [(0, 4, 6), (2, 6, 8), (4, 8, 10)]
    assert make_windows(10, 4, 2) == expected


def test_make_windows_too_short():
    assert make_windows(5, 4, 2) == []