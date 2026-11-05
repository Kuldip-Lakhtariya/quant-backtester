def make_windows(n_rows: int, train_size: int, test_size: int) -> list[tuple[int, int, int]]:
    """Return (train_start, test_start, test_end) row positions. test_end is not included."""
    windows = []
    start = 0
    while start + train_size + test_size <= n_rows:
        test_start = start + train_size
        windows.append((start, test_start, test_start + test_size))
        start += test_size
    return windows