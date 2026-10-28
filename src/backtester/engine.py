import pandas as pd


def run(prices: pd.DataFrame) -> None:
    for today in range(len(prices)):
        history = prices.iloc[: today + 1]
        if today < 3 or today == len(prices) - 1:
            print(today, len(history), history.index[-1].date())