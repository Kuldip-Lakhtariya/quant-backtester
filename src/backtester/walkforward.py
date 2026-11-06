import pandas as pd
from backtester.engine import run

def make_windows(n_rows: int, train_size: int, test_size: int) -> list[tuple[int, int, int]]:
    """Return (train_start, test_start, test_end) row positions. test_end is not included."""
    windows = []
    start = 0
    while start + train_size + test_size <= n_rows:
        test_start = start + train_size
        windows.append((start, test_start, test_start + test_size))
        start += test_size
    return windows

def run_test_window(prices: pd.DataFrame, strategy, test_start: int, test_end: int,
                    warmup: int, cash: float,
                    fee_rate: float = 0.0, slippage_rate: float = 0.0) -> pd.Series:
    """Run the strategy with warm-up history, return equity from the last warm-up bar on."""
    start = max(test_start - warmup, 0)
    chunk = prices.iloc[start:test_end]
    equity = run(chunk, strategy, cash, fee_rate, slippage_rate)
    begin = max(test_start - start - 1, 0)
    return equity.iloc[begin:]