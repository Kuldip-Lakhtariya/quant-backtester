import pandas as pd
import pytest
from backtester.metrics import max_drawdown, total_return, sharpe_ratio

def test_max_drawdown_basic():
    equity = pd.Series([200, 220, 176, 250, 225])
    result = max_drawdown(equity)
    assert result == pytest.approx(-0.2)

def test_total_return_basic():
    equity = pd.Series([200, 220, 176, 250, 225])
    result = total_return(equity)
    assert result == pytest.approx(0.125)

def test_sharpe_ratio_basic():
    equity = pd.Series([200, 220, 176, 250, 225])
    result = sharpe_ratio(equity)
    assert result == pytest.approx(3.2, abs=0.01)