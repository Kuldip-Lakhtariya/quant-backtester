# quant-backtester

A backtesting engine for trading strategies, built from scratch in Python (pandas and NumPy). It uses no ready-made backtesting library. It tests strategies on daily Indian stock data, with realistic costs and an honest out-of-sample evaluation.

> This is a learning and research project with paper results only. It is not financial advice.

## The question

Does a moving-average crossover beat buy-and-hold on large Indian stocks, after costs, when it is tested on data it has never seen?

**Short answer: not on average.** Across three stocks and 24 test years, buy-and-hold had the higher average return every time. The crossover often had a shallower drawdown, especially in years when the market fell.

## Results (walk-forward, with costs)

Each stock has 8 test windows of about one year each (first test starts 2018-01-23, last test ends 2026-03-23). Costs are included in every number. Returns are simple averages of the 8 yearly returns, not compounded.

| Stock | Windows won by crossover (return) | Average return: crossover / buy-and-hold | Average max drawdown: crossover / buy-and-hold | Windows with smaller drawdown |
|---|---|---|---|---|
| Reliance | 2 of 8 | 6.44% / 16.94% | -19.69% / -21.89% | 5 of 8 |
| TCS | 3 of 8 | 5.38% / 10.70% | -16.28% / -19.46% | 4 of 8 |
| Zydus Lifesciences | 6 of 8 | 15.84% / 17.16% | -16.71% / -24.95% | 6 of 8 |

The full per-window tables are in the `results/` folder.

**What the numbers say**

- Buy-and-hold had the higher average return on all three stocks.
- The crossover lost less in falling years. Example: Zydus in 2019-20 had a max drawdown of -4.78% for the crossover and -37.09% for buy-and-hold.
- The crossover lagged in strong rallies. In the 2023-24 window it earned less than buy-and-hold on all three stocks.
- Zydus shows that winning most windows is not the same as winning on average. The crossover won 6 of 8 windows, but by small amounts. It lost 2 windows by a lot (for example -17.47% against +29.14% in 2022-23), so its average was still lower.
- Many of the "smaller drawdown" wins are near-ties (differences under 0.2 points). The big differences are in years with a large fall.
- The best (short, long) pair chosen on the training data changed from window to window, for example (50, 200), (20, 50) and (10, 50) for Reliance. This means the choice from training data is noisy.

## How it works

### Engine rules

- The strategy sees only the history up to today (`prices.iloc[: today + 1]`). The engine, not the strategy, controls this, so the strategy cannot look at the future.
- A decision made after today's close is filled at the next day's open.
- The portfolio holds cash and whole shares. `buy_all` and `sell_all` trade the full position. There is one position at a time.

### Costs

- **Fee:** one rate of 0.135% per trade side. I estimated it from Groww's delivery charges for a trade of about 1,00,000 rupees (brokerage, STT of 0.1% on buy and sell, stamp duty on buy, exchange and SEBI charges, GST) and checked the breakdown against Groww's charges page.
- **Slippage:** a fixed 0.05% worse price on every trade (buy higher, sell lower). This is an assumption, not a measurement.
- Costs are applied to both buying and selling, and the number of shares is chosen so that the fee can always be paid.
- **Cost sensitivity** (Reliance, single test period, fee fixed at 0.135%):

| Slippage | Crossover 30/100 | Buy-and-hold |
|---|---|---|
| 0.00% | -4.68% | 14.14% |
| 0.05% | -5.11% | 14.09% |
| 0.10% | -5.51% | 14.04% |

The ranking never changed. Fees (mostly STT) cost the crossover more than slippage did, because it trades more often.

### Strategies

- `BuyAndHold`: buys once on the first day and holds.
- `MovingAverageCrossover(short, long)`: holds until it has `long` rows of history, then buys when the short average is above the long average and sells otherwise.

### Metrics

Total return, maximum drawdown (the biggest fall from a peak to a low point) and the Sharpe ratio (risk-free rate set to 0).

### Walk-forward evaluation

- Windows: 756 rows (about 3 years) for training, 252 rows (about 1 year) for testing, moving forward by 252 rows. The test periods never overlap, so every test day is used once.
- In each window, five (short, long) pairs are scored **on the training rows only**: (10, 50), (20, 50), (20, 100), (30, 100), (50, 200). The pair list was fixed before I looked at any walk-forward result.
- All pairs are scored on the same days (the first 200 training rows are skipped, because the slowest pair needs them). Otherwise slow pairs would sit in cash for longer and the comparison would be unfair.
- The pair with the highest Sharpe ratio (with costs) is chosen automatically, then run once on the next year.
- **Warm-up:** before each test year, the strategy is given the previous `long` rows to read, so it can trade on the first test day. Only the test year is scored. This uses past data only, so there is no look-ahead.

