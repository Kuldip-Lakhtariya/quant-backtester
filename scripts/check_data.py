from backtester.data import load_prices

for name in ["reliance", "tcs", "zydus"]:
    prices = load_prices(f"data/{name}_daily.csv")
    moves = prices["Close"].pct_change().abs()
    print(f"{name}: rows={len(prices)}, "
          f"{prices.index[0].date()} to {prices.index[-1].date()}, "
          f"min close={prices['Close'].min():.2f}, "
          f"biggest 1-day move={moves.max():.1%} on {moves.idxmax().date()}")