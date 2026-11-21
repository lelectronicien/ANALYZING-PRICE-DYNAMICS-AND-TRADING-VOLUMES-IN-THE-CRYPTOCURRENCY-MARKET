import numpy as np
import pandas as pd
import pytest
from src.features import make_features
from src.fetch_ohlcv import utc_ms


def sample():
    dates = pd.date_range("2024-01-01", periods=12, freq="D", tz="UTC")
    return pd.DataFrame({"symbol": ["BTCUSDT"]*12, "open_time": dates,
                         "close": [100.0 * (1.01**i) for i in range(12)],
                         "volume_quote": [1000.0 + i for i in range(12)]})


def test_returns_and_rolling_window():
    result = make_features(sample())
    assert np.isnan(result.loc[0, "log_return"])
    assert result.loc[1, "log_return"] == pytest.approx(np.log(1.01))
    assert np.isnan(result.loc[6, "realized_var_7d"])
    assert result.loc[7, "realized_var_7d"] == pytest.approx(7 * np.log(1.01)**2)


def test_duplicate_dates_rejected():
    df = pd.concat([sample(), sample().iloc[[0]]], ignore_index=True)
    with pytest.raises(ValueError, match="Duplicate"):
        make_features(df)


def test_utc_day():
    assert utc_ms("2024-01-02") - utc_ms("2024-01-01") == 86_400_000