### The first test, before walk-forward

I first used one 70/30 split by date. The (30, 100) pair had a training Sharpe of 0.58, but on the test part it earned about 0 (-3.34% against +14.28% for buy-and-hold, before costs; -5.11% against +14.09% after costs). This is what made me move to walk-forward testing.

## Tests

The project has 22 pytest tests. Most of them check a small case that I calculated by hand first (fees and slippage on buy and sell, the engine's equity, drawdown, warm-up, the window generator, picking the best pair).

## How to run

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install pandas numpy yfinance pytest

# download data (edit the tickers at the bottom of the file first)
python scripts/download_data.py

# walk-forward evaluation for one stock (reliance, tcs or zydus)
python scripts/run_walkforward.py reliance

# tests
pytest
```

If a script says `ModuleNotFoundError: backtester`, set the path first (PowerShell): `$env:PYTHONPATH="src"`.

## Limitations

I want to be clear about what these results do not show.

- **Daily bars only.** No intraday data, no volume-based ideas.
- **Long-only, all-in, one position.** No short selling, no position sizing, no stop-loss.
- **One fee rate for buy and sell.** The real cost is a little higher on buys (stamp duty) and the flat brokerage matters more for small trades. The model assumes trades of about 1,00,000 rupees.
- **Slippage is fixed** at 0.05% and was not measured.
- **No capital gains tax.** All results are before tax.
- **Only three large, liquid stocks that still exist today.** This means survivorship bias is possible. I chose the stocks by rules (enough history, liquid, adjusted prices) and not by their returns, but they are still a small sample. Reliance rose in 7 of 8 test years, TCS in 5 of 8 and Zydus in 3 of 8, so the stocks differ a lot.
- **Only 8 test windows per stock**, and the chosen pair was unstable. These results are evidence, not proof.
- **The process was not perfectly clean.** Before I made the train/test split, I had already tried the pairs (20, 50), (30, 50) and (30, 45) on the full Reliance data. I also looked at the single test result before building walk-forward, and the later windows overlap in time with that earlier test period.
- **Buy-and-hold enters one day later than the crossover** in the walk-forward runs, because the engine fills orders at the next open and buy-and-hold has no warm-up. The effect is small.
- **The first single test had a cold start.** The crossover sat in cash for about 100 days while buy-and-hold was already invested. Walk-forward with warm-up fixes this.
- The last 129 rows of the data are not used by any test window.
- **Event risk:** Zydus rose 19.8% in one day on 2017-02-16 (news about a US regulator inspection). A strategy that is out of the market on such a day misses it. I checked this day and it is real data, not an error.

## What I learned

- Look-ahead bias, and how to prevent it in the engine instead of trusting the strategy.
- Picking the best result from several tries on the same data is overfitting. Use data the choice has never seen.
- Costs matter most for strategies that trade often.
- A strategy that needs 100 days of history has a cold-start problem, and the fix (warm-up) must not use future data.
- Winning most of the time is not the same as winning on average.
- A negative result is still a result. I report it as it is.

## Possible next steps

- More strategies (for example breakout or RSI) on the same walk-forward framework.
- A SIP comparison (monthly against weekly against buy-the-dip), which needs a cash-flow model and a fixed-plus-percentage fee.
- Charts of the returns per window and of one equity curve.
- A GitHub Actions workflow that runs the tests on every push.

## Project structure

```
src/backtester/
    data.py          load_prices with checks (sorted dates, duplicates, missing Close)
    engine.py        run(prices, strategy, cash, fee_rate, slippage_rate) -> daily equity
    portfolio.py     cash, whole shares, buy_all / sell_all with fees and slippage
    strategy.py      BuyAndHold, MovingAverageCrossover
    metrics.py       total_return, max_drawdown, sharpe_ratio
    walkforward.py   make_windows, run_test_window (warm-up), pick_best_pair
scripts/             download_data.py, check_data.py, run_walkforward.py, and the earlier
                     single-split scripts (run_split, run_train_search, run_test_once,
                     run_test_costs, run_slippage_sensitivity, show_windows)
tests/               pytest tests
results/             saved walk-forward output for each stock
data/                daily CSV files (adjusted prices)
```

## Disclaimer

This project is for learning. Past results do not predict future results. Nothing here is investment advice.

---

## Author

Kuldip Lakhtariya
B.Tech ECE, LD College of Engineering, Ahmedabad

- GitHub: [Kuldip-Lakhtariya](https://github.com/Kuldip-Lakhtariya)
- LinkedIn: [kuldip-lakhtariya](https://www.linkedin.com/in/kuldip-lakhtariya-957106371/)
- HuggingFace: [kuldip2611](https://huggingface.co/kuldip2611)
- Email: kuldip2611lakhtariya@gmail.com