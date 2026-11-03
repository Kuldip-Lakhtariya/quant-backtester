from backtester.data import load_prices
from backtester.engine import run
from backtester.metrics import max_drawdown, total_return, sharpe_ratio
from backtester.strategy import BuyAndHold, MovingAverageCrossover

prices = load_prices("data/reliance_daily.csv")
cut = int(len(prices) * 0.7)
test = prices.iloc[cut:]

results = {
    "Crossover 30/100": run(test, MovingAverageCrossover(30, 100), cash=100000),
    "Buy-and-hold": run(test, BuyAndHold(), cash=100000),
}

for name, equity in results.items():
    print(name)
    print(f"  Final value:  {equity.iloc[-1]:.2f}")
    print(f"  Total return: {total_return(equity):.2%}")
    print(f"  Max drawdown: {max_drawdown(equity):.2%}")
    print(f"  Sharpe ratio: {sharpe_ratio(equity):.2f}")