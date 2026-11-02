from backtester.data import load_prices

prices = load_prices("data/reliance_daily.csv")
cut = int(len(prices) * 0.7)
train = prices.iloc[:cut]
test = prices.iloc[cut:]

print(f"Total rows: {len(prices)}")
print(f"Train: {len(train)} rows, {train.index[0].date()} to {train.index[-1].date()}")
print(f"Test:  {len(test)} rows, {test.index[0].date()} to {test.index[-1].date()}")