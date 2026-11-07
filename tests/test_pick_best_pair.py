import pandas as pd

from backtester.walkforward import pick_best_pair


def make_rising_prices(n: int = 60) -> pd.DataFrame:
    price = [100 + i for i in range(n)]   
    return pd.DataFrame({"Open": price, "Close": price})


def test_pick_best_pair_returns_one_of_the_pairs():
    pairs = [(2, 5), (3, 10)]
    best = pick_best_pair(make_rising_prices(), 0, 60, pairs, cash=100000)
    assert best in pairs


def test_pick_best_pair_tie_returns_first_pair():
    pairs = [(2, 5), (3, 10)]
    assert pick_best_pair(make_rising_prices(), 0, 60, pairs, cash=100000) == (2, 5)