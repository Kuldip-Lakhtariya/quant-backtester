import pytest
from  backtester.portfolio import Portfolio
import pandas as pd
from backtester.engine import run

def test_buy_all_with_fee_and_slippage():
    p = Portfolio(cash=1000, fee_rate=0.01, slippage_rate=0.01)
    p.buy_all(100)
    assert p.shares == 9
    assert p.cash == pytest.approx(81.91)

def test_sell_all_with_fee_and_slippage():
    p = Portfolio(cash=1000, fee_rate=0.01, slippage_rate=0.01)
    p.buy_all(100)
    p.sell_all(110)
    assert p.shares == 0
    assert p.cash == pytest.approx(1052.209)

class AlwaysBuy:
    def on_bar(self, history):
        return "buy"


def test_engine_passes_costs_to_portfolio():
    prices = pd.DataFrame({"Open": [100, 100, 100], "Close": [100, 100, 110]})
    equity = run(prices, AlwaysBuy(), cash=1000, fee_rate=0.01, slippage_rate=0.01)
    assert equity.iloc[1] == pytest.approx(981.91)
    assert equity.iloc[2] == pytest.approx(1071.91)