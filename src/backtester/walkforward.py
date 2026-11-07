import math
import pandas as pd
from backtester.engine import run
from backtester.metrics import sharpe_ratio
from backtester.strategy import MovingAverageCrossover

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

def pick_best_pair(prices: pd.DataFrame, train_start: int, train_end: int,
                   pairs: list[tuple[int, int]], cash: float,
                   fee_rate: float = 0.0, slippage_rate: float = 0.0) -> tuple[int, int]:
    """Return the (short, long) pair with the highest Sharpe on the train window.

    All pairs are scored on the same rows: from train_start + the biggest long window
    up to train_end. Each pair gets its own warm-up (its long window).
    """
    max_long = max(long_w for _, long_w in pairs)
    score_start = train_start + max_long        # the "same starting line" for everyone
    best_pair = pairs[0]
    best_score = float("-inf")
    for short_w, long_w in pairs:
        equity = run_test_window(prices, MovingAverageCrossover(short_w, long_w),
                                 test_start=score_start, test_end=train_end,
                                 warmup=long_w, cash=cash,
                                 fee_rate=fee_rate, slippage_rate=slippage_rate)
        score = sharpe_ratio(equity)
        if math.isnan(score):                   
            score = float("-inf")
        if score > best_score:                 
            best_pair = (short_w, long_w)
            best_score = score
    return best_pair