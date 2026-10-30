from backtester.data import load_prices
from backtester.engine import run
from backtester.metrics import max_drawdown, total_return, sharpe_ratio
from backtester.strategy import BuyAndHold

prices = load_prices("data/reliance_daily.csv")
equity = run(prices, BuyAndHold(), cash=100000)

print(f"Final value:  {equity.iloc[-1]:.2f}")
print(f"Total return: {total_return(equity):.2%}")
print(f"Max drawdown: {max_drawdown(equity):.2%}")
print(f"Sharpe ratio: {sharpe_ratio(equity):.2f}")