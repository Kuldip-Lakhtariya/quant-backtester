import pandas as pd

def max_drawdown(equity: pd.Series) -> float: 
    peak = equity.cummax()
    drawdown = (equity/ peak) - 1
    maxdrawdown = drawdown.min()
    return maxdrawdown

def total_return(equity: pd.Series) -> float:
    start = equity.iloc[0]
    end = equity.iloc[-1]
    return end / start - 1

def sharpe_ratio(equity: pd.Series) -> float:
    daily_returns = equity.pct_change()
    daily_average = daily_returns.mean()
    daily_std = daily_returns.std()
    return (daily_average/daily_std) * 252 ** 0.5
