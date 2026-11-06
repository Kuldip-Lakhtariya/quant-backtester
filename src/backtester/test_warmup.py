import pandas as pd
import pytest

from backtester.walkforward import run_test_window


class BuyAfter:
    """Says buy once it has seen n rows of history, otherwise hold."""

    def __init__(self, n: int) -> None:
        self.n = n

    def on_bar(self, history):
        return "buy" if len(history) >= self.n else "hold"


def make_prices() -> pd.DataFrame:
    price = [100, 100, 100, 100, 100, 100, 110, 110, 110, 110]
    return pd.DataFrame({"Open": price, "Close": price})


def test_warmup_lets_strategy_trade_on_first_test_day():
    equity = run_test_window(make_prices(), BuyAfter(3), test_start=5, test_end=10,
                             warmup=3, cash=1000)
    assert equity.iloc[0] == pytest.approx(1000)   
    assert equity.iloc[-1] == pytest.approx(1100)  

def test_no_warmup_strategy_buys_late():
    equity = run_test_window(make_prices(), BuyAfter(3), test_start=5, test_end=10,
                             warmup=0, cash=1000)
    assert equity.iloc[-1] == pytest.approx(1000)  