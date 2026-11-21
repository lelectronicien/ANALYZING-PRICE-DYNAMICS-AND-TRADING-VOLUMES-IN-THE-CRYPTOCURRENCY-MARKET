import pandas as pd
from src.coverage import audit_coverage


def frame():
    dates = pd.date_range("2020-02-28", "2020-03-01", freq="D", tz="UTC")
    return pd.DataFrame({"symbol": ["BTCUSDT"]*len(dates), "open_time": dates,
                         "open": [100.]*len(dates), "high": [102.]*len(dates),
                         "low": [99.]*len(dates), "close": [101.]*len(dates),
                         "volume_base": [5.]*len(dates), "volume_quote": [505.]*len(dates)})


def test_leap_day_included():
    report = audit_coverage(frame(), "BTCUSDT", "2020-02-28", "2020-03-02")
    assert report["expected_days"] == 3
    assert report["complete"]


def test_missing_day_detected():
    report = audit_coverage(frame().iloc[[0, 2]], "BTCUSDT", "2020-02-28", "2020-03-02")
    assert report["missing_dates"] == ["2020-02-29"]
    assert not report["complete"]


def test_duplicate_and_invalid_candle():
    df = pd.concat([frame(), frame().iloc[[0]]], ignore_index=True)
    df.loc[0, "high"] = 98
    report = audit_coverage(df, "BTCUSDT", "2020-02-28", "2020-03-02")
    assert report["duplicate_dates"]
    assert report["invalid_ohlc_rows"] == 1
    assert not report["complete"]
