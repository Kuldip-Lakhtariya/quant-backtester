from backtester.data import load_prices
from backtester.walkforward import make_windows

prices = load_prices("data/reliance_daily.csv")
windows = make_windows(len(prices), train_size=756, test_size=252)

print(f"Rows: {len(prices)}, windows: {len(windows)}")
for i, (train_start, test_start, test_end) in enumerate(windows, start=1):
    train_from = prices.index[train_start].date()
    train_to = prices.index[test_start - 1].date()
    test_from = prices.index[test_start].date()
    test_to = prices.index[test_end - 1].date()
    print(f"{i}: train {train_from} to {train_to} | test {test_from} to {test_to}")