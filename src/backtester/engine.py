import pandas as pd

from backtester.portfolio import Portfolio


def run(prices: pd.DataFrame, strategy, cash: float) -> pd.Series:
    portfolio = Portfolio(cash)
    pending = "hold"  
    equity = []

    for today in range(len(prices)):
        open_price = prices["Open"].iloc[today]
        close_price = prices["Close"].iloc[today]

        if pending == "buy":
            portfolio.buy_all(open_price)
        elif pending == "sell":
            portfolio.sell_all(open_price)

        equity.append(portfolio.value(close_price))

        history = prices.iloc[: today + 1]
        pending = strategy.on_bar(history)

    return pd.Series(equity, index=prices.index)