import pandas as pd


def load_prices(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, parse_dates=["date"], index_col="date")
    if not df.index.is_monotonic_increasing:
        raise ValueError("dates are not sorted")
    if not df.index.is_unique:
        raise ValueError("duplicate dates")
    if df["Close"].isna().any():
        raise ValueError("missing close prices")
    return df