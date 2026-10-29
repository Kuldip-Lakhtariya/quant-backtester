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
