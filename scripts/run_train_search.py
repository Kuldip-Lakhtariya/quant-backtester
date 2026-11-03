from backtester.data import load_prices
from backtester.engine import run
from backtester.metrics import max_drawdown, total_return, sharpe_ratio
from backtester.strategy import MovingAverageCrossover

prices = load_prices("data/reliance_daily.csv")
cut = int(len(prices) * 0.7)
train = prices.iloc[:cut]

pairs = [(10, 50), (20, 50), (20, 100), (30, 100), (50, 200)]

print("short long   return  drawdown  sharpe")
for short_w, long_w in pairs:
    equity = run(train, MovingAverageCrossover(short_w, long_w), cash=100000)
    print(f"{short_w:>5} {long_w:>4} {total_return(equity):>8.2%} {max_drawdown(equity):>9.2%} {sharpe_ratio(equity):>7.2f}")