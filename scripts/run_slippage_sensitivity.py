from backtester.data import load_prices
from backtester.engine import run
from backtester.metrics import total_return
from backtester.strategy import BuyAndHold, MovingAverageCrossover

FEE_RATE = 0.00135
SLIPPAGE_RATES = [0.0, 0.0005, 0.001]

prices = load_prices("data/reliance_daily.csv")
cut = int(len(prices) * 0.7)
test = prices.iloc[cut:]

print(f"Fee rate fixed at {FEE_RATE:.3%}")
print(f"{'Slippage':>10} | {'Crossover 30/100':>17} | {'Buy-and-hold':>13}")

for slip in SLIPPAGE_RATES:
    crossover = run(test, MovingAverageCrossover(30, 100), cash=100000,
                    fee_rate=FEE_RATE, slippage_rate=slip)
    hold = run(test, BuyAndHold(), cash=100000,
               fee_rate=FEE_RATE, slippage_rate=slip)
    print(f"{slip:>10.3%} | {total_return(crossover):>17.2%} | {total_return(hold):>13.2%}")