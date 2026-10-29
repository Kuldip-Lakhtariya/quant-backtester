import pandas as pd

from backtester.engine import run
from backtester.strategy import BuyAndHold


def test_buy_fills_at_next_open():
    prices = pd.DataFrame(
        {"Open": [100, 104, 108], "Close": [102, 110, 120]},
        index=pd.to_datetime(["2024-01-01", "2024-01-02", "2024-01-03"]),
    )
    equity = run(prices, BuyAndHold(), cash=1000)
    assert list(equity) == [1000, 1054, 1144]