import pandas as pd

def max_drawdown(equity: pd.Series) -> float: 
    peak = equity.cummax()
    drawdown = (equity/ peak) - 1
    maxdrawdown = drawdown.min()
    return maxdrawdown
