from backtester.portfolio import Portfolio


def test_buy_all_uses_whole_shares():
    p = Portfolio(cash=1000)
    p.buy_all(price=300)
    assert p.shares == 3
    assert p.cash == 100


def test_value_after_price_rise():
    p = Portfolio(cash=1000)
    p.buy_all(price=100)
    assert p.shares == 10
    assert p.value(price=110) == 1100