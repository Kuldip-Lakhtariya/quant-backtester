import pandas as pd

from backtester.strategy import MovingAverageCrossover


def test_crossover_sells_when_short_is_below_long():
    history = pd.DataFrame({"Close": [12, 11, 10]})
    strategy = MovingAverageCrossover(2, 3)
    result = strategy.on_bar(history)
    assert result == "sell"

def test_crossover_holds_when_not_enough_data():
    history = pd.DataFrame({"Close": [12, 11]})
    strategy = MovingAverageCrossover(2, 3)
    result = strategy.on_bar(history)
    assert result == "hold"