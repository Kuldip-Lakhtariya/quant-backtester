import pandas as pd


def run(prices: pd.DataFrame, strategy) -> list[str]:
    signals = []
    for today in range(len(prices)):
        history = prices.iloc[: today + 1]
        signals.append(strategy.on_bar(history))
    return signals