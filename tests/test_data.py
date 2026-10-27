import pandas as pd
import pytest

from backtester.data import load_prices


def write_csv(tmp_path, text):
    f = tmp_path / "prices.csv"
    f.write_text(text)
    return str(f)


def test_unsorted_dates_raise(tmp_path):
    path = write_csv(tmp_path, "date,Close\n2024-01-02,100\n2024-01-01,101\n2024-01-03,102\n")
    with pytest.raises(ValueError, match="not sorted"):
        load_prices(path)


def test_duplicate_dates_raise(tmp_path):
    path = write_csv(tmp_path, "date,Close\n2024-01-01,100\n2024-01-01,101\n2024-01-03,102\n")
    with pytest.raises(ValueError, match="duplicate"):
        load_prices(path)


def test_missing_close_raises(tmp_path):
    path = write_csv(tmp_path, "date,Close\n2024-01-01,100\n2024-01-02,\n2024-01-03,102\n")
    with pytest.raises(ValueError, match="missing"):
        load_prices(path)


def test_good_file_loads(tmp_path):
    path = write_csv(tmp_path, "date,Close\n2024-01-01,100\n2024-01-02,101\n2024-01-03,102\n")
    df = load_prices(path)
    assert len(df) == 3
    assert isinstance(df.index, pd.DatetimeIndex)