import sys

from backtester.data import load_prices
from backtester.metrics import max_drawdown, total_return
from backtester.strategy import BuyAndHold, MovingAverageCrossover
from backtester.walkforward import make_windows, pick_best_pair, run_test_window

CASH = 100000
FEE_RATE = 0.00135
SLIPPAGE_RATE = 0.0005
PAIRS = [(10, 50), (20, 50), (20, 100), (30, 100), (50, 200)]

name = sys.argv[1] if len(sys.argv) > 1 else "reliance"
prices = load_prices(f"data/{name}_daily.csv")
print(f"Stock: {name}")

windows = make_windows(len(prices), train_size=756, test_size=252)

print(f"{'Win':>3} {'Pair':>9}  {'Test period':<25} {'Crossover':>10} {'Buy-hold':>9} "
      f"{'Cross DD':>9} {'Hold DD':>9}")
cross_returns = []
hold_returns = []
cross_dds = []
hold_dds = []

for i, (train_start, test_start, test_end) in enumerate(windows, start=1):
    short_w, long_w = pick_best_pair(prices, train_start, test_start, PAIRS, CASH,
                                     FEE_RATE, SLIPPAGE_RATE)
    crossover = run_test_window(prices, MovingAverageCrossover(short_w, long_w),
                                test_start, test_end, warmup=long_w, cash=CASH,
                                fee_rate=FEE_RATE, slippage_rate=SLIPPAGE_RATE)
    hold = run_test_window(prices, BuyAndHold(), test_start, test_end,
                           warmup=0, cash=CASH,
                           fee_rate=FEE_RATE, slippage_rate=SLIPPAGE_RATE)
    cross_ret = total_return(crossover)
    hold_ret = total_return(hold)
    cross_dd = max_drawdown(crossover)
    hold_dd = max_drawdown(hold)
    cross_returns.append(cross_ret)
    hold_returns.append(hold_ret)
    cross_dds.append(cross_dd)
    hold_dds.append(hold_dd)
    period = f"{prices.index[test_start].date()} to {prices.index[test_end - 1].date()}"
    print(f"{i:>3} {str((short_w, long_w)):>9}  {period:<25} {cross_ret:>10.2%} {hold_ret:>9.2%} "
          f"{cross_dd:>9.2%} {hold_dd:>9.2%}")

wins = sum(c > h for c, h in zip(cross_returns, hold_returns))
print(f"\nCrossover beat buy-and-hold in {wins} of {len(windows)} windows")
print(f"Average return: crossover {sum(cross_returns) / len(cross_returns):.2%}, "
      f"buy-and-hold {sum(hold_returns) / len(hold_returns):.2%}")

smaller = sum(c > h for c, h in zip(cross_dds, hold_dds))
print(f"Crossover had the smaller drawdown in {smaller} of {len(windows)} windows")
print(f"Average max drawdown: crossover {sum(cross_dds) / len(cross_dds):.2%}, "
      f"buy-and-hold {sum(hold_dds) / len(hold_dds):.2%}")