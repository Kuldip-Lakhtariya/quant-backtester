import yfinance as yf


def download(ticker: str, start: str, end: str, out_path: str) -> None:
    df = yf.download(ticker, start=start, end=end, auto_adjust=True, progress=False)
    df.columns = df.columns.get_level_values(0)
    df.index.name = "date"
    df.to_csv(out_path)


if __name__ == "__main__":
    # Reliance is already downloaded.Comment it, so our results stay the same.
    # download("RELIANCE.NS", "2015-01-01", "2026-10-01", "data/reliance_daily.csv")
    download("TCS.NS", "2015-01-01", "2026-10-01", "data/tcs_daily.csv")
    download("ZYDUSLIFE.NS", "2015-01-01", "2026-10-01", "data/zydus_daily.csv")