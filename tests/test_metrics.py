import pandas as pd
import pytest
from backtester.metrics import max_drawdown

def test_max_drawdown_basic():
    equity = pd.Series([200, 220, 176, 250, 225])
    result = max_drawdown(equity)
    assert result == pytest.approx(-0.2)