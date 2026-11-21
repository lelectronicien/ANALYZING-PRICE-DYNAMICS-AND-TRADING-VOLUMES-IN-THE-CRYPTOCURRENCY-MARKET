import numpy as np
import pandas as pd
from src.walk_forward import walk_forward, score_forecasts


def synthetic(n=55):
    dates = pd.date_range("2023-01-01", periods=n, freq="D", tz="UTC")
    return pd.DataFrame({"symbol": ["BTCUSDT"]*n, "open_time": dates,
                         "close": 100*np.exp(np.cumsum(0.01*np.sin(np.arange(n)))),
                         "volume_quote": 1000+10*np.arange(n)})


def test_walk_forward_origin_and_score():
    forecast = walk_forward(synthetic(), min_train=30, step=5)
    assert set(forecast.model) == {"ar_abs_return", "ar_plus_volume"}
    assert len(forecast) > 0
    assert (pd.to_datetime(forecast.target_date) - pd.to_datetime(forecast.origin_date)
            == pd.Timedelta(days=1)).all()
    assert (forecast.train_rows >= 30).all()
    scores = score_forecasts(forecast)
    assert len(scores) == 2
    assert (scores.mae >= 0).all()
